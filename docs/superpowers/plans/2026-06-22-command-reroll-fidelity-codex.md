# Command Re-roll Fidelity — План для исполнителя (GPT/Codex)

> **Кто исполняет:** агент-исполнитель (GPT/Codex). **Кто ревьюит:** Claude (после каждого этапа по git-диффу).
> **Это исполняемый артефакт.** Design-обоснование и разбор расхождений с правилом — в соседнем файле
> `docs/superpowers/plans/2026-06-22-command-reroll-fidelity.md` (читать для контекста, не обязательно для исполнения).

**Цель:** привести core-стратагему **Command Re-roll** от fight-only/wound-only приближения к правилу
Wahapedia 10ed (реакция в любой фазе на применимый бросок), поэтапно.

---

## 0. Как работать (обязательно прочитать перед стартом)

### Конвенции проекта (источник правды — `AGENTS.md`)
- **Язык:** все комментарии в коде, тексты логов и сообщения об ошибках — **русский**. Формат ошибки: *что случилось + где (файл/функция) + что делать дальше*.
- **Платформа — Windows.** Команды ниже даны для запуска тестов/линтера/git и кроссплатформенны.
- **НЕ редактировать руками** файлы `runtime/logs/LOGS_FOR_AGENTS_*.md` и `runtime/state/*remote_is*` — они защищены и правятся только через код логирования.
- **В коммит — только релевантный код.** Не коммить runtime-логи, временные файлы, `artifacts/`.
- **README устарел** — сверяйся с актуальным кодом, а не с README.

### Линтер (заменяет автоматический hook, которого у тебя нет)
После правки любого `.py` прогоняй вручную:
```
ruff check --fix <изменённый_файл.py>
```
Конфиг — `ruff.toml`. `ruff` ставится из `requirements_windows.txt`.
**Важно:** ruff срезает временно-неиспользуемые импорты — добавляй импорт вместе с его использованием в том же шаге, иначе он удалится.

### Запуск тестов
```
pytest <путь>::<тест> -v        # один тест
pytest tests/engine/phases/ -v  # каталог
```

### Дисциплина исполнения (TDD)
Каждая задача (`Task N`) — это цикл: **падающий тест → убедиться, что падает → минимальная реализация → тест проходит → ruff → коммит**.
Шаг = одно действие. Не объединяй реализацию нескольких задач в один коммит.

### Чекпойнты ревью (КРИТИЧНО)
- **Коммить каждую задачу отдельно** (атомарные диффы для ревью).
- **В КОНЦЕ КАЖДОГО ЭТАПА — ОСТАНОВИСЬ.** Не начинай следующий этап. Напиши краткий отчёт:
  «Этап N завершён, коммиты: <хэши>, все тесты зелёные: <вывод pytest>». Дождись ревью Claude и явного «продолжай».
- Если тест или допущение в плане противоречит реальному коду — **не выдумывай**: остановись, опиши расхождение (файл/строка/что не сходится) и спроси.

### Правила коммитов
- НЕ делать `push`/PR без отдельной просьбы. Только локальные коммиты.
- Сообщения коммитов — на русском, в формате ниже (тип в скобках указан в каждой задаче).
- Перед коммитом убедись, что в индексе только релевантные файлы (`git status` → `git add <конкретные пути>`).

---

## 1. Глобальные ограничения задачи (зашиты заказчиком)

- **(1) Выбор кости — всегда худшая проваленная.** Никакого выбора игроком, никакого «fast dice rolling». Среди костей ниже порога перебрасываем кость с **наименьшим** значением.
- **(2) Лимит Command Re-roll — `UNLIMITED`** в реестре + ограничение «один бросок/одна кость = один реролл» обеспечивается флагом `consumed` и инвариантом roll-context. Естественный лимит — стоимость в CP (1 CP за реролл).
- **(3) Desperate Escape / Hazardous** в движке **не реализованы как механики** (проверено: `desperate` = только эвристика `desperate_push`; `Hazardous` — нет в `core/envs/warhamEnv.py`). Command Re-roll к ним **не применяется** (Task 12 — заглушка-документация). Сами механики — вне области этого плана.
- **(4) Charge** бросается как `dice(num=2)` и схлопывается в `sum` локально (`core/envs/warhamEnv.py:6494-6495`, `:6658`, `:6854`). Пара костей доступна только в момент броска; переброс должен перебрасывать **обе** кости (multi-dice rule).
- **НЕ менять механику `usage_limit`** для других стратагем (Insane Bravery=PER_BATTLE, Overwatch=PER_TURN и т.д.). Меняется только запись Command Re-roll.
- **Правило-источник:** Command Re-roll = 1 CP, любая фаза, реакция после броска, реролл одного roll/test/save; «кость нельзя перебросить более одного раза»; multi-dice перебрасывается целиком.

---

## 2. Карта файлов

