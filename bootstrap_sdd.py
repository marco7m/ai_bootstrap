#!/usr/bin/env python3
"""
Bootstrap a repository for a guided Spec-Driven Development workflow.

This script is intended to be run once in a new or existing repository. It creates
repository guidance files that help AI coding agents work through:

idea -> clarification -> spec -> approval -> plan -> tasks -> implementation -> validation.

The generated content emphasizes:
- clear module ownership;
- architectural locality;
- maintainability;
- security and secrets hygiene;
- minimal but explicit configuration;
- dependency discipline;
- validation before completion.

The bootstrap itself is intentionally a single file so it can be copied into a
repository, executed once, and discarded.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from textwrap import dedent

try:
    import tomllib  # Python 3.11+
except Exception:  # pragma: no cover - only used on old Python versions
    tomllib = None


@dataclass
class WriteResult:
    path: Path
    status: str
    message: str


@dataclass
class RepoProfile:
    project_name: str
    repo_name: str
    package_manager: str | None = None
    detected_stacks: list[str] = field(default_factory=list)
    commands: dict[str, str] = field(default_factory=dict)
    top_dirs: list[str] = field(default_factory=list)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "change"


def detect_project_name(target: Path, explicit_name: str | None) -> str:
    if explicit_name:
        return explicit_name.strip()
    name = target.resolve().name.strip()
    return name or "My Project"


def read_text_if_exists(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def detect_package_manager(target: Path) -> str | None:
    if (target / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (target / "bun.lockb").exists() or (target / "bun.lock").exists():
        return "bun"
    if (target / "yarn.lock").exists():
        return "yarn"
    if (target / "package-lock.json").exists() or (target / "npm-shrinkwrap.json").exists():
        return "npm"
    if (target / "package.json").exists():
        return "npm"
    if (target / "uv.lock").exists():
        return "uv"
    if (target / "poetry.lock").exists():
        return "poetry"
    return None


def parse_make_targets(makefile_text: str) -> set[str]:
    targets: set[str] = set()
    for line in makefile_text.splitlines():
        if line and not line.startswith("\t"):
            match = re.match(r"^([A-Za-z0-9_.-]+):", line)
            if match:
                targets.add(match.group(1))
    return targets


def detect_repo_profile(target: Path, project_name: str) -> RepoProfile:
    profile = RepoProfile(
        project_name=project_name,
        repo_name=target.resolve().name,
        package_manager=detect_package_manager(target),
    )

    top_dirs = []
    children = sorted(target.iterdir(), key=lambda p: p.name.lower()) if target.exists() else []
    for child in children:
        if child.is_dir() and not child.name.startswith("."):
            if child.name in {
                "src",
                "app",
                "lib",
                "frontend",
                "backend",
                "server",
                "client",
                "docs",
                "tests",
                "test",
                "packages",
                "services",
            }:
                top_dirs.append(child.name)
    profile.top_dirs = top_dirs

    makefile_text = read_text_if_exists(target / "Makefile") or read_text_if_exists(target / "makefile")
    make_targets = parse_make_targets(makefile_text) if makefile_text else set()

    def maybe_set(name: str, command: str) -> None:
        if name not in profile.commands:
            profile.commands[name] = command

    # Makefile is usually the best source of project-specific commands.
    if make_targets:
        profile.detected_stacks.append("make")
        for name in ("build", "test", "lint", "typecheck", "check", "fmt"):
            if name in make_targets:
                maybe_set(name, f"make {name}")

    package_json = target / "package.json"
    if package_json.exists():
        profile.detected_stacks.append("node")
        try:
            data = json.loads(read_text_if_exists(package_json) or "{}")
            scripts = data.get("scripts", {}) if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            scripts = {}
        runner = profile.package_manager or "npm"
        run = {
            "npm": "npm run",
            "pnpm": "pnpm",
            "yarn": "yarn",
            "bun": "bun run",
        }.get(runner, "npm run")
        for name in ("build", "test", "lint", "typecheck", "check", "dev"):
            if name in scripts:
                maybe_set(name, f"{run} {name}")

    cargo_toml = target / "Cargo.toml"
    if cargo_toml.exists():
        profile.detected_stacks.append("rust")
        maybe_set("build", "cargo build")
        maybe_set("test", "cargo test")
        maybe_set("lint", "cargo clippy --all-targets --all-features -- -D warnings")
        maybe_set("fmt", "cargo fmt --all --check")

    go_mod = target / "go.mod"
    if go_mod.exists():
        profile.detected_stacks.append("go")
        maybe_set("build", "go build ./...")
        maybe_set("test", "go test ./...")
        maybe_set("fmt", "gofmt -w .")

    pyproject = target / "pyproject.toml"
    if pyproject.exists() and tomllib is not None:
        profile.detected_stacks.append("python")
        prefix = {
            "uv": "uv run ",
            "poetry": "poetry run ",
        }.get(profile.package_manager or "", "")
        try:
            data = tomllib.loads(read_text_if_exists(pyproject))
        except Exception:
            data = {}
        tool = data.get("tool", {}) if isinstance(data, dict) else {}
        if "pytest" in tool or (target / "pytest.ini").exists() or (target / "tests").exists():
            maybe_set("test", f"{prefix}pytest")
        if "ruff" in tool:
            maybe_set("lint", f"{prefix}ruff check .")
            maybe_set("fmt", f"{prefix}ruff format --check .")
        elif "black" in tool:
            maybe_set("fmt", f"{prefix}black --check .")
        if "mypy" in tool:
            maybe_set("typecheck", f"{prefix}mypy .")
        maybe_set("build", f"{prefix}python -m build")

    if (target / "requirements.txt").exists() and "python" not in profile.detected_stacks:
        profile.detected_stacks.append("python")
        maybe_set("test", "pytest")

    # Helpful fallback command groups.
    if "check" not in profile.commands:
        parts = [profile.commands[name] for name in ("lint", "typecheck", "test") if name in profile.commands]
        if parts:
            maybe_set("check", " && ".join(parts))

    return profile


def format_repo_layout(profile: RepoProfile) -> str:
    if not profile.top_dirs:
        return "- No obvious top-level source directories detected yet. Add them later if useful."
    return "\n".join(f"- `{name}/`" for name in profile.top_dirs)


def format_commands(profile: RepoProfile) -> str:
    ordered = ["build", "test", "lint", "typecheck", "fmt", "check", "dev"]
    lines = []
    for name in ordered:
        if name in profile.commands:
            lines.append(f"- `{profile.commands[name]}` — {name}")
    if not lines:
        lines.append("- No reliable project commands detected yet. Update this file once the repo has build/test/lint commands.")
    return "\n".join(lines)


def format_detected_stack(profile: RepoProfile) -> str:
    if not profile.detected_stacks:
        return "unknown"
    return ", ".join(profile.detected_stacks)


AGENTS_TEMPLATE = """\
# AGENTS.md

