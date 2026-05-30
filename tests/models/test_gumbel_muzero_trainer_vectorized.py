"""Tests for the vectorized + value-loss-fixed GMZ learner step.

Goals being verified:
  1. value head now receives a real gradient (the bug fix);
  2. the policy / reward / consistency loss components are unchanged vs the
     original per-sample reference implementation (the refactor preserves them);
  3. every learnable head receives gradient (batching didn't detach anything);
  4. the step is deterministic;
  5. repeatedly stepping on a fixed batch drives total loss down (it learns).

`reference_step` below is a verbatim copy of the ORIGINAL per-sample
implementation (the one with the value-loss-detached bug). It serves only as a
numerical oracle for the loss components that must NOT change.
"""

from __future__ import annotations

import copy
import random

import numpy as np
import torch
import torch.nn.functional as F

from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.gumbel_muzero_replay import GMZTransition, GumbelMuZeroReplayBuffer
from core.models.gumbel_muzero_trainer import (
    GumbelMuZeroTrainConfig,
    train_gumbel_muzero_step,
    _policy_ce_loss,
    _vtrace_targets,
)


# ---------------------------------------------------------------------------
# Oracle: verbatim copy of the original per-sample implementation.
# ---------------------------------------------------------------------------
def reference_step(*, net, optimizer, replay, config, device,
                   current_policy_version=0, scheduler=None, ema_target=None):
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
        vtrace_full = bool(getattr(config, "vtrace_full", True))
        values_BT_list = []
        actions_BT_list = []
        pi_cur_all_steps = []
        behavior_logits_seq = sample.get("behavior_logits", []) or []
        obs0 = torch.as_tensor(states[0], dtype=torch.float32, device=device).unsqueeze(0)
        logits0, value0, reward0, latent = net.initial_inference(obs0, masks_by_head=None)
        pi_cur0 = [F.softmax(l, dim=1).squeeze(0) for l in logits0]
        pi_cur_all_steps = [[pi_cur0[h]] for h in range(len(pi_cur0))]
        values_BT_list.append(float(values[0]))
        actions_BT_list.append(actions[0])
        total_reward_loss = total_reward_loss + F.mse_loss(reward0, torch.tensor([0.0], device=device))
        for t in range(1, min(len(states), max(1, int(config.unroll_steps)))):
            if t > tbptt_k:
                latent = latent.detach()
            action_t = torch.as_tensor(actions[t - 1], dtype=torch.long, device=device).unsqueeze(0)
            logits_t, value_t, reward_t, latent = net.recurrent_inference(latent, action_t, masks_by_head=None)
            pi_cur_t = [F.softmax(l, dim=1).squeeze(0) for l in logits_t]
            for h in range(len(pi_cur_t)):
                pi_cur_all_steps[h].append(pi_cur_t[h])
            values_BT_list.append(float(value_t.item()))
            actions_BT_list.append(actions[t] if t < len(actions) else actions[-1])
            total_reward_loss = total_reward_loss + F.mse_loss(reward_t, torch.tensor([float(rewards[t - 1])], device=device))
            if _target_enc is not None and t < len(states):
                obs_t = torch.as_tensor(states[t], dtype=torch.float32, device=device).unsqueeze(0)
                with torch.no_grad():
                    _enc = _target_enc
                    target_proj = _enc.project_latent(_enc.encode(obs_t)).detach()
                pred_proj = net.project_latent(latent)
                total_consistency_loss = total_consistency_loss + (1.0 - (pred_proj * target_proj).sum(dim=1).mean())
        T = len(values_BT_list)
        K = len(actions[0]) if actions else 1
        values_BT = torch.tensor([values_BT_list], dtype=torch.float32, device=device)
        actions_np = np.array(actions_BT_list, dtype=np.int64)
        actions_BT = torch.tensor(actions_np, dtype=torch.long, device=device).unsqueeze(0)
        rewards_np = np.array([float(r) for r in rewards], dtype=np.float32)[:T - 1] if T > 1 else np.zeros(0, dtype=np.float32)
        rewards_BT = torch.tensor([rewards_np], dtype=torch.float32, device=device) if rewards_np.size > 0 else torch.zeros((1, max(0, T - 1)), dtype=torch.float32, device=device)
        valid_BT = torch.ones((1, T), dtype=torch.bool, device=device)
        if vtrace_full and len(behavior_logits_seq) >= 1:
            rho_clip = float(getattr(config, "vtrace_rho_clip", 0.7))
            c_clip = float(getattr(config, "vtrace_c_clip", 0.7))
            gamma = float(getattr(config, "discount", 0.997) if hasattr(config, "discount") else 0.997)
            pi_beh_list = []
            for step_idx in range(min(T, len(behavior_logits_seq))):
                beh = behavior_logits_seq[step_idx]
                if isinstance(beh, (list, tuple)):
                    pi_beh_list.append([np.asarray(x, dtype=np.float32) for x in beh])
                elif isinstance(beh, np.ndarray) and beh.ndim == 0:
                    pi_beh_list.append([])
                else:
                    pi_beh_list.append([])
            pi_cur_list = [torch.stack(pi_cur_all_steps[h], dim=0) for h in range(K)]
            corrected_values = _vtrace_targets(
                pi_cur_list=pi_cur_list, pi_beh_list=pi_beh_list, actions_BT=actions_BT,
                values_BT=values_BT, rewards_BT=rewards_BT, valid_BT=valid_BT,
                rho_clip=rho_clip, c_clip=c_clip, gamma=gamma,
            )
        else:
            corrected_values = values_BT
        logits_for_policy = [l.squeeze(0) for l in logits0]
        beh0 = behavior_logits_seq[0] if behavior_logits_seq else []
        is_weight_scalar = 1.0
        if beh0:
            log_rho = torch.tensor(0.0, device=device)
            for h in range(len(logits_for_policy)):
                pi_cur_h = F.softmax(logits_for_policy[h], dim=0)
                beh_h = torch.as_tensor(np.asarray(beh0[h], dtype=np.float32), device=device)
                pi_beh_h = F.softmax(beh_h, dim=0)
                a_h = actions[0][h] if h < len(actions[0]) else 0
                log_rho = log_rho + (torch.log(pi_cur_h[a_h].clamp_min(1e-8)) - torch.log(pi_beh_h[a_h].clamp_min(1e-8)))
            is_weight_scalar = float(torch.exp(log_rho.detach()).clamp(max=1.0))
        total_policy_loss = total_policy_loss + _policy_ce_loss(logits0, policies[0], device=device) * is_weight_scalar
        for t in range(T):
            target_v = corrected_values[0, t].item()
            total_value_loss = total_value_loss + F.mse_loss(
                torch.tensor([values_BT_list[t]], device=device),
                torch.tensor([target_v], device=device),
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
    loss = (policy_loss + float(config.value_loss_weight) * value_loss
            + float(config.reward_loss_weight) * reward_loss
            + _consistency_w * consistency_loss + float(config.l2_weight) * l2)
    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(net.parameters(), float(config.max_grad_norm))
    optimizer.step()
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


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
OBS_DIM = 6
ACTION_SIZES = [3, 2, 4]
K = len(ACTION_SIZES)


def _make_net(seed: int = 0) -> GumbelMuZeroNet:
    torch.manual_seed(seed)
    return GumbelMuZeroNet(
        obs_dim=OBS_DIM, action_sizes=ACTION_SIZES,
        latent_dim=32, hidden_dim=32, num_layers=1, action_embed_dim=8,
    )


def _transition(idx: int, done: bool) -> GMZTransition:
    rng = np.random.RandomState(1000 + idx)
    return GMZTransition(
        state=rng.randn(OBS_DIM).astype(np.float32),
        action=np.array([idx % 3, idx % 2, idx % 4], dtype=np.int64),
        reward=float(0.1 * ((idx % 5) - 2)),
        done=bool(done),
        policy_targets=[
            np.array([0.5, 0.3, 0.2], dtype=np.float32),
            np.array([0.4, 0.6], dtype=np.float32),
            np.array([0.1, 0.2, 0.3, 0.4], dtype=np.float32),
        ],
        behavior_logits=[
            rng.randn(3).astype(np.float32),
            rng.randn(2).astype(np.float32),
            rng.randn(4).astype(np.float32),
        ],
        value_target=float(0.5 if idx % 2 == 0 else -0.5),
        policy_version=1,
    )


def _make_replay(n: int = 12, done_at=(5,)) -> GumbelMuZeroReplayBuffer:
    replay = GumbelMuZeroReplayBuffer(capacity=64)
    for i in range(n):
        replay.push(_transition(i, done=(i in done_at)))
    return replay


def _config(batch_size: int = 8, l2_weight: float = 1e-6) -> GumbelMuZeroTrainConfig:
    return GumbelMuZeroTrainConfig(
        lr=3e-4, batch_size=batch_size, unroll_steps=4, tbptt_truncate=3,
        value_loss_weight=1.0, reward_loss_weight=1.0, consistency_loss_weight=1.0,
        l2_weight=l2_weight, max_grad_norm=0.5, vtrace_full=True,
    )


def _grad_norm(params) -> float:
    total = 0.0
    for p in params:
        if p.grad is not None:
            total += float(p.grad.detach().pow(2).sum().item())
    return total ** 0.5


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_value_head_receives_gradient():
    """The fix: value loss must produce a real gradient on the value head."""
    net = _make_net()
    opt = torch.optim.SGD(net.parameters(), lr=0.0)  # lr=0 so weights don't move
    replay = _make_replay()
    device = torch.device("cpu")
    random.seed(0)
    # l2_weight=0 so the value head can ONLY get gradient from the value loss
    # (it is a leaf head, fed by nothing else).
    info = train_gumbel_muzero_step(
        net=net, optimizer=opt, replay=replay, config=_config(l2_weight=0.0),
        device=device, current_policy_version=1,
    )
    assert info is not None
    vh_grad = _grad_norm(net.value_head.parameters())
    assert vh_grad > 1e-8, f"value head got no gradient (grad_norm={vh_grad})"


def test_all_heads_receive_gradient():
    net = _make_net()
    opt = torch.optim.SGD(net.parameters(), lr=0.0)
    replay = _make_replay()
    device = torch.device("cpu")
    random.seed(0)
    train_gumbel_muzero_step(
        net=net, optimizer=opt, replay=replay, config=_config(l2_weight=0.0),
        device=device, current_policy_version=1,
    )
    assert _grad_norm(net.value_head.parameters()) > 1e-8, "value head"
    assert _grad_norm(net.reward_head.parameters()) > 1e-8, "reward head"
    assert _grad_norm(net.policy_heads.parameters()) > 1e-8, "policy heads"
    assert _grad_norm(net.next_latent_head.parameters()) > 1e-8, "dynamics"
    assert _grad_norm(net.repr_output_fc.parameters()) > 1e-8, "encoder"


def test_unchanged_loss_components_match_reference():
    """policy / reward / consistency must be numerically identical to the
    original per-sample implementation (only value loss is allowed to differ)."""
    device = torch.device("cpu")
    cfg = _config()

    net_ref = _make_net(seed=7)
    net_new = copy.deepcopy(net_ref)  # identical weights
    opt_ref = torch.optim.SGD(net_ref.parameters(), lr=0.0)
    opt_new = torch.optim.SGD(net_new.parameters(), lr=0.0)

    random.seed(123)
    ref = reference_step(net=net_ref, optimizer=opt_ref, replay=_make_replay(),
                         config=cfg, device=device, current_policy_version=1)
    random.seed(123)
    new = train_gumbel_muzero_step(net=net_new, optimizer=opt_new, replay=_make_replay(),
                                   config=cfg, device=device, current_policy_version=1)

    assert ref is not None and new is not None
    assert abs(ref["policy_loss"] - new["policy_loss"]) < 1e-4, (ref["policy_loss"], new["policy_loss"])
    assert abs(ref["reward_loss"] - new["reward_loss"]) < 1e-4, (ref["reward_loss"], new["reward_loss"])
    assert abs(ref["consistency_loss"] - new["consistency_loss"]) < 1e-4, (ref["consistency_loss"], new["consistency_loss"])


def test_deterministic():
    device = torch.device("cpu")
    cfg = _config()
    net1 = _make_net(seed=3)
    net2 = copy.deepcopy(net1)
    opt1 = torch.optim.SGD(net1.parameters(), lr=0.0)
    opt2 = torch.optim.SGD(net2.parameters(), lr=0.0)
    random.seed(55)
    a = train_gumbel_muzero_step(net=net1, optimizer=opt1, replay=_make_replay(),
                                 config=cfg, device=device, current_policy_version=1)
    random.seed(55)
    b = train_gumbel_muzero_step(net=net2, optimizer=opt2, replay=_make_replay(),
                                 config=cfg, device=device, current_policy_version=1)
    for k in a:
        assert abs(a[k] - b[k]) < 1e-6, (k, a[k], b[k])


def test_overfit_reduces_loss():
    """Stepping repeatedly on a small fixed replay must drive total loss down,
    proving the value-loss fix gives a usable learning signal."""
    device = torch.device("cpu")
    net = _make_net(seed=11)
    cfg = _config(batch_size=8)
    opt = torch.optim.Adam(net.parameters(), lr=1e-2)
    replay = _make_replay(n=8, done_at=())

    random.seed(0)
    first = train_gumbel_muzero_step(net=net, optimizer=opt, replay=replay,
                                     config=cfg, device=device, current_policy_version=1)
    last = first
    for _ in range(60):
        random.seed(0)
        last = train_gumbel_muzero_step(net=net, optimizer=opt, replay=replay,
                                        config=cfg, device=device, current_policy_version=1)
    assert last["loss"] < first["loss"] * 0.7, (first["loss"], last["loss"])
    assert last["value_loss"] < first["value_loss"], (first["value_loss"], last["value_loss"])
