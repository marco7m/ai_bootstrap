# ai-workflow-bootstrap

`ai-workflow-bootstrap` is a modular, AI-agnostic Python bootstrap for repositories that use a guided Spec-Driven Development workflow.

The package opens an interactive TUI by default:

```bash
ai-bootstrap
```

For an interactive setup flow, install the optional TUI extra:

```bash
pip install -e ".[tui]"
```

Then open the TUI with either:

```bash
ai-workflow-bootstrap tui
ai-bootstrap tui
python -m ai_workflow_bootstrap
python bootstrap_sdd.py
```

The TUI is the friendliest path for new contributors and interns. It explains the workflow in plain language, shows a preview before applying, and only writes files after explicit confirmation.

## Quick Start

Run a preview without writing files:

```bash
ai-bootstrap apply --dry-run .
python bootstrap_sdd.py apply --dry-run .
```

Apply the default bootstrap to the current repository:

```bash
ai-bootstrap apply .
```

Apply spec-driven files only:

```bash
ai-bootstrap apply --no-living-docs .
```

Apply only living docs:

```bash
ai-bootstrap apply --living-docs-only .
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
- `.ai-bootstrap/state.json`

With `--no-living-docs`, the bootstrap keeps the spec-driven workflow and skips the living docs files and living-docs skill.

With `--living-docs-only`, it generates the living docs files and living-docs skill, but skips the spec-driven set.

## Workflow

The repository workflow is:

`idea -> clarification -> spec -> approval -> plan -> tasks -> implementation -> validation`

For non-trivial work, the generated docs tell the assistant to:

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

Compatible assistants can also use the open Agent Skills under `.agents/skills/`.

## TUI

The interactive TUI is optional and only available when you install `textual`.

It is useful when you want a guided flow that:

- explains spec-driven development in simple terms;
- explains living docs in simple terms;
- previews the files before applying;
- requires explicit confirmation before writing;
- lets you choose the path, workflow mode, and whether to include `.agents/skills/`.

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

## Local Launcher

`bootstrap_sdd.py` is a thin local launcher for the same CLI.

Use it when you want a single-file entrypoint from the repository root:

```bash
python bootstrap_sdd.py
python bootstrap_sdd.py apply --dry-run .
```

## Repository Purpose

This repository is the source for the bootstrap itself.

The goal is to keep it:

- portable;
- modular;
- opinionated enough to produce consistent results;
- grounded in the actual behavior of the tool.