This repository uses a guided Spec-Driven Development workflow by default.

## Project identity
- Project name: {project_name}
- Repository root: {repo_name}
- Detected stack(s): {detected_stacks}

## Repository layout
{repo_layout}

## Common commands
{commands}

## Default behavior
For any non-trivial task, do not start coding immediately.

You must first:
1. understand the user's goal;
2. read `docs/SPEC_DRIVEN.md`;
3. if available, use the `spec-driven` skill;
4. guide the user to produce a good-enough specification;
5. wait for explicit approval of the specification;
6. create an implementation plan;
7. create a task checklist;
8. only then implement.

A task is non-trivial if it:
- changes behavior;
- affects architecture, data flow, APIs, UI, persistence, security, or dependencies;
- introduces a new feature;
- changes more than one responsibility;
- is ambiguous enough that assumptions would be risky.

For trivial tasks, you may proceed directly, but still state assumptions briefly before coding.

## Engineering principles
Prioritize code that is easy to understand, modify, test, and safely extend.

Use these principles unless the repository has a more specific local convention:

- Prefer simple, explicit designs over clever abstractions.
- Keep responsibilities cohesive and clearly owned.
- Separate I/O, domain rules, persistence, external integrations, and presentation/UI.
- Keep business/domain logic out of routes, CLI entrypoints, UI components, and provider adapters.
- Encapsulate external systems behind adapters or gateways.
- Avoid circular dependencies and hidden global state.
- Prefer functions, types, modules, and names that explain intent.
- Prefer boring, maintainable code over compressed or overly generic code.
- Follow existing project conventions before introducing new ones.
- Avoid speculative abstractions; create boundaries when they protect a real responsibility or external integration.

## Architectural locality
The goal is not to minimize the number of changed files at all costs.

The goal is to preserve an architecture where responsibilities are well isolated and future changes are naturally localized.

When implementing a change:
- change every file that legitimately needs to change;
- do not force a smaller diff by putting code in the wrong place;
- do not skip tests, docs, types, config, or schema updates just to reduce file count;
- if a simple conceptual change requires edits across many unrelated areas, call this out as a possible architecture smell;
- explain whether the scattering is expected or accidental;
- propose a refactor when it would improve future maintainability.

Good architecture makes related changes local. Bad architecture causes shotgun surgery.

## Simplicity bias
Prefer the simplest architecture that preserves clear boundaries.

Do not introduce frameworks, queues, background workers, ORMs, migrations, dependency injection containers, service layers, code generation, or distributed components unless the spec justifies them.

When adding structure, explain what responsibility it protects.

## Security and privacy
Treat credentials, tokens, private URLs, personal data, production data, customer data, and message histories as sensitive.

