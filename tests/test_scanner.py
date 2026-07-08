from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.scanner import detect_repo_profile, detect_project_name


class ScannerTests(unittest.TestCase):
    def test_detects_basic_repo_hints(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Makefile").write_text(
                "build:\n\t@echo build\ntest:\n\t@echo test\nlint:\n\t@echo lint\n",
                encoding="utf-8",
            )
            (root / "package.json").write_text(
                '{"scripts": {"dev": "node index.js"}}',
                encoding="utf-8",
            )
            (root / "src").mkdir()
            (root / "tests").mkdir()

            profile = detect_repo_profile(root, detect_project_name(root, "Example"))

            self.assertIn("make", profile.detected_stacks)
            self.assertIn("node", profile.detected_stacks)
            self.assertEqual(profile.package_manager, "npm")
            self.assertEqual(profile.commands["build"], "make build")
            self.assertEqual(profile.commands["test"], "make test")
            self.assertEqual(profile.commands["lint"], "make lint")
            self.assertEqual(profile.commands["dev"], "npm run dev")
            self.assertEqual(profile.top_dirs, ["src", "tests"])


if __name__ == "__main__":
    unittest.main()

