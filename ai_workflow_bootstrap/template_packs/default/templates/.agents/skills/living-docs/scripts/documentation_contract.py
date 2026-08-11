#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK_PATTERN = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
ATX_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
CAPABILITY_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CHECKBOX = re.compile(r"^- \[[ xX]\]", re.MULTILINE)
UNCHECKED = re.compile(r"^- \[ \]", re.MULTILINE)
LIVING_DISPOSITION = re.compile(
    r"^- Living documentation:[ \t]*`([^`]+)`(?:[ \t]*[—–:-][ \t]*(.+))?[ \t]*$",
    re.MULTILINE,
)
LIVING_RATIONALE = re.compile(
    r"^- Living documentation rationale:\s*`?(.+?)`?\s*$",
    re.MULTILINE,
)

VALID_CAPABILITY_STATES = {
    "unknown",
    "absent",
    "partial",
    "implemented",
    "verified",
    "deprecated",
}
CANONICAL_INDEX = "docs/INDEX.md"
BASELINE_PATH = "docs/LIVING_DOCUMENTATION_BASELINE.md"
RESERVED_RATIONALES = {
    "",
    "todo",
    "tbd",
    "pending",
    "reason required",
    "no docs",
    "_reason required_",
    "_explain why no living owner changed_",
}


@dataclass(frozen=True)
class CapabilityRow:
    name: str
    product_link: str | None
    architecture_link: str | None
    state: str
    evidence: str
    approved_target: str
    active_change: str


@dataclass(frozen=True)
class Baseline:
    status: str | None
    evidence: str
    grandfathered: frozenset[str]
    reviewed: frozenset[str]
    errors: tuple[str, ...]


@dataclass(frozen=True)
class CloseoutDisposition:
    value: str | None
    rationale: str
    valid: bool
    problem: str


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def markdown_links(path: Path) -> list[str]:
    links: list[str] = []
    in_fence = False
    for line in read_text(path).splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if not in_fence:
            links.extend(LINK_PATTERN.findall(line))
    return links


def resolve_local_target(root: Path, source: Path, raw_target: str) -> tuple[Path, str] | None:
    target = raw_target.strip().strip("<>")
    parsed = urlsplit(target)
    if not target or parsed.scheme or parsed.netloc:
        return None
    local = unquote(parsed.path)
    if not local:
        return source.resolve(), unquote(parsed.fragment)
    if Path(local).is_absolute():
        raise ValueError("absolute path")
    resolved = (source.parent / local).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("outside repository") from exc
    if resolved.is_dir():
        resolved /= "README.md"
    return resolved, unquote(parsed.fragment)


def heading_slug(value: str) -> str:
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value.strip()).casefold()
    value = "".join(character for character in value if character.isalnum() or character in " _-")
    return re.sub(r"[\s_]+", "-", value).strip("-")


def heading_fragments(path: Path) -> set[str]:
    fragments: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    for line in read_text(path).splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = ATX_HEADING.match(stripped)
        if match is None:
            continue
        base = heading_slug(match.group(1))
        if not base:
            continue
        duplicate = counts.get(base, 0)
        counts[base] = duplicate + 1
        fragments.add(base if duplicate == 0 else f"{base}-{duplicate}")
    return fragments


def fragment_exists(path: Path, fragment: str) -> bool:
    return not fragment or fragment in heading_fragments(path)


def parse_capability_rows(text: str) -> list[CapabilityRow]:
    rows: list[CapabilityRow] = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7 or cells[0] in {"Capability", "---", "_Capability_"}:
            continue
        product = CAPABILITY_LINK.search(cells[1])
        architecture = CAPABILITY_LINK.search(cells[2])
        rows.append(
            CapabilityRow(
                name=cells[0],
                product_link=product.group(1) if product else None,
                architecture_link=architecture.group(1) if architecture else None,
                state=cells[3].strip("`"),
                evidence=cells[4],
                approved_target=cells[5],
                active_change=cells[6],
            )
        )
    return rows


