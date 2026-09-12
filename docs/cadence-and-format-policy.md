# Cadence, format mix, posting times, hooks and CTAs — all accounts

**Authority:** Group CTO, 2026-09-12, on a founder-direct instruction relayed
and confirmed through the CoS. Applies to **every** account in this repo
(`nuvarel`, `anime_ekaya`, `hype_tingles`, and every account onboarded later),
regardless of niche.

**This file is canonical.** Each account's
`accounts/<acct>/docs/daily-build-agent-prompt.md` restates the operative
numbers so a build agent never has to follow a pointer mid-run (hard rule 6:
the prompts are architecture). If a prompt and this file ever disagree, this
file wins and the prompt is a bug — fix it in the same commit.

**Machine-readable half:** `docs/slot-policy.json` (the numbers) and
`scripts/plan_day.py` (the computation). A rule that only exists as prose in
three prompt copies is a rule that drifts; these two files are the enforcement.

---

## 0. Why this exists — the evidence

Measured 2026-09-12 from `analytics/insights.csv` (61 posts, 2026-08-30 to
2026-09-10, all three accounts, `status: ok`):

| Account | Format | n | mean reach | mean views | mean interactions |
|---|---|---:|---:|---:|---:|
| anime_ekaya | CAROUSEL_ALBUM | 11 | **1.7** | 4.6 | 0.82 |
| anime_ekaya | VIDEO (Reels) | 9 | **191.3** | 220.9 | 3.00 |
| nuvarel | CAROUSEL_ALBUM | 12 | **2.9** | 6.8 | 1.25 |
| nuvarel | VIDEO (Reels) | 9 | **174.9** | 192.9 | 2.11 |
| hype_tingles | CAROUSEL_ALBUM | 11 | 5.0 | 15.7 | 0.09 |
| hype_tingles | VIDEO (Reels) | 9 | 4.2 | 6.8 | 0.89 |

Reels out-reach carousels by roughly **60x on nuvarel and 110x on
anime_ekaya**. The standing rule until today was a fixed "2 carousels +
1 Reel per day" on two of the accounts. That ratio was set before any
performance data existed and was never revised when the data arrived. This
policy removes the possibility of that happening again by computing the mix
from the data every single day.

Lifetime account totals over the same 61 posts, for scale, and stated plainly:

| Account | reach | likes | comments | saves | shares | follows* |
|---|---:|---:|---:|---:|---:|---:|
| anime_ekaya | 1,741 | 29 | 0 | 2 | 5 | 0 |
| nuvarel | 1,609 | 22 | 5 | 2 | 5 | 0 |
| hype_tingles | 93 | 9 | 0 | 0 | 0 | 0 |

\* `follows` and `profile_visits` are only requested for FEED media by
`scripts/collect_insights.py` (`EXTRA_METRICS`), so "0 follows" is measured
for carousels and **unmeasured** for Reels. Do not read it as a proven zero
across the account.

Two conclusions the rest of this file is built on:

1. **The format question is settled for nuvarel and anime_ekaya** and *moot* for
   hype_tingles, whose two formats are statistically indistinguishable because
   *nothing* on that account reaches anyone. That is an account-level
   distribution problem and no format rule fixes it.

   **Diagnosed and closed 2026-09-12 (Group CTO).** Measured with
   `GET /me/insights?metric=reach&breakdown=follow_type` over 29 days:
   hype_tingles reached **12 non-follower accounts**, against **1641**
   (anime_ekaya) and **1541** (nuvarel). The difference is the follower graph,
   not the content: hype_tingles is the only account with a real one (282
   followers) and it is dead — 9 of 282 reached in a month. The other two have
   4 and 7 followers, so Instagram routes their Reels straight onto the
   cold-start exploration path instead of seeding them into a graph that
   cannot respond. A small dead follower graph is worse than none.
   Refuted along the way, each with evidence: encoding (ffprobe shows all 27
   Reels identical at 1080x1920/30fps/AAC), dormancy (nuvarel was dormant
   *longest* — 283 days — and performs best), the 2026-08-31 AI-profile policy
   (nuvarel posts `ai_generated: true` and tops the table), and content
   quality (hype_tingles' watch times *beat* anime_ekaya's).
   Ruling: the content line moves to a fresh account; hype_tingles keeps
   publishing meanwhile because a dark slot costs more than it saves. Full
   record: `../../docs/consults/2026-09-12-group-cto-hype-tingles-distribution-diagnosis.md`.
