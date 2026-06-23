# Стратагемы как действия — Под-проект 5a (снос стопгапов) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Сделать strat-головы единственным путём MAIN-стратагем активной стороны: переставить bravery на `strat_command`, снести MC command_reroll-машинерию и fight-план стратагем, убрать `use_cp`/`cp_on` из контракта — НЕ трогая реакции оппонента и движковый мех реролла.

**Architecture:** Точечный снос стопгапов. Реакции (overwatch/go_to_ground/smokescreen/heroic) и `reaction_policy`/`_should_use_reaction` ОСТАЮТСЯ. Движковый мех реролла (`attack` decider/effect, `_apply_action_stratagem`, маски, legacy_patch) ОСТАЁТСЯ. После сноса фазы применяют стратагемы только через `_apply_action_stratagem` (head); AZ — через головы (joint_tuple).

**Tech Stack:** Python 3.12+, NumPy, PyTorch, pytest. Windows.

## Global Constraints

- **Источник дизайна:** `docs/superpowers/specs/2026-06-22-stratagem-action-cleanup-retrain-design.md`. **Под-проект 5a из проекта «стратагемы как действия»** (5b = runbook переобучения, отдельно).
- **(U)-снос:** головы — единственный путь MAIN-стратагем. После сноса в живой игре стратагемы инертны до переобучения (5b) — ОЖИДАЕМО; тесты используют рукотворные action_dict (головы заданы).
- **НЕ ТРОГАТЬ (страховка регрессией):** `reaction_policy`, `_should_use_reaction`, `_simulate_reaction_branch`, `_reaction_net_value`, реакции (`_maybe_use_go_to_ground`/`_maybe_use_smokescreen`/overwatch/heroic), `_set_shot_reaction_trigger`; движковый мех реролла (`attack()` reroll_decider/effect, `_build_reroll_decider`, `_apply_action_stratagem`, `_apply_stratagem`, маски п.2, legacy_patch п.4, `_stratagem_already_active`, `_consume_command_reroll_record`/advance/charge reroll helpers).
- **install_*_stratagem_policy** (reaction_policy для реакций) — ОСТАЁТСЯ; удаляется только `*_build_fight_plan`.
- Язык RU; `ruff check --fix`; коммит RU + `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. TDD. **engine-regression-reviewer обязателен на каждой задаче** (снос — риск задеть лишнее).
- **Baseline пересчитывается** (контракт меняется): после каждой задачи сверять `tests/engine/` набор; обновлять AZ n_actions/контракт-тесты под новый размер.

---

## File Structure

| Файл | Что меняем | Задачи |
|------|-----------|--------|
| `core/envs/warhamEnv.py` | bravery-flip; снос MC-методов + phase-hook вызовов; снос fight-план веток + `_pending_fight_stratagem_plan`/snapshot | 1,2,3 |
| `core/models/dqn_stratagem_bridge.py`, `core/models/ppo_stratagem_bridge.py` | снос `*_build_fight_plan` + command_reroll prefilter (install_* остаётся) | 2,3 |
| `core/models/option_candidates.py` | снос `_fight_stratagem_plan_from_choices`, `attach_fight_stratagem_plan`, `fight_stratagem_plan`-поля | 3 |
| `core/models/alphazero_mcts.py`, `alphazero_selfplay.py`, `train.py`, `eval.py` | снос вызовов `attach_fight_stratagem_plan`/`*_build_fight_plan`/`last_selected_fight_plan` | 2,3 |
| `core/models/action_contract.py`, `core/engine/phases/legacy_compiler.py`, `core/envs/warhamEnv.py`, `core/models/utils.py` | убрать use_cp/cp_on из контракта | 4 |
| `tests/...` | удалить/переписать тесты снесённых путей | 1–4 |

---

## Task 1: Bravery-flip (strat_command primary)

**Files:** Modify `core/envs/warhamEnv.py` (`command_phase`, ветки `_use_bravery` model ~5363 и enemy ~5450). Test: `tests/engine/phases/test_stratagem_action_apply.py`.

**Interfaces:**
- Produces: `command_phase` применяет Insane Bravery ТОЛЬКО по `strat_command`-голове (+ `decide_bravery`-override, если задан); reaction_policy- и use_cp-ветки для bravery удалены.

- [ ] **Step 1: Падающий тест (use_cp больше НЕ триггерит bravery; strat_command — да)**

В `tests/engine/phases/test_stratagem_action_apply.py` добавить:
```python
def test_bravery_via_use_cp_no_longer_triggers():
    env = build_env()
    _setup(env)
    env.phase = "command"
    env.unit_health[0] = 1.0
    env.unit_data[0]["Ld"] = 13  # 2D6<=12<13 → провал battle-shock
    action = flat_default_action(len(env.unit_health), use_cp=1, cp_on=0)
    # strat_command не задан (0) → bravery НЕ должен примениться (head-only)
    with env.simulation_mode():
        env.command_phase("model", action=action)
    assert not any(r[1] == "insane_bravery" for r in env.stratagem_used)
