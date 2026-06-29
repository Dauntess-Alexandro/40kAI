"""PHOENIX losses: SPR consistency (BYOL cosine) + IQN TD с латентным value-expansion."""
from __future__ import annotations

import torch
import torch.nn.functional as F


def spr_consistency_loss(pred_seq: torch.Tensor, target_proj_seq: torch.Tensor,
                         done_mask: torch.Tensor) -> torch.Tensor:
    # pred_seq, target_proj_seq: [B, K, P]; done_mask: [B, K] (1 = невалидный шаг)
    target = target_proj_seq.detach()
    pred_n = F.normalize(pred_seq, dim=-1, eps=1e-6)
    target_n = F.normalize(target, dim=-1, eps=1e-6)
    cos = (pred_n * target_n).sum(dim=-1)  # [B, K]
    per_step = 1.0 - cos  # косинус-дистанция
    valid = (1.0 - done_mask).to(per_step.dtype)
    denom = valid.sum().clamp(min=1.0)
    return (per_step * valid).sum() / denom


def value_expansion_target(rewards: torch.Tensor, gammas: torch.Tensor,
                           bootstrap_q: torch.Tensor, h: int) -> torch.Tensor:
    # rewards, gammas: [B, Hmax]; bootstrap_q: [B]; возврат [B]
    h = int(h)
    if h <= 0:
        return bootstrap_q
    acc = torch.zeros_like(bootstrap_q)
    discount = torch.ones_like(bootstrap_q)
    for j in range(h):
        acc = acc + discount * rewards[:, j]
        discount = discount * gammas[:, j]
    return acc + discount * bootstrap_q


def value_expansion_target_masked(rewards: torch.Tensor, gammas: torch.Tensor,
                                  bootstrap_q: torch.Tensor, done_mask: torch.Tensor,
                                  h: int) -> torch.Tensor:
    """VE-таргет с маской терминала (спека §7: не бутстрапим/не суммируем сквозь done).

    `done_mask[b,k]=1` означает «шаг k невалиден» (за терминалом эпизода). Награды за
    терминалом зануляются, bootstrap на `obs[t+h]` зануляется, если шаг h уже за терминалом —
    так VE-возврат честно обрезается на границе эпизода (нет утечки награды/значения из
    следующего эпизода в скользящем окне sequence-replay).

    rewards, gammas: [B, Hmax]; bootstrap_q: [B]; done_mask: [B, >=h+1]; возврат [B].
    """
    h = int(h)
    if h <= 0:
        return bootstrap_q
    reward_mask = (1.0 - done_mask[:, :h]).to(rewards.dtype)
    masked_rewards = rewards[:, :h] * reward_mask
    if done_mask.shape[1] > h:
        boot_mask = (1.0 - done_mask[:, h]).to(bootstrap_q.dtype)
    else:
        boot_mask = torch.ones_like(bootstrap_q)
    return value_expansion_target(masked_rewards, gammas, bootstrap_q * boot_mask, h)
