import os
import unittest


class TestEvalFirstTurnOrder(unittest.TestCase):
    def test_model_first_env_var_sets_turn_order(self):
        os.environ["FIRST_TURN"] = "model_first"
        try:
            from core.envs.warhamEnv import resolve_first_turn_side
            self.assertEqual(resolve_first_turn_side(), "model")
        finally:
            os.environ.pop("FIRST_TURN", None)

    def test_enemy_first_env_var_sets_turn_order(self):
        os.environ["FIRST_TURN"] = "enemy_first"
        try:
            from core.envs.warhamEnv import resolve_first_turn_side
            self.assertEqual(resolve_first_turn_side(), "enemy")
        finally:
            os.environ.pop("FIRST_TURN", None)

    def test_run_episode_respects_first_turn(self):
        # smoke: одна партия с FIRST_TURN=model_first не падает и завершается;
        # проверяем, что env.first_turn_side == "model" после resolve в run_episode.
        # (исполнителю: использовать существующую тест-фикстуру eval, если есть;
        #  иначе — пометить как integration и гонять вручную из run-40kai.)
        self.skipTest("integration smoke — гонять через GUI/eval вручную (см. Step 4)")
