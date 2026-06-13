# Дизайн: редизайн вкладки «Метрики эвристики» с интеграцией Phase 8

**Дата:** 2026-06-12  
**Статус:** approved  
**Затронутые файлы:** `app/gui_qt/qml/Main.qml`, `app/gui_qt/main.py`, новые файлы

---

## Контекст

Вкладка «Метрики эвристики» сейчас показывает только текст из `heuristicMetricsText`. Phase 8 добавила два CLI-инструмента (`heur_benchmark.py`, `heur_calibrate.py`), которые нужно запускать и отслеживать из GUI без открытия терминала.

---

## Что строим

Полный редизайн вкладки «Метрики эвристики»: три внутренние подвкладки вместо одного текстового блока.

---

## Структура UI

### Внутренние подвкладки
```
[ Сводка ] [ Бенчмарк ] [ Калибровка ]
```

Реализуются через QML `TabBar` + `StackLayout` внутри вкладки, не добавляя новую глобальную вкладку.

### Вкладка «Сводка» (редизайн текущей)
- Три stat-карточки вверху: **Winrate** / **Entropy** / **Draws**
- Ниже: метрики в строках (risk, fallback, charge success, mode usage, profiles)
- Добавляем новый Python property `heuristicMetricsDict: dict` в `controller` рядом с существующим `heuristicMetricsText`. Метод `_load_latest_heuristic_metrics()` дополняется: парсит уже загруженный JSON-файл метрик и складывает поля (winrate, draw_rate, style_entropy_norm, mode_totals, profile_outcomes и др.) в `self._heuristic_metrics_dict`. QML читает через `controller.heuristicMetricsDict`.

### Вкладка «Бенчмарк»
- Параметры: `Игр` (int input, default 30), `Оппонент` (combobox: `heuristic_auto`)
- Кнопка `▶ Запустить бенчмарк` / `■ Стоп` во время работы
- Статус-бар с результатом последнего прогона: `winrate=0.503  entropy=0.891  draws=2.1%`
- История последних 5 прогонов (in-memory ListModel): время, winrate, entropy, draws, игр

### Вкладка «Калибровка»
- Параметры: `Кандидатов` (default 40), `Игр/кандидат` (default 50), `Seed` (default 1390520)
- Кнопки: `▶ Калибровать` / `Dry run` / `■ Стоп` (visible во время работы)
- Прогресс-бар + счётчик `12 / 40 · ~22 мин · baseline: 0.812`
- **Живая таблица кандидатов** (ListModel, обновляется по мере завершения каждого):
  - Колонки: `#` / `score` / `winrate` / `entropy` / `draws` / `статус` (tag-ok/tag-bad + причина)
  - Лучший кандидат выделен цветом строки
- **Патч-блок** (показывается как только есть лучший):
  - Diff `reward_config.py` в стиле `+ KEY = new  # было old, Δ+delta`
  - Кнопки: `✓ Применить патч` / `Открыть файл` / `score_delta` справа

---

## Архитектура backend

### `HeurBenchmarkRunner(QObject)`
**Файл:** `app/gui_qt/heur_benchmark_runner.py`

Signals:
- `benchmarkStarted()`
- `benchmarkFinished(result: dict)` — winrate, entropy, draw_rate, games, run_id
- `benchmarkFailed(error: str)`

Methods:
- `run(games, opponent_policy)` — запускает `tools/heur_benchmark.py` как subprocess
- `stop()` — terminate subprocess

Реализация: `QThread` + `subprocess.Popen`; stdout читается построчно, результат парсится по завершении.

### `HeurCalibrateRunner(QObject)`
**Файл:** `app/gui_qt/heur_calibrate_runner.py`

Signals:
- `calibrationStarted(run_id: str)`
- `candidateResult(row: dict)` — эмитится при появлении новой строки в `candidates.jsonl`
- `calibrationFinished(summary: dict)` — best_candidate_idx, elapsed_sec, top_candidates
- `calibrationFailed(error: str)`
- `progressChanged(done: int, total: int)`

Methods:
- `run(candidates, games, seed, dry_run)` — запускает `tools/heur_calibrate.py`
- `stop()` — terminate + пишет стоп-флаг

Polling: `QTimer` раз в 2 сек читает `candidates.jsonl` и эмитит новые строки через `candidateResult`.

### Применение патча
Метод `apply_heur_patch(run_dir: str)` в `HeurCalibrateRunner`:
- Читает `best_reward_config_patch.md`, парсит блок ` ```python ``` `
- Для каждой строки `KEY = value  # ...` делает regex-замену в `reward_config.py`
- Эмитит `patchApplied(keys_changed: list)`

### Регистрация в `main.py`
```python
heur_benchmark_runner = HeurBenchmarkRunner()
heur_calibrate_runner = HeurCalibrateRunner()
engine.rootContext().setContextProperty("heurBenchRunner", heur_benchmark_runner)
engine.rootContext().setContextProperty("heurCalRunner", heur_calibrate_runner)
```

---

## QML

### Новый компонент
**Файл:** `app/gui_qt/qml/components/HeurMetricsPanel.qml`

Заменяет `Item` на строках 4195–4238 Main.qml. Main.qml вставляет:
```qml
HeurMetricsPanel { Layout.fillWidth: true; Layout.fillHeight: true }
```

Внутри: `TabBar` + `StackLayout` с тремя `Item`-ами (Сводка / Бенчмарк / Калибровка).

### Цвета и стиль
Следует существующей теме: `root.bgElevated`, `root.borderMuted`, `root.accentPrimaryAction` (#b88a26 золото для прогресса/лучшего), `root.accentP1` (#2f6ed8 для primary actions), `root.textSecondary`. Шрифт JetBrains Mono везде где моноширинные данные.

---

## Обработка ошибок

| Ситуация | Поведение |
|---|---|
| `eval.py` вернул ненулевой код | `benchmarkFailed` → красный статус-бар с текстом ошибки |
| Calibrate: первый кандидат упал | `calibrationFailed` → сообщение, кнопки сбрасываются |
| Calibrate: не-первый кандидат упал | строка в таблице со статусом `failed`, продолжаем |
| Применить патч: файл не найден | диалог с сообщением об ошибке |
| Стоп во время работы | subprocess.terminate(), прогресс сбрасывается, таблица остаётся |

---

## Тесты

- `tests/gui/test_heur_benchmark_runner.py` — юнит-тест runner'а с mock subprocess (patch applied, stop, failed signal)
- `tests/gui/test_heur_calibrate_runner.py` — тест polling: mock `candidates.jsonl` append → candidateResult signals
- `tests/gui/test_heur_patch_apply.py` — тест `apply_heur_patch`: читает тестовый `best_reward_config_patch.md`, проверяет что `reward_config.py` обновлён корректно

---

## Что не входит в скоуп

- Постоянное хранение истории бенчмарков между сессиями GUI (файлы `summary.json` уже пишутся инструментом)
- Редактор весов через GUI (только применение готового патча)
- Запуск калибровки с ПК2 / remote
