# AGENTS.md

Project: $project_name

Repository: $repo_name

Detected stack: $detected_stacks

## Start here

- Follow repository-local instructions and existing conventions.
- When `docs/INDEX.md` exists, start there and read only the product,
  architecture, capability or decision pages relevant to the task.
- Use the `spec-driven` skill for non-trivial changes. Open
  `docs/SPEC_DRIVEN.md` only when detailed workflow guidance is needed.
- Use `maintainability-audit` when ownership is unclear, tests are brittle or a
  small conceptual change is scattered across unrelated files.
- Use `living-docs` when orienting in the project or changing durable project
  knowledge.

## Project-owned instructions

- Read `AGENTS.project.md` when it exists.
- Create it only when a concrete repository-specific working instruction needs
  a durable owner. Put such instructions there instead of editing this managed
  file.
- Keep it concise, link detailed facts to their living-document owners, and
  never store secrets, private messages or sensitive production/customer data.

$stack_agent_instructions

## Required workflow

A task is non-trivial when it changes behavior, architecture, persistence,
interfaces, security, dependencies or multiple responsibilities, or when
guessing would be risky.

For non-trivial work:

1. Inspect the relevant repository state and clarify the request.
2. Create `docs/changes/<change>/spec.md` from the repository template.
3. Pause for explicit spec approval.
4. Only then create `plan.md` and `tasks.md`.
5. Pause for explicit approval of both plan and tasks.
6. Implement, validate against the approved spec and close the checklist.

The approved spec, plan and tasks are the handoff contract. Do not treat an
earlier approval or silence as approval of a later gate. A user may explicitly
request a compressed workflow when risk is low.

## Knowledge contract

- Product docs own expected behavior; architecture docs own how the system is
  built and operates.
- Keep current implementation separate from approved future behavior.
- `docs/CAPABILITIES.md` owns current state, evidence, approved target and
  active change. Never replace a verified current state with a future target.
- One durable fact has one owner. Link to it instead of copying prose.
- Change artifacts are temporal history. At closeout, distill durable facts
  into their owners and validate relative links.
- A `scaffold` or `incomplete` knowledge base is not proof of complete product
  intent. Surface conflicts between docs and code/tests/runtime before deciding
  which side is stale.
- Bootstrap reapplication is infrastructure maintenance, not documentation
  closeout. A seeded living-doc scaffold becomes project knowledge once reviewed
  or edited and must not be replaced by a template during ordinary upgrades.
- If an owner looks regenerated, truncated or downgraded, inspect
  `.ai-bootstrap/state.json` and relevant Git/evidence before trusting it.
  Restore the established knowledge boundary before a narrow change closeout.

## Engineering guardrails

- Preserve cohesive ownership and keep domain rules out of UI, transport,
  persistence and provider adapters unless that is the established boundary.
- Prefer simple local changes. Call out shotgun surgery, mixed responsibilities,
  hidden global state, repeated logic and tests coupled to private details.
- Tests should protect acceptance criteria, public behavior and invariants.
- Do not add dependencies without explaining why existing tools are
  insufficient and assessing maintenance and security impact.
- Never commit secrets, credentials, private messages, production/customer data
  or sensitive payloads. Validate external input at system boundaries.
- Do not change unrelated behavior, stage files, commit or perform destructive
  Git operations unless the user explicitly requested them.

## Repository context

Layout:

$repo_layout

Commands:

$commands
