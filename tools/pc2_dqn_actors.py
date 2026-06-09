#!/usr/bin/env python
"""ПК2: distributed DQN actors (env+net локально на ПК2, rollout PUSH → ПК1 learner)."""

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
from core.models.dqn_dist import (  # noqa: E402
    RemoteDataQ,
    derive_host_from_unc,
    dqn_dist_stop_flag_path,
    dqn_dist_stop_requested,
    wait_dqn_dist_train_context,
)


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return int(default)


def _start_pc2_telemetry_thread() -> None:
    """Демон-поток: пишет СИСТЕМНУЮ телеметрию ПК2 в actor_sync/pc2_telemetry.json.

    ПК1 читает файл и рисует карточки «ПК2 · GPU/CPU». Завершается со stop.flag или
    с процессом (daemon). Без inference-сервера это единственный канал телеметрии ПК2.
    """
    import threading

    def _loop() -> None:
        from core.telemetry.pc2_telemetry import (
            TELEMETRY_FILENAME,
            sample_system_telemetry,
            write_pc2_telemetry,
        )
        from project_paths import share_actor_sync_dir

        path = os.path.join(share_actor_sync_dir(), TELEMETRY_FILENAME)
        period = max(1.0, float(os.getenv("PC2_TELEMETRY_PERIOD_SEC", "3") or 3))
        while not dqn_dist_stop_requested():
            try:
                write_pc2_telemetry(path, sample_system_telemetry())
            except Exception:
                pass
            time.sleep(period)

    threading.Thread(target=_loop, name="pc2-telemetry", daemon=True).start()
    print("[DQN][DIST][PC2] телеметрия ПК2 -> actor_sync/pc2_telemetry.json (для карточек на ПК1)", flush=True)


def _worker_main(worker_id: int, ctx_json: str) -> None:
    import json

    # Консоль ПК2 часто cp1251 — символы вроде '→' роняют print с UnicodeEncodeError.
    # Принудительно UTF-8 + replace, чтобы лог воркера не валил процесс.
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    import gymnasium as gym
    import numpy as np
    import torch

    import train as train_mod
    from core.engine.agent_registry import make_env_contract
    from core.models.opponent_adapter import load_agent_opponent

    ctx = {}
    try:
        ctx = json.loads(ctx_json) if ctx_json else {}
    except Exception:
        ctx = {}

    # Ростер из train-context ПК1 (снимок на SMB) — иначе локальный data.json ПК2,
    # что даёт env_contract_hash mismatch при любом расхождении ростеров.
    roster = train_mod._roster_from_context(ctx)
    if roster is not None:
        print("[DQN][DIST][PC2] ростер: из контекста ПК1 (SMB)", flush=True)
    else:
        roster = train_mod._load_roster_config()
        print(
            "[DQN][DIST][PC2][WARN] ростер: локальный runtime/state/data.json "
            "(в контексте нет снимка — старый ПК1?). Возможен contract_hash mismatch.",
            flush=True,
        )
    b_len = int(roster["b_len"])
    b_hei = int(roster["b_hei"])

    enemy, model = train_mod._build_units_from_config(roster, b_len, b_hei)
    env0 = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
    state0, _ = env0.reset(options={"m": model, "e": enemy, "Type": "big", "trunc": True})
    if hasattr(state0, "values"):
        n_observations = len(list(state0.values()))
    else:
        n_observations = int(np.array(state0).shape[0])
    n_actions = train_mod.action_sizes_from_env(env0, len(model))
    try:
        env0.close()
    except Exception:
        pass

    # Стартовые веса с SMB (если есть), иначе свежая сеть.
    from project_paths import share_actor_sync_dir

    sync_path = os.path.join(share_actor_sync_dir(), "latest_policy.pth")
    init_weights = {}
    if os.path.isfile(sync_path):
        try:
            payload = torch.load(sync_path, map_location="cpu", weights_only=False)
            sd = payload.get("state_dict") if isinstance(payload, dict) else None
            if isinstance(sd, dict):
                init_weights = train_mod.normalize_state_dict(sd)
        except Exception as exc:
            print(f"[DQN][DIST][PC2][WARN] не удалось прочитать веса {sync_path}: {exc}", flush=True)
    if not init_weights:
        tmp_net = train_mod._make_dqn(n_observations, n_actions)
        init_weights = {
            k: v.detach().cpu().clone()
            for k, v in train_mod.normalize_state_dict(tmp_net.state_dict()).items()
        }

    mission_name = train_mod.normalize_mission_name(roster.get("mission", train_mod.DEFAULT_MISSION_NAME))
    env_contract = make_env_contract(
        n_observations=n_observations,
        n_actions=n_actions,
        mission_name=mission_name,
        ruleset_version=train_mod.RULESET_VERSION,
        extras={"actor_learner": 1, "distributed_actor": 1},
    )
    contract_hash = str(env_contract.get("contract_hash", "") or "")

    # Self-play opponent (опционально).
    opponent_spec = None
    self_play_enabled = int(_env_int("SELF_PLAY_ENABLED", 0))
    opp_id = str(os.getenv("OPPONENT_AGENT_ID", "") or str(ctx.get("opponent_agent_id", "") or "")).strip()
    if self_play_enabled and opp_id:
        try:
            opponent_spec = load_agent_opponent(agent_id=opp_id, expected_contract=env_contract)
        except Exception as exc:
            print(f"[DQN][DIST][PC2][WARN] opponent {opp_id} не загружен: {exc}", flush=True)
            opponent_spec = None

    host = str(os.getenv("DQN_DIST_PC1_HOST", "127.0.0.1"))
    port = _env_int("DQN_DIST_ROLLOUT_PORT", 5558)
    auth = str(os.getenv("DQN_DIST_AUTH_TOKEN", ""))
    batch_send = max(8, _env_int("ACTOR_BATCH_SEND", 32))
    episodes = max(1, _env_int("DQN_DIST_PC2_EPISODES_PER_WORKER", 1000000))

    sink = make_rollout_sink(
        mode="remote",
        source="remote",
        remote_host=host,
        remote_port=port,
        auth_token=auth,
        worker_id=int(worker_id),
        env_contract_hash=contract_hash,
        zmq_hwm=_env_int("DQN_DIST_ZMQ_HWM", 256),
    )
    remote_q = RemoteDataQ(sink)

    print(
        f"[DQN][DIST][PC2] worker={worker_id} -> {host}:{port} "
        f"contract_hash={contract_hash} n_obs={n_observations} n_act={len(n_actions)} "
        f"self_play={self_play_enabled} opp={opp_id or '-'}",
        flush=True,
    )

    try:
        train_mod._actor_learner_actor_entry(
            int(worker_id),
            int(episodes),
            roster,
            int(b_len),
            int(b_hei),
            int(n_observations),
            list(n_actions),
            init_weights,
            int(batch_send),
            0.0,
            0.0,
            False,
            remote_q,
            opponent_spec,
            float(os.getenv("SELF_PLAY_OPPONENT_EPSILON", "0.1") or 0.1),
            int(self_play_enabled),
        )
    finally:
        remote_q.close()


