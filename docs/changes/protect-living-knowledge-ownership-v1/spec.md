# Change Spec: Protect Living Knowledge Ownership v1

## 1. Summary

Change the bootstrap from path-level generation with one global overwrite rule
to lifecycle-aware planning. Infrastructure owned by the bootstrap may still be
upgraded explicitly, but living-knowledge scaffolds become project knowledge
after creation and cannot be replaced merely because `--force` was selected.

The change also makes prior applied content traceable, blocks unsafe deletion
of evolved obsolete files, separates ordinary upgrade from an explicit
knowledge reset, strengthens the generated `living-docs` recovery procedure,
and adds deterministic checks for objective documentation regressions.

This spec responds to the confirmed 0.4.0 incident in
`text-online-mmorpg`, where `--force` replaced established product,
architecture, capability, roadmap and index content with rendered scaffolds.
It corrects the engine and generated policy; it does not reconstruct that
project's lost knowledge in this change.

## 2. Problem

The current default manifest places permanently managed workflow files and
seed-once living documents in the same `files` collection without lifecycle
metadata. The planner decides only whether a file exists, matches the newly
rendered template, and whether global `force` is true. Therefore `--force`
replaces every divergent declared file, regardless of who owns its evolved
content.

The current state records template provenance but not the hash of the rendered
content actually applied. It cannot distinguish an untouched seed from a file
that the project has developed. State is also rebuilt from the latest result
set rather than explicitly preserving useful prior provenance, which would be
unsafe once selective updates are supported.

Obsolete paths are deleted under `--force` solely because the pack declares the
path obsolete. No check establishes that the file is still the unmodified
bootstrap output. A formerly generated document may now contain the only copy
of project knowledge.

The generated agent policy and `living-docs` skill assume the current index and
owners are trustworthy entry points. They do not recognize recent bootstrap
replacement, a coverage downgrade, or unexpectedly truncated product and
architecture documents as recovery signals. The link checker validates paths,
not truth-preserving invariants.

## 3. Goal

- Make normal bootstrap upgrades incapable of erasing evolved living
  documentation.
- Keep explicit upgrades of bootstrap-owned policy, skills and templates
  possible without requiring a project-knowledge reset.
- Base safe seeded-file updates and obsolete-file deletion on recorded applied
  content, not on path names or template hashes alone.
- Make destructive knowledge reset a separate, unmistakable operation.
- Detect objective signs of living-document regression and teach agents how to
  recover the union of established and new knowledge.
- Preserve compatibility conservatively for projects whose 0.4.0 state lacks
  applied-content hashes.

## 4. Scope

### 4.1 Lifecycle-aware template pack

The engine must expose these normalized lifecycle concepts:

- `managed`: the bootstrap remains authority for the declared file; divergent
  content changes only under explicit managed overwrite (`--force`).
- `seeded`: the bootstrap creates the initial file and may update it only while
  state proves the project has not changed the last applied content.
- `project`: an existing path belongs entirely to the project and is never
  created, replaced or deleted by the bootstrap.
- `composed`: bootstrap-owned fragments are merged by an existing explicit,
  idempotent composition strategy while other repository content is preserved.
- `migrated`: a retired path requires a declared migration/disposition policy;
  drift blocks automatic deletion.

These concepts do not need to force unlike operations into one manifest list.
`files` entries use explicit `lifecycle: managed|seeded`;
`project_owned_paths`, `compositions`, and `obsolete_files` retain their
cohesive schemas but expose normalized `project`, `composed`, and `migrated`
lifecycle in plans/state where applicable.

For backward compatibility, a third-party or older manifest file entry without
`lifecycle` defaults to `managed`. Every file entry in the default pack must be
explicit so its ownership is reviewable.

Default-pack classification:

- `managed`: `AGENTS.md`, workflow and living-documentation policy guides,
  change artifact templates, decision template, generated skills/scripts, and
  the stack-specific Rust development policy.
- `seeded`: `docs/INDEX.md`, `docs/CAPABILITIES.md`, product and architecture
  owners, decision index, roadmap, idea inbox, and glossary.
- `project`: `AGENTS.project.md` through the existing protected-path mechanism.
- `composed`: `Makefile` and `.gitignore` through their existing composition
  mechanisms.
- `migrated`: declared obsolete documentation paths.

### 4.2 Applied-content provenance and drift

For each rendered file the state must be able to retain:

- template path and `template_hash`;
- normalized lifecycle;
- `applied_content_hash` of the exact rendered content last written or proven
  equal to the current file;
- pack version that established that applied content.

