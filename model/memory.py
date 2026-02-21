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
        self.memory = []
        self.priorities = []
        self.pos = 0
        self.max_priority = 1.0
        self._prefetch = None
        self._lock = threading.Lock()
        self._prefetch_thread = None
        self._prefetch_result = None

    def _start_async_prefetch(self, batch_size, beta):
        def _worker():
            self._prefetch_result = self._sample_impl(batch_size, beta=beta)

        self._prefetch_thread = threading.Thread(target=_worker, daemon=True)
        self._prefetch_thread.start()

    def push(self, *args):
        transition = Transition(*args)
        with self._lock:
            if len(self.memory) < self.capacity:
                self.memory.append(transition)
                self.priorities.append(self.max_priority)
            else:
                self.memory[self.pos] = transition
                self.priorities[self.pos] = self.max_priority
            self.pos = (self.pos + 1) % self.capacity

    def _sample_impl(self, batch_size, beta=0.4):
        with self._lock:
            if len(self.memory) == 0:
                return [], [], []
            priorities = np.array(self.priorities, dtype=np.float32)
            scaled = priorities ** self.alpha
            probs = scaled / scaled.sum()
            indices = np.random.choice(len(self.memory), batch_size, p=probs)
            samples = [self.memory[idx] for idx in indices]
            weights = (len(self.memory) * probs[indices]) ** (-beta)
            weights = weights / weights.max()
            return samples, indices, weights.astype(np.float32)

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
                self.priorities[idx] = value
                if value > self.max_priority:
                    self.max_priority = value

    def __len__(self):
        return len(self.memory)
