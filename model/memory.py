from collections import namedtuple, deque
import os
import random
import numpy as np

_NUMBA_DISABLED = os.environ.get("WARHAMMER_DISABLE_NUMBA", "").strip().lower() in {"1", "true", "yes", "on"}

try:
    if _NUMBA_DISABLED:
        raise ImportError("numba disabled by WARHAMMER_DISABLE_NUMBA")
    from numba import njit
    NUMBA_AVAILABLE = True
except Exception:
    NUMBA_AVAILABLE = False

    def njit(*args, **kwargs):
        def _decorator(func):
            return func

        return _decorator

Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward', 'n_step', 'next_shoot_mask'))


@njit(cache=True)
def _compute_per_probs(priorities, alpha, eps):
    scaled = np.power(priorities, alpha)
    total = scaled.sum()
    if not np.isfinite(total) or total <= eps:
        count = priorities.shape[0]
        return np.full(count, 1.0 / count, dtype=np.float32)
    probs = scaled / total
    probs = np.maximum(probs, eps)
    probs = probs / probs.sum()
    return probs.astype(np.float32)


@njit(cache=True)
def _sanitize_priority(priority, eps):
    value = np.float32(priority)
    if not np.isfinite(value):
        return np.float32(eps)
    if value < eps:
        return np.float32(eps)
    return value

class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)
        self._prefetch = None

    def push(self, *args):
        self.memory.append(Transition(*args))

    def _sample_impl(self, batch_size):
        return random.sample(self.memory, batch_size)

    def sample(self, batch_size, prefetch=False):
        if not prefetch:
            return self._sample_impl(batch_size)
        if self._prefetch is None:
            self._prefetch = self._sample_impl(batch_size)
        result = self._prefetch
        self._prefetch = self._sample_impl(batch_size)
        return result

    def __len__(self):
        return len(self.memory)


class PrioritizedReplayMemory(object):
    def __init__(self, capacity, alpha=0.6, eps=1e-6):
        self.capacity = capacity
        self.alpha = alpha
        self.eps = eps
        self.memory = []
        self.priorities = []
        self.pos = 0
        self.max_priority = 1.0
        self._prefetch = None

    def push(self, *args):
        transition = Transition(*args)
        if len(self.memory) < self.capacity:
            self.memory.append(transition)
            self.priorities.append(self.max_priority)
        else:
            self.memory[self.pos] = transition
            self.priorities[self.pos] = self.max_priority
        self.pos = (self.pos + 1) % self.capacity

    def _sample_impl(self, batch_size, beta=0.4):
        if len(self.memory) == 0:
            return [], [], []
        priorities = np.array(self.priorities, dtype=np.float32)
        probs = _compute_per_probs(priorities, self.alpha, self.eps)
        indices = np.random.choice(len(self.memory), batch_size, p=probs)
        samples = [self.memory[idx] for idx in indices]
        weights = (len(self.memory) * probs[indices]) ** (-beta)
        max_weight = weights.max()
        if np.isfinite(max_weight) and max_weight > 0:
            weights = weights / max_weight
        else:
            weights = np.ones_like(weights, dtype=np.float32)
        return samples, indices, weights.astype(np.float32)

    def sample(self, batch_size, beta=0.4, prefetch=False):
        if not prefetch:
            return self._sample_impl(batch_size, beta=beta)
        if self._prefetch is None:
            self._prefetch = self._sample_impl(batch_size, beta=beta)
        result = self._prefetch
        self._prefetch = self._sample_impl(batch_size, beta=beta)
        return result

    def update_priorities(self, indices, priorities):
        for idx, priority in zip(indices, priorities):
            if idx < 0 or idx >= len(self.priorities):
                continue
            value = float(_sanitize_priority(priority, self.eps))
            self.priorities[idx] = value
            if value > self.max_priority:
                self.max_priority = value

    def __len__(self):
        return len(self.memory)
