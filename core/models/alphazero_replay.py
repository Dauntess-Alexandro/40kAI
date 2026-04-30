from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class AZTransition:
    state: np.ndarray
    policy_targets: list[np.ndarray]
    value_target: float


class AlphaZeroReplayBuffer:
    def __init__(self, capacity: int = 200000):
        self.capacity = max(1, int(capacity))
        self.buffer: deque[AZTransition] = deque(maxlen=self.capacity)

    def __len__(self) -> int:
        return len(self.buffer)

    def push(self, transition: AZTransition) -> None:
        self.buffer.append(transition)

    def push_many(self, transitions: List[AZTransition]) -> None:
        for t in transitions:
            self.push(t)

    def sample(self, batch_size: int) -> list[AZTransition]:
        bs = max(1, int(batch_size))
        if len(self.buffer) <= bs:
            return list(self.buffer)
        return random.sample(self.buffer, bs)
