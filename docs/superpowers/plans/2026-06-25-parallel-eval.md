# Параллельный eval + развязка метрик — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans (исполняю сам, по TDD). Шаги — checkbox (`- [ ]`).

**Goal:** Ускорить `eval.py` процессами-воркерами (env `EVAL_WORKERS` + GUI), не теряя двустороннюю таблицу стратагем; попутно развязать сбор метрик `run_episode` от verbose-trace (чтобы `EVAL_ACTION_TRACE=0` ускорял, но не обнулял таблицу).

**Architecture:** `run_episode` отдаёт единый структурный `EpisodeResult`: исход партии + `metrics: Counter` (только per-game event/action метрики) + `action_tuple_counter` + `model_applied_sids`/`opp_applied_sids` + `trace_block`/`event_log_block`. `_run_assignment` и параллельная ветка мержат результаты через общий accumulator, без парсинга строк trace. При `EVAL_WORKERS>1` родитель раздаёт игры (`seed=base+idx`) процессам-воркерам; воркеры сами строят env + агентов из `agent_id`, гоняют свои jobs и возвращают только picklable `EpisodeResult`.

**Tech Stack:** Python 3.12, pytest, stdlib `multiprocessing` (`spawn` на Windows), `collections.Counter`, `dataclasses`, torch (сети строятся в воркере). PySide6/QML для GUI.

**Spec:** `docs/superpowers/specs/2026-06-25-parallel-eval-design.md` — источник истины по цели. Этот plan уточняет недостающие implementation-контракты.

## Global Constraints

- Платформа Windows; RU-логи/сообщения/комментарии; ошибки = что + где + что делать.
- TDD: тест до кода. Частые коммиты. ruff чист (`python -m ruff check --select I ...`).
- НЕ менять: action-контракт, reward, формат `LOGS_FOR_AGENTS_*`, сквозные счётчики SUMMARY_V2 (`stratagem_*_total`, `strat_attempt_{sid}`/`strat_applied_{sid}`).
- НЕ коммитить `hyperparams.json`, `runtime/state/*` (параллельная работа пользователя), артефакты прогона.
- Метрик-ключи (источник истины — текущий парсер `eval.py:1540-1665`): `total_model_steps`, `move_opt_steps`, `stay_opt_steps`, `shoot_opt_steps`, `shoot_zero_opt_steps`, `charge_opt_steps`, `charge_zero_opt_steps`, `verdict_stay`/`verdict_skip_charge`/`verdict_default_shoot`, `step_result_total`/`step_result_model_ctrl_zero`, `stratagem_attempt_total`/`applied_total`/`miss_total`, `strat_attempt_{sid}`/`strat_applied_{sid}`, `{m_,o_}strat_attempt_{sid}`/`applied`/`miss`, `m_games_total`, `m_model_wins_total`, `o_opp_wins_total`, `{m_,o_}strat_games_used_{sid}`/`wins_used_{sid}`.
- **Ownership метрик:** `EpisodeResult.metrics` хранит только то, что реально произошло внутри одной игры (action/step/stratagem events). Серийные ключи `m_games_total`, `m_model_wins_total`, `o_opp_wins_total`, `{m_,o_}strat_games_used_{sid}`, `{m_,o_}strat_wins_used_{sid}` добавляет только общий accumulator. Так избегаем двойного счёта.
- **Action tuple:** `action_tuple_counter` не хранить в `metrics`: это `Counter[tuple[int,int,int,int]]` отдельным полем результата, потому что итоговый summary считает top1/top5 по tuple, а не по строковым метрикам.
- **Trace не источник истины:** строки `trace_block`/`event_log_block` нужны только для лога. Никакой итоговый отчёт/таблица/summary не парсит строки.
- **Trace-off performance:** при `EVAL_ACTION_TRACE=0` нельзя строить дорогие trace-only строки/JSON/`_head_masks_summary()`; метрики считаются через дешёвые структурные значения (`_head_masks_counts`, action_dict, info, stratagem journal).
- **No direct worker log writes:** код, который может выполняться в воркере, не пишет напрямую в общий eval-log через `_append_eval_log`/`log`; он возвращает строки родителю в `event_log_block`/`trace_block`. Родитель пишет блоки цельно с `[GAME idx]`.
- **Windows spawn:** все multiprocessing target/dataclass/helper, нужные worker-процессу, должны быть top-level и picklable. Не использовать lambda/inner function как target. Использовать `multiprocessing.get_context("spawn")`.
- **Import-cycle guard:** `core/models/eval_parallel.py` не импортирует `eval.py` на module import. Если нужен `run_episode`/сбор env из `eval.py`, импорт делать лениво внутри worker entry или вынести общее в отдельный helper.
- **MVP parallel scope:** `EVAL_WORKERS>1` поддерживает registry/agent-id путь (`--learner-agent-id`; opponent может быть agent-id или heuristic). Если запуск идёт только через legacy `.pickle`/checkpoint без `learner_agent_id`, ветка `workers>1` в первой версии должна явно логировать fallback to `workers=1` (что случилось + где + что сделать дальше). Legacy-parallel можно добавить отдельным планом.

