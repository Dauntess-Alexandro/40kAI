# Дизайн: миссия Annihilation / Kill Points (без захвата точек)

- **Дата:** 2026-06-27
- **Ветка:** worktree2
- **Статус:** утверждён заказчиком (решения C1/C2/D1/N зафиксированы), готов к декомпозиции в план.
- **Формат:** спека под мульти-модельный поток (дирижёр → исполнители). Раздел 7 — work-packages с файлами, интерфейсами и критериями приёмки.

---

## 1. Цель и мотивация

Сейчас единственная боевая миссия — `only_war`: одна центральная точка, VP только за её контроль. Корень частых ничьих: обе стороны стягиваются на одну спорную точку → OC равны → 0–0 → draw (см. [`mission.py`](../../../core/engine/mission.py)). Поднятый до BR20 лимит это лишь маскирует.

Добавляем **вторую миссию `annihilation`** по логике Warhammer 40k 5–7 ed «Kill Points / Purge the Enemy»: **победа по уничтоженной силе врага, без захвата точек**. Это:
- максимально «контактная» миссия → бьёт по draw сильнее всего;
- ложится на уже сделанный KataGo-margin reward (непрерывный сигнал);
- раскрывает DQN/PPO там, где они сильны — в тактике боя (фокус-огонь, allocate_shots, charge-EV).

**Источники по правилам/ничьей** (проверены): KP = число полностью уничтоженных вражеских юнитов; больше KP = победа; равные KP = ничья, при этом правила **явно разрешают вторичный тай-брейк**. Поэтому дефолтный тай-брейк по убитым ранам — каноночно и решает draw-проблему.

---

## 2. Зафиксированные решения

