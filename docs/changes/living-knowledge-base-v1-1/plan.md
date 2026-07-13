# Implementation Plan: Living Knowledge Base v1.1

## 1. Summary

Refine the default pack and the small planning/applier surface around it so
generated project memory is cheaper to load, unambiguous about current versus
future behavior, explicitly baselined, and destructively replaceable only after
the user chooses overwrite. The change removes the backup feature rather than
adding another migration or backup mode.

## 2. Relevant Existing Context

- `template_packs/default/manifest.json` declares generated files and groups;
  it is the natural owner of the fixed obsolete-file allowlist.
- `core.template_pack` parses manifest structure, while `core.planner` creates
  write results and `core.applier` executes them.
- `WriteResult` already carries `kind`, `status` and message fields used by CLI,
  TUI and state generation; it can represent a visible deletion result without
  a separate preview channel.
- `core.applier` currently imports `core.backup` and conditionally writes
  timestamped backup files. CLI exposes `--no-backup`; TUI always requests
  backups and labels overwrite accordingly.
- Existing state serializes only file results, so deletion results can use a
  non-file kind and remain out of the resulting generated-file inventory.
- The current default pack has duplicated workflow rules across `AGENTS.md`,
  `SPEC_DRIVEN.md`, skills and embedded copies of change templates.
- The current living-doc output includes `AI_CONTEXT.md`, a one-column
  capability status and no explicit baseline coverage state.
- Standard-library `unittest` contract tests already cover planning, applying,
  CLI, TUI and template pack selection.

## 3. Existing Conventions Found

- Generated destinations mirror template paths and are assigned to manifest
  groups.
- The planner uses `written`, `unchanged`, `skipped` and `overwritten` status
  values; dry-run and real application share one plan.
- The applier writes plan results in order, and state is written only after a
  successful application.
- Tests use temporary directories and inspect public plan/application results.
- Template content is English, Markdown links are relative and template pack
  version changes represent generated-output contract changes.
- Recursive template package data is already included by `pyproject.toml`.

## 4. Proposed Changes

### 4.1 Make pack migrations explicit and destructive only with overwrite

- Extend the template-pack manifest/parser with a fixed obsolete-file entry
  type containing a relative path and workflow group. This is pack-declared
  allowlisting, not user-configurable deletion support.
- Register the five superseded living-doc paths in the default manifest:
  `WORKFLOW_MODULES.md`, `PROJECT_SPEC.md`, `IMPLEMENTATION_STATUS.md`,
  `CANONICAL_DECISIONS.md` and `AI_CONTEXT.md`.
- In the planner, append deletion results only when `force=True`, the matching
  living-doc group is enabled and the legacy path exists as a regular file or
  symlink. Use a dedicated non-file result kind so state excludes it.
- Refuse directories and other non-regular legacy targets with an explicit
  skipped/blocked plan result; never recurse.
- Keep writes before deletions so a failed write prevents later cleanup. Do not
  delete paths when living docs are disabled or overwrite is not selected.
- In the applier, execute planned deletion results with `unlink`; dry-run only
  reports them.

### 4.2 Remove backups completely

- Remove `backup_existing` and `needs_backup` from planner/applier data flow.
- Change forced overwrite plan messages to state direct replacement, not
  backup creation.
- Remove `--no-backup`, backup imports, `core/backup.py`, backup tests and
  backup-specific assertions.
- Update CLI help, TUI label/text, README and result messages to say overwrite
  is destructive and Git is the recovery mechanism.
- Preserve the existing force opt-in and TUI `APPLY` confirmation. Do not add
  Git checks, commits or a third confirmation dialog.

### 4.3 Compact the generated workflow

- Rewrite `AGENTS.md` as a compact mandatory policy/router: approval gates,
  security rules, current-vs-target rule, ownership rule and pointers to
  relevant skills/docs.
- Rewrite `SPEC_DRIVEN.md` as on-demand guidance without embedded copies of
  spec/plan/task/decision templates; link to the standalone templates instead.
- Keep the standalone change templates as the only artifact definitions and
  update their living-document fields to use the new current/target model.
- Update `START_PROMPT.md`, generated spec-driven skill and generated
  living-docs skill so the full manual is not mandatory context for each task.
- Enforce word limits in focused tests: AGENTS <= 800, SPEC_DRIVEN <= 1000,
  INDEX <= 250 and each operational skill <= 300 words.

### 4.4 Refine living knowledge structure

- Remove `AI_CONTEXT.md` from fresh generation and all generated references.
- Make `INDEX.md` the sole entry point, with initial coverage `scaffold`, a
  baseline-evidence placeholder and concise rules for moving to `incomplete`
  or `baselined`.
- Rework `CAPABILITIES.md` to use columns for current state, evidence, approved
  target and active change. Current state is one of `unknown`, `absent`,
  `partial`, `implemented`, `verified` or `deprecated`.
- Move ideas and rejected/superseded disposition out of the active map; update
  roadmap and decision guidance to keep active context bounded.
