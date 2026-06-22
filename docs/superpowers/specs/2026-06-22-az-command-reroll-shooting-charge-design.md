# Command Re-roll в дереве AZ/GAZ для Shooting+Charge — Design

**Дата:** 2026-06-22
**Статус:** согласован, готов к плану реализации
**Связанные:** `docs/superpowers/plans/2026-06-22-command-reroll-fidelity.md` (механика), `docs/superpowers/specs/2026-06-22-command-reroll-mc-shooting-charge-design.md` (DQN/PPO MC shooting/charge — отдельный путь).

## Проблема

AZ (и GAZ, едущий на AZ-инфре) выбирает стратагемы **своим деревом MCTS**, а не нашей DQN/PPO-MC-приставкой. Но дерево видит стратагемы **только в fight-окнах**: пространство опций (`generate_windows` → `fight_stratagem_options_for_unit`), план кандидата (`fight_stratagem_plan`), применение в rollout (`attach_fight_stratagem_plan` на depth 0) и в реале (`_apply_pending_fight_stratagem_plan`) — всё **fight-only**. Значит AZ/GAZ не могут выбрать Command Re-roll в shooting/charge.

Цель: дать дереву AZ/GAZ видеть, оценивать (через свой rollout) и применять Command Re-roll в **shooting** и **charge** — принципиально (дерево решает), а не через MC-приставку.

## Решение (согласованные развилки)

1. **Дерево решает** (не MC). AZ не использует reaction_policy для command_reroll; выбор делает MCTS, применение — **детерминированно по выбору дерева** в colon-форме `command_reroll:<roll>` (как fight-fix `74de9df2`), минуя MC-гейт.
2. **Многофазный план стратагем.** Обобщить fight-only план до фазо-ключевого; провести через все 4 слоя (опции → план кандидата → rollout → применение).
3. **Чистое разделение с DQN/PPO:** DQN/PPO shooting/charge идут через MC-хук (`reaction_policy` установлен); AZ — через tree-план (`reaction_policy` НЕ установлен). Пути не пересекаются.
4. **GAZ — бесплатно** (общая AZ-инфра option_candidates/mcts).
5. **Бэк-компат:** fight-срез плана и `_pending_fight_stratagem_plan` сохраняются — DQN/PPO и текущий AZ-fight не ломаются.

## Архитектура — 4 слоя

### Слой 1: опции дерева
`generate_windows` ([core/engine/phases/option_generator.py](../../../core/engine/phases/option_generator.py)): в shooting- и charge-окна добавить `command_reroll_options_for_unit(env, side, u, phase=Phase.SHOOTING/CHARGE, rolls=("hit","wound")/("charge",))` (хелпер уже есть из Варианта A). Так дерево получает command_reroll как опцию в этих фазах. Fight-окна — без изменений.

### Слой 2: план кандидата
`core/models/option_candidates.py`:
- `TurnPlanCandidate.fight_stratagem_plan: tuple[(int,str)]` → обобщить до **фазо-ключевого** `stratagem_plan: tuple[(str, int, str)]` (phase, unit, sid). Сохранить свойство/шим `fight_stratagem_plan` для бэк-компата (fight-срез).
- `_fight_stratagem_plan_from_choices` → `_stratagem_plan_from_choices`: собирать USE_STRATAGEM-выборы из fight/shooting/charge-окон; для command_reroll кодировать `command_reroll:<reroll_roll>` (подтип из `opt.meta`/`opt.param`), как сделано в fight-fix.
- `RootJointCandidates.fight_plans` → `stratagem_plans` (по joint_tuple → многофазный план); метод-аксессор сохранить совместимым.

### Слой 3: применение в rollout
`core/models/alphazero_mcts.py` (depth-0 attach, ~строки 391, 800): прикреплять **весь многофазный план** (не только fight), чтобы rollout-симуляция применяла shooting/charge реролл и дерево видело его эффект в value.

