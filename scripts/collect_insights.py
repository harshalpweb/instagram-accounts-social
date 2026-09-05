"""Collect real Instagram Insights for every published post, across accounts.

Read-only against the Graph API: this script only GETs media metadata and
`/insights` — it never creates, publishes, edits or deletes anything, and it
never touches content/queue/.

Why it exists: every strategic judgment about the accounts so far has been
made on zero measured data (the only signal was the founder's own informal
observation). `ig_common.media_insights()` has existed since day one and
nothing called it. This closes that gap with one CSV.

Walks `accounts/*/content/posted/*/*.json`, and for each post with an
`ig_post_id` makes up to three GET calls:

  1. `GET /{media-id}?fields=...`      media_type, media_product_type
                                       (FEED | REELS), permalink, like/comment
                                       counts (a fallback if /insights fails)
  2. `GET /{media-id}/insights`        core metrics valid for BOTH product
                                       types per Meta's reference table
                                       (developers.facebook.com/docs/instagram-
                                       platform/reference/instagram-media/
                                       insights, checked 2026-09-05):
                                       reach, views, likes, comments, saved,
                                       shares, total_interactions.
                                       `impressions` is deliberately absent —
                                       deprecated for media created after
                                       2024-07-02, i.e. everything here.
  3. `GET /{media-id}/insights`        format-specific extras. REELS:
                                       ig_reels_avg_watch_time,
                                       ig_reels_video_view_total_time,
                                       reels_skip_rate (Meta marks the last
                                       two "in development"). FEED: follows,
                                       profile_visits. A failure here never
                                       sinks the core row — it lands in
                                       `extra_error` and the row stays `ok`.

Outputs (both CSV, both git-tracked so the CI run's commit preserves them):

  analytics/insights.csv          latest snapshot, one row per post
  analytics/insights-history.csv  append-only, one row per post per run, so a
                                  metric's growth over time is queryable once
                                  the daily workflow has run a few times

Then prints a rollup: mean of each metric per (account, format, family),
where `family` is the post's `type` with any leading `reel-`/`carousel-`
stripped, so `carousel-one-star-files` and `one-star-files` group together.
`--rollup-only` re-prints that rollup from the existing CSV with no API call
and no token, for anyone who just wants to read the numbers.

Failure handling is per post, never whole-run:
  missing         media no longer exists (e.g. the deleted day-0 test posts)
  token_invalid   OAuth code 190 — every later call for this account would
                  fail identically, so the rest of the account is skipped
  rate_limited    Meta throttle code (4/17/32/613) — same skip logic, same
                  reasoning as publish_due_posts.RATE_LIMIT_ERROR_CODES
  error           anything else; recorded, next post proceeds
  skipped         not attempted because of an earlier token/rate-limit abort
  no_token        the account's token env var is unset (fails the run, so a
                  missing CI secret can never look like a green collection)

Every error string written to the CSV goes through ig_common.redact() (the
Graph client already redacts, this is the second line of defence — the CSV
is committed to a public repo by the workflow).

Insights caveats that the reader has to carry, not the script: Meta says
metric data can lag up to 48 hours (`hours_since_post` is in every row so a
reader can tell a young post from a dead one), and `reach` is documented as
an estimate. A post's posted_at often differs from its scheduled slot here —
the founder review gate held many pieces past their slot — so both times
and the delay between them are recorded; time-of-day is a live confound in
any format-vs-format comparison over this dataset.

Env:
  IG_ACCESS_TOKEN_<ACCOUNT>   per-account token (ACCOUNT upper-cased, e.g.
                              IG_ACCESS_TOKEN_HYPE_TINGLES) — matches the
                              GitHub secret names in README.md
  IG_ACCESS_TOKEN             fallback when exactly one --account is given
                              (same contract as the other scripts)
  IG_AUTH_MODE                instagram_login (default) | facebook_login

Exit code: 0 if every attempted post ended ok/partial/missing; 1 if any
post hit token_invalid/rate_limited/error/no_token (the CSVs are still
written first).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import ig_common
from ig_common import GraphAPIError, redact

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ACCOUNTS_ROOT = REPO_ROOT / "accounts"
DEFAULT_OUT = REPO_ROOT / "analytics" / "insights.csv"
DEFAULT_HISTORY = REPO_ROOT / "analytics" / "insights-history.csv"

IST = timezone(timedelta(hours=5, minutes=30))

# Same set, same reasoning as publish_due_posts.RATE_LIMIT_ERROR_CODES — kept
# as a literal here so this read-only script does not import the publisher.
RATE_LIMIT_ERROR_CODES = {4, 17, 32, 613}
TOKEN_ERROR_CODES = {190}
# Row statuses that make the run exit 1 (CSV is still written first).
BAD_STATUSES = ("error", "rate_limited", "token_invalid", "no_token")

MEDIA_FIELDS = (
    "id,media_type,media_product_type,timestamp,permalink,like_count,comments_count"
)
CORE_METRICS = (
    "reach",
    "views",
    "likes",
    "comments",
    "saved",
    "shares",
    "total_interactions",
)
EXTRA_METRICS = {
    "REELS": ("ig_reels_avg_watch_time", "ig_reels_video_view_total_time", "reels_skip_rate"),
    "FEED": ("follows", "profile_visits"),
}
ALL_EXTRA = tuple(m for ms in EXTRA_METRICS.values() for m in ms)

COLUMNS = [
    "collected_at_utc",
    "account",
    "post_id",
    "type",
    "family",
    "format",
    "media_type",
    "ig_post_id",
    "permalink",
    "scheduled_time_ist",
    "posted_at_utc",
    "posted_at_ist",
    "posted_hour_ist",
    "slot_delay_min",
    "hours_since_post",
    "status",
    *CORE_METRICS,
    "interactions_per_reach",
    "like_count",
    "comments_count",
    *ALL_EXTRA,
    "error",
    "extra_error",
]


# ---------------------------------------------------------------------------
# Local record discovery
# ---------------------------------------------------------------------------


def family_of(post_type: str) -> str:
    """`reel-the-rule` -> `the-rule`, `carousel-masterclass` -> `masterclass`."""
    t = (post_type or "").strip().lower()
    for prefix in ("reel-", "carousel-"):
        if t.startswith(prefix):
            return t[len(prefix):]
    return t


def discover_accounts(accounts_root: Path) -> list[str]:
    return sorted(
        p.name
        for p in accounts_root.iterdir()
        if p.is_dir() and (p / "content" / "posted").is_dir()
    )


def load_posted(accounts_root: Path, account: str) -> list[dict]:
    """Every posted/*/*.json for one account, oldest posted_at first."""
    posted_dir = accounts_root / account / "content" / "posted"
    records = []
    for path in sorted(posted_dir.glob("*/*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print(f"WARN: {account}: unreadable {path.name}: {redact(e)}", file=sys.stderr)
            continue
        if not isinstance(data, dict):
            continue
        data["_path"] = path
        records.append(data)
    records.sort(key=lambda d: str(d.get("posted_at") or ""))
    return records


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def time_columns(post: dict, now: datetime) -> dict:
    posted = _parse_dt(post.get("posted_at"))
    scheduled = _parse_dt(post.get("scheduled_time_ist"))
    out = {
        "scheduled_time_ist": post.get("scheduled_time_ist", ""),
        "posted_at_utc": "",
        "posted_at_ist": "",
        "posted_hour_ist": "",
        "slot_delay_min": "",
        "hours_since_post": "",
    }
    if posted:
        posted_ist = posted.astimezone(IST)
        out["posted_at_utc"] = posted.astimezone(timezone.utc).isoformat(timespec="seconds")
        out["posted_at_ist"] = posted_ist.isoformat(timespec="seconds")
        out["posted_hour_ist"] = f"{posted_ist.hour:02d}:{posted_ist.minute:02d}"
        out["hours_since_post"] = round((now - posted).total_seconds() / 3600, 1)
        if scheduled:
            out["slot_delay_min"] = int(round((posted - scheduled).total_seconds() / 60))
    return out


