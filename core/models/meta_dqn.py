"""Meta-learning interface stub (MAML-style) for future DQN fast adaptation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Optional

import torch


@dataclass
class MetaDQNConfig:
    inner_lr: float = 1e-3
    outer_lr: float = 1e-4
    inner_steps: int = 1


class MetaDQNTrainer:
    """
    Placeholder for meta-learning loops. Not wired into train.py yet.
    """

    def __init__(self, model_factory: Callable[[], torch.nn.Module], config: Optional[MetaDQNConfig] = None):
        self.model_factory = model_factory
        self.config = config or MetaDQNConfig()

    def inner_loop(self, model: torch.nn.Module, tasks: Iterable) -> float:
        raise NotImplementedError("MetaDQN inner_loop: implement task-specific adaptation")

    def outer_loop(self, task_batches) -> dict:
        raise NotImplementedError("MetaDQN outer_loop: implement meta-gradient update")
