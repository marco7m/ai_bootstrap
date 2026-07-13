# Notes: Living Knowledge Base v1

## Implementation deviation

The repository-local `.agents/skills/spec-driven/SKILL.md` could not be updated
because that path is read-only in the active workspace permissions. The
downstream generated skill at
`ai_workflow_bootstrap/template_packs/default/templates/.agents/skills/spec-driven/SKILL.md`
and the source workflow guidance were updated, so projects bootstrapped from
this repository receive the approved lifecycle integration.

No production Python module, CLI/TUI behavior, state schema, dependency or
launcher behavior changed.
