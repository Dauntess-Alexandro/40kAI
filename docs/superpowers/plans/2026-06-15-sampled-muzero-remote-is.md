# Sampled MuZero — Remote Inference Server Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Дать `sampled_muzero` inference-server как у gmz (variant B: env-воркеры + GPU-сервер поиска), режимы local и remote (ПК2), GUI-панель + ПК2-обвязка + дока. По умолчанию ВЫКЛ.

**Architecture:** gmz remote-IS оффлоадит весь поиск целиком (obs+masks → selected_actions/policy/behavior/value), поэтому протокол/транспорт/клиент (`gmz_inference_{protocol,transport,client}.py`) и env-воркер (`train.py::_gmz_env_worker_entry`) **search-agnostic** и переиспользуются импортом. Уникален только сервер — новый `smz_inference_server.py` крутит `BatchedSampledMuZeroSearch`. Остальное — конфиг `SMZ_INFERENCE_*` + перенаправление уже-скопированного inference-каркаса в `_main_actor_learner_sampled_muzero` с gmz на smz, + tools/GUI/docs зеркалом.

**Tech Stack:** Python 3.12, PyTorch, NumPy, msgpack, pyzmq, pytest, PySide6/QML. Windows. Тесты на CPU.

**Спека:** `docs/superpowers/specs/2026-06-15-sampled-muzero-remote-is-design.md`.

**Дефолтный порт ПК2:** `5560` (gmz/az = 5555; не запускать конфликтующие серверы на одном ПК2/порту).

---

## Файловая структура

**Создаём:**
- `core/models/smz_inference_server.py` — `SMZInferenceServer` + `smz_inference_server_entry` (миррор `gmz_inference_server.py`, поиск = `BatchedSampledMuZeroSearch`).
- `tools/smz_remote_inference_server.py` — ПК2 standalone (миррор `tools/gmz_remote_inference_server.py`).
- `tools/pc2_remote_smz_is.bat` — ПК2 кнопка (миррор `tools/pc2_remote_is.bat`).
- `runtime/state/pc2_remote_smz_is_config.example.bat` + `runtime/state/pc2_remote_smz_is_config.example.rev` — шаблон конфига ПК2.
- `docs/remote-inference-server-smz.md`, `docs/pc2-remote-smz-is-setup-guide.md` — дока (миррор gmz-доки).
- `tests/engine/test_smz_inference_server.py` — тест сервера.

**Модифицируем:**
- `train.py` — блок `SMZ_INFERENCE_*` (заменяет нынешний простой SMZ device-блок 3176–3190); импорт `smz_inference_server_entry`; перенаправление inference-ветки в `_main_actor_learner_sampled_muzero` (GMZ_*→SMZ_*).
- `hyperparams.json` — секция `sampled_muzero`: поля inference-server.
- `app/gui_qt/sampled_muzero_hyperparams_defaults.py` — inference-ключи + тултипы.
- `app/gui_qt/main.py` — экспорт `SMZ_INFERENCE_*` env при train-launch + чтение `runtime/state/remote_is_smz.json` (миррор gmz remote_is.json).
- `app/gui_qt/qml/components/SectionHyperparamsEditor.qml` — int-поля (enabled/compile/batch_size/queue_max/num_env_workers) и панель Inference Server (миррор gmz).
- `.gitignore` — добавить `runtime/state/pc2_remote_smz_is_config.bat`, `runtime/state/remote_is_smz.json` (если gmz-аналоги там есть).

**Переиспользуем (импорт, без копий):** `gmz_inference_protocol`, `gmz_inference_transport`, `gmz_inference_client.GMZInferenceClient`, `train.py::_gmz_env_worker_entry`, `GMZTransition`, `normalize_state_dict`.

---

## Phase A — Сервер (единственная новая логика)

### Task 1: `smz_inference_server.py` + тест

