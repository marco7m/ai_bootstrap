from __future__ import annotations

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from ai_workflow_bootstrap import cli
from ai_workflow_bootstrap.core.lifecycle import content_hash
from ai_workflow_bootstrap.core.state import new_state, save_state, state_path


def _legacy_pattern(*parts: str) -> str:
    return "".join(parts)


class CliTests(unittest.TestCase):
    def test_help_mentions_tui_default_and_apply(self) -> None:
        help_text = cli.build_parser().format_help()
        apply_help = cli.build_parser()._subparsers._group_actions[0].choices["apply"].format_help()

        self.assertIn("Open the guided TUI by default", help_text)
        self.assertIn("ai-bootstrap tui", help_text)
        self.assertIn("ai-bootstrap apply [path]", help_text)
        self.assertIn("Examples:", help_text)
        self.assertIn("Update divergent bootstrap-managed files", apply_help)
        self.assertIn("--managed-only", apply_help)
        self.assertIn("--reset-project-knowledge", apply_help)
        self.assertNotIn("--no-backup", apply_help)

    def test_removed_no_backup_option_is_rejected(self) -> None:
        stderr = io.StringIO()
        with redirect_stderr(stderr), self.assertRaises(SystemExit):
            cli.build_parser().parse_args(["apply", "--no-backup", "."])
        self.assertIn("unrecognized arguments", stderr.getvalue())

    def test_no_args_opens_tui(self) -> None:
        with mock.patch("ai_workflow_bootstrap.cli._run_tui", return_value=0) as run_tui:
            exit_code = cli.main([])

        self.assertEqual(exit_code, 0)
        run_tui.assert_called_once_with([])

    def test_tui_subcommand_opens_tui(self) -> None:
        with mock.patch("ai_workflow_bootstrap.cli._run_tui", return_value=0) as run_tui:
            exit_code = cli.main(["tui"])

        self.assertEqual(exit_code, 0)
        run_tui.assert_called_once_with([])

    def test_apply_dry_run_completes_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = cli.main(["apply", "--dry-run", str(target)])

            self.assertEqual(exit_code, 0)
            self.assertFalse(state_path(target).exists())
            self.assertNotIn(".cursor", buffer.getvalue())
            self.assertNotIn(".codex", buffer.getvalue())
            self.assertIn(".agents/skills/maintainability-audit/SKILL.md", buffer.getvalue())

    def test_apply_writes_state_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = cli.main(["apply", str(target)])

            self.assertEqual(exit_code, 0)
            state_file = state_path(target)
            self.assertTrue(state_file.exists())
            data = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertEqual(data["tool_name"], "ai-workflow-bootstrap")
            self.assertTrue(os.path.isabs(data["target_path"]))
            self.assertEqual(data["enabled_workflows"], ["spec-driven", "living-docs"])
            self.assertIn("AGENTS.md", data["files"])
            self.assertIn("docs/INDEX.md", data["files"])
            self.assertNotIn("docs/AI_CONTEXT.md", data["files"])
            self.assertIn("docs/CAPABILITIES.md", data["files"])
            self.assertIn("docs/product/README.md", data["files"])
            self.assertIn("docs/architecture/README.md", data["files"])
            self.assertNotIn("docs/PROJECT_SPEC.md", data["files"])
            self.assertIn(".agents/skills/spec-driven/SKILL.md", data["files"])
            self.assertIn(".agents/skills/maintainability-audit/SKILL.md", data["files"])
            self.assertIn(".agents/skills/living-docs/SKILL.md", data["files"])
            self.assertTrue(all(not key.startswith("/") for key in data["files"]))

    def test_force_preview_and_apply_delete_known_legacy_without_backup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            legacy = target / "docs/AI_CONTEXT.md"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("legacy\n", encoding="utf-8")
            save_state(
                state_path(target),
                new_state(
                    target_path=str(target),
                    template_pack="default",
                    template_pack_version="0.4.0",
                    enabled_workflows=["spec-driven", "living-docs"],
                    tool_version="0.1.0",
                    files={
                        "docs/AI_CONTEXT.md": {
                            "status": "written",
                            "applied_content_hash": content_hash("legacy\n"),
                        }
                    },
                ),
            )
            preview = io.StringIO()
            with redirect_stdout(preview):
                self.assertEqual(cli.main(["apply", "--force", "--dry-run", str(target)]), 0)

            self.assertTrue(legacy.exists())
            self.assertIn("deleted", preview.getvalue())

            applied = io.StringIO()
            with redirect_stdout(applied):
                self.assertEqual(cli.main(["apply", "--force", str(target)]), 0)

            self.assertFalse(legacy.exists())
            self.assertEqual(list(target.rglob("*.bak-*")), [])

    def test_untracked_obsolete_file_blocks_apply_before_any_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            legacy = target / "docs/PROJECT_SPEC.md"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("project knowledge\n", encoding="utf-8")
            stderr = io.StringIO()

            with redirect_stderr(stderr):
                exit_code = cli.main(["apply", "--force", str(target)])

            self.assertEqual(exit_code, 2)
            self.assertIn("migration_required", stderr.getvalue())
            self.assertTrue(legacy.exists())
            self.assertFalse((target / "AGENTS.md").exists())
            self.assertFalse(state_path(target).exists())

    def test_seeded_reset_requires_separate_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(cli.main(["apply", str(target)]), 0)
            index = target / "docs/INDEX.md"
            rendered = index.read_text(encoding="utf-8")
            index.write_text("# Project knowledge\n", encoding="utf-8")

            stderr = io.StringIO()
            with redirect_stderr(stderr):
                exit_code = cli.main(["apply", "--reset-project-knowledge", str(target)])
            self.assertEqual(exit_code, 2)
            self.assertIn("RESET PROJECT KNOWLEDGE", stderr.getvalue())
            self.assertEqual(index.read_text(encoding="utf-8"), "# Project knowledge\n")

            preview = io.StringIO()
            with redirect_stdout(preview):
                self.assertEqual(
                    cli.main(["apply", "--reset-project-knowledge", "--dry-run", str(target)]),
                    0,
                )
            self.assertIn("reset", preview.getvalue())
            self.assertEqual(index.read_text(encoding="utf-8"), "# Project knowledge\n")

            self.assertEqual(
                cli.main(
                    [
                        "apply",
                        "--reset-project-knowledge",
                        "--confirm-reset-project-knowledge",
                        "RESET PROJECT KNOWLEDGE",
                        str(target),
                    ]
                ),
                0,
            )
            self.assertEqual(index.read_text(encoding="utf-8"), rendered)

    def test_managed_only_keeps_seeded_state_and_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.assertEqual(cli.main(["apply", str(target)]), 0)
            before = json.loads(state_path(target).read_text(encoding="utf-8"))
            index = target / "docs/INDEX.md"
            index.write_text("# Project knowledge\n", encoding="utf-8")
            (target / "AGENTS.md").write_text("# Old managed\n", encoding="utf-8")

            self.assertEqual(cli.main(["apply", "--force", "--managed-only", str(target)]), 0)

            after = json.loads(state_path(target).read_text(encoding="utf-8"))
            self.assertEqual(index.read_text(encoding="utf-8"), "# Project knowledge\n")
            self.assertEqual(
                after["files"]["docs/INDEX.md"]["applied_content_hash"],
                before["files"]["docs/INDEX.md"]["applied_content_hash"],
            )
            self.assertIn("Project:", (target / "AGENTS.md").read_text(encoding="utf-8"))

    def test_removed_partial_workflow_options_are_rejected(self) -> None:
        for option in ("--no-living-docs", "--living-docs-only"):
            with self.subTest(option=option):
                stderr = io.StringIO()
                with redirect_stderr(stderr), self.assertRaises(SystemExit):
                    cli.build_parser().parse_args(["apply", option, "."])
                self.assertIn("unrecognized arguments", stderr.getvalue())

    def test_make_conflict_returns_actionable_error_without_writes_or_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "Cargo.toml").write_text("[workspace]\nmembers=[]\n", encoding="utf-8")
            (target / "Makefile").write_text("run:\n\tcargo run --features desktop\n", encoding="utf-8")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                exit_code = cli.main(["apply", "--force", str(target)])

            self.assertEqual(exit_code, 2)
            message = stderr.getvalue()
            self.assertIn("Current definition", message)
            self.assertIn("cargo run --features desktop", message)
            self.assertIn("cargo run --release", message)
            self.assertIn("--force does not bypass repository-owned file conflicts", message)
            self.assertIn("rerun the bootstrap", message)
            self.assertFalse((target / "AGENTS.md").exists())
            self.assertFalse(state_path(target).exists())

    def test_dry_run_does_not_write_state_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = cli.main(["apply", "--dry-run", str(target)])

            self.assertEqual(exit_code, 0)
            self.assertFalse(state_path(target).exists())

    def test_no_args_without_textual_shows_message_and_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            original_cwd = Path.cwd()
            os.chdir(tmp)
            try:
                stderr = io.StringIO()
                with mock.patch(
                    "ai_workflow_bootstrap.tui._load_textual",
                    side_effect=ImportError('Textual is required for the TUI.\nInstall with:\npip install -e ".[tui]"'),
                ):
                    with redirect_stderr(stderr):
                        exit_code = cli.main([])

                self.assertEqual(exit_code, 1)
                self.assertIn("Textual is required for the TUI.", stderr.getvalue())
                self.assertFalse(any(Path(tmp).iterdir()))
            finally:
                os.chdir(original_cwd)

    def test_bootstrap_sdd_is_a_thin_launcher(self) -> None:
        path = Path("bootstrap_sdd.py")
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")

        self.assertLessEqual(len(text.splitlines()), 12)
        self.assertIn("from ai_workflow_bootstrap.cli import main", text)
        self.assertIn("raise SystemExit(main(sys.argv[1:]))", text)
        self.assertNotIn(_legacy_pattern(".", "cur", "sor/plans"), text)
        self.assertNotIn(_legacy_pattern(".", "cur", "sor/rules"), text)
        self.assertNotIn(_legacy_pattern("global ", "Codex"), text)
        self.assertNotIn(_legacy_pattern("Codex ", "or Cursor"), text)
        self.assertNotIn(_legacy_pattern("--global-", "codex"), text)
        self.assertNotIn(_legacy_pattern("--no-", "cursor"), text)


if __name__ == "__main__":
    unittest.main()
