# Windowed Self-Play Parity Fix — Implementation Plan (Part A)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Устранить регрессию агрессии windowed-исполнения (Stage 8.4): добиться, чтобы при одном и том же `action_dict` поведение `windowed_selfplay=1` совпадало с legacy `env.step`, и подтвердить это на winrate-harness, прежде чем возвращать дефолт `windowed_selfplay=1`.

**Статус:** план готов к исполнению; код/тесты из Tasks 1–7 **ещё не внедрены** (файла `test_windowed_legacy_parity.py` в репо нет).

**Architecture:** Диагностика-первой (systematic-debugging): сначала строим точный per-phase parity-харнесс на «боевом» сценарии (юниты в дальности стрельбы/чарджа, реальные головы `move`/`move_num`/`shoot`/`charge`), который **локализует** расхождение windowed↔legacy. Затем чиним по фактам — по одной фазе, каждый фикс закрыт своим parity-тестом. Финал — winrate-сравнение `WINDOWED_SELFPLAY=0` vs `=1` на фикс. сидах.

**Порядок задач (зависимости):** Task 1 → Task 2 (ядро) → Tasks 3–5 (регресс-гейты, правка только если красные) → Task 6 (лог out-of-range, **после** Task 2) → Task 7 (winrate). Part B — отдельно после зелёного Part A.

**Tech Stack:** Python 3.12, `core/engine/phases/` (PhaseEngine, option_generator, windowed_selfplay), `core/envs/warhamEnv.py` (legacy-фазы), pytest, `tools/mcts_winrate_baseline.py`.

## Global Constraints

- Платформа **Windows**, Python **3.12+**; тесты: `python -m pytest` из корня репозитория.
- Язык логов/ошибок/UI — **русский**; ошибки: *что случилось + где (файл/функция) + что делать дальше*.
- **Не ломать golden-trace при `WINDOWED_SELFPLAY=0`** — legacy-путь 1:1 с текущим `env.step`.
- **Движок не импортирует `core.models`** — логика окон только в `core/engine/phases/`.
- **Не редактировать** `runtime/logs/LOGS_FOR_AGENTS_*.md` (хук `guard_paths.py` заблокирует).
- ruff: `ruff.toml`, line-length 120 (хук `ruff_fix.py` прогоняется после правок `.py`).
- Коммитить только релевантный код; без runtime-логов/временных файлов. Не коммитить без «Все ок» пользователя.
- Базовый эмпирический факт (A/B до фикса, 100 эп, depth=1, sims=32, `candidate_mode=option`, `simulate_enemy=0`; метрики `artifacts/metrics/stats_*.csv`):
  - `windowed=1` (run `3247087`): **win 0.13**, draw 0.33, **turn_limit 0.80**, wipeout_enemy 0.12, turns_mean≈20.1.
  - `windowed=0` (run `2537664`): **win 0.47**, draw 0.09, **turn_limit 0.40**, wipeout_enemy 0.47, turns_mean≈17.5.
  - Гипотеза: windowed форсит STAY/PASS при «рваном» factorized `action_dict`; legacy даёт fallback по `move` и т.п.

---

## File Structure

| Файл | Ответственность | Действие |
|------|------------------|----------|
| `tests/engine/phases/test_windowed_legacy_parity.py` | Per-phase parity-харнесс на боевом сценарии (диагностика + регресс-гейт) | Create |
| `core/engine/phases/windowed_selfplay.py` | Мост flat `action_dict` → `decide(window)`; здесь живут PASS/STAY-фолбэки и игнор `move` | Modify |
| `core/engine/phases/phase_engine.py` | `run_movement/shooting/charge/fight`: сейчас строят `default_action_dict`, теряя вторичные головы | Modify |
| `tools/windowed_parity_winrate.py` | Обёртка над `mcts_winrate_baseline` для прогона windowed 0 vs 1 на фикс. сидах | Create |
| `docs/superpowers/plans/2026-06-18-windowed-selfplay-parity-fix.md` | Этот план | (создан) |

**Принцип фиксов (ключевой вывод диагностики):** при исполнении **плоского** policy/MCTS-действия windowed-путь должен **делегировать чтение голов legacy-фазам** — т.е. прокидывать **реальный** `action_dict` (как `base_action`) и `decide_*`, возвращающий **сырое** значение головы (`action[move_num_i]`, `action[shoot]`, `action[attack]/[charge]`), а не «снаппить» к опции окна и не форсить STAY/PASS. Это даёт гарантированный паритет с legacy. Структура окон при этом сохраняется (для replay-meta и будущего per-window пути Part B), но **не влияет на исполнение** плоского действия. PhaseEngine получает опциональный `base_action` (по умолчанию — прежний `default_action_dict`, чтобы не ломать другие вызовы и golden-trace). После этого единого фикса Tasks 3–5 — в основном **валидационные гейты** (правка decide нужна только если харнесс по фазе всё ещё красный).

