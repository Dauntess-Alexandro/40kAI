# Таблица стратагем в eval (только DQN-модель) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** По eval-прогону построить таблицу применения стратагем обучаемой стороны (DQN-модель, `env_side==model`) и сохранить её в `artifacts/results/` как Markdown + CSV.

**Architecture:** Чистый модуль-репортёр `core/telemetry/stratagem_report.py` (только расчёты + форматирование, без I/O игр, тестируется изолированно). `eval.py` парсит трейс-линии стратагем с фильтром `env_side=model`, копит per-sid счётчики и per-эпизодный джойн с исходом в существующем `step_metrics` (Counter, уже текущем к сводке и корректно мёржащемся под swap), и в конце прогона вызывает репортёр + пишет файлы.

**Tech Stack:** Python 3.12, pytest, stdlib (`dataclasses`, `csv`/строки). Без новых зависимостей.

## Global Constraints

- Платформа Windows; язык логов/сообщений/комментариев — русский (AGENTS.md).
- Сообщения об ошибках: что случилось + где (файл/функция) + что делать дальше.
- TDD: тест до кода. Частые коммиты. ruff чистый (`ruff check --fix` гоняется хуком).
- НЕ менять формат `runtime/logs/LOGS_FOR_AGENTS_*.md` и не коммитить runtime-логи.
- Существующие счётчики `stratagem_attempt_total/applied_total/miss_total` и `strat_attempt_{sid}`/`strat_applied_{sid}` (обе стороны) **не трогаем** — добавляем НОВЫЕ model-only счётчики с префиксом `m_`, чтобы не сломать `tests/.../test_eval_stratagem_metric.py`.
- eval обученного DQN-агента запускается через `--learner-agent-id`, НЕ через `--model .pth`.

---

### Task 1: Чистый модуль-репортёр `stratagem_report.py`

**Files:**
- Create: `core/telemetry/stratagem_report.py`
- Test: `tests/core/telemetry/test_stratagem_report.py`

**Interfaces:**
- Produces:
  - `@dataclass StratagemRow` с полями: `stratagem: str`, `attempts: int`, `applied: int`, `miss: int`, `apply_rate_pct: float | None`, `applied_per_game: float`, `games_used: int`, `pct_games: float`, `wr_used: float | None`, `wr_notused: float | None`, `dwr: float | None`.
  - `build_stratagem_rows(*, attempts: dict[str,int], applied: dict[str,int], miss: dict[str,int], games_used: dict[str,int], wins_used: dict[str,int], games_total: int, model_wins_total: int) -> list[StratagemRow]`
  - `rows_to_markdown(rows: list[StratagemRow], *, header_meta: dict) -> str`
  - `rows_to_csv(rows: list[StratagemRow]) -> str`

- [ ] **Step 1: Написать падающий тест**