# ---------------------------------------------------------------------------
# Graph calls
# ---------------------------------------------------------------------------


def classify_error(e: GraphAPIError) -> str:
    """Map a Graph failure to a row status. Order matters: throttle and token
    errors decide whether the rest of the account is even worth trying."""
    try:
        code = int(e.code) if e.code is not None else None
    except (TypeError, ValueError):
        code = None
    if code in RATE_LIMIT_ERROR_CODES:
        return "rate_limited"
    if code in TOKEN_ERROR_CODES:
        return "token_invalid"
    text = str(e).lower()
    if code == 100 and ("does not exist" in text or "unsupported get request" in text):
        return "missing"
    return "error"


def insights_to_dict(data: list) -> dict:
    """[{name, values:[{value}]} | {name, total_value:{value}}] -> {name: value}."""
    out = {}
    for item in data or []:
        if not isinstance(item, dict) or "name" not in item:
            continue
        value = None
        values = item.get("values")
        if isinstance(values, list) and values and isinstance(values[0], dict):
            value = values[0].get("value")
        elif isinstance(item.get("total_value"), dict):
            value = item["total_value"].get("value")
        out[item["name"]] = value
    return out


def fetch_post(media_id: str, token: str, *, sleep_s: float = 0.0) -> dict:
    """Up to three GETs for one post. Returns partial row columns + status.

    Raises nothing: every failure is folded into the returned dict so the
    caller decides what to do with the rest of the account.
    """
    row: dict = {"status": "ok", "error": "", "extra_error": ""}

    # 1. media object — product type decides the metric set
    try:
        meta = ig_common.api_get(media_id, token, params={"fields": MEDIA_FIELDS})
    except GraphAPIError as e:
        row["status"] = classify_error(e)
        row["error"] = redact(e)
        return row
    product = str(meta.get("media_product_type") or "").upper()
    row["format"] = product or "?"
    row["media_type"] = meta.get("media_type", "")
    row["permalink"] = meta.get("permalink", "")
    row["like_count"] = meta.get("like_count", "")
    row["comments_count"] = meta.get("comments_count", "")
    if sleep_s:
        time.sleep(sleep_s)

    # 2. core insights
    try:
        core = insights_to_dict(ig_common.media_insights(media_id, token, metrics=CORE_METRICS))
    except GraphAPIError as e:
        status = classify_error(e)
        # A throttle/token failure mid-post must still abort the account; an
        # ordinary insights failure keeps the metadata we already have.
        row["status"] = status if status in ("rate_limited", "token_invalid") else "partial"
        row["error"] = redact(e)
        return row
    for m in CORE_METRICS:
        row[m] = core.get(m, "")
    reach, ti = row.get("reach"), row.get("total_interactions")
    if isinstance(reach, (int, float)) and reach and isinstance(ti, (int, float)):
        row["interactions_per_reach"] = round(ti / reach, 4)
    if sleep_s:
        time.sleep(sleep_s)

    # 3. format extras — optional, never fatal for the row
    extras = EXTRA_METRICS.get(product)
    if extras:
        try:
            extra = insights_to_dict(ig_common.media_insights(media_id, token, metrics=extras))
            for m in extras:
                row[m] = extra.get(m, "")
        except GraphAPIError as e:
            status = classify_error(e)
            if status in ("rate_limited", "token_invalid"):
                row["status"] = status
                row["error"] = redact(e)
                return row
            row["extra_error"] = redact(e)
    return row


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def token_for(account: str, selected: list[str]) -> str | None:
    env_name = f"IG_ACCESS_TOKEN_{account.upper().replace('-', '_')}"
    token = os.environ.get(env_name)
    if not token and len(selected) == 1:
        token = os.environ.get("IG_ACCESS_TOKEN")
    if token:
        ig_common.register_secret(token)
    return token or None


