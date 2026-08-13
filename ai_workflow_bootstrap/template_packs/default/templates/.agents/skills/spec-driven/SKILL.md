---
name: spec-driven
description: Route features, repairs, refactors and investigations through existing authority, behavioral novelty, execution risk, approvals and proportionate validation.
---

1. Read repository instructions; inspect the smallest relevant knowledge, tests and code.
2. Locate the best current authority. Treat code/runtime as implementation evidence, not automatic intent. If structured living docs are absent, use available README, ADR, ticket, schema, API, test or supplied contract. When maintainability triggers exist, audit the scoped area before artifact choice and repeat it against the implemented diff at closeout.
3. Reason separately about behavioral novelty (`none`, `partial`, `material`) and execution risk. State it in one sentence only when it affects artifacts, gates, scope or material validation. Do not create an artifact only to record classification.
4. New behavior, ambiguity or conflicting authority requires a new/reconciled `spec.md` and explicit approval before planning.
5. A clear-contract repair or behavior-preserving maintenance does not automatically require a new spec.
6. Every non-trivial implementation requires proportional `plan.md`, `tasks.md` and explicit approval of both before coding. There is no risk-based exception.
7. A standalone no-spec repair uses `docs/changes/<repair>/plan.md` and `tasks.md`; link the restored authority, declare novelty `none`, and record reproduction, cause, boundary, risks, regression and validation.
8. Only genuinely trivial, unequivocal, low-risk work may flow directly. Read-only investigation does not authorize implementation or artifacts.
9. Stop and return to spec approval if a new behavioral decision, authority conflict or material contract expansion appears.
10. Implement the narrow approved plan. Keep incidental debt out unless it blocks acceptance or essential safety/correctness.
11. Validate from cheap focused checks through affected boundaries and real environments only as justified. Keep unavailable external gates pending.
12. Record meaningful evidence/deviations in `notes.md`, distill durable facts once, validate links and close tasks.

Open `docs/SPEC_DRIVEN.md` only for the detailed routes, artifact roles, handoff and validation ladder.
