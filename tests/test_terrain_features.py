import unittest
from pathlib import Path


class TestTerrainFeatures(unittest.TestCase):
    def test_mission_defines_only_war_terrain_features(self):
        source = Path("gym_mod/gym_mod/engine/mission.py").read_text(encoding="utf-8")
        self.assertIn("def only_war_terrain_features(b_len: int, b_hei: int)", source)
        self.assertIn('"kind": "barricade"', source)
        self.assertIn('"tags": ["OBSTACLE", "BARRICADE"]', source)
        self.assertIn('"opacity": "obscuring"', source)

    def test_deploy_validation_rejects_terrain_cells(self):
        source = Path("gym_mod/gym_mod/engine/mission.py").read_text(encoding="utf-8")
        self.assertIn("terrain_cells: Iterable[Tuple[int, int]] | None = None", source)
        self.assertIn('return False, "terrain_no_deploy"', source)

    def test_env_uses_terrain_for_los_and_cell_checks(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("def get_terrain_obscuring_cells_set(self)", source)
        self.assertIn("def is_terrain_cell(self, x: int, y: int)", source)
        self.assertIn("obscuring_cells_set=obscuring_cells", source)


if __name__ == "__main__":
    unittest.main()
