# Переменные окружения по режимам (GUI/Train/Самообучение/8x)

Источник: актуальные файлы GUI/скриптов/кода (`gui/Application.cpp`, `run_gui_manual.sh`, `play.sh`, `train.sh`, `train.py`).

## Игра в GUI (Play in GUI)
**Что включается сейчас через GUI:**
- `PLAY_NO_EXPLORATION=1`
- `FIGHT_REPORT=1`

**Где задаётся:** `gui/Application.cpp` (запуск через `./play.sh`).

**Дополнительно при ручном запуске GUI через скрипт:**
- `MANUAL_DICE=1` (если запускать `./run_gui_manual.sh`)

## Train (обычное обучение)
**Что включается сейчас через GUI:**
- нет дополнительных переменных (пустой префикс)

**Где задаётся:** `gui/Application.cpp` (кнопка «Обучение», запуск через `./train.sh`).

## Самообучение (Self-play)
**Что включается сейчас через GUI:**
- `SELF_PLAY_ENABLED=1`

**Где задаётся:** `gui/Application.cpp` (кнопка «Самообучение», запуск через `./train.sh`).

**Параметры самообучения в `train.py` (значения по умолчанию, если не заданы):**
- `SELF_PLAY_UPDATE_EVERY_EPISODES=50`
- `SELF_PLAY_OPPONENT_MODE=snapshot`
- `SELF_PLAY_FIXED_PATH=""`
- `SELF_PLAY_OPPONENT_EPSILON=0.0`

## Тренировать 8x
**Что включается сейчас через GUI:**
- `VEC_ENV_COUNT=8`

**Где задаётся:** `gui/Application.cpp` (кнопка «Тренировать 8x», запуск через `./train.sh`).

---

## Примечания
- `VERBOSE_LOGS` и `MANUAL_DICE` включаются в ручных режимах терминала (`launch_terminal_manual.sh`/`play_terminal_manual.sh`).
- Чтобы посмотреть, какие переменные реально активны в бою, смотри лог `[FIGHT][ENV]` в начале боевого раунда.
- Для нового формата состояния и рендера:
  - `STATE_V2=1` — экспорт `state.json` в формате v2 (через `GameStateV2`).
  - `RENDER_STATE_V2=1` — отложенное применение snapshot-ов в Viewer во время анимации юнитов.
