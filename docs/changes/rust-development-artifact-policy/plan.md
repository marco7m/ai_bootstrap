# Implementation Plan: Unified bootstrap workflow and conditional project policies

## 1. Summary

Add a small declarative extension to the template-pack contract so files,
context fragments and safe compositions can be selected by detected stack.
Use that extension to generate Rust-only Make targets, a Cargo ignore rule, a
focused development document and one compact `AGENTS.md` instruction. Preserve
all non-Rust output and all user-owned content outside explicitly managed
composition boundaries.

Collapse workflow selection to the recommended spec-driven plus living-docs
combination so every generated repository receives one coherent knowledge and
change-management contract.

Separate bootstrap-owned and project-owned agent instructions so synchronizing
the managed scaffold never erases durable repository-specific working rules.

## 2. Relevant Existing Context

- `core.scanner` already detects `Cargo.toml`, records `rust` and parses Make
  target names.
- `core.template_pack` owns manifest deserialization into typed specifications.
- `core.planner` owns render context, path resolution, statuses and preview
  ordering; `core.applier` only executes an already-built plan.
- The default manifest currently supports full files, directories, groups and
  obsolete files, but no stack conditions or composed writes.
- Generated `AGENTS.md` and `docs/architecture/README.md` already consume
  scanner-derived placeholders.
- CLI and TUI share `BootstrapPlan`/`WriteResult`, so composition results can be
  made visible without a second preview mechanism.
- State records file statuses and template provenance after successful apply.
- `core.workflow`, CLI flags and the TUI mode selector currently expose three
  workflow combinations even though the target product wants only recommended.
- Every manifest file is currently treated as bootstrap-owned: `--force` may
  replace it when content differs, and state has no project-owned distinction.

## 3. Existing Conventions Found

- Folder structure: engine behavior under `ai_workflow_bootstrap/core/`, pack
  policy under `template_packs/default/`, contract tests under `tests/`.
- Naming style: dataclass manifest specs, small formatting functions and
  underscore-prefixed planner helpers.
- Error handling: invalid target inputs raise `ValueError`; preview results use
  explicit statuses and messages.
- Logging: user-visible CLI/TUI summaries; no internal logging subsystem.
- Testing pattern: standard-library `unittest`, temporary repositories and
  assertions on public plan/application behavior rather than prose snapshots.
- Config pattern: JSON manifest parsed into frozen dataclasses.
- External integration pattern: none; generation is local and deterministic.
- Persistence/data access pattern: filesystem plan, apply, then
  `.ai-bootstrap/state.json`.

## 4. Proposed Changes

### 4.1 Collapse workflow selection to recommended

- Replace mode-based workflow resolution with one function that always returns
  `spec-driven` and `living-docs`, plus their skills when skills are enabled.
- Remove CLI `--no-living-docs` and `--living-docs-only` options, examples and
  branching. Argparse will reject those legacy options normally.
- Remove the TUI workflow selector, translated mode labels, mode readback and
  mode parameter plumbing. Do not leave a selector containing one option.
- Keep `--no-skill` and the TUI skill checkbox independent; they control skill
  files, not whether either workflow is active.
- Update README, CLI/TUI help and state tests so both workflows are always
  recorded and described.

### 4.2 Extend the declarative template-pack model

- Add manifest-declared `project_owned_paths`. These paths are protected but not
  generated: absence causes no write, while an existing path is reported and
  preserved.
- Add an optional declarative `overwrite_hint` for bootstrap-owned files whose
  replacement needs migration guidance. Use it on managed `AGENTS.md` to tell
  users to move local rules before forced synchronization.
- Add optional `when_stacks` to file, directory, context-fragment and
  composition specifications. An absent condition means current behavior; a
  present condition matches when every declared stack is present in the repo
  profile.
- Add context fragments with a manifest-declared placeholder name and template.
  The planner renders matching fragments and supplies an empty value for known
  nonmatching fragments. This lets `AGENTS.md` contain one placeholder without
  hardcoding Rust policy in Python.
- Add composition specifications with two focused modes:
  - `make-targets`: maintain a marked block of targets and detect unmanaged
    target-name collisions;
  - `ensure-lines`: append missing normalized lines without replacing existing
    file content.
- Validate all output paths as relative paths contained by the target repo.
- Reject overlap between a project-owned path and generated files,
  compositions or obsolete declarations.
- Increment the default pack version because generated behavior changes.

### 4.3 Introduce a cohesive composer boundary

- Add `core/composer.py` to own pure text composition and return a typed result
  containing content, status/message inputs and any conflict description.
- For `make-targets`, strip and replace only the matching bootstrap marker
  block. Parse the proposed target names and unmanaged current target names.
