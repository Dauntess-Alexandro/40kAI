"""Rollout emission: local mp.Queue or remote ZMQ PUSH to learner."""

from __future__ import annotations

import json
import os
import time
from typing import Any, Protocol

from core.models.az_rollout_protocol import (
    build_hello_payload,
    build_wire_message,
    encode_rollout_message,
)


def _actor_sync_dir() -> str:
    """Папка actor_sync на SMB-шаре: единый резолвер (40KAI_SHARE_ROOT → … → локально)."""
    try:
        from project_paths import share_actor_sync_dir

        return share_actor_sync_dir()
    except Exception:
        root = os.getenv("MODELS_DIR", os.path.join(os.getcwd(), "artifacts", "models"))
        return os.path.join(root, "actor_sync")


def write_az_remote_search_cfg(
    *,
    obs_dim: int,
    action_sizes: list[int],
    hidden_size: int,
    num_layers: int,
    n_value_ensemble: int,
    num_simulations: int,
    sources: list[str] | None = None,
    filename: str = "az_remote_search_cfg.json",
) -> list[str]:
    """ПК1: записать <filename> (форма сети для IS на ПК2).

    Кладёт копию в actor_sync на шаре (её читает IS-сервер ПК2, чтобы собрать
    сеть, совместимую с обучаемой) и локально в runtime/state. Вызывается
    автоматически при старте AZ/GAZ-распределёнки. Возвращает записанные пути.

    filename: имя cfg-файла. AZ → az_remote_search_cfg.json (дефолт),
    GAZ → gaz_remote_search_cfg.json (сеть та же, но веса/файл отдельные).
    """
    cfg = {
        "obs_dim": int(obs_dim),
        "action_sizes": [int(x) for x in action_sizes],
        "hidden_size": int(hidden_size),
        "num_layers": int(num_layers),
        "n_value_ensemble": int(n_value_ensemble),
        "num_simulations": int(num_simulations),
        "_generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "_sources": list(sources or ["train.py:auto"]),
    }
    body = json.dumps(cfg, indent=2, ensure_ascii=False) + "\n"

    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    targets = [
        os.path.join(repo_root, "runtime", "state", str(filename)),
        os.path.join(_actor_sync_dir(), str(filename)),
    ]
    written: list[str] = []
    for path in targets:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(body)
            written.append(path)
        except OSError:
            continue
    return written


def az_dist_stop_flag_path(algo: str | None = None) -> str:
    """Путь stop-flag distributed self-play.

    GAZ и AZ — раздельные флаги, чтобы distributed-прогоны не глушили друг друга:
    gumbel_az → gaz_dist_stop.flag, иначе az_dist_stop.flag. Env AZ_DIST_STOP_FLAG_PATH
    переопределяет (его прокидывает ПК1 → ПК2).
    """
    custom = str(os.getenv("AZ_DIST_STOP_FLAG_PATH", "") or "").strip()
    if custom:
        return custom
    name = "gaz_dist_stop.flag" if str(algo or "").strip().lower() == "gumbel_az" else "az_dist_stop.flag"
    return os.path.join(_actor_sync_dir(), name)


def az_dist_stop_requested(flag_path: str | None = None) -> bool:
    path = str(flag_path or az_dist_stop_flag_path())
    return bool(path) and os.path.isfile(path)


def az_dist_context_path() -> str:
    custom = str(os.getenv("AZ_DIST_CONTEXT_PATH", "") or "").strip()
    if custom:
        return custom
    return os.path.join(os.path.dirname(az_dist_stop_flag_path()), "az_dist_train_context.json")


