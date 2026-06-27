import atexit
import collections
import csv
import datetime
import json
import math
import multiprocessing as mp
import os
import pickle
import queue as mp_queue
import random
import sys
import threading
import time
from collections import Counter
from typing import NoReturn

import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from core.engine import Unit, initFile, metrics, unitData, weaponData
from core.engine.agent_registry import (
    AgentIdentity,
    build_agent_id,
    compatible_contracts,
    list_agents,
    load_agent_by_id,
    make_env_contract,
    save_agent_artifact,
)
from core.engine.game_io import ConsoleIO, set_active_io
from core.engine.io_profiler import get_io_profiler
from core.engine.mission import (
    board_dims_for_mission,
    deploy_for_mission,
    normalize_mission_name,
    post_deploy_setup,
)
from core.engine.phases.obs_features import (
    describe_obs_dim_mismatch,
    resolve_phase_obs_features,
)
from core.engine.phases.replay_meta import (
    az_transition_from_rollout_dict,
    az_transition_to_rollout_dict,
    gmz_transition_from_rollout_dict,
)
from core.envs.warhamEnv import *
from core.telemetry.stratagem_trace import (
    StratagemEpisodeTracer,
    make_stratagem_tracer_for_train,
    train_stratagem_trace_enabled,
)
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

from core.engine.matchmaker import record_matchup
from core.models.action_contract import action_sizes_from_env, action_tensor_to_dict, ordered_action_keys
from core.models.alphazero_ids import (
    VALID_TRAIN_ALGOS,
    az_mcts_mode_for,
    az_section_for,
    is_az_algo,
    is_gumbel_az_algo,
)
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.alphazero_model import (
    alphazero_arch_from_payload,
    alphazero_kwargs_from_env,
    load_alphazero_state_dict,
    make_alphazero_net,
)
from core.models.alphazero_replay import AlphaZeroReplayBuffer, AZTransition
from core.models.alphazero_selfplay import SelfPlayConfig, play_episode_with_mcts
from core.models.alphazero_trainer import (
    AlphaZeroTrainConfig,
    alphazero_train_config_from_env,
    build_alphazero_lr_scheduler,
    train_alphazero_step,
)
from core.models.az_family_env import resolve_az_family_env
from core.models.az_rollout_receiver import RolloutReceiver
from core.models.az_rollout_sink import (
    az_dist_stop_flag_path,
    az_dist_stop_requested,
    make_rollout_sink,
    pack_az_dist_hyperparams,
    write_az_dist_train_context,
    write_az_remote_search_cfg,
)
from core.models.DQN import *
from core.models.dqn_dist import (
    DQN_DIST_TOPUP_ACTOR_IDX,
    clear_dqn_dist_stop_flag,
    compute_dqn_dist_topup_episodes,
    dqn_dist_env_contract_extras,
    dqn_dist_stop_requested,
    resolve_dqn_dist_episode_split,
    split_count_among_workers,
    touch_dqn_dist_stop_flag,
    wait_dqn_dist_remote_workers,
    write_dqn_dist_train_context,
)
from core.models.gmz_inference_client import GMZInferenceClient
from core.models.gmz_inference_server import gmz_inference_server_entry
from core.models.gmz_remote_search_cfg_builder import publish_gmz_remote_search_cfg
from core.models.gumbel_muzero_model import (
    GumbelMuZeroNet,
    gumbel_muzero_arch_from_payload,
    gumbel_muzero_kwargs_from_env,
    load_gumbel_muzero_state_dict,
)
from core.models.gumbel_muzero_reanalysis import GumbelMuZeroReanalysisConfig, GumbelMuZeroReanalyzer
from core.models.gumbel_muzero_replay import GMZTransition, GumbelMuZeroReplayBuffer
from core.models.gumbel_muzero_search import GumbelMuZeroSearch, GumbelMuZeroSearchConfig
from core.models.gumbel_muzero_selfplay import GumbelSelfPlayConfig, play_episode_with_gumbel_muzero
from core.models.gumbel_muzero_trainer import GumbelMuZeroTrainConfig, make_gmz_lr_scheduler, train_gumbel_muzero_step
from core.models.memory import *
from core.models.opponent_adapter import OpponentSpec, build_policy_fn, load_agent_opponent
from core.models.PPO import (
    ActorCriticMultiHead,
    load_actor_critic_state_dict,
    make_actor_critic,
    ppo_arch_from_payload,
    ppo_kwargs_from_env,
    update_ppo_entropy_coef,
)
from core.models.ppo_buffer import PPORolloutBuffer
from core.models.sampled_muzero_model import (
    load_sampled_muzero_state_dict,
    make_sampled_muzero_net,
    sampled_muzero_arch_from_payload,
    sampled_muzero_kwargs_from_env,
)
from core.models.sampled_muzero_search import SampledMuZeroSearch, SampledMuZeroSearchConfig
from core.models.sampled_muzero_selfplay import SampledSelfPlayConfig, play_episode_with_sampled_muzero
from core.models.sampled_muzero_trainer import (
    SampledMuZeroEMATarget,
    SampledMuZeroTrainConfig,
    make_smz_lr_scheduler,
    train_sampled_muzero_step,
)
from core.models.smz_inference_server import smz_inference_server_entry
from core.models.smz_remote_search_cfg_builder import publish_smz_remote_search_cfg
from core.models.utils import *
from core.models.utils import _build_select_action_masks

MODELS_DIR = str(ARTIFACTS_MODELS_DIR)
METRICS_DIR = str(ARTIFACTS_METRICS_DIR)
RUNTIME_IMG_DIR = os.path.join(str(RUNTIME_STATE_DIR), "img")

# Workaround: на некоторых окружениях torch._dynamo падает из-за несовместимого triton.
# Важно: используем setdefault, чтобы пользователь мог включить dynamo вручную.
os.environ.setdefault("TORCHDYNAMO_DISABLE", "1")

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
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
DQN_REACTION_VALUE_POLICY = _cfg_bool("DQN_REACTION_VALUE_POLICY", "reaction_value_policy", "1")
if "DQN_REACTION_VALUE_POLICY" not in os.environ:
    os.environ["DQN_REACTION_VALUE_POLICY"] = "1" if DQN_REACTION_VALUE_POLICY else "0"
_PPO_CFG = data.get("ppo", {}) if isinstance(data, dict) else {}
_ppo_rvp_raw = os.getenv("PPO_REACTION_VALUE_POLICY", str(_PPO_CFG.get("reaction_value_policy", 1)))
PPO_REACTION_VALUE_POLICY = str(_ppo_rvp_raw).strip().lower() in ("1", "true", "yes", "on")
if "PPO_REACTION_VALUE_POLICY" not in os.environ:
    os.environ["PPO_REACTION_VALUE_POLICY"] = "1" if PPO_REACTION_VALUE_POLICY else "0"
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

# Точки метрик тренировки (окно реальных эпизодов; DET-прогоны удалены).
# Имена *DET_EVAL* сохранены для обратной совместимости env/GUI.
DET_EVAL_ENABLED = os.getenv("DET_EVAL_ENABLED", "1") == "1"
DET_EVAL_EVERY_EPISODES = int(os.getenv("DET_EVAL_EVERY_EPISODES", "50"))
DET_EVAL_EPISODES = int(os.getenv("DET_EVAL_EPISODES", "20"))
DET_EVAL_OPPONENT_EPSILON = float(os.getenv("DET_EVAL_OPPONENT_EPSILON", "0.0"))

# Actor-Learner: периодическая точка метрик (во время тренировки)
ACTOR_DET_EVAL_ENABLED = os.getenv("ACTOR_DET_EVAL_ENABLED", "1") == "1"
ACTOR_DET_EVAL_EVERY_EPISODES = int(os.getenv("ACTOR_DET_EVAL_EVERY_EPISODES", "50"))
ACTOR_DET_EVAL_EPISODES = int(os.getenv("ACTOR_DET_EVAL_EPISODES", "50"))
ACTOR_DET_EVAL_OPPONENT_EPSILON = float(os.getenv("ACTOR_DET_EVAL_OPPONENT_EPSILON", "0.0"))
# Скользящее окно агрегации точек: шире шага, чтобы график не дёргался.
TRAIN_METRICS_WINDOW_EPISODES = max(1, int(os.getenv("TRAIN_METRICS_WINDOW_EPISODES", "100")))

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
    "VP_DIFF_REWARD_SCALE",
    "VP_DIFF_PENALTY_SCALE",
    "OBJECTIVE_PROGRESS_STEP_SCALE",
    "OBJECTIVE_PROGRESS_STEP_CAP",
    "SHOOT_REWARD_DAMAGE_SCALE",
    "DAMAGE_TAKEN_SCALE",
    "TURN_LIMIT_DRAW_PENALTY",
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


def _make_train_stratagem_tracer() -> StratagemEpisodeTracer | None:
    side = LEARNER_SIDE if LEARNER_SIDE in {"P1", "P2"} else "P1"
    return make_stratagem_tracer_for_train(append_agent_log, learner_side=side)


OPPONENT_POLICY = str(os.getenv("OPPONENT_POLICY", "mirror")).strip().lower() or "mirror"
OPPONENT_AGENT_ID = str(os.getenv("OPPONENT_AGENT_ID", "")).strip()
RULESET_VERSION = str(os.getenv("RULESET_VERSION", "only_war_v2")).strip() or "only_war_v2"
HEURISTIC_MODE = str(os.getenv("HEURISTIC_MODE", "v2")).strip().lower() or "v2"
IO_PROFILER = get_io_profiler()

def to_np_state(s):
    if isinstance(s, (dict, collections.OrderedDict)):
        return np.array(list(s.values()), dtype=np.float32)
    return np.array(s, dtype=np.float32)

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

    ordered_keys = ordered_action_keys(int(len_model))
    legal_by_head = _build_select_action_masks(env, int(len_model))

    if sample > epsilon:
        with torch.no_grad():
            decision = policy_net(state)
            action = greedy_action_list_from_decision(decision, ordered_keys, legal_by_head)
            return torch.tensor([action], device="cpu")
    action_list = sample_action_list_from_space(env, int(len_model), legal_by_head=legal_by_head)
    return torch.tensor([action_list], device="cpu")


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


def format_clip_reward_effective(raw_value: str, enabled: bool, lo=None, hi=None) -> str:
    raw = str(raw_value).strip() or "off"
    if not enabled or lo is None or hi is None:
        return f"[TRAIN][CONFIG] CLIP_REWARD={raw} effective=disabled"
    return f"[TRAIN][CONFIG] CLIP_REWARD={raw} effective=[{float(lo):.3f},{float(hi):.3f}]"


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


def _raise_resume_error(algo: str, path: str, reason: str) -> NoReturn:
    """Громкая остановка при неудачном resume.

    Зачем: если RESUME_CHECKPOINT задан явно, но веса загрузить нельзя, продолжать «с нуля»
    молча опасно — можно впустую потратить часы обучения. Лучше остановиться с понятной
    причиной, чем тихо обучать случайную сеть.
    """
    msg = (
        f"[{algo}][RESUME][ERROR] Не удалось продолжить из чекпойнта — остановка, "
        "чтобы не учиться с нуля незаметно. "
        f"Причина: {reason}. Где: train.py (resume {algo}). path={path}. "
        "Что делать: укажите корректный чекпоинт того же алгоритма и архитектуры в RESUME_CHECKPOINT "
        "или снимите галочку resume в GUI, чтобы осознанно начать с нуля."
    )
    print(msg, flush=True)
    append_agent_log(msg)
    raise RuntimeError(msg)


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

    # TensorBoard: единая точка для всех путей train.py (DQN/PPO/subproc/actor-learner).
    # no-op, если TB выключен/не установлен; ошибки логирования не должны ронять обучение.
    try:
        from core.telemetry.tb_logger import get_tb_logger

        diag = diagnostics or {}
        algo = str(diag.get("algo") or "train")
        tb = get_tb_logger(str(run_id), algo=algo)
        if tb.active:
            step = int(diag.get("global_step") or (episode_row or {}).get("episode") or 0)
            tb.log_episode(episode_row or {}, step=step)
            # Лоссы/LR и прочие числовые величины из diagnostics (служебные ключи пропускаем).
            skip = {"global_step", "update_step"}
            train_metrics = {
                k: v
                for k, v in diag.items()
                if k not in skip and isinstance(v, (int, float)) and not isinstance(v, bool)
            }
            tb.log_train(train_metrics, step=step)
            tb.log_telemetry(step=step)
    except Exception:
        pass


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


def _metrics_plot_gui_paths(run_id: str) -> dict:
    """Стабильные (по run_id) относительные пути PNG для data_*.json."""
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


def _det_eval_read_jsonl_points(run_id: str, metrics_dir: str = METRICS_DIR) -> list[dict]:
    jsonl_path = os.path.join(metrics_dir, f"actor_det_eval_{run_id}.jsonl")
    if not os.path.exists(jsonl_path):
        return []
    by_ep: dict[int, dict] = {}
    try:
        with open(jsonl_path, encoding="utf-8") as f:
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
    """PNG-графики метрик удалены: GUI рисует живые графики (QtCharts) напрямую
    из actor_det_eval_<run_id>.jsonl, PNG никто не читал (см. вкладку «Метрики модели»).
    Возвращаем стабильные пути для схемы data_*.json или None, если точек ещё нет."""
    points = _det_eval_read_jsonl_points(run_id, metrics_dir=metrics_dir)
    if not points:
        return None
    return _metrics_plot_gui_paths(run_id)


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


def _az_episode_mission_fields(info: dict) -> dict:
    """Доп. поля итога AZ/GAZ-эпизода для [TRAIN][EP]-лога и оконных метрик.

    Раньше AZ-ряд нёс только VP → в метриках hp_diff/objective были нулями, а в
    логе нечего было показать про «почему ничья». Достаём из info контроль точек,
    суммарный HP сторон и чистый outcome value target (см. az_mission_bootstrap).
    """
    info = info or {}
    mh = info.get("model health", [])
    ph = info.get("player health", [])
    mh_sum = float(sum(mh)) if isinstance(mh, (list, tuple, np.ndarray)) else float(mh or 0.0)
    ph_sum = float(sum(ph)) if isinstance(ph, (list, tuple, np.ndarray)) else float(ph or 0.0)
    m_ctrl = info.get("model controlled objectives", []) or []
    e_ctrl = info.get("player controlled objectives", []) or []
    m_ctrl_n = len(m_ctrl) if isinstance(m_ctrl, (list, tuple)) else 0
    e_ctrl_n = len(e_ctrl) if isinstance(e_ctrl, (list, tuple)) else 0
    fields = {
        "model_hp_total": mh_sum,
        "enemy_hp_total": ph_sum,
        "model_ctrl_n": int(m_ctrl_n),
        "enemy_ctrl_n": int(e_ctrl_n),
    }
    ov = info.get("az_outcome_value")
    if ov is not None:
        fields["outcome_value"] = float(ov)
    cm = info.get("az_cum_model_ctrl")
    ce = info.get("az_cum_enemy_ctrl")
    if cm is not None and ce is not None:
        fields["cum_model_ctrl"] = float(cm)
        fields["cum_enemy_ctrl"] = float(ce)
    dm = info.get("az_cum_model_dist")
    de = info.get("az_cum_enemy_dist")
    ds = int(info.get("az_dist_samples", 0) or 0)
    if dm is not None and de is not None and ds > 0:
        fields["dist_model_mean"] = float(dm) / ds
        fields["dist_enemy_mean"] = float(de) / ds
    vmin = info.get("az_vt_min")
    vmax = info.get("az_vt_max")
    if vmin is not None and vmax is not None:
        fields["vt_min"] = float(vmin)
        fields["vt_max"] = float(vmax)
    return fields


def format_train_ep_log_line(
    *,
    ep: int,
    total: int | None,
    algo: str = "",
    actor_idx: int | None = None,
    result: str = "draw",
    end_reason: str = "unknown",
    vp_diff: int | float = 0,
    ep_reward: float = 0.0,
    turns: int = 0,
    model_vp: int | None = None,
    enemy_vp: int | None = None,
    model_ctrl_n: int | None = None,
    enemy_ctrl_n: int | None = None,
    hp_diff: float | None = None,
    outcome_value: float | None = None,
    cum_model_ctrl: float | None = None,
    cum_enemy_ctrl: float | None = None,
    dist_model_mean: float | None = None,
    dist_enemy_mean: float | None = None,
    vt_min: float | None = None,
    vt_max: float | None = None,
) -> str:
    """Единая строка итога эпизода для вкладки «Эпизоды» в GUI.

    Опциональные поля (model_vp/enemy_vp/obj/hp_diff/outcome_v) добавляются
    только если переданы — чтобы не ломать старый формат и парсер GUI. Нужны,
    чтобы draw pit (почему ничья) был виден без гадания: см. диагностику
    draw-rate в LOGS_FOR_AGENTS_TRAIN.md.
    """
    pieces = ["[TRAIN][EP]"]
    if total is not None and int(total) > 0:
        pieces.append(f"ep={int(ep)}/{int(total)}")
    else:
        pieces.append(f"ep={int(ep)}")
    if algo:
        pieces.append(f"algo={algo}")
    if actor_idx is not None and int(actor_idx) >= 0:
        pieces.append(f"actor={int(actor_idx)}")
    pieces.extend(
        [
            f"result={result or 'draw'}",
            f"end_reason={end_reason or 'unknown'}",
            f"vp_diff={int(vp_diff)}",
            f"ep_reward={float(ep_reward):.4f}",
            f"turns={int(turns)}",
        ]
    )
    if model_vp is not None:
        pieces.append(f"model_vp={int(model_vp)}")
    if enemy_vp is not None:
        pieces.append(f"enemy_vp={int(enemy_vp)}")
    if model_ctrl_n is not None and enemy_ctrl_n is not None:
        pieces.append(f"obj={int(model_ctrl_n)}/{int(enemy_ctrl_n)}")
    if cum_model_ctrl is not None and cum_enemy_ctrl is not None:
        pieces.append(f"obj_cum={int(cum_model_ctrl)}/{int(cum_enemy_ctrl)}")
    if dist_model_mean is not None and dist_enemy_mean is not None:
        pieces.append(f"dist={float(dist_model_mean):.1f}/{float(dist_enemy_mean):.1f}")
    if vt_min is not None and vt_max is not None:
        pieces.append(f"vt={float(vt_min):.3f}/{float(vt_max):.3f}")
    if hp_diff is not None:
        pieces.append(f"hp_diff={float(hp_diff):+.1f}")
    if outcome_value is not None:
        pieces.append(f"outcome_v={float(outcome_value):.3f}")
    return " ".join(pieces)


def log_train_episode_line(
    row: dict,
    *,
    ep: int | None = None,
    total: int | None = None,
    algo: str = "",
    actor_idx: int | None = None,
) -> None:
    """Печатает [TRAIN][EP] в лог-файл и stdout (если включено в TRAIN_LOG_*)."""
    if not TRAIN_LOG_ENABLED:
        return
    actor_raw = actor_idx if actor_idx is not None else row.get("actor_idx")
    actor_out = int(actor_raw) if actor_raw is not None and int(actor_raw) >= 0 else None
    # Опциональные mission-поля: добавляем в строку только если они есть в row
    # (есть у AZ/GAZ/DQN-рядов; отсутствие → поле просто не печатается).
    model_vp = row.get("model_vp")
    enemy_vp = row.get("player_vp")
    model_ctrl_n = row.get("model_ctrl_n")
    enemy_ctrl_n = row.get("enemy_ctrl_n")
    mh = row.get("model_hp_total")
    eh = row.get("enemy_hp_total")
    hp_diff = (float(mh) - float(eh)) if (mh is not None and eh is not None) else None
    outcome_value = row.get("outcome_value")
    cum_model_ctrl = row.get("cum_model_ctrl")
    cum_enemy_ctrl = row.get("cum_enemy_ctrl")
    dist_model_mean = row.get("dist_model_mean")
    dist_enemy_mean = row.get("dist_enemy_mean")
    vt_min = row.get("vt_min")
    vt_max = row.get("vt_max")
    line = format_train_ep_log_line(
        ep=int(ep if ep is not None else row.get("episode") or 0),
        total=total,
        algo=algo,
        actor_idx=actor_out,
        result=str(row.get("result") or "draw"),
        end_reason=str(row.get("end_reason") or "unknown"),
        vp_diff=int(row.get("vp_diff", 0) or 0),
        ep_reward=float(row.get("ep_reward", 0.0) or 0.0),
        turns=int(row.get("turn", row.get("ep_len", 0)) or 0),
        model_vp=int(model_vp) if model_vp is not None else None,
        enemy_vp=int(enemy_vp) if enemy_vp is not None else None,
        model_ctrl_n=int(model_ctrl_n) if model_ctrl_n is not None else None,
        enemy_ctrl_n=int(enemy_ctrl_n) if enemy_ctrl_n is not None else None,
        hp_diff=hp_diff,
        outcome_value=float(outcome_value) if outcome_value is not None else None,
        cum_model_ctrl=float(cum_model_ctrl) if cum_model_ctrl is not None else None,
        cum_enemy_ctrl=float(cum_enemy_ctrl) if cum_enemy_ctrl is not None else None,
        dist_model_mean=float(dist_model_mean) if dist_model_mean is not None else None,
        dist_enemy_mean=float(dist_enemy_mean) if dist_enemy_mean is not None else None,
        vt_min=float(vt_min) if vt_min is not None else None,
        vt_max=float(vt_max) if vt_max is not None else None,
    )
    if TRAIN_LOG_TO_FILE:
        append_agent_log(line)
    if TRAIN_LOG_TO_CONSOLE:
        print(line, flush=True)


def _train_window_payload_from_rows(
    rows: list[dict],
    *,
    episode_idx: int,
    algo: str,
    training_loss: float | None = None,
    window: int | None = None,
) -> dict:
    """Точка метрик из окна РЕАЛЬНЫХ тренировочных эпизодов (замена DET-eval).

    Отдельные DET-прогоны удалены: тренировка не останавливается, метрики
    агрегируются по последним window строкам ep_rows. Схема payload совпадает
    с прежней DET-схемой — конвейер jsonl → графики → data_*.json → GUI не меняется.
    Честное сравнение моделей — отдельный eval.py.
    """
    w = max(1, int(window or TRAIN_METRICS_WINDOW_EPISODES))
    rows_slice = [r for r in list(rows or [])[-w:] if isinstance(r, dict)]
    n = max(1, len(rows_slice))
    wins = sum(1 for r in rows_slice if str(r.get("result", "")).strip().lower() == "win")
    draws = sum(1 for r in rows_slice if str(r.get("result", "")).strip().lower() == "draw")
    turn_limit = sum(1 for r in rows_slice if str(r.get("end_reason", "")).startswith("turn_limit"))
    wipe_enemy = sum(1 for r in rows_slice if str(r.get("end_reason", "")) == "wipeout_enemy")
    wipe_model = sum(1 for r in rows_slice if str(r.get("end_reason", "")) == "wipeout_model")
    hp_rows = [
        r for r in rows_slice
        if r.get("model_hp_total") is not None and r.get("enemy_hp_total") is not None
    ]
    hp_diff_mean = (
        float(sum(float(r["model_hp_total"]) - float(r["enemy_hp_total"]) for r in hp_rows) / len(hp_rows))
        if hp_rows
        else 0.0
    )
    payload = {
        "eval_episodes": int(n),
        "win_rate": float(wins / n),
        "draw_rate": float(draws / n),
        "turn_limit_rate": float(turn_limit / n),
        "wipeout_enemy_rate": float(wipe_enemy / n),
        "wipeout_model_rate": float(wipe_model / n),
        "vp_diff_mean": float(sum(float(r.get("vp_diff", 0) or 0) for r in rows_slice) / n),
        "model_vp_mean": float(sum(float(r.get("model_vp", 0) or 0) for r in rows_slice) / n),
        "enemy_vp_mean": float(sum(float(r.get("player_vp", 0) or 0) for r in rows_slice) / n),
        "hp_diff_mean": hp_diff_mean,
        "kill_diff_mean": 0.0,
        "reward_mean": float(sum(float(r.get("ep_reward", 0.0) or 0.0) for r in rows_slice) / n),
        "ep_len_mean": float(sum(float(r.get("ep_len", 0) or 0) for r in rows_slice) / n),
        "episode": int(max(int(episode_idx), 1)),
        "algo": str(algo),
        "eval_tag": "train_window",
        "metrics_source": "train_window",
    }
    if training_loss is not None:
        payload["training_loss"] = float(training_loss)
    return payload


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
    # hp_diff из строк (AZ-ряд теперь несёт model_hp_total/enemy_hp_total —
    # см. _az_episode_mission_fields). kill_diff в info нет → честный 0.0.
    hp_rows = [
        r for r in rows
        if r.get("model_hp_total") is not None and r.get("enemy_hp_total") is not None
    ]
    hp_diff_mean = (
        float(sum(float(r["model_hp_total"]) - float(r["enemy_hp_total"]) for r in hp_rows) / len(hp_rows))
        if hp_rows
        else 0.0
    )
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
        "hp_diff_mean": hp_diff_mean,
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

        with open(log_path, encoding="utf-8", errors="replace") as handle:
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
    _log_train_summary(ep_rows, elapsed_s)


