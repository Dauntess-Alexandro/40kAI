# Eval Battle Report — Implementation Plan

> **Для агентов-исполнителей:** реализуйте по задачам, TDD (тест → провал → код → зелёный → коммит). Шаги — чекбоксы `- [ ]`.
> **Спека (источник «ЧТО и ПОЧЕМУ»):** `docs/superpowers/specs/2026-06-26-eval-battle-report-design.md`.

## Для дирижёра (GPT 5.5 xhigh)

Это план архитектора (Opus). Не меняй замысел/архитектуру. Перед делегированием разбери на узкие
TDD-под-задачи (как ниже). Порядок задач = порядок зависимостей. Задачи 1–6 — чистый Python (легко
тестируются, можно отдать исполнителю как есть). Задачи 7–8 трогают большой `eval.py run_episode` —
давай исполнителю точные якоря (ниже) и требуй прогон существующих eval-тестов на регрессии. Любая
неоднозначность → СТОП, вопрос наверх (Opus/заказчику), не выдумывай. Финальное ревью всего диффа —
за Opus (engine не трогаем, но затронут eval-горячий путь).

**Goal:** Генерировать читаемый человеком и ИИ markdown-battle-report по каждой eval-партии: пофазно
«кто как ходил» по обеим сторонам + scoreboard (VP/HP/контроль/урон/потери), файл на партию + `index.md`.

**Architecture:** Новый модуль `core/eval/battle_report.py` = collector (накапливает структурированную
запись в хук-точках `run_episode`) → `render_battle_report(record)` (чистая функция → markdown) →
writer (пишет файлы). `run_episode` рендерит и кладёт markdown+summary в `EpisodeResult`
(picklable, едет из параллельных воркеров); запись файла+index — в едином месте `_merge_and_log`.

**Tech Stack:** Python 3.12, dataclasses, pytest. Без новых зависимостей.

## Global Constraints (verbatim из спеки/AGENTS.md)

- Платформа Windows; язык отчёта/логов/ошибок — **русский**.
- Включение — существующий тумблер «Детальный лог» = env `EVAL_ACTION_TRACE` (`"1"` = вкл; дефолт вкл).
  Отдельного тумблера НЕ вводить.
- **Без RL-reward врага и без правок наград движка.** В scoreboard reward-колонок НЕТ.
- Формат — markdown: нарратив + таблицы. JSON-приложения НЕТ.
- Файлы: `artifacts/results/battle_reports/<run_id>/game_NNN.md` + `index.md`. Не трогать
  guarded `runtime/logs/LOGS_FOR_AGENTS_EVAL.md`.
- Нарратив — только значимые действия; пустые фазы сворачивать; если сторона ничего не сделала —
  строка `— без активных действий —`.
- Сбор данных гейтится тем же флагом, что текстовый трейс (`trace_enabled`), но НЕ зависит от него
  по данным (свои структуры).
- DRY/YAGNI/TDD, частые коммиты, тесты вперёд.

## Карта файлов

- **Create** `core/eval/__init__.py` — пустой пакет.
- **Create** `core/eval/battle_report.py` — dataclasses записи, `BattleReportCollector`,
  `render_battle_report`, `write_battle_report`, `update_index`.
- **Modify** `core/models/eval_result.py` — +2 поля в `EpisodeResult`.
- **Modify** `eval.py` — хуки коллектора в `run_episode`; рендер в конце; запись файлов в
  `_merge_and_log`; вычисление `run_id`/каталога.
- **Create tests** `tests/eval/test_battle_report_render.py`,
  `tests/eval/test_battle_report_collector.py`, `tests/eval/test_battle_report_writer.py`.

---

## Task 1: Поля battle-report в EpisodeResult

**Files:**
- Modify: `core/models/eval_result.py`
- Test: `tests/eval/test_battle_report_collector.py` (общий файл, начнём с него)

**Interfaces — Produces:** `EpisodeResult.battle_report_md: str | None`,
`EpisodeResult.battle_report_summary: dict | None` (дефолт `None`).

