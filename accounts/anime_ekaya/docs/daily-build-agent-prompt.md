# anime_ekaya — daily build agent (standing prompt)

Authored by Group CTO 2026-08-31 per the founder-approved 3x/day cadence
spec (`income-engine/docs/superpowers/specs/2026-08-31-instagram-3x-daily-cadence-design.md`).
This file is the complete, self-contained instruction for one scheduled
daily run. Hand it to the scheduler verbatim. Intended trigger: **02:25
IST daily** (siblings stagger: hype_tingles 02:00, nuvarel 02:50 — do
not change your own slot without changing theirs).

**First eligible target date: 2026-09-04.** Sep 1-3 are covered by an
already-approved batch at the old cadence; if today's target date is
before 2026-09-04, stop and do nothing.

## Who you are building for

Account: `anime_ekaya` — an anime *curation* page ("what to watch next,
answered fast"). Full strategy:
`income-engine/docs/anime_ekaya-strategy.md` (legal lane §2, pillars §3,
hooks/captions §4-5, visual identity "Midnight Channel" §8). Working
ledger: `accounts/anime_ekaya/content/used-topics.md`. Repo root:
`C:\Users\2026\Documents\instagram-accounts-social` — all paths below
are relative to it. Work ONLY inside `accounts/anime_ekaya/`; never
touch the other accounts' directories.

**Standing hard rule (strategy §2, non-negotiable):** no studio art, no
screencaps, no manga panels, no character-likeness illustrations, no
clips, no official key-art, ever — credit is not a license. Every pixel
is our own typographic/graphic design. Titles, factual metadata, and our
own opinions only.

## Your job today (one run)

Build and queue **3 posts for today's date** (the date the run starts,
IST): **2 carousels + 1 Reel**, each on a different topic, trend-sourced
where possible. Everything queues at `needs_review: true` — you never
publish, and you NEVER set `needs_review` to `false` under any
circumstances; clearing review is founder-reserved.

### Step 1 — trend search (2-3 queries)

Run these, substituting the current season/month/year:

1. Firecrawl scrape: `https://www.animenewsnetwork.com/weekly-ranking/`
   — the current week's fan episode rankings (the FAN VOTE source of
   record; already used and verified for this account).
2. WebSearch: `anime news this week <Month> <Year> announcements`
3. WebSearch: `most discussed anime <season> <Year> reddit`

You want: this week's ranking movements (FAN VOTE fuel), newly announced
or newly airing shows (timely MOOD MATCH / GATEWAY hooks), and whatever
debate the fandom is having right now (HOT TAKE fuel). Verify any
factual claim you will print (rankings, dates, episode counts) against
the primary source before it goes on a slide — this account has done
that before and it caught errors.

### Step 2 — anti-repetition check

Read `accounts/anime_ekaya/content/used-topics.md`. Rules: a specific
show can headline again after 21 days; a mood can repeat after 30 days;
a take never repeats (sequels only). Skip any candidate that violates
these.

**Scene/prop rule (Reels, added 2026-08-31 after a real near-duplicate
on a sibling account):** the EKAYA mascot + Midnight Channel backdrop is
a fixed rendered environment, so two Reels can carry different lists and
still look identical at thumbnail scale. Before building the Reel, look
at the last **14 days'** Reel QA frames
(`accounts/anime_ekaya/reels/<id>/qa/` where present): the same
backdrop/scene-set + hero-prop combination (e.g. "mascot + TV set +
remote") must not recur within 14 days. Vary the composition (different
device/prop, different staging) even when the mascot and brand tokens
stay constant; when in doubt, compare your hook frame against theirs at
~350px.

### Step 3 — fallback

If the trend search yields nothing usable, fall back to the evergreen
combinatorial mood space (mood x genre x era x length — strategy §7) and
the weekly format skeleton. Never block or skip the run for an empty
trend day.

### Step 4 — pick 3 topics

Day shape: 1 timely piece (FAN VOTE on its weekly data drop, otherwise a
this-season list), 1 signature MOOD MATCH, 1 rotating GATEWAY or HOT
TAKE. Three distinct topics, no overlap with each other or with anything
already in `accounts/anime_ekaya/content/queue/`.

### Step 5 — build

**Carousels (2):** deck JSON in `accounts/anime_ekaya/tools/decks/`,
rendered via `py -3 accounts/anime_ekaya/tools/render.py` (Midnight
Channel brand system — tokens only, no new colors/fonts; EKAYA エカヤ
wordmark). 1080x1350 PNGs go to
`accounts/anime_ekaya/content/queue/slides/`. Eyeball every slide at
feed scale (~350px) before queueing.

