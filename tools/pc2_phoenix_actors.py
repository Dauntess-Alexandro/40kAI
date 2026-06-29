#!/usr/bin/env python
"""ПК2: distributed PHOENIX actors (sequence windows PUSH -> ПК1 learner)."""

from __future__ import annotations

import multiprocessing as mp
import os
import sys
import time
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from core.models.az_rollout_sink import make_rollout_sink  # noqa: E402
from core.models.dqn_dist import derive_host_from_unc, pc2_dist_should_exit  # noqa: E402
from core.models.phoenix_dist import (  # noqa: E402
    PHOENIX_SYNC_WEIGHTS_NAME,
    PhoenixRemoteDataQ,
    phoenix_dist_stop_flag_path,
    phoenix_dist_stop_requested,
    resolve_phoenix_dist_contract_hash,
    split_count_among_workers,
    wait_phoenix_dist_train_context,
)


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return int(default)


def _apply_context_env(ctx: dict | None, *, log=print) -> None:
    src = ctx if isinstance(ctx, dict) else {}
    mission = str(src.get("mission") or (src.get("roster") or {}).get("mission") or "").strip()
    if mission:
        from core.engine.mission import normalize_mission_name

        mission = normalize_mission_name(mission)
        os.environ["MISSION_NAME"] = mission
    ruleset = str(src.get("ruleset_version") or "").strip()
    if not ruleset and mission:
        ruleset = f"{mission}_v2"
    if ruleset:
        os.environ["RULESET_VERSION"] = ruleset
        os.environ["ENV_RULESET_VERSION"] = ruleset
    if mission or ruleset:
        log(f"[PHOENIX][DIST][PC2] context env: mission={mission or '-'} ruleset={ruleset or '-'}")


def _start_pc2_telemetry_thread() -> None:
    import threading

    def _loop() -> None:
        from core.telemetry.pc2_telemetry import sample_system_telemetry, write_pc2_telemetry
        from project_paths import share_actor_sync_dir

        path = os.path.join(share_actor_sync_dir(), "pc2_telemetry.json")
        period = max(1.0, float(os.getenv("PC2_TELEMETRY_PERIOD_SEC", "3") or 3))
        while not phoenix_dist_stop_requested():
            try:
                write_pc2_telemetry(path, sample_system_telemetry())
            except Exception:
                pass
            time.sleep(period)

    threading.Thread(target=_loop, name="pc2-phoenix-telemetry", daemon=True).start()
    print("[PHOENIX][DIST][PC2] телеметрия ПК2 -> actor_sync/pc2_telemetry.json", flush=True)


