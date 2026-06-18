# Stage 8.4 — Windowed rollout + MCTS (полный план для Claude Code)

> **Для агента:** REQUIRED SUB-SKILL: `superpowers:test-driven-development` на каждый под-этап; перед коммитом — `engine-regression-reviewer` + `verification-before-completion`. Язык логов/ошибок/UI — **русский**. Платформа — **Windows**, Python **3.12+**, тесты: `python -m pytest` из корня.

**Цель 8.4:** расширить windowed self-play (сейчас только **command**, Stage 8.3) на **movement / shooting / charge / fight** и подключить тот же путь к **MCTS rollout'ам** (tree AlphaZero). Корневые кандидаты уже строятся в режиме `mcts_candidate_mode=option` (Stage 4); 8.4 замыкает **исполнение** и **симуляцию** через `PhaseEngine`, а не только корень.

**Статус на входе (2026-06-18):**
- ✅ 8.1 `PHASE_OBS_FEATURES` (+24 dims, флаг, дефолт 0)
- ✅ 8.2 `ReplayPhaseMeta`, `REPLAY_PHASE_META=1`
- ✅ 8.3 `WINDOWED_SELFPLAY` + command через `run_model_command_from_action` (`core/engine/phases/windowed_selfplay.py`)
- ✅ Stage 4 `option_candidates.py`, fight windows, `mcts_candidate_mode=option` (дефолт в hyperparams/GUI/train)
- ✅ `windowed_selfplay: 1` в hyperparams (дефолт), env `WINDOWED_SELFPLAY`, GUI, dist SMB
- ✅ 8.4f `MCTS_WINDOW_NODES` — корень perturb одного окна (дефолт 0)
- ✅ 8.4g `WINDOWED_REACTION_WINDOWS` — reaction DecisionWindow API (дефолт 0, не в generate_windows)

**Дефолты после 8.3+hyperparams:** `mcts_candidate_mode=option`, `windowed_selfplay=1`. Legacy-путь: `windowed_selfplay=0`.

---

## Global Constraints

- **Не ломать golden-trace** при `WINDOWED_SELFPLAY=0` — поведение 1:1 с текущим `env.step`.
- **Инвариант snapshot/restore** в MCTS: после каждого rollout-шага состояние восстанавливается; расширить покрытие на `active_stratagem_effects`, pending fight plan, phase journal.
- **Движок не импортирует models** — вся логика окон в `core/engine/phases/`, мост в `core/models/` только читает/вызывает engine.
- **Фиче-флаги:** `WINDOWED_SELFPLAY` (self-play + env.step), опционально `WINDOWED_MCTS_ROLLOUT=0/1` (только MCTS внутренние шаги — если понадобится разделить риск; иначе один флаг).
- **Не редактировать** `runtime/logs/LOGS_FOR_AGENTS_*.md` (guard_paths).
- ruff: `ruff.toml`, line-length 120.

---

## Архитектура (целевая)

```mermaid
flowchart TB
  subgraph policy [Политика / MCTS]
    AD[action_dict от сети]
    RC[root_joint_candidates option mode]
    MCTS[MCTS simulate]
  end
  subgraph bridge [windowed_selfplay.py]
    MAP[action_dict → decide(window)]
    RUN[run_model_*_from_action]
  end
  subgraph engine [PhaseEngine]
    CW[run_command]
    MV[run_movement]
    SH[run_shooting]
    CH[run_charge]
    FG[run_fight]
  end
  subgraph env [warhamEnv]
    LEG[legacy phase_* при flag=0]
    STEP[step router]
  end
  AD --> MAP
  RC --> MCTS
  MCTS --> STEP
  STEP -->|WINDOWED=1| RUN
  RUN --> CW & MV & SH & CH & FG
  STEP -->|WINDOWED=0| LEG
  MAP --> RUN
```

**Ключевая идея:** политика по-прежнему выдаёт **плоский** `action_dict` (6 голов + `move_num_i`). Мост `make_*_decide_from_action_dict` проецирует dict на **текущее** `DecisionWindow`, `PhaseEngine.run_*` исполняет без дублирования правил.