- [ ] **Step 1: Тест — поля есть и дефолтятся None**
```python
# tests/eval/test_battle_report_collector.py
from core.models.eval_result import EpisodeResult

def test_episode_result_has_battle_report_fields_default_none():
    r = EpisodeResult(
        winner="model", end_reason="x", vp_diff=0, model_vp=0, enemy_vp=0,
        episode_len=1, total_reward=0.0, hp_diff_model_minus_enemy=0.0,
        kill_diff_model_minus_enemy=0.0,
    )
    assert r.battle_report_md is None
    assert r.battle_report_summary is None
```
- [ ] **Step 2: Прогнать — провал** `pytest tests/eval/test_battle_report_collector.py -q` → FAIL (нет атрибутов).
- [ ] **Step 3: Добавить поля.** В `core/models/eval_result.py` после `event_log_block`:
```python
    battle_report_md: str | None = None
    battle_report_summary: dict | None = None
```
- [ ] **Step 4: Прогнать — зелёно.**
- [ ] **Step 5: Commit** `git add -A && git commit -m "feat(eval): поля battle_report в EpisodeResult"`

---

## Task 2: Модель данных записи + пакет core/eval

**Files:**
- Create: `core/eval/__init__.py` (пустой), `core/eval/battle_report.py`
- Test: `tests/eval/test_battle_report_collector.py`

**Interfaces — Produces (dataclasses):**
```python
@dataclass
class PhaseEvent:        # одно значимое действие в фазе
    phase: str           # "Командная"|"Движение"|"Стрельба"|"Чардж"|"Бой"
    text: str            # "Intercessors → Ork Boyz: −4 HP"

@dataclass
class SideRound:         # действия одной стороны за раунд
    side_label: str      # "P1"|"P2"
    faction: str
    events: list[PhaseEvent] = field(default_factory=list)

@dataclass
class ScoreRow:
    side_label: str; faction: str; vp: int; hp_cur: float; hp_max: float
    ctrl: int; dmg_total: float; losses: int

@dataclass
class RoundRecord:
    battle_round: int
    sides: list[SideRound] = field(default_factory=list)
    scoreboard: list[ScoreRow] = field(default_factory=list)

@dataclass
class BattleRecord:
    game_idx: int; learner_side: str; opponent_side: str
    p1_faction: str; p2_faction: str
    learner_algo: str; opponent_label: str; mission: str; seed: int | None
    rounds: list[RoundRecord] = field(default_factory=list)
    winner: str | None = None       # "P1"|"P2"|"draw"
    end_reason: str = ""; length: int = 0
    final_scoreboard: list[ScoreRow] = field(default_factory=list)
```

- [ ] **Step 1: Тест — BattleRecord конструируется и пустой по умолчанию**
```python
from core.eval.battle_report import BattleRecord
def test_battle_record_minimal():
    rec = BattleRecord(game_idx=1, learner_side="P1", opponent_side="P2",
        p1_faction="SM", p2_faction="Orks", learner_algo="dqn",
        opponent_label="heuristic", mission="Only War", seed=42)
    assert rec.rounds == [] and rec.winner is None
```
- [ ] **Step 2: Провал** (модуля нет).
- [ ] **Step 3: Создать `core/eval/__init__.py` (пусто) и dataclasses выше в `core/eval/battle_report.py`** (с `from __future__ import annotations`, `from dataclasses import dataclass, field`).
- [ ] **Step 4: Зелёно.**
- [ ] **Step 5: Commit** `git commit -m "feat(eval): модель данных BattleRecord + пакет core/eval"`

---

## Task 3: Collector — запись значимых пофазных действий

**Files:** Modify `core/eval/battle_report.py`; Test `tests/eval/test_battle_report_collector.py`

**Interfaces:**
- Consumes: `action_dict` (контракт `ordered_action_keys`), список юнитов с методом
  `showUnitData() -> dict` (есть `"Name"`).
