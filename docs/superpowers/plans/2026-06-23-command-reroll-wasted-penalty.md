# Reward-штраф за впустую-command_reroll — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Штрафовать ученика (model) за взведённый, но не сработавший Command Re-roll — per-step net, чтобы голова училась взводить реролл избирательно.

**Architecture:** Две чистые тестируемые единицы на `Warhammer40kEnv`: (1) счётчик применённых стороной model `command_reroll` за шаг, (2) функция величины штрафа `p × max(0, applied−fired)` с гейтом симуляции. `step()` снимает снапшот на входе и применяет штраф к итоговому reward после суммирования фазовых наград. `p` — константа в `reward_config.py`.

**Tech Stack:** Python 3.12, NumPy, PyTorch, pytest. Windows.

## Global Constraints

- **Источник дизайна:** `docs/superpowers/specs/2026-06-23-command-reroll-wasted-penalty-design.md`.
- **Per-step net:** штраф = `COMMAND_REROLL_WASTED_PENALTY × max(0, applied_step − fired_step)`, считается за один `step()` (= ход модели). `applied`/`fired` — только сторона **model** (ученик).
- **Сработавшие command_reroll НЕ штрафуются** (платится лишь за `applied − fired`).
- **Гейт симуляции:** штраф считается/применяется только при `not self._in_simulation_mode()` (env-счётчик `_cmd_reroll_fired` под MCTS-симом не инкрементится → иначе ложный waste).
- `p = COMMAND_REROLL_WASTED_PENALTY = 0.05` (тюнинг-константа, уважает override-механизм reward_config).
- Язык кода/комментов/коммитов — русский. TDD. `ruff check --fix` по изменённым. Коммит RU + `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- НЕ трогать: логику реролла/применения, реакции, env-счётчик `_cmd_reroll_fired` (инкремент — как есть), enemy-ход.

## File Structure

| Файл | Что | 
|------|-----|
| `reward_config.py` | новая константа `COMMAND_REROLL_WASTED_PENALTY = 0.05` |
| `core/envs/warhamEnv.py` | 2 хелпера (`_count_model_command_reroll_applied`, `_command_reroll_wasted_penalty`) + снапшот/штраф в `step()` |
| `tests/engine/test_command_reroll_wasted_penalty.py` | новый тест-файл (6 кейсов) |

---

## Task 1: Штраф за впустую-command_reroll

**Files:**
- Modify: `reward_config.py` (после строки 61, рядом с `COMMAND_INSANE_BRAVERY_PENALTY`)
- Modify: `core/envs/warhamEnv.py` (2 хелпера + `step()` ~7984 снапшот, ~8062 применение)
- Test: `tests/engine/test_command_reroll_wasted_penalty.py` (создать)

**Interfaces:**
- Produces:
  - `reward_config.COMMAND_REROLL_WASTED_PENALTY: float = 0.05`
  - `Warhammer40kEnv._count_model_command_reroll_applied() -> int` — число записей `command_reroll` стороны `model` в `self.stratagem_used`.
  - `Warhammer40kEnv._command_reroll_wasted_penalty(applied_step: int, fired_step: int) -> float` — `0.0` если `_in_simulation_mode()`, иначе `COMMAND_REROLL_WASTED_PENALTY * max(0, applied_step - fired_step)`.

- [ ] **Step 1: Константа в reward_config.py**

Открыть `reward_config.py`, после строки `COMMAND_INSANE_BRAVERY_PENALTY = 0.5` (стр.61) добавить:
```python
# Command Re-roll — штраф за взведённый, но не сработавший реролл (per-step net,
# applied − fired стороны model). Учит голову взводить command_reroll избирательно.
# Сработавшие рероллы НЕ штрафуются. См. spec 2026-06-23-command-reroll-wasted-penalty.
COMMAND_REROLL_WASTED_PENALTY = 0.05
```

- [ ] **Step 2: Падающие тесты (хелперы ещё не существуют)**

Создать `tests/engine/test_command_reroll_wasted_penalty.py`:
```python
"""Reward-штраф за впустую-command_reroll (per-step net, сторона model)."""

