"""PHOENIX network: masked action-embed, latent dynamics, encoder+IQN reuse из DQN, BYOL-головы."""
from __future__ import annotations

import torch
import torch.nn as nn


class PhoenixActionEmbed(nn.Module):
    """Эмбеддинг факторизованного действия: на каждую голову своя Embedding,
    вклад неактивных голов зануляется маской, суммируем по головам."""

    def __init__(self, action_sizes: list[int], emb_dim: int):
        super().__init__()
        self.action_sizes = list(action_sizes)
        self.emb_dim = int(emb_dim)
        self.embeddings = nn.ModuleList(
            [nn.Embedding(int(max(1, size)), self.emb_dim) for size in self.action_sizes]
        )

    def forward(self, actions: torch.Tensor, active_mask: torch.Tensor) -> torch.Tensor:
        # actions: [B, H] long; active_mask: [B, H] bool
        batch = actions.shape[0]
        out = torch.zeros(batch, self.emb_dim, device=actions.device)
        for h, embed in enumerate(self.embeddings):
            idx = actions[:, h].clamp(min=0, max=embed.num_embeddings - 1)
            vec = embed(idx)  # [B, emb_dim]
            gate = active_mask[:, h].to(vec.dtype).unsqueeze(1)  # [B, 1]
            out = out + vec * gate
        return out