- Produces:
```python
class BattleReportCollector:
    def __init__(self, header: BattleRecord) -> None: ...
    def record_side_actions(self, battle_round: int, side_label: str, faction: str,
                            action_dict: dict, units: list) -> None: ...
    def to_record(self) -> BattleRecord: ...
```
Хелпер (модульная функция, тестируемый отдельно):
```python
def significant_phase_events(action_dict: dict, units: list) -> list[PhaseEvent]:
    """Только значимые действия. move!=4 → Движение; shoot_num_i>=0 → Стрельба (юнит i →
    цель idx); charge_num_i>0 → Чардж; attack==1 → Бой. Пустые фазы пропускаются.
    Имя юнита: units[i].showUnitData().get('Name') или 'unit{i}'."""
```

- [ ] **Step 1: Тест significant_phase_events — фильтрация пустых**
```python
from core.eval.battle_report import significant_phase_events
class _U:
    def __init__(self, name): self._n = name
    def showUnitData(self): return {"Name": self._n}
def test_significant_events_skip_empty():
    units = [_U("Intercessors"), _U("Hellblasters")]
    # move=4 (stay), без shoot/charge/attack → пусто
    assert significant_phase_events({"move": 4, "attack": 0,
        "shoot_num_0": -1, "shoot_num_1": -1, "charge_num_0": 0, "charge_num_1": 0}, units) == []
def test_significant_events_shoot_named():
    units = [_U("Intercessors"), _U("Hellblasters")]
    ev = significant_phase_events({"move": 4, "attack": 0,
        "shoot_num_0": 2, "shoot_num_1": -1, "charge_num_0": 0, "charge_num_1": 0}, units)
    assert len(ev) == 1 and ev[0].phase == "Стрельба" and "Intercessors" in ev[0].text
```
- [ ] **Step 2: Провал.**
- [ ] **Step 3: Реализовать `significant_phase_events` и `BattleReportCollector`** (collector группирует
  события по `(battle_round, side_label)` в `SideRound`, складывает в `RoundRecord`, отдаёт через
  `to_record`). move-метки направлений можно опустить (просто `move=<n>`); главное — имя юнита и фаза.
- [ ] **Step 4: Зелёно.**
- [ ] **Step 5: Commit** `git commit -m "feat(eval): collector значимых пофазных действий"`

---

## Task 4: Collector — scoreboard + урон/потери из снапшотов info

**Files:** Modify `core/eval/battle_report.py`; Test `tests/eval/test_battle_report_collector.py`

**Interfaces — Produces:**
```python
def record_scoreboard(self, battle_round: int, info: dict) -> None: ...
def finish(self, winner: str | None, end_reason: str, length: int, final_info: dict) -> None: ...
```
Ключи `info`: `"model health"`,`"player health"` (списки HP), `"model VP"`,`"player VP"`,
`"model controlled objectives"`,`"player controlled objectives"` (списки → длина = ctrl),
`"winner"` (`"model"|"enemy"|None`), `"end reason"`.

Производные: `dmg_total[side]` = накопл. потеря HP противоположной стороны (сумма HP врага на старте −
текущая, не ниже 0); `losses[side]` = число своих юнитов с HP≤0. Стартовые HP коллектор запоминает в
первом `record_scoreboard`. Маппинг model↔P1/P2 — по `header.learner_side` (model = learner_side).

- [ ] **Step 1: Тест — урон/потери из двух снапшотов**
```python
def test_scoreboard_damage_and_losses(): ...
    # round1 info: model health [10,10], player health [10,10]
    # round2 info: model health [10,0],  player health [4,10]
    # learner_side="P1" → model=P1. P1 нанёс врагу (player) 10-? : player с [10,10]->[4,10]=6 урона
    # P2(player) нанёс model: model [10,10]->[10,0]=10 урона; losses: P1=1 (один юнит в 0)
```
(исполнитель: собрать collector, подать два `record_scoreboard`, проверить `to_record().rounds[-1].scoreboard`
строки P1/P2 на `dmg_total`/`losses`.)
- [ ] **Step 2: Провал.**
- [ ] **Step 3: Реализовать `record_scoreboard`/`finish`** с диффом HP и подсчётом потерь; `finish`
  заполняет `winner` (model→learner_side, enemy→opponent_side, иначе "draw"), `end_reason`, `length`,
  `final_scoreboard` (копия последнего scoreboard).
