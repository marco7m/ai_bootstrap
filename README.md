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

The bootstrap always installs the recommended combination: spec-driven
development plus living documentation. Partial workflow modes are not
supported.

To upgrade divergent bootstrap-managed policy, preview first and then opt into
the managed update:

```bash
ai-bootstrap apply --force --dry-run .
ai-bootstrap apply --force .
```

`--force` updates only `managed` files. It does not overwrite living-document
seeds that evolved in the project. To update only managed infrastructure and
safe compositions, excluding seeded files entirely, add `--managed-only`.

Resetting project knowledge is a separate destructive action:

```bash
ai-bootstrap apply --reset-project-knowledge --dry-run .
ai-bootstrap apply --reset-project-knowledge \
  --confirm-reset-project-knowledge "RESET PROJECT KNOWLEDGE" .
```

The reset affects only manifest-declared `seeded` files. It never resets
project-owned or composed files. The tool creates no backups; use Git or another
repository-owned recovery mechanism when intentionally resetting knowledge.

`AGENTS.md` is bootstrap-managed. Store repository-specific agent instructions
in `AGENTS.project.md` instead. That complement is created by the project only
when a real local rule is needed; when present, the bootstrap reports it as
project-owned and preserves it even with `--force`.

## What It Generates

The bootstrap creates a workflow scaffold for spec-driven development.

By default, the new CLI generates:

- `AGENTS.md`
- `docs/SPEC_DRIVEN.md`
- `docs/START_PROMPT.md`
- `docs/INDEX.md`
- `docs/CAPABILITIES.md`
- `docs/LIVING_DOCUMENTATION.md`
- `docs/product/README.md`
- `docs/architecture/README.md`
- `docs/decisions/README.md`
- `docs/decisions/_template.md`
- `docs/ROADMAP.md`
- `docs/IDEA_INBOX.md`
- `docs/GLOSSARY.md`
- `docs/changes/_templates/spec.md`
- `docs/changes/_templates/plan.md`
- `docs/changes/_templates/tasks.md`
- `docs/changes/_templates/notes.md`
- `docs/changes/_templates/open_questions.md`
- `docs/changes/_templates/decisions.md`
- `.agents/skills/spec-driven/SKILL.md`
- `.agents/skills/living-docs/SKILL.md`
- `.agents/skills/living-docs/scripts/check_links.py`
- `.agents/skills/living-docs/scripts/check_living_docs.py`
- `.ai-bootstrap/state.json`

The bootstrap does not create an empty `AGENTS.project.md`. Managed `AGENTS.md`
instructs assistants to create and read it only when repository-specific
working guidance exists.

For a repository detected as Rust, the bootstrap also:

- safely composes `make dev`, `make run`, `make clean-dev`, `make test`,
  `make lint`, and `make typecheck` into `Makefile`;
- ensures `target/` is ignored without replacing `.gitignore`;
- generates `docs/architecture/rust-development.md` and a short conditional
  routing rule in `AGENTS.md`.

An existing equivalent Make target is preserved. A target with the same name
but a different recipe blocks the entire apply before any write. The error
shows both recipes and remediation; `--force` does not override project-owned
Make recipes.

## Workflow

The repository workflow is:

`idea -> clarification -> spec -> spec approval -> plan -> tasks -> plan/tasks approval -> implementation -> validation`

For non-trivial work, the generated docs tell the assistant to:

- ask focused clarifying questions first;
- draft a spec under `docs/changes/<short-change-name>/spec.md`;
- wait for explicit approval of the spec;
- create `plan.md` and `tasks.md` only after spec approval;
- request explicit approval of both the plan and tasks;
- implement only after plan/tasks approval;
- allow a different AI assistant or model to continue by reading the approved change artifacts;
- validate the result against the approved spec.

## Living Docs

Living docs are compact project memory, not a conversation transcript.

The core set is included by default in the new CLI:

- `docs/INDEX.md` is the only knowledge entry point and records whether coverage is a scaffold, incomplete, or baselined;
- `docs/CAPABILITIES.md` maps current state/evidence separately from approved targets and active changes;
- `docs/product/` describes what the project is, its rules, and expected behavior;
- `docs/architecture/` describes how the project is built and operates;
- `docs/decisions/` records durable decisions and their consequences;
- `docs/LIVING_DOCUMENTATION.md` defines the living-docs policy;
- `docs/ROADMAP.md`, `docs/IDEA_INBOX.md`, and `docs/GLOSSARY.md` hold supporting durable knowledge.