| Файл | Что меняем | Этапы |
|------|-----------|-------|
| `core/engine/utils.py` | `attack()`, `_normalize_effects`, хелпер выбора кости, `reroll_decider`-hook | 1, 2, 3 |
| `core/engine/phases/stratagems.py` | реестр Command Re-roll, `legal_stratagem_options`, лимит | 1, 3 |
| `core/engine/phases/stratagem_engine.py` | payload эффекта (под-тип), потребление | 1 |
| `core/engine/phases/option_generator.py` | опции hit/wound, reaction-окна | 1, 3 |
| `core/envs/warhamEnv.py` | `_fight_effects_for_attacker`, маппинг, charge/advance, decider, очистка | 1, 2, 3 |
| `core/models/reaction_value_policy.py` + bridges | value-policy → hook | 4 |
| `tests/engine/test_attack_effects.py` | low-level | 1, 2, 3 |
| `tests/engine/phases/test_command_reroll.py` | стратагема e2e | 1, 3 |
| `tests/engine/phases/test_stratagem_engine.py` | payload | 1 |
| `tests/engine/phases/test_roll_context.py` (новый) | hook, «не дважды», save | 2 |
| `tests/engine/phases/test_command_reroll_phases.py` (новый) | advance/charge/shooting | 3 |

---

# ЭТАП 1 — hit+wound ре-ролл в Fight (attacker-side), worst-failed, потребление

> Save отложен на этап 2 (save-бросок делает защитник — атрибутируем его через roll-context).

### Task 1: Хелпер худшей кости + worst-failed для `reroll_wounds="one"`

**Files:** Modify `core/engine/utils.py`; Test `tests/engine/test_attack_effects.py`.

- [ ] **Step 1 — падающий тест.** В `tests/engine/test_attack_effects.py` добавить:
```python
def test_worst_failed_index_picks_lowest_failure():
    import numpy as np
    from core.engine.utils import _worst_failed_index
    assert _worst_failed_index(np.array([3, 5, 2, 6]), 4) == 2
    assert _worst_failed_index(np.array([4, 5, 6]), 4) is None


def test_reroll_wounds_one_rerolls_worst_failure():
    weapon = _ranged_weapon(S=4, Attacks=2)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    one, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"reroll_wounds": "one"},
                    roller=StubRoller(hit=[5, 5], wound=[2, 3, 6]))
    assert float(sum(one)) == 1.0
```
- [ ] **Step 2 — убедиться, что падает.** Run: `pytest tests/engine/test_attack_effects.py::test_worst_failed_index_picks_lowest_failure -v` → FAIL (`cannot import name '_worst_failed_index'`).
- [ ] **Step 3 — реализация.** В `core/engine/utils.py` рядом с `_normalize_effects` добавить:
```python
def _worst_failed_index(dice, threshold):
    """Индекс наименьшей кости среди проваленных (< threshold); None если провалов нет.

    Для Command Re-roll реролим всегда ХУДШУЮ проваленную кость.
    """
    worst_idx = None
    worst_val = None
    for idx, d in enumerate(dice):
        d = int(d)
        if d < int(threshold) and (worst_val is None or d < worst_val):
            worst_val = d
            worst_idx = idx
    return worst_idx
```
В wound-проходе (`core/engine/utils.py:534-548`) заменить блок выбора так, чтобы `"one"` брал худшую кость:
```python
            if eff["reroll_wounds"]:
                if eff["reroll_wounds"] == "one":
                    wi = _worst_failed_index(wound_rolls, wt)
                    need = [wi] if wi is not None else []
                else:
                    need = []
                    for idx, w in enumerate(wound_rolls):
                        w = int(w)
                        if eff["reroll_wounds"] == "ones" and w == 1:
                            need.append(idx)
                        elif eff["reroll_wounds"] == "all" and w < wt:
                            need.append(idx)
                if need:
                    new = _roll_with_stage(num=len(need), stage="wound")
                    new = np.array([new] if isinstance(new, int) else list(new), dtype=int)
                    for j, idx in enumerate(need):
                        wound_rolls[idx] = int(new[j])
```
- [ ] **Step 4 — тесты зелёные.** Run: `pytest tests/engine/test_attack_effects.py -v` → PASS. Затем `ruff check --fix core/engine/utils.py`.
- [ ] **Step 5 — коммит.**
```
git add core/engine/utils.py tests/engine/test_attack_effects.py
git commit -m "feat(engine): worst-failed выбор кости для reroll_wounds=one"
```

---

### Task 2: `reroll_hits="one"` (worst-failed)

**Files:** Modify `core/engine/utils.py` (`_normalize_effects` `:341-342`, hit-проход `:483-495`); Test `tests/engine/test_attack_effects.py`.
**Зависит от:** Task 1 (`_worst_failed_index`).

