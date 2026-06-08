# DQN Distributed Actors Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Подключить ПК2 как дополнительную фабрику опыта для DQN — actors на ПК2 шлют переходы по LAN в общий PER-replay learner'а на ПК1 (паттерн Ape-X).

**Architecture:** Переиспользуем существующий distributed-транспорт AlphaZero (`az_rollout_protocol`/`az_rollout_receiver`/`az_rollout_sink`). DQN-актор уже умеет писать в `data_q` через `.put((kind, payload))` и синкать веса через файл `actor_sync/latest_policy.pth`. Добавляем: (1) поддержку kind `"batch"` в общем транспорте, (2) шим `RemoteDataQ` (mp.Queue-совместимый, PUSH по ZMQ), (3) `RolloutReceiver` в DQN-learner под флагом, (4) PC2-скрипт акторов, (5) флаг в GUI + док.

**Tech Stack:** Python 3.12, PyZMQ, msgpack, numpy, PyTorch, PySide6/QML (GUI).

**Спека:** `docs/superpowers/specs/2026-06-08-dqn-distributed-actors-design.md`

**Ключевые факты кодовой базы (проверены):**
- Потребитель learner для `"batch"`: `train.py:6743-6755` — итерирует `payload` как список 6-кортежей `(s_np, a_list, r_sum, ns_np, done_flag, n_count)` → `memory.push(state_t, action_t, next_state_t, reward_t, int(n_count), None)`.
- Актор-энтри: `_actor_learner_actor_entry(actor_idx, episodes, roster_config, b_len, b_hei, n_observations, n_actions, init_weights, batch_send, clip_reward_min, clip_reward_max, clip_reward_enabled, data_q, opponent_spec, opponent_eps, self_play_enabled)` — `train.py:7582`. Пишет `data_q.put(("batch", buf))`, `("ep", dict)`, `("done", int)`, `("error", str)`.
- Транспорт: `make_rollout_sink(mode="remote", ...)` → `RemoteRolloutSink` (ZMQ PUSH, шлёт `hello` в конструкторе). `RemoteRolloutSink.put(kind, payload)` сейчас обрабатывает только dict-payload для `rollout`/`ep`/`error` и **молча игнорирует** `"batch"` (`az_rollout_sink.py:339-350`).
- `RolloutReceiver._handle_message` (`az_rollout_receiver.py:125`) дропает любой kind кроме `hello/heartbeat/error/rollout/ep`.
- Net-sync актора: читает `MODELS_DIR/actor_sync/latest_policy.pth` по mtime (`train.py:7652-7664`), формат `{"state_dict": ...}`.

---

## File Structure

**Создаём:**
- `core/models/dqn_dist.py` — DQN-specific оркестрация: stop-flag/контекст-файл с именами `dqn_dist_*`, шим `RemoteDataQ`. Транспорт (wire/receiver/sink) НЕ дублируем.
- `tools/pc2_dqn_actors.py` — PC2 entrypoint: спавн N акторов с `RemoteDataQ`.
- `tools/pc2_dqn_actors.bat` — однокнопочный запуск на ПК2.
- `runtime/state/pc2_dqn_actors_config.bat` — конфиг ПК2 (host/port/auth/workers).
- `docs/pc2-dqn-actors-setup-guide.md` — пошаговый гайд.
- Тесты: `tests/models/test_dqn_remote_sink_roundtrip.py`, `tests/models/test_dqn_dist_priority_optional.py`, `tests/models/test_dqn_dist_contract_guard.py`.

**Модифицируем:**
- `core/models/az_rollout_sink.py` — `RemoteRolloutSink.put`: добавить kind `"batch"`.
- `core/models/az_rollout_receiver.py` — `_handle_message`: принять kind `"batch"`.
- `train.py` — `_main_actor_learner`: receiver под флагом, контекст/стартовые веса, обработка remote `"batch"`-dict, stop-flag при завершении.
- `app/gui_qt/dqn_hyperparams_defaults.py` (или аналог секции `dqn`) — флаг `distributed_actors_enabled` + host/port/auth.

---

## Task 1: Транспорт учится kind "batch" (sink-сторона)

