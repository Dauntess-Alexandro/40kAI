# Command Re-roll — Monte-Carlo value (Shooting + Charge) — Design

**Дата:** 2026-06-22
**Статус:** согласован, готов к плану реализации
**Связанные:** `docs/superpowers/specs/2026-06-22-command-reroll-mc-value-design.md` (MC fight-first — базовая инфра), `docs/superpowers/plans/2026-06-22-command-reroll-mc-value.md` (реализация fight).

## Проблема

MC-оценка value для Command Re-roll реализована только для **fight** (fight-first). Для shooting/charge AI-решение осталось на Stage-4 вырожденном пути (`_value_pick_command_reroll` generic-loop): value subtype-агностичен и видит лишь «−1 CP» → реролл почти никогда не выбирается. Цель follow-up: дать реальный MC-сигнал для **shooting** и **charge** (advance — вне области: его move-then-derive модель делает MC плохо определённым).

## Решение (согласованные развилки)

1. **Охват:** shooting + charge. Advance отложен (позиционная выгода, реконструированный advance_roll — MC ill-defined).
2. **Репрезентативная цель = лучшая по EV** (цель выбирается внутри фазы, на старте фазы её нет → берём представителя):
   - shooting — цель с макс. ожидаемым уроном;
   - charge — chargeable-цель с лучшим melee-trade.
3. **Точка решения — старт фазы** (как fight), через существующий in-phase hook `_apply_phase_command_reroll`. **Без правок bridges/train/eval/selfplay/mcts** — shooting/charge идут через hook, не через fight-план.

## Архитектура

### Точка интеграции
`_apply_phase_command_reroll(side, phase, candidates, rolls)` (Stage 4, вызывается в начале `shooting_phase`/`charge_phase`) уже вызывает `_value_pick_command_reroll(side, u, phase, rolls)`. Расширяем **только** `_value_pick_command_reroll`: добавить ветки `phase=="shooting"` и `phase=="charge"`, дать MC-оценку (как существующая fight-ветка). Не-fight/shooting/charge (т.е. movement) — прежнее Stage-4 поведение.

Отсутствие starvation: hungry_void — fight-only; in-phase hook идёт по кандидатам независимо (не one-slot план). reaction_policy/сеть отсутствуют → parity (no-op), как в fight.

### Единый путь DQN/PPO
Как в fight: value берётся через установленную `_reaction_net_by_side[side]` и `_reaction_net_value` (DQN masked max-Q | PPO critic V). Новой per-algo логики нет.

### Компоненты — Shooting
- `_expected_shoot_damage(side: str, shooter_idx: int, target_idx: int) -> float` — аналитический EV: `attacks · P(hit) · P(wound) · P(fail_save) · avg_damage`, из статов оружия/защитника (без сети, без RNG). Используется для выбора представителя: argmax по `get_shoot_targets_for_unit(side, shooter)`.
- `_simulate_shoot_attack(side: str, shooter_idx: int, target_idx: int) -> None` — зеркало `_simulate_fight_attack`, но `attack(rangeOfComb="Ranged", distance_to_target=...)`; читает активный reroll-эффект через `_fight_effects_for_attacker(side, shooter)` + `_build_reroll_decider(side, shooter, opp_side, target, phase="shooting")`; применяет урон (`reason="shooting_sim"`). Guard на мёртвых/без цели.
- `_mc_value_command_reroll_shooting(side, unit_idx, subtype, samples) -> tuple[float,float]` — MC-цикл идентичен fight: цель = argmax `_expected_shoot_damage`; per-sample snapshot/restore + `_reaction_sim_active`; apply-ветка ставит reroll-запись (phase="shooting", subtype); `_simulate_shoot_attack`; `_reaction_net_value`; усреднение. `(0.0,0.0)` если нет сети/целей.

