---
name: spec-driven
description: Guide non-trivial features, bug fixes, refactors and ambiguous changes through clarification, spec approval, plan and tasks approval, implementation and validation. Use whenever behavior, architecture, persistence, interfaces, security, dependencies or multiple responsibilities may change.
---

1. Read repository instructions and inspect the smallest relevant code/doc set.
2. Clarify the problem, outcome, scope, exclusions, constraints, edge cases and acceptance criteria.
3. Create `docs/changes/<change>/spec.md` from `docs/changes/_templates/spec.md`.
4. Identify affected product, architecture and capability owners without duplicating their facts.
5. Pause for explicit spec approval. Do not create plan/tasks before approval.
6. After approval, record the approved target and active change without replacing current capability state.
7. Inspect established boundaries and conventions; create `plan.md` and concrete `tasks.md` from their templates.
8. Include architecture locality, security/privacy, dependencies, risks, validation and living-knowledge impact.
9. Pause for explicit approval of both plan and tasks. Spec approval is not implementation approval.
10. Implement the approved plan, recording meaningful deviations and stopping on unresolved spec/repository conflicts.
11. Validate acceptance criteria with contract-level tests and relevant checks.
12. Update current state/evidence only when supported; distill durable facts, validate links and close tasks.
13. Summarize behavior, files, validation, knowledge updates, limitations and architecture concerns.

Open `docs/SPEC_DRIVEN.md` only when detailed workflow guidance is needed.
