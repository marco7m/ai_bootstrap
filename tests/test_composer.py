from __future__ import annotations

import unittest

from ai_workflow_bootstrap.core.composer import compose_ensured_lines, compose_make_targets


REQUIRED = """dev:
\tcargo run

run:
\tcargo run --release
"""


class ComposerTests(unittest.TestCase):
    def test_make_block_is_added_and_reapplication_is_idempotent(self) -> None:
        first = compose_make_targets("custom:\n\t@echo custom\n", REQUIRED, "rust")

        self.assertTrue(first.changed)
        self.assertIn("custom:", first.content)
        self.assertIn("ai-workflow-bootstrap:rust", first.content)
        self.assertIn("cargo run --release", first.content)

        second = compose_make_targets(first.content, REQUIRED, "rust")
        self.assertFalse(second.changed)
        self.assertEqual(second.content, first.content)

    def test_equivalent_unmanaged_target_is_preserved_and_not_duplicated(self) -> None:
        current = "dev:\n\tcargo run\n\ncustom:\n\t@echo custom\n"
        result = compose_make_targets(current, REQUIRED, "rust")

        self.assertIsNone(result.conflict)
        self.assertEqual(result.content.count("dev:"), 1)
        self.assertIn("run:", result.content)
        self.assertTrue(result.content.startswith(current))

    def test_different_or_ambiguous_target_is_a_conflict(self) -> None:
        for current in ("run:\n\tcargo run --features desktop\n", "dev run:\n\tcargo run\n"):
            with self.subTest(current=current):
                result = compose_make_targets(current, REQUIRED, "rust")
                self.assertIsNotNone(result.conflict)
                self.assertIn(result.conflict.target, {"dev", "run"})

    def test_malformed_managed_markers_are_a_conflict(self) -> None:
        result = compose_make_targets("# >>> ai-workflow-bootstrap:rust >>>\ndev:\n\tcargo run\n", REQUIRED, "rust")
        self.assertIsNotNone(result.conflict)
        self.assertEqual(result.conflict.target, "<managed block>")
        self.assertIn("restore exactly one valid marker pair", result.conflict.remediation)

    def test_ensure_lines_accepts_equivalent_and_preserves_existing_text(self) -> None:
        equivalent = compose_ensured_lines("# Cargo\n/target/\n", "target/\n", ("/target/",))
        self.assertFalse(equivalent.changed)

        added = compose_ensured_lines("# Existing", "target/\n", ("/target/",))
        self.assertTrue(added.changed)
        self.assertEqual(added.content, "# Existing\ntarget/\n")

        with self.assertRaisesRegex(ValueError, "exactly one"):
            compose_ensured_lines("", "first\nsecond\n", ("equivalent",))


if __name__ == "__main__":
    unittest.main()
