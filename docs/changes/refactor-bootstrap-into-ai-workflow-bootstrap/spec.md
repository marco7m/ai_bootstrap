# Change Spec: Refactor bootstrap_sdd.py into ai-workflow-bootstrap

## 1. Summary

Refactor the current single-file bootstrap into a modular Python project named `ai-workflow-bootstrap` while preserving the current workflow and generated outputs as the compatibility baseline.

## 2. Problem

`bootstrap_sdd.py` currently mixes CLI handling, repository inspection, template rendering, file writing, backup behavior, and workflow policy in one file.

That makes it harder to extend safely, harder to move templates out into editable assets, and harder to prepare for future surfaces such as a TUI.

## 3. Goal

Create a modular bootstrap project with a decoupled engine, editable external templates, living documentation support, and a stable CLI entrypoint, while keeping the current user-facing behavior familiar.

## 4. Scope

This future change covers:

- modularizing the bootstrap codebase;
- separating workflow logic from CLI presentation;
- moving templates out of code into editable external files;
- defining core universal documentation applied by default;
- defining optional documentation modules for later adoption;
- recording applied state in the target project;
- preserving the current bootstrap behavior whenever practical;
- preparing the architecture for future TUI support without implementing a TUI yet.

## 5. Out of Scope

This change does not include:

- implementing the modular engine now;
- modifying `bootstrap_sdd.py` in this documentation-only stage;
- implementing a TUI;
- adding `Textual`, `Rich`, `Jinja2`, or web frameworks in this change;
- creating `plan.md` or `tasks.md` yet;
- forcing every optional documentation module into every target project by default;
- redesigning the workflow into something unrelated to the current spec-first model.

## 6. Users / Actors

- Repository maintainers who will later split the script into a Python package.
- Developers who will run the bootstrap against target repositories.
- AI agents that will follow the generated documentation workflow.
- Future maintainers who need templates and docs to be editable without code changes.

## 7. Functional Requirements

- The future project must have:
  - distribution name: `ai-workflow-bootstrap`;
  - Python package name: `ai_workflow_bootstrap`;
  - main CLI entrypoint: `python -m ai_workflow_bootstrap [path]`.
- The future project must preserve the current CLI concept: run against a target repository and generate workflow docs.
- It must explicitly support these flags:
  - `--project-name`
  - `--dry-run`
  - `--force`
  - `--global-codex`
  - `--no-backup`
  - `--no-cursor`
  - `--no-skill`
  - `--no-living-docs`
  - `--living-docs-only`
- Default behavior must apply spec-driven docs plus living docs core.
- `--no-living-docs` must apply only spec-driven output.
- `--living-docs-only` must apply only living docs and the living-docs skill.
- The bootstrap must never overwrite existing generated files unless `--force` is provided.
- With `--force`, overwrites must create backups unless `--no-backup` is also provided.
- `--dry-run` must not write anything.
- The future project must generate `AGENTS.md`, `docs/SPEC_DRIVEN.md`, and `docs/START_PROMPT.md` as part of the compatibility baseline unless a later approved change explicitly removes `START_PROMPT.md`.
- It must keep the current spec-first workflow intact: clarification, spec, approval, plan, tasks, implementation, validation.
- It must separate templates from engine logic so templates can be edited without rewriting the bootstrap core.
- It must record applied state for the target repository in `.ai-bootstrap/state.json`.
- It must support core universal documentation as the default output set.
- It must keep optional modules available as templates but not create them by default in target projects.
- Adoption of an optional module must require explicit user approval.

## 8. Non-Functional Requirements

### Maintainability

The codebase must be easier to extend than the current monolith, with clear module ownership and small cohesive modules.

### Modularity / Architecture

The engine must be decoupled from CLI presentation and future TUI presentation.

Template loading, rendering, repository scanning, planning, applying, backup, and state persistence should be separated into focused modules.

### Security / Privacy

The bootstrap must not introduce secret handling regressions.

It must continue to avoid writing sensitive data into generated docs or logs.

### Reliability

The future project should preserve overwrite, backup, and dry-run behavior.

The state file should support repeatable bootstrap runs without losing prior applied-state knowledge.

### Performance

The refactor does not need new performance work, but it should remain lightweight enough to run as a one-shot bootstrap.

### Observability

The CLI should continue to explain what it detected and what it wrote.

Applied state should be readable and useful for later tooling.

### Simplicity

The modular design should stay boring and explicit.

Do not introduce extra infrastructure unless the future spec requires it.

## 9. Proposed Architecture

The future project should be organized around a reusable engine with these modules:

- `ai_workflow_bootstrap/cli.py`
  - Parses CLI arguments, dispatches to the engine, and formats user-facing output.
  - It should stay thin and avoid owning workflow rules.
