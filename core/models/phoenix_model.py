"""PHOENIX network: masked action-embed, latent dynamics, encoder+IQN reuse из DQN, BYOL-головы."""
from __future__ import annotations

import copy
import re

import torch
import torch.nn as nn
import torch.nn.functional as F

from core.models.DQN import DQN


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


# --- BYOL projection / prediction heads ---


class _Projector(nn.Module):
    def __init__(self, hidden_size: int, proj_dim: int):
        super().__init__()
        self.fc1 = nn.Linear(hidden_size, proj_dim)
        self.norm = nn.LayerNorm(proj_dim)
        self.fc2 = nn.Linear(proj_dim, proj_dim)

    def forward(self, x):
        return self.fc2(F.relu(self.norm(self.fc1(x))))


class _Predictor(nn.Module):
    def __init__(self, proj_dim: int):
        super().__init__()
        self.fc = nn.Linear(proj_dim, proj_dim)

    def forward(self, x):
        return self.fc(x)


# --- PhoenixNet: encoder+IQN reuse из DQN, BYOL-головы, EMA-таргет ---


class PhoenixNet(nn.Module):
    def __init__(self, n_observations: int, action_sizes: list[int], cfg):
        super().__init__()
        self.action_sizes = list(action_sizes)
        self.hidden_size = int(cfg.hidden_size)
        self.num_layers = int(cfg.num_layers)
        self.emb_dim = int(cfg.emb_dim)
        proj_dim = self.hidden_size

        dqn_kwargs = dict(
            dueling=bool(cfg.dueling),
            noisy=bool(cfg.noisy),
            distributional="iqn",
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
            n_ensemble=int(cfg.n_ensemble),
            iqn_num_quantiles=int(cfg.iqn_num_quantiles),
            iqn_num_target_quantiles=int(cfg.iqn_num_target_quantiles),
            iqn_num_tau_samples=int(cfg.iqn_num_tau_samples),
            iqn_embed_dim=int(cfg.iqn_embed_dim),
        )
        self.online = DQN(n_observations, self.action_sizes, **dqn_kwargs)
        self.target = copy.deepcopy(self.online)
        for p in self.target.parameters():
            p.requires_grad_(False)

        self.action_embed = PhoenixActionEmbed(self.action_sizes, self.emb_dim)
        self.dynamics = PhoenixDynamics(self.hidden_size, self.emb_dim, cfg.dynamics_type)
        self.projector = _Projector(self.hidden_size, proj_dim)
        self.predictor = _Predictor(proj_dim)
        self.target_projector = copy.deepcopy(self.projector)
        for p in self.target_projector.parameters():
            p.requires_grad_(False)

    # --- encoder / RL ---
    def encode(self, obs):
        return self.online._feature(obs)

    def iqn_q(self, obs):
        return self.online.q_values(obs)

    def target_quantiles(self, obs, num_quantiles=None, taus=None, return_taus=False):
        return self.target.iqn(obs, num_quantiles=num_quantiles, taus=taus, return_taus=return_taus)

    def online_quantiles(self, obs, num_quantiles=None, taus=None, return_taus=False):
        return self.online.iqn(obs, num_quantiles=num_quantiles, taus=taus, return_taus=return_taus)

    def target_quantiles_from_latent(self, z, num_quantiles=None, taus=None, return_taus=False):
        batch_size = z.shape[0]
        n_q = int(num_quantiles or self.target.iqn_num_target_quantiles)
        if taus is None:
            taus = self.target._sample_taus(batch_size, n_q, z.device)
        iqn_feat = self.target._iqn_features(z, taus).reshape(batch_size * n_q, self.hidden_size)
        all_outputs = []
        for bundle in self.target.head_bundles:
            all_outputs.append(bundle.iqn_from_features(iqn_feat, batch_size, n_q, self.action_sizes))
        if self.target.n_ensemble == 1:
            outputs = all_outputs[0]
        else:
            outputs = []
            num_heads = len(all_outputs[0])
            for h in range(num_heads):
                stacked = torch.stack([all_outputs[e][h] for e in range(self.target.n_ensemble)], dim=0)
                outputs.append(stacked.mean(dim=0))
        if return_taus:
            return outputs, taus
        return outputs

    # --- SPR heads ---
    def project(self, z):
        return self.projector(z)

    def predict(self, p):
        return self.predictor(p)

    @torch.no_grad()
    def target_encode(self, obs):
        return self.target._feature(obs)

    @torch.no_grad()
    def target_project(self, z):
        return self.target_projector(z)

    # --- maintenance ---
    def _encoder_parameters(self):
        yield from self.online.input_fc.parameters()
        yield from self.online.input_norm.parameters()
        yield from self.online.blocks.parameters()

    def update_targets(self, ema_rl: float, ema_spr: float):
        with torch.no_grad():
            for po, pt in zip(self.online.parameters(), self.target.parameters()):
                pt.mul_(1.0 - ema_rl).add_(po, alpha=ema_rl)
            for po, pt in zip(self.projector.parameters(), self.target_projector.parameters()):
                pt.mul_(1.0 - ema_spr).add_(po, alpha=ema_spr)

    def reset_heads_and_shrink_encoder(self, alpha: float):
        with torch.no_grad():
            # 1) shrink-and-perturb ствола encoder
            for p in self._encoder_parameters():
                phi = torch.empty_like(p)
                if p.dim() >= 2:
                    nn.init.kaiming_uniform_(phi, a=5**0.5)
                else:
                    phi.normal_(0.0, 0.01)
                p.mul_(alpha).add_(phi, alpha=1.0 - alpha)
        # 2) полный reset голов и обвязки
        for module in (self.online.head_bundles, self.projector, self.predictor,
                       self.dynamics, self.action_embed):
            for sub in module.modules():
                if hasattr(sub, "reset_parameters"):
                    sub.reset_parameters()
        # 3) ресинк таргетов
        self.target.load_state_dict(self.online.state_dict())
        self.target_projector.load_state_dict(self.projector.state_dict())


def infer_phoenix_arch_from_state_dict(state_dict) -> dict:
    """Восстановить арх-параметры PhoenixNet из state_dict (для загрузки чужого чекпойнта)."""
    keys = list(state_dict.keys())
    hidden_size = None
    for k in keys:
        if k.endswith("online.input_fc.weight") or k.endswith("online.input_fc.weight_mu"):
            hidden_size = int(state_dict[k].shape[0])
            break
    num_layers = len({int(m.group(1)) for k in keys for m in [re.search(r"online\.blocks\.(\d+)\.", k)] if m})
    emb_dim = None
    for k in keys:
        if re.search(r"action_embed\.embeddings\.\d+\.weight$", k):
            emb_dim = int(state_dict[k].shape[1])
            break
    arch = {"num_layers": max(1, num_layers)}
    if hidden_size:
        arch["hidden_size"] = hidden_size
    if emb_dim:
        arch["emb_dim"] = emb_dim
    return arch
