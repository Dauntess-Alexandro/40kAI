from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import random
from typing import Any

import numpy as np


@dataclass
class GMZTransition:
    state: np.ndarray
    action: np.ndarray
    reward: float
    done: bool
    policy_targets: list[np.ndarray]
    value_target: float
    behavior_logits: list[np.ndarray] | None = None  # A3: pre-softmax root logits for V-trace IS
    legal_masks_by_head: list[np.ndarray] | None = None  # B2: for real-search reanalysis
    policy_version: int = 0


class GumbelMuZeroReplayBuffer:
    def __init__(self, capacity: int = 250_000):
        self.capacity = int(max(1, capacity))
        self.buffer: deque[GMZTransition] = deque(maxlen=self.capacity)

    def __len__(self) -> int:
        return len(self.buffer)

    def push(self, transition: GMZTransition) -> None:
        self.buffer.append(transition)

    def push_many(self, transitions: list[GMZTransition]) -> None:
        for t in transitions:
            self.push(t)

    def sample(self, batch_size: int) -> list[GMZTransition]:
        n = min(len(self.buffer), max(1, int(batch_size)))
        if n <= 0:
            return []
        return random.sample(list(self.buffer), n)

    def sample_unroll(
        self,
        batch_size: int,
        unroll_steps: int,
        max_policy_staleness_updates: int = -1,
        current_policy_version: int = 0,
    ) -> list[dict[str, Any]]:
        if len(self.buffer) == 0:
            return []
        n = min(len(self.buffer), max(1, int(batch_size)))
        starts = random.sample(range(len(self.buffer)), n)
        out: list[dict[str, Any]] = []
        min_ver = int(current_policy_version) - int(max_policy_staleness_updates)
        for start in starts:
            tr = self.buffer[start]
            if int(max_policy_staleness_updates) >= 0 and int(tr.policy_version) < min_ver:
                continue
            seq_states: list[np.ndarray] = []
            seq_actions: list[np.ndarray] = []
            seq_rewards: list[float] = []
            seq_dones: list[float] = []
            seq_policies: list[list[np.ndarray]] = []
            seq_values: list[float] = []
            seq_behavior_logits: list[list[np.ndarray]] = []  # A3
            for k in range(max(1, int(unroll_steps))):
                idx = min(start + k, len(self.buffer) - 1)
                cur = self.buffer[idx]
                seq_states.append(np.asarray(cur.state, dtype=np.float32))
                seq_actions.append(np.asarray(cur.action, dtype=np.int64))
                seq_rewards.append(float(cur.reward))
                seq_dones.append(float(bool(cur.done)))
                seq_policies.append([np.asarray(x, dtype=np.float32) for x in cur.policy_targets])
                seq_values.append(float(cur.value_target))
                seq_behavior_logits.append(
                    [np.asarray(x, dtype=np.float32) for x in (cur.behavior_logits or [])]
                )
                if bool(cur.done):
                    break
            out.append(
                {
                    "states": seq_states,
                    "actions": seq_actions,
                    "rewards": seq_rewards,
                    "dones": seq_dones,
                    "policy_targets": seq_policies,
                    "value_targets": seq_values,
                    "behavior_logits": seq_behavior_logits,
                    "legal_masks_by_head": [
                        [np.asarray(x, dtype=np.float32) for x in cur.legal_masks_by_head]
                        if cur.legal_masks_by_head else []
                        for _ in range(len(seq_states))
                    ],
                    "policy_version": int(tr.policy_version),
                }
            )
        return out

    def state_dict(self) -> dict[str, Any]:
        return {
            "capacity": int(self.capacity),
            "buffer": [
                {
                    "state": np.asarray(x.state, dtype=np.float32),
                    "action": np.asarray(x.action, dtype=np.int64),
                    "reward": float(x.reward),
                    "done": bool(x.done),
                    "policy_targets": [np.asarray(p, dtype=np.float32) for p in x.policy_targets],
                    "behavior_logits": [
                        np.asarray(b, dtype=np.float32) for b in (x.behavior_logits or [])
                    ],
                    "legal_masks_by_head": [
                        np.asarray(m, dtype=np.float32) for m in (x.legal_masks_by_head or [])
                    ],
                    "value_target": float(x.value_target),
                    "policy_version": int(x.policy_version),
                }
                for x in self.buffer
            ],
        }

    def load_state_dict(self, payload: dict[str, Any]) -> None:
        self.capacity = int(payload.get("capacity", self.capacity) or self.capacity)
        self.buffer = deque(maxlen=self.capacity)
        rows = payload.get("buffer") if isinstance(payload, dict) else None
        if not isinstance(rows, list):
            return
        for row in rows:
            if not isinstance(row, dict):
                continue
            self.buffer.append(
                GMZTransition(
                    state=np.asarray(row.get("state"), dtype=np.float32),
                    action=np.asarray(row.get("action"), dtype=np.int64),
                    reward=float(row.get("reward", 0.0) or 0.0),
                    done=bool(row.get("done", False)),
                    policy_targets=[np.asarray(p, dtype=np.float32) for p in (row.get("policy_targets") or [])],
                    behavior_logits=[
                        np.asarray(b, dtype=np.float32) for b in (row.get("behavior_logits") or [])
                    ],
                    legal_masks_by_head=[
                        np.asarray(m, dtype=np.float32) for m in (row.get("legal_masks_by_head") or [])
                    ],
                    value_target=float(row.get("value_target", 0.0) or 0.0),
                    policy_version=int(row.get("policy_version", 0) or 0),
                )
            )
