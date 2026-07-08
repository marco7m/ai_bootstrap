"""State helpers for bootstrap persistence.

This module now supports the real `.ai-bootstrap/state.json` output used by the
CLI, while staying small and explicit.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .planner import BootstrapPlan, WriteResult


@dataclass
class BootstrapState:
    tool_name: str
    tool_version: str
    template_pack: str
    template_pack_version: str
    applied_at: str
    target_path: str
    enabled_workflows: list[str] = field(default_factory=list)
    files: dict[str, dict[str, Any]] = field(default_factory=dict)
    optional_modules: list[str] = field(default_factory=list)


def state_path(target: Path) -> Path:
    return target / ".ai-bootstrap" / "state.json"


def new_state(
    *,
    target_path: str,
    template_pack: str,
    template_pack_version: str,
    enabled_workflows: list[str],
    tool_version: str,
    files: dict[str, dict[str, Any]] | None = None,
    optional_modules: list[str] | None = None,
) -> BootstrapState:
    return BootstrapState(
        tool_name="ai-workflow-bootstrap",
        tool_version=tool_version,
        template_pack=template_pack,
        template_pack_version=template_pack_version,
        applied_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        target_path=target_path,
        enabled_workflows=enabled_workflows,
        files=files or {},
        optional_modules=optional_modules or [],
    )


def load_state(path: Path) -> BootstrapState | None:
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return BootstrapState(**data)


def save_state(path: Path, state: BootstrapState, *, dry_run: bool = False) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(state), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_state(
    *,
    plan: BootstrapPlan,
    results: list[WriteResult],
    tool_version: str,
) -> BootstrapState:
    files: dict[str, dict[str, Any]] = {}
    for item in results:
        if item.kind != "file":
            continue
        try:
            relative_path = item.path.relative_to(plan.target)
        except ValueError:
            continue
        status = item.status
        if status == "written" and item.existing:
            status = "overwritten"
        entry: dict[str, Any] = {"status": status}
        if item.template:
            entry["template"] = item.template
            entry["template_hash"] = item.template_hash
        files[str(relative_path)] = entry

    return BootstrapState(
        tool_name="ai-workflow-bootstrap",
        tool_version=tool_version,
        template_pack=plan.pack.name,
        template_pack_version=plan.pack.version,
        applied_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        target_path=str(plan.target.resolve()),
        enabled_workflows=plan.enabled_workflows,
        files=files,
        optional_modules=[],
    )
