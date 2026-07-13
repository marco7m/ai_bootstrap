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
7. Keep tests focused on contract-level behavior from the spec and plan, not implementation details.
8. Ask the user to approve the spec explicitly.
9. Only after approval, create `plan.md` and `tasks.md`.
10. Ask the user to approve both the plan and tasks explicitly before implementation.
11. In `plan.md`, include existing conventions, module boundaries, architecture locality, security/privacy impact, dependency impact, risks, and validation.
12. Implement according to the approved spec, plan, and tasks.
12. Do not force a smaller diff by putting code in the wrong place.
13. If a simple conceptual change touches many unrelated areas, call it out as a possible architecture smell.
14. Validate the result against the acceptance criteria and definition of done.
15. Summarize the final result, tests, remaining assumptions, and any architecture concerns.

When the request is large, ambiguous, or likely to span multiple sessions:
- prefer a planning step before coding;
- keep the plan detailed and reviewable;
- if a persistent plan would help future sessions, save it in a project-local planning document.
