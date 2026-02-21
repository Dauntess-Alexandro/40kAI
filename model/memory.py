from collections import namedtuple, deque
import random
import numpy as np
import threading

Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward', 'n_step', 'next_shoot_mask'))

class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)
        self._prefetch = None
        self._lock = threading.Lock()
        self._prefetch_thread = None
        self._prefetch_result = None

    def _start_async_prefetch(self, batch_size):
        def _worker():
            self._prefetch_result = self._sample_impl(batch_size)

        self._prefetch_thread = threading.Thread(target=_worker, daemon=True)
        self._prefetch_thread.start()

    def push(self, *args):
        with self._lock:
            self.memory.append(Transition(*args))

    def _sample_impl(self, batch_size):
        with self._lock:
            return random.sample(self.memory, batch_size)

    def sample(self, batch_size, prefetch=False):
        if not prefetch:
            return self._sample_impl(batch_size)
        if self._prefetch_thread is not None:
            self._prefetch_thread.join()
            result = self._prefetch_result
        else:
            result = self._sample_impl(batch_size)
        self._start_async_prefetch(batch_size)
        return result

    def __len__(self):
        return len(self.memory)


class PrioritizedReplayMemory(object):
    def __init__(self, capacity, alpha=0.6, eps=1e-6):
        self.capacity = capacity
        self.alpha = alpha
        self.eps = eps
        self.memory = [None] * capacity
        self.size = 0
        self.pos = 0
        self.max_priority = 1.0
        self._lock = threading.Lock()
        self._prefetch_thread = None
        self._prefetch_result = None
        self.tree_size = 1
        while self.tree_size < capacity:
            self.tree_size <<= 1
        self.sum_tree = np.zeros(2 * self.tree_size, dtype=np.float32)
        self.min_tree = np.full(2 * self.tree_size, np.inf, dtype=np.float32)

    def _start_async_prefetch(self, batch_size, beta):
        def _worker():
            self._prefetch_result = self._sample_impl(batch_size, beta=beta)

        self._prefetch_thread = threading.Thread(target=_worker, daemon=True)
        self._prefetch_thread.start()

    def _set_leaf(self, data_idx, priority_alpha):
        leaf = data_idx + self.tree_size
        self.sum_tree[leaf] = priority_alpha
        self.min_tree[leaf] = priority_alpha
        leaf //= 2
        while leaf >= 1:
            left = leaf * 2
            right = left + 1
            self.sum_tree[leaf] = self.sum_tree[left] + self.sum_tree[right]
            self.min_tree[leaf] = min(self.min_tree[left], self.min_tree[right])
            leaf //= 2

    def _prefix_search(self, mass):
        idx = 1
        while idx < self.tree_size:
            left = idx * 2
            if self.sum_tree[left] >= mass:
                idx = left
            else:
                mass -= self.sum_tree[left]
                idx = left + 1
        return idx - self.tree_size

    def push(self, *args):
        transition = Transition(*args)
        with self._lock:
            self.memory[self.pos] = transition
            priority_alpha = float(max(self.max_priority, self.eps)) ** self.alpha
            self._set_leaf(self.pos, priority_alpha)
            if self.size < self.capacity:
                self.size += 1
            self.pos = (self.pos + 1) % self.capacity

    def _sample_impl(self, batch_size, beta=0.4):
        with self._lock:
            if self.size == 0:
                return [], [], []
            total = float(self.sum_tree[1])
            if total <= 0.0:
                return [], [], []

            actual_batch = int(batch_size)
            segment = total / actual_batch
            indices = []
            priorities_alpha = []
            samples = []
            for i in range(actual_batch):
                a = segment * i
                b = segment * (i + 1)
                mass = random.uniform(a, b)
                idx = self._prefix_search(mass)
                if idx >= self.size:
                    idx = self.size - 1
                indices.append(idx)
                p_alpha = float(self.sum_tree[idx + self.tree_size])
                priorities_alpha.append(p_alpha)
                samples.append(self.memory[idx])

            probs = np.asarray(priorities_alpha, dtype=np.float32) / total
            probs = np.clip(probs, 1e-12, None)
            weights = (self.size * probs) ** (-beta)
            weights /= weights.max()
            return samples, np.asarray(indices, dtype=np.int64), weights.astype(np.float32)

    def sample(self, batch_size, beta=0.4, prefetch=False):
        if not prefetch:
            return self._sample_impl(batch_size, beta=beta)
        if self._prefetch_thread is not None:
            self._prefetch_thread.join()
            result = self._prefetch_result
        else:
            result = self._sample_impl(batch_size, beta=beta)
        self._start_async_prefetch(batch_size, beta=beta)
        return result

    def update_priorities(self, indices, priorities):
        with self._lock:
            for idx, priority in zip(indices, priorities):
                value = float(priority)
                if value < self.eps:
                    value = self.eps
                p_alpha = value ** self.alpha
                self._set_leaf(int(idx), p_alpha)
                if value > self.max_priority:
                    self.max_priority = value

    def __len__(self):
        return self.size
