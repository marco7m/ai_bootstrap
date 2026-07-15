# Notes: Unified bootstrap workflow and conditional project policies

## Implementation discoveries

- `AGENTS.project.md` is a protected manifest path, not a generated template.
  Its absence produces no file or state entry; an existing file is reported as
  project-owned and `preserved`.
- Make composition needed an atomic preflight because ordinary generated docs
  are planned before repository-owned operational files. Any conflict now
  blocks the applier before its first filesystem mutation.
- Historical change artifacts still mention partial workflow modes because they
  record the contracts that existed at that time. Current README, CLI, TUI,
  product, architecture and capability owners describe the unified workflow.

## Maintainability audit

- Risk: moderate and localized to generated-output planning.
- Local refactor completed: pure Make/line composition moved to
  `core/composer.py`; Rust policy remains in templates and the manifest.
- No separate refactor is currently justified. `planner.py` grew, but continues
  to own selection, rendering and result construction rather than Make rules.
- Tests protect public generated behavior and preservation invariants rather
  than exact full-document snapshots.

## Validation

- `python3 -m unittest discover -s tests -v`: passed, 74 tests.
- `python3 -m compileall -q ai_workflow_bootstrap`: passed.
- default manifest JSON validation: passed.
- source and generated Rust relative-link validation: passed.
- fake-Cargo `make clean-dev` contract: passed and preserved the release probe.
- `git diff --check`: passed.

Environment-only limitations:

- `pytest -q` could not start because the configured `asdf` Python 3.11.11 is
  not installed. The same suite passed through standard-library `unittest`.
- `python3 -m build` could not start because the active Python environment does
  not provide the `build` module. No dependency was added to work around the
  local environment.
