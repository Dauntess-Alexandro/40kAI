# B3-full Reaction value-policy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Заменить «всегда реагировать» на net-value 1-ply lookahead с резолвом триггер-действия для реакций (go_to_ground/smokescreen/overwatch/heroic_intervention), за флагом, дефолт выкл.

**Architecture:** Решение реакции делает `env.reaction_policy` (callable из `reaction_value_policy.py`). На каждом reaction-окне harness `_simulate_reaction_branch` снапшотит env, для веток apply/pass досимулирует триггер-взаимодействие через переданный из call-site коллбэк `resolve_trigger`, оценивает value-головой сети реагирующей стороны и выбирает лучшее. Контракт действий и MCTS не меняются.

**Tech Stack:** Python 3.12, PyTorch, `core/envs/warhamEnv.py` (snapshot/restore, simulation_mode), `core/models/alphazero_model.py` (value head), pytest.

**Spec:** `docs/superpowers/specs/2026-06-19-b3-reaction-value-policy-design.md`

---

## File Structure

- Create: `core/models/reaction_value_policy.py` — фабрика политики реакций + решение apply/pass.
- Create: `tests/models/test_reaction_value_policy.py` — юниты политики (фейковый net).
- Create: `tests/engine/phases/test_reaction_harness.py` — harness/recursion-guard/no-side-effects.
- Modify: `core/envs/warhamEnv.py` — harness `_simulate_reaction_branch`, recursion guard, расширение `_should_use_reaction(..., resolve_trigger=None)`, обёртки call-site по одной реакции.
- Modify: `train.py` — резолв флага `AZ_REACTION_VALUE_POLICY`, лог `[AZ][CONFIG]`, установка policy в actor.
- Modify: `eval.py` — установка policy + лог.
- Modify: `hyperparams.json`, `app/gui_qt/az_hyperparams_defaults.py`, `app/gui_qt/main.py` — флаг `reaction_value_policy` (дефолт 0), валидатор, env-insert (train+eval), GUI-лог.

---

## Task 1: Флаг reaction_value_policy (plumbing, дефолт 0)

**Files:**
- Modify: `hyperparams.json` (секция `alphazero_tree`, рядом с `phase_obs_features`)
- Modify: `app/gui_qt/az_hyperparams_defaults.py` (3 списка + tooltip, как `phase_obs_features`)
- Modify: `app/gui_qt/main.py` (валидатор ~4880; train env-insert ~6685; eval env-insert ~5586; GUI-лог)
- Modify: `train.py` (резолв ~2630; `[AZ][CONFIG]` ~9384)
- Modify: `eval.py` (лог в `main()` рядом с phase_obs)

- [ ] **Step 1: hyperparams.json** — добавить в `alphazero_tree` после `"phase_obs_features": 0,`:

```json
        "reaction_value_policy": 0,
```

- [ ] **Step 2: GUI defaults** — в `app/gui_qt/az_hyperparams_defaults.py` добавить `"reaction_value_policy"` в `AZ_HYPERPARAM_KEYS`, в `_AZ_BASE` (`"reaction_value_policy": 0,`), в `AZ_GROUPS` секцию `mcts` keys, и tooltip:

```python
    "reaction_value_policy": (
        "1 = реакции (go to ground/smokescreen/overwatch/heroic) решает net-value 1-ply lookahead "
        "с резолвом триггера. 0 = всегда реагировать (legacy). env AZ_REACTION_VALUE_POLICY."
    ),
```

- [ ] **Step 3: main.py валидатор** — после блока `phase_obs` в `_validate_az_tree_hyperparams`:

```python
        reaction_vp = int(payload.get("reaction_value_policy", 0))
        if reaction_vp not in (0, 1):
            return f"{section}.reaction_value_policy должен быть 0 или 1"
```

- [ ] **Step 4: main.py env-insert (train + eval)** — в train-блоке (рядом с `PHASE_OBS_FEATURES`):

```python
            env.insert(
                "AZ_REACTION_VALUE_POLICY",
                os.getenv("AZ_REACTION_VALUE_POLICY", str(int(az_hp.get("reaction_value_policy", 0)))),
            )
```

