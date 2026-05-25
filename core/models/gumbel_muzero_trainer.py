from __future__ import annotations

from dataclasses import dataclass
import copy
import numpy as np
import torch
import torch.nn.functional as F

from core.models.gumbel_muzero_replay import GumbelMuZeroReplayBuffer


# ---------------------------------------------------------------------------
# B4: EMA target for SimSiam consistency (Conservative Polyak)
# ---------------------------------------------------------------------------

class GumbelMuZeroEMATarget:
    """Slow-moving copy of the network for SimSiam consistency loss.

    Uses Conservative Polyak (tau=0.005) to keep the target encoder stable.
    This provides the target latent for the consistency loss between
    the online network's prediction and the EMA-encoded observation.
    """

    def __init__(self, net, tau: float = 0.005):
        self.tau = tau
        # Deep copy of the entire network as the EMA target
        self.target = copy.deepcopy(net)
        self.target.eval()
        # Freeze target to prevent gradients
        for p in self.target.parameters():
            p.requires_grad_(False)

    def ema_update(self, net) -> None:
        """Move EMA target toward online network (Conservative Polyak)."""
        with torch.no_grad():
            for tp, sp in zip(self.target.parameters(), net.parameters()):
                tp.data.mul_(1.0 - self.tau).add_(sp.data, alpha=self.tau)


@dataclass
class GumbelMuZeroTrainConfig:
    lr: float = 3e-4
    batch_size: int = 128
    unroll_steps: int = 5
    tbptt_truncate: int = 3
    value_loss_weight: float = 1.0
    reward_loss_weight: float = 1.0
    consistency_loss_weight: float = 1.0
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


def _vtrace_is_weights(
    logits: list[torch.Tensor],
    behavior_logits: list[np.ndarray],
    actions: list[int],
    clip_rho: float = 10.0,
) -> float:
    """Compute per-sample V-trace importance-sampling (IS) ratio for one step.

    For each head h:
        ρ_h = π_target[a_h | h] / π_behavior[a_h | h]
    where π_target = softmax(logits) and π_behavior = softmax(behavior_logits).

    The overall ratio is the product over heads: ρ = ∏_h ρ_h.
    Clamped to [0, clip_rho] to prevent instability.

    Args:
        logits: current-network logits per head, each [n_actions]
        behavior_logits: stored root logits per head, each [n_actions]
        actions: the action indices taken at this step per head

    Returns:
        Scalar IS weight (clamped, for multiplying policy loss).
    """
    log_rho = 0.0
    for h_idx, (logits_h, beh_np, act_h) in enumerate(zip(logits, behavior_logits, actions)):
        # log π_target[a] = logits_h[a] - logsumexp(logits_h)
        log_target = logits_h.float()
        log_target = log_target - logits_h.logsumexp(dim=0)
        target_logprob = log_target[act_h] if act_h < len(log_target) else logits_h.new_full((1,), -1e9)[0]

        # log π_behavior[a] = beh_np[a] - logsumexp(beh_np)
        beh_t = torch.as_tensor(beh_np, dtype=torch.float32, device=logits_h.device)
        beh_log_softmax = beh_t - beh_t.logsumexp(dim=0)
        beh_logprob = beh_log_softmax[act_h] if act_h < len(beh_log_softmax) else beh_t.new_full((1,), -1e9)[0]

        log_rho = log_rho + float(target_logprob - beh_logprob)

    return float(np.clip(np.exp(log_rho), 0.0, float(clip_rho)))


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
    ema_target=None,
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
    total_consistency_loss = torch.tensor(0.0, device=device)
    samples_count = 0

    _consistency_w = float(getattr(config, "consistency_loss_weight", 0.0))
    _target_enc = (ema_target.target if ema_target is not None else net) if _consistency_w > 0.0 else None

    for sample in batch:
        states = sample["states"]
        actions = sample["actions"]
        rewards = sample["rewards"]
        policies = sample["policy_targets"]
        values = sample["value_targets"]
        behavior_logits_seq = sample.get("behavior_logits", []) or []
        if not states:
            continue
        samples_count += 1

        # A3: V-trace IS weight for step 0
        obs0 = torch.as_tensor(states[0], dtype=torch.float32, device=device).unsqueeze(0)
        logits, value, reward0, latent = net.initial_inference(obs0, masks_by_head=None)
        logits_list = [l.squeeze(0) for l in logits]
        beh0 = behavior_logits_seq[0] if behavior_logits_seq else []
        is_weight = _vtrace_is_weights(logits_list, beh0, actions[0]) if beh0 else 1.0
        total_policy_loss = total_policy_loss + _policy_ce_loss(logits, policies[0], device=device) * is_weight
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
            logits_t_list = [l.squeeze(0) for l in logits_t]
            beh_t = behavior_logits_seq[t] if t < len(behavior_logits_seq) else []
            is_weight_t = _vtrace_is_weights(logits_t_list, beh_t, actions[t - 1]) if beh_t else 1.0
            total_policy_loss = total_policy_loss + _policy_ce_loss(logits_t, policies[t], device=device) * is_weight_t
            total_value_loss = total_value_loss + F.mse_loss(
                value_t, torch.tensor([float(values[t])], device=device)
            )
            total_reward_loss = total_reward_loss + F.mse_loss(
                reward_t, torch.tensor([float(rewards[t - 1])], device=device)
            )

            # Consistency loss: predicted latent vs EMA-target encoding of next obs
            if _target_enc is not None and t < len(states):
                obs_t = torch.as_tensor(states[t], dtype=torch.float32, device=device).unsqueeze(0)
                with torch.no_grad():
                    _enc = _target_enc
                    target_proj = _enc.project_latent(_enc.encode(obs_t)).detach()
                pred_proj = net.project_latent(latent)
                total_consistency_loss = total_consistency_loss + (
                    1.0 - (pred_proj * target_proj).sum(dim=1).mean()
                )

    if samples_count <= 0:
        return None

    policy_loss = total_policy_loss / float(samples_count)
    value_loss = total_value_loss / float(samples_count)
    reward_loss = total_reward_loss / float(samples_count)
    consistency_loss = total_consistency_loss / float(samples_count)
    l2 = torch.tensor(0.0, device=device)
    for p in net.parameters():
        l2 = l2 + torch.sum(p * p)

    loss = (
        policy_loss
        + float(config.value_loss_weight) * value_loss
        + float(config.reward_loss_weight) * reward_loss
        + _consistency_w * consistency_loss
        + float(config.l2_weight) * l2
    )
    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(net.parameters(), float(config.max_grad_norm))
    optimizer.step()

    # B4: EMA update for consistency target (Conservative Polyak)
    if ema_target is not None:
        ema_target.ema_update(net)

    if scheduler is not None:
        scheduler.step()

    return {
        "loss": float(loss.item()),
        "policy_loss": float(policy_loss.item()),
        "value_loss": float(value_loss.item()),
        "reward_loss": float(reward_loss.item()),
        "consistency_loss": float(consistency_loss.item()),
    }
