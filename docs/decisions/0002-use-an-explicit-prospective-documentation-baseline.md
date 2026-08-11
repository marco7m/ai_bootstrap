# Decision: Use an Explicit Prospective Documentation Baseline

[Back to the decision index](README.md) ·
[Project knowledge index](../INDEX.md)

- Status: accepted
- Date: 2026-08-11
- Related product: [Living-documentation workflow](../product/living-documentation-workflow.md)
- Related architecture: [Documentation validation](../architecture/documentation-validation.md)
- Related capability: [Navigable living-documentation workflow](../CAPABILITIES.md)

## Context

Existing repositories may contain many completed changes created before a
structured documentation disposition existed. Failing all history immediately
would make adoption impractical. Inferring a cutoff from timestamps or pack
state would be unreliable, while rewriting old tasks would falsely imply
semantic review.

## Considered options

- Validate every historical change immediately.
- Infer a date or pack-version cutoff automatically.
- Ignore historical closeout debt permanently.
- Establish an explicit project-owned inventory and apply the strict gate
  prospectively.

## Decision

Use a seeded, human-readable baseline owner with reviewed evidence and exact
grandfathered change paths. Grandfathering exempts an entry only from the
prospective gate; it remains visible unresolved debt. Bootstrap application may
create the empty scaffold but never discovers, populates or resolves entries.

Once the baseline is established, every completed unlisted change must satisfy
the current closeout contract. Debt reduction requires real review and does not
require editing the historical artifact.

## Consequences

- Existing repositories can adopt stricter checks without becoming immediately
  unusable.
- New debt cannot hide behind an inferred historical cutoff.
- The baseline is reviewable by humans and deterministic tools.
- Establishment is a deliberate project action, not an automatic migration.
- Projects must keep the inventory honest as debt is reviewed or paths change.

## Supersession

No superseding decision.