## Implementation contracts

### `EpisodeResult`

Top-level dataclass (предпочтительно в `core/models/eval_parallel.py` или, если будет import-cycle, в новом `core/models/eval_result.py`):

```python
@dataclass
class EpisodeResult:
    winner: str | None
    end_reason: str
    vp_diff: int
    model_vp: int
    enemy_vp: int
    episode_len: int
    total_reward: float
    hp_diff_model_minus_enemy: float
    kill_diff_model_minus_enemy: float
    metrics: Counter[str]
    action_tuple_counter: Counter[tuple[int, int, int, int]]
    model_applied_sids: set[str]
    opp_applied_sids: set[str]
    trace_block: list[str]
    event_log_block: list[str]
```

Backcompat: если страшно менять все call-sites за один шаг, можно временно оставить tuple-return adapter, но итоговая цель — `_run_assignment` работает с `EpisodeResult`, а не с позиционным tuple.

### `EvalWorkerConfig`

Top-level dataclass/dict, строго picklable:

```python
@dataclass
class EvalWorkerConfig:
    learner_agent_id: str
    opponent_agent_id: str
    learner_side: str
    mission_name: str
    ruleset_version: str
    model_path: str
    base_seed: int
    trace_enabled: bool
    trace_style: str
    env_overrides: dict[str, str]
```

`env_overrides` должен содержать все режимы inference/search, влияющие на сбор агента: `PHASE_OBS_FEATURES`, `AZ_REACTION_VALUE_POLICY`, `AZ_EVAL_MODE`, `AZ_EVAL_OPPONENT_MODE`, `AZ_EVAL_MCTS_*`, `GMZ_*`, `SMZ_*`, `GAZ_*`, `DQN_EVAL_*`, `PPO_EVAL_*`, `HEURISTIC_MODE`, `DEPLOYMENT_MODE`, `LEARNER_SIDE`, `MISSION_NAME`, `EVAL_ACTION_TRACE`, `EVAL_TRACE_*`, `PYTHONPATH` не нужен внутри Python-процесса.

### Test harness

Добавить реальные helpers, а не ссылаться на несуществующие:

- `tests/eval/helpers_parallel.py`:
  - `ScriptedEvalAgent`: простой агент с `select_action(env, side)` и `as_policy_fn(env, side)`; возвращает легальный default/pass action с опциональной стратагемой для smoke.
  - `make_episode_result(...)`: synthetic `EpisodeResult` для unit-тестов accumulator/merge.
  - `run_smoke_episode(trace_flag="0", seed=...)`: строит `tests.engine.phases._helpers.build_env()`, запускает `run_episode` на scripted агентах, возвращает `EpisodeResult`.
  - `run_assignment_smoke(games, workers, base_seed, trace_flag)` — только если `_run_assignment_impl` вынесен top-level; иначе тестировать accumulator отдельно и делать CLI smoke отдельно.

---

### Task 0: Contracts + test harness + accumulator seam

