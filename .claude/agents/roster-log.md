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
