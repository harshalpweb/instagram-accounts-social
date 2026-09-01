# nuvarel used-topics ledger

Anti-repetition rules (docs/nuvarel-strategy.md §3/§7 — this header and
the strategy doc were reconciled 2026-09-01 by Group CTO after they had
drifted apart; the strategy doc's §3 wording is canonical): a principle,
palette, or rule never re-runs within 60 days; a named palette is never
reissued under the same name; **pillar rotation at 3x/day:** (a) no
pillar twice among the same day's three posts (carousel or Reel), (b) a
carousel pillar never occupies the same time-slot two days running (the
original 1x/day "never two days running" rule is arithmetically
unsatisfiable at 3 posts/day from 4 pillars and was reconciled, pending
founder ratification — see strategy §3); **the same scene-set + hero-prop
combination never recurs in a Reel within 14 days** (scene rule added
2026-08-31 after a real near-duplicate shipped to review). Append one
line per queued post.

**Schema rule (Group CTO, 2026-08-31):** the Format column MUST be the
exact `type` value from the post's queue JSON, verbatim (`palette-study`,
`reads-expensive`, `splurge-skip`, `the-rule`; Reels prefix `reel-`) —
never a free-text reclassification. The topic column carries every
searchable keyword the post is about (a lamp post must say "lamp" and
"lighting" here, whatever pillar it filed under). Cause: the 09-02 Reel
was queued as `reel-splurge-skip` but filed here as `the-rule`, so a
"lighting" lookup returned a false clear and a visual near-duplicate
(09-04 lamps) queued 2 days behind it. One vocabulary, both files, or
the check is decorative.

| Date | Post | Format (= queue JSON `type`) | Principle / palette / topic (all keywords) | Scene-set + props (Reels) |
|---|---|---|---|---|
| 2026-08-30 | palette-study-01 | palette-study | "The Quiet Greige" palette (Palette Study No. 01); greige, warm alabaster walls, umber dark wood frames, aged brass accents; 60-30-10 split; no chrome (keywords backfilled 2026-09-01 to current schema) | n/a (typography carousel) |
| 2026-08-30 | reads-cheap-01 | reads-expensive | Why It Reads No. 01: 5 things that read cheap — gloss vs matte finishes; single overhead light vs three light sources at three heights; RUG size, floating rug, front legs on the rug, size up; matching furniture set vs collected pieces; warm vs cool daylight bulbs, kelvin (keywords backfilled 2026-09-01 — title-only cell caused false clears) | n/a (typography carousel) |
| 2026-08-30 | splurge-skip-01 | splurge-skip | Splurge or Skip No. 01 where visible money goes — SPLURGE: light fixture, FULL-HEIGHT CURTAINS hung at ceiling touching floor, one oversized mirror; SKIP: cushion covers, decor objects, trays, vases; spend on what catches light (keywords backfilled 2026-09-01 — title-only cell caused false clears) | n/a (typography carousel) |
| 2026-08-31 | negative-space-01 (REEL) | reel-the-rule | negative space / visual quiet; shelf declutter | living room: shelf, sofa, lamp, art, plant (crowded-to-quiet) |
| 2026-09-01 | art-height (REEL, 2D Curator) | reel-the-rule | art hanging height (145 cm to centre); framed art; gallery wall | living room: sofa + framed art on wall |
| 2026-09-02 | rich-rooms-buy-two (REEL, 2D Curator) | reel-splurge-skip | symmetry / buying in pairs — a PAIR OF LAMPS flanking the sofa (lighting, lamps, cushions) | living room: sofa + two matching lamps |
| 2026-09-03 | one-big-thing (REEL, 2D Curator) | reel-the-rule | one large piece beats many small frames; scale; oversized art | living room: sofa + framed art on wall |
| 2026-09-01 | study-green-palette | palette-study | "The Study Green" palette (Palette Study No. 02); deep green, chalk cream, walnut, aged bronze; green-needs-warm-wood pairing rule | n/a (typography carousel) |
| 2026-09-01 | dining-splurge-skip | splurge-skip | Splurge or Skip No. 02: dining table; solid wood top vs veneer; skip designer dining chairs; right-sizing (daily four vs party eight); knock test (replaced rugs-splurge-skip 2026-09-01, see withdrawn) | n/a (typography carousel) |
| 2026-09-02 | black-anchor-rule | the-rule | one black element per room; black anchor; frames, lamp base, matte handles as the dark dose | n/a (typography carousel) |
| 2026-09-02 | hardware-reads-expensive | reads-expensive | hardware, handles, knobs, pulls, hinges, tap; unlacquered brass, aged bronze, matte black; one metal family per room | n/a (typography carousel) |
| 2026-09-04 | hotel-bed-rule | the-rule | hotel bed making; white bedding, linen, oversized duvet, foot layer, pillow stack; bedroom (moved Sep 3 -> Sep 4 10:00 in the 2026-09-01 pillar-rotation fix; id keeps its date) | n/a (typography carousel) |
| 2026-09-03 | sofa-splurge-skip | splurge-skip | Splurge or Skip No. 03: sofa; hardwood frame, suspension, cushion fill; skip trend colour upholstery | n/a (typography carousel) |
| 2026-09-03 | palette-study-02 | palette-study | "Chocolate" palette (Palette Study No. 03: Warm Ivory / Bitter Chocolate / Toffee / Dried Olive); chocolate brown as 2026's top designer colour; dark-sits-low rule (moved Sep 4 -> Sep 3 10:00 in the 2026-09-01 pillar-rotation fix; id keeps its date) | n/a (typography carousel) |
| 2026-09-04 | texture-reads-expensive | reads-expensive | Why It Reads No. 03: why texture reads expensive when colour stays quiet; texture as shadow, light raking across boucle/cane/linen; three-textures-to-one-colour; texture at touching distance | n/a (typography carousel) |

Withdrawn (kept for the 60-day check — the topic still counts as spent):

| Date | Post | Format | Topic | Why withdrawn |
|---|---|---|---|---|
| 2026-09-04 | lamps-over-chandeliers (REEL, pulled pre-publish) | reel-splurge-skip | lighting: lamps at eye level over a single overhead source (lamps, chandelier, pendant) | CCO 2026-08-31: same room set + lamp-pair advice as 09-02 rich-rooms-buy-two — visual near-duplicate 2 days apart. Replaced by curtains-hang-higher. Lamps/lighting stays spent for 60 days from 2026-09-02. |
| 2026-09-04 | curtains-hang-higher (REEL, pulled pre-publish) | reel-splurge-skip | curtain height and length; mount rod near ceiling, panels high wide floor-length; skip designer fabric | CCO 2026-09-01: near-verbatim repeat of published splurge-skip-01's full-height-curtains verdict (Aug 30) — the title-only ledger cell for splurge-skip-01 false-cleared it (schema backfilled same day). Curtains stay spent for 60 days from 2026-08-30. Sep 4 19:30 Reel slot left open for the Sep-4 daily run to fill with a clean topic. |
| 2026-09-01 | rugs-splurge-skip (carousel, pulled pre-publish) | splurge-skip | rugs; rug size over designer label; front-legs-on rule; seating-zone measuring | CCO 2026-09-01: near-verbatim repeat of published reads-cheap-01 principle No. 03 (floating rug / front legs / size up, Aug 30) — same title-only ledger false-clear as above. Rug topic stays spent for 60 days from 2026-08-30. Replaced by dining-splurge-skip same slot. |
