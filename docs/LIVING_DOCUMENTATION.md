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
- [Baseline](LIVING_DOCUMENTATION_BASELINE.md) owns reviewed coverage evidence
  and explicitly grandfathered historical closeout debt.

One durable fact has one owner; other documents link to it.

Generated owners such as the index, product, architecture and capability map
are scaffolds only at creation. After repository review or editing they are
project knowledge. Reapplying or upgrading the bootstrap is infrastructure
maintenance and does not authorize replacing that knowledge with seed text.

## Truth and coverage

- `scaffold` is generated structure, not established truth.
- `incomplete` has reviewed, navigable knowledge plus explicit gaps.
- `baselined` requires navigable reviewed product intent, current architecture,
  capability routes and stated evidence for a declared scope. Code can show
  what exists but cannot alone prove intended behavior.
- Keep current implementation separate from approved targets. A verified current
  capability can have a planned evolution without losing its current state.
- Investigate conflicts between docs and code/tests/runtime before updating either.

## Change lifecycle

1. Keep unapproved ideas in the inbox.
2. After spec approval, add the approved target and active change.
3. Identify living-doc owners in the plan/tasks.
4. Update current state only when implementation supports it.
5. Record `verified` only with safe relevant evidence.
6. At closeout, account for durable facts added, changed and removed; every
   removal needs disposition.
7. Close living documentation only as `updated` or justified
   `no-update-needed`; `pending`, `follow-up` and absence keep the change open.

## Navigation and baseline

`docs/INDEX.md` is the canonical entry point. Product and architecture READMEs
are compact hubs once real responsibilities gain focused owners. Every focused
current owner remains reachable from the index graph; capability product and
architecture routes stay within their respective authority areas.

`docs/LIVING_DOCUMENTATION_BASELINE.md` is established only after repository
review. Grandfathered exact paths remain visible unresolved debt and are exempt
only from the prospective gate. Bootstrap application never inventories or
marks historical changes reviewed. Once established, new completed changes
require a valid living-document disposition.

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

This repository's installed managed checks predate pack `0.7.0`; validate the
current reusable source surface with:

```bash
python ai_workflow_bootstrap/template_packs/default/templates/.agents/skills/living-docs/scripts/check_docs.py .
```

Generated/upgraded projects receive the shorter
`.agents/skills/living-docs/scripts/check_docs.py` path. Blocking checks detect
objective contradictions and regressions; advisory size/concentration does not
certify that documentation is complete or true.

Keep foundational pages compact; split only real responsibilities. Never store
secrets, credentials, private messages, production/customer data or sensitive
runtime payloads. Prefer relative links and sanitized evidence summaries.