**Files:**
- Create: `core/models/smz_inference_server.py`
- Test: `tests/engine/test_smz_inference_server.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/engine/test_smz_inference_server.py
import numpy as np
import torch

from core.models.sampled_muzero_model import make_sampled_muzero_net
from core.models.sampled_muzero_search import (
    BatchedSampledMuZeroSearch,
    SampledMuZeroSearchConfig,
)
from core.models.smz_inference_server import SMZInferenceServer


def _make_net(n_obs, n_actions):
    torch.manual_seed(0)
    return make_sampled_muzero_net(
        obs_dim=n_obs, action_sizes=n_actions,
        latent_dim=32, hidden_dim=32, num_layers=1, action_embed_dim=8,
    )


def _make_batch(n_obs, n_actions, n_envs, seed=7):
    rng = np.random.default_rng(seed)
    batch = []
    for env_id in range(n_envs):
        obs = rng.standard_normal(n_obs).astype(np.float32)
        masks = []
        for size in n_actions:
            m = rng.integers(0, 2, size=size).astype(bool)
            if not m.any():
                m[0] = True
            masks.append(m)
        batch.append({"env_id": env_id, "obs": obs,
                      "legal_masks_by_head": masks, "is_new_episode": True})
    return batch


def _server(net, cfg):
    import multiprocessing as mp
    ctx = mp.get_context("spawn")
    return SMZInferenceServer(
        net=net, search_config=cfg, device=torch.device("cpu"),
        request_queue=ctx.Queue(), reply_queues=[ctx.Queue() for _ in range(8)],
        sync_path="", sync_check_interval=999.0,
        inference_batch_size=8, inference_batch_interval_s=0.02,
        compile_mode=False,
    )


def test_server_build_batch_responses_contract():
    n_obs, n_actions, n_envs = 10, [4, 3], 5
    net = _make_net(n_obs, n_actions)
    cfg = SampledMuZeroSearchConfig(num_samples=16, prior_weight=0.0)
    srv = _server(net, cfg)
    batch = _make_batch(n_obs, n_actions, n_envs)
    np.random.seed(1)
    responses = srv.build_batch_responses(batch)
    assert len(responses) == n_envs
    for resp in responses:
        assert resp["kind"] == "infer_response"
        assert len(resp["selected_actions"]) == len(n_actions)
        assert len(resp["policy_targets"]) == len(n_actions)
        for h, size in enumerate(n_actions):
            p = resp["policy_targets"][h]
            assert p.shape[0] == size and abs(float(p.sum()) - 1.0) < 1e-5
            eid = int(resp["env_id"])
            assert batch[eid]["legal_masks_by_head"][h][resp["selected_actions"][h]]
        assert len(resp["behavior_logits"]) == len(n_actions)
        assert isinstance(resp["value_est"], float)
    srv.stop()


def test_server_matches_direct_sampled_search():
    n_obs, n_actions, n_envs = 10, [4, 3], 4
    net = _make_net(n_obs, n_actions)
    cfg = SampledMuZeroSearchConfig(num_samples=16, prior_weight=0.0)
    batch = _make_batch(n_obs, n_actions, n_envs, seed=3)
    requests = [{"env_id": b["env_id"], "obs": b["obs"],
                 "legal_masks_by_head": b["legal_masks_by_head"]} for b in batch]

    np.random.seed(99)
    direct = BatchedSampledMuZeroSearch(
        net=net, config=cfg, device=torch.device("cpu")
    ).run_batched_stateful(requests, deterministic=False)

    srv = _server(net, cfg)
    np.random.seed(99)
    served = srv.build_batch_responses(batch)
    srv.stop()

    served_by_env = {int(r["env_id"]): r for r in served}
    for d in direct:
        s = served_by_env[int(d["env_id"])]
        assert s["selected_actions"] == list(d["selected_actions"])
        for h in range(len(n_actions)):
            np.testing.assert_allclose(s["policy_targets"][h], d["policy_targets"][h], atol=1e-5)


def test_server_uses_sampled_search_not_gmz():
    net = _make_net(8, [3])
    cfg = SampledMuZeroSearchConfig(num_samples=8)
    srv = _server(net, cfg)
    assert isinstance(srv._batched_search, BatchedSampledMuZeroSearch)
    srv.stop()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/engine/test_smz_inference_server.py -q`
Expected: FAIL — `ModuleNotFoundError: core.models.smz_inference_server`.

- [ ] **Step 3: Create the server (mirror of gmz server)**

Скопируй `core/models/gmz_inference_server.py` → `core/models/smz_inference_server.py` и примени замены:

| gmz | smz |
|---|---|
| `from core.models.gumbel_muzero_model import GumbelMuZeroNet` | `from core.models.sampled_muzero_model import SampledMuZeroNet, make_sampled_muzero_net` |
| `from core.models.gumbel_muzero_search import (BatchedGumbelMuZeroSearch, GumbelMuZeroSearchConfig)` | `from core.models.sampled_muzero_search import (BatchedSampledMuZeroSearch, SampledMuZeroSearchConfig)` |
| class `GMZInferenceServer` | class `SMZInferenceServer` |
| `BatchedGumbelMuZeroSearch(` (в `__init__`) | `BatchedSampledMuZeroSearch(` |
| тип параметра `net: GumbelMuZeroNet` | `net: SampledMuZeroNet` |
| лог-маркеры `[GMZ][INF_SERVER]` | `[SMZ][INF_SERVER]` |
| env `GMZ_REMOTE_COMPILE` (в тексте лога) | `SMZ_REMOTE_COMPILE` |
| функция `gmz_inference_server_entry` | `smz_inference_server_entry` |

В `smz_inference_server_entry` блок построения сети и конфига заменить на (ВАЖНО — sampled-поля, без num_simulations/root_top_k/gumbel_scale):

