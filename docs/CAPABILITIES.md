# Capabilities

[Back to the project knowledge index](INDEX.md).

This active map routes each meaningful capability to its contract and evidence.
Detailed behavior and design remain in their owning documents.

## Current states

- `unknown`: current implementation has not been established;
- `absent`: evidence shows the capability does not currently exist;
- `partial`: only part of the current contract exists;
- `implemented`: implementation exists but is not fully validated;
- `verified`: relevant safe evidence confirms the current contract;
- `deprecated`: current behavior is being retired.

## Active map

| Capability | Product contract | Architecture | Current state | Evidence | Approved target | Active change |
| --- | --- | --- | --- | --- | --- | --- |
| Bootstrap file application and upgrade | [Product](product/README.md) | [Architecture](architecture/README.md) | `verified` | Default pack `0.8.0` passes 133 pytest tests plus 23 subtests and 133 unittest tests, compile validation, approved context budgets, fresh Python/Rust/Node delivery, synthetic `0.7.1` managed upgrade/reapply, seeded/project-owned preservation and generated no-spec repair checks. | — | — |
| Integrated maintainability and knowledge audit | [Current audit contract](product/README.md#generated-maintainability-and-knowledge-audit) | [Audit boundary](architecture/README.md#generated-maintainability-audit-boundary) | `verified` | [Focused audit contracts](../tests/test_maintainability_audit.py) cover scope, deterministic advisory output, size, missing/orphan/concentrated owners, closeout signals, sensitive exclusions, generated workflow integration and fresh Python/Rust execution; the 133-test suites, compile validation, manifest validation and [generated skill validation](../ai_workflow_bootstrap/template_packs/default/templates/.agents/skills/maintainability-audit/SKILL.md) pass. | — | — |
| Navigable living-documentation workflow | [Workflow contract](product/living-documentation-workflow.md) | [Validation architecture](architecture/documentation-validation.md) | `verified` | Pack `0.7.1` passes 127 tests plus 23 subtests, full unittest/compile validation, generic canonical-fragment and malformed baseline/closeout fixtures, source and generated direct/aggregate execution, lifecycle-preservation dry-run and targeted closeout. A read-only established-downstream run preserved status and correctly rejected its current non-canonical links without project-specific aliases. | — | — |

## Rules

- Approval adds an approved target and active change; it does not replace a
  valid current state or evidence.
- A capability may be `verified` now while its next evolution is approved.
- Use `verified` only with relevant tests, runtime evidence or another safe
  validation artifact.
- Keep unapproved ideas in [the inbox](IDEA_INBOX.md).
- Remove completed active-change links after distilling durable facts.
- Move rejected/superseded intent out of this active map after preserving any
  useful disposition or durable decision.
- Link to safe repository evidence; do not copy source, logs or sensitive data.
