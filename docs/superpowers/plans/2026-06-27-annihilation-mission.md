# Annihilation / Kill Points Mission — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Добавить вторую боевую миссию `annihilation` (40k Kill Points): победа по уничтоженной силе врага, без захвата точек, чтобы уйти от частых ничьих Only War.

**Architecture:** Миссия — это запись в `MISSION_REGISTRY` + scoring-стратегия (`objective_control` ↔ `kill_points`) + reward-профиль. `annihilation` держит фантомную нескорящую точку (obs идентичен Only War), считает Kill Points пересчётом из состояния, разрешает ничьи тай-брейком `destroyed_hp`. Reward-профили — два самодостаточных файла + фасад через module `__getattr__`. Env не переписываем: objective-shaping в annihilation нейтрализуется занулёнными константами профиля, scoring/win — через диспетчер.

**Tech Stack:** Python 3.12, numpy, gymnasium (`spaces.Box`), pytest. Платформа Windows.

## Global Constraints

- Язык логов/UI/сообщений об ошибках — **русский**; ошибка = что случилось + где (файл/функция) + что делать.
- Платформа Windows; GUI — только Qt (PySide6/QML).
- **Не менять формат** существующих `LOGS_FOR_AGENTS_*.md` и Only-War лог-строк; для annihilation — добавлять новые строки.
- **Тест-гейт = нет НОВЫХ падений против базового коммита** (`tests/engine` уже частично красный на baseline). Перед стартом зафиксировать baseline-счётчик: `pytest tests/engine -q` на текущем HEAD.
- TDD: тест до кода. Частые коммиты. DRY/YAGNI.
- Reward v1: боевые/win-loss ключи в annihilation = baseline-копия; **objective/VP-shaping ключи = 0**; тюнинг kill-наград — вне scope.
- Спека: [docs/superpowers/specs/2026-06-27-annihilation-mission-design.md](../specs/2026-06-27-annihilation-mission-design.md).

---

## File Structure

- `core/engine/mission.py` — **modify**: registry-запись annihilation, флаги missions, хелперы, layout-флаги, KP-функции, диспетчеры scoring/win, логи.
- `core/envs/warhamEnv.py` — **modify**: снапшоты ран + KP-init на reset, info-поля.
- `reward_config.py` — **modify**: превратить в фасад-резолвер (`configure_for_mission`/`active_profile_name`/`__getattr__`).
- `reward_config_onlywar.py` — **create**: полная копия текущего `reward_config.py`.
- `reward_config_annihilation.py` — **create**: полный самодостаточный профиль, objective/VP-shaping=0, новые `ANNIHILATION_*`.
- `app/gui_qt/main.py` — **modify**: `annihilation` в `_mission_options`.
- `app/gui_qt/qml/Main.qml` — **modify**: динамический мета-текст миссии.
- Tests: `tests/engine/test_annihilation_mission.py`, `tests/engine/test_annihilation_kill_points.py`, `tests/engine/test_reward_profiles.py`, `tests/engine/test_reward_profiles_no_drift.py`.

---

## Task 1: Mission registry + helpers + layout flags

**Files:**
- Modify: `core/engine/mission.py` (registry ~197-214, `apply_mission_layout` ~272-284, новые хелперы)
- Test: `tests/engine/test_annihilation_mission.py`

**Interfaces:**
- Produces: `MISSION_ANNIHILATION = "annihilation"`; `mission_scoring_mode(value_or_env) -> str` (`"objective_control"|"kill_points"`); `mission_uses_objectives(value_or_env) -> bool`; `is_annihilation_mission(value_or_env) -> bool`; env-атрибуты после layout: `env.mission_key: str`, `env.mission_scoring_mode: str`, `env.mission_uses_objectives: bool`.

- [ ] **Step 1: Write the failing test**

```python
# tests/engine/test_annihilation_mission.py
from core.engine import mission as M


def test_annihilation_registered_and_aliased():
    assert M.normalize_mission_name("annihilation") == "annihilation"
    assert M.normalize_mission_name("purge_the_enemy") == "annihilation"
    assert M.normalize_mission_name("kill_points") == "annihilation"


def test_annihilation_board_is_like_only_war():
    assert M.board_dims_for_mission("annihilation") == (
        M.ONLY_WAR_BOARD_HEIGHT_INCH, M.ONLY_WAR_BOARD_WIDTH_INCH)


def test_annihilation_has_phantom_single_objective():
    coords = M.objective_coords_for_mission("annihilation", 40, 60)
    assert len(coords) == 1  # фантом: obs остаётся как у Only War


def test_mission_flag_helpers():
    assert M.mission_scoring_mode("annihilation") == "kill_points"
    assert M.mission_scoring_mode("only_war") == "objective_control"
    assert M.mission_uses_objectives("annihilation") is False
    assert M.mission_uses_objectives("only_war") is True
    assert M.is_annihilation_mission("purge_the_enemy") is True
    assert M.is_annihilation_mission("only_war") is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/engine/test_annihilation_mission.py -v`
Expected: FAIL (`AttributeError: module ... has no attribute 'MISSION_ANNIHILATION'` / helpers undefined).

