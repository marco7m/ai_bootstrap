from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from ai_workflow_bootstrap import cli


class CliTests(unittest.TestCase):
    def test_dry_run_completes_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = cli.main(["--dry-run", str(target)])

            self.assertEqual(exit_code, 0)
            self.assertEqual(list(target.iterdir()), [])


if __name__ == "__main__":
    unittest.main()

