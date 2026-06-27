# Annihilation Kill-Rewards (v2 + opponent + v3) — Implementation Plan

> **For agentic workers:** исполняется автором инлайн. Шаги — checkbox для трекинга.

**Goal:** Заточить награды миссии `annihilation` под Kill Points: v2 (config — финиш/добивание/самосохранение), правка оппонент-эвристики (не гоняться за фантом-точкой), v3 (value-weighted kill — kill-бонус ∝ ценности убитого юнита).

**Architecture:** v2 и opponent — только значения в `reward_config_annihilation.py` (Only War не трогаем). v3 — новый флаг `KILL_VALUE_WEIGHT_ENABLED`/`KILL_VALUE_NORM` в ОБА профиля (only_war=0, annihilation=1) + правка двух reward-сайтов в `warhamEnv.py` (стрельба/мили), gated флагом. Источник ценности — `_unit_max_hp`.

**Tech Stack:** Python 3.12, pytest. Профиль активен через `reward_config` фасад.

## Global Constraints

- Менять **только** `reward_config_annihilation.py` для v2/opponent; Only War профиль не трогать.
- v3-флаги — в ОБА профиля (drift-guard требует одинаковые ключи); only_war: `KILL_VALUE_WEIGHT_ENABLED=0` (поведение Only War не меняется).
- Reward читается как `reward_cfg.X` (фасад). Никаких `from reward_config import`.
- Тест-гейт: целевые тесты зелёные; `tests/engine` = baseline (17 failed), без новых падений.
- TDD на v3 (правка движка — регрессии дорогие). Язык логов/комментов — RU.
- Только релевантные изменения в коммит.

---

## Task 1: v2 reward-веса (config, профиль annihilation)

**Files:**
- Modify: `reward_config_annihilation.py` (combat-секции)

**Изменения (значение слева→справа):**
- `SHOOT_REWARD_DAMAGE_SCALE` 0.6 → **0.45**
- `SHOOT_REWARD_KILL_BONUS` 0.4 → **0.9**
- `SHOOT_REWARD_OVERKILL_PENALTY` 0.2 → **0.35**
- `SHOOT_REWARD_SKIP_PENALTY` 0.15 → **0.20**
- `SHOOT_REWARD_TARGET_LOW_HP` 0.05 → **0.20**
- `DAMAGE_TAKEN_SCALE` 0.32 → **0.45**
- `MELEE_REWARD_DAMAGE_SCALE` 0.6 → **0.45**
- `MELEE_REWARD_KILL_BONUS` 0.4 → **0.9**
- `MELEE_REWARD_TAKEN_SCALE` 0.5 → **0.6**

- [ ] **Step 1: Write the failing test**

```python
# tests/engine/test_annihilation_kill_rewards.py
import reward_config as rc


def teardown_function():
    rc.configure_for_mission("only_war")


def test_v2_weights_in_annihilation_profile():
    rc.configure_for_mission("annihilation")
    assert rc.SHOOT_REWARD_KILL_BONUS == 0.9
    assert rc.MELEE_REWARD_KILL_BONUS == 0.9
    assert rc.SHOOT_REWARD_TARGET_LOW_HP == 0.20
    assert rc.SHOOT_REWARD_DAMAGE_SCALE == 0.45
    assert rc.MELEE_REWARD_DAMAGE_SCALE == 0.45
    assert rc.SHOOT_REWARD_OVERKILL_PENALTY == 0.35
    assert rc.DAMAGE_TAKEN_SCALE == 0.45
    assert rc.MELEE_REWARD_TAKEN_SCALE == 0.6
    assert rc.SHOOT_REWARD_SKIP_PENALTY == 0.20


def test_only_war_combat_weights_unchanged():
    rc.configure_for_mission("only_war")
    assert rc.SHOOT_REWARD_KILL_BONUS == 0.4   # v2 не затронул Only War
    assert rc.SHOOT_REWARD_DAMAGE_SCALE == 0.6
```

- [ ] **Step 2: Run → FAIL** (`assert 0.4 == 0.9`).
Run: `python -m pytest tests/engine/test_annihilation_kill_rewards.py -q`

- [ ] **Step 3:** Применить 9 правок значений в `reward_config_annihilation.py` (см. список выше). К каждой добавить инлайн-коммент `# v2 (kill-tuned): <старое>-><новое>`.

- [ ] **Step 4: Run → PASS** (2 теста).

- [ ] **Step 5: Commit**

```bash
git add reward_config_annihilation.py tests/engine/test_annihilation_kill_rewards.py
git commit -m "feat(reward): v2 kill-tuned веса для профиля annihilation"
```

---

## Task 2: Opponent heuristic — убрать objective-веса (config, профиль annihilation)

**Files:**
- Modify: `reward_config_annihilation.py` (секция Enemy heuristic)

