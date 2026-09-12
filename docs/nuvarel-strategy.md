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

**THIRD REVISION — 2026-09-12, Group CTO, founder-direct (read this first).**
Sections **§9 to §15 at the end of this file are the current strategy** and
supersede where they conflict: §7 (cadence) is superseded by §15 and
`docs/cadence-and-format-policy.md`; §1's audience and §3's pillar scope are
*widened* by §11; §2 gains the 2026 platform findings in §10; §8's
all-generated visual pipeline gains a mandatory real-footage lane in §10.3.
Everything else in §1-§8 stands. New in §9-§15: the long-term vision
(50k/100k), the two named monetization paths with real numbers and their
counter-evidence, the niche width ruling, the short-term 4-week plan, and the
useful-account metric. Reason this revision exists: the founder reviewed the
account on 2026-09-12 and said the strategy "feels random," carries no evidenced
confidence of organic growth, and has no stated long-term or short-term vision.
Full record: `../docs/consults/2026-09-12-group-cto-instagram-strategy-overhaul-and-nuvarel-deep-dive.md`.

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

**Hook & genre-matching rule (added 2026-09-05, CoS, data-driven — first
real evidence from this account's own numbers).** Insights collection
went live same day (§ above); its first snapshot surfaced one real
outlier: the (now-retired-pipeline) `cables-read-cheap` Reel hit 377
reach / 32% 3-second-skip — the best of any nuvarel post so far, and the
only post across all 3 accounts with an earned share — against a
same-day, same-quality, same-slot sibling (`bathroom-splurge-skip`) that
got 61 reach / 72.9% skip. Full root-cause trail:
`income-engine/docs/registry/instagram_accounts_social.md`. Two rules
worth carrying forward into every pillar, independent of the visual
pipeline in use:
1. **The hook must open a curiosity gap, never state the verdict.**
   "The cheapest thing in an expensive room" (withholds the answer) beat
   "Splurge or skip: the bathroom" (states the format) with identical
   production quality either side of it. Frame-1/second-1 copy should
   make the viewer need the payoff, not already have it.
2. **Prefer a topic that maps onto an already-proven viral content
   genre** ("chaos resolves to order," "reveal under a cover," "which one
   wins the test") **over a topic that is only a personal-taste opinion**
   (towel weight, lamp symmetry) — the genre itself carries pre-existing
   shareability the account doesn't have to build from zero, and Reels'
   2026 ranking model weights sends/DM-shares far above likes, so a
   topic's built-in forward-to-a-friend utility matters more than polish.
   This is a direct, evidence-based reason to actually prioritize **Reel
   pillars 7 (Satisfying Process) and 8 (Reveal/Transformation)** in §3
   below over the current default of shipping 3 Quick Games Reels
   first — that default was a reasonable bet before any real performance
   data existed; it now has a data point arguing the other way.
   **Flag for Group CTO/CCO, not unilaterally overridden here:** worth
   revisiting the pillar sequencing decision with this evidence in hand.

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
   - **Recommended first (2026-09-05, data-informed, hook & genre-matching
     rule above): "The Recovery Test."** Hook (curiosity gap, no verdict
     stated): *"Press it. Count to three."* Press a cushion, hold, watch
     it recover — or not. Genre match: cushion/foam "poke test" content
     is an established viral category (the same mechanism as a mattress
     press-test video) and this account's actual positioning ("the proof,
     not the claim") makes it more than generic ASMR — it's a real
     showroom technique. Draft caption (copydesk-clean, 51 words, 0
     em-dash): "Press a cushion and count to three. Cheap foam holds your
     handprint. High-density fill or a real feather-and-down mix stands
     back up before you finish counting. You can test this in the
     showroom before you buy, no salesperson needed. Save this for the
     next sofa shop. #interiordesigntips #homedecortips
     #furnitureshopping #expensivelooking #homestyling".
     **Correction (income-engine-d1, 2026-09-05, same day):** originally
     written as an Inspection-device (hands-only) shot — that's premature.
     Inspection was NOT settled when this was written: a feasibility
     spike found the originally-proposed gesture ("thumb along a seam")
     doesn't render reliably. **Superseded same day:** the founder has
     since decided Inspection uses a real filmed hand, not AI-generated
     (resolves the render-reliability and disclosure questions in one
     move — see the top revision note). Filming hasn't happened yet, so
     this still isn't shoot-ready with a hand. **Hands-free fallback (two
     cushions, a small weight dropped/removed to trigger the press
     instead of a hand) remains available but does NOT skip the gate
     below** — it's still generated footage of a physical event either
     way. **Second, more fundamental gate (Group Legal, 2026-09-05 —
     standing-note P26): this is a Reel, so it needs `photo_reel` open
     regardless of hands** (video generation is the unproven half of the
     pipeline, not stills) **AND, once that lane opens, a generated
     demonstration of a physical outcome is a fabricated evidentiary
     claim on an account whose whole positioning is "the proof, not the
     claim."** Before shooting this with generated footage: either film
     it for real, or reframe the caption/premise so it illustrates rather
     than claims to record an event (e.g. "here's what real recovery
     looks like," not "watch this cushion recover"). Topic is clear
     against the 60-day ledger either way.
8. **Reveal / Transformation** (`reel-reveal`) — a dust sheet pulled off
   a covered piece, a plain box unwrapped to reveal something beautiful,
   a raw-material-to-finished-object fast-forward (thread to fabric, clay
   to vessel). Drama + payoff under 10 seconds.
   - **Recommended second (2026-09-05, data-informed): "The Grain
     Underneath."** Hook (curiosity gap): *"This board was headed for the
     scrap pile."* One continuous sanding pass across two boards side by
     side — real wood reveals new grain the deeper it goes, printed
     veneer reveals the same repeating pattern no matter how far you
     sand. Genre match: wood-refinishing/sanding-reveal content is an
     established satisfying-video category; ties directly to The
     Evidence pillar's dovetail/veneer mechanic. Draft caption
     (copydesk-clean, 58 words, 0 em-dash): "Sand two boards side by
     side. Real wood reveals new grain the deeper you go, every pass
     looks a little different. Printed veneer reveals the same repeating
     pattern no matter how far you sand. Ten seconds with sandpaper tells
     you what the price tag will not. Save this for the next furniture
     aisle. #interiordesigntips #homedecortips #furnitureshopping
     #expensivelooking #homestyling". Not yet queued — needs `photo_reel`
     open (video generation unproven), and per the same Legal flag as
     above (standing-note P26): reframe as illustrating what real grain
     looks like, not as claiming to record two specific boards actually
     being sanded, unless filmed for real. Topic is clear against the
     60-day ledger.
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
  cuff at the wrist, always; one action, one take, no cuts; **never a
  face, never past the cuff, never two hands doing different things.**
  Applies inside The Evidence, Two Objects, and Insider Knowledge (esp.
  The 60-Second Inspection, Care Secrets, Ages Well/Ages Badly) on the
  carousel side, and Satisfying Process/Quick Games/Reveal on the Reel
  side. **Never** on a carousel's frame 1 (the hook stays the object
  alone), never on The Room That Proves It, Palette Study, Mood, or
  Trend-Jack (whose whole mechanic is "applied to an object instead of a
  person" — reintroducing hands voids it). Cap: no more than ~1 post in 3.

  **Resolved 2026-09-05 (founder decision): the hand is REAL, not
  AI-generated.** A feasibility spike found AI-generated hands
  technically workable but fragile (~1-in-5 usable clips, ~1-in-2.5
  usable stills, mandatory eyes-on pick each time) and the originally-
  proposed gesture ("thumb along a seam") doesn't render reliably at
  all. Separately, Group Legal/Compliance found the AI-generated-hand
  question genuinely unresolved against Instagram's AI-persona policy
  (no primary source covers this exact edge case) — a real signature
  cuff repeated across posts is exactly the kind of consistent-identity
  marker that policy targets, and the penalty is account-wide reach
  ineligibility, not a single post. **A real filmed hand resolves both
  problems at once**: no AI-persona policy exposure, no mandatory
  AI-content video disclosure (that requirement applies to AI-generated
  photorealistic video specifically — real footage is exempt by
  definition), and no fight with an unreliable generation pipeline.
  It's also arguably a *better* fit for this account's actual promise
  ("the proof, not the claim") — genuine hands-on demonstration is more
  credible than a simulation of one, and every real luxury-craft
  comparable (watch/leather/joinery content) uses real hands, never
  illustrated or generated ones.
  **Practical next step, not yet done:** someone needs to actually film
  this — a phone camera in good raking light is enough quality-wise
  given the account's existing warm/low-angle lighting discipline (§8).
  Doesn't need to be the founder's own hand specifically, just a real
  one, filmed once per needed gesture and reused/re-cropped where
  sensible. No AI generation dependency for this device anymore; the
  earlier hands-generation spike's findings (gesture vocabulary, entry
  side, pick rates) are now moot for The Inspection specifically, though
  the same spike's *general* AI-hands findings may still matter if any
  other device ever needs a generated hand.

  **Interim path, approved 2026-09-06: "The State" — hands-free
  before/after object comparison, buildable today.** Real-hand filming
  hasn't happened yet and stock footage was tried and exhausted (search
  logged in the registry) — two search passes, 4 sites, 22 clips, zero
  footage showing an actual test outcome, only people touching things.
  Rather than wait, ship the proof a different way: **two clean
  AI-generated OBJECT-ONLY stills, no hand at all, showing a state
  contrast instead of a live action** — a cushion holding a visible
  lasting dent next to one sitting smooth and recovered; a scratched
  finish next to an unmarked one; a warped board edge next to a true
  one. This is the already-validated *still* pipeline (not the fragile,
  legally-uncertain hand-generation path), so it sidesteps both open
  problems at once: no AI-people policy question (no person, generated
  or otherwise, in frame) and no fight with unreliable hand geometry.
  It still delivers the account's actual promise ("the proof, not the
  claim") as a **comparison**, not a **demonstration** — the two states
  do the proving, same underlying mechanic as Two Objects but framed as
  one object's before/after rather than two competing items. Not a
  replacement for real hands-on footage long-term (a live test is more
  credible than a static comparison), but a real, shippable device
  today rather than a blocked one. Anchors: no hand/person in frame
  ever (this variant's whole point); side-by-side or a simple wipe/
  reveal transition between the two states; verdict stated plainly, not
  left ambiguous. Once real hand footage exists, The State and the
  hands-on version can run side by side as two different Inspection
  registers rather than one replacing the other.

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
locally at ₹0 via the `video_lab` ComfyUI pipeline. **Reconciled
2026-09-05, Group CTO (this line was stale — flagged in the daily-build
rewrite consult):** the validation spike described below has RUN and
PASSED. Stills generation for single objects under the lighting
discipline below is validated and in production (`build-gates.json`:
`photo_carousel` open, keys `dark`/`mid`, `light` experimental); 5 known
issues from the spike are tracked there, including a real material-
fidelity failure mode (a generated "honed travertine" came back as
veined marble) that any human pick step must specifically check for, not
just composition/lighting. **Photoreal Reels/video remain unproven**
(~2h GPU/clip via the WAN 2.1 text-to-video path) — that gap, not stills,
is what gates the Reel pillars in §3 above. Full record:
`income-engine/docs/consults/2026-09-05-group-cto-nuvarel-daily-build-rewrite-photoreal-productionisation.md`.

**Photography discipline (now validated for stills; still applies as
written to the eventual Reel/video pipeline):**
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

---

# Revision 3 — 2026-09-12 (Group CTO, founder-direct)

Everything from §9 down was written on 2026-09-12 against live performance data
and fresh primary research. Where it conflicts with §1-§8 above, §9-§14 win.

## 9. Where this account is going — the vision, long and short

The founder's objection was that there is no stated destination. Here is one,
in two horizons, with the numbers attached.

### 9.1 Long term — what `nuvarel_` is at 50,000 and at 100,000 followers

**The one-line destination:** *the account people check before they spend money
on anything for their home.* Not a mood board. A second opinion.

At **50,000 followers**, nuvarel is:

- A library of ~150 repeatable, nameable tests ("the fold test", "the seam
  test", "the tilt test") that a viewer can perform in a shop in under a minute.
  The library, not any single post, is the asset. It is what makes the account
  worth *following* rather than worth *watching once*.
- Monetised on two paths, both named by the founder and both scoped in §12:
  an **affiliate storefront** of the specific accessible items the tests keep
  saying yes to, and **one or two paid digital products** that package the
  library into something a person about to furnish a home will pay for.
- Earning, on the evidence in §12, a realistic **$300-$1,500 a month**
  (roughly ₹25,000-₹1,25,000) combined across both paths. That is a bounded
  estimate from published creator-earnings data, not a projection from our own
  numbers — we have no revenue history at all. Treat the low end as the planning
  number.

At **100,000 followers**, the same machine plus two things that only exist at
scale: inbound brand work from furniture and material manufacturers who want the
account's verdict, and enough audience to make a higher-priced product
(a full room-by-room buying system, not a checklist) viable. Neither is planned
for; both are what the 50k structure is built to be able to accept.

**What this account is deliberately NOT becoming:** a design-inspiration feed, a
renovation-reel account, or a shopping-haul account. Those are larger niches with
far more reach available (§10.2 has the evidence), and all three are already
saturated by accounts with real homes and real cameras. The bet is that "how to
tell" is a smaller room with a much shorter queue at the door.

### 9.2 Short term — the next four weeks, concretely

Week by week. Every item is a thing someone does, not a thing someone decides.

| Week | Goal | Concrete output |
|---|---|---|
| **1** (Sep 13-19) | Stop the bleed on format. Get 3/day actually publishing. | 21 pieces, format mix from `scripts/plan_day.py` (today: Reels-heavy, one carousel explore slot per 7 days). Under-10k auto-clear live, so posts land in their real windows for the first time. First 7-day performance read written into commit messages daily. |
| **2** (Sep 20-26) | Prove the real-footage lane (§10.3). | At least **4 pieces built from real phone footage** of real objects, against 17 generated. Compare their reach, saves and sends against the generated pieces in the same week. This is the single highest-value experiment on this account. |
| **3** (Sep 27-Oct 3) | Turn reach into saves. | Every `save`-goal piece ends on a named, repeatable test. Target: **first 25 lifetime saves** (current total: 2). Ship the first keyword-comment lead-magnet post once `digital_products` delivers the checklist (§13). |
| **4** (Oct 4-10) | Decide the visual pipeline on evidence. | `growth-analyst` reads real-footage vs generated across ~28 paired pieces and `creative-director` rules on the mix. Apply to Amazon Influencer Program India (free, no published follower minimum) if the account clears ~500 followers; if not, record why and hold. |

**The measurable target for the four weeks, stated so it can fail:** 500
followers, 25 saves, 25 sends. Current: single-digit followers, 2 saves, 5
sends. If week 4 ends below 100 followers, the problem is not the content
schedule, and `audience-strategist` plus `cto` take the account-level
distribution question, the same way `hype_tingles` already has.

## 10. What the evidence actually says (researched 2026-09-12)

### 10.1 The account's own data

From `analytics/insights.csv`, 21 nuvarel posts, 2026-08-30 to 2026-09-10:

- Reels: mean reach **174.9**, n=9. Carousels: mean reach **2.9**, n=12. A
  **60x** gap. The account has been spending most of its production budget on
  the format that reaches nobody.
- Lifetime: 1,609 reach, 22 likes, 5 comments, **2 saves**, 5 shares.
- Two posts (`cables-read-cheap` at 1,091 reach, then four Reels at ~105-120)
  hold almost all of it.

**Two saves.** For an account whose entire promise is "useful," that is the
number that matters most, and it is close to zero. Reach is not this account's
first problem. Reach that produces nothing is.

### 10.2 The platform, 2026

Verified 2026-09-12. Sources are reputable secondary reporting of Instagram's
own statements; Mosseri's year-end memo is an Instagram carousel post with no
citable permalink through the tools available here, so it is flagged as
secondary throughout.

1. **Ranking signals:** watch time, **sends per reach** (DM shares), likes per
   reach — in that order. Sends are reported to carry 3-5x the weight of likes
   for Reels distribution. Nuvarel has 5 sends, lifetime.
2. **Format benchmarks, 2026:** Reels ~4.7x median reach and ~8x follower
   acquisition; carousels ~2.3x save rate and ~1.8x comment depth. Our own gap
   is an order of magnitude wider than the benchmark, which is why
   `scripts/plan_day.py` computes from our data and not from the benchmark.
3. **Mosseri's 2025-12-31 memo:** "the polished, perfect aesthetic is dead";
   Instagram will weight authenticity and provenance signals more heavily
   through 2026; raw, real, human content over synthetic.
4. **The narrow AI rule, unchanged:** from 2026-08-31 Instagram limits reach on
   *profiles featuring AI-generated people* that are unlabelled. It does **not**
   penalise AI-generated objects, graphics or edits. Group Legal's 2026-09-05
   read stands; `is_ai_generated` on a container remains a per-post disclosure
   and is not the profile label. **Do not enable the profile-level toggle.**

### 10.3 The finding that changes this account — and the ruling on it

Three independent pieces of evidence point the same way:

- Mosseri's stated 2026 direction is **away from polish and toward provenance**
  (10.2.3).
- This repo's own niche research (`docs/nuvarel-viral-reel-research-2026-09-12.md`)
  found that the two clips plausibly clearing 10M views in `#interiordesign`
  were **real renovation footage** on sub-100k accounts, while the CGI-rendered
  and styled-luxury accounts sat an order of magnitude below on engagement.
- Our own best post was a Reel matching an **established real-world genre**
  (cable management), not our prettiest render.

**This does not mean the generated-stills pipeline is wrong.** It is not
penalised, it works (175 mean reach on Reels), it costs ₹0, and it is the only
pipeline that can hold a 3-a-day floor. Killing it would be an overreaction to
directional evidence.

**Ruling (Group CTO, 2026-09-12):** the generated pipeline stays as the base
load, and a **real-footage lane opens immediately** alongside it.

- A phone camera in raking window light, filming **real objects the founder
  already owns** — a real drawer, a real fabric, a real cable, a real wood
  edge — is a ₹0 asset this account has never used. It is also the only thing
  that can carry the "proof" claim without an asterisk, and it retires a whole
  category of problem in `build-gates.json`, where a generated demonstration of
  a physical event is a fabricated evidentiary claim. Filmed, it is simply true.
- **Target: at least 4 real-footage pieces in week 2**, run as a measured
  experiment against the generated pieces of the same week (treatment vs.
  same-account control; `growth-analyst` measures).
- The **existing open build gates are unchanged** by this. Real footage needs no
  gate, carries no `ai_generated` flag, and skips the material-fidelity check,
  because the material is whatever it actually is.
- This also unblocks **The Inspection** (§3, signature devices), which has been
  waiting since 2026-09-05 on "someone needs to actually film this." Same phone,
  same session.

## 11. Niche width — the ruling the founder asked for

The founder asked whether the niche should be broader or narrower than the
original one-paragraph brief. The answer is **both, on different axes**, and the
distinction is what makes it work.

**NARROWER on mechanic.** One mechanic, forever: *a named, repeatable test a
viewer can perform themselves in under a minute.* Not "here is why this is
beautiful." Not "here are five trends." A test with a name, a verdict, and a
result the viewer can reproduce. The two best-performing posts on this account
both did exactly this; the flat ones were taste opinions. Anything that is not a
test moves to the `mood` goal, capped at roughly one piece in three.

**WIDER on object.** The original scope was luxury objects. That is too narrow
in exactly the place it costs money:

1. The mechanic works on **anything with a cheap version and an expensive
   version** — a cable, a zip, a hinge, a towel, a light bulb, a paint finish, a
   dish rack. Those are not luxury objects, and they produced this account's
   only real hit.
2. **This is also the monetization fix** (§12.1). The affiliate money in this
   niche is not in the expensive object; the research says affluent buyers still
   overwhelmingly buy the expensive thing in a physical store. It is in the
   accessible ₹500-₹5,000 item the viewer can buy from the post. An account that
   only ever shows ₹80,000 sofas has nothing to link.
3. It costs nothing brand-wise. "The proof, not the claim" does not say
   "expensive." It says *tell the difference yourself*, which is a more
   democratic promise and a larger addressable audience.

**Unchanged:** the visual register stays disciplined and premium (§8). Widening
the object set is not permission to look cheaper. A ₹300 cable photographed like
a ₹30,000 object is the whole joke, and it is the joke that worked.

**Audience, adjusted:** §1's "28-45, 6-24 months into a home they intend to
keep" stays as the core, with the floor removed at the bottom. Anyone about to
spend money on something for a home is in scope. This absorbs the CCO's recorded
dissent on §1 rather than leaving it open.

## 12. Monetization — the two paths, with real numbers and the counter-evidence

The founder named both paths and gave a reason: affluent audiences buy on
impulse. **That reason is partly wrong, and the correction improves the plan.**

Research, 2026-09-12: 89% of wealthy consumers still want to walk into a
physical store, and 51% prefer to browse online but complete a luxury purchase
in person. Separately, 19% of consumers are more likely to impulse-buy luxury
items, and 36% made a $250+ impulse purchase in Q1 2025 with a median of $497 —
so impulse at high value is real, but it is a minority behaviour and it is
weighted toward in-store. For a creator affiliate link the money is therefore
**not** in the expensive object. It is in the accessible adjacent object bought
in the moment the viewer is already convinced, which is exactly what §11's
widening produces.

### 12.1 Path A — affiliate

**Primary channel: Amazon Influencer Program (India).** Verified at Amazon's own
India newsroom, 2026-09-12: free to join, India explicitly supported, requires a
public Instagram/YouTube/Facebook business account, evaluated on "content
quality, relevance, and audience engagement" rather than follower count alone,
and it now runs a dedicated **Home Influencer Program** vertical with curated
storefronts. Amazon publishes **no follower minimum**; secondary reporting puts
practical approval near ~1,000 followers. Approval is two-stage (storefront
first, then a separate on-site video approval).

- Why this one first: it is the only channel verified as India-eligible, ₹0 to
  enter, and carrying a home vertical. It clears `CLAUDE.md`'s
  marketplace-channel gate on entry cost and India eligibility. Payout terms
  still need a primary-source read before any revenue is booked — flagged, not
  assumed.
- **LTK (RewardStyle)** is the stronger home-goods channel on commission (home
  goods reported at 8-15%, premium retail up to 25%) but it is **invite-only**,
  and its India eligibility could not be confirmed at primary source on
  2026-09-12. Treat it as a later application, not a plan.
- Reported earnings, secondary and wide: Amazon micro-creators average ~$312/mo
  in commissions; LTK creators at 10k-50k followers are reported at $500-5,000/mo
  in lifestyle and home. The $300-1,500/mo planning band in §9.1 is the
  conservative read of those two.
- **The demand channel is the platform feed** (Instagram-supplied distribution),
  not organic search. It therefore passes `CLAUDE.md`'s demand-channel default
  cleanly — that rule gates the demand channel, not the affiliate mechanism.

### 12.2 Path B — digital products

The Etsy-shaped answer (printable wall art, the highest-volume digital category
in home decor, $850M+/yr, $35-65 average order value) is **the wrong product for
this audience**. Wall art sells to people decorating. Nuvarel's audience is
people *deciding*.

The right product is the library from §9.1, packaged:

- **Free lead magnet, first:** a one-page printable **60-Second Showroom
  Inspection Checklist** — the tests, in order, for sofa, table, rug, hardware.
  Delivered through the keyword-comment mechanic ("comment SOFA and I will send
  it"), which is the standard 2026 growth loop precisely because comments are a
  ranking signal while links in captions are suppressed. **Built by
  `digital_products`, not here** — the ask is filed (§13).
- **Paid, only after 5,000 followers and only if the free one converts:** a
  materials buying guide priced in `digital_products`' existing ₹299-₹999 band,
  sold through its already-live Razorpay checkout. No new checkout, no new
  compliance surface, no new subproject.

**Neither path starts before roughly 1,000 followers**, and neither is a reason
to change today's content. They are the reason the content is shaped the way
§11 says.

## 13. The `digital_products` ask

Filed 2026-09-12 as a named cross-subproject request:
`../docs/pending-tasks/2026-09-12-nuvarel-lead-magnets-ask-to-digital-products.md`,
indexed under "Cross-subproject asks" in `../docs/pending-tasks/README.md`.
Two free PDFs (a 60-second showroom inspection checklist, and twelve accessible
swaps), ₹0, non-blocking, explicitly declinable. **Nothing in that brief is
built in this repo** — the founder ruled that `digital_products` builds it.

## 14. Trend research — specified, not live

`docs/trend-research-step-spec.md`. **Blocked on Chief Security Officer review**
of the cookie-based browser session. It is a **soft dependency** by design: when
it goes live, a failure or an unavailable machine drops the build back to pillar
rotation and logs the skip. It never blocks a build, and it never becomes the
reason a slot goes unfilled.

## 15. Operational rules that now live elsewhere

Cadence (3/day until 50k), the data-driven format mix, posting-time windows and
jitter, the hook and CTA rule, and the quality floor are **cross-account** and
are canonical in `docs/cadence-and-format-policy.md`. They supersede §7 of this
document and the standing-slot table in
`accounts/nuvarel/docs/daily-build-agent-prompt.md`. Do not restate the numbers
here; they will drift.