- [ ] **Step 3: Add registry entry + flags + helpers**

В `core/engine/mission.py` рядом с константами миссий добавить:
```python
MISSION_ANNIHILATION = "annihilation"
MISSION_NAME_ANNIHILATION = "Annihilation / Kill Points"
```
В `MISSION_REGISTRY` добавить запись и проставить флаги существующим (объект-миссиям — явные `uses_objectives/scoring_mode`):
```python
    MISSION_ANNIHILATION: {
        "aliases": {"annihilation", "kill_points", "killpoints",
                    "purge_the_enemy", "purge_the_alien"},
        "display_name": MISSION_NAME_ANNIHILATION,
        "board_dims": lambda: (int(ONLY_WAR_BOARD_HEIGHT_INCH), int(ONLY_WAR_BOARD_WIDTH_INCH)),
        "objective_coords": _center_objective_coords,   # ФАНТОМ: нескорящая центральная точка
        "terrain_generator": only_war_terrain_features,
        "uses_objectives": False,
        "scoring_mode": "kill_points",
    },
```
В записи `MISSION_ONLY_WAR` и `MISSION_TRAINING_GROUNDS` добавить `"uses_objectives": True, "scoring_mode": "objective_control"`.

Новые хелперы (после `_mission_def`):
```python
def _mission_key_from(value_or_env) -> str:
    """Принимает строку миссии ИЛИ env с атрибутом mission_key."""
    if hasattr(value_or_env, "mission_key"):
        return normalize_mission_name(getattr(value_or_env, "mission_key", None))
    if isinstance(value_or_env, str) or value_or_env is None:
        return normalize_mission_name(value_or_env)
    # env без mission_key (старый путь) -> по display-name
    name = getattr(value_or_env, "mission_name", None)
    return normalize_mission_name(name)


def mission_scoring_mode(value_or_env) -> str:
    mission_def = MISSION_REGISTRY.get(_mission_key_from(value_or_env), MISSION_REGISTRY[MISSION_ONLY_WAR])
    return str(mission_def.get("scoring_mode") or "objective_control")


def mission_uses_objectives(value_or_env) -> bool:
    mission_def = MISSION_REGISTRY.get(_mission_key_from(value_or_env), MISSION_REGISTRY[MISSION_ONLY_WAR])
    return bool(mission_def.get("uses_objectives", True))


def is_annihilation_mission(value_or_env) -> bool:
    return _mission_key_from(value_or_env) == MISSION_ANNIHILATION
```

В `apply_mission_layout` после `env.mission_name = mission_display_name(mission)` добавить:
```python
    env.mission_key = mission
    env.mission_scoring_mode = mission_scoring_mode(mission)
    env.mission_uses_objectives = mission_uses_objectives(mission)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/engine/test_annihilation_mission.py -v`
Expected: PASS (4 теста).

- [ ] **Step 5: Commit**

```bash
git add core/engine/mission.py tests/engine/test_annihilation_mission.py
git commit -m "feat(mission): registry-запись annihilation + флаги/хелперы scoring_mode"
```

---

## Task 2: Kill Points tracking (пересчёт из состояния)

**Files:**
- Modify: `core/envs/warhamEnv.py` (reset, после `model_hp_max_total` ~1185)
- Modify: `core/engine/mission.py` (новые `recompute_kill_points`, `_destroyed_hp`)
- Test: `tests/engine/test_annihilation_kill_points.py`

**Interfaces:**
- Consumes: env-атрибуты `unit_health`, `enemy_health`, `unit_data`, `enemy_data`.
- Produces: на reset — `env.modelKP=0`, `env.enemyKP=0`, `env._start_enemy_unit_wounds: list[int]`, `env._start_model_unit_wounds: list[int]`, `env._mission_destroyed_enemy_units: set[int]`, `env._mission_destroyed_model_units: set[int]`; функции `mission.recompute_kill_points(env, log_fn=None) -> None`, `mission._destroyed_hp(env, side: str) -> int`.

- [ ] **Step 1: Write the failing test**

```python
# tests/engine/test_annihilation_kill_points.py
import types
from core.engine import mission as M


def _fake_env(model_health, enemy_health):
    env = types.SimpleNamespace()
    env.unit_health = list(model_health)
    env.enemy_health = list(enemy_health)
    env._start_model_unit_wounds = list(model_health)
    env._start_enemy_unit_wounds = list(enemy_health)
    env.modelKP = 0
    env.enemyKP = 0
    env.modelVP = 0
    env.enemyVP = 0
    env._mission_destroyed_enemy_units = set()
    env._mission_destroyed_model_units = set()
    return env


def test_kp_counts_destroyed_units():
    env = _fake_env([10, 10], [6, 6, 6])
    env.enemy_health = [0, 6, 0]   # 2 вражеских юнита уничтожены
    M.recompute_kill_points(env)
    assert env.modelKP == 2
    assert env.enemyKP == 0


def test_kp_granted_once_idempotent():
    env = _fake_env([10, 10], [6, 6])
    env.enemy_health = [0, 6]
    M.recompute_kill_points(env)
    M.recompute_kill_points(env)   # повторный вызов не должен «дозасчитать»
    assert env.modelKP == 1


def test_vp_mirrors_kp_for_display():
    env = _fake_env([10], [6, 6])
    env.enemy_health = [0, 0]
    M.recompute_kill_points(env)
    assert env.modelVP == env.modelKP == 2


def test_destroyed_hp_tiebreak_value():
    env = _fake_env([10, 4], [6, 9])
    env.enemy_health = [0, 9]      # убит вражеский юнит со стартовым HP=6
    env.unit_health = [10, 0]      # убит наш юнит со стартовым HP=4
    M.recompute_kill_points(env)
    assert M._destroyed_hp(env, "model") == 6
    assert M._destroyed_hp(env, "enemy") == 4
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/engine/test_annihilation_kill_points.py -v`
Expected: FAIL (`AttributeError: module ... has no attribute 'recompute_kill_points'`).

