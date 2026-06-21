# Determine First Turn (второй roll-off) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Интегрировать шаг 10e «Determine First Turn» — второй roll-off после деплоя определяет, кто ходит первым; очередь хода берётся из его итога, а не из хардкода `["enemy","model"]`.

**Architecture:** Единый источник правды `env.first_turn_side` → `env.turn_order` в `reset()`. Общий хелпер `run_battle_round` прогоняет две половины раунда в порядке `turn_order`. Драйверы (eval/train/play, затем AZ/MuZero) резолвят `FIRST_TURN` и зовут хелпер. `step()/enemyTurn()/_advance_turn_order` не меняем — они уже корректны при инварианте «драйвер зовёт половины в порядке turn_order».

**Tech Stack:** Python 3.12+, PyTorch, Gymnasium, pytest. Платформа Windows.

**Спека:** [docs/superpowers/specs/2026-06-21-first-turn-rolloff-design.md](../specs/2026-06-21-first-turn-rolloff-design.md)

## Global Constraints

- Платформа: **Windows**; Python **3.12+**. Запуск тестов: `python -m pytest`.
- Язык логов/UI/ошибок — **русский**; ошибки в формате «что случилось + где (файл/функция) + что делать».
- Тесты — в `tests/engine/`, стиль `unittest`/`pytest` как в проекте. Без новых тяжёлых зависимостей.
- `FIRST_TURN` env: `roll` (**default**) | `model_first` | `enemy_first`. `enemy_first` = точная обратная совместимость.
- `roll_off_first_turn` возвращает победителя (`"model"|"enemy"`), который ходит **первым**.
- Не коммитить runtime-логи/артефакты (`runtime/logs/*`, `artifacts/metrics/*`). Перед коммитом крупного движкового диффа — субагент `engine-regression-reviewer`.
- Хук `ruff_fix.py` прогонит `ruff --fix` по изменённым `.py` — не оставлять неиспользуемых импортов.

---

# PHASE 1 — Ядро (env + хелпер + DQN/PPO/eval/play + регрессы)

---

### Task 1: `roll_off_first_turn` — второй roll-off

**Files:**
- Modify: `core/envs/warhamEnv.py` (рядом с `roll_off_attacker_defender`, после строки ~317)
- Test: `tests/engine/test_first_turn_rolloff.py` (create)

**Interfaces:**
- Produces: `roll_off_first_turn(manual_roll_allowed: bool = False, log_fn=None) -> str` — возвращает `"model"|"enemy"` (победитель = ходит первым). Использует модульные `auto_dice()` / `player_dice()`.

- [ ] **Step 1: Написать падающий тест**

```python
# tests/engine/test_first_turn_rolloff.py
import core.envs.warhamEnv as we


def test_first_turn_winner_goes_first(monkeypatch):
    # enemy=5 > model=2 → победитель enemy ходит первым
    monkeypatch.setattr(we, "auto_dice", lambda: 2)   # model
    seq = iter([5])                                    # enemy
    monkeypatch.setattr(we, "player_dice", lambda *a, **k: next(seq))
    monkeypatch.setenv("MANUAL_DICE", "1")
    assert we.roll_off_first_turn(manual_roll_allowed=True) == "enemy"


def test_first_turn_model_wins(monkeypatch):
    rolls = iter([6, 3])  # auto_dice: model=6, затем enemy(auto)=3
    monkeypatch.setattr(we, "auto_dice", lambda: next(rolls))
    monkeypatch.delenv("MANUAL_DICE", raising=False)
    assert we.roll_off_first_turn(manual_roll_allowed=False) == "model"


def test_first_turn_reroll_on_tie(monkeypatch):
    # сначала ничья (3,3), потом model=4 enemy(auto)=1 → model
    rolls = iter([3, 3, 4, 1])
    monkeypatch.setattr(we, "auto_dice", lambda: next(rolls))
    monkeypatch.delenv("MANUAL_DICE", raising=False)
    assert we.roll_off_first_turn(manual_roll_allowed=False) == "model"
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/test_first_turn_rolloff.py -q`
Expected: FAIL (`AttributeError: module ... has no attribute 'roll_off_first_turn'`).

- [ ] **Step 3: Реализовать функцию**

В `core/envs/warhamEnv.py` сразу после `roll_off_attacker_defender` (после строки ~317):

```python
def roll_off_first_turn(manual_roll_allowed: bool = False, log_fn=None) -> str:
    """Determine First Turn (10e): D6 vs D6 после деплоя. Победитель ходит первым.

    Зеркало roll_off_attacker_defender: enemy бросает player_dice только при
    MANUAL_DICE=1 and manual_roll_allowed, model всегда auto_dice. Ничья → переброс.
    Возвращает "model"|"enemy" — сторона, которая ходит первой.
    """
    manual = os.getenv("MANUAL_DICE", "0") == "1" and manual_roll_allowed
    verbose = os.getenv("VERBOSE_LOGS", "0") == "1"
    while True:
        enemy_roll = player_dice() if manual else auto_dice()
        model_roll = auto_dice()
        if enemy_roll == model_roll:
            continue
        first = "enemy" if enemy_roll > model_roll else "model"
        if verbose and log_fn is not None:
            log_fn(f"Determine First Turn: enemy={enemy_roll} model={model_roll} -> first={first}")
        return first
```

