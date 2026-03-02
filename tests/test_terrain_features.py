import unittest
from pathlib import Path


class TestTerrainFeatures(unittest.TestCase):
    def test_mission_defines_only_war_terrain_features(self):
        source = Path("gym_mod/gym_mod/engine/mission.py").read_text(encoding="utf-8")
        self.assertIn("def only_war_terrain_features(b_len: int, b_hei: int)", source)
        self.assertIn('"kind": "barricade"', source)
        self.assertIn('_BARRICADE_SPRITE_NAME = "barrels_red_warning_3x1.png"', source)
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

    def test_viewer_resolves_assets_from_viewer_directory(self):
        source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
        self.assertIn('return Path(__file__).resolve().parent / "assets" / rel_path', source)


if __name__ == "__main__":
    unittest.main()
