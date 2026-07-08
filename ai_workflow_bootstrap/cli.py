from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from .core.applier import apply_plan
from .core.planner import BootstrapPlan, WriteResult, build_plan
from .core.scanner import detect_project_name, detect_repo_profile
from .core.state import build_state, save_state, state_path
from .core.template_pack import load_default_template_pack
from .core.workflow import resolve_workflow_selection
from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bootstrap a repository for guided, AI-agnostic Spec-Driven Development.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python -m ai_workflow_bootstrap --dry-run .\n"
            "  python -m ai_workflow_bootstrap .\n"
            "  python -m ai_workflow_bootstrap tui\n\n"
            "Interactive TUI:\n"
            "  python -m ai_workflow_bootstrap tui"
        ),
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Target repository directory. Defaults to the current directory.",
    )
    parser.add_argument(
        "--project-name",
        help="Optional project name written into AGENTS.md. Defaults to the folder name.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files. Existing files are backed up unless --no-backup is used.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created or overwritten without writing files.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create backup files when overwriting with --force.",
    )
    parser.add_argument(
        "--no-skill",
        action="store_true",
        help="Do not create the spec-driven skill under .agents/skills/spec-driven/.",
    )
    parser.add_argument(
        "--no-living-docs",
        action="store_true",
        help="Do not create living docs files or the living-docs skill.",
    )
    parser.add_argument(
        "--living-docs-only",
        action="store_true",
        help="Create only living docs files and the living-docs skill.",
    )
    return parser


def print_summary(results: list[WriteResult], *, target: Path, profile) -> None:
    print(f"\nBootstrapped repository: {target.resolve()}\n")
    if profile.detected_stacks:
        print(f"Detected stack(s): {', '.join(profile.detected_stacks)}")
    if profile.package_manager:
        print(f"Detected package manager: {profile.package_manager}")
    if profile.top_dirs:
        print(f"Top directories: {', '.join(profile.top_dirs)}")
    if profile.commands:
        print("Suggested commands:")
        for key in ("build", "test", "lint", "typecheck", "fmt", "check", "dev"):
            if key in profile.commands:
                print(f"- {key:10} {profile.commands[key]}")

    width = max(len(str(result.path)) for result in results) if results else 10
    print("\nFiles and directories:")
    for result in results:
        rel = str(result.path)
        print(f"- {rel.ljust(width)}  {result.status:9}  {result.message}")

    print("\nNext steps:")
    print("1. Open the repository in your AI assistant.")
    print("2. Read or paste the prompt from docs/START_PROMPT.md.")
    print("3. Describe the feature you want to build.")
    print("4. Approve the generated spec before letting the assistant implement.")


def _resolve_groups(*, no_living_docs: bool, living_docs_only: bool, no_skill: bool) -> tuple[list[str], set[str]]:
    if living_docs_only:
        return resolve_workflow_selection(mode="living-docs", include_skills=not no_skill)
    if no_living_docs:
        return resolve_workflow_selection(mode="spec-driven", include_skills=not no_skill)
    return resolve_workflow_selection(mode="recommended", include_skills=not no_skill)


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(argv) if argv is not None else sys.argv[1:]
    if raw_argv and raw_argv[0] == "tui":
        from .tui import main as tui_main

        return tui_main(raw_argv[1:])

    args = build_parser().parse_args(raw_argv)
    target = Path(args.path).expanduser()

    if target.exists() and not target.is_dir():
        print(f"Error: target path is not a directory: {target}", file=sys.stderr)
        return 2

    if not target.exists() and not args.dry_run:
        target.mkdir(parents=True, exist_ok=True)

    project_name = detect_project_name(target, args.project_name)
    profile = detect_repo_profile(target, project_name)
    pack = load_default_template_pack()
    enabled_workflows, enabled_groups = _resolve_groups(
        no_living_docs=args.no_living_docs,
        living_docs_only=args.living_docs_only,
        no_skill=args.no_skill,
    )
    plan: BootstrapPlan = build_plan(
        target,
        profile=profile,
        pack=pack,
        enabled_workflows=enabled_workflows,
        enabled_groups=enabled_groups,
        force=args.force,
        dry_run=args.dry_run,
        backup_existing=not args.no_backup,
    )
    results = apply_plan(plan, dry_run=args.dry_run, backup_existing=not args.no_backup)
    if not args.dry_run:
        state = build_state(plan=plan, results=results, tool_version=__version__)
        save_state(state_path(target), state, dry_run=False)
    print_summary(results, target=target, profile=profile)
    return 0
