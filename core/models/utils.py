import collections
import json
import os
import random
from time import perf_counter

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from core.engine.utils import distance
from core.models.action_contract import action_tensor_to_dict, ordered_action_keys
from core.models.memory import Transition

with open(os.path.abspath("hyperparams.json")) as j:
    data = json.loads(j.read())

_DQN_HP = data.get("dqn", {}) if isinstance(data.get("dqn"), dict) else {}


def _hp(key: str):
    if key in _DQN_HP:
        return _DQN_HP[key]
    return data[key]


EPS_START = _hp("eps_start")
EPS_END = _hp("eps_end")
EPS_DECAY = _hp("eps_decay")
BATCH_SIZE = _hp("batch_size")
GAMMA = _hp("gamma")


def compute_epsilon(steps_done, schedule=None):
    """Epsilon for exploration; schedule from EPS_SCHEDULE env if not passed."""
    schedule = (schedule or os.getenv("EPS_SCHEDULE", "exp")).strip().lower()
    decay_steps = max(1.0, float(EPS_DECAY))
    progress = min(float(steps_done) / decay_steps, 1.0)
    if schedule == "linear":
        return max(float(EPS_END), float(EPS_START) - progress * (float(EPS_START) - float(EPS_END)))
    if schedule == "poly":
        power = float(os.getenv("EPS_POLY_POWER", "2.0"))
        return float(EPS_END) + (float(EPS_START) - float(EPS_END)) * ((1.0 - progress) ** power)
    if schedule == "sigmoid":
        mid = decay_steps * 0.5
        scale = max(1.0, decay_steps * 0.1)
        import math
        sig = 1.0 / (1.0 + math.exp((float(steps_done) - mid) / scale))
        return float(EPS_END) + (float(EPS_START) - float(EPS_END)) * sig
    # default: exp (linear progress, same as legacy)
    return float(EPS_START) + (float(EPS_END) - float(EPS_START)) * progress

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def unwrap_env(env):
    """Снять все gym-обёртки (OrderEnforcing и т.п.) до Warhammer40kEnv."""
    base = env
    seen: set[int] = set()
    while id(base) not in seen:
        seen.add(id(base))
        if hasattr(base, "unwrapped"):
            try:
                inner = base.unwrapped
                if inner is None or inner is base:
                    break
                base = inner
                continue
            except Exception:
                pass
        inner = getattr(base, "env", None)
        if inner is None or inner is base:
            break
        base = inner
    return base


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

def sample_action_list_from_space(
    env,
    len_model: int,
    *,
    masks_seq=None,
    legal_by_head: dict | None = None,
) -> list[int]:
    """Случайный flat-action по ordered_action_keys с опциональными масками (B2 per-unit)."""
    keys = ordered_action_keys(int(len_model))
    sampled = env.action_space.sample()
    action_list = [int(sampled[k]) for k in keys]
    for idx, key in enumerate(keys):
        raw_mask = None
        if masks_seq is not None and idx < len(masks_seq):
            raw_mask = masks_seq[idx]
        elif legal_by_head is not None and key in legal_by_head:
            raw_mask = legal_by_head[key]
        if raw_mask is None:
            continue
        mask = torch.as_tensor(raw_mask, dtype=torch.bool)
        valid_indices = torch.where(mask)[0].tolist()
        if valid_indices:
            action_list[idx] = int(random.choice(valid_indices))
    return action_list


def greedy_action_list_from_decision(decision, ordered_keys, legal_by_head: dict | None = None) -> list[int]:
    action: list[int] = []
    for head_idx, head in enumerate(decision):
        head = head.squeeze(0)
        key = ordered_keys[head_idx] if head_idx < len(ordered_keys) else None
        if key is not None and legal_by_head is not None and key in legal_by_head:
            mask = torch.as_tensor(legal_by_head[key], dtype=torch.bool, device=head.device)
            if mask.numel() == head.numel() and mask.any():
                masked_head = head.clone()
                masked_head[~mask] = -1e9
                action.append(int(masked_head.argmax().item()))
                continue
        action.append(int(head.argmax().item()))
    return action


def _per_unit_mask_keys(key: str) -> bool:
    """B2: головы, к которым применяем per-unit legal-маски (shoot/charge per юнит)."""
    return key.startswith("shoot_num_") or key.startswith("charge_num_")


def _build_select_action_masks(env, len_model):
    """B2: per-head legal-маски по ключам контракта (dict key -> bool-np.ndarray).

    Берём готовый per-unit контракт из env.get_legal_action_masks_by_head(side="model").
    Если env его не предоставляет — возвращаем пустой dict (маски не применяются).
    """
    env_unwrapped = unwrap_env(env)
    if not hasattr(env_unwrapped, "get_legal_action_masks_by_head"):
        return {}
    try:
        return env_unwrapped.get_legal_action_masks_by_head(side="model")
    except Exception:
        return {}