Rules:
- Never commit secrets, tokens, API keys, private keys, production credentials, database dumps, or personal data.
- Keep secrets in `.env` or in a deployment secret manager.
- Keep `.env` out of Git.
- Maintain `.env.example` with variable names only, never real values.
- Do not log secrets or sensitive payloads unless explicitly approved for a narrow debugging task.
- Validate external inputs at system boundaries.
- Prefer least privilege for tokens, credentials, and file permissions.
- Call out security or privacy impact in the plan whenever the change touches auth, credentials, network calls, files, logs, user data, or external APIs.

## Configuration policy
Configuration should be explicit but minimal.

Rules:
- Use `.env` only for secrets or environment-specific values that must not be committed.
- Use committed config files only for non-sensitive functional configuration.
- Keep config files compact; do not add options before they are needed.
- Prefer clear defaults in code for low-risk non-sensitive settings.
- Document required configuration in `.env.example`, README, or the relevant spec.

## Dependency policy
Do not add a new dependency without explaining:
- why the standard library or existing dependencies are insufficient;
- whether it is runtime, build-time, or dev-only;
- maintenance and security implications;
- how it affects build, deployment, tests, and lockfiles.

Prefer small, mature, well-maintained dependencies when a dependency is justified.

## Guided mode
When the user starts describing a feature, bugfix, refactor, or change request, enter guided mode.

In guided mode, you must:
- ask focused clarifying questions;
- reduce ambiguity instead of guessing;
- identify scope, constraints, edge cases, and done criteria;
- identify non-functional requirements such as maintainability, security, reliability, performance, and observability;
- draft a written spec before any implementation.

Do not dump too many questions at once.
Ask only the most useful next questions.

## Required workflow
For non-trivial work, follow this order:
1. Discovery
2. Specification
3. Spec approval
4. Technical plan
5. Task checklist
6. Implementation
7. Validation
8. Final summary

Prefer planning first for difficult tasks. In Codex, use plan mode or `/plan`. In Cursor, use Plan Mode before coding when the task is ambiguous or multi-step.

Do not skip steps unless the user explicitly asks to compress the process and the risk is low.
If risk is high or ambiguity remains, do not silently skip the process.

## Required artifacts
For non-trivial work, create a change folder under:
`docs/changes/<short-change-name>/`

Inside it, create:
- `spec.md`
- `plan.md`
- `tasks.md`

Optional when useful:
- `notes.md`
- `open_questions.md`
- `decisions.md`

Only create `plan.md` after `spec.md` is approved.
Only implement after `plan.md` and `tasks.md` exist.

## Spec approval rule
Before implementation, pause and explicitly ask the user to confirm the spec.
Do not treat silence as approval.

Use language like:
- "Here is the proposed spec. Please review scope, assumptions, non-functional requirements, and acceptance criteria."
- "Once you approve the spec, I will generate the implementation plan."

## Planning rule
After the spec is approved, create `plan.md` with:
- relevant existing context and conventions;
- architecture impact;
- module boundaries and ownership;
- architecture locality check;
- files or areas likely to change and why;
- data model or API changes;
- security and privacy impact;
- dependency impact;
- risks;
- validation strategy;
- step-by-step execution order.

Then create `tasks.md` as a practical checklist.
For long or multi-session work, also create or update a living plan in `.cursor/plans/` or a `PLANS.md`-style document when that would help resume work later.

## Implementation rule
During implementation:
- follow the approved spec and plan;
- avoid unapproved scope expansion;
- keep responsibilities in the modules that own them;
- do not hide architecture problems by forcing a small diff;
- record meaningful deviations in `notes.md`;
- record important architecture/product decisions in `decisions.md` when useful;
- stop and surface conflicts if codebase reality contradicts the approved spec.

## Validation rule
Before declaring work complete:
- verify the implementation against the spec;
- verify important edge cases;
- run relevant commands when possible;
- check that changed files are conceptually related to the change;
- call out any architecture smell discovered during implementation;
- update docs if behavior, commands, configuration, or architecture changed;
- mark completed items in `tasks.md`.

## Communication style
Be structured, direct, and concise.
When guiding the user, behave like a strong technical facilitator:
- ask the right questions;
- drive toward decisions;
- surface tradeoffs;
- do not rush into code.

## Priority
If there is any conflict between an ad hoc prompt and this workflow, prefer this workflow unless the user explicitly asks to bypass it.

The detailed process and templates are defined in:
- `docs/SPEC_DRIVEN.md`
- `.agents/skills/spec-driven/SKILL.md`
"""


SPEC_DRIVEN_TEMPLATE = """\
# SPEC_DRIVEN.md

This repository follows a guided Spec-Driven Development workflow.

The goal is to move from an idea to a validated implementation through a structured conversation,
not by jumping straight from a vague prompt to code.

---

