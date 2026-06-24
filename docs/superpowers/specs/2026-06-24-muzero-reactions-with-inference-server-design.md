# Умные реакции GMZ/SMZ при включённом Inference Server — дизайн

Дата: 2026-06-24
Статус: согласован заказчиком

## Цель

Сделать так, чтобы умные реакции-стратагемы (value-gate) GMZ/SMZ **работали и при включённом
inference server** — в обоих режимах: local IS (1 ПК, mp.Queue) и remote IS (ПК1+ПК2, LAN).
Сейчас фича local-only: в IS-режиме selfplay идёт через `inference_fn` (сервер делает весь
поиск), и гейт пропускается.

## Контекст (факты из кода)

- IS-режим GMZ/SMZ = **полный offload поиска**: env-воркер (`_gmz_env_worker_entry`, `train.py:7515`)
  строит `GMZInferenceClient`, а `_inference_fn` возвращает результат всего поиска
  (`policy_targets, behavior_logits, selected_actions, value_est` — `train.py:7610-7616`).
  Локальной сети и stateless `value(obs)` у воркера нет.
- Реакции — env-механизм: `make_reaction_value_policy` (`reaction_value_policy.py`) ставится в
  `env.reaction_policy`, на каждое reaction-решение делает 1-ply lookahead (apply/pass) и зовёт
  value-голову сети через `env._reaction_net_value` (`warhamEnv.py:4326`, фолбэк `net.infer(obs)`).
- **AZ уже решает это в IS** через `_ReactionEvalNet`-адаптер над evaluator (`train.py:6321-6357`) —
  потому что у AZ net-only offload (evaluator = stateless leaf-eval на воркере). У GMZ/SMZ
  evaluator'а нет → нужен **локальный value-net**.
- Сеть строится из синкаемого `*_remote_search_cfg.json`: поля `latent_dim, hidden_dim,
  num_layers, action_embed_dim, obs_dim, action_sizes` (`gmz_inference_server.py:279-294`).
  Веса синкаются как `latest_gmz_policy.pth` (`gmz_remote_search_cfg_builder.py:31-32`,
  `ACTOR_SYNC_SEARCH_CFG_NAME` / `WEIGHTS_NAME`). Сервер периодически перегружает веса
  (`gmz_inference_server.py:124`). Наш бридж `install_muzero_reaction_policy(env, net)` уже
  принимает любую сеть с `.infer`/`.parameters` (`core/models/muzero_stratagem_bridge.py`).

## Решения заказчика

- Реакции **АКТИВНЫ при IS**; целевые режимы — **оба** (local IS + remote LAN IS).
- Подход 1: **локальная value-сеть на воркере** (нагрузка реакций = CPU воркера, **без сетевых
  round-trip** → нет value-шторма по LAN). Серверный протокол не трогаем.

## Архитектура

В IS-режиме env-воркер дополнительно держит локальную value-сеть (та же `GumbelMuZeroNet` /
`SampledMuZeroNet`, что у сервера), строит её из синкнутого `*_remote_search_cfg.json` +
`latest_*_policy.pth`, и ставит `env.reaction_policy` через наш бридж напрямую (в обход
local-only guard — как AZ env-воркер). Основной поиск как был уходит на сервер; реакции
считаются локально. Веса периодически перегружаются.

### Компонент 1 — shared net-builder `core/models/muzero_value_net_builder.py` (новый)

```
def build_gmz_net_from_search_cfg(search_cfg_payload: dict, *, device) -> GumbelMuZeroNet
def build_smz_net_from_search_cfg(search_cfg_payload: dict, *, device)  # -> SMZ-сеть из sampled_muzero_model
def load_value_net_weights(net, weights_path: str) -> bool   # normalize_state_dict + load_state_dict(strict=False)
```

- Конструирование сети из cfg-полей — вынести из `gmz_inference_server.py:279-294`
  (и SMZ-аналога) сюда, чтобы сервер и воркер строили **одинаково** (DRY). Сервер
  отрефакторить на вызов этой функции (поведение неизменно, под защитой существующих IS-тестов).
- `load_value_net_weights`: `torch.load(path, map_location=device)` → `normalize_state_dict` →
  `load_state_dict(strict=False)`; вернуть True/False. Ошибка/нет файла → False (не бросать).

### Компонент 2 — worker-side install (правка `_gmz_env_worker_entry`, и SMZ-воркер)

Новый хелпер `_install_worker_reaction_value_net(env, *, assets_dir, cfg_name, weights_name, log_tag) -> net | None`:
- если флаг `{TAG}_REACTION_VALUE_POLICY` ВЫКЛ → вернуть None;
- прочитать `assets_dir/cfg_name` (JSON), построить сеть `build_*_net_from_search_cfg`,
  `load_value_net_weights(net, assets_dir/weights_name)`;