- [ ] **Step 4: Запустить — убедиться, что проходит**

Run: `python -m pytest tests/engine/test_first_turn_rolloff.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add core/envs/warhamEnv.py tests/engine/test_first_turn_rolloff.py
git commit -m "feat(engine): roll_off_first_turn — второй roll-off (Determine First Turn)"
```

---

### Task 2: `resolve_first_turn_side` — FIRST_TURN override

**Files:**
- Modify: `core/envs/warhamEnv.py` (после `roll_off_first_turn`)
- Test: `tests/engine/test_first_turn_rolloff.py` (append)

**Interfaces:**
- Consumes: `roll_off_first_turn` (Task 1).
- Produces: `resolve_first_turn_side(*, manual_roll_allowed: bool = False, log_fn=None) -> str` — читает env `FIRST_TURN`; `model_first→"model"`, `enemy_first→"enemy"`, `roll`/пусто/мусор → `roll_off_first_turn(...)`.

- [ ] **Step 1: Написать падающий тест**

```python
# append to tests/engine/test_first_turn_rolloff.py
def test_resolve_force_model_first(monkeypatch):
    monkeypatch.setenv("FIRST_TURN", "model_first")
    monkeypatch.setattr(we, "roll_off_first_turn", lambda **k: "enemy")  # не должен вызваться
    assert we.resolve_first_turn_side() == "model"


def test_resolve_force_enemy_first(monkeypatch):
    monkeypatch.setenv("FIRST_TURN", "enemy_first")
    assert we.resolve_first_turn_side() == "enemy"


def test_resolve_roll_default(monkeypatch):
    monkeypatch.delenv("FIRST_TURN", raising=False)
    monkeypatch.setattr(we, "roll_off_first_turn", lambda **k: "model")
    assert we.resolve_first_turn_side() == "model"


def test_resolve_garbage_falls_back_to_roll(monkeypatch):
    monkeypatch.setenv("FIRST_TURN", "bogus")
    monkeypatch.setattr(we, "roll_off_first_turn", lambda **k: "enemy")
    assert we.resolve_first_turn_side() == "enemy"
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/test_first_turn_rolloff.py -k resolve -q`
Expected: FAIL (`has no attribute 'resolve_first_turn_side'`).

- [ ] **Step 3: Реализовать**

```python
def resolve_first_turn_side(*, manual_roll_allowed: bool = False, log_fn=None) -> str:
    """Сторона первого хода: env FIRST_TURN (model_first|enemy_first) или roll-off.

    Невалидное значение → лог-предупреждение и фолбэк на честный бросок.
    """
    mode = (os.getenv("FIRST_TURN", "roll") or "roll").strip().lower()
    if mode == "model_first":
        return "model"
    if mode == "enemy_first":
        return "enemy"
    if mode not in ("roll", ""):
        if log_fn is not None:
            log_fn(
                f"[FIRST_TURN] неизвестное значение FIRST_TURN={mode!r}; где: "
                "warhamEnv.resolve_first_turn_side; что делать: используйте roll|model_first|enemy_first. "
                "Фолбэк на roll."
            )
    return roll_off_first_turn(manual_roll_allowed=manual_roll_allowed, log_fn=log_fn)
```

- [ ] **Step 4: Запустить — убедиться, что проходит**

Run: `python -m pytest tests/engine/test_first_turn_rolloff.py -q`
Expected: PASS (7 passed).

- [ ] **Step 5: Commit**

```bash
git add core/envs/warhamEnv.py tests/engine/test_first_turn_rolloff.py
git commit -m "feat(engine): resolve_first_turn_side — FIRST_TURN override (roll|model_first|enemy_first)"
```

---

### Task 3: `reset()` собирает turn_order из first_turn_side

**Files:**
- Modify: `core/envs/warhamEnv.py` — `__init__` (строка ~1060), `reset()` (строка ~7165-7166)
- Test: `tests/engine/test_turn_order_from_first_turn.py` (create)

**Interfaces:**
- Consumes: атрибут `env.first_turn_side` (ставится драйвером до `reset`).
- Produces: после `reset()` — `env.turn_order == [first, other]`, `env.active_side == first`; фолбэк `"enemy"` если `first_turn_side` не задан.

- [ ] **Step 1: Написать падающий тест** (через реальный env с минимальным ростером)

```python
# tests/engine/test_turn_order_from_first_turn.py
import os
import unittest

from core.envs.warhamEnv import Warhammer40kEnv
from core.engine.mission import normalize_mission_name


def _minimal_units():
    # 1 юнит на сторону — лёгкий ростер для reset (используем хелпер сборки из тестов проекта,
    # если он есть; иначе — два простых юнита через unitData).
    from core.engine.units import unitData  # путь актуализировать при наличии
    e = [unitData("Necrons", "Necron Warriors")]
    m = [unitData("Necrons", "Necron Warriors")]
    return m, e


class TestTurnOrderFromFirstTurn(unittest.TestCase):
    def _reset_with(self, first):
        env = Warhammer40kEnv()
        env.first_turn_side = first
        m, e = _minimal_units()
        env.reset(options={"m": m, "e": e, "Type": "big", "trunc": True})
        return env

    def test_model_first(self):
        env = self._reset_with("model")
        self.assertEqual(env.turn_order, ["model", "enemy"])
        self.assertEqual(env.active_side, "model")

    def test_enemy_first(self):
        env = self._reset_with("enemy")
        self.assertEqual(env.turn_order, ["enemy", "model"])
        self.assertEqual(env.active_side, "enemy")

    def test_default_fallback_enemy(self):
        env = Warhammer40kEnv()  # first_turn_side не задан
        m, e = _minimal_units()
        env.reset(options={"m": m, "e": e, "Type": "big", "trunc": True})
        self.assertEqual(env.turn_order, ["enemy", "model"])
```