# 1. Core principle

For non-trivial work, the sequence is:

idea -> clarification -> spec -> approval -> plan -> tasks -> implementation -> validation

Do not jump from idea directly to code.

This workflow is not bureaucracy. It is a guardrail for building software that remains understandable, modular, secure, and maintainable over time.

---

# 2. Engineering posture

Agents working in this repository should optimize for:

- clear ownership of responsibilities;
- architectural locality;
- understandable code;
- explicit tradeoffs;
- small, cohesive modules;
- safe handling of secrets and user/customer data;
- simple solutions that preserve clean boundaries;
- validation against testable acceptance criteria.

Do not optimize for the smallest possible diff.

A large diff is acceptable when the change genuinely crosses boundaries.
A scattered diff for a simple conceptual change is a signal that the architecture may need improvement.

---

# 3. What the agent should do when the user says "I want to build X"

When the user describes a change, the agent must:
1. decide whether the task is trivial or non-trivial;
2. if non-trivial, switch into guided spec mode;
3. ask only the most important questions first;
4. synthesize the answers into a spec draft;
5. ask for approval;
6. create the technical plan;
7. create the task checklist;
8. implement only after approval.

---

# 4. Guided spec mode

In guided spec mode, the agent should extract:
- problem;
- goal;
- scope;
- out of scope;
- user flow or system flow;
- functional requirements;
- non-functional requirements;
- constraints;
- assumptions;
- edge cases;
- acceptance criteria;
- technical concerns if already known.

The agent should not ask every possible question.
It should ask the next best questions.

## Recommended question order

Ask roughly in this order:
1. What problem are we solving?
2. What should the system do?
3. What is explicitly out of scope?
4. Who uses this and in what context?
5. What inputs, outputs, and state changes matter?
6. What reliability, security, maintainability, or performance concerns matter?
7. What edge cases or failure cases matter?
8. What would make this "done"?

If the user already answered some of these, do not repeat them.

---

# 5. Artifact creation

For each non-trivial change, create:

`docs/changes/<short-change-name>/spec.md`

After approval, create:
- `docs/changes/<short-change-name>/plan.md`
- `docs/changes/<short-change-name>/tasks.md`

Optional when useful:
- `docs/changes/<short-change-name>/notes.md`
- `docs/changes/<short-change-name>/open_questions.md`
- `docs/changes/<short-change-name>/decisions.md`

Use kebab-case for the folder name.

Examples:
- `docs/changes/add-auth-token-refresh/`
- `docs/changes/refactor-memory-store/`
- `docs/changes/fix-export-timezone-bug/`

---

# 6. Spec guidance

`spec.md` describes what should be true when the change is complete.
It should avoid premature implementation details unless they are real constraints.

A good spec answers:
- What are we changing?
- Why does it matter?
- What is included?
- What is excluded?
- What must work?
- What must not break?
- What non-functional requirements matter?
- What assumptions are we making?
- How will we know it is done?

---

# 7. spec.md template

```md
# Change Spec: <title>

## 1. Summary
A short description of the change.

## 2. Problem
What is wrong, missing, or needed?

## 3. Goal
What outcome do we want?

## 4. Scope
What is included in this change?

## 5. Out of Scope
What is explicitly not included?

## 6. Users / Actors
Who uses this and in what context?

## 7. Functional Requirements
List the expected behaviors.

## 8. Non-Functional Requirements
Document quality attributes that matter for this change.

### Maintainability

### Modularity / Architecture

### Security / Privacy

### Reliability

### Performance

### Observability

### Simplicity

## 9. User Flow / System Flow
Describe the main flow step by step.

## 10. Edge Cases
List important edge cases, invalid states, and error conditions.

## 11. Constraints
Technical, product, UX, data, compatibility, or time constraints.

## 12. Assumptions
Important assumptions currently being made.

## 13. Acceptance Criteria
Concrete statements that define when the work is done.

## 14. Open Questions
Anything still unresolved.
```

---

# 8. When is a spec "good enough"?

A spec is good enough when:
- the goal is clear;
- the scope is bounded;
- the main flow is defined;
- important non-functional requirements are explicit;
- major edge cases are acknowledged;
- acceptance criteria are testable;
- important assumptions are explicit.

The spec does not need to be perfect.
It must be good enough to avoid reckless implementation.

If important ambiguity remains, the agent should say so clearly.

---

# 9. Plan guidance

`plan.md` describes how the approved spec will be implemented.

Before planning implementation, the agent must inspect existing conventions:
- folder structure;
- naming style;
- error handling;
- logging;
- configuration;
- dependency patterns;
- tests;
- external integration patterns;
- persistence/data access patterns.

The plan should preserve existing conventions unless there is a clear reason to change them.

---

# 10. plan.md template

