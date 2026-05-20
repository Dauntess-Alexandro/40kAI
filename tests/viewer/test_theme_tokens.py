"""Sprint 2 — shared theme tokens and viewer palette."""

from __future__ import annotations

import os
import unittest

from app.viewer.config import load_viewer_config, viewer_flag
from app.viewer.styles import Theme
from app.viewer.theme.tokens import palette_from_tokens, resolve_palette
from theme.loader import contrast_ratio, load_tokens, load_tokens_flat_for_qml, validate_tokens


class TestThemeTokens(unittest.TestCase):
    def test_load_and_validate_tokens(self) -> None:
        data = load_tokens()
        validate_tokens(data)
        self.assertEqual(data["schema_version"], 1)

    def test_flat_qml_keys(self) -> None:
        flat = load_tokens_flat_for_qml()
        for key in (
            "bgBase",
            "bgSurface",
            "textPrimary",
            "accentP1",
            "accentPrimaryAction",
        ):
            self.assertIn(key, flat)
            self.assertTrue(flat[key].startswith("#"))

    def test_contrast_text_on_surface_wcag_aa(self) -> None:
        flat = load_tokens_flat_for_qml()
        ratio = contrast_ratio(flat["textPrimary"], flat["bgSurface"])
        self.assertGreaterEqual(ratio, 4.5, f"textPrimary on bgSurface ratio={ratio:.2f}")

    def test_palette_v2_differs_from_legacy(self) -> None:
        v2 = palette_from_tokens()
        legacy = resolve_palette({"flags": {"viewer.theme.v2": False}})
        self.assertNotEqual(v2.background.name(), legacy.background.name())
        self.assertEqual(v2.background.name(), "#0f172a")

    def test_viewer_flag_env_override(self) -> None:
        os.environ["VIEWER_FLAG_VIEWER_THEME_V2"] = "1"
        try:
            self.assertTrue(viewer_flag("viewer.theme.v2", load_viewer_config()))
        finally:
            os.environ.pop("VIEWER_FLAG_VIEWER_THEME_V2", None)

    def test_theme_apply_v2_via_config(self) -> None:
        cfg = load_viewer_config()
        cfg = dict(cfg)
        cfg["flags"] = dict(cfg.get("flags") or {})
        cfg["flags"]["viewer.theme.v2"] = True
        Theme.apply_from_config(cfg)
        self.assertTrue(Theme.is_v2(cfg))
        self.assertEqual(Theme.background.name(), "#0f172a")


if __name__ == "__main__":
    unittest.main()
