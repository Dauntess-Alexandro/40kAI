import unittest
from pathlib import Path


class DeadUnitsVisualFilterRegressionTest(unittest.TestCase):
    def test_state_export_skips_dead_units(self):
        source = Path("gym_mod/gym_mod/engine/state_export.py").read_text(encoding="utf-8")
        self.assertIn("if float(hp or 0.0) <= 0 or (alive_models is not None and int(alive_models) <= 0):", source)
        self.assertIn("continue", source)

    def test_viewer_filters_dead_units_before_render(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn("filtered_units = []", source)
        self.assertIn("hp_value = self._safe_int(unit.get(\"hp\"))", source)
        self.assertIn("alive_models_value = self._safe_int(unit.get(\"alive_models\"))", source)
        self.assertIn("self._units_state = filtered_units", source)

    def test_update_board_does_not_place_dead_units(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("if float(self.unit_health[i] or 0.0) > 0:", source)
        self.assertIn("if float(self.enemy_health[i] or 0.0) > 0:", source)


if __name__ == "__main__":
    unittest.main()
