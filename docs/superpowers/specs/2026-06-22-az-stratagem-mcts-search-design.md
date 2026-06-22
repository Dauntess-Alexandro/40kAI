# Стратагемы как действия — Под-проект 4: AZ MCTS ищет strat-головы — Design

**Дата:** 2026-06-22
**Статус:** согласован, готов к плану реализации
**Большой проект:** «Стратагемы как класс действий». **Под-проект 4 из 5**: 1) кодирование ✓ → 2) маски ✓ → 3) применение ✓ → **4) AZ MCTS-поиск strat-голов (этот док)** → 5) переобучение + снос стопгапов.
**Важно:** DQN/PPO головы — БЕСПЛАТНЫ (policy-головы строятся динамически из `action_sizes`: `q_heads`/`policy_heads = ModuleList(... for size in action_sizes)`), факторизованный loss их покрывает → DQN/PPO «стратагемы как действия» готовы, ждут только переобучения (п.5). Этот под-проект — **только про AZ/GAZ**.

## Проблема

У AZ policy-таргет per-head строится из visit-ов по `action_tuple` (= joint_tuple) в `_final_policy_from_visits` ([core/models/alphazero_mcts.py:558-582](../../../core/models/alphazero_mcts.py#L558-L582)). Но strat-головы в joint_tuple **всегда 0**: опции стратагем имеют пустой `legacy_patch` → не попадают в `compile_options_to_action_dict` → joint_tuple. Значит таргет strat-голов вырожден («всегда none») → AZ обучается **никогда** не использовать стратагемы. Цель: завести strat-выбор в joint_tuple и дать AZ-кандидатам окна стратагем во всех трёх фазах, чтобы MCTS реально искал strat-измерения и давал ненулевой policy-таргет.

## Объём (только AZ/GAZ candidate-search)

В области: `legacy_patch` на опциях стратагем (→ strat-головы в joint_tuple); окна стратагем для shooting/charge в `generate_windows`. GAZ — бесплатно (общая AZ-инфра).

ВНЕ области: DQN/PPO (головы бесплатны, им п.4 не нужен — сразу п.5); GMZ/SMZ (стратагемами не занимаются); снос старых путей (`use_cp`/MC-хук/fight-план) — п.5; переобучение — п.5; перестановка bravery-старшинства — п.5 (carry-forward из п.3).

## Архитектура

### Слой 1: опции стратагем → strat-головы (legacy_patch)
`core/engine/phases/stratagems.py` (`legal_stratagem_options`, command_reroll-ветка + общая) и `core/engine/phases/option_generator.py` (`command_reroll_options_for_unit`): каждой опции стратагемы задать
```
legacy_patch = {f"strat_{phase.value}": stratagem_choice_index(phase, choice), f"strat_{phase.value}_unit": unit_idx}
```
(вместо пустого). Где `choice` = id или `command_reroll:<sub>` (как в `stratagem_action_choices`). Тогда выбор опции через `compile_options_to_action_dict` → action_dict → `joint_tuple_from_action_dict` несёт strat-выбор → кандидаты различаются.

### Слой 2: окна стратагем в shooting/charge (generate_windows)
`core/engine/phases/option_generator.py::generate_windows`: для shooting и charge добавить per-unit стратагем-окна (по образцу fight): PASS + `command_reroll_options_for_unit(env, side, u, phase=Phase.SHOOTING/CHARGE, rolls=("hit","wound")/("charge",))`. Отдельные окна (не мешать с action-окнами стрельбы/чарджа), как fight-окна.

### Слой 3 (готово): применение + policy-таргет
- Применение: rollout `clone_env.step(action_dict)` (alphazero_mcts) → `_apply_action_stratagem` (п.3) применяет strat-головы. Реальный шаг — так же.
- Policy-таргет: автоматически — strat-головы теперь в `action_tuple` → `_final_policy_from_visits` даёт ненулевой таргет.
- Старые пути (fight-план/MC-хук) сосуществуют (anti-double п.3, sequenced).

### Поток (AZ, fight)
```
generate_windows: fight-окно с опциями hungry_void/command_reroll:hit/wound (legacy_patch→strat_fight) →
build_turn_plan_candidates: кандидаты с разным strat_fight различаются joint_tuple (НЕ схлопываются) →
MCTS: visit-ы по strat_fight распределяются → _final_policy_from_visits → ненулевой policy-таргет strat_fight →
rollout clone_env.step(action_dict[strat_fight=...]) → _apply_action_stratagem применяет →
сеть учит policy_heads[strat_fight] к MCTS-таргету.
```

## Конфиг
Новых флагов нет. Касается AZ/GAZ self-play/eval (где работает MCTS-кандидат-генерация).

## Тестирование (TDD)
- **legacy_patch:** опция стратагемы (fight/shooting/charge) несёт `strat_<phase>`/`_unit` в `legacy_patch`; `compile_options_to_action_dict([opt], n)` ставит их; `joint_tuple_from_action_dict` отражает выбор.
- **Не схлопываются:** через `build_turn_plan_candidates` (или прямой `_fight_stratagem_plan_from_choices`/joint) два варианта (реролл/нет) дают РАЗНЫЕ joint_tuple.
- **generate_windows:** shooting/charge содержат стратагем-окна (`USE_STRATAGEM`-опции с `command_reroll`).
- **policy-таргет:** сконструировать root с детьми, у которых `action_tuple[strat_head_i]` != 0 у части → `_final_policy_from_visits` даёт массу вне index 0 (не вырожден).
- **AZ self-play смоук:** прогон play_episode_with_mcts (локально `AZ_INFERENCE_SERVER=0 AZ_DISTRIBUTED_ACTORS=0`) → в логах применяется стратагема через head-путь, без падений; GAZ тоже.
- **Регрессия:** baseline `tests/engine/` 23; DQN/PPO/windowed/контракт-тесты целы; существующие AZ-тесты (n_actions) обновить, если размер кандидатов/окон сменился.

## Риски / open questions
- **Взрыв кандидатов:** strat-выборы теперь различают joint_tuple → `build_turn_plan_candidates` (greedy + single-window perturb, кап `max_candidates=64`) тратит слоты и на strat-пертурбации. Возможно под-исследование strat. Митигация/тюнинг: при необходимости поднять кап или дать strat-окнам приоритет в переборе. Зафиксировать как open (замер на смоуке).
- **Регрессии self-play:** AZ-внутренности (окна/кандидаты/joint_tuple) — обязателен `engine-regression-reviewer` + AZ и GAZ смоук (оба first-turn режима).
- **Перф rollout/поиск:** больше окон/кандидатов на узел.
- **Двойные пути:** strat-голова + старый fight-план (`_fight_stratagem_plan_from_choices` всё ещё строит план из тех же окон) → применятся оба? Anti-double (п.3 `_stratagem_already_active`/`_command_reroll_record_exists` + usage_limit) разводит. **Проверить тестом**, что при head-применении старый fight-план не дублирует.
- **Open:** `_fight_stratagem_plan_from_choices` теперь дублирует роль (та же стратагема и в joint_tuple, и в fight-плане). Снос дубля — п.5; в п.4 оставляем (sequenced, guard).

## Критерии готовности
- Опции стратагем несут strat-головы в joint_tuple; shooting/charge имеют стратагем-окна в `generate_windows`; кандидаты различаются по strat-выбору (не схлопываются).
- `_final_policy_from_visits` даёт ненулевой strat-таргет; AZ/GAZ self-play смоук применяет стратагему через head-путь без падений и регрессий (baseline 23); двойного применения нет.
- DQN/PPO/GMZ/SMZ не затронуты; снос дублей и переобучение — п.5.
