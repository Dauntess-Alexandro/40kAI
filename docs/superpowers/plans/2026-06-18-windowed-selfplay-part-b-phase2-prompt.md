# Claude Code — Part B фаза 2 (осталось после B5)

> **Предусловие:** B5 закоммичен (`mcts_joint_action_from_best_child`, тесты `test_mcts_joint_action_selection.py`, parity gate Δ=0pp на 50ep).
> **Полный контекст:** `docs/superpowers/plans/2026-06-18-windowed-selfplay-part-b-claude-prompt.md`

---

## Статус Part B

| Фаза | Статус |
|------|--------|
| **B5** joint best child | ✅ сделано |
| **B6** phase obs в train/eval/GUI | ⬜ следующая |
| **B1a** Insane Bravery → policy | ⬜ |
| **B1b** Hungry Void / Command Re-roll | ⬜ |
| **B1c** usage_limit enforce | ⬜ |
| **B1d** Dynasty стратагемы (Wahapedia, по одной) | ⬜ |
| **B4** mcts_window_nodes | ⬜ |
| **B3** reaction windows | ⬜ |
| **B2** per-unit shoot/charge | ⬜ отложено |

---

## Стартовая команда (скопируй в Claude Code)

```text
Прочитай AGENTS.md, CLAUDE.md и docs/superpowers/plans/2026-06-18-windowed-selfplay-part-b-phase2-prompt.md.

Контекст: B5 (mcts_joint_action_from_best_child) уже в main/worktree2. alphazero_tree: joint=1, windowed=1, candidate_mode=option.

СЕЙЧАС — Фаза B6, затем B1a:

### B6 — phase_obs_features в обучении
1. hyperparams `phase_obs_features: 0/1` + env `PHASE_OBS_FEATURES` в train/eval/GUI (код в obs_features.py уже есть).
2. Версионирование obs/checkpoint: флаг 0 = старый размер; флаг 1 = +24 dims — понятная ошибка при mismatch.
3. `[AZ][CONFIG] phase_obs_features=0/1` в лог train.
4. Тесты: размер obs, детерминизм, бит insane_bravery available при shock-сценарии.
5. Smoke train 10 ep с phase_obs_features=1.
Дефолт hyperparams оставить 0 до отдельного «Все ок».

### B1a — Insane Bravery end-to-end (первая стратагема)
Wahapedia 10ed: Command phase, Battle Shock fail → 1 CP → auto pass.
- Research-коммент в stratagems.py (URL Wahapedia, не выдумывать правила).
- Убедиться: command window + option_candidates + fight_plan не ломают parity.
- Метрика eval: cp_used > 0 на сценариях с battle shock (синтетический тест + eval trace).
- Одна стратагема = один PR-логический кусок. Не добавлять другие стратагемы в этом заходе.

Гейты перед «готово»:
- pytest tests/engine/phases/ tests/models/test_mcts_joint_action_selection.py
- test_windowed_legacy_parity.py зелёный
- tools/windowed_parity_winrate.py --episodes 50 --seed 1000 (Δ < 5pp)
- Eval 20 игр: сравнить stay_rate_when_move_options и turn_limit с baseline (до B5: stay=1.0, eval win 60% на 10 ep)

Обнови журнал в part-b-phase2-prompt.md. Коммит только после «Все ок».
```

---

## B6 — детали

**Файлы:** `core/engine/phases/obs_features.py`, `train.py`, `eval.py`, `hyperparams.json`, `app/gui_qt/az_hyperparams_defaults.py`, `app/gui_qt/main.py`, тесты `tests/engine/phases/test_obs_features*.py` (создать при отсутствии).

**Не делать:** менять action space; включать phase_obs=1 дефолтом без smoke.

---

## B1 — стратагемы (Wahapedia, по одной)

**Источник:** https://wahapedia.ru/wh40k10ed/ — CP, Stratagems, фракция Necrons.

**Очередь волны 0 (уже в REGISTRY, довести до policy):**
1. `insane_bravery` — command, use_cp/cp_on
2. `hungry_void` — fight window + fight_plan в MCTS
3. `command_reroll` — fight, документировать approx vs Wahapedia

**Реакции** (`overwatch`, `go_to_ground`, …) — только в **B3**, не смешивать с B1a.

**Шаблон одной стратагемы:**
- StratagemDef docstring + Wahapedia URL
- `stratagem_engine` effect
- `legal_stratagem_options` + `usage_limit` enforced
- `tests/engine/phases/test_stratagem_<id>.py`
- option_candidates / replay_meta при необходимости

---

## B4 — mcts_window_nodes (после B6 + B1a зелёные)

- Только при `mcts_candidate_mode=option`, дефолт `mcts_window_nodes=0`.
- Тесты snapshot/restore per-window.
- A/B winrate vs baseline.

---

## B3 — reaction windows (после B1 main-phase)

- `WINDOWED_REACTION_WINDOWS=1`, `reaction_windows.py`.
- Overwatch / Go to Ground / Smokescreen / Heroic Intervention — по одной с Wahapedia.

