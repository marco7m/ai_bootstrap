from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.backup import backup_path, create_backup


class BackupTests(unittest.TestCase):
    def test_backup_path_uses_expected_suffix(self) -> None:
        path = Path("/tmp/example.txt")

        candidate = backup_path(path)

        self.assertTrue(candidate.name.startswith("example.txt.bak-"))

    def test_create_backup_copies_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "example.txt"
            source.write_text("hello\n", encoding="utf-8")

            backup = create_backup(source)

            self.assertTrue(backup.exists())
            self.assertEqual(backup.read_text(encoding="utf-8"), "hello\n")


if __name__ == "__main__":
    unittest.main()

