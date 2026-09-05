# Nuvarel — growth strategy and content spec

**Account:** `nuvarel_` (Instagram, dormant, being revived)
**Written:** 2026-08-30, overnight autonomous session (founder-delegated)
**Revised:** 2026-09-05, founder-direct strategy conversation (CoS + CCO consult
`income-engine/docs/consults/2026-09-05-cco-nuvarel-brand-strategy.md`) —
supersedes §1, §3, §7, §8 below. §2 (algorithm reality), §4-6 (hooks/hashtags/
posting times) remain valid and are kept as-is except where noted.

**Why this revision exists:** the founder reviewed the account directly and
said (paraphrased): "just mentioning rich in text doesn't make it look rich"
— the account was teaching quiet-luxury *principles* in text/diagram form but
never actually showing anything that reads as rich. CCO's audit found the
root cause: the "Curator" character was never a bespoke asset — it's
`assets/rig2d.js`, the same shared stickman rig `hype_tingles` uses for meme
jokes (including a `sitFlop`/`eyes:"dead"` pose). A stick figure with no
material, light or weight cannot signify wealth, no matter what the caption
says. Full reasoning, comparable accounts, and the dissent on audience
targeting: see the CCO consult linked above.

**Second revision, same day:** the founder separately noticed real audience
reaction on the (still-live-at-the-time) stickman Reels and asked whether a
character could be kept. CCO and Group CTO gave genuinely conflicting
advice — CTO: redesign it into a distinct figure, it's currently nuvarel's
only *proven* Reel pipeline (photoreal Reels are unproven, ~2h GPU/clip,
unlike the now-validated photoreal *stills*); CCO: retire the figure
entirely, replace with hands-only demonstration ("The Inspection," §3), on
the theory that a cartoon face trains Instagram's early-distribution
algorithm to seed the account to the wrong audience while it's still small.
**Founder decision: CCO's case.** No character/mascot on this account,
redesigned or otherwise. See §3's Reel pillars and "The Inspection" device
below for what replaces it.

---

## 1. The chosen angle (revised 2026-09-05)

**Nuvarel shows the physical evidence that separates an expensive object
from a cheap one — the knot, the grain, the joint, the weave, the weight —
so the viewer can tell the difference themselves, in any showroom, in any
country.**

One line: *"The proof, not the claim."*

### Audience (revised — see CCO dissent before treating this as settled)

Not "rich people globally" — actually wealthy people hire designers and
don't consume this content. The real, reachable, buyable audience:
**English-speaking, 28-45, in the 6-24 month window after buying,
renovating or relocating into a home they intend to keep.** Already follows
at least one designer account. Past inspiration, into decision. Their live
question isn't "what's pretty" — it's "which of these four do I actually
buy, and is the expensive one worth it." Geography: US/UK/UAE/Singapore/
Australia plus metro India; not trade, retail buyers who can be sold to.

**Founder should know:** CCO dissents that this reachable definition and
"rich audience across the globe" (the original brief) may not fully
overlap — flagged directly rather than buried. This doc is written for the
reachable version because it's also the better business.

### What changed and why

| Old (2026-08-30) | New (2026-09-05) | Why |
|---|---|---|
| Teach quiet-luxury *principles* via text/diagram carousels | Show physical *evidence* of quality via photoreal imagery | Diagrams and hex-color blocks cannot signal wealth; every real comparable account (Studio McGee, Becki Owens, Alyssa Kapito) is photographic |
| "Aspirational-but-not-rich" viewer, budget-conscious voice | High-intent buyer mid-purchase-decision | The founder's brief moved; the old audience was explicitly *budget*-facing ("outlive three flats," "skip the trend colour") |
| Illustrated Curator character (shared `rig2d.js` stickman) | No character — the object is the subject | The character was never bespoke; it actively borrowed a meme account's visual register |
| 3 posts/day (2 carousel + 1 Reel) | **2 posts/day** (1 carousel + 1 Reel), reduce further once followers grow | Founder decision 2026-09-05. Alyssa Kapito reached 240k on 264 *total* posts — volume is a downmarket signal in this category, and the ledger already showed 3 near-duplicate withdrawals in one week at 3x/day |
| `#quietluxury` as a core hashtag | Drop the phrase, keep the substance | 1stDibs' 2026 Designer Trends Survey: maximalism (39%) and eclecticism (38%) now lead demand, quiet-luxury discourse in active backlash. The materials underneath (chocolate brown, natural stone, matte finishes) are NOT decaying — just the label |

---

## 2. Algorithm reality, 2026 (unchanged, still valid)

