# Eval arch-parity learner↔opponent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Сделать честный 1:1 в eval по архитектуре сети: opponent строится с той же `arch`, что и learner, во всех путях (последовательный `.pth`, registry-only, parallel-воркер), включая GMZ; рассинхрон арки больше не молчит.

**Architecture:** `arch` сохраняется в registry-meta при обучении (через `extra_meta`), на eval единый резолвер `resolve_arch_for_algo(algo, payload)` достаёт её из `meta` (registry) или из `checkpoint` (legacy `.pth`) для обеих сторон. `build_eval_agent` получает `arch` и `log_fn`; GMZ переходит на `arch`+lenient-загрузчик (как AZ/PPO/SMZ). Загрузчики оппонента получают `log_fn` → missing/unexpected ключи всплывают `[EVAL][WARN]`.

**Tech Stack:** Python 3.12, PyTorch, pytest. Затрагиваются: `core/models/eval_agent.py`, `core/models/opponent_adapter.py`, `eval.py`, `train.py`.

## Global Constraints

- **Язык:** все логи/сообщения/комментарии — русский. Ошибка = что + где + что делать.
- **Платформа:** Windows; запуск тестов `python -m pytest`.
- **ruff-хук** (PostToolUse) срезает временно-неиспользуемые импорты: импорт добавлять ВМЕСТЕ с использованием (или сначала использование, потом импорт).
- **MuZero-тесты жрут ОЗУ:** не гонять `pytest tests/models -k muzero` целиком; новые тесты используют TINY-арки (latent/hidden/embed≈8, num_layers=1) и запускаются точечно.
- **Коммиты:** только после «Все ок» от пользователя; в коммит — лишь релевантный код, без runtime-логов/`runtime/state/*`.
- **Существующая инфраструктура (НЕ переписывать, переиспользовать):**
  - Резолверы: `ppo_arch_from_payload` ([core/models/PPO.py:18](../../core/models/PPO.py)), `alphazero_arch_from_payload` ([core/models/alphazero_model.py:19](../../core/models/alphazero_model.py)), `sampled_muzero_arch_from_payload` ([core/models/sampled_muzero_model.py:32](../../core/models/sampled_muzero_model.py)), `gumbel_muzero_arch_from_payload` ([core/models/gumbel_muzero_model.py:72](../../core/models/gumbel_muzero_model.py)). Все читают `payload.get("arch")` и мёрджат с `*_kwargs_from_env()`.
  - Lenient-загрузчики (`strict=False`, лог через `log_fn`): `load_actor_critic_state_dict` (PPO.py:36), `load_alphazero_state_dict` (alphazero_model.py:37), `load_sampled_muzero_state_dict`, `load_gumbel_muzero_state_dict` (gumbel_muzero_model.py:96).
  - `make_gumbel_muzero_net(obs_dim, action_sizes, **overrides)` (gumbel_muzero_model.py:84) — мёрджит env-kwargs + overrides.
  - `save_agent_artifact(..., extra_meta=...)` (agent_registry.py:341) → `meta.update(extra_meta)` → пишет в `meta.json`; `load_agent_by_id` (agent_registry.py:487) возвращает `payload["meta"]`.

### Известное ограничение (зафиксировать, не чинить здесь)
Агенты, обученные ДО этого фикса, не имеют `arch` в meta → для них обе стороны падают на env-дефолтную арку (как сегодня, симметрично). 1:1 для недефолтной арки гарантируется только для агентов, обученных ПОСЛЕ Task 6. Альтернатива (инференс арки из формы state_dict, как `infer_dqn_arch_from_state_dict`) — отдельный тикет, в этот план не входит.

---

## File Structure

- `core/models/eval_agent.py` — **новый** `resolve_arch_for_algo()`; правка `build_eval_agent` (param `log_fn`, GMZ-ветка на arch+lenient).
- `core/models/opponent_adapter.py` — поле `arch` в `OpponentSpec`; извлечение в `load_agent_opponent`.
- `eval.py` — последовательный путь (learner/opponent: arch-источник + `log_fn`) и parallel-воркер `_build_eval_runtime_for_worker`.
- `train.py` — `"arch"` в `extra_meta` пяти вызовов `save_agent_artifact` (PPO×2, AZ, GMZ, SMZ).
- Тесты: `tests/models/test_eval_arch_parity.py` (**новый**), расширение `tests/models/test_eval_agent.py`.