---

## B2 — per-unit shoot/charge (отложено)

Требует `superpowers:brainstorming` — меняет `action_contract`, все алго, чекпойнты.

---

## Stage 8.5 — GAZ (после Part B на AZ Tree)

GAZ не использует `option_candidates` напрямую — портировать идею окон/стратагем в `GumbelAlphaZeroSearch` (см. roadmap 8.5). Не начинать до зелёного B1 на AZ.

---

## Журнал фазы 2

| Задача | Статус | Примечание |
|--------|--------|------------|
| B6 phase obs | ✅ | Флаг `phase_obs_features` (hyperparams alphazero_tree + env `PHASE_OBS_FEATURES`) прокинут в train/eval/GUI; дефолт 0. `[AZ][CONFIG] phase_obs_features=` в train-логе; `[EVAL][AZ][CONFIG]` в eval. Resume-гард: понятная RU-ошибка при mismatch размера obs (`describe_obs_dim_mismatch`). Тесты: `test_obs_features_config.py` (resolve/mismatch/insane_bravery bit). Smoke 10ep phase_obs=1: obs 17→41 (+24), без crash. Parity Δ=4pp (legacy .18 / windowed .14). |
| B1a Insane Bravery | ✅ | Уже end-to-end через `command_window`→`run_command`→`command_phase(decide_bravery)`→`_apply_stratagem` (1 CP, снятие battle-shock, журнал `stratagem_used`). Добавлен research-коммент с Wahapedia URL в `stratagems.py`. Тест `test_stratagem_insane_bravery.py` (4): опция в окне, расход 1 CP + auto-pass, PASS оставляет shock, блок без CP. eval-метрика `cp_used` уже считает `use_cp>0`. |
| B1b Hungry Void / Cmd Reroll | ✅ | Код+тесты уже были зелёные (fight-окно→fight_plan→MCTS→stratagem_engine, effect/snapshot/restore). Добавлены research-комменты с Wahapedia URL: hungry_void = «Protocol of the Hungry Void» (Necrons Awakened Dynasty Battle Tactic, 1CP, fight): моделируем только +1 Strength; AP+1 при CHARACTER-лидере и таргет «не выбран драться» НЕ моделируются. command_reroll = Core Stratagem (1CP, ре-ролл одного броска), в песочнице упрощено до ре-ролла всех wound-бросков юнита в fight. Тесты `test_hungry_void`/`test_command_reroll`/`test_windowed_selfplay_fight` зелёные; phases+joint 149 passed; parity-unit зелёный. |
| B1c usage_limit | ✅ | `usage_limit_reached()` в stratagems.py: PER_PHASE=(round,phase), PER_TURN=(round), PER_BATTLE=вся партия, UNLIMITED=без лимита. Два слоя: hard-guard в `stratagem_engine.apply` (reason="usage_limit", CP не списан) + фильтр в `legal_stratagem_options` (исчерпанные не предлагаются как опция → policy/obs не видят их). Тесты `test_usage_limit.py` (6): PER_BATTLE/PER_PHASE/per-side/UNLIMITED + drop из legal_options. phases+joint 155 passed. |
| Eval gate B5 (20 ep, stay/turn_limit) | ⬜ | пользователь / агент |
| B4 window nodes | ✅ | Уже реализовано (Stage 8.4f): `windowed_mcts.root_joint_candidates_window_nodes`, гейт `MCTSConfig.window_nodes` только при candidate_mode∈{option,option_plus}, дефолт 0. Проброс в train (self-play+checkpoint payload+лог `[MCTS][WINDOW_NODES]`) и eval (`AZ_EVAL_MCTS_WINDOW_NODES`). Тесты `test_mcts_window_nodes.py` (4): default-off, active-window-index, changes-root-candidates, mcts-runs. A/B winrate — прогон пользователя. Парити B1c: legacy .16 / windowed .16, Δ=0pp. |
| B3 reactions | 🟡 | Слой reaction-окон + research-комменты — готовы (см. ниже B3-full). |
| **B3-full** reaction value-policy | 🟡 в работе | Спека `specs/2026-06-19-b3-reaction-value-policy-design.md`, план `plans/2026-06-19-b3-reaction-value-policy.md`. **Готово (8 коммитов):** флаг `reaction_value_policy` (дефолт 0); `reaction_value_policy.py` (net-value apply/pass); harness `_simulate_reaction_branch` + recursion guard + seam `resolve_trigger`; decision-пламбинг всех 4 реакций (go_to_ground/smokescreen/overwatch/heroic) с тестами; **Task 8a** — install в AZ-актора (прямой az_net) + главный shooting call-site (model→enemy) trigger; smoke flag=1 `[AZ][ACTOR] reaction_value_policy=ON` без краша; 162 phases + 5 policy + 2 harness тестов зелёные. **Остаётся (Task 8b):** прочие shooting-сайты, overwatch×6, heroic call-site triggers; eval-install; 50ep parity-гейт. Дефолт 0 → parity не затронут (closure строится только при активной reaction_policy). |
