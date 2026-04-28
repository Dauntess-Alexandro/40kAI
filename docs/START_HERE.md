# 40kAI — быстрый старт

## Установка
1. Установите Python 3.12+.
2. Создайте виртуальное окружение и установите зависимости:
   - `python -m venv .venv`
   - `.venv\Scripts\pip install -r requirements_windows.txt`

## Запуск
- GUI (основной сценарий): `python app/gui_qt/main.py`
- Train через bat: `train.bat`
- Eval через GUI вкладку `Оценка`
- Viewer через bat: `scripts/viewer.bat`

## Где что лежит
- Код GUI/Viewer: `app/`
- Core-логика/движок/RL: `core/`
- Конфиги: `configs/`
- Модели и метрики: `artifacts/models`, `artifacts/metrics`
- Runtime состояние и логи: `runtime/state`, `runtime/logs`
- Результаты eval: `artifacts/results/results.txt`

## Отладка
- train/eval лог: `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md`
- play/viewer лог: `runtime/logs/LOGS_FOR_AGENTS_PLAY.md`
