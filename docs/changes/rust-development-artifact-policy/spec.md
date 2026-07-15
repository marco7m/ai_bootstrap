# Change Spec: Unified bootstrap workflow and conditional project policies

## 1. Summary

Extend the bootstrap so repositories detected as Rust receive a compact,
enforced development/release artifact policy. Non-Rust repositories must not
receive Rust commands, Rust-specific files or Rust-specific instructions.

The bootstrap will also have only one supported workflow: the current
recommended combination of spec-driven development and living documentation.
The CLI and TUI will no longer offer partial workflow modes.

Generated repositories will also separate bootstrap-owned agent policy from
project-owned instructions. `AGENTS.md` remains managed by the bootstrap, while
`AGENTS.project.md` is created by the project only when a durable local rule is
actually needed and thereafter preserved by every bootstrap synchronization.

The policy will be expressed primarily as conditional template-pack data, with
generic planner support for stack conditions and safe composition into existing
repository files. This keeps Rust knowledge out of the Python engine and avoids
repeating the full rationale in always-read context.

## 2. Problem

The bootstrap detects Rust and suggests direct Cargo commands, but it does not
establish the desired lifecycle:

- fast debug/incremental builds during implementation;
- selective cleanup only after final validation;
- a preserved release artifact for daily use;
- Git exclusion of Cargo artifacts;
- consistent Make targets and development documentation.

Adding the complete policy to every generated `AGENTS.md` would waste context
for non-Rust projects and repeat details that are rarely needed. Treating
`Makefile`, `.gitignore` or `Cargo.toml` as ordinary overwriteable templates
would also risk destroying repository-owned content.

The same ownership problem currently affects project-specific agent guidance.
Projects naturally add local working rules to `AGENTS.md`, but a later forced
bootstrap synchronization replaces that managed file and can erase those rules.
There is no explicit durable complement whose ownership belongs to the project.

## 3. Goal

For a Rust repository, make the bootstrap establish and document one reliable
workflow:

1. use debug/incremental caches throughout implementation and validation;
2. run cleanup only after the final successful validation;
3. remove development/test artifacts without deleting the release profile;
4. keep the optimized application runnable through Cargo freshness checks;
5. keep generated Rust detail out of non-Rust repositories and out of
   always-read context unless it is relevant.
6. keep bootstrap policy replaceable without deleting project-owned agent
   instructions.

## 4. Scope

- Add declarative stack conditions to applicable template-pack entries.
- Remove spec-driven-only and living-docs-only selection from CLI, TUI and core
  workflow resolution; every application enables both workflows.
- Add a generic protected project-owned path policy to the template pack.
- Leave `AGENTS.project.md` absent until a project needs its first local rule,
  then preserve it on every later bootstrap run.
- Make generated `AGENTS.md` route project-specific working rules to
  `AGENTS.project.md` and require reading that complement when present.
- Add generic, safe file-composition support for:
  - a marked, bootstrap-owned block in `Makefile`;
  - an ensured `target/` entry in `.gitignore`.
- Generate a focused Rust development document only when `rust` is detected.
- Add a short Rust-only instruction to generated `AGENTS.md` that links to the
  focused document and fixes cleanup ordering.
- Make generated command listings prefer the established Make targets for Rust.
- Record template provenance and preview statuses for composed changes.
- Test Rust and non-Rust generation, repeat application, conflict behavior and
  selective-clean semantics.
- Update bootstrap product/architecture/capability documentation at closeout.

## 5. Out of Scope

- Applying Rust policy to repositories without a detected `Cargo.toml`.
- Running builds, tests or cleanup in the target repository during bootstrap.
- Deleting user data, databases, recordings, reports or any path outside Cargo's
  generated target directory.
- Automatically adding `strip = "symbols"` to `Cargo.toml`.
- Replacing arbitrary user-owned Make recipes when they conflict with required
  target names.
- General-purpose structural editing of TOML, YAML or programming-language
  source files.
- Removing the independent `--no-skill` choice; skills may remain optional while
  the two workflows themselves are always enabled.
- Automatically extracting or classifying custom prose already mixed into an
  existing `AGENTS.md`; existing projects must move such rules deliberately
  before authorizing destructive overwrite.
- Storing machine-local preferences, secrets or untracked personal data in the
  project-owned instructions file.

