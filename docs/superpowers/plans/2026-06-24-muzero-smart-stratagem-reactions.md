# Умные реакции-стратагемы для GMZ/SMZ — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Включить умный value-gate реактивных стратагем (как у DQN/PPO/AZ) для Gumbel MuZero и Sampled MuZero — установкой `env.reaction_policy` в локальном selfplay.

**Architecture:** Новый общий бридж `core/models/muzero_stratagem_bridge.py` (флаг-хелпер + install + decision-обёртка). Единый install-пойнт — в начале `play_episode_with_gumbel_muzero` (SMZ делегирует в неё же), различие GMZ/SMZ — через параметр-тег. Активные fight-стратагемы уже в action-пространстве — не трогаем.

**Tech Stack:** Python 3.12, pytest, torch, stdlib. Без новых зависимостей.

## Global Constraints

- Платформа Windows; язык логов/сообщений/комментариев — русский (AGENTS.md).
- TDD: тест до кода. Частые коммиты. ruff чистый.
- НЕ менять формат `runtime/logs/LOGS_FOR_AGENTS_*.md`; не коммитить runtime-логи/артефакты.
- Дефолт ВКЛ (флаги `GMZ_REACTION_VALUE_POLICY` / `SMZ_REACTION_VALUE_POLICY`, default `"1"`).
- Только локальный режим: при remote (`inference_fn`, `search is None`) гейт не ставится.
- Обе стороны: `{"model": net, "enemy": net}`.
- НЕ трогать действующий механизм DQN/PPO/AZ; переиспользовать `make_reaction_value_policy`
  (`core/models/reaction_value_policy.py`) и env-методы `_simulate_reaction_branch`/`_reaction_net_value`.
- Локальная сеть берётся из `search.net` (`GumbelMuZeroSearch.net`/`SampledMuZeroSearch.net`).

---

### Task 1: Бридж `muzero_stratagem_bridge.py` (флаг + install + decision)

**Files:**
- Create: `core/models/muzero_stratagem_bridge.py`
- Test: `tests/models/test_muzero_stratagem_bridge.py`

**Interfaces:**
- Produces:
  - `muzero_reaction_value_policy_enabled(flag_env: str, default: str = "1") -> bool`
  - `install_muzero_reaction_policy(env, net, *, both_sides: bool = True, log_tag: str = "GMZ", log_fn=None) -> bool`
  - `maybe_install_muzero_reactions(env, *, search, inference_fn, flag_env: str, log_tag: str, log_fn=None) -> bool`

- [ ] **Step 1: Написать падающий тест**

```python
# tests/models/test_muzero_stratagem_bridge.py
import types

import pytest

from core.models.muzero_stratagem_bridge import (
    install_muzero_reaction_policy,
    maybe_install_muzero_reactions,
    muzero_reaction_value_policy_enabled,
)


class _FakeNet:
    # MuZero-подобная сеть: есть infer, НЕТ infer_with_value
    def parameters(self):
        import torch
        yield torch.zeros(1)

    def infer(self, obs, masks_by_head=None):
        return None, 0.0


def _fake_env():
    env = types.SimpleNamespace()
    env.unwrapped = env  # unwrap_env вернёт его же
    return env


def test_enabled_default_on(monkeypatch):
    monkeypatch.delenv("GMZ_REACTION_VALUE_POLICY", raising=False)
    assert muzero_reaction_value_policy_enabled("GMZ_REACTION_VALUE_POLICY") is True


def test_enabled_off(monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "0")
    assert muzero_reaction_value_policy_enabled("GMZ_REACTION_VALUE_POLICY") is False


def test_install_sets_policy_both_sides():
    env = _fake_env()
    net = _FakeNet()
    ok = install_muzero_reaction_policy(env, net, log_tag="GMZ")
    assert ok is True
    assert callable(env.reaction_policy)
    assert env._reaction_net_by_side == {"model": net, "enemy": net}


def test_install_net_none_is_noop():
    env = _fake_env()
    ok = install_muzero_reaction_policy(env, None, log_tag="GMZ")
    assert ok is False
    assert getattr(env, "reaction_policy", None) is None


def test_maybe_install_local_search(monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "1")
    env = _fake_env()
    search = types.SimpleNamespace(net=_FakeNet())
    ok = maybe_install_muzero_reactions(
        env, search=search, inference_fn=None,
        flag_env="GMZ_REACTION_VALUE_POLICY", log_tag="GMZ",
    )
    assert ok is True
    assert callable(env.reaction_policy)


def test_maybe_install_remote_skips(monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "1")
    env = _fake_env()
    ok = maybe_install_muzero_reactions(
        env, search=None, inference_fn=lambda *a, **k: None,
        flag_env="GMZ_REACTION_VALUE_POLICY", log_tag="GMZ",
    )
    assert ok is False
    assert getattr(env, "reaction_policy", None) is None


def test_maybe_install_flag_off(monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "0")
    env = _fake_env()
    search = types.SimpleNamespace(net=_FakeNet())
    ok = maybe_install_muzero_reactions(
        env, search=search, inference_fn=None,
        flag_env="GMZ_REACTION_VALUE_POLICY", log_tag="GMZ",
    )
    assert ok is False
    assert getattr(env, "reaction_policy", None) is None
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/models/test_muzero_stratagem_bridge.py -q`
Expected: FAIL (ModuleNotFoundError: core.models.muzero_stratagem_bridge).

