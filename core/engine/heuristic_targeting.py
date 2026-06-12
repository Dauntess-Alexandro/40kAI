# core/engine/heuristic_targeting.py
"""Чистая логика распределения стрельбы (фокус-огонь) для enemy-эвристики.

Отделено от движка ради тестируемости: на вход — обычные dict с EV урона и HP,
на выход — назначение стрелок->цель. Движок (warhamEnv) готовит данные через
expected_damage() и вызывает allocate_shots().
"""
from __future__ import annotations

import glob
import json
import math
import os

# Профили-«характеры» enemy для curriculum-разнообразия МЕЖДУ партиями.
# Выбираются по seed на старте партии; смещают базовый режим движения (когда он
# иначе схлопнулся бы в hold) и силу избегания риска / тяги к objective.
ENEMY_PROFILES = ("balanced", "kiter", "aggressor", "objective", "turtle")

ENEMY_PROFILE_CONFIG = {
    "balanced":  {"mode_bias": None,     "risk_mult": 1.0, "obj_mult": 1.0},
    "kiter":     {"mode_bias": "kite",   "risk_mult": 1.2, "obj_mult": 1.0},
    "aggressor": {"mode_bias": "commit", "risk_mult": 0.8, "obj_mult": 1.0},
    "objective": {"mode_bias": None,     "risk_mult": 1.0, "obj_mult": 1.4},
    "turtle":    {"mode_bias": "hold",   "risk_mult": 1.4, "obj_mult": 0.9},
}


def pick_enemy_profile(seed, profiles=ENEMY_PROFILES) -> str:
    """Детерминированный выбор профиля врага по seed (воспроизводимо)."""
    return profiles[int(seed) % len(profiles)]


def _objective_owner(model_oc: int, enemy_oc: int) -> str:
    if int(enemy_oc) > int(model_oc):
        return "enemy"
    if int(model_oc) > int(enemy_oc):
        return "model"
    if int(model_oc) > 0 and int(enemy_oc) > 0:
        return "contested"
    return "none"


def classify_objective_control(
    *,
    model_oc: int,
    enemy_oc_without_unit: int,
    unit_oc: int,
    candidate_in_radius: bool,
    enemy_oc_before: int | None = None,
) -> dict:
    """Оценить, что кандидатная клетка меняет в контроле одного objective.

    enemy_oc_without_unit — текущий enemy OC на objective без двигающегося юнита.
    enemy_oc_before опционален: env передаёт фактический OC до движения, чтобы stay
    юнита, который сам держит точку, классифицировался как hold, а не capture.
    """
    model = int(model_oc)
    enemy_without = max(0, int(enemy_oc_without_unit))
    unit = max(0, int(unit_oc))
    if unit <= 0:
        before_enemy = enemy_without if enemy_oc_before is None else max(0, int(enemy_oc_before))
        before_owner = _objective_owner(model, before_enemy)
        return {
            "kind": "none",
            "score": 0.0,
            "before_owner": before_owner,
            "after_owner": _objective_owner(model, enemy_without),
            "enemy_oc_after": enemy_without,
            "model_oc": model,
        }

    before_enemy = enemy_without if enemy_oc_before is None else max(0, int(enemy_oc_before))
    enemy_after = enemy_without + (unit if bool(candidate_in_radius) else 0)
    before_owner = _objective_owner(model, before_enemy)
    after_owner = _objective_owner(model, enemy_after)

    kind = "none"
    score = 0.0
    if bool(candidate_in_radius):
        if before_owner == "model" and after_owner == "enemy":
            kind = "flip"
            score = 1.0
        elif before_owner != "enemy" and after_owner == "enemy":
            kind = "capture"
            score = 0.8
        elif after_owner == "contested" and model > 0:
            kind = "contest"
            score = 0.45
        elif before_owner == "enemy" and after_owner == "enemy":
            kind = "hold"
            score = 0.25

    return {
        "kind": kind,
        "score": float(score),
        "before_owner": before_owner,
        "after_owner": after_owner,
        "enemy_oc_after": int(enemy_after),
        "model_oc": model,
    }


# ---- First-class heuristic metrics (счётчики в env, без скрейпинга debug-логов) ----

def new_heur_counters(profile: str = "balanced") -> dict:
    """Свежие счётчики решений эвристики за одну партию."""
    return {
        "profile": str(profile),
        "mode": {"kite": 0, "hold": 0, "commit": 0},
        "role": {"ranged": 0, "hybrid": 0, "melee": 0},
        "obj_kind": {"flip": 0, "capture": 0, "contest": 0, "hold": 0, "none": 0},
        "risk_sum": 0.0,
        "risk_n": 0,
        "charge_attempts": 0,
        "charge_success": 0,
        "moves": 0,
    }


def record_heur_move(counters: dict, mode, role, risk_norm, obj_kind=None) -> None:
    """Зафиксировать одно решение движения (режим/роль/риск). Неизвестные ключи игнорим."""
    if not isinstance(counters, dict):
        return
    m = str(mode)
    r = str(role)
    if m in counters["mode"]:
        counters["mode"][m] += 1
    if r in counters["role"]:
        counters["role"][r] += 1
    obj_map = counters.setdefault("obj_kind", {"flip": 0, "capture": 0, "contest": 0, "hold": 0, "none": 0})
    ok = str(obj_kind or "none")
    if ok in obj_map:
        obj_map[ok] += 1
    try:
        counters["risk_sum"] += float(risk_norm)
        counters["risk_n"] += 1
    except (TypeError, ValueError):
        pass
    counters["moves"] += 1


