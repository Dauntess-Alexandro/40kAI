import importlib.util
from pathlib import Path
import sys
import unittest

MODULE_PATH = Path("gym_mod/gym_mod/engine/visibility.py")
spec = importlib.util.spec_from_file_location("visibility_module", MODULE_PATH)
visibility = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
sys.modules["visibility_module"] = visibility
spec.loader.exec_module(visibility)

TerrainFeature = visibility.TerrainFeature
TerrainType = visibility.TerrainType
evaluate_visibility = visibility.evaluate_visibility
normalize_terrain_features = visibility.normalize_terrain_features


class TestVisibilityLos(unittest.TestCase):
    def test_opaque_blocks_los(self):
        terrain = [TerrainFeature(TerrainType.OPAQUE, 2, -1, 3, 1, "wall")]
        res = evaluate_visibility((0, 0), (5, 0), terrain)
        self.assertFalse(res.can_see)
        self.assertIn("wall", res.blockers)

    def test_obscuring_adds_cover_without_blocking(self):
        terrain = [TerrainFeature(TerrainType.OBSCURING, 2, -1, 3, 1, "ruins")]
        res = evaluate_visibility((0, 0), (5, 0), terrain)
        self.assertTrue(res.can_see)
        self.assertFalse(res.fully_visible)
        self.assertTrue(res.has_cover)

    def test_soft_adds_penalty_without_blocking(self):
        terrain = [TerrainFeature(TerrainType.SOFT, 2, -1, 3, 1, "fog")]
        res = evaluate_visibility((0, 0), (5, 0), terrain)
        self.assertTrue(res.can_see)
        self.assertEqual(res.soft_penalty, 1)

    def test_normalize_terrain_features_from_dicts(self):
        src = [{"type": "opaque", "x1": 4, "y1": 1, "x2": 1, "y2": -1, "name": "wall"}]
        items = normalize_terrain_features(src)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].x_min, 1)
        self.assertEqual(items[0].x_max, 4)


if __name__ == "__main__":
    unittest.main()
