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

    def test_optional_mission_fields_appended_when_present(self):
        line = format_train_ep_log_line(
            ep=3,
            total=400,
            algo="az",
            actor_idx=2,
            result="draw",
            end_reason="turn_limit",
            vp_diff=0,
            ep_reward=0.0,
            turns=21,
            model_vp=2,
            enemy_vp=1,
            model_ctrl_n=3,
            enemy_ctrl_n=1,
            hp_diff=15.0,
            outcome_value=-0.7,
        )
        self.assertIn("model_vp=2", line)
        self.assertIn("enemy_vp=1", line)
        self.assertIn("obj=3/1", line)
        self.assertIn("hp_diff=", line)
        self.assertIn("outcome_v=-0.700", line)
        # старые поля по-прежнему присутствуют и не сломаны
        self.assertIn("vp_diff=0", line)
        self.assertIn("turns=21", line)

    def test_optional_mission_fields_absent_when_none(self):
        line = format_train_ep_log_line(
            ep=3,
            total=400,
            algo="dqn",
            result="win",
            end_reason="wipeout_enemy",
            vp_diff=3,
            ep_reward=1.0,
            turns=12,
        )
        self.assertNotIn("model_vp=", line)
        self.assertNotIn("enemy_vp=", line)
        self.assertNotIn("obj=", line)
        self.assertNotIn("outcome_v=", line)

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


class TestAzEpisodeMissionFields(unittest.TestCase):
    def test_extracts_hp_obj_and_outcome(self):
        from train import _az_episode_mission_fields

        info = {
            "model health": [10, 5],
            "player health": [3],
            "model controlled objectives": [1, 2, 3],
            "player controlled objectives": [4],
            "az_outcome_value": -0.7,
        }
        f = _az_episode_mission_fields(info)
        self.assertEqual(f["model_hp_total"], 15.0)
        self.assertEqual(f["enemy_hp_total"], 3.0)
        self.assertEqual(f["model_ctrl_n"], 3)
        self.assertEqual(f["enemy_ctrl_n"], 1)
        self.assertEqual(f["outcome_value"], -0.7)

    def test_missing_outcome_value_omitted(self):
        from train import _az_episode_mission_fields

        f = _az_episode_mission_fields({"model health": [], "player health": []})
        self.assertNotIn("outcome_value", f)
        self.assertEqual(f["model_ctrl_n"], 0)
        self.assertEqual(f["enemy_ctrl_n"], 0)
        self.assertNotIn("cum_model_ctrl", f)

    def test_cumulative_objective_passthrough(self):
        from train import _az_episode_mission_fields

        f = _az_episode_mission_fields(
            {"az_cum_model_ctrl": 18.0, "az_cum_enemy_ctrl": 3.0, "model health": [], "player health": []}
        )
        self.assertEqual(f["cum_model_ctrl"], 18.0)
        self.assertEqual(f["cum_enemy_ctrl"], 3.0)

    def test_obj_cum_field_in_log_line(self):
        line = format_train_ep_log_line(
            ep=1, total=100, algo="az", result="draw", end_reason="turn_limit",
            vp_diff=0, ep_reward=0.0, turns=21, cum_model_ctrl=18.0, cum_enemy_ctrl=3.0,
        )
        self.assertIn("obj_cum=18/3", line)


class TestAzDetPayloadHpDiff(unittest.TestCase):
    def test_hp_diff_mean_computed_from_rows(self):
        from train import _az_det_payload_from_rows

        rows = [
            {"result": "win", "end_reason": "wipeout_enemy", "model_hp_total": 20.0, "enemy_hp_total": 0.0},
            {"result": "loss", "end_reason": "wipeout_model", "model_hp_total": 0.0, "enemy_hp_total": 10.0},
        ]
        p = _az_det_payload_from_rows(
            rows, episode_idx=2, train_loss=1.0, train_algo="alphazero_tree", mcts_mode="tree"
        )
        # (20-0 + 0-10)/2 = +5.0
        self.assertEqual(p["hp_diff_mean"], 5.0)

    def test_hp_diff_mean_zero_when_rows_lack_hp(self):
        from train import _az_det_payload_from_rows

        rows = [{"result": "draw", "end_reason": "turn_limit"}]
        p = _az_det_payload_from_rows(
            rows, episode_idx=1, train_loss=1.0, train_algo="alphazero_tree", mcts_mode="tree"
        )
        self.assertEqual(p["hp_diff_mean"], 0.0)


class TestTrainEpLineEmitted(unittest.TestCase):
    def test_all_algo_paths_use_helper(self):
        src = open("train.py", encoding="utf-8").read()
        self.assertGreaterEqual(src.count("log_train_episode_line("), 6)


if __name__ == "__main__":
    unittest.main()
