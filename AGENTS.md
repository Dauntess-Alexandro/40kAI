# 40kAI — AGENTS.md (инструкции для OpenAI Codex)

## README
- README в этом репозитории может быть устаревшим — **не полагайся на README как на источник истины**.
- Всегда сверяйся с **актуальным кодом** и реальными файлами в репо.

## Логи для отладки (runtime/logs/LOGS_FOR_AGENTS_*.md)
- В папке `runtime/logs/`:
  - **LOGS_FOR_AGENTS_TRAIN.md** — обучение (`train`),
  - **LOGS_FOR_AGENTS_PLAY.md** — игра/Viewer (`play`),
  - **LOGS_FOR_AGENTS_EVAL.md** — оценка (`eval`),
  - **LOGS_FOR_AGENTS_REMOTE_IS.md** — standalone remote inference server на ПК2.
- Все три файла — “источник правды” по тому, что реально происходило.
- При любом баге/неожиданном поведении:
  1) **сначала прочитай свежие строки** из релевантного файла (и при необходимости соседних): `LOGS_FOR_AGENTS_TRAIN.md`, `LOGS_FOR_AGENTS_PLAY.md`, `LOGS_FOR_AGENTS_EVAL.md`,
  2) найди маркеры фаз/ходов/юнитов/ошибок,
  3) только потом предлагай правки.
- Если в логах есть признаки ошибки/варнингов/неконсистентности — укажи:
  - **что случилось**, **где** (файл/функция/строка), **что сделать дальше** (конкретные шаги).
- Не добавляй “тишину”: если что-то “пропущено/автоматически”, лог должен объяснять **почему** (например: нет целей, advance без assault, invalid target index, etc).
- Логи нужны для Codex: **не переписывай их формат без необходимости**, лучше добавляй новые строки аккуратно и явно.

## Язык и стиль
- Общение с пользователем и тексты в UI/логах: **русский язык**.
- Пиши кратко и по делу, но так, чтобы новичку было понятно.
- Сообщения об ошибках должны содержать: **что случилось + где + что сделать дальше**.
- Комментарии в коде: RU/EN допустимо, без лишней воды.
- Скриншоты не делай, тесты при надобности только

## Зависимости / библиотеки
- **Можно добавлять новые библиотеки**, если это действительно упрощает задачу или улучшает качество.
- При добавлении зависимости:
  - обновляй зависимости проекта (requirements/pyproject и т.п. — как принято в репо),
  - предпочитай популярные и стабильные библиотеки,
  - избегай тяжёлых зависимостей без необходимости.
  
## Платформа и актуальный GUI
- Основная разработка и тестирование сейчас ведутся **на Windows**.
- Мы работаем только с новым GUI: **Qt GUI (PySide6)**.
- Старый GUI удалён из активной разработки; legacy-артефакты (если где-то остались) считаем архивом и не трогаем.
- Все правки по интерфейсу, логам и UX делаем **только в Qt GUI**.
- Предпочитаемый сценарий запуска:
  - игру запускать через **Viewer** (GUI), а не через терминал,
  - обучение (`train`) и оценку (`eval`) запускать через **наш Qt GUI**.
- Если есть выбор между терминальным и GUI-потоком, приоритет — GUI-вариант.


## Remote Inference Server (GMZ)
- **Пошаговый гайд (поставить сервер на ПК2):** `docs/pc2-remote-is-setup-guide.md`.
- Руководство (ПК1 + ПК2, установка, SMB, отладка): `docs/remote-inference-server-gmz.md`.
- Запуск на ПК2 одной кнопкой: `tools/pc2_remote_is.bat` (конфиг: `runtime/state/pc2_remote_is_config.bat`).
- Конфиг GUI (ПК1): `runtime/state/remote_is.json` (в `.gitignore`).
- Логи сервера на ПК2: `runtime/logs/LOGS_FOR_AGENTS_REMOTE_IS.md`, `gmz_remote_is_*.log`.

## Remote Inference Server (Sampled MuZero)
- Гайд: `docs/remote-inference-server-smz.md`; пошагово на ПК2: `docs/pc2-remote-smz-is-setup-guide.md`.
- Запуск ПК2: `tools/pc2_remote_smz_is.bat` (конфиг: `runtime/state/pc2_remote_smz_is_config.bat`). Порт по умолчанию 5560 (gmz/az — 5555; не запускать на одном ПК2/порту).
- Конфиг GUI (ПК1): `runtime/state/remote_is_smz.json`. Тумблер: hyperparams `sampled_muzero.inference_server_enabled` / env `SMZ_INFERENCE_SERVER=1`. Дефолт выкл.
- Логи: `[SMZ][INF_SERVER]`, `[SMZ][REMOTE_IS]`, `[SMZ][CONFIG]` (learner/сервер); env-воркеры переиспользуют общий воркер и логируют под `[GMZ][ENV_WORKER]`/`[GMZ][REMOTE_CLIENT]`.

## Inference Server (AlphaZero tree)
- **Дизайн:** `docs/inference-server-az-design.md` (план: `plans/az-tree-inference-server.md`).
- **LAN-руководство (ПК1+ПК2):** `docs/remote-inference-server-az.md`; пошагово на ПК2: `docs/pc2-remote-az-is-setup-guide.md`.
- Net-only offload: дерево MCTS + env-rollout'ы на CPU-воркере; на GPU-сервер уходит только `net.infer`. Сервер stateless.
- Запуск на ПК2: `tools/pc2_remote_az_is.bat` (конфиг: `runtime/state/pc2_remote_az_is_config.bat`). Порт по умолчанию **5555** (тот же, что у GMZ — не запускать оба remote-сервера на одном ПК2 одновременно; нужны оба — задать разные порты).
- Конфиг GUI (ПК1): LAN-настройки AZ (host/port/auth/mode) хранятся в `hyperparams.json` → `alphazero_tree` (поля `inference_*`); панель «Inference Server» во вкладке AlphaZero Tree.
- Флаг: `inference_server_enabled` (hyperparams `alphazero_tree`) / env `AZ_INFERENCE_SERVER=1`. По умолчанию выключен (вариант A — CPU акторы).
- Для LAN рекомендуется `mcts_max_depth=1` (иначе round-trip шторм на intermediate-evals).
- Логи: `[AZ][INF_SERVER]`, `[AZ][ENV_WORKER]`, `[AZ][REMOTE_IS]`, `[AZ][REMOTE_CLIENT]`.

