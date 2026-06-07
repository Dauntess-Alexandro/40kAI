---
name: run-40kai
description: Запуск обучения/оценки/игры 40kAI приоритетно через Qt GUI (по AGENTS.md), с терминальным фолбэком. Используй командой /run-40kai когда надо стартовать train, eval или Viewer.
disable-model-invocation: true
---

# run-40kai — запуск train / eval / play

Правило проекта (AGENTS.md): **приоритет — Qt GUI**, терминал — фолбэк.
Платформа Windows, PowerShell. Перед запуском должно быть активно окружение `.venv`.

## Аргумент
`/run-40kai <режим>` где режим: `gui` (по умолчанию) | `train` | `eval` | `play`.

---

## Режим `gui` (рекомендуется)
Запускает Qt GUI — оттуда стартуют train/eval, настраиваются миссия/гиперпараметры, видны логи.

```powershell
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD\core;$env:PYTHONPATH"
python -u app/gui_qt/main.py
```
Дальше: вкладки «Обучение» / «Оценка» / запуск Viewer — внутри GUI.

---

## Режим `train` (терминальный фолбэк)
Самый простой путь — готовый bat с дефолтами (AMP, compile, prefetch, NUM_ENVS=16):

```powershell
.\train.bat
```
Распределёнка (AlphaZero tree) — задаётся через окружение/`hyperparams.json` перед запуском:
```powershell
$env:AZ_DISTRIBUTED_ACTORS = "1"   # learner поднимет RolloutReceiver на :5557
# IS LAN: $env:AZ_INFERENCE_SERVER = "1"   (по умолчанию выкл — CPU акторы)
.\train.bat
```
Гиперпараметры — `hyperparams.json` (секции `alphazero_tree` и т.д.), reward — `reward_config.py`.

---

## Режим `eval` (терминальный фолбэк)
```powershell
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "$PWD\core;$env:PYTHONPATH"
python -u eval.py
```
Быстрая сверка итогов: `artifacts/results/results.txt`.

---

## Режим `play`
Игру смотреть через **Viewer внутри GUI** (режим `gui` → запуск Viewer).
Ручной терминальный путь — только при необходимости: `play_terminal_manual.bat`.

---

## TensorBoard (трекинг/визуализация обучения)
Во время обучения метрики пишутся в `runtime/tb/<algo>/<run_id>/` (эпизоды: reward/winrate/vp_diff;
лоссы/LR; телеметрия CPU/RAM/GPU). Смотреть — в отдельном терминале:
```powershell
.\.venv\Scripts\Activate.ps1
python -m tensorboard.main --logdir runtime/tb    # открой http://localhost:6006
```
Выключить логирование TB на прогон: `$env:TB_ENABLED = "0"` перед запуском train.
Старые CSV/PNG (`artifacts/metrics`, GUI) продолжают работать как раньше — TB добавлен рядом.

## После запуска
- Что-то пошло не так → скилл **`logs-triage`** (читаем `runtime/logs/LOGS_FOR_AGENTS_*.md`).
- Distributed: на ПК2 поднимается отдельно (`tools/pc2_remote_az_is.bat`) — см. AGENTS.md.
