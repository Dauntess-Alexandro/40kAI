import torch
import torch.nn as nn
import torch.nn.functional as F
import collections
import numpy as np
import os
import json
from time import perf_counter


import random
import math

from core.models.memory import Transition
from core.engine.utils import distance

with open(os.path.abspath("hyperparams.json")) as j:
    data = json.loads(j.read())

EPS_START = data["eps_start"]
EPS_END = data["eps_end"]
EPS_DECAY = data["eps_decay"]
BATCH_SIZE = data["batch_size"]
GAMMA = data["gamma"]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def unwrap_env(env):
    return getattr(env, "unwrapped", env)


def c51_project_distribution(reward_vec, gamma_pow_vec, next_dist, support):
    n_batch = reward_vec.shape[0]
    n_atoms = support.shape[0]
    v_min = float(support[0].item())
    v_max = float(support[-1].item())
    delta_z = (v_max - v_min) / float(n_atoms - 1)
    tz = reward_vec.unsqueeze(1) + gamma_pow_vec.unsqueeze(1) * support.view(1, -1)
    tz = tz.clamp(v_min, v_max)
    b = (tz - v_min) / delta_z
    l = b.floor().long().clamp(0, n_atoms - 1)
    u = b.ceil().long().clamp(0, n_atoms - 1)
    m = torch.zeros_like(next_dist)
    offset = torch.arange(n_batch, device=next_dist.device).unsqueeze(1) * n_atoms
    m_flat = m.view(-1)
    next_flat = next_dist.view(-1)
    m_flat.index_add_(0, (l + offset).view(-1), (next_flat * (u.float() - b).view(-1)))
    m_flat.index_add_(0, (u + offset).view(-1), (next_flat * (b - l.float()).view(-1)))
    same = u.eq(l)
    if same.any():
        same_idx = (l + offset)[same].view(-1)
        same_mass = next_dist[same].view(-1)
        m_flat.index_add_(0, same_idx, same_mass)
    return m.clamp_min(1e-8)


def quantile_huber_loss(pred_quantiles, target_quantiles, taus, kappa=1.0):
    # pred_quantiles: [B, Nq], target_quantiles: [B, Nt], taus: [B, Nq, 1]
    td = target_quantiles.unsqueeze(1) - pred_quantiles.unsqueeze(2)  # [B, Nq, Nt]
    abs_td = td.abs()
    huber = torch.where(
        abs_td <= float(kappa),
        0.5 * td.pow(2),
        float(kappa) * (abs_td - 0.5 * float(kappa)),
    )
    quantile_weight = (taus - (td.detach() < 0).float()).abs()
    loss = (quantile_weight * huber / float(kappa)).mean(dim=(1, 2))
    return loss, td

def normalize_state_dict(state_dict):
    if not isinstance(state_dict, dict):
        return state_dict
    prefixes = ("_orig_mod.", "module.")
    needs_strip = any(
        any(key.startswith(prefix) for prefix in prefixes) for key in state_dict.keys()
    )
    if not needs_strip:
        return state_dict
    normalized = {}
    for key, value in state_dict.items():
        new_key = key
        for prefix in prefixes:
            if new_key.startswith(prefix):
                new_key = new_key[len(prefix):]
                break
        normalized[new_key] = value
    return normalized

