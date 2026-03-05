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

    def test_barricades_are_vertical_1x3(self):
        source = Path("gym_mod/gym_mod/engine/mission.py").read_text(encoding="utf-8")
        self.assertIn("return [(anchor_row + i, anchor_col) for i in range(3)]", source)
        self.assertIn("right_cells = _make_barricade_cells(row, mirror_col)", source)

    def test_terrain_features_have_id_name_keywords(self):
        source = Path("gym_mod/gym_mod/engine/mission.py").read_text(encoding="utf-8")
        self.assertIn('"id": str(feature_id)', source)
        self.assertIn('"name": str(name or "Barricade")', source)
        self.assertIn('"keywords": list(keywords or ["OBSTACLE", "BARRICADE"])', source)
        self.assertIn('normalized["id"] = str(feature.get("id") or f"T{idx}")', source)

    def test_mission_registry_and_aliases_exist(self):
        source = Path("gym_mod/gym_mod/engine/mission.py").read_text(encoding="utf-8")
        self.assertIn("MISSION_REGISTRY", source)
        self.assertIn('"aliases"', source)
        self.assertIn("MISSION_TRAINING_GROUNDS", source)

    def test_layout_and_deploy_use_mission_terrain_generator(self):
        source = Path("gym_mod/gym_mod/engine/mission.py").read_text(encoding="utf-8")
        self.assertIn("def terrain_features_for_mission(value: str | None, b_len: int, b_hei: int)", source)
        self.assertIn("env.terrain_features = terrain_features_for_mission(mission, env.b_len, env.b_hei)", source)
        self.assertIn("terrain_features=terrain_features_for_mission(mission, b_len, b_hei)", source)

if __name__ == "__main__":
    unittest.main()
