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

    def test_app_world_center_prefers_anchor_coords(self):
        source = Path("viewer/app.py").read_text(encoding="utf-8")
        self.assertIn('anchor_x = unit.get("anchor_x")', source)
        self.assertIn('view_xy = self.map_scene._state_xy_to_view_xy(anchor_x, anchor_y)', source)


if __name__ == "__main__":
    unittest.main()
