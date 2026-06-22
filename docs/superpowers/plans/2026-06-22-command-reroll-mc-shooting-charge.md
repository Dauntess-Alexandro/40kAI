# Command Re-roll Monte-Carlo value — Shooting + Charge — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Распространить Monte-Carlo value-оценку Command Re-roll с fight на **shooting** и **charge**, чтобы DQN/PPO AI решал применять реролл по симуляции исхода выстрела/чарджа, а не по слепому Stage-4 пути.

**Architecture:** Зеркало fight-MC: на старте фазы (через существующий in-phase hook `_apply_phase_command_reroll`) `_value_pick_command_reroll` для shooting/charge симулирует исход против «репрезентативной» цели (shooting — argmax ожидаемого урона; charge — лучший melee-trade), усредняет value по N сэмплам, сравнивает apply vs pass. Живёт в `warhamEnv`, алго-агностично через `_reaction_net_by_side[side]` (DQN max-Q | PPO critic V). Bridges/train/eval не трогаем — shooting/charge идут через hook, не через fight-план.

**Tech Stack:** Python 3.12+, NumPy, PyTorch, Gymnasium-env (`Warhammer40kEnv`), pytest. Windows.

## Global Constraints

- **Источник дизайна:** `docs/superpowers/specs/2026-06-22-command-reroll-mc-shooting-charge-design.md`. Базовая MC-инфра: fight (`_mc_value_command_reroll_fight`, `_simulate_fight_attack`, `_reaction_net_value`, `_cmdreroll_mc_samples/_cmdreroll_mc_eps`) уже в коде.
- **Охват:** только shooting + charge. Advance — вне области. movement-ветка `_value_pick_command_reroll` без изменений.
- **Точка решения — старт фазы**, через `_apply_phase_command_reroll` (Stage 4). **Без правок bridges/train/eval/selfplay/mcts.**
- **Всегда вкл (train+eval)**; гейт по `reaction_policy` + сеть стороны → без них parity (no-op).
- **Репрезентативная цель = лучшая по EV:** shooting — argmax ожидаемого урона; charge — макс. `_melee_strength_score(me) − _melee_strength_score(target)`, тай-брейк ближайшая.
- **Конфиг переиспользуем:** `CMDREROLL_MC_SAMPLES` (8), `CMDREROLL_MC_EPS` (1e-3). Новых флагов нет.
- **Язык:** комментарии/логи русские. Линт: `ruff check --fix <файл>` после правки (ruff срезает неиспользуемые импорты — добавляй с использованием).
- **Baseline тестов:** `tests/engine/` ~23 предсуществующих падения (НЕ регрессии) — сверять счётчик.
- **Коммиты:** только релевантный код; сообщение русское + `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- **DRY/YAGNI/TDD.**

---

## File Structure

| Файл | Ответственность | Задачи |
|------|-----------------|--------|
| `core/envs/warhamEnv.py` | `_expected_shoot_damage`, `_best_shoot_target`, `_simulate_shoot_attack`, `_mc_value_command_reroll_shooting`; `_best_charge_target`, `_simulate_charge_attempt`, `_mc_value_command_reroll_charge`; shooting/charge ветки `_value_pick_command_reroll` | 1–4 |
| `tests/models/test_command_reroll_mc_shooting_charge.py` (новый) | EV-пикер, sim-хелперы, MC-оценщики, ветки value_pick, e2e+parity DQN/PPO | 1–5 |

Все методы — на `Warhammer40kEnv` (как fight-MC). Тесты — отдельный файл, чтобы не раздувать `test_command_reroll_mc_value.py`.

Существующие хелперы (готовы): `get_shoot_targets_for_unit(side, idx)→list[int]`; `get_charge_targets_for_unit(side, idx)→list[int]`; `_charge_roll_with_reroll(side, idx, roll_fn=None)→(np.ndarray, int)`; `_shooting_distance_between_units(sa, ia, sb, ib)→float`; `_melee_strength_score(side, idx)→float`; `_reaction_net_value(side, net)→float`; `_command_reroll_record_exists(side, idx, phase)→bool`; module-level `attack`, `_apply_stratagem`, `distance` (из utils), `np`.

---

## Task 1: `_expected_shoot_damage` + `_best_shoot_target`

**Files:** Modify `core/envs/warhamEnv.py`. Test: `tests/models/test_command_reroll_mc_shooting_charge.py` (новый).

**Interfaces:**
- Produces:
  - `_expected_shoot_damage(self, side, shooter_idx, target_idx) -> float` — аналитический EV урона (без сети/RNG).
  - `_best_shoot_target(self, side, shooter_idx) -> int | None` — argmax EV по `get_shoot_targets_for_unit`; None если целей нет.

- [ ] **Step 1: Написать падающий тест**

Создать `tests/models/test_command_reroll_mc_shooting_charge.py`:
```python
import torch

