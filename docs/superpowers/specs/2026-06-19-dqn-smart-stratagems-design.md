# DQN Smart Stratagems — дизайн

> Статус: спека (brainstorming, rev. 2026-06-19). Часть Stage 8 (smart stratagem selection) — DQN-часть.
> Связанные:
> - `docs/superpowers/specs/2026-06-19-stratagems-fidelity-and-smart-selection-design.md` (**prerequisite**: фазы A+B),
> - `docs/superpowers/specs/2026-06-19-b3-reaction-value-policy-design.md` (AZ reaction value-policy — переиспользуем инфру),
> - `docs/superpowers/specs/2026-06-17-stage5-stratagem-registry-design.md` (реестр стратагем),
> - `docs/superpowers/specs/2026-06-17-stage7a-reaction-policy-seam-design.md` (seam `env.reaction_policy`).

## 1. Контекст и мотивация

После переделки движка под стратагемы W40k 10e (реестр из 7 стратагем, `stratagem_engine.apply`,
`reaction_policy` seam, `attach_fight_stratagem_plan`, AZ value-gate) **DQN остался «слепым» к
стратагемам**: через плоский action-head `use_cp/cp_on` агент контролирует **только Insane Bravery**
(`use_cp=1`), а все остальные 6 стратагем движок применяет сам по rule-based триггерам с
`reaction_policy=None` (legacy «всегда реагировать, если хватает CP»).

Подробности см. в аудите `[audit: dqn-stratagems-after-engine-rework]` (та же сессия).

**Цель.** Дать DQN «умный» выбор стратагем: паритет с AZ по набору (те же 7 стратагем) и по
механике gate'a (apply если `V(apply) > V(pass) + eps`), **без MCTS**.

**Не-цели (явно вне первой версии).**
- Не меняем action-space (`action_contract.py`) — `use_cp/cp_on` остаются, маска добивается.
- Не трогаем движок (`stratagems.py`, `stratagem_engine.apply`, `phase_engine`, `warhamEnv`
  фазовые методы) — он уже умеет всё нужное.
- Не трогаем PPO — это отдельная задача, если потребуется.
- Не делаем self-play DQN с умным enemy-side (`from_opponent`/`selfplay`) — Stage 2.
- Не делаем windowed-MCTS на реакциях (`reaction_windows.py`, Stage 8.5+) — это для AZ.

### 1.1 Prerequisite (порядок работ)

DQN-bridge **не начинаем**, пока не залита
[`2026-06-19-stratagems-fidelity-and-smart-selection-design.md`](2026-06-19-stratagems-fidelity-and-smart-selection-design.md):

