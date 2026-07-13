#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK_PATTERN = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")


def markdown_links(path: Path) -> list[str]:
    links: list[str] = []
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if not in_fence:
            links.extend(LINK_PATTERN.findall(line))
    return links


def validate(root: Path) -> list[str]:
    docs = root / "docs"
    if not docs.is_dir():
        return [f"Missing documentation directory: {docs}"]

    errors: list[str] = []
    for source in sorted(docs.rglob("*.md")):
        if "changes" in source.relative_to(docs).parts:
            continue
        for raw in markdown_links(source):
            target = raw.strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            parsed = urlsplit(target)
            if not target or target.startswith("#") or parsed.scheme or parsed.netloc:
                continue
            local = unquote(parsed.path)
            if not local:
                continue
            if Path(local).is_absolute():
                errors.append(f"{source.relative_to(root)} -> {raw} (absolute path)")
                continue
            resolved = (source.parent / local).resolve()
            if not resolved.is_relative_to(root.resolve()):
                errors.append(f"{source.relative_to(root)} -> {raw} (outside repository)")
            elif not resolved.exists():
                errors.append(f"{source.relative_to(root)} -> {raw} (missing)")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[4]
    errors = validate(root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("All local Markdown links resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
