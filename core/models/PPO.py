import os

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical


def ppo_kwargs_from_env():
    """Shared PPO constructor kwargs from environment variables."""
    return {
        "hidden_size": int(os.getenv("PPO_HIDDEN_SIZE", "256")),
        "num_layers": int(os.getenv("PPO_NUM_LAYERS", "2")),
        "n_value_ensemble": int(os.getenv("PPO_VALUE_ENSEMBLE", "1")),
    }


def ppo_arch_from_payload(payload: dict | None) -> dict:
    if isinstance(payload, dict):
        arch = payload.get("arch")
        if isinstance(arch, dict):
            out = ppo_kwargs_from_env()
            for key in ("hidden_size", "num_layers", "n_value_ensemble"):
                if key in arch:
                    out[key] = int(arch[key])
            return out
    return ppo_kwargs_from_env()


def make_actor_critic(n_observations, n_actions, **overrides):
    kwargs = ppo_kwargs_from_env()
    kwargs.update(overrides)
    return ActorCriticMultiHead(n_observations, n_actions, **kwargs)


def load_actor_critic_state_dict(net: "ActorCriticMultiHead", state_dict: dict, *, log_fn=None) -> tuple:
    """Load weights with strict=False; log legacy-arch mismatch warnings."""
    state = dict(state_dict)
    legacy = any(str(k).startswith("layer1.") for k in state)
    if legacy and log_fn is not None:
        log_fn(
            "[PPO][WARN] Чекпойнт со старой архитектурой (layer1/layer2). "
            "Нужно переобучить модель или добавить миграцию ключей."
        )
    missing, unexpected = net.load_state_dict(state, strict=False)
    if log_fn is not None and (missing or unexpected):
        log_fn(
            f"[PPO][WARN] load_state_dict: missing={len(missing)} unexpected={len(unexpected)} "
            f"(первые missing: {list(missing)[:3]})"
        )
    return missing, unexpected


def update_ppo_entropy_coef(
    current_coef: float,
    observed_entropy: float,
    target_entropy: float,
    adapt_lr: float = 0.05,
) -> float:
    """Adaptive entropy coefficient in [1e-4, 0.1]."""
    err = float(target_entropy) - float(observed_entropy)
    new_coef = float(current_coef) + float(adapt_lr) * err
    return max(1e-4, min(0.1, new_coef))


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
    masked_logits = logits.masked_fill(~safe_mask, fill)
    return masked_logits


class ResidualBlock(nn.Module):
    """Pre-norm residual MLP block (PPO trunk)."""

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


class ActorCriticMultiHead(nn.Module):
    def __init__(
        self,
        n_observations: int,
        n_actions: list[int],
        hidden_size: int = 256,
        num_layers: int = 2,
        n_value_ensemble: int = 1,
    ):
        super().__init__()
        self.action_sizes = [int(x) for x in n_actions]
        self.hidden_size = int(hidden_size)
        self.num_layers = max(1, int(num_layers))
        self.n_value_ensemble = max(1, int(n_value_ensemble))

        self.input_fc = nn.Linear(n_observations, self.hidden_size)
        self.input_norm = nn.LayerNorm(self.hidden_size)
        self.blocks = nn.ModuleList([ResidualBlock(self.hidden_size) for _ in range(self.num_layers)])
        self.policy_heads = nn.ModuleList([nn.Linear(self.hidden_size, size) for size in self.action_sizes])
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
            return self.value_heads[0](x).squeeze(-1)
        stacked = torch.stack([head(x).squeeze(-1) for head in self.value_heads], dim=0)
        return stacked.mean(dim=0)

    def forward(self, obs: torch.Tensor):
        x = self._encode(obs)
        logits = [head(x) for head in self.policy_heads]
        value = self._value_from_features(x)
        return logits, value

    def evaluate_actions(
        self,
        obs: torch.Tensor,
        actions: torch.Tensor,
        masks_by_head: list[torch.Tensor | None] | None = None,
    ):
        logits_list, values = self.forward(obs)
        total_logprob = torch.zeros(obs.shape[0], device=obs.device, dtype=torch.float32)
        total_entropy = torch.zeros(obs.shape[0], device=obs.device, dtype=torch.float32)
        for idx, logits in enumerate(logits_list):
            mask = None
            if masks_by_head is not None and idx < len(masks_by_head):
                mask = masks_by_head[idx]
            logits = _apply_action_mask(logits, mask)
            dist = Categorical(logits=logits)
            head_actions = actions[:, idx]
            total_logprob = total_logprob + dist.log_prob(head_actions)
            total_entropy = total_entropy + dist.entropy()
        return total_logprob, total_entropy, values

    @torch.no_grad()
    def act(
        self,
        obs: torch.Tensor,
        masks_by_head: list[torch.Tensor | None] | None = None,
        deterministic: bool = False,
        temperature: float = 1.0,
    ):
        # temperature: масштаб логитов перед сэмплом (eval PPO→stochastic). 1.0 — без изменений
        # (тренировка вызывает act() с дефолтом). <1 заостряет распределение, >1 сглаживает.
        # На deterministic-путь (argmax) температура не влияет.
        temp = float(temperature) if temperature else 1.0
        logits_list, values = self.forward(obs)
        actions = []
        total_logprob = torch.zeros(obs.shape[0], device=obs.device, dtype=torch.float32)
        for idx, logits in enumerate(logits_list):
            mask = None
            if masks_by_head is not None and idx < len(masks_by_head):
                mask = masks_by_head[idx]
            logits = _apply_action_mask(logits, mask)
            if not deterministic and temp > 0.0 and temp != 1.0:
                logits = logits / temp
            dist = Categorical(logits=logits)
            if deterministic:
                head_actions = logits.argmax(dim=1)
            else:
                head_actions = dist.sample()
            total_logprob = total_logprob + dist.log_prob(head_actions)
            actions.append(head_actions)
        stacked_actions = torch.stack(actions, dim=1)
        return stacked_actions, total_logprob, values

    @torch.no_grad()
    def infer_with_value(self, obs, masks_by_head=None):
        """Как act, но возвращает (probs, V). V — честный critic, mask-независим.

        Нужно seam'у env._simulate_reaction_branch (duck-typing hasattr infer_with_value):
        он зовёт net.infer_with_value(obs, masks_by_head=...) и ждёт (probs, value).
        Маски влияют только на probs; critic V их игнорирует.
        """
        logits_list, value = self.forward(obs)
        probs = []
        for idx, logits in enumerate(logits_list):
            mask = masks_by_head[idx] if (masks_by_head is not None and idx < len(masks_by_head)) else None
            masked = _apply_action_mask(logits, mask)
            probs.append(torch.softmax(masked, dim=1))
        return probs, value
