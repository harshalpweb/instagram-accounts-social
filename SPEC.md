# instagram-accounts-social specification

## Purpose

Registry: instagram_accounts_social

## Product contract

This file is the canonical contract for behavior, interfaces, architecture, data, and user-visible design in `instagram-accounts-social`. Replace inferred statements with verified project-specific requirements as development proceeds.

## Scope

- Preserve the capabilities and constraints documented in the project README, registry, tests, and active design documents.
- Record new behavior and design decisions here before implementation.
- Keep implementation, tests, and this specification consistent.

## Architecture and interfaces

Document stable components, entry points, dependencies, storage, external systems, and public interfaces before changing them.

### Instagram API access modes (binding)

Two, and only two, sanctioned ways to reach Instagram from this repo:

1. **Write path** — `scripts/publish_due_posts.py`, Graph API container
   create + publish, per-account token. The only code that writes.
2. **Read path** — `scripts/collect_insights.py` (per-media) and
   `scripts/account_diagnostics.py` (per-account). GET only.

`scripts/account_diagnostics.py` answers questions per-media insights
structurally cannot: it reads profile fields (`biography`, `account_type`,
`followers_count`) and `GET /me/insights` with the documented `follow_type`
(FOLLOWER / NON_FOLLOWER / UNKNOWN) and `media_product_type` breakdowns.
The follower/non-follower reach split is the only direct measurement of
whether an account is receiving recommendation (Reels-tab/Explore)
distribution at all, as opposed to reaching only its existing followers.
It additionally reads `GET /me/media` (timestamps, to expose how dormant a
revived account was and how much unrelated history Instagram has already
modelled for it) and `follower_demographics` (Meta returns this only above
100 followers, so it is expected to fail on the purpose-built accounts --
that failure is information, not a defect).
Run via the `Account diagnostics (read-only)` workflow, manual dispatch only.

**Logged-in/cookie-session access to Instagram is out of scope for this
repo** — not merely unused, but excluded. Any capability that needs it
(profile/bio edits, Account Status, hashtag-surface checks) is a
founder-executed manual step, not something this pipeline automates.

## Constraints

- Do not invent credentials, deployment status, financial claims, or external-service guarantees.
- Follow root portfolio governance and the subproject's local instructions.
- Treat existing tests and documented contracts as binding until this specification deliberately changes them.

## Character rig files (binding)

- `assets/rig2d.js` — the shared, multi-account 2D stickman rig (math/DOM
  helpers plus the `makeStick`/`poseStick`/`P` pose vocabulary), used
  across `hype_tingles`/`anime_ekaya`-style builds.
