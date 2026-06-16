# ПК2: установка GAZ Remote Inference Server (пошагово)

Цель: поднять на ПК2 GPU inference-сервер для Gumbel AlphaZero (порт **5565**), опционально с
distributed-акторами (rollout → ПК1 :5567). Запуск — через **pc2 launcher.bat** (роль
«Gumbel AlphaZero inference server») или напрямую `tools\pc2_remote_gaz_is.bat`.

Общая логика — как у AZ (`docs/pc2-remote-az-is-setup-guide.md`); ниже отличия GAZ.

## 0. Предпосылки

- ПК2: Windows, Python 3.12+ в PATH, NVIDIA GPU + драйвер.
- Общая папка ПК1 смонтирована на ПК2 (например `Z:` = `artifacts\models` или `actor_sync`).
- Репозиторий 40kAI на ПК2 (тот же код, что на ПК1).

## 1. Конфиг

1. Запустите один раз `tools\pc2_remote_gaz_is.bat config` — создастся
   `runtime\state\pc2_remote_gaz_is_config.bat` из шаблона и откроется в блокноте.
2. Проверьте/задайте:
   - `GAZ_REMOTE_WEIGHTS_PATH=Z:\actor_sync\latest_az_gumbel_az_policy.pth`
   - `GAZ_REMOTE_SEARCH_CONFIG=Z:\actor_sync\gaz_remote_search_cfg.json`
   - `GAZ_REMOTE_PORT=5565`, `GAZ_REMOTE_DEVICE=cuda:0`
   - `GAZ_REMOTE_AUTH_TOKEN=` (если используете — должен совпасть с ПК1 GUI)
   - Для первого старта (на SMB ещё нет весов): `GAZ_REMOTE_INIT_WEIGHTS=<путь к стартовому .pth>`
   - Distributed (опционально): `GAZ_REMOTE_DIST_ACTORS_ENABLED=1`, `AZ_DIST_PC1_HOST=<IP ПК1>`,
     `AZ_DIST_ROLLOUT_PORT=5567`, `AZ_DIST_TRAIN_ALGO=gumbel_az`.

## 2. Запуск

- **Только IS:** `tools\pc2_remote_gaz_is.bat` (или роль «Gumbel AlphaZero inference server» в pc2 launcher).
  Делает: venv (`install_deps.bat` при первом запуске), firewall TCP 5565, ensure `gaz_remote_search_cfg.json`,
  старт сервера. Лог: `[GAZ][REMOTE_IS] listening on 0.0.0.0:5565` (+ `runtime\logs\gaz_remote_is_*.log`).
- **IS + distributed actors одной кнопкой:** при `GAZ_REMOTE_DIST_ACTORS_ENABLED=1` тот же bat
  поднимает IS в отдельном окне и акторов здесь (rollout → ПК1:5567).
- **Только акторы (IS уже запущен):** `tools\pc2_gaz_actors.bat`.
- **Проверка без сервера:** `tools\pc2_remote_gaz_is.bat check`.

## 3. Порядок при distributed

1. На ПК1 запустить train (`TRAIN_ALGO=gumbel_az`, IS LAN + `GAZ_DISTRIBUTED_ACTORS=1`). ПК1 пишет на SMB
   `gaz_remote_search_cfg.json`, `latest_az_gumbel_az_policy.pth`, `az_dist_train_context.json`
   (с `train_algo=gumbel_az`), поднимает приёмник rollout :5567.
2. На ПК2 запустить `tools\pc2_remote_gaz_is.bat` (IS + actors).
3. На ПК1 открыть inbound TCP **5567** (firewall), на ПК2 — **5565** (bat делает сам).

## 4. Совместимость портов

GAZ=5565 (IS) / 5567 (rollout). AZ/GMZ=5555, SMZ=5560 — можно держать несколько серверов на одном ПК2,
если порты разные. Не запускайте два сервера на одном порту.

## 5. Диагностика

- Логи ПК2: `runtime\logs\gaz_remote_is_*.log`, маркеры `[GAZ][REMOTE_IS]`.
- `[GAZ][REMOTE_IS] listening on 0.0.0.0:5565` — сервер готов.
- На ПК1: `[GAZ][REMOTE_CLIENT] health_check ok ...` — связь есть.
- Нет весов/cfg на SMB — см. раздел «Частые проблемы» в `docs/remote-inference-server-gaz.md`.