**Files:**
- Modify: `core/models/az_rollout_sink.py:339-350` (`RemoteRolloutSink.put`)
- Test: `tests/models/test_dqn_remote_sink_roundtrip.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_dqn_remote_sink_roundtrip.py
"""DQN dist: 'batch' проходит encode→decode и сохраняет форму 6-кортежей."""
import numpy as np

from core.models.az_rollout_protocol import (
    build_wire_message,
    encode_rollout_message,
    decode_rollout_message,
    validate_wire_message,
)


def _make_batch():
    s = np.arange(4, dtype=np.float32)
    ns = np.arange(4, dtype=np.float32) + 1.0
    # (s_np, a_list, r_sum, ns_np, done_flag, n_count)
    return [
        (s, [1, 0, 2], 0.5, ns, False, 3),
        (s, [0, 0, 0], -1.0, None, True, 1),
    ]


def test_batch_wire_roundtrip_preserves_tuples():
    batch = _make_batch()
    payload = {"worker_id": 7, "steps": batch, "priority": None}
    wire = build_wire_message(kind="batch", payload=payload, auth_token="tok")
    raw = encode_rollout_message(wire)
    decoded = decode_rollout_message(raw)
    kind, got = validate_wire_message(decoded, auth_token="tok")
    assert kind == "batch"
    steps = got["steps"]
    assert len(steps) == 2
    s_np, a_list, r_sum, ns_np, done_flag, n_count = steps[0]
    assert list(np.asarray(s_np, dtype=np.float32)) == [0.0, 1.0, 2.0, 3.0]
    assert list(a_list) == [1, 0, 2]
    assert abs(float(r_sum) - 0.5) < 1e-6
    assert ns_np is not None
    assert int(n_count) == 3
    # второй переход — терминальный, next_state=None
    assert steps[1][3] is None
    assert bool(steps[1][4]) is True
```

- [ ] **Step 2: Run test to verify it passes (протокол уже поддерживает numpy)**

Run: `python -m pytest tests/models/test_dqn_remote_sink_roundtrip.py -v`
Expected: PASS (этот тест проверяет только wire-протокол; он уже умеет numpy через `_encode_value/_decode_value`). Если FAIL — значит протокол не кодирует numpy/None в кортежах; тогда чинить в этом же шаге не нужно — переходи к Step 3, тест останется зелёным.

- [ ] **Step 3: Add 'batch' handling to RemoteRolloutSink.put**

В `core/models/az_rollout_sink.py`, метод `RemoteRolloutSink.put` (сейчас):

```python
    def put(self, kind: str, payload: Any) -> None:
        if kind == "done":
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
```

Заменить на (добавлен ранний разбор `"batch"` с list-payload):

```python
    def put(self, kind: str, payload: Any) -> None:
        if kind == "done":
            return
        if kind == "batch":
            # DQN: payload — голый список 6-кортежей (как в локальном data_q).
            steps = payload.get("steps") if isinstance(payload, dict) else payload
            wrapped = {
                "worker_id": int(self._worker_id),
                "steps": list(steps or []),
                "priority": (payload.get("priority") if isinstance(payload, dict) else None),
                "source": self._source,
            }
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
```

- [ ] **Step 4: Run the roundtrip test again**

Run: `python -m pytest tests/models/test_dqn_remote_sink_roundtrip.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add core/models/az_rollout_sink.py tests/models/test_dqn_remote_sink_roundtrip.py
git commit -m "feat(train): RemoteRolloutSink поддерживает kind=batch (DQN dist)"
```

---

## Task 2: Receiver принимает kind "batch"

**Files:**
- Modify: `core/models/az_rollout_receiver.py:121-135` (`_handle_message`)
- Test: `tests/models/test_dqn_dist_contract_guard.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_dqn_dist_contract_guard.py
"""DQN dist: receiver кладёт 'batch' в очередь и дропает чужой env_contract_hash."""
import queue

from core.models.az_rollout_receiver import RolloutReceiver
from core.models.az_rollout_protocol import (
    build_wire_message,
    encode_rollout_message,
)


def _batch_wire(hash_val: str):
    payload = {"worker_id": 1, "steps": [], "priority": None, "env_contract_hash": hash_val}
    wire = build_wire_message(kind="batch", payload=payload, auth_token="")
    return encode_rollout_message(wire)


def test_batch_enqueued_when_hash_matches():
    q: queue.Queue = queue.Queue()
    rcv = RolloutReceiver(q, expected_contract_hash="H1")
    rcv._handle_message(_batch_wire("H1"))
    kind, payload = q.get_nowait()
    assert kind == "batch"
    assert payload["source"] == "remote"


def test_batch_dropped_when_hash_mismatch():
    q: queue.Queue = queue.Queue()
    rcv = RolloutReceiver(q, expected_contract_hash="H1")
    rcv._handle_message(_batch_wire("H2"))
    assert q.empty()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_dqn_dist_contract_guard.py -v`
