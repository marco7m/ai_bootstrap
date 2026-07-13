# Implementation Plan: Living Knowledge Base v1

## 1. Summary

Replace the default pack's placeholder living-doc files with a compact linked
knowledge base and integrate its lifecycle into the generated agent and
spec-driven instructions. Keep the implementation inside template-pack,
documentation and contract-test boundaries; do not change the Python engine,
CLI, TUI, state schema or launcher.

## 2. Relevant Existing Context

- `ai_workflow_bootstrap/template_packs/default/manifest.json` declares every
  directory and file produced by each workflow group.
- `ai_workflow_bootstrap/template_packs/default/templates/docs/` owns the
  living-doc content received by downstream projects.
- `ai_workflow_bootstrap/template_packs/default/templates/.agents/skills/living-docs/SKILL.md`
  owns the reusable agent procedure but currently contains only seven generic
  rules.
- The generated `AGENTS.md`, `docs/SPEC_DRIVEN.md`, `docs/START_PROMPT.md`,
  spec-driven skill and change templates define how approved changes move from
  intent to implementation and validation.
- `core.template_pack` loads manifest declarations, and `core.planner` already
  renders any declared directory/file by group. Neither module interprets
  documentation semantics.
- `core.workflow.resolve_workflow_selection` already separates recommended,
  spec-driven-only and living-docs-only modes.
- `tests/test_template_pack.py` protects manifest/template existence and mode
  selection. `tests/test_planner.py` protects representative rendered output.
- `README.md` documents the generated file set and living-doc purpose.
- `docs/SPEC_DRIVEN.md` describes the bootstrap repository's intended core
  generated docs and must remain aligned with the pack.
- `.gitignore` currently ignores new `docs/changes/` paths even though older
  change artifacts are already tracked. This conflicts with the documented
  role of approved spec/plan/task files as a durable cross-agent handoff
  contract.
- The package-data wildcard already includes nested template files.
- Existing bootstrap behavior creates or overwrites declared files but does not
  delete undeclared target files, which provides the approved legacy safety.

## 3. Existing Conventions Found

- Folder structure: generated destinations mirror files below
  `template_packs/default/templates/`; the manifest assigns workflow groups.
- Naming style: uppercase foundational Markdown documents, kebab-case change
  folders and lowercase nested domain paths.
- Error handling: manifest/template errors surface through existing loader and
  planner behavior; no new runtime error path is required.
- Logging: not involved.
- Testing pattern: standard-library `unittest` with temporary target
  directories and assertions on public planning/template contracts.
- Config pattern: workflow selection is expressed through manifest groups, not
  per-document runtime configuration.
- External integration pattern: none.
- Persistence/data access pattern: `.ai-bootstrap/state.json` records planned
  outputs; its schema does not need to change.
- Template policy: generated template copies, not repository-local prose alone,
  determine what downstream projects receive.
- Skill policy: keep `SKILL.md` concise and procedural; add no scripts,
  references or assets without a demonstrated need.

## 4. Proposed Changes

### 4.1 Replace the living-doc template surface

- Add template directories for `docs/product`, `docs/architecture` and
  `docs/decisions` to the `living-docs` group.
- Add templates for `INDEX.md`, `CAPABILITIES.md`, the three foundational area
  indexes and the decision template.
- Rewrite `AI_CONTEXT.md`, `LIVING_DOCUMENTATION.md`, `ROADMAP.md`,
  `IDEA_INBOX.md` and `GLOSSARY.md` around routing, ownership and lifecycle.
- Stop declaring the superseded `WORKFLOW_MODULES.md`, `PROJECT_SPEC.md`,
  `IMPLEMENTATION_STATUS.md` and `CANONICAL_DECISIONS.md` outputs.
- Remove their unused source templates after confirming nothing else reads
  them. This does not delete files from previously bootstrapped repositories.
- Increment the default template-pack version because its generated contract
  changes, without changing the state schema.

### 4.2 Define the knowledge model in templates

- Make `INDEX.md` the primary navigation page.
- Make product and architecture indexes own `what/why` and `how`, respectively,
  with explicit current-versus-target sections.
- Make `CAPABILITIES.md` own lifecycle status and link product, architecture,
  active changes and safe evidence.
- Define single-fact ownership, relative-link rules, progressive disclosure,
  document-splitting heuristics, conflict handling and sensitive-data limits in
  `LIVING_DOCUMENTATION.md`.
- Use a decision index plus a minimal decision template rather than one large
  decision log or mandatory one-file-per-trivial-choice behavior.

### 4.3 Expand the generated living-docs skill

- Strengthen its description so it triggers for project orientation,
  product/architecture questions, documentation updates, status transitions
  and bug-contract investigation.
- Add a short ordered workflow: route from index, select owners, classify
  current/target state, update only supported lifecycle stages, link rather
  than duplicate, validate references and surface evidence conflicts.
- Keep the skill self-contained; no auxiliary resources are justified for v1.

