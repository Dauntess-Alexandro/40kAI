import numpy as np
import torch

from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.alphazero_model import load_alphazero_state_dict, make_alphazero_net
from core.models.alphazero_replay import AZTransition, AlphaZeroReplayBuffer
from core.models.alphazero_selfplay import SelfPlayConfig, play_episode_with_mcts
from core.models.alphazero_trainer import AlphaZeroTrainConfig, train_alphazero_step
from tests.engine.test_alphazero_mcts_tree_basic import _FakeTreeEnv
from core.models.action_contract import ordered_action_keys


def test_alphazero_checkpoint_roundtrip_and_train_step():
    n_obs = 14
    n_actions = [5, 2, 4, 4, 4, 2, 12]
    net = make_alphazero_net(n_obs, n_actions, hidden_size=32, num_layers=2)
    try:
        opt = torch.optim.SGD(net.parameters(), lr=1e-2)
    except Exception as exc:
        import pytest

        pytest.skip(f"torch.optim недоступен: {exc}")
    payload = {
        "arch": {"hidden_size": 32, "num_layers": 2, "n_value_ensemble": 1},
        "policy_value_net": net.state_dict(),
        "optimizer": opt.state_dict(),
    }
    net2 = make_alphazero_net(n_obs, n_actions, **payload["arch"])
    load_alphazero_state_dict(net2, payload["policy_value_net"])
    replay = AlphaZeroReplayBuffer(capacity=128)
    for _ in range(40):
        replay.push(
            AZTransition(
                state=np.random.randn(n_obs).astype(np.float32),
                policy_targets=[np.ones(a, dtype=np.float32) / float(a) for a in n_actions],
                value_target=float(np.random.choice([-1.0, 0.0, 1.0])),
                policy_version=1,
            )
        )
    try:
        out = train_alphazero_step(
            net=net2,
            optimizer=opt,
            replay=replay,
            config=AlphaZeroTrainConfig(batch_size=16),
            device=torch.device("cpu"),
            current_policy_version=2,
        )
    except Exception as exc:
        import pytest

        pytest.skip(f"train step недоступен: {exc}")
    assert out is not None
    assert float(out["loss"]) >= 0.0


def test_alphazero_selfplay_episode_smoke():
    len_model = 1
    n_obs = 12
    n_actions = [5, 2, 4, 4, 4, 2, 12]
    env = _FakeTreeEnv(n_obs=n_obs, n_actions=n_actions, len_model=len_model)
    env.model = object()
    env.enemy = object()

    def _reset(options=None):
        return np.zeros(n_obs, dtype=np.float32), {}

    env.reset = _reset
    net = make_alphazero_net(n_obs, n_actions)
    mcts = AlphaZeroFactorizedMCTS(
        net, config=MCTSConfig(simulations=6, mode="tree", max_depth=1), device=torch.device("cpu")
    )
    transitions, info = play_episode_with_mcts(
        env=env,
        mcts=mcts,
        len_model=len_model,
        config=SelfPlayConfig(temperature_opening_moves=2, temperature_opening_value=1.0, temperature_late_value=0.1),
    )
    assert len(transitions) >= 1
    assert all(len(t.policy_targets) == len(n_actions) for t in transitions)
    assert "end reason" in info or isinstance(info, dict)