---

## Task 1 — Per-phase parity-харнесс (диагностика)

**Files:**
- Create: `tests/engine/phases/test_windowed_legacy_parity.py`
- Read-ref: `tests/engine/phases/_helpers.py` (`build_env`, `make_unit`), `tests/engine/phases/test_windowed_selfplay_turn_parity.py` (паттерн snapshot/restore)

**Interfaces:**
- Consumes: `core.engine.phases.windowed_selfplay.run_model_turn_from_action(env, action_dict)`; legacy `env.command_phase/movement_phase/shooting_phase/charge_phase/fight_phase`; `env.snapshot_state()/restore_state()/simulation_mode()`.
- Produces: тест `test_parity_per_phase` (параметры `phase ∈ {command,movement,shooting,charge,fight}` × `move_num_override ∈ {legal, out_of_range}`), `test_parity_full_turn`; хелперы `_engaged_setup(env)`, `_action(env, n, move_num_override=None)`, `_legal_move_num(env, u)`, `_snap(env)`.
- Примечание по выбору тестов: из-за двойной параметризации node-id вида `[legal-movement]`; в командах ниже используем `-k "<phase>"` (подстрока), а не точный `::test[...]`.

Цель: в отличие от существующего `test_windowed_turn_matches_legacy_phases` (тривиальный `move=4, move_num=0` — обе ветки стоят), здесь сценарий **боевой** и действие **нетривиальное**, чтобы расхождение проявилось и было локализовано по фазам.

- [ ] **Step 1: Написать падающий per-phase parity-тест**

```python
# tests/engine/phases/test_windowed_legacy_parity.py
import random
import numpy as np
import pytest

from core.engine.phases.windowed_selfplay import (
    run_model_command_from_action,
    run_model_movement_from_action,
    run_model_shooting_from_action,
    run_model_charge_from_action,
    run_model_fight_from_action,
    run_model_turn_from_action,
)
from tests.engine.phases._helpers import build_env


def _engaged_setup(env):
    """Юниты модели в дальности стрельбы и чарджа от врага (чтобы фазы реально работали)."""
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [10, 10]
    env.unit_coords[1] = [11, 11]
    env.enemy_coords[0] = [14, 12]   # в радиусе стрельбы и ~чарджа
    env.enemy_coords[1] = [16, 13]
    env.enemyCP = 0
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    env._invalidate_target_cache("test")


def _legal_move_num(env, u: int) -> int:
    """Первый НЕ-STAY легальный reachable-индекс юнита (1, если есть move_cells, иначе 0=STAY).
    Берём из overlay, а не хардкодим — иначе тест ловит fixture, а не баг."""
    overlay = env.get_unit_movement_overlay("model", int(u))
    move_cells = list(overlay.get("move_cells") or [])
    return 1 if move_cells else 0


def _action(env, n: int, *, move_num_override: int | None = None) -> dict:
    """Нетривиальное действие. move_num по умолчанию — первый легальный (динамически).

    ВАЖНО (механизм из пункта 3): реальное действие в self-play факторизовано по головам
    (_final_policy_from_visits), поэтому move_num_{u} часто оказывается ВНЕ reachable конкретного
    юнита — это и есть триггер расхождения windowed(STAY) vs legacy(фолбэк по move). Поэтому
    параметризуем тест и на легальный, и на out-of-range move_num.
    """
    a = {"move": 0, "attack": 1, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0}
    for i in range(n):
        a[f"move_num_{i}"] = move_num_override if move_num_override is not None else _legal_move_num(env, i)
    return a


def _snap(env) -> dict:
    return {
        "unit_coords": [list(c) for c in env.unit_coords],
        "enemy_health": [round(float(h), 2) for h in env.enemy_health],
        "unit_health": [round(float(h), 2) for h in env.unit_health],
        "unit_in_attack": [list(x) for x in env.unitInAttack],
        "enemy_in_attack": [list(x) for x in env.enemyInAttack],
        "model_cp": int(env.modelCP),
    }


def _run_legacy_phase(env, phase: str, action, n):
    if phase == "command":
        env.command_phase("model", action=action)
    elif phase == "movement":
        bs = [False] * n
        env.movement_phase("model", action=action, battle_shock=bs)
    elif phase == "shooting":
        env.shooting_phase("model", advanced_flags=[False] * n, action=action)
    elif phase == "charge":
        env.charge_phase("model", advanced_flags=[False] * n, action=action)
    elif phase == "fight":
        env.fight_phase("model")


def _run_windowed_phase(env, phase: str, action):
    if phase == "command":
        run_model_command_from_action(env, action)
    elif phase == "movement":
        run_model_movement_from_action(env, action)
    elif phase == "shooting":
        run_model_shooting_from_action(env, action)
    elif phase == "charge":
        run_model_charge_from_action(env, action)
    elif phase == "fight":
        run_model_fight_from_action(env, action)


# move_num=None → легальный (динамически); =999 → заведомо out-of-range (живой триггер расхождения).
@pytest.mark.parametrize("move_num_override", [None, 999], ids=["legal", "out_of_range"])
@pytest.mark.parametrize("phase", ["command", "movement", "shooting", "charge", "fight"])
def test_parity_per_phase(monkeypatch, phase, move_num_override):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    env = build_env()
    _engaged_setup(env)
    n = len(env.unit_health)
    action = _action(env, n, move_num_override=move_num_override)
    snap = env.snapshot_state()

    random.seed(7); np.random.seed(7)
    with env.simulation_mode():
        _run_legacy_phase(env, phase, action, n)
        legacy = _snap(env)
    env.restore_state(snap)

    random.seed(7); np.random.seed(7)
    with env.simulation_mode():
        _run_windowed_phase(env, phase, action)
        windowed = _snap(env)
    env.restore_state(snap)

    assert legacy == windowed, f"расхождение в фазе {phase}: legacy != windowed"
```

