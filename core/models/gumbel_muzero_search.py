from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import torch
import torch.nn.functional as F


@dataclass
class GumbelMuZeroSearchConfig:
    num_simulations: int = 96
    root_top_k: int = 16
    discount: float = 0.997
    temperature: float = 0.15
    gumbel_scale: float = 1.0


def _masked_softmax(logits: np.ndarray, legal_mask: np.ndarray, temperature: float) -> np.ndarray:
    x = np.asarray(logits, dtype=np.float32).copy()
    m = np.asarray(legal_mask, dtype=bool)
    if x.shape != m.shape:
        return np.ones_like(x, dtype=np.float32) / float(max(1, x.size))
    x[~m] = -1e9
    x = x / max(1e-6, float(temperature))
    x = x - np.max(x)
    p = np.exp(x)
    p[~m] = 0.0
    s = float(p.sum())
    if s <= 1e-12:
        p = m.astype(np.float32)
        s = float(p.sum())
    return p / max(1e-12, s)


class GumbelMuZeroSearch:
    """
    Practical factorized root-search with Gumbel policy improvement.
    """

    def __init__(self, net, config: Optional[GumbelMuZeroSearchConfig] = None, device: Optional[torch.device] = None):
        self.net = net
        self.cfg = config or GumbelMuZeroSearchConfig()
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.last_run_stats: dict[str, float] = {}

    @torch.no_grad()
    def run(
        self,
        *,
        obs: np.ndarray,
        legal_masks_by_head: list[np.ndarray],
        deterministic: bool = True,
    ) -> tuple[list[np.ndarray], list[int], float]:
        obs_t = torch.tensor(np.asarray(obs, dtype=np.float32), device=self.device).unsqueeze(0)
        masks_t = [torch.as_tensor(m, dtype=torch.bool, device=self.device).unsqueeze(0) for m in legal_masks_by_head]
        root_logits, root_value, _root_reward, latent = self.net.initial_inference(obs_t, masks_by_head=masks_t)
        base_action = [int(torch.argmax(head.squeeze(0), dim=0).item()) for head in root_logits]

        sims = max(1, int(self.cfg.num_simulations))
        root_top_k = max(1, int(self.cfg.root_top_k))
        discount = float(self.cfg.discount)
        temp = float(self.cfg.temperature)
        gumbel_scale = float(self.cfg.gumbel_scale)

        policy_targets: list[np.ndarray] = []
        selected_actions: list[int] = []
        value_samples: list[float] = []

        for head_idx, head_logits in enumerate(root_logits):
            logits_np = head_logits.squeeze(0).detach().cpu().numpy().astype(np.float32)
            legal = np.asarray(legal_masks_by_head[head_idx], dtype=bool)
            legal_idx = np.where(legal)[0]
            if legal_idx.size == 0:
                policy_targets.append(np.ones_like(logits_np, dtype=np.float32) / float(max(1, logits_np.size)))
                selected_actions.append(0)
                continue

            local_logits = logits_np[legal_idx]
            gumbel = np.random.gumbel(loc=0.0, scale=max(1e-6, gumbel_scale), size=legal_idx.size).astype(np.float32)
            ranking = np.argsort(local_logits + gumbel)[::-1]
            top_local = ranking[: min(root_top_k, ranking.size)]
            candidate_actions = legal_idx[top_local]
            if candidate_actions.size == 0:
                candidate_actions = legal_idx

            visits = np.zeros_like(logits_np, dtype=np.float32)
            q_values = np.zeros_like(logits_np, dtype=np.float32)
            per_action_counts = np.zeros_like(logits_np, dtype=np.float32)

            for sim in range(sims):
                candidate = int(candidate_actions[sim % candidate_actions.size])
                action_vec = list(base_action)
                action_vec[head_idx] = candidate
                action_t = torch.tensor([action_vec], dtype=torch.long, device=self.device)
                _p, val_next, rew_next, _next_latent = self.net.recurrent_inference(latent, action_t, masks_by_head=masks_t)
                q = float(rew_next.item() + discount * float(val_next.item()))
                visits[candidate] += 1.0
                per_action_counts[candidate] += 1.0
                q_values[candidate] += q
                value_samples.append(q)

            for idx in legal_idx.tolist():
                if per_action_counts[idx] > 0:
                    q_values[idx] /= per_action_counts[idx]
                else:
                    q_values[idx] = float(logits_np[idx])

            mixed_logits = q_values.copy()
            mixed_logits[~legal] = -1e9
            pi = _masked_softmax(mixed_logits, legal_mask=legal, temperature=temp)
            if deterministic:
                action = int(np.argmax(pi))
            else:
                action = int(np.random.choice(np.arange(pi.size), p=pi))
            policy_targets.append(pi.astype(np.float32))
            selected_actions.append(action)

        self.last_run_stats = {
            "mode": 1.0,
            "simulations": float(sims),
            "root_value": float(root_value.item()),
            "q_mean": float(np.mean(value_samples) if value_samples else float(root_value.item())),
        }
        value_out = float(np.mean(value_samples) if value_samples else float(root_value.item()))
        return policy_targets, selected_actions, value_out
