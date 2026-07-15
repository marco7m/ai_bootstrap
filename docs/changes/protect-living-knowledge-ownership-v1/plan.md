# Implementation Plan: Protect Living Knowledge Ownership v1

## 1. Summary

Introduce an explicit lifecycle policy between manifest parsing and planning,
then make state provenance, obsolete-file retirement, CLI/TUI consent, and
generated living-document recovery rules consume that policy. The implementation
will preserve the existing planner/applier flow while replacing global
path-level force decisions with a small, table-tested lifecycle decision model.

The work will ship as template pack 0.5.0. It will preserve evolved living
owners during normal and forced upgrades, fail closed for legacy state without
applied hashes, and provide a separately confirmed seeded-knowledge reset.

## 2. Relevant Existing Context

- `template_packs/default/manifest.json` currently declares ordinary files,
  project-owned paths, safe compositions, and obsolete files, but only the
  project-owned collection carries ownership semantics.
- `core.template_pack` parses and validates those manifest collections.
- `core.planner._plan_file` currently owns the entire existing/equal/force
  matrix and treats every declared file alike.
- `core.state` records template hashes and last operation status, but it imports
  planner types at runtime, rebuilds the file inventory, and has no rendered
  applied-content hash.
- `core.applier` already preflights `conflict` before writes, but does not know
  about `migration_required` or reset results.
- CLI and TUI build plans without loading prior state. The TUI exposes one
  destructive overwrite checkbox and one generic `APPLY` confirmation.
- The generated `living-docs` skill is intentionally compact and currently
  runs only the link checker after structural changes.
- Tests use standard-library `unittest`, temporary repositories, public plan
  results, CLI output, and small template-content assertions.
- The confirmed 0.4.0 incident state contains `overwritten` seeded owners and
  template hashes but no rendered applied-content hashes.

## 3. Existing Conventions Found

- Folder structure: engine decisions under `ai_workflow_bootstrap/core/`, user
  adapters in `cli.py`/`tui.py`, generated policy in the default template pack,
  and contract tests under `tests/`.
- Naming style: frozen manifest dataclasses, plain dataclasses for plans/state,
  underscore-prefixed planner helpers, and lower-case result statuses.
- Error handling: invalid manifests/paths raise `ValueError`; plan blockers are
  aggregated into `PlanConflictError`; CLI/TUI convert them to actionable user
  messages.
- Logging: no logging framework; preview and final summaries expose results.
- Testing pattern: standard-library `unittest`, temporary paths, exact public
  statuses/invariants, and no third-party fixtures.
- Config pattern: JSON manifest normalized into typed specs.
- External integration pattern: none for apply; optional Git use must stay in
  the generated semantic checker.
- Persistence/data access pattern: `.ai-bootstrap/state.json` is rewritten
  after a successful real apply and never during dry-run.

## 4. Proposed Changes

### 4.1 Add a pure lifecycle policy boundary

- Add `core/lifecycle.py` with:
  - validated lifecycle constants or enum values;
  - one rendered-content hashing/normalization helper shared by planner/state;
  - an immutable input/output model for rendered-file classification;
  - a pure decision function covering managed, seeded, and explicit reset;
  - central blocking and writable status sets used by the applier.
- Keep filesystem reads and messages in the planner. The lifecycle module
  decides only status/reason from lifecycle, existence, equality, prior hash,
  force, and reset inputs.
- Represent seeded safe template evolution as `updated`, evolved/untracked seed
  as `preserved`, and explicit seeded replacement as `reset`.

### 4.2 Extend and validate manifest lifecycle metadata

- Add `lifecycle` to `TemplateFileSpec`; accept only `managed` or `seeded` and
  default omitted values to `managed` for external-pack compatibility.
- Give project-owned, composition, and obsolete specs normalized lifecycle
  properties/fields (`project`, `composed`, `migrated`) without collapsing their
  distinct schemas.
- Add an optional `migration_target`/disposition hint to obsolete specs.
- Reject unsupported lifecycles and lifecycle/path ownership overlaps at pack
  load time.
- Mark every default-pack file explicitly and bump the pack to 0.5.0.
- Classify the default pack exactly as approved in the spec.

