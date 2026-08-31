# hype_tingles — daily build agent (standing prompt)

Authored by Group CTO 2026-08-31 per the founder-approved 3x/day cadence
spec (`income-engine/docs/superpowers/specs/2026-08-31-instagram-3x-daily-cadence-design.md`).
This file is the complete, self-contained instruction for one scheduled
daily run. Hand it to the scheduler verbatim. Intended trigger: **02:00
IST daily** (siblings stagger: anime_ekaya 02:25, nuvarel 02:50 — do not
change your own slot without changing theirs).

**First eligible target date: 2026-09-04.** Sep 1-3 are covered by an
already-approved batch at the old cadence; if today's target date is
before 2026-09-04, stop and do nothing.

## Who you are building for

Account: `hype_tingles` — a viral animal-comedy entertainment brand.
Full strategy: `income-engine/docs/hype_tingles-strategy.md` (voice
bible §4, format menu F1-F5 §5, cast §8, visual identity "Neon Panel"
§11). Working ledger: `accounts/hype_tingles/brand/topic-bank.md`.
Repo root: `C:\Users\2026\Documents\instagram-accounts-social` — all
paths below are relative to it. Work ONLY inside
`accounts/hype_tingles/`; never touch the other accounts' directories.

## Your job today (one run)

Build and queue **3 posts for today's date** (the date the run starts,
IST): **2 carousels + 1 Reel**, each on a different topic, trend-sourced
where possible. Everything queues at `needs_review: true` — you never
publish, and you NEVER set `needs_review` to `false` under any
circumstances; clearing review is founder-reserved.

### Step 1 — trend search (2-3 queries)

Run these, substituting the current month/year/date:

1. WebSearch: `viral memes trending this week <Month> <Year>`
2. Firecrawl scrape: `https://knowyourmeme.com/memes/trending` — take
   the top trending meme/format names and what they're about.
3. WebSearch: `pop culture moments everyone is talking about this week
   <Month> <Year>`

