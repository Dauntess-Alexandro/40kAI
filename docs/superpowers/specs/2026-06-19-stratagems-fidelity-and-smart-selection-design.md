# Стратагемы: точность правил W40k 10e + единый «умный» выбор агентом

- **Дата:** 2026-06-19
- **Ветка:** worktree2
- **Статус:** design (approved)
- **Контекст:** по итогам аудита всех стратагем проекта (несоответствия Wahapedia + раздробленность каналов выбора).

## 1. Проблема

В проекте 7 стратагем (6 core + Necron `hungry_void`). Аудит выявил:

**Расхождения с правилами 10e:**
- `command_reroll` — реролл ВСЕХ проваленных wound-бросков вместо одного (явный перекос силы).
- `overwatch` — гейт дальности = дальность оружия, а не 24"; нет проверки LOS; лимит `PER_PHASE` (срабатывает и в movement, и в charge → потенциально 2× за ход вместо once-per-turn).
- `go_to_ground` — код-комментарий неверно описывает правило («+1 к save»); реально — Benefit of Cover + 6+ invuln save.
- `smokescreen` — не моделируется Stealth.
- `hungry_void` — нет AP+1 при Character-лидере, нет keyword-гейта NECRONS, нет таргета «ещё не дрался».

**Архитектурные проблемы:**
- `use_cp` heads 2/3/4 (overwatch/smokescreen/heroic) в плоском `action_dict` мёртвые — ничего не исполняют.
- Fight-стратагемы (`hungry_void`, `command_reroll`) молча обнуляются под `windowed_selfplay` (обучающаяся сторона их не применяет).
- Метрика `cp_used` в eval считает `use_cp>0` (нажатие head), а не реальное применение.
- Стратагемы раздроблены на 3 несвязанных канала решения (плоский head / fight-план / reaction-policy).

**Эталон правил (Wahapedia, частично сверено; core-страница давала HTTP 404, верифицировано связкой WebSearch + знание 10e):**
- Insane Bravery: 1 CP, once per battle — корректна.
- Fire Overwatch: 1 CP, цель в 24" и видима, hits only on unmodified 6, once per turn.
- Smokescreen: 1 CP, SMOKE-юнит, Benefit of Cover + Stealth, без лимита.
- Go to Ground: 1 CP, INFANTRY-юнит, Benefit of Cover + 6+ invuln save, без лимита.
- Heroic Intervention: 2 CP (код корректен; фетч галлюцинировал «1 CP / WALKER only»).
- Command Re-roll: 1 CP, реролл одного броска, любая фаза.
- Protocol of the Hungry Void (Necrons, Awakened Dynasty): 1 CP, Fight phase, NECRONS-юнит ещё не дравшийся; +1 Strength melee; если ведёт Character-лидер — дополнительно AP улучшается на 1.

## 2. Цель

