# ПК2: установка AZ Remote Inference Server с нуля

Пошаговый гайд для второго ПК (GPU-инференс AlphaZero tree). Полное руководство:
[`remote-inference-server-az.md`](remote-inference-server-az.md).

## Что нужно

- Windows 10/11, NVIDIA GPU, `nvidia-smi` работает.
- Python 3.12+ (галочка **Add to PATH**).
- Тот же репозиторий 40kAI, что на ПК1 (одинаковая версия кода).
- LAN (Gigabit; Wi-Fi не рекомендуется).

## Шаги

### 1. ПК1: сгенерировать search_cfg
На ПК1 (после хотя бы одного train-чекпойнта):
```bat
tools\write_az_remote_search_cfg.bat
```
→ `runtime\state\az_remote_search_cfg.json` + копия в `artifacts\models\actor_sync\`.

### 2. ПК1: расшарить веса по SMB
1. ПКМ по `artifacts\models\actor_sync` → «Предоставить доступ» → пользователь с ПК2.
2. Узнать IP ПК2: `ipconfig` → IPv4 (например `192.168.1.100`).

### 3. ПК2: подключить сетевой диск
«Подключить сетевой диск» → `\\ИМЯ-ПК1\actor_sync` → буква `Z:`.
Проверить: на `Z:` видны `latest_az_tree_policy.pth` и `az_remote_search_cfg.json`.

### 4. ПК2: первый запуск
```bat
cd C:\40kAI
tools\pc2_remote_az_is.bat
```
- Создаст `runtime\state\pc2_remote_az_is_config.bat` и откроет блокнот.
- Заполнить: `AZ_REMOTE_WEIGHTS_PATH=Z:\latest_az_tree_policy.pth`,
  `AZ_REMOTE_SEARCH_CONFIG=Z:\az_remote_search_cfg.json`,
  при пустом Z: — `AZ_REMOTE_INIT_WEIGHTS=` локальный checkpoint.
- Сохранить, закрыть блокнот.

> **Единая переменная (как у акторов):** вместо явных путей можно задать
> `set 40KAI_SHARE_ROOT=\\PC1\40kai_models` и оставить `AZ_REMOTE_WEIGHTS_PATH`/
> `AZ_REMOTE_SEARCH_CONFIG` пустыми — лаунчер сам найдёт файлы (пробует `SHARE\actor_sync\…`
> и `SHARE\…`), с фолбэком на `Z:\`. Через GUI-лаунчер ПК2 переменная подставляется сама.

### 5. ПК1: запустить train
GUI: LAN Inference server + Distributed actors (ПК2). Или `distributed_actors_enabled=1` в hyperparams.

### 6. ПК2: установка + старт (IS + actors одной кнопкой)
В `pc2_remote_az_is_config.bat` задать **`AZ_DIST_PC1_HOST`** = IP ПК1, **`AZ_REMOTE_DIST_ACTORS_ENABLED=1`** (в example по умолчанию).
```bat
tools\pc2_remote_az_is.bat setup    REM venv + firewall :5555 (один раз)
tools\pc2_remote_az_is.bat          REM IS в отдельном окне + actors в этом
```
Ожидаемо: окно **40kAI AZ IS** → `listening on 0.0.0.0:5555`; в основном окне → `[AZ][DIST][PC2] spawning workers=...`  
На ПК1 в логе train: `[AZ][DIST][RECEIVER] hello worker=100`.  
Только IS без actors: `set AZ_REMOTE_DIST_ACTORS_ENABLED=0` в конфиге.

### 7. (устар.) отдельный pc2_az_actors.bat
Не нужен, если используете шаг 6. `pc2_az_actors.bat` = `actors-only` (IS уже запущен).

### 8. ПК1 (env vars, если без GUI)
Env vars (или GUI после реализации панели):
```bat
set TRAIN_ALGO=alphazero_tree
set AZ_INFERENCE_SERVER=1
set AZ_INFERENCE_SERVER_MODE=remote
set AZ_INFERENCE_REMOTE_HOST=192.168.1.100
set AZ_INFERENCE_REMOTE_PORT=5555
set AZ_MCTS_MAX_DEPTH=1
python train.py ...
```

## Чеклист готовности

**ПК2**
- [ ] `tools\pc2_remote_az_is.bat check` — CUDA и zmq OK
- [ ] `pc2_remote_az_is_config.bat` заполнен
- [ ] `Z:\latest_az_tree_policy.pth` или `AZ_REMOTE_INIT_WEIGHTS`
- [ ] `Z:\az_remote_search_cfg.json` есть
- [ ] `listening on 0.0.0.0:5555`
- [ ] `AZ_DIST_PC1_HOST` верный; на ПК1 открыт inbound **TCP 5557**
- [ ] В train: `hello worker=100+` (если distributed включён)

**ПК1**
- [ ] `az_remote_health_check` OK (или train стартует без ошибки health_check)

## Проблемы
См. таблицу «Частые ошибки» в [`remote-inference-server-az.md`](remote-inference-server-az.md#6-логи-и-отладка).
