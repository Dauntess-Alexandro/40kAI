# Command Re-roll — Monte-Carlo value (fight-first) — Design

**Дата:** 2026-06-22
**Статус:** согласован, готов к плану реализации
**Связанные:** `docs/superpowers/plans/2026-06-22-command-reroll-fidelity.md` (механика Command Re-roll, этапы 1–4), `docs/superpowers/specs/2026-06-19-b3-reaction-value-policy-design.md` (reaction value-policy).

## Проблема

Механика Command Re-roll реализована полностью (этапы 1–4, fidelity-план), но **AI почти никогда не выбирает реролл**. Причина структурная: решение «использовать ли» принимается **до броска** через value-lookahead, а observation и value-голова **не видят выгоды реролла** — на момент решения известно лишь, что реролл стоит −1 CP и ставит флаг `stratagem_used`. Подтверждено eval-смоуком (3 игры, `command_reroll`=0 применений при `applied_total=83`).

Источник: `_value_pick_command_reroll` ([core/envs/warhamEnv.py]) вызывает `reaction_policy` с `resolve_trigger=None` — value-ветка apply сравнивается с pass на состоянии, где сам бросок не симулирован.

## Решение (согласованные развилки)

1. **Подход B — Monte-Carlo `resolve_trigger`.** В value-ветке симулировать сам бросок юнита с рероллом (apply) и без (pass), усреднить по N сэмплам, сравнить средние. Реальный сигнал выгоды, **без переобучения**, на готовой инфре. (Отвергнут подход A: obs-признак + переобучение — ломает чекпойнты по obs-dim, дорого, сигнал всё равно слабый.)
2. **Fight-first.** Только fight-фаза: цель атаки известна на старте фазы (`unitInAttack[u]`), симуляция атаки чистая. Shooting/charge/advance — follow-up отдельным планом (у них цель/действие выбираются внутри фазы → нужна аппроксимация цели). Roll-time decider внутри `attack()` отвергнут как самый инвазивный.
3. **Всегда вкл (train+eval).** MC работает везде, где установлен `reaction_policy`. Перф-риск гасится малым N и пре-фильтром (только engaged-юниты с CP).

## Архитектура

### Единый путь для DQN/PPO
MC-оценщик живёт в `warhamEnv` и читает установленную сеть стороны через `self._reaction_net_by_side[side]` — какой алго её положил (`install_dqn_stratagem_policy` / `install_ppo_stratagem_policy`), та и используется. Извлечение value — тем же интерфейсом `net.infer_with_value(obs, masks_by_head)`, что и существующий `_simulate_reaction_branch`:
- **DQN**: V-прокси = masked max-Q (нужны per-head маски).
- **PPO**: честный critic V (`masks_by_head=None`).

Разница прозрачна для MC. Отдельной MC-реализации на алго нет.

```
DQN-ран: install_dqn → _reaction_net_by_side={"model": dqn_net} ─┐
PPO-ран: install_ppo → _reaction_net_by_side={"model": ppo_net} ─┤→ _mc_value_command_reroll_fight (env)
                                                                  └→ infer_with_value (max-Q | critic V)
```

### Компоненты

1. **resolve_trigger для fight-атаки** — замыкание `_rt(apply)`, которое пересимулирует melee-атаку engaged-юнита по его цели (`unitInAttack[u][1]`):
   - `apply=True`: реролл активен через существующий механизм (effect-запись подтипа hit/wound + `reroll_decider`/`_fight_effects_for_attacker`, как в этапах 1–2);
   - `apply=False`: атака без реролла;
   - урон применяется к sim-состоянию (`_apply_health_update`), как в прецеденте `_set_shot_reaction_trigger`.

2. **`_mc_value_command_reroll_fight(side, unit_idx, subtype, samples) → (mean_apply, mean_pass)`**:
   - для каждой ветки (pass/apply) гоняет `samples` итераций: inner `snapshot_state()` → `simulation_mode()` → (apply: поставить reroll-запись подтипа) → `_rt(apply)` симулирует атаку с RNG → `net.infer_with_value` → restore;
   - усредняет значения по сэмплам;
   - recursion-guard `_reaction_sim_active`; сторона без сети → возвращает «не применять».

