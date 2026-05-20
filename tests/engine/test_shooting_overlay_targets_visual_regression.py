import unittest
from pathlib import Path


_OGL = Path("app/viewer/opengl_view.py")
_SHOOT_LAYER = Path("app/viewer/rendering/layers/shooting.py")
_TARGETS_OVERLAY = Path("app/viewer/rendering/layers/shooting_targets_overlay.py")
_HIT_TEST = Path("app/viewer/rendering/hit_test.py")


class TestShootingOverlayTargetsVisualRegression(unittest.TestCase):
    def test_targets_overlay_draw_function_exists(self):
        board = _OGL.read_text(encoding="utf-8")
        overlay = _TARGETS_OVERLAY.read_text(encoding="utf-8")
        self.assertIn("def _draw_shooting_targets_overlay(", board)
        for needle in ('"VALID"', '"NO_LOS"', '"OBSCURED"'):
            self.assertIn(needle, overlay)

    def test_target_hitbox_fallback_exists(self):
        board = _OGL.read_text(encoding="utf-8")
        hit_src = _HIT_TEST.read_text(encoding="utf-8")
        self.assertIn("def _target_hitbox_for_info(self, info: Dict[str, object]) -> Optional[QtCore.QRectF]:", board)
        self.assertIn("target_hitbox_for_shoot_info", board)
        self.assertIn('safe_int(info.get("unit_id"))', hit_src)

    def test_hover_marker_and_hover_hit_test_present(self):
        board = _OGL.read_text(encoding="utf-8")
        overlay = _TARGETS_OVERLAY.read_text(encoding="utf-8")
        self.assertIn("def _update_shooting_hover_target(self, screen_pos: QtCore.QPointF) -> None:", board)
        marker_line = 'painter.drawText(marker_bg, QtCore.Qt.AlignCenter, "' + "\U0001f3af" + '")'
        self.assertIn(marker_line, overlay)
        self.assertIn("self._shoot_hovered_target_key", board)

    def test_rapid_fire_cells_overlay_pattern_present(self):
        source = _OGL.read_text(encoding="utf-8")
        self.assertIn("self._shoot_rapid_range_highlights", source)
        self.assertIn("def _resolve_rapid_fire_cells_range(", source)
        self.assertIn("def _rapid_fire_hatch_brush(", source)

    def test_rapid_fire_detection_handles_compact_token(self):
        source = _OGL.read_text(encoding="utf-8")
        self.assertIn('"rapidfire"', source)

    def test_cells_fx_imports_and_zone_styles_are_used(self):
        shooting_src = _SHOOT_LAYER.read_text(encoding="utf-8")
        self.assertIn("from app.viewer.cells_fx import (", shooting_src)
        self.assertIn("SHOOTING_FULL_ZONE_STYLE", shooting_src)
        self.assertIn("SHOOTING_RAPID_ZONE_STYLE", shooting_src)
        self.assertIn("zone_fill_color(SHOOTING_FULL_ZONE_STYLE)", shooting_src)
        self.assertIn("zone_border_pen(SHOOTING_FULL_ZONE_STYLE)", shooting_src)
        self.assertIn("zone_border_pen(SHOOTING_RAPID_ZONE_STYLE)", shooting_src)

    def test_rapid_hatch_helper_reads_cells_fx_params(self):
        source = _OGL.read_text(encoding="utf-8")
        self.assertIn("SHOOTING_RAPID_HATCH_STYLE.tile_size", source)
        self.assertIn("rapid_hatch_pen(SHOOTING_RAPID_HATCH_STYLE)", source)
        self.assertIn("for x1, y1, x2, y2 in SHOOTING_RAPID_HATCH_STYLE.lines", source)


    def test_range_overlay_not_shrunk_by_target_filter(self):
        source = _OGL.read_text(encoding="utf-8")
        self.assertIn("if max_dist > 0 and (inferred_range is None or inferred_range <= 0):", source)
        self.assertIn("не сужаем range до набора текущих валидных целей", source)

    def test_shoot_range_debug_logs_present(self):
        source = _OGL.read_text(encoding="utf-8")
        self.assertIn("[VIEWER][SHOOT_RANGE]", source)
        self.assertIn("[VIEWER][SHOOT_RANGE][CELLS]", source)
        self.assertIn("Что случилось:", source)
        self.assertIn("Что делать дальше:", source)

    def test_fire_popover_stage_resolved_from_request(self):
        source = Path("app/viewer/app.py").read_text(encoding="utf-8")
        self.assertIn("def _resolve_shoot_stage(self, request) -> str:", source)
        self.assertIn("self._shoot_ui_stage = self._resolve_shoot_stage(request)", source)
        self.assertIn("stage in {\"hit\", \"wound\", \"save\"}", source)

    def test_fire_step_action_uses_stage_not_hardcoded_step_index(self):
        source = Path("app/viewer/app.py").read_text(encoding="utf-8")
        self.assertIn("stage = self._resolve_shoot_stage(req)", source)
        self.assertIn("if stage == \"target\":", source)
        self.assertIn("if stage in {\"hit\", \"wound\", \"save\"}:", source)
    def test_cells_fx_module_contains_editable_overlay_settings(self):
        source = Path("app/viewer/cells_fx.py").read_text(encoding="utf-8")
        self.assertIn("class CellsZoneStyle", source)
        self.assertIn("class RapidHatchStyle", source)
        self.assertIn("SHOOTING_FULL_ZONE_STYLE", source)
        self.assertIn("SHOOTING_RAPID_ZONE_STYLE", source)
        self.assertIn("SHOOTING_RAPID_HATCH_STYLE", source)


if __name__ == "__main__":
    unittest.main()

