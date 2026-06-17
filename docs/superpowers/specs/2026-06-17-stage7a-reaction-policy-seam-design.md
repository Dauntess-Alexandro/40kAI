# Stage 7a — Reaction policy seam (behavior-neutral) — Design

**Дата:** 2026-06-17
**Ветка:** `feat/phase-decision-windows`
**Контекст:** первый срез декомпозированного Stage 7. Stage 1–6 готовы (типы окон, генератор опций, компилятор, реестр стратагем, read-only легальность, `stratagem_engine.apply` + журнал в snapshot). Полный пошаговый rewrite хода (7b/7c) отложен — сначала делаем реакции решаемыми политикой на стабильном движке.

## Цель

Дать **подключаемый `env.reaction_policy`**, через который проходит решение «использовать ли реакцию» для трёх реакционных стратагем (Overwatch / Smokescreen / Heroic Intervention). По умолчанию (`None`) поведение **идентично текущему** (реакция всегда срабатывает). Заодно: CP-расход реакций — через `stratagem_engine.apply` (единая точка + журнал), и фикс `heroic_intervention.cp_cost = 2` в реестре (баг Stage 5).

## Не-цели (вне 7a)

- Подключение реального агента/MCTS к `reaction_policy` — позже (Stage 8). Здесь только шов + дефолт.
- Выбор реагирующего юнита политикой — `chosen` остаётся первым кандидатом (как сейчас). Политика 7a решает только «да/нет».
- Пошаговое исполнение фаз (`PhaseEngine` substep) — 7b/7c.
- Enforcement лимитов использования — не вводим (журнал инертен).

## Глобальные ограничения

- Платформа Windows; Python 3.12+; тесты `python -m pytest`; ruff `py312`, line-length 120.
- Язык логов/сообщений — русский; «без тишины» (пропуск реакции логируется с причиной).
- `core/engine/phases/*` не импортирует `core/envs/*`.
- **Инвариант:** при `reaction_policy = None` поведение игры 1:1 (та же реакция срабатывает, тот же CP списывается, тот же эффект). `reaction_policy` — конфиг эпизода, **не** игровое состояние → НЕ снапшотится.

## Соответствие коду (что трогаем)

- `_maybe_use_smokescreen` `core/envs/warhamEnv.py:3922-3970`: `use_it` реально читается (`if not use_it: return None`, `:3955`); CP-расход `self.modelCP -= 1`/`enemyCP -= 1` (`:3959/3961`).
- `_resolve_overwatch` `:4000-4132`: `use_it = True` (`:4023`) — **мёртвая** (decline в manual через ранний `return`); CP-расход `self.modelCP -= 1`/`enemyCP -= 1` (`:4050/4057`).
- `_resolve_heroic_intervention` `:4134-4227`: `use_it = True` (`:4185`) — **мёртвая**; гейт `defender_cp < 2` (`:4178`); CP-расход `self.modelCP -= 2`/`enemyCP -= 2` (`:4209/4211`).
- Реестр: `heroic_intervention.cp_cost` сейчас `1` → должно быть `2` (`core/engine/phases/stratagems.py`).
- `stratagem_engine.apply(env, side, id, unit_idx)` — `core/engine/phases/stratagem_engine.py`.

## Архитектура

### Поле и хелпер на env

- `self.reaction_policy = None` — инициализируется в `__init__` рядом с `self.stratagem_used`. Не снапшотится.
- Хелпер на env:

```python
def _should_use_reaction(self, stratagem_id, side, chosen, candidates, phase, cp) -> bool:
    """Решение «использовать реакцию»: при отсутствии политики — текущее (всегда да)."""
    policy = getattr(self, "reaction_policy", None)
    if policy is None:
        return True
    ctx = {
        "side": side, "stratagem_id": stratagem_id, "phase": phase,
        "chosen": chosen, "candidates": list(candidates), "cp": int(cp),
    }
    try:
        return bool(policy(ctx))
    except Exception:
        return True  # сбой политики не должен ломать игру → дефолтное поведение
```

### Шов в резолверах (только non-manual; manual = человек, без изменений)

