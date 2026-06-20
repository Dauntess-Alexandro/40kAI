# PPO Smart Stratagems — дизайн

> Статус: спека (brainstorming, rev. 2026-06-19). Часть Stage 8 (smart stratagem selection) — PPO-часть.
> Зеркало DQN-части, с честным critic-V вместо max-Q proxy.
> Связанные:
> - `docs/superpowers/specs/2026-06-19-dqn-smart-stratagems-design.md` (**эталон**: та же инфра, max-Q вместо critic),
> - `docs/superpowers/specs/2026-06-19-stratagems-fidelity-and-smart-selection-design.md` (**prerequisite**: фазы A+B),
> - `docs/superpowers/specs/2026-06-19-b3-reaction-value-policy-design.md` (AZ reaction value-policy — переиспользуем инфру),
> - `docs/superpowers/specs/2026-06-17-stage5-stratagem-registry-design.md` (реестр стратагем),
> - `docs/superpowers/specs/2026-06-17-stage7a-reaction-policy-seam-design.md` (seam `env.reaction_policy`).

## 1. Контекст и мотивация

После переделки движка под стратагемы W40k 10e (реестр из 7 стратагем, `stratagem_engine.apply`,
`reaction_policy` seam, `attach_fight_stratagem_plan`, AZ value-gate) и **после того, как DQN и AZ
уже получили умный выбор стратагем**, PPO остаётся «слепым» к стратагемам — даже «слепее» DQN:

1. **PPO контролирует только Insane Bravery** через плоский action-head (`use_cp`/`cp_on`), как и DQN.
   Остальные 6 стратагем (overwatch, smokescreen, go-to-ground, heroic intervention, hungry void,
   command re-roll) движок применяет сам по legacy rule-based триггерам (`reaction_policy=None` —
   «всегда реагировать, если хватает CP»).
2. **`reaction_policy` seam к PPO не подключён.** В `eval.py` / `train.py` value-gate
   (`install_dqn_stratagem_policy`, `dqn_build_fight_plan`) ставится только для DQN; PPO-ветки —
   нет.
3. **Если бы PPO-сеть просто отдали в `reaction_policy`, движок бы упал.** `warhamEnv._simulate_reaction_branch`
   делает duck-typing: `if hasattr(net, "infer_with_value") … else net.infer(obs)`. У
   `ActorCriticMultiHead` нет ни `infer_with_value`, ни `infer` — есть только `forward()→(logits, value)`
   и `act()`. PPO провалился бы в `else`-ветку и крэшнулся на отсутствующем `infer`.

**Преимущество PPO над DQN:** у `ActorCriticMultiHead` есть честный critic-head
(`_value_from_features`, с ensemble-усреднением) → настоящий `V(s)` без max-Q overestimation.

**Цель.** Дать PPO «умный» выбор стратагем: паритет с AZ/DQN по набору (те же 7 стратагем) и по
механике gate'a (apply если `V(apply) > V(pass) + eps`), **без MCTS**, с **critic-V** как источником.

**Не-цели (явно вне первой версии).**
- Не меняем action-space (`action_contract.py`) — `use_cp/cp_on` остаются, маска добивается.
- Не трогаем движок (`stratagems.py`, `stratagem_engine.apply`, `phase_engine`, `warhamEnv`
  фазовые методы, `_simulate_reaction_branch`) — он уже умеет всё нужное.
- Не трогаем DQN/AZ-код — `infer_with_value` у PPO новый и не пересекается.
- Не делаем self-play PPO с умным enemy-side (`selfplay`/`from_opponent`) — Stage 2.
- Не делаем windowed-MCTS на реакциях — это для AZ.

### 1.1 Prerequisite

PPO-bridge опирается на уже залитую фазовую инфру (фиделити A+B стратагем, AZ-reaction-value-policy,
DQN-bridge). Они в `main`/рабочей ветке. Код PPO-bridge движок **не меняет**.

## 2. Принцип дизайна

**Не трогать движок. Не трогать action-space. Переиспользовать AZ/DQN-инфру как есть.**

