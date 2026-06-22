import inspect
import math

import numpy as np


def is_num(maybeNum):
    return maybeNum.isnumeric()


def isBelowHalfStr(data, health):
    startStr = data["#OfModels"]
    return health < (data["W"] * startStr) / 2


def distance(p1, p2):
    return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def distance_cells_euclid(a, b):
    """Евклидова дистанция между центрами клеток (1 клетка = 1")."""
    return math.hypot(float(b[0]) - float(a[0]), float(b[1]) - float(a[1]))


def dice(min=1, max=6, num=1):
    """
    RNG-кубы.
    ВАЖНО: np.random.randint(a, b) даёт [a, b), поэтому используем max+1.
    """
    if num == 1:
        return np.random.randint(min, max + 1)
    return np.array([np.random.randint(min, max + 1) for _ in range(num)])


def bounds(coords, b_len, b_hei):
    if coords[0] <= 0:
        coords[0] = 0
    if coords[1] <= 0:
        coords[1] = 0
    if coords[0] >= b_len:
        coords[0] = b_len - 1
    if coords[1] >= b_hei:
        coords[1] = b_hei - 1
    return coords


def _to_int(x, default=None):
    try:
        if x is None:
            return default
        if isinstance(x, bool):
            return int(x)
        if isinstance(x, (int, np.integer)):
            return int(x)
        if isinstance(x, float):
            return int(x)
        s = str(x).strip()
        if s.endswith("+"):
            s = s[:-1]
        # "AP -2" -> "-2"
        s = s.replace("AP", "").strip()
        return int(float(s))
    except Exception:
        return default


def _roll_damage_expr(expr, _roll_fn):
    """
    Поддержка Damage:
      - int (например 1, 2, 3)
      - "D3", "D6"
    Если встретится что-то другое — считаем 1.
    """
    if isinstance(expr, (int, np.integer)):
        return int(expr)

    if isinstance(expr, str):
        e = expr.strip().upper()
        if e == "D3":
            return int(_roll_fn(min=1, max=3, num=1))
        if e == "D6":
            return int(_roll_fn(min=1, max=6, num=1))

    return 1


def _wound_target(strength: int, toughness: int) -> int:
    # 10e таблица ранений
    if strength >= 2 * toughness:
        return 2
    if strength > toughness:
        return 3
    if strength == toughness:
        return 4
    if strength * 2 <= toughness:
        return 6
    return 5


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




def _weapon_abilities_blob(weapon) -> str:
    """Best-effort собрать все строки с правилами/абилками оружия в один blob."""
    if not isinstance(weapon, dict):
        return str(weapon)

    parts = []
    for k in (
        "Abilities", "Ability", "Rules", "SpecialRules", "Special", "Keywords", "KeyWords", "Tags", "Type"
    ):
        v = weapon.get(k)
        if v is None:
            continue
        if isinstance(v, (list, tuple)):
            parts.extend([str(x) for x in v])
        else:
            parts.append(str(v))

    return " ".join(parts)


def _weapon_has_lethal_hits(weapon) -> bool:
    # 1) Нормальный формат данных: Abilities как dict
    if isinstance(weapon, dict):
        ab = weapon.get("Abilities")
        if isinstance(ab, dict):
            for k, v in ab.items():
                key = str(k).lower().replace(" ", "")
                if key == "lethalhits" and bool(v):
                    return True

    # 2) Фоллбек: строковые/списковые ключевые слова
    blob = _weapon_abilities_blob(weapon).lower()
    return ("lethal hits" in blob) or ("lethal_hit" in blob) or ("lethalhits" in blob)


def _weapon_rapid_fire_x(weapon) -> int:
    """Возвращает X из [RAPID FIRE X] / 'Rapid Fire X' или Abilities:{RapidFire:X}. Если нет — 0."""
    # 1) Нормальный формат данных: Abilities как dict
    if isinstance(weapon, dict):
        ab = weapon.get("Abilities")
        if isinstance(ab, dict):
            for k, v in ab.items():
                key = str(k).lower().replace(" ", "")
                if key == "rapidfire":
                    try:
                        return int(v)
                    except Exception:
                        vv = _to_int(v, default=0)
                        return int(vv or 0)

    # 2) Фоллбек: строковые/списковые ключевые слова
    blob = _weapon_abilities_blob(weapon).lower()

    import re
    m = re.search(r"rapid\s*fire[^0-9]*(\d+)", blob)
    if not m:
        # иногда пишут RAPIDFIRE 1 или это приходит как строка dict: "'RapidFire': 1"
        m = re.search(r"rapidfire[^0-9]*(\d+)", blob)
    if not m:
        return 0

    try:
        return int(m.group(1))
    except Exception:
        return 0



def _weapon_attacks_expr(weapon, default=1):
    if not isinstance(weapon, dict):
        return default
    for k in ("Attacks", "A", "#Attacks", "Shots"):
        if k in weapon:
            v = weapon.get(k)
            if v is not None:
                return v
    return default