- [ ] **Step 3: Implement KP functions + reset init**

В `core/engine/mission.py` добавить:
```python
def recompute_kill_points(env, log_fn: Optional[callable] = None) -> None:
    """KP = число полностью уничтоженных вражеских юнитов. Пересчёт из состояния (идемпотентно)."""
    destroyed_enemy = {i for i in range(len(env.enemy_health)) if env.enemy_health[i] <= 0}
    destroyed_model = {i for i in range(len(env.unit_health)) if env.unit_health[i] <= 0}

    prev_enemy = getattr(env, "_mission_destroyed_enemy_units", set())
    prev_model = getattr(env, "_mission_destroyed_model_units", set())
    if log_fn is not None:
        for i in sorted(destroyed_enemy - prev_enemy):
            log_fn(f"[MISSION][Annihilation] KP grant -> side=model enemy_unit_idx={i} "
                   f"KP: {env.modelKP}->{env.modelKP + 1}")
        for i in sorted(destroyed_model - prev_model):
            log_fn(f"[MISSION][Annihilation] KP grant -> side=enemy model_unit_idx={i} "
                   f"KP: {env.enemyKP}->{env.enemyKP + 1}")

    env._mission_destroyed_enemy_units = destroyed_enemy
    env._mission_destroyed_model_units = destroyed_model
    env.modelKP = len(destroyed_enemy)
    env.enemyKP = len(destroyed_model)
    # N2: VP зеркалит KP только для логов/GUI; источник истины — KP.
    env.modelVP = env.modelKP
    env.enemyVP = env.enemyKP


def _destroyed_hp(env, side: str) -> int:
    """Суммарный стартовый HP уничтоженных юнитов (тай-брейк destroyed_hp)."""
    if side == "model":
        return int(sum(env._start_enemy_unit_wounds[i] for i in env._mission_destroyed_enemy_units))
    if side == "enemy":
        return int(sum(env._start_model_unit_wounds[i] for i in env._mission_destroyed_model_units))
    raise ValueError(f"Unknown side: {side}")
```

В `core/envs/warhamEnv.py` сразу после блока `self.model_hp_max_total = max(...)` (перед `self._init_model_state_from_health()`, ~1185) добавить:
```python
        # Annihilation Kill Points: снапшот стартовых ран по юнитам + обнуление KP.
        self._start_enemy_unit_wounds = list(self.enemy_health)
        self._start_model_unit_wounds = list(self.unit_health)
        self.modelKP = 0
        self.enemyKP = 0
        self._mission_destroyed_enemy_units = set()
        self._mission_destroyed_model_units = set()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/engine/test_annihilation_kill_points.py -v`
Expected: PASS (4 теста).

- [ ] **Step 5: Commit**

```bash
git add core/engine/mission.py core/envs/warhamEnv.py tests/engine/test_annihilation_kill_points.py
git commit -m "feat(mission): KP-учёт пересчётом из состояния + снапшот ран на reset"
```

---

## Task 3: Reward-профили (самодостаточные) + фасад

**Files:**
- Create: `reward_config_onlywar.py` (полная копия текущего `reward_config.py`)
- Create: `reward_config_annihilation.py`
- Modify: `reward_config.py` → фасад
- Test: `tests/engine/test_reward_profiles.py`, `tests/engine/test_reward_profiles_no_drift.py`

**Interfaces:**
- Produces: `reward_config.configure_for_mission(mission_name: str | None) -> str`; `reward_config.active_profile_name() -> str`; module-`__getattr__` делегирует все константы на активный профиль; новые константы `ANNIHILATION_KP_PER_UNIT=1`, `ANNIHILATION_TIEBREAK_MODE="destroyed_hp"`, `ANNIHILATION_DRAW_MARGIN=0`.

- [ ] **Step 1: Write the failing test**

