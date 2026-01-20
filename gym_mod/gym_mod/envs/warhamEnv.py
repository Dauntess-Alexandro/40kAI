import gymnasium as gym
from gymnasium import spaces
import numpy as np
import matplotlib.pyplot as plt
import os
import random
import re

from ..engine.utils import *
from ..engine import utils as engine_utils
from gym_mod.engine.GUIinteract import *

# Victory condition overrides (mission selection)
_VICTORY_CONDITION_MAP = {
    "slay": 1,
    "slay_and_secure": 1,
    "slay and secure": 1,
    "ancient_relic": 2,
    "ancient relic": 2,
    "relic": 2,
    "domination": 3,
}

def _coerce_victory_condition(value):
    if value is None:
        return None
    value = value.strip().lower()
    if not value:
        return None
    if value.isdigit():
        vc = int(value)
        return vc if vc in (1, 2, 3) else None
    return _VICTORY_CONDITION_MAP.get(value)

def _get_forced_victory_condition():
    value = os.getenv("FORCE_VICTORY_CONDITION") or os.getenv("FORCE_MISSION")
    return _coerce_victory_condition(value)

# ============================================================
# 🔧 FIX: resolve string weapons like "Bolt pistol [PISTOL]"
# so engine.utils.attack() always receives a dict (or we safely
# skip the attack instead of crashing with "'str' object has no attribute 'get'").
# This is intentionally defensive: if WeaponData can't be found,
# we still won't crash during training.
# ============================================================

_attack_original = attack  # keep reference to the original engine attack
_WEAPON_INDEX = None

def _norm_weapon_name(x):
    if not isinstance(x, str):
        return x
    # remove tags in square brackets: "Bolt pistol [PISTOL]" -> "Bolt pistol"
    x = re.sub(r"\s*\[.*?\]\s*", "", x)
    return x.strip().lower()

def _build_weapon_index():
    """
    Try to locate WeaponData list from a few common places.
    Returns dict: normalized_name -> weapon_dict
    """
    weapon_list = None

    # 1) engine_utils.weaponData / engine_utils.WeaponData
    for attr in ("weaponData", "WeaponData"):
        v = getattr(engine_utils, attr, None)
        if isinstance(v, list):
            weapon_list = v
            break
        if isinstance(v, dict) and "WeaponData" in v and isinstance(v["WeaponData"], list):
            weapon_list = v["WeaponData"]
            break

    # 2) engine_utils.data["WeaponData"]
    if weapon_list is None:
        v = getattr(engine_utils, "data", None)
        if isinstance(v, dict) and isinstance(v.get("WeaponData"), list):
            weapon_list = v.get("WeaponData")

    # 3) If something named WeaponData got imported via wildcard
    if weapon_list is None:
        v = globals().get("WeaponData")
        if isinstance(v, list):
            weapon_list = v

    idx = {}
    if weapon_list:
        for w in weapon_list:
            if isinstance(w, dict) and "Name" in w:
                idx[_norm_weapon_name(w["Name"])] = w
    return idx

def attack(attackerHealth, attackerWeapon, attacker_data, defenderHealth, defender_data, *args, **kwargs):
    dist = kwargs.pop("distance_to_target", None)
    """
    Wrapper over engine.utils.attack:
    - if attackerWeapon is a string, try to resolve it into a dict from WeaponData
    - if can't resolve, return zero damage and unchanged defender health (no crash)
    """
    global _WEAPON_INDEX
    if isinstance(attackerWeapon, str):
        if _WEAPON_INDEX is None:
            _WEAPON_INDEX = _build_weapon_index()
        attackerWeapon = _WEAPON_INDEX.get(_norm_weapon_name(attackerWeapon))
    if dist is not None:
        attackerWeapon = _apply_rapid_fire(attackerWeapon, dist)


    if attackerWeapon is None or not isinstance(attackerWeapon, dict):
        # can't resolve weapon => skip attack safely
        return [], defenderHealth

    return _attack_original(attackerHealth, attackerWeapon, attacker_data, defenderHealth, defender_data, *args, **kwargs)



def player_dice(num=1, max=6):
    """
    Кубы игрока:
    - если MANUAL_DICE=1, просим ввод в терминале
    - иначе используем рандом (удобно, если хочешь быстро без кубов)
    """
    manual = os.getenv("MANUAL_DICE", "0") == "1"

    if not manual:
        if num == 1:
            return random.randint(1, max)
        return [random.randint(1, max) for _ in range(num)]

    def ask_one():
        while True:
            s = input(f"Введи результат броска (1..{max}): ").strip()
            try:
                v = int(s)
            except ValueError:
                print("❌ Нужно число")
                continue
            if 1 <= v <= max:
                return v
            print(f"❌ Должно быть от 1 до {max}")

    if num == 1:
        return ask_one()

    while True:
        s = input(f"Введи {num} значений (1..{max}) через пробел: ").strip()
        parts = s.split()
        if len(parts) != num:
            print("❌ Неверное количество значений")
            continue
        try:
            vals = [int(x) for x in parts]
        except ValueError:
            print("❌ Нужны числа")
            continue
        if any(v < 1 or v > max for v in vals):
            print(f"❌ Все значения должны быть 1..{max}")
            continue
        return vals


def weapon_is_assault(weapon) -> bool:
    """
    Пытаемся понять, Assault ли оружие.
    Работает даже если weapon — dict/строка/что угодно.
    """
    if weapon is None or weapon == "None":
        return False

    try:
        if isinstance(weapon, dict):
            blob = " ".join([f"{k} {v}" for k, v in weapon.items()])
        else:
            blob = str(weapon)
    except Exception:
        blob = str(weapon)

    return "assault" in blob.lower()

def _verbose_logs_enabled() -> bool:
    """
    Подробные логи бросков (hit/wound/save/damage).
    Включаем автоматически, когда включены MANUAL_DICE, чтобы удобно было играть руками.
    Можно принудительно включить: VERBOSE_LOGS=1.
    """
    return os.getenv("MANUAL_DICE", "0") == "1" or os.getenv("VERBOSE_LOGS", "0") == "1"

def auto_dice(num=1, max=6):
    """RNG-роллер с такой же сигнатурой, как player_dice (для логов бота)."""
    if num == 1:
        return random.randint(1, max)
    return [random.randint(1, max) for _ in range(num)]


def _get_abilities(weapon: dict) -> dict:
    if isinstance(weapon, dict):
        ab = weapon.get("Abilities")
        if isinstance(ab, dict):
            return ab
    return {}

def _apply_rapid_fire(weapon: dict, dist: float):
    """
    [RAPID FIRE X]: +X атак, если цель в половине дальности.
    dist — дистанция до цели (в тех же "дюймах", что и distance()).
    """
    if weapon is None or weapon == "None" or not isinstance(weapon, dict):
        return weapon

    ab = _get_abilities(weapon)
    rf = _parse_int_like(ab.get("RapidFire"))
    if rf is None or rf <= 0:
        return weapon

    w_range = _get_int(weapon, ["Range"], default=None)
    if w_range is None or w_range <= 0:
        return weapon

    if dist <= (w_range / 2):
        # не мутируем общий dict оружия (он может переиспользоваться)
        w2 = dict(weapon)

        # найдём ключ атак, который реально используется в профиле
        attack_key = None
        for k in ("Attacks", "A", "#Attacks", "Shots"):
            if k in weapon:
                attack_key = k
                break

        base_att = _get_int(weapon, [attack_key] if attack_key else ["Attacks","A","#Attacks","Shots"], default=0)
        new_att = base_att + rf

        if attack_key:
            w2[attack_key] = new_att
        # на всякий случай продублируем в "Attacks"
        w2["Attacks"] = new_att

        return w2

    return weapon



def _parse_int_like(v):
    # Best-effort: extracts first integer from things like "3+", "AP -2", "-1", 3, 3.0.
    # Returns None if nothing usable.
    if v is None:
        return None
    if isinstance(v, (int, float)):
        try:
            return int(v)
        except Exception:
            return None
    s = str(v).strip()
    if not s:
        return None
    if s.lower() == "none":
        return None
    m = re.search(r"-?\d+", s)
    if not m:
        return None
    try:
        return int(m.group(0))
    except Exception:
        return None


def _get_int(d: dict, keys, default=None):
    if not isinstance(d, dict):
        return default
    for k in keys:
        if k in d:
            parsed = _parse_int_like(d.get(k))
            if parsed is not None:
                return parsed
    return default


def _wound_target(strength: int, toughness: int) -> int:
    # 10e wound chart
    if strength >= 2 * toughness:
        return 2
    if strength > toughness:
        return 3
    if strength == toughness:
        return 4
    if strength * 2 <= toughness:
        return 6
    return 5