---

### Task 1: `resolve_arch_for_algo` — единый резолвер арки

**Files:**
- Modify: `core/models/eval_agent.py` (добавить функцию рядом с `build_eval_agent`, ~после строки 303)
- Test: `tests/models/test_eval_arch_parity.py`

**Interfaces:**
- Produces: `resolve_arch_for_algo(algo: str, payload: dict | None) -> dict | None` — для dqn → `None` (арка инферится из state_dict); для ppo/az(вкл. gumbel_az)/gumbel_muzero/sampled_muzero → dict kwargs из соответствующего `*_arch_from_payload(payload)`. `payload` — любой dict с ключом `"arch"` (checkpoint `.pth` ИЛИ registry `meta`).

- [ ] **Step 1: Написать падающий тест**

```python
# tests/models/test_eval_arch_parity.py
from core.models.eval_agent import resolve_arch_for_algo


def test_resolve_arch_for_algo_dispatch():
    # dqn — арка инферится из state_dict, отдельная arch не нужна
    assert resolve_arch_for_algo("dqn", {"arch": {"hidden_size": 8}}) is None
    # ppo — мёрдж с env-дефолтами, ключи из payload переопределяют
    ppo = resolve_arch_for_algo("ppo", {"arch": {"hidden_size": 17, "num_layers": 1}})
    assert ppo["hidden_size"] == 17 and ppo["num_layers"] == 1
    # alphazero_tree
    az = resolve_arch_for_algo("alphazero_tree", {"arch": {"hidden_size": 19}})
    assert az["hidden_size"] == 19
    # gumbel_muzero
    gmz = resolve_arch_for_algo("gumbel_muzero", {"arch": {"latent_dim": 8, "num_layers": 1}})
    assert gmz["latent_dim"] == 8 and gmz["num_layers"] == 1
    # sampled_muzero
    smz = resolve_arch_for_algo("sampled_muzero", {"arch": {"hidden_dim": 8}})
    assert smz["hidden_dim"] == 8
    # пустой payload → None или env-дефолты (не падает)
    assert resolve_arch_for_algo("ppo", None) is None or isinstance(resolve_arch_for_algo("ppo", None), dict)
```

- [ ] **Step 2: Запустить тест — убедиться, что падает**

Run: `python -m pytest tests/models/test_eval_arch_parity.py::test_resolve_arch_for_algo_dispatch -q`
Expected: FAIL — `ImportError: cannot import name 'resolve_arch_for_algo'`.

- [ ] **Step 3: Реализовать функцию**

В `core/models/eval_agent.py`, сразу после сигнатуры/докстринга модуля рядом с `build_eval_agent` (после `_parse_contract_sizes`, ~строка 304):

```python
def resolve_arch_for_algo(algo: str, payload: dict | None) -> dict | None:
    """Единый резолв арки сети для eval (learner и opponent — один путь).

    payload — dict с ключом 'arch' (checkpoint .pth ИЛИ registry meta). Для dqn
    арка инферится из state_dict в build_eval_agent → возвращаем None. Если payload
    без 'arch' — резолвер вернёт env-дефолты (как и для legacy learner).
    """
    a = str(algo or "").strip().lower()
    if not isinstance(payload, dict) or not payload.get("arch"):
        return None
    if a == "ppo":
        from core.models.PPO import ppo_arch_from_payload
        return ppo_arch_from_payload(payload)
    if is_alphazero_net_algo(a):
        from core.models.alphazero_model import alphazero_arch_from_payload
        return alphazero_arch_from_payload(payload)
    if a == "gumbel_muzero":
        from core.models.gumbel_muzero_model import gumbel_muzero_arch_from_payload
        return gumbel_muzero_arch_from_payload(payload)
    if a == "sampled_muzero":
        from core.models.sampled_muzero_model import sampled_muzero_arch_from_payload
        return sampled_muzero_arch_from_payload(payload)
    return None  # dqn и прочее
```

- [ ] **Step 4: Запустить тест — должен пройти**

Run: `python -m pytest tests/models/test_eval_arch_parity.py::test_resolve_arch_for_algo_dispatch -q`
Expected: PASS.

- [ ] **Step 5: Коммит** (после «Все ок»)

