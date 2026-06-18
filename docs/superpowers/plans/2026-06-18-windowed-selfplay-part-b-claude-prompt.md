# Claude Code — промпт: Windowed Self-Play Part B (полный план)

> **Скопируй этот файл целиком в Claude Code** как стартовую задачу.  
> **Предусловие:** Part A parity-fix **закоммичен и зелёный** (`test_windowed_legacy_parity.py`, `tools/windowed_parity_winrate.py`, `base_action` в PhaseEngine).  
> **Источник Part A:** `docs/superpowers/plans/2026-06-18-windowed-selfplay-parity-fix.md` (журнал ✅).

---

## Миссия

Закрыть **Part B** roadmap Stage 8: агент **осмысленно** выбирает действия (не «factorized Frankenstein»), **видит CP/стратагемы**, **тратит CP** по правилам **Warhammer 40k 10th ed** (источник — **Wahapedia**), и **постепенно** получает новые стратагемы **по одной**, а не «всё сразу».

Part A ответил: *«windowed и legacy исполняют один `action_dict` одинаково»*.  
Part B отвечает: *«какой `action_dict` выбирать и как учиться играть агрессивнее»*.

---

## Эмпирический baseline (после Part A, не переписывать)

Прогон пользователя **2026-06-18**, `windowed_selfplay=1`, `candidate_mode=option`, `mcts_window_nodes=0`, train 200 ep + eval 10:

| Метрика | Train 200 ep | Eval 10 games |
|---------|--------------|---------------|
| Win rate | **27%** | **60%** (6/10) |
| turn_limit | **68%** | 40% (4/10) |
| wipeout_enemy | 27% | 60% |
| wipeout_model | 5% | **0%** |
| Пассивность eval | — | `stay@move_opts=1.0`, `charge0@opts=0.875` |

**Вывод:** parity ок, но модель **стоит** (`move=4`), много ничьих по лимиту в train. Part B должен **снизить stay/turn_limit** и **поднять осмысленное использование CP**, не ломая parity.

Логи: `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md`, `LOGS_FOR_AGENTS_EVAL.md` (читать свежий хвост; **не править руками**).

---

## Global Constraints (жёстко)

1. **AGENTS.md + CLAUDE.md** — русский в UI/логах/ошибках; отладка **сначала логи**; GUI — Qt; коммит только после «Все ок».
2. **Windows**, Python **3.12+**, тесты: `python -m pytest` из корня; ruff по `ruff.toml`.
3. **Не ломать golden-trace** при `WINDOWED_SELFPLAY=0`.
4. **Движок (`core/engine/`) не импортирует `core/models/`**.
5. **Не редактировать** `runtime/logs/LOGS_FOR_AGENTS_*.md`, `runtime/state/*remote_is*`.
6. **Минимальный scope** на задачу: один PR-логический кусок → тест → verify → журнал в этом файле.
7. **Скиллы (обязательно):**
   - `superpowers:brainstorming` — **перед** любым изменением action space / obs size / MCTS child selection.
   - `superpowers:test-driven-development` — тест до кода на движке и MCTS.
   - `superpowers:verification-before-completion` — никаких «должно работать».
   - `engine-regression-reviewer` — перед коммитом правок движка/MCTS.
   - `logs-triage` — при странном winrate/пассивности.

---

## Карта кода (откуда стартовать)