1. **Фаза A** — правила 10e (overwatch 24"/LOS, single reroll, hungry_void gates, stealth/invuln и т.д.).
2. **Фаза B** — единый value-гейт в движке (bravery/fight/reactions через `reaction_policy`,
   windowed-дыра для fight-стратагем закрыта).

Иначе DQN будет «умно» гейтить по устаревшим триггерам и eligibility. Код DQN-bridge движок
**не меняет**, но семантика gate'а и `for_phase`/`usage_limit_reached` должны быть финальными.

## 2. Принцип дизайна

**Не трогать движок. Не трогать action-space. Переиспользовать AZ-инфру как есть.**

DQN получает недостающий кусок — `V(s)` для `_simulate_reaction_branch` — через max-Q proxy.
После этого движок сам прокидывает гейт-вызовы через ту же `reaction_policy`, что и у AZ.

Паритет с AZ по **точкам входа и семантике gate'a** (те же 7 стратагем, тот же apply/pass lookahead).
Разница: **как считается V(s)** (max-Q proxy у DQN, value-head у AZ) и **fight-планировщик**
(greedy 2-веточный lookahead у DQN vs MCTS windows у AZ — см. §8).

## 3. Архитектура

### 3.1 Data flow (полный)

```
1. env.reset() → obs
2. DQN.q_values(obs) → 4+N голов Q
3. action_dict = action_tensor_to_dict(argmax с масками)
4. ЕСЛИ DQN_REACTION_VALUE_POLICY=1 (на каждом step, не только в fight):
     fight_plan = dqn_build_fight_plan(env, net)     # greedy max-Q по 2 веткам на юнит
     attach_fight_stratagem_plan(env, fight_plan)  # plan заберёт fight_phase внутри step
5. env.step(action_dict):
     └─ command_phase:
         bravery gate → reaction_policy("insane_bravery") → _simulate_reaction_branch
                       → infer_with_value → V(apply) vs V(pass) → да/нет
     └─ movement_phase / charge_phase:
         _resolve_overwatch → reaction_policy("overwatch") → V(apply) vs V(pass)
     └─ shooting_phase:
         _maybe_use_smokescreen / _maybe_use_go_to_ground → reaction_policy → V-gate
     └─ charge_phase (end):
         _resolve_heroic_intervention → reaction_policy("heroic") → V-gate
     └─ fight_phase:
         _apply_pending_fight_stratagem_plan(plan) → _apply_stratagem (Hungry Void / Cmd Re-roll)
6. reward → memory.push (n-step)
7. backward по Q-loss как обычно
```

### 3.2 max-Q proxy для V(s)

DQN не имеет явного value-head (в отличие от AZ policy-value net). Решение:
`V(s) ≈ mean(max_a Q_head_i(s, a_legal))` по всем action-heads (**max только по legal actions**,
если переданы `masks_by_head`). Это естественный proxy для DQN:

- работает с любым вариантом сети (dueling/non-dueling, distributional iqn/c51, ensemble);
- не добавляет новых слоёв и параметров → старые чекпойнты остаются совместимы;
- известная проблема DQN — Q overestimates V → компенсируется `eps` в gate'е (дефолт 0 →
  тай в пользу PASS / экономия CP, как и в AZ);
- **masked max обязателен** в reaction-branch и fight-plan: без масок max по незамаскированным
  логитам завышает V на головах с большим числом illegal actions → gate тратит CP слишком щедро.

Почему **mean** по головам, а не max одной головы: у нас 4 базовых + N per-unit голов;
max одной может зашумлять (особенно per-unit `move_num_*`/`shoot_num_*`/`charge_num_*`).
Mean(max per head) — устойчивый V-like сигнал.

### 3.3 Компоненты

| # | Файл | Что меняем | Объём |
|---|---|---|---|
| 1 | `core/models/DQN.py` | Новый метод `infer_with_value(obs, masks_by_head=None) -> (probs, V)`; один проход `q_values`, masked max | ~15 строк |
| 2 | `core/envs/warhamEnv.py` (`_simulate_reaction_branch`) | Duck-typing + legal masks для reacting side при вызове `infer_with_value` | ~12 строк |
| 3 | `core/envs/warhamEnv.py` (`get_legal_action_masks_by_head`) | Маски `use_cp`/`cp_on`: при `reaction_policy` heads мёртвы (`{0}`); legacy — bravery через `{0,1}` + `cp_on` | ~12 строк |
| 4 | `core/models/dqn_stratagem_bridge.py` (новый модуль) | `dqn_value(env, net, device, side)`, `dqn_build_fight_plan(env, net, device, side)` — max-Q V-proxy + greedy fight-plan через snapshot/restore | ~70 строк |
| 5 | `train.py` (DQN inline + actor-learner + `_main_actor_learner`) | `reaction_policy`, fight_plan, env-var резолв | ~30 строк |
| 6 | `eval.py` (DQN-ветка) | То же, что п.5 — установка `reaction_policy` и `fight_plan` в `run_episode` | ~20 строк |
| 7 | `train.py:2618-2631` | Обернуть `PHASE_OBS_FEATURES`/`AZ_REACTION_VALUE_POLICY` в `is_az_algo(TRAIN_ALGO)`, чтобы DQN остался на чистом obs | ~3 строки |
| 8 | `hyperparams.json` | Секция `dqn.reaction_value_policy: 0|1` (дефолт 1) | 1 ключ |

### 3.4 Подробности по компонентам

#### 3.4.1 `DQN.infer_with_value` (новый метод)