PPO получает недостающий кусок — `V(s)` для `_simulate_reaction_branch` — через **critic value-head**.
После этого движок сам прокидывает гейт-вызовы через ту же `reaction_policy`, что и у AZ/DQN.

Паритет с AZ/DQN по **точкам входа и семантике gate'a** (те же 7 стратагем, тот же apply/pass
lookahead). Разница: **как считается V(s)** (critic у PPO, max-Q у DQN, value-head у AZ) и
**fight-планировщик** (greedy 2-веточный lookahead у PPO/DQN vs MCTS windows у AZ).

### 2.1 Ключевое упрощение vs DQN: V не зависит от масок

Critic-V — скаляр из features, **не зависит от action-масок**. У DQN max-Q **обязан** маскироваться
(иначе illegal-actions на головах завышают V → gate тратит CP слишком щедро). У PPO этой проблемы нет:

- `ppo_value` строит маски **не нужно** → дешевле и проще, чем `dqn_value`.
- В `infer_with_value` маски нужны только для `probs` (API-симметрия с seam'ом и DQN), для V — игнор.
- Это устраняет один источник смещения, который у DQN компенсируется `eps`.

## 3. Архитектура

### 3.1 Data flow (полный)

```
1. env.reset() → obs
2. actor_critic.act(obs, masks) → actions, logprob, value  (как раньше)
3. action_dict = convertToDict(actions)
4. ЕСЛИ PPO_REACTION_VALUE_POLICY=1 (на каждом step, не только в fight):
     fight_plan = ppo_build_fight_plan(env, ac_net)   # greedy critic-V по 2 веткам на юнит
     attach_fight_stratagem_plan(env, fight_plan)      # plan заберёт fight_phase внутри step
5. env.step(action_dict):
     └─ command_phase:  bravery gate → reaction_policy("insane_bravery") → _simulate_reaction_branch
                        → infer_with_value → V(apply) vs V(pass) → да/нет
     └─ movement/charge: _resolve_overwatch → reaction_policy("overwatch") → V-gate
     └─ shooting:        _maybe_use_smokescreen / _maybe_use_go_to_ground → reaction_policy → V-gate
     └─ charge (end):    _resolve_heroic_intervention → reaction_policy("heroic") → V-gate
     └─ fight_phase:     _apply_pending_fight_stratagem_plan(plan) → Hungry Void / Cmd Re-roll
6. reward → ppo_buffer.push
7. backward по PPO-loss как обычно
```

### 3.2 critic-V для V(s)

`ActorCriticMultiHead.forward(obs) → (logits_list, value)`. `value` — это `_value_from_features`:
для `n_value_ensemble==1` — один head, иначе — `mean` по ensemble. Это и есть `V(s)`:

- честная оценка value (в отличие от DQN max-Q proxy) — без overestimation-смещения;
- mask-независима → `ppo_value` не строит маски;
- работает с любым `n_value_ensemble` (1 или N) — усреднение внутри `_value_from_features`;
- совместима со старыми PPO-чекпойнтами: `infer_with_value` — новый метод, не новый параметр.

### 3.3 Компоненты

| # | Файл | Что меняем | Объём |
|---|------|-----------|-------|
| 1 | `core/models/PPO.py` | Новый метод `ActorCriticMultiHead.infer_with_value(obs, masks_by_head=None) -> (probs, V)`: один `forward`, masked softmax для probs, critic V | ~15 строк |
| 2 | `core/models/ppo_stratagem_bridge.py` (новый) | `ppo_reaction_value_policy_enabled()`, `install_ppo_stratagem_policy`, `ppo_value`, `ppo_build_fight_plan` | ~80 строк |
| 3 | `train.py` (PPO inline + actor-loop + actor-learner spawn `_main_actor_learner`) | `PPO_REACTION_VALUE_POLICY` резолв; install; fight-plan + attach вокруг step | ~30 строк |
| 4 | `eval.py` (PPO-ветка) | install policy + fight_plan attach, по аналогии с DQN-веткой | ~20 строк |
| 5 | `hyperparams.json` | Секция `ppo.reaction_value_policy: 0\|1` (дефолт 1) | 1 ключ |

**Движок (`warhamEnv._simulate_reaction_branch`) — 0 изменений.** Duck-typing
`hasattr(net, "infer_with_value")` уже на месте (`core/envs/warhamEnv.py:4125`). Как только у
`ActorCriticMultiHead` появится `infer_with_value`, seam подхватит PPO автоматически. AZ-net (без
метода) идёт прежним путём `net.infer(obs)`.

### 3.4 Подробности по компонентам

#### 3.4.1 `ActorCriticMultiHead.infer_with_value` (новый метод)

```python
def infer_with_value(self, obs, masks_by_head=None):
    """Как infer/act, но возвращает (probs, V). V — честный critic, mask-независим.

    Нужно для reaction_value_policy: env._simulate_reaction_branch зовёт
    net.infer_with_value(obs, masks_by_head=...) и ждёт (probs, value). У AZ-net этого метода нет
    → duck-typing в env выбирает net.infer. Маски влияют только на probs; critic V их игнорирует.
    """
    logits_list, value = self.forward(obs)
    probs = []
    for idx, logits in enumerate(logits_list):
        mask = masks_by_head[idx] if (masks_by_head is not None and idx < len(masks_by_head)) else None
        probs.append(torch.softmax(_apply_action_mask(logits, mask), dim=1))
    return probs, value
```

`_apply_action_mask` уже есть в `PPO.py` (используется `act`/`evaluate_actions`) — переиспользуем,
он сам обрабатывает `mask is None` и mismatch формы. `forward` не трогаем — он отдаёт `value`,
которым пользуется PPO-обучение; `infer_with_value` лишь добавляет masked-softmax probs поверх.

#### 3.4.2 `core/models/ppo_stratagem_bridge.py` (новый модуль)

Зеркало `dqn_stratagem_bridge.py`, с двумя отличиями: (а) V из critic, (б) `ppo_value` не строит маски.

```python
"""PPO ↔ стратагемы: critic-V, fight-plan builder, policy install.

Переиспользует AZ-инфру (reaction_value_policy, attach_fight_stratagem_plan)
поверх ActorCriticMultiHead.infer_with_value (честный critic V).
"""
from __future__ import annotations

import os

import numpy as np
import torch

from core.engine.phases.stratagem_engine import apply as _apply_stratagem
from core.engine.phases.stratagems import for_phase, usage_limit_reached
from core.engine.phases.types import Phase
from core.models.utils import unwrap_env

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def ppo_reaction_value_policy_enabled(default: str = "1") -> bool:
    raw = str(os.getenv("PPO_REACTION_VALUE_POLICY", default)).strip().lower()
    return raw in _TRUTHY


def install_ppo_stratagem_policy(env, device, net_by_side: dict) -> None:
    """Value-gate для стратагем. Side-generic: net_by_side = {side: net}.

    v1 кладёт {"model": ac_net} (learner-only). Когда eval перейдёт на честные p1/p2,
    тот же вызов принимает {"model": p1_net, "enemy": p2_net} — без правок движка/bridge.
    Сторона без сети (heuristic) → legacy (make_stratagem_value_policy: get(side) is None → True).
    """
    from core.models.reaction_value_policy import make_stratagem_value_policy

    e = unwrap_env(env)
    e._reaction_net_by_side = dict(net_by_side)
    e.reaction_policy = make_stratagem_value_policy(e._reaction_net_by_side, device=device)


def ppo_value(env, ac_net, device, side: str) -> float:
    """critic V(s) для стороны side. Маски не нужны — critic mask-независим."""
    e = unwrap_env(env)
    obs = torch.tensor(
        np.asarray([e.get_observation_for_side(side)], dtype=np.float32),
        device=device,
    )
    with torch.no_grad():
        _, v = ac_net.infer_with_value(obs, masks_by_head=None)
    return float(v.reshape(-1)[0].item())


def ppo_build_fight_plan(env, ac_net, device, side: str = "model") -> dict[int, str]:
    """Hungry Void / Command Re-roll план через critic-V lookahead (2 ветки на юнит).

    Структура 1:1 с dqn_build_fight_plan: snapshot → apply/pass → critic V → выбор.
    Инвариант snapshot: snapshot_state/restore_state покрывают modelCP/enemyCP, stratagem_used,
    active_stratagem_effects, unit_health/enemy_health, unitInAttack.
    """
    e = unwrap_env(env)
    if getattr(e, "_reaction_sim_active", False):
        return {}  # recursion guard
    health = e.unit_health if side == "model" else e.enemy_health
    in_attack = e.unitInAttack if side == "model" else e.enemyInAttack
    plan: dict[int, str] = {}
    eps = 1e-3  # greedy per-unit planner без MCTS-joint → лёгкий уклон в PASS (как у DQN)
    for d in for_phase(Phase.FIGHT):
        cp = int(e.modelCP if side == "model" else e.enemyCP)
        if cp < d.cp_cost:
            continue
        if usage_limit_reached(e, side, d, phase="fight"):
            continue
        for u in range(len(health)):
            if health[u] <= 0 or in_attack[u][0] != 1:
                continue
            if u in plan:
                continue
            snap = e.snapshot_state()
            try:
                with e.simulation_mode():
                    e.restore_state(snap)
                    _apply_stratagem(e, side, d.id, u, phase="fight")
                    v_apply = ppo_value(e, ac_net, device, side)
                    e.restore_state(snap)
                    v_pass = ppo_value(e, ac_net, device, side)
            finally:
                e.restore_state(snap)
            if v_apply > v_pass + eps:
                plan[u] = d.id
    return plan
```

> **eps в fight-plan = 1e-3:** хотя critic честнее max-Q, greedy per-unit планировщик всё равно не
> joint-оптимален (в отличие от AZ MCTS windows) → оставляем тот же мягкий уклон в PASS, что у DQN.
> Реакции — eps=0 (дефолт `make_stratagem_value_policy`, как AZ).

#### 3.4.3 `train.py` — установка gate'a и fight_plan для PPO

**Env-var резолв** (рядом с `DQN_REACTION_VALUE_POLICY` на `train.py:300`):

```python
# Внимание: общий _cfg_raw/_cfg_bool ищут cfg_key в _DQN_CFG, затем в top-level data —
# секции "ppo" они НЕ знают, а cfg_key="reaction_value_policy" совпал бы с DQN-секцией (коллизия).
# Поэтому PPO резолвим вручную из секции data["ppo"] (data — загруженный hyperparams dict в train.py).
_PPO_CFG = data.get("ppo", {}) if isinstance(data, dict) else {}
_ppo_rvp_raw = os.getenv("PPO_REACTION_VALUE_POLICY", str(_PPO_CFG.get("reaction_value_policy", 1)))
PPO_REACTION_VALUE_POLICY = str(_ppo_rvp_raw).strip().lower() in ("1", "true", "yes", "on")
if "PPO_REACTION_VALUE_POLICY" not in os.environ:
    os.environ["PPO_REACTION_VALUE_POLICY"] = "1" if PPO_REACTION_VALUE_POLICY else "0"
```

> Не переиспользуем `_cfg_bool` без правки: его `cfg_key` резолвится по DQN-секции/top-level, а не по
> `ppo`. Ручной резолв из `data["ppo"]` точнее и не трогает общий хелпер. (В runtime PPO-ветки можно
> также звать `ppo_reaction_value_policy_enabled()` из bridge — он читает env, который мы тут выставили.)

**Установка policy** (после создания `actor_critic`, для каждого inline/actor пути —
`train.py:3627`, `3919`, и spawn-путь `_main_actor_learner` рядом с `8213`):

```python
if PPO_REACTION_VALUE_POLICY and not USE_SUBPROC_ENVS:
    from core.models.ppo_stratagem_bridge import install_ppo_stratagem_policy
    for ctx in env_contexts:          # или одиночный env в actor-learner
        install_ppo_stratagem_policy(ctx["env"], device, {"model": actor_critic})
    append_agent_log("[PPO][CONFIG] reaction_value_policy установлена (critic V, learner_only)")
```

**Fight-plan вокруг step** (перед `env.step`, по аналогии с `train.py:5374-5395`):

```python
from core.models.ppo_stratagem_bridge import ppo_build_fight_plan
from core.models.option_candidates import attach_fight_stratagem_plan

if PPO_REACTION_VALUE_POLICY and not USE_SUBPROC_ENVS:
    attach_fight_stratagem_plan(ctx["env"], ppo_build_fight_plan(ctx["env"], actor_critic, device, side="model"))
try:
    next_observation, reward, done, res, info = ctx["env"].step(action_dicts[idx])
finally:
    if PPO_REACTION_VALUE_POLICY and not USE_SUBPROC_ENVS:
        attach_fight_stratagem_plan(ctx["env"], None)
```

> **Spawn-mode (Windows):** `os.environ["PPO_REACTION_VALUE_POLICY"]` прокидывается в actor-процессы;
> **обязательно** дублировать install + fight-plan в `_main_actor_learner` (PPO-ветка, `cpu_net`),
> ровно как DQN на `train.py:8213` и `8383`. Иначе learner и actors разъедутся по семантике стратагем.

#### 3.4.4 `eval.py` — то же для PPO-оценки

После загрузки PPO-чекпойнта (`eval.py:1266+`, рядом с DQN-install `1337`):

```python
if algo == "ppo" and ppo_reaction_value_policy_enabled():
    from core.models.ppo_stratagem_bridge import install_ppo_stratagem_policy
    install_ppo_stratagem_policy(env, device, {"model": policy_net})
    log("[EVAL][PPO][CONFIG] reaction_value_policy установлена (critic V, learner_only)")
```

В `run_episode` PPO-ветке (`eval.py:793`, перед `env.step`):

```python
if algo == "ppo" and ppo_reaction_value_policy_enabled():
    from core.models.ppo_stratagem_bridge import ppo_build_fight_plan
    attach_fight_stratagem_plan(env, ppo_build_fight_plan(env, policy_net, device, side="model"))
# ... env.step ...; в finally — attach_fight_stratagem_plan(env, None)
```

> `ppo_value` / `ppo_build_fight_plan` / `install_ppo_stratagem_policy` живут в общем модуле
> `core/models/ppo_stratagem_bridge.py` (импортируется в train.py, eval.py и тестах — DRY).

## 4. Enemy-сторона: side-generic API (v1 — learner_only, both-sides готов)

**Механизм value-gate уже полностью двусторонний и в этой версии не сегрегирует стороны.**
`make_stratagem_value_policy` резолвит сеть как `net_by_side.get(side)` для *любой* реагирующей
стороны; `_simulate_reaction_branch` зовёт `infer_with_value` сети из `ctx["net"]` той стороны, что
реагирует. Движок и reaction-policy не знают про «learner vs enemy». «Сегрегация» — это **только**
то, какой словарь мы кладём в `_reaction_net_by_side`.

Поэтому `install_ppo_stratagem_policy(env, device, net_by_side)` принимает **словарь side→net** с
первого дня (§3.4.2). В v1 вызыватели кладут `{"model": actor_critic}` (learner-only): enemy без
сети реагирует legacy (`reaction_value_policy.py:21-22`: `get(side) is None → return True`).

### 4.1 Путь к честному both-sides (когда eval перейдёт на p1/p2)

Чтобы убрать сегрегацию и дать обеим сторонам свой value-gate — **ноль изменений в движке, bridge,
`reaction_value_policy`**. Нужно только три точечные правки в харнессе eval (отдельная задача):

1. **Заполнить словарь обеими сетями:** `install_ppo_stratagem_policy(env, device,
   {"model": p1_net, "enemy": p2_net})`.
2. **Отдать сеть оппонента наружу.** Сейчас `build_policy_fn` (`opponent_adapter.py:141-159` для PPO)
   создаёт `net = make_actor_critic(...)`, но прячет его в замыкании `_policy_fn`. Минимальная
   правка: вернуть `(policy_fn, net)` либо положить `net` на `OpponentSpec` — общая для DQN/PPO/AZ
   (у всех есть/будет `infer_with_value`).
3. **Fight-plan для действующей стороны.** `ppo_build_fight_plan(..., side=...)` уже параметризован;
   во время `enemyTurn` строить план для `side="enemy"` через `enemy_net` (сейчас — только `"model"`).

Это намеренно вынесено в eval-рефактор (p1-agent vs p2-agent), а не в PPO-bridge: bridge остаётся
готовым к симметрии, но не тащит в себя переделку eval-харнесса. То же расширение симметрично
применимо к DQN (`install_dqn_stratagem_policy` тогда тоже станет side-generic).

## 5. Точки расширения и совместимость

- **Старые PPO-чекпойнты:** совместимы. `infer_with_value` — новый метод, не новый параметр;
  `load_actor_critic_state_dict(strict=False)` работает. `PHASE_OBS_FEATURES=0` для PPO (через
  `is_az_algo`-guard из DQN-работы) → obs-размер не меняется.
- **DQN/AZ-код:** не трогаем. `infer_with_value` у PPO независим; seam-duck-typing уже общий.
- **`reaction_value_policy.make_stratagem_value_policy`:** не меняем. Generic, уже работает с любым
  `net_by_side`, включая PPO с `infer_with_value`.

## 6. Флаги и окружение

| Флаг | Дефолт | Где | Что |
|------|--------|-----|-----|
| `PPO_REACTION_VALUE_POLICY` | `1` | env + `hyperparams.json` → `ppo.reaction_value_policy` | Включить умные стратагемы для PPO |
| `PHASE_OBS_FEATURES` (для PPO) | `0` (через `is_az_algo`-guard) | env | PPO всегда на чистом obs |

## 7. Тестирование

### 7.1 Юнит-тесты

- **`tests/models/test_ppo_infer_with_value.py`** (новый):
  - tiny `ActorCriticMultiHead`, форма `(probs, V)`, `V.shape == (B,)`, нет NaN/inf.
  - маска влияет на `probs` (illegal → ~0 вероятность), **но не** на `V` (V с маской == V без маски).
  - `n_value_ensemble==1` и `>1` — оба варианта (ensemble усредняется).
  - без масок — fallback (probs = softmax всех логитов).

- **`tests/models/test_ppo_stratagem_bridge.py`** (новый):
  - `ppo_build_fight_plan`: env с eligible-бойцом, fight-стратагема legal, CP хватает;
    stub `ac_net.infer_with_value` → `V(apply) > V(pass)` → план `{u: <strat_id>}`.
  - обратный кейс → план пустой.
  - `usage_limit_reached` срабатывает → пропускается; CP не хватает → пропускается.
  - инвариант snapshot: после вызова `env.modelCP`/`stratagem_used` не меняются.
  - recursion guard: `_reaction_sim_active=True` → план пустой, `infer_with_value` не вызван.

- **`tests/engine/phases/test_simulate_reaction_branch_ppo.py`** (новый):
  - mock PPO-net с `infer_with_value` → `_simulate_reaction_branch` вызывает его (seam-путь PPO).
  - mock AZ-формы (без `infer_with_value`) → прежний путь `net.infer(obs)` не сломан.

### 7.2 Интеграционные тесты

- **`tests/integration/test_ppo_smart_stratagems_e2e.py`** (новый, при наличии integration-набора):
  - tiny `ActorCriticMultiHead` + env + `reaction_policy` из `make_stratagem_value_policy`.
  - сценарий overwatch / bravery / fight-plan: `modelCP` списан, если `V(apply) > V(pass)`.
  - regression: `PPO_REACTION_VALUE_POLICY=0` → `modelCP` списан всегда (legacy).

### 7.3 Регрессия DQN/AZ

- Существующие DQN/AZ reaction-тесты (`test_reaction_overwatch.py`, `test_command_bravery_via_engine.py`,
  `test_reaction_smokescreen.py`, `test_reaction_heroic.py`, `test_hungry_void.py`,
  `test_command_reroll.py`, `test_dqn_*`) **не должны сломаться** — PPO-метод не пересекается,
  seam-duck-typing общий.

### 7.4 Smoke-тест

- `TRAIN_ALGO=ppo`, `PPO_REACTION_VALUE_POLICY=1`, 10-20 шагов:
  - лог `[PPO][CONFIG] reaction_value_policy установлена (critic V, learner_only)` есть.
  - в `LOGS_FOR_AGENTS_TRAIN.md` появляются строки `[STRATAGEM]` со списанным CP.
- `eval.py`, `algo=ppo`, `PPO_REACTION_VALUE_POLICY=1`, **`--games 50`** — тот же CONFIG-лог, без падения.
- `PPO_REACTION_VALUE_POLICY=0` — legacy, `modelCP` списывается всегда, если хватает CP.

## 8. Trade-offs

| Аспект | Что получаем | Цена |
|--------|--------------|------|
| Паритет с AZ/DQN по стратагемам | Все 7 стратагем умно через тот же gate | Fight-план — greedy, не MCTS joint |
| critic как V(s) | Честный value, без max-Q overestimation, mask-независим (нет mask-построения) | Зависит от качества critic (на недообученном PPO V шумит — как и max-Q у DQN) |
| Минимум нового кода | ~145 строк: bridge + `infer_with_value` + train/eval-хуки | Нужно зеркалировать блоки в train(inline/actor/spawn)/eval |
| Snapshot/restore в fight-plan | Корректность (нет side-effects) | +2 forward-pass на eligible-бойца на fight-step (терпимо) |
| `_simulate_reaction_branch` per trigger | Точно как AZ/DQN | +2 forward-pass на решение (общий AZ-паттерн) |
| learner_only в v1 | Простота, не ломаем opponent-провайдеры | Enemy-side без value-gate; eval vs heuristic асимметричен до eval-рефактора (§4.1) |

## 9. Будущие расширения (вне этого плана)

- **Честный both-sides eval (p1/p2):** включается тремя точечными правками харнесса eval — см. §4.1.
  bridge уже side-generic; движок/`reaction_value_policy` не трогаются. Симметрично применимо к DQN.
- **`PPO_REACTION_ENEMY_SIDE=selfplay`** (опц. флаг поверх side-generic API):
  `install_ppo_stratagem_policy(env, device, {"model": ac, "enemy": ac})` — симметричный self-play,
  обе стороны умно реагируют через ту же сеть. Тривиально на текущем API (одна сеть в обе ячейки).
- **Унификация bridge:** `dqn_stratagem_bridge.py` + `ppo_stratagem_bridge.py` → общий
  `stratagem_bridge.py`, параметризованный V-источником (max-Q / critic / value-head).

## 10. Открытые вопросы (решено во время brainstorming)

- ✅ V(s) для PPO: **честный critic value-head** (`_value_from_features`), не max-Q proxy.
- ✅ Маски: critic **mask-независим** → `ppo_value` маски не строит; маски в `infer_with_value` —
  только для probs (API-симметрия).
- ✅ Модуль: **отдельный `ppo_stratagem_bridge.py`** (зеркало DQN), не общий рефакторинг (Stage 2).
- ✅ `PPO_REACTION_VALUE_POLICY` дефолт: **1** (включён).
- ✅ Enemy-сторона: install-API **side-generic с первого дня** (`net_by_side` dict); v1 кладёт
  `{"model": actor_critic}` (learner-only). Both-sides (честный p1/p2) — без правок движка/bridge,
  только харнесс eval (§4.1). Механизм value-gate уже двусторонний.
- ✅ Fight-plan `eps=1e-3` vs reactions `eps=0`: greedy planner без MCTS-joint.
- ✅ Spawn PPO actors: **дублировать hook** в `_main_actor_learner` (PPO-ветка).
- ⏳ GUI-тогглер `ppo.reaction_value_policy` в Qt — **не v1** (достаточно env/hyperparams).
