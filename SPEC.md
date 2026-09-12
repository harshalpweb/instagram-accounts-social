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
  the `meme-worthy-character-reels` skill).

## Acceptance criteria

- Behavioral changes have explicit requirements and verification criteria here before code changes.
- Tests or other observable checks demonstrate the implemented behavior.
- Status and overview records are synchronized after meaningful work.
