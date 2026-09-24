# September 25 Instagram release review

Status: media prepared and checked; `approved: false` prevents publishing. The workflow is manual dispatch only.

## Live account identities

| Internal key | Verified public username | Posts |
|---|---|---|
| harshal | @harshalbuilds | The send button is a boundary; A three-line task contract; One word reversed the decision |
| anime | @anime.ekaya | The saved place in the rain; Four watch-night reactions; Just one episode |
| nuvarel | @nuvarel_ | The edge changes the silhouette; Before you choose a side table; Tape the handle first |

Two latest live Reels per account were inspected on September 25. The new package replaces the repeated pale-background object template with illustrated stories, a saveable native carousel, and a different motion treatment per account. Current local analytics stop before the recent batch, so no reach improvement is claimed.

## Quality and truthfulness

- Six H.264/AAC Reels: 1080 × 1920, 9.9 seconds. Fifteen JPEG carousel slides: 1080 × 1350. All 21 release asset hashes match.
- First, middle and final Reel frames and all carousel slides were visually reviewed at phone size. The review corrected missing carousel symbols, low-contrast footers, an unclear furniture mockup, and a repetitive furniture crop.
- Captions and on-screen copy passed the local copydesk checks. The AI note is a scripted example. The anime stories use original characters and illustrations. The furniture images are editorial concepts, with no product performance claim.
- Audio is embedded from the repository's licensed Mixkit kit; standalone licensed files are absent from this public release.
- Publisher pins the nine exact media hashes, verifies account usernames, reconciles existing matching captions, checks publication receipts, and verifies live permalinks. There is a two-minute minimum gap per account and a three-wave order.

## Source

Production files and QA are in `content_studio/jobs/2026-09-25-distinct-voices/` in the shared workspace. Captions and asset hashes are in `release.json`; release media is in `media/`.

## Publication gate

Root `AGENTS.md` requires confirmation immediately before Instagram posts. After that confirmation, set `approved: true`, place this release on `master`, manually dispatch `publish-2026-09-25-distinct-voices.yml`, and monitor the receipts and nine live permalinks.

