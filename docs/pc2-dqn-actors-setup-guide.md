# ПК2: DQN distributed actors — пошаговый запуск

## Что это
ПК2 (Ryzen 1600 + RTX 2060S) генерит опыт DQN и шлёт переходы по LAN в общий
PER-replay learner'а на ПК1. Узкое место (CPU/env throughput) масштабируется —
суммарно ~12 ядер на оба ПК работают в один replay (паттерн Ape-X).

## Предусловия
- На ПК1 и ПК2 один и тот же код репозитория и `requirements_windows.txt`.
- SMB-шара ПК1 с `artifacts/models` смонтирована/доступна на ПК2 (напр. `\\PC1\40kai_models`).
- Один и тот же ростер/миссия (иначе `env_contract_hash` не сойдётся — переходы дропнутся).

## Шаги
1. **ПК1:** в Qt GUI вкладка **Настройка параметров тренировки** → секция гиперпараметров **DQN**
   → группа **«Распределённое обучение (ПК2)»** (внизу, свёрнута) → разверни и поставь
   `distributed_actors_enabled = 1` (порт `distributed_rollout_port` оставь 5558,
   `distributed_auth_token` — опц.). Сохрани hyperparams и запусти train. Learner поднимет
   receiver :5558 и запишет `actor_sync/dqn_dist_train_context.json` + `latest_policy.pth` на SMB.
   (Альтернатива без GUI: env `DQN_DISTRIBUTED_ACTORS=1` перед запуском train.)
2. **ПК2:** запусти `tools\pc2_dqn_actors.bat` — при первом запуске он скопирует
   `runtime\state\pc2_dqn_actors_config.example.bat` → `pc2_dqn_actors_config.bat`.
   В нём **обязательно задать только `MODELS_DIR`** — путь к SMB-шаре ПК1
   (напр. `\\192.168.1.10\40kai_models`). Остальное выводится автоматически:
   - **IP ПК1** ← из UNC-пути `MODELS_DIR`,
   - **порт + auth** ← из `dqn_dist_train_context.json` (ПК1 пишет при старте),
   - **воркеры** ← число ядер CPU.
   (Если шара подключена как диск `Z:\` — UNC недоступен; тогда раскомментируй
   `DQN_DIST_PC1_HOST` в конфиге.)
3. **ПК2:** запусти `tools\pc2_dqn_actors.bat` ещё раз. В логе будет строка
   `[DQN][DIST][PC2] автоконфиг: host=… port=… auth=… workers=… context=есть`.

## Проверка
- ПК1-лог `[DQN][DIST] receiver bind=:5558 ...` и далее рост `received_rollouts`
  (через `[AZ][DIST][RECEIVER]` — транспорт общий с AZ, префикс переиспользован).
- ПК2-лог `[DQN][DIST][PC2] worker=... → IP:5558 ...`.
- Если `drop invalid message` / `env_contract_hash mismatch` — ростер/миссия/ruleset
  на ПК1≠ПК2. Синхронизируй конфиг.

## Остановка
ПК1 по завершении прогона пишет `actor_sync/dqn_dist_stop.flag` — ПК2-воркеры
сами завершатся. Можно также закрыть окно `pc2_dqn_actors.bat`.

## Порты
- DQN dist rollout — **5558** (отдельно от AZ dist :5557 и remote-IS :5555).
  AZ-dist и DQN-dist можно гонять на одном ПК1 одновременно.

## Как это работает (кратко)
- Транспорт переиспользован из AlphaZero-distributed (`core/models/az_rollout_*`):
  ZMQ PUSH (ПК2) → PULL (ПК1) → общий `data_q` learner'а.
- DQN-актор на ПК2 — тот же `_actor_learner_actor_entry`, что и локальные актора ПК1,
  но пишет через шим `RemoteDataQ` (`core/models/dqn_dist.py`) вместо `mp.Queue`.
- Веса синкаются файлом `latest_policy.pth` по SMB (как у локальных акторов).
- PER-приоритеты: MVP — learner-side (`max_priority` при вставке). Протокол несёт
  опциональное поле `priority` под будущий actor-side Ape-X (`DQN_DIST_ACTOR_PRIORITY`).
