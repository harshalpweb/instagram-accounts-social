# nuvarel used-topics ledger

Anti-repetition rules (docs/nuvarel-strategy.md §3, revised 2026-09-05 for
the **2 posts/day** cadence — 1 carousel + 1 Reel; the strategy doc's §3
wording is canonical): a topic, material or object never re-runs within
60 days; a named palette/material is never reissued under the same name;
**no carousel pillar two days running; no Reel pillar two days running;**
Insider Knowledge sub-angles don't repeat within 30 days; a Two Objects
pair is never reused; **the same staged setup (object family + surface +
key) never recurs within 7 days across photographic pieces**, and the same
scene-set + hero-prop combination never recurs in a Reel within 14 days
(scene rule added 2026-08-31 after a real near-duplicate shipped to
review). Append one line per queued post. The 3x/day pillar-rotation
wording that lived here 2026-09-01..09-05 is superseded.

**Schema rule (Group CTO, 2026-08-31, slugs revised 2026-09-05):** the
Format column MUST be the exact `type` value from the post's queue JSON,
verbatim — current carousel slugs `the-evidence`, `two-objects`, `the-room`,
`palette-study`, `insider`, `mood`; Reel slugs `reel-satisfying`,
`reel-reveal`, `reel-game`, `reel-trend`. Older slugs below
(`reads-expensive`, `splurge-skip`, `the-rule`, older `reel-*`) are history
and still count for the 60-day topic check — never reclassify them. The
topic column carries every searchable keyword the post is about (a lamp
post must say "lamp" and "lighting" here, whatever pillar it filed under).
Cause: the 09-02 Reel was queued as `reel-splurge-skip` but filed here as
`the-rule`, so a "lighting" lookup returned a false clear and a visual
near-duplicate (09-04 lamps) queued 2 days behind it. One vocabulary, both
files, or the check is decorative. **Photographic pieces (from 2026-09-06)**
record in the scene cell: `photo: <subject/surface> · key=<dark|mid|light>
· seed=<n>` — the tonal rotation and the 7-day setup check both read it.

