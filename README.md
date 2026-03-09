# AI Bootstrap

A simple repository for maintaining and evolving a single file: `AI_BOOTSTRAP`.

This file is meant to be copied into the root of a new or existing project and used as the initial instruction file for an AI to configure, organize, and document the repository.

## Goal

`AI_BOOTSTRAP` is intended to be **self-sufficient**.

That means it must contain, by itself, all the instructions needed for the AI to:

- inspect the repository,
- understand the stack and workflow,
- create or improve the minimum necessary documentation,
- create or improve the final project `AGENTS.md`,
- record open questions in `docs/OPEN_QUESTIONS.md`,
- record durable knowledge in `docs/PROJECT_MEMORY.md`,
- create a clear validation path,
- and delete itself when no actionable work remains.

The bootstrap must not depend on templates, auxiliary files, or pre-existing structure.

## How to use it

1. Copy `AI_BOOTSTRAP` into the root of the target project.
2. Run your AI in that repository.
3. Tell it something like:

```text
Follow the instructions in AI_BOOTSTRAP
```

4. As long as the `AI_BOOTSTRAP` file still exists, keep telling the AI to follow the instructions in it.
5. When everything is complete, the file should delete itself.

## Expected behavior

`AI_BOOTSTRAP` works as a temporary work queue.

The expected rules are:

- anything already completed should be removed from the file;
- anything partially completed should be rewritten so it contains only the remaining work;
- anything that does not apply, no longer makes sense, or cannot be done should be removed;
- when no actions remain, the file should be deleted.

In other words: **if the file still exists, there is still pending work**.

## When to use it

This file is useful for:

- new projects that do not yet have structure;
- existing projects with weak or inconsistent documentation;
- standardizing AI onboarding across multiple repositories;
- sharing a bootstrap workflow with other people;
- reducing the chance that the AI silently assumes things without recording uncertainty.

## What it will usually cause the AI to create

Depending on the project, the AI may create or improve files such as:

- `README.md`
- `AGENTS.md`
- `docs/PROJECT_OVERVIEW.md`
- `docs/PROJECT_INTENT.md`
- `docs/REPO_MAP.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/TESTING.md`
- `docs/PROJECT_MEMORY.md`
- `docs/OPEN_QUESTIONS.md`
- `docs/BOOTSTRAP_REPORT.md`
- `docs/DECISIONS/README.md`

These files do not need to exist beforehand. The bootstrap should decide what makes sense based on the actual repository.

## Philosophy

This repository exists to maintain a bootstrap that is:

- small enough for an AI to read,
- strong enough to be useful,
- generic enough to be reusable,
- and specific enough to produce operational results.

Core principles:

- do not assume silently;
- prefer repository evidence;
- make small, reversible changes;
- improve before replacing;
- avoid redundant documentation;
- keep open questions separate from durable knowledge;
- make the bootstrap unnecessary by the end.

## Repository structure

```text
.
├── AI_BOOTSTRAP
└── README.md
```

## Maintenance

This repository serves as the canonical source of the `AI_BOOTSTRAP` file.

As the file evolves, the goal is to improve:

- clarity,
- robustness,
- ability to work across different stacks,
- and the quality of the outputs produced by the AI.

Changes should keep the bootstrap:

- self-sufficient,
- minimal,
- portable,
- and independent from required templates.

## License

Use whatever license makes sense for your own use and for sharing it with other people.
