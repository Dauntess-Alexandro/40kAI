# Параллельный eval + развязка метрик от trace — Design

**Дата:** 2026-06-25
**Статус:** проектирование (brainstorming → spec)

## Goal

Ускорить `eval.py` (сейчас строго последовательный, ~30–67 c/игра при двух умных
агентах) через **процессы-воркеры**, не теряя двустороннюю таблицу стратагем и winrate.
Побочно — **развязать сбор метрик от verbose-trace**, чтобы `EVAL_ACTION_TRACE=0`
ускорял, но НЕ ломал таблицу.

## Контекст (как сейчас)

- `eval.py`: `main()` → `_run_assignment()` гоняет `for idx in range(games): run_episode(...)`,
  который возвращает `(winner, end_reason, vp…, total_reward, hp_diff, kill_diff, trace_lines)`.
- `step_metrics` (Counter) для таблицы строится **парсингом `trace_lines`** в `_run_assignment`
  (≈1540+): action-опции из `[TRACE][MODEL_ACTION_HUMAN]`, стратагемы `m_`/`o_` из
  `[WH40K][STRATAGEM][ATTEMPT/APPLIED/MISS]`.
- `trace_lines` гейтятся `EVAL_ACTION_TRACE` (`run_episode._trace`). → **`trace=0` ⇒ пустой
  `step_metrics` ⇒ пустая таблица** (winrate выживает — он из возвращаемых полей).
- `_write_stratagem_report(step_metrics, …)` пишет `.md`/`.csv`.
- Последовательно, без параллельности. Stop — через `eval_stop_requested()`.

## Архитектура

### Часть A — развязка метрик (фундамент)

`run_episode` возвращает структурированный per-game результат (dataclass `EpisodeResult`
или `(исход…, metrics: Counter, trace_block: list[str])`), где `metrics` считается **внутри
эпизода** (у `run_episode` уже есть `ep_stratagem_attempts/applied`; добьём per-side `m_`/`o_`
и action-опции — те же ключи, что сейчас собирает парсер `_run_assignment`).

- `metrics` Counter: `total_model_steps`, `move_opt_steps`, `shoot_opt_steps`, `charge_opt_steps`,
  `*_zero_opt_steps`, `m_strat_attempt_{sid}`/`m_strat_applied_{sid}`/`m_strat_miss_{sid}`,
  `o_strat_*`, `m_games_total`, `m_model_wins_total`, `o_opp_wins_total` и пр. (полный набор —
  по текущему парсеру).
- `trace_block`: строки игры; пуст, если `EVAL_ACTION_TRACE=0`.

`_run_assignment`: вместо парсинга `trace_lines` — `step_metrics.update(ep.metrics)` напрямую;
`trace_block` пишется в лог (если есть). **Парсинг-ветка удаляется.**

Эффект: `EVAL_ACTION_TRACE=0` → `trace_block` пуст, но `metrics` полны → таблица цела.

### Часть B — процессные воркеры

- Управление: env `EVAL_WORKERS` + GUI-поле «Воркеры» (зеркало `evalGames`), **дефолт 1**.
- `workers ≤ 1`: текущий путь (через новые структурные метрики), **без процессов** —
  поведение/совместимость сохранены.
- `workers > 1`:
  - Родитель назначает каждой игре `seed = base_seed + game_index`.
  - Распределяет индексы игр по воркерам (chunk/round-robin).
  - Воркер-процесс (`multiprocessing`, spawn; `Process`+`Queue`): принимает cfg
    (`learner_agent_id`, `opponent_agent_id`, side, mission, ruleset, список `(idx, seed)`),
    строит env + **оба агента один раз** (сети не пиклятся → строятся в воркере, как train-актёр),
    гоняет свои игры, кладёт `(idx, EpisodeResult)` в `result_queue`.
  - Родитель собирает результаты, мержит `metrics`, пишет `trace_block`'и (по `idx`), эмитит
    `[EVAL] Игра X/N` по мере поступления (счётчик завершённых; порядок неважен) → GUI-прогресс жив.
  - После всех — `_write_stratagem_report` + сводка как сейчас.
- GPU: воркеры делят одну карту (`net.infer`); малые сети — ок; число задаёт пользователь.

### Часть C — детерминизм

`seed = f(game_index)` (не воркера) → **агрегат при N воркерах == при 1** для тех же seed'ов.
Реализация: прокинуть `seed` в `run_episode` → засев env/RNG (точную точку — в плане).
Best-effort: dice/env воспроизводимы; MCTS на eval greedy. Побитовую идентичность на разном
железе не гарантируем.

### Часть D — trace в параллели

Воркер буферизует `trace_block` игры, отдаёт целиком; родитель пишет contiguously с тегом
`[GAME idx]` (не перемешано). `workers=1` — как сейчас, потоково.

### Часть E — stop-flag / прогресс

Родитель поллит `eval_stop_requested()`; при стопе — сигнал воркерам (stop-event / poison pill),
дождаться drain, написать **частичный** отчёт. Прогресс = число завершённых игр.

### Часть F — GUI

Зеркало `evalGames`: `_eval_workers`, property `evalWorkers`, slot `set_eval_workers`,
env `EVAL_WORKERS`; поле «Воркеры» рядом с «Игр»/«Детальный лог».

## Error handling

- Воркер упал → родитель ловит (`result_queue` sentinel / `exitcode`), логирует
  `[EVAL][WORKER] воркер N упал: <что/где/что делать>`; **дефолт — best-effort** (лог +
  продолжить с остальными; недостающие игры отметить в сводке).
- `agent_id` не резолвится в воркере → понятная ошибка (как в основном пути).
- GPU OOM при многих воркерах → поймать, посоветовать уменьшить `EVAL_WORKERS`.

## Тестирование (TDD)

1. **Развязка:** `run_episode` отдаёт корректные `m_`/`o_`/action метрики при `EVAL_ACTION_TRACE=0`
   (маленький env).
2. **Детерминизм-merge (ключевой):** агрегат `step_metrics` при `workers=2` == при `workers=1`
   для тех же seed'ов (2–4 игры).
3. **Worker smoke:** 2 игры × 2 воркера → метрики мержатся, `.md`/`.csv` пишутся, winrate верный.
4. **Trace:** `workers=1 trace=1` → `trace_block` в логе; `trace=0` → нет trace, но таблица есть.
5. **Stop-flag:** стоп на середине → частичный отчёт, без зависа.
6. **Регресс:** `tests/eval/*` зелёные (сверка с baseline).

## Риски / scope

- Ядро eval-цикла — зона риска; рефактор `run_episode`/`_run_assignment` строго по TDD.
- Сети не пиклятся → воркер строит сам; накладные на старт воркера (2 сети) амортизируются на
  длинных прогонах (короткие/малые `games` — лучше `workers=1`).
- GPU contention при многих воркерах — пользователь контролирует числом.
- Детерминизм MCTS на GPU — best-effort.
- **НЕ трогаем:** action-контракт, reward, формат `LOGS_FOR_AGENTS_*`, сквозные счётчики
  SUMMARY_V2 (`stratagem_*_total`, `strat_attempt_{sid}`/`strat_applied_{sid}`).

## DoD

Все тесты 1–6 зелёные; `tests/eval` регресс не хуже baseline; ruff чист; smoke: `workers=4`
на 8 играх даёт тот же агрегат, что `workers=1`; финал — eval-ревью Opus.
