"""Tests for the read-only Insights collector. No network: ig_common.api_get is
monkeypatched, which is the one choke-point every Graph call in the script
goes through (media_insights() itself calls api_get).

Protected here:
  1. Per-post failure isolation: a deleted post, a plain error, and an
     optional-extras failure each affect only their own row.
  2. Account-level aborts: a throttle or token error stops the rest of THAT
     account (no quota burn) but the next account still runs.
  3. The CSV never carries a raw token — error strings are redacted.
  4. The rollup groups reel-/carousel- prefixed types into one family.
"""
import csv
import json
from datetime import datetime, timezone

import pytest

import collect_insights as ci
import ig_common

FAKE_TOKEN = "IGAAFAKEtoken0000000000000000000000000000000000SECRETVALUE"
NOW = datetime(2026, 9, 5, 12, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    for name in ("IG_ACCESS_TOKEN", "IG_ACCESS_TOKEN_ACCT_A", "IG_ACCESS_TOKEN_ACCT_B"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(ig_common, "_SECRETS", [], raising=False)


def _post(root, account, post_id, ig_id, *, ptype="the-rule", video=False, posted="2026-09-01T14:00:00+00:00"):
    d = root / account / "content" / "posted" / post_id
    d.mkdir(parents=True)
    rec = {
        "id": post_id,
        "type": ptype,
        "caption": "x",
        "scheduled_time_ist": "2026-09-01T19:30:00+05:30",
        "status": "posted",
        "ig_post_id": ig_id,
        "posted_at": posted,
    }
    if video:
        rec["video"] = f"accounts/{account}/content/queue/video/{post_id}.mp4"
    else:
        rec["slides"] = ["a.png"]
    (d / f"{post_id}.json").write_text(json.dumps(rec), encoding="utf-8")


def _insights(**values):
    return {"data": [{"name": k, "period": "lifetime", "values": [{"value": v}]} for k, v in values.items()]}


def _fake_api(script):
    """script: {media_id: {"meta": payload|exc, "core": payload|exc, "extra": payload|exc}}"""
    calls = []

    def api_get(path, token, *, params=None, base=None, timeout=None, session=None):
        calls.append(path)
        media_id = path.split("/")[0]
        entry = script[media_id]
        if path.endswith("/insights"):
            key = "extra" if any(m in params["metric"] for m in ci.ALL_EXTRA) else "core"
        else:
            key = "meta"
        result = entry[key]
        if isinstance(result, Exception):
            raise result
        return result

    return api_get, calls


def _meta(product="FEED", media_type="CAROUSEL_ALBUM"):
    return {
        "id": "x",
        "media_type": media_type,
        "media_product_type": product,
        "permalink": "https://www.instagram.com/p/abc/",
        "like_count": 3,
        "comments_count": 1,
    }


def test_happy_path_and_family_rollup(tmp_path, monkeypatch):
    _post(tmp_path, "acct_a", "p1", "111", ptype="carousel-one-star-files")
    _post(tmp_path, "acct_a", "p2", "222", ptype="one-star-files")
    _post(tmp_path, "acct_a", "p3", "333", ptype="reel-pov", video=True)
    monkeypatch.setenv("IG_ACCESS_TOKEN_ACCT_A", FAKE_TOKEN)
    script = {
        "111": {"meta": _meta(), "core": _insights(reach=100, views=120, likes=10, comments=1, saved=2, shares=1, total_interactions=14), "extra": _insights(follows=1, profile_visits=2)},
        "222": {"meta": _meta(), "core": _insights(reach=300, views=320, likes=30, comments=3, saved=6, shares=3, total_interactions=42), "extra": _insights(follows=0, profile_visits=1)},
        "333": {"meta": _meta("REELS", "VIDEO"), "core": _insights(reach=1000, views=1500, likes=50, comments=5, saved=10, shares=20, total_interactions=85), "extra": _insights(ig_reels_avg_watch_time=4200, ig_reels_video_view_total_time=99000, reels_skip_rate=0.4)},
    }
    api_get, calls = _fake_api(script)
    monkeypatch.setattr(ig_common, "api_get", api_get)

    rows = ci.collect(tmp_path, ["acct_a"], sleep_s=0, now=NOW)
    assert [r["status"] for r in rows] == ["ok", "ok", "ok"]
    by_id = {r["post_id"]: r for r in rows}
    assert by_id["p1"]["format"] == "FEED" and by_id["p3"]["format"] == "REELS"
    assert by_id["p1"]["reach"] == 100 and by_id["p1"]["follows"] == 1
    assert by_id["p3"]["ig_reels_avg_watch_time"] == 4200
    assert by_id["p1"]["interactions_per_reach"] == 0.14
    assert by_id["p1"]["posted_hour_ist"] == "19:30" and by_id["p1"]["slot_delay_min"] == 0
    assert by_id["p1"]["hours_since_post"] == 94.0
    assert len(calls) == 9  # 3 posts x (meta + core + extra)

    entries = ci.rollup(rows)
    fam = {(e["format"], e["family"]): e for e in entries}
    assert fam[("FEED", "one-star-files")]["n"] == 2  # prefix stripped -> one family
    assert fam[("FEED", "one-star-files")]["reach"] == 200.0
    assert fam[("REELS", "pov")]["n"] == 1

    out = tmp_path / "out.csv"
    ci.write_csv(out, rows)
    ci.write_csv(out.with_name("hist.csv"), rows, append=True)
    ci.write_csv(out.with_name("hist.csv"), rows, append=True)
    assert len(ci.read_csv(out)) == 3
    assert len(ci.read_csv(out.with_name("hist.csv"))) == 6  # header once, rows twice
    assert ci.format_rollup(ci.rollup(ci.read_csv(out))).count("\n") >= 2


def test_per_post_isolation_missing_error_and_extras(tmp_path, monkeypatch):
    _post(tmp_path, "acct_a", "gone", "111", ptype="test")
    _post(tmp_path, "acct_a", "bad", "222")
    _post(tmp_path, "acct_a", "extras_fail", "333", ptype="reel-x", video=True)
    _post(tmp_path, "acct_a", "fine", "444")
    monkeypatch.setenv("IG_ACCESS_TOKEN_ACCT_A", FAKE_TOKEN)
    missing = ig_common.GraphAPIError(
        "GraphMethodException code=100 subcode=33: Unsupported get request. Object with ID '111' does not exist",
        code=100, subcode=33,
    )
    boom = ig_common.GraphAPIError("OAuthException code=100: (#100) Invalid parameter", code=100)
    script = {
        "111": {"meta": missing, "core": None, "extra": None},
        "222": {"meta": _meta(), "core": boom, "extra": None},
        "333": {"meta": _meta("REELS", "VIDEO"), "core": _insights(reach=5, views=6, likes=1, comments=0, saved=0, shares=0, total_interactions=1), "extra": boom},
        "444": {"meta": _meta(), "core": _insights(reach=50, views=60, likes=5, comments=0, saved=1, shares=0, total_interactions=6), "extra": _insights(follows=0, profile_visits=0)},
    }
    api_get, _ = _fake_api(script)
    monkeypatch.setattr(ig_common, "api_get", api_get)

    rows = ci.collect(tmp_path, ["acct_a"], include_tests=True, sleep_s=0, now=NOW)
    status = {r["post_id"]: r["status"] for r in rows}
    assert status == {"gone": "missing", "bad": "partial", "extras_fail": "ok", "fine": "ok"}
    by_id = {r["post_id"]: r for r in rows}
    assert by_id["bad"]["like_count"] == 3  # metadata kept when /insights fails
    assert by_id["extras_fail"]["reach"] == 5 and "Invalid parameter" in by_id["extras_fail"]["extra_error"]
    # type=test excluded by default
    rows2 = ci.collect(tmp_path, ["acct_a"], sleep_s=0, now=NOW)
    assert {r["post_id"] for r in rows2} == {"bad", "extras_fail", "fine"}


def test_rate_limit_aborts_account_but_not_run_and_redacts(tmp_path, monkeypatch):
    _post(tmp_path, "acct_a", "a1", "111")
    _post(tmp_path, "acct_a", "a2", "222")
    _post(tmp_path, "acct_a", "a3", "333")
    _post(tmp_path, "acct_b", "b1", "444")
    monkeypatch.setenv("IG_ACCESS_TOKEN_ACCT_A", FAKE_TOKEN)
    monkeypatch.setenv("IG_ACCESS_TOKEN_ACCT_B", FAKE_TOKEN + "B")
    throttled = ig_common.GraphAPIError(
        f"OAuthException code=4: Application request limit reached {FAKE_TOKEN}", code=4
    )
    script = {
        "111": {"meta": _meta(), "core": _insights(reach=1, views=1, likes=0, comments=0, saved=0, shares=0, total_interactions=0), "extra": _insights(follows=0, profile_visits=0)},
        "222": {"meta": _meta(), "core": throttled, "extra": None},
        "333": {"meta": _meta(), "core": _insights(reach=9), "extra": None},
        "444": {"meta": _meta(), "core": _insights(reach=7, views=7, likes=0, comments=0, saved=0, shares=0, total_interactions=0), "extra": _insights(follows=0, profile_visits=0)},
    }
    api_get, calls = _fake_api(script)
    monkeypatch.setattr(ig_common, "api_get", api_get)

    rows = ci.collect(tmp_path, ["acct_a", "acct_b"], sleep_s=0, now=NOW)
    status = {r["post_id"]: r["status"] for r in rows}
    assert status == {"a1": "ok", "a2": "rate_limited", "a3": "skipped", "b1": "ok"}
    assert "333" not in "".join(calls)  # never queried after the throttle
    joined = json.dumps(rows)
    assert FAKE_TOKEN not in joined and "<REDACTED>" in joined

    out = tmp_path / "out.csv"
    ci.write_csv(out, rows)
    text = out.read_text(encoding="utf-8")
    assert FAKE_TOKEN not in text
    assert list(csv.DictReader(text.splitlines()))[1]["error"].startswith("OAuthException code=4")


def test_token_invalid_aborts_account_and_no_token_fails(tmp_path, monkeypatch):
    _post(tmp_path, "acct_a", "a1", "111")
    _post(tmp_path, "acct_a", "a2", "222")
    _post(tmp_path, "acct_b", "b1", "333")
    monkeypatch.setenv("IG_ACCESS_TOKEN_ACCT_A", FAKE_TOKEN)
    expired = ig_common.GraphAPIError("OAuthException code=190: Error validating access token", code=190)
    api_get, calls = _fake_api({"111": {"meta": expired, "core": None, "extra": None}})
    monkeypatch.setattr(ig_common, "api_get", api_get)

    rows = ci.collect(tmp_path, ["acct_a", "acct_b"], sleep_s=0, now=NOW)
    status = {r["post_id"]: r["status"] for r in rows}
    assert status == {"a1": "token_invalid", "a2": "skipped", "b1": "no_token"}
    assert calls == ["111"]
    assert all(r["status"] in ci.BAD_STATUSES for r in rows if r["post_id"] != "a2")


def test_single_account_falls_back_to_generic_token_env(tmp_path, monkeypatch):
    _post(tmp_path, "acct_a", "a1", "111")
    monkeypatch.setenv("IG_ACCESS_TOKEN", FAKE_TOKEN)
    api_get, _ = _fake_api({"111": {"meta": _meta(), "core": _insights(reach=2, views=2, likes=0, comments=0, saved=0, shares=0, total_interactions=0), "extra": _insights(follows=0, profile_visits=0)}})
    monkeypatch.setattr(ig_common, "api_get", api_get)
    rows = ci.collect(tmp_path, ["acct_a"], sleep_s=0, now=NOW)
    assert rows[0]["status"] == "ok"
    # ...but never when several accounts are selected (wrong token -> wrong account)
    rows = ci.collect(tmp_path, ["acct_a", "acct_b"], sleep_s=0, now=NOW) if (tmp_path / "acct_b").exists() else []
    assert rows == []


def test_insights_to_dict_accepts_both_shapes():
    data = [
        {"name": "reach", "values": [{"value": 10}]},
        {"name": "views", "total_value": {"value": 12}},
        {"name": "broken"},
        "junk",
    ]
    assert ci.insights_to_dict(data) == {"reach": 10, "views": 12, "broken": None}


def test_family_of():
    assert ci.family_of("reel-the-rule") == "the-rule"
    assert ci.family_of("carousel-masterclass") == "masterclass"
    assert ci.family_of("palette-study") == "palette-study"
    assert ci.family_of("") == ""


def test_format_rollup_handles_empty():
    assert "no rows" in ci.format_rollup([])
    assert ci.rollup([]) == []