```python
# tests/core/telemetry/test_stratagem_report.py
from core.telemetry.stratagem_report import (
    StratagemRow,
    build_stratagem_rows,
    rows_to_csv,
    rows_to_markdown,
)


def _rows():
    return build_stratagem_rows(
        attempts={"command_reroll": 100, "overwatch": 40, "rare": 0},
        applied={"command_reroll": 30, "overwatch": 20, "rare": 5},
        miss={"command_reroll": 70, "overwatch": 20},
        games_used={"command_reroll": 50, "overwatch": 50, "rare": 10},
        wins_used={"command_reroll": 20, "overwatch": 15, "rare": 1},
        games_total=100,
        model_wins_total=33,
    )


def test_basic_metrics():
    rows = {r.stratagem: r for r in _rows()}
    cr = rows["command_reroll"]
    assert cr.attempts == 100 and cr.applied == 30 and cr.miss == 70
    assert cr.apply_rate_pct == 30.0          # 30/100*100
    assert cr.applied_per_game == 0.30        # 30/100
    assert cr.games_used == 50
    assert cr.pct_games == 50.0               # 50/100*100
    assert cr.wr_used == 0.40                 # 20/50
    # notused: games_not=50, wins_not=33-20=13 -> 0.26
    assert cr.wr_notused == 0.26
    assert round(cr.dwr, 4) == round(0.40 - 0.26, 4)


def test_apply_rate_none_when_zero_attempts():
    rows = {r.stratagem: r for r in _rows()}
    assert rows["rare"].attempts == 0
    assert rows["rare"].apply_rate_pct is None  # деления на ноль нет


def test_sorted_by_applied_desc():
    rows = _rows()
    applied = [r.applied for r in rows]
    assert applied == sorted(applied, reverse=True)


def test_wr_notused_none_when_all_games_used():
    rows = {
        r.stratagem: r
        for r in build_stratagem_rows(
            attempts={"x": 10}, applied={"x": 5}, miss={"x": 5},
            games_used={"x": 100}, wins_used={"x": 33},
            games_total=100, model_wins_total=33,
        )
    }
    assert rows["x"].wr_notused is None  # games_not == 0
    assert rows["x"].dwr is None


def test_empty_input_no_crash():
    rows = build_stratagem_rows(
        attempts={}, applied={}, miss={},
        games_used={}, wins_used={}, games_total=0, model_wins_total=0,
    )
    assert rows == []
    md = rows_to_markdown(rows, header_meta={"agent_id": "x", "games": 0, "winrate": 0.0, "date": "2026-06-24"})
    assert "стратагем" in md.lower()  # шапка есть, без падения
    assert "нет данных" in md.lower()
    csv = rows_to_csv(rows)
    assert csv.splitlines()[0].startswith("stratagem,")


def test_markdown_renders_dash_for_none():
    rows = _rows()
    md = rows_to_markdown(rows, header_meta={"agent_id": "ag", "games": 100, "winrate": 0.33, "date": "2026-06-24"})
    assert "| rare |" in md
    assert "—" in md  # apply_rate None отрисован как «—»
```

- [ ] **Step 2: Запустить тест — убедиться, что падает**

Run: `python -m pytest tests/core/telemetry/test_stratagem_report.py -q`
Expected: FAIL (ModuleNotFoundError: core.telemetry.stratagem_report).

- [ ] **Step 3: Реализовать модуль**

