# Таблица стратагем в eval — двусторонняя (Learner + Opponent) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Расширить уже существующую таблицу стратагем в eval так, чтобы в один отчёт попадали **обе стороны** — Learner (`env_side=model`) и Opponent (`env_side=enemy`), для сравнения двух агентов (напр. PPO vs DQN). Логирование завязано на роль, а не на алгоритм, поэтому любая пара алго работает автоматически.

**Architecture:** Расширяем готовый чистый модуль `core/telemetry/stratagem_report.py` (добавляем `SideReport` + `render_markdown`/`render_csv` для нескольких секций; существующие функции не ломаем). В `eval.py` дублируем парсинг для `env_side=enemy` (префикс `o_`) и переписываем `_write_stratagem_report` на двусторонний вывод: один `.md` с двумя таблицами + один `.csv` с колонкой `side`.

**Tech Stack:** Python 3.12, pytest, stdlib. Без новых зависимостей.

## Global Constraints

- Платформа Windows; язык логов/сообщений/комментариев — русский (AGENTS.md).
- TDD: тест до кода. Частые коммиты. ruff чистый.
- НЕ менять формат `runtime/logs/LOGS_FOR_AGENTS_*.md`, не коммитить runtime-логи и артефакты прогона.
- Существующие сквозные счётчики `stratagem_*_total`, `strat_attempt_{sid}`/`strat_applied_{sid}` (обе стороны, для SUMMARY_V2) **не трогаем**.
- Базируется на уже смёрженной фиче (коммиты `8db4c008`, `3954e314`): model-only счётчики с префиксом `m_`, `_extract_model_stratagem_aggregates`, `_write_stratagem_report`. Opponent — зеркально, префикс `o_`.
- Opponent-секция выводится **всегда** (даже против эвристики → `agent_id=heuristic`).

---

### Task A: Модуль `stratagem_report.py` — многосекционный рендер

**Files:**
- Modify: `core/telemetry/stratagem_report.py`
- Modify (под переименование kwarg): `tests/core/telemetry/test_stratagem_report.py`

**Interfaces:**
- Изменяется: `build_stratagem_rows(...)` — kwarg `model_wins_total` → `side_wins_total` (функция теперь используется для любой стороны).
- Produces:
  - `@dataclass SideReport` с полями `label: str`, `agent_id: str`, `winrate: float`, `rows: list[StratagemRow]`.
  - `render_markdown(sides: list[SideReport], *, run_meta: dict) -> str`
  - `render_csv(sides: list[SideReport]) -> str` (первая колонка — `side`).

- [ ] **Step 1: Обновить существующий тест под переименование kwarg + добавить тесты рендера**

В `tests/core/telemetry/test_stratagem_report.py`:
1) В обоих вызовах `build_stratagem_rows(...)` заменить `model_wins_total=` на `side_wins_total=`.
2) Дописать в конец файла:

```python
from core.telemetry.stratagem_report import SideReport, render_csv, render_markdown


def _two_sides():
    learner = build_stratagem_rows(
        attempts={}, applied={"command_reroll": 30, "overwatch": 20},
        miss={}, games_used={"command_reroll": 50, "overwatch": 60},
        wins_used={"command_reroll": 20, "overwatch": 25},
        games_total=100, side_wins_total=33,
    )
    opp = build_stratagem_rows(
        attempts={}, applied={"go_to_ground": 80},
        miss={}, games_used={"go_to_ground": 90},
        wins_used={"go_to_ground": 60},
        games_total=100, side_wins_total=67,
    )
    return [
        SideReport(label="Learner (model)", agent_id="dqn_ag", winrate=0.33, rows=learner),
        SideReport(label="Opponent (enemy)", agent_id="ppo_ag", winrate=0.67, rows=opp),
    ]


def test_render_markdown_two_sections():
    md = render_markdown(_two_sides(), run_meta={"games": 100, "date": "2026-06-24"})
    assert "Learner (model)" in md and "dqn_ag" in md
    assert "Opponent (enemy)" in md and "ppo_ag" in md
    assert "command_reroll" in md and "go_to_ground" in md


def test_render_csv_has_side_column():
    csv = render_csv(_two_sides())
    header = csv.splitlines()[0]
    assert header.startswith("side,stratagem,")
    body = csv.splitlines()[1:]
    assert any(line.startswith("Learner (model),command_reroll,") for line in body)
    assert any(line.startswith("Opponent (enemy),go_to_ground,") for line in body)


def test_render_markdown_empty_side_no_crash():
    sides = [SideReport(label="Opponent (enemy)", agent_id="heuristic", winrate=0.0, rows=[])]
    md = render_markdown(sides, run_meta={"games": 0, "date": "2026-06-24"})
    assert "нет данных" in md.lower()
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/core/telemetry/test_stratagem_report.py -q`
Expected: FAIL (ImportError `SideReport`/`render_markdown`; и/или TypeError по `side_wins_total`).

