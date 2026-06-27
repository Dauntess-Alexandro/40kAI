#!/usr/bin/env python
"""PC2: distributed AZ tree env workers (IS localhost + rollout PUSH → PC1 learner)."""

from __future__ import annotations

import json
import multiprocessing as mp
import os
import socket
import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from core.engine.agent_registry import make_env_contract, resolve_latest_opponent_agent_id  # noqa: E402
from core.engine.mission import normalize_mission_name  # noqa: E402
from core.models.az_rollout_sink import (  # noqa: E402
    apply_az_dist_worker_env,
    az_dist_stop_flag_path,
    az_dist_stop_requested,
    build_az_dist_worker_payloads,
    build_gaz_dist_worker_payloads,
    normalize_az_dist_hyperparams,
    read_az_dist_train_context,
    reconcile_dist_opponent,
    wait_az_dist_train_context,
)


def _is_gumbel_az(algo: str) -> bool:
    return str(algo or "").strip().lower() == "gumbel_az"


def _load_context_from_env() -> dict:
    raw = str(os.getenv("AZ_DIST_CONTEXT_JSON", "") or "").strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except (TypeError, json.JSONDecodeError):
        return {}


def _apply_context_env(ctx: dict | None, *, log=print) -> None:
    """ПК2: mission/ruleset из SMB-контекста ПК1 нужно выставить ДО import train."""
    src = ctx if isinstance(ctx, dict) else {}
    mission = str(src.get("mission") or (src.get("roster") or {}).get("mission") or "").strip()
    if mission:
        mission = normalize_mission_name(mission)
        os.environ["MISSION_NAME"] = mission
    ruleset = str(src.get("ruleset_version") or "").strip()
    if not ruleset and mission:
        ruleset = f"{mission}_v2"
    if ruleset:
        os.environ["RULESET_VERSION"] = ruleset
        os.environ["ENV_RULESET_VERSION"] = ruleset
    if mission or ruleset:
        log(f"[AZ][DIST][PC2] context env: mission={mission or '-'} ruleset={ruleset or '-'}")


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


def _pc1_receiver_reachable(host: str, port: int, timeout: float = 1.0) -> bool:
    """TCP-проба приёмника ПК1: жив ли learner и слушает ли :port."""
    try:
        with socket.create_connection((str(host), int(port)), timeout=float(timeout)):
            return True
    except OSError:
        return False


def wait_for_pc1_live(
    host: str,
    port: int,
    *,
    total_wait_sec: float,
    poll_sec: float = 2.0,
    should_stop=None,
    reachable=_pc1_receiver_reachable,
    log=print,
    sleep=time.sleep,
    now=time.monotonic,
) -> bool:
    """Ждём, пока приёмник ПК1 (host:port) станет доступен — чтобы актёры не спамили без ПК1.

    True  — ПК1 жив, можно спавнить актёров.
    False — запрошен stop или истёк total_wait_sec (тогда актёры НЕ запускаются — без спама).
    total_wait_sec<=0 — гейт выключен (старое поведение: сразу True).
    """
    if total_wait_sec <= 0:
        return True
    deadline = now() + float(total_wait_sec)
    # Залежавшийся stop.flag прошлого прогона не должен мгновенно глушить ожидание ПК1:
    # если флаг есть уже на входе в гейт — считаем его stale (свежий train на ПК1 его очистит
    # при старте) и игнорируем. Учитываем только stop, который ПОЯВИТСЯ во время ожидания
    # (живой stop текущего прогона). Иначе ПК2, запущенный раньше ПК1, выходит впустую.
    stale_stop_at_entry = bool(should_stop is not None and should_stop())
    if stale_stop_at_entry:
        log(
            "[AZ][DIST][PC2] на старте найден stop.flag прошлого прогона — игнорирую как stale, жду ПК1. "
            "Свежий train на ПК1 очистит флаг; чтобы не ждать — удалите stop.flag вручную."
        )
    while True:
        if reachable(host, port):
            return True
        if should_stop is not None and not stale_stop_at_entry and should_stop():
            log("[AZ][DIST][PC2] stop запрошен — актёры не запускаем (ПК1 не нужен).")
            return False
        if now() >= deadline:
            log(
                f"[AZ][DIST][PC2] ПК1 {host}:{port} не появился за {int(total_wait_sec)}с — "
                "выходим без запуска актёров (нет спама). Запустите train на ПК1 и перезапустите."
            )
            return False
        log(f"[AZ][DIST][PC2] ждём ПК1: приёмник {host}:{port} недоступен (осталось ~{int(deadline - now())}с)...")
        sleep(poll_sec)


