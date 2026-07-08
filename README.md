# ai-workflow-bootstrap

`ai-workflow-bootstrap` is a modular Python bootstrap for repositories that use a guided Spec-Driven Development workflow.

The package provides a CLI entrypoint:

```bash
python -m ai_workflow_bootstrap [path]
```

The legacy `bootstrap_sdd.py` script still works as a compatibility entrypoint.

## Quick Start

Run a preview without writing files:

```bash
python -m ai_workflow_bootstrap --dry-run .
```

Apply the default bootstrap to the current repository:

```bash
python -m ai_workflow_bootstrap .
```

Apply spec-driven files only:

```bash
python -m ai_workflow_bootstrap --no-living-docs .
```

Apply only living docs:

```bash
python -m ai_workflow_bootstrap --living-docs-only .
```

Also update the global Codex default:

```bash
python -m ai_workflow_bootstrap --global-codex .
```

## What It Generates

The bootstrap creates a workflow scaffold for spec-driven development.

By default, the new CLI generates:

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
- `.cursor/rules/spec-driven-always.mdc`
- `.cursor/plans/README.md`
- `.ai-bootstrap/state.json`

With `--no-living-docs`, the bootstrap keeps the spec-driven workflow and skips the living docs files and living-docs skill.

With `--living-docs-only`, it generates the living docs files and living-docs skill, but skips the spec-driven set.

## Workflow

The repository workflow is:

`idea -> clarification -> spec -> approval -> plan -> tasks -> implementation -> validation`

For non-trivial work, the generated docs tell the AI to:

- ask focused clarifying questions first;
- draft a spec under `docs/changes/<short-change-name>/spec.md`;
- wait for explicit approval;
- create `plan.md` and `tasks.md` only after approval;
- implement only after the plan exists;
- validate the result against the approved spec.

## Living Docs

Living docs are compact project memory, not a conversation transcript.

The core set is included by default in the new CLI:

- `docs/AI_CONTEXT.md` stays short and read-on-demand;
- `docs/LIVING_DOCUMENTATION.md` defines the living-docs policy;
- `docs/WORKFLOW_MODULES.md` explains optional module adoption;
- `docs/PROJECT_SPEC.md`, `docs/IMPLEMENTATION_STATUS.md`, `docs/ROADMAP.md`, `docs/IDEA_INBOX.md`, `docs/CANONICAL_DECISIONS.md`, and `docs/GLOSSARY.md` hold durable project knowledge.

## Template Packs

The bootstrap uses template packs so the generated content stays editable without changing the engine.

The default pack lives under `ai_workflow_bootstrap/template_packs/default/` in the source tree and is packaged with the Python distribution.

## State

Each real run writes `.ai-bootstrap/state.json` in the target repository.

That file records:

- tool name and version;
- template pack name and version;
- target path;
- enabled workflows;
- per-file status and template provenance;
- optional modules, if any are introduced later.

`--dry-run` does not write state.

## Compatibility

`bootstrap_sdd.py` remains available for compatibility.

It still behaves as the legacy entrypoint, so existing usage keeps working while the modular CLI becomes the preferred path.

Legacy usage still works:

```bash
python bootstrap_sdd.py --dry-run .
python bootstrap_sdd.py .
```

## Repository Purpose

This repository is the source for the bootstrap itself.

The goal is to keep it:

- portable;
- modular;
- opinionated enough to produce consistent results;
- grounded in the actual behavior of the tool.