Expected: FAIL — `test_batch_enqueued_when_hash_matches` падает (queue пустая), т.к. `_handle_message` дропает kind `"batch"` на проверке `if kind not in ("rollout", "ep"): return`.

- [ ] **Step 3: Add 'batch' to accepted kinds**

В `core/models/az_rollout_receiver.py`, метод `_handle_message`, строка:

```python
        if kind not in ("rollout", "ep"):
            return
```

заменить на:

```python
        if kind not in ("rollout", "ep", "batch"):
            return
```

И ниже, блок счётчиков:

```python
        if kind == "rollout":
            self._received_rollouts += 1
        elif kind == "ep":
            self._received_eps += 1
```

заменить на:

```python
        if kind in ("rollout", "batch"):
            self._received_rollouts += 1
        elif kind == "ep":
            self._received_eps += 1
```

(`env_contract_hash` для `"batch"` уже проверяется в `validate_wire_message`, т.к. там условие `kind in ("hello", "rollout")` — добавить `"batch"` туда тоже.)

В `core/models/az_rollout_protocol.py`, `validate_wire_message`, строка:

```python
    if expected_contract_hash and kind in ("hello", "rollout"):
```

заменить на:

```python
    if expected_contract_hash and kind in ("hello", "rollout", "batch"):
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/models/test_dqn_dist_contract_guard.py -v`
Expected: PASS (оба теста)

- [ ] **Step 5: Commit**

```bash
git add core/models/az_rollout_receiver.py core/models/az_rollout_protocol.py tests/models/test_dqn_dist_contract_guard.py
git commit -m "feat(train): RolloutReceiver принимает kind=batch + contract guard (DQN dist)"
```

---

## Task 3: Модуль dqn_dist (RemoteDataQ + stop/context хелперы)

**Files:**
- Create: `core/models/dqn_dist.py`
- Test: `tests/models/test_dqn_dist_priority_optional.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_dqn_dist_priority_optional.py
"""DQN dist: RemoteDataQ.put((kind,payload)) → sink.put(kind,payload); priority опционален."""
from core.models.dqn_dist import RemoteDataQ


class _SpySink:
    def __init__(self):
        self.calls = []

    def put(self, kind, payload):
        self.calls.append((kind, payload))

    def close(self):
        self.calls.append(("__closed__", None))


def test_remote_dataq_forwards_batch_tuple():
    sink = _SpySink()
    q = RemoteDataQ(sink)
    batch = [("s", [1], 0.0, None, True, 1)]
    q.put(("batch", batch))
    assert sink.calls == [("batch", batch)]


def test_remote_dataq_forwards_ep_and_done():
    sink = _SpySink()
    q = RemoteDataQ(sink)
    q.put(("ep", {"result": "win"}))
    q.put(("done", 3))
    assert sink.calls[0] == ("ep", {"result": "win"})
    assert sink.calls[1] == ("done", 3)


def test_remote_dataq_close_closes_sink():
    sink = _SpySink()
    q = RemoteDataQ(sink)
    q.close()
    assert ("__closed__", None) in sink.calls
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_dqn_dist_priority_optional.py -v`
Expected: FAIL — `ModuleNotFoundError: core.models.dqn_dist`.

- [ ] **Step 3: Create core/models/dqn_dist.py**

```python
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


def dqn_dist_stop_flag_path() -> str:
    custom = str(os.getenv("DQN_DIST_STOP_FLAG_PATH", "") or "").strip()
    if custom:
        return custom
    root = os.getenv("MODELS_DIR", os.path.join(os.getcwd(), "artifacts", "models"))
    return os.path.join(root, "actor_sync", "dqn_dist_stop.flag")


def dqn_dist_stop_requested(flag_path: str | None = None) -> bool:
    path = str(flag_path or dqn_dist_stop_flag_path())
    return bool(path) and os.path.isfile(path)


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
        with open(path, "r", encoding="utf-8") as handle:
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/models/test_dqn_dist_priority_optional.py -v`
Expected: PASS (3 теста)

- [ ] **Step 5: Commit**

```bash
git add core/models/dqn_dist.py tests/models/test_dqn_dist_priority_optional.py
git commit -m "feat(train): модуль dqn_dist (RemoteDataQ + stop/context хелперы)"
```

---

## Task 4: RolloutReceiver в DQN-learner (ПК1)

**Files:**
- Modify: `train.py` — `_main_actor_learner` (вставки около `data_q` создания ~6487, обработки `"batch"` ~6743, и завершения цикла ~6543/после while)
- Modify: `train.py` — секция флагов DQN (рядом с другими `os.getenv`, см. ниже)

