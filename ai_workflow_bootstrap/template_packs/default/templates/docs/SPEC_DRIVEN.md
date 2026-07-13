# SPEC_DRIVEN.md

This repository follows a guided Spec-Driven Development workflow.

The goal is to move from an idea to a validated implementation through a structured conversation,
not by jumping straight from a vague prompt to code.

---

# 1. Core principle

For non-trivial work, the sequence is:

idea -> clarification -> spec -> spec approval -> plan -> tasks -> plan/tasks approval -> implementation -> validation

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

When drafting a spec, also assess maintainability impact:
- Does this change make future changes easier or harder?
- What architecture is being touched?
- Where could entropy increase?
- Is a small local refactor needed before coding?
- Is the right response a separate refactor spec?

---

# 3. What the agent should do when the user says "I want to build X"

When the user describes a change, the agent must:
1. decide whether the task is trivial or non-trivial;
2. if non-trivial, switch into guided spec mode;
3. ask only the most important questions first;
4. synthesize the answers into a spec draft;
5. ask for approval of the spec;
6. create the technical plan;
7. create the task checklist;
8. ask for explicit approval of both the plan and tasks;
9. implement only after plan/tasks approval.

The approved `spec.md`, `plan.md`, and `tasks.md` are the handoff contract. A different assistant or model may continue any later phase by reading those artifacts and the current repository context.

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

After spec approval, create:
- `docs/changes/<short-change-name>/plan.md`
- `docs/changes/<short-change-name>/tasks.md`

Then pause and request explicit approval of both files before implementation. Spec approval alone is not approval of the implementation approach.

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

## 9. Maintainability Impact
- Does this change make future changes easier or harder?
- Touched architecture:
- Potential entropy:
- Refactor needed before coding:
- Refactor scope:

### Modularity / Architecture

### Security / Privacy

### Reliability

### Performance

### Observability

### Simplicity

## 10. User Flow / System Flow
Describe the main flow step by step.

## 11. Edge Cases
List important edge cases, invalid states, and error conditions.

## 12. Constraints
Technical, product, UX, data, compatibility, or time constraints.

## 13. Assumptions
Important assumptions currently being made.

## 14. Acceptance Criteria
Concrete statements that define when the work is done.

## 15. Open Questions
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

## 6. Architecture Locality
- Primary module or owner:
- Files expected to change:
- Files that should not be touched:
- New boundaries introduced:
- Existing boundaries preserved:
- Why this is the smallest maintainable change:
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

Include only the tests that actually protect the approved spec. If a test would mainly lock down implementation detail, leave it out and explain why.

## 11.1 Test Strategy
- Contract to protect:
- Tests to add or update:
- Tests intentionally not added:
- Why these tests should survive internal refactors:

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
- are tests sufficient for the risk level without freezing implementation details?
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

For longer-running or multi-session work, consider keeping a living project-local planning document.

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