- Retain an unmanaged target only when its normalized header and recipe are
  equivalent to the proposed contract; omit that target from the managed block
  to avoid duplicate recipes.
- Return a conflict for a non-equivalent unmanaged target. Do not modify any
  target in that case.
- For `ensure-lines`, preserve current ordering/content and append only lines
  that are not already semantically represented. The Cargo ignore rule treats
  `target/` and `/target/` as already satisfied.
- Keep filesystem reads, path resolution, preview ordering and `WriteResult`
  creation in the planner; keep filesystem writes in the applier.

### 4.4 Make conflicts previewable and apply-blocking

- Represent a composition collision as `status="conflict"`, `kind="file"`,
  with no writable content.
- Dry-run and TUI preview show conflicts with their target names.
- Before any real write, `apply_plan` checks the entire plan and raises a clear
  error if a conflict exists. This prevents partial application.
- CLI catches the conflict, prints it and exits non-zero without writing state;
  TUI uses its existing exception/status surface.
- `--force` remains limited to generated full-file replacement and known
  obsolete-file deletion; it does not override unmanaged Make recipes.
- State records composed file provenance/status only after a conflict-free
  application.

Make conflict behavior is deliberately conservative:

- if a required target is absent, add it to the managed block;
- if an unmanaged target has the same normalized recipe, keep it where it is
  and do not duplicate it in the managed block;
- if an unmanaged target has a different recipe, report its name as a conflict
  and block all writes;
- if a previous bootstrap-managed block exists, update that block in place;
- `--force` never changes these rules because it authorizes replacement of
  bootstrap-owned files, not arbitrary project-owned Make recipes.

Each blocking result and final CLI/TUI error will include:

- the conflicting file and target;
- the normalized current recipe and required recipe;
- confirmation that application stopped before writing any file;
- explicit choices: edit the existing target to the required recipe, remove or
  rename it so the bootstrap can manage the name, or make it equivalent and
  rerun the bootstrap;
- an explicit warning that `--force` does not bypass repository-owned Make
  conflicts.

### 4.5 Add project-owned agent instructions

- Declare `AGENTS.project.md` as a protected project-owned path without a seed
  template. If absent, produce no file or state result. If present, return
  `status="preserved"` without reading it for template comparison or replacing
  it, even under `--force`.
- Add one concise section to managed `AGENTS.md`: read the project complement
  when present; create it only for the first concrete repository-specific rule;
  store later local working adjustments there, not in managed `AGENTS.md`; link
  detailed facts to their living-document owners; never store sensitive data.
- Carry ownership through `WriteResult`, preview and state. State uses
  `ownership="project"` for an existing protected path and stores no template
  provenance/hash. An absent path produces no state entry.
- Teach applier that `preserved` is non-writable, like `unchanged`, while making
  the ownership reason explicit to users.
- Add the manifest-declared overwrite hint to a differing managed `AGENTS.md`
  result, especially in forced previews, so existing projects move custom rules
  before applying. Do not attempt heuristic prose extraction.

### 4.6 Add the Rust-only generated policy

- Add a Rust Make-block template containing `.PHONY` plus:
  - `dev: cargo run`;
  - `run: cargo run --release`;
  - `clean-dev: cargo clean --profile dev`;
  - `test: cargo test`;
  - `lint: cargo clippy --all-targets --all-features -- -D warnings`;
  - `typecheck: cargo check --all-targets --all-features`.
- Add a conditional `.gitignore` ensured-line template for `target/`.
- Add `docs/architecture/rust-development.md` as the single owner of the
  command lifecycle, selective cleanup rationale, user-data boundary, custom
  target-directory note and optional release stripping guidance.
- Add a Rust-only context fragment for `AGENTS.md` with one short rule and a
  link to that document.
- For Rust profiles, make detected command presentation use the Make interface
  that the bootstrap establishes. Preserve current scanner behavior for all
  other profiles.
- Bind the Rust document, fragment and operational compositions to the always
  enabled workflow groups. Every Rust bootstrap receives the complete policy as
  one unit.

### 4.7 Update source documentation and current knowledge

- Update `README.md` to explain conditional stack modules, Rust output and safe
  conflict behavior without copying the full generated Rust rationale.
- At closeout, update `docs/product/README.md` with the verified conditional
  behavior and `docs/architecture/README.md` with manifest/composer ownership.
- Change the capability row from `partial` to `verified` only after all relevant
  validation succeeds; update all three affected capability rows and clear their
  approved targets/active changes at closeout.
- Run the living-doc link checker after adding the new generated link and source
  knowledge links.

## 5. Module Boundaries

- `scanner`: repository evidence and suggested command interface; no template
  content or composition.
