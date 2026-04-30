from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import torch


@dataclass
class MCTSConfig:
    simulations: int = 64
    c_puct: float = 1.5
    dirichlet_alpha: float = 0.3
    dirichlet_eps: float = 0.25
    top_k_per_head: int = 8


def _masked_normalize(prior: np.ndarray, legal_mask: np.ndarray) -> np.ndarray:
    p = np.asarray(prior, dtype=np.float32).copy()
    m = np.asarray(legal_mask, dtype=bool)
    if p.shape != m.shape:
        return np.ones_like(p, dtype=np.float32) / float(max(1, p.size))
    p[~m] = 0.0
    s = float(p.sum())
    if s <= 1e-12:
        p = m.astype(np.float32)
        s = float(p.sum())
    return p / max(1e-12, s)


class AlphaZeroFactorizedMCTS:
    """
    Практичный factorized-search proxy для текущего env:
    - Использует priors сети по головам + legal masks.
    - Возвращает factorized policy targets (по головам) и sampled action.
    NOTE: это production-ready интерфейс, но без полного env-copy tree search;
    эволюционно сюда добавляется настоящий deep-tree rollout.
    """

    def __init__(self, policy_value_net, config: MCTSConfig | None = None, device: torch.device | None = None):
        self.net = policy_value_net
        self.cfg = config or MCTSConfig()
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @torch.no_grad()
    def run(self, *, obs: np.ndarray, legal_masks_by_head: list[np.ndarray], temperature: float = 1.0) -> tuple[list[np.ndarray], list[int], float]:
        obs_t = torch.tensor(np.asarray(obs, dtype=np.float32), device=self.device).unsqueeze(0)
        masks_t = [torch.as_tensor(m, dtype=torch.bool, device=self.device).unsqueeze(0) for m in legal_masks_by_head]
        priors_t, value_t = self.net.infer(obs_t, masks_by_head=masks_t)
        value = float(value_t.item())

        policy_targets: list[np.ndarray] = []
        selected_actions: list[int] = []
        temp = max(1e-6, float(temperature))
        for head_idx, prior_t in enumerate(priors_t):
            prior = prior_t.squeeze(0).detach().cpu().numpy().astype(np.float32)
            legal = np.asarray(legal_masks_by_head[head_idx], dtype=bool)
            pi = _masked_normalize(prior, legal)
            # Dirichlet noise at root (AZ-style)
            legal_count = int(np.sum(legal))
            if legal_count > 1 and self.cfg.dirichlet_eps > 0:
                alpha = float(self.cfg.dirichlet_alpha)
                noise = np.random.dirichlet([alpha] * legal_count).astype(np.float32)
                noisy = np.zeros_like(pi, dtype=np.float32)
                noisy[np.where(legal)[0]] = noise
                pi = (1.0 - float(self.cfg.dirichlet_eps)) * pi + float(self.cfg.dirichlet_eps) * noisy
                pi = _masked_normalize(pi, legal)

            logits = np.log(np.clip(pi, 1e-12, 1.0)) / temp
            ptemp = np.exp(logits - np.max(logits))
            ptemp = _masked_normalize(ptemp, legal)
            action = int(np.random.choice(np.arange(ptemp.size), p=ptemp))
            policy_targets.append(ptemp.astype(np.float32))
            selected_actions.append(action)
        return policy_targets, selected_actions, value