```python
def infer_with_value(self, obs, masks_by_head=None):
    """Как infer, но второй элемент кортежа — V(s) ≈ mean(masked max per head).

    Один проход q_values (без повторного infer→q_values). Нужно для reaction_value_policy:
    env._simulate_reaction_branch зовёт net и ждёт value. У DQN infer возвращает (probs, None),
    AZ-net — (policy, value). infer_with_value даёт DQN V через masked max-Q.
    """
    q_lists = self.q_values(obs)
    probs = []
    q_max_per_head = []
    for idx, head_logits in enumerate(q_lists):
        if masks_by_head is not None and idx < len(masks_by_head):
            mask = masks_by_head[idx]
            if mask is not None and mask.shape == head_logits.shape:
                safe_mask = torch.where(mask.any(dim=1, keepdim=True), mask, torch.ones_like(mask))
                masked = head_logits.masked_fill(~safe_mask, -1e9)
                probs.append(torch.softmax(masked, dim=1))
                q_max_per_head.append(masked.max(dim=1).values)
                continue
        probs.append(torch.softmax(head_logits, dim=1))
        q_max_per_head.append(head_logits.max(dim=1).values)
    v = torch.stack(q_max_per_head, dim=1).mean(dim=1)  # (B,)
    return probs, v
```

Существующий `infer` не трогаем — он используется AZ-оппонентами и MCTS-инференсом, которые
берут только `probs`. AZ policy-value net **не имеет** `infer_with_value` → duck-typing в
п.3.4.2 автоматически выбирает нужный путь.

#### 3.4.2 `_simulate_reaction_branch` — duck-typing + legal masks

В `warhamEnv.py:4109` заменить вызов value на duck-typing **с масками для reacting side**:

```python
import torch
from core.models.action_contract import ordered_action_keys

obs = torch.tensor(
    np.asarray([self.get_observation_for_side(side)], dtype=np.float32), dtype=torch.float32
)
if hasattr(net, "infer_with_value"):
    legal = self.get_legal_action_masks_by_head(side=side)
    n_model = len(self.unit_data) if side == "model" else len(self.enemy_data)
    keys = ordered_action_keys(int(n_model))
    masks_by_head = [
        torch.tensor(legal[k], dtype=torch.bool, device=obs.device).unsqueeze(0)
        for k in keys
    ]
    _, value = net.infer_with_value(obs, masks_by_head=masks_by_head)
else:
    _, value = net.infer(obs)
v = float(value.reshape(-1)[0])
```

Это **единая точка** в env. 0 изменений в AZ-коде (у AZ-net нет `infer_with_value` → прежний
`net.infer(obs)` без масок, value-head не зависит от action-mask). regression-safe: существующие
тесты `test_reaction_overwatch.py`/`test_command_bravery_via_engine.py`/`test_reaction_smokescreen.py`
используют mock-сети AZ-формы и продолжат работать.

#### 3.4.3 Маски `use_cp` / `cp_on` — убрать gradient-leak

При `reaction_policy is not None` bravery решает движок через `_should_use_stratagem` (цикл
battle-shock), **не** через `action.use_cp`/`action.cp_on` (`warhamEnv.py:4697-4705`). Heads
`use_cp`/`cp_on` становятся мёртвыми — как зарезервированные `use_cp` 2/3/4.

В `get_legal_action_masks_by_head` после блока `cp_on` (`warhamEnv.py:1757`):

```python
# use_cp: реакции (2/3/4) никогда не исполняются через action head.
# Insane Bravery: при reaction_policy — value-gate; при legacy (policy=None) — use_cp=1 + cp_on.
rvp_on = getattr(self, "reaction_policy", None) is not None
use_cp_n = int(spaces["use_cp"].n)
use_cp_mask = np.zeros(use_cp_n, dtype=bool)
use_cp_mask[0] = True  # none — всегда legal
cp_now = int(self.modelCP if is_model else self.enemyCP)
phase_cmd = str(getattr(self, "phase", "")).lower() == "command"
if not rvp_on and cp_now > 0 and phase_cmd:
    use_cp_mask[1] = True  # legacy bravery
masks["use_cp"] = use_cp_mask

# cp_on: при reaction_policy target bravery выбирает движок (индекс i в battle-shock loop).
if rvp_on:
    cp_mask = np.zeros(cp_n, dtype=bool)
    cp_mask[0] = True  # head мёртв — только dummy legal
else:
    # существующий блок: живые юниты (legacy bravery target)
    ...
masks["cp_on"] = cp_mask
```