и в eval-блоке (после `PHASE_OBS_FEATURES`):

```python
        env.insert(
            "AZ_REACTION_VALUE_POLICY",
            os.getenv("AZ_REACTION_VALUE_POLICY", str(int(self._az_tree_hyperparams.get("reaction_value_policy", 0)))),
        )
```

Добавить `reaction_value_policy={env.value("AZ_REACTION_VALUE_POLICY","0")}` в GUI `[AZ][CONFIG]`-лог.

- [ ] **Step 5: train.py резолв + лог** — после блока `AZ_PHASE_OBS_FEATURES`:

```python
AZ_REACTION_VALUE_POLICY = resolve_phase_obs_features(
    env_value=os.getenv("AZ_REACTION_VALUE_POLICY"),
    cfg_value=AZ_CFG.get("reaction_value_policy", 0),
)
os.environ["AZ_REACTION_VALUE_POLICY"] = "1" if AZ_REACTION_VALUE_POLICY else "0"
```

(переиспользуем generic-резолвер `resolve_phase_obs_features(env_value, cfg_value)` — он не специфичен для phase_obs, читает «env > cfg, truthy».) В `[AZ][CONFIG]`-строку добавить `reaction_value_policy={int(AZ_REACTION_VALUE_POLICY)} `.

- [ ] **Step 6: eval.py лог** — рядом с `[EVAL][AZ][CONFIG] phase_obs_features=`:

```python
    log(f"[EVAL][AZ][CONFIG] reaction_value_policy={int(str(os.getenv('AZ_REACTION_VALUE_POLICY','0')).strip() in ('1','true','yes','on'))}")
```

- [ ] **Step 7: Verify** — `python -c "import ast; ast.parse(open('train.py',encoding='utf-8').read())"` и то же для eval.py/main.py/az_hyperparams_defaults.py. `python -c "import json; json.load(open('hyperparams.json'))"`. Expected: без ошибок.

- [ ] **Step 8: Commit**

```bash
git add hyperparams.json app/gui_qt/az_hyperparams_defaults.py app/gui_qt/main.py train.py eval.py
git commit -m "feat(b3): флаг reaction_value_policy (plumbing, дефолт 0)"
```

---

## Task 2: Модуль reaction_value_policy.py (решение apply/pass)

**Files:**
- Create: `core/models/reaction_value_policy.py`
- Test: `tests/models/test_reaction_value_policy.py`

- [ ] **Step 1: Failing test** — `tests/models/test_reaction_value_policy.py`:

```python
from core.models.reaction_value_policy import make_reaction_value_policy


class FakeEnv:
    def __init__(self):
        self._reaction_sim_active = False
        self.branch_values = {"apply": 0.5, "pass": 0.1}
        self.restored = 0

    def snapshot_state(self):
        return {"snap": 1}

    def restore_state(self, snap):
        self.restored += 1

    def _simulate_reaction_branch(self, ctx, *, apply):
        return self.branch_values["apply" if apply else "pass"]


def _ctx(env, side="model"):
    return {"side": side, "stratagem_id": "go_to_ground", "phase": "shooting",
            "chosen": 0, "candidates": [0], "cp": 2, "env": env, "resolve_trigger": lambda apply: None}


def test_picks_apply_when_value_higher():
    env = FakeEnv()
    pol = make_reaction_value_policy({"model": object()}, device="cpu")
    assert pol(_ctx(env)) is True
    assert env.restored >= 2  # restore после каждой ветки + финал


def test_picks_pass_on_tie_for_cp_economy():
    env = FakeEnv()
    env.branch_values = {"apply": 0.3, "pass": 0.3}
    pol = make_reaction_value_policy({"model": object()}, device="cpu")
    assert pol(_ctx(env)) is False


def test_side_without_net_falls_back_to_legacy_true():
    env = FakeEnv()
    pol = make_reaction_value_policy({"model": None}, device="cpu")
    assert pol(_ctx(env)) is True


def test_recursion_guard_returns_true():
    env = FakeEnv()
    env._reaction_sim_active = True
    pol = make_reaction_value_policy({"model": object()}, device="cpu")
    assert pol(_ctx(env)) is True
```

