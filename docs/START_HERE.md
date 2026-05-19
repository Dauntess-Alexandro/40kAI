# 40kAI — быстрый старт

## Установка

### Вариант A: Install.exe (рекомендуется для Windows)
1. Готовый файл в корне репо: **`Install.exe`** (или соберите: `scripts\build_installer.bat`).  
   Подробно: [README.md](../README.md) · сборка: [installer/README.md](../installer/README.md)
2. Запустите `Install.exe` (нужен Python 3.12+ в PATH для онлайн-зависимостей).
3. В мастере можно включить **ярлык на рабочем столе**.
4. После установки: `C:\Program Files\40kAI\40kAI_GUI\40kAI_GUI.exe`

Повторный запуск `Install.exe` или `install_deps.bat` в каталоге установки обновляет пакеты; актуальные помечаются как **SKIP**.

### Вариант B: из исходников (разработка)
1. Установите Python 3.12+.
2. `installer\install_deps.bat` (меню GPU/CUDA) или `installer\install_deps.bat -y`
3. Активируйте `.venv` при необходимости.

## Запуск
- GUI (установленный): `40kAI_GUI\40kAI_GUI.exe` в каталоге установки
- GUI (из исходников): `python app/gui_qt/main.py` или `app\gui_qt\40k.bat`
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