> При `DQN_REACTION_VALUE_POLICY=0` train/eval **не** ставят `reaction_policy` → legacy-маски
> bravery `{0,1}` + живые `cp_on` сохраняются.

#### 3.4.4 `train.py` — установка gate'a и fight_plan для DQN

**Env-var резолв** (в районе `train.py:2618-2631`, но ВНУТРИ условия или с проверкой algo):

```python
DQN_REACTION_VALUE_POLICY = (
    str(os.getenv("DQN_REACTION_VALUE_POLICY",
                  str(DQN_CFG.get("reaction_value_policy", 1)))).strip().lower() in ("1", "true", "yes", "on")
)
os.environ["DQN_REACTION_VALUE_POLICY"] = "1" if DQN_REACTION_VALUE_POLICY else "0"
```

Где `DQN_CFG = HYPERPARAMS.get("dqn", {})` (если секции нет — пустой dict, дефолт 1).

**Установка в actor-learner** (после создания `policy_net`, ~`train.py:6620`):

```python
if DQN_REACTION_VALUE_POLICY:
    from core.models.reaction_value_policy import make_stratagem_value_policy
    for ctx in env_contexts:
        e_u = unwrap_env(ctx["env"])
        e_u._reaction_net_by_side = {"model": policy_net}  # learner_only (см. §4)
        e_u.reaction_policy = make_stratagem_value_policy(e_u._reaction_net_by_side, device=device)
    _log_train("[DQN][CONFIG] reaction_value_policy установлена (max-Q proxy, learner_only)")
```

Аналогично для inline-цикла (после `train.py:4646`).

> Важно про env_ctx: для каждого из `env_contexts` устанавливаем СВОЙ `reaction_policy`
> (env-ы независимы). В spawn-mode (Windows) `os.environ["DQN_REACTION_VALUE_POLICY"]`
> прокидывается в actor-процессы; **обязательно** дублировать установку `reaction_policy` +
> `_reaction_net_by_side` в `_main_actor_learner` (DQN-ветка, по аналогии с AZ
> `AZ_REACTION_VALUE_POLICY` / `make_stratagem_value_policy`). Иначе learner и actors
> разъедутся по семантике стратагем.

**Fight-plan builder** (новая функция ~30 строк, кладётся в новый модуль
`core/models/dqn_stratagem_bridge.py`, импортируется и в train.py, и в eval.py — DRY):

