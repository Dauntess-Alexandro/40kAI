import numpy as np
import torch

from core.models.alphazero_model import AlphaZeroPolicyValueNet
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.alphazero_replay import AlphaZeroReplayBuffer, AZTransition
from core.models.alphazero_trainer import AlphaZeroTrainConfig, train_alphazero_step


def test_alphazero_model_forward_shapes():
    n_obs = 32
    n_actions = [5, 2, 8, 8, 5, 4, 24, 24]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    x = torch.randn(3, n_obs)
    logits, value = net(x)
    assert len(logits) == len(n_actions)
    assert value.shape == (3,)
    for idx, head in enumerate(logits):
        assert head.shape == (3, n_actions[idx])


def test_alphazero_trainer_step_runs():
    n_obs = 16
    n_actions = [3, 2, 5]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    replay = AlphaZeroReplayBuffer(capacity=64)
    for _ in range(20):
        replay.push(
            AZTransition(
                state=np.random.randn(n_obs).astype(np.float32),
                policy_targets=[np.ones(a, dtype=np.float32) / float(a) for a in n_actions],
                value_target=float(np.random.uniform(-1.0, 1.0)),
            )
        )
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    out = train_alphazero_step(
        net=net,
        optimizer=opt,
        replay=replay,
        config=AlphaZeroTrainConfig(batch_size=8),
        device=torch.device("cpu"),
    )
    assert out is not None
    assert out["loss"] >= 0.0


def test_alphazero_mcts_policy_targets_sum_to_one():
    n_obs = 10
    n_actions = [4, 3]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    mcts = AlphaZeroFactorizedMCTS(net, config=MCTSConfig(simulations=8), device=torch.device("cpu"))
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [np.array([1, 1, 0, 1], dtype=bool), np.array([1, 0, 1], dtype=bool)]
    pi, act, value = mcts.run(obs=obs, legal_masks_by_head=legal, temperature=1.0)
    assert len(pi) == 2
    assert len(act) == 2
    for p in pi:
        assert abs(float(np.sum(p)) - 1.0) < 1e-5
    assert -1.0 <= float(value) <= 1.0
