# Spec-Driven Workflow

This is detailed on-demand guidance. The `spec-driven` skill is the normal
operational entry point.

## Two approval gates

For non-trivial work:

1. Clarify the problem, outcome, scope, constraints and acceptance criteria.
2. Draft `docs/changes/<change>/spec.md`.
3. Pause for explicit spec approval.
4. Inspect code and conventions, then draft `plan.md` and `tasks.md`.
5. Pause for explicit approval of both plan and tasks.
6. Implement, validate, update durable knowledge and summarize.

Spec approval does not approve the implementation approach. Silence is not
approval. The user may explicitly compress the workflow when risk is low.

## Artifact owners

Use the standalone templates; do not reproduce them here:

- [spec template](changes/_templates/spec.md): what must become true;
- [plan template](changes/_templates/plan.md): how the approved result will be
  implemented and validated;
- [tasks template](changes/_templates/tasks.md): concrete ordered execution;
- [notes template](changes/_templates/notes.md): meaningful deviations;
- [open questions](changes/_templates/open_questions.md): unresolved blockers;
- [change decisions](changes/_templates/decisions.md): change-local rationale.

Use kebab-case for the change folder. Rewrite generic template prompts into
change-specific content.

## Specification

A good-enough spec states:

- problem, goal, users and main flow;
- scope and explicit exclusions;
- functional and non-functional requirements;
- important edge cases, constraints and assumptions;
- maintainability, security, reliability and compatibility concerns;
- affected living-knowledge owners;
- testable acceptance criteria and unresolved questions.

Avoid premature implementation details unless they are genuine constraints.
If important ambiguity remains, surface it instead of guessing.

## Maintainability routing

Before drafting a non-trivial spec, inspect the smallest relevant code and
knowledge area. Run the scoped maintainability audit when files are large,
ownership is unclear, documentation is concentrated or orphaned, tests are
brittle, current truth appears trapped in change artifacts, or a small concept
touches many files.

Treat deterministic findings as evidence for review, not automatic refactor
orders. Record each relevant finding, risk and disposition:

- safe local cleanup;
- planned local refactor within the approved outcome;
- separate refactor spec;
- advisory observation accepted with rationale.

After spec approval, findings cannot cause silent scope expansion. Reconcile a
material in-scope contract change and obtain the required approval; route broad
or unrelated debt to a separate spec; keep justified advisory findings visible
without forcing work. Repeat the scoped audit during planning and against the
implemented diff and affected knowledge owners at closeout. A clean scoped
result is not a repository-wide baseline.

At closeout list the exact existing repository-relative paths inspected. Record
each current stable finding code/path as `accepted` with rationale or
`separate-spec` with an existing spec reference; use `resolved` only when that
tuple no longer appears, and the sole `no-findings` sentinel only for a clean
declared scope. These structural checks account for findings without turning
size or concentration thresholds into semantic verdicts.

## Planning

After spec approval, inspect relevant code, tests, structure, configuration,
interfaces, persistence and established error/logging patterns. The plan should
identify:

- module ownership and boundaries;
- expected files and intentionally untouched areas;
- data/API, security, dependency and operational impact;
- risks, rollback and ordered implementation steps;
- tests that protect the approved contract without freezing internals;
- living-doc owners, current-state evidence and approved-target links.
- exact owner paths and durable facts expected to be added, changed or removed.

Then create concrete tasks and request the second approval.

## Implementation and validation

Follow the approved artifacts and record meaningful deviations. If repository
reality contradicts the spec, stop and resolve the conflict rather than hiding
scope expansion.

Before completion:

- validate acceptance criteria and relevant edge cases;
- run proportionate tests/checks or document why they could not run;
- confirm boundaries remain cohesive and no unrelated behavior changed;
- ensure secrets and sensitive data stayed out of code, logs and docs;
- update current capability state only when implementation/evidence supports it;
- distill durable product, architecture, roadmap and decision facts;
- run `check_docs.py . --closeout docs/changes/<change> --advisory`;
- close living documentation only as `updated` or justified
  `no-update-needed`; unresolved follow-up work keeps the change open;
- validate relative links and close `tasks.md` with durable-fact and
  maintainability dispositions.

The final summary reports changed behavior, validation, documentation updates,
remaining limitations and any architectural concern.