2. **The quality problem is real and is not a format problem.** 3,443 lifetime
   reach produced 60 likes, 5 comments, 4 saves and 10 shares across three
   accounts. Section 5 is the response.

---

## 1. Cadence floor — 3 posts a day until 50,000 followers

**Founder ruling, 2026-09-12.** Every account posts **3 times a day, every
day, without fail**, until it passes **50,000 followers**. The count does not
flex. Only the format mix inside those 3 slots flexes.

- Encoded: `docs/slot-policy.json` → `cadence`.
- A slot whose production lane is closed (nuvarel's `build-gates.json`) or
  whose build fails is a **`BUILD-INCIDENT.json` entry**, not a silent drop to
  2 posts. The incident names the slot and the reason.
- The old per-account cadences (nuvarel 2/day from 2026-09-05; anime_ekaya
  1 carousel + 3 Reels from 2026-09-06) are **superseded**. `nuvarel-strategy.md`
  §7 is superseded by this section; that doc carries the pointer.
- Revisit at 50,000 followers, not before. "Volume is a downmarket signal"
  (the 2026-09-05 rationale for cutting nuvarel to 2/day) is a plausible claim
  about a *mature* account; it cannot be tested on an account with single-digit
  followers, and the founder has ruled on the growth phase.

## 2. Format mix — computed daily, never a fixed ratio

Run **first, before choosing topics**:

```
py -3 scripts/plan_day.py --account <acct>            # today
py -3 scripts/plan_day.py --account <acct> --json     # machine-readable
```

It returns 3 slots, each with a format (`REELS` or `FEED`) and a time, plus the
evidence it used. **Build exactly what it returns.** If you think it is wrong,
say so in the commit message and in your final report — do not quietly build
something else.

How the mix is decided (`scripts/plan_day.py`, `docs/slot-policy.json`):

- **Metric:** mean `reach` per format over a trailing **21 days**, from
  `analytics/insights-history.csv`, deduplicated to one row per post (the file
  is append-only; a naive mean over it weights posts by how often they were
  collected). Reach is the metric because it is the only one with a usable n —
  likes/comments/saves are 0-5 lifetime per account. **Switch the metric to
  saves + sends once any account clears ~50 lifetime saves**, because those are
  the signals Instagram actually ranks on (section 3).
- **Smoothing:** the mean is shrunk toward the account's overall mean with a
  prior weight of 3, so one freak post at n=1 cannot capture the day. The
  `cables-read-cheap` outlier (1,091 reach against a same-day sibling's 110) is
  exactly the shape this guards against.
- **Demotion:** a format scoring below **25%** of the leader loses its standing
  slots. Today that demotes FEED on nuvarel and anime_ekaya, and demotes
  nothing on hype_tingles.
- **Exploration (the part that matters most):** every **7th day**, one slot is
  forced back to the demoted format. Without this, a demotion is
  self-fulfilling — a format that is never posted is never re-measured, so the
  account can never learn that the format recovered, or that the real cause was
  the topic rather than the format. The planner marks that slot `[explore slot]`.

Worked output, nuvarel, 2026-09-13, from live data:

```
slot 1  11:04 IST  REELS  (window morning 09:40-11:20)
slot 2  15:14 IST  REELS  (window afternoon 14:10-16:00)
slot 3  20:52 IST  FEED   (window evening 19:05-21:15)  [explore slot]
evidence: smoothed mean reach over 21d: REELS=150.32 (n=9), FEED=17.66 (n=12)
demoted: FEED
```

**Format is not the same as pillar.** The planner picks `REELS` or `FEED`; the
account's own pillar rotation and anti-repetition ledger still choose *which*
Reel or *which* carousel. Nothing in this section relaxes the 60-day topic rule
or the 7-day scene/prop rule.

## 3. What the platform actually ranks (2026), and what it means here

Verified 2026-09-12 at secondary sources reporting Instagram's own statements;
flagged as secondary because Mosseri's year-end memo is an Instagram carousel
post, not a document with a citable permalink through these tools:

- The confirmed top ranking signals are **watch time, sends per reach (DM
  shares), and likes per reach** — likes weakest of the three. Sends are widely
  reported as carrying roughly **3-5x the weight of likes** for Reels
  distribution.
- Watch time replaced the fixed 3-second view threshold; total watch time plus
  replay rate is what counts.
- Benchmark studies for 2026 put Reels at roughly **4.7x the median reach** of
  other formats and **~8x follower acquisition**, while carousels hold
  **~2.3x the save rate** and **~1.8x the comment depth**. The commonly
  recommended mix is 60-70% Reels, 20-30% carousels. **Our own data is far more
  lopsided than that benchmark**, which is why section 2 computes the mix from
  our numbers rather than adopting the benchmark ratio.
- Mosseri's 2025-12-31 year-end memo declared the "polished, perfect aesthetic
  is dead" and said Instagram will weight authenticity and provenance more
  heavily through 2026.
- **Separately and narrowly:** from 2026-08-31 Instagram limits the reach of
  profiles *featuring AI-generated people* that are not labelled. It does not
  penalise a creator for using AI to generate graphics, edit photos or write
  captions. This matches Group Legal's 2026-09-05 read exactly; nothing in the
  new research changes it. `is_ai_generated` on a container is a per-post
  disclosure and is **not** the profile-level label.

Operational consequences, all accounts:

1. **Optimise for a send, not a like.** Every piece answers "who would a viewer
   forward this to, and why?" before it is built. If there is no answer, the
   concept is weak — that is a `creative-director` FAIL, not a nice-to-have.
2. **Watch time is a build constraint.** A Reel that front-loads its payoff has
   no watch time. Structure is hook → tension → payoff, payoff last.
3. **Provenance is now a strategic axis, not only a compliance one.** See
   `docs/nuvarel-strategy.md` §9 for the ruling on what this means for an
   account built entirely on generated imagery.

## 4. Hook and CTA policy

**Founder correction, 2026-09-12:** do not force a hook *and* a CTA onto every
post — a CTA on everything reads forced and cheap. The hook is always required;
the CTA is conditional. Concrete rule:

### 4.1 The hook is mandatory on every piece, with no exceptions

- Frame 1 / second 1 must open a **curiosity gap**. It must not state the
  verdict, the format name, or the conclusion.
  Evidence, this account set, 2026-09-05: `cables-read-cheap` ("the cheapest
  thing in an expensive room", withholds the answer) reached 1,091 against
  `bathroom-splurge-skip` ("splurge or skip: the bathroom", states the format)
  at 110, same day, same slot, same craft.
- ≤ 7 words on a carousel frame 1. Spoken or on-screen in a Reel's first second.
- **`content-reviewer` fails a piece whose hook states its own payoff.** This is
  now a defect, not a note.

### 4.2 Every queued piece declares a `goal`

Add one field to the queue JSON, alongside `type`:

```json
"goal": "save" | "share" | "comment" | "dm" | "mood" | "entertain"
```

The goal is chosen when the topic is chosen, not retro-fitted to justify a CTA.

### 4.3 The CTA rule

| `goal` | CTA | Shape |
|---|---|---|
| `save` | **required** | One line, phrased as future utility for the viewer. "Save this for the next showroom." Never "save this post!" |
| `share` | **required** | Names the person, not the action. "Send this to whoever picked the sofa." |
| `comment` | **required** | Asks one answerable question with a real answer. Never "thoughts?" |
| `dm` | **required** | Keyword-comment mechanic only (section 6). Names the keyword and what arrives. |
| `mood` | **forbidden** | The piece ends on the image or the line. No closer slide, no ask. |
| `entertain` | **forbidden** | The joke is the ending. A CTA after a punchline kills it. |

Ceilings, per account:

- **At most 2 of the 3 daily pieces may carry a CTA.** At least one piece a day
  is `mood` or `entertain` and ends clean. Enforced at review by
  `content-reviewer` across the day's queue, not per piece.
- **The same CTA verb may appear at most 3 times in any 7 days.** "Save this"
  three days running is the same robotic tell as a fixed clock time.
- A CTA never appears on frame 1 and never appears twice in one piece.

Encoded: `docs/slot-policy.json` → `hook_cta`.

## 5. The quality bar — the ratchet, not a sentence

**Founder, 2026-09-12: quality is currently poor; only 1-2 posts per account
have performed well.** Measured, that is accurate: 2 of 61 posts hold 59% of
all lifetime reach. The response is a *mechanical bar*, because every previous
attempt at this was a policy sentence that a passing automated check then
overrode.

Three changes, all live as of this commit:

1. **`content-reviewer` gains a quality floor** (charter, "The quality floor").
   Today the role fails *defects*. A piece can be defect-free and still be
   mediocre, and mediocre is what shipped 59 times. The floor is a **forward
   verdict**, answered in writing before PASS: *would this stop a stranger's
   thumb, and who would they send it to?* An answer of "nobody in particular"
   is a FAIL with reason `weak-concept`, referred to `creative-director`.
2. **`art-director` gains the comparison test** (charter, "The comparison
   test"): the piece is looked at at ~350 px **beside a real, currently-live
   competitor post in the same niche**, not in isolation. Every look-rejection
   this venture has taken was invisible in isolation and obvious in comparison.
3. **A piece may be killed for being ordinary.** Previously the only exits were
   PASS and defect-FAIL, so "fine, I suppose" always shipped. `qa-hold` is now
   an acceptable destination for a defect-free piece that no one can name a
   reason to forward. The cadence floor in section 1 is **not** a licence to
   ship filler: a killed slot is a `BUILD-INCIDENT`, and three incidents in a
   week is an escalation to `cto`, not a reason to lower the bar.

## 6. Posting times — windows, not clock times

**Founder note, 2026-09-12:** identical clock times every day look automated.
True, and the record is worse than that: measured across all 61 posts, the
**median gap between the scheduled time and the actual publish time was 428
minutes** (7.1 hours; max 5,252 minutes), because a piece only publishes at the
first hourly CI run *after* the founder clears `needs_review`. 40 of 49 posts
in an earlier read published between 21:45 and 02:17 IST. The "fixed slots" in
the prompts were never the real posting times at all.

So this is a two-part fix, and the first part is the one that matters:

1. **Section 7's under-10k auto-clear removes the multi-hour review lag**, which
   is what makes a scheduled time mean anything. Without it, jitter is
   decorative.
2. **Every slot is a window, not a time.** `scripts/plan_day.py` draws a minute
   from inside the window using a generator seeded on `(account, date)`. The
   schedule is therefore reproducible (a reviewer can re-derive what the times
   should have been from the date alone) but never repeats, and never lands on a
   round `:00`/`:15`/`:30`/`:45` minute — the round minute is the visible tell.

Windows are per account and editable in `docs/slot-policy.json` without
touching code. Current windows (IST):

| Account | slot 1 | slot 2 | slot 3 |
|---|---|---|---|
| nuvarel | 09:40-11:20 | 14:10-16:00 | 19:05-21:15 |
| anime_ekaya | 12:35-14:20 | 18:50-20:40 | 22:05-23:40 |
| hype_tingles | 08:20-10:10 | 17:45-19:30 | 21:20-23:05 |

These windows are a **starting hypothesis**, not measured truth: the review lag
above means this account set has never produced a clean time-of-day comparison.
Once 3 weeks of auto-cleared posts exist, `growth-analyst` re-derives them from
data and edits the JSON. That is the first experiment to run after section 7
lands.

## 7. `needs_review` below 10,000 followers — founder ruling

Recorded in full in `CLAUDE.md` hard rule 1. Summary: below 10,000 followers,
the founder-approval step is replaced by a standing auto-clear. **The quality
gates do not change** — `content-reviewer` then `creative-director` /
`art-director` still gate every piece, and now gate harder (section 5). Only the
"wait for the founder" step is removed.

## 8. Daily performance read before the build — mandatory

**Founder instruction, 2026-09-12:** yesterday's real performance informs what
gets built next.

Every daily build's **Step 0** now runs, in this order, before any topic is
chosen:

```
py -3 scripts/collect_insights.py --rollup-only      # no token, no API call
py -3 scripts/plan_day.py --account <acct>
```

and the agent reads, for the trailing 7 days on its own account: the
best-performing piece and the worst, by reach and by interactions; which pillar
(`type`) each was; and whether the format the planner just assigned matches what
the data says. **The agent writes two lines into its own commit message** naming
what it learned and what it changed because of it. "Nothing changed" is an
acceptable answer once; the same answer three days running is an escalation to
`growth-analyst`.

The collector itself runs on CI, not in the build; `--rollup-only` reads the
committed CSV and is safe to run from any session (hard rule 3: running the
collector *with* a wrong token overwrites `insights.csv` with empty rows — the
build never does that).

## 9. Trend research — designed, specified, NOT live

`docs/trend-research-step-spec.md`. **Blocked on a Chief Security Officer review
of the cookie-based browser session method** (founder: the security check is
mandatory). Do not wire it into any daily build until CSO returns a verdict.
When it does go live it is a **soft dependency**: if the browser session is
unavailable or the step fails, the build proceeds on pillar-rotation fallback
and logs the skip. It never blocks a build.

---

## Change log

- **2026-09-12** — created. Group CTO, founder-direct. Supersedes the fixed
  per-account cadences and the fixed standing slot times in all three
  `daily-build-agent-prompt.md` files, and `nuvarel-strategy.md` §7.
