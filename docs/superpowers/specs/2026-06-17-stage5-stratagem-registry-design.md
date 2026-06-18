# Stage 5 — Stratagem Registry (data-only) — Design

**Дата:** 2026-06-17
**Ветка:** `feat/phase-decision-windows`
**Контекст:** продолжение слоя `core/engine/phases/` (Stage 1–3 готовы: типы окон, `ActionOptionGenerator`, `LegacyActionCompiler`). Архитектурный отчёт — корень беседы; план Stage 1–3 — `docs/superpowers/plans/2026-06-17-phase-decision-windows.md`.

## Цель

Дать **типизированный справочник стратагем** (data-only) и **read-only движок легальности**, который из состояния `env` отвечает «какие стратагемы доступны в этом окне» — как обычные `ActionOption(kind=USE_STRATAGEM)`. Это фундамент для Stage 6 (исполнение CP через слой). **Ноль изменений поведения** `env.step`, snapshot/restore, обучения.

## Не-цели (явно вне Stage 5)

- Исполнение/`apply` стратагем, списание CP через слой — **Stage 6**.
- `StratagemState` (used_*, active_buffs) и его попадание в snapshot/restore — **Stage 6**.
- Превращение реакций (Overwatch/Smokescreen/Heroic) в реальные окна-прерывания, которые решает агент — **Stage 6/7** (сейчас они авто-срабатывают в движке и в плоском контракте не выражаются).
- Внешний конфиг стратагем (`unitData.json`/JSON) — отложено (YAGNI): 4 стратагемы это core-правила, не свойства юнитов.

## Глобальные ограничения

- Платформа Windows; Python 3.12+; тесты — `python -m pytest`; ruff `py312`, line-length 120, `select=["E","F","I","UP","B"]`, `StrEnum` вместо `(str, Enum)` (UP042).
- Язык докстрингов/сообщений — русский.
- `core/engine/*` не импортирует `core/models/*`.
- **Инвариант:** `core/envs/warhamEnv.py` не модифицируется в Stage 5. Движок легальности только читает env (`modelCP`/`enemyCP`, `unit_health`/`enemy_health`, `_unit_has_keyword`), ничего не мутирует.
- Источник истины по легальности — слой `core/engine/phases/`; описания в реестре строго соответствуют текущей логике движка.

## Соответствие текущему коду (на чём основан реестр)

- **Insane Bravery** — командная фаза, триггер «провален Battle-shock», 1 CP, цель = свой юнит. Код: `warhamEnv.py:4332-4345` (`action["use_cp"]==1 and action["cp_on"]==i`). Единственная агент-управляемая → имеет рабочий `legacy_patch`.
- **Overwatch** — реакция «вражеский юнит закончил движение», 1 CP, стрелок eligible (жив, не в ближнем бою, есть оружие, цель в дальности), попадания на 6+. Код: `_collect_overwatch_candidates` `warhamEnv.py:3972`, `_resolve_overwatch` `warhamEnv.py:4000-4132`.
- **Smokescreen** — реакция «выбран целью стрельбы», 1 CP, требует keyword SMOKE, эффект benefit of cover. Код: `_maybe_use_smokescreen` `warhamEnv.py:3922-3970`, `_unit_has_smoke` `warhamEnv.py:3919`.
- **Heroic Intervention** — реакция «после успешного charge врага», eligible = юниты защитника в 6", 1 CP. Код: `_resolve_heroic_intervention` `warhamEnv.py:4134`.
- Проверка keyword: `_unit_has_keyword(unit_data, keyword)` (регистронезависимый подстрочный поиск), `warhamEnv.py:3895-3920`.

## Архитектура

Новый модуль `core/engine/phases/stratagems.py`. Никакой логики исполнения — только описания и чистые функции легальности.

### Перечисления

```
class Trigger(StrEnum):
    BATTLE_SHOCK_FAILED = "battle_shock_failed"
    TARGETED_BY_SHOOTING = "targeted_by_shooting"
    ENEMY_ENDED_MOVE = "enemy_ended_move"
    ENEMY_CHARGED_IN = "enemy_charged_in"

class UsageLimit(StrEnum):
    PER_PHASE = "per_phase"
    PER_TURN = "per_turn"
    PER_BATTLE = "per_battle"
    UNLIMITED = "unlimited"
```

### StratagemDef (dataclass, frozen)

```
@dataclass(frozen=True)
class StratagemDef:
    id: str
    name_ru: str
    cp_cost: int
    phases: tuple[Phase, ...]      # в каких фазах применима
    timing: Timing                 # MAIN | REACTION
    trigger: Trigger
    scope: str                     # "self_unit" | "reacting_unit" | "enemy_unit"
    keyword_req: tuple[str, ...]   # требуемые keyword (lower-case), напр. ("smoke",)
    usage_limit: UsageLimit
    effect_id: str                 # ссылка на будущий обработчик-эффект (Stage 6)
```

Поля `tuple`, dataclass `frozen=True` → хешируемо и неизменяемо (реестр-константа).

### REGISTRY и лукапы

- `REGISTRY: tuple[StratagemDef, ...]` — 4 описания (insane_bravery, overwatch, smokescreen, heroic_intervention) по таблице соответствия выше.
- `by_id(stratagem_id: str) -> StratagemDef` — поиск, KeyError с понятным RU-сообщением если нет.
- `for_phase(phase: Phase) -> list[StratagemDef]`.
- `for_trigger(trigger: Trigger) -> list[StratagemDef]`.