The planner must load prior state before classifying lifecycle-sensitive
operations. Hash comparison uses the bytes/text normalization the writer
actually persists; template source hashes are not substitutes for rendered
content hashes.

State updates must merge retained provenance for preserved/skipped and
unselected paths instead of erasing it. Confirmed deletion removes the retired
path's active inventory entry while retaining any operation record needed for
diagnosis. Dry-run never changes state.

State files from 0.4.0 and earlier remain readable. Unknown extra fields remain
tolerable where practical. Missing or malformed per-file provenance is handled
per path and does not authorize destructive behavior.

### 4.3 Planning matrix

`managed`:

- missing: create;
- equal to newly rendered content: unchanged and record/refresh applied hash;
- divergent without `--force`: skip;
- divergent with `--force`: overwrite.

`seeded`:

- missing: create;
- equal to newly rendered content: unchanged and record/refresh applied hash;
- current content equals prior `applied_content_hash`: safely update to a new
  rendered seed when the pack changed;
- current content differs from prior `applied_content_hash`: preserve as
  project-evolved, including under `--force`;
- existing file with absent/unusable prior applied hash: preserve
  conservatively, including under `--force`, unless it already equals the newly
  rendered content;
- only the separate knowledge-reset operation may replace an evolved or
  untracked seeded file.

`project` is always preserved when it exists and never created by the pack.
`composed` continues to use its declared safe composer; `--force` does not
bypass composition conflicts.

Every plan result must expose lifecycle and an unambiguous status/message.
Seeded drift uses `preserved`, not `skipped` or `unchanged`, and explains that
project knowledge was detected. Unsafe retirement uses
`migration_required`, not `deleted` or a generic conflict.

### 4.4 Safe retirement of obsolete paths

An obsolete declaration must support a destination/disposition hint. It does
not imply that the engine can merge arbitrary prose.

An obsolete file may be automatically deleted only when prior state contains a
usable applied-content hash and the current file still matches it. If the file
drifted, state is missing, or provenance is unusable, planning returns
`migration_required`, preserves the file, identifies the expected destination
when declared, and blocks real application before any write or deletion.

Directories continue to be non-recursive and non-deletable. A symlink must not
permit reads or mutations outside the repository boundary.

No general semantic migration framework is introduced in this version.
Content migration remains an explicit reviewed operation whose completion can
later make the retired scaffold safely disposable.

### 4.5 Force, selective upgrade, and knowledge reset

`--force` changes meaning from “overwrite every divergent generated path” to
“update divergent `managed` files.” It never overrides evolved `seeded`,
`project`, composition conflicts, or `migration_required`.

CLI must support a safe selective upgrade mode for managed infrastructure. The
minimum interface is `--managed-only`; a repeatable manifest-group filter may
also be added during planning if it remains simple and applies the same
lifecycle rules. Selective application must not discard state for paths outside
the selection.

Knowledge reset is a separate option named `--reset-project-knowledge` and
affects only paths declared `seeded` by the active pack. For a real CLI apply it
requires a second explicit confirmation value; dry-run may preview without that
confirmation. It never affects arbitrary project files, `project` paths,
composed content, or drifted obsolete files.

The TUI must present ordinary bootstrap update and project-knowledge reset as
separate controls. Reset is off by default, lists each affected seeded owner,
uses a distinct destructive category, and requires a reset-specific typed
confirmation in addition to the normal apply confirmation.

No clean-worktree requirement, automatic commit, stash, branch, or backup is
added. Git is useful recovery evidence but is not the ownership mechanism.

### 4.6 Atomic preflight

The applier must refuse a real application before any write when the complete
plan contains `conflict` or `migration_required`. It must never write
`preserved`, `skipped`, `unchanged`, `conflict`, or `migration_required`
results.

This requirement is preflight atomicity: known blockers cannot be discovered
after unrelated owners were already updated. It does not promise a
cross-filesystem transactional rollback for unexpected I/O failure.

### 4.7 Generated policy and recovery-aware living-doc skill

The source templates for `AGENTS.md` and the `living-docs` skill must state:

- bootstrap reapplication is infrastructure maintenance, not living-doc
  closeout;
- a reviewed or repository-edited seeded owner is project knowledge;
- established current state, evidence, capability rows, product intent, and
  architecture cannot be removed without explicit disposition;
- when an owner appears regenerated, truncated, or downgraded, inspect
  `.ai-bootstrap/state.json` and relevant Git history/evidence before trusting
  it;
- unexpected coverage reduction triggers restoration/audit of the entire owner
  before a narrow change closeout;
- recovery combines still-valid prior facts with later verified increments;
  it does not blindly restore an old version or mark unsupported prose as
  verified;