- [ ] **Step 3: Реализовать модуль**

```python
# core/models/muzero_stratagem_bridge.py
"""MuZero (GMZ/SMZ) ↔ умные реакции-стратагемы.

Ставит value-gate реакций (make_reaction_value_policy) в env.reaction_policy, используя
локальную MuZero-сеть (value через net.infer — фолбэк в env._reaction_net_value). Только
локальный режим (есть search.net); при remote inference гейт не ставится.
"""
from __future__ import annotations

import os

from core.models.utils import unwrap_env

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def muzero_reaction_value_policy_enabled(flag_env: str, default: str = "1") -> bool:
    return str(os.getenv(flag_env, default)).strip().lower() in _TRUTHY


def install_muzero_reaction_policy(
    env, net, *, both_sides: bool = True, log_tag: str = "GMZ", log_fn=None
) -> bool:
    """Поставить value-gate реакций на env. net=None → no-op (False).

    Ошибка install не валит обучение: WARN-лог + возврат False (legacy-реакции).
    """
    if net is None:
        return False
    try:
        import torch

        from core.models.reaction_value_policy import make_reaction_value_policy

        try:
            device = next(net.parameters()).device
        except (StopIteration, AttributeError):
            device = torch.device("cpu")
        e = unwrap_env(env)
        e._reaction_net_by_side = {"model": net, "enemy": net} if both_sides else {"model": net}
        e.reaction_policy = make_reaction_value_policy(e._reaction_net_by_side, device=device)
        msg = f"[{log_tag}][REACTION] reaction_value_policy=ON (both_sides={both_sides})"
        (log_fn or print)(msg)
        return True
    except Exception as exc:  # noqa: BLE001 — install не должен ронять обучение
        msg = (
            f"[{log_tag}][REACTION][WARN] установка reaction_value_policy не удалась "
            f"(muzero_stratagem_bridge.install_muzero_reaction_policy): {exc}. "
            f"Продолжаем на legacy-реакциях."
        )
        (log_fn or print)(msg)
        return False


def maybe_install_muzero_reactions(
    env, *, search, inference_fn, flag_env: str, log_tag: str, log_fn=None
) -> bool:
    """Решение об install: флаг ВКЛ + локальный режим (search есть). Иначе skip."""
    if not muzero_reaction_value_policy_enabled(flag_env):
        return False
    if search is None or inference_fn is not None:
        (log_fn or print)(
            f"[{log_tag}][REACTION] skip: remote inference (local-only feature)"
        )
        return False
    net = getattr(search, "net", None)
    return install_muzero_reaction_policy(env, net, both_sides=True, log_tag=log_tag, log_fn=log_fn)
```

- [ ] **Step 4: Запустить тест — все зелёные**

Run: `python -m pytest tests/models/test_muzero_stratagem_bridge.py -q`
Expected: PASS (7 passed).

- [ ] **Step 5: ruff + коммит**

```bash
python -m ruff check core/models/muzero_stratagem_bridge.py
git add core/models/muzero_stratagem_bridge.py tests/models/test_muzero_stratagem_bridge.py
git commit -m "feat(muzero): бридж умных реакций-стратагем (install + флаг)"
```

---

### Task 2: Подключить install в MuZero selfplay (GMZ + SMZ-тег)

