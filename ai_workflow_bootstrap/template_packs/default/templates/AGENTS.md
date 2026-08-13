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
- Use `maintainability-audit` for code or living-knowledge maintainability when
  ownership is unclear, files are large, tests are brittle, documentation is
  concentrated or a small conceptual change is scattered.
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

## Long-running commands

- Before choosing a terminal wait cadence, classify the process as finite and
  non-interactive or as interactive, persistent or input-sensitive.
- For finite and non-interactive commands that may take time, use the longest
  supported wait, targeting up to `300000 ms`. If the process is still running,
  use another long wait. Do not poll at short intervals or create model rounds
  solely to check completion.
- Use responsive polling for servers, TUIs, debuggers and programs that require
  input or prompt observation.

## Required workflow

Before creating artifacts, locate the best existing authority and reason about
behavioral novelty separately from execution risk. State the classification
briefly when it changes artifacts, approvals, scope or material validation.

Using `spec-driven` does not automatically require a new spec. Create or
reconcile `docs/changes/<change>/spec.md` when behavior is new, the contract is
ambiguous or authorities conflict, then pause for explicit spec approval.

Every non-trivial implementation requires proportional `plan.md` and
`tasks.md` plus explicit approval of both plan and tasks before coding,
including a repair that only restores an existing contract. A standalone
no-spec repair uses `docs/changes/<repair>/plan.md` and `tasks.md`; the plan
links the authority and declares no behavioral novelty. If a new decision
appears, stop and create or reconcile a spec.

Only work that is genuinely trivial, unequivocal and low risk may use a direct
or compressed flow. Read-only diagnosis never implies permission to implement.
See `docs/SPEC_DRIVEN.md` for routes, artifact roles and validation guidance.

## Knowledge contract

- Product docs own expected behavior; architecture docs own how the system is
  built and operates.
- Keep current implementation separate from approved future behavior.
- `docs/CAPABILITIES.md` owns current state, evidence, approved target and
  active change. Never replace a verified current state with a future target.
- One durable fact has one owner. Link to it instead of copying prose.
- Change artifacts are temporal history. At closeout, distill durable facts
  into their owners and validate relative links.
- At closeout run the aggregate living-doc check for the active change; only
  `updated` or justified `no-update-needed` is a closed disposition.
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