### Компоненты — Charge
- Репрезентативная цель: chargeable-цель (из `get_charge_targets_for_unit(side, unit)`) с макс. melee-преимуществом `_melee_strength_score(side, unit) − _melee_strength_score(opp_side, target)`, тай-брейк — ближайшая.
- `_simulate_charge_attempt(side: str, unit_idx: int, target_idx: int) -> None` — бросок 2D6 (через `_charge_roll_with_reroll`, который уже перебрасывает обе кости при активной записи); при успехе (`dist - total <= 5`, как в charge_phase) выставить `inAttack[unit]=[1,target]` и `oppInAttack[target]=[1,unit]`; value-голова отразит «в бою». Без реального перемещения (sim только для value).
- `_mc_value_command_reroll_charge(side, unit_idx, subtype="charge", samples) -> tuple[float,float]` — MC-цикл; apply-ветка ставит charge-reroll-запись (phase="charge"); цель = best-trade.

### Интеграция в `_value_pick_command_reroll`
```
if phase == "fight":   ... (как сейчас) ...
elif phase == "shooting":  rolls=("hit","wound"); MC через _mc_value_command_reroll_shooting; argmax mean_apply > mean_pass + eps
elif phase == "charge":    rolls=("charge",);     MC через _mc_value_command_reroll_charge
else:  ... generic Stage-4 (movement) ...
```
Выбор подтипа для shooting перестаёт быть вырожденным (MC различает hit/wound по исходу выстрела).

## Конфиг
Переиспользуем `CMDREROLL_MC_SAMPLES` (дефолт 8) и `CMDREROLL_MC_EPS` (дефолт 1e-3). Новых флагов нет. Всегда вкл (train+eval), гейт по `reaction_policy` + сеть стороны → без них parity.

## Тестирование (TDD)
- `_expected_shoot_damage` — детерминированный расчёт на известных статах (S/T/Sv/AP/attacks/damage).
- Выбор представителя shooting (argmax EV) и charge (best-trade) — на сконструированных целях.
- `_simulate_shoot_attack` / `_simulate_charge_attempt` — детерминированные (monkeypatch/seed): реролл-запись → больше урона / успех чарджа.
- `_mc_value_command_reroll_shooting` / `_charge` — стаб-нет HP-aware: apply>pass когда реролл помогает; equal когда нет (monkeypatch sim, как в fight-тестах).
- `_value_pick_command_reroll` ветки shooting/charge: выбор подтипа / None ниже eps.
- Интеграция: `shooting_phase`/`charge_phase` под установленной policy применяют command_reroll; **parity** без policy (no-op); DQN и PPO.
- Регрессия: `tests/engine/` baseline 23 failed; `tests/models/`, `tests/engine/phases/` зелёные.

## Риски / open questions
- **Перф:** MC теперь и в shooting/charge каждый ход. Митигация: малый N, дешёвый аналитический EV-пикер (без сети), только кандидаты с CP, recursion-guard. Замерить на train-смоуке.
- **Charge value-сигнал** зависит от того, кодирует ли obs состояние `inAttack` (engagement). Скорее да (движок экспортит inAttack), иначе сигнал слабый — проверить на смоуке; при нуле — диагностировать как с fight (не подгонять).
- **Open:** charge-представитель «best-trade» vs «ближайший достижимый» — для решения о рерролле релевантнее borderline-дистанция; берём best-trade по согласованию, при слабом сигнале пересмотреть.
- Симуляции не учитывают ответную реакцию противника (YAGNI, как fight).

## Вне области
- Advance MC.
- Изменение точки решения на сам бросок (roll-time).
- Учёт реакций противника.

## Критерии готовности
- Новые методы и ветки покрыты тестами (DQN+PPO), parity сохранён, регрессий нет.
- На eval-смоуке (где shooting/charge command_reroll не стравливается hungry_void — это не-fight фазы) в логах появляются применения `command_reroll` в shooting/charge, которых не было до изменения. Если ноль — диагностировать (перф/eps/obs-чувствительность), не подгонять тесты.