class RollLogger:
    """
    Обёртка для roller=player_dice, чтобы:
    - показывать, что это за бросок (hit/wound/save/damage)
    - сохранять результаты
    - печатать понятный отчёт после атаки

    Важно: внутри engine.utils.attack() иногда первым делом кидается куб на
    *количество выстрелов* (если профиль "D6" и т.п.). Тогда порядок бросков смещается.
    Этот класс пытается это учесть.
    """

    def __init__(self, base_roller):
        self.base = base_roller
        self.calls = []
        self.labels = []
        self.has_attack_count_roll = False

    def configure_for_weapon(self, weapon: dict):
        # Пытаемся понять, есть ли рандом по количеству выстрелов (Attacks = D6/D3 и т.п.)
        att = None
        if isinstance(weapon, dict):
            for k in ("A", "Attacks", "#Attacks", "Shots"):
                if k in weapon:
                    att = weapon.get(k)
                    break

        att_s = str(att).lower() if att is not None else ""
        self.has_attack_count_roll = ("d" in att_s)  # эвристика: "d6", "d3", etc.

        if self.has_attack_count_roll:
            self.labels = [
                "кол-во выстрелов (attacks)",
                "на попадание (to hit)",
                "на ранение (to wound)",
                "сейвы (save)",
                "урон (damage)",
            ]
        else:
            self.labels = [
                "на попадание (to hit)",
                "на ранение (to wound)",
                "сейвы (save)",
                "урон (damage)",
            ]

    def roll(self, num=1, max=6):
        idx = len(self.calls)
        label = self.labels[idx] if idx < len(self.labels) else f"бросок #{idx+1}"
        print(f"\n🎲 Бросок {label}: {num}D{max}")
        res = self.base(num=num, max=max)
        vals = [res] if isinstance(res, int) else list(res)
        self.calls.append({"label": label, "num": num, "max": max, "vals": vals})
        return res
    def print_melee_report(self, weapon: dict, attacker_data: dict, defender_data: dict, dmg_list, effect=None):
        print("\n📌 --- ОТЧЁТ ПО БОЮ (MELEE) ---")

        # В движке WS/BS обычно берём из профиля оружия (как в 10e)
        ws = _get_int(weapon, ["WS", "Ws", "WeaponSkill", "WS+"], default=None)
        if ws is None:
            ws = _get_int(attacker_data, ["WS", "Ws", "WeaponSkill", "WS+"], default=None)

        s = _get_int(weapon, ["S", "Strength"], default=None)

        ap_val = 0
        if isinstance(weapon, dict):
            ap_parsed = _parse_int_like(weapon.get("AP"))
            if ap_parsed is not None:
                ap_val = ap_parsed

        t = _get_int(defender_data, ["T", "Toughness"], default=None)
        sv = _get_int(defender_data, ["Sv", "SV", "Save", "Sv+"], default=None)
        inv = _get_int(defender_data, ["IVSave", "Invul", "Invulnerable", "Inv", "Invul+"], default=None)
        if inv is not None:
            try:
                inv = int(inv)
            except Exception:
                inv = None
        if inv is not None and inv <= 0:
            inv = None

        lethal = False
        try:
            lethal = bool(engine_utils._weapon_has_lethal_hits(weapon))
        except Exception:
            lethal = False

        wname = weapon.get("Name", weapon) if isinstance(weapon, dict) else weapon
        print(f"Оружие: {wname}")
        if ws is not None:
            print(f"WS бойца: {ws}+")
        if s is not None and t is not None:
            print(f"S vs T: {s} vs {t}  -> базово ранение на {_wound_target(s, t)}+")
        if sv is not None:
            inv_txt = f"{inv}+" if inv is not None else "нет"
            print(f"Save цели: {sv}+ (invul: {inv_txt})")
        if ap_val != 0:
            print(f"AP: {ap_val}")
        if lethal:
            print("Абилка: Lethal Hits (6 на попадание = авто-ранение)")
        if effect:
            print(f"Эффект: {effect}")

        off = 1 if self.has_attack_count_roll else 0
        hit_rolls = self.calls[0 + off]["vals"] if len(self.calls) > (0 + off) else []
        wound_rolls = self.calls[1 + off]["vals"] if len(self.calls) > (1 + off) else []
        save_rolls = self.calls[2 + off]["vals"] if len(self.calls) > (2 + off) else []

        hits = None
        crit_hits = None
        auto_wounds = 0
        if ws is not None and hit_rolls:
            hits = sum(1 for r in hit_rolls if r != 1 and r >= ws)
            crit_hits = sum(1 for r in hit_rolls if r != 1 and r >= ws and r == 6)
            if lethal and crit_hits is not None:
                auto_wounds = crit_hits

        wt = None
        rolled_wounds = None
        if s is not None and t is not None and wound_rolls:
            wt = _wound_target(s, t)
            rolled_wounds = sum(1 for r in wound_rolls if r != 1 and r >= wt)

        total_wounds = None
        if rolled_wounds is not None or auto_wounds:
            total_wounds = (rolled_wounds or 0) + (auto_wounds or 0)

        failed_saves = None
        save_target = None
        if (sv is not None or inv is not None) and save_rolls:
            mod_sv = None
            if sv is not None:
                base_sv = sv
                if effect == "benefit of cover":
                    base_sv = max(2, sv - 1)
                mod_sv = base_sv - ap_val
                mod_sv = max(2, mod_sv)
                mod_sv = 7 if mod_sv > 6 else mod_sv

            save_target = mod_sv
            if inv is not None:
                save_target = inv if save_target is None else min(save_target, inv)

        if save_target is not None and total_wounds is not None:
            saved = sum(1 for r in save_rolls if r != 1 and r >= save_target)
            failed_saves = max(0, total_wounds - saved)

        try:
            total_damage = float(np.sum(dmg_list))
        except Exception:
            try:
                if hasattr(dmg_list, 'sum'):
                    total_damage = float(dmg_list.sum())
                elif hasattr(dmg_list, 'item'):
                    total_damage = float(dmg_list.item())
                else:
                    total_damage = float(sum(dmg_list))
            except Exception:
                total_damage = 0.0

        if hit_rolls:
            extra = []
            if hits is not None:
                extra.append(f"hits: {hits}")
            if lethal and crit_hits is not None:
                extra.append(f"crit(6s): {crit_hits} -> авто ран: {auto_wounds}")
            suf = ("  -> " + ", ".join(extra)) if extra else ""
            print(f"Hit rolls:    {hit_rolls}{suf}")

        if wound_rolls:
            if wt is not None:
                print(f"Wound rolls:  {wound_rolls}  (цель {wt}+) -> wounds: {rolled_wounds}")
            else:
                print(f"Wound rolls:  {wound_rolls}")

        if save_rolls:
            if save_target is not None:
                fs = failed_saves if failed_saves is not None else "??"
                print(f"Save rolls:   {save_rolls}  (цель {save_target}+) -> failed saves: {fs}")
            else:
                print(f"Save rolls:   {save_rolls}")

        print(f"\n✅ Итог по движку: прошло урона = {total_damage}")
        print("📌 -------------------------\n")





    def print_shoot_report(self, weapon: dict, attacker_data: dict, defender_data: dict, dmg_list, effect=None):
        print("\n📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---")

        # В движке BS/WS берём из профиля оружия (как в 10e)
        bs = _get_int(weapon, ["BS", "Bs", "BallisticSkill", "BS+"], default=None)
        ws = _get_int(weapon, ["WS", "Ws", "WeaponSkill", "WS+"], default=None)

        # Если почему-то BS/WS отсутствуют в оружии — откатимся к данным юнита (как было раньше)
        if bs is None:
            bs = _get_int(attacker_data, ["BS", "Bs", "BallisticSkill", "BS+"], default=None)

        s = _get_int(weapon, ["S", "Strength"], default=None)

        ap_val = 0
        if isinstance(weapon, dict):
            ap_parsed = _parse_int_like(weapon.get("AP"))
            if ap_parsed is not None:
                ap_val = ap_parsed

        t = _get_int(defender_data, ["T", "Toughness"], default=None)
        sv = _get_int(defender_data, ["Sv", "SV", "Save", "Sv+"], default=None)
        inv = _get_int(defender_data, ["IVSave", "Invul", "Invulnerable", "Inv", "Invul+"], default=None)

        wname = weapon
        if isinstance(weapon, dict):
            wname = weapon.get("Name", weapon)

        # Абилки оружия (берём из engine.utils, там же, где расчёт)
        lethal = False
        rf = 0
        try:
            lethal = bool(engine_utils._weapon_has_lethal_hits(weapon))
            rf = int(engine_utils._weapon_rapid_fire_x(weapon) or 0)
        except Exception:
            pass

        print(f"Оружие: {wname}")
        if bs is not None:
            print(f"BS оружия: {bs}+")
        if s is not None and t is not None:
            print(f"S vs T: {s} vs {t}  -> базово ранение на {_wound_target(s, t)}+")
        if sv is not None:
            # В данных проекта часто invul=0 означает "нет инвула".
            inv_txt = "нет"
            if inv is not None:
                try:
                    inv_i = int(inv)
                    if inv_i > 0:
                        inv_txt = f"{inv_i}+"
                except Exception:
                    pass
            print(f"Save цели: {sv}+ (invul: {inv_txt})")

        if ap_val != 0:
            print(f"AP: {ap_val}")

        if rf:
            print(f"Правило: Rapid Fire {rf} (если цель в половине дальности: +{rf} атак)")
        if lethal:
            print("Правило: Lethal Hits (крит-хиты авто-ранят)")
        if effect:
            print(f"Эффект: {effect}")

        off = 1 if self.has_attack_count_roll else 0

        atk_rolls = self.calls[0]["vals"] if self.has_attack_count_roll and len(self.calls) > 0 else []
        hit_rolls = self.calls[0 + off]["vals"] if len(self.calls) > (0 + off) else []
        wound_rolls = self.calls[1 + off]["vals"] if len(self.calls) > (1 + off) else []
        save_rolls = self.calls[2 + off]["vals"] if len(self.calls) > (2 + off) else []

        # --- hits ---
        hits = None
        crit_hits = None
        if bs is not None and hit_rolls:
            crit_hits = sum(1 for r in hit_rolls if int(r) == 6)
            hits = 0
            for r in hit_rolls:
                r = int(r)
                if r == 1:
                    continue
                if r == 6:
                    hits += 1
                    continue
                if r >= bs:
                    hits += 1

        # --- wounds ---
        wt = None
        rolled_wounds = None
        auto_wounds = 0
        total_wounds = None

        if s is not None and t is not None and wound_rolls:
            wt = _wound_target(s, t)
            rolled_wounds = sum(1 for r in wound_rolls if int(r) != 1 and int(r) >= wt)

        if lethal and crit_hits is not None:
            auto_wounds = int(crit_hits)

        if rolled_wounds is not None:
            total_wounds = rolled_wounds + (auto_wounds if lethal else 0)

        # --- saves ---
        failed_saves = None
        save_target = None
        if (sv is not None or inv is not None) and save_rolls:
            mod_sv = None
            if sv is not None:
                base_sv = sv
                if effect == "benefit of cover":
                    base_sv = max(2, sv - 1)
                mod_sv = base_sv - ap_val
                if mod_sv < 2:
                    mod_sv = 2
                if mod_sv > 6:
                    mod_sv = 7

            save_target = mod_sv
            # invul=0 в данных означает "нет инвула" — не должен улучшать сейв.
            if inv is not None:
                try:
                    inv_i = int(inv)
                except Exception:
                    inv_i = None
                if inv_i is not None and inv_i > 0:
                    save_target = inv_i if save_target is None else min(save_target, inv_i)


        if save_target is not None and total_wounds is not None:
            saved = 0
            for r in save_rolls:
                r = int(r)
                if r == 1:
                    continue
                if save_target <= 6 and r >= save_target:
                    saved += 1
            failed_saves = max(0, total_wounds - saved)

        try:
            # dmg_list обычно numpy array; sum() работает, но isinstance не ловит ndarray.
            if isinstance(dmg_list, (list, tuple, np.ndarray)):
                total_damage = float(np.sum(dmg_list))
            else:
                total_damage = float(dmg_list)
        except Exception:
           total_damage = 0

        if atk_rolls:
            print(f"\nAttacks roll: {atk_rolls}")
        if hit_rolls:
            extra = ""
            if hits is not None:
                extra = f"  -> hits: {hits}"
                if crit_hits is not None and crit_hits > 0:
                    extra += f" (crits: {crit_hits})"
            print(f"Hit rolls:    {hit_rolls}{extra}")

        if wound_rolls:
            if wt is not None and rolled_wounds is not None:
                if lethal and auto_wounds:
                    print(f"Wound rolls:  {wound_rolls}  (цель {wt}+) -> rolled wounds: {rolled_wounds} + auto(w/LETHAL): {auto_wounds} = {total_wounds}")
                else:
                    print(f"Wound rolls:  {wound_rolls}  (цель {wt}+) -> wounds: {rolled_wounds}")
            else:
                print(f"Wound rolls:  {wound_rolls}")

        if save_rolls:
            if save_target is not None:
                fs = failed_saves if failed_saves is not None else "??"
                print(f"Save rolls:   {save_rolls}  (цель {save_target}+) -> failed saves: {fs}")
            else:
                print(f"Save rolls:   {save_rolls}")

        print(f"\n✅ Итог по движку: прошло урона = {total_damage}")
        print("📌 -------------------------\n")

