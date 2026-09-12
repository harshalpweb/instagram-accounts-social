# Daily niche trend research — specification

**Status: SPECIFIED, NOT LIVE. BLOCKED ON CHIEF SECURITY OFFICER REVIEW.**

**Author:** Group CTO, 2026-09-12, on a founder-direct instruction.
**Blocker:** the founder ruled that a security check on the cookie-based
browser session is mandatory before this runs. A Chief Security Officer
dispatch is reviewing the method in parallel as of 2026-09-12. **Do not wire
this into any daily-build prompt, any scheduled task, or any CI workflow until
CSO returns a verdict, and do not treat this document as permission.** The
`accounts/*/docs/daily-build-agent-prompt.md` files each carry a placeholder
naming this block; the placeholder stays a placeholder until the verdict lands.

---

## 1. What this step is for

Every day, before a build picks its topics, find what is *currently* live and
moving in that account's niche on Instagram itself — not what a listicle said
last quarter — and take **inspiration** from it. Never a copy: not the same
clip, not the same script, not the same caption, not a re-upload. The output is
a shortlist of *angles and formats* that are demonstrably getting distribution
right now, which the build then applies to the account's own subject matter and
its own pillar rotation.

Why Instagram itself and not a web search: a web search returns commentary about
trends. The point of this step is the platform's own current surface — which
audio is attached to what is ranking in `#interiordesign` today, what structure
the top Reels in the tag are using this week. `WebSearch` already covers the
commentary layer and stays in the build prompt regardless.

## 2. Why it must be a SOFT dependency (founder correction, 2026-09-12)

The machine that holds the browser session will not always be on. **If this step
is unavailable or fails on a given day, the daily build proceeds anyway**, on
the pillar-rotation fallback that every prompt already documents. This is not a
nice-to-have: a research step that can block publication converts an offline
laptop into a missed posting day, and the cadence floor
(`docs/cadence-and-format-policy.md` §1) is 3 posts a day without fail.

**Hard requirement:** this step can never be the reason a slot goes unfilled.

## 3. Placement in the daily build

Runs as **Step 1b**, immediately after the existing `WebSearch` trend queries
and before anti-repetition checking. It has a **hard 6-minute wall-clock
budget**. On timeout, treat exactly as a failure (§5).

```
Step 0   read gates + run plan_day.py + read yesterday's performance
Step 1   WebSearch trend queries              (unchanged, always runs)
Step 1b  in-app trend research                (this spec; soft, budgeted)
Step 2   anti-repetition ledger check         (unchanged)
Step 3   fallback rotation if 1 and 1b are both empty   (unchanged)
...
```

## 4. Mechanism

Tooling that already exists on this machine: `agent-browser`
(`%APPDATA%\npm\agent-browser`, CDP-based, no Playwright dependency) driving a
separately-authenticated Chrome profile. The cookie-import mechanics, including
the `--url` vs `--domain`/`--path` CDP validation failure and the `sessionid`
requirement, are already documented in
`docs/nuvarel-viral-reel-research-2026-09-12.md` §1 — do not rediscover them.

Per account, per day:

1. **Preflight (cheap, decides everything).** Confirm the session is alive:
   load `instagram.com` and check for a logged-in marker. **A logged-out or
   expired session is a normal outcome, not an incident** — it means the step
   is unavailable today. Do not attempt to re-authenticate, do not prompt for
   credentials, do not touch any OTP flow. Degrade and move on (§5).
2. **Read 2-3 tag surfaces**, from a per-account list kept in
   `accounts/<acct>/docs/trend-tags.json` (to be written when this unblocks):
   `instagram.com/explore/tags/<tag>/`, Top tab.
3. **Record, per surface, the top 5-8 pieces**: permalink, account handle and
   follower count, format (Reel/carousel), visible engagement, the *structure*
   in one line (before/after, guess-then-reveal, talking head, text overlay),
   the audio name if visible, and the caption's first line.
4. **Write** `accounts/<acct>/research/trends/<YYYY-MM-DD>.json`, plus a
   one-paragraph "what is moving and why" summary the build actually reads.
5. **Read-only, always.** No like, no follow, no comment, no save, no DM, no
   profile edit, no story view. The session is the founder's own identity; this
   step observes and never acts as him.

## 5. Graceful degradation — the behaviour that matters

Any of: browser binary missing, daemon will not start, session logged out or
expired, cookie file absent, a challenge/checkpoint screen, a network failure,
zero results parsed, or the 6-minute budget exhausted.

**On any of those, in order:**

1. Write one line to `accounts/<acct>/content/BUILD-INCIDENT.json`:
   `{"ts": "<iso>", "stage": "trend-research", "error": "<short reason>", "degraded": true, "blocking": false}`.
   `"blocking": false` is the field that says this did not cost a post.
2. **Continue the build.** Fall back to the account's documented pillar
   rotation, exactly as an empty `WebSearch` day already does.
3. Name it in the commit message: `trend research unavailable (<reason>),
   built on pillar rotation`.
4. **Never retry more than once**, never wait on it, never prompt a human,
   never escalate it on the day. It is a missing input, not a failure.

**Escalation is by pattern, not by instance:** the same reason on **5
consecutive days** for one account is a `cto` item — the step is effectively
dead and should either be fixed or formally switched off, rather than logging a
degraded line forever. `growth-analyst` surfaces the streak from the incident
file; nobody watches for it by hand.

## 6. Anti-copy rule — non-negotiable

Inspiration means the *structure* and the *angle*, never the artefact.

- Never download, re-upload, stitch, duet or re-post another account's media.
- Never reuse another account's caption, script, or on-screen text, in whole or
  paraphrased close enough to be recognisable.
- An audio track may be adopted only through Instagram's own in-app audio reuse,
  never by extracting and re-muxing someone else's file. Licensed-media hygiene
  (hard rule 2) applies to anything this step touches.
- The trend record is an **input to the build's own topic choice**, and the
  account's own anti-repetition ledger and pillar rotation still bind. A trend
  never overrides the 60-day topic rule.
- Any piece whose premise came from this step names the source permalink in its
  ledger row, so a later reviewer can check the distance between inspiration and
  imitation. `content-reviewer` checks that distance; `niche-researcher` checks
  any factual claim the trend carried.

## 7. What CSO is being asked (for the record)

Not this role's call, listed so the verdict has a target:

1. Storing and using an exported Instagram `sessionid` cookie for the founder's
   own account on this machine — where it lives, how it is protected, how it is
   revoked, and what its blast radius is if the machine is compromised. Note
   that `docs/credentials/` is already gitignored in this repo and does not
   currently exist.
2. Whether a **read-only** automated browser session on the founder's own
   logged-in account carries a meaningful account-action risk (challenge,
   checkpoint, restriction) distinct from the API rails the repo already uses.
3. Whether this needs its own kill switch beside the existing rails, and where.
4. Rotation and expiry: what happens when the cookie dies, and who re-exports it
   (a founder action — re-export is an account-auth step, not an agent step).

## 8. Definition of unblocked

All four, together:

- CSO verdict recorded in `../docs/consults/`.
- `accounts/<acct>/docs/trend-tags.json` written for each live account.
- The degradation path in §5 tested by running the step with the session
  deliberately absent, and the build observed to complete normally.
- The Step 1b placeholder replaced in **all three** prompt copies in one commit
  (hard rule 6: a cadence, slot or step change is not done until every prompt is
  audited).