def write_az_dist_train_context(payload: dict[str, Any]) -> str:
    path = az_dist_context_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    body = dict(payload or {})
    body.setdefault("written_at", time.strftime("%Y-%m-%dT%H:%M:%S"))
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(body, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def read_az_dist_train_context() -> dict[str, Any]:
    path = az_dist_context_path()
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


# Поля alphazero_tree, которые ПК1 пишет в SMB, а dist-акторы ПК2 подставляют в MCTS.
AZ_DIST_HYPERPARAM_KEYS: tuple[str, ...] = (
    "mcts_simulations",
    "mcts_parallel_sims",
    "mcts_max_depth",
    "mcts_top_k_per_head",
    "mcts_batch_eval_size",
    "mcts_simulate_enemy",
    "mcts_mode",
    "mcts_root_dirichlet_only",
    "mcts_eval_cache_size",
    "c_puct",
    "c_puct_min",
    "c_puct_max",
    "c_puct_schedule",
    "dirichlet_alpha",
    "dirichlet_eps",
    "pw_alpha",
    "pw_beta",
    "prior_weight_early",
    "temperature_opening_moves",
    "temperature_opening_value",
    "temperature_late_value",
    "outcome_only",
    "outcome_value_win",
    "outcome_value_loss",
    "outcome_value_draw",
    "actor_batch_send",
    "inference_timeout",
    "self_play_enabled",
)

# GAZ (gumbel_az) использует те же _main_actor_learner_alphazero/_az_env_worker_entry,
# но GumbelAlphaZeroSearch читает свои поля поиска (не AZ MCTS). Ключи не пересекаются
# с AZ (mcts_* vs num_*), поэтому пакуем общим union — pack/normalize не теряют ни AZ,
# ни GAZ поля; build_*_worker_payloads выбирает форму по train_algo.
GAZ_DIST_HYPERPARAM_KEYS: tuple[str, ...] = (
    "num_simulations",
    "num_considered_actions",
    "max_depth",
    "value_scale",
    "c_visit",
    "simulate_enemy",
    "joint_action",
    "eval_cache_size",
    "batch_eval_size",
)

_DIST_HYPERPARAM_KEYS: tuple[str, ...] = AZ_DIST_HYPERPARAM_KEYS + GAZ_DIST_HYPERPARAM_KEYS


def pack_az_dist_hyperparams(values: dict[str, Any]) -> dict[str, Any]:
    """Оставить только ключи для SMB az_dist_train_context.az_hyperparams (AZ ∪ GAZ)."""
    src = values if isinstance(values, dict) else {}
    out: dict[str, Any] = {}
    for key in _DIST_HYPERPARAM_KEYS:
        if key not in src:
            continue
        out[key] = src[key]
    return out


def normalize_az_dist_hyperparams(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {}
    return pack_az_dist_hyperparams(raw)


def _hp_pick(hp: dict[str, Any], key: str, default: Any) -> Any:
    if key in hp:
        return hp[key]
    return default


def _hp_bool(hp: dict[str, Any], key: str, default: bool) -> bool:
    raw = _hp_pick(hp, key, default)
    if isinstance(raw, bool):
        return raw
    return str(raw).strip().lower() in ("1", "true", "yes")


def build_az_dist_worker_payloads(
    hp: dict[str, Any] | None,
    *,
    defaults: dict[str, Any],
) -> dict[str, Any]:
    """
  Собрать mcts/sp/outcome payload для _az_env_worker_entry.
  hp — снимок с ПК1 (SMB); defaults — локальный fallback (модуль train на ПК2).
  """
    hp = normalize_az_dist_hyperparams(hp or {})
    d = defaults if isinstance(defaults, dict) else {}

    mcts_payload = {
        "simulations": int(_hp_pick(hp, "mcts_simulations", d.get("simulations", 32))),
        "c_puct": float(_hp_pick(hp, "c_puct", d.get("c_puct", 1.5))),
        "c_puct_min": float(_hp_pick(hp, "c_puct_min", d.get("c_puct_min", 1.0))),
        "c_puct_max": float(_hp_pick(hp, "c_puct_max", d.get("c_puct_max", 2.0))),
        "c_puct_schedule": str(_hp_pick(hp, "c_puct_schedule", d.get("c_puct_schedule", "none"))),
        "dirichlet_alpha": float(_hp_pick(hp, "dirichlet_alpha", d.get("dirichlet_alpha", 0.3))),
        "dirichlet_eps": float(_hp_pick(hp, "dirichlet_eps", d.get("dirichlet_eps", 0.25))),
        "top_k_per_head": int(_hp_pick(hp, "mcts_top_k_per_head", d.get("top_k_per_head", 8))),
        "max_depth": int(_hp_pick(hp, "mcts_max_depth", d.get("max_depth", 1))),
        "mode": str(_hp_pick(hp, "mcts_mode", d.get("mode", "tree"))).strip().lower() or "tree",
        "root_dirichlet_only": _hp_bool(
            hp, "mcts_root_dirichlet_only", bool(d.get("root_dirichlet_only", True))
        ),
        "eval_cache_size": int(_hp_pick(hp, "mcts_eval_cache_size", d.get("eval_cache_size", 10000))),
        "pw_alpha": float(_hp_pick(hp, "pw_alpha", d.get("pw_alpha", 1.0))),
        "pw_beta": float(_hp_pick(hp, "pw_beta", d.get("pw_beta", 0.5))),
        "prior_weight_early": float(_hp_pick(hp, "prior_weight_early", d.get("prior_weight_early", 0.25))),
        "batch_eval_size": int(_hp_pick(hp, "mcts_batch_eval_size", d.get("batch_eval_size", 16))),
        "parallel_simulations": int(_hp_pick(hp, "mcts_parallel_sims", d.get("parallel_simulations", 1))),
        "simulate_enemy_in_tree": _hp_bool(
            hp, "mcts_simulate_enemy", bool(d.get("simulate_enemy_in_tree", True))
        ),
    }
    sp_payload = {
        "temperature_opening_moves": int(
            _hp_pick(hp, "temperature_opening_moves", d.get("temperature_opening_moves", 12))
        ),
        "temperature_opening_value": float(
            _hp_pick(hp, "temperature_opening_value", d.get("temperature_opening_value", 1.0))
        ),
        "temperature_late_value": float(
            _hp_pick(hp, "temperature_late_value", d.get("temperature_late_value", 0.3))
        ),
    }
    outcome_payload = {
        "outcome_only": _hp_bool(hp, "outcome_only", bool(d.get("outcome_only", True))),
        "outcome_value_win": float(_hp_pick(hp, "outcome_value_win", d.get("outcome_value_win", 1.0))),
        "outcome_value_loss": float(_hp_pick(hp, "outcome_value_loss", d.get("outcome_value_loss", -1.0))),
        "outcome_value_draw": float(_hp_pick(hp, "outcome_value_draw", d.get("outcome_value_draw", -0.25))),
        "policy_version": 0,
    }
    batch_send = int(_hp_pick(hp, "actor_batch_send", d.get("batch_send", 32)))
    inference_timeout = float(_hp_pick(hp, "inference_timeout", d.get("inference_timeout", 5.0)))
    self_play_enabled = int(
        _hp_bool(hp, "self_play_enabled", bool(int(d.get("self_play_enabled", 0))))
    )
    return {
        "mcts": mcts_payload,
        "sp": sp_payload,
        "outcome": outcome_payload,
        "batch_send": batch_send,
        "inference_timeout": inference_timeout,
        "self_play_enabled": self_play_enabled,
    }


def build_gaz_dist_worker_payloads(
    hp: dict[str, Any] | None,
    *,
    defaults: dict[str, Any],
) -> dict[str, Any]:
    """GAZ-вариант build_az_dist_worker_payloads: mcts-payload в форме GumbelAZSearch.

    Ключи mcts совпадают с тем, что читает _build_az_search для gumbel_az
    (num_simulations/num_considered_actions/joint_action/...). sp/outcome/batch_send —
    как у AZ (общий _az_env_worker_entry).
    """
    hp = normalize_az_dist_hyperparams(hp or {})
    d = defaults if isinstance(defaults, dict) else {}

    mcts_payload = {
        "num_simulations": int(_hp_pick(hp, "num_simulations", d.get("num_simulations", 32))),
        "num_considered_actions": int(
            _hp_pick(hp, "num_considered_actions", d.get("num_considered_actions", 8))
        ),
        "max_depth": int(_hp_pick(hp, "max_depth", d.get("max_depth", 1))),
        "value_scale": float(_hp_pick(hp, "value_scale", d.get("value_scale", 0.1))),
        "c_visit": float(_hp_pick(hp, "c_visit", d.get("c_visit", 50.0))),
        "eval_cache_size": int(_hp_pick(hp, "eval_cache_size", d.get("eval_cache_size", 10000))),
        "batch_eval_size": int(_hp_pick(hp, "batch_eval_size", d.get("batch_eval_size", 16))),
        "simulate_enemy": _hp_bool(hp, "simulate_enemy", bool(d.get("simulate_enemy", False))),
        "joint_action": _hp_bool(hp, "joint_action", bool(d.get("joint_action", False))),
    }
    sp_payload = {
        "temperature_opening_moves": int(
            _hp_pick(hp, "temperature_opening_moves", d.get("temperature_opening_moves", 12))
        ),
        "temperature_opening_value": float(
            _hp_pick(hp, "temperature_opening_value", d.get("temperature_opening_value", 1.0))
        ),
        "temperature_late_value": float(
            _hp_pick(hp, "temperature_late_value", d.get("temperature_late_value", 0.3))
        ),
    }
    outcome_payload = {
        "outcome_only": _hp_bool(hp, "outcome_only", bool(d.get("outcome_only", True))),
        "outcome_value_win": float(_hp_pick(hp, "outcome_value_win", d.get("outcome_value_win", 1.0))),
        "outcome_value_loss": float(_hp_pick(hp, "outcome_value_loss", d.get("outcome_value_loss", -1.0))),
        "outcome_value_draw": float(_hp_pick(hp, "outcome_value_draw", d.get("outcome_value_draw", -0.25))),
        "policy_version": 0,
    }
    batch_send = int(_hp_pick(hp, "actor_batch_send", d.get("batch_send", 32)))
    inference_timeout = float(_hp_pick(hp, "inference_timeout", d.get("inference_timeout", 5.0)))
    self_play_enabled = int(
        _hp_bool(hp, "self_play_enabled", bool(int(d.get("self_play_enabled", 0))))
    )
    return {
        "mcts": mcts_payload,
        "sp": sp_payload,
        "outcome": outcome_payload,
        "batch_send": batch_send,
        "inference_timeout": inference_timeout,
        "self_play_enabled": self_play_enabled,
    }


def wait_az_dist_train_context(
    *,
    wait_sec: float = 0.0,
    require_hyperparams: bool = False,
    require_opponent: bool = False,
    poll_sec: float = 2.0,
    log_fn=None,
) -> dict[str, Any]:
    """Ждать az_dist_train_context.json на SMB (ПК1 пишет при старте train)."""
    wait_sec = max(0.0, float(wait_sec))
    deadline = time.monotonic() + wait_sec if wait_sec > 0 else 0.0

    def _ready(ctx: dict[str, Any]) -> bool:
        if require_opponent and not str(ctx.get("opponent_agent_id", "") or "").strip():
            return False
        if require_hyperparams and not normalize_az_dist_hyperparams(ctx.get("az_hyperparams")):
            return False
        return bool(ctx)

    while True:
        ctx = read_az_dist_train_context()
        if _ready(ctx):
            return ctx
        if wait_sec <= 0 or time.monotonic() >= deadline:
            return ctx
        if log_fn is not None:
            left = max(0, int(deadline - time.monotonic()))
            log_fn(
                f"[AZ][DIST] ждём az_dist_train_context.json на SMB "
                f"(осталось ~{left} с, path={az_dist_context_path()})"
            )
        else:
            print(
                f"[AZ][DIST][PC2] ждём az_dist_train_context.json "
                f"(осталось ~{max(0, int(deadline - time.monotonic()))} с)...",
                flush=True,
            )
        time.sleep(max(0.5, float(poll_sec)))


class RolloutSink(Protocol):
    def put(self, kind: str, payload: Any) -> None: ...

    def close(self) -> None: ...


def make_rollout_sink(
    *,
    mode: str,
    data_q=None,
    source: str = "local",
    remote_host: str = "",
    remote_port: int = 5557,
    auth_token: str = "",
    worker_id: int = 0,
    env_contract_hash: str = "",
    zmq_hwm: int = 256,
) -> RolloutSink:
    m = str(mode or "local").strip().lower()
    if m == "remote":
        return RemoteRolloutSink(
            host=str(remote_host or "127.0.0.1"),
            port=int(remote_port),
            auth_token=str(auth_token or ""),
            source=str(source or "remote"),
            worker_id=int(worker_id),
            env_contract_hash=str(env_contract_hash or ""),
            zmq_hwm=int(zmq_hwm),
        )
    if data_q is None:
        raise ValueError("LocalRolloutSink requires data_q")
    return LocalRolloutSink(data_q, source=str(source or "local"))


class LocalRolloutSink:
    def __init__(self, data_q, *, source: str = "local") -> None:
        self._q = data_q
        self._source = str(source or "local")

    def put(self, kind: str, payload: Any) -> None:
        if kind in ("rollout", "ep") and isinstance(payload, dict):
            out = dict(payload)
            out.setdefault("source", self._source)
            self._q.put((kind, out))
            return
        self._q.put((kind, payload))

    def close(self) -> None:
        return None


class RemoteRolloutSink:
    def __init__(
        self,
        *,
        host: str,
        port: int,
        auth_token: str = "",
        source: str = "remote",
        worker_id: int = 0,
        env_contract_hash: str = "",
        zmq_hwm: int = 256,
    ) -> None:
        import zmq

        self._auth = str(auth_token or "")
        self._source = str(source or "remote")
        self._worker_id = int(worker_id)
        self._env_contract_hash = str(env_contract_hash or "")
        self._ctx = zmq.Context.instance()
        self._sock = self._ctx.socket(zmq.PUSH)
        self._sock.setsockopt(zmq.SNDHWM, max(1, int(zmq_hwm)))
        self._sock.setsockopt(zmq.LINGER, 2000)
        endpoint = f"tcp://{host}:{int(port)}"
        self._sock.connect(endpoint)
        self._sent_counts: dict[str, int] = {}
        self._failed_counts: dict[str, int] = {}
        self._sent_transitions = 0
        hello = build_hello_payload(
            worker_id=self._worker_id,
            env_contract_hash=env_contract_hash,
            source=self._source,
        )
        self._send("hello", hello)

    def _send(self, kind: str, payload: dict[str, Any]) -> None:
        import zmq

        wire = build_wire_message(kind=kind, payload=payload, auth_token=self._auth)
        data = encode_rollout_message(wire)
        try:
            self._sock.send(data, flags=0)
            self._sent_counts[kind] = self._sent_counts.get(kind, 0) + 1
        except zmq.Again:
            self._failed_counts[kind] = self._failed_counts.get(kind, 0) + 1
            print(
                f"[AZ][DIST][SINK] queue_full worker={self._worker_id} kind={kind} "
                "(ZMQ SNDHWM). Где: RemoteRolloutSink. Что делать: увеличьте HWM или снизьте нагрузку PC2.",
                flush=True,
            )
        except zmq.ZMQError as exc:
            self._failed_counts[kind] = self._failed_counts.get(kind, 0) + 1
            print(
                f"[AZ][DIST][SINK] send failed worker={self._worker_id} kind={kind}: {exc}",
                flush=True,
            )

    def put(self, kind: str, payload: Any) -> None:
        if kind == "done":
            return
        if kind == "batch":
            # DQN: payload — голый список 6-кортежей (как в локальном data_q).
            steps = payload.get("steps") if isinstance(payload, dict) else payload
            # Кортежи не обходятся _encode_value рекурсивно — конвертируем в списки.
            steps_as_lists = [list(t) for t in (steps or [])]
            wrapped = {
                "worker_id": int(self._worker_id),
                "steps": steps_as_lists,
                "priority": (payload.get("priority") if isinstance(payload, dict) else None),
                "source": self._source,
                # Контракт-гард: каждое batch-сообщение несёт хэш (ZMQ message-oriented,
                # валидация поштучная — нельзя полагаться только на hello).
                "env_contract_hash": self._env_contract_hash,
            }
            self._sent_transitions += len(steps_as_lists)
            self._send("batch", wrapped)
            return
        if not isinstance(payload, dict):
            if kind == "error":
                self._send("error", {"message": str(payload)})
            return
        out = dict(payload)
        out.setdefault("source", self._source)
        if kind == "rollout":
            out.setdefault("env_contract_hash", out.get("env_contract_hash", ""))
        self._send(str(kind), out)

    def close(self) -> None:
        try:
            batch_n = int(self._sent_counts.get("batch", 0))
            ep_n = int(self._sent_counts.get("ep", 0))
            rollout_n = int(self._sent_counts.get("rollout", 0))
            failed_n = int(sum(self._failed_counts.values()))
            # DQN dist: _actor_learner_actor_entry шлёт kind=batch (переходы) и kind=ep (метрики).
            # AZ dist: kind=rollout. sent_rollout=0 при DQN — норма, смотрите sent_batch.
            if batch_n > 0 or (ep_n > 0 and rollout_n == 0):
                warn = ""
                if ep_n > 0 and batch_n == 0:
                    warn = (
                        " WARN: ep без batch — обучающие переходы не ушли на ПК1 "
                        "(contract_hash mismatch или сбой ZMQ)."
                    )
                print(
                    f"[DQN][DIST][SINK] closed worker={self._worker_id} "
                    f"sent_batch={batch_n} sent_transitions={int(self._sent_transitions)} "
                    f"sent_ep={ep_n} failed={failed_n}{warn}",
                    flush=True,
                )
            else:
                print(
                    f"[AZ][DIST][SINK] closed worker={self._worker_id} "
                    f"sent_rollout={rollout_n} sent_ep={ep_n} failed={failed_n}",
                    flush=True,
                )
        except Exception:
            pass
        try:
            self._sock.close(linger=0)
        except Exception:
            pass