- [ ] **Step 2: Прогнать тест — зафиксировать, какие фазы расходятся**

Run: `python -m pytest tests/engine/phases/test_windowed_legacy_parity.py -v`
Expected: одна или несколько фаз — **FAIL** (это и есть локализация). Записать в PR-заметку, какие именно фазы упали и чем отличается `_snap` (координаты/HP/in_attack/CP).

- [ ] **Step 3: Зафиксировать диагноз в плане-исполнении (без правок кода)**

Закоммитить только новый тест-файл как диагностический артефакт (он останется регресс-гейтом). Фазы, что упали, определяют, какие из Task 2–5 реально нужны (зелёные фазы → их фикс-тест пройдёт сразу, фикс будет no-op).

```bash
git add tests/engine/phases/test_windowed_legacy_parity.py
git commit -m "test(phases): per-phase windowed<->legacy parity harness (диагностика регрессии 8.4)"
```

---

## Task 2 — PhaseEngine принимает реальный `base_action` (устранить потерю вторичных голов)

**Files:**
- Modify: `core/engine/phases/phase_engine.py` (`run_movement`, `run_shooting`, `run_charge`)
- Modify: `core/engine/phases/windowed_selfplay.py` (`run_model_movement/shooting/charge_from_action`)
- Test: `tests/engine/phases/test_windowed_legacy_parity.py` (уже создан в Task 1)

**Interfaces:**
- Produces: новая сигнатура `phase_engine.run_movement(env, side, decide, state=None, *, base_action=None)` (аналогично `run_shooting`, `run_charge`); при `base_action is None` поведение прежнее (`default_action_dict`). Мост передаёт реальный `action_dict`.
- Consumes: существующие `legacy_compiler.default_action_dict`, `env.movement_phase(..., action=...)`.

Причина: сейчас `run_movement` строит `action = default_action_dict(len(health))` (`move=4`), из-за чего legacy-фолбэк по направлению `move` мёртв, а несопоставленный `move_num` форсится в STAY через `decide_move=lambda i: chosen_idx.get(i, 0)`. Прокидываем реальный `action` и не подменяем на STAY, когда выбор не сопоставлен (возвращаем сырой `move_num`, чтобы сработал штатный legacy-фолбэк).

- [ ] **Step 1: Подтвердить падение movement-парити (из Task 1)**

Run: `python -m pytest tests/engine/phases/test_windowed_legacy_parity.py -k "movement" -v`
Expected: FAIL (если movement в Task 1 упал). Если PASS — этот таск no-op, перейти к Task 3, но всё равно внести `base_action` (безопасно, дефолт сохраняет поведение).

- [ ] **Step 2: Добавить `base_action` в `phase_engine.run_movement`**