> NB исполнителю: сверить точные хелперы сборки юнитов с существующими тестами движка
> (`tests/engine/test_*`), переиспользовать их фабрику ростера вместо `unitData`, если она другая.

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/test_turn_order_from_first_turn.py -q`
Expected: FAIL (`turn_order == ["enemy","model"]` для model-кейса, т.к. ещё хардкод).

- [ ] **Step 3: Реализовать плоттинг**

В `reset()` непосредственно перед `self.active_side = self.turn_order[0]` (строка ~7166) вставить:

```python
        _first = getattr(self, "first_turn_side", None)
        if _first not in ("model", "enemy"):
            _first = "enemy"  # фолбэк: прямое конструирование env без драйвера
        self.first_turn_side = _first
        self.turn_order = [_first, "model" if _first == "enemy" else "enemy"]
```

В `__init__` (строка ~1060) хардкод оставить как дефолт-плейсхолдер (для прямого доступа до первого reset): `self.turn_order = ["enemy", "model"]` — не трогаем, `reset()` его перезапишет.

- [ ] **Step 4: Запустить — убедиться, что проходит**

Run: `python -m pytest tests/engine/test_turn_order_from_first_turn.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add core/envs/warhamEnv.py tests/engine/test_turn_order_from_first_turn.py
git commit -m "feat(engine): turn_order/active_side из env.first_turn_side в reset()"
```

---

### Task 4: round-counting корректен в обоих порядках (регресс-страховка)

**Files:**
- Test: `tests/engine/test_advance_turn_order_rounds.py` (create)

**Interfaces:**
- Consumes: `Warhammer40kEnv._advance_turn_order` (метод; вызываем на стабе).

Цель: зафиксировать, что `_advance_turn_order` закрывает раунд ровно один раз за полный раунд — на второй половине — для обоих `turn_order`. Это пин против регрессий при переупорядочивании драйверов и фикс латентного AZ-расхождения.

- [ ] **Step 1: Написать тест на стабе**

```python
# tests/engine/test_advance_turn_order_rounds.py
import types

from core.envs.warhamEnv import Warhammer40kEnv


def _stub(turn_order):
    s = types.SimpleNamespace()
    s.turn_order = list(turn_order)
    s.active_side = turn_order[0]
    s.battle_round = 1
    s.phase = "command"
    s._ends = 0

    def _end_battle_round(_self=s):
        _self._ends += 1
        _self.battle_round += 1
    s._end_battle_round = _end_battle_round
    return s


def _play_full_round(stub, order):
    # имитируем драйвер: каждая половина выставляет active_side своей стороны, затем advance
    for side in order:
        stub.active_side = side
        Warhammer40kEnv._advance_turn_order(stub)


def test_enemy_first_one_round_one_end():
    s = _stub(["enemy", "model"])
    _play_full_round(s, ["enemy", "model"])
    assert s._ends == 1
    assert s.battle_round == 2
    assert s.active_side == "enemy"  # начало следующего раунда = turn_order[0]


def test_model_first_one_round_one_end():
    s = _stub(["model", "enemy"])
    _play_full_round(s, ["model", "enemy"])
    assert s._ends == 1
    assert s.battle_round == 2
    assert s.active_side == "model"
```

- [ ] **Step 2: Запустить**

Run: `python -m pytest tests/engine/test_advance_turn_order_rounds.py -q`
Expected: PASS (2 passed) — `_advance_turn_order` уже корректен (Task 3 ничего в нём не менял); тест фиксирует инвариант.

> Если тест падает — это значит инвариант «вторая половина закрывает раунд» нарушен;
> остановиться и разобрать через `superpowers:systematic-debugging` до продолжения.

- [ ] **Step 3: Commit**

```bash
git add tests/engine/test_advance_turn_order_rounds.py
git commit -m "test(engine): round-counting инвариант для обоих turn_order"
```

---

### Task 5: Общий хелпер `run_battle_round`

**Files:**
- Create: `core/engine/turn_sequencing.py`
- Test: `tests/engine/test_turn_sequencing.py` (create)

**Interfaces:**
- Produces: `run_battle_round(env, *, run_model_half, run_enemy_half) -> None` — берёт `turn_order` из `env` (через `getattr(env, "unwrapped", env)`), вызывает замыкания в порядке `turn_order`, прерывается если `game_over` после половины.

- [ ] **Step 1: Написать падающий тест**

```python
# tests/engine/test_turn_sequencing.py
import types

from core.engine.turn_sequencing import run_battle_round


def _env(turn_order, game_over_after=None):
    e = types.SimpleNamespace()
    e.turn_order = list(turn_order)
    e.game_over = False
    e._after = game_over_after  # сторона, после которой выставить game_over
    return e


def test_calls_in_turn_order_model_first():
    calls = []
    e = _env(["model", "enemy"])
    run_battle_round(
        e,
        run_model_half=lambda: calls.append("model"),
        run_enemy_half=lambda: calls.append("enemy"),
    )
    assert calls == ["model", "enemy"]


