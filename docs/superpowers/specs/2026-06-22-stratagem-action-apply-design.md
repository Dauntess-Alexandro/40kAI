# Стратагемы как действия — Под-проект 3: применение голов — Design

**Дата:** 2026-06-22
**Статус:** согласован, готов к плану реализации
**Большой проект:** «Стратагемы как класс действий». **Под-проект 3 из 5**: 1) кодирование ✓ → 2) маски ✓ → **3) применение (этот док)** → 4) головы/priors алго → 5) переобучение + снос стопгапов.

## Проблема

Под-проекты 1–2 дали контракту головы `strat_<phase>`/`strat_<phase>_unit` и маски легальности, но **значения голов не применяются** — env их игнорирует. Цель под-проекта 3: читать головы в `env.step` (по фазам) и применять выбранную стратагему детерминированно (валидируя легальность/юнита), + завести Insane Bravery на `strat_command` (наряду со старым `use_cp`).

## Ключевой факт (инертность до п.4/5)

Пока **ни одна сеть не выдаёт strat-головы**: контракт вырос (п.1), но policy-головы алго — старого размера (новые головы и переобучение — п.4/5). Значит применение голов **инертно в живой игре сейчас**: это env-проводка, читающая+применяющая головы, КОГДА они заданы. Тестируется рукотворными `action_dict`; в проде заработает после п.4/5. Это нормально и ожидаемо.

## Решение ((A)-sequenced)

Конечная цель проекта = (A): головы — единственный путь MAIN-стратагем активной стороны. Но **снос старых путей — в п.5** (после того как обученные головы доказаны). В п.3: проводка применения голов + миграция Insane Bravery; **старые пути ОСТАВЛЯЕМ** (anti-double-guard разводит). Это избегает blackout-а стратагем и не удаляет рабочий код вслепую.

## Объём

В области: чтение+применение `strat_<phase>` в фазах movement/shooting/charge/fight; интеграция `strat_command` в `decide_bravery` (command); anti-double-guard.

ВНЕ области: удаление `use_cp`/`cp_on`, MC-хука (`_apply_phase_command_reroll`), fight-план-обработки стратагем, reaction_policy — всё это **остаётся** (снос — п.5). Головы/priors алго — п.4. Переобучение/eval/GUI — п.5.

## Архитектура

### `_apply_action_stratagem(side, phase, action)` (pre-phase стратагемы)
В начале `movement_phase`/`shooting_phase`/`charge_phase`/`fight_phase`:
- `idx = action.get(f"strat_{phase.value}", 0)`; если `idx == 0` → return (none).
- `choice = stratagem_choice_str(phase, idx)`; `base_id = choice.split(":",1)[0]`; `sub = choice.split(":",1)[1] if ":" in choice else None`.
- `unit = action.get(f"strat_{phase.value}_unit", 0)`.
- **Валидация:** `_stratagem_choice_legal(side, phase, choice)` И конкретный `unit` жив И (нет keyword_req ИЛИ `_unit_has_keyword(unit)`) И НЕ `_stratagem_already_active(side, base_id, unit, phase.value)`.
- Применение: `_apply_stratagem(self, side, base_id, unit, phase=phase.value, reroll_roll=sub)` (reroll_roll только для command_reroll; для прочих игнорируется параметром по умолчанию).
- Защита `try/except` с RU-логом (что/где/что делать), как в `_apply_pending_fight_stratagem_plan`.

Вызов — в начале фазового метода (там же, где сейчас стоят MC-хуки/`_apply_pending_fight_stratagem_plan`), ПОСЛЕ `begin_phase`. Для fight — до `resolve_fight_phase` (чтобы запись была к бою).

### Insane Bravery через `strat_command` (особый триггер)
Insane Bravery срабатывает на **провал battle-shock** (не старт фазы). `command_phase`/`run_command` уже использует `decide_bravery(i) -> bool`. Расширить: `decide_bravery(i)` истинно, если `(use_cp==1 и cp_on==i)` ИЛИ (`strat_command`-голова = индекс insane_bravery И `strat_command_unit==i`). Оба пути сосуществуют (sequenced). Anti-double: если bravery уже применена на юните — guard (существующая логика command_phase не применяет дважды).

### Anti-double-guard
`_stratagem_already_active(side, stratagem_id, unit_idx, phase)` (существует) → True, если стратагема уже в `stratagem_used` для (side, id, round, phase, unit). `_apply_action_stratagem` пропускает уже-применённые → нет двойного применения с MC-хуком/fight-планом/use_cp.

### Совместимость
- Все старые пути (`use_cp`, MC-хук, fight-план, reaction_policy) — **без изменений**.
- Головы инертны, пока сети их не выдают (до п.4/5) — применение срабатывает только на заданных вручную/обученных головах.

## Тестирование (TDD)
- `_apply_action_stratagem`: рукотворный `action` с `strat_fight`=индекс(command_reroll:hit) + `strat_fight_unit`=0 → в `active_stratagem_effects` запись command_reroll/hit на юните 0; CP списан.
- shooting/charge/movement: аналогично для своих подтипов; hungry_void (fight) через `strat_fight`=индекс(hungry_void) + necrons-юнит → применён.
- Валидация: нелегальный (CP=0 / мёртвый юнит / нет keyword) → не применён; `idx=0` → ничего.
- Anti-double: предсуществующая запись (имитация MC/fight-плана) → голова не дублирует (нет второй записи / CP не списан повторно).
- Insane Bravery: `strat_command`=insane_bravery + `strat_command_unit`=i + провал battle-shock → bravery применён; через `use_cp`=1 — тоже; одновременно — не дважды.
- Parity: все strat-головы=0 → поведение идентично текущему (existing windowed/env.step тесты зелёные).
- Регрессия: MC-хук/fight-план/use_cp пути целы; baseline `tests/engine/` 23.

## Риски / open questions
- **Двойное применение** — главный риск. Митигация: `_stratagem_already_active` guard в `_apply_action_stratagem`. Тест на каждую пару (голова vs MC-хук; голова vs fight-план; strat_command vs use_cp).
- **Порядок применения в фазе:** голова применяется в начале фазы, ДО MC-хука/fight-плана? Если голова первой ставит запись — MC-хук/fight-план видят `_command_reroll_record_exists`/`_stratagem_already_active` и не дублируют. Нужно поставить вызов `_apply_action_stratagem` ПЕРЕД существующими хуками в каждом фазовом методе. Зафиксировать порядок в плане.
- **Insane Bravery trigger:** strat_command применяется только при провале battle-shock (не безусловно) — иначе тратим CP зря. Интеграция через `decide_bravery`, не через `_apply_action_stratagem` (у bravery иной триггер).
- **Инертность:** до п.4/5 головы=0 → no-op; не пугаться «эффекта нет вживую» (ожидаемо).
- **Open:** где именно живёт `decide_bravery` (command_phase сигнатура / run_command) — свериться в начале плана, чтобы расширить корректно.

## Критерии готовности
- `strat_<phase>` головы применяются по фазам (movement/shooting/charge/fight) с валидацией и anti-double; Insane Bravery доступен и через `strat_command`.
- Старые пути целы (sequenced); двойного применения нет (тесты на пары); parity при нулевых головах; регрессий нет (baseline 23).
- Применение инертно в проде до п.4/5 — проверяется рукотворными action_dict.