```python
# core/engine/phases/phase_engine.py — run_movement
def run_movement(env, side, decide, state: PhaseTurnState | None = None, *, base_action=None) -> PhaseTurnState:
    e = _unwrap(env)
    state = _ensure_state(e, side, state)
    health = e.unit_health if side == "model" else e.enemy_health
    alive = [i for i, hp in enumerate(health) if hp > 0]
    chosen_idx: dict[int, int] = {}
    for u in alive:
        opts = movement_options_for_unit(e, side, u)
        win = DecisionWindow(
            window_id=f"movement:{side}:{u}", owner_side=side, phase=Phase.MOVEMENT,
            sub_step=SubStep.MOVE_UNIT, timing=Timing.MAIN, cursor_unit_idx=int(u), options=opts,
        )
        opt = decide(win)
        if opt is not None and opt.param.get("reachable_index") is not None:
            chosen_idx[int(u)] = int(opt.param["reachable_index"])
    action = dict(base_action) if base_action is not None else default_action_dict(len(health))
    # Паритет: при наличии реального base_action исполняем СЫРОЙ move_num (как legacy want=action[move_num_i]),
    # не снаппя к опции окна. chosen_idx остаётся для replay-meta. Без base_action — прежнее окно-поведение.
    if base_action is not None:
        decide_move = lambda i: int(action.get(f"move_num_{i}", 0))  # noqa: E731
    else:
        decide_move = lambda i: chosen_idx.get(i, 0)  # noqa: E731
    result = e.movement_phase(
        side, action=action,
        battle_shock=list(state.battle_shock or [False] * len(health)),
        decide_move=decide_move,
    )
    if isinstance(result, tuple):
        advanced_flags = result[0] if len(result) > 0 else []
        reward_delta = float(result[1] or 0.0) if len(result) > 1 else 0.0
        if len(result) > 2:
            state.info["movement_meta"] = result[2]
    else:
        advanced_flags = result if result is not None else state.advanced_flags
        reward_delta = 0.0
    state.advanced_flags = list(advanced_flags or [False] * len(health))
    state.reward_delta += reward_delta
    state.info["movement_reward_delta"] = reward_delta
    _sync_positions(e)
    _invalidate(e, f"phase_engine_after_movement:{side}")
    return state
```

Примечание: `decide_move` теперь для несопоставленного юнита возвращает **сырой** `move_num_{i}` из реального действия (а не 0/STAY), что включает штатный legacy-фолбэк `_pick_destination_from_overlay` по голове `move`.

- [ ] **Step 3: Прокинуть реальный `action_dict` из моста**

```python
# core/engine/phases/windowed_selfplay.py
def run_model_movement_from_action(env, action_dict: dict | None, state=None):
    decide = make_movement_decide_from_action_dict(action_dict)
    return phase_engine.run_movement(env, "model", decide, state, base_action=action_dict)
```

- [ ] **Step 4: Зеркально добавить `base_action` в `run_shooting` и `run_charge`**

```python
# core/engine/phases/phase_engine.py — run_shooting (сигнатура: ..., *, base_action=None)
    action = dict(base_action) if base_action is not None else default_action_dict(len(health))
    # Паритет: при base_action не передаём decide_shoot — shooting_phase сам читает action["shoot"] (как legacy).
    decide_shoot = None if base_action is not None else (lambda i: chosen_rank.get(i, -1))
    result = e.shooting_phase(
        side, advanced_flags=list(state.advanced_flags or [False] * len(health)),
        action=action, decide_shoot=decide_shoot,
    )

# run_charge (аналогично, сигнатура: ..., *, base_action=None):
    action = dict(base_action) if base_action is not None else default_action_dict(len(health))
    # Паритет: при base_action не передаём decide_charge — charge_phase читает action["attack"]/["charge"] (legacy).
    decide_charge = None if base_action is not None else (lambda i: chosen_target.get(i))
    result = e.charge_phase(
        side, advanced_flags=list(state.advanced_flags or [False] * len(health)),
        action=action, decide_charge=decide_charge,
    )
```

```python
# core/engine/phases/windowed_selfplay.py
def run_model_shooting_from_action(env, action_dict: dict | None, state=None):
    decide = make_shooting_decide_from_action_dict(action_dict)
    return phase_engine.run_shooting(env, "model", decide, state, base_action=action_dict)

def run_model_charge_from_action(env, action_dict: dict | None, state=None):
    decide = make_charge_decide_from_action_dict(action_dict)
    return phase_engine.run_charge(env, "model", decide, state, base_action=action_dict)
```

- [ ] **Step 5: Прогнать movement-парити**

Run: `python -m pytest tests/engine/phases/test_windowed_legacy_parity.py -k "movement" -v`
Expected: PASS.

- [ ] **Step 6: Прогнать существующие тесты (не сломать тривиальный паритет и golden-trace)**

Run: `python -m pytest tests/engine/phases/ -q`
Expected: all PASS (включая `test_windowed_selfplay_turn_parity.py` с `WINDOWED_SELFPLAY=0/1`).

- [ ] **Step 7: Commit**