- [ ] **Step 3: Реализовать изменения модуля**

a) В сигнатуре и теле `build_stratagem_rows` заменить `model_wins_total` на `side_wins_total` (один параметр и одно использование `wins_not = side_wins_total - wu`).

b) Извлечь общий рендер строк таблицы и CSV-полей (DRY), переиспользовать в старых и новых функциях. Добавить новые сущности. Полный блок для добавления/правки:

```python
def _render_rows_table(rows: list[StratagemRow]) -> list[str]:
    out = [
        "| стратагема | attempts | applied | miss | apply_rate% | applied/game | "
        "games_used | %games | WR_used | WR_notused | ΔWR |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        out.append(
            f"| {r.stratagem} | {r.attempts} | {r.applied} | {r.miss} | "
            f"{_f(r.apply_rate_pct, 1)} | {r.applied_per_game:.2f} | "
            f"{r.games_used} | {r.pct_games:.1f} | "
            f"{_f(r.wr_used)} | {_f(r.wr_notused)} | {_f(r.dwr)} |"
        )
    return out


def _row_csv_fields(r: StratagemRow) -> list[str]:
    return [
        r.stratagem, str(r.attempts), str(r.applied), str(r.miss),
        "" if r.apply_rate_pct is None else f"{r.apply_rate_pct:.4f}",
        f"{r.applied_per_game:.6f}", str(r.games_used), f"{r.pct_games:.4f}",
        "" if r.wr_used is None else f"{r.wr_used:.6f}",
        "" if r.wr_notused is None else f"{r.wr_notused:.6f}",
        "" if r.dwr is None else f"{r.dwr:.6f}",
    ]


@dataclass
class SideReport:
    label: str
    agent_id: str
    winrate: float
    rows: list[StratagemRow]


def render_markdown(sides: list[SideReport], *, run_meta: dict) -> str:
    lines = ["# Таблица стратагем (по сторонам)\n"]
    lines.append(
        f"- games: {run_meta.get('games', 0)}  дата: {run_meta.get('date', '')}\n"
    )
    lines.append(
        "> ⚠️ Связь с winrate — **корреляция, а не причинность**: редкие стратагемы "
        "часто маркируют состояние партии, а не определяют исход.\n"
    )
    for s in sides:
        lines.append(f"\n## {s.label} — `{s.agent_id}`  (winrate: {s.winrate:.3f})\n")
        if not s.rows:
            lines.append("_нет данных: стратагемы этой стороной не применялись._\n")
            continue
        lines.extend(_render_rows_table(s.rows))
    return "\n".join(lines) + "\n"


def render_csv(sides: list[SideReport]) -> str:
    out = ["side," + ",".join(_COLUMNS)]
    for s in sides:
        for r in s.rows:
            out.append(s.label + "," + ",".join(_row_csv_fields(r)))
    return "\n".join(out) + "\n"
```

