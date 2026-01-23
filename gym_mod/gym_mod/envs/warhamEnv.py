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
from gym_mod.engine.mission import (
    MISSION_NAME,
    MAX_BATTLE_ROUNDS,
    score_end_of_command_phase,
    apply_end_of_battle,
)
from gym_mod.engine.skills import apply_end_of_command_phase

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


def roll_off_attacker_defender(manual_roll_allowed: bool = False, log_fn=None):
    """
    Roll-off D6 vs D6 to determine Attacker/Defender.
    Enemy uses player_dice only when MANUAL_DICE=1 and manual_roll_allowed is True.
    Model always uses auto_dice.
    """
    manual = os.getenv("MANUAL_DICE", "0") == "1" and manual_roll_allowed
    verbose = os.getenv("VERBOSE_LOGS", "0") == "1"
    while True:
        enemy_roll = player_dice() if manual else auto_dice()
        model_roll = auto_dice()
        if enemy_roll == model_roll:
            continue
        attacker = "enemy" if enemy_roll > model_roll else "model"
        defender = "model" if attacker == "enemy" else "enemy"
        if verbose and log_fn is not None:
            log_fn(
                f"Roll-off Attacker/Defender: enemy={enemy_roll} model={model_roll} -> attacker={attacker}"
            )
        return attacker, defender


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
        self.unitFellBack = []
        self.enemyFellBack = []

        self.modelVP = 0
        self.enemyVP = 0
        self.battle_round = 1
        self.active_side = "enemy"
        self.phase = "command"
        self.numTurns = self.battle_round
        self.turn_order = ["enemy", "model"]
        self._round_banner_shown = False
        self.mission_name = MISSION_NAME

        self.coordsOfOM = np.array([
            [self.b_len/2 + 8, self.b_hei/2 + 12],
            [self.b_len/2 - 8, self.b_hei/2 + 12],
            [self.b_len/2 + 8, self.b_hei/2 - 12],
            [self.b_len/2 - 8, self.b_hei/2 - 12],
        ])
        self.model_obj_oc = np.array([0, 0, 0, 0])
        self.enemy_obj_oc = np.array([0, 0, 0, 0])

        self.modelOC = []
        self.enemyOC = []
        self.modelUpdates = ""

        for i in range(len(enemy)):
            self.enemy_weapon.append(enemy[i].showWeapon())
            self.enemy_melee.append(enemy[i].showMelee())
            self.enemy_data.append(enemy[i].showUnitData())
            self.enemy_coords.append([enemy[i].showCoords()[0], enemy[i].showCoords()[1]])
            self.enemy_health.append(enemy[i].showUnitData()["W"] * enemy[i].showUnitData()["#OfModels"])
            self.enemyInAttack.append([0, 0])
            self.enemyOC.append(enemy[i].showUnitData()["OC"])
        self.enemyFellBack = [False] * len(self.enemy_health)

        for i in range(len(model)):
            self.unit_weapon.append(model[i].showWeapon())
            self.unit_melee.append(model[i].showMelee())
            self.unit_data.append(model[i].showUnitData())
            self.unit_coords.append([model[i].showCoords()[0], model[i].showCoords()[1]])
            self.unit_health.append(model[i].showUnitData()["W"] * model[i].showUnitData()["#OfModels"])
            self.unitInAttack.append([0, 0])
            self.modelOC.append(model[i].showUnitData()["OC"])
        self.unitFellBack = [False] * len(self.unit_health)

        obsSpace = (len(model) * 3) + (len(enemy) * 3) + len(self.coordsOfOM * 2) + 1
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
            "mission": self.mission_name,
            "turn": self.numTurns,
            "battle round": self.battle_round,
            "active side": self.active_side,
            "phase": self.phase,
        }

    def _should_log(self) -> bool:
        verbose = os.getenv("VERBOSE_LOGS", "0") == "1" or os.getenv("MANUAL_DICE", "0") == "1"
        if verbose:
            return True
        return self.trunc is False

    def _log(self, msg: str):
        if not self._should_log():
            return
        if self.playType is True:
            sendToGUI(msg)
        else:
            print(msg)

    def _log_phase(self, side: str, phase: str):
        if not self._should_log():
            return
        phase_title = {
            "command": "Фаза командования!",
            "movement": "Фаза движения!",
            "shooting": "Фаза стрельбы!",
            "charge": "Фаза чарджа!",
            "fight": "Фаза битвы!",
        }.get(phase, f"Фаза {phase}!")
        self._log(f"[{side.upper()}] {phase_title}")

    def _log_unit(self, side: str, unit_id: int, unit_idx: int, msg: str):
        if not self._should_log():
            return
        self._log(f"[{side.upper()}][Unit {unit_id}|idx={unit_idx}] {msg}")

    def _side_label(self, side: str, manual: bool = False) -> str:
        if side == "model":
            return "MODEL"
        if side == "enemy":
            return "PLAYER" if manual else "ENEMY"
        return side.upper()

    def _log_phase_msg(self, side_label: str, phase: str, msg: str):
        if not self._should_log():
            return
        self._log(f"[{side_label}][{phase.upper()}] {msg}")

    def _log_unit_phase(self, side_label: str, phase: str, unit_id: int, unit_idx: int, msg: str):
        if not self._should_log():
            return
        self._log(f"[{side_label}][{phase.upper()}][Unit {unit_id}|idx={unit_idx}] {msg}")

    def _get_input(self, prompt: str) -> str:
        if self.playType is True:
            sendToGUI(prompt)
            return recieveGUI()
        return input(prompt)

    def _prompt_choice(self, prompt: str, allowed: dict, normalize: dict, allow_quit: bool = True):
        allowed_labels = ", ".join(allowed.values())
        while True:
            response = self._get_input(prompt).strip().lower()
            if allow_quit and response in ("quit", "q"):
                return None
            if response in normalize:
                response = normalize[response]
            if response in allowed:
                return response
            self._log(f"Not a valid response ({allowed_labels}): {response}")

    def _prompt_yes_no(self, prompt: str, allow_quit: bool = True):
        normalize = {"y": "yes", "n": "no", "yes": "yes", "no": "no"}
        allowed = {"yes": "yes", "no": "no"}
        response = self._prompt_choice(prompt, allowed, normalize, allow_quit=allow_quit)
        if response is None:
            return None
        return response == "yes"

    def _unit_has_keyword(self, unit_data: dict, keyword: str) -> bool:
        if not unit_data:
            return False
        keyword = keyword.lower()
        for key in ("Keywords", "KeyWords", "Tags", "Abilities", "Rules", "SpecialRules", "Special", "Type", "Faction"):
            value = unit_data.get(key)
            if value is None:
                continue
            if isinstance(value, (list, tuple)):
                if any(keyword in str(v).lower() for v in value):
                    return True
            else:
                if keyword in str(value).lower():
                    return True
        # fallback: check all fields
        for value in unit_data.values():
            if isinstance(value, (list, tuple)):
                if any(keyword in str(v).lower() for v in value):
                    return True
            else:
                if keyword in str(value).lower():
                    return True
        return False

    def _unit_has_smoke(self, unit_data: dict) -> bool:
        return self._unit_has_keyword(unit_data, "smoke")

    def _maybe_use_smokescreen(self, defender_side: str, defender_idx: int, phase: str, manual: bool = False):
        """
        10e Smokescreen: реакция защитника в момент выбора цели для стрельбы.
        Упрощение: проверяем только keyword SMOKE и CP.
        """
        side_label = self._side_label(defender_side, manual=manual)
        if defender_side == "model":
            cp = self.modelCP
            unit_data = self.unit_data[defender_idx]
        else:
            cp = self.enemyCP
            unit_data = self.enemy_data[defender_idx]

        if not self._unit_has_smoke(unit_data):
            return None
        if cp < 1:
            self._log_unit_phase(
                side_label,
                phase,
                defender_idx + (21 if defender_side == "model" else 11),
                defender_idx,
                "Smokescreen недоступен: недостаточно CP.",
            )
            return None

        use_it = True
        if manual:
            strat = self._prompt_yes_no("Использовать Smokescreen (1 CP)? (y/n): ")
            if strat is None:
                self.game_over = True
                return None
            use_it = strat

        if not use_it:
            return None

        if defender_side == "model":
            self.modelCP -= 1
        else:
            self.enemyCP -= 1

        self._log_unit_phase(
            side_label,
            phase,
            defender_idx + (21 if defender_side == "model" else 11),
            defender_idx,
            "Использован Smokescreen: -1 CP, эффект = benefit of cover до конца атаки.",
        )
        return "benefit of cover"

    def _collect_overwatch_candidates(self, defender_side: str, moving_unit_side: str, moving_idx: int):
        if defender_side == "model":
            defender_health = self.unit_health
            defender_coords = self.unit_coords
            defender_weapon = self.unit_weapon
            defender_in_attack = self.unitInAttack
            target_coords = self.enemy_coords if moving_unit_side == "enemy" else self.unit_coords
        else:
            defender_health = self.enemy_health
            defender_coords = self.enemy_coords
            defender_weapon = self.enemy_weapon
            defender_in_attack = self.enemyInAttack
            target_coords = self.unit_coords if moving_unit_side == "model" else self.enemy_coords

        target_pos = target_coords[moving_idx]
        candidates = []
        for i in range(len(defender_health)):
            if defender_health[i] <= 0:
                continue
            if defender_in_attack[i][0] == 1:
                continue
            if defender_weapon[i] == "None":
                continue
            if distance(defender_coords[i], target_pos) <= defender_weapon[i]["Range"]:
                candidates.append(i)
        return candidates

    def _resolve_overwatch(self, defender_side: str, moving_unit_side: str, moving_idx: int, phase: str, manual: bool = False):
        """
        10e Fire Overwatch: реакция защитника после завершения перемещения врага.
        Упрощение: проверяем дальность, не учитываем LOS.
        """
        side_label = self._side_label(defender_side, manual=manual)
        target_label = self._side_label(moving_unit_side, manual=False)
        candidates = self._collect_overwatch_candidates(defender_side, moving_unit_side, moving_idx)
        if not candidates:
            self._log_phase_msg(side_label, phase, "Overwatch невозможен: нет доступных стреляющих юнитов.")
            return

        cp = self.modelCP if defender_side == "model" else self.enemyCP
        if cp < 1:
            self._log_phase_msg(side_label, phase, "Overwatch невозможен: недостаточно CP.")
            return

        self._log_phase_msg(
            side_label,
            phase,
            f"Сработал триггер Overwatch против {target_label} Unit {moving_idx + (21 if moving_unit_side == 'model' else 11)}.",
        )

        use_it = True
        chosen = candidates[0]
        if manual:
            ids = [c + (21 if defender_side == "model" else 11) for c in candidates]
            strat = self._prompt_yes_no(f"Использовать Overwatch (1 CP)? Доступные юниты: {ids} (y/n): ")
            if strat is None:
                self.game_over = True
                return
            if not strat:
                return
            choice = self._get_input("Введите номер юнита для Overwatch: ").strip()
            if not is_num(choice) or int(choice) - (21 if defender_side == "model" else 11) not in candidates:
                self._log_phase_msg(side_label, phase, "Overwatch отменён: выбран недоступный юнит.")
                return
            chosen = int(choice) - (21 if defender_side == "model" else 11)

        if defender_side == "model":
            self.modelCP -= 1
            attacker_health = self.unit_health
            attacker_weapon = self.unit_weapon
            attacker_data = self.unit_data
            target_health = self.enemy_health if moving_unit_side == "enemy" else self.unit_health
            target_data = self.enemy_data if moving_unit_side == "enemy" else self.unit_data
            target_coords = self.enemy_coords if moving_unit_side == "enemy" else self.unit_coords
        else:
            self.enemyCP -= 1
            attacker_health = self.enemy_health
            attacker_weapon = self.enemy_weapon
            attacker_data = self.enemy_data
            target_health = self.unit_health if moving_unit_side == "model" else self.enemy_health
            target_data = self.unit_data if moving_unit_side == "model" else self.enemy_data
            target_coords = self.unit_coords if moving_unit_side == "model" else self.enemy_coords

        distance_to_target = distance(
            self.unit_coords[chosen] if defender_side == "model" else self.enemy_coords[chosen],
            target_coords[moving_idx],
        )
        _logger = None
        if self.trunc is False and _verbose_logs_enabled():
            _logger = RollLogger(auto_dice)
            dmg, modHealth = attack(
                attacker_health[chosen],
                attacker_weapon[chosen],
                attacker_data[chosen],
                target_health[moving_idx],
                target_data[moving_idx],
                distance_to_target=distance_to_target,
                hit_on_6=True,
                roller=_logger.roll,
            )
        else:
            dmg, modHealth = attack(
                attacker_health[chosen],
                attacker_weapon[chosen],
                attacker_data[chosen],
                target_health[moving_idx],
                target_data[moving_idx],
                distance_to_target=distance_to_target,
                hit_on_6=True,
            )

        target_health[moving_idx] = modHealth
        attacker_unit_id = chosen + (21 if defender_side == "model" else 11)
        target_unit_id = moving_idx + (21 if moving_unit_side == "model" else 11)
        self._log_unit_phase(
            side_label,
            phase,
            attacker_unit_id,
            chosen,
            f"Overwatch по {target_label} Unit {target_unit_id}: -1 CP, урон {float(np.sum(dmg))}.",
        )
        if _logger is not None:
            _logger.print_shoot_report(
                weapon=attacker_weapon[chosen],
                attacker_data=attacker_data[chosen],
                defender_data=target_data[moving_idx],
                dmg_list=dmg,
                effect=None,
            )

    def _resolve_heroic_intervention(self, defender_side: str, charging_side: str, charging_idx: int, phase: str, manual: bool = False):
        """
        10e Heroic Intervention: реакция защитника после успешного charge move врага.
        Упрощение: eligible = юниты защитника в 6" от charging unit.
        Из-за 1v1 структуры unitInAttack отмечаем только защитника.
        """
        side_label = self._side_label(defender_side, manual=manual)
        if defender_side == "model":
            defender_health = self.unit_health
            defender_coords = self.unit_coords
            defender_in_attack = self.unitInAttack
            defender_cp = self.modelCP
        else:
            defender_health = self.enemy_health
            defender_coords = self.enemy_coords
            defender_in_attack = self.enemyInAttack
            defender_cp = self.enemyCP

        charging_coords = self.unit_coords if charging_side == "model" else self.enemy_coords
        eligible = []
        for i in range(len(defender_health)):
            if defender_health[i] <= 0:
                continue
            if defender_in_attack[i][0] == 1:
                continue
            if distance(defender_coords[i], charging_coords[charging_idx]) <= 6:
                eligible.append(i)

        if not eligible:
            self._log_phase_msg(side_label, phase, "Heroic Intervention недоступен: нет eligible юнитов в 6\".")
            return

        if defender_cp < 2:
            self._log_phase_msg(side_label, phase, "Heroic Intervention недоступен: недостаточно CP.")
            return

        unit_ids = [i + (21 if defender_side == "model" else 11) for i in eligible]
        self._log_phase_msg(
            side_label,
            phase,
            f"Доступные юниты для Heroic Intervention: {unit_ids}.",
        )

        use_it = True
        chosen = eligible[0]
        if manual:
            strat = self._prompt_yes_no("Использовать Heroic Intervention (2 CP)? (y/n): ")
            if strat is None:
                self.game_over = True
                return
            if not strat:
                return
            choice = self._get_input("Введите номер юнита для Heroic Intervention: ").strip()
            if not is_num(choice) or int(choice) - (21 if defender_side == "model" else 11) not in eligible:
                self._log_phase_msg(side_label, phase, "Heroic Intervention отменён: выбран недоступный юнит.")
                return
            chosen = int(choice) - (21 if defender_side == "model" else 11)

        if defender_side == "model":
            self.modelCP -= 2
        else:
            self.enemyCP -= 2

        pos_before = tuple(defender_coords[chosen])
        defender_coords[chosen][0] = charging_coords[charging_idx][0] + 1
        defender_coords[chosen][1] = charging_coords[charging_idx][1] + 1
        defender_coords[chosen] = bounds(defender_coords[chosen], self.b_len, self.b_hei)
        defender_in_attack[chosen][0] = 1
        defender_in_attack[chosen][1] = charging_idx
        pos_after = tuple(defender_coords[chosen])

        self._log_unit_phase(
            side_label,
            phase,
            chosen + (21 if defender_side == "model" else 11),
            chosen,
            f"Выбран для Heroic Intervention. Переместился: {pos_before} -> {pos_after}, entered_in_engagement=True.",
        )

    def _prompt_int(self, prompt: str, min_val: int, max_val: int, allow_quit: bool = True):
        while True:
            response = self._get_input(prompt).strip().lower()
            if allow_quit and response in ("quit", "q"):
                return None
            if response.isdigit():
                value = int(response)
                if min_val <= value <= max_val:
                    return value
                self._log(f"Not in range ({min_val}..{max_val}): {value}")
            else:
                self._log("Not a number, try again.")

    def begin_phase(self, side: str, phase: str):
        self.active_side = side
        self.phase = phase
        if not self._round_banner_shown:
            self._log(f"=== BATTLE ROUND {self.battle_round} ===")
            self._round_banner_shown = True
        if phase == "command":
            self._log(f"--- {side.upper()} TURN ---")
            if side == "model":
                self.unitFellBack = [False] * len(self.unit_health)
            elif side == "enemy":
                self.enemyFellBack = [False] * len(self.enemy_health)
        phase_title = {
            "command": "Command phase!",
            "movement": "Movement phase!",
            "shooting": "Shooting phase!",
            "charge": "Charge phase!",
            "fight": "Fight phase!",
        }.get(phase, f"{phase.title()} phase!")
        self._log(phase_title)

    def _end_battle_round(self):
        self._log(f"=== END OF BATTLE ROUND {self.battle_round} ===")
        self.battle_round += 1
        self.numTurns = self.battle_round
        self._round_banner_shown = False
        apply_end_of_battle(self, log_fn=self._log)

    def _advance_turn_order(self):
        if self.active_side == self.turn_order[-1]:
            self._end_battle_round()
            self.active_side = self.turn_order[0]
        else:
            current_index = self.turn_order.index(self.active_side)
            self.active_side = self.turn_order[current_index + 1]
        self.phase = "command"

    def command_phase(self, side: str, action=None, manual: bool = False):
        self.begin_phase(side, "command")
        if side == "model":
            self._log_phase("MODEL", "command")
            self.modelCP += 1
            self.enemyCP += 1
            reward_delta = 0
            battle_shock = [False] * len(self.unit_health)
            for i in range(len(self.unit_health)):
                if isBelowHalfStr(self.unit_data[i], self.unit_health[i]) is True and self.unit_health[i] > 0:
                    if self.trunc is False:
                        self._log("This unit is Battle-shocked, starting test...")
                        self._log("Rolling 2D6...")
                    diceRoll = dice(num=2)
                    if self.trunc is False:
                        self._log(f"Model rolled {diceRoll[0]} {diceRoll[1]}")
                    if sum(diceRoll) >= self.unit_data[i]["Ld"]:
                        self.modelOC[i] = self.unit_data[i]["OC"]
                        if self.trunc is False:
                            self._log("Battle-shock test passed!")
                    else:
                        battle_shock[i] = True
                        self.modelOC[i] = 0
                        if self.trunc is False:
                            self._log("Battle-shock test failed")
                        if action and action.get("use_cp") == 1 and action.get("cp_on") == i:
                            if self.modelCP - 1 >= 0:
                                battle_shock[i] = False
                                reward_delta += 0.5
                                self.modelCP -= 1
                                if self.trunc is False:
                                    self._log("Used Insane Bravery Stratagem to pass Battle Shock test")
                            else:
                                reward_delta -= 0.5
            dice_fn = player_dice if os.getenv("MANUAL_DICE", "0") == "1" and side == "enemy" else auto_dice
            apply_end_of_command_phase(self, side="model", dice_fn=dice_fn, log_fn=self._log)
            score_end_of_command_phase(self, "model", log_fn=self._log)
            return battle_shock, reward_delta

        if side == "enemy" and manual:
            self.enemyCP += 1
            self.modelCP += 1
            battle_shock = [False] * len(self.enemy_health)
            for i in range(len(self.enemy_health)):
                playerName = i + 11
                battleSh = False
                if isBelowHalfStr(self.enemy_data[i], self.enemy_health[i]) is True and self.unit_health[i] > 0:
                    self._log("This unit is Battle-shocked, starting test...")
                    self._log("Rolling 2D6...")
                    diceRoll = player_dice(num=2)
                    self._log(f"You rolled {diceRoll[0]} {diceRoll[1]}")
                    if sum(diceRoll) >= self.enemy_data[i]["Ld"]:
                        self._log("Battle-shock test passed!")
                        self.enemyOC[i] = self.enemy_data[i]["OC"]
                    else:
                        battleSh = True
                        self._log("Battle-shock test failed")
                        self.enemyOC[i] = 0
                        if self.enemyCP - 1 >= 0:
                            strat = self._prompt_yes_no(
                                f"Would you like to use the Insane Bravery Strategem for Unit {playerName}? (y/n): "
                            )
                            if strat is None:
                                self.game_over = True
                                return None
                            if strat:
                                battleSh = False
                                self.enemyCP -= 1
                                self.enemyOC[i] = self.enemy_data[i]["OC"]
                battle_shock[i] = battleSh
                if battleSh:
                    continue
            self._manual_enemy_battle_shock = battle_shock
            dice_fn = player_dice if os.getenv("MANUAL_DICE", "0") == "1" and side == "enemy" else auto_dice
            apply_end_of_command_phase(self, side="enemy", dice_fn=dice_fn, log_fn=self._log)
            score_end_of_command_phase(self, "enemy", log_fn=self._log)
            return battle_shock

        if side == "enemy":
            self.enemyCP += 1
            self.modelCP += 1
            battle_shock = [False] * len(self.enemy_health)
            cp_on = np.random.randint(0, len(self.enemy_health))
            use_cp = np.random.randint(0, 5)
            self._enemy_cp_on = cp_on
            self._enemy_use_cp = use_cp
            for i in range(len(self.enemy_health)):
                battleSh = False
                if isBelowHalfStr(self.enemy_data[i], self.enemy_health[i]) is True and self.unit_health[i] > 0:
                    if self.trunc is False:
                        self._log("This unit is Below Half Strength, starting test...")
                        self._log("Rolling 2D6...")
                    diceRoll = dice(num=2)
                    if self.trunc is False:
                        self._log(f"Player rolled {diceRoll[0]} {diceRoll[1]}")
                    if sum(diceRoll) >= self.enemy_data[i]["Ld"]:
                        if self.trunc is False:
                            self._log("Battle-shock test passed!")
                        self.enemyOC[i] = self.enemy_data[i]["OC"]
                    else:
                        battleSh = True
                        self.enemyOC[i] = 0
                        if self.trunc is False:
                            self._log("Battle-shock test failed")
                        if use_cp == 1 and cp_on == i and self.enemyCP - 1 >= 0:
                            battleSh = False
                            self.enemyCP -= 1
                            self.enemyOC[i] = self.enemy_data[i]["OC"]

                battle_shock[i] = battleSh
            dice_fn = player_dice if os.getenv("MANUAL_DICE", "0") == "1" and side == "enemy" else auto_dice
            apply_end_of_command_phase(self, side="enemy", dice_fn=dice_fn, log_fn=self._log)
            score_end_of_command_phase(self, "enemy", log_fn=self._log)
            return battle_shock

        return None

    def movement_phase(self, side: str, action=None, manual: bool = False, battle_shock=None):
        self.begin_phase(side, "movement")
        if side == "model":
            self._log_phase("MODEL", "movement")
            advanced_flags = [False] * len(self.unit_health)
            reward_delta = 0
            for i in range(len(self.unit_health)):
                modelName = i + 21
                battleSh = battle_shock[i] if battle_shock else False
                pos_before = tuple(self.unit_coords[i])
                if self.unit_health[i] <= 0:
                    self._log_unit("MODEL", modelName, i, f"Юнит мертв, движение пропущено. Позиция: {pos_before}")
                    continue
                if self.unitInAttack[i][0] == 0 and self.unit_health[i] > 0:
                    base_m = self.unit_data[i]["Movement"]
                    label = "move_num_" + str(i)
                    want = int(action[label])
                    advanced = (action["move"] != 4) and (want > base_m)
                    advance_roll = None
                    if advanced:
                        advance_roll = dice()
                        max_move = base_m + advance_roll
                    else:
                        max_move = base_m
                    movement = min(want, max_move)

                    if action["move"] == 0:
                        self.unit_coords[i][0] += movement
                    elif action["move"] == 1:
                        self.unit_coords[i][0] -= movement
                    elif action["move"] == 2:
                        self.unit_coords[i][1] -= movement
                    elif action["move"] == 3:
                        self.unit_coords[i][1] += movement
                    elif action["move"] == 4:
                        for j in range(len(self.coordsOfOM)):
                            if distance(self.unit_coords[i], self.coordsOfOM[j]) <= 5:
                                reward_delta += 0.5
                            else:
                                reward_delta -= 0.5

                    advanced_flags[i] = advanced
                    direction = {0: "down", 1: "up", 2: "left", 3: "right", 4: "none"}.get(action["move"], "none")
                    actual_movement = movement if action["move"] != 4 else 0
                    advance_text = "да" if advanced else "нет"
                    if advance_roll is not None:
                        advance_detail = f", бросок={advance_roll}, макс={max_move}"
                    else:
                        advance_detail = ""
                    self._log_unit(
                        "MODEL",
                        modelName,
                        i,
                        f"Позиция до: {pos_before}. Выбор: {direction}, advance={advance_text}{advance_detail}, distance={actual_movement}",
                    )

                    self.unit_coords[i] = bounds(self.unit_coords[i], self.b_len, self.b_hei)
                    for j in range(len(self.enemy_health)):
                        if self.unit_coords[i] == self.enemy_coords[j]:
                            self.unit_coords[i][0] -= 1
                    pos_after = tuple(self.unit_coords[i])
                    if action["move"] == 4:
                        self._log_unit("MODEL", modelName, i, f"Движение пропущено (no move). Позиция после: {pos_after}")
                    else:
                        self._log_unit("MODEL", modelName, i, f"Позиция после: {pos_after}")

                    if pos_before != pos_after:
                        self._resolve_overwatch(
                            defender_side="enemy",
                            moving_unit_side="model",
                            moving_idx=i,
                            phase="movement",
                            manual=os.getenv("MANUAL_DICE", "0") == "1",
                        )

                    for j in range(len(self.coordsOfOM)):
                        if distance(self.coordsOfOM[j], self.unit_coords[i]) <= 5:
                            reward_delta += 0.5

                elif self.unitInAttack[i][0] == 1 and self.unit_health[i] > 0:
                    idOfE = self.unitInAttack[i][1]
                    if self.enemy_health[idOfE] <= 0:
                        reward_delta += 0.3
                        self.unitInAttack[i][0] = 0
                        self.unitInAttack[i][1] = 0
                        self.enemyInAttack[idOfE][0] = 0
                        self.enemyInAttack[idOfE][1] = 0
                        self._log_unit(
                            "MODEL",
                            modelName,
                            i,
                            f"Цель в ближнем бою мертва (Enemy Unit {idOfE + 11}), юнит выходит из боя. Позиция: {pos_before}",
                        )
                    else:
                        if action["attack"] == 0:
                            if self.unit_health[i] * 2 >= self.enemy_health[idOfE]:
                                reward_delta -= 0.5
                            self._log_unit(
                                "MODEL",
                                modelName,
                                i,
                                f"Отступление из боя с Enemy Unit {idOfE + 11}. Позиция до: {pos_before}",
                            )
                            self.unitFellBack[i] = True
                            if battleSh is True:
                                diceRoll = dice()
                                if diceRoll < 3:
                                    self.unit_health[i] -= self.unit_data[i]["W"]
                            self.unit_coords[i][0] += self.unit_data[i]["Movement"]
                            self.unitInAttack[i][0] = 0
                            self.unitInAttack[i][1] = 0
                            self.enemyInAttack[idOfE][0] = 0
                            self.enemyInAttack[idOfE][1] = 0
                            pos_after = tuple(self.unit_coords[i])
                            self._log_unit("MODEL", modelName, i, f"Отступление завершено. Позиция после: {pos_after}")
                            if pos_before != pos_after:
                                self._resolve_overwatch(
                                    defender_side="enemy",
                                    moving_unit_side="model",
                                    moving_idx=i,
                                    phase="movement",
                                    manual=os.getenv("MANUAL_DICE", "0") == "1",
                                )
                        else:
                            reward_delta += 0.2
                            self._log_unit(
                                "MODEL",
                                modelName,
                                i,
                                f"Остаётся в ближнем бою с Enemy Unit {idOfE + 11}, движение пропущено.",
                            )
            return advanced_flags, reward_delta

        if side == "enemy" and manual:
            direction_map = {"up": "up", "down": "down", "left": "left", "right": "right", "none": "none"}
            normalize = {"u": "up", "d": "down", "l": "left", "r": "right", "n": "none"}
            advanced_flags = [False] * len(self.enemy_health)
            for i in range(len(self.enemy_health)):
                playerName = i + 11
                battleSh = battle_shock[i] if battle_shock else False
                pos_before = tuple(self.enemy_coords[i])
                if self.enemyInAttack[i][0] == 1 and self.enemy_health[i] > 0:
                    fall_back = self._prompt_yes_no(f"Would you like Unit {playerName} to fallback? (y/n): ")
                    if fall_back is None:
                        self.game_over = True
                        return None
                    if fall_back:
                        idOfE = self.enemyInAttack[i][1]
                        self._log(f"Player Unit {playerName} fell back from Enemy unit {idOfE + 21}")
                        self.enemyFellBack[i] = True
                        if battleSh is True:
                            diceRoll = dice()
                            if diceRoll < 3:
                                self.enemy_health[i] -= self.enemy_data[i]["W"]
                        self.enemy_coords[i][0] += self.enemy_data[i]["Movement"]
                        self.enemyInAttack[i] = [0, 0]
                        self.unitInAttack[idOfE][0] = 0
                        self.unitInAttack[idOfE][1] = 0
                    else:
                        idOfE = self.enemyInAttack[i][1]
                        self._log(
                            f"Player Unit {playerName} stays in combat with Model Unit {idOfE + 21} (will fight in Fight Phase)"
                        )
                    continue

                if self.enemyInAttack[i][0] == 0 and self.enemy_health[i] > 0:
                    self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                    for j in range(len(self.enemy_health)):
                        if self.enemy_coords[i] == self.unit_coords[j]:
                            self.enemy_coords[i][0] -= 1

                    self.updateBoard()
                    self.showBoard()

                    self._log("Take a look at board.txt or click the Show Board button in the GUI to view the current board")
                    self._log("If you would like to end the game type 'quit' into the prompt")
                    dire = self._prompt_choice(
                        f"Enter the direction of movement for Unit {playerName} (up, down, left, right, none): ",
                        direction_map,
                        normalize,
                    )
                    if dire is None:
                        self.game_over = True
                        return None

                    advanced = False
                    move_num = 0
                    if dire != "none":
                        adv = self._prompt_yes_no("Advance? (y/n): ")
                        if adv is None:
                            self.game_over = True
                            return None
                        if adv:
                            advanced = True
                            self._log("Rolling 1 D6 for Advance...")
                            roll = player_dice()
                            self._log(f"You rolled a {roll}")
                            movement_cap = self.enemy_data[i]["Movement"] + roll
                        else:
                            movement_cap = self.enemy_data[i]["Movement"]
                        move_num = self._prompt_int(
                            f"How many inches would you like to move (0..{movement_cap}): ",
                            0,
                            movement_cap,
                        )
                        if move_num is None:
                            self.game_over = True
                            return None

                    advanced_flags[i] = advanced
                    if dire == "down":
                        self.enemy_coords[i][0] += move_num
                    elif dire == "up":
                        self.enemy_coords[i][0] -= move_num
                    elif dire == "left":
                        self.enemy_coords[i][1] -= move_num
                    elif dire == "right":
                        self.enemy_coords[i][1] += move_num

                    self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                    for j in range(len(self.enemy_health)):
                        if self.enemy_coords[i] == self.unit_coords[j]:
                            self.enemy_coords[i][0] -= 1

                    self.updateBoard()
                    self.showBoard()

                    pos_after = tuple(self.enemy_coords[i])
                    if pos_before != pos_after:
                        self._resolve_overwatch(
                            defender_side="model",
                            moving_unit_side="enemy",
                            moving_idx=i,
                            phase="movement",
                            manual=False,
                        )

                    self.updateBoard()
                    self.showBoard()
            return advanced_flags

        if side == "enemy":
            advanced_flags = [False] * len(self.enemy_health)
            cp_on = getattr(self, "_enemy_cp_on", None)
            use_cp = getattr(self, "_enemy_use_cp", None)
            for i in range(len(self.enemy_health)):
                pos_before = tuple(self.enemy_coords[i])
                if self.enemyInAttack[i][0] == 1 and self.enemy_health[i] > 0:
                    decide = np.random.randint(0, 10)
                    if decide == 5:
                        idOfM = self.enemyInAttack[i][1]
                        if self.trunc is False:
                            self._log(f"Enemy unit {i + 21} pulled out of fight with Model unit {idOfM + 11}")
                        self.enemyFellBack[i] = True
                        if battle_shock and battle_shock[i]:
                            diceRoll = dice()
                            if diceRoll < 3:
                                self.enemy_health[i] -= self.enemy_data[i]["W"]
                        self.enemy_coords[i][0] -= self.enemy_data[i]["Movement"]
                        self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                        self.unitInAttack[idOfM][0] = 0
                        self.unitInAttack[idOfM][1] = 0
                        self.enemyInAttack[i] = [0, 0]
                    continue

                if self.enemyInAttack[i][0] == 0 and self.enemy_health[i] > 0:
                    aliveUnits = [j for j in range(len(self.unit_health)) if self.unit_health[j] > 0]
                    if len(aliveUnits) == 0:
                        break
                    idOfM = np.random.choice(aliveUnits)
                    base_m = self.enemy_data[i]["Movement"]
                    dist_to_target = distance(self.unit_coords[idOfM], self.enemy_coords[i])
                    advanced = dist_to_target > (base_m + 6)
                    movement = base_m + dice() if advanced else base_m

                    if distance(self.unit_coords[idOfM], [self.enemy_coords[i][0], self.enemy_coords[i][1] - movement]) < distance(self.unit_coords[idOfM], self.enemy_coords[i]):
                        self.enemy_coords[i][1] -= movement
                    elif distance(self.unit_coords[idOfM], [self.enemy_coords[i][0], self.enemy_coords[i][1] + movement]) < distance(self.unit_coords[idOfM], self.enemy_coords[i]):
                        self.enemy_coords[i][1] += movement
                    elif distance(self.unit_coords[idOfM], [self.enemy_coords[i][0] - movement, self.enemy_coords[i][1]]) < distance(self.unit_coords[idOfM], self.enemy_coords[i]):
                        self.enemy_coords[i][0] -= movement
                    elif distance(self.unit_coords[idOfM], [self.enemy_coords[i][0] + movement, self.enemy_coords[i][1]]) < distance(self.unit_coords[idOfM], self.enemy_coords[i]):
                        self.enemy_coords[i][0] += movement

                    self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                    for j in range(len(self.unit_health)):
                        if self.enemy_coords[i] == self.unit_coords[j]:
                            self.enemy_coords[i][0] -= 1
                    advanced_flags[i] = advanced

                    pos_after = tuple(self.enemy_coords[i])
                    if pos_before != pos_after:
                        self._resolve_overwatch(
                            defender_side="model",
                            moving_unit_side="enemy",
                            moving_idx=i,
                            phase="movement",
                            manual=False,
                        )
            return advanced_flags

        return None

    def shooting_phase(self, side: str, advanced_flags=None, action=None, manual: bool = False):
        self.begin_phase(side, "shooting")
        if side == "model":
            self._log_phase("MODEL", "shooting")
            reward_delta = 0
            for i in range(len(self.unit_health)):
                modelName = i + 21
                advanced = advanced_flags[i] if advanced_flags else False
                if self.unit_health[i] <= 0:
                    self._log_unit("MODEL", modelName, i, "Юнит мертв, стрельба пропущена.")
                    continue
                if self.unitFellBack[i]:
                    self._log_unit("MODEL", modelName, i, "Fall Back в этом ходу — стрельба недоступна.")
                    continue
                if self.unitInAttack[i][0] == 1:
                    self._log_unit("MODEL", modelName, i, "Юнит в ближнем бою, стрельба недоступна.")
                    continue
                if self.unit_weapon[i] == "None":
                    self._log_unit("MODEL", modelName, i, "Нет дальнобойного оружия, стрельба пропущена.")
                    continue
                if advanced and not weapon_is_assault(self.unit_weapon[i]):
                    self._log_unit("MODEL", modelName, i, "Advance без Assault — стрельба пропущена.")
                    continue

                shootAbleUnits = []
                for j in range(len(self.enemy_health)):
                    if (
                        distance(self.unit_coords[i], self.enemy_coords[j]) <= self.unit_weapon[i]["Range"]
                        and self.enemy_health[j] > 0
                        and self.enemyInAttack[j][0] == 0
                    ):
                        shootAbleUnits.append(j)
                if len(shootAbleUnits) > 0:
                    target_ids = [j + 11 for j in shootAbleUnits]
                    idOfE = action["shoot"]
                    if idOfE in shootAbleUnits:
                        distances = {j: distance(self.unit_coords[i], self.enemy_coords[j]) for j in shootAbleUnits}
                        closest = min(distances, key=distances.get)
                        min_hp = min(shootAbleUnits, key=lambda idx: self.enemy_health[idx])
                        if idOfE == closest:
                            reason = "самая близкая"
                        elif idOfE == min_hp:
                            reason = "цель с меньшим HP"
                        else:
                            reason = "выбор политики"
                        self._log_unit(
                            "MODEL",
                            modelName,
                            i,
                            f"Цели в дальности: {target_ids}, выбрана: {idOfE + 11} (причина: {reason})",
                        )
                        effect = self._maybe_use_smokescreen(
                            defender_side="enemy",
                            defender_idx=idOfE,
                            phase="shooting",
                            manual=os.getenv("MANUAL_DICE", "0") == "1",
                        )
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
                        reward_delta += 0.2
                        self._log_unit(
                            "MODEL",
                            modelName,
                            i,
                            f"Итог урона по Enemy Unit {idOfE + 11}: {float(np.sum(dmg))}",
                        )
                        if self.trunc is False:
                            self._log(f"Model Unit {modelName} shoots Enemy Unit {idOfE + 11} {float(np.sum(dmg))} damage")
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
                        reward_delta -= 0.5
                        target_ids = [j + 11 for j in shootAbleUnits]
                        self._log_unit(
                            "MODEL",
                            modelName,
                            i,
                            f"Цели в дальности: {target_ids}, выбрана недоступная {idOfE + 11}. Стрельба пропущена.",
                        )
                        if self.trunc is False:
                            self._log(f"Model Unit {modelName} fails to shoot an Enemy Unit")
                else:
                    self._log_unit("MODEL", modelName, i, "Нет целей в дальности, стрельба пропущена.")
            return reward_delta
        elif side == "enemy" and manual:
            for i in range(len(self.enemy_health)):
                playerName = i + 11
                advanced = advanced_flags[i] if advanced_flags else False
                if self.enemyFellBack[i]:
                    self._log(f"Unit {playerName} Fell Back this turn — skipping shooting")
                    continue
                if self.enemy_weapon[i] != "None":
                    if advanced and not weapon_is_assault(self.enemy_weapon[i]):
                        self._log("You advanced — non-Assault weapon, skipping shooting")
                    else:
                        shootAble = np.array([])
                        for j in range(len(self.unit_health)):
                            if distance(self.enemy_coords[i], self.unit_coords[j]) <= self.enemy_weapon[i]["Range"] and self.unit_health[j] > 0 and self.unitInAttack[j][0] == 0:
                                shootAble = np.append(shootAble, j)
                        if len(shootAble) > 0:
                            response = False
                            while response is False:
                                shoot = self._get_input(
                                    "Select which enemy unit you would like to shoot ({}) with Unit {}: ".format(shootAble + 21, playerName)
                                ).strip()
                                if shoot.lower() in ("quit", "q"):
                                    self.game_over = True
                                    return None
                                if is_num(shoot) is True and int(shoot) - 21 in shootAble:
                                    idOfE = int(shoot) - 21
                                    effect = self._maybe_use_smokescreen(
                                        defender_side="model",
                                        defender_idx=idOfE,
                                        phase="shooting",
                                        manual=False,
                                    )
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
                                    self._log(f"Player Unit {playerName} нанёс {sum(dmg)} урона по Model Unit {idOfE + 21}")
                                    logger.print_shoot_report(
                                        weapon=self.enemy_weapon[i],
                                        attacker_data=self.enemy_data[i],
                                        defender_data=self.unit_data[idOfE],
                                        dmg_list=dmg,
                                        effect=effect,
                                    )
                                    response = True
                                else:
                                    self._log("Not an available unit")
                else:
                    self._log("No available weapons to shoot")
        elif side == "enemy":
            for i in range(len(self.enemy_health)):
                advanced = advanced_flags[i] if advanced_flags else False
                if self.enemyFellBack[i]:
                    if self.trunc is False:
                        self._log(f"Enemy Unit {i + 21} Fell Back — skipping shooting")
                    continue
                if self.enemy_weapon[i] != "None":
                    if advanced and not weapon_is_assault(self.enemy_weapon[i]):
                        if self.trunc is False:
                            self._log("Enemy advanced — non-Assault weapon, skipping shooting")
                    else:
                        shootAbleUnits = []
                        for j in range(len(self.unit_health)):
                            if distance(self.enemy_coords[i], self.unit_coords[j]) <= self.enemy_weapon[i]["Range"] and self.unit_health[j] > 0 and self.unitInAttack[j][0] == 0:
                                shootAbleUnits.append(j)
                        if len(shootAbleUnits) > 0:
                            idOfM = np.random.choice(shootAbleUnits)
                            effect = self._maybe_use_smokescreen(
                                defender_side="model",
                                defender_idx=idOfM,
                                phase="shooting",
                                manual=False,
                            )
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
                            if self.trunc is False:
                                self._log(f"Enemy Unit {i + 21} shoots Model Unit {idOfM + 11} {float(np.sum(dmg))} damage")
        return None

    def charge_phase(self, side: str, advanced_flags=None, action=None, manual: bool = False):
        self.begin_phase(side, "charge")
        if side == "model":
            self._log_phase("MODEL", "charge")
            reward_delta = 0
            any_charge_targets = False
            for i in range(len(self.unit_health)):
                modelName = i + 21
                advanced = advanced_flags[i] if advanced_flags else False
                pos_before = tuple(self.unit_coords[i])
                if self.unit_health[i] <= 0:
                    self._log_unit("MODEL", modelName, i, "Юнит мертв, чардж пропущен.")
                    continue
                if self.unitFellBack[i]:
                    self._log_unit("MODEL", modelName, i, "Fall Back в этом ходу — чардж невозможен.")
                    continue
                if self.unitInAttack[i][0] == 1:
                    self._log_unit("MODEL", modelName, i, "Уже в ближнем бою, чардж невозможен.")
                    continue
                if advanced:
                    self._log_unit("MODEL", modelName, i, "Advance — чардж невозможен.")
                else:
                    potential_targets = []
                    for j in range(len(self.enemy_health)):
                        if distance(self.enemy_coords[j], self.unit_coords[i]) <= 12 and self.enemyInAttack[j][0] == 0 and self.enemy_health[j] > 0:
                            potential_targets.append(j)
                    if potential_targets:
                        any_charge_targets = True
                    if action["attack"] != 1:
                        if potential_targets:
                            target_ids = [j + 11 for j in potential_targets]
                            self._log_unit(
                                "MODEL",
                                modelName,
                                i,
                                f"Доступные цели для чарджа: {target_ids}. Решение: пропуск чарджа.",
                            )
                        else:
                            self._log_unit("MODEL", modelName, i, "Нет целей в 12\", чардж пропущен.")
                        continue
                    chargeAble = []
                    dice_vals = dice(num=2)
                    diceRoll = sum(dice_vals)
                    if action["attack"] == 1:
                        for j in range(len(self.enemy_health)):
                            if distance(self.enemy_coords[j], self.unit_coords[i]) <= 12 and self.enemyInAttack[j][0] == 0 and self.enemy_health[j] > 0:
                                if distance(self.enemy_coords[j], self.unit_coords[i]) - diceRoll <= 5:
                                    chargeAble.append(j)
                    if len(chargeAble) > 0:
                        idOfE = action["charge"]
                        target_ids = [j + 11 for j in chargeAble]
                        dist_to_target = distance(self.enemy_coords[idOfE], self.unit_coords[i]) if idOfE in chargeAble else None
                        if _verbose_logs_enabled():
                            roll_text = f"бросок: {dice_vals[0]} + {dice_vals[1]} = {diceRoll}"
                        else:
                            roll_text = f"бросок total={diceRoll}"
                        if idOfE in chargeAble:
                            self._log_unit_phase(
                                "MODEL",
                                "charge",
                                modelName,
                                i,
                                f"Charge объявлен по цели Enemy Unit {idOfE + 11}. Дистанция: {dist_to_target:.1f}. Бросок 2D6: {dice_vals[0]} + {dice_vals[1]} = {diceRoll}.",
                            )
                            self._log_unit(
                                "MODEL",
                                modelName,
                                i,
                                f"Чардж цели: {target_ids}, выбрана {idOfE + 11} (dist={dist_to_target:.1f}). {roll_text}. Результат: успех.",
                            )
                            self.unitInAttack[i][0] = 1
                            self.unitInAttack[i][1] = idOfE
                            self.unit_coords[i][0] = self.enemy_coords[idOfE][0] + 1
                            self.unit_coords[i][1] = self.enemy_coords[idOfE][1] + 1
                            self.unit_coords[i] = bounds(self.unit_coords[i], self.b_len, self.b_hei)
                            self.enemyInAttack[idOfE][0] = 1
                            self.enemyInAttack[idOfE][1] = i
                            self.unitCharged[i] = 1
                            pos_after = tuple(self.unit_coords[i])
                            self._log_unit_phase(
                                "MODEL",
                                "charge",
                                modelName,
                                i,
                                f"Charge move: from {pos_before} -> {pos_after}, ended_in_engagement={self.unitInAttack[i][0] == 1}.",
                            )
                            # 10e: Heroic Intervention доступен защитнику после успешного charge move.
                            self._resolve_heroic_intervention(
                                defender_side="enemy",
                                charging_side="model",
                                charging_idx=i,
                                phase="charge",
                                manual=os.getenv("MANUAL_DICE", "0") == "1",
                            )
                            reward_delta += 0.5
                        else:
                            reason = "цель вне досягаемости" if idOfE in potential_targets else "цель недоступна"
                            if idOfE in potential_targets:
                                dist_to_target = distance(self.enemy_coords[idOfE], self.unit_coords[i])
                                self._log_unit_phase(
                                    "MODEL",
                                    "charge",
                                    modelName,
                                    i,
                                    f"Charge объявлен по цели Enemy Unit {idOfE + 11}. Дистанция: {dist_to_target:.1f}. Бросок 2D6: {dice_vals[0]} + {dice_vals[1]} = {diceRoll}.",
                                )
                            self._log_unit(
                                "MODEL",
                                modelName,
                                i,
                                f"Чардж цели: {target_ids}, выбрана {idOfE + 11}. {roll_text}. Результат: провал ({reason}).",
                            )
                            reward_delta -= 0.5
                    else:
                        if potential_targets:
                            target_ids = [j + 11 for j in potential_targets]
                            if _verbose_logs_enabled():
                                roll_text = f"бросок: {dice_vals[0]} + {dice_vals[1]} = {diceRoll}"
                            else:
                                roll_text = f"бросок total={diceRoll}"
                            self._log_unit(
                                "MODEL",
                                modelName,
                                i,
                                f"Цели в 12\": {target_ids}. {roll_text}. Нет достижимых целей.",
                            )
                        else:
                            self._log_unit("MODEL", modelName, i, "Нет целей в 12\", чардж пропущен.")
            if not any_charge_targets:
                self._log("[MODEL] Чардж: нет доступных целей")
            return reward_delta
        elif side == "enemy" and manual:
            any_chargeable = False
            battle_shock = getattr(self, "_manual_enemy_battle_shock", None)
            for i in range(len(self.enemy_health)):
                playerName = i + 11
                advanced = advanced_flags[i] if advanced_flags else False
                pos_before = tuple(self.enemy_coords[i])
                if self.enemyFellBack[i]:
                    self._log(f"Unit {playerName} Fell Back this turn — skipping charge")
                    continue
                if advanced:
                    self._log("You advanced — cannot charge, skipping charge")
                    continue
                charg = np.array([])
                for j in range(len(self.unit_health)):
                    if distance(self.unit_coords[j], self.enemy_coords[i]) <= 12 and self.unitInAttack[j][0] == 0 and self.unit_health[j] > 0:
                        charg = np.append(charg, j)
                if len(charg) > 0:
                    any_chargeable = True
                    want_charge = self._prompt_yes_no(f"Would you like Unit {playerName} to charge? (y/n): ")
                    if want_charge is None:
                        self.game_over = True
                        return None
                    if not want_charge:
                        self._log(f"Player Unit {playerName} decided to skip charge")
                        continue
                    response = False
                    while response is False:
                        attk = self._get_input(
                            "Select which enemy you would like to charge ({}) with Unit {}: ".format(charg + 21, playerName)
                        ).strip()
                        if attk.lower() in ("quit", "q"):
                            self.game_over = True
                            return None
                        if is_num(attk) is True and int(attk) - 21 in charg:
                            response = True
                            j = int(attk) - 21
                            self._log("Rolling 2 D6...")
                            roll = player_dice(num=2)
                            self._log(f"You rolled a {roll[0]} and {roll[1]}")
                            dist_to_target = distance(self.enemy_coords[i], self.unit_coords[j])
                            self._log_unit_phase(
                                self._side_label("enemy", manual=True),
                                "charge",
                                playerName,
                                i,
                                f"Charge объявлен по цели Model Unit {j + 21}. Дистанция: {dist_to_target:.1f}. Бросок 2D6: {roll[0]} + {roll[1]} = {sum(roll)}.",
                            )
                            if distance(self.enemy_coords[i], self.unit_coords[j]) - sum(roll) <= 5:
                                self._log(f"Player Unit {playerName} Successfully charged Model Unit {j + 21}")
                                self.enemyInAttack[i][0] = 1
                                self.enemyInAttack[i][1] = j
                                self.enemy_coords[i][0] = self.unit_coords[j][0] + 1
                                self.enemy_coords[i][1] = self.unit_coords[j][1] + 1
                                self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                                self.enemyCharged[i] = 1
                                self.updateBoard()
                                self.unitInAttack[j][0] = 1
                                self.unitInAttack[j][1] = i
                                pos_after = tuple(self.enemy_coords[i])
                                self._log_unit_phase(
                                    self._side_label("enemy", manual=True),
                                    "charge",
                                    playerName,
                                    i,
                                    f"Charge move: from {pos_before} -> {pos_after}, ended_in_engagement={self.enemyInAttack[i][0] == 1}.",
                                )
                                # 10e: Heroic Intervention доступен защитнику после успешного charge move.
                                self._resolve_heroic_intervention(
                                    defender_side="model",
                                    charging_side="enemy",
                                    charging_idx=i,
                                    phase="charge",
                                    manual=False,
                                )
                            else:
                                self._log(f"Player Unit {playerName} Failed to charge Model Unit {j + 21}")
                        else:
                            self._log("Not an available unit")
            if not any_chargeable:
                self._log("No available units to charge")
        elif side == "enemy":
            for i in range(len(self.enemy_health)):
                advanced = advanced_flags[i] if advanced_flags else False
                pos_before = tuple(self.enemy_coords[i])
                if self.enemyFellBack[i]:
                    if self.trunc is False:
                        self._log("Enemy Fell Back — cannot charge, skipping charge")
                    continue
                if advanced:
                    if self.trunc is False:
                        self._log("Enemy advanced — cannot charge, skipping charge")
                else:
                    chargeAble = []
                    diceRoll = sum(dice(num=2))
                    for j in range(len(self.unit_health)):
                        if distance(self.enemy_coords[i], self.unit_coords[j]) <= 12 and self.unitInAttack[j][0] == 0:
                            if distance(self.enemy_coords[i], self.unit_coords[j]) - diceRoll <= 5:
                                chargeAble.append(j)
                    if len(chargeAble) > 0:
                        idOfM = int(np.random.choice(chargeAble))
                        dist = distance(self.enemy_coords[i], self.unit_coords[idOfM])
                        required = max(0, dist - 1)
                        self._log_unit_phase(
                            "ENEMY",
                            "charge",
                            i + 21,
                            i,
                            f"Charge объявлен по цели Model Unit {idOfM + 11}. Дистанция: {dist:.1f}. Бросок 2D6: {diceRoll}.",
                        )
                        if diceRoll >= required:
                            if self.trunc is False:
                                self._log(
                                    f"Enemy unit {i + 21} successfully charged Model unit {idOfM + 11} (roll {diceRoll} vs need {required:.1f})"
                                )
                            self.enemy_coords[i][0] = self.unit_coords[idOfM][0] + 1
                            self.enemy_coords[i][1] = self.unit_coords[idOfM][1]
                            self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                            self.enemyInAttack[i][0] = 1
                            self.enemyInAttack[i][1] = idOfM
                            self.unitInAttack[idOfM][0] = 1
                            self.unitInAttack[idOfM][1] = i
                            self.enemyCharged[i] = 1
                            pos_after = tuple(self.enemy_coords[i])
                            self._log_unit_phase(
                                "ENEMY",
                                "charge",
                                i + 21,
                                i,
                                f"Charge move: from {pos_before} -> {pos_after}, ended_in_engagement={self.enemyInAttack[i][0] == 1}.",
                            )
                            # 10e: Heroic Intervention доступен защитнику после успешного charge move.
                            self._resolve_heroic_intervention(
                                defender_side="model",
                                charging_side="enemy",
                                charging_idx=i,
                                phase="charge",
                                manual=False,
                            )
                        elif self.trunc is False:
                            self._log(
                                f"Enemy unit {i + 21} failed charge vs Model unit {idOfM + 11} (roll {diceRoll} vs need {required:.1f})"
                            )
        return None

    def fight_phase(self, side: str):
        self.begin_phase(side, "fight")
        if side == "model":
            self._log_phase("MODEL", "fight")
            engaged_model = [i for i in range(len(self.unit_health)) if self.unit_health[i] > 0 and self.unitInAttack[i][0] == 1]
            engaged_enemy = [i for i in range(len(self.enemy_health)) if self.enemy_health[i] > 0 and self.enemyInAttack[i][0] == 1]
            if not engaged_model and not engaged_enemy:
                self._log("[MODEL] Ближний бой: нет доступных атак")
            else:
                model_ids = [i + 21 for i in engaged_model]
                enemy_ids = [i + 11 for i in engaged_enemy]
                self._log(f"[MODEL] Ближний бой: участвуют Model units {model_ids}, Enemy units {enemy_ids}")
                for idx in engaged_model:
                    def_idx = self.unitInAttack[idx][1]
                    if 0 <= def_idx < len(self.enemy_health):
                        self._log_unit(
                            "MODEL",
                            idx + 21,
                            idx,
                            f"В бою с Enemy Unit {def_idx + 11}",
                        )
        self.resolve_fight_phase(active_side=side, trunc=self.trunc)

    def refresh_objective_control(self):
        self.model_obj_oc = np.zeros(len(self.coordsOfOM), dtype=int)
        self.enemy_obj_oc = np.zeros(len(self.coordsOfOM), dtype=int)

        for i in range(len(self.unit_health)):
            if self.unit_health[i] <= 0:
                continue
            wounds = self.unit_data[i]["W"]
            remaining_models = (self.unit_health[i] + wounds - 1) // wounds
            effective_oc = self.modelOC[i] * remaining_models
            if effective_oc <= 0:
                continue
            for j in range(len(self.coordsOfOM)):
                if distance(self.coordsOfOM[j], self.unit_coords[i]) <= 5:
                    self.model_obj_oc[j] += effective_oc

        for i in range(len(self.enemy_health)):
            if self.enemy_health[i] <= 0:
                continue
            wounds = self.enemy_data[i]["W"]
            remaining_models = (self.enemy_health[i] + wounds - 1) // wounds
            effective_oc = self.enemyOC[i] * remaining_models
            if effective_oc <= 0:
                continue
            for j in range(len(self.coordsOfOM)):
                if distance(self.coordsOfOM[j], self.enemy_coords[i]) <= 5:
                    self.enemy_obj_oc[j] += effective_oc

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
        self.unitFellBack = []
        self.enemyFellBack = []
        self.unitCharged = [0] * len(self.unit_health)
        self.enemyCharged = [0] * len(self.enemy_health)

        self.model_obj_oc = np.zeros(len(self.coordsOfOM), dtype=int)
        self.enemy_obj_oc = np.zeros(len(self.coordsOfOM), dtype=int)

        self.modelCP = 0
        self.enemyCP = 0
        self.modelVP = 0
        self.enemyVP = 0
        self.battle_round = 1
        self.active_side = self.turn_order[0]
        self.phase = "command"
        self.numTurns = self.battle_round
        self._round_banner_shown = False
        self.mission_name = MISSION_NAME
        self.modelUpdates = ""

        for i in range(len(self.enemy_data)):
            self.enemy_coords.append([e[i].showCoords()[0], e[i].showCoords()[1]])
            self.enemy_health.append(self.enemy_data[i]["W"] * self.enemy_data[i]["#OfModels"])
            self.enemyInAttack.append([0, 0])
        self.enemyFellBack = [False] * len(self.enemy_health)

        for i in range(len(self.unit_data)):
            self.unit_coords.append([m[i].showCoords()[0], m[i].showCoords()[1]])
            self.unit_health.append(self.unit_data[i]["W"] * self.unit_data[i]["#OfModels"])
            self.unitInAttack.append([0, 0])
        self.unitFellBack = [False] * len(self.unit_health)

        self.game_over = False
        self.current_action_index = 0
        info = self.get_info()

        if Type == "big":
            self.updateBoard()

        return self._get_observation(), info

    def enemyTurn(self, trunc=False):
        self.unitCharged = [0] * len(self.unit_health)
        self.enemyCharged = [0] * len(self.enemy_health)
        if trunc is True:
            self.trunc = True

        self.active_side = "enemy"
        battle_shock = self.command_phase("enemy")
        advanced_flags = self.movement_phase("enemy", battle_shock=battle_shock)
        self.shooting_phase("enemy", advanced_flags=advanced_flags)
        self.charge_phase("enemy", advanced_flags=advanced_flags)
        self.fight_phase("enemy")
        apply_end_of_battle(self, log_fn=self._log)

        if self.modelStrat["overwatch"] != -1:
            self.modelStrat["overwatch"] = -1
        if self.modelStrat["smokescreen"] != -1:
            self.modelStrat["smokescreen"] = -1

        self._advance_turn_order()

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
                self._log(msg)

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
                self._log_unit_phase(
                    "MODEL",
                    "fight",
                    att_idx + 21,
                    att_idx,
                    f"Выбран для атаки. Цель: Enemy Unit {def_idx + 11}.",
                )

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
                self._log_unit_phase(
                    "MODEL",
                    "fight",
                    att_idx + 21,
                    att_idx,
                    f"Итог атаки: урон {float(np.sum(dmg))}, HP цели {hp_before} -> {modHealth}.",
                )

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
                enemy_label = self._side_label("enemy", manual=os.getenv("MANUAL_DICE", "0") == "1")
                self._log_unit_phase(
                    enemy_label,
                    "fight",
                    att_idx + 11,
                    att_idx,
                    f"Выбран для атаки. Цель: Model Unit {def_idx + 21}.",
                )

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
                self._log_unit_phase(
                    enemy_label,
                    "fight",
                    att_idx + 11,
                    att_idx,
                    f"Итог атаки: урон {float(np.sum(dmg))}, HP цели {hp_before} -> {modHealth}.",
                )

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

        model_eligible = [i for i in range(len(self.unit_health)) if self.unit_health[i] > 0 and self.unitInAttack[i][0] == 1]
        enemy_eligible = [i for i in range(len(self.enemy_health)) if self.enemy_health[i] > 0 and self.enemyInAttack[i][0] == 1]
        active_label = self._side_label(active_side, manual=os.getenv("MANUAL_DICE", "0") == "1" and active_side == "enemy")
        self._log_phase_msg(
            active_label,
            "fight",
            "Начало Fight phase. Первым выбирает активный игрок. "
            f"Eligible MODEL: {[i + 21 for i in model_eligible]}, "
            f"Eligible ENEMY: {[i + 11 for i in enemy_eligible]}.",
        )

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
            self._log("⚔️ Combat resolution complete.\n")



    def step(self, action):
        reward = 0
        res = 0
        self.unitCharged = [0] * len(self.unit_health)
        self.enemyCharged = [0] * len(self.enemy_health)
        self.active_side = "model"
        battle_shock, delta = self.command_phase("model", action=action)
        reward += delta
        advanced_flags, delta = self.movement_phase("model", action=action, battle_shock=battle_shock)
        reward += delta
        reward += self.shooting_phase("model", advanced_flags=advanced_flags, action=action) or 0
        reward += self.charge_phase("model", advanced_flags=advanced_flags, action=action) or 0
        self.fight_phase("model")
        game_over, _, winner = apply_end_of_battle(self, log_fn=self._log)
        self.enemyStrat["overwatch"] = -1
        self.enemyStrat["smokescreen"] = -1

        for i in range(len(self.unit_health)):
            if self.unit_health[i] < 0:
                self.unit_health[i] = 0
        for i in range(len(self.enemy_health)):
            if self.enemy_health[i] < 0:
                self.enemy_health[i] = 0

        if game_over:
            res = 4
            if winner == "model":
                reward += 2
            elif winner == "enemy":
                reward -= 2

        self._advance_turn_order()
        if self.game_over and res == 0:
            res = 4

        self.iter += 1
        info = self.get_info()
        return self._get_observation(), reward, self.game_over, res, info

    # for a real person playing
    def player(self):
        self.enemyCP += 1
        self.modelCP += 1

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
            pos_before = tuple(self.enemy_coords[i])
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

                pos_after = tuple(self.enemy_coords[i])
                if pos_before != pos_after:
                    self._resolve_overwatch(
                        defender_side="model",
                        moving_unit_side="enemy",
                        moving_idx=i,
                        phase="movement",
                        manual=False,
                    )

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
                                    effect = self._maybe_use_smokescreen(
                                        defender_side="model",
                                        defender_idx=idOfE,
                                        phase="shooting",
                                        manual=False,
                                    )

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

                                dist_to_target = distance(self.enemy_coords[i], self.unit_coords[j])
                                self._log_unit_phase(
                                    self._side_label("enemy", manual=True),
                                    "charge",
                                    playerName,
                                    i,
                                    f"Charge объявлен по цели Model Unit {j + 21}. Дистанция: {dist_to_target:.1f}. Бросок 2D6: {roll[0]} + {roll[1]} = {sum(roll)}.",
                                )
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
                                    pos_after = tuple(self.enemy_coords[i])
                                    self._log_unit_phase(
                                        self._side_label("enemy", manual=True),
                                        "charge",
                                        playerName,
                                        i,
                                        f"Charge move: from {pos_before} -> {pos_after}, ended_in_engagement={self.enemyInAttack[i][0] == 1}.",
                                    )
                                    # 10e: Heroic Intervention доступен защитнику после успешного charge move.
                                    self._resolve_heroic_intervention(
                                        defender_side="model",
                                        charging_side="enemy",
                                        charging_idx=i,
                                        phase="charge",
                                        manual=False,
                                    )
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

        apply_end_of_battle(self, log_fn=self._log)

        for k in range(len(self.enemy_health)):
            if self.enemy_health[k] < 0:
                self.enemy_health[k] = 0

        self.iter += 1
        info = self.get_info()
        return self.game_over, info

    def player(self):
        self.active_side = "enemy"

        info = self.get_info()
        if self.playType is False:
            self._log(str(info))
        else:
            moreInfo = "Model Unit Health: {}, Player Unit Health: {}\nModel CP: {}, Player CP: {}\nModel VP: {}, Player VP: {}\n".format(
                info["model health"], info["player health"], info["modelCP"], info["playerCP"], info["model VP"], info["player VP"]
            )
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
                    info = self.get_info()
                    return self.game_over, info
                else:
                    sendToGUI("Its a yes or no question dude...: ")
                    ans = recieveGUI()

        battle_shock = self.command_phase("enemy", manual=True)
        if self.game_over:
            info = self.get_info()
            return self.game_over, info

        advanced_flags = self.movement_phase("enemy", manual=True, battle_shock=battle_shock)
        if self.game_over:
            info = self.get_info()
            return self.game_over, info

        self.shooting_phase("enemy", advanced_flags=advanced_flags, manual=True)
        if self.game_over:
            info = self.get_info()
            return self.game_over, info

        self.charge_phase("enemy", advanced_flags=advanced_flags, manual=True)
        if self.game_over:
            info = self.get_info()
            return self.game_over, info

        self.fight_phase("enemy")
        apply_end_of_battle(self, log_fn=self._log)

        if self.modelStrat["overwatch"] != -1:
            self.modelStrat["overwatch"] = -1
        if self.modelStrat["smokescreen"] != -1:
            self.modelStrat["smokescreen"] = -1

        self._advance_turn_order()
        apply_end_of_battle(self, log_fn=self._log)

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

        return np.array(obs, dtype=np.float32)