def collect(
    accounts_root: Path,
    accounts: list[str],
    *,
    include_tests: bool = False,
    sleep_s: float = 0.3,
    now: datetime | None = None,
) -> list[dict]:
    now = now or datetime.now(timezone.utc)
    stamp = now.replace(microsecond=0).isoformat().replace("+00:00", "Z")
    rows: list[dict] = []

    for account in accounts:
        token = token_for(account, accounts)
        posts = load_posted(accounts_root, account)
        if not include_tests:
            posts = [p for p in posts if str(p.get("type", "")).lower() != "test"]
        if token is None:
            print(
                f"WARN: {account}: no token in env "
                f"(IG_ACCESS_TOKEN_{account.upper()}) - {len(posts)} post(s) not collected",
                file=sys.stderr,
            )
        abort_reason: str | None = None
        n_ok = 0
        for post in posts:
            base = {
                "collected_at_utc": stamp,
                "account": account,
                "post_id": post.get("id", post["_path"].stem),
                "type": post.get("type", ""),
                "family": family_of(post.get("type", "")),
                "format": "REELS" if post.get("video") else "FEED",
                "media_type": "",
                "ig_post_id": post.get("ig_post_id", ""),
                "permalink": "",
                **time_columns(post, now),
                "status": "skipped",
                "error": "",
                "extra_error": "",
            }
            if token is None:
                base["status"] = "no_token"
                base["error"] = f"IG_ACCESS_TOKEN_{account.upper()} not set"
            elif abort_reason:
                base["error"] = f"skipped after {abort_reason} earlier in this account"
            elif not base["ig_post_id"]:
                base["status"] = "error"
                base["error"] = "no ig_post_id in record"
            else:
                base.update(fetch_post(str(base["ig_post_id"]), token, sleep_s=sleep_s))
                if base["status"] in ("rate_limited", "token_invalid"):
                    abort_reason = base["status"]
                    print(
                        f"ABORT {account}: {base['status']} on {base['post_id']}: "
                        f"{base['error']} - skipping the rest of this account",
                        file=sys.stderr,
                    )
                elif base["status"] in ("ok", "partial"):
                    n_ok += 1
            rows.append({c: base.get(c, "") for c in COLUMNS})
        print(f"{account}: {n_ok}/{len(posts)} post(s) with insights")
    return rows