```md
# Implementation Plan: <title>

## 1. Summary
Short description of implementation intent.

## 2. Relevant Existing Context
Relevant files, modules, architecture, or patterns.

## 3. Existing Conventions Found
- Folder structure:
- Naming style:
- Error handling:
- Logging:
- Testing pattern:
- Config pattern:
- External integration pattern:
- Persistence/data access pattern:

## 4. Proposed Changes
What will be added, changed, removed, or refactored?

## 5. Module Boundaries
- What module owns this responsibility?
- What module must not know about this change?
- What interface or adapter boundary should be preserved?
- What should remain decoupled?

## 6. Architecture Locality Check
- Which files are expected to change, and why?
- Are the affected files all part of the same conceptual area?
- Does this change require edits across unrelated areas?
- If yes, is that expected or a sign of weak boundaries?
- Should we refactor before, during, or after this change?

## 7. Data / API / Interface Impact
Any persistence, schema, API, event, or interface changes.

## 8. Security / Privacy Impact
- Does this touch credentials, tokens, secrets, user data, logs, permissions, network calls, files, or external APIs?
- Are secrets kept out of Git?
- Are logs free of sensitive data?
- Are external inputs validated?

## 9. Dependency Impact
- Are new dependencies needed?
- Why are existing tools insufficient?
- Is the dependency runtime, build-time, or dev-only?
- What are the maintenance/security implications?

## 10. Risks
Technical or execution risks.

## 11. Validation Strategy
How this will be verified.

## 12. Execution Steps
Ordered implementation steps.

## 13. Rollback / Recovery
How to revert or limit damage if needed.

## 14. Notes
Anything important for implementation.
```

---

# 11. tasks.md template

```md
# Tasks: <title>

- [ ] Re-read approved spec and plan
- [ ] Inspect relevant code paths and conventions
- [ ] Confirm module ownership and boundaries
- [ ] Implement the first cohesive change
- [ ] Implement the second cohesive change
- [ ] Implement the third cohesive change
- [ ] Add or update tests
- [ ] Validate acceptance criteria
- [ ] Check whether changed files are conceptually related
- [ ] Document architecture smell if the change is unexpectedly scattered
- [ ] Update docs if behavior, config, commands, or architecture changed
- [ ] Summarize final result
```

The checklist must be rewritten to match the actual change.
Tasks should be concrete, ordered, and independently checkable.

Avoid generic tasks like:
- "implement backend"
- "update frontend"
- "fix bug"

Prefer tasks like:
- "add repository function to upsert messages by provider_message_id"
- "add test proving duplicate sync does not duplicate messages"
- "update product parser to accept SKU prefix"

---

# 12. decisions.md guidance

Use `decisions.md` when the change includes meaningful product, architecture, dependency, persistence, integration, or security decisions.

Example:

```md
# Decisions: <title>

## Decision 1: <decision name>

### Context
Why did this decision come up?

### Decision
What did we decide?

### Consequences
What becomes easier, harder, constrained, or intentionally excluded?
```

---

# 13. Agent behavior during implementation

During implementation, the agent must:
- stick to the approved spec;
- avoid hidden scope expansion;
- document meaningful deviations;
- stop and surface conflicts if codebase reality contradicts the spec;
- prefer clear, maintainable changes over clever shortcuts;
- preserve module ownership;
- avoid pushing business rules into integration, UI, or persistence layers unless that is already the established project pattern.

If implementation reveals that the spec is insufficient, the agent should return to clarification mode instead of pushing ahead blindly.

---

# 14. Final validation checklist

Before completion, the agent should validate:
- does the implementation satisfy the functional requirements?
- do the acceptance criteria hold?
- were relevant edge cases addressed?
- are non-functional requirements still respected?
- are tests sufficient for the risk level?
- were docs/spec/tasks updated?
- were relevant commands run?
- were secrets and sensitive data kept out of code, logs, and docs?
- are changed files conceptually related to the change?
- was any architecture smell found and documented?

Then provide a final summary with:
- what changed;
- files affected;
- tests run;
- assumptions or limitations remaining;
- any architecture concerns discovered.

---

# 15. Definition of Done

A change is done only when:

- [ ] Public behavior matches the approved spec
- [ ] Acceptance criteria are satisfied
- [ ] Code follows existing conventions
- [ ] Module boundaries remain clear
- [ ] Related changes are placed in the modules that own them
- [ ] No unrelated behavior was changed without approval
- [ ] No secrets or sensitive data were committed
- [ ] Relevant tests were added or updated
- [ ] Relevant validation commands were run, or the reason they were not run is documented
- [ ] Documentation was updated if behavior, config, commands, or architecture changed
- [ ] Known limitations are documented

---

# 16. Plan mode guidance

For ambiguous or multi-step work:
- prefer plan mode before coding;
- ask clarifying questions first;
- produce a reviewable plan;
- only implement after the plan is accepted.