```bash
git add core/models/eval_agent.py tests/models/test_eval_arch_parity.py
git commit -m "feat(eval): resolve_arch_for_algo — единый резолв арки learner/opponent"
```

---

### Task 2: `build_eval_agent` — GMZ на arch+lenient + параметр `log_fn`

**Files:**
- Modify: `core/models/eval_agent.py` (сигнатура `build_eval_agent` ~306-315; GMZ-ветка 421-453; AZ-ветка 386; PPO 363; SMZ 475)
- Test: `tests/models/test_eval_arch_parity.py`

**Interfaces:**
- Consumes: `resolve_arch_for_algo` (Task 1).
- Produces: `build_eval_agent(*, algo, policy_state, contract, len_model, cfg=None, device=..., arch=None, log_fn=None) -> EvalAgent`. Новый kwarg `log_fn: Callable[[str], None] | None`. GMZ грузится lenient (`strict=False`) и уважает `arch` (вкл. `num_layers`).

- [ ] **Step 1: Написать падающий тест (GMZ недефолтная арка грузится 1:1 + WARN при рассинхроне)**

```python
# tests/models/test_eval_arch_parity.py  (добавить)
from core.models.action_contract import action_sizes_from_env
from core.models.eval_agent import build_eval_agent, resolve_eval_search_cfg
from core.models.gumbel_muzero_model import make_gumbel_muzero_net
from tests.engine.phases._helpers import build_env


def _contract(env):
    n_obs = len(env.get_observation_for_side("model"))
    sizes = action_sizes_from_env(env, len(env.model))
    return {
        "obs_space_signature": f"vec:{n_obs}",
        "action_space_signature": "heads:" + ",".join(str(int(s)) for s in sizes),
    }


def test_build_eval_agent_gmz_nondefault_arch_loads_1to1():
    # GMZ learner-чекпойнт с НЕдефолтной аркой (вкл. num_layers) грузится без потерь.
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_obs = len(env.get_observation_for_side("model"))
    n_actions = action_sizes_from_env(env, len(env.model))
    tiny = {"latent_dim": 8, "hidden_dim": 8, "num_layers": 1, "action_embed_dim": 8}
    net = make_gumbel_muzero_net(n_obs, n_actions, **tiny)

    warns: list[str] = []
    agent = build_eval_agent(
        algo="gumbel_muzero",
        policy_state=net.state_dict(),
        contract=_contract(env),
        len_model=len(env.model),
        cfg=resolve_eval_search_cfg("gumbel_muzero"),
        arch=dict(tiny),
        log_fn=warns.append,
    )
    # 1:1: ни одного [GMZ][WARN] про missing/unexpected
    assert not any("missing" in w for w in warns), warns
    action, plan = agent.select_action(env, "model")
    assert isinstance(action, dict)


def test_build_eval_agent_gmz_arch_mismatch_warns():
    # Без arch (env-дефолт 256) на TINY-весах → lenient-загрузка + видимый WARN, без краша.
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_obs = len(env.get_observation_for_side("model"))
    n_actions = action_sizes_from_env(env, len(env.model))
    tiny = {"latent_dim": 8, "hidden_dim": 8, "num_layers": 1, "action_embed_dim": 8}
    net = make_gumbel_muzero_net(n_obs, n_actions, **tiny)

    warns: list[str] = []
    build_eval_agent(
        algo="gumbel_muzero",
        policy_state=net.state_dict(),
        contract=_contract(env),
        len_model=len(env.model),
        cfg=resolve_eval_search_cfg("gumbel_muzero"),
        arch=None,            # ← рассинхрон арки
        log_fn=warns.append,  # ← должен всплыть WARN, не краш (strict бы упал)
    )
    assert any("missing" in w or "unexpected" in w for w in warns), warns
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/models/test_eval_arch_parity.py -q -k gmz`
Expected: FAIL — `build_eval_agent() got an unexpected keyword argument 'log_fn'` (и/или strict-краш `Error(s) in loading state_dict` во втором тесте).

- [ ] **Step 3: Реализация**

(3a) Сигнатура `build_eval_agent` — добавить `log_fn`:

```python
def build_eval_agent(
    *,
    algo: str,
    policy_state: dict,
    contract: dict,
    len_model: int,
    cfg: EvalSearchCfg | None = None,
    device=torch.device("cpu"),
    arch: dict | None = None,
    log_fn=None,
) -> EvalAgent:
```