def record_heur_charge(counters: dict, success: bool) -> None:
    """Зафиксировать объявление чарджа и его исход."""
    if not isinstance(counters, dict):
        return
    counters["charge_attempts"] += 1
    if success:
        counters["charge_success"] += 1


def aggregate_heur_records(records: list[dict]) -> dict:
    """Свести список покадровых счётчиков (по партиям) в итоговую сводку.

    Возвращает распределение режимов, нормированную энтропию стилей, средний риск,
    success-rate чарджа и счётчик профилей.
    """
    mode_totals = {"kite": 0, "hold": 0, "commit": 0}
    role_totals = {"ranged": 0, "hybrid": 0, "melee": 0}
    obj_kind_totals = {"flip": 0, "capture": 0, "contest": 0, "hold": 0, "none": 0}
    profile_counts: dict[str, int] = {}
    risk_sum = 0.0
    risk_n = 0
    charge_attempts = 0
    charge_success = 0
    games = 0
    for rec in records or []:
        if not isinstance(rec, dict):
            continue
        games += 1
        for k in mode_totals:
            mode_totals[k] += int(rec.get("mode", {}).get(k, 0))
        for k in role_totals:
            role_totals[k] += int(rec.get("role", {}).get(k, 0))
        for k in obj_kind_totals:
            obj_kind_totals[k] += int(rec.get("obj_kind", {}).get(k, 0))
        prof = str(rec.get("profile", "balanced"))
        profile_counts[prof] = profile_counts.get(prof, 0) + 1
        risk_sum += float(rec.get("risk_sum", 0.0))
        risk_n += int(rec.get("risk_n", 0))
        charge_attempts += int(rec.get("charge_attempts", 0))
        charge_success += int(rec.get("charge_success", 0))

    total_modes = sum(mode_totals.values())
    entropy = 0.0
    if total_modes > 0:
        for c in mode_totals.values():
            if c <= 0:
                continue
            p = c / total_modes
            entropy -= p * math.log2(p)
    n_modes = len(mode_totals)
    max_entropy = math.log2(n_modes) if n_modes > 1 else 1.0
    entropy_norm = (entropy / max_entropy) if max_entropy > 0 else 0.0

    return {
        "games": games,
        "mode_totals": mode_totals,
        "role_totals": role_totals,
        "obj_kind_totals": obj_kind_totals,
        "profile_counts": profile_counts,
        "style_entropy_norm": entropy_norm,
        "hold_ratio": (float(mode_totals.get("hold", 0)) / float(total_modes)) if total_modes > 0 else 0.0,
        "avg_risk": (risk_sum / risk_n) if risk_n > 0 else 0.0,
        "charge_success_rate": (charge_success / charge_attempts) if charge_attempts > 0 else 0.0,
        "charge_attempts": charge_attempts,
    }


def outcomes_by_profile(records: list[dict]) -> dict:
    """Разбивка исходов по профилям: games / draws / heur_wins / model_wins.

    draw = winner не 'model' и не 'enemy' (turn_limit/ничья). heur_win = winner=='enemy'.
    """
    out: dict[str, dict] = {}
    for rec in records or []:
        if not isinstance(rec, dict):
            continue
        prof = str(rec.get("profile", "balanced"))
        d = out.setdefault(prof, {"games": 0, "draws": 0, "heur_wins": 0, "model_wins": 0})
        d["games"] += 1
        winner = str(rec.get("winner", "") or "").strip().lower()
        if winner == "enemy":
            d["heur_wins"] += 1
        elif winner == "model":
            d["model_wins"] += 1
        else:
            d["draws"] += 1
    return out


def load_heur_records(metrics_dir) -> list[dict]:
    """Считать все записи (по партиям) из per-pid JSONL-файлов heur_dec_*.jsonl."""
    records: list[dict] = []
    for path in glob.glob(os.path.join(str(metrics_dir), "heur_dec_*.jsonl")):
        try:
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except OSError:
            continue
    return records


# P(2d6 >= n): число исходов из 36, дающих сумму >= n (n от 2 до 12).
_2D6_GE_COUNTS = {2: 36, 3: 35, 4: 33, 5: 30, 6: 26, 7: 21, 8: 15, 9: 10, 10: 6, 11: 3, 12: 1}


def prob_2d6_at_least(n) -> float:
    """Вероятность броска 2d6 >= n (для расчёта успеха чарджа в движке: diceRoll >= dist-5)."""
    ni = int(n)
    if ni <= 2:
        return 1.0
    if ni > 12:
        return 0.0
    return _2D6_GE_COUNTS[ni] / 36.0


def melee_trade_value(my_dmg: float, their_hp: float, their_dmg: float, my_hp: float) -> float:
    """Выгодность рукопашного размена: доля HP цели, что я снесу, минус доля моего HP в ответ.

    >0 — выгодный чардж (я сношу больше, чем теряю), <0 — лезу под убой.
    """
    my_frac = float(my_dmg) / max(1.0, float(their_hp))
    their_frac = float(their_dmg) / max(1.0, float(my_hp))
    return my_frac - their_frac


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
