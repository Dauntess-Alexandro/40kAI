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
