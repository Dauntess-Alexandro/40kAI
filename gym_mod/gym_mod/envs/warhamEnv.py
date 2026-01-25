import gymnasium as gym
from gymnasium import spaces
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
import random
import re
from typing import Optional

from ..engine.utils import *
from ..engine import utils as engine_utils
from gym_mod.engine.mission import (
    MISSION_NAME,
    MAX_BATTLE_ROUNDS,
    score_end_of_command_phase,
    apply_end_of_battle,
)
from gym_mod.engine.skills import apply_end_of_command_phase
from gym_mod.engine.logging_utils import format_unit
from gym_mod.engine.state_export import write_state_json
from gym_mod.engine.game_io import get_active_io

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

    io = get_active_io()

    def ask_one(idx: Optional[int] = None):
        suffix = f" {idx}/{num}" if idx is not None else ""
        while True:
            v = io.request_int(f"Введи результат броска{suffix} (1..{max}): ", min_value=1, max_value=max)
            if v is None:
                io.log("Нужно число в допустимом диапазоне.")
                continue
            if 1 <= v <= max:
                return v
            io.log(f"Должно быть от 1 до {max}.")

    if num == 1:
        return ask_one()

    while True:
        rolls = io.request_dice(
            f"Введи {num} результатов (1..{max}) через пробел или запятую: ",
            count=num,
            min_value=1,
            max_value=max,
        )
        if rolls is None:
            io.log(
                f"Ошибка ввода кубов: нужно ввести {num} значений от 1 до {max}. "
                "Где: ввод кубов. Что делать дальше: повторите ввод."
            )
            continue
        return rolls


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
        self._io = get_active_io()

    def _log(self, message: str):
        self._io.log(message)

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
        self._log(f"\n🎲 Бросок {label}: {num}D{max}")
        res = self.base(num=num, max=max)
        vals = [res] if isinstance(res, int) else list(res)
        self.calls.append({"label": label, "num": num, "max": max, "vals": vals})
        return res
    def print_melee_report(self, weapon: dict, attacker_data: dict, defender_data: dict, dmg_list, effect=None):
        self._log("\n📌 --- ОТЧЁТ ПО БОЮ (MELEE) ---")

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
        self._log(f"Оружие: {wname}")
        if ws is not None:
            self._log(f"WS бойца: {ws}+")
        if s is not None and t is not None:
            self._log(f"S vs T: {s} vs {t}  -> базово ранение на {_wound_target(s, t)}+")
        if sv is not None:
            inv_txt = f"{inv}+" if inv is not None else "нет"
            self._log(f"Save цели: {sv}+ (invul: {inv_txt})")
        if ap_val != 0:
            self._log(f"AP: {ap_val}")
        if lethal:
            self._log("Абилка: Lethal Hits (6 на попадание = авто-ранение)")
        if effect:
            self._log(f"Эффект: {effect}")

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
            self._log(f"Hit rolls:    {hit_rolls}{suf}")

        if wound_rolls:
            if wt is not None:
                self._log(f"Wound rolls:  {wound_rolls}  (цель {wt}+) -> wounds: {rolled_wounds}")
            else:
                self._log(f"Wound rolls:  {wound_rolls}")

        if save_rolls:
            if save_target is not None:
                fs = failed_saves if failed_saves is not None else "??"
                self._log(f"Save rolls:   {save_rolls}  (цель {save_target}+) -> failed saves: {fs}")
            else:
                self._log(f"Save rolls:   {save_rolls}")

        self._log(f"\n✅ Итог по движку: прошло урона = {total_damage}")
        self._log("📌 -------------------------\n")





    def print_shoot_report(self, weapon: dict, attacker_data: dict, defender_data: dict, dmg_list, effect=None):
        self._log("\n📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---")

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

        self._log(f"Оружие: {wname}")
        if bs is not None:
            self._log(f"BS оружия: {bs}+")
        if s is not None and t is not None:
            self._log(f"S vs T: {s} vs {t}  -> базово ранение на {_wound_target(s, t)}+")
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
            self._log(f"Save цели: {sv}+ (invul: {inv_txt})")

        if ap_val != 0:
            self._log(f"AP: {ap_val}")

        if rf:
            self._log(f"Правило: Rapid Fire {rf} (если цель в половине дальности: +{rf} атак)")
        if lethal:
            self._log("Правило: Lethal Hits (крит-хиты авто-ранят)")
        if effect:
            self._log(f"Эффект: {effect}")

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
            self._log(f"\nAttacks roll: {atk_rolls}")
        if hit_rolls:
            extra = ""
            if hits is not None:
                extra = f"  -> hits: {hits}"
                if crit_hits is not None and crit_hits > 0:
                    extra += f" (crits: {crit_hits})"
            self._log(f"Hit rolls:    {hit_rolls}{extra}")

        if wound_rolls:
            if wt is not None and rolled_wounds is not None:
                if lethal and auto_wounds:
                    self._log(f"Wound rolls:  {wound_rolls}  (цель {wt}+) -> rolled wounds: {rolled_wounds} + auto(w/LETHAL): {auto_wounds} = {total_wounds}")
                else:
                    self._log(f"Wound rolls:  {wound_rolls}  (цель {wt}+) -> wounds: {rolled_wounds}")
            else:
                self._log(f"Wound rolls:  {wound_rolls}")

        if save_rolls:
            if save_target is not None:
                fs = failed_saves if failed_saves is not None else "??"
                self._log(f"Save rolls:   {save_rolls}  (цель {save_target}+) -> failed saves: {fs}")
            else:
                self._log(f"Save rolls:   {save_rolls}")

        self._log(f"\n✅ Итог по движку: прошло урона = {total_damage}")
        self._log("📌 -------------------------\n")

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
        get_active_io().log(f"Action keys: {self.action_space.spaces.keys()}")

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
        if self._is_verbose():
            return True
        return self.trunc is False

    def _is_verbose(self) -> bool:
        return os.getenv("VERBOSE_LOGS", "0") == "1" or os.getenv("MANUAL_DICE", "0") == "1"

    def _ensure_io(self):
        if not hasattr(self, "io") or self.io is None:
            self.io = get_active_io()
        return self.io

    def _log(self, msg: str, verbose_only: bool = False):
        if verbose_only and not self._is_verbose():
            return
        if not self._should_log():
            return
        self._ensure_io().log(msg)

    def _log_phase(self, side: str, phase: str):
        if not self._should_log():
            return
        phase_title = {
            "command": "ФАЗА КОМАНДОВАНИЯ",
            "movement": "ФАЗА ДВИЖЕНИЯ",
            "shooting": "ФАЗА СТРЕЛЬБЫ",
            "charge": "ФАЗА ЧАРДЖА",
            "fight": "ФАЗА БОЯ",
        }.get(phase, f"ФАЗА {phase.upper()}")
        self._log(f"--- {phase_title} ---")

    def _log_unit(self, side: str, unit_id: int, unit_idx: int, msg: str):
        if not self._should_log():
            return
        side_label = self._side_label(side)
        unit_label = self._format_unit_label(side, unit_idx, unit_id=unit_id)
        self._log(f"[{side_label}] {unit_label}: {msg}")

    def _display_side(self, side: str) -> str:
        if side == "enemy":
            return "PLAYER"
        if side == "model":
            return "MODEL"
        return side.upper()

    def _side_label(self, side: str, manual: bool = False) -> str:
        _ = manual
        return self._display_side(side)

    def _log_phase_msg(self, side_label: str, phase: str, msg: str):
        if not self._should_log():
            return
        self._log(f"[{side_label}][{phase.upper()}] {msg}")

    def _log_unit_phase(self, side_label: str, phase: str, unit_id: int, unit_idx: int, msg: str):
        if not self._should_log():
            return
        unit_label = self._format_unit_label(
            "model" if side_label == "MODEL" else "enemy",
            unit_idx,
            unit_id=unit_id,
        )
        self._log(f"[{side_label}][{phase.upper()}] {unit_label}: {msg}")

    def _log_action(self, side: str, unit_idx: int, msg: str, phase: str = None, verbose_only: bool = False):
        side_label = self._side_label(side)
        unit_label = self._format_unit_label(side, unit_idx)
        phase_prefix = f"[{phase.upper()}] " if phase else ""
        self._log(f"[{side_label}] {phase_prefix}{unit_label}: {msg}", verbose_only=verbose_only)

    def _log_rule(
        self,
        side: str,
        unit_idx: int,
        rule_name: str,
        details: str,
        phase: str = None,
        verbose_only: bool = False,
    ):
        rule_msg = f"Правило/стратагема «{rule_name}»: {details}"
        self._log_action(side, unit_idx, rule_msg, phase=phase, verbose_only=verbose_only)

    def _log_range(self, weapon: dict, dist: float, weapon_range: float, half_range: float, rapid_fire_on: bool):
        weapon_name = weapon.get("Name", "оружие") if isinstance(weapon, dict) else "оружие"
        rapid_text = "да" if rapid_fire_on else "нет"
        self._log(
            f"[Дальность] {weapon_name}: дистанция={dist:.1f}, range={weapon_range}, half={half_range}, rapid_fire={rapid_text}",
            verbose_only=True,
        )

    def _unit_id(self, side: str, unit_idx: int) -> int:
        side = side.lower()
        return (21 + unit_idx) if side == "model" else (11 + unit_idx)

    def _get_unit_data(self, side: str, unit_idx: int):
        side = side.lower()
        data_list = self.unit_data if side == "model" else self.enemy_data
        if 0 <= unit_idx < len(data_list):
            return data_list[unit_idx]
        return None

    def _format_unit_label(self, side: str, unit_idx: int, unit_id: int = None) -> str:
        side = side.lower()
        unit_id = unit_id if unit_id is not None else self._unit_id(side, unit_idx)
        unit_data = self._get_unit_data(side, unit_idx)
        return format_unit(
            unit_id,
            unit_data,
            include_instance_id=self._is_verbose(),
        )

    def _format_unit_choices(self, side: str, indices: list[int]) -> str:
        return ", ".join(self._format_unit_label(side, idx) for idx in indices)

    def _get_input(self, prompt: str) -> str:
        return str(self._ensure_io().request_choice(prompt, []))

    def _request_choice(self, prompt: str, options: list[str]):
        return self._ensure_io().request_choice(prompt, options)

    def _request_bool(self, prompt: str):
        return self._ensure_io().request_bool(prompt)

    def _request_int(self, prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None):
        return self._ensure_io().request_int(prompt, min_value=min_value, max_value=max_value)

    def _request_direction(self, prompt: str, options: list[str]):
        return self._ensure_io().request_direction(prompt, options)

    def _prompt_choice(self, prompt: str, allowed: dict, normalize: dict, allow_quit: bool = True):
        allowed_labels = ", ".join(allowed.values())
        options = list(allowed.keys())
        while True:
            response = self._request_choice(prompt, options)
            if response is None:
                if allow_quit:
                    return None
                self._log(f"Неверный ввод (доступно: {allowed_labels}).")
                continue
            response = str(response).strip().lower()
            if allow_quit and response in ("quit", "q"):
                return None
            if response in normalize:
                response = normalize[response]
            if response in allowed:
                return response
            self._log(f"Неверный ввод (доступно: {allowed_labels}): {response}")

    def _prompt_yes_no(self, prompt: str, allow_quit: bool = True):
        response = self._request_bool(prompt)
        if response is None and allow_quit:
            return None
        return bool(response)

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
            self._log_rule(
                defender_side,
                defender_idx,
                "Smokescreen",
                "Условие: есть SMOKE и 1 CP. Результат: недостаточно CP.",
                phase=phase,
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

        self._log_rule(
            defender_side,
            defender_idx,
            "Smokescreen",
            "Триггер: выбран в качестве цели. Стоимость: -1 CP. Эффект: benefit of cover до конца атаки.",
            phase=phase,
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
        candidates = self._collect_overwatch_candidates(defender_side, moving_unit_side, moving_idx)
        if not candidates:
            self._log_phase_msg(side_label, phase, "Overwatch невозможен: нет доступных стреляющих юнитов.")
            return

        cp = self.modelCP if defender_side == "model" else self.enemyCP
        if cp < 1:
            self._log_phase_msg(side_label, phase, "Overwatch невозможен: недостаточно CP.")
            return

        target_label = self._format_unit_label(moving_unit_side, moving_idx)
        self._log_phase_msg(
            side_label,
            phase,
            f"Триггер Overwatch: цель переместилась. Цель: {target_label}.",
        )

        use_it = True
        chosen = candidates[0]
        if manual:
            ids = [c + (21 if defender_side == "model" else 11) for c in candidates]
            candidates_label = self._format_unit_choices(defender_side, candidates)
            strat = self._prompt_yes_no(
                f"Использовать Overwatch (1 CP)? Доступные юниты: {candidates_label}. (y/n): "
            )
            if strat is None:
                self.game_over = True
                return
            if not strat:
                return
            choice = self._request_choice(
                "Введите номер юнита для Overwatch: ",
                [str(unit_id) for unit_id in ids],
            )
            if choice is None:
                self.game_over = True
                return
            choice = str(choice).strip()
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
        self._log_rule(
            defender_side,
            chosen,
            "Overwatch",
            f"Цель: {target_label}. Стоимость: -1 CP. Итоговый урон: {float(np.sum(dmg))}.",
            phase=phase,
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
            self._log_phase_msg(side_label, phase, "Heroic Intervention недоступен: нет подходящих юнитов в 6\".")
            return

        if defender_cp < 2:
            self._log_phase_msg(side_label, phase, "Heroic Intervention недоступен: недостаточно CP.")
            return

        unit_choices = self._format_unit_choices(defender_side, eligible)
        self._log_phase_msg(side_label, phase, f"Доступные юниты для Heroic Intervention: {unit_choices}.")

        use_it = True
        chosen = eligible[0]
        if manual:
            strat = self._prompt_yes_no("Использовать Heroic Intervention (2 CP)? (y/n): ")
            if strat is None:
                self.game_over = True
                return
            if not strat:
                return
            ids = [c + (21 if defender_side == "model" else 11) for c in eligible]
            choice = self._request_choice(
                "Введите номер юнита для Heroic Intervention: ",
                [str(unit_id) for unit_id in ids],
            )
            if choice is None:
                self.game_over = True
                return
            choice = str(choice).strip()
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
            response = self._request_int(prompt, min_value=min_val, max_value=max_val)
            if response is None and allow_quit:
                return None
            if response is not None:
                value = int(response)
                if min_val <= value <= max_val:
                    return value
                self._log(f"Значение вне диапазона ({min_val}..{max_val}): {value}")
            else:
                self._log("Это не число, попробуйте снова.")

    def begin_phase(self, side: str, phase: str):
        self.active_side = side
        self.phase = phase
        if not self._round_banner_shown:
            self._log(f"=== БОЕВОЙ РАУНД {self.battle_round} ===")
            self._round_banner_shown = True
        if phase == "command":
            self._log(f"--- ХОД {self._side_label(side)} ---")
            if side == "model":
                self.unitFellBack = [False] * len(self.unit_health)
            elif side == "enemy":
                self.enemyFellBack = [False] * len(self.enemy_health)
        self._log_phase(self._side_label(side), phase)

    def _end_battle_round(self):
        self._log(f"=== КОНЕЦ БОЕВОГО РАУНДА {self.battle_round} ===")
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
                unit_label = self._format_unit_label("model", i)
                if self.unit_health[i] <= 0:
                    self.modelOC[i] = 0
                    continue
                self.modelOC[i] = self.unit_data[i]["OC"]
                if isBelowHalfStr(self.unit_data[i], self.unit_health[i]) is True and self.unit_health[i] > 0:
                    if self.trunc is False:
                        self._log(f"{unit_label}: ниже половины состава, тест Battle-shock.")
                        self._log("Бросок 2D6...", verbose_only=True)
                    diceRoll = dice(num=2)
                    if self.trunc is False:
                        self._log(f"Бросок: {diceRoll[0]} {diceRoll[1]}", verbose_only=True)
                    if sum(diceRoll) >= self.unit_data[i]["Ld"]:
                        self.modelOC[i] = self.unit_data[i]["OC"]
                        if self.trunc is False:
                            self._log(f"{unit_label}: тест Battle-shock пройден.")
                    else:
                        battle_shock[i] = True
                        self.modelOC[i] = 0
                        if self.trunc is False:
                            self._log(f"{unit_label}: тест Battle-shock провален.")
                        if action and action.get("use_cp") == 1 and action.get("cp_on") == i:
                            if self.modelCP - 1 >= 0:
                                battle_shock[i] = False
                                reward_delta += 0.5
                                self.modelCP -= 1
                                if self.trunc is False:
                                    self._log(f"{unit_label}: применена Insane Bravery (-1 CP), тест пройден.")
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
                unit_label = self._format_unit_label("enemy", i, unit_id=playerName)
                if self.enemy_health[i] <= 0:
                    self.enemyOC[i] = 0
                    battle_shock[i] = False
                    continue
                self.enemyOC[i] = self.enemy_data[i]["OC"]
                if isBelowHalfStr(self.enemy_data[i], self.enemy_health[i]) is True and self.enemy_health[i] > 0:
                    self._log(f"{unit_label}: ниже половины состава, тест Battle-shock.")
                    self._log("Бросок 2D6...", verbose_only=True)
                    diceRoll = player_dice(num=2)
                    self._log(f"Бросок: {diceRoll[0]} {diceRoll[1]}", verbose_only=True)
                    if sum(diceRoll) >= self.enemy_data[i]["Ld"]:
                        self._log(f"{unit_label}: тест Battle-shock пройден.")
                        self.enemyOC[i] = self.enemy_data[i]["OC"]
                    else:
                        battleSh = True
                        self._log(f"{unit_label}: тест Battle-shock провален.")
                        self.enemyOC[i] = 0
                        if self.enemyCP - 1 >= 0:
                            strat = self._prompt_yes_no(
                                f"{unit_label}. Использовать стратагему Insane Bravery (1 CP)? (y/n): "
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
                unit_label = self._format_unit_label("enemy", i)
                if self.enemy_health[i] <= 0:
                    self.enemyOC[i] = 0
                    battle_shock[i] = False
                    continue
                self.enemyOC[i] = self.enemy_data[i]["OC"]
                if isBelowHalfStr(self.enemy_data[i], self.enemy_health[i]) is True and self.enemy_health[i] > 0:
                    if self.trunc is False:
                        self._log(f"{unit_label}: ниже половины состава, тест Battle-shock.")
                        self._log("Бросок 2D6...", verbose_only=True)
                    diceRoll = dice(num=2)
                    if self.trunc is False:
                        self._log(f"Бросок: {diceRoll[0]} {diceRoll[1]}", verbose_only=True)
                    if sum(diceRoll) >= self.enemy_data[i]["Ld"]:
                        if self.trunc is False:
                            self._log(f"{unit_label}: тест Battle-shock пройден.")
                        self.enemyOC[i] = self.enemy_data[i]["OC"]
                    else:
                        battleSh = True
                        self.enemyOC[i] = 0
                        if self.trunc is False:
                            self._log(f"{unit_label}: тест Battle-shock провален.")
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
                            f"Цель в ближнем бою мертва ({self._format_unit_label('enemy', idOfE)}), юнит выходит из боя. Позиция: {pos_before}",
                        )
                    else:
                        if action["attack"] == 0:
                            if self.unit_health[i] * 2 >= self.enemy_health[idOfE]:
                                reward_delta -= 0.5
                            self._log_unit(
                                "MODEL",
                                modelName,
                                i,
                                f"Отступление из боя с {self._format_unit_label('enemy', idOfE)}. Позиция до: {pos_before}",
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
                                f"Остаётся в ближнем бою с {self._format_unit_label('enemy', idOfE)}, движение пропущено.",
                            )
            return advanced_flags, reward_delta

        if side == "enemy" and manual:
            direction_map = {"up": "up", "down": "down", "left": "left", "right": "right", "none": "none"}
            normalize = {"u": "up", "d": "down", "l": "left", "r": "right", "n": "none"}
            advanced_flags = [False] * len(self.enemy_health)
            for i in range(len(self.enemy_health)):
                playerName = i + 11
                battleSh = battle_shock[i] if battle_shock else False
                unit_label = self._format_unit_label("enemy", i, unit_id=playerName)
                pos_before = tuple(self.enemy_coords[i])
                if self.enemyInAttack[i][0] == 1 and self.enemy_health[i] > 0:
                    fall_back = self._prompt_yes_no(f"{unit_label}. Отступить (fallback)? (y/n): ")
                    if fall_back is None:
                        self.game_over = True
                        return None
                    if fall_back:
                        idOfE = self.enemyInAttack[i][1]
                        self._log(f"{unit_label} отступил из боя с {self._format_unit_label('model', idOfE)}")
                        self.enemyFellBack[i] = True
                        if battleSh is True:
                            diceRoll = dice()
                            if diceRoll < 3:
                                self.enemy_health[i] -= self.enemy_data[i]["W"]
                        self.enemy_coords[i][0] += self.enemy_data[i]["Movement"]
                        self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                        self.enemyInAttack[i] = [0, 0]
                        self.unitInAttack[idOfE][0] = 0
                        self.unitInAttack[idOfE][1] = 0
                        pos_after = tuple(self.enemy_coords[i])
                        self._log(f"{unit_label}: отступление завершено. Позиция после: {pos_after}")
                        self.updateBoard()
                        self.showBoard()
                    else:
                        idOfE = self.enemyInAttack[i][1]
                        self._log(
                            f"{unit_label} остаётся в бою с {self._format_unit_label('model', idOfE)} (будет драться в фазе боя)."
                        )
                    continue

                if self.enemyInAttack[i][0] == 0 and self.enemy_health[i] > 0:
                    self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                    for j in range(len(self.enemy_health)):
                        if self.enemy_coords[i] == self.unit_coords[j]:
                            self.enemy_coords[i][0] -= 1

                    self.updateBoard()
                    self.showBoard()

                    dire = self._prompt_choice(
                        f"Ход юнита: {unit_label}. Выберите направление (up/down/left/right/none): ",
                        direction_map,
                        normalize,
                    )
                    if dire is None:
                        self.game_over = True
                        return None

                    advanced = False
                    move_num = 0
                    if dire != "none":
                        adv = self._prompt_yes_no("Сделать Advance? (y/n): ")
                        if adv is None:
                            self.game_over = True
                            return None
                        if adv:
                            advanced = True
                            self._log("Бросок 1D6 на Advance...", verbose_only=True)
                            roll = player_dice()
                            self._log(f"Бросок: {roll}", verbose_only=True)
                            movement_cap = self.enemy_data[i]["Movement"] + roll
                        else:
                            movement_cap = self.enemy_data[i]["Movement"]
                        move_num = self._prompt_int(
                            f"На сколько дюймов двигаться (0..{movement_cap}): ",
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
                    valid_target_ids = shootAbleUnits
                    raw = action["shoot"]
                    if 0 <= raw < len(valid_target_ids):
                        idOfE = valid_target_ids[raw]
                        distances = {j: distance(self.unit_coords[i], self.enemy_coords[j]) for j in valid_target_ids}
                        closest = min(distances, key=distances.get)
                        min_hp = min(valid_target_ids, key=lambda idx: self.enemy_health[idx])
                        if idOfE == closest:
                            reason = "самая близкая"
                        elif idOfE == min_hp:
                            reason = "цель с меньшим HP"
                        else:
                            reason = "выбор политики"
                        target_list = self._format_unit_choices("enemy", valid_target_ids)
                        self._log_unit(
                            "MODEL",
                            modelName,
                            i,
                            f"Цели в дальности: {target_list}, выбрана: {self._format_unit_label('enemy', idOfE)} (причина: {reason})",
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
                            f"Итог урона по {self._format_unit_label('enemy', idOfE)}: {float(np.sum(dmg))}",
                        )
                        if self.trunc is False:
                            self._log(
                                f"{self._format_unit_label('model', i)} стреляет по {self._format_unit_label('enemy', idOfE)}: урон {float(np.sum(dmg))}."
                            )
                        else:
                            self.modelUpdates += "{} стреляет по {} {} раз(а)\n".format(
                                self._format_unit_label("model", i),
                                self._format_unit_label("enemy", idOfE),
                                sum(dmg),
                            )
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
                        target_list = self._format_unit_choices("enemy", valid_target_ids)
                        self._log_unit(
                            "MODEL",
                            modelName,
                            i,
                            f"Цели в дальности: {target_list}, выбрана недоступная цель (raw={raw}). Стрельба пропущена.",
                        )
                        if _verbose_logs_enabled():
                            self._log(
                                f"[MODEL][SHOOT] Невалидный выбор цели: raw={raw}, доступные={valid_target_ids} (ожидался индекс 0..{len(valid_target_ids) - 1}). Стрельба пропущена."
                            )
                        if self.trunc is False:
                            self._log(f"{self._format_unit_label('model', i)} не смог стрелять: выбранная цель недоступна.")
                else:
                    self._log_unit("MODEL", modelName, i, "Нет целей в дальности, стрельба пропущена.")
            return reward_delta
        elif side == "enemy" and manual:
            for i in range(len(self.enemy_health)):
                playerName = i + 11
                unit_label = self._format_unit_label("enemy", i, unit_id=playerName)
                advanced = advanced_flags[i] if advanced_flags else False
                if self.enemyFellBack[i]:
                    self._log(f"{unit_label}: отступил в этом ходу — стрельба пропущена.")
                    continue
                if self.enemy_weapon[i] != "None":
                    if advanced and not weapon_is_assault(self.enemy_weapon[i]):
                        self._log(f"{unit_label}: был Advance без Assault — стрельба пропущена.")
                    else:
                        shootAble = np.array([])
                        for j in range(len(self.unit_health)):
                            if distance(self.enemy_coords[i], self.unit_coords[j]) <= self.enemy_weapon[i]["Range"] and self.unit_health[j] > 0 and self.unitInAttack[j][0] == 0:
                                shootAble = np.append(shootAble, j)
                        if len(shootAble) > 0:
                            response = False
                            while response is False:
                                targets_label = self._format_unit_choices("model", shootAble.astype(int).tolist())
                                options = [str(21 + int(idx)) for idx in shootAble.astype(int).tolist()]
                                shoot = self._request_choice(
                                    f"Выберите цель для стрельбы. Стреляет: {unit_label}. Доступные цели: {targets_label}. Введите ID цели: ",
                                    options,
                                )
                                if shoot is None:
                                    self.game_over = True
                                    return None
                                shoot_value = str(shoot).strip()
                                if is_num(shoot_value) is True and int(shoot_value) - 21 in shootAble:
                                    idOfE = int(shoot_value) - 21
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
                                    self._log(
                                        f"{unit_label} нанёс {sum(dmg)} урона по {self._format_unit_label('model', idOfE)}"
                                    )
                                    logger.print_shoot_report(
                                        weapon=self.enemy_weapon[i],
                                        attacker_data=self.enemy_data[i],
                                        defender_data=self.unit_data[idOfE],
                                        dmg_list=dmg,
                                        effect=effect,
                                    )
                                    response = True
                                else:
                                    self._log("Недоступная цель, попробуйте снова.")
                else:
                    self._log("Нет доступного оружия для стрельбы.")
        elif side == "enemy":
            for i in range(len(self.enemy_health)):
                advanced = advanced_flags[i] if advanced_flags else False
                if self.enemyFellBack[i]:
                    if self.trunc is False:
                        self._log(f"{self._format_unit_label('enemy', i)}: отступил — стрельба пропущена.")
                    continue
                if self.enemy_weapon[i] != "None":
                    if advanced and not weapon_is_assault(self.enemy_weapon[i]):
                        if self.trunc is False:
                            self._log(f"{self._format_unit_label('enemy', i)}: Advance без Assault — стрельба пропущена.")
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
                                self._log(
                                    f"{self._format_unit_label('enemy', i)} стреляет по {self._format_unit_label('model', idOfM)}: урон {float(np.sum(dmg))}."
                                )
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
                            target_list = self._format_unit_choices("enemy", potential_targets)
                            self._log_unit(
                                "MODEL",
                                modelName,
                                i,
                                f"Доступные цели для чарджа: {target_list}. Решение: пропуск чарджа.",
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
                        target_list = self._format_unit_choices("enemy", chargeAble)
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
                                f"Charge объявлен по цели {self._format_unit_label('enemy', idOfE)}. Дистанция: {dist_to_target:.1f}. Бросок 2D6: {dice_vals[0]} + {dice_vals[1]} = {diceRoll}.",
                            )
                            self._log_unit(
                                "MODEL",
                                modelName,
                                i,
                                f"Чардж цели: {target_list}, выбрана {self._format_unit_label('enemy', idOfE)} (dist={dist_to_target:.1f}). {roll_text}. Результат: успех.",
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
                                f"Движение чарджа: {pos_before} -> {pos_after}, в контакте={self.unitInAttack[i][0] == 1}.",
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
                                    f"Charge объявлен по цели {self._format_unit_label('enemy', idOfE)}. Дистанция: {dist_to_target:.1f}. Бросок 2D6: {dice_vals[0]} + {dice_vals[1]} = {diceRoll}.",
                                )
                            target_list = self._format_unit_choices("enemy", potential_targets)
                            self._log_unit(
                                "MODEL",
                                modelName,
                                i,
                                f"Чардж цели: {target_list}, выбрана {self._format_unit_label('enemy', idOfE)}. {roll_text}. Результат: провал ({reason}).",
                            )
                            reward_delta -= 0.5
                    else:
                        if potential_targets:
                            target_list = self._format_unit_choices("enemy", potential_targets)
                            if _verbose_logs_enabled():
                                roll_text = f"бросок: {dice_vals[0]} + {dice_vals[1]} = {diceRoll}"
                            else:
                                roll_text = f"бросок total={diceRoll}"
                            self._log_unit(
                                "MODEL",
                                modelName,
                                i,
                                f"Цели в 12\": {target_list}. {roll_text}. Нет достижимых целей.",
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
                unit_label = self._format_unit_label("enemy", i, unit_id=playerName)
                advanced = advanced_flags[i] if advanced_flags else False
                pos_before = tuple(self.enemy_coords[i])
                if self.enemyFellBack[i]:
                    self._log(f"{unit_label}: отступил в этом ходу — чардж пропущен.")
                    continue
                if advanced:
                    self._log(f"{unit_label}: был Advance — чардж невозможен.")
                    continue
                charg = np.array([])
                for j in range(len(self.unit_health)):
                    if distance(self.unit_coords[j], self.enemy_coords[i]) <= 12 and self.unitInAttack[j][0] == 0 and self.unit_health[j] > 0:
                        charg = np.append(charg, j)
                if len(charg) > 0:
                    any_chargeable = True
                    want_charge = self._prompt_yes_no(f"{unit_label}. Объявить чардж? (y/n): ")
                    if want_charge is None:
                        self.game_over = True
                        return None
                    if not want_charge:
                        self._log(f"{unit_label} решил пропустить чардж.")
                        continue
                    response = False
                    while response is False:
                        targets_label = self._format_unit_choices("model", charg.astype(int).tolist())
                        options = [str(21 + int(idx)) for idx in charg.astype(int).tolist()]
                        attk = self._request_choice(
                            f"Выберите цель для чарджа. Доступные цели: {targets_label}. Введите ID цели: ",
                            options,
                        )
                        if attk is None:
                            self.game_over = True
                            return None
                        attk_value = str(attk).strip()
                        if is_num(attk_value) is True and int(attk_value) - 21 in charg:
                            response = True
                            j = int(attk_value) - 21
                            self._log("Бросок 2D6...", verbose_only=True)
                            roll = player_dice(num=2)
                            self._log(f"Бросок: {roll[0]} и {roll[1]}", verbose_only=True)
                            dist_to_target = distance(self.enemy_coords[i], self.unit_coords[j])
                            self._log_unit_phase(
                                self._side_label("enemy", manual=True),
                                "charge",
                                playerName,
                                i,
                                f"Charge объявлен по цели {self._format_unit_label('model', j)}. Дистанция: {dist_to_target:.1f}. Бросок 2D6: {roll[0]} + {roll[1]} = {sum(roll)}.",
                            )
                            if distance(self.enemy_coords[i], self.unit_coords[j]) - sum(roll) <= 5:
                                self._log(f"{unit_label} успешно зачарджил {self._format_unit_label('model', j)}")
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
                                    f"Движение чарджа: {pos_before} -> {pos_after}, в контакте={self.enemyInAttack[i][0] == 1}.",
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
                                self._log(f"{unit_label} не смог зачарджить {self._format_unit_label('model', j)}")
                        else:
                            self._log("Недоступная цель.")
            if not any_chargeable:
                self._log("Нет доступных целей для чарджа.")
        elif side == "enemy":
            for i in range(len(self.enemy_health)):
                advanced = advanced_flags[i] if advanced_flags else False
                pos_before = tuple(self.enemy_coords[i])
                if self.enemyFellBack[i]:
                    if self.trunc is False:
                        self._log(f"{self._format_unit_label('enemy', i)}: отступил — чардж невозможен.")
                    continue
                if advanced:
                    if self.trunc is False:
                        self._log(f"{self._format_unit_label('enemy', i)}: был Advance — чардж невозможен.")
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
                            self._display_side("enemy"),
                            "charge",
                            i + 21,
                            i,
                            f"Charge объявлен по цели {self._format_unit_label('model', idOfM)}. Дистанция: {dist:.1f}. Бросок 2D6: {diceRoll}.",
                        )
                        if diceRoll >= required:
                            if self.trunc is False:
                                self._log(
                                    f"{self._format_unit_label('enemy', i)} успешно зачарджил {self._format_unit_label('model', idOfM)} (бросок {diceRoll} vs нужно {required:.1f})"
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
                                self._display_side("enemy"),
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
                                f"{self._format_unit_label('enemy', i)} не смог зачарджить {self._format_unit_label('model', idOfM)} (бросок {diceRoll} vs нужно {required:.1f})"
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
                model_list = self._format_unit_choices("model", engaged_model)
                enemy_list = self._format_unit_choices("enemy", engaged_enemy)
                self._log(f"[MODEL] Ближний бой: участвуют {model_list}; противники {enemy_list}")
                for idx in engaged_model:
                    def_idx = self.unitInAttack[idx][1]
                    if 0 <= def_idx < len(self.enemy_health):
                        self._log_unit(
                            "MODEL",
                            idx + 21,
                            idx,
                            f"В бою с {self._format_unit_label('enemy', def_idx)}",
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
                    f"Выбран для атаки. Цель: {self._format_unit_label('enemy', def_idx)}.",
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
                _log(
                    f"⚔️ {self._format_unit_label('model', att_idx)} атакует {self._format_unit_label('enemy', def_idx)} оружием {wname}: урон {float(np.sum(dmg))} | HP {hp_before} -> {modHealth}"
                )
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
                    f"Выбран для атаки. Цель: {self._format_unit_label('model', def_idx)}.",
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
                _log(
                    f"⚔️ {self._format_unit_label('enemy', att_idx)} атакует {self._format_unit_label('model', def_idx)} оружием {wname}: урон {float(np.sum(dmg))} | HP {hp_before} -> {modHealth}"
                )
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

        manual_enemy = bool(getattr(self, "playType", False))

        def _prompt_enemy_attacker(eligible_indices: list[int]) -> Optional[int]:
            if not eligible_indices:
                return None
            unit_choices = self._format_unit_choices("enemy", eligible_indices)
            self._log("ФАЗА БОЯ (Игрок): выберите атакующего юнита")
            self._log("ФАЗА БОЯ: ожидается выбор атакующего юнита")
            options = [str(11 + idx) for idx in eligible_indices]
            while True:
                choice = self._request_choice(
                    f"ФАЗА БОЯ: выбери юнита для атаки. Доступные: {unit_choices}. Введите ID юнита: ",
                    options,
                )
                if choice is None:
                    self.game_over = True
                    return None
                choice_value = str(choice).strip()
                if is_num(choice_value) and int(choice_value) - 11 in eligible_indices:
                    return int(choice_value) - 11
                self._log(f"Неверный ввод: выберите юнита из списка {unit_choices}.")

        def _prompt_enemy_target(att_idx: int) -> Optional[int]:
            def_idx = self.enemyInAttack[att_idx][1]
            targets = []
            if 0 <= def_idx < len(self.unit_health) and self.unit_health[def_idx] > 0:
                targets = [def_idx]
            if not targets:
                self._log("Целей для атаки нет: бой пропущен.")
                return None
            target_choices = self._format_unit_choices("model", targets)
            self._log("Выберите цель")
            self._log("ФАЗА БОЯ: ожидается выбор цели")
            options = [str(21 + idx) for idx in targets]
            while True:
                choice = self._request_choice(
                    f"Выберите цель. Доступные цели: {target_choices}. Введите ID цели: ",
                    options,
                )
                if choice is None:
                    self.game_over = True
                    return None
                choice_value = str(choice).strip()
                if is_num(choice_value) and int(choice_value) - 21 in targets:
                    return int(choice_value) - 21
                self._log(f"Неверный ввод: выберите цель из списка {target_choices}.")

        def _manual_enemy_attack(eligible_indices: list[int]) -> Optional[int]:
            while True:
                attacker_idx = _prompt_enemy_attacker(eligible_indices)
                if attacker_idx is None:
                    return None
                target_idx = _prompt_enemy_target(attacker_idx)
                if target_idx is None:
                    return None
                confirm = self._request_bool("Начать атаку? (y/n): ")
                if confirm is None:
                    self.game_over = True
                    return None
                if confirm:
                    return attacker_idx
                self._log("Атака отменена: выберите юнита и цель заново.")

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
            f"Eligible {self._display_side('enemy')}: {[i + 11 for i in enemy_eligible]}.",
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
            if manual_enemy:
                remaining = [i for i in chargers if i not in fought_enemy]
                while remaining:
                    attacker_idx = _manual_enemy_attack(remaining)
                    if attacker_idx is None:
                        return
                    if _do_melee("enemy", attacker_idx):
                        fought_enemy.add(attacker_idx)
                    remaining = [i for i in chargers if i not in fought_enemy]
            else:
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
                    if manual_enemy:
                        attacker_idx = _manual_enemy_attack(enemy_left)
                        if attacker_idx is None:
                            return
                        _do_melee("enemy", attacker_idx)
                        fought_enemy.add(attacker_idx)
                    else:
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

    def player(self):
        self.active_side = "enemy"

        info = self.get_info()
        self._log(str(info))
        more_info = "Здоровье MODEL: {}, здоровье PLAYER: {}\nCP MODEL: {}, CP PLAYER: {}\nVP MODEL: {}, VP PLAYER: {}\n".format(
            info["model health"],
            info["player health"],
            info["modelCP"],
            info["playerCP"],
            info["model VP"],
            info["player VP"],
        )
        if self.modelUpdates:
            self._log(more_info + self.modelUpdates)
        else:
            self._log(more_info)
        continue_game = self._request_bool("Продолжить? (y/n): ")
        if continue_game is None or not continue_game:
            self.game_over = True
            info = self.get_info()
            return self.game_over, info
        self.modelUpdates = ""

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

        write_state_json(self)

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

        health = "Здоровье MODEL: {}, CP: {}; здоровье {}: {}, CP {}\nVP {}".format(
            self.unit_health,
            self.modelCP,
            self._display_side("enemy"),
            self.enemy_health,
            self.enemyCP,
            [self.modelVP, self.enemyVP],
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
            output_dir = "display"
            os.makedirs(output_dir, exist_ok=True)
            fileName = os.path.join(output_dir, f"{self.restarts}_{self.iter}.png")
        else:
            output_dir = os.path.join("gui", "build", "img")
            legacy_dir = os.path.join("gui", "img")
            os.makedirs(output_dir, exist_ok=True)
            os.makedirs(legacy_dir, exist_ok=True)
            fileName = os.path.join(output_dir, "board.png")
            fig.savefig(os.path.join(legacy_dir, "board.png"))

        fig.savefig(fileName)
        ax.cla()
        plt.close(fig)
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
