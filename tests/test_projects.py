from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.projects import (
    add_recent_project,
    format_project_choice,
    is_project_dir,
    load_recent_projects,
    save_recent_projects,
    scan_project_dirs,
)


class ProjectHelperTests(unittest.TestCase):
    def _make_project(self, root: Path, name: str, marker: str = "pyproject.toml") -> Path:
        project = root / name
        project.mkdir(parents=True, exist_ok=True)
        if marker == ".git":
            (project / marker).mkdir()
        else:
            (project / marker).write_text("", encoding="utf-8")
        return project

    def test_load_recent_missing_file_returns_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            storage = Path(tmp) / "recent.json"
            self.assertEqual(load_recent_projects(storage), [])

    def test_load_recent_invalid_json_returns_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            storage = Path(tmp) / "recent.json"
            storage.write_text("{not json", encoding="utf-8")
            self.assertEqual(load_recent_projects(storage), [])

    def test_save_load_deduplicates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self._make_project(root, "one")
            second = self._make_project(root, "two")
            storage = root / "recent.json"

            save_recent_projects([first, first, second], storage)

            self.assertEqual(load_recent_projects(storage), [first.resolve(), second.resolve()])
            payload = json.loads(storage.read_text(encoding="utf-8"))
            self.assertEqual(payload["recent_projects"], [str(first.resolve()), str(second.resolve())])

    def test_add_recent_moves_existing_to_top(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self._make_project(root, "one")
            second = self._make_project(root, "two")
            storage = root / "recent.json"
            save_recent_projects([first, second], storage)

            updated = add_recent_project(second, storage)

            self.assertEqual(updated, [second.resolve(), first.resolve()])
            self.assertEqual(load_recent_projects(storage), [second.resolve(), first.resolve()])

    def test_add_recent_limits_to_ten(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            storage = root / "recent.json"
            projects = [self._make_project(root, f"project-{index}") for index in range(11)]

            for project in projects:
                add_recent_project(project, storage, limit=10)

            recent = load_recent_projects(storage)
            self.assertEqual(len(recent), 10)
            self.assertEqual(recent[0], projects[-1].resolve())
            self.assertNotIn(projects[0].resolve(), recent)

    def test_is_project_dir_detects_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            markers = ["pyproject.toml", "package.json", "Cargo.toml", "go.mod", "Makefile", ".git"]

            for marker in markers:
                with self.subTest(marker=marker):
                    project = root / marker.replace(".", "_")
                    project.mkdir()
                    if marker == ".git":
                        (project / marker).mkdir()
                    else:
                        (project / marker).write_text("", encoding="utf-8")
                    self.assertTrue(is_project_dir(project))

    def test_scan_project_dirs_is_shallow_and_deduplicates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            root_project = self._make_project(root, "root-project")
            nested = root / "outer" / "deep-project"
            nested.mkdir(parents=True)
            (nested / "pyproject.toml").write_text("", encoding="utf-8")
            direct = self._make_project(root, "direct-project")
            ignored = root / "node_modules"
            ignored.mkdir()
            (ignored / "ignored-project").mkdir()
            (ignored / "ignored-project" / "pyproject.toml").write_text("", encoding="utf-8")

            scanned = scan_project_dirs([root, root, root / "missing"])

            self.assertEqual(scanned, sorted({root_project.resolve(), direct.resolve()}, key=lambda item: (item.name.casefold(), str(item).casefold())))
            self.assertNotIn(nested.resolve(), scanned)

    def test_format_project_choice_includes_name_and_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project-name"
            project.mkdir()
            choice = format_project_choice(project)
            self.assertIn("project-name", choice)
            self.assertIn(str(project), choice)


if __name__ == "__main__":
    unittest.main()
