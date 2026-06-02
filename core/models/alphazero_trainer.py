from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np
import torch
import torch.nn.functional as F

from core.models.alphazero_replay import AlphaZeroReplayBuffer


@dataclass
class AlphaZeroTrainConfig:
    lr: float = 3e-4
    batch_size: int = 128
    value_loss_weight: float = 1.0
    l2_weight: float = 1e-6
    balanced_outcome_sampling: bool = False
    balanced_faction_sampling: bool = False
    max_policy_staleness_updates: int = -1
    lr_scheduler_type: str = "none"
    lr_warmup_steps: int = 0
    lr_total_steps: int = 0


def alphazero_train_config_from_env(base: AlphaZeroTrainConfig | None = None) -> AlphaZeroTrainConfig:
    cfg = base or AlphaZeroTrainConfig()
    sched = str(os.getenv("AZ_LR_SCHEDULER", cfg.lr_scheduler_type or "none")).strip().lower() or "none"
    return AlphaZeroTrainConfig(
        lr=float(cfg.lr),
        batch_size=int(cfg.batch_size),
        value_loss_weight=float(cfg.value_loss_weight),
        l2_weight=float(cfg.l2_weight),
        balanced_outcome_sampling=bool(cfg.balanced_outcome_sampling),
        max_policy_staleness_updates=int(cfg.max_policy_staleness_updates),
        lr_scheduler_type=sched,
        lr_warmup_steps=int(os.getenv("AZ_LR_WARMUP_STEPS", str(cfg.lr_warmup_steps or 0))),
        lr_total_steps=int(os.getenv("AZ_LR_TOTAL_STEPS", str(cfg.lr_total_steps or 0))),
    )


def build_alphazero_lr_scheduler(optimizer, config: AlphaZeroTrainConfig, total_steps_hint: int | None = None):
    sched_type = str(getattr(config, "lr_scheduler_type", "none") or "none").strip().lower()
    if sched_type == "cosine":
        t_max = max(1, int(config.lr_total_steps or total_steps_hint or int(os.getenv("TOT_LIFE_T", "1000")) * 50))
        return torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=t_max)
    if sched_type == "plateau":
        return torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode="min", factor=0.5, patience=50, min_lr=1e-6
        )
    if sched_type == "linear_warmup_then_decay":
        warmup = max(0, int(config.lr_warmup_steps or 0))
        total = max(warmup + 1, int(config.lr_total_steps or total_steps_hint or 1000))

        def lr_lambda(step: int) -> float:
            if step < warmup:
                return float(step + 1) / float(max(1, warmup))
            progress = float(step - warmup) / float(max(1, total - warmup))
            return max(0.0, 1.0 - progress)

        return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lr_lambda)
    return None


def step_alphazero_lr_scheduler(scheduler, loss_value: float | None = None) -> None:
    if scheduler is None:
        return
    if isinstance(scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
        if loss_value is not None:
            scheduler.step(float(loss_value))
    else:
        scheduler.step()


def train_alphazero_step(
    *,
    net,
    optimizer,
    replay: AlphaZeroReplayBuffer,
    config: AlphaZeroTrainConfig,
    device: torch.device,
    current_policy_version: int = 0,
    scheduler=None,
):
    if bool(getattr(config, "balanced_faction_sampling", False)):
        batch = replay.sample_balanced_per_faction(int(config.batch_size))
    elif bool(getattr(config, "balanced_outcome_sampling", False)):
        batch = replay.sample_balanced_outcome(int(config.batch_size))
    else:
        batch = replay.sample(int(config.batch_size))
    if not batch:
        return None
    max_staleness = int(getattr(config, "max_policy_staleness_updates", -1))
    if max_staleness >= 0:
        min_ver = int(current_policy_version) - max_staleness
        batch = [b for b in batch if int(getattr(b, "policy_version", 0)) >= min_ver]
        if not batch:
            return None
    # np.stack + from_numpy вместо torch.tensor([np-массивы]) — ~20× быстрее сборки
    # и без UserWarning «extremely slow» (числа идентичны).
    obs_np = np.stack([np.asarray(b.state, dtype=np.float32) for b in batch])
    obs = torch.from_numpy(obs_np).to(device)
    target_value = torch.from_numpy(
        np.asarray([b.value_target for b in batch], dtype=np.float32)
    ).to(device)
    logits_by_head, value = net(obs)

    num_heads = len(logits_by_head)
    # Стэки таргетов по головам собираем разом (один np.stack на голову, не torch.tensor([...]))
    target_pi_by_head = [
        torch.from_numpy(
            np.stack([np.asarray(b.policy_targets[h], dtype=np.float32) for b in batch])
        ).to(device)
        for h in range(num_heads)
    ]

    policy_loss = torch.tensor(0.0, device=device)
    for h_idx, logits in enumerate(logits_by_head):
        target_pi = target_pi_by_head[h_idx]
        target_pi = target_pi / target_pi.sum(dim=1, keepdim=True).clamp_min(1e-8)
        logp = F.log_softmax(logits, dim=1)
        policy_loss = policy_loss + (-(target_pi * logp).sum(dim=1).mean())

    value_loss = F.mse_loss(value, target_value)
    l2 = torch.tensor(0.0, device=device)
    for p in net.parameters():
        l2 = l2 + torch.sum(p * p)
    loss = policy_loss + float(config.value_loss_weight) * value_loss + float(config.l2_weight) * l2

    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
    optimizer.step()
    step_alphazero_lr_scheduler(scheduler, loss_value=float(loss.item()))

    return {
        "loss": float(loss.item()),
        "policy_loss": float(policy_loss.item()),
        "value_loss": float(value_loss.item()),
    }
