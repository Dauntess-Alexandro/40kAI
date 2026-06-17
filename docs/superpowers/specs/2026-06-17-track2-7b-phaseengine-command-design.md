# Track 2 · 7b — PhaseEngine: пошаговое командное окно — Design

**Дата:** 2026-06-17
**Ветка:** `feat/phase-decision-windows`
**Контекст:** первая фаза Track 2 (пошаговое исполнение хода по окнам). Делаем на простейшей фазе — командной (единственное решение = Insane Bravery), чтобы установить паттерн `PhaseEngine` + decision-seam, не трогая legacy `env.step`. Защита — golden-trace harness (`tests/engine/test_golden_trace_regression.py`).

## Цель

Дать `PhaseEngine`, который исполняет командную фазу как последовательность решений из `DecisionWindow`, переиспользуя существующую `command_phase` (без дублирования логики battle-shock/reanimation/scoring). **Поведение legacy `env.step` идентично** (decision-seam по умолчанию воспроизводит действие из плоского `action`).

## Не-цели (вне 7b)

- Movement/Shooting/Charge/Fight пошагово — это 7c (по одной фазе за заход).
- Замена `env.step` на windowed-драйвер / миграция обучения — Stage 8.
- Генераторное приостанавливание фаз (pull-stepping) — отложено (для 7b достаточно decision-seam).
- Подключение активных стратагем (Sudden Storm/Hungry Void) — после 7c (нужны точки решения в movement/fight).

## Глобальные ограничения

- Windows; Python 3.12+; тесты `python -m pytest`; ruff `py312`.
- `core/engine/phases/*` не импортирует `core/envs/*` (PhaseEngine принимает env параметром).
- **Инвариант:** `command_phase(..., decide_bravery=None)` ведёт себя ровно как сейчас. Golden-trace (seed 12345) обязан остаться зелёным после рефактора.

## Соответствие коду

- `command_phase` (model-ветка) `core/envs/warhamEnv.py:4345+`. Bravery-решение во вложенном `else` (battle-shock провален): сейчас `if action and action.get("use_cp") == 1 and action.get("cp_on") == i: _apply_stratagem(self, "model", "insane_bravery", i)`.
- `command_window(env, side)` / `legal_stratagem_options` — `core/engine/phases/` (даёт PASS + USE_STRATAGEM(insane_bravery, unit_idx=i)).
- golden-trace harness — `tests/engine/test_golden_trace_regression.py`.

## Архитектура

### Decision-seam в `command_phase`

Сигнатура: `command_phase(self, side, action=None, manual=False, decide_bravery=None)`.
- `decide_bravery: Callable[[int], bool] | None` — для юнита `i` (провалившего battle-shock) вернуть «применить ли Insane Bravery».
- Внутри (model-ветка), в точке решения bravery:
  ```python
  if decide_bravery is not None:
      use_bravery = bool(decide_bravery(i))
  else:
      use_bravery = bool(action and action.get("use_cp") == 1 and action.get("cp_on") == i)
  if use_bravery:
      _bravery = _apply_stratagem(self, "model", "insane_bravery", i)
      if _bravery["ok"]:
          ... (как сейчас: battle_shock[i]=False, reward+=BONUS, log)
      else:
          ... (как сейчас: reward-=PENALTY, log "нет CP")
  ```
  При `decide_bravery=None` — поведение бит-в-бит прежнее (читаем из `action`).
- Заметка: ветка `use_bravery=True`, но `apply` вернул `ok=False` (нет CP) → текущая штраф-ветка. Это сохраняет семантику «запросил, но не смог».

### `PhaseEngine` (новый модуль `core/engine/phases/phase_engine.py`)

```python
def run_command(env, side, decide):
    """Исполнить командную фазу, беря решение Insane Bravery из decide(window, option).

    decide(window, options) -> ActionOption  — выбирает опцию окна (PASS или USE_STRATAGEM).
    Реализация 7b: строим командное окно (command_window), но решение применяем
    через decide_bravery-колбэк к command_phase (переиспользуем её логику).
    """
```
Реализация (7b, без дублирования):
- `win = command_window(env, side)` — даёт опции PASS + USE_STRATAGEM(unit_idx=i) для живых при CP≥1.
- Построить множество юнитов, по которым decide выбрал bravery: для каждого USE_STRATAGEM-опции спросить `decide` (или: decide возвращает выбранную опцию; собрать `chosen_units = {opt.unit_idx}` если выбран USE_STRATAGEM).
- `env.command_phase(side, decide_bravery=lambda i: i in chosen_units)`.

Т.е. PhaseEngine инвертирует управление (внешний `decide` выбирает опции окна), а исполнение делегируется `command_phase` через seam. Один источник истины.

### Поток данных

legacy: `env.step` → `command_phase(action=...)` (decide_bravery=None) → как раньше.
windowed: внешний драйвер → `PhaseEngine.run_command(env, side, decide)` → `command_window` → `decide` выбирает опции → `command_phase(decide_bravery=...)`.

## Обработка ошибок

- `decide_bravery(i)` бросил исключение → пробросить (баг драйвера; не глотаем, чтобы не маскировать).
- `decide` вернул опцию не из окна → PhaseEngine игнорирует (трактует как PASS); лог не обязателен (read-side).

## Тест-план

`tests/engine/phases/test_phase_engine_command.py`:
1. **seam equivalence** — `command_phase(side, decide_bravery=lambda i: i==0)` для юнита 0 (ниже половины + Ld 13 → провал) применяет bravery (CP списан, журнал, battle_shock[0]=False) — как action-путь `use_cp=1/cp_on=0`. Сравнить с прямым action-вызовом из одного snapshot.
2. **seam None == legacy** — `command_phase(side, action=<use_cp=1,cp_on=0>, decide_bravery=None)` идентичен старому (golden-trace это тоже покрывает).
3. **run_command applies bravery** — `PhaseEngine.run_command(env, "model", decide=выбрать USE_STRATAGEM для unit0)` при провале → bravery применён (журнал, CP).
4. **run_command declines** — `decide`=выбирать PASS → bravery не применён, юнит в battle_shock, журнал пуст.

Регрессия (КРИТИЧНО): `tests/engine/test_golden_trace_regression.py` (поведение env.step не изменилось), весь `tests/engine/phases/`, командные тесты движка, ruff (warhamEnv не растит долг).

## Риски

- **Любое расхождение в command_phase ломает обучение** — митигейт: decision-seam по умолчанию воспроизводит action-логику, golden-trace + командные тесты как жёсткий гард.
- **PhaseEngine как сканер/костыль** — 7b сознательно тонкий (делегирует исполнение в command_phase). Реальная пошаговость нескольких решений — 7c.
- **Соблазн затащить movement** — вне scope 7b.