- `accounts/nuvarel/assets/curator.js` (added 2026-09-13, **rewritten same
  day**) — a **dedicated, account-local** rig for nuvarel's Curator
  character. The first version ("Curator Mk II": 8.5-head proportions, no
  face, tapered filled limbs, an overcoat garment silhouette) was rejected
  by the founder outright ("the earlier stickman was better than this, it
  just needed some refinement") and is superseded —
  `docs/visual/nuvarel-curator-mk2.md` records that spec as history only,
  marked SUPERSEDED/REJECTED at the top. The current file goes back to the
  original `assets/rig2d.js` skeleton (4.58 heads tall, same `L` values)
  with only light, targeted changes on top: face restored (dot eyes), a
  small amount of limb taper, small rounded hand/foot dots instead of bare
  line-ends, and nuvarel's own taupe/bronze palette
  (`docs/nuvarel-strategy.md` §8) plus a small bronze belt accent.
  **Must not be merged into `assets/rig2d.js`** — the original Curator's
  failure was exactly a rig reused across accounts (hype_tingles' meme
  stickman) standing in for a bespoke wealth-signalling figure; a future
  account-specific character gets its own file the same way, not a fold
  into the shared one. **Reinstated for production use 2026-09-13**
  (Group CTO, founder-direct): the no-mascot ruling in
  `docs/nuvarel-strategy.md` §"Second revision" is superseded for the
  **illustrated** lane, and §8's claim that the rule was "a hard platform
  constraint" is struck as factually wrong — Instagram's 2026-08-31 rule is a
  profile-level toggle for profiles featuring an AI-generated *person*, and
  this file is hand-written deterministic SVG geometry, not generated output.
  The photoreal lane's no-people rule is unchanged. Ruling:
  `../docs/consults/2026-09-13-group-cto-nuvarel-press-test-character-and-medium.md`.

  Two optional fields added 2026-09-13, both **default-off so every existing
  pose renders byte-identically**: `shoulderW` (pose field — arms originate at
  ±shoulderW perpendicular to the torso instead of both leaving the single
  neck point, plus a drawn clavicle; the shared rig has no shoulder width
  because it was built for SIDE views, and head-on two arms from one point
  read as a tripod) and `belt: false` (opts — hides the bronze waist accent,
  needed when a shot puts the hip at a prop's surface line and the accent
  reads as a stray mark on the prop).

  **Binding IK note for any two-handed action with this rig.** The arm bones
  are 95 and 88 — near enough to equal that a hand target at about 73% of full
  reach throws the elbow ~90px sideways, and two of those plus a torso close
  into a diamond that reads as a scarecrow rather than a person. Any reel
  driving this rig with 2-bone IK must apply a **minimum-extension clamp**
  (push a near target out along the same shoulder-to-target line, at about 97%
  of full reach), not per-frame pose corrections. Reference implementation:
  `accounts/nuvarel/reels/2026-09-13-the-press-test/reel.html`, `MIN_REACH`.

## Content format vocabulary (queue JSON `type`)

Each account's queue JSON `type` is free text, `carousel-*` or `reel-*`
prefixed so `scripts/collect_insights.py`'s family grouping works. New
type strings get added here as they ship rather than only living in a
ledger row.

- `hype_tingles`: `carousel-one-star-files`, `carousel-masterclass`,
  `carousel-panel`, `carousel-solo-panel` (added 2026-09-12: the
  masterclass mechanic re-cast as a single-speaker cat monologue, same
  `speaker` visual role as `carousel-panel`, so the featured character
  is on screen every slide instead of only the payoff), `reel-breaking-news`,
  `reel-hold-and-judge` (a persistent on-screen character nudges a hero
  prop toward a table edge across escalating text cards; the character
  and prop are chosen per build, engine in
  `accounts/hype_tingles/reels/*/reel.html` reused verbatim per build per
  the `meme-worthy-character-reels` skill; build 02, 2026-09-12, swapped
  the hero prop phone -> piggy bank so a fresh scene/prop pair satisfies
  the 7-day no-repeat rule without depending on the 7-day boundary).
- `nuvarel`: `reel-reads-expensive` (the account's best-performing format —
  `2026-09-04-cables-read-cheap`, 1,091 reach — a 2D Curator working on a room
  prop while overlay cards name why it reads cheap or expensive),
  `reel-press-test` (added 2026-09-13: two identical Curators perform an
  identical named test on two visually identical objects whose only difference
  is hidden, and a bronze datum line plus a measured residual give the verdict,
  so the viewer reads a measurement instead of eyeballing a difference. Engine
  in `accounts/nuvarel/reels/2026-09-13-the-press-test/reel.html`; the
  deformable-object model there — rest crown, global compression plus a
  flat-bottomed palm dish, side bulge, a piping seam through the same
  deformation field, depth-tracked creases, and occlusion by draw order — is
  the reusable part and generalises to any A/B physical test on this account.
  PREVIEW as of this commit: not queued, `content/queue/` untouched).
- `anime_ekaya`: `reel-show-converter` (a mainstream, non-anime show/game/
  film "converted" into an anime pick via a shared CONVERTER-machine rig,
  EKAYA pulls a lever, an anime title pops out; engine in
  `accounts/anime_ekaya/reels/2026-09-04-show-converter/reel.html`, reused
  verbatim per build and reskinned per theme -- colour palette + a
  hero-prop deco on the machine top -- so repeat builds don't share a
  backdrop/prop combination inside the 14-day scene/prop window;
  `content-reviewer`'s external-facts check caught an overstated real-world
  purpose-claim in the first `2026-09-12-gamer-converter` build -- "built
  as a tribute to" read as settled authorial intent where the primary
  source only supported "widely credited as an influence." Any card
  naming a real creator's intent behind a real work needs the creator's
  own words checked, not just enthusiast-press consensus, which tends to
  run hotter than the source).

## Visual quality gate (binding, added 2026-09-13)

`scripts/frame_gate.py` is a deterministic still-frame floor: p99-p1 luminance
range, contrast (stddev), dark-pixel fraction and mean saturation, with
deliberate solid title/end cards auto-detected and skipped so the gate cannot be
argued past. It exits non-zero below the bar.

- **Thresholds are calibrated on a measured known-good artifact**, never
  guessed. The `nuvarel` profile is measured on the 41 committed QA frames of
  `2026-09-04-cables-read-cheap`. A guessed saturation floor of 0.15 was
  proposed and would have failed that very post (measured median 0.081); the
  calibrated floor is 0.04, with a ceiling of 0.35 because
  `docs/nuvarel-strategy.md` §8 makes over-saturation a brand failure too. Any
  new profile must cite the artifact it was measured on.
- **Run it on stills BEFORE rendering a sequence**, then again on the
  `--qa-dir` output afterwards. Wired into `docs/cadence-and-format-policy.md`
  §5 as item 3.
- **It is a floor, not a verdict.** Passing says nothing about whether a piece
  is good. `art-director`'s eyes-on comparison at about 350px feed scale still
  decides that, and on the build that introduced this gate the eyes-on pass is
  what caught a dead first 2.2 seconds and sub-copy too small to read — both
  invisible at full resolution, both passing the gate.

## Acceptance criteria

- Behavioral changes have explicit requirements and verification criteria here before code changes.
- Tests or other observable checks demonstrate the implemented behavior.
- Status and overview records are synchronized after meaningful work.
