from __future__ import annotations


def resolve_workflow_selection(*, include_skills: bool) -> tuple[list[str], set[str]]:
    enabled_workflows = ["spec-driven", "living-docs"]
    enabled_groups = {"spec-driven", "living-docs"}
    if include_skills:
        enabled_groups.update({"skill/spec-driven", "skill/maintainability-audit", "skill/living-docs"})
    return enabled_workflows, enabled_groups