| Зона | Файлы | Статус |
|------|-------|--------|
| Реестр стратагем | `core/engine/phases/stratagems.py` | 7 defs; `usage_limit` **не enforced** |
| Применение эффектов | `core/engine/phases/stratagem_engine.py` | Insane Bravery, Hungry Void, Command Re-roll (approx), cover |
| Окна / PhaseEngine | `core/engine/phases/phase_engine.py`, `option_generator.py` | command + fight stratagem windows |
| Windowed мост | `core/engine/phases/windowed_selfplay.py` | Part A: `base_action` |
| Obs CP/стратагем | `core/engine/phases/obs_features.py` | `PHASE_OBS_FEATURES=1` (+24 dims), **дефолт выкл** |
| Replay meta | `core/engine/phases/replay_meta.py` | `REPLAY_PHASE_META=1` |
| MCTS joint/option | `core/models/option_candidates.py`, `alphazero_mcts.py` | `_final_policy_from_visits` — **независимый sample по головам** |
| Action contract | `core/models/action_contract.py` | `move, attack, shoot, charge, use_cp, cp_on, move_num_*` |
| Self-play | `core/models/alphazero_selfplay.py` | windowed router |
| Roadmap | `docs/superpowers/specs/2026-06-17-stage8-roadmap.md` | 8.1–8.6 |
| Attack effects (Dynasty) | `docs/superpowers/specs/2026-06-17-track1-attack-effects-design.md` | reroll hits, +S, AP |

---

## Part B — шесть столпов (scope)

| ID | Название | Риск | Зависимости |
|----|----------|------|-------------|
| **B5** | Joint action из best MCTS child | средний | option mode, Part A |
| **B6** | Obs CP/стратагем в train/eval | низкий | `obs_features.py` готов |
| **B1** | Стратагемы как решения политики (Wahapedia, по одной) | средний→высокий | B5 желателен; B6 для обучения |
| **B4** | `mcts_window_nodes=1` (узел = окно) | высокий | B5 + winrate harness |
| **B3** | Reaction windows в self-play (Overwatch…) | высокий | B1 частично; 8.4g API |
| **B2** | Per-unit `shoot_u` / `charge_u` головы | **очень высокий** | отдельный brainstorming; **последний** |

**Рекомендованный порядок исполнения:** `B5 → B6 → B1 (волнами) → B4 → B3 → B2`.

---

## Wahapedia — правила стратагем (обязательная политика)

### Источник истины

- База: **https://wahapedia.ru/wh40k10ed/**
- Общие правила CP/стратагем: разделы *Command Points*, *Stratagems*, *Using Stratagems*.
- Фракция (Necrons / Awakened Dynasty): страницы фракции и datasheet-стратагем на Wahapedia.
- **Не выдумывать** механику: если в движке упрощение — явно документировать в `StratagemDef` + тест «approx».

### Как внедрять (НЕ целым скопом)

Каждая новая/доработанная стратагема — **отдельная подзадача** с чеклистом:

1. **Research (Wahapedia):** выписка в комментарии к `StratagemDef`: CP cost, timing (main/reaction), when (trigger), target, effect, limits (once per phase/battle…).
2. **Engine:** `effect_id` + реализация в `stratagem_engine.py` / `attack()` effects (см. track1 design).
3. **Legal options:** `legal_stratagem_options()` — фаза, триггер, CP, keywords, **enforced `usage_limit`** (Stage 6 debt — закрывать по мере добавления).
4. **Legacy patch / window:** если выражается в `use_cp/cp_on` — только command; иначе `ActionOption` + `PhaseEngine`.
5. **MCTS:** кандидат в `option_candidates.build_turn_plan_candidates` / fight plan map.
6. **Obs:** флаг доступности уже в `obs_features` (REGISTRY-driven).
7. **Тесты:** `tests/engine/phases/test_stratagem_*.py` — минимум legal/illegal + эффект на бой.
8. **Eval метрика:** `cp_used > 0` на сценариях, где стратагема очевидна.

### Очередь стратагем (волны)

**Волна 0 — уже в REGISTRY, довести до policy (не добавлять новые):**

| id | Wahapedia / правило | Статус движка | Цель Part B |
|----|---------------------|---------------|-------------|
| `insane_bravery` | Core stratagem, auto-pass Battle Shock | legacy `use_cp/cp_on` | агент **выбирает** в command window |
| `hungry_void` | Fight, +S / AP (Dynasty) | fight window | кандидат MCTS + replay meta |
| `command_reroll` | Re-roll one dice (упрощено до fight wounds) | approx | документировать approx; тест |
| `go_to_ground` | Infantry, benefit of cover | reaction | **позже** (B3) |
| `smokescreen` | Smoke keyword | reaction | **позже** (B3) |
| `overwatch` | Fire Overwatch | reaction | **позже** (B3) |
| `heroic_intervention` | Counter-charge | reaction | **позже** (B3) |