def _train_dist_defaults(train_mod) -> dict:
    return {
        "simulations": int(train_mod.AZ_MCTS_SIMS),
        "c_puct": float(train_mod.AZ_C_PUCT),
        "c_puct_min": float(train_mod.AZ_C_PUCT_MIN),
        "c_puct_max": float(train_mod.AZ_C_PUCT_MAX),
        "c_puct_schedule": str(train_mod.AZ_C_PUCT_SCHEDULE),
        "dirichlet_alpha": float(train_mod.AZ_DIR_ALPHA),
        "dirichlet_eps": float(train_mod.AZ_DIR_EPS),
        "top_k_per_head": int(train_mod.AZ_MCTS_TOP_K_PER_HEAD),
        "max_depth": int(train_mod.AZ_MCTS_MAX_DEPTH),
        "mode": str(train_mod.AZ_MCTS_MODE),
        "root_dirichlet_only": bool(train_mod.AZ_MCTS_ROOT_DIRICHLET_ONLY),
        "eval_cache_size": int(train_mod.AZ_MCTS_EVAL_CACHE_SIZE),
        "pw_alpha": float(train_mod.AZ_PW_ALPHA),
        "pw_beta": float(train_mod.AZ_PW_BETA),
        "prior_weight_early": float(train_mod.AZ_PRIOR_WEIGHT_EARLY),
        "batch_eval_size": int(train_mod.AZ_MCTS_BATCH_EVAL_SIZE),
        "parallel_simulations": int(train_mod.AZ_MCTS_PARALLEL_SIMS),
        "simulate_enemy_in_tree": bool(train_mod.AZ_MCTS_SIMULATE_ENEMY),
        "candidate_mode": str(train_mod.AZ_MCTS_CANDIDATE_MODE),
        "window_nodes": bool(train_mod.AZ_MCTS_WINDOW_NODES),
        "joint_action_from_best_child": bool(train_mod.AZ_MCTS_JOINT_BEST_CHILD),
        "temperature_opening_moves": int(train_mod.AZ_TEMP_OPENING_MOVES),
        "temperature_opening_value": float(train_mod.AZ_TEMP_OPENING),
        "temperature_late_value": float(train_mod.AZ_TEMP_LATE),
        "outcome_only": bool(train_mod.AZ_OUTCOME_ONLY),
        "outcome_value_win": float(train_mod.AZ_OUTCOME_VALUE_WIN),
        "outcome_value_loss": float(train_mod.AZ_OUTCOME_VALUE_LOSS),
        "outcome_value_draw": float(train_mod.AZ_OUTCOME_VALUE_DRAW),
        "batch_send": int(train_mod.AZ_ACTOR_BATCH_SEND),
        "inference_timeout": float(train_mod.AZ_INFERENCE_TIMEOUT),
        "self_play_enabled": int(train_mod.SELF_PLAY_ENABLED),
    }


