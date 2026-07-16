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

Generated owners such as the index, product, architecture and capability map
are scaffolds only at creation. After repository review or editing they are
project knowledge. Reapplying or upgrading the bootstrap is infrastructure
maintenance and does not authorize replacing that knowledge with seed text.

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

## Regeneration and recovery

Treat an unexpected downgrade, seed placeholder, sharply reduced capability
map, or product/architecture page that covers only the latest change as a
possible documentation regression.

1. Inspect `.ai-bootstrap/state.json` for recently overwritten seeded owners.
2. Compare relevant Git history when available, then check current change
   artifacts, code, tests and safe runtime evidence.
3. Restore the union of still-valid prior knowledge and later supported
   increments. Do not blindly restore an old file or infer intent from code.
4. Preserve every capability unless it has an explicit deprecated, rejected or
   superseded disposition. Recovered prose alone is not `verified` evidence.
5. Restore an honest `scaffold`, `incomplete` or `baselined` status and keep
   unresolved gaps explicit.
6. Before closeout, account for facts added, changed and removed; state what
   authorizes each removal.

When legacy state still records the destructive event after a completed audit,
record `Bootstrap recovery audit:` in `docs/INDEX.md` with the reviewed scope
and safe evidence reference. This is a disposition marker, not proof that all
project knowledge is complete.

Run both deterministic checks after recovery or structural closeout:

```bash
python .agents/skills/living-docs/scripts/check_living_docs.py
python .agents/skills/living-docs/scripts/check_links.py
```

The semantic checker detects objective contradictions and regression signals;
it does not certify that the documentation is complete or true.

Keep foundational pages compact; split only real responsibilities. Never store
secrets, credentials, private messages, production/customer data or sensitive
runtime payloads. Prefer relative links and sanitized evidence summaries.
