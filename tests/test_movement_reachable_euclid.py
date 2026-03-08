import unittest
from pathlib import Path


class TestMovementReachableChebyshev(unittest.TestCase):
    def test_engine_utils_keeps_shared_euclid_distance_for_non_movement(self):
        source = Path("gym_mod/gym_mod/engine/utils.py").read_text(encoding="utf-8")
        self.assertIn("def distance_cells_euclid(a, b):", source)
        self.assertIn("return math.hypot", source)

    def test_movement_overlay_uses_chebyshev_budget(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("def _grid_distance_chebyshev", source)
        self.assertIn("dist = self._grid_distance_chebyshev((row, col), (r, c))", source)
        self.assertIn("if dist == 0 or dist > int(move_budget):", source)
        self.assertNotIn("dist = self._grid_distance_euclid((row, col), (r, c))", source)

    def test_chebyshev_boundary_examples(self):
        self.assertLessEqual(max(abs(5), abs(0)), 5)
        self.assertLessEqual(max(abs(5), abs(5)), 5)
        self.assertGreater(max(abs(6), abs(5)), 5)

    def test_shooting_distance_path_not_switched_to_chebyshev(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("d = distance(pa[:2], pb[:2])", source)


if __name__ == "__main__":
    unittest.main()