**Цель:** до рефактора зафиксировать API результата и вынести общий accumulator, чтобы последовательная и параллельная ветки считали одинаково.

**Files:**
- Create: `core/models/eval_result.py` (или `core/models/eval_parallel.py`, если без циклов) — `EpisodeResult`.
- Modify: `eval.py` — top-level helper `_accumulate_episode_result(...)` без запуска env.
- Test: `tests/eval/helpers_parallel.py` (create), `tests/eval/test_eval_result_accumulator.py` (create).

**Interfaces:**
- Produces: `EpisodeResult`, `_accumulate_episode_result(acc, idx, result, learner_side, opponent_side, assignment_label="")`.
- Accumulator updates: wins/losses/draws, p1/p2 wins/vps, vp/hp/kill diffs, rewards, end reasons, `step_metrics`, `action_tuple_counter`, `m_games_total`, win totals, games-used/wins-used.

- [ ] **Step 1: Падающий тест — accumulator не парсит trace и сохраняет top-action**

```python
def test_accumulator_uses_structured_metrics_and_action_counter():
    result = make_episode_result(
        winner="model",
        metrics=Counter({"total_model_steps": 2, "m_strat_applied_command_reroll": 1}),
        action_tuple_counter=Counter({(4, 0, 0, 0): 2}),
        model_applied_sids={"command_reroll"},
        trace_block=["[TRACE][MODEL_ACTION_HUMAN] should_not_be_parsed"],
    )
    acc = new_assignment_accumulator()
    _accumulate_episode_result(acc, idx=1, result=result, learner_side="P1", opponent_side="P2")
    assert acc.step_metrics["total_model_steps"] == 2
    assert acc.step_metrics["m_games_total"] == 1
    assert acc.step_metrics["m_strat_games_used_command_reroll"] == 1
    assert acc.action_tuple_counter[(4, 0, 0, 0)] == 2
```

- [ ] **Step 2: FAIL.** Run: `python -m pytest tests/eval/test_eval_result_accumulator.py -q`
- [ ] **Step 3: Реализация**
  - Добавить dataclass результата.
  - Вынести accumulator в top-level. Не переносить пока весь `_run_assignment`, только чистую функцию/малый класс состояния.
  - В accumulator не читать `trace_block` вообще.
- [ ] **Step 4: PASS.**
- [ ] **Step 5: Коммит**

```bash
git add eval.py core/models/eval_result.py tests/eval/helpers_parallel.py tests/eval/test_eval_result_accumulator.py
git commit -m "eval: add structured episode result and accumulator seam"
```

---

### Task 1: `run_episode` отдаёт action-метрики структурно (не из trace)

**Цель:** `run_episode` возвращает `EpisodeResult.metrics` с action-опционными ключами, считаемыми из `action_dict` + masks прямо в цикле. `EVAL_ACTION_TRACE=0` не строит дорогие trace-only строки.

**Files:**
- Modify: `eval.py` (`run_episode` ~407-1045).
- Test: `tests/eval/test_episode_metrics_decoupled.py` (create/extend).

**Interfaces:**
- Consumes: `EpisodeResult` from Task 0.
- Produces: `run_episode(...) -> EpisodeResult`.

- [ ] **Step 1: Падающий тест — action-метрики есть при trace off**

```python
def test_metrics_present_without_trace(monkeypatch):
    monkeypatch.setenv("EVAL_ACTION_TRACE", "0")
    result = run_smoke_episode(trace_flag="0", seed=101)
    assert isinstance(result.metrics, Counter)
    assert result.metrics["total_model_steps"] >= 1
    assert result.trace_block == []
    assert result.action_tuple_counter
```

- [ ] **Step 2: Падающий тест — trace-only formatter не вызывается при trace off**

```python
def test_trace_off_does_not_call_head_masks_summary(monkeypatch):
    monkeypatch.setenv("EVAL_ACTION_TRACE", "0")
    # monkeypatch helper/spy в eval.py: если _head_masks_summary вызвали, тест падает.
```