def _worker_main(worker_id: int, ctx_json: str, episodes: int) -> None:
    import json

    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    try:
        ctx = json.loads(ctx_json) if ctx_json else {}
    except Exception:
        ctx = {}
    _apply_context_env(ctx)

    import gymnasium as gym
    import numpy as np
    import torch

    import train as train_mod
    from core.engine.agent_registry import make_env_contract
    from core.models.opponent_adapter import load_agent_opponent
    from core.models.phoenix_config import resolve_phoenix_config
    from core.models.phoenix_model import PhoenixNet

    roster = train_mod._roster_from_context(ctx)
    if roster is not None:
        print("[PHOENIX][DIST][PC2] ростер: из контекста ПК1 (SMB)", flush=True)
    else:
        roster = train_mod._load_roster_config()
        print(
            "[PHOENIX][DIST][PC2][WARN] ростер: локальный runtime/state/data.json "
            "(в контексте нет снимка). Возможен contract_hash mismatch.",
            flush=True,
        )
    b_len = int(roster["b_len"])
    b_hei = int(roster["b_hei"])
    enemy, model = train_mod._build_units_from_config(roster, b_len, b_hei)
    env0 = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
    state0, _ = env0.reset(options={"m": model, "e": enemy, "Type": "big", "trunc": True})
    n_observations = len(list(state0.values())) if hasattr(state0, "values") else int(np.asarray(state0).shape[0])
    n_actions = train_mod.action_sizes_from_env(env0, len(model))
    try:
        env0.close()
    except Exception:
        pass

    cfg = resolve_phoenix_config({"phoenix": ctx.get("phoenix_config", {})}, os.environ)
    from project_paths import share_actor_sync_dir

    sync_path = os.path.join(share_actor_sync_dir(), PHOENIX_SYNC_WEIGHTS_NAME)
    init_weights = {}
    if os.path.isfile(sync_path):
        try:
            payload = torch.load(sync_path, map_location="cpu", weights_only=False)
            sd = payload.get("state_dict") if isinstance(payload, dict) else None
            if isinstance(sd, dict):
                init_weights = train_mod.normalize_state_dict(sd)
        except Exception as exc:
            print(f"[PHOENIX][DIST][PC2][WARN] не удалось прочитать веса {sync_path}: {exc}", flush=True)
    if not init_weights:
        tmp_net = PhoenixNet(n_observations, list(n_actions), cfg)
        init_weights = {k: v.detach().cpu().clone() for k, v in train_mod.normalize_state_dict(tmp_net.state_dict()).items()}

    mission_name = train_mod.normalize_mission_name(roster.get("mission", train_mod.DEFAULT_MISSION_NAME))
    num_local_actors = max(1, int(ctx.get("num_local_actors", 1) or 1))
    extras = train_mod.phoenix_dist_env_contract_extras(num_local_actors=num_local_actors)
    env_contract = make_env_contract(
        n_observations=n_observations,
        n_actions=list(n_actions),
        mission_name=mission_name,
        ruleset_version=train_mod.RULESET_VERSION,
        extras=extras,
    )
    contract_hash = resolve_phoenix_dist_contract_hash(
        ctx=ctx,
        n_observations=n_observations,
        n_actions=list(n_actions),
        mission_name=mission_name,
        ruleset_version=train_mod.RULESET_VERSION,
        num_local_actors=num_local_actors,
    )
    if contract_hash and contract_hash != str(env_contract.get("contract_hash", "") or ""):
        print(
            f"[PHOENIX][DIST][PC2][WARN] contract_hash из контекста ({contract_hash}) "
            f"!= локальный пересчёт ({env_contract.get('contract_hash', '')}). Используем хэш ПК1 для sink.",
            flush=True,
        )

    opponent_spec = None
    self_play_enabled = int(_env_int("SELF_PLAY_ENABLED", 0))
    opp_id = str(os.getenv("OPPONENT_AGENT_ID", "") or str(ctx.get("opponent_agent_id", "") or "")).strip()
    if self_play_enabled and opp_id:
        try:
            opponent_spec = load_agent_opponent(agent_id=opp_id, expected_contract=env_contract)
        except Exception as exc:
            print(f"[PHOENIX][DIST][PC2][WARN] opponent {opp_id} не загружен: {exc}", flush=True)

    host = str(os.getenv("PHOENIX_DIST_PC1_HOST", "127.0.0.1"))
    port = _env_int("PHOENIX_DIST_ROLLOUT_PORT", int(ctx.get("rollout_port", 5562) or 5562))
    auth = str(os.getenv("PHOENIX_DIST_AUTH_TOKEN", str(ctx.get("auth_token", "") or "")))
    episodes = max(0, int(episodes))
    if episodes <= 0:
        print(f"[PHOENIX][DIST][PC2] worker={worker_id} episodes=0 — пропуск", flush=True)
        return

    sink = make_rollout_sink(
        mode="remote",
        source="remote",
        remote_host=host,
        remote_port=port,
        auth_token=auth,
        worker_id=int(worker_id),
        env_contract_hash=contract_hash,
        zmq_hwm=int(ctx.get("zmq_hwm", _env_int("PHOENIX_DIST_ZMQ_HWM", 256))),
    )
    remote_q = PhoenixRemoteDataQ(sink)
    print(
        f"[PHOENIX][DIST][PC2] worker={worker_id} -> {host}:{port} "
        f"contract_hash={contract_hash} episodes={episodes} self_play={self_play_enabled}",
        flush=True,
    )
    try:
        train_mod._phoenix_actor_entry(
            int(worker_id),
            int(episodes),
            roster,
            int(b_len),
            int(b_hei),
            int(n_observations),
            list(n_actions),
            cfg,
            init_weights,
            min(int(getattr(cfg, "actor_batch_send", 32)), int(getattr(cfg, "dist_max_windows_per_msg", 64))),
            0.0,
            0.0,
            False,
            remote_q,
            opponent_spec,
            float(os.getenv("SELF_PLAY_OPPONENT_EPSILON", "0.1") or 0.1),
            int(self_play_enabled),
            dict(env_contract),
            int(num_local_actors + _env_int("PHOENIX_DIST_PC2_NUM_WORKERS", int(ctx.get("pc2_num_workers", 8) or 8))),
        )
    finally:
        remote_q.close()