def write_csv(path: Path, rows: list[dict], *, append: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists() and path.stat().st_size > 0
    mode = "a" if append else "w"
    with path.open(mode, newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        if not (append and exists):
            writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------------------
# Rollup
# ---------------------------------------------------------------------------

ROLLUP_METRICS = ("reach", "views", "likes", "comments", "saved", "shares", "total_interactions")


def _num(value) -> float | None:
    if value in ("", None):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def rollup(rows: list[dict], *, mature_hours: float = 48.0) -> list[dict]:
    """Mean of each metric per (account, format, family) over rows with data.

    `n_young` counts posts younger than `mature_hours` — Meta says insight
    data can lag up to 48 h, so those rows are provisional, not final.
    """
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        if row.get("status") not in ("ok", "partial"):
            continue
        if _num(row.get("reach")) is None:
            continue
        groups[(row["account"], row["format"], row["family"])].append(row)
    out = []
    for key in sorted(groups):
        members = groups[key]
        entry = {"account": key[0], "format": key[1], "family": key[2], "n": len(members)}
        entry["n_young"] = sum(
            1 for r in members if (_num(r.get("hours_since_post")) or 0) < mature_hours
        )
        for m in ROLLUP_METRICS:
            vals = [v for v in (_num(r.get(m)) for r in members) if v is not None]
            entry[m] = round(sum(vals) / len(vals), 1) if vals else None
        ipr = [v for v in (_num(r.get("interactions_per_reach")) for r in members) if v is not None]
        entry["interactions_per_reach"] = round(sum(ipr) / len(ipr), 4) if ipr else None
        out.append(entry)
    return out


def format_rollup(entries: list[dict]) -> str:
    if not entries:
        return "  (no rows with insights)"
    cols = ["account", "format", "family", "n", "n_young", *ROLLUP_METRICS, "interactions_per_reach"]
    widths = {c: max([len(c)] + [len(str(e.get(c, ""))) for e in entries]) for c in cols}
    lines = ["  ".join(c.ljust(widths[c]) for c in cols)]
    lines.append("  ".join("-" * widths[c] for c in cols))
    for e in entries:
        lines.append(
            "  ".join(str("" if e.get(c) is None else e.get(c)).ljust(widths[c]) for c in cols)
        )
    return "\n".join(lines)


def format_status_summary(rows: list[dict]) -> str:
    counts: dict[tuple, int] = defaultdict(int)
    for r in rows:
        counts[(r["account"], r["status"])] += 1
    return "\n".join(
        f"  {acct:<14} {status:<14} {n}" for (acct, status), n in sorted(counts.items())
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--accounts-root", type=Path, default=DEFAULT_ACCOUNTS_ROOT)
    p.add_argument(
        "--account",
        action="append",
        default=None,
        help="account name (repeatable); default: every account with content/posted/",
    )
    p.add_argument("--out", type=Path, default=DEFAULT_OUT, help="latest-snapshot CSV")
    p.add_argument(
        "--history",
        type=Path,
        default=DEFAULT_HISTORY,
        help="append-only CSV; pass an empty string to disable",
    )
    p.add_argument("--include-tests", action="store_true", help="also query type=test posts")
    p.add_argument("--sleep", type=float, default=0.3, help="seconds between Graph calls")
    p.add_argument(
        "--rollup-only",
        action="store_true",
        help="no API calls: print the rollup from --out as it stands",
    )
    p.add_argument("--mature-hours", type=float, default=48.0)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args([] if argv is None else argv)

    if args.rollup_only:
        if not args.out.exists():
            print(f"FAIL: {args.out} does not exist yet", file=sys.stderr)
            return 1
        rows = read_csv(args.out)
        print(format_rollup(rollup(rows, mature_hours=args.mature_hours)))
        return 0

    accounts = args.account or discover_accounts(args.accounts_root)
    if not accounts:
        print(f"FAIL: no accounts under {args.accounts_root}", file=sys.stderr)
        return 1

    rows = collect(
        args.accounts_root,
        accounts,
        include_tests=args.include_tests,
        sleep_s=args.sleep,
    )
    write_csv(args.out, rows)
    if str(args.history):
        write_csv(Path(args.history), rows, append=True)

    print(f"\nWrote {len(rows)} row(s) to {args.out}")
    print("Status by account:")
    print(format_status_summary(rows))
    print(f"\nRollup (mean per account / format / family; n_young = posted <{args.mature_hours:g}h ago):")
    print(format_rollup(rollup(rows, mature_hours=args.mature_hours)))

    bad = [r for r in rows if r["status"] in BAD_STATUSES]
    return 1 if bad else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:  # noqa: BLE001 - never let a traceback leak a token
        print(f"FAIL: unexpected error: {redact(e)}", file=sys.stderr)
        sys.exit(1)