- [ ] **Step 3: FAIL.** Run: `python -m pytest tests/eval/test_episode_metrics_decoupled.py -q`
- [ ] **Step 4: Реализация**
  - В `run_episode` завести `ep_metrics = Counter()` и `ep_action_tuple_counter = Counter()`.
  - В месте выбора `action_dict` считать: `total_model_steps`, tuple `(move, attack, shoot, charge)`, `move_opt_steps`/`stay_opt_steps`, `shoot_opt_steps`/`shoot_zero_opt_steps`, `charge_opt_steps`/`charge_zero_opt_steps`.
  - Для verdict считать `verdict_stay`, `verdict_skip_charge`, `verdict_default_shoot` структурно сразу после `_step_verdict(...)`.
  - Для step result считать `step_result_total` и `step_result_model_ctrl_zero` из `_info`, не из `[TRACE][STEP_RESULT]`.
  - Обернуть дорогие trace-only f-string/helper в `if trace_enabled:` или `if trace_enabled and trace_style == "warhammer"`.
  - Вернуть `EpisodeResult` вместо tuple (или через adapter только на переходном коммите).
- [ ] **Step 5: PASS.**
- [ ] **Step 6: Коммит**

```bash
git add eval.py tests/eval/test_episode_metrics_decoupled.py
git commit -m "eval: run_episode returns structured action metrics independent of trace"
```

---

### Task 2: `run_episode` отдаёт стратагем-метрики `m_`/`o_` + applied-sids

**Цель:** перенести подсчёт стратагем (attempt/applied/miss по сторонам + множества applied sid) из парсера trace в `run_episode`; считать по `attempt_specs` и journal diff, независимо от `emit`/trace.

**Files:**
- Modify: `eval.py` (`run_episode`: места `log_stratagem_attempts` и `log_stratagem_journal_diff`).
- Optional Modify: `core/telemetry/stratagem_trace.py` — только если нужно вынести чистые helpers без изменения формата логов.
- Test: `tests/eval/test_episode_metrics_decoupled.py` (extend).

**Interfaces:**
- Produces: `metrics` с `{m_,o_}strat_attempt/applied/miss_{sid}`, `stratagem_attempt_total/applied_total/miss_total`, `strat_attempt_{sid}`/`strat_applied_{sid}`; `model_applied_sids`, `opp_applied_sids`.

- [ ] **Step 1: Падающий тест — side counters без trace**

```python
def test_stratagem_side_counters_without_trace(monkeypatch):
    monkeypatch.setenv("EVAL_ACTION_TRACE", "0")
    result = run_smoke_episode(trace_flag="0", seed=102, force_model_stratagem=True)
    met = result.metrics
    assert "stratagem_applied_total" in met
    assert any(k.startswith("m_strat_applied_") for k in met)
    assert isinstance(result.model_applied_sids, set)
```

- [ ] **Step 2: FAIL.** Run: `python -m pytest tests/eval/test_episode_metrics_decoupled.py -q`
- [ ] **Step 3: Реализация**
  - Добавить маленькие helpers в `eval.py`:
    - `_record_stratagem_attempt_metrics(metrics, attempt_specs, env_side)`.
    - `_record_stratagem_apply_and_miss_metrics(metrics, new_records, attempt_specs, env_side_acting, model_set, opp_set)`.
  - Вызвать helpers сразу после `log_stratagem_attempts` / `log_stratagem_journal_diff` для model и enemy.
  - Не полагаться на `ep_stratagem_applied`, потому что сейчас `log_stratagem_journal_diff` обновляет его только при `emit=True`.
  - Не менять формат строк `[WH40K][STRATAGEM]`.
- [ ] **Step 4: PASS.**
- [ ] **Step 5: Коммит**

```bash
git add eval.py tests/eval/test_episode_metrics_decoupled.py
git commit -m "eval: collect stratagem metrics per side inside episode"
```

---

### Task 3: `_run_assignment` мержит структурные метрики (удалить парсинг trace)

**Цель:** заменить парсинг `trace_lines` на `accumulate(EpisodeResult)`; trace/event blocks идут только в лог. Сохранить `action_tuple_counter` и итоговый summary.