- Update product, architecture and living-document policy templates to explain
  baseline evidence, current/target ownership and conflict handling.

### 4.5 Add deterministic link validation

- Add `scripts/check_links.py` beneath the generated living-docs skill and
  declare it in the skill group of the manifest.
- Implement with the standard library: scan living docs, ignore fenced code
  blocks, external URLs and anchor-only links, and report broken local relative
  Markdown links with non-zero exit status.
- Update the generated skill to invoke the script after structural changes.
- Add direct script tests plus the existing freshly-applied-doc link test.

### 4.6 Align source documentation and tests

- Increment the default template-pack version.
- Update README and relevant source workflow guidance to remove backup promises,
  describe destructive overwrite, explain the baseline model and show INDEX as
  the entry point.
- Update planner, applier, CLI, TUI, state and template tests for deletion
  visibility, force/no-force behavior, no-backup behavior removal, workflow
  modes, output contracts, word budgets, link checker and capability semantics.

## 5. Module Boundaries

- Manifest/parser: fixed generated and obsolete-path declarations.
- Planner: safe resolution and visible creation/overwrite/deletion plan results.
- Applier: execution of already-planned writes and deletions only.
- CLI/TUI: explicit user consent, accurate language and results presentation.
- Default templates/skills: project knowledge and agent procedure.
- Link-checker script: deterministic documentation-path validation.
- Tests: public contract coverage; no full-prose snapshots.

The deletion path necessarily crosses manifest, planner and applier, but it
remains one cohesive operation. Documentation semantics remain in the pack;
the engine only understands pack-declared file operations.

## 6. Data / API / Interface Impact

- Manifest gains an internal obsolete-file declaration section.
- `BootstrapPlan` and `WriteResult` lose backup-only fields and gain/use a
  deletion result kind.
- CLI removes `--no-backup`; callers using it will receive argparse's normal
  unsupported-option error.
- `--force` becomes an explicitly destructive replacement/legacy-cleanup
  consent while remaining opt-in.
- TUI overwrite wording changes but its mode, checkbox and APPLY confirmation
  remain.
- State JSON format remains the same and excludes deletion results.
- Fresh living-doc output no longer includes `docs/AI_CONTEXT.md` and includes
  the generated link-checker script.

## 7. Security / Privacy Impact

- Deletion is limited to manifest-declared relative paths under the target
  directory and only after explicit overwrite consent.
- Directory deletion is refused; no recursive removal API is introduced.
- Link validation performs only local reads and does not fetch URLs.
- Existing living-doc sensitive-data restrictions remain.
- Removing backups deliberately shifts recovery responsibility to the user’s
  Git history as approved in the spec.

## 8. Dependency Impact

- No dependencies are added. The checker uses Python's standard library.
- Removing the backup module reduces internal surface area.

## 9. Risks and Mitigations

- Destructive overwrite can remove user-modified legacy files: force/TUI
  confirmation is explicit, preview lists each deletion and the allowlist is
  narrow.
- Partial application can leave writes completed before a deletion fails: write
  first, surface errors and do not save state as successful on failure.
- Compact instructions could omit a mandatory approval rule: protect both gates
  with exact contract tests.
- A naive regex checker can read links in examples: skip fenced blocks and test
  that behavior.
- Word budgets can become brittle: use intentionally loose limits tied to the
  approved context objective, not exact wording.

## 10. Validation Strategy

- Unit-test planner/applier force/no-force replacement and allowlisted deletion
  behavior, including directory refusal and spec-driven-only preservation.
- Test no backup files are created and no backup interfaces remain.
- Test CLI parser/help rejects `--no-backup` and accurately describes `--force`.
- Test TUI planning/labels reflect destructive overwrite.
- Test fresh/recommended/living-only output excludes AI_CONTEXT and includes the
  link checker; spec-driven-only excludes both living docs and cleanup.
- Test capability template content can represent verified current plus planned
  target, scaffold/baseline guidance and active-map bounds.
- Test the checker against valid generated output, a broken local link and
  fenced/external/anchor links.
- Run the full suite, `compileall`, manifest JSON validation, generated checker
  against a temporary application and `git diff --check`.

## 11. Execution Steps

1. Add obsolete-file manifest support and update planner/applier result flow.
2. Remove backup logic and update CLI/TUI contract.
3. Revise the manifest, templates and generated skills for compact context,
   baseline state and current/target capability mapping.
4. Add the link-checker script and manifest entry.
5. Update source docs and focused tests.
6. Validate all modes, destructive-preview behavior and context budgets.

## 12. Rollback / Recovery

- Before a user selects overwrite, no target file is changed.
- After explicit overwrite, recovery is through the user’s Git history; this
  tool intentionally creates no backup files.
- Source template recovery is also through Git.
- If validation reveals unsafe deletion behavior, revert the implementation
  change as a whole rather than adding a hidden fallback backup path.

## 13. Notes

The repository-local `.agents` directory is read-only in this workspace. The
implementation will update generated skill templates, which are the downstream
product contract, but will not attempt to mutate that protected local copy.