def _log_train_summary(ep_rows: list[dict], elapsed_s: float | None) -> None:
    """Итоговая сводка тренировки в журнал GUI (stdout) и лог-файл:
    winrate/reward по всем эпизодам прогона + общее время и скорость."""
    n = len(ep_rows or [])
    if n <= 0:
        return
    wins = sum(1 for r in ep_rows if str(r.get("result", "")) == "win")
    draws = sum(1 for r in ep_rows if str(r.get("result", "")) == "draw")
    reward_mean = sum(float(r.get("ep_reward", 0.0) or 0.0) for r in ep_rows) / n
    vp_diff_mean = sum(float(r.get("vp_diff", 0) or 0) for r in ep_rows) / n
    lines = [
        "[TRAIN][SUMMARY] "
        f"episodes={n} "
        f"win_rate={wins / n:.3f} "
        f"draw_rate={draws / n:.3f} "
        f"loss_rate={(n - wins - draws) / n:.3f} "
        f"reward_mean={reward_mean:.4f} "
        f"vp_diff_mean={vp_diff_mean:.3f}"
    ]
    if elapsed_s is not None and float(elapsed_s) > 0:
        sec_per_ep = float(elapsed_s) / n
        hh = int(elapsed_s // 3600)
        mm = int((elapsed_s % 3600) // 60)
        ss = int(elapsed_s % 60)
        lines.append(
            "[TRAIN][SUMMARY] "
            f"elapsed={hh:02d}:{mm:02d}:{ss:02d} "
            f"sec_per_ep={sec_per_ep:.2f} "
            f"it_per_s={(1.0 / sec_per_ep) if sec_per_ep > 0 else 0.0:.2f}"
        )
    for ln in lines:
        append_agent_log(ln)
        try:
            print(ln, flush=True)
        except Exception:
            pass


def append_agent_log(line: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_line = f"{timestamp} | {line}\n"
    with _TRAIN_LOG_LOCK:
        _TRAIN_LOG_BUFFER.append(full_line)
    _flush_agent_log_buffer(force=False)


def _torch_save_atomic(payload: object, final_path: str, *, label: str = "sync") -> None:
    final_path = str(final_path)
    final_dir = os.path.dirname(final_path)
    if final_dir:
        os.makedirs(final_dir, exist_ok=True)
    tmp_path = f"{final_path}.tmp.{os.getpid()}.{threading.get_ident()}"
    try:
        with open(tmp_path, "wb") as fh:
            torch.save(payload, fh)
            fh.flush()
            os.fsync(fh.fileno())
        last_exc: Exception | None = None
        for attempt in range(6):
            try:
                os.replace(tmp_path, final_path)
                return
            except OSError as exc:
                last_exc = exc
                if attempt >= 5:
                    break
                time.sleep(0.05 * (attempt + 1))
        raise RuntimeError(f"atomic replace failed for {label}: {final_path} exc={last_exc}")
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass


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

    heads = ("move", "attack", "shoot", "charge")
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


def _jsonable_roster(config):
    """Снимок ростера для записи в dqn_dist_train_context.json (SMB → ПК2).

    JSON не хранит кортежи, поэтому weapons (tuple) → list. Остальные поля
    копируются как есть. Обратное преобразование — `_roster_from_context`.
    """
    def _unit(spec):
        return {
            "name": spec.get("name"),
            "weapons": list(spec.get("weapons") or ()),
            "count": spec.get("count"),
            "instance_id": spec.get("instance_id"),
        }

    snapshot = dict(config or {})
    snapshot["enemy_units"] = [_unit(u) for u in config.get("enemy_units", [])]
    snapshot["model_units"] = [_unit(u) for u in config.get("model_units", [])]
    return snapshot


def _roster_from_context(ctx):
    """Восстановить ростер из train-context ПК1 (None, если снимка нет).

    Зеркало `_jsonable_roster`: weapons (list) → tuple, чтобы env на ПК2
    строился из РОВНО того же ростера, что на ПК1 (совпадение contract_hash).
    """
    raw = (ctx or {}).get("roster")
    if not isinstance(raw, dict):
        return None

    def _unit(spec):
        return {
            "name": spec.get("name"),
            "weapons": tuple(spec.get("weapons") or ()),
            "count": spec.get("count"),
            "instance_id": spec.get("instance_id"),
        }

    roster = dict(raw)
    roster["enemy_units"] = [_unit(u) for u in raw.get("enemy_units", [])]
    roster["model_units"] = [_unit(u) for u in raw.get("model_units", [])]
    return roster


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
if is_az_algo(TRAIN_ALGO):
    _AZ_HP_SECTION = az_section_for(TRAIN_ALGO)
elif is_gumbel_az_algo(TRAIN_ALGO):
    _AZ_HP_SECTION = "gumbel_az"
else:
    _AZ_HP_SECTION = "alphazero_tree"
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
elif is_gumbel_az_algo(TRAIN_ALGO):
    AZ_MCTS_MODE = "gumbel"
else:
    AZ_MCTS_MODE = str(AZ_CFG.get("mcts_mode", "tree")).strip().lower() or "tree"
if AZ_MCTS_MODE not in {"proxy", "tree", "gumbel"}:
    AZ_MCTS_MODE = "tree"
AZ_MCTS_TOP_K_PER_HEAD = int(os.getenv("AZ_MCTS_TOP_K_PER_HEAD", str(AZ_CFG.get("mcts_top_k_per_head", 8))))
AZ_MCTS_CANDIDATE_MODE = str(
    os.getenv("MCTS_CANDIDATE_MODE", str(AZ_CFG.get("mcts_candidate_mode", "option")))
).strip().lower() or "option"
if AZ_MCTS_CANDIDATE_MODE not in {"joint", "filter", "option", "option_plus"}:
    AZ_MCTS_CANDIDATE_MODE = "option"
AZ_MCTS_WINDOW_NODES = str(os.getenv("MCTS_WINDOW_NODES", str(AZ_CFG.get("mcts_window_nodes", 0)))).strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
AZ_MCTS_JOINT_BEST_CHILD = str(
    os.getenv("AZ_MCTS_JOINT_BEST_CHILD", str(AZ_CFG.get("mcts_joint_action_from_best_child", 0)))
).strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
AZ_WINDOWED_SELFPLAY = str(
    os.getenv("WINDOWED_SELFPLAY", str(AZ_CFG.get("windowed_selfplay", 1)))
).strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
if "WINDOWED_SELFPLAY" not in os.environ:
    os.environ["WINDOWED_SELFPLAY"] = "1" if AZ_WINDOWED_SELFPLAY else "0"
if "MCTS_WINDOW_NODES" not in os.environ:
    os.environ["MCTS_WINDOW_NODES"] = "1" if AZ_MCTS_WINDOW_NODES else "0"
# B6: phase_obs_features (+24 dims obs). env-var приоритетнее hyperparams; прокидываем в os.environ,
# чтобы spawn-акторы (Windows) построили env с тем же размером obs, что и learner.
AZ_PHASE_OBS_FEATURES = False
AZ_REACTION_VALUE_POLICY = False
if is_az_algo(TRAIN_ALGO):
    AZ_PHASE_OBS_FEATURES = resolve_phase_obs_features(
        env_value=os.getenv("PHASE_OBS_FEATURES"),
        cfg_value=AZ_CFG.get("phase_obs_features", 1),
    )
    os.environ["PHASE_OBS_FEATURES"] = "1" if AZ_PHASE_OBS_FEATURES else "0"
    # B3-full: стратагемы через net-value lookahead (дефолт 1 для AZ; 0 = legacy «всегда реагировать»).
    AZ_REACTION_VALUE_POLICY = resolve_phase_obs_features(
        env_value=os.getenv("AZ_REACTION_VALUE_POLICY"),
        cfg_value=AZ_CFG.get("reaction_value_policy", 1),
    )
    os.environ["AZ_REACTION_VALUE_POLICY"] = "1" if AZ_REACTION_VALUE_POLICY else "0"
else:
    # phase_obs_features теперь дефолт-ВКЛ и для не-AZ алго (dqn/ppo/gumbel_muzero/sampled_muzero):
    # резолвим из секции hyperparams того же алго (env-var приоритетнее), дефолт 1.
    _algo_phase_cfg = data.get(str(TRAIN_ALGO), {}) if isinstance(data, dict) else {}
    _algo_phase_obs = resolve_phase_obs_features(
        env_value=os.getenv("PHASE_OBS_FEATURES"),
        cfg_value=_algo_phase_cfg.get("phase_obs_features", 1),
    )
    os.environ["PHASE_OBS_FEATURES"] = "1" if _algo_phase_obs else "0"
    os.environ["AZ_REACTION_VALUE_POLICY"] = "0"
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


def _az_det_eval_gate_pass(det_payload: dict) -> bool:
    """Диагностика качества DET-eval по порогам AZ_DET_EVAL_GATE_*.

    Только аннотация gate_pass в det-eval JSON: оппонент AZ фиксирован весь прогон,
    снапшот-файл оппонента по результату gate не пишется (его никто не читал).
    """
    return (
        float(det_payload.get("win_rate", 0.0)) >= float(AZ_DET_EVAL_GATE_WIN_MIN)
        and float(det_payload.get("turn_limit_rate", 1.0)) <= float(AZ_DET_EVAL_GATE_TURN_LIMIT_MAX)
        and float(det_payload.get("draw_rate", 1.0)) <= float(AZ_DET_EVAL_GATE_DRAW_MAX)
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
# GAZ едет на общей AZ-инфре, но управляется своими GAZ_* env (свои порты 5565/5567),
# чтобы не пересекаться с AZ-запусками. Приоритет: GAZ_* → AZ_* → секция gumbel_az.
# Для не-GAZ алго GAZ_* игнорируется (AZ без изменений).
_GAZ_ALGO = is_gumbel_az_algo(TRAIN_ALGO)


def _az_family_env(gaz_key: str, az_key: str, default):
    return resolve_az_family_env(gaz_key, az_key, default, is_gumbel=_GAZ_ALGO)


# Mission-bootstrap (AZ/GAZ): слабый сигнал «играй миссию» поверх outcome-таргета
# при outcome_only. По умолчанию 0.0 (ВЫКЛ → поведение бит-в-бит как раньше).
# Резолв GAZ_* → AZ_* → секция конфига. Рекомендуемое значение для включения ≈0.05–0.1.
AZ_MISSION_BOOTSTRAP_COEF = float(
    _az_family_env(
        "GAZ_MISSION_BOOTSTRAP_COEF",
        "AZ_MISSION_BOOTSTRAP_COEF",
        AZ_CFG.get("mission_bootstrap_coef", 0.0),
    )
)
AZ_MISSION_BOOTSTRAP_COEF = max(0.0, min(1.0, AZ_MISSION_BOOTSTRAP_COEF))

# Dense reward-shaping (AZ/GAZ): при relaxed outcome_only value-таргет = outcome +
# вес·tanh(дисконт. отдача per-step env-наград, вкл. objective-progress/proximity из
# reward_config). На порядок сильнее эпизодного bootstrap — даёт градиент «иди на
# точку» на каждом шаге. По умолчанию 0.0 (ВЫКЛ). Реком. старт ≈0.3–0.5.
AZ_REWARD_SHAPING_WEIGHT = float(
    _az_family_env(
        "GAZ_REWARD_SHAPING_WEIGHT",
        "AZ_REWARD_SHAPING_WEIGHT",
        AZ_CFG.get("reward_shaping_weight", 0.0),
    )
)
AZ_REWARD_SHAPING_WEIGHT = max(0.0, min(1.0, AZ_REWARD_SHAPING_WEIGHT))


AZ_INFERENCE_SERVER_REQUESTED = (
    str(_az_family_env("GAZ_INFERENCE_SERVER", "AZ_INFERENCE_SERVER",
                       AZ_CFG.get("inference_server_enabled", 0))).strip() == "1"
)
AZ_INFERENCE_SERVER_MODE = str(
    _az_family_env("GAZ_INFERENCE_SERVER_MODE", "AZ_INFERENCE_SERVER_MODE",
                   AZ_CFG.get("inference_server_mode", "local"))
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
AZ_INFERENCE_REMOTE_HOST = str(_az_family_env(
    "GAZ_INFERENCE_REMOTE_HOST", "AZ_INFERENCE_REMOTE_HOST",
    AZ_CFG.get("inference_remote_host", "127.0.0.1")))
AZ_INFERENCE_REMOTE_PORT = int(_az_family_env(
    "GAZ_INFERENCE_REMOTE_PORT", "AZ_INFERENCE_REMOTE_PORT",
    AZ_CFG.get("inference_remote_port", 5565 if _GAZ_ALGO else 5555)))
AZ_INFERENCE_REMOTE_AUTH_TOKEN = str(_az_family_env(
    "GAZ_INFERENCE_REMOTE_AUTH_TOKEN", "AZ_INFERENCE_REMOTE_AUTH_TOKEN",
    AZ_CFG.get("inference_remote_auth_token", "")))

# --- Distributed self-play (PC2 env workers → rollout ZMQ → learner data_q) ---
AZ_DISTRIBUTED_ACTORS = str(
    _az_family_env("GAZ_DISTRIBUTED_ACTORS", "AZ_DISTRIBUTED_ACTORS",
                   AZ_CFG.get("distributed_actors_enabled", 0))
).strip() == "1"
AZ_DIST_ROLLOUT_BIND = str(
    _az_family_env("GAZ_DIST_ROLLOUT_BIND", "AZ_DIST_ROLLOUT_BIND",
                   AZ_CFG.get("distributed_actors_bind_host", "0.0.0.0"))
).strip() or "0.0.0.0"
AZ_DIST_ROLLOUT_PORT = max(
    1, int(_az_family_env("GAZ_DIST_ROLLOUT_PORT", "AZ_DIST_ROLLOUT_PORT",
                          AZ_CFG.get("distributed_actors_port", 5567 if _GAZ_ALGO else 5557)))
)
AZ_DIST_AUTH_TOKEN = str(
    _az_family_env("GAZ_DIST_AUTH_TOKEN", "AZ_DIST_AUTH_TOKEN",
                   AZ_CFG.get("distributed_actors_auth_token", ""))
).strip() or str(AZ_INFERENCE_REMOTE_AUTH_TOKEN or "")
AZ_DIST_DRAIN_SEC = max(
    1.0, float(os.getenv("AZ_DIST_DRAIN_SEC", str(AZ_CFG.get("distributed_actors_drain_sec", 30.0))))
)
AZ_DIST_ZMQ_HWM = max(8, int(os.getenv("AZ_DIST_ZMQ_HWM", str(AZ_CFG.get("distributed_actors_zmq_hwm", 256)))))

# --- Distributed DQN actors (ПК2 → rollout ZMQ → learner data_q) ---
DQN_DISTRIBUTED_ACTORS = os.getenv(
    "DQN_DISTRIBUTED_ACTORS", str(_DQN_CFG.get("distributed_actors_enabled", 0))
).strip() in {"1", "true", "yes"}
DQN_DIST_ROLLOUT_PORT = max(
    1, int(os.getenv("DQN_DIST_ROLLOUT_PORT", str(_DQN_CFG.get("distributed_rollout_port", 5558))))
)
DQN_DIST_BIND_HOST = str(os.getenv("DQN_DIST_BIND_HOST", "0.0.0.0"))
DQN_DIST_AUTH_TOKEN = str(os.getenv("DQN_DIST_AUTH_TOKEN", str(_DQN_CFG.get("distributed_auth_token", ""))))
DQN_DIST_ZMQ_HWM = max(8, int(os.getenv("DQN_DIST_ZMQ_HWM", str(_DQN_CFG.get("distributed_zmq_hwm", 256)))))
DQN_DIST_DRAIN_SEC = max(
    1.0,
    float(os.getenv("DQN_DIST_DRAIN_SEC", str(_DQN_CFG.get("distributed_actors_drain_sec", 30.0)))),
)
def _dqn_dist_local_episode_fraction() -> float:
    legacy = _DQN_CFG.get("distributed_local_worker_fraction")
    default = _DQN_CFG.get("distributed_local_episode_fraction", legacy if legacy is not None else 0.7)
    return max(
        0.05,
        min(
            0.95,
            float(os.getenv("DQN_DIST_LOCAL_EPISODE_FRACTION", str(default))),
        ),
    )


DQN_DIST_LOCAL_EPISODE_FRACTION = _dqn_dist_local_episode_fraction()
DQN_DIST_PC2_NUM_WORKERS = max(
    1,
    int(os.getenv("DQN_DIST_PC2_NUM_WORKERS", str(_DQN_CFG.get("distributed_pc2_num_workers", 8)))),
)
DQN_DIST_WAIT_PC2 = os.getenv(
    "DQN_DIST_WAIT_PC2", str(_DQN_CFG.get("distributed_wait_pc2", 0))
).strip() in {"1", "true", "yes"}
DQN_DIST_WAIT_PC2_TIMEOUT_SEC = max(
    0.0,
    float(
        os.getenv(
            "DQN_DIST_WAIT_PC2_TIMEOUT_SEC",
            str(_DQN_CFG.get("distributed_wait_pc2_timeout_sec", 600)),
        )
    ),
)
DQN_DIST_BIND_RETRY_SEC = max(
    0.0,
    float(os.getenv("DQN_DIST_BIND_RETRY_SEC", str(_DQN_CFG.get("distributed_bind_retry_sec", 25)))),
)
DQN_DIST_TOPUP_GRACE_SEC = max(
    1.0,
    float(os.getenv("DQN_DIST_TOPUP_GRACE_SEC", str(_DQN_CFG.get("distributed_topup_grace_sec", 5.0)))),
)


def _clear_az_dist_stop_flag() -> None:
    path = az_dist_stop_flag_path(TRAIN_ALGO)
    try:
        removed = False
        if os.path.isfile(path):
            os.remove(path)
            removed = True
        append_agent_log(f"[AZ][DIST] cleared stop.flag removed={int(removed)} path={path}")
    except Exception as exc:
        append_agent_log(f"[AZ][DIST][WARN] не удалось удалить stop.flag: {path} exc={exc}")


def _touch_az_dist_stop_flag() -> None:
    path = az_dist_stop_flag_path(TRAIN_ALGO)
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
        candidate_mode=str(AZ_MCTS_CANDIDATE_MODE),
        window_nodes=bool(AZ_MCTS_WINDOW_NODES),
        joint_action_from_best_child=bool(AZ_MCTS_JOINT_BEST_CHILD),
        terminal_value_win=float(AZ_OUTCOME_VALUE_WIN),
        terminal_value_loss=float(AZ_OUTCOME_VALUE_LOSS),
        terminal_value_draw=float(AZ_OUTCOME_VALUE_DRAW),
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
        candidate_mode=str(AZ_MCTS_CANDIDATE_MODE),
        window_nodes=bool(AZ_MCTS_WINDOW_NODES),
        joint_action_from_best_child=bool(AZ_MCTS_JOINT_BEST_CHILD),
        terminal_value_win=float(AZ_OUTCOME_VALUE_WIN),
        terminal_value_loss=float(AZ_OUTCOME_VALUE_LOSS),
        terminal_value_draw=float(AZ_OUTCOME_VALUE_DRAW),
    )


# --- Gumbel AlphaZero (gumbel_az) search config ---
GAZ_CFG = data.get("gumbel_az", {}) if isinstance(data, dict) else {}
GAZ_NUM_SIMS = max(1, int(os.getenv("GAZ_NUM_SIMULATIONS", str(GAZ_CFG.get("num_simulations", 32)))))
GAZ_NUM_CONSIDERED = max(2, int(os.getenv("GAZ_NUM_CONSIDERED_ACTIONS", str(GAZ_CFG.get("num_considered_actions", 8)))))
GAZ_MAX_DEPTH = max(1, int(os.getenv("GAZ_MAX_DEPTH", str(GAZ_CFG.get("max_depth", 1)))))
GAZ_VALUE_SCALE = float(os.getenv("GAZ_VALUE_SCALE", str(GAZ_CFG.get("value_scale", 0.1))))
GAZ_C_VISIT = float(os.getenv("GAZ_C_VISIT", str(GAZ_CFG.get("c_visit", 50.0))))
GAZ_SIMULATE_ENEMY = str(os.getenv("GAZ_SIMULATE_ENEMY", str(GAZ_CFG.get("simulate_enemy", 0)))).strip() == "1"
GAZ_EVAL_CACHE_SIZE = int(os.getenv("GAZ_EVAL_CACHE_SIZE", str(GAZ_CFG.get("eval_cache_size", 10000))))
GAZ_BATCH_EVAL_SIZE = max(1, int(os.getenv("GAZ_BATCH_EVAL_SIZE", str(GAZ_CFG.get("batch_eval_size", 16)))))
GAZ_JOINT_ACTION = str(os.getenv("GAZ_JOINT_ACTION", str(GAZ_CFG.get("joint_action", 1)))).strip() == "1"

# Лог-теги/числа для AZ-семейства: у gumbel_az показываем [GAZ] и его sims/depth, а не
# generic AZ_MCTS_* (которые для gumbel_az остаются дефолтами секции AZ и путают в логах).
_AZ_LOG_TAG = "GAZ" if is_gumbel_az_algo(TRAIN_ALGO) else "AZ"
_AZ_LOG_SIMS = GAZ_NUM_SIMS if is_gumbel_az_algo(TRAIN_ALGO) else AZ_MCTS_SIMS
_AZ_LOG_DEPTH = GAZ_MAX_DEPTH if is_gumbel_az_algo(TRAIN_ALGO) else AZ_MCTS_MAX_DEPTH


def _gaz_cfg_payload() -> dict:
    return {
        "num_simulations": GAZ_NUM_SIMS,
        "num_considered_actions": GAZ_NUM_CONSIDERED,
        "max_depth": GAZ_MAX_DEPTH,
        "value_scale": GAZ_VALUE_SCALE,
        "c_visit": GAZ_C_VISIT,
        "simulate_enemy": GAZ_SIMULATE_ENEMY,
        "joint_action": GAZ_JOINT_ACTION,
        "eval_cache_size": GAZ_EVAL_CACHE_SIZE,
        "batch_eval_size": GAZ_BATCH_EVAL_SIZE,
        "terminal_value_win": float(AZ_OUTCOME_VALUE_WIN),
        "terminal_value_loss": float(AZ_OUTCOME_VALUE_LOSS),
        "terminal_value_draw": float(AZ_OUTCOME_VALUE_DRAW),
    }


def _build_az_search(net, payload: dict, device, *, evaluator=None):
    """Фабрика бэкенда поиска для AZ-семейства актёров.

    gumbel_az → GumbelAlphaZeroSearch; alphazero_tree/proxy → AlphaZeroFactorizedMCTS.
    payload — это dict, что уже едет в актёр (mcts_cfg_payload). Для gumbel_az он
    содержит gaz-поля (см. _gaz_cfg_payload), для AZ — mcts-поля.
    """
    if is_gumbel_az_algo(TRAIN_ALGO):
        from core.models.gumbel_alphazero_search import GumbelAlphaZeroSearch, GumbelAZSearchConfig
        return GumbelAlphaZeroSearch(
            net,
            config=GumbelAZSearchConfig(
                num_simulations=int(payload.get("num_simulations", GAZ_NUM_SIMS)),
                num_considered_actions=int(payload.get("num_considered_actions", GAZ_NUM_CONSIDERED)),
                max_depth=int(payload.get("max_depth", GAZ_MAX_DEPTH)),
                value_scale=float(payload.get("value_scale", GAZ_VALUE_SCALE)),
                c_visit=float(payload.get("c_visit", GAZ_C_VISIT)),
                temperature_opening_moves=int(AZ_TEMP_OPENING_MOVES),
                eval_cache_size=int(payload.get("eval_cache_size", GAZ_EVAL_CACHE_SIZE)),
                batch_eval_size=int(payload.get("batch_eval_size", GAZ_BATCH_EVAL_SIZE)),
                simulate_enemy=bool(payload.get("simulate_enemy", GAZ_SIMULATE_ENEMY)),
                joint_action=bool(payload.get("joint_action", GAZ_JOINT_ACTION)),
                terminal_value_win=float(payload.get("terminal_value_win", AZ_OUTCOME_VALUE_WIN)),
                terminal_value_loss=float(payload.get("terminal_value_loss", AZ_OUTCOME_VALUE_LOSS)),
                terminal_value_draw=float(payload.get("terminal_value_draw", AZ_OUTCOME_VALUE_DRAW)),
            ),
            device=device,
            evaluator=evaluator,
        )
    return AlphaZeroFactorizedMCTS(
        net,
        config=MCTSConfig(
            simulations=int(payload.get("simulations", AZ_MCTS_SIMS)),
            c_puct=float(payload.get("c_puct", AZ_C_PUCT)),
            c_puct_min=float(payload.get("c_puct_min", AZ_C_PUCT_MIN)),
            c_puct_max=float(payload.get("c_puct_max", AZ_C_PUCT_MAX)),
            c_puct_schedule=str(payload.get("c_puct_schedule", AZ_C_PUCT_SCHEDULE)),
            dirichlet_alpha=float(payload.get("dirichlet_alpha", AZ_DIR_ALPHA)),
            dirichlet_eps=float(payload.get("dirichlet_eps", AZ_DIR_EPS)),
            top_k_per_head=int(payload.get("top_k_per_head", AZ_MCTS_TOP_K_PER_HEAD)),
            max_depth=int(payload.get("max_depth", AZ_MCTS_MAX_DEPTH)),
            mode=str(payload.get("mode", AZ_MCTS_MODE)),
            root_dirichlet_only=bool(payload.get("root_dirichlet_only", AZ_MCTS_ROOT_DIRICHLET_ONLY)),
            eval_cache_size=int(payload.get("eval_cache_size", AZ_MCTS_EVAL_CACHE_SIZE)),
            pw_alpha=float(payload.get("pw_alpha", AZ_PW_ALPHA)),
            pw_beta=float(payload.get("pw_beta", AZ_PW_BETA)),
            prior_weight_early=float(payload.get("prior_weight_early", AZ_PRIOR_WEIGHT_EARLY)),
            temperature_opening_moves=int(AZ_TEMP_OPENING_MOVES),
            batch_eval_size=int(payload.get("batch_eval_size", AZ_MCTS_BATCH_EVAL_SIZE)),
            parallel_simulations=int(payload.get("parallel_simulations", AZ_MCTS_PARALLEL_SIMS)),
            simulate_enemy_in_tree=bool(payload.get("simulate_enemy_in_tree", AZ_MCTS_SIMULATE_ENEMY)),
            candidate_mode=str(payload.get("candidate_mode", AZ_MCTS_CANDIDATE_MODE)),
            window_nodes=bool(payload.get("window_nodes", AZ_MCTS_WINDOW_NODES)),
            joint_action_from_best_child=bool(
                payload.get("joint_action_from_best_child", AZ_MCTS_JOINT_BEST_CHILD)
            ),
            terminal_value_win=float(payload.get("terminal_value_win", AZ_OUTCOME_VALUE_WIN)),
            terminal_value_loss=float(payload.get("terminal_value_loss", AZ_OUTCOME_VALUE_LOSS)),
            terminal_value_draw=float(payload.get("terminal_value_draw", AZ_OUTCOME_VALUE_DRAW)),
        ),
        device=device,
        evaluator=evaluator,
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

# === Sampled MuZero config (SMZ_*) ===
SMZ_CFG = data.get("sampled_muzero", {}) if isinstance(data, dict) else {}
SMZ_LR = float(SMZ_CFG.get("learning_rate", AZ_LR))
SMZ_BATCH_SIZE = int(SMZ_CFG.get("batch_size", 160))
SMZ_UNROLL_STEPS = int(SMZ_CFG.get("unroll_steps", 5))
SMZ_REWARD_LOSS_WEIGHT = float(SMZ_CFG.get("reward_loss_weight", 1.0))
SMZ_VALUE_LOSS_WEIGHT = float(SMZ_CFG.get("value_loss_weight", 1.0))
SMZ_L2_WEIGHT = float(SMZ_CFG.get("l2_weight", 1e-6))
SMZ_DISCOUNT = float(SMZ_CFG.get("discount", 0.997))
SMZ_REPLAY_CAPACITY = int(SMZ_CFG.get("replay_capacity", 400000))
SMZ_NUM_ACTORS = max(1, int(os.getenv("SMZ_NUM_ACTORS", str(SMZ_CFG.get("num_actors", AZ_NUM_ACTORS)))))
SMZ_SYNC_EVERY_UPDATES = max(1, int(os.getenv("SMZ_SYNC_EVERY_UPDATES", str(SMZ_CFG.get("sync_every_updates", 20)))))
SMZ_UPDATES_PER_ROLLOUT = max(1, int(os.getenv("SMZ_UPDATES_PER_ROLLOUT", str(SMZ_CFG.get("updates_per_rollout", 3)))))
SMZ_REPLAY_MIN_SIZE = max(1, int(os.getenv("SMZ_REPLAY_MIN_SIZE", str(SMZ_CFG.get("replay_min_size", 512)))))
SMZ_MAX_POLICY_STALENESS_UPDATES = int(os.getenv("SMZ_MAX_POLICY_STALENESS_UPDATES", str(SMZ_CFG.get("max_policy_staleness_updates", 600))))
SMZ_LATENT_DIM = int(os.getenv("SMZ_LATENT_DIM", str(SMZ_CFG.get("latent_dim", 256))))
SMZ_HIDDEN_DIM = int(os.getenv("SMZ_HIDDEN_DIM", str(SMZ_CFG.get("hidden_dim", 256))))
SMZ_NUM_LAYERS = int(os.getenv("SMZ_NUM_LAYERS", str(SMZ_CFG.get("num_layers", 2))))
SMZ_ACTION_EMBED_DIM = int(os.getenv("SMZ_ACTION_EMBED_DIM", str(SMZ_CFG.get("action_embed_dim", 64))))
SMZ_NUM_SAMPLES = int(os.getenv("SMZ_NUM_SAMPLES", str(SMZ_CFG.get("num_samples", 24))))
SMZ_SAMPLE_TEMP = float(os.getenv("SMZ_SAMPLE_TEMPERATURE", str(SMZ_CFG.get("sample_temperature", 1.0))))
SMZ_SEARCH_TEMP = float(os.getenv("SMZ_SEARCH_TEMPERATURE", str(SMZ_CFG.get("search_temperature", 0.15))))
SMZ_PRIOR_WEIGHT = float(os.getenv("SMZ_PRIOR_WEIGHT", str(SMZ_CFG.get("prior_weight", 0.0))))
SMZ_DEDUP = str(os.getenv("SMZ_DEDUP", str(SMZ_CFG.get("dedup", 1)))).strip() == "1"
SMZ_MAX_GRAD_NORM = float(os.getenv("SMZ_MAX_GRAD_NORM", str(SMZ_CFG.get("max_grad_norm", 0.5))))
SMZ_TBPTT_TRUNCATE = int(os.getenv("SMZ_TBPTT_TRUNCATE", str(SMZ_CFG.get("tbptt_truncate", 3))))
SMZ_CONSISTENCY_W = float(os.getenv("SMZ_CONSISTENCY_W", str(SMZ_CFG.get("consistency_loss_weight", "1.0"))))
SMZ_TEMP_OPENING_MOVES = int(os.getenv("SMZ_TEMP_OPENING_MOVES", str(SMZ_CFG.get("temperature_opening_moves", 12))))
SMZ_TEMP_OPENING = float(os.getenv("SMZ_TEMP_OPENING", str(SMZ_CFG.get("temperature_opening_value", 1.0))))
SMZ_TEMP_LATE = float(os.getenv("SMZ_TEMP_LATE", str(SMZ_CFG.get("temperature_late_value", 0.25))))
SMZ_OUTCOME_ONLY = str(os.getenv("SMZ_OUTCOME_ONLY", str(SMZ_CFG.get("outcome_only", 1)))).strip() == "1"
SMZ_OUTCOME_VALUE_WIN = float(os.getenv("SMZ_OUTCOME_VALUE_WIN", str(SMZ_CFG.get("outcome_value_win", 1.0))))
SMZ_OUTCOME_VALUE_LOSS = float(os.getenv("SMZ_OUTCOME_VALUE_LOSS", str(SMZ_CFG.get("outcome_value_loss", -1.0))))
SMZ_OUTCOME_VALUE_DRAW = float(os.getenv("SMZ_OUTCOME_VALUE_DRAW", str(SMZ_CFG.get("outcome_value_draw", -0.25))))
SMZ_ATOM_RANGE = str(os.getenv("SMZ_ATOM_RANGE", str(SMZ_CFG.get("atom_range", "tight")))).lower()
SMZ_VTRACE_FULL = int(os.getenv("SMZ_VTRACE_FULL", str(SMZ_CFG.get("vtrace_full", 1))))
SMZ_VTRACE_RHO_CLIP = float(os.getenv("SMZ_VTRACE_RHO_CLIP", str(SMZ_CFG.get("vtrace_rho_clip", 0.7))))
SMZ_VTRACE_C_CLIP = float(os.getenv("SMZ_VTRACE_C_CLIP", str(SMZ_CFG.get("vtrace_c_clip", 0.7))))
SMZ_REANALYZE_FRACTION = float(os.getenv("SMZ_REANALYZE_FRACTION", str(SMZ_CFG.get("reanalyze_fraction", 0.15))))
SMZ_EMA_TAU = float(os.getenv("SMZ_EMA_TAU", str(SMZ_CFG.get("ema_tau", 0.005))))
SMZ_LEARNER_COMPILE = str(os.getenv("SMZ_LEARNER_COMPILE", str(SMZ_CFG.get("learner_compile", 1)))).strip() == "1"
# Вариант A: GPU/CPU-акторы; вариант B: inference_server + CPU env workers (local|remote)
SMZ_ACTOR_DEVICE_REQUESTED = str(os.getenv("SMZ_ACTOR_DEVICE", str(SMZ_CFG.get("actor_device", "cuda")))).strip().lower()
if SMZ_ACTOR_DEVICE_REQUESTED not in ("cpu", "cuda", "inference_server"):
    SMZ_ACTOR_DEVICE_REQUESTED = "cuda"
SMZ_ACTOR_MAX_CUDA = max(1, int(os.getenv("SMZ_ACTOR_MAX_CUDA", str(SMZ_CFG.get("actor_max_cuda", 2)))))
SMZ_ACTOR_CPU_FALLBACK_NUM_ACTORS = 8
SMZ_INFERENCE_SERVER_MODE = str(
    os.getenv("SMZ_INFERENCE_SERVER_MODE", str(SMZ_CFG.get("inference_server_mode", "local")))
).strip().lower()
if SMZ_INFERENCE_SERVER_MODE == "inference_server":
    SMZ_INFERENCE_SERVER_MODE = "local"
SMZ_INFERENCE_REMOTE = SMZ_INFERENCE_SERVER_MODE == "remote"
SMZ_INFERENCE_REMOTE_HOST = str(os.getenv("SMZ_INFERENCE_REMOTE_HOST", "127.0.0.1")).strip() or "127.0.0.1"
SMZ_INFERENCE_REMOTE_PORT = max(1, int(os.getenv("SMZ_INFERENCE_REMOTE_PORT", "5560")))
SMZ_INFERENCE_REMOTE_AUTH_TOKEN = str(os.getenv("SMZ_INFERENCE_REMOTE_AUTH_TOKEN", "")).strip()
SMZ_INFERENCE_SERVER_REQUESTED = (
    SMZ_INFERENCE_REMOTE
    or str(os.getenv("SMZ_INFERENCE_SERVER", str(SMZ_CFG.get("inference_server_enabled", 0)))).strip() == "1"
    or SMZ_ACTOR_DEVICE_REQUESTED == "inference_server"
)
SMZ_INFERENCE_SERVER_USING_FALLBACK = (
    SMZ_INFERENCE_SERVER_REQUESTED and not SMZ_INFERENCE_REMOTE and not torch.cuda.is_available()
)
SMZ_INFERENCE_SERVER_ENABLED = SMZ_INFERENCE_SERVER_REQUESTED and (
    SMZ_INFERENCE_REMOTE or torch.cuda.is_available()
)
SMZ_INFERENCE_SERVER_LOCAL = bool(SMZ_INFERENCE_SERVER_ENABLED and not SMZ_INFERENCE_REMOTE)
SMZ_NUM_ENV_WORKERS = max(
    1, int(os.getenv("SMZ_NUM_ENV_WORKERS", str(SMZ_CFG.get("num_env_workers", SMZ_CFG.get("num_actors", 6)))))
)
SMZ_INFERENCE_BATCH_SIZE = max(1, int(os.getenv("SMZ_INFERENCE_BATCH_SIZE", str(SMZ_CFG.get("inference_batch_size", 8)))))
SMZ_INFERENCE_BATCH_INTERVAL_MS = float(
    os.getenv("SMZ_INFERENCE_BATCH_INTERVAL_MS", str(SMZ_CFG.get("inference_batch_interval_ms", 20.0)))
)
SMZ_INFERENCE_TIMEOUT = float(os.getenv("SMZ_INFERENCE_TIMEOUT", str(SMZ_CFG.get("inference_timeout", 5.0))))
SMZ_INFERENCE_REQUEST_QUEUE_MAX = max(
    4, int(os.getenv("SMZ_INFERENCE_REQUEST_QUEUE_MAX", str(SMZ_CFG.get("inference_request_queue_max", 32))))
)
SMZ_INFERENCE_SERVER_COMPILE = str(
    os.getenv("SMZ_INFERENCE_SERVER_COMPILE", str(SMZ_CFG.get("inference_server_compile", 1)))
).strip() == "1"
SMZ_CLEAR_TREE_ON_WEIGHT_SYNC = str(
    os.getenv("SMZ_CLEAR_TREE_ON_WEIGHT_SYNC", str(SMZ_CFG.get("clear_tree_on_weight_sync", 0)))
).strip() == "1"
SMZ_ACTOR_USING_CUDA_FALLBACK = (
    not SMZ_INFERENCE_SERVER_ENABLED
    and SMZ_ACTOR_DEVICE_REQUESTED == "cuda"
    and not torch.cuda.is_available()
)
if SMZ_INFERENCE_SERVER_ENABLED:
    SMZ_ACTOR_DEVICE = "inference_server"
    SMZ_ACTOR_DEVICE_CUDA = False
    SMZ_ACTOR_EFFECTIVE_NUM_ACTORS = int(SMZ_NUM_ENV_WORKERS)
elif SMZ_INFERENCE_SERVER_USING_FALLBACK:
    SMZ_ACTOR_DEVICE = "cpu"
    SMZ_ACTOR_DEVICE_CUDA = False
    SMZ_ACTOR_EFFECTIVE_NUM_ACTORS = int(SMZ_ACTOR_CPU_FALLBACK_NUM_ACTORS)
elif SMZ_ACTOR_USING_CUDA_FALLBACK:
    SMZ_ACTOR_DEVICE = "cpu"
    SMZ_ACTOR_DEVICE_CUDA = False
    SMZ_ACTOR_EFFECTIVE_NUM_ACTORS = int(SMZ_ACTOR_CPU_FALLBACK_NUM_ACTORS)
else:
    SMZ_ACTOR_DEVICE = SMZ_ACTOR_DEVICE_REQUESTED
    SMZ_ACTOR_DEVICE_CUDA = SMZ_ACTOR_DEVICE == "cuda" and torch.cuda.is_available()
    if SMZ_ACTOR_DEVICE_CUDA:
        SMZ_ACTOR_EFFECTIVE_NUM_ACTORS = min(int(SMZ_NUM_ACTORS), int(SMZ_ACTOR_MAX_CUDA))
    else:
        SMZ_ACTOR_EFFECTIVE_NUM_ACTORS = int(SMZ_NUM_ACTORS)
if "SMZ_ACTOR_COMPILE" in os.environ:
    SMZ_ACTOR_COMPILE = str(os.getenv("SMZ_ACTOR_COMPILE", "1")).strip() == "1"
else:
    SMZ_ACTOR_COMPILE = not bool(torch.cuda.is_available())
SMZ_ACTOR_QUEUE_MAX = max(64, int(os.getenv("SMZ_ACTOR_QUEUE_MAX", str(SMZ_CFG.get("actor_queue_max", 256)))))
SMZ_ACTOR_BATCH_SEND = max(8, int(os.getenv("SMZ_ACTOR_BATCH_SEND", str(SMZ_CFG.get("actor_batch_send", 64)))))
SMZ_LR_SCHEDULER = str(os.getenv("SMZ_LR_SCHEDULER", str(SMZ_CFG.get("lr_scheduler", "none"))))
SMZ_LR_WARMUP_STEPS = int(os.getenv("SMZ_LR_WARMUP_STEPS", str(SMZ_CFG.get("lr_warmup_steps", 0))))
SMZ_LR_TOTAL_STEPS = int(os.getenv("SMZ_LR_TOTAL_STEPS", str(SMZ_CFG.get("lr_total_steps", 0))))

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
    global_step: int = 0,
    update_step: int = 0,
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
        "global_step": int(global_step),
        "update_step": int(update_step),
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


def _resume_ppo_checkpoint(actor_critic, optimizer, lr_scheduler=None) -> dict:
    """Тёплый старт PPO из чекпоинта (resume).

    Что делает: грузит веса actor-critic (strict=False), состояние optimizer и lr_scheduler,
    возвращает базовые счётчики (episode_base/global_step/update_step) для продолжения нумерации.
    PPO — on-policy, replay-буфера нет: «продолжение» = тёплый старт с сохранённых весов
    плюс состояние оптимизатора/планировщика LR; роллауты собираются заново текущей сетью.
    Если RESUME_CHECKPOINT не задан — возвращает нули (обычный старт с нуля). Если задан, но
    веса загрузить нельзя — поднимает RuntimeError через _raise_resume_error (громкая остановка,
    чтобы не учиться с нуля незаметно). Сбой optimizer/lr_scheduler — некритичный warning.
    """
    meta = {"episode_base": 0, "global_step": 0, "update_step": 0}
    if not RESUME_CHECKPOINT:
        return meta
    try:
        checkpoint = _load_checkpoint_payload(RESUME_CHECKPOINT)
    except Exception as exc:
        _raise_resume_error("PPO", RESUME_CHECKPOINT, f"не удалось прочитать файл: {exc}")
    if not isinstance(checkpoint, dict):
        _raise_resume_error("PPO", RESUME_CHECKPOINT, "payload не является словарём")
    state = checkpoint.get("actor_critic")
    if not isinstance(state, dict):
        state = checkpoint.get("policy_net")
    if not isinstance(state, dict):
        _raise_resume_error(
            "PPO",
            RESUME_CHECKPOINT,
            "в чекпойнте нет actor_critic/policy_net (нужен PPO checkpoint_ep*.pth)",
        )
    ckpt_arch = ppo_arch_from_payload(checkpoint)
    cur_arch = _ppo_arch_dict(actor_critic)
    if ckpt_arch != cur_arch:
        append_agent_log(
            f"[PPO][RESUME][WARN] arch mismatch checkpoint={ckpt_arch} current={cur_arch}; "
            "strict=False load (часть весов может не загрузиться)."
        )
    try:
        load_actor_critic_state_dict(actor_critic, normalize_state_dict(state), log_fn=append_agent_log)
    except Exception as exc:
        _raise_resume_error("PPO", RESUME_CHECKPOINT, f"не удалось загрузить веса actor-critic: {exc}")
    opt_state = checkpoint.get("optimizer")
    if isinstance(opt_state, dict):
        try:
            optimizer.load_state_dict(opt_state)
        except Exception as exc:
            append_agent_log(
                "[PPO][RESUME][WARN] Не удалось загрузить optimizer state, продолжаю с чистым оптимизатором. "
                f"Где: train.py (_resume_ppo_checkpoint/optimizer.load_state_dict). exc={exc}"
            )
    sched_state = checkpoint.get("lr_scheduler")
    if lr_scheduler is not None and isinstance(sched_state, dict):
        try:
            lr_scheduler.load_state_dict(sched_state)
        except Exception as exc:
            append_agent_log(
                "[PPO][RESUME][WARN] Не удалось загрузить lr_scheduler state, продолжаю без него. "
                f"Где: train.py (_resume_ppo_checkpoint/lr_scheduler.load_state_dict). exc={exc}"
            )
    meta["episode_base"] = int(checkpoint.get("episode", 0) or 0)
    meta["global_step"] = int(checkpoint.get("global_step", 0) or 0)
    meta["update_step"] = int(checkpoint.get("update_step", checkpoint.get("ppo_update_step", 0)) or 0)
    append_agent_log(
        "[PPO][RESUME] "
        f"path={RESUME_CHECKPOINT} episode_base={meta['episode_base']} "
        f"global_step={meta['global_step']} update_step={meta['update_step']}"
    )
    return meta


def _infer_env_shape_from_roster(roster_config: dict) -> tuple[int, list[int]]:
    """Минимальный env probe для режимов без rollout, например distill."""
    b_len = int(roster_config["b_len"])
    b_hei = int(roster_config["b_hei"])
    enemy0, model0 = _build_units_from_config(roster_config, b_len, b_hei)
    env0 = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy0, model=model0, b_len=b_len, b_hei=b_hei)
    try:
        state0, _info0 = env0.reset(options={"m": model0, "e": enemy0, "Type": "big", "trunc": True})
        if isinstance(state0, dict) or "OrderedDict" in str(type(state0)):
            n_observations = len(list(state0.values()))
        else:
            n_observations = int(np.array(state0).shape[0])

        n_actions: list[int] = []
        for key in ordered_action_keys(len(model0)):
            sp = env0.action_space.spaces[key]
            if hasattr(sp, "n"):
                n_actions.append(int(sp.n))
            elif hasattr(sp, "nvec"):
                n_actions.extend([int(x) for x in sp.nvec])
            else:
                raise TypeError(f"Unsupported action space for {key}: {type(sp)}")
        return int(n_observations), n_actions
    finally:
        try:
            env0.close()
        except Exception:
            pass


def main():
    print("\nTraining...\n")
    # Route env/runtime logs (phase-by-phase from warhamEnv) to the same train agent log file.
    # Otherwise they fall back to default response log, and LOGS_FOR_AGENTS_TRAIN.md shows only compact lines.
    set_active_io(ConsoleIO(log_path=str(AGENT_TRAIN_LOG_PATH)))
    clip_reward_enabled, clip_reward_min, clip_reward_max = parse_clip_reward_config(CLIP_REWARD)
    _log_train(format_clip_reward_effective(CLIP_REWARD, clip_reward_enabled, clip_reward_min, clip_reward_max))

    roster_config = _load_roster_config()
    totLifeT = roster_config["totLifeT"]
    episodes_override_raw = str(os.getenv("TRAIN_EPISODES_OVERRIDE", "")).strip()
    if episodes_override_raw:
        try:
            totLifeT = max(1, int(episodes_override_raw))
        except ValueError:
            warn_line = (
                "[TRAIN][WARN] TRAIN_EPISODES_OVERRIDE не число. "
                "Где: train.py (main). Что делать дальше: используйте целое > 0."
            )
            if TRAIN_LOG_TO_FILE:
                append_agent_log(warn_line)
            if TRAIN_LOG_TO_CONSOLE:
                print(warn_line)

    legacy_flag = str(os.getenv("PRO_ACTOR_LEARNER", "1")).strip()
    if legacy_flag != "1":
        warn_line = (
            "[TRAIN][WARN] PRO_ACTOR_LEARNER=0 больше не поддерживается: legacy non-pro pipeline удалён. "
            "Где: train.py (main). Что делать дальше: уберите PRO_ACTOR_LEARNER=0; запуск продолжится через actor-learner."
        )
        if TRAIN_LOG_TO_FILE:
            append_agent_log(warn_line)
        if TRAIN_LOG_TO_CONSOLE:
            print(warn_line)

    if TRAIN_LOG_TO_CONSOLE:
        print("[TRAIN][MODE] PRO_ACTOR_LEARNER=1 (actor-learner only)")
        print(f"[TRAIN][MODE] TRAIN_ALGO={TRAIN_ALGO}")

    if TRAIN_ALGO == "distill":
        n_observations, n_actions = _infer_env_shape_from_roster(roster_config)
        append_agent_log("[DISTILL] Запуск режима дистилляции teacher→DQN student")
        _run_dqn_distill_mode(
            n_observations,
            n_actions,
            steps=int(os.getenv("DISTILL_STEPS", "200")),
        )
        return

    if is_az_algo(TRAIN_ALGO) or is_gumbel_az_algo(TRAIN_ALGO):
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
                _gmz_actor_mode = f"inference_server + {GMZ_ACTOR_EFFECTIVE_NUM_ACTORS} env workers"
            elif GMZ_INFERENCE_SERVER_USING_FALLBACK:
                _gmz_actor_mode = f"variant A CPU fallback (IS недоступен, actors={GMZ_ACTOR_EFFECTIVE_NUM_ACTORS})"
            elif GMZ_ACTOR_DEVICE_CUDA:
                _gmz_actor_mode = f"CUDA (max {GMZ_ACTOR_MAX_CUDA})"
            else:
                _gmz_actor_mode = "CPU"
            if GMZ_ACTOR_USING_CUDA_FALLBACK:
                _gmz_actor_mode = f"CPU fallback (запрошен cuda, num_actors={GMZ_ACTOR_EFFECTIVE_NUM_ACTORS})"
            print(f"[TRAIN][MODE] PRO_ACTOR_LEARNER=1 (Gumbel MuZero {_gmz_actor_mode} + learner GPU)")
        _main_actor_learner_gumbel_muzero(
            roster_config=roster_config,
            totLifeT=totLifeT,
            clip_reward_enabled=clip_reward_enabled,
            clip_reward_min=clip_reward_min,
            clip_reward_max=clip_reward_max,
        )
        return

    if TRAIN_ALGO == "sampled_muzero":
        if TRAIN_LOG_TO_CONSOLE:
            print("[TRAIN][MODE] PRO_ACTOR_LEARNER=1 (Sampled MuZero actors + learner GPU)")
        _main_actor_learner_sampled_muzero(
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

    raise ValueError(
        f"[TRAIN][ERROR] Неподдерживаемый TRAIN_ALGO={TRAIN_ALGO!r}. "
        "Где: train.py (main). Что делать дальше: выберите dqn/ppo/alphazero_tree/gumbel_az/gumbel_muzero/sampled_muzero."
    )


def _push_dqn_batch_steps_to_memory(memory, batch_steps) -> int:
    """Push one actor batch into DQN replay as isolated CPU tensors."""
    steps = list(batch_steps or [])
    if not steps:
        return 0

    states_np = np.stack(
        [np.asarray(s_np, dtype=np.float32) for (s_np, _a, _r, _ns, _done, _n) in steps],
        axis=0,
    )
    state_batch_t = torch.tensor(states_np, device="cpu", dtype=torch.float32)
    action_batch_t = torch.tensor(
        [a_list for (_s, a_list, _r, _ns, _done, _n) in steps],
        device="cpu",
        dtype=torch.long,
    )
    reward_batch_t = torch.tensor(
        [float(r_sum) for (_s, _a, r_sum, _ns, _done, _n) in steps],
        device="cpu",
        dtype=torch.float32,
    )

    next_pos_by_step: dict[int, int] = {}
    next_rows = []
    for idx, (_s, _a, _r, ns_np, _done, _n) in enumerate(steps):
        if ns_np is not None:
            next_pos_by_step[idx] = len(next_rows)
            next_rows.append(np.asarray(ns_np, dtype=np.float32))

    next_batch_t = None
    if next_rows:
        next_batch_t = torch.tensor(np.stack(next_rows, axis=0), device="cpu", dtype=torch.float32)

    for idx, (_s, _a, _r, ns_np, _done, n_count) in enumerate(steps):
        next_state_t = None
        if ns_np is not None and next_batch_t is not None:
            next_idx = next_pos_by_step[idx]
            next_state_t = next_batch_t[next_idx : next_idx + 1]
        memory.push(
            state_batch_t[idx : idx + 1].clone(),
            action_batch_t[idx : idx + 1].clone(),
            next_state_t.clone() if next_state_t is not None else None,
            reward_batch_t[idx : idx + 1].clone(),
            int(n_count),
            None,
        )

    return len(steps)


def _resolve_dqn_updates_per_batch(
    base_updates: int,
    *,
    num_local_actors: int,
    num_remote_actors: int = 0,
    distributed_enabled: bool = False,
    adapt_enabled: bool = True,
) -> int:
    base = max(1, int(base_updates))
    local = max(1, int(num_local_actors))
    remote = max(0, int(num_remote_actors))
    if not distributed_enabled or not adapt_enabled or remote <= 0:
        return base
    total = max(1, local + remote)
    return max(1, int(round(float(base) * float(local) / float(total))))


def _format_dqn_queue_metrics(
    *,
    qsize: int | None,
    dropped_batches: int,
    push_batch_ms: float,
    optimize_ms: float,
    updates_per_sec: float,
    batches: int,
    transitions: int,
    updates: int,
    interval_s: float,
) -> str:
    qsize_text = "unknown" if qsize is None else str(int(qsize))
    return (
        "[DQN][PERF] "
        f"qsize={qsize_text} "
        f"dropped_batches={int(dropped_batches)} "
        f"push_batch_ms={float(push_batch_ms):.2f} "
        f"optimize_ms={float(optimize_ms):.2f} "
        f"updates/sec={float(updates_per_sec):.2f} "
        f"batches={int(batches)} "
        f"transitions={int(transitions)} "
        f"updates={int(updates)} "
        f"interval_s={float(interval_s):.1f}"
    )


def _main_actor_learner(*, roster_config, totLifeT, clip_reward_enabled, clip_reward_min, clip_reward_max) -> None:
    """
    Actor-Learner MVP (Windows-friendly, spawn):
    - Actors (CPU) гоняют env и шлют transitions батчами в очередь.
    - Learner (GPU) читает очередь, наполняет replay и делает optimize_model.
    Важно: это отдельный режим, не ломает текущий pipeline (ACTOR_LEARNER=0 по умолчанию).
    """
    num_actors = max(1, int(os.getenv("NUM_ACTORS", "8")))
    dqn_dist_local_episodes = int(totLifeT)
    dqn_dist_remote_episodes = 0
    if DQN_DISTRIBUTED_ACTORS:
        dqn_dist_local_episodes, dqn_dist_remote_episodes = resolve_dqn_dist_episode_split(
            total_episodes=int(totLifeT),
            local_fraction=DQN_DIST_LOCAL_EPISODE_FRACTION,
        )
        append_agent_log(
            f"[DQN][DIST] episodes total={int(totLifeT)} "
            f"local={dqn_dist_local_episodes} pc2={dqn_dist_remote_episodes} "
            f"local_fraction={DQN_DIST_LOCAL_EPISODE_FRACTION:.2f} "
            f"actors_pc1={num_actors} actors_pc2={DQN_DIST_PC2_NUM_WORKERS}"
        )
    batch_send = max(8, int(os.getenv("ACTOR_BATCH_SEND", "32")))
    dqn_updates_default = _DQN_CFG.get("updates_per_batch")
    if dqn_updates_default is None:
        dqn_updates_default = _DQN_CFG.get("updates_per_step")
    if dqn_updates_default is None and isinstance(data, dict):
        dqn_updates_default = data.get("updates_per_step")
    if dqn_updates_default is None:
        dqn_updates_default = "8"
    base_updates_per_batch = max(1, int(os.getenv("UPDATES_PER_BATCH", str(dqn_updates_default))))
    adapt_updates_per_batch = os.getenv("DQN_DIST_ADAPT_UPDATES_PER_BATCH", "1").strip().lower() in {"1", "true", "yes"}
    updates_per_batch = _resolve_dqn_updates_per_batch(
        base_updates_per_batch,
        num_local_actors=num_actors,
        num_remote_actors=DQN_DIST_PC2_NUM_WORKERS if DQN_DISTRIBUTED_ACTORS else 0,
        distributed_enabled=bool(DQN_DISTRIBUTED_ACTORS),
        adapt_enabled=adapt_updates_per_batch,
    )
    if DQN_DISTRIBUTED_ACTORS and updates_per_batch != base_updates_per_batch:
        append_agent_log(
            f"[DQN][DIST] adaptive updates_per_batch={updates_per_batch} "
            f"(base={base_updates_per_batch}, actors_pc1={num_actors}, actors_pc2={DQN_DIST_PC2_NUM_WORKERS})"
        )
    queue_max = max(64, int(os.getenv("ACTOR_QUEUE_MAX", "256")))
    if DQN_DISTRIBUTED_ACTORS:
        queue_max = max(
            queue_max,
            int(os.getenv("DQN_DIST_ACTOR_QUEUE_MAX", str(_DQN_CFG.get("distributed_actor_queue_max", 1024)))),
        )

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

    ordered_keys = ordered_action_keys(len(model0))
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
        extras=dqn_dist_env_contract_extras(num_local_actors=num_actors),
    )

    # Self-play opponent snapshot (optional): загружаем один раз в learner и раздаём акторам.
    opponent_spec: OpponentSpec | None = None
    opponent_eps = float(SELF_PLAY_OPPONENT_EPSILON)
    if SELF_PLAY_ENABLED:
        try:
            if SELF_PLAY_OPPONENT_MODE == "fixed_checkpoint" and SELF_PLAY_FIXED_PATH:
                checkpoint = torch.load(SELF_PLAY_FIXED_PATH, map_location="cpu", weights_only=False)
                checkpoint_algo = str(checkpoint.get("algo", "dqn")).strip().lower() if isinstance(checkpoint, dict) else "dqn"
                if checkpoint_algo not in {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero", "sampled_muzero"}:
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
                    metadata=dict(checkpoint) if isinstance(checkpoint, dict) else {},
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

    # Resume до формирования init_weights, чтобы акторы (локальные и ПК2 через sync_path)
    # стартовали с восстановленных весов, а не случайных.
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
            append_agent_log(
                "[RESUME][WARN] Не удалось загрузить lr_scheduler state (DQN actor-learner). "
                f"Где: train.py (_main_actor_learner). Детали: {exc}"
            )
    target_net.eval()
    scaler = torch.cuda.amp.GradScaler(enabled=bool(USE_AMP and device.type == "cuda"))

    if DQN_REACTION_VALUE_POLICY:
        append_agent_log(
            "[DQN][CONFIG] reaction_value_policy=ON (max-Q proxy, learner_only; actors устанавливают на env)"
        )

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

    # --- Distributed actors (ПК2): receiver + SMB train-context ---
    rollout_receiver = None
    if DQN_DISTRIBUTED_ACTORS:
        env_contract_hash = str(env_contract.get("contract_hash", "") or "")
        # Чистим stop.flag прошлого прогона, иначе ПК2-воркеры выйдут сразу при старте.
        try:
            if clear_dqn_dist_stop_flag():
                append_agent_log("[DQN][DIST] очищен stop.flag прошлого прогона")
        except Exception:
            pass
        rollout_receiver = RolloutReceiver(
            data_q,
            bind_host=DQN_DIST_BIND_HOST,
            bind_port=DQN_DIST_ROLLOUT_PORT,
            expected_contract_hash=env_contract_hash,
            auth_token=DQN_DIST_AUTH_TOKEN,
            zmq_hwm=DQN_DIST_ZMQ_HWM,
            log_fn=append_agent_log,
            bind_retry_sec=DQN_DIST_BIND_RETRY_SEC,
            log_prefix="[DQN][DIST]",
            # Своевременный прогресс ПК2 для GUI: маркер в stdout (GUI читает stdout,
            # не log-файл), эмитится потоком приёмника сразу при приёме ep — не ждёт,
            # пока learner добьёт backlog ep из data_q. Префикс не в GUI-allowlist —
            # видимый лог не засоряется (только парсинг прогресса).
            ep_marker_fn=lambda n: print(f"[TRAIN][DIST][PC2] pc2_ep_accepted={n}", flush=True),
        )
        rollout_receiver.start()
        try:
            torch.save({"state_dict": init_weights}, sync_path)
        except Exception as exc:
            append_agent_log(f"[DQN][DIST][WARN] не удалось записать стартовые веса {sync_path}: {exc}")
        try:
            write_dqn_dist_train_context({
                "env_contract_hash": env_contract_hash,
                "env_contract_extras": dqn_dist_env_contract_extras(num_local_actors=num_actors),
                "opponent_agent_id": str(OPPONENT_AGENT_ID or ""),
                "learner_side": str(learner_side_cfg),
                "n_observations": int(n_observations),
                "n_actions": list(n_actions),
                "rollout_port": int(DQN_DIST_ROLLOUT_PORT),
                "auth_token": str(DQN_DIST_AUTH_TOKEN or ""),
                "mission": str(normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))),
                "ruleset_version": str(RULESET_VERSION),
                "roster": _jsonable_roster(roster_config),
                "local_episode_total": int(dqn_dist_local_episodes),
                "remote_episode_total": int(dqn_dist_remote_episodes),
                "num_local_actors": int(num_actors),
                "pc2_num_workers": int(DQN_DIST_PC2_NUM_WORKERS),
                "distributed_local_episode_fraction": float(DQN_DIST_LOCAL_EPISODE_FRACTION),
                # Арх-параметры сети — чтобы ПК2 собрал сеть под форму latest_policy.pth.
                "ensemble_size": int(DQN_ENSEMBLE_SIZE),
                "hidden_size": int(DQN_HIDDEN_SIZE),
                "num_layers": int(DQN_NUM_LAYERS),
                # Транспорт: ПК2 берёт SNDHWM с ПК1 (иначе локальный дефолт 256).
                "zmq_hwm": int(DQN_DIST_ZMQ_HWM),
            })
        except Exception as exc:
            append_agent_log(f"[DQN][DIST][WARN] не удалось записать train-context: {exc}")
        append_agent_log(
            f"[DQN][DIST] receiver bind=:{DQN_DIST_ROLLOUT_PORT} "
            f"contract_hash={env_contract_hash or '-'} sync={sync_path}"
        )
        if DQN_DIST_WAIT_PC2:
            append_agent_log("[TRAIN][PHASE] waiting_pc2")
            print("[TRAIN][PHASE] waiting_pc2", flush=True)
            try:
                wait_dqn_dist_remote_workers(
                    rollout_receiver,
                    min_workers=int(DQN_DIST_PC2_NUM_WORKERS),
                    timeout_sec=float(DQN_DIST_WAIT_PC2_TIMEOUT_SEC),
                    log_fn=lambda msg: (append_agent_log(msg), print(msg, flush=True)),
                )
            except RuntimeError as exc:
                rollout_receiver.stop()
                raise RuntimeError(str(exc)) from exc

    local_actor_episode_plan = (
        split_count_among_workers(total=int(dqn_dist_local_episodes), num_workers=int(num_actors))
        if DQN_DISTRIBUTED_ACTORS
        else []
    )
    cr_min = 0.0 if clip_reward_min is None else float(clip_reward_min)
    cr_max = 0.0 if clip_reward_max is None else float(clip_reward_max)

    def _spawn_dqn_local_actor(actor_idx: int, episodes: int) -> mp.Process:
        proc = ctx.Process(
            target=_actor_learner_actor_entry,
            args=(
                int(actor_idx),
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
        proc.start()
        return proc

    procs = []
    for a_idx in range(num_actors):
        if DQN_DISTRIBUTED_ACTORS:
            episodes = int(local_actor_episode_plan[a_idx])
        else:
            base = int(totLifeT) // int(num_actors)
            rem = int(totLifeT) % int(num_actors)
            episodes = int(base + (1 if a_idx < rem else 0))
        procs.append(_spawn_dqn_local_actor(a_idx, episodes))

    done_actors = 0
    optimize_steps = int(resume_meta.get("optimize_steps", 0) or 0)
    global_step = int(resume_meta.get("global_step", 0) or 0)
    # episodes_finished — счётчик ТЕКУЩЕГО запуска (totLifeT = доп. игры за прогон).
    # resume_episode_base — кумулятивный сдвиг из чекпойнта (для нумерации сохранений/агента).
    episodes_finished = 0
    resume_episode_base = int(resume_meta.get("episode", 0) or 0)
    if RESUME_CHECKPOINT:
        append_agent_log(
            "[RESUME] DQN actor-learner продолжение: "
            f"episode_base={resume_episode_base} global_step={global_step} "
            f"optimize_steps={optimize_steps} replay_size={int(resume_meta.get('replay_size', 0) or 0)} "
            f"(доп. игр за запуск={int(totLifeT)})"
        )
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
    try:
        dqn_perf_log_every_sec = max(1.0, float(os.getenv("DQN_QUEUE_METRICS_EVERY_SEC", "30")))
    except Exception:
        dqn_perf_log_every_sec = 30.0
    perf_interval_started = time.perf_counter()
    perf_push_ms_total = 0.0
    perf_opt_ms_total = 0.0
    perf_batches = 0
    perf_transitions = 0
    perf_opt_calls = 0
    perf_updates = 0

    dist_draining = False
    dist_stop_sent = False
    dist_drain_until = 0.0
    dist_last_ep_progress_mono = time.monotonic()
    dist_collect_stall_sec = max(
        30.0,
        float(os.getenv("DQN_DIST_COLLECT_STALL_SEC", "120")),
    )
    dist_topup_proc: mp.Process | None = None
    dist_idle_since_mono: float | None = None

    def _dqn_queue_size() -> int | None:
        try:
            return max(0, int(data_q.qsize()))
        except Exception:
            return None

    def _dqn_dropped_batches() -> int:
        if rollout_receiver is None:
            return 0
        try:
            return int(rollout_receiver.dropped_queue_count())
        except Exception:
            try:
                return int(getattr(rollout_receiver, "_dropped_queue", 0))
            except Exception:
                return 0

    def _emit_dqn_perf_metrics(*, force: bool = False) -> None:
        nonlocal perf_interval_started
        nonlocal perf_push_ms_total, perf_opt_ms_total
        nonlocal perf_batches, perf_transitions, perf_opt_calls, perf_updates

        now = time.perf_counter()
        interval_s = max(0.000001, now - perf_interval_started)
        if not force and interval_s < dqn_perf_log_every_sec:
            return

        qsize = _dqn_queue_size()
        dropped_batches = _dqn_dropped_batches()
        has_signal = (
            perf_batches > 0
            or perf_opt_calls > 0
            or dropped_batches > 0
            or (qsize is not None and qsize > 0)
        )
        if not has_signal:
            perf_interval_started = now
            return

        push_batch_ms = perf_push_ms_total / float(perf_batches) if perf_batches > 0 else 0.0
        optimize_ms = perf_opt_ms_total / float(perf_opt_calls) if perf_opt_calls > 0 else 0.0
        updates_per_sec = float(perf_updates) / interval_s
        append_agent_log(
            _format_dqn_queue_metrics(
                qsize=qsize,
                dropped_batches=dropped_batches,
                push_batch_ms=push_batch_ms,
                optimize_ms=optimize_ms,
                updates_per_sec=updates_per_sec,
                batches=perf_batches,
                transitions=perf_transitions,
                updates=perf_updates,
                interval_s=interval_s,
            )
        )

        perf_interval_started = now
        perf_push_ms_total = 0.0
        perf_opt_ms_total = 0.0
        perf_batches = 0
        perf_transitions = 0
        perf_opt_calls = 0
        perf_updates = 0

    def _dqn_dist_remote_alive() -> int:
        if rollout_receiver is None:
            return 0
        # Короткий stale при drain: не ждём 30 с, пока heartbeat «протухнет».
        return int(rollout_receiver.active_remote_workers(stale_sec=5.0))

    def _dqn_dist_topup_shortfall() -> int:
        _topup_alive = dist_topup_proc is not None and dist_topup_proc.is_alive()
        return int(
            compute_dqn_dist_topup_episodes(
                episodes_finished=int(episodes_finished),
                total_episodes=int(totLifeT),
                local_actors_done=int(done_actors),
                num_local_actors=int(num_actors),
                remote_alive=int(_dqn_dist_remote_alive()),
                topup_process_alive=bool(_topup_alive),
            )
        )

    def _spawn_dqn_dist_topup(shortfall: int) -> None:
        nonlocal dist_topup_proc, dist_idle_since_mono
        need = max(0, int(shortfall))
        if need <= 0:
            return
        dist_topup_proc = _spawn_dqn_local_actor(int(DQN_DIST_TOPUP_ACTOR_IDX), need)
        procs.append(dist_topup_proc)
        dist_idle_since_mono = None
        for _ln in (
            f"[TRAIN][DIST] topup_start shortfall={need} actor_idx={int(DQN_DIST_TOPUP_ACTOR_IDX)} "
            f"ep_done={int(episodes_finished)}/{int(totLifeT)}",
            "[TRAIN][PHASE] topup",
        ):
            append_agent_log(_ln)
            print(_ln, flush=True)

    def _dqn_dist_should_finish_drain() -> tuple[bool, str]:
        if not dist_draining:
            return False, ""
        if done_actors < num_actors:
            return False, "local_actors_pending"
        remote_alive = _dqn_dist_remote_alive()
        if remote_alive == 0:
            return True, "all_workers_idle"
        if time.monotonic() >= dist_drain_until:
            return True, "drain_budget_elapsed"
        return False, "drain_waiting"

    if DQN_DISTRIBUTED_ACTORS:
        append_agent_log("[TRAIN][PHASE] collecting")
        print("[TRAIN][PHASE] collecting", flush=True)

    while True:
        if not DQN_DISTRIBUTED_ACTORS:
            if done_actors >= num_actors:
                break
        else:
            if int(episodes_finished) >= int(totLifeT):
                if not dist_stop_sent:
                    dist_stop_sent = True
                    dist_drain_until = time.monotonic() + float(DQN_DIST_DRAIN_SEC)
                    touch_dqn_dist_stop_flag()
                    _ln = (
                        f"[TRAIN][DIST] stop_requested ep_done={int(episodes_finished)}/{int(totLifeT)} "
                        f"drain_budget_max={int(round(float(DQN_DIST_DRAIN_SEC)))}s"
                    )
                    append_agent_log(_ln)
                    print(_ln, flush=True)
                if not dist_draining:
                    _remote_alive = _dqn_dist_remote_alive()
                    _drain_left = max(0, int(round(dist_drain_until - time.monotonic())))
                    dist_draining = True
                    for _ln in (
                        "[TRAIN][PHASE] draining",
                        f"[TRAIN][DIST] remote_alive={_remote_alive} "
                        f"ep_done={int(episodes_finished)}/{int(totLifeT)} drain_left_max={_drain_left}s",
                    ):
                        append_agent_log(_ln)
                        print(_ln, flush=True)
                _finish_drain, _drain_reason = _dqn_dist_should_finish_drain()
                if _finish_drain:
                    append_agent_log(
                        f"[TRAIN][DIST] drain_done reason={_drain_reason} "
                        f"ep_done={int(episodes_finished)}/{int(totLifeT)} "
                        f"local_done={done_actors}/{num_actors} remote_alive={_dqn_dist_remote_alive()}"
                    )
                    break
        try:
            kind, payload = data_q.get(timeout=1.0)
        except mp_queue.Empty:
            _emit_dqn_perf_metrics()
            if DQN_DISTRIBUTED_ACTORS and dist_draining:
                _remote_alive = _dqn_dist_remote_alive()
                _drain_left = max(0, int(round(dist_drain_until - time.monotonic())))
                dist_line = (
                    f"[TRAIN][DIST] remote_alive={_remote_alive} "
                    f"ep_done={int(episodes_finished)}/{int(totLifeT)} drain_left_max={_drain_left}s"
                )
                print(dist_line, flush=True)
                append_agent_log(dist_line)
                _finish_drain, _drain_reason = _dqn_dist_should_finish_drain()
                if _finish_drain:
                    append_agent_log(
                        f"[TRAIN][DIST] drain_done reason={_drain_reason} "
                        f"ep_done={int(episodes_finished)}/{int(totLifeT)} "
                        f"local_done={done_actors}/{num_actors} remote_alive={_remote_alive}"
                    )
                    break
            elif DQN_DISTRIBUTED_ACTORS and not dist_draining:
                _remote_alive = _dqn_dist_remote_alive()
                _shortfall = _dqn_dist_topup_shortfall()
                _topup_alive = dist_topup_proc is not None and dist_topup_proc.is_alive()
                if dist_topup_proc is not None and not dist_topup_proc.is_alive():
                    dist_topup_proc = None
                if _shortfall > 0:
                    if dist_idle_since_mono is None:
                        dist_idle_since_mono = time.monotonic()
                    elif (
                        dist_topup_proc is None
                        and (time.monotonic() - float(dist_idle_since_mono)) >= float(DQN_DIST_TOPUP_GRACE_SEC)
                    ):
                        _spawn_dqn_dist_topup(_shortfall)
                else:
                    dist_idle_since_mono = None
                if _topup_alive or (_shortfall > 0 and dist_topup_proc is not None):
                    dist_last_ep_progress_mono = time.monotonic()
                elif _shortfall > 0 and dist_idle_since_mono is not None:
                    dist_last_ep_progress_mono = time.monotonic()
                _stall_sec = time.monotonic() - float(dist_last_ep_progress_mono)
                if _stall_sec >= float(dist_collect_stall_sec):
                    if _shortfall > 0 and dist_topup_proc is None:
                        _spawn_dqn_dist_topup(_shortfall)
                    elif _shortfall > 0:
                        for _ln in (
                            f"[TRAIN][DIST][WARN] добор не закрыл дефицит ep "
                            f"(ep_done={int(episodes_finished)}/{int(totLifeT)} shortfall={_shortfall}). "
                            "Где: _main_actor_learner (сбор). Завершаем сбор.",
                            "[TRAIN][PHASE] done",
                        ):
                            append_agent_log(_ln)
                            print(_ln, flush=True)
                        break
                    else:
                        for _ln in (
                            f"[TRAIN][DIST][WARN] нет новых ep {_stall_sec:.0f}s "
                            f"(ep_done={int(episodes_finished)}/{int(totLifeT)} "
                            f"local_done={done_actors}/{num_actors} remote_alive={_remote_alive}). "
                            "Где: _main_actor_learner (сбор). Завершаем сбор.",
                            "[TRAIN][PHASE] done",
                        ):
                            append_agent_log(_ln)
                            print(_ln, flush=True)
                        break
            continue

        if kind == "error":
            raise RuntimeError(payload)
        if kind == "done":
            done_actors += 1
            continue
        if kind == "ep":
            if isinstance(payload, dict):
                if DQN_DISTRIBUTED_ACTORS and int(episodes_finished) >= int(totLifeT):
                    continue
                if payload.get("episode") is None:
                    payload["episode"] = len(ep_rows) + 1
                ep_rows.append(payload)
                episodes_finished = len(ep_rows)
                dist_last_ep_progress_mono = time.monotonic()
                target_n = min(int(totLifeT), int(episodes_finished))
                if target_n > int(pbar.n):
                    pbar.update(target_n - int(pbar.n))
                # GUI прогресс читает stdout и парсит шаблон ep=X/Y.
                if (episodes_finished % ACTOR_PROGRESS_STDOUT_EVERY == 0) or (episodes_finished >= int(totLifeT)):
                    try:
                        print(f"ep={episodes_finished}/{totLifeT}", flush=True)
                    except Exception:
                        pass
                log_train_episode_line(
                    payload,
                    ep=int(episodes_finished),
                    total=int(totLifeT),
                    algo="dqn",
                    actor_idx=int(payload.get("actor_idx", -1) or -1),
                )
                # Per-episode стратагемная сводка (DQN)
                if _trace_ep_enabled(int(episodes_finished)):
                    from core.telemetry.stratagem_trace import episode_stratagem_summary_line
                    _strat_line = episode_stratagem_summary_line(payload, ep_label=int(episodes_finished), tag="TRAIN")
                    if _strat_line:
                        append_agent_log(_strat_line)

                # Periodic DET-like eval для Actor-Learner (аналог DET_EVAL в основном loop).
                if (
                    ACTOR_DET_EVAL_ENABLED
                    and episodes_finished > 0
                    and (episodes_finished % ACTOR_DET_EVAL_EVERY_EPISODES == 0 or episodes_finished == int(totLifeT))
                    and episodes_finished != last_actor_det_eval_ep
                ):
                    try:
                        det_payload = _train_window_payload_from_rows(
                            ep_rows,
                            episode_idx=int(episodes_finished),
                            algo="dqn",
                            training_loss=float(last_loss) if last_loss is not None else None,
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
                                    metrics_mode="train_window",
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
                        if (
                            DQN_DISTRIBUTED_ACTORS
                            and int(episodes_finished) >= int(totLifeT)
                            and not dist_stop_sent
                        ):
                            dist_stop_sent = True
                            dist_drain_until = time.monotonic() + float(DQN_DIST_DRAIN_SEC)
                            touch_dqn_dist_stop_flag()
                            _ln = (
                                f"[TRAIN][DIST] stop_requested ep_done={int(episodes_finished)}/{int(totLifeT)} "
                                f"drain_budget={int(round(float(DQN_DIST_DRAIN_SEC)))}s"
                            )
                            append_agent_log(_ln)
                            print(_ln, flush=True)
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
            _emit_dqn_perf_metrics()
            continue
        if kind != "batch":
            _emit_dqn_perf_metrics()
            continue

        # Локальный actor шлёт голый список; remote (ПК2) — dict {"steps":..,"priority":..}.
        if isinstance(payload, dict):
            batch_steps = payload.get("steps", []) or []
            # MVP: priority принимается, но не применяется (learner-side max_priority).
            # Точка расширения под actor-side Ape-X (DQN_DIST_ACTOR_PRIORITY).
            _remote_priority = payload.get("priority", None)  # noqa: F841
        else:
            batch_steps = payload

        push_started = time.perf_counter()
        pushed_steps = _push_dqn_batch_steps_to_memory(memory, batch_steps)
        push_batch_ms = (time.perf_counter() - push_started) * 1000.0
        global_step += pushed_steps
        perf_push_ms_total += float(push_batch_ms)
        perf_batches += 1
        perf_transitions += int(pushed_steps)

        for _ in range(updates_per_batch):
            per_beta = PER_BETA_START
            if PER_ENABLED and PER_BETA_FRAMES > 0:
                per_beta = min(
                    1.0,
                    PER_BETA_START + (1.0 - PER_BETA_START) * (optimize_steps / float(PER_BETA_FRAMES)),
                )
            opt_started = time.perf_counter()
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
            perf_opt_ms_total += (time.perf_counter() - opt_started) * 1000.0
            perf_opt_calls += 1
            if result and result.get("loss") is not None:
                last_loss = float(result["loss"])
                optimize_steps += 1
                perf_updates += 1
                loss_trace.append(float(last_loss))
                if lr_scheduler is not None:
                    if DQN_LR_SCHEDULER == "plateau":
                        lr_scheduler.step(float(last_loss))
                    else:
                        lr_scheduler.step()
                # TensorBoard: тренировочный лосс DQN actor-learner (no-op, если TB выключен).
                try:
                    from core.telemetry.tb_logger import get_tb_logger

                    _tb = get_tb_logger(str(randNum), algo="dqn")
                    if _tb.active:
                        _tb.log_train(
                            {
                                "loss": float(last_loss),
                                "td_target_mean": float(result.get("td_target_mean", 0.0) or 0.0),
                                "lr": float(optimizer.param_groups[0]["lr"]),
                            },
                            step=int(optimize_steps),
                        )
                except Exception:
                    pass

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

        _emit_dqn_perf_metrics()

    _emit_dqn_perf_metrics(force=True)

    if DQN_DISTRIBUTED_ACTORS:
        try:
            if not dist_stop_sent:
                stop_path = touch_dqn_dist_stop_flag()
                append_agent_log(f"[DQN][DIST] stop.flag записан: {stop_path}")
        except Exception as exc:
            append_agent_log(f"[DQN][DIST][WARN] не удалось записать stop.flag: {exc}")
        for _ln in ("[TRAIN][PHASE] done",):
            append_agent_log(_ln)
            print(_ln, flush=True)
        if rollout_receiver is not None:
            try:
                rollout_receiver.stop()
            except Exception:
                pass

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
                "episode": int(resume_episode_base + len(ep_rows)),
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
                metrics_mode="train_window",
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
                metrics_mode="train_window",
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
        final_agent_id = build_agent_id(learner_identity, f"final_ep{resume_episode_base + len(ep_rows)}")
        artifact_dir = save_agent_artifact(
            identity=learner_identity,
            agent_id=final_agent_id,
            env_contract=env_contract,
            policy_state_dict=normalize_state_dict(policy_net.state_dict()),
            target_state_dict=normalize_state_dict(target_net.state_dict()),
            optimizer_state_dict=optimizer.state_dict(),
            extra_meta={
                "algo": "dqn",
                "episode": int(resume_episode_base + len(ep_rows)),
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

    # Быстрый sanity-check качества по окну тренировки (DET-прогоны удалены;
    # честное сравнение моделей — отдельный eval.py).
    if ep_rows:
        try:
            payload = _train_window_payload_from_rows(
                ep_rows,
                episode_idx=int(max(episodes_finished, 1)),
                algo="dqn",
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
                print(f"[ACTOR_LEARNER][EVAL][WARN] сводка пропущена: {exc}")

    for p in procs:
        try:
            p.join(timeout=1.0)
            # Зависший актор (например, заблокирован на put() в переполненную очередь
            # во время remote-флуда) иначе подвесит выход родителя на atexit-join. Убиваем.
            if p.is_alive():
                p.terminate()
                p.join(timeout=2.0)
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

    ordered_keys = ordered_action_keys(len(model0))
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
    # Resume до сборки init_weights, чтобы акторы стартовали с обученных весов, а не случайных.
    ppo_resume_meta = _resume_ppo_checkpoint(actor_critic, optimizer, ppo_lr_scheduler)
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
                    if checkpoint_meta_algo not in ("dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero", "sampled_muzero"):
                        if "actor_critic" in checkpoint:
                            checkpoint_meta_algo = "ppo"
                        elif "sampled_muzero_net" in checkpoint:
                            checkpoint_meta_algo = "sampled_muzero"
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
                        metadata=dict(checkpoint) if isinstance(checkpoint, dict) else {},
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
        "sampled_muzero",
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
    episode_base = int(ppo_resume_meta["episode_base"])
    global_step = int(ppo_resume_meta["global_step"])
    ppo_update_step = int(ppo_resume_meta["update_step"])
    last_checkpoint = ""
    last_actor_det_eval_ep = 0

    run_id = str(random.randint(1000000, 9999999))
    model_name = datetime.datetime.now().strftime("%d-%H%M%S")
    metrics_obj = metrics(MODELS_DIR, run_id, model_name)
    ep_rows: list[dict] = []
    train_t0_summary = time.perf_counter()
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
                print(f"ep={episodes_finished}/{totLifeT}", flush=True)
                metrics_obj.updateRew(float(payload.get("ep_reward", 0.0) or 0.0))
                metrics_obj.updateEpLen(int(payload.get("ep_len", 0) or 0))
                ep_row = {k: payload.get(k) for k in (
                    "episode", "ep_reward", "ep_len", "turn", "model_vp", "player_vp",
                    "vp_diff", "result", "end_reason", "end_code",
                )}
                append_episode_diagnostics(
                    run_id=run_id,
                    episode_row=ep_row,
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
                log_train_episode_line(
                    ep_row,
                    ep=int(episodes_finished),
                    total=int(totLifeT),
                    algo="ppo",
                    actor_idx=int(payload.get("actor_idx", -1) or -1),
                )
                # Per-episode стратагемная сводка (PPO)
                if _trace_ep_enabled(int(episodes_finished)):
                    from core.telemetry.stratagem_trace import episode_stratagem_summary_line
                    _strat_line = episode_stratagem_summary_line(payload, ep_label=int(episodes_finished), tag="TRAIN")
                    if _strat_line:
                        append_agent_log(_strat_line)

                # Periodic DET-like eval для PPO Actor-Learner (как в DQN actor-learner).
                if (
                    ACTOR_DET_EVAL_ENABLED
                    and episodes_finished > 0
                    and (episodes_finished % ACTOR_DET_EVAL_EVERY_EPISODES == 0 or episodes_finished == int(totLifeT))
                    and episodes_finished != last_actor_det_eval_ep
                ):
                    try:
                        det_payload = _train_window_payload_from_rows(
                            ep_rows,
                            episode_idx=int(episodes_finished),
                            algo="ppo",
                            training_loss=float(
                                last_update_metrics.get("policy_loss", 0.0)
                                + PPO_VALUE_COEF * last_update_metrics.get("value_loss", 0.0)
                            ),
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
                                    metrics_mode="train_window",
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
                                "arch": _ppo_arch_dict(actor_critic),
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
                        episode=episode_base + episodes_finished,
                        n_actions=n_actions,
                        n_observations=n_observations,
                        model=None,
                        enemy=None,
                        env_contract=env_contract,
                        roster_config=roster_config,
                        b_len=b_len,
                        b_hei=b_hei,
                        lr_scheduler=ppo_lr_scheduler,
                        global_step=global_step,
                        update_step=ppo_update_step,
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
            episode=int(episode_base + (episodes_finished or totLifeT)),
            n_actions=n_actions,
            n_observations=n_observations,
            model=None,
            enemy=None,
            env_contract=env_contract,
            roster_config=roster_config,
            b_len=b_len,
            b_hei=b_hei,
            lr_scheduler=ppo_lr_scheduler,
            global_step=global_step,
            update_step=ppo_update_step,
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
                    metrics_mode="train_window",
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
                    metrics_mode="train_window",
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
    _log_train_summary(ep_rows, time.perf_counter() - train_t0_summary)
    append_agent_log(f"[PPO][ACTOR_LEARNER] done: episodes={totLifeT} steps={global_step} updates={ppo_update_step} checkpoint={last_checkpoint}")

    # Финальный снапшот в registry (чтобы GUI мог выбрать PPO как оппонента).
    # Важно: сохраняем даже при SELF_PLAY_ENABLED=0 (PPO vs эвристика), иначе агент не появляется в GUI.
    try:
        final_cumulative_episode = episode_base + int(episodes_finished or len(ep_rows))
        final_agent_id = build_agent_id(learner_identity, f"final_ep{final_cumulative_episode}")
        artifact_dir = save_agent_artifact(
            identity=learner_identity,
            agent_id=final_agent_id,
            env_contract=env_contract,
            policy_state_dict=normalize_state_dict(actor_critic.state_dict()),
            target_state_dict=None,
            optimizer_state_dict=optimizer.state_dict(),
            extra_meta={
                "algo": "ppo",
                "arch": _ppo_arch_dict(actor_critic),
                "episode": int(final_cumulative_episode),
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

        if DQN_REACTION_VALUE_POLICY:
            try:
                from core.models.dqn_stratagem_bridge import install_dqn_stratagem_policy

                install_dqn_stratagem_policy(env, {"model": cpu_net}, torch.device("cpu"))
                append_agent_log(f"[DQN][ACTOR] actor={int(actor_idx)} reaction_value_policy=ON")
            except Exception as exc:
                append_agent_log(
                    f"[DQN][ACTOR][WARN] actor={int(actor_idx)} reaction_value_policy install failed: {exc}"
                )

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

        dist_stop = os.getenv("DQN_DISTRIBUTED_ACTORS", "0").strip().lower() in {"1", "true", "yes"}
        for _ep in range(int(episodes)):
            if dist_stop and dqn_dist_stop_requested():
                append_agent_log(f"[DQN][ACTOR] actor={int(actor_idx)} stop.flag — выход")
                break
            ep_idx_1based = int(_ep) + 1
            trace_lines: list[str] = []
            round_timeline: list[dict] = []
            step_idx = 0
            action_head_total = Counter({"move": 0, "attack": 0, "shoot": 0, "charge": 0})
            action_head_skip = Counter({"move": 0, "attack": 0, "shoot": 0, "charge": 0})
            action_head_invalid = Counter({"move": 0, "attack": 0, "shoot": 0, "charge": 0})
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
            # ВАЖНО: повторяем init как в actor-learner env setup:
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

            from core.envs.warhamEnv import resolve_first_turn_side

            env_u_for_ft = unwrap_env(env)
            env_u_for_ft.first_turn_side = resolve_first_turn_side(manual_roll_allowed=False, log_fn=None)
            append_agent_log(
                f"[DQN][ACTOR][FIRST_TURN] mode={os.getenv('FIRST_TURN', 'roll')} first={env_u_for_ft.first_turn_side}"
            )

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
                decay_steps = max(1.0, float(EPS_DECAY))
                progress = min(float(steps_done) / decay_steps, 1.0)
                eps_threshold = EPS_START + (EPS_END - EPS_START) * progress
                action_t = select_action_with_epsilon(
                    env, obs, cpu_net, eps_threshold, len(model)
                )
                action_dict = action_tensor_to_dict(action_t, len_model=len(model))

                # --- episode action analytics (cheap) ---
                try:
                    for _h in ("move", "attack", "shoot", "charge"):
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

                    valid_shoot_indices = []
                    try:
                        legal_for_analytics = unwrap_env(env).get_legal_action_masks_by_head(side="model")
                        for key in ordered_action_keys(len(model)):
                            if key.startswith("shoot_num_"):
                                mask_arr = np.asarray(legal_for_analytics.get(key, []), dtype=np.bool_)
                                if bool(mask_arr.any()):
                                    valid_shoot_indices.append(key)
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
                            f"shoot_targets={len(valid_shoot_indices)}"
                        )
                except Exception:
                    pass

                # --- run_battle_round: порядок половин из env.turn_order (first-turn roll-off) ---
                env_unwrapped = unwrap_env(env)
                from core.engine.turn_sequencing import run_battle_round

                def _enemy_half() -> None:
                    if opponent_policy_fn is not None:
                        env_unwrapped.enemyTurn(trunc=trunc, policy_fn=opponent_policy_fn)
                    else:
                        env_unwrapped.enemyTurn(trunc=trunc)

                def _model_half() -> None:
                    nonlocal next_obs, reward, done, res, info2, last_info, last_res, ep_reward, ep_len, obs, steps_done, buf
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

                    r_clipped, _ = maybe_clip_reward(
                        float(reward),
                        bool(clip_reward_enabled),
                        float(clip_reward_min),
                        float(clip_reward_max),
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

                # Переменные, которые _model_half может установить при game_over short-circuit
                next_obs = obs
                reward = 0.0
                res = 0
                info2 = {}
                run_battle_round(env_unwrapped, run_model_half=_model_half, run_enemy_half=_enemy_half)

                # Если game_over после enemy_half (модель не ходила) — корректно завершаем эпизод
                if bool(getattr(env_unwrapped, "game_over", False)) and not done:
                    done = True
                    if hasattr(env_unwrapped, "get_info"):
                        last_info = env_unwrapped.get_info() or last_info

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

                # Стратагемная сводка per-episode для learner-лога
                from core.telemetry.stratagem_trace import collect_ep_stratagem_payload
                _dqn_strat_payload = collect_ep_stratagem_payload(env_unwrapped)

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
                                "skip": {k: int(action_head_skip.get(k, 0)) for k in ("move","attack","shoot","charge")},
                                "invalid": {k: int(action_head_invalid.get(k, 0)) for k in ("move","attack","shoot","charge")},
                                "skip_rate": {k: float(action_head_skip.get(k, 0)) / float(max(1, int(ep_len))) for k in ("move","attack","shoot","charge")},
                                "invalid_rate": {k: float(action_head_invalid.get(k, 0)) / float(max(1, int(ep_len))) for k in ("move","attack","shoot","charge")},
                                "shoot_windows": {"with_targets": int(shoot_windows_with_targets), "without_targets": int(shoot_windows_without_targets)},
                                "shoot_taken_when_targets": int(shoot_taken_when_targets),
                                "move": {"stay": int(move_stay), "nonstay": int(move_nonstay)},
                            },
                            **_dqn_strat_payload,
                        },
                    )
                )
            except Exception:
                pass

            if DQN_DISTRIBUTED_ACTORS:
                # Своевременный маркер сбора ПК1 для GUI (аналог pc2_ep_accepted):
                # learner-TRACE отстаёт на размер очереди обучения, прогресс сбора — отсюда.
                try:
                    print(f"[TRAIN][DIST][PC1] pc1_ep_collected actor={int(actor_idx)}", flush=True)
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

        if PPO_REACTION_VALUE_POLICY:
            try:
                from core.models.ppo_stratagem_bridge import install_ppo_stratagem_policy

                install_ppo_stratagem_policy(env, torch.device("cpu"), {"model": cpu_net})
                append_agent_log(f"[PPO][ACTOR] actor={int(actor_idx)} reaction_value_policy=ON")
            except Exception as exc:
                append_agent_log(
                    f"[PPO][ACTOR][WARN] actor={int(actor_idx)} reaction_value_policy install failed: {exc}"
                )

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
        ordered_keys = ordered_action_keys(len(model))

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

            from core.envs.warhamEnv import resolve_first_turn_side

            env_u_for_ft = unwrap_env(env)
            env_u_for_ft.first_turn_side = resolve_first_turn_side(manual_roll_allowed=False, log_fn=None)
            append_agent_log(
                f"[PPO][ACTOR][FIRST_TURN] mode={os.getenv('FIRST_TURN', 'roll')} first={env_u_for_ft.first_turn_side}"
            )

            obs, info0 = env.reset(options={"m": model, "e": enemy, "Type": "small", "trunc": trunc})
            done = False
            ep_reward = 0.0
            ep_len = 0
            last_info = info0 if isinstance(info0, dict) else {}
            last_res = 0

            while not done:
                env_unwrapped = unwrap_env(env)
                from core.engine.turn_sequencing import run_battle_round

                def _enemy_half() -> None:
                    if opponent_policy_fn is not None:
                        env_unwrapped.enemyTurn(trunc=trunc, policy_fn=opponent_policy_fn)
                    elif int(SELF_PLAY_ENABLED) == 1 and opponent_loaded:
                        # PPO-vs-PPO fallback (sync-file), deterministic
                        def _ppo_opp_policy_fn(obs_opp, env=env, net=opponent_net, lm=len(model), n_actions=n_actions):
                            obs_np_local = to_np_state(obs_opp)
                            obs_t_local = torch.tensor(obs_np_local, dtype=torch.float32, device=torch.device("cpu")).unsqueeze(0)
                            masks_cpu_local = build_action_masks_by_head(
                                env, int(lm), log_fn=None, debug=False, side="enemy"
                            )
                            masks_batch_local = [
                                m.to(torch.device("cpu")).unsqueeze(0) for m in masks_cpu_local
                            ]
                            with torch.no_grad():
                                act_t, _logp_t, _val_t = net.act(obs_t_local, masks_by_head=masks_batch_local, deterministic=True)
                            act_np = act_t.squeeze(0).detach().cpu().numpy()
                            return action_tensor_to_dict(torch.tensor([act_np], device="cpu"), len_model=int(lm))

                        env_unwrapped.enemyTurn(trunc=trunc, policy_fn=_ppo_opp_policy_fn)
                    else:
                        env_unwrapped.enemyTurn(trunc=trunc)

                def _model_half() -> None:
                    nonlocal done, last_info, last_res, ep_reward, ep_len, obs, steps_buf

                    obs_np = to_np_state(obs)
                    obs_t = torch.tensor(obs_np, dtype=torch.float32, device=torch.device("cpu")).unsqueeze(0)

                    masks_cpu = build_action_masks_by_head(
                        env, len(model), log_fn=None, debug=False, side="model"
                    )
                    masks_batch = [m.to(torch.device("cpu")).unsqueeze(0) for m in masks_cpu]

                    with torch.no_grad():
                        action_t, logprob_t, value_t = cpu_net.act(obs_t, masks_by_head=masks_batch, deterministic=False)
                    action_np = action_t.squeeze(0).detach().cpu().numpy()

                    action_dict = action_tensor_to_dict(torch.tensor([action_np], device="cpu"), len_model=len(model))

                    next_obs, reward, _done, res, info2 = env.step(action_dict)
                    done = _done
                    last_info = info2 if isinstance(info2, dict) else last_info
                    last_res = res

                    r_clipped, _ = maybe_clip_reward(
                        float(reward),
                        bool(clip_reward_enabled),
                        float(clip_reward_min),
                        float(clip_reward_max),
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

                run_battle_round(env_unwrapped, run_model_half=_model_half, run_enemy_half=_enemy_half)

                # Если game_over после enemy_half (модель не ходила) — корректно завершаем эпизод
                if bool(getattr(env_unwrapped, "game_over", False)) and not done:
                    done = True
                    if hasattr(env_unwrapped, "get_info"):
                        last_info = env_unwrapped.get_info() or last_info

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

                # Стратагемная сводка per-episode для learner-лога
                from core.telemetry.stratagem_trace import collect_ep_stratagem_payload
                _ppo_strat_payload = collect_ep_stratagem_payload(env_unwrapped)

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
                            **_ppo_strat_payload,
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
        mcts = _build_az_search(az_net, mcts_cfg_payload, cpu_device)
        sp_cfg = SelfPlayConfig(
            temperature_opening_moves=int(sp_cfg_payload.get("temperature_opening_moves", AZ_TEMP_OPENING_MOVES)),
            temperature_opening_value=float(sp_cfg_payload.get("temperature_opening_value", AZ_TEMP_OPENING)),
            temperature_late_value=float(sp_cfg_payload.get("temperature_late_value", AZ_TEMP_LATE)),
        )

        enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
        mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
        env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
        len_model = int(len(model))

        # B3-full: установка reaction_value_policy (net-value lookahead реакций) — прямой az_net.
        if str(os.getenv("AZ_REACTION_VALUE_POLICY", "1")).strip().lower() in ("1", "true", "yes", "on"):
            try:
                from core.models.reaction_value_policy import make_reaction_value_policy

                _eu = env.unwrapped
                _eu._reaction_net_by_side = {"model": az_net, "enemy": az_net}
                _eu.reaction_policy = make_reaction_value_policy(_eu._reaction_net_by_side, device=cpu_device)
                print(f"[{_AZ_LOG_TAG}][ACTOR] actor={int(actor_idx)} reaction_value_policy=ON", flush=True)
            except Exception as exc:
                print(
                    f"[{_AZ_LOG_TAG}][ACTOR][WARN] actor={int(actor_idx)} reaction_value_policy install failed: {exc}",
                    flush=True,
                )

        sync_enabled = os.getenv("ACTOR_SYNC_ENABLED", "1") == "1"
        # Путь sync должен совпадать с тем, что пишет learner (_save_az_sync, train.py ~8377):
        # learner использует тег tree/proxy по TRAIN_ALGO. Раньше актор читал untagged
        # "latest_az_policy.pth" → файл не находился, ACTOR_SYNC молча no-op (веса не обновлялись).
        if TRAIN_ALGO == "alphazero_tree":
            _az_sync_tag = "tree"
        elif is_gumbel_az_algo(TRAIN_ALGO):
            _az_sync_tag = "gumbel_az"
        else:
            _az_sync_tag = "proxy"
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
                f"[{_AZ_LOG_TAG}][ACTOR] actor={int(actor_idx)} local_ep={ep_idx_1based}/{ep_total_label} starting "
                f"mcts_mode={getattr(mcts.cfg, 'mode', 'proxy')} "
                f"sims={getattr(mcts.cfg, 'simulations', None) or getattr(mcts.cfg, 'num_simulations', 0)}",
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
                mission_bootstrap_coef=float(
                    outcome_payload.get("mission_bootstrap_coef", AZ_MISSION_BOOTSTRAP_COEF)
                ),
                reward_shaping_weight=float(
                    outcome_payload.get("reward_shaping_weight", AZ_REWARD_SHAPING_WEIGHT)
                ),
                policy_version=int(current_policy_version),
                actor_idx=int(actor_idx),
                heartbeat_moves=heartbeat_moves,
            )
            for t in transitions:
                rollout_batch.append(
                    az_transition_to_rollout_dict(
                        t,
                        policy_version=int(getattr(t, "policy_version", current_policy_version)),
                    )
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
            ep_payload = {
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
            }
            ep_payload.update(_az_episode_mission_fields(info))
            sink.put("ep", ep_payload)

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
                f"[{_AZ_LOG_TAG}][REMOTE_CLIENT][CONN] worker={int(worker_id)} "
                f"tcp://{remote_host}:{int(remote_port)}"
            )

        mcts = _build_az_search(None, mcts_cfg_payload, torch.device("cpu"), evaluator=evaluator)
        sp_cfg = SelfPlayConfig(
            temperature_opening_moves=int(sp_cfg_payload.get("temperature_opening_moves", AZ_TEMP_OPENING_MOVES)),
            temperature_opening_value=float(sp_cfg_payload.get("temperature_opening_value", AZ_TEMP_OPENING)),
            temperature_late_value=float(sp_cfg_payload.get("temperature_late_value", AZ_TEMP_LATE)),
        )

        enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
        mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
        env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
        len_model = int(len(model))

        # B3-full: установка reaction_value_policy (net-value lookahead реакций) через evaluator-адаптер.
        if str(os.getenv("AZ_REACTION_VALUE_POLICY", "1")).strip().lower() in ("1", "true", "yes", "on"):
            try:
                import numpy as _np

                from core.models.reaction_value_policy import make_reaction_value_policy

                _react_sizes = action_sizes_from_env(env, len_model)

                class _ReactionEvalNet:
                    """Адаптер evaluator.evaluate_one → net.infer-совместимый value (для harness)."""

                    def __init__(self, _ev, _sizes):
                        self._ev = _ev
                        self._masks = [_np.ones(int(a), dtype=bool) for a in _sizes]

                    def infer(self, obs_tensor, masks_by_head=None):
                        obs = _np.asarray(obs_tensor.detach().cpu().numpy()[0], dtype=_np.float32)
                        _, value = self._ev.evaluate_one(obs, self._masks)
                        return None, torch.tensor([float(value)])

                _react_net = _ReactionEvalNet(evaluator, _react_sizes)
                _eu = env.unwrapped
                _eu._reaction_net_by_side = {"model": _react_net, "enemy": _react_net}
                _eu.reaction_policy = make_reaction_value_policy(
                    _eu._reaction_net_by_side, device=torch.device("cpu")
                )
                print(
                    f"[{_AZ_LOG_TAG}][ENV_WORKER] worker={int(worker_id)} reaction_value_policy=ON",
                    flush=True,
                )
            except Exception as exc:
                print(
                    f"[{_AZ_LOG_TAG}][ENV_WORKER][WARN] worker={int(worker_id)} "
                    f"reaction_value_policy install failed: {exc}",
                    flush=True,
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

        current_policy_version = int(outcome_payload.get("policy_version", 0) or 0)
        rollout_batch: list[dict] = []
        heartbeat_moves = max(1, int(os.getenv("AZ_ACTOR_HEARTBEAT_MOVES", "5") or 5))

        ep_limit = int(episodes)
        ep_total_label = str(ep_limit) if ep_limit > 0 else "open"
        append_agent_log(
            f"[{_AZ_LOG_TAG}][ENV_WORKER] worker={int(worker_id)} started episodes={ep_total_label} "
            f"rollout_sink={rollout_sink_mode}"
        )
        ep_iter = range(ep_limit) if ep_limit > 0 else itertools.count()
        for _ep in ep_iter:
            if dist_stop_flag_path and az_dist_stop_requested(dist_stop_flag_path):
                append_agent_log(f"[{_AZ_LOG_TAG}][ENV_WORKER] worker={int(worker_id)} stop.flag — выход")
                break
            ep_idx_1based = int(_ep) + 1
            print(
                f"[{_AZ_LOG_TAG}][ENV_WORKER] worker={int(worker_id)} local_ep={ep_idx_1based}/{ep_total_label} starting",
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
                mission_bootstrap_coef=float(
                    outcome_payload.get("mission_bootstrap_coef", AZ_MISSION_BOOTSTRAP_COEF)
                ),
                reward_shaping_weight=float(
                    outcome_payload.get("reward_shaping_weight", AZ_REWARD_SHAPING_WEIGHT)
                ),
                policy_version=int(current_policy_version),
                actor_idx=int(worker_id),
                heartbeat_moves=heartbeat_moves,
            )

            # Подхватываем policy_version из последнего ответа IS (через evaluator)
            if hasattr(evaluator, "_last_policy_version"):
                current_policy_version = int(evaluator._last_policy_version)

            for t in transitions:
                rollout_batch.append(
                    az_transition_to_rollout_dict(
                        t,
                        policy_version=int(getattr(t, "policy_version", current_policy_version)),
                    )
                )
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
            ep_payload = {
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
            }
            ep_payload.update(_az_episode_mission_fields(info))
            sink.put("ep", ep_payload)
            if str(rollout_sink_mode or "local").strip().lower() == "local":
                # Своевременный маркер сбора ПК1 для GUI (аналог pc2_ep_accepted у приёмника).
                try:
                    print(
                        f"[TRAIN][DIST][PC1] pc1_ep_collected actor={int(worker_id)}",
                        flush=True,
                    )
                except Exception:
                    pass

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
        extras={
            "actor_learner": 1,
            "train_algo": TRAIN_ALGO,
            "mcts_mode": AZ_MCTS_MODE,
            "num_actors": int(AZ_NUM_ACTORS),
            # Пишем РЕАЛЬНО использованные значения (резолв GAZ_*→AZ_*→секция), чтобы
            # контракт совпал с обучением. Иначе авто-резолв по env мог разойтись —
            # напр. у GAZ при значении из секции. Eval берёт reaction/phase из контракта.
            "reaction_value_policy": int(bool(AZ_REACTION_VALUE_POLICY)),
            "phase_obs_features": int(bool(AZ_PHASE_OBS_FEATURES)),
        },
    )

    try:
        _gaz_cfg = is_gumbel_az_algo(TRAIN_ALGO)
        _az_search_cfg_paths = write_az_remote_search_cfg(
            obs_dim=int(n_observations),
            action_sizes=[int(x) for x in n_actions],
            hidden_size=int(AZ_HIDDEN_SIZE),
            num_layers=int(AZ_NUM_LAYERS),
            n_value_ensemble=int(AZ_VALUE_ENSEMBLE),
            num_simulations=int(GAZ_NUM_SIMS if _gaz_cfg else AZ_MCTS_SIMS),
            sources=["train.py:auto"],
            filename="gaz_remote_search_cfg.json" if _gaz_cfg else "az_remote_search_cfg.json",
        )
        append_agent_log(
            f"[{_AZ_LOG_TAG}][REMOTE_IS] search_cfg обновлён (obs={int(n_observations)}): {_az_search_cfg_paths}"
        )
    except Exception as exc:
        append_agent_log(
            f"[{_AZ_LOG_TAG}][REMOTE_IS][WARN] не удалось записать search_cfg: {exc}. "
            "Где: write_az_remote_search_cfg. Что делать: откройте Qt GUI на ПК1."
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
        except Exception as exc:
            _raise_resume_error("AZ", RESUME_CHECKPOINT, f"не удалось прочитать файл: {exc}")
        if not isinstance(checkpoint, dict):
            _raise_resume_error("AZ", RESUME_CHECKPOINT, "payload не является словарём")
        policy_state = checkpoint.get("policy_value_net")
        if not isinstance(policy_state, dict):
            policy_state = _extract_policy_state_dict(checkpoint)
        if not isinstance(policy_state, dict):
            _raise_resume_error(
                "AZ",
                RESUME_CHECKPOINT,
                "в чекпойнте нет policy_value_net/policy state_dict (нужен AlphaZero checkpoint)",
            )
        arch = alphazero_arch_from_payload(checkpoint)
        if arch != az_kw:
            append_agent_log(
                f"[AZ][RESUME][WARN] arch mismatch checkpoint={arch} current={az_kw}; strict=False load"
            )
        # B6: явная проверка размера obs (phase_obs_features меняет input-слой) — понятная остановка.
        _ckpt_input_w = policy_state.get("input_fc.weight")
        if hasattr(_ckpt_input_w, "shape") and len(getattr(_ckpt_input_w, "shape", ())) == 2:
            _obs_mismatch = describe_obs_dim_mismatch(
                checkpoint_obs_dim=int(_ckpt_input_w.shape[1]),
                current_obs_dim=int(n_observations),
            )
            if _obs_mismatch:
                _raise_resume_error("AZ", RESUME_CHECKPOINT, _obs_mismatch)
        try:
            load_alphazero_state_dict(
                az_net,
                normalize_state_dict(policy_state),
                log_fn=append_agent_log,
            )
        except Exception as exc:
            _raise_resume_error("AZ", RESUME_CHECKPOINT, f"не удалось загрузить веса policy_value_net: {exc}")
        opt_state = checkpoint.get("optimizer")
        if isinstance(opt_state, dict):
            try:
                optimizer.load_state_dict(opt_state)
            except Exception as exc:
                append_agent_log(
                    f"[AZ][RESUME][WARN] optimizer load failed: {exc}. "
                    "Где: train.py (_main_actor_learner_alphazero). Что делать: продолжить с чистым optimizer."
                )
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
            try:
                replay.load_state_dict(replay_state)
            except Exception as exc:
                append_agent_log(
                    f"[AZ][RESUME][WARN] replay load failed: {exc}. "
                    "Где: train.py (_main_actor_learner_alphazero). Что делать: продолжить с пустым буфером."
                )
        # Семантика totLifeT — «дополнительные игры за этот запуск» (как DQN/PPO):
        # episodes_finished считаем с нуля, а resume_episode_base держит накопительную базу
        # для нумерации чекпоинтов и продолжения общего счётчика игр.
        resume_episode_base = int(checkpoint.get("episode", 0) or 0)
        global_step = int(checkpoint.get("global_step", 0) or 0)
        optimize_steps = int(checkpoint.get("optimize_steps", 0) or 0)
        policy_version = int(checkpoint.get("policy_version", optimize_steps) or optimize_steps)
        append_agent_log(
            "[AZ][RESUME] "
            f"path={RESUME_CHECKPOINT} episode_base={resume_episode_base} replay={len(replay)} "
            f"global_step={global_step} optimize_steps={optimize_steps} policy_version={policy_version} "
            f"(доп. игр за запуск={int(totLifeT)})"
        )

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
        f"[{_AZ_LOG_TAG}][CONFIG] "
        f"num_actors={AZ_NUM_ACTORS} actor_batch_send={AZ_ACTOR_BATCH_SEND} queue_max={AZ_ACTOR_QUEUE_MAX} "
        f"sync_every_updates={AZ_SYNC_EVERY_UPDATES} updates_per_rollout={AZ_UPDATES_PER_ROLLOUT} "
        f"balanced_sampling={int(AZ_BALANCED_OUTCOME_SAMPLING)} "
        f"max_staleness={AZ_MAX_POLICY_STALENESS_UPDATES} replay_min={AZ_REPLAY_MIN_SIZE} "
        f"outcome_only={int(AZ_OUTCOME_ONLY)} mission_bootstrap_coef={AZ_MISSION_BOOTSTRAP_COEF:.3f} "
        f"reward_shaping_weight={AZ_REWARD_SHAPING_WEIGHT:.3f} "
        f"mcts_mode={AZ_MCTS_MODE} candidate_mode={AZ_MCTS_CANDIDATE_MODE} "
        f"windowed_selfplay={int(AZ_WINDOWED_SELFPLAY)} window_nodes={int(AZ_MCTS_WINDOW_NODES)} "
        f"joint_best_child={int(AZ_MCTS_JOINT_BEST_CHILD)} phase_obs_features={int(AZ_PHASE_OBS_FEATURES)} "
        f"reaction_value_policy={int(AZ_REACTION_VALUE_POLICY)} "
        f"mcts={_AZ_LOG_SIMS} "
        f"{f'joint_action={int(GAZ_JOINT_ACTION)} ' if is_gumbel_az_algo(TRAIN_ALGO) else ''}"
        f"top_k={AZ_MCTS_TOP_K_PER_HEAD} depth={_AZ_LOG_DEPTH} "
        f"hidden={az_kw['hidden_size']} layers={az_kw['num_layers']} value_ensemble={az_kw['n_value_ensemble']} "
        f"lr_scheduler={AZ_LR_SCHEDULER} c_puct_schedule={AZ_C_PUCT_SCHEDULE} "
        f"opponent_mode={opponent_source_label} opponent_algo={opponent_algo_label} "
        f"batch_eval={AZ_MCTS_BATCH_EVAL_SIZE} parallel_sims={AZ_MCTS_PARALLEL_SIMS} "
        f"det_eval_n={int(AZ_HONEST_EVAL_EPISODES)} det_eval_temp={float(AZ_HONEST_EVAL_TEMPERATURE):.3f}"
    )

    ep_rows: list[dict] = []
    train_t0_summary = time.perf_counter()
    loss_trace: list[float] = []
    last_checkpoint = ""
    last_actor_det_eval_ep = 0
    last_guard_turn_limit_rate = 0.0

    checkpoint_dir = os.path.join(MODELS_DIR, TRAIN_ALGO)
    os.makedirs(checkpoint_dir, exist_ok=True)
    sync_dir = os.path.join(MODELS_DIR, "actor_sync")
    os.makedirs(sync_dir, exist_ok=True)
    if TRAIN_ALGO == "alphazero_tree":
        _az_sync_tag = "tree"
    elif is_gumbel_az_algo(TRAIN_ALGO):
        _az_sync_tag = "gumbel_az"
    else:
        _az_sync_tag = "proxy"
    sync_path = os.path.join(sync_dir, f"latest_az_{_az_sync_tag}_policy.pth")

    def _save_az_sync() -> None:
        cpu_sd = {k: v.detach().cpu() for k, v in normalize_state_dict(az_net.state_dict()).items()}
        _torch_save_atomic(
            {
                "policy_version": int(policy_version),
                "optimize_steps": int(optimize_steps),
                "state_dict": cpu_sd,
            },
            sync_path,
            label="latest_az_policy",
        )

    def _save_checkpoint(episode_idx: int) -> str:
        ckpt_path = os.path.join(checkpoint_dir, f"checkpoint_ep{int(episode_idx)}.pth")
        payload = {
            "algo": TRAIN_ALGO,
            "mcts_mode": AZ_MCTS_MODE,
            "policy_value_net": az_net.state_dict(),
            "optimizer": optimizer.state_dict(),
            "episode": int(episode_idx),
            "episodes_finished": int(episode_idx),
            "global_step": int(global_step),
            "optimize_steps": int(optimize_steps),
            "policy_version": int(policy_version),
            "replay_memory": replay.state_dict(),
            "env_contract": env_contract,
            "num_actors": int(AZ_NUM_ACTORS),
            "arch": dict(az_kw),
            "outcome_only": bool(AZ_OUTCOME_ONLY),
            "outcome_value_win": float(AZ_OUTCOME_VALUE_WIN),
            "outcome_value_loss": float(AZ_OUTCOME_VALUE_LOSS),
            "outcome_value_draw": float(AZ_OUTCOME_VALUE_DRAW),
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

    if is_gumbel_az_algo(TRAIN_ALGO):
        _mcts_cfg_payload = _gaz_cfg_payload()
    else:
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
            "candidate_mode": AZ_MCTS_CANDIDATE_MODE,
            "window_nodes": AZ_MCTS_WINDOW_NODES,
            "joint_action_from_best_child": AZ_MCTS_JOINT_BEST_CHILD,
            "terminal_value_win": float(AZ_OUTCOME_VALUE_WIN),
            "terminal_value_loss": float(AZ_OUTCOME_VALUE_LOSS),
            "terminal_value_draw": float(AZ_OUTCOME_VALUE_DRAW),
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
        "mission_bootstrap_coef": AZ_MISSION_BOOTSTRAP_COEF,
        "reward_shaping_weight": AZ_REWARD_SHAPING_WEIGHT,
        "policy_version": int(policy_version),
    }
    _init_weights_cpu = {k: v.detach().cpu() for k, v in normalize_state_dict(az_net.state_dict()).items()}
    _az_contract_hash = str(env_contract.get("contract_hash", "") or "")
    _az_dist_stop_flag = str(az_dist_stop_flag_path(TRAIN_ALGO)) if AZ_DISTRIBUTED_ACTORS else ""
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
            ep_marker_fn=lambda n: print(f"[TRAIN][DIST][PC2] pc2_ep_accepted={n}", flush=True),
        )
        # ВНИМАНИЕ: receiver.start() перенесён НИЖЕ — после записи az_dist_train_context.json.
        # Инвариант для ПК2: «порт приёмника открыт ⇒ свежий контекст уже на шаре», иначе ПК2,
        # стартовавший раньше, мог прочитать оппонента прошлого прогона (тихий рассинхрон self-play).
        try:
            _dist_shared_hp = {
                "temperature_opening_moves": int(AZ_TEMP_OPENING_MOVES),
                "temperature_opening_value": float(AZ_TEMP_OPENING),
                "temperature_late_value": float(AZ_TEMP_LATE),
                "outcome_only": int(AZ_OUTCOME_ONLY),
                "outcome_value_win": float(AZ_OUTCOME_VALUE_WIN),
                "outcome_value_loss": float(AZ_OUTCOME_VALUE_LOSS),
                "outcome_value_draw": float(AZ_OUTCOME_VALUE_DRAW),
                "mission_bootstrap_coef": float(AZ_MISSION_BOOTSTRAP_COEF),
                "reward_shaping_weight": float(AZ_REWARD_SHAPING_WEIGHT),
                "actor_batch_send": int(AZ_ACTOR_BATCH_SEND),
                "inference_timeout": float(AZ_INFERENCE_TIMEOUT),
                "self_play_enabled": int(SELF_PLAY_ENABLED),
            }
            if is_gumbel_az_algo(TRAIN_ALGO):
                # GAZ: пакуем поля GumbelAlphaZeroSearch (num_simulations/joint_action/...),
                # чтобы ПК2-акторы строили тот же поиск, что и ПК1 (см. build_gaz_dist_worker_payloads).
                _dist_az_hp = pack_az_dist_hyperparams({**_gaz_cfg_payload(), **_dist_shared_hp})
            else:
                _dist_az_hp = pack_az_dist_hyperparams(
                    {
                        **AZ_CFG,
                        "mcts_simulations": int(AZ_MCTS_SIMS),
                        "mcts_parallel_sims": int(AZ_MCTS_PARALLEL_SIMS),
                        "mcts_max_depth": int(AZ_MCTS_MAX_DEPTH),
                        "mcts_top_k_per_head": int(AZ_MCTS_TOP_K_PER_HEAD),
                        "mcts_candidate_mode": str(AZ_MCTS_CANDIDATE_MODE),
                        "windowed_selfplay": int(AZ_WINDOWED_SELFPLAY),
                        "mcts_window_nodes": int(AZ_MCTS_WINDOW_NODES),
                        "mcts_joint_action_from_best_child": int(AZ_MCTS_JOINT_BEST_CHILD),
                        "phase_obs_features": int(AZ_PHASE_OBS_FEATURES),
                        "reaction_value_policy": int(AZ_REACTION_VALUE_POLICY),
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
                        **_dist_shared_hp,
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
            # Авто-запись search-cfg для IS на ПК2 (форма сети) — чтобы не требовался
            # ручной tools/write_az_remote_search_cfg.bat и не было рассинхрона арх.
            try:
                # GAZ и AZ используют одну сеть → форма search_cfg одна, но имя файла и
                # число sims различаются (GAZ: gaz_remote_search_cfg.json + GAZ_NUM_SIMS).
                _gaz_cfg = is_gumbel_az_algo(TRAIN_ALGO)
                _search_cfg_filename = "gaz_remote_search_cfg.json" if _gaz_cfg else "az_remote_search_cfg.json"
                _search_cfg_paths = write_az_remote_search_cfg(
                    obs_dim=int(n_observations),
                    action_sizes=list(n_actions),
                    hidden_size=int(AZ_HIDDEN_SIZE),
                    num_layers=int(AZ_NUM_LAYERS),
                    n_value_ensemble=int(AZ_VALUE_ENSEMBLE),
                    num_simulations=int(GAZ_NUM_SIMS if _gaz_cfg else AZ_MCTS_SIMS),
                    sources=["train.py:auto", f"env_contract_hash={_az_contract_hash}"],
                    filename=_search_cfg_filename,
                )
                append_agent_log(
                    f"[{_AZ_LOG_TAG}][DIST][CONTEXT] search_cfg обновлён ({_search_cfg_filename} "
                    f"obs={int(n_observations)} hidden={int(AZ_HIDDEN_SIZE)} layers={int(AZ_NUM_LAYERS)} "
                    f"n_value_ensemble={int(AZ_VALUE_ENSEMBLE)}): {_search_cfg_paths}"
                )
            except Exception as exc:
                append_agent_log(
                    f"[{_AZ_LOG_TAG}][DIST][CONTEXT][WARN] не удалось записать search_cfg: {exc}. "
                    "Где: write_az_remote_search_cfg. Что делать: проверьте SMB actor_sync "
                    "или запустите tools/write_az_remote_search_cfg.bat вручную."
                )
            append_agent_log(
                f"[{_AZ_LOG_TAG}][DIST][CONTEXT] wrote opponent_agent_id="
                f"{opponent_agent_id or OPPONENT_AGENT_ID or '-'} "
                f"sims={_dist_az_hp.get('num_simulations', _dist_az_hp.get('mcts_simulations', '?'))} "
                f"path={_dist_ctx_path}"
            )
        except Exception as exc:
            append_agent_log(
                f"[AZ][DIST][CONTEXT][WARN] Не удалось записать контекст для PC2: {exc}. "
                "Где: write_az_dist_train_context. Что делать: проверьте SMB actor_sync."
            )
        # Контекст и search_cfg записаны → ТОЛЬКО ТЕПЕРЬ открываем приёмник. Порядок
        # context→receiver даёт ПК2 инвариант: порт :AZ_DIST_ROLLOUT_PORT отвечает ⇒ свежий
        # az_dist_train_context.json уже на шаре (нет гонки со stale-оппонентом прошлого прогона).
        rollout_receiver.start()
        append_agent_log(
            f"[{_AZ_LOG_TAG}][DIST][RECEIVER] start (после записи контекста: порядок context→receiver)"
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
                        f"[{_AZ_LOG_TAG}][REMOTE_CLIENT] health_check ok host={AZ_INFERENCE_REMOTE_HOST} "
                        f"port={AZ_INFERENCE_REMOTE_PORT} policy_version={hc.get('policy_version', '?')} "
                        f"gpu={hc.get('gpu_name', '?')}"
                    )
                except Exception as exc:
                    append_agent_log(
                        f"[{_AZ_LOG_TAG}][REMOTE_CLIENT] health_check failed host={AZ_INFERENCE_REMOTE_HOST}: {exc}"
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
                    f"[{_AZ_LOG_TAG}][INF_SERVER] process spawned pid={inf_proc.pid} "
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
                        _az_dist_stop_flag,
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
                        _az_dist_stop_flag,
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
    dist_stop_sent = False
    dist_drain_until = 0.0
    dist_remote_transitions_total = 0
    dist_remote_stale_total = 0

    def _az_dist_remote_alive() -> int:
        if rollout_receiver is None:
            return 0
        return int(rollout_receiver.active_remote_workers())

    def _az_dist_should_finish_drain() -> tuple[bool, str]:
        if not dist_draining:
            return False, ""
        remote_alive = _az_dist_remote_alive()
        if remote_alive == 0 and done_actors >= active_actors:
            return True, "all_workers_idle"
        if time.monotonic() >= dist_drain_until:
            return True, "drain_budget_elapsed"
        return False, "drain_waiting"

    def _az_dist_log_drain_done(reason: str) -> None:
        _ln = (
            f"[TRAIN][DIST] drain_done reason={reason} "
            f"ep_done={int(episodes_finished)}/{int(totLifeT)} "
            f"local_done={done_actors}/{active_actors} remote_alive={_az_dist_remote_alive()}"
        )
        append_agent_log(_ln)
        print(_ln, flush=True)

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
                if not dist_stop_sent:
                    dist_stop_sent = True
                    dist_drain_until = time.monotonic() + float(AZ_DIST_DRAIN_SEC)
                    _touch_az_dist_stop_flag()
                    _ln = (
                        f"[TRAIN][DIST] stop_requested ep_done={int(episodes_finished)}/{int(totLifeT)} "
                        f"drain_budget={int(round(float(AZ_DIST_DRAIN_SEC)))}s"
                    )
                    append_agent_log(_ln)
                    print(_ln, flush=True)
                if not dist_draining:
                    _remote_alive = _az_dist_remote_alive()
                    _drain_left = max(0, int(round(dist_drain_until - time.monotonic())))
                    dist_draining = True
                    for _ln in (
                        "[TRAIN][PHASE] draining",
                        f"[TRAIN][DIST] remote_alive={_remote_alive} "
                        f"ep_done={int(episodes_finished)}/{int(totLifeT)} drain_left={_drain_left}s",
                    ):
                        append_agent_log(_ln)
                        print(_ln, flush=True)
                _finish_drain, _drain_reason = _az_dist_should_finish_drain()
                if _finish_drain:
                    _az_dist_log_drain_done(_drain_reason)
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
                    f"[{_AZ_LOG_TAG}][WAIT] elapsed={elapsed}s replay={len(replay)} "
                    f"actors_alive={alive}/{active_actors} mode={AZ_MCTS_MODE} "
                    f"sims={_AZ_LOG_SIMS} depth={_AZ_LOG_DEPTH} "
                    f"(первый ep может занять несколько минут; прогресс считается по завершённым ep)"
                )
                print(wait_line, flush=True)
                append_agent_log(wait_line)
                if dist_draining:
                    _remote_alive = _az_dist_remote_alive()
                    _drain_left = max(0, int(round(dist_drain_until - time.monotonic())))
                    dist_line = (
                        f"[TRAIN][DIST] remote_alive={_remote_alive} "
                        f"ep_done={int(episodes_finished)}/{int(totLifeT)} drain_left={_drain_left}s"
                    )
                    print(dist_line, flush=True)
                    append_agent_log(dist_line)
                    _finish_drain, _drain_reason = _az_dist_should_finish_drain()
                    if _finish_drain:
                        _az_dist_log_drain_done(_drain_reason)
                        break
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
            # TensorBoard: метрики эпизода + телеметрия (no-op, если TB выключен).
            try:
                from core.telemetry.tb_logger import get_tb_logger

                _tb = get_tb_logger(str(run_id), algo="alphazero")
                if _tb.active:
                    _tb.log_episode(payload, step=int(episodes_finished))
                    _tb.log_telemetry(step=int(episodes_finished))
            except Exception:
                pass
            target_n = min(int(totLifeT), int(episodes_finished))
            if target_n > int(pbar.n):
                pbar.update(target_n - int(pbar.n))
            # Всегда в stdout: GUI парсит ep= для прогресс-бара.
            print(f"ep={episodes_finished}/{totLifeT}", flush=True)

            log_train_episode_line(
                payload,
                ep=int(episodes_finished),
                total=int(totLifeT),
                algo="gumbel_az" if is_gumbel_az_algo(TRAIN_ALGO) else "az",
                actor_idx=int(payload.get("actor_idx", -1) or -1),
            )

            if (
                ACTOR_DET_EVAL_ENABLED
                and episodes_finished > last_actor_det_eval_ep
                and (episodes_finished % ACTOR_DET_EVAL_EVERY_EPISODES == 0 or episodes_finished == int(totLifeT))
            ):
                last_actor_det_eval_ep = int(episodes_finished)
                # Гасим ПК2 по достижении cap: лишние rollout'ы отбрасываются.
                if AZ_DISTRIBUTED_ACTORS and int(episodes_finished) >= int(totLifeT) and not dist_stop_sent:
                    dist_stop_sent = True
                    dist_drain_until = time.monotonic() + float(AZ_DIST_DRAIN_SEC)
                    _touch_az_dist_stop_flag()
                    _ln = (
                        f"[TRAIN][DIST] stop_requested ep_done={int(episodes_finished)}/{int(totLifeT)} "
                        f"drain_budget={int(round(float(AZ_DIST_DRAIN_SEC)))}s"
                    )
                    append_agent_log(_ln)
                    print(_ln, flush=True)
                if int(episodes_finished) >= int(totLifeT):
                    for _ln in ("[TRAIN][PHASE] evaluating",):
                        append_agent_log(_ln)
                        print(_ln, flush=True)
                det_payload = _az_det_payload_from_rows(
                    list(ep_rows)[-int(TRAIN_METRICS_WINDOW_EPISODES):],
                    episode_idx=int(episodes_finished),
                    train_loss=float(last_loss),
                    train_algo=str(TRAIN_ALGO),
                    mcts_mode=str(AZ_MCTS_MODE),
                    eval_tag="train_window",
                )
                _save_actor_det_eval_snapshot(run_id=str(run_id), payload=det_payload, metrics_dir=METRICS_DIR)
                gate_pass = _az_det_eval_gate_pass(det_payload)

                try:
                    det_gui = save_actor_det_eval_plot(run_id=str(run_id), metrics_dir=METRICS_DIR)
                    if det_gui:
                        learner_side = str(learner_identity.side or "P1").strip().upper() or "P1"
                        opponent_side = "P2" if learner_side == "P1" else "P1"
                        _write_det_eval_data_json(
                            run_id=str(run_id),
                            det_plot_gui_paths=det_gui,
                            model_path=str(last_checkpoint or ""),
                            metrics_mode="train_window",
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
                last_checkpoint = _save_checkpoint(resume_episode_base + episodes_finished)
                append_agent_log(f"[AZ][CHECKPOINT] ep={resume_episode_base + episodes_finished} path={last_checkpoint}")

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
            tr = az_transition_from_rollout_dict(
                raw,
                default_policy_version=int(payload.get("policy_version", 0) or 0),
            )
            if tr is None:
                continue
            tr_pv = int(tr.policy_version)
            if rollout_source == "remote":
                dist_remote_transitions_total += 1
                if min_policy_ver >= 0 and tr_pv < min_policy_ver:
                    dist_remote_stale_total += 1
                    continue
            transitions.append(tr)
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
            # TensorBoard: тренировочные лоссы AZ (no-op, если TB выключен).
            try:
                from core.telemetry.tb_logger import get_tb_logger

                _tb = get_tb_logger(str(run_id), algo="alphazero")
                if _tb.active:
                    _tb_metrics = {
                        "loss": float(last_loss),
                        "policy_loss": float(update_info.get("policy_loss", 0.0) or 0.0),
                        "value_loss": float(update_info.get("value_loss", 0.0) or 0.0),
                        "lr": float(optimizer.param_groups[0]["lr"]),
                    }
                    _tb.log_train(_tb_metrics, step=int(optimize_steps))
            except Exception:
                pass
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
            if p.is_alive():
                append_agent_log(
                    f"[{_AZ_LOG_TAG}][ENV_WORKER] процесс pid={p.pid} не завершился за 2с — terminate."
                )
                p.terminate()
                p.join(timeout=1.0)
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
            append_agent_log(f"[{_AZ_LOG_TAG}][INF_SERVER] process не завершился за 3с, terminate.")
            inf_proc.terminate()

    if not last_checkpoint:
        last_checkpoint = _save_checkpoint(int(resume_episode_base + (episodes_finished or totLifeT)))
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
        _log_train_summary(ep_rows, time.perf_counter() - train_t0_summary)
        try:
            det_gui = save_actor_det_eval_plot(run_id=str(run_id), metrics_dir=METRICS_DIR)
            if det_gui:
                learner_side = str(learner_identity.side or "P1").strip().upper() or "P1"
                opponent_side = "P2" if learner_side == "P1" else "P1"
                _write_det_eval_data_json(
                    run_id=str(run_id),
                    det_plot_gui_paths=det_gui,
                    model_path=str(last_checkpoint or ""),
                    metrics_mode="train_window",
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

    final_episode = int(resume_episode_base + episodes_finished)
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
            "arch": dict(az_kw),
            "mcts_mode": AZ_MCTS_MODE,
            "episode": int(final_episode),
            "source_model_path": str(last_checkpoint or ""),
            "mode": "actor_learner",
            "num_actors": int(AZ_NUM_ACTORS),
            "policy_version": int(policy_version),
            "outcome_only": bool(AZ_OUTCOME_ONLY),
            "outcome_value_win": float(AZ_OUTCOME_VALUE_WIN),
            "outcome_value_loss": float(AZ_OUTCOME_VALUE_LOSS),
            "outcome_value_draw": float(AZ_OUTCOME_VALUE_DRAW),
            "mission_bootstrap_coef": float(AZ_MISSION_BOOTSTRAP_COEF),
            "reward_shaping_weight": float(AZ_REWARD_SHAPING_WEIGHT),
        },
    )
    az_done_msg = (
        "[AZ][ACTOR_LEARNER] done "
        f"episodes={final_episode}/{resume_episode_base + int(totLifeT)} checkpoint={last_checkpoint} "
        f"global_step={global_step} updates={optimize_steps} replay={len(replay)}"
    )
    append_agent_log(az_done_msg)
    print(az_done_msg, flush=True)
    if AZ_DISTRIBUTED_ACTORS:
        for _ln in ("[TRAIN][PHASE] done",):
            append_agent_log(_ln)
            print(_ln, flush=True)


def _gmz_rollout_dict_from_transition(t: GMZTransition, policy_version: int) -> dict:
    from core.engine.phases.replay_meta import gmz_transition_to_rollout_dict

    return gmz_transition_to_rollout_dict(t, policy_version=policy_version)


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
    reaction_algo: str = "gmz",
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

        # IS: локальная value-сеть для умных реакций (Подход 1) — реакции считаются ЛОКАЛЬНО на
        # воркере, без сетевых round-trip. GMZ/SMZ — общий воркер, различаем по reaction_algo.
        from core.models.muzero_stratagem_bridge import (
            install_worker_reaction_value_net,
            refresh_worker_reaction_net,
        )
        from core.models.muzero_value_net_builder import (
            build_gmz_net_from_search_cfg,
            build_smz_net_from_search_cfg,
        )

        if str(reaction_algo).strip().lower() == "smz":
            _r_cfg, _r_w = "smz_remote_search_cfg.json", "latest_smz_policy.pth"
            _r_flag, _r_tag, _r_build = "SMZ_REACTION_VALUE_POLICY", "SMZ", build_smz_net_from_search_cfg
        else:
            _r_cfg, _r_w = "gmz_remote_search_cfg.json", "latest_gmz_policy.pth"
            _r_flag, _r_tag, _r_build = "GMZ_REACTION_VALUE_POLICY", "GMZ", build_gmz_net_from_search_cfg
        _reaction_assets_dir = os.path.join(MODELS_DIR, "actor_sync")

        def _try_install_reaction_net():
            return install_worker_reaction_value_net(
                env,
                assets_dir=_reaction_assets_dir,
                cfg_name=_r_cfg,
                weights_name=_r_w,
                build_net_fn=_r_build,
                flag_env=_r_flag,
                log_tag=_r_tag,
                log_fn=append_agent_log,
            )

        _reaction_net = _try_install_reaction_net()
        _reaction_refresh_k = max(1, int(os.getenv("MUZERO_REACTION_NET_REFRESH_EVERY_EP", "10")))

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
            # refresh/retry локальной value-сети реакций каждые K эпизодов: если поставлена —
            # перегружаем веса; если нет (ассеты не были синканы на старте) — пробуем поставить снова.
            if int(_ep) > 0 and (int(_ep) % _reaction_refresh_k == 0):
                if _reaction_net is None:
                    _reaction_net = _try_install_reaction_net()
                else:
                    refresh_worker_reaction_net(
                        _reaction_net, assets_dir=_reaction_assets_dir, weights_name=_r_w
                    )
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


def _actor_learner_actor_entry_sampled_muzero(
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
    """Top-level entrypoint for Windows spawn pickling (Sampled MuZero actor)."""
    try:
        actor_device = torch.device("cuda" if SMZ_ACTOR_DEVICE_CUDA else "cpu")
        smz_net = make_sampled_muzero_net(
            obs_dim=int(n_observations),
            action_sizes=[int(x) for x in n_actions],
            latent_dim=int(search_cfg_payload.get("latent_dim", SMZ_LATENT_DIM)),
            hidden_dim=int(search_cfg_payload.get("hidden_dim", SMZ_HIDDEN_DIM)),
            num_layers=int(search_cfg_payload.get("num_layers", SMZ_NUM_LAYERS)),
            action_embed_dim=int(search_cfg_payload.get("action_embed_dim", SMZ_ACTION_EMBED_DIM)),
        ).to(actor_device)
        smz_net.load_state_dict(normalize_state_dict(init_weights))
        smz_net.eval()

        # torch.compile: только на CPU (на GPU overhead обычно не окупается)
        if SMZ_ACTOR_COMPILE and not SMZ_ACTOR_DEVICE_CUDA and hasattr(torch, "compile"):
            try:
                smz_net = torch.compile(smz_net, mode="default", fullgraph=False)
                append_agent_log("[SMZ][ACTOR] torch.compile enabled for actor inference (mode=default)")
            except Exception as e:
                append_agent_log(f"[SMZ][ACTOR] torch.compile skipped: {e}")

        search = SampledMuZeroSearch(
            smz_net,
            config=SampledMuZeroSearchConfig(
                num_samples=int(search_cfg_payload.get("num_samples", SMZ_NUM_SAMPLES)),
                discount=float(search_cfg_payload.get("discount", SMZ_DISCOUNT)),
                temperature=float(search_cfg_payload.get("temperature", SMZ_SEARCH_TEMP)),
                sample_temperature=float(search_cfg_payload.get("sample_temperature", SMZ_SAMPLE_TEMP)),
                prior_weight=float(search_cfg_payload.get("prior_weight", SMZ_PRIOR_WEIGHT)),
                dedup=bool(int(search_cfg_payload.get("dedup", int(SMZ_DEDUP)))),
            ),
            device=actor_device,
        )
        append_agent_log(
            f"[SMZ][ACTOR] actor={int(actor_idx)} device={actor_device.type} "
            f"latent={search_cfg_payload.get('latent_dim', SMZ_LATENT_DIM)} "
            f"num_samples={search_cfg_payload.get('num_samples', SMZ_NUM_SAMPLES)}"
        )
        sp_cfg = SampledSelfPlayConfig(
            temperature_opening_moves=int(sp_cfg_payload.get("temperature_opening_moves", SMZ_TEMP_OPENING_MOVES)),
            temperature_opening_value=float(sp_cfg_payload.get("temperature_opening_value", SMZ_TEMP_OPENING)),
            temperature_late_value=float(sp_cfg_payload.get("temperature_late_value", SMZ_TEMP_LATE)),
            outcome_only=bool(outcome_payload.get("outcome_only", SMZ_OUTCOME_ONLY)),
            outcome_value_win=float(outcome_payload.get("outcome_value_win", SMZ_OUTCOME_VALUE_WIN)),
            outcome_value_loss=float(outcome_payload.get("outcome_value_loss", SMZ_OUTCOME_VALUE_LOSS)),
            outcome_value_draw=float(outcome_payload.get("outcome_value_draw", SMZ_OUTCOME_VALUE_DRAW)),
        )

        enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
        mission_name = normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))
        env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
        len_model = int(len(model))

        sync_enabled = os.getenv("ACTOR_SYNC_ENABLED", "1") == "1"
        sync_path = os.path.join(MODELS_DIR, "actor_sync", "latest_smz_policy.pth")
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
                                smz_net.load_state_dict(normalize_state_dict(sd))
                                smz_net.eval()
                                search.net = smz_net
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

            transitions, info = play_episode_with_sampled_muzero(
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
            data_q.put(("error", f"smz_actor[{actor_idx}] {exc}"))
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

    try:
        _gmz_search_cfg_paths = publish_gmz_remote_search_cfg(
            obs_dim=int(n_observations),
            action_sizes=[int(x) for x in n_actions],
            latent_dim=int(GMZ_LATENT_DIM),
            hidden_dim=int(GMZ_HIDDEN_DIM),
            num_layers=int(GMZ_NUM_LAYERS),
            action_embed_dim=int(GMZ_ACTION_EMBED_DIM),
            num_simulations=int(GMZ_MCTS_SIMS),
            root_top_k=int(GMZ_ROOT_TOP_K),
            discount=float(GMZ_DISCOUNT),
            temperature=float(GMZ_SEARCH_TEMP),
            gumbel_scale=float(GMZ_GUMBEL_SCALE),
            prior_weight=float(GMZ_PRIOR_WEIGHT),
            batch_recurrent=bool(GMZ_BATCH_RECURRENT),
            tree_reuse=bool(GMZ_TREE_REUSE),
            mission=mission_name,
            sources=["train.py:auto"],
        )
        append_agent_log(
            f"[GMZ][REMOTE_IS] search_cfg обновлён (obs={int(n_observations)} "
            f"sims={int(GMZ_MCTS_SIMS)}): {_gmz_search_cfg_paths}"
        )
    except Exception as exc:
        append_agent_log(
            f"[GMZ][REMOTE_IS][WARN] не удалось записать search_cfg: {exc}. "
            "Где: publish_gmz_remote_search_cfg. Что делать: откройте Qt GUI на ПК1."
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
        except Exception as exc:
            _raise_resume_error("GMZ", RESUME_CHECKPOINT, f"не удалось прочитать файл: {exc}")
        if not isinstance(checkpoint, dict):
            _raise_resume_error("GMZ", RESUME_CHECKPOINT, "payload не является словарём")
        policy_state = checkpoint.get("gumbel_muzero_net")
        if not isinstance(policy_state, dict):
            policy_state = _extract_policy_state_dict(checkpoint)
        if not isinstance(policy_state, dict):
            _raise_resume_error(
                "GMZ",
                RESUME_CHECKPOINT,
                "в чекпойнте нет gumbel_muzero_net/policy state_dict (нужен Gumbel MuZero checkpoint)",
            )
        gmz_arch = gumbel_muzero_arch_from_payload(checkpoint)
        cur_gmz_arch = gumbel_muzero_kwargs_from_env()
        if gmz_arch != cur_gmz_arch:
            append_agent_log(
                f"[GMZ][RESUME][WARN] arch mismatch checkpoint={gmz_arch} current={cur_gmz_arch}; strict=False load"
            )
        try:
            load_gumbel_muzero_state_dict(
                gmz_net,
                normalize_state_dict(policy_state),
                log_fn=append_agent_log,
            )
        except Exception as exc:
            _raise_resume_error("GMZ", RESUME_CHECKPOINT, f"не удалось загрузить веса gumbel_muzero_net: {exc}")
        opt_state = checkpoint.get("optimizer")
        if isinstance(opt_state, dict):
            try:
                optimizer.load_state_dict(opt_state)
            except Exception as exc:
                append_agent_log(
                    f"[GMZ][RESUME][WARN] optimizer load failed: {exc}. "
                    "Где: train.py (_main_actor_learner_gumbel_muzero). Что делать: продолжить с чистым optimizer."
                )
        sched_state = checkpoint.get("lr_scheduler")
        if gmz_scheduler is not None and isinstance(sched_state, dict):
            try:
                gmz_scheduler.load_state_dict(sched_state)
            except Exception as exc:
                append_agent_log(
                    f"[GMZ][RESUME][WARN] lr_scheduler load failed: {exc}. "
                    "Где: train.py (_main_actor_learner_gumbel_muzero). Что делать: продолжить без scheduler state."
                )
        replay_state = checkpoint.get("replay_memory")
        if replay_state is not None:
            try:
                replay.load_state_dict(replay_state)
            except Exception as exc:
                append_agent_log(
                    f"[GMZ][RESUME][WARN] replay load failed: {exc}. "
                    "Где: train.py (_main_actor_learner_gumbel_muzero). Что делать: продолжить с пустым буфером."
                )
        # Семантика totLifeT — «дополнительные игры за этот запуск» (как DQN/PPO):
        # episodes_finished считаем с нуля, resume_episode_base — накопительная база.
        resume_episode_base = int(checkpoint.get("episode", 0) or 0)
        global_step = int(checkpoint.get("global_step", 0) or 0)
        optimize_steps = int(checkpoint.get("optimize_steps", 0) or 0)
        policy_version = int(checkpoint.get("policy_version", optimize_steps) or optimize_steps)
        append_agent_log(
            "[GMZ][RESUME] "
            f"path={RESUME_CHECKPOINT} episode_base={resume_episode_base} replay={len(replay)} "
            f"global_step={global_step} optimize_steps={optimize_steps} policy_version={policy_version}"
        )

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
    train_t0_summary = time.perf_counter()
    last_checkpoint = ""
    last_loss = 0.0

    checkpoint_dir = os.path.join(MODELS_DIR, "gumbel_muzero")
    os.makedirs(checkpoint_dir, exist_ok=True)
    sync_dir = os.path.join(MODELS_DIR, "actor_sync")
    os.makedirs(sync_dir, exist_ok=True)
    sync_path = os.path.join(sync_dir, "latest_gmz_policy.pth")

    def _save_gmz_sync() -> None:
        cpu_sd = {k: v.detach().cpu() for k, v in normalize_state_dict(gmz_net.state_dict()).items()}
        _torch_save_atomic(
            {
                "policy_version": int(policy_version),
                "optimize_steps": int(optimize_steps),
                "state_dict": cpu_sd,
            },
            sync_path,
            label="latest_gmz_policy",
        )

    def _save_checkpoint(episode_idx: int) -> str:
        ckpt_path = os.path.join(checkpoint_dir, f"checkpoint_ep{int(episode_idx)}.pth")
        payload = {
            "algo": "gumbel_muzero",
            "gumbel_muzero_net": gmz_net.state_dict(),
            "policy_net": gmz_net.state_dict(),
            "optimizer": optimizer.state_dict(),
            "episode": int(episode_idx),
            "episodes_finished": int(episode_idx),
            "global_step": int(global_step),
            "optimize_steps": int(optimize_steps),
            "policy_version": int(policy_version),
            "replay_memory": replay.state_dict(),
            "env_contract": env_contract,
            "num_actors": int(GMZ_NUM_ACTORS),
            "arch": gumbel_muzero_kwargs_from_env(),
            "outcome_only": bool(GMZ_OUTCOME_ONLY),
            "outcome_value_win": float(GMZ_OUTCOME_VALUE_WIN),
            "outcome_value_loss": float(GMZ_OUTCOME_VALUE_LOSS),
            "outcome_value_draw": float(GMZ_OUTCOME_VALUE_DRAW),
        }
        if gmz_scheduler is not None:
            payload["lr_scheduler"] = gmz_scheduler.state_dict()
        torch.save(payload, ckpt_path)
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
                    "gmz",
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
            # TensorBoard: метрики эпизода + телеметрия (no-op, если TB выключен).
            try:
                from core.telemetry.tb_logger import get_tb_logger

                _tb = get_tb_logger(str(run_id), algo="gumbel_muzero")
                if _tb.active:
                    _tb.log_episode(payload, step=int(episodes_finished))
                    _tb.log_telemetry(step=int(episodes_finished))
            except Exception:
                pass
            target_n = min(int(totLifeT), int(episodes_finished))
            if target_n > int(pbar.n):
                pbar.update(target_n - int(pbar.n))
            if (episodes_finished % ACTOR_PROGRESS_STDOUT_EVERY == 0) or (episodes_finished >= int(totLifeT)):
                print(f"ep={episodes_finished}/{totLifeT}", flush=True)
            log_train_episode_line(
                payload,
                ep=int(episodes_finished),
                total=int(totLifeT),
                algo="gmz",
                actor_idx=int(payload.get("actor_idx", -1) or -1),
            )
            _maybe_train_progress_heartbeat(force=True)
            if SAVE_EVERY > 0 and (episodes_finished % max(1, SAVE_EVERY) == 0):
                last_checkpoint = _save_checkpoint(resume_episode_base + episodes_finished)
                append_agent_log(f"[GMZ][CHECKPOINT] ep={resume_episode_base + episodes_finished} path={last_checkpoint}")
            if (
                ACTOR_DET_EVAL_ENABLED
                and episodes_finished > last_actor_det_eval_ep
                and (episodes_finished % ACTOR_DET_EVAL_EVERY_EPISODES == 0 or episodes_finished == int(totLifeT))
            ):
                last_actor_det_eval_ep = int(episodes_finished)
                det_payload = _gmz_det_payload_from_rows(
                    list(ep_rows)[-int(TRAIN_METRICS_WINDOW_EPISODES):],
                    episode_idx=int(episodes_finished),
                    train_loss=float(last_loss),
                    eval_tag="train_window",
                )
                _save_actor_det_eval_snapshot(run_id=str(run_id), payload=det_payload, metrics_dir=METRICS_DIR)
                det_gui = save_actor_det_eval_plot(run_id=str(run_id), metrics_dir=METRICS_DIR)
                learner_side = str(learner_identity.side or "P1").strip().upper() or "P1"
                opponent_side = "P2" if learner_side == "P1" else "P1"
                _write_det_eval_data_json(
                    run_id=str(run_id),
                    det_plot_gui_paths=det_gui or {},
                    model_path=str(last_checkpoint or ""),
                    metrics_mode="train_window",
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
            tr = gmz_transition_from_rollout_dict(
                raw,
                default_policy_version=int(payload.get("policy_version", 0) or 0),
            )
            if tr is None:
                continue
            transitions.append(tr)
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
            # TensorBoard: тренировочные лоссы MuZero (no-op, если TB выключен).
            try:
                from core.telemetry.tb_logger import get_tb_logger

                _tb = get_tb_logger(str(run_id), algo="gumbel_muzero")
                if _tb.active:
                    _tb_metrics = {
                        "loss": float(last_loss),
                        "policy_loss": float(update_info.get("policy_loss", 0.0) or 0.0),
                        "value_loss": float(update_info.get("value_loss", 0.0) or 0.0),
                        "reward_loss": float(update_info.get("reward_loss", 0.0) or 0.0),
                        "lr": float(optimizer.param_groups[0]["lr"]),
                    }
                    _tb.log_train(_tb_metrics, step=int(optimize_steps))
            except Exception:
                pass
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
        last_checkpoint = _save_checkpoint(int(resume_episode_base + (episodes_finished or totLifeT)))
        append_agent_log(f"[GMZ][CHECKPOINT] final path={last_checkpoint}")

    if ep_rows:
        save_extra_metrics(
            run_id=run_id,
            ep_rows=ep_rows,
            metrics_dir=METRICS_DIR,
            write_legacy_gui_plots=False,
        )
        save_heuristic_metrics_snapshot(run_id=run_id, ep_rows=ep_rows, metrics_dir=METRICS_DIR)
        # Финальный снапшот метрик (окно тренировки) для надёжной привязки GUI к run_id.
        det_payload = _gmz_det_payload_from_rows(
            list(ep_rows)[-int(TRAIN_METRICS_WINDOW_EPISODES):],
            episode_idx=int(max(episodes_finished, 1)),
            train_loss=float(last_loss),
            eval_tag="train_window",
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
                metrics_mode="train_window",
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
                metrics_mode="train_window",
                extra={"algo": "gumbel_muzero", "mode": "actor_learner", "det_eval_note": "нет точек DET-eval"},
            )
        append_agent_log(f"[GMZ][METRICS] saved run_id={run_id}")
        _log_train_summary(ep_rows, time.perf_counter() - train_t0_summary)

    final_episode = int(resume_episode_base + episodes_finished)
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
            "arch": gumbel_muzero_kwargs_from_env(),
            "episode": int(final_episode),
            "source_model_path": str(last_checkpoint or ""),
            "mode": "actor_learner",
            "num_actors": int(GMZ_NUM_ACTORS),
            "policy_version": int(policy_version),
            "outcome_only": bool(GMZ_OUTCOME_ONLY),
            "outcome_value_win": float(GMZ_OUTCOME_VALUE_WIN),
            "outcome_value_loss": float(GMZ_OUTCOME_VALUE_LOSS),
            "outcome_value_draw": float(GMZ_OUTCOME_VALUE_DRAW),
        },
    )
    append_agent_log(
        "[GMZ][ACTOR_LEARNER] done "
        f"episodes={final_episode}/{resume_episode_base + int(totLifeT)} checkpoint={last_checkpoint} "
        f"global_step={global_step} updates={optimize_steps} replay={len(replay)}"
    )


def _main_actor_learner_sampled_muzero(*, roster_config, totLifeT, clip_reward_enabled, clip_reward_min, clip_reward_max) -> None:
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
        extras={"actor_learner": 1, "train_algo": "sampled_muzero", "num_actors": int(SMZ_NUM_ACTORS)},
    )

    try:
        _smz_search_cfg_paths = publish_smz_remote_search_cfg(
            obs_dim=int(n_observations),
            action_sizes=[int(x) for x in n_actions],
            latent_dim=int(SMZ_LATENT_DIM),
            hidden_dim=int(SMZ_HIDDEN_DIM),
            num_layers=int(SMZ_NUM_LAYERS),
            action_embed_dim=int(SMZ_ACTION_EMBED_DIM),
            num_samples=int(SMZ_NUM_SAMPLES),
            discount=float(SMZ_DISCOUNT),
            temperature=float(SMZ_SEARCH_TEMP),
            sample_temperature=float(SMZ_SAMPLE_TEMP),
            prior_weight=float(SMZ_PRIOR_WEIGHT),
            dedup=bool(SMZ_DEDUP),
            mission=mission_name,
            sources=["train.py:auto"],
        )
        append_agent_log(
            f"[SMZ][REMOTE_IS] search_cfg обновлён (obs={int(n_observations)} "
            f"num_samples={int(SMZ_NUM_SAMPLES)}): {_smz_search_cfg_paths}"
        )
    except Exception as exc:
        append_agent_log(
            f"[SMZ][REMOTE_IS][WARN] не удалось записать search_cfg: {exc}. "
            "Где: publish_smz_remote_search_cfg. Что делать: tools\\write_smz_remote_search_cfg.bat "
            "или запуск SMZ Remote IS из лаунчера ПК2."
        )

    smz_net = make_sampled_muzero_net(
        obs_dim=int(n_observations),
        action_sizes=[int(x) for x in n_actions],
        latent_dim=int(SMZ_LATENT_DIM),
        hidden_dim=int(SMZ_HIDDEN_DIM),
        num_layers=int(SMZ_NUM_LAYERS),
        action_embed_dim=int(SMZ_ACTION_EMBED_DIM),
    ).to(device)

    # torch.compile for learner — ~15-30% faster training, compilation cost ~10-20s
    if SMZ_LEARNER_COMPILE and device.type == "cuda" and hasattr(torch, "compile"):
        try:
            smz_net = torch.compile(smz_net, mode="reduce-overhead", fullgraph=False)
            append_agent_log("[SMZ][LEARNER] torch.compile enabled (mode=reduce-overhead)")
        except Exception as e:
            append_agent_log(f"[SMZ][LEARNER] torch.compile skipped: {e}")

    optimizer = optim.AdamW(smz_net.parameters(), lr=SMZ_LR, amsgrad=True)
    _patch_optimizer_methods_no_compile(optimizer)
    replay = GumbelMuZeroReplayBuffer(capacity=SMZ_REPLAY_CAPACITY)
    trainer_cfg = SampledMuZeroTrainConfig(
        lr=SMZ_LR,
        batch_size=SMZ_BATCH_SIZE,
        unroll_steps=SMZ_UNROLL_STEPS,
        tbptt_truncate=SMZ_TBPTT_TRUNCATE,
        value_loss_weight=SMZ_VALUE_LOSS_WEIGHT,
        reward_loss_weight=SMZ_REWARD_LOSS_WEIGHT,
        consistency_loss_weight=SMZ_CONSISTENCY_W,
        l2_weight=SMZ_L2_WEIGHT,
        max_grad_norm=SMZ_MAX_GRAD_NORM,
        lr_scheduler=SMZ_LR_SCHEDULER,
        lr_warmup_steps=SMZ_LR_WARMUP_STEPS,
        lr_total_steps=SMZ_LR_TOTAL_STEPS,
        max_policy_staleness_updates=int(SMZ_MAX_POLICY_STALENESS_UPDATES),
        vtrace_full=bool(SMZ_VTRACE_FULL),
        vtrace_rho_clip=SMZ_VTRACE_RHO_CLIP,
        vtrace_c_clip=SMZ_VTRACE_C_CLIP,
    )
    smz_scheduler = make_smz_lr_scheduler(optimizer, trainer_cfg)

    # B4: EMA target for SimSiam consistency loss
    ema_target = None
    if float(SMZ_CONSISTENCY_W) > 0.0:
        ema_target = SampledMuZeroEMATarget(smz_net, tau=SMZ_EMA_TAU)
        append_agent_log(f"[SMZ][EMA] tau={SMZ_EMA_TAU} consistency_w={SMZ_CONSISTENCY_W}")

    # B2: Reanalyzer for real-search policy target refresh
    reanalyze_frac = float(SMZ_REANALYZE_FRACTION)
    smz_reanalyzer = None
    if reanalyze_frac > 0.0:
        _search_for_reanalyze = SampledMuZeroSearch(
            smz_net,
            config=SampledMuZeroSearchConfig(
                num_samples=max(1, int(SMZ_NUM_SAMPLES) // 2),  # fast search for reanalysis
                discount=float(SMZ_DISCOUNT),
                temperature=float(SMZ_SEARCH_TEMP),
                sample_temperature=float(SMZ_SAMPLE_TEMP),
                prior_weight=float(SMZ_PRIOR_WEIGHT),
                dedup=SMZ_DEDUP,
            ),
            device=device,
        )
        smz_reanalyzer = GumbelMuZeroReanalyzer(
            config=GumbelMuZeroReanalysisConfig(fast_sims=max(1, int(SMZ_NUM_SAMPLES) // 2)),
            search=_search_for_reanalyze,
            device=device,
        )
        append_agent_log(f"[SMZ][REANALYZE] fraction={reanalyze_frac} fast_samples={max(1, int(SMZ_NUM_SAMPLES) // 2)}")

    policy_version = 0
    optimize_steps = 0
    global_step = 0
    episodes_finished = 0
    resume_episode_base = 0
    if RESUME_CHECKPOINT:
        try:
            checkpoint = _load_checkpoint_payload(RESUME_CHECKPOINT)
        except Exception as exc:
            _raise_resume_error("SMZ", RESUME_CHECKPOINT, f"не удалось прочитать файл: {exc}")
        if not isinstance(checkpoint, dict):
            _raise_resume_error("SMZ", RESUME_CHECKPOINT, "payload не является словарём")
        policy_state = checkpoint.get("sampled_muzero_net")
        if not isinstance(policy_state, dict):
            policy_state = _extract_policy_state_dict(checkpoint)
        if not isinstance(policy_state, dict):
            _raise_resume_error(
                "SMZ",
                RESUME_CHECKPOINT,
                "в чекпойнте нет sampled_muzero_net/policy state_dict (нужен Sampled MuZero checkpoint)",
            )
        smz_arch = sampled_muzero_arch_from_payload(checkpoint)
        cur_smz_arch = sampled_muzero_kwargs_from_env()
        if smz_arch != cur_smz_arch:
            append_agent_log(
                f"[SMZ][RESUME][WARN] arch mismatch checkpoint={smz_arch} current={cur_smz_arch}; strict=False load"
            )
        try:
            load_sampled_muzero_state_dict(
                smz_net,
                normalize_state_dict(policy_state),
                log_fn=append_agent_log,
            )
        except Exception as exc:
            _raise_resume_error("SMZ", RESUME_CHECKPOINT, f"не удалось загрузить веса sampled_muzero_net: {exc}")
        opt_state = checkpoint.get("optimizer")
        if isinstance(opt_state, dict):
            try:
                optimizer.load_state_dict(opt_state)
            except Exception as exc:
                append_agent_log(
                    f"[SMZ][RESUME][WARN] optimizer load failed: {exc}. "
                    "Где: train.py (_main_actor_learner_sampled_muzero). Что делать: продолжить с чистым optimizer."
                )
        sched_state = checkpoint.get("lr_scheduler")
        if smz_scheduler is not None and isinstance(sched_state, dict):
            try:
                smz_scheduler.load_state_dict(sched_state)
            except Exception as exc:
                append_agent_log(
                    f"[SMZ][RESUME][WARN] lr_scheduler load failed: {exc}. "
                    "Где: train.py (_main_actor_learner_sampled_muzero). Что делать: продолжить без scheduler state."
                )
        replay_state = checkpoint.get("replay_memory")
        if replay_state is not None:
            try:
                replay.load_state_dict(replay_state)
            except Exception as exc:
                append_agent_log(
                    f"[SMZ][RESUME][WARN] replay load failed: {exc}. "
                    "Где: train.py (_main_actor_learner_sampled_muzero). Что делать: продолжить с пустым буфером."
                )
        # Семантика totLifeT — «дополнительные игры за этот запуск» (как DQN/PPO):
        # episodes_finished считаем с нуля, resume_episode_base — накопительная база.
        resume_episode_base = int(checkpoint.get("episode", 0) or 0)
        global_step = int(checkpoint.get("global_step", 0) or 0)
        optimize_steps = int(checkpoint.get("optimize_steps", 0) or 0)
        policy_version = int(checkpoint.get("policy_version", optimize_steps) or optimize_steps)
        append_agent_log(
            "[SMZ][RESUME] "
            f"path={RESUME_CHECKPOINT} episode_base={resume_episode_base} replay={len(replay)} "
            f"global_step={global_step} optimize_steps={optimize_steps} policy_version={policy_version}"
        )

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
                    "[SMZ][SELFPLAY][WARN] "
                    f"Не удалось загрузить оппонента agent_id={OPPONENT_AGENT_ID}; fallback на heuristic. exc={exc}"
                )
        else:
            append_agent_log("[SMZ][SELFPLAY][WARN] SELF_PLAY_ENABLED=1, но OPPONENT_AGENT_ID пустой; fallback на heuristic.")

    effective_num_actors = int(SMZ_ACTOR_EFFECTIVE_NUM_ACTORS)
    if SMZ_INFERENCE_SERVER_USING_FALLBACK:
        append_agent_log(
            "[SMZ][CONFIG][FALLBACK] Запрошен inference server (variant B), но CUDA недоступна. "
            f"Переключаемся на вариант A: actor_device=cpu, num_actors={SMZ_ACTOR_CPU_FALLBACK_NUM_ACTORS}."
        )
    elif SMZ_INFERENCE_SERVER_ENABLED:
        if SMZ_INFERENCE_REMOTE:
            append_agent_log(
                f"[SMZ][CONFIG] Remote inference server (variant B-remote): env_workers={effective_num_actors} "
                f"host={SMZ_INFERENCE_REMOTE_HOST} port={SMZ_INFERENCE_REMOTE_PORT}"
            )
        else:
            append_agent_log(
                f"[SMZ][CONFIG] Inference server (variant B-local): env_workers={effective_num_actors} "
                f"batch={SMZ_INFERENCE_BATCH_SIZE} interval_ms={SMZ_INFERENCE_BATCH_INTERVAL_MS}"
            )
    elif SMZ_ACTOR_USING_CUDA_FALLBACK:
        append_agent_log(
            "[SMZ][CONFIG][FALLBACK] В hyperparams указан actor_device=cuda, но PyTorch не видит GPU с CUDA "
            f"(torch.cuda.is_available()=False, device_count={int(torch.cuda.device_count()) if hasattr(torch.cuda, 'device_count') else 0}). "
            f"Переключаемся на CPU: actor_device=cpu, num_actors={effective_num_actors} "
            f"(вместо cuda + num_actors={SMZ_NUM_ACTORS} + actor_max_cuda={SMZ_ACTOR_MAX_CUDA}). "
            "Чтобы включить GPU-акторов: установите драйвер NVIDIA и PyTorch с поддержкой CUDA (cu124/cu128)."
        )
    elif SMZ_ACTOR_DEVICE_CUDA:
        append_agent_log(
            f"[SMZ][CONFIG] GPU actors: {effective_num_actors} "
            f"(capped from num_actors={SMZ_NUM_ACTORS}, actor_max_cuda={SMZ_ACTOR_MAX_CUDA})"
        )

    append_agent_log(
        "[SMZ][CONFIG] "
        f"num_samples={SMZ_NUM_SAMPLES} unroll={SMZ_UNROLL_STEPS} "
        f"batch={SMZ_BATCH_SIZE} actors={SMZ_NUM_ACTORS} effective_actors={effective_num_actors} "
        f"inference_server={int(SMZ_INFERENCE_SERVER_ENABLED)} "
        f"inference_mode={SMZ_INFERENCE_SERVER_MODE} env_workers={SMZ_NUM_ENV_WORKERS} "
        f"replay={SMZ_REPLAY_CAPACITY} "
        f"actor_device_req={SMZ_ACTOR_DEVICE_REQUESTED} actor_device_cuda={int(SMZ_ACTOR_DEVICE_CUDA)} "
        f"cuda_fallback={int(SMZ_ACTOR_USING_CUDA_FALLBACK)} "
        f"vtrace_full={int(SMZ_VTRACE_FULL)} rho_clip={SMZ_VTRACE_RHO_CLIP} c_clip={SMZ_VTRACE_C_CLIP} "
        f"atom={SMZ_ATOM_RANGE} dedup={int(SMZ_DEDUP)} "
        f"reanalyze={SMZ_REANALYZE_FRACTION} consistency_w={SMZ_CONSISTENCY_W} "
        f"ema_tau={SMZ_EMA_TAU} max_grad_norm={SMZ_MAX_GRAD_NORM} "
        f"actor_compile={int(SMZ_ACTOR_COMPILE)} learner_compile={int(SMZ_LEARNER_COMPILE)} "
        f"outcome_only={int(SMZ_OUTCOME_ONLY)} opponent={opponent_source_label}/{opponent_algo_label}"
    )

    ep_rows: list[dict] = []
    train_t0_summary = time.perf_counter()
    last_checkpoint = ""
    last_loss = 0.0

    checkpoint_dir = os.path.join(MODELS_DIR, "sampled_muzero")
    os.makedirs(checkpoint_dir, exist_ok=True)
    sync_dir = os.path.join(MODELS_DIR, "actor_sync")
    os.makedirs(sync_dir, exist_ok=True)
    sync_path = os.path.join(sync_dir, "latest_smz_policy.pth")

    def _save_smz_sync() -> None:
        cpu_sd = {k: v.detach().cpu() for k, v in normalize_state_dict(smz_net.state_dict()).items()}
        _torch_save_atomic(
            {
                "policy_version": int(policy_version),
                "optimize_steps": int(optimize_steps),
                "state_dict": cpu_sd,
            },
            sync_path,
            label="latest_smz_policy",
        )

    def _save_checkpoint(episode_idx: int) -> str:
        ckpt_path = os.path.join(checkpoint_dir, f"checkpoint_ep{int(episode_idx)}.pth")
        payload = {
            "algo": "sampled_muzero",
            "sampled_muzero_net": smz_net.state_dict(),
            "policy_net": smz_net.state_dict(),
            "optimizer": optimizer.state_dict(),
            "episode": int(episode_idx),
            "episodes_finished": int(episode_idx),
            "global_step": int(global_step),
            "optimize_steps": int(optimize_steps),
            "policy_version": int(policy_version),
            "replay_memory": replay.state_dict(),
            "env_contract": env_contract,
            "num_actors": int(SMZ_NUM_ACTORS),
            "arch": sampled_muzero_kwargs_from_env(),
            "outcome_only": bool(SMZ_OUTCOME_ONLY),
            "outcome_value_win": float(SMZ_OUTCOME_VALUE_WIN),
            "outcome_value_loss": float(SMZ_OUTCOME_VALUE_LOSS),
            "outcome_value_draw": float(SMZ_OUTCOME_VALUE_DRAW),
        }
        if smz_scheduler is not None:
            payload["lr_scheduler"] = smz_scheduler.state_dict()
        torch.save(payload, ckpt_path)
        return ckpt_path

    smz_sp_cfg = SampledSelfPlayConfig(
        temperature_opening_moves=int(SMZ_TEMP_OPENING_MOVES),
        temperature_opening_value=float(SMZ_TEMP_OPENING),
        temperature_late_value=float(SMZ_TEMP_LATE),
        outcome_only=bool(SMZ_OUTCOME_ONLY),
        outcome_value_win=float(SMZ_OUTCOME_VALUE_WIN),
        outcome_value_loss=float(SMZ_OUTCOME_VALUE_LOSS),
        outcome_value_draw=float(SMZ_OUTCOME_VALUE_DRAW),
    )
    _ = smz_sp_cfg  # передаётся акторам через sp_cfg_payload; держим для совместимости с gmz-паттерном

    _save_smz_sync()
    remaining_episodes = max(0, int(totLifeT) - int(episodes_finished))
    ctx = mp.get_context("spawn")
    data_q: mp.Queue = ctx.Queue(maxsize=int(SMZ_ACTOR_QUEUE_MAX))
    procs: list = []
    inf_proc = None
    request_q = None

    init_weights_cpu = {
        k: v.detach().cpu() for k, v in normalize_state_dict(smz_net.state_dict()).items()
    }
    sp_cfg_payload = {
        "temperature_opening_moves": SMZ_TEMP_OPENING_MOVES,
        "temperature_opening_value": SMZ_TEMP_OPENING,
        "temperature_late_value": SMZ_TEMP_LATE,
    }
    search_cfg_payload = {
        "obs_dim": int(n_observations),
        "action_sizes": [int(x) for x in n_actions],
        "latent_dim": int(SMZ_LATENT_DIM),
        "hidden_dim": int(SMZ_HIDDEN_DIM),
        "num_layers": int(SMZ_NUM_LAYERS),
        "action_embed_dim": int(SMZ_ACTION_EMBED_DIM),
        "num_samples": int(SMZ_NUM_SAMPLES),
        "discount": float(SMZ_DISCOUNT),
        "temperature": float(SMZ_SEARCH_TEMP),
        "sample_temperature": float(SMZ_SAMPLE_TEMP),
        "prior_weight": float(SMZ_PRIOR_WEIGHT),
        "dedup": 1 if SMZ_DEDUP else 0,
    }
    outcome_payload = {
        "outcome_only": SMZ_OUTCOME_ONLY,
        "outcome_value_win": SMZ_OUTCOME_VALUE_WIN,
        "outcome_value_loss": SMZ_OUTCOME_VALUE_LOSS,
        "outcome_value_draw": SMZ_OUTCOME_VALUE_DRAW,
        "policy_version": int(policy_version),
    }

    if remaining_episodes > 0:
        if SMZ_INFERENCE_SERVER_ENABLED and SMZ_INFERENCE_REMOTE:
            from core.models.gmz_inference_transport import remote_health_check

            try:
                hc = remote_health_check(
                    host=SMZ_INFERENCE_REMOTE_HOST,
                    port=int(SMZ_INFERENCE_REMOTE_PORT),
                    auth_token=SMZ_INFERENCE_REMOTE_AUTH_TOKEN,
                    timeout=min(3.0, float(SMZ_INFERENCE_TIMEOUT)),
                )
                append_agent_log(
                    f"[SMZ][REMOTE_CLIENT] health_check ok host={SMZ_INFERENCE_REMOTE_HOST} "
                    f"port={SMZ_INFERENCE_REMOTE_PORT} policy_version={hc.get('policy_version', '?')} "
                    f"gpu={hc.get('gpu_name', '?')}"
                )
            except Exception as exc:
                append_agent_log(
                    f"[SMZ][REMOTE_CLIENT] health_check failed host={SMZ_INFERENCE_REMOTE_HOST}: {exc}"
                )
                raise RuntimeError(
                    "Remote IS недоступен. Проверьте: 1) сервер на ПК2, 2) IP/порт, "
                    f"3) firewall (TCP {SMZ_INFERENCE_REMOTE_PORT})."
                ) from exc
            append_agent_log(
                f"[SMZ][REMOTE_CLIENT] connecting to tcp://{SMZ_INFERENCE_REMOTE_HOST}:{SMZ_INFERENCE_REMOTE_PORT}"
            )
        elif SMZ_INFERENCE_SERVER_LOCAL:
            request_q = ctx.Queue(maxsize=int(SMZ_INFERENCE_REQUEST_QUEUE_MAX))
            reply_queues = [ctx.Queue(maxsize=8) for _ in range(int(effective_num_actors))]
            inf_proc = ctx.Process(
                target=smz_inference_server_entry,
                args=(
                    request_q,
                    reply_queues,
                    sync_path,
                    init_weights_cpu,
                    search_cfg_payload,
                ),
                kwargs={
                    "inference_batch_size": int(SMZ_INFERENCE_BATCH_SIZE),
                    "inference_batch_interval_ms": float(SMZ_INFERENCE_BATCH_INTERVAL_MS),
                    "inference_server_compile": bool(SMZ_INFERENCE_SERVER_COMPILE),
                    "clear_tree_on_weight_sync": bool(SMZ_CLEAR_TREE_ON_WEIGHT_SYNC),
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
            if SMZ_INFERENCE_SERVER_ENABLED:
                worker_args = (
                    int(a_idx),
                    int(actor_episodes),
                    roster_config,
                    int(b_len),
                    int(b_hei),
                    int(n_observations),
                    list(n_actions),
                    int(SMZ_ACTOR_BATCH_SEND),
                    data_q,
                    request_q,
                    reply_queues[int(a_idx)] if SMZ_INFERENCE_SERVER_LOCAL else None,
                    int(1 if SELF_PLAY_ENABLED else 0),
                    opponent_spec,
                    sp_cfg_payload,
                    outcome_payload,
                    float(SMZ_INFERENCE_TIMEOUT),
                    str(SMZ_INFERENCE_SERVER_MODE),
                    str(SMZ_INFERENCE_REMOTE_HOST),
                    int(SMZ_INFERENCE_REMOTE_PORT),
                    str(SMZ_INFERENCE_REMOTE_AUTH_TOKEN),
                    "smz",
                )
                p = ctx.Process(
                    target=_gmz_env_worker_entry,
                    args=worker_args,
                    daemon=True,
                )
            else:
                p = ctx.Process(
                    target=_actor_learner_actor_entry_sampled_muzero,
                    args=(
                        int(a_idx),
                        int(actor_episodes),
                        roster_config,
                        int(b_len),
                        int(b_hei),
                        int(n_observations),
                        list(n_actions),
                        init_weights_cpu,
                        int(SMZ_ACTOR_BATCH_SEND),
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
            # TensorBoard: метрики эпизода + телеметрия (no-op, если TB выключен).
            try:
                from core.telemetry.tb_logger import get_tb_logger

                _tb = get_tb_logger(str(run_id), algo="sampled_muzero")
                if _tb.active:
                    _tb.log_episode(payload, step=int(episodes_finished))
                    _tb.log_telemetry(step=int(episodes_finished))
            except Exception:
                pass
            target_n = min(int(totLifeT), int(episodes_finished))
            if target_n > int(pbar.n):
                pbar.update(target_n - int(pbar.n))
            if (episodes_finished % ACTOR_PROGRESS_STDOUT_EVERY == 0) or (episodes_finished >= int(totLifeT)):
                print(f"ep={episodes_finished}/{totLifeT}", flush=True)
            log_train_episode_line(
                payload,
                ep=int(episodes_finished),
                total=int(totLifeT),
                algo="smz",
                actor_idx=int(payload.get("actor_idx", -1) or -1),
            )
            _maybe_train_progress_heartbeat(force=True)
            if SAVE_EVERY > 0 and (episodes_finished % max(1, SAVE_EVERY) == 0):
                last_checkpoint = _save_checkpoint(resume_episode_base + episodes_finished)
                append_agent_log(f"[SMZ][CHECKPOINT] ep={resume_episode_base + episodes_finished} path={last_checkpoint}")
            if (
                ACTOR_DET_EVAL_ENABLED
                and episodes_finished > last_actor_det_eval_ep
                and (episodes_finished % ACTOR_DET_EVAL_EVERY_EPISODES == 0 or episodes_finished == int(totLifeT))
            ):
                last_actor_det_eval_ep = int(episodes_finished)
                det_payload = _gmz_det_payload_from_rows(
                    list(ep_rows)[-int(TRAIN_METRICS_WINDOW_EPISODES):],
                    episode_idx=int(episodes_finished),
                    train_loss=float(last_loss),
                    eval_tag="train_window",
                )
                _save_actor_det_eval_snapshot(run_id=str(run_id), payload=det_payload, metrics_dir=METRICS_DIR)
                det_gui = save_actor_det_eval_plot(run_id=str(run_id), metrics_dir=METRICS_DIR)
                learner_side = str(learner_identity.side or "P1").strip().upper() or "P1"
                opponent_side = "P2" if learner_side == "P1" else "P1"
                _write_det_eval_data_json(
                    run_id=str(run_id),
                    det_plot_gui_paths=det_gui or {},
                    model_path=str(last_checkpoint or ""),
                    metrics_mode="train_window",
                    extra={
                        "algo": "sampled_muzero",
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
            tr = gmz_transition_from_rollout_dict(
                raw,
                default_policy_version=int(payload.get("policy_version", 0) or 0),
            )
            if tr is None:
                continue
            transitions.append(tr)
        if not transitions:
            continue
        replay.push_many(transitions)
        global_step += len(transitions)
        for _ in range(int(SMZ_UPDATES_PER_ROLLOUT)):
            if len(replay) < max(int(SMZ_REPLAY_MIN_SIZE), int(SMZ_BATCH_SIZE)):
                break
            update_info = train_sampled_muzero_step(
                net=smz_net,
                optimizer=optimizer,
                replay=replay,
                config=trainer_cfg,
                device=device,
                current_policy_version=int(policy_version),
                scheduler=smz_scheduler,
                ema_target=ema_target,
            )
            if update_info is None:
                continue
            optimize_steps += 1
            policy_version += 1
            last_loss = float(update_info.get("loss", 0.0) or 0.0)
            metrics_obj.updateLoss(float(last_loss))
            # TensorBoard: тренировочные лоссы MuZero (no-op, если TB выключен).
            try:
                from core.telemetry.tb_logger import get_tb_logger

                _tb = get_tb_logger(str(run_id), algo="sampled_muzero")
                if _tb.active:
                    _tb_metrics = {
                        "loss": float(last_loss),
                        "policy_loss": float(update_info.get("policy_loss", 0.0) or 0.0),
                        "value_loss": float(update_info.get("value_loss", 0.0) or 0.0),
                        "reward_loss": float(update_info.get("reward_loss", 0.0) or 0.0),
                        "lr": float(optimizer.param_groups[0]["lr"]),
                    }
                    _tb.log_train(_tb_metrics, step=int(optimize_steps))
            except Exception:
                pass
            # B2: Periodic reanalysis — refresh policy targets with real search
            if (
                smz_reanalyzer is not None
                and float(reanalyze_frac) > 0.0
                and optimize_steps > 0
                and (optimize_steps % max(1, int(1.0 / float(reanalyze_frac)))) == 0
            ):
                n_reanalyzed = smz_reanalyzer.update_replay_with_reanalysis(replay, smz_net)
                if n_reanalyzed > 0:
                    append_agent_log(f"[SMZ][REANALYZE] step={optimize_steps} updated={n_reanalyzed}")
            append_agent_log(
                "[SMZ][UPDATE] "
                f"step={optimize_steps} policy_version={policy_version} "
                f"loss={float(update_info.get('loss', 0.0)):.6f} "
                f"policy_loss={float(update_info.get('policy_loss', 0.0)):.6f} "
                f"value_loss={float(update_info.get('value_loss', 0.0)):.6f} "
                f"reward_loss={float(update_info.get('reward_loss', 0.0)):.6f} replay={len(replay)}"
            )
            if optimize_steps - last_sync_opt_steps >= int(SMZ_SYNC_EVERY_UPDATES):
                _save_smz_sync()
                last_sync_opt_steps = int(optimize_steps)
            _maybe_train_progress_heartbeat()

    pbar.close()
    _save_smz_sync()
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
        last_checkpoint = _save_checkpoint(int(resume_episode_base + (episodes_finished or totLifeT)))
        append_agent_log(f"[SMZ][CHECKPOINT] final path={last_checkpoint}")

    if ep_rows:
        save_extra_metrics(
            run_id=run_id,
            ep_rows=ep_rows,
            metrics_dir=METRICS_DIR,
            write_legacy_gui_plots=False,
        )
        save_heuristic_metrics_snapshot(run_id=run_id, ep_rows=ep_rows, metrics_dir=METRICS_DIR)
        # Финальный снапшот метрик (окно тренировки) для надёжной привязки GUI к run_id.
        det_payload = _gmz_det_payload_from_rows(
            list(ep_rows)[-int(TRAIN_METRICS_WINDOW_EPISODES):],
            episode_idx=int(max(episodes_finished, 1)),
            train_loss=float(last_loss),
            eval_tag="train_window",
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
                metrics_mode="train_window",
                extra={
                    "algo": "sampled_muzero",
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
                metrics_mode="train_window",
                extra={"algo": "sampled_muzero", "mode": "actor_learner", "det_eval_note": "нет точек DET-eval"},
            )
        append_agent_log(f"[SMZ][METRICS] saved run_id={run_id}")
        _log_train_summary(ep_rows, time.perf_counter() - train_t0_summary)

    final_episode = int(resume_episode_base + episodes_finished)
    final_agent_id = build_agent_id(learner_identity, f"final_ep{final_episode}")
    save_agent_artifact(
        identity=learner_identity,
        agent_id=final_agent_id,
        env_contract=env_contract,
        policy_state_dict=normalize_state_dict(smz_net.state_dict()),
        target_state_dict={},
        optimizer_state_dict=optimizer.state_dict(),
        extra_meta={
            "algo": "sampled_muzero",
            "arch": sampled_muzero_kwargs_from_env(),
            "episode": int(final_episode),
            "source_model_path": str(last_checkpoint or ""),
            "mode": "actor_learner",
            "num_actors": int(SMZ_NUM_ACTORS),
            "policy_version": int(policy_version),
            "outcome_only": bool(SMZ_OUTCOME_ONLY),
            "outcome_value_win": float(SMZ_OUTCOME_VALUE_WIN),
            "outcome_value_loss": float(SMZ_OUTCOME_VALUE_LOSS),
            "outcome_value_draw": float(SMZ_OUTCOME_VALUE_DRAW),
        },
    )
    append_agent_log(
        "[SMZ][ACTOR_LEARNER] done "
        f"episodes={final_episode}/{resume_episode_base + int(totLifeT)} checkpoint={last_checkpoint} "
        f"global_step={global_step} updates={optimize_steps} replay={len(replay)}"
    )


if __name__ == "__main__":
    mp.freeze_support()
    main()