```
(Существующий `test_command_strat_head_triggers_bravery` должен продолжать проходить — strat_command триггерит.)

- [ ] **Step 2: Запустить — упадёт** (сейчас use_cp ещё триггерит bravery).

Run: `python -m pytest tests/engine/phases/test_stratagem_action_apply.py -k "bravery" -v`

- [ ] **Step 3: Реализация** — в обеих ветках `_use_bravery` (model ~5363, enemy ~5450) заменить трёхветочную логику на head-primary. Найти блок:
```python
                        if getattr(self, "reaction_policy", None) is not None and decide_bravery is None:
                            _use_bravery = self._should_use_stratagem(... "insane_bravery" ...)
                        elif decide_bravery is not None:
                            _use_bravery = bool(decide_bravery(i))
                        else:
                            _use_bravery = bool(action and action.get("use_cp") == 1 and action.get("cp_on") == i)
                            if not _use_bravery and isinstance(action, dict):
                                <strat_command check>
```
заменить на:
```python
                        if decide_bravery is not None:
                            _use_bravery = bool(decide_bravery(i))
                        else:
                            _use_bravery = False
                            if isinstance(action, dict):
                                from core.engine.phases.stratagems import stratagem_choice_str
                                from core.engine.phases.types import Phase as _Ph
                                if (
                                    stratagem_choice_str(_Ph.COMMAND, int(action.get("strat_command", 0) or 0)) == "insane_bravery"
                                    and int(action.get("strat_command_unit", 0) or 0) == i
                                ):
                                    _use_bravery = True
```
(reaction_policy-ветка для bravery удалена; use_cp/cp_on более не читается для bravery. `decide_bravery`-override сохранён.)

- [ ] **Step 4: PASS + регрессия**

Run: `python -m pytest tests/engine/phases/test_stratagem_action_apply.py tests/engine/phases/test_command_bravery_via_engine.py tests/engine/phases/test_stratagem_insane_bravery.py -v` → PASS (обновить тесты, которые ждали use_cp-bravery — переписать на strat_command/decide_bravery). `ruff check --fix core/envs/warhamEnv.py`.

- [ ] **Step 5: engine-regression-reviewer + Коммит**
```
git add core/envs/warhamEnv.py tests/engine/phases/test_stratagem_action_apply.py <обновлённые bravery-тесты>
git commit -m "refactor(env): Insane Bravery — strat_command primary (снос reaction_policy/use_cp bravery-веток)"
```

---

## Task 2: Снос MC command_reroll-машинерии

**Files:** Modify `core/envs/warhamEnv.py` (методы + phase-hook вызовы), `core/models/dqn_stratagem_bridge.py`/`ppo_stratagem_bridge.py` (command_reroll prefilter). Delete/rewrite tests `tests/models/test_command_reroll_mc_*.py`, `tests/models/test_command_reroll_value_policy.py`, `tests/engine/phases/test_command_reroll_phases.py`.

**Interfaces:**
- Produces: shooting/charge/movement/fight применяют command_reroll ТОЛЬКО через `_apply_action_stratagem` (head); MC value-путь удалён.

- [ ] **Step 1: Падающий тест (MC-методов больше нет; head-путь жив; реакции целы)**
```python
def test_mc_value_methods_removed():
    env = build_env()
    _setup(env)
    for name in ("_value_pick_command_reroll", "_apply_phase_command_reroll",
                 "_mc_value_command_reroll_fight", "_mc_value_command_reroll_shooting",
                 "_mc_value_command_reroll_charge", "_simulate_fight_attack",
                 "_simulate_shoot_attack", "_simulate_charge_attempt"):
        assert not hasattr(env, name), f"{name} должен быть удалён (снос MC, под-проект 5a)"