(3b) AZ-ветка — заменить эвристику `print if arch else None` на `log_fn`:

```python
        load_alphazero_state_dict(net, normalize_state_dict(policy_state), log_fn=log_fn)
```

(3c) PPO-ветка (строка 363) — прокинуть `log_fn`:

```python
        load_actor_critic_state_dict(net, normalize_state_dict(policy_state), log_fn=log_fn)
```

(3d) SMZ-ветка (строка 475) — прокинуть `log_fn`:

```python
        load_sampled_muzero_state_dict(net, normalize_state_dict(policy_state), log_fn=log_fn)
```

(3e) GMZ-ветка (421-453) — заменить прямую сборку+strict-load на `make_gumbel_muzero_net(**arch)`+lenient:

```python
    if algo == "gumbel_muzero":
        from core.models.gumbel_muzero_model import (
            load_gumbel_muzero_state_dict,
            make_gumbel_muzero_net,
        )
        from core.models.gumbel_muzero_search import GumbelMuZeroSearch, GumbelMuZeroSearchConfig

        # arch из payload (learner/opponent) → недефолтные чекпойнты грузятся 1:1; иначе env-дефолт.
        net = make_gumbel_muzero_net(
            int(n_obs), [int(x) for x in n_actions], **(arch or {})
        ).to(device)
        # Лениентный загрузчик (strict=False) вместо net.load_state_dict — фикс краха на недефолтной арке.
        load_gumbel_muzero_state_dict(net, normalize_state_dict(policy_state), log_fn=log_fn)
        net.eval()
        mode = str(search_cfg.get("mode", "search")).strip().lower()
        search = None
        if mode != "greedy":
            search = GumbelMuZeroSearch(
                net=net,
                config=GumbelMuZeroSearchConfig(
                    num_simulations=max(1, int(search_cfg.get("num_simulations", 32))),
                    root_top_k=max(1, int(search_cfg.get("root_top_k", 8))),
                    temperature=float(search_cfg.get("temperature", 0.10)),
                ),
                device=device,
            )
        return EvalAgent(
            algo=algo,
            net=net,
            reaction_net=_reaction_net_for_algo(algo, net),
            search=search,
            cfg=cfg,
            len_model=len_model,
        )
```

- [ ] **Step 4: Запустить тесты GMZ + регрессию файла**

Run: `python -m pytest tests/models/test_eval_arch_parity.py tests/models/test_eval_agent.py -q`
Expected: PASS (новые GMZ-тесты + старые 5 тестов eval_agent не сломаны — `log_fn` имеет дефолт `None`).

- [ ] **Step 5: Коммит** (после «Все ок»)

```bash
git add core/models/eval_agent.py tests/models/test_eval_arch_parity.py
git commit -m "feat(eval): build_eval_agent — log_fn + GMZ на arch/lenient-загрузчик"
```

---

### Task 3: `OpponentSpec.arch` + извлечение в `load_agent_opponent`

**Files:**
- Modify: `core/models/opponent_adapter.py` (`OpponentSpec` 11-16; `load_agent_opponent` 42-69)
- Test: `tests/models/test_eval_arch_parity.py`

**Interfaces:**
- Consumes: `resolve_arch_for_algo` (Task 1).
- Produces: `OpponentSpec.arch: dict | None`. `load_agent_opponent(...)` заполняет `arch = resolve_arch_for_algo(algo, meta)` (meta — из registry-payload).

- [ ] **Step 1: Падающий тест (регистрируем TINY-агента с arch в meta → OpponentSpec.arch заполнен)**