def test_calls_in_turn_order_enemy_first():
    calls = []
    e = _env(["enemy", "model"])
    run_battle_round(
        e,
        run_model_half=lambda: calls.append("model"),
        run_enemy_half=lambda: calls.append("enemy"),
    )
    assert calls == ["enemy", "model"]


def test_short_circuit_on_game_over():
    calls = []
    e = _env(["enemy", "model"])

    def enemy():
        calls.append("enemy")
        e.game_over = True

    run_battle_round(e, run_model_half=lambda: calls.append("model"), run_enemy_half=enemy)
    assert calls == ["enemy"]  # model-половина не вызвана


def test_reads_unwrapped_turn_order():
    calls = []
    inner = types.SimpleNamespace(turn_order=["model", "enemy"], game_over=False)
    wrapper = types.SimpleNamespace(unwrapped=inner)
    run_battle_round(
        wrapper,
        run_model_half=lambda: calls.append("model"),
        run_enemy_half=lambda: calls.append("enemy"),
    )
    assert calls == ["model", "enemy"]
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/test_turn_sequencing.py -q`
Expected: FAIL (`ModuleNotFoundError: core.engine.turn_sequencing`).

- [ ] **Step 3: Реализовать хелпер**

```python
# core/engine/turn_sequencing.py
"""Порядок двух половин боевого раунда из env.turn_order (Determine First Turn).

Единая точка решения «кто ходит первым» для всех драйверов (eval/train/play/self-play),
чтобы не дублировать порядок и держать счёт раундов согласованным (см.
docs/superpowers/specs/2026-06-21-first-turn-rolloff-design.md).
"""
from __future__ import annotations

from typing import Callable


def run_battle_round(env, *, run_model_half: Callable[[], None], run_enemy_half: Callable[[], None]) -> None:
    """Прогнать обе половины раунда в порядке env.turn_order, short-circuit по game_over."""
    env_u = getattr(env, "unwrapped", env)
    order = list(getattr(env_u, "turn_order", ["enemy", "model"]))
    halves = {"model": run_model_half, "enemy": run_enemy_half}
    for side in order:
        half = halves.get(side)
        if half is None:
            continue
        half()
        if bool(getattr(env_u, "game_over", False)):
            return
```

- [ ] **Step 4: Запустить — убедиться, что проходит**

Run: `python -m pytest tests/engine/test_turn_sequencing.py -q`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add core/engine/turn_sequencing.py tests/engine/test_turn_sequencing.py
git commit -m "feat(engine): run_battle_round — порядок половин раунда из turn_order"
```

---

### Task 6: Интеграция в `eval.run_episode` + резолв first-turn + лог

**Files:**
- Modify: `eval.py` — `run_episode` (резолв перед `env.reset` ~стр.345; цикл ~стр.588-714)
- Test: `tests/engine/test_eval_first_turn_order.py` (create)

**Interfaces:**
- Consumes: `resolve_first_turn_side` (Task 2), `run_battle_round` (Task 5).

- [ ] **Step 1: Написать падающий интеграционный тест** (форс-режимы, проверяем кто отходил первым)

```python
# tests/engine/test_eval_first_turn_order.py
import os
import unittest


class TestEvalFirstTurnOrder(unittest.TestCase):
    def test_model_first_env_var_sets_turn_order(self):
        os.environ["FIRST_TURN"] = "model_first"
        try:
            from core.envs.warhamEnv import resolve_first_turn_side
            self.assertEqual(resolve_first_turn_side(), "model")
        finally:
            os.environ.pop("FIRST_TURN", None)

    def test_run_episode_respects_first_turn(self):
        # smoke: одна партия с FIRST_TURN=model_first не падает и завершается;
        # проверяем, что env.first_turn_side == "model" после resolve в run_episode.
        # (исполнителю: использовать существующую тест-фикстуру eval, если есть;
        #  иначе — пометить как integration и гонять вручную из run-40kai.)
        self.skipTest("integration smoke — гонять через GUI/eval вручную (см. Step 4)")
```

- [ ] **Step 2: Запустить unit-часть**

Run: `python -m pytest tests/engine/test_eval_first_turn_order.py -q`
Expected: 1 passed, 1 skipped.

- [ ] **Step 3: Внести правки в `run_episode`**

(3a) Перед `env.reset(...)` (~стр.345) после установки `attacker_side/defender_side` добавить:

```python
    from core.envs.warhamEnv import resolve_first_turn_side
    env_unwrapped.first_turn_side = resolve_first_turn_side(
        manual_roll_allowed=False, log_fn=None
    )
    _append_eval_log(
        f"[FIRST_TURN] mode={os.getenv('FIRST_TURN','roll')} first={env_unwrapped.first_turn_side}"
    )
```

(3b) Тело `while not done:` (строки ~588-714) обернуть в две локальные функции и вызвать хелпер.
Структура (перенести существующие блоки как есть, не меняя их логику):

