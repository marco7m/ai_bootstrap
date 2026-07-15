from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from .core.applier import PlanConflictError, apply_plan
from .core.lifecycle import RESET_CONFIRMATION
from .core.planner import BootstrapPlan, WriteResult, build_plan
from .core.scanner import detect_project_name, detect_repo_profile
from .core.state import build_state, load_state, save_state, state_path
from .core.template_pack import load_default_template_pack
from .core.workflow import resolve_workflow_selection

HELP_EPILOG = (
    "Usage:\n"
    "  ai-bootstrap                  Open the guided TUI\n"
    "  ai-bootstrap tui              Open the guided TUI\n"
    "  ai-bootstrap apply [path]     Apply from CLI\n\n"
    "Examples:\n"
    "  ai-bootstrap\n"
    "  ai-bootstrap apply --dry-run ."
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
        help=(
            "Update divergent bootstrap-managed files and retire proven-unchanged obsolete scaffolds; "
            "evolved seeded knowledge stays preserved."
        ),
    )
    apply_parser.add_argument(
        "--managed-only",
        action="store_true",
        help="Apply only managed infrastructure and safe compositions; do not create or update seeded knowledge.",
    )
    apply_parser.add_argument(
        "--reset-project-knowledge",
        action="store_true",
        help="Destructively reset only manifest-declared seeded knowledge files.",
    )
    apply_parser.add_argument(
        "--confirm-reset-project-knowledge",
        metavar="PHRASE",
        help=f'Required for a real knowledge reset; use "{RESET_CONFIRMATION}".',
    )
    apply_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created or overwritten without writing files.",
    )
    apply_parser.add_argument(
        "--no-skill",
        action="store_true",
        help="Do not create the spec-driven skill under .agents/skills/spec-driven/.",
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
        for key in ("build", "dev", "run", "test", "lint", "typecheck", "fmt", "check", "clean-dev"):
            if key in profile.commands:
                print(f"- {key:10} {profile.commands[key]}")

    width = max(len(str(result.path)) for result in results) if results else 10
    print("\nFiles and directories:")
    for result in results:
        rel = str(result.path)
        print(
            f"- {rel.ljust(width)}  {result.lifecycle:8}  "
            f"{result.status:18}  {result.message}"
        )

    print("\nNext steps:")
    print("1. Open your preferred AI assistant.")
    print("2. Follow generated entry points when present: AGENTS.md, docs/INDEX.md, and .agents/skills/.")
    print("3. For non-trivial work, respect the generated approval workflow.")


def _run_tui(argv: Sequence[str] | None = None) -> int:
    from .tui import main as tui_main

    return tui_main(list(argv) if argv is not None else [])


def _run_apply(args: argparse.Namespace) -> int:
    target = Path(args.path).expanduser()

    if args.reset_project_knowledge and args.managed_only:
        print("Error: --managed-only and --reset-project-knowledge cannot be combined.", file=sys.stderr)
        return 2
    if (
        args.reset_project_knowledge
        and not args.dry_run
        and args.confirm_reset_project_knowledge != RESET_CONFIRMATION
    ):
        print(
            "Error: a real knowledge reset requires "
            f'--confirm-reset-project-knowledge "{RESET_CONFIRMATION}".',
            file=sys.stderr,
        )
        return 2

    if target.exists() and not target.is_dir():
        print(f"Error: target path is not a directory: {target}", file=sys.stderr)
        return 2

    if not target.exists() and not args.dry_run:
        target.mkdir(parents=True, exist_ok=True)

    project_name = detect_project_name(target, args.project_name)
    profile = detect_repo_profile(target, project_name)
    pack = load_default_template_pack()
    try:
        prior_state = load_state(state_path(target))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    enabled_workflows, enabled_groups = resolve_workflow_selection(include_skills=not args.no_skill)
    plan: BootstrapPlan = build_plan(
        target,
        profile=profile,
        pack=pack,
        enabled_workflows=enabled_workflows,
        enabled_groups=enabled_groups,
        force=args.force,
        dry_run=args.dry_run,
        prior_files=prior_state.files if prior_state else None,
        managed_only=args.managed_only,
        reset_project_knowledge=args.reset_project_knowledge,
    )
    try:
        results = apply_plan(plan, dry_run=args.dry_run)
    except PlanConflictError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    if not args.dry_run:
        state = build_state(
            plan=plan,
            results=results,
            tool_version=__version__,
            prior_state=prior_state,
        )
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