- [ ] **Step 2: Run, verify fails** — `pytest tests/models/test_reaction_value_policy.py -q`. Expected: FAIL (нет модуля).

- [ ] **Step 3: Implement** — `core/models/reaction_value_policy.py`:

```python
"""B3-full: net-value 1-ply lookahead для реакций (apply vs pass).

Ставится в env.reaction_policy. На каждое reaction-решение: snapshot → для веток
apply/pass досимулировать триггер через env._simulate_reaction_branch → value-голова
сети реагирующей стороны → restore → выбрать лучшее (тай → PASS, экономия CP).
"""
from __future__ import annotations

from typing import Callable


def make_reaction_value_policy(net_by_side: dict, *, device, eps: float = 0.0) -> Callable[[dict], bool]:
    def policy(ctx: dict) -> bool:
        env = ctx["env"]
        side = str(ctx["side"])
        net = net_by_side.get(side)
        if net is None:
            return True  # сторона без сети: legacy «реагировать»
        if bool(getattr(env, "_reaction_sim_active", False)):
            return True  # recursion guard
        snap = env.snapshot_state()
        values = {}
        for branch in ("pass", "apply"):
            env.restore_state(snap)
            values[branch] = float(env._simulate_reaction_branch(ctx, apply=(branch == "apply")))
        env.restore_state(snap)
        return values["apply"] > values["pass"] + float(eps)

    return policy
```

- [ ] **Step 4: Run, verify passes** — `pytest tests/models/test_reaction_value_policy.py -q`. Expected: PASS (4).

- [ ] **Step 5: Commit**

```bash
git add core/models/reaction_value_policy.py tests/models/test_reaction_value_policy.py
git commit -m "feat(b3): reaction_value_policy — решение apply/pass по net-value"
```

---

## Task 3: Harness `_simulate_reaction_branch` + recursion guard + seam-расширение

**Files:**
- Modify: `core/envs/warhamEnv.py` (рядом с `_should_use_reaction` ~4025; init `_reaction_sim_active` рядом с `_simulation_mode_depth` ~1087)
- Test: `tests/engine/phases/test_reaction_harness.py`

- [ ] **Step 1: Failing test** — `tests/engine/phases/test_reaction_harness.py`:

```python
from tests.engine.phases._helpers import build_env


def _net_value_stub(value):
    class _Net:
        def infer(self, obs, masks_by_head=None):
            import torch
            return None, torch.tensor([float(value)])
    return _Net()


def test_simulate_branch_restores_state_and_returns_value():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    cp_before = env.modelCP
    called = {"apply": None}

    def resolve_trigger(apply):
        called["apply"] = apply  # триггер-резолв в симуляции (заглушка)

    ctx = {"side": "model", "stratagem_id": "go_to_ground", "phase": "shooting",
           "chosen": 0, "candidates": [0], "cp": cp_before, "env": env,
           "resolve_trigger": resolve_trigger, "net": _net_value_stub(0.42)}
    v = env._simulate_reaction_branch(ctx, apply=True)
    assert abs(v - 0.42) < 1e-6
    assert called["apply"] is True
    assert env.modelCP == cp_before  # внутренний снапшот восстановлен (no side-effects)
    assert env._reaction_sim_active is False  # флаг сброшен в finally


def test_recursion_guard_set_during_branch():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    seen = {}

    def resolve_trigger(apply):
        seen["guard"] = env._reaction_sim_active

    ctx = {"side": "model", "stratagem_id": "go_to_ground", "phase": "shooting",
           "chosen": 0, "candidates": [0], "cp": 1, "env": env,
           "resolve_trigger": resolve_trigger, "net": _net_value_stub(0.0)}
    env._simulate_reaction_branch(ctx, apply=False)
    assert seen["guard"] is True
```