| ID | Решение | Обоснование |
|----|---------|-------------|
| **C1** | **Фантомная нескорящая точка**: `annihilation` держит ту же 1 центральную координату в `coordsOfOM`, что и `only_war`, но `uses_objectives=False` и `scoring_mode="kill_points"`. Точка **не скорит** и objective-shaping для неё выключен. | Размер obs зависит от `len(coordsOfOM)` ([`warhamEnv.py:1189`](../../../core/envs/warhamEnv.py#L1189), [`:1192`](../../../core/envs/warhamEnv.py#L1192)). Пустой `coordsOfOM` → другой obs-размер (несовместимость моделей/сети) **и** краши в необгороженных `min(... for obj in coordsOfOM)` ([`:2293`](../../../core/envs/warhamEnv.py#L2293), [`:2301`](../../../core/envs/warhamEnv.py#L2301), [`:2302`](../../../core/envs/warhamEnv.py#L2302)). Фантом сохраняет obs идентичным Only War (перенос моделей возможен) и снимает crash-surface целиком. |
| **C2** | **Дефолтный тай-брейк `destroyed_hp`** (по суммарному max-HP уничтоженных юнитов). `"none"` (строгий KP) остаётся опцией. | Чистый KP-count на малом ростере часто даёт равные целые → ничьи (против цели миссии). Источник сам предусматривает вторичный счёт. |
| **D1** | **Полные самодостаточные reward-файлы**: `reward_config_onlywar.py` и `reward_config_annihilation.py`, каждый содержит ВСЕ ключи (без импорта общего из соседа). `reward_config.py` — фасад-резолвер. + **drift-guard тест**. | Выбор заказчика. Guard-тест компенсирует риск дрейфа общих ключей. |
| **N1** | KP считаем **пересчётом из состояния** каждый шаг, не событийным хуком на путь урона. | Идемпотентно, не врезается в стрельбу/мили/mortal/overwatch. |
| **N2** | **KP — источник истины.** `modelVP/enemyVP` зеркалят KP только для логов/GUI; ни один shaping в annihilation не читает VP. | Не смешивать две сущности. |
| **N3** | Тест-гейт = «нет **новых** падений против базового коммита» (база `tests/engine` уже ~красная). | Реальность baseline. |
| **N4** | Снят C1 (фантом) — downstream `min()` работает. | — |
| **N5** | Логи/GUI/Viewer — по конвенциям, явные «почему», без тихих пропусков. | — |

**Reward v1-политика (явное допущение для ревью):** на этом этапе делаем **только логику миссии**. `reward_config_annihilation.py` создаётся как полный самодостаточный модуль, где **objective/VP-shaping ключи занулены**, а боевые/террейн/win-loss ключи берут текущие baseline-значения (копия), чтобы агент мог обучаться драться уже в v1. **Тюнинг annihilation-специфичных наград — отдельная будущая задача** (вне scope, см. §9). Если заказчик хочет иной старт (полностью пустой файл-заглушка) — поправим на ревью-гейте.

---

## 3. Архитектура (high-level)

Миссия определяется **только** четырьмя вещами, остальное общее:
1. **registry-запись** (`MISSION_REGISTRY` в `mission.py`): board/deploy/terrain (как Only War), `objective_coords` (фантом-центр), флаги `uses_objectives`/`scoring_mode`;
2. **scoring-стратегия** (диспетчер по `scoring_mode`): `objective_control` ↔ `kill_points`;
3. **win-condition** (диспетчер): VP-сравнение ↔ KP-сравнение + тай-брейк;
4. **reward-профиль** (`reward_config` фасад выбирает `_onlywar` или `_annihilation`).

Env **не переписываем** — он продолжает звать `score_end_of_command_phase()`, `apply_end_of_battle()`, `refresh_objective_control()`; objective-shaping блоки гейтятся одним предикатом `mission_uses_objectives(self)`.

---

## 4. Компоненты и интерфейсы

### 4.1 Mission registry + helpers (`core/engine/mission.py`)

Добавить:
```python
MISSION_ANNIHILATION = "annihilation"
MISSION_NAME_ANNIHILATION = "Annihilation / Kill Points"
```
Запись реестра:
```python
MISSION_ANNIHILATION: {
    "aliases": {"annihilation", "kill_points", "killpoints",
                "purge_the_enemy", "purge_the_alien"},
    "display_name": MISSION_NAME_ANNIHILATION,
    "board_dims": lambda: (ONLY_WAR_BOARD_HEIGHT_INCH, ONLY_WAR_BOARD_WIDTH_INCH),  # 40x60 как Only War
    "objective_coords": _center_objective_coords,   # ФАНТОМ: та же центральная точка
    "terrain_generator": only_war_terrain_features,  # тот же террейн v1
    "uses_objectives": False,
    "scoring_mode": "kill_points",
}
```
У `only_war`/`training_grounds` добавить явно `"uses_objectives": True, "scoring_mode": "objective_control"`.

Хелперы (принимают строку миссии ИЛИ env):
```python
def mission_scoring_mode(value_or_env) -> str        # "objective_control" | "kill_points"
def mission_uses_objectives(value_or_env) -> bool
def is_annihilation_mission(value_or_env) -> bool
```
Резолв: если передан env — читаем `env.mission_key`; иначе `normalize_mission_name(value)`.

В `apply_mission_layout(env, mission_name)` дополнительно сохранять:
```python
env.mission_key = mission            # normalized key, НЕ display-name
env.mission_uses_objectives = mission_uses_objectives(mission)
env.mission_scoring_mode = mission_scoring_mode(mission)
```

### 4.2 Фантомная точка
`objective_coords = _center_objective_coords` → `coordsOfOM` длиной 1 (как Only War). Никаких изменений в obs-плумбинге. Для Viewer фантом помечается флагом `uses_objectives=False` (см. 4.8) — маркер не рисуется, но в obs присутствует.

### 4.3 KP tracking — пересчёт из состояния (`warhamEnv` + `mission.py`)

Снапшот на `reset` (там же, где инициализируются `unit_health`/`enemy_health`, [`warhamEnv.py:1152`](../../../core/envs/warhamEnv.py#L1152)/[`:1172`](../../../core/envs/warhamEnv.py#L1172)):
```python
self._start_enemy_unit_wounds = list(self.enemy_health)   # W*#models на старте = полный HP
self._start_model_unit_wounds = list(self.unit_health)
self.modelKP = 0
self.enemyKP = 0
self._mission_destroyed_enemy_units = set()
self._mission_destroyed_model_units = set()
```
Функция пересчёта (в `mission.py`, вызывается из scoring/end-чека; идемпотентна):
```python
def recompute_kill_points(env, log_fn=None) -> None:
    destroyed_enemy = {i for i in range(len(env.enemy_health)) if env.enemy_health[i] <= 0}
    destroyed_model = {i for i in range(len(env.unit_health)) if env.unit_health[i] <= 0}
    # лог только для НОВЫХ уничтожений (diff с прошлым set)
    new_enemy = destroyed_enemy - env._mission_destroyed_enemy_units
    new_model = destroyed_model - env._mission_destroyed_model_units
    ...  # лог [MISSION][Annihilation] KP-grant per new unit
    env._mission_destroyed_enemy_units = destroyed_enemy
    env._mission_destroyed_model_units = destroyed_model
    env.modelKP = len(destroyed_enemy)   # model уничтожила столько ВРАЖЕСКИХ юнитов
    env.enemyKP = len(destroyed_model)
    env.modelVP = env.modelKP            # N2: зеркало для логов/GUI
    env.enemyVP = env.enemyKP
```
`destroyed_hp` (тай-брейк):
```python
def _destroyed_hp(env, side) -> int:
    if side == "model":   # сколько вражеских ран model «снёс под ноль»
        return sum(env._start_enemy_unit_wounds[i] for i in env._mission_destroyed_enemy_units)
    return sum(env._start_model_unit_wounds[i] for i in env._mission_destroyed_model_units)
```

### 4.4 Scoring & win-condition (диспетчеры в `mission.py`)

`score_end_of_command_phase(env, side, log_fn)` — разветвить по `mission_scoring_mode(env)`:
- `objective_control` → текущая логика без изменений;
- `kill_points` → `recompute_kill_points(env)`, **VP за objective не начисляем**, лог: `[MISSION][Annihilation] objective scoring skipped (mission=annihilation), KP model=X enemy=Y`.

`check_end_of_battle(env)` — разветвить:
- wipeout enemy → `winner="model"`; wipeout model → `winner="enemy"` (как сейчас);
- **оба wipeout** → `kill_points`: `recompute_kill_points`; сравнить KP → тай-брейк → draw;
- **turn_limit**:
  - `objective_control` → текущее VP-сравнение;
  - `kill_points` → `recompute_kill_points`; победитель по `modelKP` vs `enemyKP`; при равенстве — тай-брейк `ANNIHILATION_TIEBREAK_MODE`:
    - `"destroyed_hp"` → сравнить `_destroyed_hp(model)` vs `_destroyed_hp(enemy)`;
    - `"none"` → сразу draw;
    - если тай-брейк тоже равен → draw (`draw_reason="equal_kp"` / `"equal_kp_and_hp"`).

`apply_end_of_battle` — логирование draw/winner с явной причиной (`draw_reason`, `tiebreak`).

### 4.5 Reward-config split (`reward_config*.py`)

**Файлы:**
- `reward_config_onlywar.py` — полная копия текущего `reward_config.py` (ВСЕ константы + `apply_heur_calibration_overrides` machinery + `_HEUR_CALIBRATION_APPLIED_OVERRIDES = ...`).
- `reward_config_annihilation.py` — **полный самодостаточный** модуль: те же ключи; objective/VP-shaping занулены; добавлены annihilation-ключи. Боевые/террейн/win-loss = baseline-копия (reward v1-политика, §2).
- `reward_config.py` — **фасад-резолвер** (см. ниже).

**Зануляемые в annihilation ключи** (objective/VP-shaping): `VP_OBJECTIVE_*`, `VP_DIFF_*`, `VP_STALL_*`, `TURN_LIMIT_*` (включая `TURN_LIMIT_DRAW_PENALTY=0` на v1), `MISSION_NO_CONTEST_*`, `OBJECTIVE_PROGRESS_*`, `IDLE_OUT_OF_OBJECTIVE_PENALTY`, `NO_TARGET_NO_CONTEST_*`, `KILL_ON_OBJECTIVE_BONUS`, `DAMAGE_ON_OBJECTIVE_SCALE`, `MELEE_OBJECTIVE_CONTROL_SCALE` → 0.

**Новые annihilation-ключи:**
```python
ANNIHILATION_KP_PER_UNIT = 1
ANNIHILATION_TIEBREAK_MODE = "destroyed_hp"   # C2 default; допустимо: "none" | "destroyed_hp" | "remaining_hp"
ANNIHILATION_DRAW_MARGIN = 0                  # запас на VP-margin режим (0 = строгое равенство KP)
```

**Фасад `reward_config.py` (механизм — module `__getattr__`, PEP 562):** фасад НЕ объявляет констант сам, а делегирует на активный профиль-модуль:
```python
import reward_config_onlywar as _profile_only_war
import reward_config_annihilation as _profile_annihilation
_PROFILES = {"only_war": _profile_only_war, "training_grounds": _profile_only_war,
             "annihilation": _profile_annihilation}
_active = _profile_only_war          # дефолт
def configure_for_mission(mission_name: str | None) -> str: ...   # ставит _active, возвращает имя профиля
def active_profile_name() -> str: ...
def __getattr__(name):               # делегирует ВСЁ остальное на активный профиль
    return getattr(_active, name)
```
Преимущество над мутацией глобалов: **одно** изменяемое состояние (`_active`), чтения всегда живые, нет stale-копий. C3 закрыт.

**Контракт (C3):**
- `configure_for_mission(mission)` вызывается **один раз** на старте процесса после резолва миссии: в `train.py`, `eval.py`, `play.py`/`game_controller`, и в entry-точках воркеров (env-worker, distributed actors).
- Тест-фикстура сбрасывает `_active` на дефолт после теста (анти-поллюшн).
- Существующий механизм `apply_heur_calibration_overrides` / `HEUR_CALIBRATION_OVERRIDES_JSON` живёт **внутри каждого профиля** (исполняется при импорте профиля); фасад делегирует вызов на активный профиль. Проверить `tools/heur_calibrate.py` и `tests/engine/test_reward_config_overrides.py` — должны работать через фасад без правок (дефолт-профиль уже активен на импорте).

**Drift-guard (D1):** тест `tests/engine/test_reward_profiles_no_drift.py`: множество ОБЩИХ ключей (всё, кроме `ANNIHILATION_*` и явно объявленного списка `_MISSION_SPECIFIC_KEYS`) должно **присутствовать в обоих** профилях; типы совпадают. Падение = кто-то добавил ключ только в один файл.

### 4.6 Env gating (`warhamEnv.py`)

Все objective-specific reward-блоки обернуть предикатом `mission_uses_objectives(self)`:
- proximity/hold rewards, missed-objective-progress penalty, OC-margin reward, objective-streak reward, mission no-contest pressure, VP-stall penalty, idle-out-of-objective, no-target-no-contest, kill/damage-on-objective бонусы.
- **Оставить включёнными** (общие): shooting damage/kill, melee damage/kill, damage taken, terrain-shaping, win/loss bonus.

`info` (в `_get_observation`/step-info, [`warhamEnv.py:8927`](../../../core/envs/warhamEnv.py#L8927)) дополнить:
`mission_key`, `mission_scoring_mode`, `model_kill_points`, `player_kill_points`, `model_destroyed_units`, `player_destroyed_units`, `mission_draw_reason` (если draw).

### 4.7 Логирование (без «тишины»)
- layout: `[MISSION][Annihilation] objectives=1(phantom, non-scoring) scoring=kill_points`;
- command phase: `[MISSION][Annihilation] objective scoring skipped (mission=annihilation); KP model=X enemy=Y`;
- первое уничтожение: `[MISSION][Annihilation] KP grant -> side=model unit=#13(Name) KP: 2->3`;
- turn limit: `[MISSION][Annihilation] turn_limit -> KP model=X enemy=Y winner=... | draw reason=equal_kp tiebreak=destroyed_hp(mX,eY)`.
- **Формат Only-War логов не менять**, только добавлять строки для annihilation.

### 4.8 Qt GUI / Viewer / запуск
- `controller.missionOptions` (Qt GUI) — добавить `annihilation`.
- QML мета-блок миссии — динамический: `only_war` → текущий текст про центр-точку; `annihilation` → «Kill Points», «точек нет», «победа по уничтоженным юнитам».
- `MISSION_NAME=annihilation` уходит в train/eval/play существующим GUI-flow (проверить проброс).
- Viewer: при `uses_objectives=False` не рисовать objective-radius/маркер (фантом скрыт визуально).

---

## 5. Поток данных
`reset` → `apply_mission_layout` ставит `mission_key/scoring_mode/uses_objectives`, фантом-точку, снапшоты ран, обнуляет KP; `configure_for_mission` ставит reward-профиль (вызывается выше по стеку, в train/eval/play).
`step` → бой меняет health; objective-shaping гейтнут; combat-shaping активен.
конец фазы команд → `score_end_of_command_phase` (kill_points: только `recompute_kill_points`, без VP).
проверка конца → `apply_end_of_battle`/`check_end_of_battle` (kill_points: KP-сравнение + тай-брейк).

---

## 6. Тест-план (N3: гейт = нет НОВЫХ падений против базы)

**Registry:** `normalize_mission_name("purge_the_enemy")=="annihilation"`; board 40×60; `coordsOfOM` длиной 1 (фантом); `mission_uses_objectives("annihilation") is False`; `mission_scoring_mode=="kill_points"`.
**Scoring/win:** command phase в annihilation не меняет KP сверх пересчёта и не даёт objective-VP; уничтоженный enemy unit → `modelKP+1` ровно один раз (идемпотентность пересчёта); turn_limit `modelKP>enemyKP` → winner=model; равные KP + `tiebreak="none"` → draw; равные KP + `destroyed_hp` различается → winner по hp; wipeout enemy → winner=model; оба wipeout → KP-сравнение.
**Reward profiles:** `configure_for_mission("only_war")` — objective-константы на месте (не нули); `configure_for_mission("annihilation")` — objective/VP-shaping = 0, `ANNIHILATION_TIEBREAK_MODE=="destroyed_hp"`; `active_profile_name()` корректно; **drift-guard** проходит; фикстура сбрасывает профиль.
**Regression:** существующие Only War тесты — без изменения поведения; smoke train/eval init с `MISSION_NAME=annihilation` создаёт env (1 фантом-точка) без падений; gating не сломал Only War shaping.
**Команда:** `pytest tests/engine tests/train -q` + точечно затронутые в `tests/models`. Сверка счётчика фейлов с базовым коммитом.

---

## 7. Декомпозиция для дирижёра (work-packages)

Порядок: WP1 → (WP2, WP3 параллельно) → WP4 → WP5 → (WP6, WP7 параллельно). Каждый WP — TDD (тест до кода).

| WP | Что | Файлы | Интерфейс/выход | Приёмка | Зависит |
|----|-----|-------|-----------------|---------|---------|
| **WP1** | Registry-запись `annihilation` + хелперы + `mission_key/flags` в layout | `core/engine/mission.py` | `mission_scoring_mode/uses_objectives/is_annihilation_mission`; `env.mission_key` | unit-тесты registry (§6) зелёные | — |
| **WP2** | KP-tracking: снапшоты на reset + `recompute_kill_points` + `_destroyed_hp` | `core/envs/warhamEnv.py`, `core/engine/mission.py` | `env.modelKP/enemyKP`, destroyed-sets, `_start_*_unit_wounds` | тесты идемпотентности/однократности KP | WP1 |
| **WP3** | Reward split: `_onlywar.py` (копия), `_annihilation.py` (full + зануление + новые ключи), фасад `reward_config.py` + `configure_for_mission` | `reward_config.py`, `reward_config_onlywar.py`, `reward_config_annihilation.py` | фасад через `__getattr__`; `configure_for_mission/active_profile_name` | profile-тесты + drift-guard; heur-overrides не сломаны | — |
| **WP4** | Scoring/win-condition диспетчеры | `core/engine/mission.py` | разветвление `score_end_of_command_phase`/`check_end_of_battle` | scoring/win тесты (§6) | WP1, WP2 |
| **WP5** | Env-gating objective-shaping + `info`-поля + вызовы `configure_for_mission` в train/eval/play/worker-entry | `core/envs/warhamEnv.py`, `train.py`, `eval.py`, `play.py`/`game_controller`, worker entry-точки | objective-блоки под `mission_uses_objectives(self)` | regression Only War + smoke annihilation init | WP3, WP4 |
| **WP6** | Логи annihilation (layout/command/KP-grant/turn_limit) | `core/engine/mission.py`, `core/envs/warhamEnv.py` | новые лог-строки `[MISSION][Annihilation]` | лог содержит причину draw/winner | WP4 |
| **WP7** | Qt GUI/QML/Viewer (опция миссии, мета-текст, скрытие маркера) | `app/gui_qt/*`, `app/viewer/*` | `annihilation` в `missionOptions`, динамический мета-блок | визуальный smoke (без скриншотов) | WP1 |

---

## 8. Acceptance criteria (definition of done)
1. Партия `MISSION_NAME=annihilation` доигрывается без крашей; obs-размер = как у Only War (фантом-точка).
2. Победитель определяется по KP; равные KP разрешаются `destroyed_hp`; чистая ничья — только при равенстве и KP, и hp.
3. Objective-shaping в annihilation полностью выключен; combat-shaping активен.
4. `only_war` поведение не изменилось (regression-тесты).
5. Reward-профили: два самодостаточных файла + фасад; drift-guard зелёный; heur-calibration работает.
6. Логи объясняют каждый KP-grant и исход партии (причина draw/winner, tiebreak).
7. Нет новых падений `tests/engine tests/train` против базового коммита.

---

## 9. Вне scope / отложено
- **Тюнинг annihilation-наград** (kill-focused weights) — отдельная задача после рабочей логики (reward v1 = baseline-копия с занулённым objective-shaping).
- Режимы тай-брейка `remaining_hp` и VP-margin-primary — ключи заложены, логика — по запросу.
- Свой террейн/доска/деплой для annihilation (v1 = как Only War).
- Совместимость старых Only War моделей при будущем переходе на «obs без точек» (сейчас фантом сохраняет совместимость).

## 10. Риски
- **R1 (gating-полнота):** пропустить objective-блок в env → краш на фантоме маловероятен (точка есть), но возможна objective-награда в annihilation. Митигатор: grep всех objective-reward веток + regression.
- **R2 (multi-process профиль):** воркер не вызвал `configure_for_mission` → читает дефолт (only_war) reward. Митигатор: вызов в каждой entry-точке + guard-лог `[REWARD][PROFILE] active=...`.
- **R3 (KP на partial wipeout):** юнит «ожил» (health назад) — в движке не происходит; пересчёт из состояния всё равно идемпотентен.

## 11. Code map (референсы)
- Реестр/scoring/win: [`core/engine/mission.py`](../../../core/engine/mission.py) (`MISSION_REGISTRY` ~197, `score_end_of_command_phase` ~1182, `check_end_of_battle` ~1239, `apply_mission_layout` ~272).
- Env: [`core/envs/warhamEnv.py`](../../../core/envs/warhamEnv.py) (health init 1152/1172, obs-size 1189/1192, `refresh_objective_control` 7606, необгороженные `min(coordsOfOM)` 2293/2301/2302, `_get_observation` 8927).
- Reward: [`reward_config.py`](../../../reward_config.py) (objective/VP ключи 17–53, anti-draw 202–219, heur-calibration 348–392).
