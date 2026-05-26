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
    max_grad_norm: float = 0.5
    lr_scheduler: str = "none"
    lr_warmup_steps: int = 0
    lr_total_steps: int = 0
    max_policy_staleness_updates: int = -1
    vtrace_full: bool = True
    vtrace_rho_clip: float = 0.7
    vtrace_c_clip: float = 0.7


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
    pi_beh_list: list[list[np.ndarray]],
    actions_BT: torch.Tensor,
    values_BT: torch.Tensor,
    rewards_BT: torch.Tensor,
    valid_BT: torch.Tensor,
    rho_clip: float = 0.7,
    c_clip: float = 0.7,
    gamma: float = 0.997,
) -> torch.Tensor:
    """Compute Retrace-style value targets across full unroll.

    Args:
        pi_cur_list: current-network softmax probs per head. pi_cur_list[h] has shape (T, A_h).
        pi_beh_list: per-step behavior logits (raw, pre-softmax). Each element is a list
            of per-head arrays: pi_beh_list[t][h] → np.ndarray of shape (A_h,).
            Heads can have different action-space sizes (factorized actions).
        actions_BT: selected actions per step, shape (B, T, K).
        values_BT: current value estimates, shape (B, T).
        rewards_BT: rewards, shape (B, T-1).
        valid_BT: validity mask, shape (B, T).
        rho_clip: max IS ratio clamp (e.g. 0.7).
        c_clip: trace-decay clip (e.g. 0.7).
        gamma: discount factor.

    Returns:
        (B, T) corrected value estimates.
    """
    B, T = values_BT.shape
    K = actions_BT.shape[-1]
    rho_clip = float(rho_clip)
    c_clip = float(c_clip)
    device = values_BT.device

    corrected_values = values_BT.clone()

    for t in range(T - 1):
        valid_t = valid_BT[:, t] * valid_BT[:, t + 1]
        if not valid_t.any():
            continue

        # Skip timestep if behavior logits are unavailable (IS weight defaults to 1)
        if t >= len(pi_beh_list):
            continue
        beh_heads = pi_beh_list[t]  # list[np.ndarray], one per head

        log_ratio = torch.zeros(B, device=device)
        skipped_head = False

        for h in range(K):
            # --- behavior probability for head h ---
            if h >= len(beh_heads):
                skipped_head = True
                break
            beh_h_np = beh_heads[h]
            if not isinstance(beh_h_np, np.ndarray):
                beh_h_np = np.asarray(beh_h_np, dtype=np.float32)
            if beh_h_np.size == 0:
                skipped_head = True
                break
            beh_h_logits = torch.as_tensor(beh_h_np.astype(np.float32), device=device)
            beh_h_probs = torch.softmax(beh_h_logits, dim=0)  # (A_h,)

            # --- current-policy probability for head h ---
            pi_cur_h_t = pi_cur_list[h][t]  # (A_h,) — already softmax
            A_h = pi_cur_h_t.shape[0]

            # action taken at this timestep for head h (B=1)
            a_h_idx = int(actions_BT[0, t, h].item())
            a_h_beh = min(a_h_idx, beh_h_probs.shape[0] - 1)
            a_h_cur = min(a_h_idx, A_h - 1)

            beh_prob = beh_h_probs[a_h_beh].clamp_min(1e-8)
            cur_prob = pi_cur_h_t[a_h_cur].clamp_min(1e-8)

            log_ratio = log_ratio + (torch.log(cur_prob) - torch.log(beh_prob))

        if skipped_head:
            # Incomplete behavior logits — skip IS correction for this step
            continue

        rho = torch.exp(log_ratio).clamp(max=rho_clip, min=0.0)
        c_t = torch.exp(log_ratio).clamp(max=c_clip, min=0.0)

        r_t = rewards_BT[:, t]
        v_next = values_BT[:, t + 1]
        v_cur = values_BT[:, t]
        delta = r_t + gamma * v_next - v_cur

        mask = valid_t.float()
        corrected_values[:, t] = v_cur + rho * delta * mask
        # Propagate correction backward (Retrace trace)
        if t + 1 < T:
            corrected_values[:, t + 1] = corrected_values[:, t + 1] + gamma * c_t * delta * mask

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
        vtrace_full = bool(getattr(config, "vtrace_full", True))

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
            rho_clip = float(getattr(config, "vtrace_rho_clip", 0.7))
            c_clip = float(getattr(config, "vtrace_c_clip", 0.7))
            gamma = float(getattr(config, "discount", 0.997) if hasattr(config, "discount") else 0.997)

            # Build pi_beh_list: list[list[np.ndarray]] — per-step, per-head raw logits
            # Each pi_beh_list[t][h] is a 1-D np.ndarray of shape (A_h,)
            # Heads can have different action-space sizes (factorized actions)
            pi_beh_list: list[list[np.ndarray]] = []
            for step_idx in range(min(T, len(behavior_logits_seq))):
                beh = behavior_logits_seq[step_idx]
                if isinstance(beh, (list, tuple)):
                    # Already a list of per-head arrays — keep as-is
                    pi_beh_list.append([np.asarray(x, dtype=np.float32) for x in beh])
                elif isinstance(beh, np.ndarray) and beh.ndim == 0:
                    pi_beh_list.append([])
                else:
                    # Unexpected format — skip
                    pi_beh_list.append([])

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
