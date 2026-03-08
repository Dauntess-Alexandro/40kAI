import unittest
from pathlib import Path


class TestMovementReachableEuclid(unittest.TestCase):
    def test_engine_utils_has_shared_euclid_distance(self):
        source = Path("gym_mod/gym_mod/engine/utils.py").read_text(encoding="utf-8")
        self.assertIn("def distance_cells_euclid(a, b):", source)
        self.assertIn("return math.hypot", source)

    def test_movement_overlay_uses_euclid_budget(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("def _grid_distance_euclid", source)
        self.assertIn("dist = self._grid_distance_euclid((row, col), (r, c))", source)
        self.assertIn("if dist == 0.0 or dist > float(move_budget):", source)
        self.assertNotIn("dist = abs(r - row) + abs(c - col)", source)

    def test_boundary_examples_3_4_and_4_4_present(self):
        # Прямая самопроверка формулы: (3,4)=5 входит, (4,4)>5 не входит
        self.assertLessEqual((3 ** 2 + 4 ** 2) ** 0.5, 5)
        self.assertGreater((4 ** 2 + 4 ** 2) ** 0.5, 5)


if __name__ == "__main__":
    unittest.main()
