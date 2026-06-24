# Умные реакции-стратагемы для GMZ/SMZ — дизайн

Дата: 2026-06-24
Статус: согласован заказчиком

## Цель

Научить Gumbel MuZero (GMZ) и Sampled MuZero (SMZ) **умно выбирать реактивные стратагемы**
(overwatch, go_to_ground и т.п.) — через тот же value-gate (1-ply lookahead apply/pass),
который уже есть у DQN/PPO/AZ/GAZ. Сейчас MuZero-варианты этот механизм не ставят, поэтому
реагируют по legacy («всегда реагировать»).

## Контекст (факты из кода)

- «Умный выбор» = `make_reaction_value_policy` (`core/models/reaction_value_policy.py`),
  ставится в `env.reaction_policy`. На каждое reaction-решение: snapshot → симуляция apply/pass
  через `env._simulate_reaction_branch` → value-голова сети → выбор лучшего (тай → PASS).
- Install-сайты сейчас: DQN (`train.py:5310`), PPO (`train.py:5731`), AZ/GAZ (`train.py:6055`,
  `:6345`). MuZero (GMZ/SMZ) — **нет install вообще**; без `reaction_policy` env возвращает
  `True` (всегда реагировать, `core/envs/warhamEnv.py:4305`).
- Механизм алго-агностичен: `env._reaction_net_value` (`warhamEnv.py:4326`) при отсутствии у сети
  `infer_with_value` использует фолбэк `net.infer(obs)` и читает value. MuZero-модель `infer`
  (`gumbel_muzero_model.py:315`) как раз возвращает (policy, value) → подходит без доработок сети.
- **Активные fight-стратагемы уже в action-пространстве MuZero**: `ordered_action_keys`
  (`action_contract.py:20`) включает `strat_{phase}`/`strat_{phase}_unit`, MuZero-selfplay их
  использует (`gumbel_muzero_selfplay.py:98`). Эту часть НЕ трогаем — гэп только в реакциях.
- Локальная сеть доступна в search-объекте: `GumbelMuZeroSearch.net` / `SampledMuZeroSearch.net`
  (`gumbel_muzero_search.py:102`, `sampled_muzero_search.py:106`). Selfplay-функции принимают
  либо `search` (локально), либо `inference_fn` (remote).

## Решения заказчика

- Дефолт: **ВКЛ** (как DQN/PPO), флаги `GMZ_REACTION_VALUE_POLICY` / `SMZ_REACTION_VALUE_POLICY`.
- **Только локальный режим**: при remote-inference (`inference_fn`, нет дешёвой локальной value-сети)
  гейт не ставится (иначе round-trip шторм).
- **Обе стороны** (как AZ): `{"model": net, "enemy": net}`.

## Архитектура

Один общий бридж + install-пойнт внутри каждой selfplay-функции (а не в train.py) — так один
вызов покрывает все call-site'ы (eval/actor/single) и сам реализует local-only.

### Компонент 1 — `core/models/muzero_stratagem_bridge.py` (новый)

```
def muzero_reaction_value_policy_enabled(flag_env: str, default: str = "1") -> bool
def install_muzero_reaction_policy(env, net, *, device, both_sides: bool = True,
                                   log_tag: str = "GMZ", log_fn=None) -> bool
```

- `install_...`: если `net is None` → вернуть False, ничего не ставить. Иначе:
  `_eu._reaction_net_by_side = {"model": net, "enemy": net}` (both_sides; иначе только `model`);
  `_eu.reaction_policy = make_reaction_value_policy(_eu._reaction_net_by_side, device=device)`;
  залогировать `[{log_tag}][REACTION] reaction_value_policy=ON`; вернуть True.
- Весь install в try/except: провал → WARN-лог (рус., что/где/что делать) + вернуть False
  (обучение продолжается на legacy).

### Компонент 2 — install-пойнт в selfplay (правка)

В начале `play_episode_with_gumbel_muzero` и `play_episode_with_sampled_muzero`, после `env_u`:

- если `muzero_reaction_value_policy_enabled("GMZ_REACTION_VALUE_POLICY")` И `search is not None`:
  `install_muzero_reaction_policy(env, search.net, device=<device search>, log_tag="GMZ")`;
- если `inference_fn is not None` (remote): не ставить, лог
  `[GMZ][REACTION] skip: remote inference (local-only)` (по флагу, чтобы не шуметь).

Device берётся из сети (`next(net.parameters()).device`) — `_reaction_net_value` и так это делает,
явный device в install передаётся для `make_reaction_value_policy` (как в AZ — cpu_device).
В MuZero selfplay устройство известно у search; передать его.

## Поток данных

```
старт эпизода → install_muzero_reaction_policy (1 раз, если локально+флаг)
   → env.step() по ходу → env зовёт reaction_policy на каждое reaction-решение
      → snapshot → _simulate_reaction_branch(apply/pass) → net.infer(obs) → value стороны
      → apply если value(apply) > value(pass), иначе pass (экономия CP)
```

Активные fight-стратагемы остаются как есть (action-пространство MuZero).

## Обработка краёв / ошибок

- remote (`inference_fn`) → skip + лог.
- `net is None` или нет `infer` → skip, legacy (`_reaction_net_value` уже терпим).
- ошибка install → WARN, продолжаем без гейта (не валим обучение).
- Сообщения об ошибках: что случилось + где (файл/функция) + что делать (AGENTS.md), язык русский.

## Тестирование (TDD, тесты до кода)

- `tests/models/test_muzero_stratagem_bridge.py`:
  1. `install_muzero_reaction_policy(env, net)` ставит `reaction_policy` (callable) и
     `_reaction_net_by_side == {"model": net, "enemy": net}`, возвращает True;
     `net=None` → возвращает False, `reaction_policy` не появилось.
  2. **value-семантика (критичный):** фейковая MuZero-подобная сеть с `infer(obs, masks_by_head=None)
     -> (policy, value)` (БЕЗ `infer_with_value`) на мок-env с `_simulate_reaction_branch`,
     возвращающим заранее заданные value → гейт выбирает apply при value(apply) > value(pass)
     и pass иначе. Проверяет фолбэк `_reaction_net_value→net.infer` и знак value.
  3. wiring: `muzero_reaction_value_policy_enabled` корректно читает флаг (вкл/выкл, дефолт ВКЛ).
- `tests/models/` рядом с существующими GMZ/SMZ-тестами: smoke-проверка, что selfplay-функция
  при `search` (локально) и флаге ВКЛ зовёт install (через monkeypatch install_… или проверку
  `env.unwrapped.reaction_policy is not None` после короткого эпизода); при `inference_fn`/флаг
  ВЫКЛ — `reaction_policy is None`.

## Definition of Done

1. Тесты бриджа + wiring зелёные (TDD).
2. Существующие GMZ/SMZ-тесты не сломаны (`pytest tests/models -q` по релевантным).
3. ruff на новом коде чистый.
4. Smoke: короткий GMZ-selfplay (локально, флаг ВКЛ) → в env стоит `reaction_policy`,
   в логе `[GMZ][REACTION] reaction_value_policy=ON`; remote/флаг-выкл → не стоит.
5. Коммиты только по коду; артефакты/логи не коммитятся.

## Не-цели (YAGNI)

- Remote-inference поддержка реакций — нет (local-only).
- Изменение action-пространства / активных fight-стратагем — нет (уже работают).
- Тюнинг reward/таблиц — нет (отдельные задачи).
- Тренировочные прогоны «до/после» с измерением эффекта — вне scope этой задачи (можно потом,
  у нас уже есть таблица стратагем для замера).

## Риски

- Семантика value у MuZero `infer` (знак/перспектива стороны) — закрывается тестом №2.
- Стоимость: гейт делает доп. `net.infer` на каждое reaction-решение в локальном режиме —
  ожидаемо терпимо (как у DQN/PPO), но при заметном замедлении флаг позволяет выключить.