```python
# core/telemetry/stratagem_report.py
"""Таблица применения стратагем обучаемой стороны (model) по eval-прогону.

Чистые функции расчёта/форматирования: на вход — агрегаты per-sid и тоталы,
на выход — строки таблицы, Markdown и CSV. Без файлового I/O и без запуска игр,
чтобы тестировать изолированно.
"""
from __future__ import annotations

from dataclasses import dataclass

# Колонки CSV/таблицы — единый источник порядка.
_COLUMNS = [
    "stratagem", "attempts", "applied", "miss", "apply_rate_pct",
    "applied_per_game", "games_used", "pct_games", "wr_used", "wr_notused", "dwr",
]


@dataclass
class StratagemRow:
    stratagem: str
    attempts: int
    applied: int
    miss: int
    apply_rate_pct: float | None
    applied_per_game: float
    games_used: int
    pct_games: float
    wr_used: float | None
    wr_notused: float | None
    dwr: float | None


def build_stratagem_rows(
    *,
    attempts: dict[str, int],
    applied: dict[str, int],
    miss: dict[str, int],
    games_used: dict[str, int],
    wins_used: dict[str, int],
    games_total: int,
    model_wins_total: int,
) -> list[StratagemRow]:
    """Собрать строки таблицы по всем встретившимся стратагемам (model-сторона).

    Деления на ноль не бывает: при нулевом знаменателе соответствующая метрика = None
    (в отчёте отрисуется как «—»). Сортировка — по applied убыв.
    """
    sids = set(attempts) | set(applied) | set(miss) | set(games_used) | set(wins_used)
    rows: list[StratagemRow] = []
    for sid in sids:
        att = int(attempts.get(sid, 0))
        app = int(applied.get(sid, 0))
        ms = int(miss.get(sid, 0))
        gu = int(games_used.get(sid, 0))
        wu = int(wins_used.get(sid, 0))
        apply_rate = (app / att * 100.0) if att > 0 else None
        per_game = (app / games_total) if games_total > 0 else 0.0
        pct_games = (gu / games_total * 100.0) if games_total > 0 else 0.0
        wr_used = (wu / gu) if gu > 0 else None
        games_not = games_total - gu
        wins_not = model_wins_total - wu
        wr_notused = (wins_not / games_not) if games_not > 0 else None
        dwr = (wr_used - wr_notused) if (wr_used is not None and wr_notused is not None) else None
        rows.append(StratagemRow(
            stratagem=sid, attempts=att, applied=app, miss=ms,
            apply_rate_pct=apply_rate, applied_per_game=per_game,
            games_used=gu, pct_games=pct_games,
            wr_used=wr_used, wr_notused=wr_notused, dwr=dwr,
        ))
    rows.sort(key=lambda r: r.applied, reverse=True)
    return rows


def _f(value: float | None, digits: int = 3) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def rows_to_markdown(rows: list[StratagemRow], *, header_meta: dict) -> str:
    lines: list[str] = []
    lines.append("# Таблица стратагем (только DQN-модель)\n")
    lines.append(
        f"- agent_id: `{header_meta.get('agent_id', '?')}`  "
        f"games: {header_meta.get('games', 0)}  "
        f"overall winrate: {float(header_meta.get('winrate', 0.0)):.3f}  "
        f"дата: {header_meta.get('date', '')}\n"
    )
    lines.append(
        "> ⚠️ Связь с winrate — **корреляция, а не причинность**: редкие стратагемы "
        "часто маркируют состояние партии (их жмут, когда уже хорошо/плохо), а не определяют исход.\n"
    )
    if not rows:
        lines.append("\n_нет данных: стратагемы моделью не применялись или трейс выключен._\n")
        return "\n".join(lines)
    lines.append(
        "| стратагема | attempts | applied | miss | apply_rate% | applied/game | "
        "games_used | %games | WR_used | WR_notused | ΔWR |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        lines.append(
            f"| {r.stratagem} | {r.attempts} | {r.applied} | {r.miss} | "
            f"{_f(r.apply_rate_pct, 1)} | {r.applied_per_game:.2f} | "
            f"{r.games_used} | {r.pct_games:.1f} | "
            f"{_f(r.wr_used)} | {_f(r.wr_notused)} | {_f(r.dwr)} |"
        )
    return "\n".join(lines) + "\n"


def rows_to_csv(rows: list[StratagemRow]) -> str:
    out = [",".join(_COLUMNS)]
    for r in rows:
        out.append(",".join([
            r.stratagem, str(r.attempts), str(r.applied), str(r.miss),
            "" if r.apply_rate_pct is None else f"{r.apply_rate_pct:.4f}",
            f"{r.applied_per_game:.6f}", str(r.games_used), f"{r.pct_games:.4f}",
            "" if r.wr_used is None else f"{r.wr_used:.6f}",
            "" if r.wr_notused is None else f"{r.wr_notused:.6f}",
            "" if r.dwr is None else f"{r.dwr:.6f}",
        ]))
    return "\n".join(out) + "\n"
```

- [ ] **Step 4: Запустить тест — убедиться, что проходит**

Run: `python -m pytest tests/core/telemetry/test_stratagem_report.py -q`
Expected: PASS (6 passed).

- [ ] **Step 5: Коммит**

```bash
git add core/telemetry/stratagem_report.py tests/core/telemetry/test_stratagem_report.py
git commit -m "feat(eval): чистый модуль-репортёр таблицы стратагем (model-only)"
```

---

### Task 2: Интеграция в `eval.py` — model-only парсинг + джойн + запись файлов

**Files:**
- Modify: `eval.py` (блок парсинга трейс-линий `eval.py:1477-1488`; per-эпизодная аккумуляция около `eval.py:1507`; место сводки около `eval.py:1686`)
- Test: `tests/eval/test_eval_stratagem_table.py`

