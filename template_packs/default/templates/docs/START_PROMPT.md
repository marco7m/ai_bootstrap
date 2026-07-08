# Start Prompt

## Codex

```text
Read AGENTS.md, docs/SPEC_DRIVEN.md, and the spec-driven skill if available.
Use the guided Spec-Driven Development workflow in this repository.
Prefer plan mode first for ambiguous or multi-step work.
Pay special attention to architectural locality, module boundaries, security, configuration, and dependency discipline.

My request is:
<describe what you want to build here>
```

If you use the Codex CLI, a good first move is:

```text
/plan Read AGENTS.md, docs/SPEC_DRIVEN.md, and use the spec-driven skill.
I want to build: <describe the change>
Guide me through the spec first, ask focused questions, and only implement after the spec is approved.
Preserve clear module ownership and call out any architecture smell you notice.
```

## Cursor

Turn on Plan Mode first, then paste:

```text
Read AGENTS.md and docs/SPEC_DRIVEN.md.
Use the guided Spec-Driven Development workflow in this repository.
Please question me first, draft the spec, wait for my approval, then create the plan and tasks before implementing.
Pay attention to architectural locality, security, configuration, dependency discipline, and maintainability.

My request is:
<describe what you want to build here>
```

