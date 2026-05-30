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


def _vtrace_targets_batched(
    *,
    pi_cur_steps: list[list[torch.Tensor]],   # [t][h] -> (B, A_h) detached softmax probs
    beh_logits_steps: list[torch.Tensor],      # [h] -> (B, T, A_h) raw logits (0 where unavailable)
    beh_avail: torch.Tensor,                    # (B, T) bool — step usable (all heads present)
    actions: torch.Tensor,                      # (B, T, K) long
    value_base: torch.Tensor,                   # (B, T) float — base (target) values, detached
    rewards: torch.Tensor,                      # (B, T) float — replay reward at step t
    valid: torch.Tensor,                        # (B, T) bool
    rho_clip: float,
    c_clip: float,
    gamma: float,
) -> torch.Tensor:
    """Batched Retrace-style value-target correction.

    Mirrors :func:`_vtrace_targets` step-for-step but operates on the whole batch
    at once. IS ratios use detached current-policy probs (these are *targets*).
    """
    B, T = value_base.shape
    K = actions.shape[-1]
    device = value_base.device
    corrected = value_base.clone()
    for t in range(T - 1):
        valid_t = valid[:, t] & valid[:, t + 1]
        usable = (valid_t & beh_avail[:, t]).float()       # (B,)
        log_ratio = torch.zeros(B, device=device)
        for h in range(K):
            cur = pi_cur_steps[t][h]                        # (B, A_h)
            a = actions[:, t, h].clamp(0, cur.shape[1] - 1)
            cur_p = cur.gather(1, a.unsqueeze(1)).squeeze(1).clamp_min(1e-8)
            beh_p = F.softmax(beh_logits_steps[h][:, t, :], dim=1)
            beh_p = beh_p.gather(1, a.unsqueeze(1)).squeeze(1).clamp_min(1e-8)
            log_ratio = log_ratio + (torch.log(cur_p) - torch.log(beh_p))
        rho = torch.exp(log_ratio).clamp(min=0.0, max=rho_clip)
        c_t = torch.exp(log_ratio).clamp(min=0.0, max=c_clip)
        delta = rewards[:, t] + gamma * value_base[:, t + 1] - value_base[:, t]
        corrected[:, t] = value_base[:, t] + rho * delta * usable
        if t + 1 < T:
            corrected[:, t + 1] = corrected[:, t + 1] + gamma * c_t * delta * usable
    return corrected


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

    _consistency_w = float(getattr(config, "consistency_loss_weight", 0.0))
    _target_enc = (ema_target.target if ema_target is not None else net) if _consistency_w > 0.0 else None

    # -------------------------------------------------------------------
    # Vectorised batch assembly: all samples padded to a common unroll
    # length T_max with a validity mask. One batched forward per unroll
    # step instead of (batch_size × unroll) tiny B=1 forwards.
    # -------------------------------------------------------------------
    samples = [s for s in batch if s.get("states")]
    B = len(samples)
    if B == 0:
        return None

    unroll = max(1, int(config.unroll_steps))
    vtrace_full = bool(getattr(config, "vtrace_full", True))
    obs_dim = int(np.asarray(samples[0]["states"][0], dtype=np.float32).reshape(-1).shape[0])
    K = int(len(samples[0]["actions"][0]))
    A_sizes = [int(net.action_sizes[h]) for h in range(K)]
    T_b = [min(len(s["states"]), unroll) for s in samples]
    T_max = max(T_b)

    states_np = np.zeros((B, T_max, obs_dim), dtype=np.float32)
    actions_np = np.zeros((B, T_max, K), dtype=np.int64)
    value_tg_np = np.zeros((B, T_max), dtype=np.float32)
    rewards_np = np.zeros((B, T_max), dtype=np.float32)
    valid_np = np.zeros((B, T_max), dtype=bool)
    target0_np = [np.zeros((B, A_sizes[h]), dtype=np.float32) for h in range(K)]
    beh_np = [np.zeros((B, T_max, A_sizes[h]), dtype=np.float32) for h in range(K)]
    beh_avail_np = np.zeros((B, T_max), dtype=bool)

    for b, s in enumerate(samples):
        n = T_b[b]
        s_states = s["states"]
        s_actions = s["actions"]
        s_rewards = s["rewards"]
        s_values = s["value_targets"]
        s_policies = s["policy_targets"]
        beh_seq = s.get("behavior_logits") or []
        for t in range(n):
            states_np[b, t] = np.asarray(s_states[t], dtype=np.float32).reshape(-1)[:obs_dim]
            actions_np[b, t] = np.asarray(s_actions[t], dtype=np.int64).reshape(-1)[:K]
            value_tg_np[b, t] = float(s_values[t])
            rewards_np[b, t] = float(s_rewards[t]) if t < len(s_rewards) else 0.0
            valid_np[b, t] = True
        for h in range(K):
            target0_np[h][b] = np.asarray(s_policies[0][h], dtype=np.float32).reshape(-1)[:A_sizes[h]]
        if vtrace_full and len(beh_seq) >= 1:
            for t in range(min(n, len(beh_seq))):
                beh = beh_seq[t]
                if not isinstance(beh, (list, tuple)) or len(beh) < K:
                    continue
                heads = [np.asarray(beh[h], dtype=np.float32).reshape(-1) for h in range(K)]
                if any(heads[h].size != A_sizes[h] for h in range(K)):
                    continue
                for h in range(K):
                    beh_np[h][b, t] = heads[h]
                beh_avail_np[b, t] = True

    states_t = torch.as_tensor(states_np, device=device)
    actions_t = torch.as_tensor(actions_np, device=device)
    value_tg_t = torch.as_tensor(value_tg_np, device=device)
    rewards_t = torch.as_tensor(rewards_np, device=device)
    valid_t = torch.as_tensor(valid_np, device=device)
    valid_f = valid_t.float()
    target0_t = [torch.as_tensor(target0_np[h], device=device) for h in range(K)]
    beh_t = [torch.as_tensor(beh_np[h], device=device) for h in range(K)]
    beh_avail_t = torch.as_tensor(beh_avail_np, device=device)

    # --- batched unroll: 1 forward per step ---
    obs0 = states_t[:, 0, :]
    logits0, value0, reward0, latent = net.initial_inference(obs0, masks_by_head=None)
    v_pred_steps = [value0]
    r_pred_steps = [reward0]
    pi_cur_steps: list[list[torch.Tensor]] = [
        [F.softmax(logits0[h], dim=1).detach() for h in range(K)]
    ]
    cons_per_sample = torch.zeros(B, device=device)

    for t in range(1, T_max):
        if t > tbptt_k:
            latent = latent.detach()
        act = actions_t[:, t - 1, :]
        logits_t, value_t, reward_t, latent = net.recurrent_inference(latent, act, masks_by_head=None)
        v_pred_steps.append(value_t)
        r_pred_steps.append(reward_t)
        pi_cur_steps.append([F.softmax(logits_t[h], dim=1).detach() for h in range(K)])
        if _target_enc is not None:
            obs_t = states_t[:, t, :]
            with torch.no_grad():
                target_proj = _target_enc.project_latent(_target_enc.encode(obs_t)).detach()
            pred_proj = net.project_latent(latent)
            cos = (pred_proj * target_proj).sum(dim=1)
            cons_per_sample = cons_per_sample + (1.0 - cos) * valid_f[:, t]

    V_pred = torch.stack(v_pred_steps, dim=1)   # (B, T_max) — carries grad (the value-loss fix)
    R_pred = torch.stack(r_pred_steps, dim=1)   # (B, T_max)

    # --- value loss (FIXED): regress network value preds onto V-trace targets ---
    gamma = float(getattr(config, "discount", 0.997) if hasattr(config, "discount") else 0.997)
    if vtrace_full:
        corrected = _vtrace_targets_batched(
            pi_cur_steps=pi_cur_steps, beh_logits_steps=beh_t, beh_avail=beh_avail_t,
            actions=actions_t, value_base=value_tg_t, rewards=rewards_t, valid=valid_t,
            rho_clip=float(getattr(config, "vtrace_rho_clip", 0.7)),
            c_clip=float(getattr(config, "vtrace_c_clip", 0.7)), gamma=gamma,
        )
    else:
        corrected = value_tg_t
    value_targets = corrected.detach()
    value_loss = (((V_pred - value_targets) ** 2) * valid_f).sum() / float(B)

    # --- reward loss: predicted reward at step t (t>=1) vs replay reward[t-1] ---
    reward_target = torch.zeros_like(R_pred)
    if T_max > 1:
        reward_target[:, 1:] = rewards_t[:, : T_max - 1]
    reward_loss = (((R_pred - reward_target) ** 2) * valid_f).sum() / float(B)

    # --- consistency loss (mean over samples of summed per-step 1-cos) ---
    consistency_loss = cons_per_sample.sum() / float(B)

    # --- policy loss: cross-entropy at t=0 with detached IS weight (as before) ---
    ce_b = torch.zeros(B, device=device)
    for h in range(K):
        tgt = target0_t[h]
        tgt = tgt / tgt.sum(dim=1, keepdim=True).clamp_min(1e-8)
        logp = F.log_softmax(logits0[h], dim=1)
        ce_b = ce_b + (-(tgt * logp).sum(dim=1))
    log_rho = torch.zeros(B, device=device)
    for h in range(K):
        a0 = actions_t[:, 0, h].clamp(0, logits0[h].shape[1] - 1)
        cur_p = F.softmax(logits0[h], dim=1).gather(1, a0.unsqueeze(1)).squeeze(1).clamp_min(1e-8)
        beh_p = F.softmax(beh_t[h][:, 0, :], dim=1).gather(1, a0.unsqueeze(1)).squeeze(1).clamp_min(1e-8)
        log_rho = log_rho + (torch.log(cur_p) - torch.log(beh_p))
    is_weight = torch.where(
        beh_avail_t[:, 0], torch.exp(log_rho).clamp(max=1.0), torch.ones(B, device=device)
    ).detach()
    policy_loss = (is_weight * ce_b).sum() / float(B)
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
