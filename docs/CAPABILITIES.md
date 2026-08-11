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
| Bootstrap file application and upgrade | [Product](product/README.md) | [Architecture](architecture/README.md) | `verified` | The 103-test suite passes, including rendered Python/Rust audit and wait-policy contracts; lifecycle, manifest, state, planner/applier, CLI/TUI, incident and semantic checks remain covered. | — | — |
| Integrated maintainability and knowledge audit | [Current audit contract](product/README.md#generated-maintainability-and-knowledge-audit) | [Audit boundary](architecture/README.md#generated-maintainability-audit-boundary) | `verified` | [Eleven focused audit contracts](../tests/test_maintainability_audit.py) cover scope, deterministic advisory output, size, missing/orphan/concentrated owners, closeout signals, sensitive exclusions, generated workflow integration and fresh Python/Rust execution; the full 103-test suite, compile validation, manifest validation and [generated skill validation](../ai_workflow_bootstrap/template_packs/default/templates/.agents/skills/maintainability-audit/SKILL.md) pass. | — | — |
| Navigable living-documentation workflow | [Workflow contract](product/living-documentation-workflow.md) | [Validation architecture](architecture/documentation-validation.md) | `verified` | The 118-test suite plus 23 subtests passes across shared parsing, aggregate checks, generation, reapplication, legacy state and conservative baseline migration; source aggregate, direct living-doc/link, compile and dry-run validations also pass. | — | — |

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
