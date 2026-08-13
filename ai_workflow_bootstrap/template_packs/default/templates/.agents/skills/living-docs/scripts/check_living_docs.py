#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from documentation_contract import (
    BASELINE_PATH,
    VALID_CAPABILITY_STATES,
    closeout_disposition,
    fragment_exists,
    is_completed_tasks,
    knowledge_status,
    parse_baseline,
    parse_capability_rows,
    reachable_markdown,
    read_text,
    resolve_local_target,
    suggested_fragment,
)

SEEDED_OWNERS = {
    "docs/INDEX.md",
    "docs/CAPABILITIES.md",
    "docs/product/README.md",
    "docs/architecture/README.md",
    "docs/decisions/README.md",
    "docs/ROADMAP.md",
    "docs/IDEA_INBOX.md",
    "docs/GLOSSARY.md",
    BASELINE_PATH,
}
SOURCE_DIRS = {"src", "app", "apps", "lib", "crates", "packages", "services", "cmd", "internal"}
OWNER_PLACEHOLDERS = {
    "docs/product/README.md": "Describe the problem, desired outcome",
    "docs/architecture/README.md": "Document the smallest useful current view",
}


def _git_text(root: Path, ref: str, relative: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{ref}:{relative}"],
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def _current_owner_pages(root: Path):
    for area in ("product", "architecture", "decisions"):
        directory = root / "docs" / area
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.md")):
            if path.name not in {"README.md", "_template.md"}:
                yield path.resolve()


def _route_problem(root: Path, source: Path, raw: str | None, area: str) -> str | None:
    if raw is None:
        return f"missing {area} owner link"
    try:
        target = resolve_local_target(root, source, raw)
    except ValueError as exc:
        return str(exc)
    if target is None:
        return "external links cannot own current capability knowledge"
    path, fragment = target
    if not path.is_file():
        return "target does not exist"
    expected = (root / "docs" / area).resolve()
    try:
        path.relative_to(expected)
    except ValueError:
        return f"target must stay under docs/{area}"
    if fragment and not fragment_exists(path, fragment):
        suggestion = suggested_fragment(path, fragment)
        hint = f"; expected canonical fragment #{suggestion}" if suggestion else ""
        return f"fragment does not match a supported ATX heading{hint}"
    return None


def _change_closeout_issues(root: Path, baseline) -> list[str]:
    if baseline.status != "established":
        return []
    issues: list[str] = []
    for relative in sorted(baseline.grandfathered | baseline.reviewed):
        if not (root / relative).is_dir():
            issues.append(f"baseline-stale {BASELINE_PATH}: listed change does not exist: {relative}")
    changes = root / "docs/changes"
    if not changes.is_dir():
        return issues
    exempt = baseline.grandfathered | baseline.reviewed
    for tasks in sorted(changes.glob("*/tasks.md")):
        relative_change = tasks.parent.relative_to(root).as_posix()
        text = read_text(tasks)
        if not is_completed_tasks(text) or relative_change in exempt:
            continue
        disposition = closeout_disposition(text)
        if not disposition.valid:
            issues.append(
                f"new-closeout-debt {tasks.relative_to(root)}: {disposition.problem}; "
                "use updated or justified no-update-needed"
            )
    return issues


def check(
    root: Path,
    baseline_ref: str | None = None,
    closeout_change: str | None = None,
) -> list[str]:
    issues: list[str] = []
    index_path = root / "docs/INDEX.md"
    capability_path = root / "docs/CAPABILITIES.md"
    index = read_text(index_path)
    capability_text = read_text(capability_path)
    product = read_text(root / "docs/product/README.md")
    architecture = read_text(root / "docs/architecture/README.md")
    rows = parse_capability_rows(capability_text)
    verified = {row.name for row in rows if row.state == "verified"}

    if verified and (
        knowledge_status(index) == "scaffold" or "Baseline evidence: _not established_" in index
    ):
        issues.append("coverage-regression docs/INDEX.md: scaffold/unestablished coverage has verified capabilities")

    for relative, placeholder in OWNER_PLACEHOLDERS.items():
        if rows and placeholder in read_text(root / relative):
            issues.append(f"owner-placeholder {relative}: initial placeholder remains beside active capabilities")

    repo_area_lines = [line.strip()[2:].strip("`") for line in architecture.splitlines() if line.startswith("- `")]
    substantive_dirs = SOURCE_DIRS & {path.name for path in root.iterdir() if path.is_dir()}
    if substantive_dirs and repo_area_lines and all(area.startswith("docs/") for area in repo_area_lines):
        issues.append("architecture-placeholder docs/architecture/README.md: architecture lists only documentation beside source")

    state_path = root / ".ai-bootstrap/state.json"
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            issues.append(f"state-invalid .ai-bootstrap/state.json: {exc}")
        else:
            files = state.get("files", {}) if isinstance(state, dict) else {}
            if isinstance(files, dict):
                overwritten = sorted(
                    path
                    for path in SEEDED_OWNERS
                    if isinstance(files.get(path), dict) and files[path].get("status") == "overwritten"
                )
                if overwritten and "Bootstrap recovery audit:" not in index:
                    issues.append(
                        "seeded-owner-overwrite .ai-bootstrap/state.json: overwritten seeded owners: "
                        + ", ".join(overwritten)
                    )

    for row in rows:
        if row.state not in VALID_CAPABILITY_STATES:
            issues.append(f"capability-state {capability_path.relative_to(root)}: {row.name!r} uses {row.state!r}")
        for area, raw in (("product", row.product_link), ("architecture", row.architecture_link)):
            problem = _route_problem(root, capability_path, raw, area)
            if problem:
                issues.append(f"capability-route {capability_path.relative_to(root)}: {row.name!r} {area}: {problem}")
        if row.evidence in {"", "_Evidence_"}:
            issues.append(f"capability-evidence {capability_path.relative_to(root)}: {row.name!r} lacks evidence or explicit gap")

    reachable = reachable_markdown(root)
    for path in _current_owner_pages(root):
        if path not in reachable:
            issues.append(f"orphan-current-owner {path.relative_to(root)}: not reachable from docs/INDEX.md")

    baseline = parse_baseline(root / BASELINE_PATH)
    issues.extend(f"baseline-invalid {BASELINE_PATH}: {error}" for error in baseline.errors)
    issues.extend(_change_closeout_issues(root, baseline))

    if closeout_change:
        candidate = (root / closeout_change).resolve()
        try:
            candidate.relative_to((root / "docs/changes").resolve())
        except ValueError:
            issues.append(f"closeout-path {closeout_change}: must stay under docs/changes")
        else:
            tasks = candidate / "tasks.md" if candidate.is_dir() else candidate
            if not tasks.is_file() or tasks.name != "tasks.md":
                issues.append(f"closeout-path {closeout_change}: tasks.md does not exist")
            else:
                disposition = closeout_disposition(read_text(tasks))
                if not disposition.valid:
                    issues.append(
                        f"closeout-invalid {tasks.relative_to(root)}: {disposition.problem}; "
                        "use updated or justified no-update-needed"
                    )

    if baseline_ref:
        previous_index = _git_text(root, baseline_ref, "docs/INDEX.md")
        previous_capabilities = _git_text(root, baseline_ref, "docs/CAPABILITIES.md")
        if previous_index is None or previous_capabilities is None:
            issues.append(f"git-baseline {baseline_ref!r}: index or capabilities could not be read")
        else:
            rank = {"scaffold": 0, "incomplete": 1, "baselined": 2, None: -1}
            previous_status = knowledge_status(previous_index)
            current_status = knowledge_status(index)
            if rank[current_status] < rank[previous_status]:
                issues.append(
                    f"coverage-downgrade docs/INDEX.md: downgraded from {previous_status} to {current_status}"
                )
            old_rows = {row.name: row.state for row in parse_capability_rows(previous_capabilities)}
            current_rows = {row.name: row.state for row in rows}
            for name, old_state in old_rows.items():
                if name not in current_rows:
                    issues.append(
                        f"capability-removed docs/CAPABILITIES.md: capability removed since {baseline_ref}: {name}"
                    )
                elif old_state == "verified" and current_rows[name] not in {"verified", "deprecated"}:
                    issues.append(f"capability-downgrade docs/CAPABILITIES.md: {name}")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect objective living-document regressions.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root (default: current directory).")
    parser.add_argument("--baseline-ref", help="Optional Git ref for coverage/capability comparison.")
    parser.add_argument("--closeout", help="Repository-relative change directory for targeted closeout.")
    args = parser.parse_args(argv)
    issues = check(Path(args.root).resolve(), args.baseline_ref, args.closeout)
    if issues:
        for issue in issues:
            print(f"living-doc regression: {issue}", file=sys.stderr)
        return 1
    print("No objective living-document regressions detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