def select_action(env, state, steps_done, policy_net, len_model, shoot_mask=None):
    force_greedy = os.getenv("FORCE_GREEDY", "0") == "1" or os.getenv("PLAY_NO_EXPLORATION", "0") == "1"
    noisy_disable_eps = os.getenv("NOISY_DISABLE_EPS", "1") == "1"
    sample = random.random()
    decay_steps = max(1.0, float(EPS_DECAY))
    progress = min(float(steps_done) / decay_steps, 1.0)
    eps_threshold = 0.0 if (force_greedy or noisy_disable_eps) else EPS_START + (EPS_END - EPS_START) * progress
    steps_done += 1
    dev = next(policy_net.parameters()).device

    
    if isinstance(state, collections.OrderedDict):
        state = np.array(list(state.values()), dtype=np.float32)
    elif isinstance(state, np.ndarray):
        state = state.astype(np.float32, copy=False)

    if not torch.is_tensor(state):
        state = torch.tensor(state, dtype=torch.float32, device=dev)
    else:
        state = state.to(dev)

    # делаем батч-измерение (batch dimension)
    if state.dim() == 1:
        state = state.unsqueeze(0)


    if hasattr(policy_net, "reset_noise") and not force_greedy:
        try:
            policy_net.reset_noise()
        except Exception:
            pass

    if force_greedy or sample > eps_threshold:
        with torch.no_grad():
            decision = policy_net(state)
            action = []
            for head_idx, head in enumerate(decision):
                head = head.squeeze(0)
                if head_idx == 2 and shoot_mask is not None:
                    mask = torch.as_tensor(shoot_mask, dtype=torch.bool, device=head.device)
                    if mask.numel() == head.numel() and mask.any():
                        masked_head = head.clone()
                        masked_head[~mask] = -1e9
                        action.append(int(masked_head.argmax().item()))
                        continue
                action.append(int(head.argmax().item()))
            return torch.tensor([action], device="cpu")
    else:
        sampled_action = env.action_space.sample()
        shoot_choice = sampled_action["shoot"]
        if shoot_mask is not None:
            mask = torch.as_tensor(shoot_mask, dtype=torch.bool)
            valid_indices = torch.where(mask)[0].tolist()
            if valid_indices:
                shoot_choice = random.choice(valid_indices)
        action_list = [
            sampled_action["move"],
            sampled_action["attack"],
            shoot_choice,
            sampled_action["charge"],
            sampled_action["use_cp"],
            sampled_action["cp_on"],
        ]
        for i in range(len_model):
            label = "move_num_" + str(i)
            action_list.append(sampled_action[label])
        action = torch.tensor([action_list], device="cpu")
        return action

def build_shoot_action_mask(env, log_fn=None, debug=False):
    env_unwrapped = unwrap_env(env)

    def maybe_log_mask_state(state_key, message):
        if log_fn is None:
            return
        last_state = getattr(env, "_last_shoot_mask_log_state", None)
        if last_state != state_key:
            env._last_shoot_mask_log_state = state_key
            log_fn(message)

    shoot_space = env_unwrapped.action_space.spaces["shoot"].n
    valid_lengths = []
    for i in range(len(env_unwrapped.unit_health)):
        if hasattr(env_unwrapped, "get_shoot_targets_for_unit"):
            valid_targets = env_unwrapped.get_shoot_targets_for_unit("model", i)
        else:
            if env_unwrapped.unit_health[i] <= 0:
                continue
            if env_unwrapped.unitFellBack[i]:
                continue
            if env_unwrapped.unitInAttack[i][0] == 1:
                continue
            if env_unwrapped.unit_weapon[i] == "None":
                continue
            valid_targets = []
            for j in range(len(env_unwrapped.enemy_health)):
                if (
                    distance(env_unwrapped.unit_coords[i], env_unwrapped.enemy_coords[j])
                    <= env_unwrapped.unit_weapon[i]["Range"]
                    and env_unwrapped.enemy_health[j] > 0
                    and env_unwrapped.enemyInAttack[j][0] == 0
                ):
                    valid_targets.append(j)
        if valid_targets:
            valid_lengths.append(len(valid_targets))
    if not valid_lengths:
        maybe_log_mask_state(
            ("none", "no_targets"),
            "[MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).",
        )
        return None
    min_len = min(valid_lengths)
    if min_len <= 0:
        maybe_log_mask_state(
            ("none", "zero_len"),
            "[MASK][SHOOT] Нулевая длина маски (маска не применяется).",
        )
        return None
    mask = torch.zeros(shoot_space, dtype=torch.bool)
    mask[:min_len] = True
    mask_state = ("mask", min_len, len(valid_lengths), shoot_space)
    maybe_log_mask_state(
        mask_state,
        "[MASK][SHOOT] "
        f"Доступные индексы: 0..{min_len - 1}, "
        f"юнитов с целями={len(valid_lengths)}, размер пространства={shoot_space}.",
    )
    if debug and log_fn is not None:
        log_fn(f"[MASK][SHOOT][DEBUG] Полная маска: {mask.tolist()}")
    return mask