```bash
git add core/engine/phases/phase_engine.py core/engine/phases/windowed_selfplay.py
git commit -m "fix(phases): PhaseEngine принимает base_action — windowed не теряет голову move и не форсит STAY"
```

---

## Task 3 — Charge-парити (gate `attack` и набор целей)

> **РЕГРЕСС-ГЕЙТ (после Task 2).** При `base_action` `run_charge` передаёт `decide_charge=None` — `charge_phase` читает `action["attack"]/["charge"]` напрямую (= legacy), поэтому правки в `make_charge_decide_from_action_dict` на **исполнение не влияют** (только на путь без `base_action` / будущий per-window Part B). Меняем decide **только если** `test_parity_per_phase[charge-*]` остался красным после Task 2.

**Files:**
- Modify: `core/engine/phases/windowed_selfplay.py` (`make_charge_decide_from_action_dict`)
- Test: `tests/engine/phases/test_windowed_legacy_parity.py`

**Interfaces:**
- Consumes: `env.get_charge_targets_for_unit(side, u)`; `ActionKind.CHARGE`.
- Produces: исправленный `make_charge_decide_from_action_dict`, согласованный с legacy `charge_phase` (где `_do_charge = action["attack"]==1` для всех юнитов, цель — глобальный `action["charge"]`).

