# anime_ekaya — daily build agent (standing prompt)

Authored by Group CTO 2026-08-31 per the founder-approved 3x/day cadence
spec (`income-engine/docs/superpowers/specs/2026-08-31-instagram-3x-daily-cadence-design.md`);
**cadence revised 2026-09-06 (founder-direct, relayed via CoS)** — Reels
are the account's only surface actually getting reach (0-2 on carousels
vs 39-430 on Reels, insights-verified), so cadence shifts further toward
Reels. This file is the complete, self-contained instruction for one
scheduled daily run. Hand it to the scheduler verbatim. Intended trigger:
**02:25 IST daily** (siblings stagger: hype_tingles 02:00, nuvarel
02:50 — do not change your own slot without changing theirs).

**First eligible target date under this cadence: 2026-09-07.** If
today's target date is before that, use the prior "1 carousel + 2 Reels"
shape instead.

**Creativity-over-formula rule (founder-direct, 2026-09-06 — read this
before Step 4):** the founder's own words: "I want creativity, not
repetitiveness in the immediate next posts." The CCO's 2026-09-05 audit
(`income-engine/docs/consults/2026-09-05-cco-anime-ekaya-brand-strategy.md`)
found the account's actual defect wasn't topic repetition (the
topic-level ledger below already catches that) — it was **mechanic**
repetition: five documented "pillars" collapsed to three interchangeable
renderer shapes, indistinguishable at feed scale. Naming the
`reel-show-converter` bridge format as a daily slot (Step 4 below) is
useful because it's proven, but treating it as an automatic daily fill
would recreate the exact same defect with a new label. **Build it only
when it's genuinely the sharpest, freshest idea available that day —
never as a default to avoid thinking of something better.**

## Who you are building for

