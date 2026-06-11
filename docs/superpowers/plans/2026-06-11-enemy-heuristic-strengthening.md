# Enemy Heuristic Strengthening — Implementation Plan (Increment 1)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Дать enemy-эвристике измеримый бенчмарк и первый прирост силы (реальный EV урона + фокус-огонь без овёркилла), не уменьшая разнообразие стилей (цель — curriculum-оппонент).

**Architecture:** Чистые тестируемые функции отделяем от движка. `expected_damage()` — аналитический EV, зеркалит `attack()` из [core/engine/utils.py](../../../core/engine/utils.py). `allocate_shots()` — чистая логика фокус-огня в новом модуле `core/engine/heuristic_targeting.py`. Движок ([core/envs/warhamEnv.py](../../../core/envs/warhamEnv.py)) только вызывает их в auto-пути стрельбы. Бенчмарк-харнесс оборачивает существующий `eval.py` как subprocess и парсит логи — движок не трогает.

**Tech Stack:** Python 3.12, numpy, pytest (репозиторий использует `unittest.TestCase`, запуск через `python -m pytest`), eval.py CLI.

**Scope note:** Аудит выявил 6 направлений. Этот план покрывает **только Инкремент 1** (Phases 1–3) — он самодостаточен и шиппабелен. Phases 4–7 (контроль objective, LoS-гейт, charge-EV, рандомизация профиля между партиями) вынесены в раздел «Roadmap» и получат собственные детальные планы.

---

## File Structure

| Файл | Ответственность | Действие |
|------|-----------------|----------|
| `core/engine/utils.py` | `expected_damage()` рядом с `attack()` | Modify (добавить функцию + 2 хелпера EV) |
| `core/engine/heuristic_targeting.py` | Чистая логика фокус-огня `allocate_shots()` | Create |
| `core/envs/warhamEnv.py` | Вызов `allocate_shots` в auto-пути стрельбы | Modify (~5625–5669) |
| `tools/heur_benchmark.py` | Бенчмарк-харнесс (subprocess eval.py + агрегация) | Create |
| `tests/engine/test_expected_damage.py` | Поведенческие тесты EV | Create |
| `tests/engine/test_heuristic_targeting.py` | Поведенческие тесты фокус-огня | Create |
| `tests/engine/test_enemy_shoot_focus_fire_contract.py` | Контракт: auto-путь вызывает `allocate_shots` | Create |
| `tests/tools/test_heur_benchmark_parse.py` | Тесты парсера/агрегации бенчмарка | Create |

---

## Phase 1 — Benchmark harness (измеряем всё последующее)

Без замера «стало ли сильнее» любой тюнинг слепой. Под curriculum нам нужен НЕ только win-rate, но и энтропия распределения стилей (kite/commit/hold) — чтобы не схлопнуть разнообразие. Харнесс не трогает движок: гоняет `eval.py` с `HEURISTIC_DEBUG=1` и парсит логи.

### Task 1: Чистый парсер результатов бенчмарка

**Files:**
- Create: `tools/heur_benchmark.py`
- Test: `tests/tools/test_heur_benchmark_parse.py`

- [ ] **Step 1: Написать падающий тест парсинга win-count и стилей**

