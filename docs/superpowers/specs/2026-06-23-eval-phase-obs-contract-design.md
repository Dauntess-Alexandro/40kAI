# Eval строит env под контракт агента (phase_obs_features) — Design

**Дата:** 2026-06-23
**Статус:** согласован, готов к плану реализации
**Контекст:** AZ-eval падает `obs_space_signature mismatch` — агент `..._ep10` обучен с `phase_obs_features=1` (obs `vec:41` = 17 базовых + 24 phase), а eval поднимает env с `phase_obs_features=0` (obs=17). Причина: `phase_obs_features_enabled()` читает env-var `PHASE_OBS_FEATURES`; `train.py` сам выставляет её из hyperparams, **а eval — нет** → дефолт 0 → obs=17 → mismatch.

## Проблема

eval не знает, с каким `phase_obs_features` обучался агент, и строит env с дефолтом (0). Контракт агента (`vec:41`) кодирует полный obs, но eval строит env ДО загрузки контракта (env: eval.py:981/985, reset/obs: 1027-1031; контракт агента грузится позже, 1053) → не может подстроиться.

## Решение (один связный фикс, без слома legacy)

**Источник истины — контракт самого агента, не текущие hyperparams.**

### A. Self-describing контракт (не ломая формат сигнатуры)
`make_env_contract` (`core/engine/agent_registry.py:160`) дополнительно кладёт в `extras` текущие `phase_obs_features` и `reaction_value_policy` (читая `phase_obs_features_enabled()` и env `AZ_REACTION_VALUE_POLICY`), НЕ перетирая явно переданные ключи. **Формат `obs_space_signature` не меняется** (`vec:{n}` — число уже кодирует полный obs). `extras` не участвует в `compatible_contracts` (там сравниваются только ruleset/obs_sig/action_sig) → совместимость не ломается; меняется лишь `contract_hash` (для идентичности, не для совместимости).

### B. Eval резолвит phase_obs ДО постройки env
В `eval.py`, в начале (ДО `load_latest_model`/`_build_env_from_train_roster`, т.е. до eval.py:981), если задан `args.learner_agent_id`:
1. Загрузить контракт агента (`load_agent_by_id` или прочитать `env_contract.json`), взять `extras.get("phase_obs_features")`.
2. Резолв по приоритету: **контракт агента → hyperparams (`alphazero_tree.phase_obs_features`) → env-var `PHASE_OBS_FEATURES` → 0**.
3. Выставить `os.environ["PHASE_OBS_FEATURES"]` = "1"/"0" ДО постройки env.
4. То же для `reaction_value_policy` → `os.environ["AZ_REACTION_VALUE_POLICY"]` (поведенческий паритет; obs не меняет, но матчит обучение).

После этого env строится с правильным phase_obs → obs=41 → `make_env_contract` (eval.py:1040) даёт `vec:41` → `compatible_contracts` совпадает.

### C. Legacy
Существующий `vec:41`-агент (в `extras` нет `phase_obs_features`) → шаг резолва падает на hyperparams (`alphazero_tree.phase_obs_features=1`) → obs=41 → грузится. Будущие агенты несут флаг в `extras` → матчатся независимо от текущих hyperparams.

## Архитектура

- **`core/engine/agent_registry.py` `make_env_contract`:** в начале построения `extras` — слить `{"phase_obs_features": int(phase_obs_features_enabled()), "reaction_value_policy": <resolve из env AZ_REACTION_VALUE_POLICY>}` с переданным `extras` (переданные ключи приоритетны). Импорт `phase_obs_features_enabled` из `core.engine.phases.obs_features` (или `core.engine.phases`).
- **`eval.py`:** новая функция-резолвер (напр. `_resolve_phase_obs_for_agent(agent_id) -> None`), вызывается в `main()` до постройки env. Читает контракт агента (если id задан), hyperparams (`alphazero_tree`), выставляет `os.environ`. Использует существующий `resolve_phase_obs_features(env_value=..., cfg_value=...)` (`obs_features.py:50`) для согласованного приоритета env>cfg, плюс верхний приоритет — контракт агента.
- **Чтение hyperparams в eval:** через тот же механизм, что train.py грузит `alphazero_tree` (если eval ещё не грузит hyperparams — добавить чтение `hyperparams.json` → `alphazero_tree.phase_obs_features`; формат и путь — как в train.py `_load_*`/AZ_CFG).

## Тестирование (TDD)
- `make_env_contract` кладёт `phase_obs_features`/`reaction_value_policy` в `extras` (при phase on → `extras["phase_obs_features"]==1`); явно переданный `extras`-ключ не перетирается.
- `obs_space_signature` формат НЕ изменился (`vec:N`, без суффикса) — регресс-тест.
- `compatible_contracts` по-прежнему совпадает для контрактов с одинаковыми sig и разными extras (extras не влияет).
- Резолвер eval: контракт `extras.phase_obs_features=1` → выставляет `PHASE_OBS_FEATURES=1`; нет в extras → берёт hyperparams; нет ни там, ни там → env-var/0. (Юнит-тест функции-резолвера с подменой загрузчика контракта/hyperparams.)
- Legacy: контракт без `extras.phase_obs_features` + hyperparams=1 → резолвится в 1.
- Обновить существующие контракт-тесты, ожидающие пустой/точный `extras` или `contract_hash` (`test_agent_registry_b2_contract`, `test_dqn_dist_contract_extras`, `test_sampled_muzero_registry`) — под новые автодобавляемые extras-ключи.

## Валидация (smoke, на железе)
Запустить тот же eval, что падал (`--learner-agent-id P1_Necrons_only_war_v2_final_ep10_...`, AZ mcts) **без** ручного `PHASE_OBS_FEATURES` → eval должен подняться: лог `[EVAL][AZ][CONFIG] phase_obs_features=1 obs_size=41`, нет `obs_space_signature mismatch`, оценка стартует.

## Риски
- **Тесты на точный contract_hash/extras** сломаются от автодобавления — обязательная часть плана (обновить).
- **Чтение hyperparams в eval** — если eval не грузил hyperparams, добавить аккуратно (тот же путь/формат, что train.py), не сломав запуск без hyperparams (fallback на env-var/0).
- **reaction_value_policy** — кладём для паритета; если выяснится, что он меняет obs (не подтверждено; obs полностью объясняется phase=+24), это всплывёт в smoke (obs≠41) — тогда резолвить и его до env. Базово obs определяет только phase.

## Вне области (долг, не трогаем)
Дублирующая формула obs-сигнатуры `warhamEnv.py:90` (`vec:N+phaseM`) vs `agent_registry.py:168` (`vec:N`) — латентная несогласованность, в eval-пути (registry-формула с обеих сторон) не участвует. Не меняем (смена формата сломала бы существующий `vec:41`-агент).

## Критерии готовности
- `make_env_contract` пишет phase_obs/reaction в extras (формат sig неизменен); eval резолвит phase_obs (контракт→hyperparams→env→0) до постройки env; legacy `vec:41`-агент грузится через hyperparams-фолбэк; все TDD-тесты + обновлённые контракт-тесты зелёные; smoke падавшего eval поднимается без ручного env-var.
