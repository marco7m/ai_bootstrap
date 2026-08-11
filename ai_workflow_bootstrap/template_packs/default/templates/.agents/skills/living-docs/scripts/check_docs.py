#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from check_links import validate as validate_links
from check_living_docs import check as check_living_docs
from documentation_contract import BASELINE_PATH, parse_baseline, read_text


def _load_audit():
    skills = Path(__file__).resolve().parents[2]
    audit_scripts = skills / "maintainability-audit" / "scripts"
    sys.path.insert(0, str(audit_scripts))
    from audit_repository import audit  # type: ignore[import-not-found]

    return audit


def _maintainability_closeout_problem(root: Path, closeout: str) -> str | None:
    candidate = (root / closeout).resolve()
    tasks = candidate / "tasks.md" if candidate.is_dir() else candidate
    if not tasks.is_file():
        return None
    match = re.search(r"^- Maintainability findings:\s*`?(.+?)`?\s*$", read_text(tasks), re.MULTILINE)
    if match is None or match.group(1).strip(" `").casefold() in {"", "pending", "todo", "tbd"}:
        return (
            f"closeout-maintainability {tasks.relative_to(root)}: record resolved, accepted with rationale, "
            "separate-spec, or no-findings with inspected scope"
        )
    return None


def run(
    root: Path,
    *,
    baseline_ref: str | None = None,
    closeout: str | None = None,
    advisory: bool = False,
) -> tuple[list[str], list[str]]:
    selected = (root / closeout).resolve() if closeout else None
    selected_is_safe = False
    if selected is not None:
        try:
            selected.relative_to((root / "docs/changes").resolve())
        except ValueError:
            pass
        else:
            selected_is_safe = True
    blocking = validate_links(root)
    if selected_is_safe and selected is not None and selected.exists():
        blocking.extend(validate_links(root, include_changes=True, selected_change=selected))
    blocking.extend(check_living_docs(root, baseline_ref, closeout))
    if closeout and selected_is_safe:
        problem = _maintainability_closeout_problem(root, closeout)
        if problem:
            blocking.append(problem)

    observations: list[str] = []
    baseline = parse_baseline(root / BASELINE_PATH)
    if baseline.status in {None, "unestablished"}:
        observations.append(
            f"baseline-unestablished {BASELINE_PATH}: establish reviewed evidence before prospective debt gating"
        )
    if advisory:
        audit = _load_audit()
        requested = [closeout] if closeout else [
            "docs/INDEX.md",
            "docs/CAPABILITIES.md",
            "docs/product",
            "docs/architecture",
            "docs/decisions",
        ]
        existing = [path for path in requested if path and (root / path).exists()]
        findings, scope = audit(root, existing, False)
        observations.append(
            f"audit-scope mode={scope['mode']} inspected_files={scope['inspected_files']}"
        )
        observations.extend(
            f"{finding.level} {finding.code} {finding.path}: {finding.evidence}"
            for finding in findings
        )
    return sorted(set(blocking)), observations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run aggregate stack-independent living-document checks.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root (default: current directory).")
    parser.add_argument("--baseline-ref", help="Optional Git ref for coverage/capability comparison.")
    parser.add_argument("--closeout", help="Repository-relative change directory for targeted closeout.")
    parser.add_argument("--advisory", action="store_true", help="Include scoped advisory maintainability findings.")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    blocking, observations = run(
        root,
        baseline_ref=args.baseline_ref,
        closeout=args.closeout,
        advisory=args.advisory,
    )
    for observation in observations:
        print(f"docs observation: {observation}")
    if blocking:
        for issue in blocking:
            print(f"docs check failed: {issue}", file=sys.stderr)
        return 1
    print("Documentation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
