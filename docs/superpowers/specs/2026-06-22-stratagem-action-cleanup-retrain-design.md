# Стратагемы как действия — Под-проект 5: снос стопгапов + переобучение — Design

**Дата:** 2026-06-22
**Статус:** согласован, готов к плану реализации
**Большой проект:** «Стратагемы как класс действий». **Под-проект 5 из 5 (финал)**: 1) кодирование ✓ → 2) маски ✓ → 3) применение ✓ → 4) AZ MCTS-поиск ✓ → **5) снос стопгапов + переобучение (этот док)**.
**Решения:** (U) безусловный снос (не gated); снос **точечный** (реакции оппонента и движковый мех реролла ОСТАЮТСЯ); декомпозиция: **5a = код (TDD)**, **5b = runbook переобучения (процесс, на GPU пользователя)**.

## Проблема

После п.1–4 головы `strat_<phase>` готовы (контракт+маски+применение+AZ-поиск), но MAIN-стратагемы активной стороны всё ещё применяются 3 старыми «стопгап»-путями (use_cp/cp_on bravery, MC command_reroll, fight-план), а головы инертны до переобучения. Цель п.5: сделать головы ЕДИНСТВЕННЫМ путём ((A)-финал) — снести стопгапы, переставить старшинство bravery на head, переобучить агентов, проверить критериями.

## Объём

### 5a — код (TDD, в этой спеке + план)
**Сносим (стопгапы MAIN-стратагем активной стороны):**
- `use_cp`/`cp_on` из контракта (`BASE_ACTION_HEADS`, `ordered_action_keys`, `default_action_dict`, `env.action_space`, `convertToDict`-инференс) + их маски + старая bravery-ветка use_cp.
- **bravery-старшинство** в `command_phase`: убрать reaction_policy- и use_cp-ветки для bravery; `strat_command`-голова становится primary (`_use_bravery` ⟺ `strat_command`-голова = insane_bravery и `strat_command_unit==i`). **(carry-forward из п.3, см. memory `stratagem-bravery-precedence-carryforward`.)**
- **MC command_reroll-машинерия:** `_value_pick_command_reroll`, `_apply_phase_command_reroll`, `_mc_value_command_reroll_{fight,shooting,charge}`, `_simulate_{fight,shoot,charge}_attack`, `_best_shoot_target`, `_best_charge_target`, `_expected_shoot_damage`, `_cmdreroll_mc_samples/eps`, `_command_reroll_record_exists` (если больше не нужен после сноса), command_reroll-prefilter в `dqn_build_fight_plan`/`ppo_build_fight_plan`; вызовы `_apply_phase_command_reroll` в фазах.
- **fight-план стратагем:** ветки command_reroll/hungry_void в `_apply_pending_fight_stratagem_plan`; `_fight_stratagem_plan_from_choices`; `attach_fight_stratagem_plan` + `_pending_fight_stratagem_plan`; AZ `last_selected_fight_plan` + вызовы attach в alphazero_mcts/selfplay/train/eval; `dqn_build_fight_plan`/`ppo_build_fight_plan` целиком.
- Удалить/обновить тесты на снесённые пути (MC-фичи, fight-план bridges).

**ОСТАВЛЯЕМ (вне области, не трогать):**
- `reaction_policy` + `_should_use_reaction` + `_simulate_reaction_branch` + `_reaction_net_value` + реакции оппонента (overwatch/go_to_ground/smokescreen/heroic) — целиком (они НЕ «стратагемы как действия»).
- Движковый мех реролла: `attack()` reroll_decider/effect, `_build_reroll_decider`, `_apply_action_stratagem`, `_apply_stratagem`, маски (п.2), legacy_patch опций (п.4), `_stratagem_already_active`, `_consume_command_reroll_record`/advance/charge reroll helpers.

### 5b — runbook переобучения (процесс, раздел спеки/плана, НЕ TDD)
Контракт изменился (п.1, +ещё после сноса use_cp/cp_on) → все чекпойнты несовместимы → переобучить. Runbook: команды train для DQN/PPO/AZ/GAZ (+GMZ/SMZ — переобучить ради совместимости контракта, стратагемами не пользуются); критерии; что мерить в eval.

## Архитектура (5a)

### Bravery-flip (command_phase)
Заменить трёхветочный `_use_bravery` (reaction_policy → decide_bravery → use_cp+strat_command) на:
- `decide_bravery` (windowed) — сохранить как явный override-хук (тесты/совместимость), если он задан.
- иначе: `_use_bravery ⟺ action["strat_command"]` = индекс(insane_bravery) И `action["strat_command_unit"]==i`.
- Убрать reaction_policy-ветку и use_cp/cp_on-ветку для bravery.

