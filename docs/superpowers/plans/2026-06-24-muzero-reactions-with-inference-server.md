# Умные реакции GMZ/SMZ при включённом Inference Server — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Включить умные реакции-стратагемы GMZ/SMZ при работающем inference server (local и remote IS) через локальную value-сеть на env-воркере — без сетевых round-trip.

**Architecture:** Общий net-builder (DRY с сервером) строит локальную `GumbelMuZeroNet`/SMZ-сеть из синкаемого `*_remote_search_cfg.json` + `latest_*_policy.pth`. Env-воркер строит её, ставит `env.reaction_policy` через готовый бридж `install_muzero_reaction_policy` (напрямую, как AZ env-воркер), и периодически перегружает веса. Основной поиск как был уходит на сервер.

**Tech Stack:** Python 3.12, torch, pytest, stdlib. Без новых зависимостей и серверных RPC.

## Global Constraints

- Платформа Windows; язык логов/сообщений/комментариев — русский (AGENTS.md).
- TDD: тест до кода. Частые коммиты. ruff чистый.
- НЕ менять серверный протокол/RPC; НЕ менять основной поиск и action-пространство.
- НЕ коммитить runtime-логи/веса/артефакты.
- Реакции активны в IS для **обоих** режимов (local + remote), нагрузка — CPU воркера (без round-trip).
- Флаги (дефолт ВКЛ): `GMZ_REACTION_VALUE_POLICY` / `SMZ_REACTION_VALUE_POLICY`.
- Refresh весов: env `MUZERO_REACTION_NET_REFRESH_EVERY_EP`, default `10`.
- Переиспользовать: `install_muzero_reaction_policy` (`core/models/muzero_stratagem_bridge.py`),
  `normalize_state_dict` (`core/models/utils.py`).
- Конструкции сетей (как у сервера): GMZ `GumbelMuZeroNet(obs_dim, action_sizes, latent_dim,
  hidden_dim, num_layers, action_embed_dim)` (`gmz_inference_server.py:286-294`); SMZ
  `make_sampled_muzero_net(...)` те же поля (`smz_inference_server.py:288-296`).
- Имена ассетов: GMZ `gmz_remote_search_cfg.json` + `latest_gmz_policy.pth`; SMZ
  `smz_remote_search_cfg.json` + `latest_smz_policy.pth` (см. `*_remote_search_cfg_builder.py`).

---

### Task 1: Shared net-builder `muzero_value_net_builder.py`

**Files:**
- Create: `core/models/muzero_value_net_builder.py`
- Test: `tests/models/test_muzero_value_net_builder.py`

**Interfaces:**
- Produces:
  - `build_gmz_net_from_search_cfg(search_cfg_payload: dict, *, device) -> GumbelMuZeroNet`
  - `build_smz_net_from_search_cfg(search_cfg_payload: dict, *, device)` (SMZ-сеть)
  - `load_value_net_weights(net, weights_path: str, *, device=None) -> bool`

- [ ] **Step 1: Написать падающий тест**

```python
# tests/models/test_muzero_value_net_builder.py
import torch

from core.models.muzero_value_net_builder import (
    build_gmz_net_from_search_cfg,
    build_smz_net_from_search_cfg,
    load_value_net_weights,
)

_CFG = {
    "obs_dim": 8,
    "action_sizes": [3, 2],
    "latent_dim": 16,
    "hidden_dim": 16,
    "num_layers": 1,
    "action_embed_dim": 4,
}


def test_build_gmz_net_infers_value():
    net = build_gmz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    policy, value = net.infer(torch.zeros(1, 8), masks_by_head=None)
    assert float(value.reshape(-1)[0]) == float(value.reshape(-1)[0])  # не NaN-проверка структуры


def test_build_smz_net_infers_value():
    net = build_smz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    policy, value = net.infer(torch.zeros(1, 8), masks_by_head=None)
    assert value.reshape(-1).shape[0] >= 1


def test_build_raises_on_empty_cfg():
    import pytest
    with pytest.raises(ValueError):
        build_gmz_net_from_search_cfg({}, device=torch.device("cpu"))


def test_load_value_net_weights_roundtrip(tmp_path):
    net = build_gmz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    p = tmp_path / "w.pth"
    torch.save(net.state_dict(), str(p))
    net2 = build_gmz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    assert load_value_net_weights(net2, str(p)) is True


def test_load_value_net_weights_missing_returns_false():
    net = build_gmz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    assert load_value_net_weights(net, "no_such_file.pth") is False
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/models/test_muzero_value_net_builder.py -q`
Expected: FAIL (ModuleNotFoundError: core.models.muzero_value_net_builder).

