from __future__ import annotations

from contextlib import contextmanager
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from core.models.alphazero_selfplay import play_episode_with_mcts


@contextmanager
def _make_mock_env(*, steps_before_done: int = 1):
    env = MagicMock()
    env_u = MagicMock()
    env_u.model = [object()]
    env_u.enemy = [object()]
    env_u.game_over = False
    state = {"x": 0.0}
    step_idx = {"n": 0}

    def reset(options=None):
        step_idx["n"] = 0
        env_u.game_over = False
        return state, {}

    def step(action_dict):
        step_idx["n"] += 1
        done = step_idx["n"] >= steps_before_done
        env_u.game_over = done
        return state, 0.0, done, False, {"turn": step_idx["n"]}

    env.reset.side_effect = reset
    env.step.side_effect = step
    env_u.enemyTurn.return_value = None
    env_u.get_info.return_value = {
        "end reason": "wipeout_enemy",
        "model VP": 10,
        "player VP": 2,
        "turn": step_idx["n"],
        "reward": 1.0,
    }
    env_u.get_legal_action_masks_by_head.return_value = {
        "move": np.array([1, 1], dtype=bool),
        "attack": np.array([1, 0, 1], dtype=bool),
        "shoot": np.array([1], dtype=bool),
        "charge": np.array([1], dtype=bool),
        "use_cp": np.array([1], dtype=bool),
        "cp_on": np.array([1], dtype=bool),
        "move_num_0": np.array([1, 1], dtype=bool),
    }

    with patch("core.models.alphazero_selfplay.unwrap_env", return_value=env_u):
        yield env


def _pi_and_actions():
    pi = [np.array([0.1, 0.9], dtype=np.float32) for _ in range(7)]
    actions = [0, 0, 0, 0, 0, 0, 0]
    return pi, actions


def test_play_episode_fixed_temperature_passed_to_mcts():
    mcts = MagicMock()
    pi, actions = _pi_and_actions()
    mcts.run.return_value = (pi, actions, 0.5)

    with _make_mock_env(steps_before_done=1) as env:
        play_episode_with_mcts(
            env=env,
            mcts=mcts,
            len_model=1,
            fixed_temperature=0.06,
        )

    assert mcts.run.call_args.kwargs.get("temperature") == 0.06


def test_play_episode_policy_argmax_overrides_actions():
    mcts = MagicMock()
    pi, actions = _pi_and_actions()
    mcts.run.return_value = (pi, [0] * 7, 0.5)

    with _make_mock_env(steps_before_done=1) as env:
        play_episode_with_mcts(
            env=env,
            mcts=mcts,
            len_model=1,
            policy_argmax=True,
            heartbeat_moves=0,
        )

    action_passed = env.step.call_args[0][0]
    assert action_passed["attack"] == 1
    assert action_passed["move"] == 1


def test_az_det_payload_from_rows_schema():
    from train import _az_det_payload_from_rows

    rows = [
        {
            "result": "win",
            "end_reason": "wipeout_enemy",
            "vp_diff": 2,
            "model_vp": 5,
            "player_vp": 3,
            "ep_len": 9,
            "ep_reward": 1.0,
        }
    ]
    payload = _az_det_payload_from_rows(
        rows,
        episode_idx=300,
        train_loss=4.0,
        train_algo="alphazero_tree",
        mcts_mode="tree",
    )
    assert payload["win_rate"] == 1.0
    assert payload["mcts_mode"] == "tree"
    assert payload["algo"] == "alphazero_tree"
    assert payload["eval_tag"] == "actor_learner_search_eval"


@patch("train.AlphaZeroFactorizedMCTS")
@patch("train.post_deploy_setup")
@patch("train.deploy_for_mission")
@patch("train.roll_off_attacker_defender", return_value=("model", "enemy"))
@patch("train.play_episode_with_mcts")
@patch("train.gym.make")
@patch("train._build_units_from_config")
def test_run_az_honest_eval_tree_and_proxy(
    mock_build_units, mock_gym_make, mock_play, _mock_roll, _mock_deploy, _mock_post, _mock_mcts_cls
):
    from train import _run_az_honest_eval

    mock_build_units.return_value = ([object()], [object()])
    mock_gym_make.return_value = MagicMock()
    mock_play.return_value = (
        [],
        {"end reason": "wipeout_enemy", "model VP": 8, "player VP": 1, "turn": 11, "reward": 1.0},
    )
    net = MagicMock()
    net.training = False

    for mode in ("tree", "proxy"):
        rows = _run_az_honest_eval(
            az_net=net,
            device=MagicMock(),
            roster_config={"mission": "test"},
            b_len=10,
            b_hei=10,
            n_eval=2,
            mcts_mode=mode,
            self_play_enabled=False,
            opponent_spec=None,
        )
        assert len(rows) == 2
        assert rows[0]["result"] == "win"

    assert mock_play.call_count == 4
    for call in mock_play.call_args_list:
        assert call.kwargs.get("fixed_temperature") is not None
        assert call.kwargs.get("policy_argmax") is True


@patch("train._run_az_honest_eval")
def test_az_build_actor_det_payload(mock_honest):
    from train import _az_build_actor_det_payload

    mock_honest.return_value = [
        {
            "result": "win",
            "end_reason": "wipeout_enemy",
            "vp_diff": 1,
            "model_vp": 2,
            "player_vp": 1,
            "ep_len": 5,
            "ep_reward": 1.0,
        }
    ]
    payload = _az_build_actor_det_payload(
        az_net=MagicMock(),
        device=MagicMock(),
        roster_config={},
        b_len=10,
        b_hei=10,
        episodes_finished=600,
        last_loss=3.5,
        train_algo="alphazero_proxy",
        mcts_mode="proxy",
        self_play_enabled=False,
        opponent_spec=None,
    )
    mock_honest.assert_called_once()
    assert payload["mcts_mode"] == "proxy"
    assert payload["win_rate"] == 1.0