```python
# tests/models/test_eval_arch_parity.py  (добавить)
import torch
from core.engine.agent_registry import AgentIdentity, save_agent_artifact
from core.engine.make_env_contract import make_env_contract  # см. фактический путь helper'а
from core.models.opponent_adapter import load_agent_opponent
from core.models.sampled_muzero_model import make_sampled_muzero_net
from core.models.utils import normalize_state_dict


def test_load_agent_opponent_carries_arch(tmp_path, monkeypatch):
    # Изолируем registry в tmp (как tests/engine/test_sampled_muzero_registry.py).
    import core.engine.agent_registry as ar
    monkeypatch.setattr(ar, "AGENTS_ROOT", str(tmp_path / "agents"))
    monkeypatch.setattr(ar, "AGENTS_REGISTRY_PATH", str(tmp_path / "agents_registry.json"))

    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_obs = len(env.get_observation_for_side("model"))
    n_actions = action_sizes_from_env(env, len(env.model))
    tiny = {"latent_dim": 8, "hidden_dim": 8, "num_layers": 1, "action_embed_dim": 8}
    net = make_sampled_muzero_net(n_obs, n_actions, **tiny)
    contract = make_env_contract(n_observations=n_obs, n_actions=n_actions,
                                 mission_name="only_war", ruleset_version="only_war_v2")
    identity = AgentIdentity(side="P2", faction="space_marines", ruleset_version="only_war_v2")
    save_agent_artifact(
        identity=identity, agent_id="t-smz-tiny", env_contract=contract,
        policy_state_dict=normalize_state_dict(net.state_dict()),
        extra_meta={"algo": "sampled_muzero", "arch": dict(tiny)},
    )

    spec = load_agent_opponent(agent_id="t-smz-tiny", expected_contract=contract)
    assert spec.algo == "sampled_muzero"
    assert isinstance(spec.arch, dict)
    assert spec.arch["latent_dim"] == 8 and spec.arch["num_layers"] == 1
```

> ⚠️ Перед реализацией уточнить фактические импорты (`make_env_contract`, `AgentIdentity` поля) по `tests/engine/test_sampled_muzero_registry.py:30-92` — там рабочий образец; скопировать оттуда конструкцию identity/contract один-в-один.

- [ ] **Step 2: Запустить — падает**

Run: `python -m pytest tests/models/test_eval_arch_parity.py::test_load_agent_opponent_carries_arch -q`
Expected: FAIL — `AttributeError: 'OpponentSpec' object has no attribute 'arch'`.

- [ ] **Step 3: Реализация**

(3a) `OpponentSpec` — добавить поле:

```python
@dataclass(frozen=True)
class OpponentSpec:
    agent_id: str
    algo: str
    contract: dict[str, Any]
    policy_state: dict[str, Any]
    arch: dict[str, Any] | None = None
```

(3b) `load_agent_opponent` — извлечь arch из meta и положить в spec (вернуть в `return OpponentSpec(...)`):

```python
    meta = payload.get("meta") if isinstance(payload, dict) else {}
    from core.models.eval_agent import resolve_arch_for_algo
    arch = resolve_arch_for_algo(str(algo), meta if isinstance(meta, dict) else {})

    return OpponentSpec(
        agent_id=str(agent_id),
        algo=str(algo),
        contract=dict(contract or {}),
        policy_state=normalize_state_dict(policy_state),
        arch=arch,
    )
```

> Примечание: `meta` уже доступен в payload (см. `load_agent_by_id` → `payload["meta"]`). Импорт `resolve_arch_for_algo` — ленивый (внутри функции), чтобы избежать цикла: `eval_agent` не импортит `opponent_adapter` на уровне модуля.

- [ ] **Step 4: Запустить — пройдёт**

Run: `python -m pytest tests/models/test_eval_arch_parity.py::test_load_agent_opponent_carries_arch -q`
Expected: PASS.

- [ ] **Step 5: Коммит** (после «Все ок»)

```bash
git add core/models/opponent_adapter.py tests/models/test_eval_arch_parity.py
git commit -m "feat(eval): OpponentSpec.arch — load_agent_opponent извлекает арку из registry-meta"
```

---

### Task 4: eval.py (последовательный путь) — arch для обеих сторон + log_fn + источник meta/checkpoint

**Files:**
- Modify: `eval.py` (learner registry-блок ~1598-1632; opponent build 1643-1650; learner arch 1700-1722; reaction-блок 1724+)
- Test: `tests/models/test_eval_arch_parity.py` (build-level honesty)

**Interfaces:**
- Consumes: `resolve_arch_for_algo` (Task 1), `OpponentSpec.arch` (Task 3), `build_eval_agent(log_fn=...)` (Task 2).
- Produces: learner и opponent в последовательном eval строятся с корректной `arch` и общим `log_fn=log`.

- [ ] **Step 1: Тест честного 1:1 на уровне сборки (learner и opponent для одного TINY-агента грузятся без потерь)**

