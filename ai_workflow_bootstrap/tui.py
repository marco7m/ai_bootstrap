from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from .core.applier import apply_plan
from .core.planner import BootstrapPlan, build_plan
from .core.projects import add_recent_project, format_project_choice, load_recent_projects, scan_project_dirs
from .core.scanner import detect_project_name, detect_repo_profile
from .core.state import build_state, save_state, state_path
from .core.template_pack import load_default_template_pack
from .core.workflow import resolve_workflow_selection
from .tui_text import SUPPORTED_LANGUAGES, detect_default_language, t

TEXTUAL_REQUIRED_MESSAGE = "Textual is required for the TUI.\nInstall with:\npip install -e \".[tui]\""

LANGUAGE_SELECT_ID = "language_select"
PROJECT_SELECT_ID = "project_select"
PROJECT_MESSAGE_ID = "project_message"
PATH_INPUT_ID = "path_input"
MODE_SELECT_ID = "mode_select"
INCLUDE_SKILLS_ID = "include_skills"
OVERWRITE_EXISTING_ID = "overwrite_existing"
PREVIEW_BUTTON_ID = "preview_button"
DRY_RUN_BUTTON_ID = "dry_run_button"
APPLY_BUTTON_ID = "apply_button"
CANCEL_BUTTON_ID = "cancel_button"
CURRENT_DIRECTORY_BUTTON_ID = "current_directory_button"
HOME_BUTTON_ID = "home_button"
PARENT_BUTTON_ID = "parent_button"
REFRESH_PROJECTS_BUTTON_ID = "refresh_projects_button"
PREVIEW_TABLE_ID = "preview_table"
CONFIRM_INPUT_ID = "confirm_input"
STATUS_ID = "status"
APP_INTRO_ID = "app_intro"
SPEC_DRIVEN_HELP_ID = "spec_driven_help"
LIVING_DOCS_HELP_ID = "living_docs_help"
SKILLS_HELP_ID = "skills_help"
DRY_RUN_HELP_ID = "dry_run_help"
STATUS_HELP_ID = "status_help"


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