3. **Интеграция решения** — `_value_pick_command_reroll` для `phase=="fight"`:
   - для каждого подтипа из `("hit","wound")` считает `(mean_apply, mean_pass)` через MC;
   - выбирает подтип с макс. `mean_apply`, если он `> mean_pass + eps`; иначе `None`;
   - **бонус:** подтип перестаёт быть вырожденным — MC различает hit vs wound (разные исходы атаки), что чинит ограничение Stage 4.
   - Для не-fight фаз поведение Stage 4 без изменений.

4. **Пре-фильтр в bridges** — `dqn_build_fight_plan` / `ppo_build_fight_plan` (они 1:1 зеркала): **только для `command_reroll`** предлагать engaged-юнитам с CP дешёвым пре-фильтром, **без** слабого value-гейта `apply→value`; финальное «да/нет» и подтип — за MC в `_apply_pending_fight_stratagem_plan`. **`hungry_void` и прочие стратагемы — без изменений** (сохраняют свой `apply→value` гейт). Для `command_reroll` обходим слабый `_should_use_stratagem` (он без resolve_trigger всегда видит −CP).

### Поток данных (fight)
```
fight_phase(side)
  → _apply_pending_fight_stratagem_plan(side)
      для command_reroll-записи плана:
        subtype, ok = _value_pick_command_reroll(side, u, "fight", ("hit","wound"))   # MC внутри
        если ok: _apply_stratagem(..., reroll_roll=subtype)
  → resolve_fight_phase   # реальная атака читает reroll-запись (decider/effect)
```

## Конфиг
- `CMDREROLL_MC_SAMPLES` (env, дефолт **8**) — сэмплов на ветку.
- `eps` — порог `mean_apply > mean_pass + eps` (переиспользуем стиль `1e-3`, можно поднять для устойчивости к шуму, напр. небольшой положительный порог).
- Всегда вкл; гейт только по наличию `reaction_policy` + сети стороны → без них полный parity со Stage 4.

## Тестирование (TDD)
- **MC-оценщик** — стаб-нет, value = f(enemy_health) (меньше HP врага → выше value): сетап, где реролл добивает → `mean_apply > mean_pass`; где бесполезен → `None`.
- **Выбор подтипа** — сетап, где выгоден реролл wound (а не hit) → MC выбирает `"wound"` (фикс вырожденности Stage 4).
- **Интеграция fight** — установленная policy + MC: `command_reroll` применяется на engaged-юните, где помогает; не применяется, где нет.
- **Parity** — без `reaction_policy` → no-op (поведение Stage 4).
- **DQN и PPO** — по одному интеграционному на каждый (оба через `infer_with_value`).
- **Регрессии** — `tests/engine/` остаётся на baseline (23 failed предсуществующих); `tests/models/`, `tests/engine/phases/` зелёные.

## Риски / open questions
- **Перф** (всегда вкл в train): N× симуляций атаки × подтип на engaged-юнита за каждый fight. Митигация: малый N (8), только engaged+CP, recursion-guard. **Замерить на train-смоуке**; при необходимости снизить N или ввести отдельный train-флаг.
- **Вариация**: малый N шумит → нестабильный выбор; `eps`-маржа сглаживает. Возможна настройка N/eps по результатам смоука.
- **Чувствительность value-головы** к HP врага: если сеть грубая — сигнал слабее, но ненулевой (в отличие от Stage 4).
- **Open**: учитывать ли в resolve_trigger ответную атаку цели — пока нет (YAGNI), симулируем только атаку нашего юнита.

## Вне области
- Shooting / charge / advance MC (нужна аппроксимация цели на старте фазы) — отдельный follow-up план.
- Подход A (obs-признак + переобучение) — не делаем.
- Учёт реакций противника в симуляции броска.

## Критерии готовности
- MC-оценщик и интеграция покрыты тестами (DQN+PPO), parity сохранён, регрессий нет.
- На eval-смоуке с обученной моделью в логах появляются применения `command_reroll` в fight (`[WH40K][STRATAGEM] applied=command_reroll ... phase=fight`), которых не было до изменения.
