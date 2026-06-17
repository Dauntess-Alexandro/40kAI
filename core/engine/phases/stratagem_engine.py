from __future__ import annotations

from core.engine.phases.stratagems import by_id


def _unwrap(env):
    return getattr(env, "unwrapped", env)


def apply(env, side: str, stratagem_id: str, unit_idx: int | None = None, phase: str | None = None) -> dict:
    """Списать CP за стратагему и записать использование в журнал env.

    Единая точка CP-расхода. Решение «можно ли» — по наличию CP (cp >= cost).
    unit_idx пока резервируется для Stage 7 (эффект на юнита applies вызывающим).
    Возвращает {"ok": bool, "cp_spent": int, "reason": str | None}.
    """
    e = _unwrap(env)
    d = by_id(stratagem_id)
    is_model = side == "model"
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
    if d.effect_id == "hungry_void_strength_mod" and unit_idx is not None:
        active = getattr(e, "active_stratagem_effects", None)
        if active is None:
            active = []
            e.active_stratagem_effects = active
        active.append(
            {
                "side": str(side),
                "unit_idx": int(unit_idx),
                "round": int(getattr(e, "battle_round", 1)),
                "phase": str(phase or getattr(e, "phase", "fight") or "fight"),
                "effect_id": d.effect_id,
                "strength_mod": 1,
            }
        )
    return {"ok": True, "cp_spent": d.cp_cost, "reason": None}
