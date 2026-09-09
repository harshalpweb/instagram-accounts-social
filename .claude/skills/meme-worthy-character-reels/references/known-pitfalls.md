# Known pitfalls — hit once already, check before repeating

## A shared-element style guard can silently break rendering

`assets/rig2d.js`'s stale-paint guard (used to force Chromium to commit a
repaint before each frame capture) sets its target element's
`backgroundColor` to `"transparent"` on alternating frames. When the
target was `document.body` (or any element that itself carried a
background), this silently killed the page's background — one Reel
rendered fully white before the bug was caught during frame-level review
(not by any automated check).

**Rule:** any guard/helper that writes styles to a shared element for a
side-effect purpose (forcing a repaint, forcing a reflow) must target a
dedicated, background-less wrapper element — never an element that also
carries real visual state of its own. The bug is invisible in code review
and only shows up as a wrong-looking rendered frame, which is one more
reason the frame-level review step in the main `SKILL.md` is not
optional.

## "Intentional" scenery can still read as a broken UI element

One early scene included a background prop (a bathroom mirror, styled as
a flat rounded rectangle) that happened to share the exact visual
language — panel fill, rounded corners, hairline border — of this
pipeline's empty/unpopulated UI card states. In a still frame it was
genuinely ambiguous whether it was set dressing or a card that failed to
populate, and at one timestamp a character-reaction stamp overlapped it,
reading as a broken second bubble.

**Rule:** if any authored element (whether it's "real" scenery or "real"
UI) could plausibly be mistaken for the other at a glance, that's a
defect regardless of what it was intended to be — fix the visual
distinction (different fill, no border, a clearly different shape) rather
than defending the intent. This is exactly the kind of thing frame-level
review catches and code review does not.

## Lerping a mirrored pose wraps the torso through "pointing down"

`rig2d.js` angles are degrees with 0 = down, 180 = up, and `mixPose`
lerps them numerically. Mirroring a pose for a character facing the other
way (negate every angle) turns a torso of 192 into -192 -- the same
direction, but `mixPose(stand, mirrored, k)` then interpolates 180 -> -192
the long way round, passing through ~0 (straight down) mid-blend. On the
2026-09-10 elevator Reel this made the second stickman fold in half onto
the floor for ~6 frames of a windup; every probe frame happened to miss
that window and it was only caught on the full render's QA dump.

**Rule:** any pose that is *lerped into* (not just set) must keep its
angles on the same side of the wrap as the pose it is lerped from --
after mirroring, re-express the torso (and anything else near 180) as
its 360-equivalent (e.g. -192 -> 168) before handing it to `mixPose`.
Poses that are assigned directly are unaffected. Probe the whole blend
window at 1-2 frame spacing, not just its endpoints.

## Automated QA passing is not the same signal as "looks good"

Worth restating here because it's the whole reason this skill exists: a
batch that passes ffmpeg validation, correct resolution/framerate,
correct duration, and copydesk's text-voice check can still be rejected
outright on motion quality. Don't report a Reel (or a batch) as done on
the strength of those checks alone — see the main `SKILL.md`'s
frame-level review step, which is the actual gate for the thing those
checks cannot see.

## Add to this file

If you hit a new pipeline-specific bug while using this skill — something
that would waste another session's time rediscovering it — add it here
with the same shape: what it looked like, why it's non-obvious, and the
rule that prevents it. Keep entries short; this file is for real,
already-hit bugs, not hypothetical ones.