- [ ] **Step 1 — падающий тест.**
```python
def test_reroll_hits_one_rerolls_worst_failure():
    weapon = _ranged_weapon(S=4, Attacks=2)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    one, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"reroll_hits": "one"},
                    roller=StubRoller(hit=[2, 3, 6], wound=[6]))
    assert float(sum(one)) == 1.0


def test_normalize_effects_reroll_hits_one_allowed():
    assert _normalize_effects({"reroll_hits": "one"})["reroll_hits"] == "one"
```
- [ ] **Step 2 — падает.** Run: `pytest tests/engine/test_attack_effects.py::test_normalize_effects_reroll_hits_one_allowed -v` → FAIL (`None != 'one'`).
- [ ] **Step 3 — реализация.** В `_normalize_effects` (`:341-342`):
```python
        rh = effects.get("reroll_hits")
        out["reroll_hits"] = rh if rh in ("ones", "all", "one") else None
```
В hit-проходе (`:483-495`) добавить ветку `"one"` (порог = `bs`, крит-6 не провал):
```python
    if eff["reroll_hits"]:
        if eff["reroll_hits"] == "one":
            wi = _worst_failed_index(rolls, bs)
            need = [wi] if wi is not None else []
        else:
            need = []
            for idx, r in enumerate(rolls):
                r = int(r)
                if eff["reroll_hits"] == "ones" and r == 1:
                    need.append(idx)
                elif eff["reroll_hits"] == "all" and r != 6 and r < bs:
                    need.append(idx)
        if need:
            new = _roll_with_stage(num=len(need), stage="hit")
            new = np.array([new] if isinstance(new, int) else list(new), dtype=int)
            for j, idx in enumerate(need):
                rolls[idx] = int(new[j])
```
- [ ] **Step 4 — зелёные.** Run: `pytest tests/engine/test_attack_effects.py -v` → PASS. `ruff check --fix core/engine/utils.py`.
- [ ] **Step 5 — коммит.**
```
git add core/engine/utils.py tests/engine/test_attack_effects.py
git commit -m "feat(engine): reroll_hits=one (worst-failed) в attack()"
```

---

### Task 3: Под-тип ре-ролла (hit|wound) в стратагеме + потребление эффекта

**Files:** Modify `core/engine/phases/stratagems.py`, `core/engine/phases/stratagem_engine.py`, `core/envs/warhamEnv.py` (`_fight_effects_for_attacker` `:2341-2342`); Test `tests/engine/phases/test_command_reroll.py`, `tests/engine/phases/test_stratagem_engine.py`.
**Зависит от:** Tasks 1–2.

- [ ] **Step 1 — падающие тесты.** В `tests/engine/phases/test_stratagem_engine.py` заменить `test_command_reroll_payload_is_single` на:
```python
def test_command_reroll_payload_records_roll_subtype():
    env = build_env()
    env.modelCP = 2
    env.stratagem_used = []
    env.active_stratagem_effects = []
    stratagem_engine.apply(env, "model", "command_reroll", 0, phase="fight", reroll_roll="hit")
    rec = [r for r in env.active_stratagem_effects if r["effect_id"] == "command_reroll"][0]
    assert rec["reroll_roll"] == "hit"
    assert rec["consumed"] is False
```
В `tests/engine/phases/test_command_reroll.py` добавить:
```python
def test_fight_effect_consumed_after_first_read():
    env = build_env()
    env.battle_round = 1
    env.active_stratagem_effects = [{
        "side": "model", "unit_idx": 0, "round": 1, "phase": "fight",
        "effect_id": "command_reroll", "reroll_roll": "wound", "consumed": False,
    }]
    first = env._fight_effects_for_attacker("model", 0)
    assert first == {"reroll_wounds": "one"}
    second = env._fight_effects_for_attacker("model", 0)
    assert second is None
```
- [ ] **Step 2 — падают.** Run: `pytest tests/engine/phases/test_stratagem_engine.py::test_command_reroll_payload_records_roll_subtype tests/engine/phases/test_command_reroll.py::test_fight_effect_consumed_after_first_read -v` → FAIL.
- [ ] **Step 3 — реализация.**
  - `stratagem_engine.py::apply` — добавить параметр:
    ```python
    def apply(env, side: str, stratagem_id: str, unit_idx: int | None = None,
              phase: str | None = None, *, reroll_roll: str = "wound") -> dict:
    ```
    Заменить запись эффекта Command Re-roll (`core/engine/phases/stratagem_engine.py:43-60`): hungry_void оставить как есть, а для command_reroll писать:
    ```python
    if d.effect_id == "command_reroll" and unit_idx is not None:
        active = getattr(e, "active_stratagem_effects", None)
        if active is None:
            active = []
            e.active_stratagem_effects = active
        roll = reroll_roll if reroll_roll in ("hit", "wound") else "wound"
        active.append({
            "side": str(side), "unit_idx": int(unit_idx),
            "round": int(getattr(e, "battle_round", 1)),
            "phase": str(phase or getattr(e, "phase", "fight") or "fight"),
            "effect_id": "command_reroll", "reroll_roll": roll, "consumed": False,
        })
    ```
  - В реестре (`core/engine/phases/stratagems.py:142-153`) сменить `effect_id="command_reroll_wounds"` → `effect_id="command_reroll"`.
  - `warhamEnv.py::_fight_effects_for_attacker` (`:2341-2342`) — потребление:
    ```python
            elif rec.get("effect_id") == "command_reroll" and not rec.get("consumed", False):
                roll = str(rec.get("reroll_roll", "wound"))
                effects[f"reroll_{roll}"] = "one"
                rec["consumed"] = True
    ```
  - Обновить существующие тесты под новую форму: `test_registry_has_command_reroll` → `assert d.effect_id == "command_reroll"`; `test_apply_command_reroll_writes_reroll_effect` → проверять запись `effect_id == "command_reroll"` и `reroll_roll == "wound"`; `test_fight_effects_for_attacker_returns_reroll_wounds` — обновить запись на `effect_id="command_reroll"`, `reroll_roll="wound"`, `consumed=False` и ожидать `{"reroll_wounds": "one"}`.
