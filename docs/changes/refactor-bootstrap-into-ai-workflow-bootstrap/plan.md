# Implementation Plan: Refactor bootstrap_sdd.py into ai-workflow-bootstrap

## 1. Summary

Refactor the current single-file bootstrap into a modular Python package named `ai_workflow_bootstrap`, with a stable CLI entrypoint, external template packs, state persistence, and a compatibility path that preserves the current script behavior as the baseline.

The implementation should proceed in safe stages so the current workflow remains usable while the package is introduced.

## 2. Relevant Existing Context

Current repository state:

- `bootstrap_sdd.py` is a single-file bootstrap script.
- `README.md` describes the script and the current generated structure.
- The script already handles:
  - CLI parsing with `argparse`;
  - repo profile detection;
  - template generation through in-code string constants;
  - file writing with `dry-run`, `force`, and backup behavior;
  - optional Cursor files;
  - optional local Codex skill generation;
  - optional global Codex config output.

The approved spec defines the future target:

- distribution name: `ai-workflow-bootstrap`;
- Python package name: `ai_workflow_bootstrap`;
- CLI entrypoint: `python -m ai_workflow_bootstrap [path]`;
- default workflows: spec-driven + living docs core;
- optional modules as templates only;
- `.ai-bootstrap/state.json` for applied state.

## 3. Existing Conventions Found

- Folder structure: single root-level script with generated docs under `docs/`, templates under `docs/changes/_templates/`, and optional `.cursor/` and `.agents/` outputs.
- Naming style: snake_case functions and dataclasses, explicit helper functions, straightforward module-local constants.
- Error handling: simple exit codes and printed messages; failures are mostly guarded by direct checks.
- Logging: human-readable CLI summary printed to stdout; no logging framework.
- Testing pattern: no formal test harness is present in the current script.
- Config pattern: CLI flags control behavior; no config files besides generated outputs.
- External integration pattern: none beyond filesystem writes and optional `~/.codex/AGENTS.md`.
- Persistence/data access pattern: filesystem-only; no database or network persistence.

Important script behaviors to preserve:

- `--dry-run` shows planned actions without writing.
- `--force` allows overwrites.
- `--no-backup` suppresses backup creation when overwriting.
- `--no-cursor` and `--no-skill` suppress optional generated outputs.
- `--global-codex` writes the global `~/.codex/AGENTS.md` default.
- repo scanning infers package manager, top-level directories, and common commands.

## 4. Proposed Changes

Build a new package in stages:

1. create `ai_workflow_bootstrap/` as the new code home without breaking the existing script;
2. extract small types and models from the monolithic script;
3. extract repository scanning into `core/scanner.py`;
4. move templates into `template_packs/default/`;
5. implement `template_pack.py`, `renderer.py`, `planner.py`, `applier.py`, `backup.py`, and `state.py`;
6. add packaging metadata in `pyproject.toml`, plus `ai_workflow_bootstrap/__init__.py` and `ai_workflow_bootstrap/__main__.py`, with `python -m ai_workflow_bootstrap [path]` as the primary entrypoint;
7. keep `bootstrap_sdd.py` functioning as the compatibility entrypoint, with preference for turning it into a temporary wrapper around the new CLI if that can be done without breaking behavior;
8. migrate templates in two phases: first preserve current `bootstrap_sdd.py` output through external templates, then add living docs core;
9. add optional documentation modules as templates only;
10. add focused tests around scanning, planning, applying, backup, workflow selection, and state;
11. validate with `--dry-run` in a temporary directory before considering the refactor complete.

## 5. Module Boundaries

- `ai_workflow_bootstrap/cli.py`
  - Owns argument parsing, command dispatch, and user-facing summary output.
  - Must not contain template policy or filesystem write logic.
- `ai_workflow_bootstrap/core/scanner.py`
  - Owns repo inspection and profile building.
  - Must not render templates or write files.
- `ai_workflow_bootstrap/core/template_pack.py`
  - Owns loading template pack manifests and assets.
  - Must not decide which workflows are enabled.
- `ai_workflow_bootstrap/core/renderer.py`
  - Owns template interpolation using a standard-library-friendly or minimal custom renderer.
  - Must not pull in Jinja2, Rich, Textual, or web frameworks in the MVP.
- `ai_workflow_bootstrap/core/planner.py`
  - Owns the decision of what would happen for a run: written, skipped, unchanged, overwritten, backed up.
  - Must remain side-effect free.
- `ai_workflow_bootstrap/core/applier.py`
  - Owns applying the plan to disk.
  - Must respect overwrite and workflow-selection rules.
- `ai_workflow_bootstrap/core/backup.py`
  - Owns backup naming and backup creation.
  - Must be the only place that encodes backup policy.