- [ ] **Step 4: Зелёно.**
- [ ] **Step 5: Commit** `git commit -m "feat(eval): scoreboard + урон/потери в collector"`

---

## Task 5: render_battle_report — markdown (главная точка тестов)

**Files:** Modify `core/eval/battle_report.py`; Test `tests/eval/test_battle_report_render.py`

**Interfaces — Produces:** `def render_battle_report(record: BattleRecord) -> str`.
Формат — как в спеке §5: H1 «Battle Report — Партия N», строка «P1 … vs P2 … · миссия … · seed …»;
по раундам `## Battle Round k` → `### P1 (faction)` + буллеты событий (или `— без активных действий —`)
→ `### P2 …` → markdown-таблица scoreboard (колонки §6, БЕЗ reward); в конце `## Итог (After-Action)`.

- [ ] **Step 1: Тест — секции, обе стороны, таблица, итог, без reward**
```python
from core.eval.battle_report import (BattleRecord, RoundRecord, SideRound,
    PhaseEvent, ScoreRow, render_battle_report)
def _rec():
    sr = [ScoreRow("P1","SM",5,18,30,2,22,1), ScoreRow("P2","Orks",3,11,30,1,17,3)]
    rr = RoundRecord(2, sides=[
        SideRound("P1","SM",[PhaseEvent("Стрельба","Intercessors → Ork Boyz: −4 HP")]),
        SideRound("P2","Orks",[])], scoreboard=sr)
    return BattleRecord(7,"P1","P2","SM","Orks","dqn","ppo","Only War",42,
        rounds=[rr], winner="P1", end_reason="vp", length=24, final_scoreboard=sr)
def test_render_has_sections():
    md = render_battle_report(_rec())
    assert "# Battle Report — Партия 7" in md
    assert "## Battle Round 2" in md
    assert "### P1 (SM)" in md and "### P2 (Orks)" in md
    assert "Intercessors → Ork Boyz: −4 HP" in md
    assert "— без активных действий —" in md          # пустая сторона свёрнута
    assert "| Сторона | VP |" in md                    # scoreboard-таблица
    assert "reward" not in md.lower()                   # reward-колонок нет
    assert "## Итог (After-Action)" in md and "Победитель: P1" in md
```
- [ ] **Step 2: Провал.**
- [ ] **Step 3: Реализовать `render_battle_report`** (чистый markdown по спеке §5/§6).
- [ ] **Step 4: Зелёно.**
- [ ] **Step 5: Commit** `git commit -m "feat(eval): render_battle_report (markdown)"`

---

## Task 6: writer + index

**Files:** Modify `core/eval/battle_report.py`; Test `tests/eval/test_battle_report_writer.py`

**Interfaces — Produces:**
```python
def write_battle_report(run_dir: str, game_idx: int, markdown: str) -> str   # путь game_NNN.md
def update_index(run_dir: str, summary: dict) -> None
# summary: {"game_idx":int,"p1_faction":str,"p2_faction":str,"winner":str,
#           "p1_vp":int,"p2_vp":int,"file":"game_007.md"}
```
`run_dir` создаётся при необходимости; `game_NNN.md` — zero-pad 3 (`game_007.md`); `index.md` —
заголовок таблицы при первом вызове, далее аппенд строки.