- Instagram's confirmed top ranking signals: **watch time, sends per
  reach (DM shares), likes per reach** — likes weakest of the three.
- **Saves outweigh likes**: a save signals "worth returning to."
- **Carousels are the save/reach vehicle**: ~1.7x the reach of static
  posts. 8-12 slides is the sweet spot for educational carousels.
- Distribution is staged: small test audience first, expansion only if
  early save/share/watch signals fire. Slide 1 (the hook) carries the post.

**New for this revision:** sends-per-reach is the specific metric to watch
for the Two Objects pillar (§3) — it's the intended proxy for "this
resolved a decision I was about to discuss with someone." No Insights
collection exists yet for this account (or any of the three); building one
is the single highest-priority open engineering item portfolio-wide.

---

## 3. Content pillars (revised 2026-09-05 — expanded from 4 to a full rotation)

**Structure:** every day = **1 carousel + 1 Reel** (see §7). Carousel
pillars and Reel pillars are separate lists — pick one from each per day,
rotating so no pillar repeats inside any 7-day window if avoidable.

### Carousel pillars

1. **The Evidence** (`the-evidence`) — one object, one macro photoreal
   detail that proves quality or its absence: the dovetail vs. the staple,
   solid brass vs. plated, book-matched veining vs. printed. Near-zero
   text; the photo does the work.
2. **Two Objects** (`two-objects`) — the same object at two price points,
   photographed identically, four named differences, one honest verdict
   on when the expensive one is (and isn't) worth it. This is the impulse
   engine — see §3.4 on why.
3. **The Room That Proves It** (`the-room`) — one photoreal room built
   around a single material decision, named in three words. No tips, no
   list. Pure desire, replaces the old inspo-diagram slides.
4. **Palette Study** (`palette-study`, kept, re-worked) — same series
   numbering as before ("No. 01, 02...") but the swatch is now a
   *photographed material* (real stained oak, real leather, real linen)
   instead of a flat hex-color rectangle. The account's best existing
   asset; keep the mechanic, fix the execution.
5. **Insider Knowledge** (`insider`, new — the "tips" angle) — a rotating
   set of sub-angles under one pillar so the ledger doesn't fragment:
   - *Showroom Secrets* — what salespeople don't volunteer (how to spot
     real wood veneer vs. laminate, genuine vs. fake leather)
   - *The 60-Second Inspection* — exactly what to check in person before
     buying a specific item (a sofa, a rug, a dining table)
   - *Ages Well / Ages Badly* — which materials improve with age (brass
     patina, real leather) vs. which just look worn (ties to §3.6 below)
   - *The One Swap* — one small, specific, buyable change that upgrades a
     room (a hardware swap, one lamp)
   - *Real Cost Breakdown* — an itemized "here's what a real ₹X room
     actually costs" — genuine numbers, high save rate
   - *Where It's Made* — real craftsmanship traditions (Italian marble,
     Kashmiri weaves, Japanese joinery) — this is the account's actual
     "global" angle, and a genuine differentiator vs. US-only comparables
   - *Care Secrets* — how to keep expensive materials looking expensive
     for decades
6. **Mood** (`mood`, new — pure vibe, no lesson) — texture and
   plausible-object photography with no caption payload beyond a feeling.
   Two registers (candid gesture shots moved out to The Inspection, §3.5
   below, per the 2026-09-05 character-question resolution — they're a
   demonstration, not decoration, and belong under Evidence/Inspection):
   - Plausible imagined objects: an unlabeled amber bottle catching
     window light, a stack of uncut-edge books with a wax seal, a
     decanter half-poured at golden hour
   - Pure texture/atmosphere: water beading on cold marble, linen creases
     in raking light, candlelight on dark wood at dusk

### Reel pillars

**Production reality, 2026-09-05:** the character/stickman is retired
(see the second revision note above) and full photoreal *video* is
unproven and expensive (~2h GPU/clip via the video_lab I2V chain — only
photoreal *stills* have been validated so far). Until a photoreal-Reel
workflow is proven by hand, **prioritize Quick Games** — its
guess-then-reveal structure works as a sequence of photoreal *stills*
with simple cuts/text overlay (the same mechanism as the now-validated
still pipeline), inherits the stickman's actual engagement function
(setup → tension → payoff) without needing a character or expensive
video generation, and converts a passive reaction into a comment, a
better seed-audience signal. Ship 3 Quick Games Reels before any other
Reel pillar gets production time.

7. **Satisfying Process** (`reel-satisfying`) — oddly-satisfying, no
   character needed: oil spreading on water, wax being poured and set,
   raw wood being sanded to reveal grain, ice melting on warm stone.
   Cheapest to produce well because the eye follows motion, not scene
   detail.