## Distributed self-play (AlphaZero tree, PC1+PC2)
- **План:** `plans/az-distributed-selfplay.md`. Целевой профиль: **IS LAN** на PC2 + доп. env-воркеры на PC2 (rollout → PC1).
- **ПК1 (train):** `distributed_actors_enabled=1` в `hyperparams.json` → `alphazero_tree` или env `AZ_DISTRIBUTED_ACTORS=1`. Learner поднимает `RolloutReceiver` (PULL **5557**), пишет `artifacts/models/actor_sync/az_dist_stop.flag` по завершении.
- **ПК2:** `tools/pc2_remote_az_is.bat` — IS (:5555) + distributed actors (конфиг: `runtime/state/pc2_remote_az_is_config.bat`, `AZ_REMOTE_DIST_ACTORS_ENABLED=1`). Отдельно только actors: `tools/pc2_az_actors.bat` → `actors-only`. Воркеры: infer → `127.0.0.1:5555`, rollout → IP PC1:5557.
- Логи: `[AZ][DIST]`, `[AZ][DIST][RECEIVER]`, `[AZ][DIST][SINK]`, `stale_drop remote=…%`.
- Отключить: `AZ_DISTRIBUTED_ACTORS=0` — прежний одиночный путь.

## Remote Inference Server + Distributed self-play (Gumbel AlphaZero, GAZ)
- **Дизайн:** `docs/inference-server-gaz-design.md` (спека: `docs/superpowers/specs/2026-06-16-gaz-inference-and-distributed-design.md`). **LAN-гайд:** `docs/remote-inference-server-gaz.md`; пошагово на ПК2: `docs/pc2-remote-gaz-is-setup-guide.md`. Планы: `plans/gaz-inference-server.md`, `plans/gaz-distributed-selfplay.md`.
- **Тонкий слой:** GAZ (`gumbel_az`) едет на общей AZ-инфре (та же сеть `AlphaZeroPolicyValueNet`, общие `_main_actor_learner_alphazero`/`_az_env_worker_entry`/`az_inference_*`/`az_rollout_*`). Net-only offload: дерево SH + env-rollout на CPU-воркере, на GPU-сервер — только `net.infer` (+ батч leaf-eval). Свои у GAZ: порт, веса, имена, флаги, GUI-панель, ПК2-лаунчер.
- **Порты (свои, не конфликтуют):** IS **5565**, distributed **5567** (AZ/GMZ=5555, SMZ=5560).
- **Флаги:** `gumbel_az.inference_server_enabled` / env `GAZ_INFERENCE_SERVER=1` (дефолт 0); `gumbel_az.distributed_actors_enabled` / env `GAZ_DISTRIBUTED_ACTORS=1` (дефолт 0); на ПК2 — `GAZ_REMOTE_DIST_ACTORS_ENABLED=1`. Приоритет резолва: `GAZ_* → AZ_* → секция gumbel_az` (`core/models/az_family_env.py`).
- **Веса (SMB):** `latest_az_gumbel_az_policy.pth`; search_cfg: `gaz_remote_search_cfg.json` (форма сети = AZ; пишется автоматически на ПК1). Stop-flag: `gaz_dist_stop.flag`.
- **ПК2:** `tools/pc2_remote_gaz_is.bat` — IS (:5565) + опц. distributed actors (`AZ_DIST_TRAIN_ALGO=gumbel_az`, rollout → PC1:5567). Только actors: `tools/pc2_gaz_actors.bat`. Конфиг: `runtime/state/pc2_remote_gaz_is_config.bat`. Сервер: `tools/az_remote_inference_server.py --algo-label GAZ`.
- **Конфиг GUI (ПК1):** `runtime/state/remote_is_gaz.json` (в `.gitignore`); панель «Inference Server» во вкладке **Gumbel AlphaZero**.
- **Логи:** `[GAZ][INF_SERVER]`, `[GAZ][ENV_WORKER]`, `[GAZ][REMOTE_IS]`, `[GAZ][REMOTE_CLIENT]`, `[GAZ][DIST]`, `[GAZ][DIST][RECEIVER]`, `[GAZ][DIST][SINK]`, `[GAZ][CONFIG][FALLBACK]`.
- Отключить: `GAZ_INFERENCE_SERVER=0` / `GAZ_DISTRIBUTED_ACTORS=0` — прежний одиночный CPU-путь.

## Результаты треинровки (общее)
- **Можно смотреть `artifacts/results/results.txt`** для быстрой сверки итогов train/eval.

## Правило коммитов после подтверждения пользователя
- Если пользователь после внесённых изменений и проверок пишет **«Все ок»**, агент может сразу делать коммит текущих проверенных изменений без отдельного запроса.
- Если после «Все ок» пользователь в том же сообщении (или следующим сообщением) даёт новую задачу («теперь делаем ...»), агент должен:
  1) сначала закоммитить уже подтверждённые изменения,
  2) затем переходить к новым изменениям.
- В коммит включать только релевантные кодовые изменения; служебные логи/временные runtime-файлы по возможности не коммитить.


