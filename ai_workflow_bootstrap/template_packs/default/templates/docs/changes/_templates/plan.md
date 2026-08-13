# Implementation Plan: <title>

## 1. Contract Basis

- Route: `approved-spec` or `existing-contract-repair`
- Approved spec: <relative link or `not required`>
- Existing authority: <relative link; required for a no-spec repair>
- Behavioral novelty: <`none`, `partial` or `material`>
- Execution risk and rationale:

For an existing-contract repair, begin here by linking the authority and
declaring Behavioral novelty `none`. If planning reveals a new decision or
conflict, stop and create or reconcile a spec before continuing.

## 2. Summary

## 3. Repair Evidence (when no spec exists)

- Reproduction:
- Diagnosed cause:
- Repair boundary:
- Regression to add or preserve:

Delete this section for a spec-led change. Do not copy the existing contract.

## 4. Relevant Existing Context

## 5. Existing Conventions Found

- Folder structure:
- Naming style:
- Error handling:
- Logging:
- Testing pattern:
- Config pattern:
- External integration pattern:
- Persistence/data access pattern:

## 6. Proposed Changes

## 7. Module Boundaries

- What module owns this responsibility?
- What module must not know about this change?
- What interface or adapter boundary should be preserved?
- What should remain decoupled?

## 8. Architecture Locality

- Finding disposition from the approved scoped audit:
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

## 9. Data / API / Interface Impact

## 10. Security / Privacy Impact

- Does this touch credentials, tokens, secrets, user data, logs, permissions, network calls, files, or external APIs?
- Are secrets kept out of Git?
- Are logs free of sensitive data?
- Are external inputs validated?

## 11. Dependency Impact

- Are new dependencies needed?
- Why are existing tools insufficient?
- Is the dependency runtime, build-time, or dev-only?
- What are the maintenance/security implications?

## 12. Risks

## 13. Validation Strategy

Include only tests that protect the approved spec or existing authority. If a
test would mainly lock down implementation detail, leave it out and explain why.

## 13.1 Test Strategy
- Contract to protect:
- Tests to add or update:
- Tests intentionally not added:
- Why these tests should survive internal refactors:

## 14. Living Documentation Impact

- Product fact owner(s) to update:
- Architecture fact owner(s) to update:
- Exact owner paths:
- Durable facts to add/change/remove:
- Current state/evidence changes:
- Approved target/active-change changes:
- Roadmap/decision changes:
- Links/evidence to validate:
- Why no living-doc update is needed, if applicable:
- Targeted closeout command:

## 15. Execution Steps

## 16. Rollback / Recovery

## 17. Notes
