---
name: maintainability-audit
description: Audit code and living-knowledge maintainability before planning or after non-trivial changes. Use when files or documents are large, responsibilities or ownership are unclear, tests are brittle, knowledge pages are concentrated or orphaned, current truth remains in change artifacts, or a small conceptual change touches many files.
---

1. Inspect the smallest relevant code and knowledge area. For deterministic signals run `python .agents/skills/maintainability-audit/scripts/audit_repository.py . --path <path>` with repeated paths; use `--repo-wide` only when explicitly requested or scoped evidence justifies it.
2. Treat script output and size thresholds as review signals, not semantic verdicts or hard limits. A large cohesive reference may remain; a small mixed-responsibility file may still need work.
3. Check code for long functions, duplication, brittle tests, unclear ownership and shotgun surgery. Check living docs for retrieval cost, mixed owners, orphan pages, concentrated capability routes, missing decisions and current truth trapped in change artifacts.
4. For each finding report evidence, risk, relation to the active change and one disposition:
   - safe local cleanup;
   - planned local refactor;
   - separate refactor spec;
   - advisory observation.
5. Before approval, include directly related requirements in the spec. After approval, do not expand scope silently: reconcile material in-scope changes, route unrelated work to a separate spec, or accept an advisory finding with rationale.
6. Prefer local refactors that reduce future human/agent context. Flag tests coupled to implementation details.
7. Re-audit the implemented diff and affected knowledge owners at closeout. Report inspected scope so a clean scoped result is not mistaken for a repository baseline.

The audit is advisory; existing correctness, security and living-doc regression gates remain blocking.