- `ai_workflow_bootstrap/core/scanner.py`
  - Inspects the target repository and builds the repo profile.
  - It should detect stack hints, commands, and basic repo metadata.
- `ai_workflow_bootstrap/core/template_pack.py`
  - Loads template packs from disk and exposes their manifest and assets.
  - It should understand the default pack structure and template provenance.
- `ai_workflow_bootstrap/core/renderer.py`
  - Renders templates using a standard-library-friendly or minimal custom renderer.
  - It should not depend on Jinja2 or other new template engines in the MVP.
- `ai_workflow_bootstrap/core/planner.py`
  - Computes what would be written, updated, skipped, or backed up for a target run.
  - It should support dry-run planning and status classification.
- `ai_workflow_bootstrap/core/applier.py`
  - Applies the planned writes to disk when not in dry-run mode.
  - It should respect overwrite rules, optional modules, and workflow selection.
- `ai_workflow_bootstrap/core/backup.py`
  - Handles backup naming and backup creation when overwriting existing files.
  - It should be the only module responsible for backup policy details.
- `ai_workflow_bootstrap/core/state.py`
  - Reads and writes `.ai-bootstrap/state.json`.
  - It should persist applied state, template provenance, and file outcomes.

The engine should expose pure or mostly pure operations where possible and keep side effects at the boundaries.

## 10. External Templates

Templates should live outside the engine so they can be edited independently.

The expected bootstrap project structure is:

- `template_packs/default/manifest.json`
- `template_packs/default/templates/...`
- `template_packs/default/optional_modules/...`

`manifest.json` is preferred for the MVP because it avoids adding YAML dependencies.

The bootstrap project should provide editable templates for:

- `AGENTS.md`
- `docs/SPEC_DRIVEN.md`
- `docs/START_PROMPT.md`
- `docs/AI_CONTEXT.md`
- `docs/LIVING_DOCUMENTATION.md`
- `docs/WORKFLOW_MODULES.md`
- `docs/PROJECT_SPEC.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `docs/ROADMAP.md`
- `docs/IDEA_INBOX.md`
- `docs/CANONICAL_DECISIONS.md`
- `docs/GLOSSARY.md`
- `docs/changes/_templates/spec.md`
- `docs/changes/_templates/plan.md`
- `docs/changes/_templates/tasks.md`
- `docs/changes/_templates/notes.md`
- `docs/changes/_templates/open_questions.md`
- `docs/changes/_templates/decisions.md`
- `.agents/skills/spec-driven/SKILL.md`
- `.agents/skills/living-docs/SKILL.md`

## 11. Core Universal Documentation

The bootstrap should apply this core documentation set by default in target projects:

- `AGENTS.md`
- `docs/AI_CONTEXT.md`
- `docs/SPEC_DRIVEN.md`
- `docs/START_PROMPT.md`
- `docs/LIVING_DOCUMENTATION.md`
- `docs/WORKFLOW_MODULES.md`
- `docs/PROJECT_SPEC.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `docs/ROADMAP.md`
- `docs/IDEA_INBOX.md`
- `docs/CANONICAL_DECISIONS.md`
- `docs/GLOSSARY.md`
- `docs/changes/_templates/spec.md`
- `docs/changes/_templates/plan.md`
- `docs/changes/_templates/tasks.md`
- `docs/changes/_templates/notes.md`
- `docs/changes/_templates/open_questions.md`
- `docs/changes/_templates/decisions.md`
- `.agents/skills/spec-driven/SKILL.md`
- `.agents/skills/living-docs/SKILL.md`

`docs/AI_CONTEXT.md` must stay short.

## 12. Optional Documentation Modules

The following documents should be available as optional modules and templates, but not created by default in every target project:

- `docs/ARCHITECTURE.md`
- `docs/DATA_MODEL.md`
- `docs/API_CONTRACTS.md`
- `docs/SECURITY.md`
- `docs/TESTING_STRATEGY.md`
- `docs/OPERATIONS.md`
- `docs/OBSERVABILITY.md`
- `docs/DEPLOYMENT.md`
- `docs/DOMAIN_MODEL.md`
- `docs/AI_PIPELINES.md`
- `docs/INTEGRATIONS.md`

These modules should live in the bootstrap project as templates, not as default target outputs.

`docs/WORKFLOW_MODULES.md` must teach the AI when to propose adoption of an optional module.

Adoption of an optional module must require explicit user approval.

## 13. Living Documentation Rules

Living docs must be compact memory, not transcripts.

Rules:

- write the current state, not the full discussion history;
- classify entries as Idea, Candidate, Canonical, Planned, Implemented, Future, Rejected, or Deprecated;
- prefer short, current, decision-oriented entries;
- keep `docs/AI_CONTEXT.md` brief;
- do not force every document to be read every time;
- read docs on demand according to the task;
- keep durable project knowledge in the right doc instead of scattering it across chat logs.

