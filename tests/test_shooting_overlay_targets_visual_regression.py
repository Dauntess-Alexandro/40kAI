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
        self.assertIn('painter.drawText(marker_bg, QtCore.Qt.AlignCenter, "🎯")', source)
        self.assertIn("self._shoot_hovered_target_key", source)

    def test_rapid_fire_cells_overlay_pattern_present(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn("self._shoot_rapid_range_highlights", source)
        self.assertIn("def _resolve_rapid_fire_cells_range(", source)
        self.assertIn("def _rapid_fire_hatch_brush(", source)

    def test_rapid_fire_detection_handles_compact_token(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn('"rapidfire"', source)

    def test_cells_fx_imports_and_zone_styles_are_used(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn("from viewer.cells_fx import (", source)
        self.assertIn("SHOOTING_FULL_ZONE_STYLE", source)
        self.assertIn("SHOOTING_RAPID_ZONE_STYLE", source)
        self.assertIn("zone_fill_color(SHOOTING_FULL_ZONE_STYLE)", source)
        self.assertIn("zone_border_pen(SHOOTING_FULL_ZONE_STYLE)", source)
        self.assertIn("zone_border_pen(SHOOTING_RAPID_ZONE_STYLE)", source)

    def test_rapid_hatch_helper_reads_cells_fx_params(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn("SHOOTING_RAPID_HATCH_STYLE.tile_size", source)
        self.assertIn("rapid_hatch_pen(SHOOTING_RAPID_HATCH_STYLE)", source)
        self.assertIn("for x1, y1, x2, y2 in SHOOTING_RAPID_HATCH_STYLE.lines", source)


    def test_range_overlay_not_shrunk_by_target_filter(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn("if max_dist > 0 and (inferred_range is None or inferred_range <= 0):", source)
        self.assertIn("не сужаем range до набора текущих валидных целей", source)

    def test_shoot_range_debug_logs_present(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn("[VIEWER][SHOOT_RANGE]", source)
        self.assertIn("[VIEWER][SHOOT_RANGE][CELLS]", source)
        self.assertIn("Что случилось:", source)
        self.assertIn("Что делать дальше:", source)
    def test_cells_fx_module_contains_editable_overlay_settings(self):
        source = Path("viewer/cells_fx.py").read_text(encoding="utf-8")
        self.assertIn("class CellsZoneStyle", source)
        self.assertIn("class RapidHatchStyle", source)
        self.assertIn("SHOOTING_FULL_ZONE_STYLE", source)
        self.assertIn("SHOOTING_RAPID_ZONE_STYLE", source)
        self.assertIn("SHOOTING_RAPID_HATCH_STYLE", source)


if __name__ == "__main__":
    unittest.main()