```python
# tests/tools/test_heur_benchmark_parse.py
import math
import unittest

from tools.heur_benchmark import parse_eval_output, summarize


class TestHeurBenchmarkParse(unittest.TestCase):
    def test_parse_win_counts_from_eval_detail_line(self):
        text = "blah\n[DETAIL] Итог серии P1/P2/Draw: 7/2/1\nmore\n"
        res = parse_eval_output(text)
        self.assertEqual(res["p1_wins"], 7)
        self.assertEqual(res["p2_wins"], 2)
        self.assertEqual(res["draws"], 1)

    def test_parse_mode_distribution_from_heur_move_lines(self):
        text = (
            "[ENEMY][HEUR][MOVE] unit=11 target=21 mode=kite enemy_role=ranged\n"
            "[ENEMY][HEUR][MOVE] unit=12 target=21 mode=commit enemy_role=melee\n"
            "[ENEMY][HEUR][MOVE] unit=13 target=22 mode=kite enemy_role=ranged\n"
            "[ENEMY][HEUR][MOVE] unit=14 target=22 mode=hold enemy_role=hybrid\n"
        )
        res = parse_eval_output(text)
        self.assertEqual(res["mode_counts"], {"kite": 2, "commit": 1, "hold": 1})

    def test_summarize_computes_winrate_and_style_entropy(self):
        parsed = {"p1_wins": 6, "p2_wins": 3, "draws": 1,
                  "mode_counts": {"kite": 2, "commit": 2, "hold": 2}}
        s = summarize(parsed, heuristic_side="p2")
        self.assertAlmostEqual(s["heur_winrate_all"], 0.3, places=6)
        self.assertAlmostEqual(s["heur_winrate_decisive"], 3 / 9, places=6)
        # три равновероятных режима => энтропия = log2(3) (нормируем по log2(3) => 1.0)
        self.assertAlmostEqual(s["style_entropy_norm"], 1.0, places=6)

    def test_summarize_entropy_zero_when_single_mode(self):
        parsed = {"p1_wins": 5, "p2_wins": 5, "draws": 0,
                  "mode_counts": {"kite": 10}}
        s = summarize(parsed, heuristic_side="p2")
        self.assertAlmostEqual(s["style_entropy_norm"], 0.0, places=6)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Прогнать тест — убедиться, что падает**

Run: `python -m pytest tests/tools/test_heur_benchmark_parse.py -v`
Expected: FAIL с `ModuleNotFoundError: No module named 'tools.heur_benchmark'` (или ImportError на `parse_eval_output`).

- [ ] **Step 3: Реализовать парсер и агрегацию**

```python
# tools/heur_benchmark.py
"""Бенчмарк enemy-эвристики: гоняет eval.py и измеряет силу + разнообразие стилей.

Запуск (пример):
    python tools/heur_benchmark.py --games 30 --seed 0

Зачем style_entropy: цель эвристики — curriculum-оппонент. Чистый win-rate без
контроля энтропии режимов схлопнет разнообразие в один стиль. Мерим оба числа.
"""
from __future__ import annotations

import argparse
import math
import os
import re
import subprocess
import sys

_DETAIL_RE = re.compile(r"Итог серии P1/P2/Draw:\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)")
_MODE_RE = re.compile(r"\[ENEMY\]\[HEUR\]\[MOVE\].*?\bmode=(\w+)")


def parse_eval_output(text: str) -> dict:
    """Достаёт из stdout+логов eval.py: счёт партий и распределение режимов движения."""
    p1 = p2 = draws = 0
    m = _DETAIL_RE.search(text)
    if m:
        p1, p2, draws = int(m.group(1)), int(m.group(2)), int(m.group(3))
    mode_counts: dict[str, int] = {}
    for mm in _MODE_RE.finditer(text):
        mode = mm.group(1)
        mode_counts[mode] = mode_counts.get(mode, 0) + 1
    return {"p1_wins": p1, "p2_wins": p2, "draws": draws, "mode_counts": mode_counts}


def summarize(parsed: dict, *, heuristic_side: str = "p2") -> dict:
    """Считает win-rate эвристики и нормированную энтропию распределения стилей."""
    p1 = int(parsed.get("p1_wins", 0))
    p2 = int(parsed.get("p2_wins", 0))
    draws = int(parsed.get("draws", 0))
    games = p1 + p2 + draws
    decisive = p1 + p2
    heur_wins = p2 if heuristic_side == "p2" else p1
    winrate_all = heur_wins / games if games else 0.0
    winrate_dec = heur_wins / decisive if decisive else 0.0

    counts = parsed.get("mode_counts", {}) or {}
    total = sum(counts.values())
    entropy = 0.0
    if total > 0:
        for c in counts.values():
            if c <= 0:
                continue
            p = c / total
            entropy -= p * math.log2(p)
    n_modes = max(1, len(counts))
    max_entropy = math.log2(n_modes) if n_modes > 1 else 1.0
    entropy_norm = (entropy / max_entropy) if max_entropy > 0 else 0.0
    return {
        "games": games,
        "heur_winrate_all": winrate_all,
        "heur_winrate_decisive": winrate_dec,
        "style_entropy_norm": entropy_norm,
        "mode_counts": dict(counts),
    }


