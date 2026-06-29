"""PHOENIX distributed actors: sequence windows, stop/context helpers, sync metadata."""

from __future__ import annotations

import json
import os
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import numpy as np

from core.models.phoenix_replay import SequenceWindow

PHOENIX_DIST_TOPUP_ACTOR_IDX = 9100
PHOENIX_DIST_PROTOCOL_KIND = "phoenix_batch"
PHOENIX_SYNC_WEIGHTS_NAME = "latest_phoenix_policy.pth"


def _actor_sync_dir() -> str:
    try:
        from project_paths import share_actor_sync_dir

        return share_actor_sync_dir()
    except Exception:
        root = os.getenv("MODELS_DIR", os.path.join(os.getcwd(), "artifacts", "models"))
        return os.path.join(root, "actor_sync")


def phoenix_dist_env_contract_extras(*, num_local_actors: int) -> dict[str, int | str]:
    return {"actor_learner": 1, "train_algo": "phoenix", "num_actors": max(1, int(num_local_actors))}


def resolve_phoenix_dist_contract_hash(
    *,
    ctx: dict[str, Any] | None,
    n_observations: int,
    n_actions: list[int],
    mission_name: str,
    ruleset_version: str,
    num_local_actors: int,
) -> str:
    cached = str((ctx or {}).get("env_contract_hash", "") or "").strip()
    if cached:
        return cached
    from core.engine.agent_registry import make_env_contract

    ec = make_env_contract(
        n_observations=int(n_observations),
        n_actions=[int(x) for x in n_actions],
        mission_name=str(mission_name),
        ruleset_version=str(ruleset_version),
        extras=phoenix_dist_env_contract_extras(num_local_actors=num_local_actors),
    )
    return str(ec.get("contract_hash", "") or "")


def phoenix_dist_stop_flag_path() -> str:
    custom = str(os.getenv("PHOENIX_DIST_STOP_FLAG_PATH", "") or "").strip()
    if custom:
        return custom
    return os.path.join(_actor_sync_dir(), "phoenix_dist_stop.flag")


def phoenix_dist_stop_requested(flag_path: str | None = None) -> bool:
    path = str(flag_path or phoenix_dist_stop_flag_path())
    return bool(path) and os.path.isfile(path)


def clear_phoenix_dist_stop_flag(flag_path: str | None = None) -> bool:
    path = str(flag_path or phoenix_dist_stop_flag_path())
    try:
        if os.path.isfile(path):
            os.remove(path)
            return True
    except OSError:
        pass
    return False


def touch_phoenix_dist_stop_flag(flag_path: str | None = None) -> str:
    path = str(flag_path or phoenix_dist_stop_flag_path())
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(time.strftime("%Y-%m-%dT%H:%M:%S") + "\n")
    return path


def phoenix_dist_context_path() -> str:
    custom = str(os.getenv("PHOENIX_DIST_CONTEXT_PATH", "") or "").strip()
    if custom:
        return custom
    return os.path.join(os.path.dirname(phoenix_dist_stop_flag_path()), "phoenix_dist_train_context.json")


