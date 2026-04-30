from __future__ import annotations

from dataclasses import dataclass

import torch
import torch.nn.functional as F

from core.models.alphazero_replay import AlphaZeroReplayBuffer


@dataclass
class AlphaZeroTrainConfig:
    lr: float = 3e-4
    batch_size: int = 128
    value_loss_weight: float = 1.0
    l2_weight: float = 1e-6


def train_alphazero_step(*, net, optimizer, replay: AlphaZeroReplayBuffer, config: AlphaZeroTrainConfig, device: torch.device):
    batch = replay.sample(int(config.batch_size))
    if not batch:
        return None
    obs = torch.tensor([b.state for b in batch], dtype=torch.float32, device=device)
    target_value = torch.tensor([b.value_target for b in batch], dtype=torch.float32, device=device)
    logits_by_head, value = net(obs)

    policy_loss = torch.tensor(0.0, device=device)
    for h_idx, logits in enumerate(logits_by_head):
        target_pi = torch.tensor([b.policy_targets[h_idx] for b in batch], dtype=torch.float32, device=device)
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
    return {
        "loss": float(loss.item()),
        "policy_loss": float(policy_loss.item()),
        "value_loss": float(value_loss.item()),
    }
