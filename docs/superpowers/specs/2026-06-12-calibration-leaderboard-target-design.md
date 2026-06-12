# Дизайн: редизайн «Калибровка» (лидерборд) + настраиваемый target winrate

**Дата:** 2026-06-12
**Статус:** approved
**Затронуто:** `tools/heur_calibrate.py`, `tools/heur_benchmark.py` (только если нужно), `app/gui_qt/heur_calibrate_runner.py`, `app/gui_qt/qml/components/HeurMetricsPanel.qml`, тесты.

---

## Контекст

Вкладка «Калибровка» показывает кандидатов плоской таблицей в порядке появления. score-функция жёстко настроена на сбалансированного врага (target winrate 0.50): winrate>0.56 отклоняется. Пользователь хочет (1) уметь задавать цель (в т.ч. «максимально сильный враг»), (2) более «прикольный» лидерборд-вид.

---

## Часть 1 — настраиваемый `target_winrate`

Новый параметр `target_winrate ∈ (0,1]`, по умолчанию **0.50** (полностью воспроизводит текущее поведение).

### `score_candidate(metrics, target_winrate=0.50)`
```
score = 1.00 * min(winrate, target_winrate + 0.04)
      - 0.50 * abs(winrate - target_winrate)
      - 0.70 * max(0, draw_rate - 0.015)
      - 1.50 * invalid_rate
      - 0.60 * max(0, 0.86 - entropy)
      - 0.25 * max(0, hold_ratio - 0.62)
      - 0.15 * fallback_rate
```
- target=0.50 → идентично текущему (cap 0.54, штраф |w−0.5|).
- target=1.0 → `min(w,1.04)=w`, `−0.5·|w−1|=−0.5(1−w)` ⇒ `score_w = 1.5w − 0.5`, монотонно растёт с winrate.

### `reject_reasons(metrics, requested_games, target_winrate=0.50)`
Без изменений, кроме верхнего порога winrate:
- `winrate > target_winrate + 0.06` ⇒ reject, **но только если `target_winrate < 0.95`** (в режиме «Максимум» верхний reject отключён).
- Остальные guardrail без изменений: `actual_games != requested`, `invalid_rate > 0.001`, `style_entropy_norm < 0.84`, `draw_rate > 0.03`, `fallback_rate > 0.02`.

### `acceptance_reasons(metrics, baseline_score, target_winrate=0.50)`
Право кандидата стать «лучшим» (`not acceptance_reasons`):
- `score <= baseline_score` ⇒ reason.
- `style_entropy_norm < 0.86` ⇒ reason.
- `draw_rate > 0.02` ⇒ reason.
- Окно winrate **только при `target_winrate < 0.95`**: `not (target−0.04 ≤ winrate ≤ target+0.04)` ⇒ reason. В «Максимум» окна нет (лучший = макс. score среди качественных).

### Плумбинг
- `tools/heur_calibrate.py`: аргумент `--target-winrate` (float, default 0.50); прокинуть в score/reject/accept и в `summary_payload["target_winrate"]`.
- `HeurCalibrateRunner.run(...)`: новый параметр `target_winrate: float` → `--target-winrate`.
- Пресеты в GUI: Спарринг=0.50, Хард=0.65, Максимум=1.0, + ручной ввод (0..1).

`heur_benchmark.py` не трогаем (там winrate считается для стороны эвристики, target — это уже логика калибровки).

---

## Часть 2 — QML лидерборд

### Параметры (как есть): Кандидатов / Игр / Seed / Learner-агент.

### НОВОЕ — «Режим цели»
Ряд: 3 чипа-пресета (`Спарринг 0.50` золото-актив, `Хард 0.65`, `Максимум`) + поле «свой» (TextField 0..1, перебивает пресет). Подпись справа: «цель winrate = X · эвристика на стороне Y». Свойство панели `targetWinrate` (real); чип/поле его задают.

### Лидерборд (вместо плоской таблицы)
- Источник — `candidatesModel` (ListModel), но **живо сортируется по score по убыванию** при каждом `candidateResult`.
- Реализация сортировки: панель держит JS-массив `_rows`; на каждый `candidateResult` — push, сортировка по score (нечисловой score/«…» — в конец), затем перестроение `candidatesModel` (≤40 строк — дёшево).
- Строка: медаль ранга (1=#b88a26, 2=#9aa7b8, 3=#a06a3a, далее — номер места приглушённо), **score + мини-бар** (ширина ∝ score), winrate, entropy (цвет по порогам 0.86/0.84), draws, статус-пилюля. Лучший (★, по `bestCandidateIdx`) — зелёная подсветка строки; reject — приглушены.
- Заголовок столбцов: `место / score / winrate / entropy / draws / статус`.

### Патч-блок — как сейчас (кнопка уже починена в предыдущем коммите).

---

## Тесты
- `tests/tools/test_heur_target_winrate.py`:
  - `score_candidate(target=0.50)` == старое значение на фикстуре; `target=0.65` сдвигает максимум; `target=1.0` монотонно растёт с winrate.
  - `reject_reasons`: при target=0.65 отклоняет `winrate>0.71`, не отклоняет 0.60; при target=1.0 нет верхнего winrate-reject.
  - `acceptance_reasons`: окно сдвигается с target; при target=1.0 окна winrate нет.
- `tests/gui/test_heur_calibrate_runner.py` (дополнить): `run()` принимает `target_winrate` и есть `--target-winrate` в коде.
- `tests/gui/test_heur_metrics_panel_contract.py` (дополнить): есть «Режим цели»/target, чипы пресетов, функция сортировки лидерборда, медаль/ранг.

## Что не входит
- Изменение самого `eval.py` / движка.
- Сохранение истории прогонов между сессиями.
- Scatter-график (вариант B) — отклонён в пользу лидерборда.