- `install_muzero_reaction_policy(env, net, log_tag=log_tag)` (наш бридж, напрямую);
- вернуть net (для последующего refresh). Любая ошибка/нет файлов → WARN + None (legacy-реакции).

Вызвать в воркере после `env = gym.make(...)` (до цикла эпизодов).

### Компонент 3 — refresh весов

В цикле эпизодов воркера: каждые `K` эпизодов (env `MUZERO_REACTION_NET_REFRESH_EVERY_EP`,
default `10`) — `load_value_net_weights(net, assets_dir/weights_name)` (если net установлен).
Так реакции отслеживают улучшающуюся политику. Ошибка reload → WARN, продолжаем со старыми весами.

### Пути к ассетам (cfg + weights)

Воркеру передаётся `reaction_assets_dir` — каталог, где лежат синкнутые `*_remote_search_cfg.json`
и `latest_*_policy.pth`:
- local IS → `MODELS_DIR/actor_sync` (куда publish_*_remote_search_cfg уже пишет);
- remote IS → `share_root` (SMB) на ПК2.
Путь резолвится в месте спавна воркеров (там, где уже известны share_root/actor_sync) и
прокидывается параметром в `_gmz_env_worker_entry` / SMZ-воркер.

## Поток данных

```
воркер старт → _install_worker_reaction_value_net:
   read *_remote_search_cfg.json → build_*_net_from_search_cfg → load latest_*_policy.pth
   → install_muzero_reaction_policy(env, value_net)  [лог {TAG}][ENV_WORKER] reaction_value_policy=ON]
по ходу env.step → reaction_policy → value_net.infer(obs) ЛОКАЛЬНО (нет round-trip)
каждые K эпизодов → reload latest_*_policy.pth в value_net
основной поиск шага → как был, на сервер
```

## Обработка краёв / ошибок

- cfg/веса ещё не синканы (ранний старт) → install вернёт None, WARN, реакции legacy; на ближайшем
  refresh, когда файлы появятся, можно поставить (опц.: попытка install и в refresh, если net=None).
- битый cfg/веса, несовпадение формы → `load_state_dict(strict=False)` + WARN; если сеть совсем
  не строится → None, legacy.
- Сообщения об ошибках: что/где/что делать (AGENTS.md), русский. Воркер не падает ни при какой ошибке install/refresh.

## Тестирование (TDD)

- `tests/models/test_muzero_value_net_builder.py`:
  - `build_gmz_net_from_search_cfg` на мини-cfg (маленькие dims) строит сеть; `net.infer(obs)`
    возвращает (policy, value); `build_smz_...` аналогично.
  - `load_value_net_weights`: на сохранённом state_dict грузит (True); несуществующий путь → False
    без исключения.
- `tests/models/test_worker_reaction_value_net.py`:
  - `_install_worker_reaction_value_net` с подготовленным tmp `assets_dir` (cfg.json + weights.pth,
    мини-сеть) → `env.reaction_policy` поставлен, вернул net; нет файлов → None, `reaction_policy`
    не появилось, без падения; флаг ВЫКЛ → None.
- Регресс: существующие IS-тесты сервера (после рефактора builder) не сломаны.
- Smoke (Task в плане): короткий GMZ-прогон с local IS + флаг ВКЛ → лог
  `[GMZ][ENV_WORKER] reaction_value_policy=ON`, эпизоды без падений (value-путь локальной сети отработал).

## Definition of Done

1. Тесты builder + worker-install зелёные (TDD).
2. Сервер отрефакторен на shared builder; существующие IS-тесты не сломаны.
3. ruff чистый.
4. Smoke (local IS) подтверждает install локальной value-сети и работу реакций без падений.
5. SMZ-симметрия: то же для sampled-воркера.
6. Коммиты только по коду; артефакты/логи/веса не коммитятся.

## Не-цели (YAGNI)

- Новые серверные RPC (value-endpoint) — нет (в этом плюс Подхода 1).
- Изменение основного поиска / action-пространства / активных fight-стратагем — нет.
- Тонкая оптимизация частоты reload — фиксированный K с env-override, без адаптива.
- Измерение эффекта на winrate — отдельно (есть таблица стратагем).

## Риски

- CPU-оверхед value-форвардов на воркере (особенно много реакций/шаг). Сопоставим с local-actors
  режимом; если ощутимо — флаг `{TAG}_REACTION_VALUE_POLICY=0` выключает. K reload регулирует свежесть/стоимость.
- Рассинхрон формы cfg↔weights при обновлении на лету: `strict=False` + WARN; формы стабильны в рамках прогона.
- Доступность `reaction_assets_dir` на ПК2 (SMB) — та же зависимость, что и у remote-сервера; если путь
  недоступен → install вернёт None (legacy), не падаем.