```python
# tests/models/test_eval_arch_parity.py  (добавить)
def test_learner_and_opponent_build_1to1_for_nondefault_arch(tmp_path, monkeypatch):
    # Эмулируем eval-сборку обеих сторон из ОДНОГО registry-агента с недефолтной аркой.
    import core.engine.agent_registry as ar
    monkeypatch.setattr(ar, "AGENTS_ROOT", str(tmp_path / "agents"))
    monkeypatch.setattr(ar, "AGENTS_REGISTRY_PATH", str(tmp_path / "agents_registry.json"))

    env = build_env(); env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_obs = len(env.get_observation_for_side("model"))
    n_actions = action_sizes_from_env(env, len(env.model))
    tiny = {"latent_dim": 8, "hidden_dim": 8, "num_layers": 1, "action_embed_dim": 8}
    net = make_sampled_muzero_net(n_obs, n_actions, **tiny)
    contract = make_env_contract(n_observations=n_obs, n_actions=n_actions,
                                 mission_name="only_war", ruleset_version="only_war_v2")
    identity = AgentIdentity(side="P2", faction="space_marines", ruleset_version="only_war_v2")
    save_agent_artifact(identity=identity, agent_id="t-smz", env_contract=contract,
                        policy_state_dict=normalize_state_dict(net.state_dict()),
                        extra_meta={"algo": "sampled_muzero", "arch": dict(tiny)})

    # learner: арка из meta (registry-путь)
    payload = ar.load_agent_by_id("t-smz")
    learner_arch = resolve_arch_for_algo("sampled_muzero", payload["meta"])
    lw: list[str] = []
    build_eval_agent(algo="sampled_muzero", policy_state=payload["policy_state"],
                     contract=contract, len_model=len(env.model),
                     cfg=resolve_eval_search_cfg("sampled_muzero"), arch=learner_arch, log_fn=lw.append)
    # opponent: арка из OpponentSpec
    spec = load_agent_opponent(agent_id="t-smz", expected_contract=contract)
    ow: list[str] = []
    build_eval_agent(algo=spec.algo, policy_state=spec.policy_state, contract=spec.contract,
                     len_model=len(env.enemy), cfg=resolve_eval_search_cfg(spec.algo),
                     arch=spec.arch, log_fn=ow.append)
    assert not any("missing" in w for w in lw), lw
    assert not any("missing" in w for w in ow), ow
```

- [ ] **Step 2: Запустить — должен пройти уже после Task 1-3** (это «защёлка» инварианта; если падает — баг в Task 1-3)

Run: `python -m pytest tests/models/test_eval_arch_parity.py::test_learner_and_opponent_build_1to1_for_nondefault_arch -q`
Expected: PASS. (Тест фиксирует контракт, который eval.py обязан соблюсти проводкой ниже.)

- [ ] **Step 3: Проводка в eval.py**

(3a) Hoist `meta` (чтобы был доступен на строке ~1700). Перед блоком `if selected_agent_id:` (строка 1601) добавить:

```python
    meta = {}
```
и убрать локальное `meta = payload.get("meta") ...` затенение — оставить присваивание внутри блока как есть (оно перезапишет hoisted `{}`).

(3b) Opponent build (1643-1650) — добавить `arch` и `log_fn`:

```python
            opponent_agent = build_eval_agent(
                algo=opp.algo,
                policy_state=opp.policy_state,
                contract=opp.contract,
                len_model=len(enemy_units),
                cfg=resolve_eval_search_cfg(opp.algo),
                device=device,
                arch=opp.arch,
                log_fn=log,
            )
```

(3c) Learner arch (заменить блок 1700-1713) — единый источник через резолвер:

```python
    # Арку learner резолвим единым путём: registry → meta, legacy .pth → checkpoint.
    # Тот же resolve_arch_for_algo, что и для opponent (честный 1:1, вкл. gumbel_muzero).
    arch_source = meta if selected_agent_id else (checkpoint if isinstance(checkpoint, dict) else {})
    learner_arch = resolve_arch_for_algo(algo, arch_source)
```
Импорт в шапке eval.py (рядом с `from core.models.eval_agent import build_eval_agent, resolve_eval_search_cfg`):
```python
    from core.models.eval_agent import build_eval_agent, resolve_arch_for_algo, resolve_eval_search_cfg
```

(3d) Learner build (1714-1722) — добавить `log_fn=log`:

