from __future__ import annotations

from dataclasses import dataclass
import torch
import torch.nn.functional as F

from core.models.gumbel_muzero_replay import GumbelMuZeroReplayBuffer


@dataclass
class GumbelMuZeroTrainConfig:
    lr: float = 3e-4
    batch_size: int = 128
    unroll_steps: int = 5
    tbptt_truncate: int = 3
    value_loss_weight: float = 1.0
    reward_loss_weight: float = 1.0
    l2_weight: float = 1e-6
    max_grad_norm: float = 1.0
    lr_scheduler: str = "none"
    lr_warmup_steps: int = 0
    lr_total_steps: int = 0
    max_policy_staleness_updates: int = -1


def _policy_ce_loss(logits_by_head, target_by_head, device: torch.device) -> torch.Tensor:
    loss = torch.tensor(0.0, device=device)
    for h_idx, logits in enumerate(logits_by_head):
        target = torch.as_tensor(target_by_head[h_idx], dtype=torch.float32, device=device).unsqueeze(0)
        target = target / target.sum(dim=1, keepdim=True).clamp_min(1e-8)
        logp = F.log_softmax(logits, dim=1)
        loss = loss + (-(target * logp).sum(dim=1).mean())
    return loss


def make_gmz_lr_scheduler(optimizer, config: GumbelMuZeroTrainConfig):
    name = str(config.lr_scheduler).lower()
    if name == "cosine" and int(config.lr_total_steps) > 0:
        return torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=int(config.lr_total_steps),
            eta_min=float(config.lr) * 0.1,
        )
    if name == "linear" and int(config.lr_total_steps) > 0:
        def lr_lambda(step: int) -> float:
            warmup = max(1, int(config.lr_warmup_steps))
            total = max(warmup + 1, int(config.lr_total_steps))
            if step < warmup:
                return float(step) / float(warmup)
            return max(0.0, 1.0 - (step - warmup) / float(total - warmup))
        return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lr_lambda)
    return None


def train_gumbel_muzero_step(
    *,
    net,
    optimizer,
    replay: GumbelMuZeroReplayBuffer,
    config: GumbelMuZeroTrainConfig,
    device: torch.device,
    current_policy_version: int = 0,
    scheduler=None,
):
    batch = replay.sample_unroll(
        batch_size=int(config.batch_size),
        unroll_steps=max(1, int(config.unroll_steps)),
        max_policy_staleness_updates=int(getattr(config, "max_policy_staleness_updates", -1)),
        current_policy_version=int(current_policy_version),
    )
    if not batch:
        return None

    tbptt_k = max(1, int(getattr(config, "tbptt_truncate", config.unroll_steps)))

    total_policy_loss = torch.tensor(0.0, device=device)
    total_value_loss = torch.tensor(0.0, device=device)
    total_reward_loss = torch.tensor(0.0, device=device)
    samples_count = 0

    for sample in batch:
        states = sample["states"]
        actions = sample["actions"]
        rewards = sample["rewards"]
        policies = sample["policy_targets"]
        values = sample["value_targets"]
        if not states:
            continue
        samples_count += 1

        obs0 = torch.as_tensor(states[0], dtype=torch.float32, device=device).unsqueeze(0)
        logits, value, reward0, latent = net.initial_inference(obs0, masks_by_head=None)
        total_policy_loss = total_policy_loss + _policy_ce_loss(logits, policies[0], device=device)
        total_value_loss = total_value_loss + F.mse_loss(
            value, torch.tensor([float(values[0])], device=device)
        )
        total_reward_loss = total_reward_loss + F.mse_loss(
            reward0, torch.tensor([0.0], device=device)
        )

        for t in range(1, min(len(states), max(1, int(config.unroll_steps)))):
            # TBPTT: detach latent after tbptt_k steps to truncate gradients
            if t > tbptt_k:
                latent = latent.detach()

            action_t = torch.as_tensor(actions[t - 1], dtype=torch.long, device=device).unsqueeze(0)
            logits_t, value_t, reward_t, latent = net.recurrent_inference(
                latent, action_t, masks_by_head=None
            )
            total_policy_loss = total_policy_loss + _policy_ce_loss(logits_t, policies[t], device=device)
            total_value_loss = total_value_loss + F.mse_loss(
                value_t, torch.tensor([float(values[t])], device=device)
            )
            total_reward_loss = total_reward_loss + F.mse_loss(
                reward_t, torch.tensor([float(rewards[t - 1])], device=device)
            )

    if samples_count <= 0:
        return None

    policy_loss = total_policy_loss / float(samples_count)
    value_loss = total_value_loss / float(samples_count)
    reward_loss = total_reward_loss / float(samples_count)
    l2 = torch.tensor(0.0, device=device)
    for p in net.parameters():
        l2 = l2 + torch.sum(p * p)

    loss = (
        policy_loss
        + float(config.value_loss_weight) * value_loss
        + float(config.reward_loss_weight) * reward_loss
        + float(config.l2_weight) * l2
    )
    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(net.parameters(), float(config.max_grad_norm))
    optimizer.step()

    if scheduler is not None:
        scheduler.step()

    return {
        "loss": float(loss.item()),
        "policy_loss": float(policy_loss.item()),
        "value_loss": float(value_loss.item()),
        "reward_loss": float(reward_loss.item()),
    }
