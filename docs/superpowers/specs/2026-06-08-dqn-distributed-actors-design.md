# Distributed DQN actors (ПК1 + ПК2) — дизайн

> Дата: 2026-06-08. Статус: согласован, готов к плану реализации.
> Цель: подключить второй ПК (ПК2) как дополнительную фабрику опыта для DQN —
> аналогично уже работающему distributed self-play для AlphaZero tree.

## 1. Контекст и проблема

- Узкое место обучения DQN на ПК1 — **CPU / throughput окружений** (шаг env + n-step
  накопление). GPU ПК1 (RTX 5060 Ti) недогружен относительно скорости генерации опыта.
- Для AlphaZero tree и Gumbel MuZero распределёнка на ПК2 уже есть; для DQN/PPO/AZ proxy — нет.
- **DQN уже имеет actor-learner split** локально (`_main_actor_learner`, `train.py`):
  GPU-learner + CPU-актора через `mp.Queue` (`data_q`), и актора **уже синкают сеть через файл**
  `actor_sync/latest_policy.pth`. AZ-distributed просто добавил к тому же `data_q` сетевой
  `RolloutReceiver` (ZMQ PULL). Значит ~80% машинерии уже существует.

### Железо
- **ПК1 (learner):** Ryzen 5 7600 (6 быстрых ядер) + RTX 5060 Ti. Тренирует на GPU и
  параллельно крутит локальные актора на CPU.
- **ПК2 (actors):** Ryzen 1600 (6 ядер) + RTX 2060 Super. Гоняет env на CPU, сеть DQN
  считает локально на 2060. Добавляет акторов поверх локальных ПК1.

Итог — ~12 ядер генерят опыт в один общий PER-replay на ПК1 (паттерн Ape-X).

## 2. Архитектура

```
ПК1 (learner, 5060 Ti)                         ПК2 (actors, 2060S + Ryzen 1600)
┌─────────────────────────────┐                ┌──────────────────────────────┐
│ _main_actor_learner (DQN)   │                │ tools/pc2_dqn_actors.py      │
│  • GPU train + PER replay   │                │  • N актор-процессов (spawn) │
│  • локальные актора → data_q │                │  • env + ε/noisy net (2060)  │
│  • RolloutReceiver (PULL     │◄──── LAN ──────│  • n-step → buf              │
│    :5557) → тот же data_q    │   transitions  │  • RolloutSink (PUSH :5557)  │
│  • пишет latest_policy.pth ──┼──► SMB-шара ◄──┼─ читает веса раз в N апдейтов │
│  • dqn_dist_stop.flag ───────┼──► SMB ────────┼─ стоп-сигнал                 │
└─────────────────────────────┘                └──────────────────────────────┘
```

Ключевой инвариант: **локальный и удалённый путь сходятся в один `data_q`** —
learner не различает, откуда пришёл батч.

### Решения по дизайну
- **Net-sync = SMB-файл** (не remote inference server). DQN-актор гоняет сеть локально
  на 2060 ПК2; веса прилетают файлом `latest_policy.pth` раз в `ACTOR_SYNC_EVERY_UPDATES`.
  Remote IS отвергнут: для DQN без дерева это round-trip на каждый ход.
- **PER-приоритеты = «оба сразу» через опциональное поле.** Wire-формат несёт необязательный
  `priority`. MVP едет на learner-side (поле пустое → `max_priority` при вставке, как сейчас).
  Actor-side TD-error (честный Ape-X) добавляется позже одним флагом — формат не меняется.
- **IS-сервера для DQN нет** → порт 5555 свободен, конфликта с AZ/GMZ remote-IS на ПК2 нет.
- **Off-policy толерантность:** дроп переходов при переполнении очереди и stale-веса безвредны
  (в отличие от PPO, где нужен V-trace).

## 3. Компоненты

### Переиспользуем без изменений
| Компонент | Файл | Роль для DQN |
|---|---|---|
| `RolloutReceiver` | `core/models/az_rollout_receiver.py` | PULL :5557 → `data_q`. Алго-агностичен. hello/heartbeat/контракт-хеш. |
| wire-протокол | `core/models/az_rollout_protocol.py` | `encode/decode`, `validate_wire_message`, auth + `env_contract_hash`. |
| sink на ПК2 | `core/models/az_rollout_sink.py` | ZMQ PUSH + stop-flag хелперы. |
| net-sync файл | `train.py` (`actor_sync/latest_policy.pth`) | Уже пишется learner'ом; ПК2 направит `MODELS_DIR`→SMB. |
| актор-цикл | `train.py` `_actor_learner_actor_entry` | Тело актора без изменений (пишет через `.put()`). |

### Новое (минимум кода)
1. **`_RemoteDataQ` адаптер** — объект с `.put((kind, payload))`, сериализует и PUSH'ит через
   sink вместо `mp.Queue`. `_actor_learner_actor_entry` получает его вместо `data_q` и работает
   без изменений. Локальный `("batch", buf)` (голый список) по сети заворачивается в
   `{"actor_idx", "steps": buf, "priority": None}` (как PPO-rollout).
