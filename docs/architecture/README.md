# Architecture: ai_bootstrap

[Index](../INDEX.md) · [Capabilities](../CAPABILITIES.md) ·
[Product](../product/README.md)

This area owns how the current system realizes the product contract.

## Current architecture

Detected stack: python.

Repository areas:

- `docs/`
- `tests/`

Document the smallest useful current view: module responsibilities, boundaries,
external adapters, important data/control/runtime flows, persistence authority,
security/reliability/operations constraints and known limitations. Base claims
on repository or runtime evidence; state unknowns explicitly.

## Approved target architecture

Keep future boundaries separate from current architecture. Link the approved
target and active change; a design is not evidence that implementation exists.

## Architecture documents

Create a focused page only when a component, cross-cutting concern or flow has
enough durable detail. Link it here, from capabilities and relevant decisions.

## Detected commands

- `python -m build` — build
- `pytest` — test
- `pytest` — check
