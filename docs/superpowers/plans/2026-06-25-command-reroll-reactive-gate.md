# Реактивный гейт command_reroll — Implementation Plan

> **Для дирижёра GPT 5.5:** это **каркас**. РАЗБЕРИ каждую задачу в bite-sized TDD под-задачи
> (тест→красный→код→зелёный→коммит) ПЕРЕД делегированием GLM 5.2. Точные сигнатуры/анкоры —
> дочитывай по коду (spec даёт строки). Сомнения по дизайну — наверх (заказчику/архитектору).
> REQUIRED: TDD для движка; полный прогон `tests/engine/phases` после каждой движковой задачи.

**Goal:** command_reroll решается реактивно (в момент броска) + CP списывается только при реальном рероле → waste≈0 для всех алго. Без изменения action-контракта (переобучение не нужно).

**Spec:** `docs/superpowers/specs/2026-06-25-command-reroll-reactive-gate-design.md` — источник истины по дизайну/инвариантам/рискам.

## Global Constraints
- Платформа Windows; RU-логи/сообщения. TDD (движок!). ruff чист. Коммиты — только релевантный код.
- НЕ менять action-контракт (`ordered_action_keys`, размер obs), reward, прочие стратагемы.
- Combat-резолв (`warhamEnv` consume-точки) — зона повышенного риска: строгий TDD + регресс `tests/engine/phases` (сверка с baseline, не добавить падений).
- Финал — обязательно к архитектору Opus на engine-ревью.

---

### Task 1: Выделить единую точку CP-расхода (рефактор, без смены поведения)
**Цель:** иметь функцию «списать CP стороне за стратагему» отдельно от `apply`, чтобы вызывать её на consume.
**Files:** `core/engine/phases/stratagem_engine.py`; test `tests/engine/phases/test_stratagem_cp_charge.py`
**Acceptance:** функция `charge_cp(env, side, cost) -> bool` (или аналог) списывает CP/не уходит в минус; `apply()` для НЕ-reroll использует её — поведение и существующие тесты неизменны (baseline зелёный).
**GPT: разбей на TDD-шаги (тест на charge_cp → реализация → подмена в apply → регресс).**

### Task 2: arm без оплаты для command_reroll
**Цель:** при выборе command_reroll CP НЕ списывается на arm; эффект помечается `paid=False`.
**Files:** `stratagem_engine.py` (ветка `effect_id=="command_reroll"`, `:68-85`); тесты.
**Acceptance:** после arm command_reroll `modelCP` не изменился; эффект в `active_stratagem_effects` имеет `consumed=False` + флаг неоплаченности. Существующие тесты, ожидавшие списание на arm, — обновить (это цель), сверяя baseline.
**GPT: детализируй (тест «arm не списывает CP» → правка apply → обновить затронутые тесты).**

### Task 3: реактивное решение + pay-on-apply в consume-точках
**Цель:** в `warhamEnv.py:2407-2415` и `:2427-2450` при совпадающем броске прогнать armed-эффект
через `reaction_policy` (apply/pass, как overwatch); на apply — `charge_cp` + реролл + `consumed=True` +
`_cmd_reroll_fired+=1`; на pass / нет CP — не списывать, не реролить. Legacy (reaction_policy=None) →
реролл по приходу броска, но CP на consume.
**Files:** `core/envs/warhamEnv.py` (consume-точки; ctx для reaction как у overwatch — см. `_simulate_reaction_branch`, `_pending_reaction_trigger`); тесты в `tests/engine/phases/`.
**Acceptance (тесты):** apply→CP списан 1 раз+реролл+fired; pass→CP не списан, реролла нет; нет броска до конца фазы→CP не списан; нет CP на apply→не реролит (не в минус); один armed=один реролл; legacy→реролл+CP на consume.
**GPT: это самая крупная задача — разбей на несколько под-задач (shooting hit/wound отдельно от прочих фаз; ctx-сборка; pay-on-apply; legacy-путь), каждая с TDD + прогоном tests/engine/phases.**

### Task 4: телеметрия и end-of-phase очистка
**Цель:** неоплаченные armed-эффекты отбрасываются в конце фазы/хода без потери CP; метрики
`cmd_reroll_wasted` отражают «armed-not-fired (CP не потрачен)», `fired` = реальные рероллы.
**Files:** `warhamEnv` (очистка эффектов в конце фазы/хода), `core/telemetry/stratagem_trace.py` (смысл метрик/коммент); тесты.
**Acceptance:** после фазы неоплаченные armed убраны; `cmd_reroll_wasted` не считает потерю CP; smoke-лог показывает applied≈fired.

### Task 5: регресс + smoke
**Acceptance:** `tests/engine/phases` и `tests/engine` без новых падений vs baseline; ruff чист;
короткий GMZ/AZ прогон с debug-логами → `cmd_reroll_wasted`≈0. Артефакты/логи не коммитить.

## DoD (сводно)
Все тесты задач 1-4 зелёные; engine-регресс не хуже baseline; ruff чист; smoke подтверждает waste≈0; финальное engine-ревью Opus пройдено.
