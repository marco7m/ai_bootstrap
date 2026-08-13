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

### Generated workflow ownership

Default pack `0.8.0` keeps authority-first route invariants in the managed
`AGENTS.md`, start prompt and compact `spec-driven` skill. The managed
`docs/SPEC_DRIVEN.md` is the single on-demand owner for the detailed route
matrix, progressive context, artifact budgets, compact handoff, stop conditions
and validation ladder. The always-read surfaces stay within explicit word
budgets and link to that guide instead of copying it.

Existing spec/plan/tasks/notes templates represent both spec-led changes and
clear-contract repairs. A standalone non-trivial repair may have plan/tasks and
later notes without a spec. Generated link, living-document, aggregate and
maintainability checks remain tasks/change-directory oriented and enforce their
existing closeout contracts without deciding behavioral novelty. No routing
logic enters renderer, lifecycle, planner, applier, state, CLI or TUI modules.

### Generated maintainability audit boundary

Since pack `0.7.0`, the default pack (now `0.8.0`) declares
`.agents/skills/maintainability-audit/scripts/audit_repository.py` as a managed
standard-library tool. The script owns deterministic advisory collection,
explicit scoped/repo-wide traversal, sensitive/cache exclusions, Markdown
knowledge-graph reachability, capability-route concentration, completed-change
disposition checks and stable text/JSON output. It returns success for review
findings and never becomes a bootstrap planner or applier concern.

The generated `maintainability-audit` skill owns semantic cohesion, risk and
finding disposition. `spec-driven` owns the pre-spec, planning and closeout
timing plus approval-scope routing. `living-docs` owns focused knowledge pages,
durable fact distillation and ADR evaluation. Its existing semantic/link
checkers remain separate blocking regression gates, as recorded in
[the audit-boundary decision](../decisions/0001-separate-advisory-health-from-regression-gates.md).

The default manifest and renderer only distribute these managed artifacts.
Core planner, lifecycle, applier, state, CLI and TUI modules remain unaware of
maintainability thresholds and documentation heuristics.

The shared structural parser, blocking adapters, aggregate command and
prospective baseline boundary are owned by
[documentation validation](documentation-validation.md).

## Approved target architecture

There is no active approved architecture target. The project-agnostic
shared-contract repair was completed by
[Living Docs Downstream Compatibility v1](../changes/living-docs-downstream-compatibility-v1/spec.md),
preserving the generated parser/adapters and generic lifecycle boundary. The current
lifecycle boundary and provenance flow were introduced by the completed
[living-knowledge ownership change](../changes/protect-living-knowledge-ownership-v1/spec.md);
the audit boundary was introduced by the completed
[Integrated Maintainability and Knowledge Audit v1](../changes/integrated-maintainability-knowledge-audit-v1/spec.md).

## Architecture documents

- [Documentation validation](documentation-validation.md) owns generated parser,
  checker, baseline and distribution boundaries.

Create another focused page only when a component, cross-cutting concern or flow
has enough durable detail. Link it here, from capabilities and relevant decisions.

## Detected commands

- `python -m build` — build
- `pytest` — test
- `pytest` — check