- [ ] **Step 4 — зелёные.** Run: `pytest tests/engine/phases/test_command_reroll.py tests/engine/phases/test_stratagem_engine.py -v` → PASS. `ruff check --fix` по трём изменённым `.py`.
- [ ] **Step 5 — коммит.**
```
git add core/engine/phases/stratagems.py core/engine/phases/stratagem_engine.py core/envs/warhamEnv.py tests/engine/phases/test_command_reroll.py tests/engine/phases/test_stratagem_engine.py
git commit -m "feat(strat): Command Re-roll выбор hit|wound + потребление эффекта"
```

---

### Task 4: Опции hit/wound в fight-окне + под-тип в pending-plan

**Files:** Modify `core/engine/phases/stratagems.py::legal_stratagem_options` (`:271-285`), `core/envs/warhamEnv.py::_apply_pending_fight_stratagem_plan` (`:2353-2382`); Test `tests/engine/phases/test_command_reroll.py`.
**Зависит от:** Task 3.

- [ ] **Step 1 — падающий тест.**
```python
def test_fight_window_offers_command_reroll_hit_and_wound():
    env = build_env()
    env.modelCP = 1
    opts = fight_stratagem_options_for_unit(env, "model", 0)
    rolls = {o.param.get("reroll_roll") for o in opts
             if o.kind is ActionKind.USE_STRATAGEM and o.meta.get("stratagem_id") == "command_reroll"}
    assert rolls == {"hit", "wound"}
```
- [ ] **Step 2 — падает.** Run: `pytest tests/engine/phases/test_command_reroll.py::test_fight_window_offers_command_reroll_hit_and_wound -v` → FAIL.
- [ ] **Step 3 — реализация.** В `legal_stratagem_options` (внутри цикла по кандидатам, `:271-285`) добавить спец-ветку ПЕРЕД общим `options.append(...)`:
```python
            if d.id == "command_reroll":
                for roll in ("hit", "wound"):
                    options.append(ActionOption(
                        kind=ActionKind.USE_STRATAGEM, unit_idx=i,
                        param={"stratagem_id": d.id, "reroll_roll": roll},
                        legacy_patch={},
                        meta={"stratagem_id": d.id, "cp_cost": d.cp_cost,
                              "timing": d.timing, "scope": d.scope, "reroll_roll": roll},
                    ))
                continue
```
В `_apply_pending_fight_stratagem_plan` (`:2379-2382`, место вызова `_apply_stratagem`) распарсить под-тип из значения плана:
```python
                sid_raw = str(sid)
                if sid_raw.startswith("command_reroll:"):
                    _apply_stratagem(self, side, "command_reroll", ui, phase="fight",
                                     reroll_roll=sid_raw.split(":", 1)[1])
                else:
                    _apply_stratagem(self, side, sid_raw, ui, phase="fight")
```
- [ ] **Step 4 — зелёные.** Run: `pytest tests/engine/phases/test_command_reroll.py tests/engine/phases/test_obs_features.py -v` → PASS. `ruff check --fix` по двум `.py`.
- [ ] **Step 5 — коммит.**
```
git add core/engine/phases/stratagems.py core/envs/warhamEnv.py tests/engine/phases/test_command_reroll.py
git commit -m "feat(strat): fight-окно отдаёт Command Re-roll отдельно для hit/wound"
```

### ⛔ ЧЕКПОЙНТ — КОНЕЦ ЭТАПА 1
Прогони весь блок: `pytest tests/engine/ -v`. Напиши отчёт (коммиты + вывод pytest) и **жди ревью Claude**. Не начинай Этап 2.

---

# ЭТАП 2 — roll-context hook в attack() + save-attribution

### Task 5: `reroll_decider`-hook в attack()

**Files:** Modify `core/engine/utils.py::attack` (сигнатура `:366-367`, hit/wound/save проходы); Test `tests/engine/phases/test_roll_context.py` (новый).

