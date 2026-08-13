# Notes: Contract-First Proportional Workflow v1

## Result

Default template-pack `0.8.0` now separates spec necessity from the independent
plan/tasks approval gate. A clear-contract repair can omit a new product spec,
but every non-trivial implementation still requires approved plan/tasks. The
existing artifact family now represents a standalone no-spec repair without a
new document type.

## Validation evidence

- Focused initial regression: 5 expected failures and 1 passing checker gate
  against pack `0.7.1` before template changes.
- Affected boundary: 83 tests and 13 subtests passed.
- Full pytest: 133 tests and 23 subtests passed.
- Full unittest: 133 tests passed.
- `python -m compileall -q ai_workflow_bootstrap tests` passed with bytecode
  redirected outside the repository.
- Generated context budgets: `AGENTS.md` 694/800 words, `spec-driven/SKILL.md`
  298/300 and `docs/SPEC_DRIVEN.md` 905/1000.
- Temporary fixtures covered fresh Python/Rust/Node generation, Node command
  detection, tasks-based repair closeout without `spec.md`, pending-closeout
  rejection, synthetic `0.7.1` managed update, managed-only, reapply, pack-state
  advancement and byte preservation of evolved seeded/project-owned files.

## Deviations and limitations

No approved production boundary changed: checker scripts, maintainability
auditor, manifest topology and all core/CLI/TUI modules remained unchanged.
Tests confirmed that current checkers already accept a tasks-based change
directory without `spec.md`.

A fresh Rust scaffold has a pre-existing documentation-health warning:
`docs/architecture/rust-development.md` is not reachable from `docs/INDEX.md`.
The Rust fixture therefore validated the no-spec repair with the focused link
checker, while Python, Node and the upgrade fixture exercised aggregate
closeout. Adding conditional seeded navigation would change manifest/scaffold
scope and was not necessary to validate this workflow, so the warning remains
separate rather than expanding the approved change.

No real downstream repository was read or changed. No commit, stage, force
application, project-knowledge reset or dependency was used.
