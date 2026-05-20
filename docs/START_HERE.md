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
- **Windows + QML-панели:** если доска чёрная или консоль спамит `D3D11` / `QOpenGLWidget`, по умолчанию viewer выставляет `QSG_RHI_BACKEND=opengl` до загрузки Qt; переопределение: env `VIEWER_QSG_RHI_BACKEND` (например `d3d11`, `vulkan`, `opengl`).

## Где что лежит
- Код GUI/Viewer: `app/`
- Core-логика/движок/RL: `core/`
- Конфиги: `configs/`
- Модели и метрики: `artifacts/models`, `artifacts/metrics`
- Runtime состояние и логи: `runtime/state`, `runtime/logs`
- Результаты eval: `artifacts/results/results.txt`
- План модернизации viewer (QML-hybrid): `docs/viewer_migration_plan.md`, контракт состояния: `docs/viewer_state_contract.md`
- Общие цвета UI: `theme/tokens.json` (лаунчер всегда; viewer — флаг `viewer.theme.v2` в `app/viewer/viewer_config.json` или env `VIEWER_FLAG_VIEWER_THEME_V2=1`)
- ViewerController (миграция Sprint 3): флаг `viewer.controller.v1` в том же JSON или env `VIEWER_FLAG_VIEWER_CONTROLLER_V1=1`
- Модульные слои доски Sprint 4 (`ground` / `grid` / `objectives` / `labels`): код в `app/viewer/rendering/`; флаг `viewer.render.layers_v2`; для замера времени слоя в консоли задайте env `VIEWER_LAYER_MS=1`
- Sprint 5 — почти полный стек слоёв доски в `app/viewer/rendering/layers/` (в т.ч. terrain props, decals при `render_decals`, hover/tooltip оверлеи, platform FX, squad HUD, damage popups, AI badge); координатный hit-test: `ViewerController.hitTestBoard(x,y)` → `{kind, side, unitId}`; зелёные hitbox при `viewer.debug.overlay` или `VIEWER_DEBUG=1`; счётчик отрисовок и маркер последнего клика — при `viewer.debug.overlay`

## Отладка
- train/eval лог: `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md`
- play/viewer лог: `runtime/logs/LOGS_FOR_AGENTS_PLAY.md`