def main() -> int:
    import json

    # Консоль ПК2 часто cp1251 — любой не-ASCII символ ('->' и т.п.) роняет print.
    # Форсим UTF-8 для всего main-процесса (воркеры делают это сами в _worker_main).
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    wait_sec = max(0.0, float(os.getenv("DQN_DIST_WAIT_CONTEXT_SEC", "0") or 0.0))
    ctx = wait_dqn_dist_train_context(wait_sec=wait_sec)
    if ctx.get("opponent_agent_id"):
        os.environ.setdefault("OPPONENT_AGENT_ID", str(ctx["opponent_agent_id"]))

    # --- Автозаполнение: на ПК2 достаточно задать 40KAI_SHARE_ROOT (SMB-шара ПК1). ---
    # IP ПК1 — из UNC-пути шары; порт и auth — из train-context, который пишет ПК1.
    from project_paths import resolve_share_models_root

    share_root = resolve_share_models_root()
    # MODELS_DIR для обратной совместимости (downstream-код, читающий его напрямую).
    os.environ.setdefault("MODELS_DIR", share_root)

    host = str(os.getenv("DQN_DIST_PC1_HOST", "") or "").strip()
    if not host:
        host = derive_host_from_unc(share_root)
    if not host:
        host = "127.0.0.1"
    os.environ["DQN_DIST_PC1_HOST"] = host

    if not str(os.getenv("DQN_DIST_ROLLOUT_PORT", "") or "").strip():
        os.environ["DQN_DIST_ROLLOUT_PORT"] = str(ctx.get("rollout_port", 5558) or 5558)

    if not str(os.getenv("DQN_DIST_AUTH_TOKEN", "") or "").strip():
        ctx_auth = str(ctx.get("auth_token", "") or "")
        if ctx_auth:
            os.environ["DQN_DIST_AUTH_TOKEN"] = ctx_auth

    if not str(os.getenv("DQN_DIST_PC2_NUM_WORKERS", "") or "").strip():
        os.environ["DQN_DIST_PC2_NUM_WORKERS"] = str(max(1, min(int(os.cpu_count() or 6), 12)))

    print(
        f"[DQN][DIST][PC2] автоконфиг: host={host} (из {'env' if os.getenv('DQN_DIST_PC1_HOST') else 'UNC'}) "
        f"port={os.environ.get('DQN_DIST_ROLLOUT_PORT')} "
        f"auth={'задан' if os.environ.get('DQN_DIST_AUTH_TOKEN') else 'нет'} "
        f"workers={os.environ.get('DQN_DIST_PC2_NUM_WORKERS')} "
        f"context={'есть' if ctx else 'НЕТ (ПК1 не запущен?)'}",
        flush=True,
    )

    _start_pc2_telemetry_thread()

    ctx_json = json.dumps(ctx, ensure_ascii=False)

    num_workers = max(1, _env_int("DQN_DIST_PC2_NUM_WORKERS", 6))
    worker_id_base = max(0, _env_int("DQN_DIST_PC2_WORKER_ID_BASE", 100))

    print(
        f"[DQN][DIST][PC2] spawning workers={num_workers} id_base={worker_id_base} "
        f"rollout_target={os.getenv('DQN_DIST_PC1_HOST', '127.0.0.1')}:{_env_int('DQN_DIST_ROLLOUT_PORT', 5558)}",
        flush=True,
    )

    mp_ctx = mp.get_context("spawn")
    procs = []
    for i in range(num_workers):
        wid = worker_id_base + i
        p = mp_ctx.Process(target=_worker_main, args=(int(wid), ctx_json), daemon=False)
        p.start()
        procs.append(p)

    stop_flag = dqn_dist_stop_flag_path()
    try:
        while True:
            if dqn_dist_stop_requested(stop_flag):
                print(f"[DQN][DIST][PC2] stop.flag detected ({stop_flag}), завершаем воркеры...", flush=True)
                break
            if sum(1 for p in procs if p.is_alive()) == 0:
                print("[DQN][DIST][PC2] все воркеры завершились.", flush=True)
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