def knowledge_status(text: str) -> str | None:
    for status in ("scaffold", "incomplete", "baselined"):
        if f"Knowledge status: `{status}`" in text:
            return status
    return None


def is_completed_tasks(text: str) -> bool:
    return bool(CHECKBOX.search(text)) and not bool(UNCHECKED.search(text))


def closeout_disposition(text: str) -> CloseoutDisposition:
    match = LIVING_DISPOSITION.search(text)
    if match is None:
        return CloseoutDisposition(None, "", False, "living-document disposition is absent")
    value = match.group(1).strip()
    rationale = (match.group(2) or "").strip()
    if not rationale:
        rationale_match = LIVING_RATIONALE.search(text)
        rationale = (rationale_match.group(1).strip(" `") if rationale_match else "")
    if value == "updated":
        return CloseoutDisposition(value, rationale, True, "")
    if value != "no-update-needed":
        return CloseoutDisposition(value, rationale, False, f"unsupported closed disposition {value!r}")
    normalized = re.sub(r"\s+", " ", rationale.casefold()).strip()
    placeholder = normalized in RESERVED_RATIONALES or (
        normalized.startswith("_") and normalized.endswith("_")
    )
    if placeholder:
        return CloseoutDisposition(value, rationale, False, "no-update-needed requires a specific rationale")
    return CloseoutDisposition(value, rationale, True, "")


def _field(text: str, label: str) -> str | None:
    match = re.search(rf"^- {re.escape(label)}:\s*`?(.+?)`?\s*$", text, re.MULTILINE)
    return match.group(1).strip(" `") if match else None


def _table_paths(text: str, heading: str) -> tuple[set[str], list[str]]:
    section = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if section is None:
        return set(), [f"missing section {heading!r}"]
    paths: set[str] = set()
    errors: list[str] = []
    for line in section.group(1).splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if not cells or cells[0] in {"Change", "Change artifact", "---", "_None_", "—"}:
            continue
        path = cells[0].removeprefix("./")
        candidate = Path(path)
        if candidate.is_absolute() or ".." in candidate.parts or not path.startswith("docs/changes/"):
            errors.append(f"invalid change path {path!r} in {heading}")
            continue
        paths.add(candidate.as_posix())
    return paths, errors


def parse_baseline(path: Path) -> Baseline:
    if not path.is_file():
        return Baseline(None, "", frozenset(), frozenset(), ())
    if path.is_symlink():
        return Baseline(None, "", frozenset(), frozenset(), ("baseline file must not be a symlink",))
    text = read_text(path)
    status = _field(text, "Baseline status")
    evidence = _field(text, "Baseline evidence") or ""
    grandfathered, errors = _table_paths(text, "Grandfathered closeout debt")
    reviewed, reviewed_errors = _table_paths(text, "Reviewed debt dispositions")
    errors.extend(reviewed_errors)
    if status not in {"unestablished", "established"}:
        errors.append("Baseline status must be unestablished or established")
    if status == "established" and evidence.casefold() in {
        "",
        "not established",
        "_not established_",
        "todo",
        "tbd",
    }:
        errors.append("established baseline requires non-placeholder evidence")
    overlap = grandfathered & reviewed
    if overlap:
        errors.append("change paths cannot be both grandfathered and reviewed: " + ", ".join(sorted(overlap)))
    return Baseline(status, evidence, frozenset(grandfathered), frozenset(reviewed), tuple(errors))


def reachable_markdown(root: Path) -> set[Path]:
    index = (root / CANONICAL_INDEX).resolve()
    pending = [index] if index.is_file() else []
    reachable: set[Path] = set()
    while pending:
        current = pending.pop()
        if current in reachable or current.is_symlink():
            continue
        reachable.add(current)
        for raw_target in markdown_links(current):
            try:
                target = resolve_local_target(root, current, raw_target)
            except ValueError:
                continue
            if target is None:
                continue
            path, _ = target
            if path.is_file() and path.suffix.lower() == ".md" and path not in reachable:
                pending.append(path)
    return reachable
