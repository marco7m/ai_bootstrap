# Change Spec: Approval gate for plan and tasks

## 1. Summary

Extend the default spec-driven workflow with a second explicit approval gate after `plan.md` and `tasks.md` are drafted and before implementation begins.

## 2. Problem

The current workflow pauses for approval after the spec but allows implementation to begin immediately after planning. That prevents the user from reviewing the proposed technical approach and execution checklist as a separate decision, and makes it less natural to hand off the spec, planning, and implementation phases to different AI models.

## 3. Goal

Make the plan and tasks a reviewable, approved implementation contract. The workflow must support a user choosing a different assistant or model for any phase by relying on the persisted change artifacts rather than conversational continuity.

## 4. Scope

- Change the documented non-trivial workflow to: clarification → spec → spec approval → plan → tasks → plan/tasks approval → implementation → validation.
- Require agents to pause and request explicit approval after both `plan.md` and `tasks.md` exist.
- State that another assistant or model may continue at any stage by reading the approved artifacts and relevant repository context.
- Update the bootstrap's generated workflow templates and this repository's corresponding workflow documentation and skill.
- Update the start prompts and README workflow summary where they describe the sequence.

## 5. Out of Scope

- Tracking which model produced or approved each artifact.
- Adding a configuration option to disable the second approval gate.
- Changing the CLI, TUI, state-file schema, or generated project layout.
- Requiring approval for trivial changes or when the user explicitly authorizes bypassing the workflow.

## 6. Users / Actors

- Project owners reviewing both desired behavior and implementation approach.
- AI assistants or models drafting the spec, plan/tasks, or implementation in separate sessions.

## 7. Functional Requirements

- For non-trivial work, agents must not implement after spec approval alone.
- After spec approval, agents must create both `plan.md` and `tasks.md`, summarize their approach, and explicitly request approval of the plan/tasks.
- Implementation may start only after explicit plan/tasks approval.
- The workflow docs must tell a new assistant/model to read the approved `spec.md`, `plan.md`, and `tasks.md` before continuing, and to resolve conflicts rather than assuming prior conversational context.
- The workflow must continue to permit the user to explicitly bypass or compress the process when appropriate.
- Generated templates and the bootstrap repository's own workflow instructions must express the same sequence.

## 8. Non-Functional Requirements

### Maintainability

Keep the workflow wording concise and avoid duplicating detailed explanations that can drift across documents.

### Modularity / Architecture

This is a documentation and instruction-policy change. Template files remain the source for generated instructions; no engine behavior is added.

### Security / Privacy

No model names, prompts, private conversations, or user content are stored as workflow state.

### Reliability

Approval must be explicit; silence and the prior spec approval must not count as approval of the plan/tasks.

### Performance

No runtime or dependency impact.

### Observability

The persisted change artifacts make phase handoffs reviewable across sessions and models.

### Simplicity

Use one additional approval checkpoint, not model-specific metadata or tooling.

## 9. User Flow / System Flow

1. An assistant clarifies the request and drafts `spec.md`.
2. The user approves the spec.
3. Any assistant/model drafts `plan.md` and `tasks.md` from the approved spec and repository context.
4. The user reviews and approves the plan/tasks, or asks for revisions.
5. The same or another assistant/model implements from the approved artifacts and validates the result.

## 10. Edge Cases

- If implementation reveals a conflict with the approved plan, the agent stops and asks for direction or updates the relevant artifact for review.
- If only the plan or only the tasks exist, implementation remains blocked.
- A user may explicitly say to implement without the second review; agents follow that explicit instruction while noting the compressed process when useful.
- A new model must not treat an old conversational approval as sufficient if the current plan/tasks have changed since that approval.

## 11. Constraints

- Preserve the existing spec approval gate.
- Keep the change documentation-only: do not modify bootstrap execution code.
- Keep generated and source workflow instructions aligned.

## 12. Assumptions

- Users who want a faster path can explicitly authorize skipping the plan/tasks review.
- Artifact-based handoff is enough; recording model identity would add complexity without improving the workflow contract.

## 13. Acceptance Criteria

- The generated `AGENTS.md`, generated `docs/SPEC_DRIVEN.md`, generated spec-driven skill, and generated start prompt require explicit plan/tasks approval before implementation.
- This repository's matching workflow docs and skill state the same rule.
- The instructions explicitly support changing AI/model between spec, planning, and implementation through artifact review.
- README workflow text reflects the new sequence.
- No Python runtime behavior or generated-file selection changes.

## 14. Open Questions

None.
