# Eval строит env под контракт агента (phase_obs_features) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Чтобы AZ-eval поднимал env с тем же `phase_obs_features`, с которым агент обучался (источник истины — контракт агента, фолбэк — hyperparams), и не падал `obs_space_signature mismatch`.

**Architecture:** (A) `make_env_contract` авто-кладёт `phase_obs_features`/`reaction_value_policy` в `extras` (контракт самоописывающий; формат сигнатуры неизменен). (B) `eval.py` ДО постройки env резолвит `phase_obs_features` из контракта агента → hyperparams → env-var → 0 и выставляет `os.environ["PHASE_OBS_FEATURES"]`.

**Tech Stack:** Python 3.12, pytest, JSON-контракты агентов. Windows.

## Global Constraints

- **Источник дизайна:** `docs/superpowers/specs/2026-06-23-eval-phase-obs-contract-design.md`.
- **Формат `obs_space_signature` НЕ меняется** (`vec:{n}`, без суффикса) — иначе сломается существующий `vec:41`-агент. `extras` НЕ участвует в `compatible_contracts`.
- **Приоритет резолва phase_obs:** контракт агента (`extras.phase_obs_features`) → hyperparams (`alphazero_tree.phase_obs_features`) → env-var `PHASE_OBS_FEATURES` → 0.
- **Legacy:** агент без `extras.phase_obs_features` грузится через hyperparams-фолбэк (там сейчас `=1`).
- eval НЕ полагается на побочный эффект импорта `train.py` для phase_obs — читает `hyperparams.json` напрямую.
- Язык кода/комментов/коммитов — русский. TDD. Коммит RU + `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- НЕ трогать: формулу `warhamEnv.py:90` (`vec:N+phaseM`) — вне области; логику движка/обучения.
- `ruff check --fix` по изменённым (если ruff установлен; иначе пропустить и отметить).

## File Structure

| Файл | Что |
|------|-----|
| `core/engine/agent_registry.py` | `make_env_contract`: авто-`extras` с phase_obs/reaction |
| `eval.py` | резолвер phase_obs до постройки env + вызов в `main()` |
| `tests/engine/test_agent_registry_phase_obs_extras.py` | новый тест (A) |
| `tests/test_eval_phase_obs_resolve.py` | новый тест (B) |
| существующие контракт-тесты | обновить под авто-extras |

---

## Task 1: make_env_contract — phase_obs/reaction в extras

**Files:**
- Modify: `core/engine/agent_registry.py` (`make_env_contract`, строки 160-186)
- Test: `tests/engine/test_agent_registry_phase_obs_extras.py` (создать)
- Возможно обновить: `tests/engine/test_agent_registry_b2_contract.py`, `tests/models/test_dqn_dist_contract_extras.py`, `tests/engine/test_sampled_muzero_registry.py`

**Interfaces:**
- Produces: `make_env_contract(...)` теперь возвращает контракт, где `extras` содержит ключи `phase_obs_features: int(0|1)` и `reaction_value_policy: int(0|1)` (если не переданы явно). `obs_space_signature` формат неизменен.

- [ ] **Step 1: Падающий тест**

Создать `tests/engine/test_agent_registry_phase_obs_extras.py`:
```python
"""make_env_contract авто-кладёт phase_obs_features/reaction_value_policy в extras."""

import os

from core.engine.agent_registry import compatible_contracts, make_env_contract


