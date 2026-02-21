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

from model.memory import Transition
from gym_mod.engine.utils import distance

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
    sample = random.random()
    decay_steps = max(1.0, float(EPS_DECAY))
    progress = min(float(steps_done) / decay_steps, 1.0)
    eps_threshold = 0.0 if force_greedy else EPS_START + (EPS_END - EPS_START) * progress
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
    action_batch = _to_device(torch.cat(batch.action)).long()  # индексы ОБЯЗАТЕЛЬНО long и на dev
    reward_batch = _to_device(torch.cat(batch.reward)).float().view(-1)  # [B]
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

    forward_start = perf_counter()
    # ---- Q(s,a) ----
    with torch.autocast(device_type=dev.type, dtype=torch.float16, enabled=amp_enabled):
        state_action_values = policy_net(state_batch)
    move_action, attack_action, shoot_action, charge_action, use_cp_action, cp_on_action, *move_actions = state_action_values

    arr = [
        move_action.gather(1, action_batch[:, 0].unsqueeze(1)),
        attack_action.gather(1, action_batch[:, 1].unsqueeze(1)),
        shoot_action.gather(1, action_batch[:, 2].unsqueeze(1)),
        charge_action.gather(1, action_batch[:, 3].unsqueeze(1)),
        use_cp_action.gather(1, action_batch[:, 4].unsqueeze(1)),
        cp_on_action.gather(1, action_batch[:, 5].unsqueeze(1)),
    ]
    for i in range(len(move_actions)):
        arr.append(move_actions[i].gather(1, action_batch[:, i + 6].unsqueeze(1)))

    selected_action_values = torch.cat(arr, dim=1)  # [B, num_heads]

    # ---- max_a' Q_target(s', a') per head ----
    next_state_values = torch.zeros((BATCH_SIZE, selected_action_values.shape[1]), device=dev, dtype=torch.float32)

    with torch.no_grad():
        if non_final_next_states is not None:
            with torch.autocast(device_type=dev.type, dtype=torch.float16, enabled=amp_enabled):
                target_next = target_net(non_final_next_states)  # list of [N, n_i]
                if double_dqn_enabled:
                    policy_next = policy_net(non_final_next_states)
                    next_actions = [h.argmax(1) for h in policy_next]  # list of [N]
                    if non_final_next_shoot_masks is not None:
                        mask_list = []
                        for m in non_final_next_shoot_masks:
                            if m is None:
                                mask_list.append(torch.ones(policy_next[2].shape[1], device=dev, dtype=torch.bool))
                            else:
                                mask_list.append(torch.as_tensor(m, dtype=torch.bool, device=dev))
                        shoot_mask = torch.stack(mask_list, dim=0)
                        if shoot_mask.shape == policy_next[2].shape and shoot_mask.numel() > 0:
                            valid_any = shoot_mask.any(dim=1)
                            masked_shoot = policy_next[2].clone()
                            masked_shoot[~shoot_mask] = -1e9
                            masked_shoot[~valid_any] = policy_next[2][~valid_any]
                            next_actions[2] = masked_shoot.argmax(1)
                    next_q = [
                        tgt.gather(1, act.unsqueeze(1)).squeeze(1)
                        for tgt, act in zip(target_next, next_actions)
                    ]
                    max_per_head = torch.stack(next_q, dim=1)  # [N, num_heads]
                else:
                    masked_targets = []
                    for head_idx, head in enumerate(target_next):
                        if head_idx == 2 and non_final_next_shoot_masks is not None:
                            mask_list = []
                            for m in non_final_next_shoot_masks:
                                if m is None:
                                    mask_list.append(torch.ones(head.shape[1], device=dev, dtype=torch.bool))
                                else:
                                    mask_list.append(torch.as_tensor(m, dtype=torch.bool, device=dev))
                            shoot_mask = torch.stack(mask_list, dim=0)
                            if shoot_mask.numel() > 0 and shoot_mask.shape == head.shape:
                                valid_any = shoot_mask.any(dim=1)
                                masked_head = head.clone()
                                masked_head[~shoot_mask] = -1e9
                                masked_head[~valid_any] = head[~valid_any]
                                masked_targets.append(masked_head.max(1).values)
                                continue
                        masked_targets.append(head.max(1).values)
                    max_per_head = torch.stack(masked_targets, dim=1)  # [N, num_heads]
                next_state_values[non_final_mask] = max_per_head.float()

    gamma_n = GAMMA ** n_step_batch
    expected_state_action_values = reward_batch.unsqueeze(1) + (gamma_n.unsqueeze(1) * next_state_values)  # [B, num_heads]

    if per_enabled:
        with torch.autocast(device_type=dev.type, dtype=torch.float16, enabled=amp_enabled):
            loss_per_element = F.smooth_l1_loss(
                selected_action_values, expected_state_action_values, reduction="none"
            )
            per_sample_loss = loss_per_element.mean(dim=1)  # [B]
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
        "timing": {
            "sample_s": sample_time,
            "forward_s": forward_time,
            "backward_s": backward_time,
        },
    }
