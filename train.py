from collections import Counter
import sys
import os
import csv
import numpy as np
import gymnasium as gym
import pickle
import datetime
import collections
import math
import json
import random
import matplotlib.pyplot as plt
import time
import multiprocessing as mp
import threading
import atexit
from tqdm import tqdm
from gym_mod.envs.warhamEnv import *
from gym_mod.engine import genDisplay, Unit, unitData, weaponData, initFile, metrics
from gym_mod.engine.io_profiler import get_io_profiler
from gym_mod.engine.mission import (
    normalize_mission_name,
    board_dims_for_mission,
    deploy_for_mission,
    post_deploy_setup,
)
from gym_mod.engine.agent_registry import (
    AgentIdentity,
    build_agent_id,
    compatible_contracts,
    load_agent_by_id,
    make_env_contract,
    list_agents,
    save_agent_artifact,
)
from gym_mod.engine.matchmaker import choose_opponent, record_matchup
from gymnasium import spaces

AGENT_TRAIN_LOG_FILE = "LOGS_FOR_AGENTS_TRAIN.md"
os.environ.setdefault("AGENT_LOG_FILE", AGENT_TRAIN_LOG_FILE)

from model.DQN import *
from model.memory import *
from model.utils import *

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.optim import Optimizer
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
import torch
print("[DEVICE CHECK] cuda:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("[DEVICE CHECK] name:", torch.cuda.get_device_name(0))

# Workaround для окружений, где torch._dynamo падает из-за несовместимого triton.
if os.getenv("TORCH_OPTIMIZER_NO_DYNAMO", "1") == "1":
    if hasattr(Optimizer.add_param_group, "__wrapped__"):
        Optimizer.add_param_group = Optimizer.add_param_group.__wrapped__
    if hasattr(Optimizer.state_dict, "__wrapped__"):
        Optimizer.state_dict = Optimizer.state_dict.__wrapped__
    if hasattr(Optimizer.load_state_dict, "__wrapped__"):
        Optimizer.load_state_dict = Optimizer.load_state_dict.__wrapped__


import warnings
warnings.filterwarnings("ignore") 

# ===== torch inductor warnings/behavior =====
INDUCTOR_CUDAGRAPH_WARN_LIMIT = os.getenv("INDUCTOR_CUDAGRAPH_WARN_LIMIT")
INDUCTOR_SKIP_DYNAMIC_CUDAGRAPHS = os.getenv("INDUCTOR_SKIP_DYNAMIC_CUDAGRAPHS", "0") == "1"
if INDUCTOR_CUDAGRAPH_WARN_LIMIT is not None:
    if INDUCTOR_CUDAGRAPH_WARN_LIMIT.lower() in ("none", "off", "disable"):
        torch._inductor.config.triton.cudagraph_dynamic_shape_warn_limit = None
    else:
        torch._inductor.config.triton.cudagraph_dynamic_shape_warn_limit = int(INDUCTOR_CUDAGRAPH_WARN_LIMIT)
if INDUCTOR_SKIP_DYNAMIC_CUDAGRAPHS:
    torch._inductor.config.triton.cudagraph_skip_dynamic_graphs = True
# ==========================================

with open(os.path.abspath("hyperparams.json")) as j:
    data = json.loads(j.read())

# ===== algo flags =====
DOUBLE_DQN_ENABLED = os.getenv("DOUBLE_DQN_ENABLED", "1") == "1"
DUELING_ENABLED = os.getenv("DUELING_ENABLED", "1") == "1"
REWARD_DEBUG = os.getenv("REWARD_DEBUG", "0") == "1"
REWARD_DEBUG_EVERY = int(os.getenv("REWARD_DEBUG_EVERY", "200"))
# ===== train logging =====
TRAIN_LOG_ENABLED = os.getenv("TRAIN_LOG_ENABLED", "1") == "1"
TRAIN_LOG_EVERY_UPDATES = int(os.getenv("TRAIN_LOG_EVERY_UPDATES", "200"))
TRAIN_LOG_TO_FILE = os.getenv("TRAIN_LOG_TO_FILE", "1") == "1"
TRAIN_LOG_TO_CONSOLE = os.getenv("TRAIN_LOG_TO_CONSOLE", "0") == "1"
TRAIN_DEBUG = os.getenv("TRAIN_DEBUG", "0") == "1"
LOG_EVERY = int(os.getenv("LOG_EVERY", "200"))
if TRAIN_LOG_EVERY_UPDATES < 1:
    TRAIN_LOG_EVERY_UPDATES = 1
if TRAIN_DEBUG:
    TRAIN_LOG_EVERY_UPDATES = min(TRAIN_LOG_EVERY_UPDATES, 50)
# =========================
# ===== per + n-step =====
PER_ENABLED = os.getenv("PER_ENABLED", "1") == "1"
PER_ALPHA = float(os.getenv("PER_ALPHA", "0.55"))
PER_BETA_START = float(os.getenv("PER_BETA_START", "0.4"))
PER_BETA_FRAMES = int(os.getenv("PER_BETA_FRAMES", "200000"))
PER_EPS = float(os.getenv("PER_EPS", "1e-6"))
N_STEP = int(os.getenv("N_STEP", "3"))
if N_STEP < 1:
    N_STEP = 1
# ======================

# ===== perf knobs =====
RENDER_EVERY = int(os.getenv("RENDER_EVERY", "0"))  # 0 = выключить рендер полностью
UPDATES_PER_STEP = int(os.getenv("UPDATES_PER_STEP", "4"))  
BATCH_ACT = os.getenv("BATCH_ACT", "1") == "1"
PREFETCH = os.getenv("PREFETCH", "0") == "1"
PIN_MEMORY = os.getenv("PIN_MEMORY", "0") == "1"
USE_AMP = os.getenv("USE_AMP", "1") == "1"
USE_COMPILE = os.getenv("USE_COMPILE", "0") == "1"
SAVE_EVERY = int(os.getenv("SAVE_EVERY", "0"))
SAVE_EVERY_MIN = max(1, int(os.getenv("SAVE_EVERY_MIN", "50")))
SAVE_EVERY_ALLOW_LOW = os.getenv("SAVE_EVERY_ALLOW_LOW", "0") == "1"
if SAVE_EVERY > 0 and SAVE_EVERY < SAVE_EVERY_MIN and not SAVE_EVERY_ALLOW_LOW:
    SAVE_EVERY = SAVE_EVERY_MIN
RESUME_CHECKPOINT = os.getenv("RESUME_CHECKPOINT", "").strip()
# Параллелизм через subprocess (только без self-play, маски считаются в воркерах).
USE_SUBPROC_ENVS = os.getenv("USE_SUBPROC_ENVS", "0") == "1"
# Рекомендации (включать вручную при наличии GPU/CPU): NUM_ENVS=8..16, BATCH_ACT=1,
# USE_AMP=1, USE_COMPILE=1, PREFETCH=1, PIN_MEMORY=1, LOG_EVERY=200.
# ======================

# ===== self-play config =====
SELF_PLAY_ENABLED = os.getenv("SELF_PLAY_ENABLED", "0") == "1"
SELF_PLAY_UPDATE_EVERY_EPISODES = int(os.getenv("SELF_PLAY_UPDATE_EVERY_EPISODES", "50"))
SELF_PLAY_OPPONENT_MODE = os.getenv("SELF_PLAY_OPPONENT_MODE", "snapshot")
SELF_PLAY_FIXED_PATH = os.getenv("SELF_PLAY_FIXED_PATH", "")
SELF_PLAY_OPPONENT_EPSILON = float(os.getenv("SELF_PLAY_OPPONENT_EPSILON", "0.0"))
SELF_PLAY_OPPONENT_EPSILON_MIN = float(os.getenv("SELF_PLAY_OPPONENT_EPSILON_MIN", str(SELF_PLAY_OPPONENT_EPSILON)))
SELF_PLAY_OPPONENT_EPSILON_MAX = float(os.getenv("SELF_PLAY_OPPONENT_EPSILON_MAX", str(max(SELF_PLAY_OPPONENT_EPSILON, 0.08))))
SELF_PLAY_OPPONENT_EPSILON_DECAY_EPISODES = int(os.getenv("SELF_PLAY_OPPONENT_EPSILON_DECAY_EPISODES", "1600"))
SELF_PLAY_ADAPTIVE_UPDATE = os.getenv("SELF_PLAY_ADAPTIVE_UPDATE", "1") == "1"
SELF_PLAY_UPDATE_EVERY_MIN = int(os.getenv("SELF_PLAY_UPDATE_EVERY_MIN", "25"))
SELF_PLAY_UPDATE_EVERY_MAX = int(os.getenv("SELF_PLAY_UPDATE_EVERY_MAX", "150"))
SELF_PLAY_DRAW_RATE_HIGH = float(os.getenv("SELF_PLAY_DRAW_RATE_HIGH", "0.70"))
SELF_PLAY_DRAW_RATE_LOW = float(os.getenv("SELF_PLAY_DRAW_RATE_LOW", "0.45"))
SELF_PLAY_POOL_ENABLED = os.getenv("SELF_PLAY_POOL_ENABLED", "1") == "1"
SELF_PLAY_POOL_SIZE = int(os.getenv("SELF_PLAY_POOL_SIZE", "6"))
SELF_PLAY_POOL_SAMPLE_OLD_PROB = float(os.getenv("SELF_PLAY_POOL_SAMPLE_OLD_PROB", "0.45"))
SELF_PLAY_POOL_SMART_SAMPLING = os.getenv("SELF_PLAY_POOL_SMART_SAMPLING", "1") == "1"
SELF_PLAY_POOL_SCORE_WIN_W = float(os.getenv("SELF_PLAY_POOL_SCORE_WIN_W", "0.50"))
SELF_PLAY_POOL_SCORE_DRAW_W = float(os.getenv("SELF_PLAY_POOL_SCORE_DRAW_W", "0.15"))
SELF_PLAY_POOL_SCORE_VP_W = float(os.getenv("SELF_PLAY_POOL_SCORE_VP_W", "0.35"))
SELF_PLAY_POOL_SCORE_EXPLORE_BONUS = float(os.getenv("SELF_PLAY_POOL_SCORE_EXPLORE_BONUS", "0.25"))
SELF_PLAY_POOL_EMA_ENABLED = os.getenv("SELF_PLAY_POOL_EMA_ENABLED", "1") == "1"
SELF_PLAY_POOL_EMA_ALPHA = float(os.getenv("SELF_PLAY_POOL_EMA_ALPHA", "0.15"))
SELF_PLAY_POOL_MIN_GAMES_FOR_SMART = int(os.getenv("SELF_PLAY_POOL_MIN_GAMES_FOR_SMART", "3"))

EVAL_WINDOW_EPISODES = int(os.getenv("EVAL_WINDOW_EPISODES", "100"))
EVAL_WINDOW_LOG_EVERY = int(os.getenv("EVAL_WINDOW_LOG_EVERY", "50"))
DRAW_PIT_ALERT_RATE = float(os.getenv("DRAW_PIT_ALERT_RATE", "0.70"))
DRAW_PIT_ALERT_WIN_MAX = float(os.getenv("DRAW_PIT_ALERT_WIN_MAX", "0.15"))
DRAW_PIT_ALERT_STREAK = int(os.getenv("DRAW_PIT_ALERT_STREAK", "3"))

BEST_EVAL_ENABLED = os.getenv("BEST_EVAL_ENABLED", "1") == "1"
BEST_EVAL_W_WIN = float(os.getenv("BEST_EVAL_W_WIN", "1.00"))
BEST_EVAL_W_DRAW = float(os.getenv("BEST_EVAL_W_DRAW", "0.75"))
BEST_EVAL_W_WIPE_ENEMY = float(os.getenv("BEST_EVAL_W_WIPE_ENEMY", "0.30"))
BEST_EVAL_W_WIPE_MODEL = float(os.getenv("BEST_EVAL_W_WIPE_MODEL", "0.25"))
BEST_EVAL_W_VP = float(os.getenv("BEST_EVAL_W_VP", "0.45"))

DRAW_GUARD_ENABLED = os.getenv("DRAW_GUARD_ENABLED", "1") == "1"
DRAW_GUARD_PENALTY_STEP = float(os.getenv("DRAW_GUARD_PENALTY_STEP", "0.02"))
DRAW_GUARD_PENALTY_MAX = float(os.getenv("DRAW_GUARD_PENALTY_MAX", "1.00"))
DRAW_GUARD_POOL_OLD_PROB_STEP = float(os.getenv("DRAW_GUARD_POOL_OLD_PROB_STEP", "0.05"))
DRAW_GUARD_POOL_OLD_PROB_MAX = float(os.getenv("DRAW_GUARD_POOL_OLD_PROB_MAX", "0.95"))

DET_EVAL_ENABLED = os.getenv("DET_EVAL_ENABLED", "1") == "1"
DET_EVAL_EVERY_EPISODES = int(os.getenv("DET_EVAL_EVERY_EPISODES", "250"))
DET_EVAL_EPISODES = int(os.getenv("DET_EVAL_EPISODES", "20"))
DET_EVAL_OPPONENT_EPSILON = float(os.getenv("DET_EVAL_OPPONENT_EPSILON", "0.0"))

REWARD_SCHEDULE_ENABLED = os.getenv("REWARD_SCHEDULE_ENABLED", "1") == "1"
REWARD_STAGE1_END_EP = int(os.getenv("REWARD_STAGE1_END_EP", "1500"))
REWARD_STAGE2_END_EP = int(os.getenv("REWARD_STAGE2_END_EP", "3500"))
REWARD_STAGE1_DRAW_PENALTY = float(os.getenv("REWARD_STAGE1_DRAW_PENALTY", str(getattr(reward_cfg, "TURN_LIMIT_DRAW_PENALTY", 0.35))))
REWARD_STAGE2_DRAW_PENALTY = float(os.getenv("REWARD_STAGE2_DRAW_PENALTY", str(max(getattr(reward_cfg, "TURN_LIMIT_DRAW_PENALTY", 0.35), 0.45))))
REWARD_STAGE3_DRAW_PENALTY = float(os.getenv("REWARD_STAGE3_DRAW_PENALTY", str(max(getattr(reward_cfg, "TURN_LIMIT_DRAW_PENALTY", 0.35), 0.60))))
REWARD_STAGE1_VP_REWARD_SCALE = float(os.getenv("REWARD_STAGE1_VP_REWARD_SCALE", str(getattr(reward_cfg, "TURN_LIMIT_VP_MARGIN_REWARD_SCALE", 0.12))))
REWARD_STAGE2_VP_REWARD_SCALE = float(os.getenv("REWARD_STAGE2_VP_REWARD_SCALE", str(max(getattr(reward_cfg, "TURN_LIMIT_VP_MARGIN_REWARD_SCALE", 0.12), 0.16))))
REWARD_STAGE3_VP_REWARD_SCALE = float(os.getenv("REWARD_STAGE3_VP_REWARD_SCALE", str(max(getattr(reward_cfg, "TURN_LIMIT_VP_MARGIN_REWARD_SCALE", 0.12), 0.20))))

if SELF_PLAY_UPDATE_EVERY_EPISODES < 1:
    SELF_PLAY_UPDATE_EVERY_EPISODES = 1
if SELF_PLAY_UPDATE_EVERY_MIN < 1:
    SELF_PLAY_UPDATE_EVERY_MIN = 1
if SELF_PLAY_UPDATE_EVERY_MAX < SELF_PLAY_UPDATE_EVERY_MIN:
    SELF_PLAY_UPDATE_EVERY_MAX = SELF_PLAY_UPDATE_EVERY_MIN
if SELF_PLAY_OPPONENT_EPSILON_DECAY_EPISODES < 1:
    SELF_PLAY_OPPONENT_EPSILON_DECAY_EPISODES = 1
if SELF_PLAY_OPPONENT_EPSILON_MIN < 0:
    SELF_PLAY_OPPONENT_EPSILON_MIN = 0.0
if SELF_PLAY_OPPONENT_EPSILON_MAX < SELF_PLAY_OPPONENT_EPSILON_MIN:
    SELF_PLAY_OPPONENT_EPSILON_MAX = SELF_PLAY_OPPONENT_EPSILON_MIN
if SELF_PLAY_POOL_SIZE < 1:
    SELF_PLAY_POOL_SIZE = 1
if SELF_PLAY_POOL_SAMPLE_OLD_PROB < 0:
    SELF_PLAY_POOL_SAMPLE_OLD_PROB = 0.0
if SELF_PLAY_POOL_SAMPLE_OLD_PROB > 1:
    SELF_PLAY_POOL_SAMPLE_OLD_PROB = 1.0
if SELF_PLAY_POOL_SCORE_EXPLORE_BONUS < 0:
    SELF_PLAY_POOL_SCORE_EXPLORE_BONUS = 0.0
if SELF_PLAY_POOL_EMA_ALPHA <= 0:
    SELF_PLAY_POOL_EMA_ALPHA = 0.05
if SELF_PLAY_POOL_EMA_ALPHA > 1:
    SELF_PLAY_POOL_EMA_ALPHA = 1.0
if SELF_PLAY_POOL_MIN_GAMES_FOR_SMART < 0:
    SELF_PLAY_POOL_MIN_GAMES_FOR_SMART = 0
if DRAW_GUARD_PENALTY_STEP < 0:
    DRAW_GUARD_PENALTY_STEP = 0.0
if DRAW_GUARD_PENALTY_MAX < 0:
    DRAW_GUARD_PENALTY_MAX = 0.0
if DRAW_GUARD_POOL_OLD_PROB_STEP < 0:
    DRAW_GUARD_POOL_OLD_PROB_STEP = 0.0
if DRAW_GUARD_POOL_OLD_PROB_MAX < 0:
    DRAW_GUARD_POOL_OLD_PROB_MAX = 0.0
if DRAW_GUARD_POOL_OLD_PROB_MAX > 1:
    DRAW_GUARD_POOL_OLD_PROB_MAX = 1.0
if DET_EVAL_EVERY_EPISODES < 1:
    DET_EVAL_EVERY_EPISODES = 1
if DET_EVAL_EPISODES < 1:
    DET_EVAL_EPISODES = 1
if REWARD_STAGE1_END_EP < 0:
    REWARD_STAGE1_END_EP = 0
if REWARD_STAGE2_END_EP < REWARD_STAGE1_END_EP:
    REWARD_STAGE2_END_EP = REWARD_STAGE1_END_EP
if EVAL_WINDOW_EPISODES < 1:
    EVAL_WINDOW_EPISODES = 1
if EVAL_WINDOW_LOG_EVERY < 1:
    EVAL_WINDOW_LOG_EVERY = 1
if DRAW_PIT_ALERT_STREAK < 1:
    DRAW_PIT_ALERT_STREAK = 1
if SELF_PLAY_OPPONENT_MODE not in ("snapshot", "fixed_checkpoint"):
    raise ValueError(
        "SELF_PLAY_OPPONENT_MODE должен быть 'snapshot' или 'fixed_checkpoint'. "
        f"Получено: {SELF_PLAY_OPPONENT_MODE}"
    )
# ============================


DEFAULT_MISSION_NAME = "only_war"
LEAGUE_ENABLE = os.getenv("LEAGUE_ENABLE", "1") == "1"
LEARNER_SIDE = str(os.getenv("LEARNER_SIDE", "P1")).strip().upper() or "P1"
LEARNER_FACTION = str(os.getenv("LEARNER_FACTION", "Necrons")).strip() or "Necrons"
OPPONENT_POLICY = str(os.getenv("OPPONENT_POLICY", "mirror")).strip().lower() or "mirror"
OPPONENT_AGENT_ID = str(os.getenv("OPPONENT_AGENT_ID", "")).strip()
RULESET_VERSION = str(os.getenv("RULESET_VERSION", "only_war_v1")).strip() or "only_war_v1"
HEURISTIC_MODE = str(os.getenv("HEURISTIC_MODE", "v2")).strip().lower() or "v2"
IO_PROFILER = get_io_profiler()

def to_np_state(s):
    if isinstance(s, (dict, collections.OrderedDict)):
        return np.array(list(s.values()), dtype=np.float32)
    return np.array(s, dtype=np.float32)

def build_n_step_transition(buffer, gamma):
    reward_sum = 0.0
    next_state = None
    next_shoot_mask = None
    n_step = 0
    for idx, (_, _, reward, next_state_candidate, done_flag, next_shoot_mask_candidate) in enumerate(buffer):
        reward_sum += (gamma ** idx) * reward
        n_step += 1
        next_state = next_state_candidate
        next_shoot_mask = next_shoot_mask_candidate
        if done_flag:
            next_state = None
            next_shoot_mask = None
            break
    return reward_sum, next_state, next_shoot_mask, n_step

def select_action_with_epsilon(env, state, policy_net, epsilon, len_model, shoot_mask=None):
    sample = random.random()
    dev = next(policy_net.parameters()).device

    if isinstance(state, collections.OrderedDict):
        state = np.array(list(state.values()), dtype=np.float32)
    elif isinstance(state, np.ndarray):
        state = state.astype(np.float32, copy=False)

    if not torch.is_tensor(state):
        state = torch.tensor(state, dtype=torch.float32, device=dev)
    else:
        state = state.to(dev)

    if state.dim() == 1:
        state = state.unsqueeze(0)

    if sample > epsilon:
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
        label = "move_num_"+str(i)
        action_list.append(sampled_action[label])
    action = torch.tensor([action_list], device="cpu")
    return action


def moving_avg(values, window=50):
    if len(values) == 0:
        return []
    w = max(1, int(window))
    out = []
    for i in range(len(values)):
        j0 = max(0, i - w + 1)
        chunk = values[j0:i+1]
        out.append(sum(chunk) / len(chunk))
    return out


def parse_clip_reward_config(raw_value: str):
    """
    CLIP_REWARD варианты:
      - off/none/0/false -> отключено
      - "1" -> симметричный клип [-1, +1]
      - "-1,1" -> явный диапазон [min, max]
    """
    text = str(raw_value).strip().lower()
    if text in ("", "off", "none", "false", "0"):
        return False, None, None

    if "," in text:
        parts = [p.strip() for p in text.split(",") if p.strip()]
        if len(parts) != 2:
            warn_msg = (
                "[TRAIN][WARN] Неверный формат CLIP_REWARD. "
                "Где: train.py (parse_clip_reward_config). "
                "Что делать: используйте off, число (например 1) или диапазон min,max (например -1,1). "
                f"Получено: {raw_value}. Клиппинг отключен."
            )
            print(warn_msg)
            append_agent_log(warn_msg)
            return False, None, None
        try:
            lo, hi = float(parts[0]), float(parts[1])
        except ValueError:
            warn_msg = (
                "[TRAIN][WARN] CLIP_REWARD содержит нечисловые границы. "
                "Где: train.py (parse_clip_reward_config). "
                "Что делать: задайте диапазон числами, например -1,1. "
                f"Получено: {raw_value}. Клиппинг отключен."
            )
            print(warn_msg)
            append_agent_log(warn_msg)
            return False, None, None
    else:
        try:
            bound = abs(float(text))
        except ValueError:
            warn_msg = (
                "[TRAIN][WARN] CLIP_REWARD не является числом. "
                "Где: train.py (parse_clip_reward_config). "
                "Что делать: используйте off, число (например 1) или диапазон min,max (например -1,1). "
                f"Получено: {raw_value}. Клиппинг отключен."
            )
            print(warn_msg)
            append_agent_log(warn_msg)
            return False, None, None
        lo, hi = -bound, bound

    if lo > hi:
        lo, hi = hi, lo
    return True, float(lo), float(hi)


def maybe_clip_reward(value: float, enabled: bool, lo=None, hi=None):
    if not enabled or lo is None or hi is None:
        return float(value), False
    clipped = float(np.clip(float(value), lo, hi))
    return clipped, clipped != float(value)


def _load_checkpoint_payload(checkpoint_path: str):
    try:
        return torch.load(checkpoint_path, map_location=device, weights_only=False)
    except TypeError:
        return torch.load(checkpoint_path, map_location=device)


def _extract_policy_state_dict(checkpoint):
    if not isinstance(checkpoint, dict):
        return checkpoint
    for key in ("policy_net", "model_state_dict", "state_dict"):
        value = checkpoint.get(key)
        if isinstance(value, dict):
            return value
    if checkpoint and all(hasattr(value, "shape") for value in checkpoint.values()):
        return checkpoint
    return None


def _resume_from_checkpoint(policy_net, target_net, optimizer, memory, checkpoint_path: str) -> dict:
    if not os.path.isfile(checkpoint_path):
        err_msg = (
            "[RESUME][ERROR] Не найден чекпойнт. "
            "Где: train.py (_resume_from_checkpoint). "
            "Что делать: проверьте RESUME_CHECKPOINT и укажите существующий файл .pth. "
            f"Путь: {checkpoint_path}"
        )
        print(err_msg)
        append_agent_log(err_msg)
        raise FileNotFoundError(err_msg)

    try:
        load_start_line = f"[RESUME] loading checkpoint path={checkpoint_path}"
        print(load_start_line)
        append_agent_log(load_start_line)
        load_start_ts = time.perf_counter()
        checkpoint = _load_checkpoint_payload(checkpoint_path)
        load_elapsed = time.perf_counter() - load_start_ts
        loaded_line = f"[RESUME] checkpoint payload loaded in {load_elapsed:.2f}s"
        print(loaded_line)
        append_agent_log(loaded_line)
    except Exception as exc:
        err_msg = (
            "[RESUME][ERROR] Не удалось загрузить чекпойнт. "
            "Где: train.py (_load_checkpoint_payload/torch.load). "
            "Что делать: проверьте целостность файла или пересохраните чекпойнт текущей версией PyTorch. "
            f"Путь: {checkpoint_path}. Детали: {exc}"
        )
        print(err_msg)
        append_agent_log(err_msg)
        raise

    policy_state = _extract_policy_state_dict(checkpoint)
    if not isinstance(policy_state, dict):
        err_msg = (
            "[RESUME][ERROR] В чекпойнте нет policy_net state_dict. "
            "Где: train.py (_extract_policy_state_dict). "
            "Что делать: укажите корректный checkpoint_ep*.pth с policy_net. "
            f"Путь: {checkpoint_path}"
        )
        print(err_msg)
        append_agent_log(err_msg)
        raise ValueError(err_msg)

    policy_net.load_state_dict(normalize_state_dict(policy_state))
    policy_loaded = 1

    target_loaded = 0
    target_state = checkpoint.get("target_net") if isinstance(checkpoint, dict) else None
    if isinstance(target_state, dict):
        target_net.load_state_dict(normalize_state_dict(target_state))
        target_loaded = 1
    else:
        target_net.load_state_dict(normalize_state_dict(policy_net.state_dict()))

    optimizer_loaded = 0
    optimizer_state = checkpoint.get("optimizer") if isinstance(checkpoint, dict) else None
    if isinstance(optimizer_state, dict):
        try:
            optimizer.load_state_dict(optimizer_state)
            optimizer_loaded = 1
        except Exception as exc:
            warn_msg = (
                "[RESUME][WARN] Не удалось загрузить optimizer state. "
                "Где: train.py (_resume_from_checkpoint/optimizer.load_state_dict). "
                "Что делать: обучение продолжится с новым optimizer, при необходимости "
                "сохраните свежий checkpoint и проверьте совместимость версий. "
                f"Детали: {exc}"
            )
            print(warn_msg)
            append_agent_log(warn_msg)
    else:
        warn_msg = (
            "[RESUME][WARN] В чекпойнте нет optimizer state. "
            "Где: train.py (_resume_from_checkpoint). "
            "Что делать: обучение продолжится с новым optimizer; "
            "для полного resume сохраняйте checkpoint с optimizer."
        )
        print(warn_msg)
        append_agent_log(warn_msg)

    restored_global_step = 0
    restored_optimize_steps = 0
    restored_episode = 0
    if isinstance(checkpoint, dict):
        restored_global_step = int(checkpoint.get("global_step", 0) or 0)
        restored_optimize_steps = int(checkpoint.get("optimize_steps", 0) or 0)
        restored_episode = int(checkpoint.get("episode", 0) or 0)

    replay_loaded = 0
    replay_state = checkpoint.get("replay_memory") if isinstance(checkpoint, dict) else None
    if replay_state is not None:
        try:
            replay_loaded = int(memory.load_state_dict(replay_state) or 0)
        except Exception as exc:
            warn_msg = (
                "[RESUME][WARN] Не удалось загрузить replay buffer. "
                "Где: train.py (_resume_from_checkpoint/memory.load_state_dict). "
                "Что делать: обучение продолжится с пустым буфером; проверьте совместимость формата. "
                f"Детали: {exc}"
            )
            print(warn_msg)
            append_agent_log(warn_msg)
    else:
        warn_msg = (
            "[RESUME][WARN] В чекпойнте нет replay buffer state. "
            "Где: train.py (_resume_from_checkpoint). "
            "Что делать: обучение продолжится с пустым буфером; "
            "для полного resume сохраняйте replay_memory в checkpoint."
        )
        print(warn_msg)
        append_agent_log(warn_msg)

    decay_steps = max(1.0, float(EPS_DECAY))
    eps_progress = min(float(restored_global_step) / decay_steps, 1.0)
    eps_at_resume = EPS_START + (EPS_END - EPS_START) * eps_progress

    ok_line = f"[RESUME] loaded checkpoint={checkpoint_path}"
    details_line = (
        "[RESUME] loaded: "
        f"policy={policy_loaded} target={target_loaded} optimizer={optimizer_loaded} "
        f"global_step={restored_global_step} optimize_steps={restored_optimize_steps} "
        f"episode={restored_episode} replay_size={replay_loaded} eps={eps_at_resume:.4f}"
    )
    print(ok_line)
    print(details_line)
    append_agent_log(ok_line)
    append_agent_log(details_line)

    return {
        "global_step": restored_global_step,
        "optimize_steps": restored_optimize_steps,
        "episode": restored_episode,
        "replay_size": replay_loaded,
        "epsilon": float(eps_at_resume),
    }

def save_extra_metrics(run_id: str, ep_rows: list[dict], metrics_dir="metrics"):
    os.makedirs(metrics_dir, exist_ok=True)
    os.makedirs("gui/img", exist_ok=True)

    # --- CSV ---
    csv_path = os.path.join(metrics_dir, f"stats_{run_id}.csv")
    cols = ["episode", "ep_reward", "ep_len", "turn", "model_vp", "player_vp", "vp_diff", "result", "end_reason", "end_code"]
    with IO_PROFILER.timed("metrics save"):
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in ep_rows:
                w.writerow({k: r.get(k, "") for k in cols})

    wins01 = [1 if r["result"] == "win" else 0 for r in ep_rows]
    vp_diff = [r["vp_diff"] for r in ep_rows]
    ep_idx = list(range(1, len(ep_rows) + 1))

    # --- Winrate plot ---
    winrate_ma = moving_avg(wins01, window=50)
    plt.figure()
    plt.plot(ep_idx, winrate_ma)
    plt.xlabel("Episodes")
    plt.ylabel("Winrate (MA 50)")
    plt.title("Winrate (moving average)")
    plt.ylim(-0.05, 1.05)

    plt.savefig(os.path.join(metrics_dir, f"winrate_{run_id}.png"))
    plt.savefig(os.path.join("gui/img", f"winrate_{run_id}.png"))
    plt.savefig(os.path.join("gui/img", "winrate.png"))
    plt.close()

    # --- VP diff plot ---
    vp_ma = moving_avg(vp_diff, window=50)
    plt.figure()
    plt.plot(ep_idx, vp_diff)
    plt.plot(ep_idx, vp_ma)
    plt.xlabel("Episodes")
    plt.ylabel("VP diff (model - player)")
    plt.title("VP diff (per episode + MA 50)")

    plt.savefig(os.path.join(metrics_dir, f"vpdiff_{run_id}.png"))
    plt.savefig(os.path.join("gui/img", f"vpdiff_{run_id}.png"))
    plt.savefig(os.path.join("gui/img", "vpdiff.png"))
    plt.close()

    # --- End reasons bar ---
    reasons = [r["end_reason"] for r in ep_rows]
    c = Counter(reasons)
    keys = sorted(c.keys())
    vals = [c[k] for k in keys]

    plt.figure()
    plt.bar(keys, vals)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Count")
    plt.title("End reasons")
    plt.tight_layout()

    plt.savefig(os.path.join(metrics_dir, f"endreasons_{run_id}.png"))
    plt.savefig(os.path.join("gui/img", f"endreasons_{run_id}.png"))
    plt.savefig(os.path.join("gui/img", "endreasons.png"))
    plt.close()

    print(f"[metrics] saved: {csv_path}")


def _safe_div(n: float, d: float) -> float:
    return float(n) / float(d) if float(d) > 0 else 0.0


def save_heuristic_metrics_snapshot(run_id: str, ep_rows: list[dict] | None = None, metrics_dir: str = "metrics") -> str | None:
    """
    Агрегирует ключевые метрики эвристики из train-логов и сохраняет JSON:
    - metrics/heur_metrics_<run_id>.json
    - metrics/heur_metrics_latest.json
    """
    log_path = os.path.abspath(AGENT_TRAIN_LOG_FILE)
    if not os.path.exists(log_path):
        return None

    mode_counts = {"kite": 0, "hold": 0, "commit": 0}
    role_counts = {"ranged": 0, "hybrid": 0, "melee": 0}
    risk_vals: list[float] = []
    cover_vals: list[float] = []
    invalid_vals: list[float] = []
    fallback_count = 0
    shoot_overkill_vals: list[float] = []
    charge_attempts = 0
    charge_success = 0
    win_rate = 0.0
    draw_rate = 0.0
    turn_limit_rate = 0.0

    try:
        with open(log_path, "r", encoding="utf-8", errors="replace") as handle:
            all_lines = handle.readlines()
            start_idx = 0
            for idx, line in enumerate(all_lines):
                if "[TRAIN][START]" in line:
                    start_idx = idx
            for line in all_lines[start_idx:]:
                if "[ENEMY][HEUR][MOVE]" in line:
                    mode_match = re.search(r"mode=(kite|hold|commit)", line)
                    if mode_match:
                        mode_counts[mode_match.group(1)] += 1
                    role_match = re.search(r"enemy_role=(ranged|hybrid|melee)", line)
                    if role_match:
                        role_counts[role_match.group(1)] += 1
                    risk_match = re.search(r"risk=([-\d\.]+)", line)
                    if risk_match:
                        risk_vals.append(float(risk_match.group(1)))
                    cover_match = re.search(r"cover=([-\d\.]+)", line)
                    if cover_match:
                        cover_vals.append(float(cover_match.group(1)))
                if "[ENEMY][HEUR][CHARGE]" in line:
                    charge_attempts += 1
                if "Reward (чардж): success_bonus" in line:
                    charge_success += 1
                if "fallback_target=" in line:
                    fallback_count += 1
                if "[ENEMY][HEUR][SHOOT]" in line:
                    ovk_match = re.findall(r"ovk=([-\d\.]+)", line)
                    for token in ovk_match:
                        shoot_overkill_vals.append(float(token))
                if "[TRAIN][ACTIONS]" in line:
                    invalid_block = re.search(r"invalid_rate=\{([^}]*)\}", line)
                    if invalid_block:
                        vals = re.findall(r":([0-9\.]+)", invalid_block.group(1))
                        if vals:
                            avg_inv = sum(float(v) for v in vals) / len(vals)
                            invalid_vals.append(avg_inv)
                if "[EVAL][DET]" in line:
                    m = re.search(r"win_rate=([0-9\.]+)", line)
                    if m:
                        win_rate = float(m.group(1))
                    m = re.search(r"draw_rate=([0-9\.]+)", line)
                    if m:
                        draw_rate = float(m.group(1))
                    m = re.search(r"turn_limit_rate=([0-9\.]+)", line)
                    if m:
                        turn_limit_rate = float(m.group(1))
    except OSError:
        return None

    total_games = len(ep_rows) if ep_rows else 0
    model_wins = sum(1 for r in (ep_rows or []) if str(r.get("result", "")) == "win")
    model_draws = sum(1 for r in (ep_rows or []) if str(r.get("result", "")) == "draw")
    heur_wins = sum(1 for r in (ep_rows or []) if str(r.get("result", "")) == "loss")

    os.makedirs(metrics_dir, exist_ok=True)
    payload = {
        "run_id": str(run_id),
        "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        # DET-EVAL метрики (сохраняем для отладки, но UI эвристики может их игнорировать)
        "winrate": float(win_rate),
        "draw_rate": float(draw_rate),
        "turn_limit_rate": float(turn_limit_rate),
        # Метрики эвристики по ВСЕМ тренировочным играм текущего рана
        "train_total_games": int(total_games),
        "train_heur_winrate": _safe_div(float(heur_wins), float(total_games)),
        "train_model_winrate": _safe_div(float(model_wins), float(total_games)),
        "train_draw_rate": _safe_div(float(model_draws), float(total_games)),
        "invalid_rate_total": float(sum(invalid_vals) / len(invalid_vals)) if invalid_vals else 0.0,
        "mode_usage": mode_counts,
        "role_usage": role_counts,
        "avg_risk": float(sum(risk_vals) / len(risk_vals)) if risk_vals else 0.0,
        "avg_cover": float(sum(cover_vals) / len(cover_vals)) if cover_vals else 0.0,
        "charge_attempt_rate": _safe_div(charge_attempts, max(1, len(risk_vals))),
        "charge_success_rate": _safe_div(charge_success, max(1, charge_attempts)),
        "shoot_overkill_rate": _safe_div(sum(1 for v in shoot_overkill_vals if v > 0.15), max(1, len(shoot_overkill_vals))),
        "fallback_rate": _safe_div(fallback_count, max(1, charge_attempts + len(shoot_overkill_vals))),
    }
    out_path = os.path.join(metrics_dir, f"heur_metrics_{run_id}.json")
    latest_path = os.path.join(metrics_dir, "heur_metrics_latest.json")
    try:
        with open(out_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
        with open(latest_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
    except OSError:
        return None
    return out_path

def save_training_summary(run_id: str, model_tag: str, ep_rows: list[dict], elapsed_s: float, results_path: str = "results.txt") -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ep_count = len(ep_rows)
    if ep_count > 0:
        winrate_mean = sum(1 for r in ep_rows if r.get("result") == "win") / ep_count
        vp_diff_mean = sum(r.get("vp_diff", 0) for r in ep_rows) / ep_count
        reward_mean = sum(r.get("ep_reward", 0.0) for r in ep_rows) / ep_count
        ep_len_mean = sum(r.get("ep_len", 0) for r in ep_rows) / ep_count
        turn_mean = sum(r.get("turn", 0) for r in ep_rows) / ep_count
    else:
        winrate_mean = 0.0
        vp_diff_mean = 0.0
        reward_mean = 0.0
        ep_len_mean = 0.0
        turn_mean = 0.0

    summary_line = (
        f"время={timestamp} "
        f"длительность_с={elapsed_s:.2f} "
        f"модель={model_tag} "
        f"run_id={run_id} "
        f"эпизоды={ep_count} "
        f"winrate_mean={winrate_mean:.4f} "
        f"vp_diff_mean={vp_diff_mean:.4f} "
        f"reward_mean={reward_mean:.6f} "
        f"ep_len_mean={ep_len_mean:.2f} "
        f"turn_mean={turn_mean:.2f}"
    )
    with open(results_path, "a", encoding="utf-8") as f:
        f.write(summary_line + "\n")
    print(f"[results] запись в {results_path}: {summary_line}")

def append_agent_log(line: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_line = f"{timestamp} | {line}\n"
    with _TRAIN_LOG_LOCK:
        _TRAIN_LOG_BUFFER.append(full_line)
    _flush_agent_log_buffer(force=False)


def _log_train(line: str) -> None:
    """Лог в `LOGS_FOR_AGENTS_TRAIN.md` + (опционально) в консоль."""
    if TRAIN_LOG_TO_CONSOLE:
        # Печатаем без timestamp, чтобы консоль не была слишком шумной.
        print(line)
    append_agent_log(line)


def _units_as_inline(units: list[dict]) -> str:
    """Компактное человеко-читаемое представление ростера."""
    parts: list[str] = []
    for spec in units or []:
        name = str(spec.get("name") or "-").strip()
        count = spec.get("count", None)
        count_part = ""
        try:
            if count is not None and float(count) > 0:
                # В roster_config count обычно целое.
                count_part = f" x{int(float(count))}"
        except (TypeError, ValueError):
            pass

        weapons = spec.get("weapons") or ()
        ranged = ""
        melee = ""
        if isinstance(weapons, (list, tuple)) and len(weapons) >= 2:
            ranged = str(weapons[0] or "").strip()
            melee = str(weapons[1] or "").strip()
        elif isinstance(weapons, str):
            ranged = weapons.strip()

        weapons_part = ""
        if ranged and melee and ranged.lower() != "none" and melee.lower() != "none":
            weapons_part = f" ({ranged} / {melee})"
        elif ranged and ranged.lower() != "none":
            weapons_part = f" ({ranged})"

        parts.append(f"{name}{count_part}{weapons_part}")

    return "; ".join(parts) if parts else "-"


def _opponent_type_label(
    *,
    opponent_policy_net,
    opponent_source_state: dict[str, object],
    self_play_enabled: bool,
) -> tuple[str, str]:
    """Возвращает: (тип, agent_id_text)."""
    if not self_play_enabled or opponent_policy_net is None:
        return "эвристика (policy_net отсутствует)", "-"

    source = str(opponent_source_state.get("source") or "").strip()
    agent_id = opponent_source_state.get("id", None)

    if source in {"roster", "roster_fixed"}:
        return "policy (roster_fixed)", str(agent_id) if agent_id is not None else "-"
    if source == "explicit":
        # Явно заданный agent_id, но по смыслу это всё равно roster_fixed-оппонент.
        return "policy (roster_fixed / explicit)", str(agent_id) if agent_id is not None else "-"
    if source == "fixed_checkpoint":
        return "policy (fixed_checkpoint)", "-"
    if source.startswith("pool") or source in {"latest_init"}:
        return f"policy (snapshot: {source})", f"{agent_id}" if agent_id is not None else "-"

    # fallback
    return f"policy ({source or 'unknown'})", str(agent_id) if agent_id is not None else "-"


def _log_roster_and_opponent_summary(
    *,
    learner_identity: AgentIdentity,
    roster_config: dict,
    opponent_policy_net,
    opponent_source_state: dict[str, object],
    self_play_enabled: bool,
    league_enabled: bool,
) -> None:
    mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
    learner_side = str(learner_identity.side or "").strip().upper() or "P1"
    learner_faction = str(learner_identity.faction or "Unknown").strip()

    opponent_side = "P2" if learner_side == "P1" else "P1"
    opponent_faction = str(roster_config.get("enemy_faction", "Unknown")).strip()

    model_units = roster_config.get("model_units", []) or []
    enemy_units = roster_config.get("enemy_units", []) or []

    opponent_type, opponent_agent_id_text = _opponent_type_label(
        opponent_policy_net=opponent_policy_net,
        opponent_source_state=opponent_source_state,
        self_play_enabled=self_play_enabled,
    )

    league_hint = "включена" if league_enabled else "выключена"

    # Важно для GUI: каждая строка должна начинаться с нужного префикса,
    # иначе GUI-фильтр не покажет часть многострочного блока.
    _log_train(f"[TRAIN][CONFIG] Миссия: {mission_name}")
    _log_train(f"[TRAIN][CONFIG] Обучение: {learner_side} ({learner_faction})")
    _log_train(f"[TRAIN][CONFIG] Heuristic mode: {HEURISTIC_MODE}")
    _log_train(f"[TRAIN][CONFIG] League: {league_hint}")

    _log_train(f"[TRAIN][ROSTER] model_units (сторона обучения): {_units_as_inline(model_units)}")
    _log_train(f"[TRAIN][ROSTER] enemy_units (оппонент): {_units_as_inline(enemy_units)}")

    _log_train(f"[TRAIN][OPPONENT] Тип: {opponent_type}")
    _log_train(f"[TRAIN][OPPONENT] side/faction (из ростера): {opponent_side} ({opponent_faction})")
    _log_train(f"[TRAIN][OPPONENT] agent_id: {opponent_agent_id_text}")


_TRAIN_LOG_BUFFER: list[str] = []
_TRAIN_LOG_LOCK = threading.Lock()
_TRAIN_LOG_LAST_FLUSH = time.monotonic()


def _flush_agent_log_buffer(force: bool = False) -> None:
    global _TRAIN_LOG_LAST_FLUSH
    max_lines = max(1, int(os.getenv("TRAIN_LOG_BUFFER_LINES", "64") or "64"))
    flush_interval = max(0.1, float(os.getenv("TRAIN_LOG_FLUSH_INTERVAL_SEC", "1.0") or "1.0"))

    with _TRAIN_LOG_LOCK:
        now = time.monotonic()
        if not force and len(_TRAIN_LOG_BUFFER) < max_lines and (now - _TRAIN_LOG_LAST_FLUSH) < flush_interval:
            return
        lines = list(_TRAIN_LOG_BUFFER)
        _TRAIN_LOG_BUFFER.clear()
        _TRAIN_LOG_LAST_FLUSH = now

    if not lines:
        return

    script_path = globals().get("__file__") or sys.argv[0] or "train.py"
    log_path = os.path.join(os.path.dirname(os.path.abspath(script_path)), AGENT_TRAIN_LOG_FILE)
    try:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.writelines(lines)
    except Exception as exc:
        print(f"[LOG][WARN] Не удалось записать LOGS_FOR_AGENTS_TRAIN.md: {exc}")


atexit.register(lambda: _flush_agent_log_buffer(force=True))

def _env_worker(conn, roster_config, b_len, b_hei, trunc):
    try:
        lean_info_enabled = os.getenv("TRAIN_LEAN_INFO", "1") == "1"

        def _lean_train_info(info):
            if not isinstance(info, dict):
                return info
            # Lean info для train-mode: уменьшаем IPC payload, оставляем только нужные поля.
            return {
                "model health": info.get("model health", []),
                "player health": info.get("player health", []),
                "in attack": info.get("in attack", 0),
                "model VP": info.get("model VP", 0),
                "player VP": info.get("player VP", 0),
                "mission": info.get("mission", DEFAULT_MISSION_NAME),
                "end reason": info.get("end reason", ""),
                "winner": info.get("winner", None),
                "turn": info.get("turn", 0),
            }

        enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
        mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
        attacker_side, defender_side = roll_off_attacker_defender(
            manual_roll_allowed=False,
            log_fn=None,
        )
        deploy_for_mission(
            mission_name,
            model_units=model,
            enemy_units=enemy,
            b_len=b_len,
            b_hei=b_hei,
            attacker_side=attacker_side,
            log_fn=None,
        )
        post_deploy_setup(log_fn=None)

        env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
        env.attacker_side = attacker_side
        env.defender_side = defender_side

        state, info = env.reset(options={"m": model, "e": enemy, "Type": "big", "trunc": True})
        conn.send(
            {
                "state": state,
                "info": info,
                "len_model": len(model),
            }
        )

        while True:
            cmd, payload = conn.recv()
            if cmd == "enemy_turn":
                env_unwrapped = unwrap_env(env)
                env_unwrapped.enemyTurn(trunc=trunc)
                conn.send(True)
            elif cmd == "step":
                next_observation, reward, done, res, info = env.step(payload)
                if lean_info_enabled:
                    info = _lean_train_info(info)
                conn.send((next_observation, reward, done, res, info))
            elif cmd == "reset":
                mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
                attacker_side, defender_side = roll_off_attacker_defender(
                    manual_roll_allowed=False,
                    log_fn=None,
                )
                deployment_mode = str(os.getenv("DEPLOYMENT_MODE", "auto")).strip().lower() or "auto"
                deployment_strategy = str(os.getenv("DEPLOYMENT_STRATEGY", "template_jitter")).strip().lower() or "template_jitter"
                deployment_seed_raw = os.getenv("DEPLOYMENT_SEED", "").strip()
                deployment_seed = None
                if deployment_seed_raw:
                    try:
                        deployment_seed = int(deployment_seed_raw)
                    except ValueError:
                        deployment_seed = None
                deploy_stats = deploy_for_mission(
                    mission_name,
                    model_units=model,
                    enemy_units=enemy,
                    b_len=b_len,
                    b_hei=b_hei,
                    attacker_side=attacker_side,
                    log_fn=None,
                    deployment_seed=deployment_seed,
                    deployment_strategy=deployment_strategy,
                    deployment_mode=deployment_mode,
                )
                post_deploy_setup(log_fn=None)
                env.attacker_side = attacker_side
                env.defender_side = defender_side
                env.deployment_mode = deployment_mode
                env.deployment_rl_stats = deploy_stats if isinstance(deploy_stats, dict) else None
                state, info = env.reset(
                    options={"m": model, "e": enemy, "Type": "small", "trunc": True}
                )
                conn.send((state, info))
            elif cmd == "get_shoot_mask":
                mask = build_shoot_action_mask(env, log_fn=None, debug=False)
                conn.send(mask)
            elif cmd == "get_action_space":
                keys = payload
                sizes = []
                for k in keys:
                    sp = env.action_space.spaces[k]
                    if hasattr(sp, "n"):
                        sizes.append(int(sp.n))
                    elif hasattr(sp, "nvec"):
                        sizes.extend([int(x) for x in sp.nvec])
                    else:
                        raise TypeError(f"Unsupported action space for {k}: {type(sp)}")
                conn.send(sizes)
            elif cmd == "save_pickle":
                try:
                    legacy_path = payload
                    human_path = None
                    if isinstance(payload, dict):
                        legacy_path = payload.get("legacy")
                        human_path = payload.get("human")
                    if not legacy_path:
                        raise ValueError("save_pickle: legacy path is empty")
                    os.makedirs(os.path.dirname(str(legacy_path)) or ".", exist_ok=True)
                    with open(legacy_path, "wb") as file:
                        pickle.dump([env, model, enemy], file)
                    if human_path and str(human_path) != str(legacy_path):
                        os.makedirs(os.path.dirname(str(human_path)) or ".", exist_ok=True)
                        with open(human_path, "wb") as file:
                            pickle.dump([env, model, enemy], file)
                    conn.send({"ok": True, "path": legacy_path, "human_path": human_path})
                except Exception as exc:
                    conn.send({"ok": False, "error": str(exc)})
            elif cmd == "close":
                conn.send(True)
                break
    except Exception as exc:
        try:
            conn.send({"error": str(exc)})
        except Exception:
            pass

def _load_roster_config():
    config = {
        "totLifeT": 10,
        "b_len": 40,
        "b_hei": 60,
        "mission": DEFAULT_MISSION_NAME,
        "enemy_faction": "Necrons",
        "model_faction": "Necrons",
        "enemy_units": [
            {
                "name": "Necron Warriors",
                "weapons": ("Gauss flayer", "Necron close combat weapon"),
                "count": None,
                "instance_id": None,
            },
            {
                "name": "Royal Warden",
                "weapons": ("Relic gauss blaster", "Royal warden close combat weapon"),
                "count": None,
                "instance_id": None,
            },
        ],
        "model_units": [
            {
                "name": "Necron Warriors",
                "weapons": ("Gauss flayer", "Necron close combat weapon"),
                "count": None,
                "instance_id": None,
            },
            {
                "name": "Royal Warden",
                "weapons": ("Relic gauss blaster", "Royal warden close combat weapon"),
                "count": None,
                "instance_id": None,
            },
        ],
    }

    if os.path.isfile("gui/data.json"):
        config["totLifeT"] = initFile.getNumLife()
        config["b_len"] = initFile.getBoardX()
        config["b_hei"] = initFile.getBoardY()
        config["enemy_faction"] = initFile.getEnemyFaction()
        config["model_faction"] = initFile.getModelFaction()
        config["mission"] = normalize_mission_name(getattr(initFile, "getMission", lambda: DEFAULT_MISSION_NAME)())
        enemy_counts = initFile.getEnemyUnitCounts()
        model_counts = initFile.getModelUnitCounts()
        enemy_instance_ids = initFile.getEnemyUnitInstanceIds()
        model_instance_ids = initFile.getModelUnitInstanceIds()

        enemy_units = []
        for i in range(len(initFile.getEnemyUnits())):
            count = enemy_counts[i] if i < len(enemy_counts) and enemy_counts[i] > 0 else None
            instance_id = enemy_instance_ids[i] if i < len(enemy_instance_ids) else None
            enemy_units.append(
                {
                    "name": initFile.getEnemyUnits()[i],
                    "weapons": (initFile.getEnemyW()[i][0], initFile.getEnemyW()[i][1]),
                    "count": count,
                    "instance_id": instance_id,
                }
            )

        model_units = []
        for i in range(len(initFile.getModelUnits())):
            count = model_counts[i] if i < len(model_counts) and model_counts[i] > 0 else None
            instance_id = model_instance_ids[i] if i < len(model_instance_ids) else None
            model_units.append(
                {
                    "name": initFile.getModelUnits()[i],
                    "weapons": (initFile.getModelW()[i][0], initFile.getModelW()[i][1]),
                    "count": count,
                    "instance_id": instance_id,
                }
            )

        config["enemy_units"] = enemy_units
        config["model_units"] = model_units

    config["mission"] = normalize_mission_name(config.get("mission", os.getenv("MISSION_NAME", DEFAULT_MISSION_NAME)))
    config["b_len"], config["b_hei"] = board_dims_for_mission(config["mission"])

    return config

def _build_units_from_config(config, b_len, b_hei):
    enemy = []
    model = []
    for spec in config["enemy_units"]:
        unit_data = unitData(config["enemy_faction"], spec["name"])
        if spec["count"]:
            unit_data["#OfModels"] = spec["count"]
        enemy.append(
            Unit(
                unit_data,
                weaponData(spec["weapons"][0]),
                weaponData(spec["weapons"][1]),
                b_len,
                b_hei,
                instance_id=spec["instance_id"],
            )
        )
    for spec in config["model_units"]:
        unit_data = unitData(config["model_faction"], spec["name"])
        if spec["count"]:
            unit_data["#OfModels"] = spec["count"]
        model.append(
            Unit(
                unit_data,
                weaponData(spec["weapons"][0]),
                weaponData(spec["weapons"][1]),
                b_len,
                b_hei,
                instance_id=spec["instance_id"],
            )
        )
    return enemy, model

def _sample_random_action_from_sizes(action_sizes, shoot_mask=None):
    action_list = [random.randrange(int(size)) for size in action_sizes]
    if shoot_mask is not None and len(action_list) > 2:
        mask = torch.as_tensor(shoot_mask, dtype=torch.bool)
        valid_indices = torch.where(mask)[0].tolist()
        if valid_indices:
            action_list[2] = random.choice(valid_indices)
    return action_list


def _select_actions_batch(env_contexts, states, steps_done, policy_net, action_sizes, shoot_masks=None):
    decay_steps = max(1.0, float(EPS_DECAY))
    progress = min(float(steps_done) / decay_steps, 1.0)
    eps_threshold = EPS_START + (EPS_END - EPS_START) * progress

    dev = next(policy_net.parameters()).device
    state_tensors = []
    for state in states:
        if isinstance(state, (dict, collections.OrderedDict)):
            arr = np.array(list(state.values()), dtype=np.float32)
        else:
            arr = np.array(state, dtype=np.float32)
        state_tensors.append(torch.tensor(arr, dtype=torch.float32, device=dev))
    state_batch = torch.stack(state_tensors, dim=0)

    actions = []
    with torch.no_grad():
        decision = policy_net(state_batch)

    for env_idx, ctx in enumerate(env_contexts):
        env = ctx.get("env")
        use_random = random.random() <= eps_threshold
        if use_random:
            if env is None:
                action_list = _sample_random_action_from_sizes(
                    action_sizes,
                    shoot_mask=shoot_masks[env_idx] if shoot_masks else None,
                )
            else:
                sampled_action = env.action_space.sample()
                shoot_choice = sampled_action["shoot"]
                if shoot_masks and shoot_masks[env_idx] is not None:
                    mask = torch.as_tensor(shoot_masks[env_idx], dtype=torch.bool)
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
                for i in range(ctx["len_model"]):
                    label = "move_num_" + str(i)
                    action_list.append(sampled_action[label])
            actions.append(torch.tensor([action_list], device="cpu"))
        else:
            action = []
            for head_idx, head in enumerate(decision):
                head_row = head[env_idx]
                if head_idx == 2 and shoot_masks and shoot_masks[env_idx] is not None:
                    mask = torch.as_tensor(shoot_masks[env_idx], dtype=torch.bool, device=head_row.device)
                    if mask.numel() == head_row.numel() and mask.any():
                        masked_head = head_row.clone()
                        masked_head[~mask] = -1e9
                        action.append(int(masked_head.argmax().item()))
                        continue
                action.append(int(head_row.argmax().item()))
            actions.append(torch.tensor([action], device="cpu"))
    return actions, eps_threshold

TAU = data["tau"]
LR = data["lr"]
GAMMA = data["gamma"]
NET_TYPE = "dueling" if DUELING_ENABLED else "basic"
CLIP_REWARD = os.getenv("CLIP_REWARD", "off")
GRAD_CLIP_VALUE = 100.0

# ============================================================
# (C) Несколько обучающих апдейтов на один шаг среды
# ============================================================
UPDATES_PER_STEP = int(data.get("updates_per_step", 1))  # 1 = как было раньше
WARMUP_STEPS     = int(data.get("warmup_steps", 0))      # 0 = без прогрева

def main():
    global USE_SUBPROC_ENVS
    print("\nTraining...\n")
    train_start_time = time.perf_counter()
    clip_reward_enabled, clip_reward_min, clip_reward_max = parse_clip_reward_config(CLIP_REWARD)
    
    end = False
    trunc = True
    
    roster_config = _load_roster_config()
    totLifeT = roster_config["totLifeT"]
    episodes_override_raw = str(os.getenv("TRAIN_EPISODES_OVERRIDE", "")).strip()
    if episodes_override_raw:
        try:
            episodes_override = max(1, int(episodes_override_raw))
            totLifeT = episodes_override
        except ValueError:
            warn_line = (
                "[TRAIN][WARN] TRAIN_EPISODES_OVERRIDE не число. "
                "Где: train.py (main). Что делать дальше: используйте целое > 0."
            )
            if TRAIN_LOG_TO_FILE:
                append_agent_log(warn_line)
            if TRAIN_LOG_TO_CONSOLE:
                print(warn_line)
    b_len = roster_config["b_len"]
    b_hei = roster_config["b_hei"]
    
    vec_env_count = int(os.getenv("NUM_ENVS", os.getenv("VEC_ENV_COUNT", "1")))
    if vec_env_count < 1:
        vec_env_count = 1
    deployment_mode = str(os.getenv("DEPLOYMENT_MODE", "auto")).strip().lower() or "auto"
    manual_in_rl_phase = os.getenv("DEPLOYMENT_PLAYER_MANUAL_IN_RL_PHASE", "1").strip().lower() not in {"0", "false", "no"}
    stdin_is_tty = bool(getattr(sys.stdin, "isatty", lambda: False)())
    if not stdin_is_tty:
        if deployment_mode == "manual_player":
            warn_msg = (
                "[TRAIN][WARN] DEPLOYMENT_MODE=manual_player в неинтерактивном процессе. "
                "Где: train.py (main). Что делать дальше: переключаю DEPLOYMENT_MODE=auto, "
                "иначе тренировка зависнет в ожидании ручного ввода."
            )
            print(warn_msg)
            append_agent_log(warn_msg)
            deployment_mode = "auto"
            os.environ["DEPLOYMENT_MODE"] = "auto"
        if deployment_mode == "rl_phase" and manual_in_rl_phase:
            warn_msg = (
                "[TRAIN][WARN] DEPLOYMENT_MODE=rl_phase + ручной деплой игрока в неинтерактивном процессе. "
                "Где: train.py (main). Что делать дальше: выставляю DEPLOYMENT_PLAYER_MANUAL_IN_RL_PHASE=0, "
                "иначе запуск зависнет на первом reset/deploy."
            )
            print(warn_msg)
            append_agent_log(warn_msg)
            os.environ["DEPLOYMENT_PLAYER_MANUAL_IN_RL_PHASE"] = "0"
            manual_in_rl_phase = False
    
    if USE_SUBPROC_ENVS and vec_env_count < 2:
        USE_SUBPROC_ENVS = False
    if USE_SUBPROC_ENVS and SELF_PLAY_ENABLED:
        warn_msg = "[WARN] USE_SUBPROC_ENVS=1 несовместим с SELF_PLAY_ENABLED=1, отключаю subprocess env."
        print(warn_msg)
        append_agent_log(warn_msg)
        USE_SUBPROC_ENVS = False
    
    if TRAIN_LOG_ENABLED:
        if clip_reward_enabled:
            clip_reward_mode = f"on[{clip_reward_min:.3f},{clip_reward_max:.3f}]"
        else:
            clip_reward_mode = "off"
        update_ratio = float(UPDATES_PER_STEP) / max(1.0, float(vec_env_count))
        train_start_line = (
            "[TRAIN][START] "
            f"DoubleDQN={int(DOUBLE_DQN_ENABLED)} "
            f"Dueling={int(DUELING_ENABLED)} "
            f"PER={int(PER_ENABLED)} "
            f"N_STEP={N_STEP} "
            f"LR={LR} "
            f"clip_reward={clip_reward_mode} "
            f"grad_clip={GRAD_CLIP_VALUE} "
            f"NUM_ENVS={vec_env_count} "
            f"UPDATES_PER_STEP={UPDATES_PER_STEP} "
            f"update_ratio={update_ratio:.3f} "
            f"WARMUP_STEPS={WARMUP_STEPS} "
            f"BATCH_ACT={int(BATCH_ACT)} "
            f"USE_AMP={int(USE_AMP)} "
            f"USE_COMPILE={int(USE_COMPILE)} "
            f"USE_SUBPROC_ENVS={int(USE_SUBPROC_ENVS)} "
            f"PREFETCH={int(PREFETCH)} "
            f"PIN_MEMORY={int(PIN_MEMORY)} "
            f"LOG_EVERY={LOG_EVERY} "
            f"SAVE_EVERY={SAVE_EVERY}"
        )
        if TRAIN_LOG_TO_FILE:
            append_agent_log(train_start_line)
        if TRAIN_LOG_TO_CONSOLE:
            print(train_start_line)
        boot_env_line = (
            "[TRAIN][BOOT] "
            f"SELF_PLAY_ENABLED={int(SELF_PLAY_ENABLED)} "
            f"SELF_PLAY_OPPONENT_MODE={SELF_PLAY_OPPONENT_MODE} "
            f"SELF_PLAY_OPP_EPS_MIN={SELF_PLAY_OPPONENT_EPSILON_MIN:.3f} "
            f"SELF_PLAY_OPP_EPS_MAX={SELF_PLAY_OPPONENT_EPSILON_MAX:.3f} "
            f"SELF_PLAY_OPP_EPS_DECAY_EP={SELF_PLAY_OPPONENT_EPSILON_DECAY_EPISODES} "
            f"SELF_PLAY_ADAPTIVE_UPDATE={int(SELF_PLAY_ADAPTIVE_UPDATE)} "
            f"SELF_PLAY_POOL_ENABLED={int(SELF_PLAY_POOL_ENABLED)} "
            f"SELF_PLAY_POOL_SIZE={SELF_PLAY_POOL_SIZE} "
            f"SELF_PLAY_POOL_SAMPLE_OLD_PROB={SELF_PLAY_POOL_SAMPLE_OLD_PROB:.2f} "
            f"SELF_PLAY_POOL_SMART_SAMPLING={int(SELF_PLAY_POOL_SMART_SAMPLING)} "
            f"SELF_PLAY_POOL_EMA_ENABLED={int(SELF_PLAY_POOL_EMA_ENABLED)} "
            f"SELF_PLAY_POOL_EMA_ALPHA={SELF_PLAY_POOL_EMA_ALPHA:.3f} "
            f"SELF_PLAY_POOL_MIN_GAMES_FOR_SMART={SELF_PLAY_POOL_MIN_GAMES_FOR_SMART} "
            f"RESUME_CHECKPOINT={'set' if bool(RESUME_CHECKPOINT) else 'empty'} "
            f"DEPLOYMENT_MODE={deployment_mode} "
            f"DEPLOYMENT_PLAYER_MANUAL_IN_RL_PHASE={int(manual_in_rl_phase)} "
            f"stdin_is_tty={int(stdin_is_tty)} "
            f"EVAL_WINDOW_EPISODES={EVAL_WINDOW_EPISODES} "
            f"TRAIN_EPISODES_OVERRIDE={(episodes_override_raw if episodes_override_raw else 'off')} "
            f"DRAW_PIT_ALERT_RATE={DRAW_PIT_ALERT_RATE:.2f} "
            f"DRAW_PIT_ALERT_WIN_MAX={DRAW_PIT_ALERT_WIN_MAX:.2f} "
            f"BEST_EVAL_ENABLED={int(BEST_EVAL_ENABLED)} "
            f"DRAW_GUARD_ENABLED={int(DRAW_GUARD_ENABLED)} "
            f"DET_EVAL_ENABLED={int(DET_EVAL_ENABLED)} "
            f"REWARD_SCHEDULE_ENABLED={int(REWARD_SCHEDULE_ENABLED)}"
        )
        if TRAIN_LOG_TO_FILE:
            append_agent_log(boot_env_line)
        if TRAIN_LOG_TO_CONSOLE:
            print(boot_env_line)
        if update_ratio < 0.25:
            ratio_warn = (
                "[TRAIN][WARN] Низкий update_ratio: "
                f"updates_per_step={UPDATES_PER_STEP}, num_envs={vec_env_count}, ratio={update_ratio:.3f}. "
                "Что делать: повысить updates_per_step или уменьшить NUM_ENVS, иначе возможно недообучение."
            )
            if TRAIN_LOG_TO_FILE:
                append_agent_log(ratio_warn)
            if TRAIN_LOG_TO_CONSOLE:
                print(ratio_warn)
    
    if USE_SUBPROC_ENVS and RENDER_EVERY > 0:
        warn_msg = "[WARN] USE_SUBPROC_ENVS=1: рендер в subprocess env недоступен, рендер будет пропущен."
        print(warn_msg)
        append_agent_log(warn_msg)
    
    env_contexts = []
    subproc_envs = []
    subproc_conns = []
    
    
    verbose = os.getenv("VERBOSE_LOGS", "0") == "1"
    log_fn = print if verbose else None
    
    if USE_SUBPROC_ENVS:
        ctx = mp.get_context("spawn")
        for env_idx in range(vec_env_count):
            parent_conn, child_conn = ctx.Pipe()
            proc = ctx.Process(
                target=_env_worker,
                args=(child_conn, roster_config, b_len, b_hei, trunc),
                daemon=True,
            )
            proc.start()
            init_payload = parent_conn.recv()
            if isinstance(init_payload, dict) and init_payload.get("error"):
                raise RuntimeError(init_payload["error"])
            env_contexts.append(
                {
                    "conn": parent_conn,
                    "state": init_payload["state"],
                    "info": init_payload["info"],
                    "len_model": init_payload["len_model"],
                }
            )
            subproc_envs.append(proc)
            subproc_conns.append(parent_conn)
    else:
        for env_idx in range(vec_env_count):
            enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
            env_log_fn = log_fn if env_idx == 0 else None
            mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
            attacker_side, defender_side = roll_off_attacker_defender(
                manual_roll_allowed=False,
                log_fn=print if env_idx == 0 else None,
            )
            if verbose and env_idx == 0:
                # Юниты/ростеры уже выводятся единым “шапочным” блоком выше по логике.
                # Здесь оставляем только компактный sanity-check по количеству.
                print(f"[roster] model_units={len(model)} enemy_units={len(enemy)}")
    
            deploy_for_mission(
                mission_name,
                model_units=model,
                enemy_units=enemy,
                b_len=b_len,
                b_hei=b_hei,
                attacker_side=attacker_side,
                log_fn=env_log_fn,
            )
            post_deploy_setup(log_fn=env_log_fn)
    
            env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
            env.attacker_side = attacker_side
            env.defender_side = defender_side
    
            state, info = env.reset(options={"m": model, "e": enemy, "trunc": True})
            env_contexts.append(
                {
                    "env": env,
                    "model": model,
                    "enemy": enemy,
                    "state": state,
                    "info": info,
                    "attacker_side": attacker_side,
                    "defender_side": defender_side,
                    "len_model": len(model),
                }
            )
    
    primary_ctx = env_contexts[0]
    model = primary_ctx.get("model")
    enemy = primary_ctx.get("enemy")
    env = primary_ctx.get("env")
    
    ordered_keys = ["move", "attack", "shoot", "charge", "use_cp", "cp_on"]
    for i_u in range(primary_ctx["len_model"]):
        ordered_keys.append(f"move_num_{i_u}")
    
    if USE_SUBPROC_ENVS:
        primary_ctx["conn"].send(("get_action_space", ordered_keys))
        n_actions = primary_ctx["conn"].recv()
    else:
        n_actions = []
        for k in ordered_keys:
            sp = env.action_space.spaces[k]
    
            # Discrete (и gym, и gymnasium)
            if hasattr(sp, "n"):
                n_actions.append(int(sp.n))
    
            # MultiDiscrete (на всякий)
            elif hasattr(sp, "nvec"):
                n_actions.extend([int(x) for x in sp.nvec])
    
            else:
                raise TypeError(f"Unsupported action space for {k}: {type(sp)}")
    
    
    state = primary_ctx["state"]
    info = primary_ctx["info"]
    if verbose and model is not None:
        squads_for_actions_count = len(model)
        print(f"[action_space] squads_for_actions_count={squads_for_actions_count}")
        for idx, unit in enumerate(model):
            unit_data = unit.showUnitData()
            unit_name = unit_data.get("Name", "Unknown")
            print(f"[action_space] squad[{idx}] name={unit_name}")
        total_models_count = 0
        for unit in model:
            unit_data = unit.showUnitData()
            total_models_count += int(unit_data.get("#OfModels", 1))
        print(f"[action_space] total_models_count={total_models_count}")
        move_num_keys = [
            key for key in env.action_space.spaces.keys() if key.startswith("move_num_")
        ]
        print(f"[action_space] move_num_keys_count={len(move_num_keys)}")
    
    # state может быть np.array или OrderedDict
    if isinstance(state, dict) or "OrderedDict" in str(type(state)):
        n_observations = len(list(state.values()))
    else:
        n_observations = int(np.array(state).shape[0])

    learner_side_cfg = LEARNER_SIDE if LEARNER_SIDE in {"P1", "P2"} else "P1"
    learner_identity = AgentIdentity(
        side=learner_side_cfg,
        faction=LEARNER_FACTION,
        ruleset_version=RULESET_VERSION,
    ).normalized()
    env_contract = make_env_contract(
        n_observations=n_observations,
        n_actions=n_actions,
        mission_name=normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME)),
        ruleset_version=learner_identity.ruleset_version,
        extras={
            "vec_env_count": int(vec_env_count),
            "self_play_enabled": int(SELF_PLAY_ENABLED),
        },
    )
    
    if USE_COMPILE and torch.cuda.is_available():
        torch.backends.cudnn.benchmark = True
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        try:
            torch.set_float32_matmul_precision("high")
        except Exception:
            pass
    
    
    policy_net = DQN(n_observations, n_actions, dueling=DUELING_ENABLED).to(device)
    target_net = DQN(n_observations, n_actions, dueling=DUELING_ENABLED).to(device)
    optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)

    replay_capacity = int(os.getenv("REPLAY_CAPACITY", "100000"))
    if PER_ENABLED:
        memory = PrioritizedReplayMemory(replay_capacity, alpha=PER_ALPHA, eps=PER_EPS)
    else:
        memory = ReplayMemory(replay_capacity)

    resume_meta = {
        "global_step": 0,
        "optimize_steps": 0,
        "episode": 0,
        "replay_size": 0,
        "epsilon": float(EPS_START),
    }
    if RESUME_CHECKPOINT:
        resume_meta = _resume_from_checkpoint(policy_net, target_net, optimizer, memory, RESUME_CHECKPOINT)
    else:
        target_net.load_state_dict(normalize_state_dict(policy_net.state_dict()))

    target_net.eval()
    
    if USE_COMPILE and hasattr(torch, "compile"):
        try:
            policy_net = torch.compile(policy_net, mode="reduce-overhead")
            target_net = torch.compile(target_net, mode="reduce-overhead")
        except Exception as exc:
            print(f"[WARN] torch.compile недоступен: {exc}")
    
    opponent_policy_net = None
    current_selfplay_update_every = SELF_PLAY_UPDATE_EVERY_EPISODES
    opponent_eps_state = {"value": float(SELF_PLAY_OPPONENT_EPSILON)}
    opponent_pool_entries = collections.deque(maxlen=SELF_PLAY_POOL_SIZE)
    opponent_pool_next_id = {"value": 1}
    opponent_source_state = {"source": "unset", "id": None, "score": None}
    pool_sampling_state = {"old_prob": float(SELF_PLAY_POOL_SAMPLE_OLD_PROB)}
    draw_guard_state = {"turn_limit_draw_penalty": float(getattr(reward_cfg, "TURN_LIMIT_DRAW_PENALTY", 0.0))}

    def _clone_state_dict_cpu(state_dict: dict) -> dict:
        cloned = {}
        for key, value in state_dict.items():
            if torch.is_tensor(value):
                cloned[key] = value.detach().cpu().clone()
            else:
                cloned[key] = value
        return cloned

    def _load_opponent_state(state_dict: dict, source_label: str, source_id=None, source_score=None) -> None:
        if opponent_policy_net is None:
            return
        opponent_policy_net.load_state_dict(normalize_state_dict(state_dict))
        opponent_source_state["source"] = source_label
        opponent_source_state["id"] = source_id
        opponent_source_state["score"] = source_score

    def _create_pool_entry(state_dict: dict) -> dict:
        entry_id = int(opponent_pool_next_id["value"])
        opponent_pool_next_id["value"] += 1
        return {
            "id": entry_id,
            "state_dict": _clone_state_dict_cpu(state_dict),
            "games": 0,
            "wins": 0,
            "draws": 0,
            "vp_diff_sum": 0.0,
            "ema_win": 0.5,
            "ema_draw": 0.5,
            "ema_vp_diff": 0.0,
        }

    def _pool_entry_score(entry: dict) -> float:
        games = max(0, int(entry.get("games", 0)))
        if games <= 0:
            win_rate = 0.5
            draw_rate = 0.5
            vp_diff_mean = 0.0
        else:
            if SELF_PLAY_POOL_EMA_ENABLED:
                win_rate = float(entry.get("ema_win", 0.5))
                draw_rate = float(entry.get("ema_draw", 0.5))
                vp_diff_mean = float(entry.get("ema_vp_diff", 0.0))
            else:
                win_rate = float(entry.get("wins", 0)) / float(games)
                draw_rate = float(entry.get("draws", 0)) / float(games)
                vp_diff_mean = float(entry.get("vp_diff_sum", 0.0)) / float(games)

        if games < SELF_PLAY_POOL_MIN_GAMES_FOR_SMART:
            # Пока мало наблюдений — смягчаем оценку, чтобы не переоценивать шум.
            confidence = float(games) / max(1.0, float(SELF_PLAY_POOL_MIN_GAMES_FOR_SMART))
            win_rate = 0.5 + (win_rate - 0.5) * confidence
            draw_rate = 0.5 + (draw_rate - 0.5) * confidence
            vp_diff_mean = vp_diff_mean * confidence
        vp_hard = max(0.0, -vp_diff_mean) / max(1.0, float(getattr(reward_cfg, "TURN_LIMIT_VP_MARGIN_CLAMP", 3.0)))
        explore_bonus = SELF_PLAY_POOL_SCORE_EXPLORE_BONUS / float(1 + games)
        score = (
            SELF_PLAY_POOL_SCORE_WIN_W * (1.0 - win_rate)
            + SELF_PLAY_POOL_SCORE_DRAW_W * draw_rate
            + SELF_PLAY_POOL_SCORE_VP_W * vp_hard
            + explore_bonus
        )
        return float(max(1e-6, score))

    def _choose_opponent_from_pool(latest_policy_state: dict):
        if not SELF_PLAY_POOL_ENABLED or len(opponent_pool_entries) == 0:
            return latest_policy_state, "latest", None, None
        sample_old = random.random() < float(pool_sampling_state.get("old_prob", SELF_PLAY_POOL_SAMPLE_OLD_PROB))
        if not sample_old:
            return latest_policy_state, "latest", None, None

        # исключаем самый свежий элемент (он соответствует latest-снапшоту)
        candidates = list(opponent_pool_entries)[:-1] if len(opponent_pool_entries) > 1 else []
        if not candidates:
            return latest_policy_state, "latest", None, None

        if SELF_PLAY_POOL_SMART_SAMPLING:
            weights = [_pool_entry_score(entry) for entry in candidates]
            picked = random.choices(candidates, weights=weights, k=1)[0]
            picked_score = _pool_entry_score(picked)
            return picked["state_dict"], "pool_smart", int(picked.get("id")), float(picked_score)

        picked = random.choice(candidates)
        return picked["state_dict"], "pool_random", int(picked.get("id")), None

    def _choose_opponent_from_roster(
        *,
        desired_side: str,
        desired_faction: str,
        learner_contract: dict[str, object],
    ):
        """
        Выбираем оппонента строго по ростеру:
        - desired_side: противоположная side (P1/P2)
        - desired_faction: фракция с противоположной стороны из roster_config
        """
        desired_side_norm = str(desired_side or "").strip().upper()
        desired_faction_norm = str(desired_faction or "").strip().lower()
        candidates: list[dict[str, object]] = []

        def _load_contract_by_entry(entry: dict[str, object]) -> dict[str, object]:
            contract_path = entry.get("contract_path")
            if not contract_path:
                return {}
            try:
                with open(contract_path, "r", encoding="utf-8") as handle:
                    payload = json.load(handle)
                return payload if isinstance(payload, dict) else {}
            except Exception:
                return {}

        for entry in list_agents():
            entry_side = str(entry.get("side", "")).strip().upper()
            if entry_side != desired_side_norm:
                continue
            entry_faction = str(entry.get("faction", "")).strip().lower()
            if entry_faction != desired_faction_norm:
                continue
            contract = _load_contract_by_entry(entry)
            ok_contract, _ = compatible_contracts(learner_contract, contract)
            if not ok_contract:
                continue
            candidates.append(entry)

        if not candidates:
            return None

        # Если несколько кандидатов: берем самый свежий по updated_at.
        candidates.sort(key=lambda e: str(e.get("updated_at", "")), reverse=True)
        chosen = candidates[0]
        return {
            "agent_id": str(chosen.get("agent_id", "")),
            "source": "roster",
            "reason": f"side={desired_side_norm}, faction={desired_faction_norm}",
        }
    if SELF_PLAY_ENABLED:
        opponent_policy_net = DQN(n_observations, n_actions, dueling=DUELING_ENABLED).to(device)
        opponent_policy_net.eval()
        league_pick = None
        if LEAGUE_ENABLE:
            desired_side = "P2" if str(learner_identity.side).upper() == "P1" else "P1"
            desired_faction = roster_config.get("enemy_faction", "")

            if OPPONENT_AGENT_ID:
                try:
                    payload_explicit = load_agent_by_id(OPPONENT_AGENT_ID)
                    entry = payload_explicit.get("entry", {}) if isinstance(payload_explicit, dict) else {}
                    entry_side = str(entry.get("side", "")).strip().upper()
                    entry_faction = str(entry.get("faction", "")).strip().lower()
                    if entry_side == desired_side and entry_faction == str(desired_faction).strip().lower():
                        league_pick = {"agent_id": OPPONENT_AGENT_ID, "source": "explicit"}
                    else:
                        append_agent_log(
                            "[LEAGUE][WARN] OPPONENT_AGENT_ID задан, но side/faction не совпадают с ростером. "
                            f"skip explicit agent_id={OPPONENT_AGENT_ID} entry_side={entry_side} entry_faction={entry_faction} "
                            f"desired_side={desired_side} desired_faction={str(desired_faction).strip().lower()}"
                        )
                except Exception as exc:
                    append_agent_log(
                        "[LEAGUE][WARN] OPPONENT_AGENT_ID задан, но не удалось загрузить/проверить агент. "
                        f"skip explicit agent_id={OPPONENT_AGENT_ID}. exc={exc}"
                    )

            if league_pick is None:
                picked = _choose_opponent_from_roster(
                    desired_side=desired_side,
                    desired_faction=desired_faction,
                    learner_contract=env_contract,
                )
                if picked is not None:
                    league_pick = picked
        if league_pick is not None:
            selected_id = str(league_pick["agent_id"])
            payload = load_agent_by_id(selected_id)
            ok_contract, mismatch_reason = compatible_contracts(env_contract, payload.get("contract", {}))
            if not ok_contract:
                raise ValueError(
                    f"Несовместимый агент-оппонент '{selected_id}': {mismatch_reason}. "
                    "Что делать: переобучите агента с тем же ruleset/action/obs контрактом."
                )
            loaded_policy = normalize_state_dict(payload["policy_state"])
            opponent_policy_net.load_state_dict(loaded_policy)
            opponent_source_state["source"] = str(league_pick.get("source", "registry"))
            opponent_source_state["id"] = selected_id
            opponent_source_state["score"] = league_pick.get("reason")
            append_agent_log(
                f"[LEAGUE] выбран оппонент agent_id={selected_id} source={opponent_source_state['source']} mode=roster_fixed"
            )
        elif SELF_PLAY_OPPONENT_MODE == "fixed_checkpoint":
            if not SELF_PLAY_FIXED_PATH:
                raise ValueError("SELF_PLAY_FIXED_PATH обязателен для режима fixed_checkpoint.")
            if not os.path.isfile(SELF_PLAY_FIXED_PATH):
                raise FileNotFoundError(
                    f"SELF_PLAY_FIXED_PATH не найден: {SELF_PLAY_FIXED_PATH}. Проверь путь."
                )
            try:
                fixed_load_start = f"[SELFPLAY] loading fixed checkpoint path={SELF_PLAY_FIXED_PATH}"
                print(fixed_load_start)
                append_agent_log(fixed_load_start)
                fixed_start_ts = time.perf_counter()
                checkpoint = torch.load(
                    SELF_PLAY_FIXED_PATH, map_location=device, weights_only=False
                )
                fixed_elapsed = time.perf_counter() - fixed_start_ts
                fixed_loaded = f"[SELFPLAY] fixed checkpoint payload loaded in {fixed_elapsed:.2f}s"
                print(fixed_loaded)
                append_agent_log(fixed_loaded)
            except TypeError:
                checkpoint = torch.load(SELF_PLAY_FIXED_PATH, map_location=device)
                fixed_elapsed = time.perf_counter() - fixed_start_ts
                fixed_loaded = f"[SELFPLAY] fixed checkpoint payload loaded in {fixed_elapsed:.2f}s"
                print(fixed_loaded)
                append_agent_log(fixed_loaded)
            except Exception as exc:
                err_msg = (
                    "[SELFPLAY][ERROR] Не удалось загрузить fixed_checkpoint. "
                    "Где: train.py (torch.load). "
                    "Что делать: убедитесь, что файл модели доверенный и целый, "
                    "или пересохраните чекпойнт текущей версией PyTorch. "
                    f"Детали: {exc}"
                )
                print(err_msg)
                append_agent_log(err_msg)
                raise
            def _normalize_state_dict(state_dict: dict) -> dict:
                if not state_dict:
                    return state_dict
                if any(key.startswith("_orig_mod.") for key in state_dict.keys()):
                    return {key.replace("_orig_mod.", "", 1): value for key, value in state_dict.items()}
                return state_dict

            if isinstance(checkpoint, dict) and "policy_net" in checkpoint:
                checkpoint_net_type = checkpoint.get("net_type", "basic")
                if checkpoint_net_type != NET_TYPE:
                    warn_msg = (
                        "[SELFPLAY] ВНИМАНИЕ: несовпадение типа сети "
                        f"(checkpoint={checkpoint_net_type}, текущая={NET_TYPE}). "
                        "Стартуем с новой инициализацией."
                    )
                    print(warn_msg)
                    append_agent_log(warn_msg)
                else:
                    opponent_policy_net.load_state_dict(
                        _normalize_state_dict(checkpoint["policy_net"])
                    )
            else:
                if NET_TYPE != "basic":
                    warn_msg = (
                        "[SELFPLAY] ВНИМАНИЕ: старый формат чекпойнта без net_type, "
                        f"а текущая сеть={NET_TYPE}. Стартуем с новой инициализацией."
                    )
                    print(warn_msg)
                    append_agent_log(warn_msg)
                else:
                    opponent_policy_net.load_state_dict(_normalize_state_dict(checkpoint))
            append_agent_log(
                f"[SELFPLAY] fixed_checkpoint path={SELF_PLAY_FIXED_PATH}"
            )
            opponent_source_state["source"] = "fixed_checkpoint"
            opponent_source_state["id"] = None
            opponent_source_state["score"] = None
        else:
            initial_policy_state = normalize_state_dict(policy_net.state_dict())
            _load_opponent_state(initial_policy_state, "latest_init", source_id=None, source_score=None)
            opponent_pool_entries.append(_create_pool_entry(initial_policy_state))

        opponent_eps_state["value"] = float(
            max(
                SELF_PLAY_OPPONENT_EPSILON_MIN,
                min(SELF_PLAY_OPPONENT_EPSILON_MAX, SELF_PLAY_OPPONENT_EPSILON_MAX),
            )
        )

    # Один понятный блок вместо нагромождений:
    _log_roster_and_opponent_summary(
        learner_identity=learner_identity,
        roster_config=roster_config,
        opponent_policy_net=opponent_policy_net,
        opponent_source_state=opponent_source_state,
        self_play_enabled=SELF_PLAY_ENABLED,
        league_enabled=LEAGUE_ENABLE,
    )
    
    scaler = torch.cuda.amp.GradScaler(enabled=USE_AMP)
    
    def opponent_policy(obs, env, len_model):
        if opponent_policy_net is None:
            return None
        action = select_action_with_epsilon(
            env,
            obs,
            opponent_policy_net,
            float(opponent_eps_state["value"]),
            len_model,
        )
        return convertToDict(action)
    
    inText = []
    
    if model is not None and enemy is not None:
        inText.append("Model units:")
        for i in model:
            inText.append("Name: {}, Army Type: {}".format(i.showUnitData()["Name"], i.showUnitData()["Army"]))
        inText.append("Enemy units:")
        for i in enemy:
            inText.append("Name: {}, Army Type: {}".format(i.showUnitData()["Name"], i.showUnitData()["Army"]))
    inText.append("Number of Lifetimes ran: {}\n".format(totLifeT))
    
    pbar_update_every = int(os.getenv("PBAR_UPDATE_EVERY", "5" if os.name == "nt" else "1"))
    pbar_update_every = max(1, pbar_update_every)
    pbar_mininterval = float(os.getenv("PBAR_MININTERVAL", "1.5" if os.name == "nt" else "0.1"))
    pbar_mininterval = max(0.0, pbar_mininterval)
    pbar = tqdm(total=totLifeT, mininterval=pbar_mininterval, miniters=pbar_update_every)
    pending_pbar_updates = 0
    
    for ctx in env_contexts:
        if USE_SUBPROC_ENVS:
            ctx["conn"].send(("reset", None))
            ctx["state"], ctx["info"] = ctx["conn"].recv()
        else:
            ctx["state"], ctx["info"] = ctx["env"].reset(
                options={"m": ctx["model"], "e": ctx["enemy"], "Type": "big", "trunc": True}
            )
        ctx["ep_len"] = 0
        ctx["rew_arr"] = []
        ctx["n_step_buffer"] = collections.deque(maxlen=N_STEP)
        ctx["action_head_total"] = Counter({"move": 0, "attack": 0, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0})
        ctx["action_head_skip"] = Counter({"move": 0, "attack": 0, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0})
        ctx["action_head_invalid"] = Counter({"move": 0, "attack": 0, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0})
        ctx["shoot_windows_with_targets"] = 0
        ctx["shoot_windows_without_targets"] = 0
    
    state = primary_ctx["state"]
    info = primary_ctx["info"]
    
    current_time = datetime.datetime.now()
    date = str(current_time.second)+"-"+str(current_time.microsecond)
    if model is not None and enemy is not None:
        name = "M:"+model[0].showUnitData()["Army"]+"_vs_"+"P:"+enemy[0].showUnitData()["Army"]
    else:
        name = f"M:{roster_config['model_faction']}_vs_P:{roster_config['enemy_faction']}"
    def _sanitize_fs_name(value):
        forbidden = '<>:"/\\\\|?*'
        for ch in forbidden:
            value = value.replace(ch, "_")
        return value
    
    side_tag = f"{learner_identity.side}_{learner_identity.faction}"
    safe_name = _sanitize_fs_name(f"{name}__learner_{side_tag}")
    fold = "models/" + safe_name
    fileName = fold+"/model-"+date+".pickle"
    randNum = np.random.randint(0, 10000000)
    metrics_obj = metrics(fold, randNum, date)
    ep_rows = [] 
    eval_window = collections.deque(maxlen=EVAL_WINDOW_EPISODES)
    draw_pit_alert_streak = 0
    best_eval_score = float("-inf")
    best_eval_episode = 0
    reward_schedule_state = {"stage": None}
    
    global_step = int(resume_meta.get("global_step", 0) or 0)
    optimize_steps = int(resume_meta.get("optimize_steps", 0) or 0)
    perf_stats = {
        "action_select_s": 0.0,
        "enemy_turn_s": 0.0,
        "env_step_s": 0.0,
        "replay_sample_s": 0.0,
        "train_forward_s": 0.0,
        "train_backward_s": 0.0,
        "logging_s": 0.0,
    }
    perf_counts = {
        "env_steps": 0,
        "updates": 0,
        "reward_clipped": 0,
    }
    resume_episode_base = int(resume_meta.get("episode", 0) or 0)
    numLifeT = 0
    if RESUME_CHECKPOINT:
        append_agent_log(
            "[RESUME] Параметры продолжения: "
            f"path={RESUME_CHECKPOINT}, episode_base={resume_episode_base}, global_step={global_step}, "
            f"optimize_steps={optimize_steps}, replay_size={int(resume_meta.get('replay_size', 0) or 0)}, "
            f"eps_at_resume={float(resume_meta.get('epsilon', EPS_START)):.4f}"
        )
    primary_env_unwrapped = unwrap_env(primary_ctx["env"]) if not USE_SUBPROC_ENVS else None
    if primary_env_unwrapped is not None:
        initial_model_hp = float(sum(getattr(primary_env_unwrapped, "unit_health", [])))
        initial_enemy_hp = float(sum(getattr(primary_env_unwrapped, "enemy_health", [])))
        append_agent_log(
            "Старт обучения: "
            f"model_hp_total={initial_model_hp}, enemy_hp_total={initial_enemy_hp}, "
            f"battle_round={getattr(primary_env_unwrapped, 'battle_round', 'n/a')}, trunc={trunc}"
        )
        if trunc:
            append_agent_log(
                "Логи фаз/ходов отключены (trunc=True). "
                "Чтобы включить подробные логи: VERBOSE_LOGS=1 или MANUAL_DICE=1."
            )
        if initial_model_hp <= 0 or initial_enemy_hp <= 0:
            append_agent_log(
                "ВНИМАНИЕ: на старте эпизода обнаружено нулевое здоровье. "
                f"model_hp_total={initial_model_hp}, enemy_hp_total={initial_enemy_hp}. "
                "Это может приводить к мгновенному завершению эпизодов."
            )
    else:
        append_agent_log(
            "Старт обучения: USE_SUBPROC_ENVS=1, начальные HP недоступны из subprocess env."
        )

    def _apply_reward_schedule(total_episode: int) -> None:
        if not REWARD_SCHEDULE_ENABLED:
            return
        if total_episode <= REWARD_STAGE1_END_EP:
            stage = 1
            draw_penalty = REWARD_STAGE1_DRAW_PENALTY
            vp_reward_scale = REWARD_STAGE1_VP_REWARD_SCALE
        elif total_episode <= REWARD_STAGE2_END_EP:
            stage = 2
            draw_penalty = REWARD_STAGE2_DRAW_PENALTY
            vp_reward_scale = REWARD_STAGE2_VP_REWARD_SCALE
        else:
            stage = 3
            draw_penalty = REWARD_STAGE3_DRAW_PENALTY
            vp_reward_scale = REWARD_STAGE3_VP_REWARD_SCALE
        reward_cfg.TURN_LIMIT_DRAW_PENALTY = float(draw_penalty)
        reward_cfg.TURN_LIMIT_VP_MARGIN_REWARD_SCALE = float(vp_reward_scale)
        draw_guard_state["turn_limit_draw_penalty"] = float(draw_penalty)
        if reward_schedule_state["stage"] != stage:
            reward_schedule_state["stage"] = stage
            append_agent_log(
                "[TRAIN][REWARD_SCHEDULE] "
                f"episode={total_episode} stage={stage} "
                f"TURN_LIMIT_DRAW_PENALTY={draw_penalty:.3f} "
                f"TURN_LIMIT_VP_MARGIN_REWARD_SCALE={vp_reward_scale:.3f}"
            )

    def _run_deterministic_eval(total_episode: int) -> None:
        if not DET_EVAL_ENABLED:
            return
        if total_episode <= 0 or total_episode % DET_EVAL_EVERY_EPISODES != 0:
            return
        wins = 0
        draws = 0
        wipeout_enemy = 0
        wipeout_model = 0
        turn_limit = 0
        vp_diff_sum = 0.0
        for eval_i in range(DET_EVAL_EPISODES):
            eval_enemy, eval_model = _build_units_from_config(roster_config, b_len, b_hei)
            mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
            attacker_side, defender_side = roll_off_attacker_defender(manual_roll_allowed=False, log_fn=None)
            deploy_for_mission(
                mission_name,
                model_units=eval_model,
                enemy_units=eval_enemy,
                b_len=b_len,
                b_hei=b_hei,
                attacker_side=attacker_side,
                log_fn=None,
            )
            post_deploy_setup(log_fn=None)
            eval_env = gym.make("40kAI-v0", disable_env_checker=True, enemy=eval_enemy, model=eval_model, b_len=b_len, b_hei=b_hei)
            eval_env.attacker_side = attacker_side
            eval_env.defender_side = defender_side
            state_eval, info_eval = eval_env.reset(options={"m": eval_model, "e": eval_enemy, "trunc": True})
            done_eval = False
            step_guard = 0
            while not done_eval and step_guard < 256:
                step_guard += 1
                shoot_mask_eval = build_shoot_action_mask(eval_env, log_fn=None, debug=False)
                action_eval = select_action_with_epsilon(
                    eval_env,
                    state_eval,
                    policy_net,
                    0.0,
                    len(eval_model),
                    shoot_mask=shoot_mask_eval,
                )
                action_eval_dict = convertToDict(action_eval)
                eval_unwrapped = unwrap_env(eval_env)
                if SELF_PLAY_ENABLED and opponent_policy_net is not None:
                    eval_unwrapped.enemyTurn(
                        trunc=trunc,
                        policy_fn=lambda obs, env=eval_env, lm=len(eval_model): convertToDict(
                            select_action_with_epsilon(
                                env,
                                obs,
                                opponent_policy_net,
                                DET_EVAL_OPPONENT_EPSILON,
                                lm,
                            )
                        ),
                    )
                else:
                    eval_unwrapped.enemyTurn(trunc=trunc)
                next_state_eval, _reward_eval, done_eval, _res_eval, info_eval = eval_env.step(action_eval_dict)
                state_eval = next_state_eval
            end_reason_eval = info_eval.get("end reason", "")
            vp_diff_eval = int(info_eval.get("model VP", 0)) - int(info_eval.get("player VP", 0))
            vp_diff_sum += float(vp_diff_eval)

            if end_reason_eval == "wipeout_enemy":
                wins += 1
                wipeout_enemy += 1
            elif end_reason_eval == "wipeout_model":
                wipeout_model += 1
            elif str(end_reason_eval).startswith("turn_limit"):
                turn_limit += 1
                if vp_diff_eval > 0:
                    wins += 1
                elif vp_diff_eval == 0:
                    draws += 1
            else:
                if vp_diff_eval > 0:
                    wins += 1
                elif vp_diff_eval == 0:
                    draws += 1
            try:
                eval_env.close()
            except Exception:
                pass
        n_eval = max(1, DET_EVAL_EPISODES)
        eval_det_line = (
            "[EVAL][DET] "
            f"episode={total_episode} "
            f"eval_episodes={n_eval} "
            f"win_rate={wins/n_eval:.3f} "
            f"draw_rate={draws/n_eval:.3f} "
            f"turn_limit_rate={turn_limit/n_eval:.3f} "
            f"wipeout_enemy_rate={wipeout_enemy/n_eval:.3f} "
            f"wipeout_model_rate={wipeout_model/n_eval:.3f} "
            f"vp_diff_mean={vp_diff_sum/n_eval:.3f}"
        )
        append_agent_log(eval_det_line)

    _apply_reward_schedule(resume_episode_base + numLifeT)
    
    while end is False:
        shoot_masks = []
        if USE_SUBPROC_ENVS:
            # Batched IPC: сначала отправляем всем env, затем читаем ответы по порядку.
            for ctx in env_contexts:
                ctx["conn"].send(("get_shoot_mask", None))
            for ctx in env_contexts:
                shoot_masks.append(ctx["conn"].recv())
        else:
            for idx, ctx in enumerate(env_contexts):
                mask_log_fn = append_agent_log if idx == 0 else None
                shoot_masks.append(build_shoot_action_mask(ctx["env"], log_fn=mask_log_fn, debug=TRAIN_DEBUG))
    
        states = [ctx["state"] for ctx in env_contexts]
        action_start = time.perf_counter()
        if BATCH_ACT:
            actions, eps_threshold = _select_actions_batch(
                env_contexts,
                states,
                global_step,
                policy_net,
                n_actions,
                shoot_masks,
            )
        else:
            decay_steps = max(1.0, float(EPS_DECAY))
            progress = min(float(global_step) / decay_steps, 1.0)
            eps_threshold = EPS_START + (EPS_END - EPS_START) * progress
            actions = []
            for env_idx, ctx in enumerate(env_contexts):
                actions.append(
                    select_action_with_epsilon(
                        ctx["env"],
                        ctx["state"],
                        policy_net,
                        eps_threshold,
                        ctx["len_model"],
                        shoot_mask=shoot_masks[env_idx],
                    )
                )
        perf_stats["action_select_s"] += time.perf_counter() - action_start
    
        enemy_turn_start = time.perf_counter()
        if USE_SUBPROC_ENVS:
            for ctx in env_contexts:
                ctx["conn"].send(("enemy_turn", None))
            for ctx in env_contexts:
                ctx["conn"].recv()
        else:
            for idx, ctx in enumerate(env_contexts):
                env_unwrapped = unwrap_env(ctx["env"])
                if SELF_PLAY_ENABLED:
                    env_unwrapped.enemyTurn(
                        trunc=trunc,
                        policy_fn=lambda obs, env=ctx["env"], lm=ctx["len_model"]: opponent_policy(obs, env, lm),
                    )
                else:
                    env_unwrapped.enemyTurn(trunc=trunc)
        perf_stats["enemy_turn_s"] += time.perf_counter() - enemy_turn_start
    
        losses = []
        last_td_stats = None
        last_per_beta = PER_BETA_START
        last_loss_value = None
    
        dev = next(policy_net.parameters()).device
    
        action_dicts = []
        for idx, ctx in enumerate(env_contexts):
            ctx["ep_len"] += 1
            action_dict = convertToDict(actions[idx])
            action_dicts.append(action_dict)
            # Локальная аналитика по головам action-space (для [TRAIN][ACTIONS] в конце эпизода)
            for _head in ("move", "attack", "shoot", "charge", "use_cp", "cp_on"):
                ctx["action_head_total"][_head] += 1
            if int(action_dict.get("move", 4)) == 4:
                ctx["action_head_skip"]["move"] += 1
            if int(action_dict.get("attack", 0)) == 0:
                ctx["action_head_skip"]["attack"] += 1
                ctx["action_head_skip"]["charge"] += 1
            if int(action_dict.get("use_cp", 0)) == 0:
                ctx["action_head_skip"]["use_cp"] += 1
            shoot_mask_now = shoot_masks[idx] if idx < len(shoot_masks) else None
            valid_shoot_indices = []
            if shoot_mask_now is not None:
                try:
                    valid_shoot_indices = [j for j, allowed in enumerate(shoot_mask_now) if bool(allowed)]
                except Exception:
                    valid_shoot_indices = []
            if len(valid_shoot_indices) == 0:
                ctx["shoot_windows_without_targets"] += 1
                ctx["action_head_skip"]["shoot"] += 1
            else:
                ctx["shoot_windows_with_targets"] += 1
                shoot_raw = int(action_dict.get("shoot", -1))
                if shoot_raw not in valid_shoot_indices:
                    ctx["action_head_invalid"]["shoot"] += 1

        step_results = [None] * len(env_contexts)
        next_shoot_masks = [None] * len(env_contexts)
        if USE_SUBPROC_ENVS:
            # Batched IPC: сначала отправляем step всем env, затем собираем ответы.
            step_start = time.perf_counter()
            for idx, ctx in enumerate(env_contexts):
                ctx["conn"].send(("step", action_dicts[idx]))
            for idx, ctx in enumerate(env_contexts):
                step_results[idx] = ctx["conn"].recv()
            perf_stats["env_step_s"] += time.perf_counter() - step_start
            perf_counts["env_steps"] += len(env_contexts)

            # Batched IPC для масок стрельбы после шага (только где эпизод не завершён).
            pending_next_mask_indices = []
            for idx, (_next_observation, _reward, done, _res, _info) in enumerate(step_results):
                if not done:
                    env_contexts[idx]["conn"].send(("get_shoot_mask", None))
                    pending_next_mask_indices.append(idx)
            for idx in pending_next_mask_indices:
                next_shoot_masks[idx] = env_contexts[idx]["conn"].recv()

        for idx, ctx in enumerate(env_contexts):
            step_start = time.perf_counter()
            if USE_SUBPROC_ENVS:
                next_observation, reward, done, res, info = step_results[idx]
            else:
                next_observation, reward, done, res, info = ctx["env"].step(action_dicts[idx])
                perf_stats["env_step_s"] += time.perf_counter() - step_start
                perf_counts["env_steps"] += 1
            raw_reward = float(reward)
            ctx["rew_arr"].append(raw_reward)
            reward_for_buffer, reward_was_clipped = maybe_clip_reward(
                raw_reward,
                clip_reward_enabled,
                clip_reward_min,
                clip_reward_max,
            )
            if reward_was_clipped:
                perf_counts["reward_clipped"] += 1
    
            unit_health = info["model health"]
            enemy_health = info["player health"]
            inAttack = info["in attack"]
    
            if inAttack == 1 and trunc is False:
                print("The units are fighting")
    
            if RENDER_EVERY > 0 and not USE_SUBPROC_ENVS and vec_env_count == 1 and (global_step % RENDER_EVERY == 0 or done):
                ctx["env"].render()
    
            mission_name = info.get("mission", DEFAULT_MISSION_NAME)
            message = (
                "Iteration {} ended with reward {}, enemy health {}, model health {}, model VP {}, enemy VP {}, mission {}".format(
                    global_step,
                    reward,
                    enemy_health,
                    unit_health,
                    info["model VP"],
                    info["player VP"],
                    mission_name,
                )
            )
            if trunc is False:
                print(message)
            inText.append(message)
    
            state_t = torch.tensor(to_np_state(ctx["state"]), device=dev).unsqueeze(0)
            next_state_t = None
            next_shoot_mask = None
            if not done:
                next_state_t = torch.tensor(to_np_state(next_observation), device=dev).unsqueeze(0)
                mask_log_fn = append_agent_log if idx == 0 else None
                if USE_SUBPROC_ENVS:
                    next_shoot_mask = next_shoot_masks[idx]
                else:
                    next_shoot_mask = build_shoot_action_mask(ctx["env"], log_fn=mask_log_fn, debug=TRAIN_DEBUG)
    
            ctx["n_step_buffer"].append((state_t, actions[idx], reward_for_buffer, next_state_t, done, next_shoot_mask))
            if len(ctx["n_step_buffer"]) >= N_STEP:
                reward_sum, n_step_next_state, n_step_next_mask, n_step_count = build_n_step_transition(
                    ctx["n_step_buffer"], GAMMA
                )
                reward_sum_t = torch.tensor([reward_sum], device=dev, dtype=torch.float32)
                head_state, head_action, _, _, _, _ = ctx["n_step_buffer"][0]
                memory.push(head_state, head_action, n_step_next_state, reward_sum_t, n_step_count, n_step_next_mask)
                ctx["n_step_buffer"].popleft()
            if done:
                while ctx["n_step_buffer"]:
                    reward_sum, n_step_next_state, n_step_next_mask, n_step_count = build_n_step_transition(
                        ctx["n_step_buffer"], GAMMA
                    )
                    reward_sum_t = torch.tensor([reward_sum], device=dev, dtype=torch.float32)
                    head_state, head_action, _, _, _, _ = ctx["n_step_buffer"][0]
                    memory.push(head_state, head_action, n_step_next_state, reward_sum_t, n_step_count, n_step_next_mask)
                    ctx["n_step_buffer"].popleft()
            ctx["state"] = next_observation
    
            if done is True:
                logging_start = time.perf_counter()
                if SELF_PLAY_ENABLED:
                    append_agent_log(
                        f"Конец эпизода {numLifeT + 1}. "
                        f"[SELFPLAY] enabled=1 mode={SELF_PLAY_OPPONENT_MODE} "
                        f"update_every={current_selfplay_update_every} opp_eps={float(opponent_eps_state.get('value', SELF_PLAY_OPPONENT_EPSILON)):.3f} "
                        f"opponent_source={opponent_source_state.get('source', 'unknown')} "
                        f"opponent_id={opponent_source_state.get('id')} "
                        f"opponent_score={opponent_source_state.get('score')}"
                    )
                end_reason_env = info.get("end reason", "")
                winner_env = info.get("winner")
                model_hp_total = sum(info.get("model health", [])) if isinstance(info.get("model health"), (list, tuple, np.ndarray)) else info.get("model health")
                enemy_hp_total = sum(info.get("player health", [])) if isinstance(info.get("player health"), (list, tuple, np.ndarray)) else info.get("player health")
                if ctx["ep_len"] == 1:
                    append_agent_log(
                        "ВНИМАНИЕ: эпизод завершился на первом шаге. "
                        "Проверьте reset/условия завершения (нулевое здоровье, лимиты хода, "
                        "ошибки расстановки)."
                    )
                pending_pbar_updates += 1
                if pending_pbar_updates >= pbar_update_every or (numLifeT + 1) >= totLifeT:
                    pbar.update(pending_pbar_updates)
                    pending_pbar_updates = 0
                metrics_obj.updateRew(sum(ctx["rew_arr"]) / len(ctx["rew_arr"]))
                metrics_obj.updateEpLen(ctx["ep_len"])
                # ===== extra metrics (winrate / VP diff / end reason) =====
                ep_reward = float(sum(ctx["rew_arr"]) / len(ctx["rew_arr"])) if len(ctx["rew_arr"]) > 0 else 0.0
                model_vp = int(info.get("model VP", 0))
                player_vp = int(info.get("player VP", 0))
                vp_diff = model_vp - player_vp
    
                mh_list = info.get("model health", [])
                ph_list = info.get("player health", [])
    
                def _sum_health(x):
                    try:
                        if isinstance(x, (list, tuple, np.ndarray)):
                            return int(sum(x))
                        return int(x)
                    except Exception:
                        return 0
    
                mh = _sum_health(mh_list)
                ph = _sum_health(ph_list)
    
                end_code = res  # то, что возвращает env (1..3 миссия или 4)
                end_reason_env = info.get("end reason", "")
                turn = int(info.get("turn", ctx["ep_len"]))  # если turn не добавляли в env — будет epLen
    
                if end_reason_env:
                    end_reason = end_reason_env
                    if end_reason_env == "wipeout_enemy":
                        result = "win"
                    elif end_reason_env == "wipeout_model":
                        result = "loss"
                    elif end_reason_env == "turn_limit":
                        if vp_diff > 0:
                            result = "win"
                        elif vp_diff < 0:
                            result = "loss"
                        else:
                            result = "draw"
                    else:
                        if vp_diff > 0:
                            result = "win"
                        elif vp_diff < 0:
                            result = "loss"
                        else:
                            result = "draw"
                elif ph <= 0 and mh > 0:
                    result = "win"
                    end_reason = "wipe_enemy"
                elif mh <= 0 and ph > 0:
                    result = "loss"
                    end_reason = "wipe_model"
                else:
                    mission_name = info.get("mission", DEFAULT_MISSION_NAME)
                    end_reason = f"turn_limit_{mission_name}"
                    if vp_diff > 0:
                        result = "win"
                    elif vp_diff < 0:
                        result = "loss"
                    else:
                        result = "draw"
    
                if result == "win":
                    inText.append("model won!")
                    if trunc is False:
                        print("model won!")
                elif result == "loss":
                    inText.append("enemy won!")
                    if trunc is False:
                        print("enemy won!")
                else:
                    inText.append("draw!")
                    if trunc is False:
                        print("draw!")
    
                resolved_winner = "model" if result == "win" else ("enemy" if result == "loss" else "draw")
                resolved_end_reason = end_reason_env or end_reason
                learner_episode_agent_id = f"{learner_identity.side}_{learner_identity.faction}_live"
                opponent_agent_id = (
                    str(opponent_source_state.get("id"))
                    if opponent_source_state.get("id") is not None
                    else "heuristic_or_snapshot"
                )
                if LEAGUE_ENABLE:
                    record_matchup(
                        learner_agent_id=learner_episode_agent_id,
                        opponent_agent_id=opponent_agent_id,
                        win=(result == "win"),
                        draw=(result == "draw"),
                        vp_diff=float(vp_diff),
                        reason=str(resolved_end_reason),
                    )
                if TRAIN_LOG_TO_FILE:
                    append_agent_log(
                        "Конец эпизода: "
                        f"reason={resolved_end_reason} "
                        f"winner={resolved_winner} "
                        f"winner_env={winner_env} "
                        f"model_hp_total={model_hp_total} enemy_hp_total={enemy_hp_total} "
                        f"model_vp={info.get('model VP')} enemy_vp={info.get('player VP')} "
                        f"turn={info.get('turn')} battle_round={info.get('battle round')}"
                    )
                    steps_denom = max(1, int(ctx.get("ep_len", 0)))
                    skip_counts = ctx.get("action_head_skip", Counter())
                    invalid_counts = ctx.get("action_head_invalid", Counter())
                    append_agent_log(
                        "[TRAIN][ACTIONS] "
                        f"ep={numLifeT + 1} "
                        f"steps={steps_denom} "
                        f"skip={{move:{skip_counts['move']},attack:{skip_counts['attack']},shoot:{skip_counts['shoot']},charge:{skip_counts['charge']},use_cp:{skip_counts['use_cp']},cp_on:{skip_counts['cp_on']}}} "
                        f"invalid={{move:{invalid_counts['move']},attack:{invalid_counts['attack']},shoot:{invalid_counts['shoot']},charge:{invalid_counts['charge']},use_cp:{invalid_counts['use_cp']},cp_on:{invalid_counts['cp_on']}}} "
                        f"skip_rate={{move:{skip_counts['move']/steps_denom:.3f},attack:{skip_counts['attack']/steps_denom:.3f},shoot:{skip_counts['shoot']/steps_denom:.3f},charge:{skip_counts['charge']/steps_denom:.3f},use_cp:{skip_counts['use_cp']/steps_denom:.3f},cp_on:{skip_counts['cp_on']/steps_denom:.3f}}} "
                        f"invalid_rate={{move:{invalid_counts['move']/steps_denom:.3f},attack:{invalid_counts['attack']/steps_denom:.3f},shoot:{invalid_counts['shoot']/steps_denom:.3f},charge:{invalid_counts['charge']/steps_denom:.3f},use_cp:{invalid_counts['use_cp']/steps_denom:.3f},cp_on:{invalid_counts['cp_on']/steps_denom:.3f}}} "
                        f"shoot_windows={{with_targets:{ctx.get('shoot_windows_with_targets', 0)},without_targets:{ctx.get('shoot_windows_without_targets', 0)}}}"
                    )

                if TRAIN_LOG_ENABLED:
                    win_flag = 1 if result == "win" else 0
                    train_ep_line = (
                        "[TRAIN][EP] "
                        f"ep={numLifeT + 1} "
                        f"ep_reward={ep_reward:.6f} "
                        f"win={win_flag} "
                        f"vp_diff={vp_diff} "
                        f"end_reason={end_reason}"
                    )
                    if TRAIN_LOG_TO_FILE:
                        append_agent_log(train_ep_line)
                    if TRAIN_LOG_TO_CONSOLE:
                        print(train_ep_line)

                eval_window.append(
                    {
                        "win": 1 if result == "win" else 0,
                        "draw": 1 if result == "draw" else 0,
                        "wipeout_enemy": 1 if end_reason == "wipeout_enemy" else 0,
                        "wipeout_model": 1 if end_reason == "wipeout_model" else 0,
                        "turn_limit": 1 if str(end_reason).startswith("turn_limit") else 0,
                        "vp_diff": float(vp_diff),
                    }
                )
                should_log_eval_window = (
                    len(eval_window) >= EVAL_WINDOW_EPISODES
                    and ((numLifeT + 1) % EVAL_WINDOW_LOG_EVERY == 0 or (numLifeT + 1) == totLifeT)
                )
                if should_log_eval_window:
                    window_len = max(1, len(eval_window))
                    win_rate_w = sum(item["win"] for item in eval_window) / window_len
                    draw_rate_w = sum(item["draw"] for item in eval_window) / window_len
                    turn_limit_rate_w = sum(item["turn_limit"] for item in eval_window) / window_len
                    wipeout_enemy_rate_w = sum(item["wipeout_enemy"] for item in eval_window) / window_len
                    wipeout_model_rate_w = sum(item["wipeout_model"] for item in eval_window) / window_len
                    vp_diff_mean_w = sum(item["vp_diff"] for item in eval_window) / window_len
                    eval_line = (
                        "[TRAIN][EVAL_WINDOW] "
                        f"ep={numLifeT + 1} "
                        f"window={window_len} "
                        f"win_rate={win_rate_w:.3f} "
                        f"draw_rate={draw_rate_w:.3f} "
                        f"turn_limit_rate={turn_limit_rate_w:.3f} "
                        f"wipeout_enemy_rate={wipeout_enemy_rate_w:.3f} "
                        f"wipeout_model_rate={wipeout_model_rate_w:.3f} "
                        f"vp_diff_mean={vp_diff_mean_w:.3f} "
                        f"opp_eps={float(opponent_eps_state.get('value', SELF_PLAY_OPPONENT_EPSILON)):.3f} "
                        f"snapshot_update_every={int(current_selfplay_update_every)} "
                        f"pool_old_prob={float(pool_sampling_state.get('old_prob', SELF_PLAY_POOL_SAMPLE_OLD_PROB)):.3f} "
                        f"turn_limit_draw_penalty={float(getattr(reward_cfg, 'TURN_LIMIT_DRAW_PENALTY', 0.0)):.3f} "
                        f"opponent_source={opponent_source_state.get('source', 'unknown')} "
                        f"opponent_id={opponent_source_state.get('id')} "
                        f"opponent_score={opponent_source_state.get('score')}"
                    )
                    if TRAIN_LOG_TO_FILE:
                        append_agent_log(eval_line)
                    if TRAIN_LOG_TO_CONSOLE:
                        print(eval_line)

                    vp_diff_norm = math.tanh(vp_diff_mean_w / max(1.0, float(getattr(reward_cfg, "TURN_LIMIT_VP_MARGIN_CLAMP", 3.0))))
                    eval_score = (
                        BEST_EVAL_W_WIN * win_rate_w
                        - BEST_EVAL_W_DRAW * draw_rate_w
                        + BEST_EVAL_W_WIPE_ENEMY * wipeout_enemy_rate_w
                        - BEST_EVAL_W_WIPE_MODEL * wipeout_model_rate_w
                        + BEST_EVAL_W_VP * vp_diff_norm
                    )
                    if BEST_EVAL_ENABLED and eval_score > best_eval_score:
                        prev_best = best_eval_score
                        best_eval_score = float(eval_score)
                        best_eval_episode = int(numLifeT + 1)
                        best_path = f"models/{safe_name}/best_eval_checkpoint.pth"
                        os.makedirs(f"models/{safe_name}", exist_ok=True)
                        with IO_PROFILER.timed("checkpoint save"):
                            torch.save(
                                {
                                    "policy_net": policy_net.state_dict(),
                                    "target_net": target_net.state_dict(),
                                    "net_type": NET_TYPE,
                                    "optimizer": optimizer.state_dict(),
                                    "global_step": int(global_step),
                                    "optimize_steps": int(optimize_steps),
                                    "episode": int(resume_episode_base + numLifeT + 1),
                                    "replay_memory": memory.state_dict(),
                                    "best_eval_score": float(best_eval_score),
                                    "best_eval_episode": int(best_eval_episode),
                                    "eval_window_metrics": {
                                        "win_rate": float(win_rate_w),
                                        "draw_rate": float(draw_rate_w),
                                        "turn_limit_rate": float(turn_limit_rate_w),
                                        "wipeout_enemy_rate": float(wipeout_enemy_rate_w),
                                        "wipeout_model_rate": float(wipeout_model_rate_w),
                                        "vp_diff_mean": float(vp_diff_mean_w),
                                        "vp_diff_norm": float(vp_diff_norm),
                                        "eval_score": float(eval_score),
                                    },
                                },
                                best_path,
                            )
                        best_line = (
                            "[TRAIN][BEST] "
                            f"ep={numLifeT + 1} "
                            f"old_score={prev_best if prev_best != float('-inf') else 'none'} "
                            f"new_score={best_eval_score:.4f} "
                            f"win_rate={win_rate_w:.3f} draw_rate={draw_rate_w:.3f} "
                            f"wipe_enemy={wipeout_enemy_rate_w:.3f} wipe_model={wipeout_model_rate_w:.3f} "
                            f"vp_diff_mean={vp_diff_mean_w:.3f} "
                            f"path={best_path}"
                        )
                        if TRAIN_LOG_TO_FILE:
                            append_agent_log(best_line)
                        if TRAIN_LOG_TO_CONSOLE:
                            print(best_line)

                    if draw_rate_w >= DRAW_PIT_ALERT_RATE and win_rate_w <= DRAW_PIT_ALERT_WIN_MAX:
                        draw_pit_alert_streak += 1
                    else:
                        draw_pit_alert_streak = 0
                    if draw_pit_alert_streak >= DRAW_PIT_ALERT_STREAK:
                        alert_line = (
                            "[TRAIN][ALERT] draw_pit "
                            f"ep={numLifeT + 1} "
                            f"streak={draw_pit_alert_streak} "
                            f"draw_rate={draw_rate_w:.3f} "
                            f"win_rate={win_rate_w:.3f} "
                            f"thresholds(draw>={DRAW_PIT_ALERT_RATE:.2f}, win<={DRAW_PIT_ALERT_WIN_MAX:.2f})"
                        )
                        if TRAIN_LOG_TO_FILE:
                            append_agent_log(alert_line)
                        if TRAIN_LOG_TO_CONSOLE:
                            print(alert_line)
                        if DRAW_GUARD_ENABLED:
                            old_penalty = float(getattr(reward_cfg, "TURN_LIMIT_DRAW_PENALTY", 0.0))
                            new_penalty = min(DRAW_GUARD_PENALTY_MAX, old_penalty + DRAW_GUARD_PENALTY_STEP)
                            reward_cfg.TURN_LIMIT_DRAW_PENALTY = float(new_penalty)
                            draw_guard_state["turn_limit_draw_penalty"] = float(new_penalty)

                            old_prob = float(pool_sampling_state.get("old_prob", SELF_PLAY_POOL_SAMPLE_OLD_PROB))
                            new_prob = min(DRAW_GUARD_POOL_OLD_PROB_MAX, old_prob + DRAW_GUARD_POOL_OLD_PROB_STEP)
                            pool_sampling_state["old_prob"] = float(new_prob)

                            guard_line = (
                                "[TRAIN][GUARD] anti_draw_adjustment "
                                f"ep={numLifeT + 1} "
                                f"draw_penalty={old_penalty:.3f}->{new_penalty:.3f} "
                                f"pool_old_prob={old_prob:.3f}->{new_prob:.3f}"
                            )
                            if TRAIN_LOG_TO_FILE:
                                append_agent_log(guard_line)
                            if TRAIN_LOG_TO_CONSOLE:
                                print(guard_line)

                pool_opponent_id = opponent_source_state.get("id")
                if SELF_PLAY_POOL_ENABLED and pool_opponent_id is not None:
                    for entry in opponent_pool_entries:
                        if int(entry.get("id", -1)) == int(pool_opponent_id):
                            entry["games"] = int(entry.get("games", 0)) + 1
                            game_outcome_win = 1.0 if result == "win" else 0.0
                            game_outcome_draw = 1.0 if result == "draw" else 0.0
                            if result == "win":
                                entry["wins"] = int(entry.get("wins", 0)) + 1
                            if result == "draw":
                                entry["draws"] = int(entry.get("draws", 0)) + 1
                            entry["vp_diff_sum"] = float(entry.get("vp_diff_sum", 0.0)) + float(vp_diff)
                            alpha = float(SELF_PLAY_POOL_EMA_ALPHA)
                            entry["ema_win"] = (1.0 - alpha) * float(entry.get("ema_win", 0.5)) + alpha * game_outcome_win
                            entry["ema_draw"] = (1.0 - alpha) * float(entry.get("ema_draw", 0.5)) + alpha * game_outcome_draw
                            entry["ema_vp_diff"] = (1.0 - alpha) * float(entry.get("ema_vp_diff", 0.0)) + alpha * float(vp_diff)
                            break
    
                ep_rows.append(
                    {
                        "episode": numLifeT + 1,  # lifetimes считаются у тебя через numLifeT
                        "ep_reward": ep_reward,
                        "ep_len": ctx["ep_len"],
                        "turn": turn,
                        "model_vp": model_vp,
                        "player_vp": player_vp,
                        "vp_diff": vp_diff,
                        "result": result,
                        "end_reason": end_reason,
                        "end_code": end_code,
                    }
                )
                # ==========================================================
    
                if res == 4:
                    inText.append("Major Victory")
    
                if float(reward) > 0:
                    inText.append("model won!")
                    if trunc is False:
                        print("model won!")
                else:
                    inText.append("enemy won!")
                    if trunc is False:
                        print("enemy won!")
                if trunc is False:
                    print("Restarting...")
                numLifeT += 1
                total_episode = resume_episode_base + numLifeT
                _apply_reward_schedule(total_episode)
                if SAVE_EVERY > 0 and total_episode % SAVE_EVERY == 0:
                    checkpoint_path = f"models/{safe_name}/checkpoint_ep{total_episode}.pth"
                    os.makedirs(f"models/{safe_name}", exist_ok=True)
                    with IO_PROFILER.timed("checkpoint save"):
                        torch.save(
                            {
                                "policy_net": policy_net.state_dict(),
                                "target_net": target_net.state_dict(),
                                "net_type": NET_TYPE,
                                "optimizer": optimizer.state_dict(),
                                "global_step": int(global_step),
                                "optimize_steps": int(optimize_steps),
                                "episode": int(total_episode),
                                "replay_memory": memory.state_dict(),
                            },
                            checkpoint_path,
                        )
                    periodic_agent_id = build_agent_id(learner_identity, f"ep{total_episode}")
                    save_agent_artifact(
                        identity=learner_identity,
                        agent_id=periodic_agent_id,
                        env_contract=env_contract,
                        policy_state_dict=normalize_state_dict(policy_net.state_dict()),
                        target_state_dict=normalize_state_dict(target_net.state_dict()),
                        optimizer_state_dict=optimizer.state_dict(),
                        extra_meta={
                            "episode": int(total_episode),
                            "legacy_checkpoint_path": checkpoint_path,
                            "opponent_source": opponent_source_state.get("source"),
                            "opponent_id": opponent_source_state.get("id"),
                        },
                    )
                    if TRAIN_LOG_ENABLED:
                        save_line = f"[TRAIN][SAVE] ep={total_episode} path={checkpoint_path}"
                        if TRAIN_LOG_TO_FILE:
                            append_agent_log(save_line)
                        if TRAIN_LOG_TO_CONSOLE:
                            print(save_line)
    
                if SELF_PLAY_ENABLED:
                    # curriculum по epsilon оппонента: от max к min по эпизодам
                    decay_progress = min(1.0, float(total_episode) / float(SELF_PLAY_OPPONENT_EPSILON_DECAY_EPISODES))
                    next_opp_eps = SELF_PLAY_OPPONENT_EPSILON_MAX + (
                        SELF_PLAY_OPPONENT_EPSILON_MIN - SELF_PLAY_OPPONENT_EPSILON_MAX
                    ) * decay_progress
                    opponent_eps_state["value"] = float(
                        max(SELF_PLAY_OPPONENT_EPSILON_MIN, min(SELF_PLAY_OPPONENT_EPSILON_MAX, next_opp_eps))
                    )

                    if SELF_PLAY_ADAPTIVE_UPDATE and len(eval_window) >= EVAL_WINDOW_EPISODES:
                        window_len = max(1, len(eval_window))
                        draw_rate_w = sum(item["draw"] for item in eval_window) / window_len
                        prev_update = int(current_selfplay_update_every)
                        if draw_rate_w >= SELF_PLAY_DRAW_RATE_HIGH:
                            current_selfplay_update_every = min(
                                SELF_PLAY_UPDATE_EVERY_MAX, current_selfplay_update_every + 10
                            )
                        elif draw_rate_w <= SELF_PLAY_DRAW_RATE_LOW:
                            current_selfplay_update_every = max(
                                SELF_PLAY_UPDATE_EVERY_MIN, current_selfplay_update_every - 5
                            )
                        if current_selfplay_update_every != prev_update:
                            append_agent_log(
                                "[SELFPLAY] adaptive_update_every "
                                f"episode={total_episode} draw_rate={draw_rate_w:.3f} "
                                f"from={prev_update} to={current_selfplay_update_every}"
                            )

                if SELF_PLAY_ENABLED and SELF_PLAY_OPPONENT_MODE == "snapshot":
                    if total_episode % max(1, int(current_selfplay_update_every)) == 0:
                        latest_policy_state = normalize_state_dict(policy_net.state_dict())
                        if SELF_PLAY_POOL_ENABLED:
                            opponent_pool_entries.append(_create_pool_entry(latest_policy_state))
                        selected_state, selected_source, selected_id, selected_score = _choose_opponent_from_pool(latest_policy_state)
                        _load_opponent_state(selected_state, selected_source, source_id=selected_id, source_score=selected_score)
                        opponent_type, opponent_agent_id_text = _opponent_type_label(
                            opponent_policy_net=opponent_policy_net,
                            opponent_source_state=opponent_source_state,
                            self_play_enabled=True,
                        )
                        enemy_units_inline = _units_as_inline(roster_config.get("enemy_units", []) or [])
                        _log_train(
                            f"[TRAIN][OPPONENT] Snapshot обновлен: эпизод={total_episode} "
                            f"тип={opponent_type} agent_id={opponent_agent_id_text} "
                            f"Enemy units={enemy_units_inline} "
                            f"pool_source={selected_source} picked_id={selected_id} picked_score={selected_score} "
                            f"pool_size={len(opponent_pool_entries)}"
                        )
                _run_deterministic_eval(total_episode)
    
                if USE_SUBPROC_ENVS:
                    ctx["conn"].send(("reset", None))
                    ctx["state"], ctx["info"] = ctx["conn"].recv()
                else:
                    mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
                    attacker_side, defender_side = roll_off_attacker_defender(
                        manual_roll_allowed=False,
                        log_fn=print if idx == 0 else None,
                    )
                    if verbose and idx == 0:
                        print(f"[MISSION Only War] Attacker={attacker_side}, Defender={defender_side}")
    
                    deploy_for_mission(
                        mission_name,
                        model_units=ctx["model"],
                        enemy_units=ctx["enemy"],
                        b_len=b_len,
                        b_hei=b_hei,
                        attacker_side=attacker_side,
                        log_fn=log_fn if idx == 0 else None,
                    )
                    post_deploy_setup(log_fn=log_fn if idx == 0 else None)
                    ctx["env"].attacker_side = attacker_side
                    ctx["env"].defender_side = defender_side
    
                    ctx["state"], ctx["info"] = ctx["env"].reset(
                        options={"m": ctx["model"], "e": ctx["enemy"], "Type": "small", "trunc": True}
                    )
                ctx["ep_len"] = 0
                ctx["rew_arr"] = []
                ctx["action_head_total"] = Counter({"move": 0, "attack": 0, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0})
                ctx["action_head_skip"] = Counter({"move": 0, "attack": 0, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0})
                ctx["action_head_invalid"] = Counter({"move": 0, "attack": 0, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0})
                ctx["shoot_windows_with_targets"] = 0
                ctx["shoot_windows_without_targets"] = 0
                perf_stats["logging_s"] += time.perf_counter() - logging_start
    
            if numLifeT == totLifeT:
                end = True
                if pending_pbar_updates:
                    pbar.update(pending_pbar_updates)
                    pending_pbar_updates = 0
                pbar.close()
                break
    
        if end:
            break
    
        if global_step >= WARMUP_STEPS:
            for _ in range(UPDATES_PER_STEP):
                per_beta = PER_BETA_START
                if PER_ENABLED and PER_BETA_FRAMES > 0:
                    per_beta = min(
                        1.0,
                        PER_BETA_START
                        + (1.0 - PER_BETA_START)
                        * (optimize_steps / float(PER_BETA_FRAMES)),
                    )
                result = optimize_model(
                    policy_net,
                    target_net,
                    optimizer,
                    memory,
                    n_observations,
                    double_dqn_enabled=DOUBLE_DQN_ENABLED,
                    per_enabled=PER_ENABLED,
                    per_beta=per_beta,
                    per_eps=PER_EPS,
                    use_amp=USE_AMP,
                    scaler=scaler,
                    pin_memory=PIN_MEMORY,
                    prefetch=PREFETCH,
                )
    
                # optimize_model возвращает 0 если replay ещё маленький — такие пропускаем
                if result and result["loss"] != 0:
                    losses.append(result["loss"])
                    last_td_stats = result
                    last_per_beta = per_beta
                    last_loss_value = result["loss"]
                    optimize_steps += 1
                    perf_counts["updates"] += 1
                    timing = result.get("timing", {})
                    perf_stats["replay_sample_s"] += float(timing.get("sample_s", 0.0))
                    perf_stats["train_forward_s"] += float(timing.get("forward_s", 0.0))
                    perf_stats["train_backward_s"] += float(timing.get("backward_s", 0.0))
                    if TRAIN_LOG_ENABLED and optimize_steps % TRAIN_LOG_EVERY_UPDATES == 0:
                        train_line = (
                            "[TRAIN] "
                            f"ep={numLifeT + 1} "
                            f"upd={optimize_steps} "
                            f"step={global_step} "
                            f"loss={last_loss_value:.6f} "
                            f"eps={eps_threshold:.4f} "
                            f"lr={LR:.6g} "
                            f"gamma={GAMMA:.6g} "
                            f"PER={int(PER_ENABLED)} "
                            f"alpha={PER_ALPHA:.4g} "
                            f"beta={last_per_beta:.4g} "
                            f"N_STEP={N_STEP}"
                        )
                        if N_STEP > 1:
                            effective_gamma = GAMMA ** N_STEP
                            train_line += f" effective_gamma={effective_gamma:.6g}"
                        if PER_ENABLED and last_td_stats.get("per_stats"):
                            per_stats = last_td_stats["per_stats"]
                            train_line += (
                                f" td_abs_mean={per_stats['td_error_mean']:.6f}"
                                f" td_abs_max={per_stats['td_error_max']:.6f}"
                                f" prio_mean={per_stats['priority_mean']:.6f}"
                                f" prio_max={per_stats['priority_max']:.6f}"
                                f" isw_mean={per_stats['is_weight_mean']:.6f}"
                                f" isw_max={per_stats['is_weight_max']:.6f}"
                            )
                        if TRAIN_LOG_TO_FILE:
                            append_agent_log(train_line)
                        if TRAIN_LOG_TO_CONSOLE:
                            print(train_line)
    
                # ✅ Быстрый soft-update target_net (намного быстрее, чем state_dict)
                with torch.no_grad():
                    for p_tgt, p in zip(target_net.parameters(), policy_net.parameters()):
                        p_tgt.data.mul_(1.0 - TAU)
                        p_tgt.data.add_(p.data, alpha=TAU)
    
        # чтобы график loss не раздувался в 100 раз — пишем среднее за env-step
        if len(losses) > 0:
            metrics_obj.updateLoss(sum(losses) / len(losses))
        else:
            metrics_obj.updateLoss(0)
        if REWARD_DEBUG and last_td_stats and optimize_steps % REWARD_DEBUG_EVERY == 0:
            append_agent_log(
                "[TD] "
                f"step={global_step} "
                f"mean={last_td_stats['td_target_mean']:.6f} "
                f"max={last_td_stats['td_target_max']:.6f}"
            )
            if PER_ENABLED and last_td_stats.get("per_stats"):
                per_stats = last_td_stats["per_stats"]
                append_agent_log(
                    "[PER] "
                    f"opt_step={optimize_steps} "
                    f"priority_mean={per_stats['priority_mean']:.6f} "
                    f"priority_max={per_stats['priority_max']:.6f} "
                    f"is_weight_mean={per_stats['is_weight_mean']:.6f} "
                    f"td_error_mean={per_stats['td_error_mean']:.6f} "
                    f"td_error_max={per_stats['td_error_max']:.6f}"
                )
        # =========================
    
        if LOG_EVERY > 0 and global_step > 0 and global_step % LOG_EVERY == 0:
            steps = max(1, perf_counts["env_steps"])
            updates = max(1, perf_counts["updates"])
            perf_line = (
                "[PERF] "
                f"steps={perf_counts['env_steps']} "
                f"updates={perf_counts['updates']} "
                f"action_ms={1000.0 * perf_stats['action_select_s'] / steps:.3f} "
                f"enemy_turn_ms={1000.0 * perf_stats['enemy_turn_s'] / steps:.3f} "
                f"env_step_ms={1000.0 * perf_stats['env_step_s'] / steps:.3f} "
                f"replay_sample_ms={1000.0 * perf_stats['replay_sample_s'] / updates:.3f} "
                f"train_fwd_ms={1000.0 * perf_stats['train_forward_s'] / updates:.3f} "
                f"train_bwd_ms={1000.0 * perf_stats['train_backward_s'] / updates:.3f} "
                f"log_ms={1000.0 * perf_stats['logging_s'] / steps:.3f}"
            )
            if clip_reward_enabled:
                perf_line += f" reward_clip_events={perf_counts['reward_clipped']}"
            if TRAIN_LOG_TO_FILE:
                append_agent_log(perf_line)
            if TRAIN_LOG_TO_CONSOLE:
                print(perf_line)
            perf_stats = {k: 0.0 for k in perf_stats}
            perf_counts = {"env_steps": 0, "updates": 0, "reward_clipped": 0}
    
        global_step += vec_env_count
    
    with open('trainRes.txt', 'w') as f:
        for i in range(len(inText)):
            f.write(inText[i])
            f.write('\n')

    # Делать gif только если мы реально сохраняли кадры
    if RENDER_EVERY > 0 and not USE_SUBPROC_ENVS:
        if totLifeT > 30:
            genDisplay.makeGif(numOfLife=totLifeT, trunc=True)
        else:
            genDisplay.makeGif(numOfLife=totLifeT)
    else:
        print("[render] RENDER_EVERY=0 -> gif skipped")

    metrics_obj.lossCurve()
    metrics_obj.showRew()
    metrics_obj.showEpLen()

    save_extra_metrics(run_id=str(randNum), ep_rows=ep_rows, metrics_dir="metrics")
    heur_metrics_path = save_heuristic_metrics_snapshot(run_id=str(randNum), ep_rows=ep_rows, metrics_dir="metrics")
    if heur_metrics_path:
        _log_train(f"[HEUR][METRICS] saved={heur_metrics_path}")
    with IO_PROFILER.timed("metrics save"):
        metrics_obj.createJson()
    print("Generated metrics")

    os.makedirs(fold, exist_ok=True)

    with IO_PROFILER.timed("checkpoint save"):
        torch.save(
            {
                "policy_net": policy_net.state_dict(),
                "target_net": target_net.state_dict(),
                "net_type": NET_TYPE,
                "optimizer": optimizer.state_dict(),
                "global_step": int(global_step),
                "optimize_steps": int(optimize_steps),
                "episode": int(resume_episode_base + numLifeT),
                "replay_memory": memory.state_dict(),
            },
            ("models/{}/model-{}.pth".format(safe_name, date)),
        )
    final_agent_id = build_agent_id(learner_identity, f"final_ep{resume_episode_base + numLifeT}")
    artifact_dir = save_agent_artifact(
        identity=learner_identity,
        agent_id=final_agent_id,
        env_contract=env_contract,
        policy_state_dict=normalize_state_dict(policy_net.state_dict()),
        target_state_dict=normalize_state_dict(target_net.state_dict()),
        optimizer_state_dict=optimizer.state_dict(),
        extra_meta={
            "episode": int(resume_episode_base + numLifeT),
            "legacy_model_tag": f"{safe_name}/model-{date}",
            "opponent_policy": "roster_fixed",
            "opponent_source": opponent_source_state.get("source"),
            "opponent_id": opponent_source_state.get("id"),
            "learner_side": learner_identity.side,
            "learner_faction": learner_identity.faction,
        },
    )
    append_agent_log(f"[LEAGUE][SAVE] agent_id={final_agent_id} artifact_dir={artifact_dir}")
    train_elapsed_s = time.perf_counter() - train_start_time
    model_tag = f"{safe_name}/model-{date}"
    save_training_summary(
        run_id=str(randNum),
        model_tag=model_tag,
        ep_rows=ep_rows,
        elapsed_s=train_elapsed_s,
    )

    final_episode = int(resume_episode_base + numLifeT)
    mission_tag = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
    # Человекочитаемое имя для pickle (для удобства выбора в GUI).
    # legacy-путь сохраняем, чтобы не ломать старые сценарии/парсинг метрик.
    mission_tag_s = _sanitize_fs_name(mission_tag)
    human_pickle_path = os.path.join(
        fold,
        f"model-{date}_{learner_identity.side}_{learner_identity.faction}_{mission_tag_s}_final_ep{final_episode}.pickle",
    )

    if "env" in primary_ctx and "model" in primary_ctx and "enemy" in primary_ctx:
        toSave = [primary_ctx["env"], primary_ctx["model"], primary_ctx["enemy"]]
        with open(fileName, "wb") as file:
            pickle.dump(toSave, file)
        # Дублируем в человекочитаемый файл (single final save).
        try:
            with open(human_pickle_path, "wb") as file:
                pickle.dump(toSave, file)
        except Exception:
            # Не критично: legacy-модель уже сохранена.
            pass
    else:
        if USE_SUBPROC_ENVS:
            try:
                primary_ctx["conn"].send(("save_pickle", {"legacy": fileName, "human": human_pickle_path}))
                save_resp = primary_ctx["conn"].recv()
            except (BrokenPipeError, EOFError, OSError) as exc:
                err_line = (
                    "[SAVE][WARN] subprocess env недоступен: сохранение pickle пропущено. "
                    "Где: train.py main/save_pickle (send/recv). "
                    f"Ошибка: {exc}. "
                    "Что сделать: проверь, что subprocess не завершился до сохранения, "
                    "и смотри логи subprocess/Training."
                )
                append_agent_log(err_line)
                if TRAIN_LOG_TO_CONSOLE:
                    print(err_line)
            else:
                if isinstance(save_resp, dict) and save_resp.get("ok"):
                    ok_line = f"[SAVE] pickle сохранён в subprocess env: {save_resp.get('path')}"
                    append_agent_log(ok_line)
                    if TRAIN_LOG_TO_CONSOLE:
                        print(ok_line)
                else:
                    err_line = "[SAVE][WARN] не удалось сохранить pickle в subprocess env."
                    if isinstance(save_resp, dict) and save_resp.get("error"):
                        err_line += f" Ошибка: {save_resp['error']}"
                    append_agent_log(err_line)
                    if TRAIN_LOG_TO_CONSOLE:
                        print(err_line)
        else:
            skip_line = "[SAVE] subprocess env: нет локальных env/model/enemy, pickle пропущен."
            append_agent_log(skip_line)
            if TRAIN_LOG_TO_CONSOLE:
                print(skip_line)

    if USE_SUBPROC_ENVS:
        for ctx in env_contexts:
            try:
                ctx["conn"].send(("close", None))
                ctx["conn"].recv()
            except Exception:
                pass
        for proc in subproc_envs:
            proc.join(timeout=1.0)
    else:
        for ctx in env_contexts:
            ctx["env"].close()

    with IO_PROFILER.timed("metrics save"):
        IO_PROFILER.write_snapshot()

    _flush_agent_log_buffer(force=True)
    
    if os.path.isfile("gui/data.json"):
        initFile.delFile()

if __name__ == "__main__":
    mp.freeze_support()
    main()