def build_action_masks_by_head(env, len_model, log_fn=None, debug=False):
    """
    Унифицированный контракт масок для всех голов действия.
    Сейчас строгая маска есть только для shoot; остальные головы = all_true.
    """
    env_unwrapped = unwrap_env(env)
    ordered_keys = ["move", "attack", "shoot", "charge", "use_cp", "cp_on"]
    for i_u in range(int(len_model)):
        ordered_keys.append(f"move_num_{i_u}")

    masks = []
    shoot_mask = build_shoot_action_mask(env_unwrapped, log_fn=log_fn, debug=debug)
    fallback_count = 0
    for key in ordered_keys:
        sp = env_unwrapped.action_space.spaces[key]
        if hasattr(sp, "n"):
            size = int(sp.n)
        elif hasattr(sp, "nvec"):
            # В текущем проекте головы nvec не используются, но на всякий.
            size = int(sp.nvec[0])
        else:
            size = 1
        if key == "shoot" and shoot_mask is not None and len(shoot_mask) == size:
            mask = torch.as_tensor(shoot_mask, dtype=torch.bool).clone()
        else:
            mask = torch.ones(size, dtype=torch.bool)
        if not bool(mask.any()):
            mask[:] = True
            fallback_count += 1
        masks.append(mask)
    if fallback_count > 0 and log_fn is not None:
        log_fn(
            f"[MASK][ALL_HEADS] Пустые маски заменены на all_true: {fallback_count}. "
            "Где: model/utils.py build_action_masks_by_head."
        )
    return masks

def convertToDict(action):
    naction = action.numpy()[0]
    action_dict = {
        'move': naction[0],
        'attack': naction[1],
        'shoot': naction[2],
        'charge': naction[3],
        'use_cp': naction[4],
        'cp_on': naction[5]
    }
    for i in range(len(naction)-6):
        label = "move_num_"+str(i)
        action_dict[label] = naction[i+6]
    return action_dict

