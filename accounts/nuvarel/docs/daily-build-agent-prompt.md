# nuvarel — daily build agent (standing prompt)

Authored by Group CTO 2026-08-31 for the 3x/day cadence; **rewritten by
Group CTO 2026-09-05** against the founder-direct strategy revision of the
same day (`docs/nuvarel-strategy.md`, revision header 2026-09-05: §1/§3/§7/§8
superseded; the CoS's hook & genre-matching rule in §2). This file is the
complete, self-contained instruction for one scheduled daily run. Hand it to
the scheduler verbatim. Intended trigger: **02:53 IST daily** (siblings
stagger: hype_tingles 02:03, anime_ekaya 02:28 — do not change your own slot
without changing theirs).

**First eligible target date under this version: 2026-09-06.** If today's
target date is earlier, stop and do nothing.

## Step 0 — read the gates before anything else

Read `accounts/nuvarel/docs/build-gates.json`. It names which production
lanes are open tonight and why. As written on 2026-09-05:

- `photo_carousel` **open** (keys `dark`, `mid`; `light` experimental).
- `photo_reel` **closed** — no Reel is built until it opens.
- `inspection_hands` **closed** — no hands in any frame.
- `typography_only` **closed** — never fall back to text-only cards.
- `character_rig` **retired** — `assets/rig2d.js` is never used here again.

Build only for open lanes. A closed lane is skipped silently and named in
the commit message (e.g. `Reel slot skipped: photo_reel gate closed`). It is
not a failure and not an incident. If every lane you would build for is
closed or covered (Step 7), stop: no commit, no incident, print why.

## Who you are building for

Account: `nuvarel_`. Positioning (strategy §1): **"The proof, not the
claim."** Nuvarel shows the physical evidence that separates an expensive
object from a cheap one — the knot, the grain, the joint, the weave, the
weight — so the viewer can tell the difference themselves in any showroom.
Audience: English-speaking, 28-45, 6-24 months after buying/renovating/
relocating into a home they intend to keep, mid-purchase-decision. Their
question is "which of these do I actually buy, and is the expensive one
worth it," not "what's pretty."

Full strategy: `docs/nuvarel-strategy.md` (pillars §3, hooks/captions §4,
hashtags §5, posting times §6, cadence §7, visual identity §8). Working
ledger: `accounts/nuvarel/content/used-topics.md`. Repo root:
`C:\Users\2026\Documents\instagram-accounts-social` — all paths below are
relative to it. Work ONLY inside `accounts/nuvarel/`; never touch the other
accounts' directories.

**Voice guardrails:** knowing, calm, specific. Never preachy, never
"hacks!!", never mocking cheap things (the reader may own them) — "reads
expensive," never "stop being tacky." **Not budget-facing:** no
"outlive three flats," no "skip the trend colour," no rationing language;
the reader is deciding between price tiers, not saving up. Every verdict
includes a real "no" somewhere in the rotation — an account that says the
expensive one is always worth it smells like a vendor. Drop `#quietluxury`
entirely (the label is in backlash; the materials are not).

**Hard visual constraints (strategy §8 + platform):** no people, no hands,
no faces, no silhouettes that read as a posed human — Instagram limits reach
on undisclosed AI-generated people; the object is the subject. Every
photoreal piece is published with Meta's AI self-disclosure (Step 7).

## Your job today (one run)

Build and queue **up to 2 posts for today's date** (the date the run
starts, IST): **1 carousel** (10:00 IST) **+ 1 Reel** (19:30 IST), subject
to the gates in Step 0 and slot occupancy in Step 7. Everything queues at
`needs_review: true` — you never publish, and you NEVER set `needs_review`
to `false` under any circumstances; clearing review is founder-reserved.

### Step 1 — trend search (2-3 queries)

Run these, substituting the current month/year:

1. WebSearch: `interior design material trends <Month> <Year>`
2. WebSearch: `furniture buying guide solid wood vs veneer <Year>` (or the
   equivalent for the material the rotation lands on: brass vs plated,
   linen vs poly blend, stone vs porcelain, leather grades)
3. WebSearch: `home decor colour trends <Year> chocolate brown natural
   stone matte` (or Firecrawl a current-month trends roundup from Elle
   Decor / House Beautiful / Homes & Gardens)

You want: a material, object or comparison you can translate into
*evidence* — a detail the camera can show that proves quality or its
absence. The account's product is the proof, not the trend: "bouclé is
everywhere" becomes "how to tell a dense bouclé from a loose one before you
sit on it."

### Step 2 — anti-repetition check