- closeout must account for facts added, changed, and removed, with an explicit
  disposition for each intentional removal.

The skill must stay within its existing compact context budget. Detailed
recovery and validation guidance belongs in the generated living-documentation
policy or checker help rather than duplicating long prose in always-read files.

### 4.8 Deterministic living-document regression checker

Add a standard-library-only `check_living_docs.py` beside `check_links.py`.
It detects objective contradictions and risk signals; it does not claim that
documentation is complete or semantically true.

At minimum it checks:

- `scaffold` or “baseline not established” coexisting with verified capability
  evidence;
- known seed placeholders coexisting with non-placeholder capability content;
- architecture listing only documentation while the repository scanner finds
  substantive source areas;
- seeded living owners marked `overwritten` by a recent legacy bootstrap state;
- current seeded owners identical to empty seed templates when state/evidence
  indicates prior project evolution;
- malformed capability state values or placeholder contract links in active
  non-placeholder rows.

When given an explicit Git baseline/reference, it also reports coverage-status
downgrades, removed capability identities, and removal of `verified` rows
without a current deprecated/disposition signal. It reports diagnostics for
human/agent review rather than automatically rewriting prose.

`check_links.py` remains focused on links. The generated skill runs both checks
after structural recovery or closeout when applicable.

### 4.9 Incident fixture and upgrade compatibility

Tests must include a repository fixture representing the relevant 0.4.0
incident shape: seeded owners with established content, legacy state containing
template hashes/statuses but no applied-content hashes, and a normal forced
upgrade. The upgrade must preserve those owners while updating managed files.

A second fixture covers a clean untouched scaffold so a corrected pack can
adopt provenance and later update it safely. Tests must not depend on the live
`text-online-mmorpg` checkout.

### 4.10 Documentation and release contract

Update README, CLI/TUI help, template pack version, state documentation,
generated policies, and source living docs after implementation evidence
exists. The durable capability map must keep current 0.4.0 behavior separate
from the approved target until validation closes this change.

Provide an explicit read-only audit/recovery procedure for already affected
projects. Repairing their product knowledge remains a separate project-local
task.

## 5. Out of Scope

- Reconstructing `text-online-mmorpg` living docs in this repository change.
- Inferring complete product intent or architecture automatically.
- Automatically merging arbitrary Markdown prose.
- Treating Git as the sole source of truth or requiring a Git repository.
- Creating backups, commits, branches, stashes, or enforcing a clean worktree.
- Transactional rollback after an unexpected filesystem/OS write failure.
- Deleting arbitrary user-selected paths or recursively deleting directories.
- Redesigning the spec-driven approval workflow.
- Adding third-party dependencies, a database, embeddings, or network services.

## 6. Users / Actors

- Project owners installing or upgrading the bootstrap.
- AI agents maintaining and recovering living project knowledge.
- Template-pack maintainers classifying ownership and migrations.
- Contributors reviewing destructive previews and migration blockers.

## 7. Functional Requirements

1. Every default-pack output path has an explicit, reviewable normalized
   lifecycle.
2. Missing seeded documents are created on first application.
3. An untouched seeded document may receive a later safe template update when
   its current content matches recorded applied content.
4. An evolved seeded document is preserved under ordinary apply and `--force`.
5. Existing seeded content without usable applied provenance is preserved
   conservatively unless it already equals the new rendered seed.
6. Managed divergent files remain skipped without `--force` and are updated
   with `--force`.
7. Project-owned paths are never created, overwritten, reset, or deleted.
8. Composed files preserve repository content and block incompatible
   definitions regardless of force/reset flags.
9. State records lifecycle, rendered applied-content hash, template provenance,
   and applied pack version for eligible files.
10. State merging preserves provenance for unselected and preserved paths.
11. Older state without new fields remains readable and cannot grant overwrite
    authority.
12. Obsolete files are deleted automatically only when state proves they are
    unchanged bootstrap output.
13. Drifted or untracked obsolete files produce `migration_required`, remain
    on disk, and block all real writes for that plan.
14. `--force` never resets seeded knowledge.
15. CLI managed-only selection updates no seeded files and does not lose their
    state.
16. Project-knowledge reset is a separate CLI/TUI action, affects only seeded
    paths, and requires reset-specific confirmation for real apply.
17. Preview and final summaries group or label managed updates, seeded safe
    updates, preserved project knowledge, composed updates, reset candidates,
    migration requirements, and conflicts distinctly.
18. The applier rejects known blockers before any write/deletion and never
    applies non-writable statuses.
19. Generated policy and skill instruct agents to detect and recover recent
    owner regeneration before local closeout.
