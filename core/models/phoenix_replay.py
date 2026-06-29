# core/models/phoenix_replay.py
"""PHOENIX sequence-replay: sum-tree по началу окна, per-step маски голов.

Реюз — МЕХАНИЗМ sum-tree (как в PrioritizedReplayMemory), но индексируем по
НАЧАЛУ окна длиной window+1 шагов, а не по одиночному переходу."""
from __future__ import annotations

import random
import threading
from collections import namedtuple
from typing import Any

import numpy as np

SequenceWindow = namedtuple("SequenceWindow", ("obs", "actions", "active_masks", "rewards", "dones"))


class SequenceReplayBuffer:
    def __init__(self, capacity: int, window: int, alpha: float = 0.6, eps: float = 1e-6):
        self.capacity = int(capacity)
        self.window = int(window)            # H; окно = H+1 шагов
        self.span = self.window + 1
        self.alpha = float(alpha)
        self.eps = float(eps)
        self._steps: list = []               # только короткий rolling-tail для legacy push()
        self._windows: list[SequenceWindow | None] = [None] * self.capacity
        self.size = 0
        self.pos = 0
        self.max_priority = 1.0
        self._lock = threading.Lock()
        self.tree_size = 1
        while self.tree_size < self.capacity:
            self.tree_size <<= 1
        self.sum_tree = np.zeros(2 * self.tree_size, dtype=np.float32)

    def _set_leaf(self, data_idx: int, priority_alpha: float):
        leaf = data_idx + self.tree_size
        self.sum_tree[leaf] = priority_alpha
        leaf //= 2
        while leaf >= 1:
            self.sum_tree[leaf] = self.sum_tree[2 * leaf] + self.sum_tree[2 * leaf + 1]
            leaf //= 2

    def _prefix_search(self, mass: float) -> int:
        idx = 1
        while idx < self.tree_size:
            left = idx * 2
            if self.sum_tree[left] >= mass:
                idx = left
            else:
                mass -= self.sum_tree[left]
                idx = left + 1
        return idx - self.tree_size

    def push(self, obs, action, active_mask, reward: float, done: bool):
        with self._lock:
            self._steps.append((
                np.asarray(obs, dtype=np.float32),
                np.asarray(action, dtype=np.int64),
                np.asarray(active_mask, dtype=bool),
                float(reward),
                bool(done),
            ))
            if len(self._steps) >= self.span:
                self._register_window(self._materialize_from_steps(self._steps[-self.span:]))
            # bounded tail: для следующего окна нужен только последний span шагов.
            if len(self._steps) > self.span:
                self._steps = self._steps[-self.span:]

    def push_window(self, window: SequenceWindow | dict[str, Any], priority: float | None = None) -> None:
        """Добавить уже materialized окно H+1 от actor-process/PC2.

        Actor-side materialization не даёт learner'у случайно склеить шаги разных акторов или
        разных эпизодов. `done`-tail приходит уже размеченным, здесь только shape/dtype validation.
        """
        win = self._coerce_window(window)
        with self._lock:
            self._register_window(win, priority=priority)

    def push_windows(self, windows, priorities=None) -> int:
        count = 0
        priorities = list(priorities) if priorities is not None else []
        for i, window in enumerate(windows or []):
            priority = priorities[i] if i < len(priorities) else None
            self.push_window(window, priority=priority)
            count += 1
        return count

    def _register_window(self, window: SequenceWindow, priority: float | None = None):
        self._windows[self.pos] = window
        raw_priority = float(self.max_priority)
        if priority is not None:
            try:
                raw_priority = max(float(priority), self.eps)
                self.max_priority = max(self.max_priority, raw_priority)
            except (TypeError, ValueError):
                pass
        p_alpha = float(max(raw_priority, self.eps)) ** self.alpha
        self._set_leaf(self.pos, p_alpha)
        if self.size < self.capacity:
            self.size += 1
        self.pos = (self.pos + 1) % self.capacity

    def _coerce_window(self, window: SequenceWindow | dict[str, Any]) -> SequenceWindow:
        if isinstance(window, dict):
            src = window
            win = SequenceWindow(
                src.get("obs"),
                src.get("actions"),
                src.get("active_masks"),
                src.get("rewards"),
                src.get("dones"),
            )
        else:
            win = window
        obs = np.asarray(win.obs, dtype=np.float32)
        actions = np.asarray(win.actions, dtype=np.int64)
        active = np.asarray(win.active_masks, dtype=bool)
        rewards = np.asarray(win.rewards, dtype=np.float32)
        dones = np.asarray(win.dones, dtype=np.float32)
        if obs.shape[0] != self.span:
            raise ValueError(
                f"PHOENIX replay window obs span mismatch: got {obs.shape[0]}, expected {self.span}. "
                "Где: SequenceReplayBuffer.push_window. Что делать: проверьте spr_horizon_K/ve_horizon у акторов."
            )
        if actions.shape[0] != self.span or active.shape[0] != self.span:
            raise ValueError(
                "PHOENIX replay window action/mask span mismatch. "
                "Где: SequenceReplayBuffer.push_window. Что делать: проверьте sequence assembler акторов."
            )
        if rewards.shape != (self.span,) or dones.shape != (self.span,):
            raise ValueError(
                "PHOENIX replay window rewards/dones shape mismatch. "
                "Где: SequenceReplayBuffer.push_window. Что делать: отправляйте rewards/dones длиной H+1."
            )
        return SequenceWindow(obs, actions, active, rewards, dones)

    def _materialize_from_steps(self, steps) -> SequenceWindow:
        obs = np.stack([s[0] for s in steps])
        actions = np.stack([s[1] for s in steps])
        active = np.stack([s[2] for s in steps])
        rewards = np.asarray([s[3] for s in steps], dtype=np.float32)
        # done-маска: terminal transition валиден; 1 ставим только на padding/шаги после терминала.
        dones = np.zeros(self.span, dtype=np.float32)
        terminated = False
        for k, s in enumerate(steps):
            if terminated:
                dones[k] = 1.0
            if s[4]:
                terminated = True
                if k + 1 < self.span:
                    dones[k + 1:] = 1.0
        return SequenceWindow(obs, actions, active, rewards, dones)

    def __len__(self) -> int:
        return self.size

    def sample(self, batch_size: int, beta: float = 0.4):
        with self._lock:
            total = float(self.sum_tree[1])
            if self.size == 0 or total <= 0.0:
                return [], np.zeros(0, dtype=np.int64), np.zeros(0, dtype=np.float32)
            segment = total / batch_size
            indices, samples, pri = [], [], []
            for i in range(batch_size):
                mass = random.uniform(segment * i, segment * (i + 1))
                idx = self._prefix_search(mass)
                if idx >= self.size:
                    idx = self.size - 1
                indices.append(idx)
                pri.append(float(self.sum_tree[idx + self.tree_size]))
                win = self._windows[idx]
                if win is None:
                    continue
                samples.append(win)
            probs = np.asarray(pri, dtype=np.float32) / total
            probs = np.clip(probs, 1e-12, None)
            weights = (self.size * probs) ** (-beta)
            weights /= weights.max()
            return samples, np.asarray(indices, dtype=np.int64), weights.astype(np.float32)

    def update_priorities(self, indices, priorities):
        with self._lock:
            for idx, priority in zip(indices, priorities):
                value = max(float(priority), self.eps)
                self._set_leaf(int(idx), value ** self.alpha)
                if value > self.max_priority:
                    self.max_priority = value