### Снос MC/fight-план
Удалить методы/вызовы списком выше. После сноса:
- shooting/charge/movement/fight фазы применяют стратагемы ТОЛЬКО через `_apply_action_stratagem` (head).
- AZ применяет стратагемы через головы (legacy_patch→joint_tuple→action_dict→`_apply_action_stratagem`), fight-план не нужен.
- Bridges (`dqn/ppo_stratagem_bridge`) — `install_*_stratagem_policy` для РЕАКЦИЙ остаётся (reaction_policy для overwatch/go_to_ground), но `*_build_fight_plan` удаляется.

### Контракт без use_cp/cp_on
`BASE_ACTION_HEADS = ["move", "attack"]` (убрать use_cp/cp_on); обновить `ordered_action_keys`, `default_action_dict`, `env.action_space`, `convertToDict`-инференс (−2 головы); удалить use_cp/cp_on маски. Это снова меняет контракт → ещё одна несовместимость чекпойнтов (ок, всё равно переобучаем).

## Тестирование 5a (TDD)
- bravery через `strat_command` срабатывает БЕЗ reaction_policy и БЕЗ use_cp (теперь primary); провал battle-shock триггерит; use_cp больше не триггерит (head-only).
- shooting/charge/fight: стратагема применяется ТОЛЬКО через head (`_apply_action_stratagem`); MC-хук/fight-план отсутствуют (методы удалены — `AttributeError` при попытке вызвать в старых тестах → тесты удалить/переписать).
- Контракт: `ordered_action_keys` БЕЗ use_cp/cp_on; round-trip; `env.action_space` без них; `convertToDict` инференс корректен (−2).
- AZ self-play смоук (контроллер): применяет стратагему через head без fight-плана; exit=0.
- Регрессия: реакции (overwatch/go_to_ground) НЕ сломаны (их тесты зелёные); baseline `tests/engine/` (пересчитать — контракт сменился, AZ n_actions-тесты обновить).
- Удалённые тесты: MC-фичи (`test_command_reroll_mc_*`, `test_command_reroll_value_policy`), fight-план bridges (`test_dqn/ppo_stratagem_bridge` fight-plan части), windowed fight-план — удалить или переписать под head-путь.

## 5b — Runbook переобучения + критерии (процесс)
**Команды (на GPU пользователя, локально):** для каждого algo — `TRAIN_ALGO=<algo> python train.py` с боевыми episodes (не смоук). Algo: `dqn`, `ppo`, `alphazero_tree`, `gumbel_az` (+ `gumbel_muzero`, `sampled_muzero` — ради загрузки контракта). Точные флаги/длительность — по обычному train-конфигу проекта.
**Критерии «агент реально юзает стратагемы через головы»:** в eval обученной модели (`eval.py --learner-agent-id ...`, `EVAL_TRACE_STYLE=warhammer`):
- `applied=command_reroll`/`hungry_void`/`insane_bravery` count > 0 (через head-путь — стопгапы снесены, значит это головы);
- применение не вырождено (не на каждый ход подряд — разумная частота), CP не выжигается в ноль бессмысленно;
- winrate не просел против baseline (стратагемы не вредят).
**Если критерии НЕ выполнены:** снос в git (5a) → можно откатить (revert) и вернуться к (G)/стопгапам; диагностировать (AZ кап кандидатов / слабый сигнал / мало эпизодов).

## Риски / open questions
- **(U) необратимость до отката:** головы необучены на момент сноса → между 5a и завершением 5b-переобучения агенты НЕ используют стратагемы (blackout). Принято пользователем. Откат — git revert 5a.
- **Не сломать реакции:** снос строго НЕ трогает reaction_policy/`_should_use_reaction`/реакции. **Главный риск 5a** — обязательна регрессия реакц-тестов + `engine-regression-reviewer`.
- **Объём удаления велик** (~12 методов + bridges + тесты) → риск задеть лишнее. Митигация: TDD по шагам, реакц/реролл-тесты как страховка.
- **Контракт снова меняется** (−use_cp/cp_on) → чекпойнты опять несовместимы (ок, переобучаем).
- **Open:** часть `_command_reroll_record_exists`/`_stratagem_already_active` могут остаться нужны `_apply_action_stratagem` (anti-double внутри head-пути на повтор) — в плане свериться, что не удалить нужное.

## Критерии готовности
- 5a: стопгапы снесены; bravery через `strat_command` primary; головы — единственный путь MAIN-стратагем; реакции и реролл-мех целы; тесты зелёные (обновлённый baseline); AZ смоук exit=0 без fight-плана.
- 5b: runbook + критерии задокументированы; переобучение и проверка критериев — на пользователе (GPU). Проект «стратагемы как действия» завершён после прохождения критериев.