**Files:**
- Modify: `eval.py` (`_run_assignment` 1512-1665).
- Test: `tests/eval/test_eval_stratagem_table.py` (extend), `tests/eval/test_eval_result_accumulator.py`.

**Interfaces:**
- Consumes: Tasks 0–2.

- [ ] **Step 1: Тест — таблица не пуста при trace=0**

```python
def test_table_nonempty_with_trace_off(monkeypatch):
    monkeypatch.setenv("EVAL_ACTION_TRACE", "0")
    result = run_smoke_episode(trace_flag="0", seed=103, force_model_stratagem=True)
    acc = new_assignment_accumulator()
    _accumulate_episode_result(acc, idx=1, result=result, learner_side="P1", opponent_side="P2")
    assert acc.step_metrics["m_games_total"] == 1
    assert any(k.startswith("m_strat_applied_") for k in acc.step_metrics)
```

- [ ] **Step 2: FAIL/PASS по текущему состоянию.** Run: `python -m pytest tests/eval/test_eval_stratagem_table.py tests/eval/test_eval_result_accumulator.py -q`
- [ ] **Step 3: Реализация**
  - В `_run_assignment`: `result = run_episode(...)`.
  - Для `result.event_log_block` и `result.trace_block`: родитель пишет `_append_eval_log(f"[TRACE][GAME {idx}]{label} {line}")` / event prefix.
  - Удалить regex-парсеры `model_action_re`, `step_result_re`, `strat_*_re`, цикл metric parsing.
  - Все summary lists/counters обновлять через `_accumulate_episode_result`.
  - Убедиться, что итоговые `top1_action_share/top5_action_share` используют merged `action_tuple_counter`.
- [ ] **Step 4: PASS + регресс зоны.** Run: `python -m pytest tests/eval -q`
- [ ] **Step 5: Коммит**

```bash
git add eval.py tests/eval/test_eval_stratagem_table.py tests/eval/test_eval_result_accumulator.py
git commit -m "eval: assignment merges structured metrics and keeps trace log-only"
```

---

### Task 4: seed на игру (детерминизм)

**Цель:** `run_episode(..., seed=None)` засевает RNG до roll-off/deploy/reset; `_run_assignment` передаёт `seed = base_seed + idx`, чтобы агрегат не зависел от числа воркеров.

**Files:**
- Modify: `eval.py` (`run_episode` сигнатура + засев в самом начале; `_run_assignment` loop).
- Test: `tests/eval/test_eval_determinism.py` (create).

**Interfaces:**
- Produces: `run_episode(..., seed: int | None = None)`.
- Env: `EVAL_BASE_SEED` default `0`.

- [ ] **Step 1: Падающий тест — те же seed → те же структурные метрики**

```python
def test_same_seed_same_episode_metrics(monkeypatch):
    a = run_smoke_episode(trace_flag="0", seed=123)
    b = run_smoke_episode(trace_flag="0", seed=123)
    assert a.metrics == b.metrics
    assert a.action_tuple_counter == b.action_tuple_counter
    assert a.winner == b.winner
```

- [ ] **Step 2: FAIL** (или flaky без seed). Run: `python -m pytest tests/eval/test_eval_determinism.py -q`
- [ ] **Step 3: Реализация**
  - В самом начале `run_episode`, до `roll_off_attacker_defender` и deployment: `random.seed(seed)`, `np.random.seed(seed)`, `torch.manual_seed(seed)`, `torch.cuda.manual_seed_all(seed)` если cuda доступна.
  - Перед reset: `env.reset(seed=seed, options=...)`.
  - `_run_assignment`: `base_seed = int(os.getenv("EVAL_BASE_SEED", "0") or "0")`, `seed = base_seed + idx`.
  - Лог в parent: `[EVAL][SEED] base=... game_idx=... seed=...` только при debug/trace, чтобы не шуметь.
- [ ] **Step 4: PASS.**
- [ ] **Step 5: Коммит**