- `ai_workflow_bootstrap/core/state.py`
  - Owns `.ai-bootstrap/state.json` read/write behavior.
  - Must preserve applied-state provenance and file status data.

## 6. Architecture Locality Check

Expected file groups for the migration:

- package bootstrap: new package files under `ai_workflow_bootstrap/`;
- scanning and profile detection: `core/scanner.py`;
- template assets: `template_packs/default/`;
- render/plan/apply/backup/state: core module set;
- CLI surface: `ai_workflow_bootstrap/cli.py` and package `__main__.py`;
- compatibility bridge: `bootstrap_sdd.py` only if kept as a temporary wrapper;
- packaging metadata: `pyproject.toml`, package `__init__.py`, and `__main__.py`;
- tests: a small test package focused on behavior, not implementation details.

This is an expected cross-cutting refactor, but related changes should still stay grouped by responsibility.

## 7. Data / API / Interface Impact

- No external API is introduced.
- The CLI interface becomes package-based: `python -m ai_workflow_bootstrap [path]`.
- `.ai-bootstrap/state.json` is a new local persistence format in target repositories.
- Template packs introduce a manifest-driven interface for rendered outputs.

## 8. Security / Privacy Impact

- The refactor must not add secret handling features.
- No secrets should be written into generated docs or state.
- The CLI should continue to avoid logging sensitive payloads.
- Any file writes to the target repository or `~/.codex/AGENTS.md` should remain explicit and user-controlled.

## 9. Dependency Impact

- MVP must prefer the Python standard library.
- Do not add Jinja2, Textual, Rich, or web frameworks.
- Prefer `json` for the manifest format over YAML.
- Use `unittest` or another standard-library testing path for the MVP.
- Do not add `pytest` in this MVP unless a separate future decision explicitly approves it.
- If a future dependency becomes necessary, it must be introduced in a separate spec and decision.

## 10. Risks

- The modular split may drift from current behavior if the compatibility path is not tested against the current script output.
- Template extraction may create accidental output changes if defaults or placeholders are interpreted differently.
- The state file could become stale or misleading if file statuses are not updated consistently.
- A wrapper approach for `bootstrap_sdd.py` may be awkward if the new CLI diverges too much from current assumptions.
- Living-docs support may expand scope if the default workflow set is not kept strict.

## 11. Validation Strategy

Minimum validation for the implementation:

- scanner test covering stack and command detection from simple repo fixtures;
- planner test covering dry-run and per-file status classification;
- applier test proving existing files are not overwritten without `--force`;
- backup test proving overwrite creates backups with `--force` unless `--no-backup`;
- state test covering `.ai-bootstrap/state.json` content and update behavior;
- workflow-selection test covering `--no-living-docs` and `--living-docs-only`;
- manual `--dry-run` run in a temporary directory;
- baseline compatibility validation comparing the current script and the new CLI in comparable temporary directories, with intentional differences recorded explicitly.

Validation should focus on contract-level behavior, not internal call order.

## 12. Execution Steps

1. Create the `ai_workflow_bootstrap` package skeleton and module boundaries without changing current behavior.
2. Extract small shared models/types from the current script into package code.
3. Extract repository scanning into `core/scanner.py` and verify it still detects the same basic data.
4. Move template content into `template_packs/default/manifest.json` and template files.
5. Implement `template_pack.py`, `renderer.py`, `planner.py`, `applier.py`, `backup.py`, and `state.py`.
6. Add packaging metadata in `pyproject.toml`, plus `ai_workflow_bootstrap/__init__.py` and `ai_workflow_bootstrap/__main__.py`, and wire `python -m ai_workflow_bootstrap [path]`.
7. Keep `bootstrap_sdd.py` working as the compatibility entrypoint, preferably as a temporary wrapper if behavior can be preserved exactly.
8. Add living docs core outputs and supporting templates in a second phase after preserving the current bootstrap output through external templates.
9. Add optional documentation modules as templates only, with approval-driven adoption.
10. Add tests for scanner, planner, applier, backup, state, and workflow selection using standard-library tooling.
11. Validate with dry-run in a temporary directory and compare behavior against the current baseline.

## 13. Rollback / Recovery

If the refactor causes regressions:

- preserve the current `bootstrap_sdd.py` baseline behavior;
- keep `bootstrap_sdd.py` as the active entrypoint until the package path is stable;
- revert the package wiring before removing the script path;
- keep the template pack changes isolated so they can be rolled back without touching the script;
- use the existing script output as the fallback reference for compatibility.

## 14. Notes

- The current script is the behavioral baseline, not the future architecture target.
- The MVP should stay standard-library-first.
- Living docs should remain compact memory, not conversation transcripts.
- Future TUI work remains out of scope for this change and must be handled in a separate spec.
