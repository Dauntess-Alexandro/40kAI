# Reward-штраф за впустую-command_reroll — Design

**Дата:** 2026-06-23
**Статус:** согласован, готов к плану реализации
**Контекст:** продолжение проекта «стратагемы как действия». После п.5a (головы — единственный путь) + телеметрии (`cmd_reroll_fired`/honest `wasted = applied − fired`) замер на 3к PPO показал: command_reroll применяется ~20/эпизод, но **fired только ~29%** и **падает** по ходу обучения (38%→25%) — голова спамит реролл рефлекторно, ~70% CP впустую. Reward не штрафует впустую-CP → политике «всё равно».

## Проблема

Голова `strat_<phase>` взводит `command_reroll` спекулятивно (в начале фазы, до бросков). Если соответствующего броска нет или он успешен — реролл не срабатывает (`consumed=False`), CP потрачен впустую. Reward сейчас не различает сработавший реролл и впустую-взвод → нет сигнала «взводи избирательно».

## Решение

**Reward-штраф за впустую-command_reroll, per-step net, сторона ученика (model):**
- В конце каждого шага модели: `reward -= COMMAND_REROLL_WASTED_PENALTY × max(0, applied_step − fired_step)`, где `applied_step`/`fired_step` — число command_reroll, *взведённых* и *сработавших* стороной model за этот шаг.
- `p = COMMAND_REROLL_WASTED_PENALTY = 0.05` (тюнится, override-механизм reward_config).
- **Сработавшие command_reroll штраф НЕ несут** (платится только за `applied − fired`) → избирательную «умную» игру не давит; модель может свести штраф к 0, взводя реролл только когда он реально срабатывает.

### Почему per-step net (вариант C)
Взвод и срабатывание command_reroll происходят **внутри одного шага** (в той же фазе: реролл-decider отрабатывает на бросках этой же фазы). Поэтому `applied_step − fired_step` точно равно числу впустую-взводов этого шага — не зависит от недосчётного `_clear_phase_stratagem_effects`-детекта (который ловит лишь часть). Кредит assignment корректный (штраф на том шаге, где голова приняла решение).

Отвергнутые варианты: (A) per-event на clear — недосчитывает ~половину; (B) terminal per-episode — точно по сумме, но размазанный кредит (PPO хуже учится, какой ход виноват).

### Почему reward-шейпинг, а не смена механики
Альтернатива — списывать CP только при срабатывании (consume), а не при взводе (apply): тогда waste невозможен, и это даже точнее по правилам Wahapedia. Но тогда «взвод» бесплатен → у головы исчезает решение «стоит ли», и учить нечему. Reward-штраф **сохраняет осмысленное решение** «взводить только когда реально нужно» — это и есть цель проекта (агент учится умному использованию стратагем).

## Архитектура

### Конфиг
`reward_config.py`: добавить `COMMAND_REROLL_WASTED_PENALTY = 0.05` рядом с `COMMAND_INSANE_BRAVERY_REWARD/PENALTY`. Подхватывается существующим override-механизмом (`test_reward_config_overrides`).

### Детекция и применение (`core/envs/warhamEnv.py`)
Существует глобальный счётчик `self._cmd_reroll_fired` (per-episode, инкремент при `consumed=True`, гейт `not _in_simulation_mode()`). Журнал `self.stratagem_used` хранит кортежи `(side, id, round, phase, unit)`.

Per-step net для стороны model:
1. **На входе шага модели** (точка, где начинается обработка хода model в `step()` — там же, где инициализируется `reward_delta` для model-ветки): снять снапшот
   - `_cr_fired_at_step_start = int(self._cmd_reroll_fired)`
   - `_cr_applied_at_step_start = ` число записей в `stratagem_used` c `side=="model"` и `id=="command_reroll"`.
