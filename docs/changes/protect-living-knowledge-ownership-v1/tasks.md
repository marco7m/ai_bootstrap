# Tasks: Protect Living Knowledge Ownership v1

## 1. Contract and lifecycle policy

- [x] Re-read the approved spec and plan; record any implementation deviation
  before coding past it.
- [x] Add `core/lifecycle.py` with validated lifecycle/status vocabulary,
  exact-output hashing normalization, and pure rendered-file classification.
- [x] Add table-driven lifecycle tests covering every managed, seeded, reset,
  missing-state, drift, equality, force, and line-ending/trailing-newline case.
- [x] Centralize writable and blocking status sets for applier consumers.

## 2. Manifest ownership

- [x] Extend file specs with validated `managed|seeded` lifecycle and a
  backward-compatible `managed` default.
- [x] Expose normalized `project`, `composed`, and `migrated` lifecycle for the
  existing specialized manifest collections.
- [x] Add obsolete migration target/disposition hints and validate all path and
  ownership overlaps.
- [x] Explicitly classify every default-pack path according to the approved
  spec and bump the pack version to 0.5.0.
- [x] Add manifest contract tests for valid/default/invalid lifecycle,
  migration hints, overlaps, conditional files, and explicit default-pack
  coverage.

## 3. State provenance and compatibility

- [x] Decouple runtime state parsing from planner imports sufficiently to pass
  prior provenance into planning without a circular dependency.
- [x] Make state loading tolerate known old state and unknown future fields,
  while treating malformed global/per-path data conservatively.
- [x] Record lifecycle, `applied_content_hash`, and `applied_version` only for
  content written or proven equal.
- [x] Merge prior inventory for preserved, skipped, and unselected paths;
  remove only safely retired active entries and retain required disposition
  evidence.
- [x] Add state tests for 0.4.0 compatibility, unknown fields, malformed state,
  exact provenance, selective merge, preserved drift, reset, and retirement.

## 4. Planner, retirement, and applier

- [x] Extend plan/result metadata with lifecycle, managed-only selection,
  reset intent, drift reason, and applied-content provenance.
- [x] Replace `_plan_file` force-only behavior with the pure lifecycle decision
  matrix and actionable status messages.
- [x] Implement managed-only planning without seeded/obsolete operations and
  without losing omitted state.
- [x] Plan obsolete deletion only when prior applied hash proves no drift;
  otherwise return actionable `migration_required` with destination/hint.
- [x] Preserve directory and symlink safety for hashing, planning, and
  retirement.
- [x] Make applier preflight aggregate `conflict` and
  `migration_required` before any mutation and execute only writable statuses.
- [x] Add planner/applier tests for all lifecycle paths, composition
  preservation, reset, managed-only, obsolete drift, blocker aggregation, and
  no-write preflight.

## 5. CLI and TUI consent

- [x] Load prior state in CLI/TUI plan construction and merge it only after a
  successful real apply.
- [x] Redefine CLI `--force` help/behavior as managed-file update and add
  `--managed-only`.
- [x] Add `--reset-project-knowledge` plus exact
  `--confirm-reset-project-knowledge "RESET PROJECT KNOWLEDGE"` validation;
  allow unconfirmed dry-run preview only.
- [x] Add lifecycle/category to CLI summaries and clearly distinguish managed
  updates, safe seeded updates, preserved knowledge, resets, compositions,
  migrations, and conflicts.
- [x] Separate managed update and knowledge reset in the TUI, keep reset off by
  default, add reset-specific confirmation, and list every seeded reset owner.
- [x] Update English and pt-BR UI text without duplicating lifecycle policy in
  widget handlers.
- [x] Add CLI/TUI tests for options, confirmation timing, preview, summaries,
  localization, reset defaults, errors, and state preservation.

## 6. Generated recovery policy and semantic checks

- [x] Update default-pack `AGENTS.md` with the compact rule that bootstrap
  maintenance cannot replace established project knowledge.
- [x] Update generated `docs/LIVING_DOCUMENTATION.md` with detailed
  regeneration/downgrade/truncation audit and union-recovery guidance.
- [x] Update generated `living-docs` skill to route suspicious owners through
  state/Git audit and require removal disposition during closeout.
- [x] Add standard-library `check_living_docs.py` with all approved current-tree
  invariant checks and concise, non-sensitive diagnostics.
- [x] Add optional `--baseline-ref` Git comparison for coverage downgrade,
  removed capability identities, and removed verified rows.
- [x] Keep `check_links.py` independent and keep AGENTS/skill artifacts within
  existing word budgets.
- [x] Add semantic-checker tests for each blocking signal, clean scaffolds,
  unavailable Git, and baseline comparisons.

## 7. Incident and integration regression coverage

- [x] Add a self-contained 0.4.0 incident fixture with evolved seeded owners
  and legacy state lacking applied-content hashes.
- [x] Prove ordinary apply and `--force` preserve every evolved seeded owner
  while eligible managed files update.
- [x] Add fresh untouched-seed adoption and later safe seed-upgrade coverage.
- [x] Add state-less existing project, evolved obsolete file, clean obsolete
  file, Python output, and Rust composition/reapply coverage.
- [x] Ensure fixtures never read or modify the live `text-online-mmorpg`
  checkout.

## 8. Durable documentation and closeout

- [x] Update README with lifecycle taxonomy, safe `--force`, managed-only,
  explicit reset, state provenance, migration blockers, and affected-project
  audit guidance.
- [x] Update product and architecture living owners with validated current
  behavior; do not promote approved design as implementation evidence.
- [x] Update the capability row from destructive 0.4.0 current state to the
  validated lifecycle-aware state, preserve test evidence, and clear the active
  change only after all acceptance criteria pass.
- [x] Decide whether any implementation alternative requires a durable decision;
  do not create an ADR for the already approved lifecycle contract alone.
- [x] Reconcile every intentionally removed fact/status with an explicit
  disposition and confirm touched files remain conceptually cohesive.

## 9. Validation

- [x] Run focused lifecycle, manifest, state, planner, applier, CLI/TUI, checker,
  and incident-fixture tests during implementation.
- [x] Run `python3 -m unittest discover -s tests -v`.
- [x] Run `python3 -m compileall -q ai_workflow_bootstrap`.
- [x] Run `python3 -m json.tool ai_workflow_bootstrap/template_packs/default/manifest.json`.
- [x] Generate temporary Python and Rust repositories and run their generated
  `check_living_docs.py` and `check_links.py`.
- [x] Run `python -m build` when the environment provides a working build
  backend; record an exact environment blocker otherwise.
- [x] Run `git diff --check` and the repository-local living-doc link checker.
- [x] Validate every acceptance criterion against evidence and record meaningful
  deviations/limitations in change notes.
- [x] Confirm the touched area is at least as maintainable as before and that no
  lifecycle rule is duplicated across engine and UI layers.
- [x] Summarize behavior, files, validation, knowledge updates, limitations,
  migration implications, and the separate downstream recovery step.
