# Nuvarel — home-décor niche viral-Reel research (2026-09-12)

**Written by:** CoS (income-engine), founder-requested live session.
**Relates to:** `docs/nuvarel-strategy.md` (the account's actual committed
strategy — quiet-luxury "proof, not the claim," photoreal evidence stills,
no character, 2 posts/day). **This document does not replace that
strategy.** It answers a narrower question the founder asked directly:
in the broader home-décor/interior-design niche, what makes a Reel from a
small, unknown account reach 10M+ views, and is any of that mechanic worth
borrowing. Read `nuvarel-strategy.md` first for the account's actual
positioning; treat this as input to weigh against it, not a new mandate.

---

## 1. Method: how this research was done

Access was via `agent-browser` (a CLI browser-automation tool, CDP-based,
no Playwright/Puppeteer dependency — see `agent-browser skills get core`)
driving a real, separately-authenticated Chrome session, logged in via the
founder's own Instagram cookies (exported once via the "Cookie-Editor"
Chrome extension, JSON format).

**Cookie-import gotcha (agent-browser 0.37.1, Windows):**
`cookies set --curl <file>` (the documented bulk-import path) silently
imported zero cookies from a Cookie-Editor JSON export on this version —
it reported success but the session stayed logged out. Root cause,
confirmed by isolating flags one at a time:

- `agent-browser cookies set <name> <value> --domain <host> ...` fails
  with `CDP error (Network.setCookies): Invalid cookie fields` whenever
  `--domain` is combined with `--path`, or `--domain` is used at all
  alongside `--secure`/`--sameSite` in some combinations.
- **Working fix:** set each cookie individually using `--url
  https://www.instagram.com` instead of `--domain`/`--path`, keeping
  `--secure`, `--httpOnly`, `--sameSite <Strict|Lax|None>` and `--expires
  <unix ts>` as needed. Omit `--path` entirely when the source cookie's
  path is `/` (Chrome's default).
- Cookie-Editor's JSON export uses `expirationDate` (Unix seconds) and
  `sameSite` values `no_restriction|lax|strict|unspecified` — map these to
  `--expires` and `Strict|Lax|None` respectively before calling
  agent-browser; its own field names don't match agent-browser's flags
  directly.
- The critical cookie for a logged-in session is `sessionid` (plus
  `ds_user_id`). A partial cookie export that's missing `sessionid`
  (Instagram sets it `httpOnly`+`secure`; some export configurations skip
  it) leaves you looking logged-in-adjacent but still on the login page —
  check for it by name before assuming an export is complete.

**Limitation:** Instagram's web UI does not expose an exact view/play
count for a Reel to a non-owner, only likes, comments, and shares. Where
this document says a post "likely clears 10M views," that is an estimate
from the like count using a common Reels like-to-view ratio (roughly
2-5%), not a directly observed number — flagged explicitly wherever used,
per this portfolio's own numbers-must-be-sourced-or-bounded standard.

---

## 2. What was checked

Explored `#interiordesign` and `#homedecor` (Top tab) via
`instagram.com/explore/tags/<tag>/`, opened the highest-engagement Reels,
and read each account's profile (follower count, bio, content mix).

| Account | Followers | Likes (top Reel) | Est. views | Content type |
|---|---|---|---|---|
| `the_designdomain` | 74.7K | 3.6M | likely well over 10M (proxy) | Real renovation-in-progress footage, trending audio, one-line caption |
| `furkanozlermimarlik` | 93.6K | 4.8M | likely well over 10M (proxy) | "Before / After" room transformation, near-blank caption, trending audio |
| `mai_saad_designs` | not checked | 758K | unconfirmed vs. 10M bar | Polished luxury CGI-adjacent interiors, hashtag-heavy caption |
| `iz_designs` | not checked | 748K | unconfirmed vs. 10M bar | 3D-rendered/animated interior showcase (not real photography) |
| `designswithkhushi` | not checked | like count not visible | unconfirmed | Text-overlay "tip" format ("Don't let empty corners go to waste") |
| `arq.andreach` | not checked | 18.7K | well under 10M | Text-overlay hot-take/trend format ("Beige era is over") |
| `ammar_builders1` | not checked | 474K | unconfirmed | Real-estate listing/ad style |
| `444leafhome` | not checked | 241K | unconfirmed | Cozy room-tour style |

Only the first two are asserted as clearing the 10M-view bar (via the
like-count proxy above); the rest are recorded for format diversity, not
as confirmed 10M+ examples.

---

## 3. The core finding

**Follower count and view count were completely decoupled for the top
two accounts.** Both sit under 100K followers yet each produced a single
Reel that plausibly reached tens of millions of views. That only happens
when Instagram's Reels ranking pushes a clip to non-followers at scale —
it is a property of the *video*, not the account's existing audience.

Common traits across the two confirmed viral clips:
1. **Visual, not verbal, hook.** A real space changing state (mid-reno,
   or a hard cut from "before" to "after"). No voiceover explains it.
2. **"Before / After" as a structural device**, not just a caption word —
   it gives the viewer a reason to watch to the end, which Reels ranking
   rewards with more distribution.
3. **Real footage, not styled photography or CGI** — the lower-performing
   CGI account (`iz_designs`) and styled-luxury account (`mai_saad_designs`)
   sit an order of magnitude below on likes, though the CGI account also
   has a smaller absolute reach ambition (interior-viz service, not a
   growth play).
4. **Trending audio over voiceover** on both top clips.
5. **Minimal caption** — one line plus hashtags, sometimes nothing at all.

---

## 4. Weighed against nuvarel_'s actual strategy

`nuvarel-strategy.md` deliberately targets a narrower, higher-intent
audience (28-45, post-purchase-decision window, US/UK/UAE/Singapore/
Australia + metro India) with photoreal *evidence* content and explicitly
**no character/mascot** and **no mass-virality volume play** (2 posts/day,
reduced further as followers grow — the founder's own comparables,
Studio McGee/Becki Owens/Alyssa Kapito, grew on curation, not volume).

That means this research's format (raw Before/After renovation reels
optimized for anonymous mass reach) is **not a drop-in replacement** for
nuvarel's current content pillars — it's a different growth mechanic
(algorithmic mass-reach) aimed at a different audience (broad home-decor
interest, not high-intent affluent buyers). Two ways it could still be
useful without contradicting the existing strategy:

- **A distinct top-of-funnel Reel pillar**, clearly separated from the
  evidence/proof carousels, using real (not styled) footage of an actual
  renovation or install with a hard Before/After cut and trending audio —
  kept to real, unstaged footage to stay consistent with "the proof, not
  the claim."
- **Format signal, not audience signal**: adopt the *mechanic* (visual
  hook, before/after structure, minimal caption, trending audio) on
  content that still shows genuine material/quality evidence, rather than
  importing the mass-market meme register wholesale.

**Recommendation, not a decision:** this needs a CCO read before it
changes anything in `nuvarel-strategy.md` itself, the same way the
2026-09-05 revision did — that document's own dissent-and-revision history
shows format changes here get real pushback and should route through
that process, not get bolted on unilaterally from this research alone.

---

## 5. Roster feedback

New pattern for the observation log: Cookie-Editor JSON exports need
field-name translation before `agent-browser cookies set` will accept
them, and `--domain`+`--path` together trips a CDP validation error that
`--url` alone avoids. Worth a reusable helper script if agent-browser
cookie-import gets used again for any other account's research.
