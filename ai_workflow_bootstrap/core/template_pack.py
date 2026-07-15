from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path
from typing import Any

from .lifecycle import COMPOSED, MANAGED, MIGRATED, PROJECT, RENDERED_FILE_LIFECYCLES


@dataclass(frozen=True)
class TemplateDirectorySpec:
    path: str
    group: str = "core"
    when_stacks: tuple[str, ...] = ()


@dataclass(frozen=True)
class TemplateFileSpec:
    path: str
    template: str
    group: str = "core"
    when_stacks: tuple[str, ...] = ()
    overwrite_hint: str = ""
    lifecycle: str = MANAGED


@dataclass(frozen=True)
class TemplateContextFragmentSpec:
    name: str
    template: str
    group: str = "core"
    when_stacks: tuple[str, ...] = ()


@dataclass(frozen=True)
class TemplateCompositionSpec:
    path: str
    template: str
    mode: str
    group: str = "core"
    when_stacks: tuple[str, ...] = ()
    marker: str = ""
    equivalent_lines: tuple[str, ...] = ()
    lifecycle: str = COMPOSED


@dataclass(frozen=True)
class TemplateProjectOwnedPathSpec:
    path: str
    group: str = "core"
    lifecycle: str = PROJECT


@dataclass(frozen=True)
class TemplateObsoleteFileSpec:
    path: str
    group: str = "core"
    migration_target: str = ""
    lifecycle: str = MIGRATED


@dataclass(frozen=True)
class TemplatePack:
    name: str
    version: str
    root: Path
    directories: list[TemplateDirectorySpec] = field(default_factory=list)
    files: list[TemplateFileSpec] = field(default_factory=list)
    context_fragments: list[TemplateContextFragmentSpec] = field(default_factory=list)
    compositions: list[TemplateCompositionSpec] = field(default_factory=list)
    project_owned_paths: list[TemplateProjectOwnedPathSpec] = field(default_factory=list)
    obsolete_files: list[TemplateObsoleteFileSpec] = field(default_factory=list)

    def template_path(self, relative_path: str) -> Path:
        relative = Path(relative_path)
        if relative.is_absolute() or relative_path.startswith("~") or ".." in relative.parts:
            raise ValueError(f"Template source must stay inside the pack: {relative_path}")
        path = self.root / relative
        try:
            path.resolve().relative_to(self.root.resolve())
        except ValueError as exc:
            raise ValueError(f"Template source must stay inside the pack: {relative_path}") from exc
        return path

    def read_template(self, relative_path: str) -> str:
        return self.template_path(relative_path).read_text(encoding="utf-8")


def _normalize_directory_specs(raw_dirs: Any) -> list[TemplateDirectorySpec]:
    specs: list[TemplateDirectorySpec] = []
    for item in raw_dirs or []:
        if isinstance(item, str):
            specs.append(TemplateDirectorySpec(path=item))
        elif isinstance(item, dict):
            specs.append(
                TemplateDirectorySpec(
                    path=item["path"],
                    group=item.get("group", "core"),
                    when_stacks=tuple(item.get("when_stacks", ())),
                )
            )
    return specs


def _normalize_file_specs(raw_files: Any) -> list[TemplateFileSpec]:
    specs: list[TemplateFileSpec] = []
    for item in raw_files or []:
        if isinstance(item, dict):
            specs.append(
                TemplateFileSpec(
                    path=item["path"],
                    template=item["template"],
                    group=item.get("group", "core"),
                    when_stacks=tuple(item.get("when_stacks", ())),
                    overwrite_hint=item.get("overwrite_hint", ""),
                    lifecycle=item.get("lifecycle", MANAGED),
                )
            )
    return specs


def _normalize_context_fragment_specs(raw_fragments: Any) -> list[TemplateContextFragmentSpec]:
    return [
        TemplateContextFragmentSpec(
            name=item["name"],
            template=item["template"],
            group=item.get("group", "core"),
            when_stacks=tuple(item.get("when_stacks", ())),
        )
        for item in raw_fragments or []
        if isinstance(item, dict)
    ]


def _normalize_composition_specs(raw_compositions: Any) -> list[TemplateCompositionSpec]:
    return [
        TemplateCompositionSpec(
            path=item["path"],
            template=item["template"],
            mode=item["mode"],
            group=item.get("group", "core"),
            when_stacks=tuple(item.get("when_stacks", ())),
            marker=item.get("marker", ""),
            equivalent_lines=tuple(item.get("equivalent_lines", ())),
        )
        for item in raw_compositions or []
        if isinstance(item, dict)
    ]


