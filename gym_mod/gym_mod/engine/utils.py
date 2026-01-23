import numpy as np


def is_num(maybeNum):
    return maybeNum.isnumeric()


def isBelowHalfStr(data, health):
    startStr = data["#OfModels"]
    return health < (data["W"] * startStr) / 2


def distance(p1, p2):
    return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


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


def attack(attackerHealth, attackerWeapon, attackerData, attackeeHealth, attackeeData,
           rangeOfComb="Ranged", effects=None, roller=None, distance_to_target=None, hit_on_6: bool = False):
    """Attack resolution (приведено к "10e-стилю" бросков).

    Поддержано (упрощённо):
      - RAPID FIRE X: +X к Attacks, если цель в половине дальности
      - LETHAL HITS: крит-хит (натуральная 6) авто-ранит (без wound roll)

    roller:
      - None => используем RNG dice()
      - иначе => функция броска, сигнатура: roller(num=1, max=6) -> int или list[int]
                 (min в проекте везде = 1)

    distance_to_target:
      - float/int (дюймы) — дистанция между атакующим и целью (для Rapid Fire)
    """

    def _roll(min=1, max=6, num=1):
        if roller is None:
            return dice(min=min, max=max, num=num)

        # player_dice поддерживает (num, max) и подразумевает min=1
        if min != 1:
            raise ValueError("roller поддерживает только min=1")
        return roller(num=num, max=max)

    # --- Targets / profile parsing ---
    sv_base = _to_int(attackeeData.get("Sv"), default=7)
    inv = _to_int(attackeeData.get("IVSave"), default=0)  # 0 = нет инвула

    bs = _to_int(attackerWeapon.get("BS") if rangeOfComb == "Ranged" else attackerWeapon.get("WS"), default=7)
    if hit_on_6:
        # Overwatch 10e: попадания только на натуральную 6.
        bs = 6

    s = _to_int(attackerWeapon.get("S"), default=0)
    t = _to_int(attackeeData.get("T"), default=0)

    # AP в 10e обычно отрицательный (например -1, -2)
    ap = _to_int(attackerWeapon.get("AP"), default=0)

    # Benefit of cover: +1 к сейву => целевое значение СНИЖАЕТСЯ на 1 (мин 2+)
    cover_bonus = 1 if (effects == "benefit of cover" and rangeOfComb == "Ranged") else 0

    # Цель сейва: Sv - cover_bonus - AP  (если AP отрицательный, то минус AP => +)
    save_target = sv_base - cover_bonus - ap
    if save_target < 2:
        save_target = 2
    # 7+ = нельзя засейвить (кроме инвула)
    if save_target > 6:
        save_target = 7

    if inv and inv > 0:
        save_target = min(save_target, inv)

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
    rolls = _roll(num=attacks)
    if isinstance(rolls, int):
        rolls = np.array([rolls], dtype=int)
    else:
        rolls = np.array(list(rolls), dtype=int)

    lethal = _weapon_has_lethal_hits(attackerWeapon)

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
        if r >= bs:
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
            wound_rolls = _roll(num=wound_roll_count)
            if isinstance(wound_rolls, int):
                wound_rolls = np.array([wound_rolls], dtype=int)
            else:
                wound_rolls = np.array(list(wound_rolls), dtype=int)

            for w in wound_rolls:
                w = int(w)
                if w == 1:
                    continue
                if w >= wt:
                    dmg_instances.append(_roll_damage_expr(attackerWeapon.get("Damage"), _roll))

    # --- SAVES ---
    if dmg_instances:
        save_rolls = _roll(num=len(dmg_instances))
        if isinstance(save_rolls, int):
            save_rolls = np.array([save_rolls], dtype=int)
        else:
            save_rolls = np.array(list(save_rolls), dtype=int)

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
