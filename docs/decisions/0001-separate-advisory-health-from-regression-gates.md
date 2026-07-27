# Decision: Separate Advisory Repository Health from Regression Gates

[Back to the decision index](README.md) ·
[Project knowledge index](../INDEX.md)

- Status: accepted
- Date: 2026-07-27
- Related product: [generated audit contract](../product/README.md#generated-maintainability-and-knowledge-audit)
- Related architecture: [generated audit boundary](../architecture/README.md#generated-maintainability-audit-boundary)
- Related capability: [integrated maintainability and knowledge audit](../CAPABILITIES.md)

## Context

File size, capability-route concentration, orphaned knowledge and incomplete
change closeout are useful maintainability evidence, but they do not by
themselves prove incorrect behavior or documentation. Treating every threshold
as a failing check would force arbitrary splits and turn project-health guidance
into bureaucracy. Omitting deterministic signals entirely would leave agents
to rediscover the same repository evidence and would not expose slow knowledge
concentration.

The existing living-document checker already owns objective contradictions and
regressions such as invalid capability states, destroyed seeded owners and
verified capability loss.

## Considered options

- Make every health heuristic fail the existing living-document checker.
- Keep all maintainability inspection semantic and provide no deterministic
  repository signal collector.
- Generate a separate advisory collector and let skills interpret and route its
  findings while preserving objective regression gates.

## Decision

Generate a deterministic advisory audit with stable evidence and successful
exit status for findings. Keep objective living-document and link regressions as
separate blocking checks. The maintainability skill interprets cohesion and
risk; spec-driven controls approval scope; living docs owns knowledge
distillation and focused-page decisions.

Thresholds trigger review only. A material finding changes the active work only
through the normal spec/plan approval contract.

## Consequences

- Projects receive cheap, reproducible health evidence without automatic broad
  refactoring or documentation rewriting.
- CI and future integrations can consume stable text/JSON output without
  mistaking advisory debt for correctness failure.
- Agents must still make and record semantic disposition decisions.
- A clean scoped audit does not certify repository-wide health.
- Blocking and advisory interfaces need separate tests and documentation.

## Supersession

No superseding decision.
