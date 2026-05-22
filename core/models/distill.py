"""Knowledge distillation from teacher policy networks into DQN student."""

from __future__ import annotations

import torch
import torch.nn.functional as F


def _softmax_heads(q_heads: list[torch.Tensor], temperature: float = 1.0) -> list[torch.Tensor]:
    temp = max(1e-6, float(temperature))
    return [F.softmax(head / temp, dim=-1) for head in q_heads]


def policy_kl_loss(teacher_probs: list[torch.Tensor], student_q_heads: list[torch.Tensor], temperature: float = 1.0) -> torch.Tensor:
    """KL(teacher || student) averaged over action heads."""
    student_probs = _softmax_heads(student_q_heads, temperature=temperature)
    losses = []
    for p_t, p_s in zip(teacher_probs, student_probs):
        log_s = (p_s + 1e-8).log()
        losses.append(F.kl_div(log_s, p_t, reduction="batchmean"))
    if not losses:
        return torch.tensor(0.0)
    return torch.stack(losses).mean()


def distill_step(
    teacher,
    student,
    obs_batch: torch.Tensor,
    alpha_kl: float = 1.0,
    beta_value: float = 0.0,
    temperature: float = 1.0,
) -> dict:
    """
    One distillation step: teacher provides policy targets, student DQN matches via KL on Q-softmax.
    teacher must implement forward returning list of per-head tensors (probabilities or logits).
    """
    student.train()
    teacher.eval()
    with torch.no_grad():
        teacher_out = teacher(obs_batch)
        if isinstance(teacher_out, tuple):
            teacher_out = teacher_out[0]
        if isinstance(teacher_out, list):
            teacher_probs = [
                F.softmax(h, dim=-1) if h.dtype.is_floating_point else h.float()
                for h in teacher_out
            ]
        else:
            raise TypeError("teacher должен возвращать list тензоров по action-головам")

    student_q = student.q_values(obs_batch)
    kl = policy_kl_loss(teacher_probs, student_q, temperature=temperature)
    loss = float(alpha_kl) * kl
    stats = {"kl_loss": float(kl.item()), "total_loss": float(loss.item())}
    if beta_value > 0.0 and hasattr(teacher, "value_head"):
        pass  # value MSE hook for future AZ/MuZero value heads
    return {"loss": loss, "stats": stats}


def distill_az_to_dqn(teacher_az, student_dqn, obs_batch: torch.Tensor, **kwargs) -> dict:
    """Distill AlphaZero policy_value_net policy into DQN Q-heads."""
    return distill_step(teacher_az, student_dqn, obs_batch, **kwargs)


def distill_muzero_to_dqn(teacher_gmz, student_dqn, obs_batch: torch.Tensor, **kwargs) -> dict:
    """Distill GumbelMuZero prediction policy into DQN Q-heads."""
    return distill_step(teacher_gmz, student_dqn, obs_batch, **kwargs)
