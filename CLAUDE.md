# instagram-accounts-social — standing instructions (loaded every session)

Automated Instagram publishing for the founder's revived personal/business
accounts (`hype_tingles`, `anime_ekaya`, `nuvarel_` live; 4 more to come),
one shared `ACCOUNT_DIR`-parameterized pipeline, one folder per account.
Registered income-engine subproject; current status, blocker and next step
live only in `../docs/registry/instagram_accounts_social.md` — never
duplicate status here.

## Where this repo sits (changed 2026-09-12)

This is its own git repo (`github.com/harshalpweb/instagram-accounts-social`)
nested inside `income-engine/` and gitignored there — the same pattern as
`../trend_predictor/` and `../codelens/`. Two consequences:

- `../CLAUDE.md` (the portfolio charter) now loads into every session here.
  Its copydesk rule, shared-repo git-safety rule, founder-communication
  rules and CTO-first routing all apply in this repo directly.
- Paths into the portfolio are one level up: the vendored ffmpeg is
  `../video_lab/samples/hyperframes/.bin/ffmpeg.exe` (`scripts/render_reel.py`
  resolves it; `FFMPEG_BIN` overrides), 2D/3D character work is in
  `../video_lab/samples/motion-engine-2d/` and `../blender_studio/scenes/`,
  and `../video_lab/samples/motion-engine-2d/` reads this repo's
  `assets/audio/` kit by relative path. Any absolute `C:\...` path to this
  repo in code is a bug — resolve from `__file__` instead.

## Roster

`docs/ROSTER.md` — seven local roles under `.claude/agents/`
(`cto`, `audience-strategist`, `creative-director`, `art-director`,
`niche-researcher`, `content-reviewer`, `growth-analyst`), plus the
portfolio roles in `../docs/ROSTER.md`. Expanded from four 2026-09-12 by
Group CTO. The local `cto` reports to Group CTO on every matter (founder
ruling 2026-09-12); the portfolio Chief Creative Officer's verdict wins
over both `creative-director` and `art-director` on cross-account brand
coherence. Four roles touch creative work and the split is by discipline,
not by account — `audience-strategist` owns who and why,
`creative-director` owns what it says, `art-director` owns how it looks,
`niche-researcher` owns whether it is true. `docs/ROSTER.md` also records
the roles deliberately **not** created and the tripwire that reopens each,
plus the bar a new local role must clear. The main session here is the
Chief of Staff for this repo: it convenes roles, dispatches the daily
builds, records decisions in `docs/consults/` (local-role consults) or
`../docs/consults/` (anything a portfolio role ruled — see
`docs/ROSTER.md`).

## Hard rules in this repo

1. **`needs_review` is the publish gate.** Every queued piece is built at
   `needs_review: true`. Flipping it to `false` publishes to the founder's
   own accounts at the next hourly run.

   **Founder ruling, 2026-09-12 — auto-clear below 10,000 followers.** The
   founder decided directly (relayed and confirmed through the CoS) that
   **no founder review is required before a post goes live on any account
   under 10,000 followers.** He reviews on Instagram after publish instead.
   This is a founder decision, not a Group CTO one.

   What this changes: **only the founder-approval step.** Both quality
   gates stay exactly as they are and now gate harder
   (`docs/cadence-and-format-policy.md` §5) — `content-reviewer` first on
   defects, then `creative-director` (with `art-director` on look) on
   brand fit. A piece that fails either gate still goes to
   `accounts/<acct>/content/qa-hold/` and never publishes.

   The mechanism: after **both** verdicts are PASS on a piece, **the
   session that dispatched the build** sets `needs_review: false` on that
   piece and commits it, naming both verdicts in the commit message. The
   build agent still never flips it — the builder and the clearer must not
   be the same actor, which is the whole point of the ladder. No local
   role flips it either.

   **At 10,000 followers on an account, the auto-clear stops for that
   account** and founder approval returns, unless the founder rules
   otherwise. Follower count is checked per account, not portfolio-wide.
   As of 2026-09-12 all three accounts are far below 100 followers, so
   this applies to every account in the repo today. Group CTO may still
   clear a piece directly at any follower count, recorded in a consult
   (2026-09-12 ruling).
2. **Licensed media never gets committed.** Mixkit audio (`assets/audio/`)
   and Pexels clips (`assets/video/`) are usable inside a rendered post but
   not redistributable; this repo is public. `.gitignore` enforces it —
   commit the attribution record, not the file.
