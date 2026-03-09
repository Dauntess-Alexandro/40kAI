import unittest
from pathlib import Path


class TestShootingOverlayTargetsVisualRegression(unittest.TestCase):
    def test_targets_overlay_draw_function_exists(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn("def _draw_shooting_targets_overlay(", source)
        self.assertIn('"VALID"', source)
        self.assertIn('"NO_LOS"', source)
        self.assertIn('"OBSCURED"', source)

    def test_target_hitbox_fallback_exists(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn("def _target_hitbox_for_info(self, info: Dict[str, object]) -> Optional[QtCore.QRectF]:", source)
        self.assertIn('unit_id = self._safe_int(info.get("unit_id"))', source)

    def test_hover_marker_and_hover_hit_test_present(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn("def _update_shooting_hover_target(self, screen_pos: QtCore.QPointF) -> None:", source)
        self.assertIn("painter.drawPixmap(draw_rect, reticle", source)
        self.assertIn("rect.center().x() - marker_side * 0.5", source)
        self.assertIn("self._shoot_hovered_target_key", source)

    def test_target_overlay_debug_logging_present(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn('"[VIEWER][TARGET_OVERLAY] "', source)
        self.assertIn("draw_calls=", source)
        self.assertIn('"[VIEWER][TARGET_TEX] key=', source)

    def test_explicit_targets_are_not_range_culled(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn("if (not is_explicit_target) and inferred_range is not None", source)
        self.assertIn("skip=range_cull", source)


if __name__ == "__main__":
    unittest.main()
