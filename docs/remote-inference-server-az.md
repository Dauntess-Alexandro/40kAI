# Remote Inference Server (AZ) — руководство

**Версия:** v1
**Сценарий:** два ПК в одной LAN — learner + env workers на **ПК1**, GPU `net.infer` для AlphaZero tree на **ПК2**.

Дизайн: [`inference-server-az-design.md`](inference-server-az-design.md). Пошаговый гайд ПК2: [`pc2-remote-az-is-setup-guide.md`](pc2-remote-az-is-setup-guide.md).

> Отличие от GMZ remote: у AZ на ПК2 уходит только `net.infer` (priors+value).
> MCTS-дерево и env-rollout'ы остаются на ПК1. Порт по умолчанию **5556** (GMZ — 5555),
> можно держать оба сервера на одном ПК2.

---

## 1. Архитектура

| ПК | Роль |
|----|------|
| **ПК1** | Qt GUI, `train.py` (learner на GPU), CPU env workers (MCTS+env), пишет `latest_az_tree_policy.pth` |
| **ПК2** | `tools/az_remote_inference_server.py` — ZMQ ROUTER + `AZInferenceEngine` на GPU |

**Транспорт:** ZMQ DEALER (каждый воркер на ПК1) ↔ ROUTER (ПК2), msgpack + numpy bytes.
**Веса (v1):** только SMB — ПК2 читает `latest_az_tree_policy.pth` с общей папки.

```text
ПК1                              LAN                         ПК2
┌─────────────────────┐                                      ┌─────────────────────┐
│ Learner (GPU)       │                                      │ AZ Remote IS (GPU)  │
│ Env workers (CPU)   │─── infer req (ZMQ :5556) ───────────►│ net.infer (priors,  │
│ MCTS+env на CPU     │◄── priors + value ──────────────────│   value)            │
│ пишет .pth на диск  │                                      │ читает .pth по SMB  │
└─────────────────────┘                                      └─────────────────────┘
         │ SMB share: latest_az_tree_policy.pth
         └──────────────────────────────────────────────────────────► (Z:)
```

---

## 2. ПК2: быстрый старт

1. На ПК1: `tools\write_az_remote_search_cfg.bat` → создаст `runtime\state\az_remote_search_cfg.json` (+ копию в `actor_sync` для SMB). **Нужен хотя бы один checkpoint** (env_contract).
2. На ПК2: скопировать репозиторий, установить Python 3.12 + NVIDIA-драйвер.
3. На ПК1: расшарить `artifacts\models\actor_sync`; на ПК2 подключить как `Z:`.
4. На ПК2: запустить `tools\pc2_remote_az_is.bat` → создаст конфиг из примера, открыть в блокноте, заполнить пути (`Z:\latest_az_tree_policy.pth`, `Z:\az_remote_search_cfg.json`).
5. Запустить `tools\pc2_remote_az_is.bat` снова → сервер слушает:
   ```text
   [AZ][REMOTE_IS] listening on 0.0.0.0:5556 device=cuda:0
   ```

Режимы: `tools\pc2_remote_az_is.bat [setup|check]` (setup = venv+firewall, check = CUDA/zmq).

---

## 3. Конфиг ПК2 (`pc2_remote_az_is_config.bat`)

Из `pc2_remote_az_is_config.example.bat`. Ключевые поля:

| Переменная | Пример | Описание |
|------------|--------|----------|
| `AZ_REMOTE_WEIGHTS_PATH` | `Z:\latest_az_tree_policy.pth` | SMB-файл весов (learner на ПК1) |
| `AZ_REMOTE_INIT_WEIGHTS` | `C:\...\checkpoint_ep1.pth` | стартовый checkpoint, если на Z: ещё пусто |
| `AZ_REMOTE_SEARCH_CONFIG` | `Z:\az_remote_search_cfg.json` | obs_dim/action_sizes/арх |
| `AZ_REMOTE_PORT` | `5556` | TCP-порт |
| `AZ_REMOTE_DEVICE` | `cuda:0` | GPU |
| `AZ_REMOTE_BATCH_SIZE` | `32` | max batch (≥ num_env_workers × parallel_sims) |
| `AZ_REMOTE_BATCH_INTERVAL_MS` | `10` | окно сбора батча |
| `AZ_REMOTE_AUTH_TOKEN` | пусто | общий секрет (= GUI на ПК1) |

---

## 4. ПК1: запуск обучения

### Через env vars (без GUI)

```bat
set TRAIN_ALGO=alphazero_tree
set AZ_INFERENCE_SERVER=1
set AZ_INFERENCE_SERVER_MODE=remote
set AZ_INFERENCE_REMOTE_HOST=192.168.1.100
set AZ_INFERENCE_REMOTE_PORT=5556
set AZ_MCTS_MAX_DEPTH=1
python train.py ...
```

Перед стартом train делает health_check ПК2; если сервер недоступен — **train не стартует** с RU-ошибкой (v1).

### Проверка соединения вручную

```bat
.\.venv\Scripts\activate
python -c "from core.models.az_inference_transport import az_remote_health_check; print(az_remote_health_check(host='192.168.1.100', port=5556))"
```

---

## 5. Поведение v1 (ограничения)

| Правило | Поведение |
|---------|-----------|
| Синхронизация весов | Только SMB |
| IS недоступен при старте | Train **не** стартует |
| IS упал во время train | Train останавливается, без reconnect |
| Fallback на локальный IS | Нет |
| eval / play | Remote IS **не** поддерживается |

Throughput по LAN может быть ниже B-local. При `max_depth>1` — заметно ниже (round-trip на intermediate-evals).

---

## 6. Логи и отладка

| Где | Файл / маркер |
|-----|---------------|
| ПК2 | `runtime/logs/az_remote_is_<дата>.log`, `[AZ][REMOTE_IS]` |
| ПК1 | `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md`, `[AZ][REMOTE_CLIENT]` |

Частые ошибки:

| Симптом | Решение |
|---------|---------|
| `CUDA: False` на ПК2 | драйвер NVIDIA + `installer\install_deps.bat -y` |
| `Веса не найдены` | проверьте `Z:` / `AZ_REMOTE_INIT_WEIGHTS` |
| health_check failed с ПК1 | сервер запущен? firewall TCP 5556? верный IP? |
| `protocol_version mismatch` | одинаковая версия кода на ПК1/ПК2 |
| `obs_dim/action_sizes не определены` | сначала train (создаст checkpoint), затем `write_az_remote_search_cfg.bat` |

---

## 7. Ключевые файлы

| Файл | Назначение |
|------|------------|
| `tools/az_remote_inference_server.py` | сервер ПК2 |
| `tools/pc2_remote_az_is.bat` | одна кнопка ПК2 |
| `runtime/state/pc2_remote_az_is_config.example.bat` | шаблон конфига |
| `tools/write_az_remote_search_cfg.bat` | генерация search_cfg на ПК1 |
| `app/gui_qt/qml/components/AzInferenceServerPanel.qml` | панель ПК1 (Local/LAN, host/port/auth → `hyperparams.json` `alphazero_tree`) |