- [ ] **Step 2: Run, verify fails** — `pytest tests/engine/phases/test_reaction_harness.py -q`. Expected: FAIL (нет `_simulate_reaction_branch`).

- [ ] **Step 3: Implement** — в `core/envs/warhamEnv.py`:

В `__init__`/reset рядом с `self._simulation_mode_depth = 0` добавить `self._reaction_sim_active = False`.

Добавить метод (рядом с `_should_use_reaction`):

```python
    def _simulate_reaction_branch(self, ctx, *, apply: bool) -> float:
        """B3-full: оценить value реагирующей стороны при apply/pass, досимулировав триггер.

        Снапшот/restore делает вызывающая reaction_policy; здесь — внутренний guard, применение
        реакции (apply), резолв триггера и value-голова сети.
        """
        side = str(ctx["side"])
        net = ctx.get("net")
        resolve_trigger = ctx.get("resolve_trigger")
        inner = self.snapshot_state()
        self._reaction_sim_active = True
        try:
            with self.simulation_mode():
                if apply:
                    from core.engine.phases.stratagem_engine import apply as _apply
                    _apply(self, side, str(ctx["stratagem_id"]), int(ctx["chosen"]), phase=str(ctx["phase"]))
                if resolve_trigger is not None:
                    resolve_trigger(apply)
                import torch
                obs = torch.tensor([self.get_observation_for_side(side)], dtype=torch.float32)
                _, value = net.infer(obs)
                v = float(value.reshape(-1)[0])
        finally:
            self._reaction_sim_active = False
            self.restore_state(inner)
        return v
```

Расширить `_should_use_reaction` так, чтобы класть `env`/`resolve_trigger`/`net` в ctx — сигнатура: `def _should_use_reaction(self, stratagem_id, side, chosen, candidates, phase, cp, *, resolve_trigger=None, net=None)`, и в `ctx` добавить `"env": self, "resolve_trigger": resolve_trigger, "net": net`. Legacy-путь (policy is None) их игнорирует.

- [ ] **Step 4: Run, verify passes** — `pytest tests/engine/phases/test_reaction_harness.py -q`. Expected: PASS (2).

- [ ] **Step 5: Регресс** — `pytest tests/engine/phases/ -q`. Expected: всё зелёное (seam расширен опциональными kwargs, старые вызовы не сломаны).

- [ ] **Step 6: Commit**

```bash
git add core/envs/warhamEnv.py tests/engine/phases/test_reaction_harness.py
git commit -m "feat(b3): harness _simulate_reaction_branch + recursion guard + seam resolve_trigger"
```

---

## Task 4: go_to_ground end-to-end (триггер — входящая стрельба)

**Цель:** на главном shooting-call-site (`core/envs/warhamEnv.py:5570`, `_maybe_use_smokescreen` для `defender_side="enemy"`) построить `resolve_trigger(apply)`, который досимулирует именно этот выстрел, и прокинуть `net` реагирующей стороны.

**Files:**
- Modify: `core/envs/warhamEnv.py` (call-site ~5570; внутри `_maybe_use_go_to_ground` пробросить `resolve_trigger`/`net` в `_should_use_reaction`)
- Modify: `core/models/reaction_value_policy.py` (передать `net` в ctx — см. ниже)
- Test: `tests/engine/phases/test_reaction_go_to_ground.py`

- [ ] **Step 1: Failing test** — детерминированный: cover снижает урон → apply выгоднее. `tests/engine/phases/test_reaction_go_to_ground.py`:

```python
import core.envs.warhamEnv as warham_mod
from core.models.reaction_value_policy import make_reaction_value_policy
from tests.engine.phases._helpers import build_env


class _NetByDamage:
    """value тем выше для защитника, чем больше его суммарное HP после выстрела."""
    def __init__(self, env, side):
        self.env = env; self.side = side
    def infer(self, obs, masks_by_head=None):
        import torch
        hp = float(sum(self.env.unit_health if self.side == "model" else self.env.enemy_health))
        return None, torch.tensor([hp])


def test_go_to_ground_applied_when_cover_saves_damage(monkeypatch):
    # attack с cover (effects benefit_of_cover) наносит 0, без — 3.
    def fake_attack(ah, w, ad, dh, dd, *a, effects=None, **k):
        dmg = 0.0 if effects == "benefit of cover" else 3.0
        return [dmg], max(0.0, dh - dmg)
    monkeypatch.setattr(warham_mod, "attack", fake_attack)

    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.enemyCP = 3
    env.enemy_data[0]["Keywords"] = ["Infantry"]  # go_to_ground требует infantry
    env.reaction_policy = make_reaction_value_policy({"enemy": _NetByDamage(env, "enemy")}, device="cpu")
    # прямой вызов сайта: defender=enemy idx0 под обстрелом model
    effect = env._maybe_use_go_to_ground("enemy", 0, "shooting")
    assert effect == "benefit of cover"  # реакция выбрана (apply выгоднее)
    used = [r[1] for r in env.stratagem_used]
    assert "go_to_ground" in used
```

> NB: реальный `resolve_trigger` досимулирует выстрел; в этом юните мы проверяем решение через прямой вызов сайта с net, оценивающим HP защитника. Полный shooting-путь покрывается smoke (Task 8).

- [ ] **Step 2: Run, verify fails** — `pytest tests/engine/phases/test_reaction_go_to_ground.py -q`. Expected: FAIL (reaction_policy не получает net/resolve_trigger → решение не строится).

- [ ] **Step 3: Implement** — в `_maybe_use_go_to_ground` заменить вызов `_should_use_reaction(...)` на проброс контекста (net реагирующей стороны и resolve_trigger):

```python
            use_it = self._should_use_reaction(
                "go_to_ground", defender_side, defender_idx, [defender_idx], phase, cp,
                resolve_trigger=getattr(self, "_pending_reaction_trigger", None),
                net=getattr(self, "_reaction_net_by_side", {}).get(defender_side),
            )
```

На call-site (5570) перед `_maybe_use_smokescreen(...)` установить `self._pending_reaction_trigger` как замыкание, досимулирующее этот выстрел (без reward/логов):

```python
                        def _resolve_shot(apply, _i=i, _e=idOfE):
                            eff = "benefit of cover" if apply else None
                            eff = self._resolve_cover_effect_for_shot("model", _i, "enemy", _e, base_effect=eff, phase="shooting")
                            _, mh = attack(self.unit_health[_i], self.unit_weapon[_i], self.unit_data[_i],
                                           self.enemy_health[_e], self.enemy_data[_e], effects=eff,
                                           distance_to_target=self._shooting_distance_between_units("model", _i, "enemy", _e))
                            self._apply_health_update("enemy", _e, mh, reason="shooting_sim")
                        self._pending_reaction_trigger = _resolve_shot
```

и в `finally`/после выстрела очищать `self._pending_reaction_trigger = None`. Также `make_reaction_value_policy` уже кладёт `net` в ctx через seam (Task 3); убедиться, что `policy` передаёт `ctx["net"]` в `_simulate_reaction_branch` — он берёт `ctx.get("net")` (уже так).

Установка `self._reaction_net_by_side` — в Task 8 (actor/eval). Для теста выставляется через `env.reaction_policy` + net в ctx; для прямого вызова сайта добавить fallback: если `reaction_policy` есть, seam передаёт net из `_reaction_net_by_side`.

- [ ] **Step 4: Run, verify passes** — `pytest tests/engine/phases/test_reaction_go_to_ground.py -q`. Expected: PASS.

- [ ] **Step 5: Регресс + commit**

```bash
pytest tests/engine/phases/ -q
git add core/envs/warhamEnv.py core/models/reaction_value_policy.py tests/engine/phases/test_reaction_go_to_ground.py
git commit -m "feat(b3): go_to_ground через net-value lookahead (resolve_trigger выстрела)"
```

---

## Task 5: smokescreen (тот же триггер-резолв, keyword smoke)

**Files:**
- Modify: `core/envs/warhamEnv.py` (`_maybe_use_smokescreen`: тот же проброс `resolve_trigger`/`net`, что в Task 4)
- Test: `tests/engine/phases/test_reaction_smokescreen.py`

