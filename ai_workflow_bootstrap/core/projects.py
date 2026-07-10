from __future__ import annotations

import json
from pathlib import Path

RECENT_PROJECTS_PATH = Path.home() / ".ai-workflow-bootstrap" / "recent-projects.json"
PROJECT_MARKERS = {
    ".git",
    "pyproject.toml",
    "package.json",
    "Cargo.toml",
    "go.mod",
    "Makefile",
}
IGNORED_SCAN_DIR_NAMES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "__pycache__",
}


def _as_absolute_dir(path: Path) -> Path | None:
    candidate = Path(path).expanduser()
    try:
        candidate = candidate.resolve()
    except Exception:
        candidate = candidate.absolute()
    if not candidate.exists() or not candidate.is_dir():
        return None
    return candidate


def _dedupe_paths(projects: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    result: list[Path] = []
    for project in projects:
        absolute = _as_absolute_dir(project)
        if absolute is None or absolute in seen:
            continue
        seen.add(absolute)
        result.append(absolute)
    return result


def load_recent_projects(path: Path | None = None) -> list[Path]:
    storage = Path(path or RECENT_PROJECTS_PATH).expanduser()
    if not storage.exists():
        return []

    try:
        data = json.loads(storage.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    raw_projects: list[str] = []
    if isinstance(data, dict):
        raw_value = data.get("recent_projects", [])
        if isinstance(raw_value, list):
            raw_projects = [item for item in raw_value if isinstance(item, str)]
    elif isinstance(data, list):
        raw_projects = [item for item in data if isinstance(item, str)]
    else:
        return []

    return _dedupe_paths(Path(item) for item in raw_projects)


def save_recent_projects(projects: list[Path], path: Path | None = None) -> None:
    storage = Path(path or RECENT_PROJECTS_PATH).expanduser()
    storage.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "recent_projects": [str(project) for project in _dedupe_paths(projects)],
    }
    storage.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def add_recent_project(project: Path, path: Path | None = None, limit: int = 10) -> list[Path]:
    absolute = _as_absolute_dir(project)
    if absolute is None:
        return load_recent_projects(path)

    storage = Path(path or RECENT_PROJECTS_PATH).expanduser()
    existing = load_recent_projects(storage)
    updated = [absolute]
    updated.extend(candidate for candidate in existing if candidate != absolute)
    updated = updated[: max(limit, 0)]
    save_recent_projects(updated, storage)
    return updated


def is_project_dir(path: Path) -> bool:
    candidate = Path(path).expanduser()
    try:
        if not candidate.exists() or not candidate.is_dir():
            return False
    except OSError:
        return False
    return any((candidate / marker).exists() for marker in PROJECT_MARKERS)


def scan_project_dirs(base_dirs: list[Path] | None = None) -> list[Path]:
    home = Path.home()
    bases = base_dirs or [
        Path.cwd(),
        Path.cwd().parent,
        home,
        home / "projects",
        home / "Projects",
        home / "Projetos",
        home / "projetos",
        home / "slapy" / "projetos",
    ]

    candidates: list[Path] = []
    for base in bases:
        resolved_base = Path(base).expanduser()
        if is_project_dir(resolved_base):
            candidates.append(resolved_base)
        if not resolved_base.exists() or not resolved_base.is_dir():
            continue
        try:
            children = sorted(resolved_base.iterdir(), key=lambda item: item.name.casefold())
        except OSError:
            continue
        for child in children:
            if child.name.startswith(".") or child.name in IGNORED_SCAN_DIR_NAMES:
                continue
            try:
                is_directory = child.is_dir()
            except OSError:
                continue
            if is_directory and is_project_dir(child):
                candidates.append(child)

    deduped = _dedupe_paths(candidates)
    return sorted(deduped, key=lambda item: (item.name.casefold(), str(item).casefold()))


def format_project_choice(path: Path) -> str:
    candidate = Path(path).expanduser()
    name = candidate.name or candidate.as_posix()
    return f"{name} — {candidate}"