def _roll_attacks_expr(expr, _roll_fn):
    """Поддержка Attacks:
      - int / numeric string
      - "D3", "D6"

    Возвращает tuple: (value:int, rolled:bool)
    """
    if isinstance(expr, (int, np.integer)):
        return int(expr), False

    if isinstance(expr, str):
        e = expr.strip().upper()
        if e == "D3":
            return int(_roll_fn(min=1, max=3, num=1)), True
        if e == "D6":
            return int(_roll_fn(min=1, max=6, num=1)), True

        # numeric-like string: "1", "2", "3+"...
        v = _to_int(e, default=None)
        if v is not None:
            return int(v), False

    # неизвестно что — считаем 1
    return 1, False


def _normalize_effects(effects):
    """Привести effects к dict со стабильными ключами (назад-совместимо).

    None -> дефолты (cover=False); "benefit of cover" -> cover=True; dict -> читаем ключи.
    """
    out = {
        "cover": False,
        "reroll_hits": None,
        "reroll_wounds": None,
        "reroll_save": None,
        "strength_mod": 0,
        "ap_improve": 0,
        "hit_penalty": 0,
        "invuln_grant": 0,
    }
    if effects is None:
        return out
    if isinstance(effects, str):
        if effects.strip().lower() == "benefit of cover":
            out["cover"] = True
        return out
    if isinstance(effects, dict):
        out["cover"] = bool(effects.get("cover") or effects.get("benefit_of_cover"))
        rh = effects.get("reroll_hits")
        out["reroll_hits"] = rh if rh in ("ones", "all") else None
        rw = effects.get("reroll_wounds")
        out["reroll_wounds"] = rw if rw in ("ones", "all", "one") else None
        rs = effects.get("reroll_save")
        out["reroll_save"] = rs if rs in ("ones", "all") else None
        try:
            out["strength_mod"] = int(effects.get("strength_mod", 0) or 0)
        except (TypeError, ValueError):
            out["strength_mod"] = 0
        try:
            out["ap_improve"] = int(effects.get("ap_improve", 0) or 0)
        except (TypeError, ValueError):
            out["ap_improve"] = 0
        try:
            out["hit_penalty"] = max(0, int(effects.get("hit_penalty", 0) or 0))
        except (TypeError, ValueError):
            out["hit_penalty"] = 0
        try:
            out["invuln_grant"] = max(0, int(effects.get("invuln_grant", 0) or 0))
        except (TypeError, ValueError):
            out["invuln_grant"] = 0
    return out


def _worst_failed_index(dice, threshold):
    """Индекс наименьшей кости среди проваленных (< threshold); None, если провалов нет.

    Для Command Re-roll реролим всегда худшую проваленную кость.
    """
    worst_idx = None
    worst_val = None
    for idx, d in enumerate(dice):
        d = int(d)
        if d < int(threshold) and (worst_val is None or d < worst_val):
            worst_val = d
            worst_idx = idx
    return worst_idx


