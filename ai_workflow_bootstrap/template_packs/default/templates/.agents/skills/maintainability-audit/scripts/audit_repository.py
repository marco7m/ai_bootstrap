#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote

MARKDOWN_LINE_LIMIT = 250
MARKDOWN_BYTE_LIMIT = 16 * 1024
SOURCE_LINE_LIMIT = 500
SOURCE_BYTE_LIMIT = 32 * 1024
CONCENTRATION_ROUTE_LIMIT = 4

SOURCE_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".go",
    ".h",
    ".hpp",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".kts",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sql",
    ".swift",
    ".ts",
    ".tsx",
}
EXCLUDED_DIRS = {
    ".ai-bootstrap",
    ".codex",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "vendor",
    "venv",
}
SENSITIVE_SUFFIXES = {".key", ".pem", ".p12", ".pfx"}
KNOWLEDGE_ROOTS = (
    "docs/INDEX.md",
    "docs/CAPABILITIES.md",
    "docs/product/README.md",
    "docs/architecture/README.md",
    "docs/decisions/README.md",
)
PLACEHOLDERS = {
    "docs/product/README.md": "Describe the problem, desired outcome",
    "docs/architecture/README.md": "Document the smallest useful current view",
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CHECKBOX = re.compile(r"^- \[[ xX]\]", re.MULTILINE)
UNCHECKED = re.compile(r"^- \[ \]", re.MULTILINE)
CAPABILITY_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
LIVING_DISPOSITION = re.compile(
    r"^- Living documentation:\s*`([^`]+)`(?:\s*[—–:-]\s*(.+))?\s*$",
    re.MULTILINE,
)


@dataclass(frozen=True, order=True)
class Finding:
    code: str
    level: str
    path: str
    evidence: str


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _is_sensitive_name(name: str) -> bool:
    lowered = name.lower()
    return (
        lowered == ".env"
        or lowered.startswith(".env.")
        or lowered in {"credentials", "credentials.json", "secrets.json"}
        or Path(lowered).suffix in SENSITIVE_SUFFIXES
    )


def _is_excluded(root: Path, path: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True
    return any(part in EXCLUDED_DIRS for part in relative.parts) or _is_sensitive_name(path.name)


def _iter_directory(root: Path, directory: Path):
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            continue
        if path.is_file() and not _is_excluded(root, path):
            yield path


def _resolve_scope(
    root: Path,
    requested_paths: list[str] | None,
    repo_wide: bool,
) -> tuple[list[Path], list[str]]:
    files: set[Path] = set()
    skipped: list[str] = []
    if repo_wide:
        files.update(_iter_directory(root, root))
        return sorted(files), skipped

    for raw in requested_paths or []:
        candidate = (root / raw).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"scoped path escapes repository root: {raw}") from exc
        if not candidate.exists():
            raise ValueError(f"scoped path does not exist: {raw}")
        if _is_excluded(root, candidate):
            skipped.append(raw)
            continue
        if candidate.is_dir():
            files.update(_iter_directory(root, candidate))
        elif candidate.is_file():
            files.add(candidate)
    return sorted(files), sorted(skipped)


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _measure(path: Path) -> tuple[int, int, str] | None:
    suffix = path.suffix.lower()
    if suffix == ".md":
        kind = "markdown"
        line_limit = MARKDOWN_LINE_LIMIT
        byte_limit = MARKDOWN_BYTE_LIMIT
    elif suffix in SOURCE_SUFFIXES:
        kind = "source"
        line_limit = SOURCE_LINE_LIMIT
        byte_limit = SOURCE_BYTE_LIMIT
    else:
        return None
    text = _read_text(path)
    if text is None:
        return None
    return len(text.splitlines()), path.stat().st_size, (
        f"kind={kind}; line_limit={line_limit}; byte_limit={byte_limit}"
    )


def _is_large(path: Path) -> tuple[bool, int, int, str] | None:
    measured = _measure(path)
    if measured is None:
        return None
    lines, size, limits = measured
    if path.suffix.lower() == ".md":
        large = lines > MARKDOWN_LINE_LIMIT or size > MARKDOWN_BYTE_LIMIT
    else:
        large = lines > SOURCE_LINE_LIMIT or size > SOURCE_BYTE_LIMIT
    return large, lines, size, limits


def _size_findings(root: Path, files: list[Path], repo_wide: bool) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        relative = _relative(root, path)
        if repo_wide and relative.startswith("docs/changes/"):
            continue
        measured = _is_large(path)
        if measured is None or not measured[0]:
            continue
        _, lines, size, limits = measured
        findings.append(
            Finding(
                code="large-file-review",
                level="advisory",
                path=relative,
                evidence=f"lines={lines}; bytes={size}; {limits}",
            )
        )
    return findings


def _normalize_markdown_target(root: Path, source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().strip("<>")
    if not target or target.startswith("#") or "://" in target or target.startswith("mailto:"):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None
    candidate = (source.parent / target).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    if candidate.is_dir():
        candidate /= "README.md"
    return candidate if candidate.suffix.lower() == ".md" else None


def _reachable_markdown(root: Path) -> set[Path]:
    pending = [
        root / relative
        for relative in KNOWLEDGE_ROOTS
        if (root / relative).is_file()
    ]
    reachable: set[Path] = set()
    while pending:
        current = pending.pop()
        current = current.resolve()
        if current in reachable or _is_excluded(root, current):
            continue
        reachable.add(current)
        text = _read_text(current)
        if text is None:
            continue
        for raw_target in MARKDOWN_LINK.findall(text):
            target = _normalize_markdown_target(root, current, raw_target)
            if target is not None and target.is_file() and target not in reachable:
                pending.append(target)
    return reachable


def _current_knowledge_pages(root: Path):
    for area in ("product", "architecture", "decisions"):
        directory = root / "docs" / area
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.md")):
            if path.name == "_template.md" or _is_excluded(root, path):
                continue
            yield path.resolve()


def _orphan_findings(root: Path, scoped_files: set[Path] | None = None) -> list[Finding]:
    reachable = _reachable_markdown(root)
    return [
        Finding(
            code="orphan-current-doc",
            level="review",
            path=_relative(root, path),
            evidence="current knowledge page is not reachable from canonical knowledge roots",
        )
        for path in _current_knowledge_pages(root)
        if path not in reachable and (scoped_files is None or path in scoped_files)
    ]


def _capability_targets(root: Path) -> dict[Path, set[str]]:
    capability_path = root / "docs/CAPABILITIES.md"
    text = _read_text(capability_path)
    targets: dict[Path, set[str]] = {}
    if text is None:
        return targets
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7 or cells[0] in {"Capability", "---", "_Capability_"}:
            continue
        for cell in cells[1:3]:
            match = CAPABILITY_LINK.search(cell)
            if match is None:
                continue
            target = _normalize_markdown_target(root, capability_path, match.group(1))
            if target is not None:
                targets.setdefault(target, set()).add(cells[0])
    return targets


def _concentration_findings(root: Path, scoped_files: set[Path] | None = None) -> list[Finding]:
    findings: list[Finding] = []
    capability_map_scoped = (
        scoped_files is not None
        and (root / "docs/CAPABILITIES.md").resolve() in scoped_files
    )
    for path, capabilities in _capability_targets(root).items():
        if (
            scoped_files is not None
            and not capability_map_scoped
            and path.resolve() not in scoped_files
        ):
            continue
        if len(capabilities) < CONCENTRATION_ROUTE_LIMIT or not path.is_file():
            continue
        measured = _is_large(path)
        if measured is None or not measured[0]:
            continue
        _, lines, size, _ = measured
        findings.append(
            Finding(
                code="knowledge-owner-concentration",
                level="review",
                path=_relative(root, path),
                evidence=(
                    f"capability_routes={len(capabilities)}; lines={lines}; bytes={size}; "
                    f"route_limit={CONCENTRATION_ROUTE_LIMIT}"
                ),
            )
        )
    return findings


def _valid_living_disposition(text: str) -> bool:
    match = LIVING_DISPOSITION.search(text)
    if match is None:
        return False
    value = match.group(1).strip()
    rationale = (match.group(2) or "").strip()
    if value == "updated":
        return True
    return value in {"no-update-needed", "follow-up"} and bool(rationale)


def _closeout_findings(root: Path, files: list[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in files:
        relative = _relative(root, path)
        if not relative.startswith("docs/changes/") or path.name != "tasks.md":
            continue
        text = _read_text(path)
        if text is None or not CHECKBOX.search(text) or UNCHECKED.search(text):
            continue
        if _valid_living_disposition(text):
            continue
        findings.append(
            Finding(
                code="change-closeout-undispositioned",
                level="review",
                path=relative,
                evidence="completed checklist lacks a valid living-document closeout disposition",
            )
        )
    return findings


def _placeholder_findings(root: Path, scoped_files: set[Path] | None = None) -> list[Finding]:
    substantive = any(
        (root / name).is_dir()
        for name in ("app", "apps", "cmd", "crates", "lib", "packages", "services", "src")
    )
    if not substantive:
        return []
    findings: list[Finding] = []
    for relative, placeholder in PLACEHOLDERS.items():
        path = root / relative
        if scoped_files is not None and path.resolve() not in scoped_files:
            continue
        if not path.is_file():
            findings.append(
                Finding(
                    code="knowledge-owner-placeholder",
                    level="review",
                    path=relative,
                    evidence="required knowledge owner is missing beside substantive project material",
                )
            )
            continue
        text = _read_text(path)
        if text is not None and placeholder in text:
            findings.append(
                Finding(
                    code="knowledge-owner-placeholder",
                    level="review",
                    path=relative,
                    evidence="initial owner placeholder remains beside substantive project material",
                )
            )
    return findings


def audit(
    root: Path,
    requested_paths: list[str] | None,
    repo_wide: bool,
) -> tuple[list[Finding], dict[str, object]]:
    files, skipped = _resolve_scope(root, requested_paths, repo_wide)
    findings = _size_findings(root, files, repo_wide)
    docs_in_scope = repo_wide or any(
        _relative(root, path).startswith("docs/") for path in files
    )
    if docs_in_scope:
        scoped_files = None if repo_wide else {path.resolve() for path in files}
        findings.extend(_orphan_findings(root, scoped_files))
        findings.extend(_concentration_findings(root, scoped_files))
        findings.extend(_placeholder_findings(root, scoped_files))
    findings.extend(_closeout_findings(root, files))
    unique = sorted(set(findings))
    scope = {
        "mode": "repo-wide" if repo_wide else "scoped",
        "requested_paths": [] if repo_wide else list(requested_paths or []),
        "inspected_files": len(files),
        "skipped_paths": skipped,
    }
    return unique, scope


def _render_text(findings: list[Finding], scope: dict[str, object]) -> str:
    lines = [
        (
            f"Audit scope: {scope['mode']}; inspected_files={scope['inspected_files']}; "
            f"skipped={len(scope['skipped_paths'])}"
        )
    ]
    if not findings:
        if scope["inspected_files"] == 0:
            lines.append("No eligible files were inspected.")
        else:
            lines.append("No advisory maintainability signals in inspected scope.")
        return "\n".join(lines)
    lines.extend(
        f"{finding.level} {finding.code} {finding.path}: {finding.evidence}"
        for finding in findings
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Collect advisory code and living-knowledge maintainability signals."
    )
    parser.add_argument("root", nargs="?", default=".", help="Repository root (default: current directory).")
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--path", action="append", dest="paths", help="Repository-relative path to inspect; repeatable.")
    scope.add_argument("--repo-wide", action="store_true", help="Explicitly inspect the whole repository.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        parser.error(f"repository root is not a directory: {root}")
    try:
        findings, inspected_scope = audit(root, args.paths, args.repo_wide)
    except ValueError as exc:
        parser.error(str(exc))

    if args.format == "json":
        print(
            json.dumps(
                {
                    "scope": inspected_scope,
                    "findings": [asdict(finding) for finding in findings],
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print(_render_text(findings, inspected_scope))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