def optimize_model(
    policy_net,
    target_net,
    optimizer,
    memory,
    n_obs,
    double_dqn_enabled=True,
    per_enabled=False,
    per_beta=0.4,
    per_eps=1e-6,
    use_amp=False,
    scaler=None,
    pin_memory=False,
    prefetch=False,
):
    if len(memory) < BATCH_SIZE:
        return None

    # ВАЖНО: берем device прямо от сети (cuda или cpu)
    dev = next(policy_net.parameters()).device
    amp_enabled = bool(use_amp and dev.type == "cuda")

    def _to_device(tensor):
        if tensor is None:
            return None
        if tensor.device == dev:
            return tensor
        if pin_memory and tensor.device.type == "cpu" and dev.type == "cuda":
            return tensor.pin_memory().to(dev, non_blocking=True)
        return tensor.to(dev)

    sample_start = perf_counter()
    if per_enabled:
        transitions, indices, weights = memory.sample(BATCH_SIZE, beta=per_beta, prefetch=prefetch)
        if not transitions:
            return None
    else:
        transitions = memory.sample(BATCH_SIZE, prefetch=prefetch)
        indices = None
        weights = None
    sample_time = perf_counter() - sample_start
    batch = Transition(*zip(*transitions))

    desired_shape = (1, n_obs)

    # ---- state_batch ----
    state_tensors = []
    for s in batch.state:
        if s is None:
            state_tensors.append(torch.zeros(desired_shape, device=dev, dtype=torch.float32))
        else:
            state_tensors.append(_to_device(s).view(desired_shape))
    state_batch = torch.cat(state_tensors, dim=0)  # [B, n_obs]

    # ---- action_batch / reward_batch (на тот же dev!) ----
    action_tensors = [_to_device(a) for a in batch.action]
    reward_tensors = [_to_device(r) for r in batch.reward]
    action_batch = torch.cat(action_tensors).long()  # индексы ОБЯЗАТЕЛЬНО long и на dev
    reward_batch = torch.cat(reward_tensors).float().view(-1)  # [B]
    n_step_batch = torch.tensor(batch.n_step, device=dev, dtype=torch.float32)  # [B]

    # ---- next states ----
    non_final_mask = torch.tensor([s is not None for s in batch.next_state], device=dev, dtype=torch.bool)

    non_final_next_states = None
    non_final_next_shoot_masks = None
    if non_final_mask.any():
        non_final_next_states = torch.cat([_to_device(s) for s in batch.next_state if s is not None], dim=0)
        non_final_next_shoot_masks = [
            m for m, s in zip(batch.next_shoot_mask, batch.next_state) if s is not None
        ]

    def _gather_selected_q(head_outputs, actions):
        arr_local = []
        for head_idx, head in enumerate(head_outputs):
            arr_local.append(head.gather(1, actions[:, head_idx].unsqueeze(1)))
        return torch.cat(arr_local, dim=1)

    def _build_shoot_mask(mask_source, width):
        if mask_source is None:
            return None
        mask_list = []
        for m in mask_source:
            if m is None:
                mask_list.append(torch.ones(width, device=dev, dtype=torch.bool))
            else:
                mask_list.append(torch.as_tensor(m, dtype=torch.bool, device=dev))
        return torch.stack(mask_list, dim=0)

    def _select_next_actions_from_q(q_heads, shoot_masks):
        acts = [h.argmax(1) for h in q_heads]
        if shoot_masks is not None and len(q_heads) > 2:
            shoot_mask = _build_shoot_mask(shoot_masks, q_heads[2].shape[1])
            if shoot_mask is not None and shoot_mask.shape == q_heads[2].shape:
                valid_any = shoot_mask.any(dim=1)
                masked_shoot = q_heads[2].clone()
                masked_shoot[~shoot_mask] = -1e9
                masked_shoot[~valid_any] = q_heads[2][~valid_any]
                acts[2] = masked_shoot.argmax(1)
        return acts

    forward_start = perf_counter()
    if hasattr(policy_net, "reset_noise"):
        policy_net.reset_noise()
    if hasattr(target_net, "reset_noise"):
        target_net.reset_noise()

    dist_type = str(getattr(policy_net, "distributional", "")).lower()
    use_iqn = dist_type == "iqn"
    use_c51 = dist_type == "c51"

    if use_iqn:
        iqn_n = int(getattr(policy_net, "iqn_num_quantiles", 32))
        iqn_n_tgt = int(getattr(policy_net, "iqn_num_target_quantiles", 32))
        iqn_kappa = float(os.getenv("IQN_KAPPA", "1.0"))
        with torch.autocast(device_type=dev.type, dtype=torch.float16, enabled=amp_enabled):
            online_quantiles, taus = policy_net.iqn(state_batch, num_quantiles=iqn_n, return_taus=True)
        selected_quantiles = []
        for head_idx, head_q in enumerate(online_quantiles):
            idx = action_batch[:, head_idx].view(-1, 1, 1).expand(-1, 1, head_q.shape[2])
            selected_quantiles.append(head_q.gather(1, idx).squeeze(1))

        num_heads = len(selected_quantiles)
        target_quantiles = torch.zeros((BATCH_SIZE, num_heads, iqn_n_tgt), device=dev, dtype=torch.float32)
        next_state_values = torch.zeros((BATCH_SIZE, num_heads), device=dev, dtype=torch.float32)
        with torch.no_grad():
            if non_final_next_states is not None:
                if double_dqn_enabled:
                    policy_next_q = policy_net(non_final_next_states)
                    next_actions = _select_next_actions_from_q(policy_next_q, non_final_next_shoot_masks)
                else:
                    target_next_q = target_net(non_final_next_states)
                    next_actions = _select_next_actions_from_q(target_next_q, non_final_next_shoot_masks)
                target_next_quantiles = target_net.iqn(non_final_next_states, num_quantiles=iqn_n_tgt, return_taus=False)
                gamma_n_nf = (GAMMA ** n_step_batch[non_final_mask]).float()
                reward_nf = reward_batch[non_final_mask]
                for head_idx, head_q in enumerate(target_next_quantiles):
                    act = next_actions[head_idx].view(-1, 1, 1).expand(-1, 1, head_q.shape[2])
                    chosen = head_q.gather(1, act).squeeze(1).float()
                    target_quantiles[non_final_mask, head_idx, :] = (
                        reward_nf.unsqueeze(1) + gamma_n_nf.unsqueeze(1) * chosen
                    )
                    next_state_values[non_final_mask, head_idx] = chosen.mean(dim=1)
        if (~non_final_mask).any():
            terminal_idx = torch.where(~non_final_mask)[0]
            terminal_reward = reward_batch[terminal_idx].float()
            target_quantiles[terminal_idx, :, :] = terminal_reward.view(-1, 1, 1)

        per_head_losses = []
        per_head_td = []
        for head_idx in range(num_heads):
            loss_i, td_i = quantile_huber_loss(
                selected_quantiles[head_idx].float(),
                target_quantiles[:, head_idx, :],
                taus.float(),
                kappa=iqn_kappa,
            )
            per_head_losses.append(loss_i)
            per_head_td.append(td_i.abs().mean(dim=(1, 2)))
        stacked_loss = torch.stack(per_head_losses, dim=1)
        per_sample_loss = stacked_loss.mean(dim=1)
        td_errors = torch.stack(per_head_td, dim=1).mean(dim=1)

        if per_enabled:
            weight_t = torch.tensor(weights, device=dev, dtype=torch.float32)
            loss = (per_sample_loss * weight_t).mean()
            new_priorities = td_errors.detach().cpu().numpy() + per_eps
            memory.update_priorities(indices, new_priorities)
            per_stats = {
                "priority_mean": float(new_priorities.mean()),
                "priority_max": float(new_priorities.max()),
                "is_weight_mean": float(weight_t.mean().item()),
                "is_weight_max": float(weight_t.max().item()),
                "td_error_mean": float(td_errors.mean().item()),
                "td_error_max": float(td_errors.max().item()),
            }
        else:
            loss = per_sample_loss.mean()
            per_stats = None
        expected_state_action_values = reward_batch.unsqueeze(1) + ((GAMMA ** n_step_batch).unsqueeze(1) * next_state_values)
        dist_stats = {
            "quantile_loss_mean": float(per_sample_loss.mean().item()),
            "quantile_loss_max": float(per_sample_loss.max().item()),
            "td_quantile_mean": float(td_errors.mean().item()),
            "td_quantile_max": float(td_errors.max().item()),
            "n_quantiles": int(iqn_n),
            "n_target_quantiles": int(iqn_n_tgt),
        }
    elif use_c51:
        with torch.autocast(device_type=dev.type, dtype=torch.float16, enabled=amp_enabled):
            dist_outputs = policy_net.dist(state_batch)
        selected_log_probs = []
        for head_idx, head_logits in enumerate(dist_outputs):
            action_idx = action_batch[:, head_idx].view(-1, 1, 1).expand(-1, 1, head_logits.shape[-1])
            chosen_logits = head_logits.gather(1, action_idx).squeeze(1)
            selected_log_probs.append(F.log_softmax(chosen_logits, dim=-1))

        num_heads = len(dist_outputs)
        n_atoms = int(getattr(policy_net, "num_atoms", 51))
        support = policy_net.support.to(dev)
        target_proj = torch.zeros((BATCH_SIZE, num_heads, n_atoms), device=dev, dtype=torch.float32)
        next_state_values = torch.zeros((BATCH_SIZE, num_heads), device=dev, dtype=torch.float32)

        with torch.no_grad():
            if non_final_next_states is not None:
                if double_dqn_enabled:
                    policy_next_q = policy_net(non_final_next_states)
                    next_actions = _select_next_actions_from_q(policy_next_q, non_final_next_shoot_masks)
                else:
                    if hasattr(target_net, "reset_noise"):
                        target_net.reset_noise()
                    target_next_q = target_net(non_final_next_states)
                    next_actions = _select_next_actions_from_q(target_next_q, non_final_next_shoot_masks)

                if hasattr(target_net, "reset_noise"):
                    target_net.reset_noise()
                target_next_dist_logits = target_net.dist(non_final_next_states)
                gamma_n_nf = (GAMMA ** n_step_batch[non_final_mask]).float()
                reward_nf = reward_batch[non_final_mask]

                for head_idx, head_logits in enumerate(target_next_dist_logits):
                    act = next_actions[head_idx].view(-1, 1, 1).expand(-1, 1, n_atoms)
                    chosen_logits = head_logits.gather(1, act).squeeze(1)
                    chosen_dist = torch.softmax(chosen_logits, dim=-1)
                    projected = c51_project_distribution(reward_nf, gamma_n_nf, chosen_dist, support)
                    target_proj[non_final_mask, head_idx] = projected
                    next_state_values[non_final_mask, head_idx] = (chosen_dist * support.view(1, -1)).sum(dim=1)

        non_final_reward = reward_batch[~non_final_mask]
        if non_final_reward.numel() > 0:
            terminal_idx = torch.where(~non_final_mask)[0]
            for idx_t, r_val in zip(terminal_idx.tolist(), non_final_reward.tolist()):
                atom_idx = torch.argmin((support - float(r_val)).abs()).item()
                target_proj[idx_t, :, atom_idx] = 1.0

        ce_per_head = []
        for head_idx, log_p in enumerate(selected_log_probs):
            ce = -(target_proj[:, head_idx, :] * log_p.float()).sum(dim=1)
            ce_per_head.append(ce)
        per_sample_loss = torch.stack(ce_per_head, dim=1).mean(dim=1)
        if per_enabled:
            weight_t = torch.tensor(weights, device=dev, dtype=torch.float32)
            loss = (per_sample_loss * weight_t).mean()
            td_errors = per_sample_loss.detach()
            new_priorities = td_errors.cpu().numpy() + per_eps
            memory.update_priorities(indices, new_priorities)
            per_stats = {
                "priority_mean": float(new_priorities.mean()),
                "priority_max": float(new_priorities.max()),
                "is_weight_mean": float(weight_t.mean().item()),
                "is_weight_max": float(weight_t.max().item()),
                "td_error_mean": float(td_errors.mean().item()),
                "td_error_max": float(td_errors.max().item()),
            }
        else:
            loss = per_sample_loss.mean()
            per_stats = None
        expected_state_action_values = reward_batch.unsqueeze(1) + ((GAMMA ** n_step_batch).unsqueeze(1) * next_state_values)
        dist_stats = {
            "ce_mean": float(per_sample_loss.mean().item()),
            "ce_max": float(per_sample_loss.max().item()),
            "atoms": int(n_atoms),
            "v_min": float(support[0].item()),
            "v_max": float(support[-1].item()),
        }
    else:
        with torch.autocast(device_type=dev.type, dtype=torch.float16, enabled=amp_enabled):
            state_action_values = policy_net(state_batch)
        selected_action_values = _gather_selected_q(state_action_values, action_batch)
        next_state_values = torch.zeros((BATCH_SIZE, selected_action_values.shape[1]), device=dev, dtype=torch.float32)
        with torch.no_grad():
            if non_final_next_states is not None:
                with torch.autocast(device_type=dev.type, dtype=torch.float16, enabled=amp_enabled):
                    target_next = target_net(non_final_next_states)
                    if double_dqn_enabled:
                        policy_next = policy_net(non_final_next_states)
                        next_actions = _select_next_actions_from_q(policy_next, non_final_next_shoot_masks)
                        next_q = [tgt.gather(1, act.unsqueeze(1)).squeeze(1) for tgt, act in zip(target_next, next_actions)]
                        max_per_head = torch.stack(next_q, dim=1)
                    else:
                        masked_targets = []
                        for head_idx, head in enumerate(target_next):
                            if head_idx == 2 and non_final_next_shoot_masks is not None:
                                shoot_mask = _build_shoot_mask(non_final_next_shoot_masks, head.shape[1])
                                if shoot_mask is not None and shoot_mask.shape == head.shape:
                                    valid_any = shoot_mask.any(dim=1)
                                    masked_head = head.clone()
                                    masked_head[~shoot_mask] = -1e9
                                    masked_head[~valid_any] = head[~valid_any]
                                    masked_targets.append(masked_head.max(1).values)
                                    continue
                            masked_targets.append(head.max(1).values)
                        max_per_head = torch.stack(masked_targets, dim=1)
                    next_state_values[non_final_mask] = max_per_head.float()
        gamma_n = GAMMA ** n_step_batch
        expected_state_action_values = reward_batch.unsqueeze(1) + (gamma_n.unsqueeze(1) * next_state_values)
        if per_enabled:
            with torch.autocast(device_type=dev.type, dtype=torch.float16, enabled=amp_enabled):
                loss_per_element = F.smooth_l1_loss(
                    selected_action_values, expected_state_action_values, reduction="none"
                )
                per_sample_loss = loss_per_element.mean(dim=1)
                weight_t = torch.tensor(weights, device=dev, dtype=torch.float32)
                loss = (per_sample_loss * weight_t).mean()
                td_errors = (selected_action_values - expected_state_action_values).abs().mean(dim=1)
                new_priorities = td_errors.detach().cpu().numpy() + per_eps
            memory.update_priorities(indices, new_priorities)
            per_stats = {
                "priority_mean": float(new_priorities.mean()),
                "priority_max": float(new_priorities.max()),
                "is_weight_mean": float(weight_t.mean().item()),
                "is_weight_max": float(weight_t.max().item()),
                "td_error_mean": float(td_errors.mean().item()),
                "td_error_max": float(td_errors.max().item()),
            }
        else:
            criterion = nn.SmoothL1Loss()
            with torch.autocast(device_type=dev.type, dtype=torch.float16, enabled=amp_enabled):
                loss = criterion(selected_action_values, expected_state_action_values)
            per_stats = None
        dist_stats = None

    optimizer.zero_grad()
    backward_start = perf_counter()
    if amp_enabled and scaler is not None:
        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
        scaler.step(optimizer)
        scaler.update()
    else:
        loss.backward()
        torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
        optimizer.step()
    backward_time = perf_counter() - backward_start
    forward_time = perf_counter() - forward_start

    return {
        "loss": loss.item(),
        "td_target_mean": expected_state_action_values.mean().item(),
        "td_target_max": expected_state_action_values.max().item(),
        "per_stats": per_stats,
        "dist_stats": dist_stats,
        "timing": {
            "sample_s": sample_time,
            "forward_s": forward_time,
            "backward_s": backward_time,
        },
    }