- [ ] **Step 1: Тест — файлы создаются (tmp_path)**
```python
def test_writer_creates_files(tmp_path):
    from core.eval.battle_report import write_battle_report, update_index
    p = write_battle_report(str(tmp_path), 7, "# hi")
    assert p.endswith("game_007.md") and open(p, encoding="utf-8").read() == "# hi"
    update_index(str(tmp_path), {"game_idx":7,"p1_faction":"SM","p2_faction":"Orks",
        "winner":"P1","p1_vp":5,"p2_vp":3,"file":"game_007.md"})
    idx = open(str(tmp_path)+"/index.md", encoding="utf-8").read()
    assert "game_007.md" in idx and "| 7 |" in idx
```
- [ ] **Step 2: Провал.**
- [ ] **Step 3: Реализовать writer/index** (utf-8, `os.makedirs(exist_ok=True)`).
- [ ] **Step 4: Зелёно.**
- [ ] **Step 5: Commit** `git commit -m "feat(eval): writer battle report + index"`

---

## Task 7: Интеграция в run_episode (сбор + рендер в EpisodeResult)

**Files:** Modify `eval.py` (функция `run_episode`, начало `def run_episode` ~стр.759; возврат
`EpisodeResult` ~стр.1456). Test: расширить `tests/eval/test_battle_report_collector.py` лёгким
интеграционным проходом (или smoke в Task 9).

**Якоря (точные места вставки):**
- Импорт вверху `eval.py` рядом с прочими `from core...`: `from core.eval.battle_report import BattleReportCollector, render_battle_report`.
- После вычисления сторон/миссии в начале `run_episode` (после `mission_name = ...`, ~стр.790):
  создать коллектор под флагом:
```python
    report_collector = None
    if trace_enabled:   # trace_enabled определяется ниже; перенести создание ПОСЛЕ его вычисления
        from core.eval.battle_report import BattleRecord
        report_collector = BattleReportCollector(BattleRecord(
            game_idx=0,  # реальный idx проставит писатель; для рендера не критичен
            learner_side=str(learner_side),
            opponent_side=("P2" if str(learner_side).upper()=="P1" else "P1"),
            p1_faction=_faction_for("P1"), p2_faction=_faction_for("P2"),
            learner_algo=str(getattr(learner_agent,"algo","")),
            opponent_label=(str(getattr(opponent_agent,"algo","")) if opponent_agent else "heuristic"),
            mission=str(mission_name), seed=seed))
```
  ВАЖНО: `trace_enabled` в текущем коде определяется внутри (стр.795). Дирижёр: помести создание
  коллектора СРАЗУ после строки `trace_enabled = ...`. `_faction_for(side)` — взять фракцию из
  roster/`env_unwrapped` (если нет готового — `learner`/`opponent` faction из тех же источников, что
  `[WH40K][AFTER_ACTION_REPORT]`; при отсутствии — `"—"`).
- В `_enemy_half`, внутри `_logged_opponent_policy`, рядом с `_trace(f"[TRACE][ENEMY_ACTION] ...")`
  (~стр.1055), под `if report_collector is not None`:
```python
        report_collector.record_side_actions(int(battle_round), opponent_side,
            _faction_for(opponent_side), action, enemy_units)
```
- В `_model_half`, после получения `action_dict` (~стр.1117), аналогично для model:
```python
        if report_collector is not None:
            report_collector.record_side_actions(int(_safe_int(_info.get("battle round",0),0) or 1),
                "model_as_side", _faction_for("model"), action_dict, model_units)
```
  (дирижёр: `side_label` для model = `eval_side_label('model', learner_side)` → "P1"/"P2"; используй
  существующий helper `eval_side_label`.)
- В step-result блоке (после `[WH40K][BATTLESTATE]`, ~стр.1301) под `if report_collector is not None`:
  `report_collector.record_scoreboard(int(_safe_int(_info.get("battle round",0),0)), _info)`.
