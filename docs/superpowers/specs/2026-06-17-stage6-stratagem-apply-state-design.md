# Stage 6 — StratagemEngine.apply + StratagemState (behavior-neutral) — Design

**Дата:** 2026-06-17
**Ветка:** `feat/phase-decision-windows`
**Контекст:** продолжение слоя `core/engine/phases/` (Stage 1–3 + Stage 5 готовы: типы окон, генератор опций, компилятор, реестр стратагем + read-only легальность). Это **первая стадия, трогающая движок** `core/envs/warhamEnv.py`.

## Цель

Единая точка **списания CP** для стратагем (`StratagemEngine.apply`) + **журнал использования** на env, который попадает в `snapshot_state`/`restore_state`. Insane Bravery (единственная агент-управляемая стратагема) проводится через эту точку. **Поведение игры идентично** (golden-trace): меняется только то, что CP-расход теперь идёт через один метод и пишется в журнал, который пока ничего не гейтит.

## Не-цели (явно вне Stage 6)

- Любое **enforcement** лимитов (once-per-phase/turn/battle) — отложено (выбор пользователя: behavior-neutral). Журнал пишется, но не используется для запрета.
- Превращение реакций (Overwatch/Smokescreen/Heroic) в агент-решаемые окна — **Stage 7** (нужно поэтапное исполнение хода).
- Маршрутизация CP-расхода **врага** (heuristic/random opponent) через `apply` — вне фокуса; враг не учится. Остаётся как есть.
- `active_buffs` как отдельная структура — пока не нужно (эффекты cover уже живут в `modelStrat`/`effect`); YAGNI.

## Глобальные ограничения

- Платформа Windows; Python 3.12+; тесты — `python -m pytest`; ruff `py312`, line-length 120, `StrEnum`.
- Язык докстрингов/сообщений — русский; ошибка = что + где + что делать.
- `core/engine/phases/*` НЕ импортирует `core/envs/*` (функции принимают `env` параметром; цикла нет). `warhamEnv.py` импортирует `core/engine/phases` — допустимо (один слой).
- **Инвариант поведения:** исход `env.step` из одного snapshot обязан совпадать до/после рефактора (golden-trace). Insane Bravery остаётся: применяется при `use_cp==1 & cp_on==i` и наличии ≥1 CP; награда/штраф/battle-shock — без изменений.

## Соответствие коду (что трогаем)

- Insane Bravery (model), инлайн-расход CP: `warhamEnv.py:4332-4345` — заменяем `if self.modelCP - 1 >= 0: ... self.modelCP -= 1` на вызов `apply`, ветки reward/log сохраняем 1:1.
- `snapshot_state`: `warhamEnv.py:1134` (списки/скаляры/strat-dicts), `restore_state`: `:1243`.
- `_enemy_cp_on`/`_enemy_use_cp`: ставятся `:4466-4467`, читаются `:5113-5114` (внутри одного `enemyTurn` ставятся раньше чтения → утечка безвредна, но добавим в snapshot для чистоты).

## Архитектура

### Журнал использования (на env, чтобы попасть в snapshot)

- `env.stratagem_used: list[tuple[str, str, int]]` — записи `(side, stratagem_id, battle_round)`. Инициализируется `[]` в `__init__` и сбрасывается в `[]` в `reset()` (новый бой). Не чистится по фазам/ходам — это журнал на весь бой.

### StratagemEngine.apply (в слое phases)

```
def apply(env, side: str, stratagem_id: str, unit_idx: int | None = None) -> dict
```
- `d = by_id(stratagem_id)`; `cp = env.modelCP|enemyCP` (через `_unwrap`).
- Если `cp < d.cp_cost` → вернуть `{"ok": False, "reason": "not_enough_cp", "cp_spent": 0}` (CP НЕ трогаем).
- Иначе: списать `cp_cost` (`env.modelCP -= d.cp_cost` либо enemy), добавить запись в `env.stratagem_used` (`(side, id, env.battle_round)`), вернуть `{"ok": True, "cp_spent": d.cp_cost}`.
- Read-only по части решения «можно ли» — само списание единообразно тут.

### Интеграция в command_phase (model, Insane Bravery)

Заменяем (псевдо):
```
if self.modelCP - 1 >= 0:
    battle_shock[i] = False; reward += BONUS; log; self.modelCP -= 1
else:
    reward -= PENALTY; log
```
на:
```
res = stratagem_engine.apply(self, "model", "insane_bravery", i)
if res["ok"]:
    battle_shock[i] = False; reward += BONUS; log
else:
    reward -= PENALTY; log
```
Условие `modelCP-1>=0` ⟺ `cp>=cost=1` ⟺ `res["ok"]` → ветки идентичны. Награда/логи/battle-shock не меняются. Дополнительно теперь есть запись в журнал.

### snapshot_state / restore_state

- Добавить `stratagem_used` в копирование (list-of-tuples: `[tuple(x) for x in ...]` при snapshot, `list(...)` при restore).
- Добавить `_enemy_cp_on`, `_enemy_use_cp` в набор скаляров (default `None`).

## Поток данных

`command_phase(model)` → `apply` списывает CP + пишет журнал → reward/battle-shock как раньше. `snapshot_state` сериализует журнал и enemy-cp-поля; `restore_state` их возвращает. Никто журнал не читает для решений (Stage 6).

## Обработка ошибок

- `apply` с неизвестным `stratagem_id` → пробрасывает `KeyError` из `by_id` (баг вызывающего, должно падать явно).
- `apply` при нехватке CP → `{"ok": False}` без побочных эффектов (не исключение): нормальная ветка (агент выбрал Bravery без CP — текущий штраф сохраняется вызывающим).

## Тест-план

`tests/engine/phases/test_stratagem_engine.py`:
1. `apply` списывает ровно `cp_cost`, пишет запись `(side,id,battle_round)`, `ok=True` (model и enemy).
2. `apply` при `cp=0` → `{"ok": False, "reason":"not_enough_cp", "cp_spent":0}`, CP и журнал не изменились.
3. `apply` с неизвестным id → `KeyError`.

`tests/engine/phases/test_snapshot_stratagem_state.py`:
4. snapshot→ `apply` (мутация CP+журнал) →restore → CP, `stratagem_used`, `_enemy_cp_on/_enemy_use_cp` вернулись к снимку.

`tests/engine/phases/test_no_behavior_change.py` (расширить) или новый golden-trace:
5. **Поведение `env.step` идентично**: из одного snapshot прогон с `action(use_cp=1,cp_on=0)` даёт тот же `(reward, unit_health, enemy_health, modelCP, VP, coords)` — сравнение «до/после» через два прогона одинакового действия из общего snapshot (детерминизм по rng). Плюс: после хода с реально применённой Bravery в `stratagem_used` появляется запись `("model","insane_bravery",...)`.

Регрессия: весь пакет `tests/engine/phases/`, смоук движка (`test_warham_env_snapshot_restore.py`, `test_command_phase_reanimation_sync_regression.py`, `test_snapshot_slim_regression.py`), ruff.

## Риски

- **Правка delicate command_phase** (battle-shock+reward): митигейт — замена 1:1 по веткам, golden-trace тест (тест 5), смоук командной фазы.
- **snapshot_slim регрессия** (`test_snapshot_slim_regression.py` проверяет состав snapshot) — возможно, потребует обновления ожидаемых ключей; учесть при исполнении.
- **Соблазн начать enforcement** — явно вне scope (выбор behavior-neutral); журнал инертен.
