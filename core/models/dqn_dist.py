# core/models/dqn_dist.py
"""DQN distributed actors: оркестрация ПК1↔ПК2 (stop-flag, train-context, RemoteDataQ).

Транспорт (wire/receiver/sink) переиспользуем из az_rollout_* — здесь только
DQN-specific имена файлов и mp.Queue-совместимый шим над RolloutSink.
"""

from __future__ import annotations

import json
import os
import time
from typing import Any


def derive_host_from_unc(path: str) -> str:
    r"""Из UNC-пути SMB-шары (\\server\share\...) достать имя/IP сервера ПК1.

    Возвращает '' для не-UNC (например, подключённый диск Z:\...) — тогда host
    надо задать явно. Примеры: '\\192.168.1.10\models' → '192.168.1.10';
    '//PC1/share' → 'PC1'.
    """
    p = str(path or "").strip()
    if p.startswith("\\\\") or p.startswith("//"):
        rest = p.lstrip("\\/").replace("/", "\\")
        server = rest.split("\\")[0].strip()
        return server
    return ""


def _actor_sync_dir() -> str:
    """Папка actor_sync на SMB-шаре: единый резолвер (40KAI_SHARE_ROOT → … → локально)."""
    try:
        from project_paths import share_actor_sync_dir

        return share_actor_sync_dir()
    except Exception:
        # Фолбэк, если project_paths недоступен (изолированный запуск).
        root = os.getenv("MODELS_DIR", os.path.join(os.getcwd(), "artifacts", "models"))
        return os.path.join(root, "actor_sync")


def dqn_dist_stop_flag_path() -> str:
    custom = str(os.getenv("DQN_DIST_STOP_FLAG_PATH", "") or "").strip()
    if custom:
        return custom
    return os.path.join(_actor_sync_dir(), "dqn_dist_stop.flag")


def dqn_dist_stop_requested(flag_path: str | None = None) -> bool:
    path = str(flag_path or dqn_dist_stop_flag_path())
    return bool(path) and os.path.isfile(path)


def clear_dqn_dist_stop_flag(flag_path: str | None = None) -> bool:
    """Удалить stop.flag прошлого прогона, чтобы ПК2-воркеры не вышли сразу. True, если файл был."""
    path = str(flag_path or dqn_dist_stop_flag_path())
    try:
        if os.path.isfile(path):
            os.remove(path)
            return True
    except OSError:
        pass
    return False


def touch_dqn_dist_stop_flag(flag_path: str | None = None) -> str:
    path = str(flag_path or dqn_dist_stop_flag_path())
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(time.strftime("%Y-%m-%dT%H:%M:%S") + "\n")
    return path


def dqn_dist_context_path() -> str:
    custom = str(os.getenv("DQN_DIST_CONTEXT_PATH", "") or "").strip()
    if custom:
        return custom
    return os.path.join(os.path.dirname(dqn_dist_stop_flag_path()), "dqn_dist_train_context.json")


def write_dqn_dist_train_context(payload: dict[str, Any]) -> str:
    path = dqn_dist_context_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    body = dict(payload or {})
    body.setdefault("written_at", time.strftime("%Y-%m-%dT%H:%M:%S"))
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(body, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def read_dqn_dist_train_context() -> dict[str, Any]:
    path = dqn_dist_context_path()
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def wait_dqn_dist_train_context(*, wait_sec: float = 0.0, poll_sec: float = 2.0) -> dict[str, Any]:
    wait_sec = max(0.0, float(wait_sec))
    deadline = time.monotonic() + wait_sec if wait_sec > 0 else 0.0
    while True:
        ctx = read_dqn_dist_train_context()
        if ctx:
            return ctx
        if wait_sec <= 0 or time.monotonic() >= deadline:
            return ctx
        print(
            f"[DQN][DIST][PC2] ждём dqn_dist_train_context.json "
            f"(осталось ~{max(0, int(deadline - time.monotonic()))} с, path={dqn_dist_context_path()})...",
            flush=True,
        )
        time.sleep(max(0.5, float(poll_sec)))


class RemoteDataQ:
    """mp.Queue-совместимый шим: .put((kind, payload)) → RolloutSink.put(kind, payload).

    Позволяет переиспользовать _actor_learner_actor_entry без правок: актор зовёт
    data_q.put(("batch", buf)) / ("ep", {...}) / ("done", idx) / ("error", str),
    а RemoteDataQ перенаправляет это в ZMQ PUSH (RemoteRolloutSink).
    """

    def __init__(self, sink) -> None:
        self._sink = sink

    def put(self, item, *args, **kwargs) -> None:
        if not isinstance(item, tuple) or len(item) != 2:
            return
        kind, payload = item
        self._sink.put(str(kind), payload)

    def close(self) -> None:
        try:
            self._sink.close()
        except Exception:
            pass
