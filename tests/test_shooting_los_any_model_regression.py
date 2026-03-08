import unittest
from pathlib import Path


class TestShootingLosAnyModelRegression(unittest.TestCase):
    def test_shoot_targets_use_unit_has_los(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn('targets = [int(idx) for idx in target_ids if self._unit_has_los("model", unit_idx, "enemy", int(idx))]', source)
        self.assertIn('targets = [int(idx) for idx in target_ids if self._unit_has_los("enemy", unit_idx, "model", int(idx))]', source)

    def test_unit_has_los_checks_any_model_pair(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("def _unit_has_los(self, attacker_side: str, attacker_idx: int, target_side: str, target_idx: int) -> bool:", source)
        self.assertIn("for attacker_cell in attacker_cells:", source)
        self.assertIn("for target_cell in target_cells:", source)
        self.assertIn('if bool(report.get("los", False)):\n                    return True', source)


if __name__ == "__main__":
    unittest.main()
