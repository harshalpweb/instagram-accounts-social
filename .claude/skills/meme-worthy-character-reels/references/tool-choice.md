# Tool choice: why HTML/SVG-via-headless-render, not 3D or GUI-first 2D

## What was tried and rejected

A 3D character rig (Quaternius CC0 base character + Rigify retargeting,
stock mocap animation-library clips) via Blender, rendered headless
through `bpy`. This produced technically correct video (right resolution,
right framerate, clean encode) that the founder rejected outright as
amateur-looking. The specific, nameable cause: stock mocap clips carry
animation timing designed for their *original* context (a punch, a walk
cycle), not for the comedic beat they were repurposed into — no squash-
stretch was added, no anticipation was authored for the actual joke, and
default retarget timing doesn't know where a comedic pause should land.

## What was tried and approved

A flat 2D "stickman" character animated as SVG shapes on an FK (forward-
kinematics) bone-like rig, driven entirely by hand-authored pose/timing
data in JavaScript (`assets/rig2d.js` + one `reel.html` per Reel), and
rendered to mp4 through this repo's existing `scripts/render_reel.py`
(a headless-Chromium seek-and-screenshot renderer that was already
proven for this repo's static/carousel content before this skill's
Reels work started).

## Why this won, specifically for this repo

- **Every animation principle became an explicit, authored number** —
  a windup angle, an easing curve, a 2-frame squash peak, a hold-frame
  count — rather than a retarget/interpolation default inherited from
  someone else's mocap clip. This directly targets the actual failure
  mode: motion that doesn't read as intentional.
- **It reused proven infrastructure** — the same headless renderer,
  brand CSS, audio mixing, and QA path this repo's other video content
  already used successfully, rather than introducing a new tool (Synfig,
  OpenToonz, DragonBones) with no established headless/scriptable
  automation story on this box.
- **No new install, no new licensing research, no new failure surface** —
  Chromium/Playwright and this repo's renderer already existed and were
  already trusted.

## Free/open-source alternatives considered, for when this reasoning
## *doesn't* hold (different repo, different constraints)

| Tool | Model | Automation fit | When it might actually be the better call |
|---|---|---|---|
| **Blender Grease Pencil** | Hybrid 2D-in-3D, bone/hand-drawn, free | High if the pipeline is already `bpy`-scripted (as `blender_studio`'s is) | A repo already built around headless Blender automation, where adding an HTML/SVG renderer would be the *new* dependency instead. |
| **Synfig Studio** | Vector, node-based, bone-rig tweening, free/OSS | Low-medium — CLI render exists, but rigs are normally hand-built once in its GUI | A one-off hero asset where a human animator builds the rig once and only rendering needs to repeat. |
| **OpenToonz / Tahoma2D** | Frame-by-frame traditional, free/OSS | Low — built for hand-drawn animation, not procedural generation | Highest quality ceiling, worst fit for a scripted overnight batch; only worth it if a human animator is actually in the loop per frame. |
| **DragonBones** | 2D skeletal (bones/slots/skins), free/OSS | Medium — structured export, but built for game runtimes, not video | Content that's *also* going to live as an interactive game asset, not just a rendered video. |

The general principle, not just this repo's specific answer: **prefer
whichever tool lets every animation-principle decision be an explicit,
inspectable number in code that a human or a future session can read and
adjust — not a default inherited from a retarget/interpolation step.**
That property, not "2D vs 3D" as such, is what actually predicts whether
the result reads as intentional.
