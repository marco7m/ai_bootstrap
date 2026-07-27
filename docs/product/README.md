# Product: ai_bootstrap

[Index](../INDEX.md) · [Capabilities](../CAPABILITIES.md) ·
[Architecture](../architecture/README.md)

This area owns what the product is, why it exists and how it should behave.
Implementation mechanisms belong in architecture.

## Purpose and actors

`ai-workflow-bootstrap` prepares repositories with reusable agent instructions,
spec-driven change contracts, living-document scaffolds, and stack-aware
workflow support. Project owners use the CLI or TUI to preview and apply that
surface; agents and contributors consume the generated workflow and knowledge
owners.

## Current contract

The bootstrap renders declared files, safely composes supported repository-owned
files, previews operations, and writes state after successful application.
Rendered files are either permanently `managed` or seed-once `seeded` knowledge.
Without update consent, divergent managed files are skipped. `--force` updates
managed files while evolved or untracked seeded knowledge remains preserved.
Untouched seeds may safely receive a new rendered template when their current
content matches the last applied-content hash.

`--managed-only` excludes seeded and obsolete operations. Project-knowledge
reset is a separate destructive action that affects only seeded paths and
requires the exact `RESET PROJECT KNOWLEDGE` confirmation for a real CLI/TUI
apply. Dry-run may preview it without confirmation.

Obsolete bootstrap files are deleted only when prior state proves their current
content still matches the last applied content. Drifted, untracked or malformed
provenance produces `migration_required`, preserves the file and blocks the
entire real apply before any write.

Project-owned paths such as `AGENTS.project.md` and conflicting composition
targets remain protected. The tool creates no backup, commit, branch, or stash.

Generated agent instructions classify process behavior before choosing a
terminal wait cadence. Finite non-interactive work uses the longest supported
wait, targeting up to five minutes, and avoids completion-only short polling;
interactive or persistent processes retain responsive observation. Rust
projects also receive conditional Cargo examples without assuming that every
program launched through Cargo is non-interactive.

### Generated maintainability and knowledge audit

Generated projects receive a local standard-library audit that inspects an
explicit path set during ordinary work or the whole repository only when
requested. It reports stable advisory evidence for large files, orphaned
current-knowledge pages, concentrated capability routing, missing owner
baselines and completed changes without a living-document disposition. It
skips common generated, dependency, cache and sensitive local paths and emits
measurements rather than file contents.

The generated maintainability skill interprets those signals across code and
living knowledge. It classifies local cleanup, planned refactoring,
separate-spec work and accepted advisory observations. Spec-driven guidance
runs that review proportionally before specification, during planning and
against the implemented diff at closeout. Findings discovered after approval
cannot silently expand the active contract.

Size remains a cohesion trigger rather than a failure. Existing link and
living-document regression checks remain the blocking validation surface;
agents retain responsibility for semantic ownership, intent and whether a
focused wiki page or ADR is justified.

## Approved targets

No further product target is currently approved. The generated audit contract
was introduced by the completed
[Integrated Maintainability and Knowledge Audit v1](../changes/integrated-maintainability-knowledge-audit-v1/spec.md).

The lifecycle-aware ownership contract was introduced by the completed
[living-knowledge ownership change](../changes/protect-living-knowledge-ownership-v1/spec.md).

## Product documents

Create a focused page only when a real product responsibility has enough durable
detail. Link it here and from the relevant capability row.