- [ ] **Step 1: Failing test** — копия Task 4-теста, но юнит с keyword `smoke`, стратагема `smokescreen`:

```python
# как test_go_to_ground_applied..., но:
#   env.enemy_data[0]["Keywords"] = ["Smoke"]
#   ожидать "smokescreen" в env.stratagem_used; вызвать env._maybe_use_smokescreen("enemy", 0, "shooting")
```

- [ ] **Step 2: Run, verify fails** — `pytest tests/engine/phases/test_reaction_smokescreen.py -q`. Expected: FAIL.

- [ ] **Step 3: Implement** — в `_maybe_use_smokescreen` заменить `_should_use_reaction("smokescreen", ...)` на проброс `resolve_trigger=getattr(self,"_pending_reaction_trigger",None)`, `net=getattr(self,"_reaction_net_by_side",{}).get(defender_side)` (идентично Task 4).

- [ ] **Step 4: Run, verify passes** — `pytest tests/engine/phases/test_reaction_smokescreen.py -q`. Expected: PASS.

- [ ] **Step 5: Регресс + commit**

```bash
pytest tests/engine/phases/ -q
git add core/envs/warhamEnv.py tests/engine/phases/test_reaction_smokescreen.py
git commit -m "feat(b3): smokescreen через net-value lookahead"
```

---

## Task 6: overwatch (триггер — overwatch-стрельба по двигавшемуся врагу)

**Files:**
- Modify: `core/envs/warhamEnv.py` (`_resolve_overwatch` ~4214/4219/4226; call-sites overwatch — построить `resolve_trigger`, досимулирующий overwatch-выстрел `attack(... hit_on_6=True)` + `_apply_health_update(...)`)
- Test: `tests/engine/phases/test_reaction_overwatch.py`

- [ ] **Step 1: Failing test** — `tests/engine/phases/test_reaction_overwatch.py`: fake_attack, где overwatch наносит урон врагу → net (value по урону врагу) предпочитает apply; проверить выбор overwatch и списание CP.

```python
# build_env; env.modelCP=3; reaction_policy с net, оценивающим -сумму enemy_health (больше урон врагу => выше value)
# вызвать env._resolve_overwatch("model", "enemy", 0, "movement"); ожидать "overwatch" в stratagem_used
```

- [ ] **Step 2: Run, verify fails** — `pytest tests/engine/phases/test_reaction_overwatch.py -q`. Expected: FAIL.

- [ ] **Step 3: Implement** — в `_resolve_overwatch` перед `_should_use_reaction("overwatch", ...)` (строка ~4214) установить `self._pending_reaction_trigger` как замыкание, досимулирующее overwatch-выстрел `chosen→moving_idx` (тело — копия блока `attack(... hit_on_6=True)` + `_apply_health_update`, без reward/логов), и пробросить `net=...[defender_side]`. После решения — очистить trigger.

- [ ] **Step 4: Run, verify passes** — `pytest tests/engine/phases/test_reaction_overwatch.py -q`. Expected: PASS.

- [ ] **Step 5: Регресс + commit**

```bash
pytest tests/engine/phases/ -q
git add core/envs/warhamEnv.py tests/engine/phases/test_reaction_overwatch.py
git commit -m "feat(b3): overwatch через net-value lookahead"
```

---

## Task 7: heroic_intervention (триггер — counter-charge)

**Files:**
- Modify: `core/envs/warhamEnv.py` (`_resolve_heroic_intervention` ~4303/4364/4369)
- Test: `tests/engine/phases/test_reaction_heroic.py`

- [ ] **Step 1: Failing test** — counter-charge меняет состояние (юнит входит в бой); net, оценивающий «выгоду от counter-charge» (напр. value по тому, что защитник в engagement), предпочитает apply. Проверить `heroic_intervention` в stratagem_used + списание 2 CP.

- [ ] **Step 2: Run, verify fails** — `pytest tests/engine/phases/test_reaction_heroic.py -q`. Expected: FAIL.

