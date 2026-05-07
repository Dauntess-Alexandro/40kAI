from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


def _normalize_latent(latent: torch.Tensor, eps: float = 1e-6) -> torch.Tensor:
    mean = latent.mean(dim=1, keepdim=True)
    std = latent.std(dim=1, keepdim=True).clamp_min(eps)
    return (latent - mean) / std


@dataclass
class GumbelMuZeroModelConfig:
    obs_dim: int
    action_sizes: list[int]
    latent_dim: int = 256
    hidden_dim: int = 256
    action_embed_dim: int = 64


class GumbelMuZeroNet(nn.Module):
    """
    Factorized Gumbel MuZero network:
    - representation: obs -> latent
    - dynamics: (latent, action) -> next_latent + reward
    - prediction: latent -> policy heads + value
    """

    def __init__(
        self,
        obs_dim: int,
        action_sizes: list[int],
        latent_dim: int = 256,
        hidden_dim: int = 256,
        action_embed_dim: int = 64,
    ):
        super().__init__()
        self.obs_dim = int(obs_dim)
        self.action_sizes = [int(x) for x in action_sizes]
        self.latent_dim = int(latent_dim)
        self.hidden_dim = int(hidden_dim)
        self.action_embed_dim = int(action_embed_dim)
        self.num_heads = len(self.action_sizes)

        self.representation = nn.Sequential(
            nn.Linear(self.obs_dim, self.hidden_dim),
            nn.ReLU(),
            nn.Linear(self.hidden_dim, self.latent_dim),
            nn.ReLU(),
        )

        self.action_embeddings = nn.ModuleList(
            [nn.Embedding(int(size), self.action_embed_dim) for size in self.action_sizes]
        )

        dyn_in = self.latent_dim + self.action_embed_dim * self.num_heads
        self.dynamics_torso = nn.Sequential(
            nn.Linear(dyn_in, self.hidden_dim),
            nn.ReLU(),
            nn.Linear(self.hidden_dim, self.hidden_dim),
            nn.ReLU(),
        )
        self.next_latent_head = nn.Linear(self.hidden_dim, self.latent_dim)
        self.reward_head = nn.Linear(self.hidden_dim, 1)

        self.prediction_torso = nn.Sequential(
            nn.Linear(self.latent_dim, self.hidden_dim),
            nn.ReLU(),
        )
        self.policy_heads = nn.ModuleList([nn.Linear(self.hidden_dim, int(size)) for size in self.action_sizes])
        self.value_head = nn.Linear(self.hidden_dim, 1)

    def encode(self, obs: torch.Tensor) -> torch.Tensor:
        latent = self.representation(obs)
        return _normalize_latent(latent)

    def _embed_actions(self, actions: torch.Tensor) -> torch.Tensor:
        embeds = []
        for idx, emb in enumerate(self.action_embeddings):
            head_actions = actions[:, idx].long().clamp(min=0, max=self.action_sizes[idx] - 1)
            embeds.append(emb(head_actions))
        return torch.cat(embeds, dim=1)

    def dynamics(self, latent: torch.Tensor, actions: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        action_emb = self._embed_actions(actions)
        h = self.dynamics_torso(torch.cat([latent, action_emb], dim=1))
        next_latent = _normalize_latent(self.next_latent_head(h))
        reward = self.reward_head(h).squeeze(1)
        return next_latent, reward

    def predict(self, latent: torch.Tensor, masks_by_head: Optional[list[torch.Tensor]] = None):
        trunk = self.prediction_torso(latent)
        logits = [head(trunk) for head in self.policy_heads]
        if masks_by_head:
            masked_logits: list[torch.Tensor] = []
            for i, head_logits in enumerate(logits):
                if i < len(masks_by_head) and masks_by_head[i] is not None:
                    mask = masks_by_head[i].to(dtype=torch.bool, device=head_logits.device)
                    if mask.shape == head_logits.shape and bool(mask.any()):
                        tmp = head_logits.clone()
                        tmp[~mask] = -1e9
                        masked_logits.append(tmp)
                        continue
                masked_logits.append(head_logits)
            logits = masked_logits
        value = torch.tanh(self.value_head(trunk).squeeze(1))
        return logits, value

    def initial_inference(self, obs: torch.Tensor, masks_by_head: Optional[list[torch.Tensor]] = None):
        latent = self.encode(obs)
        policy_logits, value = self.predict(latent, masks_by_head=masks_by_head)
        reward = torch.zeros_like(value)
        return policy_logits, value, reward, latent

    def recurrent_inference(
        self,
        latent: torch.Tensor,
        actions: torch.Tensor,
        masks_by_head: Optional[list[torch.Tensor]] = None,
    ):
        next_latent, reward = self.dynamics(latent, actions)
        policy_logits, value = self.predict(next_latent, masks_by_head=masks_by_head)
        return policy_logits, value, reward, next_latent

    @torch.no_grad()
    def infer(self, obs: torch.Tensor, masks_by_head: Optional[list[torch.Tensor]] = None):
        logits, value, _reward, _latent = self.initial_inference(obs, masks_by_head=masks_by_head)
        probs = [F.softmax(x, dim=1) for x in logits]
        return probs, value

    def forward(self, obs: torch.Tensor, masks_by_head: Optional[list[torch.Tensor]] = None):
        logits, value, _reward, _latent = self.initial_inference(obs, masks_by_head=masks_by_head)
        return logits, value