**Контекст:** В `_main_actor_learner` есть `data_q = ctx.Queue(...)`, спавн локальных акторов, и цикл `while done_actors < num_actors`. Receiver кладёт remote-сообщения в тот же `data_q`. Remote `"batch"` приходит как dict `{"steps":[...], "priority":..., "source":"remote"}`, локальный — как голый список. Обработчик `"batch"` должен принять оба.

- [ ] **Step 1: Добавить флаги DQN-dist (рядом с DQN-env-флагами в train.py)**

Найди блок DQN-флагов (около `TRAIN_ALGO`, `REPLAY_CAPACITY` и т.п. в начале train.py — например после строки с `NUM_ACTORS`/`ACTOR_*`). Добавь:

```python
# --- Distributed DQN actors (ПК2 → rollout ZMQ → learner data_q) ---
DQN_DISTRIBUTED_ACTORS = os.getenv("DQN_DISTRIBUTED_ACTORS", "0").strip() in {"1", "true", "yes"}
DQN_DIST_ROLLOUT_PORT = int(os.getenv("DQN_DIST_ROLLOUT_PORT", "5558"))
DQN_DIST_BIND_HOST = str(os.getenv("DQN_DIST_BIND_HOST", "0.0.0.0"))
DQN_DIST_AUTH_TOKEN = str(os.getenv("DQN_DIST_AUTH_TOKEN", ""))
DQN_DIST_ZMQ_HWM = max(8, int(os.getenv("DQN_DIST_ZMQ_HWM", "256")))
```

- [ ] **Step 2: Импорт хелперов dqn_dist в начале train.py**

Рядом с `from core.models.az_rollout_receiver import RolloutReceiver` (`train.py:93`) добавь:

```python
from core.models.dqn_dist import (
    touch_dqn_dist_stop_flag,
    write_dqn_dist_train_context,
)
```

- [ ] **Step 3: Поднять receiver + записать train-context и стартовые веса**

В `_main_actor_learner`, сразу ПОСЛЕ создания `data_q` (строка `data_q: mp.Queue = ctx.Queue(maxsize=queue_max)`) и ДО спавна локальных акторов, вставь:

```python
        # --- Distributed actors (ПК2): receiver + SMB train-context ---
        rollout_receiver = None
        if DQN_DISTRIBUTED_ACTORS:
            env_contract_hash = str(env_contract.get("contract_hash", "") or "")
            rollout_receiver = RolloutReceiver(
                data_q,
                bind_host=DQN_DIST_BIND_HOST,
                bind_port=DQN_DIST_ROLLOUT_PORT,
                expected_contract_hash=env_contract_hash,
                auth_token=DQN_DIST_AUTH_TOKEN,
                zmq_hwm=DQN_DIST_ZMQ_HWM,
                log_fn=append_agent_log,
            )
            rollout_receiver.start()
            # Стартовые веса для ПК2 (тот же файл, что и локальный actor-sync).
            try:
                torch.save({"state_dict": init_weights}, sync_path)
            except Exception as exc:
                append_agent_log(f"[DQN][DIST][WARN] не удалось записать стартовые веса {sync_path}: {exc}")
            try:
                write_dqn_dist_train_context({
                    "env_contract_hash": env_contract_hash,
                    "opponent_agent_id": str(OPPONENT_AGENT_ID or ""),
                    "learner_side": str(learner_side_cfg),
                    "n_observations": int(n_observations),
                    "n_actions": list(n_actions),
                    "rollout_port": int(DQN_DIST_ROLLOUT_PORT),
                    "mission": str(normalize_mission_name(roster_config.get("mission", DEFAULT_MISSION_NAME))),
                })
            except Exception as exc:
                append_agent_log(f"[DQN][DIST][WARN] не удалось записать train-context: {exc}")
            append_agent_log(
                f"[DQN][DIST] receiver bind=:{DQN_DIST_ROLLOUT_PORT} "
                f"contract_hash={env_contract_hash or '-'} sync={sync_path}"
            )
```

Примечание: `sync_path` определяется ниже по коду (строка `sync_path = os.path.join(MODELS_DIR, "actor_sync", "latest_policy.pth")`). Перенеси определение `sync_path` и `os.makedirs(...)` ВЫШЕ — до этого вставленного блока (т.е. сразу после `init_weights = {...}`), чтобы `sync_path` был доступен.

- [ ] **Step 4: Обработка remote "batch"-dict в потребителе**

В цикле `while done_actors < num_actors`, блок (`train.py:6743-6746`):

```python
        if kind != "batch":
            continue

        for (s_np, a_list, r_sum, ns_np, done_flag, n_count) in payload:
```