**Контракт hook:** `attack(..., reroll_decider=None)`, где `reroll_decider: Callable[[str, np.ndarray, int], bool] | None`. Вызывается **после** бросков стадии `stage in {"hit","wound","save"}` с `(stage, dice_array, threshold)`. Возвращает `True` → движок перебрасывает ЕДИНСТВЕННУЮ худшую проваленную кость этой стадии один раз. Один вызов decider на стадию за атаку. Decider НЕ получает side/unit_idx (их связывает замыкание вызывающего — Task 7).

- [ ] **Step 1 — падающий тест.** Создать `tests/engine/phases/test_roll_context.py`:
```python
from core.engine.utils import attack
from tests.engine.test_attack_effects import StubRoller, _ranged_weapon, _ATT_DATA


def test_reroll_decider_rerolls_worst_failed_wound():
    weapon = _ranged_weapon(S=4, Attacks=2)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    calls = []

    def decider(stage, dice, threshold):
        calls.append(stage)
        return stage == "wound"

    dmg, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                    roller=StubRoller(hit=[5, 5], wound=[2, 3, 6]),
                    reroll_decider=decider)
    assert "wound" in calls
    assert float(sum(dmg)) == 1.0
```
- [ ] **Step 2 — падает.** Run: `pytest tests/engine/phases/test_roll_context.py::test_reroll_decider_rerolls_worst_failed_wound -v` → FAIL (`unexpected keyword argument 'reroll_decider'`).
- [ ] **Step 3 — реализация.** В сигнатуру `attack()` (`:366-367`) добавить `reroll_decider=None`. После `eff = _normalize_effects(effects)` добавить хелпер (использует множество уже-переброшенных — пригодится в Task 6, заведи `set` на стадию):
```python
    def _maybe_decider_reroll(stage, dice, threshold, rerolled):
        # Реактивный Command Re-roll-style hook: после броска стадии спросить decider,
        # реролить ли худшую проваленную кость (один раз, исключая уже переброшенные).
        if reroll_decider is None:
            return dice
        try:
            want = bool(reroll_decider(stage, dice, int(threshold)))
        except Exception:
            want = False
        if not want:
            return dice
        wi = None
        worst = None
        for idx, d in enumerate(dice):
            if idx in rerolled:
                continue
            d = int(d)
            if d < int(threshold) and (worst is None or d < worst):
                worst, wi = d, idx
        if wi is None:
            return dice
        new = _roll_with_stage(num=1, stage=stage)
        dice[wi] = int(new if isinstance(new, int) else list(new)[0])
        rerolled.add(wi)
        return dice
```
Вызвать после каждого effect-прохода со своим `set()`: hit (после `:495`, порог `bs`), wound (после wound-реролла, порог `wt`), save (после `:577`, порог `save_target`). Пример для wound:
```python
            wound_rerolled = set()
            # ... (existing effect-based reroll fills wound_rerolled — добавляется в Task 6)
            wound_rolls = _maybe_decider_reroll("wound", wound_rolls, wt, wound_rerolled)
```
(На этом шаге `set()` можно создавать пустым; наполнение из effect-прохода — в Task 6.)
- [ ] **Step 4 — зелёные.** Run: `pytest tests/engine/phases/test_roll_context.py tests/engine/test_attack_effects.py -v` → PASS (без decider поведение неизменно). `ruff check --fix core/engine/utils.py`.
- [ ] **Step 5 — коммит.**
```
git add core/engine/utils.py tests/engine/phases/test_roll_context.py
git commit -m "feat(engine): reroll_decider hook в attack() (worst-failed, per-stage)"
```

---

### Task 6: Инвариант «кость нельзя перебросить дважды»

**Files:** Modify `core/engine/utils.py::attack`; Test `tests/engine/phases/test_roll_context.py`.
**Зависит от:** Task 5.

- [ ] **Step 1 — падающий тест.**
```python
def test_die_not_rerolled_twice_effect_then_decider():
    weapon = _ranged_weapon(S=4, Attacks=2)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}

    def decider(stage, dice, threshold):
        return True

    # wound: [2,3]. effect "one" реролит худший (2)→[5]. decider не должен трогать уже-переброшенную;
    # реролит вторую failed (3)→[6]. Итог: 2 раны.
    dmg, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                    effects={"reroll_wounds": "one"},
                    roller=StubRoller(hit=[5, 5], wound=[2, 3, 5, 6]),
                    reroll_decider=decider)
    assert float(sum(dmg)) == 2.0
```
- [ ] **Step 2 — падает.** Run: `pytest tests/engine/phases/test_roll_context.py::test_die_not_rerolled_twice_effect_then_decider -v` → FAIL (без защиты decider реролит уже-переброшенную, итог неверный).
- [ ] **Step 3 — реализация.** В каждом effect-проходе (hit/wound/save) при записи переброшенного индекса добавлять его в соответствующий `*_rerolled` set, и передавать этот set в `_maybe_decider_reroll` (он уже исключает `rerolled`). Т.е. для wound:
```python
                for j, idx in enumerate(need):
                    wound_rolls[idx] = int(new[j])
                    wound_rerolled.add(idx)
```
Аналогично для hit (`hit_rerolled`) и save (`save_rerolled`).
- [ ] **Step 4 — зелёные.** Run: `pytest tests/engine/phases/test_roll_context.py tests/engine/test_attack_effects.py -v` → PASS. `ruff check --fix core/engine/utils.py`.
- [ ] **Step 5 — коммит.**
```
git add core/engine/utils.py tests/engine/phases/test_roll_context.py
git commit -m "feat(engine): инвариант одна кость = один реролл (effect+decider)"
```