### 4.4 Integrate with generated spec-driven workflow

- Update generated `AGENTS.md`, `docs/SPEC_DRIVEN.md`, `docs/START_PROMPT.md`
  and relevant generated skills so agents know when and how to consult living
  docs.
- Add a living-documentation impact/ownership section to generated spec and
  plan templates.
- Add concrete living-doc lifecycle items to the generated task template.
- Preserve both explicit approval gates. Planning may identify documentation
  owners, but implementation still waits for plan/tasks approval.
- Register approved target behavior as `planned`; promote status only when
  implementation and validation evidence justify it.

### 4.5 Align source documentation

- Update `README.md` with the new generated tree, responsibilities, reading
  path, lifecycle and non-destructive legacy behavior.
- Update this repository's `docs/SPEC_DRIVEN.md` where it enumerates or
  classifies generated living docs.
- Update the repository-local spec-driven skill only where needed to keep the
  bootstrap's own planning/documentation-impact rules aligned; avoid unrelated
  rewrites.

### 4.6 Make change artifacts normally versionable

- Remove only the source `.gitignore` entry for `docs/changes/`.
- Preserve all other ignore rules, including rules for generated root workflow
  files and packaged template exceptions.
- Do not stage, commit or force-add any unrelated change folder automatically.
- Verify that this change folder and future change artifacts appear through
  ordinary Git status/add behavior.

### 4.7 Protect the public contract with focused tests

- Update mode-selection assertions for the new file set and removed fresh
  outputs.
- Update rendered-output assertions to use `INDEX.md`, `CAPABILITIES.md` and the
  foundational product/architecture pages.
- Add a focused relative-link integrity test over freshly rendered core
  living-doc files. Ignore external URLs and anchors; validate only repository
  relative Markdown document links emitted by the default templates.
- Add narrow content assertions for lifecycle vocabulary, current/target
  separation, routing and evidence ownership.
- Do not snapshot complete prose or assert incidental wording.
- Confirm a pre-existing legacy file is not included in a deletion operation;
  since the planner has no deletion result type, prefer a small public-contract
  assertion over new production logic.

## 5. Module Boundaries

- `template_packs/default/manifest.json` owns generated structure and grouping.
- `template_packs/default/templates/docs/` owns foundational knowledge content.
- Generated `.agents/skills/living-docs/SKILL.md` owns the reusable agent
  maintenance procedure.
- Generated spec-driven instruction/templates own change lifecycle and approval
  integration.
- `tests/test_template_pack.py` and `tests/test_planner.py` own output-contract
  validation.
- `README.md` and source `docs/SPEC_DRIVEN.md` own public/source workflow
  explanation.
- `core.template_pack`, `core.planner`, `core.applier`, `core.workflow`, CLI,
  TUI, state and `bootstrap_sdd.py` must not learn product-documentation
  semantics or change for this feature.

## 6. Architecture Locality Check

- Primary owner: default template pack.
- Files expected to change:
  - default manifest;
  - living-doc and related workflow templates;
  - generated skill templates;
  - focused template/planner tests;
  - README and relevant source workflow guidance;
  - source `.gitignore`;
  - this change folder during implementation closeout.
- Files that should not change:
  - Python core engine modules;
  - CLI and TUI modules/text;
  - state schema and backup/applier logic;
  - `bootstrap_sdd.py`;
  - dependencies and packaging configuration unless validation reveals the
    existing recursive package-data wildcard is insufficient.
- New boundaries introduced: knowledge areas inside generated docs, not runtime
  modules.
- Existing boundaries preserved: manifest declares, templates describe,
  planner renders, applier writes.
- The multiple template edits are conceptually related mirrors of one generated
  workflow. This is expected template locality, not shotgun surgery.
- No preliminary refactor is required. If implementation requires production
  Python changes merely to express document semantics, stop and reassess the
  plan instead of expanding the engine.

## 7. Data / API / Interface Impact

- Generated filesystem interface changes for fresh living-doc applications:
  new foundational files/directories replace four legacy outputs.
- The default template-pack version will advance to represent that changed
  output contract.
- CLI flags, TUI choices, Python APIs, state JSON schema and workflow group
  names remain unchanged.
- Existing targets retain undeclared legacy files because the bootstrap has no
  delete operation.
- Markdown-relative link paths become part of the generated documentation
  contract.
- The source repository begins tracking new `docs/changes/` artifacts through
  normal Git workflows; there is no automatic staging or commit behavior.

## 8. Security / Privacy Impact

- No secrets, credentials, network calls, permissions or production data are
  introduced.
- Templates will explicitly prohibit recording secrets, private conversations,
  sensitive runtime payloads and personal/production data as project memory.
- Evidence guidance will favor safe repository paths and sanitized validation
  references rather than copied logs.
- Existing file overwrite and backup protections remain unchanged.

## 9. Dependency Impact