заменить на:

```python
        if kind != "batch":
            continue

        # Локальный actor шлёт голый список; remote (ПК2) — dict {"steps":..,"priority":..}.
        if isinstance(payload, dict):
            batch_steps = payload.get("steps", []) or []
            # MVP: priority принимается, но не применяется (learner-side max_priority).
            # Точка расширения под actor-side Ape-X (DQN_DIST_ACTOR_PRIORITY).
            _remote_priority = payload.get("priority", None)  # noqa: F841
        else:
            batch_steps = payload

        for (s_np, a_list, r_sum, ns_np, done_flag, n_count) in batch_steps:
```

- [ ] **Step 5: Остановить ПК2 и receiver при завершении прогона**

Найди конец `_main_actor_learner` — после выхода из `while done_actors < num_actors` (там, где actors завершились и идёт финализация/сохранение). Добавь ПЕРЕД return/в начале финализации:

```python
        if DQN_DISTRIBUTED_ACTORS:
            try:
                stop_path = touch_dqn_dist_stop_flag()
                append_agent_log(f"[DQN][DIST] stop.flag записан: {stop_path}")
            except Exception as exc:
                append_agent_log(f"[DQN][DIST][WARN] не удалось записать stop.flag: {exc}")
            if rollout_receiver is not None:
                try:
                    rollout_receiver.stop()
                except Exception:
                    pass
```

**Заметка по логам:** переиспользуемый `RolloutReceiver` пишет с префиксом `[AZ][DIST][RECEIVER]` (хардкод в `az_rollout_receiver.py`), и видимость удалённых воркеров (hello/heartbeat, `received_rollouts`, `dropped_contract`) идёт через эти строки + summary при `stop()`. Для DQN это даёт `[AZ]`-префикс в TRAIN-логах — допустимо для MVP (транспорт общий). Если на ревью потребуют — вынести префикс в параметр `log_prefix` конструктора receiver отдельной задачей (затронет и AZ). Не делать в этом плане.

- [ ] **Step 6: Smoke-проверка импорта и синтаксиса**

Run: `python -c "import train"`
Expected: импорт без ошибок (модуль грузится; флаги DQN_DIST_* доступны).

- [ ] **Step 7: Commit**

```bash
git add train.py
git commit -m "feat(train): RolloutReceiver + SMB train-context в DQN-learner (ПК1, dist)"
```

---

## Task 5: PC2 entrypoint — tools/pc2_dqn_actors.py

**Files:**
- Create: `tools/pc2_dqn_actors.py`

**Контекст:** Аналог `tools/pc2_az_actors.py`, но проще (нет MCTS/IS). Каждый воркер: строит env → определяет n_obs/n_actions → грузит веса с SMB → опционально opponent → конструирует `RemoteDataQ(make_rollout_sink(mode="remote", ...))` → зовёт `_actor_learner_actor_entry(...)`.

- [ ] **Step 1: Create tools/pc2_dqn_actors.py**

```python
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
    dqn_dist_stop_flag_path,
    dqn_dist_stop_requested,
    wait_dqn_dist_train_context,
)


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return int(default)


def _worker_main(worker_id: int, ctx_json: str) -> None:
    import json

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

    roster = train_mod._load_roster_config()
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
    sync_path = os.path.join(os.getenv("MODELS_DIR", os.path.join(os.getcwd(), "artifacts", "models")), "actor_sync", "latest_policy.pth")
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
        init_weights = {k: v.detach().cpu().clone() for k, v in train_mod.normalize_state_dict(tmp_net.state_dict()).items()}

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
        f"[DQN][DIST][PC2] worker={worker_id} → {host}:{port} "
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

    wait_sec = max(0.0, float(os.getenv("DQN_DIST_WAIT_CONTEXT_SEC", "0") or 0.0))
    ctx = wait_dqn_dist_train_context(wait_sec=wait_sec)
    if ctx.get("opponent_agent_id"):
        os.environ.setdefault("OPPONENT_AGENT_ID", str(ctx["opponent_agent_id"]))
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
```

- [ ] **Step 2: Проверить вспомогательные функции существуют**

Run: `python -c "import train; assert hasattr(train, 'action_sizes_from_env'); assert hasattr(train, '_build_units_from_config'); assert hasattr(train, '_load_roster_config'); assert hasattr(train, 'normalize_state_dict'); print('ok')"`
Expected: `ok`. Если какой-то функции нет под этим именем — найди фактическое имя в `train.py` (grep `def action_sizes_from_env`, `def _build_units_from_config`, `def _load_roster_config`) и поправь вызовы в скрипте.

