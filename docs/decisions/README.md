# Decision Index

[Back to the project knowledge index](../INDEX.md) ·
[Decision template](_template.md)

Record durable product, architecture, dependency, persistence, integration or
security decisions when their rationale and consequences should survive the
change that introduced them.

Do not create a separate record for trivial or easily reversible choices. A
change-local decision may stay in its change folder until it becomes durable
project guidance.

## Decisions

| Decision | Status | Related product | Related architecture |
| --- | --- | --- | --- |
| [Separate advisory repository health from regression gates](0001-separate-advisory-health-from-regression-gates.md) | accepted | [Audit contract](../product/README.md#generated-maintainability-and-knowledge-audit) | [Audit boundary](../architecture/README.md#generated-maintainability-audit-boundary) |
| [Use an explicit prospective documentation baseline](0002-use-an-explicit-prospective-documentation-baseline.md) | accepted | [Workflow contract](../product/living-documentation-workflow.md) | [Validation architecture](../architecture/documentation-validation.md) |

When replacing a decision, preserve its history and link to the superseding
record instead of rewriting the original rationale.