```python
    from core.engine.turn_sequencing import run_battle_round
    ...
    while not done:
        step_no = int(episode_len) + 1
        round_io = {"done": done, "reward": 0.0, "info": info, "next_obs": None}

        def _enemy_half():
            # СУЩЕСТВУЮЩИЙ enemy-блок (стр. ~590-660): enemy_mode, base_enemy_fn,
            # enemyTurn(...), log_stratagem_journal_diff(...). Внутри уже есть проверка
            # env_unwrapped.game_over — она ставит game_over в env, чего хелперу достаточно.
            ...

        def _model_half():
            nonlocal episode_len, total_reward
            # СУЩЕСТВУЮЩИЙ model-блок (стр. ~662-714+): attach_fight_stratagem_plan,
            # learner_agent.select_action, трейсы, env.step(action_dict), журнал.
            next_observation, reward, done_m, _, info_m = env.step(action_dict)
            round_io.update(done=done_m, reward=reward, info=info_m, next_obs=next_observation)
            ...  # остальной существующий пост-степ код

        run_battle_round(env_unwrapped, run_model_half=_model_half, run_enemy_half=_enemy_half)

        if bool(getattr(env_unwrapped, "game_over", False)):
            done = True
            info = env_unwrapped.get_info()
            break
        done = bool(round_io["done"])
        info = round_io["info"] if round_io["info"] is not None else info
        reward = round_io["reward"]
        # далее существующий per-round код (battle_round трекинг, round_stats, hp/ctrl) — без изменений
```

> Контракт: `_enemy_half` НЕ должен делать `break`/`return` из внешнего цикла (его роль теперь у `run_battle_round`
> через `env.game_over`). Если в текущем enemy-блоке есть `break` по `game_over` — заменить на «ничего не делать»
> (game_over уже выставлен в env, хелпер сам прервёт раунд).

(3c) Перенести объявления, которые model-блок использует из enemy-блока (например `action_dict`),
так, чтобы `_model_half` имел к ним доступ (объявить `action_dict` внутри `_model_half`, как в оригинале).

- [ ] **Step 4: Запустить регресс eval + ручной smoke**

Run (юнит/смежные): `python -m pytest tests/engine/ tests/tools/test_heur_benchmark_parse.py -q`
Expected: всё PASS.

Ручной smoke (через GUI или CLI), 2 партии в каждом режиме — убедиться, что обе стороны реально ходят первыми:
```bash
FIRST_TURN=enemy_first python -u eval.py --games 2 --learner-agent-id <ID>   # лог [FIRST_TURN] first=enemy
FIRST_TURN=model_first python -u eval.py --games 2 --learner-agent-id <ID>   # лог [FIRST_TURN] first=model
```
Expected: в трейсе при `model_first` первым идёт model-ход; партии завершаются, `actual_games=2`.

- [ ] **Step 5: Commit**

```bash
git add eval.py tests/engine/test_eval_first_turn_order.py
git commit -m "feat(eval): first-turn roll-off в run_episode (порядок через run_battle_round)"
```

---

### Task 7: Интеграция в `train.py` — PPO/DQN rollout + det-eval

**Files:**
- Modify: `train.py` — det-eval loop (~стр.3733-3767), single-env PPO/DQN rollout, det-eval `_run_deterministic_eval` (~стр.5306), резолв first-turn в местах reset (~стр.2218, 2301, 1458, 1597)
- Test: `tests/engine/test_train_first_turn_resolve.py` (create)

**Interfaces:**
- Consumes: `resolve_first_turn_side`, `run_battle_round`.

> Примечание по subproc-rollout: батчевый путь (`USE_SUBPROC_ENVS`, ~стр.5380-5500) делает все enemy-ходы, затем все step. Там
> first-turn резолвится per-env в воркере при reset (`_env_worker`, ~стр.2171/2274), а порядок половин внутри раунда обеспечивается
> тем, что воркер сам гоняет обе половины в порядке `env.turn_order` (см. 7c). Главный процесс остаётся батчевым по «model-step»,
> а enemy-половина уезжает в воркер вместе с раундом.

- [ ] **Step 1: Падающий тест на резолв в train-контексте**

```python
# tests/engine/test_train_first_turn_resolve.py
import os


def test_train_uses_resolve(monkeypatch):
    from core.envs.warhamEnv import resolve_first_turn_side
    monkeypatch.setenv("FIRST_TURN", "model_first")
    assert resolve_first_turn_side() == "model"
    monkeypatch.setenv("FIRST_TURN", "enemy_first")
    assert resolve_first_turn_side() == "enemy"
```

- [ ] **Step 2: Запустить**

Run: `python -m pytest tests/engine/test_train_first_turn_resolve.py -q`
Expected: PASS.

- [ ] **Step 3: Правки**

(7a) В каждом месте, где train ставит `env.attacker_side`/`defender_side` перед reset (~стр.1458-1459, 1596-1597, 2218-2219, 2301-2302), добавить:

```python
                from core.envs.warhamEnv import resolve_first_turn_side
                env.first_turn_side = resolve_first_turn_side(manual_roll_allowed=False, log_fn=None)
```
(для `env_e`/`env` — по имени в данном блоке). Залогировать один раз на старте обучения:
`_log_train(f"[FIRST_TURN] mode={os.getenv('FIRST_TURN','roll')}")`.

(7b) Non-subproc PPO rollout (~стр.3733-3767) и det-eval (~стр.3733; `_run_deterministic_eval`):
обернуть enemy-половину (`enemyTurn`/`strat_tracer.run_enemy_turn`) и model-половину (act+`env.step`) в замыкания,
вызвать `run_battle_round(env_unwrapped, run_model_half=..., run_enemy_half=...)`. Паттерн идентичен Task 6:
`done`/`reward`/`info` прокидывать через `round_io`-холдер; убрать `break` по game_over из enemy-блока
(хелпер прерывает по `env.game_over`).

