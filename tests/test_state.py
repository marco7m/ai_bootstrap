from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_workflow_bootstrap.core.state import load_state, new_state, save_state, state_path


class StateTests(unittest.TestCase):
    def test_state_round_trip(self) -> None:
        # State is prepared infrastructure here, not yet part of the CLI flow.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = state_path(root)
            state = new_state(
                target_path=str(root),
                template_pack="default",
                template_pack_version="0.1.0",
                enabled_workflows=["spec-driven"],
                tool_version="0.1.0",
                files={
                    "AGENTS.md": {
                        "status": "written",
                        "template": "templates/AGENTS.md",
                        "template_hash": "abc123",
                    }
                },
                optional_modules=[],
            )

            save_state(path, state)
            loaded = load_state(path)

            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.tool_name, "ai-workflow-bootstrap")
            self.assertEqual(loaded.template_pack, "default")
            self.assertEqual(loaded.enabled_workflows, ["spec-driven"])
            self.assertEqual(loaded.files["AGENTS.md"]["template_hash"], "abc123")


if __name__ == "__main__":
    unittest.main()