```python
    learner_agent = build_eval_agent(
        algo=algo,
        policy_state=normalize_state_dict(learner_state),
        contract=eval_contract,
        len_model=len(model_units),
        cfg=cfg,
        device=device,
        arch=learner_arch,
        log_fn=log,
    )
```

- [ ] **Step 4: Прогон тестов + быстрый импорт-смоук eval.py**

Run: `python -m pytest tests/models/test_eval_arch_parity.py tests/test_eval_honest_symmetry.py -q`
Run: `python -c "import eval"`
Expected: PASS; импорт без ошибок.

- [ ] **Step 5: Коммит** (после «Все ок»)

```bash
git add eval.py tests/models/test_eval_arch_parity.py
git commit -m "feat(eval): последовательный eval — arch+log_fn для learner и opponent (registry/.pth)"
```

---

### Task 5: eval.py parallel-воркер — arch для обеих сторон

**Files:**
- Modify: `eval.py` `_build_eval_runtime_for_worker` (learner build 488-495; opponent build 501-508)
- Test: покрыт build-level тестом Task 4 (та же `build_eval_agent`-проводка); добавить точечный тест источника арки воркера если воркер-функция импортируема.

**Interfaces:**
- Consumes: `resolve_arch_for_algo`, `OpponentSpec.arch`, `build_eval_agent`.
- Produces: parallel-воркер строит обе стороны с `arch`.

- [ ] **Step 1: Реализация learner (488-495)** — арка из meta, `log_fn=None` (субпроцесс; WARN не критичен — registry-агенты уже несут корректную арку):

```python
    learner_arch = resolve_arch_for_algo(algo, meta if isinstance(meta, dict) else {})
    learner_agent = build_eval_agent(
        algo=algo,
        policy_state=normalize_state_dict(policy_state),
        contract=eval_contract,
        len_model=len(model_units),
        cfg=resolve_eval_search_cfg(algo),
        device=device,
        arch=learner_arch,
    )
```
> `meta` уже извлекается на строке 481 (`meta = payload.get("meta") ...`).

- [ ] **Step 2: Реализация opponent (501-508)** — арка из spec:

```python
        opponent_agent = build_eval_agent(
            algo=opp.algo,
            policy_state=opp.policy_state,
            contract=opp.contract,
            len_model=len(enemy_units),
            cfg=resolve_eval_search_cfg(opp.algo),
            device=device,
            arch=opp.arch,
        )
```

- [ ] **Step 3: Импорт `resolve_arch_for_algo` в области воркера** (если шапка eval.py уже импортит из Task 4 — переиспользовать; иначе добавить в импорт-блок eval.py).

- [ ] **Step 4: Прогон**

Run: `python -m pytest tests/models/test_eval_arch_parity.py -q`
Run: `python -c "import eval"`
Expected: PASS; импорт ок.

- [ ] **Step 5: Коммит** (после «Все ок»)

```bash
git add eval.py
git commit -m "feat(eval): parallel-воркер — arch для learner и opponent (1:1 в parallel-пути)"
```

---

### Task 6: train.py — писать `arch` в registry-meta (PPO/AZ/GMZ/SMZ)

**Files:**
- Modify: `train.py` — `extra_meta` пяти вызовов `save_agent_artifact`: PPO actor_learner (~5067), PPO final (~5256), AZ final (~7475), GMZ final (~8955), SMZ final (~9718). (DQN — не нужно: арка инферится из state_dict.)
- Test: `tests/train/test_agent_meta_arch.py` (**новый**, лёгкий — без полного train)

**Interfaces:**
- Produces: meta.json зарегистрированных агентов содержит `"arch"` (kwargs сети) → eval-оппонент/learner получают 1:1.

- [ ] **Step 1: Падающий тест (source-guard: каждая ветка extra_meta содержит arch)**

Прецедент source-теста — `tests/train/test_train_side_selection.py`.