c) Чтобы не дублировать формат, переписать существующие `rows_to_markdown`/`rows_to_csv` через хелперы (поведение прежнее — старые тесты остаются зелёными):
- в `rows_to_markdown` блок генерации таблицы заменить на `lines.extend(_render_rows_table(rows))`;
- в `rows_to_csv` тело цикла заменить на `out.append(",".join(_row_csv_fields(r)))`.

- [ ] **Step 4: Запустить тесты модуля — все зелёные**

Run: `python -m pytest tests/core/telemetry/test_stratagem_report.py -q`
Expected: PASS (9 passed: 6 старых + 3 новых).

- [ ] **Step 5: ruff + коммит**

```bash
python -m ruff check core/telemetry/stratagem_report.py
git add core/telemetry/stratagem_report.py tests/core/telemetry/test_stratagem_report.py
git commit -m "feat(eval): многосекционный рендер таблицы стратагем (SideReport)"
```

---

### Task B: `eval.py` — парсинг Opponent (env_side=enemy) + двусторонний отчёт

**Files:**
- Modify: `eval.py`
- Modify: `tests/eval/test_eval_stratagem_table.py`

**Interfaces:**
- Consumes: `SideReport`, `render_markdown`, `render_csv`, `build_stratagem_rows` (Task A).
- Produces: `_extract_stratagem_aggregates(step_metrics, *, prefix, games_key, wins_key) -> dict` (обобщённый); `_extract_model_stratagem_aggregates` сохраняется как тонкая обёртка (обратная совместимость).

- [ ] **Step 1: Обновить eval-тест под двусторонний формат**

Переписать `tests/eval/test_eval_stratagem_table.py`:

```python
from collections import Counter

from eval import _extract_model_stratagem_aggregates, _write_stratagem_report


def _sm():
    sm = Counter()
    # learner (model)
    sm["m_strat_applied_command_reroll"] = 30
    sm["m_strat_games_used_command_reroll"] = 50
    sm["m_strat_wins_used_command_reroll"] = 20
    sm["m_games_total"] = 100
    sm["m_model_wins_total"] = 33
    # opponent (enemy)
    sm["o_strat_applied_go_to_ground"] = 80
    sm["o_strat_games_used_go_to_ground"] = 90
    sm["o_strat_wins_used_go_to_ground"] = 60
    sm["o_opp_wins_total"] = 67
    return sm


def test_extract_model_aggregates_backcompat():
    agg = _extract_model_stratagem_aggregates(_sm())
    assert agg["applied"]["command_reroll"] == 30
    assert agg["games_total"] == 100
    assert agg["model_wins_total"] == 33  # обратная совместимость


def test_write_two_sided_report(tmp_path):
    md_path, csv_path = _write_stratagem_report(
        _sm(), agent_id="dqn_ag", out_dir=str(tmp_path), opponent_agent_id="ppo_ag"
    )
    md = open(md_path, encoding="utf-8").read()
    csv = open(csv_path, encoding="utf-8").read()
    assert "Learner (model)" in md and "command_reroll" in md
    assert "Opponent (enemy)" in md and "go_to_ground" in md
    assert csv.splitlines()[0].startswith("side,stratagem,")
    assert any(l.startswith("Opponent (enemy),go_to_ground,") for l in csv.splitlines())
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/eval/test_eval_stratagem_table.py -q`
Expected: FAIL (TypeError: `_write_stratagem_report` не принимает `opponent_agent_id`; и/или нет колонки `side`).

- [ ] **Step 3: Обобщить экстрактор и переписать writer в `eval.py`**

Заменить блок функций `_extract_model_stratagem_aggregates` / `_write_stratagem_report` на:

