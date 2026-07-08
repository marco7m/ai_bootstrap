from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from .core.applier import apply_plan
from .core.planner import BootstrapPlan, WriteResult, build_plan
from .core.scanner import detect_project_name, detect_repo_profile
from .core.state import build_state, save_state, state_path
from .core.template_pack import load_default_template_pack
from .core.workflow import resolve_workflow_selection

HELP_EPILOG = (
    "Usage:\n"
    "  ai-bootstrap                  Open the guided TUI\n"
    "  ai-bootstrap tui              Open the guided TUI\n"
    "  ai-bootstrap apply [path]     Apply from CLI\n\n"
    "Examples:\n"
    "  ai-bootstrap\n"
    "  ai-bootstrap apply --dry-run .\n"
    "  ai-bootstrap apply --no-living-docs .\n"
    "  ai-bootstrap apply --living-docs-only ."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-bootstrap",
        description="Open the guided TUI by default. Use apply for non-interactive runs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=HELP_EPILOG,
    )
    subparsers = parser.add_subparsers(dest="command", title="Commands")

    tui_parser = subparsers.add_parser("tui", help="Open the guided TUI.")
    tui_parser.set_defaults(command="tui")

    apply_parser = subparsers.add_parser("apply", help="Apply the bootstrap non-interactively.")
    apply_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Target repository directory. Defaults to the current directory.",
    )
    apply_parser.add_argument(
        "--project-name",
        help="Optional project name written into AGENTS.md. Defaults to the folder name.",
    )
    apply_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files. Existing files are backed up unless --no-backup is used.",
    )
    apply_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created or overwritten without writing files.",
    )
    apply_parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create backup files when overwriting with --force.",
    )
    apply_parser.add_argument(
        "--no-skill",
        action="store_true",
        help="Do not create the spec-driven skill under .agents/skills/spec-driven/.",
    )
    apply_parser.add_argument(
        "--no-living-docs",
        action="store_true",
        help="Do not create living docs files or the living-docs skill.",
    )
    apply_parser.add_argument(
        "--living-docs-only",
        action="store_true",
        help="Create only living docs files and the living-docs skill.",
    )
    apply_parser.set_defaults(command="apply")
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
    print("1. Open your preferred AI assistant.")
    print("2. Read AGENTS.md and docs/AI_CONTEXT.md.")
    print("3. For non-trivial changes, follow docs/SPEC_DRIVEN.md.")
    print("4. Approve the spec before implementation.")


def _resolve_groups(*, no_living_docs: bool, living_docs_only: bool, no_skill: bool) -> tuple[list[str], set[str]]:
    if living_docs_only:
        return resolve_workflow_selection(mode="living-docs", include_skills=not no_skill)
    if no_living_docs:
        return resolve_workflow_selection(mode="spec-driven", include_skills=not no_skill)
    return resolve_workflow_selection(mode="recommended", include_skills=not no_skill)


def _run_tui(argv: Sequence[str] | None = None) -> int:
    from .tui import main as tui_main

    return tui_main(list(argv) if argv is not None else [])


def _run_apply(args: argparse.Namespace) -> int:
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


def main(argv: Sequence[str] | None = None) -> int:
    raw_argv = list(argv) if argv is not None else sys.argv[1:]
    if not raw_argv:
        return _run_tui([])

    args = build_parser().parse_args(raw_argv)
    if args.command == "tui":
        return _run_tui([])
    if args.command == "apply":
        return _run_apply(args)
    return 0