def test_head_path_still_applies_command_reroll_fight():
    env = build_env()
    _setup(env)
    env.unit_health[0] = 6.0; env.enemy_health[0] = 6.0
    env.unitInAttack[0] = [1, 0]; env.enemyInAttack[0] = [1, 0]
    env.unitCharged = [0]*len(env.unit_health); env.enemyCharged = [0]*len(env.enemy_health)
    from core.engine.phases.stratagems import stratagem_choice_index
    action = flat_default_action(len(env.unit_health))
    action["strat_fight"] = stratagem_choice_index(Phase.FIGHT, "command_reroll:hit")
    action["strat_fight_unit"] = 0
    with env.simulation_mode():
        env.fight_phase("model", action=action)
    assert any(r[1] == "command_reroll" and r[3] == "fight" for r in env.stratagem_used)
```
(в `tests/engine/phases/test_stratagem_action_apply.py`)

- [ ] **Step 2: Запустить — упадёт** (`test_mc_value_methods_removed` падает — методы ещё есть).

- [ ] **Step 3: Реализация (снос)**
  - В `core/envs/warhamEnv.py` УДАЛИТЬ методы: `_value_pick_command_reroll`, `_apply_phase_command_reroll`, `_mc_value_command_reroll_fight`, `_mc_value_command_reroll_shooting`, `_mc_value_command_reroll_charge`, `_simulate_fight_attack`, `_simulate_shoot_attack`, `_simulate_charge_attempt`, `_best_shoot_target`, `_best_charge_target`, `_expected_shoot_damage`; module-level `_cmdreroll_mc_samples`/`_cmdreroll_mc_eps`.
  - Удалить ВЫЗОВЫ `self._apply_phase_command_reroll(...)` в `movement_phase`/`shooting_phase`/`charge_phase` (оставив `_apply_action_stratagem` head-вызов).
  - В `dqn_build_fight_plan`/`ppo_build_fight_plan` удалить ветку `if d.id == "command_reroll": plan[u]=d.id; continue` (Task 5/fight-MC). [Полный снос build_fight_plan — Task 3.]
  - Сохранить: `_apply_action_stratagem`, `_build_reroll_decider`, `_command_reroll_record_exists` (если используется `_apply_action_stratagem`/anti-double — свериться; если нет потребителей после Task 3 — удалить в Task 3), `_consume_command_reroll_record`/`_advance_roll_with_reroll`/`_charge_roll_with_reroll` (мех реролла).
  - УДАЛИТЬ тест-файлы снесённых MC-фич: `tests/models/test_command_reroll_mc_value.py`, `tests/models/test_command_reroll_mc_shooting_charge.py`, `tests/models/test_command_reroll_value_policy.py`; в `tests/engine/phases/test_command_reroll_phases.py` — удалить/переписать тесты, звавшие MC/`_apply_phase_command_reroll` (оставить чисто-механические реролл-тесты, если есть).

- [ ] **Step 4: PASS + регрессия**

Run: `python -m pytest tests/engine/phases/ tests/models/ -q` → PASS (после удаления MC-тестов). **Реакции:** `python -m pytest tests/engine/phases/test_reaction_*.py tests/engine/phases/test_go_to_ground.py tests/engine/phases/test_reaction_overwatch.py -v` → PASS (НЕ сломаны). `python -m pytest tests/engine/ -q` → новый baseline (зафиксировать). `ruff check --fix` по изменённым.

- [ ] **Step 5: engine-regression-reviewer + Коммит**
```
git add -A
git commit -m "refactor(env): снос MC command_reroll-машинерии (head — единственный путь); реакции/мех реролла целы"
```

---

## Task 3: Снос fight-план стратагем

**Files:** Modify `core/envs/warhamEnv.py` (`_apply_pending_fight_stratagem_plan` стратагем-ветки + `_pending_fight_stratagem_plan` snapshot/init), `core/models/option_candidates.py` (`_fight_stratagem_plan_from_choices`, `attach_fight_stratagem_plan`, `fight_stratagem_plan`/`fight_plans` поля), bridges (`*_build_fight_plan` целиком), `alphazero_mcts.py`/`alphazero_selfplay.py`/`train.py`/`eval.py` (вызовы attach/build_fight_plan/last_selected_fight_plan). Delete tests `test_dqn/ppo_stratagem_bridge` (fight-plan), `test_option_candidates` (fight-plan части), `test_windowed_fight_stratagem`, `test_windowed_selfplay_fight`.

**Interfaces:**
- Produces: fight-стратагемы применяются ТОЛЬКО через head (`_apply_action_stratagem`); fight-план механизм удалён.

- [ ] **Step 1: Падающий тест**
```python
def test_fight_plan_mechanism_removed():
    env = build_env(); _setup(env)
    assert not hasattr(env, "_apply_pending_fight_stratagem_plan")
    from core.models import option_candidates as oc
    assert not hasattr(oc, "attach_fight_stratagem_plan")
    assert not hasattr(oc, "_fight_stratagem_plan_from_choices")