```python
def _extract_stratagem_aggregates(step_metrics, *, prefix: str, games_key: str, wins_key: str) -> dict:
    """Распаковать стратагемные агрегаты одной стороны из step_metrics по префиксу."""
    def _by_prefix(p: str) -> dict[str, int]:
        out: dict[str, int] = {}
        for key, val in step_metrics.items():
            if key.startswith(p):
                out[key[len(p):]] = int(val)
        return out

    return {
        "attempts": _by_prefix(f"{prefix}strat_attempt_"),
        "applied": _by_prefix(f"{prefix}strat_applied_"),
        "miss": _by_prefix(f"{prefix}strat_miss_"),
        "games_used": _by_prefix(f"{prefix}strat_games_used_"),
        "wins_used": _by_prefix(f"{prefix}strat_wins_used_"),
        "games_total": int(step_metrics.get(games_key, 0) or 0),
        "side_wins_total": int(step_metrics.get(wins_key, 0) or 0),
    }


def _extract_model_stratagem_aggregates(step_metrics) -> dict:
    """Обёртка над _extract_stratagem_aggregates для learner-стороны (обратная совместимость)."""
    agg = _extract_stratagem_aggregates(
        step_metrics, prefix="m_", games_key="m_games_total", wins_key="m_model_wins_total"
    )
    agg["model_wins_total"] = agg["side_wins_total"]  # старый ключ
    return agg


def _write_stratagem_report(
    step_metrics, *, agent_id: str, out_dir: str, opponent_agent_id: str = "heuristic"
) -> tuple[str, str]:
    """Построить двустороннюю таблицу стратагем (Learner + Opponent) и записать MD + CSV."""
    import datetime
    import os

    from core.telemetry.stratagem_report import (
        SideReport,
        build_stratagem_rows,
        render_csv,
        render_markdown,
    )

    def _rows(agg: dict):
        return build_stratagem_rows(
            attempts=agg["attempts"], applied=agg["applied"], miss=agg["miss"],
            games_used=agg["games_used"], wins_used=agg["wins_used"],
            games_total=agg["games_total"], side_wins_total=agg["side_wins_total"],
        )

    m = _extract_stratagem_aggregates(
        step_metrics, prefix="m_", games_key="m_games_total", wins_key="m_model_wins_total"
    )
    o = _extract_stratagem_aggregates(
        step_metrics, prefix="o_", games_key="m_games_total", wins_key="o_opp_wins_total"
    )
    games = m["games_total"]
    m_wr = (m["side_wins_total"] / games) if games > 0 else 0.0
    o_wr = (o["side_wins_total"] / games) if games > 0 else 0.0
    sides = [
        SideReport(label="Learner (model)", agent_id=agent_id, winrate=m_wr, rows=_rows(m)),
        SideReport(label="Opponent (enemy)", agent_id=opponent_agent_id, winrate=o_wr, rows=_rows(o)),
    ]
    date = datetime.date.today().isoformat()
    md = render_markdown(sides, run_meta={"games": games, "date": date})
    csv = render_csv(sides)
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

- [ ] **Step 4: Запустить eval-тест — зелёный**

Run: `python -m pytest tests/eval/test_eval_stratagem_table.py -q`
Expected: PASS (2 passed).

- [ ] **Step 5: Добавить парсинг Opponent (env_side=enemy) — рефактор трёх веток**

В цикле `for line in trace_lines:` три model-only блока (ATTEMPT/applied/MISS), добавленные прошлой задачей, обобщить на обе стороны по префиксу. Заменить каждую из трёх вставок на вариант, бакетирующий по стороне. ATTEMPT:

```python
                    _es = strat_env_side_re.search(line)
                    _side = _es.group("side") if _es else None
                    if _side in ("model", "enemy"):
                        _pfx = "m_" if _side == "model" else "o_"
                        _m = strat_attempt_re.search(line)
                        if _m:
                            _sid = _m.group("sid")
                            step_metrics[f"{_pfx}strat_attempt_{_sid}"] += 1
                            (ep_model_attempt_sids if _side == "model" else ep_opp_attempt_sids).add(_sid)