- [ ] **Step 3: Smoke-импорт скрипта**

Run: `python -c "import importlib.util, pathlib; spec=importlib.util.spec_from_file_location('pc2_dqn_actors', 'tools/pc2_dqn_actors.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print('import ok')"`
Expected: `import ok` (модуль грузится; main не вызывается).

- [ ] **Step 4: Commit**

```bash
git add tools/pc2_dqn_actors.py
git commit -m "feat(tools): ПК2 entrypoint pc2_dqn_actors (DQN distributed)"
```

---

## Task 6: Локальный self-connect smoke-тест (без ПК2)

**Files:**
- Test: `tests/models/test_dqn_dist_self_connect.py`

**Цель:** Проверить полный путь sink→receiver→data_q на 127.0.0.1 без обучения и без живого ПК2.

- [ ] **Step 1: Write the test**

```python
# tests/models/test_dqn_dist_self_connect.py
"""DQN dist smoke: RemoteRolloutSink PUSH → RolloutReceiver PULL → data_q (127.0.0.1)."""
import queue
import time

import numpy as np
import pytest

from core.models.az_rollout_receiver import RolloutReceiver
from core.models.az_rollout_sink import make_rollout_sink
from core.models.dqn_dist import RemoteDataQ

zmq = pytest.importorskip("zmq")


def test_batch_flows_sink_to_receiver():
    port = 5599
    q: queue.Queue = queue.Queue()
    rcv = RolloutReceiver(q, bind_host="127.0.0.1", bind_port=port, auth_token="t")
    rcv.start()
    time.sleep(0.3)  # дать PULL забиндиться
    try:
        sink = make_rollout_sink(
            mode="remote", source="remote", remote_host="127.0.0.1",
            remote_port=port, auth_token="t", worker_id=42, env_contract_hash="",
        )
        rq = RemoteDataQ(sink)
        s = np.arange(3, dtype=np.float32)
        rq.put(("batch", [(s, [1, 0, 0], 0.5, s, False, 2)]))
        # дождаться доставки
        got_kind = None
        got_payload = None
        deadline = time.time() + 5.0
        while time.time() < deadline:
            try:
                got_kind, got_payload = q.get(timeout=0.5)
                if got_kind == "batch":
                    break
            except queue.Empty:
                continue
        assert got_kind == "batch"
        assert isinstance(got_payload, dict)
        steps = got_payload["steps"]
        assert len(steps) == 1
        assert int(steps[0][5]) == 2
        rq.close()
    finally:
        rcv.stop()
```

- [ ] **Step 2: Run the test**

Run: `python -m pytest tests/models/test_dqn_dist_self_connect.py -v`
Expected: PASS (если `pyzmq` установлен; иначе skip). Если flaky по таймингу bind — увеличь `time.sleep(0.3)` до `0.6`.

- [ ] **Step 3: Commit**

```bash
git add tests/models/test_dqn_dist_self_connect.py
git commit -m "test(train): self-connect smoke для DQN distributed (sink→receiver)"
```

---

## Task 7: .bat запуск + конфиг на ПК2

**Files:**
- Create: `runtime/state/pc2_dqn_actors_config.bat`
- Create: `tools/pc2_dqn_actors.bat`

- [ ] **Step 1: Create runtime/state/pc2_dqn_actors_config.bat**

```bat
@echo off
REM === Конфиг ПК2 для DQN distributed actors ===
REM IP ПК1 (learner) — куда слать переходы:
set DQN_DIST_PC1_HOST=192.168.1.10
REM Порт rollout (должен совпадать с ПК1, по умолчанию 5558):
set DQN_DIST_ROLLOUT_PORT=5558
REM Общий секрет (должен совпадать с ПК1; пусто = без auth):
set DQN_DIST_AUTH_TOKEN=
REM Число актор-процессов на ПК2 (по числу ядер CPU, напр. 6 для Ryzen 1600):
set DQN_DIST_PC2_NUM_WORKERS=6
REM SMB-шара ПК1 с моделью (actor_sync лежит здесь): \\PC1\40kai_models
set MODELS_DIR=\\PC1\40kai_models
REM Сколько ждать train-context от ПК1 (сек):
set DQN_DIST_WAIT_CONTEXT_SEC=120
REM Self-play (1 — если ПК1 учит с оппонентом-снапшотом):
set SELF_PLAY_ENABLED=0
```

- [ ] **Step 2: Create tools/pc2_dqn_actors.bat**

