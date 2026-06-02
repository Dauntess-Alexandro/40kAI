#!/usr/bin/env python
"""PC2: distributed AZ tree env workers (IS localhost + rollout PUSH → PC1 learner)."""

from __future__ import annotations

import multiprocessing as mp
import os
import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# train импортируется после path setup
import train  # noqa: E402
from core.engine.agent_registry import make_env_contract, resolve_latest_opponent_agent_id  # noqa: E402
from core.models.opponent_adapter import load_agent_opponent  # noqa: E402
from core.models.az_rollout_sink import (  # noqa: E402
    az_dist_stop_flag_path,
    az_dist_stop_requested,
    read_az_dist_train_context,
)


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return int(default)


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except Exception:
        return float(default)


def _resolve_opponent_agent_id() -> str:
    explicit = str(os.getenv("OPPONENT_AGENT_ID", "") or "").strip()
    if explicit:
        return explicit

    wait_sec = max(0.0, _env_float("AZ_DIST_WAIT_CONTEXT_SEC", 0.0))
    deadline = time.monotonic() + wait_sec if wait_sec > 0 else 0.0
    while True:
        ctx = read_az_dist_train_context()
        agent_id = str(ctx.get("opponent_agent_id", "") or "").strip()
        if agent_id:
            print(f"[AZ][DIST][PC2] opponent из train context (SMB): {agent_id}", flush=True)
            return agent_id
        if wait_sec <= 0 or time.monotonic() >= deadline:
            break
        print(
            "[AZ][DIST][PC2] ждём az_dist_train_context.json с ПК1 "
            f"(осталось ~{max(0, int(deadline - time.monotonic()))} с)...",
            flush=True,
        )
        time.sleep(2.0)

    learner_side = str(os.getenv("LEARNER_SIDE", "P1") or "P1").strip().upper() or "P1"
    ctx = read_az_dist_train_context()
    if str(ctx.get("learner_side", "")).strip():
        learner_side = str(ctx.get("learner_side")).strip().upper()
    agent_id = resolve_latest_opponent_agent_id(learner_side=learner_side)
    if agent_id:
        print(f"[AZ][DIST][PC2] opponent auto (latest_snapshot / SMB agents): {agent_id}", flush=True)
        return agent_id
    print(
        "[AZ][DIST][PC2][WARN] OPPONENT_AGENT_ID не найден — эвристический оппонент. "
        "Где: pc2_az_actors._resolve_opponent_agent_id. "
        "Что делать: запустите train на ПК1 (пишет az_dist_train_context.json) или задайте OPPONENT_AGENT_ID в конфиге.",
        flush=True,
    )
    return ""


def _load_opponent_spec(roster_config: dict, b_len: int, b_hei: int):
    agent_id = _resolve_opponent_agent_id()
    if not agent_id:
        return None
    enemy, model = train._build_units_from_config(roster_config, b_len, b_hei)
    mission_name = train.normalize_mission_name(roster_config.get("mission", train.DEFAULT_MISSION_NAME))
    import gymnasium as gym

    env = gym.make(
        "40kAI-v0",
        disable_env_checker=True,
        enemy=enemy,
        model=model,
        b_len=b_len,
        b_hei=b_hei,
    )
    state0, _ = env.reset(options={"m": model, "e": enemy, "trunc": True})
    if hasattr(state0, "values"):
        n_obs = len(list(state0.values()))
    else:
        n_obs = int(__import__("numpy").array(state0).shape[0])
    n_actions = train.action_sizes_from_env(env, len(model))
    try:
        env.close()
    except Exception:
        pass
    contract = make_env_contract(
        n_observations=n_obs,
        n_actions=n_actions,
        mission_name=mission_name,
        ruleset_version=train.RULESET_VERSION,
        extras={"distributed_actor": 1},
    )
    return load_agent_opponent(agent_id=agent_id, expected_contract=contract)


