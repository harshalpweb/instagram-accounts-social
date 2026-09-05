# instagram-accounts-social

Automated Instagram publishing for the founder's revived personal/business
accounts (separate from `trend-signals-social`, which is TrendGiri only).
One shared repo, one subfolder per account, one workflow pair per account.

Publishing plumbing (`scripts/`) is copied from `trend-signals-social` (the
working TrendGiri pipeline) — same Graph API client, same queue format, same
token-refresh mechanics — parameterized to run against any account's own
`content/` tree via `ACCOUNT_DIR`. Meta auth uses the shared **TrendRadar
Publisher** Meta Developer App (App ID `2230374924469484`); each account is
added as its **own independent Instagram Tester** with its own access token
— tokens are never shared across accounts, only the app registration is.

## Structure

```
scripts/                        shared, account-agnostic (ACCOUNT_DIR-parameterized)
accounts/
  hype_tingles/
    content/queue/               posts waiting to publish (one JSON + slides per post)
    content/posted/              published posts move here
    content/failed/              posts that failed 3 attempts move here
analytics/
  insights.csv                   latest Insights snapshot, one row per published post
  insights-history.csv           append-only: one row per post per collection run
.github/workflows/
  publish-hype_tingles.yml       hourly: publishes hype_tingles's due posts
  refresh-hype_tingles.yml       monthly: refreshes hype_tingles's token
  collect-insights.yml           daily: pulls real Insights for every posted piece, all accounts
```

## How it works (per account)

1. **Publishing** (hourly): reads `accounts/<name>/content/queue/*.json`,
   publishes anything due via the Instagram Graph API, moves it to
   `posted/` or `failed/`.
2. **Token refresh** (monthly): renews that account's long-lived token
   before its ~60-day expiry, writes it back to that account's own GitHub
   secret.
3. **Insights collection** (daily, all accounts in one run, read-only):
   `scripts/collect_insights.py` walks every `content/posted/*/*.json`,
   calls `/insights` on each stored `ig_post_id` (reach, views, likes,
   comments, saved, shares, total_interactions, plus Reel watch-time /
   feed follows+profile_visits extras) and writes `analytics/insights.csv`
   (latest) + `analytics/insights-history.csv` (append-only). Failures are
   per post — a deleted post, a throttle, or an expired token never aborts
   the whole run. `python scripts/collect_insights.py --rollup-only` prints
   the mean-per-account/format/family table from the CSV with no token and
   no API call. Column meanings and caveats (48 h insights lag, reach is an
   estimate, posted time vs. scheduled slot) are in the script's docstring.

Content generation (what actually goes into `content/queue/`) is not yet
built for any account — this repo currently only has the publish/refresh
rails. Each account's content strategy gets designed and built separately
once its niche/purpose is defined.

## Required GitHub Secrets (per account, e.g. `hype_tingles`)

- `IG_ACCESS_TOKEN_HYPE_TINGLES` — long-lived Instagram access token
- `IG_USER_ID_HYPE_TINGLES` — Instagram Business Account ID
- `REPO_ADMIN_TOKEN` — **shared across all accounts in this repo**: a
  fine-grained PAT scoped to this repo only, with "Secrets: Read and write"
  permission (lets each account's refresh workflow write its own renewed
  token back automatically). Set once.

## Adding a new account

1. Add it as an Instagram Tester under the TrendRadar Publisher Meta app
   (App roles → Roles → Add People → Instagram Tester → accept the invite
   from the account's own Instagram → Apps and Websites), then generate its
   access token from the app's "Generate access tokens" screen.
2. `mkdir -p accounts/<name>/content/{queue,posted,failed}` (+ `.gitkeep`
   in each).
3. Copy `publish-hype_tingles.yml` → `publish-<name>.yml` and
   `refresh-hype_tingles.yml` → `refresh-<name>.yml`; replace every
   `hype_tingles`/`HYPE_TINGLES` with the new account's name.
4. Add that account's `IG_ACCESS_TOKEN_<NAME>` / `IG_USER_ID_<NAME>`
   repository secrets. `REPO_ADMIN_TOKEN` is already shared, no change
   needed.
5. Add `IG_ACCESS_TOKEN_<NAME>: ${{ secrets.IG_ACCESS_TOKEN_<NAME> }}` to
   the env block of `collect-insights.yml` so the daily Insights run covers
   the new account too (the script discovers the account folder by itself;
   only the token line is needed).
6. Design and build that account's content-generation pipeline separately.

## Manual test run

Every workflow supports `workflow_dispatch` — trigger a run by hand from
the repo's Actions tab.