---

## Файлы (карта)

| Зона | Файлы |
|------|--------|
| Окна/исполнение | `core/engine/phases/phase_engine.py`, `option_generator.py`, `legacy_compiler.py` |
| Windowed мост | `core/engine/phases/windowed_selfplay.py` (**расширить**) |
| Env router | `core/envs/warhamEnv.py` (`step`, phase hooks) |
| MCTS | `core/models/alphazero_mcts.py`, `option_candidates.py` |
| Self-play | `core/models/alphazero_selfplay.py`, `gumbel_muzero_selfplay.py` |
| Replay meta | `core/engine/phases/replay_meta.py` |
| Конфиг | `hyperparams.json`, `train.py`, `app/gui_qt/*` |
| Harness | `tools/mcts_winrate_baseline.py`, `tests/engine/phases/*` |

---

## Под-этапы (порядок обязателен)

### 8.4a — Movement windowed (низкий риск, шаблон для остальных)

**Files:**
- Modify: `core/engine/phases/windowed_selfplay.py`
- Modify: `core/envs/warhamEnv.py` (movement branch в `step`)
- Test: `tests/engine/phases/test_windowed_selfplay_movement.py`

**Interfaces:**
- `make_movement_decide_from_action_dict(action_dict, unit_idx) -> Callable[[DecisionWindow], ActionOption]`
  - Читает `move_num_{i}` из dict (как `_pick_destination_by_reachable_index`).
  - Маппит индекс reachable → `ActionOption` в текущем `movement_options_for_unit` окне.
  - Fallback: STAY / первая легальная опция.
- `run_model_movement_from_action(env, action_dict) -> PhaseTurnState | side-effect`
  - Делегирует `phase_engine.run_movement` с decide, построенным из dict.
  - Сохраняет контракт reward/done/info как `movement_phase`.

**warhamEnv.step:** при `WINDOWED_SELFPLAY=1` и фазе movement — вызвать `run_model_movement_from_action` вместо inline `movement_phase`.

**Тесты (TDD):**
1. Snapshot env в movement, один unit — windowed vs legacy `action_dict` → те же позиции/health/reward (допуск float).
2. `windowed_selfplay_enabled()=False` → старый путь без импорта engine в step (mock/spy).
3. Replay meta: `window_id` содержит `movement:` при windowed=1.

**Checkpoint:** `pytest tests/engine/phases/test_windowed_selfplay*.py` green; golden-trace movement slice без регрессий.

---

### 8.4b — Shooting + Charge windowed

**Files:**
- Modify: `windowed_selfplay.py`, `warhamEnv.py`
- Test: `tests/engine/phases/test_windowed_selfplay_shoot_charge.py`

**Shooting:**
- `make_shooting_decide_from_action_dict` — `shoot` head → локальный ранг цели в `shooting_options_for_unit`.
- `run_model_shooting_from_action` → `phase_engine.run_shooting`.

**Charge:**
- `make_charge_decide_from_action_dict` — `charge` + `attack==1` → `charge_options_for_unit`.
- `run_model_charge_from_action` → `phase_engine.run_charge`.

**Особенности контракта (из roadmap / warhamEnv):**
- `shoot` — локальный индекс в valid targets юнита.
- `charge` — глобальный индекс врага; нужен `attack==1`.

**Тесты:** паритет legacy vs windowed на фиксированных сидах (2–3 сценария на фазу); meta `window_id` shoot/charge.

---

### 8.4c — Fight windowed + стратагемы

**Files:**
- Modify: `windowed_selfplay.py`, `warhamEnv.py`, возможно `option_generator.py`
- Test: `tests/engine/phases/test_windowed_selfplay_fight.py`

**Цель:** fight через `phase_engine.run_fight` + окна из `fight_stratagem_options_for_unit` (Hungry Void, Command Re-roll).

