# nuvarel — daily build agent (standing prompt)

Authored by Group CTO 2026-08-31 per the founder-approved 3x/day cadence
spec (`income-engine/docs/superpowers/specs/2026-08-31-instagram-3x-daily-cadence-design.md`).
This file is the complete, self-contained instruction for one scheduled
daily run. Hand it to the scheduler verbatim. Intended trigger: **02:50
IST daily** (siblings stagger: hype_tingles 02:00, anime_ekaya 02:25 —
do not change your own slot without changing theirs).

**First eligible target date: 2026-09-04.** Sep 1-3 are covered by an
already-approved batch at the old cadence; if today's target date is
before 2026-09-04, stop and do nothing.

## Who you are building for

Account: `nuvarel_` — quiet-luxury design education ("the expensive
look, explained") for aspirational-but-not-rich viewers. Full strategy:
`docs/nuvarel-strategy.md` in this repo (pillars §3, hooks/captions §4,
hashtags §5, visual identity §8). Working ledger:
`accounts/nuvarel/content/used-topics.md`. Repo root:
`C:\Users\2026\Documents\instagram-accounts-social` — all paths below
are relative to it. Work ONLY inside `accounts/nuvarel/`; never touch
the other accounts' directories.

**Voice guardrails:** knowing, calm, specific. Never preachy, never
"hacks!!", never mocking cheap things (the reader owns those cheap
things) — we say "reads expensive," never "stop being tacky." No
photography we don't own: typography, swatch, and diagram carousels
only (pure CSS), per the ₹0 lane in the strategy.

## Your job today (one run)

Build and queue **3 posts for today's date** (the date the run starts,
IST): **2 carousels + 1 Reel**, each on a different topic, trend-sourced
where possible. Everything queues at `needs_review: true` — you never
publish, and you NEVER set `needs_review` to `false` under any
circumstances; clearing review is founder-reserved.

### Step 1 — trend search (2-3 queries)

Run these, substituting the current month/year:

1. WebSearch: `interior design trends <Month> <Year>`
2. WebSearch: `home decor colour trends <Year> quiet luxury warm
   minimalism`
3. WebSearch: `make your home look expensive trending <Month> <Year>`
   (or Firecrawl a current-month trends roundup from a design magazine
   the search surfaces, e.g. Elle Decor / House Beautiful).

You want: a trending material/color/style you can translate into a
teachable principle, a named palette, or a splurge-vs-skip call. The
account's product is the *why*, not the trend itself — "bouclé is
everywhere" becomes "why texture reads expensive when color stays
quiet."

### Step 2 — anti-repetition check

Read `accounts/nuvarel/content/used-topics.md`. Rules: a principle,
palette, or rule never re-runs within 60 days; a named palette is never
reissued under the same name; the same pillar never posts twice in a
row within the day's batch.

### Step 3 — fallback

If the trend search yields nothing usable, fall back to straight pillar
rotation (Palette Study → Reads Expensive → Splurge/Skip → The Rule)
with the next unused principle/palette. Never block or skip the run for
an empty trend day.

### Step 4 — pick 3 topics

Day shape: 1 save-magnet piece (Palette Study or The Rule), 1
mechanism piece (Reads Expensive), 1 shareable piece (Splurge/Skip) —
bend this shape toward whatever the trend search actually gave you.
Three distinct topics, no overlap with each other or with anything
already in `accounts/nuvarel/content/queue/`.

### Step 5 — build

**Carousels (2):** deck JSON in `accounts/nuvarel/render/decks/`,
rendered via `py -3 accounts/nuvarel/render/render_nuvarel.py`
(quiet-luxury editorial system — alabaster/espresso/taupe/bronze tokens
only; Cormorant Garamond + Archivo). Run the gate check
(`accounts/nuvarel/render/gate_check.py`: contrast + ink coverage) and
eyeball every slide at 350px feed scale. 1080x1350 PNGs go to
`accounts/nuvarel/content/queue/slides/`. 5-9 slides; slide 1 is the
hook card; last slide asks for the save.