```python
        net = make_sampled_muzero_net(
            obs_dim=int(search_cfg_payload.get("obs_dim", 0)),
            action_sizes=[int(x) for x in search_cfg_payload.get("action_sizes", [])],
            latent_dim=int(search_cfg_payload.get("latent_dim", 256)),
            hidden_dim=int(search_cfg_payload.get("hidden_dim", 256)),
            num_layers=int(search_cfg_payload.get("num_layers", 2)),
            action_embed_dim=int(search_cfg_payload.get("action_embed_dim", 64)),
        ).to(device)
        net.load_state_dict(normalize_state_dict(init_weights))
        net.eval()

        search_config = SampledMuZeroSearchConfig(
            num_samples=int(search_cfg_payload.get("num_samples", 24)),
            discount=float(search_cfg_payload.get("discount", 0.997)),
            temperature=float(search_cfg_payload.get("temperature", 0.15)),
            sample_temperature=float(search_cfg_payload.get("sample_temperature", 1.0)),
            prior_weight=float(search_cfg_payload.get("prior_weight", 0.0)),
            dedup=bool(int(search_cfg_payload.get("dedup", 1))),
        )

        server = SMZInferenceServer(
            net=net, search_config=search_config, device=device,
            request_queue=request_q, reply_queues=reply_queues,
            sync_path=sync_path, sync_check_interval=sync_check_interval,
            inference_batch_size=inference_batch_size,
            inference_batch_interval_s=float(inference_batch_interval_ms) / 1000.0,
            compile_mode=bool(inference_server_compile),
            clear_tree_on_weight_sync=clear_tree_on_weight_sync,
        )
```

Всё остальное (батч-цикл `_collect_and_process_batch`, `build_batch_responses`, `_poll_weights`, форма ответа `infer_response`, torch.compile-guard) — оставить как в gmz (это и есть контракт для клиента/воркера). Сигнатуру `smz_inference_server_entry(...)` оставить идентичной gmz-версии (request_q, reply_queues, sync_path, init_weights, search_cfg_payload, *, inference_batch_size, inference_batch_interval_ms, sync_check_interval, inference_server_compile, clear_tree_on_weight_sync).

Проверь ruff: если какой-то импорт (SampledMuZeroNet) не используется напрямую — оставь только используемые.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/engine/test_smz_inference_server.py -q`
Expected: PASS (4 tests). Если equivalence-тест падает — сервер должен звать `run_batched_stateful` с `deterministic=False` так же, как gmz; numerics идентичны при одном seed.

- [ ] **Step 5: Commit**

```bash
git add core/models/smz_inference_server.py tests/engine/test_smz_inference_server.py
git commit -m "feat(sampled_muzero): smz_inference_server (sampled batched-поиск на GPU)"
```

---

## Phase B — Конфиг и провод в train.py

### Task 2: Блок `SMZ_INFERENCE_*`

**Files:** Modify `train.py` (заменить строки 3176–3190 — нынешний простой SMZ device-блок)

- [ ] **Step 1: Replace SMZ device block with inference-aware block**

Найди в train.py текущий блок (начинается с `SMZ_ACTOR_DEVICE_REQUESTED = ...`, ~3176, заканчивается `SMZ_ACTOR_QUEUE_MAX = ...` ~3190). ЗАМЕНИ часть от `SMZ_ACTOR_DEVICE_REQUESTED` до конца device-логики на (миррор GMZ-блока 3060–3133):

```python
# Вариант A: GPU/CPU-акторы; вариант B: inference_server + CPU env workers (local|remote)
SMZ_ACTOR_DEVICE_REQUESTED = str(os.getenv("SMZ_ACTOR_DEVICE", str(SMZ_CFG.get("actor_device", "cuda")))).strip().lower()
if SMZ_ACTOR_DEVICE_REQUESTED not in ("cpu", "cuda", "inference_server"):
    SMZ_ACTOR_DEVICE_REQUESTED = "cuda"
SMZ_ACTOR_MAX_CUDA = max(1, int(os.getenv("SMZ_ACTOR_MAX_CUDA", str(SMZ_CFG.get("actor_max_cuda", 2)))))
SMZ_ACTOR_CPU_FALLBACK_NUM_ACTORS = 8
SMZ_INFERENCE_SERVER_MODE = str(
    os.getenv("SMZ_INFERENCE_SERVER_MODE", str(SMZ_CFG.get("inference_server_mode", "local")))
).strip().lower()
if SMZ_INFERENCE_SERVER_MODE == "inference_server":
    SMZ_INFERENCE_SERVER_MODE = "local"
