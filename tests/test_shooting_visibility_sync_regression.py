import unittest
from pathlib import Path


class TestShootingVisibilitySyncRegression(unittest.TestCase):
    def test_shoot_target_selection_uses_any_model_los_rule(self):
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("Критичное правило: если есть LOS хотя бы до одной модели цели, цель валидна для стрельбы.", source)
        self.assertIn('if not self._unit_has_los("model", unit_idx, "enemy", int(enemy_idx)):', source)
        self.assertIn('if not self._unit_has_los("enemy", unit_idx, "model", int(model_idx)):', source)

    def test_state_export_reports_can_see_by_los_even_out_of_range(self):
        source = Path("gym_mod/gym_mod/engine/state_export.py").read_text(encoding="utf-8")
        self.assertIn('if not _has_los_between_units_local(side, idx, enemy_side, enemy_idx):', source)
        self.assertIn('can_see_ids.append(int(enemy_id))', source)
        self.assertIn('if own_range > 0:', source)
        self.assertIn('if distance <= own_range:', source)


if __name__ == "__main__":
    unittest.main()