8. **Reveal / Transformation** (`reel-reveal`) — a dust sheet pulled off
   a covered piece, a plain box unwrapped to reveal something beautiful,
   a raw-material-to-finished-object fast-forward (thread to fabric, clay
   to vessel). Drama + payoff under 10 seconds.
9. **Quick Games** (`reel-game`) — comment-bait, genuinely fun: "which
   one's real" (two near-identical objects, guess before reveal), "guess
   the price," quick material-vs-material showdowns (sunlight test, water
   test) with a clear winner.
10. **Trend-Jack** (`reel-trend`) — whatever Reel audio/format is
    actually trending that week, applied to an object instead of a
    person (e.g. an "expectation vs. reality" trend applied to
    online-bought furniture vs. how it looks in person). Borrows the
    platform's own momentum; check what's live before building, don't
    invent from a stale list.

### Signature devices (not separate pillars — applied ACROSS the pillars above)

These are what make the account recognizably *itself* over time, the way
"the cat has spoken" works for hype_tingles. Apply them inside Evidence,
Two Objects, and Palette Study especially:

- **The Nuvarel Index** — a proprietary, consistent 0-100 score (weight,
  material, finish, how it ages) applied to objects shown. Built to be
  quoted back ("that's only a 60?!"). This is the one signature device to
  build first — cheapest, and it works inside every other pillar rather
  than needing its own content slot.
- **The Provenance Card** — auction-house visual language (letterspaced
  serif, a stamped number, a wax-seal mark) applied to ordinary objects.
  Borrow this treatment for Evidence and Two Objects hook cards.
- **A signature sound cue** — one consistent, clean sound (a clink or a
  thud) at the reveal moment of every Reel. Sonic branding; nobody else
  in this niche does it.
- **One Object, Aged** (later, v2) — a slow-burn format tracking one kind
  of object at day one / year one / year ten. Genuinely differentiated
  because it requires patience most accounts won't invest. Don't start
  until the core rotation above is running reliably — this is a
  numbered-series-shaped commitment, and the portfolio already has one
  unfulfilled "EP02" promise on file elsewhere as a cautionary example.
- **The Inspection** — founder decision 2026-09-05, resolving the
  character question below. Not a mascot: a recurring point of view.
  Hands only, performing the exact verb this account's positioning
  promises ("tell the difference yourself") — a thumb along a seam
  checking whether veneer wraps or stops, a panel tilted into raking
  light to expose a printed grain repeat, a cushion pressed and timed as
  it recovers, a corner lifted to feel hardwood vs. ply. Anchors: hands
  always enter from lower right, never centred; one plain dark unbranded
  cuff at the wrist, always (a shape/tone anchor a generator can hold
  consistent — not a ring or watch, which will drift across posts and a
  drifting signature is worse than none); one action, one take, no cuts;
  **never a face, never past the cuff, never two hands doing different
  things.** Applies inside The Evidence, Two Objects, and Insider
  Knowledge (esp. The 60-Second Inspection, Care Secrets, Ages Well/
  Ages Badly) on the carousel side, and Satisfying Process/Quick Games/
  Reveal on the Reel side. **Never** on a carousel's frame 1 (the hook
  stays the object alone), never on The Room That Proves It, Palette
  Study, Mood, or Trend-Jack (whose whole mechanic is "applied to an
  object instead of a person" — reintroducing hands voids it). Cap: no
  more than ~1 post in 3. **Gated on a hands-specific feasibility spike
  before any real production** — hands are harder to generate cleanly
  than objects (the photoreal spike already logged a ~1/3 artifact rate
  on objects alone), and a Group Legal/Compliance read on whether an
  AI-generated disembodied hand falls inside Instagram's 2026-08-31
  AI-people reach-limit policy (which targets generated *people*, not
  products/backgrounds — likely clear, not yet confirmed).

### Anti-repetition (revised for 2/day)

- No carousel pillar repeats two days running.
- No Reel pillar repeats two days running.
- Palette Study gets a new named material each time; Insider Knowledge
  sub-angles don't repeat within 30 days; a Two Objects comparison never
  reuses the same object pair.
- Add a scene/prop check to Mood and Evidence photography the same way
  Reels already have one — two posts in one week must not share the same
  staged setup even if the "lesson" differs.

---

## 4-6. Hooks, hashtags, posting times

Unchanged from the 2026-08-30 doc **except**: drop `#quietluxury` from the
always-on hashtag pool per §1's table above (the label is in backlash, the
substance isn't — don't advertise the label). Everything else in these
sections (caption pattern, copydesk gate, hashtag/keyword strategy,
posting-time research) remains valid and is not repeated here to avoid
drift between two copies of the same guidance.