```python
# tests/engine/test_reward_profiles.py
import importlib
import pytest
import reward_config as rc


@pytest.fixture(autouse=True)
def _reset_profile():
    yield
    rc.configure_for_mission("only_war")   # анти-поллюшн


def test_default_profile_is_only_war():
    importlib.reload(rc)
    assert rc.active_profile_name() == "only_war"
    assert rc.VP_OBJECTIVE_HOLD_REWARD != 0   # objective-shaping включён


def test_switch_to_annihilation_zeroes_objective_shaping():
    assert rc.configure_for_mission("annihilation") == "annihilation"
    assert rc.active_profile_name() == "annihilation"
    assert rc.VP_OBJECTIVE_HOLD_REWARD == 0
    assert rc.VP_OBJECTIVE_PROXIMITY_REWARD == 0
    assert rc.KILL_ON_OBJECTIVE_BONUS == 0
    assert rc.MISSION_NO_CONTEST_PENALTY == 0
    assert rc.VP_DIFF_REWARD_SCALE == 0
    assert rc.TURN_LIMIT_DRAW_PENALTY == 0
    assert rc.ANNIHILATION_TIEBREAK_MODE == "destroyed_hp"


def test_combat_shaping_present_in_annihilation():
    rc.configure_for_mission("annihilation")
    assert rc.SHOOT_REWARD_DAMAGE_SCALE != 0   # combat-shaping есть (reward v1)
    assert rc.MELEE_REWARD_DAMAGE_SCALE != 0


def test_training_grounds_uses_only_war_profile():
    assert rc.configure_for_mission("training_grounds") == "only_war"
    assert rc.VP_OBJECTIVE_HOLD_REWARD != 0
```

```python
# tests/engine/test_reward_profiles_no_drift.py
import reward_config_onlywar as ow
import reward_config_annihilation as an


def _const_keys(mod):
    return {k for k in vars(mod) if k.isupper() and not k.startswith("_")}


def test_shared_keys_identical_between_profiles():
    mission_specific = {k for k in _const_keys(an) if k.startswith("ANNIHILATION_")}
    shared_annihilation = _const_keys(an) - mission_specific
    shared_only_war = _const_keys(ow)
    missing_in_annihilation = shared_only_war - shared_annihilation
    extra_in_annihilation = shared_annihilation - shared_only_war
    assert not missing_in_annihilation, f"Ключи есть в onlywar, нет в annihilation: {missing_in_annihilation}"
    assert not extra_in_annihilation, f"Лишние общие ключи в annihilation: {extra_in_annihilation}"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/engine/test_reward_profiles.py tests/engine/test_reward_profiles_no_drift.py -v`
Expected: FAIL (`ModuleNotFoundError: reward_config_onlywar` / `configure_for_mission` undefined).

- [ ] **Step 3: Create profiles + facade**

1. **`reward_config_onlywar.py`** — побайтовая копия текущего `reward_config.py` (все константы + `_validate_heur_calibration_override` + `apply_heur_calibration_overrides` + `_HEUR_CALIBRATION_APPLIED_OVERRIDES = apply_heur_calibration_overrides()`):
```bash
cp reward_config.py reward_config_onlywar.py
```
В шапке заменить docstring на: `"""Reward-профиль миссии Only War (самодостаточный)."""`.

2. **`reward_config_annihilation.py`** — копия onlywar, затем:
```bash
cp reward_config_onlywar.py reward_config_annihilation.py
```
- заменить docstring: `"""Reward-профиль миссии Annihilation / Kill Points (самодостаточный)."""`;
- **занулить** objective/VP-shaping константы (значение `= 0.0`, имена сохранить): `VP_OBJECTIVE_HOLD_REWARD`, `VP_OBJECTIVE_HOLD_PENALTY`, `VP_OBJECTIVE_PROXIMITY_REWARD`, `VP_OBJECTIVE_MISSED_PROGRESS_NORM`(оставить ≥1, ставим `6.0`→норм. знаменатель, не зануляем — это делитель), `VP_DIFF_REWARD_SCALE`, `VP_DIFF_PENALTY_SCALE`, `TURN_LIMIT_DRAW_PENALTY`, `TURN_LIMIT_VP_MARGIN_REWARD_SCALE`, `TURN_LIMIT_VP_MARGIN_PENALTY_SCALE`, `VP_OBJECTIVE_STREAK_BONUS`, `VP_OBJECTIVE_OC_MARGIN_SCALE`, `IDLE_OUT_OF_OBJECTIVE_PENALTY`, `OBJECTIVE_PROGRESS_STEP_SCALE`, `OBJECTIVE_PROGRESS_STEP_CAP`, `NO_TARGET_NO_CONTEST_PENALTY`, `KILL_ON_OBJECTIVE_BONUS`, `DAMAGE_ON_OBJECTIVE_SCALE`, `MISSION_NO_CONTEST_PENALTY`, `VP_STALL_PENALTY`, `MELEE_OBJECTIVE_CONTROL_SCALE` → `0.0`. (Делители/нормы и `*_NORM`, `*_START_ROUND`, `*_CAP` НЕ зануляем — только награды/штрафы/масштабы.)
- в конец файла (перед `_HEUR_CALIBRATION_APPLIED_OVERRIDES = ...`) добавить annihilation-ключи:
```python
# ==========================================
# Annihilation / Kill Points (mission-specific)
# ==========================================
ANNIHILATION_KP_PER_UNIT = 1
# Тай-брейк при равных KP: "none" | "destroyed_hp" | "remaining_hp". Дефолт source-sanctioned.
ANNIHILATION_TIEBREAK_MODE = "destroyed_hp"
# Запас под VP-margin режим (0 = строгое равенство KP -> тай-брейк).
ANNIHILATION_DRAW_MARGIN = 0
```