def attack(attackerHealth, attackerWeapon, attackerData, attackeeHealth, attackeeData,
           rangeOfComb="Ranged", effects=None, roller=None, distance_to_target=None, hit_on_6: bool = False):
    """Attack resolution (приведено к "10e-стилю" бросков).

    Поддержано (упрощённо):
      - RAPID FIRE X: +X к Attacks, если цель в половине дальности
      - LETHAL HITS: крит-хит (натуральная 6) авто-ранит (без wound roll)

    roller:
      - None => используем RNG dice()
      - иначе => функция броска, сигнатура: roller(num=1, max=6, stage=None) -> int или list[int]
                 (min в проекте везде = 1)

    distance_to_target:
      - float/int (дюймы) — дистанция между атакующим и целью (для Rapid Fire)
    """

    roller_accepts_stage = False
    if callable(roller):
        try:
            roller_accepts_stage = "stage" in inspect.signature(roller).parameters
        except (TypeError, ValueError):
            roller_accepts_stage = False

    def _roll(min=1, max=6, num=1):
        if roller is None:
            return dice(min=min, max=max, num=num)

        return _roll_with_stage(min=min, max=max, num=num)

    def _roll_with_stage(min=1, max=6, num=1, stage=None):
        if roller is None:
            return dice(min=min, max=max, num=num)

        # player_dice поддерживает (num, max) и подразумевает min=1
        if min != 1:
            raise ValueError("roller поддерживает только min=1")
        if roller_accepts_stage:
            return roller(num=num, max=max, stage=stage)
        return roller(num=num, max=max)

    eff = _normalize_effects(effects)

    # --- Targets / profile parsing ---
    sv_base = _to_int(attackeeData.get("Sv"), default=7)
    inv = _to_int(attackeeData.get("IVSave"), default=0)  # 0 = нет инвула

    bs = _to_int(attackerWeapon.get("BS") if rangeOfComb == "Ranged" else attackerWeapon.get("WS"), default=7)
    if hit_on_6:
        # Overwatch 10e: попадания только на натуральную 6.
        bs = 6

    s = _to_int(attackerWeapon.get("S"), default=0) + int(eff["strength_mod"])
    t = _to_int(attackeeData.get("T"), default=0)

    # AP в 10e обычно отрицательный (например -1, -2)
    ap = _to_int(attackerWeapon.get("AP"), default=0) - int(eff["ap_improve"])

    # Benefit of cover: +1 к сейву => целевое значение СНИЖАЕТСЯ на 1 (мин 2+)
    cover_bonus = 1 if (eff["cover"] and rangeOfComb == "Ranged") else 0

    # Цель сейва: Sv - cover_bonus - AP  (если AP отрицательный, то минус AP => +)
    save_target = sv_base - cover_bonus - ap
    if save_target < 2:
        save_target = 2
    # 7+ = нельзя засейвить (кроме инвула)
    if save_target > 6:
        save_target = 7

    if inv and inv > 0:
        save_target = min(save_target, inv)

    granted = int(eff["invuln_grant"])
    if granted > 0:
        save_target = min(save_target, granted)

    # --- How many attacks? ---
    n_models_raw = attackerData.get("#OfModels")
    n_models = int(n_models_raw) if n_models_raw is not None else None
    if n_models is not None and n_models < 1:
        n_models = 1

    model_w = _to_int(attackerData.get("W"), default=0)
    remaining_models = None
    if model_w and model_w > 0 and attackerHealth and attackerHealth > 0:
        remaining_models = int(np.ceil(attackerHealth / model_w))

    if n_models is None:
        n_models = remaining_models if remaining_models is not None else 1
    elif remaining_models is not None:
        n_models = max(1, min(n_models, remaining_models))

    attacks_expr = _weapon_attacks_expr(attackerWeapon, default=1)
    attacks_per_model, attacks_was_rolled = _roll_attacks_expr(attacks_expr, _roll)

    # Rapid Fire X
    if rangeOfComb == "Ranged":
        rf = _weapon_rapid_fire_x(attackerWeapon)
        if rf and distance_to_target is not None:
            w_range = _to_int(attackerWeapon.get("Range"), default=None)
            if w_range is not None and distance_to_target <= (w_range / 2):
                attacks_per_model += int(rf)

    if attacks_per_model < 1:
        attacks_per_model = 1

    attacks = int(n_models * attacks_per_model)
    if attacks < 1:
        attacks = 1

    # --- HIT ROLLS ---
    rolls = _roll_with_stage(num=attacks, stage="hit")
    if isinstance(rolls, int):
        rolls = np.array([rolls], dtype=int)
    else:
        rolls = np.array(list(rolls), dtype=int)

    if eff["reroll_hits"]:
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

    lethal = _weapon_has_lethal_hits(attackerWeapon)

    hit_threshold = bs + int(eff["hit_penalty"])
    hits = 0
    crit_hits = 0
    for r in rolls:
        r = int(r)
        if r == 1:
            continue
        if r == 6:
            # крит-хит (и считаем, что это всегда попадание)
            hits += 1
            crit_hits += 1
            continue
        if r >= hit_threshold:
            hits += 1

    # --- WOUND ROLLS ---
    dmg_instances = []

    if hits > 0:
        wt = _wound_target(s, t) if (s and t) else 7

        auto_wounds = crit_hits if lethal else 0
        # авто-раны сразу добавляем как успешные ранения
        for _ in range(auto_wounds):
            dmg_instances.append(_roll_damage_expr(attackerWeapon.get("Damage"), _roll))

        wound_roll_count = hits - crit_hits if lethal else hits

        if wound_roll_count > 0:
            wound_rolls = _roll_with_stage(num=wound_roll_count, stage="wound")
            if isinstance(wound_rolls, int):
                wound_rolls = np.array([wound_rolls], dtype=int)
            else:
                wound_rolls = np.array(list(wound_rolls), dtype=int)

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

            for w in wound_rolls:
                w = int(w)
                if w == 1:
                    continue
                if w >= wt:
                    dmg_instances.append(_roll_damage_expr(attackerWeapon.get("Damage"), _roll))

    # --- SAVES ---
    if dmg_instances:
        save_rolls = _roll_with_stage(num=len(dmg_instances), stage="save")
        if isinstance(save_rolls, int):
            save_rolls = np.array([save_rolls], dtype=int)
        else:
            save_rolls = np.array(list(save_rolls), dtype=int)

        if eff["reroll_save"]:
            need = []
            for idx, r in enumerate(save_rolls):
                r = int(r)
                if eff["reroll_save"] == "ones" and r == 1:
                    need.append(idx)
                elif eff["reroll_save"] == "all" and r < save_target:
                    need.append(idx)
            if need:
                new = _roll_with_stage(num=len(need), stage="save")
                new = np.array([new] if isinstance(new, int) else list(new), dtype=int)
                for j, idx in enumerate(need):
                    save_rolls[idx] = int(new[j])

        for k in range(len(dmg_instances)):
            r = int(save_rolls[k])
            if r == 1:
                # автопровал
                continue
            if save_target <= 6 and r >= save_target:
                # засейвил => урон 0
                dmg_instances[k] = 0

    dmg = np.array(dmg_instances, dtype=float)

    # --- ALLOCATE DAMAGE ---
    for k in dmg:
        attackeeHealth -= k
        if attackeeHealth < 0:
            attackeeHealth = 0

    return dmg, attackeeHealth
