"""State helpers for future bootstrap persistence.

This module is prepared infrastructure. It is intentionally not wired into the
CLI flow yet, so the current behavior remains focused on preserving the legacy
bootstrap output while the rest of the engine is introduced incrementally.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


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