**Interfaces:**
- Consumes: `build_stratagem_rows`, `rows_to_markdown`, `rows_to_csv` из Task 1.
- Produces: функция `_extract_model_stratagem_aggregates(step_metrics) -> dict` и `_write_stratagem_report(step_metrics, *, agent_id, out_dir) -> tuple[str, str]` в `eval.py` (имена точные — используются тестом).

**Контекст по коду (факты):**
- `step_metrics` создаётся `eval.py:1414`, возвращается `eval.py:1577` (`"step_metrics": step_metrics`), мёржится под swap `eval.py:1662-1664`, читается в сводке `eval.py:1686`.
- Трейс-линии модели: `[WH40K][STRATAGEM][ATTEMPT] ... env_side=model stratagem=<sid> ...`, `[WH40K][STRATAGEM] applied=<sid> ... env_side=model ...`, `[WH40K][STRATAGEM][MISS] ... env_side=model attempted=<sid> ...`.
- Исход игры известен в `eval.py:1527` (`winner == "model"` → победа модели).

- [ ] **Step 1: Написать падающий тест** (парсер-хелперы model-only + запись файлов)

```python
# tests/eval/test_eval_stratagem_table.py
from collections import Counter

from eval import _extract_model_stratagem_aggregates, _write_stratagem_report


def _sm():
    sm = Counter()
    # model-only per-sid (префикс m_), заполняется парсером eval
    sm["m_strat_attempt_command_reroll"] = 100
    sm["m_strat_applied_command_reroll"] = 30
    sm["m_strat_miss_command_reroll"] = 70
    sm["m_strat_games_used_command_reroll"] = 50
    sm["m_strat_wins_used_command_reroll"] = 20
    sm["m_games_total"] = 100
    sm["m_model_wins_total"] = 33
    return sm


def test_extract_aggregates():
    agg = _extract_model_stratagem_aggregates(_sm())
    assert agg["attempts"]["command_reroll"] == 100
    assert agg["applied"]["command_reroll"] == 30
    assert agg["miss"]["command_reroll"] == 70
    assert agg["games_used"]["command_reroll"] == 50
    assert agg["wins_used"]["command_reroll"] == 20
    assert agg["games_total"] == 100
    assert agg["model_wins_total"] == 33


def test_write_report_creates_files(tmp_path):
    md_path, csv_path = _write_stratagem_report(_sm(), agent_id="ag", out_dir=str(tmp_path))
    md = open(md_path, encoding="utf-8").read()
    csv = open(csv_path, encoding="utf-8").read()
    assert "command_reroll" in md
    assert csv.splitlines()[0].startswith("stratagem,")
    assert "command_reroll" in csv
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/eval/test_eval_stratagem_table.py -q`
Expected: FAIL (ImportError: cannot import name `_extract_model_stratagem_aggregates`).

- [ ] **Step 3: Добавить хелперы в `eval.py`** (рядом с другими модульными функциями, напр. возле `_aggregate_swap`)