- [ ] **Step 3: Реализовать модуль**

```python
# core/models/muzero_value_net_builder.py
"""Построение локальной value-сети MuZero (GMZ/SMZ) из remote_search_cfg + загрузка весов.

Используется и сервером (DRY), и env-воркером для реакций. Конструкция идентична серверной
(gmz_inference_server / smz_inference_server), чтобы веса грузились в совместимую форму.
"""
from __future__ import annotations


def _dims(search_cfg_payload: dict):
    obs_dim = int(search_cfg_payload.get("obs_dim", 0))
    action_sizes = [int(x) for x in search_cfg_payload.get("action_sizes", [])]
    if obs_dim <= 0 or not action_sizes:
        raise ValueError(
            "muzero_value_net_builder: пустой search_cfg (obs_dim<=0 или action_sizes=[]). "
            "Где: build_*_net_from_search_cfg. Что делать: дождаться публикации "
            "*_remote_search_cfg.json рядом с весами (actor_sync/SMB)."
        )
    return obs_dim, action_sizes, {
        "latent_dim": int(search_cfg_payload.get("latent_dim", 256)),
        "hidden_dim": int(search_cfg_payload.get("hidden_dim", 256)),
        "num_layers": int(search_cfg_payload.get("num_layers", 2)),
        "action_embed_dim": int(search_cfg_payload.get("action_embed_dim", 64)),
    }


def build_gmz_net_from_search_cfg(search_cfg_payload: dict, *, device):
    from core.models.gumbel_muzero_model import GumbelMuZeroNet

    obs_dim, action_sizes, rest = _dims(search_cfg_payload)
    net = GumbelMuZeroNet(obs_dim=obs_dim, action_sizes=action_sizes, **rest).to(device)
    net.eval()
    return net


def build_smz_net_from_search_cfg(search_cfg_payload: dict, *, device):
    from core.models.sampled_muzero_model import make_sampled_muzero_net

    obs_dim, action_sizes, rest = _dims(search_cfg_payload)
    net = make_sampled_muzero_net(obs_dim=obs_dim, action_sizes=action_sizes, **rest).to(device)
    net.eval()
    return net


def load_value_net_weights(net, weights_path: str, *, device=None) -> bool:
    """Загрузить веса в сеть (strict=False). Нет файла/ошибка → False, без исключения."""
    import torch

    from core.models.utils import normalize_state_dict

    try:
        sd = torch.load(weights_path, map_location=device or torch.device("cpu"))
        net.load_state_dict(normalize_state_dict(sd), strict=False)
        return True
    except Exception:
        return False
```

- [ ] **Step 4: Запустить тест — зелёный**

Run: `python -m pytest tests/models/test_muzero_value_net_builder.py -q`
Expected: PASS (5 passed).

- [ ] **Step 5: ruff + коммит**

```bash
python -m ruff check core/models/muzero_value_net_builder.py
git add core/models/muzero_value_net_builder.py tests/models/test_muzero_value_net_builder.py
git commit -m "feat(muzero): shared net-builder из search_cfg + загрузка весов (для сервера и воркера)"
```

---

### Task 2: Worker-install + refresh хелперы в `muzero_stratagem_bridge.py`

**Files:**
- Modify: `core/models/muzero_stratagem_bridge.py`
- Test: `tests/models/test_worker_reaction_value_net.py`

**Interfaces:**
- Consumes: `install_muzero_reaction_policy` (тот же модуль); `load_value_net_weights` (Task 1).
- Produces:
  - `install_worker_reaction_value_net(env, *, assets_dir, cfg_name, weights_name, build_net_fn, flag_env, log_tag, device=None, log_fn=None) -> object | None`
  - `refresh_worker_reaction_net(net, *, assets_dir, weights_name, device=None) -> bool`

- [ ] **Step 1: Написать падающий тест**