In Cursor, save useful plans to `.cursor/plans/` so future sessions can resume from them.
For longer-running or multi-session work, consider keeping a living `PLANS.md`-style document.

---

# 17. Default conversation pattern

When a user starts a non-trivial request, the agent should roughly follow this pattern:
1. Restate the goal briefly.
2. Ask 2-5 focused questions.
3. Draft `spec.md`.
4. Ask for review and approval.
5. Draft `plan.md`.
6. Draft `tasks.md`.
7. Implement.
8. Validate and summarize.

---

# 18. Example approval language

Use phrases like:
- "I drafted the spec. Please review the scope, assumptions, non-functional requirements, and acceptance criteria."
- "If this spec looks right, I will generate the implementation plan next."
- "I found an ambiguity that should be resolved before implementation."
- "The approved spec and codebase reality conflict here; we should decide before continuing."

---

# 19. Override rules

The user may explicitly ask to skip or compress the process.
If so:
- comply when risk is low;
- still state assumptions;
- still prefer a minimal written spec for any behavior-changing task.

For risky or ambiguous tasks, do not silently skip the process.
"""


START_PROMPT_TEMPLATE = """\
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
"""


SPEC_TEMPLATE = """\
# Change Spec: <title>

## 1. Summary

## 2. Problem

## 3. Goal

## 4. Scope

## 5. Out of Scope

## 6. Users / Actors

## 7. Functional Requirements

## 8. Non-Functional Requirements

### Maintainability

### Modularity / Architecture

### Security / Privacy

### Reliability

### Performance

### Observability

### Simplicity

## 9. User Flow / System Flow

## 10. Edge Cases

## 11. Constraints

## 12. Assumptions

## 13. Acceptance Criteria

## 14. Open Questions
"""


PLAN_TEMPLATE = """\
# Implementation Plan: <title>

## 1. Summary

## 2. Relevant Existing Context

## 3. Existing Conventions Found

- Folder structure:
- Naming style:
- Error handling:
- Logging:
- Testing pattern:
- Config pattern:
- External integration pattern:
- Persistence/data access pattern:

## 4. Proposed Changes

## 5. Module Boundaries

- What module owns this responsibility?
- What module must not know about this change?
- What interface or adapter boundary should be preserved?
- What should remain decoupled?

## 6. Architecture Locality Check

- Which files are expected to change, and why?
- Are the affected files all part of the same conceptual area?
- Does this change require edits across unrelated areas?
- If yes, is that expected or a sign of weak boundaries?
- Should we refactor before, during, or after this change?

## 7. Data / API / Interface Impact

## 8. Security / Privacy Impact

- Does this touch credentials, tokens, secrets, user data, logs, permissions, network calls, files, or external APIs?
- Are secrets kept out of Git?
- Are logs free of sensitive data?
- Are external inputs validated?

## 9. Dependency Impact

- Are new dependencies needed?
- Why are existing tools insufficient?
- Is the dependency runtime, build-time, or dev-only?
- What are the maintenance/security implications?

## 10. Risks

## 11. Validation Strategy

## 12. Execution Steps

## 13. Rollback / Recovery

## 14. Notes
"""


TASKS_TEMPLATE = """\
# Tasks: <title>

- [ ] Re-read approved spec and plan
- [ ] Inspect relevant code paths and conventions
- [ ] Confirm module ownership and boundaries
- [ ] Replace these generic items with concrete, ordered, checkable tasks
- [ ] Add or update tests
- [ ] Validate acceptance criteria
- [ ] Check whether changed files are conceptually related
- [ ] Document architecture smell if the change is unexpectedly scattered
- [ ] Update docs if behavior, config, commands, or architecture changed
- [ ] Summarize final result
"""


NOTES_TEMPLATE = """\
# Notes: <title>

Use this file to capture deviations, discoveries, implementation notes, and codebase facts that matter later.
"""


OPEN_QUESTIONS_TEMPLATE = """\
# Open Questions: <title>

- [ ] Question 1
- [ ] Question 2
"""


DECISIONS_TEMPLATE = """\
# Decisions: <title>

Use this file for meaningful product, architecture, dependency, persistence, integration, or security decisions.

## Decision 1: <decision name>

### Context

Why did this decision come up?

### Decision

What did we decide?

### Consequences

What becomes easier, harder, constrained, or intentionally excluded?
"""


SKILL_TEMPLATE = """\
---
name: spec-driven
description: Use for non-trivial feature work, bug fixes, refactors, or ambiguous tasks. Guides the user through clarification -> spec -> approval -> plan -> tasks -> implementation -> validation, with emphasis on architectural locality, maintainability, security, and clear module ownership.
---