SMZ_INFERENCE_REMOTE = SMZ_INFERENCE_SERVER_MODE == "remote"
SMZ_INFERENCE_REMOTE_HOST = str(os.getenv("SMZ_INFERENCE_REMOTE_HOST", "127.0.0.1")).strip() or "127.0.0.1"
SMZ_INFERENCE_REMOTE_PORT = max(1, int(os.getenv("SMZ_INFERENCE_REMOTE_PORT", "5560")))
SMZ_INFERENCE_REMOTE_AUTH_TOKEN = str(os.getenv("SMZ_INFERENCE_REMOTE_AUTH_TOKEN", "")).strip()
SMZ_INFERENCE_SERVER_REQUESTED = (
    SMZ_INFERENCE_REMOTE
    or str(os.getenv("SMZ_INFERENCE_SERVER", str(SMZ_CFG.get("inference_server_enabled", 0)))).strip() == "1"
    or SMZ_ACTOR_DEVICE_REQUESTED == "inference_server"
)
SMZ_INFERENCE_SERVER_USING_FALLBACK = (
    SMZ_INFERENCE_SERVER_REQUESTED and not SMZ_INFERENCE_REMOTE and not torch.cuda.is_available()
)
SMZ_INFERENCE_SERVER_ENABLED = SMZ_INFERENCE_SERVER_REQUESTED and (
    SMZ_INFERENCE_REMOTE or torch.cuda.is_available()
)
SMZ_INFERENCE_SERVER_LOCAL = bool(SMZ_INFERENCE_SERVER_ENABLED and not SMZ_INFERENCE_REMOTE)
SMZ_NUM_ENV_WORKERS = max(
    1, int(os.getenv("SMZ_NUM_ENV_WORKERS", str(SMZ_CFG.get("num_env_workers", SMZ_CFG.get("num_actors", 6)))))
)
SMZ_INFERENCE_BATCH_SIZE = max(1, int(os.getenv("SMZ_INFERENCE_BATCH_SIZE", str(SMZ_CFG.get("inference_batch_size", 8)))))
SMZ_INFERENCE_BATCH_INTERVAL_MS = float(
    os.getenv("SMZ_INFERENCE_BATCH_INTERVAL_MS", str(SMZ_CFG.get("inference_batch_interval_ms", 20.0)))
)
SMZ_INFERENCE_TIMEOUT = float(os.getenv("SMZ_INFERENCE_TIMEOUT", str(SMZ_CFG.get("inference_timeout", 5.0))))
SMZ_INFERENCE_REQUEST_QUEUE_MAX = max(
    4, int(os.getenv("SMZ_INFERENCE_REQUEST_QUEUE_MAX", str(SMZ_CFG.get("inference_request_queue_max", 32))))
)
SMZ_INFERENCE_SERVER_COMPILE = str(
    os.getenv("SMZ_INFERENCE_SERVER_COMPILE", str(SMZ_CFG.get("inference_server_compile", 1)))
).strip() == "1"
SMZ_CLEAR_TREE_ON_WEIGHT_SYNC = str(
    os.getenv("SMZ_CLEAR_TREE_ON_WEIGHT_SYNC", str(SMZ_CFG.get("clear_tree_on_weight_sync", 0)))
).strip() == "1"
SMZ_ACTOR_USING_CUDA_FALLBACK = (
    not SMZ_INFERENCE_SERVER_ENABLED
    and SMZ_ACTOR_DEVICE_REQUESTED == "cuda"
    and not torch.cuda.is_available()
)
if SMZ_INFERENCE_SERVER_ENABLED:
    SMZ_ACTOR_DEVICE = "inference_server"
    SMZ_ACTOR_DEVICE_CUDA = False
    SMZ_ACTOR_EFFECTIVE_NUM_ACTORS = int(SMZ_NUM_ENV_WORKERS)
elif SMZ_INFERENCE_SERVER_USING_FALLBACK:
    SMZ_ACTOR_DEVICE = "cpu"
    SMZ_ACTOR_DEVICE_CUDA = False
    SMZ_ACTOR_EFFECTIVE_NUM_ACTORS = int(SMZ_ACTOR_CPU_FALLBACK_NUM_ACTORS)
elif SMZ_ACTOR_USING_CUDA_FALLBACK:
    SMZ_ACTOR_DEVICE = "cpu"
    SMZ_ACTOR_DEVICE_CUDA = False
    SMZ_ACTOR_EFFECTIVE_NUM_ACTORS = int(SMZ_ACTOR_CPU_FALLBACK_NUM_ACTORS)
else:
    SMZ_ACTOR_DEVICE = SMZ_ACTOR_DEVICE_REQUESTED
    SMZ_ACTOR_DEVICE_CUDA = SMZ_ACTOR_DEVICE == "cuda" and torch.cuda.is_available()
    if SMZ_ACTOR_DEVICE_CUDA:
        SMZ_ACTOR_EFFECTIVE_NUM_ACTORS = min(int(SMZ_NUM_ACTORS), int(SMZ_ACTOR_MAX_CUDA))
    else:
        SMZ_ACTOR_EFFECTIVE_NUM_ACTORS = int(SMZ_NUM_ACTORS)