```python
# core/models/dqn_stratagem_bridge.py
"""DQN ↔ стратагемы: V-proxy (max-Q), fight-plan builder, value-bridge.

Переиспользует AZ-инфру (reaction_value_policy, attach_fight_stratagem_plan) поверх DQN.infer_with_value.
"""
from __future__ import annotations

import numpy as np
import torch

from core.engine.phases.stratagem_engine import apply as _apply_stratagem
from core.engine.phases.stratagems import for_phase, usage_limit_reached
from core.engine.phases.types import Phase
from core.models.action_contract import ordered_action_keys
from core.models.utils import unwrap_env


def _masks_for_side(env, side: str, device) -> list:
    """Legal action masks в порядке ordered_action_keys — для masked max-Q."""
    e = unwrap_env(env)
    legal = e.get_legal_action_masks_by_head(side=side)
    n_model = len(e.unit_data) if side == "model" else len(e.enemy_data)
    keys = ordered_action_keys(int(n_model))
    return [
        torch.tensor(legal[k], dtype=torch.bool, device=device).unsqueeze(0)
        for k in keys
    ]


def dqn_value(env, policy_net, device, side: str) -> float:
    """max-Q V(s) для стороны side (masked infer_with_value)."""
    e = unwrap_env(env)
    obs = torch.tensor(
        np.asarray([e.get_observation_for_side(side)], dtype=np.float32),
        device=device,
    )
    masks = _masks_for_side(e, side, device)
    with torch.no_grad():
        _, v = policy_net.infer_with_value(obs, masks_by_head=masks)
    return float(v.reshape(-1)[0].item())


def dqn_build_fight_plan(env, policy_net, device, side: str = "model") -> dict[int, str]:
    """Hungry Void / Command Re-roll план через max-Q lookahead (2 ветки на юнит).

    Для каждого eligible-бойца (in_attack==1, жив): snapshot → restore + apply стратагему →
    V(apply); restore → V(pass). Если V(apply) > V(pass) + eps — кладём в план. CP читается
    заново на каждой итерации (сосед мог уже списать в предыдущей итерации).

    Инвариант snapshot: snapshot_state/restore_state должны покрывать modelCP/enemyCP,
    stratagem_used, active_stratagem_effects, unit_health/enemy_health, unitInAttack.
    Если какой-то из них не покрывается — `_apply_stratagem` в симуляции испортит реальное
    состояние (диагностика: тест в 7.1/7.2 ловит).
    """
    e = unwrap_env(env)
    if getattr(e, "_reaction_sim_active", False):
        return {}  # recursion guard (вдруг нас вызвали изнутри _simulate_reaction_branch)
    health = e.unit_health if side == "model" else e.enemy_health
    in_attack = e.unitInAttack if side == "model" else e.enemyInAttack
    plan: dict[int, str] = {}
    eps = 1e-3  # fight-plan строже реакций: greedy planner без MCTS → чуть выше порог PASS
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
                continue  # уже выбран юнит → не дублируем
            snap = e.snapshot_state()
            try:
                with e.simulation_mode():
                    e.restore_state(snap)
                    _apply_stratagem(e, side, d.id, u, phase="fight")
                    v_apply = dqn_value(e, policy_net, device, side)
                    e.restore_state(snap)
                    v_pass = dqn_value(e, policy_net, device, side)
            finally:
                e.restore_state(snap)
            if v_apply > v_pass + eps:
                plan[u] = d.id  # при нескольких fight-стратагемах — первая по порядку for_phase
    return plan
```

> **Fight-plan vs AZ MCTS:** AZ выбирает план joint'ом через decision windows; DQN — greedy
> per-unit 2-веточный lookahead. Паритет gate'a (apply/pass), не паритет планировщика.
> Если на юните legal обе fight-стратагемы — побеждает первая в `for_phase(Phase.FIGHT)`.

**Точка вызова** в DQN-цикле (`train.py:5354-5365`, перед `tracer.run_model_step`/`env.step`):

```python
# Важно: attach делается ВСЕГДА (не зависит от текущей phase). fight-phase исполняется ВНУТРИ
# env.step (modelTurn вызывает все фазы последовательно); _pending_fight_stratagem_plan
# persists в env до тех пор, пока fight_phase его не заберёт. Это та же семантика, что у AZ
# в eval.py:359 — `attach_fight_stratagem_plan(env, mcts.last_selected_fight_plan)`.
from core.models.dqn_stratagem_bridge import dqn_build_fight_plan
fight_plan = dqn_build_fight_plan(ctx["env"], policy_net, device, side="model") if DQN_REACTION_VALUE_POLICY else None
attach_fight_stratagem_plan(ctx["env"], fight_plan)
try:
    next_observation, reward, done, res, info = ...  # существующий step
finally:
    attach_fight_stratagem_plan(ctx["env"], None)  # cleanup (как eval.py:791/886)
```

> Примечание по overhead: `dqn_build_fight_plan` делает 2 forward-pass на каждого
> eligible-бойца (`in_attack[u][0]==1`). Если eligible нет — план пустой, overhead = 0.
> На типичных партиях eligible 0–2 юнита → терпимо. На каждом step план перевычисляется
> свежий (env.state мог измениться).

#### 3.4.5 `eval.py` — то же для DQN-оценки

