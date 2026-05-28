# Remote Inference Server (GMZ) — руководство

**Версия:** v1  
**Сценарий:** два ПК в одной LAN — learner + env workers на **ПК1**, GPU-инференс (MCTS/search) на **ПК2**.

Связанный дизайн B-local: `docs/inference-server-gmz-design.md` (§15 Remote).

---

## Содержание

1. [Архитектура](#1-архитектура)
2. [ПК2: быстрый старт (`tools\pc2_remote_is.bat`)](#2-пк2-быстрый-старт-toolspc2_remote_isbat)
3. [ПК2: что установить вручную](#3-пк2-что-установить-вручную)
4. [Конфиг ПК2 (`pc2_remote_is_config.bat`)](#4-конфиг-пк2-pc2_remote_is_configbat)
5. [Сеть и SMB](#5-сеть-и-smb)
6. [Файл `search_cfg.json`](#6-файл-search_cfgjson)
7. [Запуск сервера вручную (без bat)](#7-запуск-сервера-вручную-без-bat)
8. [ПК1: GUI и обучение](#8-пк1-gui-и-обучение)
9. [Поведение v1 (ограничения)](#9-поведение-v1-ограничения)
10. [Отладка и логи](#10-отладка-и-логи)
11. [Частые ошибки](#11-частые-ошибки)
12. [Чеклист готовности](#12-чеклист-готовности)
13. [Ключевые файлы](#13-ключевые-файлы)

---

## 1. Архитектура

| ПК | Роль |
|----|------|
| **ПК1** | Qt GUI, `train.py` (learner на GPU), CPU env workers, запись `latest_gmz_policy.pth` |
| **ПК2** | `tools/gmz_remote_inference_server.py` — ZMQ ROUTER + `GMZInferenceServer` на GPU |

**Транспорт:** ZMQ DEALER (каждый env worker на ПК1) ↔ ROUTER (сервер на ПК2), **msgpack** + numpy bytes.  
**Веса (v1):** только **SMB** — сервер на ПК2 читает `artifacts/models/actor_sync/latest_gmz_policy.pth` с общей папки.

На ПК2 **не** нужны: запуск train, eval, play, Qt GUI.

```text
ПК1                              LAN                         ПК2
┌─────────────────────┐                                      ┌─────────────────────┐
│ Learner (GPU)       │                                      │ Remote IS (GPU)     │
│ Env workers (CPU)   │─── InferRequest (ZMQ :5555) ────────►│ MCTS / search       │
│ пишет .pth на диск  │◄── InferResponse ───────────────────│ читает .pth по SMB  │
└─────────────────────┘                                      └─────────────────────┘
         │ SMB share: latest_gmz_policy.pth
         └──────────────────────────────────────────────────────────► (то же на Z:)
```

---

## 2. ПК2: быстрый старт (`tools\pc2_remote_is.bat`)

Один скрипт в репозитории делает почти всё за вас: зависимости, firewall, проверку CUDA и запуск сервера.

**Файл:** `C:\40kAI\tools\pc2_remote_is.bat`  
**Конфиг (создаётся при первом запуске):** `runtime\state\pc2_remote_is_config.bat`  
**Шаблон конфига (в git):** `runtime\state\pc2_remote_is_config.example.bat`

### Что нужно до первого запуска

| # | Действие |
|---|----------|
| 1 | Установить **Python 3.12+** ([python.org](https://www.python.org/downloads/)), галочка **Add to PATH** |
| 2 | Скопировать на ПК2 **тот же репозиторий 40kAI**, что на ПК1 (git clone или копия папки) |
| 3 | Установить **драйвер NVIDIA**, проверить `nvidia-smi` |
| 4 | На ПК1 расшарить папку с весами; на ПК2 подключить сетевой диск (например `Z:`) — см. [§5](#5-сеть-и-smb) |
| 5 | Создать **`search_cfg.json`** (как на ПК1) — см. [§6](#6-файл-search_cfgjson) |
| 6 | При необходимости скопировать с ПК1 **checkpoint** для первого старта (`checkpoint_ep*.pth`) |

### Первый запуск (настройка)

1. Двойной клик по **`tools\pc2_remote_is.bat`**  
   (или из cmd: `cd C:\40kAI` → `tools\pc2_remote_is.bat`)

2. Скрипт создаст `runtime\state\pc2_remote_is_config.bat` и откроет **блокнот**.

3. В блокноте укажите (минимум):
   - `GMZ_REMOTE_WEIGHTS_PATH` — путь к SMB-файлу, например `Z:\latest_gmz_policy.pth`
   - `GMZ_REMOTE_SEARCH_CONFIG` — путь к JSON, например `C:\40kAI\runtime\state\gmz_remote_search_cfg.json`
   - `GMZ_REMOTE_INIT_WEIGHTS` — локальный checkpoint, если на `Z:` ещё нет файла

4. **Сохраните** конфиг и закройте блокнот.

5. Снова запустите **`tools\pc2_remote_is.bat`**.

6. При первом полном запуске скрипт:
   - вызовет `installer\install_deps.bat -y` (создаст `.venv`, PyTorch+CUDA, pyzmq, msgpack) — **5–20 минут**;
   - при `GMZ_REMOTE_SETUP_FIREWALL=1` добавит правило Windows Firewall на порт;
   - проверит `torch.cuda`, `zmq`, `msgpack`;
   - запустит remote inference server.

7. В консоли должно появиться:

   ```text
   [GMZ][REMOTE_IS] listening on 0.0.0.0:5555 device=cuda
   ```

8. Окно **не закрывайте** — пока оно открыто, сервер работает. Остановка: **Ctrl+C**.

### Каждый следующий раз (одна кнопка)

Двойной клик **`tools\pc2_remote_is.bat`** — если `.venv` уже есть, сразу проверка и старт сервера.

### Режимы (аргументы)

Запуск из `C:\40kAI`:

| Команда | Когда использовать |
|---------|-------------------|
| `tools\pc2_remote_is.bat` | Обычный запуск: setup при необходимости + сервер |
| `tools\pc2_remote_is.bat setup` | Только установка `.venv` + firewall, без сервера |
| `tools\pc2_remote_is.bat check` | Только проверка Python / CUDA / zmq, без сервера |

### Что делает bat внутри (кратко)

1. Переходит в корень репо (`tools\` → `..`).
2. Читает `runtime\state\pc2_remote_is_config.bat`.
3. Проверяет наличие `search_cfg.json` и путей к весам.
4. Если нет `.venv` → `installer\install_deps.bat -y`.
5. Активирует `.venv`, проверяет импорты.
6. Запускает `tools\gmz_remote_inference_server.py` с параметрами из конфига.

Логи сервера: `runtime\logs\gmz_remote_is_<дата>.log`.

---

## 3. ПК2: что установить вручную

Если не используете bat, или нужно переустановить окружение:

### Железо

- Windows 10/11, NVIDIA GPU (например RTX 2060 Super 8 GB)
- LAN (Gigabit; Wi‑Fi не рекомендуется)
- ~5–15 GB на диск

### Зависимости

```bat
cd C:\40kAI
installer\install_deps.bat -y
```

Проверка:

```bat
.\.venv\Scripts\activate
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
python -c "import zmq, msgpack; print('OK')"
```

| Пакет | Зачем на ПК2 |
|-------|----------------|
| `torch` + CUDA | Инференс на GPU |
| `pyzmq` | Сеть ZMQ |
| `msgpack` | Сериализация запросов |
| `numpy`, `scipy` | Модель и search |
| PySide6, gym… | Ставятся с полным `requirements_windows.txt`, для сервера не используются |

---

## 4. Конфиг ПК2 (`pc2_remote_is_config.bat`)

Локальный файл, **не коммитится** (см. `.gitignore`). Создаётся из `pc2_remote_is_config.example.bat`.

| Переменная | Пример | Описание |
|------------|--------|----------|
| `GMZ_REMOTE_WEIGHTS_PATH` | `Z:\latest_gmz_policy.pth` | SMB-путь к файлу, который learner обновляет на ПК1 |
| `GMZ_REMOTE_INIT_WEIGHTS` | `C:\40kAI\artifacts\models\gumbel_muzero\checkpoint_ep1.pth` | Стартовый checkpoint, если на SMB файла ещё нет. Можно оставить пустым, если SMB-файл уже есть |
| `GMZ_REMOTE_SEARCH_CONFIG` | `C:\40kAI\runtime\state\gmz_remote_search_cfg.json` | JSON с `obs_dim`, `action_sizes`, MCTS — **должен совпадать с ПК1** |
| `GMZ_REMOTE_HOST` | `0.0.0.0` | На каком интерфейсе слушать (обычно все) |
| `GMZ_REMOTE_PORT` | `5555` | TCP-порт (тот же, что в GUI на ПК1) |
| `GMZ_REMOTE_DEVICE` | `cuda:0` | GPU для инференса |
| `GMZ_REMOTE_BATCH_SIZE` | `10` | Размер batch (8–12 для 8 GB VRAM) |
| `GMZ_REMOTE_BATCH_INTERVAL_MS` | `20` | Окно сбора batch (мс) |
| `GMZ_REMOTE_SYNC_INTERVAL` | `0.5` | Как часто проверять новый `.pth` по SMB (сек) |
| `GMZ_REMOTE_COMPILE` | `1` | `1` = включить `torch.compile` на CUDA |
| `GMZ_REMOTE_AUTH_TOKEN` | пусто | Опционально; если задан — тот же токен в GUI на ПК1 |
| `GMZ_REMOTE_SETUP_FIREWALL` | `1` | `1` = bat добавит правило firewall на `GMZ_REMOTE_PORT` |

После правки конфига перезапустите `tools\pc2_remote_is.bat`.

---

## 5. Сеть и SMB

### Firewall на ПК2

Bat делает это сам при `GMZ_REMOTE_SETUP_FIREWALL=1`. Вручную:

```bat
netsh advfirewall firewall add rule name="40kAI Remote IS" dir=in action=allow protocol=TCP localport=5555
```

### IP ПК2 (для GUI на ПК1)

На ПК2: `ipconfig` → IPv4 (например `192.168.1.100`).

### SMB

**ПК1 пишет:** `C:\40kAI\artifacts\models\actor_sync\latest_gmz_policy.pth`

**Шаги:**

1. ПК1: ПКМ по папке `actor_sync` → «Предоставить доступ» → пользователь с ПК2.
2. ПК2: «Подключить сетевой диск» → `\\ИМЯ-ПК1\share` → буква `Z:`.
3. В конфиге ПК2: `GMZ_REMOTE_WEIGHTS_PATH=Z:\latest_gmz_policy.pth`.

Сервер не качает веса по HTTP — только читает файл с диска каждые ~0.5 с.

---

## 6. Файл `search_cfg.json`

Обязателен. Поля должны **совпадать с ПК1** (ростер, миссия, preset GMZ).

Пример `runtime\state\gmz_remote_search_cfg.json`:

```json
{
  "obs_dim": 512,
  "action_sizes": [12, 8, 6],
  "latent_dim": 256,
  "hidden_dim": 256,
  "num_layers": 2,
  "action_embed_dim": 64,
  "num_simulations": 32,
  "root_top_k": 8,
  "discount": 0.997,
  "temperature": 0.15,
  "gumbel_scale": 1.0,
  "prior_weight": 0.25,
  "batch_recurrent": 1,
  "tree_reuse": 1
}
```

**Откуда взять:** настройки GMZ на ПК1 (Heavy/Balanced). `obs_dim` / `action_sizes` — из контракта среды; при ошибках infer сверьте с рабочим B-local на одном ПК.

---

## 7. Запуск сервера вручную (без bat)

```bat
cd C:\40kAI
.\.venv\Scripts\activate

python tools\gmz_remote_inference_server.py ^
  --host 0.0.0.0 ^
  --port 5555 ^
  --device cuda:0 ^
  --weights-path Z:\latest_gmz_policy.pth ^
  --init-weights C:\40kAI\artifacts\models\gumbel_muzero\checkpoint_ep1.pth ^
  --search-config C:\40kAI\runtime\state\gmz_remote_search_cfg.json ^
  --sync-method smb ^
  --sync-interval 0.5 ^
  --batch-size 10 ^
  --batch-interval-ms 20 ^
  --compile
```

Остановка: **Ctrl+C**.

### HealthCheck

```bat
.\.venv\Scripts\activate
python -c "from core.models.gmz_inference_transport import remote_health_check; print(remote_health_check(host='127.0.0.1', port=5555))"
```

С ПК1 замените host на IP ПК2.

---

## 8. ПК1: GUI и обучение

Inference Server настраивается в **Настройки → Hyperparams → Gumbel MuZero** (панель сверху, не в presets): ползунки **Local** и **LAN** (подсказки при наведении).

**По умолчанию (один ПК):** Local включён (при CUDA), LAN выключен. LAN сохраняется только если вы **сами** включили ползунок LAN (`user_enabled_lan` в `remote_is.json`).

### Один ПК (локальный IS)

1. **Настройки → Gumbel MuZero** → **Local Inference server** — включить (при CUDA по умолчанию рекомендуется).
2. **LAN Inference server** — выключен.
3. Сохранить hyperparams.
4. **Главная** → GUMBEL MUZERO → начать обучение.

### Два ПК (remote IS)

Порядок **после** `tools\pc2_remote_is.bat` на ПК2:

1. **LAN Inference server** — включить (Local выключится автоматически).
2. **Хост** = IP ПК2, **порт** = 5555.
3. **Проверить соединение** → OK.
4. **Главная** → GMZ → начать обучение.

Remote не сбрасывается при смене preset GMZ.

Конфиг GUI (ПК1): `runtime\state\remote_is.json` (в `.gitignore`).

### Env vars (без GUI)

```bat
set GMZ_INFERENCE_SERVER_MODE=remote
set GMZ_INFERENCE_REMOTE_HOST=192.168.1.100
set GMZ_INFERENCE_REMOTE_PORT=5555
set GMZ_INFERENCE_SERVER=1
set GMZ_ACTOR_DEVICE=inference_server
```

---

## 9. Поведение v1 (ограничения)

| Правило | Поведение |
|---------|-----------|
| Синхронизация весов | Только SMB |
| IS недоступен при старте train | Train **не** стартует |
| IS упал во время train | Train **останавливается**, без reconnect |
| Fallback на локальный IS | **Нет** |
| eval / play | Remote IS **не** поддерживается |

Throughput может быть на **5–15% ниже**, чем B-local на одной GPU — нормально для LAN.

---

## 10. Отладка и логи

| Где | Файл |
|-----|------|
| ПК2 | `runtime/logs/gmz_remote_is_<дата>.log` |
| ПК2 (справка) | `runtime/logs/LOGS_FOR_AGENTS_REMOTE_IS.md` |
| ПК1 | `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md` — `[GMZ][REMOTE_CLIENT]` |

Маркеры: `[GMZ][REMOTE_IS]`, `[GMZ][REMOTE_CLIENT]`, `[GMZ][REMOTE_CLIENT][CONN]`.

---

## 11. Частые ошибки

| Симптом | Решение |
|---------|---------|
| При первом запуске bat сразу закрылся с блокнотом | Норма: заполните конфиг и запустите снова |
| `CUDA: False` | Драйвер NVIDIA + `installer\install_deps.bat -y` |
| `search_cfg не найден` | Создайте JSON, путь в `GMZ_REMOTE_SEARCH_CONFIG` |
| `Нет файла весов` | SMB / `GMZ_REMOTE_INIT_WEIGHTS` |
| Connection refused с ПК1 | Сервер запущен? Firewall? Верный IP? |
| `protocol_version mismatch` | Одинаковая версия кода на ПК1 и ПК2 |
| Train упал mid-run | IS на ПК2 упал — перезапустить `tools\pc2_remote_is.bat` и train |
| Странный infer | Неверный `search_cfg.json` |

---

## 12. Чеклист готовности

**ПК2**

- [ ] Python 3.12+, репозиторий 40kAI = версия ПК1
- [ ] `tools\pc2_remote_is.bat check` — CUDA и zmq OK
- [ ] `pc2_remote_is_config.bat` заполнен
- [ ] `gmz_remote_search_cfg.json` создан
- [ ] SMB `Z:\latest_gmz_policy.pth` или `GMZ_REMOTE_INIT_WEIGHTS`
- [ ] `tools\pc2_remote_is.bat` → `listening on 0.0.0.0:5555`

**ПК1**

- [ ] Настройки → GMZ → LAN Inference server → HealthCheck OK
- [ ] GMZ variant B
- [ ] Train стартует

---

## 13. Ключевые файлы

| Файл | Назначение |
|------|------------|
| `tools/pc2_remote_is.bat` | Одна кнопка на ПК2 |
| `runtime/state/pc2_remote_is_config.example.bat` | Шаблон конфига |
| `runtime/state/pc2_remote_is_config.bat` | Ваш конфиг (gitignore) |
| `tools/gmz_remote_inference_server.py` | Python-сервер |
| `runtime/state/remote_is.json` | Конфиг remote на ПК1 (gitignore) |
| `app/gui_qt/qml/components/GmzInferenceServerPanel.qml` | Панель IS в настройках GMZ |