20. The semantic checker catches the minimum objective invariants in section
    4.8 and returns non-zero when blocking regressions are found.
21. Existing link checking continues to work independently.
22. A 0.4.0 incident fixture proves normal/forced upgrade preserves established
    seeded owners while updating eligible managed infrastructure.
23. Fresh bootstrap behavior and safe composition remain supported.
24. README and both user interfaces accurately explain lifecycle, force,
    reset, preservation, and migration-required behavior.

## 8. Non-Functional Requirements

### Modularity / Architecture

- Lifecycle decision rules must live in a small pure/testable policy boundary,
  rather than expanding `_plan_file` into a matrix coupled to CLI/TUI text.
- Template parsing owns manifest validation; state owns compatible provenance
  loading/merging; planning owns classification; applying executes only an
  already valid plan; UI layers own consent and presentation.
- Composition remains separate from arbitrary prose-file lifecycle logic.

### Security / Privacy

- All generated, retired, state, and comparison paths remain repository-local;
  symlinks cannot escape the target boundary.
- Checkers read local repository data only and never send content over the
  network.
- State stores hashes and provenance, not copies of project documents or
  sensitive payloads.
- Existing secret/private-data prohibitions remain.

### Reliability

- Destructive authority is fail-closed when provenance is missing or invalid.
- Dry-run and real apply build the same lifecycle classifications for the same
  inputs.
- Known blockers prevent partial application before writing begins.
- State is written only after successful application and never claims an
  unapplied content hash.

### Performance

- Hashing is linear in declared file size and limited to repository-local
  declared paths; no full repository content index is required for apply.
- Git comparison is opt-in for the semantic checker, not part of every normal
  bootstrap plan.

### Observability

- Results expose lifecycle, drift reason, and why an operation is writable,
  preserved, reset, or blocked.
- State and checker diagnostics are sufficient to audit a potentially affected
  project without retaining document copies.

### Simplicity

- No generic prose merge engine or migration DSL is introduced.
- Prefer one explicit decision matrix and focused contract tests over scattered
  path-name exceptions.

## 9. Maintainability Impact

- Does this change make future changes easier or harder? Easier after the
  lifecycle matrix is centralized; harder if drift rules are duplicated in
  planner, state, CLI, and TUI.
- Touched architecture: manifest parsing, lifecycle policy, state provenance,
  planner/applier, CLI/TUI consent and summaries, generated docs/skills/checker.
- Potential entropy: `planner.py` is already about 300 lines and `tui.py` about
  455 lines; adding the matrix inline would mix policy and presentation. The
  current `test_template_pack.py` is also broad and should not become the sole
  owner of lifecycle behavior tests.
- Refactor needed before coding: planned local extraction of pure lifecycle
  classification/hash helpers and focused lifecycle/state tests.
- Refactor scope: local to this change. A broader TUI framework rewrite is not
  justified.

Maintainability-audit classification:

- planned local refactor: extract lifecycle/drift decisions from planner and
  keep reset confirmation as a small UI adapter over plan metadata;
- safe local cleanup: centralize writable/blocking status sets used by applier
  and summaries;
- separate refactor spec: none currently required;
- tests to keep: public planner/applier, path-boundary, CLI/TUI and composition
  contract tests;
- tests to add/rewrite: decision-matrix tables, state compatibility/merge,
  legacy incident fixture, reset consent, migration blocking, and semantic
  checker behavior; avoid asserting full prose snapshots.

## 10. Living Documentation Impact

- Product fact owner(s): `docs/product/README.md` after approval/implementation,
  for safe bootstrap upgrade and explicit reset behavior.
- Architecture fact owner(s): `docs/architecture/README.md` after
  implementation, for lifecycle policy, state provenance and plan/apply flow.
- Current capability state/evidence affected: current destructive 0.4.0
  overwrite behavior remains the current fact until tests prove the new
  contract.
- Approved target and active change: add this change to
  `docs/CAPABILITIES.md` only after spec approval.
- Roadmap or durable decisions affected: roadmap only if the user approves its
  ordering; lifecycle ownership may merit a decision during planning if the
  implementation reveals a durable alternative.
- Documents intentionally unchanged at this gate: all living owners; this spec
  is temporal history and does not claim implementation.

## 11. User Flow / System Flow

### Safe upgrade

1. User previews or applies normally, optionally with `--force` for managed
   infrastructure.
2. Bootstrap loads the pack, profile, and prior state.
3. Lifecycle policy compares current, rendered, and prior applied hashes.
4. Managed updates and untouched seeded updates are planned; evolved seeded
   knowledge is visibly preserved.