(7c) Subproc-воркер `_env_worker` (~стр.2171): в обработке команды одного раунда воркер должен гонять обе половины
в порядке `env.turn_order` через `run_battle_round`. Если сейчас воркер делает только `step` (а enemyTurn — в главном процессе),
то: перенести enemy-половину в воркер ИЛИ в главном процессе для каждой ctx выбирать порядок по `ctx.turn_order`.
Минимальный безопасный вариант: в главном цикле (~стр.5383-5405) заменить безусловный «сначала все enemyTurn» на
группировку: сперва обработать enemy-half у env, где `turn_order[0]=="enemy"`, отложить у остальных; после model-step
догнать enemy-half у тех, где `turn_order[0]=="model"`. (Исполнителю: сначала прочитать полный батчевый блок 5380-5520,
затем применить контракт; пин — Step 4 integration.)

- [ ] **Step 4: Тесты + smoke**

Run: `python -m pytest tests/engine/ -q`
Expected: PASS.

Ручной smoke (короткий train, 10-20 эпизодов) в обоих форс-режимах через GUI:
- `FIRST_TURN=model_first` — в TRAIN-логе первым ходит model; `[FIRST_TURN] mode=model_first`.
- `FIRST_TURN=enemy_first` — поведение как до фичи (регресс-эквивалент).
Expected: обучение идёт, нет падений, `battle_round` растёт корректно.

- [ ] **Step 5: Commit**

```bash
git add train.py tests/engine/test_train_first_turn_resolve.py
git commit -m "feat(train): first-turn roll-off в PPO/DQN rollout + det-eval"
```

---

### Task 8: Интеграция в Viewer/play (`game_controller`)

**Files:**
- Modify: `core/engine/game_controller.py` — резолв перед reset (~стр.574-579), цикл (~стр.712-833)
- Test: ручной smoke через Viewer (движковый цикл play тяжело юнит-тестировать)

**Interfaces:**
- Consumes: `resolve_first_turn_side`, `run_battle_round`. Enemy-половина в play = `env.unwrapped.player()` (не `enemyTurn`).

- [ ] **Step 1: Правки**

(8a) Перед `env.reset(...)` (~стр.579) после `env.attacker_side=...` добавить:
```python
            from core.envs.warhamEnv import resolve_first_turn_side
            env.unwrapped.first_turn_side = resolve_first_turn_side(manual_roll_allowed=True, log_fn=self._io.log)
            self._io.log(f"[FIRST_TURN] mode={os.getenv('FIRST_TURN','roll')} first={env.unwrapped.first_turn_side}")
```
(`manual_roll_allowed=True` — Viewer поддерживает ручной бросок при `MANUAL_DICE=1`, как attacker/defender.)

(8b) В цикле (~стр.712-833) обернуть enemy-половину (`env.unwrapped.player()`) и model-половину
(select_action + `env.step`) в замыкания, вызвать `run_battle_round(env.unwrapped, run_model_half=..., run_enemy_half=...)`.
`player()` уже возвращает `(done, info)` и ставит `game_over` — холдер `round_io` прокидывает наружу как в Task 6.

- [ ] **Step 2: Ручной smoke через Viewer**

Запустить Viewer на сохранённом агенте, по одной партии в `FIRST_TURN=model_first` и `enemy_first`.
Expected: в `model_first` первый ход — игрока-модели; UI/логи консистентны; партия доходит до конца; нет рассинхрона раундов.

- [ ] **Step 3: Commit**

```bash
git add core/engine/game_controller.py
git commit -m "feat(play): first-turn roll-off в Viewer/game_controller"
```

---

### Task 9: Регрессионный чеклист — тесты симметрии по порядку

**Files:**
- Test: `tests/engine/test_first_turn_regression.py` (create)

**Interfaces:**
- Consumes: реальный `Warhammer40kEnv`.

- [ ] **Step 1: Тесты на инвариантность по первому ходу**

```python
# tests/engine/test_first_turn_regression.py
import unittest

from core.envs.warhamEnv import Warhammer40kEnv


def _units():
    from core.engine.units import unitData  # сверить с фабрикой из тестов проекта
    return [unitData("Necrons", "Necron Warriors")], [unitData("Necrons", "Necron Warriors")]


class TestFirstTurnRegression(unittest.TestCase):
    def _fresh(self, first):
        env = Warhammer40kEnv()
        env.first_turn_side = first
        m, e = _units()
        env.reset(options={"m": m, "e": e, "Type": "big", "trunc": True})
        return env

    def test_cp_increment_symmetric_after_one_round(self):
        # каждая command_phase даёт +1 обеим сторонам → за полный раунд обе CP равны вне зависимости от порядка
        for first in ("model", "enemy"):
            env = self._fresh(first)
            cp0_m, cp0_e = env.modelCP, env.enemyCP
            env.command_phase(env.turn_order[0], action={} if env.turn_order[0] == "enemy" else None)
            env.command_phase(env.turn_order[1], action={} if env.turn_order[1] == "enemy" else None)
            self.assertEqual(env.modelCP - cp0_m, env.enemyCP - cp0_e,
                             f"CP несимметричны при first={first}")

    def test_reset_round_starts_at_one(self):
        for first in ("model", "enemy"):
            env = self._fresh(first)
            self.assertEqual(env.battle_round, 1)
            self.assertEqual(env.active_side, first)
```