**Конфликт с Stage 4:** сейчас `_pending_fight_stratagem_plan` в `warhamEnv.fight_phase` при `option` MCTS. В windowed пути:
- **Предпочтение:** стратагемы fight выбираются через `decide(window)` → `run_fight`, а не через pending plan.
- Убрать дублирование: если `WINDOWED_SELFPLAY=1`, не применять `_apply_pending_fight_stratagem_plan` для тех же решений (guard по флагу).

**Interfaces:**
- `make_fight_decide_from_action_dict` — маппинг fight heads + stratagem options (если в dict нет явной стратагемы — PASS).
- `run_model_fight_from_action` → `phase_engine.run_fight`.
- `fight_replay_meta_from_action` + `merge_fight_meta_into` (аналог command).

**Тесты:** fight без стратагемы; fight + Hungry Void при легальности; CP не течёт в snapshot restore.

---

### 8.4d — Единый step-router + replay meta всех фаз

**Files:**
- Modify: `windowed_selfplay.py` — `run_model_phase_from_action(env, action_dict)` диспетчер по `env.phase`.
- Modify: `alphazero_selfplay.py`, `gumbel_muzero_selfplay.py` — `merge_*_meta_into` для всех фаз (не только command).
- Modify: `replay_meta.py` при необходимости (phase-specific helpers).

**warhamEnv.step:** один вызов `run_model_phase_from_action` при windowed=1 для model-side фаз (command уже есть — рефактор в общий диспетчер).

**Тесты:** smoke 10 эпизодов `play_episode_with_mcts` (как в сессии): 0 errors, meta заполнена по фазам.

---

### 8.4e — MCTS rollout через windowed step

**Files:**
- Modify: `core/models/alphazero_mcts.py` — в simulate/expand после `env.step` убедиться, что rollout использует windowed path (env наследует `WINDOWED_SELFPLAY` из train/GUI).
- Modify: `option_candidates.py` — при simulate внутри MCTS те же кандидаты option mode + windowed execution.
- Test: `tests/models/test_mcts_windowed_rollout.py`

**Задачи:**
1. В `_simulate` / `_step_env` MCTS: не обходить windowed router (сейчас `env.step` уже роутит — **проверить** все ветки: enemy turn, restore).
2. Snapshot restore после windowed step: добавить поля fight plan / stratagem journal если мутируются.
3. Счётчики в лог train: `windowed_selfplay=1` уже есть; добавить маркер `[MCTS][WINDOWED]` при первом windowed rollout (опционально).

**Тесты:**
- MCTS 8 sims, 1 ход: snapshot до/после restore идентичен.
- `mcts_candidate_mode=option` + `WINDOWED=1`: root candidates ⊆ legal options; simulate не падает.

**Harness:** прогнать `python tools/mcts_winrate_baseline.py` (100 ep × seeds) — winrate/draws не хуже baseline ± noise; зафиксировать в `artifacts/results/` или комментарий в PR.

---

### 8.4f — (Опционально, отдельный флаг) MCTS узлы = decision windows

**Не блокирует 8.4a–e.** Высокий риск, делать только после winrate harness.

**Что:** вместо одного узла MCTS = весь ход model, узел = одно `DecisionWindow` (command → move unit 0 → …).

**Files:** `alphazero_mcts.py`, новый `core/models/windowed_mcts.py` (если раздувается).

**Митигейт:** `MCTS_WINDOW_NODES=0/1`, дефолт 0; depth budget per turn; батч leaf-eval.

---

### 8.4g — Reactions как отдельные окна
u
**Что:** Overwatch и др. через `generate_windows` timing=REACTION, не в плоском ходу.

**Зависит от:** reaction_policy в engine, opt-in в self-play.

**Флаг:** можно отложить на 8.5; в плане заложить тест-заглушку `test_reaction_windows_skipped_by_default`.

---

## Конфигурация (уже сделано / проверить в 8.4)

