from __future__ import annotations

from pathlib import Path

from .backup import create_backup
from .planner import BootstrapPlan, WriteResult


def _write_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def apply_plan(plan: BootstrapPlan, *, dry_run: bool, backup_existing: bool) -> list[WriteResult]:
    results: list[WriteResult] = []
    for item in plan.results:
        if item.kind == "directory":
            if not dry_run:
                _write_directory(item.path)
            results.append(item)
            continue

        if item.status in {"skipped", "unchanged"}:
            results.append(item)
            continue

        if not dry_run:
            if item.needs_backup and backup_existing and item.path.exists():
                create_backup(item.path)
            _write_file(item.path, item.content)
        results.append(item)

    return results

