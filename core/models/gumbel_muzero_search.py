from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import torch


# ---------------------------------------------------------------------------
# Search preset configs
# ---------------------------------------------------------------------------

@dataclass
class GumbelMuZeroSearchConfig:
    num_simulations: int = 32
    root_top_k: int = 8
    discount: float = 0.997
    temperature: float = 0.15
    gumbel_scale: float = 1.0
    prior_weight: float = 0.25


SEARCH_PRESETS: dict[str, dict] = {
    "fast": {
        "num_simulations": 16,
        "root_top_k": 4,
        "temperature": 0.2,
        "gumbel_scale": 1.0,
        "prior_weight": 0.3,
    },
    "balanced": {
        "num_simulations": 32,
        "root_top_k": 8,
        "temperature": 0.15,
        "gumbel_scale": 1.0,
        "prior_weight": 0.25,
    },
    "heavy": {
        "num_simulations": 64,
        "root_top_k": 12,
        "temperature": 0.1,
        "gumbel_scale": 0.8,
        "prior_weight": 0.2,
    },
}


def make_search_config(preset: str = "balanced", **overrides) -> GumbelMuZeroSearchConfig:
    kwargs = SEARCH_PRESETS.get(preset, SEARCH_PRESETS["balanced"]).copy()
    kwargs.update(overrides)
    return GumbelMuZeroSearchConfig(**kwargs)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _masked_softmax(logits: np.ndarray, legal_mask: np.ndarray, temperature: float) -> np.ndarray:
    x = np.asarray(logits, dtype=np.float32).copy()
    m = np.asarray(legal_mask, dtype=bool)
    if x.shape != m.shape:
        return np.ones_like(x, dtype=np.float32) / float(max(1, x.size))
    x[~m] = -1e9
    x = x / max(1e-6, float(temperature))
    x = x - np.max(x[m])
    p = np.exp(x)
    p[~m] = 0.0
    s = float(p.sum())
    if s <= 1e-12:
        p = m.astype(np.float32)
        s = float(p.sum())
    return p / max(1e-12, s)


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

class GumbelMuZeroSearch:
    """
    Factorized root-search with proper Gumbel-UCB and prior mixing.

    Each head independently:
    1. Samples top-k candidates via Gumbel trick on policy prior
    2. Evaluates each candidate via recurrent_inference (reward + value)
    3. Builds Q-values with UCB exploration bonus
    4. Mixes Q-values with prior: π = (1-α)*softmax(Q/T) + α*prior
    5. Selects action deterministically or stochastically
    """

    def __init__(
        self,
        net,
        config: Optional[GumbelMuZeroSearchConfig] = None,
        device: Optional[torch.device] = None,
    ):
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
        masks_t = [
            torch.as_tensor(m, dtype=torch.bool, device=self.device).unsqueeze(0)
            for m in legal_masks_by_head
        ]
        root_logits, root_value, _root_reward, latent = self.net.initial_inference(
            obs_t, masks_by_head=masks_t
        )

        sims = max(1, int(self.cfg.num_simulations))
        root_top_k = max(1, int(self.cfg.root_top_k))
        discount = float(self.cfg.discount)
        temp = float(self.cfg.temperature)
        gumbel_scale = float(self.cfg.gumbel_scale)
        prior_weight = float(self.cfg.prior_weight)

        # Greedy base action (fallback when no legal actions)
        base_action = [int(torch.argmax(head.squeeze(0), dim=0).item()) for head in root_logits]

        policy_targets: list[np.ndarray] = []
        selected_actions: list[int] = []
        value_samples: list[float] = []

        for head_idx, head_logits in enumerate(root_logits):
            logits_np = head_logits.squeeze(0).detach().cpu().numpy().astype(np.float32)
            legal = np.asarray(legal_masks_by_head[head_idx], dtype=bool)
            legal_idx = np.where(legal)[0]

            if legal_idx.size == 0:
                policy_targets.append(
                    np.ones_like(logits_np, dtype=np.float32) / float(max(1, logits_np.size))
                )
                selected_actions.append(0)
                continue

            # Prior probabilities from root policy
            prior_np = np.full_like(logits_np, -1e9)
            prior_np[legal_idx] = logits_np[legal_idx]
            prior_np -= prior_np[legal_idx].max()
            prior_exp = np.exp(prior_np)
            prior_exp[~legal] = 0.0
            prior_sum = prior_exp.sum()
            prior_probs = prior_exp / max(prior_sum, 1e-12)

            # Top-k selection via Gumbel trick on legal actions
            local_logits = logits_np[legal_idx]
            gumbel = np.random.gumbel(
                loc=0.0, scale=max(1e-6, gumbel_scale), size=legal_idx.size
            ).astype(np.float32)
            ranking = np.argsort(local_logits + gumbel)[::-1]
            top_local = ranking[: min(root_top_k, ranking.size)]
            candidate_actions = legal_idx[top_local]

            # Per-action statistics
            visits = np.zeros(logits_np.size, dtype=np.float32)
            q_sums = np.zeros(logits_np.size, dtype=np.float32)

            for sim in range(sims):
                # Cycle through candidates; each gets ~equal budget
                candidate = int(candidate_actions[sim % candidate_actions.size])
                action_vec = list(base_action)
                action_vec[head_idx] = candidate
                action_t = torch.tensor([action_vec], dtype=torch.long, device=self.device)

                _p, val_next, rew_next, _nl = self.net.recurrent_inference(
                    latent, action_t, masks_by_head=masks_t
                )
                q = float(rew_next.item()) + discount * float(val_next.item())

                visits[candidate] += 1.0
                q_sums[candidate] += q
                value_samples.append(q)

            # Mean Q-values for visited actions; fallback to logit for unvisited
            q_values = np.where(visits > 0, q_sums / np.maximum(visits, 1.0), logits_np)
            q_values[~legal] = -1e9

            # UCB bonus on Q-values (sqrt exploration)
            total_visits = visits.sum() + 1.0
            ucb_bonus = np.sqrt(np.log(total_visits + 1.0) / (visits + 1.0))
            ucb_q = np.where(legal, q_values + 0.3 * ucb_bonus, -1e9)

            # Softmax over Q-values
            q_soft = _masked_softmax(ucb_q, legal_mask=legal, temperature=temp)

            # Prior mixing: π = (1-α)*softmax(Q/T) + α*prior
            mixed = (1.0 - prior_weight) * q_soft + prior_weight * prior_probs
            mixed[~legal] = 0.0
            mixed_sum = mixed.sum()
            if mixed_sum > 1e-12:
                mixed /= mixed_sum
            else:
                mixed = legal.astype(np.float32) / float(legal.sum())

            if deterministic:
                action = int(np.argmax(mixed))
            else:
                action = int(np.random.choice(np.arange(mixed.size), p=mixed))

            policy_targets.append(mixed.astype(np.float32))
            selected_actions.append(action)

        self.last_run_stats = {
            "mode": 1.0,
            "simulations": float(sims),
            "root_value": float(root_value.item()),
            "q_mean": float(np.mean(value_samples) if value_samples else float(root_value.item())),
        }
        value_out = float(
            np.mean(value_samples) if value_samples else float(root_value.item())
        )
        return policy_targets, selected_actions, value_out