**Files:**
- Modify: `core/models/gumbel_muzero_selfplay.py` (функция `play_episode_with_gumbel_muzero`, после `env_u = unwrap_env(env)` — строка ~67)
- Modify: `core/models/sampled_muzero_selfplay.py` (обёртка `play_episode_with_sampled_muzero`)
- Test: `tests/models/test_muzero_selfplay_reaction_wiring.py`

**Interfaces:**
- Consumes: `maybe_install_muzero_reactions` (Task 1).
- Produces: у `play_episode_with_gumbel_muzero` новый параметр `reaction_algo_tag: str = "GMZ"`;
  SMZ-обёртка форсит `reaction_algo_tag="SMZ"`.

- [ ] **Step 1: Написать падающий тест (wiring)**

```python
# tests/models/test_muzero_selfplay_reaction_wiring.py
import types

import pytest

import core.models.gumbel_muzero_selfplay as gmz_sp
import core.models.sampled_muzero_selfplay as smz_sp


class _StopReset(Exception):
    pass


def _fake_env():
    # env, падающий на reset, чтобы остановиться сразу после install-пойнта
    env = types.SimpleNamespace()
    env.unwrapped = env
    env.model = []
    env.enemy = []
    env.first_turn_side = "model"

    def _reset(*a, **k):
        raise _StopReset()

    env.reset = _reset
    return env


def test_gmz_selfplay_calls_install(monkeypatch):
    calls = {}

    def _fake_maybe(env, *, search, inference_fn, flag_env, log_tag, log_fn=None):
        calls["flag_env"] = flag_env
        calls["log_tag"] = log_tag
        return True

    monkeypatch.setattr(gmz_sp, "maybe_install_muzero_reactions", _fake_maybe)
    with pytest.raises(_StopReset):
        gmz_sp.play_episode_with_gumbel_muzero(
            env=_fake_env(), search=object(), len_model=1
        )
    assert calls["flag_env"] == "GMZ_REACTION_VALUE_POLICY"
    assert calls["log_tag"] == "GMZ"


def test_smz_wrapper_forwards_smz_tag(monkeypatch):
    calls = {}

    def _fake_maybe(env, *, search, inference_fn, flag_env, log_tag, log_fn=None):
        calls["flag_env"] = flag_env
        calls["log_tag"] = log_tag
        return True

    monkeypatch.setattr(gmz_sp, "maybe_install_muzero_reactions", _fake_maybe)
    with pytest.raises(_StopReset):
        smz_sp.play_episode_with_sampled_muzero(
            env=_fake_env(), search=object(), len_model=1
        )
    assert calls["flag_env"] == "SMZ_REACTION_VALUE_POLICY"
    assert calls["log_tag"] == "SMZ"
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/models/test_muzero_selfplay_reaction_wiring.py -q`
Expected: FAIL (TypeError: unexpected keyword `reaction_algo_tag`, либо install не вызван / тег неверен).

- [ ] **Step 3: Добавить install-вызов в `play_episode_with_gumbel_muzero`**

В сигнатуру `play_episode_with_gumbel_muzero(...)` добавить параметр (рядом с `deterministic`):

```python
    reaction_algo_tag: str = "GMZ",
```

Импорт вверху файла (рядом с прочими импортами из core.models):

```python
from core.models.muzero_stratagem_bridge import maybe_install_muzero_reactions
```

Сразу после `env_u = unwrap_env(env)` (строка ~67) вставить install (до reset, чтобы гейт стоял на весь эпизод):

```python
    maybe_install_muzero_reactions(
        env,
        search=search,
        inference_fn=inference_fn,
        flag_env=f"{reaction_algo_tag}_REACTION_VALUE_POLICY",
        log_tag=reaction_algo_tag,
    )
```

- [ ] **Step 4: Прокинуть SMZ-тег в обёртке** `sampled_muzero_selfplay.py`

```python
def play_episode_with_sampled_muzero(**kwargs):
    """Прогон эпизода с sampled-поиском. selfplay-петля идентична gmz: search.run имеет
    ту же сигнатуру, поэтому переиспользуем play_episode_with_gumbel_muzero как есть."""
    kwargs.setdefault("reaction_algo_tag", "SMZ")
    return play_episode_with_gumbel_muzero(**kwargs)
```

- [ ] **Step 5: Запустить wiring-тест — зелёный**

