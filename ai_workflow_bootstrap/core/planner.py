from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .composer import CompositionConflict, compose_ensured_lines, compose_make_targets
from .lifecycle import (
    COMPOSED,
    MANAGED,
    MIGRATED,
    PROJECT,
    SEEDED,
    classify_rendered_file,
    content_hash,
    is_content_hash,
)
from .renderer import render_template
from .scanner import RepoProfile, format_commands, format_detected_stack, format_repo_layout
from .template_pack import TemplateCompositionSpec, TemplatePack


@dataclass
class WriteResult:
    path: Path
    status: str
    message: str
    kind: str = "file"
    content: str = ""
    template: str = ""
    template_hash: str = ""
    existing: bool = False
    ownership: str = "bootstrap"
    lifecycle: str = MANAGED


@dataclass
class BootstrapPlan:
    target: Path
    profile: RepoProfile
    pack: TemplatePack
    results: list[WriteResult]
    enabled_workflows: list[str]
    enabled_groups: set[str]
    force: bool
    dry_run: bool
    managed_only: bool = False
    reset_project_knowledge: bool = False


def _resolve_repo_path(target: Path, raw_path: str) -> Path:
    relative = Path(raw_path)
    if relative.is_absolute() or raw_path.startswith("~") or ".." in relative.parts:
        raise ValueError(f"Template path must stay inside the target repository: {raw_path}")
    path = target / relative
    root = target.resolve()
    resolved = path.resolve() if path.exists() or path.is_symlink() else path.parent.resolve() / path.name
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"Template path must stay inside the target repository: {raw_path}") from exc
    return path


def _matches_stacks(required: tuple[str, ...], profile: RepoProfile) -> bool:
    return set(required).issubset(profile.detected_stacks)


def _render_context(profile: RepoProfile) -> dict[str, object]:
    return {
        "project_name": profile.project_name,
        "repo_name": profile.repo_name,
        "detected_stacks": format_detected_stack(profile),
        "repo_layout": format_repo_layout(profile),
        "commands": format_commands(profile),
    }


def _template_hash(template_text: str) -> str:
    return content_hash(template_text)


def _plan_directory(path: Path) -> WriteResult:
    if path.exists():
        return WriteResult(path=path, status="unchanged", message="directory already exists", kind="directory")
    return WriteResult(path=path, status="written", message="directory created", kind="directory")


def _plan_file(
    path: Path,
    template_path: str,
    template_text: str,
    *,
    force: bool,
    content: str,
    lifecycle: str,
    prior_entry: Mapping[str, Any] | None = None,
    reset_project_knowledge: bool = False,
    overwrite_hint: str = "",
) -> WriteResult:
    existing = path.exists()
    current_hash: str | None = None
    if existing:
        try:
            current = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            current = path.read_text(encoding="utf-8", errors="replace")
        current_hash = content_hash(current)
    prior_hash = (prior_entry or {}).get("applied_content_hash")
    decision = classify_rendered_file(
        lifecycle=lifecycle,
        exists=existing,
        current_hash=current_hash,
        rendered_hash=content_hash(content),
        prior_applied_hash=prior_hash if isinstance(prior_hash, str) else None,
        force=force,
        reset_project_knowledge=reset_project_knowledge,
    )
    messages = {
        "written": "created from bootstrap template",
        "unchanged": "already matches rendered bootstrap content",
        "updated": "untouched seed safely updated to the current template",
        "overwritten": "bootstrap-managed file updated by explicit request",
        "reset": "seeded project knowledge reset by separate explicit request",
        "skipped": "managed file differs; use --force to update it",
        "preserved": (
            "project-evolved seeded knowledge preserved"
            if is_content_hash(prior_hash)
            else "seeded knowledge preserved because applied provenance is unavailable"
        ),
    }
    message = messages[decision.status]
    if existing and overwrite_hint and decision.status in {"skipped", "overwritten"}:
        message += f". {overwrite_hint}"
    return WriteResult(
        path=path,
        status=decision.status,
        message=message,
        content=content,
        template=template_path,
        template_hash=_template_hash(template_text),
        existing=existing,
        lifecycle=lifecycle,
    )


def _plan_obsolete_file(
    path: Path,
    *,
    prior_entry: Mapping[str, Any] | None,
    migration_target: str,
) -> WriteResult | None:
    if not path.exists() and not path.is_symlink():
        return None
    if path.is_file() or path.is_symlink():
        try:
            current = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            return WriteResult(
                path=path,
                status="migration_required",
                message=f"obsolete file cannot be verified safely: {exc}",
                kind="deletion",
                existing=True,
                lifecycle=MIGRATED,
            )
        prior_hash = (prior_entry or {}).get("applied_content_hash")
        if not is_content_hash(prior_hash) or content_hash(current) != prior_hash:
            destination = f" Migrate durable content to {migration_target}." if migration_target else ""
            return WriteResult(
                path=path,
                status="migration_required",
                message=(
                    "obsolete file has project drift or no trusted applied provenance; preserved."
                    + destination
                ),
                kind="deletion",
                existing=True,
                lifecycle=MIGRATED,
            )
        return WriteResult(
            path=path,
            status="deleted",
            message="unchanged obsolete bootstrap file will be deleted",
            kind="deletion",
            existing=True,
            lifecycle=MIGRATED,
        )
    return WriteResult(
        path=path,
        status="migration_required",
        message="obsolete path is not a regular file; refusing recursive deletion",
        kind="deletion",
        existing=True,
        lifecycle=MIGRATED,
    )