## 14. CLI Compatibility

The future modular project should keep the current CLI recognizable and functional.

It should continue to accept a target path and the current operational switches, and it should continue to report what it would write or did write.

The current `bootstrap_sdd.py` behavior is the compatibility baseline.

The future refactor should preserve, as much as practical:

- generated repo guidance files;
- dry-run behavior;
- force and backup behavior;
- global Codex config support;
- cursor opt-out behavior;
- skill opt-out behavior;
- repository detection and command suggestions;
- the current spec-first workflow language and intent;
- `docs/START_PROMPT.md` generation.

Compatibility strategy:

- `bootstrap_sdd.py` should remain the baseline during refactoring.
- It may become a temporary wrapper around the new CLI if that reduces migration risk.
- If it is replaced rather than wrapped, that replacement must be documented and approved explicitly.
- Do not remove compatibility without a separate decision.

Where behavior changes are unavoidable, they should be explicitly documented and kept minimal.

## 15. State File

The target project should receive a `.ai-bootstrap/state.json` file that records applied bootstrap state.

Minimum expected shape:

```json
{
  "tool_name": "ai-workflow-bootstrap",
  "tool_version": "...",
  "template_pack": "default",
  "template_pack_version": "...",
  "applied_at": "...",
  "target_path": "...",
  "enabled_workflows": ["spec-driven", "living-docs"],
  "files": {
    "AGENTS.md": {
      "status": "written|skipped|unchanged|overwritten",
      "template": "...",
      "template_hash": "..."
    }
  },
  "optional_modules": []
}
```

The exact schema can be refined during implementation, but the state file must be stable enough to be useful.

## 16. Future TUI Preparation

The architecture should make a future TUI possible without forcing a TUI now.

That means:

- keep core workflow logic separate from the CLI;
- avoid hard-coding CLI-only assumptions into the engine;
- keep state inspection and rendering reusable;
- define clean boundaries for future interactive presentation;
- do not add `Textual` now;
- do not create a TUI now;
- treat TUI as a separate future spec and change.

## 17. Compatibility With Existing Script

The current `bootstrap_sdd.py` behavior is the compatibility baseline.

The future refactor should preserve, as much as practical:

- generated repo guidance files;
- dry-run behavior;
- force and backup behavior;
- global Codex config support;
- cursor opt-out behavior;
- skill opt-out behavior;
- repository detection and command suggestions;
- the current spec-first workflow language and intent.

The current script must remain untouched in this documentation-only phase.

## 18. Dependency Policy

The MVP should prefer the Python standard library.

Do not add `Jinja2`, `Textual`, `Rich`, or web frameworks in this change.

External templates must use a format that the standard library can support directly, or a minimal custom renderer if needed.

Any future dependency must be justified in its own spec and decision, not smuggled into this change.

## 19. Risks

- The modularization may accidentally drift from current output and break user expectations.
- Splitting templates out of code may create versioning and drift concerns if template ownership is unclear.
- The state file could become a source of stale or misleading truth if its schema is too weak.
- Optional module support could become overcomplicated if the defaults and opt-in paths are not kept clear.
- A future TUI could pressure the engine design if boundaries are not kept clean now.

## 20. Acceptance Criteria

- The refactor can be planned without ambiguity about the desired end state.
- The future project has a clear modular direction.
- The current bootstrap behavior is identified as the compatibility baseline.
- Core universal documentation is defined, including `docs/START_PROMPT.md`.
- Optional documentation modules are clearly separated from default outputs.
- External templates are explicitly called out as editable assets.
- State persistence in `.ai-bootstrap/state.json` is defined.
- Future TUI readiness is specified without implementing a TUI.
- The package/distribution naming and CLI entrypoint are explicit.
- The supported flags and their behavior are explicit.
- The spec is detailed enough to support later `plan.md` and `tasks.md` creation.
- The plan for validation includes scanner, planner, applier, backup, state, workflow-selection, and manual dry-run coverage.

## 21. Validation Strategy

The implementation phase should include at least:

- a scanner test for detecting basic stack hints and commands;
- a planner test for dry-run output and file status classification;
- an applier test for not overwriting without `--force`;
- a backup test for overwrite behavior with `--force`;
- a state-file test for `.ai-bootstrap/state.json`;
- a workflow-selection test for `--living-docs-only` and `--no-living-docs`;
- a manual validation run using `--dry-run` in a temporary directory.

Tests should protect behavior, not implementation details.

## 22. Open Questions

- What package layout should the modular Python project use beyond the module split listed here?
- How should template versioning and template hashes be generated and updated?
- Should the core universal docs be generated on every run or only during bootstrap?
- How should existing generated files be detected and updated during repeat runs?
- What is the final minimal compatibility bar for the current CLI flags in edge cases?
- Should optional documentation modules be grouped or enabled individually in the manifest?