import reward_config as reward_cfg
from tests.engine.phases._helpers import build_env


def _setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.stratagem_used = []
    env._cmd_reroll_fired = 0


def test_count_model_command_reroll_ignores_enemy():
    env = build_env()
    _setup(env)
    env.stratagem_used = [
        ("model", "command_reroll", 1, "charge", 0),
        ("enemy", "command_reroll", 1, "charge", 0),
        ("model", "overwatch", 1, "movement", 0),
        ("model", "command_reroll", 2, "fight", 1),
    ]
    assert env._count_model_command_reroll_applied() == 2


def test_penalty_applied_when_wasted():
    env = build_env()
    _setup(env)
    # 3 взведено, 1 сработал → 2 впустую → 2 * 0.05
    pen = env._command_reroll_wasted_penalty(applied_step=3, fired_step=1)
    assert abs(pen - 2 * reward_cfg.COMMAND_REROLL_WASTED_PENALTY) < 1e-9


def test_no_penalty_when_all_fired():
    env = build_env()
    _setup(env)
    assert env._command_reroll_wasted_penalty(applied_step=3, fired_step=3) == 0.0


def test_no_penalty_clamped_when_fired_exceeds_applied():
    env = build_env()
    _setup(env)
    assert env._command_reroll_wasted_penalty(applied_step=1, fired_step=4) == 0.0


def test_penalty_respects_config_override(monkeypatch):
    env = build_env()
    _setup(env)
    monkeypatch.setattr(reward_cfg, "COMMAND_REROLL_WASTED_PENALTY", 0.2)
    pen = env._command_reroll_wasted_penalty(applied_step=2, fired_step=0)
    assert abs(pen - 2 * 0.2) < 1e-9


def test_penalty_skipped_in_simulation_mode():
    env = build_env()
    _setup(env)
    with env.simulation_mode():
        assert env._command_reroll_wasted_penalty(applied_step=5, fired_step=0) == 0.0
```

- [ ] **Step 3: Запустить — упадут (нет методов)**

Run: `python -m pytest tests/engine/test_command_reroll_wasted_penalty.py -v`
Expected: FAIL — `AttributeError: ... _count_model_command_reroll_applied` / `_command_reroll_wasted_penalty`.

- [ ] **Step 4: Реализовать хелперы в warhamEnv.py**

В `core/envs/warhamEnv.py` добавить два метода в класс `Warhammer40kEnv` (удобно — рядом с `_command_reroll_record_exists` / реролл-хелперами, либо после `_in_simulation_mode`). `reward_config` уже импортируется в файле как `reward_cfg` (сверься: в фазах используется `reward_cfg.COMMAND_INSANE_BRAVERY_REWARD` — тот же алиас; если алиас иной, используй его):
```python
    def _count_model_command_reroll_applied(self) -> int:
        """Число записей command_reroll стороны model в журнале stratagem_used."""
        used = getattr(self, "stratagem_used", None) or []
        return sum(
            1 for r in used
            if len(r) > 1 and str(r[0]) == "model" and str(r[1]) == "command_reroll"
        )

    def _command_reroll_wasted_penalty(self, applied_step: int, fired_step: int) -> float:
        """Штраф за впустую-command_reroll за шаг (per-step net). 0 под симуляцией."""
        if self._in_simulation_mode():
            return 0.0
        wasted = max(0, int(applied_step) - int(fired_step))
        return float(reward_cfg.COMMAND_REROLL_WASTED_PENALTY) * wasted