### Движок легальности (read-only)

```
def legal_stratagem_options(
    env, side: str, *,
    phase: Phase,
    trigger: Trigger,
    candidate_unit_idxs: list[int] | None = None,   # юниты, к которым стратагема могла бы привязаться
) -> list[ActionOption]
```

Логика (чистое чтение env). `scope` — описательное поле (кладётся в `meta`), перечисление кандидатов единообразное:
1. `defs = [d for d in for_trigger(trigger) if phase in d.phases]`.
2. CP стороны: `cp = env.modelCP if side=="model" else env.enemyCP` (через `_unwrap`).
3. Для каждого `d`: если `cp < d.cp_cost` → пропустить (стратагема не предлагается).
4. Юниты-кандидаты = `candidate_unit_idxs` (если `None` → пусто, нечего предлагать), оставить только живых (`health[i] > 0`) и прошедших фильтр `keyword_req` (все kw через `env._unit_has_keyword(unit_data, kw)`; пустой `keyword_req` → фильтр пропускается).
5. На каждого оставшегося юнита `i` — одна `ActionOption(kind=USE_STRATAGEM, unit_idx=i, meta={"stratagem_id": d.id, "cp_cost": d.cp_cost, "timing": d.timing, "scope": d.scope}, legacy_patch=<см. ниже>)`.

**legacy_patch:**
- `insane_bravery`: `{"use_cp": 1, "cp_on": i}` (компилируется в текущий `env.step`).
- реакции (`overwatch`/`smokescreen`/`heroic_intervention`): `{}` — в плоском контракте не выражаются (движок их обрабатывает авто). Это информационные опции до Stage 6/7. Фиксируется тестом.

### Интеграция с генератором

`command_window` (в `option_generator.py`) перестаёт инлайнить Insane Bravery: вместо ручного цикла зовёт
`legal_stratagem_options(env, side, phase=Phase.COMMAND, trigger=Trigger.BATTLE_SHOCK_FAILED, candidate_unit_idxs=alive)`
и кладёт результат в `options` после `PASS`. Выход обязан быть **идентичен** прежнему (PASS + по одному USE_STRATAGEM на живого с `legacy_patch={"use_cp":1,"cp_on":i}` при CP≥1).

Реакционные стратагемы в Stage 5 в окна не подключаются (нет reaction-окон до Stage 6/7) — только доступны через `legal_stratagem_options`/реестр и покрыты тестами легальности.

## Поток данных

`env` (только чтение: CP, health, keywords) → `legal_stratagem_options` → `list[ActionOption]`. Мутаций нет. `command_window`/`generate_windows` продолжают работать как раньше, просто Bravery-опции теперь из реестра.

## Обработка ошибок

- `by_id` с неизвестным id → `KeyError` с сообщением «нет стратагемы id=… ; где: stratagems.by_id; что делать: проверить REGISTRY/опечатку».
- `legal_stratagem_options` при отсутствии нужных входов (scope требует юнита, а `candidate_unit_idxs is None`) → возвращает пустой список (не исключение): «нет кандидатов» — нормальная ситуация.

## Тест-план

Файл `tests/engine/phases/test_stratagems.py`:
1. **registry integrity** — ровно 4 дефа; id уникальны; `cp_cost>=1`; `by_id` находит каждый; `for_phase(COMMAND)` содержит `insane_bravery`; `for_trigger(TARGETED_BY_SHOOTING)` содержит `smokescreen`.
2. **command bravery legality** — при `modelCP=0` опций USE_STRATAGEM нет; при `modelCP>=1` — по одной на каждого живого, `legacy_patch=={"use_cp":1,"cp_on":i}`, `meta["stratagem_id"]=="insane_bravery"`.
3. **smokescreen legality == env** — юнит с keyword SMOKE и `cp>=1` → опция есть; без SMOKE → нет; с SMOKE но `cp=0` → нет. (Сверяется с `env._unit_has_smoke`.) Хелпер строит юнит с/без SMOKE через KEYWORDS.
4. **reaction legacy_patch empty** — для overwatch/smokescreen/heroic возвращаемые опции имеют `legacy_patch == {}` (не выражаются в плоском контракте).
5. **cp gate generic** — для каждого реакционного дефа при `cp=0` опций нет.

Файл `tests/engine/phases/test_option_generator.py` (дополнить):
6. **command_window unchanged after refactor** — при `modelCP=2` и 2 живых юнитах окно содержит ровно `[PASS, USE_STRATAGEM(cp_on=0), USE_STRATAGEM(cp_on=1)]` с прежними `legacy_patch`; при `modelCP=0` — только `[PASS]`.

Регрессия:
7. Существующий `tests/engine/phases/test_no_behavior_change.py` (инвариант компилятора) остаётся зелёным.
8. Смоук движка (`test_warham_env_snapshot_restore.py`, `test_shoot_targets_contract_regression.py`) — зелёный (env не тронут).

## Риски

- **Рассинхрон реестра с движком** (например, забыли keyword) — митигейт: тест 3 сверяет smokescreen-легальность напрямую с `env._unit_has_smoke`.
- **Случайное изменение поведения `command_window`** — митигейт: тест 6 фиксирует точный состав опций до/после рефактора.
- **Соблазн начать исполнение** — явно вне scope; `legacy_patch={}` у реакций не даёт им «протечь» в `env.step`.