def _plan_from_ui(
    target_text: str,
    mode: str,
    include_skills: bool,
    dry_run: bool,
    force: bool = False,
) -> BootstrapPlan:
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
        force=force,
        dry_run=dry_run,
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

        #app_intro,
        #spec_driven_help,
        #living_docs_help,
        #skills_help,
        #dry_run_help,
        #status_help,
        #project_message,
        #status {
            padding: 0 2 1 2;
        }

        #controls,
        #path_controls,
        #mode_controls,
        #action_controls {
            height: auto;
            padding: 0 2;
            margin-bottom: 1;
        }

        #language_select,
        #project_select {
            width: 44;
        }

        #path_input {
            width: 56;
        }

        #mode_select {
            width: 34;
        }

        #confirm_input {
            width: 24;
        }

        #preview_table {
            height: 1fr;
            min-height: 12;
            margin: 0 2 1 2;
        }
        """

        BINDINGS = [("q", "quit", "Quit")]

        def __init__(self) -> None:
            super().__init__()
            self._current_plan: BootstrapPlan | None = None
            self._language = detect_default_language(os.environ)

        def compose(self) -> ComposeResult:
            yield Header()
            with Container():
                yield Static(t(self._language, "app_intro"), id=APP_INTRO_ID)
                yield Static(t(self._language, "spec_driven_help"), id=SPEC_DRIVEN_HELP_ID)
                yield Static(t(self._language, "living_docs_help"), id=LIVING_DOCS_HELP_ID)
                yield Static(t(self._language, "skills_help"), id=SKILLS_HELP_ID)
                yield Static(t(self._language, "dry_run_help"), id=DRY_RUN_HELP_ID)
                yield Static(t(self._language, "status_help"), id=STATUS_HELP_ID)

                with Horizontal(id="controls"):
                    yield Select(
                        options=[("English", "en"), ("Português (pt-BR)", "pt-BR")],
                        prompt=t(self._language, "language_label"),
                        value=self._language,
                        id=LANGUAGE_SELECT_ID,
                    )
                    yield Select(
                        options=[],
                        prompt=t(self._language, "project_select_label"),
                        value=Select.NULL,
                        allow_blank=True,
                        id=PROJECT_SELECT_ID,
                    )
                    yield Static("", id=PROJECT_MESSAGE_ID)

                with Horizontal(id="path_controls"):
                    yield Input(
                        value=".",
                        placeholder=t(self._language, "project_path_placeholder"),
                        id=PATH_INPUT_ID,
                    )
                    yield Button(t(self._language, "current_directory_button"), id=CURRENT_DIRECTORY_BUTTON_ID)
                    yield Button(t(self._language, "home_button"), id=HOME_BUTTON_ID)
                    yield Button(t(self._language, "parent_button"), id=PARENT_BUTTON_ID)
                    yield Button(t(self._language, "refresh_projects_button"), id=REFRESH_PROJECTS_BUTTON_ID)

                with Horizontal(id="mode_controls"):
                    yield Select(
                        options=self._mode_options(),
                        prompt=t(self._language, "mode_label"),
                        value="recommended",
                        id=MODE_SELECT_ID,
                    )
                    yield Checkbox(t(self._language, "include_skills_label"), True, id=INCLUDE_SKILLS_ID)
                    yield Checkbox(t(self._language, "overwrite_existing_label"), False, id=OVERWRITE_EXISTING_ID)
                    yield Input(placeholder=t(self._language, "confirm_placeholder"), id=CONFIRM_INPUT_ID)

                with Horizontal(id="action_controls"):
                    yield Button(t(self._language, "preview_button"), id=PREVIEW_BUTTON_ID, variant="primary")
                    yield Button(t(self._language, "dry_run_button"), id=DRY_RUN_BUTTON_ID)
                    yield Button(t(self._language, "apply_button"), id=APPLY_BUTTON_ID, variant="success")
                    yield Button(t(self._language, "cancel_button"), id=CANCEL_BUTTON_ID)

                yield Static(t(self._language, "preview_ready"), id=STATUS_ID)
                yield DataTable(id=PREVIEW_TABLE_ID)
            yield Footer()

        def on_mount(self) -> None:
            table = self.query_one(f"#{PREVIEW_TABLE_ID}", DataTable)
            table.add_columns("Path", "Status", "Kind", "Message")
            self._refresh_language_texts()
            self._refresh_projects()
            self._refresh_preview()

        def _mode_options(self) -> list[tuple[str, str]]:
            return [
                (t(self._language, "recommended_mode"), "recommended"),
                (t(self._language, "spec_driven_only_mode"), "spec-driven"),
                (t(self._language, "living_docs_only_mode"), "living-docs"),
            ]

        def _language_widget(self):
            return self.query_one(f"#{LANGUAGE_SELECT_ID}", Select)

        def _project_widget(self):
            return self.query_one(f"#{PROJECT_SELECT_ID}", Select)

        def _path_widget(self):
            return self.query_one(f"#{PATH_INPUT_ID}", Input)

        def _mode_widget(self):
            return self.query_one(f"#{MODE_SELECT_ID}", Select)

        def _include_skills_widget(self):
            return self.query_one(f"#{INCLUDE_SKILLS_ID}", Checkbox)

        def _overwrite_existing_widget(self):
            return self.query_one(f"#{OVERWRITE_EXISTING_ID}", Checkbox)

        def _confirm_widget(self):
            return self.query_one(f"#{CONFIRM_INPUT_ID}", Input)

        def _project_message_widget(self):
            return self.query_one(f"#{PROJECT_MESSAGE_ID}", Static)

        def _set_status(self, message: str) -> None:
            self.query_one(f"#{STATUS_ID}", Static).update(message)

        def _button(self, button_id: str):
            return self.query_one(f"#{button_id}", Button)

        def _refresh_button_labels(self) -> None:
            self._button(CURRENT_DIRECTORY_BUTTON_ID).label = t(self._language, "current_directory_button")
            self._button(HOME_BUTTON_ID).label = t(self._language, "home_button")
            self._button(PARENT_BUTTON_ID).label = t(self._language, "parent_button")
            self._button(REFRESH_PROJECTS_BUTTON_ID).label = t(self._language, "refresh_projects_button")
            self._button(PREVIEW_BUTTON_ID).label = t(self._language, "preview_button")
            self._button(DRY_RUN_BUTTON_ID).label = t(self._language, "dry_run_button")
            self._button(APPLY_BUTTON_ID).label = t(self._language, "apply_button")
            self._button(CANCEL_BUTTON_ID).label = t(self._language, "cancel_button")

        def _refresh_language_texts(self) -> None:
            self._language_widget().prompt = t(self._language, "language_label")
            self._project_widget().prompt = t(self._language, "project_select_label")
            self._path_widget().placeholder = t(self._language, "project_path_placeholder")
            self._mode_widget().prompt = t(self._language, "mode_label")
            self._mode_widget().set_options(self._mode_options())
            self._include_skills_widget().label = t(self._language, "include_skills_label")
            self._overwrite_existing_widget().label = t(self._language, "overwrite_existing_label")
            self._confirm_widget().placeholder = t(self._language, "confirm_placeholder")
            self._refresh_button_labels()
            self.query_one(f"#{APP_INTRO_ID}", Static).update(t(self._language, "app_intro"))
            self.query_one(f"#{SPEC_DRIVEN_HELP_ID}", Static).update(t(self._language, "spec_driven_help"))
            self.query_one(f"#{LIVING_DOCS_HELP_ID}", Static).update(t(self._language, "living_docs_help"))
            self.query_one(f"#{SKILLS_HELP_ID}", Static).update(t(self._language, "skills_help"))
            self.query_one(f"#{DRY_RUN_HELP_ID}", Static).update(t(self._language, "dry_run_help"))
            self.query_one(f"#{STATUS_HELP_ID}", Static).update(t(self._language, "status_help"))

        def _recent_and_detected_projects(self) -> list[Path]:
            candidates = load_recent_projects()
            candidates.extend(scan_project_dirs())
            unique: list[Path] = []
            seen: set[Path] = set()
            for candidate in candidates:
                if candidate in seen:
                    continue
                seen.add(candidate)
                unique.append(candidate)
            return unique

        def _refresh_projects(self) -> None:
            projects = self._recent_and_detected_projects()
            project_select = self._project_widget()
            if not projects:
                project_select.disabled = True
                project_select.set_options([(t(self._language, "no_projects_found"), "__none__")])
                project_select.value = Select.NULL
                self._project_message_widget().update(t(self._language, "no_projects_found"))
                return

            project_select.disabled = False
            options = [(format_project_choice(project), str(project)) for project in projects]
            project_select.set_options(options)
            current_path = self._path_widget().value.strip()
            if current_path:
                current = str(Path(current_path).expanduser().resolve())
                values = {value for _, value in options}
                project_select.value = current if current in values else Select.NULL
            else:
                project_select.value = Select.NULL
            self._project_message_widget().update("")

        def _read_settings(self) -> tuple[str, str, bool, bool]:
            path = self._path_widget().value.strip() or "."
            mode_value = self._mode_widget().value
            mode = mode_value if isinstance(mode_value, str) and mode_value in {"recommended", "spec-driven", "living-docs"} else "recommended"
            include_skills = bool(self._include_skills_widget().value)
            force = bool(self._overwrite_existing_widget().value)
            return path, mode, include_skills, force

        def _show_plan(self, plan: BootstrapPlan) -> None:
            table = self.query_one(f"#{PREVIEW_TABLE_ID}", DataTable)
            table.clear()
            for item in plan.results:
                table.add_row(str(item.path), item.status, item.kind, item.message)

        def _update_path(self, value: str) -> None:
            self._path_widget().value = value

        def _set_path_to_project(self, value: str) -> None:
            self._update_path(value)
            self._refresh_projects()
            self._refresh_preview()

        def _refresh_preview(self) -> None:
            try:
                path, mode, include_skills, force = self._read_settings()
                plan = _plan_from_ui(path, mode, include_skills, dry_run=True, force=force)
            except ValueError as exc:
                self._current_plan = None
                self._set_status(str(exc))
                return

            self._current_plan = plan
            self._show_plan(plan)
            self._set_status(t(self._language, "preview_ready"))

        def _dry_run(self) -> None:
            path, mode, include_skills, force = self._read_settings()

            try:
                plan = _plan_from_ui(path, mode, include_skills, dry_run=True, force=force)
            except ValueError as exc:
                self._current_plan = None
                self._set_status(str(exc))
                return

            self._current_plan = plan
            self._show_plan(plan)
            apply_plan(plan, dry_run=True)
            self._set_status(t(self._language, "dry_run_done"))

        def _apply(self) -> None:
            path, mode, include_skills, force = self._read_settings()
            confirm = self._confirm_widget().value.strip().upper()

            if confirm != "APPLY":
                self._set_status(t(self._language, "type_apply"))
                return

            try:
                plan = _plan_from_ui(path, mode, include_skills, dry_run=False, force=force)
            except ValueError as exc:
                self._current_plan = None
                self._set_status(str(exc))
                return

            self._current_plan = plan
            self._show_plan(plan)
            results = apply_plan(plan, dry_run=False)

            state = build_state(plan=plan, results=results, tool_version=__version__)
            save_state(state_path(plan.target), state, dry_run=False)
            try:
                add_recent_project(plan.target)
            except OSError:
                pass
            self._refresh_projects()
            self._set_status(t(self._language, "applied_done"))

        def action_quit(self) -> None:
            self.exit(0)

        def on_select_changed(self, event) -> None:
            if event.control.id == LANGUAGE_SELECT_ID:
                self._language = event.value if event.value in SUPPORTED_LANGUAGES else "en"
                self._refresh_language_texts()
                self._refresh_projects()
                self._refresh_preview()
                return

            if event.control.id == PROJECT_SELECT_ID:
                if event.value in {None, "", "__none__"}:
                    return
                self._update_path(str(event.value))
                self._refresh_preview()

        def on_input_changed(self, event) -> None:
            if event.control.id == PATH_INPUT_ID:
                self._refresh_preview()

        def on_checkbox_changed(self, event) -> None:
            if event.control.id in {INCLUDE_SKILLS_ID, OVERWRITE_EXISTING_ID}:
                self._refresh_preview()

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
            elif button_id == CURRENT_DIRECTORY_BUTTON_ID:
                self._set_path_to_project(".")
            elif button_id == HOME_BUTTON_ID:
                self._set_path_to_project(str(Path.home()))
            elif button_id == PARENT_BUTTON_ID:
                current = Path(self._path_widget().value.strip() or ".").expanduser()
                try:
                    parent = current.resolve().parent
                except OSError:
                    parent = current.parent
                self._set_path_to_project(str(parent))
            elif button_id == REFRESH_PROJECTS_BUTTON_ID:
                self._refresh_projects()
                self._refresh_preview()

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
