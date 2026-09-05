# Stock video licensing record

Same rule as `assets/audio/ATTRIBUTION.md`: log the source at copy time,
it cannot be reconstructed later. Raw clips are **gitignored**
(`assets/video/**/*.mp4`) because these repos are public and every free
stock licence below permits use *inside* a rendered post but not
redistribution of the raw file as a standalone asset. Commit the record,
never the clip.

## Per-source licence terms (verified at the source, not by reputation)

**Pexels License** — https://www.pexels.com/license/ (read 2026-09-05).
Verbatim from that page: "All photos and videos on Pexels are free to use.
Attribution is not required." Explicitly allowed: "Use the photos and
videos online … Share them on social media … Facebook, Instagram or
YouTube." Not allowed: "Don't sell unaltered copies of a photo or video";
"Don't imply endorsement of your product by people or brands on the
imagery"; "Don't redistribute or sell the photos and videos on other stock
photo or wallpaper platforms"; "Identifiable people may not appear in a bad
light." Terms of Service §7B (https://www.pexels.com/terms-of-service/,
read 2026-09-05): contributors "will not upload Content … created with
generative AI technology" — but Pexels "makes no warranty … that all
Content is human-produced." So a real-footage claim still needs per-clip
evidence (upload date, photographer track record, eyes-on review).
ToS §9 bans scraping/automated collection; for ongoing sourcing use the
official Pexels API (free key, needs an account: founder-reserved auth),
not page fetches.

## stock/ (Pexels License)

| file (local-only) | original title | photographer | Pexels URL | uploaded | licence | used in |
|---|---|---|---|---|---|---|
| pexels-10527016-touching-the-marble-surface-hd_1080_2048_25fps.mp4 | Touching the marble surface | Ron Lach (pexels.com/@ron-lach) | https://www.pexels.com/video/touching-the-marble-surface-10527016/ | 2021-12-12 (pre-dates generative video; real footage) | Pexels License, free commercial use, no attribution required, no standalone redistribution | nuvarel "The Inspection" review sample, 2026-09-05 (`accounts/nuvarel/render/out/inspection-stock-sample-2026-09-05/`, local-only, not queued) |

Use-case check for this repo (public repo + commercial Instagram account):
posting a graded/composited cut on Instagram is an expressly listed
permitted use; the clip is modified (trim, crop, grade, type overlay), so
the "unaltered copies" clause does not bite; no identifiable person (hand
only); no brand/endorsement implied. The only conflict is redistribution
of the raw file, which the gitignore handles.