```python
# tests/train/test_agent_meta_arch.py
import re
from pathlib import Path


def _extra_meta_blocks(src: str) -> list[str]:
    # Грубо выделяем тело каждого extra_meta={ ... } (до парной }), для проверки наличия "arch".
    blocks = []
    for m in re.finditer(r"extra_meta=\{", src):
        i = m.end(); depth = 1
        while i < len(src) and depth:
            depth += src[i] == "{"; depth -= src[i] == "}"; i += 1
        blocks.append(src[m.start():i])
    return blocks


def test_train_writes_arch_into_agent_meta():
    src = Path("train.py").read_text(encoding="utf-8")
    blocks = _extra_meta_blocks(src)
    assert blocks, "не найдено ни одного extra_meta={...} в train.py"
    # У каждого алго-агента (кроме dqn) extra_meta должен нести 'arch'.
    for b in blocks:
        m = re.search(r'"algo":\s*"([^"]+)"', b) or re.search(r'"algo":\s*([A-Z_]+)', b)
        algo = (m.group(1) if m else "").lower()
        if "dqn" in algo:
            continue
        if any(a in b for a in ("ppo", "alphazero", "gumbel_muzero", "sampled_muzero")):
            assert '"arch"' in b, f"extra_meta без arch для блока:\n{b[:200]}"
```

> Если в каком-то блоке `"algo"` берётся из переменной (`TRAIN_ALGO`), тест мягко пропускает по отсутствию явного dqn — поэтому проверяем по наличию алго-маркеров. При неоднозначности — адаптировать ассерт под реальную форму блока AZ (`"algo": TRAIN_ALGO`).

- [ ] **Step 2: Запустить — падает**

Run: `python -m pytest tests/train/test_agent_meta_arch.py -q`
Expected: FAIL — в текущих extra_meta нет `"arch"`.

- [ ] **Step 3: Реализация — добавить `"arch"` в каждый extra_meta**

PPO (оба вызова, ~5067 и ~5256) — у train уже есть `actor_critic` и `_ppo_arch_dict`:
```python
                "arch": _ppo_arch_dict(actor_critic),
```
AZ (~7475) — рядом используется `az_kw` (см. checkpoint-запись train.py:6767):
```python
            "arch": dict(az_kw),
```
GMZ (~8955):
```python
            "arch": gumbel_muzero_kwargs_from_env(),
```
SMZ (~9718):
```python
            "arch": sampled_muzero_kwargs_from_env(),
```
> Перед правкой убедиться, что соответствующая переменная (`az_kw`/`actor_critic`) в области видимости вызова `save_agent_artifact`; если AZ использует другое имя kwargs — взять то, что строит сеть в этой функции (грепнуть `make_alphazero_net(` в теле AZ-learner).

- [ ] **Step 4: Запустить — пройдёт + интеграционная защёлка**

Run: `python -m pytest tests/train/test_agent_meta_arch.py -q`
Expected: PASS.
Доп. (если позволяет ОЗУ, точечно): запустить самый лёгкий из существующих smoke с регистрацией агента и проверить meta.json вручную — НЕ обязательно для гейта.

- [ ] **Step 5: Коммит** (после «Все ок»)

```bash
git add train.py tests/train/test_agent_meta_arch.py
git commit -m "feat(train): писать arch сети в registry-meta агента (PPO/AZ/GMZ/SMZ) для честного eval 1:1"
```

---

## Self-Review

**Spec coverage:**
- Паритет оппонента (Q1) → Task 3 (OpponentSpec.arch) + Task 4/5 (build с arch). ✓
- Унификация registry/parallel (Q1) → Task 4 (learner meta-источник) + Task 5 (parallel обе стороны) + Task 6 (arch в meta). ✓
- GMZ (Q2) → Task 1 (gumbel-ветка резолвера) + Task 2 (build GMZ на arch+lenient) + Task 6 (GMZ arch в meta) + Task 4 (gumbel в learner arch через общий резолвер). ✓
- WARN-видимость (Q3) → Task 2 (log_fn в загрузчиках) + Task 4 (log_fn=log обеим сторонам). ✓

**Placeholder scan:** код во всех code-шагах конкретный; помечены 2 места «уточнить по образцу» (импорты registry-теста в Task 3; имя kwargs AZ в Task 6) — это указания свериться с существующим кодом, не заглушки логики.

**Type consistency:** `resolve_arch_for_algo(algo, payload) -> dict|None` используется идентично в Task 3/4/5; `build_eval_agent(..., arch, log_fn)` — единая сигнатура из Task 2 во всех вызовах; `OpponentSpec.arch: dict|None` из Task 3 потребляется в Task 4/5.

**Порядок задач:** 1 → 2 → 3 → 4 → 5 → 6. Task 4 build-level тест зелёный уже после 1-3 (фиксирует инвариант перед проводкой). Task 6 независим (можно делать раньше), но логически последний — включает фикс «в будущее».
