# Documentation Validation Architecture

[Architecture hub](README.md) ·
[Product contract](../product/living-documentation-workflow.md) ·
[Capability map](../CAPABILITIES.md)

## Shared structural contract

Default pack `0.7.0` distributes a managed
`documentation_contract.py` beside the living-document checkers. It is the
single deterministic owner for Markdown links and supported ATX fragments,
capability rows and authority routes, index reachability, baseline tables and
closeout dispositions.

Generated scripts resolve imports from their own installed paths, so direct
execution works independently of the current working directory. The contract
uses only the Python standard library and emits no document contents.

## Adapter boundaries

- `check_links.py` blocks broken repository-local file and supported-fragment
  links while retaining its direct command.
- `check_living_docs.py` blocks objective current-state, navigation,
  capability-route, baseline and prospective-closeout regressions.
- `check_docs.py` composes the direct checks, targeted closeout and optional
  advisory output without duplicating parsing.
- `audit_repository.py` imports the shared contract but continues to own
  advisory collection. Size and capability-route concentration are independent
  signals and never fail solely by threshold.

The aggregate command supports repository validation and
`--closeout docs/changes/<change>`. Targeted closeout also requires an explicit
maintainability disposition. Git comparison remains optional evidence in the
living-doc checker.

## Baseline and prospective gate

The seeded baseline is constrained human-readable Markdown. Its explicit
status, evidence, grandfathered table and reviewed-disposition table are parsed
without interpreting free prose. Established grandfather paths define the
legacy exception boundary; timestamps are not trusted as completion evidence.
Malformed or stale inventory fails actionably and never authorizes mutation.

Missing or unestablished baseline produces setup guidance rather than silently
waiving or failing all history. Once established, a completed unlisted change
must have `updated` or justified `no-update-needed` disposition.

## Distribution boundary

The manifest owns distribution and lifecycle: baseline is `seeded`; parser and
checkers are `managed`. Existing `core.lifecycle`, planner, applier, state, CLI
and TUI remain unaware of Markdown and closeout semantics. Their existing
provenance matrix protects evolved seeds and supplies compatibility for older
state, including the repository's `0.5.1` self-host shape.
