import numpy as np
import torch

from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.gumbel_muzero_replay import GMZTransition, GumbelMuZeroReplayBuffer
from core.models.gumbel_muzero_trainer import GumbelMuZeroTrainConfig, train_gumbel_muzero_step


def _make_transition(n_obs: int, n_actions: list[int], value: float, policy_version: int) -> GMZTransition:
    action = [np.random.randint(0, max(1, n_actions[h])) for h in range(len(n_actions))]
    return GMZTransition(
        state=np.random.randn(n_obs).astype(np.float32),
        action=np.asarray(action, dtype=np.int64),
        reward=float(np.random.uniform(-1.0, 1.0)),
        done=False,
        policy_targets=[np.ones(a, dtype=np.float32) / float(a) for a in n_actions],
        behavior_logits=[np.zeros(a, dtype=np.float32) for a in n_actions],
        value_target=float(value),
        policy_version=int(policy_version),
    )


def test_gumbel_muzero_train_step_runs():
    n_obs = 18
    n_actions = [5, 3, 7]
    net = GumbelMuZeroNet(obs_dim=n_obs, action_sizes=n_actions, latent_dim=64, hidden_dim=64, action_embed_dim=16)
    optimizer = torch.optim.Adam(net.parameters(), lr=1e-3)
    replay = GumbelMuZeroReplayBuffer(capacity=128)
    for _ in range(48):
        replay.push(_make_transition(n_obs, n_actions, value=np.random.uniform(-1.0, 1.0), policy_version=9))

    cfg = GumbelMuZeroTrainConfig(
        batch_size=16,
        unroll_steps=4,
        max_policy_staleness_updates=5,
    )
    out = train_gumbel_muzero_step(
        net=net,
        optimizer=optimizer,
        replay=replay,
        config=cfg,
        device=torch.device("cpu"),
        current_policy_version=10,
    )
    assert out is not None
    assert float(out["loss"]) >= 0.0
