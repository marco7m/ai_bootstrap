from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from .core.applier import apply_plan
from .core.planner import BootstrapPlan, build_plan
from .core.scanner import detect_project_name, detect_repo_profile
from .core.state import build_state, save_state, state_path
from .core.template_pack import load_default_template_pack
from .core.workflow import resolve_workflow_selection

TEXTUAL_REQUIRED_MESSAGE = "Textual is required for the TUI.\nInstall with:\npip install -e \".[tui]\""
PATH_INPUT_ID = "path_input"
MODE_SELECT_ID = "mode_select"
INCLUDE_SKILLS_ID = "include_skills"
PREVIEW_BUTTON_ID = "preview_button"
DRY_RUN_BUTTON_ID = "dry_run_button"
APPLY_BUTTON_ID = "apply_button"
CANCEL_BUTTON_ID = "cancel_button"
PREVIEW_TABLE_ID = "preview_table"
CONFIRM_INPUT_ID = "confirm_input"
STATUS_ID = "status"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-workflow-bootstrap tui",
        description="Open the interactive AI-agnostic bootstrap TUI.",
    )
    return parser


def _load_textual():
    try:
        from textual.app import App, ComposeResult
        from textual.containers import Container, Horizontal
        from textual.widgets import Button, Checkbox, DataTable, Footer, Header, Input, Select, Static
    except ImportError as exc:  # pragma: no cover - exercised via runtime fallback
        raise ImportError(TEXTUAL_REQUIRED_MESSAGE) from exc

    return {
        "App": App,
        "ComposeResult": ComposeResult,
        "Container": Container,
        "Horizontal": Horizontal,
        "Button": Button,
        "Checkbox": Checkbox,
        "DataTable": DataTable,
        "Footer": Footer,
        "Header": Header,
        "Input": Input,
        "Select": Select,
        "Static": Static,
    }


def _plan_from_ui(target_text: str, mode: str, include_skills: bool, dry_run: bool) -> BootstrapPlan:
    target = Path(target_text or ".").expanduser()
    if target.exists() and not target.is_dir():
        raise ValueError(f"Target path is not a directory: {target}")

    project_name = detect_project_name(target, None)
    profile = detect_repo_profile(target, project_name)
    pack = load_default_template_pack()
    enabled_workflows, enabled_groups = resolve_workflow_selection(mode=mode, include_skills=include_skills)
    return build_plan(
        target,
        profile=profile,
        pack=pack,
        enabled_workflows=enabled_workflows,
        enabled_groups=enabled_groups,
        force=False,
        dry_run=dry_run,
        backup_existing=True,
    )