> NB исполнителю: `command_phase` для enemy ожидает `action`/manual; сверить сигнатуру вызова с
> реальным кодом ([warhamEnv.py:4693](../../../core/envs/warhamEnv.py)) и подобрать минимальный валидный `action`.
> Если прямой вызов фаз неудобен — заменить на проигрыш одного полного раунда через `run_battle_round`
> с заглушечным агентом (stay-действия) и сверить CP/VP/battle_round.

- [ ] **Step 2: Запустить**

Run: `python -m pytest tests/engine/test_first_turn_regression.py -q`
Expected: PASS. Падение → реальная регрессия/несимметрия, разбирать через `superpowers:systematic-debugging`.

- [ ] **Step 3: engine-regression-reviewer + commit**

Прогнать субагент `engine-regression-reviewer` по диффу Phase 1. Затем:
```bash
git add tests/engine/test_first_turn_regression.py
git commit -m "test(engine): регресс-инварианты first-turn (CP/раунды симметричны по порядку)"
```

---

# PHASE 2 — AZ/MuZero self-play (изолированно)

> Phase 2 не блокирует Phase 1. При неустойчивости MCTS-интеграции откатывается независимо.

### Task 10: AlphaZero self-play — first-turn + MCTS-prepend

**Files:**
- Modify: `core/models/alphazero_selfplay.py` — `play_episode_with_mcts` (цикл ~стр.106-172)
- Test: `tests/engine/test_az_selfplay_first_turn.py` (create)

**Interfaces:**
- Consumes: `resolve_first_turn_side`, `run_battle_round`.

Контекст: сейчас AZ делает `env.step(model)` → `enemyTurn()` (model-first жёстко). Нужно: (а) резолв `first_turn_side`
перед стартом эпизода и установка на env до reset; (б) если `first=="enemy"` — применить **одну** enemy-половину
ДО входа в per-move MCTS-цикл (prepend), чтобы корень MCTS соответствовал реальному состоянию; (в) тело цикла
(model-MCTS + enemy) оставить — итоговая последовательность при enemy-first: `enemy,(model,enemy),(model,enemy)...`.

Общий prepend-хелпер кладём в `core/engine/turn_sequencing.py` (рядом с `run_battle_round`), чтобы все три self-play
драйвера переиспользовали его без дублирования.

- [ ] **Step 1: Тест порядка для общего prepend-хелпера**

```python
# tests/engine/test_az_selfplay_first_turn.py
import types

from core.engine.turn_sequencing import apply_first_turn_prepend


def _env(first):
    return types.SimpleNamespace(
        turn_order=[first, "model" if first == "enemy" else "enemy"],
        game_over=False,
    )


def test_prepend_when_enemy_first():
    calls = []
    apply_first_turn_prepend(_env("enemy"), run_enemy_half=lambda: calls.append("enemy"))
    assert calls == ["enemy"]


def test_no_prepend_when_model_first():
    calls = []
    apply_first_turn_prepend(_env("model"), run_enemy_half=lambda: calls.append("enemy"))
    assert calls == []


def test_no_prepend_when_already_game_over():
    calls = []
    e = _env("enemy")
    e.game_over = True
    apply_first_turn_prepend(e, run_enemy_half=lambda: calls.append("enemy"))
    assert calls == []
```

- [ ] **Step 2: Запустить — падает**

Run: `python -m pytest tests/engine/test_az_selfplay_first_turn.py -q`
Expected: FAIL (`cannot import name 'apply_first_turn_prepend'`).

- [ ] **Step 3: Реализовать общий хелпер + интеграция в AZ**

(10a) В `core/engine/turn_sequencing.py` добавить:
```python
def apply_first_turn_prepend(env, *, run_enemy_half) -> None:
    """Self-play: если враг ходит первым (turn_order[0]=='enemy'), прогнать его половину
    до per-move цикла, чтобы корень планировщика = реальное состояние после первого хода врага."""
    env_u = getattr(env, "unwrapped", env)
    order = list(getattr(env_u, "turn_order", ["enemy", "model"]))
    if order and order[0] == "enemy" and not bool(getattr(env_u, "game_over", False)):
        run_enemy_half()
```

(10b) В `play_episode_with_mcts` (`core/models/alphazero_selfplay.py`): перед reset поставить
`env_u.first_turn_side = resolve_first_turn_side(manual_roll_allowed=False, log_fn=None)` (импорт из `core.envs.warhamEnv`);
сразу после reset (и установки `obs`) вызвать:
```python
        from core.engine.turn_sequencing import apply_first_turn_prepend
        apply_first_turn_prepend(
            env_u,
            run_enemy_half=lambda: env_u.enemyTurn(trunc=trunc_mode, policy_fn=enemy_policy_fn),
        )
        if bool(getattr(env_u, "game_over", False)):
            done = True
```
Тело per-move цикла (стр. ~106-172) не меняем.

- [ ] **Step 4: Запустить + smoke**