**Волна 1 — Awakened Dynasty (по одной с Wahapedia):**

Добавлять **только после** зелёной волны 0. Кандидаты из roadmap / track1 (примерный порядок — уточнить по Wahapedia Necrons 10ed):

- `conquering_tyrant` (re-roll hits) — если ещё нет в REGISTRY, добавить **одной** задачей.
- `the_solar_divider` / другие dynasty — **только** когда предыдущая зелёная.

**Запрещено в одном PR:** «добавить 5 стратагем + сменить action space + включить reactions».

---

## Фаза 1 — B5: Joint action из best child (приоритет #1)

### Проблема

`alphazero_mcts.py` → `_final_policy_from_visits` (≈489–534): **каждая голова** сэмплируется **независимо** из маргинальных visits. Исполняемый `action_dict` может **не соответствовать ни одному** child MCTS → `move=stay` + `shoot=1` + несогласованные `move_num`.

Part A это **не чинит** (оба пути исполняют тот же dict). Для **обучения и eval** нужна **когерентность**.

### Целевое поведение

В режиме `mcts_candidate_mode=option` (и опционально `filter`):

1. После search: `best_child = argmax_visit_count(root)` (или PUCT-consistent).
2. **Исполнение:** `action_dict = best_child.action_dict` (или `action_dict_from_joint_tuple(best_child.action_tuple)`).
3. **Policy targets для IL:** оставить **маргинальные** `policy_targets` из visits (как сейчас) **или** projected на опции — **зафиксировать в brainstorming**; не ломать loss без A/B.
4. **Fight stratagem plan:** брать из `OptionCandidateSet.fight_plan_for(joint_tuple)` согласованно с best child.

### Файлы

- Modify: `core/models/alphazero_mcts.py` (`_final_policy_from_visits`, `_run_tree` return path)
- Modify: `core/models/alphazero_selfplay.py` (если дублирует сбор action)
- Create: `tests/models/test_mcts_joint_action_selection.py`

### Тесты (TDD)

- Synthetic root: 3 children с разными tuples; independent heads дают несовместимый dict; **новый путь** возвращает dict **ровно** best child.
- Legal mask: best child illegal → fallback на второй по visits (явный лог `[AZ][MCTS][JOINT_FALLBACK]`).
- Regression: `mcts_candidate_mode=joint` — поведение **без изменений**.

### Verification gate

- `python -m pytest tests/models/test_mcts_joint_action_selection.py -q`
- `tools/windowed_parity_winrate.py --episodes 50 --seed 1000` — Δ winrate windowed 0 vs 1 **< 5pp** (parity не регрессирует).
- Eval 20 games: `stay_rate_when_move_options` **должен снизиться** vs baseline 1.0 (хотя бы < 0.95 как промежуточный gate).

### Hyperparams

- Новый флаг (предложение): `mcts_joint_action_from_best_child: 1` в `alphazero_tree` + env `AZ_MCTS_JOINT_BEST_CHILD=1`, **дефолт 0** до зелёных тестов; после verify — дефолт 1.

---

## Фаза 2 — B6: Включить obs CP/стратагем в обучении

### Что уже есть

`core/engine/phases/obs_features.py`: `PHASE_OBS_FEATURES=1` добавляет **24** измерения (phase one-hot, timing, CP norm, stratagem available/used flags по `REGISTRY`).

### Задачи

1. Прокинуть флаг в **train/eval/GUI/hyperparams** (`phase_obs_features: 0/1`), не только env.
2. `build_env_contract_from_spaces` / checkpoint load: **версионирование** obs — старые чекпойнты с флагом 0; с флагом 1 — re-init head или strict mismatch error с понятным сообщением.
3. Тесты: размер obs 0 vs 1; детерминизм; при `insane_bravery` legal — соответствующий бит available=1.