```

- [ ] **Step 2: Запустить — упадёт.**

- [ ] **Step 3: Реализация (снос)**
  - `warhamEnv.py`: удалить `_apply_pending_fight_stratagem_plan` + его вызов в `fight_phase` (оставив `_apply_action_stratagem`); удалить `_pending_fight_stratagem_plan` из `__init__`/snapshot/restore (строки ~1305-1306/1389-1391); `_command_reroll_record_exists` — если больше не используется (был для colon-anti-double в fight-плане), удалить; иначе оставить.
  - `option_candidates.py`: удалить `_fight_stratagem_plan_from_choices`, `attach_fight_stratagem_plan`, поля `fight_stratagem_plan` (`TurnPlanCandidate`), `fight_plans`/`fight_plan_for` (`RootJointCandidates`); вызов `_fight_stratagem_plan_from_choices` в `_turn_plan_from_choices`.
  - `dqn_stratagem_bridge.py`/`ppo_stratagem_bridge.py`: удалить `dqn_build_fight_plan`/`ppo_build_fight_plan` целиком (install_* + reaction-value-policy ОСТАЮТСЯ).
  - `alphazero_mcts.py`: удалить импорт/вызовы `attach_fight_stratagem_plan` (~391, ~800) и `last_selected_fight_plan`-проводку; `alphazero_selfplay.py` ~137/147 — удалить attach.
  - `train.py` (~5466-5477, ~5869-5881), `eval.py` (~672-674, ~725, ~703), `core/telemetry/stratagem_trace.py` (~289-310), `core/models/eval_agent.py` (~172, `_fight_plan`/`as_policy_fn` attach) — удалить вызовы `attach_fight_stratagem_plan`/`*_build_fight_plan`/`_pending_fight_stratagem_plan`-чтение. (AZ/DQN/PPO теперь применяют стратагемы через головы.)
  - Удалить/переписать тесты: `tests/models/test_dqn_stratagem_bridge.py`/`test_ppo_stratagem_bridge.py` (fight-plan части; install-тесты оставить), `tests/models/test_option_candidates.py` (fight-plan части), `tests/engine/phases/test_windowed_fight_stratagem.py`, `tests/engine/phases/test_windowed_selfplay_fight.py`.

- [ ] **Step 4: PASS + регрессия + AZ смоук**

Run: `python -m pytest tests/engine/phases/ tests/models/ -q` → PASS. `python -m pytest tests/engine/ -q` → baseline. **AZ self-play смоук (контроллер):** `TRAIN_ALGO=alphazero_tree AZ_INFERENCE_SERVER=0 AZ_DISTRIBUTED_ACTORS=0 TRAIN_EPISODES_OVERRIDE=4 NUM_ACTORS=1 python train.py` → exit=0 без traceback (AZ работает без fight-плана, стратагемы через головы). `ruff check --fix`.

- [ ] **Step 5: engine-regression-reviewer + Коммит**
```
git add -A
git commit -m "refactor(models): снос fight-план механизма стратагем (head — единственный путь; AZ через joint_tuple)"
```

---

## Task 4: Убрать use_cp/cp_on из контракта

**Files:** Modify `core/models/action_contract.py` (`BASE_ACTION_HEADS`), `core/engine/phases/legacy_compiler.py` (`default_action_dict`), `core/envs/warhamEnv.py` (`action_space` ~1045-1052 + use_cp/cp_on маски ~1819-1841), `core/models/utils.py` (`convertToDict`-инференс). Update contract tests.

**Interfaces:**
- Produces: контракт без `use_cp`/`cp_on`; `ordered_action_keys` = `["move","attack", per-unit..., strat_<phase>...]`.

- [ ] **Step 1: Падающий тест**
```python
def test_contract_has_no_use_cp_cp_on():
    from core.models.action_contract import ordered_action_keys
    keys = ordered_action_keys(2)
    assert "use_cp" not in keys and "cp_on" not in keys
    assert "move" in keys and "attack" in keys
    # strat-головы на месте
    assert "strat_command" in keys