---

### Task 7: Проброс decider из resolve_fight + side-attribution (attacker=hit/wound, defender=save)

**Files:** Modify `core/engine/phases/stratagem_engine.py` (whitelist под-типа), `core/envs/warhamEnv.py` (новый `_build_reroll_decider`; вызовы `attack()` `:7377-7396` и `:7464-7485`); Test `tests/engine/phases/test_roll_context.py`.
**Зависит от:** Tasks 5–6, Task 3.

- [ ] **Step 1 — падающий тест.**
```python
def test_defender_command_reroll_applies_to_save():
    import numpy as np
    from tests.engine.phases._helpers import build_env
    env = build_env()
    env.battle_round = 1
    env.active_stratagem_effects = [{
        "side": "enemy", "unit_idx": 0, "round": 1, "phase": "fight",
        "effect_id": "command_reroll", "reroll_roll": "save", "consumed": False,
    }]
    decider = env._build_reroll_decider("model", 0, "enemy", 0)
    assert decider("save", np.array([2]), 4) is True
    assert decider("hit", np.array([2]), 4) is False
```
- [ ] **Step 2 — падает.** Run: `pytest tests/engine/phases/test_roll_context.py::test_defender_command_reroll_applies_to_save -v` → FAIL (нет `_build_reroll_decider`).
- [ ] **Step 3 — реализация.**
  - В `stratagem_engine.apply` расширить whitelist под-типа: `roll = reroll_roll if reroll_roll in ("hit", "wound", "save") else "wound"`.
  - Добавить метод в `warhamEnv.py`:
    ```python
    def _build_reroll_decider(self, attacker_side, attacker_idx, defender_side, defender_idx):
        def _find(side, unit_idx, roll):
            for rec in list(getattr(self, "active_stratagem_effects", []) or []):
                if (rec.get("effect_id") == "command_reroll" and not rec.get("consumed", False)
                        and str(rec.get("phase", "")) == "fight"
                        and str(rec.get("side", "")) == str(side)
                        and int(rec.get("unit_idx", -1)) == int(unit_idx)
                        and str(rec.get("reroll_roll", "")) == roll
                        and int(rec.get("round", getattr(self, "battle_round", 1)))
                            == int(getattr(self, "battle_round", 1))):
                    return rec
            return None

        def decider(stage, dice, threshold):
            if stage in ("hit", "wound"):
                rec = _find(attacker_side, attacker_idx, stage)
            elif stage == "save":
                rec = _find(defender_side, defender_idx, "save")
            else:
                rec = None
            if rec is None:
                return False
            rec["consumed"] = True
            return True

        return decider
    ```
  - В `resolve_fight_phase` перед вызовами `attack()` построить `decider = self._build_reroll_decider(...)` (для model-attacker: `("model", att_idx, "enemy", def_idx)`; для enemy-attacker: `("enemy", att_idx, "model", def_idx)`) и передать `reroll_decider=decider` во все вызовы `attack(...)` обеих веток.
  - Hit/wound по-прежнему могут идти effect-путём (`_fight_effects_for_attacker`); инвариант Task 6 не даст двойного реролла.
- [ ] **Step 4 — зелёные.** Run: `pytest tests/engine/phases/test_roll_context.py tests/engine/phases/test_command_reroll.py -v` → PASS. `ruff check --fix` по двум `.py`.
- [ ] **Step 5 — коммит.**
```
git add core/engine/phases/stratagem_engine.py core/envs/warhamEnv.py tests/engine/phases/test_roll_context.py
git commit -m "feat(strat): save-реролл защитника через reroll_decider в fight"
```

### ⛔ ЧЕКПОЙНТ — КОНЕЦ ЭТАПА 2
`pytest tests/engine/ -v` → отчёт + **жди ревью Claude**. Этап 2 трогает боевой pipeline — ревью обязательно до Этапа 3.

---

# ЭТАП 3 — все фазы и броски

> Шаги «падающий тест» здесь пиши по образцу `tests/engine/phases/test_command_reroll.py::test_run_fight_command_reroll_spends_cp_and_applies`
> (seeded `random`/`numpy`, `env.simulation_mode()`, `phase_engine.run_*`). Тесты — в `tests/engine/phases/test_command_reroll_phases.py` (новый).

