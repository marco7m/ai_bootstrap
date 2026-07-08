from __future__ import annotations

import json
from importlib import import_module
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TemplateDirectorySpec:
    path: str
    group: str = "core"


@dataclass(frozen=True)
class TemplateFileSpec:
    path: str
    template: str
    group: str = "core"


@dataclass(frozen=True)
class TemplatePack:
    name: str
    version: str
    root: Path
    directories: list[TemplateDirectorySpec] = field(default_factory=list)
    files: list[TemplateFileSpec] = field(default_factory=list)

    def template_path(self, relative_path: str) -> Path:
        return self.root / relative_path

    def read_template(self, relative_path: str) -> str:
        return self.template_path(relative_path).read_text(encoding="utf-8")


def _normalize_directory_specs(raw_dirs: Any) -> list[TemplateDirectorySpec]:
    specs: list[TemplateDirectorySpec] = []
    for item in raw_dirs or []:
        if isinstance(item, str):
            specs.append(TemplateDirectorySpec(path=item))
        elif isinstance(item, dict):
            specs.append(TemplateDirectorySpec(path=item["path"], group=item.get("group", "core")))
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
                )
            )
    return specs


def load_template_pack(pack_root: Path) -> TemplatePack:
    manifest_path = pack_root / "manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    return TemplatePack(
        name=data.get("name", "default"),
        version=data.get("version", "0.1.0"),
        root=pack_root,
        directories=_normalize_directory_specs(data.get("directories")),
        files=_normalize_file_specs(data.get("files")),
    )


def load_default_template_pack(base_path: Path | None = None) -> TemplatePack:
    if base_path is not None:
        return load_template_pack(base_path / "template_packs" / "default")

    module = import_module("ai_workflow_bootstrap.template_packs.default")
    return load_template_pack(Path(module.__file__).resolve().parent)
