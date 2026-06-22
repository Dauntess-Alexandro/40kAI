from __future__ import annotations

from core.engine.phases.stratagems import by_id, usage_limit_reached


def _unwrap(env):
    return getattr(env, "unwrapped", env)


def apply(
    env,
    side: str,
    stratagem_id: str,
    unit_idx: int | None = None,
    phase: str | None = None,
    *,
    reroll_roll: str = "wound",
) -> dict:
    """Списать CP за стратагему и записать использование в журнал env.

    Единая точка CP-расхода. Решение «можно ли» — по наличию CP (cp >= cost).
    unit_idx пока резервируется для Stage 7 (эффект на юнита applies вызывающим).
    Возвращает {"ok": bool, "cp_spent": int, "reason": str | None}.
    """
    e = _unwrap(env)
    d = by_id(stratagem_id)
    is_model = side == "model"
    # B1c: hard-guard по usage_limit — нельзя применить стратагему сверх лимита окна.
    if usage_limit_reached(e, side, d, phase=phase):
        return {"ok": False, "cp_spent": 0, "reason": "usage_limit"}
    cp = int(e.modelCP if is_model else e.enemyCP)
    if cp < d.cp_cost:
        return {"ok": False, "cp_spent": 0, "reason": "not_enough_cp"}
    if is_model:
        e.modelCP = cp - d.cp_cost
    else:
        e.enemyCP = cp - d.cp_cost
    used = getattr(e, "stratagem_used", None)
    if used is None:
        used = []
        e.stratagem_used = used
    used.append(
        (
            side,
            d.id,
            int(getattr(e, "battle_round", 1)),
            str(phase or getattr(e, "phase", "")),
            int(unit_idx) if unit_idx is not None else None,
        )
    )
    _FIGHT_EFFECT_PAYLOAD = {
        "hungry_void_strength_mod": {"strength_mod": 1},
    }
    if d.effect_id in _FIGHT_EFFECT_PAYLOAD and unit_idx is not None:
        active = getattr(e, "active_stratagem_effects", None)
        if active is None:
            active = []
            e.active_stratagem_effects = active
        rec = {
            "side": str(side),
            "unit_idx": int(unit_idx),
            "round": int(getattr(e, "battle_round", 1)),
            "phase": str(phase or getattr(e, "phase", "fight") or "fight"),
            "effect_id": d.effect_id,
        }
        rec.update(_FIGHT_EFFECT_PAYLOAD[d.effect_id])
        active.append(rec)
    if d.effect_id == "command_reroll" and unit_idx is not None:
        active = getattr(e, "active_stratagem_effects", None)
        if active is None:
            active = []
            e.active_stratagem_effects = active
        roll = reroll_roll if reroll_roll in ("hit", "wound", "save", "damage", "attacks", "advance", "charge") else "wound"
        active.append(
            {
                "side": str(side),
                "unit_idx": int(unit_idx),
                "round": int(getattr(e, "battle_round", 1)),
                "phase": str(phase or getattr(e, "phase", "fight") or "fight"),
                "effect_id": "command_reroll",
                "reroll_roll": roll,
                "consumed": False,
            }
        )
    return {"ok": True, "cp_spent": d.cp_cost, "reason": None}