| Date | Post | Format (= queue JSON `type`) | Principle / palette / topic (all keywords) | Scene-set + props (Reels) / photo setup |
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
| 2026-09-05 | hotel-bed-rule | the-rule | hotel bed making; white bedding, linen, oversized duvet, foot layer, pillow stack; bedroom (moved Sep 3 -> Sep 4 10:00 in the 2026-09-01 pillar-rotation fix; moved again Sep 4 -> Sep 5 10:00 by Group CTO 2026-09-04 in the 2-Reels-plus-1-carousel cadence fix, Sep 4's one carousel slot already spent by palette-study-02; id keeps its date) | n/a (typography carousel) |
| 2026-09-03 | sofa-splurge-skip | splurge-skip | Splurge or Skip No. 03: sofa; hardwood frame, suspension, cushion fill; skip trend colour upholstery | n/a (typography carousel) |
| 2026-09-03 | palette-study-02 | palette-study | "Chocolate" palette (Palette Study No. 03: Warm Ivory / Bitter Chocolate / Toffee / Dried Olive); chocolate brown as 2026's top designer colour; dark-sits-low rule (moved Sep 4 -> Sep 3 10:00 in the 2026-09-01 pillar-rotation fix; id keeps its date) | n/a (typography carousel) |
| 2026-09-06 | texture-reads-expensive | reads-expensive | Why It Reads No. 03: why texture reads expensive when colour stays quiet; texture as shadow, light raking across boucle/cane/linen; three-textures-to-one-colour; texture at touching distance (moved Sep 4 13:30 -> Sep 6 10:00 by Group CTO 2026-09-04, same cadence fix; id keeps its date) | n/a (typography carousel) |
| 2026-09-04 | cables-read-cheap (REEL, 2D Curator) | reel-reads-expensive | cables, cords, wires, cable management, visible wiring, TV wall, wall-mounted screen, sideboard/console, wall socket, cable cover/channel painted to match the wall; "every visible wire is a line you did not choose" | MEDIA WALL (new set): wall-mounted screen + closed sideboard + wall socket; hero prop: four loose cables -> one channel cover |
| 2026-09-04 | bathroom-splurge-skip (REEL, 2D Curator) | reel-splurge-skip | Splurge or Skip No. 04: bathroom; SPLURGE heavy white towels all one weight, same fold; SKIP printed/patterned shower curtain, coloured towel set; plain curtain near the wall colour; towel rail; hotel-bathroom read | BATHROOM (new set): half-height tile, towel rail + three mismatched towels -> two white, shower rod + patterned curtain -> plain, mat |
| 2026-09-07 | the-state-foam-seat-cushion | the-state | The State No. 01: foam seat cushion press test (press it, count to three), compression set, support factor, sofa/seat cushion foam density, down cushion exception; series 'The State' (hands-free two-state comparison, distinct from The Inspection) -- row backfilled 2026-09-07 by Group CTO, the post was queued 2026-09-06 without one | photo: linen seat cushion on a dark wood table, brown wall · key=dark (measured 0.19-0.30) · seed=906601 (base) / 907101 (sunk composite) |
| 2026-09-07 | which-leather-is-real (REEL, photoreal stills cut, opened `photo_reel`) | reel-game | The Game No. 01: leather; full-grain vs bonded leather, polyurethane/PU faux leather, cut edge, suede back vs woven back, grain repeat vs irregular grain, sheen; sofa/armchair upholstery buying | photo: two square saddle-tan leather swatches on espresso ground · key=dark · seed=90807 (same seed for both swatches) |
| 2026-09-08 | the-vein-over-the-edge (ANIMATED CAROUSEL, one auto-play video via render_reel.py) | the-evidence | The Evidence No. 01: marble, natural stone vs marble-look porcelain tile, veining that carries over the edge, printed face vs plain body, through-body porcelain, etching (lemon/acid), slab/tile/countertop buying | photo: white Carrara marble block and slab on tan ground · key=mid (matted, alabaster) · seeds=1788721103 (hook, frames 2+3) / 1788721208 (macro, frames 1+3) |
| 2026-09-08 | turn-it-over (REEL, photoreal stills cut) | reel-reveal | The Reveal No. 01: ceramics, stoneware vs earthenware, unglazed foot ring, clay body colour (grey/buff vs chalky/orange), glaze, firing temperature, bowl/pot/vase buying | photo: glazed speckled stoneware bowl upright, then a low close view of the same bowl on its bare unglazed foot ring, tan ground · key=dark · seed=1788721773 (top/3 + inverted-v3-sameseed/2; the 2026-09-07 first cut on seed 1788721877 was withdrawn for a foot-geometry defect) |
| 2026-09-12 | crystal-or-glass (REEL, photoreal stills cut) | reel-game | The Game No. 02: crystal, glass, drinkware; cut lead crystal vs pressed glass; facet edges, mould seam line, prismatic refraction, rim-feel test; glassware/tableware buying | photo: two tumblers, A=faceted cut crystal (crystal/photo-912001-1.png) · key=dark · seed=912001; B=plain pressed glass (glass2/photo-912050-2.png) · key=dark · seed=912050 (different seed from A -- first glass attempt at seed 912001 rendered opaque/frosted, a material-fidelity fail per daily-build-prompt 5c, regenerated at a new seed emphasising transparency and passed) |
| 2026-09-12 | the-corner-gives-it-away (ANIMATED CAROUSEL, one auto-play video via render_reel.py) | the-evidence | The Evidence No. 02: solid wood vs veneer/laminate, wood grain continuity over a cut edge, table edge / drawer side inspection; furniture buying. Original subject for this slot was hand-cut dovetail joinery (seeds 912201/912301) — rejected at the Step 5c eyes-on pick, the model rendered a generic drawer front with no visible interlocking pins/tails, so the named evidence was not visibly what was in frame; subject swapped to wood-grain-over-the-edge, same mechanic family as the-vein-over-the-edge (marble) | photo: solid oak tabletop corner, grain flowing from top surface over the cut edge, tan/espresso ground · key=mid · seed=912401 (hook, hook2/photo-912401-2.png + silent hook2/photo-912401-1.png) / seed=912501 (macro, macro2/photo-912501-1.png + macro2/photo-912501-2.png) |

Withdrawn (kept for the 60-day check — the topic still counts as spent):

| Date | Post | Format | Topic | Why withdrawn |
|---|---|---|---|---|
| 2026-09-04 | lamps-over-chandeliers (REEL, pulled pre-publish) | reel-splurge-skip | lighting: lamps at eye level over a single overhead source (lamps, chandelier, pendant) | CCO 2026-08-31: same room set + lamp-pair advice as 09-02 rich-rooms-buy-two — visual near-duplicate 2 days apart. Replaced by curtains-hang-higher. Lamps/lighting stays spent for 60 days from 2026-09-02. |
| 2026-09-04 | curtains-hang-higher (REEL, pulled pre-publish) | reel-splurge-skip | curtain height and length; mount rod near ceiling, panels high wide floor-length; skip designer fabric | CCO 2026-09-01: near-verbatim repeat of published splurge-skip-01's full-height-curtains verdict (Aug 30) — the title-only ledger cell for splurge-skip-01 false-cleared it (schema backfilled same day). Curtains stay spent for 60 days from 2026-08-30. Sep 4 19:30 Reel slot left open for the Sep-4 daily run to fill with a clean topic. |
| 2026-09-01 | rugs-splurge-skip (carousel, pulled pre-publish) | splurge-skip | rugs; rug size over designer label; front-legs-on rule; seating-zone measuring | CCO 2026-09-01: near-verbatim repeat of published reads-cheap-01 principle No. 03 (floating rug / front legs / size up, Aug 30) — same title-only ledger false-clear as above. Rug topic stays spent for 60 days from 2026-08-30. Replaced by dining-splurge-skip same slot. |