**Изменения (зануляем objective-веса оппонента; combat-веса оставляем):**
- `ENEMY_HEUR_OBJECTIVE_DIST_W` 0.14 → **0.0**
- `ENEMY_HEUR_OBJECTIVE_CONTROL_W` 0.42 → **0.0**
- `ENEMY_HEUR_OBJECTIVE_PRESSURE_W` 0.18 → **0.0**
- `ENEMY_HEUR_SHOOT_OBJECTIVE_W` 0.15 → **0.0**
- `ENEMY_HEUR_CHARGE_OBJECTIVE_W` 0.25 → **0.0**
- `ENEMY_HEUR_OBJECTIVE_CONTROL_ENABLED` 1 → **0**

(Флаг-suffix `_ENABLED` — менять руками; HEUR_CALIBRATION его трогать не может. `*_OBJ_MULT` фазовые множители не трогаем — они множат уже нулевые веса.)

- [ ] **Step 1: Write the failing test** (дополнить `test_annihilation_kill_rewards.py`)

```python
def test_opponent_objective_weights_zeroed_in_annihilation():
    rc.configure_for_mission("annihilation")
    assert rc.ENEMY_HEUR_OBJECTIVE_CONTROL_W == 0.0
    assert rc.ENEMY_HEUR_OBJECTIVE_DIST_W == 0.0
    assert rc.ENEMY_HEUR_OBJECTIVE_PRESSURE_W == 0.0
    assert rc.ENEMY_HEUR_SHOOT_OBJECTIVE_W == 0.0
    assert rc.ENEMY_HEUR_CHARGE_OBJECTIVE_W == 0.0
    assert int(rc.ENEMY_HEUR_OBJECTIVE_CONTROL_ENABLED) == 0


def test_only_war_opponent_objective_weights_intact():
    rc.configure_for_mission("only_war")
    assert rc.ENEMY_HEUR_OBJECTIVE_CONTROL_W == 0.42
```

- [ ] **Step 2: Run → FAIL.**

- [ ] **Step 3:** Применить 6 правок в `reward_config_annihilation.py` (секция Enemy heuristic), инлайн-коммент `# annihilation: оппонент не гоняется за фантом-точкой`.

- [ ] **Step 4: Run → PASS.**

- [ ] **Step 5: Commit**

```bash
git add reward_config_annihilation.py tests/engine/test_annihilation_kill_rewards.py
git commit -m "feat(reward): оппонент-эвристика в annihilation без objective-весов"
```

---

## Task 3: v3 — value-weighted kill bonus (флаги + движок, TDD)

**Files:**
- Modify: `reward_config_onlywar.py`, `reward_config_annihilation.py` (новые флаги в ОБА)
- Modify: `core/envs/warhamEnv.py` (стрельба ~6355-6358, мили ~7537-7538)
- Test: `tests/engine/test_annihilation_kill_rewards.py`, `tests/engine/test_kill_value_weight.py`

**Interfaces:**
- Produces: `KILL_VALUE_WEIGHT_ENABLED` (only_war=0, annihilation=1), `KILL_VALUE_NORM=8.0` (оба); helper `Warhammer40kEnv._kill_value_factor(side, unit_idx) -> float`.

**Дизайн фактора:** `factor = clamp(_unit_max_hp(side, idx) / KILL_VALUE_NORM, 0.3, 2.5)` если `KILL_VALUE_WEIGHT_ENABLED`, иначе `1.0`. Юнит с max_hp=NORM → ×1.0 (нейтрально); крупнее → дороже, мельче → дешевле. Согласует kill-бонус с destroyed_hp тай-брейком.

- [ ] **Step 1: Add flags to BOTH profiles**

В `reward_config_onlywar.py` и `reward_config_annihilation.py` рядом с combat-секцией (после `MELEE_*`) добавить:
```python
# Value-weighted kill: kill-бонус домножается на ценность убитого юнита (max_hp/NORM).
# only_war=0 (плоский бонус), annihilation=1 (согласует с destroyed_hp тай-брейком).
KILL_VALUE_WEIGHT_ENABLED = 0   # в annihilation-профиле = 1
KILL_VALUE_NORM = 8.0
```
(в `reward_config_annihilation.py` — `KILL_VALUE_WEIGHT_ENABLED = 1`.)

- [ ] **Step 2: Write failing tests**

