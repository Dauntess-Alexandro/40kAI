import unittest
from pathlib import Path


class TestEnemyHeuristicMatchupContract(unittest.TestCase):
    def test_profile_and_matchup_helpers_exist(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("def _unit_profile(", source)
        self.assertIn("def _enemy_matchup_distance_plan(", source)
        self.assertIn("def _enemy_heur_movement_score(", source)

    def test_lookahead_and_team_penalty_used_in_movement(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("ENEMY_HEUR_LOOKAHEAD_TOP_K", source)
        self.assertIn("ENEMY_HEUR_LOOKAHEAD_W", source)
        self.assertIn("ENEMY_HEUR_TEAM_FOCUS_PENALTY_W", source)
        self.assertIn("focus_counter", source)


if __name__ == "__main__":
    unittest.main()
