#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from documentation_contract import (
    fragment_exists,
    markdown_links,
    resolve_local_target,
    suggested_fragment,
)


def validate(
    root: Path,
    *,
    include_changes: bool = False,
    selected_change: Path | None = None,
) -> list[str]:
    docs = root / "docs"
    if not docs.is_dir():
        return [f"missing-docs {docs}: documentation directory is required"]

    if selected_change is not None:
        sources = sorted(selected_change.rglob("*.md")) if selected_change.is_dir() else [selected_change]
    else:
        sources = sorted(docs.rglob("*.md"))

    errors: list[str] = []
    for source in sources:
        if source.is_symlink():
            errors.append(f"invalid-link-source {source}: Markdown source must not be a symlink")
            continue
        relative_parts = source.relative_to(docs).parts if source.is_relative_to(docs) else ()
        if not include_changes and "changes" in relative_parts:
            continue
        for raw in markdown_links(source):
            try:
                target = resolve_local_target(root, source, raw)
            except ValueError as exc:
                errors.append(f"invalid-link {source.relative_to(root)} -> {raw}: {exc}")
                continue
            if target is None:
                continue
            resolved, fragment = target
            if not resolved.exists():
                errors.append(f"broken-link {source.relative_to(root)} -> {raw}: target does not exist")
            elif fragment and resolved.is_file() and not fragment_exists(resolved, fragment):
                suggestion = suggested_fragment(resolved, fragment)
                hint = f"; expected canonical fragment #{suggestion}" if suggestion else ""
                errors.append(
                    f"broken-fragment {source.relative_to(root)} -> {raw}: "
                    f"fragment does not match a supported ATX heading{hint}"
                )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate local Markdown links and supported fragments.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root (default: current directory).")
    parser.add_argument("--include-changes", action="store_true", help="Also validate temporal change artifacts.")
    parser.add_argument("--change", help="Validate only one repository-relative change directory or Markdown file.")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    selected = (root / args.change).resolve() if args.change else None
    if selected is not None:
        try:
            selected.relative_to(root / "docs/changes")
        except ValueError:
            parser.error("--change must stay under docs/changes")
        if not selected.exists():
            parser.error(f"--change does not exist: {args.change}")
    errors = validate(root, include_changes=args.include_changes, selected_change=selected)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("All selected local Markdown links and supported fragments resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