Current capability state uses `unknown`, `absent`, `partial`, `implemented`, `verified`, or `deprecated`. Approved future work is recorded separately so a verified current capability can have a planned evolution without ambiguity. Relative Markdown links keep the knowledge graph portable and mechanically verifiable.

Generated paths have explicit lifecycles:

- `managed`: bootstrap policy that changes only under `--force` when divergent;
- `seeded`: initial project-knowledge structure, safely updatable only while its
  content still matches the last applied hash;
- `project`: never created, overwritten, reset or deleted by the bootstrap;
- `composed`: structurally and idempotently merged with repository content;
- `migrated`: retired content deleted only when state proves it never drifted.

Evolved or untracked seeded files are preserved even with `--force`. An obsolete
file with drift or missing provenance becomes `migration_required` and blocks
the whole real apply before any write. This keeps migration review explicit
instead of attempting an automatic prose merge.

Protected project-owned paths are never overwritten or deleted by that option.

Compatible assistants can also use the open Agent Skills under `.agents/skills/`.

## Maintainability Guardrails

The generated workflow includes guardrails for code quality and test quality.

- Tests should protect behavior contracts, not private implementation details.
- File and function size are review triggers, not hard rules.
- The `maintainability-audit` skill helps spot brittle tests, mixed responsibilities, duplicated logic, and other signs that a small change should include a small local refactor.
- If a change needs a larger refactor, the workflow asks for a separate spec instead of hiding the debt.

## TUI

The interactive TUI is optional and only available when you install `textual`.

It is useful when you want a guided flow that:

- explains spec-driven development in simple terms;
- explains living docs in simple terms;
- previews the files before applying;
- requires explicit confirmation before writing;
- lets you choose the path and whether to include `.agents/skills/`;
- can update bootstrap-managed files without replacing evolved living docs;
- exposes seeded-knowledge reset as a separate, off-by-default control with its
  own typed confirmation;
- labels lifecycle, preservation, reset and migration blockers in the preview;
- supports English and Portuguese (pt-BR);
- can pick from recent or detected projects;
- stores recent projects in `~/.ai-workflow-bootstrap/recent-projects.json`;
- still supports manual path input.

## Template Packs

The bootstrap uses template packs so the generated content stays editable without changing the engine.

Pack entries may be conditional on detected stacks. Rendered file entries
declare `managed` or `seeded`; omitted lifecycle defaults to `managed` for pack
compatibility. Specialized collections represent safe compositions, protected
project paths and guarded obsolete migrations.

The default pack lives under `ai_workflow_bootstrap/template_packs/default/` in the source tree and is packaged with the Python distribution.

## State

Each real run writes `.ai-bootstrap/state.json` in the target repository.

That file records:

- tool name and version;
- template pack name and version;
- target path;
- enabled workflows;
- per-file status, lifecycle, ownership, template provenance, rendered
  `applied_content_hash`, and applied pack version when established;
- safely retired-file disposition when applicable;
- optional modules, if any are introduced later.

`--dry-run` does not write state.

State from older versions remains readable. Missing or malformed per-file
applied provenance never grants permission to overwrite seeded knowledge or
delete obsolete content. Selective managed updates merge state rather than
discarding unselected seeded provenance.

## Auditing Previously Affected Projects

The corrected bootstrap prevents new loss; it cannot reconstruct documentation
that an older run already replaced. For a suspected project:

1. Inspect `.ai-bootstrap/state.json` for seeded owners whose last legacy status
   is `overwritten`.
2. Run the generated `check_living_docs.py`, optionally with
   `--baseline-ref <git-ref>`.
3. Compare prior Git content, current change artifacts, code/tests and safe
   runtime evidence.
4. Restore the union of still-valid prior facts and later supported increments;
   do not blindly restore an old revision or infer product intent from code.
5. Give every removed capability/fact an explicit disposition, restore an
   honest coverage status, then run both semantic and link checkers.

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