3. **`reward_config.py`** — заменить содержимое на фасад:
```python
"""Фасад reward-конфигурации: делегирует константы на активный профиль миссии.

Профиль выбирается configure_for_mission() (зовётся из mission.apply_mission_layout).
Контракт: все чтения идут как reward_config.X (атрибут); прямой `from reward_config import NAME`
не использовать (захват по значению не увидит смену профиля)."""
import reward_config_onlywar as _profile_only_war
import reward_config_annihilation as _profile_annihilation

_PROFILES = {
    "only_war": _profile_only_war,
    "training_grounds": _profile_only_war,
    "annihilation": _profile_annihilation,
}
_active = _profile_only_war
_active_name = "only_war"


def configure_for_mission(mission_name):
    """Ставит активный reward-профиль по имени миссии. Возвращает имя профиля."""
    global _active, _active_name
    key = (mission_name or "only_war").strip().lower().replace("-", "_").replace(" ", "_")
    profile = _PROFILES.get(key, _profile_only_war)
    _active = profile
    _active_name = "annihilation" if profile is _profile_annihilation else "only_war"
    return _active_name


def active_profile_name():
    return _active_name


def __getattr__(name):
    # Делегируем ВСЁ (константы + apply_heur_calibration_overrides) на активный профиль.
    return getattr(_active, name)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/engine/test_reward_profiles.py tests/engine/test_reward_profiles_no_drift.py tests/engine/test_reward_config_overrides.py -v`
Expected: PASS (профили + drift-guard + существующий heur-override тест не сломан).

- [ ] **Step 5: Commit**

```bash
git add reward_config.py reward_config_onlywar.py reward_config_annihilation.py tests/engine/test_reward_profiles.py tests/engine/test_reward_profiles_no_drift.py
git commit -m "feat(reward): самодостаточные профили миссий + фасад configure_for_mission"
```

---

## Task 4: Scoring & win-condition dispatch

**Files:**
- Modify: `core/engine/mission.py` (`score_end_of_command_phase` ~1182, `check_end_of_battle` ~1239, новый `_resolve_kill_points_winner`)
- Test: `tests/engine/test_annihilation_mission.py` (дополнить)

**Interfaces:**
- Consumes: `mission_scoring_mode(env)`, `recompute_kill_points`, `_destroyed_hp`, `reward_config.ANNIHILATION_TIEBREAK_MODE`.
- Produces: `_resolve_kill_points_winner(env) -> tuple[str | None, str]` (winner, reason); `env._mission_draw_reason: str`; ветки `kill_points` в `score_end_of_command_phase` и `check_end_of_battle`.

- [ ] **Step 1: Write the failing test**

```python
# дополнить tests/engine/test_annihilation_mission.py
import types
import pytest
import reward_config as _rc
from core.engine import mission as M


@pytest.fixture(autouse=True)
def _ann_profile():
    # Тай-брейк читает reward_config.ANNIHILATION_TIEBREAK_MODE — ключ есть только в
    # annihilation-профиле. Активируем его на время тестов файла, сбрасываем после.
    _rc.configure_for_mission("annihilation")
    yield
    _rc.configure_for_mission("only_war")


def _ann_env(model_health, enemy_health, *, battle_round=21):
    env = types.SimpleNamespace()
    env.unit_health = list(model_health)
    env.enemy_health = list(enemy_health)
    env._start_model_unit_wounds = list(model_health)
    env._start_enemy_unit_wounds = list(enemy_health)
    env.modelKP = env.enemyKP = env.modelVP = env.enemyVP = 0
    env._mission_destroyed_enemy_units = set()
    env._mission_destroyed_model_units = set()
    env.mission_key = "annihilation"
    env.mission_scoring_mode = "kill_points"
    env.battle_round = battle_round
    env.game_over = False
    return env


def test_command_phase_no_objective_vp_in_annihilation():
    env = _ann_env([10], [6, 0])
    gained = M.score_end_of_command_phase(env, "model")
    assert gained == 0                 # objective VP не начисляется
    assert env.modelKP == 1            # но KP пересчитан


def test_turn_limit_winner_by_kp():
    env = _ann_env([10, 10], [0, 0, 6])   # model убила 2 вражеских юнита
    over, reason, winner = M.check_end_of_battle(env)
    assert over and reason == "turn_limit" and winner == "model"


def test_turn_limit_equal_kp_tiebreak_destroyed_hp():
    # равные KP (по 1), но model снёс юнит с большим стартовым HP -> побеждает по destroyed_hp
    env = _ann_env([10, 4], [7, 9])       # стартовые раны: model=[10,4], enemy=[7,9]
    env.enemy_health = [0, 9]             # model убил enemy#0 (start HP 7)
    env.unit_health = [10, 0]             # enemy убил model#1 (start HP 4)
    over, reason, winner = M.check_end_of_battle(env)
    assert over and winner == "model"     # 7 > 4


def test_wipeout_enemy_winner_model():
    env = _ann_env([10], [0, 0], battle_round=3)
    over, reason, winner = M.check_end_of_battle(env)
    assert over and reason == "wipeout_enemy" and winner == "model"


def test_only_war_turn_limit_unchanged():
    env = types.SimpleNamespace(unit_health=[10], enemy_health=[10],
                                modelVP=5, enemyVP=2, battle_round=21,
                                mission_key="only_war", mission_scoring_mode="objective_control",
                                game_over=False)
    over, reason, winner = M.check_end_of_battle(env)
    assert over and reason == "turn_limit" and winner == "model"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/engine/test_annihilation_mission.py -v`