- No runtime, build-time or dev dependency is needed.
- Standard-library `unittest`, `pathlib` and a small test-local Markdown-link
  matcher are sufficient.
- No lockfile or deployment impact.

## 10. Risks

1. **Documentation sprawl:** too many default files would recreate context
   overhead. Mitigation: generate only foundational indexes and grow systems on
   demand.
2. **Duplicate truth:** product, architecture, capability and AI context may
   restate the same fact. Mitigation: explicit owner table and links.
3. **Planned/current confusion:** target behavior could be used as a bug
   contract. Mitigation: lifecycle states plus current/target sections.
4. **Broken links:** nested relative paths are easy to mistype. Mitigation:
   generated-link integrity test.
5. **Legacy confusion:** old files remain after applying the new pack. Mitigation:
   document non-deletion and require explicit project migration rather than
   silent destructive cleanup.
6. **Brittle prose tests:** exact wording would make future editing expensive.
   Mitigation: assert paths, lifecycle tokens and semantic contract fragments
   only.
7. **Source/template drift:** source workflow docs may disagree with generated
   templates. Mitigation: update both intentional layers and test downstream
   templates as authoritative generated output.
8. **Skill context growth:** expanding `living-docs` could consume excessive
   context. Mitigation: concise imperative workflow with details in generated
   policy docs loaded on demand.
9. **Accidental engine scope:** link validation or migration could leak into
   production code. Mitigation: keep validation test-local and migration out of
   scope.
10. **Previously hidden artifacts:** removing the ignore rule may reveal other
    local change folders. Mitigation: inspect Git status and never stage
    unrelated files automatically.

## 11. Validation Strategy

### Contract to protect

A selected living-doc workflow generates the approved linked knowledge base,
teaches agents to maintain its lifecycle, preserves other workflow modes and
does not introduce deletion or runtime behavior.

### Tests to add or update

- Manifest references every declared template and required directory.
- Recommended and living-docs-only plans include the new structure and skill.
- Spec-driven-only plans exclude the living structure.
- Fresh plans exclude superseded output paths.
- Rendered index/capability/product/architecture documents contain the required
  ownership and lifecycle contracts.
- Relative Markdown links emitted between generated core docs resolve after an
  apply to a temporary repository.
- Existing planner/applier tests continue to prove skip/force/backup semantics.
- Verify with `git check-ignore` and `git status` that `docs/changes/` is no
  longer ignored while unrelated ignore patterns still apply.
- Run:
  - `python3 -m unittest discover -s tests -v`;
  - `python3 -m compileall -q ai_workflow_bootstrap`;
  - a representative CLI dry run against a temporary directory if useful;
  - `git diff --check`.

### Tests intentionally not added

- Full-document snapshots.
- Assertions for every heading or explanatory sentence.
- Tests of Obsidian-specific behavior.
- Production tests for automatic migration or deletion, which do not exist.
- Network or external documentation-tool tests.

### Refactor resilience

The tests target generated paths, mode boundaries, link resolution and lifecycle
contracts. They should survive prose editing and internal template-loader
refactors as long as public generated behavior remains correct.

## 12. Execution Steps

1. Re-read the approved artifacts and confirm the worktree is safe.
2. Update the default manifest version, living-doc directories and output file
   mappings; remove only unused legacy source templates.
3. Add/rewrite the foundational living-doc templates with relative links,
   ownership, lifecycle, security and progressive-disclosure rules.
4. Expand the generated living-docs skill without adding auxiliary resources.
5. Integrate living-doc impacts into generated AGENTS, workflow, start prompt,
   spec/plan/tasks templates and relevant generated spec-driven skill wording.
6. Align README and the bootstrap repository's relevant workflow guidance.
7. Remove only the `docs/changes/` rule from the source `.gitignore` and inspect
   newly visible paths without staging unrelated artifacts.
8. Update focused manifest/planner tests and add generated-link validation.
9. Run targeted tests, then the full validation suite.
10. Inspect the final diff for conceptual locality, accidental runtime changes,
   secrets and broken paths.
11. Update this change's tasks and record any approved deviation in `notes.md`
    if necessary.

## 13. Rollback / Recovery

- Revert manifest/template/documentation/test changes as one conceptual unit.
- No database, state-schema or runtime migration requires rollback.
- Previously bootstrapped repositories are unaffected until the user applies a
  new pack.
- If a user applies the new pack and wants the old generated files, existing
  backups and Git history remain the recovery mechanisms; this change itself
  performs no deletion.

## 14. Notes

- Relative Markdown links are an approved portability decision for v1.
- The future `text-online-mmorpg` migration is a separate project change. This
  bootstrap increment provides the reusable structure and workflow only.
- External research informed the design, but the implementation deliberately
  adopts no external documentation framework or dependency.
- The change artifacts are intentionally not staged in this planning phase.
  After the approved `.gitignore` change they will become visible through the
  ordinary Git workflow, but staging and committing remain explicit user
  actions.
