from collections import namedtuple, deque
import random
import numpy as np

Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward', 'n_step', 'next_shoot_mask'))

class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

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

    def push(self, *args):
        transition = Transition(*args)
        if len(self.memory) < self.capacity:
            self.memory.append(transition)
            self.priorities.append(self.max_priority)
        else:
            self.memory[self.pos] = transition
            self.priorities[self.pos] = self.max_priority
        self.pos = (self.pos + 1) % self.capacity

    def sample(self, batch_size, beta=0.4):
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

    def update_priorities(self, indices, priorities):
        for idx, priority in zip(indices, priorities):
            value = float(priority)
            self.priorities[idx] = value
            if value > self.max_priority:
                self.max_priority = value

    def __len__(self):
        return len(self.memory)