def test_extras_has_phase_obs_and_reaction(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    monkeypatch.setenv("AZ_REACTION_VALUE_POLICY", "1")
    c = make_env_contract(n_observations=41, n_actions=[5, 2], mission_name="only_war")
    assert c["extras"]["phase_obs_features"] == 1
    assert c["extras"]["reaction_value_policy"] == 1
    # формат сигнатуры неизменен — без суффикса +phase
    assert c["obs_space_signature"] == "vec:41"


def test_phase_obs_off(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "0")
    c = make_env_contract(n_observations=17, n_actions=[5, 2], mission_name="only_war")
    assert c["extras"]["phase_obs_features"] == 0
    assert c["obs_space_signature"] == "vec:17"


def test_explicit_extras_not_overwritten(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    c = make_env_contract(
        n_observations=41, n_actions=[5, 2], mission_name="only_war",
        extras={"phase_obs_features": 0, "custom": "x"},
    )
    assert c["extras"]["phase_obs_features"] == 0  # явный приоритетнее
    assert c["extras"]["custom"] == "x"


def test_extras_do_not_break_compatibility(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    a = make_env_contract(n_observations=41, n_actions=[5, 2], mission_name="only_war")
    monkeypatch.setenv("PHASE_OBS_FEATURES", "0")
    b = make_env_contract(n_observations=41, n_actions=[5, 2], mission_name="only_war")
    # extras различаются, но sig одинаковы → совместимы
    ok, reason = compatible_contracts(a, b)
    assert ok, reason
```

- [ ] **Step 2: Запустить — упадёт**

Run: `python -m pytest tests/engine/test_agent_registry_phase_obs_extras.py -v`
Expected: FAIL — в `extras` нет `phase_obs_features`.

- [ ] **Step 3: Реализация в make_env_contract**

В `core/engine/agent_registry.py`, в начале файла добавить импорт (рядом с прочими):
```python
from core.engine.phases.obs_features import phase_obs_features_enabled
```
В `make_env_contract` (после `act_signature = ...`, перед сборкой `payload`) собрать авто-extras и слить с переданным (переданный приоритетнее):
```python
    _auto_extras = {
        "phase_obs_features": int(phase_obs_features_enabled()),
        "reaction_value_policy": 1 if str(os.getenv("AZ_REACTION_VALUE_POLICY", "1")).strip().lower() in ("1", "true", "yes", "on") else 0,
    }
    merged_extras = {**_auto_extras, **(extras or {})}
```
Заменить `"extras": extras or {},` на `"extras": merged_extras,` И в `contract_hash`-payload `"extras": payload["extras"],` (уже ссылается на payload["extras"] → ок). Убедиться, что `import os` в файле есть (если нет — добавить).

- [ ] **Step 4: Запустить — пройдёт**

Run: `python -m pytest tests/engine/test_agent_registry_phase_obs_extras.py -v` → 4 passed.

- [ ] **Step 5: Обновить существующие контракт-тесты**

Run: `python -m pytest tests/engine/test_agent_registry_b2_contract.py tests/models/test_dqn_dist_contract_extras.py tests/engine/test_sampled_muzero_registry.py -v`
Если падают из-за новых авто-ключей в `extras` или изменившегося `contract_hash` — обновить ожидания: тесты, сверяющие `extras == {...}` точным сравнением, должны учитывать авто-ключи `phase_obs_features`/`reaction_value_policy` (или проверять `extras` через `>=`/подмножество, или явно передавать extras). Тесты на `compatible_contracts` (сравнение sig) — НЕ должны падать (extras не влияет); если падают — это сигнал реальной ошибки, разобраться. Не ослабляй проверки совместимости.

- [ ] **Step 6: Commit**
```bash
git add core/engine/agent_registry.py tests/engine/test_agent_registry_phase_obs_extras.py
# + обновлённые контракт-тесты, если менялись
git commit -m "feat(registry): phase_obs_features/reaction_value_policy в extras контракта (самоописывающий, формат sig неизменен)"
```

---

## Task 2: eval резолвит phase_obs до постройки env

**Files:**
- Modify: `eval.py` (новая функция-резолвер + вызов в `main()` до `load_latest_model`, ~строка 981)
- Test: `tests/test_eval_phase_obs_resolve.py` (создать)

**Interfaces:**
- Consumes: `extras.phase_obs_features` из контракта агента (Task 1); `load_agent_by_id` (уже импортирован в eval.py:19).
- Produces: `eval._resolve_phase_obs_env(agent_id: str | None) -> int` — резолвит phase_obs (контракт→hyperparams→env-var→0), выставляет `os.environ["PHASE_OBS_FEATURES"]`, возвращает 0|1.

- [ ] **Step 1: Падающий тест**

Создать `tests/test_eval_phase_obs_resolve.py`:
```python
"""eval._resolve_phase_obs_env: приоритет контракт агента → hyperparams → env → 0."""

import os

import eval as eval_mod


def test_contract_extras_takes_priority(monkeypatch):
    monkeypatch.delenv("PHASE_OBS_FEATURES", raising=False)
    monkeypatch.setattr(
        eval_mod, "load_agent_by_id",
        lambda aid: {"contract": {"extras": {"phase_obs_features": 1}}},
    )
    # hyperparams вернёт 0 — но контракт (1) приоритетнее
    monkeypatch.setattr(eval_mod, "_hyperparams_phase_obs", lambda: 0)
    res = eval_mod._resolve_phase_obs_env("some_agent")
    assert res == 1
    assert os.environ["PHASE_OBS_FEATURES"] == "1"


def test_falls_back_to_hyperparams_when_no_extras(monkeypatch):
    monkeypatch.delenv("PHASE_OBS_FEATURES", raising=False)
    monkeypatch.setattr(
        eval_mod, "load_agent_by_id",
        lambda aid: {"contract": {"extras": {}}},  # нет phase_obs_features (legacy)
    )
    monkeypatch.setattr(eval_mod, "_hyperparams_phase_obs", lambda: 1)
    res = eval_mod._resolve_phase_obs_env("legacy_agent")
    assert res == 1
    assert os.environ["PHASE_OBS_FEATURES"] == "1"


def test_no_agent_uses_env_or_zero(monkeypatch):
    monkeypatch.delenv("PHASE_OBS_FEATURES", raising=False)
    monkeypatch.setattr(eval_mod, "_hyperparams_phase_obs", lambda: 0)
    res = eval_mod._resolve_phase_obs_env(None)
    assert res == 0
```

- [ ] **Step 2: Запустить — упадёт**

Run: `python -m pytest tests/test_eval_phase_obs_resolve.py -v`
Expected: FAIL — нет `_resolve_phase_obs_env` / `_hyperparams_phase_obs`.

- [ ] **Step 3: Реализация в eval.py**

Добавить в `eval.py` (рядом с другими хелперами, до `main`/`run_episode`):
```python
def _hyperparams_phase_obs() -> int | None:
    """phase_obs_features из hyperparams.json (alphazero_tree). None если нет/ошибка."""
    import json
    try:
        with open(os.path.abspath("hyperparams.json"), encoding="utf-8") as j:
            data = json.load(j)
        az = data.get("alphazero_tree", {}) if isinstance(data, dict) else {}
        v = az.get("phase_obs_features", None)
        return None if v is None else (1 if int(v) else 0)
    except Exception:
        return None


def _resolve_phase_obs_env(agent_id: str | None) -> int:
    """Резолв phase_obs: контракт агента → hyperparams → env-var → 0. Ставит os.environ."""
    # 1) контракт агента
    if agent_id and str(agent_id).strip():
        try:
            payload = load_agent_by_id(str(agent_id).strip())
            extras = ((payload or {}).get("contract", {}) or {}).get("extras", {}) or {}
            if "phase_obs_features" in extras:
                val = 1 if int(extras["phase_obs_features"]) else 0
                os.environ["PHASE_OBS_FEATURES"] = str(val)
                return val
        except Exception:
            pass
    # 2) hyperparams
    hp = _hyperparams_phase_obs()
    if hp is not None:
        os.environ["PHASE_OBS_FEATURES"] = str(int(hp))
        return int(hp)
    # 3) env-var → 4) 0
    env_v = str(os.getenv("PHASE_OBS_FEATURES", "0")).strip().lower()
    val = 1 if env_v in ("1", "true", "yes", "on") else 0
    os.environ["PHASE_OBS_FEATURES"] = str(val)
    return val
```
(`os` и `load_agent_by_id` уже импортированы в eval.py.)

- [ ] **Step 4: Запустить — пройдёт**

Run: `python -m pytest tests/test_eval_phase_obs_resolve.py -v` → 3 passed.

- [ ] **Step 5: Вызвать резолвер в main() ДО постройки env**

В `eval.py`, в `main()`, НАЙТИ строку `env, model_units, enemy_units, checkpoint, pickle_path, checkpoint_path = load_latest_model(args.model)` (~стр.981). НЕПОСРЕДСТВЕННО ПЕРЕД ней вставить:
```python
    # phase_obs_features должен совпасть с тем, на чём обучался агент (иначе obs_space mismatch).
    # Резолвим ДО постройки env: контракт агента → hyperparams → env-var → 0.
    _resolved_phase_obs = _resolve_phase_obs_env(getattr(args, "learner_agent_id", None))
    log(f"[EVAL][AZ][CONFIG] phase_obs резолв до env: PHASE_OBS_FEATURES={_resolved_phase_obs}")
```
(Это гарантирует, что `phase_obs_features_enabled()` при reset() вернёт правильное значение → obs=41 для phase-obs-агента.)

- [ ] **Step 6: Регрессия + import**

Run: `python -c "import eval"` → без ошибок.
Run: `python -m pytest tests/test_eval_phase_obs_resolve.py tests/engine/test_agent_registry_phase_obs_extras.py -v` → PASS.
Run: `python -m pytest tests/engine/ -q -p no:cacheprovider --continue-on-collection-errors` → baseline не вырос (раньше ~23 failed; новых падений нет).

- [ ] **Step 7: Smoke — падавший eval теперь поднимается**

Запустить тот же eval, что падал (AZ, learner-agent-id `P1_Necrons_only_war_v2_final_ep10_20260623_163453`, opponent heuristic, **без** ручного `PHASE_OBS_FEATURES`). Ожидать в логе:
- `[EVAL][AZ][CONFIG] phase_obs резолв до env: PHASE_OBS_FEATURES=1`
- `[EVAL][AZ][CONFIG] phase_obs_features=1 obs_size=41`
- НЕТ `[ERROR] ... obs_space_signature mismatch`; оценка стартует (идут `[GAME ...]`).
Если eval требует CUDA/GPU и среда без него — отметить в отчёте, что smoke не прогнан из-за окружения (юнит-тесты + логика покрывают).
`ruff check --fix eval.py core/engine/agent_registry.py` (если ruff есть).

- [ ] **Step 8: Commit**
```bash
git add eval.py tests/test_eval_phase_obs_resolve.py
git commit -m "fix(eval): резолв phase_obs_features из контракта агента до постройки env (чинит obs_space_signature mismatch)"
```

---

## Self-Review

**Spec coverage:**
- (A) make_env_contract авто-extras phase_obs/reaction, формат sig неизменен — Task 1. ✓
- (B) eval резолвит phase_obs контракт→hyperparams→env→0 до env — Task 2 (Steps 3,5). ✓
- (C) legacy `vec:41`-агент через hyperparams-фолбэк — Task 2 Step 1 `test_falls_back_to_hyperparams`. ✓
- compatible_contracts не ломается (extras не влияет) — Task 1 `test_extras_do_not_break_compatibility`. ✓
- eval читает hyperparams напрямую (не через импорт train) — Task 2 `_hyperparams_phase_obs`. ✓
- smoke падавшего eval — Task 2 Step 7. ✓
- обновление существующих контракт-тестов — Task 1 Step 5. ✓

**Placeholder scan:** код в каждом шаге полный; точки вставки по якорю (`load_latest_model(args.model)` ~981) + строка-импорт. Step 5 Task 1 — реальная инструкция «обнови ожидания под авто-ключи» (зависит от факта падения теста, не плейсхолдер).

**Type consistency:** `_resolve_phase_obs_env(agent_id)->int`, `_hyperparams_phase_obs()->int|None`, `extras["phase_obs_features"]:int` — согласованы между тестами и реализацией. `load_agent_by_id` возвращает payload с `["contract"]["extras"]` (как в eval.py:1053-1060).

**Примечание:** reaction_value_policy кладётся в extras (Task 1), но eval-резолвер (Task 2) его в os.environ НЕ выставляет (obs определяет только phase_obs). Если smoke покажет obs≠41 при phase=1 — значит reaction тоже влияет на obs (не ожидается); тогда добавить его резолв аналогично. Базово — вне необходимости (YAGNI).

---

## Execution Handoff

См. сообщение после плана (исполнение внешним агентом, я — ревью).