Expected: FAIL (annihilation ветки ещё не разветвлены; `score_end_of_command_phase` начислит/упадёт, `check_end_of_battle` сравнит VP).

- [ ] **Step 3: Implement dispatch**

В `core/engine/mission.py` добавить резолвер победителя:
```python
def _resolve_kill_points_winner(env) -> Tuple[str | None, str]:
    import reward_config as reward_cfg
    recompute_kill_points(env)
    m, e = int(env.modelKP), int(env.enemyKP)
    if m > e:
        return "model", "kp"
    if e > m:
        return "enemy", "kp"
    mode = str(getattr(reward_cfg, "ANNIHILATION_TIEBREAK_MODE", "none"))
    if mode == "destroyed_hp":
        mh, eh = _destroyed_hp(env, "model"), _destroyed_hp(env, "enemy")
        if mh > eh:
            return "model", "destroyed_hp"
        if eh > mh:
            return "enemy", "destroyed_hp"
        return None, "equal_kp_and_hp"
    return None, "equal_kp"
```

В начале `score_end_of_command_phase(env, side, log_fn=None)` добавить раннюю ветку:
```python
    if mission_scoring_mode(env) == "kill_points":
        recompute_kill_points(env, log_fn=log_fn)
        if log_fn is not None:
            log_fn(f"[MISSION][Annihilation] objective scoring skipped (mission=annihilation); "
                   f"KP model={env.modelKP} enemy={env.enemyKP}")
        return 0
```
(остальная objective-логика остаётся ниже без изменений).

В `check_end_of_battle(env)` переписать тело с ветвлением по scoring_mode:
```python
def check_end_of_battle(env) -> Tuple[bool, str, str | None]:
    model_wiped = sum(env.unit_health) <= 0
    enemy_wiped = sum(env.enemy_health) <= 0
    kill_points = mission_scoring_mode(env) == "kill_points"

    if model_wiped and enemy_wiped:
        if kill_points:
            winner, reason = _resolve_kill_points_winner(env)
            env._mission_draw_reason = reason if winner is None else ""
            return True, "wipeout_both", winner
        return True, "wipeout_model", None
    if model_wiped:
        return True, "wipeout_model", "enemy"
    if enemy_wiped:
        return True, "wipeout_enemy", "model"

    if env.battle_round > MAX_BATTLE_ROUNDS:
        if kill_points:
            winner, reason = _resolve_kill_points_winner(env)
            env._mission_draw_reason = reason if winner is None else ""
            return True, "turn_limit", winner
        if env.modelVP > env.enemyVP:
            winner = "model"
        elif env.enemyVP > env.modelVP:
            winner = "enemy"
        else:
            winner = None
        return True, "turn_limit", winner

    return False, "", None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/engine/test_annihilation_mission.py -v`
Expected: PASS (все, включая `test_only_war_turn_limit_unchanged`).

- [ ] **Step 5: Commit**

```bash
git add core/engine/mission.py tests/engine/test_annihilation_mission.py
git commit -m "feat(mission): диспетчер scoring/win-condition (kill_points + tiebreak)"
```

---

## Task 5: Env wiring — reward-профиль + info-поля + проверка нейтрализации objective-shaping

**Files:**
- Modify: `core/engine/mission.py` (`apply_mission_layout` — вызов `configure_for_mission`)
- Modify: `core/envs/warhamEnv.py` (info-поля в `_get_observation`/step-info ~8927)
- Test: `tests/engine/test_annihilation_mission.py` (дополнить интеграционным smoke)

**Interfaces:**
- Consumes: `reward_config.configure_for_mission`, `env.mission_key/scoring_mode`, `env.modelKP/enemyKP`.
- Produces: после layout активен корректный reward-профиль; в `info` — поля `mission_key`, `mission_scoring_mode`, `model_kill_points`, `player_kill_points`, `model_destroyed_units`, `player_destroyed_units`, `mission_draw_reason`.

- [ ] **Step 1: Write the failing test**