## 6. Users / Actors

- Maintainers bootstrapping an existing or new Rust repository.
- AI assistants following the generated repository instructions.
- Developers using Make targets during development and daily execution.

## 7. Functional Requirements

1. Rust detection continues to use repository evidence (`Cargo.toml`), not a
   manual prose declaration.
2. For a detected Rust repository, the resulting Make interface includes:
   - `make dev` -> `cargo run` (debug profile, incremental by Cargo default);
   - `make run` -> `cargo run --release`;
   - `make clean-dev` -> `cargo clean --profile dev`;
   - `make test` -> `cargo test`;
   - `make lint` -> the repository's detected compatible lint command, with the
     current Cargo/Clippy default as fallback;
   - `make typecheck` -> the repository's detected compatible check command,
     with `cargo check --all-targets --all-features` as fallback.
3. The generated Make recipes are held in one clearly marked managed block.
   Reapplying the same pack updates that block idempotently and preserves all
   content outside it.
4. If an unmanaged Make target collides with a required managed target:
   - an equivalent target may be retained;
   - a non-equivalent target is reported as a conflict and is not silently
     replaced, including under the existing broad `--force` behavior;
   - the conflict identifies the `Makefile`, target name, current recipe,
     required recipe and concrete remediation choices;
   - remediation tells the user to update/remove/rename the conflicting target
     or intentionally make it equivalent, then run the bootstrap again;
   - the message explicitly says that `--force` will not resolve the conflict.
5. Rust repositories have `target/` ensured in `.gitignore` without replacing
   or duplicating existing ignore rules.
6. `make clean-dev` must use Cargo's profile-aware cleanup. It must not invoke
   bare `cargo clean`, remove `target/release`, or address user-data paths.
7. The Rust development document explains the command contract, the lifecycle,
   and the reason cleanup is delayed until after final validation.
8. The Rust document presents `[profile.release] strip = "symbols"` only as an
   opt-in for binary applications whose symbols are not needed for diagnosis.
   The bootstrap does not infer that diagnostic tradeoff.
9. The Rust-only `AGENTS.md` instruction says to retain development/test caches
   during implementation cycles and run `make clean-dev` only after final
   validation. Detailed rationale remains in the focused document.
10. A non-Rust profile produces no Rust development document, Make fragment,
    `.gitignore` mutation, Rust command substitution or Rust-specific
    `AGENTS.md` text.
11. Dry-run/TUI preview shows each planned composed write or conflict before
    application.
12. The only supported workflow is `spec-driven` plus `living-docs`.
13. CLI options that selected a partial workflow are removed and rejected as
    unsupported. The TUI has no workflow-mode selector.
14. State and previews always report both workflows for successful applications.
15. `AGENTS.project.md` is declared a protected project-owned path:
    - the bootstrap does not create it when absent;
    - the project or assistant creates it only when the first durable
      repository-specific instruction is actually needed;
    - once it exists, its bytes are preserved under normal apply, `--force` and
      template-pack upgrades;
    - it is never part of obsolete-file deletion;
    - preview distinguishes this intentional preservation from an unchanged
      bootstrap-managed file.
16. Generated `AGENTS.md` instructs assistants to:
    - read `AGENTS.project.md` when it exists;
    - create it only when a concrete repository-specific instruction needs a
      durable owner;
    - put repository-specific workflow adjustments and durable agent reminders
      in that file rather than editing managed `AGENTS.md`;
    - keep the complement concise and link to durable knowledge owners for
      detailed product or architecture facts.
17. `AGENTS.project.md` is intended to be committed with the repository. Managed
    `AGENTS.md` applies the existing prohibition on secrets, private messages
    and sensitive production/customer data to that complement.
18. A forced preview that would replace a differing legacy `AGENTS.md` reminds
    the user to move project-specific rules to `AGENTS.project.md` before apply.

## 8. Non-Functional Requirements

### Modularity / Architecture

- Stack matching and composition modes are generic template-pack mechanisms.
- Rust policy text and recipes live in Rust-specific templates, not hardcoded
  branches throughout scanner, planner, CLI or TUI.
- Full-file rendering remains the existing path for current generated files;
  composition is a separate explicit manifest contract.

### Security / Privacy