- [ ] **Step 3: Implement** — в `_resolve_heroic_intervention` построить `resolve_trigger`, досимулирующий counter-charge (тело — блок установки `unitInAttack`/`enemyInAttack` для `chosen`↔`charging_idx`, как в реальном эффекте `counter_charge`), пробросить `net`, очистить trigger после решения.

- [ ] **Step 4: Run, verify passes** — `pytest tests/engine/phases/test_reaction_heroic.py -q`. Expected: PASS.

- [ ] **Step 5: Регресс + commit**

```bash
pytest tests/engine/phases/ -q
git add core/envs/warhamEnv.py tests/engine/phases/test_reaction_heroic.py
git commit -m "feat(b3): heroic_intervention через net-value lookahead"
```

---

## Task 8: Wiring self-play/eval + smoke + parity-гейт

**Files:**
- Modify: `train.py` / `core/models/alphazero_selfplay.py` (в actor перед роллаутом ставить policy)
- Modify: `eval.py` (ставить policy для learner-стороны)

- [ ] **Step 1: Установка в actor** — там, где actor строит env и имеет `net`/`opp_net`, при `os.environ.get("AZ_REACTION_VALUE_POLICY")=="1"`:

```python
    if str(os.getenv("AZ_REACTION_VALUE_POLICY", "0")).strip() in ("1", "true", "yes", "on"):
        from core.models.reaction_value_policy import make_reaction_value_policy
        env.unwrapped._reaction_net_by_side = {learner_side: net, opp_side: opp_net}
        env.unwrapped.reaction_policy = make_reaction_value_policy(
            env.unwrapped._reaction_net_by_side, device=device
        )
```

(`learner_side`/`opp_side` — "model"/"enemy" по конфигу актора; `opp_net` = снапшот-оппонент или `net` в чистом self-play.)

- [ ] **Step 2: Установка в eval** — аналогично в `eval.py:main()` после загрузки сети: learner-сторона → learner-net, оппонент → его сеть или None.

- [ ] **Step 3: Smoke** — `AZ_REACTION_VALUE_POLICY=1 TRAIN_ALGO=alphazero_tree TRAIN_EPISODES_OVERRIDE=10 AZ_NUM_ACTORS=2 AZ_MCTS_SIMULATIONS=8 python train.py`. Expected: без краша; в `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md` строка `[AZ][CONFIG] ... reaction_value_policy=1`.

- [ ] **Step 4: Parity-гейт (флаг 0)** — `python tools/windowed_parity_winrate.py --episodes 50 --seed 1000`. Expected: Δ между legacy и windowed как до B3 (флаг 0 → код не на пути).

- [ ] **Step 5: Полный регресс** — `pytest tests/engine/phases/ tests/models/ -q`. Expected: зелёное.

- [ ] **Step 6: Commit**

```bash
git add train.py core/models/alphazero_selfplay.py eval.py
git commit -m "feat(b3): wiring reaction_value_policy в self-play/eval + smoke/parity"
```

---

## Self-Review

**Spec coverage:** §2 флаг → Task 1; §3.1 policy → Task 2; §3.3 harness + §3.4 recursion guard/seam → Task 3; §3.4 per-reaction (go_to_ground/smokescreen/overwatch/heroic) → Tasks 4–7; §3.5 wiring + §4 smoke/parity → Task 8. §3.2 value-перспектива → реализовано в harness (Task 3, `get_observation_for_side(side)`).

**Открытые риски для исполнителя:**
- Точные строки call-site сместятся после Task 3 — ищи по `_maybe_use_smokescreen(`/`_resolve_overwatch(`/`_resolve_heroic_intervention(`, не по номерам.
- `resolve_trigger` должен мутировать только sim-состояние (его оборачивает `simulation_mode` + внешний snapshot/restore). НЕ дублируй reward/логи в нём — value считается по состоянию.
- Keyword-доступ (`_unit_has_keyword`/`_unit_has_smoke`) — использовать существующие helper'ы, не хардкодить ключ "Keywords".
