# tests/models/test_phoenix_replay.py
import numpy as np

from core.models.phoenix_replay import SequenceReplayBuffer, SequenceWindow


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


def test_push_window_roundtrip():
    buf = SequenceReplayBuffer(capacity=4, window=2)
    win = SequenceWindow(
        obs=np.arange(12, dtype=np.float32).reshape(3, 4),
        actions=np.zeros((3, 2), dtype=np.int64),
        active_masks=np.ones((3, 2), dtype=bool),
        rewards=np.asarray([1.0, 2.0, 3.0], dtype=np.float32),
        dones=np.asarray([0.0, 0.0, 1.0], dtype=np.float32),
    )
    buf.push_window(win)
    windows, idx, weights = buf.sample(1)
    assert len(windows) == 1
    assert np.allclose(windows[0].obs, win.obs)
    assert np.allclose(windows[0].rewards, win.rewards)
    assert idx.shape == (1,) and weights.shape == (1,)


def test_push_window_priority_sets_leaf():
    buf = SequenceReplayBuffer(capacity=4, window=2)
    win = SequenceWindow(
        obs=np.zeros((3, 2), dtype=np.float32),
        actions=np.zeros((3, 1), dtype=np.int64),
        active_masks=np.ones((3, 1), dtype=bool),
        rewards=np.zeros(3, dtype=np.float32),
        dones=np.zeros(3, dtype=np.float32),
    )
    buf.push_window(win, priority=0.5)
    buf.push_window(win, priority=4.0)
    first = float(buf.sum_tree[buf.tree_size + 0])
    second = float(buf.sum_tree[buf.tree_size + 1])
    assert second > first


def test_steps_are_trimmed_after_capacity():
    buf = SequenceReplayBuffer(capacity=3, window=2)
    _push_episode(buf, 20)
    assert len(buf) == 3
    # Legacy step-push keeps only rolling tail; old materialized windows stay in capacity ring.
    assert len(buf._steps) <= buf.span


def test_done_tail_padding_not_cross_episode_when_window_pushed():
    buf = SequenceReplayBuffer(capacity=4, window=2)
    win = {
        "obs": np.asarray([[0, 0], [1, 1], [1, 1]], dtype=np.float32),
        "actions": np.zeros((3, 1), dtype=np.int64),
        "active_masks": np.ones((3, 1), dtype=bool),
        "rewards": np.asarray([1.0, 0.0, 0.0], dtype=np.float32),
        "dones": np.asarray([0.0, 0.0, 1.0], dtype=np.float32),
    }
    buf.push_window(win)
    windows, _, _ = buf.sample(1)
    assert windows[0].dones.tolist() == [0.0, 0.0, 1.0]
    assert np.allclose(windows[0].obs[1], windows[0].obs[2])