```python
# tests/models/test_worker_reaction_value_net.py
import json
import types

import torch

from core.models.muzero_stratagem_bridge import install_worker_reaction_value_net
from core.models.muzero_value_net_builder import build_gmz_net_from_search_cfg

_CFG = {"obs_dim": 8, "action_sizes": [3, 2], "latent_dim": 16,
        "hidden_dim": 16, "num_layers": 1, "action_embed_dim": 4}


def _assets(tmp_path):
    (tmp_path / "gmz_remote_search_cfg.json").write_text(json.dumps(_CFG), encoding="utf-8")
    net = build_gmz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    torch.save(net.state_dict(), str(tmp_path / "latest_gmz_policy.pth"))


def _env():
    e = types.SimpleNamespace()
    e.unwrapped = e
    return e


def test_install_worker_reaction_net_ok(tmp_path, monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "1")
    _assets(tmp_path)
    env = _env()
    net = install_worker_reaction_value_net(
        env, assets_dir=str(tmp_path), cfg_name="gmz_remote_search_cfg.json",
        weights_name="latest_gmz_policy.pth",
        build_net_fn=build_gmz_net_from_search_cfg,
        flag_env="GMZ_REACTION_VALUE_POLICY", log_tag="GMZ",
    )
    assert net is not None
    assert callable(env.reaction_policy)


def test_install_worker_reaction_net_missing_assets(tmp_path, monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "1")
    env = _env()  # каталог пуст
    net = install_worker_reaction_value_net(
        env, assets_dir=str(tmp_path), cfg_name="gmz_remote_search_cfg.json",
        weights_name="latest_gmz_policy.pth",
        build_net_fn=build_gmz_net_from_search_cfg,
        flag_env="GMZ_REACTION_VALUE_POLICY", log_tag="GMZ",
    )
    assert net is None
    assert getattr(env, "reaction_policy", None) is None


def test_install_worker_reaction_net_flag_off(tmp_path, monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "0")
    _assets(tmp_path)
    env = _env()
    net = install_worker_reaction_value_net(
        env, assets_dir=str(tmp_path), cfg_name="gmz_remote_search_cfg.json",
        weights_name="latest_gmz_policy.pth",
        build_net_fn=build_gmz_net_from_search_cfg,
        flag_env="GMZ_REACTION_VALUE_POLICY", log_tag="GMZ",
    )
    assert net is None
    assert getattr(env, "reaction_policy", None) is None
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/models/test_worker_reaction_value_net.py -q`
Expected: FAIL (ImportError: install_worker_reaction_value_net).

- [ ] **Step 3: Добавить хелперы в `core/models/muzero_stratagem_bridge.py`** (в конец файла)

```python
def install_worker_reaction_value_net(
    env, *, assets_dir, cfg_name, weights_name, build_net_fn,
    flag_env, log_tag, device=None, log_fn=None,
):
    """IS-воркер: построить локальную value-сеть из assets_dir и поставить reaction_policy.

    assets_dir содержит cfg_name (*_remote_search_cfg.json) и weights_name (latest_*_policy.pth).
    Флаг ВЫКЛ / нет файлов / ошибка → None (legacy-реакции), без падения воркера.
    """
    import json
    import os

    import torch

    from core.models.muzero_value_net_builder import load_value_net_weights

    if not muzero_reaction_value_policy_enabled(flag_env):
        return None
    _dev = device or torch.device("cpu")
    try:
        cfg_path = os.path.join(assets_dir, cfg_name)
        weights_path = os.path.join(assets_dir, weights_name)
        if not (os.path.isfile(cfg_path) and os.path.isfile(weights_path)):
            (log_fn or print)(
                f"[{log_tag}][ENV_WORKER] reaction_value_policy skip: нет {cfg_name}/{weights_name} "
                f"в {assets_dir} (ещё не синканы) — legacy-реакции."
            )
            return None
        with open(cfg_path, encoding="utf-8") as fh:
            payload = json.load(fh)
        net = build_net_fn(payload, device=_dev)
        if not load_value_net_weights(net, weights_path, device=_dev):
            (log_fn or print)(
                f"[{log_tag}][ENV_WORKER][WARN] не удалось загрузить веса {weights_path} — legacy-реакции."
            )
            return None
        ok = install_muzero_reaction_policy(env, net, log_tag=log_tag, log_fn=log_fn)
        return net if ok else None
    except Exception as exc:  # noqa: BLE001 — воркер не должен падать
        (log_fn or print)(
            f"[{log_tag}][ENV_WORKER][WARN] установка локальной value-сети реакций не удалась "
            f"(install_worker_reaction_value_net): {exc}. Legacy-реакции."
        )
        return None


def refresh_worker_reaction_net(net, *, assets_dir, weights_name, device=None) -> bool:
    """Перегрузить веса локальной value-сети реакций (refresh). net=None → False."""
    import os

    import torch

    from core.models.muzero_value_net_builder import load_value_net_weights

    if net is None:
        return False
    return load_value_net_weights(
        net, os.path.join(assets_dir, weights_name), device=device or torch.device("cpu")
    )
```

- [ ] **Step 4: Запустить тест — зелёный**