1. Read `AGENTS.md` and `docs/SPEC_DRIVEN.md`.
2. Decide whether the request is trivial or non-trivial.
3. For non-trivial work, do not code immediately.
4. Ask a small number of focused clarifying questions.
5. Draft `docs/changes/<short-change-name>/spec.md` using the repo template.
6. Include functional and non-functional requirements.
7. Ask the user to approve the spec explicitly.
8. Only after approval, create `plan.md` and `tasks.md`.
9. In `plan.md`, include existing conventions, module boundaries, architecture locality, security/privacy impact, dependency impact, risks, and validation.
10. Implement according to the approved spec and plan.
11. Do not force a smaller diff by putting code in the wrong place.
12. If a simple conceptual change touches many unrelated areas, call it out as a possible architecture smell.
13. Validate the result against the acceptance criteria and definition of done.
14. Summarize the final result, tests, remaining assumptions, and any architecture concerns.

When the request is large, ambiguous, or likely to span multiple sessions:
- prefer plan mode before coding;
- keep the plan detailed and reviewable;
- if using Cursor, save the plan to `.cursor/plans/` when that would help future sessions.
"""


CURSOR_RULE_TEMPLATE = """\
---
description: Guided Spec-Driven Development workflow for non-trivial changes
alwaysApply: true
---

- Read `AGENTS.md` and `docs/SPEC_DRIVEN.md` before non-trivial work.
- Prefer Plan Mode first for ambiguous or multi-step tasks.
- Do not implement a non-trivial change before drafting and getting approval for `docs/changes/<short-change-name>/spec.md`.
- Include non-functional requirements in specs: maintainability, modularity, security, reliability, performance, observability, and simplicity.
- After spec approval, create `plan.md` and `tasks.md` before implementation.
- In plans, document existing conventions, module boundaries, architecture locality, security/privacy impact, dependency impact, risks, and validation strategy.
- Keep changes scoped to the approved spec.
- Do not optimize for fewer changed files at the expense of architecture.
- Preserve clear ownership and cohesive modules.
- If a simple conceptual change touches many unrelated areas, call it out as a possible architecture smell.
- Validate the final result against acceptance criteria, relevant tests, and the definition of done.
- Save useful long-form plans to `.cursor/plans/` when that will help future sessions.
"""


CURSOR_PLANS_README = """\
# Cursor plans

Store saved plan-mode documents here when they are useful to resume a feature later.

Recommended naming:
- `2026-04-09-add-auth-refresh.md`
- `2026-04-09-refactor-memory-store.md`

A saved plan should include:
- approved scope;
- module boundaries;
- architecture locality concerns;
- ordered execution steps;
- validation strategy;
- unresolved questions.
"""


GLOBAL_CODEX_TEMPLATE = """\
# ~/.codex/AGENTS.md

