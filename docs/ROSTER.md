# instagram-accounts-social — Roster

Scope: one Instagram content operation (3 live accounts, up to 7). The main
session working in this repo is its Chief of Staff (CoS): convenes the roles
below, dispatches the per-account daily builds, records decisions in
`docs/consults/`. Portfolio-level roles live in `../docs/ROSTER.md`; this
file lists only what serves this repo. Created 2026-09-12 by Group CTO
(`../docs/consults/2026-09-12-group-cto-instagram-accounts-social-relocation-and-roster.md`);
role files reviewed by Chief People/Talent Officer 2026-09-12 and the
findings applied the same day (accounts-repo commits `3d352b4` and the
follow-up recorded in that consult). **Expanded from 4 to 7 roles
2026-09-12** by Group CTO on the founder's direct ask, from a Chief
People/Talent Officer draft — ruling:
`../docs/consults/2026-09-12-group-cto-instagram-roster-expansion-ruling.md`.

### Where a consult is recorded (doc-truth split resolved 2026-09-12)

This repo's `docs/consults/` was named as the consult home but has been
empty since it was created, while every real consult about this venture
lives in the portfolio's `../docs/consults/`. Both stay, with a rule:

- **`../docs/consults/` (portfolio)** — any ruling by a portfolio role
  (Group CTO, CCO, Group Legal/Compliance, Chief People/Talent Officer) or
  anything the registry entry cites. Cross-boundary decisions must be
  readable without cloning this repo. All existing records stay where they
  are; none are moved.
- **`docs/consults/` (local)** — consults between local roles only:
  review-gate verdicts worth preserving in full, `art-director` system
  decisions, `audience-strategist` briefs' decision records. Nothing here
  is ever the sole record of a decision the portfolio needs.

## Roles

| Role | Agent | Model | Mode | Owns (output artifact) |
|---|---|---|---|---|
| Pipeline CTO | `cto` | opus | advise + execute (this repo) | Publish/refresh/insights rails, renderers and gates, toolchain, prompt mechanics, ledger schemas, scheduler durability, Meta API mechanics. Output: working pipeline changes + tests. Reports to Group CTO on every matter. |
| Audience Strategist | `audience-strategist` | opus | advise + execute (`docs/strategy/`, `docs/open-decisions.md`) | Per-account positioning (who it is for, promise, geography, cadence rationale, mascot decisions), concept briefs for the 4 unbuilt accounts, and the persuasion spec (what earns a share, what holds past 3 s, parasocial attachment). Output: positioning briefs + `persuasion-spec.md` + experiment proposals. Briefs `creative-director`; never edits a strategy doc. |
| Creative Director | `creative-director` | opus | advise + execute (strategy docs, brand assets, creative sections of build prompts) | Per-account voice, pillars, format vocabulary, hook standards, anti-repetition rules, quality ratchet, and **in-app discoverability** (caption keywords, hashtags, audio-for-search, `alt_text` copy). Output: strategy docs and brand-fit verdicts per batch. |
| Art Director | `art-director` | opus | advise + execute (`accounts/*/brand/`, `docs/visual/`) | Per-account visual identity system, generation-prompt vocabulary, motion-quality bar, material fidelity, the mandatory eyes-on pick at feed scale. Output: `docs/visual/<account>.md` + visual verdicts naming the frame. Never touches `scripts/` or a renderer. |
| Niche Researcher | `niche-researcher` | opus | advisory (writes only new files under `docs/niche/`) | Parameterized per account: subject-matter fluency and primary-source verification of external factual claims before a piece is queued; topic currency. Output: `docs/niche/<account>-<topic>.md` + cited, dated facts. |
| Content Reviewer | `content-reviewer` | opus | advisory (read-only) | Independent QA on every built piece before the founder gate: deterministic checks, dense frame-level eyes-on review, and (from 2026-09-12) primary-source verification of every external factual claim. Output: per-piece PASS/FAIL with a defect list. Never reviews a piece it built. |
| Growth Analyst | `growth-analyst` | opus | advisory (read-only) | Reads `analytics/insights*.csv`, names confounds, recommends experiments and slot/cadence changes; from 2026-09-12 also account-level metrics and standing account-health escalation. Output: evidence-backed performance reads and experiment proposals. |

Builders are not separate agent files: each account's
`accounts/<acct>/docs/daily-build-agent-prompt.md` is the implementer spec,
dispatched as one agent per account per day. A standalone "content creator"
role was considered and declined 2026-09-12: hard rule 6 already makes the
prompt the implementer spec, and no recorded incident says otherwise.

### Who owns which half of a creative question

Four roles touch creative work. The split is by discipline, not by account:

- **`audience-strategist` — WHO and WHY.** Who the account is for, why a
  stranger forwards it. Writes briefs only.
- **`creative-director` — WHAT and how it SOUNDS.** Voice, premise,
  pillars, formats, hooks, discoverability copy. Owns the strategy docs;
  holds the per-piece brand-fit verdict.
- **`art-director` — how it LOOKS.** Palette, type, grid, composition,
  light, material, motion bar, generation-prompt vocabulary. Owns the
  visual system; its call on the *system*, `creative-director`'s call on
  the *piece*.
- **`niche-researcher` — whether it is TRUE and CURRENT.** Subject-matter
  fluency and primary-source facts, before the build.

### Named open tasks assigned by this ruling (2026-09-12)

| Task | Owner | Why |
|---|---|---|
| Add `alt_text` to image container creation in the publisher | `cto` | Graph API supports it; verified zero uses repo-wide. ~30 min, not a role. |
| Add account-level insights (`reach`, `accounts_engaged`, `total_interactions`, `views`) to `collect_insights.py` | `cto` | The venture cannot currently tell whether any account is growing. `follower_count` needs ≥100 followers per Meta and is manual until then. |
| ~~Investigate `hype_tingles` distribution (2-9 reach across 20 posts, flat since 2026-09-05)~~ **CLOSED 2026-09-12 by Group CTO** | was `cto`, escalated by `growth-analyst` | Diagnosed: dead legacy follower graph (9 of 282 followers reached in 29 days) starves the early-distribution signal, so nothing escalates to the Reels recommendation surface — 12 non-follower accounts reached in 29 days vs 1541/1641 on the two accounts that have no follower graph to seed into. Not content, pipeline, encoding, dormancy, or the AI-profile policy; each refuted with evidence. Ruling: content line moves to a fresh account; no bio/profile change. `../../docs/consults/2026-09-12-group-cto-hype-tingles-distribution-diagnosis.md` |
| Run the share-replication experiment (treatment vs. same-account control) | `audience-strategist` designs, `growth-analyst` measures, `creative-director` builds | 2 of 61 posts hold 59% of lifetime reach. Highest-leverage open question in the venture. |
| Hardcoded machine-local absolute path in `accounts/nuvarel/render/gen_photo.py:43` | `cto` | Binds nuvarel's build to one physical machine; relevant to the scheduler decision. |

## Chain of authority

- `cto` → **Group CTO** (`../.claude/agents/group-cto.md`) on any matter;
  Group CTO's ruling stands (founder ruling 2026-09-12).
- `creative-director` and `art-director` → **Chief Creative Officer**
  (portfolio) on cross-account brand coherence and venture-level
  differentiation; CCO spot-checks batches on its own referral cadence and
  its verdict wins over both.
- `art-director` → `creative-director` on any single piece's brand fit;
  `art-director` holds the visual *system*, `creative-director` holds the
  *piece*. A deadlock goes to Chief Creative Officer, then Group CTO.
- `audience-strategist` → **Portfolio Strategist** (portfolio) on whether
  an account should exist at all or how it is positioned against other
  ventures; → `creative-director`, which adopts or rejects every brief.
- `niche-researcher` → **Group Legal/Compliance** (portfolio) the moment
  subject matter touches copyright, trademark or a platform content rule.
  It names the risk; it never clears it.
- Content clearance (`needs_review: false`) → the founder, or Group CTO
  with a recorded consult. Never a local role.
- Money (paid automation, ads, any spend) → Group CFO within the current
  spend-ladder unlock; above it, the founder.

## Referral map