from tests.engine.phases._helpers import build_env


class _HpAwareNet:
    """value = -sum(HP врага стороны): меньше HP врага → выше value."""

    def __init__(self, env, side):
        self.env = env
        self.side = side

    def infer_with_value(self, obs, masks_by_head=None):
        opp = self.env.enemy_health if self.side == "model" else self.env.unit_health
        return None, torch.tensor([-float(sum(opp))])


def _setup(env, cp=3):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = cp
    env.enemyCP = cp
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env._invalidate_target_cache("mc_sc_test")


def test_expected_shoot_damage_positive_for_valid_target():
    env = build_env()
    _setup(env)
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env._invalidate_target_cache("ev")
    ev = env._expected_shoot_damage("model", 0, 0)
    assert ev > 0.0


def test_best_shoot_target_picks_max_ev(monkeypatch):
    env = build_env()
    _setup(env)
    monkeypatch.setattr(env, "get_shoot_targets_for_unit", lambda side, i: [0, 1])
    monkeypatch.setattr(
        env, "_expected_shoot_damage",
        lambda side, s, t: 5.0 if t == 1 else 1.0,
    )
    assert env._best_shoot_target("model", 0) == 1


def test_best_shoot_target_none_without_targets(monkeypatch):
    env = build_env()
    _setup(env)
    monkeypatch.setattr(env, "get_shoot_targets_for_unit", lambda side, i: [])
    assert env._best_shoot_target("model", 0) is None
```

- [ ] **Step 2: Запустить — упадёт**

Run: `python -m pytest tests/models/test_command_reroll_mc_shooting_charge.py -v`
Expected: FAIL — `AttributeError: ... '_expected_shoot_damage'`.

- [ ] **Step 3: Реализация** — в `core/envs/warhamEnv.py` (рядом с `_mc_value_command_reroll_fight`):
```python
    def _expected_shoot_damage(self, side: str, shooter_idx: int, target_idx: int) -> float:
        """Аналитический EV урона выстрела (без сети/RNG): attacks·P(hit)·P(wound)·P(fail_save)·avg_dmg.

        Для выбора репрезентативной цели MC (ранжирование), не для точного урона.
        """
        from core.engine.utils import _to_int, _wound_target

        if side == "model":
            weapon, defender = self.unit_weapon[shooter_idx], self.enemy_data[target_idx]
        else:
            weapon, defender = self.enemy_weapon[shooter_idx], self.unit_data[target_idx]
        if not isinstance(weapon, dict):
            return 0.0
        attacks = max(0, _to_int(weapon.get("A", weapon.get("Attacks", 1)), default=1))
        bs = _to_int(weapon.get("BS", 4), default=4)
        s = _to_int(weapon.get("S", 4), default=4)
        ap = _to_int(weapon.get("AP", 0), default=0)
        t = _to_int(defender.get("T", 4), default=4)
        sv = _to_int(defender.get("Sv", 7), default=7)
        inv = _to_int(defender.get("IVSave", 0), default=0)
        p_hit = max(0.0, min(1.0, (7 - max(2, min(6, bs))) / 6.0))
        wt = _wound_target(s, t) if (s and t) else 7
        p_wound = max(0.0, min(1.0, (7 - max(2, min(6, wt))) / 6.0)) if wt <= 6 else 0.0
        save_t = sv + ap  # хуже = больше; AP ухудшает
        if inv and (save_t > inv or save_t > 6):
            save_t = inv
        p_fail_save = 1.0 if save_t > 6 else max(0.0, min(1.0, (max(2, save_t) - 1) / 6.0))
        dmg_raw = weapon.get("Damage", weapon.get("D", 1))
        avg_dmg = {"D3": 2.0, "D6": 3.5}.get(str(dmg_raw).strip().upper(), float(_to_int(dmg_raw, default=1)))
        return float(attacks) * p_hit * p_wound * p_fail_save * avg_dmg

    def _best_shoot_target(self, side: str, shooter_idx: int) -> int | None:
        targets = list(self.get_shoot_targets_for_unit(side, int(shooter_idx)) or [])
        if not targets:
            return None
        return max(targets, key=lambda t: self._expected_shoot_damage(side, int(shooter_idx), int(t)))