def write_phoenix_dist_train_context(payload: dict[str, Any]) -> str:
    path = phoenix_dist_context_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    body = dict(payload or {})
    body.setdefault("written_at", time.strftime("%Y-%m-%dT%H:%M:%S"))
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(body, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def read_phoenix_dist_train_context() -> dict[str, Any]:
    path = phoenix_dist_context_path()
    if not os.path.isfile(path):
        return {}
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def wait_phoenix_dist_train_context(*, wait_sec: float = 0.0, poll_sec: float = 2.0) -> dict[str, Any]:
    wait_sec = max(0.0, float(wait_sec))
    deadline = time.monotonic() + wait_sec if wait_sec > 0 else 0.0
    while True:
        ctx = read_phoenix_dist_train_context()
        if ctx:
            return ctx
        if wait_sec <= 0 or time.monotonic() >= deadline:
            return ctx
        print(
            f"[PHOENIX][DIST][PC2] ждём phoenix_dist_train_context.json "
            f"(осталось ~{max(0, int(deadline - time.monotonic()))} с, path={phoenix_dist_context_path()})...",
            flush=True,
        )
        time.sleep(max(0.5, float(poll_sec)))


def split_count_among_workers(*, total: int, num_workers: int) -> list[int]:
    n = max(1, int(num_workers))
    count = max(0, int(total))
    base = count // n
    rem = count % n
    return [int(base + (1 if i < rem else 0)) for i in range(n)]


def resolve_phoenix_dist_episode_split(*, total_episodes: int, local_fraction: float) -> tuple[int, int]:
    total = max(1, int(total_episodes))
    frac = max(0.05, min(0.95, float(local_fraction)))
    if total == 1:
        return 1, 0
    local = max(1, min(total - 1, int(round(total * frac))))
    remote = max(0, total - local)
    if remote == 0:
        local = total - 1
        remote = 1
    return local, remote


def compute_phoenix_dist_topup_episodes(
    *,
    episodes_finished: int,
    total_episodes: int,
    local_actors_done: int,
    num_local_actors: int,
    remote_alive: int,
    topup_process_alive: bool,
) -> int:
    if bool(topup_process_alive) or int(remote_alive) > 0 or int(local_actors_done) < int(num_local_actors):
        return 0
    return max(0, int(total_episodes) - int(episodes_finished))


def phoenix_actor_epsilon_floor(
    *,
    actor_idx: int,
    total_actors: int,
    floor_min: float = 0.02,
    floor_max: float = 0.20,
    mode: str = "apex",
) -> float:
    if str(mode or "apex").strip().lower() != "apex":
        return 0.0
    n = max(1, int(total_actors))
    lo = max(0.0, float(floor_min))
    hi = max(lo, float(floor_max))
    if n <= 1:
        return 0.0
    # Stable for local ids 0..N-1 and remote ids 100+; rank wraps by total actor count.
    rank = max(0, int(actor_idx)) % n
    return float(lo + (hi - lo) * (rank / float(n - 1)))


@dataclass(frozen=True)
class PhoenixWindowMeta:
    episode_id: int
    start_step: int


class PhoenixSequenceAssembler:
    """Actor-side assembler: raw steps -> H+1 windows with terminal tail padding."""

    def __init__(self, window: int):
        self.window = int(window)
        self.span = self.window + 1
        self._episode_steps: list[tuple[np.ndarray, np.ndarray, np.ndarray, float, bool]] = []
        self._emit_start = 0
        self._episode_id = 0

    def reset_episode(self, episode_id: int | None = None) -> None:
        self._episode_steps = []
        self._emit_start = 0
        if episode_id is not None:
            self._episode_id = int(episode_id)

    def append(self, obs, action, active_mask, reward: float, done: bool) -> list[tuple[SequenceWindow, PhoenixWindowMeta]]:
        self._episode_steps.append(
            (
                np.asarray(obs, dtype=np.float32),
                np.asarray(action, dtype=np.int64),
                np.asarray(active_mask, dtype=bool),
                float(reward),
                bool(done),
            )
        )
        out: list[tuple[SequenceWindow, PhoenixWindowMeta]] = []
        while self._emit_start + self.span <= len(self._episode_steps):
            out.append((self._materialize(self._emit_start), PhoenixWindowMeta(self._episode_id, self._emit_start)))
            self._emit_start += 1
        if bool(done):
            while self._emit_start < len(self._episode_steps):
                out.append((self._materialize(self._emit_start, pad_terminal=True), PhoenixWindowMeta(self._episode_id, self._emit_start)))
                self._emit_start += 1
            self.reset_episode(self._episode_id + 1)
        return out

    def _materialize(self, start: int, *, pad_terminal: bool = False) -> SequenceWindow:
        steps = list(self._episode_steps[start : start + self.span])
        if pad_terminal and steps:
            last = steps[-1]
            while len(steps) < self.span:
                steps.append((last[0], last[1], last[2], 0.0, True))
        if len(steps) != self.span:
            raise ValueError(
                f"PHOENIX assembler span mismatch: got {len(steps)}, expected {self.span}. "
                "Где: PhoenixSequenceAssembler._materialize. Что делать: проверьте порядок append/done."
            )
        obs = np.stack([s[0] for s in steps]).astype(np.float32, copy=False)
        actions = np.stack([s[1] for s in steps]).astype(np.int64, copy=False)
        active = np.stack([s[2] for s in steps]).astype(bool, copy=False)
        rewards = np.asarray([s[3] for s in steps], dtype=np.float32)
        dones = np.zeros(self.span, dtype=np.float32)
        terminated = False
        for k, s in enumerate(steps):
            if terminated:
                dones[k] = 1.0
            if s[4]:
                terminated = True
                if k + 1 < self.span:
                    dones[k + 1 :] = 1.0
        return SequenceWindow(obs, actions, active, rewards, dones)


def pack_phoenix_batch(
    windows: list[SequenceWindow],
    *,
    worker_id: int,
    env_contract_hash: str = "",
    source: str = "local",
    metas: list[PhoenixWindowMeta] | None = None,
    priorities: list[float] | np.ndarray | None = None,
) -> dict[str, Any]:
    if not windows:
        return {
            "worker_id": int(worker_id),
            "env_contract_hash": str(env_contract_hash or ""),
            "source": str(source),
            "obs": np.zeros((0,), dtype=np.float32),
            "actions": np.zeros((0,), dtype=np.int64),
            "active_masks": np.zeros((0,), dtype=bool),
            "rewards": np.zeros((0,), dtype=np.float32),
            "dones": np.zeros((0,), dtype=np.float32),
            "episode_ids": np.zeros((0,), dtype=np.int64),
            "start_steps": np.zeros((0,), dtype=np.int64),
        }
    meta_list = metas or [PhoenixWindowMeta(0, i) for i in range(len(windows))]
    return {
        "worker_id": int(worker_id),
        "env_contract_hash": str(env_contract_hash or ""),
        "source": str(source),
        "obs": np.stack([np.asarray(w.obs, dtype=np.float32) for w in windows]),
        "actions": np.stack([np.asarray(w.actions, dtype=np.int64) for w in windows]),
        "active_masks": np.stack([np.asarray(w.active_masks, dtype=bool) for w in windows]),
        "rewards": np.stack([np.asarray(w.rewards, dtype=np.float32) for w in windows]),
        "dones": np.stack([np.asarray(w.dones, dtype=np.float32) for w in windows]),
        "episode_ids": np.asarray([m.episode_id for m in meta_list], dtype=np.int64),
        "start_steps": np.asarray([m.start_step for m in meta_list], dtype=np.int64),
        "priority": None if priorities is None else np.asarray(priorities, dtype=np.float32),
    }


def unpack_phoenix_batch(payload: dict[str, Any]) -> tuple[list[SequenceWindow], np.ndarray | None]:
    obs = np.asarray(payload.get("obs"), dtype=np.float32)
    if obs.size == 0:
        return [], None
    actions = np.asarray(payload.get("actions"), dtype=np.int64)
    active = np.asarray(payload.get("active_masks"), dtype=bool)
    rewards = np.asarray(payload.get("rewards"), dtype=np.float32)
    dones = np.asarray(payload.get("dones"), dtype=np.float32)
    if obs.ndim < 3 or actions.ndim < 3 or active.ndim < 3:
        raise ValueError(
            "PHOENIX phoenix_batch имеет неверные ранги массивов. "
            "Где: unpack_phoenix_batch. Что делать: проверьте actor_batch_send и версию протокола."
        )
    batch = int(obs.shape[0])
    if actions.shape[0] != batch or active.shape[0] != batch or rewards.shape[0] != batch or dones.shape[0] != batch:
        raise ValueError(
            "PHOENIX phoenix_batch имеет несовпадающий batch dimension. "
            "Где: unpack_phoenix_batch. Что делать: перезапустите ПК2-акторов с актуальным кодом."
        )
    windows = [
        SequenceWindow(obs[i], actions[i], active[i], rewards[i].astype(np.float32), dones[i].astype(np.float32))
        for i in range(batch)
    ]
    priority = payload.get("priority")
    if priority is None:
        return windows, None
    return windows, np.asarray(priority, dtype=np.float32)


def phoenix_sync_path() -> str:
    return os.path.join(_actor_sync_dir(), PHOENIX_SYNC_WEIGHTS_NAME)


def atomic_save_phoenix_sync(payload: dict[str, Any], path: str | None = None, *, save_fn: Callable | None = None) -> str:
    path = str(path or phoenix_sync_path())
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    tmp = f"{path}.tmp"
    saver = save_fn
    if saver is None:
        import torch

        saver = torch.save
    saver(payload, tmp)
    os.replace(tmp, path)
    return path


class PhoenixRemoteDataQ:
    """mp.Queue-compatible shim for PC2 PHOENIX actors."""

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