def _train_gaz_dist_defaults(train_mod) -> dict:
    """Дефолты GumbelAlphaZeroSearch на ПК2 (fallback, если в SMB нет полей с ПК1)."""
    return {
        "num_simulations": int(train_mod.GAZ_NUM_SIMS),
        "num_considered_actions": int(train_mod.GAZ_NUM_CONSIDERED),
        "max_depth": int(train_mod.GAZ_MAX_DEPTH),
        "value_scale": float(train_mod.GAZ_VALUE_SCALE),
        "c_visit": float(train_mod.GAZ_C_VISIT),
        "simulate_enemy": bool(train_mod.GAZ_SIMULATE_ENEMY),
        "joint_action": bool(train_mod.GAZ_JOINT_ACTION),
        "eval_cache_size": int(train_mod.GAZ_EVAL_CACHE_SIZE),
        "batch_eval_size": int(train_mod.GAZ_BATCH_EVAL_SIZE),
        "temperature_opening_moves": int(train_mod.AZ_TEMP_OPENING_MOVES),
        "temperature_opening_value": float(train_mod.AZ_TEMP_OPENING),
        "temperature_late_value": float(train_mod.AZ_TEMP_LATE),
        "outcome_only": bool(train_mod.AZ_OUTCOME_ONLY),
        "outcome_value_win": float(train_mod.AZ_OUTCOME_VALUE_WIN),
        "outcome_value_loss": float(train_mod.AZ_OUTCOME_VALUE_LOSS),
        "outcome_value_draw": float(train_mod.AZ_OUTCOME_VALUE_DRAW),
        "batch_send": int(train_mod.AZ_ACTOR_BATCH_SEND),
        "inference_timeout": float(train_mod.AZ_INFERENCE_TIMEOUT),
        "self_play_enabled": int(train_mod.SELF_PLAY_ENABLED),
    }


def _resolve_opponent_agent_id(ctx: dict | None = None) -> str:
    explicit = str(os.getenv("OPPONENT_AGENT_ID", "") or "").strip()
    if explicit:
        return explicit

    dist_ctx = ctx if isinstance(ctx, dict) else read_az_dist_train_context()
    agent_id = str(dist_ctx.get("opponent_agent_id", "") or "").strip()
    if agent_id:
        print(f"[AZ][DIST][PC2] opponent из train context (SMB): {agent_id}", flush=True)
        return agent_id

    learner_side = str(os.getenv("LEARNER_SIDE", "P1") or "P1").strip().upper() or "P1"
    if str(dist_ctx.get("learner_side", "")).strip():
        learner_side = str(dist_ctx.get("learner_side")).strip().upper()
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


def _load_opponent_spec(train_mod, roster_config: dict, b_len: int, b_hei: int):
    agent_id = _resolve_opponent_agent_id()
    if not agent_id:
        return None
    enemy, model = train_mod._build_units_from_config(roster_config, b_len, b_hei)
    mission_name = train_mod.normalize_mission_name(
        roster_config.get("mission", train_mod.DEFAULT_MISSION_NAME)
    )
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
    n_actions = train_mod.action_sizes_from_env(env, len(model))
    try:
        env.close()
    except Exception:
        pass
    contract = make_env_contract(
        n_observations=n_obs,
        n_actions=n_actions,
        mission_name=mission_name,
        ruleset_version=train_mod.RULESET_VERSION,
        extras={"distributed_actor": 1},
    )
    from core.models.opponent_adapter import load_agent_opponent

    return load_agent_opponent(agent_id=agent_id, expected_contract=contract)