Run: `python -m pytest tests/models/test_muzero_selfplay_reaction_wiring.py -q`
Expected: PASS (2 passed).
> Если тест падает с AttributeError ДО install (доступ к атрибуту env между `unwrap_env` и
> install) — значит install-вызов стоит слишком поздно; перенести его строго сразу после
> `env_u = unwrap_env(env)`.

- [ ] **Step 6: Регресс — существующие MuZero-тесты не сломаны**

Run: `python -m pytest tests/models -q -k "muzero or gmz or smz or gumbel or sampled"`
Expected: PASS (все ранее зелёные остаются зелёными).

- [ ] **Step 7: ruff + коммит**

```bash
python -m ruff check core/models/gumbel_muzero_selfplay.py core/models/sampled_muzero_selfplay.py
git add core/models/gumbel_muzero_selfplay.py core/models/sampled_muzero_selfplay.py tests/models/test_muzero_selfplay_reaction_wiring.py
git commit -m "feat(muzero): install умных реакций в GMZ/SMZ selfplay (local-only, дефолт ВКЛ)"
```

---

### Task 3: Косметика — видимый дефолт AZ в train.py

**Files:**
- Modify: `train.py:6049` и `train.py:6322`

Контекст: AZ/GAZ уже ВКЛ по умолчанию (резолв `train.py:2398-2402`, hyperparams `reaction_value_policy: 1`). Инлайновые `os.getenv("AZ_REACTION_VALUE_POLICY", "0")` — фолбэк, перетираемый строкой 2402; видимый «0» вводит в заблуждение. Меняем дефолт на `"1"` для совпадения видимого и реального поведения. **Поведение не меняется** (os.environ всегда пред-установлен на 2402/2405).

- [ ] **Step 1: Правка обоих мест**

В `train.py:6049` и `train.py:6322` заменить:

```python
        if str(os.getenv("AZ_REACTION_VALUE_POLICY", "0")).strip().lower() in ("1", "true", "yes", "on"):
```
на:
```python
        if str(os.getenv("AZ_REACTION_VALUE_POLICY", "1")).strip().lower() in ("1", "true", "yes", "on"):
```

- [ ] **Step 2: Проверка, что AZ-тесты/импорт не сломаны**

Run: `python -m pytest tests/eval -q -k "az or alphazero" ; python -c "import train"`
Expected: импорт train без ошибок; релевантные тесты зелёные (как на baseline).

- [ ] **Step 3: Коммит**

```bash
git add train.py
git commit -m "chore(az): видимый дефолт AZ_REACTION_VALUE_POLICY=1 (совпадает с реальным)"
```

---

### Task 4: Smoke — реальный короткий GMZ-selfplay (локально)

**Files:** нет правок кода (только проверка)

- [ ] **Step 1: Короткий локальный GMZ-прогон** (через Qt GUI приоритетно по AGENTS.md; для smoke допустим терминал). Запустить обучение GMZ на 1-2 эпизода локально (без remote-IS, `GMZ_INFERENCE_SERVER` не выставлен), флаг по умолчанию ВКЛ.

- [ ] **Step 2: Проверить лог** `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md`: присутствует строка
`[GMZ][REACTION] reaction_value_policy=ON`; эпизод(ы) завершаются без исключений (value-путь
`net.infer` отработал в реальном env — закрывает риск value-семантики).

- [ ] **Step 3: Проверить выключение**: запустить с `GMZ_REACTION_VALUE_POLICY=0` → в логе
строки `reaction_value_policy=ON` нет; эпизод проходит (legacy-реакции).

- [ ] **Step 4: Без правок кода — коммитов нет** (только подтверждение поведения).

---

## Definition of Done

- Task 1: 7 passed, ruff чистый.
- Task 2: 2 wiring-теста passed; существующие MuZero-тесты не сломаны; ruff чистый.
- Task 3: import train ок, AZ-тесты как на baseline.
- Task 4: smoke подтверждает install в реальном GMZ-эпизоде (лог `=ON`, без падений) и
  корректное отключение по флагу.
- Коммиты только по коду; артефакты прогона/логи не коммитятся.

## Не-цели (YAGNI)

- Remote-inference поддержка реакций — нет (local-only).
- Изменение action-пространства / активных fight-стратагем — нет.
- Тренировочные прогоны «до/после» с измерением эффекта — отдельно (есть таблица стратагем для замера).
