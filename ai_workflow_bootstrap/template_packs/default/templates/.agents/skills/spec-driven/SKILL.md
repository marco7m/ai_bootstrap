---
name: spec-driven
description: Guide non-trivial features, bug fixes, refactors and ambiguous changes through clarification, spec approval, plan and tasks approval, implementation and validation. Use whenever behavior, architecture, persistence, interfaces, security, dependencies or multiple responsibilities may change.
---

1. Read repository instructions and inspect the smallest relevant code/doc set.
2. Before drafting the spec, run a proportional maintainability audit when code or knowledge-health triggers are present. Record evidence and route related requirements versus separate-spec or advisory findings.
3. Clarify the problem, outcome, scope, exclusions, constraints, edge cases and acceptance criteria.
4. Create `docs/changes/<change>/spec.md` from `docs/changes/_templates/spec.md`.
5. Identify affected product, architecture and capability owners without duplicating their facts.
6. Pause for explicit spec approval. Do not create plan/tasks before approval.
7. After approval, record the approved target and active change without replacing current capability state.
8. Reconcile audit findings with established boundaries; create `plan.md` and concrete `tasks.md`. A material post-approval scope change needs explicit reconciliation; unrelated debt needs a separate spec.
9. Include architecture locality, security/privacy, dependencies, risks, validation and living-knowledge impact.
10. Pause for explicit approval of both plan and tasks. Spec approval is not implementation approval.
11. Implement the approved plan, recording meaningful deviations and stopping on unresolved spec/repository conflicts.
12. Validate acceptance criteria with contract-level tests and relevant checks.
13. After implementation, re-audit the diff and affected knowledge owners; distill durable facts, fill closeout disposition, validate links and update current evidence only when supported.
14. Summarize behavior, files, validation, knowledge updates, accepted findings, limitations and architecture concerns.

Open `docs/SPEC_DRIVEN.md` only when detailed workflow guidance is needed.