```

- [ ] **Step 5: Запустить тесты — должны пройти**

Run: `python -m pytest tests/engine/test_command_reroll_wasted_penalty.py -v`
Expected: 6 passed. Если `reward_cfg` не импортирован под этим именем — поправить ссылку на фактический алиас reward_config в файле.

- [ ] **Step 6: Снапшот в начале step()**

В `core/envs/warhamEnv.py`, метод `step()` (def на ~7982). Сразу после `reward = 0` (стр.~7984) добавить снапшот:
```python
        _cr_fired_at_start = int(getattr(self, "_cmd_reroll_fired", 0) or 0)
        _cr_applied_at_start = self._count_model_command_reroll_applied()
```

- [ ] **Step 7: Применение штрафа после суммирования фазовых наград**

В том же `step()`, ПОСЛЕ блока суммирования фазовых наград (после `reward += fight_delta` и его лог-строки — это стр.~8062-8064, перед `game_over, end_reason, winner = apply_end_of_battle(...)` на ~8065) вставить:
```python
        _cr_applied_step = self._count_model_command_reroll_applied() - _cr_applied_at_start
        _cr_fired_step = int(getattr(self, "_cmd_reroll_fired", 0) or 0) - _cr_fired_at_start
        _cr_waste_penalty = self._command_reroll_wasted_penalty(_cr_applied_step, _cr_fired_step)
        if _cr_waste_penalty > 0:
            reward -= _cr_waste_penalty
            _cr_wasted_n = max(0, _cr_applied_step - _cr_fired_step)
            self._log_reward(
                f"Reward (шаг): command_reroll впустую×{_cr_wasted_n} penalty=-{_cr_waste_penalty:.3f}"
            )
```
(`self._log_reward` уже используется в step() для пофазных строк — стр.8050/8054 и т.д.)

- [ ] **Step 8: Тест интеграции в step() — штраф реально вычитается из reward**

Добавить в `tests/engine/test_command_reroll_wasted_penalty.py` тест, проверяющий, что step() применяет штраф через дельту счётчиков (без зависимости от стохастики костей — задаём состояние и считаем дельту напрямую через моки хелперов):
```python
def test_step_subtracts_waste_penalty(monkeypatch):
    env = build_env()
    _setup(env)
    # Изолируем от реальной игровой механики step(): обнуляем игровой reward,
    # эмулируем «за шаг model взвёл 2 command_reroll, сработал 0».
    seq = {"applied": [0, 2]}  # 1-й вызов (снапшот)=0, 2-й (конец шага)=2
    monkeypatch.setattr(env, "_count_model_command_reroll_applied", lambda: seq["applied"].pop(0))
    # fired не менялся за шаг → fired_step=0 → wasted=2 → -2*0.05=-0.10
    import numpy as np
    obs, reward, done, trunc, info = env.step(
        __import__("core.engine.phases.legacy_compiler", fromlist=["default_action_dict"]).default_action_dict(len(env.unit_health))
    )
    # reward содержит компонент -0.10 от штрафа (проверяем, что штраф вычтен:
    # сравнение с тем же шагом без waste — см. ниже принцип).
    assert isinstance(reward, float) or hasattr(reward, "__float__")