- Composed paths must obey the same target-repository boundary as existing
  generated paths.
- Composition must not follow a path outside the target through absolute or
  parent-relative manifest paths.
- Cleanup recipes must only delegate deletion to Cargo's profile-aware cleanup.

### Reliability

- Generation and reapplication are idempotent.
- Existing user content outside a managed block is byte-preserved except for
  the normalized final newline needed to append content.
- Conflicts fail visibly rather than producing duplicate Make recipes.
- A blocking message explains why application stopped, confirms that no files
  were written and tells the user exactly what to change before retrying.
- Release preservation is covered by command-contract tests and an integration
  fixture where practical without requiring a network download.

### Performance

- Stack filtering and composition add negligible work relative to repository
  scanning.
- The generated workflow keeps Cargo incremental caches during active work and
  avoids rebuilding release artifacts after cleanup when source is unchanged.

### Observability

- Preview and state distinguish full-file writes, managed-block updates,
  ensured-line updates, unchanged results and conflicts.

### Simplicity

- Keep `AGENTS.md` to one short Rust-only rule plus a link.
- Keep the rationale in one focused development document.
- Prefer Cargo's stable `--profile dev` behavior over custom filesystem deletion
  scripts.
- Remove mode-selection code and UI text instead of retaining a one-option
  selector.
- Express protected project-path ownership once in the manifest/planner contract;
  do not special-case the `AGENTS.project.md` path across interfaces.
- Add only a short routing rule to always-read `AGENTS.md`; detailed project
  rules consume context only because the project intentionally recorded them.

## 9. Maintainability Impact

- Does this change make future changes easier or harder? Easier: future
  stack-specific modules can use the same condition/composition contracts.
- Touched architecture: scanner profile evidence, template-pack manifest model,
  planner/composer, state/preview representation and default templates.
- Potential entropy: parallel ad hoc stack checks and unsafe whole-file
  templates for repository-owned files.
- Refactor needed before coding: no broad refactor. Introduce one local
  composition boundary rather than expanding `_plan_file` with several format
  branches.
- Refactor scope: planned local refactor within template-pack parsing and plan
  construction.

Maintainability-audit classification:

- safe local cleanup: centralize manifest path validation so composed and
  obsolete paths share one repository-boundary rule;
- planned local refactor: introduce a small composer abstraction and behavior-
  level tests;
- separate refactor spec: none currently justified.

## 10. Living Documentation Impact

- Product fact owner(s): `docs/product/README.md` for conditional bootstrap
  behavior.
- Architecture fact owner(s): `docs/architecture/README.md` for manifest
  conditions/composition and current generation flow.
- Current capability state/evidence affected: add capability rows for
  stack-specific development conventions, unified workflow selection and
  project-owned agent instructions; preserve current evidence until
  implementation validates the targets.
- Approved target and active change: this spec after approval.
- Roadmap or durable decisions affected: no roadmap change required unless the
  implementation reveals a broader stack-module sequence.
- Documents intentionally unchanged: generic spec-driven workflow and skill
  contracts; Rust build lifecycle is not part of spec approval semantics.

## 11. User Flow / System Flow

1. The bootstrap scans the target repository.
2. The profile records `rust` when `Cargo.toml` exists.
3. The planner always enables spec-driven plus living-doc groups, then selects
   additional entries whose stack condition matches `rust`.
4. Full generated docs render normally.
5. The planner does nothing when `AGENTS.project.md` is absent and reports it as
   preserved when the project already owns it.
6. The composer previews an ensured `.gitignore` line and a managed Make block,
   preserving repository-owned content.
7. A collision becomes a visible conflict; otherwise apply writes the composed
   result.
8. During work, the assistant reads both agent files and stores new local rules
   only in `AGENTS.project.md`.
9. During Rust work, the assistant uses `make dev`, `make test`, lint and typecheck
   without cleaning between cycles.
10. After the last successful validation, it runs `make clean-dev`.
11. Daily execution uses `make run`; Cargo checks freshness and reuses the
   release build when unchanged.

## 12. Edge Cases

- Rust plus another detected stack: Rust policy still applies because Rust is
  present, while unrelated stack behavior is preserved.
- Existing Makefile with no collisions: append/update one managed block.
- Existing equivalent targets outside the block: retain them and avoid duplicate
  recipes.