5. Any conflict or migration requirement blocks the real apply before writes.
6. Applier executes eligible results and state merges proven new provenance.

### Explicit knowledge reset

1. User selects the separate reset option and previews affected seeded owners.
2. UI lists only seeded files that would be replaced.
3. Real apply requires reset-specific confirmation.
4. Planner still preserves project-owned/composed paths and blocks unsafe
   obsolete migrations.
5. Successfully reset seeded files receive new applied-content provenance.

### Recovery audit

1. Agent/checker notices legacy `overwritten` seeded owners, a downgrade, or
   internal contradictions.
2. Agent inspects state, Git history when available, current change artifacts,
   and current code/tests/runtime evidence.
3. Agent reconstructs the union of still-valid prior facts and later supported
   increments, with explicit disposition for removals.
4. Agent restores an honest coverage status, runs semantic and link checks, and
   does not promote unsupported recovered prose to `verified`.

## 12. Edge Cases

- Existing file equals the newly rendered seed but prior state is absent: mark
  unchanged and establish provenance without rewriting.
- Existing file equals an old applied hash while the new seed changed: safe
  seeded update.
- Existing file was changed and later changed back byte-for-byte to the applied
  version: it is operationally indistinguishable from untouched and may update.
- Line-ending or trailing-newline differences follow the documented writer/hash
  normalization and must be tested.
- State JSON is malformed globally: fail with actionable error rather than
  silently assuming destructive authority.
- One per-file entry is malformed: preserve that path and report unusable
  provenance; do not necessarily block unrelated safe managed updates unless
  the path requires migration/reset.
- Pack removes or renames a formerly tracked path: retirement rules apply; the
  old entry is not silently dropped from state before disposition.
- Selective update omits a previously tracked stack-specific path: retain its
  state provenance.
- Reset flag is used in dry-run without confirmation: preview is allowed; no
  write/state change occurs.
- Reset flag is used for real apply without exact confirmation: reject before
  planning/application side effects.
- Target is not a Git repository: lifecycle protection still works; baseline
  comparison diagnostics explain that Git-specific checks were skipped.
- Narrow change closes while an entire owner was regenerated: recovery/audit
  precedes closeout of that owner.

## 13. Constraints

- Python standard library only for engine and generated checker additions.
- Preserve repository-relative path and symlink protections.
- Preserve the two explicit spec-driven approval gates.
- Do not modify the affected `text-online-mmorpg` repository in this change.
- Do not write plan/tasks or implementation before explicit approval of this
  spec.

## 14. Assumptions

- The default pack is the only bundled pack, but parser defaults should avoid
  unnecessarily breaking external packs.
- Exact applied-content hashes are sufficient for safe automatic drift
  detection; they do not prove semantic correctness.
- A separate explicit reset is occasionally useful for intentionally returning
  seeded owners to scaffolds, but it should never be needed for a normal
  upgrade.
- Existing composition mechanisms are already the correct ownership model for
  `Makefile` and `.gitignore`.

## 15. Acceptance Criteria

1. A normal upgrade, including `--force`, cannot overwrite an evolved seeded
   living owner.
2. `--force` updates eligible managed files without resetting project
   knowledge.
3. The manifest and normalized plan/state represent lifecycle/ownership for
   every default-pack path.
4. State records and safely merges applied rendered-content provenance.
5. Old or missing provenance fails closed for seeded overwrite and obsolete
   deletion.
6. Drifted obsolete documents remain intact and block apply as
   `migration_required` before any write.
7. Reset is a separate, reset-specific-confirmed CLI/TUI action and affects
   only seeded owners.
8. Selective managed updates retain state for all unselected owners.
9. CLI/TUI preview makes ownership and destructive impact unmistakable.
10. Generated `AGENTS.md` and `living-docs` procedures recognize regeneration,
    downgrade, and truncation as recovery signals.
11. The semantic checker detects the objective contradictions/regressions in
    section 4.8 without claiming completeness.
12. Regression tests reproduce the 0.4.0 incident shape and prove the corrected
    upgrade preserves established knowledge.
13. Fresh, untouched, evolved, state-less, selective, reset, obsolete-drift,
    composition-conflict, symlink, and dry-run paths have contract-level tests.
14. Full test suite, compile check, manifest validation, generated semantic/link
    checks, and `git diff --check` pass.
15. Durable product/architecture/capability docs are updated only after the
    implementation is validated, with current and approved-target state kept
    separate throughout.

## 16. Open Questions

No question blocks spec approval. Exact CLI spelling for the reset confirmation
value and whether group filtering ships alongside `--managed-only` are planning
details, provided they satisfy the consent and state-preservation contracts
above.