```bat
@echo off
setlocal
cd /d "%~dp0\.."
call "runtime\state\pc2_dqn_actors_config.bat"
echo [DQN][DIST][PC2] PC1=%DQN_DIST_PC1_HOST%:%DQN_DIST_ROLLOUT_PORT% workers=%DQN_DIST_PC2_NUM_WORKERS% MODELS_DIR=%MODELS_DIR%
python tools\pc2_dqn_actors.py
endlocal
```

- [ ] **Step 3: Commit**

```bash
git add runtime/state/pc2_dqn_actors_config.bat tools/pc2_dqn_actors.bat
git commit -m "feat(tools): .bat + конфиг запуска DQN actors на ПК2"
```

---

## Task 8: Флаг в GUI (секция DQN hyperparams)

**Files:**
- Modify: `app/gui_qt/algo_hyperparams_defaults.py` — `DQN_HYPERPARAM_KEYS` (стр. 18-36) и `DEFAULT_DQN_HYPERPARAMS` (стр. 38-65)
- Modify: `app/gui_qt/main.py:5008-5013` — блок `env_overrides.setdefault(...)` для actor-learner

**Контекст:** DQN-параметры хранятся в `DEFAULT_DQN_HYPERPARAMS`, перечислены в `DQN_HYPERPARAM_KEYS`. Actor-learner-knobs пробрасываются в окружение train через `env_overrides.setdefault(...)` в `main.py` (около стр. 5008-5013, рядом с `NUM_ACTORS`/`ACTOR_BATCH_SEND`). Distributed-флаг — такой же actor-learner-knob.

- [ ] **Step 1: Добавить ключи в DQN_HYPERPARAM_KEYS**

В `app/gui_qt/algo_hyperparams_defaults.py`, в конец кортежа `DQN_HYPERPARAM_KEYS` (перед закрывающей `)` на стр. 36, после `"per_ensemble_priority_lambda",`) добавь:

```python
    "distributed_actors_enabled",
    "distributed_rollout_port",
    "distributed_auth_token",
```

- [ ] **Step 2: Добавить значения в DEFAULT_DQN_HYPERPARAMS**

В `DEFAULT_DQN_HYPERPARAMS`, перед закрывающей `}` (после `"per_ensemble_priority_lambda": 0.1,` на стр. 64) добавь:

```python
    "distributed_actors_enabled": 0,
    "distributed_rollout_port": 5558,
    "distributed_auth_token": "",
```

- [ ] **Step 3: Пробросить флаги в env_overrides (main.py)**

В `app/gui_qt/main.py`, сразу ПОСЛЕ строки `env_overrides.setdefault("ACTOR_QUEUE_MAX", "256")` (стр. 5013) добавь. `dqn_hp` — словарь DQN-секции hyperparams; если в этой функции он называется иначе, используй фактический источник DQN-полей (тот же, из которого берутся остальные dqn-параметры выше по функции):

```python
        # Distributed DQN actors (ПК2): включаем receiver на ПК1, если выставлено в GUI.
        try:
            _dqn_hp = self._load_algo_hyperparams("dqn") if hasattr(self, "_load_algo_hyperparams") else {}
        except Exception:
            _dqn_hp = {}
        if int(_dqn_hp.get("distributed_actors_enabled", 0) or 0) == 1:
            env_overrides["DQN_DISTRIBUTED_ACTORS"] = "1"
            env_overrides.setdefault("DQN_DIST_ROLLOUT_PORT", str(_dqn_hp.get("distributed_rollout_port", 5558)))
            env_overrides.setdefault("DQN_DIST_AUTH_TOKEN", str(_dqn_hp.get("distributed_auth_token", "") or ""))
```

Примечание: имя загрузчика `_load_algo_hyperparams` — ориентир. Найди фактический способ чтения DQN-секции в этой функции (grep `"dqn"` / `hyperparams` в окрестности `_start_training` в main.py) и используй его. Цель — прочитать `distributed_actors_enabled` из сохранённого DQN-конфига.

- [ ] **Step 4: Smoke — дефолты и GUI грузятся**

Run: `python -c "from app.gui_qt.algo_hyperparams_defaults import DEFAULT_DQN_HYPERPARAMS, DQN_HYPERPARAM_KEYS; assert 'distributed_actors_enabled' in DEFAULT_DQN_HYPERPARAMS; assert 'distributed_actors_enabled' in DQN_HYPERPARAM_KEYS; print('ok')"`
Expected: `ok`

- [ ] **Step 5: Commit**

```bash
git add app/gui_qt/algo_hyperparams_defaults.py app/gui_qt/main.py
git commit -m "feat(gui): флаг distributed_actors для DQN (ПК1 receiver)"
```