Паттерн на каждый резолвер: после CP-гейта, перед расходом CP —
```python
if not manual and not self._should_use_reaction(<id>, defender_side, chosen, <candidates>, phase, cp):
    <лог «реакция пропущена политикой»>
    return  # без CP/эффекта
```
И замена расхода CP `self.<side>CP -= N` на `_apply_stratagem(self, defender_side, <id>, chosen)`.

- **Smokescreen** (`chosen = defender_idx`, candidates `[defender_idx]`): `use_it` уже читается — заменяем его источник: `use_it = self._should_use_reaction("smokescreen", ...)` в non-manual; spend через apply.
- **Overwatch** (`chosen = candidates[0]`): убрать мёртвую `use_it = True`; добавить non-manual skip-check; spend `self.modelCP/enemyCP -= 1` → `apply(... "overwatch" ...)`.
- **Heroic** (`chosen = eligible[0]`, cp=`defender_cp`): убрать мёртвую `use_it = True`; добавить non-manual skip-check; spend `-= 2` → `apply(... "heroic_intervention" ...)` (после фикса реестра спишет 2).

### Реестр

`heroic_intervention.cp_cost`: `1 → 2`.

## Поток данных

Реакция-триггер (в фазе движения/стрельбы/чарджа) → резолвер собирает кандидатов → CP-гейт → (non-manual) `reaction_policy` решает да/нет → при «да» `apply` списывает CP и пишет журнал → эффект применяется как раньше. При `reaction_policy=None` ветка «да» всегда, поведение прежнее.

## Обработка ошибок

- Сбой/исключение в `reaction_policy` → трактуем как «использовать» (дефолт), игра не падает.
- Нехватка CP отлавливается существующим гейтом до политики (как сейчас).

## Тест-план

`tests/engine/phases/test_reaction_policy_seam.py` (вызовы резолверов напрямую, в `simulation_mode`):
1. **overwatch, policy=None** → `modelCP` уменьшился на 1, в `stratagem_used` запись `("model","overwatch",round)`. (Сетап: model[0] и enemy[0] на дистанции ≤ range; `modelCP=2`; sanity `assert _collect_overwatch_candidates(...)`.)
2. **overwatch, policy=lambda ctx: False** → `modelCP` не изменился, журнал пуст (реакция пропущена).
3. **overwatch, policy получает ctx** → захватывающая политика видит `ctx["stratagem_id"]=="overwatch"`, `ctx["side"]=="model"`, `ctx["cp"]>=1`.
4. **smokescreen, policy=None** → возвращает `"benefit of cover"`, `modelCP -= 1`; **policy=False** → возвращает `None`, CP не тронут.
5. **heroic, policy=None** → `modelCP -= 2`, журнал `("model","heroic_intervention",round)`. (Сетап: defender в 6" от charger; `modelCP=2`.)
6. **registry**: `by_id("heroic_intervention").cp_cost == 2`.
7. **policy=None ⇒ поведение реакций как раньше** (smoke: overwatch всё ещё бьёт — проверяем, что эффект/урон-путь отрабатывает без исключений).

Регрессия: весь `tests/engine/phases/`, смоук движка (`test_warham_env_snapshot_restore.py`, `test_command_phase_reanimation_sync_regression.py` — ожидаемо 1 преэкзистинг-fail, фиксируем как «не наш»), ruff на новых/изменённых строках чист, `import core.envs.warhamEnv` ок.

## Риски

- **Правки в 3 delicate-резолверах** — митигейт: шов только в non-manual, default=1:1, тесты 1–7; замена расхода CP строго на `apply` той же суммы.
- **Мёртвая `use_it`** в overwatch/heroic — удаляем (иначе ruff F841 / pyright unused); проверяем, что логика decline в manual сохранилась (ранний `return`).
- **`heroic` реестр-фикс** меняет данные Stage 5 — обновить тест Stage 5, если он фиксировал `cp_cost` (не фиксировал конкретное значение для heroic — проверить).
- **Случайный снапшот `reaction_policy`** — НЕ добавлять в snapshot (callable, конфиг эпизода).