```python
def _extract_model_stratagem_aggregates(step_metrics) -> dict:
    """Распаковать model-only стратагемные агрегаты из step_metrics (префикс m_)."""
    def _by_prefix(prefix: str) -> dict[str, int]:
        out: dict[str, int] = {}
        for key, val in step_metrics.items():
            if key.startswith(prefix):
                out[key[len(prefix):]] = int(val)
        return out

    return {
        "attempts": _by_prefix("m_strat_attempt_"),
        "applied": _by_prefix("m_strat_applied_"),
        "miss": _by_prefix("m_strat_miss_"),
        "games_used": _by_prefix("m_strat_games_used_"),
        "wins_used": _by_prefix("m_strat_wins_used_"),
        "games_total": int(step_metrics.get("m_games_total", 0) or 0),
        "model_wins_total": int(step_metrics.get("m_model_wins_total", 0) or 0),
    }


def _write_stratagem_report(step_metrics, *, agent_id: str, out_dir: str) -> tuple[str, str]:
    """Построить таблицу стратагем (model-only) и записать Markdown + CSV.

    Возвращает (md_path, csv_path). При ошибке записи — пробрасывает с понятным
    русским сообщением (что/где/что делать).
    """
    import datetime
    import os

    from core.telemetry.stratagem_report import (
        build_stratagem_rows,
        rows_to_csv,
        rows_to_markdown,
    )

    agg = _extract_model_stratagem_aggregates(step_metrics)
    rows = build_stratagem_rows(
        attempts=agg["attempts"], applied=agg["applied"], miss=agg["miss"],
        games_used=agg["games_used"], wins_used=agg["wins_used"],
        games_total=agg["games_total"], model_wins_total=agg["model_wins_total"],
    )
    games = agg["games_total"]
    winrate = (agg["model_wins_total"] / games) if games > 0 else 0.0
    date = datetime.date.today().isoformat()
    md = rows_to_markdown(rows, header_meta={
        "agent_id": agent_id, "games": games, "winrate": winrate, "date": date,
    })
    csv = rows_to_csv(rows)
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        os.makedirs(out_dir, exist_ok=True)
        md_path = os.path.join(out_dir, f"stratagem_eval_{stamp}.md")
        csv_path = os.path.join(out_dir, f"stratagem_eval_{stamp}.csv")
        with open(md_path, "w", encoding="utf-8") as fh:
            fh.write(md)
        with open(csv_path, "w", encoding="utf-8") as fh:
            fh.write(csv)
    except OSError as exc:
        raise OSError(
            f"Не удалось записать отчёт по стратагемам в {out_dir} "
            f"(_write_stratagem_report): {exc}. Проверь права/путь artifacts/results."
        ) from exc
    return md_path, csv_path
```

- [ ] **Step 4: Запустить тест Task 2 — должен пройти**

Run: `python -m pytest tests/eval/test_eval_stratagem_table.py -q`
Expected: PASS (2 passed).

- [ ] **Step 5: Подключить model-only парсинг трейс-линий** в блоке `eval.py:1477-1488`. Добавить рядом с существующими ветками (НЕ удаляя их) разбор `env_side=model`. Перед циклом игр добавить компиляцию регэкспов:

```python
        strat_env_side_re = re.compile(r"env_side=(?P<side>model|enemy)")
        strat_miss_sid_re = re.compile(r"attempted=(?P<sid>\S+)")
```

Внутри `for line in trace_lines:` в соответствующих ветках добавить model-only учёт. Для ATTEMPT (после существующего `step_metrics["stratagem_attempt_total"] += 1`):

```python
                    _es = strat_env_side_re.search(line)
                    if _es and _es.group("side") == "model":
                        _m = strat_attempt_re.search(line)
                        if _m:
                            sid = _m.group("sid")
                            step_metrics[f"m_strat_attempt_{sid}"] += 1
                            ep_model_attempt_sids.add(sid)
```

Для applied-ветки (`[WH40K][STRATAGEM] applied=`):

```python
                    _es = strat_env_side_re.search(line)
                    if _es and _es.group("side") == "model":
                        _m = strat_applied_re.search(line)
                        if _m:
                            sid = _m.group("sid")
                            step_metrics[f"m_strat_applied_{sid}"] += 1
                            ep_model_applied_sids.add(sid)
```

Для MISS-ветки (`[WH40K][STRATAGEM][MISS]`):

```python
                    _es = strat_env_side_re.search(line)
                    if _es and _es.group("side") == "model":
                        _m = strat_miss_sid_re.search(line)
                        if _m:
                            step_metrics[f"m_strat_miss_{_m.group('sid')}"] += 1
```

- [ ] **Step 6: Per-эпизодный джойн с исходом.** В начале тела `for idx in range(1, _games + 1):` (сразу после строки `for idx ...`, до `run_episode`) завести per-game множества:

```python
            ep_model_applied_sids: set[str] = set()
            ep_model_attempt_sids: set[str] = set()  # пока не используется в таблице, для будущего
```

После определения `winner` (после `eval.py:1535`, т.е. после блока if/elif winner) добавить аккумуляцию:

```python
            step_metrics["m_games_total"] += 1
            if winner == "model":
                step_metrics["m_model_wins_total"] += 1
            for sid in ep_model_applied_sids:
                step_metrics[f"m_strat_games_used_{sid}"] += 1
                if winner == "model":
                    step_metrics[f"m_strat_wins_used_{sid}"] += 1
```

