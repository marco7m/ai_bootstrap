from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.template_pack import load_default_template_pack


def _checker() -> Path:
    return load_default_template_pack().template_path(
        "templates/.agents/skills/living-docs/scripts/check_living_docs.py"
    )


def _write_docs(root: Path, *, status: str = "scaffold", capability_rows: str = "") -> None:
    (root / "docs/product").mkdir(parents=True, exist_ok=True)
    (root / "docs/architecture").mkdir(parents=True, exist_ok=True)
    (root / "docs/INDEX.md").write_text(
        f"# Index\n\n- Knowledge status: `{status}`\n- Baseline evidence: _not established_\n",
        encoding="utf-8",
    )
    (root / "docs/CAPABILITIES.md").write_text(
        "# Capabilities\n\n"
        "| Capability | Product contract | Architecture | Current state | Evidence | Approved target | Active change |\n"
        "| --- | --- | --- | --- | --- | --- | --- |\n"
        + capability_rows,
        encoding="utf-8",
    )
    (root / "docs/product/README.md").write_text("# Product\n", encoding="utf-8")
    (root / "docs/architecture/README.md").write_text("# Architecture\n", encoding="utf-8")


class LivingDocsCheckerTests(unittest.TestCase):
    def _run(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(_checker()), str(root), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_clean_scaffold_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_docs(root)
            result = self._run(root)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_verified_capability_with_scaffold_and_legacy_overwrite_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_docs(
                root,
                capability_rows=(
                    "| Play | [Product](product/README.md) | [Architecture](architecture/README.md) "
                    "| `verified` | tests | — | — |\n"
                ),
            )
            state_path = root / ".ai-bootstrap/state.json"
            state_path.parent.mkdir()
            state_path.write_text(
                json.dumps(
                    {
                        "files": {
                            "docs/INDEX.md": {"status": "overwritten"},
                            "docs/CAPABILITIES.md": {"status": "overwritten"},
                        }
                    }
                ),
                encoding="utf-8",
            )

            result = self._run(root)

            self.assertEqual(result.returncode, 1)
            self.assertIn("scaffold/unestablished", result.stderr)
            self.assertIn("overwritten seeded owners", result.stderr)

    def test_git_baseline_reports_downgrade_and_removed_capability(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_docs(
                root,
                status="incomplete",
                capability_rows=(
                    "| Play | [Product](product/README.md) | [Architecture](architecture/README.md) "
                    "| `verified` | tests | — | — |\n"
                ),
            )
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
            subprocess.run(["git", "-C", str(root), "add", "docs"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "baseline"], check=True)
            _write_docs(root, status="scaffold")

            result = self._run(root, "--baseline-ref", "HEAD")

            self.assertEqual(result.returncode, 1)
            self.assertIn("downgraded from incomplete to scaffold", result.stderr)
            self.assertIn("capability removed since HEAD: Play", result.stderr)


if __name__ == "__main__":
    unittest.main()