### 4.3 Make state tolerant, mergeable, and provenance-aware

- Remove the runtime state-to-planner import cycle by using `TYPE_CHECKING` or
  protocol/plain mapping inputs where only annotations are required.
- Make `load_state` parse known top-level fields with defaults, tolerate unknown
  future fields, and validate `files`/per-file entries without granting unsafe
  authority.
- Add lifecycle, `applied_content_hash`, and `applied_version` to eligible file
  entries; add a small retired-operation inventory only if needed to retain
  confirmed obsolete disposition.
- Load prior state in CLI/TUI and pass a read-only prior-file mapping into the
  planner rather than making the planner perform persistence I/O.
- Change `build_state` to merge prior inventory with selected results:
  - writable and proven-equal rendered files receive new applied provenance;
  - preserved/skipped paths retain valid prior applied provenance;
  - unselected paths remain unchanged;
  - confirmed retired paths leave the active inventory and retain their safe
    retirement record if the chosen state shape includes one;
  - no result records a content hash that was not written or proven equal.
- Fail the command before planning side effects when global state JSON is
  unreadable/malformed; degrade malformed per-path provenance to untrusted.

### 4.4 Integrate lifecycle decisions into planning

- Extend `WriteResult` with lifecycle and applied-content metadata sufficient
  for summaries and state construction.
- Replace `_plan_file`'s force-only matrix with:
  1. repository-local current-content read;
  2. prior entry extraction;
  3. pure lifecycle classification;
  4. status-specific actionable message construction.
- Preserve the existing equality shortcut while using the shared exact output
  normalization/hash contract.
- Add `managed_only` and `reset_project_knowledge` plan inputs.
- In managed-only mode, include managed rendered files and applicable safe
  compositions/directories, exclude seeded creation/update/reset and obsolete
  migration processing, and retain all omitted state entries.
- Keep project-owned path reporting and composition conflict semantics intact.

### 4.5 Protect obsolete files with provenance

- Replace force-only `_plan_obsolete_file` with lifecycle-aware retirement:
  - missing: no result;
  - directory: preserve/block with actionable status;
  - unchanged according to prior applied hash: plan `deleted`;
  - drifted, untracked, or malformed provenance: plan
    `migration_required`, include its migration target/hint, and preserve it.
- Do not make explicit knowledge reset bypass retirement checks.
- Keep repository/symlink boundary validation before content hashing/deletion.

### 4.6 Strengthen applier preflight

- Aggregate both `conflict` and `migration_required` before iterating results.
- Raise one actionable `PlanConflictError` before creating directories, writing
  files, composing content, resetting seeds, or deleting retired paths.
- Write only statuses declared writable by `core.lifecycle`; explicitly skip
  preserved/skipped/unchanged/blocking results.
- Keep the approved preflight guarantee and do not add transactional rollback
  or backups.

### 4.7 Redesign CLI consent and summary

- Change `--force` help to “update divergent bootstrap-managed files”; remove
  language implying that it resets every generated file.
- Add `--managed-only`.
- Add `--reset-project-knowledge` plus
  `--confirm-reset-project-knowledge "RESET PROJECT KNOWLEDGE"` for real apply.
  Dry-run permits reset preview without the confirmation value.
- Validate reset confirmation before target creation or any apply/state write.
- Load state before building the plan and pass it through state merge after
  successful apply.
- Add lifecycle/category to the CLI summary and group or clearly label managed
  changes, seeded safe updates, preserved knowledge, reset operations,
  compositions, migration requirements, and conflicts.

### 4.8 Separate TUI managed update and reset

- Rename the current overwrite control to describe managed-file update.
- Add a distinct reset checkbox/control, reset-specific confirmation input, and
  localized English/pt-BR explanations.
- Require both ordinary `APPLY` and exact `RESET PROJECT KNOWLEDGE` when a real
  plan requests seeded reset; keep reset off by default.
- Add lifecycle/category to preview rows so every affected seeded owner is
  visible before reset.
- Reuse pure plan metadata/confirmation helpers; do not place lifecycle policy
  in widget handlers or undertake a broad TUI refactor.

### 4.9 Add recovery-aware generated policy and checker