### Слой 4: применение в env
`core/envs/warhamEnv.py`:
- Новый `_pending_stratagem_plan` (фазо-ключевой: `{phase: {unit_idx: sid}}`) + snapshot/restore (как `_pending_fight_stratagem_plan`).
- `attach_*` (в option_candidates) задаёт его; fight-срез по-прежнему пишется в `_pending_fight_stratagem_plan` для бэк-компата.
- `shooting_phase`/`charge_phase` в начале применяют свой срез **детерминированно**: для `command_reroll:<roll>` — прямой `_apply_stratagem(..., reroll_roll=roll)` (минуя MC-гейт). Метод `_apply_pending_phase_stratagem_plan(side, phase)` по образцу `_apply_pending_fight_stratagem_plan`, но прямое применение без `_should_use_stratagem`/MC (дерево уже решило).

### Поток (shooting, AZ)
```
MCTS: shooting-окно содержит command_reroll:hit/wound → дерево выбирает →
  _stratagem_plan_from_choices → stratagem_plan[(shooting, u, "command_reroll:hit")]
  → rollout depth0 attach → tree оценивает эффект → выбран joint →
  attach многофазного плана для реального env.step →
  shooting_phase начало: _apply_pending_phase_stratagem_plan("model","shooting") →
  _apply_stratagem(... reroll_roll="hit") → выстрел читает reroll-эффект (decider) → урон
```

## Конфиг
Новых флагов нет. Применяется всегда, когда дерево выбрало (AZ/GAZ self-play/eval). Без AZ — `_pending_stratagem_plan` пуст → no-op (parity для DQN/PPO/эвристики).

## Тестирование (TDD)
- **option_generator:** AZ-окна shooting/charge содержат command_reroll-опции (`meta.stratagem_id=="command_reroll"`, `param.reroll_roll`).
- **`_stratagem_plan_from_choices`:** собирает многофазный план; command_reroll → colon-форма с подтипом; fight-стратагемы прочие — как раньше; бэк-компат `fight_stratagem_plan`-среза.
- **env:** `_apply_pending_phase_stratagem_plan` применяет shooting/charge command_reroll напрямую (без reaction_policy); parity без плана (no-op); fight-путь не затронут.
- **rollout:** многофазный план прикрепляется на depth 0 (юнит-тест на attach).
- **e2e:** AZ self-play смоук — command_reroll появляется в shooting/charge (`[STRATAGEM] applied=command_reroll ... phase=shooting|charge`), которого не было.
- **Регрессия:** `tests/engine/` baseline 23 failed; AZ/GAZ self-play смоук оба first-turn режима exit=0; DQN/PPO fight/shooting/charge не затронуты.

## Риски / open questions
- **Rollout-перф:** дерево теперь симулирует shooting/charge реролл — больше работы на узел MCTS. Замерить на self-play смоуке; при деградации — ограничить (напр. только если есть провалы/CP).
- **Регрессии self-play:** правка внутренностей AZ MCTS (план/кандидаты/rollout) — обязателен `engine-regression-reviewer` + смоук AZ и GAZ (оба first-turn режима, локально `AZ_INFERENCE_SERVER=0 AZ_DISTRIBUTED_ACTORS=0`).
- **Бэк-компат плана:** обобщение `fight_stratagem_plan` → `stratagem_plan` должно сохранить fight-поведение DQN/PPO bridges и текущего AZ-fight (шим/свойство). Проверяется регресс-тестами `test_option_candidates`, `test_windowed_fight_stratagem`, bridge-тестами.
- **Open:** charge-реролл низкого EV (одна 2D6-попытка) — дерево может почти не выбирать; это ок (как у DQN/PPO). Цель — чтобы МОГ, не чтобы всегда.

## Вне области
- Advance/movement command_reroll для AZ (move-then-derive; вне области как и в DQN/PPO).
- Прочие стратагемы AZ в не-fight фазах (только command_reroll сейчас).
- DQN/PPO путь (не трогаем — у них свой MC).
- Включение reaction_policy/MC для AZ.

## Критерии готовности
- 4 слоя проведены; AZ/GAZ дерево может выбрать command_reroll в shooting/charge; применяется детерминированно по выбору дерева.
- Тесты (option/plan/env/rollout) зелёные; регрессий нет (baseline 23); fight/DQN/PPO не затронуты.
- AZ self-play смоук: command_reroll в shooting/charge логах появляется. Если ноль — диагностировать (rollout не применяет / опции не в окне), не подгонять тесты.
