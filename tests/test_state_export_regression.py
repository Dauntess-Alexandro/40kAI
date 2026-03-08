import unittest
from pathlib import Path


class TestStateExportRegression(unittest.TestCase):
    def test_state_export_contains_model_metadata_fields(self):
        source = Path("gym_mod/gym_mod/engine/state_export.py").read_text(encoding="utf-8")

        self.assertIn('"alive_models"', source)
        self.assertIn('"anchor_x"', source)
        self.assertIn('"anchor_y"', source)
        self.assertIn('_alive_models_from_pool("enemy", idx)', source)
        self.assertIn('_alive_models_from_pool("model", idx)', source)

    def test_state_export_contains_terrain_metadata_fields(self):
        source = Path("gym_mod/gym_mod/engine/state_export.py").read_text(encoding="utf-8")
        self.assertIn('"id": str(feature.get("id") or "")', source)
        self.assertIn('"name": str(feature.get("name") or feature.get("kind") or "Terrain")', source)
        self.assertIn('"keywords": keywords', source)
        self.assertIn('"covering_unit_ids": sorted(terrain_cover_map.get(str(feature.get("id") or ""), set()))', source)
        self.assertIn('"cover_source_terrain_id": cover_source_terrain_id', source)


if __name__ == "__main__":
    unittest.main()