Read `accounts/nuvarel/content/used-topics.md`. Rules (strategy §3,
revised for 2/day): a topic/material/object never re-runs within 60 days;
no carousel pillar two days running; no Reel pillar two days running;
Palette Study gets a new named *material* every time; Insider Knowledge
sub-angles don't repeat within 30 days; a Two Objects pair is never
reused; **scene/prop rule (now applies to photography too):** two posts in
the same 7 days must not share the same staged setup (same object family on
the same surface under the same key) even if the lesson differs.

**Vocabulary rule (standing since 2026-08-31):** the ledger's Format column
and the queue JSON's `type` field are ONE vocabulary. Current slugs —
carousels: `the-evidence`, `two-objects`, `the-room`, `palette-study`,
`insider`, `mood`; Reels: `reel-satisfying`, `reel-reveal`, `reel-game`,
`reel-trend`. Older slugs in the ledger (`reads-expensive`, `splurge-skip`,
`the-rule`, `reel-*` variants) are history and still count for the 60-day
topic check. Check candidates against the ledger's *topic keywords*, not
just its Format column.

### Step 3 — fallback

If the trend search yields nothing usable, fall back to straight pillar
rotation with the next unused material/object: carousel order **The
Evidence → Two Objects → Palette Study → Insider Knowledge → Mood → (The
Room, see the hold below)**. Never block or skip the run for an empty
trend day.

### Step 4 — pick the day's topics

**Carousel:** one pillar from the carousel list, by rotation, bent toward
what the trend search gave you. Production notes per pillar (2026-09-05):

- `the-evidence` — one object, one macro detail. The spike validated exactly
  this shape (single object, one low warm light). Preferred while the
  pipeline is young.
- `two-objects` — the same object at two price points "photographed
  identically": generate both with the **same seed** and a prompt that
  differs only in the material words, so framing and light match. Four
  named differences, one honest verdict; the buyable item is named in the
  caption's second line. Watch sends-per-reach on these (strategy §2).
- `palette-study` — keep the "No. NN" series numbering (next is No. 04);
  the swatch is now a **photographed material** (stained oak, saddle
  leather, washed linen), not a hex block. Hex codes may still appear as
  a small eyebrow label, never as the image.