- `workflow`: one recommended group set; no product mode branching.
- `template_pack`: declarative schema parsing; no repository mutation.
- `composer`: pure Make/line text composition and conflict detection; no I/O.
- `planner`: selection, safe paths, rendering, current-file reads and visible
  plan results.
- `applier`: preflight conflict guard and execution of approved plan results.
- default templates/manifest: all Rust policy wording, commands and conditions.
- default managed `AGENTS` template: router to an on-demand project-owned
  complement, with no duplicated detailed project knowledge.
- CLI/TUI: presentation and error propagation only.

The CLI, TUI and state modules must not learn Rust-specific rules. Non-Rust
stacks must not require branches outside generic manifest condition matching.

## 6. Architecture Locality

- Primary module or owner: template pack plus the planner/composer boundary.
- Files expected to change:
  - `core/template_pack.py`, `core/planner.py`, `core/applier.py`,
    `core/scanner.py`, new `core/composer.py`;
  - `cli.py` and small TUI status text only for generic conflict reporting;
  - default manifest and new/existing templates;
  - focused scanner/planner/applier/template-pack/CLI/TUI/state tests;
  - README and living-doc owners.
- Files that should not be touched: spec-driven artifact templates and generated
  operational skills; their approval semantics are unrelated.
- New boundaries introduced: one pure composer module.
- Existing boundaries preserved: manifest describes, planner previews, applier
  mutates, interfaces present.
- Why this is the smallest maintainable change: repository-owned file merging
  cannot safely be modeled as current full-file replacement, while a pure
  composer avoids spreading special cases through planner and applier.
- Are the affected files all part of the same conceptual area? Yes: conditional
  generated-output planning and presentation.
- Does this change require edits across unrelated areas? No; docs/tests mirror
  the same public contract.
- Should we refactor before, during, or after this change? Perform only the
  planned local extraction of composition logic during implementation.

## 7. Data / API / Interface Impact

- The internal manifest schema gains `when_stacks`, `context_fragments`,
  `compositions`, `project_owned_paths` and optional file `overwrite_hint`;
  existing manifests remain valid.
- CLI removes `--no-living-docs` and `--living-docs-only`; TUI removes its mode
  selector and mode argument plumbing.
- `TemplatePack` gains corresponding typed lists/fields.
- `WriteResult.status` gains `conflict`; no serialized state is written for a
  failed application.
- `WriteResult`/state gain explicit ownership, and status gains `preserved` for
  existing project-owned files.
- Dry-run, CLI summaries and TUI tables can show composed-file results using
  the existing public plan shape.
- Every generated Rust repository gains/modifies `Makefile` and `.gitignore`
  safely and gains `docs/architecture/rust-development.md`.
- No repository receives an empty `AGENTS.project.md`; once the project creates
  it for a real rule, normal, forced and upgraded runs preserve it byte for byte.
- Non-Rust generated output remains unchanged except for pack version metadata.

## 8. Security / Privacy Impact

- This touches local repository files but no credentials, network calls, user
  data or external APIs.
- Manifest composition paths receive repository-boundary validation.
- No arbitrary command is executed during bootstrap.
- The generated cleanup command delegates only dev-profile artifact removal to
  Cargo and names no user-data path.
- Conflict preflight prevents partially writing docs before discovering a
  repository-owned Make collision.

## 9. Dependency Impact

- No dependency is added. Make parsing/composition uses the Python standard
  library and the repository's existing simple target conventions.
- Avoiding a general Make parser is acceptable because the composer needs only
  top-level target headers and tab-indented recipe equivalence; unsupported or
  ambiguous constructs resolve conservatively as conflicts.

## 10. Risks

- Make syntax can be complex: restrict parsing to explicit simple targets and
  fail conservatively on ambiguity instead of rewriting.
- A managed marker could be malformed or duplicated: report conflict and do not
  write.
- A future manifest could accidentally reclaim a project-owned file: reject
  overlap with generated/composed/obsolete paths and test force plus pack-upgrade
  preservation.
- Existing custom rules may still live in managed `AGENTS.md`: show a concrete
  migration hint before overwrite but avoid unsafe automatic classification.
- The project complement could become another context dump: create it only on
  demand and keep the managed routing/brevity instruction short.
- Conditional placeholders could leak unresolved `$...` text: test both
  matching and nonmatching contexts.
- Removing partial modes could leave dead CLI/TUI text or branches: search for
  legacy flags/mode identifiers and protect the single workflow with tests.
- Docs could claim Make commands after a conflict: real apply is atomic at the
  plan level, and dry-run labels the unresolved conflict.
- A technically correct conflict could still strand a user: assert actionable
  reason/remediation fields in planner, CLI and TUI behavior tests.