```
(в `tests/models/test_action_contract_stratagems.py`)

- [ ] **Step 2: Запустить — упадёт.**

- [ ] **Step 3: Реализация**
  - `action_contract.py`: `BASE_ACTION_HEADS = ["move", "attack"]` (убрать use_cp/cp_on).
  - `legacy_compiler.py` `default_action_dict`: убрать `"use_cp": 0, "cp_on": 0`.
  - `warhamEnv.py` `action_space` (~1045-1052): убрать `'use_cp'`/`'cp_on'` Discrete; маски (~1819-1841): убрать блоки `cp_on`/`use_cp`.
  - `core/models/utils.py` `convertToDict`: инференс `len_model` пересчитать (теперь base=2 вместо 4): `(n - 2 - 2*len(STRATAGEM_PHASES)) // 3` (свериться с фактической формулой после Task — base heads теперь 2).
  - Обновить тесты, ожидавшие use_cp/cp_on в контракте/действии (`test_action_contract.py`, любые с use_cp/cp_on).

- [ ] **Step 4: PASS + регрессия**

Run: `python -m pytest tests/models/ tests/engine/phases/ -q` → PASS (обновить контракт-size тесты; AZ n_actions-векторы −2). `python -m pytest tests/engine/ -q` → baseline (AZ n_actions-тесты обновить под новый размер). `ruff check --fix`.

- [ ] **Step 5: engine-regression-reviewer + Коммит**
```
git add -A
git commit -m "refactor(contract): убрать use_cp/cp_on (head — единственный путь стратагем; контракт −2 головы)"
```

---

## Task 5: Финальная регрессия + AZ/GAZ смоук + реакции

**Files:** проверочная (контроллер). Test: весь сьют.

- [ ] **Step 1: Полная регрессия**

Run: `python -m pytest tests/engine/phases/ tests/models/ -q` → PASS.
`python -m pytest tests/engine/ -q` → зафиксировать новый baseline (контракт изменился; сверить, что новые падения — только обновлённые-под-контракт AZ n_actions, не логические).
**Реакции целы:** `python -m pytest tests/engine/phases/test_reaction_*.py tests/engine/phases/test_go_to_ground.py tests/engine/phases/test_simulate_reaction_branch_*.py -v` → PASS.

- [ ] **Step 2: AZ + GAZ self-play смоук (контроллер)**

`TRAIN_ALGO=alphazero_tree ... python train.py` (4ep) и `TRAIN_ALGO=gumbel_az ... python train.py` (3ep) → exit=0 без traceback.
DQN/PPO смоук: `TRAIN_ALGO=dqn/ppo TRAIN_EPISODES_OVERRIDE=4 python train.py` → exit=0 (контракт без use_cp загружается, головы инертны но не падают).

- [ ] **Step 3: Финальный whole-branch review (opus)** — снос большой, реакции/реролл-мех должны быть verified целыми.

- [ ] **Step 4: Коммит (если правки от ревью)** + пометить 5b-runbook к исполнению пользователем.

---

## Self-Review

**Spec coverage:**
- bravery-flip (strat_command primary, снос reaction_policy/use_cp bravery) — Task 1. ✅
- снос MC command_reroll-машинерии + phase-hooks + bridge prefilter + тесты — Task 2. ✅
- снос fight-план (apply/attach/from_choices/AZ/bridges build_fight_plan) + тесты — Task 3. ✅
- убрать use_cp/cp_on из контракта (+convertToDict) — Task 4. ✅
- реакции/реролл-мех НЕ тронуты (регрессия) — Tasks 2-5 (реакц-тесты). ✅
- AZ/GAZ смоук, новый baseline — Task 5. ✅
- 5b runbook — вне этого плана (раздел спеки; исполняет пользователь). ✅

**Placeholder scan:** removal-задачи дают СПИСКИ символов/вызовов к удалению + точные verification-команды (это и есть «код» для сноса). `convertToDict` формула помечена «свериться с фактической после base=2» — реальная сверка, не placeholder. Точные строки вызовов даны ориентирами (~NNNN) — исполнитель грепает по уникальным именам (`attach_fight_stratagem_plan`, `_apply_phase_command_reroll` и т.д.).

**Type consistency:** `strat_command`/`strat_<phase>` ключи едины с п.1–4; удаляемые имена методов согласованы между Task 2/3 и spec.

**Примечание:** baseline `tests/engine/` СМЕНИТСЯ (контракт −2 головы → AZ n_actions-тесты обновляются). Это не регрессия логики — фиксируется как новый baseline в Task 5.

---

## Execution Handoff

См. ниже выбор способа исполнения.