Причина: legacy при `attack==1` заставляет **каждый** юнит с целями катить 2d6 и объявлять чардж по глобальному `charge`, если тот в `chargeAble`. Windowed-decide объявляет чардж только если глобальный `charge` входит в `get_charge_targets_for_unit(u)` (12"-предфильтр). Привести к одному критерию.

- [ ] **Step 1: Подтвердить статус charge-парити**

Run: `python -m pytest tests/engine/phases/test_windowed_legacy_parity.py -k "charge" -v`
Expected: FAIL → чинить ниже; PASS → таск no-op (зафиксировать и пропустить).

- [ ] **Step 2: Согласовать decide с legacy-критерием**

```python
# core/engine/phases/windowed_selfplay.py
def make_charge_decide_from_action_dict(action_dict: dict | None):
    """attack==1 → CHARGE по глобальному charge для каждого юнита, у кого цель в его charge-окне.
    Согласовано с legacy charge_phase: цель — единый action['charge'], gate — action['attack']==1."""
    attack = _action_int(action_dict, "attack", 0)
    charge_target = _action_int(action_dict, "charge", 0)

    def decide(window: DecisionWindow) -> ActionOption:
        if attack != 1:
            return _pick_pass(window)
        for opt in window.options:
            if opt.kind is ActionKind.CHARGE and opt.target_idx is not None and int(opt.target_idx) == charge_target:
                return opt
        return _pick_pass(window)

    return decide
```

(Если Task 1 показал расхождение из-за того, что у юнита нет опции на глобальную цель, но legacy всё равно катит и фейлит, — паритет достигается тем, что в обоих случаях итог «чарджа нет». Тест из Task 1 это проверит на конкретном `_snap`.)

- [ ] **Step 3: Прогнать charge-парити**

Run: `python -m pytest tests/engine/phases/test_windowed_legacy_parity.py -k "charge" -v`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add core/engine/phases/windowed_selfplay.py
git commit -m "fix(phases): charge windowed согласован с legacy (gate attack, единая цель)"
```

---

## Task 4 — Shooting-парити (множественная стрельба юнитов)

> **РЕГРЕСС-ГЕЙТ (после Task 2).** При `base_action` `run_shooting` передаёт `decide_shoot=None` — `shooting_phase` читает `action["shoot"]` напрямую (= legacy), поэтому правки в `make_shooting_decide_from_action_dict` на **исполнение не влияют**. Меняем decide **только если** `test_parity_per_phase[shooting-*]` остался красным после Task 2.

**Files:**
- Modify: `core/engine/phases/windowed_selfplay.py` (`make_shooting_decide_from_action_dict`)
- Test: `tests/engine/phases/test_windowed_legacy_parity.py`

**Interfaces:**
- Consumes: `ActionKind.SHOOT`, `opt.param["local_rank"]`.
- Produces: исправленный `make_shooting_decide_from_action_dict`, согласованный с legacy `shooting_phase` (где `raw = action["shoot"]` применяется к каждому юниту; вне диапазона → пропуск).

Причина: убедиться, что windowed-decide для каждого юнита возвращает SHOOT по `local_rank == action["shoot"]`, а при отсутствии такого ранга — пропуск (как legacy: `0 <= raw < len(valid)` иначе skip). Текущая реализация уже близка; задача — закрыть тестом и поправить кромочные случаи, если Task 1 показал расхождение.

- [ ] **Step 1: Подтвердить статус shooting-парити**

Run: `python -m pytest tests/engine/phases/test_windowed_legacy_parity.py -k "shooting" -v`
Expected: FAIL → чинить; PASS → no-op.

- [ ] **Step 2: Привести decide к legacy-семантике ранга**

```python
# core/engine/phases/windowed_selfplay.py
def make_shooting_decide_from_action_dict(action_dict: dict | None):
    """shoot — общий ранг на ход; каждый юнит стреляет в свою цель ранга shoot, иначе пропуск (как legacy)."""
    shoot_rank = _action_int(action_dict, "shoot", 0)

    def decide(window: DecisionWindow) -> ActionOption:
        for opt in window.options:
            if opt.kind is ActionKind.SHOOT and int(opt.param.get("local_rank", -1)) == shoot_rank:
                return opt
        return _pick_pass(window)

    return decide
```

- [ ] **Step 3: Прогнать shooting-парити**

Run: `python -m pytest tests/engine/phases/test_windowed_legacy_parity.py -k "shooting" -v`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add core/engine/phases/windowed_selfplay.py
git commit -m "fix(phases): shooting windowed согласован с legacy (общий ранг на ход)"
```

---

## Task 5 — Fight-парити + полный ход

> **РЕГРЕСС-ГЕЙТ (после Task 2).** `run_model_fight_from_action` уже вызывает `env.fight_phase` (как legacy). Меняем `run_model_fight_from_action` **только если** fight/full_turn красные после Task 2 (частый кейс — `_pending_fight_stratagem_plan` / порядок очистки плана).

**Files:**
- Modify: `core/engine/phases/windowed_selfplay.py` (`run_model_fight_from_action`) при необходимости
- Test: `tests/engine/phases/test_windowed_legacy_parity.py`

**Interfaces:**
- Consumes: `env.fight_phase(side)`, `stratagem_engine.apply`, `_pending_fight_stratagem_plan`.
- Produces: parity для fight и для полного хода `run_model_turn_from_action`.

Причина: урон ближнего боя считает один и тот же `env.fight_phase(side)`; расхождение возможно только из-за порядка применения стратагем/дедупа `_pending_fight_stratagem_plan`. Закрыть тестом fight и full_turn.

- [ ] **Step 1: Добавить full-turn parity-тест (legal + out_of_range)**

```python
# tests/engine/phases/test_windowed_legacy_parity.py — добавить
@pytest.mark.parametrize("move_num_override", [None, 999], ids=["legal", "out_of_range"])
def test_parity_full_turn(monkeypatch, move_num_override):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    env = build_env()
    _engaged_setup(env)
    n = len(env.unit_health)
    action = _action(env, n, move_num_override=move_num_override)
    snap = env.snapshot_state()

    random.seed(7); np.random.seed(7)
    with env.simulation_mode():
        bs, _ = env.command_phase("model", action=action)
        env.movement_phase("model", action=action, battle_shock=bs)
        env.shooting_phase("model", advanced_flags=[False] * n, action=action)
        env.charge_phase("model", advanced_flags=[False] * n, action=action)
        env.fight_phase("model")
        legacy = _snap(env)
    env.restore_state(snap)

    random.seed(7); np.random.seed(7)
    with env.simulation_mode():
        run_model_turn_from_action(env, action)
        windowed = _snap(env)
    env.restore_state(snap)

    assert legacy == windowed
```

- [ ] **Step 2: Прогнать fight и full_turn**

Run: `python -m pytest tests/engine/phases/test_windowed_legacy_parity.py -k "fight or full_turn" -v`
Expected: PASS (если расходится — выровнять порядок применения стратагем в `run_model_fight_from_action`, чтобы совпадал с legacy fight_phase; код правки определяется конкретным `_snap`-диффом).

- [ ] **Step 3: Commit**

```bash
git add tests/engine/phases/test_windowed_legacy_parity.py core/engine/phases/windowed_selfplay.py
git commit -m "test(phases): fight + full-turn windowed<->legacy parity; выравнивание fight при необходимости"
```

---

## Task 6 — Фолбэк move_num не «тихий» в windowed-пути (правило AGENTS.md)

> **Поправка по ревью:** НЕ добавляем декоративный лог в `make_movement_decide_from_action_dict` — после Task 2 исполнение идёт через legacy `movement_phase` + сырой `move_num`, а out-of-range уже логируется в `warhamEnv._pick_destination_by_reachable_index` (строка ~2176: `move_num_{idx}={choice} вне диапазона reachable[0..{total-1}]`). Задача — **зафиксировать тестом**, что сообщение доходит в windowed-пути; дублирующий лог в `phase_engine` — только если тест красный.

**Files:**
- Test: `tests/engine/phases/test_windowed_legacy_parity.py`
- Modify (только если тест красный): `core/engine/phases/phase_engine.py` (`run_movement`) — продублировать пояснение через `e._log(...)` в месте, где видно out-of-range.

**Interfaces:**
- Consumes: `env._log` (движковый логгер; монкипатчим в тесте для перехвата), существующий лог `_pick_destination_by_reachable_index`.
- Produces: гарантия, что out-of-range `move_num` объяснён в логе при `WINDOWED_SELFPLAY=1`.

- [ ] **Step 1: Тест — out-of-range move_num логируется в windowed-пути (перехват `env._log`)**

```python
# tests/engine/phases/test_windowed_legacy_parity.py — добавить
def test_movement_out_of_range_is_logged(monkeypatch):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    env = build_env()
    _engaged_setup(env)
    n = len(env.unit_health)
    action = _action(env, n, move_num_override=999)  # заведомо вне reachable

    captured: list[str] = []
    monkeypatch.setattr(env, "_log", lambda msg: captured.append(str(msg)))

    with env.simulation_mode():
        run_model_movement_from_action(env, action)

    assert any("move_num" in m and "вне диапазона reachable" in m for m in captured), (
        "out-of-range move_num должен быть объяснён в логе (не тихий пропуск)"
    )
```

- [ ] **Step 2: Прогнать тест**

Run: `python -m pytest "tests/engine/phases/test_windowed_legacy_parity.py::test_movement_out_of_range_is_logged" -v`
Expected: PASS (после Task 2 windowed идёт через `movement_phase` → существующий лог `_pick_destination_by_reachable_index` срабатывает).

- [ ] **Step 3: (Условно) добавить лог, если тест красный**

Если Step 2 — FAIL (сообщение не дошло), добавить в `phase_engine.run_movement` после сбора `chosen_idx`:

```python
# core/engine/phases/phase_engine.py — внутри run_movement, после построения chosen_idx, если base_action задан
    if base_action is not None:
        for u in alive:
            want = int(base_action.get(f"move_num_{u}", 0))
            n_opts = len(movement_options_for_unit(e, side, u))
            if not (0 <= want < n_opts):
                e._log(
                    f"{side} юнит {u}: move_num_{u}={want} вне диапазона reachable[0..{n_opts - 1}] "
                    f"→ фолбэк по legacy-движению. Где: phase_engine.run_movement."
                )
```

- [ ] **Step 4: Commit**

```bash
git add tests/engine/phases/test_windowed_legacy_parity.py core/engine/phases/phase_engine.py
git commit -m "test(phases): out-of-range move_num не тихий в windowed-пути (регресс-гейт)"
```

---

## Task 7 — Winrate-валидация windowed=0 vs =1 и условный возврат дефолта

**Files:**
- Create: `tools/windowed_parity_winrate.py`
- Read-ref: `tools/mcts_winrate_baseline.py`

**Interfaces:**
- Consumes: существующий прогон эпизодов из `mcts_winrate_baseline` (импорт `run_modes`/`main`-логики или повторный вызов через subprocess с env `WINDOWED_SELFPLAY`).
- Produces: печать таблицы `windowed=0` vs `windowed=1`: winrate, turn_limit_rate, wipeout_enemy_rate на одинаковых сидах.

- [ ] **Step 1: Скрипт-обёртка прогоняет оба режима на фикс. сидах**

```python
# tools/windowed_parity_winrate.py
"""Сравнение агрессии windowed=0 vs windowed=1 на одинаковых сидах (after-fix gate).

Запуск: python tools/windowed_parity_winrate.py --episodes 100 --seed 1000
"""
import argparse
import os
import subprocess
import sys


def _run(windowed: str, episodes: int, seed: int) -> str:
    env = dict(os.environ)
    env["WINDOWED_SELFPLAY"] = windowed
    env["TRAIN_ALGO"] = "az"
    cmd = [sys.executable, "tools/mcts_winrate_baseline.py",
           "--episodes", str(episodes), "--seed", str(seed), "--modes", "option"]
    out = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8")
    return out.stdout + out.stderr


def main() -> int:
    p = argparse.ArgumentParser(description="windowed 0 vs 1 winrate parity")
    p.add_argument("--episodes", type=int, default=100)
    p.add_argument("--seed", type=int, default=1000)
    args = p.parse_args()
    for w in ("0", "1"):
        print(f"=== WINDOWED_SELFPLAY={w} ===", flush=True)
        print(_run(w, args.episodes, args.seed), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Прогнать сравнение**

Run: `python tools/windowed_parity_winrate.py --episodes 100 --seed 1000`
Expected: две таблицы; разница winrate/turn_limit между windowed=0 и =1 в пределах шума (|Δwinrate| ≲ 5 п.п.). Зафиксировать числа в PR.

- [ ] **Step 3: Условие возврата дефолта**

Если паритет достигнут (windowed=1 ≈ windowed=0 по winrate и turn_limit) — `windowed_selfplay` можно оставлять дефолтным `1`. Если windowed=1 всё ещё хуже — **оставить дефолт `0`** в `hyperparams.json` (секция `alphazero_tree`) и завести задачу на доисследование (вернуться к Task 1 с расширенным сценарием). Записать решение в `artifacts/results/results.txt` строкой с числами.

- [ ] **Step 4: Commit**

```bash
git add tools/windowed_parity_winrate.py
git commit -m "tools: winrate-гейт windowed 0 vs 1 (после паритет-фиксов)"
```

---

## Verification checklist (перед «готово»)

- [ ] `python -m pytest tests/engine/phases/ -q` — all green (новый parity-харнесс + старые тесты).
- [ ] `test_parity_per_phase[*]` и `test_parity_full_turn` — PASS (паритет достигнут).
- [ ] `python tools/windowed_parity_winrate.py --episodes 100 --seed 1000` — |Δ| по winrate/turn_limit в пределах шума; числа задокументированы.
- [ ] `WINDOWED_SELFPLAY=0` golden-trace не затронут (паритетные тесты с флагом 0).
- [ ] `engine-regression-reviewer` на дифф `core/engine/phases/`, при правках `warhamEnv` — тоже.
- [ ] Решение по дефолту `windowed_selfplay` (0 или 1) зафиксировано в `artifacts/results/results.txt`.
- [ ] Не закоммичены runtime-логи / временные файлы.

---

## Out of scope — Part B (отдельный план, нужен brainstorming)

Эти пункты **не входят** в Part A (они меняют action-контракт / сети / чекпойнты и требуют отдельного дизайна через `superpowers:brainstorming` → `writing-plans`):

1. **Стратагемы / Command Points как действия политики** — сейчас `use_cp/cp_on` почти не используются (eval: `cp_used=0`). Нужен дизайн голов/масок для выбора стратагемы и юнита (Insane Bravery, Hungry Void, Command Re-roll, Awakened Dynasty), их подача в obs и в MCTS-кандидаты.
2. **Per-unit `shoot_{u}` / `charge_{u}` головы** — снять lossy single-head (один стреляющий/чарджащий юнит за ход). Меняет `ordered_action_keys`, размер action-пространства, сети всех алго, совместимость старых чекпойнтов.
3. **Реакции как отдельные окна** (Overwatch и пр.) — `generate_windows` с `timing=REACTION` + `reaction_policy` в self-play (Stage 8.4g, сейчас дефолт off).
4. **MCTS-узлы = decision windows** (Stage 8.4f, `mcts_window_nodes`) — включать только после Part A и winrate-harness.
5. **Joint action selection из best child** (вместо per-head sample). Подтверждено в `core/models/alphazero_mcts.py` → `_final_policy_from_visits` (~489–532): финальное действие — **независимый** argmax/sample по головам из маргинальных visits, исполняемый `action_dict` может быть некогерентным (нет ни в одном child). Part A это **не чинит** (winrate 0 vs 1: оба пути исполняют один dict), но для **обучения** нужен выбор `action_tuple` лучшего child + согласование policy-таргетов. Черновик фикса: в `option` mode после search взять `argmax_child.action_tuple`, а `policy_targets` оставить маргинальными для IL.
6. **Obs-фичи CP/стратагем (Stage 8.1)** — без них сеть «слепа» к моменту траты CP даже при правильном action space.

Каждый из пунктов 1–6 — самостоятельный план; 2, 4, 5 — высокий риск, начинать с brainstorming.

---

## Журнал исполнения (заполнять по ходу)

| Task | Статус | Примечание |
|------|--------|------------|
| 1 parity-харнесс | ✅ | 10 per-phase + full_turn + log |
| 2 base_action | ✅ | phase_engine + windowed bridge |
| 3 charge gate | ✅ | no-op (зелёный после Task 2) |
| 4 shooting gate | ✅ | no-op |
| 5 fight + full_turn | ✅ | fix теста advanced_flags в legacy |
| 6 log out-of-range | ✅ | через warhamEnv._log |
| 7 winrate 0 vs 1 | ⬜ | см. artifacts/results |
| дефолт hyperparams | 0 | пока windowed=0 в alphazero_tree |