- Перед `return EpisodeResult(...)` (~стр.1456): если коллектор есть —
```python
    battle_md = None; battle_summary = None
    if report_collector is not None:
        report_collector.finish(winner, end_reason or "unknown", int(episode_len), info)
        _rec = report_collector.to_record()
        battle_md = render_battle_report(_rec)
        battle_summary = {"p1_faction": _rec.p1_faction, "p2_faction": _rec.p2_faction,
            "winner": _rec.winner or "draw", "p1_vp": _safe_int(model_vp if learner_side=="P1" else enemy_vp,0),
            "p2_vp": _safe_int(enemy_vp if learner_side=="P1" else model_vp,0)}
```
  и добавить в конструктор `EpisodeResult(...)`: `battle_report_md=battle_md, battle_report_summary=battle_summary`.

- [ ] **Step 1: Тест — run_episode при trace_enabled кладёт markdown в результат** (мини-eval, как в
  существующих eval-тестах: построить env через `tests.engine.phases._helpers.build_env`, агентов через
  `_agent`/фабрику, выставить `os.environ["EVAL_ACTION_TRACE"]="1"`, вызвать `run_episode`, проверить
  `result.battle_report_md` содержит `"# Battle Report"` и `result.battle_report_summary["winner"]` задан).
- [ ] **Step 2: Провал** (поля None).
- [ ] **Step 3: Внести хуки по якорям выше.** Все вызовы коллектора — строго под `if report_collector
  is not None` / `if trace_enabled`, чтобы при выключенном тумблере путь не менялся.
- [ ] **Step 4: Зелёно + регрессии:** `pytest tests/eval -q` (не должно покраснеть).
- [ ] **Step 5: Commit** `git commit -m "feat(eval): сбор battle report в run_episode"`

---

## Task 8: Запись файлов в _merge_and_log (оба пути) + run_id

**Files:** Modify `eval.py` (функция `main` → вложенная `_run_assignment` ~стр.1896 → `_merge_and_log`
~стр.1924; обе ветки вызывают `_merge_and_log`: parallel ~стр.2053, sequential ~стр.2088).

**Якоря:**
- В `main`, до запуска назначений (рядом с резолвом `_results_dir`, ~стр.2198), вычислить один раз:
```python
    import datetime as _dt
    _battle_run_id = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    _battle_dir = os.path.join(_results_dir, "battle_reports", _battle_run_id)
```
  (`_results_dir` уже есть; если резолвится позже — поднять вычисление выше или передать в `_run_assignment`.)
- Передать `_battle_dir` в `_run_assignment` (доп. параметр или замыкание). Внутри `_merge_and_log(idx,
  result, ...)` после `_accumulate_episode_result`/`_write_blocks` добавить:
```python
        if getattr(result, "battle_report_md", None):
            from core.eval.battle_report import write_battle_report, update_index
            try:
                write_battle_report(_battle_dir, int(idx), result.battle_report_md)
                s = dict(result.battle_report_summary or {}); s["game_idx"] = int(idx)
                s["file"] = f"game_{int(idx):03d}.md"
                update_index(_battle_dir, s)
            except Exception as exc:
                log(f"[EVAL][BATTLE_REPORT][WARN] не записан отчёт игры {idx}: {exc}. "
                    f"Где: eval.py (_merge_and_log). Проверь права/путь {_battle_dir}.")
```
  Это покрывает ОБА пути (parallel и sequential), т.к. оба зовут `_merge_and_log`. Воркер уже возвращает
  `EpisodeResult` с `battle_report_md` (markdown picklable).

- [ ] **Step 1: Тест — _merge_and_log пишет файл+index** (можно юнит на хелпер записи отдельно, если
  `_merge_and_log` трудно изолировать: вызвать `write_battle_report`/`update_index` уже покрыты Task 6;
  здесь — лёгкий интеграционный smoke: запустить `main`-эквивалент короткого eval с 1 игрой и
  `EVAL_ACTION_TRACE=1`, проверить, что появился `artifacts/.../battle_reports/<run>/game_001.md` и
  `index.md`). Если полноценный `main` дорог — оформить как Task 9 smoke и здесь ограничиться ревью кода.