- `insider` — one sub-angle from §3.5 (Showroom Secrets, The 60-Second
  Inspection, Ages Well/Ages Badly, The One Swap, Real Cost Breakdown,
  Where It's Made, Care Secrets); object macro + short text slides.
  The 60-Second Inspection stays object-only (no hands) while
  `inspection_hands` is closed.
- `mood` — texture/atmosphere or a plausible imagined object, no lesson.
  Frame 1 stays the object alone.
- `the-room` — **on hold** until one full-room generation passes the gate
  and an eyes-on review: the spike validated single objects, not rooms.
  Skip it in rotation for now and say so in the commit message.

**Reel:** only if `photo_reel` is open (Step 0). When it opens: the
standing default is **Quick Games (`reel-game`) first, three of them**
(guess-then-reveal works as a cut sequence of photoreal stills, needs no
character and no video generation), then rotate `reel-satisfying` /
`reel-reveal` / `reel-trend`. Two concepts are pre-drafted and copydesk-
clean in strategy §3 pillars 7-8: **"The Grain Underneath"** (sanding
reveal, no hands needed if framed as the block moving across the board) is
first in line among them; **"The Recovery Test"** as written needs the
Inspection device and stays behind `inspection_hands` — a hands-free
reframe (two cushions, a small weight lifted off one, the recovery is the
reveal) is acceptable if you can produce it without a hand in frame. Both
are *motion* pieces and therefore also wait on photoreal video being
proven; the Quick Games stills path is what opens the lane first.

### Step 5 — build the carousel

**5a. Tonal key.** The grid rotates value key across consecutive posts
(strategy §8). Read the last carousel's key from the ledger's scene cell
and take the next one in the cycle **mid → dark → mid → dark** while
`light` is experimental. Mechanically: **full-bleed layout on a dark-key
generation reads as `dark`; matted layout (alabaster mat) around the same
photo reads as `mid`** (spike: 0.15-0.17 vs 0.50 mean luminance). The first
time you attempt `light`, generate with `--key light`, and if the deck
passes the gate and looks right at 350 px, record it in
`build-gates.json` (`light_key`) so the rotation can become
light → mid → dark.

**5b. Generate photographs.** ComfyUI must be up on `127.0.0.1:8188`:

```
curl -s -m 5 http://127.0.0.1:8188/system_stats >/dev/null && echo up || echo down
```

If down: run `nvidia-smi --query-gpu=memory.used --format=csv,noheader`.
If a peer holds more than ~8 GB, wait up to 20 minutes (re-check every 5)
and, still busy, skip the carousel with a `BUILD-INCIDENT.json` entry
(stage `gpu-busy`). Otherwise start the server (it takes ~60-90 s to
answer):

```
cd "C:\Users\2026\Documents\income-engine\video_lab\samples\comfyui-mcp\ComfyUI" && ..\.venv\Scripts\python.exe main.py --port 8188
```

(run it in the background; if you started it, stop that process by PID
after the build — peers share this GPU.) Then, per distinct shot:

```
py -3 accounts/nuvarel/render/gen_photo.py --subject "<object, material, surface — one sentence>" --key dark|mid --n 3 --out accounts/nuvarel/render/photos/<post-id>/<shot-slug>
```

~35 s/frame, 1088x1360 (measured 2026-09-05: 2 frames in 68 s with a
peer already holding 10.7 GB of the GPU). Plan 2-3 distinct shots per deck
(hook object, the macro detail, the comparison object), 3 candidates each;
more than ~10 frames a night is waste. Subjects follow §8 verbatim: one
object, one low warm light, matte, desaturated, nothing else in frame.
Name the material precisely ("saddle-tan vegetable-tanned leather," not
"leather"). Wood subjects get an automatic grain phrase — still check them.

**5c. Eyes-on pick (mandatory — the gate cannot see this class).** Open
every candidate PNG and look. Reject: a shadow detached from its object or
falling off-frame the wrong way; warped/fused geometry; any text, logo or
watermark; gloss/mirror reflections; any hand, person or human silhouette;
wood grain that reads as printed laminate when viewed at full size.
**Material fidelity:** the model substitutes a more common material for a
rarer one without telling you (2026-09-05 smoke test: "honed travertine"
came back as veined white marble; the light also drifted to upper-left).
An account whose claim is "the proof" cannot caption marble as travertine
— either the named material is visibly what's in the frame, or you rename
the caption to what is actually shown, or you reject the frame. Roughly
1 in 3 frames fails this step; if all 3 fail, re-run with a new `--seed`.
Note the picked file and seed for the ledger.

**5d. Deck.** Deck JSON in `accounts/nuvarel/render/decks/<post-id>.json`.
Shape, 5-7 slides:

1. `photo` — the hook. Full-bleed (dark) or matted (mid) per 5a.
   `"h"` is **≤ 7 words and opens a curiosity gap, never states the
   verdict** (strategy §2: "The cheapest thing in an expensive room" beat
   "Splurge or skip: the bathroom" with identical craft). `"eyebrow"` is
   the series line (`The Evidence · No. 02`). Optional `"index"`: the
   Nuvarel Index score (0-100) — include it only if the caption's second
   line can justify it in four parts (weight, material, finish, how it
   ages), otherwise leave it out; a number nobody can reproduce is noise.
2. `photo` with `"silent": true` — the photograph alone, no type. Every
   deck. No exceptions.
3-5. The evidence: `photo` slides with ≤ 7-word headlines for what the
   camera shows; `principle` (text) slides only where the point genuinely
   needs a sentence (a Two Objects difference, an Insider tip).
6. `closer` — the save CTA phrased as utility ("Save this for the next
   showroom").

Photo `src` paths are repo-relative (`accounts/nuvarel/render/photos/...`).

**5e. Render + gate.**

```
py -3 accounts/nuvarel/render/render_nuvarel.py accounts/nuvarel/render/decks/<post-id>.json
py -3 accounts/nuvarel/render/gate_check.py accounts/nuvarel/render/out/<post-id>
```

The gate now checks photo slides for declared key vs measured luminance,
type ≤ 15 % of frame, ≤ 7 headline words, silent slide 2. A FAIL is fixed,
not argued with. Then open every file in `out/<post-id>/_preview350/` and
look at the deck at feed scale — that is the review; the numbers are not.
Copy the 1080x1350 PNGs to `accounts/nuvarel/content/queue/slides/<post-id>-N.png`.

### Step 6 — copydesk gate (mandatory)

Every caption AND every on-screen text line passes
`py -3 -m copydesk --caption <file>` run from
`C:\Users\2026\Documents\income-engine\copydesk` (write the lines to a
temp .txt first). Fix and re-run until clean. Canonical ruleset:
`income-engine/copydesk/copydesk/rules.py`. Captions follow strategy §4:
keyword-rich opening line, 2-4 lines of real substance, a save CTA
phrased as utility, 3-5 hashtags from the §5 pool **minus `#quietluxury`**.

### Step 7 — queue

One JSON per post in `accounts/nuvarel/content/queue/`, id format
`YYYY-MM-DD-<slug>`. Schema (carousel):

```json
{
  "id": "2026-09-06-example-slug",
  "type": "<pillar-slug>",
  "caption": "...",
  "slides": ["accounts/nuvarel/content/queue/slides/<id>-1.png", "..."],
  "scheduled_time_ist": "2026-09-06T10:00:00+05:30",
  "status": "pending",
  "attempts": 0,
  "needs_review": true,
  "ai_generated": true,
  "tonal_key": "dark"
}
```

`"ai_generated": true` is **mandatory on every piece containing generated
imagery** — the publisher turns it into Meta's `is_ai_generated=true`
self-disclosure on the container (Group Legal, 2026-09-05: disclosure on
AI photoreal video is a platform duty; on stills it is the honest default
for an account whose whole claim is "the proof"). Reels use
`"video": "accounts/nuvarel/content/queue/video/<id>.mp4"` instead of
`"slides"`.

**Standing slots (IST), strategy §6/§7, 2/day from 2026-09-06:**
- **10:00** — **carousel** (decor-specific morning-at-home window).
- **19:30** — **Reel** (all-India evening peak; Reels carry the
  non-follower reach, so they take the best slot).
- The old 13:30 slot is retired. Do not build for it.

**Slot-occupancy rule (Group CTO, 2026-09-01):** before building anything,
list the target date's existing queue items. A standing slot already
occupied by an existing queue item is COVERED — do not build a piece for
it. Build only for the standing slots that are empty on the target date
*and* whose lane is open; if nothing is both empty and open, stop and do
nothing. Never shift-and-double. If a genuine timing conflict arises for a
slot you ARE building, shift +30 minutes and note it in the commit
message; the publish cron is hourly, so the next top-of-hour still lands.

### Step 8 — update the ledger

Append one row per queued post to
`accounts/nuvarel/content/used-topics.md` (existing table format: date,
post, format, topic keywords, scene-set + props). The Format cell is the
exact `type` value you wrote in the queue JSON — copy it verbatim. The
topic cell lists every searchable keyword (object, material, comparison
pair, sub-angle). The scene cell now records, for photographic pieces:
`photo: <subject/surface> · key=<dark|mid|light> · seed=<n>` — this is
what the 7-day setup check and the tonal rotation read next time.

### Step 9 — commit (shared-repo git safety, non-negotiable)

This repo has multiple concurrent sessions. Exactly this sequence, each
git command its own separate invocation — NEVER chained with `&&`/`;`:

1. `git add accounts/nuvarel/ assets/audio/ATTRIBUTION.md` — scoped
   pathspec only; never `git add -A`, never a bare `git add .`. Raw
   candidate photographs are gitignored (`render/.gitignore`); the
   `gen-<seed>.json` beside them is committed so a frame can be
   regenerated.
2. `git diff --cached --name-only` — as its own command. Actually read
   the output: every listed file must be yours and inside
   `accounts/nuvarel/` (plus at most the ATTRIBUTION.md line you
   added). If anything else is staged, unstage it and investigate
   before proceeding.
3. `git commit accounts/nuvarel/ assets/audio/ATTRIBUTION.md -m "feat(nuvarel): daily batch <date> (<what was built>, needs_review)"`
   — pathspec on the commit itself, not only on the add. Name any
   skipped lane and any pillar hold in the message.
4. Push with the race-retry loop (same pattern as `publish-*.yml`):
   `git push`; on rejection, `git pull --rebase`, wait 1-5s, retry, up
   to 5 times.

## Failure handling

If the carousel fails to build (generation error, all candidates rejected
twice, gate FAIL you cannot fix, GPU busy past the wait): **skip it** and
log the failure to `accounts/nuvarel/content/BUILD-INCIDENT.json`
(`{"ts": "<iso>", "stage": "...", "error": "..."}` appended to a list).
**Never substitute a typography-only card** — a missed carousel costs
nothing measurable (31 typography carousels reached 0-8 people each); a
retired-format post contradicts a founder decision. Do NOT write to
`content/INCIDENT.json` — that file is the publish workflow's token-health
throttle and has load-bearing semantics for `scripts/check_token.py`. If
you started ComfyUI, stop it even on failure.

## Definition of done

Queue JSONs for every open, uncovered slot today at `needs_review: true`
with `ai_generated: true`, rendered assets committed, ledger updated,
copydesk clean, gate PASS with the previews actually looked at, pushed to
`master` with the safety sequence above, ComfyUI left in the state you
found it. No founder ping needed — the founder reviews the morning batch
through the normal daily review flow.
