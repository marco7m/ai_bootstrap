from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from .renderer import render_template
from .scanner import RepoProfile, format_commands, format_detected_stack, format_repo_layout
from .template_pack import TemplatePack


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
    needs_backup: bool = False


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
    backup_existing: bool


def _resolve_output_path(target: Path, raw_path: str) -> Path:
    if raw_path.startswith("~"):
        return Path(raw_path).expanduser()
    return target / raw_path


def _render_context(profile: RepoProfile) -> dict[str, object]:
    return {
        "project_name": profile.project_name,
        "repo_name": profile.repo_name,
        "detected_stacks": format_detected_stack(profile),
        "repo_layout": format_repo_layout(profile),
        "commands": format_commands(profile),
    }


def _template_hash(template_text: str) -> str:
    return hashlib.sha256(template_text.encode("utf-8")).hexdigest()


def _plan_directory(path: Path) -> WriteResult:
    if path.exists():
        return WriteResult(path=path, status="unchanged", message="directory already exists", kind="directory")
    return WriteResult(path=path, status="written", message="directory created", kind="directory")


def _plan_file(path: Path, template_path: str, template_text: str, *, force: bool, content: str) -> WriteResult:
    existing = path.exists()
    if existing:
        try:
            current = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            current = path.read_text(encoding="utf-8", errors="replace")
        normalized_current = current.rstrip() + "\n"
        if normalized_current == content:
            return WriteResult(
                path=path,
                status="unchanged",
                message="already up to date",
                content=content,
                template=template_path,
                template_hash=_template_hash(template_text),
                existing=True,
            )
        if not force:
            return WriteResult(
                path=path,
                status="skipped",
                message="exists; use --force to overwrite",
                content=content,
                template=template_path,
                template_hash=_template_hash(template_text),
                existing=True,
            )
    return WriteResult(
        path=path,
        status="overwritten" if existing else "written",
        message="overwritten; backup will be created" if existing else "created/updated",
        content=content,
        template=template_path,
        template_hash=_template_hash(template_text),
        existing=existing,
        needs_backup=existing and force,
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
    backup_existing: bool,
) -> BootstrapPlan:
    results: list[WriteResult] = []
    context = _render_context(profile)

    for directory in pack.directories:
        if directory.group in enabled_groups:
            results.append(_plan_directory(_resolve_output_path(target, directory.path)))

    for spec in pack.files:
        if spec.group not in enabled_groups:
            continue
        template_text = pack.read_template(spec.template)
        content = render_template(template_text, context)
        results.append(_plan_file(_resolve_output_path(target, spec.path), spec.template, template_text, force=force, content=content))

    return BootstrapPlan(
        target=target,
        profile=profile,
        pack=pack,
        results=results,
        enabled_workflows=enabled_workflows,
        enabled_groups=enabled_groups,
        force=force,
        dry_run=dry_run,
        backup_existing=backup_existing,
    )
