import numpy as np
import pytest
import torch

from core.models.action_contract import ordered_action_keys
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.alphazero_model import AlphaZeroPolicyValueNet
from core.models.alphazero_selfplay import SelfPlayConfig, play_episode_with_mcts
from tests.engine.phases._helpers import build_env


def _make_mcts(env, *, candidate_mode: str = "option") -> AlphaZeroFactorizedMCTS:
    len_model = len(env.unit_health)
    n_actions = [int(env.action_space.spaces[k].n) for k in ordered_action_keys(len_model)]
    state, _ = env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    obs = np.asarray(list(state.values()) if isinstance(state, dict) else state, dtype=np.float32)
    net = AlphaZeroPolicyValueNet(int(obs.size), n_actions)
    return AlphaZeroFactorizedMCTS(
        net,
        config=MCTSConfig(
            simulations=4,
            mode="tree",
            max_depth=1,
            dirichlet_eps=0.0,
            root_dirichlet_only=False,
            candidate_mode=candidate_mode,
            simulate_enemy_in_tree=False,
        ),
        device=torch.device("cpu"),
    )


@pytest.fixture
def windowed_env(monkeypatch):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    monkeypatch.setenv("MCTS_CANDIDATE_MODE", "option")
    monkeypatch.setenv("REPLAY_PHASE_META", "1")
    return build_env()


def test_mcts_snapshot_restore_after_windowed_step(windowed_env):
    env = windowed_env
    mcts = _make_mcts(env)
    len_model = len(env.unit_health)
    state, _ = env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    obs = np.asarray(list(state.values()) if isinstance(state, dict) else state, dtype=np.float32)
    legal_dict = env.get_legal_action_masks_by_head(side="model")
    legal = [legal_dict[k] for k in ordered_action_keys(len_model)]

    snap_before = env.snapshot_state()
    mcts.run(
        obs=obs,
        legal_masks_by_head=legal,
        temperature=0.0,
        env=env,
        len_model=len_model,
        reset_options={"m": env.model, "e": env.enemy, "trunc": True},
    )
    snap_after = env.snapshot_state()
    env.restore_state(snap_before)
    snap_restored = env.snapshot_state()

    for key in ("unit_health", "enemy_health", "modelCP", "enemyCP", "unit_coords", "enemy_coords"):
        assert snap_after[key] == snap_restored[key]


def test_mcts_smoke_windowed_option_mode(windowed_env):
    env = windowed_env
    mcts = _make_mcts(env)
    transitions, _info = play_episode_with_mcts(
        env=env,
        mcts=mcts,
        len_model=len(env.unit_health),
        config=SelfPlayConfig(temperature_opening_moves=1, temperature_opening_value=0.5, temperature_late_value=0.1),
    )
    assert len(transitions) >= 1
    meta = transitions[0].phase_meta
    if meta is not None:
        assert meta.window_id == "windowed_turn:model"
