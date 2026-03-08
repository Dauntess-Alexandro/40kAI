import unittest
from pathlib import Path


class TestShootingOverlayTargetsVisualRegression(unittest.TestCase):
    def test_targets_overlay_draw_function_exists(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn("def _draw_shooting_targets_overlay(", source)
        self.assertIn('"VALID"', source)
        self.assertIn('"NO_LOS"', source)
        self.assertIn('"OBSCURED"', source)

    def test_hover_marker_and_hover_hit_test_present(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn("def _update_shooting_hover_target(self, screen_pos: QtCore.QPointF) -> None:", source)
        self.assertIn('painter.drawText(marker_bg, QtCore.Qt.AlignCenter, "🎯")', source)
        self.assertIn("self._shoot_hovered_target_key", source)


if __name__ == "__main__":
    unittest.main()
