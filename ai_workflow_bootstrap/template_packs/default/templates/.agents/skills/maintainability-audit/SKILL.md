---
name: maintainability-audit
description: Use before or after non-trivial changes when code seems hard to modify, tests seem brittle, files are large, functions are long, or a small change touches many files.
---

1. Read the current file or area with an eye for maintainability risk.
2. Look for large files, long functions, mixed responsibilities, duplicated logic, brittle tests, unclear ownership, and shotgun surgery.
3. Separate safe local cleanup from work that needs its own spec.
4. Do not recommend a broad refactor automatically if the change needs a spec or plan first.
5. Prefer quick local refactors that reduce future context needed by assistants.
6. Flag tests that lock implementation details instead of behavior contracts.
7. For each finding, classify it as one of:
   - safe local cleanup;
   - planned local refactor;
   - separate refactor spec.
8. Report:
   - findings;
   - risk level;
   - quick local refactors;
   - refactors that need their own spec;
   - tests to keep, remove, or rewrite;
   - final recommendation.

The skill is advisory. It should improve maintainability without turning every change into a large refactor.
