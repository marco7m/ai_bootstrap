# AGENTS.md

This repository uses a guided Spec-Driven Development workflow by default.

## Project identity
- Project name: $project_name
- Repository root: $repo_name
- Detected stack(s): $detected_stacks

## Repository layout
$repo_layout

## Common commands
$commands

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

## Testing policy
Tests should protect the contract defined by the spec and plan.

Prefer a small number of high-signal tests that cover:
- acceptance criteria;
- public behavior and invariants;
- regression cases that would break the contract.

Avoid adding tests that only freeze implementation detail, internal call order, incidental text, or other behavior that the spec does not require.
If no new test is justified, say so in the validation notes instead of adding a fragile test for coverage alone.

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