```
**Замечание исполнителю:** step() стохастичен (кости) и сложен — точное значение reward не детерминировано. Достаточный тест интеграции: замокать `_count_model_command_reroll_applied` так, чтобы дельта = 2 при `_cmd_reroll_fired` неизменном, и убедиться, что итоговый reward на `2*p` меньше, чем при дельте 0. Реализуй через ДВА прогона step() с одинаковым сидом костей (`random.seed`/`np.random.seed` + env-сид, как в других engine-тестах — сверься с `tests/engine/`), один с замоканной дельтой 0, другой с дельтой 2; разница ≈ `2*COMMAND_REROLL_WASTED_PENALTY`. Если детерминизм костей в step() недостижим — оставь юнит-тесты хелперов (Step 2) как основное покрытие, а интеграцию подтверди смоуком (Step 10) и пометь в отчёте. Не пиши вакуумный assert.

- [ ] **Step 9: Прогон тестов + регрессия**

Run: `python -m pytest tests/engine/test_command_reroll_wasted_penalty.py -v` → PASS.
Run: `python -m pytest tests/engine/ -q -p no:cacheprovider --continue-on-collection-errors` → baseline `tests/engine/` не вырос (раньше 23 failed; новые падения, связанные со штрафом — недопустимы). `ruff check --fix reward_config.py core/envs/warhamEnv.py tests/engine/test_command_reroll_wasted_penalty.py`.

- [ ] **Step 10: Смоук — штраф виден в reward-логе**

Run: `TRAIN_ALGO=dqn TRAIN_EPISODES_OVERRIDE=6 NUM_ACTORS=1 ACTION_TRACE_ENABLED=1 python train.py` → exit=0.
Проверить, что reward-механика не падает; если в reward-логах/трейсе встречается строка `command_reroll впустую×N penalty=-…` — штраф работает в живом шаге (может не встретиться за 6 эп, если все рероллы сработали — это ок, не ошибка). Грепни последние строки лога на `command_reroll впустую`.

- [ ] **Step 11: Commit**
```bash
git add reward_config.py core/envs/warhamEnv.py tests/engine/test_command_reroll_wasted_penalty.py
git commit -m "feat(reward): штраф за впустую-command_reroll (per-step net, p=0.05)"
```

---

## Валидация (после переобучения — на пользователе, НЕ часть этого плана)

Переобучить PPO (опц. DQN/AZ) со штрафом, сверить по honest-телеметрии (`cmd_reroll_fired` / `wasted = applied − fired`):
- `fired%` растёт (выше нынешних 25-29%), `wasted` падает;
- DET_EVAL winrate НЕ просел;
- command_reroll не исчез совсем (если applied→0 — `COMMAND_REROLL_WASTED_PENALTY` снизить).
Тюнинг — изменением `COMMAND_REROLL_WASTED_PENALTY` (вниз при коллапсе, вверх при слабом эффекте).

---

## Self-Review

**Spec coverage:**
- `COMMAND_REROLL_WASTED_PENALTY=0.05` в reward_config — Step 1. ✓
- per-step net, сторона model — `_count_model_command_reroll_applied` (model-фильтр) + снапшот/дельта в step() — Steps 4,6,7. ✓
- сработавшие не штрафуются (`max(0, applied−fired)`) — Step 4. ✓
- гейт sim — Step 4 (`_in_simulation_mode` → 0). ✓
- применение к reward + лог — Step 7. ✓
- TDD-кейсы spec (applied/all-fired/clamp/enemy-not-penalized/override/sim) — Step 2 (6 тестов) + Step 8 (интеграция). ✓
- baseline не вырос — Step 9. ✓
- валидация (retrain) — раздел «Валидация», на пользователе. ✓

**Placeholder scan:** кода в каждом шаге достаточно; Step 8 даёт принцип детерминизма костей (два прогона с сидом) + явный фолбэк, не плейсхолдер. Точки вставки в step() даны по строкам (~7984 снапшот, ~8062 применение) + якоря (`reward = 0`, `reward += fight_delta`).

**Type consistency:** `_count_model_command_reroll_applied()->int`, `_command_reroll_wasted_penalty(applied_step:int, fired_step:int)->float`, `COMMAND_REROLL_WASTED_PENALTY:float` — согласованы между Steps 1/4/6/7/тестами. Алиас `reward_cfg` — Step 4 требует сверить с фактическим импортом в файле.

**Примечание (AZ):** под MCTS-симом штраф гейтится (sim), т.е. дерево AZ его не моделирует — штраф действует в реальных шагах PPO/DQN/реальных AZ-роллаутах. Для немедленной цели (PPO command_reroll) достаточно; при необходимости AZ-симам — отдельная задача (трекать fired под симом).

---

## Execution Handoff

См. сообщение после плана.