2. **Адаптер чтения в learner-цикле** — потребитель `data_q` учится понимать и
   `("batch", {"steps": [...], "priority": ...})` от удалёнки (где `priority` есть — в
   `memory.push`/`update_priorities`). Точка под будущий actor-side Ape-X.
3. **`RolloutReceiver` в `_main_actor_learner`** — под флагом `DQN_DISTRIBUTED_ACTORS=1`,
   bind PULL :5557, тот же `data_q`. Учёт `active_remote_workers` в `[TRAIN][DIST]`.
4. **`tools/pc2_dqn_actors.py` + `.bat` + `runtime/state/pc2_dqn_actors_config.bat`** — по
   образцу `tools/pc2_az_actors.py`: спавнит N акторов с `_RemoteDataQ`, читает opponent/контракт
   из SMB train-context, останавливается по stop-flag.
5. **Флаг в GUI** — `dqn` секция hyperparams: `distributed_actors_enabled` + host/port/auth
   (зеркало AZ-панели). Док `docs/pc2-dqn-actors-setup-guide.md`.

Принцип: **ноль дублирования транспорта** — переиспользуем существующий `az_rollout_*`
слой, не плодим `dqn_rollout_*` (требование проекта про рассинхрон параллельных веток).

## 4. Поток данных (happy path)

1. ПК1 стартует train (DQN, `distributed_actors_enabled=1`) → пишет в SMB
   `dqn_dist_train_context.json` (контракт env, `env_contract_hash`, `opponent_agent_id`,
   hyperparams) и стартовый `latest_policy.pth`. Поднимает `RolloutReceiver` (:5557).
2. ПК2: `pc2_dqn_actors.bat` → читает train-context с SMB, грузит веса, спавнит N акторов.
3. ПК2-актор: `reset` → каждый шаг считает сеть на 2060 (ε/noisy) → копит n-step →
   при `len(buf)>=batch_send` PUSH `("batch", {...})` на ПК1:5557. По концу эпизода — `("ep", {...})`.
4. ПК1 `RolloutReceiver` декодирует, валидирует (auth + `env_contract_hash`), кладёт в общий
   `data_q`. Learner вставляет в PER-replay и тренирует — источник безразличен.
5. Раз в `ACTOR_SYNC_EVERY_UPDATES` learner перезаписывает `latest_policy.pth`; ПК2-актора
   подхватывают по mtime (механизм уже есть для локальных).
6. Конец прогона → ПК1 трогает `dqn_dist_stop.flag` на SMB → ПК2-актора завершаются.

## 5. Обработка ошибок (переиспустим из receiver/sink)

- **Несовпадение контракта** (ростер/миссия/ruleset) → `env_contract_hash` не сходится → дроп
  перехода с логом «что/где/что делать». Защита от мусора в replay.
- **auth_token / protocol_version** не сошлись → дроп + лог.
- **Переполнение `data_q`** → `queue_full`, дроп с советом снизить число воркеров. Для off-policy
  DQN дроп переходов безвреден.
- **ПК2 отвалился** → learner по `active_remote_workers` (heartbeat) логирует затишье удалёнки
  и продолжает на локальных акторах, не падает.
- **Stale-веса на ПК2** → норма для off-policy (Ape-X); логируем возраст весов для диагностики.

## 6. Тестирование (тест до кода; движок не трогаем)

- `tests/models/test_dqn_remote_sink_roundtrip.py` — `_RemoteDataQ` → encode → decode → форма
  `("batch", {...})` совпадает с тем, что ждёт learner-потребитель.
- `tests/models/test_dqn_dist_priority_optional.py` — payload без `priority` → `max_priority`;
  с `priority` → `update_priorities`. Фиксирует «оба сразу».
- `tests/models/test_dqn_dist_contract_guard.py` — чужой `env_contract_hash` дропается.
- Smoke: локальный self-connect (актор PUSH 127.0.0.1:5557 → receiver → data_q) на пару батчей,
  без обучения и без живого ПК2.

Движок (фазы хода, бой, видимость, MCTS) не затрагиваем — только транспорт и learner-обвязка.

## 7. Конфигурация (флаги)

| Флаг | Где | Назначение |
|---|---|---|
| `DQN_DISTRIBUTED_ACTORS` / `distributed_actors_enabled` (hyperparams `dqn`) | ПК1 | Поднять `RolloutReceiver` в DQN-learner. По умолчанию 0. |
| `DQN_DIST_ROLLOUT_PORT` | оба | Порт PULL/PUSH rollout'ов (по умолчанию 5557). |
| `DQN_DIST_AUTH_TOKEN` | оба | Совместный секрет (можно общий с AZ). |
| `DQN_DIST_PC2_NUM_WORKERS` | ПК2 | Число актор-процессов на ПК2. |
| `DQN_DIST_ACTOR_PRIORITY` | ПК2 | (Будущее) включить actor-side TD-error. По умолчанию 0. |

## 8. Вне рамок (YAGNI для MVP)

- Actor-side TD-error (честный Ape-X) — протокол готов, реализация позже по флагу.
- Аналогичная распределёнка для PPO (нужен V-trace) и AZ proxy (выигрыш сомнителен).
- Балансировка/шардинг replay между несколькими ПК2 (пока один ПК2).
