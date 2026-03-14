import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "gym_mod"))

from gym_mod.envs.warhamEnv import Warhammer40kEnv


class _DummyUnit:
    def __init__(self, x: int, y: int):
        self._coords = [x, y]

    def showWeapon(self):
        return {"Name": "Gauss flayer", "Range": 24, "BS": 4, "S": 4, "AP": 0, "Damage": 1, "Attacks": 1}

    def showMelee(self):
        return {"Name": "Fists", "WS": 4, "S": 4, "AP": 0, "Damage": 1, "Attacks": 1}

    def showUnitData(self):
        return {"W": 1, "#OfModels": 10, "OC": 1, "Sv": 4, "T": 4}

    def showCoords(self):
        return list(self._coords)


class ShootTargetsContractRegressionTest(unittest.TestCase):
    def _build_env(self):
        enemy = [_DummyUnit(10, 10)]
        model = [_DummyUnit(20, 20)]
        return Warhammer40kEnv(enemy=enemy, model=model, b_len=60, b_hei=44)

    def test_include_rejected_returns_pair_for_invalid_enemy_unit(self):
        env = self._build_env()
        env.enemy_health[0] = 0

        result = env.get_shoot_targets_for_unit("enemy", 0, include_rejected=True)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], [])
        self.assertEqual(result[1], [])

    def test_manual_enemy_shooting_skips_dead_unit_without_crash(self):
        env = self._build_env()
        env.enemy_health[0] = 0

        out = env.shooting_phase("enemy", advanced_flags=[False], manual=True)

        self.assertIsNone(out)


if __name__ == "__main__":
    unittest.main()