- Existing conflicting targets: surface the current and required recipes plus
  remediation without partial Make changes.
- Existing `.gitignore` containing `/target/`, `target/` or a semantically
  equivalent Cargo ignore: do not duplicate it.
- Workspace root with a virtual Cargo manifest: apply the same root-level policy.
- Custom Cargo target directory: the Make cleanup remains Cargo-aware; the
  generated docs note that `.gitignore` may need an additional project-specific
  rule for a non-default directory.
- A project needs runtime arguments or a specific workspace binary: keep the
  command contract explicit and allow repository-owned Make customization to be
  resolved rather than guessed.
- Applying a newer template-pack version replaces only its marked block.
- Existing `AGENTS.project.md`, including an empty or heavily customized file:
  preserve it byte for byte and do not treat template drift as a conflict.
- Missing `AGENTS.project.md`: do not create an empty placeholder or state entry.
- Existing project-specific clauses inside managed `AGENTS.md`: warn before
  forced replacement but do not guess which prose should be migrated.

## 13. Constraints

- Preserve existing destructive-overwrite semantics for ordinary generated
  scaffold files; do not broaden `--force` into arbitrary repository-file
  replacement.
- Use no new dependency for Make or ignore-file composition.
- Replace existing CLI/TUI workflow selection with the single recommended
  spec-driven plus living-docs workflow.
- Keep generated always-read context within its existing word budget.
- Follow stable Cargo behavior: `dev` is incremental by default, `test` inherits
  `dev`, `cargo run --release` uses the release profile, and
  `cargo clean --profile dev` removes only the dev-profile artifact directory.

## 14. Assumptions

- GNU Make or a compatible `make` is available in projects adopting this
  interface.
- `Cargo.toml` at the selected target root is sufficient evidence that Rust
  policy is applicable.
- The default Cargo target directory is `target/` unless the project documents a
  custom target directory.
- Preserving diagnostic symbols is safer by default, so release stripping is
  advisory and opt-in.

## 15. Acceptance Criteria

1. A Rust fixture preview includes the Rust document, Rust-only `AGENTS.md`
   guidance, required Make targets and the `.gitignore` rule.
2. Applying that fixture twice produces unchanged results on the second run.
3. `make dev`, `make run`, `make clean-dev`, `make test`, `make lint` and
   `make typecheck` resolve to the approved Rust command contract.
4. The clean target contains `cargo clean --profile dev` and no bare full-clean
   command or release deletion.
5. An existing release probe under `target/release` remains after executing the
   cleanup recipe in a controlled fixture, without network access.
6. Existing Makefile content outside the managed block and existing ignore
   rules remain intact.
7. A conflicting unmanaged Make target is shown as a conflict and not silently
   overwritten. Its message identifies the target and both recipes, confirms no
   files were written, gives actionable remediation and says `--force` is not a
   bypass.
8. A Python-only fixture receives no Rust content or repository-file
   composition; its workflow surface changes only as required by removal of the
   partial modes and template-pack version/state metadata.
9. Generated `AGENTS.md` remains within its word budget, and the Rust rationale
   exists in only one durable generated document.
10. Unit tests, compile checks, manifest validation, generated link checks and
    `git diff --check` pass.
11. CLI help exposes neither `--no-living-docs` nor `--living-docs-only`, and
    both old options fail as unsupported.
12. The TUI exposes no workflow-mode selector, and every CLI/TUI plan records
    both `spec-driven` and `living-docs` as enabled.
13. A fresh repository does not receive an empty `AGENTS.project.md`. After the
    project creates it for a concrete rule, normal apply and `--force` preserve
    it byte for byte.
14. Generated `AGENTS.md` routes local rules to the project-owned complement and
    a forced replacement warning explains how to preserve legacy custom rules.
15. Preview/state identify ownership and preservation when the file exists,
    without claiming it matches a pack template; absence produces no file or
    state entry.
16. Tests prove project-owned files cannot be overwritten or declared obsolete
    through the normal template-pack contract.

## 16. Open Questions

None blocking. The recommended default is to treat release stripping as a
documented opt-in, because deciding whether symbols are needed for diagnosis is
project-specific and cannot be inferred safely from the presence of a binary
target alone.
