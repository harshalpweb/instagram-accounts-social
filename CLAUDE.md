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

`docs/ROSTER.md` — four local roles (`cto`, `creative-director`,
`content-reviewer`, `growth-analyst`) under `.claude/agents/`, plus the
portfolio roles in `../docs/ROSTER.md`. The local `cto` reports to Group
CTO on every matter (founder ruling 2026-09-12); the portfolio Chief
Creative Officer's verdict wins over `creative-director` on cross-account
brand coherence. The main session here is the Chief of Staff for this
repo: it convenes roles, dispatches the daily builds, records decisions in
`docs/consults/`.

## Hard rules in this repo

1. **`needs_review` is the publish gate.** Every queued piece is built at
   `needs_review: true`. Flipping it to `false` publishes to the founder's
   own accounts at the next hourly run. The founder clears it (live, or by
   editing the JSON); under the 2026-09-12 ruling Group CTO may also,
   recorded in a consult. No local role and no daily-build agent ever
   flips it.
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
5. **AI-generated content carries `ai_generated: true`** in its queue JSON;
   the publisher maps it to Meta's `is_ai_generated` (Reel container, or
   carousel parent only). Required for photoreal AI video per Group
   Legal's 2026-09-05 read.
6. **The daily-build prompts are architecture, not config.** Each
   `accounts/<acct>/docs/daily-build-agent-prompt.md` is handed verbatim to
   a build agent. A cadence, slot, pillar or format change is not done
   until every prompt copy is audited; nuvarel additionally reads
   `accounts/nuvarel/docs/build-gates.json` first and builds only open
   lanes.
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
- Load `.claude/skills/meme-worthy-character-reels/` before any Reel build.

## Strategy documents

- `docs/nuvarel-strategy.md` — canonical for `nuvarel_` (revised
  2026-09-05, founder-direct).
- `docs/nuvarel-viral-reel-research-2026-09-12.md` — niche viral-Reel
  research, input to weigh against the strategy above, not a replacement.
- `../docs/hype_tingles-strategy.md`, `../docs/anime_ekaya-strategy.md` —
  canonical for those two accounts, still in the portfolio `docs/`;
  moving them here is the `creative-director`'s first task.
- Full index: `docs/RESEARCH-INDEX.md`.
