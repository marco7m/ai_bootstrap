#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SEEDED_OWNERS = {
    "docs/INDEX.md",
    "docs/CAPABILITIES.md",
    "docs/product/README.md",
    "docs/architecture/README.md",
    "docs/decisions/README.md",
    "docs/ROADMAP.md",
    "docs/IDEA_INBOX.md",
    "docs/GLOSSARY.md",
}
VALID_STATES = {"unknown", "absent", "partial", "implemented", "verified", "deprecated"}
SOURCE_DIRS = {"src", "app", "apps", "lib", "crates", "packages", "services", "cmd", "internal"}


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _knowledge_status(text: str) -> str | None:
    for status in ("scaffold", "incomplete", "baselined"):
        if f"Knowledge status: `{status}`" in text:
            return status
    return None


def _capabilities(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7 or cells[0] in {"Capability", "---", "_Capability_"}:
            continue
        state = cells[3].strip("`")
        rows[cells[0]] = state
    return rows


def _git_text(root: Path, ref: str, relative: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(root), "show", f"{ref}:{relative}"],
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def check(root: Path, baseline_ref: str | None = None) -> list[str]:
    issues: list[str] = []
    index = _read(root / "docs/INDEX.md")
    capability_text = _read(root / "docs/CAPABILITIES.md")
    product = _read(root / "docs/product/README.md")
    architecture = _read(root / "docs/architecture/README.md")
    capabilities = _capabilities(capability_text)
    verified = {name for name, state in capabilities.items() if state == "verified"}

    if verified and (
        _knowledge_status(index) == "scaffold" or "Baseline evidence: _not established_" in index
    ):
        issues.append("knowledge coverage is scaffold/unestablished while verified capabilities exist")

    active_rows = {name for name in capabilities if not name.startswith("_")}
    if active_rows and "Describe the problem, desired outcome" in product:
        issues.append("product owner still contains the initial purpose placeholder beside active capabilities")
    if active_rows and "Document the smallest useful current view" in architecture:
        issues.append("architecture owner still contains the initial architecture placeholder beside active capabilities")

    repo_area_lines = [line.strip()[2:].strip("`") for line in architecture.splitlines() if line.startswith("- `")]
    substantive_dirs = SOURCE_DIRS & {path.name for path in root.iterdir() if path.is_dir()}
    if substantive_dirs and repo_area_lines and all(area.startswith("docs/") for area in repo_area_lines):
        issues.append("architecture lists only documentation although substantive source directories exist")

    state_path = root / ".ai-bootstrap/state.json"
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            issues.append(f"bootstrap state cannot be inspected: {exc}")
        else:
            files = state.get("files", {}) if isinstance(state, dict) else {}
            if isinstance(files, dict):
                overwritten = sorted(
                    path
                    for path in SEEDED_OWNERS
                    if isinstance(files.get(path), dict) and files[path].get("status") == "overwritten"
                )
                recovery_recorded = "Bootstrap recovery audit:" in index
                if overwritten and not recovery_recorded:
                    issues.append(
                        "legacy bootstrap state reports overwritten seeded owners: " + ", ".join(overwritten)
                    )

    for name, state in capabilities.items():
        if state not in VALID_STATES:
            issues.append(f"capability {name!r} uses invalid current state {state!r}")
    for line in capability_text.splitlines():
        if line.startswith("|") and "_Relative link" in line:
            issues.append("active capability map contains placeholder contract links")

    if baseline_ref:
        previous_index = _git_text(root, baseline_ref, "docs/INDEX.md")
        previous_capabilities = _git_text(root, baseline_ref, "docs/CAPABILITIES.md")
        if previous_index is None or previous_capabilities is None:
            issues.append(f"Git baseline {baseline_ref!r} could not be read")
        else:
            rank = {"scaffold": 0, "incomplete": 1, "baselined": 2, None: -1}
            previous_status = _knowledge_status(previous_index)
            current_status = _knowledge_status(index)
            if rank[current_status] < rank[previous_status]:
                issues.append(
                    f"knowledge coverage downgraded from {previous_status} to {current_status}"
                )
            old_rows = _capabilities(previous_capabilities)
            for name, old_state in old_rows.items():
                if name not in capabilities:
                    issues.append(f"capability removed since {baseline_ref}: {name}")
                elif old_state == "verified" and capabilities[name] not in {"verified", "deprecated"}:
                    issues.append(
                        f"verified capability lost verified/deprecated disposition since {baseline_ref}: {name}"
                    )
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect objective living-document regressions.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root (default: current directory).")
    parser.add_argument("--baseline-ref", help="Optional Git ref used for coverage/capability comparison.")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    issues = check(root, args.baseline_ref)
    if issues:
        for issue in issues:
            print(f"living-doc regression: {issue}", file=sys.stderr)
        return 1
    print("No objective living-document regressions detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