def _build_app():
    symbols = _load_textual()
    App = symbols["App"]
    ComposeResult = symbols["ComposeResult"]
    Container = symbols["Container"]
    Horizontal = symbols["Horizontal"]
    Button = symbols["Button"]
    Checkbox = symbols["Checkbox"]
    DataTable = symbols["DataTable"]
    Footer = symbols["Footer"]
    Header = symbols["Header"]
    Input = symbols["Input"]
    Select = symbols["Select"]
    Static = symbols["Static"]

    class BootstrapTuiApp(App):
        CSS = """
        Screen {
            layout: vertical;
        }

        #intro {
            padding: 1 2;
        }

        #controls {
            height: auto;
            padding: 0 2;
        }

        #controls > * {
            margin-bottom: 1;
        }

        #mode_select {
            width: 36;
        }

        #path_input {
            width: 40;
        }

        #confirm_input {
            width: 20;
        }

        #preview_table {
            height: 1fr;
            min-height: 12;
            margin: 0 2 1 2;
        }

        #status {
            padding: 0 2 1 2;
        }
        """

        BINDINGS = [("q", "quit", "Quit")]

        def __init__(self) -> None:
            super().__init__()
            self._current_plan: BootstrapPlan | None = None

        def compose(self) -> ComposeResult:
            yield Header()
            with Container():
                yield Static(
                    "This tool prepares a repository for assistant-driven work with AGENTS.md, docs, and open Agent Skills.",
                    id="intro",
                )
                yield Static(
                    "Spec-driven means the assistant first clarifies the request, writes a spec, waits for approval, then creates a plan and tasks before coding.",
                    id="spec_driven_help",
                )
                yield Static(
                    "Living docs are compact project memory: decisions, current status, roadmap, ideas, and glossary.",
                    id="living_docs_help",
                )
                yield Static(
                    "Agent Skills are reusable instructions for compatible AI coding agents.",
                    id="skills_help",
                )
                yield Static(
                    "Dry run shows what would happen, but writes nothing.",
                    id="dry_run_help",
                )
                yield Static(
                    "written = will be created or updated; skipped = already exists and will not be changed; unchanged = already matches; overwritten = only with force.",
                    id="status_help",
                )
                with Horizontal(id="controls"):
                    yield Input(value=".", placeholder="Project path", id=PATH_INPUT_ID)
                    yield Select(
                        options=[
                            ("Recommended: spec-driven + living docs", "recommended"),
                            ("Spec-driven only", "spec-driven"),
                            ("Living docs only", "living-docs"),
                        ],
                        value="recommended",
                        id=MODE_SELECT_ID,
                    )
                    yield Checkbox("Include .agents/skills", True, id=INCLUDE_SKILLS_ID)
                    yield Input(placeholder="Type APPLY to write", id=CONFIRM_INPUT_ID)
                with Horizontal():
                    yield Button("Preview", id=PREVIEW_BUTTON_ID, variant="primary")
                    yield Button("Dry Run", id=DRY_RUN_BUTTON_ID)
                    yield Button("Apply", id=APPLY_BUTTON_ID, variant="success")
                    yield Button("Cancel", id=CANCEL_BUTTON_ID)
                yield Static(
                    "Preview first. Apply writes only after explicit confirmation. Cancel writes nothing.",
                    id="status",
                )
                yield DataTable(id=PREVIEW_TABLE_ID)
            yield Footer()

        def on_mount(self) -> None:
            table = self.query_one(f"#{PREVIEW_TABLE_ID}", DataTable)
            table.add_columns("Path", "Status", "Kind", "Message")
            self._refresh_preview()

        def _read_settings(self) -> tuple[str, str, bool]:
            path = self.query_one(f"#{PATH_INPUT_ID}", Input).value.strip() or "."
            mode = self.query_one(f"#{MODE_SELECT_ID}", Select).value or "recommended"
            include_skills = bool(self.query_one(f"#{INCLUDE_SKILLS_ID}", Checkbox).value)
            return path, mode, include_skills

        def _set_status(self, message: str) -> None:
            self.query_one(f"#{STATUS_ID}", Static).update(message)

        def _show_plan(self, plan: BootstrapPlan) -> None:
            table = self.query_one(f"#{PREVIEW_TABLE_ID}", DataTable)
            table.clear()
            for item in plan.results:
                table.add_row(str(item.path), item.status, item.kind, item.message)

        def _refresh_preview(self) -> None:
            try:
                path, mode, include_skills = self._read_settings()
                plan = _plan_from_ui(path, mode, include_skills, dry_run=True)
            except ValueError as exc:
                self._current_plan = None
                self._set_status(str(exc))
                return

            self._current_plan = plan
            self._show_plan(plan)
            self._set_status("Preview ready. Type APPLY and press Apply to write changes.")

        def _dry_run(self) -> None:
            path, mode, include_skills = self._read_settings()

            try:
                plan = _plan_from_ui(path, mode, include_skills, dry_run=True)
            except ValueError as exc:
                self._current_plan = None
                self._set_status(str(exc))
                return

            self._current_plan = plan
            self._show_plan(plan)
            apply_plan(plan, dry_run=True, backup_existing=True)
            self._set_status("Dry run completed. No files were written.")

        def _apply(self) -> None:
            path, mode, include_skills = self._read_settings()
            confirm = self.query_one(f"#{CONFIRM_INPUT_ID}", Input).value.strip().upper()

            if confirm != "APPLY":
                self._set_status('Type APPLY in the confirmation field before writing files.')
                return

            try:
                plan = _plan_from_ui(path, mode, include_skills, dry_run=False)
            except ValueError as exc:
                self._current_plan = None
                self._set_status(str(exc))
                return

            self._current_plan = plan
            self._show_plan(plan)
            results = apply_plan(plan, dry_run=False, backup_existing=True)

            state = build_state(plan=plan, results=results, tool_version=__version__)
            save_state(state_path(plan.target), state, dry_run=False)
            self._set_status(
                "Applied changes and wrote .ai-bootstrap/state.json.\n"
                "Next steps:\n"
                "1. Open your preferred AI assistant.\n"
                "2. Ask it to read AGENTS.md and docs/AI_CONTEXT.md.\n"
                "3. For non-trivial changes, follow docs/SPEC_DRIVEN.md.\n"
                "4. Approve the spec before implementation."
            )

        def on_button_pressed(self, event) -> None:
            button_id = event.button.id
            if button_id == PREVIEW_BUTTON_ID:
                self._refresh_preview()
            elif button_id == DRY_RUN_BUTTON_ID:
                self._dry_run()
            elif button_id == APPLY_BUTTON_ID:
                self._apply()
            elif button_id == CANCEL_BUTTON_ID:
                self.exit(0)

    return BootstrapTuiApp()


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(list(argv) if argv is not None else sys.argv[1:])

    try:
        app = _build_app()
    except ImportError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    app.run()
    return 0
