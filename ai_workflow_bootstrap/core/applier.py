from __future__ import annotations

from pathlib import Path

from .planner import BootstrapPlan, WriteResult


class PlanConflictError(ValueError):
    pass


def _write_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def apply_plan(plan: BootstrapPlan, *, dry_run: bool) -> list[WriteResult]:
    conflicts = [item for item in plan.results if item.status == "conflict"]
    if conflicts and not dry_run:
        details = "\n\n".join(item.message for item in conflicts)
        raise PlanConflictError(details)

    results: list[WriteResult] = []
    for item in plan.results:
        if item.kind == "directory":
            if not dry_run:
                _write_directory(item.path)
            results.append(item)
            continue

        if item.kind == "deletion":
            if item.status == "deleted" and not dry_run:
                item.path.unlink()
            results.append(item)
            continue

        if item.status in {"skipped", "unchanged", "preserved", "conflict"}:
            results.append(item)
            continue

        if not dry_run:
            _write_file(item.path, item.content)
        results.append(item)

    return results