```

- [ ] **Step 4: Запустить — PASS**

Run: `python -m pytest tests/models/test_command_reroll_mc_shooting_charge.py -v`
Expected: PASS. Затем `ruff check --fix core/envs/warhamEnv.py tests/models/test_command_reroll_mc_shooting_charge.py`.

- [ ] **Step 5: Коммит**
```
git add core/envs/warhamEnv.py tests/models/test_command_reroll_mc_shooting_charge.py
git commit -m "feat(env): EV-пикер цели для shooting MC (_expected_shoot_damage/_best_shoot_target)"
```

---

## Task 2: `_simulate_shoot_attack` + `_mc_value_command_reroll_shooting`

**Files:** Modify `core/envs/warhamEnv.py`. Test: `tests/models/test_command_reroll_mc_shooting_charge.py`.

**Interfaces:**
- Consumes: `_best_shoot_target` (Task 1); `_fight_effects_for_attacker`, `_build_reroll_decider`, `_reaction_net_value`, `_shooting_distance_between_units` (готовы).
- Produces:
  - `_simulate_shoot_attack(self, side, shooter_idx, target_idx) -> None` — симулирует выстрел, читает reroll-эффект (phase shooting), применяет урон (`reason="shooting_sim"`).
  - `_mc_value_command_reroll_shooting(self, side, unit_idx, subtype, samples) -> tuple[float, float]` — `(mean_apply, mean_pass)` против `_best_shoot_target`.

- [ ] **Step 1: Падающий тест**
```python
def test_mc_shooting_apply_beats_pass_when_reroll_adds_damage(monkeypatch):
    env = build_env()
    _setup(env)
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env._invalidate_target_cache("mc_sh")
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}

    def fake_shoot(side, shooter, target):
        dmg = 4.0 if env._command_reroll_record_exists(side, shooter, "shooting") else 1.0
        env._apply_health_update("enemy", target, max(0.0, float(env.enemy_health[target]) - dmg), reason="shooting_sim")

    monkeypatch.setattr(env, "_simulate_shoot_attack", fake_shoot)
    monkeypatch.setattr(env, "_best_shoot_target", lambda side, u: 0)
    ma, mp = env._mc_value_command_reroll_shooting("model", 0, "wound", samples=4)
    assert ma > mp


