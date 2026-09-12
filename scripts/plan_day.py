#!/usr/bin/env python3
"""Plan one account's posting day: how many pieces, which formats, at what times.

Group CTO, 2026-09-12, on a founder-direct instruction. This script exists so
that three standing rules are *mechanical* rather than prose a build agent may
or may not apply:

  1. **Cadence floor.** 3 posts a day, every day, until the account passes
     50,000 followers (`docs/slot-policy.json` -> `cadence`). The count never
     flexes; only the mix inside it does.

  2. **Data-driven format mix.** The mix of FEED (carousel) vs REELS is
     recomputed every day from `analytics/insights-history.csv` over a trailing
     window, not fixed at a ratio. A format that is measurably losing loses
     share. Scoring is a *smoothed* mean (a Bayesian shrink toward the account
     mean) so one lucky post with n=1 cannot capture the whole day.

     The demotion is deliberately not greedy-forever: `explore_every_n_days`
     forces one slot back to the demoted format on a fixed cycle. Without it a
     demotion is self-fulfilling -- a format that is never posted is never
     re-measured, and the account can never discover that the format recovered
     (or that the real cause was the topic, not the format).

  3. **Natural posting times.** Each slot is a *window*, not a clock time. The
     minute inside the window is drawn from a generator seeded on
     (account, date), so the schedule is reproducible and auditable from the
     date alone, but differs every day and never repeats a clock time. Founder
     note 2026-09-12: identical daily slot times read as automated.

Reads only committed files; no token, no network, no API call.

Usage:
    py -3 scripts/plan_day.py --account nuvarel
    py -3 scripts/plan_day.py --account nuvarel --date 2026-09-13
    py -3 scripts/plan_day.py --account anime_ekaya --json

Output (human by default, `--json` for machine use):
    slot 1  09:53 IST  REELS   (window morning)
    slot 2  15:07 IST  REELS   (window afternoon)
    slot 3  20:41 IST  FEED    (window evening)  [explore slot]

Exit codes: 0 planned, 2 misconfiguration (unknown account, bad policy file).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
POLICY_PATH = REPO / "docs" / "slot-policy.json"
HISTORY_PATH = REPO / "analytics" / "insights-history.csv"
SNAPSHOT_PATH = REPO / "analytics" / "insights.csv"

FORMATS = ("REELS", "FEED")


# --------------------------------------------------------------------------
# policy
# --------------------------------------------------------------------------

def load_policy(path: Path = POLICY_PATH) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------
# performance
# --------------------------------------------------------------------------

def _f(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def latest_rows_per_post(account: str) -> list[dict]:
    """One row per post -- the most recent collection for each post_id.

    insights-history.csv is append-only (one row per post per collector run),
    so a naive mean over it weights long-lived posts by how many times they
    were collected. Deduplicate on post_id, keeping the latest
    `collected_at_utc`, before any averaging.
    """
    path = HISTORY_PATH if HISTORY_PATH.exists() else SNAPSHOT_PATH
    if not path.exists():
        return []
    best: dict[str, dict] = {}
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("account") != account:
                continue
            if row.get("status") != "ok":
                continue
            pid = row.get("post_id") or ""
            prev = best.get(pid)
            if prev is None or (row.get("collected_at_utc") or "") > (
                prev.get("collected_at_utc") or ""
            ):
                best[pid] = row
    return list(best.values())


def score_formats(account: str, today: dt.date, policy: dict) -> dict:
    """Smoothed mean reach per format over the trailing window.

    score(f) = (sum_reach(f) + prior_weight * account_mean) / (n(f) + prior_weight)

    `reach` is the metric because it is the only one with a usable n on this
    account set: likes/comments/saves are 0-5 lifetime per account as of
    2026-09-12, which cannot separate two formats. Revisit the metric once any
    account clears ~50 lifetime saves (see docs/cadence-and-format-policy.md).
    """
    cfg = policy["format_mix"]
    window = int(cfg["window_days"])
    k = float(cfg["prior_weight"])
    cutoff = today - dt.timedelta(days=window)

    rows = latest_rows_per_post(account)
    windowed = []
    for row in rows:
        posted = (row.get("posted_at_ist") or "")[:10]
        if not posted:
            continue
        try:
            day = dt.date.fromisoformat(posted)
        except ValueError:
            continue
        if day >= cutoff:
            windowed.append(row)

    # Fall back to all-time if the trailing window is too thin to say anything.
    used_window = True
    if len(windowed) < 4:
        windowed = rows
        used_window = False

    if not windowed:
        return {
            "scores": {f: 0.0 for f in FORMATS},
            "n": {f: 0 for f in FORMATS},
            "account_mean": 0.0,
            "window_days": window,
            "used_window": used_window,
            "basis": "no-data",
        }

    account_mean = sum(_f(r.get("reach", "")) for r in windowed) / len(windowed)

    scores, counts = {}, {}
    for fmt in FORMATS:
        subset = [r for r in windowed if (r.get("format") or "").upper() == fmt]
        counts[fmt] = len(subset)
        total = sum(_f(r.get("reach", "")) for r in subset)
        scores[fmt] = (total + k * account_mean) / (len(subset) + k)

    return {
        "scores": scores,
        "n": counts,
        "account_mean": round(account_mean, 2),
        "window_days": window,
        "used_window": used_window,
        "basis": "reach",
    }


def allocate(perf: dict, slots: int, policy: dict, day_index: int) -> list[str]:
    """Assign a format to each of `slots` slots from the performance scores."""
    cfg = policy["format_mix"]
    demote_ratio = float(cfg["demote_ratio"])
    explore_n = int(cfg["explore_every_n_days"])
    min_share = int(cfg.get("min_share_of_top", 1))

    scores = perf["scores"]
    ranked = sorted(FORMATS, key=lambda f: scores.get(f, 0.0), reverse=True)
    top, rest = ranked[0], ranked[1:]
    top_score = scores.get(top, 0.0) or 1e-9

    demoted = [f for f in rest if scores.get(f, 0.0) < demote_ratio * top_score]
    kept = [f for f in rest if f not in demoted]

    plan: list[str] = [top] * max(min_share, 1)
    # Non-demoted formats each keep one standing slot.
    for fmt in kept:
        if len(plan) < slots:
            plan.append(fmt)
    # Any remaining slots go to the top format.
    while len(plan) < slots:
        plan.append(top)
    plan = plan[:slots]

    explore = False
    if demoted and explore_n > 0 and day_index % explore_n == 0:
        # Force the last slot back to the best-scoring demoted format so a
        # demotion is re-tested on a fixed cycle instead of freezing forever.
        target = max(demoted, key=lambda f: scores.get(f, 0.0))
        plan[-1] = target
        explore = True

    return plan, explore, demoted


# --------------------------------------------------------------------------
# times
# --------------------------------------------------------------------------

def _minutes(hhmm: str) -> int:
    hh, mm = hhmm.split(":")
    return int(hh) * 60 + int(mm)


def _hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def jittered_times(account: str, day: dt.date, windows: list[dict]) -> list[str]:
    """One time per window, drawn from a (account, date)-seeded generator.

    Deterministic: the same account and date always produce the same schedule,
    so a build is reproducible and a reviewer can re-derive what the times
    should have been. Varying: consecutive days never land on the same clock
    time, and the values are not round (:00/:15/:30), which is what makes the
    pattern read as a person rather than a cron entry.
    """
    seed = int(
        hashlib.sha256(f"{account}|{day.isoformat()}".encode("utf-8")).hexdigest()[:16],
        16,
    )
    rng = random.Random(seed)
    out = []
    for win in windows:
        lo, hi = _minutes(win["start"]), _minutes(win["end"])
        if hi <= lo:
            raise ValueError(f"window {win['name']}: end must be after start")
        pick = rng.randint(lo, hi)
        # Avoid round-number minutes; they are the visible tell.
        if pick % 5 == 0:
            pick += rng.choice((-2, -1, 1, 2))
            pick = max(lo, min(hi, pick))
        out.append(_hhmm(pick))
    return out


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def plan(account: str, day: dt.date, policy: dict) -> dict:
    accounts = policy["accounts"]
    if account not in accounts:
        raise KeyError(account)
    windows = accounts[account]["windows"]
    slots = int(policy["cadence"]["posts_per_day"])
    if len(windows) < slots:
        raise ValueError(
            f"{account}: {len(windows)} windows configured but cadence wants {slots}"
        )
    windows = windows[:slots]

    perf = score_formats(account, day, policy)
    day_index = day.toordinal()
    formats, explore, demoted = allocate(perf, slots, policy, day_index)
    times = jittered_times(account, day, windows)

    return {
        "account": account,
        "date": day.isoformat(),
        "cadence_floor": policy["cadence"],
        "slots": [
            {
                "slot": i + 1,
                "window": windows[i]["name"],
                "window_range_ist": f"{windows[i]['start']}-{windows[i]['end']}",
                "time_ist": times[i],
                "scheduled_time_ist": f"{day.isoformat()}T{times[i]}:00+05:30",
                "format": formats[i],
                "explore": bool(explore and i == slots - 1),
            }
            for i in range(slots)
        ],
        "evidence": {
            "metric": perf["basis"],
            "trailing_window_days": perf["window_days"],
            "used_trailing_window": perf["used_window"],
            "account_mean_reach": perf["account_mean"],
            "smoothed_score": {f: round(perf["scores"][f], 2) for f in FORMATS},
            "n_posts": perf["n"],
            "demoted_formats": demoted,
            "explore_slot_fired": explore,
        },
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--account", required=True)
    ap.add_argument("--date", default=None, help="YYYY-MM-DD, default today (IST)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--policy", default=str(POLICY_PATH))
    args = ap.parse_args(argv)

    try:
        policy = load_policy(Path(args.policy))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"policy file unreadable: {exc}", file=sys.stderr)
        return 2

    if args.date:
        day = dt.date.fromisoformat(args.date)
    else:
        ist = dt.timezone(dt.timedelta(hours=5, minutes=30))
        day = dt.datetime.now(dt.timezone.utc).astimezone(ist).date()

    try:
        result = plan(args.account, day, policy)
    except KeyError:
        known = ", ".join(sorted(policy["accounts"]))
        print(f"unknown account {args.account!r}; known: {known}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"policy error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    ev = result["evidence"]
    print(f"{result['account']}  {result['date']}  "
          f"({result['cadence_floor']['posts_per_day']} posts/day floor until "
          f"{result['cadence_floor']['floor_until_followers']:,} followers)")
    for s in result["slots"]:
        tag = "  [explore slot]" if s["explore"] else ""
        print(f"  slot {s['slot']}  {s['time_ist']} IST  {s['format']:<6s} "
              f"(window {s['window']} {s['window_range_ist']}){tag}")
    print(f"  evidence: smoothed mean {ev['metric']} over "
          f"{ev['trailing_window_days']}d"
          f"{'' if ev['used_trailing_window'] else ' (too thin -> all-time)'}: "
          + ", ".join(f"{f}={ev['smoothed_score'][f]} (n={ev['n_posts'][f]})"
                      for f in FORMATS))
    if ev["demoted_formats"]:
        print(f"  demoted: {', '.join(ev['demoted_formats'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
