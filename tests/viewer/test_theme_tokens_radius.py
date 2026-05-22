"""Theme v2 radius/spacing/font fields."""

from __future__ import annotations

import unittest

from app.viewer.styles import Theme
from app.viewer.theme.tokens import palette_from_tokens


class TestThemeTokensRadius(unittest.TestCase):
    def test_palette_has_spacing_and_fonts(self) -> None:
        pal = palette_from_tokens()
        self.assertGreaterEqual(pal.spacing_md, 8)
        self.assertGreaterEqual(pal.header_font_size, 10)
        self.assertGreaterEqual(pal.mono_font_size, 10)
        Theme.apply_from_config({"flags": {"viewer.theme.v2": True}})
        self.assertEqual(Theme.spacing_md, pal.spacing_md)
        Theme.set_ui_scale(1.25)
        body = Theme.scaled_ui_font_size()
        self.assertEqual(body, max(8, round(pal.ui_font_size * 1.25)))
        self.assertEqual(max(8, round(body * 0.82)), max(8, round(Theme.scaled_ui_font_size() * 0.82)))


if __name__ == "__main__":
    unittest.main()