```

Сохрани существующие `SMZ_ACTOR_COMPILE` и `SMZ_ACTOR_QUEUE_MAX` строки (они шли после device-блока) — не удаляй их.

- [ ] **Step 2: Verify import** — `python -c "import train; print('OK')"` → без ошибок.
- [ ] **Step 3: Verify default-off** — `python -c "import train; print(train.SMZ_INFERENCE_SERVER_ENABLED)"` → `False` (дефолт выкл).
- [ ] **Step 4: Commit**

```bash
git add train.py
git commit -m "feat(sampled_muzero): конфиг SMZ_INFERENCE_* (variant B local/remote, дефолт выкл)"
```

### Task 3: Перенаправление inference-ветки в `_main_actor_learner_sampled_muzero`

**Files:** Modify `train.py`

> В sampled actor-learner уже скопирован inference-каркас с gmz-«хвостом». Найди в теле `_main_actor_learner_sampled_muzero` (примерно строки 10860–11074, маркеры `[GMZ][CONFIG]`, `gmz_inference_server_entry`, `GMZ_INFERENCE_*`) и примени замены. Env-воркеры (`_gmz_env_worker_entry`) и клиент НЕ трогаем — они search-agnostic.

- [ ] **Step 1: Add import** (рядом с строкой 118 `from core.models.gmz_inference_server import gmz_inference_server_entry`):

```python
from core.models.smz_inference_server import smz_inference_server_entry
```

- [ ] **Step 2: Substitution table** — в теле `_main_actor_learner_sampled_muzero` заменить:

| было (gmz-хвост) | стало (sampled) |
|---|---|
| `GMZ_INFERENCE_SERVER_ENABLED` | `SMZ_INFERENCE_SERVER_ENABLED` |
| `GMZ_INFERENCE_SERVER_LOCAL` | `SMZ_INFERENCE_SERVER_LOCAL` |
| `GMZ_INFERENCE_REMOTE` | `SMZ_INFERENCE_REMOTE` |
| `GMZ_INFERENCE_SERVER_MODE` | `SMZ_INFERENCE_SERVER_MODE` |
| `GMZ_INFERENCE_REMOTE_HOST/PORT/AUTH_TOKEN` | `SMZ_INFERENCE_REMOTE_HOST/PORT/AUTH_TOKEN` |
| `GMZ_INFERENCE_SERVER_USING_FALLBACK` | `SMZ_INFERENCE_SERVER_USING_FALLBACK` |
| `GMZ_INFERENCE_BATCH_SIZE` | `SMZ_INFERENCE_BATCH_SIZE` |
| `GMZ_INFERENCE_BATCH_INTERVAL_MS` | `SMZ_INFERENCE_BATCH_INTERVAL_MS` |
| `GMZ_INFERENCE_REQUEST_QUEUE_MAX` | `SMZ_INFERENCE_REQUEST_QUEUE_MAX` |
| `GMZ_INFERENCE_TIMEOUT` | `SMZ_INFERENCE_TIMEOUT` |
| `GMZ_INFERENCE_SERVER_COMPILE` | `SMZ_INFERENCE_SERVER_COMPILE` |
| `GMZ_CLEAR_TREE_ON_WEIGHT_SYNC` | `SMZ_CLEAR_TREE_ON_WEIGHT_SYNC` |
| `GMZ_NUM_ENV_WORKERS` | `SMZ_NUM_ENV_WORKERS` |
| `gmz_inference_server_entry` | `smz_inference_server_entry` |
| `[GMZ][CONFIG]` / `[GMZ][INF_SERVER]` строки логов | `[SMZ][CONFIG]` / `[SMZ][INF_SERVER]` |

- [ ] **Step 3: Fix search_cfg_payload** — в месте, где собирается `search_cfg_payload` для сервера (передаётся в `*_inference_server_entry`), заменить gmz-поля на sampled:

```python
        search_cfg_payload = {
            "obs_dim": int(n_observations),
            "action_sizes": [int(x) for x in n_actions],
            "latent_dim": int(SMZ_LATENT_DIM),
            "hidden_dim": int(SMZ_HIDDEN_DIM),
            "num_layers": int(SMZ_NUM_LAYERS),
            "action_embed_dim": int(SMZ_ACTION_EMBED_DIM),
            "num_samples": int(SMZ_NUM_SAMPLES),
            "discount": float(SMZ_DISCOUNT),
            "temperature": float(SMZ_SEARCH_TEMP),
            "sample_temperature": float(SMZ_SAMPLE_TEMP),
            "prior_weight": float(SMZ_PRIOR_WEIGHT),
            "dedup": 1 if SMZ_DEDUP else 0,
        }