```bash
git add eval.py tests/eval/test_eval_determinism.py
git commit -m "eval: seed each game for worker-independent determinism"
```

---

### Task 5: worker config + worker entry (один процесс, поднабор игр)

**Цель:** top-level worker entry строит env + агентов один раз из picklable config, гоняет jobs `(idx, seed)` и кладёт `(idx, EpisodeResult | WorkerError)` в очередь. Без прямой записи в общий eval-log.

**Files:**
- Create/Modify: `core/models/eval_parallel.py` — `EvalWorkerConfig`, `WorkerError`, `eval_worker_entry`, `build_worker_runtime`.
- Modify: `eval.py` — вынести/переиспользовать helper сборки runtime для registry-agent path без запуска CLI.
- Test: `tests/eval/test_eval_parallel_worker.py` (create).

**Interfaces:**
- Consumes: `EpisodeResult`, `run_episode(..., seed=...)`.
- Produces: `eval_worker_entry(worker_id, cfg, jobs, result_q, stop_ev)`.

- [ ] **Step 1: Падающий тест (in-process, без spawn)**

```python
def test_worker_runs_jobs_inprocess(monkeypatch):
    cfg = make_worker_smoke_cfg(monkeypatch)  # scripted agents / registry smoke path
    q = queue.Queue()
    class Stop:
        def is_set(self): return False
    eval_worker_entry(worker_id=0, cfg=cfg, jobs=[(1, 100), (2, 101)], result_q=q, stop_ev=Stop())
    got = [q.get(), q.get()]
    assert sorted(i for i, _ in got) == [1, 2]
    assert all(hasattr(r, "metrics") for _, r in got)
```

- [ ] **Step 2: FAIL.** Run: `python -m pytest tests/eval/test_eval_parallel_worker.py -q`
- [ ] **Step 3: Реализация**
  - `eval_parallel.py` не импортирует `eval.py` top-level.
  - В worker entry:
    - применить `cfg.env_overrides` к `os.environ`;
    - lazy-import `eval`;
    - собрать env/model_units/enemy_units/learner_agent/opponent_agent/device через helper из `eval.py`;
    - если `stop_ev.is_set()` перед игрой — break;
    - вызвать `run_episode(..., seed=seed)`;
    - положить `(idx, result)`.
  - В except: положить `WorkerError(worker_id, idx, message, traceback_tail)`; текст RU: что случилось + где + что сделать.
  - MVP: если `cfg.learner_agent_id` пустой, worker возвращает понятный error/fallback handled parent, не пытается пиклить сети.
- [ ] **Step 4: PASS.**
- [ ] **Step 5: Коммит**

```bash
git add eval.py core/models/eval_parallel.py tests/eval/test_eval_parallel_worker.py
git commit -m "eval: add spawn-safe worker entry for parallel evaluation"
```

---

### Task 6: родитель — распределение/мерж/progress/stop (workers>1)

**Цель:** при `EVAL_WORKERS>1` `_run_assignment` гоняет worker-процессы и мержит результаты тем же accumulator, что и последовательный путь. `workers=1` остаётся текущим no-process path.

**Files:**
- Modify: `eval.py` (`_run_assignment`: branch workers>1 + helpers).
- Test: `tests/eval/test_eval_parallel_merge.py` (create), `tests/eval/test_eval_stop_flag.py` (extend if needed).

**Interfaces:**
- Consumes: Task 5 (`eval_worker_entry`, `EvalWorkerConfig`, `WorkerError`).
- Env: `EVAL_WORKERS` default `1`, clamp `>=1`, max no hard cap except games.

- [ ] **Step 1: Ключевой тест — synthetic merge workers=2 == workers=1**

```python
def test_parallel_merge_equals_sequential_on_synthetic_results():
    seq = run_assignment_with_fake_runner(games=4, workers=1, base_seed=7)
    par = run_assignment_with_fake_runner(games=4, workers=2, base_seed=7)
    assert seq["games"] == par["games"] == 4
    assert seq["step_metrics"] == par["step_metrics"]
    assert seq["action_tuple_counter"] == par["action_tuple_counter"]
```

