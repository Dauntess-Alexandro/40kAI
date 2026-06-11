# tests/engine/test_enemy_shoot_focus_fire_contract.py
import unittest
from pathlib import Path


class TestEnemyShootFocusFireContract(unittest.TestCase):
    def test_auto_shooting_uses_allocate_shots(self):
        source = Path("core/envs/warhamEnv.py").read_text(encoding="utf-8")
        # warhamEnv импортирует allocate_shots из heuristic_targeting (импорт может быть
        # многострочным — проверяем устойчиво: и модуль, и имя).
        self.assertIn("from ..engine.heuristic_targeting import", source)
        self.assertIn("allocate_shots", source)
        # EV урона считается через expected_damage (доступен через wildcard from ..engine.utils)
        self.assertIn("expected_damage(", source)
        # auto-путь стрельбы строит назначение через allocate_shots
        self.assertIn("allocate_shots(", source)
        self.assertIn("_enemy_focus_fire_assignment", source)


if __name__ == "__main__":
    unittest.main()