def _format_composition_conflict(path: Path, conflict: CompositionConflict) -> str:
    return (
        f"Blocked before writing any files: {path} target {conflict.target!r}. "
        f"{conflict.reason}\nCurrent definition:\n{conflict.current}\n"
        f"Required definition:\n{conflict.required}\n"
        f"To continue: {conflict.remediation} "
        "--force does not bypass repository-owned file conflicts."
    )


def _plan_composition(
    path: Path,
    spec: TemplateCompositionSpec,
    template_text: str,
    content: str,
) -> WriteResult:
    existing = path.exists()
    current = ""
    if existing:
        try:
            current = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            conflict = CompositionConflict(
                target="<file encoding>",
                current="file is not valid UTF-8",
                required="UTF-8 text",
                reason="The repository-owned file cannot be composed safely.",
                remediation="Convert the file to UTF-8 or move it aside, then rerun the bootstrap.",
            )
            return WriteResult(
                path=path,
                status="conflict",
                message=_format_composition_conflict(path, conflict),
                template=spec.template,
                template_hash=_template_hash(template_text),
                existing=True,
                lifecycle=COMPOSED,
            )

    if spec.mode == "make-targets":
        result = compose_make_targets(current, content, spec.marker)
    elif spec.mode == "ensure-lines":
        result = compose_ensured_lines(current, content, spec.equivalent_lines)
    else:
        raise ValueError(f"Unknown composition mode: {spec.mode}")

    if result.conflict:
        return WriteResult(
            path=path,
            status="conflict",
            message=_format_composition_conflict(path, result.conflict),
            template=spec.template,
            template_hash=_template_hash(template_text),
            existing=existing,
            lifecycle=COMPOSED,
        )
    if not result.changed:
        status = "unchanged"
    else:
        status = "updated" if existing else "written"
    return WriteResult(
        path=path,
        status=status,
        message="safely composed" if result.changed else "composed content already satisfied",
        content=result.content,
        template=spec.template,
        template_hash=_template_hash(template_text),
        existing=existing,
        lifecycle=COMPOSED,
    )


def build_plan(
    target: Path,
    *,
    profile: RepoProfile,
    pack: TemplatePack,
    enabled_workflows: list[str],
    enabled_groups: set[str],
    force: bool,
    dry_run: bool,
    prior_files: Mapping[str, Mapping[str, Any]] | None = None,
    managed_only: bool = False,
    reset_project_knowledge: bool = False,
) -> BootstrapPlan:
    results: list[WriteResult] = []
    prior_files = prior_files or {}
    context = _render_context(profile)

    for fragment in pack.context_fragments:
        context.setdefault(fragment.name, "")
        if fragment.group not in enabled_groups or not _matches_stacks(fragment.when_stacks, profile):
            continue
        template_text = pack.read_template(fragment.template)
        context[fragment.name] = render_template(template_text, context).rstrip()

    for directory in pack.directories:
        if directory.group in enabled_groups and _matches_stacks(directory.when_stacks, profile):
            results.append(_plan_directory(_resolve_repo_path(target, directory.path)))

    for spec in pack.files:
        if spec.group not in enabled_groups or not _matches_stacks(spec.when_stacks, profile):
            continue
        if managed_only and spec.lifecycle == SEEDED:
            continue
        template_text = pack.read_template(spec.template)
        content = render_template(template_text, context)
        results.append(
            _plan_file(
                _resolve_repo_path(target, spec.path),
                spec.template,
                template_text,
                force=force,
                content=content,
                lifecycle=spec.lifecycle,
                prior_entry=prior_files.get(Path(spec.path).as_posix()),
                reset_project_knowledge=reset_project_knowledge and spec.lifecycle == SEEDED,
                overwrite_hint=spec.overwrite_hint,
            )
        )

    for spec in pack.project_owned_paths:
        if spec.group not in enabled_groups:
            continue
        path = _resolve_repo_path(target, spec.path)
        if path.exists() or path.is_symlink():
            results.append(
                WriteResult(
                    path=path,
                    status="preserved",
                    message="project-owned instructions preserved; bootstrap will never overwrite this path",
                    existing=True,
                    ownership="project",
                    lifecycle=PROJECT,
                )
            )

    for spec in pack.compositions:
        if spec.group not in enabled_groups or not _matches_stacks(spec.when_stacks, profile):
            continue
        template_text = pack.read_template(spec.template)
        content = render_template(template_text, context)
        path = _resolve_repo_path(target, spec.path)
        results.append(_plan_composition(path, spec, template_text, content))

    if force and not managed_only:
        for spec in pack.obsolete_files:
            if spec.group not in enabled_groups:
                continue
            deletion = _plan_obsolete_file(
                _resolve_repo_path(target, spec.path),
                prior_entry=prior_files.get(Path(spec.path).as_posix()),
                migration_target=spec.migration_target,
            )
            if deletion is not None:
                results.append(deletion)

    return BootstrapPlan(
        target=target,
        profile=profile,
        pack=pack,
        results=results,
        enabled_workflows=enabled_workflows,
        enabled_groups=enabled_groups,
        force=force,
        dry_run=dry_run,
        managed_only=managed_only,
        reset_project_knowledge=reset_project_knowledge,
    )