def main() -> int:
    import json

    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    wait_sec = max(0.0, float(os.getenv("PHOENIX_DIST_WAIT_CONTEXT_SEC", "0") or 0.0))
    ctx = wait_phoenix_dist_train_context(wait_sec=wait_sec)
    if ctx.get("opponent_agent_id"):
        os.environ.setdefault("OPPONENT_AGENT_ID", str(ctx["opponent_agent_id"]))

    from project_paths import resolve_share_models_root

    share_root = resolve_share_models_root()
    os.environ.setdefault("MODELS_DIR", share_root)
    host = str(os.getenv("PHOENIX_DIST_PC1_HOST", "") or "").strip()
    if not host:
        host = derive_host_from_unc(share_root)
    if not host:
        host = "127.0.0.1"
    os.environ["PHOENIX_DIST_PC1_HOST"] = host
    os.environ.setdefault("PHOENIX_DIST_ROLLOUT_PORT", str(ctx.get("rollout_port", 5562) or 5562))
    if not str(os.getenv("PHOENIX_DIST_AUTH_TOKEN", "") or "").strip():
        auth = str(ctx.get("auth_token", "") or "")
        if auth:
            os.environ["PHOENIX_DIST_AUTH_TOKEN"] = auth
    if not str(os.getenv("PHOENIX_DIST_PC2_NUM_WORKERS", "") or "").strip():
        os.environ["PHOENIX_DIST_PC2_NUM_WORKERS"] = str(max(1, int(ctx.get("pc2_num_workers", 8) or 8)))

    print(
        f"[PHOENIX][DIST][PC2] автоконфиг: host={host} port={os.environ.get('PHOENIX_DIST_ROLLOUT_PORT')} "
        f"auth={'задан' if os.environ.get('PHOENIX_DIST_AUTH_TOKEN') else 'нет'} "
        f"workers={os.environ.get('PHOENIX_DIST_PC2_NUM_WORKERS')} context={'есть' if ctx else 'НЕТ'}",
        flush=True,
    )
    _start_pc2_telemetry_thread()

    ctx_json = json.dumps(ctx, ensure_ascii=False)
    num_workers = max(1, _env_int("PHOENIX_DIST_PC2_NUM_WORKERS", 8))
    worker_id_base = max(0, _env_int("PHOENIX_DIST_PC2_WORKER_ID_BASE", 100))
    remote_ep_total = max(0, int(ctx.get("remote_episode_total", 0) or 0))
    if remote_ep_total <= 0:
        remote_ep_total = max(1, _env_int("PHOENIX_DIST_PC2_EPISODES_TOTAL", 0))
    worker_episode_plan = split_count_among_workers(total=remote_ep_total, num_workers=num_workers)
    print(
        f"[PHOENIX][DIST][PC2] spawning workers={num_workers} id_base={worker_id_base} "
        f"remote_episodes={remote_ep_total} plan={worker_episode_plan}",
        flush=True,
    )

    mp_ctx = mp.get_context("spawn")
    procs = []
    for i in range(num_workers):
        wid = worker_id_base + i
        p = mp_ctx.Process(target=_worker_main, args=(int(wid), ctx_json, int(worker_episode_plan[i])), daemon=False)
        p.start()
        procs.append(p)

    stop_flag = phoenix_dist_stop_flag_path()
    linger_sec = max(0.0, float(os.getenv("PHOENIX_DIST_PC2_LINGER_SEC", "600") or 600))
    workers_done_mono: float | None = None
    workers_done_logged = False
    try:
        while True:
            all_dead = sum(1 for p in procs if p.is_alive()) == 0
            if all_dead and workers_done_mono is None:
                workers_done_mono = time.monotonic()
            if all_dead and not workers_done_logged:
                workers_done_logged = True
                print(
                    "[PHOENIX][DIST][PC2] все воркеры доиграли квоту — держим телеметрию до stop.flag ПК1...",
                    flush=True,
                )
            should_exit, reason = pc2_dist_should_exit(
                stop_requested=phoenix_dist_stop_requested(stop_flag),
                all_workers_dead=all_dead,
                workers_done_mono=workers_done_mono,
                now_mono=time.monotonic(),
                linger_sec=linger_sec,
            )
            if should_exit:
                if reason == "stop_flag":
                    print(f"[PHOENIX][DIST][PC2] stop.flag detected ({stop_flag}), завершаем воркеры...", flush=True)
                else:
                    print(
                        f"[PHOENIX][DIST][PC2][WARN] stop.flag не пришёл за {int(linger_sec)} с после завершения воркеров. "
                        "Где: pc2_phoenix_actors.main. Что делать: проверьте train на ПК1.",
                        flush=True,
                    )
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