- `cargo clean --profile dev` behavior could drift: contract uses documented
  stable Cargo interface and tests the generated recipe plus release
  preservation in a local fixture.
- Context could grow: retain the current `AGENTS.md` word-budget test and keep
  detailed Rust rationale in one conditional page.

## 11. Validation Strategy

### 11.1 Test Strategy

- Contract to protect: Rust repositories receive the complete safe lifecycle;
  non-Rust repositories receive none of it; repository-owned text is preserved;
  project-owned agent instructions survive every sync; conflicts block all
  writes; release artifacts survive dev cleanup.
- Tests to add or update:
  - scanner tests for Rust Make command presentation and non-Rust stability;
  - template-pack parsing tests for absent/matching/nonmatching stack conditions;
  - ownership tests for absence/no-write, project creation, arbitrary edits,
    normal/forced/upgrade preservation, all overlap rejection and state semantics;
  - pure composer tests for new, idempotent, upgraded, equivalent, conflicting,
    malformed-marker and ensured-line cases;
  - planner tests for conditional files/fragments/compositions and safe paths;
  - applier/CLI/TUI tests proving conflicts block mutation/state and remain
    visible in previews with current/required recipes and remediation;
  - generated-pack tests for the unified workflow, Rust/non-Rust surface,
    command contents, links and word budget;
  - CLI/TUI/workflow tests proving partial modes are absent and both workflows
    are always enabled;
  - preview tests proving managed `AGENTS.md` overwrite includes actionable
    migration guidance while `AGENTS.project.md` is reported as preserved;
  - a controlled Make cleanup test with fake `cargo` on `PATH` that validates
    the exact call and leaves a `target/release` probe intact, avoiding network
    and toolchain dependence.
- Tests intentionally not added: exact full-document snapshots, Cargo
  compilation of a synthetic dependency graph, or tests of Cargo internals.
- Why these tests should survive internal refactors: they assert generated
  repository behavior, preservation and user-visible plan contracts.

Final commands:

1. `python3 -m unittest discover -s tests -v`
2. `python3 -m compileall -q ai_workflow_bootstrap`
3. `python3 -m json.tool ai_workflow_bootstrap/template_packs/default/manifest.json`
4. Apply the pack to temporary Rust and Python repositories and run the
   generated link checker.
5. Exercise the generated Make targets with a fake Cargo executable where
   needed for deterministic cleanup validation.
6. `git diff --check`

## 12. Living Documentation Impact

- Product fact owner(s) to update: `docs/product/README.md`.
- Architecture fact owner(s) to update: `docs/architecture/README.md`.
- Current state/evidence changes: `partial` becomes `verified` only after the
  full validation set passes.
- Approved target/active-change changes: registered now; remove after closeout
  while retaining durable current evidence.
- Roadmap/decision changes: none expected; the spec records the temporal design
  and no separate durable decision is needed unless implementation deviates.
- Links/evidence to validate: capability-to-source/change links and all newly
  generated architecture-document links.

## 13. Execution Steps

1. Add failing tests for the unified workflow and remove partial-mode test
   expectations.
2. Add failing behavior-level tests for manifest ownership/conditions,
   composition, conflict preflight and Rust/non-Rust generated surfaces.
3. Remove CLI/TUI mode selection and simplify core workflow resolution.
4. Implement template-pack protected-path ownership, overwrite-hint,
   condition/context/composition specs and parsing.
5. Add project-owned planning/state semantics and managed AGENTS routing.
6. Add the pure composer and integrate it into planner result construction.
7. Add conflict preflight/error handling across applier, CLI and TUI text.
8. Add Rust templates/manifest declarations and align scanner command output.
9. Add release-preservation/cleanup fixture and unified-workflow/idempotency
   tests.
10. Update README and living knowledge owners, then increment pack version.
11. Run the full validation set and inspect the diff for unrelated behavior,
   unsafe writes, duplicated policy and context-budget regressions.
12. Close tasks and capability state only with supporting evidence.

## 14. Rollback / Recovery

- Before apply, dry-run shows all full-file and composed changes.
- A composition conflict blocks every real write, so no rollback is needed.
- Managed Make content can be removed by deleting only its marked block;
  `.gitignore` can be restored through Git if desired.
- Existing text outside managed boundaries is never intentionally replaced.
- `AGENTS.project.md` is not rolled back by the bootstrap because its content is
  project-owned; Git remains the project's recovery mechanism.
- Source changes are recovered through Git; the implementation will not stage,
  commit or create backup files.

## 15. Notes

The plan deliberately does not modify `Cargo.toml`. Release stripping remains
an explicit project decision because removing symbols can reduce diagnostic
value. The generated Rust document will show the supported option without
claiming it is universally appropriate.