```

applied:

```python
                    _es = strat_env_side_re.search(line)
                    _side = _es.group("side") if _es else None
                    if _side in ("model", "enemy"):
                        _pfx = "m_" if _side == "model" else "o_"
                        _m = strat_applied_re.search(line)
                        if _m:
                            _sid = _m.group("sid")
                            step_metrics[f"{_pfx}strat_applied_{_sid}"] += 1
                            (ep_model_applied_sids if _side == "model" else ep_opp_applied_sids).add(_sid)
```

MISS:

```python
                    _es = strat_env_side_re.search(line)
                    _side = _es.group("side") if _es else None
                    if _side in ("model", "enemy"):
                        _pfx = "m_" if _side == "model" else "o_"
                        _m = strat_miss_sid_re.search(line)
                        if _m:
                            step_metrics[f"{_pfx}strat_miss_{_m.group('sid')}"] += 1
```

- [ ] **Step 6: Per-эпизодные множества и аккумуляция Opponent**

Рядом с `ep_model_applied_sids`/`ep_model_attempt_sids` (начало тела `for idx ...`) добавить:

```python
            ep_opp_applied_sids: set[str] = set()
            ep_opp_attempt_sids: set[str] = set()  # для будущего, как и у model
```

В блоке аккумуляции после определения `winner` (где уже есть `m_games_total`/`m_model_wins_total`) добавить opponent:

```python
            if winner == "enemy":
                step_metrics["o_opp_wins_total"] += 1
            for sid in ep_opp_applied_sids:
                step_metrics[f"o_strat_games_used_{sid}"] += 1
                if winner == "enemy":
                    step_metrics[f"o_strat_wins_used_{sid}"] += 1
```

- [ ] **Step 7: Прокинуть opponent_agent_id в месте вызова writer**

В блоке сводки, где вызывается `_write_stratagem_report(...)`, добавить opponent id. Использовать реальный идентификатор оппонента, доступный в этой области (по аналогии с `selected_agent_id` для learner — найди соответствующую переменную оппонента в eval, напр. `selected_opponent_agent_id`; при отсутствии — строку `"heuristic"`):

```python
    _opp_label = str(globals().get("selected_opponent_agent_id", "") or "") or "heuristic"
    _md_path, _csv_path = _write_stratagem_report(
        step_metrics, agent_id=_agent_label, out_dir=_results_dir, opponent_agent_id=_opp_label
    )
```

> Примечание исполнителю: имя переменной оппонента сверь по коду eval (как в прошлой задаче сверял `ARTIFACTS_RESULTS_DIR`/`selected_agent_id`). Если оппонент-агента нет (игра против эвристики) — оставить `"heuristic"`.

- [ ] **Step 8: Полный прогон тестов + smoke**

Run:
```bash
python -m pytest tests/core/telemetry/test_stratagem_report.py tests/eval -q
python eval.py --learner-agent-id P1_Necrons_only_war_v2_final_ep1000_20260623_192723 --episodes 5
```
Expected: тесты PASS; в `.md` две секции (Learner с данными, Opponent с данными — эвристика тоже жмёт go_to_ground/overwatch); CSV с колонкой `side`.

- [ ] **Step 9: Коммит (только код, без артефактов прогона)**

```bash
git add eval.py tests/eval/test_eval_stratagem_table.py
git commit -m "feat(eval): двусторонняя таблица стратагем (Learner + Opponent)"
```

---

## Definition of Done

- Task A: 9 passed (модуль), ruff чистый.
- Task B: eval-тесты passed, существующие eval-тесты не сломаны (`python -m pytest tests/eval -q`), ruff на eval.py без НОВЫХ ошибок (базовый долг файла не считается).
- Smoke (5 игр) даёт `.md` с двумя непустыми секциями и `.csv` с колонкой `side`.
- Полный прогон 1000 игр (по желанию заказчика; для agent-vs-agent — запустить с `--opponent-agent-id`).
- Коммиты только по коду; артефакты прогона/логи не коммитятся.
