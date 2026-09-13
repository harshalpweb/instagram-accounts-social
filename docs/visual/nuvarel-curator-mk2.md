# Nuvarel — "The Curator Mk II" character spec

**Status:** PREVIEW SPEC, not yet cleared for production. Written
2026-09-13 to capture a design brief that existed only in chat before this
point (a real gap — nothing about "Curator Mk II" existed as a file
anywhere in this repo or `income-engine/docs/` until this document).
Companion rig implementation: `accounts/nuvarel/assets/curator.js`
(account-local, deliberately NOT part of the shared `assets/rig2d.js` —
see "Why a dedicated file" below). First sample Reel built against this
spec: "The Foil Hat" (candle wax test), rendered as a one-off preview, not
queued to `content/`.

**Relationship to the standing no-mascot ruling.** `docs/nuvarel-strategy.md`
(2026-09-12, founder-direct, via Group CTO) currently reads: *"No
character/mascot on this account, redesigned or otherwise."* This spec and
its sample Reel do not reverse that ruling — they exist because the founder
asked to actually watch a redesigned-character sample before any decision
about production use is made. Treat this document and the sample Reel as
decision input, not as an implicit re-approval of a Curator-based pipeline.
Whoever reviews the sample should explicitly record whether it changes the
2026-09-12 ruling, rather than let the existence of a rendered sample
silently supersede it.

## Why a dedicated file, not `assets/rig2d.js`

The original "Curator" was never a bespoke asset — it was `assets/rig2d.js`,
the same shared stickman rig `hype_tingles` uses for meme jokes (down to a
`sitFlop`/`eyes:"dead"` pose). A stick figure with no material, light or
weight cannot signify wealth, and reusing one rig across a slapstick
meme account and a quiet-luxury account meant neither could develop its own
visual language. `curator.js` is nuvarel's own file for exactly this reason
— never merge this character into the shared rig, even if a future rig
looks superficially similar.

## Character spec

**Proportions.** 8.5 heads tall; figure height ≈563px in the rig's internal
coordinate space (one head ≈66px). Ovoid head (rx 26, ry 33). Visible neck,
30px. Torso 175px. Upper arm 112px, lower arm 100px, hand ≈20px. Upper leg
142px, lower leg 136px, foot ≈14px.

**Limbs.** Tapered FILLED paths, 8px half-width at the torso/thigh end
tapering to 5px at the wrist/ankle end — never a uniform-stroke line.
Junctions (shoulder, hip, neck) get explicit construction, not a bare
butt-join: in the implemented rig each limb is one continuous tapered
ribbon drawn along a single quadratic-bezier spine (shoulder→elbow(control)
→wrist, hip→knee(control)→ankle) rather than two straight segments meeting
at a raw joint, which is what actually avoids the classic segmented-limb
seam; the neck gets its own explicit trapezoid shape; the coat garment
silhouette visually resolves the shoulder/hip attachment points.

**Hands.** Three fixed shapes — `flat` (open palm), `pinch` (thumb+finger),
`grip` (closed) — each ~20px, built as tapered wedges/paddles, never dots.
**Feet.** ~14px forward-angled wedges (14px is the wedge's cross-width; the
wedge extends further in the toe direction).

**No face.** Ovoid head, one continuous hair mass (a single filled path,
never cloned shapes), no eyes, no mouth.

**Garment.** One continuous ovoid overcoat/wrap silhouette, filled (not
just outlined), gradient light `#E4DCCB` (shoulder) → dark `#4A4138` (hem).

**Color.**
- Figure body: Taupe `#6E6257` (mid-key scenes) / `#B8AFA2` (dark-key
  variant, for a scene where the background itself is dark).
- One bronze `#9C7A4F` hairline accent at a cuff/closure, ≤2% of frame.
- **The figure must never be the darkest or lightest element in frame** —
  that belongs to whatever object it is interacting with. In a mid-key
  nuvarel scene (alabaster walls, espresso trim) the figure's taupe sits
  correctly between the two.

## Motion principles

