from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CompositionConflict:
    target: str
    current: str
    required: str
    reason: str
    remediation: str


@dataclass(frozen=True)
class CompositionResult:
    content: str = ""
    changed: bool = False
    conflict: CompositionConflict | None = None


@dataclass(frozen=True)
class MakeTarget:
    name: str
    prerequisites: str
    recipes: tuple[str, ...]
    raw_lines: tuple[str, ...]
    simple: bool

    def normalized(self) -> str:
        header = f"{self.name}: {' '.join(self.prerequisites.split())}".rstrip()
        recipes = "\n".join(self.recipes)
        return f"{header}\n{recipes}".rstrip()


def _marker_lines(marker: str) -> tuple[str, str]:
    if not marker.strip() or "\n" in marker or "\r" in marker:
        raise ValueError("make-targets composition requires a non-empty marker")
    return (f"# >>> ai-workflow-bootstrap:{marker} >>>", f"# <<< ai-workflow-bootstrap:{marker} <<<")


def _remove_managed_block(text: str, marker: str) -> tuple[str, CompositionConflict | None]:
    begin, end = _marker_lines(marker)
    begin_positions = [match.start() for match in re.finditer(re.escape(begin), text)]
    end_positions = [match.start() for match in re.finditer(re.escape(end), text)]
    if not begin_positions and not end_positions:
        return text, None
    if len(begin_positions) != 1 or len(end_positions) != 1 or begin_positions[0] >= end_positions[0]:
        return "", CompositionConflict(
            target="<managed block>",
            current="malformed or duplicated bootstrap markers",
            required=f"one {begin} / {end} pair",
            reason="The existing managed Make block cannot be identified safely.",
            remediation=(
                "Remove the malformed/duplicated marker lines or restore exactly one valid marker pair, "
                "then rerun the bootstrap. Preserve all Make content outside that pair."
            ),
        )
    start = begin_positions[0]
    finish = end_positions[0] + len(end)
    if finish < len(text) and text[finish] == "\n":
        finish += 1
    return text[:start] + text[finish:], None


def _parse_make_targets(text: str) -> dict[str, list[MakeTarget]]:
    lines = text.splitlines()
    targets: dict[str, list[MakeTarget]] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith(("\t", "#")) or ":" not in line:
            index += 1
            continue
        header, prerequisites = line.split(":", 1)
        names = header.split()
        if not names or any(not re.fullmatch(r"[A-Za-z0-9_.-]+", name) for name in names):
            index += 1
            continue
        raw_lines = [line]
        recipes: list[str] = []
        cursor = index + 1
        while cursor < len(lines) and lines[cursor].startswith("\t"):
            raw_lines.append(lines[cursor])
            recipes.append(lines[cursor][1:].strip())
            cursor += 1
        for name in names:
            if name == ".PHONY":
                continue
            targets.setdefault(name, []).append(
                MakeTarget(
                    name=name,
                    prerequisites=prerequisites.strip(),
                    recipes=tuple(recipes),
                    raw_lines=tuple(raw_lines),
                    simple=len(names) == 1,
                )
            )
        index = max(cursor, index + 1)
    return targets


def _append_managed_block(text: str, block: str) -> str:
    if not block:
        return text
    if not text:
        return block + "\n"
    separator = "" if text.endswith("\n\n") else "\n" if text.endswith("\n") else "\n\n"
    return text + separator + block + "\n"


def compose_make_targets(current: str, required: str, marker: str) -> CompositionResult:
    unmanaged, marker_conflict = _remove_managed_block(current, marker)
    if marker_conflict:
        return CompositionResult(conflict=marker_conflict)

    expected = _parse_make_targets(required)
    existing = _parse_make_targets(unmanaged)
    missing: list[MakeTarget] = []
    for name, expected_items in expected.items():
        if len(expected_items) != 1 or not expected_items[0].simple:
            raise ValueError(f"Managed Make template must define target {name!r} exactly once")
        wanted = expected_items[0]
        found = existing.get(name, [])
        if not found:
            missing.append(wanted)
            continue
        if len(found) == 1 and found[0].simple and found[0].normalized() == wanted.normalized():
            continue
        current_text = "\n\n".join(item.normalized() for item in found) or "ambiguous target definition"
        return CompositionResult(
            conflict=CompositionConflict(
                target=name,
                current=current_text,
                required=wanted.normalized(),
                reason="An unmanaged Make target uses a required name with a different recipe.",
                remediation=(
                    "Edit the existing target to match the required definition, or remove/rename it so the "
                    "bootstrap can manage that name, then rerun the bootstrap."
                ),
            )
        )

    begin, end = _marker_lines(marker)
    if missing:
        body = [begin, f".PHONY: {' '.join(item.name for item in missing)}", ""]
        for position, item in enumerate(missing):
            body.extend(item.raw_lines)
            if position < len(missing) - 1:
                body.append("")
        body.append(end)
        composed = _append_managed_block(unmanaged, "\n".join(body))
    else:
        composed = unmanaged
    return CompositionResult(content=composed, changed=composed != current)


def compose_ensured_lines(current: str, required: str, equivalent_lines: tuple[str, ...] = ()) -> CompositionResult:
    existing = {line.strip() for line in current.splitlines() if line.strip()}
    equivalents = {line.strip() for line in equivalent_lines if line.strip()}
    required_lines = [line.strip() for line in required.splitlines() if line.strip()]
    if equivalents and len(required_lines) != 1:
        raise ValueError("equivalent_lines requires exactly one non-empty ensured line")
    missing = []
    for normalized in required_lines:
        if normalized in existing:
            continue
        if equivalents & existing:
            continue
        missing.append(normalized)
    if not missing:
        return CompositionResult(content=current, changed=False)
    prefix = current
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    content = prefix + "\n".join(missing) + "\n"
    return CompositionResult(content=content, changed=True)