### Task 8: Command Re-roll в Shooting (hit/wound для стрелка, save для цели)
**Files:** Modify `core/envs/warhamEnv.py` (shooting-резолв — место вызова `attack(..., rangeOfComb="Ranged")`), `core/engine/phases/stratagems.py` (`phases` += `SHOOTING`), `core/engine/phases/option_generator.py` (shooting reaction-опции). Test `test_command_reroll_phases.py`.
- [ ] **Step 1** — падающий e2e тест: стрелок с активным `command_reroll/wound` реролит худший провальный wound в стрельбе.
- [ ] **Step 2** — Run: `pytest tests/engine/phases/test_command_reroll_phases.py -k shooting -v` → FAIL.
- [ ] **Step 3** — добавить `Phase.SHOOTING` в реестр Command Re-roll; добавить shooting reaction-опции в `option_generator` (по образцу `fight_stratagem_options_for_unit`); строить decider в shooting-резолве через `_build_reroll_decider` и передавать в `attack()`; вызвать `_clear_phase_stratagem_effects("shooting")` в конце shooting-фазы.
- [ ] **Step 4** — Run: `pytest tests/engine/phases/ -v` → PASS. `ruff check --fix`.
- [ ] **Step 5** — `git commit -m "feat(strat): Command Re-roll в Shooting phase (hit/wound/save)"`

### Task 8b: Damage- и Attacks-броски (gap из self-review)
**Files:** Modify `core/engine/utils.py` (добавить `stage="damage"` и `stage="attacks"` вызовы `_maybe_decider_reroll` в местах броска урона `_roll_damage_expr` и парсинга кол-ва атак). Test `test_roll_context.py`.
- [ ] **Step 1** — падающий тест: decider на `stage="damage"` перебрасывает худший бросок урона D6/D3.
- [ ] **Step 2** — FAIL.
- [ ] **Step 3** — провести `dice`-броски урона/атак через `_roll_with_stage` со стадиями `"damage"`/`"attacks"` и добавить `_maybe_decider_reroll` после них (своя `set()` на стадию). Расширить whitelist под-типа в `apply` до `("hit","wound","save","damage","attacks")`.
- [ ] **Step 4** — PASS. `ruff check --fix`.
- [ ] **Step 5** — `git commit -m "feat(engine): Command Re-roll на Damage/Attacks-броски"`

### Task 9: Command Re-roll на Advance (D6)
**Files:** Modify `core/envs/warhamEnv.py` (advance `:4986-5100` model, `:5249-5306` enemy; `model/enemy_advance_roll` `:1074-1075`), реестр (`phases` += `MOVEMENT`), `option_generator` (advance-reaction-окно). Test `test_command_reroll_phases.py`.
- [ ] **Step 1** — падающий тест: advance-бросок юнита с активным `command_reroll/advance` перебрасывается (seeded: первый низкий, реролл выше; проверить итоговый `model_advance_roll[i]`).
- [ ] **Step 2** — FAIL.
- [ ] **Step 3** — в момент записи `*_advance_roll[i]` проверить активный неиспользованный `command_reroll/advance` для юнита; если есть — перебросить `dice()` один раз, перезаписать, пометить `consumed=True`. Для одиночной кости «худшая» = сам бросок (перебрасываем безусловно при срабатывании). Добавить `Phase.MOVEMENT` в реестр + advance reaction-окно.
- [ ] **Step 4** — PASS. `ruff check --fix`.
- [ ] **Step 5** — `git commit -m "feat(strat): Command Re-roll на Advance-бросок"`

### Task 10: Command Re-roll на Charge (2D6, обе кости) + унификация charge-путей
**Files:** Modify `core/envs/warhamEnv.py::charge_phase` (три пути `:6494-6495`, `:6658`, `:6854`), реестр (`phases` += `CHARGE`), `option_generator`. Test `test_command_reroll_phases.py`.
- [ ] **Step 1** — падающий тест: юнит с `command_reroll/charge`, первый `dice(num=2)` — провал, реролл обеих → успех; проверить успех charge и что переброшены ОБЕ кости (seeded).
- [ ] **Step 2** — FAIL.
- [ ] **Step 3** — выделить хелпер `_charge_roll_with_reroll(side, unit_idx) -> (dice_vals, total)`; во всех трёх путях заменить `dice(num=2)`/`sum(...)` на него; в enemy-heur (`:6854`) перестать схлопывать сумму до реакции; внутри хелпера при активном `command_reroll/charge` перебросить `dice(num=2)` ЦЕЛИКОМ один раз. Добавить `Phase.CHARGE` в реестр + charge reaction-окно.
- [ ] **Step 4** — Run: `pytest tests/engine/ -v` (включая существующие charge-тесты) → PASS. `ruff check --fix`.
- [ ] **Step 5** — `git commit -m "feat(strat): Command Re-roll на Charge 2D6 (обе кости), унификация charge-путей"`