---

## Task 9: Док-гайд + регрессионное ревью

**Files:**
- Create: `docs/pc2-dqn-actors-setup-guide.md`

- [ ] **Step 1: Create docs/pc2-dqn-actors-setup-guide.md**

```markdown
# ПК2: DQN distributed actors — пошаговый запуск

## Что это
ПК2 (Ryzen 1600 + RTX 2060S) генерит опыт DQN и шлёт переходы по LAN в общий
PER-replay learner'а на ПК1. Узкое место (CPU/env throughput) масштабируется.

## Предусловия
- На ПК1 и ПК2 один и тот же код репозитория и `requirements_windows.txt`.
- SMB-шара ПК1 с `artifacts/models` смонтирована/доступна на ПК2 (напр. `\\PC1\40kai_models`).
- Один и тот же ростер/миссия (иначе `env_contract_hash` не сойдётся — переходы дропнутся).

## Шаги
1. **ПК1:** в Qt GUI вкладка DQN → включи `distributed_actors_enabled`, задай порт (5558)
   и auth-token (опц.). Запусти train. Learner поднимет receiver :5558 и запишет
   `actor_sync/dqn_dist_train_context.json` + `latest_policy.pth` на SMB.
2. **ПК2:** правь `runtime/state/pc2_dqn_actors_config.bat`:
   - `DQN_DIST_PC1_HOST` = IP ПК1,
   - `DQN_DIST_ROLLOUT_PORT` = 5558 (как на ПК1),
   - `DQN_DIST_AUTH_TOKEN` = тот же, что на ПК1,
   - `DQN_DIST_PC2_NUM_WORKERS` = число ядер (6),
   - `MODELS_DIR` = путь к SMB-шаре ПК1.
3. **ПК2:** запусти `tools\pc2_dqn_actors.bat`.

## Проверка
- ПК1-лог `[DQN][DIST] receiver bind=:5558 ...` и далее рост `received_rollouts`.
- ПК2-лог `[DQN][DIST][PC2] worker=... → IP:5558 ...`.
- Если `drop invalid message` / `env_contract_hash mismatch` — ростер/миссия/ruleset
  на ПК1≠ПК2. Синхронизируй конфиг.

## Остановка
ПК1 по завершении прогона пишет `actor_sync/dqn_dist_stop.flag` — ПК2-воркеры
сами завершатся. Можно также закрыть окно `pc2_dqn_actors.bat`.

## Порты
- DQN dist rollout — **5558** (отдельно от AZ dist :5557 и remote-IS :5555).
```

- [ ] **Step 2: Прогнать все новые тесты разом**

Run: `python -m pytest tests/models/test_dqn_remote_sink_roundtrip.py tests/models/test_dqn_dist_contract_guard.py tests/models/test_dqn_dist_priority_optional.py tests/models/test_dqn_dist_self_connect.py -v`
Expected: все PASS (self_connect может skip без pyzmq).

- [ ] **Step 3: Регрессионное ревью транспорта (AZ не сломан)**

Поскольку Task 1-2 трогают общий `az_rollout_*`, запусти существующие AZ-dist тесты (если есть) и вызови субагента `engine-regression-reviewer` или `code-reviewer` на диффе.

Run: `python -m pytest tests/ -k "rollout or dist or az_inference" -v`
Expected: без новых падений (AZ-поведение не изменилось — `"batch"` для AZ не используется, изменения аддитивные).

- [ ] **Step 4: Commit**

```bash
git add docs/pc2-dqn-actors-setup-guide.md
git commit -m "docs: гайд запуска DQN distributed actors на ПК2"
```

---

## Готовность / приёмка

- [ ] ПК1 с `DQN_DISTRIBUTED_ACTORS=1` стартует, пишет context+веса на SMB, держит receiver :5558.
- [ ] ПК2 `pc2_dqn_actors.bat` коннектится, шлёт `batch`, ПК1 их вставляет в replay (рост `global_step`).
- [ ] Несовпадение контракта → переходы дропаются с понятным логом, learner не падает.
- [ ] Завершение прогона → `dqn_dist_stop.flag` → ПК2 останавливается.
- [ ] Все новые юнит-тесты зелёные; AZ-dist не задет.

## Вне рамок (YAGNI)
- Actor-side TD-error (честный Ape-X) — протокол готов (`priority`), реализация позже под `DQN_DIST_ACTOR_PRIORITY`.
- PPO/AZ proxy distributed.
- Несколько ПК2 одновременно.