Run: `python -m pytest tests/engine/test_az_selfplay_first_turn.py -q`
Expected: PASS.
Smoke: короткий AZ self-play train (через GUI), `FIRST_TURN=enemy_first` vs `model_first` — нет падений, `battle_round` корректен.

- [ ] **Step 5: Commit**

```bash
git add core/models/alphazero_selfplay.py tests/engine/test_az_selfplay_first_turn.py
git commit -m "feat(az): first-turn roll-off + MCTS-prepend в alphazero_selfplay"
```

---

### Task 11: Gumbel MuZero self-play — first-turn

**Files:**
- Modify: `core/models/gumbel_muzero_selfplay.py` (главный per-move цикл `play_episode_with_gumbel_muzero`)
- Test: `tests/engine/test_gmz_selfplay_first_turn.py` (create)

**Interfaces:**
- Consumes: `resolve_first_turn_side` (Task 2), `apply_first_turn_prepend` (Task 10).

- [ ] **Step 1: Прочитать структуру цикла**

Прочитать `play_episode_with_gumbel_muzero` целиком (найти место reset, `env.step(model)`, `enemyTurn`). Убедиться,
что порядок сейчас model-first (`step` → `enemyTurn`), как в AZ.

- [ ] **Step 2: Написать тест порядка prepend (как в Task 10)**

```python
# tests/engine/test_gmz_selfplay_first_turn.py
import types

from core.engine.turn_sequencing import apply_first_turn_prepend


def _env(first):
    return types.SimpleNamespace(
        turn_order=[first, "model" if first == "enemy" else "enemy"], game_over=False
    )


def test_gmz_prepend_enemy_first():
    calls = []
    apply_first_turn_prepend(_env("enemy"), run_enemy_half=lambda: calls.append("enemy"))
    assert calls == ["enemy"]


def test_gmz_no_prepend_model_first():
    calls = []
    apply_first_turn_prepend(_env("model"), run_enemy_half=lambda: calls.append("enemy"))
    assert calls == []
```

Run: `python -m pytest tests/engine/test_gmz_selfplay_first_turn.py -q` → PASS (хелпер уже есть из Task 10).

- [ ] **Step 3: Интеграция**

В `play_episode_with_gumbel_muzero`: перед reset — `env_u.first_turn_side = resolve_first_turn_side(manual_roll_allowed=False, log_fn=None)`;
сразу после reset:
```python
        from core.engine.turn_sequencing import apply_first_turn_prepend
        apply_first_turn_prepend(
            env_u,
            run_enemy_half=lambda: env_u.enemyTurn(trunc=trunc_mode, policy_fn=enemy_policy_fn),
        )
        if bool(getattr(env_u, "game_over", False)):
            done = True
```
(имена `trunc_mode`/`enemy_policy_fn` — сверить с фактическими в этом драйвере.)

- [ ] **Step 4: Smoke + Commit**

Короткий GMZ self-play train через GUI в `enemy_first`/`model_first` — нет падений, раунды корректны.
```bash
git add core/models/gumbel_muzero_selfplay.py tests/engine/test_gmz_selfplay_first_turn.py
git commit -m "feat(gmz): first-turn roll-off в gumbel_muzero_selfplay"
```

---

### Task 12: Sampled MuZero self-play — first-turn

**Files:**
- Modify: `core/models/sampled_muzero_selfplay.py` (главный per-move цикл `play_episode_with_sampled_muzero`)
- Test: `tests/engine/test_smz_selfplay_first_turn.py` (create)

**Interfaces:**
- Consumes: `resolve_first_turn_side` (Task 2), `apply_first_turn_prepend` (Task 10).

- [ ] **Step 1: Прочитать структуру цикла** `play_episode_with_sampled_muzero` (reset, `env.step`, `enemyTurn`).

- [ ] **Step 2: Тест порядка** — `tests/engine/test_smz_selfplay_first_turn.py`, идентичен Task 11 Step 2 (заменить имена тестов на `smz_`). Run → PASS.

- [ ] **Step 3: Интеграция** — тот же паттерн, что Task 11 Step 3: `first_turn_side = resolve_first_turn_side(...)` перед reset; `apply_first_turn_prepend(env_u, run_enemy_half=lambda: env_u.enemyTurn(trunc=trunc_mode, policy_fn=enemy_policy_fn))` после reset + `done` при `game_over`. Сверить имена переменных с этим драйвером.

- [ ] **Step 4: Smoke + engine-regression-reviewer + Commit**

Короткий SMZ self-play smoke. Перед финальным коммитом Phase 2 — субагент `engine-regression-reviewer` по диффу self-play.
```bash
git add core/models/sampled_muzero_selfplay.py tests/engine/test_smz_selfplay_first_turn.py
git commit -m "feat(smz): first-turn roll-off в sampled_muzero_selfplay"
```

---

## Финальная проверка (после Phase 1; Phase 2 — отдельно)

- [ ] `python -m pytest tests/engine/ tests/tools/ -q` — всё зелёное.
- [ ] Ручной A/B через GUI: `FIRST_TURN=enemy_first` ≈ старое поведение; `FIRST_TURN=model_first` — learner ходит первым; `roll` — лог показывает обе стороны на разных партиях.
- [ ] `engine-regression-reviewer` без критичных замечаний.
- [ ] Обновить память проекта (`MEMORY.md`) пунктом про `FIRST_TURN` и инвариант «драйвер зовёт половины в порядке turn_order».