```python
# дополнить tests/engine/test_annihilation_mission.py
import reward_config as rc
from core.engine import mission as M


def test_apply_layout_sets_reward_profile():
    import types
    env = types.SimpleNamespace()   # apply_mission_layout только ВЫСТАВЛЯЕТ атрибуты
    try:
        M.apply_mission_layout(env, "annihilation")
        assert env.mission_key == "annihilation"
        assert env.mission_scoring_mode == "kill_points"
        assert env.mission_uses_objectives is False
        assert len(env.coordsOfOM) == 1            # фантом-точка
        assert rc.active_profile_name() == "annihilation"
        assert rc.VP_OBJECTIVE_HOLD_REWARD == 0    # objective-shaping нейтрализован профилем
    finally:
        rc.configure_for_mission("only_war")


def test_apply_layout_only_war_keeps_objective_profile():
    import types
    env = types.SimpleNamespace()
    M.apply_mission_layout(env, "only_war")
    assert rc.active_profile_name() == "only_war"
    assert rc.VP_OBJECTIVE_HOLD_REWARD != 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/engine/test_annihilation_mission.py::test_apply_layout_sets_reward_profile -v`
Expected: FAIL (`active_profile_name()` остаётся only_war — layout не зовёт configure_for_mission).

- [ ] **Step 3: Wire reward profile + info fields**

В `core/engine/mission.py`, в начале `apply_mission_layout` после `mission = normalize_mission_name(mission_name)` добавить:
```python
    reward_cfg.configure_for_mission(mission)   # единый chokepoint: train/eval/play/воркеры
```
(`reward_cfg` уже импортирован сверху файла как `import reward_config as reward_cfg`.)

В `core/envs/warhamEnv.py` найти словарь `info`, возвращаемый из `step` (локализовать: `rg -n "info\[|, info|return .*info" core/envs/warhamEnv.py` и выбрать формирование финального `info` в `step`). Добавить поля (после существующих ключей, перед `return`):
```python
        info["mission_key"] = getattr(self, "mission_key", "only_war")
        info["mission_scoring_mode"] = getattr(self, "mission_scoring_mode", "objective_control")
        info["model_kill_points"] = int(getattr(self, "modelKP", 0))
        info["player_kill_points"] = int(getattr(self, "enemyKP", 0))
        info["model_destroyed_units"] = len(getattr(self, "_mission_destroyed_enemy_units", set()))
        info["player_destroyed_units"] = len(getattr(self, "_mission_destroyed_model_units", set()))
        info["mission_draw_reason"] = str(getattr(self, "_mission_draw_reason", ""))
```
(Если в step несколько точек возврата info — добавить там, где формируется финальный info; искать по `return obs` / `, info` в методе step.)

- [ ] **Step 4: Run tests + regression smoke**

Run: `pytest tests/engine/test_annihilation_mission.py -v`
Expected: PASS.

Smoke инициализации annihilation-env (фантом-точка, без падений):
Run: `python -c "import os; os.environ['MISSION_NAME']='annihilation'; import reward_config as rc; print(rc.configure_for_mission('annihilation'), rc.active_profile_name())"`
Expected: `annihilation annihilation`.

- [ ] **Step 5: Commit**

```bash
git add core/engine/mission.py core/envs/warhamEnv.py tests/engine/test_annihilation_mission.py
git commit -m "feat(mission): reward-профиль в apply_mission_layout + KP-поля в info"
```

---

## Task 6: Логирование исходов annihilation

**Files:**
- Modify: `core/engine/mission.py` (`apply_end_of_battle` ~1262, layout-лог)
- Test: `tests/engine/test_annihilation_mission.py` (дополнить лог-тестом)

**Interfaces:**
- Consumes: `env._mission_draw_reason`, `env.modelKP/enemyKP`, `mission_scoring_mode(env)`.
- Produces: лог-строки `[MISSION][Annihilation]` при завершении (winner/draw + причина + tiebreak).

- [ ] **Step 1: Write the failing test**

```python
# дополнить tests/engine/test_annihilation_mission.py
def test_apply_end_of_battle_logs_kp_outcome():
    env = _ann_env([10, 10], [0, 0, 6])   # model 2 KP -> winner
    logs = []
    M.apply_end_of_battle(env, log_fn=logs.append)
    joined = "\n".join(logs)
    assert "[MISSION][Annihilation]" in joined
    assert "winner=model" in joined
    assert "KP model=2" in joined


def test_apply_end_of_battle_logs_draw_reason():
    env = _ann_env([0, 10], [0, 10])      # по 1 KP, стартовые hp равны -> draw
    env._start_enemy_unit_wounds = [10, 10]
    env._start_model_unit_wounds = [10, 10]
    env.enemy_health = [0, 10]
    env.unit_health = [0, 10]
    logs = []
    M.apply_end_of_battle(env, log_fn=logs.append)
    joined = "\n".join(logs)
    assert "draw" in joined and "reason=equal_kp_and_hp" in joined
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/engine/test_annihilation_mission.py -k logs -v`
Expected: FAIL (нет annihilation-лог-строк).

- [ ] **Step 3: Add annihilation logging in apply_end_of_battle**

