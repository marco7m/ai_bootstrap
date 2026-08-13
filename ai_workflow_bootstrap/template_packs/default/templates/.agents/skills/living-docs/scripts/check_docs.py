#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from check_links import validate as validate_links
from check_living_docs import check as check_living_docs
from documentation_contract import (
    BASELINE_PATH,
    parse_baseline,
    parse_maintainability_closeout,
)


def _load_audit():
    skills = Path(__file__).resolve().parents[2]
    audit_scripts = skills / "maintainability-audit" / "scripts"
    sys.path.insert(0, str(audit_scripts))
    from audit_repository import audit  # type: ignore[import-not-found]

    return audit


def _maintainability_closeout_problems(root: Path, closeout: str, audit):
    candidate = (root / closeout).resolve()
    tasks = candidate / "tasks.md" if candidate.is_dir() else candidate
    if not tasks.is_file():
        return [], [], None
    parsed = parse_maintainability_closeout(root, tasks)
    problems = [
        f"closeout-maintainability {tasks.relative_to(root)}: {error}"
        for error in parsed.errors
    ]
    if not parsed.scope:
        return problems, [], None

    findings, scope = audit(root, list(parsed.scope), False)
    current = {(finding.code, finding.path): finding for finding in findings}
    declared = {(item.code, item.path): item for item in parsed.dispositions}

    if parsed.no_findings and current:
        problems.append(
            f"closeout-maintainability {tasks.relative_to(root)}: "
            "no-findings cannot close a scope with current findings"
        )
    for key, finding in current.items():
        item = declared.get(key)
        if item is None:
            problems.append(
                f"closeout-maintainability {tasks.relative_to(root)}: "
                f"current finding {finding.code!r} at {finding.path!r} lacks a disposition"
            )
        elif item.value == "resolved":
            problems.append(
                f"closeout-maintainability {tasks.relative_to(root)}: "
                f"resolved finding is still present: {finding.code!r} at {finding.path!r}"
            )
    for key, item in declared.items():
        if item.value in {"accepted", "separate-spec"} and key not in current:
            problems.append(
                f"closeout-maintainability {tasks.relative_to(root)}: "
                f"{item.value} disposition has no current matching finding: {item.code!r} at {item.path!r}"
            )
    return problems, findings, scope


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
    observations: list[str] = []
    baseline = parse_baseline(root / BASELINE_PATH)
    if baseline.status in {None, "unestablished"}:
        observations.append(
            f"baseline-unestablished {BASELINE_PATH}: establish reviewed evidence before prospective debt gating"
        )
    audit = _load_audit() if advisory or (closeout and selected_is_safe) else None
    closeout_audit = False
    if closeout and selected_is_safe and audit is not None:
        problems, findings, scope = _maintainability_closeout_problems(root, closeout, audit)
        blocking.extend(problems)
        if scope is not None:
            closeout_audit = True
            observations.append(
                f"audit-scope mode={scope['mode']} inspected_files={scope['inspected_files']}"
            )
            observations.extend(
                f"{finding.level} {finding.code} {finding.path}: {finding.evidence}"
                for finding in findings
            )
    if advisory and not closeout_audit and audit is not None:
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
