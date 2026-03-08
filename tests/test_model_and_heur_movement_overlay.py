import unittest
from pathlib import Path


class TestModelAndHeurMovementOverlay(unittest.TestCase):
    def test_model_movement_uses_overlay_destination_picker(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("def _pick_destination_from_overlay(", source)
        self.assertIn('dest, move_mode, movement = self._pick_destination_from_overlay(', source)
        self.assertIn('self.unit_coords[i] = [int(dest[1]), int(dest[0])]', source)

    def test_enemy_heuristic_uses_overlay_candidates(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn('overlay = self.get_unit_movement_overlay("enemy", i)', source)
        self.assertIn('candidates = move_cells + adv_cells', source)
        self.assertIn('best_x, best_y, best_mode = min(candidates, key=_heur_score)', source)


if __name__ == "__main__":
    unittest.main()