- [ ] **Step 2: Optional smoke — real processes 2 games x 2 workers**
  - Mark `pytest.mark.slow` if too heavy.
  - Run only registry/smoke path.
- [ ] **Step 3: FAIL.** Run: `python -m pytest tests/eval/test_eval_parallel_merge.py -q`
- [ ] **Step 4: Реализация**
  - `_eval_workers = max(1, int(os.getenv("EVAL_WORKERS", "1") or "1"))`.
  - If `_eval_workers > 1` and no `selected_agent_id`: log fallback:
    - что: parallel eval для legacy checkpoint пока не включён;
    - где: `eval.py (_run_assignment)`;
    - что сделать: выбрать learner-agent-id или поставить `EVAL_WORKERS=1`.
  - Jobs: `[(idx, base_seed + idx) for idx in range(1, _games + 1)]`.
  - Distribution: round-robin or chunks; deterministic assignment irrelevant because seed per idx.
  - Spawn: `ctx = multiprocessing.get_context("spawn")`, `ctx.Queue()`, `ctx.Event()`, `ctx.Process(target=eval_worker_entry, args=(...))`.
  - Collect loop:
    - until received results == expected completed/non-started accounting;
    - poll `eval_stop_requested()`; on stop `stop_ev.set()`;
    - `result_q.get(timeout=0.2)`; check worker `exitcode` periodically;
    - on `WorkerError`: log RU error, mark game failed, continue best-effort;
    - on missing games after worker exit: log `[EVAL][WORKER] missing game idx...`, partial report.
  - Graceful shutdown: `join(timeout=5)`, then `terminate()` stuck processes; log action.
  - Progress: log `Игра {done}/{_games}{label}: ...` по мере поступления; GUI парсит число завершённых игр, порядок неважен.
  - Trace: parent writes each `trace_block` contiguously as `[TRACE][GAME {idx}]...`; no interleaving.
  - Reuse `_accumulate_episode_result` for both sequential and parallel branches.
- [ ] **Step 5: PASS + регресс.** Run: `python -m pytest tests/eval -q`
- [ ] **Step 6: Коммит**

```bash
git add eval.py tests/eval/test_eval_parallel_merge.py tests/eval/test_eval_stop_flag.py
git commit -m "eval: run assignments in parallel workers with deterministic merge"
```

---

### Task 7: GUI-поле «Воркеры» + env `EVAL_WORKERS`

**Цель:** поле ввода «Воркеры» рядом с «Игр»/«Детальный лог»; экспорт `EVAL_WORKERS`; стартовый лог показывает число воркеров.

**Files:**
- Modify: `app/gui_qt/main.py`:
  - signal `evalWorkersChanged` рядом с `evalGamesChanged`;
  - `_eval_workers = 1`;
  - property `evalWorkers`;
  - slot `set_eval_workers`;
  - `env.insert("EVAL_WORKERS", str(self._eval_workers))` рядом с `EVAL_ACTION_TRACE`;
  - стартовая строка eval включает `workers=...`.
- Modify: `app/gui_qt/qml/Main.qml`:
  - `TextField` «Воркеры» после «Игр» и перед/рядом с «ДЕТАЛЬНЫЙ ЛОГ».
- Test: `tests/gui_qt/test_eval_workers_field.py` (create).

**Interfaces:**
- Produces: `controller.evalWorkers` / `set_eval_workers(int)`.

- [ ] **Step 1: Падающий тест**

```python
def test_set_eval_workers_clamps_min_1(controller):
    controller.set_eval_workers(4)
    assert controller.evalWorkers == 4
    controller.set_eval_workers(0)
    assert controller.evalWorkers == 4  # <1 игнор, как evalGames
```

- [ ] **Step 2: FAIL.** Run: `python -m pytest tests/gui_qt/test_eval_workers_field.py -q`
- [ ] **Step 3: Реализация**
  - Повторить паттерн `evalGames`/`set_eval_games`.
  - QML `Connections` дополняет `onEvalWorkersChanged`, чтобы поле синхронизировалось с controller.
  - Tooltip/подпись: `1 = последовательный режим; >1 = процессы, больше нагрузка на GPU/CPU`.