def test_mc_shooting_zero_when_no_target(monkeypatch):
    env = build_env()
    _setup(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    monkeypatch.setattr(env, "_best_shoot_target", lambda side, u: None)
    assert env._mc_value_command_reroll_shooting("model", 0, "wound", samples=4) == (0.0, 0.0)
```

- [ ] **Step 2: Падает.** Run: `python -m pytest tests/models/test_command_reroll_mc_shooting_charge.py -k mc_shooting -v` → FAIL.

- [ ] **Step 3: Реализация:**
```python
    def _simulate_shoot_attack(self, side: str, shooter_idx: int, target_idx: int) -> None:
        """Симулировать выстрел shooter_idx по target_idx (читает reroll-эффект shooting), применить урон.

        Только в MC-симуляции (внутри snapshot/restore). reason='shooting_sim'.
        """
        if side == "model":
            a_side, atk_h, atk_w, atk_d = "model", self.unit_health, self.unit_weapon, self.unit_data
            d_side, def_h, def_d = "enemy", self.enemy_health, self.enemy_data
        else:
            a_side, atk_h, atk_w, atk_d = "enemy", self.enemy_health, self.enemy_weapon, self.enemy_data
            d_side, def_h, def_d = "model", self.unit_health, self.unit_data
        ai, di = int(shooter_idx), int(target_idx)
        if not (0 <= ai < len(atk_h)) or atk_h[ai] <= 0:
            return
        if not (0 <= di < len(def_h)) or def_h[di] <= 0:
            return
        if not isinstance(atk_w[ai], dict):
            return
        fight_effect = self._fight_effects_for_attacker(a_side, ai)
        reroll_decider = self._build_reroll_decider(a_side, ai, d_side, di, phase="shooting")
        _dmg, mod_health = attack(
            atk_h[ai], atk_w[ai], atk_d[ai], def_h[di], def_d[di],
            rangeOfComb="Ranged", effects=fight_effect, reroll_decider=reroll_decider,
            distance_to_target=self._shooting_distance_between_units(a_side, ai, d_side, di),
        )
        self._apply_health_update(d_side, di, mod_health, reason="shooting_sim")

    def _mc_value_command_reroll_shooting(self, side: str, unit_idx: int, subtype: str, samples: int) -> tuple[float, float]:
        """MC-оценка реролла (subtype) для выстрела юнита по argmax-EV цели: (mean_apply, mean_pass)."""
        net = getattr(self, "_reaction_net_by_side", {}).get(side)
        if net is None:
            return 0.0, 0.0
        target = self._best_shoot_target(side, int(unit_idx))
        if target is None:
            return 0.0, 0.0
        means: dict[str, float] = {}
        for branch in ("pass", "apply"):
            vals: list[float] = []
            for _ in range(max(1, int(samples))):
                inner = self.snapshot_state()
                self._reaction_sim_active = True
                try:
                    with self.simulation_mode():
                        if branch == "apply":
                            _apply_stratagem(self, side, "command_reroll", int(unit_idx), phase="shooting", reroll_roll=str(subtype))
                        self._simulate_shoot_attack(side, int(unit_idx), int(target))
                        vals.append(self._reaction_net_value(side, net))
                finally:
                    self._reaction_sim_active = False
                    self.restore_state(inner)
            means[branch] = sum(vals) / max(1, len(vals))
        return means["apply"], means["pass"]
```

- [ ] **Step 4: PASS.** Run: `python -m pytest tests/models/test_command_reroll_mc_shooting_charge.py -v` → PASS. `ruff check --fix core/envs/warhamEnv.py`.

- [ ] **Step 5: Коммит**
```
git add core/envs/warhamEnv.py tests/models/test_command_reroll_mc_shooting_charge.py
git commit -m "feat(env): MC-оценщик Command Re-roll для shooting (_simulate_shoot_attack/_mc_value_command_reroll_shooting)"
```

---

## Task 3: `_best_charge_target` + `_simulate_charge_attempt` + `_mc_value_command_reroll_charge`

**Files:** Modify `core/envs/warhamEnv.py`. Test: `tests/models/test_command_reroll_mc_shooting_charge.py`.

**Interfaces:**
- Consumes: `get_charge_targets_for_unit`, `_melee_strength_score`, `_charge_roll_with_reroll`, `_reaction_net_value`, module-level `distance`.
- Produces:
  - `_best_charge_target(self, side, unit_idx) -> int | None` — макс. melee-преимущество, тай-брейк ближайшая.
  - `_simulate_charge_attempt(self, side, unit_idx, target_idx) -> None` — 2D6 (с рероллом обеих при записи), при успехе выставить engaged.
  - `_mc_value_command_reroll_charge(self, side, unit_idx, subtype, samples) -> tuple[float, float]`.

- [ ] **Step 1: Падающий тест**
```python
def test_best_charge_target_picks_max_advantage(monkeypatch):
    env = build_env()
    _setup(env)
    monkeypatch.setattr(env, "get_charge_targets_for_unit", lambda side, u: [0, 1])
    monkeypatch.setattr(
        env, "_melee_strength_score",
        lambda side, idx: 9.0 if side == "model" else (1.0 if idx == 1 else 5.0),
    )
    # advantage vs t1 = 9-1=8 > vs t0 = 9-5=4 → t1
    assert env._best_charge_target("model", 0) == 1


def test_mc_charge_apply_beats_pass_when_reroll_makes_charge(monkeypatch):
    env = build_env()
    _setup(env)
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    monkeypatch.setattr(env, "_best_charge_target", lambda side, u: 0)

    def fake_charge(side, u, t):
        # apply (реролл-запись) → успех (engaged); pass → нет
        if env._command_reroll_record_exists(side, u, "charge"):
            env.unitInAttack[u] = [1, t]
            env.enemy_health[t] = max(0.0, float(env.enemy_health[t]) - 2.0)

    monkeypatch.setattr(env, "_simulate_charge_attempt", fake_charge)
    ma, mp = env._mc_value_command_reroll_charge("model", 0, "charge", samples=4)
    assert ma > mp
```

- [ ] **Step 2: Падает.** Run: `python -m pytest tests/models/test_command_reroll_mc_shooting_charge.py -k "charge" -v` → FAIL.

- [ ] **Step 3: Реализация:**
```python
    def _best_charge_target(self, side: str, unit_idx: int) -> int | None:
        targets = list(self.get_charge_targets_for_unit(side, int(unit_idx)) or [])
        if not targets:
            return None
        opp = "enemy" if side == "model" else "model"
        my = self._melee_strength_score(side, int(unit_idx))
        my_coords = self.unit_coords if side == "model" else self.enemy_coords
        opp_coords = self.enemy_coords if side == "model" else self.unit_coords

        def _key(t):
            adv = my - self._melee_strength_score(opp, int(t))
            dist = distance(my_coords[int(unit_idx)], opp_coords[int(t)])
            return (adv, -dist)  # макс. преимущество, тай-брейк ближайшая

        return int(max(targets, key=_key))

    def _simulate_charge_attempt(self, side: str, unit_idx: int, target_idx: int) -> None:
        """Симулировать charge unit_idx→target_idx: 2D6 (реролл обеих при записи), при успехе — engaged.

        Только в MC-симуляции. Без реального перемещения — выставляет inAttack для value-головы.
        """
        ui, ti = int(unit_idx), int(target_idx)
        if side == "model":
            my_coords, opp_coords = self.unit_coords, self.enemy_coords
            my_in, opp_in = self.unitInAttack, self.enemyInAttack
            opp_h = self.enemy_health
        else:
            my_coords, opp_coords = self.enemy_coords, self.unit_coords
            my_in, opp_in = self.enemyInAttack, self.unitInAttack
            opp_h = self.unit_health
        if not (0 <= ti < len(opp_h)) or opp_h[ti] <= 0:
            return
        _dice, total = self._charge_roll_with_reroll(side, ui)
        dist = distance(my_coords[ui], opp_coords[ti])
        if dist - float(total) <= 5:  # порог успеха как в charge_phase (model-путь)
            my_in[ui] = [1, ti]
            opp_in[ti] = [1, ui]

    def _mc_value_command_reroll_charge(self, side: str, unit_idx: int, subtype: str, samples: int) -> tuple[float, float]:
        """MC-оценка charge-реролла для юнита по best-trade цели: (mean_apply, mean_pass)."""
        net = getattr(self, "_reaction_net_by_side", {}).get(side)
        if net is None:
            return 0.0, 0.0
        target = self._best_charge_target(side, int(unit_idx))
        if target is None:
            return 0.0, 0.0
        means: dict[str, float] = {}
        for branch in ("pass", "apply"):
            vals: list[float] = []
            for _ in range(max(1, int(samples))):
                inner = self.snapshot_state()
                self._reaction_sim_active = True
                try:
                    with self.simulation_mode():
                        if branch == "apply":
                            _apply_stratagem(self, side, "command_reroll", int(unit_idx), phase="charge", reroll_roll=str(subtype))
                        self._simulate_charge_attempt(side, int(unit_idx), int(target))
                        vals.append(self._reaction_net_value(side, net))
                finally:
                    self._reaction_sim_active = False
                    self.restore_state(inner)
            means[branch] = sum(vals) / max(1, len(vals))
        return means["apply"], means["pass"]
```

- [ ] **Step 4: PASS.** Run: `python -m pytest tests/models/test_command_reroll_mc_shooting_charge.py -v` → PASS. `ruff check --fix core/envs/warhamEnv.py`.

- [ ] **Step 5: Коммит**
```
git add core/envs/warhamEnv.py tests/models/test_command_reroll_mc_shooting_charge.py
git commit -m "feat(env): MC-оценщик Command Re-roll для charge (_simulate_charge_attempt/_mc_value_command_reroll_charge)"
```

---

## Task 4: ветки shooting/charge в `_value_pick_command_reroll`

**Files:** Modify `core/envs/warhamEnv.py` (`_value_pick_command_reroll`, fight-ветка ~2463-2473). Test: `tests/models/test_command_reroll_mc_shooting_charge.py`.

**Interfaces:**
- Consumes: `_mc_value_command_reroll_shooting` (Task 2), `_mc_value_command_reroll_charge` (Task 3), `_cmdreroll_mc_samples/_cmdreroll_mc_eps`.
- Produces: `_value_pick_command_reroll(side, u, "shooting", ("hit","wound"))` и `(..., "charge", ("charge",))` через MC; movement — без изменений.

- [ ] **Step 1: Падающий тест**
```python
def test_value_pick_shooting_uses_mc(monkeypatch):
    env = build_env()
    _setup(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    env.reaction_policy = lambda ctx: False
    monkeypatch.setattr(
        env, "_mc_value_command_reroll_shooting",
        lambda side, u, sub, n: (5.0, 1.0) if sub == "wound" else (1.0, 1.0),
    )
    assert env._value_pick_command_reroll("model", 0, "shooting", ("hit", "wound")) == "wound"


def test_value_pick_charge_uses_mc(monkeypatch):
    env = build_env()
    _setup(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    env.reaction_policy = lambda ctx: False
    monkeypatch.setattr(env, "_mc_value_command_reroll_charge", lambda side, u, sub, n: (5.0, 1.0))
    assert env._value_pick_command_reroll("model", 0, "charge", ("charge",)) == "charge"


def test_value_pick_shooting_none_below_eps(monkeypatch):
    env = build_env()
    _setup(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    env.reaction_policy = lambda ctx: True
    monkeypatch.setattr(env, "_mc_value_command_reroll_shooting", lambda *a, **k: (1.0, 1.0))
    assert env._value_pick_command_reroll("model", 0, "shooting", ("hit", "wound")) is None
```

- [ ] **Step 2: Падает.** Run: `python -m pytest tests/models/test_command_reroll_mc_shooting_charge.py -k value_pick -v` → FAIL (shooting/charge сейчас идут в generic-loop, который вернёт None/не тот результат).

- [ ] **Step 3: Реализация** — в `_value_pick_command_reroll`, ПОСЛЕ fight-ветки (`if str(phase) == "fight": ... return ...`) и ПЕРЕД generic `for roll in rolls`, добавить общий MC-диспатч для shooting/charge:
```python
        _mc_by_phase = {
            "shooting": self._mc_value_command_reroll_shooting,
            "charge": self._mc_value_command_reroll_charge,
        }
        if str(phase) in _mc_by_phase:
            samples = _cmdreroll_mc_samples()
            eps = _cmdreroll_mc_eps()
            mc_fn = _mc_by_phase[str(phase)]
            best_roll = None
            best_apply = None
            for roll in rolls:
                mean_apply, mean_pass = mc_fn(side, int(unit_idx), str(roll), samples)
                if mean_apply > mean_pass + eps and (best_apply is None or mean_apply > best_apply):
                    best_apply = mean_apply
                    best_roll = roll
            return str(best_roll) if best_roll is not None else None
```
(Generic-loop ниже остаётся для movement.)

- [ ] **Step 4: PASS.** Run: `python -m pytest tests/models/test_command_reroll_mc_shooting_charge.py -v` → PASS. `ruff check --fix core/envs/warhamEnv.py`.

- [ ] **Step 5: Коммит**
```
git add core/envs/warhamEnv.py tests/models/test_command_reroll_mc_shooting_charge.py
git commit -m "feat(env): shooting/charge ветки _value_pick_command_reroll через MC"
```

---

## Task 5: e2e DQN+PPO интеграция + parity + верификация смоуком

**Files:** Test: `tests/models/test_command_reroll_mc_shooting_charge.py`. Верификация — eval-смоук (наблюдательная).

**Interfaces:** Consumes всё выше.

- [ ] **Step 1: Падающие тесты (фазовые hooks применяют под MC; parity без policy)**
```python
from core.engine.phases import stratagem_engine  # noqa: E402  (вверх файла к импортам)
from core.models.dqn_stratagem_bridge import install_dqn_stratagem_policy  # noqa: E402
from tests.engine.phases._helpers import flat_default_action  # noqa: E402


def _engage_shoot(env):
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env._invalidate_target_cache("engage_shoot")


def test_shooting_phase_value_applies_command_reroll(monkeypatch):
    env = build_env()
    _setup(env)
    _engage_shoot(env)
    install_dqn_stratagem_policy(env, {"model": _HpAwareNet(env, "model")}, torch.device("cpu"))
    # MC: реролл выгоден.
    monkeypatch.setattr(env, "_mc_value_command_reroll_shooting", lambda side, u, sub, n: (5.0, 1.0) if sub == "wound" else (1.0, 1.0))
    with env.simulation_mode():
        env.shooting_phase("model", advanced_flags=[False] * len(env.unit_health), action=flat_default_action(len(env.unit_health), shoot_num_0=0))
    assert any(r[1] == "command_reroll" and r[3] == "shooting" for r in env.stratagem_used)


def test_shooting_phase_parity_without_policy():
    env = build_env()
    _setup(env)
    _engage_shoot(env)
    with env.simulation_mode():
        env.shooting_phase("model", advanced_flags=[False] * len(env.unit_health), action=flat_default_action(len(env.unit_health), shoot_num_0=0))
    assert not any(r[1] == "command_reroll" for r in env.stratagem_used)
    assert env.modelCP == 3
```

- [ ] **Step 2: Запустить.** Run: `python -m pytest tests/models/test_command_reroll_mc_shooting_charge.py -k "shooting_phase" -v`. `test_shooting_phase_value_applies...` может зависеть от того, что unit 0 «can_shoot_now» — если кандидат не попадает в `_apply_phase_command_reroll`, тест упадёт; тогда проверить, что `_unit_can_shoot_now("model",0)` True при заданном сетапе (цель в range, не в melee, оружие не "None"). Parity-тест должен пройти сразу.

- [ ] **Step 3: Доп. кода не требуется** (поведение реализовано в Tasks 1-4 + Stage-4 hook). Если `test_shooting_phase_value_applies` падает из-за того, что MC реальный (не замокан) вернул None — здесь он замокан, проверить, что hook реально вызывает `_value_pick_command_reroll` для unit 0 (candidate из `_unit_can_shoot_now`). Если parity-тест падает — `_value_pick_command_reroll` без сети должен возвращать None (guard `net is None`).

- [ ] **Step 4: Полный прогон**

Run: `python -m pytest tests/models/test_command_reroll_mc_shooting_charge.py tests/models/test_command_reroll_mc_value.py tests/models/ tests/engine/phases/ -q`
Expected: PASS. Затем `python -m pytest tests/engine/ -q` → сверить: **23 failed (baseline)**, остальное passed (0 новых). `ruff check --fix tests/models/test_command_reroll_mc_shooting_charge.py`.

- [ ] **Step 5: Верификация смоуком (наблюдательная) + Коммит**

```
PYTHONIOENCODING=utf-8 PPO_REACTION_VALUE_POLICY=1 EVAL_TRACE_STYLE=warhammer \
  python eval.py --learner-agent-id P1_Necrons_only_war_v2_final_ep1000_20260621_193846 --games 6
```
Затем: `grep -iE "applied=command_reroll" runtime/logs/LOGS_FOR_AGENTS_EVAL.md | grep -iE "phase=(shooting|charge)" | head`.
Ожидаемо: ≥1 строка `applied=command_reroll ... phase=shooting|charge` (которой не было). Если 0 — диагностировать (перф/eps/obs `inAttack`-чувствительность для charge), **не подгонять тесты** (см. open questions спеки). В отличие от fight, тут нет hungry_void-starvation — shooting/charge не-fight фазы.
Коммит покрытия:
```
git add tests/models/test_command_reroll_mc_shooting_charge.py
git commit -m "test(ai): e2e shooting/charge Command Re-roll под MC + parity"
```

---

## Self-Review

**Spec coverage:**
- Shooting MC (EV-пикер + sim + оценщик) — Tasks 1-2. ✅
- Charge MC (best-trade пикер + sim + оценщик) — Task 3. ✅
- Интеграция в `_value_pick_command_reroll` (shooting/charge ветки, movement без изменений) — Task 4. ✅
- Единый DQN/PPO через `_reaction_net_value` — переиспользуется в обоих оценщиках. ✅
- Без правок bridges/entry-points — подтверждено (всё через in-phase hook + `_value_pick_command_reroll`). ✅
- Конфиг переиспользуется (`CMDREROLL_MC_SAMPLES/EPS`) — Task 4. ✅
- Parity без policy — Task 5. ✅
- Тесты DQN+PPO — Task 5 (install_dqn) + оценщики алго-агностичны (PPO через тот же `_reaction_net_value`; явный PPO e2e — опционально, т.к. путь идентичен; покрыт parity+DQN+unit). **Частично:** явного PPO-фазового e2e нет (путь алго-агностичен — DQN e2e + unit-оценщики достаточны; PPO smoke в Step 5 покрывает live).
- Критерий готовности (command_reroll в shooting/charge логах) — Task 5 Step 5. ✅

**Placeholder scan:** код во всех шагах полный; Task 5 Step 2/3 честно помечают возможные ветвления (тест может пройти сразу / зависит от `_unit_can_shoot_now`) — это реальная последовательность, не placeholder.

**Type consistency:** `_expected_shoot_damage(side,shooter,target)->float`; `_best_shoot_target(side,shooter)->int|None`; `_simulate_shoot_attack(side,shooter,target)->None`; `_mc_value_command_reroll_shooting(side,unit,subtype,samples)->(float,float)`; `_best_charge_target(side,unit)->int|None`; `_simulate_charge_attempt(side,unit,target)->None`; `_mc_value_command_reroll_charge(side,unit,subtype,samples)->(float,float)` — единообразны во всех задачах и зеркалят fight-MC сигнатуры.

**Примечание по перфу:** MC теперь и в shooting/charge каждый ход при установленной policy — доп. симуляции. EV-пикер аналитический (дёшев). После мержа — замер train steps/s; при деградации снизить `CMDREROLL_MC_SAMPLES`. Не блокирующий шаг плана.

---

## Execution Handoff

См. ниже выбор способа исполнения.