### Verification gate

- Train smoke 10 ep с `phase_obs_features=1` — без crash; `[AZ][CONFIG]` показывает флаг.
- Старый checkpoint **не** грузится с флагом 1 без resize (ожидаемо) — документировать в логе/GUI.

**Дефолт:** оставить `0` в hyperparams до отдельного «Все ок»; для экспериментов пользователь включает в GUI.

---

## Фаза 3 — B1: Стратагемы ↔ политика (волнами, Wahapedia)

### 3a — Insane Bravery end-to-end (первая стратагема в обучении)

**Wahapedia:** Command phase, when unit fails Battle Shock test, spend 1CP → auto pass.

1. Сценарий self-play/eval: battle shock fail → command window содержит `USE_STRATAGEM insane_bravery`.
2. Политика/MCTS **может выбрать** опцию (не только `use_cp=0`).
3. Метрика: `cp_used > 0` хотя бы в **синтетическом** тесте и в **≥10%** eval эпизодов с shock-сценарием.

Файлы: `option_candidates.py`, `windowed_selfplay.py` (command), `alphazero_selfplay.py`, тесты.

### 3b — Hungry Void + Command Re-roll (fight windows)

Уже есть `fight_stratagem_options_for_unit` + `_pending_fight_stratagem_plan`.

1. Убедиться, что при `option` mode fight stratagem попадает в `fight_plans` кандидата.
2. После B5: best child включает согласованный fight plan.
3. Command Re-roll: в docstring + тест пометить **approx** vs Wahapedia (one dice any phase).

### 3c — Enforcement `usage_limit`

По одной стратагеме: journal `stratagem_used` блокирует повтор; тест per_phase / per_battle.

### 3d — Новые Dynasty стратагемы (строго по одной)

Шаблон PR «одна стратагема»:

```
feat(stratagem): <id> по Wahapedia 10ed

- StratagemDef + Wahapedia URL в docstring
- stratagem_engine effect
- legal_stratagem_options + usage_limit
- test_stratagem_<id>.py
- (если main) option_candidates + replay meta
```

---

## Фаза 4 — B4: `mcts_window_nodes=1`

**Только после** зелёных B5 + winrate harness.

- Узел MCTS = **одно DecisionWindow** (не весь ход); rollout вызывает `PhaseEngine.run_*` для одного окна.
- Дефолт остаётся `0`; включение через hyperparams + A/B.
- Тесты: snapshot/restore после каждого окна; CP не «течёт»; visits растут предсказуемо.
- Ожидание: лучше локальные решения shoot/charge/move, но **дороже** по infer — логировать `[AZ][MCTS][WINDOW]` timing.

См. `plans/2026-06-18-stage8-4-windowed-mcts-rollout.md` §8.4f.

---

## Фаза 5 — B3: Reaction windows в self-play

Реакции из REGISTRY (`overwatch`, `smokescreen`, `go_to_ground`, `heroic_intervention`) — timing `REACTION`.

1. Включить `WINDOWED_REACTION_WINDOWS=1` (сейчас stub / дефолт off).
2. `generate_windows` / `reaction_windows.py` — вставка окон **между** шагами врага.
3. **Не** смешивать с волной 0: reactions — отдельный milestone после main-phase stratagems.
4. Heuristic enemy должен триггерить реакции в тестах.

---

## Фаза 6 — B2: Per-unit shoot/charge heads (отложено)

**Требует отдельного brainstorming + плана** (меняет `ordered_action_keys`, размер сети, все алго, чекпойнты).

До завершения B5–B3 **не начинать**.

Черновик направления: `shoot_0..shoot_{n-1}`, `charge_0..` вместо single `shoot`/`charge`; миграция checkpoint через resize / fresh head.

---

## Hyperparams / GUI (сводка флагов)

