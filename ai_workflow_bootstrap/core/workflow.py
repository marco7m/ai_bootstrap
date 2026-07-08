from __future__ import annotations


def resolve_workflow_selection(*, mode: str, include_skills: bool) -> tuple[list[str], set[str]]:
    if mode == "living-docs":
        enabled_workflows = ["living-docs"]
        enabled_groups: set[str] = {"living-docs"}
        if include_skills:
            enabled_groups.add("skill/living-docs")
        return enabled_workflows, enabled_groups

    if mode == "spec-driven":
        enabled_workflows = ["spec-driven"]
        enabled_groups = {"spec-driven"}
        if include_skills:
            enabled_groups.update({"skill/spec-driven", "skill/maintainability-audit"})
        return enabled_workflows, enabled_groups

    if mode == "recommended":
        enabled_workflows = ["spec-driven", "living-docs"]
        enabled_groups = {"spec-driven", "living-docs"}
        if include_skills:
            enabled_groups.update({"skill/spec-driven", "skill/maintainability-audit", "skill/living-docs"})
        return enabled_workflows, enabled_groups

    raise ValueError(f"Unknown workflow mode: {mode}")
