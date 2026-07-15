"""State helpers for bootstrap persistence.

This module now supports the real `.ai-bootstrap/state.json` output used by the
CLI, while staying small and explicit.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .lifecycle import WRITABLE_STATUSES, content_hash

if TYPE_CHECKING:
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
    retired_files: dict[str, dict[str, Any]] = field(default_factory=dict)
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
        applied_at=datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        target_path=target_path,
        enabled_workflows=enabled_workflows,
        files=files or {},
        optional_modules=optional_modules or [],
    )


def load_state(path: Path) -> BootstrapState | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read bootstrap state {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"Cannot read bootstrap state {path}: top-level JSON must be an object")

    files = data.get("files", {})
    retired_files = data.get("retired_files", {})
    if not isinstance(files, dict) or not isinstance(retired_files, dict):
        raise ValueError(f"Cannot read bootstrap state {path}: files inventories must be objects")

    return BootstrapState(
        tool_name=str(data.get("tool_name", "ai-workflow-bootstrap")),
        tool_version=str(data.get("tool_version", "unknown")),
        template_pack=str(data.get("template_pack", "unknown")),
        template_pack_version=str(data.get("template_pack_version", "unknown")),
        applied_at=str(data.get("applied_at", "")),
        target_path=str(data.get("target_path", "")),
        enabled_workflows=[str(value) for value in data.get("enabled_workflows", [])]
        if isinstance(data.get("enabled_workflows", []), list)
        else [],
        files={str(key): value if isinstance(value, dict) else {} for key, value in files.items()},
        retired_files={
            str(key): value if isinstance(value, dict) else {} for key, value in retired_files.items()
        },
        optional_modules=[str(value) for value in data.get("optional_modules", [])]
        if isinstance(data.get("optional_modules", []), list)
        else [],
    )


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
    prior_state: BootstrapState | None = None,
) -> BootstrapState:
    files: dict[str, dict[str, Any]] = {
        path: dict(entry) for path, entry in (prior_state.files.items() if prior_state else [])
    }
    retired_files: dict[str, dict[str, Any]] = {
        path: dict(entry) for path, entry in (prior_state.retired_files.items() if prior_state else [])
    }
    for item in results:
        try:
            relative_path = item.path.relative_to(plan.target)
        except ValueError:
            continue
        relative = str(relative_path)
        if item.kind == "deletion":
            if item.status == "deleted":
                previous = files.pop(relative, {})
                retired_files[relative] = {
                    "status": "deleted",
                    "lifecycle": getattr(item, "lifecycle", "migrated"),
                    "retired_at_version": plan.pack.version,
                    **({"previous": previous} if previous else {}),
                }
            continue
        if item.kind != "file":
            continue
        status = item.status
        if status == "written" and item.existing:
            status = "overwritten"
        previous = files.get(relative, {})
        entry: dict[str, Any] = dict(previous)
        entry["status"] = status
        lifecycle = getattr(item, "lifecycle", "managed")
        entry["lifecycle"] = lifecycle
        if item.ownership != "bootstrap":
            entry["ownership"] = item.ownership
        proven_content = status in WRITABLE_STATUSES or status == "unchanged"
        if item.template and (proven_content or not previous):
            entry["template"] = item.template
            entry["template_hash"] = item.template_hash
        if proven_content and item.content:
            entry["applied_content_hash"] = content_hash(item.content)
            entry["applied_version"] = plan.pack.version
        files[relative] = entry

    return BootstrapState(
        tool_name="ai-workflow-bootstrap",
        tool_version=tool_version,
        template_pack=plan.pack.name,
        template_pack_version=plan.pack.version,
        applied_at=datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        target_path=str(plan.target.resolve()),
        enabled_workflows=plan.enabled_workflows,
        files=files,
        retired_files=retired_files,
        optional_modules=[],
    )