You want *human behaviors and cultural moments the animal cast can react
to* (a trend the Pigeon can teach, the Cat can review, or the Breaking
News desk can cover). Hard filters:
- Never repost or recreate the meme asset itself — original content in
  our own template only (Meta's originality policy kills aggregators).
- No real, identifiable individuals as joke targets; no tragedy/news
  requiring taste judgment. When in doubt, drop the topic.
- Stylized/illustrated only, never photoreal AI imagery.

### Step 2 — anti-repetition check

Read `accounts/hype_tingles/brand/topic-bank.md`. Rules: never the same
format twice in a row; F1 (Panel) max 1/day; never repeat a
format+topic+cast combination. Also check "Queued promises to keep" at
the bottom of that file — an owed episode/format beats a trend topic.

**Scene/prop rule (Reels, added 2026-08-31 after a real near-duplicate
on a sibling account):** recurring sets and cast are this brand's
format, but two Reels can differ in joke and still look identical at
thumbnail scale. Before building the Reel, look at the last **7 days'**
Reel QA frames (`accounts/hype_tingles/reels/<id>/qa/` where present)
and the ledger's topic column: the same scene-set + hero-prop/gag
combination (e.g. "news desk + phone prop") must not recur within 7
days. Same set with a genuinely different prop/composition is fine;
when in doubt, compare your hook frame against theirs at ~350px.

### Step 3 — fallback

If the trend search yields nothing usable for a slot, take the next
topic from the topic wheel in `topic-bank.md` with the normal format
rotation. Never block or skip the run for an empty trend day.

### Step 4 — pick 3 topics

Day shape (strategy §10): 1 flagship-format piece (F1/F3), 1 fast
relatable piece (F2/F4), 1 reactive/experimental piece (F5 or a format
test — this is where today's trend topic most naturally lands). Three
distinct topics, no overlap with each other or with anything already in
`accounts/hype_tingles/content/queue/`.

### Step 5 — build

**Carousels (2):** deck JSON in `accounts/hype_tingles/tools/decks/`,
rendered via `py -3 accounts/hype_tingles/tools/render.py` (Neon Panel
brand system — tokens only, no new colors/fonts). 1080x1350 PNGs go to
`accounts/hype_tingles/content/queue/slides/`. Eyeball every slide at
feed scale (~350px) before queueing; the cat-payoff slide inverts to
volt background.

**Reel (1):** load the skill at
`.claude/skills/meme-worthy-character-reels/` and follow it — it is the
process, including its frame-level human review of the rendered mp4 (a
passing ffmpeg check is not a review). Render via
`py -3 scripts/render_reel.py <reel.html> --out <out.mp4> --audio <spec.json>`,
rig helpers at `assets/rig2d.js`. Tone ruling for this account: punchy,
meme-fast, ~14-15s. Music is mandatory (free Pixabay/Mixkit track); log
the license in `assets/audio/ATTRIBUTION.md` in that file's existing
format, keep the raw audio file LOCAL-ONLY (never commit it — public
repo; the rendered mp4 with mixed audio is committed). Final mp4 goes to
`accounts/hype_tingles/content/queue/video/`.

### Step 6 — copydesk gate (mandatory)

Every caption AND every on-screen text line passes
`py -3 -m copydesk --caption <file>` run from
`C:\Users\2026\Documents\income-engine\copydesk` (write the lines to a
temp .txt first). Fix and re-run until clean. Canonical ruleset:
`income-engine/copydesk/copydesk/rules.py`. Captions follow strategy §7:
keyword-rich first line, 1-2 punch lines, a send/tag CTA, exactly 3-5
hashtags.

### Step 7 — queue

One JSON per post in `accounts/hype_tingles/content/queue/`, id format
`YYYY-MM-DD-<slug>`. Schema (carousel):

```json
{
  "id": "2026-09-04-example-slug",
  "type": "<format-slug>",
  "caption": "...",
  "slides": ["accounts/hype_tingles/content/queue/slides/<id>-1.png", "..."],
  "scheduled_time_ist": "2026-09-04T08:00:00+05:30",
  "status": "pending",
  "attempts": 0,
  "needs_review": true
}
```

Reels use `"video": "accounts/hype_tingles/content/queue/video/<id>.mp4"`
instead of `"slides"`.

**Standing slots (IST), from strategy §9:**
- Weekdays: 08:00 carousel, 13:00 carousel, **20:00 Reel** (prime slot
  carries the strongest piece; Reels carry non-follower reach).
- Weekends: 11:30 carousel, 16:30 carousel, **20:30 Reel**.

If a slot on the target date is already occupied by an existing queue
item, shift your new piece +30 minutes and note it in the commit
message. The publish cron is hourly; these times are chosen so the next
top-of-hour still lands in the target window.

### Step 8 — update the ledger

Append one row per queued post to
`accounts/hype_tingles/brand/topic-bank.md` (existing table format:
date, post id, format, topic, cast used). The format cell MUST include
the exact `type` value from the queue JSON, verbatim (the F-code prefix
before it is fine, e.g. "F5 reel-breaking-news") — a ledger filed under
one vocabulary while the queue uses another produced a real
anti-repetition false clear on a sibling account (2026-08-31). Add any
new on-air promise to "Queued promises to keep."

### Step 9 — commit (shared-repo git safety, non-negotiable)

This repo has multiple concurrent sessions. Exactly this sequence, each
git command its own separate invocation — NEVER chained with `&&`/`;`:

1. `git add accounts/hype_tingles/ assets/audio/ATTRIBUTION.md` —
   scoped pathspec only; never `git add -A`, never a bare `git add .`.
2. `git diff --cached --name-only` — as its own command. Actually read
   the output: every listed file must be yours and inside
   `accounts/hype_tingles/` (plus at most the ATTRIBUTION.md line you
   added). If anything else is staged, unstage it and investigate
   before proceeding.
3. `git commit -m "feat(hype_tingles): daily 3x batch <date> (2 carousels + 1 Reel, needs_review)"`
4. Push with the race-retry loop (same pattern as `publish-*.yml`):
   `git push`; on rejection, `git pull --rebase`, wait 1-5s, retry, up
   to 5 times.

## Failure handling

If one piece fails to build (e.g. Reel render error): queue and commit
whatever succeeded, and log the failure to
`accounts/hype_tingles/content/BUILD-INCIDENT.json`
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
