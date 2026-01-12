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


def attack(attackerHealth, attackerWeapon, attackerData, attackeeHealth, attackeeData,
           rangeOfComb="Ranged", effects=None, roller=None):
    """
    Attack resolution (приведено к "10e-стилю" бросков):
      - попадание/ранение/сейв: успех если roll >= target (например 4+)
      - natural 1 всегда провал
      - сейв невозможен, если целевое значение > 6 (т.е. 7+)

    roller:
      - None => используем RNG dice()
      - иначе => функция броска, сигнатура: roller(num=1, max=6) -> int или list[int]
                 (min в проекте везде = 1)
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
    # В исходном проекте используется "#OfModels" (очень грубо), оставляем так.
    attacks = int(attackerData.get("#OfModels", 1))
    if attacks < 1:
        attacks = 1

    # --- HIT ROLLS ---
    rolls = _roll(num=attacks)
    if isinstance(rolls, int):
        rolls = np.array([rolls], dtype=int)
    else:
        rolls = np.array(list(rolls), dtype=int)

    hits = 0
    for r in rolls:
        if r == 1:
            continue
        if r >= bs:
            hits += 1

    # --- WOUND ROLLS ---
    dmg_instances = []
    if hits > 0:
        wound_rolls = _roll(num=hits)
        if isinstance(wound_rolls, int):
            wound_rolls = np.array([wound_rolls], dtype=int)
        else:
            wound_rolls = np.array(list(wound_rolls), dtype=int)

        wt = _wound_target(s, t) if (s and t) else 7
        for w in wound_rolls:
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
