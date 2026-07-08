from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from string import Template


def render_template(template_text: str, context: Mapping[str, object]) -> str:
    return Template(template_text).safe_substitute(context).rstrip() + "\n"


def render_template_file(path: Path, context: Mapping[str, object]) -> str:
    return render_template(path.read_text(encoding="utf-8"), context)