def run_benchmark(games: int, seed: int) -> dict:
    """Гоняет eval.py как subprocess с HEURISTIC_DEBUG=1 и агрегирует результат."""
    env = dict(os.environ)
    env["HEURISTIC_DEBUG"] = "1"
    cmd = [
        sys.executable, "eval.py",
        "--games", str(games),
        "--opponent-policy", "random",
        "--seed", str(seed),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    text = (proc.stdout or "") + "\n" + (proc.stderr or "")
    parsed = parse_eval_output(text)
    return summarize(parsed, heuristic_side="p2")


def main() -> None:
    ap = argparse.ArgumentParser(description="Бенчмарк силы и разнообразия enemy-эвристики")
    ap.add_argument("--games", type=int, default=30)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    summary = run_benchmark(args.games, args.seed)
    print(
        "[HEUR-BENCH] "
        f"games={summary['games']} "
        f"winrate_all={summary['heur_winrate_all']:.3f} "
        f"winrate_decisive={summary['heur_winrate_decisive']:.3f} "
        f"style_entropy_norm={summary['style_entropy_norm']:.3f} "
        f"modes={summary['mode_counts']}"
    )


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Прогнать тест — убедиться, что проходит**

Run: `python -m pytest tests/tools/test_heur_benchmark_parse.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Smoke-проверка харнесса (вне TDD) + фиксация базовой линии**

Run: `python tools/heur_benchmark.py --games 6 --seed 0`
Expected: одна строка `[HEUR-BENCH] games=6 winrate_all=... winrate_decisive=... style_entropy_norm=... modes={...}`.
Записать вывод в описание коммита как baseline-замер. Если `--opponent-policy random` или `--seed` не поддержаны eval.py — сверить флаги в [eval.py](../../../eval.py) (`add_argument`) и подставить реально существующие; флаги парсера менять только в `tools/heur_benchmark.py`, eval.py не трогать.

- [ ] **Step 6: Commit**

```bash
git add tools/heur_benchmark.py tests/tools/test_heur_benchmark_parse.py
git commit -m "feat(heur): benchmark harness для силы и разнообразия enemy-эвристики"
```

---

## Phase 2 — `expected_damage()`: реальный EV урона (фундамент)

Сейчас выбор цели стрельбы использует `expected_damage = min(1.0, attacker_ranged/hp)` — абстрактный скор, не учитывает Toughness/Save цели. Делаем аналитический EV, точно зеркалящий `attack()`.

### Task 2: Аналитический EV урона в utils.py

**Files:**
- Modify: `core/engine/utils.py` (добавить после `_wound_target`, ~строка 97)
- Test: `tests/engine/test_expected_damage.py`

- [ ] **Step 1: Написать падающие тесты EV**

```python
# tests/engine/test_expected_damage.py
import unittest

from core.engine.utils import expected_damage


class TestExpectedDamage(unittest.TestCase):
    def test_basic_no_specials(self):
        # 1 модель, 2 атаки, BS3 (p_hit=4/6), S4 vs T4 (wt=4, p_wound=3/6),
        # Sv4 без AP (save_target=4, p_unsaved=3/6), Damage=1, без lethal/rapid.
        weapon = {"Attacks": 2, "BS": 3, "S": 4, "AP": 0, "Damage": 1, "Range": 24}
        adata = {"#OfModels": 1, "W": 2}
        ddata = {"Sv": 4, "T": 4, "IVSave": 0}
        ev = expected_damage(2, weapon, adata, ddata, rangeOfComb="Ranged", distance_to_target=20)
        # 2 * (4/6) * (3/6) * (3/6) * 1 = 0.33333...
        self.assertAlmostEqual(ev, 2 * (4 / 6) * 0.5 * 0.5 * 1.0, places=6)

    def test_lethal_hits_increase_ev(self):
        base = {"Attacks": 6, "BS": 3, "S": 4, "AP": 0, "Damage": 1, "Range": 24}
        adata = {"#OfModels": 1, "W": 6}
        ddata = {"Sv": 4, "T": 4, "IVSave": 0}
        ev_plain = expected_damage(6, base, adata, ddata, distance_to_target=20)
        lethal = dict(base, Abilities={"LethalHits": True})
        ev_lethal = expected_damage(6, lethal, adata, ddata, distance_to_target=20)
        self.assertGreater(ev_lethal, ev_plain)

    def test_rapid_fire_within_half_range_adds_attacks(self):
        rf = {"Attacks": 1, "BS": 3, "S": 4, "AP": 0, "Damage": 1, "Range": 24,
              "Abilities": {"RapidFire": 1}}
        adata = {"#OfModels": 1, "W": 2}
        ddata = {"Sv": 4, "T": 4, "IVSave": 0}
        ev_far = expected_damage(2, rf, adata, ddata, distance_to_target=20)   # >12 => нет RF
        ev_close = expected_damage(2, rf, adata, ddata, distance_to_target=10)  # <=12 => +1 атака
        self.assertGreater(ev_close, ev_far)

    def test_ap_reduces_save_increases_ev(self):
        w0 = {"Attacks": 4, "BS": 3, "S": 4, "AP": 0, "Damage": 1, "Range": 24}
        w2 = dict(w0, AP=-2)
        adata = {"#OfModels": 1, "W": 4}
        ddata = {"Sv": 3, "T": 4, "IVSave": 0}
        self.assertGreater(
            expected_damage(4, w2, adata, ddata, distance_to_target=20),
            expected_damage(4, w0, adata, ddata, distance_to_target=20),
        )

    def test_models_scale_attacks(self):
        w = {"Attacks": 2, "BS": 3, "S": 4, "AP": 0, "Damage": 1, "Range": 24}
        ddata = {"Sv": 4, "T": 4, "IVSave": 0}
        ev1 = expected_damage(2, w, {"#OfModels": 1, "W": 2}, ddata, distance_to_target=20)
        ev5 = expected_damage(10, w, {"#OfModels": 5, "W": 2}, ddata, distance_to_target=20)
        self.assertAlmostEqual(ev5, ev1 * 5, places=6)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Прогнать тесты — убедиться, что падают**

Run: `python -m pytest tests/engine/test_expected_damage.py -v`
Expected: FAIL с `ImportError: cannot import name 'expected_damage'`.

- [ ] **Step 3: Реализовать `expected_damage` (зеркалит `attack()`)**

Вставить в [core/engine/utils.py](../../../core/engine/utils.py) сразу после `_wound_target` (после строки ~97):

```python
def _attacks_expr_ev(expr) -> float:
    """EV числа атак: int / numeric-str напрямую, D3=2.0, D6=3.5."""
    if isinstance(expr, (int, np.integer)):
        return float(expr)
    if isinstance(expr, str):
        e = expr.strip().upper()
        if e == "D3":
            return 2.0
        if e == "D6":
            return 3.5
        v = _to_int(e, default=None)
        if v is not None:
            return float(v)
    return 1.0


def _damage_expr_ev(expr) -> float:
    """EV урона за неспасённую рану: int напрямую, D3=2.0, D6=3.5, иначе 1.0."""
    if isinstance(expr, (int, np.integer)):
        return float(expr)
    if isinstance(expr, str):
        e = expr.strip().upper()
        if e == "D3":
            return 2.0
        if e == "D6":
            return 3.5
    return 1.0


def expected_damage(attacker_health, attacker_weapon, attacker_data, attackee_data,
                    rangeOfComb="Ranged", distance_to_target=None, effects=None,
                    hit_on_6: bool = False) -> float:
    """Аналитический ожидаемый урон одной атаки attacker -> attackee.

    Точно зеркалит механику attack() из этого же модуля (10e-стиль), но без бросков:
    hit -> wound -> save -> damage, с LETHAL HITS и RAPID FIRE X. Используется
    эвристикой врага для выбора цели и определения «добью/не добью». Возвращает
    float (НЕ обрезается по HP цели — обрезание делает вызывающий код).
    """
    # --- профиль защитника / сейв ---
    sv_base = _to_int(attackee_data.get("Sv"), default=7)
    inv = _to_int(attackee_data.get("IVSave"), default=0)
    ap = _to_int(attacker_weapon.get("AP"), default=0)
    cover_bonus = 1 if (effects == "benefit of cover" and rangeOfComb == "Ranged") else 0
    save_target = sv_base - cover_bonus - ap
    if save_target < 2:
        save_target = 2
    if save_target > 6:
        save_target = 7
    if inv and inv > 0:
        save_target = min(save_target, inv)
    p_save = (7 - save_target) / 6.0 if save_target <= 6 else 0.0
    p_unsaved = 1.0 - p_save

    # --- to-hit ---
    bs = _to_int(attacker_weapon.get("BS") if rangeOfComb == "Ranged" else attacker_weapon.get("WS"), default=7)
    if hit_on_6:
        bs = 6
    if 2 <= bs <= 6:
        p_hit = (7 - bs) / 6.0
    elif bs >= 7:
        p_hit = 1.0 / 6.0  # только натуральная 6 (crit) попадает
    else:
        p_hit = 1.0
    p_crit = 1.0 / 6.0

    # --- to-wound ---
    s = _to_int(attacker_weapon.get("S"), default=0)
    t = _to_int(attackee_data.get("T"), default=0)
    wt = _wound_target(s, t) if (s and t) else 7
    p_wound = (7 - wt) / 6.0 if wt <= 6 else 0.0

    # --- число атак (зеркалит attack()) ---
    n_models_raw = attacker_data.get("#OfModels")
    n_models = int(n_models_raw) if n_models_raw is not None else None
    if n_models is not None and n_models < 1:
        n_models = 1
    model_w = _to_int(attacker_data.get("W"), default=0)
    remaining_models = None
    if model_w and model_w > 0 and attacker_health and attacker_health > 0:
        remaining_models = int(np.ceil(attacker_health / model_w))
    if n_models is None:
        n_models = remaining_models if remaining_models is not None else 1
    elif remaining_models is not None:
        n_models = max(1, min(n_models, remaining_models))

    attacks_per_model = _attacks_expr_ev(_weapon_attacks_expr(attacker_weapon, default=1))
    if rangeOfComb == "Ranged":
        rf = _weapon_rapid_fire_x(attacker_weapon)
        if rf and distance_to_target is not None:
            w_range = _to_int(attacker_weapon.get("Range"), default=None)
            if w_range is not None and distance_to_target <= (w_range / 2):
                attacks_per_model += int(rf)
    if attacks_per_model < 1:
        attacks_per_model = 1
    attacks = float(n_models) * float(attacks_per_model)
    if attacks < 1:
        attacks = 1.0

    # --- свод EV ---
    ev_hits = attacks * p_hit
    if _weapon_has_lethal_hits(attacker_weapon):
        ev_crit = attacks * p_crit
        ev_wound_rolls = max(0.0, ev_hits - ev_crit)
        ev_wounds = ev_crit + ev_wound_rolls * p_wound
    else:
        ev_wounds = ev_hits * p_wound
    ev_unsaved = ev_wounds * p_unsaved
    return float(ev_unsaved * _damage_expr_ev(attacker_weapon.get("Damage")))
```

- [ ] **Step 4: Прогнать тесты — убедиться, что проходят**

Run: `python -m pytest tests/engine/test_expected_damage.py -v`
Expected: PASS (5 passed).

- [ ] **Step 5: Commit**

```bash
git add core/engine/utils.py tests/engine/test_expected_damage.py
git commit -m "feat(heur): аналитический expected_damage (EV урона, зеркалит attack())"
```

---

## Phase 3 — Фокус-огонь без овёркилла

Сейчас каждый стрелок жадно берёт максимум по своему скору — нет учёта урона, уже забронированного другими стрелками в этой фазе. Делаем чистую функцию `allocate_shots()`: последовательное жадное распределение, добивающее цели и избегающее овёркилла.

### Task 3: Чистая логика `allocate_shots`

**Files:**
- Create: `core/engine/heuristic_targeting.py`
- Test: `tests/engine/test_heuristic_targeting.py`

- [ ] **Step 1: Написать падающие тесты фокус-огня**

```python
# tests/engine/test_heuristic_targeting.py
import unittest

from core.engine.heuristic_targeting import allocate_shots


class TestAllocateShots(unittest.TestCase):
    def test_focus_fire_finishes_one_target(self):
        # Два стрелка по 5 EV; Ta(hp6), Tb(hp12). Оба бьют Ta, чтобы снять юнит.
        shooters = [1, 2]
        ev = {1: {10: 5.0, 20: 5.0}, 2: {10: 5.0, 20: 5.0}}
        targets = {10: (6.0, 6.0), 20: (12.0, 12.0)}
        result = allocate_shots(shooters, ev, targets)
        self.assertEqual(result[1], 10)
        self.assertEqual(result[2], 10)

    def test_avoid_overkill_on_already_dead_projection(self):
        # S1 (10 EV) сносит Ta(6). S2 не добивает труп, а бьёт Tb.
        shooters = [1, 2]
        ev = {1: {10: 10.0}, 2: {10: 10.0, 20: 3.0}}
        targets = {10: (6.0, 6.0), 20: (9.0, 9.0)}
        result = allocate_shots(shooters, ev, targets)
        self.assertEqual(result[1], 10)
        self.assertEqual(result[2], 20)

    def test_objective_bonus_breaks_ties_toward_objective_target(self):
        shooters = [1]
        ev = {1: {10: 4.0, 20: 4.0}}
        targets = {10: (10.0, 10.0), 20: (10.0, 10.0)}
        result = allocate_shots(shooters, ev, targets, obj_bonus={20: 1.0})
        self.assertEqual(result[1], 20)

    def test_assigns_every_shooter(self):
        shooters = [1, 2, 3]
        ev = {1: {10: 2.0}, 2: {20: 2.0}, 3: {10: 1.0, 20: 1.0}}
        targets = {10: (5.0, 5.0), 20: (5.0, 5.0)}
        result = allocate_shots(shooters, ev, targets)
        self.assertEqual(set(result.keys()), {1, 2, 3})
        for s in (1, 2, 3):
            self.assertIn(result[s], (10, 20))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Прогнать тесты — убедиться, что падают**

Run: `python -m pytest tests/engine/test_heuristic_targeting.py -v`
Expected: FAIL с `ModuleNotFoundError: No module named 'core.engine.heuristic_targeting'`.

- [ ] **Step 3: Реализовать `allocate_shots`**

```python
# core/engine/heuristic_targeting.py
"""Чистая логика распределения стрельбы (фокус-огонь) для enemy-эвристики.

Отделено от движка ради тестируемости: на вход — обычные dict с EV урона и HP,
на выход — назначение стрелок->цель. Движок (warhamEnv) готовит данные через
expected_damage() и вызывает allocate_shots().
"""
from __future__ import annotations


def allocate_shots(
    shooters: list[int],
    ev_damage: dict[int, dict[int, float]],
    targets: dict[int, tuple[float, float]],
    obj_bonus: dict[int, float] | None = None,
    *,
    kill_w: float = 1.0,
    overkill_w: float = 0.1,
    obj_w: float = 0.15,
) -> dict[int, int]:
    """Последовательное жадное распределение стрельбы.

    shooters:  список id стрелков; обрабатываются от «крупных пушек» к мелким.
    ev_damage: ev_damage[shooter][target] — ожидаемый урон (из expected_damage()).
               Цели, недостижимые для стрелка, просто отсутствуют в его словаре.
    targets:   target_id -> (hp, max_hp).
    obj_bonus: target_id -> 0/1 (стоит ли цель на objective).

    Логика: для каждого стрелка приоритет = добивание (kill_w) + эффективность
    (доля нанесённого урона от max_hp) - штраф овёркилла + бонус objective.
    После назначения вычитаем EV из остатка HP цели (проекция), чтобы следующие
    стрелки не добивали уже «убитую в проекции» цель.
    """
    obj_bonus = obj_bonus or {}
    remaining = {t: float(hp) for t, (hp, _mhp) in targets.items()}
    maxhp = {t: max(1.0, float(mhp)) for t, (_hp, mhp) in targets.items()}

    order = sorted(
        shooters,
        key=lambda s: max((ev_damage.get(s, {}).get(t, 0.0) for t in targets), default=0.0),
        reverse=True,
    )

    assignment: dict[int, int] = {}
    for s in order:
        s_ev = ev_damage.get(s, {})
        best_t = None
        best_pri = float("-inf")
        for t in targets:
            ev = float(s_ev.get(t, 0.0))
            if ev <= 0.0:
                continue
            rem = remaining[t]
            alive = rem > 0.0
            kills = 1.0 if (alive and ev >= rem) else 0.0
            overkill = max(0.0, ev - rem) if alive else ev
            eff = (min(ev, rem) / maxhp[t]) if alive else 0.0
            pri = (
                kill_w * kills
                + eff
                - overkill_w * (overkill / maxhp[t])
                + obj_w * float(obj_bonus.get(t, 0.0))
            )
            if pri > best_pri:
                best_pri = pri
                best_t = t
        if best_t is None:
            # все цели мертвы в проекции / стрелок никого не достаёт: берём max EV
            best_t = max(targets, key=lambda t: s_ev.get(t, 0.0))
        assignment[s] = best_t
        remaining[best_t] = remaining.get(best_t, 0.0) - float(s_ev.get(best_t, 0.0))
    return assignment
```

- [ ] **Step 4: Прогнать тесты — убедиться, что проходят**

Run: `python -m pytest tests/engine/test_heuristic_targeting.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add core/engine/heuristic_targeting.py tests/engine/test_heuristic_targeting.py
git commit -m "feat(heur): allocate_shots — фокус-огонь без овёркилла (чистая логика)"
```

### Task 4: Подключить фокус-огонь в auto-путь стрельбы

Меняем только heuristic_auto-ветку стрельбы ([core/envs/warhamEnv.py:5625-5669](../../../core/envs/warhamEnv.py#L5625-L5669)) — там, где врага ведёт эвристика, а не policy. Policy-ветку ([:5404](../../../core/envs/warhamEnv.py#L5404)) не трогаем (там целью управляет RL-агент).

**Files:**
- Modify: `core/envs/warhamEnv.py` (~5625–5669, auto-ветка `elif side == "enemy":` в `shooting_phase`)
- Modify: импорт `expected_damage`, `allocate_shots` вверху файла
- Test: `tests/engine/test_enemy_shoot_focus_fire_contract.py`

- [ ] **Step 1: Написать контракт-тест (стиль репозитория — проверка источника)**

```python
# tests/engine/test_enemy_shoot_focus_fire_contract.py
import unittest
from pathlib import Path


class TestEnemyShootFocusFireContract(unittest.TestCase):
    def test_auto_shooting_uses_allocate_shots(self):
        source = Path("core/envs/warhamEnv.py").read_text(encoding="utf-8")
        self.assertIn("from core.engine.heuristic_targeting import allocate_shots", source)
        self.assertIn("from core.engine.utils import", source)
        self.assertIn("expected_damage", source)
        # auto-путь стрельбы строит назначение через allocate_shots
        self.assertIn("allocate_shots(", source)
        self.assertIn("_enemy_focus_fire_assignment", source)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Прогнать тест — убедиться, что падает**

Run: `python -m pytest tests/engine/test_enemy_shoot_focus_fire_contract.py -v`
Expected: FAIL на `assertIn("allocate_shots(", ...)`.

- [ ] **Step 3: Добавить импорты**

Найти существующий импорт из `core.engine.utils` в шапке [core/envs/warhamEnv.py](../../../core/envs/warhamEnv.py) (там уже импортируются `attack`, `dice`, `distance` и т.п.) и добавить `expected_damage`. Затем добавить импорт нового модуля рядом:

```python
from core.engine.utils import (
    # ... существующие имена без изменений ...
    expected_damage,
)
from core.engine.heuristic_targeting import allocate_shots
```

Если импорты из `core.engine.utils` идут одной строкой `from core.engine.utils import attack, dice, distance, ...` — просто дописать `, expected_damage` в конец списка, не меняя остального.

- [ ] **Step 4: Построить назначение фокус-огня перед auto-циклом стрельбы**

Вставить непосредственно перед циклом `for i in range(len(self.enemy_health)):` в auto-ветке (`elif side == "enemy":`, ~5626) построение назначения:

```python
        elif side == "enemy":
            # Фокус-огонь: распределяем цели по всем живым стрелкам сразу,
            # чтобы добивать юниты и не делать овёркилл (см. allocate_shots).
            ff_shooters: list[int] = []
            ff_ev: dict[int, dict[int, float]] = {}
            ff_targets: dict[int, tuple[float, float]] = {}
            ff_obj: dict[int, float] = {}
            for i in range(len(self.enemy_health)):
                if self.enemy_health[i] <= 0 or self.enemyFellBack[i]:
                    continue
                if self.enemy_weapon[i] == "None":
                    continue
                adv_i = advanced_flags[i] if advanced_flags else False
                if adv_i and not weapon_is_assault(self.enemy_weapon[i]):
                    continue
                targets_i = self.get_shoot_targets_for_unit("enemy", i)
                if not targets_i:
                    continue
                ff_shooters.append(i)
                ff_ev[i] = {}
                for tid in targets_i:
                    tid = int(tid)
                    dist = self._shooting_distance_between_units("enemy", i, "model", tid)
                    ff_ev[i][tid] = expected_damage(
                        self.enemy_health[i], self.enemy_weapon[i], self.enemy_data[i],
                        self.unit_data[tid], rangeOfComb="Ranged", distance_to_target=dist,
                    )
                    if tid not in ff_targets:
                        ff_targets[tid] = (
                            float(self.unit_health[tid]),
                            float(self._unit_max_hp("model", tid)),
                        )
                        ff_obj[tid] = 1.0 if self._is_position_near_objective(self.unit_coords[tid]) else 0.0
            self._enemy_focus_fire_assignment = (
                allocate_shots(ff_shooters, ff_ev, ff_targets, obj_bonus=ff_obj)
                if ff_shooters else {}
            )
            for i in range(len(self.enemy_health)):
```

(Старый `for i in range(len(self.enemy_health)):` остаётся телом цикла ниже — мы лишь добавили блок и повторили строку заголовка. Убедиться, что заголовок цикла не задублирован: добавляемый блок заканчивается строкой `for i in range(len(self.enemy_health)):`, а исходная такая же строка удаляется.)

- [ ] **Step 5: Использовать назначение вместо пер-юнитного жадного выбора**

Внутри тела цикла заменить строку выбора цели ([:5639](../../../core/envs/warhamEnv.py#L5639)):

```python
                            idOfM, scored_targets = self._enemy_heur_pick_shoot_target(i, [int(v) for v in shootAbleUnits])
```

на использование заранее посчитанного назначения с фоллбеком на старый пик:

```python
                            assigned = getattr(self, "_enemy_focus_fire_assignment", {}).get(i)
                            if assigned is not None and assigned in [int(v) for v in shootAbleUnits]:
                                idOfM = int(assigned)
                                _, scored_targets = self._enemy_heur_pick_shoot_target(i, [int(v) for v in shootAbleUnits])
                            else:
                                idOfM, scored_targets = self._enemy_heur_pick_shoot_target(i, [int(v) for v in shootAbleUnits])
```

- [ ] **Step 6: Прогнать контракт-тест + связанные контракт-тесты эвристики**

Run: `python -m pytest tests/engine/test_enemy_shoot_focus_fire_contract.py tests/engine/test_enemy_heuristic_target_selection_contract.py -v`
Expected: PASS (оба файла).

- [ ] **Step 7: Регресс — прогнать весь engine-набор тестов**

Run: `python -m pytest tests/engine -q`
Expected: PASS без новых падений (сверить с состоянием до правок; известные пред-существующие падения — задокументировать, не чинить в этом плане).

- [ ] **Step 8: Smoke прогон движка через бенчмарк (поведенческая проверка)**

Run: `python tools/heur_benchmark.py --games 10 --seed 0`
Expected: завершается без исключений; строка `[HEUR-BENCH] ...`. Сравнить `winrate_decisive` и `style_entropy_norm` с baseline из Phase 1 Step 5: ожидаем **не ниже** по win-rate и **не ниже** по энтропии стилей (фокус-огонь не должен схлопывать разнообразие движения). Числа записать в коммит.

- [ ] **Step 9: Commit**

```bash
git add core/envs/warhamEnv.py tests/engine/test_enemy_shoot_focus_fire_contract.py
git commit -m "feat(heur): фокус-огонь в auto-стрельбе врага через allocate_shots + expected_damage"
```

---

## Self-Review (выполнено автором плана)

- **Spec coverage:** План покрывает аудит-пункты «реальный EV урона» (п.2, Phase 2), «фокус-огонь без овёркилла» (п.1, Phase 3) и инфраструктуру замера с учётом разнообразия стилей (Phase 1, под curriculum-цель). Пункты 3/4/5/«рандомизация профиля» — в Roadmap (отдельные планы).
- **Placeholder scan:** Все шаги с кодом содержат полный код; команды и ожидаемый вывод указаны. Плейсхолдеров нет.
- **Type consistency:** `expected_damage(...)` сигнатура одинакова в Phase 2 и в вызове Phase 3 Step 4. `allocate_shots(shooters, ev_damage, targets, obj_bonus=...)` — сигнатура из Task 3 совпадает с вызовом в Task 4. `_enemy_focus_fire_assignment` (dict shooter->target) объявляется в Task 4 Step 4 и читается в Step 5; имя совпадает с контракт-тестом Step 1.

**Известный риск интеграции (Task 4):** auto-ветка стрельбы — крупный блок; перед правкой перечитать [warhamEnv.py:5625-5669](../../../core/envs/warhamEnv.py#L5625-L5669) целиком и убедиться, что заголовок `for i in range(len(self.enemy_health)):` не задублирован. Прогнать `pytest tests/engine -q` до и после, чтобы поймать регрессию движка (правило проекта: движок — регрессии дорогие).

---

## Roadmap — последующие планы (каждый = отдельный детальный план)

Под цель **curriculum** (оппонент силён, но варьирует стиль). Порядок — по соотношению сила/трудозатраты.

1. **Phase 4 — Контроль objective вместо дистанции** (аудит п.3). Заменить `_enemy_heur_objective_distance` (евклид до ближайшего маркера) на модель контроля: friendly OC vs enemy OC в радиусе объектива, награда за переворот/удержание контроля с весом по числу оставшихся scoring-ходов. Самый крупный выигрыш по win-rate; крупнее по объёму → отдельный план.
2. **Phase 5 — LoS-гейт risk/threat** (аудит п.4). `_enemy_heur_exposure_risk` и `_enemy_cell_threat_score` сейчас по чистой евклидовой дистанции — гейтить через `visibility_report` (учёт террейна), кешировать на фазу (`ENEMY_HEUR_THREAT_MAP_CACHE`). Делает kite/hold реально живучими.
3. **Phase 6 — Charge EV + 2d6 CDF** (аудит п.5). Заменить фейковую `p_success=(12-…)/12` на реальную таблицу `P(2d6 ≥ нужное)`; гейтить объявление чарджа по ожидаемому размену в melee (`expected_damage` с `rangeOfComb="Melee"` в обе стороны — функция уже готова из Phase 2).
4. **Phase 7 — Рандомизация профиля между партиями** (главный curriculum-рычаг). Пресеты весов (агрессор / черепаха / objective-camper) выбираются по сиду в `reset()`. Даёт агенту спектр оппонентов; mode-quota ([warhamEnv.py:3148](../../../core/envs/warhamEnv.py#L3148)) **оставляем** как внутрипартийный механизм разнообразия.
5. **Phase 8 — Калибровка весов** (аудит п.8). CMA-ES/random search по вектору `ENEMY_HEUR_*` с метрикой бенчмарка (Phase 1), **с ограничением на `style_entropy_norm`** — иначе оптимизатор схлопнет разнообразие. Слить дублирующие термы (`risk_norm`↔`threat_norm`).

---

**Plan complete and saved to `docs/superpowers/plans/2026-06-11-enemy-heuristic-strengthening.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — свежий субагент на каждую задачу, ревью между задачами, быстрая итерация.

**2. Inline Execution** — выполняю задачи в этой сессии через executing-plans, пакетно с чекпойнтами на ревью.

**Какой подход?**