def select_action(env, state, steps_done, policy_net, len_model, shoot_mask=None):
    force_greedy = os.getenv("FORCE_GREEDY", "0") == "1" or os.getenv("PLAY_NO_EXPLORATION", "0") == "1"
    noisy_disable_eps = os.getenv("NOISY_DISABLE_EPS", "1") == "1"
    sample = random.random()
    eps_threshold = 0.0 if (force_greedy or noisy_disable_eps) else compute_epsilon(steps_done)
    steps_done += 1
    dev = next(policy_net.parameters()).device

    # B2: маски shoot/charge стали per-unit. Хардкод головы №2 больше не валиден,
    # поэтому применяем маски по КЛЮЧУ из ordered_action_keys. Источник масок —
    # per-head контракт env (legacy-параметр shoot_mask больше не используется).
    ordered_keys = ordered_action_keys(int(len_model))
    legal_by_head = _build_select_action_masks(env, int(len_model))


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
                key = ordered_keys[head_idx] if head_idx < len(ordered_keys) else None
                if key is not None and _per_unit_mask_keys(key) and key in legal_by_head:
                    mask = torch.as_tensor(legal_by_head[key], dtype=torch.bool, device=head.device)
                    if mask.numel() == head.numel() and mask.any():
                        masked_head = head.clone()
                        masked_head[~mask] = -1e9
                        action.append(int(masked_head.argmax().item()))
                        continue
                action.append(int(head.argmax().item()))
            return torch.tensor([action], device="cpu")
    else:
        sampled_action = env.action_space.sample()
        action_list = []
        for key in ordered_keys:
            choice = int(sampled_action[key])
            # B2: per-unit shoot/charge — ограничиваем случайный выбор легальной маской головы.
            if _per_unit_mask_keys(key) and key in legal_by_head:
                mask = torch.as_tensor(legal_by_head[key], dtype=torch.bool)
                valid_indices = torch.where(mask)[0].tolist()
                if valid_indices:
                    choice = random.choice(valid_indices)
            action_list.append(choice)
        action = torch.tensor([action_list], device="cpu")
        return action

