from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------

GMZ_PRESETS: dict[str, dict] = {
    "fast": {
        "latent_dim": 128,
        "hidden_dim": 128,
        "num_layers": 1,
        "action_embed_dim": 32,
    },
    "balanced": {
        "latent_dim": 256,
        "hidden_dim": 256,
        "num_layers": 2,
        "action_embed_dim": 64,
    },
    "heavy": {
        "latent_dim": 512,
        "hidden_dim": 512,
        "num_layers": 3,
        "action_embed_dim": 128,
    },
}


# ---------------------------------------------------------------------------
# Factory helpers
# ---------------------------------------------------------------------------

def gumbel_muzero_kwargs_from_env() -> dict:
    preset_name = os.getenv("GMZ_PRESET", "balanced").lower()
    preset = GMZ_PRESETS.get(preset_name, GMZ_PRESETS["balanced"]).copy()
    overrides = {
        "latent_dim": int(os.getenv("GMZ_LATENT_DIM", str(preset["latent_dim"]))),
        "hidden_dim": int(os.getenv("GMZ_HIDDEN_DIM", str(preset["hidden_dim"]))),
        "num_layers": int(os.getenv("GMZ_NUM_LAYERS", str(preset["num_layers"]))),
        "action_embed_dim": int(os.getenv("GMZ_ACTION_EMBED_DIM", str(preset["action_embed_dim"]))),
    }
    return overrides


def gumbel_muzero_arch_from_payload(payload: dict | None) -> dict:
    if isinstance(payload, dict):
        arch = payload.get("arch")
        if isinstance(arch, dict):
            out = gumbel_muzero_kwargs_from_env()
            for key in ("latent_dim", "hidden_dim", "num_layers", "action_embed_dim"):
                if key in arch:
                    out[key] = int(arch[key])
            return out
    return gumbel_muzero_kwargs_from_env()


def make_gumbel_muzero_net(obs_dim: int, action_sizes: list[int], **overrides):
    kwargs = gumbel_muzero_kwargs_from_env()
    kwargs.update(overrides)
    return GumbelMuZeroNet(obs_dim, action_sizes, **kwargs)


def make_gumbel_muzero_net_preset(obs_dim: int, action_sizes: list[int], preset: str = "balanced", **overrides):
    kwargs = GMZ_PRESETS.get(preset, GMZ_PRESETS["balanced"]).copy()
    kwargs.update(overrides)
    return GumbelMuZeroNet(obs_dim, action_sizes, **kwargs)


def load_gumbel_muzero_state_dict(net: "GumbelMuZeroNet", state_dict: dict, *, log_fn=None) -> tuple:
    state = dict(state_dict)
    legacy = any(str(k).startswith("representation.0.") for k in state) and not any(
        str(k).startswith("repr_input_fc.") for k in state
    )
    if legacy and log_fn is not None:
        log_fn(
            "[GMZ][WARN] Чекпойнт со старой архитектурой (простой MLP). "
            "Нужно переобучить модель — миграция весов не поддерживается."
        )
    missing, unexpected = net.load_state_dict(state, strict=False)
    if log_fn is not None and (missing or unexpected):
        log_fn(
            f"[GMZ][WARN] load_state_dict: missing={len(missing)} unexpected={len(unexpected)} "
            f"(первые missing: {list(missing)[:3]})"
        )
    return missing, unexpected


# ---------------------------------------------------------------------------
# Building blocks
# ---------------------------------------------------------------------------

def _normalize_latent(latent: torch.Tensor, eps: float = 1e-6) -> torch.Tensor:
    mean = latent.mean(dim=1, keepdim=True)
    std = latent.std(dim=1, keepdim=True).clamp_min(eps)
    return (latent - mean) / std