def _worker_main(worker_id: int) -> None:
    roster = train._load_roster_config()
    b_len = int(roster["b_len"])
    b_hei = int(roster["b_hei"])
    opponent_spec = _load_opponent_spec(roster, b_len, b_hei)

    hp = train.AZ_CFG
    mcts_payload = {
        "simulations": train.AZ_MCTS_SIMS,
        "c_puct": train.AZ_C_PUCT,
        "dirichlet_alpha": train.AZ_DIR_ALPHA,
        "dirichlet_eps": train.AZ_DIR_EPS,
        "top_k_per_head": train.AZ_MCTS_TOP_K_PER_HEAD,
        "max_depth": train.AZ_MCTS_MAX_DEPTH,
        "mode": train.AZ_MCTS_MODE,
        "root_dirichlet_only": train.AZ_MCTS_ROOT_DIRICHLET_ONLY,
        "eval_cache_size": train.AZ_MCTS_EVAL_CACHE_SIZE,
        "c_puct_min": train.AZ_C_PUCT_MIN,
        "c_puct_max": train.AZ_C_PUCT_MAX,
        "c_puct_schedule": train.AZ_C_PUCT_SCHEDULE,
        "pw_alpha": train.AZ_PW_ALPHA,
        "pw_beta": train.AZ_PW_BETA,
        "prior_weight_early": train.AZ_PRIOR_WEIGHT_EARLY,
        "batch_eval_size": train.AZ_MCTS_BATCH_EVAL_SIZE,
        "parallel_simulations": train.AZ_MCTS_PARALLEL_SIMS,
        "simulate_enemy_in_tree": train.AZ_MCTS_SIMULATE_ENEMY,
    }
    sp_payload = {
        "temperature_opening_moves": train.AZ_TEMP_OPENING_MOVES,
        "temperature_opening_value": train.AZ_TEMP_OPENING,
        "temperature_late_value": train.AZ_TEMP_LATE,
    }
    outcome_payload = {
        "outcome_only": train.AZ_OUTCOME_ONLY,
        "outcome_value_win": train.AZ_OUTCOME_VALUE_WIN,
        "outcome_value_loss": train.AZ_OUTCOME_VALUE_LOSS,
        "outcome_value_draw": train.AZ_OUTCOME_VALUE_DRAW,
        "policy_version": 0,
    }

    is_host = str(os.getenv("AZ_DIST_PC2_IS_HOST", "127.0.0.1"))
    is_port = _env_int("AZ_DIST_PC2_IS_PORT", 5555)
    rollout_host = str(os.getenv("AZ_DIST_PC1_HOST", "127.0.0.1"))
    rollout_port = _env_int("AZ_DIST_ROLLOUT_PORT", 5557)
    auth = str(os.getenv("AZ_DIST_AUTH_TOKEN", os.getenv("AZ_INFERENCE_REMOTE_AUTH_TOKEN", "")))
    contract_hash = str(os.getenv("AZ_DIST_ENV_CONTRACT_HASH", ""))
    stop_flag = str(os.getenv("AZ_DIST_STOP_FLAG_PATH", "") or az_dist_stop_flag_path())
    batch_send = _env_int("AZ_ACTOR_BATCH_SEND", int(hp.get("actor_batch_send", 32)))

    train._az_env_worker_entry(
        int(worker_id),
        0,
        roster,
        b_len,
        b_hei,
        batch_send,
        None,
        None,
        None,
        int(1 if train.SELF_PLAY_ENABLED else 0),
        opponent_spec,
        sp_payload,
        mcts_payload,
        outcome_payload,
        float(train.AZ_INFERENCE_TIMEOUT),
        "remote",
        is_host,
        is_port,
        str(os.getenv("AZ_INFERENCE_REMOTE_AUTH_TOKEN", hp.get("inference_remote_auth_token", ""))),
        "remote",
        "remote",
        rollout_host,
        rollout_port,
        auth,
        contract_hash,
        stop_flag,
    )


def main() -> int:
    num_workers = max(1, _env_int("AZ_DIST_PC2_NUM_WORKERS", 4))
    worker_id_base = max(0, _env_int("AZ_DIST_PC2_WORKER_ID_BASE", 100))
    opp_id = _resolve_opponent_agent_id()
    if opp_id:
        os.environ["OPPONENT_AGENT_ID"] = opp_id

    print(
        f"[AZ][DIST][PC2] spawning workers={num_workers} id_base={worker_id_base} "
        f"rollout_target={os.getenv('AZ_DIST_PC1_HOST', '127.0.0.1')}:{_env_int('AZ_DIST_ROLLOUT_PORT', 5557)} "
        f"is=127.0.0.1:{_env_int('AZ_DIST_PC2_IS_PORT', 5555)}",
        flush=True,
    )

    ctx = mp.get_context("spawn")
    procs = []
    for i in range(num_workers):
        wid = worker_id_base + i
        p = ctx.Process(target=_worker_main, args=(int(wid),), daemon=False)
        p.start()
        procs.append(p)

    stop_flag = str(os.getenv("AZ_DIST_STOP_FLAG_PATH", "") or az_dist_stop_flag_path())
    try:
        while True:
            if az_dist_stop_requested(stop_flag):
                print(f"[AZ][DIST][PC2] stop.flag detected ({stop_flag}), завершаем воркеры...", flush=True)
                break
            alive = sum(1 for p in procs if p.is_alive())
            if alive == 0:
                print("[AZ][DIST][PC2] все воркеры завершились.", flush=True)
                break
            time.sleep(2.0)
    finally:
        for p in procs:
            if p.is_alive():
                p.join(timeout=5.0)
            if p.is_alive():
                p.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
