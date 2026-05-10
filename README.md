# AI Bootstrap

Single-file Python bootstrap for setting up a repository with a guided Spec-Driven Development workflow.

The intended usage is simple:

1. Copy `bootstrap_sdd.py` into the root of a new or existing repository.
2. Run it once.
3. Start using the generated docs and prompts with Codex or Cursor.

## What the script does

When you run `bootstrap_sdd.py`, it inspects the target repository and generates a small working structure for AI-assisted development.

It creates:

- `AGENTS.md`
- `docs/SPEC_DRIVEN.md`
- `docs/START_PROMPT.md`
- `docs/changes/_templates/spec.md`
- `docs/changes/_templates/plan.md`
- `docs/changes/_templates/tasks.md`
- `docs/changes/_templates/notes.md`
- `docs/changes/_templates/open_questions.md`
- `docs/changes/_templates/decisions.md`

By default, it also creates:

- `.cursor/rules/spec-driven-always.mdc`
- `.cursor/plans/README.md`
- `.agents/skills/spec-driven/SKILL.md`

Optionally, with `--global-codex`, it also writes:

- `~/.codex/AGENTS.md`

## What it detects automatically

The script profiles the repository before generating files.

It detects things like:

- project name from the folder name, unless `--project-name` is provided;
- package manager such as `npm`, `pnpm`, `yarn`, `bun`, `uv`, or `poetry`;
- stack hints from files such as `Makefile`, `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, and `requirements.txt`;
- common commands such as build, test, lint, typecheck, fmt, check, and dev when they can be inferred.

Those detections are written into `AGENTS.md` so the repository starts with project-specific guidance instead of a totally generic template.

## How to use it

### In the current repository

Copy `bootstrap_sdd.py` into the repo root and run:

```bash
python3 bootstrap_sdd.py
```

### Against another path

You can also point it at another repository directory:

```bash
python3 bootstrap_sdd.py /path/to/repo
```

### Typical next steps

After running it:

1. Open the repository in Codex or Cursor.
2. Read or paste the prompt from `docs/START_PROMPT.md`.
3. Describe the change you want to build.
4. Review and approve the generated spec before implementation.

## Useful options

Preview without writing files:

```bash
python3 bootstrap_sdd.py --dry-run
```

Overwrite previously generated files:

```bash
python3 bootstrap_sdd.py --force
```

Overwrite without creating backup files:

```bash
python3 bootstrap_sdd.py --force --no-backup
```

Set an explicit project name in `AGENTS.md`:

```bash
python3 bootstrap_sdd.py --project-name "My Project"
```

Skip Cursor-specific files:

```bash
python3 bootstrap_sdd.py --no-cursor
```

Skip the local spec-driven skill:

```bash
python3 bootstrap_sdd.py --no-skill
```

Also install a small global Codex default:

```bash
python3 bootstrap_sdd.py --global-codex
```

## Generated structure

The default generated layout looks like this:

```text
.
├── AGENTS.md
├── docs/
│   ├── SPEC_DRIVEN.md
│   ├── START_PROMPT.md
│   └── changes/
│       └── _templates/
│           ├── decisions.md
│           ├── notes.md
│           ├── open_questions.md
│           ├── plan.md
│           ├── spec.md
│           └── tasks.md
├── .agents/
│   └── skills/
│       └── spec-driven/
│           └── SKILL.md
└── .cursor/
    ├── plans/
    │   └── README.md
    └── rules/
        └── spec-driven-always.mdc
```

## Workflow the generated files enforce

The generated workflow is:

`idea -> clarification -> spec -> approval -> plan -> tasks -> implementation -> validation`

For non-trivial work, the repository guidance tells the AI to:

- ask focused clarifying questions first;
- draft a spec under `docs/changes/<short-change-name>/spec.md`;
- wait for explicit approval;
- create `plan.md` and `tasks.md` only after approval;
- implement only after the plan exists;
- validate the result against the approved spec.

## Overwrite behavior

If a generated file already exists:

- the script leaves it untouched by default;
- `--force` allows overwriting it;
- backups are created automatically when overwriting, unless `--no-backup` is used.

## When to use this

This bootstrap is useful when you want a repo to start with:

- an explicit AI working agreement;
- a documented spec-first workflow;
- reusable templates for changes under `docs/changes/`;
- lightweight editor/agent integration for Codex and Cursor.

## Repository purpose

This repository is the source for `bootstrap_sdd.py` itself.

The goal is to keep the bootstrap:

- portable;
- small enough to copy into another repository;
- opinionated enough to produce consistent results;
- grounded in the actual behavior of the script.
