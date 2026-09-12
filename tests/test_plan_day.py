"""Tests for the daily plan (cadence floor, data-driven format mix, time jitter).

What is protected here is the set of properties the founder's 2026-09-12
instruction actually asked for. Each one is a property a prose rule in a build
prompt cannot enforce:

  1. The cadence floor is a floor: exactly `posts_per_day` slots come back,
     whatever the data says. A losing format loses SHARE, never the count.
  2. The mix follows the data: the better-performing format takes the majority
     of slots, and a format far below the leader is demoted.
  3. The demotion cannot freeze: an explore slot returns the demoted format on
     a fixed cycle, so a format that is never posted is never permanently
     un-measurable.
  4. Scoring is smoothed: one outlier post with n=1 cannot capture the day.
  5. Times vary day to day, stay inside their window, and are reproducible
     from (account, date) alone.
  6. History deduplication: insights-history.csv is append-only, so a post
     collected 30 times must still count once.
"""
import csv
import datetime as dt
import json

import plan_day


POLICY = {
    "cadence": {"posts_per_day": 3, "floor_until_followers": 50000},
    "format_mix": {
        "window_days": 21,
        "prior_weight": 3,
        "demote_ratio": 0.25,
        "explore_every_n_days": 7,
        "min_share_of_top": 1,
    },
    "accounts": {
        "acct": {
            "windows": [
                {"name": "morning", "start": "09:40", "end": "11:20"},
                {"name": "afternoon", "start": "14:10", "end": "16:00"},
                {"name": "evening", "start": "19:05", "end": "21:15"},
            ]
        }
    },
}

HEADER = [
    "collected_at_utc", "account", "post_id", "type", "family", "format",
    "media_type", "posted_at_ist", "status", "reach",
]


def _write_history(tmp_path, rows, monkeypatch):
    path = tmp_path / "insights-history.csv"
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in HEADER})
    monkeypatch.setattr(plan_day, "HISTORY_PATH", path)
    monkeypatch.setattr(plan_day, "SNAPSHOT_PATH", path)
    return path


def _row(pid, fmt, reach, day, collected="2026-09-12T00:00:00Z"):
    return {
        "collected_at_utc": collected, "account": "acct", "post_id": pid,
        "format": fmt, "media_type": "VIDEO" if fmt == "REELS" else "CAROUSEL_ALBUM",
        "posted_at_ist": f"{day}T10:00:00+05:30", "status": "ok", "reach": str(reach),
    }


def _lopsided(day="2026-09-05"):
    """REELS strongly outperforming FEED -- the live 2026-09-12 shape."""
    rows = [_row(f"r{i}", "REELS", 180, day) for i in range(9)]
    rows += [_row(f"c{i}", "FEED", 3, day) for i in range(12)]
    return rows


# 1. cadence floor ---------------------------------------------------------

def test_cadence_floor_is_exact_regardless_of_data(tmp_path, monkeypatch):
    _write_history(tmp_path, _lopsided(), monkeypatch)
    out = plan_day.plan("acct", dt.date(2026, 9, 13), POLICY)
    assert len(out["slots"]) == 3
    assert out["cadence_floor"]["posts_per_day"] == 3


def test_cadence_floor_holds_with_no_data_at_all(tmp_path, monkeypatch):
    _write_history(tmp_path, [], monkeypatch)
    out = plan_day.plan("acct", dt.date(2026, 9, 13), POLICY)
    assert len(out["slots"]) == 3
    assert all(s["format"] in plan_day.FORMATS for s in out["slots"])


# 2. data-driven mix -------------------------------------------------------

def test_winning_format_takes_the_majority_and_loser_is_demoted(tmp_path, monkeypatch):
    _write_history(tmp_path, _lopsided(), monkeypatch)
    # a non-explore day
    day = dt.date(2026, 9, 14)
    assert day.toordinal() % 7 != 0
    out = plan_day.plan("acct", day, POLICY)
    assert [s["format"] for s in out["slots"]] == ["REELS"] * 3
    assert out["evidence"]["demoted_formats"] == ["FEED"]


def test_no_demotion_when_formats_are_comparable(tmp_path, monkeypatch):
    rows = [_row(f"r{i}", "REELS", 50, "2026-09-05") for i in range(6)]
    rows += [_row(f"c{i}", "FEED", 45, "2026-09-05") for i in range(6)]
    _write_history(tmp_path, rows, monkeypatch)
    out = plan_day.plan("acct", dt.date(2026, 9, 14), POLICY)
    assert out["evidence"]["demoted_formats"] == []
    assert set(s["format"] for s in out["slots"]) == {"REELS", "FEED"}