- [ ] **Step 7: Вызвать запись отчёта в сводке.** После `eval.py:1686` (`step_metrics = _report["step_metrics"]`) и рядом с `[SUMMARY_V2]` добавить:

> **Уточнение дирижёра (сверено с кодом):** `project_paths.py` экспортирует `ARTIFACTS_RESULTS_DIR` (НЕ `RESULTS_DIR`); в области сводки доступна переменная `selected_agent_id` (НЕ `_run_agent_label`). Использовать именно эти имена.

```python
    try:
        from project_paths import ARTIFACTS_RESULTS_DIR  # каталог artifacts/results
        _results_dir = str(ARTIFACTS_RESULTS_DIR)
    except Exception:
        _results_dir = "artifacts/results"
    _agent_label = str(selected_agent_id or "") or "eval_model"
    _md_path, _csv_path = _write_stratagem_report(
        step_metrics, agent_id=_agent_label, out_dir=_results_dir
    )
    log(
        f"[EVAL][STRATAGEM_TABLE] games={int(step_metrics.get('m_games_total', 0) or 0)} "
        f"model_wins={int(step_metrics.get('m_model_wins_total', 0) or 0)} "
        f"md={_md_path} csv={_csv_path}"
    )
```

> Примечание исполнителю: `selected_agent_id` — это та же переменная, что задаётся из CLI `--learner-agent-id` (см. `eval.py:1078`); она в области видимости функции `main()`, где находится сводка. Если по какой-то причине переменная недоступна — fallback `"eval_model"`.

- [ ] **Step 8: Прогнать полный набор тестов модуля + eval-парсера и smoke**

Run:
```bash
python -m pytest tests/core/telemetry/test_stratagem_report.py tests/eval/test_eval_stratagem_table.py -q
```
Expected: PASS (8 passed).

- [ ] **Step 9: Коммит**

```bash
git add eval.py tests/eval/test_eval_stratagem_table.py
git commit -m "feat(eval): model-only агрегация стратагем + запись таблицы (md+csv)"
```

---

### Task 3: Реальный прогон 1000 игр и заполненная таблица

**Files:**
- Output (не коммитить как код — это артефакт): `artifacts/results/stratagem_eval_<stamp>.md` и `.csv`

- [ ] **Step 1: Smoke на малом прогоне (5 игр)** через тот же путь, что eval использует для агентов. Пример CLI (сверь точные флаги по `eval.py` argparse — у проекта приоритет запуска через Qt GUI, но для smoke допустим терминал):

```bash
python eval.py --learner-agent-id P1_Necrons_only_war_v2_final_ep1000_20260623_192723 --episodes 5
```
Expected: в логе появляется строка `[EVAL][STRATAGEM_TABLE] ... md=... csv=...`; оба файла созданы; в `.md` непустая таблица по model-стороне (как минимум command_reroll/overwatch/go_to_ground).

- [ ] **Step 2: Полный прогон 1000 игр** тем же агентом (~14 мин). Дождаться завершения, проверить, что свежие `stratagem_eval_*.md/.csv` созданы и таблица заполнена.

- [ ] **Step 3: Приложить итоговую таблицу** (содержимое `.md`) к ответу дирижёру/архитектору. Проверить вменяемость: overall winrate в шапке ≈ winrate из `[SUMMARY_V2]` того же прогона.

- [ ] **Step 4: НЕ коммитить** сами артефакты прогона и runtime-логи. Коммитов на этом шаге нет (только проверка результата).

---

## Definition of Done (сводно)

- Task 1+2 тесты зелёные (8 passed), ruff чистый.
- Smoke (5 игр) создаёт оба файла, model-таблица непустая.
- Полный прогон 1000 игр выполнен, `artifacts/results/stratagem_eval_*.md/.csv` заполнены.
- Существующие eval-тесты не сломаны (`python -m pytest tests/eval -q`).
- Коммиты только по коду (Task 1, Task 2); артефакты прогона и логи не коммитятся.
