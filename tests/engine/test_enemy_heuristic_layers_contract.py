import unittest
from pathlib import Path


class TestEnemyHeuristicLayersContract(unittest.TestCase):
    def test_team_role_threat_look2_helpers_exist(self):
        source = Path("core/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("def _enemy_team_tactic(", source)
        self.assertIn("def _enemy_effective_role(", source)
        self.assertIn("def _enemy_cell_threat_score(", source)
        self.assertIn("ENEMY_HEUR_LOOK2_ENABLED", source)
        self.assertIn("[ENEMY][HEUR][TEAM]", source)
        self.assertIn("[ENEMY][HEUR][ROLE]", source)
        self.assertIn("[ENEMY][HEUR][LOOK2]", source)

    def test_ev_targeting_fields_present(self):
        source = Path("core/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("ENEMY_HEUR_SHOOT_EV_KILL_VALUE_W", source)
        self.assertIn("ENEMY_HEUR_CHARGE_EV_SUCCESS_W", source)
        self.assertIn("\"ev\": float(ev_value)", source)
        self.assertIn("\"ev\": float(ev_charge)", source)


if __name__ == "__main__":
    unittest.main()