- Update template-pack `AGENTS.md`, `docs/LIVING_DOCUMENTATION.md`, and the
  generated `living-docs` skill with the compact recovery contract from the
  approved spec.
- Preserve existing word budgets by keeping the always-read skill/AGENTS rules
  short and placing detailed recovery guidance in the policy/checker help.
- Add generated
  `.agents/skills/living-docs/scripts/check_living_docs.py` using only the
  standard library.
- Implement current-tree checks for:
  - scaffold/baseline contradictions with verified capabilities;
  - seed placeholders mixed with established capability content;
  - architecture reduced to docs-only despite substantive source areas;
  - legacy state marking seeded owners overwritten;
  - empty-seed equality conflicting with available prior-evolution evidence;
  - invalid capability states and active placeholder links.
- Add optional `--baseline-ref` Git comparison for coverage downgrade, removed
  capability identity, and verified-row removal diagnostics. If Git/ref is
  unavailable, report the skipped comparison without weakening current-tree
  checks.
- Keep `check_links.py` independent and invoke both checkers from the skill when
  their respective risk/structure conditions apply.

### 4.10 Add focused regression fixtures and contract tests

- Add `tests/test_lifecycle.py` for a table-driven pure decision matrix and
  normalization/hash rules.
- Expand manifest tests for explicit default lifecycles, invalid values,
  normalized lifecycle reporting, migration hints, and version 0.5.0.
- Expand state tests for old-state compatibility, unknown fields, malformed
  entries, provenance recording, selective merge, and retirement inventory.
- Expand planner/applier tests for managed, untouched seeded, evolved seeded,
  no-state seeded, safe seed upgrade, explicit reset, managed-only, blockers,
  symlinks, compositions, and no-write preflight.
- Add a self-contained 0.4.0 incident fixture under `tests/fixtures/` or build it
  in a focused test helper; do not read the live affected repository.
- Expand CLI/TUI tests for help, lifecycle summaries, separate consent,
  localized labels, dry-run reset preview, confirmation failure, and state
  preservation.
- Test the generated semantic checker directly against minimal temporary repos,
  including optional Git-baseline comparisons.
- Avoid full Markdown snapshots and private-helper assertions; protect public
  decisions, diagnostics, and persisted invariants.

### 4.11 Close durable knowledge and release documentation

- Update README and source product/architecture/capability owners after the
  behavior is proven.
- Replace the capability's destructive 0.4.0 current-state evidence with the
  validated lifecycle-aware state only at closeout; remove the active change
  after distillation.
- Document the read-only audit/recovery procedure for previously affected
  projects without claiming those projects were repaired.
- Run link and semantic checkers against both this repository and a freshly
  generated temporary repository.

## 5. Module Boundaries

- `core.lifecycle`: owns lifecycle vocabulary, hashing normalization, decision
  matrix, and writable/blocking status sets.
- `core.template_pack`: owns manifest schema/defaults/validation only.
- `core.state`: owns compatible state parsing and provenance merge only.
- `core.planner`: owns filesystem observation and conversion of lifecycle
  decisions into visible plan results.
- `core.applier`: owns blocker preflight and execution of eligible results; it
  must not infer ownership or drift.
- CLI/TUI: own selection, confirmation, localization, and presentation; they
  must not reimplement lifecycle rules.
- Generated policy/checkers: own agent recovery procedure and objective
  documentation diagnostics; the engine must not interpret project prose.
- Git comparison remains optional inside the checker and must not enter normal
  apply planning.

## 6. Architecture Locality

- Primary module or owner: new `core.lifecycle` policy consumed by existing
  template-pack/state/planner/applier boundaries.
- Files expected to change: lifecycle core, template parser, planner, state,
  applier, CLI/TUI/text, default manifest/templates/checker, focused tests,
  README and living owners.
- Files that should not be touched: scanners, renderers, project discovery,
  composer algorithms, spec-driven artifact semantics, packaging dependencies,
  and the live affected project.
- New boundaries introduced: pure lifecycle decision module and generated
  semantic checker.
- Existing boundaries preserved: manifest describes, planner observes/plans,
  applier executes, state persists, adapters confirm/present.
- Why this is the smallest maintainable change: the incident crosses these
  surfaces because lifecycle affects declaration, prior evidence, planning,
  execution, consent, and generated policy; centralizing the decision prevents
  shotgun rule duplication.
