import numpy as np
import torch

from core.models.alphazero_model import AlphaZeroPolicyValueNet
from core.models.alphazero_replay import AZTransition, AlphaZeroReplayBuffer
from core.models.alphazero_trainer import AlphaZeroTrainConfig, train_alphazero_step


def _make_transition(n_obs: int, n_actions: list[int], value: float, policy_version: int) -> AZTransition:
    return AZTransition(
        state=np.random.randn(n_obs).astype(np.float32),
        policy_targets=[np.ones(a, dtype=np.float32) / float(a) for a in n_actions],
        value_target=float(value),
        policy_version=int(policy_version),
    )


def test_az_replay_state_roundtrip_preserves_policy_version():
    replay = AlphaZeroReplayBuffer(capacity=32)
    replay.push(_make_transition(8, [3, 2, 5], value=1.0, policy_version=7))
    replay.push(_make_transition(8, [3, 2, 5], value=-1.0, policy_version=8))

    payload = replay.state_dict()
    clone = AlphaZeroReplayBuffer(capacity=32)
    loaded = clone.load_state_dict(payload)

    assert loaded == 2
    assert len(clone) == 2
    sample = clone.sample(2)
    assert {int(s.policy_version) for s in sample} == {7, 8}


def test_az_replay_balanced_outcome_sampling_smoke():
    n_obs = 10
    n_actions = [4, 2, 6]
    replay = AlphaZeroReplayBuffer(capacity=128)
    for _ in range(20):
        replay.push(_make_transition(n_obs, n_actions, value=1.0, policy_version=1))
    for _ in range(20):
        replay.push(_make_transition(n_obs, n_actions, value=-1.0, policy_version=1))
    for _ in range(20):
        replay.push(_make_transition(n_obs, n_actions, value=-0.25, policy_version=1))

    batch = replay.sample_balanced_outcome(24)
    assert len(batch) == 24
    signs = {np.sign(float(b.value_target)) for b in batch}
    assert 1.0 in signs
    assert -1.0 in signs


def test_az_train_step_staleness_filter_skips_old_samples():
    n_obs = 12
    n_actions = [5, 3, 7]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    optimizer = torch.optim.Adam(net.parameters(), lr=1e-3)
    replay = AlphaZeroReplayBuffer(capacity=64)
    for _ in range(32):
        replay.push(_make_transition(n_obs, n_actions, value=1.0, policy_version=0))

    cfg = AlphaZeroTrainConfig(
        batch_size=16,
        balanced_outcome_sampling=True,
        max_policy_staleness_updates=0,
    )
    out = train_alphazero_step(
        net=net,
        optimizer=optimizer,
        replay=replay,
        config=cfg,
        device=torch.device("cpu"),
        current_policy_version=10,
    )
    assert out is None


def test_az_train_step_balanced_sampling_runs():
    n_obs = 12
    n_actions = [5, 3, 7]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    optimizer = torch.optim.Adam(net.parameters(), lr=1e-3)
    replay = AlphaZeroReplayBuffer(capacity=64)
    for _ in range(20):
        replay.push(_make_transition(n_obs, n_actions, value=1.0, policy_version=9))
    for _ in range(20):
        replay.push(_make_transition(n_obs, n_actions, value=-1.0, policy_version=9))
    for _ in range(20):
        replay.push(_make_transition(n_obs, n_actions, value=-0.25, policy_version=9))

    cfg = AlphaZeroTrainConfig(
        batch_size=24,
        balanced_outcome_sampling=True,
        max_policy_staleness_updates=5,
    )
    out = train_alphazero_step(
        net=net,
        optimizer=optimizer,
        replay=replay,
        config=cfg,
        device=torch.device("cpu"),
        current_policy_version=10,
    )
    assert out is not None
    assert float(out["loss"]) >= 0.0
