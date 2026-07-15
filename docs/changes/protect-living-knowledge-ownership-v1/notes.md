# Notes: Protect Living Knowledge Ownership v1

## Outcome

Implemented the approved lifecycle-aware bootstrap contract as default template
pack 0.5.0. Normal and forced upgrades preserve evolved seeded owners; managed
updates, explicit seeded reset, composed content and guarded obsolete migration
are distinct plan categories.

## Validation evidence

- `python3 -m unittest discover -s tests -v`: 91 tests passed.
- `python3 -m compileall -q ai_workflow_bootstrap`: passed.
- `python3 -m json.tool ai_workflow_bootstrap/template_packs/default/manifest.json`: passed.
- Current repository semantic checker: passed after recording the reviewed
  legacy overwrite disposition in `docs/INDEX.md`.
- Current repository link checker: passed.
- Fresh temporary Python repository: apply, semantic checker and link checker
  passed; edited seeded `docs/INDEX.md` remained byte-for-byte intact after
  `--force`.
- Fresh temporary Rust repository: apply, semantic checker and link checker
  passed; composed `Makefile` and Rust architecture policy were generated.
- `git diff --check`: passed.

## Environment limitation

`python -m build` could not run because the active Python environment lacks the
`build` module:

```text
/home/marco/.asdf/installs/python/3.11.11/bin/python: No module named build
```

No dependency was installed because this change adds no dependency and the
approved standard-library validation path passed.

## Deliberate implementation choices

- Shipped `--managed-only`, the approved minimum selective interface; no generic
  group filter or partial workflow mode was added.
- `migrated` remains guarded retirement with `migration_required`, not automatic
  semantic Markdown merge.
- Legacy `overwritten` state remains a blocking semantic-check signal until a
  project records a reviewed `Bootstrap recovery audit:` disposition or a later
  safe bootstrap run updates its state.
- The 0.4.0 incident is reproduced entirely in temporary test data; tests never
  read or modify the live affected project.
- No backup, Git mutation, clean-worktree requirement or transactional rollback
  was introduced.

## Maintainability closeout

- Planned local refactor completed: lifecycle decisions and status sets live in
  `core.lifecycle` rather than CLI/TUI/planner branches.
- Safe local cleanup completed: timezone-aware state timestamps and one blocker
  preflight path.
- The TUI remains the largest touched file, but only adapter/widget wiring was
  added; lifecycle policy is not duplicated there.
- No separate refactor spec is required. Tests assert public plans, persisted
  state, file content, diagnostics and interface behavior rather than private
  helper call order.
