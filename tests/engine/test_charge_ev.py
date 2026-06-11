# tests/engine/test_charge_ev.py
import unittest

from core.engine.heuristic_targeting import melee_trade_value, prob_2d6_at_least


class TestProb2d6AtLeast(unittest.TestCase):
    def test_known_cdf_values(self):
        self.assertAlmostEqual(prob_2d6_at_least(2), 1.0, places=6)
        self.assertAlmostEqual(prob_2d6_at_least(7), 21 / 36, places=6)
        self.assertAlmostEqual(prob_2d6_at_least(9), 10 / 36, places=6)
        self.assertAlmostEqual(prob_2d6_at_least(12), 1 / 36, places=6)

    def test_below_two_is_certain(self):
        self.assertEqual(prob_2d6_at_least(1), 1.0)
        self.assertEqual(prob_2d6_at_least(0), 1.0)

    def test_above_twelve_impossible(self):
        self.assertEqual(prob_2d6_at_least(13), 0.0)

    def test_monotonic_decreasing(self):
        vals = [prob_2d6_at_least(n) for n in range(2, 13)]
        self.assertEqual(vals, sorted(vals, reverse=True))


class TestMeleeTradeValue(unittest.TestCase):
    def test_favorable_trade_positive(self):
        # я сношу 6 из 6 HP цели, мне в ответ 1 из 10 -> сильно положительно
        self.assertGreater(melee_trade_value(6.0, 6.0, 1.0, 10.0), 0.0)

    def test_unfavorable_trade_negative(self):
        # я наношу 1 из 10, мне в ответ 8 из 6 -> отрицательно
        self.assertLess(melee_trade_value(1.0, 10.0, 8.0, 6.0), 0.0)

    def test_symmetry_zero_when_equal(self):
        self.assertAlmostEqual(melee_trade_value(3.0, 6.0, 3.0, 6.0), 0.0, places=6)


class TestEnemyMeleeTradeValue(unittest.TestCase):
    def _stub(self, e_melee, t_melee):
        import types

        s = types.SimpleNamespace()
        s.enemy_melee = [e_melee]
        s.unit_melee = [t_melee]
        s.enemy_health = [10.0]
        s.unit_health = [6.0]
        s.enemy_data = [{"#OfModels": 1, "W": 10, "T": 4, "Sv": 3}]
        s.unit_data = [{"#OfModels": 1, "W": 6, "T": 4, "Sv": 4}]
        return s

    def test_strong_enemy_melee_gives_positive_trade(self):
        from core.envs.warhamEnv import Warhammer40kEnv

        s = self._stub(
            e_melee={"WS": 3, "S": 8, "AP": -2, "Damage": 3, "Attacks": 4},  # сильная рукопашка
            t_melee={"WS": 4, "S": 3, "AP": 0, "Damage": 1, "Attacks": 1},   # слабая
        )
        self.assertGreater(Warhammer40kEnv._enemy_melee_trade_value(s, 0, 0), 0.0)

    def test_no_enemy_melee_weapon_gives_nonpositive_trade(self):
        from core.envs.warhamEnv import Warhammer40kEnv

        # у врага нет рукопашного оружия ({}), у цели есть -> размен невыгоден
        s = self._stub(
            e_melee={},
            t_melee={"WS": 3, "S": 6, "AP": -1, "Damage": 2, "Attacks": 3},
        )
        self.assertLess(Warhammer40kEnv._enemy_melee_trade_value(s, 0, 0), 0.0)


class TestChargeEvWiringContract(unittest.TestCase):
    def test_charge_picker_uses_real_prob_and_trade(self):
        from pathlib import Path

        source = Path("core/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("prob_2d6_at_least(", source)
        self.assertIn("_enemy_melee_trade_value(", source)
        self.assertIn("ENEMY_HEUR_CHARGE_EV_V2_ENABLED", source)
        self.assertIn("ENEMY_HEUR_CHARGE_SKIP_BAD_ENABLED", source)

    def test_flags_present_in_reward_config(self):
        import reward_config

        self.assertTrue(hasattr(reward_config, "ENEMY_HEUR_CHARGE_EV_V2_ENABLED"))
        self.assertTrue(hasattr(reward_config, "ENEMY_HEUR_CHARGE_SKIP_BAD_ENABLED"))
        # skip по умолчанию выключен (поведенческое изменение, требует A/B)
        self.assertEqual(int(reward_config.ENEMY_HEUR_CHARGE_SKIP_BAD_ENABLED), 0)


if __name__ == "__main__":
    unittest.main()