| Trigger | Roles |
|---|---|
| Any pipeline, renderer, gate, workflow, token or scheduler change | `cto`; Group CTO if it touches `../video_lab`, `../blender_studio`, `../copydesk`, TrendGiri's copy of the publisher, or a portfolio convention |
| New format, pillar change, voice question, hook quality, caption keywords or hashtags | `creative-director`; Chief Creative Officer for cross-account coherence or a venture-level verdict |
| A founder reaction about how something LOOKS ("amateur", "fonts unreadable", "not premium"), a palette/type/grid question, a generation-prompt vocabulary, the motion bar, a generate-many-pick-one step | `art-director`; `creative-director` if the disagreement is about one specific piece rather than the system |
| Who an account is for, a positioning or cadence rationale, a mascot decision, a concept for one of the 4 unbuilt accounts, "why would anyone share this?" | `audience-strategist`; Portfolio Strategist (portfolio) before any "should this account exist" question reaches the founder queue |
| A piece asserts an external fact (date, count, title, price, material, canon detail); a topic may be stale; the build needs real fluency in the niche | `niche-researcher` (named account) before the build; `content-reviewer` verifies again at the gate — both, not either |
| A daily build has pushed its commit (every piece is already at `needs_review: true`) | `content-reviewer` first (mandatory, on the pushed commit, gates on defects), then `creative-director` on the pieces that passed (gates on concept/brand fit; its FAIL overrides a `content-reviewer` PASS, never the reverse). The dispatching session convenes both, logs each verdict in `.claude/agents/roster-log.md`, and moves an unfixable FAIL to `accounts/<acct>/content/qa-hold/`. Only then does the piece reach the founder's review queue. |
| "What is working?", cadence or slot change proposals, an outlier post, an account whose reach is flat and far below its siblings | `growth-analyst` → `creative-director` decides what to change; a flat-account escalation goes to `cto`, then Group CTO — it is a distribution question, not a content one |
| Platform policy (AI disclosure, AI-people, music, Original Content rules, monetization terms) | Group Legal/Compliance (portfolio) |
| A new token, secret, cookie export, or credential on disk | Chief Security Officer (portfolio), before it is used |
| Research on a generic problem shape | grep every `docs/RESEARCH-INDEX.md` under `income-engine/` first (portfolio dedup rule) |
| Two sessions on the same account/queue | Session Manager (portfolio) |

## Roles deliberately NOT created (2026-09-12), with their tripwires

A role is not created because a category sounds useful. It is created when
a named incident has already shipped *and* it owns an artifact no existing
charter covers. These were considered and held, each with the observation
that would reopen it:

| Not created | Why | Reopen when |
|---|---|---|
| `discovery-specialist` (Instagram SEO) | Function reassigned to `creative-director`; the `alt_text` gap is a ~30-min `cto` task. The evidence was a measured absence, not an incident — and `profile_visits` is FEED-only and reads 0 on posts 1-7 people saw. You cannot optimise discovery on a post nobody was shown. | Any account sustains ~500+ reach per post, or crosses 100 followers (the threshold where Meta's own account metrics become available). |
| `community-manager` | 5 comments and 0 recorded follows across 61 posts (2026-09-12 snapshot). There is no community to manage yet. | First account past ~500 followers, or >10 inbound comments/DMs in one week. |
| `monetization-lead` | Facebook Content Monetization is invite-only as of 2026-09-01; nothing to operate. | A monetization invite lands, or the first brand/affiliate approach arrives. |
| Scheduling / ops role | Mechanically impossible: a subagent cannot hold `CronCreate`/`CronList`, so the role could not do its own job. Stays with the CoS of the owning session. | A durable scheduler exists that a subagent can actually drive. |
| Review-throughput role | At 7 accounts × 3 pieces/day the two-reviewer gate is the scaling wall — but current throughput is 0 pieces/day, so there is no incident. | ≥5 live accounts, or a review backlog sustained past 24 h while the pipeline is actually running. |
| Local legal/compliance liaison | Declined 2026-09-12 by Group CTO; the cross-account policy view must stay portfolio-level. | Unchanged. |
| Standalone "content creator" roles | Hard rule 6: the daily-build prompt *is* the implementer spec. | A recorded incident traceable to the prompt-as-spec model itself. |

## Evolution

Every consult ends with a Roster feedback block; the CoS applies learnings
to the role file's `## Accumulated learnings` section and appends one
line per consult to `.claude/agents/roster-log.md` (the instrument the
next sentence is measured against). A role that scores below-bar twice
in that log goes to Chief People/Talent Officer (portfolio) for a
rewrite/retire recommendation; Group CTO approves role changes here.

**The bar for creating a local role (Group CTO, 2026-09-12).** This repo is
currently the only subproject in the portfolio with local agent files —
every other `docs/ROSTER.md` under `income-engine/` sits over an empty
`.claude/agents/`. Whatever shape is set here is the template the other
subprojects will copy, so the bar is set deliberately high:

1. A **named incident that already shipped**, or a measured gap with a
   number attached — not a category that sounds useful.
2. An **owned output artifact** that no existing role's charter covers.
   "Advises on X" is not an artifact.
3. The function is **not better served by a tool, a check, or a charter
   line** on a role that already exists. Two of the four roles proposed in
   the 2026-09-12 draft were closed this way: an external-fact defect class
   became `content-reviewer`'s `WebSearch`/`WebFetch` plus one named check
   step, and in-app discoverability became a `creative-director` charter
   line plus a `cto` backlog item.
4. A **role count is not a capability.** Throughput is. Before adding a
   role, check `.claude/agents/roster-log.md`: if the existing roles have
   not been dispatched, the constraint is dispatch, not headcount.
