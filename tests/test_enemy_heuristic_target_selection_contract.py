import unittest
from pathlib import Path


class TestEnemyHeuristicTargetSelectionContract(unittest.TestCase):
    def test_shoot_and_charge_scoring_helpers_exist(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("def _enemy_heur_pick_shoot_target(", source)
        self.assertIn("def _enemy_heur_pick_charge_target(", source)

    def test_enemy_shoot_and_charge_use_scoring_fallback(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("heur_target, scored_targets = self._enemy_heur_pick_shoot_target(", source)
        self.assertIn("idOfM, scored_targets = self._enemy_heur_pick_shoot_target(", source)
        self.assertIn("heur_charge_target, charge_scored = self._enemy_heur_pick_charge_target(", source)
        self.assertIn("idOfM, charge_scored = self._enemy_heur_pick_charge_target(", source)


if __name__ == "__main__":
    unittest.main()
