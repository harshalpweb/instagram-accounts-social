# instagram-accounts-social — Roster

Scope: one Instagram content operation (3 live accounts, up to 7). The main
session working in this repo is its Chief of Staff (CoS): convenes the roles
below, dispatches the per-account daily builds, records decisions in
`docs/consults/`. Portfolio-level roles live in `../docs/ROSTER.md`; this
file lists only what serves this repo. Created 2026-09-12 by Group CTO
(`../docs/consults/2026-09-12-group-cto-instagram-accounts-social-relocation-and-roster.md`);
role files reviewed by Chief People/Talent Officer 2026-09-12 and the
findings applied the same day (accounts-repo commits `3d352b4` and the
follow-up recorded in that consult).

## Roles

| Role | Agent | Model | Mode | Owns (output artifact) |
|---|---|---|---|---|
| Pipeline CTO | `cto` | opus | advise + execute (this repo) | Publish/refresh/insights rails, renderers and gates, toolchain, prompt mechanics, ledger schemas, scheduler durability, Meta API mechanics. Output: working pipeline changes + tests. Reports to Group CTO on every matter. |
| Creative Director | `creative-director` | opus | advise + execute (strategy docs, brand assets, creative sections of build prompts) | Per-account voice, pillars, format vocabulary, hook standards, anti-repetition rules, quality ratchet. Output: strategy docs and brand-fit verdicts per batch. |
| Content Reviewer | `content-reviewer` | opus | advisory (read-only) | Independent QA on every built piece before the founder gate: deterministic checks plus dense frame-level eyes-on review. Output: per-piece PASS/FAIL with a defect list. Never reviews a piece it built. |
| Growth Analyst | `growth-analyst` | opus | advisory (read-only) | Reads `analytics/insights*.csv`, names confounds, recommends experiments and slot/cadence changes. Output: evidence-backed performance reads and experiment proposals. |

Builders are not separate agent files: each account's
`accounts/<acct>/docs/daily-build-agent-prompt.md` is the implementer spec,
dispatched as one agent per account per day.

## Chain of authority

- `cto` → **Group CTO** (`../.claude/agents/group-cto.md`) on any matter;
  Group CTO's ruling stands (founder ruling 2026-09-12).
- `creative-director` → **Chief Creative Officer** (portfolio) on
  cross-account brand coherence and venture-level differentiation; CCO
  spot-checks batches on its own referral cadence.
- Content clearance (`needs_review: false`) → the founder, or Group CTO
  with a recorded consult. Never a local role.
- Money (paid automation, ads, any spend) → Group CFO within the current
  spend-ladder unlock; above it, the founder.

## Referral map

| Trigger | Roles |
|---|---|
| Any pipeline, renderer, gate, workflow, token or scheduler change | `cto`; Group CTO if it touches `../video_lab`, `../blender_studio`, `../copydesk`, TrendGiri's copy of the publisher, or a portfolio convention |
| New format, pillar change, voice question, hook quality, a founder "this looks bad" | `creative-director`; Chief Creative Officer for cross-account coherence or a venture-level verdict |
| A daily build has pushed its commit (every piece is already at `needs_review: true`) | `content-reviewer` first (mandatory, on the pushed commit, gates on defects), then `creative-director` on the pieces that passed (gates on concept/brand fit; its FAIL overrides a `content-reviewer` PASS, never the reverse). The dispatching session convenes both, logs each verdict in `.claude/agents/roster-log.md`, and moves an unfixable FAIL to `accounts/<acct>/content/qa-hold/`. Only then does the piece reach the founder's review queue. |
| "What is working?", cadence or slot change proposals, an outlier post | `growth-analyst` → `creative-director` decides what to change |
| Platform policy (AI disclosure, AI-people, music, Original Content rules, monetization terms) | Group Legal/Compliance (portfolio) |
| A new token, secret, cookie export, or credential on disk | Chief Security Officer (portfolio), before it is used |
| Research on a generic problem shape | grep every `docs/RESEARCH-INDEX.md` under `income-engine/` first (portfolio dedup rule) |
| Two sessions on the same account/queue | Session Manager (portfolio) |

## Evolution

Every consult ends with a Roster feedback block; the CoS applies learnings
to the role file's `## Accumulated learnings` section and appends one
line per consult to `.claude/agents/roster-log.md` (the instrument the
next sentence is measured against). A role that scores below-bar twice
in that log goes to Chief People/Talent Officer (portfolio) for a
rewrite/retire recommendation; Group CTO approves role changes here.