В `core/engine/mission.py`, в `apply_end_of_battle`, **полностью заменить** блок `if log_fn is not None:` (внутри `if game_over and not env.game_over:`) на разветвлённый по scoring_mode (Only-War формат сохранён без изменений в elif-ветках):
```python
        if log_fn is not None:
            if mission_scoring_mode(env) == "kill_points":
                draw_reason = str(getattr(env, "_mission_draw_reason", "") or "")
                tb = "; tiebreak=destroyed_hp" if draw_reason == "equal_kp_and_hp" else ""
                if winner is None:
                    log_fn(f"[MISSION][Annihilation] {reason} -> draw reason={draw_reason or 'equal_kp'}{tb} "
                           f"(KP model={env.modelKP} enemy={env.enemyKP})")
                else:
                    log_fn(f"[MISSION][Annihilation] {reason} -> winner={winner} "
                           f"(KP model={env.modelKP} enemy={env.enemyKP})")
            elif reason == "turn_limit":
                if winner is None:
                    log_fn(f"Game over: turn_limit -> draw (VP {env.modelVP}-{env.enemyVP})")
                else:
                    log_fn(f"Game over: turn_limit (after BR{MAX_BATTLE_ROUNDS}) -> winner={winner} "
                           f"(VP {env.modelVP}-{env.enemyVP})")
            else:
                if winner is None:
                    log_fn(f"Game over: {reason} -> draw")
                else:
                    log_fn(f"Game over: {reason} -> winner={winner}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/engine/test_annihilation_mission.py -k logs -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/engine/mission.py tests/engine/test_annihilation_mission.py
git commit -m "feat(mission): логи исхода Annihilation (winner/draw + tiebreak)"
```

---

## Task 7: Qt GUI / Viewer

**Files:**
- Modify: `app/gui_qt/main.py:299` (`_mission_options`)
- Modify: `app/gui_qt/qml/Main.qml` (мета-текст миссии)
- Manual smoke (без скриншотов, по AGENTS.md)

**Interfaces:**
- Consumes: `controller.missionOptions`, `controller.selectedMission`.
- Produces: выбор `annihilation` в GUI → `MISSION_NAME=annihilation` уходит в train/eval/play существующим flow.

- [ ] **Step 1: Add mission to options**

В `app/gui_qt/main.py:299` заменить:
```python
        self._mission_options = ["only_war"]
```
на:
```python
        self._mission_options = ["only_war", "annihilation"]
```

- [ ] **Step 2: Dynamic mission meta-text in QML**

В `app/gui_qt/qml/Main.qml` найти блок мета-описания миссии (где показывается текст про центральную точку Only War) и сделать его зависимым от `controller.selectedMission`:
```qml
text: controller.selectedMission === "annihilation"
      ? "Annihilation / Kill Points: точек нет; победа по уничтоженным юнитам врага."
      : "Only War: 1 центральная точка; победа по контролю objective."
```
(Если блока нет — добавить `Label`/`Text` рядом с селектором миссии с этим биндингом.)

- [ ] **Step 3: Viewer — скрыть фантом-маркер**

В `app/viewer/` найти отрисовку objective-радиуса/маркера и обернуть условием «рисуем только если миссия использует точки». Если Viewer получает миссию/флаг — гейт `uses_objectives`; если получает только `objectives` список — для annihilation отрисовку маркера пропустить (фантом виден в obs, но не на экране).

- [ ] **Step 4: Manual smoke**

Запустить Qt GUI (по `/run-40kai`), выбрать миссию `annihilation`, стартовать короткий train/eval, проверить в логах строку `[MISSION][Annihilation]` и отсутствие крашей. Скриншоты не делать.

- [ ] **Step 5: Commit**

```bash
git add app/gui_qt/main.py app/gui_qt/qml/Main.qml app/viewer
git commit -m "feat(gui): миссия annihilation в Qt GUI + Viewer без objective-маркера"
```

---

## Финальная проверка (после всех задач)

- [ ] `pytest tests/engine tests/train -q` — сверить счётчик НОВЫХ падений с baseline (Global Constraints).
- [ ] Точечно: `pytest tests/engine/test_annihilation_mission.py tests/engine/test_annihilation_kill_points.py tests/engine/test_reward_profiles.py tests/engine/test_reward_profiles_no_drift.py -v`.
- [ ] Smoke: короткий train с `MISSION_NAME=annihilation` доигрывает партию, в логах есть KP-grant и исход с причиной.
- [ ] Regression: короткий train с `MISSION_NAME=only_war` — поведение/логи не изменились.

---

## Self-review notes (соответствие спеке)

- C1 фантом-точка → Task 1 (objective_coords=_center_objective_coords, len==1) + obs не трогаем.
- C2 tiebreak destroyed_hp → Task 3 (константа) + Task 4 (`_resolve_kill_points_winner`).
- D1 самодостаточные файлы + drift-guard → Task 3.
- N1 KP пересчётом из состояния → Task 2.
- N2 KP — источник истины, VP зеркало → Task 2 (`recompute_kill_points`).
- N3 baseline-гейт → Global Constraints + Финальная проверка.
- Objective-shaping нейтрализация → через занулённый профиль (Task 3), проверка в Task 5; явный гейт `mission_uses_objectives` — только scoring/win (Task 4) и Viewer (Task 7).
- Вне scope: тюнинг kill-наград, `remaining_hp`/VP-margin режимы, свой террейн.
