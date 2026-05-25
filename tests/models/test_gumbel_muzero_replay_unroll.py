import numpy as np

from core.models.gumbel_muzero_replay import GMZTransition, GumbelMuZeroReplayBuffer


def _tr(idx: int, done: bool, ver: int) -> GMZTransition:
    return GMZTransition(
        state=np.array([idx, idx + 1], dtype=np.float32),
        action=np.array([idx % 2, (idx + 1) % 3], dtype=np.int64),
        reward=float(idx) * 0.1,
        done=bool(done),
        policy_targets=[
            np.array([0.6, 0.4], dtype=np.float32),
            np.array([0.2, 0.3, 0.5], dtype=np.float32),
        ],
        behavior_logits=[
            np.zeros(2, dtype=np.float32),
            np.zeros(3, dtype=np.float32),
        ],
        value_target=float(1.0 if idx % 2 == 0 else -1.0),
        policy_version=int(ver),
    )


def test_gumbel_muzero_replay_unroll_and_roundtrip():
    replay = GumbelMuZeroReplayBuffer(capacity=32)
    for i in range(10):
        replay.push(_tr(i, done=(i in {4, 9}), ver=5))

    batch = replay.sample_unroll(batch_size=4, unroll_steps=5, current_policy_version=6)
    assert len(batch) == 4
    assert all(len(item["states"]) >= 1 for item in batch)
    assert all(len(item["actions"]) >= 1 for item in batch)

    payload = replay.state_dict()
    clone = GumbelMuZeroReplayBuffer(capacity=1)
    clone.load_state_dict(payload)
    assert len(clone) == len(replay)
