#!/usr/bin/env python3
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
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


@dataclass(frozen=True)
class MaintainabilityDisposition:
    code: str
    path: str
    value: str
    rationale: str


@dataclass(frozen=True)
class MaintainabilityCloseout:
    scope: tuple[str, ...]
    dispositions: tuple[MaintainabilityDisposition, ...]
    no_findings: bool
    errors: tuple[str, ...]


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
    value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value.strip())
    value = re.sub(r"[*_~`]", "", value).casefold()
    return "".join(
        "-" if character == " " else character
        for character in value
        if character == " " or character == "-" or character.isalnum()
    )


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


def suggested_fragment(path: Path, fragment: str) -> str | None:
    def folded(value: str) -> str:
        return "".join(
            character
            for character in unicodedata.normalize("NFKD", value)
            if not unicodedata.combining(character)
        )

    matches = [candidate for candidate in heading_fragments(path) if folded(candidate) == fragment]
    return matches[0] if len(matches) == 1 else None


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


def _table_lines(text: str, heading: str, level: int = 2) -> tuple[list[tuple[int, str]], list[str]]:
    section = re.search(
        rf"^{'#' * level} {re.escape(heading)}\s*$\n(.*?)(?=^#{{1,{level}}} |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if section is None:
        return [], [f"missing section {heading!r}"]
    start_line = text[: section.start(1)].count("\n") + 1
    return [
        (start_line + offset, line)
        for offset, line in enumerate(section.group(1).splitlines())
        if line.startswith("|")
    ], []


def _cells(line: str) -> list[str]:
    return [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]


def _is_divider(cells: list[str]) -> bool:
    return bool(cells) and all(cell and set(cell) <= {"-", ":", " "} for cell in cells)


def _is_placeholder(value: str) -> bool:
    normalized = re.sub(r"\s+", " ", value.strip().strip("`_").casefold())
    return normalized in {
        "",
        "—",
        "-",
        "todo",
        "tbd",
        "pending",
        "not reviewed",
        "not established",
        "reason required",
        "pending implementation and scoped audit",
        "pending approved implementation paths",
    }


def _canonical_change_path(root: Path, raw: str) -> tuple[str | None, str | None]:
    path = raw.strip().strip("`")
    pure = PurePosixPath(path)
    if (
        not path
        or unquote(path) != path
        or "\\" in path
        or path.endswith("/")
        or pure.is_absolute()
        or pure.as_posix() != path
        or len(pure.parts) != 3
        or pure.parts[:2] != ("docs", "changes")
        or pure.parts[2] in {"", ".", ".."}
    ):
        return None, f"invalid change path {path!r}"
    candidate = root / path
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError:
        return None, f"invalid change path {path!r}: outside repository"
    if candidate.is_symlink():
        return None, f"invalid change path {path!r}: listed change directory must not be a symlink"
    if not candidate.is_dir():
        return None, f"invalid change path {path!r}: listed change directory does not exist"
    return path, None


def _baseline_table(
    text: str,
    root: Path,
    heading: str,
    header: tuple[str, str, str],
    allowed_value: str,
) -> tuple[list[str], list[str]]:
    lines, errors = _table_lines(text, heading)
    if errors:
        return [], errors
    if len(lines) < 3:
        return [], [f"{heading} requires a header, divider and data row"]
    header_cells = _cells(lines[0][1])
    if tuple(header_cells) != header:
        errors.append(f"{heading} has an invalid table header")
    if len(_cells(lines[1][1])) != 3 or not _is_divider(_cells(lines[1][1])):
        errors.append(f"{heading} has an invalid table divider")

    data = lines[2:]
    sentinel_rows = [line_number for line_number, line in data if _cells(line) == ["_None_", "—", "—"]]
    if sentinel_rows and len(data) != 1:
        errors.append(f"{heading} empty sentinel must be the only data row")
    if sentinel_rows:
        return [], errors

    paths: list[str] = []
    seen: set[str] = set()
    for line_number, line in data:
        cells = _cells(line)
        if len(cells) != 3:
            errors.append(f"{heading} row {line_number} must contain exactly three cells")
            continue
        raw_path, value, evidence = cells
        canonical, path_error = _canonical_change_path(root, raw_path)
        row_valid = True
        if path_error:
            errors.append(f"{path_error} in {heading} row {line_number}")
            row_valid = False
        if value != allowed_value:
            errors.append(
                f"{heading} row {line_number} uses unsupported value {value!r}; expected {allowed_value!r}"
            )
            row_valid = False
        if _is_placeholder(evidence):
            errors.append(f"{heading} row {line_number} requires non-placeholder evidence or rationale")
            row_valid = False
        if canonical is None:
            continue
        if canonical in seen:
            errors.append(f"duplicate change path {canonical!r} in {heading}")
            row_valid = False
        else:
            seen.add(canonical)
        if row_valid:
            paths.append(canonical)
    return paths, errors


def parse_baseline(path: Path) -> Baseline:
    if not path.is_file():
        return Baseline(None, "", frozenset(), frozenset(), ())
    if path.is_symlink():
        return Baseline(None, "", frozenset(), frozenset(), ("baseline file must not be a symlink",))
    text = read_text(path)
    root = path.parent.parent if path.parent.name == "docs" else path.parent
    status = _field(text, "Baseline status")
    evidence = _field(text, "Baseline evidence") or ""
    grandfathered, errors = _baseline_table(
        text,
        root,
        "Grandfathered closeout debt",
        ("Change artifact", "Debt status", "Review evidence or rationale"),
        "unresolved",
    )
    reviewed, reviewed_errors = _baseline_table(
        text,
        root,
        "Reviewed debt dispositions",
        ("Change artifact", "Disposition", "Review evidence or rationale"),
        "reviewed",
    )
    errors.extend(reviewed_errors)
    if status not in {"unestablished", "established"}:
        errors.append("Baseline status must be unestablished or established")
    if status == "established" and _is_placeholder(evidence):
        errors.append("established baseline requires non-placeholder evidence")
    if status == "unestablished" and (grandfathered or reviewed):
        errors.append("unestablished baseline cannot list change paths")
    grandfathered_set = set(grandfathered)
    reviewed_set = set(reviewed)
    overlap = grandfathered_set & reviewed_set
    if overlap:
        errors.append("change paths cannot be both grandfathered and reviewed: " + ", ".join(sorted(overlap)))
    if errors:
        grandfathered_set.clear()
        reviewed_set.clear()
    return Baseline(status, evidence, frozenset(grandfathered_set), frozenset(reviewed_set), tuple(errors))


def _safe_scope_path(root: Path, raw: str, *, must_exist: bool) -> tuple[str | None, str | None]:
    value = raw.strip().strip("`")
    pure = PurePosixPath(value)
    if (
        not value
        or _is_placeholder(value)
        or unquote(value) != value
        or "\\" in value
        or value.endswith("/")
        or pure.is_absolute()
        or pure.as_posix() != value
        or any(part in {"", ".", ".."} for part in pure.parts)
    ):
        return None, f"invalid repository-relative path {value!r}"
    candidate = root / value
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError:
        return None, f"invalid repository-relative path {value!r}: outside repository"
    if candidate.is_symlink():
        return None, f"invalid repository-relative path {value!r}: symlinks are not allowed"
    if must_exist and not candidate.exists():
        return None, f"invalid repository-relative path {value!r}: path does not exist"
    return value, None


def parse_maintainability_closeout(root: Path, tasks: Path) -> MaintainabilityCloseout:
    text = read_text(tasks)
    errors: list[str] = []
    scope_lines, scope_errors = _table_lines(text, "Maintainability audit scope", level=3)
    errors.extend(scope_errors)
    scope: list[str] = []
    if scope_lines:
        if _cells(scope_lines[0][1]) != ["Repository-relative path"]:
            errors.append("Maintainability audit scope has an invalid table header")
        if len(scope_lines) < 3 or len(_cells(scope_lines[1][1])) != 1 or not _is_divider(_cells(scope_lines[1][1])):
            errors.append("Maintainability audit scope has an invalid table divider or no data row")
        seen_scope: set[str] = set()
        for line_number, line in scope_lines[2:]:
            cells = _cells(line)
            if len(cells) != 1:
                errors.append(f"Maintainability audit scope row {line_number} must contain exactly one cell")
                continue
            relative, problem = _safe_scope_path(root, cells[0], must_exist=True)
            if problem:
                errors.append(f"{problem} in maintainability scope row {line_number}")
            elif relative in seen_scope:
                errors.append(f"duplicate maintainability scope path {relative!r}")
            elif relative is not None:
                seen_scope.add(relative)
                scope.append(relative)
    if not scope:
        errors.append("maintainability audit scope requires at least one existing path")

    disposition_lines, disposition_errors = _table_lines(
        text, "Maintainability finding dispositions", level=3
    )
    errors.extend(disposition_errors)
    dispositions: list[MaintainabilityDisposition] = []
    no_findings = False
    if disposition_lines:
        expected_header = ["Finding code", "Path", "Disposition", "Rationale or reference"]
        if _cells(disposition_lines[0][1]) != expected_header:
            errors.append("Maintainability finding dispositions has an invalid table header")
        if (
            len(disposition_lines) < 3
            or len(_cells(disposition_lines[1][1])) != 4
            or not _is_divider(_cells(disposition_lines[1][1]))
        ):
            errors.append("Maintainability finding dispositions has an invalid divider or no data row")
        data = disposition_lines[2:]
        sentinel = ["_None_", "—", "no-findings"]
        seen_findings: set[tuple[str, str]] = set()
        for line_number, line in data:
            cells = _cells(line)
            if len(cells) != 4:
                errors.append(
                    f"Maintainability finding dispositions row {line_number} must contain exactly four cells"
                )
                continue
            code, raw_path, value, rationale = cells
            if cells[:3] == sentinel:
                no_findings = True
                if len(data) != 1:
                    errors.append("no-findings sentinel must be the only disposition row")
                if _is_placeholder(rationale):
                    errors.append("no-findings requires a non-placeholder scoped-audit rationale")
                continue
            if value not in {"resolved", "accepted", "separate-spec"}:
                errors.append(f"unsupported maintainability disposition {value!r} in row {line_number}")
            relative, path_problem = _safe_scope_path(root, raw_path, must_exist=False)
            if path_problem:
                errors.append(f"{path_problem} in maintainability disposition row {line_number}")
            if _is_placeholder(code):
                errors.append(f"maintainability disposition row {line_number} requires a finding code")
            if _is_placeholder(rationale):
                errors.append(
                    f"maintainability disposition {value!r} in row {line_number} requires non-placeholder rationale"
                )
            if value == "separate-spec":
                reference = rationale.strip().strip("`")
                reference_path, reference_problem = _safe_scope_path(root, reference, must_exist=True)
                if (
                    reference_problem
                    or reference_path is None
                    or not reference_path.startswith("docs/changes/")
                    or not reference_path.endswith("/spec.md")
                ):
                    errors.append("separate-spec requires an existing safe spec reference")
            if relative is None or _is_placeholder(code):
                continue
            key = (code, relative)
            if key in seen_findings:
                errors.append(f"duplicate maintainability finding {code!r} at {relative!r}")
                continue
            seen_findings.add(key)
            dispositions.append(MaintainabilityDisposition(code, relative, value, rationale))
    if not dispositions and not no_findings:
        errors.append("maintainability closeout requires finding dispositions or no-findings")
    return MaintainabilityCloseout(tuple(scope), tuple(dispositions), no_findings, tuple(errors))


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