- [ ] **Step 4: PASS.**
- [ ] **Step 5: Коммит**

```bash
git add app/gui_qt/main.py app/gui_qt/qml/Main.qml tests/gui_qt/test_eval_workers_field.py
git commit -m "feat(gui): add eval workers field and EVAL_WORKERS export"
```

---

### Task 8: stop/error hardening + live smoke

**Цель:** довести поведение при stop, worker crash, partial report и убедиться, что GUI progress не ломается.

**Files:**
- Modify: `eval.py`, `core/models/eval_parallel.py`.
- Test: `tests/eval/test_eval_parallel_errors.py` (create/extend).

- [ ] **Step 1: Падающий тест — worker error не вешает parent**
  - Fake worker кладёт `WorkerError` или падает после первой игры.
  - Parent возвращает partial report, пишет понятный log, не ждёт бесконечно.
- [ ] **Step 2: Падающий тест — stop flag середина серии**
  - Stop после N результатов: `stop_ev.set()`, workers drain, partial `games=N`, no hang.
- [ ] **Step 3: Реализация**
  - Timeout collect, exitcode polling, missing jobs accounting.
  - Error messages RU format: что случилось + где + что сделать.
  - GPU OOM hint: `уменьшите EVAL_WORKERS`.
- [ ] **Step 4: PASS.** Run: `python -m pytest tests/eval/test_eval_parallel_errors.py tests/eval/test_eval_stop_flag.py -q`
- [ ] **Step 5: Коммит**

```bash
git add eval.py core/models/eval_parallel.py tests/eval/test_eval_parallel_errors.py tests/eval/test_eval_stop_flag.py
git commit -m "eval: harden parallel workers stop and error handling"
```

---

### Task 9: регресс + smoke

- [ ] **Step 1:** `python -m pytest tests/eval -q` — без новых падений vs baseline.
- [ ] **Step 2:** GUI contract: `python -m pytest tests/gui_qt/test_eval_workers_field.py tests/gui/test_gui_eval_summary_v2_contract.py -q`.
- [ ] **Step 3:** ruff imports: `python -m ruff check --select I eval.py core/models/eval_result.py core/models/eval_parallel.py app/gui_qt/main.py tests/eval tests/gui_qt/test_eval_workers_field.py`.
- [ ] **Step 4:** Живой smoke registry-agent path:
  - `EVAL_ACTION_TRACE=0 EVAL_WORKERS=1 EVAL_BASE_SEED=7 python -u eval.py --games 4 --learner-agent-id <id>`
  - `EVAL_ACTION_TRACE=0 EVAL_WORKERS=2 EVAL_BASE_SEED=7 python -u eval.py --games 4 --learner-agent-id <id>`
  - Сравнить: `SUMMARY_V2`, `m_games_total`, `m_model_wins_total`, stratagem table, top-action shares.
- [ ] **Step 5:** Smoke trace parallel:
  - `EVAL_ACTION_TRACE=1 EVAL_WORKERS=2 EVAL_BASE_SEED=7 ... --games 2`
  - Проверить, что trace блоки `[GAME idx]` не перемешаны.
- [ ] **Step 6:** GUI smoke: поле «Воркеры» выставляет env, progress bar считает завершённые игры.
- [ ] **Step 7:** Артефакты/логи не коммитить.
- [ ] **Step 8:** Финал — eval-ревью Opus.

## DoD (сводно)

Tasks 0–8 тесты зелёные; `tests/eval` не хуже baseline; ruff clean; `EVAL_ACTION_TRACE=0` НЕ обнуляет таблицу и не строит дорогие trace-only строки; `workers=N` даёт тот же агрегат, что `workers=1` при том же `EVAL_BASE_SEED`; `action_tuple_counter`/top1/top5 сохранены; worker crash/stop не вешает parent; GUI-поле работает и экспортирует `EVAL_WORKERS`; eval-ревью Opus пройдено.
