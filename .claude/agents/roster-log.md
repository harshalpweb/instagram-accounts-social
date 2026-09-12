# Roster Log (append-only) — instagram-accounts-social

One line per consult, appended by the CoS of this repo:
`YYYY-MM-DD | role | task (short) | verdict: up-to-mark / below-bar | learning applied (or "none")`

Daily review-gate runs count as consults: one line per `content-reviewer`
run and one per `creative-director` run, naming the account, the date of
the batch, and the per-piece verdicts (e.g. `3 PASS`, `2 PASS / 1 FAIL
(reel-02: clipped type at 4.2 s)`). A morning batch with no line here for
its account and date was not reviewed.

Two below-bar verdicts for the same role → Chief People/Talent Officer
(portfolio) recommends a rewrite/retire; Group CTO approves
(`docs/ROSTER.md`, Evolution). Do not edit or delete existing lines.
Precedent: `../trend_predictor/.claude/agents/roster-log.md`.

---
2026-09-12 | (all four roles) | role files created by Group CTO, reviewed by Chief People/Talent Officer the same day | verdict: n/a (review of the files, not of a consult) | learning applied: reviewer findings applied — stale repo root and bare `git commit` in the prompts (`3d352b4`); review gate wired into all three DoDs; verdict precedence between `content-reviewer` and `creative-director`; explicit never-commit lines; this log created
2026-09-12 | Chief People/Talent Officer (portfolio) | draft roster expansion for this repo on the founder's direct ask (4 proposed roles + a growth-analyst charter extension), with an explicit dissent on sequencing | verdict: up-to-mark (evidence-grounded, dissent stated plainly, correct cut order, correctly declined 3 categories the founder named) | learning applied: 2 of 4 proposed roles approved as roles, 1 approved with a widened scope, 1 cut with its function reassigned — see the Group CTO ruling
2026-09-12 | Group CTO (portfolio) | ruling on the roster expansion: verified the rollup, `content-reviewer` frontmatter, live queues, `alt_text` absence and Meta's own metric limits before deciding | verdict: n/a (ruling, not a consult on this repo's own work) | learning applied: roster grown 4 → 7 (`audience-strategist`, `art-director`, `niche-researcher`); `discovery-specialist` cut, function split between `creative-director` and a `cto` task; `content-reviewer` granted `WebSearch`/`WebFetch` + a named external-fact check step; `growth-analyst` charter extended to account-level metrics and account-health escalation; the bar for creating a local role and 7 not-created roles with tripwires recorded in `docs/ROSTER.md`; production restart ruled P0 ahead of dispatching any new role
