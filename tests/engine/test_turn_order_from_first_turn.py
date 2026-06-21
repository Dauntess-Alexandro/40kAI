import unittest

from tests.engine.phases._helpers import build_env


class TestTurnOrderFromFirstTurn(unittest.TestCase):
    def _reset_with(self, first):
        env = build_env()
        env.first_turn_side = first
        env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
        return env

    def test_model_first(self):
        env = self._reset_with("model")
        self.assertEqual(env.turn_order, ["model", "enemy"])
        self.assertEqual(env.active_side, "model")

    def test_enemy_first(self):
        env = self._reset_with("enemy")
        self.assertEqual(env.turn_order, ["enemy", "model"])
        self.assertEqual(env.active_side, "enemy")

    def test_default_fallback_enemy(self):
        env = build_env()  # first_turn_side не задан
        env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
        self.assertEqual(env.turn_order, ["enemy", "model"])
        self.assertEqual(env.active_side, "enemy")