class Warhammer40kEnv(gym.Env):
    def __init__(self, enemy, model, b_len, b_hei):
        # keep original references (handy + avoids AttributeError in some branches)
        self.enemy = enemy
        self.model = model

        savePath = "display/"
        if os.path.isdir(savePath):
            for fil in os.listdir(savePath):
                try:
                    os.remove(os.path.join(savePath, fil))
                except Exception:
                    pass

        # ✅ 1) Собираем Обычный Python dict со всеми ключами
        action_spaces = {
            'move':   spaces.Discrete(5),          # 0 down, 1 up, 2 left, 3 right, 4 none
            'attack': spaces.Discrete(2),          # 0 = fallback/leave fight, 1 = try charge/engage
            'shoot':  spaces.Discrete(len(enemy)), # индекс цели для стрельбы
            'charge': spaces.Discrete(len(enemy)), # индекс цели для чарджа
            'use_cp': spaces.Discrete(5),          # 0 none, 1 bravery, 2 overwatch, 3 smokescreen, 4 heroic
            'cp_on':  spaces.Discrete(len(model))  # на какого своего юнита тратить CP
        }

        # ✅ 2) Добавляем индивидуальные "move_num_i" для каждого модельного юнита
        for i in range(len(model)):
            action_spaces[f"move_num_{i}"] = spaces.Discrete(12)

        # ✅ 3) Теперь только ОДИН раз создаём spaces.Dict
        self.action_space = spaces.Dict(action_spaces)
        print("Action keys:", self.action_space.spaces.keys())

        # Initialize game state + board
        self.iter = 0
        self.restarts = 0
        self.playType = False
        self.b_len = b_len
        self.b_hei = b_hei
        self.board = np.zeros((self.b_len, self.b_hei))

        self.unit_weapon = []
        self.unit_melee = []
        self.enemy_weapon = []
        self.enemy_melee = []
        self.unit_data = []
        self.enemy_data = []
        self.unit_coords = []
        self.enemy_coords = []
        self.unit_health = []
        self.enemy_health = []

        self.game_over = False
        self.unitInAttack = []
        self.enemyInAttack = []
        self.trunc = False

        self.enemyCP = 0
        self.modelCP = 0

        self.enemyOverwatch = -1
        self.modelStrat = {"overwatch": -1, "smokescreen": -1}
        self.enemyStrat = {"overwatch": -1, "smokescreen": -1}

        self.modelVP = 0
        self.enemyVP = 0
        self.numTurns = 0

        self.coordsOfOM = np.array([
            [self.b_len/2 + 8, self.b_hei/2 + 12],
            [self.b_len/2 - 8, self.b_hei/2 + 12],
            [self.b_len/2 + 8, self.b_hei/2 - 12],
            [self.b_len/2 - 8, self.b_hei/2 - 12],
        ])
        self.modelOnOM = np.array([-1, -1, -1, -1])
        self.enemyOnOM = np.array([-1, -1, -1, -1])

        self.modelOC = []
        self.enemyOC = []
        self.relic = 3
        forced_vic_cond = _get_forced_victory_condition()
        self.vicCond = forced_vic_cond if forced_vic_cond else dice(max=3)   # Slay and Secure, Ancient Relic, Domination
        self.modelUpdates = ""

        if self.trunc is True:
            if self.vicCond == 1:
                print("Victory Condition rolled: Slay and Secure")
            elif self.vicCond == 2:
                print("Victory Condition rolled: Ancient Relic")
            elif self.vicCond == 3:
                print("Victory Condition rolled: Domination")

        for i in range(len(enemy)):
            self.enemy_weapon.append(enemy[i].showWeapon())
            self.enemy_melee.append(enemy[i].showMelee())
            self.enemy_data.append(enemy[i].showUnitData())
            self.enemy_coords.append([enemy[i].showCoords()[0], enemy[i].showCoords()[1]])
            self.enemy_health.append(enemy[i].showUnitData()["W"] * enemy[i].showUnitData()["#OfModels"])
            self.enemyInAttack.append([0, 0])
            self.enemyOC.append(enemy[i].showUnitData()["OC"])

        for i in range(len(model)):
            self.unit_weapon.append(model[i].showWeapon())
            self.unit_melee.append(model[i].showMelee())
            self.unit_data.append(model[i].showUnitData())
            self.unit_coords.append([model[i].showCoords()[0], model[i].showCoords()[1]])
            self.unit_health.append(model[i].showUnitData()["W"] * model[i].showUnitData()["#OfModels"])
            self.unitInAttack.append([0, 0])
            self.modelOC.append(model[i].showUnitData()["OC"])

        obsSpace = (len(model) * 3) + (len(enemy) * 3) + len(self.coordsOfOM * 2) + 2
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(obsSpace,), dtype=np.float32)

    def get_info(self):
        return {
            "model health": self.unit_health,
            "player health": self.enemy_health,
            "modelCP": self.modelCP,
            "playerCP": self.enemyCP,
            "in attack": self.unitInAttack,
            "model VP": self.modelVP,
            "player VP": self.enemyVP,
            "victory condition": self.vicCond,
            "turn": self.numTurns,
        }

    def reset(self, m, e, playType=False, Type="small", trunc=False):
        # keep original references too
        self.model = m
        self.enemy = e

        self.iter = 0
        self.trunc = trunc
        self.playType = playType

        if Type == "small":
            self.restarts += 1
        elif Type == "big":
            self.restarts = 0
            savePath = "display/"
            if os.path.isdir(savePath):
                for fil in os.listdir(savePath):
                    try:
                        os.remove(os.path.join(savePath, fil))
                    except Exception:
                        pass

        self.board = np.zeros((self.b_len, self.b_hei))
        self.enemy_coords = []
        self.unit_coords = []
        self.enemy_health = []
        self.unit_health = []
        self.enemyInAttack = []
        self.unitInAttack = []
        self.unitCharged = [0] * len(self.unit_health)
        self.enemyCharged = [0] * len(self.enemy_health)


        self.modelCP = 0
        self.enemyCP = 0
        self.modelVP = 0
        self.enemyVP = 0
        self.numTurns = 0

        forced_vic_cond = _get_forced_victory_condition()
        self.vicCond = forced_vic_cond if forced_vic_cond else dice(max=3)
        self.modelUpdates = ""

        for i in range(len(self.enemy_data)):
            self.enemy_coords.append([e[i].showCoords()[0], e[i].showCoords()[1]])
            self.enemy_health.append(self.enemy_data[i]["W"] * self.enemy_data[i]["#OfModels"])
            self.enemyInAttack.append([0, 0])

        for i in range(len(self.unit_data)):
            self.unit_coords.append([m[i].showCoords()[0], m[i].showCoords()[1]])
            self.unit_health.append(self.unit_data[i]["W"] * self.unit_data[i]["#OfModels"])
            self.unitInAttack.append([0, 0])

        self.game_over = False
        self.current_action_index = 0
        info = self.get_info()

        if Type == "big":
            self.updateBoard()

        return self._get_observation(), info

    def enemyTurn(self, trunc=False):
        # новый ход врага -> сброс “charged this turn”
        self.unitCharged = [0] * len(self.unit_health)
        self.enemyCharged = [0] * len(self.enemy_health)
        if trunc is True:
            self.trunc = True

        self.enemyCP += 1
        self.modelCP += 1
        self.numTurns += 1

        cp_on = np.random.randint(0, len(self.enemy_health))
        use_cp = np.random.randint(0, 5)

        for i in range(len(self.enemy_health)):
            enemyName = i + 21
            battleSh = False

            if isBelowHalfStr(self.enemy_data[i], self.enemy_health[i]) is True and self.unit_health[i] > 0:
                if trunc is False:
                    print("This unit is Below Half Strength, starting test...")
                    print("Rolling 2D6...")
                diceRoll = dice(num=2)
                if trunc is False:
                    print("Player rolled", diceRoll[0], diceRoll[1])
                if sum(diceRoll) >= self.enemy_data[i]["Ld"]:
                    if trunc is False:
                        print("Battle-shock test passed!")
                        self.enemyOC[i] = self.enemy_data[i]["OC"]
                else:
                    battleSh = True
                    self.enemyOC[i] = 0
                    if trunc is False:
                        print("Battle-shock test failed")
                    if use_cp == 1 and cp_on == i and self.enemyCP - 1 >= 0:
                        battleSh = False
                        self.enemyCP -= 1
                        self.enemyOC[i] = self.enemy_data[i]["OC"]

            # Heroic Intervention (enemy)
            if use_cp == 4 and cp_on == i:
                if self.enemyCP - 2 >= 0 and self.enemyInAttack[i][0] == 0:
                    for j in range(len(self.unitInAttack)):
                        if self.unitInAttack[j][0] == 1 and distance(self.enemy_coords[i], self.unit_coords[j]) >= 6:
                            self.enemyInAttack[i][0] = 1
                            self.enemyInAttack[i][1] = j

                            self.enemyInAttack[self.enemyInAttack[j][1]][0] = 0
                            self.enemyInAttack[self.enemyInAttack[j][1]][1] = 0

                            self.enemy_coords[i][0] = self.enemy_coords[j][0] + 1
                            self.enemy_coords[i][1] = self.enemy_coords[j][1] + 1
                            self.enemy_coords[i] = bounds(self.unit_coords[i], self.b_len, self.b_hei)

                            self.unitInAttack[j][1] = i
                            self.enemyCP -= 2
                            break

            if self.enemyInAttack[i][0] == 0 and self.enemy_health[i] > 0:
                # follow random alive model unit
                aliveUnits = []
                for j in range(len(self.unit_health)):
                    if self.unit_health[j] > 0:
                        aliveUnits.append(j)
                if len(aliveUnits) == 0:
                    break
                idOfM = np.random.choice(aliveUnits)

                base_m = self.enemy_data[i]["Movement"]
                dist_to_target = distance(self.unit_coords[idOfM], self.enemy_coords[i])
                advanced = dist_to_target > (base_m + 6)

                if advanced:
                    movement = base_m + dice()
                else:
                    movement = base_m

                if distance(self.unit_coords[idOfM], [self.enemy_coords[i][0], self.enemy_coords[i][1] - movement]) < distance(self.unit_coords[idOfM], self.enemy_coords[i]):
                    self.enemy_coords[i][1] -= movement
                elif distance(self.unit_coords[idOfM], [self.enemy_coords[i][0], self.enemy_coords[i][1] + movement]) < distance(self.unit_coords[idOfM], self.enemy_coords[i]):
                    self.enemy_coords[i][1] += movement
                elif distance(self.unit_coords[idOfM], [self.enemy_coords[i][0] - movement, self.enemy_coords[i][1]]) < distance(self.unit_coords[idOfM], self.enemy_coords[i]):
                    self.enemy_coords[i][0] -= movement
                elif distance(self.unit_coords[idOfM], [self.enemy_coords[i][0] + movement, self.enemy_coords[i][1]]) < distance(self.unit_coords[idOfM], self.enemy_coords[i]):
                    self.enemy_coords[i][0] += movement

                # bounds + collision
                self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                for j in range(len(self.unit_health)):
                    if self.enemy_coords[i] == self.unit_coords[j]:
                        self.enemy_coords[i][0] -= 1

                # Fight Phase (10e simplified)
                self.resolve_fight_phase(active_side="enemy", trunc=trunc)

                # model overwatch reaction
                if self.modelStrat["overwatch"] != -1:
                    if self.unit_weapon[self.modelStrat["overwatch"]] != "None":
                        if distance(self.enemy_coords[i], self.unit_coords[self.modelStrat["overwatch"]]) <= self.unit_weapon[self.modelStrat["overwatch"]]["Range"]:
                            _logger = None
                            if trunc is False and _verbose_logs_enabled():
                                _logger = RollLogger(auto_dice)
                                dmg, modHealth = attack(
                                    self.unit_health[self.modelStrat["overwatch"]],
                                    self.unit_weapon[self.modelStrat["overwatch"]],
                                    self.unit_data[self.modelStrat["overwatch"]],
                                    self.enemy_health[i],
                                    self.enemy_data[i],
                                    distance_to_target=distance(self.enemy_coords[i], self.unit_coords[self.modelStrat["overwatch"]]),
                                    roller=_logger.roll,
                                )
                            else:
                                dmg, modHealth = attack(
                                    self.unit_health[self.modelStrat["overwatch"]],
                                    self.unit_weapon[self.modelStrat["overwatch"]],
                                    self.unit_data[self.modelStrat["overwatch"]],
                                    self.enemy_health[i],
                                    self.enemy_data[i],
                                    distance_to_target=distance(self.enemy_coords[i], self.unit_coords[self.modelStrat["overwatch"]]),
                                )
                            self.enemy_health[i] = modHealth
                            if trunc is False and _logger is not None:
                                print("\n🟦 Model Overwatch (подробно):")
                                _logger.print_shoot_report(
                                    weapon=self.unit_weapon[self.modelStrat["overwatch"]],
                                    attacker_data=self.unit_data[self.modelStrat["overwatch"]],
                                    defender_data=self.enemy_data[i],
                                    dmg_list=dmg,
                                    effect=None,
                                )
                            self.modelStrat["overwatch"] = -1

                # set overwatch
                if use_cp == 2 and cp_on == i and self.enemyCP - 1 >= 0 and battleSh is False:
                    self.enemyCP -= 1
                    self.enemyStrat["overwatch"] = i

                # Shooting phase (if applicable)
                if self.enemy_weapon[i] != "None":
                    if advanced and not weapon_is_assault(self.enemy_weapon[i]):
                        if trunc is False:
                            print("Enemy advanced — non-Assault weapon, skipping shooting")
                    else:
                        shootAbleUnits = []
                        for j in range(len(self.unit_health)):
                            if distance(self.enemy_coords[i], self.unit_coords[j]) <= self.enemy_weapon[i]["Range"] and self.unit_health[j] > 0 and self.unitInAttack[j][0] == 0:
                                shootAbleUnits.append(j)

                        if len(shootAbleUnits) > 0:
                            idOfM = np.random.choice(shootAbleUnits)
                            if self.modelStrat["smokescreen"] != -1 and self.modelStrat["smokescreen"] == idOfM:
                                self.modelStrat["smokescreen"] = -1
                                effect = "benefit of cover"
                            else:
                                effect = None

                            dmg, modHealth = attack(
                                self.enemy_health[i],
                                self.enemy_weapon[i],
                                self.enemy_data[i],
                                self.unit_health[idOfM],
                                self.unit_data[idOfM],
                                effects=effect,
                                distance_to_target=distance(self.enemy_coords[i], self.unit_coords[idOfM]),
                            )
                            self.unit_health[idOfM] = modHealth
                            if trunc is False:
                                print("Enemy Unit", enemyName, "shoots Model Unit", idOfM + 11, float(np.sum(dmg)), "damage")

                # Charging (if applicable)
                if advanced:
                    if trunc is False:
                        print("Enemy advanced — cannot charge, skipping charge")
                else:
                    chargeAble = []
                    diceRoll = sum(dice(num=2))
                    for j in range(len(self.unit_health)):
                        if distance(self.enemy_coords[i], self.unit_coords[j]) <= 12 and self.unitInAttack[j][0] == 0:
                            if distance(self.enemy_coords[i], self.unit_coords[j]) - diceRoll <= 5:
                                chargeAble.append(j)

                    if len(chargeAble) > 0:
                        # Выбираем цель для чарджа
                        idOfM = int(np.random.choice(chargeAble))

                        # 10e: успех, если 2D6 >= (distance - 1")
                        dist = distance(self.enemy_coords[i], self.unit_coords[idOfM])
                        required = max(0, dist - 1)

                        # diceRoll ты уже кинул выше, поэтому используем его
                        if diceRoll >= required:
                            if trunc is False:
                                print("Enemy unit", enemyName, "successfully charged Model unit", idOfM + 11,
                                      f"(roll {diceRoll} vs need {required:.1f})")

                            # Ставим врага в пределах 1" (упрощённо: рядом по оси X)
                            # Делаем так, чтобы distance <= 1
                            self.enemy_coords[i][0] = self.unit_coords[idOfM][0] + 1
                            self.enemy_coords[i][1] = self.unit_coords[idOfM][1]
                            self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)

                            # Помечаем, что они в бою (Engagement)
                            self.enemyInAttack[i][0] = 1
                            self.enemyInAttack[i][1] = idOfM

                            self.unitInAttack[idOfM][0] = 1
                            self.unitInAttack[idOfM][1] = i
                            self.enemyCharged[i] = 1


                            # ВАЖНО: урон НЕ наносим сейчас. Урон будет в Fight Phase.
                            # Нужно также пометить "charged this turn" для приоритета.
                            # Если у тебя нет массива, добавь:
                            # self.enemyCharged[i] = 1
                        else:
                            if trunc is False:
                                print("Enemy unit", enemyName, "failed charge vs Model unit", idOfM + 11,
                                      f"(roll {diceRoll} vs need {required:.1f})")


                if use_cp == 3 and cp_on == i and self.enemyCP - 1 >= 0 and battleSh is False:
                    self.enemyCP -= 1
                    self.enemyStrat["smokescreen"] = i

                for j in range(len(self.coordsOfOM)):
                    if distance(self.coordsOfOM[j], self.enemy_coords[i]) <= 5:
                        self.enemyOnOM[j] = i

            elif self.enemyInAttack[i][0] == 1 and self.enemy_health[i] > 0:
                decide = np.random.randint(0, 10)
                idOfM = self.enemyInAttack[i][1]
                if decide == 5:
                    if trunc is False:
                        print("Enemy unit", enemyName, "pulled out of fight with Model unit", idOfM + 11)

                    if battleSh is True:
                        diceRoll = dice()
                        if diceRoll < 3:
                            self.enemy_health[i] -= self.enemy_data[i]["W"]

                    self.enemy_coords[i][0] -= self.enemy_data[i]["Movement"]
                    self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                    self.unitInAttack[idOfM][0] = 0
                    self.unitInAttack[idOfM][1] = 0

                    self.enemyInAttack[i][0] = 0
                    self.enemyInAttack[i][1] = 0
                else:
                    if self.unit_health[idOfM] > 0:
                        dmg, modHealth = attack(
                            self.enemy_health[i],
                            self.enemy_melee[i],
                            self.enemy_data[i],
                            self.unit_health[idOfM],
                            self.unit_data[idOfM],
                            rangeOfComb="Melee",
                        )
                        self.unit_health[idOfM] = modHealth
                    else:
                        self.unitInAttack[idOfM][0] = 0
                        self.unitInAttack[idOfM][1] = 0

                        self.enemyInAttack[i][0] = 0
                        self.enemyInAttack[i][1] = 0

        if self.modelStrat["overwatch"] != -1:
            self.modelStrat["overwatch"] = -1
        if self.modelStrat["smokescreen"] != -1:
            self.modelStrat["smokescreen"] = -1

        for i in range(len(self.enemyOnOM)):
            if self.enemyOnOM[i] != -1 and self.modelOnOM[i] != -1:
                if self.enemyOC[self.enemyOnOM[i]] > self.modelOC[self.modelOnOM[i]]:
                    self.enemyVP += 1
            elif self.enemyOnOM[i] != -1:
                self.enemyVP += 1

    def resolve_fight_phase(self, active_side: str, trunc=None):
        """
        10e simplified Fight Phase:
        1) Chargers (charged this turn) fight first (active side only in this simplified model)
        2) Then alternate fights starting with the NON-active side
        Only units within Engagement (unitInAttack/enemyInAttack) can fight.
        No pile-in/consolidate here (упрощение).
        """
        quiet = self.trunc if trunc is None else trunc

        # кто кидает кубы (если MANUAL_DICE=1 — спрашиваем руками)
        dice_fn = player_dice if os.getenv("MANUAL_DICE", "0") == "1" else auto_dice

        def _log(msg: str):
            if quiet is False:
                print(msg)

        def _do_melee(att_side: str, att_idx: int):
            """
            att_side: "model" (self.unit_*) or "enemy" (self.enemy_*)
            att_idx: index in corresponding arrays
            """
            # проверка жив/в бою
            if att_side == "model":
                if self.unit_health[att_idx] <= 0 or self.unitInAttack[att_idx][0] != 1:
                    return False
                def_idx = self.unitInAttack[att_idx][1]
                if def_idx < 0 or def_idx >= len(self.enemy_health) or self.enemy_health[def_idx] <= 0:
                    # цель мертва/невалидна — снимаем бой
                    self.unitInAttack[att_idx] = [0, 0]
                    return False

                weapon = self.unit_melee[att_idx]
                attacker_data = self.unit_data[att_idx]
                defender_data = self.enemy_data[def_idx]
                hp_before = self.enemy_health[def_idx]

                _logger = None
                if quiet is False and _verbose_logs_enabled():
                    _logger = RollLogger(auto_dice)
                    _logger.configure_for_weapon(weapon)
                    dmg, modHealth = attack(
                        self.unit_health[att_idx],
                        weapon,
                        attacker_data,
                        self.enemy_health[def_idx],
                        defender_data,
                        rangeOfComb="Melee",
                        roller=_logger.roll,
                    )
                else:
                    dmg, modHealth = attack(
                        self.unit_health[att_idx],
                        weapon,
                        attacker_data,
                        self.enemy_health[def_idx],
                        defender_data,
                        rangeOfComb="Melee",
                    )

                self.enemy_health[def_idx] = modHealth

                wname = weapon.get("Name", "Melee") if isinstance(weapon, dict) else str(weapon)
                _log(f"⚔️ Model Unit {att_idx + 21} fights Enemy Unit {def_idx + 11} with {wname}: dmg {float(np.sum(dmg))} | HP {hp_before} -> {modHealth}")

                # если у тебя уже есть print_melee_report — можно включить:
                if quiet is False and _logger is not None and hasattr(_logger, "print_melee_report"):
                    _logger.print_melee_report(
                        weapon=weapon,
                        attacker_data=attacker_data,
                        defender_data=defender_data,
                        dmg_list=dmg,
                        effect=None,
                    )

                # если цель умерла — снимаем “в бою” с обеих сторон
                if self.enemy_health[def_idx] <= 0:
                    self.enemyInAttack[def_idx] = [0, 0]
                    self.unitInAttack[att_idx] = [0, 0]

                return True

            else:  # att_side == "enemy"
                if self.enemy_health[att_idx] <= 0 or self.enemyInAttack[att_idx][0] != 1:
                    return False
                def_idx = self.enemyInAttack[att_idx][1]
                if def_idx < 0 or def_idx >= len(self.unit_health) or self.unit_health[def_idx] <= 0:
                    self.enemyInAttack[att_idx] = [0, 0]
                    return False

                weapon = self.enemy_melee[att_idx]
                attacker_data = self.enemy_data[att_idx]
                defender_data = self.unit_data[def_idx]
                hp_before = self.unit_health[def_idx]

                _logger = None
                if quiet is False and _verbose_logs_enabled():
                    _logger = RollLogger(dice_fn)
                    _logger.configure_for_weapon(weapon)
                    dmg, modHealth = attack(
                        self.enemy_health[att_idx],
                        weapon,
                        attacker_data,
                        self.unit_health[def_idx],
                        defender_data,
                        rangeOfComb="Melee",
                        roller=_logger.roll,
                    )
                else:
                    dmg, modHealth = attack(
                        self.enemy_health[att_idx],
                        weapon,
                        attacker_data,
                        self.unit_health[def_idx],
                        defender_data,
                        rangeOfComb="Melee",
                    )

                self.unit_health[def_idx] = modHealth

                wname = weapon.get("Name", "Melee") if isinstance(weapon, dict) else str(weapon)
                _log(f"⚔️ Enemy Unit {att_idx + 11} fights Model Unit {def_idx + 21} with {wname}: dmg {float(np.sum(dmg))} | HP {hp_before} -> {modHealth}")

                if quiet is False and _logger is not None and hasattr(_logger, "print_melee_report"):
                    _logger.print_melee_report(
                        weapon=weapon,
                        attacker_data=attacker_data,
                        defender_data=defender_data,
                        dmg_list=dmg,
                        effect=None,
                    )

                if self.unit_health[def_idx] <= 0:
                    self.unitInAttack[def_idx] = [0, 0]
                    self.enemyInAttack[att_idx] = [0, 0]

                return True

        # есть ли вообще кому драться?
        any_fight = any(x[0] == 1 for x in self.unitInAttack) or any(x[0] == 1 for x in self.enemyInAttack)
        if not any_fight:
            return

        if quiet is False:
            print("\n⚔️ ===== FIGHT PHASE =====")

        fought_model = set()
        fought_enemy = set()

        # 1) chargers fight first (упрощение: только активная сторона)
        if active_side == "model":
            chargers = [i for i in range(len(self.unit_health))
                        if self.unitCharged[i] == 1 and self.unitInAttack[i][0] == 1 and self.unit_health[i] > 0]
            for i in chargers:
                if i not in fought_model:
                    if _do_melee("model", i):
                        fought_model.add(i)
        else:
            chargers = [i for i in range(len(self.enemy_health))
                        if self.enemyCharged[i] == 1 and self.enemyInAttack[i][0] == 1 and self.enemy_health[i] > 0]
            for i in chargers:
                if i not in fought_enemy:
                    if _do_melee("enemy", i):
                        fought_enemy.add(i)

        # 2) then alternate, starting with NON-active side
        next_side = "enemy" if active_side == "model" else "model"

        while True:
            model_left = [i for i in range(len(self.unit_health))
                          if self.unit_health[i] > 0 and self.unitInAttack[i][0] == 1 and i not in fought_model]
            enemy_left = [i for i in range(len(self.enemy_health))
                          if self.enemy_health[i] > 0 and self.enemyInAttack[i][0] == 1 and i not in fought_enemy]

            if not model_left and not enemy_left:
                break

            if next_side == "model":
                if model_left:
                    i = model_left[0]
                    _do_melee("model", i)
                    fought_model.add(i)
                next_side = "enemy"
            else:
                if enemy_left:
                    i = enemy_left[0]
                    _do_melee("enemy", i)
                    fought_enemy.add(i)
                next_side = "model"

        # после Fight Phase — charged сбрасываем (на всякий)
        self.unitCharged = [0] * len(self.unit_health)
        self.enemyCharged = [0] * len(self.enemy_health)

        if quiet is False:
            print("⚔️ ===== END FIGHT PHASE =====\n")



    def step(self, action):
        reward = 0
        self.unitCharged = [0] * len(self.unit_health)
        self.enemyCharged = [0] * len(self.enemy_health)
        self.enemyCP += 1
        self.modelCP += 1
        effect = None
        res = 0

        for i in range(len(self.unit_health)):
            modelName = i + 21
            battleSh = False

            if isBelowHalfStr(self.unit_data[i], self.unit_health[i]) is True and self.unit_health[i] > 0:
                if self.trunc is False:
                    print("This unit is Battle-shocked, starting test...")
                    print("Rolling 2D6...")
                diceRoll = dice(num=2)
                if self.trunc is False:
                    print("Model rolled", diceRoll[0], diceRoll[1])
                if sum(diceRoll) >= self.unit_data[i]["Ld"]:
                    self.modelOC[i] = self.unit_data[i]["OC"]
                    if self.trunc is False:
                        print("Battle-shock test passed!")
                else:
                    battleSh = True
                    if self.trunc is False:
                        print("Battle-shock test failed")
                    self.modelOC[i] = 0
                    if action["use_cp"] == 1 and action["cp_on"] == i:
                        if self.modelCP - 1 >= 0:
                            battleSh = False
                            reward += 0.5
                            self.modelCP -= 1
                            if self.trunc is False:
                                print("Used Insane Bravery Stratagem to pass Battle Shock test")
                        else:
                            reward -= 0.5

            # Heroic Intervention
            if action["use_cp"] == 4 and action["cp_on"] == i:
                if self.modelCP - 2 >= 0 and self.unitInAttack[i][0] == 0:
                    for j in range(len(self.enemyInAttack)):
                        if self.enemyInAttack[j][0] == 1 and distance(self.unit_coords[i], self.enemy_coords[j]) >= 6:
                            self.unitInAttack[i][0] = 1
                            self.unitInAttack[i][1] = j

                            self.unitInAttack[self.enemyInAttack[j][1]][0] = 0
                            self.unitInAttack[self.enemyInAttack[j][1]][1] = 0

                            self.unit_coords[i][0] = self.enemy_coords[j][0] + 1
                            self.unit_coords[i][1] = self.enemy_coords[j][1] + 1
                            self.unit_coords[i] = bounds(self.unit_coords[i], self.b_len, self.b_hei)

                            self.enemyInAttack[j][1] = i
                            self.modelCP -= 2
                            reward += 0.5
                            break
                    reward += 0.5
                else:
                    reward -= 0.5

            if self.unitInAttack[i][0] == 0 and self.unit_health[i] > 0:
                base_m = self.unit_data[i]["Movement"]
                label = "move_num_" + str(i)
                want = int(action[label])

                advanced = (action["move"] != 4) and (want > base_m)

                if advanced:
                    max_move = base_m + dice()
                else:
                    max_move = base_m

                movement = min(want, max_move)

                if action["move"] == 0:  # down
                    self.unit_coords[i][0] += movement
                elif action["move"] == 1:  # up
                    self.unit_coords[i][0] -= movement
                elif action["move"] == 2:  # left
                    self.unit_coords[i][1] -= movement
                elif action["move"] == 3:  # right
                    self.unit_coords[i][1] += movement
                elif action["move"] == 4:  # no move
                    for j in range(len(self.coordsOfOM)):
                        if distance(self.unit_coords[i], self.coordsOfOM[j]) <= 5:
                            reward += 0.5
                        else:
                            reward -= 0.5

                if self.trunc is False:
                    if action["move"] == 0:
                        print("Model unit", modelName, "moved", movement, "inches downward")
                    elif action["move"] == 1:
                        print("Model unit", modelName, "moved", movement, "inches upward")
                    elif action["move"] == 2:
                        print("Model unit", modelName, "moved", movement, "inches left")
                    elif action["move"] == 3:
                        print("Model unit", modelName, "moved", movement, "inches right")
                    elif action["move"] == 4:
                        print("Model unit", modelName, "did not move")

                # bounds + collision
                self.unit_coords[i] = bounds(self.unit_coords[i], self.b_len, self.b_hei)
                for j in range(len(self.enemy_health)):
                    if self.unit_coords[i] == self.enemy_coords[j]:
                        self.unit_coords[i][0] -= 1

                # enemy overwatch reaction
                if self.enemyStrat["overwatch"] != -1 and self.enemy_weapon[self.enemyStrat["overwatch"]] != "None":
                    if distance(self.unit_coords[i], self.enemy_coords[self.enemyStrat["overwatch"]]) <= self.enemy_weapon[self.enemyStrat["overwatch"]]["Range"]:
                        dmg, modHealth = attack(
                            self.enemy_health[self.enemyStrat["overwatch"]],
                            self.enemy_weapon[self.enemyStrat["overwatch"]],
                            self.enemy_data[self.enemyStrat["overwatch"]],
                            self.unit_health[i],
                            self.unit_data[i],
                            distance_to_target=distance(self.unit_coords[i], self.enemy_coords[self.enemyStrat["overwatch"]]),
                        )
                        self.unit_health[i] = modHealth
                        if self.trunc is False:
                            print(
                                "Player unit",
                                self.enemyStrat["overwatch"] + 11,
                                "successfully hit model unit",
                                i + 11,
                                "for",
                                sum(dmg),
                                "damage using the overwatch strategem",
                            )
                        self.enemyStrat["overwatch"] = -1

                if action["use_cp"] == 2 and action["cp_on"] == i:
                    if self.modelCP - 1 >= 0 and self.enemy_weapon[i] != "None":
                        self.modelCP -= 1
                        self.modelStrat["overwatch"] = i
                        reward += 0.5
                    elif battleSh is not False:
                        if self.trunc is False:
                            print("This unit is BattleShocked, no stratagems can be used on it")
                    else:
                        reward -= 1

                # shooting phase (if eligible)
                if self.unit_weapon[i] != "None":
                    if advanced and not weapon_is_assault(self.unit_weapon[i]):
                        if self.trunc is False:
                            print("Model advanced — non-Assault weapon, skipping shooting")
                    else:
                        shootAbleUnits = []
                        for j in range(len(self.enemy_health)):
                            if distance(self.unit_coords[i], self.enemy_coords[j]) <= self.unit_weapon[i]["Range"] and self.enemy_health[j] > 0 and self.enemyInAttack[j][0] == 0:
                                shootAbleUnits.append(j)

                        if len(shootAbleUnits) > 0:
                            idOfE = action["shoot"]
                            if idOfE in shootAbleUnits:
                                if idOfE == self.enemyStrat["smokescreen"]:
                                    effect = "benefit of cover"

                                _logger = None
                                if self.trunc is False and _verbose_logs_enabled():
                                    _logger = RollLogger(auto_dice)
                                    dmg, modHealth = attack(
                                        self.unit_health[i],
                                        self.unit_weapon[i],
                                        self.unit_data[i],
                                        self.enemy_health[idOfE],
                                        self.enemy_data[idOfE],
                                        effects=effect,
                                        distance_to_target=distance(self.unit_coords[i], self.enemy_coords[idOfE]),
                                        roller=_logger.roll,
                                    )
                                else:
                                    dmg, modHealth = attack(
                                        self.unit_health[i],
                                        self.unit_weapon[i],
                                        self.unit_data[i],
                                        self.enemy_health[idOfE],
                                        self.enemy_data[idOfE],
                                        effects=effect,
                                        distance_to_target=distance(self.unit_coords[i], self.enemy_coords[idOfE]),
                                    )
                                self.enemy_health[idOfE] = modHealth
                                reward += 0.2
                                if self.trunc is False:
                                    
                                    print("Model Unit", modelName, "shoots Enemy Unit", idOfE + 11, float(np.sum(dmg)), "damage")
                                else:
                                    self.modelUpdates += "Model Unit {} shoots Enemy Unit {} {} times\n".format(modelName, idOfE + 11, sum(dmg))
                                if self.trunc is False and _logger is not None:
                                    _logger.print_shoot_report(
                                        weapon=self.unit_weapon[i],
                                        attacker_data=self.unit_data[i],
                                        defender_data=self.enemy_data[idOfE],
                                        dmg_list=dmg,
                                        effect=effect,
                                    )
                            else:
                                reward -= 0.5
                                if self.trunc is False:
                                    print("Model Unit", modelName, "fails to shoot an Enemy Unit")

                # Charge (if applicable)
                if advanced:
                    if self.trunc is False:
                        print("Model advanced — cannot charge, skipping charge")
                else:
                    chargeAble = []
                    diceRoll = sum(dice(num=2))

                    if action["attack"] == 1:
                        for j in range(len(self.enemy_health)):
                            if distance(self.enemy_coords[j], self.unit_coords[i]) <= 12 and self.enemyInAttack[j][0] == 0 and self.enemy_health[j] > 0:
                                if distance(self.enemy_coords[j], self.unit_coords[i]) - diceRoll <= 5:
                                    chargeAble.append(j)

                    if len(chargeAble) > 0:
                        idOfE = action["charge"]
                        if idOfE in chargeAble:
                            if self.trunc is False:
                                print("Model unit", modelName, "started attack with Enemy unit", idOfE + 11)
                            else:
                                self.modelUpdates += "Model unit {} started attack with Enemy Unit {}\n".format(modelName, idOfE + 11)

                            self.unitInAttack[i][0] = 1
                            self.unitInAttack[i][1] = idOfE

                            self.unit_coords[i][0] = self.enemy_coords[idOfE][0] + 1
                            self.unit_coords[i][1] = self.enemy_coords[idOfE][1] + 1
                            self.unit_coords[i] = bounds(self.unit_coords[i], self.b_len, self.b_hei)

                            self.enemyInAttack[idOfE][0] = 1
                            self.enemyInAttack[idOfE][1] = i
                            self.unitCharged[i] = 1


                            reward += 0.5
                        else:
                            if self.trunc is False:
                                print("Model unit", modelName, "failed to attack Enemy")
                            reward -= 0.5




                # smokescreen
                if action["use_cp"] == 3 and action["cp_on"] == i:
                    if self.modelCP - 1 >= 0:
                        self.modelCP -= 1
                        self.modelStrat["smokescreen"] = i
                        reward += 0.5
                    elif battleSh is not False:
                        if self.trunc is False:
                            print("This unit is Battle shocked, stratagems can not be used")
                    else:
                        reward -= 0.5

                for j in range(len(self.coordsOfOM)):
                    if distance(self.coordsOfOM[j], self.unit_coords[i]) <= 5:
                        reward += 0.5
                        self.modelOnOM[j] = i

            elif self.unitInAttack[i][0] == 1 and self.unit_health[i] > 0:
                idOfE = self.unitInAttack[i][1]

                # Если враг уже мёртв — автоматически выходим из боя
                if self.enemy_health[idOfE] <= 0:
                    reward += 0.3

                    self.unitInAttack[i][0] = 0
                    self.unitInAttack[i][1] = 0

                    self.enemyInAttack[idOfE][0] = 0
                    self.enemyInAttack[idOfE][1] = 0

                else:
                    # ВАЖНО:
                    # В 10e здесь НЕ наносим урон. Урон будет в Fight Phase.
                    #
                    # action["attack"] используем как:
                    # 0 = Fall Back (выйти из боя)
                    # 1 = остаться в Engagement (удар потом в Fight Phase)
                    if action["attack"] == 0:
                        # Fall Back
                        if self.unit_health[i] * 2 >= self.enemy_health[idOfE]:
                            reward -= 0.5

                        if self.trunc is False:
                            print("Model unit", modelName, "pulled out of fight with Enemy unit", idOfE + 11)
                        else:
                            self.modelUpdates += "Model Unit {} pulled out of fight with Enemy unit {}\n".format(modelName, idOfE + 11)

                        # Если battleshock — риск потерь при отступлении (как у тебя было)
                        if battleSh is True:
                            diceRoll = dice()
                            if diceRoll < 3:
                                self.unit_health[i] -= self.unit_data[i]["W"]

                        # Отходим (как у тебя было)
                        self.unit_coords[i][0] += self.unit_data[i]["Movement"]

                        # Снимаем статусы боя
                        self.unitInAttack[i][0] = 0
                        self.unitInAttack[i][1] = 0

                        self.enemyInAttack[idOfE][0] = 0
                        self.enemyInAttack[idOfE][1] = 0

                    else:
                        # Остаёмся в бою — урон будет в Fight Phase (позже)
                        reward += 0.2
                        # (можно вообще без print, чтобы не засорять; оставляем тишину)
                        pass


            elif self.unit_health[i] == 0:
                reward -= 1
                if self.trunc is False:
                    print("Model unit", modelName, "is destroyed")

        # Fight Phase (10e simplified)
        self.resolve_fight_phase(active_side="model")
        self.enemyStrat["overwatch"] = -1
        self.enemyStrat["smokescreen"] = -1

        for i in range(len(self.modelOnOM)):
            if self.enemyOnOM[i] != -1 and self.modelOnOM[i] != -1:
                if self.enemyOC[self.enemyOnOM[i]] < self.modelOC[self.modelOnOM[i]]:
                    self.modelVP += 1
            elif self.modelOnOM[i] != -1:
                self.modelVP += 1

        for i in range(len(self.unit_health)):
            if self.unit_health[i] < 0:
                self.unit_health[i] = 0

        for i in range(len(self.enemy_health)):
            if self.enemy_health[i] < 0:
                self.enemy_health[i] = 0

        # Determine winning team
        if sum(self.unit_health) <= 0:
            self.game_over = True
            reward -= 2
            res = 4
        elif sum(self.enemy_health) <= 0:
            self.game_over = True
            reward += 2
            res = 4

        # Other victory conditions
        if self.numTurns == 10 and self.game_over is not True:
            self.game_over = True
            res = self.vicCond
            if res == 1:
                self.modelVP = 0
                self.enemyVP = 0
                for i in range(len(self.enemyOnOM)):
                    if self.enemyOnOM[i] != -1 and self.modelOnOM[i] != -1:
                        if self.enemyOC[self.enemyOnOM[i]] > self.modelOC[self.modelOnOM[i]]:
                            self.enemyVP += 1
                        elif self.enemyOC[self.enemyOnOM[i]] < self.modelOC[self.modelOnOM[i]]:
                            self.modelVP += 1
                    elif self.enemyOnOM[i] != -1:
                        self.enemyVP += 1
                    elif self.modelOnOM[i] != -1:
                        self.modelVP += 1
                if self.modelVP > self.enemyVP:
                    reward += 2
                else:
                    reward -= 2
            elif res == 2:
                if self.enemyOnOM[self.relic] != -1 and self.modelOnOM[self.relic] != -1:
                    if self.enemyOC[self.enemyOnOM[self.relic]] > self.modelOC[self.modelOnOM[self.relic]]:
                        self.enemyVP += 6
                    elif self.enemyOC[self.enemyOnOM[self.relic]] < self.modelOC[self.modelOnOM[self.relic]]:
                        self.modelVP += 6
                if self.modelVP > self.enemyVP:
                    reward += 2
                else:
                    reward -= 2
            elif res == 3:
                if self.modelVP > self.enemyVP:
                    reward += 2
                else:
                    reward -= 2

        self.iter += 1
        info = self.get_info()
        return self._get_observation(), reward, self.game_over, res, info

    # for a real person playing
    def player(self):
        self.enemyCP += 1
        self.modelCP += 1

        if self.numTurns == 0:
            if self.playType is False:
                if self.vicCond == 1:
                    print("Victory Condition rolled: Slay and Secure")
                elif self.vicCond == 2:
                    print("Victory Condition rolled: Ancient Relic")
                elif self.vicCond == 3:
                    print("Victory Condition rolled: Domination")
            else:
                if self.vicCond == 1:
                    sendToGUI("Victory Condition rolled: Slay and Secure")
                elif self.vicCond == 2:
                    sendToGUI("Victory Condition rolled: Ancient Relic")
                elif self.vicCond == 3:
                    sendToGUI("Victory Condition rolled: Domination")

        if self.playType is False:
            print(self.get_info())
        else:
            info = self.get_info()
            moreInfo = "Model Unit Health: {}, Player Unit Health: {}\nModel CP: {}, Player CP: {}\nModel VP: {}, Player VP: {}\n".format(
                info["model health"], info["player health"], info["modelCP"], info["playerCP"], info["model VP"], info["player VP"]
            )

        if self.playType is not False:
            if self.modelUpdates != "":
                sendToGUI(moreInfo + self.modelUpdates + "\nWould you like to continue: ")
            else:
                sendToGUI(moreInfo + "\nWould you like to continue: ")
            ans = recieveGUI()
            response = False
            while response is False:
                if ans.lower() in ("y", "yes"):
                    response = True
                    self.modelUpdates = ""
                elif ans.lower() in ("n", "no"):
                    self.game_over = True
                    info = self.get_info
                    return self.game_over, info
                else:
                    sendToGUI("Its a yes or no question dude...: ")
                    ans = recieveGUI()

        for i in range(len(self.enemy_health)):
            playerName = i + 11
            if self.playType is False:
                print("For unit", playerName)
            else:
                sendToGUI("For unit {}".format(playerName))

            battleSh = False
            if isBelowHalfStr(self.enemy_data[i], self.enemy_health[i]) is True and self.unit_health[i] > 0:
                if self.playType is False:
                    print("This unit is Battle-shocked, starting test...")
                    print("Rolling 2D6...")
                    diceRoll = player_dice(num=2)
                    print("You rolled", diceRoll[0], diceRoll[1])
                else:
                    diceRoll = player_dice(num=2)
                    sendToGUI("This unit is Battle-shocked, starting test...\nRolling 2D6...\nYou rolled: {} and {}".format(diceRoll[0], diceRoll[1]))

                if sum(diceRoll) >= self.enemy_data[i]["Ld"]:
                    if self.playType is False:
                        print("Battle-shock test passed!")
                    else:
                        sendToGUI("Battle-shock test passed!")
                    self.enemyOC[i] = self.enemy_data[i]["OC"]
                else:
                    battleSh = True
                    if self.playType is False:
                        print("Battle-shock test failed")
                    else:
                        sendToGUI("Battle-shock test failed")

                    response = False
                    self.enemyOC[i] = 0
                    if self.enemyCP - 1 >= 0:
                        if self.playType is False:
                            strat = input("Would you like to use the Insane Bravery Strategem? (y/n): ")
                        else:
                            sendToGUI("Would you like to use the Insane Bravery Strategem for Unit {}? (y/n): ".format(playerName))
                            strat = recieveGUI()

                        while response is False:
                            if strat.lower() in ("y", "yes"):
                                response = True
                                battleSh = False
                                self.enemyCP -= 1
                                self.enemyOC[i] = self.enemy_data[i]["OC"]
                            elif strat.lower() in ("n", "no"):
                                response = True
                            elif strat.lower() == "quit":
                                self.game_over = True
                                info = self.get_info()
                                return self.game_over, info
                            elif strat.lower() in ("?", "help"):
                                if self.playType is False:
                                    print("The Insane Bravery Stratagem costs 1 CP and is used when a unit fails a Battle-Shock Test. If used it treats the unit as if it passed.")
                                    strat = input("Would you like to use the Insane Bravery Stratagem? (y/n): ")
                                else:
                                    sendToGUI("The Insane Bravery Stratagem costs 1 CP and is used when a unit fails a Battle-Shock Test. If used it treats the unit as if it passed.\nWould you like to use the Insane Bravery Stratagem? (y/n): ")
                                    strat = recieveGUI()
                            else:
                                if self.playType is False:
                                    strat = input("Valid answers are: y, yes, n, and no: ")
                                else:
                                    sendToGUI("Valid answers are: y, yes, n, and no: ")
                                    strat = recieveGUI()

            # Heroic Intervention (player)
            if self.enemyCP - 2 >= 0 and self.enemyInAttack[i][0] == 0:
                response = False
                if self.playType is False:
                    strat = input("Would you like to use the Heroic Intervention Stratagem? (y/n): ")
                else:
                    sendToGUI("Would you like to use the Heroic Intervention Stratagem for Unit {}? (y/n): ".format(playerName))
                    strat = recieveGUI()

                while response is False:
                    if strat.lower() in ("y", "yes"):
                        response = True
                        for j in range(len(self.unitInAttack)):
                            if self.unitInAttack[j][0] == 1 and distance(self.enemy_coords[i], self.unit_coords[j]) >= 6:
                                self.enemyInAttack[i][0] = 1
                                self.enemyInAttack[i][1] = j

                                self.enemyInAttack[self.enemyInAttack[j][1]][0] = 0
                                self.enemyInAttack[self.enemyInAttack[j][1]][1] = 0

                                self.enemy_coords[i][0] = self.enemy_coords[j][0] + 1
                                self.enemy_coords[i][1] = self.enemy_coords[j][1] + 1
                                self.enemy_coords[i] = bounds(self.unit_coords[i], self.b_len, self.b_hei)

                                self.unitInAttack[j][1] = i
                                self.enemyCP -= 2

                                if self.playType is False:
                                    print("Heroic Intervention Successfully used!")
                                else:
                                    sendToGUI("Heroic Intervention Successfully used!")
                                break
                    elif strat.lower() in ("n", "no"):
                        response = True
                    elif strat.lower() == "quit":
                        self.game_over = True
                        info = self.get_info
                        return self.game_over, info
                    elif strat.lower() in ("?", "help"):
                        if self.playType is False:
                            print("The Heroic Intervention stratagem allows the player to choose an enemy unit within 6 inches and charge them")
                            strat = input("Would you like to use the Heroic Intervention Stratagem? (y/n): ")
                        else:
                            sendToGUI("The Heroic Intervention stratagem allows the player to choose an enemy unit within 6 inches and charge them\nWould you like to use the Heroic Intervention Stratagem? (y/n): ")
                            strat = recieveGUI()
                    else:
                        if self.playType is False:
                            strat = input("Valid answers are: y, yes, n, and no: ")

                if self.enemyInAttack[i][0] != 1:
                    if self.playType is False:
                        print("Heroic Intervention failed")
                    else:
                        sendToGUI("Heroic Intervention failed")

            if self.enemyInAttack[i][0] == 0 and self.enemy_health[i] > 0:
                self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                for j in range(len(self.enemy_health)):
                    if self.enemy_coords[i] == self.unit_coords[j]:
                        self.enemy_coords[i][0] -= 1

                self.updateBoard()
                self.showBoard()

                if self.playType is False:
                    print("Take a look at board.txt or click the Show Board button in the GUI to view the current board")
                    print("If you would like to end the game type 'quit' into the prompt")
                    dire = input("Enter the direction of movement (up, down, left, right, none (no move)): ")
                else:
                    sendToGUI(
                        "Take a look at board.txt or click the Show Board button in the GUI to view the current board\n"
                        "If you would like to end the game type 'quit' into the prompt\n"
                        "Enter the direction of movement for Unit {} (up, down, left, right, none (no move)): ".format(playerName)
                    )
                    dire = recieveGUI()

                if dire.lower() == "quit":
                    self.game_over = True
                    info = self.get_info()
                    return self.game_over, info

                # ======= FIX: Advance is optional, move distance is exactly what you choose =======
                advanced = False
                move_num = 0

                if dire.lower() != "none":
                    if self.playType is False:
                        adv = input("Advance? (y/n): ").strip().lower()
                        if adv in ("y", "yes"):
                            advanced = True
                            print("Rolling 1 D6 for Advance...")
                            roll = player_dice()
                            print("You rolled a", roll)
                            movement_cap = self.enemy_data[i]["Movement"] + roll
                        else:
                            movement_cap = self.enemy_data[i]["Movement"]

                        move_len = input(f"How many inches would you like to move (0..{movement_cap}): ")
                    else:
                        # GUI branch оставляем максимально похожим на старую логику
                        adv = "y"
                        advanced = True
                        roll = player_dice()
                        movement_cap = self.enemy_data[i]["Movement"] + roll
                        sendToGUI("How many inches would you like to move your unit (Max: {}): ".format(movement_cap))
                        move_len = recieveGUI()

                    response = False
                    while response is False:
                        if is_num(move_len) is True:
                            if int(move_len) <= movement_cap:
                                move_num = int(move_len)
                                response = True
                            else:
                                if self.playType is False:
                                    move_len = input("Not in range, try again: ")
                                else:
                                    sendToGUI("Not in range, try again: ")
                                    move_len = recieveGUI()
                        elif move_len.lower() in ("quit", "q"):
                            self.game_over = True
                            info = self.get_info()
                            return self.game_over, info
                        else:
                            if self.playType is False:
                                move_len = input("Not a number, try again: ")
                            else:
                                sendToGUI("Not a number, try again: ")
                                move_len = recieveGUI()

                # apply movement using move_num (NOT cap)
                response = False
                while response is False:
                    if dire.lower() == "down":
                        self.enemy_coords[i][0] += move_num
                        response = True
                    elif dire.lower() == "up":
                        self.enemy_coords[i][0] -= move_num
                        response = True
                    elif dire.lower() == "left":
                        self.enemy_coords[i][1] -= move_num
                        response = True
                    elif dire.lower() == "right":
                        self.enemy_coords[i][1] += move_num
                        response = True
                    elif dire.lower() == "none":
                        response = True
                    elif dire.lower() == "quit":
                        self.game_over = True
                        info = self.get_info()
                        return self.game_over, info
                    else:
                        if self.playType is False:
                            dire = input("Not a valid response (up, down, left, right): ")
                        else:
                            sendToGUI("Not a valid response (up, down, left, right): ")
                            dire = recieveGUI()
                        response = False

                # bounds + collision
                self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                for j in range(len(self.enemy_health)):
                    if self.enemy_coords[i] == self.unit_coords[j]:
                        self.enemy_coords[i][0] -= 1

                self.updateBoard()
                self.showBoard()

                # Overwatch strat prompt (kept)
                if self.enemyCP - 1 >= 0 and battleSh is False:
                    response = False
                    if self.playType is False:
                        strat = input("Would you like to use the Fire Overwatch Stratagem? (y/n): ")
                    else:
                        sendToGUI("Would you like to use the Fire Overwatch Stratagem? (y/n): ")
                        strat = recieveGUI()

                    while response is False:
                        if strat.lower() in ("y", "yes"):
                            response = True
                            self.enemyStrat["overwatch"] = i
                            self.enemyCP -= 1
                        elif strat.lower() in ("n", "no"):
                            response = True
                        elif strat.lower() in ("?", "help"):
                            if self.playType is False:
                                print("Fire Overwatch costs 1 CP and lets your unit shoot during enemy Movement/Charge (simplified here).")
                                strat = input("Would you like to use the Fire Overwatch Stratagem? (y/n): ")
                            else:
                                sendToGUI("Fire Overwatch costs 1 CP and lets your unit shoot during enemy Movement/Charge (simplified here).\nWould you like to use the Fire Overwatch Stratagem? (y/n): ")
                                strat = recieveGUI()
                        elif strat.lower() == "quit":
                            self.game_over = True
                            info = self.get_info()
                            return self.game_over, info
                        else:
                            if self.playType is False:
                                strat = input("Valid answers are: y, yes, n, and no: ")
                            else:
                                sendToGUI("Valid answers are: y, yes, n, and no: ")
                                strat = recieveGUI()

                # model overwatch reaction
                if self.modelStrat["overwatch"] != -1 and self.unit_weapon[self.modelStrat["overwatch"]] != "None":
                    if distance(self.enemy_coords[i], self.unit_coords[self.modelStrat["overwatch"]]) <= self.unit_weapon[self.modelStrat["overwatch"]]["Range"]:
                        _logger = None
                        if self.playType is False and _verbose_logs_enabled():
                            _logger = RollLogger(auto_dice)
                            dmg, modHealth = attack(
                                self.unit_health[self.modelStrat["overwatch"]],
                                self.unit_weapon[self.modelStrat["overwatch"]],
                                self.unit_data[self.modelStrat["overwatch"]],
                                self.enemy_health[i],
                                self.enemy_data[i],
                                roller=_logger.roll,
                            )
                        else:
                            dmg, modHealth = attack(
                                self.unit_health[self.modelStrat["overwatch"]],
                                self.unit_weapon[self.modelStrat["overwatch"]],
                                self.unit_data[self.modelStrat["overwatch"]],
                                self.enemy_health[i],
                                self.enemy_data[i],
                            )
                        self.enemy_health[i] = modHealth
                        if self.playType is False:
                            print("Model unit", self.modelStrat["overwatch"] + 21, "successfully hit player unit", i + 11, "for", sum(dmg), "damage using the overwatch strategem")
                            if _logger is not None:
                                _logger.print_shoot_report(
                                    weapon=self.unit_weapon[self.modelStrat["overwatch"]],
                                    attacker_data=self.unit_data[self.modelStrat["overwatch"]],
                                    defender_data=self.enemy_data[i],
                                    dmg_list=dmg,
                                    effect=None,
                                )
                        else:
                            sendToGUI("Model unit {} successfully hit player unit {} for {} damage using the overwatch stratagem".format(self.modelStrat["overwatch"] + 21, i + 11, sum(dmg)))
                        self.modelStrat["overwatch"] = -1

                self.updateBoard()
                self.showBoard()

                # ======= Shooting phase (Assault rule after Advance) =======
                if self.enemy_weapon[i] != "None":
                    if self.playType is False:
                        print("Beginning shooting phase!")
                    else:
                        sendToGUI("Beginning shooting phase!")

                    if advanced and not weapon_is_assault(self.enemy_weapon[i]):
                        if self.playType is False:
                            print("You advanced — non-Assault weapon, skipping shooting")
                        else:
                            sendToGUI("You advanced — non-Assault weapon, skipping shooting")
                    else:
                        shootAble = np.array([])
                        for j in range(len(self.unit_health)):
                            if distance(self.enemy_coords[i], self.unit_coords[j]) <= self.enemy_weapon[i]["Range"] and self.unit_health[j] > 0 and self.unitInAttack[j][0] == 0:
                                shootAble = np.append(shootAble, j)

                        if len(shootAble) > 0:
                            response = False
                            while response is False:
                                if self.playType is False:
                                    shoot = input("Select which enemy unit you would like to shoot ({}): ".format(shootAble + 21))
                                else:
                                    sendToGUI("Select which enemy unit you would like to shoot ({}) with Unit {}: ".format(shootAble + 21, playerName))
                                    shoot = recieveGUI()

                                if is_num(shoot) is True and int(shoot) - 21 in shootAble:
                                    idOfE = int(shoot) - 21
                                    if self.modelStrat["smokescreen"] != -1 and self.modelStrat["smokescreen"] == idOfE:
                                        if self.playType is False:
                                            print("Model unit", self.modelStrat["smokescreen"] + 21, "used the Smokescreen Strategem")
                                        else:
                                            sendToGUI("Model unit {} used the Smokescreen Stratagem".format(self.modelStrat["smokescreen"] + 21))
                                        self.modelStrat["smokescreen"] = -1
                                        effect = "benefit of cover"
                                    else:
                                        effect = None

                                    logger = RollLogger(player_dice)

                                    dmg, modHealth = attack(
                                        self.enemy_health[i],
                                        self.enemy_weapon[i],
                                        self.enemy_data[i],
                                        self.unit_health[idOfE],
                                        self.unit_data[idOfE],
                                        effects=effect,
                                        distance_to_target=distance(self.enemy_coords[i], self.unit_coords[idOfE]),
                                        roller=logger.roll,
                                    )

                                    self.unit_health[idOfE] = modHealth
                                    if self.playType is False:
                                        print(f"Player Unit {playerName} нанёс {sum(dmg)} урона по Model Unit {idOfE + 21}")
                                    else:
                                        sendToGUI("Player Unit {} нанёс {} урона по Model Unit {}".format(playerName, sum(dmg), idOfE + 21))

                                    logger.print_shoot_report(
                                        weapon=self.enemy_weapon[i],
                                        attacker_data=self.enemy_data[i],
                                        defender_data=self.unit_data[idOfE],
                                        dmg_list=dmg,
                                        effect=effect,
                                    )
                                    response = True
                                elif shoot == "quit":
                                    self.game_over = True
                                    info = self.get_info()
                                    return self.game_over, info
                                else:
                                    if self.playType is False:
                                        print("Not an available unit")
                                    else:
                                        sendToGUI("Not an available unit")
                else:
                    if self.playType is False:
                        print("No available weapons to shoot")
                    else:
                        sendToGUI("No available weapons to shoot")

                # ======= Charge phase (no charge after Advance) =======
                if self.playType is False:
                    print("Beginning Charge phase!")
                else:
                    sendToGUI("Beginning Charge phase!")

                if advanced:
                    if self.playType is False:
                        print("You advanced — cannot charge, skipping charge")
                    else:
                        sendToGUI("You advanced — cannot charge, skipping charge")
                else:
                    charg = np.array([])
                    for j in range(len(self.unit_health)):
                        if distance(self.unit_coords[j], self.enemy_coords[i]) <= 12 and self.unitInAttack[j][0] == 0 and self.unit_health[j] > 0:
                            charg = np.append(charg, j)

                    if len(charg) > 0:
                        response = False
                        while response is False:
                            if self.playType is False:
                                attk = input("Select which enemy you would like to charge ({}): ".format(charg + 21))
                            else:
                                sendToGUI("Select which enemy you would like to charge ({}) with Unit {}: ".format(charg + 21, playerName))
                                attk = recieveGUI()

                            if is_num(attk) is True and int(attk) - 21 in charg:
                                response = True
                                j = int(attk) - 21
                                if self.playType is False:
                                    print("Rolling 2 D6...")
                                    roll = player_dice(num=2)
                                    print("You rolled a", roll[0], "and", roll[1])
                                else:
                                    sendToGUI("Rolling 2 D6...")
                                    roll = player_dice(num=2)
                                    sendToGUI("You rolled a {} and {}".format(roll[0], roll[1]))

                                if distance(self.enemy_coords[i], self.unit_coords[j]) - sum(roll) <= 5:
                                    if self.playType is False:
                                        print("Player Unit", playerName, "Successfully charged Model Unit", j + 21)
                                    else:
                                        sendToGUI("Player Unit {} Successfully charged Model Unit {}".format(playerName, j + 21))

                                    self.enemyInAttack[i][0] = 1
                                    self.enemyInAttack[i][1] = j

                                    self.enemy_coords[i][0] = self.unit_coords[j][0] + 1
                                    self.enemy_coords[i][1] = self.unit_coords[j][1] + 1
                                    self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)

                                    # 10e: Charge не наносит урон. Урон — в Fight Phase
                                    self.enemyCharged[i] = 1
                                    self.updateBoard()

                                    self.unitInAttack[j][0] = 1
                                    self.unitInAttack[j][1] = i
                                else:
                                    if self.playType is False:
                                        print("Player Unit {} Failed to charge Model Unit {}".format(playerName, j + 21))
                                    else:
                                        sendToGUI("Player Unit {} Failed to charge Model Unit {}".format(playerName, j + 21))

                            elif attk == "quit":
                                self.game_over = True
                                info = self.get_info()
                                return self.game_over, info
                            else:
                                if self.playType is False:
                                    print("Not an available unit")
                                else:
                                    sendToGUI("Not an available unit")
                    else:
                        if self.playType is False:
                            print("No available units to charge")
                        else:
                            sendToGUI("No available units to charge")

                # Smokescreen prompt (kept)
                if self.enemyCP - 1 >= 0 and battleSh is False:
                    response = False
                    if self.playType is False:
                        strat = input("Would you like to use the Smokescreen Stratagem for this unit? (y/n): ")
                    else:
                        sendToGUI("Would you like to use the Smokescreen Stratagem for this unit? (y/n): ")
                        strat = recieveGUI()

                    while response is False:
                        if strat.lower() in ("y", "yes"):
                            self.enemyStrat["smokescreen"] = i
                            response = True
                        elif strat.lower() in ("n", "no"):
                            response = True
                        elif strat.lower() in ("?", "help"):
                            if self.playType is False:
                                print("Smokescreen costs 1 CP and gives benefit of cover / stealth (simplified here).")
                                strat = input("Would you like to use the Smokescreen Stratagem? (y/n): ")
                            else:
                                sendToGUI("Smokescreen costs 1 CP and gives benefit of cover / stealth (simplified here).\nWould you like to use the Smokescreen Stratagem? (y/n): ")
                                strat = recieveGUI()
                        else:
                            if self.playType is False:
                                strat = input("It's a yes or no question dude: ")
                            else:
                                sendToGUI("It's a yes or no question dude: ")
                                strat = recieveGUI()

                for j in range(len(self.coordsOfOM)):
                    if distance(self.coordsOfOM[j], self.enemy_coords[i]) <= 5:
                        self.enemyOnOM[j] = i

            elif self.enemyInAttack[i][0] == 1 and self.enemy_health[i] > 0:
                idOfE = self.enemyInAttack[i][1]
                response = False
                while response is False:
                    if self.playType is False:
                        fallB = input("Would you like Unit {} to fallback? (y/n): ".format(playerName))
                    else:
                        sendToGUI("Would you like Unit {} to fallback? (y/n): ".format(playerName))
                        fallB = recieveGUI()

                    if fallB.lower() in ("n", "no"):
                        response = True

                        # 10e: здесь НЕ атакуем. Атаки происходят в Fight Phase.
                        if self.playType is False:
                            print("Player Unit", playerName, "stays in combat with Model Unit", idOfE + 21, "(will fight in Fight Phase)")
                        else:
                            sendToGUI("Player Unit {} stays in combat with Model Unit {} (will fight in Fight Phase)".format(playerName, idOfE + 21))

                        # Ничего не меняем: они остаются в бою
                        # self.enemyInAttack / self.unitInAttack остаются как есть
                        continue

                        if self.unit_health[idOfE] <= 0:

                            if self.playType is False:
                                print("Model Unit", idOfE + 21, "has been killed")
                            else:
                                sendToGUI("Model Unit {} has been killed".format(idOfE + 21))

                            self.enemyInAttack[i][0] = 0
                            self.enemyInAttack[i][1] = 0
                            self.unitInAttack[idOfE][0] = 0
                            self.unitInAttack[idOfE][1] = 0

                    elif fallB.lower() in ("y", "yes"):
                        response = True
                        if self.playType is False:
                            print("Player Unit", playerName, "fell back from Enemy unit", idOfE + 21)
                        else:
                            sendToGUI("Player Unit {} fell back from Enemy unit {}".format(playerName, idOfE + 21))

                        if battleSh is True:
                            diceRoll = dice()
                            if diceRoll < 3:
                                self.enemy_health[i] -= self.enemy_data[i]["W"]

                        self.enemy_coords[i][0] += self.enemy_data[i]["Movement"]
                        self.enemyInAttack[i][0] = 0
                        self.enemyInAttack[i][1] = 0

                        self.unitInAttack[idOfE][0] = 0
                        self.unitInAttack[idOfE][1] = 0

                    elif fallB.lower() == "quit":
                        self.game_over = True
                        info = self.get_info()
                        return self.game_over, info
                    else:
                        if self.playType is False:
                            fallB = input("It's a yes or no question dude: ")
                        else:
                            sendToGUI("It's a yes or no question dude: ")
                            fallB = recieveGUI()

            elif self.enemy_health[i] == 0:
                if self.playType is False:
                    print("Unit", playerName, "is dead")
                else:
                    sendToGUI("Unit {} is dead".format(playerName))

        if self.modelStrat["overwatch"] != -1:
            self.modelStrat["overwatch"] = -1
        if self.modelStrat["smokescreen"] != -1:
            self.modelStrat["smokescreen"] = -1

        for i in range(len(self.enemyOnOM)):
            if self.enemyOnOM[i] != -1 and self.modelOnOM[i] != -1:
                if self.enemyOC[self.enemyOnOM[i]] > self.modelOC[self.modelOnOM[i]]:
                    self.enemyVP += 1
            elif self.enemyOnOM[i] != -1:
                self.enemyVP += 1

        for k in range(len(self.enemy_health)):
            if self.enemy_health[k] < 0:
                self.enemy_health[k] = 0

        self.iter += 1
        info = self.get_info()
        return self.game_over, info

    def updateBoard(self):
        self.render(mode="test")
        self.board = np.zeros((self.b_len, self.b_hei))

        for i in range(len(self.unit_health)):
            self.unit_coords[i] = bounds(self.unit_coords[i], self.b_len, self.b_hei)
            self.board[self.unit_coords[i][0]][self.unit_coords[i][1]] = 20 + i + 1

        for i in range(len(self.enemy_health)):
            self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
            self.board[self.enemy_coords[i][0]][self.enemy_coords[i][1]] = 10 + i + 1

        for i in range(len(self.coordsOfOM)):
            self.board[int(self.coordsOfOM[i][0])][int(self.coordsOfOM[i][1])] = 3

    def returnBoard(self):
        return self.board

    def render(self, mode='train'):
        fig = plt.figure()
        ax = fig.add_subplot()
        fig.subplots_adjust(top=0.85)

        if mode == 'train':
            title = "Turn " + str(self.iter) + " Lifetime " + str(self.restarts)
        else:
            title = "Turn " + str(self.iter)

        fig.suptitle(title)

        health = "Model Unit health: {}, CP: {}; Enemy Unit health: {}, CP {}\nVP {}".format(
            self.unit_health, self.modelCP, self.enemy_health, self.enemyCP, [self.modelVP, self.enemyVP]
        )
        ax.set_title(health)

        x1 = np.linspace(0, self.b_len, 10)
        y1 = np.zeros(10)
        x2 = np.zeros(10)
        y2 = np.linspace(0, self.b_hei, 10)

        ax.set_ylim(-5, self.b_len + 5)
        ax.set_xlim(-3, self.b_hei * 1.65)
        ax.plot(y1, x1, color="black")
        ax.plot(y2, x2, color="black")
        ax.plot(y1 + self.b_hei, x1, color="black")
        ax.plot(y2, x2 + self.b_len, color="black")

        for i in range(len(self.unit_health)):
            if i == 0:
                ax.plot(self.unit_coords[i][1], self.unit_coords[i][0], 'bo', label="Model Unit")
            else:
                ax.plot(self.unit_coords[i][1], self.unit_coords[i][0], 'bo')

        for i in range(len(self.enemy_coords)):
            if i == 0:
                ax.plot(self.enemy_coords[i][1], self.enemy_coords[i][0], 'go', label="Player Unit")
            else:
                ax.plot(self.enemy_coords[i][1], self.enemy_coords[i][0], 'go')

        for i in range(len(self.coordsOfOM)):
            if i == 0:
                ax.plot(self.coordsOfOM[i][1], self.coordsOfOM[i][0], 'o', color="black", label="Objective Marker(s)")
            elif i == self.relic and self.vicCond == 2:
                ax.plot(self.coordsOfOM[i][1], self.coordsOfOM[i][0], 'o', color="gold", label="Relic")
            else:
                ax.plot(self.coordsOfOM[i][1], self.coordsOfOM[i][0], 'o', color="black")

        ax.legend(loc="right")

        if mode == "train":
            fileName = "display/" + str(self.restarts) + "_" + str(self.iter) + ".png"
        else:
            fileName = "gui/build/img/board.png"
            fig.savefig("gui/img/board.png")

        fig.savefig(fileName)
        ax.cla()
        plt.close()
        return self.board

    def showBoard(self):
        board = self.returnBoard()
        np.savetxt("board.txt", board.astype(int), fmt="%i", delimiter=",")
        self.render(mode="play")

    def close(self):
        pass

    def _get_observation(self):
        obs = []

        for i in range(len(self.unit_health)):
            obs.append(self.unit_health[i])
            obs.append(self.unit_coords[i][0])
            obs.append(self.unit_coords[i][1])

        obs.append(self.modelCP)

        for i in range(len(self.enemy_health)):
            obs.append(self.enemy_health[i])
            obs.append(self.enemy_coords[i][0])
            obs.append(self.enemy_coords[i][1])

        obs.append(self.enemyCP)

        for OM in self.coordsOfOM:
            obs.append(OM[0])
            obs.append(OM[1])

        obs.append(int(self.game_over))
        obs.append(self.vicCond)

        return np.array(obs, dtype=np.float32)
