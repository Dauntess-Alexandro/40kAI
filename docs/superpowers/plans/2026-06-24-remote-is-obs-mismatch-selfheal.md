# Remote IS obs-мисматч self-heal — Implementation Plan

> REQUIRED SUB-SKILL: superpowers:executing-plans. Steps — checkbox `- [ ]`.

**Goal:** Авто-republish search_cfg на шару при несовпадении obs_dim (+ удалить устаревшие веса); сервер при obs-мисматче запроса даёт понятную ошибку и не падает.

**Tech Stack:** Python 3.12, pytest.

## Global Constraints
- RU-сообщения (что/где/что делать). TDD. ruff чист. Коммит только релевантного кода.
- Не трогать формат cfg/протокол, in-process серверы, переобучение.

---

### Task 1: Хелпер сообщения `obs_dim_mismatch_message`

**Files:** `core/engine/phases/obs_features.py`; test `tests/engine/test_obs_dim_mismatch_message.py`

- [ ] Step 1 — тест: `obs_dim_mismatch_message(41,41) is None`; `obs_dim_mismatch_message(17,41)` → строка содержит "17","41","search_cfg".
- [ ] Step 2 — запустить (FAIL).
- [ ] Step 3 — реализовать:
```python
def obs_dim_mismatch_message(expected: int, actual: int) -> str | None:
    if int(expected) == int(actual):
        return None
    return (
        f"[REMOTE_IS] obs_dim сети={int(expected)} != запрос={int(actual)}. "
        "Перегенери search_cfg на ПК1 (tools\\write_*_remote_search_cfg.bat) и удали старые "
        "latest_*_policy.pth на шаре, затем перезапусти сервер."
    )
```
- [ ] Step 4 — PASS. Step 5 — ruff + commit.

---

### Task 2: ensure_remote_search_cfg — republish при obs-мисматче

**Files:** `core/models/remote_is_search_cfg_common.py`; test `tests/models/test_remote_is_obs_mismatch.py`

- [ ] Step 1 — тест (mock): tmp share, cfg(obs_dim=17); publish-callback пишет cfg(obs_dim=41) в target; weights-файл создан.
  - `current_obs_dim_fn=lambda:41` → action!="found" (republish), weights удалён.
  - cfg(41)+fn→41 → action=="found", weights на месте.
  - fn=None → "found".
- [ ] Step 2 — FAIL (нет параметра / нет логики).
- [ ] Step 3 — добавить:
  1. `current_env_obs_dim(sync_dir) -> int` (резолв ростера как в publish + `measure_env_dims_from_roster`; 0 при ошибке).
  2. param `current_obs_dim_fn: Callable[[], int] | None = None` в `ensure_remote_search_cfg`; в ветке found — если fn задан и `cur != cfg_obs` (оба >0): лог, `os.remove(paths.weights_path)` (try/except), провалиться в publish.
  3. читать cfg obs_dim через `read_search_cfg`/json existing.
- [ ] Step 4 — PASS. Step 5 — пробросить `current_obs_dim_fn` в ensure_gmz/smz/az/gaz билдерах (lambda → current_env_obs_dim(sync_dir)).
- [ ] Step 6 — регресс: `tests/test_*_remote_search_cfg_builder.py`, `tests/test_remote_is_search_cfg_registry.py` зелёные. ruff + commit.

---

### Task 3: Серверы (GMZ+SMZ) — проверка obs перед инференсом

**Files:** `tools/gmz_remote_inference_server.py`, `tools/smz_remote_inference_server.py`

- [ ] Step 1 — сохранить `self._obs_dim = int(obs_dim)` в `__init__` (рядом с построением net).
- [ ] Step 2 — в `_process_and_reply` ДО инференса: для каждого req измерить ширину obs; если `obs_dim_mismatch_message(self._obs_dim, w)` не None → `_log(msg)` + `_send_error(identity, msg)`, исключить из батча. Пустой батч после фильтра → return.
- [ ] Step 3 — проверка: `python -c "import ..."` оба сервера импортируются; ruff чист.
- [ ] Step 4 — commit.

---

## DoD
- Task1/2 тесты зелёные; регресс remote_search/registry не сломан; серверы импортируются; ruff чист; коммиты только код.