- Are the affected files all part of the same conceptual area? Yes: bootstrap
  file ownership/application plus its generated recovery contract.
- Does this change require edits across unrelated areas? No; UI, tests and docs
  are consumers of the same lifecycle contract.
- If yes, is that expected or a sign of weak boundaries? Not applicable.
- Should we refactor before, during, or after this change? Extract the pure
  lifecycle boundary first, then integrate locally. No separate broad refactor.

## 7. Data / API / Interface Impact

- Manifest file entries gain `lifecycle`; obsolete entries gain an optional
  migration target/hint. Omitted file lifecycle defaults to `managed`.
- `TemplateFileSpec`, related manifest specs, `WriteResult`, and `BootstrapPlan`
  gain lifecycle/reset/selection metadata.
- `build_plan` accepts prior file provenance plus managed-only/reset selection.
- State per-file entries gain lifecycle, `applied_content_hash`, and
  `applied_version`; old state remains readable.
- `build_state` accepts prior state and merges instead of replacing its
  inventory.
- CLI gains `--managed-only`, `--reset-project-knowledge`, and reset
  confirmation; `--force` retains its spelling with safer semantics.
- TUI gains a distinct reset control and confirmation.
- Plan result statuses add `reset` and `migration_required`; summaries expose
  lifecycle/category.
- Default pack becomes 0.5.0 and generates `check_living_docs.py`.

## 8. Security / Privacy Impact

- The change reads only declared repository-local files, state, templates, and
  optional local Git history.
- Existing path normalization and symlink containment must cover hashing and
  retirement, not only writes.
- State stores hashes/provenance rather than document bodies.
- Semantic checker performs no network calls and must not print full document
  contents in diagnostics.
- No secrets, tokens, user payloads, external APIs, backups, or new permissions
  are introduced.
- Manifest and state inputs are treated as untrusted enough to validate types,
  lifecycle values, and repository containment before mutations.

## 9. Dependency Impact

- No dependency is added. Hashing, JSON parsing, subprocess-based optional Git
  comparison, and checkers use the Python standard library.
- Existing `textual` remains the optional TUI dependency; no new widget package
  is required.

## 10. Risks

- Incorrect normalization could classify edited content as untouched or vice
  versa. Mitigation: one shared exact-output hash contract with LF/trailing
  newline fixtures.
- State merge could retain stale entries or claim unapplied provenance.
  Mitigation: explicit transition tests for every result status and selective
  mode.
- Backward-compatible default `managed` could be unsafe for external packs that
  implicitly treated living files as managed. Mitigation: compatibility keeps
  old behavior but default pack is fully explicit; README warns pack authors to
  classify seed-once knowledge.
- Reset confirmation could drift between CLI and TUI. Mitigation: one constant
  and pure validation helper.
- Migration blockers may stop upgrades that formerly deleted files. This is an
  intentional fail-closed outcome with actionable destination guidance.
- Semantic checker may produce false positives. Mitigation: limit it to
  objective contradictions/risk signals, offer baseline comparison explicitly,
  and never auto-edit.
- TUI size/mixed responsibilities could worsen. Mitigation: small adapter-only
  changes and no lifecycle logic in event handlers.
- A known blocker could still be followed by partial writes if preflight is
  incomplete. Mitigation: central blocking statuses and an applier test proving
  no directory/file/state mutation.

## 11. Validation Strategy

- Run lifecycle decision-table tests first, then state/manifest tests, then
  planner/applier integration tests.
- Validate CLI and TUI consent/presentation without requiring interactive
  manual input.
- Reproduce the 0.4.0 incident in a temporary fixture and prove both ordinary
  and forced upgrades preserve seeded owners while managed files update.
- Generate fresh Python and Rust temporary repositories, evolve seeded owners,
  reapply 0.5.0, and validate state hashes, compositions, semantic checks, and
  links.
- Run:
  - `python3 -m unittest discover -s tests -v`;
  - `python3 -m compileall -q ai_workflow_bootstrap`;
  - `python3 -m json.tool ai_workflow_bootstrap/template_packs/default/manifest.json`;
  - generated `check_living_docs.py` and `check_links.py` on temporary output;
  - `git diff --check`.
