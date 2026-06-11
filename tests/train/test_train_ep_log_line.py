"""Единый формат [TRAIN][EP] для вкладки «Эпизоды» в GUI."""
from __future__ import annotations

import unittest

from train import format_train_ep_log_line, log_train_episode_line


class TestFormatTrainEpLogLine(unittest.TestCase):
    def test_full_line_with_actor(self):
        line = format_train_ep_log_line(
            ep=25,
            total=3000,
            algo="dqn",
            actor_idx=6,
            result="win",
            end_reason="wipeout_enemy",
            vp_diff=0,
            ep_reward=4.8744,
            turns=12,
        )
        self.assertTrue(line.startswith("[TRAIN][EP] "))
        self.assertIn("ep=25/3000", line)
        self.assertIn("algo=dqn", line)
        self.assertIn("actor=6", line)
        self.assertIn("result=win", line)
        self.assertIn("end_reason=wipeout_enemy", line)
        self.assertIn("vp_diff=0", line)
        self.assertIn("ep_reward=4.8744", line)
        self.assertIn("turns=12", line)

    def test_ppo_sync_without_actor(self):
        line = format_train_ep_log_line(
            ep=20,
            total=300,
            algo="ppo",
            result="loss",
            end_reason="wipeout_model",
            vp_diff=-2,
            ep_reward=-1.25,
            turns=8,
        )
        self.assertIn("algo=ppo", line)
        self.assertNotIn("actor=", line)
        self.assertIn("result=loss", line)

    def test_row_dict_via_log_helper(self):
        import io
        from contextlib import redirect_stdout
        import train as train_mod

        old_enabled = train_mod.TRAIN_LOG_ENABLED
        old_file = train_mod.TRAIN_LOG_TO_FILE
        old_console = train_mod.TRAIN_LOG_TO_CONSOLE
        logged: list[str] = []
        try:
            train_mod.TRAIN_LOG_ENABLED = True
            train_mod.TRAIN_LOG_TO_FILE = False
            train_mod.TRAIN_LOG_TO_CONSOLE = True
            row = {
                "episode": 7,
                "result": "draw",
                "end_reason": "turn_limit",
                "vp_diff": 0,
                "ep_reward": 0.5,
                "turn": 21,
            }
            buf = io.StringIO()
            with redirect_stdout(buf):
                log_train_episode_line(row, total=300, algo="az", actor_idx=3)
            out = buf.getvalue().strip()
            self.assertIn("[TRAIN][EP]", out)
            self.assertIn("ep=7/300", out)
            self.assertIn("algo=az", out)
            self.assertIn("actor=3", out)
            self.assertIn("result=draw", out)
        finally:
            train_mod.TRAIN_LOG_ENABLED = old_enabled
            train_mod.TRAIN_LOG_TO_FILE = old_file
            train_mod.TRAIN_LOG_TO_CONSOLE = old_console


class TestTrainEpLineEmitted(unittest.TestCase):
    def test_all_algo_paths_use_helper(self):
        src = open("train.py", encoding="utf-8").read()
        self.assertGreaterEqual(src.count("log_train_episode_line("), 6)


if __name__ == "__main__":
    unittest.main()
