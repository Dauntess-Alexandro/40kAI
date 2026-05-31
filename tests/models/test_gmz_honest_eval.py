from __future__ import annotations

from contextlib import contextmanager
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from core.models.gumbel_muzero_selfplay import play_episode_with_gumbel_muzero


@contextmanager
def _make_mock_env(*, steps_before_done: int = 2):
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

    def enemy_turn(trunc=True, policy_fn=None):
        pass

    def get_info():
        return {"end reason": "turn_limit_vp", "model VP": 10, "player VP": 5, "turn": step_idx["n"], "reward": 1.0}

    env.reset.side_effect = reset
    env.step.side_effect = step
    env_u.enemyTurn.side_effect = enemy_turn
    env_u.get_info.side_effect = get_info
    env_u.get_legal_action_masks_by_head.return_value = {
        "move": np.array([1, 1], dtype=bool),
        "attack": np.array([1, 0, 1], dtype=bool),
        "shoot": np.array([1], dtype=bool),
        "charge": np.array([1], dtype=bool),
        "use_cp": np.array([1], dtype=bool),
        "cp_on": np.array([1], dtype=bool),
        "move_num_0": np.array([1, 1], dtype=bool),
    }

    with patch("core.models.gumbel_muzero_selfplay.unwrap_env", return_value=env_u):
        yield env


def _action_list_for_len_model(len_model: int) -> list[int]:
    from core.models.action_contract import ordered_action_keys

    return [0] * len(ordered_action_keys(len_model))


def test_play_episode_passes_deterministic_true_to_search():
    search = MagicMock()
    pi = [np.array([0.2, 0.8], dtype=np.float32)]
    beh = [np.array([0.0, 0.0], dtype=np.float32)]
    actions = _action_list_for_len_model(1)
    search.run.side_effect = [
        (pi, beh, actions, 0.5),
        (pi, beh, actions, 0.5),
    ]

    with _make_mock_env(steps_before_done=2) as env:
        play_episode_with_gumbel_muzero(
            env=env,
            search=search,
            len_model=1,
            deterministic=True,
        )

    assert search.run.call_count == 2
    for call in search.run.call_args_list:
        assert call.kwargs.get("deterministic") is True


def test_play_episode_deterministic_false_by_default():
    search = MagicMock()
    pi = [np.array([0.5, 0.5], dtype=np.float32)]
    beh = [np.array([0.0, 0.0], dtype=np.float32)]
    search.run.return_value = (pi, beh, _action_list_for_len_model(1), 0.0)

    with _make_mock_env(steps_before_done=1) as env:
        play_episode_with_gumbel_muzero(env=env, search=search, len_model=1)

    search.run.assert_called_once()
    assert search.run.call_args.kwargs.get("deterministic") is False


def test_gmz_episode_result_row_win_on_wipeout_enemy():
    from train import _gmz_episode_result_row

    row = _gmz_episode_result_row(
        info={"end reason": "wipeout_enemy", "model VP": 5, "player VP": 1, "res": 1},
        ep_reward=1.0,
        ep_len=7,
    )
    assert row["result"] == "win"
    assert row["vp_diff"] == 4
    assert row["ep_len"] == 7


def test_gmz_det_payload_from_rows_schema():
    from train import _gmz_det_payload_from_rows

    rows = [
        {"result": "win", "end_reason": "wipeout_enemy", "vp_diff": 3, "model_vp": 5, "player_vp": 2, "ep_len": 10, "ep_reward": 1.0},
        {"result": "loss", "end_reason": "wipeout_model", "vp_diff": -2, "model_vp": 1, "player_vp": 3, "ep_len": 8, "ep_reward": -1.0},
    ]
    payload = _gmz_det_payload_from_rows(rows, episode_idx=300, train_loss=5.5, eval_tag="actor_learner_search_eval")
    assert payload["eval_episodes"] == 2
    assert payload["win_rate"] == 0.5
    assert payload["eval_tag"] == "actor_learner_search_eval"
    assert payload["episode"] == 300
    assert payload["algo"] == "gumbel_muzero"
    assert 0.0 <= payload["win_rate"] <= 1.0


@patch("train.GumbelMuZeroSearch")
@patch("train.post_deploy_setup")
@patch("train.deploy_for_mission")
@patch("train.roll_off_attacker_defender", return_value=("model", "enemy"))
@patch("train.play_episode_with_gumbel_muzero")
@patch("train.gym.make")
@patch("train._build_units_from_config")
def test_run_gmz_honest_eval_returns_rows(
    mock_build_units, mock_gym_make, mock_play, _mock_roll, _mock_deploy, _mock_post, _mock_search_cls
):
    from train import _run_gmz_honest_eval

    mock_build_units.return_value = ([object()], [object(), object()])
    mock_env = MagicMock()
    mock_gym_make.return_value = mock_env
    mock_play.return_value = (
        [],
        {"end reason": "wipeout_enemy", "model VP": 10, "player VP": 2, "turn": 12, "reward": 1.0},
    )

    net = MagicMock()
    net.training = True
    rows = _run_gmz_honest_eval(
        gmz_net=net,
        device=MagicMock(),
        roster_config={"mission": "test"},
        b_len=10,
        b_hei=10,
        n_eval=3,
        sims=4,
        root_top_k=2,
        eval_temperature=0.1,
        gumbel_scale=1.0,
        prior_weight=0.25,
        discount=0.99,
        batch_recurrent=True,
        tree_reuse=True,
        self_play_enabled=False,
        opponent_spec=None,
    )
    assert len(rows) == 3
    assert all(r["result"] == "win" for r in rows)
    assert mock_play.call_count == 3
    assert mock_play.call_args.kwargs.get("deterministic") is True
    net.eval.assert_called()
    net.train.assert_called()


@patch("train._run_gmz_honest_eval")
def test_gmz_build_actor_det_payload(mock_honest):
    from train import _gmz_build_actor_det_payload

    mock_honest.return_value = [
        {"result": "win", "end_reason": "wipeout_enemy", "vp_diff": 1, "model_vp": 2, "player_vp": 1, "ep_len": 5, "ep_reward": 1.0},
    ]
    net = MagicMock()
    payload = _gmz_build_actor_det_payload(
        gmz_net=net,
        device=MagicMock(),
        roster_config={},
        b_len=10,
        b_hei=10,
        episodes_finished=300,
        last_loss=4.0,
        self_play_enabled=False,
        opponent_spec=None,
    )
    mock_honest.assert_called_once()
    assert payload["eval_tag"] == "actor_learner_search_eval"
    assert payload["win_rate"] == 1.0
