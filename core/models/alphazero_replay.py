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
    policy_version: int = 0


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

    def sample_balanced_outcome(self, batch_size: int) -> list[AZTransition]:
        """
        Quality-oriented sampling:
        - стараемся сохранить баланс между win/loss/draw-like исходами,
        - fallback на uniform, если данных мало.
        """
        bs = max(1, int(batch_size))
        if len(self.buffer) <= bs:
            return list(self.buffer)

        wins: list[AZTransition] = []
        losses: list[AZTransition] = []
        draws: list[AZTransition] = []
        for t in self.buffer:
            v = float(getattr(t, "value_target", 0.0))
            if v > 0.20:
                wins.append(t)
            elif v < -0.50:
                losses.append(t)
            else:
                draws.append(t)

        groups = [wins, losses, draws]
        non_empty = [g for g in groups if g]
        if not non_empty:
            return self.sample(bs)

        out: list[AZTransition] = []
        per_group = max(1, bs // len(non_empty))
        for g in non_empty:
            take_n = min(len(g), per_group)
            out.extend(random.sample(g, take_n) if len(g) > take_n else list(g))

        if len(out) < bs:
            picked = {id(t) for t in out}
            rest = [t for t in self.buffer if id(t) not in picked]
            random.shuffle(rest)
            need = bs - len(out)
            out.extend(rest[:need])

        if len(out) > bs:
            out = random.sample(out, bs)
        return out

    def state_dict(self) -> dict:
        items = []
        for t in self.buffer:
            items.append(
                {
                    "state": np.asarray(t.state, dtype=np.float32),
                    "policy_targets": [np.asarray(p, dtype=np.float32) for p in list(t.policy_targets)],
                    "value_target": float(t.value_target),
                    "policy_version": int(getattr(t, "policy_version", 0)),
                }
            )
        return {
            "type": "alphazero_replay",
            "capacity": int(self.capacity),
            "items": items,
        }

    def load_state_dict(self, state: dict) -> int:
        if not isinstance(state, dict):
            return 0
        items = state.get("items")
        if not isinstance(items, list):
            return 0
        self.buffer.clear()
        for raw in items[-self.capacity:]:
            if not isinstance(raw, dict):
                continue
            state_np = np.asarray(raw.get("state", []), dtype=np.float32)
            targets_raw = raw.get("policy_targets", [])
            if not isinstance(targets_raw, list):
                continue
            policy_targets = [np.asarray(p, dtype=np.float32) for p in targets_raw]
            value_target = float(raw.get("value_target", 0.0) or 0.0)
            policy_version = int(raw.get("policy_version", 0) or 0)
            self.buffer.append(
                AZTransition(
                    state=state_np,
                    policy_targets=policy_targets,
                    value_target=value_target,
                    policy_version=policy_version,
                )
            )
        return len(self.buffer)
