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
| Bootstrap file application and upgrade | [Product](product/README.md) | [Architecture](architecture/README.md) | `verified` | The 92-test suite passes, including rendered Python/Rust contracts for generic long waits, interactive exceptions and conditional Cargo examples; lifecycle, manifest, state, planner/applier, CLI/TUI, incident and semantic checks remain covered. | — | — |

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