| Ключ | Назначение | Дефолт (пока) |
|------|------------|---------------|
| `windowed_selfplay` | PhaseEngine path | `1` (после Part A OK) |
| `mcts_candidate_mode` | option/joint/filter | `option` |
| `mcts_window_nodes` | B4 | `0` |
| `mcts_joint_action_from_best_child` | B5 (новый) | `0` → `1` после verify |
| `phase_obs_features` | B6 | `0` |
| `windowed_reaction_windows` | B3 | `0` |
| env `PHASE_OBS_FEATURES` | зеркало B6 | `0` |
| env `REPLAY_PHASE_META` | журнал окон | `1` (если уже так в проекте) |

Обновлять: `hyperparams.json`, `app/gui_qt/az_hyperparams_defaults.py`, `train.py` env resolve.

---

## Verification checklist (каждая фаза)

- [ ] `python -m pytest tests/engine/phases/ tests/models/ -q` — релевантные подмножества зелёные
- [ ] `tests/engine/phases/test_windowed_legacy_parity.py` — **всегда** зелёный (Part A не регрессировать)
- [ ] `tools/windowed_parity_winrate.py --episodes 50 --seed 1000` — Δ < 5pp (если трогали MCTS/env)
- [ ] Train smoke 20–50 ep через Qt или CLI — `[TRAIN][SUMMARY]` без аномалий
- [ ] Eval 20+ games — `[EVAL][SUMMARY_V2]`:
  - `stay_rate_when_move_options` снижается (после B5)
  - `cp_used` / stratagem journal — растёт (после B1)
  - `turn_limit_count` не растёт относительно baseline train
- [ ] `engine-regression-reviewer` на дифф движка/MCTS
- [ ] Журнал ниже обновлён

---

## Журнал исполнения (заполнять агентом)

| Фаза | Статус | PR/коммит | Примечание |
|------|--------|-----------|------------|
| B5 joint best child | ✅ | коммит B5; `mcts_joint_action_from_best_child` (tree default `1`). Eval gate 20 ep — в phase2. Следующий промпт: `part-b-phase2-prompt.md`. |
| B6 phase obs в train | ⬜ | | |
| B1a Insane Bravery policy | ⬜ | | |
| B1b Hungry Void / Cmd Reroll | ⬜ | | |
| B1c usage_limit enforce | ⬜ | | |
| B1d Dynasty +1 stratagem | ⬜ | | по одной |
| B4 mcts_window_nodes | ⬜ | | |
| B3 reactions | ⬜ | | |
| B2 per-unit heads | ⬜ | отложено | brainstorming |

---

## Что НЕ делать

- ❌ Добавить все стратагемы Wahapedia одним PR.
- ❌ Менять `windowed_selfplay` parity bridge (`base_action`) без новых parity-тестов.
- ❌ Включить `mcts_window_nodes=1` и reactions одновременно.
- ❌ Ломать совместимость чекпойнтов без флага и сообщения в логе.
- ❌ Править `LOGS_FOR_AGENTS_*.md` вручную.
- ❌ Коммитить без «Все ок» пользователя.

---

## Стартовая команда для Claude Code (первый заход)

```text
Прочитай AGENTS.md, CLAUDE.md и docs/superpowers/plans/2026-06-18-windowed-selfplay-part-b-claude-prompt.md.

Начни Фазу 1 (B5): brainstorming → TDD tests/models/test_mcts_joint_action_selection.py →
реализация joint action from best child при mcts_candidate_mode=option →
pytest + windowed_parity_winrate → краткий отчёт по метрикам stay/turn_limit.

Стратагемы пока не добавляй; Wahapedia — только research note для Insane Bravery в комментарии.
Обнови журнал в конце part-b prompt файла.
```

---

## Ссылки

- Part A plan: `docs/superpowers/plans/2026-06-18-windowed-selfplay-parity-fix.md`
- Stage 8 roadmap: `docs/superpowers/specs/2026-06-17-stage8-roadmap.md`
- Stage 8.4 windowed: `plans/2026-06-18-stage8-4-windowed-mcts-rollout.md`
- Attack effects: `docs/superpowers/specs/2026-06-17-track1-attack-effects-design.md`
- Wahapedia 10ed: https://wahapedia.ru/wh40k10ed/