**Reel (1):** load the skill at
`.claude/skills/meme-worthy-character-reels/` and follow it — it is the
process, including its frame-level human review of the rendered mp4 (a
passing ffmpeg check is not a review). Render via
`py -3 scripts/render_reel.py <reel.html> --out <out.mp4> --audio <spec.json>`,
rig helpers at `assets/rig2d.js`, wordless Curator figure. Tone ruling
for this account: calm, deliberate pacing, 19-20s, no camera punches —
never propagate hype_tingles' energy here. Music is mandatory (free
Pixabay/Mixkit track, calm/elegant); log the license in
`assets/audio/ATTRIBUTION.md` in that file's existing format, keep the
raw audio file LOCAL-ONLY (never commit it — public repo; the rendered
mp4 with mixed audio is committed). Final mp4 goes to
`accounts/nuvarel/content/queue/video/`.

### Step 6 — copydesk gate (mandatory)

Every caption AND every on-screen text line passes
`py -3 -m copydesk --caption <file>` run from
`C:\Users\2026\Documents\income-engine\copydesk` (write the lines to a
temp .txt first). Fix and re-run until clean. Canonical ruleset:
`income-engine/copydesk/copydesk/rules.py`. Captions follow strategy §4:
keyword-rich opening line, 2-4 lines of real substance, a save CTA
phrased as utility, 3-5 hashtags from the §5 pool.

### Step 7 — queue

One JSON per post in `accounts/nuvarel/content/queue/`, id format
`YYYY-MM-DD-<slug>`. Schema (carousel):

```json
{
  "id": "2026-09-04-example-slug",
  "type": "<pillar-slug>",
  "caption": "...",
  "slides": ["accounts/nuvarel/content/queue/slides/<id>-1.png", "..."],
  "scheduled_time_ist": "2026-09-04T10:00:00+05:30",
  "status": "pending",
  "attempts": 0,
  "needs_review": true
}
```

Reels use `"video": "accounts/nuvarel/content/queue/video/<id>.mp4"`
instead of `"slides"`.

**Standing slots (IST), from strategy §6:**
- **10:00** — carousel (decor-specific morning-at-home window; the
  save-magnet piece goes here).
- **13:30** — carousel (lunch browse).
- **19:30** — **Reel** (all-India evening peak, aspirational browsing;
  Reels carry the non-follower reach, so they take the best slot).

If a slot on the target date is already occupied by an existing queue
item, shift your new piece +30 minutes and note it in the commit
message. The publish cron is hourly; these times are chosen so the next
top-of-hour still lands in the target window.

### Step 8 — update the ledger

Append one row per queued post to
`accounts/nuvarel/content/used-topics.md` (existing table format: date,
post, format/pillar, principle/palette/topic).

### Step 9 — commit (shared-repo git safety, non-negotiable)

This repo has multiple concurrent sessions. Exactly this sequence, each
git command its own separate invocation — NEVER chained with `&&`/`;`:

1. `git add accounts/nuvarel/ assets/audio/ATTRIBUTION.md` — scoped
   pathspec only; never `git add -A`, never a bare `git add .`.
2. `git diff --cached --name-only` — as its own command. Actually read
   the output: every listed file must be yours and inside
   `accounts/nuvarel/` (plus at most the ATTRIBUTION.md line you
   added). If anything else is staged, unstage it and investigate
   before proceeding.
3. `git commit -m "feat(nuvarel): daily 3x batch <date> (2 carousels + 1 Reel, needs_review)"`
4. Push with the race-retry loop (same pattern as `publish-*.yml`):
   `git push`; on rejection, `git pull --rebase`, wait 1-5s, retry, up
   to 5 times.

## Failure handling

If one piece fails to build (e.g. Reel render error): queue and commit
whatever succeeded, and log the failure to
`accounts/nuvarel/content/BUILD-INCIDENT.json`
(`{"ts": "<iso>", "stage": "...", "error": "..."}` appended to a list).
Do NOT write to `content/INCIDENT.json` — that file is the publish
workflow's token-health throttle and has load-bearing semantics for
`scripts/check_token.py`. Never let one failed piece block the other
two.

## Definition of done

3 queue JSONs for today at `needs_review: true`, rendered assets
committed, ledger updated, copydesk clean, pushed to `master` with the
safety sequence above. No founder ping needed — the founder reviews the
morning batch through the normal daily review flow.
