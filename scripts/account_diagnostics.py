"""Account-level, strictly read-only Graph API diagnostic for every account.

Why this exists
---------------
`scripts/collect_insights.py` answers "how did each *post* do". It cannot
answer "is this *account* being distributed at all", because every metric it
reads is per-media and none of them separate follower reach from
non-follower reach.

That distinction is the whole diagnosis for the `hype_tingles` distribution
problem (2-9 reach/post since 2026-08-30 while `anime_ekaya` and `nuvarel`
run 39-1091 on the identical pipeline). Per-media data already shows the
shape: on hype_tingles, Reels reach (mean 4.2) is *lower* than its own
carousel reach (mean 5.0), whereas on the other two accounts Reels out-reach
carousels by 60-110x. Carousels are distributed almost entirely to
followers; Reels get most of their reach from Reels-tab/Explore
recommendation. An account whose Reels perform like its carousels is an
account getting ~zero recommendation distribution.

`GET /me/insights?metric=reach&breakdown=follow_type` measures that directly,
splitting reach into FOLLOWER / NON_FOLLOWER / UNKNOWN
(developers.facebook.com/docs/instagram-platform/api-reference/
instagram-user/insights -- `follow_type` is a documented breakdown for
`reach` at period=day, metric_type=total_value; checked 2026-09-12).

It also reads the profile fields (`biography`, `account_type`,
`followers_count`), because "does the bio self-describe as AI-run, and does
Instagram's 2026-08-31 AI-generated-profile policy therefore apply" is a
live question on this account and nobody had actually read the bio.

Safety
------
GET only. This script has no api_post/api_delete import path and never
writes to Instagram. It does not touch content/queue/. Every error string
goes through ig_common.redact() before printing, because this runs in a
public repo's Actions log.

Env (same contract as collect_insights.py):
  IG_ACCESS_TOKEN_<ACCOUNT>   per-account token
  IG_ACCESS_TOKEN             fallback when exactly one --account is given
  IG_AUTH_MODE                instagram_login (default) | facebook_login

Exit code: 0 if every account produced at least the profile block; 1 if any
account failed entirely (no token, or the profile GET failed).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import ig_common
from ig_common import GraphAPIError, redact

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ACCOUNTS_ROOT = REPO_ROOT / "accounts"

PROFILE_FIELDS = (
    "id,username,name,biography,followers_count,follows_count,"
    "media_count,account_type,website,profile_picture_url"
)

# Breakdowns documented for `reach` at period=day / metric_type=total_value.
REACH_BREAKDOWNS = ("follow_type", "media_product_type")

# Account-level totals worth having next to the breakdown.
TOTAL_METRICS = ("reach", "views", "accounts_engaged", "profile_links_taps")


def discover_accounts(accounts_root: Path) -> list[str]:
    return sorted(
        p.name
        for p in accounts_root.iterdir()
        if p.is_dir() and (p / "content" / "posted").is_dir()
    )


def token_for(account: str, selected: list[str]) -> str | None:
    env_name = f"IG_ACCESS_TOKEN_{account.upper().replace('-', '_')}"
    token = os.environ.get(env_name)
    if not token and len(selected) == 1:
        token = os.environ.get("IG_ACCESS_TOKEN")
    if token:
        ig_common.register_secret(token)
    return token or None


def window(days: int) -> tuple[int, int]:
    """(since, until) unix timestamps for a trailing `days`-day window.

    Meta caps account insights at 30 days back from today and rejects a
    window longer than 30 days.
    """
    now = datetime.now(timezone.utc)
    until = int(now.timestamp())
    since = int((now - timedelta(days=days)).timestamp())
    return since, until


def fetch_profile(token: str) -> dict:
    return ig_common.api_get("me", token, params={"fields": PROFILE_FIELDS})


def fetch_reach_breakdown(token: str, breakdown: str, days: int) -> dict:
    """reach split by `breakdown` over a trailing window.

    Returns {dimension_value: reach}. The total_value payload nests the split
    under total_value.breakdowns[].results[], each result carrying
    dimension_values[] and a value.
    """
    since, until = window(days)
    payload = ig_common.api_get(
        "me/insights",
        token,
        params={
            "metric": "reach",
            "period": "day",
            "metric_type": "total_value",
            "breakdown": breakdown,
            "since": since,
            "until": until,
        },
    )
    out: dict[str, int] = {}
    for item in payload.get("data", []):
        total = item.get("total_value") or {}
        for bd in total.get("breakdowns", []) or []:
            for res in bd.get("results", []) or []:
                dims = res.get("dimension_values") or ["?"]
                out[str(dims[0])] = res.get("value")
    return out


def fetch_totals(token: str, days: int) -> dict:
    since, until = window(days)
    out: dict[str, object] = {}
    for metric in TOTAL_METRICS:
        try:
            payload = ig_common.api_get(
                "me/insights",
                token,
                params={
                    "metric": metric,
                    "period": "day",
                    "metric_type": "total_value",
                    "since": since,
                    "until": until,
                },
            )
            for item in payload.get("data", []):
                out[item.get("name", metric)] = (item.get("total_value") or {}).get("value")
        except GraphAPIError as e:
            out[metric] = f"ERROR: {redact(e)}"
    return out


def diagnose(account: str, token: str | None, days: int) -> dict:
    result: dict = {"account": account}
    if token is None:
        result["error"] = f"IG_ACCESS_TOKEN_{account.upper()} not set"
        return result

    try:
        result["profile"] = fetch_profile(token)
    except GraphAPIError as e:
        result["error"] = f"profile GET failed: {redact(e)}"
        return result

    result["reach_breakdowns"] = {}
    for bd in REACH_BREAKDOWNS:
        try:
            result["reach_breakdowns"][bd] = fetch_reach_breakdown(token, bd, days)
        except GraphAPIError as e:
            result["reach_breakdowns"][bd] = {"_error": redact(e)}

    result["totals"] = fetch_totals(token, days)
    return result


def render(results: list[dict], days: int) -> str:
    lines: list[str] = []
    add = lines.append
    add(f"Account diagnostics -- trailing {days} days, read-only Graph API")
    add("=" * 72)

    for r in results:
        add("")
        add(f"### {r['account']}")
        if "error" in r:
            add(f"  FAILED: {r['error']}")
            continue
        p = r.get("profile", {})
        add(f"  username        @{p.get('username')}")
        add(f"  name            {p.get('name')!r}")
        add(f"  account_type    {p.get('account_type')}")
        add(f"  followers       {p.get('followers_count')}")
        add(f"  follows         {p.get('follows_count')}")
        add(f"  media_count     {p.get('media_count')}")
        add(f"  website         {p.get('website')!r}")
        add("  biography       |" + "\n                  |".join(
            (p.get("biography") or "").splitlines() or [""]
        ))

        for bd, data in (r.get("reach_breakdowns") or {}).items():
            add(f"  reach by {bd}:")
            if "_error" in data:
                add(f"    ERROR: {data['_error']}")
                continue
            if not data:
                add("    (empty)")
                continue
            total = sum(v for v in data.values() if isinstance(v, (int, float))) or 0
            for k in sorted(data, key=lambda k: -(data[k] or 0)):
                v = data[k]
                pct = f"{100 * v / total:5.1f}%" if total and isinstance(v, (int, float)) else "    -"
                add(f"    {k:<22} {str(v):>8}  {pct}")

        add("  account totals:")
        for k, v in (r.get("totals") or {}).items():
            add(f"    {k:<22} {v}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--accounts-root", type=Path, default=DEFAULT_ACCOUNTS_ROOT)
    p.add_argument("--account", action="append", default=None)
    p.add_argument("--days", type=int, default=29, help="trailing window (Meta caps at 30)")
    p.add_argument("--json", action="store_true", help="also dump raw JSON")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args([] if argv is None else argv)
    accounts = args.account or discover_accounts(args.accounts_root)
    if not accounts:
        print(f"FAIL: no accounts under {args.accounts_root}", file=sys.stderr)
        return 1

    results = [diagnose(a, token_for(a, accounts), args.days) for a in accounts]
    print(render(results, args.days))
    if args.json:
        print("\n--- raw ---")
        print(json.dumps(results, indent=2, default=str))
    return 1 if any("error" in r for r in results) else 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as e:  # noqa: BLE001 - never let a traceback leak a token
        print(f"FAIL: unexpected error: {redact(e)}", file=sys.stderr)
        sys.exit(1)