### Task 11: Лимит Command Re-roll → UNLIMITED
**Files:** Modify `core/engine/phases/stratagems.py:151`. Test `tests/engine/phases/test_usage_limit.py`, `test_command_reroll_phases.py`.
- [ ] **Step 1** — падающий тест: два разных броска в одной фазе → оба Command Re-roll применяются (CP 2→0), `usage_limit_reached` не блокирует.
- [ ] **Step 2** — FAIL (сейчас PER_PHASE блокирует второй).
- [ ] **Step 3** — сменить `usage_limit=UsageLimit.PER_PHASE` → `UsageLimit.UNLIMITED` для command_reroll. Механику `usage_limit_reached` НЕ менять (UNLIMITED уже возвращает False, `:212-213`). Лимит «один бросок = один реролл» держится на `consumed`+инварианте.
- [ ] **Step 4** — Run: `pytest tests/engine/phases/test_usage_limit.py tests/engine/phases/ -v` → PASS (лимиты Insane Bravery/Overwatch не затронуты). `ruff check --fix`.
- [ ] **Step 5** — `git commit -m "feat(strat): Command Re-roll лимит = UNLIMITED (per-roll вместо per-phase)"`

### Task 12: Desperate Escape / Hazardous — документировать как «вне области»
**Files:** Modify комментарий реестра `core/engine/phases/stratagems.py:136-141`.
- [ ] **Step 1** — в комментарии Command Re-roll зафиксировать: Desperate Escape/Hazardous-тесты в движке не моделируются (механики нет), Command Re-roll к ним не применяется; реализация самих механик — вне этого плана.
- [ ] **Step 2** — `ruff check --fix core/engine/phases/stratagems.py` (комментарий — ruff не тронет) и `git commit -m "docs(strat): Command Re-roll — Desperate Escape/Hazardous вне области (нет механики)"`

### ⛔ ЧЕКПОЙНТ — КОНЕЦ ЭТАПА 3
`pytest tests/engine/ -v` → отчёт + **жди ревью Claude**.

---

# ЭТАП 4 — AI / MCTS reaction-policy на hook

### Task 13: Подключить value-reaction-policy к reroll_decider
**Files:** Modify `core/models/reaction_value_policy.py` (`:16-36`), `core/envs/warhamEnv.py::_build_reroll_decider`, `core/models/dqn_stratagem_bridge.py` (`:66-98`), `core/models/ppo_stratagem_bridge.py`. Test `tests/models/test_eval_agent.py` (`:52-56`) + новый reaction-policy тест.
- [ ] **Step 1** — падающий тест: reaction-policy на ctx «бросок с провалами» → apply, «без провалов» → pass (мок value-сети). Обновить `test_eval_agent.py` под план с под-типом `command_reroll:hit`.
- [ ] **Step 2** — FAIL.
- [ ] **Step 3** — расширить ctx reaction-policy полями броска (`stage`, число провалов); в `_build_reroll_decider` при отсутствии предустановленной записи, наличии CP и сети — вызвать `env.reaction_policy(ctx)`; добавить heuristics-гейт «есть провалы и CP>0», чтобы не плодить reaction-вызовы. Обновить bridges: fight-plan учитывает под-тип hit/wound; реактивные save/charge/advance решает decider.
- [ ] **Step 4** — Run: `pytest tests/models/ tests/engine/ -v` → PASS + смоук eval (число reaction-вызовов в норме). `ruff check --fix`.
- [ ] **Step 5** — `git commit -m "feat(ai): reaction value-policy для Command Re-roll в точке броска"`

### ⛔ ЧЕКПОЙНТ — КОНЕЦ ЭТАПА 4
`pytest tests/ -v` → финальный отчёт + **жди финального ревью Claude**.

---

## 3. Сводка чекпойнтов для ревьюера (Claude)

| Этап | Что проверять в диффе |
|------|------------------------|
| 1 | worst-failed логика, форма записи `active_stratagem_effects`, потребление, обновлённые «approximation»-тесты |
| 2 | инвариант «не дважды», корректная side-attribution save→защитник, неизменность `attack()` без decider |
| 3 | charge перебрасывает ОБЕ кости, enemy-heur путь не схлопывает рано, лимит UNLIMITED не сломал другие стратагемы, очистка эффектов по фазам |
| 4 | отсутствие взрыва reaction-вызовов, корректность value-гейта, обновление bridges |

## 4. Стоп-сигналы (когда НЕ продолжать, а спрашивать)
- Реальный код не совпадает со строками/сигнатурами из плана (рефакторинг сдвинул номера) — опиши, где именно.
- Существующий тест начал падать и причина не очевидна — не «чини» подгонкой ассертов, сообщи.
- Нужен новый сторонний пакет — сперва согласуй (и внеси в `requirements_windows.txt`).
- Любая правка задела бы `runtime/logs/LOGS_FOR_AGENTS_*.md` или remote/pc2-конфиги — не трогай, сообщи.
