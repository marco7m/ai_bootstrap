from __future__ import annotations

import unittest

from ai_workflow_bootstrap.core.lifecycle import (
    MANAGED,
    SEEDED,
    classify_rendered_file,
    content_hash,
    is_content_hash,
)


class LifecycleTests(unittest.TestCase):
    def test_managed_and_seeded_decision_matrix(self) -> None:
        rendered = content_hash("new\n")
        old = content_hash("old\n")
        custom = content_hash("custom\n")
        cases = [
            ("managed missing", MANAGED, False, None, None, False, False, "written"),
            ("managed equal", MANAGED, True, rendered, None, False, False, "unchanged"),
            ("managed safe", MANAGED, True, old, old, False, False, "skipped"),
            ("managed force", MANAGED, True, old, old, True, False, "overwritten"),
            ("seed missing", SEEDED, False, None, None, True, False, "written"),
            ("seed equal", SEEDED, True, rendered, None, True, False, "unchanged"),
            ("seed untouched", SEEDED, True, old, old, True, False, "updated"),
            ("seed drift", SEEDED, True, custom, old, True, False, "preserved"),
            ("seed no state", SEEDED, True, custom, None, True, False, "preserved"),
            ("seed reset", SEEDED, True, custom, old, False, True, "reset"),
        ]

        for name, lifecycle, exists, current, prior, force, reset, expected in cases:
            with self.subTest(name=name):
                decision = classify_rendered_file(
                    lifecycle=lifecycle,
                    exists=exists,
                    current_hash=current,
                    rendered_hash=rendered,
                    prior_applied_hash=prior,
                    force=force,
                    reset_project_knowledge=reset,
                )
                self.assertEqual(decision.status, expected)

    def test_hash_is_exact_for_line_endings_and_trailing_newline(self) -> None:
        self.assertNotEqual(content_hash("value"), content_hash("value\n"))
        self.assertNotEqual(content_hash("value\n"), content_hash("value\r\n"))
        self.assertTrue(is_content_hash(content_hash("value\n")))
        self.assertFalse(is_content_hash("not-a-hash"))

    def test_invalid_rendered_lifecycle_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported rendered-file lifecycle"):
            classify_rendered_file(
                lifecycle="project",
                exists=False,
                current_hash=None,
                rendered_hash=content_hash("new\n"),
                prior_applied_hash=None,
                force=False,
                reset_project_knowledge=False,
            )


if __name__ == "__main__":
    unittest.main()