---

## 7. Cadence plan (revised 2026-09-05 — founder decision)

**Daily: 2 posts — 1 carousel + 1 Reel.** Reduce further (to 1/day, or
3/week) once follower growth is real — the founder's own stated plan, not
a fixed schedule. Revisit this number once Insights data exists (§2).

Sample week (illustrative rotation, not a fixed script — trend-jack and
real trending audio always take priority over the pre-planned Reel slot
when something genuinely relevant is live):

| Day | Carousel | Reel |
|---|---|---|
| Mon | Palette Study | Satisfying Process |
| Tue | Two Objects | Quick Game |
| Wed | The Evidence | Reveal/Transformation |
| Thu | Insider Knowledge | Trend-Jack |
| Fri | The Room That Proves It | Satisfying Process |
| Sat | Mood | Quick Game |
| Sun | Insider Knowledge | Reveal/Transformation |

**Every post:** gate-checked render (contrast + ink coverage + eyeballed
350px feed preview), copydesk-clean caption, `needs_review: true` for
founder clearance — unchanged from before.

---

## 8. Visual identity (revised 2026-09-05 — the pivot)

**Retired:** the Curator character and the illustrated room-set renderer.
`assets/rig2d.js` (the shared stickman) is no longer used on this account
under any pose.

**New primary visual: photoreal object/material imagery**, generated
locally at ₹0 via the `video_lab` ComfyUI pipeline. **This is not yet
technically validated** — the existing local setup is proven for
text-to-video (WAN 2.1), not verified for 1080x1350 still-image
generation. **Immediate next step, before any real production:** a
Group CTO spike — 3 test images of one object under the lighting
discipline below, gate-checked, compared side by side against the old
cream hook-card style at actual feed scale. Decide from the thumbnails,
not from this document.

**Photography discipline (once the pipeline is validated):**
- One light source, low angle, warm (~3000-3500K), consistent across
  every post — this consistency is what makes a grid read as one
  continuous world (Studio McGee's mechanism).
- Desaturated grade. Saturation is the loudest cheap signal there is.
- Matte surfaces only — gloss reads cheap in stills.
- Real shadow with soft falloff.
- **No people, no hands with visible faces, no silhouettes that read as a
  posed human.** This is a hard platform constraint, not a style choice:
  Instagram (as of 2026-08-31) limits reach on undisclosed AI-generated
  *people* specifically — it does not restrict AI-generated objects,
  backgrounds, or products. The Mood pillar's candid gesture shots must
  stay partial/ambiguous (a hand, never a posed face) for this reason.

**Palette — tokens kept, roles changed:**
- Alabaster `#F2EEE6` — now the mat/frame/negative-space around
  photography, not the dominant ground.
- Espresso `#2A241E` — ink, and the ground for every third post (see
  tonal rotation below).
- Taupe `#6E6257` — secondary type only, never a photographic subject.
- Bronze `#9C7A4F` — hairlines, numerals, meta labels only. Never body
  text, never more than ~2% of frame area.

**New rule — tonal rotation across the grid**, the single fastest fix for
"the grid looks monotonic": every post rotates strictly light -> mid ->
dark value key (light = alabaster-dominant, mid = the photo's own
mid-tones, dark = espresso ground). Checkable mechanically (mean
luminance, banded into three ranges) in `gate_check.py`.

**Typography restraint (tightened):**
- On any frame containing photography, type occupies ≤15% of frame area,
  sits in a margin, never centered, never over the subject.
- Maximum 7 words on frame 1 (the old hook cards ran 8-10 words across
  three lines, eating ~40% of the frame — fix this specifically).
- Cormorant Garamond for the one headline, Archivo letterspaced caps for
  eyebrow/numeral/Nuvarel Index score. Nothing else.
- Drop the `@NUVAREL_ · 01/07` footer bar from photographic frames
  entirely — it signals "a template made this."
- Frame 2 of every carousel is a full-bleed photograph with no type at
  all. A silent frame is the cheapest luxury signal available.

**What makes a frame instantly recognizable as nuvarel:** a single
object, lit from one low warm side, on an alabaster or espresso ground,
one bronze hairline, at most seven words of Cormorant in a margin, and
(once built) the Nuvarel Index numeral in the corner. Renderer path stays
`accounts/nuvarel/render/` — same deck-JSON → HTML → headless Chromium
mechanism, new deck content and new photography step, not a new pipeline.
