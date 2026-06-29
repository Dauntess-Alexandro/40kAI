"""PHOENIX network: masked action-embed, latent dynamics, encoder+IQN reuse из DQN, BYOL-головы."""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


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


class PhoenixDynamics(nn.Module):
    """Латентная transition-модель: ẑ' = h(ẑ, g(a)). MLP (детерминированный) или GRUCell."""

    def __init__(self, hidden_size: int, emb_dim: int, dynamics_type: str = "mlp"):
        super().__init__()
        self.hidden_size = int(hidden_size)
        self.emb_dim = int(emb_dim)
        self.dynamics_type = str(dynamics_type).strip().lower() or "mlp"
        if self.dynamics_type == "gru":
            self.cell = nn.GRUCell(self.emb_dim, self.hidden_size)
        else:
            self.fc1 = nn.Linear(self.hidden_size + self.emb_dim, self.hidden_size)
            self.norm = nn.LayerNorm(self.hidden_size)
            self.fc2 = nn.Linear(self.hidden_size, self.hidden_size)

    def step(self, z: torch.Tensor, a_emb: torch.Tensor) -> torch.Tensor:
        if self.dynamics_type == "gru":
            return self.cell(a_emb, z)
        x = torch.cat([z, a_emb], dim=1)
        x = F.relu(self.norm(self.fc1(x)))
        return self.fc2(x)

    def rollout(self, z0: torch.Tensor, a_emb_seq: torch.Tensor) -> torch.Tensor:
        # a_emb_seq: [B, K, emb] → выход [B, K, hidden] (ẑ_1..ẑ_K)
        steps = []
        z = z0
        for k in range(a_emb_seq.shape[1]):
            z = self.step(z, a_emb_seq[:, k])
            steps.append(z)
        return torch.stack(steps, dim=1)
