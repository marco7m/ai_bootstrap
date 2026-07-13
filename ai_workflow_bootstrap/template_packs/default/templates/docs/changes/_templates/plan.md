# Implementation Plan: <title>

## 1. Summary

## 2. Relevant Existing Context

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

## 11. Validation Strategy

Include only the tests that actually protect the approved spec. If a test would mainly lock down implementation detail, leave it out and explain why.

## 11.1 Test Strategy
- Contract to protect:
- Tests to add or update:
- Tests intentionally not added:
- Why these tests should survive internal refactors:

## 12. Living Documentation Impact

- Product fact owner(s) to update:
- Architecture fact owner(s) to update:
- Current state/evidence changes:
- Approved target/active-change changes:
- Roadmap/decision changes:
- Links/evidence to validate:
- Why no living-doc update is needed, if applicable:

## 13. Execution Steps

## 14. Rollback / Recovery

## 15. Notes