Полный объём: **и точность правил, и ум агента**.
1. Привести эффекты/условия/лимиты стратагем к 10e (включая «глубокие» механики: 24"+LOS, 6+ invuln, Stealth, AP+1/keyword).
2. Свести выбор всех стратагем к единому value-ориентированному механизму, чтобы AZ-агент осмысленно решал «применять или нет».
3. Дать честные метрики применения.

## 3. Архитектура: единый value-выбор

`reaction_value_policy` (B3-full, 1-ply lookahead) обобщается в общий **stratagem value gate** для ВСЕХ стратагем (command/fight/reaction).

**Механизм** (обобщение `_should_use_reaction` → `_should_use_stratagem(ctx)` + `make_reaction_value_policy` → `make_stratagem_value_policy`):
1. snapshot состояния;
2. для веток `apply` / `pass` досимулировать триггер (`resolve_trigger`) через `_simulate_reaction_branch` (переиспользуется);
3. value-голова сети обучающейся стороны (`net_by_side[side]`);
4. выбрать ветку с большей ценностью; тай → `pass` (экономия CP);
5. recursion-guard `_reaction_sim_active`.

**Перевод точек вызова на общий гейт:**
- Реакции (overwatch/smokescreen/go_to_ground/heroic) — уже на нём (обобщение/переименование, поведение неизменно).
- Fight (`hungry_void`/`command_reroll`) — `_apply_pending_fight_stratagem_plan` перестаёт обнуляться под windowed; каждый юнит-кандидат с активной fight-стратагемой проходит value-гейт; `resolve_trigger` = эффект на бой этого юнита.
- Insane Bravery — решение в `command_phase` идёт через тот же гейт вместо `action.get("use_cp")==1`.

**Parity:** при отсутствии политики (`stratagem_policy is None`) — поведение байт-в-байт прежнее (эвристический оппонент без сети, старые тесты/replay). Источник сети — `net_by_side` по реагирующей/действующей стороне. Включение — флаг по аналогии с reaction_value_policy (env / hyperparams).

## 4. Изменения по правилам (боёвка/реестр)

| Стратагема | Изменение |
|---|---|
| **Command Re-roll** | `reroll_wounds: "all"` → `"one"` (реролл одного «худшего» проваленного wound-броска). Остаётся fight-only (осознанное упрощение). |
| **Fire Overwatch** | Гейт дальности → фикс. 24" (не дальность оружия); проверка LOS через `_visibility_report_between_units` перед выстрелом; `usage_limit` → `PER_TURN`. |
| **Go to Ground** | Новый эффект `benefit_of_cover_invuln6`: Benefit of Cover + 6+ invuln (через существующий `inv` в `attack()`). Исправить комментарий в реестре. |
| **Smokescreen** | Новая механика `hit_penalty` в `attack()` (Stealth → атакующему -1 к hit, не лучше 6+). Эффект = cover + stealth. |
| **Hungry Void** | `ap_improve=1` только при Character-лидере; keyword-гейт NECRONS (`keyword_req`); таргет «ещё не дрался» (юнит без отметки fought в этой фазе). Нужен признак «юнит ведёт Character» в данных юнита. |
| **Insane Bravery** | Без изменений. |

**Новые механики в `attack()` (назад-совместимо через `_normalize_effects`):**
- `hit_penalty: int` — штраф к hit-роллу атакующего (для Stealth). Натуральная 6 всегда попадает.
- `invuln_grant: int` — даровать инвул N+ цели, если у неё нет лучшего (для Go to Ground 6+).

## 5. Наблюдаемость и метрики

- В eval: заменить `cp_used` (`use_cp>0`) на `strat_applied` (diff журнала `stratagem_used`) и `strat_attempt`, с разбивкой по `stratagem_id`. `cp_used` либо удалить, либо переименовать в `use_cp_head_set`.
- Убрать/задокументировать мёртвые `use_cp` heads 2/3/4.
- Логи по правилу AGENTS.md: при отказе стратагемы (вне 24" / нет LOS / нет CP / usage_limit) — явная строка «что случилось + где + что дальше».

## 6. Тесты (TDD, до кода)

- `test_command_reroll_single` — рероллится один бросок, не все.
- `test_overwatch_24_and_los` — нет overwatch >24" и без LOS; once-per-turn (нет второго в charge после movement).
- `test_go_to_ground_invuln` — AP-heavy выстрел сейвится на 6+.
- `test_smokescreen_stealth` — -1 к hit у атакующего по SMOKE-юниту.
- `test_hungry_void_ap_character` / `test_hungry_void_keyword_gate` — AP+1 только при Character-лидере; гейт NECRONS.
- `test_windowed_selfplay_fight_stratagems` — fight-стратагемы применяются под windowed.
- `test_stratagem_value_gate_parity` — без политики поведение = legacy.
- `test_cp_used_metric_honest` — метрика считает применение, не нажатие head.

## 7. Порядок работ (фазы с чекпойнтами)

1. **Фаза A — фиксы правил**: реестр (`stratagems.py`) + механики `attack()` (`utils.py`) + метрики/комменты/мёртвые heads. Каждая стратагема — тест→код.
2. **Фаза B — единый value-гейт**: обобщить `_should_use_reaction`/`reaction_value_policy`, закрыть windowed-дыру, перевести fight + bravery на гейт.
3. **Фаза C — интеграция и smoke**: eval-метрики, короткий прогон train/eval, parity-проверка Δ=0 без политики.

Каждая фаза — чекпойнт: `engine-regression-reviewer` перед коммитом (CLAUDE.md). Язык логов/UI — русский. Платформа — Windows.

## 8. Затронутые файлы

- `core/engine/phases/stratagems.py` — реестр (эффекты/лимиты/keyword/комменты).
- `core/engine/phases/stratagem_engine.py` — payload эффектов (`reroll_wounds`, `ap_improve`, новый invuln/stealth).
- `core/engine/utils.py` — `attack()` + `_normalize_effects` (hit_penalty, invuln_grant, single-reroll).
- `core/envs/warhamEnv.py` — `_resolve_overwatch` (24"/LOS/limit), `_maybe_use_go_to_ground` (invuln), `_maybe_use_smokescreen` (stealth), `_fight_effects_for_attacker`, `_apply_pending_fight_stratagem_plan` (windowed fix), `command_phase` (bravery через гейт), `_should_use_stratagem`.
- `core/models/reaction_value_policy.py` → обобщить в stratagem value policy.
- `eval.py` — метрики `strat_applied`/`strat_attempt` вместо `cp_used`.
- `tests/engine/phases/` — новые тесты (см. §6).

## 9. Риски / открытые вопросы

- Признак «юнит ведёт Character-лидера» — нужно проверить, есть ли он в данных юнитов; если нет — минимальный гейт (по keyword leader) либо отложить AP-бонус.
- Stealth (`hit_penalty`) — первая hit-механика в `attack()`; проверить взаимодействие с `hit_on_6` (Overwatch): при overwatch уже только 6+, stealth не должен делать строже.
- Включение value-гейта для command/fight может сдвинуть динамику обучения — фаза C проверяет parity без политики и smoke с политикой.
