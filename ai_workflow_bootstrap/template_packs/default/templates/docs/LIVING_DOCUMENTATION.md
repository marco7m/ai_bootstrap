# Living Documentation

Living docs are compact current project knowledge, not transcripts.

## Ownership

- [INDEX](INDEX.md) owns navigation and coverage state.
- [Product](product/README.md) owns expected behavior and approved targets.
- [Architecture](architecture/README.md) owns current technical shape.
- [Capabilities](CAPABILITIES.md) owns current state/evidence and active changes.
- [Roadmap](ROADMAP.md) owns ordered approved outcomes.
- [Decisions](decisions/README.md) owns durable rationale.
- [Idea inbox](IDEA_INBOX.md) owns unapproved possibilities.

One durable fact has one owner; other documents link to it.

## Truth and coverage

- `scaffold` is generated structure, not established truth.
- `incomplete` has reviewed knowledge plus explicit gaps.
- `baselined` requires reviewed product intent, current architecture and stated
  evidence. Code can show what exists but cannot alone prove intended behavior.
- Keep current implementation separate from approved targets. A verified current
  capability can have a planned evolution without losing its current state.
- Investigate conflicts between docs and code/tests/runtime before updating either.

## Change lifecycle

1. Keep unapproved ideas in the inbox.
2. After spec approval, add the approved target and active change.
3. Identify living-doc owners in the plan/tasks.
4. Update current state only when implementation supports it.
5. Record `verified` only with safe relevant evidence.
6. At closeout, distill durable facts, remove stale active links and validate links.

Keep foundational pages compact; split only real responsibilities. Never store
secrets, credentials, private messages, production/customer data or sensitive
runtime payloads. Prefer relative links and sanitized evidence summaries.