```

(точные имена локальных переменных `n_observations`/`n_actions` сверь с тем, как они зовутся в gmz-версии — повтори 1:1.)

- [ ] **Step 4: Verify** — `python -c "import train; print('OK')"`; затем убедись, что в теле функции не осталось `GMZ_INFERENCE`/`gmz_inference_server_entry`:
  Run: `python -c "import ast,re,io; s=open('train.py',encoding='utf-8').read(); i=s.index('def _main_actor_learner_sampled_muzero'); j=s.index('def ', i+10); body=s[i:j]; print('GMZ_INFERENCE leftovers:', body.count('GMZ_INFERENCE'), '| gmz_inference_server_entry:', body.count('gmz_inference_server_entry'))"`
  Expected: `0 | 0`.

- [ ] **Step 5: Commit**

```bash
git add train.py
git commit -m "fix(sampled_muzero): variant B запускает smz_inference_server (а не gmz)"
```

### Task 4: hyperparams.json inference-поля

**Files:** Modify `hyperparams.json`

- [ ] **Step 1: Add inference fields to `sampled_muzero`** (в существующую секцию):

```json
"actor_max_cuda": 2,
"num_env_workers": 6,
"inference_server_enabled": 0,
"inference_server_mode": "local",
"inference_server_compile": 1,
"inference_batch_size": 8,
"inference_batch_interval_ms": 20.0,
"inference_request_queue_max": 32,
"inference_timeout": 5.0,
"clear_tree_on_weight_sync": 0
```

- [ ] **Step 2: Validate JSON** — `python -c "import json; json.load(open('hyperparams.json',encoding='utf-8')); print('json ok')"`.
- [ ] **Step 3: Commit** — `git add hyperparams.json && git commit -m "feat(sampled_muzero): hyperparams inference-server поля (дефолт выкл)"`

---

## Phase C — ПК2-обвязка

### Task 5: `tools/smz_remote_inference_server.py`

**Files:** Create `tools/smz_remote_inference_server.py`

- [ ] **Step 1: Mirror gmz remote server** — скопируй `tools/gmz_remote_inference_server.py` → `tools/smz_remote_inference_server.py`, замены:

| gmz | smz |
|---|---|
| `from core.models.gmz_inference_server import GMZInferenceServer` | `from core.models.smz_inference_server import SMZInferenceServer` |
| `from core.models.gumbel_muzero_model import GumbelMuZeroNet` | `from core.models.sampled_muzero_model import make_sampled_muzero_net` |
| `from core.models.gumbel_muzero_search import GumbelMuZeroSearchConfig` | `from core.models.sampled_muzero_search import SampledMuZeroSearchConfig` |
| `GumbelMuZeroNet(...)` (построение сети) | `make_sampled_muzero_net(obs_dim=..., action_sizes=..., latent_dim=..., hidden_dim=..., num_layers=..., action_embed_dim=...)` |
| `GumbelMuZeroSearchConfig(num_simulations=…, root_top_k=…, gumbel_scale=…, batch_recurrent=…, tree_reuse=…)` | `SampledMuZeroSearchConfig(num_samples=int(search_cfg.get("num_samples",24)), discount=…, temperature=…, sample_temperature=float(search_cfg.get("sample_temperature",1.0)), prior_weight=float(search_cfg.get("prior_weight",0.0)), dedup=bool(int(search_cfg.get("dedup",1))))` |
| `GMZInferenceServer(...)` | `SMZInferenceServer(...)` (те же kwargs) |
| класс `GMZRemoteInferenceServer` | `SMZRemoteInferenceServer` |
| лог-маркеры `[GMZ][REMOTE_IS]` | `[SMZ][REMOTE_IS]` |
| `--port` default `5555` | `5560` |
| лог-файл `gmz_remote_is_{stamp}.log` | `smz_remote_is_{stamp}.log` |
| `description="40kAI GMZ Remote..."` | `"40kAI Sampled MuZero Remote..."` |

Протокол/транспорт (`gmz_inference_protocol`), ZMQ ROUTER-логику, health-check, батч-цикл — оставить как есть (импортируем gmz protocol).

- [ ] **Step 2: Verify import** — `python -c "import importlib; importlib.import_module('tools.smz_remote_inference_server'); print('OK')"` (или `python -m py_compile tools/smz_remote_inference_server.py`).
- [ ] **Step 3: Commit** — `git add tools/smz_remote_inference_server.py && git commit -m "feat(sampled_muzero): ПК2 standalone remote IS сервер"`

### Task 6: ПК2 bat + конфиг-шаблон

**Files:** Create `tools/pc2_remote_smz_is.bat`, `runtime/state/pc2_remote_smz_is_config.example.bat`, `runtime/state/pc2_remote_smz_is_config.example.rev`

- [ ] **Step 1: Mirror bat** — скопируй `tools/pc2_remote_is.bat` → `tools/pc2_remote_smz_is.bat`, замены:
  - env-префикс `GMZ_REMOTE_*` → `SMZ_REMOTE_*` (HOST/PORT/DEVICE/BATCH_SIZE/BATCH_INTERVAL_MS/SYNC_INTERVAL/COMPILE/AUTH_TOKEN/WEIGHTS_PATH/SEARCH_CONFIG/INIT_WEIGHTS/SETUP_FIREWALL).
  - `SERVER_PY=...\gmz_remote_inference_server.py` → `...\smz_remote_inference_server.py`.
  - конфиг-пути: `pc2_remote_is_config*.bat/.rev` → `pc2_remote_smz_is_config*.bat/.rev`.
  - дефолт порта `5555` → `5560`; firewall rule name `"40kAI Remote IS"` → `"40kAI SMZ Remote IS"`.
  - имена SMB-файлов: `latest_gmz_policy.pth`→`latest_smz_policy.pth`, `gmz_remote_search_cfg.json`→`smz_remote_search_cfg.json`.
  - заголовки/тексты echo: «Remote Inference Server (PC2)» → «Sampled MuZero Remote IS (PC2)».
  - дока-ссылка в ошибке: `docs\remote-inference-server-gmz.md` → `docs\remote-inference-server-smz.md`.

- [ ] **Step 2: Create config example** — `runtime/state/pc2_remote_smz_is_config.example.bat`:

```bat
@echo off
REM Конфиг ПК2 для Sampled MuZero Remote Inference Server. Скопируется в pc2_remote_smz_is_config.bat.
REM Пути под вашу SMB-шару (Z:\ или 40KAI_SHARE_ROOT).
set "SMZ_REMOTE_HOST=0.0.0.0"
set "SMZ_REMOTE_PORT=5560"
set "SMZ_REMOTE_DEVICE=cuda:0"
set "SMZ_REMOTE_BATCH_SIZE=10"
set "SMZ_REMOTE_BATCH_INTERVAL_MS=20"
set "SMZ_REMOTE_SYNC_INTERVAL=0.5"
set "SMZ_REMOTE_COMPILE=1"
set "SMZ_REMOTE_AUTH_TOKEN="
set "SMZ_REMOTE_SETUP_FIREWALL=1"
REM Веса и search-cfg (если не выводятся из 40KAI_SHARE_ROOT):
set "SMZ_REMOTE_WEIGHTS_PATH="
set "SMZ_REMOTE_SEARCH_CONFIG="
set "SMZ_REMOTE_INIT_WEIGHTS="
exit /b 0
```

И `runtime/state/pc2_remote_smz_is_config.example.rev` с содержимым `1`.

- [ ] **Step 3: gitignore** — добавь в `.gitignore` (если gmz-аналог там есть — проверь): `runtime/state/pc2_remote_smz_is_config.bat`, `runtime/state/pc2_remote_smz_is_config.rev`, `runtime/state/pc2_remote_smz_is_config.bat.bak`.

- [ ] **Step 4: Smoke** — `python -m py_compile` неприменим к .bat; проверь, что bat не ломает синтаксис визуально и SERVER_PY указывает на smz-файл. (Реальный запуск — на ПК2, ручной.)
- [ ] **Step 5: Commit** — `git add tools/pc2_remote_smz_is.bat runtime/state/pc2_remote_smz_is_config.example.* .gitignore && git commit -m "feat(sampled_muzero): ПК2 кнопка pc2_remote_smz_is.bat + конфиг-шаблон"`

---

## Phase D — GUI

### Task 7: GUI inference-дефолты

**Files:** Modify `app/gui_qt/sampled_muzero_hyperparams_defaults.py`

- [ ] **Step 1:** Добавь inference-ключи в `DEFAULT_SMZ_HYPERPARAMS` и `SMZ_HYPERPARAM_KEYS` (значения = Task 4) + в подходящую группу `SMZ_GROUPS` (например, новая группа «Inference Server» или существующая «actors»), с тултипами RU. Изучи, как gmz-дефолты (`gmz_hyperparams_defaults.py`) группируют inference-поля, и повтори.
- [ ] **Step 2: Verify** — `python -c "import app.gui_qt.sampled_muzero_hyperparams_defaults as m; print('inference_server_enabled' in m.SMZ_HYPERPARAM_KEYS)"` → `True`.
- [ ] **Step 3: Commit** — `git add app/gui_qt/sampled_muzero_hyperparams_defaults.py && git commit -m "feat(sampled_muzero): GUI inference-server дефолты гиперов"`

### Task 8: GUI train-launch env + QML панель

**Files:** Modify `app/gui_qt/main.py`, `app/gui_qt/qml/components/SectionHyperparamsEditor.qml`

> Источник-эталон: как gmz при train-launch экспортит `GMZ_INFERENCE_*` env и читает `runtime/state/remote_is.json`. Найди в main.py train-launch функцию (где для gumbel_muzero выставляются GMZ_* env) и зеркаль для sampled.

- [ ] **Step 1: main.py train-launch** — в ветке train-launch для sampled добавь экспорт env из hpSmz-полей:
  `SMZ_INFERENCE_SERVER` (=inference_server_enabled), `SMZ_INFERENCE_SERVER_MODE`, `SMZ_INFERENCE_SERVER_COMPILE`, `SMZ_INFERENCE_BATCH_SIZE`, `SMZ_INFERENCE_BATCH_INTERVAL_MS`, `SMZ_INFERENCE_REQUEST_QUEUE_MAX`, `SMZ_INFERENCE_TIMEOUT`, `SMZ_NUM_ENV_WORKERS`, `SMZ_ACTOR_DEVICE`. Для remote — `SMZ_INFERENCE_REMOTE_HOST/PORT/AUTH_TOKEN` из `runtime/state/remote_is_smz.json` (миррор того, как gmz читает remote_is.json; если файла нет — local).
- [ ] **Step 2: isIntKey** — в `SectionHyperparamsEditor.qml::isIntKey` добавь inference-целочисленные: `inference_server_enabled`, `inference_server_compile`, `inference_batch_size`, `inference_request_queue_max`, `num_env_workers`, `clear_tree_on_weight_sync`, `actor_max_cuda` (если ещё нет — многие уже покрыты паттернами `num_`/`_size`). Проверь `k.indexOf("inference_server_enabled")`, `"inference_server_compile"`, `"clear_tree_on_weight_sync"`.
- [ ] **Step 3: Verify** — `QT_QPA_PLATFORM=offscreen python -c "import app.gui_qt.main; print('OK')"` + `.venv/Scripts/pyside6-qmllint app/gui_qt/qml/components/SectionHyperparamsEditor.qml` (только синтаксис/error).
- [ ] **Step 4: Commit** — `git add app/gui_qt/main.py app/gui_qt/qml/components/SectionHyperparamsEditor.qml && git commit -m "feat(sampled_muzero): GUI экспорт SMZ_INFERENCE_* + панель inference-server"`

---

## Phase E — Дока и финал

### Task 9: Документация

**Files:** Create `docs/remote-inference-server-smz.md`, `docs/pc2-remote-smz-is-setup-guide.md`

- [ ] **Step 1: Mirror docs** — скопируй `docs/remote-inference-server-gmz.md` → `docs/remote-inference-server-smz.md` и `docs/pc2-remote-smz-is-setup-guide.md` (если есть gmz-аналог `docs/pc2-remote-is-setup-guide.md` — миррор его). Замены: gmz→sampled_muzero/smz, порт 5555→5560, имена файлов/тулзов/env (`SMZ_REMOTE_*`, `tools/pc2_remote_smz_is.bat`, `latest_smz_policy.pth`, `smz_remote_search_cfg.json`), search-cfg-пример с полями `num_samples/sample_temperature/temperature/prior_weight/dedup` вместо `num_simulations/root_top_k/gumbel_scale`. Маркер логов `[SMZ]`.
- [ ] **Step 2: Cross-link AGENTS.md** — добавь в `AGENTS.md` (секция Remote Inference Server) строку про sampled-вариант с ссылкой на новую доку и порт 5560. (Правка AGENTS.md — это инструкции проекта; добавляй аккуратно, одну строку-пойнтер.)
- [ ] **Step 3: Commit** — `git add docs/remote-inference-server-smz.md docs/pc2-remote-smz-is-setup-guide.md AGENTS.md && git commit -m "docs(sampled_muzero): remote IS гайды (ПК1+ПК2)"`

### Task 10: Сквозная проверка

- [ ] **Step 1: Server + regress tests**

Run: `python -m pytest tests/engine/test_smz_inference_server.py tests/engine/test_gmz_inference_transport.py tests/engine/test_gmz_inference_ipc.py tests/models/test_sampled_muzero_search.py tests/models/test_sampled_muzero_search_batched.py tests/train/test_sampled_muzero_actor_learner_smoke.py -q`
Expected: ALL PASS (smz server + gmz провод-регресс + sampled регресс).

- [ ] **Step 2: Import + default-off**

Run: `python -c "import train; print('enabled=', train.SMZ_INFERENCE_SERVER_ENABLED)"`
Expected: `enabled= False`.

- [ ] **Step 3: Variant-B-local smoke (CPU)** — если позволяет время/CUDA: запусти короткий sampled train с `SMZ_INFERENCE_SERVER=1` (или на CPU — fallback в вариант A с WARN `[SMZ][CONFIG][FALLBACK]`, что тоже валидно). Проверь логи `[SMZ][INF_SERVER]`/`[SMZ][CONFIG]`. Полный ПК2-прогон — ручной (пользователь).

- [ ] **Step 4: Final** — докоммит мелочей при необходимости.

---

## Self-Review (выполнено при написании плана)

- **Покрытие спеки:** Секция 1 (сервер) → Task 1. Секция 2 (SMZ_INFERENCE_* config) → Task 2. Секция 3 (провод в actor-learner) → Task 3. Секция 4 (ПК2-обвязка) → Tasks 5–6. Секция 5 (GUI) → Tasks 4,7,8. Секция 6 (тесты) → Task 1 + Task 10. Секция 7 (риски) → анти-«забытое зеркало» тест `test_server_uses_sampled_search_not_gmz` (Task 1), порт 5560 (Tasks 2,5,6), graceful compile-skip (наследуется от gmz), секреты в gitignore (Task 6).
- **Заглушки:** новый сервер/тест/config — полный код; мирроры (tools/bat/docs/GUI) — таблицы точных замен + конкретные новые файлы (config.example.bat, hyperparams-поля) даны целиком. Это исполнимо.
- **Согласованность имён:** `SMZInferenceServer`/`smz_inference_server_entry`, `BatchedSampledMuZeroSearch`, `SampledMuZeroSearchConfig(num_samples/discount/temperature/sample_temperature/prior_weight/dedup)`, env `SMZ_INFERENCE_*`/`SMZ_REMOTE_*`, файлы `latest_smz_policy.pth`/`smz_remote_search_cfg.json`, порт 5560, чекпойнт-ключ `sampled_muzero_net` — едины во всех тасках. Реюз: gmz protocol/transport/client/`_gmz_env_worker_entry` (search-agnostic).