## Global working agreement
- Prefer the repository's local `AGENTS.md` whenever present.
- For non-trivial tasks, do not code immediately; first look for project workflow docs.
- If the repository contains `docs/SPEC_DRIVEN.md`, follow that process.
- Prefer plan mode first for ambiguous or multi-step tasks.
- State assumptions before coding if the request is ambiguous.
- Prefer clear module ownership and architectural locality.
- Do not optimize for fewer changed files at the expense of maintainability.
- Keep secrets out of code, logs, and committed files.
"""


def backup_path(path: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return path.with_suffix(path.suffix + f".bak-{timestamp}")


def write_text_file(
    path: Path,
    content: str,
    *,
    force: bool,
    dry_run: bool,
    backup_existing: bool,
) -> WriteResult:
    normalized = dedent(content).rstrip() + "\n"
    if path.exists():
        existing = read_text_if_exists(path)
        if existing == normalized:
            return WriteResult(path, "unchanged", "already up to date")
        if not force:
            return WriteResult(path, "skipped", "exists; use --force to overwrite")
        if backup_existing and not dry_run:
            backup = backup_path(path)
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup)
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(normalized, encoding="utf-8")
    return WriteResult(path, "written", "created/updated")


def ensure_dir(path: Path, *, dry_run: bool) -> WriteResult:
    if path.exists():
        return WriteResult(path, "unchanged", "directory already exists")
    if not dry_run:
        path.mkdir(parents=True, exist_ok=True)
    return WriteResult(path, "written", "directory created")


def bootstrap_repo(
    target: Path,
    *,
    profile: RepoProfile,
    force: bool,
    dry_run: bool,
    install_global_codex: bool,
    backup_existing: bool,
    with_cursor: bool,
    with_skill: bool,
) -> list[WriteResult]:
    results: list[WriteResult] = []

    docs_dir = target / "docs"
    changes_dir = docs_dir / "changes"
    templates_dir = changes_dir / "_templates"
    cursor_rules_dir = target / ".cursor" / "rules"
    cursor_plans_dir = target / ".cursor" / "plans"
    skill_dir = target / ".agents" / "skills" / "spec-driven"

    for directory in (docs_dir, changes_dir, templates_dir):
        results.append(ensure_dir(directory, dry_run=dry_run))
    if with_cursor:
        results.append(ensure_dir(cursor_rules_dir, dry_run=dry_run))
        results.append(ensure_dir(cursor_plans_dir, dry_run=dry_run))
    if with_skill:
        results.append(ensure_dir(skill_dir, dry_run=dry_run))

    files: dict[Path, str] = {
        target / "AGENTS.md": AGENTS_TEMPLATE.format(
            project_name=profile.project_name,
            repo_name=profile.repo_name,
            detected_stacks=format_detected_stack(profile),
            repo_layout=format_repo_layout(profile),
            commands=format_commands(profile),
        ),
        docs_dir / "SPEC_DRIVEN.md": SPEC_DRIVEN_TEMPLATE,
        docs_dir / "START_PROMPT.md": START_PROMPT_TEMPLATE,
        templates_dir / "spec.md": SPEC_TEMPLATE,
        templates_dir / "plan.md": PLAN_TEMPLATE,
        templates_dir / "tasks.md": TASKS_TEMPLATE,
        templates_dir / "notes.md": NOTES_TEMPLATE,
        templates_dir / "open_questions.md": OPEN_QUESTIONS_TEMPLATE,
        templates_dir / "decisions.md": DECISIONS_TEMPLATE,
    }

    if with_skill:
        files[skill_dir / "SKILL.md"] = SKILL_TEMPLATE

    if with_cursor:
        files[cursor_rules_dir / "spec-driven-always.mdc"] = CURSOR_RULE_TEMPLATE
        files[cursor_plans_dir / "README.md"] = CURSOR_PLANS_README

    for path, content in files.items():
        results.append(
            write_text_file(
                path,
                content,
                force=force,
                dry_run=dry_run,
                backup_existing=backup_existing,
            )
        )

    if install_global_codex:
        global_agents = Path.home() / ".codex" / "AGENTS.md"
        results.append(
            write_text_file(
                global_agents,
                GLOBAL_CODEX_TEMPLATE,
                force=force,
                dry_run=dry_run,
                backup_existing=backup_existing,
            )
        )

    return results


def print_summary(results: list[WriteResult], *, target: Path, profile: RepoProfile) -> None:
    print(f"\nBootstrapped repository: {target.resolve()}\n")
    if profile.detected_stacks:
        print(f"Detected stack(s): {', '.join(profile.detected_stacks)}")
    if profile.package_manager:
        print(f"Detected package manager: {profile.package_manager}")
    if profile.top_dirs:
        print(f"Top directories: {', '.join(profile.top_dirs)}")
    if profile.commands:
        print("Suggested commands:")
        for key in ("build", "test", "lint", "typecheck", "fmt", "check", "dev"):
            if key in profile.commands:
                print(f"- {key:10} {profile.commands[key]}")

    width = max(len(str(result.path)) for result in results) if results else 10
    print("\nFiles and directories:")
    for result in results:
        rel = str(result.path)
        print(f"- {rel.ljust(width)}  {result.status:9}  {result.message}")

    print("\nNext steps:")
    print("1. Open the repository in Codex or Cursor.")
    print("2. Read or paste the prompt from docs/START_PROMPT.md.")
    print("3. Describe the feature you want to build.")
    print("4. Approve the generated spec before letting the agent implement.")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap a repository for guided Spec-Driven Development.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Target repository directory. Defaults to the current directory.",
    )
    parser.add_argument(
        "--project-name",
        help="Optional project name written into AGENTS.md. Defaults to the folder name.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files. Existing files are backed up unless --no-backup is used.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created or overwritten without writing files.",
    )
    parser.add_argument(
        "--global-codex",
        action="store_true",
        help="Also create or update ~/.codex/AGENTS.md with a small global default.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create backup files when overwriting with --force.",
    )
    parser.add_argument(
        "--no-cursor",
        action="store_true",
        help="Do not create Cursor-specific files under .cursor/.",
    )
    parser.add_argument(
        "--no-skill",
        action="store_true",
        help="Do not create the Codex skill under .agents/skills/spec-driven/.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    target = Path(args.path).expanduser()

    if target.exists() and not target.is_dir():
        print(f"Error: target path is not a directory: {target}", file=sys.stderr)
        return 2

    if not target.exists() and not args.dry_run:
        target.mkdir(parents=True, exist_ok=True)

    project_name = detect_project_name(target, args.project_name)
    profile = detect_repo_profile(target, project_name)
    results = bootstrap_repo(
        target,
        profile=profile,
        force=args.force,
        dry_run=args.dry_run,
        install_global_codex=args.global_codex,
        backup_existing=not args.no_backup,
        with_cursor=not args.no_cursor,
        with_skill=not args.no_skill,
    )
    print_summary(results, target=target, profile=profile)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