Account: `anime_ekaya` — an anime *curation* page ("what to watch next,
answered fast"). Full strategy:
`income-engine/docs/anime_ekaya-strategy.md` (legal lane §2, pillars §3,
hooks/captions §4-5, visual identity "Midnight Channel" §8). Working
ledger: `accounts/anime_ekaya/content/used-topics.md`. Repo root:
`C:\Users\2026\Documents\income-engine\instagram-accounts-social` (moved
2026-09-12, was a sibling of `income-engine`) — all paths below
are relative to it. Work ONLY inside `accounts/anime_ekaya/`; never
touch the other accounts' directories.

**Standing hard rule (strategy §2, non-negotiable):** no studio art, no
screencaps, no manga panels, no character-likeness illustrations, no
clips, no official key-art, ever — credit is not a license. Every pixel
is our own typographic/graphic design. Titles, factual metadata, and our
own opinions only. (Reconfirmed 2026-09-06, Group Legal/Compliance
consult on clip-commentary formats: no real licensing channel exists at
this account's scale, and fair-use/fair-dealing framing does not protect
against Instagram's own enforcement — see
`income-engine/docs/consults/2026-09-06-group-legal-anime-clip-commentary-fair-use.md`.
This rule stays in force regardless of format cadence.)

## Step 0 — read the gates before anything else

Read `accounts/anime_ekaya/docs/build-gates.json`. As of 2026-09-06 (Group
CTO update):

- `carousel_video_slides` **closed** — the code side is done: the shared
  publisher (`scripts/publish_due_posts.py`) now accepts a mixed
  `slides` array (`{"type": "image"|"video", "src": "..."}` entries
  alongside plain image-path strings) and sends the right Graph API
  params for each child, unit-tested (`tests/test_publish_mixed_carousel.py`).
  It is still closed because nobody has actually published one live
  end-to-end yet — that verification needs real credentials and a real
  (public, irreversible) post, so it's a CoS/founder-gated step, not
  something the daily build does on its own. **Until this gate flips to
  open, every carousel you build is still a static-image carousel** — do
  not hand-construct a `"type": "video"` slide entry in a real queued
  post; the gate's own `note` field has the exact reopening procedure if
  you want to check status.

## Step 0A — plan the day, and read yesterday, before anything else

**Group CTO, 2026-09-12, founder-direct.** Canonical rule and the evidence
behind it: `docs/cadence-and-format-policy.md`. Run these two commands before
you think about topics. Neither needs a token and neither calls the API.

```
py -3 scripts/collect_insights.py --rollup-only
py -3 scripts/plan_day.py --account anime_ekaya
```

1. **`plan_day.py` decides how many pieces, which format each is, and what
   time each posts.** Build exactly the slots it returns. It enforces the
   founder's **3 posts a day, every day, until 50,000 followers** floor,
   recomputes the FEED/REELS mix daily from the trailing 21 days of real
   performance, and draws each slot's minute from inside a window so the
   account never posts at identical clock times two days running. You do not
   choose the count, the mix or the times. If you believe the plan is wrong,
   build it anyway and say why in your final report and the commit message.
2. **Read yesterday and the trailing 7 days on this account** from the rollup:
   which piece reached most and least, which `type` each was, and whether the
   format the planner assigned agrees with that. **Write two lines into your
   commit message** naming what you learned and what you changed because of
   it. "Nothing changed" is fine once; three days running is an escalation to
   `growth-analyst`.

Measured 2026-09-12 on this account: Reels mean reach **191.3** (n=9),
carousels **1.7** (n=11). A 110x gap. That is why the mix is computed and no
longer fixed.

**Strategy content on this account is under active review by the portfolio
Chief Creative Officer (dispatch 2026-09-12).** This section changes cadence,
timing, format mix, hooks and CTAs only. Pillars, voice and premise are
unchanged until CCO's direction lands and `creative-director` applies it.

## Your job today (one run)

Build and queue **the 3 slots `plan_day.py` returned in Step 0A** for today's
date (the date the run starts, IST), each on a different topic, trend-sourced
where possible. The fixed "1 carousel + 3 Reels" cadence from 2026-09-06 is
retired — the count is now 3 and the mix is computed.

Everything queues at `needs_review: true` — **you never flip it.** Under the
founder's 2026-09-12 ruling (`CLAUDE.md` hard rule 1) the founder-approval step
is replaced below 10,000 followers by an auto-clear, but the clear is applied by
the **dispatching session** after `content-reviewer` and `creative-director`
both PASS, never by you. The builder and the clearer are never the same actor.

**Carousel format variety (new 2026-09-06):** while `carousel_video_slides`
stays closed, vary the carousel's *visual density* instead of pretending
it's animated — alternate between a **dense multi-slide list carousel**
(the existing FAN VOTE/list format, 6-8 slides) and a **single strong
image carousel** (2-3 slides: one bold statement slide, one full-bleed
mood/visual slide, one save-CTA slide — closer to a single-image post
than a list). Don't run the same carousel shape two days running; check
`used-topics.md`'s format cell before picking. Once `carousel_video_slides`
opens, a third option (a short video-loop slide mixed with image slides,
built the same way a Reel's video is — via `scripts/render_reel.py`'s
HTML/Playwright frame-capture path, just shorter and without needing the
full Reel skill's beat structure) becomes available — don't build it
before then.

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

### Step 1b — in-app trend research — NOT LIVE, DO NOT RUN

Specified in `docs/trend-research-step-spec.md` and **blocked on a Chief
Security Officer review of the cookie-based browser session** (founder: the
security check is mandatory). Skip this step entirely; do not open a browser
session, do not look for a cookie file. When it unblocks it is a **soft**
dependency and its failure will never block a build. Until then Step 1's
`WebSearch` is the whole trend input.

### Step 2 — anti-repetition check (topic AND mechanic — both, not just topic)

Read `accounts/anime_ekaya/content/used-topics.md`. Topic-level rules: a
specific show can headline again after 21 days; a mood can repeat after
30 days; a take never repeats (sequels only). Skip any candidate that
violates these.

**Mechanic-level rule (added 2026-09-06, per the CCO's own diagnosis of
this account's actual defect — this is the check that was missing, not
an extra formality):** classify every post you're about to build into
one mechanic class before queueing it: **list/ranking** (multiple items
named in sequence, e.g. MOOD MATCH, FAN VOTE), **single-declaration**
(one opinion, one show, no list — HOT TAKE, THE PICK-style), **bridge/
comparison** (map one known thing to an unknown thing — `reel-show-converter`),
**game/quiz** (the viewer scores or guesses something — DIAGNOSTIC,
future blind-rank formats), **character moment** (EKAYA reacting/
performing, not listing). Look at the last 5 posted-or-queued pieces
(check both `used-topics.md` and today's own queue as you build it): **no
two consecutive posts — including across the carousel/Reel boundary —
may share a mechanic class**, and **no mechanic class may exceed 2 of
today's 4 posts**. If your planned lineup fails this check, swap one
piece's mechanic before building, not after — this is a planning gate,
not a post-hoc note.

**Scene/prop rule (Reels, added 2026-08-31 after a real near-duplicate
on a sibling account):** the EKAYA mascot + Midnight Channel backdrop is
a fixed rendered environment, so two Reels can carry different lists and
still look identical at thumbnail scale. Before building each Reel, look
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
trend day. A quiet trend day is not license to default to the easiest
mechanic — the fallback space is large enough to still satisfy Step 2's
mechanic-variety gate.

### Step 4 — pick 4 topics

Day shape (revised 2026-09-06, tightened same day per the
creativity-over-formula rule above): the timely piece (FAN VOTE on its
weekly data drop, otherwise a this-season list) is the day's
**carousel** — ranking/list data still reads better as a carousel than a
Reel, and carousels stay in rotation for that reason even though they
don't carry reach. For the **three Reels**, choose three *different*
mechanic classes (per Step 2) — do not reach for MOOD MATCH + GATEWAY +
bridge as a fixed trio out of habit. The `reel-show-converter` bridge
format (proven: `2026-09-04-show-converter`, "Anime for beginners" — 430
reach, 542 views, 4 shares, by far the account's best result) earns a
slot only when a genuinely fitting, non-forced non-anime comparison
exists that day — a strained bridge is worse than a strong entry in a
different mechanic class. Four distinct topics, no overlap with each
other or with anything already in `accounts/anime_ekaya/content/queue/`.

### Step 5 — build

**Carousel (1):** deck JSON in `accounts/anime_ekaya/tools/decks/`,
rendered via `py -3 accounts/anime_ekaya/tools/render.py` (Midnight
Channel brand system — tokens only, no new colors/fonts; EKAYA エカヤ
wordmark). Pick the dense-list or single-strong-image shape per the
variety rule above. 1080x1350 PNGs go to
`accounts/anime_ekaya/content/queue/slides/`. Eyeball every slide at
feed scale (~350px) before queueing.

**Reels (3):** load the skill at
`.claude/skills/meme-worthy-character-reels/` and follow it for EACH
Reel — it is the process, including its frame-level human review of
every rendered mp4 (a passing ffmpeg check is not a review). Render via
`py -3 scripts/render_reel.py <reel.html> --out <out.mp4> --audio <spec.json>`,
rig helpers at `assets/rig2d.js`, EKAYA mascot (own design,
lane-compliant — never a recognizable existing character). Tone ruling
for this account: energetic but not slapstick, 20-22s each. Music is
mandatory on all three (free Pixabay/Mixkit track, use a different track
for each); log each license in `assets/audio/ATTRIBUTION.md` in that
file's existing format, keep raw audio files LOCAL-ONLY (never commit
them — public repo; each rendered mp4 with mixed audio is committed).
Final mp4s go to `accounts/anime_ekaya/content/queue/video/`.
**Same-day scene/prop check:** all three Reels must not share the same
backdrop/scene-set + hero-prop combination with EACH OTHER, not just
against history — apply the 14-day rule above pairwise across all three
before queueing any of them.

**Reel quality ratchet (standing, added 2026-09-02 — founder wants the
Reels kept improving, not just repeated):** before building, open the
last 3 live or queued Reels for this account and pick ONE concrete
thing to make better in today's builds — mascot rig/motion fluidity,
comedic/emotional timing, hook-frame strength (the first 1 second),
audio mix/sync, backdrop polish, or list-pacing clarity. Actually
implement the improvement, don't just note it; name the dimension and
what changed in the commit message. The bar each day is "better than
last time" on at least one axis, not "as good as last time."

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
  "id": "2026-09-07-example-slug",
  "type": "<format-slug>",
  "goal": "share",
  "caption": "...",
  "slides": ["accounts/anime_ekaya/content/queue/slides/<id>-1.png", "..."],
  "scheduled_time_ist": "<paste from plan_day.py --json>",
  "status": "pending",
  "attempts": 0,
  "needs_review": true
}
```

**`goal` is required on every piece (added 2026-09-12).** One of `save`,
`share`, `comment`, `dm`, `mood`, `entertain`. Chosen when the topic is chosen,
never retro-fitted. It decides whether the piece gets a CTA — see the hook/CTA
rule below. **`scheduled_time_ist` comes from `plan_day.py`, verbatim** — do
not invent a time, do not round the minute, do not reuse yesterday's.

Reels use `"video": "accounts/anime_ekaya/content/queue/video/<id>.mp4"`
instead of `"slides"`.

**Mixed video+image carousel schema (added 2026-09-06, DO NOT USE until
`carousel_video_slides` flips to open — see Step 0):** once open, a
`slides` entry may be `{"type": "image", "src": "<path>"}` or
`{"type": "video", "src": "<path>"}` instead of a bare string; the two
forms may mix freely in one array. Build the video slide's clip with
`py -3 scripts/render_reel.py <loop.html> --out <out.mp4>` (a short 3-5s
seek(t) loop, no `--audio` needed for a silent background loop) — reuse
this renderer, do not write a second one.

**Type whitelist (added 2026-09-01, Group CTO — three undocumented
pillar values had slipped into the queue by then):** `type` MUST be one
of `mood-match`, `fan-vote`, `gateway-guide`, `hot-take`,
`seasonal-preview`, `diagnostic`, or the same list with a `reel-`
prefix, plus `reel-relatable-action` and `reel-show-converter` (the
"bridge a famous non-anime show" mechanic, named 2026-09-06 after
`show-converter`'s breakout result — see Step 4). These are exactly the
pillars documented in strategy §3 plus this one addition. If the piece
you built doesn't fit any of them, STOP: do not invent a new type value —
either reshape the piece into a documented pillar, or queue it under the
closest documented pillar and flag the proposed new pillar in the commit
message for a strategy-doc decision. **Note the mechanic class (Step 2)
in the commit message for each piece, alongside the type** — this is
what makes the mechanic-variety rule auditable by whoever reviews the
batch, since `type` alone doesn't reveal it (e.g. `diagnostic` could be
a quiz or a listicle depending on execution).

**Slots (replaced 2026-09-12 — there is no standing slot table any more).**
`plan_day.py` (Step 0A) returns today's 3 slots, each with a format and a
`scheduled_time_ist` drawn from inside a window. The fixed
10:00/13:00/19:30/22:30 table is retired. Windows live in
`docs/slot-policy.json`; edit that file, never this prompt, to move a window.

**Slot-occupancy rule (tightened 2026-09-01, Group CTO, still binding):**
before building anything, list the target date's existing queue items. A slot
already occupied by an existing queue item is COVERED — do not build a piece
for it. Build only for the planner's slots that are empty on the target date;
if all three are occupied, stop and do nothing (the day is fully covered by an
earlier batch). Never shift-and-double. Match an existing item to a planner slot
by nearest time, not by exact string.

**A closed lane does not reduce the day below 3 posts.** If a slot's assigned
format cannot be built, build the other open format for that slot; only if no
lane can fill it does the slot become a `BUILD-INCIDENT` entry naming the slot
and the reason.

### Hook and CTA rule (Group CTO, 2026-09-12, founder-direct)

Canonical: `docs/cadence-and-format-policy.md` §4. Operative here:

- **The hook is mandatory on every piece.** Frame 1 / second 1 opens a
  curiosity gap and never states the verdict or names the format. ≤ 7 words.
- **The CTA is conditional, and forcing one onto every post is now a defect**
  (founder, 2026-09-12: it looks forced). By the piece's `goal`:

  | `goal` | CTA | Shape |
  |---|---|---|
  | `save` | required | future utility, phrased for the viewer |
  | `share` | required | names the person, not the action |
  | `comment` | required | one answerable question, never "thoughts?" |
  | `dm` | required | keyword-comment mechanic only; names the keyword |
  | `mood` | **forbidden** | ends on the image |
  | `entertain` | **forbidden** | the punchline is the ending; a CTA kills it |

- **At most 2 of today's 3 pieces carry a CTA.** At least one is `mood` or
  `entertain` and ends clean. On a comedy account this matters more, not less.
- **The same CTA verb appears at most 3 times in any 7 days** — check the
  ledger.
- A CTA never appears on frame 1, and never twice in one piece.

### Step 8 — update the ledger

Append one row per queued post to
`accounts/anime_ekaya/content/used-topics.md` (existing table format:
date, post, format, mood/topic, shows featured). The format cell MUST
start with the exact `type` value from the queue JSON, verbatim
(parenthetical notes after it are fine) — a ledger filed under one
vocabulary while the queue uses another produced a real
anti-repetition false clear on a sibling account (2026-08-31). **Also
add the mechanic class (Step 2) in parentheses after the format cell**
so the next run's Step 2 check doesn't have to re-derive it from
memory — e.g. `mood-match (list/ranking)` or `reel-show-converter
(bridge/comparison)`.

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
3. `git commit accounts/anime_ekaya/ assets/audio/ATTRIBUTION.md -m "feat(anime_ekaya): daily 4x batch <date> (1 carousel + 3 Reels, needs_review)"`
   — pathspec on the commit itself, not only on the add.
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
three.

## Definition of done

Queue JSONs for all 3 planner slots today at `needs_review: true`, each with a
`goal` and each with its `scheduled_time_ist` taken verbatim from
`plan_day.py`, rendered assets
committed, ledger updated (topic AND mechanic class), copydesk clean,
pushed to `master` with the safety sequence above, **and your final
message lists every piece built (queue JSON path, rendered asset path,
slot) so it can be reviewed.**

**Your push is not the end of the batch.** The batch is done only after
the independent review gate (added 2026-09-12, Group CTO): the session
that dispatched you convenes `content-reviewer` on the pushed commit —
never the agent that built the piece — and it issues PASS/FAIL per piece
on defects; `creative-director` then rules on brand fit for the pieces
that passed. A FAIL comes back to you as a fix round (rounds 1-3 same
builder, round 4 escalates to `cto`, round 5 is a hard stop). A piece
still FAILed when the fix rounds run out is moved from `content/queue/`
to `accounts/anime_ekaya/content/qa-hold/` (outside the publisher's
scan; never `content/failed/`, which is the publisher's own state).

**A defect-free piece can still be killed (2026-09-12).** `content-reviewer`
now applies a quality floor as well as a defect list: a piece nobody can name a
reason to forward is a FAIL with reason `weak-concept`. The 3-a-day floor is not
a licence to ship filler — a killed slot is a `BUILD-INCIDENT`, and three
incidents in one week escalate to `cto`.

**Clearing for publish (changed 2026-09-12, founder ruling).** Once both
verdicts are PASS, the **dispatching session** sets `needs_review: false` and
commits, naming both verdicts in the message. This account is far below 10,000
followers, so no founder approval step runs (`CLAUDE.md` hard rule 1); the
founder reviews on Instagram after publish. You still never flip the flag
yourself.
