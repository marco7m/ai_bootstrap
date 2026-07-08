from __future__ import annotations

import unittest

from ai_workflow_bootstrap.core.renderer import render_template


class RendererTests(unittest.TestCase):
    def test_renders_placeholders_and_normalizes_trailing_newline(self) -> None:
        rendered = render_template("Hello $name\n\n", {"name": "world"})

        self.assertEqual(rendered, "Hello world\n")

    def test_leaves_literal_braces_intact(self) -> None:
        rendered = render_template("Keep {braces} and $name", {"name": "world"})

        self.assertEqual(rendered, "Keep {braces} and world\n")


if __name__ == "__main__":
    unittest.main()
