# Таблица стратагем в eval (только DQN-модель) — дизайн

Дата: 2026-06-24
Статус: согласован заказчиком

## Цель

По прогону eval (N игр) построить подробную таблицу применения стратагем **обучаемой
стороны (DQN-модель, `env_side==model`)** и сохранить её в `artifacts/results/` в форматах
Markdown + CSV, плюс краткая сводка в eval-лог.

Задача возникла из ревью train-прогона 1000 игр: per-stratagem агрегация по всему прогону
отсутствовала (были только тоталы), train-лог не содержит `attempts`/`miss`, а данные мешали
обе стороны. В eval-прогоне `attempts`/`miss` логируются и линии тегированы `env_side`, поэтому
чистая таблица по модели достижима.

## Не-цели (YAGNI)

- Разбивка по сторонам/цветам (swap) — нет; считаем только `env_side==model`.
- Причинно-следственный анализ — нет; WR-связь подаётся как корреляция с явной оговоркой.
- Графики/визуализация — нет; только таблица (MD+CSV) и строка в логе.
- Поддержка других алгоритмов специально не делается, но т.к. парсинг трейса алго-агностичен,
  фича работает для любого eval без доп. усилий.

## Источники данных (факты из кода)

- `eval.py`, цикл прогона N игр (вокруг `eval.py:1427`): на каждую игру `run_episode(...)`
  возвращает `winner`, `end_reason`, `vp_diff`, …, `trace_lines`.
- Трейс-линии стратагем (из `core/telemetry/stratagem_trace.py`):
  - `[WH40K][STRATAGEM][ATTEMPT] step=.. side=.. env_side=model|enemy stratagem=<sid> unit=.. source=..`
  - `[WH40K][STRATAGEM] applied=<sid> side=.. env_side=model|enemy unit=.. phase=.. round=.. cp_before=.. cp_after=..`
  - `[WH40K][STRATAGEM][MISS] step=.. side=.. env_side=model|enemy attempted=<sid> unit=.. source=.. reason=..`
- Текущий парсер (`eval.py:1477-1488`) уже считает per-sid `strat_attempt_{sid}` /
  `strat_applied_{sid}`, но: (а) не фильтрует `env_side`, (б) miss только тоталом, (в) нет
  per-эпизодного джойна с исходом.

## Архитектура (компоненты)

### 1. Парсер per-side per-sid (правка `eval.py`)
- Фильтр: учитывать линии только при `env_side=model`.
- Per-sid счётчики для **attempt, applied, miss** (miss-sid берётся из `attempted=<sid>`).
- Регэксп для `env_side` и для `attempted=` (miss).

### 2. Per-эпизодный джойн с исходом (правка `eval.py`)
- На каждый эпизод: множество sid, применённых моделью (`applied`, `env_side=model`), и `winner`.
- Накапливать по всему прогону:
  - `games_total`, `wins_total`;
  - `games_used[sid]` — в скольких играх sid применялся ≥1 раз моделью;
  - `wins_used[sid]` — из них победных.
- Отсюда: WR_used = wins_used/games_used; WR_notused = (wins_total−wins_used)/(games_total−games_used);
  ΔWR = WR_used − WR_notused (если обе группы непусты, иначе «—»).

### 3. Модуль-репортер `core/telemetry/stratagem_report.py` (новый)
- Чистая функция (без I/O игр), вход — агрегаты, выход — структура строк + Markdown + CSV.
- Колонки: `stratagem, attempts, applied, miss, apply_rate_pct, applied_per_game,
  games_used, pct_games, wr_used, wr_notused, dwr`.
- `apply_rate_pct = applied/attempts*100` (если attempts==0 → «—»).
- Пустой ввод → корректная пустая таблица, без падения.
- Сортировка строк по `applied` убыв.

### 4. Запись файлов (правка `eval.py`, конец прогона)
- `artifacts/results/stratagem_eval_<run_id или timestamp>.md` и `.csv`.
- Шапка отчёта: модель/agent_id, число игр, overall winrate, дата, **оговорка про корреляцию**.
- Краткая сводка в лог: `[EVAL][STRATAGEM_TABLE] games=.. wr=.. file=..`.

## Обработка ошибок

- Нет стратагемных линий в трейсе → файлы создаются с пустой таблицей и пометкой «нет данных»;
  лог поясняет почему (трейс выключен / стратагемы не применялись).
- Деление на ноль (attempts==0, группа пуста) → «—», не исключение.
- Сообщения об ошибках по AGENTS.md: что случилось + где + что делать дальше; язык — русский.

## Тестирование (TDD, тесты до кода)

- `tests/core/telemetry/test_stratagem_report.py`:
  - корректные apply_rate_pct, pct_games, dwr на синтетических агрегатах;
  - пустой ввод → пустая таблица;
  - attempts==0 / пустая группа → «—» вместо краха;
  - сортировка по applied.
- `tests/eval/test_eval_stratagem_table.py`: парсер на мок-трейс-линиях правильно фильтрует
  `env_side=model` (игнорит enemy), разносит per-sid attempt/applied/miss, и per-эпизодный
  джойн с исходом считает games_used/wins_used корректно.
- Smoke (ручной/быстрый): eval на 5-10 играх создаёт `.md` и `.csv`, модель-сторона непустая.

## Definition of Done

1. Тесты (репортер + парсер) написаны до кода и зелёные.
2. Фича собрана, smoke на 5-10 играх создаёт оба файла.
3. Исполнитель прогоняет реальный eval **1000 игр** DQN-агентом
   `P1_Necrons_only_war_v2_final_ep1000_20260623_192723` через `--learner-agent-id`
   (не `--model .pth`), ~14 мин.
4. Заполненные `artifacts/results/stratagem_eval_*.md` и `.csv` на месте, таблица непустая.
5. ruff чистый; коммит только релевантного кода (без runtime-логов).

## Открытые риски

- `run_id` в eval может отличаться от train-овского; если недоступен — fallback на timestamp в имени файла.
- Объём trace_lines на 1000 играх — парсинг построчный, уже существующий путь; доп. памяти не вводим
  (агрегаты — Counter-ы, не храним сырые линии).
