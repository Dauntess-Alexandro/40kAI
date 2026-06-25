from __future__ import annotations

from core.engine.phases.stratagems import by_id, usage_limit_reached


def _unwrap(env):
    return getattr(env, "unwrapped", env)


def charge_cp(env, side: str, cost: int) -> bool:
    """Единая точка CP-расхода. Списывает `cost` CP у стороны `side`.

    side == "model" → env.modelCP, иначе env.enemyCP (по текущему стилю файла).
    Гарантии:
    - cost <= 0: CP не меняется, возвращает True (бесплатное применение).
    - текущий CP < cost: CP не меняется, возвращает False (CP никогда не уходит в минус).
    - успех: CP уменьшается ровно на cost, возвращает True.
    """
    e = _unwrap(env)
    cost = int(cost)
    if cost <= 0:
        return True
    is_model = side == "model"
    cp = int(e.modelCP if is_model else e.enemyCP)
    if cp < cost:
        return False
    if is_model:
        e.modelCP = cp - cost
    else:
        e.enemyCP = cp - cost
    return True


def apply(
    env,
    side: str,
    stratagem_id: str,
    unit_idx: int | None = None,
    phase: str | None = None,
    *,
    reroll_roll: str = "wound",
) -> dict:
    """Применить стратагему (arm) и записать использование в журнал env.

    CP-расход:
    - command_reroll: arm БЕЗ оплаты (pay-on-apply перенесён на consume-точку в warhamEnv),
      но CP-check сохраняется — нельзя arm при CP < cost (легальность выбора, CP не в минус).
      Эффект помечается consumed=False + paid=False (armed, не оплачен).
    - остальные стратагемы: списание CP сразу через единую точку charge_cp.
    Решение «можно ли» — по наличию CP (cp >= cost) и usage_limit.
    unit_idx пока резервируется для Stage 7 (эффект на юнита applies вызывающим).
    Возвращает {"ok": bool, "cp_spent": int, "reason": str | None}.
    """
    e = _unwrap(env)
    d = by_id(stratagem_id)
    # B1c: hard-guard по usage_limit — нельзя применить стратагему сверх лимита окна.
    if usage_limit_reached(e, side, d, phase=phase):
        return {"ok": False, "cp_spent": 0, "reason": "usage_limit"}
    # CP-расход. command_reroll: arm без оплаты, но CP-check сохраняется (CP не в минус).
    # Остальные стратагемы: списание CP сразу (единая точка charge_cp).
    if d.effect_id == "command_reroll":
        cp_now = int(e.modelCP if side == "model" else e.enemyCP)
        if cp_now < d.cp_cost:
            return {"ok": False, "cp_spent": 0, "reason": "not_enough_cp"}
        cp_spent = 0
    elif not charge_cp(e, side, d.cp_cost):
        return {"ok": False, "cp_spent": 0, "reason": "not_enough_cp"}
    else:
        cp_spent = d.cp_cost
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
        # paid=False: arm без оплаты (pay-on-apply перенесён на consume-точку в warhamEnv).
        # consumed=False: эффект ещё не «сработал» (ждёт совпадающего броска).
        active.append(
            {
                "side": str(side),
                "unit_idx": int(unit_idx),
                "round": int(getattr(e, "battle_round", 1)),
                "phase": str(phase or getattr(e, "phase", "fight") or "fight"),
                "effect_id": "command_reroll",
                "reroll_roll": roll,
                "consumed": False,
                "paid": False,
            }
        )
    return {"ok": True, "cp_spent": cp_spent, "reason": None}