def build_shoot_action_mask(env, log_fn=None, debug=False, side: str = "model"):
    """Legacy helper для eval/play-логов: min-rank маска по shoot_num_* (B2).

    side: сторона, для которой строится маска ("model" или "enemy"). По умолчанию
    "model" — обратная совместимость. В честном eval обе стороны должны вызывать
    с корректным side, иначе противник получит маски не своей стороны (сегрегация).
    """
    side = str(side or "model").strip().lower()
    if side not in {"model", "enemy"}:
        side = "model"
    env_unwrapped = unwrap_env(env)
    own_health = getattr(env_unwrapped, "unit_health", []) if side == "model" else getattr(env_unwrapped, "enemy_health", [])
    n_units = len(own_health or [])
    if n_units <= 0:
        return None
    space_key = "shoot_num_0"
    if space_key not in getattr(env_unwrapped.action_space, "spaces", {}):
        return None

    def maybe_log_mask_state(state_key, message):
        if log_fn is None:
            return
        last_state = getattr(env, "_last_shoot_mask_log_state", None)
        if last_state != state_key:
            env._last_shoot_mask_log_state = state_key
            log_fn(message)

    # own_* = атрибуты стороны side; other_* = атрибуты противоположной стороны.
    if side == "model":
        own_health_arr = env_unwrapped.unit_health
        own_fell_back = env_unwrapped.unitFellBack
        own_in_attack = env_unwrapped.unitInAttack
        own_weapon = env_unwrapped.unit_weapon
        own_coords = env_unwrapped.unit_coords
        other_health_arr = env_unwrapped.enemy_health
        other_coords = env_unwrapped.enemy_coords
        other_in_attack = env_unwrapped.enemyInAttack
    else:
        own_health_arr = env_unwrapped.enemy_health
        own_fell_back = env_unwrapped.enemyFellBack
        own_in_attack = env_unwrapped.enemyInAttack
        own_weapon = env_unwrapped.enemy_weapon
        own_coords = env_unwrapped.enemy_coords
        other_health_arr = env_unwrapped.unit_health
        other_coords = env_unwrapped.unit_coords
        other_in_attack = env_unwrapped.unitInAttack

    if hasattr(env_unwrapped, "get_legal_action_masks_by_head"):
        try:
            legal = env_unwrapped.get_legal_action_masks_by_head(side=side)
            valid_lengths: list[int] = []
            for u_idx in range(n_units):
                mask = legal.get(f"shoot_num_{u_idx}")
                if mask is None:
                    continue
                k = int(sum(1 for x in np.asarray(mask, dtype=bool) if bool(x)))
                if k > 0:
                    valid_lengths.append(k)
            if valid_lengths:
                min_len = min(valid_lengths)
                shoot_space = int(env_unwrapped.action_space.spaces[space_key].n)
                tmask = torch.zeros(shoot_space, dtype=torch.bool)
                tmask[: min(min_len, shoot_space)] = True
                if bool(tmask.any()):
                    return tmask
        except Exception:
            pass

    shoot_space = int(env_unwrapped.action_space.spaces[space_key].n)
    valid_lengths = []
    for i in range(n_units):
        if hasattr(env_unwrapped, "get_shoot_targets_for_unit"):
            valid_targets = env_unwrapped.get_shoot_targets_for_unit(side, i)
        else:
            if own_health_arr[i] <= 0:
                continue
            if own_fell_back[i]:
                continue
            if own_in_attack[i][0] == 1:
                continue
            if own_weapon[i] == "None":
                continue
            valid_targets = []
            for j in range(len(other_health_arr)):
                if (
                    distance(own_coords[i], other_coords[j])
                    <= own_weapon[i]["Range"]
                    and other_health_arr[j] > 0
                    and other_in_attack[j][0] == 0
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


def build_action_masks_by_head(env, len_model, log_fn=None, debug=False, side: str = "model"):
    """Унифицированный контракт масок для всех голов действия (B2 per-unit).

    side: сторона, для которой строятся маски ("model" или "enemy"). По умолчанию
    "model" — обратная совместимость (train/play всегда ходят за model). В честном
    eval обе стороны обязаны вызывать с корректным side: иначе противник (enemy)
    получит маски model-стороны (сегрегация → нечестный eval).
    """
    side = str(side or "model").strip().lower()
    if side not in {"model", "enemy"}:
        side = "model"
    env_unwrapped = unwrap_env(env)
    ordered_keys = ordered_action_keys(int(len_model))

    masks = []
    fallback_count = 0
    legal_by_head = None
    if hasattr(env_unwrapped, "get_legal_action_masks_by_head"):
        try:
            legal_by_head = env_unwrapped.get_legal_action_masks_by_head(side=side)
        except Exception:
            legal_by_head = None

    for key in ordered_keys:
        sp = env_unwrapped.action_space.spaces[key]
        if hasattr(sp, "n"):
            size = int(sp.n)
        elif hasattr(sp, "nvec"):
            size = int(sp.nvec[0])
        else:
            size = 1
        if legal_by_head is not None and key in legal_by_head:
            mask = torch.as_tensor(legal_by_head[key], dtype=torch.bool).clone()
            if mask.numel() != size:
                mask = torch.ones(size, dtype=torch.bool)
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

def convertToDict(action, len_model: int | None = None):
    naction = action.numpy()[0]
    if len_model is None:
        len_model = max(0, (len(naction) - 4) // 3)
    return action_tensor_to_dict(action, len_model=int(len_model))

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

    def _to_device_batch(tensor):
        if tensor is None:
            return None
        if tensor.device == dev:
            return tensor
        if pin_memory and tensor.device.type == "cpu" and dev.type == "cuda":
            return tensor.pin_memory().to(dev, non_blocking=True)
        return tensor.to(dev)

    def _as_cpu_tensor(value, *, dtype=None):
        if value is None:
            return None
        if torch.is_tensor(value):
            tensor = value.detach()
            if tensor.device.type != "cpu":
                tensor = tensor.cpu()
            if dtype is not None and tensor.dtype != dtype:
                tensor = tensor.to(dtype=dtype)
            return tensor
        return torch.as_tensor(value, dtype=dtype)

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
    state_tensors_cpu = []
    for s in batch.state:
        if s is None:
            state_tensors_cpu.append(torch.zeros(desired_shape, device="cpu", dtype=torch.float32))
        else:
            state_tensors_cpu.append(_as_cpu_tensor(s, dtype=torch.float32).reshape(desired_shape))
    state_batch = _to_device_batch(torch.cat(state_tensors_cpu, dim=0))  # [B, n_obs]

    # ---- action_batch / reward_batch (на тот же dev!) ----
    action_tensors_cpu = [_as_cpu_tensor(a, dtype=torch.long).reshape(1, -1) for a in batch.action]
    reward_tensors_cpu = [_as_cpu_tensor(r, dtype=torch.float32).reshape(-1) for r in batch.reward]
    action_batch = _to_device_batch(torch.cat(action_tensors_cpu, dim=0)).long()  # индексы ОБЯЗАТЕЛЬНО long и на dev
    reward_batch = _to_device_batch(torch.cat(reward_tensors_cpu, dim=0)).float().view(-1)  # [B]
    n_step_batch = _to_device_batch(torch.as_tensor(batch.n_step, dtype=torch.float32))  # [B]

    # ---- next states ----
    non_final_mask = _to_device_batch(torch.as_tensor([s is not None for s in batch.next_state], dtype=torch.bool))

    non_final_next_states = None
    non_final_next_shoot_masks = None
    if non_final_mask.any():
        non_final_next_states = _to_device_batch(
            torch.cat(
                [_as_cpu_tensor(s, dtype=torch.float32).reshape(desired_shape) for s in batch.next_state if s is not None],
                dim=0,
            )
        )
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
        n_ensemble = int(getattr(policy_net, "n_ensemble", 1))
        ensemble_priority_lambda = float(os.getenv("PER_ENSEMBLE_PRIORITY_LAMBDA", "0.1"))

        def _iqn_member_loss(online_quantiles, taus_local):
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
                    target_next_quantiles = target_net.iqn(
                        non_final_next_states, num_quantiles=iqn_n_tgt, return_taus=False
                    )
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
                    taus_local.float(),
                    kappa=iqn_kappa,
                )
                per_head_losses.append(loss_i)
                per_head_td.append(td_i.abs().mean(dim=(1, 2)))
            stacked_loss = torch.stack(per_head_losses, dim=1)
            per_sample_loss = stacked_loss.mean(dim=1)
            td_errors = torch.stack(per_head_td, dim=1).mean(dim=1)
            return per_sample_loss, td_errors, next_state_values

        if n_ensemble > 1:
            members_online, taus = policy_net.iqn_ensemble_members(
                state_batch, num_quantiles=iqn_n, return_taus=True
            )
            member_sample_losses = []
            member_td_errors = []
            next_state_values = None
            for online_quantiles in members_online:
                ps, td_e, nsv = _iqn_member_loss(online_quantiles, taus)
                member_sample_losses.append(ps)
                member_td_errors.append(td_e)
                next_state_values = nsv
            per_sample_loss = torch.stack(member_sample_losses, dim=0).mean(dim=0)
            td_errors = torch.stack(member_td_errors, dim=0).mean(dim=0)
        else:
            with torch.autocast(device_type=dev.type, dtype=torch.float16, enabled=amp_enabled):
                online_quantiles, taus = policy_net.iqn(state_batch, num_quantiles=iqn_n, return_taus=True)
            per_sample_loss, td_errors, next_state_values = _iqn_member_loss(online_quantiles, taus)

        ensemble_std_mean = 0.0
        if n_ensemble > 1:
            with torch.no_grad():
                _, stds = policy_net.q_ensemble_stats(state_batch)
                if stds:
                    # Головы имеют разную ширину (move/attack/shoot/...), поэтому
                    # усредняем std внутри каждой головы и затем по головам — без stack.
                    ensemble_std_mean = float(
                        torch.stack([s.mean() for s in stds]).mean().item()
                    )

        if per_enabled:
            weight_t = torch.tensor(weights, device=dev, dtype=torch.float32)
            loss = (per_sample_loss * weight_t).mean()
            new_priorities = td_errors.detach().cpu().numpy() + per_eps
            if n_ensemble > 1 and ensemble_priority_lambda > 0.0:
                with torch.no_grad():
                    _, stds = policy_net.q_ensemble_stats(state_batch)
                    if stds:
                        # per-sample неопределённость: усредняем std внутри головы
                        # ([B, A_head] -> [B]), затем по головам ([B, H] -> [B]).
                        std_per_sample = (
                            torch.stack([s.mean(dim=1) for s in stds], dim=1)
                            .mean(dim=1)
                            .detach()
                            .cpu()
                            .numpy()
                        )
                        new_priorities = new_priorities + ensemble_priority_lambda * std_per_sample
            memory.update_priorities(indices, new_priorities)
            per_stats = {
                "priority_mean": float(new_priorities.mean()),
                "priority_max": float(new_priorities.max()),
                "is_weight_mean": float(weight_t.mean().item()),
                "is_weight_max": float(weight_t.max().item()),
                "td_error_mean": float(td_errors.mean().item()),
                "td_error_max": float(td_errors.max().item()),
                "ensemble_std_mean": ensemble_std_mean,
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
            "n_ensemble": int(n_ensemble),
            "ensemble_std_mean": ensemble_std_mean,
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