# 3. the demotion cannot freeze -------------------------------------------

def test_explore_slot_returns_the_demoted_format_on_cycle(tmp_path, monkeypatch):
    _write_history(tmp_path, _lopsided(), monkeypatch)
    seen, explore_days = set(), 0
    start = dt.date(2026, 9, 13)
    for i in range(28):
        out = plan_day.plan("acct", start + dt.timedelta(days=i), POLICY)
        fmts = [s["format"] for s in out["slots"]]
        seen.update(fmts)
        if out["evidence"]["explore_slot_fired"]:
            explore_days += 1
            assert "FEED" in fmts, "explore day must actually post the demoted format"
    assert seen == {"REELS", "FEED"}, "a demoted format must never vanish forever"
    assert explore_days == 4, f"expected 1-in-7 over 28 days, got {explore_days}"


# 4. smoothing -------------------------------------------------------------

def test_single_outlier_post_cannot_capture_the_day(tmp_path, monkeypatch):
    # One FEED post with a freak 5000 reach against 9 solid REELS posts.
    rows = [_row(f"r{i}", "REELS", 200, "2026-09-05") for i in range(9)]
    rows += [_row("c0", "FEED", 5000, "2026-09-05")]
    _write_history(tmp_path, rows, monkeypatch)
    out = plan_day.plan("acct", dt.date(2026, 9, 14), POLICY)
    ev = out["evidence"]
    # Raw mean would be 5000 vs 200. Smoothing pulls the n=1 format toward the
    # account mean, so it does not read as 25x better than the n=9 format.
    assert ev["smoothed_score"]["FEED"] < 5000 / 2
    assert ev["n_posts"] == {"REELS": 9, "FEED": 1}


# 5. jitter ----------------------------------------------------------------

def test_times_stay_inside_their_window():
    windows = POLICY["accounts"]["acct"]["windows"]
    for i in range(60):
        day = dt.date(2026, 9, 13) + dt.timedelta(days=i)
        for t, win in zip(plan_day.jittered_times("acct", day, windows), windows):
            assert win["start"] <= t <= win["end"], (t, win)


def test_times_vary_day_to_day_and_are_not_round():
    windows = POLICY["accounts"]["acct"]["windows"]
    firsts = [
        plan_day.jittered_times("acct", dt.date(2026, 9, 13) + dt.timedelta(days=i), windows)[0]
        for i in range(30)
    ]
    assert len(set(firsts)) >= 20, "slot times must not repeat day after day"
    assert not any(t.endswith((":00", ":15", ":30", ":45")) for t in firsts)


def test_times_are_reproducible_from_account_and_date():
    windows = POLICY["accounts"]["acct"]["windows"]
    day = dt.date(2026, 9, 13)
    assert plan_day.jittered_times("acct", day, windows) == \
        plan_day.jittered_times("acct", day, windows)
    assert plan_day.jittered_times("acct", day, windows) != \
        plan_day.jittered_times("other", day, windows)


# 6. history dedup ---------------------------------------------------------

def test_append_only_history_counts_each_post_once(tmp_path, monkeypatch):
    rows = []
    for run in range(30):  # same post collected 30 times
        rows.append(_row("c0", "FEED", 3, "2026-09-05",
                         collected=f"2026-09-{12 - run % 10:02d}T00:00:00Z"))
    rows += [_row(f"r{i}", "REELS", 100, "2026-09-05") for i in range(3)]
    _write_history(tmp_path, rows, monkeypatch)
    out = plan_day.plan("acct", dt.date(2026, 9, 14), POLICY)
    assert out["evidence"]["n_posts"] == {"REELS": 3, "FEED": 1}


# 7. the shipped policy file is valid -------------------------------------

def test_shipped_policy_file_plans_every_live_account():
    policy = plan_day.load_policy()
    assert policy["cadence"]["posts_per_day"] == 3
    assert policy["cadence"]["floor_until_followers"] == 50000
    for account in ("nuvarel", "anime_ekaya", "hype_tingles"):
        out = plan_day.plan(account, dt.date(2026, 9, 13), policy)
        assert len(out["slots"]) == 3
        assert all(s["scheduled_time_ist"].endswith("+05:30") for s in out["slots"])
        json.dumps(out)  # must be serialisable for --json
