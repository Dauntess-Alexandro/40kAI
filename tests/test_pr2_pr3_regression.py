import unittest
from pathlib import Path


class TestPr2Pr3Regression(unittest.TestCase):
    def test_model_pool_helpers_exist(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("def _model_wounds_pool_from_hp", source)
        self.assertIn("def _apply_health_update", source)
        self.assertIn("def _sync_model_positions_to_anchors", source)
        self.assertIn("self._init_model_state_from_health()", source)

    def test_damage_paths_use_apply_health_update(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn('reason="shooting"', source)
        self.assertIn('reason="fight"', source)
        self.assertIn('reason="Overwatch"', source)
        self.assertNotIn('self.enemy_health[idOfE] = modHealth', source)
        self.assertNotIn('self.unit_health[idOfM] = modHealth', source)


if __name__ == "__main__":
    unittest.main()
