# Architecture: ai_bootstrap

[Index](../INDEX.md) · [Capabilities](../CAPABILITIES.md) ·
[Product](../product/README.md)

This area owns how the current system realizes the product contract.

## Current architecture

Detected stack: python.

Repository areas:

- `ai_workflow_bootstrap/core/`
- `ai_workflow_bootstrap/template_packs/`
- `ai_workflow_bootstrap/cli.py`
- `ai_workflow_bootstrap/tui.py`
- `docs/`
- `tests/`

The default template-pack manifest declares generated directories/files with
explicit lifecycle, project-owned paths, safe compositions, context fragments,
workflow groups, and guarded obsolete migrations. `core.template_pack` parses
and validates that declaration. `core.lifecycle` owns exact content hashing,
the pure managed/seeded decision matrix, reset confirmation, and writable versus
blocking statuses.

The renderer and scanner supply output content/context. `core.planner` observes
the target and combines manifest lifecycle with prior state provenance to
classify visible results. `core.applier` preflights all `conflict` and
`migration_required` results before executing an eligible mutation.
`core.state` compatibly reads old state and merges lifecycle,
`applied_content_hash`, applied pack version, unselected provenance and safe
retirement records after successful application.

CLI and TUI are adapters over the same plan/apply contract. They own selection,
preview and separate reset consent, not lifecycle decisions. Composition logic
owns structural updates to `Makefile` and `.gitignore`; force/reset never bypass
a composition or migration conflict. Optional Git comparison exists only in the
generated semantic checker and is not part of normal apply planning.

The managed base `AGENTS.md` template owns stack-independent process
classification and wait-cadence guidance. Manifest-selected context fragments
add only stack-specific examples; the Rust fragment classifies common Cargo
validation commands while leaving launched-program behavior authoritative.
Renderer, planner and execution adapters remain policy-agnostic.

## Approved target architecture

No further architecture target is currently approved. The current lifecycle
boundary and provenance flow were introduced by the completed
[living-knowledge ownership change](../changes/protect-living-knowledge-ownership-v1/spec.md).

## Architecture documents

Create a focused page only when a component, cross-cutting concern or flow has
enough durable detail. Link it here, from capabilities and relevant decisions.

## Detected commands

- `python -m build` — build
- `pytest` — test
- `pytest` — check