Run: `python -m pytest tests/models/test_worker_reaction_value_net.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: ruff + коммит**

```bash
python -m ruff check core/models/muzero_stratagem_bridge.py
git add core/models/muzero_stratagem_bridge.py tests/models/test_worker_reaction_value_net.py
git commit -m "feat(muzero): worker-install локальной value-сети реакций + refresh (для IS)"
```

---

### Task 3: Рефактор серверов на shared net-builder (DRY)

**Files:**
- Modify: `core/models/gmz_inference_server.py:279-294`
- Modify: `core/models/smz_inference_server.py:288-296`

**Interfaces:**
- Consumes: `build_gmz_net_from_search_cfg` / `build_smz_net_from_search_cfg`, `load_value_net_weights` (Task 1).

- [ ] **Step 1: GMZ-сервер — заменить инлайн-конструкцию на builder**

В `gmz_inference_server.py` заменить блок `gmz_inference_server.py:279-295` (от `latent_dim = ...`
до `net.eval()`) на:

```python
        from core.models.muzero_value_net_builder import build_gmz_net_from_search_cfg

        net = build_gmz_net_from_search_cfg(search_cfg_payload, device=device)
        net.load_state_dict(normalize_state_dict(init_weights))
        net.eval()
```

- [ ] **Step 2: SMZ-сервер — то же**

В `smz_inference_server.py` заменить блок построения (`smz_inference_server.py:288-297`, от
`net = make_sampled_muzero_net(` до `net.eval()`) на:

```python
        from core.models.muzero_value_net_builder import build_smz_net_from_search_cfg

        net = build_smz_net_from_search_cfg(search_cfg_payload, device=device)
        net.load_state_dict(normalize_state_dict(init_weights))
        net.eval()
```

> Примечание: серверы оставляют существующую проверку пустого cfg (там свой текст ошибки) ПЕРЕД
> вызовом builder, либо полагаются на ValueError из `_dims` — сохранить прежнее поведение
> (если до этого была явная проверка obs_dim/action_sizes — оставить её).

- [ ] **Step 3: Проверка — серверы импортируются, существующие IS-тесты не сломаны**

Run:
```bash
python -c "import core.models.gmz_inference_server, core.models.smz_inference_server"
python -m pytest tests/eval tests/models/test_gaz_remote_search_cfg_builder.py tests/models/test_smz_remote_search_cfg_builder.py -q -k "smz or gmz or remote_search or inference"
```
Expected: импорт ок; релевантные тесты как на baseline (не хуже).

- [ ] **Step 4: ruff + коммит**

```bash
python -m ruff check core/models/gmz_inference_server.py core/models/smz_inference_server.py
git add core/models/gmz_inference_server.py core/models/smz_inference_server.py
git commit -m "refactor(muzero): серверы строят сеть через shared net-builder (DRY)"
```

---

### Task 4: Подключить install + refresh в env-воркерах GMZ/SMZ (train.py)

**Files:**
- Modify: `train.py` — `_gmz_env_worker_entry` (старт ~`train.py:7515`, env build `:7550`, цикл эпизодов `:7619`)
- Modify: `train.py` — SMZ env-worker entry (рядом, ищи `latest_smz_policy.pth` `:8015`)
- Modify: `train.py` — спавн воркеров (`target=_gmz_env_worker_entry` `:8635`, `:9397`) — прокинуть `reaction_assets_dir`

**Interfaces:**
- Consumes: `install_worker_reaction_value_net`, `refresh_worker_reaction_net` (Task 2);
  `build_gmz_net_from_search_cfg` / `build_smz_net_from_search_cfg` (Task 1).

- [ ] **Step 1: Добавить параметр `reaction_assets_dir` в сигнатуру `_gmz_env_worker_entry`**

В сигнатуру (после `remote_auth_token: str = "",`) добавить:

```python
    reaction_assets_dir: str = "",
```

- [ ] **Step 2: После `env = gym.make(...)` в `_gmz_env_worker_entry` (`train.py:7550`) — install**

```python
        from core.models.muzero_stratagem_bridge import (
            install_worker_reaction_value_net,
            refresh_worker_reaction_net,
        )
        from core.models.muzero_value_net_builder import build_gmz_net_from_search_cfg

        _assets_dir = str(reaction_assets_dir or os.path.join(MODELS_DIR, "actor_sync"))
        _reaction_net = install_worker_reaction_value_net(
            env,
            assets_dir=_assets_dir,
            cfg_name="gmz_remote_search_cfg.json",
            weights_name="latest_gmz_policy.pth",
            build_net_fn=build_gmz_net_from_search_cfg,
            flag_env="GMZ_REACTION_VALUE_POLICY",
            log_tag="GMZ",
            log_fn=append_agent_log,
        )
        _reaction_refresh_k = max(1, int(os.getenv("MUZERO_REACTION_NET_REFRESH_EVERY_EP", "10")))
```

- [ ] **Step 3: В цикле эпизодов `_gmz_env_worker_entry` (`train.py:7619`, `for _ep in range(...)`) — refresh**

В конце тела цикла (после отправки rollout) добавить:

```python
            if _reaction_net is not None and ((int(_ep) + 1) % _reaction_refresh_k == 0):
                refresh_worker_reaction_net(
                    _reaction_net, assets_dir=_assets_dir, weights_name="latest_gmz_policy.pth"
                )
```

- [ ] **Step 4: SMZ env-worker — те же 3 вставки** с заменами: `build_smz_net_from_search_cfg`,
`cfg_name="smz_remote_search_cfg.json"`, `weights_name="latest_smz_policy.pth"`,
`flag_env="SMZ_REACTION_VALUE_POLICY"`, `log_tag="SMZ"`. Параметр сигнатуры `reaction_assets_dir`
добавить так же.

- [ ] **Step 5: Прокинуть `reaction_assets_dir` на спавне** (`target=_gmz_env_worker_entry`, `:8635`
и `:9397`; SMZ-спавн рядом). В `args=(...)` добавить значение каталога ассетов: для local IS —
`os.path.join(MODELS_DIR, "actor_sync")`; для remote — переменную share_root, если она в области
видимости спавна (сверь по коду; если её нет — оставить `os.path.join(MODELS_DIR, "actor_sync")`,
а на remote-воркере путь к SMB резолвится тем же механизмом, что у sync_path воркера).

> Примечание исполнителю: точные позиции `args` сверь по коду (Process(target=...) формирует
> кортеж позиционных аргументов в порядке сигнатуры). `reaction_assets_dir` — последний параметр,
> добавляй его последним элементом кортежа во ВСЕХ местах спавна обоих воркеров.

- [ ] **Step 6: Проверка импорта + регресс точечно (не тяжёлый muzero subset)**

Run:
```bash
python -c "import train"
python -m pytest tests/models/test_muzero_value_net_builder.py tests/models/test_worker_reaction_value_net.py tests/models/test_muzero_stratagem_bridge.py -q
```
Expected: import train ок; тесты PASS.
> ВНИМАНИЕ: НЕ запускать `pytest tests/models -k muzero` целиком — этот subset тяжёлый по ОЗУ и лагает машину.

- [ ] **Step 7: ruff + коммит**

```bash
python -m ruff check train.py
git add train.py
git commit -m "feat(muzero): env-воркеры GMZ/SMZ ставят локальную value-сеть реакций при IS + refresh"
```

---

### Task 5: Smoke — local IS с реакциями

**Files:** нет правок кода (проверка)

- [ ] **Step 1: Локальный IS-прогон GMZ** (приоритетно через Qt GUI; для smoke допустим терминал):
включить inference server в локальном режиме (`GMZ_INFERENCE_SERVER=1`, mode local), флаг реакций
по умолчанию ВКЛ. Прогнать 1-2 эпизода.

- [ ] **Step 2: Проверить лог** `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md`: есть строка
`[GMZ][REACTION] reaction_value_policy=ON` (бридж логирует с тегом, переданным из воркера);
эпизоды без падений (локальная value-сеть отработала в IS-режиме). Если ассеты ещё не синканы
на старте — допустима строка `[GMZ][ENV_WORKER] reaction_value_policy skip: нет ... (ещё не синканы)`,
затем на следующем прогоне (после публикации cfg+весов) install проходит.

- [ ] **Step 3: Проверить отключение**: `GMZ_REACTION_VALUE_POLICY=0` → строки `reaction_value_policy=ON` нет, эпизод идёт.

- [ ] **Step 4: Без правок кода — коммитов нет.**

---

## Definition of Done

- Task 1: 5 passed, ruff чистый.
- Task 2: 3 passed, ruff чистый.
- Task 3: серверы импортируются, релевантные IS-тесты как на baseline, ruff чистый.
- Task 4: `import train` ок, целевые тесты passed, ruff чистый (НЕ гонять тяжёлый muzero subset).
- Task 5: smoke (local IS) — лог `[GMZ][REACTION] reaction_value_policy=ON`, без падений; отключение по флагу работает.
- SMZ-симметрия выполнена (Task 4 Step 4).
- Коммиты только по коду; артефакты/логи/веса не коммитятся.

## Не-цели (YAGNI)

- Новые серверные RPC — нет. Изменение основного поиска/action-пространства — нет.
- Адаптивная частота refresh — нет (фикс K + env-override).
- Измерение эффекта на winrate — отдельно (есть таблица стратагем).
