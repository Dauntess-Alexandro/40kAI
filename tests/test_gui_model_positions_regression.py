import unittest
from pathlib import Path


class TestGuiModelPositionsRegression(unittest.TestCase):
    def test_opengl_view_uses_model_positions_and_anchor(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")

        self.assertIn('def _unit_anchor_state_xy', source)
        self.assertIn('unit.get("anchor_x")', source)
        self.assertIn('model_positions = unit.get("model_positions")', source)
        self.assertIn('render.model_centers', source)

    def test_tooltip_shows_alive_over_total_models(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn('models = f"{alive_models}/{total_models}"', source)

    def test_units_layer_draws_icons_for_models_without_circles(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn("# Без кругов: рисуем только иконки", source)
        self.assertIn("for model_center in model_centers", source)
        self.assertIn("painter.drawPixmap(rect, icon, QtCore.QRectF(icon.rect()))", source)


    def test_icon_scales_are_configurable_for_units_and_models(self):
        app_source = Path("viewer/app.py").read_text(encoding="utf-8")
        view_source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn('"model_icon_scale"', app_source)
        self.assertIn('model_icon_scale=max(0.2, model_icon_scale)', app_source)
        self.assertIn('model_icon_scale: float = 0.75', view_source)
        self.assertIn('self._model_icon_scale', view_source)

    def test_app_world_center_prefers_anchor_coords(self):
        source = Path("viewer/app.py").read_text(encoding="utf-8")
        self.assertIn('anchor_x = unit.get("anchor_x")', source)
        self.assertIn('view_xy = self.map_scene._state_xy_to_view_xy(anchor_x, anchor_y)', source)


if __name__ == "__main__":
    unittest.main()
