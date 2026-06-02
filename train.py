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
import queue as mp_queue
from tqdm import tqdm
from core.envs.warhamEnv import *
from core.engine import genDisplay, Unit, unitData, weaponData, initFile, metrics
from core.engine.io_profiler import get_io_profiler
from core.engine.game_io import ConsoleIO, set_active_io
from core.engine.mission import (
    normalize_mission_name,
    board_dims_for_mission,
    deploy_for_mission,
    post_deploy_setup,
)
from core.engine.agent_registry import (
    AgentIdentity,
    build_agent_id,
    compatible_contracts,
    load_agent_by_id,
    make_env_contract,
    list_agents,
    save_agent_artifact,
)
from core.engine.matchmaker import choose_opponent, record_matchup
from gymnasium import spaces
from project_paths import (
    AGENT_TRAIN_LOG_PATH,
    ARTIFACTS_METRICS_DIR,
    ARTIFACTS_MODELS_DIR,
    RESULTS_PATH,
    RUNTIME_STATE_DIR,
    TRAIN_DATA_PATH,
    ensure_runtime_dirs,
)

plt.rcParams.update(
    {
        "figure.facecolor": "#171d26",
        "axes.facecolor": "#1d2632",
        "axes.edgecolor": "#3a4658",
        "axes.labelcolor": "#d7dde7",
        "xtick.color": "#b8c2d1",
        "ytick.color": "#b8c2d1",
        "grid.color": "#3a4658",
        "text.color": "#d7dde7",
        "savefig.facecolor": "#171d26",
        "savefig.edgecolor": "#171d26",
    }
)

AGENT_TRAIN_LOG_FILE = str(AGENT_TRAIN_LOG_PATH.relative_to(AGENT_TRAIN_LOG_PATH.parent.parent))
os.environ.setdefault("AGENT_LOG_FILE", AGENT_TRAIN_LOG_FILE)

from core.models.DQN import *
from core.models.memory import *
from core.models.utils import *
from core.models.PPO import (
    ActorCriticMultiHead,
    make_actor_critic,
    ppo_kwargs_from_env,
    update_ppo_entropy_coef,
)
from core.models.ppo_buffer import PPORolloutBuffer
from core.models.opponent_adapter import OpponentSpec, build_policy_fn, load_agent_opponent
from core.models.alphazero_ids import (
    VALID_TRAIN_ALGOS,
    az_mcts_mode_for,
    az_section_for,
    is_az_algo,
)
from core.models.alphazero_model import (
    alphazero_arch_from_payload,
    alphazero_kwargs_from_env,
    load_alphazero_state_dict,
    make_alphazero_net,
)
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.alphazero_replay import AlphaZeroReplayBuffer, AZTransition
from core.models.alphazero_selfplay import play_episode_with_mcts, SelfPlayConfig
from core.models.az_rollout_receiver import RolloutReceiver
from core.models.az_rollout_sink import (
    az_dist_stop_flag_path,
    az_dist_stop_requested,
    make_rollout_sink,
    pack_az_dist_hyperparams,
    write_az_dist_train_context,
)
from core.models.alphazero_trainer import (
    AlphaZeroTrainConfig,
    alphazero_train_config_from_env,
    build_alphazero_lr_scheduler,
    train_alphazero_step,
)
from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.gumbel_muzero_search import GumbelMuZeroSearch, GumbelMuZeroSearchConfig
from core.models.gumbel_muzero_replay import GumbelMuZeroReplayBuffer, GMZTransition
from core.models.gumbel_muzero_selfplay import play_episode_with_gumbel_muzero, GumbelSelfPlayConfig
from core.models.gmz_inference_client import GMZInferenceClient
from core.models.gmz_inference_server import gmz_inference_server_entry
from core.models.gumbel_muzero_trainer import GumbelMuZeroTrainConfig, train_gumbel_muzero_step, make_gmz_lr_scheduler
from core.models.gumbel_muzero_reanalysis import GumbelMuZeroReanalyzer, GumbelMuZeroReanalysisConfig
from core.models.action_contract import ordered_action_keys, action_sizes_from_env
MODELS_DIR = str(ARTIFACTS_MODELS_DIR)
METRICS_DIR = str(ARTIFACTS_METRICS_DIR)
RUNTIME_IMG_DIR = os.path.join(str(RUNTIME_STATE_DIR), "img")

# Workaround: на некоторых окружениях torch._dynamo падает из-за несовместимого triton.
# Важно: используем setdefault, чтобы пользователь мог включить dynamo вручную.
os.environ.setdefault("TORCHDYNAMO_DISABLE", "1")

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

def _unwrap_wrapped_callable(fn):
    base = fn
    while hasattr(base, "__wrapped__"):
        base = base.__wrapped__
    return base

def _patch_optimizer_methods_no_compile(optimizer) -> None:
    """
    На некоторых сборках PyTorch оптимизаторные методы обёрнуты torch._compile wrapper,
    что тянет torch._dynamo и падает на несовместимом triton. Здесь просто снимаем обёртки.
    """
    try:
        base_zero_grad = _unwrap_wrapped_callable(optimizer.zero_grad)
        optimizer.zero_grad = base_zero_grad.__get__(optimizer, optimizer.__class__)
    except Exception:
        pass

    # optimizer.step в новых torch может идти через wrapper/_use_grad, который импортит torch._dynamo.
    # Снимаем обёртки и гарантируем no_grad вручную, чтобы:
    # - не трогать torch._dynamo (triton incompat)
    # - не ловить "leaf Variable ... in-place" (нужно no_grad)
    try:
        base_step = _unwrap_wrapped_callable(optimizer.step)
        bound_step = base_step.__get__(optimizer, optimizer.__class__)

        def _step_no_grad(*args, **kwargs):
            with torch.no_grad():
                return bound_step(*args, **kwargs)

        optimizer.step = _step_no_grad
    except Exception:
        pass


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

_DQN_CFG = data.get("dqn", {}) if isinstance(data, dict) and isinstance(data.get("dqn"), dict) else {}


def _cfg_raw(env_name: str, cfg_key: str, default):
    if os.getenv(env_name) is not None:
        return os.getenv(env_name)
    if cfg_key in _DQN_CFG:
        return _DQN_CFG[cfg_key]
    if isinstance(data, dict) and cfg_key in data:
        return data[cfg_key]
    return default


def _cfg_bool(env_name: str, cfg_key: str, default: str = "1") -> bool:
    return str(_cfg_raw(env_name, cfg_key, default)).strip().lower() in ("1", "true", "yes")


# ===== algo flags =====
DOUBLE_DQN_ENABLED = _cfg_bool("DOUBLE_DQN_ENABLED", "double_dqn", "1")
DUELING_ENABLED = _cfg_bool("DUELING_ENABLED", "dueling", "1")
DIST_TYPE = str(_cfg_raw("DIST_TYPE", "dist_type", "iqn")).strip().lower() or "iqn"
IQN_N_QUANTILES = int(_cfg_raw("IQN_N_QUANTILES", "iqn_n_quantiles", "32"))
IQN_N_TARGET_QUANTILES = int(_cfg_raw("IQN_N_TARGET_QUANTILES", "iqn_n_target_quantiles", "32"))
IQN_N_TAU_SAMPLES = int(_cfg_raw("IQN_N_TAU_SAMPLES", "iqn_n_tau_samples", "32"))
IQN_EMBED_DIM = int(_cfg_raw("IQN_EMBED_DIM", "iqn_embed_dim", "64"))
IQN_KAPPA = float(_cfg_raw("IQN_KAPPA", "iqn_kappa", "1.0"))
NOISY_SIGMA0 = float(_cfg_raw("NOISY_SIGMA0", "noisy_sigma0", "0.5"))
NOISY_DISABLE_EPS = _cfg_bool("NOISY_DISABLE_EPS", "noisy_disable_eps", "1")
NOISY_SIGMA_ANNEAL = _cfg_bool("NOISY_SIGMA_ANNEAL", "noisy_sigma_anneal", "0")
DQN_HIDDEN_SIZE = int(_cfg_raw("DQN_HIDDEN_SIZE", "hidden_size", "256"))
DQN_NUM_LAYERS = int(_cfg_raw("DQN_NUM_LAYERS", "num_layers", "2"))
DQN_ENSEMBLE_SIZE = int(_cfg_raw("DQN_ENSEMBLE_SIZE", "ensemble_size", "1"))
DQN_LR_SCHEDULER = str(_cfg_raw("DQN_LR_SCHEDULER", "lr_scheduler", "none")).strip().lower() or "none"
PER_ENSEMBLE_PRIORITY_LAMBDA = float(_cfg_raw("PER_ENSEMBLE_PRIORITY_LAMBDA", "per_ensemble_priority_lambda", "0.1"))
EPS_SCHEDULE = str(_cfg_raw("EPS_SCHEDULE", "eps_schedule", "exp")).strip().lower() or "exp"
if DQN_HIDDEN_SIZE < 32:
    DQN_HIDDEN_SIZE = 32
if DQN_NUM_LAYERS < 1:
    DQN_NUM_LAYERS = 1
if DQN_ENSEMBLE_SIZE < 1:
    DQN_ENSEMBLE_SIZE = 1
REWARD_DEBUG = os.getenv("REWARD_DEBUG", "0") == "1"
REWARD_DEBUG_EVERY = int(os.getenv("REWARD_DEBUG_EVERY", "200"))
TRAIN_ALGO = str(os.getenv("TRAIN_ALGO", "dqn")).strip().lower() or "dqn"
if TRAIN_ALGO not in VALID_TRAIN_ALGOS:
    TRAIN_ALGO = "dqn"
# ===== train logging =====
TRAIN_LOG_ENABLED = os.getenv("TRAIN_LOG_ENABLED", "1") == "1"
TRAIN_LOG_EVERY_UPDATES = int(os.getenv("TRAIN_LOG_EVERY_UPDATES", "200"))
TRAIN_LOG_TO_FILE = os.getenv("TRAIN_LOG_TO_FILE", "1") == "1"
TRAIN_LOG_TO_CONSOLE = str(os.getenv("TRAIN_LOG_TO_CONSOLE", "0")).strip() == "1"
TRAIN_DEBUG = os.getenv("TRAIN_DEBUG", "0") == "1"
ACTOR_PROGRESS_STDOUT_EVERY = max(1, int(os.getenv("ACTOR_PROGRESS_STDOUT_EVERY", "1")))
TRAIN_PROGRESS_HEARTBEAT_SEC = max(
    0.5, float(os.getenv("TRAIN_PROGRESS_HEARTBEAT_SEC", "2.0"))
)
ACTOR_PBAR_MININTERVAL = max(0.0, float(os.getenv("ACTOR_PBAR_MININTERVAL", "0.05" if os.name == "nt" else "0.05")))
ACTOR_PBAR_MINITERS = max(1, int(os.getenv("ACTOR_PBAR_MINITERS", "1")))
LOG_EVERY = int(os.getenv("LOG_EVERY", "200"))
ACTION_TRACE_ENABLED = os.getenv("ACTION_TRACE_ENABLED", "0") == "1"
ACTION_TRACE_FIRST_EP = max(0, int(os.getenv("ACTION_TRACE_FIRST_EP", "3") or "3"))
ACTION_TRACE_EVERY_EP = max(1, int(os.getenv("ACTION_TRACE_EVERY_EP", "1") or "1"))
ACTION_TRACE_MAX_LINES_PER_EP = max(20, int(os.getenv("ACTION_TRACE_MAX_LINES_PER_EP", "200") or "200"))
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
if DIST_TYPE != "iqn":
    raise ValueError(
        "[CONFIG][ERROR] Поддерживается только DIST_TYPE=iqn. "
        "Где: train.py (algo flags). Что делать: установите DIST_TYPE=iqn."
    )
if IQN_N_QUANTILES < 1 or IQN_N_TARGET_QUANTILES < 1 or IQN_N_TAU_SAMPLES < 1 or IQN_EMBED_DIM < 1 or IQN_KAPPA <= 0:
    raise ValueError(
        "[CONFIG][ERROR] Некорректные IQN параметры. "
        "Где: train.py (algo flags). Что делать: проверьте IQN_N_QUANTILES/IQN_N_TARGET_QUANTILES/IQN_N_TAU_SAMPLES/IQN_EMBED_DIM>=1 и IQN_KAPPA>0."
    )

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
SELF_PLAY_OPPONENT_MODE = str(os.getenv("SELF_PLAY_OPPONENT_MODE", "snapshot")).strip()
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

# Actor-Learner periodic DET-like eval (во время тренировки)
ACTOR_DET_EVAL_ENABLED = os.getenv("ACTOR_DET_EVAL_ENABLED", "1") == "1"
ACTOR_DET_EVAL_EVERY_EPISODES = int(os.getenv("ACTOR_DET_EVAL_EVERY_EPISODES", "300"))
ACTOR_DET_EVAL_EPISODES = int(os.getenv("ACTOR_DET_EVAL_EPISODES", "50"))
ACTOR_DET_EVAL_OPPONENT_EPSILON = float(os.getenv("ACTOR_DET_EVAL_OPPONENT_EPSILON", "0.0"))

REWARD_SCHEDULE_ENABLED = os.getenv("REWARD_SCHEDULE_ENABLED", "1") == "1"
REWARD_STAGE1_END_EP = int(os.getenv("REWARD_STAGE1_END_EP", "1500"))
REWARD_STAGE2_END_EP = int(os.getenv("REWARD_STAGE2_END_EP", "3500"))
REWARD_STAGE1_DRAW_PENALTY = float(os.getenv("REWARD_STAGE1_DRAW_PENALTY", str(getattr(reward_cfg, "TURN_LIMIT_DRAW_PENALTY", 0.35))))
REWARD_STAGE2_DRAW_PENALTY = float(os.getenv("REWARD_STAGE2_DRAW_PENALTY", str(max(getattr(reward_cfg, "TURN_LIMIT_DRAW_PENALTY", 0.35), 0.45))))
REWARD_STAGE3_DRAW_PENALTY = float(os.getenv("REWARD_STAGE3_DRAW_PENALTY", str(max(getattr(reward_cfg, "TURN_LIMIT_DRAW_PENALTY", 0.35), 0.60))))
REWARD_STAGE1_VP_REWARD_SCALE = float(os.getenv("REWARD_STAGE1_VP_REWARD_SCALE", str(getattr(reward_cfg, "TURN_LIMIT_VP_MARGIN_REWARD_SCALE", 0.12))))
REWARD_STAGE2_VP_REWARD_SCALE = float(os.getenv("REWARD_STAGE2_VP_REWARD_SCALE", str(max(getattr(reward_cfg, "TURN_LIMIT_VP_MARGIN_REWARD_SCALE", 0.12), 0.16))))
REWARD_STAGE3_VP_REWARD_SCALE = float(os.getenv("REWARD_STAGE3_VP_REWARD_SCALE", str(max(getattr(reward_cfg, "TURN_LIMIT_VP_MARGIN_REWARD_SCALE", 0.12), 0.20))))

# Runtime override: RCFG_<NAME>=<value> для быстрых A/B прогонов reward-конфига без правок файлов.
_REWARD_CFG_ENV_KEYS = (
    "VP_OBJECTIVE_STREAK_LEN",
    "VP_OBJECTIVE_STREAK_BONUS",
    "VP_OBJECTIVE_STREAK_LINEAR_CAP",
    "VP_OBJECTIVE_OC_MARGIN_SCALE",
    "MISSION_NO_CONTEST_PENALTY",
    "MISSION_NO_CONTEST_LATE_MULT",
    "NO_TARGET_NO_CONTEST_PENALTY",
    "NO_TARGET_NO_CONTEST_ROUND_SCALE",
    "VP_STALL_STEPS_THRESHOLD",
    "VP_STALL_PENALTY",
    "VP_STALL_STEP_GROWTH",
    "REWARD_PROGRESS_EARLY_MULT",
    "REWARD_PROGRESS_LATE_MULT",
    "REWARD_HOLD_EARLY_MULT",
    "REWARD_HOLD_LATE_MULT",
)
for _k in _REWARD_CFG_ENV_KEYS:
    _v = os.getenv(f"RCFG_{_k}")
    if _v is None:
        continue
    try:
        _curr = getattr(reward_cfg, _k)
        if isinstance(_curr, int):
            setattr(reward_cfg, _k, int(float(_v)))
        else:
            setattr(reward_cfg, _k, float(_v))
        print(f"[TRAIN][REWARD_CFG] override {_k}={getattr(reward_cfg, _k)}")
    except Exception:
        print(f"[TRAIN][REWARD_CFG][WARN] invalid override {_k}={_v}")

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
if ACTOR_DET_EVAL_EVERY_EPISODES < 1:
    ACTOR_DET_EVAL_EVERY_EPISODES = 1
if ACTOR_DET_EVAL_EPISODES < 1:
    ACTOR_DET_EVAL_EPISODES = 1
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


def _dqn_ctor_kwargs():
    return {
        "dueling": DUELING_ENABLED,
        "noisy": True,
        "noisy_sigma0": NOISY_SIGMA0,
        "distributional": DIST_TYPE,
        "hidden_size": DQN_HIDDEN_SIZE,
        "num_layers": DQN_NUM_LAYERS,
        "n_ensemble": DQN_ENSEMBLE_SIZE,
        "iqn_num_quantiles": IQN_N_QUANTILES,
        "iqn_num_target_quantiles": IQN_N_TARGET_QUANTILES,
        "iqn_num_tau_samples": IQN_N_TAU_SAMPLES,
        "iqn_embed_dim": IQN_EMBED_DIM,
    }


def _make_dqn(n_observations, n_actions):
    return DQN(n_observations, n_actions, **_dqn_ctor_kwargs())


def _build_dqn_lr_scheduler(optimizer, total_steps_hint=None):
    if DQN_LR_SCHEDULER == "cosine":
        t_max = max(1, int(total_steps_hint or int(os.getenv("TOT_LIFE_T", "1000")) * 500))
        return torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=t_max)
    if DQN_LR_SCHEDULER == "plateau":
        return torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode="min", factor=0.5, patience=50, min_lr=1e-6
        )
    return None


def _dqn_checkpoint_extra(policy_net, target_net, optimizer, lr_scheduler=None):
    extra = {
        "target_net": target_net.state_dict(),
        "target_model_state_dict": target_net.state_dict(),
    }
    if lr_scheduler is not None:
        extra["lr_scheduler"] = lr_scheduler.state_dict()
    return extra


def _run_dqn_distill_mode(n_observations, n_actions, steps: int = 100):
    """Отдельный режим TRAIN_ALGO=distill: KL-дистилляция teacher→student DQN."""
    from core.models.distill import distill_step

    teacher_ckpt = os.getenv("DISTILL_TEACHER_CKPT", "").strip()
    if not teacher_ckpt or not os.path.isfile(teacher_ckpt):
        raise ValueError(
            "[DISTILL][ERROR] Не задан DISTILL_TEACHER_CKPT. "
            "Где: train.py (_run_dqn_distill_mode). Что делать: укажите путь к чекпойнту teacher (AZ/PPO/DQN)."
        )
    student = _make_dqn(n_observations, n_actions).to(device)
    teacher = _make_dqn(n_observations, n_actions).to(device)
    ckpt = _load_checkpoint_payload(teacher_ckpt)
    teacher_state = _extract_policy_state_dict(ckpt)
    teacher.load_state_dict(normalize_state_dict(teacher_state))
    teacher.eval()
    if isinstance(ckpt, dict) and ckpt.get("policy_net"):
        try:
            student.load_state_dict(normalize_state_dict(ckpt["policy_net"]))
        except Exception:
            pass
    opt = optim.AdamW(student.parameters(), lr=float(os.getenv("DISTILL_LR", "1e-4")))
    batch = max(1, int(os.getenv("DISTILL_BATCH", "32")))
    for step_i in range(max(1, int(steps))):
        obs = torch.randn(batch, n_observations, device=device)
        out = distill_step(teacher, student, obs, alpha_kl=float(os.getenv("DISTILL_ALPHA_KL", "1.0")))
        opt.zero_grad()
        out["loss"].backward()
        opt.step()
        if step_i % 20 == 0:
            line = f"[DISTILL] step={step_i} kl={out['stats']['kl_loss']:.6f}"
            print(line)
            append_agent_log(line)
    save_path = os.getenv("DISTILL_OUT_CKPT", os.path.join(MODELS_DIR, "distill_student.pth"))
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    torch.save({"policy_net": student.state_dict(), "algo": "dqn"}, save_path)
    print(f"[DISTILL] saved student={save_path}")
    append_agent_log(f"[DISTILL] saved student={save_path}")


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

    try:
        policy_net.load_state_dict(normalize_state_dict(policy_state))
    except Exception as exc:
        err_msg = (
            "[RESUME][ERROR] Чекпойнт несовместим с текущей архитектурой Rainbow (Noisy+C51). "
            "Где: train.py (_resume_from_checkpoint/policy_net.load_state_dict). "
            "Что делать: используйте новый checkpoint из этой версии или запустите обучение с нуля. "
            f"Детали: {exc}"
        )
        print(err_msg)
        append_agent_log(err_msg)
        raise RuntimeError(err_msg) from exc
    policy_loaded = 1

    target_loaded = 0
    target_state = None
    if isinstance(checkpoint, dict):
        target_state = checkpoint.get("target_net") or checkpoint.get("target_model_state_dict")
    if isinstance(target_state, dict):
        try:
            target_net.load_state_dict(normalize_state_dict(target_state))
        except Exception as exc:
            err_msg = (
                "[RESUME][ERROR] target_net в чекпойнте несовместим с текущей архитектурой Rainbow (Noisy+C51). "
                "Где: train.py (_resume_from_checkpoint/target_net.load_state_dict). "
                "Что делать: используйте совместимый checkpoint. "
                f"Детали: {exc}"
            )
            print(err_msg)
            append_agent_log(err_msg)
            raise RuntimeError(err_msg) from exc
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

    scheduler_loaded = 0
    scheduler_state = checkpoint.get("lr_scheduler") if isinstance(checkpoint, dict) else None

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
        "lr_scheduler_state": scheduler_state,
        "scheduler_loaded": scheduler_loaded,
    }

def save_extra_metrics(
    run_id: str,
    ep_rows: list[dict],
    metrics_dir=METRICS_DIR,
    *,
    write_legacy_gui_plots: bool = True,
):
    os.makedirs(metrics_dir, exist_ok=True)
    os.makedirs(RUNTIME_IMG_DIR, exist_ok=True)

    # --- CSV ---
    csv_path = os.path.join(metrics_dir, f"stats_{run_id}.csv")
    cols = ["episode", "ep_reward", "ep_len", "turn", "model_vp", "player_vp", "vp_diff", "result", "end_reason", "end_code"]
    with IO_PROFILER.timed("metrics save"):
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in ep_rows:
                w.writerow({k: r.get(k, "") for k in cols})

    if not write_legacy_gui_plots:
        print(f"[metrics] saved (csv only): {csv_path}")
        return

    wins01 = [1 if r["result"] == "win" else 0 for r in ep_rows]
    vp_diff = [r["vp_diff"] for r in ep_rows]
    ep_idx = list(range(1, len(ep_rows) + 1))

    # --- Winrate plot (raw + moving avg + trend) ---
    plt.figure()
    if len(ep_idx) > 0:
        # Сырые 0/1 точки слишком плотные (плохо читаются на 300+ эпизодов),
        # поэтому рисуем их как полупрозрачный scatter + скользящую среднюю.
        plt.scatter(ep_idx, wins01, color="#1f77b4", s=8, alpha=0.18, label="raw (0/1)")
        win_window = int(max(10, min(100, len(wins01) // 20 or 10)))
        wins_ma = moving_avg(wins01, window=win_window)
        plt.plot(ep_idx, wins_ma, color="#1f77b4", linewidth=2.0, label=f"MA {win_window}")

        if len(ep_idx) >= 2:
            x = np.asarray(ep_idx, dtype=np.float64)
            y = np.asarray(wins_ma, dtype=np.float64)
            try:
                a, b = np.polyfit(x, y, 1)
                y_fit = a * x + b
                plt.plot(ep_idx, y_fit.tolist(), color="#ff7f0e", linewidth=2.0, label="trend")
            except Exception:
                pass
    plt.xlabel("Episodes")
    plt.ylabel("Winrate")
    plt.title("Winrate (raw + MA + trend)")
    plt.ylim(-0.05, 1.05)
    plt.legend(loc="lower right")

    plt.savefig(os.path.join(metrics_dir, f"winrate_{run_id}.png"))
    plt.savefig(os.path.join(RUNTIME_IMG_DIR, f"winrate_{run_id}.png"))
    plt.savefig(os.path.join(RUNTIME_IMG_DIR, "winrate.png"))
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
    plt.savefig(os.path.join(RUNTIME_IMG_DIR, f"vpdiff_{run_id}.png"))
    plt.savefig(os.path.join(RUNTIME_IMG_DIR, "vpdiff.png"))
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
    plt.savefig(os.path.join(RUNTIME_IMG_DIR, f"endreasons_{run_id}.png"))
    plt.savefig(os.path.join(RUNTIME_IMG_DIR, "endreasons.png"))
    plt.close()

    print(f"[metrics] saved: {csv_path}")


def _append_jsonl(path: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    line = json.dumps(payload, ensure_ascii=False)
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def append_episode_diagnostics(
    *,
    run_id: str,
    episode_row: dict,
    diagnostics: dict,
    metrics_dir: str = METRICS_DIR,
) -> None:
    """
    Пишем "супер-подробные" данные по эпизодам в JSONL, чтобы потом можно было
    строить разбор draw-матчей без ручного ковыряния логов.
    - artifacts/metrics/episodes_<run_id>.jsonl
    - artifacts/metrics/episodes_latest.jsonl
    """
    os.makedirs(metrics_dir, exist_ok=True)
    payload = {
        "run_id": str(run_id),
        "ts": time.time(),
        **(episode_row or {}),
        **(diagnostics or {}),
    }
    _append_jsonl(os.path.join(metrics_dir, f"episodes_{run_id}.jsonl"), payload)
    _append_jsonl(os.path.join(metrics_dir, "episodes_latest.jsonl"), payload)


def _save_actor_det_eval_snapshot(run_id: str, payload: dict, metrics_dir: str = METRICS_DIR) -> None:
    os.makedirs(metrics_dir, exist_ok=True)
    out = {"run_id": str(run_id), "updated_at": datetime.datetime.now().isoformat(timespec="seconds"), **(payload or {})}
    _append_jsonl(os.path.join(metrics_dir, f"actor_det_eval_{run_id}.jsonl"), out)
    with open(os.path.join(metrics_dir, "actor_det_eval_latest.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)


def _write_det_eval_data_json(
    *,
    run_id: str,
    det_plot_gui_paths: dict[str, str],
    model_path: str,
    metrics_mode: str = "det_eval",
    extra: dict | None = None,
) -> str:
    """
    GUI читает artifacts/models/data_<run_id>.json: только det_* пути.
    """
    data_json_path = os.path.join(MODELS_DIR, f"data_{run_id}.json")
    os.makedirs(MODELS_DIR, exist_ok=True)
    payload = {
        "run_id": str(run_id),
        "metrics_mode": metrics_mode,
        "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "model_path": model_path,
        **{k: v for k, v in (det_plot_gui_paths or {}).items()},
    }
    if extra:
        payload.update(extra)
    with open(data_json_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    # Alias для GUI "latest metrics" без зависимости от mtime старых data_*.json.
    latest_json_path = os.path.join(MODELS_DIR, "data_latest.json")
    try:
        with open(latest_json_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
    except OSError:
        pass
    return data_json_path


def _det_eval_read_jsonl_points(run_id: str, metrics_dir: str = METRICS_DIR) -> list[dict]:
    jsonl_path = os.path.join(metrics_dir, f"actor_det_eval_{run_id}.jsonl")
    if not os.path.exists(jsonl_path):
        return []
    by_ep: dict[int, dict] = {}
    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(payload, dict):
                    continue
                ep = int(payload.get("episode", 0) or 0)
                if ep <= 0:
                    continue
                by_ep[ep] = payload
    except OSError:
        return []
    return [by_ep[k] for k in sorted(by_ep.keys())]


def save_actor_det_eval_plot(run_id: str, metrics_dir: str = METRICS_DIR) -> dict | None:
    """
    Графики только из actor_det_eval_<run_id>.jsonl (DET-eval чекпоинты).
    PNG: winrate, reward, loss (на момент обучения), ep_len, hp_diff, kill_diff, причины завершения.
    Возвращает словарь относительных путей для gui (ключи det_winrate, …) или None.
    """
    points = _det_eval_read_jsonl_points(run_id, metrics_dir=metrics_dir)
    if not points:
        return None

    episodes = [int(p.get("episode", 0) or 0) for p in points]
    win_rates = [float(p.get("win_rate", 0.0) or 0.0) for p in points]
    reward_mean = [float(p.get("reward_mean", 0.0) or 0.0) for p in points]
    model_vp_m = [float(p.get("model_vp_mean", 0.0) or 0.0) for p in points]
    enemy_vp_m = [float(p.get("enemy_vp_mean", 0.0) or 0.0) for p in points]
    hp_diff_m = [float(p.get("hp_diff_mean", 0.0) or 0.0) for p in points]
    kill_diff_m = [float(p.get("kill_diff_mean", 0.0) or 0.0) for p in points]
    ep_len_m = [float(p.get("ep_len_mean", 0.0) or 0.0) for p in points]
    wo_e = [float(p.get("wipeout_enemy_rate", 0.0) or 0.0) for p in points]
    wo_m = [float(p.get("wipeout_model_rate", 0.0) or 0.0) for p in points]
    tl_r = [float(p.get("turn_limit_rate", 0.0) or 0.0) for p in points]

    loss_ep: list[int] = []
    loss_vals: list[float] = []
    for p in points:
        raw = p.get("training_loss", None)
        if raw is None:
            continue
        try:
            v = float(raw)
        except (TypeError, ValueError):
            continue
        loss_ep.append(int(p.get("episode", 0) or 0))
        loss_vals.append(v)

    os.makedirs(metrics_dir, exist_ok=True)
    os.makedirs(RUNTIME_IMG_DIR, exist_ok=True)

    def _save_fig(path_metrics: str, path_gui_run: str, path_gui_latest: str) -> None:
        plt.savefig(path_metrics)
        plt.savefig(path_gui_run)
        plt.savefig(path_gui_latest)

    def _trend_line(ax, xs: list, ys: list) -> None:
        if len(xs) >= 2:
            x = np.asarray(xs, dtype=np.float64)
            y = np.asarray(ys, dtype=np.float64)
            try:
                a, b = np.polyfit(x, y, 1)
                ax.plot(xs, (a * x + b).tolist(), color="#ff7f0e", linewidth=2.0, label="trend")
            except Exception:
                pass

    # --- winrate ---
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(episodes, win_rates, color="#1f77b4", linewidth=1.6, marker="o", markersize=3, label="win_rate")
    _trend_line(ax, episodes, win_rates)
    ax.set_ylim(-0.05, 1.05)
    ax.set_ylabel("Win rate")
    ax.set_title("DET-eval: win rate (по чекпоинтам)")
    ax.set_xlabel("Эпизод обучения (якорь)")
    ax.legend(loc="lower right")
    plt.tight_layout()
    _save_fig(
        os.path.join(metrics_dir, f"det_winrate_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, f"det_winrate_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, "det_winrate.png"),
    )
    plt.close()

    # --- reward ---
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(episodes, reward_mean, color="#1f77b4", linewidth=1.6, marker="o", markersize=3, label="reward_mean")
    _trend_line(ax, episodes, reward_mean)
    ax.set_ylabel("Суммарная награда за eval-игру / N")
    ax.set_title("DET-eval: средняя награда")
    ax.set_xlabel("Эпизод обучения (якорь)")
    ax.legend()
    plt.tight_layout()
    _save_fig(
        os.path.join(metrics_dir, f"det_reward_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, f"det_reward_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, "det_reward.png"),
    )
    plt.close()

    # --- avg VP (model/enemy) ---
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(episodes, model_vp_m, color="#1f77b4", linewidth=1.6, marker="o", markersize=3, label="model_vp_mean")
    ax.plot(episodes, enemy_vp_m, color="#d62728", linewidth=1.6, marker="o", markersize=3, label="enemy_vp_mean")
    ax.set_ylabel("VP")
    ax.set_title("DET-eval: Avg VP (model vs enemy)")
    ax.set_xlabel("Эпизод обучения (якорь)")
    ax.legend(loc="best")
    plt.tight_layout()
    _save_fig(
        os.path.join(metrics_dir, f"det_avg_vp_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, f"det_avg_vp_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, "det_avg_vp.png"),
    )
    plt.close()

    # --- loss (training checkpoint) ---
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    if loss_ep:
        ax.plot(loss_ep, loss_vals, color="#2ca02c", linewidth=1.6, marker="o", markersize=3, label="training_loss")
        if len(loss_ep) >= 2:
            _trend_line(ax, loss_ep, loss_vals)
    else:
        ax.text(0.5, 0.5, "Нет training_loss в JSONL", ha="center", va="center", transform=ax.transAxes)
    ax.set_ylabel("Loss")
    ax.set_title("Loss на момент чекпоинта обучения (не loss игры)")
    ax.set_xlabel("Эпизод обучения (якорь)")
    ax.legend()
    plt.tight_layout()
    _save_fig(
        os.path.join(metrics_dir, f"det_loss_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, f"det_loss_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, "det_loss.png"),
    )
    plt.close()

    # --- ep_len ---
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(episodes, ep_len_m, color="#9467bd", linewidth=1.6, marker="o", markersize=3, label="ep_len_mean")
    _trend_line(ax, episodes, ep_len_m)
    ax.set_ylabel("Средняя длина eval-эпизода (шаги)")
    ax.set_title("DET-eval: длина эпизода")
    ax.set_xlabel("Эпизод обучения (якорь)")
    ax.legend()
    plt.tight_layout()
    _save_fig(
        os.path.join(metrics_dir, f"det_ep_len_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, f"det_ep_len_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, "det_ep_len.png"),
    )
    plt.close()

    # --- hp_diff ---
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(episodes, hp_diff_m, color="#d62728", linewidth=1.6, marker="o", markersize=3, label="hp_diff_mean")
    _trend_line(ax, episodes, hp_diff_m)
    ax.set_ylabel("HP diff (model − enemy)")
    ax.set_title("DET-eval: HP diff (конец игры)")
    ax.set_xlabel("Эпизод обучения (якорь)")
    ax.legend()
    plt.tight_layout()
    _save_fig(
        os.path.join(metrics_dir, f"det_hp_diff_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, f"det_hp_diff_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, "det_hp_diff.png"),
    )
    plt.close()

    # --- kill_diff ---
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(episodes, kill_diff_m, color="#8c564b", linewidth=1.6, marker="o", markersize=3, label="kill_diff_mean")
    _trend_line(ax, episodes, kill_diff_m)
    ax.set_ylabel("Kill diff (model − enemy)")
    ax.set_title("DET-eval: Kill diff (по моделям)")
    ax.set_xlabel("Эпизод обучения (якорь)")
    ax.legend()
    plt.tight_layout()
    _save_fig(
        os.path.join(metrics_dir, f"det_kill_diff_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, f"det_kill_diff_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, "det_kill_diff.png"),
    )
    plt.close()

    # --- end reasons (доли) ---
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(episodes, wo_e, color="#1f77b4", linewidth=1.4, marker="o", markersize=3, label="wipeout_enemy")
    ax.plot(episodes, wo_m, color="#ff7f0e", linewidth=1.4, marker="o", markersize=3, label="wipeout_model")
    ax.plot(episodes, tl_r, color="#2ca02c", linewidth=1.4, marker="o", markersize=3, label="turn_limit")
    ax.set_ylim(-0.05, 1.05)
    ax.set_ylabel("Доля игр")
    ax.set_title("DET-eval: причины завершения (доли)")
    ax.set_xlabel("Эпизод обучения (якорь)")
    ax.legend(loc="best")
    plt.tight_layout()
    _save_fig(
        os.path.join(metrics_dir, f"det_endreasons_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, f"det_endreasons_{run_id}.png"),
        os.path.join(RUNTIME_IMG_DIR, "det_endreasons.png"),
    )
    plt.close()

    return {
        "det_winrate": f"img/det_winrate_{run_id}.png",
        "det_reward": f"img/det_reward_{run_id}.png",
        "det_avg_vp": f"img/det_avg_vp_{run_id}.png",
        "det_loss": f"img/det_loss_{run_id}.png",
        "det_ep_len": f"img/det_ep_len_{run_id}.png",
        "det_hp_diff": f"img/det_hp_diff_{run_id}.png",
        "det_kill_diff": f"img/det_kill_diff_{run_id}.png",
        "det_endreasons": f"img/det_endreasons_{run_id}.png",
    }


def _run_actor_det_eval(
    *,
    policy_net,
    roster_config: dict,
    b_len: int,
    b_hei: int,
    n_eval: int,
    opponent_epsilon: float,
    self_play_enabled: bool = False,
    opponent_spec: OpponentSpec | None = None,
) -> dict:
    policy_net.eval()
    wins = 0
    draws = 0
    vp_diff_sum = 0.0
    model_vp_sum = 0.0
    enemy_vp_sum = 0.0
    hp_diff_sum = 0.0
    kill_diff_sum = 0.0
    wipeout_enemy = 0
    wipeout_model = 0
    turn_limit = 0
    reward_sum_total = 0.0
    steps_sum_total = 0.0

    def _sum_health(value) -> float:
        try:
            if isinstance(value, (list, tuple, np.ndarray)):
                return float(sum(float(x) for x in value))
            return float(value or 0.0)
        except Exception:
            return 0.0

    def _sum_alive_models(value) -> int:
        try:
            if isinstance(value, (list, tuple, np.ndarray)):
                return int(sum(int(x) for x in value))
            return int(value or 0)
        except Exception:
            return 0

    mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
    for eval_idx in range(max(1, int(n_eval))):
        enemy_e, model_e = _build_units_from_config(roster_config, b_len, b_hei)
        attacker_side, defender_side = roll_off_attacker_defender(manual_roll_allowed=False, log_fn=None)
        deploy_for_mission(
            mission_name,
            model_units=model_e,
            enemy_units=enemy_e,
            b_len=b_len,
            b_hei=b_hei,
            attacker_side=attacker_side,
            log_fn=None,
        )
        post_deploy_setup(log_fn=None)
        env_e = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy_e, model=model_e, b_len=b_len, b_hei=b_hei)
        env_e.attacker_side = attacker_side
        env_e.defender_side = defender_side
        state_e, info_e = env_e.reset(options={"m": model_e, "e": enemy_e, "trunc": True})
        opponent_policy_fn = None
        if bool(self_play_enabled) and opponent_spec is not None:
            try:
                opponent_policy_fn = build_policy_fn(
                    env=env_e,
                    len_model=len(model_e),
                    opponent=opponent_spec,
                    deterministic=True,
                )
            except Exception:
                opponent_policy_fn = None
        # Стартовые totals для kill diff
        model_alive_start = _sum_alive_models((info_e or {}).get("model alive models", []))
        enemy_alive_start = _sum_alive_models((info_e or {}).get("player alive models", []))
        done_e = False
        step_count = 0
        while not done_e:
            step_count += 1
            shoot_mask_e = build_shoot_action_mask(env_e, log_fn=None, debug=False)
            action_e = select_action_with_epsilon(env_e, state_e, policy_net, 0.0, len(model_e), shoot_mask=shoot_mask_e)
            action_e_dict = convertToDict(action_e)
            env_unwrapped_e = unwrap_env(env_e)
            if opponent_policy_fn is not None:
                env_unwrapped_e.enemyTurn(trunc=True, policy_fn=opponent_policy_fn)
            else:
                env_unwrapped_e.enemyTurn(trunc=True)
            next_state_e, _reward_e, done_e, _res_e, info_e = env_e.step(action_e_dict)
            reward_sum_total += float(_reward_e or 0.0)
            state_e = next_state_e
        steps_sum_total += float(step_count)
        end_reason_e = info_e.get("end reason", "")
        model_vp_e = int(info_e.get("model VP", 0))
        enemy_vp_e = int(info_e.get("player VP", 0))
        vp_diff_e = model_vp_e - enemy_vp_e
        vp_diff_sum += float(vp_diff_e)
        model_vp_sum += float(model_vp_e)
        enemy_vp_sum += float(enemy_vp_e)

        # HP diff / Kill diff на конец игры
        model_hp_end = _sum_health((info_e or {}).get("model health", []))
        enemy_hp_end = _sum_health((info_e or {}).get("player health", []))
        hp_diff_sum += float(model_hp_end - enemy_hp_end)
        model_alive_end = _sum_alive_models((info_e or {}).get("model alive models", []))
        enemy_alive_end = _sum_alive_models((info_e or {}).get("player alive models", []))
        kills_by_model = enemy_alive_start - enemy_alive_end
        kills_by_enemy = model_alive_start - model_alive_end
        kill_diff_sum += float(kills_by_model - kills_by_enemy)

        try:
            append_agent_log(
                "[DET][DEBUG] "
                f"kind=dqn_det_eval "
                f"idx={eval_idx+1}/{n_eval} "
                f"end_reason={end_reason_e} "
                f"model_vp={model_vp_e} "
                f"player_vp={enemy_vp_e} "
                f"vp_diff={vp_diff_e}"
            )
        except Exception:
            pass

        if end_reason_e == "wipeout_enemy":
            wins += 1
            wipeout_enemy += 1
        elif end_reason_e == "wipeout_model":
            wipeout_model += 1
        elif str(end_reason_e).startswith("turn_limit"):
            turn_limit += 1
            if vp_diff_e > 0:
                wins += 1
            elif vp_diff_e == 0:
                draws += 1
        else:
            if vp_diff_e > 0:
                wins += 1
            elif vp_diff_e == 0:
                draws += 1
        try:
            env_e.close()
        except Exception:
            pass

    n = max(1, int(n_eval))
    return {
        "eval_episodes": int(n),
        "win_rate": float(wins / n),
        "draw_rate": float(draws / n),
        "turn_limit_rate": float(turn_limit / n),
        "wipeout_enemy_rate": float(wipeout_enemy / n),
        "wipeout_model_rate": float(wipeout_model / n),
        "vp_diff_mean": float(vp_diff_sum / n),
        "model_vp_mean": float(model_vp_sum / n),
        "enemy_vp_mean": float(enemy_vp_sum / n),
        "hp_diff_mean": float(hp_diff_sum / n),
        "kill_diff_mean": float(kill_diff_sum / n),
        "reward_mean": float(reward_sum_total / n),
        "ep_len_mean": float(steps_sum_total / n),
        "opponent_epsilon": float(opponent_epsilon),
    }


def _gmz_episode_result_row(*, info: dict, ep_reward: float, ep_len: int) -> dict:
    info = dict(info or {})
    end_reason = str(info.get("end reason", "") or "")
    model_vp = int(info.get("model VP", 0) or 0)
    player_vp = int(info.get("player VP", 0) or 0)
    vp_diff = int(model_vp) - int(player_vp)
    result = "loss"
    if end_reason == "wipeout_enemy":
        result = "win"
    elif end_reason == "wipeout_model":
        result = "loss"
    elif str(end_reason).startswith("turn_limit"):
        if vp_diff > 0:
            result = "win"
        elif vp_diff == 0:
            result = "draw"
    elif vp_diff > 0:
        result = "win"
    elif vp_diff == 0:
        result = "draw"
    return {
        "ep_reward": float(ep_reward),
        "ep_len": int(ep_len),
        "turn": int(ep_len),
        "model_vp": int(model_vp),
        "player_vp": int(player_vp),
        "vp_diff": int(vp_diff),
        "result": str(result),
        "end_reason": str(end_reason),
        "end_code": int(info.get("res", 0) or 0),
    }


def _gmz_det_payload_from_rows(
    rows_slice: list[dict],
    *,
    episode_idx: int,
    train_loss: float,
    eval_tag: str = "actor_learner_search_eval",
) -> dict:
    rows = rows_slice if rows_slice else []
    n_eval = max(1, len(rows))
    wins = sum(1 for r in rows if str(r.get("result", "")).strip().lower() == "win")
    draws = sum(1 for r in rows if str(r.get("result", "")).strip().lower() == "draw")
    turn_limit = sum(1 for r in rows if str(r.get("end_reason", "")).startswith("turn_limit"))
    wipe_enemy = sum(1 for r in rows if str(r.get("end_reason", "")) == "wipeout_enemy")
    wipe_model = sum(1 for r in rows if str(r.get("end_reason", "")) == "wipeout_model")
    vp_diff_mean = float(sum(float(r.get("vp_diff", 0) or 0) for r in rows) / n_eval)
    model_vp_mean = float(sum(float(r.get("model_vp", 0) or 0) for r in rows) / n_eval)
    enemy_vp_mean = float(sum(float(r.get("player_vp", 0) or 0) for r in rows) / n_eval)
    ep_len_mean = float(sum(float(r.get("ep_len", 0) or 0) for r in rows) / n_eval)
    reward_mean = float(sum(float(r.get("ep_reward", 0.0) or 0.0) for r in rows) / n_eval)
    return {
        "eval_episodes": int(n_eval),
        "win_rate": float(wins / n_eval),
        "draw_rate": float(draws / n_eval),
        "turn_limit_rate": float(turn_limit / n_eval),
        "wipeout_enemy_rate": float(wipe_enemy / n_eval),
        "wipeout_model_rate": float(wipe_model / n_eval),
        "vp_diff_mean": vp_diff_mean,
        "model_vp_mean": model_vp_mean,
        "enemy_vp_mean": enemy_vp_mean,
        "hp_diff_mean": 0.0,
        "kill_diff_mean": 0.0,
        "reward_mean": reward_mean,
        "ep_len_mean": ep_len_mean,
        "opponent_epsilon": 0.0,
        "episode": int(max(episode_idx, 1)),
        "algo": "gumbel_muzero",
        "eval_tag": str(eval_tag),
        "training_loss": float(train_loss),
    }


def _run_gmz_honest_eval(
    *,
    gmz_net,
    device: torch.device,
    roster_config: dict,
    b_len: int,
    b_hei: int,
    n_eval: int,
    sims: int,
    root_top_k: int,
    eval_temperature: float,
    gumbel_scale: float,
    prior_weight: float,
    discount: float,
    batch_recurrent: bool,
    tree_reuse: bool,
    self_play_enabled: bool,
    opponent_spec: OpponentSpec | None,
    sp_cfg: GumbelSelfPlayConfig | None = None,
) -> list[dict]:
    """Play n_eval games with local search (deterministic=True). Returns per-episode rows."""
    was_training = bool(getattr(gmz_net, "training", False))
    gmz_net.eval()
    eval_rows: list[dict] = []
    mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
    cfg_sp = sp_cfg or GumbelSelfPlayConfig()
    try:
        with torch.no_grad():
            for _ in range(max(1, int(n_eval))):
                enemy_e, model_e = _build_units_from_config(roster_config, b_len, b_hei)
                attacker_side, defender_side = roll_off_attacker_defender(manual_roll_allowed=False, log_fn=None)
                deploy_for_mission(
                    mission_name,
                    model_units=model_e,
                    enemy_units=enemy_e,
                    b_len=b_len,
                    b_hei=b_hei,
                    attacker_side=attacker_side,
                    log_fn=None,
                )
                post_deploy_setup(log_fn=None)
                env_e = gym.make(
                    "40kAI-v0",
                    disable_env_checker=True,
                    enemy=enemy_e,
                    model=model_e,
                    b_len=b_len,
                    b_hei=b_hei,
                )
                env_e.attacker_side = attacker_side
                env_e.defender_side = defender_side
                opponent_policy_fn = None
                if bool(self_play_enabled) and opponent_spec is not None:
                    try:
                        opponent_policy_fn = build_policy_fn(
                            env=env_e,
                            len_model=len(model_e),
                            opponent=opponent_spec,
                            deterministic=True,
                        )
                    except Exception:
                        opponent_policy_fn = None
                search = GumbelMuZeroSearch(
                    gmz_net,
                    config=GumbelMuZeroSearchConfig(
                        num_simulations=int(sims),
                        root_top_k=int(root_top_k),
                        discount=float(discount),
                        temperature=float(eval_temperature),
                        gumbel_scale=float(gumbel_scale),
                        prior_weight=float(prior_weight),
                        batch_recurrent=bool(batch_recurrent),
                        tree_reuse=bool(tree_reuse),
                    ),
                    device=device,
                )
                _transitions, info = play_episode_with_gumbel_muzero(
                    env=env_e,
                    search=search,
                    len_model=int(len(model_e)),
                    config=cfg_sp,
                    enemy_policy_fn=opponent_policy_fn,
                    deterministic=True,
                )
                info = dict(info or {})
                ep_len = int(info.get("turn", 0) or 0)
                ep_reward = float(info.get("reward", 0.0) or 0.0)
                eval_rows.append(
                    _gmz_episode_result_row(info=info, ep_reward=ep_reward, ep_len=ep_len)
                )
                try:
                    env_e.close()
                except Exception:
                    pass
    finally:
        if was_training:
            gmz_net.train()
    return eval_rows


def _gmz_build_actor_det_payload(
    *,
    gmz_net,
    device: torch.device,
    roster_config: dict,
    b_len: int,
    b_hei: int,
    episodes_finished: int,
    last_loss: float,
    self_play_enabled: bool,
    opponent_spec: OpponentSpec | None,
    sp_cfg: GumbelSelfPlayConfig | None = None,
) -> dict:
    append_agent_log(
        f"[GMZ][HONEST_EVAL] start ep={int(episodes_finished)} n={int(GMZ_HONEST_EVAL_EPISODES)} "
        f"sims={int(GMZ_HONEST_EVAL_SIMS)} temp={float(GMZ_HONEST_EVAL_TEMPERATURE):.2f}"
    )
    eval_rows = _run_gmz_honest_eval(
        gmz_net=gmz_net,
        device=device,
        roster_config=roster_config,
        b_len=b_len,
        b_hei=b_hei,
        n_eval=int(GMZ_HONEST_EVAL_EPISODES),
        sims=int(GMZ_HONEST_EVAL_SIMS),
        root_top_k=int(GMZ_HONEST_EVAL_TOP_K),
        eval_temperature=float(GMZ_HONEST_EVAL_TEMPERATURE),
        gumbel_scale=float(GMZ_GUMBEL_SCALE),
        prior_weight=float(GMZ_PRIOR_WEIGHT),
        discount=float(GMZ_DISCOUNT),
        batch_recurrent=bool(GMZ_BATCH_RECURRENT),
        tree_reuse=bool(GMZ_TREE_REUSE),
        self_play_enabled=bool(self_play_enabled),
        opponent_spec=opponent_spec,
        sp_cfg=sp_cfg,
    )
    payload = _gmz_det_payload_from_rows(
        eval_rows,
        episode_idx=int(episodes_finished),
        train_loss=float(last_loss),
        eval_tag="actor_learner_search_eval",
    )
    append_agent_log(
        f"[GMZ][HONEST_EVAL] done ep={int(episodes_finished)} "
        f"win_rate={float(payload.get('win_rate', 0.0)):.3f} "
        f"n={int(payload.get('eval_episodes', 0))}"
    )
    return payload


def _az_det_payload_from_rows(
    rows_slice: list[dict],
    *,
    episode_idx: int,
    train_loss: float,
    train_algo: str,
    mcts_mode: str,
    eval_tag: str = "actor_learner_search_eval",
) -> dict:
    rows = rows_slice if rows_slice else []
    n_eval = max(1, len(rows))
    wins = sum(1 for r in rows if str(r.get("result", "")).strip().lower() == "win")
    draws = sum(1 for r in rows if str(r.get("result", "")).strip().lower() == "draw")
    turn_limit = sum(1 for r in rows if str(r.get("end_reason", "")).startswith("turn_limit"))
    wipe_enemy = sum(1 for r in rows if str(r.get("end_reason", "")) == "wipeout_enemy")
    wipe_model = sum(1 for r in rows if str(r.get("end_reason", "")) == "wipeout_model")
    vp_diff_mean = float(sum(float(r.get("vp_diff", 0) or 0) for r in rows) / n_eval)
    model_vp_mean = float(sum(float(r.get("model_vp", 0) or 0) for r in rows) / n_eval)
    enemy_vp_mean = float(sum(float(r.get("player_vp", 0) or 0) for r in rows) / n_eval)
    ep_len_mean = float(sum(float(r.get("ep_len", 0) or 0) for r in rows) / n_eval)
    reward_mean = float(sum(float(r.get("ep_reward", 0.0) or 0.0) for r in rows) / n_eval)
    return {
        "eval_episodes": int(n_eval),
        "win_rate": float(wins / n_eval),
        "draw_rate": float(draws / n_eval),
        "turn_limit_rate": float(turn_limit / n_eval),
        "wipeout_enemy_rate": float(wipe_enemy / n_eval),
        "wipeout_model_rate": float(wipe_model / n_eval),
        "vp_diff_mean": vp_diff_mean,
        "model_vp_mean": model_vp_mean,
        "enemy_vp_mean": enemy_vp_mean,
        "hp_diff_mean": 0.0,
        "kill_diff_mean": 0.0,
        "reward_mean": reward_mean,
        "ep_len_mean": ep_len_mean,
        "opponent_epsilon": 0.0,
        "episode": int(max(episode_idx, 1)),
        "algo": str(train_algo),
        "mcts_mode": str(mcts_mode),
        "eval_tag": str(eval_tag),
        "training_loss": float(train_loss),
    }


def _run_az_honest_eval(
    *,
    az_net,
    device: torch.device,
    roster_config: dict,
    b_len: int,
    b_hei: int,
    n_eval: int,
    mcts_mode: str,
    self_play_enabled: bool,
    opponent_spec: OpponentSpec | None,
    outcome_only: bool = True,
    outcome_value_win: float = 1.0,
    outcome_value_loss: float = -1.0,
    outcome_value_draw: float = -0.25,
) -> list[dict]:
    was_training = bool(getattr(az_net, "training", False))
    az_net.eval()
    eval_rows: list[dict] = []
    mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
    try:
        with torch.no_grad():
            for _ in range(max(1, int(n_eval))):
                enemy_e, model_e = _build_units_from_config(roster_config, b_len, b_hei)
                attacker_side, defender_side = roll_off_attacker_defender(manual_roll_allowed=False, log_fn=None)
                deploy_for_mission(
                    mission_name,
                    model_units=model_e,
                    enemy_units=enemy_e,
                    b_len=b_len,
                    b_hei=b_hei,
                    attacker_side=attacker_side,
                    log_fn=None,
                )
                post_deploy_setup(log_fn=None)
                env_e = gym.make(
                    "40kAI-v0",
                    disable_env_checker=True,
                    enemy=enemy_e,
                    model=model_e,
                    b_len=b_len,
                    b_hei=b_hei,
                )
                env_e.attacker_side = attacker_side
                env_e.defender_side = defender_side
                opponent_policy_fn = None
                if bool(self_play_enabled) and opponent_spec is not None:
                    try:
                        opponent_policy_fn = build_policy_fn(
                            env=env_e,
                            len_model=len(model_e),
                            opponent=opponent_spec,
                            deterministic=True,
                        )
                    except Exception:
                        opponent_policy_fn = None
                mcts = AlphaZeroFactorizedMCTS(
                    az_net,
                    config=_az_honest_eval_mcts_config(mcts_mode=str(mcts_mode)),
                    device=device,
                )
                _transitions, info = play_episode_with_mcts(
                    env=env_e,
                    mcts=mcts,
                    len_model=int(len(model_e)),
                    enemy_policy_fn=opponent_policy_fn,
                    outcome_only=bool(outcome_only),
                    outcome_value_win=float(outcome_value_win),
                    outcome_value_loss=float(outcome_value_loss),
                    outcome_value_draw=float(outcome_value_draw),
                    fixed_temperature=float(AZ_HONEST_EVAL_TEMPERATURE),
                    policy_argmax=True,
                    heartbeat_moves=0,
                )
                info = dict(info or {})
                ep_len = int(info.get("turn", 0) or 0)
                ep_reward = float(info.get("reward", 0.0) or 0.0)
                eval_rows.append(
                    _gmz_episode_result_row(info=info, ep_reward=ep_reward, ep_len=ep_len)
                )
                try:
                    env_e.close()
                except Exception:
                    pass
    finally:
        if was_training:
            az_net.train()
    return eval_rows


def _az_build_actor_det_payload(
    *,
    az_net,
    device: torch.device,
    roster_config: dict,
    b_len: int,
    b_hei: int,
    episodes_finished: int,
    last_loss: float,
    train_algo: str,
    mcts_mode: str,
    self_play_enabled: bool,
    opponent_spec: OpponentSpec | None,
) -> dict:
    append_agent_log(
        f"[AZ][HONEST_EVAL] start ep={int(episodes_finished)} n={int(AZ_HONEST_EVAL_EPISODES)} "
        f"mode={str(mcts_mode)} sims={int(AZ_HONEST_EVAL_SIMS)} temp={float(AZ_HONEST_EVAL_TEMPERATURE):.3f}"
    )
    eval_rows = _run_az_honest_eval(
        az_net=az_net,
        device=device,
        roster_config=roster_config,
        b_len=b_len,
        b_hei=b_hei,
        n_eval=int(AZ_HONEST_EVAL_EPISODES),
        mcts_mode=str(mcts_mode),
        self_play_enabled=bool(self_play_enabled),
        opponent_spec=opponent_spec,
        outcome_only=bool(AZ_OUTCOME_ONLY),
        outcome_value_win=float(AZ_OUTCOME_VALUE_WIN),
        outcome_value_loss=float(AZ_OUTCOME_VALUE_LOSS),
        outcome_value_draw=float(AZ_OUTCOME_VALUE_DRAW),
    )
    payload = _az_det_payload_from_rows(
        eval_rows,
        episode_idx=int(episodes_finished),
        train_loss=float(last_loss),
        train_algo=str(train_algo),
        mcts_mode=str(mcts_mode),
        eval_tag="actor_learner_search_eval",
    )
    append_agent_log(
        f"[AZ][HONEST_EVAL] done ep={int(episodes_finished)} "
        f"win_rate={float(payload.get('win_rate', 0.0)):.3f} "
        f"n={int(payload.get('eval_episodes', 0))}"
    )
    return payload


def _run_actor_det_eval_ppo(
    *,
    actor_critic,
    roster_config: dict,
    b_len: int,
    b_hei: int,
    n_actions: list[int],
    n_eval: int,
    opponent_epsilon: float,
    self_play_enabled: bool = False,
    opponent_spec: OpponentSpec | None = None,
) -> dict:
    """
    DET-eval для PPO: детерминированная политика (argmax) против enemyTurn(policy_fn) при self-play.
    Возвращаем те же агрегаты, что и для DQN DET-eval.
    """
    actor_critic.eval()
    wins = 0
    draws = 0
    vp_diff_sum = 0.0
    model_vp_sum = 0.0
    enemy_vp_sum = 0.0
    hp_diff_sum = 0.0
    kill_diff_sum = 0.0
    wipeout_enemy = 0
    wipeout_model = 0
    turn_limit = 0
    reward_sum_total = 0.0
    steps_sum_total = 0.0

    def _sum_health(value) -> float:
        try:
            if isinstance(value, (list, tuple, np.ndarray)):
                return float(sum(float(x) for x in value))
            return float(value or 0.0)
        except Exception:
            return 0.0

    def _sum_alive_models(value) -> int:
        try:
            if isinstance(value, (list, tuple, np.ndarray)):
                return int(sum(int(x) for x in value))
            return int(value or 0)
        except Exception:
            return 0

    mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
    for eval_idx in range(max(1, int(n_eval))):
        enemy_e, model_e = _build_units_from_config(roster_config, b_len, b_hei)
        attacker_side, defender_side = roll_off_attacker_defender(manual_roll_allowed=False, log_fn=None)
        deploy_for_mission(
            mission_name,
            model_units=model_e,
            enemy_units=enemy_e,
            b_len=b_len,
            b_hei=b_hei,
            attacker_side=attacker_side,
            log_fn=None,
        )
        post_deploy_setup(log_fn=None)
        env_e = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy_e, model=model_e, b_len=b_len, b_hei=b_hei)
        env_e.attacker_side = attacker_side
        env_e.defender_side = defender_side
        obs_e, info_e = env_e.reset(options={"m": model_e, "e": enemy_e, "trunc": True})
        opponent_policy_fn = None
        if bool(self_play_enabled) and opponent_spec is not None:
            try:
                opponent_policy_fn = build_policy_fn(
                    env=env_e,
                    len_model=len(model_e),
                    opponent=opponent_spec,
                    deterministic=True,
                )
            except Exception:
                opponent_policy_fn = None
        model_alive_start = _sum_alive_models((info_e or {}).get("model alive models", []))
        enemy_alive_start = _sum_alive_models((info_e or {}).get("player alive models", []))
        done_e = False
        step_count = 0
        while not done_e:
            step_count += 1
            # маски: strict для shoot, остальные all_true
            shoot_mask_e = build_shoot_action_mask(env_e, log_fn=None, debug=False)
            masks_cpu = []
            for head_idx, head_size in enumerate(n_actions):
                if head_idx == 2 and shoot_mask_e is not None:
                    mask_arr = np.asarray(shoot_mask_e, dtype=np.bool_).reshape(-1)
                    if mask_arr.size == int(head_size) and bool(mask_arr.any()):
                        masks_cpu.append(mask_arr)
                        continue
                masks_cpu.append(np.ones(int(head_size), dtype=np.bool_))
            masks_batch = [torch.tensor(m, dtype=torch.bool, device=next(actor_critic.parameters()).device).unsqueeze(0) for m in masks_cpu]

            obs_np = to_np_state(obs_e)
            obs_t = torch.tensor(obs_np, dtype=torch.float32, device=next(actor_critic.parameters()).device).unsqueeze(0)
            with torch.no_grad():
                action_t, _logp_t, _value_t = actor_critic.act(obs_t, masks_by_head=masks_batch, deterministic=True)
            action_np = action_t.squeeze(0).detach().cpu().numpy()
            action_dict = convertToDict(torch.tensor([action_np], device="cpu"))
            for i_u in range(len(model_e)):
                action_dict[f"move_num_{i_u}"] = int(action_np[6 + i_u])

            env_unwrapped_e = unwrap_env(env_e)
            if opponent_policy_fn is not None:
                env_unwrapped_e.enemyTurn(trunc=True, policy_fn=opponent_policy_fn)
            else:
                env_unwrapped_e.enemyTurn(trunc=True)
            next_obs_e, reward_e, done_e, _res_e, info_e = env_e.step(action_dict)
            reward_sum_total += float(reward_e or 0.0)
            obs_e = next_obs_e

        steps_sum_total += float(step_count)
        end_reason_e = (info_e or {}).get("end reason", "")
        model_vp_e = int((info_e or {}).get("model VP", 0))
        enemy_vp_e = int((info_e or {}).get("player VP", 0))
        vp_diff_e = model_vp_e - enemy_vp_e
        vp_diff_sum += float(vp_diff_e)
        model_vp_sum += float(model_vp_e)
        enemy_vp_sum += float(enemy_vp_e)

        model_hp_end = _sum_health((info_e or {}).get("model health", []))
        enemy_hp_end = _sum_health((info_e or {}).get("player health", []))
        hp_diff_sum += float(model_hp_end - enemy_hp_end)
        model_alive_end = _sum_alive_models((info_e or {}).get("model alive models", []))
        enemy_alive_end = _sum_alive_models((info_e or {}).get("player alive models", []))
        kills_by_model = enemy_alive_start - enemy_alive_end
        kills_by_enemy = model_alive_start - model_alive_end
        kill_diff_sum += float(kills_by_model - kills_by_enemy)

        try:
            append_agent_log(
                "[DET][DEBUG] "
                f"kind=ppo_det_eval "
                f"idx={eval_idx+1}/{n_eval} "
                f"end_reason={end_reason_e} "
                f"model_vp={model_vp_e} "
                f"player_vp={enemy_vp_e} "
                f"vp_diff={vp_diff_e}"
            )
        except Exception:
            pass

        if end_reason_e == "wipeout_enemy":
            wins += 1
            wipeout_enemy += 1
        elif end_reason_e == "wipeout_model":
            wipeout_model += 1
        elif str(end_reason_e).startswith("turn_limit"):
            turn_limit += 1
            if vp_diff_e > 0:
                wins += 1
            elif vp_diff_e == 0:
                draws += 1
        else:
            if vp_diff_e > 0:
                wins += 1
            elif vp_diff_e == 0:
                draws += 1
        try:
            env_e.close()
        except Exception:
            pass

    n = max(1, int(n_eval))
    return {
        "eval_episodes": int(n),
        "win_rate": float(wins / n),
        "draw_rate": float(draws / n),
        "turn_limit_rate": float(turn_limit / n),
        "wipeout_enemy_rate": float(wipeout_enemy / n),
        "wipeout_model_rate": float(wipeout_model / n),
        "vp_diff_mean": float(vp_diff_sum / n),
        "model_vp_mean": float(model_vp_sum / n),
        "enemy_vp_mean": float(enemy_vp_sum / n),
        "hp_diff_mean": float(hp_diff_sum / n),
        "kill_diff_mean": float(kill_diff_sum / n),
        "reward_mean": float(reward_sum_total / n),
        "ep_len_mean": float(steps_sum_total / n),
        "opponent_epsilon": float(opponent_epsilon),
    }


def _safe_div(n: float, d: float) -> float:
    return float(n) / float(d) if float(d) > 0 else 0.0


def save_heuristic_metrics_snapshot(run_id: str, ep_rows: list[dict] | None = None, metrics_dir: str = METRICS_DIR) -> str | None:
    """
    Агрегирует ключевые метрики эвристики из train-логов и сохраняет JSON:
    - artifacts/metrics/heur_metrics_<run_id>.json
    - artifacts/metrics/heur_metrics_latest.json
    """
    ensure_runtime_dirs()
    log_path = str(AGENT_TRAIN_LOG_PATH)
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
        def _safe_float(token: str) -> float | None:
            if token is None:
                return None
            s = str(token).strip()
            # Иногда парсер цепляет кусок timestamp/мусор (например "0.8162026-03-25").
            m = re.match(r"^[+-]?\d+(?:\.\d+)?", s)
            if not m:
                return None
            try:
                return float(m.group(0))
            except ValueError:
                return None

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
                        v = _safe_float(risk_match.group(1))
                        if v is not None:
                            risk_vals.append(v)
                    cover_match = re.search(r"cover=([-\d\.]+)", line)
                    if cover_match:
                        v = _safe_float(cover_match.group(1))
                        if v is not None:
                            cover_vals.append(v)
                if "[ENEMY][HEUR][CHARGE]" in line:
                    charge_attempts += 1
                if "Reward (чардж): success_bonus" in line:
                    charge_success += 1
                if "fallback_target=" in line:
                    fallback_count += 1
                if "[ENEMY][HEUR][SHOOT]" in line:
                    ovk_match = re.findall(r"ovk=([-\d\.]+)", line)
                    for token in ovk_match:
                        v = _safe_float(token)
                        if v is not None:
                            shoot_overkill_vals.append(v)
                if "[TRAIN][ACTIONS]" in line:
                    invalid_block = re.search(r"invalid_rate=\{([^}]*)\}", line)
                    if invalid_block:
                        vals = re.findall(r":([0-9\.]+)", invalid_block.group(1))
                        if vals:
                            try:
                                parsed = [x for x in (_safe_float(v) for v in vals) if x is not None]
                                if not parsed:
                                    continue
                                avg_inv = sum(parsed) / len(parsed)
                                invalid_vals.append(avg_inv)
                            except ValueError:
                                pass
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

def save_training_summary(run_id: str, model_tag: str, ep_rows: list[dict], elapsed_s: float, results_path: str = str(RESULTS_PATH)) -> None:
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


def _trace_ep_enabled(ep_idx_1based: int) -> bool:
    if not ACTION_TRACE_ENABLED:
        return False
    if ep_idx_1based <= 0:
        return False
    if ep_idx_1based <= ACTION_TRACE_FIRST_EP:
        return True
    return (ep_idx_1based % ACTION_TRACE_EVERY_EP) == 0


def _trace_write_lines(ep_idx_1based: int, lines: list[str], *, actor_idx: int | None = None, run_id: str | int | None = None) -> None:
    if not _trace_ep_enabled(ep_idx_1based):
        return
    if not lines:
        return
    n = min(len(lines), ACTION_TRACE_MAX_LINES_PER_EP)
    actor_part = f" actor={int(actor_idx)}" if actor_idx is not None else ""
    run_part = f" run_id={run_id}" if run_id is not None else ""
    append_agent_log(f"[TRACE][EP]{run_part} ep={ep_idx_1based}{actor_part} lines={n}/{len(lines)}")
    for i in range(n):
        prefix = ""
        if actor_idx is not None:
            prefix += f"actor={int(actor_idx)} "
        if run_id is not None:
            prefix += f"run_id={run_id} "
        append_agent_log(f"[TRACE] {prefix}{lines[i]}")


def _format_action_trace_summary(ep_idx_1based: int, actor_idx: int | None, payload: dict) -> str:
    """
    Компактный, но подробный блок для runtime/logs/LOGS_FOR_AGENTS_TRAIN.md.
    payload ожидает структуру вида:
      {
        "steps": int,
        "skip": {head:int},
        "invalid": {head:int},
        "skip_rate": {head:float},
        "invalid_rate": {head:float},
        "shoot_windows": {"with_targets":int,"without_targets":int},
        "move": {"stay":int,"nonstay":int}
      }
    """
    try:
        steps = max(1, int(payload.get("steps", 0) or 0))
    except Exception:
        steps = 1
    skip = payload.get("skip") or {}
    invalid = payload.get("invalid") or {}
    skip_rate = payload.get("skip_rate") or {}
    invalid_rate = payload.get("invalid_rate") or {}
    shoot_windows = payload.get("shoot_windows") or {}
    shoot_taken_when_targets = payload.get("shoot_taken_when_targets", None)
    move = payload.get("move") or {}

    def _g_int(d, k):
        try:
            return int(d.get(k, 0) or 0)
        except Exception:
            return 0

    def _g_f(d, k):
        try:
            return float(d.get(k, 0.0) or 0.0)
        except Exception:
            return 0.0

    heads = ("move", "attack", "shoot", "charge", "use_cp", "cp_on")
    head_skip = ",".join([f"{h}:{_g_int(skip,h)}" for h in heads])
    head_invalid = ",".join([f"{h}:{_g_int(invalid,h)}" for h in heads])
    head_skip_rate = ",".join([f"{h}:{_g_f(skip_rate,h):.3f}" for h in heads])
    head_invalid_rate = ",".join([f"{h}:{_g_f(invalid_rate,h):.3f}" for h in heads])

    with_t = _g_int(shoot_windows, "with_targets")
    without_t = _g_int(shoot_windows, "without_targets")
    try:
        taken_t = int(shoot_taken_when_targets) if shoot_taken_when_targets is not None else None
    except Exception:
        taken_t = None
    taken_rate = None
    if taken_t is not None:
        taken_rate = float(taken_t) / float(max(1, with_t))
    stay = _g_int(move, "stay")
    nonstay = _g_int(move, "nonstay")
    stay_rate = float(stay) / float(max(1, (stay + nonstay)))

    actor_part = f" actor={int(actor_idx)}" if actor_idx is not None else ""
    shoot_taken_part = ""
    if taken_t is not None and taken_rate is not None:
        shoot_taken_part = f" shoot_taken_when_targets={taken_t}/{with_t} ({taken_rate:.3f})"

    return (
        "[TRACE][ACTIONS] "
        f"ep={int(ep_idx_1based)}{actor_part} "
        f"steps={steps} "
        f"move_stay={stay}/{stay+nonstay} ({stay_rate:.3f}) "
        f"skip={{{{ {head_skip} }}}} "
        f"invalid={{{{ {head_invalid} }}}} "
        f"skip_rate={{{{ {head_skip_rate} }}}} "
        f"invalid_rate={{{{ {head_invalid_rate} }}}} "
        f"shoot_windows={{with_targets:{with_t},without_targets:{without_t}}}"
        f"{shoot_taken_part}"
    )


def _log_train(line: str) -> None:
    """Лог в `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md` + (опционально) в консоль."""
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

    ensure_runtime_dirs()
    log_path = str(AGENT_TRAIN_LOG_PATH)
    try:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.writelines(lines)
    except Exception as exc:
        print(f"[LOG][WARN] Не удалось записать runtime/logs/LOGS_FOR_AGENTS_TRAIN.md: {exc}")


atexit.register(lambda: _flush_agent_log_buffer(force=True))

def _env_worker(conn, roster_config, b_len, b_hei, trunc):
    try:
        lean_info_enabled = os.getenv("TRAIN_LEAN_INFO", "1") == "1"
        include_masks = os.getenv("TRAIN_IPC_INCLUDE_MASKS", "1") == "1"

        def _to_np_state(state):
            if isinstance(state, (dict, collections.OrderedDict)):
                return np.array(list(state.values()), dtype=np.float32)
            return np.array(state, dtype=np.float32)

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
                "battle round": info.get("battle round", 0),
                "model controlled objectives": info.get("model controlled objectives", []),
                "player controlled objectives": info.get("player controlled objectives", []),
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
        state = _to_np_state(state)
        shoot_mask = build_shoot_action_mask(env, log_fn=None, debug=False) if include_masks else None
        conn.send(
            {
                "state": state,
                "info": info,
                "len_model": len(model),
                "shoot_mask": shoot_mask,
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
                next_observation = _to_np_state(next_observation)
                if lean_info_enabled:
                    info = _lean_train_info(info)
                next_mask = None
                if include_masks and not done:
                    next_mask = build_shoot_action_mask(env, log_fn=None, debug=False)
                conn.send((next_observation, reward, done, res, info, next_mask))
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
                state = _to_np_state(state)
                mask = build_shoot_action_mask(env, log_fn=None, debug=False) if include_masks else None
                conn.send((state, info, mask))
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

    if os.path.isfile(str(TRAIN_DATA_PATH)):
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
PPO_CFG = data.get("ppo", {}) if isinstance(data, dict) else {}
PPO_LR = float(PPO_CFG.get("learning_rate", LR))
PPO_GAMMA = float(PPO_CFG.get("gamma", GAMMA))
PPO_GAE_LAMBDA = float(PPO_CFG.get("gae_lambda", 0.95))
PPO_CLIP_RATIO = float(PPO_CFG.get("clip_ratio", 0.2))
PPO_VALUE_COEF = float(PPO_CFG.get("value_coef", 0.5))
PPO_ENTROPY_COEF = float(PPO_CFG.get("entropy_coef", 0.01))
PPO_ROLLOUT_STEPS = int(PPO_CFG.get("rollout_steps", 1024))
PPO_UPDATE_EPOCHS = int(PPO_CFG.get("update_epochs", 4))
PPO_MINIBATCH_SIZE = int(PPO_CFG.get("minibatch_size", 256))
PPO_MAX_GRAD_NORM = float(PPO_CFG.get("max_grad_norm", 0.5))
PPO_TARGET_KL = float(PPO_CFG.get("target_kl", 0.03))
def _ppo_cfg_raw(env_name: str, cfg_key: str, default):
    if os.getenv(env_name) is not None:
        return os.getenv(env_name)
    if cfg_key in PPO_CFG:
        return PPO_CFG[cfg_key]
    return default


PPO_LR_SCHEDULER = str(_ppo_cfg_raw("PPO_LR_SCHEDULER", "lr_scheduler", "none")).strip().lower() or "none"
PPO_ADAPTIVE_ENTROPY = str(_ppo_cfg_raw("PPO_ADAPTIVE_ENTROPY", "adaptive_entropy", "0")).strip().lower() in (
    "1",
    "true",
    "yes",
)
PPO_ENTROPY_TARGET = float(_ppo_cfg_raw("PPO_ENTROPY_TARGET", "entropy_target", "0.5"))
PPO_ENTROPY_ADAPT_LR = float(_ppo_cfg_raw("PPO_ENTROPY_ADAPT_LR", "entropy_adapt_lr", "0.05"))
_AZ_HP_SECTION = az_section_for(TRAIN_ALGO) if is_az_algo(TRAIN_ALGO) else "alphazero_tree"
AZ_CFG = data.get(_AZ_HP_SECTION, {}) if isinstance(data, dict) else {}
AZ_LR = float(AZ_CFG.get("learning_rate", LR))
AZ_BATCH_SIZE = int(AZ_CFG.get("batch_size", 128))
AZ_VALUE_LOSS_WEIGHT = float(AZ_CFG.get("value_loss_weight", 1.0))
AZ_L2_WEIGHT = float(AZ_CFG.get("l2_weight", 1e-6))
AZ_MCTS_SIMS = int(os.getenv("AZ_MCTS_SIMULATIONS", str(AZ_CFG.get("mcts_simulations", 96))))
AZ_C_PUCT = float(AZ_CFG.get("c_puct", 1.5))
AZ_DIR_ALPHA = float(AZ_CFG.get("dirichlet_alpha", 0.3))
AZ_DIR_EPS = float(AZ_CFG.get("dirichlet_eps", 0.25))
AZ_TEMP_OPENING_MOVES = int(AZ_CFG.get("temperature_opening_moves", 12))
AZ_TEMP_OPENING = float(AZ_CFG.get("temperature_opening_value", 1.0))
AZ_TEMP_LATE = float(AZ_CFG.get("temperature_late_value", 0.3))
AZ_REPLAY_CAPACITY = int(AZ_CFG.get("replay_capacity", 200000))
if is_az_algo(TRAIN_ALGO):
    AZ_MCTS_MODE = az_mcts_mode_for(TRAIN_ALGO)
else:
    AZ_MCTS_MODE = str(AZ_CFG.get("mcts_mode", "tree")).strip().lower() or "tree"
if AZ_MCTS_MODE not in {"proxy", "tree"}:
    AZ_MCTS_MODE = "tree"
AZ_MCTS_TOP_K_PER_HEAD = int(os.getenv("AZ_MCTS_TOP_K_PER_HEAD", str(AZ_CFG.get("mcts_top_k_per_head", 8))))
AZ_MCTS_MAX_DEPTH = int(os.getenv("AZ_MCTS_MAX_DEPTH", str(AZ_CFG.get("mcts_max_depth", 1))))
AZ_MCTS_ROOT_DIRICHLET_ONLY = str(
    os.getenv("AZ_MCTS_ROOT_DIRICHLET_ONLY", str(AZ_CFG.get("mcts_root_dirichlet_only", 1)))
).strip() == "1"
AZ_SNAPSHOT_OPP_DETERMINISTIC = str(
    os.getenv("AZ_SNAPSHOT_OPP_DETERMINISTIC", str(AZ_CFG.get("snapshot_opp_deterministic", 0)))
).strip() == "1"
AZ_OPPONENT_STOCHASTIC_EPS = float(
    os.getenv("AZ_OPPONENT_STOCHASTIC_EPS", str(AZ_CFG.get("opponent_stochastic_eps", 0.10)))
)
AZ_OPPONENT_STOCHASTIC_EPS = max(0.0, min(1.0, AZ_OPPONENT_STOCHASTIC_EPS))
AZ_OUTCOME_ONLY = str(os.getenv("AZ_OUTCOME_ONLY", str(AZ_CFG.get("outcome_only", 1)))).strip() == "1"
AZ_OUTCOME_VALUE_WIN = float(os.getenv("AZ_OUTCOME_VALUE_WIN", str(AZ_CFG.get("outcome_value_win", 1.0))))
AZ_OUTCOME_VALUE_LOSS = float(os.getenv("AZ_OUTCOME_VALUE_LOSS", str(AZ_CFG.get("outcome_value_loss", -1.0))))
AZ_OUTCOME_VALUE_DRAW = float(os.getenv("AZ_OUTCOME_VALUE_DRAW", str(AZ_CFG.get("outcome_value_draw", -0.25))))
AZ_OUTCOME_VALUE_WIN = max(-1.0, min(1.0, AZ_OUTCOME_VALUE_WIN))
AZ_OUTCOME_VALUE_LOSS = max(-1.0, min(1.0, AZ_OUTCOME_VALUE_LOSS))
AZ_OUTCOME_VALUE_DRAW = max(-1.0, min(1.0, AZ_OUTCOME_VALUE_DRAW))
AZ_NUM_ACTORS = max(
    1,
    int(
        os.getenv(
            "AZ_NUM_ACTORS",
            os.getenv("NUM_ACTORS", str(AZ_CFG.get("num_actors", 2))),
        )
    ),
)
AZ_ACTOR_BATCH_SEND = max(
    8,
    int(
        os.getenv(
            "AZ_ACTOR_BATCH_SEND",
            os.getenv("ACTOR_BATCH_SEND", str(AZ_CFG.get("actor_batch_send", 64))),
        )
    ),
)
AZ_ACTOR_QUEUE_MAX = max(
    64,
    int(
        os.getenv(
            "AZ_ACTOR_QUEUE_MAX",
            os.getenv("ACTOR_QUEUE_MAX", str(AZ_CFG.get("actor_queue_max", 256))),
        )
    ),
)
AZ_SYNC_EVERY_UPDATES = max(1, int(os.getenv("AZ_SYNC_EVERY_UPDATES", str(AZ_CFG.get("sync_every_updates", 2)))))
AZ_UPDATES_PER_ROLLOUT = max(1, int(os.getenv("AZ_UPDATES_PER_ROLLOUT", str(AZ_CFG.get("updates_per_rollout", 2)))))
AZ_REPLAY_MIN_SIZE = max(1, int(os.getenv("AZ_REPLAY_MIN_SIZE", str(AZ_CFG.get("replay_min_size", 512)))))
AZ_MAX_POLICY_STALENESS_UPDATES = int(
    os.getenv("AZ_MAX_POLICY_STALENESS_UPDATES", str(AZ_CFG.get("max_policy_staleness_updates", 600)))
)
AZ_BALANCED_OUTCOME_SAMPLING = str(
    os.getenv("AZ_BALANCED_OUTCOME_SAMPLING", str(AZ_CFG.get("balanced_outcome_sampling", 1)))
).strip() == "1"
AZ_DET_EVAL_GATE_WIN_MIN = float(os.getenv("AZ_DET_EVAL_GATE_WIN_MIN", str(AZ_CFG.get("det_eval_gate_win_min", 0.45))))
AZ_DET_EVAL_GATE_TURN_LIMIT_MAX = float(
    os.getenv("AZ_DET_EVAL_GATE_TURN_LIMIT_MAX", str(AZ_CFG.get("det_eval_gate_turn_limit_max", 0.60)))
)
AZ_DET_EVAL_GATE_DRAW_MAX = float(
    os.getenv("AZ_DET_EVAL_GATE_DRAW_MAX", str(AZ_CFG.get("det_eval_gate_draw_max", 0.70)))
)
AZ_HONEST_EVAL_EPISODES = max(1, int(os.getenv("AZ_HONEST_EVAL_EPISODES", "20")))
AZ_HONEST_EVAL_SIMS = max(1, int(os.getenv("AZ_HONEST_EVAL_SIMS", str(AZ_MCTS_SIMS))))
AZ_HONEST_EVAL_TEMPERATURE = float(os.getenv("AZ_HONEST_EVAL_TEMPERATURE", "0.06"))
AZ_HONEST_EVAL_DIR_EPS = float(os.getenv("AZ_HONEST_EVAL_DIR_EPS", "0.0"))
AZ_HIDDEN_SIZE = int(os.getenv("AZ_HIDDEN_SIZE", str(AZ_CFG.get("hidden_size", 256))))
AZ_NUM_LAYERS = int(os.getenv("AZ_NUM_LAYERS", str(AZ_CFG.get("num_layers", 2))))
AZ_VALUE_ENSEMBLE = int(os.getenv("AZ_VALUE_ENSEMBLE", str(AZ_CFG.get("value_ensemble", 1))))
AZ_LR_SCHEDULER = str(os.getenv("AZ_LR_SCHEDULER", str(AZ_CFG.get("lr_scheduler", "none")))).strip().lower() or "none"
AZ_LR_WARMUP_STEPS = int(os.getenv("AZ_LR_WARMUP_STEPS", str(AZ_CFG.get("lr_warmup_steps", 0))))
AZ_LR_TOTAL_STEPS = int(os.getenv("AZ_LR_TOTAL_STEPS", str(AZ_CFG.get("lr_total_steps", 0))))
AZ_MCTS_EVAL_CACHE_SIZE = int(os.getenv("AZ_MCTS_EVAL_CACHE_SIZE", str(AZ_CFG.get("mcts_eval_cache_size", 10000))))
AZ_C_PUCT_MIN = float(os.getenv("AZ_C_PUCT_MIN", str(AZ_CFG.get("c_puct_min", 1.0))))
AZ_C_PUCT_MAX = float(os.getenv("AZ_C_PUCT_MAX", str(AZ_CFG.get("c_puct_max", 2.0))))
AZ_C_PUCT_SCHEDULE = str(os.getenv("AZ_C_PUCT_SCHEDULE", str(AZ_CFG.get("c_puct_schedule", "none")))).strip().lower() or "none"
AZ_PW_ALPHA = float(os.getenv("AZ_PW_ALPHA", str(AZ_CFG.get("pw_alpha", 1.0))))
AZ_PW_BETA = float(os.getenv("AZ_PW_BETA", str(AZ_CFG.get("pw_beta", 0.5))))
AZ_PRIOR_WEIGHT_EARLY = float(os.getenv("AZ_PRIOR_WEIGHT_EARLY", str(AZ_CFG.get("prior_weight_early", 0.25))))
AZ_BALANCED_FACTION_SAMPLING = str(os.getenv("AZ_BALANCED_FACTION_SAMPLING", "0")).strip() == "1"
AZ_MCTS_BATCH_EVAL_SIZE = int(os.getenv("AZ_MCTS_BATCH_EVAL_SIZE", str(AZ_CFG.get("mcts_batch_eval_size", 16))))
AZ_MCTS_PARALLEL_SIMS = int(os.getenv("AZ_MCTS_PARALLEL_SIMS", str(AZ_CFG.get("mcts_parallel_sims", 8))))
# 1 = симулировать ход врага в rollout'ах (точнее, но дороже — enemyTurn самый тяжёлый);
# 0 = пропустить enemyTurn, брать оценку сети на листе (быстрее, оценки грубее).
AZ_MCTS_SIMULATE_ENEMY = str(
    os.getenv("AZ_MCTS_SIMULATE_ENEMY", str(AZ_CFG.get("mcts_simulate_enemy", 1)))
).strip() == "1"

# --- Inference Server (variant B) ---
AZ_INFERENCE_SERVER_REQUESTED = (
    str(os.getenv("AZ_INFERENCE_SERVER", str(AZ_CFG.get("inference_server_enabled", 0)))).strip() == "1"
)
AZ_INFERENCE_SERVER_MODE = str(
    os.getenv("AZ_INFERENCE_SERVER_MODE", str(AZ_CFG.get("inference_server_mode", "local")))
).strip().lower() or "local"
AZ_INFERENCE_REMOTE = AZ_INFERENCE_SERVER_MODE == "remote"
AZ_INFERENCE_SERVER_USING_FALLBACK = (
    AZ_INFERENCE_SERVER_REQUESTED and not AZ_INFERENCE_REMOTE and not torch.cuda.is_available()
)
AZ_INFERENCE_SERVER_ENABLED = AZ_INFERENCE_SERVER_REQUESTED and (
    AZ_INFERENCE_REMOTE or torch.cuda.is_available()
)
AZ_INFERENCE_SERVER_LOCAL = bool(AZ_INFERENCE_SERVER_ENABLED and not AZ_INFERENCE_REMOTE)
AZ_NUM_ENV_WORKERS = max(
    1,
    int(os.getenv("AZ_NUM_ENV_WORKERS", str(AZ_CFG.get("num_env_workers", AZ_NUM_ACTORS)))),
)
AZ_INFERENCE_BATCH_SIZE = max(
    1,
    int(os.getenv("AZ_INFERENCE_BATCH_SIZE", str(AZ_CFG.get("inference_batch_size", 32)))),
)
AZ_INFERENCE_BATCH_INTERVAL_MS = float(
    os.getenv("AZ_INFERENCE_BATCH_INTERVAL_MS", str(AZ_CFG.get("inference_batch_interval_ms", 10.0)))
)
AZ_INFERENCE_TIMEOUT = float(
    os.getenv("AZ_INFERENCE_TIMEOUT", str(AZ_CFG.get("inference_timeout", 5.0)))
)
AZ_INFERENCE_SYNC_INTERVAL = float(os.getenv("AZ_INFERENCE_SYNC_INTERVAL", "0.5"))
AZ_INFERENCE_REQUEST_QUEUE_MAX = max(
    8, int(os.getenv("AZ_INFERENCE_REQUEST_QUEUE_MAX", str(AZ_NUM_ENV_WORKERS * 4)))
)
AZ_INFERENCE_REMOTE_HOST = str(os.getenv("AZ_INFERENCE_REMOTE_HOST", AZ_CFG.get("inference_remote_host", "127.0.0.1")))
AZ_INFERENCE_REMOTE_PORT = int(os.getenv("AZ_INFERENCE_REMOTE_PORT", str(AZ_CFG.get("inference_remote_port", 5555))))
AZ_INFERENCE_REMOTE_AUTH_TOKEN = str(os.getenv("AZ_INFERENCE_REMOTE_AUTH_TOKEN", AZ_CFG.get("inference_remote_auth_token", "")))

# --- Distributed self-play (PC2 env workers → rollout ZMQ → learner data_q) ---
AZ_DISTRIBUTED_ACTORS = str(
    os.getenv("AZ_DISTRIBUTED_ACTORS", str(AZ_CFG.get("distributed_actors_enabled", 0)))
).strip() == "1"
AZ_DIST_ROLLOUT_BIND = str(
    os.getenv("AZ_DIST_ROLLOUT_BIND", str(AZ_CFG.get("distributed_actors_bind_host", "0.0.0.0")))
).strip() or "0.0.0.0"
AZ_DIST_ROLLOUT_PORT = max(
    1, int(os.getenv("AZ_DIST_ROLLOUT_PORT", str(AZ_CFG.get("distributed_actors_port", 5557))))
)
AZ_DIST_AUTH_TOKEN = str(
    os.getenv("AZ_DIST_AUTH_TOKEN", str(AZ_CFG.get("distributed_actors_auth_token", "")))
).strip() or str(AZ_INFERENCE_REMOTE_AUTH_TOKEN or "")
AZ_DIST_DRAIN_SEC = max(
    1.0, float(os.getenv("AZ_DIST_DRAIN_SEC", str(AZ_CFG.get("distributed_actors_drain_sec", 30.0))))
)
AZ_DIST_ZMQ_HWM = max(8, int(os.getenv("AZ_DIST_ZMQ_HWM", str(AZ_CFG.get("distributed_actors_zmq_hwm", 256)))))


def _clear_az_dist_stop_flag() -> None:
    path = az_dist_stop_flag_path()
    try:
        if os.path.isfile(path):
            os.remove(path)
    except Exception as exc:
        append_agent_log(f"[AZ][DIST][WARN] не удалось удалить stop.flag: {path} exc={exc}")


def _touch_az_dist_stop_flag() -> None:
    path = az_dist_stop_flag_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("1\n")
        append_agent_log(f"[AZ][DIST] stop.flag записан: {path}")
    except Exception as exc:
        append_agent_log(
            f"[AZ][DIST][WARN] не удалось записать stop.flag: {path} exc={exc}. "
            "Где: train._touch_az_dist_stop_flag. Что делать: проверьте SMB actor_sync."
        )


if AZ_DISTRIBUTED_ACTORS:
    append_agent_log(
        f"[AZ][DIST][CONFIG] enabled=1 bind={AZ_DIST_ROLLOUT_BIND}:{AZ_DIST_ROLLOUT_PORT} "
        f"drain_sec={AZ_DIST_DRAIN_SEC}"
    )

if AZ_INFERENCE_SERVER_USING_FALLBACK:
    append_agent_log(
        "[AZ][CONFIG][FALLBACK] AZ_INFERENCE_SERVER=1 запрошен, но CUDA недоступна. "
        "Откат на вариант A (CPU акторы). Где: train.py (AZ constants). "
        "Что делать: установить CUDA-драйвер или использовать вариант A (inference_server_enabled=0)."
    )
elif AZ_INFERENCE_SERVER_ENABLED:
    append_agent_log(
        f"[AZ][CONFIG] inference_server={int(AZ_INFERENCE_SERVER_ENABLED)} "
        f"mode={AZ_INFERENCE_SERVER_MODE} env_workers={AZ_NUM_ENV_WORKERS} "
        f"batch={AZ_INFERENCE_BATCH_SIZE} interval_ms={AZ_INFERENCE_BATCH_INTERVAL_MS}"
    )


def _make_alphazero(n_observations, n_actions, **overrides):
    return make_alphazero_net(n_observations, n_actions, **overrides)


def _build_az_lr_scheduler(optimizer, total_steps_hint=None):
    cfg = AlphaZeroTrainConfig(
        lr=AZ_LR,
        lr_scheduler_type=AZ_LR_SCHEDULER,
        lr_warmup_steps=AZ_LR_WARMUP_STEPS,
        lr_total_steps=AZ_LR_TOTAL_STEPS or int(total_steps_hint or 0),
    )
    return build_alphazero_lr_scheduler(optimizer, cfg, total_steps_hint=total_steps_hint)


def _az_mcts_config(*, progress: float = 0.0, move_count: int = 0) -> MCTSConfig:
    return MCTSConfig(
        simulations=int(AZ_MCTS_SIMS),
        c_puct=float(AZ_C_PUCT),
        c_puct_min=float(AZ_C_PUCT_MIN),
        c_puct_max=float(AZ_C_PUCT_MAX),
        c_puct_schedule=str(AZ_C_PUCT_SCHEDULE),
        dirichlet_alpha=float(AZ_DIR_ALPHA),
        dirichlet_eps=float(AZ_DIR_EPS),
        top_k_per_head=int(AZ_MCTS_TOP_K_PER_HEAD),
        max_depth=int(AZ_MCTS_MAX_DEPTH),
        mode=str(AZ_MCTS_MODE),
        root_dirichlet_only=bool(AZ_MCTS_ROOT_DIRICHLET_ONLY),
        eval_cache_size=int(AZ_MCTS_EVAL_CACHE_SIZE),
        pw_alpha=float(AZ_PW_ALPHA),
        pw_beta=float(AZ_PW_BETA),
        prior_weight_early=float(AZ_PRIOR_WEIGHT_EARLY),
        progress=float(progress),
        move_count=int(move_count),
        temperature_opening_moves=int(AZ_TEMP_OPENING_MOVES),
        batch_eval_size=int(AZ_MCTS_BATCH_EVAL_SIZE),
        parallel_simulations=int(AZ_MCTS_PARALLEL_SIMS),
        simulate_enemy_in_tree=bool(AZ_MCTS_SIMULATE_ENEMY),
    )


def _az_honest_eval_mcts_config(*, mcts_mode: str) -> MCTSConfig:
    """MCTS config for inline AZ DET-eval (no train Dirichlet noise, eval sims/temp)."""
    return MCTSConfig(
        simulations=int(AZ_HONEST_EVAL_SIMS),
        c_puct=float(AZ_C_PUCT),
        c_puct_min=float(AZ_C_PUCT_MIN),
        c_puct_max=float(AZ_C_PUCT_MAX),
        c_puct_schedule=str(AZ_C_PUCT_SCHEDULE),
        dirichlet_alpha=float(AZ_DIR_ALPHA),
        dirichlet_eps=float(AZ_HONEST_EVAL_DIR_EPS),
        top_k_per_head=int(AZ_MCTS_TOP_K_PER_HEAD),
        max_depth=int(AZ_MCTS_MAX_DEPTH),
        mode=str(mcts_mode),
        root_dirichlet_only=bool(AZ_MCTS_ROOT_DIRICHLET_ONLY),
        eval_cache_size=int(AZ_MCTS_EVAL_CACHE_SIZE),
        pw_alpha=float(AZ_PW_ALPHA),
        pw_beta=float(AZ_PW_BETA),
        prior_weight_early=float(AZ_PRIOR_WEIGHT_EARLY),
        temperature_opening_moves=int(AZ_TEMP_OPENING_MOVES),
        batch_eval_size=int(AZ_MCTS_BATCH_EVAL_SIZE),
        parallel_simulations=int(AZ_MCTS_PARALLEL_SIMS),
    )


GMZ_CFG = data.get("gumbel_muzero", {}) if isinstance(data, dict) else {}
GMZ_LR = float(GMZ_CFG.get("learning_rate", AZ_LR))
GMZ_BATCH_SIZE = int(GMZ_CFG.get("batch_size", 128))
GMZ_UNROLL_STEPS = int(GMZ_CFG.get("unroll_steps", 5))
GMZ_REWARD_LOSS_WEIGHT = float(GMZ_CFG.get("reward_loss_weight", 1.0))
GMZ_VALUE_LOSS_WEIGHT = float(GMZ_CFG.get("value_loss_weight", 1.0))
GMZ_L2_WEIGHT = float(GMZ_CFG.get("l2_weight", 1e-6))
GMZ_DISCOUNT = float(GMZ_CFG.get("discount", 0.997))
GMZ_REPLAY_CAPACITY = int(GMZ_CFG.get("replay_capacity", 250000))
GMZ_NUM_ACTORS = max(1, int(os.getenv("GMZ_NUM_ACTORS", str(GMZ_CFG.get("num_actors", AZ_NUM_ACTORS)))))
GMZ_ACTOR_BATCH_SEND = max(8, int(os.getenv("GMZ_ACTOR_BATCH_SEND", str(GMZ_CFG.get("actor_batch_send", 64)))))
GMZ_ACTOR_QUEUE_MAX = max(64, int(os.getenv("GMZ_ACTOR_QUEUE_MAX", str(GMZ_CFG.get("actor_queue_max", 256)))))
GMZ_SYNC_EVERY_UPDATES = max(1, int(os.getenv("GMZ_SYNC_EVERY_UPDATES", str(GMZ_CFG.get("sync_every_updates", 2)))))
GMZ_UPDATES_PER_ROLLOUT = max(1, int(os.getenv("GMZ_UPDATES_PER_ROLLOUT", str(GMZ_CFG.get("updates_per_rollout", 2)))))
GMZ_REPLAY_MIN_SIZE = max(1, int(os.getenv("GMZ_REPLAY_MIN_SIZE", str(GMZ_CFG.get("replay_min_size", 512)))))
GMZ_MAX_POLICY_STALENESS_UPDATES = int(
    os.getenv("GMZ_MAX_POLICY_STALENESS_UPDATES", str(GMZ_CFG.get("max_policy_staleness_updates", 600)))
)
GMZ_LATENT_DIM = int(os.getenv("GMZ_LATENT_DIM", str(GMZ_CFG.get("latent_dim", 256))))
GMZ_HIDDEN_DIM = int(os.getenv("GMZ_HIDDEN_DIM", str(GMZ_CFG.get("hidden_dim", 256))))
GMZ_NUM_LAYERS = int(os.getenv("GMZ_NUM_LAYERS", str(GMZ_CFG.get("num_layers", 2))))
GMZ_ACTION_EMBED_DIM = int(os.getenv("GMZ_ACTION_EMBED_DIM", str(GMZ_CFG.get("action_embed_dim", 64))))
GMZ_MCTS_SIMS = int(os.getenv("GMZ_MCTS_SIMS", str(GMZ_CFG.get("num_simulations", 32))))
GMZ_ROOT_TOP_K = int(os.getenv("GMZ_ROOT_TOP_K", str(GMZ_CFG.get("root_top_k", 8))))
GMZ_GUMBEL_SCALE = float(os.getenv("GMZ_GUMBEL_SCALE", str(GMZ_CFG.get("gumbel_scale", 1.0))))
GMZ_SEARCH_TEMP = float(os.getenv("GMZ_SEARCH_TEMPERATURE", str(GMZ_CFG.get("search_temperature", 0.15))))
GMZ_PRIOR_WEIGHT = float(os.getenv("GMZ_PRIOR_WEIGHT", str(GMZ_CFG.get("prior_weight", 0.25))))
GMZ_MAX_GRAD_NORM = float(os.getenv("GMZ_MAX_GRAD_NORM", str(GMZ_CFG.get("max_grad_norm", 0.5))))
GMZ_TBPTT_TRUNCATE = int(os.getenv("GMZ_TBPTT_TRUNCATE", str(GMZ_CFG.get("tbptt_truncate", 3))))
GMZ_CONSISTENCY_W = float(os.getenv("GMZ_CONSISTENCY_W", str(GMZ_CFG.get("consistency_loss_weight", "1.0"))))
GMZ_LR_SCHEDULER = str(os.getenv("GMZ_LR_SCHEDULER", str(GMZ_CFG.get("lr_scheduler", "none"))))
GMZ_LR_WARMUP_STEPS = int(os.getenv("GMZ_LR_WARMUP_STEPS", str(GMZ_CFG.get("lr_warmup_steps", 0))))
GMZ_LR_TOTAL_STEPS = int(os.getenv("GMZ_LR_TOTAL_STEPS", str(GMZ_CFG.get("lr_total_steps", 0))))
GMZ_TEMP_OPENING_MOVES = int(os.getenv("GMZ_TEMP_OPENING_MOVES", str(GMZ_CFG.get("temperature_opening_moves", 12))))
GMZ_TEMP_OPENING = float(os.getenv("GMZ_TEMP_OPENING", str(GMZ_CFG.get("temperature_opening_value", 1.0))))
GMZ_TEMP_LATE = float(os.getenv("GMZ_TEMP_LATE", str(GMZ_CFG.get("temperature_late_value", 0.25))))
GMZ_OUTCOME_ONLY = str(os.getenv("GMZ_OUTCOME_ONLY", str(GMZ_CFG.get("outcome_only", 1)))).strip() == "1"
GMZ_OUTCOME_VALUE_WIN = float(os.getenv("GMZ_OUTCOME_VALUE_WIN", str(GMZ_CFG.get("outcome_value_win", 1.0))))
GMZ_OUTCOME_VALUE_LOSS = float(os.getenv("GMZ_OUTCOME_VALUE_LOSS", str(GMZ_CFG.get("outcome_value_loss", -1.0))))
GMZ_OUTCOME_VALUE_DRAW = float(os.getenv("GMZ_OUTCOME_VALUE_DRAW", str(GMZ_CFG.get("outcome_value_draw", -0.25))))
GMZ_BATCH_RECURRENT = str(os.getenv("GMZ_BATCH_RECURRENT", str(GMZ_CFG.get("batch_recurrent", 1)))).strip() == "1"
# A1: tight atom range for value/reward heads — biggest single improvement
# "tight" = [-1.05, 1.05] for value, [-0.06, 0.06] for reward (matches actual target range)
# "legacy" = [-20, 20] / [-5, 5] (backward compatible with old checkpoints)
GMZ_ATOM_RANGE = str(os.getenv("GMZ_ATOM_RANGE", str(GMZ_CFG.get("atom_range", "tight")))).lower()
# B1: V-trace on full unroll (Retrace-style, not just t=0) — adds ~10-15% wall-clock
GMZ_VTRACE_FULL = int(os.getenv("GMZ_VTRACE_FULL", str(GMZ_CFG.get("vtrace_full", 1))))
# B1: V-trace IS weight clips (rho/c)
GMZ_VTRACE_RHO_CLIP = float(os.getenv("GMZ_VTRACE_RHO_CLIP", str(GMZ_CFG.get("vtrace_rho_clip", 0.7))))
GMZ_VTRACE_C_CLIP = float(os.getenv("GMZ_VTRACE_C_CLIP", str(GMZ_CFG.get("vtrace_c_clip", 0.7))))
# B2: fraction of training steps to run reanalysis (0=disabled)
GMZ_REANALYZE_FRACTION = float(os.getenv("GMZ_REANALYZE_FRACTION", str(GMZ_CFG.get("reanalyze_fraction", 0.15))))
# B3: tree reuse across moves
GMZ_TREE_REUSE = str(os.getenv("GMZ_TREE_REUSE", str(GMZ_CFG.get("tree_reuse", 1)))).strip() == "1"
GMZ_HONEST_EVAL_EPISODES = max(1, int(os.getenv("GMZ_HONEST_EVAL_EPISODES", "20")))
GMZ_HONEST_EVAL_SIMS = max(1, int(os.getenv("GMZ_HONEST_EVAL_SIMS", str(GMZ_MCTS_SIMS))))
GMZ_HONEST_EVAL_TOP_K = max(1, int(os.getenv("GMZ_HONEST_EVAL_TOP_K", str(GMZ_ROOT_TOP_K))))
GMZ_HONEST_EVAL_TEMPERATURE = float(os.getenv("GMZ_HONEST_EVAL_TEMPERATURE", "0.10"))
# B4: EMA tau for consistency target + torch.compile flags
GMZ_EMA_TAU = float(os.getenv("GMZ_EMA_TAU", str(GMZ_CFG.get("ema_tau", 0.005))))
if "GMZ_ACTOR_COMPILE" in os.environ:
    GMZ_ACTOR_COMPILE = str(os.getenv("GMZ_ACTOR_COMPILE", "1")).strip() == "1"
else:
    # С CUDA — learner_compile; без CUDA — compile на CPU-акторах (вариант A).
    GMZ_ACTOR_COMPILE = not bool(torch.cuda.is_available())
GMZ_LEARNER_COMPILE = str(os.getenv("GMZ_LEARNER_COMPILE", str(GMZ_CFG.get("learner_compile", 1)))).strip() == "1"
# Вариант A: GPU-акторы; вариант B: inference_server + CPU env workers
GMZ_ACTOR_DEVICE_REQUESTED = str(os.getenv("GMZ_ACTOR_DEVICE", str(GMZ_CFG.get("actor_device", "cuda")))).strip().lower()
if GMZ_ACTOR_DEVICE_REQUESTED not in ("cpu", "cuda", "inference_server"):
    GMZ_ACTOR_DEVICE_REQUESTED = "cuda"
GMZ_ACTOR_MAX_CUDA = max(1, int(os.getenv("GMZ_ACTOR_MAX_CUDA", str(GMZ_CFG.get("actor_max_cuda", 2)))))
GMZ_ACTOR_CPU_FALLBACK_NUM_ACTORS = 8  # прежний дефолт self-play на CPU
GMZ_INFERENCE_SERVER_MODE = str(
    os.getenv("GMZ_INFERENCE_SERVER_MODE", str(GMZ_CFG.get("inference_server_mode", "local")))
).strip().lower()
if GMZ_INFERENCE_SERVER_MODE == "inference_server":
    GMZ_INFERENCE_SERVER_MODE = "local"
GMZ_INFERENCE_REMOTE = GMZ_INFERENCE_SERVER_MODE == "remote"
GMZ_INFERENCE_REMOTE_HOST = str(os.getenv("GMZ_INFERENCE_REMOTE_HOST", "127.0.0.1")).strip() or "127.0.0.1"
GMZ_INFERENCE_REMOTE_PORT = max(1, int(os.getenv("GMZ_INFERENCE_REMOTE_PORT", "5555")))
GMZ_INFERENCE_REMOTE_AUTH_TOKEN = str(os.getenv("GMZ_INFERENCE_REMOTE_AUTH_TOKEN", "")).strip()
GMZ_INFERENCE_SERVER_REQUESTED = (
    GMZ_INFERENCE_REMOTE
    or str(os.getenv("GMZ_INFERENCE_SERVER", str(GMZ_CFG.get("inference_server_enabled", 0)))).strip() == "1"
    or GMZ_ACTOR_DEVICE_REQUESTED == "inference_server"
)
GMZ_INFERENCE_SERVER_USING_FALLBACK = (
    GMZ_INFERENCE_SERVER_REQUESTED and not GMZ_INFERENCE_REMOTE and not torch.cuda.is_available()
)
GMZ_INFERENCE_SERVER_ENABLED = GMZ_INFERENCE_SERVER_REQUESTED and (
    GMZ_INFERENCE_REMOTE or torch.cuda.is_available()
)
GMZ_INFERENCE_SERVER_LOCAL = bool(GMZ_INFERENCE_SERVER_ENABLED and not GMZ_INFERENCE_REMOTE)
GMZ_NUM_ENV_WORKERS = max(
    1,
    int(
        os.getenv(
            "GMZ_NUM_ENV_WORKERS",
            str(GMZ_CFG.get("num_env_workers", GMZ_CFG.get("num_actors", 6))),
        )
    ),
)
GMZ_INFERENCE_BATCH_SIZE = max(1, int(os.getenv("GMZ_INFERENCE_BATCH_SIZE", str(GMZ_CFG.get("inference_batch_size", 8)))))
GMZ_INFERENCE_BATCH_INTERVAL_MS = float(
    os.getenv("GMZ_INFERENCE_BATCH_INTERVAL_MS", str(GMZ_CFG.get("inference_batch_interval_ms", 20.0)))
)
GMZ_INFERENCE_TIMEOUT = float(os.getenv("GMZ_INFERENCE_TIMEOUT", str(GMZ_CFG.get("inference_timeout", 5.0))))
GMZ_INFERENCE_REQUEST_QUEUE_MAX = max(
    4, int(os.getenv("GMZ_INFERENCE_REQUEST_QUEUE_MAX", str(GMZ_CFG.get("inference_request_queue_max", 32))))
)
GMZ_INFERENCE_SERVER_COMPILE = str(
    os.getenv("GMZ_INFERENCE_SERVER_COMPILE", str(GMZ_CFG.get("inference_server_compile", 1)))
).strip() == "1"
GMZ_CLEAR_TREE_ON_WEIGHT_SYNC = str(
    os.getenv("GMZ_CLEAR_TREE_ON_WEIGHT_SYNC", str(GMZ_CFG.get("clear_tree_on_weight_sync", 0)))
).strip() == "1"
GMZ_ACTOR_USING_CUDA_FALLBACK = (
    not GMZ_INFERENCE_SERVER_ENABLED
    and GMZ_ACTOR_DEVICE_REQUESTED == "cuda"
    and not torch.cuda.is_available()
)
if GMZ_INFERENCE_SERVER_ENABLED:
    GMZ_ACTOR_DEVICE = "inference_server"
    GMZ_ACTOR_DEVICE_CUDA = False
    GMZ_ACTOR_EFFECTIVE_NUM_ACTORS = int(GMZ_NUM_ENV_WORKERS)
elif GMZ_INFERENCE_SERVER_USING_FALLBACK:
    GMZ_ACTOR_DEVICE = "cpu"
    GMZ_ACTOR_DEVICE_CUDA = False
    GMZ_ACTOR_EFFECTIVE_NUM_ACTORS = int(GMZ_ACTOR_CPU_FALLBACK_NUM_ACTORS)
elif GMZ_ACTOR_USING_CUDA_FALLBACK:
    GMZ_ACTOR_DEVICE = "cpu"
    GMZ_ACTOR_DEVICE_CUDA = False
    GMZ_ACTOR_EFFECTIVE_NUM_ACTORS = int(GMZ_ACTOR_CPU_FALLBACK_NUM_ACTORS)
else:
    GMZ_ACTOR_DEVICE = GMZ_ACTOR_DEVICE_REQUESTED
    GMZ_ACTOR_DEVICE_CUDA = GMZ_ACTOR_DEVICE == "cuda" and torch.cuda.is_available()
    if GMZ_ACTOR_DEVICE_CUDA:
        GMZ_ACTOR_EFFECTIVE_NUM_ACTORS = min(int(GMZ_NUM_ACTORS), int(GMZ_ACTOR_MAX_CUDA))
    else:
        GMZ_ACTOR_EFFECTIVE_NUM_ACTORS = int(GMZ_NUM_ACTORS)

# ============================================================
# (C) Несколько обучающих апдейтов на один шаг среды
# ============================================================
UPDATES_PER_STEP = int(data.get("updates_per_step", 1))  # 1 = как было раньше
WARMUP_STEPS     = int(data.get("warmup_steps", 0))      # 0 = без прогрева


def _cleanup_train_envs(env_contexts, subproc_envs, use_subproc: bool) -> None:
    if use_subproc:
        for ctx in env_contexts:
            try:
                ctx["conn"].send(("close", None))
                ctx["conn"].recv()
            except Exception:
                pass
        for proc in subproc_envs:
            try:
                proc.join(timeout=1.0)
            except Exception:
                pass
    else:
        for ctx in env_contexts:
            try:
                ctx["env"].close()
            except Exception:
                pass


def _ppo_arch_dict(actor_critic) -> dict:
    return {
        "hidden_size": int(getattr(actor_critic, "hidden_size", 256)),
        "num_layers": int(getattr(actor_critic, "num_layers", 2)),
        "n_value_ensemble": int(getattr(actor_critic, "n_value_ensemble", 1)),
    }


def _ppo_checkpoint_extra(actor_critic, optimizer, lr_scheduler=None) -> dict:
    extra = {"arch": _ppo_arch_dict(actor_critic)}
    if lr_scheduler is not None:
        extra["lr_scheduler"] = lr_scheduler.state_dict()
    return extra


def _build_ppo_lr_scheduler(optimizer, total_steps_hint=None):
    if PPO_LR_SCHEDULER == "cosine":
        t_max = max(1, int(total_steps_hint or int(os.getenv("TOT_LIFE_T", "1000")) * 50))
        return torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=t_max)
    if PPO_LR_SCHEDULER == "plateau":
        return torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode="min", factor=0.5, patience=50, min_lr=1e-6
        )
    return None


def _step_ppo_lr_scheduler(lr_scheduler, loss_value: float | None = None) -> None:
    if lr_scheduler is None:
        return
    if isinstance(lr_scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau):
        if loss_value is not None:
            lr_scheduler.step(float(loss_value))
    else:
        lr_scheduler.step()


def _run_ppo_update_loop(
    actor_critic,
    optimizer,
    batch,
    *,
    entropy_coef: float,
    lr_scheduler=None,
) -> tuple[dict, float, int]:
    """PPO clipped objective over batch; returns metrics, updated entropy_coef, update count."""
    num_samples = int(batch.obs.shape[0])
    if num_samples <= 0:
        return {"policy_loss": 0.0, "value_loss": 0.0, "entropy": 0.0, "approx_kl": 0.0, "clip_fraction": 0.0}, entropy_coef, 0

    idx_all = np.arange(num_samples)
    ppo_metrics = {"policy_loss": 0.0, "value_loss": 0.0, "entropy": 0.0, "approx_kl": 0.0, "clip_fraction": 0.0}
    updates = 0
    for _ in range(max(1, PPO_UPDATE_EPOCHS)):
        np.random.shuffle(idx_all)
        epoch_kl = 0.0
        epoch_kl_steps = 0
        for start in range(0, num_samples, max(1, PPO_MINIBATCH_SIZE)):
            mb_idx = idx_all[start : start + max(1, PPO_MINIBATCH_SIZE)]
            mb_obs = batch.obs[mb_idx]
            mb_actions = batch.actions[mb_idx]
            mb_old_logp = batch.logprobs[mb_idx]
            mb_adv = batch.advantages[mb_idx]
            mb_returns = batch.returns[mb_idx]
            mb_masks = [m[mb_idx] for m in batch.masks_by_head]
            new_logp, entropy, values = actor_critic.evaluate_actions(mb_obs, mb_actions, masks_by_head=mb_masks)
            ratio = torch.exp(new_logp - mb_old_logp)
            clipped_ratio = torch.clamp(ratio, 1.0 - PPO_CLIP_RATIO, 1.0 + PPO_CLIP_RATIO)
            policy_loss = -torch.min(ratio * mb_adv, clipped_ratio * mb_adv).mean()
            value_loss = F.mse_loss(values, mb_returns)
            entropy_loss = entropy.mean()
            loss = policy_loss + PPO_VALUE_COEF * value_loss - float(entropy_coef) * entropy_loss
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(actor_critic.parameters(), PPO_MAX_GRAD_NORM)
            optimizer.step()
            approx_kl = (mb_old_logp - new_logp).mean().detach()
            clip_frac = ((ratio - 1.0).abs() > PPO_CLIP_RATIO).float().mean().detach()
            ppo_metrics["policy_loss"] += float(policy_loss.detach().item())
            ppo_metrics["value_loss"] += float(value_loss.detach().item())
            ppo_metrics["entropy"] += float(entropy_loss.detach().item())
            ppo_metrics["approx_kl"] += float(approx_kl.item())
            ppo_metrics["clip_fraction"] += float(clip_frac.item())
            updates += 1
            epoch_kl += float(approx_kl.item())
            epoch_kl_steps += 1
        mean_epoch_kl = epoch_kl / max(1, epoch_kl_steps)
        if mean_epoch_kl > PPO_TARGET_KL:
            append_agent_log(
                f"[PPO] Ранний stop эпохи по KL: epoch_kl={mean_epoch_kl:.6f} > target_kl={PPO_TARGET_KL:.6f}."
            )
            break
    if updates > 0:
        for key in ppo_metrics:
            ppo_metrics[key] /= updates
    total_loss = ppo_metrics["policy_loss"] + PPO_VALUE_COEF * ppo_metrics["value_loss"]
    _step_ppo_lr_scheduler(lr_scheduler, loss_value=total_loss)
    if PPO_ADAPTIVE_ENTROPY and updates > 0:
        entropy_coef = update_ppo_entropy_coef(
            entropy_coef,
            ppo_metrics["entropy"],
            PPO_ENTROPY_TARGET,
            adapt_lr=PPO_ENTROPY_ADAPT_LR,
        )
        append_agent_log(
            f"[PPO][ENT] coef={entropy_coef:.6f} entropy={ppo_metrics['entropy']:.6f} "
            f"target={PPO_ENTROPY_TARGET:.6f}"
        )
    return ppo_metrics, entropy_coef, updates


def _save_ppo_checkpoint(
    actor_critic,
    optimizer,
    episode,
    n_actions,
    n_observations,
    model,
    enemy,
    env_contract,
    *,
    roster_config: dict | None = None,
    b_len: int | None = None,
    b_hei: int | None = None,
    lr_scheduler=None,
):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = os.path.join(MODELS_DIR, "ppo", f"ppo-run-{timestamp}")
    os.makedirs(run_dir, exist_ok=True)
    checkpoint_path = os.path.join(run_dir, f"checkpoint_ep{int(episode)}.pth")
    payload = {
        "algo": "ppo",
        "net_type": "ppo_actor_critic",
        "policy_net": actor_critic.state_dict(),
        "actor_critic": actor_critic.state_dict(),
        "optimizer": optimizer.state_dict(),
        "episode": int(episode),
        "n_actions": [int(x) for x in n_actions],
        "n_observations": int(n_observations),
        "env_contract": env_contract,
    }
    payload.update(_ppo_checkpoint_extra(actor_critic, optimizer, lr_scheduler))
    torch.save(payload, checkpoint_path)
    pickle_path = os.path.join(run_dir, f"model-{timestamp}.pickle")
    if model is None or enemy is None:
        # Actor-learner PPO не держит готовые roster'ы в этом месте.
        # Но Viewer требует (env=None, model=list[Unit], enemy=list[Unit]) в pickle.
        try:
            cfg = dict(roster_config or {})
            if b_len is not None:
                cfg["b_len"] = int(b_len)
            if b_hei is not None:
                cfg["b_hei"] = int(b_hei)
            bb_len = int(cfg.get("b_len", 0) or 0)
            bb_hei = int(cfg.get("b_hei", 0) or 0)
            if bb_len > 0 and bb_hei > 0:
                enemy, model = _build_units_from_config(cfg, bb_len, bb_hei)
        except Exception:
            pass
    with open(pickle_path, "wb") as handle:
        pickle.dump((None, model, enemy), handle)
    append_agent_log(f"[PPO][SAVE] checkpoint={checkpoint_path}")
    append_agent_log(f"[PPO][SAVE] pickle={pickle_path}")
    return checkpoint_path


def run_ppo_training(
    env_contexts,
    totLifeT,
    n_actions,
    n_observations,
    env_contract,
    model,
    enemy,
    roster_config: dict,
    *,
    learner_identity: AgentIdentity,
):
    if not env_contexts:
        raise RuntimeError("PPO: пустой список env_contexts.")
    ctx = env_contexts[0]
    env = ctx["env"]
    len_model = int(ctx["len_model"])
    b_len = int(roster_config.get("b_len", 0))
    b_hei = int(roster_config.get("b_hei", 0))
    actor_critic = make_actor_critic(n_observations, n_actions).to(device)
    optimizer = optim.AdamW(actor_critic.parameters(), lr=PPO_LR, amsgrad=True)
    _patch_optimizer_methods_no_compile(optimizer)
    ppo_lr_scheduler = _build_ppo_lr_scheduler(optimizer, total_steps_hint=int(totLifeT) * 20)
    buffer = PPORolloutBuffer()
    global_step = 0
    ppo_update_step = 0
    entropy_coef = float(PPO_ENTROPY_COEF)
    last_checkpoint = ""
    run_id = str(random.randint(1000000, 9999999))
    model_name = datetime.datetime.now().strftime("%d-%H%M%S")
    metrics_obj = metrics(os.path.join(MODELS_DIR, "ppo"), run_id, model_name)
    ep_rows = []
    last_det_eval_ep = 0
    ppo_kw = ppo_kwargs_from_env()
    append_agent_log(
        f"[PPO][CONFIG] hidden_size={ppo_kw['hidden_size']} num_layers={ppo_kw['num_layers']} "
        f"n_value_ensemble={ppo_kw['n_value_ensemble']} lr_scheduler={PPO_LR_SCHEDULER} "
        f"adaptive_entropy={int(PPO_ADAPTIVE_ENTROPY)} vectorized_gae={os.getenv('PPO_VECTORIZED_GAE', '0')}"
    )

    for episode in range(1, int(totLifeT) + 1):
        state, info0 = env.reset(options={"m": model, "e": enemy, "trunc": True})
        obs = to_np_state(state)
        done = False
        ep_reward = 0.0
        ep_len = 0
        buffer.clear()
        # GUI прогресс читает stdout и парсит шаблон ep=X/Y.
        print(f"[PPO] ep={episode}/{totLifeT} rollout_start", flush=True)
        append_agent_log(f"[PPO][EP] ep={episode}/{totLifeT} сбор rollout...")
        final_info = {}
        while not done:
            env_unwrapped = unwrap_env(env)
            env_unwrapped.enemyTurn(trunc=True)
            if bool(getattr(env_unwrapped, "game_over", False)):
                done = True
                final_info = env_unwrapped.get_info() if hasattr(env_unwrapped, "get_info") else {}
                break
            obs_t = torch.tensor(obs, dtype=torch.float32, device=device).unsqueeze(0)
            masks_cpu = build_action_masks_by_head(env, len_model, log_fn=None, debug=False)
            masks_batch = [m.to(device).unsqueeze(0) for m in masks_cpu]
            action_t, logprob_t, value_t = actor_critic.act(obs_t, masks_by_head=masks_batch, deterministic=False)
            action_np = action_t.squeeze(0).detach().cpu().numpy()
            action_dict = convertToDict(torch.tensor([action_np], device="cpu"))
            next_obs, reward, done, _, info = env.step(action_dict)
            final_info = info or {}
            buffer.add(
                obs=obs,
                action=action_np,
                logprob=float(logprob_t.item()),
                reward=float(reward),
                done=bool(done),
                value=float(value_t.item()),
                masks_by_head=[m.detach().cpu().numpy() for m in masks_cpu],
            )
            obs = to_np_state(next_obs) if not done else obs
            ep_reward += float(reward)
            ep_len += 1
            global_step += 1

        batch = buffer.to_tensors(device=device, gamma=PPO_GAMMA, gae_lambda=PPO_GAE_LAMBDA, normalize_adv=True)
        if int(batch.obs.shape[0]) == 0:
            continue
        ppo_metrics, entropy_coef, updates = _run_ppo_update_loop(
            actor_critic,
            optimizer,
            batch,
            entropy_coef=entropy_coef,
            lr_scheduler=ppo_lr_scheduler,
        )
        ppo_update_step += int(updates)
        metrics_obj.updateRew(ep_reward)
        metrics_obj.updateEpLen(ep_len)
        metrics_obj.updateLoss(ppo_metrics["policy_loss"] + PPO_VALUE_COEF * ppo_metrics["value_loss"])

        model_vp = float(final_info.get("model VP", 0.0) or 0.0)
        player_vp = float(final_info.get("player VP", 0.0) or 0.0)
        vp_diff = model_vp - player_vp
        end_reason = str(final_info.get("end reason", "unknown") or "unknown")
        winner_raw = str(final_info.get("winner", "draw")).strip().lower()
        if end_reason == "wipeout_enemy":
            result = "win"
        elif end_reason == "wipeout_model":
            result = "loss"
        elif str(end_reason).startswith("turn_limit"):
            if vp_diff > 0:
                result = "win"
            elif vp_diff < 0:
                result = "loss"
            else:
                result = "draw"
        elif winner_raw in {"model", "learner", "ai"}:
            result = "win"
        elif winner_raw in {"enemy", "player", "opponent"}:
            result = "loss"
        elif vp_diff > 0:
            result = "win"
        elif vp_diff < 0:
            result = "loss"
        else:
            result = "draw"
        episode_row = {
            "episode": int(episode),
            "ep_reward": float(ep_reward),
            "ep_len": int(ep_len),
            "turn": int(final_info.get("turn", ep_len) or ep_len),
            "model_vp": float(model_vp),
            "player_vp": float(player_vp),
            "vp_diff": float(vp_diff),
            "result": result,
            "end_reason": end_reason,
            "end_code": str(final_info.get("end code", end_reason)),
        }
        ep_rows.append(episode_row)
        append_episode_diagnostics(
            run_id=run_id,
            episode_row=episode_row,
            diagnostics={
                "algo": "ppo",
                "policy_loss": float(ppo_metrics["policy_loss"]),
                "value_loss": float(ppo_metrics["value_loss"]),
                "entropy": float(ppo_metrics["entropy"]),
                "approx_kl": float(ppo_metrics["approx_kl"]),
                "clip_fraction": float(ppo_metrics["clip_fraction"]),
                "global_step": int(global_step),
                "update_step": int(ppo_update_step),
            },
            metrics_dir=METRICS_DIR,
        )
        append_agent_log(
            f"[PPO][METRICS] ep={episode}/{totLifeT} reward={ep_reward:.4f} "
            f"policy_loss={ppo_metrics['policy_loss']:.6f} value_loss={ppo_metrics['value_loss']:.6f} "
            f"entropy={ppo_metrics['entropy']:.6f} approx_kl={ppo_metrics['approx_kl']:.6f} "
            f"clip_fraction={ppo_metrics['clip_fraction']:.6f} global_step={global_step} update_step={ppo_update_step}"
        )
        if (
            DET_EVAL_ENABLED
            and b_len > 0
            and b_hei > 0
            and episode > 0
            and (episode % DET_EVAL_EVERY_EPISODES == 0)
            and episode != last_det_eval_ep
        ):
            try:
                det_payload = _run_actor_det_eval_ppo(
                    actor_critic=actor_critic,
                    roster_config=roster_config,
                    b_len=b_len,
                    b_hei=b_hei,
                    n_actions=[int(x) for x in n_actions],
                    n_eval=DET_EVAL_EPISODES,
                    opponent_epsilon=DET_EVAL_OPPONENT_EPSILON,
                )
                det_payload["episode"] = int(episode)
                det_payload["algo"] = "ppo"
                det_payload["eval_tag"] = "train_loop_det"
                det_payload["training_loss"] = float(
                    ppo_metrics["policy_loss"] + PPO_VALUE_COEF * ppo_metrics["value_loss"]
                )
                _save_actor_det_eval_snapshot(run_id=str(run_id), payload=det_payload, metrics_dir=METRICS_DIR)
                last_det_eval_ep = int(episode)
            except Exception as exc:
                append_agent_log(f"[PPO][DET_EVAL][WARN] eval пропущен: {exc}")
        if SAVE_EVERY > 0 and (episode % SAVE_EVERY == 0):
            last_checkpoint = _save_ppo_checkpoint(
                actor_critic=actor_critic,
                optimizer=optimizer,
                episode=episode,
                n_actions=n_actions,
                n_observations=n_observations,
                model=model,
                enemy=enemy,
                env_contract=env_contract,
                lr_scheduler=ppo_lr_scheduler,
            )
            # Снапшот в registry для GUI ("Конкретный агент" / "Последний снапшот").
            try:
                periodic_agent_id = build_agent_id(learner_identity, f"ep{int(episode)}")
                artifact_dir = save_agent_artifact(
                    identity=learner_identity,
                    agent_id=periodic_agent_id,
                    env_contract=env_contract,
                    policy_state_dict=normalize_state_dict(actor_critic.state_dict()),
                    target_state_dict=None,
                    optimizer_state_dict=optimizer.state_dict(),
                    extra_meta={
                        "algo": "ppo",
                        "episode": int(episode),
                        "mode": "train_loop",
                        "legacy_checkpoint_path": str(last_checkpoint).replace("\\", "/") if last_checkpoint else "",
                    },
                )
                append_agent_log(f"[LEAGUE][SAVE][PPO] agent_id={periodic_agent_id} artifact_dir={artifact_dir}")
            except Exception as exc:
                append_agent_log(f"[PPO][SAVE][WARN] не удалось сохранить agent snapshot: {exc}")

    if not last_checkpoint:
        last_checkpoint = _save_ppo_checkpoint(
            actor_critic=actor_critic,
            optimizer=optimizer,
            episode=totLifeT,
            n_actions=n_actions,
            n_observations=n_observations,
            model=model,
            enemy=enemy,
            env_contract=env_contract,
            lr_scheduler=ppo_lr_scheduler,
        )
    # Финальный снапшот в registry (чтобы GUI мог взять latest_snapshot)
    try:
        final_agent_id = build_agent_id(learner_identity, f"final_ep{int(totLifeT)}")
        artifact_dir = save_agent_artifact(
            identity=learner_identity,
            agent_id=final_agent_id,
            env_contract=env_contract,
            policy_state_dict=normalize_state_dict(actor_critic.state_dict()),
            target_state_dict=None,
            optimizer_state_dict=optimizer.state_dict(),
            extra_meta={
                "algo": "ppo",
                "episode": int(totLifeT),
                "mode": "train_loop",
                "legacy_checkpoint_path": str(last_checkpoint).replace("\\", "/") if last_checkpoint else "",
            },
        )
        append_agent_log(f"[LEAGUE][SAVE][PPO] agent_id={final_agent_id} artifact_dir={artifact_dir}")
    except Exception as exc:
        append_agent_log(f"[PPO][SAVE][WARN] финальный agent snapshot не сохранён: {exc}")
    if ep_rows:
        try:
            save_extra_metrics(
                run_id=run_id, ep_rows=ep_rows, metrics_dir=METRICS_DIR, write_legacy_gui_plots=False
            )
            save_heuristic_metrics_snapshot(run_id=run_id, ep_rows=ep_rows, metrics_dir=METRICS_DIR)
            det_gui = save_actor_det_eval_plot(run_id=run_id, metrics_dir=METRICS_DIR)
            ckpt_path_for_json = str(last_checkpoint).replace("\\", "/") if last_checkpoint else ""
            if det_gui:
                _write_det_eval_data_json(
                    run_id=run_id,
                    det_plot_gui_paths=det_gui,
                    model_path=ckpt_path_for_json,
                    metrics_mode="det_eval",
                    extra={"algo": "ppo", "mode": "train_loop"},
                )
            elif ckpt_path_for_json:
                _write_det_eval_data_json(
                    run_id=run_id,
                    det_plot_gui_paths={},
                    model_path=ckpt_path_for_json,
                    metrics_mode="det_eval",
                    extra={"algo": "ppo", "mode": "train_loop", "det_eval_note": "нет точек DET-eval"},
                )
            print("Generated metrics", flush=True)
        except Exception as exc:
            append_agent_log(
                "[PPO][METRICS][WARN] Не удалось сохранить метрики/графики. "
                f"Где: train.py run_ppo_training. Ошибка: {exc}"
            )
    append_agent_log(f"[PPO] Training завершён. Последний checkpoint: {last_checkpoint}")


def run_ppo_training_subproc(env_contexts, totLifeT, n_actions, n_observations, env_contract, ordered_keys):
    if not env_contexts:
        raise RuntimeError("PPO(subproc): пустой список env_contexts.")
    vec_env_count = len(env_contexts)
    len_model = int(env_contexts[0].get("len_model", 0))
    if len_model <= 0:
        raise RuntimeError("PPO(subproc): len_model <= 0 (не удалось определить количество юнитов).")

    actor_critic = make_actor_critic(n_observations, n_actions).to(device)
    optimizer = optim.AdamW(actor_critic.parameters(), lr=PPO_LR, amsgrad=True)
    _patch_optimizer_methods_no_compile(optimizer)
    ppo_lr_scheduler = _build_ppo_lr_scheduler(optimizer, total_steps_hint=int(totLifeT) * 20)
    buffer = PPORolloutBuffer()

    global_step = 0
    ppo_update_step = 0
    entropy_coef = float(PPO_ENTROPY_COEF)
    last_checkpoint = ""
    run_id = str(random.randint(1000000, 9999999))
    model_name = datetime.datetime.now().strftime("%d-%H%M%S")
    metrics_obj = metrics(MODELS_DIR, run_id, model_name)
    ep_rows = []
    last_update_metrics = {"policy_loss": 0.0, "value_loss": 0.0, "entropy": 0.0, "approx_kl": 0.0, "clip_fraction": 0.0}

    episodes_finished = 0
    env_ep_reward = [0.0 for _ in range(vec_env_count)]
    env_ep_len = [0 for _ in range(vec_env_count)]

    ppo_kw = ppo_kwargs_from_env()
    append_agent_log(
        f"[PPO][CONFIG] vec_env_count={vec_env_count} use_subproc=1 rollout_steps={PPO_ROLLOUT_STEPS} "
        f"hidden_size={ppo_kw['hidden_size']} num_layers={ppo_kw['num_layers']} "
        f"n_value_ensemble={ppo_kw['n_value_ensemble']} lr_scheduler={PPO_LR_SCHEDULER}"
    )
    print(f"[PPO][CONFIG] vec_env_count={vec_env_count} use_subproc=1", flush=True)

    # В subproc у нас нет доступа к env.action_space, поэтому делаем "быстрый" контракт масок:
    # - shoot_mask приходит по IPC (если включено TRAIN_IPC_INCLUDE_MASKS=1)
    # - остальные головы = all_true.
    while episodes_finished < int(totLifeT):
        obs_batch = []
        shoot_masks = []
        for ctx in env_contexts:
            obs_batch.append(np.asarray(ctx["state"], dtype=np.float32))
            shoot_masks.append(ctx.get("shoot_mask"))

        obs_t = torch.tensor(np.stack(obs_batch, axis=0), dtype=torch.float32, device=device)

        masks_by_head = []
        for head_idx, head_size in enumerate(n_actions):
            mask = torch.ones((vec_env_count, int(head_size)), dtype=torch.bool, device=device)
            if head_idx == 2:
                for i in range(vec_env_count):
                    sm = shoot_masks[i]
                    if sm is None:
                        continue
                    sm_t = torch.as_tensor(sm, dtype=torch.bool, device=device).view(-1)
                    if sm_t.numel() == mask.shape[1] and bool(sm_t.any()):
                        mask[i] = sm_t
            masks_by_head.append(mask)

        # enemy_turn синхронно (до model step)
        for ctx in env_contexts:
            ctx["conn"].send(("enemy_turn", None))
        for ctx in env_contexts:
            _ = ctx["conn"].recv()

        action_t, logprob_t, value_t = actor_critic.act(obs_t, masks_by_head=masks_by_head, deterministic=False)
        action_np = action_t.detach().cpu().numpy()
        logprob_np = logprob_t.detach().cpu().numpy()
        value_np = value_t.detach().cpu().numpy()

        # step синхронно
        for env_idx, ctx in enumerate(env_contexts):
            action_row = action_np[env_idx]
            action_dict = convertToDict(torch.tensor([action_row], device="cpu"))
            for i_u in range(int(ctx["len_model"])):
                key = f"move_num_{i_u}"
                action_dict[key] = int(action_row[6 + i_u])
            ctx["conn"].send(("step", action_dict))

        for env_idx, ctx in enumerate(env_contexts):
            next_obs, reward, done, _, info, next_mask = ctx["conn"].recv()

            # сохраняем transition
            masks_cpu = []
            for head_idx, head_size in enumerate(n_actions):
                if head_idx == 2 and ctx.get("shoot_mask") is not None:
                    masks_cpu.append(np.asarray(ctx["shoot_mask"], dtype=np.bool_))
                else:
                    masks_cpu.append(np.ones(int(head_size), dtype=np.bool_))
            buffer.add(
                obs=np.asarray(ctx["state"], dtype=np.float32),
                action=action_np[env_idx],
                logprob=float(logprob_np[env_idx]),
                reward=float(reward),
                done=bool(done),
                value=float(value_np[env_idx]),
                masks_by_head=masks_cpu,
                env_id=int(env_idx),
            )

            ctx["state"] = next_obs
            ctx["info"] = info
            ctx["shoot_mask"] = next_mask
            env_ep_reward[env_idx] += float(reward)
            env_ep_len[env_idx] += 1
            global_step += 1

            if bool(done):
                episodes_finished += 1
                ep_reward = float(env_ep_reward[env_idx])
                ep_len = int(env_ep_len[env_idx])
                final_info = info or {}

                # GUI прогресс читает stdout и парсит шаблон ep=X/Y.
                print(f"[PPO] ep={episodes_finished}/{totLifeT} done", flush=True)

                model_vp = float(final_info.get("model VP", 0.0) or 0.0)
                player_vp = float(final_info.get("player VP", 0.0) or 0.0)
                vp_diff = model_vp - player_vp
                end_reason = str(final_info.get("end reason", "unknown") or "unknown")
                winner_raw = str(final_info.get("winner", "draw")).strip().lower()
                if end_reason == "wipeout_enemy":
                    result = "win"
                elif end_reason == "wipeout_model":
                    result = "loss"
                elif str(end_reason).startswith("turn_limit"):
                    if vp_diff > 0:
                        result = "win"
                    elif vp_diff < 0:
                        result = "loss"
                    else:
                        result = "draw"
                elif winner_raw in {"model", "learner", "ai"}:
                    result = "win"
                elif winner_raw in {"enemy", "player", "opponent"}:
                    result = "loss"
                elif vp_diff > 0:
                    result = "win"
                elif vp_diff < 0:
                    result = "loss"
                else:
                    result = "draw"
                episode_row = {
                    "episode": int(episodes_finished),
                    "ep_reward": float(ep_reward),
                    "ep_len": int(ep_len),
                    "turn": int(final_info.get("turn", ep_len) or ep_len),
                    "model_vp": float(model_vp),
                    "player_vp": float(player_vp),
                    "vp_diff": float(vp_diff),
                    "result": result,
                    "end_reason": end_reason,
                    "end_code": str(final_info.get("end code", end_reason)),
                }
                ep_rows.append(episode_row)
                metrics_obj.updateRew(ep_reward)
                metrics_obj.updateEpLen(ep_len)

                # сброс счётчиков эпизода этого env
                env_ep_reward[env_idx] = 0.0
                env_ep_len[env_idx] = 0

                append_episode_diagnostics(
                    run_id=run_id,
                    episode_row=episode_row,
                    diagnostics={
                        "algo": "ppo",
                        "policy_loss": float(last_update_metrics.get("policy_loss", 0.0)),
                        "value_loss": float(last_update_metrics.get("value_loss", 0.0)),
                        "entropy": float(last_update_metrics.get("entropy", 0.0)),
                        "approx_kl": float(last_update_metrics.get("approx_kl", 0.0)),
                        "clip_fraction": float(last_update_metrics.get("clip_fraction", 0.0)),
                        "global_step": int(global_step),
                        "update_step": int(ppo_update_step),
                    },
                    metrics_dir=METRICS_DIR,
                )

                # reset env сразу после done
                ctx["conn"].send(("reset", None))
                state, info0, mask0 = ctx["conn"].recv()
                ctx["state"] = state
                ctx["info"] = info0
                ctx["shoot_mask"] = mask0

                if SAVE_EVERY > 0 and (episodes_finished % SAVE_EVERY == 0):
                    last_checkpoint = _save_ppo_checkpoint(
                        actor_critic=actor_critic,
                        optimizer=optimizer,
                        episode=episodes_finished,
                        n_actions=n_actions,
                        n_observations=n_observations,
                        model=None,
                        enemy=None,
                        env_contract=env_contract,
                        lr_scheduler=ppo_lr_scheduler,
                    )

        # Обновляем PPO по порогу шагов роллаута.
        if len(buffer) >= max(1, int(PPO_ROLLOUT_STEPS)):
            batch = buffer.to_tensors(device=device, gamma=PPO_GAMMA, gae_lambda=PPO_GAE_LAMBDA, normalize_adv=True)
            if int(batch.obs.shape[0]) > 0:
                ppo_metrics, entropy_coef, updates = _run_ppo_update_loop(
                    actor_critic,
                    optimizer,
                    batch,
                    entropy_coef=entropy_coef,
                    lr_scheduler=ppo_lr_scheduler,
                )
                ppo_update_step += int(updates)
                last_update_metrics = dict(ppo_metrics)
                append_agent_log(
                    f"[PPO][UPDATE] policy_loss={ppo_metrics['policy_loss']:.6f} value_loss={ppo_metrics['value_loss']:.6f} "
                    f"entropy={ppo_metrics['entropy']:.6f} approx_kl={ppo_metrics['approx_kl']:.6f} "
                    f"clip_fraction={ppo_metrics['clip_fraction']:.6f} global_step={global_step} update_step={ppo_update_step}"
                )
                metrics_obj.updateLoss(ppo_metrics["policy_loss"] + PPO_VALUE_COEF * ppo_metrics["value_loss"])
            buffer.clear()

    # Финальный чекпойнт
    if not last_checkpoint:
        last_checkpoint = _save_ppo_checkpoint(
            actor_critic=actor_critic,
            optimizer=optimizer,
            episode=episodes_finished,
            n_actions=n_actions,
            n_observations=n_observations,
            model=None,
            enemy=None,
            env_contract=env_contract,
            lr_scheduler=ppo_lr_scheduler,
        )

    if ep_rows:
        try:
            save_extra_metrics(
                run_id=run_id, ep_rows=ep_rows, metrics_dir=METRICS_DIR, write_legacy_gui_plots=False
            )
            save_heuristic_metrics_snapshot(run_id=run_id, ep_rows=ep_rows, metrics_dir=METRICS_DIR)
            det_gui = save_actor_det_eval_plot(run_id=run_id, metrics_dir=METRICS_DIR)
            ckpt_path_for_json = str(last_checkpoint).replace("\\", "/") if last_checkpoint else ""
            if det_gui:
                _write_det_eval_data_json(
                    run_id=run_id,
                    det_plot_gui_paths=det_gui,
                    model_path=ckpt_path_for_json,
                    metrics_mode="det_eval",
                    extra={"algo": "ppo", "mode": "train_loop_subproc"},
                )
            elif ckpt_path_for_json:
                _write_det_eval_data_json(
                    run_id=run_id,
                    det_plot_gui_paths={},
                    model_path=ckpt_path_for_json,
                    metrics_mode="det_eval",
                    extra={"algo": "ppo", "mode": "train_loop_subproc", "det_eval_note": "нет точек DET-eval"},
                )
            print("Generated metrics", flush=True)
        except Exception as exc:
            append_agent_log(
                "[PPO][METRICS][WARN] Не удалось сохранить метрики/графики. "
                f"Где: train.py run_ppo_training_subproc. Ошибка: {exc}"
            )
    append_agent_log(f"[PPO] Training(subproc) завершён. Последний checkpoint: {last_checkpoint}")


def main():
    global USE_SUBPROC_ENVS
    print("\nTraining...\n")
    # Route env/runtime logs (phase-by-phase from warhamEnv) to the same train agent log file.
    # Otherwise they fall back to default response log, and LOGS_FOR_AGENTS_TRAIN.md shows only compact lines.
    set_active_io(ConsoleIO(log_path=str(AGENT_TRAIN_LOG_PATH)))
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

    use_pro_actor_learner = os.getenv("PRO_ACTOR_LEARNER", "1").strip() == "1"
    if TRAIN_LOG_TO_CONSOLE:
        print(f"[TRAIN][MODE] PRO_ACTOR_LEARNER={int(use_pro_actor_learner)}")
        print(f"[TRAIN][MODE] TRAIN_ALGO={TRAIN_ALGO}")

    # PRO actor-learner по умолчанию (для DQN и PPO).
    # Для отката на старый pipeline: PRO_ACTOR_LEARNER=0.
    if use_pro_actor_learner:
        if is_az_algo(TRAIN_ALGO):
            if TRAIN_LOG_TO_CONSOLE:
                print(f"[TRAIN][MODE] PRO_ACTOR_LEARNER=1 (AlphaZero {TRAIN_ALGO} MCTS={AZ_MCTS_MODE} + learner)")
            _main_actor_learner_alphazero(
                roster_config=roster_config,
                totLifeT=totLifeT,
                clip_reward_enabled=clip_reward_enabled,
                clip_reward_min=clip_reward_min,
                clip_reward_max=clip_reward_max,
            )
            return
        if TRAIN_ALGO == "ppo":
            if TRAIN_LOG_TO_CONSOLE:
                print("[TRAIN][MODE] PRO_ACTOR_LEARNER=1 (PPO actors CPU + learner GPU)")
            _main_actor_learner_ppo(
                roster_config=roster_config,
                totLifeT=totLifeT,
                clip_reward_enabled=clip_reward_enabled,
                clip_reward_min=clip_reward_min,
                clip_reward_max=clip_reward_max,
            )
            return
        if TRAIN_ALGO == "gumbel_muzero":
            if TRAIN_LOG_TO_CONSOLE:
                if GMZ_INFERENCE_SERVER_ENABLED:
                    _gmz_actor_mode = (
                        f"inference_server + {GMZ_ACTOR_EFFECTIVE_NUM_ACTORS} env workers"
                    )
                elif GMZ_INFERENCE_SERVER_USING_FALLBACK:
                    _gmz_actor_mode = (
                        f"variant A CPU fallback (IS недоступен, actors={GMZ_ACTOR_EFFECTIVE_NUM_ACTORS})"
                    )
                elif GMZ_ACTOR_DEVICE_CUDA:
                    _gmz_actor_mode = f"CUDA (max {GMZ_ACTOR_MAX_CUDA})"
                else:
                    _gmz_actor_mode = "CPU"
                if GMZ_ACTOR_USING_CUDA_FALLBACK:
                    _gmz_actor_mode = f"CPU fallback (запрошен cuda, num_actors={GMZ_ACTOR_EFFECTIVE_NUM_ACTORS})"
                print(
                    f"[TRAIN][MODE] PRO_ACTOR_LEARNER=1 "
                    f"(Gumbel MuZero {_gmz_actor_mode} + learner GPU)"
                )
            _main_actor_learner_gumbel_muzero(
                roster_config=roster_config,
                totLifeT=totLifeT,
                clip_reward_enabled=clip_reward_enabled,
                clip_reward_min=clip_reward_min,
                clip_reward_max=clip_reward_max,
            )
            return
        if TRAIN_ALGO == "dqn":
            if TRAIN_LOG_TO_CONSOLE:
                print("[TRAIN][MODE] PRO_ACTOR_LEARNER=1 (DQN actors CPU + learner GPU)")
            _main_actor_learner(
                roster_config=roster_config,
                totLifeT=totLifeT,
                clip_reward_enabled=clip_reward_enabled,
                clip_reward_min=clip_reward_min,
                clip_reward_max=clip_reward_max,
            )
            return
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
    
    # PPO теперь поддерживает subprocess env (USE_SUBPROC_ENVS=1).
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
            f"Noisy=1 sigma0={NOISY_SIGMA0:.3f} "
            f"IQN=1 n_quant={IQN_N_QUANTILES} n_tgt={IQN_N_TARGET_QUANTILES} n_tau={IQN_N_TAU_SAMPLES} embed={IQN_EMBED_DIM} kappa={IQN_KAPPA:.3f} "
            f"NOISY_DISABLE_EPS={int(NOISY_DISABLE_EPS)} "
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
                    "shoot_mask": init_payload.get("shoot_mask"),
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

    if TRAIN_ALGO == "distill":
        append_agent_log("[DISTILL] Запуск режима дистилляции teacher→DQN student")
        _run_dqn_distill_mode(
            n_observations,
            n_actions,
            steps=int(os.getenv("DISTILL_STEPS", "200")),
        )
        return

    if is_az_algo(TRAIN_ALGO):
        append_agent_log(f"[AZ] Запуск AlphaZero ветки algo={TRAIN_ALGO} mcts_mode={AZ_MCTS_MODE}. episodes={totLifeT}")
        _main_actor_learner_alphazero(
            roster_config=roster_config,
            totLifeT=totLifeT,
            clip_reward_enabled=clip_reward_enabled,
            clip_reward_min=clip_reward_min,
            clip_reward_max=clip_reward_max,
        )
        _cleanup_train_envs(env_contexts=env_contexts, subproc_envs=subproc_envs, use_subproc=USE_SUBPROC_ENVS)
        return

    if TRAIN_ALGO == "gumbel_muzero":
        append_agent_log(f"[GMZ] Запуск Gumbel MuZero ветки. episodes={totLifeT}")
        _main_actor_learner_gumbel_muzero(
            roster_config=roster_config,
            totLifeT=totLifeT,
            clip_reward_enabled=clip_reward_enabled,
            clip_reward_min=clip_reward_min,
            clip_reward_max=clip_reward_max,
        )
        _cleanup_train_envs(env_contexts=env_contexts, subproc_envs=subproc_envs, use_subproc=USE_SUBPROC_ENVS)
        return

    if TRAIN_ALGO == "ppo":
        append_agent_log(
            f"[PPO] Запуск PPO ветки. episodes={totLifeT} vec_env_count={vec_env_count} "
            f"rollout_steps={PPO_ROLLOUT_STEPS} update_epochs={PPO_UPDATE_EPOCHS} minibatch={PPO_MINIBATCH_SIZE}"
        )
        if USE_SUBPROC_ENVS:
            run_ppo_training_subproc(
                env_contexts=env_contexts,
                totLifeT=totLifeT,
                n_actions=n_actions,
                n_observations=n_observations,
                env_contract=env_contract,
                ordered_keys=ordered_keys,
            )
        else:
            run_ppo_training(
                env_contexts=env_contexts,
                totLifeT=totLifeT,
                n_actions=n_actions,
                n_observations=n_observations,
                env_contract=env_contract,
                model=model,
                enemy=enemy,
                roster_config=roster_config,
                learner_identity=learner_identity,
            )
        _cleanup_train_envs(env_contexts=env_contexts, subproc_envs=subproc_envs, use_subproc=USE_SUBPROC_ENVS)
        with IO_PROFILER.timed("metrics save"):
            IO_PROFILER.write_snapshot()
        _flush_agent_log_buffer(force=True)
        if os.path.isfile(str(TRAIN_DATA_PATH)):
            initFile.delFile()
        return
    
    if USE_COMPILE and torch.cuda.is_available():
        torch.backends.cudnn.benchmark = True
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        try:
            torch.set_float32_matmul_precision("high")
        except Exception:
            pass
    
    
    policy_net = _make_dqn(n_observations, n_actions).to(device)
    target_net = _make_dqn(n_observations, n_actions).to(device)
    optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
    if os.getenv("TORCH_OPTIMIZER_NO_DYNAMO", "1") == "1":
        _patch_optimizer_methods_no_compile(optimizer)
    lr_scheduler = _build_dqn_lr_scheduler(optimizer, total_steps_hint=int(totLifeT) * 500)

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

    if lr_scheduler is not None and isinstance(resume_meta.get("lr_scheduler_state"), dict):
        try:
            lr_scheduler.load_state_dict(resume_meta["lr_scheduler_state"])
        except Exception as exc:
            warn_msg = (
                "[RESUME][WARN] Не удалось загрузить lr_scheduler state. "
                f"Где: train.py (lr_scheduler.load_state_dict). Детали: {exc}"
            )
            print(warn_msg)
            append_agent_log(warn_msg)

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
        # PPO vs PPO / DQN vs DQN: периодические snapshot-обновления оппонента с learner.
        # PPO vs DQN / DQN vs PPO: веса оппонента фиксированы (без подмены state_dict другого algo).
        opponent_snapshot_sync_enabled = True
        opponent_policy_net = _make_dqn(n_observations, n_actions).to(device)
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
            try:
                _opp_sp = load_agent_opponent(agent_id=selected_id, expected_contract=env_contract)
                opponent_snapshot_sync_enabled = str(_opp_sp.algo).lower() == str(TRAIN_ALGO).lower()
            except Exception:
                pass
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

    if SELF_PLAY_ENABLED:
        opp_source = str(opponent_source_state.get("source", "unknown"))
        opp_id = str(opponent_source_state.get("id"))
        opp_type, opp_agent_id_text = _opponent_type_label(
            opponent_policy_net=opponent_policy_net,
            opponent_source_state=opponent_source_state,
            self_play_enabled=True,
        )
        enemy_policy_mode = "snapshot_policy_fn" if opponent_policy_net is not None else "heuristic_auto"
        _log_train(
            "[SELFPLAY][CONFIG] "
            f"enabled=1 mode={SELF_PLAY_OPPONENT_MODE} "
            f"learner_algo={TRAIN_ALGO} opponent_snapshot_sync={int(opponent_snapshot_sync_enabled)} "
            f"opponent_source={opp_source} opponent_id={opp_id} "
            f"opponent_type={opp_type} opponent_agent_id={opp_agent_id_text} "
            f"enemy_policy_mode={enemy_policy_mode}"
        )
    
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
            ctx["state"], ctx["info"], ctx["shoot_mask"] = ctx["conn"].recv()
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
    algo_tag = str(TRAIN_ALGO or "dqn").strip().lower()
    if algo_tag not in {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero"}:
        algo_tag = "dqn"
    models_root = os.path.join(MODELS_DIR, algo_tag)
    fold = os.path.join(models_root, safe_name)
    fileName = os.path.join(fold, "model-" + date + ".pickle")
    randNum = np.random.randint(0, 10000000)
    metrics_obj = metrics(fold, randNum, date)
    ep_rows = []
    # Последний известный train loss (для DET-eval снимка; optimize идёт после шага env).
    last_known_training_loss: float | None = None
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
        model_vp_sum = 0.0
        enemy_vp_sum = 0.0
        hp_diff_sum = 0.0
        kill_diff_sum = 0.0
        reward_sum_total = 0.0
        steps_sum_total = 0.0
        def _sum_health(value) -> float:
            try:
                if isinstance(value, (list, tuple, np.ndarray)):
                    return float(sum(float(x) for x in value))
                return float(value or 0.0)
            except Exception:
                return 0.0

        def _sum_alive_models(value) -> int:
            try:
                if isinstance(value, (list, tuple, np.ndarray)):
                    return int(sum(int(x) for x in value))
                return int(value or 0)
            except Exception:
                return 0
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
            model_alive_start = _sum_alive_models((info_eval or {}).get("model alive models", []))
            enemy_alive_start = _sum_alive_models((info_eval or {}).get("player alive models", []))
            done_eval = False
            step_guard = 0
            ep_reward_sum = 0.0
            while not done_eval and step_guard < 10000:
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
                ep_reward_sum += float(_reward_eval or 0.0)
                state_eval = next_state_eval
            reward_sum_total += ep_reward_sum
            steps_sum_total += float(step_guard)
            end_reason_eval = info_eval.get("end reason", "")
            model_vp_eval = int(info_eval.get("model VP", 0))
            enemy_vp_eval = int(info_eval.get("player VP", 0))
            vp_diff_eval = model_vp_eval - enemy_vp_eval
            vp_diff_sum += float(vp_diff_eval)
            model_vp_sum += float(model_vp_eval)
            enemy_vp_sum += float(enemy_vp_eval)
            model_hp_end = _sum_health((info_eval or {}).get("model health", []))
            enemy_hp_end = _sum_health((info_eval or {}).get("player health", []))
            hp_diff_sum += float(model_hp_end - enemy_hp_end)
            model_alive_end = _sum_alive_models((info_eval or {}).get("model alive models", []))
            enemy_alive_end = _sum_alive_models((info_eval or {}).get("player alive models", []))
            kills_by_model = enemy_alive_start - enemy_alive_end
            kills_by_enemy = model_alive_start - model_alive_end
            kill_diff_sum += float(kills_by_model - kills_by_enemy)

            try:
                append_agent_log(
                    "[DET][DEBUG] "
                    f"kind=dqn_train_loop_det "
                    f"idx={eval_i+1}/{DET_EVAL_EPISODES} "
                    f"end_reason={end_reason_eval} "
                    f"model_vp={model_vp_eval} "
                    f"player_vp={enemy_vp_eval} "
                    f"vp_diff={vp_diff_eval}"
                )
            except Exception:
                pass

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
        reward_mean = float(reward_sum_total / n_eval)
        ep_len_mean = float(steps_sum_total / n_eval)
        eval_det_line = (
            "[EVAL][DET] "
            f"episode={total_episode} "
            f"eval_episodes={n_eval} "
            f"win_rate={wins/n_eval:.3f} "
            f"draw_rate={draws/n_eval:.3f} "
            f"turn_limit_rate={turn_limit/n_eval:.3f} "
            f"wipeout_enemy_rate={wipeout_enemy/n_eval:.3f} "
            f"wipeout_model_rate={wipeout_model/n_eval:.3f} "
            f"vp_diff_mean={vp_diff_sum/n_eval:.3f} "
            f"reward_mean={reward_mean:.3f} "
            f"ep_len_mean={ep_len_mean:.3f}"
        )
        append_agent_log(eval_det_line)
        det_payload = {
            "episode": int(total_episode),
            "algo": "dqn",
            "eval_episodes": int(n_eval),
            "win_rate": float(wins / n_eval),
            "draw_rate": float(draws / n_eval),
            "turn_limit_rate": float(turn_limit / n_eval),
            "wipeout_enemy_rate": float(wipeout_enemy / n_eval),
            "wipeout_model_rate": float(wipeout_model / n_eval),
            "vp_diff_mean": float(vp_diff_sum / n_eval),
            "model_vp_mean": float(model_vp_sum / n_eval),
            "enemy_vp_mean": float(enemy_vp_sum / n_eval),
            "hp_diff_mean": float(hp_diff_sum / n_eval),
            "kill_diff_mean": float(kill_diff_sum / n_eval),
            "reward_mean": reward_mean,
            "ep_len_mean": ep_len_mean,
            "eval_tag": ("train_loop_det_selfplay" if (SELF_PLAY_ENABLED and opponent_policy_net is not None) else "train_loop_det"),
        }
        if last_known_training_loss is not None:
            det_payload["training_loss"] = float(last_known_training_loss)
        try:
            _save_actor_det_eval_snapshot(run_id=str(randNum), payload=det_payload, metrics_dir=METRICS_DIR)
        except Exception as exc:
            append_agent_log(f"[EVAL][DET][WARN] не удалось записать JSONL: {exc}")

    _apply_reward_schedule(resume_episode_base + numLifeT)
    
    while end is False:
        if USE_SUBPROC_ENVS:
            shoot_masks = [ctx.get("shoot_mask") for ctx in env_contexts]
        else:
            shoot_masks = []
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
                if SELF_PLAY_ENABLED and opponent_policy_net is not None:
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
        if USE_SUBPROC_ENVS:
            # Batched IPC: сначала отправляем step всем env, затем собираем ответы.
            step_start = time.perf_counter()
            for idx, ctx in enumerate(env_contexts):
                ctx["conn"].send(("step", action_dicts[idx]))
            for idx, ctx in enumerate(env_contexts):
                step_results[idx] = ctx["conn"].recv()
            perf_stats["env_step_s"] += time.perf_counter() - step_start
            perf_counts["env_steps"] += len(env_contexts)

        for idx, ctx in enumerate(env_contexts):
            step_start = time.perf_counter()
            if USE_SUBPROC_ENVS:
                next_observation, reward, done, res, info, next_shoot_mask = step_results[idx]
                ctx["shoot_mask"] = next_shoot_mask
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
            if not USE_SUBPROC_ENVS:
                next_shoot_mask = None
            if not done:
                next_state_t = torch.tensor(to_np_state(next_observation), device=dev).unsqueeze(0)
                mask_log_fn = append_agent_log if idx == 0 else None
                if USE_SUBPROC_ENVS:
                    # маска уже пришла вместе с step()
                    pass
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

            # ---- timeline по battle round (для анализа draw) ----
            # Сохраняем 1 снапшот на battle round (последний увиденный в раунде).
            try:
                if isinstance(info, dict):
                    if ctx.get("ep_model_hp_start") is None:
                        mh0 = info.get("model health", [])
                        ph0 = info.get("player health", [])
                        ctx["ep_model_hp_start"] = float(sum(mh0)) if isinstance(mh0, (list, tuple, np.ndarray)) else float(mh0 or 0.0)
                        ctx["ep_enemy_hp_start"] = float(sum(ph0)) if isinstance(ph0, (list, tuple, np.ndarray)) else float(ph0 or 0.0)

                    if os.getenv("METRICS_SAVE_ROUND_TIMELINE", "1") == "1":
                        br = int(info.get("battle round", 0) or 0)
                        if br > 0:
                            mh_now = info.get("model health", [])
                            ph_now = info.get("player health", [])
                            mh_sum = float(sum(mh_now)) if isinstance(mh_now, (list, tuple, np.ndarray)) else float(mh_now or 0.0)
                            ph_sum = float(sum(ph_now)) if isinstance(ph_now, (list, tuple, np.ndarray)) else float(ph_now or 0.0)
                            snap = {
                                "battle_round": br,
                                "turn": int(info.get("turn", 0) or 0),
                                "model_vp": int(info.get("model VP", 0) or 0),
                                "enemy_vp": int(info.get("player VP", 0) or 0),
                                "model_hp": mh_sum,
                                "enemy_hp": ph_sum,
                                "model_ctrl_n": int(len(info.get("model controlled objectives", []) or [])),
                                "enemy_ctrl_n": int(len(info.get("player controlled objectives", []) or [])),
                            }
                            # Перезаписываем снапшот данного BR (чтобы был "последний" за раунд).
                            timeline = ctx.get("round_timeline")
                            if not isinstance(timeline, list):
                                timeline = []
                            replaced = False
                            for i in range(len(timeline)):
                                if int(timeline[i].get("battle_round", -1)) == br:
                                    timeline[i] = snap
                                    replaced = True
                                    break
                            if not replaced:
                                timeline.append(snap)
                            ctx["round_timeline"] = timeline
            except Exception:
                pass
    
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

                # ---- расширенные диагностические метрики (для анализа draw) ----
                battle_round = int(info.get("battle round", 0) or 0)
                model_ctrl = info.get("model controlled objectives", []) if isinstance(info, dict) else []
                enemy_ctrl = info.get("player controlled objectives", []) if isinstance(info, dict) else []
                try:
                    model_ctrl_n = int(len(model_ctrl)) if isinstance(model_ctrl, (list, tuple)) else 0
                except Exception:
                    model_ctrl_n = 0
                try:
                    enemy_ctrl_n = int(len(enemy_ctrl)) if isinstance(enemy_ctrl, (list, tuple)) else 0
                except Exception:
                    enemy_ctrl_n = 0

                # damage_dealt/taken по эпизоду считаем по суммарным HP
                # (без детализации по оружию/фазам, зато дешево и всегда доступно).
                ep_model_hp_start = float(ctx.get("ep_model_hp_start", mh))
                ep_enemy_hp_start = float(ctx.get("ep_enemy_hp_start", ph))
                damage_taken_total = max(0.0, ep_model_hp_start - float(mh))
                damage_dealt_total = max(0.0, ep_enemy_hp_start - float(ph))
    
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
                        best_path = os.path.join(models_root, safe_name, "best_eval_checkpoint.pth")
                        os.makedirs(os.path.join(models_root, safe_name), exist_ok=True)
                        with IO_PROFILER.timed("checkpoint save"):
                            best_ckpt = {
                                "policy_net": policy_net.state_dict(),
                                "net_type": NET_TYPE,
                                "algo": "dqn",
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
                            }
                            best_ckpt.update(_dqn_checkpoint_extra(policy_net, target_net, optimizer, lr_scheduler))
                            torch.save(best_ckpt, best_path)
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

                # Пишем "супер-подробную" диагностику по эпизоду (JSONL).
                try:
                    # Последняя строка ep_rows — это row текущего эпизода.
                    episode_row = ep_rows[-1] if ep_rows else {}
                    timeline_enabled = os.getenv("METRICS_SAVE_ROUND_TIMELINE", "1") == "1"
                    timeline = ctx.get("round_timeline", []) if timeline_enabled else []
                    append_episode_diagnostics(
                        run_id=str(randNum),
                        episode_row=episode_row,
                        diagnostics={
                            "battle_round": battle_round,
                            "model_hp_total": mh,
                            "enemy_hp_total": ph,
                            "damage_dealt_total": float(damage_dealt_total),
                            "damage_taken_total": float(damage_taken_total),
                            "model_ctrl": list(model_ctrl) if isinstance(model_ctrl, (list, tuple)) else [],
                            "enemy_ctrl": list(enemy_ctrl) if isinstance(enemy_ctrl, (list, tuple)) else [],
                            "model_ctrl_n": int(model_ctrl_n),
                            "enemy_ctrl_n": int(enemy_ctrl_n),
                            "timeline": timeline,
                            "winner_env": winner_env,
                            "end_reason_env": end_reason_env,
                        },
                        metrics_dir=METRICS_DIR,
                    )
                except Exception as exc:
                    if TRAIN_LOG_TO_FILE:
                        append_agent_log(f"[METRICS][WARN] append_episode_diagnostics failed: {exc}")
                    if TRAIN_LOG_TO_CONSOLE:
                        print(f"[METRICS][WARN] append_episode_diagnostics failed: {exc}")
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
                # сброс накопителей таймлайна/стартовых HP для следующего эпизода
                ctx["round_timeline"] = []
                ctx["ep_model_hp_start"] = None
                ctx["ep_enemy_hp_start"] = None
                if SAVE_EVERY > 0 and total_episode % SAVE_EVERY == 0:
                    checkpoint_path = os.path.join(models_root, safe_name, f"checkpoint_ep{total_episode}.pth")
                    os.makedirs(os.path.join(models_root, safe_name), exist_ok=True)
                    with IO_PROFILER.timed("checkpoint save"):
                        ckpt_payload = {
                            "policy_net": policy_net.state_dict(),
                            "net_type": NET_TYPE,
                            "algo": "dqn",
                            "optimizer": optimizer.state_dict(),
                            "global_step": int(global_step),
                            "optimize_steps": int(optimize_steps),
                            "episode": int(total_episode),
                            "replay_memory": memory.state_dict(),
                        }
                        ckpt_payload.update(_dqn_checkpoint_extra(policy_net, target_net, optimizer, lr_scheduler))
                        torch.save(ckpt_payload, checkpoint_path)
                    periodic_agent_id = build_agent_id(learner_identity, f"ep{total_episode}")
                    save_agent_artifact(
                        identity=learner_identity,
                        agent_id=periodic_agent_id,
                        env_contract=env_contract,
                        policy_state_dict=normalize_state_dict(policy_net.state_dict()),
                        target_state_dict=normalize_state_dict(target_net.state_dict()),
                        optimizer_state_dict=optimizer.state_dict(),
                        extra_meta={
                            "algo": "dqn",
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

                if (
                    SELF_PLAY_ENABLED
                    and SELF_PLAY_OPPONENT_MODE == "snapshot"
                    and opponent_snapshot_sync_enabled
                ):
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
                    ctx["state"], ctx["info"], ctx["shoot_mask"] = ctx["conn"].recv()
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
                    last_known_training_loss = float(last_loss_value)
                    optimize_steps += 1
                    if lr_scheduler is not None:
                        if DQN_LR_SCHEDULER == "plateau":
                            lr_scheduler.step(float(result["loss"]))
                        else:
                            lr_scheduler.step()
                    perf_counts["updates"] += 1
                    timing = result.get("timing", {})
                    perf_stats["replay_sample_s"] += float(timing.get("sample_s", 0.0))
                    perf_stats["train_forward_s"] += float(timing.get("forward_s", 0.0))
                    perf_stats["train_backward_s"] += float(timing.get("backward_s", 0.0))
                    if TRAIN_LOG_ENABLED and optimize_steps % TRAIN_LOG_EVERY_UPDATES == 0:
                        current_lr = float(optimizer.param_groups[0]["lr"])
                        noisy_sigma_mean = float(policy_net.mean_noisy_sigma()) if hasattr(policy_net, "mean_noisy_sigma") else 0.0
                        train_line = (
                            "[TRAIN] "
                            f"ep={numLifeT + 1} "
                            f"upd={optimize_steps} "
                            f"step={global_step} "
                            f"loss={last_loss_value:.6f} "
                            f"eps={eps_threshold:.4f} "
                            f"lr={current_lr:.6g} "
                            f"gamma={GAMMA:.6g} "
                            f"PER={int(PER_ENABLED)} "
                            f"alpha={PER_ALPHA:.4g} "
                            f"beta={last_per_beta:.4g} "
                            f"N_STEP={N_STEP} "
                            f"Noisy=1 sigma0={NOISY_SIGMA0:.3f} sigma_mean={noisy_sigma_mean:.4f} "
                            f"hidden={DQN_HIDDEN_SIZE} layers={DQN_NUM_LAYERS} ensemble={DQN_ENSEMBLE_SIZE} "
                            f"IQN=1 n_quant={IQN_N_QUANTILES} n_tgt={IQN_N_TARGET_QUANTILES} n_tau={IQN_N_TAU_SAMPLES} embed={IQN_EMBED_DIM} kappa={IQN_KAPPA:.3f}"
                        )
                        if last_td_stats.get("dist_stats") and "ensemble_std_mean" in last_td_stats["dist_stats"]:
                            train_line += f" q_std={last_td_stats['dist_stats']['ensemble_std_mean']:.6f}"
                        if N_STEP > 1:
                            effective_gamma = GAMMA ** N_STEP
                            train_line += f" effective_gamma={effective_gamma:.6g}"
                        if PER_ENABLED and last_td_stats.get("per_stats"):
                            per_stats = last_td_stats["per_stats"]
                        if last_td_stats.get("dist_stats"):
                            dist_stats = last_td_stats["dist_stats"]
                            if "quantile_loss_mean" in dist_stats:
                                train_line += (
                                    f" qloss_mean={dist_stats['quantile_loss_mean']:.6f}"
                                    f" qloss_max={dist_stats['quantile_loss_max']:.6f}"
                                    f" tdq_mean={dist_stats['td_quantile_mean']:.6f}"
                                    f" tdq_max={dist_stats['td_quantile_max']:.6f}"
                                )
                            else:
                                train_line += (
                                    f" ce_mean={dist_stats.get('ce_mean', 0.0):.6f}"
                                    f" ce_max={dist_stats.get('ce_max', 0.0):.6f}"
                                )
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
                if NOISY_SIGMA_ANNEAL and hasattr(policy_net, "anneal_noisy_sigma"):
                    decay_steps = max(1.0, float(EPS_DECAY))
                    policy_net.anneal_noisy_sigma(min(float(global_step) / decay_steps, 1.0))
    
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

    save_extra_metrics(
        run_id=str(randNum), ep_rows=ep_rows, metrics_dir=METRICS_DIR, write_legacy_gui_plots=False
    )
    heur_metrics_path = save_heuristic_metrics_snapshot(run_id=str(randNum), ep_rows=ep_rows, metrics_dir=METRICS_DIR)
    if heur_metrics_path:
        _log_train(f"[HEUR][METRICS] saved={heur_metrics_path}")

    os.makedirs(fold, exist_ok=True)

    model_rel_path = os.path.join(models_root, safe_name, f"model-{date}.pth")
    with IO_PROFILER.timed("checkpoint save"):
        final_ckpt = {
            "policy_net": policy_net.state_dict(),
            "net_type": NET_TYPE,
            "algo": "dqn",
            "optimizer": optimizer.state_dict(),
            "global_step": int(global_step),
            "optimize_steps": int(optimize_steps),
            "episode": int(resume_episode_base + numLifeT),
            "replay_memory": memory.state_dict(),
        }
        final_ckpt.update(_dqn_checkpoint_extra(policy_net, target_net, optimizer, lr_scheduler))
        torch.save(final_ckpt, model_rel_path)
    with IO_PROFILER.timed("metrics save"):
        det_gui = save_actor_det_eval_plot(run_id=str(randNum), metrics_dir=METRICS_DIR)
        opponent_source = str(opponent_source_state.get("source", "unknown"))
        opponent_id = opponent_source_state.get("id")
        if SELF_PLAY_ENABLED:
            opponent_algo = "dqn" if opponent_policy_net is not None else "heuristic"
        else:
            opponent_algo = "heuristic"
        learner_side = str(learner_identity.side or "P1").strip().upper() or "P1"
        opponent_side = "P2" if learner_side == "P1" else "P1"
        if det_gui:
            _write_det_eval_data_json(
                run_id=str(randNum),
                det_plot_gui_paths=det_gui,
                model_path=model_rel_path.replace("\\", "/"),
                metrics_mode="det_eval",
                extra={
                    "algo": "dqn",
                    "mode": "train_loop",
                    "learner_side": learner_side,
                    "learner_faction": str(learner_identity.faction or "Unknown"),
                    "opponent_side": opponent_side,
                    "opponent_faction": str(roster_config.get("enemy_faction", "Unknown")).strip(),
                    "opponent_algo": opponent_algo,
                    "opponent_source": opponent_source,
                    "opponent_id": str(opponent_id) if opponent_id is not None else "",
                },
            )
        else:
            _write_det_eval_data_json(
                run_id=str(randNum),
                det_plot_gui_paths={},
                model_path=model_rel_path.replace("\\", "/"),
                metrics_mode="det_eval",
                extra={
                    "algo": "dqn",
                    "mode": "train_loop",
                    "det_eval_note": "нет точек DET-eval (DET_EVAL выкл. или ещё не было)",
                    "learner_side": learner_side,
                    "learner_faction": str(learner_identity.faction or "Unknown"),
                    "opponent_side": opponent_side,
                    "opponent_faction": str(roster_config.get("enemy_faction", "Unknown")).strip(),
                    "opponent_algo": opponent_algo,
                    "opponent_source": opponent_source,
                    "opponent_id": str(opponent_id) if opponent_id is not None else "",
                },
            )
    print("Generated metrics")
    final_agent_id = build_agent_id(learner_identity, f"final_ep{resume_episode_base + numLifeT}")
    artifact_dir = save_agent_artifact(
        identity=learner_identity,
        agent_id=final_agent_id,
        env_contract=env_contract,
        policy_state_dict=normalize_state_dict(policy_net.state_dict()),
        target_state_dict=normalize_state_dict(target_net.state_dict()),
        optimizer_state_dict=optimizer.state_dict(),
        extra_meta={
            "algo": "dqn",
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
    model_tag = f"{algo_tag}/{safe_name}/model-{date}"
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
    
    if os.path.isfile(str(TRAIN_DATA_PATH)):
        initFile.delFile()


def _main_actor_learner(*, roster_config, totLifeT, clip_reward_enabled, clip_reward_min, clip_reward_max) -> None:
    """
    Actor-Learner MVP (Windows-friendly, spawn):
    - Actors (CPU) гоняют env и шлют transitions батчами в очередь.
    - Learner (GPU) читает очередь, наполняет replay и делает optimize_model.
    Важно: это отдельный режим, не ломает текущий pipeline (ACTOR_LEARNER=0 по умолчанию).
    """
    num_actors = max(1, int(os.getenv("NUM_ACTORS", "8")))
    batch_send = max(8, int(os.getenv("ACTOR_BATCH_SEND", "32")))
    updates_per_batch = max(1, int(os.getenv("UPDATES_PER_BATCH", "8")))
    queue_max = max(64, int(os.getenv("ACTOR_QUEUE_MAX", "256")))

    b_len = roster_config["b_len"]
    b_hei = roster_config["b_hei"]
    trunc = True

    # 1) Определяем размеры наблюдения и action-space
    enemy0, model0 = _build_units_from_config(roster_config, b_len, b_hei)
    env0 = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy0, model=model0, b_len=b_len, b_hei=b_hei)
    state0, _info0 = env0.reset(options={"m": model0, "e": enemy0, "Type": "big", "trunc": True})
    if isinstance(state0, dict) or "OrderedDict" in str(type(state0)):
        n_observations = len(list(state0.values()))
    else:
        n_observations = int(np.array(state0).shape[0])

    ordered_keys = ["move", "attack", "shoot", "charge", "use_cp", "cp_on"]
    for i_u in range(len(model0)):
        ordered_keys.append(f"move_num_{i_u}")
    n_actions = []
    for k in ordered_keys:
        sp = env0.action_space.spaces[k]
        if hasattr(sp, "n"):
            n_actions.append(int(sp.n))
        elif hasattr(sp, "nvec"):
            n_actions.extend([int(x) for x in sp.nvec])
        else:
            raise TypeError(f"Unsupported action space for {k}: {type(sp)}")
    try:
        env0.close()
    except Exception:
        pass

    # 2) Learner (GPU)
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
            "actor_learner": 1,
            "num_actors": int(num_actors),
        },
    )

    # Self-play opponent snapshot (optional): загружаем один раз в learner и раздаём акторам.
    opponent_spec: OpponentSpec | None = None
    opponent_eps = float(SELF_PLAY_OPPONENT_EPSILON)
    if SELF_PLAY_ENABLED:
        try:
            if SELF_PLAY_OPPONENT_MODE == "fixed_checkpoint" and SELF_PLAY_FIXED_PATH:
                checkpoint = torch.load(SELF_PLAY_FIXED_PATH, map_location="cpu", weights_only=False)
                checkpoint_algo = str(checkpoint.get("algo", "dqn")).strip().lower() if isinstance(checkpoint, dict) else "dqn"
                if checkpoint_algo not in {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero"}:
                    checkpoint_algo = "dqn"
                if isinstance(checkpoint, dict) and "policy_net" in checkpoint:
                    policy_state = normalize_state_dict(checkpoint["policy_net"])
                elif isinstance(checkpoint, dict) and "actor_critic" in checkpoint:
                    policy_state = normalize_state_dict(checkpoint["actor_critic"])
                elif isinstance(checkpoint, dict):
                    policy_state = normalize_state_dict(checkpoint)
                else:
                    policy_state = normalize_state_dict(checkpoint)
                opponent_spec = OpponentSpec(
                    agent_id=str(SELF_PLAY_FIXED_PATH),
                    algo=str(checkpoint_algo),
                    contract=dict(env_contract),
                    policy_state=policy_state,
                )
            else:
                if not OPPONENT_AGENT_ID:
                    raise ValueError("SELF_PLAY: нужен OPPONENT_AGENT_ID (GUI должен подставить последний снапшот).")
                opponent_spec = load_agent_opponent(agent_id=OPPONENT_AGENT_ID, expected_contract=env_contract)
        except Exception as exc:
            warn = f"[SELFPLAY][WARN] Actor-Learner: не удалось загрузить снапшот оппонента, откатываюсь на эвристику. exc={exc}"
            append_agent_log(warn)
            if TRAIN_LOG_TO_CONSOLE:
                print(warn)
            opponent_spec = None
        enemy_policy_mode = "snapshot_policy_fn" if opponent_spec is not None else "heuristic_auto"
        _log_train(
            "[SELFPLAY][CONFIG] "
            f"enabled=1 mode={SELF_PLAY_OPPONENT_MODE} "
            f"opponent_agent_id={OPPONENT_AGENT_ID or '-'} "
            f"enemy_policy_mode={enemy_policy_mode}"
        )
    opponent_source_actor = "snapshot_policy_fn" if (SELF_PLAY_ENABLED and opponent_spec is not None) else "heuristic_auto"
    try:
        opponent_id_actor = str(getattr(opponent_spec, "agent_id", "") or OPPONENT_AGENT_ID or "")
    except Exception:
        opponent_id_actor = str(OPPONENT_AGENT_ID or "")

    policy_net = _make_dqn(n_observations, n_actions).to(device)
    target_net = _make_dqn(n_observations, n_actions).to(device)
    optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
    if os.getenv("TORCH_OPTIMIZER_NO_DYNAMO", "1") == "1":
        _patch_optimizer_methods_no_compile(optimizer)
    lr_scheduler = _build_dqn_lr_scheduler(optimizer, total_steps_hint=int(totLifeT) * 500)

    replay_capacity = int(os.getenv("REPLAY_CAPACITY", "200000"))
    if PER_ENABLED:
        memory = PrioritizedReplayMemory(replay_capacity, alpha=PER_ALPHA, eps=PER_EPS)
    else:
        memory = ReplayMemory(replay_capacity)

    target_net.load_state_dict(normalize_state_dict(policy_net.state_dict()))
    target_net.eval()
    scaler = torch.cuda.amp.GradScaler(enabled=bool(USE_AMP and device.type == "cuda"))

    # Веса для акторов (CPU). MVP: без онлайн-синхронизации, только стартовая копия.
    init_weights = {
        k: v.detach().cpu().clone()
        for k, v in normalize_state_dict(policy_net.state_dict()).items()
    }

    # Online sync (learner -> actors) через файл: Windows-friendly.
    sync_enabled = os.getenv("ACTOR_SYNC_ENABLED", "1") == "1"
    sync_every_updates = max(1, int(os.getenv("ACTOR_SYNC_EVERY_UPDATES", "200")))
    sync_path = os.path.join(MODELS_DIR, "actor_sync", "latest_policy.pth")
    os.makedirs(os.path.dirname(sync_path), exist_ok=True)
    last_sync_opt_steps = 0

    ctx = mp.get_context("spawn")
    data_q: mp.Queue = ctx.Queue(maxsize=queue_max)

    procs = []
    for a_idx in range(num_actors):
        base = int(totLifeT) // int(num_actors)
        rem = int(totLifeT) % int(num_actors)
        episodes = int(base + (1 if a_idx < rem else 0))
        cr_min = 0.0 if clip_reward_min is None else float(clip_reward_min)
        cr_max = 0.0 if clip_reward_max is None else float(clip_reward_max)
        p = ctx.Process(
            target=_actor_learner_actor_entry,
            args=(
                a_idx,
                int(episodes),
                roster_config,
                int(b_len),
                int(b_hei),
                int(n_observations),
                list(n_actions),
                init_weights,
                int(batch_send),
                cr_min,
                cr_max,
                bool(clip_reward_enabled),
                data_q,
                opponent_spec,
                float(opponent_eps),
                int(1 if SELF_PLAY_ENABLED else 0),
            ),
            daemon=True,
        )
        p.start()
        procs.append(p)

    done_actors = 0
    optimize_steps = 0
    global_step = 0
    episodes_finished = 0
    last_actor_det_eval_ep = 0
    last_loss = None
    ep_rows: list[dict] = []
    randNum = random.randint(1000000, 9999999)
    loss_trace: list[float] = []
    adaptive_tl_curriculum = os.getenv("ADAPTIVE_TURN_LIMIT_CURRICULUM", "1").strip() == "1"
    tl_curriculum_hi = float(os.getenv("ADAPTIVE_TL_RATE_HIGH", "0.72"))
    tl_curriculum_lo = float(os.getenv("ADAPTIVE_TL_RATE_LOW", "0.58"))
    tl_penalty_step = float(os.getenv("ADAPTIVE_NO_CONTEST_STEP", "0.01"))
    tl_penalty_max = float(os.getenv("ADAPTIVE_NO_CONTEST_MAX", "0.30"))
    tl_oc_step = float(os.getenv("ADAPTIVE_OC_MARGIN_STEP", "0.003"))
    tl_oc_max = float(os.getenv("ADAPTIVE_OC_MARGIN_MAX", "0.05"))
    tl_penalty_min = float(getattr(reward_cfg, "MISSION_NO_CONTEST_PENALTY", 0.0))
    tl_oc_min = float(getattr(reward_cfg, "VP_OBJECTIVE_OC_MARGIN_SCALE", 0.0))

    started = time.perf_counter()
    pbar = tqdm(total=int(totLifeT), mininterval=ACTOR_PBAR_MININTERVAL, miniters=ACTOR_PBAR_MINITERS)

    while done_actors < num_actors:
        try:
            kind, payload = data_q.get(timeout=1.0)
        except mp_queue.Empty:
            continue

        if kind == "error":
            raise RuntimeError(payload)
        if kind == "done":
            done_actors += 1
            continue
        if kind == "ep":
            if isinstance(payload, dict):
                if payload.get("episode") is None:
                    payload["episode"] = len(ep_rows) + 1
                ep_rows.append(payload)
                episodes_finished = len(ep_rows)
                target_n = min(int(totLifeT), int(episodes_finished))
                if target_n > int(pbar.n):
                    pbar.update(target_n - int(pbar.n))
                # GUI прогресс читает stdout и парсит шаблон ep=X/Y.
                if (episodes_finished % ACTOR_PROGRESS_STDOUT_EVERY == 0) or (episodes_finished >= int(totLifeT)):
                    try:
                        print(f"ep={episodes_finished}/{totLifeT}", flush=True)
                    except Exception:
                        pass

                # Periodic DET-like eval для Actor-Learner (аналог DET_EVAL в основном loop).
                if (
                    ACTOR_DET_EVAL_ENABLED
                    and episodes_finished > 0
                    and (episodes_finished % ACTOR_DET_EVAL_EVERY_EPISODES == 0)
                    and episodes_finished != last_actor_det_eval_ep
                ):
                    try:
                        det_payload = _run_actor_det_eval(
                            policy_net=policy_net,
                            roster_config=roster_config,
                            b_len=b_len,
                            b_hei=b_hei,
                            n_eval=ACTOR_DET_EVAL_EPISODES,
                            opponent_epsilon=ACTOR_DET_EVAL_OPPONENT_EPSILON,
                            self_play_enabled=bool(SELF_PLAY_ENABLED),
                            opponent_spec=opponent_spec,
                        )
                        det_payload["episode"] = int(episodes_finished)
                        det_payload["algo"] = "dqn"
                        det_payload["eval_tag"] = (
                            "actor_learner_policy_fn"
                            if bool(SELF_PLAY_ENABLED) and (opponent_spec is not None)
                            else "actor_learner_heuristic"
                        )
                        if last_loss is not None:
                            det_payload["training_loss"] = float(last_loss)
                        if adaptive_tl_curriculum:
                            try:
                                tl_rate = float(det_payload.get("turn_limit_rate", 0.0) or 0.0)
                                old_pen = float(getattr(reward_cfg, "MISSION_NO_CONTEST_PENALTY", tl_penalty_min))
                                old_oc = float(getattr(reward_cfg, "VP_OBJECTIVE_OC_MARGIN_SCALE", tl_oc_min))
                                new_pen = old_pen
                                new_oc = old_oc
                                if tl_rate >= tl_curriculum_hi:
                                    new_pen = min(tl_penalty_max, old_pen + tl_penalty_step)
                                    new_oc = min(tl_oc_max, old_oc + tl_oc_step)
                                elif tl_rate <= tl_curriculum_lo:
                                    new_pen = max(tl_penalty_min, old_pen - tl_penalty_step)
                                    new_oc = max(tl_oc_min, old_oc - tl_oc_step)
                                reward_cfg.MISSION_NO_CONTEST_PENALTY = float(new_pen)
                                reward_cfg.VP_OBJECTIVE_OC_MARGIN_SCALE = float(new_oc)
                                if abs(new_pen - old_pen) > 1e-9 or abs(new_oc - old_oc) > 1e-9:
                                    _log_train(
                                        "[TRAIN][CURRICULUM] adaptive_turn_limit "
                                        f"ep={episodes_finished} tl_rate={tl_rate:.3f} "
                                        f"MISSION_NO_CONTEST_PENALTY={old_pen:.3f}->{new_pen:.3f} "
                                        f"VP_OBJECTIVE_OC_MARGIN_SCALE={old_oc:.4f}->{new_oc:.4f}"
                                    )
                            except Exception:
                                pass
                        _save_actor_det_eval_snapshot(run_id=str(randNum), payload=det_payload, metrics_dir=METRICS_DIR)
                        # Обновляем графики + data_*.json сразу после DET-eval,
                        # чтобы GUI мог показывать прогресс без ожидания завершения тренировки.
                        try:
                            det_gui = save_actor_det_eval_plot(run_id=str(randNum), metrics_dir=METRICS_DIR)
                            if det_gui:
                                try:
                                    learner_side = str(learner_identity.side or "P1").strip().upper() or "P1"
                                except Exception:
                                    learner_side = "P1"
                                opponent_side = "P2" if learner_side == "P1" else "P1"
                                opponent_faction = str(roster_config.get("enemy_faction", "Unknown")).strip()
                                opponent_source = str(opponent_source_actor)
                                opponent_id = str(opponent_id_actor)
                                _write_det_eval_data_json(
                                    run_id=str(randNum),
                                    det_plot_gui_paths=det_gui,
                                    model_path="",
                                    metrics_mode="det_eval",
                                    extra={
                                        "algo": "dqn",
                                        "mode": "actor_learner",
                                        "learner_side": learner_side,
                                        "learner_faction": str(learner_identity.faction or "Unknown"),
                                        "opponent_side": opponent_side,
                                        "opponent_faction": opponent_faction,
                                        "opponent_algo": "dqn" if (SELF_PLAY_ENABLED and opponent_spec is not None) else "heuristic",
                                        "opponent_source": opponent_source,
                                        "opponent_id": str(opponent_id or ""),
                                    },
                                )
                        except Exception:
                            pass
                        det_line = (
                            "[ACTOR_LEARNER][DET_EVAL] "
                            f"ep={episodes_finished} "
                            f"eval_episodes={det_payload['eval_episodes']} "
                            f"win_rate={det_payload['win_rate']:.3f} "
                            f"draw_rate={det_payload['draw_rate']:.3f} "
                            f"turn_limit_rate={det_payload['turn_limit_rate']:.3f} "
                            f"wipeout_enemy_rate={det_payload['wipeout_enemy_rate']:.3f} "
                            f"wipeout_model_rate={det_payload['wipeout_model_rate']:.3f} "
                            f"vp_diff_mean={det_payload['vp_diff_mean']:.3f} "
                            f"ep_len_mean={det_payload['ep_len_mean']:.3f} "
                            f"opp_eps={det_payload['opponent_epsilon']:.3f}"
                        )
                        append_agent_log(det_line)
                        if TRAIN_LOG_TO_CONSOLE:
                            print(det_line)
                        last_actor_det_eval_ep = int(episodes_finished)
                    except Exception as exc:
                        warn_line = f"[ACTOR_LEARNER][DET_EVAL][WARN] eval пропущен: {exc}"
                        append_agent_log(warn_line)
                        if TRAIN_LOG_TO_CONSOLE:
                            print(warn_line)

                # Пер-эпизодная "супер-подробная" диагностика (JSONL).
                try:
                    # В actor-learner payload уже включает нужные поля; просто продублируем в JSONL,
                    # чтобы потом анализировать draw без парсинга огромных логов.
                    append_episode_diagnostics(
                        run_id=str(randNum),
                        episode_row={
                            k: payload.get(k)
                            for k in (
                                "episode",
                                "actor_idx",
                                "actor_ep",
                                "ep_reward",
                                "ep_len",
                                "turn",
                                "battle_round",
                                "model_vp",
                                "player_vp",
                                "vp_diff",
                                "result",
                                "end_reason",
                                "end_code",
                            )
                        },
                        diagnostics={
                            "model_hp_total": payload.get("model_hp_total"),
                            "enemy_hp_total": payload.get("enemy_hp_total"),
                            "damage_dealt_total": payload.get("damage_dealt_total"),
                            "damage_taken_total": payload.get("damage_taken_total"),
                            "model_ctrl": payload.get("model_ctrl", []),
                            "enemy_ctrl": payload.get("enemy_ctrl", []),
                            "model_ctrl_n": payload.get("model_ctrl_n", 0),
                            "enemy_ctrl_n": payload.get("enemy_ctrl_n", 0),
                            "timeline": payload.get("timeline", []),
                        },
                        metrics_dir=METRICS_DIR,
                    )
                except Exception as exc:
                    if TRAIN_LOG_TO_CONSOLE:
                        print(f"[METRICS][WARN] actor-learner append_episode_diagnostics failed: {exc}")

                # Пишем подробную аналитику действий (из actor-процесса) в общий лог.
                try:
                    trace_payload = payload.get("trace_actions") if isinstance(payload, dict) else None
                    if isinstance(trace_payload, dict):
                        ep_i = int(payload.get("episode") or episodes_finished or 0)
                        actor_idx = payload.get("actor_idx")
                        _log_train(_format_action_trace_summary(ep_i, int(actor_idx) if actor_idx is not None else None, trace_payload))
                except Exception:
                    pass

                # Пошаговый трейс пишем ТОЛЬКО из learner, чтобы global ep совпадал с CSV.
                try:
                    trace_steps = payload.get("trace_steps") if isinstance(payload, dict) else None
                    if isinstance(trace_steps, list) and trace_steps:
                        ep_i = int(payload.get("episode") or episodes_finished or 0)
                        actor_idx = payload.get("actor_idx")
                        _trace_write_lines(
                            ep_i,
                            [str(x) for x in trace_steps],
                            actor_idx=(int(actor_idx) if actor_idx is not None else None),
                            run_id=str(randNum),
                        )
                except Exception:
                    pass
            continue
        if kind != "batch":
            continue

        for (s_np, a_list, r_sum, ns_np, done_flag, n_count) in payload:
            dev = next(policy_net.parameters()).device
            state_t = torch.tensor(np.asarray(s_np, dtype=np.float32), device=dev).unsqueeze(0)
            action_t = torch.tensor([a_list], device="cpu")
            reward_t = torch.tensor([float(r_sum)], device=dev, dtype=torch.float32)
            next_state_t = None
            if ns_np is not None:
                next_state_t = torch.tensor(np.asarray(ns_np, dtype=np.float32), device=dev).unsqueeze(0)
            memory.push(state_t, action_t, next_state_t, reward_t, int(n_count), None)
            global_step += 1

        for _ in range(updates_per_batch):
            per_beta = PER_BETA_START
            if PER_ENABLED and PER_BETA_FRAMES > 0:
                per_beta = min(
                    1.0,
                    PER_BETA_START + (1.0 - PER_BETA_START) * (optimize_steps / float(PER_BETA_FRAMES)),
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
            if result and result.get("loss") is not None:
                last_loss = float(result["loss"])
                optimize_steps += 1
                loss_trace.append(float(last_loss))
                if lr_scheduler is not None:
                    if DQN_LR_SCHEDULER == "plateau":
                        lr_scheduler.step(float(last_loss))
                    else:
                        lr_scheduler.step()

            # периодически публикуем свежие веса для акторов
            if sync_enabled and (optimize_steps - last_sync_opt_steps) >= sync_every_updates:
                try:
                    cpu_sd = {
                        k: v.detach().cpu()
                        for k, v in normalize_state_dict(policy_net.state_dict()).items()
                    }
                    torch.save({"optimize_steps": int(optimize_steps), "state_dict": cpu_sd}, sync_path)
                    last_sync_opt_steps = int(optimize_steps)
                except Exception:
                    pass

            with torch.no_grad():
                for p_tgt, p in zip(target_net.parameters(), policy_net.parameters()):
                    p_tgt.data.mul_(1.0 - TAU)
                    p_tgt.data.add_(p.data, alpha=TAU)

        # прогресс по ep_rows (приходит отдельными сообщениями "ep")

    pbar.close()
    elapsed = time.perf_counter() - started
    print(
        f"[ACTOR_LEARNER] done: episodes={totLifeT} steps={global_step} updates={optimize_steps} "
        f"loss={last_loss} elapsed_s={elapsed:.2f}"
    )

    # Сохранение метрик/графиков как в обычном режиме.
    try:
        run_id = str(randNum)

        # --- side mapping: кто считается "model" в CSV/метриках ---
        try:
            learner_side = str(learner_identity.side or "P1").strip().upper() or "P1"
            opponent_side = "P2" if learner_side == "P1" else "P1"
            _log_train(
                "[METRICS][SIDES] "
                f"learner_side={learner_side} opponent_side={opponent_side} "
                "CSV fields: model_* == learner_side, player_* == opponent_side; "
                "result='win' означает победу learner_side."
            )
        except Exception:
            pass

        # CSV для отладки; legacy PNG в runtime/state/img не пишем (GUI на DET-eval).
        save_extra_metrics(run_id=run_id, ep_rows=ep_rows, metrics_dir=METRICS_DIR, write_legacy_gui_plots=False)

        # --- save model (so GUI can find latest model) ---
        safe_name = "ACTOR_LEARNER"
        date = datetime.datetime.now().strftime("%d-%H%M%S")
        os.makedirs(os.path.join(MODELS_DIR, safe_name), exist_ok=True)
        model_path = os.path.join(MODELS_DIR, safe_name, f"model-{date}-{run_id}.pth")
        with IO_PROFILER.timed("checkpoint save"):
            actor_ckpt = {
                "policy_net": policy_net.state_dict(),
                "net_type": NET_TYPE,
                "algo": "dqn",
                "optimizer": optimizer.state_dict(),
                "global_step": int(global_step),
                "optimize_steps": int(optimize_steps),
                "episode": int(len(ep_rows)),
                "replay_memory": memory.state_dict(),
            }
            actor_ckpt.update(_dqn_checkpoint_extra(policy_net, target_net, optimizer, lr_scheduler))
            torch.save(actor_ckpt, model_path)

        det_gui = save_actor_det_eval_plot(run_id=run_id, metrics_dir=METRICS_DIR)
        if det_gui:
            try:
                learner_side = str(learner_identity.side or "P1").strip().upper() or "P1"
            except Exception:
                learner_side = "P1"
            opponent_side = "P2" if learner_side == "P1" else "P1"
            opponent_faction = str(roster_config.get("enemy_faction", "Unknown")).strip()
            opponent_source = str(opponent_source_actor)
            opponent_id = str(opponent_id_actor)
            _write_det_eval_data_json(
                run_id=run_id,
                det_plot_gui_paths=det_gui,
                model_path=model_path.replace("\\", "/"),
                metrics_mode="det_eval",
                extra={
                    "mode": "actor_learner",
                    "algo": "dqn",
                    "learner_side": learner_side,
                    "learner_faction": str(learner_identity.faction or "Unknown"),
                    "opponent_side": opponent_side,
                    "opponent_faction": opponent_faction,
                    "opponent_algo": "dqn" if (SELF_PLAY_ENABLED and opponent_spec is not None) else "heuristic",
                    "opponent_source": opponent_source,
                    "opponent_id": str(opponent_id or ""),
                },
            )
        else:
            _write_det_eval_data_json(
                run_id=run_id,
                det_plot_gui_paths={},
                model_path=model_path.replace("\\", "/"),
                metrics_mode="det_eval",
                extra={
                    "mode": "actor_learner",
                    "algo": "dqn",
                    "det_eval_note": "нет точек actor_det_eval_*.jsonl",
                    "learner_side": str(getattr(learner_identity, "side", "P1") or "P1"),
                    "learner_faction": str(getattr(learner_identity, "faction", "Unknown") or "Unknown"),
                    "opponent_side": "P2" if str(getattr(learner_identity, "side", "P1") or "P1").strip().upper() == "P1" else "P1",
                    "opponent_faction": str(roster_config.get("enemy_faction", "Unknown")).strip(),
                    "opponent_algo": "dqn" if (SELF_PLAY_ENABLED and opponent_spec is not None) else "heuristic",
                    "opponent_source": str(opponent_source_actor),
                    "opponent_id": str(opponent_id_actor or ""),
                },
            )

        print("Generated metrics")
        save_training_summary(run_id=run_id, model_tag=model_path.replace("\\", "/"), ep_rows=ep_rows, elapsed_s=elapsed)
        save_heuristic_metrics_snapshot(run_id=run_id, ep_rows=ep_rows)
    except Exception as exc:
        if TRAIN_LOG_TO_CONSOLE:
            print(f"[ACTOR_LEARNER][WARN] не удалось сохранить метрики: {exc}")

    # --- agent snapshot for GUI ("Конкретный агент" / latest_snapshot) ---
    # Делаем независимо от блока метрик: если метрики/плоты упали, агент всё равно должен сохраниться.
    try:
        safe_model_tag = ""
        try:
            safe_model_tag = model_path.replace("\\", "/")  # type: ignore[name-defined]
        except Exception:
            safe_model_tag = ""
        final_agent_id = build_agent_id(learner_identity, f"final_ep{len(ep_rows)}")
        artifact_dir = save_agent_artifact(
            identity=learner_identity,
            agent_id=final_agent_id,
            env_contract=env_contract,
            policy_state_dict=normalize_state_dict(policy_net.state_dict()),
            target_state_dict=normalize_state_dict(target_net.state_dict()),
            optimizer_state_dict=optimizer.state_dict(),
            extra_meta={
                "algo": "dqn",
                "episode": int(len(ep_rows)),
                "legacy_model_tag": safe_model_tag,
                "mode": "actor_learner",
                "num_actors": int(num_actors),
                "self_play_enabled": int(1 if SELF_PLAY_ENABLED else 0),
                "opponent_agent_id": str(OPPONENT_AGENT_ID or ""),
            },
        )
        append_agent_log(f"[LEAGUE][SAVE] agent_id={final_agent_id} artifact_dir={artifact_dir}")
    except Exception as exc:
        warn = f"[LEAGUE][WARN] DQN agent snapshot не сохранён: {exc}"
        append_agent_log(warn)
        if TRAIN_LOG_TO_CONSOLE:
            print(warn)

    # Быстрый sanity-check качества (по желанию).
    eval_eps = int(os.getenv("ACTOR_EVAL_EPISODES", "20") or "20")
    if eval_eps > 0:
        try:
            payload = _run_actor_det_eval(
                policy_net=policy_net,
                roster_config=roster_config,
                b_len=b_len,
                b_hei=b_hei,
                n_eval=eval_eps,
                opponent_epsilon=0.0,
                self_play_enabled=bool(SELF_PLAY_ENABLED),
                opponent_spec=opponent_spec,
            )
            print(
                "[ACTOR_LEARNER][EVAL] "
                f"eval_episodes={payload['eval_episodes']} "
                f"win_rate={payload['win_rate']:.3f} "
                f"draw_rate={payload['draw_rate']:.3f} "
                f"turn_limit_rate={payload['turn_limit_rate']:.3f} "
                f"wipeout_enemy_rate={payload['wipeout_enemy_rate']:.3f} "
                f"wipeout_model_rate={payload['wipeout_model_rate']:.3f} "
                f"vp_diff_mean={payload['vp_diff_mean']:.3f}"
            )
        except Exception as exc:
            if TRAIN_LOG_TO_CONSOLE:
                print(f"[ACTOR_LEARNER][EVAL][WARN] eval пропущен: {exc}")

    for p in procs:
        try:
            p.join(timeout=1.0)
        except Exception:
            pass


def _main_actor_learner_ppo(*, roster_config, totLifeT, clip_reward_enabled, clip_reward_min, clip_reward_max) -> None:
    """
    PRO Actor-Learner для PPO (on-policy):
    - Actors (CPU) собирают шаги (obs, action, reward, done, logprob, value, masks) и шлют пачками.
    - Learner (GPU) агрегирует роллауты, считает GAE и делает PPO update.
    """
    num_actors = max(1, int(os.getenv("NUM_ACTORS", "8")))
    batch_send = max(8, int(os.getenv("ACTOR_BATCH_SEND", "32")))
    queue_max = max(64, int(os.getenv("ACTOR_QUEUE_MAX", "256")))

    b_len = roster_config["b_len"]
    b_hei = roster_config["b_hei"]
    trunc = True

    # 1) Определяем размеры наблюдения и action-space (как в DQN actor-learner)
    enemy0, model0 = _build_units_from_config(roster_config, b_len, b_hei)
    env0 = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy0, model=model0, b_len=b_len, b_hei=b_hei)
    state0, _info0 = env0.reset(options={"m": model0, "e": enemy0, "Type": "big", "trunc": True})
    if isinstance(state0, dict) or "OrderedDict" in str(type(state0)):
        n_observations = len(list(state0.values()))
    else:
        n_observations = int(np.array(state0).shape[0])

    ordered_keys = ["move", "attack", "shoot", "charge", "use_cp", "cp_on"]
    for i_u in range(len(model0)):
        ordered_keys.append(f"move_num_{i_u}")
    n_actions = []
    for k in ordered_keys:
        sp = env0.action_space.spaces[k]
        if hasattr(sp, "n"):
            n_actions.append(int(sp.n))
        elif hasattr(sp, "nvec"):
            n_actions.extend([int(x) for x in sp.nvec])
        else:
            raise TypeError(f"Unsupported action space for {k}: {type(sp)}")
    try:
        env0.close()
    except Exception:
        pass

    # 2) Learner (GPU)
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
            "actor_learner": 1,
            "train_algo": "ppo",
            "num_actors": int(num_actors),
        },
    )

    actor_critic = make_actor_critic(n_observations, n_actions).to(device)
    optimizer = optim.AdamW(actor_critic.parameters(), lr=PPO_LR, amsgrad=True)
    _patch_optimizer_methods_no_compile(optimizer)
    ppo_lr_scheduler = _build_ppo_lr_scheduler(optimizer, total_steps_hint=int(totLifeT) * 20)
    buffer = PPORolloutBuffer()
    entropy_coef = float(PPO_ENTROPY_COEF)
    ppo_kw = ppo_kwargs_from_env()
    append_agent_log(
        f"[PPO][CONFIG] actor_learner num_actors={num_actors} hidden_size={ppo_kw['hidden_size']} "
        f"num_layers={ppo_kw['num_layers']} n_value_ensemble={ppo_kw['n_value_ensemble']} "
        f"lr_scheduler={PPO_LR_SCHEDULER} adaptive_entropy={int(PPO_ADAPTIVE_ENTROPY)}"
    )

    # Self-play opponent snapshot (optional): загружаем один раз в learner и раздаём акторам.
    opponent_state_dict_cpu = None
    opponent_source_label = "heuristic_auto"
    opponent_agent_id = None
    opponent_spec_det: OpponentSpec | None = None
    # algo загруженного оппонента (для решения: обновлять ли снапшоты с PPO-learner)
    checkpoint_meta_algo: str | None = None
    if SELF_PLAY_ENABLED:
        try:
            if SELF_PLAY_OPPONENT_MODE == "fixed_checkpoint" and SELF_PLAY_FIXED_PATH:
                checkpoint = torch.load(SELF_PLAY_FIXED_PATH, map_location="cpu", weights_only=False)
                if isinstance(checkpoint, dict) and "actor_critic" in checkpoint:
                    opponent_state_dict_cpu = normalize_state_dict(checkpoint["actor_critic"])
                elif isinstance(checkpoint, dict) and "policy_net" in checkpoint:
                    opponent_state_dict_cpu = normalize_state_dict(checkpoint["policy_net"])
                elif isinstance(checkpoint, dict):
                    opponent_state_dict_cpu = normalize_state_dict(checkpoint)
                else:
                    opponent_state_dict_cpu = normalize_state_dict(checkpoint)
                opponent_source_label = "fixed_checkpoint"
                if isinstance(checkpoint, dict):
                    checkpoint_meta_algo = str(checkpoint.get("algo", "") or "").strip().lower()
                    if checkpoint_meta_algo not in ("dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero"):
                        if "actor_critic" in checkpoint:
                            checkpoint_meta_algo = "ppo"
                        elif "gumbel_muzero_net" in checkpoint:
                            checkpoint_meta_algo = "gumbel_muzero"
                        elif "policy_value_net" in checkpoint:
                            mm = str(checkpoint.get("mcts_mode", "") or "").strip().lower()
                            if mm == "proxy":
                                checkpoint_meta_algo = "alphazero_proxy"
                            elif mm == "tree":
                                checkpoint_meta_algo = "alphazero_tree"
                        elif "policy_net" in checkpoint:
                            checkpoint_meta_algo = "dqn"
                if opponent_state_dict_cpu is not None:
                    opponent_spec_det = OpponentSpec(
                        agent_id=str(SELF_PLAY_FIXED_PATH),
                        algo=str(checkpoint_meta_algo or "ppo"),
                        contract=dict(env_contract),
                        policy_state=dict(opponent_state_dict_cpu),
                    )
            else:
                if not OPPONENT_AGENT_ID:
                    raise ValueError("SELF_PLAY snapshot: нужен OPPONENT_AGENT_ID (GUI должен подставить latest_snapshot).")
                _opp_spec_ppo = load_agent_opponent(agent_id=OPPONENT_AGENT_ID, expected_contract=env_contract)
                opponent_state_dict_cpu = normalize_state_dict(_opp_spec_ppo.policy_state)
                checkpoint_meta_algo = str(_opp_spec_ppo.algo).lower()
                opponent_spec_det = _opp_spec_ppo
                opponent_source_label = "snapshot_policy_fn"
                opponent_agent_id = str(OPPONENT_AGENT_ID)
        except Exception as exc:
            warn = f"[SELFPLAY][WARN] PPO actor-learner: не удалось загрузить оппонента, откатываюсь на эвристику. exc={exc}"
            append_agent_log(warn)
            if TRAIN_LOG_TO_CONSOLE:
                print(warn)
            opponent_state_dict_cpu = None
            opponent_source_label = "heuristic_auto"
            checkpoint_meta_algo = None
            opponent_spec_det = None

    # PPO vs PPO: learner периодически пишет снапшот в latest_ppo_opp. PPO vs DQN: оппонент фиксирован.
    opponent_snapshot_sync_enabled = True
    if SELF_PLAY_ENABLED and opponent_state_dict_cpu is not None and checkpoint_meta_algo in (
        "dqn",
        "ppo",
        "alphazero_tree",
        "alphazero_proxy",
        "gumbel_muzero",
    ):
        opponent_snapshot_sync_enabled = checkpoint_meta_algo == "ppo"

    # Sync learner -> actors (через файл, Windows-friendly)
    sync_enabled = os.getenv("ACTOR_SYNC_ENABLED", "1") == "1"
    sync_every_updates = max(1, int(os.getenv("ACTOR_SYNC_EVERY_UPDATES", "1")))
    sync_path = os.path.join(MODELS_DIR, "actor_sync", "latest_ppo.pth")
    os.makedirs(os.path.dirname(sync_path), exist_ok=True)
    last_sync_update_step = 0

    # Sync opponent -> actors
    opp_sync_path = os.path.join(MODELS_DIR, "actor_sync", "latest_ppo_opp.pth")
    os.makedirs(os.path.dirname(opp_sync_path), exist_ok=True)
    last_opp_sync_episode = 0
    snapshot_update_every = max(1, int(SELF_PLAY_UPDATE_EVERY_EPISODES))

    init_weights = {
        k: v.detach().cpu().clone()
        for k, v in normalize_state_dict(actor_critic.state_dict()).items()
    }

    ctx = mp.get_context("spawn")
    data_q: mp.Queue = ctx.Queue(maxsize=queue_max)

    procs = []
    for a_idx in range(num_actors):
        base = int(totLifeT) // int(num_actors)
        rem = int(totLifeT) % int(num_actors)
        episodes = int(base + (1 if a_idx < rem else 0))
        cr_min = 0.0 if clip_reward_min is None else float(clip_reward_min)
        cr_max = 0.0 if clip_reward_max is None else float(clip_reward_max)
        p = ctx.Process(
            target=_actor_learner_actor_entry_ppo,
            args=(
                a_idx,
                int(episodes),
                roster_config,
                int(b_len),
                int(b_hei),
                int(n_observations),
                list(n_actions),
                init_weights,
                int(batch_send),
                float(cr_min),
                float(cr_max),
                bool(clip_reward_enabled),
                data_q,
            ),
            daemon=True,
        )
        p.start()
        procs.append(p)

    done_actors = 0
    episodes_finished = 0
    global_step = 0
    ppo_update_step = 0
    last_checkpoint = ""
    last_actor_det_eval_ep = 0

    run_id = str(random.randint(1000000, 9999999))
    model_name = datetime.datetime.now().strftime("%d-%H%M%S")
    metrics_obj = metrics(MODELS_DIR, run_id, model_name)
    ep_rows: list[dict] = []
    last_update_metrics = {"policy_loss": 0.0, "value_loss": 0.0, "entropy": 0.0, "approx_kl": 0.0, "clip_fraction": 0.0}
    adaptive_tl_curriculum = os.getenv("ADAPTIVE_TURN_LIMIT_CURRICULUM", "1").strip() == "1"
    tl_curriculum_hi = float(os.getenv("ADAPTIVE_TL_RATE_HIGH", "0.72"))
    tl_curriculum_lo = float(os.getenv("ADAPTIVE_TL_RATE_LOW", "0.58"))
    tl_penalty_step = float(os.getenv("ADAPTIVE_NO_CONTEST_STEP", "0.01"))
    tl_penalty_max = float(os.getenv("ADAPTIVE_NO_CONTEST_MAX", "0.30"))
    tl_oc_step = float(os.getenv("ADAPTIVE_OC_MARGIN_STEP", "0.003"))
    tl_oc_max = float(os.getenv("ADAPTIVE_OC_MARGIN_MAX", "0.05"))
    tl_penalty_min = float(getattr(reward_cfg, "MISSION_NO_CONTEST_PENALTY", 0.0))
    tl_oc_min = float(getattr(reward_cfg, "VP_OBJECTIVE_OC_MARGIN_SCALE", 0.0))

    append_agent_log(f"[PPO][ACTOR_LEARNER][CONFIG] actors={num_actors} batch_send={batch_send} queue_max={queue_max}")
    print(f"[PPO][ACTOR_LEARNER][CONFIG] actors={num_actors} batch_send={batch_send}", flush=True)
    if SELF_PLAY_ENABLED:
        append_agent_log(
            "[SELFPLAY][CONFIG] "
            f"enabled=1 mode={SELF_PLAY_OPPONENT_MODE} learner_algo=ppo opponent_algo={checkpoint_meta_algo or '-'} "
            f"opponent_snapshot_sync={int(opponent_snapshot_sync_enabled)} "
            f"opponent_agent_id={OPPONENT_AGENT_ID or '-'} "
            f"enemy_policy_mode={opponent_source_label} snapshot_update_every={snapshot_update_every}"
        )

    while done_actors < num_actors:
        try:
            kind, payload = data_q.get(timeout=1.0)
        except mp_queue.Empty:
            continue

        if kind == "error":
            raise RuntimeError(payload)
        if kind == "done":
            done_actors += 1
            continue

        if kind == "ep":
            if isinstance(payload, dict):
                # learner-side нумерация по порядку
                if len(ep_rows) >= int(totLifeT):
                    continue
                if payload.get("episode") is None:
                    payload["episode"] = len(ep_rows) + 1
                ep_rows.append(payload)
                episodes_finished = len(ep_rows)
                # GUI прогресс читает stdout и парсит шаблон ep=X/Y.
                print(f"[PPO] ep={episodes_finished}/{totLifeT} done", flush=True)
                metrics_obj.updateRew(float(payload.get("ep_reward", 0.0) or 0.0))
                metrics_obj.updateEpLen(int(payload.get("ep_len", 0) or 0))
                append_episode_diagnostics(
                    run_id=run_id,
                    episode_row={k: payload.get(k) for k in ("episode","ep_reward","ep_len","turn","model_vp","player_vp","vp_diff","result","end_reason","end_code")},
                    diagnostics={
                        "algo": "ppo",
                        "self_play_enabled": int(1 if SELF_PLAY_ENABLED else 0),
                        "opponent_source": str(opponent_source_label),
                        "opponent_agent_id": str(opponent_agent_id or ""),
                        "snapshot_update_every": int(snapshot_update_every),
                        "policy_loss": float(last_update_metrics.get("policy_loss", 0.0)),
                        "value_loss": float(last_update_metrics.get("value_loss", 0.0)),
                        "entropy": float(last_update_metrics.get("entropy", 0.0)),
                        "approx_kl": float(last_update_metrics.get("approx_kl", 0.0)),
                        "clip_fraction": float(last_update_metrics.get("clip_fraction", 0.0)),
                        "global_step": int(global_step),
                        "update_step": int(ppo_update_step),
                    },
                    metrics_dir=METRICS_DIR,
                )

                # Periodic DET-like eval для PPO Actor-Learner (как в DQN actor-learner).
                if (
                    ACTOR_DET_EVAL_ENABLED
                    and episodes_finished > 0
                    and (episodes_finished % ACTOR_DET_EVAL_EVERY_EPISODES == 0)
                    and episodes_finished != last_actor_det_eval_ep
                ):
                    try:
                        det_payload = _run_actor_det_eval_ppo(
                            actor_critic=actor_critic,
                            roster_config=roster_config,
                            b_len=b_len,
                            b_hei=b_hei,
                            n_actions=[int(x) for x in n_actions],
                            n_eval=ACTOR_DET_EVAL_EPISODES,
                            opponent_epsilon=ACTOR_DET_EVAL_OPPONENT_EPSILON,
                            self_play_enabled=bool(SELF_PLAY_ENABLED),
                            opponent_spec=opponent_spec_det,
                        )
                        det_payload["episode"] = int(episodes_finished)
                        det_payload["algo"] = "ppo"
                        det_payload["eval_tag"] = (
                            "actor_learner_policy_fn"
                            if bool(SELF_PLAY_ENABLED) and (opponent_spec_det is not None)
                            else "actor_learner_heuristic"
                        )
                        det_payload["training_loss"] = float(
                            last_update_metrics.get("policy_loss", 0.0)
                            + PPO_VALUE_COEF * last_update_metrics.get("value_loss", 0.0)
                        )
                        if adaptive_tl_curriculum:
                            try:
                                tl_rate = float(det_payload.get("turn_limit_rate", 0.0) or 0.0)
                                old_pen = float(getattr(reward_cfg, "MISSION_NO_CONTEST_PENALTY", tl_penalty_min))
                                old_oc = float(getattr(reward_cfg, "VP_OBJECTIVE_OC_MARGIN_SCALE", tl_oc_min))
                                new_pen = old_pen
                                new_oc = old_oc
                                if tl_rate >= tl_curriculum_hi:
                                    new_pen = min(tl_penalty_max, old_pen + tl_penalty_step)
                                    new_oc = min(tl_oc_max, old_oc + tl_oc_step)
                                elif tl_rate <= tl_curriculum_lo:
                                    new_pen = max(tl_penalty_min, old_pen - tl_penalty_step)
                                    new_oc = max(tl_oc_min, old_oc - tl_oc_step)
                                reward_cfg.MISSION_NO_CONTEST_PENALTY = float(new_pen)
                                reward_cfg.VP_OBJECTIVE_OC_MARGIN_SCALE = float(new_oc)
                                if abs(new_pen - old_pen) > 1e-9 or abs(new_oc - old_oc) > 1e-9:
                                    append_agent_log(
                                        "[TRAIN][CURRICULUM] adaptive_turn_limit "
                                        f"ep={episodes_finished} tl_rate={tl_rate:.3f} "
                                        f"MISSION_NO_CONTEST_PENALTY={old_pen:.3f}->{new_pen:.3f} "
                                        f"VP_OBJECTIVE_OC_MARGIN_SCALE={old_oc:.4f}->{new_oc:.4f}"
                                    )
                            except Exception:
                                pass
                        _save_actor_det_eval_snapshot(run_id=str(run_id), payload=det_payload, metrics_dir=METRICS_DIR)
                        # Обновляем графики + data_*.json сразу после DET-eval, чтобы GUI видел прогресс.
                        try:
                            det_gui = save_actor_det_eval_plot(run_id=str(run_id), metrics_dir=METRICS_DIR)
                            if det_gui:
                                learner_side = str(getattr(learner_identity, "side", "P1") or "P1").strip().upper() or "P1"
                                opponent_side = "P2" if learner_side == "P1" else "P1"
                                _write_det_eval_data_json(
                                    run_id=str(run_id),
                                    det_plot_gui_paths=det_gui,
                                    model_path=str(last_checkpoint).replace("\\", "/") if last_checkpoint else "",
                                    metrics_mode="det_eval",
                                    extra={
                                        "algo": "ppo",
                                        "mode": "actor_learner",
                                        "learner_side": learner_side,
                                        "learner_faction": str(getattr(learner_identity, "faction", "Unknown") or "Unknown"),
                                        "opponent_side": opponent_side,
                                        "opponent_faction": str(roster_config.get("enemy_faction", "Unknown")).strip(),
                                        "opponent_algo": str(checkpoint_meta_algo or "heuristic"),
                                        "opponent_source": str(opponent_source_label),
                                        "opponent_id": str(opponent_agent_id or ""),
                                    },
                                )
                        except Exception:
                            pass
                        det_line = (
                            "[ACTOR_LEARNER][DET_EVAL] "
                            f"ep={episodes_finished} "
                            f"eval_episodes={det_payload['eval_episodes']} "
                            f"win_rate={det_payload['win_rate']:.3f} "
                            f"draw_rate={det_payload['draw_rate']:.3f} "
                            f"turn_limit_rate={det_payload['turn_limit_rate']:.3f} "
                            f"wipeout_enemy_rate={det_payload['wipeout_enemy_rate']:.3f} "
                            f"wipeout_model_rate={det_payload['wipeout_model_rate']:.3f} "
                            f"vp_diff_mean={det_payload['vp_diff_mean']:.3f} "
                            f"ep_len_mean={det_payload['ep_len_mean']:.3f}"
                        )
                        append_agent_log(det_line)
                        if TRAIN_LOG_TO_CONSOLE:
                            print(det_line)
                        last_actor_det_eval_ep = int(episodes_finished)
                    except Exception as exc:
                        warn_line = f"[ACTOR_LEARNER][DET_EVAL][WARN] eval пропущен: {exc}"
                        append_agent_log(warn_line)
                        if TRAIN_LOG_TO_CONSOLE:
                            print(warn_line)

                # Periodic opponent snapshot update (learner -> actors + registry)
                if (
                    SELF_PLAY_ENABLED
                    and opponent_snapshot_sync_enabled
                    and (episodes_finished - last_opp_sync_episode) >= snapshot_update_every
                ):
                    try:
                        opponent_state_dict_cpu = {
                            k: v.detach().cpu()
                            for k, v in normalize_state_dict(actor_critic.state_dict()).items()
                        }
                        agent_id = build_agent_id(learner_identity, f"ep{episodes_finished}")
                        artifact_dir = save_agent_artifact(
                            identity=learner_identity,
                            agent_id=agent_id,
                            env_contract=env_contract,
                            policy_state_dict=opponent_state_dict_cpu,
                            target_state_dict=None,
                            optimizer_state_dict=None,
                            extra_meta={
                                "algo": "ppo",
                                "episode": int(episodes_finished),
                                "mode": "actor_learner",
                                "num_actors": int(num_actors),
                            },
                        )
                        append_agent_log(f"[LEAGUE][SAVE][PPO] agent_id={agent_id} artifact_dir={artifact_dir}")
                        torch.save(
                            {
                                "episode": int(episodes_finished),
                                "agent_id": str(agent_id),
                                "state_dict": opponent_state_dict_cpu,
                            },
                            opp_sync_path,
                        )
                        opponent_source_label = "snapshot_policy_fn"
                        opponent_agent_id = str(agent_id)
                        opponent_spec_det = OpponentSpec(
                            agent_id=str(agent_id),
                            algo="ppo",
                            contract=dict(env_contract),
                            policy_state=dict(opponent_state_dict_cpu),
                        )
                        last_opp_sync_episode = int(episodes_finished)
                    except Exception as exc:
                        append_agent_log(f"[SELFPLAY][WARN] PPO snapshot update failed: {exc}")

                if SAVE_EVERY > 0 and (episodes_finished % SAVE_EVERY == 0):
                    last_checkpoint = _save_ppo_checkpoint(
                        actor_critic=actor_critic,
                        optimizer=optimizer,
                        episode=episodes_finished,
                        n_actions=n_actions,
                        n_observations=n_observations,
                        model=None,
                        enemy=None,
                        env_contract=env_contract,
                        roster_config=roster_config,
                        b_len=b_len,
                        b_hei=b_hei,
                        lr_scheduler=ppo_lr_scheduler,
                    )
            continue

        if kind != "rollout":
            continue

        # rollout payload: dict(actor_idx, steps=[...])
        if not isinstance(payload, dict):
            continue
        actor_idx = int(payload.get("actor_idx", -1))
        steps = payload.get("steps")
        if actor_idx < 0 or not isinstance(steps, list) or not steps:
            continue

        for step in steps:
            if not isinstance(step, dict):
                continue
            buffer.add(
                obs=np.asarray(step.get("obs"), dtype=np.float32),
                action=np.asarray(step.get("action"), dtype=np.int64),
                logprob=float(step.get("logprob", 0.0) or 0.0),
                reward=float(step.get("reward", 0.0) or 0.0),
                done=bool(step.get("done", False)),
                value=float(step.get("value", 0.0) or 0.0),
                masks_by_head=step.get("masks_by_head") or [],
                env_id=int(actor_idx),
            )
            global_step += 1

        # Update PPO по порогу шагов
        if len(buffer) >= max(1, int(PPO_ROLLOUT_STEPS)):
            batch = buffer.to_tensors(device=device, gamma=PPO_GAMMA, gae_lambda=PPO_GAE_LAMBDA, normalize_adv=True)
            if int(batch.obs.shape[0]) > 0:
                ppo_metrics, entropy_coef, updates = _run_ppo_update_loop(
                    actor_critic,
                    optimizer,
                    batch,
                    entropy_coef=entropy_coef,
                    lr_scheduler=ppo_lr_scheduler,
                )
                ppo_update_step += int(updates)
                last_update_metrics = dict(ppo_metrics)
                metrics_obj.updateLoss(ppo_metrics["policy_loss"] + PPO_VALUE_COEF * ppo_metrics["value_loss"])
                append_agent_log(
                    f"[PPO][ACTOR_LEARNER][UPDATE] policy_loss={ppo_metrics['policy_loss']:.6f} value_loss={ppo_metrics['value_loss']:.6f} "
                    f"entropy={ppo_metrics['entropy']:.6f} approx_kl={ppo_metrics['approx_kl']:.6f} "
                    f"clip_fraction={ppo_metrics['clip_fraction']:.6f} global_step={global_step} update_step={ppo_update_step}"
                )

                # sync weights
                if sync_enabled and (ppo_update_step - last_sync_update_step) >= sync_every_updates:
                    try:
                        cpu_sd = {k: v.detach().cpu() for k, v in normalize_state_dict(actor_critic.state_dict()).items()}
                        torch.save({"update_step": int(ppo_update_step), "state_dict": cpu_sd}, sync_path)
                        last_sync_update_step = int(ppo_update_step)
                    except Exception:
                        pass

            buffer.clear()

    # Финальный чекпойнт + метрики
    if not last_checkpoint:
        last_checkpoint = _save_ppo_checkpoint(
            actor_critic=actor_critic,
            optimizer=optimizer,
            episode=int(episodes_finished or totLifeT),
            n_actions=n_actions,
            n_observations=n_observations,
            model=None,
            enemy=None,
            env_contract=env_contract,
            roster_config=roster_config,
            b_len=b_len,
            b_hei=b_hei,
            lr_scheduler=ppo_lr_scheduler,
        )

    if ep_rows:
        try:
            save_extra_metrics(
                run_id=run_id, ep_rows=ep_rows, metrics_dir=METRICS_DIR, write_legacy_gui_plots=False
            )
            save_heuristic_metrics_snapshot(run_id=run_id, ep_rows=ep_rows, metrics_dir=METRICS_DIR)
            det_gui = save_actor_det_eval_plot(run_id=run_id, metrics_dir=METRICS_DIR)
            ckpt_path_for_json = str(last_checkpoint).replace("\\", "/") if last_checkpoint else ""
            if det_gui:
                _write_det_eval_data_json(
                    run_id=run_id,
                    det_plot_gui_paths=det_gui,
                    model_path=ckpt_path_for_json,
                    metrics_mode="det_eval",
                    extra={
                        "algo": "ppo",
                        "mode": "actor_learner",
                        "learner_side": str(getattr(learner_identity, "side", "P1") or "P1"),
                        "learner_faction": str(getattr(learner_identity, "faction", "Unknown") or "Unknown"),
                        "opponent_side": "P2" if str(getattr(learner_identity, "side", "P1") or "P1").strip().upper() == "P1" else "P1",
                        "opponent_faction": str(roster_config.get("enemy_faction", "Unknown")).strip(),
                        "opponent_algo": str(checkpoint_meta_algo or "heuristic"),
                        "opponent_source": str(opponent_source_label),
                        "opponent_id": str(opponent_agent_id or ""),
                    },
                )
            elif ckpt_path_for_json:
                _write_det_eval_data_json(
                    run_id=run_id,
                    det_plot_gui_paths={},
                    model_path=ckpt_path_for_json,
                    metrics_mode="det_eval",
                    extra={
                        "algo": "ppo",
                        "mode": "actor_learner",
                        "det_eval_note": "нет точек DET-eval",
                        "learner_side": str(getattr(learner_identity, "side", "P1") or "P1"),
                        "learner_faction": str(getattr(learner_identity, "faction", "Unknown") or "Unknown"),
                        "opponent_side": "P2" if str(getattr(learner_identity, "side", "P1") or "P1").strip().upper() == "P1" else "P1",
                        "opponent_faction": str(roster_config.get("enemy_faction", "Unknown")).strip(),
                        "opponent_algo": str(checkpoint_meta_algo or "heuristic"),
                        "opponent_source": str(opponent_source_label),
                        "opponent_id": str(opponent_agent_id or ""),
                    },
                )
            print("Generated metrics", flush=True)
        except Exception as exc:
            append_agent_log(
                "[PPO][ACTOR_LEARNER][METRICS][WARN] Не удалось сохранить метрики/графики. "
                f"Где: train.py _main_actor_learner_ppo. Ошибка: {exc}"
            )
    append_agent_log(f"[PPO][ACTOR_LEARNER] done: episodes={totLifeT} steps={global_step} updates={ppo_update_step} checkpoint={last_checkpoint}")

    # Финальный снапшот в registry (чтобы GUI мог выбрать PPO как оппонента).
    # Важно: сохраняем даже при SELF_PLAY_ENABLED=0 (PPO vs эвристика), иначе агент не появляется в GUI.
    try:
        final_agent_id = build_agent_id(learner_identity, f"final_ep{int(episodes_finished or len(ep_rows))}")
        artifact_dir = save_agent_artifact(
            identity=learner_identity,
            agent_id=final_agent_id,
            env_contract=env_contract,
            policy_state_dict=normalize_state_dict(actor_critic.state_dict()),
            target_state_dict=None,
            optimizer_state_dict=optimizer.state_dict(),
            extra_meta={
                "algo": "ppo",
                "episode": int(episodes_finished or len(ep_rows)),
                "mode": "actor_learner",
                "num_actors": int(num_actors),
                "self_play_enabled": int(1 if SELF_PLAY_ENABLED else 0),
                "opponent_agent_id": str(OPPONENT_AGENT_ID or ""),
            },
        )
        append_agent_log(f"[LEAGUE][SAVE][PPO] agent_id={final_agent_id} artifact_dir={artifact_dir}")
    except Exception as exc:
        append_agent_log(f"[PPO][ACTOR_LEARNER][WARN] PPO final agent snapshot failed: {exc}")


def _actor_learner_actor_entry(
    actor_idx: int,
    episodes: int,
    roster_config: dict,
    b_len: int,
    b_hei: int,
    n_observations: int,
    n_actions: list,
    init_weights: dict,
    batch_send: int,
    clip_reward_min: float,
    clip_reward_max: float,
    clip_reward_enabled: bool,
    data_q,
    opponent_spec,
    opponent_eps: float,
    self_play_enabled: int,
):
    """Top-level entrypoint for Windows spawn pickling."""
    try:
        cpu_net = _make_dqn(n_observations, n_actions).to(torch.device("cpu"))
        cpu_net.load_state_dict(init_weights)
        cpu_net.eval()

        trunc = True
        enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
        mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
        env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)

        sync_enabled = os.getenv("ACTOR_SYNC_ENABLED", "1") == "1"
        sync_path = os.path.join(MODELS_DIR, "actor_sync", "latest_policy.pth")
        sync_check_every_ep = max(1, int(os.getenv("ACTOR_SYNC_CHECK_EVERY_EP", "10")))
        last_sync_mtime = -1.0

        opponent_policy_fn = None
        if int(self_play_enabled) == 1 and opponent_spec is not None:
            try:
                opponent_policy_fn = build_policy_fn(
                    env=env,
                    len_model=len(model),
                    opponent=opponent_spec,
                    deterministic=True,
                )
            except Exception:
                opponent_policy_fn = None
        if int(self_play_enabled) == 1:
            append_agent_log(
                "[SELFPLAY][ACTOR] "
                f"actor_idx={actor_idx} "
                f"enemy_policy_mode={'snapshot_policy_fn' if opponent_policy_fn is not None else 'heuristic_auto'}"
            )

        steps_done = 0
        buf = []
        n_step_buf = collections.deque(maxlen=N_STEP)

        for _ep in range(int(episodes)):
            ep_idx_1based = int(_ep) + 1
            trace_lines: list[str] = []
            round_timeline: list[dict] = []
            step_idx = 0
            action_head_total = Counter({"move": 0, "attack": 0, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0})
            action_head_skip = Counter({"move": 0, "attack": 0, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0})
            action_head_invalid = Counter({"move": 0, "attack": 0, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0})
            shoot_windows_with_targets = 0
            shoot_windows_without_targets = 0
            shoot_taken_when_targets = 0
            move_stay = 0
            move_nonstay = 0

            if sync_enabled and (_ep % sync_check_every_ep == 0):
                try:
                    if os.path.isfile(sync_path):
                        mtime = os.path.getmtime(sync_path)
                        if mtime > last_sync_mtime:
                            payload = torch.load(sync_path, map_location="cpu", weights_only=False)
                            sd = payload.get("state_dict") if isinstance(payload, dict) else None
                            if isinstance(sd, dict):
                                cpu_net.load_state_dict(normalize_state_dict(sd))
                                cpu_net.eval()
                                last_sync_mtime = float(mtime)
                except Exception:
                    pass
            # ВАЖНО: повторяем init как в основном train-loop / _env_worker:
            # roll-off ролей + deploy_for_mission + post_deploy_setup.
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
            env.attacker_side = attacker_side
            env.defender_side = defender_side

            obs, _info = env.reset(options={"m": model, "e": enemy, "Type": "small", "trunc": trunc})
            done = False
            ep_reward = 0.0
            ep_len = 0
            last_info = {}
            last_res = 0
            # Стартовые HP — для грубой оценки damage_dealt/taken по эпизоду.
            try:
                if isinstance(_info, dict):
                    mh0 = _info.get("model health", [])
                    ph0 = _info.get("player health", [])
                    ep_model_hp_start = float(sum(mh0)) if isinstance(mh0, (list, tuple, np.ndarray)) else float(mh0 or 0.0)
                    ep_enemy_hp_start = float(sum(ph0)) if isinstance(ph0, (list, tuple, np.ndarray)) else float(ph0 or 0.0)
                else:
                    ep_model_hp_start = 0.0
                    ep_enemy_hp_start = 0.0
            except Exception:
                ep_model_hp_start = 0.0
                ep_enemy_hp_start = 0.0
            while not done:
                step_idx += 1
                shoot_mask = build_shoot_action_mask(env, log_fn=None, debug=False)
                decay_steps = max(1.0, float(EPS_DECAY))
                progress = min(float(steps_done) / decay_steps, 1.0)
                eps_threshold = EPS_START + (EPS_END - EPS_START) * progress
                action_t = select_action_with_epsilon(
                    env, obs, cpu_net, eps_threshold, len(model), shoot_mask=shoot_mask
                )
                action_dict = convertToDict(action_t)

                # --- episode action analytics (cheap) ---
                try:
                    for _h in ("move", "attack", "shoot", "charge", "use_cp", "cp_on"):
                        action_head_total[_h] += 1

                    move_dir = int(action_dict.get("move", 4))
                    if move_dir == 4:
                        move_stay += 1
                        action_head_skip["move"] += 1
                    else:
                        move_nonstay += 1

                    if int(action_dict.get("attack", 0)) == 0:
                        action_head_skip["attack"] += 1
                        action_head_skip["charge"] += 1
                    if int(action_dict.get("use_cp", 0)) == 0:
                        action_head_skip["use_cp"] += 1

                    valid_shoot_indices = []
                    if shoot_mask is not None:
                        try:
                            valid_shoot_indices = [j for j, allowed in enumerate(shoot_mask) if bool(allowed)]
                        except Exception:
                            valid_shoot_indices = []
                    if len(valid_shoot_indices) == 0:
                        shoot_windows_without_targets += 1
                        action_head_skip["shoot"] += 1
                    else:
                        shoot_windows_with_targets += 1
                        shoot_raw = int(action_dict.get("shoot", -1))
                        if shoot_raw not in valid_shoot_indices:
                            action_head_invalid["shoot"] += 1
                        else:
                            shoot_taken_when_targets += 1

                    if _trace_ep_enabled(ep_idx_1based) and len(trace_lines) < ACTION_TRACE_MAX_LINES_PER_EP:
                        trace_lines.append(
                            f"step={step_idx} eps={eps_threshold:.3f} "
                            f"move={move_dir} attack={int(action_dict.get('attack',0))} "
                            f"shoot={int(action_dict.get('shoot',-1))} charge={int(action_dict.get('charge',0))} "
                            f"use_cp={int(action_dict.get('use_cp',0))} cp_on={int(action_dict.get('cp_on',0))} "
                            f"shoot_targets={len(valid_shoot_indices)}"
                        )
                except Exception:
                    pass

                # ВАЖНО: как в основном train-loop — сначала ход противника, потом env.step (ход модели).
                env_unwrapped = unwrap_env(env)
                if opponent_policy_fn is not None:
                    env_unwrapped.enemyTurn(trunc=trunc, policy_fn=opponent_policy_fn)
                else:
                    env_unwrapped.enemyTurn(trunc=trunc)
                next_obs, reward, done, res, info2 = env.step(action_dict)
                last_info = info2 if isinstance(info2, dict) else {}
                last_res = res
                ep_reward += float(reward)
                ep_len += 1

                # Таймлайн по battle round (1 снапшот на BR).
                try:
                    if os.getenv("METRICS_SAVE_ROUND_TIMELINE", "1") == "1" and isinstance(last_info, dict):
                        br = int(last_info.get("battle round", 0) or 0)
                        if br > 0:
                            mh_now = last_info.get("model health", [])
                            ph_now = last_info.get("player health", [])
                            mh_sum = float(sum(mh_now)) if isinstance(mh_now, (list, tuple, np.ndarray)) else float(mh_now or 0.0)
                            ph_sum = float(sum(ph_now)) if isinstance(ph_now, (list, tuple, np.ndarray)) else float(ph_now or 0.0)
                            snap = {
                                "battle_round": br,
                                "turn": int(last_info.get("turn", 0) or 0),
                                "model_vp": int(last_info.get("model VP", 0) or 0),
                                "enemy_vp": int(last_info.get("player VP", 0) or 0),
                                "model_hp": mh_sum,
                                "enemy_hp": ph_sum,
                                "model_ctrl_n": int(len(last_info.get("model controlled objectives", []) or [])),
                                "enemy_ctrl_n": int(len(last_info.get("player controlled objectives", []) or [])),
                            }
                            replaced = False
                            for i in range(len(round_timeline)):
                                if int(round_timeline[i].get("battle_round", -1)) == br:
                                    round_timeline[i] = snap
                                    replaced = True
                                    break
                            if not replaced:
                                round_timeline.append(snap)
                except Exception:
                    pass

                r_clipped, _clipped = maybe_clip_reward(
                    float(reward), bool(clip_reward_enabled), float(clip_reward_min), float(clip_reward_max)
                )

                n_step_buf.append(
                    (
                        to_np_state(obs),
                        action_t.detach().cpu().numpy()[0].tolist(),
                        float(r_clipped),
                        to_np_state(next_obs),
                        bool(done),
                    )
                )

                if len(n_step_buf) >= N_STEP:
                    reward_sum = 0.0
                    n_count = 0
                    last_next = None
                    last_done = False
                    for idx, (_s, _a, rr, ns, dd) in enumerate(n_step_buf):
                        reward_sum += (GAMMA ** idx) * float(rr)
                        n_count += 1
                        last_next = ns
                        last_done = bool(dd)
                        if dd:
                            last_next = None
                            break
                    head_s, head_a, _, _, _ = n_step_buf[0]
                    buf.append((head_s, head_a, reward_sum, last_next, last_done, n_count))
                    n_step_buf.popleft()

                if done:
                    while n_step_buf:
                        reward_sum = 0.0
                        n_count = 0
                        for idx, (_s, _a, rr, _ns, dd) in enumerate(n_step_buf):
                            reward_sum += (GAMMA ** idx) * float(rr)
                            n_count += 1
                            if dd:
                                break
                        head_s, head_a, _, _, _ = n_step_buf[0]
                        buf.append((head_s, head_a, reward_sum, None, True, n_count))
                        n_step_buf.popleft()

                obs = next_obs
                steps_done += 1

                if len(buf) >= int(batch_send):
                    data_q.put(("batch", buf))
                    buf = []

            # Эпизод завершён: отправляем компактную строку метрик (как в обычном режиме)
            try:
                end_reason = str(last_info.get("end reason", "") or "")
                model_vp = int(last_info.get("model VP", 0) or 0)
                player_vp = int(last_info.get("player VP", 0) or 0)
                vp_diff = int(model_vp) - int(player_vp)
                turn = int(last_info.get("turn", 0) or 0)
                battle_round = int(last_info.get("battle round", 0) or 0)

                # Итоговые HP/урон
                mh_end = last_info.get("model health", [])
                ph_end = last_info.get("player health", [])
                mh_sum = float(sum(mh_end)) if isinstance(mh_end, (list, tuple, np.ndarray)) else float(mh_end or 0.0)
                ph_sum = float(sum(ph_end)) if isinstance(ph_end, (list, tuple, np.ndarray)) else float(ph_end or 0.0)
                damage_taken_total = max(0.0, float(ep_model_hp_start) - float(mh_sum))
                damage_dealt_total = max(0.0, float(ep_enemy_hp_start) - float(ph_sum))

                model_ctrl = last_info.get("model controlled objectives", []) if isinstance(last_info, dict) else []
                enemy_ctrl = last_info.get("player controlled objectives", []) if isinstance(last_info, dict) else []
                model_ctrl = list(model_ctrl) if isinstance(model_ctrl, (list, tuple)) else []
                enemy_ctrl = list(enemy_ctrl) if isinstance(enemy_ctrl, (list, tuple)) else []

                result = "loss"
                if end_reason == "wipeout_enemy":
                    result = "win"
                elif end_reason == "wipeout_model":
                    result = "loss"
                elif str(end_reason).startswith("turn_limit"):
                    if vp_diff > 0:
                        result = "win"
                    elif vp_diff == 0:
                        result = "draw"
                else:
                    if vp_diff > 0:
                        result = "win"
                    elif vp_diff == 0:
                        result = "draw"

                # Защита от явно подозрительных "побед" (обычно признак сломанного протокола).
                if result == "win" and end_reason == "wipeout_enemy" and model_vp == 0 and player_vp == 0 and turn <= 0:
                    end_reason = "suspicious_wipeout_enemy"
                    result = "draw"

                data_q.put(
                    (
                        "ep",
                        {
                            "episode": None,  # learner пронумерует по порядку
                            "actor_idx": int(actor_idx),
                            "actor_ep": int(ep_idx_1based),
                            "ep_reward": float(ep_reward),
                            "ep_len": int(ep_len),
                            "turn": int(turn),
                            "model_vp": int(model_vp),
                            "player_vp": int(player_vp),
                            "vp_diff": int(vp_diff),
                            "result": str(result),
                            "end_reason": str(end_reason),
                            "end_code": int(last_res),
                            "battle_round": int(battle_round),
                            "model_hp_total": float(mh_sum),
                            "enemy_hp_total": float(ph_sum),
                            "damage_dealt_total": float(damage_dealt_total),
                            "damage_taken_total": float(damage_taken_total),
                            "model_ctrl": list(model_ctrl),
                            "enemy_ctrl": list(enemy_ctrl),
                            "model_ctrl_n": int(len(model_ctrl)),
                            "enemy_ctrl_n": int(len(enemy_ctrl)),
                            "timeline": list(round_timeline) if os.getenv("METRICS_SAVE_ROUND_TIMELINE", "1") == "1" else [],
                            "trace_steps": list(trace_lines) if (_trace_ep_enabled(ep_idx_1based) and trace_lines) else None,
                            "trace_actions": {
                                "steps": int(max(1, int(ep_len))),
                                "skip": {k: int(action_head_skip.get(k, 0)) for k in ("move","attack","shoot","charge","use_cp","cp_on")},
                                "invalid": {k: int(action_head_invalid.get(k, 0)) for k in ("move","attack","shoot","charge","use_cp","cp_on")},
                                "skip_rate": {k: float(action_head_skip.get(k, 0)) / float(max(1, int(ep_len))) for k in ("move","attack","shoot","charge","use_cp","cp_on")},
                                "invalid_rate": {k: float(action_head_invalid.get(k, 0)) / float(max(1, int(ep_len))) for k in ("move","attack","shoot","charge","use_cp","cp_on")},
                                "shoot_windows": {"with_targets": int(shoot_windows_with_targets), "without_targets": int(shoot_windows_without_targets)},
                                "shoot_taken_when_targets": int(shoot_taken_when_targets),
                                "move": {"stay": int(move_stay), "nonstay": int(move_nonstay)},
                            },
                        },
                    )
                )
            except Exception:
                pass

        if buf:
            data_q.put(("batch", buf))
        data_q.put(("done", int(actor_idx)))
    except Exception as exc:
        try:
            data_q.put(("error", f"actor[{actor_idx}] {exc}"))
        except Exception:
            pass


def _actor_learner_actor_entry_ppo(
    actor_idx: int,
    episodes: int,
    roster_config: dict,
    b_len: int,
    b_hei: int,
    n_observations: int,
    n_actions: list,
    init_weights: dict,
    batch_send: int,
    clip_reward_min: float,
    clip_reward_max: float,
    clip_reward_enabled: bool,
    data_q,
):
    """Top-level entrypoint for Windows spawn pickling (PPO actor)."""
    try:
        cpu_net = make_actor_critic(n_observations, n_actions).to(torch.device("cpu"))
        cpu_net.load_state_dict(init_weights, strict=False)
        cpu_net.eval()

        trunc = True
        enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
        mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
        env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)

        sync_enabled = os.getenv("ACTOR_SYNC_ENABLED", "1") == "1"
        sync_path = os.path.join(MODELS_DIR, "actor_sync", "latest_ppo.pth")
        sync_check_every_ep = max(1, int(os.getenv("ACTOR_SYNC_CHECK_EVERY_EP", "5")))
        last_sync_mtime = -1.0

        opponent_policy_fn = None
        # 1) Explicit opponent via registry (supports cross-algo)
        if int(SELF_PLAY_ENABLED) == 1 and OPPONENT_AGENT_ID:
            try:
                opp_spec = load_agent_opponent(agent_id=OPPONENT_AGENT_ID)
                opponent_policy_fn = build_policy_fn(env=env, len_model=len(model), opponent=opp_spec, deterministic=True)
            except Exception:
                opponent_policy_fn = None
        # 2) Fallback: PPO snapshot sync file (PPO vs PPO), if explicit not set
        opp_sync_path = os.path.join(MODELS_DIR, "actor_sync", "latest_ppo_opp.pth")
        last_opp_sync_mtime = -1.0
        opponent_net = make_actor_critic(n_observations, n_actions).to(torch.device("cpu"))
        opponent_net.eval()
        opponent_loaded = False

        # ordered_keys локально (для action_dict)
        ordered_keys = ["move", "attack", "shoot", "charge", "use_cp", "cp_on"]
        for i_u in range(len(model)):
            ordered_keys.append(f"move_num_{i_u}")

        steps_buf: list[dict] = []

        for _ep in range(int(episodes)):
            ep_idx_1based = int(_ep) + 1
            if sync_enabled and (_ep % sync_check_every_ep == 0):
                try:
                    if os.path.isfile(sync_path):
                        mtime = os.path.getmtime(sync_path)
                        if mtime > last_sync_mtime:
                            payload = torch.load(sync_path, map_location="cpu", weights_only=False)
                            sd = payload.get("state_dict") if isinstance(payload, dict) else None
                            if isinstance(sd, dict):
                                cpu_net.load_state_dict(normalize_state_dict(sd))
                                cpu_net.eval()
                                last_sync_mtime = float(mtime)
                except Exception:
                    pass

            # Обновление оппонента для self-play через sync-файл (если снапшот появился)
            if opponent_policy_fn is None and int(SELF_PLAY_ENABLED) == 1 and (_ep % sync_check_every_ep == 0):
                try:
                    if os.path.isfile(opp_sync_path):
                        mtime = os.path.getmtime(opp_sync_path)
                        if mtime > last_opp_sync_mtime:
                            payload = torch.load(opp_sync_path, map_location="cpu", weights_only=False)
                            sd = payload.get("state_dict") if isinstance(payload, dict) else None
                            if isinstance(sd, dict):
                                opponent_net.load_state_dict(normalize_state_dict(sd))
                                opponent_net.eval()
                                opponent_loaded = True
                                last_opp_sync_mtime = float(mtime)
                except Exception:
                    pass

            # roll-off + deploy как в остальных пайплайнах
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
            env.attacker_side = attacker_side
            env.defender_side = defender_side

            obs, info0 = env.reset(options={"m": model, "e": enemy, "Type": "small", "trunc": trunc})
            done = False
            ep_reward = 0.0
            ep_len = 0
            last_info = info0 if isinstance(info0, dict) else {}
            last_res = 0

            while not done:
                env_unwrapped = unwrap_env(env)
                if opponent_policy_fn is not None:
                    env_unwrapped.enemyTurn(trunc=trunc, policy_fn=opponent_policy_fn)
                elif int(SELF_PLAY_ENABLED) == 1 and opponent_loaded:
                    # PPO-vs-PPO fallback (sync-file), deterministic
                    def _ppo_opp_policy_fn(obs_opp, env=env, net=opponent_net, lm=len(model), n_actions=n_actions):
                        obs_np_local = to_np_state(obs_opp)
                        obs_t_local = torch.tensor(obs_np_local, dtype=torch.float32, device=torch.device("cpu")).unsqueeze(0)
                        shoot_mask_local = build_shoot_action_mask(env, log_fn=None, debug=False)
                        masks_local = []
                        for head_idx, head_size in enumerate(n_actions):
                            if head_idx == 2 and shoot_mask_local is not None:
                                mask_arr = np.asarray(shoot_mask_local, dtype=np.bool_).reshape(-1)
                                if mask_arr.size == int(head_size) and bool(mask_arr.any()):
                                    masks_local.append(mask_arr)
                                    continue
                            masks_local.append(np.ones(int(head_size), dtype=np.bool_))
                        masks_batch_local = [torch.tensor(m, dtype=torch.bool, device=torch.device("cpu")).unsqueeze(0) for m in masks_local]
                        with torch.no_grad():
                            act_t, _logp_t, _val_t = net.act(obs_t_local, masks_by_head=masks_batch_local, deterministic=True)
                        act_np = act_t.squeeze(0).detach().cpu().numpy()
                        act_dict = convertToDict(torch.tensor([act_np], device="cpu"))
                        for i_u in range(int(lm)):
                            act_dict[f"move_num_{i_u}"] = int(act_np[6 + i_u])
                        return act_dict

                    env_unwrapped.enemyTurn(trunc=trunc, policy_fn=_ppo_opp_policy_fn)
                else:
                    env_unwrapped.enemyTurn(trunc=trunc)

                if bool(getattr(env_unwrapped, "game_over", False)):
                    done = True
                    if hasattr(env_unwrapped, "get_info"):
                        last_info = env_unwrapped.get_info() or last_info
                    break

                obs_np = to_np_state(obs)
                obs_t = torch.tensor(obs_np, dtype=torch.float32, device=torch.device("cpu")).unsqueeze(0)

                # маски: strict для shoot, остальные all_true
                shoot_mask = build_shoot_action_mask(env, log_fn=None, debug=False)
                masks_cpu = []
                for head_idx, head_size in enumerate(n_actions):
                    if head_idx == 2 and shoot_mask is not None:
                        mask_arr = np.asarray(shoot_mask, dtype=np.bool_).reshape(-1)
                        if mask_arr.size == int(head_size) and bool(mask_arr.any()):
                            masks_cpu.append(mask_arr)
                            continue
                    masks_cpu.append(np.ones(int(head_size), dtype=np.bool_))
                masks_batch = [torch.tensor(m, dtype=torch.bool, device=torch.device("cpu")).unsqueeze(0) for m in masks_cpu]

                with torch.no_grad():
                    action_t, logprob_t, value_t = cpu_net.act(obs_t, masks_by_head=masks_batch, deterministic=False)
                action_np = action_t.squeeze(0).detach().cpu().numpy()

                action_dict = convertToDict(torch.tensor([action_np], device="cpu"))
                for i_u in range(len(model)):
                    action_dict[f"move_num_{i_u}"] = int(action_np[6 + i_u])

                next_obs, reward, done, res, info2 = env.step(action_dict)
                last_info = info2 if isinstance(info2, dict) else last_info
                last_res = res

                r_clipped, _clipped = maybe_clip_reward(
                    float(reward), bool(clip_reward_enabled), float(clip_reward_min), float(clip_reward_max)
                )
                steps_buf.append(
                    {
                        "obs": obs_np,
                        "action": action_np.tolist(),
                        "logprob": float(logprob_t.squeeze(0).item()),
                        "value": float(value_t.squeeze(0).item()),
                        "reward": float(r_clipped),
                        "done": bool(done),
                        "masks_by_head": masks_cpu,
                    }
                )

                ep_reward += float(reward)
                ep_len += 1
                obs = next_obs

                if len(steps_buf) >= int(batch_send):
                    data_q.put(("rollout", {"actor_idx": int(actor_idx), "steps": steps_buf}))
                    steps_buf = []

            # flush remaining steps at episode end
            if steps_buf:
                data_q.put(("rollout", {"actor_idx": int(actor_idx), "steps": steps_buf}))
                steps_buf = []

            # episode row
            try:
                end_reason = str(last_info.get("end reason", "") or "")
                model_vp = int(last_info.get("model VP", 0) or 0)
                player_vp = int(last_info.get("player VP", 0) or 0)
                vp_diff = int(model_vp) - int(player_vp)
                turn = int(last_info.get("turn", 0) or 0)

                result = "loss"
                if end_reason == "wipeout_enemy":
                    result = "win"
                elif end_reason == "wipeout_model":
                    result = "loss"
                elif str(end_reason).startswith("turn_limit"):
                    if vp_diff > 0:
                        result = "win"
                    elif vp_diff == 0:
                        result = "draw"
                else:
                    if vp_diff > 0:
                        result = "win"
                    elif vp_diff == 0:
                        result = "draw"

                data_q.put(
                    (
                        "ep",
                        {
                            "episode": None,
                            "actor_idx": int(actor_idx),
                            "actor_ep": int(ep_idx_1based),
                            "ep_reward": float(ep_reward),
                            "ep_len": int(ep_len),
                            "turn": int(turn),
                            "model_vp": int(model_vp),
                            "player_vp": int(player_vp),
                            "vp_diff": int(vp_diff),
                            "result": str(result),
                            "end_reason": str(end_reason),
                            "end_code": int(last_res),
                        },
                    )
                )
            except Exception:
                pass

        data_q.put(("done", int(actor_idx)))
    except Exception as exc:
        try:
            data_q.put(("error", f"ppo_actor[{actor_idx}] {exc}"))
        except Exception:
            pass


def _actor_learner_actor_entry_alphazero(
    actor_idx: int,
    episodes: int,
    roster_config: dict,
    b_len: int,
    b_hei: int,
    n_observations: int,
    n_actions: list,
    init_weights: dict,
    batch_send: int,
    data_q,
    self_play_enabled: int,
    opponent_spec,
    sp_cfg_payload: dict,
    mcts_cfg_payload: dict,
    outcome_payload: dict,
    rollout_sink_mode: str = "local",
    rollout_source: str = "local",
    rollout_remote_host: str = "",
    rollout_remote_port: int = 5557,
    rollout_remote_auth_token: str = "",
    env_contract_hash: str = "",
    dist_stop_flag_path: str = "",
):
    """Top-level entrypoint for Windows spawn pickling (AlphaZero actor)."""
    import itertools

    try:
        sink = make_rollout_sink(
            mode=rollout_sink_mode,
            data_q=data_q,
            source=rollout_source,
            remote_host=rollout_remote_host,
            remote_port=int(rollout_remote_port),
            auth_token=rollout_remote_auth_token,
            worker_id=int(actor_idx),
            env_contract_hash=str(env_contract_hash or ""),
        )
        cpu_device = torch.device("cpu")
        az_kw = alphazero_kwargs_from_env()
        az_net = make_alphazero_net(n_observations=n_observations, n_actions=n_actions, **az_kw).to(cpu_device)
        load_alphazero_state_dict(az_net, normalize_state_dict(init_weights))
        az_net.eval()
        mcts = AlphaZeroFactorizedMCTS(
            az_net,
            config=MCTSConfig(
                simulations=int(mcts_cfg_payload.get("simulations", AZ_MCTS_SIMS)),
                c_puct=float(mcts_cfg_payload.get("c_puct", AZ_C_PUCT)),
                c_puct_min=float(mcts_cfg_payload.get("c_puct_min", AZ_C_PUCT_MIN)),
                c_puct_max=float(mcts_cfg_payload.get("c_puct_max", AZ_C_PUCT_MAX)),
                c_puct_schedule=str(mcts_cfg_payload.get("c_puct_schedule", AZ_C_PUCT_SCHEDULE)),
                dirichlet_alpha=float(mcts_cfg_payload.get("dirichlet_alpha", AZ_DIR_ALPHA)),
                dirichlet_eps=float(mcts_cfg_payload.get("dirichlet_eps", AZ_DIR_EPS)),
                top_k_per_head=int(mcts_cfg_payload.get("top_k_per_head", AZ_MCTS_TOP_K_PER_HEAD)),
                max_depth=int(mcts_cfg_payload.get("max_depth", AZ_MCTS_MAX_DEPTH)),
                mode=str(mcts_cfg_payload.get("mode", AZ_MCTS_MODE)),
                root_dirichlet_only=bool(mcts_cfg_payload.get("root_dirichlet_only", AZ_MCTS_ROOT_DIRICHLET_ONLY)),
                eval_cache_size=int(mcts_cfg_payload.get("eval_cache_size", AZ_MCTS_EVAL_CACHE_SIZE)),
                pw_alpha=float(mcts_cfg_payload.get("pw_alpha", AZ_PW_ALPHA)),
                pw_beta=float(mcts_cfg_payload.get("pw_beta", AZ_PW_BETA)),
                prior_weight_early=float(mcts_cfg_payload.get("prior_weight_early", AZ_PRIOR_WEIGHT_EARLY)),
                temperature_opening_moves=int(sp_cfg_payload.get("temperature_opening_moves", AZ_TEMP_OPENING_MOVES)),
                batch_eval_size=int(mcts_cfg_payload.get("batch_eval_size", AZ_MCTS_BATCH_EVAL_SIZE)),
                parallel_simulations=int(mcts_cfg_payload.get("parallel_simulations", AZ_MCTS_PARALLEL_SIMS)),
                simulate_enemy_in_tree=bool(mcts_cfg_payload.get("simulate_enemy_in_tree", AZ_MCTS_SIMULATE_ENEMY)),
            ),
            device=cpu_device,
        )
        sp_cfg = SelfPlayConfig(
            temperature_opening_moves=int(sp_cfg_payload.get("temperature_opening_moves", AZ_TEMP_OPENING_MOVES)),
            temperature_opening_value=float(sp_cfg_payload.get("temperature_opening_value", AZ_TEMP_OPENING)),
            temperature_late_value=float(sp_cfg_payload.get("temperature_late_value", AZ_TEMP_LATE)),
        )

        enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
        mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
        env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
        len_model = int(len(model))

        sync_enabled = os.getenv("ACTOR_SYNC_ENABLED", "1") == "1"
        # Путь sync должен совпадать с тем, что пишет learner (_save_az_sync, train.py ~8377):
        # learner использует тег tree/proxy по TRAIN_ALGO. Раньше актор читал untagged
        # "latest_az_policy.pth" → файл не находился, ACTOR_SYNC молча no-op (веса не обновлялись).
        _az_sync_tag = "tree" if TRAIN_ALGO == "alphazero_tree" else "proxy"
        sync_path = os.path.join(MODELS_DIR, "actor_sync", f"latest_az_{_az_sync_tag}_policy.pth")
        sync_check_every_ep = max(1, int(os.getenv("ACTOR_SYNC_CHECK_EVERY_EP", "5")))
        last_sync_mtime = -1.0
        current_policy_version = int(outcome_payload.get("policy_version", 0) or 0)

        opponent_policy_fn = None
        if int(self_play_enabled) == 1 and opponent_spec is not None:
            try:
                opponent_policy_fn = build_policy_fn(
                    env=env,
                    len_model=len_model,
                    opponent=opponent_spec,
                    deterministic=bool(AZ_SNAPSHOT_OPP_DETERMINISTIC),
                )
            except Exception:
                opponent_policy_fn = None

        rollout_batch: list[dict] = []
        heartbeat_moves = max(1, int(os.getenv("AZ_ACTOR_HEARTBEAT_MOVES", "5") or 5))
        ep_limit = int(episodes)
        ep_iter = range(ep_limit) if ep_limit > 0 else itertools.count()
        for _ep in ep_iter:
            if dist_stop_flag_path and az_dist_stop_requested(dist_stop_flag_path):
                append_agent_log(f"[AZ][ACTOR] actor={int(actor_idx)} stop.flag — выход")
                break
            ep_idx_1based = int(_ep) + 1 if ep_limit > 0 else int(_ep) + 1
            ep_total_label = str(ep_limit) if ep_limit > 0 else "open"
            print(
                f"[AZ][ACTOR] actor={int(actor_idx)} local_ep={ep_idx_1based}/{ep_total_label} starting "
                f"mcts_mode={getattr(mcts.cfg, 'mode', 'proxy')} sims={getattr(mcts.cfg, 'simulations', 0)}",
                flush=True,
            )
            if sync_enabled and (_ep % sync_check_every_ep == 0):
                try:
                    if os.path.isfile(sync_path):
                        mtime = os.path.getmtime(sync_path)
                        if mtime > last_sync_mtime:
                            payload = torch.load(sync_path, map_location="cpu", weights_only=False)
                            sd = payload.get("state_dict") if isinstance(payload, dict) else None
                            if isinstance(sd, dict):
                                load_alphazero_state_dict(az_net, normalize_state_dict(sd))
                                az_net.eval()
                                mcts.net = az_net
                                last_sync_mtime = float(mtime)
                                current_policy_version = int(payload.get("policy_version", current_policy_version) or current_policy_version)
                                append_agent_log(
                                    f"[AZ][ACTOR] weight_sync actor={int(actor_idx)} "
                                    f"version={current_policy_version} file={os.path.basename(sync_path)}"
                                )
                except Exception:
                    pass

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
            env.attacker_side = attacker_side
            env.defender_side = defender_side

            transitions, info = play_episode_with_mcts(
                env=env,
                mcts=mcts,
                len_model=len_model,
                config=sp_cfg,
                enemy_policy_fn=opponent_policy_fn,
                outcome_only=bool(outcome_payload.get("outcome_only", AZ_OUTCOME_ONLY)),
                outcome_value_win=float(outcome_payload.get("outcome_value_win", AZ_OUTCOME_VALUE_WIN)),
                outcome_value_loss=float(outcome_payload.get("outcome_value_loss", AZ_OUTCOME_VALUE_LOSS)),
                outcome_value_draw=float(outcome_payload.get("outcome_value_draw", AZ_OUTCOME_VALUE_DRAW)),
                policy_version=int(current_policy_version),
                actor_idx=int(actor_idx),
                heartbeat_moves=heartbeat_moves,
            )
            for t in transitions:
                rollout_batch.append(
                    {
                        "state": np.asarray(t.state, dtype=np.float32),
                        "policy_targets": [np.asarray(p, dtype=np.float32) for p in t.policy_targets],
                        "value_target": float(t.value_target),
                        "policy_version": int(getattr(t, "policy_version", current_policy_version)),
                    }
                )
            if len(rollout_batch) >= int(batch_send):
                sink.put(
                    "rollout",
                    {
                        "actor_idx": int(actor_idx),
                        "policy_version": int(current_policy_version),
                        "env_contract_hash": str(env_contract_hash or ""),
                        "transitions": list(rollout_batch),
                    },
                )
                rollout_batch = []

            info = dict(info or {})
            end_reason = str(info.get("end reason", "") or "")
            model_vp = int(info.get("model VP", 0) or 0)
            player_vp = int(info.get("player VP", 0) or 0)
            vp_diff = int(model_vp) - int(player_vp)
            result = "loss"
            if end_reason == "wipeout_enemy":
                result = "win"
            elif end_reason == "wipeout_model":
                result = "loss"
            elif str(end_reason).startswith("turn_limit"):
                if vp_diff > 0:
                    result = "win"
                elif vp_diff == 0:
                    result = "draw"
            elif vp_diff > 0:
                result = "win"
            elif vp_diff == 0:
                result = "draw"
            sink.put(
                "ep",
                {
                    "episode": None,
                    "actor_idx": int(actor_idx),
                    "actor_ep": int(ep_idx_1based),
                    "ep_reward": float(info.get("reward", 0.0) or 0.0),
                    "ep_len": int(info.get("turn", 0) or 0),
                    "turn": int(info.get("turn", 0) or 0),
                    "model_vp": int(model_vp),
                    "player_vp": int(player_vp),
                    "vp_diff": int(vp_diff),
                    "result": str(result),
                    "end_reason": str(end_reason),
                    "end_code": int(info.get("res", 0) or 0),
                    "policy_version": int(current_policy_version),
                },
            )

        if rollout_batch:
            sink.put(
                "rollout",
                {
                    "actor_idx": int(actor_idx),
                    "policy_version": int(current_policy_version),
                    "env_contract_hash": str(env_contract_hash or ""),
                    "transitions": list(rollout_batch),
                },
            )
        if str(rollout_sink_mode or "local").strip().lower() != "remote":
            data_q.put(("done", int(actor_idx)))
    except Exception as exc:
        try:
            if "sink" in locals():
                sink.put("error", f"az_actor[{actor_idx}] {exc}")
            else:
                data_q.put(("error", f"az_actor[{actor_idx}] {exc}"))
        except Exception:
            pass
    finally:
        try:
            if "sink" in locals():
                sink.close()
        except Exception:
            pass


def _az_env_worker_entry(
    worker_id: int,
    episodes: int,
    roster_config: dict,
    b_len: int,
    b_hei: int,
    batch_send: int,
    data_q,
    request_q,
    reply_q,
    self_play_enabled: int,
    opponent_spec,
    sp_cfg_payload: dict,
    mcts_cfg_payload: dict,
    outcome_payload: dict,
    inference_timeout: float,
    inference_server_mode: str = "local",
    remote_host: str = "",
    remote_port: int = 5555,
    remote_auth_token: str = "",
    rollout_sink_mode: str = "local",
    rollout_source: str = "local",
    rollout_remote_host: str = "",
    rollout_remote_port: int = 5557,
    rollout_remote_auth_token: str = "",
    env_contract_hash: str = "",
    dist_stop_flag_path: str = "",
):
    """CPU env worker для AZ IS (variant B): env + MCTS + RemoteEvaluator → data_q."""
    import itertools

    try:
        sink = make_rollout_sink(
            mode=rollout_sink_mode,
            data_q=data_q,
            source=rollout_source,
            remote_host=rollout_remote_host,
            remote_port=int(rollout_remote_port),
            auth_token=rollout_remote_auth_token,
            worker_id=int(worker_id),
            env_contract_hash=str(env_contract_hash or ""),
        )
        from core.models.az_inference_client import RemoteEvaluator
        from core.models.az_inference_transport import make_az_transport

        mode = str(inference_server_mode or "local").strip().lower()
        transport = make_az_transport(
            mode,
            request_q=request_q,
            reply_q=reply_q,
            worker_id=int(worker_id),
            host=str(remote_host or "127.0.0.1"),
            port=int(remote_port),
            auth_token=str(remote_auth_token or ""),
        )
        evaluator = RemoteEvaluator(
            worker_id=int(worker_id),
            transport=transport,
            timeout=float(inference_timeout),
            auth_token=str(remote_auth_token or ""),
        )
        if mode == "remote":
            append_agent_log(
                f"[AZ][REMOTE_CLIENT][CONN] worker={int(worker_id)} "
                f"tcp://{remote_host}:{int(remote_port)}"
            )

        mcts = AlphaZeroFactorizedMCTS(
            None,  # net не используется — всё через evaluator
            config=MCTSConfig(
                simulations=int(mcts_cfg_payload.get("simulations", AZ_MCTS_SIMS)),
                c_puct=float(mcts_cfg_payload.get("c_puct", AZ_C_PUCT)),
                c_puct_min=float(mcts_cfg_payload.get("c_puct_min", AZ_C_PUCT_MIN)),
                c_puct_max=float(mcts_cfg_payload.get("c_puct_max", AZ_C_PUCT_MAX)),
                c_puct_schedule=str(mcts_cfg_payload.get("c_puct_schedule", AZ_C_PUCT_SCHEDULE)),
                dirichlet_alpha=float(mcts_cfg_payload.get("dirichlet_alpha", AZ_DIR_ALPHA)),
                dirichlet_eps=float(mcts_cfg_payload.get("dirichlet_eps", AZ_DIR_EPS)),
                top_k_per_head=int(mcts_cfg_payload.get("top_k_per_head", AZ_MCTS_TOP_K_PER_HEAD)),
                max_depth=int(mcts_cfg_payload.get("max_depth", AZ_MCTS_MAX_DEPTH)),
                mode=str(mcts_cfg_payload.get("mode", AZ_MCTS_MODE)),
                root_dirichlet_only=bool(mcts_cfg_payload.get("root_dirichlet_only", AZ_MCTS_ROOT_DIRICHLET_ONLY)),
                eval_cache_size=int(mcts_cfg_payload.get("eval_cache_size", AZ_MCTS_EVAL_CACHE_SIZE)),
                pw_alpha=float(mcts_cfg_payload.get("pw_alpha", AZ_PW_ALPHA)),
                pw_beta=float(mcts_cfg_payload.get("pw_beta", AZ_PW_BETA)),
                prior_weight_early=float(mcts_cfg_payload.get("prior_weight_early", AZ_PRIOR_WEIGHT_EARLY)),
                temperature_opening_moves=int(sp_cfg_payload.get("temperature_opening_moves", AZ_TEMP_OPENING_MOVES)),
                batch_eval_size=int(mcts_cfg_payload.get("batch_eval_size", AZ_MCTS_BATCH_EVAL_SIZE)),
                parallel_simulations=int(mcts_cfg_payload.get("parallel_simulations", AZ_MCTS_PARALLEL_SIMS)),
                simulate_enemy_in_tree=bool(mcts_cfg_payload.get("simulate_enemy_in_tree", AZ_MCTS_SIMULATE_ENEMY)),
            ),
            device=torch.device("cpu"),
            evaluator=evaluator,
        )
        sp_cfg = SelfPlayConfig(
            temperature_opening_moves=int(sp_cfg_payload.get("temperature_opening_moves", AZ_TEMP_OPENING_MOVES)),
            temperature_opening_value=float(sp_cfg_payload.get("temperature_opening_value", AZ_TEMP_OPENING)),
            temperature_late_value=float(sp_cfg_payload.get("temperature_late_value", AZ_TEMP_LATE)),
        )

        enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
        mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
        env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
        len_model = int(len(model))

        opponent_policy_fn = None
        if int(self_play_enabled) == 1 and opponent_spec is not None:
            try:
                opponent_policy_fn = build_policy_fn(
                    env=env,
                    len_model=len_model,
                    opponent=opponent_spec,
                    deterministic=bool(AZ_SNAPSHOT_OPP_DETERMINISTIC),
                )
            except Exception:
                opponent_policy_fn = None

        current_policy_version = int(outcome_payload.get("policy_version", 0) or 0)
        rollout_batch: list[dict] = []
        heartbeat_moves = max(1, int(os.getenv("AZ_ACTOR_HEARTBEAT_MOVES", "5") or 5))

        ep_limit = int(episodes)
        ep_total_label = str(ep_limit) if ep_limit > 0 else "open"
        append_agent_log(
            f"[AZ][ENV_WORKER] worker={int(worker_id)} started episodes={ep_total_label} "
            f"rollout_sink={rollout_sink_mode}"
        )
        ep_iter = range(ep_limit) if ep_limit > 0 else itertools.count()
        for _ep in ep_iter:
            if dist_stop_flag_path and az_dist_stop_requested(dist_stop_flag_path):
                append_agent_log(f"[AZ][ENV_WORKER] worker={int(worker_id)} stop.flag — выход")
                break
            ep_idx_1based = int(_ep) + 1
            print(
                f"[AZ][ENV_WORKER] worker={int(worker_id)} local_ep={ep_idx_1based}/{ep_total_label} starting",
                flush=True,
            )
            attacker_side, defender_side = roll_off_attacker_defender(manual_roll_allowed=False, log_fn=None)
            deploy_for_mission(
                mission_name, model_units=model, enemy_units=enemy,
                b_len=b_len, b_hei=b_hei,
                attacker_side=attacker_side, log_fn=None,
            )
            post_deploy_setup(log_fn=None)
            env.attacker_side = attacker_side
            env.defender_side = defender_side

            transitions, info = play_episode_with_mcts(
                env=env,
                mcts=mcts,
                len_model=len_model,
                config=sp_cfg,
                enemy_policy_fn=opponent_policy_fn,
                outcome_only=bool(outcome_payload.get("outcome_only", AZ_OUTCOME_ONLY)),
                outcome_value_win=float(outcome_payload.get("outcome_value_win", AZ_OUTCOME_VALUE_WIN)),
                outcome_value_loss=float(outcome_payload.get("outcome_value_loss", AZ_OUTCOME_VALUE_LOSS)),
                outcome_value_draw=float(outcome_payload.get("outcome_value_draw", AZ_OUTCOME_VALUE_DRAW)),
                policy_version=int(current_policy_version),
                actor_idx=int(worker_id),
                heartbeat_moves=heartbeat_moves,
            )

            # Подхватываем policy_version из последнего ответа IS (через evaluator)
            if hasattr(evaluator, "_last_policy_version"):
                current_policy_version = int(evaluator._last_policy_version)

            for t in transitions:
                rollout_batch.append({
                    "state": np.asarray(t.state, dtype=np.float32),
                    "policy_targets": [np.asarray(p, dtype=np.float32) for p in t.policy_targets],
                    "value_target": float(t.value_target),
                    "policy_version": int(getattr(t, "policy_version", current_policy_version)),
                })
            if len(rollout_batch) >= int(batch_send):
                sink.put(
                    "rollout",
                    {
                        "actor_idx": int(worker_id),
                        "policy_version": int(current_policy_version),
                        "env_contract_hash": str(env_contract_hash or ""),
                        "transitions": list(rollout_batch),
                    },
                )
                rollout_batch = []

            info = dict(info or {})
            end_reason = str(info.get("end reason", "") or "")
            model_vp = int(info.get("model VP", 0) or 0)
            player_vp = int(info.get("player VP", 0) or 0)
            vp_diff = int(model_vp) - int(player_vp)
            result = "loss"
            if end_reason == "wipeout_enemy":
                result = "win"
            elif end_reason == "wipeout_model":
                result = "loss"
            elif str(end_reason).startswith("turn_limit"):
                result = "win" if vp_diff > 0 else ("draw" if vp_diff == 0 else "loss")
            elif vp_diff > 0:
                result = "win"
            elif vp_diff == 0:
                result = "draw"
            sink.put(
                "ep",
                {
                    "episode": None,
                    "actor_idx": int(worker_id),
                    "actor_ep": int(ep_idx_1based),
                    "ep_reward": float(info.get("reward", 0.0) or 0.0),
                    "ep_len": int(info.get("turn", 0) or 0),
                    "turn": int(info.get("turn", 0) or 0),
                    "model_vp": int(model_vp),
                    "player_vp": int(player_vp),
                    "vp_diff": int(vp_diff),
                    "result": str(result),
                    "end_reason": str(end_reason),
                    "end_code": int(info.get("res", 0) or 0),
                    "policy_version": int(current_policy_version),
                },
            )

        if rollout_batch:
            sink.put(
                "rollout",
                {
                    "actor_idx": int(worker_id),
                    "policy_version": int(current_policy_version),
                    "env_contract_hash": str(env_contract_hash or ""),
                    "transitions": list(rollout_batch),
                },
            )
        if str(rollout_sink_mode or "local").strip().lower() != "remote":
            data_q.put(("done", int(worker_id)))
        evaluator.close()
    except Exception as exc:
        try:
            if "sink" in locals():
                sink.put("error", f"az_env_worker[{worker_id}] {exc}")
            else:
                data_q.put(("error", f"az_env_worker[{worker_id}] {exc}"))
        except Exception:
            pass
    finally:
        try:
            if "sink" in locals():
                sink.close()
        except Exception:
            pass


def _main_actor_learner_alphazero(*, roster_config, totLifeT, clip_reward_enabled, clip_reward_min, clip_reward_max) -> None:
    """
    AlphaZero actor-learner (quality-first):
    - actors (CPU) генерируют self-play эпизоды через MCTS,
    - learner (GPU/CPU) читает rollout-и, обновляет net и sync-ит веса акторам.
    """
    b_len = int(roster_config["b_len"])
    b_hei = int(roster_config["b_hei"])
    run_id = str(random.randint(1000000, 9999999))
    model_name = datetime.datetime.now().strftime("%d-%H%M%S")
    metrics_obj = metrics(MODELS_DIR, run_id, model_name)

    # bootstrap env for contracts/sizes
    enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
    mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
    attacker_side, defender_side = roll_off_attacker_defender(manual_roll_allowed=False, log_fn=None)
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
    env0 = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
    env0.attacker_side = attacker_side
    env0.defender_side = defender_side
    state0, _ = env0.reset(options={"m": model, "e": enemy, "trunc": True})
    if isinstance(state0, (dict, collections.OrderedDict)):
        n_observations = len(list(state0.values()))
    else:
        n_observations = int(np.array(state0).shape[0])
    len_model = int(len(model))
    n_actions = action_sizes_from_env(env0, len_model)
    try:
        env0.close()
    except Exception:
        pass

    learner_side_cfg = LEARNER_SIDE if LEARNER_SIDE in {"P1", "P2"} else "P1"
    learner_identity = AgentIdentity(
        side=learner_side_cfg,
        faction=LEARNER_FACTION,
        ruleset_version=RULESET_VERSION,
    ).normalized()
    env_contract = make_env_contract(
        n_observations=n_observations,
        n_actions=n_actions,
        mission_name=mission_name,
        ruleset_version=learner_identity.ruleset_version,
        extras={"actor_learner": 1, "train_algo": TRAIN_ALGO, "mcts_mode": AZ_MCTS_MODE, "num_actors": int(AZ_NUM_ACTORS)},
    )

    az_kw = alphazero_kwargs_from_env()
    az_net = make_alphazero_net(n_observations=n_observations, n_actions=n_actions, **az_kw).to(device)
    optimizer = optim.AdamW(az_net.parameters(), lr=AZ_LR, amsgrad=True)
    _patch_optimizer_methods_no_compile(optimizer)
    replay = AlphaZeroReplayBuffer(capacity=AZ_REPLAY_CAPACITY)
    trainer_cfg = alphazero_train_config_from_env(
        AlphaZeroTrainConfig(
            lr=AZ_LR,
            batch_size=AZ_BATCH_SIZE,
            value_loss_weight=AZ_VALUE_LOSS_WEIGHT,
            l2_weight=AZ_L2_WEIGHT,
            balanced_outcome_sampling=bool(AZ_BALANCED_OUTCOME_SAMPLING),
            balanced_faction_sampling=bool(AZ_BALANCED_FACTION_SAMPLING),
            max_policy_staleness_updates=int(AZ_MAX_POLICY_STALENESS_UPDATES),
            lr_scheduler_type=AZ_LR_SCHEDULER,
            lr_warmup_steps=AZ_LR_WARMUP_STEPS,
            lr_total_steps=AZ_LR_TOTAL_STEPS,
        )
    )
    az_lr_scheduler = _build_az_lr_scheduler(optimizer, total_steps_hint=int(totLifeT) * max(1, AZ_UPDATES_PER_ROLLOUT) * 20)

    policy_version = 0
    optimize_steps = 0
    global_step = 0
    episodes_finished = 0
    resume_episode_base = 0
    if RESUME_CHECKPOINT:
        try:
            checkpoint = _load_checkpoint_payload(RESUME_CHECKPOINT)
            if isinstance(checkpoint, dict):
                policy_state = checkpoint.get("policy_value_net")
                if not isinstance(policy_state, dict):
                    policy_state = _extract_policy_state_dict(checkpoint)
                if isinstance(policy_state, dict):
                    arch = alphazero_arch_from_payload(checkpoint)
                    if arch != az_kw:
                        append_agent_log(
                            f"[AZ][RESUME][WARN] arch mismatch checkpoint={arch} current={az_kw}; strict=False load"
                        )
                    load_alphazero_state_dict(
                        az_net,
                        normalize_state_dict(policy_state),
                        log_fn=append_agent_log,
                    )
                opt_state = checkpoint.get("optimizer")
                if isinstance(opt_state, dict):
                    optimizer.load_state_dict(opt_state)
                sched_state = checkpoint.get("lr_scheduler")
                if az_lr_scheduler is not None and isinstance(sched_state, dict):
                    try:
                        az_lr_scheduler.load_state_dict(sched_state)
                    except Exception as exc:
                        append_agent_log(
                            f"[AZ][RESUME][WARN] lr_scheduler load failed: {exc}. "
                            "Где: train.py (_main_actor_learner_alphazero). Что делать: продолжить без scheduler state."
                        )
                replay_state = checkpoint.get("replay_memory")
                if replay_state is not None:
                    replay.load_state_dict(replay_state)
                resume_episode_base = int(checkpoint.get("episode", 0) or 0)
                episodes_finished = int(checkpoint.get("episodes_finished", resume_episode_base) or resume_episode_base)
                global_step = int(checkpoint.get("global_step", 0) or 0)
                optimize_steps = int(checkpoint.get("optimize_steps", 0) or 0)
                policy_version = int(checkpoint.get("policy_version", optimize_steps) or optimize_steps)
                append_agent_log(
                    "[AZ][RESUME] "
                    f"path={RESUME_CHECKPOINT} episode={episodes_finished} replay={len(replay)} "
                    f"global_step={global_step} optimize_steps={optimize_steps} policy_version={policy_version}"
                )
        except Exception as exc:
            append_agent_log(f"[AZ][RESUME][WARN] Не удалось загрузить checkpoint, старт с нуля. exc={exc}")

    opponent_spec = None
    opponent_algo_label = "heuristic"
    opponent_source_label = "heuristic_auto"
    opponent_agent_id = ""
    if int(SELF_PLAY_ENABLED) == 1:
        if OPPONENT_AGENT_ID:
            try:
                opponent_spec = load_agent_opponent(agent_id=OPPONENT_AGENT_ID, expected_contract=env_contract)
                opponent_algo_label = str(opponent_spec.algo or "unknown")
                opponent_source_label = "snapshot_policy_fn"
                opponent_agent_id = str(opponent_spec.agent_id or OPPONENT_AGENT_ID)
            except Exception as exc:
                append_agent_log(
                    "[AZ][SELFPLAY][WARN] "
                    f"Не удалось загрузить оппонента agent_id={OPPONENT_AGENT_ID}; fallback на heuristic. exc={exc}"
                )
        else:
            append_agent_log("[AZ][SELFPLAY][WARN] SELF_PLAY_ENABLED=1, но OPPONENT_AGENT_ID пустой; fallback на heuristic.")

    append_agent_log(
        "[AZ][CONFIG] "
        f"num_actors={AZ_NUM_ACTORS} actor_batch_send={AZ_ACTOR_BATCH_SEND} queue_max={AZ_ACTOR_QUEUE_MAX} "
        f"sync_every_updates={AZ_SYNC_EVERY_UPDATES} updates_per_rollout={AZ_UPDATES_PER_ROLLOUT} "
        f"balanced_sampling={int(AZ_BALANCED_OUTCOME_SAMPLING)} "
        f"max_staleness={AZ_MAX_POLICY_STALENESS_UPDATES} replay_min={AZ_REPLAY_MIN_SIZE} "
        f"outcome_only={int(AZ_OUTCOME_ONLY)} mcts_mode={AZ_MCTS_MODE} mcts={AZ_MCTS_SIMS} "
        f"top_k={AZ_MCTS_TOP_K_PER_HEAD} depth={AZ_MCTS_MAX_DEPTH} "
        f"hidden={az_kw['hidden_size']} layers={az_kw['num_layers']} value_ensemble={az_kw['n_value_ensemble']} "
        f"lr_scheduler={AZ_LR_SCHEDULER} c_puct_schedule={AZ_C_PUCT_SCHEDULE} "
        f"opponent_mode={opponent_source_label} opponent_algo={opponent_algo_label} "
        f"batch_eval={AZ_MCTS_BATCH_EVAL_SIZE} parallel_sims={AZ_MCTS_PARALLEL_SIMS} "
        f"det_eval_n={int(AZ_HONEST_EVAL_EPISODES)} det_eval_temp={float(AZ_HONEST_EVAL_TEMPERATURE):.3f}"
    )

    ep_rows: list[dict] = []
    loss_trace: list[float] = []
    last_checkpoint = ""
    last_actor_det_eval_ep = 0
    last_guard_turn_limit_rate = 0.0

    checkpoint_dir = os.path.join(MODELS_DIR, TRAIN_ALGO)
    os.makedirs(checkpoint_dir, exist_ok=True)
    sync_dir = os.path.join(MODELS_DIR, "actor_sync")
    os.makedirs(sync_dir, exist_ok=True)
    _az_sync_tag = "tree" if TRAIN_ALGO == "alphazero_tree" else "proxy"
    sync_path = os.path.join(sync_dir, f"latest_az_{_az_sync_tag}_policy.pth")
    opp_sync_path = os.path.join(sync_dir, f"latest_az_{_az_sync_tag}_opponent.pth")

    def _save_az_sync() -> None:
        cpu_sd = {k: v.detach().cpu() for k, v in normalize_state_dict(az_net.state_dict()).items()}
        torch.save(
            {
                "policy_version": int(policy_version),
                "optimize_steps": int(optimize_steps),
                "state_dict": cpu_sd,
            },
            sync_path,
        )

    def _save_checkpoint(episode_idx: int) -> str:
        ckpt_path = os.path.join(checkpoint_dir, f"checkpoint_ep{int(episode_idx)}.pth")
        payload = {
            "algo": TRAIN_ALGO,
            "mcts_mode": AZ_MCTS_MODE,
            "policy_value_net": az_net.state_dict(),
            "optimizer": optimizer.state_dict(),
            "episode": int(episode_idx),
            "episodes_finished": int(episodes_finished),
            "global_step": int(global_step),
            "optimize_steps": int(optimize_steps),
            "policy_version": int(policy_version),
            "replay_memory": replay.state_dict(),
            "env_contract": env_contract,
            "num_actors": int(AZ_NUM_ACTORS),
            "arch": dict(az_kw),
        }
        if az_lr_scheduler is not None:
            payload["lr_scheduler"] = az_lr_scheduler.state_dict()
        torch.save(payload, ckpt_path)
        return ckpt_path

    _save_az_sync()

    remaining_episodes = max(0, int(totLifeT) - int(episodes_finished))
    ctx = mp.get_context("spawn")
    data_q: mp.Queue = ctx.Queue(maxsize=int(AZ_ACTOR_QUEUE_MAX))
    procs = []
    inf_proc = None  # inference server process (variant B only)

    _mcts_cfg_payload = {
        "simulations": AZ_MCTS_SIMS,
        "c_puct": AZ_C_PUCT,
        "dirichlet_alpha": AZ_DIR_ALPHA,
        "dirichlet_eps": AZ_DIR_EPS,
        "top_k_per_head": AZ_MCTS_TOP_K_PER_HEAD,
        "max_depth": AZ_MCTS_MAX_DEPTH,
        "mode": AZ_MCTS_MODE,
        "root_dirichlet_only": AZ_MCTS_ROOT_DIRICHLET_ONLY,
        "eval_cache_size": AZ_MCTS_EVAL_CACHE_SIZE,
        "c_puct_min": AZ_C_PUCT_MIN,
        "c_puct_max": AZ_C_PUCT_MAX,
        "c_puct_schedule": AZ_C_PUCT_SCHEDULE,
        "pw_alpha": AZ_PW_ALPHA,
        "pw_beta": AZ_PW_BETA,
        "prior_weight_early": AZ_PRIOR_WEIGHT_EARLY,
        "batch_eval_size": AZ_MCTS_BATCH_EVAL_SIZE,
        "parallel_simulations": AZ_MCTS_PARALLEL_SIMS,
        "simulate_enemy_in_tree": AZ_MCTS_SIMULATE_ENEMY,
    }
    _sp_cfg_payload = {
        "temperature_opening_moves": AZ_TEMP_OPENING_MOVES,
        "temperature_opening_value": AZ_TEMP_OPENING,
        "temperature_late_value": AZ_TEMP_LATE,
    }
    _outcome_payload = {
        "outcome_only": AZ_OUTCOME_ONLY,
        "outcome_value_win": AZ_OUTCOME_VALUE_WIN,
        "outcome_value_loss": AZ_OUTCOME_VALUE_LOSS,
        "outcome_value_draw": AZ_OUTCOME_VALUE_DRAW,
        "policy_version": int(policy_version),
    }
    _init_weights_cpu = {k: v.detach().cpu() for k, v in normalize_state_dict(az_net.state_dict()).items()}
    _az_contract_hash = str(env_contract.get("contract_hash", "") or "")
    rollout_receiver = None
    if AZ_DISTRIBUTED_ACTORS:
        _clear_az_dist_stop_flag()
        rollout_receiver = RolloutReceiver(
            data_q,
            bind_host=AZ_DIST_ROLLOUT_BIND,
            bind_port=int(AZ_DIST_ROLLOUT_PORT),
            expected_contract_hash=_az_contract_hash,
            auth_token=AZ_DIST_AUTH_TOKEN,
            zmq_hwm=int(AZ_DIST_ZMQ_HWM),
            log_fn=append_agent_log,
        )
        rollout_receiver.start()
        try:
            _dist_az_hp = pack_az_dist_hyperparams(
                {
                    **AZ_CFG,
                    "mcts_simulations": int(AZ_MCTS_SIMS),
                    "mcts_parallel_sims": int(AZ_MCTS_PARALLEL_SIMS),
                    "mcts_max_depth": int(AZ_MCTS_MAX_DEPTH),
                    "mcts_top_k_per_head": int(AZ_MCTS_TOP_K_PER_HEAD),
                    "mcts_batch_eval_size": int(AZ_MCTS_BATCH_EVAL_SIZE),
                    "mcts_simulate_enemy": int(AZ_MCTS_SIMULATE_ENEMY),
                    "mcts_mode": str(AZ_MCTS_MODE),
                    "mcts_root_dirichlet_only": int(AZ_MCTS_ROOT_DIRICHLET_ONLY),
                    "mcts_eval_cache_size": int(AZ_MCTS_EVAL_CACHE_SIZE),
                    "c_puct": float(AZ_C_PUCT),
                    "c_puct_min": float(AZ_C_PUCT_MIN),
                    "c_puct_max": float(AZ_C_PUCT_MAX),
                    "c_puct_schedule": str(AZ_C_PUCT_SCHEDULE),
                    "dirichlet_alpha": float(AZ_DIR_ALPHA),
                    "dirichlet_eps": float(AZ_DIR_EPS),
                    "pw_alpha": float(AZ_PW_ALPHA),
                    "pw_beta": float(AZ_PW_BETA),
                    "prior_weight_early": float(AZ_PRIOR_WEIGHT_EARLY),
                    "temperature_opening_moves": int(AZ_TEMP_OPENING_MOVES),
                    "temperature_opening_value": float(AZ_TEMP_OPENING),
                    "temperature_late_value": float(AZ_TEMP_LATE),
                    "outcome_only": int(AZ_OUTCOME_ONLY),
                    "outcome_value_win": float(AZ_OUTCOME_VALUE_WIN),
                    "outcome_value_loss": float(AZ_OUTCOME_VALUE_LOSS),
                    "outcome_value_draw": float(AZ_OUTCOME_VALUE_DRAW),
                    "actor_batch_send": int(AZ_ACTOR_BATCH_SEND),
                    "inference_timeout": float(AZ_INFERENCE_TIMEOUT),
                    "self_play_enabled": int(SELF_PLAY_ENABLED),
                }
            )
            _dist_ctx_path = write_az_dist_train_context(
                {
                    "opponent_agent_id": str(opponent_agent_id or OPPONENT_AGENT_ID or ""),
                    "learner_side": str(LEARNER_SIDE or "P1"),
                    "env_contract_hash": str(_az_contract_hash),
                    "self_play_enabled": int(SELF_PLAY_ENABLED),
                    "train_algo": str(TRAIN_ALGO),
                    "az_hyperparams": _dist_az_hp,
                }
            )
            append_agent_log(
                f"[AZ][DIST][CONTEXT] wrote opponent_agent_id="
                f"{opponent_agent_id or OPPONENT_AGENT_ID or '-'} "
                f"parallel_sims={_dist_az_hp.get('mcts_parallel_sims', '?')} "
                f"path={_dist_ctx_path}"
            )
        except Exception as exc:
            append_agent_log(
                f"[AZ][DIST][CONTEXT][WARN] Не удалось записать контекст для PC2: {exc}. "
                "Где: write_az_dist_train_context. Что делать: проверьте SMB actor_sync."
            )

    if remaining_episodes > 0:
        if AZ_INFERENCE_SERVER_ENABLED:
            # --- Variant B: GPU inference server + CPU env workers ---
            effective_num_workers = int(AZ_NUM_ENV_WORKERS)

            if AZ_INFERENCE_REMOTE:
                # Pre-train health_check: train не стартует если ПК2 недоступен (v1)
                from core.models.az_inference_transport import az_remote_health_check

                try:
                    hc = az_remote_health_check(
                        host=AZ_INFERENCE_REMOTE_HOST,
                        port=int(AZ_INFERENCE_REMOTE_PORT),
                        auth_token=AZ_INFERENCE_REMOTE_AUTH_TOKEN,
                        timeout=min(3.0, float(AZ_INFERENCE_TIMEOUT)),
                    )
                    append_agent_log(
                        f"[AZ][REMOTE_CLIENT] health_check ok host={AZ_INFERENCE_REMOTE_HOST} "
                        f"port={AZ_INFERENCE_REMOTE_PORT} policy_version={hc.get('policy_version', '?')} "
                        f"gpu={hc.get('gpu_name', '?')}"
                    )
                except Exception as exc:
                    append_agent_log(
                        f"[AZ][REMOTE_CLIENT] health_check failed host={AZ_INFERENCE_REMOTE_HOST}: {exc}"
                    )
                    hint_host = ""
                    if str(AZ_INFERENCE_REMOTE_HOST).strip() in ("127.0.0.1", "localhost", "::1"):
                        hint_host = (
                            f" Сейчас host={AZ_INFERENCE_REMOTE_HOST!r} — это ПК1, не ПК2. "
                            "В hyperparams/GUI задайте LAN-IP ПК2 (inference_remote_host)."
                        )
                    raise RuntimeError(
                        "Remote AZ inference server недоступен. Проверьте: 1) сервер на ПК2 "
                        f"(tools\\pc2_remote_az_is.bat), 2) IP/порт ({AZ_INFERENCE_REMOTE_HOST}:{AZ_INFERENCE_REMOTE_PORT}), "
                        f"3) firewall (TCP 5555).{hint_host} exc={exc}"
                    ) from exc
                request_q = None
                reply_queues = None

            if AZ_INFERENCE_SERVER_LOCAL:
                # Запускаем локальный IS-процесс
                request_q = ctx.Queue(maxsize=int(AZ_INFERENCE_REQUEST_QUEUE_MAX))
                reply_queues = [ctx.Queue(maxsize=8) for _ in range(effective_num_workers)]
                _net_cfg = {
                    "obs_dim": int(n_observations),
                    "action_sizes": list(n_actions),
                    "hidden_size": int(az_kw.get("hidden_size", AZ_HIDDEN_SIZE)),
                    "num_layers": int(az_kw.get("num_layers", AZ_NUM_LAYERS)),
                    "n_value_ensemble": int(az_kw.get("n_value_ensemble", AZ_VALUE_ENSEMBLE)),
                }
                from core.models.az_inference_server import az_inference_server_entry
                inf_proc = ctx.Process(
                    target=az_inference_server_entry,
                    args=(
                        request_q,
                        reply_queues,
                        sync_path,
                        _init_weights_cpu,
                        _net_cfg,
                    ),
                    kwargs={
                        "inference_batch_size": int(AZ_INFERENCE_BATCH_SIZE),
                        "inference_batch_interval_ms": float(AZ_INFERENCE_BATCH_INTERVAL_MS),
                        "sync_check_interval": float(AZ_INFERENCE_SYNC_INTERVAL),
                    },
                    daemon=True,
                )
                inf_proc.start()
                append_agent_log(
                    f"[AZ][INF_SERVER] process spawned pid={inf_proc.pid} "
                    f"workers={effective_num_workers}"
                )

            for w_idx in range(effective_num_workers):
                base = int(remaining_episodes) // effective_num_workers
                rem = int(remaining_episodes) % effective_num_workers
                worker_episodes = int(base + (1 if w_idx < rem else 0))
                if worker_episodes <= 0:
                    continue
                p = ctx.Process(
                    target=_az_env_worker_entry,
                    args=(
                        int(w_idx),
                        int(worker_episodes),
                        roster_config,
                        int(b_len),
                        int(b_hei),
                        int(AZ_ACTOR_BATCH_SEND),
                        data_q,
                        request_q if AZ_INFERENCE_SERVER_LOCAL else None,
                        reply_queues[w_idx] if AZ_INFERENCE_SERVER_LOCAL else None,
                        int(1 if SELF_PLAY_ENABLED else 0),
                        opponent_spec,
                        _sp_cfg_payload,
                        _mcts_cfg_payload,
                        _outcome_payload,
                        float(AZ_INFERENCE_TIMEOUT),
                        str(AZ_INFERENCE_SERVER_MODE),
                        str(AZ_INFERENCE_REMOTE_HOST),
                        int(AZ_INFERENCE_REMOTE_PORT),
                        str(AZ_INFERENCE_REMOTE_AUTH_TOKEN),
                        "local",
                        "local",
                        "",
                        int(AZ_DIST_ROLLOUT_PORT),
                        str(AZ_DIST_AUTH_TOKEN),
                        str(_az_contract_hash),
                        "",
                    ),
                    daemon=True,
                )
                p.start()
                procs.append(p)

        else:
            # --- Variant A: CPU actors (текущее поведение, fallback) ---
            for a_idx in range(int(AZ_NUM_ACTORS)):
                base = int(remaining_episodes) // int(AZ_NUM_ACTORS)
                rem = int(remaining_episodes) % int(AZ_NUM_ACTORS)
                actor_episodes = int(base + (1 if a_idx < rem else 0))
                if actor_episodes <= 0:
                    continue
                p = ctx.Process(
                    target=_actor_learner_actor_entry_alphazero,
                    args=(
                        int(a_idx),
                        int(actor_episodes),
                        roster_config,
                        int(b_len),
                        int(b_hei),
                        int(n_observations),
                        list(n_actions),
                        _init_weights_cpu,
                        int(AZ_ACTOR_BATCH_SEND),
                        data_q,
                        int(1 if SELF_PLAY_ENABLED else 0),
                        opponent_spec,
                        _sp_cfg_payload,
                        _mcts_cfg_payload,
                        _outcome_payload,
                        "local",
                        "local",
                        "",
                        int(AZ_DIST_ROLLOUT_PORT),
                        str(AZ_DIST_AUTH_TOKEN),
                        str(_az_contract_hash),
                        "",
                    ),
                    daemon=True,
                )
                p.start()
                procs.append(p)

    done_actors = 0
    active_actors = len(procs)
    last_sync_opt_steps = optimize_steps
    pbar = tqdm(total=int(totLifeT), initial=int(episodes_finished), mininterval=ACTOR_PBAR_MININTERVAL, miniters=ACTOR_PBAR_MINITERS)
    last_loss = 0.0
    wait_started = time.time()
    last_heartbeat = wait_started
    az_heartbeat_sec = max(5.0, float(os.getenv("AZ_HEARTBEAT_SEC", "20") or 20))
    dist_draining = False
    dist_drain_until = 0.0
    dist_remote_transitions_total = 0
    dist_remote_stale_total = 0

    # P2: фаза прогресса для GUI (collecting → draining → done). Только distributed AZ.
    if AZ_DISTRIBUTED_ACTORS:
        append_agent_log("[TRAIN][PHASE] collecting")
        print("[TRAIN][PHASE] collecting", flush=True)

    while True:
        if not AZ_DISTRIBUTED_ACTORS:
            if done_actors >= active_actors:
                break
        else:
            if int(episodes_finished) >= int(totLifeT):
                if not dist_draining:
                    dist_draining = True
                    dist_drain_until = time.monotonic() + float(AZ_DIST_DRAIN_SEC)
                    _touch_az_dist_stop_flag()
                    _remote_alive = (
                        rollout_receiver.active_remote_workers() if rollout_receiver is not None else 0
                    )
                    _drain_left = max(0, int(round(dist_drain_until - time.monotonic())))
                    for _ln in (
                        "[TRAIN][PHASE] draining",
                        f"[TRAIN][DIST] remote_alive={_remote_alive} "
                        f"ep_done={int(episodes_finished)}/{int(totLifeT)} drain_left={_drain_left}s",
                    ):
                        append_agent_log(_ln)
                        print(_ln, flush=True)
                if dist_draining and time.monotonic() >= dist_drain_until and done_actors >= active_actors:
                    break
            elif active_actors > 0 and done_actors >= active_actors:
                # Локальные воркеры закончили, ждём эпизоды с PC2 до totLifeT.
                pass
        try:
            kind, payload = data_q.get(timeout=1.0)
        except mp_queue.Empty:
            now = time.time()
            if now - last_heartbeat >= az_heartbeat_sec:
                alive = sum(1 for p in procs if p.is_alive())
                elapsed = int(now - wait_started)
                wait_line = (
                    f"[AZ][WAIT] elapsed={elapsed}s replay={len(replay)} "
                    f"actors_alive={alive}/{active_actors} mode={AZ_MCTS_MODE} "
                    f"sims={AZ_MCTS_SIMS} depth={AZ_MCTS_MAX_DEPTH} "
                    f"(tree-MCTS: первый ep может занять 5–20 мин, прогресс по ep=...)"
                )
                print(wait_line, flush=True)
                append_agent_log(wait_line)
                if dist_draining:
                    _remote_alive = (
                        rollout_receiver.active_remote_workers() if rollout_receiver is not None else 0
                    )
                    _drain_left = max(0, int(round(dist_drain_until - time.monotonic())))
                    dist_line = (
                        f"[TRAIN][DIST] remote_alive={_remote_alive} "
                        f"ep_done={int(episodes_finished)}/{int(totLifeT)} drain_left={_drain_left}s"
                    )
                    print(dist_line, flush=True)
                    append_agent_log(dist_line)
                last_heartbeat = now
            continue

        if kind == "error":
            raise RuntimeError(payload)
        if kind == "done":
            done_actors += 1
            continue

        if kind == "ep":
            if not isinstance(payload, dict):
                continue
            if AZ_DISTRIBUTED_ACTORS and int(episodes_finished) >= int(totLifeT):
                continue
            episodes_finished += 1
            payload["episode"] = int(episodes_finished)
            ep_rows.append(payload)
            metrics_obj.updateRew(float(payload.get("ep_reward", 0.0) or 0.0))
            metrics_obj.updateEpLen(int(payload.get("ep_len", 0) or 0))
            target_n = min(int(totLifeT), int(episodes_finished))
            if target_n > int(pbar.n):
                pbar.update(target_n - int(pbar.n))
            # Всегда в stdout: GUI парсит ep= для прогресс-бара.
            print(f"ep={episodes_finished}/{totLifeT}", flush=True)

            ep_line = (
                f"[AZ] ep={episodes_finished}/{totLifeT} actor={int(payload.get('actor_idx', -1))} "
                f"result={payload.get('result','')} end_reason={payload.get('end_reason','')} "
                f"vp_diff={int(payload.get('vp_diff',0) or 0)} "
                f"loss={float(last_loss):.6f} replay={len(replay)} "
                f"staleness_guard={AZ_MAX_POLICY_STALENESS_UPDATES}"
            )
            append_agent_log(ep_line)
            if TRAIN_LOG_TO_CONSOLE:
                print(ep_line, flush=True)

            if (
                ACTOR_DET_EVAL_ENABLED
                and episodes_finished > last_actor_det_eval_ep
                and (episodes_finished % ACTOR_DET_EVAL_EVERY_EPISODES == 0 or episodes_finished == int(totLifeT))
            ):
                last_actor_det_eval_ep = int(episodes_finished)
                det_payload = _az_build_actor_det_payload(
                    az_net=az_net,
                    device=device,
                    roster_config=roster_config,
                    b_len=b_len,
                    b_hei=b_hei,
                    episodes_finished=int(episodes_finished),
                    last_loss=float(last_loss),
                    train_algo=str(TRAIN_ALGO),
                    mcts_mode=str(AZ_MCTS_MODE),
                    self_play_enabled=bool(int(SELF_PLAY_ENABLED) == 1),
                    opponent_spec=opponent_spec,
                )
                _save_actor_det_eval_snapshot(run_id=str(run_id), payload=det_payload, metrics_dir=METRICS_DIR)
                gate_pass = (
                    float(det_payload.get("win_rate", 0.0)) >= float(AZ_DET_EVAL_GATE_WIN_MIN)
                    and float(det_payload.get("turn_limit_rate", 1.0)) <= float(AZ_DET_EVAL_GATE_TURN_LIMIT_MAX)
                    and float(det_payload.get("draw_rate", 1.0)) <= float(AZ_DET_EVAL_GATE_DRAW_MAX)
                )
                if gate_pass:
                    try:
                        torch.save(
                            {
                                "episode": int(episodes_finished),
                                "policy_version": int(policy_version),
                                "state_dict": {k: v.detach().cpu() for k, v in normalize_state_dict(az_net.state_dict()).items()},
                            },
                            opp_sync_path,
                        )
                        append_agent_log(
                            "[AZ][GATE] pass "
                            f"ep={episodes_finished} win_rate={det_payload['win_rate']:.3f} "
                            f"turn_limit_rate={det_payload['turn_limit_rate']:.3f} "
                            f"draw_rate={det_payload['draw_rate']:.3f}"
                        )
                    except Exception as exc:
                        append_agent_log(f"[AZ][GATE][WARN] Не удалось обновить latest_az_opponent: {exc}")
                else:
                    append_agent_log(
                        "[AZ][GATE] blocked "
                        f"ep={episodes_finished} win_rate={det_payload['win_rate']:.3f}<{AZ_DET_EVAL_GATE_WIN_MIN:.3f} "
                        f"or turn_limit_rate={det_payload['turn_limit_rate']:.3f}>{AZ_DET_EVAL_GATE_TURN_LIMIT_MAX:.3f} "
                        f"or draw_rate={det_payload['draw_rate']:.3f}>{AZ_DET_EVAL_GATE_DRAW_MAX:.3f}"
                    )

                try:
                    det_gui = save_actor_det_eval_plot(run_id=str(run_id), metrics_dir=METRICS_DIR)
                    if det_gui:
                        learner_side = str(learner_identity.side or "P1").strip().upper() or "P1"
                        opponent_side = "P2" if learner_side == "P1" else "P1"
                        _write_det_eval_data_json(
                            run_id=str(run_id),
                            det_plot_gui_paths=det_gui,
                            model_path=str(last_checkpoint or ""),
                            metrics_mode="det_eval",
                            extra={
                                "algo": TRAIN_ALGO,
                                "mcts_mode": AZ_MCTS_MODE,
                                "mode": "actor_learner",
                                "learner_side": learner_side,
                                "learner_faction": str(learner_identity.faction or "Unknown"),
                                "opponent_side": opponent_side,
                                "opponent_faction": str(roster_config.get("enemy_faction", "Unknown")).strip(),
                                "opponent_algo": str(opponent_algo_label),
                                "opponent_source": str(opponent_source_label),
                                "opponent_id": str(opponent_agent_id),
                                "gate_pass": int(1 if gate_pass else 0),
                            },
                        )
                except Exception:
                    pass

                turn_limit_rate = float(det_payload.get("turn_limit_rate", 0.0) or 0.0)
                if turn_limit_rate > max(0.70, last_guard_turn_limit_rate + 0.05):
                    append_agent_log(
                        "[AZ][GUARD][WARN] "
                        f"turn_limit_rate растёт: prev={last_guard_turn_limit_rate:.3f} now={turn_limit_rate:.3f}. "
                        "Что делать: проверьте temperature/outcome targets и self-play opponent."
                    )
                last_guard_turn_limit_rate = float(turn_limit_rate)

            if SAVE_EVERY > 0 and (episodes_finished % max(1, SAVE_EVERY) == 0):
                last_checkpoint = _save_checkpoint(episodes_finished)
                append_agent_log(f"[AZ][CHECKPOINT] ep={episodes_finished} path={last_checkpoint}")

            continue

        if kind != "rollout":
            continue
        if not isinstance(payload, dict):
            continue
        raw_transitions = payload.get("transitions")
        if not isinstance(raw_transitions, list) or not raw_transitions:
            continue
        rollout_source = str(payload.get("source", "local") or "local")
        min_policy_ver = -1
        if int(AZ_MAX_POLICY_STALENESS_UPDATES) >= 0:
            min_policy_ver = int(policy_version) - int(AZ_MAX_POLICY_STALENESS_UPDATES)
        transitions: list[AZTransition] = []
        for raw in raw_transitions:
            if not isinstance(raw, dict):
                continue
            state_np = np.asarray(raw.get("state", []), dtype=np.float32)
            pi_raw = raw.get("policy_targets", [])
            if not isinstance(pi_raw, list):
                continue
            pi = [np.asarray(p, dtype=np.float32) for p in pi_raw]
            tr_pv = int(raw.get("policy_version", payload.get("policy_version", 0)) or 0)
            if rollout_source == "remote":
                dist_remote_transitions_total += 1
                if min_policy_ver >= 0 and tr_pv < min_policy_ver:
                    dist_remote_stale_total += 1
                    continue
            transitions.append(
                AZTransition(
                    state=state_np,
                    policy_targets=pi,
                    value_target=float(raw.get("value_target", 0.0) or 0.0),
                    policy_version=tr_pv,
                )
            )
        if not transitions:
            continue
        if rollout_source == "remote" and dist_remote_transitions_total > 0:
            if dist_remote_transitions_total % 200 == 0 or dist_remote_stale_total > 0 and dist_remote_stale_total % 50 == 0:
                stale_pct = 100.0 * float(dist_remote_stale_total) / max(1.0, float(dist_remote_transitions_total))
                append_agent_log(
                    f"[AZ][DIST] stale_drop remote={stale_pct:.1f}% "
                    f"({dist_remote_stale_total}/{dist_remote_transitions_total})"
                )

        replay.push_many(transitions)
        global_step += len(transitions)
        for _ in range(int(AZ_UPDATES_PER_ROLLOUT)):
            if len(replay) < max(int(AZ_REPLAY_MIN_SIZE), int(AZ_BATCH_SIZE)):
                break
            update_info = train_alphazero_step(
                net=az_net,
                optimizer=optimizer,
                replay=replay,
                config=trainer_cfg,
                device=device,
                current_policy_version=int(policy_version),
                scheduler=az_lr_scheduler,
            )
            if update_info is None:
                continue
            optimize_steps += 1
            policy_version += 1
            last_loss = float(update_info.get("loss", 0.0) or 0.0)
            loss_trace.append(float(last_loss))
            metrics_obj.updateLoss(float(last_loss))
            append_agent_log(
                "[AZ][UPDATE] "
                f"step={optimize_steps} policy_version={policy_version} "
                f"loss={float(update_info.get('loss', 0.0)):.6f} "
                f"policy_loss={float(update_info.get('policy_loss', 0.0)):.6f} "
                f"value_loss={float(update_info.get('value_loss', 0.0)):.6f} replay={len(replay)}"
            )
            if optimize_steps - last_sync_opt_steps >= int(AZ_SYNC_EVERY_UPDATES):
                _save_az_sync()
                last_sync_opt_steps = int(optimize_steps)

    if AZ_DISTRIBUTED_ACTORS:
        append_agent_log("[TRAIN][PHASE] done")
        print("[TRAIN][PHASE] done", flush=True)
    if rollout_receiver is not None:
        rollout_receiver.stop()
    if dist_remote_transitions_total > 0:
        stale_pct = 100.0 * float(dist_remote_stale_total) / max(1.0, float(dist_remote_transitions_total))
        append_agent_log(
            f"[AZ][DIST] final stale_drop remote={stale_pct:.1f}% "
            f"({dist_remote_stale_total}/{dist_remote_transitions_total})"
        )

    pbar.close()
    _save_az_sync()
    for p in procs:
        try:
            p.join(timeout=2.0)
        except Exception:
            pass
    if inf_proc is not None and inf_proc.is_alive():
        try:
            # Sentinel → inference server выходит из run-loop
            request_q.put_nowait(None)
        except Exception:
            pass
        inf_proc.join(timeout=3.0)
        if inf_proc.is_alive():
            append_agent_log("[AZ][INF_SERVER] process не завершился за 3с, terminate.")
            inf_proc.terminate()

    if not last_checkpoint:
        last_checkpoint = _save_checkpoint(int(episodes_finished or resume_episode_base or totLifeT))
        append_agent_log(f"[AZ][CHECKPOINT] final path={last_checkpoint}")

    if ep_rows:
        save_extra_metrics(
            run_id=run_id,
            ep_rows=ep_rows,
            metrics_dir=METRICS_DIR,
            write_legacy_gui_plots=False,
        )
        save_heuristic_metrics_snapshot(run_id=run_id, ep_rows=ep_rows, metrics_dir=METRICS_DIR)
        append_agent_log(f"[AZ][METRICS] saved run_id={run_id}")
        try:
            det_gui = save_actor_det_eval_plot(run_id=str(run_id), metrics_dir=METRICS_DIR)
            if det_gui:
                learner_side = str(learner_identity.side or "P1").strip().upper() or "P1"
                opponent_side = "P2" if learner_side == "P1" else "P1"
                _write_det_eval_data_json(
                    run_id=str(run_id),
                    det_plot_gui_paths=det_gui,
                    model_path=str(last_checkpoint or ""),
                    metrics_mode="det_eval",
                    extra={
                        "algo": TRAIN_ALGO,
                        "mcts_mode": AZ_MCTS_MODE,
                        "mode": "actor_learner",
                        "learner_side": learner_side,
                        "learner_faction": str(learner_identity.faction or "Unknown"),
                        "opponent_side": opponent_side,
                        "opponent_faction": str(roster_config.get("enemy_faction", "Unknown")).strip(),
                        "opponent_algo": str(opponent_algo_label),
                        "opponent_source": str(opponent_source_label),
                        "opponent_id": str(opponent_agent_id),
                    },
                )
        except Exception:
            pass

    final_episode = int(max(episodes_finished, resume_episode_base))
    final_agent_id = build_agent_id(learner_identity, f"final_ep{final_episode}")
    save_agent_artifact(
        identity=learner_identity,
        agent_id=final_agent_id,
        env_contract=env_contract,
        policy_state_dict=normalize_state_dict(az_net.state_dict()),
        target_state_dict={},
        optimizer_state_dict=optimizer.state_dict(),
        extra_meta={
            "algo": TRAIN_ALGO,
            "mcts_mode": AZ_MCTS_MODE,
            "episode": int(final_episode),
            "source_model_path": str(last_checkpoint or ""),
            "mode": "actor_learner",
            "num_actors": int(AZ_NUM_ACTORS),
            "policy_version": int(policy_version),
        },
    )
    append_agent_log(
        "[AZ][ACTOR_LEARNER] done "
        f"episodes={final_episode}/{totLifeT} checkpoint={last_checkpoint} "
        f"global_step={global_step} updates={optimize_steps} replay={len(replay)}"
    )


def _gmz_rollout_dict_from_transition(t: GMZTransition, policy_version: int) -> dict:
    beh = getattr(t, "behavior_logits", None) or []
    masks = getattr(t, "legal_masks_by_head", None) or []
    return {
        "state": np.asarray(t.state, dtype=np.float32),
        "action": np.asarray(t.action, dtype=np.int64),
        "reward": float(t.reward),
        "done": bool(t.done),
        "policy_targets": [np.asarray(p, dtype=np.float32) for p in t.policy_targets],
        "behavior_logits": [np.asarray(b, dtype=np.float32) for b in beh],
        "legal_masks_by_head": [np.asarray(m, dtype=np.float32) for m in masks],
        "value_target": float(t.value_target),
        "policy_version": int(getattr(t, "policy_version", policy_version) or policy_version),
    }


def _gmz_env_worker_entry(
    worker_id: int,
    episodes: int,
    roster_config: dict,
    b_len: int,
    b_hei: int,
    n_observations: int,
    n_actions: list,
    batch_send: int,
    data_q,
    request_q,
    reply_q,
    self_play_enabled: int,
    opponent_spec,
    sp_cfg_payload: dict,
    outcome_payload: dict,
    inference_timeout: float,
    inference_server_mode: str = "local",
    remote_host: str = "",
    remote_port: int = 5555,
    remote_auth_token: str = "",
):
    """CPU env worker: env + opponent; inference через GPU inference server."""
    try:
        sp_cfg = GumbelSelfPlayConfig(
            temperature_opening_moves=int(sp_cfg_payload.get("temperature_opening_moves", GMZ_TEMP_OPENING_MOVES)),
            temperature_opening_value=float(sp_cfg_payload.get("temperature_opening_value", GMZ_TEMP_OPENING)),
            temperature_late_value=float(sp_cfg_payload.get("temperature_late_value", GMZ_TEMP_LATE)),
            outcome_only=bool(outcome_payload.get("outcome_only", GMZ_OUTCOME_ONLY)),
            outcome_value_win=float(outcome_payload.get("outcome_value_win", GMZ_OUTCOME_VALUE_WIN)),
            outcome_value_loss=float(outcome_payload.get("outcome_value_loss", GMZ_OUTCOME_VALUE_LOSS)),
            outcome_value_draw=float(outcome_payload.get("outcome_value_draw", GMZ_OUTCOME_VALUE_DRAW)),
        )
        enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
        mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
        env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
        len_model = int(len(model))

        mode = str(inference_server_mode or "local").strip().lower()
        if mode == "remote":
            from core.models.gmz_inference_transport import RemoteInferenceTransport

            transport = RemoteInferenceTransport(
                worker_id=int(worker_id),
                host=str(remote_host or "127.0.0.1"),
                port=int(remote_port),
                auth_token=str(remote_auth_token or ""),
            )
            client = GMZInferenceClient(
                int(worker_id),
                transport=transport,
                timeout=float(inference_timeout),
                auth_token=str(remote_auth_token or ""),
            )
            append_agent_log(
                f"[GMZ][REMOTE_CLIENT][CONN] worker={int(worker_id)} "
                f"tcp://{remote_host}:{int(remote_port)}"
            )
        else:
            client = GMZInferenceClient(
                int(worker_id),
                request_q,
                reply_q,
                timeout=float(inference_timeout),
            )

        opponent_policy_fn = None
        if int(self_play_enabled) == 1 and opponent_spec is not None:
            try:
                opponent_policy_fn = build_policy_fn(
                    env=env,
                    len_model=len_model,
                    opponent=opponent_spec,
                    deterministic=bool(AZ_SNAPSHOT_OPP_DETERMINISTIC),
                )
            except Exception:
                opponent_policy_fn = None

        append_agent_log(f"[GMZ][ENV_WORKER] worker={int(worker_id)} started episodes={int(episodes)}")

        def _inference_fn(
            obs: np.ndarray,
            legal_masks_by_head: list,
            *,
            is_new_episode: bool,
            step_in_episode: int,
            episode_id: int,
        ):
            resp = client.infer(
                obs=obs,
                legal_masks_by_head=legal_masks_by_head,
                step_in_episode=step_in_episode,
                episode_id=episode_id,
                is_new_episode=is_new_episode,
            )
            return (
                resp["policy_targets"],
                resp["behavior_logits"],
                resp["selected_actions"],
                float(resp["value_est"]),
                int(resp.get("policy_version", 0) or 0),
            )

        rollout_batch: list[dict] = []
        for _ep in range(int(episodes)):
            ep_idx_1based = int(_ep) + 1
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
            env.attacker_side = attacker_side
            env.defender_side = defender_side

            ep_policy_version = 0
            transitions, info = play_episode_with_gumbel_muzero(
                env=env,
                inference_fn=_inference_fn,
                len_model=len_model,
                config=sp_cfg,
                enemy_policy_fn=opponent_policy_fn,
                policy_version=0,
                episode_id=int(_ep),
            )
            for t in transitions:
                item = _gmz_rollout_dict_from_transition(t, ep_policy_version)
                ep_policy_version = int(item.get("policy_version", ep_policy_version))
                rollout_batch.append(item)
            if len(rollout_batch) >= int(batch_send):
                data_q.put(
                    (
                        "rollout",
                        {
                            "actor_idx": int(worker_id),
                            "policy_version": int(ep_policy_version),
                            "transitions": list(rollout_batch),
                        },
                    )
                )
                rollout_batch = []

            info = dict(info or {})
            end_reason = str(info.get("end reason", "") or "")
            model_vp = int(info.get("model VP", 0) or 0)
            player_vp = int(info.get("player VP", 0) or 0)
            vp_diff = int(model_vp) - int(player_vp)
            result = "loss"
            if end_reason == "wipeout_enemy":
                result = "win"
            elif end_reason == "wipeout_model":
                result = "loss"
            elif str(end_reason).startswith("turn_limit"):
                if vp_diff > 0:
                    result = "win"
                elif vp_diff == 0:
                    result = "draw"
            elif vp_diff > 0:
                result = "win"
            elif vp_diff == 0:
                result = "draw"
            data_q.put(
                (
                    "ep",
                    {
                        "episode": None,
                        "actor_idx": int(worker_id),
                        "actor_ep": int(ep_idx_1based),
                        "ep_reward": float(info.get("reward", 0.0) or 0.0),
                        "ep_len": int(info.get("turn", 0) or 0),
                        "turn": int(info.get("turn", 0) or 0),
                        "model_vp": int(model_vp),
                        "player_vp": int(player_vp),
                        "vp_diff": int(vp_diff),
                        "result": str(result),
                        "end_reason": str(end_reason),
                        "end_code": int(info.get("res", 0) or 0),
                        "policy_version": int(ep_policy_version),
                    },
                )
            )

        if rollout_batch:
            data_q.put(
                (
                    "rollout",
                    {
                        "actor_idx": int(worker_id),
                        "policy_version": int(ep_policy_version),
                        "transitions": list(rollout_batch),
                    },
                )
            )
        data_q.put(("done", int(worker_id)))
    except Exception as exc:
        try:
            data_q.put(("error", f"gmz_env_worker[{worker_id}] {exc}"))
        except Exception:
            pass
    finally:
        _client = locals().get("client")
        if _client is not None:
            try:
                _client.close()
            except Exception:
                pass


def _actor_learner_actor_entry_gumbel_muzero(
    actor_idx: int,
    episodes: int,
    roster_config: dict,
    b_len: int,
    b_hei: int,
    n_observations: int,
    n_actions: list,
    init_weights: dict,
    batch_send: int,
    data_q,
    self_play_enabled: int,
    opponent_spec,
    sp_cfg_payload: dict,
    search_cfg_payload: dict,
    outcome_payload: dict,
):
    """Top-level entrypoint for Windows spawn pickling (Gumbel MuZero actor)."""
    try:
        actor_device = torch.device("cuda" if GMZ_ACTOR_DEVICE_CUDA else "cpu")
        gmz_net = GumbelMuZeroNet(
            obs_dim=int(n_observations),
            action_sizes=[int(x) for x in n_actions],
            latent_dim=int(search_cfg_payload.get("latent_dim", GMZ_LATENT_DIM)),
            hidden_dim=int(search_cfg_payload.get("hidden_dim", GMZ_HIDDEN_DIM)),
            num_layers=int(search_cfg_payload.get("num_layers", GMZ_NUM_LAYERS)),
            action_embed_dim=int(search_cfg_payload.get("action_embed_dim", GMZ_ACTION_EMBED_DIM)),
        ).to(actor_device)
        gmz_net.load_state_dict(normalize_state_dict(init_weights))
        gmz_net.eval()

        # torch.compile: только на CPU (на GPU overhead обычно не окупается)
        if GMZ_ACTOR_COMPILE and not GMZ_ACTOR_DEVICE_CUDA and hasattr(torch, "compile"):
            try:
                gmz_net = torch.compile(gmz_net, mode="default", fullgraph=False)
                append_agent_log("[GMZ][ACTOR] torch.compile enabled for actor inference (mode=default)")
            except Exception as e:
                append_agent_log(f"[GMZ][ACTOR] torch.compile skipped: {e}")

        search = GumbelMuZeroSearch(
            gmz_net,
            config=GumbelMuZeroSearchConfig(
                num_simulations=int(search_cfg_payload.get("num_simulations", GMZ_MCTS_SIMS)),
                root_top_k=int(search_cfg_payload.get("root_top_k", GMZ_ROOT_TOP_K)),
                discount=float(search_cfg_payload.get("discount", GMZ_DISCOUNT)),
                temperature=float(search_cfg_payload.get("temperature", GMZ_SEARCH_TEMP)),
                gumbel_scale=float(search_cfg_payload.get("gumbel_scale", GMZ_GUMBEL_SCALE)),
                prior_weight=float(search_cfg_payload.get("prior_weight", GMZ_PRIOR_WEIGHT)),
                batch_recurrent=bool(int(search_cfg_payload.get("batch_recurrent", int(GMZ_BATCH_RECURRENT)))),
                tree_reuse=bool(int(search_cfg_payload.get("tree_reuse", int(GMZ_TREE_REUSE)))),
            ),
            device=actor_device,
        )
        append_agent_log(
            f"[GMZ][ACTOR] actor={int(actor_idx)} device={actor_device.type} "
            f"latent={search_cfg_payload.get('latent_dim', GMZ_LATENT_DIM)} "
            f"sims={search_cfg_payload.get('num_simulations', GMZ_MCTS_SIMS)} "
            f"batch_rec={bool(int(search_cfg_payload.get('batch_recurrent', int(GMZ_BATCH_RECURRENT))))}"
        )
        sp_cfg = GumbelSelfPlayConfig(
            temperature_opening_moves=int(sp_cfg_payload.get("temperature_opening_moves", GMZ_TEMP_OPENING_MOVES)),
            temperature_opening_value=float(sp_cfg_payload.get("temperature_opening_value", GMZ_TEMP_OPENING)),
            temperature_late_value=float(sp_cfg_payload.get("temperature_late_value", GMZ_TEMP_LATE)),
            outcome_only=bool(outcome_payload.get("outcome_only", GMZ_OUTCOME_ONLY)),
            outcome_value_win=float(outcome_payload.get("outcome_value_win", GMZ_OUTCOME_VALUE_WIN)),
            outcome_value_loss=float(outcome_payload.get("outcome_value_loss", GMZ_OUTCOME_VALUE_LOSS)),
            outcome_value_draw=float(outcome_payload.get("outcome_value_draw", GMZ_OUTCOME_VALUE_DRAW)),
        )

        enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
        mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
        env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
        len_model = int(len(model))

        sync_enabled = os.getenv("ACTOR_SYNC_ENABLED", "1") == "1"
        sync_path = os.path.join(MODELS_DIR, "actor_sync", "latest_gmz_policy.pth")
        sync_check_every_ep = max(1, int(os.getenv("ACTOR_SYNC_CHECK_EVERY_EP", "5")))
        last_sync_mtime = -1.0
        current_policy_version = int(outcome_payload.get("policy_version", 0) or 0)

        opponent_policy_fn = None
        if int(self_play_enabled) == 1 and opponent_spec is not None:
            try:
                opponent_policy_fn = build_policy_fn(
                    env=env,
                    len_model=len_model,
                    opponent=opponent_spec,
                    deterministic=bool(AZ_SNAPSHOT_OPP_DETERMINISTIC),
                )
            except Exception:
                opponent_policy_fn = None

        rollout_batch: list[dict] = []
        for _ep in range(int(episodes)):
            ep_idx_1based = int(_ep) + 1
            if sync_enabled and (_ep % sync_check_every_ep == 0):
                try:
                    if os.path.isfile(sync_path):
                        mtime = os.path.getmtime(sync_path)
                        if mtime > last_sync_mtime:
                            payload = torch.load(sync_path, map_location="cpu", weights_only=False)
                            sd = payload.get("state_dict") if isinstance(payload, dict) else None
                            if isinstance(sd, dict):
                                gmz_net.load_state_dict(normalize_state_dict(sd))
                                gmz_net.eval()
                                search.net = gmz_net
                                last_sync_mtime = float(mtime)
                                current_policy_version = int(payload.get("policy_version", current_policy_version) or current_policy_version)
                except Exception:
                    pass

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
            env.attacker_side = attacker_side
            env.defender_side = defender_side

            transitions, info = play_episode_with_gumbel_muzero(
                env=env,
                search=search,
                len_model=len_model,
                config=sp_cfg,
                enemy_policy_fn=opponent_policy_fn,
                policy_version=int(current_policy_version),
            )
            for t in transitions:
                rollout_batch.append(
                    _gmz_rollout_dict_from_transition(t, int(current_policy_version))
                )
            if len(rollout_batch) >= int(batch_send):
                data_q.put(
                    (
                        "rollout",
                        {
                            "actor_idx": int(actor_idx),
                            "policy_version": int(current_policy_version),
                            "transitions": list(rollout_batch),
                        },
                    )
                )
                rollout_batch = []

            info = dict(info or {})
            end_reason = str(info.get("end reason", "") or "")
            model_vp = int(info.get("model VP", 0) or 0)
            player_vp = int(info.get("player VP", 0) or 0)
            vp_diff = int(model_vp) - int(player_vp)
            result = "loss"
            if end_reason == "wipeout_enemy":
                result = "win"
            elif end_reason == "wipeout_model":
                result = "loss"
            elif str(end_reason).startswith("turn_limit"):
                if vp_diff > 0:
                    result = "win"
                elif vp_diff == 0:
                    result = "draw"
            elif vp_diff > 0:
                result = "win"
            elif vp_diff == 0:
                result = "draw"
            data_q.put(
                (
                    "ep",
                    {
                        "episode": None,
                        "actor_idx": int(actor_idx),
                        "actor_ep": int(ep_idx_1based),
                        "ep_reward": float(info.get("reward", 0.0) or 0.0),
                        "ep_len": int(info.get("turn", 0) or 0),
                        "turn": int(info.get("turn", 0) or 0),
                        "model_vp": int(model_vp),
                        "player_vp": int(player_vp),
                        "vp_diff": int(vp_diff),
                        "result": str(result),
                        "end_reason": str(end_reason),
                        "end_code": int(info.get("res", 0) or 0),
                        "policy_version": int(current_policy_version),
                    },
                )
            )

        if rollout_batch:
            data_q.put(
                (
                    "rollout",
                    {
                        "actor_idx": int(actor_idx),
                        "policy_version": int(current_policy_version),
                        "transitions": list(rollout_batch),
                    },
                )
            )
        data_q.put(("done", int(actor_idx)))
    except Exception as exc:
        try:
            data_q.put(("error", f"gmz_actor[{actor_idx}] {exc}"))
        except Exception:
            pass


def _emit_train_progress_heartbeat(
    *,
    ep_done: int,
    ep_total: int,
    updates: int = 0,
    global_step: int = 0,
    replay_size: int = 0,
) -> None:
    """Периодический stdout для GUI: плавный elapsed/it/s между завершёнными эпизодами."""
    print(
        f"[TRAIN][PROGRESS] ep={int(ep_done)}/{int(ep_total)} "
        f"updates={int(updates)} steps={int(global_step)} replay={int(replay_size)}",
        flush=True,
    )


def _main_actor_learner_gumbel_muzero(*, roster_config, totLifeT, clip_reward_enabled, clip_reward_min, clip_reward_max) -> None:
    b_len = int(roster_config["b_len"])
    b_hei = int(roster_config["b_hei"])
    run_id = str(random.randint(1000000, 9999999))
    model_name = datetime.datetime.now().strftime("%d-%H%M%S")
    metrics_obj = metrics(MODELS_DIR, run_id, model_name)

    enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
    mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
    attacker_side, defender_side = roll_off_attacker_defender(manual_roll_allowed=False, log_fn=None)
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
    env0 = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
    env0.attacker_side = attacker_side
    env0.defender_side = defender_side
    state0, _ = env0.reset(options={"m": model, "e": enemy, "trunc": True})
    if isinstance(state0, (dict, collections.OrderedDict)):
        n_observations = len(list(state0.values()))
    else:
        n_observations = int(np.array(state0).shape[0])
    len_model = int(len(model))
    n_actions = action_sizes_from_env(env0, len_model)
    try:
        env0.close()
    except Exception:
        pass

    learner_side_cfg = LEARNER_SIDE if LEARNER_SIDE in {"P1", "P2"} else "P1"
    learner_identity = AgentIdentity(
        side=learner_side_cfg,
        faction=LEARNER_FACTION,
        ruleset_version=RULESET_VERSION,
    ).normalized()
    env_contract = make_env_contract(
        n_observations=n_observations,
        n_actions=n_actions,
        mission_name=mission_name,
        ruleset_version=learner_identity.ruleset_version,
        extras={"actor_learner": 1, "train_algo": "gumbel_muzero", "num_actors": int(GMZ_NUM_ACTORS)},
    )

    gmz_net = GumbelMuZeroNet(
        obs_dim=int(n_observations),
        action_sizes=[int(x) for x in n_actions],
        latent_dim=int(GMZ_LATENT_DIM),
        hidden_dim=int(GMZ_HIDDEN_DIM),
        num_layers=int(GMZ_NUM_LAYERS),
        action_embed_dim=int(GMZ_ACTION_EMBED_DIM),
    ).to(device)

    # torch.compile for learner — ~15-30% faster training, compilation cost ~10-20s
    if GMZ_LEARNER_COMPILE and device.type == "cuda" and hasattr(torch, "compile"):
        try:
            gmz_net = torch.compile(gmz_net, mode="reduce-overhead", fullgraph=False)
            append_agent_log("[GMZ][LEARNER] torch.compile enabled (mode=reduce-overhead)")
        except Exception as e:
            append_agent_log(f"[GMZ][LEARNER] torch.compile skipped: {e}")

    optimizer = optim.AdamW(gmz_net.parameters(), lr=GMZ_LR, amsgrad=True)
    _patch_optimizer_methods_no_compile(optimizer)
    replay = GumbelMuZeroReplayBuffer(capacity=GMZ_REPLAY_CAPACITY)
    trainer_cfg = GumbelMuZeroTrainConfig(
        lr=GMZ_LR,
        batch_size=GMZ_BATCH_SIZE,
        unroll_steps=GMZ_UNROLL_STEPS,
        tbptt_truncate=GMZ_TBPTT_TRUNCATE,
        value_loss_weight=GMZ_VALUE_LOSS_WEIGHT,
        reward_loss_weight=GMZ_REWARD_LOSS_WEIGHT,
        consistency_loss_weight=GMZ_CONSISTENCY_W,
        l2_weight=GMZ_L2_WEIGHT,
        max_grad_norm=GMZ_MAX_GRAD_NORM,
        lr_scheduler=GMZ_LR_SCHEDULER,
        lr_warmup_steps=GMZ_LR_WARMUP_STEPS,
        lr_total_steps=GMZ_LR_TOTAL_STEPS,
        max_policy_staleness_updates=int(GMZ_MAX_POLICY_STALENESS_UPDATES),
        vtrace_full=bool(GMZ_VTRACE_FULL),
        vtrace_rho_clip=GMZ_VTRACE_RHO_CLIP,
        vtrace_c_clip=GMZ_VTRACE_C_CLIP,
    )
    gmz_scheduler = make_gmz_lr_scheduler(optimizer, trainer_cfg)

    # B4: EMA target for SimSiam consistency loss
    from core.models.gumbel_muzero_trainer import GumbelMuZeroEMATarget
    ema_target = None
    if float(GMZ_CONSISTENCY_W) > 0.0:
        ema_target = GumbelMuZeroEMATarget(gmz_net, tau=GMZ_EMA_TAU)
        append_agent_log(f"[GMZ][EMA] tau={GMZ_EMA_TAU} consistency_w={GMZ_CONSISTENCY_W}")

    # B2: Reanalyzer for real-search policy target refresh
    reanalyze_frac = float(GMZ_REANALYZE_FRACTION)
    gmz_reanalyzer = None
    if reanalyze_frac > 0.0:
        from core.models.gumbel_muzero_search import GumbelMuZeroSearch, GumbelMuZeroSearchConfig
        _search_for_reanalyze = GumbelMuZeroSearch(
            gmz_net,
            config=GumbelMuZeroSearchConfig(
                num_simulations=max(1, int(GMZ_MCTS_SIMS) // 2),  # fast search for reanalysis
                root_top_k=max(1, int(GMZ_ROOT_TOP_K) // 2),
                discount=float(GMZ_DISCOUNT),
                temperature=float(GMZ_SEARCH_TEMP),
                gumbel_scale=float(GMZ_GUMBEL_SCALE),
                prior_weight=float(GMZ_PRIOR_WEIGHT),
                batch_recurrent=GMZ_BATCH_RECURRENT,
                tree_reuse=GMZ_TREE_REUSE,
            ),
            device=device,
        )
        gmz_reanalyzer = GumbelMuZeroReanalyzer(
            config=GumbelMuZeroReanalysisConfig(fast_sims=max(1, int(GMZ_MCTS_SIMS) // 2)),
            search=_search_for_reanalyze,
            device=device,
        )
        append_agent_log(f"[GMZ][REANALYZE] fraction={reanalyze_frac} fast_sims={max(1, int(GMZ_MCTS_SIMS) // 2)}")

    policy_version = 0
    optimize_steps = 0
    global_step = 0
    episodes_finished = 0
    resume_episode_base = 0
    if RESUME_CHECKPOINT:
        try:
            checkpoint = _load_checkpoint_payload(RESUME_CHECKPOINT)
            if isinstance(checkpoint, dict):
                policy_state = checkpoint.get("gumbel_muzero_net")
                if not isinstance(policy_state, dict):
                    policy_state = _extract_policy_state_dict(checkpoint)
                if isinstance(policy_state, dict):
                    gmz_net.load_state_dict(normalize_state_dict(policy_state))
                opt_state = checkpoint.get("optimizer")
                if isinstance(opt_state, dict):
                    optimizer.load_state_dict(opt_state)
                replay_state = checkpoint.get("replay_memory")
                if replay_state is not None:
                    replay.load_state_dict(replay_state)
                resume_episode_base = int(checkpoint.get("episode", 0) or 0)
                episodes_finished = int(checkpoint.get("episodes_finished", resume_episode_base) or resume_episode_base)
                global_step = int(checkpoint.get("global_step", 0) or 0)
                optimize_steps = int(checkpoint.get("optimize_steps", 0) or 0)
                policy_version = int(checkpoint.get("policy_version", optimize_steps) or optimize_steps)
                append_agent_log(
                    "[GMZ][RESUME] "
                    f"path={RESUME_CHECKPOINT} episode={episodes_finished} replay={len(replay)} "
                    f"global_step={global_step} optimize_steps={optimize_steps} policy_version={policy_version}"
                )
        except Exception as exc:
            append_agent_log(f"[GMZ][RESUME][WARN] Не удалось загрузить checkpoint, старт с нуля. exc={exc}")

    opponent_spec = None
    opponent_algo_label = "heuristic"
    opponent_source_label = "heuristic_auto"
    opponent_agent_id = ""
    if int(SELF_PLAY_ENABLED) == 1:
        if OPPONENT_AGENT_ID:
            try:
                opponent_spec = load_agent_opponent(agent_id=OPPONENT_AGENT_ID, expected_contract=env_contract)
                opponent_algo_label = str(opponent_spec.algo or "unknown")
                opponent_source_label = "snapshot_policy_fn"
                opponent_agent_id = str(opponent_spec.agent_id or OPPONENT_AGENT_ID)
            except Exception as exc:
                append_agent_log(
                    "[GMZ][SELFPLAY][WARN] "
                    f"Не удалось загрузить оппонента agent_id={OPPONENT_AGENT_ID}; fallback на heuristic. exc={exc}"
                )
        else:
            append_agent_log("[GMZ][SELFPLAY][WARN] SELF_PLAY_ENABLED=1, но OPPONENT_AGENT_ID пустой; fallback на heuristic.")

    effective_num_actors = int(GMZ_ACTOR_EFFECTIVE_NUM_ACTORS)
    if GMZ_INFERENCE_SERVER_USING_FALLBACK:
        append_agent_log(
            "[GMZ][CONFIG][FALLBACK] Запрошен inference server (variant B), но CUDA недоступна. "
            f"Переключаемся на вариант A: actor_device=cpu, num_actors={GMZ_ACTOR_CPU_FALLBACK_NUM_ACTORS}."
        )
    elif GMZ_INFERENCE_SERVER_ENABLED:
        if GMZ_INFERENCE_REMOTE:
            append_agent_log(
                f"[GMZ][CONFIG] Remote inference server (variant B-remote): env_workers={effective_num_actors} "
                f"host={GMZ_INFERENCE_REMOTE_HOST} port={GMZ_INFERENCE_REMOTE_PORT}"
            )
        else:
            append_agent_log(
                f"[GMZ][CONFIG] Inference server (variant B-local): env_workers={effective_num_actors} "
                f"batch={GMZ_INFERENCE_BATCH_SIZE} interval_ms={GMZ_INFERENCE_BATCH_INTERVAL_MS}"
            )
    elif GMZ_ACTOR_USING_CUDA_FALLBACK:
        append_agent_log(
            "[GMZ][CONFIG][FALLBACK] В hyperparams указан actor_device=cuda, но PyTorch не видит GPU с CUDA "
            f"(torch.cuda.is_available()=False, device_count={int(torch.cuda.device_count()) if hasattr(torch.cuda, 'device_count') else 0}). "
            f"Переключаемся на CPU: actor_device=cpu, num_actors={effective_num_actors} "
            f"(вместо cuda + num_actors={GMZ_NUM_ACTORS} + actor_max_cuda={GMZ_ACTOR_MAX_CUDA}). "
            "Чтобы включить GPU-акторов: установите драйвер NVIDIA и PyTorch с поддержкой CUDA (cu124/cu128)."
        )
    elif GMZ_ACTOR_DEVICE_CUDA:
        append_agent_log(
            f"[GMZ][CONFIG] GPU actors: {effective_num_actors} "
            f"(capped from num_actors={GMZ_NUM_ACTORS}, actor_max_cuda={GMZ_ACTOR_MAX_CUDA})"
        )

    append_agent_log(
        "[GMZ][CONFIG] "
        f"sims={GMZ_MCTS_SIMS} root_top_k={GMZ_ROOT_TOP_K} unroll={GMZ_UNROLL_STEPS} "
        f"batch={GMZ_BATCH_SIZE} actors={GMZ_NUM_ACTORS} effective_actors={effective_num_actors} "
        f"inference_server={int(GMZ_INFERENCE_SERVER_ENABLED)} "
        f"inference_mode={GMZ_INFERENCE_SERVER_MODE} env_workers={GMZ_NUM_ENV_WORKERS} "
        f"replay={GMZ_REPLAY_CAPACITY} "
        f"actor_device_req={GMZ_ACTOR_DEVICE_REQUESTED} actor_device={GMZ_ACTOR_DEVICE} "
        f"actor_device_cuda={int(GMZ_ACTOR_DEVICE_CUDA)} cuda_fallback={int(GMZ_ACTOR_USING_CUDA_FALLBACK)} "
        f"vtrace_full={int(GMZ_VTRACE_FULL)} rho_clip={GMZ_VTRACE_RHO_CLIP} c_clip={GMZ_VTRACE_C_CLIP} "
        f"atom={GMZ_ATOM_RANGE} tree_reuse={int(GMZ_TREE_REUSE)} batch_rec={int(GMZ_BATCH_RECURRENT)} "
        f"reanalyze={GMZ_REANALYZE_FRACTION} consistency_w={GMZ_CONSISTENCY_W} "
        f"ema_tau={GMZ_EMA_TAU} max_grad_norm={GMZ_MAX_GRAD_NORM} "
        f"actor_compile={int(GMZ_ACTOR_COMPILE)} learner_compile={int(GMZ_LEARNER_COMPILE)} "
        f"outcome_only={int(GMZ_OUTCOME_ONLY)} opponent={opponent_source_label}/{opponent_algo_label} "
        f"det_eval_n={int(GMZ_HONEST_EVAL_EPISODES)} det_eval_temp={float(GMZ_HONEST_EVAL_TEMPERATURE):.2f}"
    )

    ep_rows: list[dict] = []
    last_checkpoint = ""
    last_loss = 0.0

    checkpoint_dir = os.path.join(MODELS_DIR, "gumbel_muzero")
    os.makedirs(checkpoint_dir, exist_ok=True)
    sync_dir = os.path.join(MODELS_DIR, "actor_sync")
    os.makedirs(sync_dir, exist_ok=True)
    sync_path = os.path.join(sync_dir, "latest_gmz_policy.pth")

    def _save_gmz_sync() -> None:
        cpu_sd = {k: v.detach().cpu() for k, v in normalize_state_dict(gmz_net.state_dict()).items()}
        torch.save(
            {
                "policy_version": int(policy_version),
                "optimize_steps": int(optimize_steps),
                "state_dict": cpu_sd,
            },
            sync_path,
        )

    def _save_checkpoint(episode_idx: int) -> str:
        ckpt_path = os.path.join(checkpoint_dir, f"checkpoint_ep{int(episode_idx)}.pth")
        torch.save(
            {
                "algo": "gumbel_muzero",
                "gumbel_muzero_net": gmz_net.state_dict(),
                "policy_net": gmz_net.state_dict(),
                "optimizer": optimizer.state_dict(),
                "episode": int(episode_idx),
                "episodes_finished": int(episodes_finished),
                "global_step": int(global_step),
                "optimize_steps": int(optimize_steps),
                "policy_version": int(policy_version),
                "replay_memory": replay.state_dict(),
                "env_contract": env_contract,
                "num_actors": int(GMZ_NUM_ACTORS),
            },
            ckpt_path,
        )
        return ckpt_path

    gmz_sp_cfg = GumbelSelfPlayConfig(
        temperature_opening_moves=int(GMZ_TEMP_OPENING_MOVES),
        temperature_opening_value=float(GMZ_TEMP_OPENING),
        temperature_late_value=float(GMZ_TEMP_LATE),
        outcome_only=bool(GMZ_OUTCOME_ONLY),
        outcome_value_win=float(GMZ_OUTCOME_VALUE_WIN),
        outcome_value_loss=float(GMZ_OUTCOME_VALUE_LOSS),
        outcome_value_draw=float(GMZ_OUTCOME_VALUE_DRAW),
    )

    _save_gmz_sync()
    remaining_episodes = max(0, int(totLifeT) - int(episodes_finished))
    ctx = mp.get_context("spawn")
    data_q: mp.Queue = ctx.Queue(maxsize=int(GMZ_ACTOR_QUEUE_MAX))
    procs: list = []
    inf_proc = None
    request_q = None

    init_weights_cpu = {
        k: v.detach().cpu() for k, v in normalize_state_dict(gmz_net.state_dict()).items()
    }
    sp_cfg_payload = {
        "temperature_opening_moves": GMZ_TEMP_OPENING_MOVES,
        "temperature_opening_value": GMZ_TEMP_OPENING,
        "temperature_late_value": GMZ_TEMP_LATE,
    }
    search_cfg_payload = {
        "num_simulations": GMZ_MCTS_SIMS,
        "root_top_k": GMZ_ROOT_TOP_K,
        "discount": GMZ_DISCOUNT,
        "temperature": GMZ_SEARCH_TEMP,
        "gumbel_scale": GMZ_GUMBEL_SCALE,
        "prior_weight": GMZ_PRIOR_WEIGHT,
        "latent_dim": GMZ_LATENT_DIM,
        "hidden_dim": GMZ_HIDDEN_DIM,
        "num_layers": GMZ_NUM_LAYERS,
        "action_embed_dim": GMZ_ACTION_EMBED_DIM,
        "batch_recurrent": int(GMZ_BATCH_RECURRENT),
        "tree_reuse": int(GMZ_TREE_REUSE),
        "obs_dim": int(n_observations),
        "action_sizes": list(n_actions),
    }
    outcome_payload = {
        "outcome_only": GMZ_OUTCOME_ONLY,
        "outcome_value_win": GMZ_OUTCOME_VALUE_WIN,
        "outcome_value_loss": GMZ_OUTCOME_VALUE_LOSS,
        "outcome_value_draw": GMZ_OUTCOME_VALUE_DRAW,
        "policy_version": int(policy_version),
    }

    if remaining_episodes > 0:
        if GMZ_INFERENCE_SERVER_ENABLED and GMZ_INFERENCE_REMOTE:
            from core.models.gmz_inference_transport import remote_health_check

            try:
                hc = remote_health_check(
                    host=GMZ_INFERENCE_REMOTE_HOST,
                    port=int(GMZ_INFERENCE_REMOTE_PORT),
                    auth_token=GMZ_INFERENCE_REMOTE_AUTH_TOKEN,
                    timeout=min(3.0, float(GMZ_INFERENCE_TIMEOUT)),
                )
                append_agent_log(
                    f"[GMZ][REMOTE_CLIENT] health_check ok host={GMZ_INFERENCE_REMOTE_HOST} "
                    f"port={GMZ_INFERENCE_REMOTE_PORT} policy_version={hc.get('policy_version', '?')} "
                    f"gpu={hc.get('gpu_name', '?')}"
                )
            except Exception as exc:
                append_agent_log(
                    f"[GMZ][REMOTE_CLIENT] health_check failed host={GMZ_INFERENCE_REMOTE_HOST}: {exc}"
                )
                raise RuntimeError(
                    "Remote IS недоступен. Проверьте: 1) сервер на ПК2, 2) IP/порт, "
                    "3) firewall (TCP 5555)."
                ) from exc
            append_agent_log(
                f"[GMZ][REMOTE_CLIENT] connecting to tcp://{GMZ_INFERENCE_REMOTE_HOST}:{GMZ_INFERENCE_REMOTE_PORT}"
            )
        elif GMZ_INFERENCE_SERVER_LOCAL:
            request_q = ctx.Queue(maxsize=int(GMZ_INFERENCE_REQUEST_QUEUE_MAX))
            reply_queues = [ctx.Queue(maxsize=8) for _ in range(int(effective_num_actors))]
            inf_proc = ctx.Process(
                target=gmz_inference_server_entry,
                args=(
                    request_q,
                    reply_queues,
                    sync_path,
                    init_weights_cpu,
                    search_cfg_payload,
                ),
                kwargs={
                    "inference_batch_size": int(GMZ_INFERENCE_BATCH_SIZE),
                    "inference_batch_interval_ms": float(GMZ_INFERENCE_BATCH_INTERVAL_MS),
                    "inference_server_compile": bool(GMZ_INFERENCE_SERVER_COMPILE),
                    "clear_tree_on_weight_sync": bool(GMZ_CLEAR_TREE_ON_WEIGHT_SYNC),
                },
                daemon=True,
            )
            inf_proc.start()

        for a_idx in range(int(effective_num_actors)):
            base = int(remaining_episodes) // int(effective_num_actors)
            rem = int(remaining_episodes) % int(effective_num_actors)
            actor_episodes = int(base + (1 if a_idx < rem else 0))
            if actor_episodes <= 0:
                continue
            if GMZ_INFERENCE_SERVER_ENABLED:
                worker_args = (
                    int(a_idx),
                    int(actor_episodes),
                    roster_config,
                    int(b_len),
                    int(b_hei),
                    int(n_observations),
                    list(n_actions),
                    int(GMZ_ACTOR_BATCH_SEND),
                    data_q,
                    request_q,
                    reply_queues[int(a_idx)] if GMZ_INFERENCE_SERVER_LOCAL else None,
                    int(1 if SELF_PLAY_ENABLED else 0),
                    opponent_spec,
                    sp_cfg_payload,
                    outcome_payload,
                    float(GMZ_INFERENCE_TIMEOUT),
                    str(GMZ_INFERENCE_SERVER_MODE),
                    str(GMZ_INFERENCE_REMOTE_HOST),
                    int(GMZ_INFERENCE_REMOTE_PORT),
                    str(GMZ_INFERENCE_REMOTE_AUTH_TOKEN),
                )
                p = ctx.Process(
                    target=_gmz_env_worker_entry,
                    args=worker_args,
                    daemon=True,
                )
            else:
                p = ctx.Process(
                    target=_actor_learner_actor_entry_gumbel_muzero,
                    args=(
                        int(a_idx),
                        int(actor_episodes),
                        roster_config,
                        int(b_len),
                        int(b_hei),
                        int(n_observations),
                        list(n_actions),
                        init_weights_cpu,
                        int(GMZ_ACTOR_BATCH_SEND),
                        data_q,
                        int(1 if SELF_PLAY_ENABLED else 0),
                        opponent_spec,
                        sp_cfg_payload,
                        search_cfg_payload,
                        outcome_payload,
                    ),
                    daemon=True,
                )
            p.start()
            procs.append(p)

    done_actors = 0
    active_actors = len(procs)
    last_sync_opt_steps = optimize_steps
    last_actor_det_eval_ep = 0
    last_progress_heartbeat = time.time()

    def _maybe_train_progress_heartbeat(*, force: bool = False) -> None:
        nonlocal last_progress_heartbeat
        now = time.time()
        if not force and (now - last_progress_heartbeat) < TRAIN_PROGRESS_HEARTBEAT_SEC:
            return
        last_progress_heartbeat = now
        _emit_train_progress_heartbeat(
            ep_done=int(episodes_finished),
            ep_total=int(totLifeT),
            updates=int(optimize_steps),
            global_step=int(global_step),
            replay_size=int(len(replay)),
        )

    pbar = tqdm(total=int(totLifeT), initial=int(episodes_finished), mininterval=ACTOR_PBAR_MININTERVAL, miniters=ACTOR_PBAR_MINITERS)
    while done_actors < active_actors:
        try:
            kind, payload = data_q.get(timeout=1.0)
        except mp_queue.Empty:
            _maybe_train_progress_heartbeat()
            continue
        if kind == "error":
            raise RuntimeError(payload)
        if kind == "done":
            done_actors += 1
            continue
        if kind == "ep":
            if not isinstance(payload, dict):
                continue
            episodes_finished += 1
            payload["episode"] = int(episodes_finished)
            ep_rows.append(payload)
            metrics_obj.updateRew(float(payload.get("ep_reward", 0.0) or 0.0))
            metrics_obj.updateEpLen(int(payload.get("ep_len", 0) or 0))
            target_n = min(int(totLifeT), int(episodes_finished))
            if target_n > int(pbar.n):
                pbar.update(target_n - int(pbar.n))
            if (episodes_finished % ACTOR_PROGRESS_STDOUT_EVERY == 0) or (episodes_finished >= int(totLifeT)):
                print(f"ep={episodes_finished}/{totLifeT}", flush=True)
            _maybe_train_progress_heartbeat(force=True)
            if SAVE_EVERY > 0 and (episodes_finished % max(1, SAVE_EVERY) == 0):
                last_checkpoint = _save_checkpoint(episodes_finished)
                append_agent_log(f"[GMZ][CHECKPOINT] ep={episodes_finished} path={last_checkpoint}")
            if (
                ACTOR_DET_EVAL_ENABLED
                and episodes_finished > last_actor_det_eval_ep
                and (episodes_finished % ACTOR_DET_EVAL_EVERY_EPISODES == 0 or episodes_finished == int(totLifeT))
            ):
                last_actor_det_eval_ep = int(episodes_finished)
                det_payload = _gmz_build_actor_det_payload(
                    gmz_net=gmz_net,
                    device=device,
                    roster_config=roster_config,
                    b_len=b_len,
                    b_hei=b_hei,
                    episodes_finished=int(episodes_finished),
                    last_loss=float(last_loss),
                    self_play_enabled=bool(int(SELF_PLAY_ENABLED) == 1),
                    opponent_spec=opponent_spec,
                    sp_cfg=gmz_sp_cfg,
                )
                _save_actor_det_eval_snapshot(run_id=str(run_id), payload=det_payload, metrics_dir=METRICS_DIR)
                det_gui = save_actor_det_eval_plot(run_id=str(run_id), metrics_dir=METRICS_DIR)
                learner_side = str(learner_identity.side or "P1").strip().upper() or "P1"
                opponent_side = "P2" if learner_side == "P1" else "P1"
                _write_det_eval_data_json(
                    run_id=str(run_id),
                    det_plot_gui_paths=det_gui or {},
                    model_path=str(last_checkpoint or ""),
                    metrics_mode="det_eval",
                    extra={
                        "algo": "gumbel_muzero",
                        "mode": "actor_learner",
                        "learner_side": learner_side,
                        "learner_faction": str(learner_identity.faction or "Unknown"),
                        "opponent_side": opponent_side,
                        "opponent_faction": str(roster_config.get("enemy_faction", "Unknown")).strip(),
                        "opponent_algo": str(opponent_algo_label),
                        "opponent_source": str(opponent_source_label),
                        "opponent_id": str(opponent_agent_id),
                    },
                )
            continue
        if kind != "rollout":
            continue
        if not isinstance(payload, dict):
            continue
        raw_transitions = payload.get("transitions")
        if not isinstance(raw_transitions, list) or not raw_transitions:
            continue
        transitions: list[GMZTransition] = []
        for raw in raw_transitions:
            if not isinstance(raw, dict):
                continue
            pi_raw = raw.get("policy_targets", [])
            if not isinstance(pi_raw, list):
                continue
            beh_raw = raw.get("behavior_logits", [])
            masks_raw = raw.get("legal_masks_by_head", [])
            transitions.append(
                GMZTransition(
                    state=np.asarray(raw.get("state", []), dtype=np.float32),
                    action=np.asarray(raw.get("action", []), dtype=np.int64),
                    reward=float(raw.get("reward", 0.0) or 0.0),
                    done=bool(raw.get("done", False)),
                    policy_targets=[np.asarray(p, dtype=np.float32) for p in pi_raw],
                    behavior_logits=[
                        np.asarray(b, dtype=np.float32)
                        for b in (beh_raw if isinstance(beh_raw, list) else [])
                    ],
                    legal_masks_by_head=[
                        np.asarray(m, dtype=np.float32)
                        for m in (masks_raw if isinstance(masks_raw, list) else [])
                    ],
                    value_target=float(raw.get("value_target", 0.0) or 0.0),
                    policy_version=int(raw.get("policy_version", payload.get("policy_version", 0)) or 0),
                )
            )
        if not transitions:
            continue
        replay.push_many(transitions)
        global_step += len(transitions)
        for _ in range(int(GMZ_UPDATES_PER_ROLLOUT)):
            if len(replay) < max(int(GMZ_REPLAY_MIN_SIZE), int(GMZ_BATCH_SIZE)):
                break
            update_info = train_gumbel_muzero_step(
                net=gmz_net,
                optimizer=optimizer,
                replay=replay,
                config=trainer_cfg,
                device=device,
                current_policy_version=int(policy_version),
                scheduler=gmz_scheduler,
                ema_target=ema_target,
            )
            if update_info is None:
                continue
            optimize_steps += 1
            policy_version += 1
            last_loss = float(update_info.get("loss", 0.0) or 0.0)
            metrics_obj.updateLoss(float(last_loss))
            # B2: Periodic reanalysis — refresh policy targets with real search
            if (
                gmz_reanalyzer is not None
                and float(reanalyze_frac) > 0.0
                and optimize_steps > 0
                and (optimize_steps % max(1, int(1.0 / float(reanalyze_frac)))) == 0
            ):
                n_reanalyzed = gmz_reanalyzer.update_replay_with_reanalysis(replay, gmz_net)
                if n_reanalyzed > 0:
                    append_agent_log(f"[GMZ][REANALYZE] step={optimize_steps} updated={n_reanalyzed}")
            append_agent_log(
                "[GMZ][UPDATE] "
                f"step={optimize_steps} policy_version={policy_version} "
                f"loss={float(update_info.get('loss', 0.0)):.6f} "
                f"policy_loss={float(update_info.get('policy_loss', 0.0)):.6f} "
                f"value_loss={float(update_info.get('value_loss', 0.0)):.6f} "
                f"reward_loss={float(update_info.get('reward_loss', 0.0)):.6f} replay={len(replay)}"
            )
            if optimize_steps - last_sync_opt_steps >= int(GMZ_SYNC_EVERY_UPDATES):
                _save_gmz_sync()
                last_sync_opt_steps = int(optimize_steps)
            _maybe_train_progress_heartbeat()

    pbar.close()
    _save_gmz_sync()
    if request_q is not None:
        try:
            request_q.put(None)
        except Exception:
            pass
    for p in procs:
        try:
            p.join(timeout=2.0)
        except Exception:
            pass
    if inf_proc is not None:
        try:
            inf_proc.join(timeout=3.0)
        except Exception:
            pass

    if not last_checkpoint:
        last_checkpoint = _save_checkpoint(int(episodes_finished or resume_episode_base or totLifeT))
        append_agent_log(f"[GMZ][CHECKPOINT] final path={last_checkpoint}")

    if ep_rows:
        save_extra_metrics(
            run_id=run_id,
            ep_rows=ep_rows,
            metrics_dir=METRICS_DIR,
            write_legacy_gui_plots=False,
        )
        save_heuristic_metrics_snapshot(run_id=run_id, ep_rows=ep_rows, metrics_dir=METRICS_DIR)
        # Финальный DET-снапшот для надёжной привязки GUI к текущему run_id.
        det_payload = _gmz_build_actor_det_payload(
            gmz_net=gmz_net,
            device=device,
            roster_config=roster_config,
            b_len=b_len,
            b_hei=b_hei,
            episodes_finished=int(max(episodes_finished, 1)),
            last_loss=float(last_loss),
            self_play_enabled=bool(int(SELF_PLAY_ENABLED) == 1),
            opponent_spec=opponent_spec,
            sp_cfg=gmz_sp_cfg,
        )
        _save_actor_det_eval_snapshot(run_id=str(run_id), payload=det_payload, metrics_dir=METRICS_DIR)
        det_gui = save_actor_det_eval_plot(run_id=str(run_id), metrics_dir=METRICS_DIR)
        if det_gui:
            learner_side = str(learner_identity.side or "P1").strip().upper() or "P1"
            opponent_side = "P2" if learner_side == "P1" else "P1"
            _write_det_eval_data_json(
                run_id=str(run_id),
                det_plot_gui_paths=det_gui,
                model_path=str(last_checkpoint or ""),
                metrics_mode="det_eval",
                extra={
                    "algo": "gumbel_muzero",
                    "mode": "actor_learner",
                    "learner_side": learner_side,
                    "learner_faction": str(learner_identity.faction or "Unknown"),
                    "opponent_side": opponent_side,
                    "opponent_faction": str(roster_config.get("enemy_faction", "Unknown")).strip(),
                    "opponent_algo": str(opponent_algo_label),
                    "opponent_source": str(opponent_source_label),
                    "opponent_id": str(opponent_agent_id),
                },
            )
        else:
            _write_det_eval_data_json(
                run_id=str(run_id),
                det_plot_gui_paths={},
                model_path=str(last_checkpoint or ""),
                metrics_mode="det_eval",
                extra={"algo": "gumbel_muzero", "mode": "actor_learner", "det_eval_note": "нет точек DET-eval"},
            )
        append_agent_log(f"[GMZ][METRICS] saved run_id={run_id}")

    final_episode = int(max(episodes_finished, resume_episode_base))
    final_agent_id = build_agent_id(learner_identity, f"final_ep{final_episode}")
    save_agent_artifact(
        identity=learner_identity,
        agent_id=final_agent_id,
        env_contract=env_contract,
        policy_state_dict=normalize_state_dict(gmz_net.state_dict()),
        target_state_dict={},
        optimizer_state_dict=optimizer.state_dict(),
        extra_meta={
            "algo": "gumbel_muzero",
            "episode": int(final_episode),
            "source_model_path": str(last_checkpoint or ""),
            "mode": "actor_learner",
            "num_actors": int(GMZ_NUM_ACTORS),
            "policy_version": int(policy_version),
        },
    )
    append_agent_log(
        "[GMZ][ACTOR_LEARNER] done "
        f"episodes={final_episode}/{totLifeT} checkpoint={last_checkpoint} "
        f"global_step={global_step} updates={optimize_steps} replay={len(replay)}"
    )

if __name__ == "__main__":
    mp.freeze_support()
    main()