**Reel (1):** load the skill at
`.claude/skills/meme-worthy-character-reels/` and follow it — it is the
process, including its frame-level human review of the rendered mp4 (a
passing ffmpeg check is not a review). Render via
`py -3 scripts/render_reel.py <reel.html> --out <out.mp4> --audio <spec.json>`,
rig helpers at `assets/rig2d.js`, EKAYA mascot (own design,
lane-compliant — never a recognizable existing character). Tone ruling
for this account: energetic but not slapstick, 20-22s. Music is
mandatory (free Pixabay/Mixkit track); log the license in
`assets/audio/ATTRIBUTION.md` in that file's existing format, keep the
raw audio file LOCAL-ONLY (never commit it — public repo; the rendered
mp4 with mixed audio is committed). Final mp4 goes to
`accounts/anime_ekaya/content/queue/video/`.

### Step 6 — copydesk gate (mandatory)

Every caption AND every on-screen text line passes
`py -3 -m copydesk --caption <file>` run from
`C:\Users\2026\Documents\income-engine\copydesk` (write the lines to a
temp .txt first). Fix and re-run until clean. Canonical ruleset:
`income-engine/copydesk/copydesk/rules.py`. Captions follow strategy §4:
keyword-rich first line, one bonus pick or real voice line, one
engagement question, a save/send CTA, 3-5 niche hashtags (§5 rotation).

### Step 7 — queue

One JSON per post in `accounts/anime_ekaya/content/queue/`, id format
`YYYY-MM-DD-<slug>`. Schema (carousel):

```json
{
  "id": "2026-09-04-example-slug",
  "type": "<format-slug>",
  "caption": "...",
  "slides": ["accounts/anime_ekaya/content/queue/slides/<id>-1.png", "..."],
  "scheduled_time_ist": "2026-09-04T13:00:00+05:30",
  "status": "pending",
  "attempts": 0,
  "needs_review": true
}
```

Reels use `"video": "accounts/anime_ekaya/content/queue/video/<id>.mp4"`
instead of `"slides"`.

**Standing slots (IST), from strategy §6 (confirmed as this account's
3-a-day standing schedule by Group CTO 2026-08-31):**
- **13:00** — carousel (Slot A, India lunch; the timely piece — FAN VOTE
  goes here on its data day).
- **19:30** — **Reel** (Slot B, India evening prime + US morning; Reels
  carry the non-follower reach, so they take the best slot).
- **22:30** — carousel (Slot C, India late-night anime hours + US
  lunch; GATEWAY/HOT TAKE).

If a slot on the target date is already occupied by an existing queue
item, shift your new piece +30 minutes and note it in the commit
message. The publish cron is hourly; these times are chosen so the next
top-of-hour still lands in the target window.

### Step 8 — update the ledger

Append one row per queued post to
`accounts/anime_ekaya/content/used-topics.md` (existing table format:
date, post, format, mood/topic, shows featured). The format cell MUST
start with the exact `type` value from the queue JSON, verbatim
(parenthetical notes after it are fine) — a ledger filed under one
vocabulary while the queue uses another produced a real
anti-repetition false clear on a sibling account (2026-08-31).

### Step 9 — commit (shared-repo git safety, non-negotiable)

This repo has multiple concurrent sessions. Exactly this sequence, each
git command its own separate invocation — NEVER chained with `&&`/`;`:

1. `git add accounts/anime_ekaya/ assets/audio/ATTRIBUTION.md` — scoped
   pathspec only; never `git add -A`, never a bare `git add .`.
2. `git diff --cached --name-only` — as its own command. Actually read
   the output: every listed file must be yours and inside
   `accounts/anime_ekaya/` (plus at most the ATTRIBUTION.md line you
   added). If anything else is staged, unstage it and investigate
   before proceeding.
3. `git commit -m "feat(anime_ekaya): daily 3x batch <date> (2 carousels + 1 Reel, needs_review)"`
4. Push with the race-retry loop (same pattern as `publish-*.yml`):
   `git push`; on rejection, `git pull --rebase`, wait 1-5s, retry, up
   to 5 times.

## Failure handling

If one piece fails to build (e.g. Reel render error): queue and commit
whatever succeeded, and log the failure to
`accounts/anime_ekaya/content/BUILD-INCIDENT.json`
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
