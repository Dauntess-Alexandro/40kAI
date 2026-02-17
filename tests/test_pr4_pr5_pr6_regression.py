import unittest
from pathlib import Path


class TestPr4Pr5Pr6Regression(unittest.TestCase):
    def test_coherency_hooks_exist(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("def _coherency_required_neighbors", source)
        self.assertIn("def _validate_unit_coherency", source)
        self.assertIn("def _auto_fix_all_coherency", source)
        self.assertIn('self._auto_fix_all_coherency(reason="конец боевого раунда")', source)

    def test_state_export_has_model_positions(self):
        source = Path("gym_mod/gym_mod/engine/state_export.py").read_text(encoding="utf-8")
        self.assertIn('"model_positions"', source)
        self.assertIn('env.unit_model_positions', source)
        self.assertIn('env.enemy_model_positions', source)

    def test_distance_between_units_used_in_ranged_paths(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn('self._distance_between_units("model", i, "enemy", j)', source)
        self.assertIn('self._distance_between_units("enemy", i, "model", j)', source)
        self.assertIn('distance_to_target=self._distance_between_units("model", i, "enemy", idOfE)', source)
        self.assertIn('distance_to_target=self._distance_between_units("enemy", i, "model", idOfM)', source)


if __name__ == "__main__":
    unittest.main()