- **No squash/stretch on the figure itself.** Squash/stretch is reserved
  for objects the figure interacts with (3-5% typical).
- **Anticipation:** 0.35-0.5s before any major action.
- **Overlapping action:** hair/hem lags the torso by ~3 frames (~0.1s at
  30fps) — implemented by sampling the torso's own angle/lean function at
  `t - 0.1` when driving hair sway, not by keeping per-frame state (every
  frame must stay independently seekable).
- **Easing:** `easeInOutCubic` only. No bouncy overshoot.
- **Stillness holds:** 0.6-0.9s after each payoff.
- **Staggered resolution:** when multiple objects resolve at once, stagger
  them 0.05-0.12s apart — never simultaneous.

## "The Appraisal" beat structure

Khaby-Lame-inspired comedy, deliberately toned down (~3-4/10 intensity,
not full meme-level 7+/10) to fit nuvarel's calm, quiet-luxury tone.

1. **The Overcomplication** (~2.6s) — the "wrong"/overcomplicated way,
   shown fast and silent (no dialogue; music/SFX only), ≤7-word on-screen
   hook, curiosity gap.
2. **The Appraisal hold** (~1.1s / 33 frames) — the Curator stops
   completely. One small micro-motion at ~40% through: a 6° head tilt OR a
   1.5% breath-scale — pick one, not both. This pause IS the joke; nothing
   else moves.
3. **The Simple Way** (~4s) — one clean movement, the real test/payoff,
   performed once, in real time.
4. **The Verdict Mark** (~2s close) — the Curator places the object down
   with one decisive tap (8-10% squash on the OBJECT only, never the
   figure), one hand rotates palm-up beside it at ≤25° from rest, held
   ~12 frames, hand exits frame, object alone on screen with a closing
   sound cue.

**Calibration ceiling** (do not exceed):
- The closing gesture is ONE hand only, ≤25° rotation, never above chest
  height.
- Shoulder rise ≤4% of body height — no visible shrug.
- Head rotation ≤8°, once per Reel.
- The Curator moves at most twice in the whole Reel (the Appraisal
  micro-motion and the Verdict gesture count as the two; the figure stays
  otherwise static — no idle sway, no continuous breathing loop).
- The joke targets the METHOD or the OBJECT, never a person.

## Rig API (`accounts/nuvarel/assets/curator.js`)

- `ensureCuratorDefs(stageSvgEl)` — adds the coat gradient `<defs>` once.
- `makeCurator(parentEl)` — builds the persistent SVG elements for one
  figure, returns a handle.
- `poseCurator(handle, {x, y, scale, pose})` — repositions the whole
  figure at stage coordinates `(x, y)` (the figure's local origin is the
  top of the head) and applies a pose dict shaped like:
  `{head_tilt, lean, legs: {back: {...}, front: {...}}, arms: {back: {...},
  front: {...}}}` (per-limb keys: `*_dx`/`*_dy` offsets from the limb's
  default anchor, `hand`/`hand_rot`/`hand_ox`/`hand_oy` for the front/back
  hand, `foot_rot`/`foot_mirror` for feet).
- `CURATOR_POSES` — four named reference poses (`regard`, `reach`, `draw`,
  `liftAndTilt`) carried over from the static reference sheet
  (`curator_mk2_sheet.png`, preview-only, not committed) as starting
  points for new Reels; author new poses by copying and adjusting one of
  these rather than starting from raw numbers.
- Pose parameters are hand-authored control points on a quadratic-bezier
  ribbon per limb, **not** a rigid forward-kinematics skeleton — the
  declared bone lengths above are for scale reference only. This is a
  deliberate simplification for a stylized flat-illustration rig; if a
  future Reel needs true IK (e.g., a hand that must track a moving prop
  precisely), extend the rig rather than fighting the free-form authoring
  model.

## Known limitation of this preview

The garment reads closer to a knee-length wrap dress/tunic than a heavier
"overcoat" in the strict wardrobe sense — acceptable for this preview per
the spec's own "ovoid overcoat/wrap garment silhouette" language, but worth
a second design pass if the character moves toward production.
