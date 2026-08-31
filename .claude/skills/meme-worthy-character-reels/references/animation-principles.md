# Animation principles: what to name, per beat, before you call motion done

Three principles account for most of the gap between "reads as amateur"
and "reads as intentional." Name where each one fires — with a timestamp
or beat label — in your own notes or code comments before rendering.
Motion that skips this and just interpolates between poses is exactly
what produced the rejected batch.

## Squash & stretch

Its *absence* is what reads as stiff/rigid. Use a "feel it, don't see it"
amount — enough to register at a glance on a fast watch-through, not so
much it looks cartoonishly wrong — and recover out of the extreme
quickly (2-3 frames, not a slow ease back). Every impact (a landing, a
splash entry, an object set down) is a candidate beat for this.

`assets/rig2d.js` implements this as scale keyframes about a pivot point
(`sx`/`sy` fields on a pose, `px`/`py` for the pivot) — a squash needs its
pivot at the contact point (e.g. the feet on a landing), not the object's
center, or it reads as the whole shape shrinking rather than compressing
against something.

## Anticipation

A small counter-movement before the real action sells the action as
intentional and weighted — a slight crouch before a jump, a windup before
a punch, a lean back before a lunge forward. The failure mode from the
rejected batch: anticipation *was* present in the stock mocap clips used,
but it was anticipation authored for the clip's *original* action, not
the comedic beat it was repurposed into — mismatched anticipation reads
as motion that doesn't quite make sense even when a viewer can't say why.

Rule of thumb: if you're authoring a beat from scratch (as this rig's
approach requires), give every "big" motion its own short counter-move
in the opposite direction first, sized to that specific beat — don't
borrow timing from an unrelated action.

## Timing & spacing, specifically for comedic beats

Comedic timing is rapid action followed by a **hard pause** so the
audience can register the joke — not smooth continuous motion throughout.
Name, per Reel, where the hard pause lands (a timestamp or beat index)
and how long it holds (a frame or second count) — don't leave this to
"however long the next beat happens to start." A held "dead-eye" or flat
expression during the pause reads as a deliberate comedic choice; a pause
that's just an animation finishing and nothing happening yet reads as
dead air.

## What this looked like in practice (from the approved prototype)

From the actual notes for the first approved 2D Reel (`hype_tingles` H1,
"morning routine judged by animals," 14.2s runtime):

- Anticipation: bed-compress at 0.90s, tub windup at 3.30s **with a
  2-frame hold** before the dive, a counter-lean at 7.55s, a dive-brake
  at 9.95s.
- Squash/stretch: every impact at 10-18% scale change, 2-frame peak, fast
  recovery — including a secondary squash on a prop (the mattress) at
  10.45s, not just the character.
- Comedic holds: 2.18s, 4.65-5.60s (the largest — a single blink at
  5.25s inside the hold, not a static freeze), 8.20-9.30s, 11.40-12.30s.

None of this needs to look identical on a new Reel — the point is that
every beat like this was a specific, named, deliberate choice, not a
default the renderer produced on its own.

## Checking your work

Extract still frames at each of these labeled beats from the *rendered*
output (not just reasoning about the code) and look at them — see the
main SKILL.md's frame-level review step. A squash that isn't visible at
its peak frame, or an anticipation counter-move too small to read in a
still, needs to be bigger, not just theoretically present in the code.
