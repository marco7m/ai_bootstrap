from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except Exception:  # pragma: no cover - only used on old Python versions
    tomllib = None


@dataclass
class RepoProfile:
    project_name: str
    repo_name: str
    package_manager: str | None = None
    detected_stacks: list[str] = field(default_factory=list)
    commands: dict[str, str] = field(default_factory=dict)
    top_dirs: list[str] = field(default_factory=list)


def detect_project_name(target: Path, explicit_name: str | None) -> str:
    if explicit_name:
        return explicit_name.strip()
    name = target.resolve().name.strip()
    return name or "My Project"


def read_text_if_exists(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def detect_package_manager(target: Path) -> str | None:
    if (target / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (target / "bun.lockb").exists() or (target / "bun.lock").exists():
        return "bun"
    if (target / "yarn.lock").exists():
        return "yarn"
    if (target / "package-lock.json").exists() or (target / "npm-shrinkwrap.json").exists():
        return "npm"
    if (target / "package.json").exists():
        return "npm"
    if (target / "uv.lock").exists():
        return "uv"
    if (target / "poetry.lock").exists():
        return "poetry"
    return None


def parse_make_targets(makefile_text: str) -> set[str]:
    targets: set[str] = set()
    for line in makefile_text.splitlines():
        if line and not line.startswith("\t"):
            match = re.match(r"^([A-Za-z0-9_.-]+):", line)
            if match:
                targets.add(match.group(1))
    return targets


def detect_repo_profile(target: Path, project_name: str) -> RepoProfile:
    profile = RepoProfile(
        project_name=project_name,
        repo_name=target.resolve().name,
        package_manager=detect_package_manager(target),
    )

    top_dirs = []
    children = sorted(target.iterdir(), key=lambda p: p.name.lower()) if target.exists() else []
    for child in children:
        if child.is_dir() and not child.name.startswith("."):
            if child.name in {
                "src",
                "app",
                "lib",
                "frontend",
                "backend",
                "server",
                "client",
                "docs",
                "tests",
                "test",
                "packages",
                "services",
            }:
                top_dirs.append(child.name)
    profile.top_dirs = top_dirs

    makefile_text = read_text_if_exists(target / "Makefile") or read_text_if_exists(target / "makefile")
    make_targets = parse_make_targets(makefile_text) if makefile_text else set()

    def maybe_set(name: str, command: str) -> None:
        if name not in profile.commands:
            profile.commands[name] = command

    if make_targets:
        profile.detected_stacks.append("make")
        for name in ("build", "test", "lint", "typecheck", "check", "fmt"):
            if name in make_targets:
                maybe_set(name, f"make {name}")

    package_json = target / "package.json"
    if package_json.exists():
        profile.detected_stacks.append("node")
        try:
            data = json.loads(read_text_if_exists(package_json) or "{}")
            scripts = data.get("scripts", {}) if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            scripts = {}
        runner = profile.package_manager or "npm"
        run = {
            "npm": "npm run",
            "pnpm": "pnpm",
            "yarn": "yarn",
            "bun": "bun run",
        }.get(runner, "npm run")
        for name in ("build", "test", "lint", "typecheck", "check", "dev"):
            if name in scripts:
                maybe_set(name, f"{run} {name}")

    cargo_toml = target / "Cargo.toml"
    if cargo_toml.exists():
        profile.detected_stacks.append("rust")
        maybe_set("build", "cargo build")
        maybe_set("test", "cargo test")
        maybe_set("lint", "cargo clippy --all-targets --all-features -- -D warnings")
        maybe_set("fmt", "cargo fmt --all --check")

    go_mod = target / "go.mod"
    if go_mod.exists():
        profile.detected_stacks.append("go")
        maybe_set("build", "go build ./...")
        maybe_set("test", "go test ./...")
        maybe_set("fmt", "gofmt -w .")

    pyproject = target / "pyproject.toml"
    if pyproject.exists() and tomllib is not None:
        profile.detected_stacks.append("python")
        prefix = {
            "uv": "uv run ",
            "poetry": "poetry run ",
        }.get(profile.package_manager or "", "")
        try:
            data = tomllib.loads(read_text_if_exists(pyproject))
        except Exception:
            data = {}
        tool = data.get("tool", {}) if isinstance(data, dict) else {}
        if "pytest" in tool or (target / "pytest.ini").exists() or (target / "tests").exists():
            maybe_set("test", f"{prefix}pytest")
        if "ruff" in tool:
            maybe_set("lint", f"{prefix}ruff check .")
            maybe_set("fmt", f"{prefix}ruff format --check .")
        elif "black" in tool:
            maybe_set("fmt", f"{prefix}black --check .")
        if "mypy" in tool:
            maybe_set("typecheck", f"{prefix}mypy .")
        maybe_set("build", f"{prefix}python -m build")

    if (target / "requirements.txt").exists() and "python" not in profile.detected_stacks:
        profile.detected_stacks.append("python")
        maybe_set("test", "pytest")

    if "check" not in profile.commands:
        parts = [profile.commands[name] for name in ("lint", "typecheck", "test") if name in profile.commands]
        if parts:
            maybe_set("check", " && ".join(parts))

    return profile


def format_repo_layout(profile: RepoProfile) -> str:
    if not profile.top_dirs:
        return "- No obvious top-level source directories detected yet. Add them later if useful."
    return "\n".join(f"- `{name}/`" for name in profile.top_dirs)


def format_commands(profile: RepoProfile) -> str:
    ordered = ["build", "test", "lint", "typecheck", "fmt", "check", "dev"]
    lines = []
    for name in ordered:
        if name in profile.commands:
            lines.append(f"- `{profile.commands[name]}` — {name}")
    if not lines:
        lines.append("- No reliable project commands detected yet. Update this file once the repo has build/test/lint commands.")
    return "\n".join(lines)


def format_detected_stack(profile: RepoProfile) -> str:
    if not profile.detected_stacks:
        return "unknown"
    return ", ".join(profile.detected_stacks)