- [ ] **Step 2: Провал** (файлов нет).
- [ ] **Step 3: Внести запись по якорям.**
- [ ] **Step 4: Зелёно + регрессии** `pytest tests/eval -q`.
- [ ] **Step 5: Commit** `git commit -m "feat(eval): запись battle report файлов + index в _merge_and_log"`

---

## Task 9: Smoke — короткий eval с тумблером создаёт отчёт (лёгкий)

**Files:** Test `tests/eval/test_battle_report_writer.py` (добавить) или новый
`tests/eval/test_battle_report_smoke.py`.

- [ ] **Step 1: Тест** — построить минимальный env+агентов (как в `tests/eval`/`tests/models/test_eval_agent.py`:
  `build_env`, dqn-`_FixedDQN`/фабрика), `EVAL_ACTION_TRACE=1`, вызвать `run_episode` 1 раз, затем
  `write_battle_report(tmp, 1, result.battle_report_md)` и `update_index(...)`; проверить, что файл
  существует, содержит `# Battle Report`, `## Итог`, scoreboard-таблицу и обе стороны.
- [ ] **Step 2: Провал → Step 3: (уже реализовано) → Step 4: Зелёно.**
- [ ] **Step 5: Commit** `git commit -m "test(eval): smoke battle report"`
- Если smoke тяжёл по ОЗУ/времени (см. память про MuZero subset) — держать на DQN/коротком эпизоде,
  не гонять полный `main`.

---

## Self-review (архитектор)

- **Покрытие спеки:** §3 collector→T2–T4; §4 модель→T2; §5 формат→T5; §6 scoreboard→T4/T5;
  §7 интеграция (run_episode + оба пути)→T7/T8; §8 пути файлов→T6/T8; §9 тумблер→T7; §10 тесты→T1–T9;
  §2.2 нет reward→тест в T5 (`"reward" not in md`). Покрыто.
- **Плейсхолдеры:** в T7/T8 даны точные якоря и код; `_faction_for`/`eval_side_label`/`_safe_int` —
  существующие/локальные helper'ы eval.py (дирижёр уточняет точную форму при декомпозиции — это
  единственная зона детализации «КАК», допустимая дирижёру).
- **Согласованность типов:** `render_battle_report(record)`, `BattleReportCollector.record_side_actions/
  record_scoreboard/finish/to_record`, `write_battle_report(run_dir,idx,md)`, `update_index(run_dir,summary)`
  — имена едины во всех задачах.

## Решённые детали (проверено архитектором — НЕ открытые вопросы)

- `eval_side_label` импортирован в `eval.py` (стр.56) — использовать для model→P1/P2. ✓
- `_safe_int` определён в `run_episode` (стр.841) — доступен в хук-точках. ✓
- **`_faction_for(side)` — MVP-дефолт `"—"`.** Фракция в `run_episode` напрямую НЕ в scope
  (`roster_config` грузится только в worker-setup, стр.420). Чтобы не блокировать и не тащить
  roster_config в горячий путь: добавить локальный helper в `run_episode`
  ```python
  def _faction_for(_side: str) -> str:
      return "—"   # MVP: имя армии в шапке опускаем; юниты в нарративе несут «кто есть кто»
  ```
  Улучшение (реальные фракции из roster_config) — ВНЕ объёма этого плана.
- `battle_round` в `_model_half`/`_enemy_half` — `_info.get("battle round")`; если на старте раунда
  info ещё нет — `1`.

## Открытые риски (для дирижёра — при неясности СТОП, вопрос наверх)

1. Точные строки-якоря в `run_episode` могли сместиться от последующих коммитов — сверяй по
   содержимому (маркеры `[TRACE][ENEMY_ACTION]`, `[WH40K][BATTLESTATE]`, `return EpisodeResult(`),
   а не по номерам строк.
2. Все вызовы коллектора — строго под `if report_collector is not None`: при выключенном тумблере
   горячий путь eval НЕ должен меняться (проверить регрессией `pytest tests/eval -q`).