3. **Tokens are per account.** The publisher reads `ACCOUNT_DIR` plus
   generic `IG_ACCESS_TOKEN` / `IG_USER_ID` (each workflow maps its own
   account's secret in); `scripts/collect_insights.py` reads
   `IG_ACCESS_TOKEN_<ACCOUNT>` for every account in one run. Running the
   collector ad hoc without the right token overwrites
   `analytics/insights.csv` with empty rows (it happened 2026-09-05).
   Secrets stay in GitHub Actions secrets or a local `.env`; never in a
   committed file.
4. **Rate-limit hygiene.** Instagram caps ~25 API publishes per account per
   rolling 24 h, counting failed attempts. Stagger clearances; the
   publisher aborts on a rate limit instead of burning retries — keep it so.
5. **`ai_generated: true` is SUSPENDED, founder-direct override, 2026-09-12.**
   The publisher still supports mapping it to Meta's `is_ai_generated`
   (Reel container, or carousel parent only) if a piece sets it, but no
   daily build should set it until the founder says otherwise. This
   reverses Group Legal's 2026-09-05 read that the flag is required for
   photoreal AI video under Meta's Misinformation self-disclosure duty —
   the founder was told this directly (reach data was inconclusive: the
   one clear counter-example, `2026-09-08-the-vein-over-the-edge`, got
   102 reach with the flag on, in line with unflagged Reels; the account's
   best-ever post, `2026-09-04-cables-read-cheap` at 1,091 reach, predates
   the flag entirely and is a different, non-photoreal format) and gave a
   direct, final order to stop anyway. **Do not silently re-enable this**
   — a future session finding Legal's original read should not restore
   the flag without a fresh, explicit founder decision; this is a real
   compliance/policy-risk trade the founder made knowingly, not a bug.
6. **The daily-build prompts are architecture, not config.** Each
   `accounts/<acct>/docs/daily-build-agent-prompt.md` is handed verbatim to
   a build agent. A cadence, slot, pillar or format change is not done
   until every prompt copy is audited; nuvarel additionally reads
   `accounts/nuvarel/docs/build-gates.json` first and builds only open
   lanes.
9. **Cadence, format mix and posting times are computed, not written
   down** (Group CTO, 2026-09-12, founder-direct). Every build runs
   `py -3 scripts/plan_day.py --account <acct>` before choosing topics and
   builds exactly the slots it returns: **3 posts a day until the account
   passes 50,000 followers**, with the FEED/REELS mix recomputed daily from
   `analytics/insights-history.csv` and each slot's time drawn from inside
   a window so the schedule never repeats day to day. Numbers live in
   `docs/slot-policy.json`; the rule, the evidence behind it, and the
   hook/CTA policy live in `docs/cadence-and-format-policy.md`, which is
   canonical over any prompt copy.
7. **Anti-repetition ledgers are checked on the fields the pipeline
   actually writes** (queue JSON `type` + topic keywords + scene/prop
   set), not on a drifted column — a false clear already shipped a
   near-duplicate once.
8. **Every customer-facing caption and on-screen line passes copydesk**
   (`py -3 -m copydesk`, from `../copydesk/`) before it is queued.

## Execution standards (portfolio, applied here)

- **Ladder:** the daily-build prompt is the implementer spec; a piece is
  reviewed by `content-reviewer` (never by the agent that built it), brand
  fit by `creative-director` on the pieces that passed, then the founder
  gate. The session that dispatched the build convenes both reviews on the
  pushed commit and logs each verdict in `.claude/agents/roster-log.md`; a
  piece still FAILed after the fix rounds moves to
  `accounts/<acct>/content/qa-hold/` (outside the publisher's
  `content/queue/` scan; never `content/failed/`, which is publisher
  state). Judgment calls go `cto` → Group CTO.
- **Fix-round circuit breaker:** rounds 1-3 same implementer; round 4
  escalates one tier; round 5 is a hard stop — report BLOCKED.
- **Concurrent-dispatch cap:** at most 2-3 parallel agents, with a
  write-ahead dispatch ledger once more than one is in flight.
- **Shared checkout:** several sessions use this one working tree. Scoped
  `git add`, `git diff --cached --name-only` as its own call, pathspec on
  `git commit`, `git pull --rebase` before push.

## How to run

- Tests: `py -3 -m pytest tests -q`
- Render a Reel: `py -3 scripts/render_reel.py <reel.html> --out <out.mp4> --audio <spec.json> --qa-dir <dir>`
- Publish (CI does this hourly per account; local runs need the token):
  `ACCOUNT_DIR=accounts/<acct> py -3 scripts/publish_due_posts.py`
- Insights rollup, no token needed: `py -3 scripts/collect_insights.py --rollup-only`
- Plan a day (cadence, format mix, jittered slot times; no token, no API):
  `py -3 scripts/plan_day.py --account <acct>` (add `--json` for machine use)
- Load `.claude/skills/meme-worthy-character-reels/` before any Reel build.

## Strategy documents

- `docs/cadence-and-format-policy.md` — **canonical for all accounts**:
  the 3/day-until-50k floor, the data-driven format mix, posting-time
  windows, the hook/CTA rule, the quality floor. Wins over any prompt copy.
- `docs/nuvarel-strategy.md` — canonical for `nuvarel_` (**Revision 3,
  2026-09-12, founder-direct**: §9-§15 carry the long-term vision,
  monetization paths, niche-width ruling and the real-footage lane, and
  supersede §7).
- `docs/trend-research-step-spec.md` — daily niche trend research.
  **Specified, NOT live — blocked on Chief Security Officer review.**
- `docs/nuvarel-viral-reel-research-2026-09-12.md` — niche viral-Reel
  research, input to weigh against the strategy above, not a replacement.
- `../docs/hype_tingles-strategy.md`, `../docs/anime_ekaya-strategy.md` —
  canonical for those two accounts, still in the portfolio `docs/`;
  moving them here is the `creative-director`'s first task.
- Full index: `docs/RESEARCH-INDEX.md`.