class ResidualBlock(nn.Module):
    """Pre-norm residual MLP block — mirrors AlphaZero trunk."""

    def __init__(self, hidden_dim: int):
        super().__init__()
        self.norm1 = nn.LayerNorm(hidden_dim)
        self.fc1 = nn.Linear(hidden_dim, hidden_dim)
        self.norm2 = nn.LayerNorm(hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = x
        x = F.silu(self.norm1(self.fc1(x)))
        x = self.norm2(self.fc2(x))
        return F.silu(x + residual)


# ---------------------------------------------------------------------------
# Config dataclass
# ---------------------------------------------------------------------------

@dataclass
class GumbelMuZeroModelConfig:
    obs_dim: int
    action_sizes: list[int]
    latent_dim: int = 256
    hidden_dim: int = 256
    num_layers: int = 2
    action_embed_dim: int = 64


# ---------------------------------------------------------------------------
# Main network
# ---------------------------------------------------------------------------

class GumbelMuZeroNet(nn.Module):
    """
    Factorized Gumbel MuZero network with residual trunk:
    - representation: obs -> latent  (LayerNorm + ResidualBlocks)
    - dynamics: (latent, action) -> next_latent + reward  (skip connection + MLP reward head)
    - prediction: latent -> policy heads + value  (ResidualBlock trunk)
    """

    def __init__(
        self,
        obs_dim: int,
        action_sizes: list[int],
        latent_dim: int = 256,
        hidden_dim: int = 256,
        num_layers: int = 2,
        action_embed_dim: int = 64,
    ):
        super().__init__()
        self.obs_dim = int(obs_dim)
        self.action_sizes = [int(x) for x in action_sizes]
        self.latent_dim = int(latent_dim)
        self.hidden_dim = int(hidden_dim)
        self.num_layers = max(1, int(num_layers))
        self.action_embed_dim = int(action_embed_dim)
        self.num_heads = len(self.action_sizes)

        # --- Representation: obs -> hidden -> ... -> latent ---
        self.repr_input_fc = nn.Linear(self.obs_dim, self.hidden_dim)
        self.repr_input_norm = nn.LayerNorm(self.hidden_dim)
        self.repr_blocks = nn.ModuleList(
            [ResidualBlock(self.hidden_dim) for _ in range(self.num_layers)]
        )
        self.repr_output_fc = nn.Linear(self.hidden_dim, self.latent_dim)

        # --- Action embeddings ---
        self.action_embeddings = nn.ModuleList(
            [nn.Embedding(int(size), self.action_embed_dim) for size in self.action_sizes]
        )

        # --- Dynamics: (latent + action_emb) -> next_latent + reward ---
        dyn_in = self.latent_dim + self.action_embed_dim * self.num_heads
        self.dyn_input_norm = nn.LayerNorm(dyn_in)
        self.dyn_fc1 = nn.Linear(dyn_in, self.hidden_dim)
        self.dyn_norm1 = nn.LayerNorm(self.hidden_dim)
        self.dyn_fc2 = nn.Linear(self.hidden_dim, self.hidden_dim)
        self.dyn_norm2 = nn.LayerNorm(self.hidden_dim)
        self.dyn_skip = nn.Linear(dyn_in, self.hidden_dim)
        self.next_latent_head = nn.Linear(self.hidden_dim, self.latent_dim)
        self.reward_head = nn.Sequential(
            nn.Linear(self.hidden_dim, self.hidden_dim // 2),
            nn.LayerNorm(self.hidden_dim // 2),
            nn.SiLU(),
            nn.Linear(self.hidden_dim // 2, 1),
        )

        # --- Prediction: latent -> policy + value ---
        self.pred_input_fc = nn.Linear(self.latent_dim, self.hidden_dim)
        self.pred_input_norm = nn.LayerNorm(self.hidden_dim)
        self.pred_blocks = nn.ModuleList(
            [ResidualBlock(self.hidden_dim) for _ in range(max(1, self.num_layers - 1))]
        )
        self.policy_heads = nn.ModuleList(
            [nn.Linear(self.hidden_dim, int(size)) for size in self.action_sizes]
        )
        self.value_head = nn.Sequential(
            nn.Linear(self.hidden_dim, self.hidden_dim // 2),
            nn.SiLU(),
            nn.Linear(self.hidden_dim // 2, 1),
        )

        # --- Consistency projection (SimSiam-style) ---
        proj_dim = max(64, self.latent_dim // 2)
        self.consistency_projector = nn.Sequential(
            nn.Linear(self.latent_dim, proj_dim),
            nn.LayerNorm(proj_dim),
            nn.SiLU(),
            nn.Linear(proj_dim, proj_dim),
        )

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def project_latent(self, latent: torch.Tensor) -> torch.Tensor:
        """L2-normalised projection for SimSiam consistency loss."""
        z = self.consistency_projector(latent)
        return F.normalize(z, dim=1)

    def encode(self, obs: torch.Tensor) -> torch.Tensor:
        h = F.silu(self.repr_input_norm(self.repr_input_fc(obs)))
        for block in self.repr_blocks:
            h = block(h)
        latent = self.repr_output_fc(h)
        return _normalize_latent(latent)

    def _embed_actions(self, actions: torch.Tensor) -> torch.Tensor:
        embeds = []
        for idx, emb in enumerate(self.action_embeddings):
            head_actions = actions[:, idx].long().clamp(min=0, max=self.action_sizes[idx] - 1)
            embeds.append(emb(head_actions))
        return torch.cat(embeds, dim=1)

    def dynamics(self, latent: torch.Tensor, actions: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        action_emb = self._embed_actions(actions)
        x = torch.cat([latent, action_emb], dim=1)
        x = self.dyn_input_norm(x)
        h = F.silu(self.dyn_norm1(self.dyn_fc1(x)))
        h = self.dyn_norm2(self.dyn_fc2(h))
        skip = F.silu(self.dyn_skip(x))
        h = F.silu(h + skip)
        next_latent = _normalize_latent(self.next_latent_head(h))
        reward = self.reward_head(h).squeeze(1)
        return next_latent, reward

    def predict(self, latent: torch.Tensor, masks_by_head: Optional[list[torch.Tensor]] = None):
        h = F.silu(self.pred_input_norm(self.pred_input_fc(latent)))
        for block in self.pred_blocks:
            h = block(h)
        logits = [head(h) for head in self.policy_heads]
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
        value = torch.tanh(self.value_head(h).squeeze(1))
        return logits, value

    # ------------------------------------------------------------------
    # Public inference API
    # ------------------------------------------------------------------

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
