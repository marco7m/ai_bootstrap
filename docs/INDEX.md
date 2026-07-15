# Project Knowledge Index

- Knowledge status: `incomplete`
- Baseline evidence: repository at `e57c818`, the validated 91-test lifecycle
  suite, fresh Python/Rust generation checks, and the reviewed 0.4.0 downstream
  overwrite incident (2026-07-15).
- Bootstrap recovery audit: the 0.4.0 overwrite of this repository's index,
  capabilities, product and architecture owners was reviewed during
  `protect-living-knowledge-ownership-v1`; current coverage remains explicitly
  incomplete rather than assuming the old scaffold was complete.

`scaffold` means these generated placeholders are not complete project truth.
Use `incomplete` when useful reviewed knowledge exists with known gaps. Use
`baselined` only after product intent and current architecture were reviewed
against the stated evidence.

## Knowledge owners

- [Product](product/README.md): purpose, expected behavior and approved targets.
- [Architecture](architecture/README.md): current implementation and technical constraints.
- [Capabilities](CAPABILITIES.md): current state/evidence and approved changes.
- [Roadmap](ROADMAP.md): ordered approved outcomes.
- [Decisions](decisions/README.md): durable rationale and consequences.
- [Idea inbox](IDEA_INBOX.md): unapproved possibilities.
- [Glossary](GLOSSARY.md): stable project terms.
- [Living-documentation policy](LIVING_DOCUMENTATION.md): ownership and maintenance.

## Reading path

1. Read this page and the relevant capability row.
2. Follow only the needed product or architecture links.
3. Open changes, decisions, tests or source when evidence is required.

Do not use an empty scaffold, one large change spec or a conversation transcript
as the current project description.

Current reviewed coverage is limited to bootstrap application/overwrite
ownership and the generated workflow surface. Broader product and architecture
coverage remains incomplete.