2. **В конце шага модели** (после всех фаз model, до формирования итогового reward шага):
   - `applied_step = (текущее число model/command_reroll в stratagem_used) − _cr_applied_at_step_start`
   - `fired_step = self._cmd_reroll_fired − _cr_fired_at_step_start`
   - `wasted_step = max(0, applied_step − fired_step)`
   - `reward_delta -= reward_cfg.COMMAND_REROLL_WASTED_PENALTY * wasted_step`
   - reward-лог (как `_log_reward_unit` для insane_bravery): строка вида `Reward (стратагема): command_reroll впустую×{wasted_step} penalty=-{...:.3f}` (только при `wasted_step > 0` и `not _in_simulation_mode()`).

**Атрибуция стороне model корректна:** в ход модели command_reroll взводит/срабатывает только модель; реакции оппонента (overwatch/go_to_ground) — это не command_reroll, журнал/счётчик их не путает (фильтр `side=="model"` + командный реролл считается в фазах модели). Снапшот-дельта в пределах model-шага исключает попадание enemy-применений.

### Гейт симуляции
Штраф — часть reward реальной игры; в `_in_simulation_mode()` (MCTS-симы AZ) фактический reward тоже считается симом, но env-счётчик `_cmd_reroll_fired` под симом не инкрементится → дельта может исказиться. Применять штраф так же, как прочий reward_delta (он и так не пишется/не учитывается отдельно под симом по месту вызова). Для DQN/PPO (без симов) — прямой путь. Если point применения в model-ветке исполняется и под AZ-симом — гейтить расчёт штрафа `not self._in_simulation_mode()` для согласованности со счётчиком (иначе fired занижен → ложный waste). **Решение: считать и применять штраф только при `not self._in_simulation_mode()`.**

## Тестирование (TDD)
- `test_wasted_command_reroll_penalty_applied`: смоделировать шаг model, где взведено N command_reroll и сработало M (M<N) → итоговый reward содержит `−0.05*(N−M)` (сверить дельту reward). Не вакуумный.
- `test_no_penalty_when_all_fired`: N взведено, N сработало → штраф 0.
- `test_no_penalty_clamped_negative`: fired ≥ applied → `max(0,·)` = 0, штраф 0.
- `test_enemy_command_reroll_not_penalized_to_model`: command_reroll стороны enemy → model reward не изменяется.
- `test_penalty_respects_config_override`: переопределение `COMMAND_REROLL_WASTED_PENALTY` через override-механизм меняет величину.
- `test_penalty_skipped_in_simulation_mode`: под `simulation_mode()` штраф не начисляется.

## Валидация (после переобучения, на пользователе)
Переобучить PPO (и опц. DQN/AZ) с штрафом → в honest-телеметрии (`cmd_reroll_fired` / `wasted = applied − fired`):
- **fired% растёт** (цель — заметно выше нынешних 25-29%), wasted падает;
- **winrate НЕ просел** (DET_EVAL) — штраф не сломал игру;
- command_reroll **не исчез совсем** (если applied→0 — p слишком велик, снизить).
Если критерии не выполнены — `COMMAND_REROLL_WASTED_PENALTY` тюнится (вниз при коллапсе использования, вверх при слабом эффекте).

## Риски
- **Коллапс использования** (модель совсем бросает command_reroll): митигация — умеренный p=0.05, сработавшие не штрафуются, p тюнится, валидация по телеметрии+winrate.
- **Атрибуция стороны:** строго фильтровать model в журнале + дельта в пределах model-шага; покрыто тестом `enemy_not_penalized`.
- **Сим-искажение:** гейт `not _in_simulation_mode()` на расчёт штрафа (согласован со счётчиком fired).
- **Точка применения в step():** надо точно найти, где формируется per-step reward модели (где живёт `reward_delta` model-ветки) — план обязан это локализовать перед правкой.

## Критерии готовности
- `COMMAND_REROLL_WASTED_PENALTY` в reward_config; per-step net штраф в model-ветке step; reward-лог; гейт sim; все TDD-тесты зелёные; baseline `tests/engine/` не вырос. Переобучение/валидация winrate+fired% — на пользователе.
