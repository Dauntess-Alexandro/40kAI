"""PHOENIX config: dataclass + резолв env(PHOENIX_*) → hyperparams[phoenix] → default."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class PhoenixConfig:
    # расписания / BBF
    replay_ratio: int = 2
    reset_interval: int = 40000
    anneal_steps: int = 10000
    shrink_alpha: float = 0.5
    nstep_start: int = 10
    nstep_end: int = 3
    gamma_start: float = 0.97
    gamma_end: float = 0.99
    target_ema_rl: float = 0.005
    target_ema_spr: float = 0.01
    replay_capacity: int = 200000
    batch_size: int = 32
    replay_min_size: int = 256
    # actor-learner / distributed runtime
    num_actors: int = 1
    actor_batch_send: int = 32
    actor_queue_max: int = 256
    sync_every_updates: int = 200
    actor_epsilon_mode: str = "apex"
    actor_eps_floor_min: float = 0.02
    actor_eps_floor_max: float = 0.20
    distributed_actors_enabled: bool = False
    distributed_rollout_port: int = 5562
    distributed_bind_host: str = "0.0.0.0"
    distributed_auth_token: str = ""
    distributed_local_episode_fraction: float = 0.7
    distributed_pc2_num_workers: int = 8
    distributed_actors_drain_sec: float = 30.0
    distributed_wait_pc2: bool = False
    distributed_wait_pc2_timeout_sec: float = 600.0
    distributed_bind_retry_sec: float = 25.0
    dist_zmq_hwm: int = 256
    dist_max_windows_per_msg: int = 64
    # SPR / value-expansion
    spr_horizon_K: int = 5
    spr_coef: float = 2.0
    ve_horizon: int = 3
    ve_steve: bool = False
    ve_latent_bootstrap: bool = False
    iqn_kappa: float = 1.0
    # сеть
    dynamics_type: str = "mlp"
    emb_dim: int = 64
    noisy: bool = False
    dueling: bool = False
    hidden_size: int = 256
    num_layers: int = 2
    n_ensemble: int = 1
    iqn_num_quantiles: int = 32
    iqn_num_target_quantiles: int = 32
    iqn_num_tau_samples: int = 32
    iqn_embed_dim: int = 64

    @property
    def window_horizon(self) -> int:
        """H = max(spr_horizon_K, ve_horizon); окно replay = H+1 шагов."""
        return max(int(self.spr_horizon_K), int(self.ve_horizon))


def _as_bool(value, default: bool) -> bool:
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def resolve_phoenix_config(hp: dict | None, env: Mapping[str, str] | None = None) -> PhoenixConfig:
    section = {}
    if isinstance(hp, dict):
        sec = hp.get("phoenix")
        if isinstance(sec, dict):
            section = sec
    env = env if env is not None else {}
    d = PhoenixConfig()

    def _env_value(*env_keys: str):
        for env_key in env_keys:
            if env_key in env and str(env[env_key]).strip() != "":
                return env[env_key]
        return None

    def pick_int(env_key: str | tuple[str, ...], sec_key: str, default: int) -> int:
        keys = (env_key,) if isinstance(env_key, str) else tuple(env_key)
        raw = _env_value(*keys)
        if raw is not None:
            try:
                return int(raw)
            except (TypeError, ValueError):
                pass
        if sec_key in section:
            try:
                return int(section[sec_key])
            except (TypeError, ValueError):
                pass
        return default

    def pick_float(env_key: str | tuple[str, ...], sec_key: str, default: float) -> float:
        keys = (env_key,) if isinstance(env_key, str) else tuple(env_key)
        raw = _env_value(*keys)
        if raw is not None:
            try:
                return float(raw)
            except (TypeError, ValueError):
                pass
        if sec_key in section:
            try:
                return float(section[sec_key])
            except (TypeError, ValueError):
                pass
        return default

    def pick_bool(env_key: str | tuple[str, ...], sec_key: str, default: bool) -> bool:
        keys = (env_key,) if isinstance(env_key, str) else tuple(env_key)
        raw = _env_value(*keys)
        if raw is not None:
            return _as_bool(raw, default)
        if sec_key in section:
            return _as_bool(section[sec_key], default)
        return default

    def pick_str(env_key: str | tuple[str, ...], sec_key: str, default: str, *, lower: bool = True) -> str:
        keys = (env_key,) if isinstance(env_key, str) else tuple(env_key)
        raw = _env_value(*keys)
        if raw is not None:
            text = str(raw).strip()
            return text.lower() if lower else text
        if sec_key in section and str(section[sec_key]).strip() != "":
            text = str(section[sec_key]).strip()
            return text.lower() if lower else text
        return default

    return PhoenixConfig(
        replay_ratio=pick_int("PHOENIX_REPLAY_RATIO", "replay_ratio", d.replay_ratio),
        reset_interval=pick_int("PHOENIX_RESET_INTERVAL", "reset_interval", d.reset_interval),
        anneal_steps=pick_int("PHOENIX_ANNEAL_STEPS", "anneal_steps", d.anneal_steps),
        shrink_alpha=pick_float("PHOENIX_SHRINK_ALPHA", "shrink_alpha", d.shrink_alpha),
        nstep_start=pick_int("PHOENIX_NSTEP_START", "nstep_start", d.nstep_start),
        nstep_end=pick_int("PHOENIX_NSTEP_END", "nstep_end", d.nstep_end),
        gamma_start=pick_float("PHOENIX_GAMMA_START", "gamma_start", d.gamma_start),
        gamma_end=pick_float("PHOENIX_GAMMA_END", "gamma_end", d.gamma_end),
        target_ema_rl=pick_float("PHOENIX_TARGET_EMA_RL", "target_ema_rl", d.target_ema_rl),
        target_ema_spr=pick_float("PHOENIX_TARGET_EMA_SPR", "target_ema_spr", d.target_ema_spr),
        replay_capacity=pick_int("PHOENIX_REPLAY_CAPACITY", "replay_capacity", d.replay_capacity),
        batch_size=pick_int("PHOENIX_BATCH", "batch_size", d.batch_size),
        replay_min_size=pick_int("PHOENIX_MIN_REPLAY", "replay_min_size", d.replay_min_size),
        num_actors=pick_int(("PHOENIX_NUM_ACTORS", "NUM_ACTORS"), "num_actors", d.num_actors),
        actor_batch_send=pick_int("PHOENIX_ACTOR_BATCH_SEND", "actor_batch_send", d.actor_batch_send),
        actor_queue_max=pick_int("PHOENIX_ACTOR_QUEUE_MAX", "actor_queue_max", d.actor_queue_max),
        sync_every_updates=pick_int("PHOENIX_SYNC_EVERY_UPDATES", "sync_every_updates", d.sync_every_updates),
        actor_epsilon_mode=pick_str("PHOENIX_ACTOR_EPS_MODE", "actor_epsilon_mode", d.actor_epsilon_mode),
        actor_eps_floor_min=pick_float("PHOENIX_ACTOR_EPS_FLOOR_MIN", "actor_eps_floor_min", d.actor_eps_floor_min),
        actor_eps_floor_max=pick_float("PHOENIX_ACTOR_EPS_FLOOR_MAX", "actor_eps_floor_max", d.actor_eps_floor_max),
        distributed_actors_enabled=pick_bool(
            "PHOENIX_DISTRIBUTED_ACTORS", "distributed_actors_enabled", d.distributed_actors_enabled
        ),
        distributed_rollout_port=pick_int(
            "PHOENIX_DIST_ROLLOUT_PORT", "distributed_rollout_port", d.distributed_rollout_port
        ),
        distributed_bind_host=pick_str(
            "PHOENIX_DIST_BIND_HOST", "distributed_bind_host", d.distributed_bind_host, lower=False
        ),
        distributed_auth_token=pick_str(
            "PHOENIX_DIST_AUTH_TOKEN", "distributed_auth_token", d.distributed_auth_token, lower=False
        ),
        distributed_local_episode_fraction=pick_float(
            "PHOENIX_DIST_LOCAL_EPISODE_FRACTION",
            "distributed_local_episode_fraction",
            d.distributed_local_episode_fraction,
        ),
        distributed_pc2_num_workers=pick_int(
            "PHOENIX_DIST_PC2_NUM_WORKERS", "distributed_pc2_num_workers", d.distributed_pc2_num_workers
        ),
        distributed_actors_drain_sec=pick_float(
            "PHOENIX_DIST_DRAIN_SEC", "distributed_actors_drain_sec", d.distributed_actors_drain_sec
        ),
        distributed_wait_pc2=pick_bool("PHOENIX_DIST_WAIT_PC2", "distributed_wait_pc2", d.distributed_wait_pc2),
        distributed_wait_pc2_timeout_sec=pick_float(
            "PHOENIX_DIST_WAIT_PC2_TIMEOUT_SEC",
            "distributed_wait_pc2_timeout_sec",
            d.distributed_wait_pc2_timeout_sec,
        ),
        distributed_bind_retry_sec=pick_float(
            "PHOENIX_DIST_BIND_RETRY_SEC", "distributed_bind_retry_sec", d.distributed_bind_retry_sec
        ),
        dist_zmq_hwm=pick_int("PHOENIX_DIST_ZMQ_HWM", "dist_zmq_hwm", d.dist_zmq_hwm),
        dist_max_windows_per_msg=pick_int(
            "PHOENIX_DIST_MAX_WINDOWS_PER_MSG", "dist_max_windows_per_msg", d.dist_max_windows_per_msg
        ),
        spr_horizon_K=pick_int("PHOENIX_SPR_HORIZON_K", "spr_horizon_K", d.spr_horizon_K),
        spr_coef=pick_float("PHOENIX_SPR_COEF", "spr_coef", d.spr_coef),
        ve_horizon=pick_int("PHOENIX_VE_HORIZON", "ve_horizon", d.ve_horizon),
        ve_steve=pick_bool("PHOENIX_VE_STEVE", "ve_steve", d.ve_steve),
        ve_latent_bootstrap=pick_bool(
            "PHOENIX_VE_LATENT_BOOTSTRAP", "ve_latent_bootstrap", d.ve_latent_bootstrap
        ),
        iqn_kappa=pick_float("PHOENIX_IQN_KAPPA", "iqn_kappa", d.iqn_kappa),
        dynamics_type=pick_str("PHOENIX_DYNAMICS_TYPE", "dynamics_type", d.dynamics_type),
        emb_dim=pick_int("PHOENIX_EMB_DIM", "emb_dim", d.emb_dim),
        noisy=pick_bool("PHOENIX_NOISY", "noisy", d.noisy),
        dueling=pick_bool("PHOENIX_DUELING", "dueling", d.dueling),
        hidden_size=pick_int("PHOENIX_HIDDEN_SIZE", "hidden_size", d.hidden_size),
        num_layers=pick_int("PHOENIX_NUM_LAYERS", "num_layers", d.num_layers),
        n_ensemble=pick_int("PHOENIX_ENSEMBLE_SIZE", "n_ensemble", d.n_ensemble),
        iqn_num_quantiles=pick_int("IQN_N_QUANTILES", "iqn_num_quantiles", d.iqn_num_quantiles),
        iqn_num_target_quantiles=pick_int(
            "IQN_N_TARGET_QUANTILES", "iqn_num_target_quantiles", d.iqn_num_target_quantiles
        ),
        iqn_num_tau_samples=pick_int("IQN_N_TAU_SAMPLES", "iqn_num_tau_samples", d.iqn_num_tau_samples),
        iqn_embed_dim=pick_int("IQN_EMBED_DIM", "iqn_embed_dim", d.iqn_embed_dim),
    )
