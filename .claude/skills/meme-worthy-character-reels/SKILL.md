---
name: meme-worthy-character-reels
description: How to build genuinely meme-worthy, character-animated Instagram Reels for this repo's accounts using free/open-source tooling (no paid AI-video APIs). Use this whenever asked to make a Reel, animate a character for Instagram, build a "hook" video, or improve an account's video content -- even if the request just says "make a reel" or "animate this" without naming a tool. Also use it if a founder/reviewer says animated content looks "amateur," "not catchy," "PPT-style," or otherwise rejects a video on motion quality -- this skill exists specifically because that happened once already and documents both the fix and the review discipline that catches it before it ships again.
---

# Meme-worthy character Reels

This skill exists because a full batch of 9 "character-animated" Reels was
built once, passed every automated check (ffmpeg validation, frame
sampling, copydesk), and was still rejected outright by the founder:
*"All are very very bad... looks like someone just starting with video
editing made it."* The cause wasn't the hook writing or the brand voice —
both had already passed review. It was motion quality: a 3D mocap
character rig retargeted from stock clips, with no animation principles
designed in on purpose. The redo (2D HTML/SVG stickman, same account
family) was approved on the first real look. The difference between the
two attempts is what this skill captures — not just the winning
technique, but the checkpoint discipline that would have caught the
losing one before it shipped to a founder review.

## The core discipline, in one sentence

**Build one prototype, actually look at rendered frames yourself before
building the other eight, and never let a technical QA pass (ffmpeg
validation, frame count, file size) stand in for a human actually judging
whether the motion reads as intentional.** Everything else in this skill
is in service of that one rule.

## Process

1. **Research current hooks and trends** if you don't already have
   solid, dated source material — proven hook categories, retention
   benchmarks, what's actually winning right now (not what won a year
   ago). See `references/hook-research-summary.md` for the last verified
   pull (2026-08-30) if it's still recent enough to reuse; otherwise
   redo it, dated sources only.
2. **Pick a tool. Read `references/tool-choice.md` before defaulting to
   whatever's already installed** — the wrong default (a 3D rig doing
   comedy) is exactly what caused the rejection this skill exists to
   prevent.
3. **Build ONE prototype Reel first.** Pick whichever account/concept is
   fastest to validate the approach against, and the account with the
   strictest bar if there's a choice (a "must be funny" account beats a
   "must be calm" account as your validation case — comedic timing
   failures are more visible). Do not proceed to the rest of the batch
   until this step's output has been reviewed by a human against real
   rendered frames.
4. **Extract labeled still frames from the actual render** — not just
   from the source code, from the rendered mp4 — at the hook (~0.5-1s),
   each anticipation beat, each impact/squash-stretch peak, each
   comedic-pause hold, and the payoff. Read them yourself (or have the
   requester read them) with an image-viewing tool before calling
   anything done. A frame that looks wrong on screen is real feedback; a
   passing ffmpeg check on the same file is not evidence against it.
5. **Only after that checkpoint clears, build the rest of the batch**,
   reusing whatever rig/helper code the prototype produced — don't
   rebuild animation-principle infrastructure per Reel. See
   `references/animation-principles.md` for what to name and check at
   each beat.
6. **Differentiate tone per account, explicitly — never propagate one
   account's energy onto another by default.** A punchy, slapstick,
   meme-fast account and a calm, elegant, deliberate-pacing account need
   different edit rhythm even off the *same* rig and the *same* craft
   bar. Ground each account's tone in its own existing strategy
   doc/brand voice, not in whichever account you built first.
7. **Music/audio is not optional.** Silence or SFX-only reads as
   unfinished. Use a free, no-signup source (Pixabay Music, Mixkit) and
   log the license the same way this repo's `assets/audio/
   ATTRIBUTION.md` already does — check that file for the established
   format before adding a new entry.
8. **Run every on-screen line through this repo's copydesk voice check**
   (`py -3 -m copydesk --caption`, or however the current gate is
   invoked — check `docs/registry/copydesk.md` in the `income-engine`
   portfolio repo if unsure) before calling any Reel finished. This
   applies to captions, overlay text, and any character dialogue that
   renders as text.
9. **Leave `needs_review: true`** on every new/changed manifest unless a
   human has explicitly told you to clear it. Publishing is a
   founder-reserved action in this portfolio — see `income-engine/
   CLAUDE.md`'s decision-authority section if you're unsure whether a
   given clearance is yours to make. If you do get explicit clearance,
   flip only the specific manifests you were told to, verify the diff
   before committing (see step 10), and don't touch scheduling for
   anything you weren't asked about.
10. **Shared-repo git safety applies throughout.** This repo may have
    other sessions working in it concurrently. Before any `git commit`,
    run `git diff --cached --name-only` as its own, separate command —
    never chained with `&&`/`;` into the same call as the commit — and
    actually confirm the staged file list matches only your own intended
    changes before committing.

## Why frame-level human review beats automated QA here

Automated checks (does the file decode, is it the right resolution/
framerate, does the runtime match) can only catch whether a video
*exists correctly* — never whether the *motion reads as intentional*.
The rejected 3D batch passed every one of those checks. What it lacked —
absence of squash-stretch, mismatched anticipation carried over from an
unrelated stock clip, no designed comedic pause — is invisible to a
frame-count or codec check and immediately visible to a human looking at
even a handful of still frames. Treat "the render pipeline succeeded" and
"a human looked at it and it's good" as two separate, both-required gates
— never let the first stand in for the second, and don't skip straight to
building nine outputs before the first prototype has cleared the second
gate.

## Reference files

- `references/tool-choice.md` — why HTML/SVG-via-headless-render beat 3D
  character rigs and GUI-first 2D tools for this repo's pipeline, and
  when that reasoning might not hold (read before assuming the same
  choice applies to a different repo/pipeline).
- `references/animation-principles.md` — the specific, nameable things
  ("anticipation beat at Ts," "squash-stretch peak, 2-frame hold, fast
  recovery," "hard comedic pause, N-frame hold before the next beat")
  that separate motion which reads as intentional from motion that
  doesn't, plus the concrete rig helpers already built for this
  (`assets/rig2d.js`) that implement them.
- `references/hook-research-summary.md` — the last dated pull of proven
  hook categories and retention data (2026-08-30) — reuse if still
  recent, redo with fresh dated sources if not.
- `references/known-pitfalls.md` — specific bugs already hit and fixed
  once (a shared-element style guard silently killing a page background;
  an "intentional" scenery element that visually read as a broken UI
  card) — check before you re-invent, or re-break, the same thing.
