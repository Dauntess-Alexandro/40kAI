from __future__ import annotations

import copy
import math
import random
from dataclasses import dataclass
from typing import Callable, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

from model.agent_types import AgentType


class AlphaZeroNet(nn.Module):
    """Сеть AlphaZero с общим trunk, policy-head и value-head."""

    def __init__(self, observation_dim: int, action_sizes: list[int], hidden_dim: int = 256):
        super().__init__()
        self.observation_dim = int(observation_dim)
        self.action_sizes = [int(v) for v in action_sizes]

        self.trunk = nn.Sequential(
            nn.Linear(self.observation_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )
        self.policy_heads = nn.ModuleList([nn.Linear(hidden_dim, size) for size in self.action_sizes])
        self.value_head = nn.Linear(hidden_dim, 1)

    def forward(self, obs: torch.Tensor) -> tuple[list[torch.Tensor], torch.Tensor]:
        if obs.dim() == 1:
            obs = obs.unsqueeze(0)
        x = self.trunk(obs)
        logits = [head(x) for head in self.policy_heads]
        value = torch.tanh(self.value_head(x)).squeeze(-1)
        return logits, value


@dataclass
class MCTSConfig:
    simulations: int = 32
    c_puct: float = 1.25
    dirichlet_alpha: float = 0.3
    dirichlet_eps: float = 0.25
    max_children: int = 16


@dataclass
class SearchResult:
    policy: torch.Tensor
    best_action: dict[str, int]
    root_value: float


class MCTSNode:
    def __init__(self, prior: float = 1.0):
        self.prior = float(prior)
        self.visit_count = 0
        self.value_sum = 0.0
        self.children: dict[tuple[int, ...], "MCTSNode"] = {}

    @property
    def q_value(self) -> float:
        if self.visit_count == 0:
            return 0.0
        return self.value_sum / self.visit_count


class AlphaZeroMCTS:
    """MCTS с PUCT. Требует функцию rollout(action)->(reward, value, priors, done)."""

    def __init__(self, cfg: Optional[MCTSConfig] = None):
        self.cfg = cfg or MCTSConfig()

    def _ucb_score(self, parent: MCTSNode, child: MCTSNode) -> float:
        pb_c = self.cfg.c_puct * child.prior * math.sqrt(parent.visit_count + 1) / (child.visit_count + 1)
        return child.q_value + pb_c

    def search(
        self,
        root: MCTSNode,
        action_priors: list[tuple[tuple[int, ...], float]],
        rollout_fn: Callable[[tuple[int, ...]], tuple[float, float, list[tuple[tuple[int, ...], float]], bool]],
    ) -> dict[tuple[int, ...], int]:
        for action_tuple, prior in action_priors:
            root.children.setdefault(action_tuple, MCTSNode(prior=prior))

        for _ in range(self.cfg.simulations):
            node = root
            path = [node]
            selected_action = None

            while node.children:
                selected_action, node = max(node.children.items(), key=lambda item: self._ucb_score(path[-1], item[1]))
                path.append(node)

            if selected_action is None:
                leaf_value = 0.0
            else:
                reward, leaf_value, next_priors, done = rollout_fn(selected_action)
                leaf_value = reward if done else reward + leaf_value
                if not done:
                    for action_tuple, prior in next_priors:
                        node.children.setdefault(action_tuple, MCTSNode(prior=prior))

            for back_node in reversed(path):
                back_node.visit_count += 1
                back_node.value_sum += leaf_value
                leaf_value = -leaf_value

        return {action: child.visit_count for action, child in root.children.items()}


def flatten_observation(obs) -> torch.Tensor:
    if isinstance(obs, dict):
        ordered = [float(v) for v in obs.values()]
        return torch.tensor(ordered, dtype=torch.float32)
    return torch.tensor(obs, dtype=torch.float32)


def action_space_layout(action_space) -> tuple[list[str], list[int]]:
    keys = list(action_space.spaces.keys())
    sizes = [int(action_space.spaces[k].n) for k in keys]
    return keys, sizes


def sample_joint_actions(policy_logits: list[torch.Tensor], max_children: int) -> list[tuple[tuple[int, ...], float]]:
    probs_per_head = [F.softmax(logits.squeeze(0), dim=-1) for logits in policy_logits]
    candidates: list[tuple[tuple[int, ...], float]] = []
    for _ in range(max_children):
        action = []
        prob = 1.0
        for head_probs in probs_per_head:
            idx = int(torch.multinomial(head_probs, 1).item())
            action.append(idx)
            prob *= float(head_probs[idx].item())
        candidates.append((tuple(action), prob))

    best = {}
    for action, prior in candidates:
        best[action] = max(prior, best.get(action, 0.0))
    return sorted(best.items(), key=lambda x: x[1], reverse=True)


def to_action_dict(action_keys: list[str], action_tuple: tuple[int, ...]) -> dict[str, int]:
    return {k: int(v) for k, v in zip(action_keys, action_tuple)}


def save_alphazero_checkpoint(path: str, net: AlphaZeroNet, optimizer: torch.optim.Optimizer, *, epoch: int, step: int) -> None:
    payload = {
        "agent_type": AgentType.ALPHAZERO.value,
        "version": 1,
        "epoch": int(epoch),
        "step": int(step),
        "observation_dim": net.observation_dim,
        "action_sizes": net.action_sizes,
        "model_state": net.state_dict(),
        "optimizer_state": optimizer.state_dict(),
    }
    torch.save(payload, path)


def load_alphazero_checkpoint(path: str, device: torch.device | str = "cpu") -> tuple[AlphaZeroNet, dict]:
    payload = torch.load(path, map_location=device)
    if payload.get("agent_type") != AgentType.ALPHAZERO.value:
        raise ValueError(
            "Неверный тип чекпойнта в model/alphazero.py (load_alphazero_checkpoint). "
            "Что делать: выберите .pth, сохранённый AlphaZero пайплайном."
        )
    net = AlphaZeroNet(payload["observation_dim"], payload["action_sizes"])
    net.load_state_dict(payload["model_state"])
    meta = {
        "version": payload.get("version", 1),
        "epoch": int(payload.get("epoch", 0)),
        "step": int(payload.get("step", 0)),
        "agent_type": payload.get("agent_type"),
        "optimizer_state": payload.get("optimizer_state"),
    }
    return net, meta


def safe_env_copy(env):
    return copy.deepcopy(env)
