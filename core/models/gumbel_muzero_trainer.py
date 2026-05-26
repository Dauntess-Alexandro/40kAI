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


def _vtrace_targets(
    pi_cur_list: list[torch.Tensor],
    pi_beh_list: list[np.ndarray],
    actions_BT: torch.Tensor,
    values_BT: torch.Tensor,
    rewards_BT: torch.Tensor,
    valid_BT: torch.Tensor,
    rho_clip: float = 1.0,
    c_clip: float = 1.0,
    gamma: float = 0.997,
) -> torch.Tensor:
    """Compute Retrace-style value targets across full unroll.

    Uses the canonical Retrace algorithm to correct value estimates using
    importance-sampling corrections from the behavior policy.

    Args:
        pi_cur_list: current-network softmax probs per head, each (T, A_h) where
            T is the number of unroll steps and A_h is the number of actions for head h.
            At timestep t, we use pi_cur_list[h][t] for the IS ratio.
        pi_beh_list: behavior policy raw logits per step, each (A_total,) flattened
            over all heads (or list of head arrays).
        actions_BT: selected actions per step, (B, T-1, K) where K is num_heads
        values_BT: current value estimates, (B, T)
        rewards_BT: rewards, (B, T-1)
        valid_BT: validity mask, (B, T)
        rho_clip: max importance sampling ratio (clamp max)
        c_clip: trace decay clip (clamp max for c_t)
        gamma: discount factor

    Returns:
        (B, T) corrected value estimates with Retrace bootstrap corrections
    """
    B, T = values_BT.shape
    K = actions_BT.shape[-1]
    rho_clip = float(rho_clip)
    c_clip = float(c_clip)
    device = values_BT.device

    corrected_values = values_BT.clone()

    # Build behavior softmax per step: pi_beh_softmax[t] = (A_total,) tensor
    pi_beh_softmax_list: list[torch.Tensor] = []
    for beh_np in pi_beh_list:
        beh_t = torch.as_tensor(beh_np, dtype=torch.float32, device=device)
        if beh_t.dim() == 1:
            pi_beh_softmax_list.append(beh_t)  # (A_total,)
        else:
            pi_beh_softmax_list.append(beh_t.flatten())

    # Retrace recursive update: for each t=0..T-2
    for t in range(T - 1):
        valid_t = valid_BT[:, t] * valid_BT[:, t + 1]
        if not valid_t.any():
            continue

        # Compute importance ratio log π_cur[a] - log π_beh[a] for batch
        log_ratio = torch.zeros(B, device=device)

        # For each head, accumulate log ratio
        for h in range(K):
            a_h = actions_BT[:, t, h].long()  # (B,)
            # π_cur for head h at timestep t: pi_cur_list[h][t] → shape (A_h,) for batch item 0
            pi_cur_h_t = pi_cur_list[h][t]  # (A_h,) — per sample, single sample (B=1)
            # For batch B>1 this would need indexing; here B=1 so we use directly
            if B == 1:
                pi_cur_h_t = pi_cur_h_t.unsqueeze(0)  # → (1, A_h)

            # Find offset for head h in flattened behavior probs
            # behavior logits are stored per step, each with K heads of A actions each
            # We assume equal action space per head: A = total_actions / K
            # Or we use the stored format: pi_beh_list[t] is list of arrays per head
            # Let's handle both cases
            beh_t = pi_beh_softmax_list[t] if t < len(pi_beh_softmax_list) else pi_beh_softmax_list[-1]
            # Try to reshape if it looks like concatenated heads
            beh_len = beh_t.numel()
            A = beh_len // K if K > 0 and beh_len % K == 0 else beh_len
            if beh_len == K * A:
                # Flat concatenated; extract head h
                beh_h_t = beh_t[h * A:(h + 1) * A]
            else:
                beh_h_t = beh_t

            # π_beh for selected action
            beh_prob = beh_h_t[a_h % beh_h_t.numel()].clamp_min(1e-8)

            # For current policy, find the action offset
            A_h = pi_cur_h_t.shape[-1]
            action_idx = a_h[0] if B > 1 else a_h.item()
            action_idx = min(action_idx, A_h - 1)
            cur_prob = pi_cur_h_t[0 if B == 1 else 0, action_idx].clamp_min(1e-8)

            log_ratio = log_ratio + (torch.log(cur_prob) - torch.log(beh_prob))

        rho = torch.exp(log_ratio).clamp(max=rho_clip, min=0.0)

        # Bootstrap correction: η_t = ρ_t * (r_t + γ * V_{t+1} - V_t)
        r_t = rewards_BT[:, t]
        v_next = values_BT[:, t + 1]
        v_cur = values_BT[:, t]
        delta = r_t + gamma * v_next - v_cur

        correction = rho * delta
        mask = valid_t.float().unsqueeze(1)
        corrected_values[:, t] = v_cur + correction * mask.squeeze(1)

    return corrected_values


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

        # B1: V-trace full unroll — collect all values/actions/rewards through unroll
        # Then apply Retrace correction across all timesteps t=0..T-1
        import os as _os
        vtrace_full = _os.environ.get("GMZ_VTRACE_FULL", "0") == "1"

        values_BT_list: list[float] = []
        actions_BT_list: list[list[int]] = []
        # pi_cur_all_steps[h] = (T, A_h) per head
        pi_cur_all_steps: list[list[torch.Tensor]] = []
        behavior_logits_seq = sample.get("behavior_logits", []) or []

        # --- t=0 ---
        obs0 = torch.as_tensor(states[0], dtype=torch.float32, device=device).unsqueeze(0)
        logits0, value0, reward0, latent = net.initial_inference(obs0, masks_by_head=None)
        pi_cur0 = [F.softmax(l, dim=1).squeeze(0) for l in logits0]  # (B, A_h) → squeeze → (A_h,)
        pi_cur_all_steps = [list(step) for step in zip(*[[F.softmax(l, dim=1).squeeze(0) for l in logits0]])]
        pi_cur_all_steps = [[pi_cur0[h]] for h in range(len(pi_cur0))]

        values_BT_list.append(float(values[0]))
        actions_BT_list.append(actions[0])
        total_reward_loss = total_reward_loss + F.mse_loss(
            reward0, torch.tensor([0.0], device=device)
        )

        # --- t=1..T-1 ---
        for t in range(1, min(len(states), max(1, int(config.unroll_steps)))):
            # TBPTT: detach latent after tbptt_k steps to truncate gradients
            if t > tbptt_k:
                latent = latent.detach()

            action_t = torch.as_tensor(actions[t - 1], dtype=torch.long, device=device).unsqueeze(0)
            logits_t, value_t, reward_t, latent = net.recurrent_inference(
                latent, action_t, masks_by_head=None
            )
            pi_cur_t = [F.softmax(l, dim=1).squeeze(0) for l in logits_t]
            for h in range(len(pi_cur_t)):
                pi_cur_all_steps[h].append(pi_cur_t[h])

            values_BT_list.append(float(value_t.item()))
            actions_BT_list.append(actions[t] if t < len(actions) else actions[-1])
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

        # Build tensors for V-trace
        T = len(values_BT_list)
        K = len(actions[0]) if actions else 1

        values_BT = torch.tensor([values_BT_list], dtype=torch.float32, device=device)
        actions_np = np.array(actions_BT_list, dtype=np.int64)  # (T, K)
        actions_BT = torch.tensor(actions_np, dtype=torch.long, device=device).unsqueeze(0)  # (1, T, K)
        rewards_np = np.array([float(r) for r in rewards], dtype=np.float32)[:T - 1] if T > 1 else np.zeros(0, dtype=np.float32)
        rewards_BT = torch.tensor([rewards_np], dtype=torch.float32, device=device) if rewards_np.size > 0 else torch.zeros((1, max(0, T - 1)), dtype=torch.float32, device=device)
        valid_BT = torch.ones((1, T), dtype=torch.bool, device=device)

        # V-trace correction across full unroll
        if vtrace_full and len(behavior_logits_seq) >= 1:
            rho_clip = float(_os.environ.get("GMZ_VTRACE_RHO_CLIP", "0.7"))
            c_clip = float(_os.environ.get("GMZ_VTRACE_C_CLIP", "0.7"))
            gamma = float(_os.environ.get("GMZ_VTRACE_GAMMA", "0.997"))

            # Build pi_beh list from behavior_logits_seq (raw logits, pre-softmax)
            # Each entry: list of arrays per head, shape (A_h,)
            pi_beh_list: list[np.ndarray] = []
            for step_idx in range(min(T, len(behavior_logits_seq))):
                beh = behavior_logits_seq[step_idx]
                if isinstance(beh, (list, tuple)):
                    pi_beh_list.append(np.array(beh, dtype=np.float32))
                else:
                    pi_beh_list.append(np.asarray(beh, dtype=np.float32))

            # pi_cur_list[h] = (T, A_h) — stack across timesteps for each head
            pi_cur_list = [
                torch.stack(pi_cur_all_steps[h], dim=0)  # (T, A_h)
                for h in range(K)
            ]

            corrected_values = _vtrace_targets(
                pi_cur_list=pi_cur_list,
                pi_beh_list=pi_beh_list,
                actions_BT=actions_BT,
                values_BT=values_BT,
                rewards_BT=rewards_BT,
                valid_BT=valid_BT,
                rho_clip=rho_clip,
                c_clip=c_clip,
                gamma=gamma,
            )
        else:
            corrected_values = values_BT

        # Policy loss: simple IS weight at t=0 (backward compat)
        logits_for_policy = [l.squeeze(0) for l in logits0]
        beh0 = behavior_logits_seq[0] if behavior_logits_seq else []
        is_weight_scalar = 1.0
        if beh0:
            log_rho = torch.tensor(0.0, device=device)
            for h in range(len(logits_for_policy)):
                pi_cur_h = F.softmax(logits_for_policy[h], dim=0)
                beh_h = torch.as_tensor(
                    np.asarray(beh0[h] if isinstance(beh0[h], np.ndarray) else beh0[h], dtype=np.float32),
                    device=device
                )
                pi_beh_h = F.softmax(beh_h, dim=0)
                a_h = actions[0][h] if h < len(actions[0]) else 0
                log_rho = log_rho + (torch.log(pi_cur_h[a_h].clamp_min(1e-8)) - torch.log(pi_beh_h[a_h].clamp_min(1e-8)))
            is_weight_scalar = float(torch.exp(log_rho.detach()).clamp(max=1.0))
        total_policy_loss = total_policy_loss + _policy_ce_loss(logits0, policies[0], device=device) * is_weight_scalar

        # Value loss: use V-trace corrected targets
        for t in range(T):
            target_v = corrected_values[0, t].item()
            total_value_loss = total_value_loss + F.mse_loss(
                torch.tensor([values_BT_list[t]], device=device),
                torch.tensor([target_v], device=device)
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