def _normalize_project_owned_path_specs(raw_paths: Any) -> list[TemplateProjectOwnedPathSpec]:
    return [
        TemplateProjectOwnedPathSpec(path=item["path"], group=item.get("group", "core"))
        for item in raw_paths or []
        if isinstance(item, dict)
    ]


def _normalize_obsolete_file_specs(raw_files: Any) -> list[TemplateObsoleteFileSpec]:
    specs: list[TemplateObsoleteFileSpec] = []
    for item in raw_files or []:
        if isinstance(item, dict):
            specs.append(
                TemplateObsoleteFileSpec(
                    path=item["path"],
                    group=item.get("group", "core"),
                    migration_target=item.get("migration_target", ""),
                )
            )
    return specs


def _normalized_declared_path(raw_path: str) -> str:
    path = Path(raw_path)
    if path.is_absolute() or raw_path.startswith("~") or ".." in path.parts:
        raise ValueError(f"Template path must stay inside the target repository: {raw_path}")
    return path.as_posix().removeprefix("./")


def load_template_pack(pack_root: Path) -> TemplatePack:
    manifest_path = pack_root / "manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    pack = TemplatePack(
        name=data.get("name", "default"),
        version=data.get("version", "0.1.0"),
        root=pack_root,
        directories=_normalize_directory_specs(data.get("directories")),
        files=_normalize_file_specs(data.get("files")),
        context_fragments=_normalize_context_fragment_specs(data.get("context_fragments")),
        compositions=_normalize_composition_specs(data.get("compositions")),
        project_owned_paths=_normalize_project_owned_path_specs(data.get("project_owned_paths")),
        obsolete_files=_normalize_obsolete_file_specs(data.get("obsolete_files")),
    )
    all_declared_paths = [
        *(spec.path for spec in pack.directories),
        *(spec.path for spec in pack.files),
        *(spec.path for spec in pack.compositions),
        *(spec.path for spec in pack.project_owned_paths),
        *(spec.path for spec in pack.obsolete_files),
    ]
    for raw_path in all_declared_paths:
        _normalized_declared_path(raw_path)
    output_paths = [
        *(_normalized_declared_path(spec.path) for spec in pack.files),
        *(_normalized_declared_path(spec.path) for spec in pack.compositions),
    ]
    duplicate_outputs = sorted(path for path, count in Counter(output_paths).items() if count > 1)
    if duplicate_outputs:
        raise ValueError(f"Output paths must be unique: {', '.join(duplicate_outputs)}")
    fragment_names = [spec.name for spec in pack.context_fragments]
    duplicate_fragments = sorted(name for name, count in Counter(fragment_names).items() if count > 1)
    if duplicate_fragments:
        raise ValueError(f"Context fragment names must be unique: {', '.join(duplicate_fragments)}")
    supported_modes = {"make-targets", "ensure-lines"}
    invalid_modes = sorted({spec.mode for spec in pack.compositions if spec.mode not in supported_modes})
    if invalid_modes:
        raise ValueError(f"Unsupported composition modes: {', '.join(invalid_modes)}")
    invalid_lifecycles = sorted(
        {
            repr(spec.lifecycle)
            for spec in pack.files
            if not isinstance(spec.lifecycle, str) or spec.lifecycle not in RENDERED_FILE_LIFECYCLES
        }
    )
    if invalid_lifecycles:
        raise ValueError(f"Unsupported file lifecycles: {', '.join(invalid_lifecycles)}")
    protected = {_normalized_declared_path(spec.path) for spec in pack.project_owned_paths}
    claimed = {_normalized_declared_path(spec.path) for spec in pack.files}
    claimed.update(_normalized_declared_path(spec.path) for spec in pack.compositions)
    claimed.update(_normalized_declared_path(spec.path) for spec in pack.obsolete_files)
    overlap = sorted(protected & claimed)
    if overlap:
        raise ValueError(f"Project-owned paths cannot be generated, composed, or obsolete: {', '.join(overlap)}")
    return pack


def load_default_template_pack(base_path: Path | None = None) -> TemplatePack:
    if base_path is not None:
        return load_template_pack(base_path / "template_packs" / "default")

    module = import_module("ai_workflow_bootstrap.template_packs.default")
    return load_template_pack(Path(module.__file__).resolve().parent)