После `make_dqn`/`load_state_dict` (`eval.py:1311-1328`):

```python
if str(os.getenv("DQN_REACTION_VALUE_POLICY", "1")).strip().lower() in ("1", "true", "yes", "on"):
    from core.models.reaction_value_policy import make_stratagem_value_policy
    e_u = unwrap_env(env)
    e_u._reaction_net_by_side = {"model": policy_net}
    e_u.reaction_policy = make_stratagem_value_policy(e_u._reaction_net_by_side, device=device)
    log("[EVAL][DQN][CONFIG] reaction_value_policy установлена (max-Q proxy, learner_only)")
```

В `run_episode` DQN-ветке (`eval.py:825-834`) — построение `fight_plan` перед step:

```python
from core.models.dqn_stratagem_bridge import dqn_build_fight_plan
_dqn_rvp_on = str(os.getenv("DQN_REACTION_VALUE_POLICY", "1")).strip().lower() in ("1", "true", "yes", "on")
# ... внутри цикла, перед action selection:
fight_plan = dqn_build_fight_plan(env, policy_net, device, side="model") if _dqn_rvp_on else None
attach_fight_stratagem_plan(env, fight_plan)
try:
    action_masks = build_action_masks_by_head(env, len(model_units), log_fn=None, debug=False)
    action = select_action_with_epsilon(...)
    ...
finally:
    attach_fight_stratagem_plan(env, None)
```

> `dqn_build_fight_plan` / `dqn_value` живут в общем модуле `core/models/dqn_stratagem_bridge.py`
> (DRY, импортируется и в train.py, и в eval.py, и в тестах).

#### 3.4.6 Обернуть `PHASE_OBS_FEATURES` в `is_az_algo`

`train.py:2618-2631` — обернуть в:

```python
if is_az_algo(TRAIN_ALGO):
    AZ_PHASE_OBS_FEATURES = resolve_phase_obs_features(
        env_value=os.getenv("PHASE_OBS_FEATURES"),
        cfg_value=AZ_CFG.get("phase_obs_features", 0),
    )
    os.environ["PHASE_OBS_FEATURES"] = "1" if AZ_PHASE_OBS_FEATURES else "0"
    AZ_REACTION_VALUE_POLICY = resolve_phase_obs_features(
        env_value=os.getenv("AZ_REACTION_VALUE_POLICY"),
        cfg_value=AZ_CFG.get("reaction_value_policy", 1),
    )
    os.environ["AZ_REACTION_VALUE_POLICY"] = "1" if AZ_REACTION_VALUE_POLICY else "0"
else:
    # DQN/PPO/etc — на чистом obs, без AZ-фич
    os.environ["PHASE_OBS_FEATURES"] = "0"
    os.environ["AZ_REACTION_VALUE_POLICY"] = "0"
```

Это решает регрессию из аудита: resume старого DQN-чекпойнта больше не сломается, DQN
обучается на чистом obs без +24 dims шума.

## 4. Enemy-сторона (v1: learner_only)

`_reaction_net_by_side = {"model": policy_net}` — только learner-сторона получает
value-gate. Enemy-сторона (любая — эвристика, policy-оппонент, self-play) реагирует **legacy**
(`reaction_value_policy.py:21-22`: `net_by_side.get(side) is None → return True`).

Обоснование:
- **Эвристика** — у неё нет сети, legacy-поведение корректно.
- **Policy-оппонент через `opponent-agent-id`** — его action-policy активна через
  `enemyTurn(policy_fn=...)`, но реакции в любом случае делает движок через `_resolve_*`.
  Достать сеть оппонента для value-gate — Stage 2 (`from_opponent`).
