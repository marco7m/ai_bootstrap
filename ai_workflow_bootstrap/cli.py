from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from .core.applier import apply_plan
from .core.planner import BootstrapPlan, WriteResult, build_plan
from .core.scanner import detect_project_name, detect_repo_profile
from .core.template_pack import load_default_template_pack


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bootstrap a repository for guided Spec-Driven Development.",
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
        "--global-codex",
        action="store_true",
        help="Also create or update ~/.codex/AGENTS.md with a small global default.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create backup files when overwriting with --force.",
    )
    parser.add_argument(
        "--no-cursor",
        action="store_true",
        help="Do not create Cursor-specific files under .cursor/.",
    )
    parser.add_argument(
        "--no-skill",
        action="store_true",
        help="Do not create the Codex skill under .agents/skills/spec-driven/.",
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
    print("1. Open the repository in Codex or Cursor.")
    print("2. Read or paste the prompt from docs/START_PROMPT.md.")
    print("3. Describe the feature you want to build.")
    print("4. Approve the generated spec before letting the agent implement.")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else sys.argv[1:])
    target = Path(args.path).expanduser()

    if target.exists() and not target.is_dir():
        print(f"Error: target path is not a directory: {target}", file=sys.stderr)
        return 2

    if not target.exists() and not args.dry_run:
        target.mkdir(parents=True, exist_ok=True)

    project_name = detect_project_name(target, args.project_name)
    profile = detect_repo_profile(target, project_name)
    pack = load_default_template_pack()
    plan: BootstrapPlan = build_plan(
        target,
        profile=profile,
        pack=pack,
        force=args.force,
        dry_run=args.dry_run,
        backup_existing=not args.no_backup,
        install_global_codex=args.global_codex,
        with_cursor=not args.no_cursor,
        with_skill=not args.no_skill,
    )
    results = apply_plan(plan, dry_run=args.dry_run, backup_existing=not args.no_backup)
    print_summary(results, target=target, profile=profile)
    return 0