| Ключ | Где | Дефолт |
|------|-----|--------|
| `windowed_selfplay` | `hyperparams.json` alphazero_tree/proxy | `1` |
| `WINDOWED_SELFPLAY` | env, train.py, GUI main.py | из hyperparams |
| `mcts_candidate_mode` | hyperparams | `option` |
| `MCTS_CANDIDATE_MODE` | env | `option` |
| SMB dist | `AZ_DIST_HYPERPARAM_KEYS` + `apply_az_dist_worker_env` | sync PC1↔PC2 |

При добавлении `WINDOWED_MCTS_ROLLOUT` — зеркально в hyperparams + GUI (группа MCTS).

---

## Verification checklist (перед «готово»)

- [ ] `python -m pytest tests/engine/phases/ tests/models/test_option_candidates.py tests/models/test_mcts_candidate_modes.py` — green
- [ ] Smoke: 10 ep `play_episode_with_mcts`, `WINDOWED=1`, `REPLAY_PHASE_META=1` — 0 exceptions
- [ ] `WINDOWED=0` — тесты паритета с legacy (movement/shoot/charge/fight/command)
- [ ] `tools/mcts_winrate_baseline.py` — не регрессия > ~5% winrate на фикс. seeds (документировать цифры)
- [ ] Лог train: строка с `windowed_selfplay=1 candidate_mode=option`
- [ ] `engine-regression-reviewer` на дифф `core/engine/`, `warhamEnv.py`
- [ ] Не коммитить runtime-логи / pc2 secrets

---

## Порядок коммитов (рекомендация)

1. `8.4a movement windowed`
2. `8.4b shoot/charge`
3. `8.4c fight + stratagem dedup`
4. `8.4d step router + replay meta`
5. `8.4e MCTS rollout + snapshot`
6. (опц.) `8.4f window nodes`, `8.4g reactions`

Каждый коммит — отдельный pytest scope + краткая строка в results.

---

## Промпт для вставки в Claude Code (копипаст)

```
Реализуй Stage 8.4 по плану plans/2026-06-18-stage8-4-windowed-mcts-rollout.md.

Контекст: 8.3 уже роутит command через PhaseEngine при WINDOWED_SELFPLAY=1.
Дефолты: mcts_candidate_mode=option, windowed_selfplay=1 в hyperparams.

Начни с 8.4a (movement): TDD, затем 8.4b–e по порядку. Не трогай 8.4f/8.4g без явного запроса.

Обязательно:
- superpowers:test-driven-development на каждый под-этап
- паритет legacy (WINDOWED=0) и windowed (WINDOWED=1) в тестах
- расширить windowed_selfplay.py, не дублировать логику фаз вне PhaseEngine
- fight: согласовать с option_candidates / _pending_fight_stratagem_plan
- MCTS: env.step уже windowed — проверить snapshot/restore в simulate
- русские логи/ошибки; ruff; AGENTS.md
- verification-before-completion + engine-regression-reviewer перед финальным отчётом

Не коммить без «Все ок» от пользователя.
```

---

## Связь с roadmap

- Roadmap §8.4 («кандидаты из generate_windows») — **частично сделано** в Stage 4 (`option` mode).
- Этот план закрывает **исполнение** и **rollout** (roadmap §8.3 расширение + MCTS).
- Stage **8.5** — GAZ/GMZ/SMZ/PPO/DQN на тот же windowed router.

---

## Риски

| Риск | Митигация |
|------|-----------|
| Сдвиг обучения | winrate-baseline, флаг 0 |
| Дубли fight stratagem plan vs run_fight | единый путь при WINDOWED=1 |
| Производительность | больше вызовов engine; профилировать movement loop |
| Dist PC2 рассинхрон | `apply_az_dist_worker_env`, SMB keys |
| Старые чекпойнты | obs size не меняется в 8.4 |

---

## Следующий шаг после 8.4e

Stage **8.5**: `gumbel_muzero_selfplay` + distributed actors — тот же `windowed_selfplay` hyperparam; затем опционально **8.4f** (узлы=окна).