```python
# tests/engine/test_kill_value_weight.py
import types
import reward_config as rc
from core.envs.warhamEnv import Warhammer40kEnv


def teardown_function():
    rc.configure_for_mission("only_war")


def _factor(enabled, max_hp, norm=8.0):
    rc.configure_for_mission("annihilation" if enabled else "only_war")
    env = object.__new__(Warhammer40kEnv)   # без полного reset
    env.enemy_health = [max_hp]
    env.enemy_data = [{"W": max_hp, "#OfModels": 1}]
    # _unit_max_hp должен вернуть max_hp
    return Warhammer40kEnv._kill_value_factor(env, "enemy", 0)


def test_factor_disabled_is_one():
    assert _factor(enabled=False, max_hp=20) == 1.0


def test_factor_scales_with_value():
    rc.configure_for_mission("annihilation")
    # max_hp == NORM -> 1.0
    assert abs(_factor(enabled=True, max_hp=8) - 1.0) < 1e-6
    # крупный юнит -> >1 (с клампом 2.5)
    assert _factor(enabled=True, max_hp=40) == 2.5
    # мелкий -> <1 (с клампом 0.3)
    assert _factor(enabled=True, max_hp=1) == 0.3
```
```python
# дополнить tests/engine/test_annihilation_kill_rewards.py
def test_kill_value_flags_present_both_profiles():
    rc.configure_for_mission("only_war")
    assert int(rc.KILL_VALUE_WEIGHT_ENABLED) == 0
    rc.configure_for_mission("annihilation")
    assert int(rc.KILL_VALUE_WEIGHT_ENABLED) == 1
    assert rc.KILL_VALUE_NORM == 8.0
```

- [ ] **Step 3: Run → FAIL** (`_kill_value_factor` не существует).

- [ ] **Step 4: Implement helper + wire two sites**

В `core/envs/warhamEnv.py` добавить метод (рядом с `_unit_max_hp`):
```python
    def _kill_value_factor(self, side: str, unit_idx: int) -> float:
        """Множитель kill-бонуса по ценности убитого юнита (max_hp/NORM).
        Включается флагом KILL_VALUE_WEIGHT_ENABLED (annihilation=1, only_war=0)."""
        if not int(getattr(reward_cfg, "KILL_VALUE_WEIGHT_ENABLED", 0)):
            return 1.0
        norm = max(1.0, float(getattr(reward_cfg, "KILL_VALUE_NORM", 8.0)))
        max_hp = float(self._unit_max_hp(side, unit_idx))
        return max(0.3, min(2.5, max_hp / norm))
```
Стрельба — строка 6357, заменить:
```python
                            kill_term = reward_cfg.SHOOT_REWARD_KILL_BONUS
```
на:
```python
                            kill_term = reward_cfg.SHOOT_REWARD_KILL_BONUS * self._kill_value_factor("enemy", idOfE)
```
Мили — строки 7537-7538, заменить плоский `kill_delta` на сумму факторов по реально убитым юнитам:
```python
            kill_delta = max(0, post_enemy_dead - pre_enemy_dead)
            kill_value_sum = 0.0
            for enemy_idx, pre_hp in pre_enemy_hp_by_idx.items():
                if pre_hp > 0 and float(self.enemy_health[enemy_idx]) <= 0:
                    kill_value_sum += self._kill_value_factor("enemy", enemy_idx)
            kill_term = reward_cfg.MELEE_REWARD_KILL_BONUS * (kill_value_sum if kill_value_sum > 0 else kill_delta)
```
(`pre_enemy_hp_by_idx` уже доступен в этой ветке — используется ниже для objective-kills.)

- [ ] **Step 5: Run → PASS** (`test_kill_value_weight.py` + флаг-тест).
Run: `python -m pytest tests/engine/test_kill_value_weight.py tests/engine/test_annihilation_kill_rewards.py -q`

- [ ] **Step 6: Regression** — Only War kill-бонус не изменился (флаг=0 → factor=1.0).
Run: `python -m pytest tests/engine -q --continue-on-collection-errors 2>&1 | tail -3` → 17 failed (baseline).

- [ ] **Step 7: Commit**

```bash
git add reward_config_onlywar.py reward_config_annihilation.py core/envs/warhamEnv.py tests/engine/test_kill_value_weight.py tests/engine/test_annihilation_kill_rewards.py
git commit -m "feat(reward): v3 value-weighted kill bonus (annihilation), флаг + движок"
```

---

## Финальная проверка
- [ ] `python -m pytest tests/engine/test_annihilation_mission.py tests/engine/test_annihilation_kill_points.py tests/engine/test_reward_profiles.py tests/engine/test_reward_profiles_no_drift.py tests/engine/test_annihilation_kill_rewards.py tests/engine/test_kill_value_weight.py -q` — всё зелёное.
- [ ] `python -m pytest tests/engine -q --continue-on-collection-errors` — 17 failed (baseline, без новых).
- [ ] drift-guard зелёный (флаги добавлены в оба профиля).
- [ ] (Опционально, по слову заказчика) A/B-eval: короткий annihilation-прогон, сверить draw-rate/KP-margin v1 vs v2+v3.

## Вне scope
- A/B-замер как отдельный eval-ран (предложу после реализации).
- Тюнинг `KILL_VALUE_NORM`/клампов по результатам A/B.