def _worker_main(worker_id: int) -> None:
    dist_ctx = _load_context_from_env()
    _apply_context_env(dist_ctx)
    import train as train_mod

    hp_pc1: dict = {}
    raw_hp = str(os.getenv("AZ_DIST_HYPERPARAMS_JSON", "") or "").strip()
    if raw_hp:
        try:
            hp_pc1 = normalize_az_dist_hyperparams(json.loads(raw_hp))
        except (TypeError, json.JSONDecodeError):
            hp_pc1 = {}

    # train_algo берём из SMB-контекста ПК1 (main() кладёт в env). GAZ → GumbelAlphaZeroSearch.
    train_algo = str(os.getenv("AZ_DIST_TRAIN_ALGO", "") or "").strip().lower()
    gaz = _is_gumbel_az(train_algo)
    if gaz:
        payloads = build_gaz_dist_worker_payloads(hp_pc1, defaults=_train_gaz_dist_defaults(train_mod))
    else:
        payloads = build_az_dist_worker_payloads(hp_pc1, defaults=_train_dist_defaults(train_mod))
    apply_az_dist_worker_env(hp_pc1)
    mcts_payload = payloads["mcts"]
    sp_payload = payloads["sp"]
    outcome_payload = payloads["outcome"]

    roster = train_mod._roster_from_context(dist_ctx)
    if roster is not None:
        print("[AZ][DIST][PC2] ростер: из контекста ПК1 (SMB)", flush=True)
    else:
        roster = train_mod._load_roster_config()
        print(
            "[AZ][DIST][PC2][WARN] ростер: локальный runtime/state/data.json "
            "(в контексте нет снимка — старый ПК1?). Возможен env/contract mismatch.",
            flush=True,
        )
    b_len = int(roster["b_len"])
    b_hei = int(roster["b_hei"])
    opponent_spec = _load_opponent_spec(train_mod, roster, b_len, b_hei)

    hp = train_mod.AZ_CFG
    # Дефолтные порты GAZ (5565/5567) отличаются от AZ (5555/5557); их обычно задаёт bat,
    # но fallback по алго страхует от рассинхрона.
    is_host = str(os.getenv("AZ_DIST_PC2_IS_HOST", "127.0.0.1"))
    is_port = _env_int("AZ_DIST_PC2_IS_PORT", 5565 if gaz else 5555)
    rollout_host = str(os.getenv("AZ_DIST_PC1_HOST", "127.0.0.1"))
    rollout_port = _env_int("AZ_DIST_ROLLOUT_PORT", 5567 if gaz else 5557)
    auth = str(os.getenv("AZ_DIST_AUTH_TOKEN", os.getenv("AZ_INFERENCE_REMOTE_AUTH_TOKEN", "")))
    contract_hash = str(os.getenv("AZ_DIST_ENV_CONTRACT_HASH", ""))
    stop_flag = str(os.getenv("AZ_DIST_STOP_FLAG_PATH", "") or az_dist_stop_flag_path(train_algo))
    batch_send = int(payloads["batch_send"])

    train_mod._az_env_worker_entry(
        int(worker_id),
        0,
        roster,
        b_len,
        b_hei,
        batch_send,
        None,
        None,
        None,
        int(payloads["self_play_enabled"]),
        opponent_spec,
        sp_payload,
        mcts_payload,
        outcome_payload,
        float(payloads["inference_timeout"]),
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
    # Явный OPPONENT_AGENT_ID (конфиг/ENV) фиксируем ДО того, как ниже выставим его из контекста —
    # иначе reconcile не отличит «задано пользователем» от «взято из (возможно stale) контекста».
    explicit_opp = str(os.getenv("OPPONENT_AGENT_ID", "") or "").strip()
    wait_sec = max(0.0, _env_float("AZ_DIST_WAIT_CONTEXT_SEC", 0.0))
    dist_ctx = wait_az_dist_train_context(
        wait_sec=wait_sec,
        require_opponent=False,
        require_hyperparams=False,
    )
    _apply_context_env(dist_ctx)
    # train_algo из контекста ПК1 → выбор GumbelAlphaZeroSearch (gumbel_az) vs AZ MCTS.
    ctx_algo = str(dist_ctx.get("train_algo", "") or os.getenv("AZ_DIST_TRAIN_ALGO", "")).strip().lower()
    if ctx_algo:
        os.environ["AZ_DIST_TRAIN_ALGO"] = ctx_algo
    _gaz = _is_gumbel_az(ctx_algo)
    _tag = "GAZ" if _gaz else "AZ"
    hp_pc1 = normalize_az_dist_hyperparams(dist_ctx.get("az_hyperparams"))
    if hp_pc1:
        os.environ["AZ_DIST_HYPERPARAMS_JSON"] = json.dumps(hp_pc1, ensure_ascii=False)
        if _gaz:
            print(
                f"[{_tag}][DIST][PC2] hyperparams с ПК1 (SMB): "
                f"num_simulations={hp_pc1.get('num_simulations')} "
                f"num_considered={hp_pc1.get('num_considered_actions')} "
                f"joint_action={hp_pc1.get('joint_action')}",
                flush=True,
            )
        else:
            print(
                f"[{_tag}][DIST][PC2] hyperparams с ПК1 (SMB): "
                f"parallel_sims={hp_pc1.get('mcts_parallel_sims')} "
                f"mcts_sims={hp_pc1.get('mcts_simulations')} "
                f"max_depth={hp_pc1.get('mcts_max_depth')}",
                flush=True,
            )
    elif wait_sec > 0:
        print(
            "[AZ][DIST][PC2][WARN] az_hyperparams в SMB нет — MCTS из локального hyperparams.json на ПК2. "
            "Где: az_dist_train_context.json. Что делать: сначала запустите train на ПК1.",
            flush=True,
        )

    num_workers = max(1, _env_int("AZ_DIST_PC2_NUM_WORKERS", 8))
    worker_id_base = max(0, _env_int("AZ_DIST_PC2_WORKER_ID_BASE", 100))
    opp_id = _resolve_opponent_agent_id(dist_ctx)
    if opp_id:
        os.environ["OPPONENT_AGENT_ID"] = opp_id
    # Единый резолвер (40KAI_SHARE_ROOT → 40KAI_MODELS_DIR → MODELS_DIR → локально).
    from project_paths import resolve_share_models_root

    models_dir = resolve_share_models_root()
    os.environ.setdefault("MODELS_DIR", models_dir)
    os.environ.setdefault("40KAI_MODELS_DIR", models_dir)
    from core.engine.agent_registry import agents_meta_root

    print(
        f"[AZ][DIST][PC2] MODELS_DIR={models_dir or '(local artifacts/models)'} agents={agents_meta_root()}",
        flush=True,
    )

    # Гейт «ждём живого ПК1»: без работающего learner'а (приёмник :5557) актёры не
    # запускаем — иначе они крутят партии впустую (роллауты летят в мёртвый порт и
    # дропаются). Проба досягаемости приёмника ПК1. Выключить: AZ_DIST_WAIT_PC1_SEC=0.
    rollout_host = str(os.getenv("AZ_DIST_PC1_HOST", "127.0.0.1"))
    rollout_port = _env_int("AZ_DIST_ROLLOUT_PORT", 5567 if _gaz else 5557)
    stop_flag = str(os.getenv("AZ_DIST_STOP_FLAG_PATH", "") or az_dist_stop_flag_path(ctx_algo))
    wait_pc1_sec = _env_float("AZ_DIST_WAIT_PC1_SEC", 600.0)
    if not wait_for_pc1_live(
        rollout_host,
        rollout_port,
        total_wait_sec=wait_pc1_sec,
        should_stop=lambda: az_dist_stop_requested(stop_flag),
    ):
        print(f"[{_tag}][DIST][PC2] ПК1 не обнаружен — актёры не запущены (без спама).", flush=True)
        return 0

    # ПК1 жив → он уже записал СВЕЖИЙ контекст (train.py пишет az_dist_train_context.json ДО
    # открытия приёмника). Лечим возможный stale-оппонент: ПК2 мог стартовать раньше ПК1 и
    # прочитать оппонента прошлого прогона. Перечитываем и согласуем (см. reconcile_dist_opponent).
    fresh_ctx = read_az_dist_train_context()
    _apply_context_env(fresh_ctx)
    opp_id, opp_warn = reconcile_dist_opponent(
        opp_id, fresh_ctx, explicit_opp=explicit_opp
    )
    if opp_warn:
        print(f"[{_tag}][DIST][PC2][WARN] {opp_warn}", flush=True)
    if opp_id:
        os.environ["OPPONENT_AGENT_ID"] = opp_id
    ctx_for_workers = fresh_ctx if fresh_ctx else dist_ctx
    os.environ["AZ_DIST_CONTEXT_JSON"] = json.dumps(ctx_for_workers, ensure_ascii=False)
    ctx_hash = str((ctx_for_workers or {}).get("env_contract_hash", "") or "").strip()
    if ctx_hash:
        os.environ["AZ_DIST_ENV_CONTRACT_HASH"] = ctx_hash
    print(
        f"[{_tag}][DIST][PC2] оппонент подтверждён после подъёма ПК1: {opp_id or '(эвристика)'}",
        flush=True,
    )

    print(
        f"[{_tag}][DIST][PC2] spawning workers={num_workers} id_base={worker_id_base} "
        f"rollout_target={rollout_host}:{rollout_port} "
        f"is=127.0.0.1:{_env_int('AZ_DIST_PC2_IS_PORT', 5565 if _gaz else 5555)}",
        flush=True,
    )

    ctx = mp.get_context("spawn")
    procs = []
    for i in range(num_workers):
        wid = worker_id_base + i
        p = ctx.Process(target=_worker_main, args=(int(wid),), daemon=False)
        p.start()
        procs.append(p)

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
