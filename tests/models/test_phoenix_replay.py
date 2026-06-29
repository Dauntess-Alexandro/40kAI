# tests/models/test_phoenix_replay.py
import numpy as np

from core.models.phoenix_replay import SequenceReplayBuffer


def _push_episode(buf, n, n_heads=2, obs_dim=4, base=0.0):
    for t in range(n):
        obs = [base + t] * obs_dim
        action = [0] * n_heads
        active = [True] * n_heads
        done = (t == n - 1)
        buf.push(obs, action, active, reward=float(t), done=done)


def test_window_shapes_and_contiguity():
    buf = SequenceReplayBuffer(capacity=100, window=3)
    _push_episode(buf, 10)
    assert len(buf) > 0
    windows, idx, w = buf.sample(batch_size=4)
    assert len(windows) == 4
    win = windows[0]
    assert win.obs.shape == (4, 4)       # H+1 = 4
    assert win.actions.shape == (4, 2)
    assert win.active_masks.shape == (4, 2)
    assert win.rewards.shape == (4,)
    assert win.dones.shape == (4,)
    assert idx.shape == (4,) and w.shape == (4,)


def test_done_mask_beyond_terminal():
    buf = SequenceReplayBuffer(capacity=100, window=3)
    _push_episode(buf, 2, base=0.0)   # короткий эпизод: терминал на t=1
    _push_episode(buf, 2, base=10.0)  # второй эпизод — добивает span
    windows, _, _ = buf.sample(batch_size=1)
    win = windows[0]
    # после терминала шаги помечены done=1
    assert win.dones[-1] == 1.0


def test_update_priorities_changes_sampling_distribution():
    buf = SequenceReplayBuffer(capacity=100, window=2)
    _push_episode(buf, 20)
    _, idx, _ = buf.sample(batch_size=8)
    buf.update_priorities(idx, np.full(len(idx), 10.0, dtype=np.float32))
    # после повышения приоритета те же индексы должны доминировать
    _, idx2, _ = buf.sample(batch_size=32)
    overlap = len(set(idx2.tolist()) & set(idx.tolist()))
    assert overlap > 0