- **Self-play DQN** — Stage 2 (`selfplay` — клон learner'а на enemy-side).

Env-var `DQN_REACTION_ENEMY_SIDE` зарезервирован, но в v1 не читается (всегда `learner_only`).
Расширение вынесено в §9 (Stage 2).

## 5. Точки расширения и совместимость

- **Старые DQN-чекпойнты**: совместимы. `infer_with_value` — новый метод, не новый параметр;
  `load_state_dict` работает. `PHASE_OBS_FEATURES=0` для DQN → obs-размер не меняется.
- **AZ-код**: не трогаем. `infer_with_value` есть только у DQN, AZ-net идёт прежним путём
  в `_simulate_reaction_branch` через duck-typing.
- **PPO**: не трогаем (если потребуется — отдельная задача, тот же bridge-модуль).
- **`reaction_value_policy.make_stratagem_value_policy`**: не меняем. Она generic и уже
  работает с любым `net_by_side` (включая DQN с `infer_with_value`).

## 6. Флаги и окружение

| Флаг | Дефолт | Где | Что |
|---|---|---|---|
| `DQN_REACTION_VALUE_POLICY` | `1` | env + `hyperparams.json` → `dqn.reaction_value_policy` | Включить умные стратагемы для DQN |
| `PHASE_OBS_FEATURES` (для DQN) | `0` (после §3.4.6) | env, выставляется в train.py | DQN всегда на чистом obs |
| `AZ_REACTION_VALUE_POLICY` | не для DQN | env | Только AZ-путь |

## 7. Тестирование

### 7.1 Юнит-тесты

- **`tests/models/test_dqn_infer_with_value.py`** (новый):
  - tiny DQN, форма `(probs, V)` корректна, `V.shape == (B,)`, нет NaN/inf.
  - masked max-Q: с маской, где legal только action 0, `V == q[:,0]` (не max по illegal).
  - без масок — fallback на unmasked max (как раньше).
  - dueling=True и dueling=False — оба варианта.
  - distributional iqn/c51 — оба варианта.
  - один вызов `q_values` (нет двойного forward — smoke через mock/spy при желании).

- **`tests/models/test_dqn_stratagem_bridge.py`** (новый):
  - `dqn_build_fight_plan`: mock-env с eligible-бойцом, Hungry Void legal (necrons-keyword), CP хватает.
  - stub `policy_net.infer_with_value` → `V(apply) > V(pass)` → план `{u: "hungry_void"}`.
  - обратный кейс → план пустой.
  - `usage_limit_reached` срабатывает → пропускается.
  - CP не хватает → пропускается.
  - инвариант snapshot: после вызова `dqn_build_fight_plan` `env.modelCP`/`env.stratagem_used`
    не меняются (snapshot/restore корректны).
  - recursion guard: `_reaction_sim_active=True` → план пустой, исключений нет.

- **`tests/engine/phases/test_simulate_reaction_branch_dqn.py`** (новый):
  - mock-сеть с `infer_with_value` → `_simulate_reaction_branch` вызывает его **с masks_by_head**.
  - mock-сеть AZ-формы (без `infer_with_value`) → прежний путь `net.infer(obs)`.

- **`tests/envs/test_use_cp_masks_with_reaction_policy.py`** (новый):
  - `reaction_policy=None`, command, CP>0 → `use_cp` legal `{0,1}`.
  - `reaction_policy` установлена → `use_cp` только `{0}`, `cp_on` только `{0}` (heads мёртвы).
  - вне command-phase → `use_cp` только `{0}` в обоих режимах.

### 7.2 Интеграционные тесты

- **`tests/integration/test_dqn_smart_stratagems_e2e.py`** (новый):
  - tiny DQN-policy-net + env + `reaction_policy` из `make_stratagem_value_policy`.
  - сценарий overwatch: enemy ends move в 24" + LOS → `modelCP` списан, если `V(apply) > V(pass)`.
  - сценарий bravery: command-phase, battle-shock failed → `modelCP` списан.
  - сценарий fight-plan: fight-phase, eligible necrons-unit → `_pending_fight_stratagem_plan` применён.
  - regression: `DQN_REACTION_VALUE_POLICY=0` → `modelCP` списан всегда (legacy).

### 7.3 Регрессия AZ

- Существующие AZ-тесты (`test_reaction_overwatch.py`, `test_command_bravery_via_engine.py`,
  `test_reaction_smokescreen.py`, `test_reaction_heroic.py`, `test_hungry_void.py`,
  `test_command_reroll.py`) **не должны сломаться** — `_simulate_reaction_branch` делает
  duck-typing, AZ-mock-сети остаются на прежнем пути.
- Паритетный тест `windowed_parity_winrate` (если есть) для AZ — Δ=0pp при включении флага для DQN.

### 7.4 Smoke-тест

- `TRAIN_ALGO=dqn`, `DQN_REACTION_VALUE_POLICY=1`, 10-20 шагов.
  - лог `[DQN][CONFIG] reaction_value_policy установлена (max-Q proxy, learner_only)` есть.
  - в `LOGS_FOR_AGENTS_TRAIN.md` появляются строки `[STRATAGEM]` со списанным CP.
- `eval.py`, `DQN_REACTION_VALUE_POLICY=1`, 1 эпизод — тот же CONFIG-лог, без падения.
- `DQN_REACTION_VALUE_POLICY=0` — legacy, `modelCP` списывается всегда, если хватает CP.

## 8. Trade-offs

| Аспект | Что получаем | Цена |
|---|---|---|
| Паритет с AZ по стратагемам | Все 7 стратагем умно через тот же gate | Fight-план — greedy, не MCTS joint (§3.4.4) |
| Минимум нового кода | ~170 строк: bridge + masked infer + маски + spawn-hook | Нужно зеркалировать AZ-блоки в train/eval/**_main_actor_learner** |
| max-Q как V(s) | 0 новой архитектуры, compat с dueling/distributional/ensemble | Q overestimates V → masked max + `eps`. Fight-plan: `eps=1e-3` (строже, т.к. greedy без MCTS); реакции: `eps=0` из `make_stratagem_value_policy` (как AZ) |
| Snapshot/restore в fight-plan | Корректность (нет side-effects) | +2 masked forward-pass на eligible-бойца на fight-step (терпимо) |
| `_simulate_reaction_branch` per trigger | Точно как AZ | +2 masked forward-pass на решение (AZ-паттерн, не DQN-новинка) |
| learner_only в v1 | Простота, не ломаем opponent-провайдеры | Enemy-side без value-gate; eval vs heuristic асимметричен (Stage 2) |

## 9. Stage 2 (опционально, не в этом плане)

Зарезервированные расширения (не реализуются в первой версии):

- **`DQN_REACTION_ENEMY_SIDE=selfplay`**: `_reaction_net_by_side = {"model": policy_net,
  "enemy": policy_net}`. Симметричный self-play DQN — обе стороны умно реагируют.
- **`DQN_REACTION_ENEMY_SIDE=from_opponent`**: при `opponent-agent-id` попытаться достать
  внутреннюю сеть оппонента (если это DQN/AZ — есть V-источник) и положить в
  `{"enemy": opponent_net}`. PPO требует отдельной адаптации (PPO critic как V-источник).
- **PPO smart stratagems**: тот же bridge-модуль (`dqn_stratagem_bridge.py` →
  `stratagem_bridge.py`), PPO actor вместо DQN, PPO critic как V-источник.

## 10. Открытые вопросы (решено во время brainstorming)

- ✅ V(s) для DQN: **masked max-Q proxy = mean(max per head over legal actions)**.
- ✅ `DQN_REACTION_VALUE_POLICY` дефолт: **1** (включён).
- ✅ `PHASE_OBS_FEATURES` для DQN: **обернуть в `is_az_algo`**, DQN на чистом obs.
- ✅ Enemy-сторона v1: **learner_only** (`_reaction_net_by_side = {"model": policy_net}`).
- ✅ Prerequisite: **fidelity A+B** до DQN-bridge.
- ✅ `use_cp`/`cp_on` при `reaction_policy`: **heads мёртвы** (`{0}`), legacy только при policy=None.
- ✅ Fight-plan `eps=1e-3` vs reactions `eps=0`: **осознанно** (greedy planner без MCTS).
- ✅ Spawn DQN actors: **дублировать hook** в `_main_actor_learner`.
- ⏳ GUI-тогглер `dqn.reaction_value_policy` в Qt — **не v1** (достаточно env/hyperparams).