- Treat `python -m build` as an additional packaging check when the environment
  provides a working build backend; the standard-library validation path is
  required regardless.

## 11.1 Test Strategy

- Contract to protect: lifecycle ownership and provenance—not private helper
  shapes—determine whether each path is written, preserved, reset, retired, or
  blocked.
- Tests to add or update: decision matrix, manifest schema, compatible state
  merge, incident fixture, planner/applier preflight, CLI/TUI consent and
  summary, semantic checker, template output, and fresh/reapply integration.
- Tests intentionally not added: full rendered-document snapshots,
  implementation-specific call ordering outside the no-write preflight, Git
  worktree cleanliness, backup behavior, or automatic semantic merge.
- Why these tests should survive internal refactors: they assert public statuses,
  file bytes, state invariants, CLI/TUI behavior, diagnostics, and acceptance
  criteria rather than helper names or internal branching.

## 12. Living Documentation Impact

- Product fact owner(s) to update: `docs/product/README.md` for current
  destructive apply and approved safe-upgrade/reset contract; generated product
  seed remains a seed, not the source of this tool's implementation truth.
- Architecture fact owner(s) to update: `docs/architecture/README.md` for
  current manifest/planner/applier/state flow and, at closeout, the lifecycle
  policy/provenance boundary.
- Current state/evidence changes: none during planning; current 0.4.0 force
  behavior stays `verified` from code/tests and incident evidence.
- Approved target/active-change changes: record lifecycle-safe upgrade and this
  change now; clear active change only after validation.
- Roadmap/decision changes: no roadmap ordering is needed for this isolated
  approved correction; add a durable decision only if implementation exposes a
  meaningful alternative not already settled by the spec.
- Links/evidence to validate: spec/plan/tasks links, product/architecture links,
  generated skill/checker links, test evidence, and README commands.
- Why no living-doc update is needed, if applicable: not applicable; the target
  is recorded before implementation and current state is preserved.

## 13. Execution Steps

1. Add pure lifecycle/hash policy and its complete decision-table tests.
2. Extend manifest schema/validation, explicitly classify the 0.5.0 default
   pack, and test pack compatibility.
3. Make state parsing/merge provenance-aware and test legacy/selective paths.
4. Integrate lifecycle and prior provenance into planner results.
5. Implement safe obsolete retirement and applier blocker preflight.
6. Add CLI managed-only/reset consent and lifecycle summaries.
7. Add TUI managed/reset separation, confirmation, localization, and preview.
8. Update generated policies and add/test the semantic checker.
9. Add the self-contained incident and fresh/reapply integration fixtures.
10. Run focused/full validation and correct only spec-relevant regressions.
11. Distill proven behavior into README and living owners, clear the active
    change, close tasks, and rerun semantic/link/diff checks.

## 14. Rollback / Recovery

- Implementation is additive until default manifest lifecycle and UI semantics
  change; keep commits/edits logically grouped so the whole unvalidated change
  can be reverted through Git by the project owner.
- The tool itself creates no backup, commit, branch, or stash.
- Before apply, lifecycle preflight preserves all seeded/project knowledge on
  uncertain provenance.
- If a 0.5.0 state write fails after file application, rerunning is safe because
  current rendered equality can re-establish provenance for exact outputs;
  evolved seeded files remain conservative.
- If lifecycle classification is found unsafe during validation, do not ship a
  permissive fallback: revert the lifecycle integration or preserve/block.
- Repair of already damaged downstream projects follows the documented audit
  process and remains separate from bootstrap reapplication.

## 15. Notes

- This plan deliberately does not add a generic group filter. `--managed-only`
  satisfies the approved minimum selective-upgrade contract without reopening
  partial workflow modes. A future group filter can reuse the same state merge
  and lifecycle policy.
- Reset confirmation uses the shared exact phrase `RESET PROJECT KNOWLEDGE` in
  CLI and TUI.
- `migrated` means guarded retirement/disposition in this version, not automatic
  semantic prose merge.
- The repository-local `.agents` skill copy is workspace-managed/read-only;
  implementation changes the default-pack source that downstream repositories
  receive.
