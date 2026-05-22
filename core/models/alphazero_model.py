from __future__ import annotations

import os

import torch
import torch.nn as nn
import torch.nn.functional as F


def alphazero_kwargs_from_env() -> dict:
    """Shared AlphaZero constructor kwargs from environment variables."""
    return {
        "hidden_size": int(os.getenv("AZ_HIDDEN_SIZE", "256")),
        "num_layers": int(os.getenv("AZ_NUM_LAYERS", "2")),
        "n_value_ensemble": int(os.getenv("AZ_VALUE_ENSEMBLE", "1")),
    }


def alphazero_arch_from_payload(payload: dict | None) -> dict:
    if isinstance(payload, dict):
        arch = payload.get("arch")
        if isinstance(arch, dict):
            out = alphazero_kwargs_from_env()
            for key in ("hidden_size", "num_layers", "n_value_ensemble"):
                if key in arch:
                    out[key] = int(arch[key])
            return out
    return alphazero_kwargs_from_env()


def make_alphazero_net(n_observations: int, n_actions: list[int], **overrides):
    kwargs = alphazero_kwargs_from_env()
    kwargs.update(overrides)
    return AlphaZeroPolicyValueNet(n_observations, n_actions, **kwargs)


def load_alphazero_state_dict(net: "AlphaZeroPolicyValueNet", state_dict: dict, *, log_fn=None) -> tuple:
    """Load weights with strict=False; log legacy-arch mismatch warnings."""
    state = dict(state_dict)
    legacy = any(str(k).startswith("layer1.") for k in state)
    if legacy and log_fn is not None:
        log_fn(
            "[AZ][WARN] Чекпойнт со старой архитектурой (layer1/layer2). "
            "Нужно переобучить модель или добавить миграцию ключей."
        )
    missing, unexpected = net.load_state_dict(state, strict=False)
    if log_fn is not None and (missing or unexpected):
        log_fn(
            f"[AZ][WARN] load_state_dict: missing={len(missing)} unexpected={len(unexpected)} "
            f"(первые missing: {list(missing)[:3]})"
        )
    return missing, unexpected


def _mask_fill_value(logits: torch.Tensor) -> float:
    return float(torch.finfo(logits.dtype).min)


def _apply_action_mask(logits: torch.Tensor, mask: torch.Tensor | None) -> torch.Tensor:
    if mask is None:
        return logits
    if mask.dtype != torch.bool:
        mask = mask.to(dtype=torch.bool)
    if mask.shape != logits.shape:
        return logits
    valid_any = mask.any(dim=1, keepdim=True)
    safe_mask = torch.where(valid_any, mask, torch.ones_like(mask, dtype=torch.bool))
    fill = _mask_fill_value(logits)
    return logits.masked_fill(~safe_mask, fill)


class ResidualBlock(nn.Module):
    """Pre-norm residual MLP block (AlphaZero trunk)."""

    def __init__(self, hidden_size: int):
        super().__init__()
        self.norm1 = nn.LayerNorm(hidden_size)
        self.fc1 = nn.Linear(hidden_size, hidden_size)
        self.norm2 = nn.LayerNorm(hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)

    def forward(self, x):
        residual = x
        x = F.relu(self.norm1(self.fc1(x)))
        x = self.norm2(self.fc2(x))
        return F.relu(x + residual)


class AlphaZeroPolicyValueNet(nn.Module):
    """
    Factorized policy-value net:
    - несколько policy heads (по контракту action heads),
    - value head(s) в диапазоне [-1, 1] (tanh после усреднения ensemble).
    """

    def __init__(
        self,
        n_observations: int,
        n_actions: list[int],
        hidden_size: int = 256,
        num_layers: int = 2,
        n_value_ensemble: int = 1,
    ):
        super().__init__()
        self.n_observations = int(n_observations)
        self.action_sizes = [int(x) for x in n_actions]
        self.hidden_size = int(hidden_size)
        self.num_layers = max(1, int(num_layers))
        self.n_value_ensemble = max(1, int(n_value_ensemble))

        self.input_fc = nn.Linear(self.n_observations, self.hidden_size)
        self.input_norm = nn.LayerNorm(self.hidden_size)
        self.blocks = nn.ModuleList([ResidualBlock(self.hidden_size) for _ in range(self.num_layers)])
        self.policy_heads = nn.ModuleList([nn.Linear(self.hidden_size, n) for n in self.action_sizes])
        self.value_heads = nn.ModuleList(
            [nn.Linear(self.hidden_size, 1) for _ in range(self.n_value_ensemble)]
        )
        if self.n_value_ensemble == 1:
            self.value_head = self.value_heads[0]

    def _encode(self, obs: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.input_norm(self.input_fc(obs)))
        for block in self.blocks:
            x = block(x)
        return x

    def _value_from_features(self, x: torch.Tensor) -> torch.Tensor:
        if self.n_value_ensemble == 1:
            raw = self.value_heads[0](x).squeeze(-1)
        else:
            stacked = torch.stack([head(x).squeeze(-1) for head in self.value_heads], dim=0)
            raw = stacked.mean(dim=0)
        return torch.tanh(raw)

    def forward(self, obs: torch.Tensor):
        x = self._encode(obs)
        policy_logits = [head(x) for head in self.policy_heads]
        value = self._value_from_features(x)
        return policy_logits, value

    @torch.no_grad()
    def infer(self, obs: torch.Tensor, masks_by_head: list[torch.Tensor] | None = None):
        logits, value = self.forward(obs)
        probs = []
        for idx, head_logits in enumerate(logits):
            mask = None
            if masks_by_head is not None and idx < len(masks_by_head):
                mask = masks_by_head[idx]
            masked = _apply_action_mask(head_logits, mask)
            probs.append(torch.softmax(masked, dim=1))
        return probs, value
