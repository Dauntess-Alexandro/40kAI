import gymnasium as gym
from gymnasium import spaces
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import datetime
import os
import random
import re
import sys
import time
from typing import Optional

import reward_config as reward_cfg

from ..engine.utils import *
from ..engine.visibility import visibility_report
from ..engine import utils as engine_utils
from gym_mod.engine.mission import (
    MISSION_NAME,
    MAX_BATTLE_ROUNDS,
    apply_mission_layout,
    score_end_of_command_phase,
    apply_end_of_battle,
    controlled_objectives,
    terrain_cells_from_features,
)
from gym_mod.engine.skills import apply_end_of_command_phase
from gym_mod.engine.logging_utils import format_unit
from gym_mod.engine.state_export import write_state_json
from gym_mod.engine.game_io import get_active_io
from gym_mod.engine.event_bus import get_event_bus, get_event_recorder

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

    if num == 1:
        while True:
            rolls = io.request_dice(
                f"Введи 1 результат (1..{max}) через пробел или запятую: ",
                count=1,
                min_value=1,
                max_value=max,
            )
            if not rolls:
                io.log(
                    f"Ошибка ввода кубов: нужно ввести 1 значение от 1 до {max}. "
                    "Где: ввод кубов. Что делать дальше: повторите ввод."
                )
                continue
            try:
                return int(rolls[0])
            except (TypeError, ValueError, IndexError):
                io.log(
                    f"Ошибка ввода кубов: некорректное значение {rolls}. "
                    "Где: ввод кубов. Что делать дальше: повторите ввод."
                )
                continue

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

def _fight_report_enabled() -> bool:
    """
    Подробный отчёт ближнего боя. По умолчанию выключен.
    Включаем: FIGHT_REPORT=1.
    """
    return os.getenv("FIGHT_REPORT", "0") == "1"

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

    def __init__(self, base_roller, agent_log_fn=None):
        self.base = base_roller
        self.calls = []
        self.labels = []
        self.has_attack_count_roll = False
        self._io = get_active_io()
        self._agent_log_fn = agent_log_fn

    def _log(self, message: str):
        self._io.log(message)

    def _append_agent_log(self, msg: str):
        if msg is None:
            return
        if callable(self._agent_log_fn):
            try:
                self._agent_log_fn(msg)
            except Exception:
                return

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
    def print_melee_report(
        self,
        weapon: dict,
        attacker_data: dict,
        defender_data: dict,
        dmg_list,
        effect=None,
        report_title: Optional[str] = None,
        attacker_label: Optional[str] = None,
        defender_label: Optional[str] = None,
        extra_rules: Optional[list[str]] = None,
        hp_before: Optional[float] = None,
        hp_after: Optional[float] = None,
        models_before: Optional[int] = None,
        models_after: Optional[int] = None,
    ):
        title = report_title or "ОТЧЁТ ПО БЛИЖНЕМУ БОЮ"
        self._log(f"\n📌 --- {title} ---")

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

        attack_raw = None
        if isinstance(weapon, dict):
            for k in ("A", "Attacks", "#Attacks", "Shots"):
                if k in weapon:
                    attack_raw = weapon.get(k)
                    break
        if attack_raw is None and isinstance(attacker_data, dict):
            for k in ("A", "Attacks"):
                if k in attacker_data:
                    attack_raw = attacker_data.get(k)
                    break

        damage_raw = None
        if isinstance(weapon, dict):
            for k in ("Damage", "D"):
                if k in weapon:
                    damage_raw = weapon.get(k)
                    break

        wname = weapon.get("Name", weapon) if isinstance(weapon, dict) else weapon
        if attacker_label or defender_label:
            parts = []
            if attacker_label:
                parts.append(f"Атакует: {attacker_label}")
            if defender_label:
                parts.append(f"цель: {defender_label}")
            self._log("; ".join(parts))
        self._log(f"Оружие: {wname}")
        if ws is not None:
            self._log(f"WS: {ws}+")
        if attack_raw is not None:
            self._log(f"A: {attack_raw}")
        if s is not None and t is not None:
            self._log(f"S vs T: {s} vs {t}  -> базово ранение на {_wound_target(s, t)}+")
        if sv is not None:
            inv_txt = f"{inv}+" if inv is not None else "нет"
            self._log(f"Save цели: {sv}+ (invul: {inv_txt})")
        if ap_val != 0 or damage_raw is not None:
            damage_text = damage_raw if damage_raw is not None else "?"
            self._log(f"AP: {ap_val}  Damage: {damage_text}")

        rules = []
        if lethal:
            rules.append("Lethal Hits (крит-хиты авто-ранят)")
        if extra_rules:
            rules.extend(extra_rules)
        if rules:
            self._log(f"Правила: {', '.join(rules)}")
        else:
            self._log("Правила: нет")
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
                extra.append(f"crits: {crit_hits}")
            suf = ("  -> " + ", ".join(extra)) if extra else ""
            self._log(f"Hit rolls:    {hit_rolls}{suf}")

        if wound_rolls:
            if wt is not None:
                if lethal and auto_wounds:
                    self._log(
                        f"Wound rolls:  {wound_rolls}  (цель {wt}+) -> rolled wounds: {rolled_wounds} + auto(w/LETHAL): {auto_wounds} = {total_wounds}"
                    )
                else:
                    self._log(f"Wound rolls:  {wound_rolls}  (цель {wt}+) -> wounds: {rolled_wounds}")
            else:
                self._log(f"Wound rolls:  {wound_rolls}")

        if save_rolls:
            if save_target is not None:
                fs = failed_saves if failed_saves is not None else "??"
                self._log(f"Save rolls:   {save_rolls}  (цель {save_target}+) -> failed: {fs}")
            else:
                self._log(f"Save rolls:   {save_rolls}")

        self._log(f"\n✅ Итог по движку: прошло урона = {total_damage}")
        if hp_before is not None and hp_after is not None:
            models_text = ""
            if models_before is not None and models_after is not None:
                models_text = f" ; модели цели: {models_before} -> {models_after}"
            self._log(f"HP цели: {hp_before} -> {hp_after}{models_text}")
        self._log("📌 -------------------------\n")





    def print_shoot_report(
        self,
        weapon: dict,
        attacker_data: dict,
        defender_data: dict,
        dmg_list,
        effect=None,
        report_title: Optional[str] = None,
        attacker_label: Optional[str] = None,
        defender_label: Optional[str] = None,
        extra_rules: Optional[list[str]] = None,
    ):
        title = report_title or "ОТЧЁТ ПО СТРЕЛЬБЕ"
        self._log(f"\n📌 --- {title} ---")

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

        if attacker_label or defender_label:
            parts = []
            if attacker_label:
                parts.append(f"Стреляет: {attacker_label}")
            if defender_label:
                parts.append(f"цель: {defender_label}")
            self._log("; ".join(parts))

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
            if effect == "benefit of cover":
                self._log("Benefit of Cover: активен (+1 к сейву цели против ranged).")
            else:
                self._log("Benefit of Cover: не активен.")

        if ap_val != 0:
            self._log(f"AP: {ap_val}")

        if rf:
            self._log(f"Правило: Rapid Fire {rf} (если цель в половине дальности: +{rf} атак)")
        if lethal:
            self._log("Правило: Lethal Hits (крит-хиты авто-ранят)")
        if extra_rules:
            for rule in extra_rules:
                self._log(f"Правило: {rule}")
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

        # TRAIN/EVAL: обычные _log-сообщения не всегда попадают в AGENT_LOG_FILE,
        # поэтому сохраняем компактный контекст расчёта сейва отдельной строкой.
        effect_norm = str(effect).strip().lower() if effect is not None else ""
        cover_active = effect_norm == "benefit of cover"
        self._append_agent_log(
            "SHOT_DEBUG | "
            f"attacker={attacker_label or '-'} target={defender_label or '-'} "
            f"effect={effect_norm or '-'} cover_active={1 if cover_active else 0} "
            f"save_base={sv if sv is not None else '-'} ap={ap_val} "
            f"inv={inv if inv is not None else '-'} "
            f"save_target={save_target if save_target is not None else '-'} "
            f"save_rolls={save_rolls if save_rolls else []}"
        )

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
        self._state_flush_last_ts = 0.0
        self._state_flush_pending = False
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
        self.unit_model_wounds = []
        self.enemy_model_wounds = []
        self.unit_anchor_coords = []
        self.enemy_anchor_coords = []
        self.unit_model_positions = []
        self.enemy_model_positions = []
        self.model_used_advance: list[bool] = []
        self.enemy_used_advance: list[bool] = []
        self.model_advance_roll: list[int | None] = []
        self.enemy_advance_roll: list[int | None] = []

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
        self._fight_env_logged = False
        self._phase_event_emitted = False
        self._phase_unit_logged = set()
        self.mission_name = MISSION_NAME
        apply_mission_layout(self)

        self._prev_vp_diff = 0
        self._objective_hold_streaks = [0] * len(self.coordsOfOM)
        self._target_cache_epoch = 0
        self._distance_cache = {}
        self._shoot_target_cache = {}
        self._shoot_target_reject_cache = {}
        self.terrain_features = list(getattr(self, "terrain_features", []) or [])
        self.terrain_opaque_cells: set[tuple[int, int]] = set()
        self.terrain_obscuring_cells: set[tuple[int, int]] = self.get_terrain_obscuring_cells_set()
        self.visibility_mode = str(os.getenv("VISIBILITY_MODE", "multi_ray_5") or "multi_ray_5").strip().lower()
        self._terrain_shaping_shot_bonus_units: set[int] = set()
        log_name = str(os.getenv("AGENT_LOG_FILE", "LOGS_FOR_AGENTS_PLAY.md") or "LOGS_FOR_AGENTS_PLAY.md")
        self._agent_log_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", log_name)
        )

        self.modelOC = []
        self.enemyOC = []
        self.modelUpdates = ""
        get_event_recorder().clear()

        for i in range(len(enemy)):
            self.enemy_weapon.append(enemy[i].showWeapon())
            self.enemy_melee.append(enemy[i].showMelee())
            self.enemy_data.append(enemy[i].showUnitData())
            self.enemy_coords.append([enemy[i].showCoords()[0], enemy[i].showCoords()[1]])
            self.enemy_health.append(enemy[i].showUnitData()["W"] * enemy[i].showUnitData()["#OfModels"])
            self.enemyInAttack.append([0, 0])
            self.enemyOC.append(enemy[i].showUnitData()["OC"])
        self.enemyFellBack = [False] * len(self.enemy_health)
        self.enemy_used_advance = [False] * len(self.enemy_health)
        self.enemy_advance_roll = [None] * len(self.enemy_health)
        self.enemy_hp_max_total = max(
            1,
            sum(
                unit.get("W", 0) * unit.get("#OfModels", 0)
                for unit in self.enemy_data
                if isinstance(unit, dict)
            ),
        )

        for i in range(len(model)):
            self.unit_weapon.append(model[i].showWeapon())
            self.unit_melee.append(model[i].showMelee())
            self.unit_data.append(model[i].showUnitData())
            self.unit_coords.append([model[i].showCoords()[0], model[i].showCoords()[1]])
            self.unit_health.append(model[i].showUnitData()["W"] * model[i].showUnitData()["#OfModels"])
            self.unitInAttack.append([0, 0])
            self.modelOC.append(model[i].showUnitData()["OC"])
        self.unitFellBack = [False] * len(self.unit_health)
        self.model_used_advance = [False] * len(self.unit_health)
        self.model_advance_roll = [None] * len(self.unit_health)
        self.model_hp_max_total = max(
            1,
            sum(
                unit.get("W", 0) * unit.get("#OfModels", 0)
                for unit in self.unit_data
                if isinstance(unit, dict)
            ),
        )

        self._init_model_state_from_health()

        obsSpace = (len(model) * 3) + (len(enemy) * 3) + len(self.coordsOfOM * 2) + 1
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(obsSpace,), dtype=np.float32)

    def get_info(self):
        return {
            "model health": self.unit_health,
            "player health": self.enemy_health,
            "model alive models": [self._alive_models_from_pool("model", i) for i in range(len(self.unit_health))],
            "player alive models": [self._alive_models_from_pool("enemy", i) for i in range(len(self.enemy_health))],
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
            "game over": self.game_over,
            "end reason": getattr(self, "last_end_reason", ""),
            "winner": getattr(self, "last_winner", None),
        }


    def _coerce_int(self, value, default=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _invalidate_target_cache(self, reason: str = ""):
        self._target_cache_epoch += 1
        self._distance_cache.clear()
        self._shoot_target_cache.clear()
        self._shoot_target_reject_cache.clear()

    def _shoot_range_epsilon(self) -> float:
        raw = os.getenv("SHOOT_RANGE_EPSILON", "0.10")
        try:
            value = float(raw)
        except (TypeError, ValueError):
            value = 0.10
        return max(0.0, value)

    def _cached_distance_model_enemy(self, model_idx: int, enemy_idx: int) -> float:
        key = ("m2e", self._target_cache_epoch, int(model_idx), int(enemy_idx))
        cached = self._distance_cache.get(key)
        if cached is not None:
            return cached
        value = distance(self.unit_coords[model_idx], self.enemy_coords[enemy_idx])
        self._distance_cache[key] = value
        return value

    def _cached_distance_enemy_model(self, enemy_idx: int, model_idx: int) -> float:
        key = ("e2m", self._target_cache_epoch, int(enemy_idx), int(model_idx))
        cached = self._distance_cache.get(key)
        if cached is not None:
            return cached
        value = distance(self.enemy_coords[enemy_idx], self.unit_coords[model_idx])
        self._distance_cache[key] = value
        return value

    def get_shoot_targets_for_unit(self, side: str, unit_idx: int, *, include_rejected: bool = False):
        def _ret(targets_list, rejected_list):
            if include_rejected:
                return list(targets_list), list(rejected_list)
            return list(targets_list)

        cache_key = (self._target_cache_epoch, side, int(unit_idx))
        cached = self._shoot_target_cache.get(cache_key)
        cached_rejected = self._shoot_target_reject_cache.get(cache_key)
        if cached is not None and cached_rejected is not None:
            return _ret(cached, cached_rejected)

        targets = []
        rejected: list[dict] = []
        range_eps = self._shoot_range_epsilon()

        def _add_reject(dst_side: str, dst_idx: int, reason: str, dist: Optional[float] = None, range_limit: Optional[float] = None) -> None:
            dst_label = self._format_unit_label(dst_side, int(dst_idx))
            entry = {
                "target_id": self._unit_id(dst_side, int(dst_idx)),
                "target_label": dst_label,
                "reason": reason,
            }
            if dist is not None:
                entry["distance"] = float(dist)
            if range_limit is not None:
                entry["range"] = float(range_limit)
                overflow = float(dist) - float(range_limit) if dist is not None else None
                if overflow is not None:
                    entry["out_of_range_by"] = float(overflow)
            rejected.append(entry)

        def _log_target_filter(unit_side: str, src_idx: int, dst_side: str, dst_idx: int, reason: str) -> None:
            if not _verbose_logs_enabled():
                return
            src_label = self._format_unit_label(unit_side, int(src_idx))
            dst_label = self._format_unit_label(dst_side, int(dst_idx))
            self._log(
                f"[TARGET][SHOOT] {src_label} -> {dst_label}: {reason}. "
                "Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели."
            )

        if side == "model":
            if not (0 <= unit_idx < len(self.unit_health)):
                return _ret([], [])
            if self.unit_health[unit_idx] <= 0 or self.unitFellBack[unit_idx] or self.unitInAttack[unit_idx][0] == 1:
                return _ret([], [])
            if self.unit_weapon[unit_idx] == "None":
                return _ret([], [])
            range_limit = self.unit_weapon[unit_idx]["Range"]
            for enemy_idx in range(len(self.enemy_health)):
                if self.enemy_health[enemy_idx] <= 0:
                    _add_reject("enemy", enemy_idx, "цель мертва")
                    _log_target_filter("model", unit_idx, "enemy", enemy_idx, "цель мертва")
                    continue
                if self.enemyInAttack[enemy_idx][0] == 1:
                    _add_reject("enemy", enemy_idx, "цель в engagement")
                    _log_target_filter("model", unit_idx, "enemy", enemy_idx, "цель в engagement")
                    continue
                dist = float(self._shooting_distance_between_units("model", unit_idx, "enemy", enemy_idx))
                range_limit_f = float(range_limit)
                if dist > (range_limit_f + range_eps):
                    overflow = dist - range_limit_f
                    reason = f"цель вне дальности: range {dist:.2f} > {range_limit_f:.2f} (out_of_range by +{overflow:.2f})"
                    _add_reject("enemy", enemy_idx, reason, dist=dist, range_limit=range_limit_f)
                    _log_target_filter(
                        "model",
                        unit_idx,
                        "enemy",
                        enemy_idx,
                        f"цель вне дальности (distance={dist:.2f}, range={range_limit_f:.2f}, delta=+{overflow:.2f}, eps={range_eps:.2f})",
                    )
                    continue
                # Критичное правило: если есть LOS хотя бы до одной модели цели, цель валидна для стрельбы.
                if not self._unit_has_los("model", unit_idx, "enemy", int(enemy_idx)):
                    _add_reject("enemy", enemy_idx, "нет LOS ни к одной модели цели")
                    _log_target_filter("model", unit_idx, "enemy", enemy_idx, "нет LOS ни к одной модели цели")
                    continue
                targets.append(int(enemy_idx))
        else:
            if not (0 <= unit_idx < len(self.enemy_health)):
                return _ret([], [])
            if self.enemy_health[unit_idx] <= 0 or self.enemyFellBack[unit_idx] or self.enemyInAttack[unit_idx][0] == 1:
                return _ret([], [])
            if self.enemy_weapon[unit_idx] == "None":
                return _ret([], [])
            range_limit = self.enemy_weapon[unit_idx]["Range"]
            for model_idx in range(len(self.unit_health)):
                if self.unit_health[model_idx] <= 0:
                    _add_reject("model", model_idx, "цель мертва")
                    _log_target_filter("enemy", unit_idx, "model", model_idx, "цель мертва")
                    continue
                if self.unitInAttack[model_idx][0] == 1:
                    _add_reject("model", model_idx, "цель в engagement")
                    _log_target_filter("enemy", unit_idx, "model", model_idx, "цель в engagement")
                    continue
                dist = float(self._shooting_distance_between_units("enemy", unit_idx, "model", model_idx))
                range_limit_f = float(range_limit)
                if dist > (range_limit_f + range_eps):
                    overflow = dist - range_limit_f
                    reason = f"цель вне дальности: range {dist:.2f} > {range_limit_f:.2f} (out_of_range by +{overflow:.2f})"
                    _add_reject("model", model_idx, reason, dist=dist, range_limit=range_limit_f)
                    _log_target_filter(
                        "enemy",
                        unit_idx,
                        "model",
                        model_idx,
                        f"цель вне дальности (distance={dist:.2f}, range={range_limit_f:.2f}, delta=+{overflow:.2f}, eps={range_eps:.2f})",
                    )
                    continue
                # Критичное правило: если есть LOS хотя бы до одной модели цели, цель валидна для стрельбы.
                if not self._unit_has_los("enemy", unit_idx, "model", int(model_idx)):
                    _add_reject("model", model_idx, "нет LOS ни к одной модели цели")
                    _log_target_filter("enemy", unit_idx, "model", model_idx, "нет LOS ни к одной модели цели")
                    continue
                targets.append(int(model_idx))

        self._shoot_target_cache[cache_key] = list(targets)
        self._shoot_target_reject_cache[cache_key] = list(rejected)
        return _ret(targets, rejected)

    def _cell_from_coord(self, coord) -> tuple[int, int]:
        return int(round(float(coord[0]))), int(round(float(coord[1])))

    def get_terrain_obscuring_cells_set(self) -> set[tuple[int, int]]:
        return terrain_cells_from_features(getattr(self, "terrain_features", []))

    def is_terrain_cell(self, x: int, y: int) -> bool:
        return (int(x), int(y)) in self.get_terrain_obscuring_cells_set()

    def _adjust_end_move_from_terrain(self, side: str, unit_idx: int, pos_before: tuple[int, int], phase: str) -> None:
        coords = self.unit_coords if side == "model" else self.enemy_coords
        if not (0 <= unit_idx < len(coords)):
            return
        curr = self._cell_from_coord(coords[unit_idx])
        if not self.is_terrain_cell(curr[0], curr[1]):
            return

        fallback = self._cell_from_coord(pos_before)
        unit_id = unit_idx + (21 if side == "model" else 11)
        if not self.is_terrain_cell(fallback[0], fallback[1]):
            coords[unit_idx] = [fallback[0], fallback[1]]
            self._log_unit(
                "MODEL" if side == "model" else "enemy",
                unit_id,
                unit_idx,
                f"Движение завершено на террейне {curr}, откат на {fallback}. Где: {phase}. Что делать дальше: выбрать другую конечную клетку.",
            )
            return

        for radius in range(1, 4):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if max(abs(dx), abs(dy)) != radius:
                        continue
                    cand = (curr[0] + dx, curr[1] + dy)
                    if not (0 <= cand[0] < self.b_len and 0 <= cand[1] < self.b_hei):
                        continue
                    if self.is_terrain_cell(cand[0], cand[1]):
                        continue
                    coords[unit_idx] = [cand[0], cand[1]]
                    self._log_unit(
                        "MODEL" if side == "model" else "enemy",
                        unit_id,
                        unit_idx,
                        f"Движение завершено на террейне {curr}, сдвиг на {cand}. Где: {phase}. Что делать дальше: выбрать клетку без террейна.",
                    )
                    return


    def _los_debug_enabled(self) -> bool:
        raw = str(os.getenv("LOS_DEBUG", "1")).strip().lower()
        return raw not in {"0", "false", "off", "no"}

    def _log_los_debug(
        self,
        attacker_cell: tuple[int, int],
        target_cell: tuple[int, int],
        report: dict,
        *,
        attacker_id: int | None = None,
        target_id: int | None = None,
    ) -> None:
        if not self._los_debug_enabled():
            return
        crossed = report.get("crossed_cells") or []
        preview = crossed if len(crossed) <= 12 else (crossed[:6] + ["..."] + crossed[-5:])
        obscured_example = None
        obscured_dist = None
        ray_reports = report.get("ray_reports") or []
        for ray in ray_reports:
            cells = ray.get("obscured_cells") or []
            if not cells:
                continue
            obscured_example = cells[0]
            obscured_dist = self._grid_distance_chebyshev(obscured_example, target_cell)
            break
        self._append_agent_log(
            "LOS_DEBUG | "
            f"attacker_id={attacker_id if attacker_id is not None else '-'} "
            f"target_id={target_id if target_id is not None else '-'} "
            f"mode={report.get('visibility_mode')} a_cell={attacker_cell} b_cell={target_cell} "
            f"crossed_cells={preview} los={report.get('los')} "
            f"obscured={report.get('obscured')} fully_visible={report.get('fully_visible')} "
            f"rays={report.get('rays_clear')}/{report.get('rays_total')} rays_obscured={report.get('rays_obscured')} "
            f"target_cover_cells={report.get('target_cover_cells_count')} "
            f"obscured_cell={obscured_example if obscured_example is not None else '-'} "
            f"obscured_cell_dist={obscured_dist if obscured_dist is not None else '-'} "
            f"blocked_by={report.get('blocked_by')}"
        )

    def _target_cover_cells_for_unit(self, target_side: str, target_idx: int, radius: int = 3) -> set[tuple[int, int]]:
        coords = self.unit_coords if target_side == "model" else self.enemy_coords
        if not (0 <= int(target_idx) < len(coords)):
            return set()
        target_cell = self._cell_from_coord(coords[int(target_idx)])
        obstacle_cells = self.get_terrain_obscuring_cells_set()
        if not obstacle_cells:
            return set()
        cover_cells = {
            (int(cell[0]), int(cell[1]))
            for cell in obstacle_cells
            if self._grid_distance_chebyshev((int(cell[0]), int(cell[1])), target_cell) <= int(radius)
        }
        return cover_cells

    def _has_line_of_sight(self, attacker_side: str, attacker_idx: int, target_side: str, target_idx: int) -> bool:
        attacker_coords = self.unit_coords if attacker_side == "model" else self.enemy_coords
        target_coords = self.unit_coords if target_side == "model" else self.enemy_coords
        attacker_cell = self._cell_from_coord(attacker_coords[int(attacker_idx)])
        target_cell = self._cell_from_coord(target_coords[int(target_idx)])

        obscuring_cells = self.get_terrain_obscuring_cells_set()
        self.terrain_obscuring_cells = set(obscuring_cells)
        target_cover_cells = self._target_cover_cells_for_unit(target_side, int(target_idx), radius=3)
        report = visibility_report(
            attacker_cell,
            target_cell,
            opaque_cells_set=self.terrain_opaque_cells,
            obscuring_cells_set=obscuring_cells,
            target_cover_cells_set=target_cover_cells,
            visibility_mode=self.visibility_mode,
        )
        self._log_los_debug(
            attacker_cell,
            target_cell,
            report,
            attacker_id=self._unit_id(attacker_side, int(attacker_idx)) if hasattr(self, "_unit_id") else None,
            target_id=self._unit_id(target_side, int(target_idx)) if hasattr(self, "_unit_id") else None,
        )
        return bool(report.get("los", False))

    def _unit_cells_for_los(self, side: str, idx: int) -> list[tuple[int, int]]:
        cells: list[tuple[int, int]] = []
        seen: set[tuple[int, int]] = set()
        for point in self._unit_model_points(side, int(idx)):
            if not isinstance(point, (list, tuple)) or len(point) < 2:
                continue
            cell = self._cell_from_coord((point[0], point[1]))
            if cell in seen:
                continue
            seen.add(cell)
            cells.append(cell)
        return cells

    def _unit_has_los(self, attacker_side: str, attacker_idx: int, target_side: str, target_idx: int) -> bool:
        attacker_cells = self._unit_cells_for_los(attacker_side, int(attacker_idx))
        target_cells = self._unit_cells_for_los(target_side, int(target_idx))
        if not attacker_cells or not target_cells:
            return False

        obscuring_cells = self.get_terrain_obscuring_cells_set()
        self.terrain_obscuring_cells = set(obscuring_cells)
        target_cover_cells = self._target_cover_cells_for_unit(target_side, int(target_idx), radius=3)
        attacker_id = self._unit_id(attacker_side, int(attacker_idx)) if hasattr(self, "_unit_id") else None
        target_id = self._unit_id(target_side, int(target_idx)) if hasattr(self, "_unit_id") else None

        for attacker_cell in attacker_cells:
            for target_cell in target_cells:
                report = visibility_report(
                    attacker_cell,
                    target_cell,
                    opaque_cells_set=self.terrain_opaque_cells,
                    obscuring_cells_set=obscuring_cells,
                    target_cover_cells_set=target_cover_cells,
                    visibility_mode=self.visibility_mode,
                )
                self._log_los_debug(
                    attacker_cell,
                    target_cell,
                    report,
                    attacker_id=attacker_id,
                    target_id=target_id,
                )
                if bool(report.get("los", False)):
                    return True
        return False

    def _grid_distance_chebyshev(self, a: tuple[int, int], b: tuple[int, int]) -> int:
        return max(abs(int(a[0]) - int(b[0])), abs(int(a[1]) - int(b[1])))

    def _grid_distance_euclid(self, a: tuple[int, int], b: tuple[int, int]) -> float:
        return float(distance_cells_euclid((int(a[0]), int(a[1])), (int(b[0]), int(b[1]))))

    def _barricade_cells(self) -> list[tuple[int, int]]:
        cells: list[tuple[int, int]] = []
        for feature in (self.terrain_features or []):
            if not isinstance(feature, dict):
                continue
            kind = str(feature.get("kind") or "").strip().lower()
            tags_blob = " ".join(str(tag) for tag in (feature.get("tags") or []))
            if kind != "barricade" and "barricade" not in tags_blob.lower():
                continue
            for raw_cell in (feature.get("cells") or []):
                if isinstance(raw_cell, (list, tuple)) and len(raw_cell) >= 2:
                    cells.append((int(raw_cell[0]), int(raw_cell[1])))
        return cells

    def _movement_budget_for_unit(self, side: str, idx: int) -> int:
        data = self.unit_data if side == "model" else self.enemy_data
        base_move = 0
        if 0 <= int(idx) < len(data) and isinstance(data[int(idx)], dict):
            base_move = int(data[int(idx)].get("Movement", 0) or 0)

        used = self.model_used_advance if side == "model" else self.enemy_used_advance
        rolls = self.model_advance_roll if side == "model" else self.enemy_advance_roll
        used_advance = bool(used[int(idx)]) if 0 <= int(idx) < len(used) else False
        roll = rolls[int(idx)] if 0 <= int(idx) < len(rolls) else None
        bonus = int(roll) if used_advance and roll is not None else 0
        return max(0, int(base_move) + bonus)

    def get_unit_reachable_cells(self, side: str, idx: int, budget: Optional[int] = None) -> list[tuple[int, int]]:
        coords = self.unit_coords if side == "model" else self.enemy_coords
        hp = self.unit_health if side == "model" else self.enemy_health
        if not (0 <= int(idx) < len(coords)):
            return []
        if not (0 <= int(idx) < len(hp)) or float(hp[int(idx)] or 0.0) <= 0:
            return []

        row = int(coords[int(idx)][0])
        col = int(coords[int(idx)][1])
        move_budget = self._movement_budget_for_unit(side, int(idx)) if budget is None else max(0, int(budget))

        barricades = set(self._barricade_cells())
        occupied: set[tuple[int, int]] = set()
        for j, pos in enumerate(self.unit_coords):
            if j == int(idx) and side == "model":
                continue
            if j < len(self.unit_health) and float(self.unit_health[j] or 0.0) > 0 and isinstance(pos, (list, tuple)) and len(pos) >= 2:
                occupied.add((int(pos[0]), int(pos[1])))
        for j, pos in enumerate(self.enemy_coords):
            if j == int(idx) and side == "enemy":
                continue
            if j < len(self.enemy_health) and float(self.enemy_health[j] or 0.0) > 0 and isinstance(pos, (list, tuple)) and len(pos) >= 2:
                occupied.add((int(pos[0]), int(pos[1])))

        reachable: list[tuple[int, int]] = []
        for r in range(max(0, row - move_budget), min(self.b_len - 1, row + move_budget) + 1):
            for c in range(max(0, col - move_budget), min(self.b_hei - 1, col + move_budget) + 1):
                dist = self._grid_distance_chebyshev((row, col), (r, c))
                if dist == 0 or dist > int(move_budget):
                    continue
                if (r, c) in occupied:
                    continue
                if (r, c) in barricades:
                    continue
                reachable.append((c, r))  # state coords (x, y)

        if (os.getenv("TERRAIN_DEBUG", "0") == "1" or os.getenv("VIEWER_DEBUG", "0") == "1") and hasattr(self, "_append_agent_log"):
            if reachable:
                xs = [int(x) for x, _y in reachable]
                ys = [int(y) for _x, y in reachable]
                self._append_agent_log(
                    f"[MOVE][REACHABLE] side={side} unit={self._unit_id(side, int(idx)) if hasattr(self, '_unit_id') else int(idx)} "
                    f"budget={int(move_budget)} count={len(reachable)} min_x={min(xs)} max_x={max(xs)} min_y={min(ys)} max_y={max(ys)}"
                )
            else:
                self._append_agent_log(
                    f"[MOVE][REACHABLE] side={side} unit={self._unit_id(side, int(idx)) if hasattr(self, '_unit_id') else int(idx)} "
                    f"budget={int(move_budget)} count=0"
                )

        return reachable

    def get_unit_movement_overlay(self, side: str, idx: int) -> dict[str, list[tuple[int, int]]]:
        move_budget = self._movement_budget_for_unit(side, int(idx))
        move_cells = self.get_unit_reachable_cells(side, idx, budget=move_budget)
        advance_budget = move_budget + 6
        advance_all = self.get_unit_reachable_cells(side, idx, budget=advance_budget)
        move_set = set((int(x), int(y)) for x, y in move_cells)
        advance_cells = [
            (int(x), int(y))
            for x, y in advance_all
            if (int(x), int(y)) not in move_set
        ]
        if (os.getenv("TERRAIN_DEBUG", "0") == "1" or os.getenv("VIEWER_DEBUG", "0") == "1") and hasattr(self, "_append_agent_log"):
            self._append_agent_log(
                f"[MOVE] unit={self._unit_id(side, int(idx)) if hasattr(self, '_unit_id') else int(idx)} "
                f"M={int(move_budget)} budget={int(advance_budget)} reachable_move={len(move_cells)} reachable_adv={len(advance_cells)}"
            )
        return {
            "move_cells": [(int(x), int(y)) for x, y in move_cells],
            "advance_cells": advance_cells,
        }

    def _pick_destination_from_overlay(
        self,
        side: str,
        idx: int,
        *,
        move_dir: int,
        want: int,
        base_m: int,
        unit_label: str,
    ) -> tuple[tuple[int, int] | None, str | None, int]:
        overlay = self.get_unit_movement_overlay(side, idx)
        move_cells = overlay.get("move_cells") or []
        advance_cells = overlay.get("advance_cells") or []
        move_set = set((int(x), int(y)) for x, y in move_cells)
        advance_set = set((int(x), int(y)) for x, y in advance_cells)
        candidates = [(int(x), int(y), "normal") for x, y in move_cells]
        candidates.extend((int(x), int(y), "advance") for x, y in advance_cells)
        if not candidates:
            self._log(f"{unit_label}: нет достижимых клеток для движения (budget={int(base_m) + 6}).")
            return None, None, 0

        coords = self.unit_coords if side == "model" else self.enemy_coords
        row = int(coords[int(idx)][0])
        col = int(coords[int(idx)][1])
        desired = max(0, min(int(want), int(base_m) + 6))

        dir_vec = {
            0: (1.0, 0.0),   # down
            1: (-1.0, 0.0),  # up
            2: (0.0, -1.0),  # left
            3: (0.0, 1.0),   # right
        }.get(int(move_dir))

        filtered = candidates
        if dir_vec is not None:
            dr_sign, dc_sign = dir_vec
            directional = []
            for x, y, mode in candidates:
                dr = float(int(y) - row)
                dc = float(int(x) - col)
                dot = (dr * dr_sign) + (dc * dc_sign)
                if dot > 0.0:
                    directional.append((x, y, mode))
            if directional:
                filtered = directional

        def _score(item):
            x, y, mode = item
            dist = self._grid_distance_chebyshev((row, col), (int(y), int(x)))
            dr = float(int(y) - row)
            dc = float(int(x) - col)
            if dir_vec is None:
                align = 0.0
            else:
                norm = max(1e-6, float(np.hypot(dr, dc)))
                align = -(((dr * dir_vec[0]) + (dc * dir_vec[1])) / norm)
            mode_penalty = 0.0 if mode == "normal" else 0.1
            return (align, abs(int(dist) - int(desired)), mode_penalty, int(dist))

        best = min(filtered, key=_score)
        bx, by, best_mode = int(best[0]), int(best[1]), str(best[2])
        dist = int(self._grid_distance_chebyshev((row, col), (by, bx)))
        if (bx, by) in move_set:
            best_mode = "normal"
        elif (bx, by) in advance_set:
            best_mode = "advance"
        return (bx, by), best_mode, dist

    def _visibility_report_between_units(self, attacker_side: str, attacker_idx: int, target_side: str, target_idx: int) -> dict:
        attacker_coords = self.unit_coords if attacker_side == "model" else self.enemy_coords
        target_coords = self.unit_coords if target_side == "model" else self.enemy_coords
        attacker_cell = self._cell_from_coord(attacker_coords[int(attacker_idx)])
        target_cell = self._cell_from_coord(target_coords[int(target_idx)])
        target_cover_cells = self._target_cover_cells_for_unit(target_side, int(target_idx), radius=3)
        return visibility_report(
            attacker_cell,
            target_cell,
            opaque_cells_set=self.terrain_opaque_cells,
            obscuring_cells_set=self.get_terrain_obscuring_cells_set(),
            target_cover_cells_set=target_cover_cells,
            visibility_mode=self.visibility_mode,
        )

    def _resolve_cover_effect_for_shot(
        self,
        attacker_side: str,
        attacker_idx: int,
        defender_side: str,
        defender_idx: int,
        base_effect=None,
        phase: str = "shooting",
    ):
        """Возвращает итоговый effect для ranged-атаки c учётом LOS/obscured.

        При obscured=True автоматически даём benefit of cover (если он ещё не активен).
        """
        effect_norm = str(base_effect).strip().lower() if base_effect is not None else ""
        if effect_norm == "benefit of cover":
            return "benefit of cover"

        report = self._visibility_report_between_units(attacker_side, int(attacker_idx), defender_side, int(defender_idx))
        has_los = bool(report.get("los", False))
        obscured = bool(report.get("obscured", False))
        if has_los and obscured:
            cover_msg = (
                f"[COVER][{phase.upper()}] {self._format_unit_label(attacker_side, int(attacker_idx))} -> "
                f"{self._format_unit_label(defender_side, int(defender_idx))}: "
                "применён Benefit of Cover (причина: obscured=True по LOS_DEBUG)."
            )
            self._log(cover_msg)
            self._append_agent_log(cover_msg)
            return "benefit of cover"
        return base_effect

    def _unit_can_shoot_now(self, side: str, unit_idx: int) -> bool:
        if side == "enemy":
            if not (0 <= unit_idx < len(self.enemy_health)):
                return False
            return (
                self.enemy_health[unit_idx] > 0
                and not self.enemyFellBack[unit_idx]
                and self.enemyInAttack[unit_idx][0] != 1
                and self.enemy_weapon[unit_idx] != "None"
            )
        if not (0 <= unit_idx < len(self.unit_health)):
            return False
        return (
            self.unit_health[unit_idx] > 0
            and not self.unitFellBack[unit_idx]
            and self.unitInAttack[unit_idx][0] != 1
            and self.unit_weapon[unit_idx] != "None"
        )

    def _count_real_threats_to_model_unit(self, model_idx: int) -> tuple[int, bool, int]:
        if not (0 <= model_idx < len(self.unit_health)) or self.unit_health[model_idx] <= 0:
            return 0, False, 0
        threat_count = 0
        has_fully_visible_threat = False
        obscured_threats = 0
        for enemy_idx in range(len(self.enemy_health)):
            if not self._unit_can_shoot_now("enemy", enemy_idx):
                continue
            report = self._visibility_report_between_units("enemy", enemy_idx, "model", model_idx)
            if not bool(report.get("los", False)):
                continue
            distance_to_unit = self._shooting_distance_between_units("enemy", enemy_idx, "model", model_idx)
            range_limit = float(self.enemy_weapon[enemy_idx].get("Range", 0) or 0)
            if distance_to_unit > range_limit:
                continue
            threat_count += 1
            fully_visible = bool(report.get("fully_visible", True))
            if fully_visible:
                has_fully_visible_threat = True
            else:
                obscured_threats += 1
        return threat_count, has_fully_visible_threat, obscured_threats

    def _model_unit_cover_state(self, unit_idx: int) -> tuple[bool, float, str]:
        if not (0 <= unit_idx < len(self.unit_health)) or self.unit_health[unit_idx] <= 0:
            return False, 0.0, "юнит мёртв"
        if not self._unit_has_keyword(self.unit_data[unit_idx], "infantry"):
            return False, 0.0, "не INFANTRY"
        barricades = self._barricade_cells()
        if not barricades:
            return False, 0.0, "на карте нет barricade"
        unit_cell = self._cell_from_coord(self.unit_coords[unit_idx])
        min_dist = min(self._grid_distance_chebyshev(unit_cell, cell) for cell in barricades)
        cover_radius = float(getattr(reward_cfg, "TERRAIN_COVER_RADIUS", 3.0))
        if min_dist > cover_radius:
            return False, 0.0, f"далеко от barricade (dist={min_dist}, need<={cover_radius:.0f})"
        threat_count, _has_full_visible, obscured_threats = self._count_real_threats_to_model_unit(unit_idx)
        if threat_count <= 0:
            return False, 0.0, "нет реальных угроз для оценки fully_visible"
        # Мягкий вариант: доля угроз, в которых лучи дают fully_visible=False.
        cover_soft = obscured_threats / max(1.0, float(threat_count))
        if cover_soft <= 0:
            return False, 0.0, "все реальные угрозы видят юнит полностью"
        return True, float(cover_soft), f"near_barricade=1, obscured_threats={obscured_threats}/{threat_count}"

    def _terrain_potential_snapshot(self, start_dists: list[float]) -> dict:
        alive_units = [idx for idx, hp in enumerate(self.unit_health) if hp > 0]
        if not alive_units:
            return {
                "phi": 0.0,
                "cover_score": 0.0,
                "threat_score": 0.0,
                "guard_score": 0.0,
                "threat_count_total": 0,
                "cover_units": 0,
                "exposed_units": 0,
            }

        cover_acc = 0.0
        threat_acc = 0.0
        guard_acc = 0.0
        threat_total = 0
        covered_units = 0
        exposed_units = 0
        guard_norm = max(1.0, float(getattr(reward_cfg, "TERRAIN_GUARD_RANGE_NORM", 12.0)))
        threat_norm = max(1.0, float(getattr(reward_cfg, "TERRAIN_THREAT_COUNT_NORM", 3.0)))
        cover_norm = max(1.0, float(getattr(reward_cfg, "TERRAIN_COVER_SCORE_NORM", 2.0)))
        guard_progress_bonus = float(getattr(reward_cfg, "TERRAIN_GUARD_PROGRESS_BONUS", 0.20))

        for idx in alive_units:
            cover_ok, cover_soft, _reason = self._model_unit_cover_state(idx)
            threat_count, has_full_visible_threat, _ = self._count_real_threats_to_model_unit(idx)
            threat_total += threat_count
            threat_acc += min(1.0, threat_count / threat_norm)
            if cover_ok:
                covered_units += 1
                cover_acc += max(0.0, min(1.0, cover_soft))
            if threat_count > 0 and has_full_visible_threat:
                exposed_units += 1

            guard_unit = 0.0
            if cover_ok and len(self.coordsOfOM) > 0:
                unit_pos = self.unit_coords[idx]
                obj_dist = min(distance(unit_pos, objective) for objective in self.coordsOfOM)
                weapon_range = float(self.unit_weapon[idx].get("Range", 0) or 0) if self.unit_weapon[idx] != "None" else 0.0
                in_guard_range = obj_dist <= max(1.0, weapon_range)
                if in_guard_range:
                    range_factor = max(0.0, 1.0 - (obj_dist / guard_norm))
                    guard_unit = 0.6 + (0.4 * range_factor)
                    if idx < len(start_dists):
                        if obj_dist + 1e-6 < float(start_dists[idx]):
                            guard_unit += guard_progress_bonus
                        elif abs(obj_dist - float(start_dists[idx])) <= 1.0:
                            guard_unit += 0.5 * guard_progress_bonus
            guard_acc += min(1.0, guard_unit)

        alive_count = max(1.0, float(len(alive_units)))
        cover_score = min(1.0, (cover_acc / alive_count) * (alive_count / cover_norm))
        threat_score = -min(1.0, (threat_acc / alive_count))
        guard_score = min(1.0, guard_acc / alive_count)

        w_cover = float(getattr(reward_cfg, "TERRAIN_POTENTIAL_W_COVER", 0.08))
        w_threat = float(getattr(reward_cfg, "TERRAIN_POTENTIAL_W_THREAT", 0.10))
        w_guard = float(getattr(reward_cfg, "TERRAIN_POTENTIAL_W_GUARD", 0.04))
        phi = (w_cover * cover_score) + (w_threat * threat_score) + (w_guard * guard_score)
        return {
            "phi": float(phi),
            "cover_score": float(cover_score),
            "threat_score": float(threat_score),
            "guard_score": float(guard_score),
            "threat_count_total": int(threat_total),
            "cover_units": int(covered_units),
            "exposed_units": int(exposed_units),
        }

    def _model_wounds_pool_from_hp(self, unit_data: dict, hp_value: float) -> list[int]:
        if not isinstance(unit_data, dict):
            return []
        wounds_max = max(1, self._coerce_int(unit_data.get("W"), default=1))
        models_cap = max(1, self._coerce_int(unit_data.get("#OfModels"), default=1))
        hp = max(0, self._coerce_int(round(float(hp_value)), default=0))
        if hp <= 0:
            return []
        full = hp // wounds_max
        rem = hp % wounds_max
        pool = [wounds_max] * min(full, models_cap)
        if rem > 0 and len(pool) < models_cap:
            pool.append(rem)
        return pool[:models_cap]

    def _alive_models_from_pool(self, side: str, idx: int) -> int:
        pools = self.unit_model_wounds if side == "model" else self.enemy_model_wounds
        if 0 <= idx < len(pools):
            return sum(1 for w in pools[idx] if w > 0)
        return 0

    def _flush_state_snapshot(self, reason: str = "", force: bool = False) -> bool:
        """Синхронный экспорт state.json для GUI с throttle, безопасный для training."""
        if not hasattr(self, "board"):
            return False

        mode_raw = str(os.getenv("STATE_FLUSH_MODE", "auto")).strip().lower()
        if mode_raw in {"0", "off", "disabled", "none"}:
            return False

        if mode_raw == "auto":
            # В training (playType=False) не пишем state на каждый hit.
            enabled = bool(getattr(self, "playType", False))
        elif mode_raw in {"gui", "on", "enabled", "always"}:
            enabled = True
        elif mode_raw in {"train", "training"}:
            enabled = False
        else:
            enabled = bool(getattr(self, "playType", False))

        if not enabled:
            if not force:
                return False
            allow_force_train = str(os.getenv("STATE_FLUSH_ALLOW_FORCE_IN_TRAIN", "0")).strip().lower()
            if allow_force_train not in {"1", "true", "yes", "on"}:
                return False

        min_interval_ms = 120
        try:
            min_interval_ms = max(0, int(os.getenv("STATE_FLUSH_MIN_INTERVAL_MS", "120")))
        except (TypeError, ValueError):
            min_interval_ms = 120

        # Для GUI по умолчанию делаем чуть более редкий flush, чтобы снизить I/O пики.
        if bool(getattr(self, "playType", False)) and "STATE_FLUSH_MIN_INTERVAL_MS" not in os.environ:
            min_interval_ms = max(min_interval_ms, 180)

        now = time.monotonic()
        min_interval_s = min_interval_ms / 1000.0
        if not force and min_interval_s > 0:
            last_ts = float(getattr(self, "_state_flush_last_ts", 0.0) or 0.0)
            if now - last_ts < min_interval_s:
                self._state_flush_pending = True
                return False

        try:
            write_state_json(self)
            self._state_flush_last_ts = now
            self._state_flush_pending = False
            return True
        except Exception as exc:
            details = f" ({reason})" if reason else ""
            self._log(
                f"[STATE] Не удалось обновить state.json{details}. Где: warhamEnv._flush_state_snapshot. "
                f"Что делать дальше: проверить доступ к файлу state.json. Ошибка: {exc}"
            )
            return False


    def _apply_health_update(self, side: str, idx: int, new_hp: float, reason: str = "") -> None:
        health = self.unit_health if side == "model" else self.enemy_health
        data = self.unit_data if side == "model" else self.enemy_data
        pools = self.unit_model_wounds if side == "model" else self.enemy_model_wounds
        prefix = "MODEL" if side == "model" else self._display_side("enemy")

        if not (0 <= idx < len(health)):
            return

        old_hp = float(health[idx])
        bounded_hp = max(0.0, float(new_hp))
        health[idx] = bounded_hp

        if 0 <= idx < len(data):
            old_pool = pools[idx] if idx < len(pools) else []
            old_alive = sum(1 for w in old_pool if w > 0)
            new_pool = self._model_wounds_pool_from_hp(data[idx], bounded_hp)
            new_alive = sum(1 for w in new_pool if w > 0)
            if idx < len(pools):
                pools[idx] = new_pool
            killed = max(0, old_alive - new_alive)
            if killed > 0:
                unit_id = idx + (21 if side == "model" else 11)
                unit_label = self._format_unit_label(side, idx, unit_id=unit_id)
                suffix = f" ({reason})" if reason else ""
                self._log_unit(
                    prefix,
                    unit_id,
                    idx,
                    f"Потери: убито моделей {killed}. Осталось: {new_alive}. HP: {old_hp:.1f} -> {bounded_hp:.1f}{suffix}",
                )
            self._sync_model_positions_to_anchors()
            if killed > 0:
                self._auto_fix_unit_coherency(side, idx, reason="потери моделей")
            self._flush_state_snapshot(reason=f"health_update:{side}:{idx}")

    def _sync_model_positions_to_anchors(self) -> None:
        self.unit_anchor_coords = [list(coords) for coords in self.unit_coords]
        self.enemy_anchor_coords = [list(coords) for coords in self.enemy_coords]

        occupied: set[tuple[int, int]] = set()
        self.unit_model_positions = self._resolve_side_model_positions(
            side="model",
            occupied=occupied,
        )
        self.enemy_model_positions = self._resolve_side_model_positions(
            side="enemy",
            occupied=occupied,
        )

    def _resolve_side_model_positions(self, side: str, occupied: set[tuple[int, int]]):
        coords = self.unit_coords if side == "model" else self.enemy_coords
        anchors = self.unit_anchor_coords if side == "model" else self.enemy_anchor_coords
        resolved_positions = []
        max_radius = max(1, self.b_len + self.b_hei)

        for idx in range(len(coords)):
            alive = self._alive_models_from_pool(side, idx)
            if alive <= 0:
                resolved_positions.append([])
                continue

            preferred = self._clamp_anchor(coords[idx])
            best_anchor = self._find_nearest_valid_anchor(
                preferred_anchor=preferred,
                count=alive,
                occupied=occupied,
                max_radius=max_radius,
            )
            if best_anchor is None:
                best_anchor = preferred
                unit_label = self._format_unit_label(side, idx)
                self._log(
                    f"[MODEL_POS] {unit_label}: не найдено полностью валидное размещение формации. "
                    "Где: warhamEnv._resolve_side_model_positions. "
                    "Что делать дальше: увеличить карту или уменьшить плотность юнитов."
                )

            anchors[idx] = [int(best_anchor[0]), int(best_anchor[1])]
            coords[idx] = [int(best_anchor[0]), int(best_anchor[1])]
            formation = self._build_anchor_formation(best_anchor, alive)
            resolved_positions.append(formation)
            for pos in formation:
                occupied.add((int(pos[0]), int(pos[1])))

        return resolved_positions

    def _init_model_state_from_health(self) -> None:
        self.unit_model_wounds = [
            self._model_wounds_pool_from_hp(self.unit_data[i], self.unit_health[i])
            for i in range(len(self.unit_health))
        ]
        self.enemy_model_wounds = [
            self._model_wounds_pool_from_hp(self.enemy_data[i], self.enemy_health[i])
            for i in range(len(self.enemy_health))
        ]
        self._sync_model_positions_to_anchors()

    def _sync_after_command_phase_reanimation(self, side: str) -> None:
        # Reanimation меняет суммарный HP; синхронизируем пулы/позиции и сразу обновляем state.json.
        self._init_model_state_from_health()
        self._sync_model_positions_to_anchors()
        self._flush_state_snapshot(reason=f"command_phase_reanimation:{side}", force=True)

    def _coherency_required_neighbors(self, alive_models: int) -> int:
        if alive_models >= 7:
            return 2
        if alive_models >= 2:
            return 1
        return 0

    def _models_in_coherency(self, model_a, model_b) -> bool:
        if model_a is None or model_b is None:
            return False
        ax, ay, az = float(model_a[0]), float(model_a[1]), float(model_a[2] if len(model_a) > 2 else 0)
        bx, by, bz = float(model_b[0]), float(model_b[1]), float(model_b[2] if len(model_b) > 2 else 0)
        horizontal = float(np.sqrt((bx - ax) ** 2 + (by - ay) ** 2))
        vertical = abs(bz - az)
        return horizontal <= 2.0 and vertical <= 5.0

    def _build_anchor_formation(self, anchor_xy, count: int):
        x, y = int(anchor_xy[0]), int(anchor_xy[1])
        offsets = self._formation_offsets()
        positions = []
        for dx, dy in offsets:
            positions.append([x + dx, y + dy, 0])
            if len(positions) >= count:
                break
        while len(positions) < count:
            positions.append([x, y, 0])
        return positions

    def _formation_offsets(self):
        return [
            (0, 0),
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1),
            (0, 2), (0, -2), (2, 0), (-2, 0),
            (1, 2), (1, -2), (-1, 2), (-1, -2),
            (2, 1), (2, -1), (-2, 1), (-2, -1),
        ]

    def _clamp_anchor(self, anchor_xy):
        x = int(anchor_xy[0]) if anchor_xy is not None else 0
        y = int(anchor_xy[1]) if anchor_xy is not None else 0
        x = max(0, min(self.b_len - 1, x))
        y = max(0, min(self.b_hei - 1, y))
        return [x, y]

    def _is_model_cell_in_bounds(self, pos_xy) -> bool:
        x = int(pos_xy[0])
        y = int(pos_xy[1])
        return 0 <= x < self.b_len and 0 <= y < self.b_hei

    def _is_formation_valid(self, anchor_xy, count: int, occupied: set[tuple[int, int]]) -> bool:
        if count <= 0:
            return True
        formation = self._build_anchor_formation(anchor_xy, count)
        used = set()
        for pos in formation:
            cell = (int(pos[0]), int(pos[1]))
            if not self._is_model_cell_in_bounds(cell):
                return False
            if cell in occupied or cell in used:
                return False
            if self.is_terrain_cell(cell[0], cell[1]):
                return False
            used.add(cell)
        return True

    def _ring_positions(self, center, radius: int):
        cx, cy = int(center[0]), int(center[1])
        if radius == 0:
            yield [cx, cy]
            return
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if max(abs(dx), abs(dy)) != radius:
                    continue
                yield [cx + dx, cy + dy]

    def _find_nearest_valid_anchor(
        self,
        preferred_anchor,
        count: int,
        occupied: set[tuple[int, int]],
        max_radius: int,
    ):
        preferred = self._clamp_anchor(preferred_anchor)
        for radius in range(0, max_radius + 1):
            for candidate in self._ring_positions(preferred, radius):
                if not self._is_formation_valid(candidate, count, occupied):
                    continue
                return self._clamp_anchor(candidate)
        return None

    def _validate_unit_coherency(self, side: str, idx: int) -> bool:
        positions_all = self.unit_model_positions if side == "model" else self.enemy_model_positions
        if not (0 <= idx < len(positions_all)):
            return True
        positions = positions_all[idx]
        alive = len(positions)
        required = self._coherency_required_neighbors(alive)
        if required == 0:
            return True
        for i, pos_i in enumerate(positions):
            neighbors = 0
            for j, pos_j in enumerate(positions):
                if i == j:
                    continue
                if self._models_in_coherency(pos_i, pos_j):
                    neighbors += 1
            if neighbors < required:
                return False
        return True

    def _auto_fix_unit_coherency(self, side: str, idx: int, reason: str = "") -> None:
        anchors = self.unit_anchor_coords if side == "model" else self.enemy_anchor_coords
        positions_all = self.unit_model_positions if side == "model" else self.enemy_model_positions
        if not (0 <= idx < len(anchors)):
            return
        alive = self._alive_models_from_pool(side, idx)
        positions_all[idx] = self._build_anchor_formation(anchors[idx], alive)
        self._sync_model_positions_to_anchors()
        unit_id = idx + (21 if side == "model" else 11)
        side_label = "MODEL" if side == "model" else self._display_side("enemy")
        why = f" Причина: {reason}." if reason else ""
        self._log_unit(
            side_label,
            unit_id,
            idx,
            f"Когеренция автоматически обновлена. Живых моделей: {alive}.{why}",
        )

    def _auto_fix_all_coherency(self, reason: str = "") -> None:
        for side, total in (("model", len(self.unit_health)), ("enemy", len(self.enemy_health))):
            for idx in range(total):
                if self._alive_models_from_pool(side, idx) <= 1:
                    continue
                if not self._validate_unit_coherency(side, idx):
                    self._auto_fix_unit_coherency(side, idx, reason=reason)

    def _unit_model_points(self, side: str, idx: int):
        positions_all = self.unit_model_positions if side == "model" else self.enemy_model_positions
        coords_all = self.unit_coords if side == "model" else self.enemy_coords
        if 0 <= idx < len(positions_all) and positions_all[idx]:
            return positions_all[idx]
        if 0 <= idx < len(coords_all):
            c = coords_all[idx]
            return [[float(c[0]), float(c[1]), 0.0]]
        return []

    def _distance_between_units(self, side_a: str, idx_a: int, side_b: str, idx_b: int) -> float:
        pts_a = self._unit_model_points(side_a, idx_a)
        pts_b = self._unit_model_points(side_b, idx_b)
        if not pts_a or not pts_b:
            return float("inf")
        best = float("inf")
        for pa in pts_a:
            for pb in pts_b:
                d = distance(pa[:2], pb[:2])
                if d < best:
                    best = d
        return best

    def _shooting_distance_between_units(self, side_a: str, idx_a: int, side_b: str, idx_b: int) -> float:
        """Дистанция для стрельбы: минимум по парам моделей в метрике Чебышёва."""
        pts_a = self._unit_model_points(side_a, idx_a)
        pts_b = self._unit_model_points(side_b, idx_b)
        if not pts_a or not pts_b:
            return float("inf")
        best = float("inf")
        for pa in pts_a:
            a_cell = self._cell_from_coord((pa[0], pa[1]))
            for pb in pts_b:
                b_cell = self._cell_from_coord((pb[0], pb[1]))
                d = float(self._grid_distance_chebyshev(a_cell, b_cell))
                if d < best:
                    best = d
        return best

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
        if self.active_side == "model" and self._looks_like_dice_log(msg):
            self._emit_event(
                {
                    "side": "enemy",
                    "phase": self.phase,
                    "type": "dice",
                    "msg": msg,
                    "data": {"raw": msg},
                    "unit_id": None,
                    "unit_name": None,
                    "verbosity": "verbose" if verbose_only else "normal",
                }
            )

    def _looks_like_dice_log(self, msg: str) -> bool:
        lowered = msg.lower()
        return any(token in lowered for token in ("🎲", "бросок", "d6", "2d6", "d3"))

    def _normalize_event_side(self, side: str) -> str:
        side_upper = str(side).upper()
        if side_upper in ("MODEL", "ENEMY"):
            return "enemy"
        if side_upper in ("PLAYER", "HUMAN"):
            return "player"
        if side == "model":
            return "enemy"
        if side == "enemy":
            return "player"
        return str(side)

    def _unit_name(self, side: str, unit_idx: int) -> str | None:
        data = self._get_unit_data(side, unit_idx)
        if isinstance(data, dict):
            return data.get("Name")
        return None

    def _emit_event(self, event: dict) -> None:
        if not isinstance(event, dict):
            return
        event.setdefault("battle_round", self.battle_round)
        event.setdefault("turn", self.numTurns)
        event.setdefault("phase", self.phase)
        event.setdefault("data", {})
        event.setdefault("msg", "")
        event.setdefault("verbosity", "normal")
        get_event_bus().emit(event)

    def _append_agent_log(self, msg: str) -> None:
        if msg is None:
            return
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_line = f"{timestamp} | {msg}"
        try:
            with open(self._agent_log_path, "a", encoding="utf-8") as log_file:
                log_file.write(full_line + "\n")
        except Exception:
            return

    def _log_reward(self, msg: str, unit_id: int | None = None, unit_name: str | None = None) -> None:
        self._log(msg)
        self._append_agent_log(msg)
        if self.active_side == "model":
            self._emit_event(
                {
                    "side": "enemy",
                    "phase": self.phase,
                    "type": "reward",
                    "msg": msg,
                    "data": {"raw": msg},
                    "unit_id": unit_id,
                    "unit_name": unit_name,
                }
            )

    def _log_reward_unit(self, side: str, unit_id: int, unit_idx: int, msg: str) -> None:
        side_label = self._side_label(side)
        unit_label = self._format_unit_label(side, unit_idx, unit_id=unit_id)
        unit_side = "model" if self._normalize_event_side(side) == "enemy" else "enemy"
        unit_name = self._unit_name(unit_side, unit_idx)
        self._log_reward(f"[{side_label}] {unit_label}: {msg}", unit_id=unit_id, unit_name=unit_name)

    def _log_reward_warning(self, msg: str) -> None:
        if os.getenv("REWARD_DEBUG", "0") != "1":
            return
        self._log_reward(msg)

    def _objective_positions_available(self) -> bool:
        return isinstance(getattr(self, "coordsOfOM", None), (list, np.ndarray)) and len(self.coordsOfOM) > 0

    def _is_position_near_objective(self, pos, radius: float = 5.0) -> bool:
        if not self._objective_positions_available():
            self._log_reward_warning(
                "Reward (объекты): нет координат целей, бонусы за урон/килл у цели отключены. "
                "Где: Warhammer40kEnv._is_position_near_objective. "
                "Что сделать: проверьте заполнение coordsOfOM."
            )
            return False
        return any(distance(pos, om) <= radius for om in self.coordsOfOM)

    def _min_model_obj_distance(self) -> Optional[float]:
        if not self._objective_positions_available():
            return None
        distances = []
        for i in range(len(self.unit_health)):
            if self.unit_health[i] <= 0:
                continue
            for om in self.coordsOfOM:
                distances.append(distance(self.unit_coords[i], om))
        if not distances:
            return None
        return float(min(distances))

    def _any_model_near_objective(self, radius: float = 5.0) -> bool:
        if not self._objective_positions_available():
            return False
        for i in range(len(self.unit_health)):
            if self.unit_health[i] <= 0:
                continue
            if self._is_position_near_objective(self.unit_coords[i], radius=radius):
                return True
        return False

    def _unit_max_hp(self, side: str, idx: int) -> float:
        data_list = self.unit_data if side == "model" else self.enemy_data
        if not (0 <= idx < len(data_list)):
            return 1.0
        unit_data = data_list[idx]
        if not isinstance(unit_data, dict):
            return 1.0
        wounds = float(unit_data.get("W", 1))
        models = float(unit_data.get("#OfModels", 1))
        return max(1.0, wounds * models)

    def _melee_strength_score(self, side: str, idx: int) -> float:
        weapons = self.unit_melee if side == "model" else self.enemy_melee
        data_list = self.unit_data if side == "model" else self.enemy_data
        if not (0 <= idx < len(weapons)) or not (0 <= idx < len(data_list)):
            return 0.0
        weapon = weapons[idx]
        if not isinstance(weapon, dict):
            return 0.0
        attacks = float(weapon.get("A", 1))
        strength = float(weapon.get("S", 1))
        damage = float(weapon.get("Damage", 1))
        ws = float(weapon.get("WS", 4))
        ap = float(weapon.get("AP", 0))
        hit_chance = max(0.0, min(1.0, (7.0 - ws) / 6.0))
        ap_bonus = 1.0 + max(0.0, -ap) * 0.05
        models = float(data_list[idx].get("#OfModels", 1)) if isinstance(data_list[idx], dict) else 1.0
        return attacks * strength * damage * hit_chance * ap_bonus * models

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
        if not self._phase_event_emitted:
            event_side = self._normalize_event_side(side)
            if event_side == "enemy":
                self._emit_event(
                    {
                        "side": event_side,
                        "phase": phase,
                        "type": "phase_start",
                        "msg": phase_title,
                        "data": {"title": phase_title},
                        "unit_id": None,
                        "unit_name": None,
                    }
                )
                self._phase_event_emitted = True

    def _log_unit(self, side: str, unit_id: int, unit_idx: int, msg: str):
        if not self._should_log():
            return
        side_label = self._side_label(side)
        unit_label = self._format_unit_label(side, unit_idx, unit_id=unit_id)
        self._log(f"[{side_label}] {unit_label}: {msg}")
        self._emit_unit_event(side_label, side, unit_id, unit_idx, msg, None, verbose_only=False)

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
        self._emit_unit_event(side_label, None, None, None, msg, phase, verbose_only=False)

    def _log_unit_phase(self, side_label: str, phase: str, unit_id: int, unit_idx: int, msg: str):
        if not self._should_log():
            return
        unit_label = self._format_unit_label(
            "model" if side_label == "MODEL" else "enemy",
            unit_idx,
            unit_id=unit_id,
        )
        self._log(f"[{side_label}][{phase.upper()}] {unit_label}: {msg}")
        self._emit_unit_event(side_label, None, unit_id, unit_idx, msg, phase, verbose_only=False)

    def _log_action(self, side: str, unit_idx: int, msg: str, phase: str = None, verbose_only: bool = False):
        side_label = self._side_label(side)
        unit_label = self._format_unit_label(side, unit_idx)
        phase_prefix = f"[{phase.upper()}] " if phase else ""
        self._log(f"[{side_label}] {phase_prefix}{unit_label}: {msg}", verbose_only=verbose_only)
        self._emit_unit_event(side_label, side, None, unit_idx, msg, phase, verbose_only=verbose_only)

    def _emit_unit_event(
        self,
        side_label: str,
        side: str | None,
        unit_id: int | None,
        unit_idx: int | None,
        msg: str,
        phase: str | None,
        verbose_only: bool,
    ) -> None:
        event_side = self._normalize_event_side(side_label if side is None else side)
        if event_side != "enemy":
            return
        phase_value = phase or self.phase
        resolved_unit_id = unit_id
        resolved_unit_name = None
        if unit_idx is not None:
            resolved_unit_name = self._unit_name("model", unit_idx)
            if resolved_unit_id is None:
                resolved_unit_id = self._unit_id("model", unit_idx)
        if resolved_unit_id is not None and resolved_unit_id not in self._phase_unit_logged:
            self._phase_unit_logged.add(resolved_unit_id)
            self._emit_event(
                {
                    "side": event_side,
                    "phase": phase_value,
                    "type": "unit_start",
                    "msg": f"Юнит {resolved_unit_id} — {resolved_unit_name or '—'}",
                    "unit_id": resolved_unit_id,
                    "unit_name": resolved_unit_name,
                    "data": {},
                }
            )
        event_type = self._classify_event_type(msg, phase_value)
        self._emit_event(
            {
                "side": event_side,
                "phase": phase_value,
                "type": event_type,
                "msg": msg,
                "data": {"raw": msg},
                "unit_id": resolved_unit_id,
                "unit_name": resolved_unit_name,
                "verbosity": "verbose" if verbose_only else "normal",
            }
        )

    def _classify_event_type(self, msg: str, phase: str | None) -> str:
        lowered = msg.lower()
        if "reward" in lowered or "награда" in lowered:
            return "reward"
        if "vp" in lowered or "объект" in lowered or "cp" in lowered:
            return "vp"
        if "бросок" in lowered or "🎲" in lowered or "d6" in lowered or "2d6" in lowered or "d3" in lowered:
            return "dice"
        if "цели" in lowered or "доступн" in lowered or "скан" in lowered or "выбор" in lowered:
            return "scan"
        if "пропущ" in lowered or "нет доступных целей" in lowered or "нет целей" in lowered:
            return "skip"
        if phase == "movement":
            return "move"
        if phase == "shooting":
            return "shoot"
        if phase == "charge":
            return "charge"
        if phase == "fight":
            return "fight"
        return "summary"

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

    def _request_choice(self, prompt: str, options: list[str], meta: Optional[dict] = None):
        return self._ensure_io().request_choice(prompt, options, meta=meta)

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
        target_side = "enemy" if moving_unit_side == "enemy" else "model"
        candidates = []
        for i in range(len(defender_health)):
            if defender_health[i] <= 0:
                continue
            if defender_in_attack[i][0] == 1:
                continue
            if defender_weapon[i] == "None":
                continue
            if self._distance_between_units(defender_side, i, target_side, moving_idx) <= defender_weapon[i]["Range"]:
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
        else:
            self.enemyCP -= 1
            attacker_health = self.enemy_health
            attacker_weapon = self.enemy_weapon
            attacker_data = self.enemy_data
            target_health = self.unit_health if moving_unit_side == "model" else self.enemy_health
            target_data = self.unit_data if moving_unit_side == "model" else self.enemy_data

        distance_to_target = self._shooting_distance_between_units(
            "model" if defender_side == "model" else "enemy",
            chosen,
            moving_unit_side,
            moving_idx,
        )
        shooter_side = "model" if defender_side == "model" else "enemy"
        effect = self._resolve_cover_effect_for_shot(
            shooter_side,
            chosen,
            moving_unit_side,
            moving_idx,
            base_effect=None,
            phase=phase,
        )
        _logger = None
        if _verbose_logs_enabled():
            _logger = RollLogger(auto_dice, agent_log_fn=self._append_agent_log)
            _logger.configure_for_weapon(attacker_weapon[chosen])
            dmg, modHealth = attack(
                attacker_health[chosen],
                attacker_weapon[chosen],
                attacker_data[chosen],
                target_health[moving_idx],
                target_data[moving_idx],
                effects=effect,
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
                effects=effect,
                distance_to_target=distance_to_target,
                hit_on_6=True,
            )

        self._apply_health_update("enemy" if moving_unit_side == "enemy" else "model", moving_idx, modHealth, reason="Overwatch")
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
                effect=effect,
                report_title="ОТЧЁТ ПО OVERWATCH",
                attacker_label=self._format_unit_label(defender_side, chosen),
                defender_label=target_label,
                extra_rules=["Overwatch: попадания только на 6+"],
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
        self._phase_event_emitted = False
        self._phase_unit_logged = set()
        if not self._round_banner_shown:
            self._log(f"=== БОЕВОЙ РАУНД {self.battle_round} ===")
            self._round_banner_shown = True
            if not self._fight_env_logged:
                self._log(
                    "[FIGHT][ENV] "
                    f"file={__file__} exe={sys.executable} cwd={os.getcwd()} "
                    f"FIGHT_REPORT={int(_fight_report_enabled())} "
                    f"VERBOSE_LOGS={os.getenv('VERBOSE_LOGS', '0')} "
                    f"MANUAL_DICE={os.getenv('MANUAL_DICE', '0')} "
                    f"PLAY_NO_EXPLORATION={os.getenv('PLAY_NO_EXPLORATION', '0')} "
                    f"TRAIN_DEBUG={os.getenv('TRAIN_DEBUG', '0')}"
                )
                self._fight_env_logged = True
        if phase == "command":
            self._log(f"--- ХОД {self._side_label(side)} ---")
            if side == "model":
                self.unitFellBack = [False] * len(self.unit_health)
            elif side == "enemy":
                self.enemyFellBack = [False] * len(self.enemy_health)
        self._log_phase(self._side_label(side), phase)
        if side == "model":
            self._emit_event(
                {
                    "side": "enemy",
                    "phase": phase,
                    "type": "summary",
                    "msg": f"Ход модели: {phase}",
                    "unit_id": None,
                    "unit_name": None,
                    "data": {"phase": phase},
                }
            )

    def _end_battle_round(self):
        self._log(f"=== КОНЕЦ БОЕВОГО РАУНДА {self.battle_round} ===")
        self._emit_event(
            {
                "side": "enemy",
                "phase": self.phase,
                "type": "summary",
                "msg": f"Конец боевого раунда {self.battle_round}",
                "unit_id": None,
                "unit_name": None,
                "data": {},
            }
        )
        self.battle_round += 1
        self.numTurns = self.battle_round
        self._round_banner_shown = False
        self._auto_fix_all_coherency(reason="конец боевого раунда")
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
            self._terrain_shaping_shot_bonus_units = set()
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
                                reward_delta += reward_cfg.COMMAND_INSANE_BRAVERY_REWARD
                                self._log_reward_unit(
                                    "model",
                                    i + 21,
                                    i,
                                    "Reward (командование): "
                                    f"Insane Bravery bonus=+{reward_cfg.COMMAND_INSANE_BRAVERY_REWARD:.3f}",
                                )
                                self.modelCP -= 1
                                if self.trunc is False:
                                    self._log(f"{unit_label}: применена Insane Bravery (-1 CP), тест пройден.")
                            else:
                                reward_delta -= reward_cfg.COMMAND_INSANE_BRAVERY_PENALTY
                                self._log_reward_unit(
                                    "model",
                                    i + 21,
                                    i,
                                    "Reward (командование): "
                                    f"Insane Bravery penalty=-{reward_cfg.COMMAND_INSANE_BRAVERY_PENALTY:.3f} "
                                    "(нет CP)",
                                )
            dice_fn = player_dice if os.getenv("MANUAL_DICE", "0") == "1" and side == "enemy" else auto_dice
            apply_end_of_command_phase(self, side="model", dice_fn=dice_fn, log_fn=self._log)
            score_end_of_command_phase(self, "model", log_fn=self._log)
            self._emit_event(
                {
                    "side": "enemy",
                    "phase": "command",
                    "type": "phase_end",
                    "msg": f"Командование завершено: VP={self.modelVP}, CP={self.modelCP}",
                    "unit_id": None,
                    "unit_name": None,
                    "data": {"vp": self.modelVP, "cp": self.modelCP},
                }
            )
            return battle_shock, reward_delta

        if side == "enemy" and action is not None and not manual:
            self.enemyCP += 1
            self.modelCP += 1
            battle_shock = [False] * len(self.enemy_health)
            cp_on = action.get("cp_on", 0) if isinstance(action, dict) else 0
            use_cp = action.get("use_cp", 0) if isinstance(action, dict) else 0
            for i in range(len(self.enemy_health)):
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
                        battle_shock[i] = True
                        self.enemyOC[i] = 0
                        if self.trunc is False:
                            self._log(f"{unit_label}: тест Battle-shock провален.")
                        if use_cp == 1 and cp_on == i and self.enemyCP - 1 >= 0:
                            battle_shock[i] = False
                            self.enemyCP -= 1
                            self.enemyOC[i] = self.enemy_data[i]["OC"]
                            if self.trunc is False:
                                self._log(f"{unit_label}: применена Insane Bravery (-1 CP), тест пройден.")
            dice_fn = player_dice if os.getenv("MANUAL_DICE", "0") == "1" and side == "enemy" else auto_dice
            apply_end_of_command_phase(self, side="enemy", dice_fn=dice_fn, log_fn=self._log)
            score_end_of_command_phase(self, "enemy", log_fn=self._log)
            return battle_shock

        if side == "enemy" and manual:
            self.enemyCP += 1
            self.modelCP += 1
            battle_shock = [False] * len(self.enemy_health)
            for i in range(len(self.enemy_health)):
                self.current_action_index = i
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
            advanced_flags = [False] * len(self.unit_health)
            self.model_used_advance = [False] * len(self.unit_health)
            self.model_advance_roll = [None] * len(self.unit_health)
            reward_delta = 0
            objective_hold_delta = 0.0
            objective_proximity_delta = 0.0
            movement_meta = {
                "applied_hold_penalty": False,
                "hold_penalty_events": 0,
            }
            for i in range(len(self.unit_health)):
                modelName = i + 21
                battleSh = battle_shock[i] if battle_shock else False
                pos_before = tuple(self.unit_coords[i])
                if self.unit_health[i] <= 0:
                    self._log_unit("MODEL", modelName, i, f"Юнит мертв, движение пропущено. Позиция: {pos_before}")
                    continue
                if self.unitInAttack[i][0] == 0 and self.unit_health[i] > 0:
                    base_m = int(self.unit_data[i]["Movement"])
                    label = "move_num_" + str(i)
                    want = int(action[label])
                    move_dir = int(action["move"])
                    advance_roll = None
                    movement = 0.0

                    if move_dir != 4:
                        dest, move_mode, movement = self._pick_destination_from_overlay(
                            "model",
                            i,
                            move_dir=move_dir,
                            want=want,
                            base_m=base_m,
                            unit_label=self._format_unit_label("model", i, unit_id=modelName),
                        )
                        if dest is None:
                            advanced_flags[i] = False
                            self.model_used_advance[i] = False
                            self.model_advance_roll[i] = None
                            continue
                        advanced = str(move_mode) == "advance" or int(movement) > int(base_m)
                        if advanced:
                            adv_used = max(0, int(movement) - int(base_m))
                            advance_roll = max(1, min(6, int(adv_used)))
                        self.unit_coords[i] = [int(dest[1]), int(dest[0])]
                    else:
                        move_mode = "stay"
                        advanced = False

                    if move_dir == 4:
                        nearest_obj_idx = None
                        nearest_obj_dist = None
                        for j, obj in enumerate(self.coordsOfOM):
                            curr_dist = distance(self.unit_coords[i], obj)
                            if nearest_obj_dist is None or curr_dist < nearest_obj_dist:
                                nearest_obj_dist = curr_dist
                                nearest_obj_idx = j

                        if nearest_obj_idx is not None and nearest_obj_dist is not None:
                            if nearest_obj_dist <= 5:
                                reward_delta += reward_cfg.VP_OBJECTIVE_HOLD_REWARD
                                objective_hold_delta += reward_cfg.VP_OBJECTIVE_HOLD_REWARD
                                self._log_reward_unit(
                                    "model",
                                    modelName,
                                    i,
                                    "Reward (VP/объекты): "
                                    f"hold=+{reward_cfg.VP_OBJECTIVE_HOLD_REWARD:.3f} "
                                    f"(obj={nearest_obj_idx}, dist={nearest_obj_dist:.3f})",
                                )
                            else:
                                base_m = max(0.0, float(self.unit_data[i].get("Movement", 0)))
                                max_reach = base_m + 6.0
                                d_before = float(nearest_obj_dist)
                                d_best_possible = max(d_before - max_reach, 0.0)
                                d_after = d_before
                                could_improve = d_best_possible < d_before
                                could_reach_control = d_best_possible <= 5.0
                                if could_improve:
                                    missed_progress = max(0.0, d_after - d_best_possible)
                                    norm_base = max(1.0, float(getattr(reward_cfg, "VP_OBJECTIVE_MISSED_PROGRESS_NORM", 6.0)))
                                    severity = min(1.0, missed_progress / norm_base)
                                    hold_penalty = reward_cfg.VP_OBJECTIVE_HOLD_PENALTY * severity
                                    round_scale = 1.0
                                    if self.battle_round <= 2:
                                        round_scale = 0.5
                                    elif self.battle_round <= 4:
                                        round_scale = 0.75
                                    hold_penalty *= round_scale
                                    reward_delta -= hold_penalty
                                    objective_hold_delta -= hold_penalty
                                    movement_meta["applied_hold_penalty"] = True
                                    movement_meta["hold_penalty_events"] += 1
                                    hold_penalty_reason = "no_move_missed_progress"
                                    self._log_reward_unit(
                                        "model",
                                        modelName,
                                        i,
                                        "Reward (VP/объекты): "
                                        f"hold_penalty=-{hold_penalty:.3f} "
                                        f"(obj={nearest_obj_idx}, d_before={d_before:.3f}, "
                                        f"d_after={d_after:.3f}, d_best={d_best_possible:.3f}, max_reach={max_reach:.3f}, "
                                        f"could_reach_objective={int(could_reach_control)}, severity={severity:.3f}, "
                                        f"round_scale={round_scale:.2f}, reason={hold_penalty_reason})",
                                    )
                                else:
                                    hold_penalty_reason = "no_move_cannot_improve"
                                    self._log_reward_unit(
                                        "model",
                                        modelName,
                                        i,
                                        "Reward (VP/объекты): hold_penalty=0.000 "
                                        f"(obj={nearest_obj_idx}, d_before={d_before:.3f}, d_after={d_after:.3f}, "
                                        f"d_best={d_best_possible:.3f}, max_reach={max_reach:.3f}, "
                                        f"could_reach_objective={int(could_reach_control)}, reason={hold_penalty_reason})",
                                    )

                    advanced_flags[i] = advanced
                    self.model_used_advance[i] = bool(advanced)
                    self.model_advance_roll[i] = int(advance_roll) if advance_roll is not None else None
                    direction = {0: "down", 1: "up", 2: "left", 3: "right", 4: "stay"}.get(move_dir, "stay")
                    actual_movement = int(movement) if move_dir != 4 else 0
                    advance_text = "да" if advanced else "нет"
                    if advance_roll is not None:
                        max_move = int(base_m + advance_roll)
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
                    if move_dir == 4:
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
                            reward_delta += reward_cfg.VP_OBJECTIVE_PROXIMITY_REWARD
                            objective_proximity_delta += reward_cfg.VP_OBJECTIVE_PROXIMITY_REWARD
                            self._log_reward_unit(
                                "model",
                                modelName,
                                i,
                                "Reward (VP/объекты): "
                                f"proximity=+{reward_cfg.VP_OBJECTIVE_PROXIMITY_REWARD:.3f} (obj={j})",
                            )

                elif self.unitInAttack[i][0] == 1 and self.unit_health[i] > 0:
                    idOfE = self.unitInAttack[i][1]
                    if self.enemy_health[idOfE] <= 0:
                        reward_delta += reward_cfg.MOVEMENT_MELEE_TARGET_DEAD_BONUS
                        self._log_reward_unit(
                            "model",
                            modelName,
                            i,
                            "Reward (движение): "
                            f"цель мертва, выход из боя bonus=+{reward_cfg.MOVEMENT_MELEE_TARGET_DEAD_BONUS:.3f}",
                        )
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
                        retreated = False
                        if action["attack"] == 0:
                            if self.unit_health[i] * 2 >= self.enemy_health[idOfE]:
                                reward_delta -= reward_cfg.MOVEMENT_MELEE_RETREAT_PENALTY
                                self._log_reward_unit(
                                    "model",
                                    modelName,
                                    i,
                                    "Reward (движение): "
                                    f"отступление из боя penalty=-{reward_cfg.MOVEMENT_MELEE_RETREAT_PENALTY:.3f}",
                                )
                            self._log_unit(
                                "MODEL",
                                modelName,
                                i,
                                f"Отступление из боя с {self._format_unit_label('enemy', idOfE)}. Позиция до: {pos_before}",
                            )
                            self.unitFellBack[i] = True
                            retreated = True
                            if battleSh is True:
                                diceRoll = dice()
                                if diceRoll < 3:
                                    self.unit_health[i] -= self.unit_data[i]["W"]
                            self.unit_coords[i][0] += self.unit_data[i]["Movement"]
                            self.unit_coords[i] = bounds(self.unit_coords[i], self.b_len, self.b_hei)
                            self._adjust_end_move_from_terrain("model", i, pos_before, "movement_phase:model_fallback")
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
                            reward_delta += reward_cfg.MOVEMENT_MELEE_STAY_BONUS
                            self._log_reward_unit(
                                "model",
                                modelName,
                                i,
                                "Reward (движение): "
                                f"остался в бою bonus=+{reward_cfg.MOVEMENT_MELEE_STAY_BONUS:.3f}",
                            )
                        if not retreated:
                            self._log_unit(
                                "MODEL",
                                modelName,
                                i,
                                f"Остаётся в ближнем бою с {self._format_unit_label('enemy', idOfE)}, движение пропущено.",
                            )
            if objective_hold_delta != 0 or objective_proximity_delta != 0:
                total_obj_delta = objective_hold_delta + objective_proximity_delta
                self._log_reward(
                    "Reward (VP/объекты, движение): "
                    f"hold={objective_hold_delta:.3f}, proximity={objective_proximity_delta:.3f}, total={total_obj_delta:.3f}"
                )
            self._emit_event(
                {
                    "side": "enemy",
                    "phase": "movement",
                    "type": "phase_end",
                    "msg": "Движение завершено.",
                    "unit_id": None,
                    "unit_name": None,
                    "data": {"reward_delta": reward_delta},
                }
            )
            return advanced_flags, reward_delta, movement_meta

        if side == "enemy" and action is not None and not manual:
            advanced_flags = [False] * len(self.enemy_health)
            self.enemy_used_advance = [False] * len(self.enemy_health)
            self.enemy_advance_roll = [None] * len(self.enemy_health)
            move_dir = action.get("move", 4) if isinstance(action, dict) else 4
            attack_choice = action.get("attack", 1) if isinstance(action, dict) else 1
            for i in range(len(self.enemy_health)):
                unit_id = i + 11
                battleSh = battle_shock[i] if battle_shock else False
                pos_before = tuple(self.enemy_coords[i])
                if self.enemy_health[i] <= 0:
                    self._log_unit("enemy", unit_id, i, f"Юнит мертв, движение пропущено. Позиция: {pos_before}")
                    continue
                if self.enemyInAttack[i][0] == 0 and self.enemy_health[i] > 0:
                    base_m = self.enemy_data[i]["Movement"]
                    label = "move_num_" + str(i)
                    want = int(action.get(label, base_m)) if isinstance(action, dict) else base_m
                    advanced = (move_dir != 4) and (want > base_m)
                    advance_roll = None
                    if advanced:
                        advance_roll = dice()
                        max_move = base_m + advance_roll
                    else:
                        max_move = base_m
                    movement = min(want, max_move)

                    if move_dir == 0:
                        self.enemy_coords[i][0] += movement
                    elif move_dir == 1:
                        self.enemy_coords[i][0] -= movement
                    elif move_dir == 2:
                        self.enemy_coords[i][1] -= movement
                    elif move_dir == 3:
                        self.enemy_coords[i][1] += movement
                    elif move_dir == 4:
                        for j in range(len(self.coordsOfOM)):
                            if distance(self.enemy_coords[i], self.coordsOfOM[j]) <= 5:
                                pass

                    advanced_flags[i] = advanced
                    self.enemy_used_advance[i] = bool(advanced)
                    self.enemy_advance_roll[i] = int(advance_roll) if advance_roll is not None else None
                    direction = {0: "down", 1: "up", 2: "left", 3: "right", 4: "stay"}.get(move_dir, "stay")
                    actual_movement = movement if move_dir != 4 else 0
                    advance_text = "да" if advanced else "нет"
                    if advance_roll is not None:
                        advance_detail = f", бросок={advance_roll}, макс={max_move}"
                    else:
                        advance_detail = ""
                    self._log_unit(
                        "enemy",
                        unit_id,
                        i,
                        f"Позиция до: {pos_before}. Выбор: {direction}, advance={advance_text}{advance_detail}, distance={actual_movement}",
                    )

                    self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                    for j in range(len(self.unit_health)):
                        if self.enemy_coords[i] == self.unit_coords[j]:
                            self.enemy_coords[i][0] -= 1
                    self._adjust_end_move_from_terrain("enemy", i, pos_before, "movement_phase:enemy")
                    pos_after = tuple(self.enemy_coords[i])
                    if move_dir == 4:
                        self._log_unit("enemy", unit_id, i, f"Движение пропущено (no move). Позиция после: {pos_after}")
                    else:
                        self._log_unit("enemy", unit_id, i, f"Позиция после: {pos_after}")

                    if pos_before != pos_after:
                        self._resolve_overwatch(
                            defender_side="model",
                            moving_unit_side="enemy",
                            moving_idx=i,
                            phase="movement",
                            manual=os.getenv("MANUAL_DICE", "0") == "1",
                        )

                elif self.enemyInAttack[i][0] == 1 and self.enemy_health[i] > 0:
                    idOfM = self.enemyInAttack[i][1]
                    if self.unit_health[idOfM] <= 0:
                        self.enemyInAttack[i][0] = 0
                        self.enemyInAttack[i][1] = 0
                        self.unitInAttack[idOfM][0] = 0
                        self.unitInAttack[idOfM][1] = 0
                        self._log_unit(
                            "enemy",
                            unit_id,
                            i,
                            f"Цель в ближнем бою мертва ({self._format_unit_label('model', idOfM)}), юнит выходит из боя. Позиция: {pos_before}",
                        )
                    else:
                        if attack_choice == 0:
                            self._log_unit(
                                "enemy",
                                unit_id,
                                i,
                                f"Отступление из боя с {self._format_unit_label('model', idOfM)}. Позиция до: {pos_before}",
                            )
                            self.enemyFellBack[i] = True
                            if battleSh is True:
                                diceRoll = dice()
                                if diceRoll < 3:
                                    self.enemy_health[i] -= self.enemy_data[i]["W"]
                            self.enemy_coords[i][0] -= self.enemy_data[i]["Movement"]
                            self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                            self._adjust_end_move_from_terrain("enemy", i, pos_before, "movement_phase:enemy_fallback")
                            self.enemyInAttack[i][0] = 0
                            self.enemyInAttack[i][1] = 0
                            self.unitInAttack[idOfM][0] = 0
                            self.unitInAttack[idOfM][1] = 0
                            pos_after = tuple(self.enemy_coords[i])
                            self._log_unit("enemy", unit_id, i, f"Отступление завершено. Позиция после: {pos_after}")
                            if pos_before != pos_after:
                                self._resolve_overwatch(
                                    defender_side="model",
                                    moving_unit_side="enemy",
                                    moving_idx=i,
                                    phase="movement",
                                    manual=os.getenv("MANUAL_DICE", "0") == "1",
                                )
                        else:
                            self._log_unit(
                                "enemy",
                                unit_id,
                                i,
                                f"Остаётся в ближнем бою с {self._format_unit_label('model', idOfM)}, движение пропущено.",
                            )
            return advanced_flags

        if side == "enemy" and manual:
            advanced_flags = [False] * len(self.enemy_health)
            self.enemy_used_advance = [False] * len(self.enemy_health)
            self.enemy_advance_roll = [None] * len(self.enemy_health)
            for i in range(len(self.enemy_health)):
                self.current_action_index = i
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

                    base_move = int(self.enemy_data[i].get("Movement", 0) or 0)
                    overlay = self.get_unit_movement_overlay("enemy", i)
                    move_cells = overlay.get("move_cells") or []
                    advance_cells = overlay.get("advance_cells") or []
                    reachable = list(move_cells) + list(advance_cells)
                    if not reachable:
                        self._log(f"{unit_label}: нет достижимых клеток для движения (budget={base_move + 6}).")
                        advanced_flags[i] = False
                        continue

                    self.enemy_used_advance[i] = False
                    self.enemy_advance_roll[i] = None
                    self.updateBoard()
                    self.showBoard()

                    dest = None
                    move_set = set((int(x), int(y)) for x, y in move_cells)
                    advance_set = set((int(x), int(y)) for x, y in advance_cells)
                    while dest is None:
                        move_meta = {
                            "move_request": True,
                            "unit_id": int(playerName),
                            "unit_side": "player",
                            "movement_budget": int(base_move),
                            "movement_budget_advance": int(base_move + 6),
                            "reachable_cells": [[int(x), int(y)] for x, y in reachable],
                            "move_cells": [[int(x), int(y)] for x, y in move_cells],
                            "advance_cells": [[int(x), int(y)] for x, y in advance_cells],
                            "supports_stay": True,
                        }
                        answer = self._ensure_io().request_deploy_coord(
                            f"{unit_label}. Выберите клетку назначения (reachable={len(reachable)}): ",
                            x_min=0,
                            x_max=max(0, int(self.b_hei) - 1),
                            y_min=0,
                            y_max=max(0, int(self.b_len) - 1),
                            meta=move_meta,
                        )
                        if answer is None:
                            self.game_over = True
                            return None
                        mode = str(answer.get("mode") or "").strip().lower()
                        skip_requested = bool(answer.get("skip_movement"))
                        if mode == "stay" or skip_requested:
                            dest = (int(pos_before[1]), int(pos_before[0]))
                            move_mode = "stay"
                            source = "mode=stay" if mode == "stay" else "legacy skip-флаг"
                            self._log(
                                f"{unit_label}: движение stay ({source}). "
                                f"Позиция сохранена: ({int(dest[0])},{int(dest[1])})."
                            )
                            break
                        if answer.get("x") is None or answer.get("y") is None:
                            self._log(
                                f"{unit_label}: движение отклонено (нет координат). Где: warhamEnv.movement_phase. "
                                "Что делать дальше: выберите подсвеченную reachable-клетку или используйте mode=stay."
                            )
                            continue
                        tx = int(answer.get("x"))
                        ty = int(answer.get("y"))
                        cell = (tx, ty)
                        if cell in move_set:
                            move_mode = "normal"
                        elif cell in advance_set:
                            move_mode = "advance"
                        elif mode in {"normal", "move"} and cell in move_set:
                            move_mode = "normal"
                        elif mode in {"advance", "adv"} and cell in advance_set:
                            move_mode = "advance"
                        else:
                            self._log(
                                f"{unit_label}: клетка ({tx},{ty}) недостижима. Где: warhamEnv.movement_phase. "
                                "Что делать дальше: выберите подсвеченную reachable-клетку или используйте mode=stay."
                            )
                            continue
                        dest = cell

                    distance_cells = self._grid_distance_chebyshev(
                        (int(pos_before[0]), int(pos_before[1])),
                        (int(dest[1]), int(dest[0])),
                    )
                    advanced = move_mode == "advance"
                    adv_used = max(0, int(distance_cells) - int(base_move))
                    advance_roll = max(1, min(6, int(adv_used))) if advanced else 0
                    self.enemy_used_advance[i] = bool(advanced)
                    self.enemy_advance_roll[i] = int(advance_roll)
                    advanced_flags[i] = bool(advanced)
                    self._append_agent_log(
                        f"[MOVE] unit={playerName} {move_mode} to=({int(dest[0])},{int(dest[1])}) "
                        f"dist={int(distance_cells)} M={int(base_move)}"
                        + (f" adv={int(max(0, min(6, int(distance_cells) - int(base_move))))}" if advanced else "")
                    )
                    self.enemy_coords[i] = [int(dest[1]), int(dest[0])]

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
            self.enemy_used_advance = [False] * len(self.enemy_health)
            self.enemy_advance_roll = [None] * len(self.enemy_health)
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
                    base_m = int(self.enemy_data[i]["Movement"])
                    overlay = self.get_unit_movement_overlay("enemy", i)
                    move_cells = [(int(x), int(y), "normal") for x, y in (overlay.get("move_cells") or [])]
                    adv_cells = [(int(x), int(y), "advance") for x, y in (overlay.get("advance_cells") or [])]
                    stay_cell = (int(pos_before[1]), int(pos_before[0]), "stay")
                    candidates = move_cells + adv_cells + [stay_cell]
                    if not (move_cells or adv_cells):
                        self._log(f"[ENEMY][HEUR] Unit {i + 11}: движение stay, причина: нет reachable-клеток.")

                    target_row = int(self.unit_coords[idOfM][0])
                    target_col = int(self.unit_coords[idOfM][1])

                    def _heur_score(item):
                        x, y, mode = item
                        dist_to_target = float(self._grid_distance_euclid((int(y), int(x)), (target_row, target_col)))
                        dist_from_start = float(self._grid_distance_chebyshev((int(self.enemy_coords[i][0]), int(self.enemy_coords[i][1])), (int(y), int(x))))
                        mode_penalty = 0.0 if mode == "normal" else 0.1 if mode == "advance" else 0.25
                        return (dist_to_target, mode_penalty, -dist_from_start)

                    best_x, best_y, best_mode = min(candidates, key=_heur_score)
                    movement = int(self._grid_distance_chebyshev((int(self.enemy_coords[i][0]), int(self.enemy_coords[i][1])), (int(best_y), int(best_x))))
                    advanced = str(best_mode) == "advance" or int(movement) > int(base_m)
                    if str(best_mode) == "stay":
                        self._log(f"[ENEMY][HEUR] Unit {i + 11}: выбран режим stay (distance=0).")
                    adv_used = max(0, int(movement) - int(base_m))
                    advance_roll = max(1, min(6, int(adv_used))) if advanced else None
                    self.enemy_coords[i] = [int(best_y), int(best_x)]

                    self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                    for j in range(len(self.unit_health)):
                        if self.enemy_coords[i] == self.unit_coords[j]:
                            self.enemy_coords[i][0] -= 1
                    self._adjust_end_move_from_terrain("enemy", i, pos_before, "movement_phase:enemy")
                    advanced_flags[i] = advanced
                    self.enemy_used_advance[i] = bool(advanced)
                    self.enemy_advance_roll[i] = int(advance_roll) if advance_roll is not None else None

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

                shootAbleUnits = self.get_shoot_targets_for_unit("model", i)
                if len(shootAbleUnits) > 0:
                    valid_target_ids = shootAbleUnits
                    raw = action["shoot"]
                    if 0 <= raw < len(valid_target_ids):
                        idOfE = valid_target_ids[raw]
                        target_hp_prev = self.enemy_health[idOfE]
                        target_max_hp = self.enemy_data[idOfE]["W"] * self.enemy_data[idOfE]["#OfModels"]
                        distances = {j: self._shooting_distance_between_units("model", i, "enemy", j) for j in valid_target_ids}
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
                        effect = self._resolve_cover_effect_for_shot("model", i, "enemy", idOfE, base_effect=effect, phase="shooting")
                        threat_count_before_shot, _, _ = self._count_real_threats_to_model_unit(i)
                        _logger = None
                        if _verbose_logs_enabled():
                            _logger = RollLogger(auto_dice, agent_log_fn=self._append_agent_log)
                            _logger.configure_for_weapon(self.unit_weapon[i])
                            dmg, modHealth = attack(
                                self.unit_health[i],
                                self.unit_weapon[i],
                                self.unit_data[i],
                                self.enemy_health[idOfE],
                                self.enemy_data[idOfE],
                                effects=effect,
                                distance_to_target=self._shooting_distance_between_units("model", i, "enemy", idOfE),
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
                                distance_to_target=self._shooting_distance_between_units("model", i, "enemy", idOfE),
                            )
                        self._apply_health_update("enemy", idOfE, modHealth, reason="shooting")
                        damage_dealt = max(0.0, float(target_hp_prev - modHealth))
                        normalized_damage = damage_dealt / max(1.0, float(self.enemy_hp_max_total))
                        damage_term = reward_cfg.SHOOT_REWARD_DAMAGE_SCALE * normalized_damage
                        reward_delta += damage_term
                        if damage_term != 0:
                            self._log_reward_unit(
                                "model",
                                modelName,
                                i,
                                "Reward (стрельба): "
                                f"damage_term=+{damage_term:.3f} (norm={normalized_damage:.3f}, dealt={damage_dealt:.2f})",
                            )
                        kill_term = 0.0
                        if modHealth <= 0:
                            kill_term = reward_cfg.SHOOT_REWARD_KILL_BONUS
                            reward_delta += kill_term
                            self._log_reward_unit(
                                "model",
                                modelName,
                                i,
                                "Reward (стрельба): "
                                f"kill_bonus=+{kill_term:.3f}",
                            )
                        overkill = max(0.0, float(damage_dealt - target_hp_prev))
                        overkill_penalty = 0.0
                        if target_max_hp > 0 and overkill > 0:
                            overkill_penalty = reward_cfg.SHOOT_REWARD_OVERKILL_PENALTY * (overkill / target_max_hp)
                            reward_delta -= overkill_penalty
                            self._log_reward_unit(
                                "model",
                                modelName,
                                i,
                                "Reward (стрельба): "
                                f"overkill_penalty=-{overkill_penalty:.3f} (overkill={overkill:.2f})",
                            )
                        quality_term = 0.0
                        target_on_objective = self._is_position_near_objective(self.enemy_coords[idOfE])
                        if damage_dealt > 0:
                            if target_max_hp > 0 and target_hp_prev / target_max_hp <= 0.3:
                                quality_term += reward_cfg.SHOOT_REWARD_TARGET_LOW_HP
                            if target_on_objective:
                                quality_term += reward_cfg.SHOOT_REWARD_TARGET_ON_OBJ
                            if self.enemy_data[idOfE].get("OC", 0) >= 2:
                                quality_term += reward_cfg.SHOOT_REWARD_TARGET_HIGH_OC
                        reward_delta += quality_term
                        if quality_term != 0:
                            self._log_reward_unit(
                                "model",
                                modelName,
                                i,
                                "Reward (стрельба): "
                                f"quality_bonus=+{quality_term:.3f}",
                            )
                        objective_damage_term = 0.0
                        objective_kill_term = 0.0
                        if target_on_objective and damage_dealt > 0:
                            objective_damage_term = reward_cfg.DAMAGE_ON_OBJECTIVE_SCALE * damage_dealt
                            reward_delta += objective_damage_term
                            if objective_damage_term != 0:
                                self._log_reward_unit(
                                    "model",
                                    modelName,
                                    i,
                                    "Reward (стрельба/у цели): "
                                    f"damage_bonus=+{objective_damage_term:.3f} (dealt={damage_dealt:.2f})",
                                )
                            if modHealth <= 0:
                                objective_kill_term = reward_cfg.KILL_ON_OBJECTIVE_BONUS
                                reward_delta += objective_kill_term
                                self._log_reward_unit(
                                    "model",
                                    modelName,
                                    i,
                                    "Reward (стрельба/у цели): "
                                    f"kill_bonus=+{objective_kill_term:.3f}",
                                )
                        action_bonus = reward_cfg.SHOOT_REWARD_ACTION_BONUS
                        reward_delta += action_bonus
                        if action_bonus != 0:
                            self._log_reward_unit(
                                "model",
                                modelName,
                                i,
                                "Reward (стрельба): "
                                f"action_bonus=+{action_bonus:.3f}",
                            )

                        event_bonus = 0.0
                        if i in self._terrain_shaping_shot_bonus_units:
                            self._log_reward_unit(
                                "model",
                                modelName,
                                i,
                                "Reward (terrain event): бонус за выстрел из cover уже получен в этом ходу, повтор не начисляется.",
                            )
                        else:
                            pre_threat_count = int(threat_count_before_shot)
                            cover_ok, cover_soft, cover_reason = self._model_unit_cover_state(i)
                            post_threat_count, _, _ = self._count_real_threats_to_model_unit(i)
                            if not cover_ok:
                                self._log_reward_unit(
                                    "model",
                                    modelName,
                                    i,
                                    f"Reward (terrain event): бонус за выстрел из cover не начислен, причина: {cover_reason}.",
                                )
                            elif post_threat_count > pre_threat_count:
                                self._log_reward_unit(
                                    "model",
                                    modelName,
                                    i,
                                    "Reward (terrain event): бонус за выстрел из cover не начислен, "
                                    f"угроза выросла ({pre_threat_count} -> {post_threat_count}).",
                                )
                            else:
                                event_bonus = float(getattr(reward_cfg, "TERRAIN_EVENT_SHOT_FROM_COVER_BONUS", 0.03))
                                reward_delta += event_bonus
                                self._terrain_shaping_shot_bonus_units.add(i)
                                self._log_reward_unit(
                                    "model",
                                    modelName,
                                    i,
                                    "Reward (terrain event): "
                                    f"shot_from_cover=+{event_bonus:.3f} (cover_soft={cover_soft:.3f}, threat={pre_threat_count}->{post_threat_count}).",
                                )

                        shot_reward = (
                            damage_term
                            + kill_term
                            - overkill_penalty
                            + quality_term
                            + objective_damage_term
                            + objective_kill_term
                            + action_bonus
                            + event_bonus
                        )
                        self._log_reward_unit(
                            "model",
                            modelName,
                            i,
                            "Reward (стрельба): "
                            f"damage={damage_term:.3f} (norm={normalized_damage:.3f}, dealt={damage_dealt:.2f}), "
                            f"kill={kill_term:.3f}, overkill=-{overkill_penalty:.3f}, "
                            f"quality={quality_term:.3f}, "
                            f"obj_damage={objective_damage_term:.3f}, obj_kill={objective_kill_term:.3f}, "
                            f"action={action_bonus:.3f}, terrain_event={event_bonus:.3f}, total={shot_reward:.3f}",
                        )
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
                        if _logger is not None:
                            _logger.print_shoot_report(
                                weapon=self.unit_weapon[i],
                                attacker_data=self.unit_data[i],
                                defender_data=self.enemy_data[idOfE],
                                dmg_list=dmg,
                                effect=effect,
                                attacker_label=self._format_unit_label("model", i),
                                defender_label=self._format_unit_label("enemy", idOfE),
                            )
                    else:
                        penalty = float(getattr(reward_cfg, "SHOOT_REWARD_INVALID_TARGET_PENALTY", 0.20))
                        reward_delta -= penalty
                        target_list = self._format_unit_choices("enemy", valid_target_ids)
                        self._log_unit(
                            "MODEL",
                            modelName,
                            i,
                            f"Цели в дальности: {target_list}, выбрана недоступная цель (raw={raw}). Стрельба пропущена.",
                        )
                        self._log_reward_unit(
                            "model",
                            modelName,
                            i,
                            f"Reward (стрельба): штраф за пропуск = -{penalty:.3f}",
                        )
                        if _verbose_logs_enabled():
                            self._log(
                                f"[MODEL][SHOOT] Невалидный выбор цели: raw={raw}, доступные={valid_target_ids} (ожидался индекс 0..{len(valid_target_ids) - 1}). Стрельба пропущена."
                            )
                        if self.trunc is False:
                            self._log(f"{self._format_unit_label('model', i)} не смог стрелять: выбранная цель недоступна.")
                else:
                    self._log_unit("MODEL", modelName, i, "Нет целей в дальности, стрельба пропущена.")
            self._emit_event(
                {
                    "side": "enemy",
                    "phase": "shooting",
                    "type": "phase_end",
                    "msg": "Стрельба завершена.",
                    "unit_id": None,
                    "unit_name": None,
                    "data": {"reward_delta": reward_delta},
                }
            )
            return reward_delta
        elif side == "enemy" and action is not None and not manual:
            for i in range(len(self.enemy_health)):
                unit_id = i + 11
                advanced = advanced_flags[i] if advanced_flags else False
                if self.enemy_health[i] <= 0:
                    self._log_unit("enemy", unit_id, i, "Юнит мертв, стрельба пропущена.")
                    continue
                if self.enemyFellBack[i]:
                    self._log_unit("enemy", unit_id, i, "Fall Back в этом ходу — стрельба недоступна.")
                    continue
                if self.enemyInAttack[i][0] == 1:
                    self._log_unit("enemy", unit_id, i, "Юнит в ближнем бою, стрельба недоступна.")
                    continue
                if self.enemy_weapon[i] == "None":
                    self._log_unit("enemy", unit_id, i, "Нет дальнобойного оружия, стрельба пропущена.")
                    continue
                if advanced and not weapon_is_assault(self.enemy_weapon[i]):
                    self._log_unit("enemy", unit_id, i, "Advance без Assault — стрельба пропущена.")
                    continue

                shootAbleUnits = self.get_shoot_targets_for_unit("enemy", i)
                if len(shootAbleUnits) > 0:
                    valid_target_ids = shootAbleUnits
                    raw = action.get("shoot", 0) if isinstance(action, dict) else 0
                    if 0 <= raw < len(valid_target_ids):
                        idOfM = valid_target_ids[raw]
                        target_list = self._format_unit_choices("model", valid_target_ids)
                        self._log_unit(
                            "enemy",
                            unit_id,
                            i,
                            f"Цели в дальности: {target_list}, выбрана: {self._format_unit_label('model', idOfM)} (причина: выбор политики)",
                        )
                        effect = self._maybe_use_smokescreen(
                            defender_side="model",
                            defender_idx=idOfM,
                            phase="shooting",
                            manual=os.getenv("MANUAL_DICE", "0") == "1",
                        )
                        effect = self._resolve_cover_effect_for_shot("enemy", i, "model", idOfM, base_effect=effect, phase="shooting")
                        _logger = None
                        if _verbose_logs_enabled():
                            _logger = RollLogger(auto_dice, agent_log_fn=self._append_agent_log)
                            _logger.configure_for_weapon(self.enemy_weapon[i])
                            dmg, modHealth = attack(
                                self.enemy_health[i],
                                self.enemy_weapon[i],
                                self.enemy_data[i],
                                self.unit_health[idOfM],
                                self.unit_data[idOfM],
                                effects=effect,
                                distance_to_target=self._shooting_distance_between_units("enemy", i, "model", idOfM),
                                roller=_logger.roll,
                            )
                        else:
                            dmg, modHealth = attack(
                                self.enemy_health[i],
                                self.enemy_weapon[i],
                                self.enemy_data[i],
                                self.unit_health[idOfM],
                                self.unit_data[idOfM],
                                effects=effect,
                                distance_to_target=self._shooting_distance_between_units("enemy", i, "model", idOfM),
                            )
                        self._apply_health_update("model", idOfM, modHealth, reason="shooting")
                        self._log_unit(
                            "enemy",
                            unit_id,
                            i,
                            f"Итог урона по {self._format_unit_label('model', idOfM)}: {float(np.sum(dmg))}",
                        )
                        if self.trunc is False:
                            self._log(
                                f"{self._format_unit_label('enemy', i)} стреляет по {self._format_unit_label('model', idOfM)}: урон {float(np.sum(dmg))}."
                            )
                        else:
                            self.modelUpdates += "{} стреляет по {} {} раз(а)\n".format(
                                self._format_unit_label("enemy", i),
                                self._format_unit_label("model", idOfM),
                                sum(dmg),
                            )
                        if _logger is not None:
                            _logger.print_shoot_report(
                                weapon=self.enemy_weapon[i],
                                attacker_data=self.enemy_data[i],
                                defender_data=self.unit_data[idOfM],
                                dmg_list=dmg,
                                effect=effect,
                                attacker_label=self._format_unit_label("enemy", i),
                                defender_label=self._format_unit_label("model", idOfM),
                            )
                    else:
                        target_list = self._format_unit_choices("model", valid_target_ids)
                        self._log_unit(
                            "enemy",
                            unit_id,
                            i,
                            f"Цели в дальности: {target_list}, выбрана недоступная цель (raw={raw}). Стрельба пропущена.",
                        )
                        if _verbose_logs_enabled():
                            self._log(
                                f"[PLAYER][SHOOT] Невалидный выбор цели: raw={raw}, доступные={valid_target_ids} (ожидался индекс 0..{len(valid_target_ids) - 1}). Стрельба пропущена."
                            )
                        if self.trunc is False:
                            self._log(f"{self._format_unit_label('enemy', i)} не смог стрелять: выбранная цель недоступна.")
                else:
                    self._log_unit("enemy", unit_id, i, "Нет целей в дальности, стрельба пропущена.")
        elif side == "enemy" and manual:
            for i in range(len(self.enemy_health)):
                playerName = i + 11
                unit_label = self._format_unit_label("enemy", i, unit_id=playerName)
                advanced = advanced_flags[i] if advanced_flags else False
                if self.enemy_health[i] <= 0:
                    self._log(f"{unit_label}: юнит мертв — стрельба пропущена.")
                    continue
                if self.enemyFellBack[i]:
                    self._log(f"{unit_label}: отступил в этом ходу — стрельба пропущена.")
                    continue
                if self.enemy_weapon[i] != "None":
                    if advanced and not weapon_is_assault(self.enemy_weapon[i]):
                        self._log(f"{unit_label}: был Advance без Assault — стрельба пропущена.")
                    else:
                        shootAble = self.get_shoot_targets_for_unit("enemy", i)
                        targets_with_rejected = self.get_shoot_targets_for_unit("enemy", i, include_rejected=True)
                        if (
                            isinstance(targets_with_rejected, tuple)
                            and len(targets_with_rejected) == 2
                        ):
                            _, rejected_targets = targets_with_rejected
                        else:
                            rejected_targets = []
                            self._log(
                                f"[WARN][SHOOT] {unit_label}: get_shoot_targets_for_unit вернул некорректный формат "
                                f"({type(targets_with_rejected).__name__}). Где: warhamEnv.shooting_phase(enemy, manual). "
                                "Что делать дальше: проверить контракт include_rejected=True и вернуть (targets, rejected)."
                            )
                        if len(shootAble) > 0:
                            response = False
                            while response is False:
                                target_ids = [int(idx) for idx in shootAble]
                                targets_label = self._format_unit_choices("model", target_ids)
                                options = [str(21 + int(idx)) for idx in target_ids]
                                reject_meta = []
                                for item in list(rejected_targets or []):
                                    if not isinstance(item, dict):
                                        continue
                                    target_id = item.get("target_id")
                                    reason = str(item.get("reason") or "").strip()
                                    if target_id is None or not reason:
                                        continue
                                    reject_meta.append({"target_id": int(target_id), "reason": reason})
                                shoot = self._request_choice(
                                    f"Выберите цель для стрельбы. Стреляет: {unit_label}. Доступные цели: {targets_label}. Введите ID цели: ",
                                    options,
                                    meta={
                                        "shoot_filtered": reject_meta,
                                        "shooter_id": int(11 + i),
                                    },
                                )
                                if shoot is None:
                                    self.game_over = True
                                    return None
                                shoot_value = str(shoot).strip()
                                shoot_parts = [part for part in re.split(r"[|,;:]", shoot_value) if str(part).strip()]
                                shoot_target_raw = shoot_parts[0].strip() if shoot_parts else shoot_value
                                dice_count = None
                                if len(shoot_parts) > 1 and str(shoot_parts[1]).strip().isdigit():
                                    dice_count = int(str(shoot_parts[1]).strip())
                                if is_num(shoot_target_raw) is True and int(shoot_target_raw) - 21 in target_ids:
                                    idOfE = int(shoot_target_raw) - 21
                                    if dice_count is not None:
                                        self._log(
                                            f"{unit_label}: Fire popover -> цель={self._format_unit_label('model', idOfE)}, кубы(D6)={dice_count}."
                                        )
                                    effect = self._maybe_use_smokescreen(
                                        defender_side="model",
                                        defender_idx=idOfE,
                                        phase="shooting",
                                        manual=False,
                                    )
                                    effect = self._resolve_cover_effect_for_shot("enemy", i, "model", idOfE, base_effect=effect, phase="shooting")
                                    logger = RollLogger(player_dice, agent_log_fn=self._append_agent_log)
                                    logger.configure_for_weapon(self.enemy_weapon[i])
                                    dmg, modHealth = attack(
                                        self.enemy_health[i],
                                        self.enemy_weapon[i],
                                        self.enemy_data[i],
                                        self.unit_health[idOfE],
                                        self.unit_data[idOfE],
                                        effects=effect,
                                        distance_to_target=self._shooting_distance_between_units("enemy", i, "model", idOfE),
                                        roller=logger.roll,
                                    )
                                    self._apply_health_update("model", idOfE, modHealth, reason="overwatch")
                                    self._log(
                                        f"{unit_label} нанёс {sum(dmg)} урона по {self._format_unit_label('model', idOfE)}"
                                    )
                                    logger.print_shoot_report(
                                        weapon=self.enemy_weapon[i],
                                        attacker_data=self.enemy_data[i],
                                        defender_data=self.unit_data[idOfE],
                                        dmg_list=dmg,
                                        effect=effect,
                                        attacker_label=unit_label,
                                        defender_label=self._format_unit_label("model", idOfE),
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
                        shootAbleUnits = self.get_shoot_targets_for_unit("enemy", i)
                        if len(shootAbleUnits) > 0:
                            idOfM = np.random.choice(shootAbleUnits)
                            effect = self._maybe_use_smokescreen(
                                defender_side="model",
                                defender_idx=idOfM,
                                phase="shooting",
                                manual=False,
                            )
                            effect = self._resolve_cover_effect_for_shot("enemy", i, "model", idOfM, base_effect=effect, phase="shooting")
                            dmg, modHealth = attack(
                                self.enemy_health[i],
                                self.enemy_weapon[i],
                                self.enemy_data[i],
                                self.unit_health[idOfM],
                                self.unit_data[idOfM],
                                effects=effect,
                                distance_to_target=self._shooting_distance_between_units("enemy", i, "model", idOfM),
                            )
                            self._apply_health_update("model", idOfM, modHealth, reason="shooting")
                            if self.trunc is False:
                                self._log(
                                    f"{self._format_unit_label('enemy', i)} стреляет по {self._format_unit_label('model', idOfM)}: урон {float(np.sum(dmg))}."
                                )
        return None

    def charge_phase(self, side: str, advanced_flags=None, action=None, manual: bool = False):
        self.begin_phase(side, "charge")
        if side == "model":
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
                            self._adjust_end_move_from_terrain("model", i, pos_before, "charge_phase:model")
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
                            reward_delta += reward_cfg.CHARGE_SUCCESS_REWARD
                            self._log_reward_unit(
                                "model",
                                modelName,
                                i,
                                "Reward (чардж): "
                                f"success_bonus=+{reward_cfg.CHARGE_SUCCESS_REWARD:.3f}",
                            )
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
                            reward_delta -= reward_cfg.CHARGE_FAIL_PENALTY
                            self._log_reward_unit(
                                "model",
                                modelName,
                                i,
                                "Reward (чардж): "
                                f"fail_penalty=-{reward_cfg.CHARGE_FAIL_PENALTY:.3f}",
                            )
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
                                f"Цели в 12\": {target_list}. {roll_text}. Чардж пропущен при доступных целях (penalty=0).",
                            )
                        else:
                            self._log_unit("MODEL", modelName, i, "Нет целей в 12\", чардж пропущен.")
            if not any_charge_targets:
                self._log("[MODEL] Чардж: нет доступных целей")
            self._emit_event(
                {
                    "side": "enemy",
                    "phase": "charge",
                    "type": "phase_end",
                    "msg": "Чардж завершён.",
                    "unit_id": None,
                    "unit_name": None,
                    "data": {"reward_delta": reward_delta},
                }
            )
            return reward_delta
        elif side == "enemy" and action is not None and not manual:
            any_charge_targets = False
            for i in range(len(self.enemy_health)):
                unit_id = i + 11
                advanced = advanced_flags[i] if advanced_flags else False
                pos_before = tuple(self.enemy_coords[i])
                if self.enemy_health[i] <= 0:
                    self._log_unit("enemy", unit_id, i, "Юнит мертв, чардж пропущен.")
                    continue
                if self.enemyFellBack[i]:
                    self._log_unit("enemy", unit_id, i, "Fall Back в этом ходу — чардж невозможен.")
                    continue
                if self.enemyInAttack[i][0] == 1:
                    self._log_unit("enemy", unit_id, i, "Уже в ближнем бою, чардж невозможен.")
                    continue
                if advanced:
                    self._log_unit("enemy", unit_id, i, "Advance — чардж невозможен.")
                else:
                    potential_targets = []
                    for j in range(len(self.unit_health)):
                        if distance(self.unit_coords[j], self.enemy_coords[i]) <= 12 and self.unitInAttack[j][0] == 0 and self.unit_health[j] > 0:
                            potential_targets.append(j)
                    if potential_targets:
                        any_charge_targets = True
                    if action.get("attack", 0) != 1:
                        if potential_targets:
                            target_list = self._format_unit_choices("model", potential_targets)
                            self._log_unit(
                                "enemy",
                                unit_id,
                                i,
                                f"Доступные цели для чарджа: {target_list}. Решение: пропуск чарджа.",
                            )
                        else:
                            self._log_unit("enemy", unit_id, i, "Нет целей в 12\", чардж пропущен.")
                        continue
                    chargeAble = []
                    dice_vals = dice(num=2)
                    diceRoll = sum(dice_vals)
                    for j in range(len(self.unit_health)):
                        if distance(self.unit_coords[j], self.enemy_coords[i]) <= 12 and self.unitInAttack[j][0] == 0 and self.unit_health[j] > 0:
                            if distance(self.unit_coords[j], self.enemy_coords[i]) - diceRoll <= 5:
                                chargeAble.append(j)
                    if len(chargeAble) > 0:
                        idOfM = action.get("charge", 0)
                        target_list = self._format_unit_choices("model", chargeAble)
                        dist_to_target = distance(self.unit_coords[idOfM], self.enemy_coords[i]) if idOfM in chargeAble else None
                        if _verbose_logs_enabled():
                            roll_text = f"бросок: {dice_vals[0]} + {dice_vals[1]} = {diceRoll}"
                        else:
                            roll_text = f"бросок total={diceRoll}"
                        if idOfM in chargeAble:
                            self._log_unit_phase(
                                self._display_side("enemy"),
                                "charge",
                                unit_id,
                                i,
                                f"Charge объявлен по цели {self._format_unit_label('model', idOfM)}. Дистанция: {dist_to_target:.1f}. Бросок 2D6: {dice_vals[0]} + {dice_vals[1]} = {diceRoll}.",
                            )
                            self._log_unit(
                                "enemy",
                                unit_id,
                                i,
                                f"Чардж цели: {target_list}, выбрана {self._format_unit_label('model', idOfM)} (dist={dist_to_target:.1f}). {roll_text}. Результат: успех.",
                            )
                            self.enemyInAttack[i][0] = 1
                            self.enemyInAttack[i][1] = idOfM
                            self.enemy_coords[i][0] = self.unit_coords[idOfM][0] + 1
                            self.enemy_coords[i][1] = self.unit_coords[idOfM][1] + 1
                            self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
                            self._adjust_end_move_from_terrain("enemy", i, pos_before, "charge_phase:enemy")
                            self.unitInAttack[idOfM][0] = 1
                            self.unitInAttack[idOfM][1] = i
                            self.enemyCharged[i] = 1
                            pos_after = tuple(self.enemy_coords[i])
                            self._log_unit_phase(
                                self._display_side("enemy"),
                                "charge",
                                unit_id,
                                i,
                                f"Движение чарджа: {pos_before} -> {pos_after}, в контакте={self.enemyInAttack[i][0] == 1}.",
                            )
                            self._resolve_heroic_intervention(
                                defender_side="model",
                                charging_side="enemy",
                                charging_idx=i,
                                phase="charge",
                                manual=os.getenv("MANUAL_DICE", "0") == "1",
                            )
                        else:
                            reason = "цель вне досягаемости" if idOfM in potential_targets else "цель недоступна"
                            if idOfM in potential_targets:
                                dist_to_target = distance(self.unit_coords[idOfM], self.enemy_coords[i])
                                self._log_unit_phase(
                                    self._display_side("enemy"),
                                    "charge",
                                    unit_id,
                                    i,
                                    f"Charge объявлен по цели {self._format_unit_label('model', idOfM)}. Дистанция: {dist_to_target:.1f}. Бросок 2D6: {dice_vals[0]} + {dice_vals[1]} = {diceRoll}.",
                                )
                            target_list = self._format_unit_choices("model", potential_targets)
                            self._log_unit(
                                "enemy",
                                unit_id,
                                i,
                                f"Чардж цели: {target_list}, выбрана {self._format_unit_label('model', idOfM)}. {roll_text}. Результат: провал ({reason}).",
                            )
                    else:
                        if potential_targets:
                            target_list = self._format_unit_choices("model", potential_targets)
                            if _verbose_logs_enabled():
                                roll_text = f"бросок: {dice_vals[0]} + {dice_vals[1]} = {diceRoll}"
                            else:
                                roll_text = f"бросок total={diceRoll}"
                            self._log_unit(
                                "enemy",
                                unit_id,
                                i,
                                f"Цели в 12\": {target_list}. {roll_text}. Нет достижимых целей.",
                            )
                        else:
                            self._log_unit("enemy", unit_id, i, "Нет целей в 12\", чардж пропущен.")
            if not any_charge_targets:
                self._log("[PLAYER] Чардж: нет доступных целей")
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
                                self._adjust_end_move_from_terrain("enemy", i, pos_before, "charge_phase:enemy_manual")
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
                            self._adjust_end_move_from_terrain("enemy", i, pos_before, "charge_phase:enemy")
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
        reward_delta = 0.0
        engaged_pairs = []
        pre_enemy_hp_total = None
        pre_model_hp_total = None
        pre_enemy_dead = None
        pre_obj_controlled = None
        advantage_term = 0.0
        strength_term = 0.0
        if side == "model":
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
                        engaged_pairs.append((idx, def_idx))
                if engaged_pairs:
                    pre_enemy_hp_total = float(sum(self.enemy_health))
                    pre_model_hp_total = float(sum(self.unit_health))
                    pre_enemy_dead = sum(1 for hp in self.enemy_health if hp <= 0)
                    pre_enemy_hp_by_idx = {}
                    pre_enemy_on_obj = {}
                    self.refresh_objective_control()
                    pre_obj_controlled, _ = controlled_objectives(self, "model")
                    for model_idx, enemy_idx in engaged_pairs:
                        if enemy_idx not in pre_enemy_hp_by_idx:
                            pre_enemy_hp_by_idx[enemy_idx] = float(self.enemy_health[enemy_idx])
                            pre_enemy_on_obj[enemy_idx] = self._is_position_near_objective(
                                self.enemy_coords[enemy_idx]
                            )
                        model_max_hp = self._unit_max_hp("model", model_idx)
                        enemy_max_hp = self._unit_max_hp("enemy", enemy_idx)
                        model_hp_frac = float(self.unit_health[model_idx]) / model_max_hp
                        enemy_hp_frac = float(self.enemy_health[enemy_idx]) / enemy_max_hp
                        advantage = max(-1.0, min(1.0, model_hp_frac - enemy_hp_frac))
                        advantage_term += reward_cfg.MELEE_ADVANTAGE_SCALE * advantage
                        model_power = self._melee_strength_score("model", model_idx)
                        enemy_power = self._melee_strength_score("enemy", enemy_idx)
                        if model_power > enemy_power:
                            strength_term += reward_cfg.MELEE_STRENGTH_SCALE
                        elif model_power < enemy_power:
                            strength_term -= reward_cfg.MELEE_STRENGTH_SCALE
        self.resolve_fight_phase(active_side=side, trunc=self.trunc)

        if side == "model" and engaged_pairs:
            post_enemy_hp_total = float(sum(self.enemy_health))
            post_model_hp_total = float(sum(self.unit_health))
            post_enemy_dead = sum(1 for hp in self.enemy_health if hp <= 0)

            damage_dealt = max(0.0, pre_enemy_hp_total - post_enemy_hp_total)
            damage_taken = max(0.0, pre_model_hp_total - post_model_hp_total)
            damage_dealt_norm = damage_dealt / max(1.0, float(self.enemy_hp_max_total))
            damage_taken_norm = damage_taken / max(1.0, float(self.model_hp_max_total))
            damage_term = reward_cfg.MELEE_REWARD_DAMAGE_SCALE * damage_dealt_norm
            taken_term = reward_cfg.MELEE_REWARD_TAKEN_SCALE * damage_taken_norm
            kill_delta = max(0, post_enemy_dead - pre_enemy_dead)
            kill_term = reward_cfg.MELEE_REWARD_KILL_BONUS * kill_delta

            objective_damage = 0.0
            objective_kills = 0
            for enemy_idx, pre_hp in pre_enemy_hp_by_idx.items():
                if not pre_enemy_on_obj.get(enemy_idx, False):
                    continue
                post_hp = float(self.enemy_health[enemy_idx])
                objective_damage += max(0.0, pre_hp - post_hp)
                if pre_hp > 0 and post_hp <= 0:
                    objective_kills += 1
            objective_damage_term = reward_cfg.DAMAGE_ON_OBJECTIVE_SCALE * objective_damage
            objective_kill_term = reward_cfg.KILL_ON_OBJECTIVE_BONUS * objective_kills

            self.refresh_objective_control()
            post_obj_controlled, _ = controlled_objectives(self, "model")
            obj_delta = post_obj_controlled - (pre_obj_controlled or 0)
            obj_term = reward_cfg.MELEE_OBJECTIVE_CONTROL_SCALE * obj_delta

            if damage_term != 0:
                reward_delta += damage_term
                self._log_reward(
                    "Reward (бой): "
                    f"damage_term=+{damage_term:.3f} (norm={damage_dealt_norm:.3f})"
                )
            if kill_term != 0:
                reward_delta += kill_term
                self._log_reward(
                    "Reward (бой): "
                    f"kill_term=+{kill_term:.3f} (delta={kill_delta})"
                )
            if taken_term != 0:
                reward_delta -= taken_term
                self._log_reward(
                    "Reward (бой): "
                    f"taken_penalty=-{taken_term:.3f} (norm={damage_taken_norm:.3f})"
                )
            if advantage_term != 0:
                reward_delta += advantage_term
                self._log_reward(
                    "Reward (бой): "
                    f"advantage_term={advantage_term:+.3f}"
                )
            if strength_term != 0:
                reward_delta += strength_term
                self._log_reward(
                    "Reward (бой): "
                    f"strength_term={strength_term:+.3f}"
                )
            if obj_term != 0:
                reward_delta += obj_term
                self._log_reward(
                    "Reward (бой): "
                    f"objective_term={obj_term:+.3f} (delta={obj_delta})"
                )
            if objective_damage_term != 0:
                reward_delta += objective_damage_term
                self._log_reward(
                    "Reward (бой/у цели): "
                    f"damage_term=+{objective_damage_term:.3f} (raw={objective_damage:.2f})"
                )
            if objective_kill_term != 0:
                reward_delta += objective_kill_term
                self._log_reward(
                    "Reward (бой/у цели): "
                    f"kill_term=+{objective_kill_term:.3f} (count={objective_kills})"
                )
            if obj_term != 0:
                self._log_reward(
                    "Reward (VP/объекты, бой): "
                    f"delta={obj_delta}, term={obj_term:.3f}"
                )
            if objective_damage_term != 0 or objective_kill_term != 0:
                self._log_reward(
                    "Reward (объекты, бой): "
                    f"damage={objective_damage_term:.3f} (raw={objective_damage:.2f}), "
                    f"kills={objective_kill_term:.3f} (count={objective_kills})"
                )
            self._log_reward(
                "Reward (бой): "
                f"damage={damage_term:.3f} (norm={damage_dealt_norm:.3f}, dealt={damage_dealt:.2f}), "
                f"kills={kill_term:.3f} (delta={kill_delta}), "
                f"taken=-{taken_term:.3f} (norm={damage_taken_norm:.3f}, taken={damage_taken:.2f}), "
                f"advantage={advantage_term:.3f}, strength={strength_term:.3f}, "
                f"objectives={obj_term:.3f} (delta={obj_delta}), total={reward_delta:.3f}"
            )
        if side == "model":
            self._emit_event(
                {
                    "side": "enemy",
                    "phase": "fight",
                    "type": "phase_end",
                    "msg": "Фаза боя завершена.",
                    "unit_id": None,
                    "unit_name": None,
                    "data": {"reward_delta": reward_delta},
                }
            )
        return reward_delta

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

    def reset(self, *, seed=None, options=None, **kwargs):
        super().reset(seed=seed)
        opts = options or {}
        opts.update(kwargs)
        m = opts.get("m", self.model)
        e = opts.get("e", self.enemy)
        playType = opts.get("playType", False)
        Type = opts.get("Type", "small")
        trunc = opts.get("trunc", False)

        # keep original references too
        self.model = m
        self.enemy = e

        self.iter = 0
        self.trunc = trunc
        self.playType = playType
        self._state_flush_last_ts = 0.0
        self._state_flush_pending = False

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
        self.unit_model_wounds = []
        self.enemy_model_wounds = []
        self.unit_anchor_coords = []
        self.enemy_anchor_coords = []
        self.unit_model_positions = []
        self.enemy_model_positions = []
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
        self._prev_vp_diff = 0
        self._objective_hold_streaks = [0] * len(self.coordsOfOM)
        self._phase_event_emitted = False
        self._phase_unit_logged = set()
        self._terrain_shaping_shot_bonus_units = set()
        get_event_recorder().clear()

        for i in range(len(self.enemy_data)):
            self.enemy_coords.append([self.enemy[i].showCoords()[0], self.enemy[i].showCoords()[1]])
            self.enemy_health.append(self.enemy_data[i]["W"] * self.enemy_data[i]["#OfModels"])
            self.enemyInAttack.append([0, 0])
        self.enemyFellBack = [False] * len(self.enemy_health)
        self.enemy_used_advance = [False] * len(self.enemy_health)
        self.enemy_advance_roll = [None] * len(self.enemy_health)
        self.enemy_hp_max_total = max(
            1,
            sum(
                unit.get("W", 0) * unit.get("#OfModels", 0)
                for unit in self.enemy_data
                if isinstance(unit, dict)
            ),
        )

        for i in range(len(self.unit_data)):
            self.unit_coords.append([self.model[i].showCoords()[0], self.model[i].showCoords()[1]])
            self.unit_health.append(self.unit_data[i]["W"] * self.unit_data[i]["#OfModels"])
            self.unitInAttack.append([0, 0])
        self.unitFellBack = [False] * len(self.unit_health)
        self.model_used_advance = [False] * len(self.unit_health)
        self.model_advance_roll = [None] * len(self.unit_health)
        self.model_hp_max_total = max(
            1,
            sum(
                unit.get("W", 0) * unit.get("#OfModels", 0)
                for unit in self.unit_data
                if isinstance(unit, dict)
            ),
        )

        self._init_model_state_from_health()

        self.game_over = False
        self.last_end_reason = ""
        self.last_winner = None
        self.current_action_index = 0
        info = self.get_info()

        if Type == "big":
            self.updateBoard()

        return self._get_observation(), info

    def enemyTurn(self, trunc=False, policy_fn=None):
        self._invalidate_target_cache("enemy_turn_start")
        self.unitCharged = [0] * len(self.unit_health)
        self.enemyCharged = [0] * len(self.enemy_health)
        if trunc is True:
            self.trunc = True

        self.active_side = "enemy"
        action = None
        if policy_fn is not None:
            obs = self.get_observation_for_side("enemy")
            action = policy_fn(obs)
        battle_shock = self.command_phase("enemy", action=action)
        advanced_flags = self.movement_phase("enemy", action=action, battle_shock=battle_shock)
        self._invalidate_target_cache("enemy_after_movement")
        self.shooting_phase("enemy", advanced_flags=advanced_flags, action=action)
        self.charge_phase("enemy", advanced_flags=advanced_flags, action=action)
        self.fight_phase("enemy")
        self._invalidate_target_cache("enemy_after_fight")
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
        2) Then alternate fights starting with the active side
        Only units within Engagement (unitInAttack/enemyInAttack) can fight.
        No pile-in/consolidate here (упрощение).
        """
        quiet = self.trunc if trunc is None else trunc
        fight_report = _fight_report_enabled()
        use_roll_logger = fight_report or _verbose_logs_enabled()

        # кто кидает кубы (если MANUAL_DICE=1 — спрашиваем руками)
        dice_fn = player_dice if os.getenv("MANUAL_DICE", "0") == "1" else auto_dice

        def _log(msg: str):
            if quiet is False:
                self._log(msg)

        def _remaining_models(side: str, idx: int, hp_value: Optional[float]) -> Optional[int]:
            data_list = self.unit_data if side == "model" else self.enemy_data
            if not (0 <= idx < len(data_list)) or not isinstance(data_list[idx], dict):
                return None
            wounds = data_list[idx].get("W")
            try:
                wounds = float(wounds)
            except Exception:
                return None
            if wounds <= 0 or hp_value is None:
                return None
            if hp_value <= 0:
                return 0
            return int((hp_value + wounds - 1) // wounds)

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
                models_before = _remaining_models("enemy", def_idx, hp_before)

                _logger = None
                if quiet is False and use_roll_logger:
                    _logger = RollLogger(auto_dice, agent_log_fn=self._append_agent_log)
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

                self._apply_health_update("enemy", def_idx, modHealth, reason="fight")
                models_after = _remaining_models("enemy", def_idx, modHealth)

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
                        attacker_label=self._format_unit_label("model", att_idx),
                        defender_label=self._format_unit_label("enemy", def_idx),
                        hp_before=hp_before,
                        hp_after=modHealth,
                        models_before=models_before,
                        models_after=models_after,
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
                models_before = _remaining_models("model", def_idx, hp_before)

                _logger = None
                manual_dice = os.getenv("MANUAL_DICE", "0") == "1"
                if quiet is False and use_roll_logger:
                    _logger = RollLogger(dice_fn, agent_log_fn=self._append_agent_log)
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
                    extra_kwargs = {"roller": dice_fn} if manual_dice else {}
                    dmg, modHealth = attack(
                        self.enemy_health[att_idx],
                        weapon,
                        attacker_data,
                        self.unit_health[def_idx],
                        defender_data,
                        rangeOfComb="Melee",
                        **extra_kwargs,
                    )

                self._apply_health_update("model", def_idx, modHealth, reason="fight")
                models_after = _remaining_models("model", def_idx, modHealth)

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
                        attacker_label=self._format_unit_label("enemy", att_idx),
                        defender_label=self._format_unit_label("model", def_idx),
                        hp_before=hp_before,
                        hp_after=modHealth,
                        models_before=models_before,
                        models_after=models_after,
                    )

                if self.unit_health[def_idx] <= 0:
                    self.unitInAttack[def_idx] = [0, 0]
                    self.enemyInAttack[att_idx] = [0, 0]

                return True

        manual_enemy = bool(getattr(self, "playType", False))

        def _prompt_enemy_target(att_idx: int) -> Optional[int]:
            def_idx = self.enemyInAttack[att_idx][1]
            targets = []
            if 0 <= def_idx < len(self.unit_health) and self.unit_health[def_idx] > 0:
                targets = [def_idx]
            if not targets:
                self._log("Целей для атаки нет: бой пропущен.")
                return None
            target_choices = self._format_unit_choices("model", targets)
            options = [str(21 + idx) for idx in targets]
            while True:
                choice = self._request_choice(
                    f"Выберите цель для атаки. Атакует: {self._format_unit_label('enemy', att_idx)}. "
                    f"Доступные цели: {target_choices}. Введите ID цели: ",
                    options,
                )
                if choice is None:
                    self.game_over = True
                    return None
                choice_value = str(choice).strip()
                if is_num(choice_value) and int(choice_value) - 21 in targets:
                    return int(choice_value) - 21
                self._log("Недоступная цель, попробуйте снова.")

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

        if fight_report:
            chargers_model = [
                i for i in range(len(self.unit_health))
                if self.unitCharged[i] == 1 and self.unitInAttack[i][0] == 1 and self.unit_health[i] > 0
            ]
            chargers_enemy = [
                i for i in range(len(self.enemy_health))
                if self.enemyCharged[i] == 1 and self.enemyInAttack[i][0] == 1 and self.enemy_health[i] > 0
            ]
            self._log("📌 --- FIGHT PHASE (DEBUG) ---")
            self._log(f"active_side={self._display_side(active_side)}")
            self._log(f"eligible_player={[i + 11 for i in enemy_eligible]}")
            self._log(f"eligible_model={[i + 21 for i in model_eligible]}")
            self._log(f"fights_first_player={[i + 11 for i in chargers_enemy]}")
            self._log(f"fights_first_model={[i + 21 for i in chargers_model]}")
            self._log("computed_first_picker=ACTIVE")
            self._log("reason=чередование начинается с активной стороны")
            self._log("📌 ---------------------------")

        fought_model = set()
        fought_enemy = set()

        # 1) chargers fight first (упрощение: только активная сторона)
        if active_side == "model":
            chargers = [i for i in range(len(self.unit_health))
                        if self.unitCharged[i] == 1 and self.unitInAttack[i][0] == 1 and self.unit_health[i] > 0]
            for i in chargers:
                if i not in fought_model:
                    if fight_report:
                        remaining_model = [idx + 21 for idx in chargers if idx not in fought_model and idx != i]
                        remaining_enemy = [idx + 11 for idx in enemy_eligible if idx not in fought_enemy]
                        self._log(
                            "[FIGHT][ORDER] "
                            f"active_side={self._display_side(active_side)} bucket=first picker=MODEL "
                            f"picked_unit={i + 21} remaining_player={remaining_enemy} "
                            f"remaining_model={remaining_model}"
                        )
                    if _do_melee("model", i):
                        fought_model.add(i)
        else:
            chargers = [i for i in range(len(self.enemy_health))
                        if self.enemyCharged[i] == 1 and self.enemyInAttack[i][0] == 1 and self.enemy_health[i] > 0]
            if manual_enemy:
                remaining = [i for i in chargers if i not in fought_enemy]
                while remaining:
                    attacker_idx = remaining[0]
                    target_idx = _prompt_enemy_target(attacker_idx)
                    if target_idx is None:
                        return
                    self.enemyInAttack[attacker_idx][1] = target_idx
                    if fight_report:
                        remaining_enemy = [idx + 11 for idx in chargers if idx not in fought_enemy and idx != attacker_idx]
                        remaining_model = [idx + 21 for idx in model_eligible if idx not in fought_model]
                        self._log(
                            "[FIGHT][ORDER] "
                            f"active_side={self._display_side(active_side)} bucket=first picker=PLAYER "
                            f"picked_unit={attacker_idx + 11} remaining_player={remaining_enemy} "
                            f"remaining_model={remaining_model}"
                        )
                    if _do_melee("enemy", attacker_idx):
                        fought_enemy.add(attacker_idx)
                    remaining = [i for i in chargers if i not in fought_enemy]
            else:
                for i in chargers:
                    if i not in fought_enemy:
                        if fight_report:
                            remaining_enemy = [idx + 11 for idx in chargers if idx not in fought_enemy and idx != i]
                            remaining_model = [idx + 21 for idx in model_eligible if idx not in fought_model]
                            self._log(
                                "[FIGHT][ORDER] "
                                f"active_side={self._display_side(active_side)} bucket=first picker=PLAYER "
                                f"picked_unit={i + 11} remaining_player={remaining_enemy} "
                                f"remaining_model={remaining_model}"
                            )
                        if _do_melee("enemy", i):
                            fought_enemy.add(i)

        # 2) then alternate, starting with active side (упрощение)
        next_side = active_side

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
                    if fight_report:
                        remaining_enemy = [idx + 11 for idx in enemy_left]
                        remaining_model = [idx + 21 for idx in model_left if idx != i]
                        self._log(
                            "[FIGHT][ORDER] "
                            f"active_side={self._display_side(active_side)} bucket=normal picker=MODEL "
                            f"picked_unit={i + 21} remaining_player={remaining_enemy} "
                            f"remaining_model={remaining_model}"
                        )
                    _do_melee("model", i)
                    fought_model.add(i)
                next_side = "enemy"
            else:
                if enemy_left:
                    if manual_enemy:
                        attacker_idx = enemy_left[0]
                        target_idx = _prompt_enemy_target(attacker_idx)
                        if target_idx is None:
                            return
                        self.enemyInAttack[attacker_idx][1] = target_idx
                        if fight_report:
                            remaining_enemy = [idx + 11 for idx in enemy_left if idx != attacker_idx]
                            remaining_model = [idx + 21 for idx in model_left]
                            self._log(
                                "[FIGHT][ORDER] "
                                f"active_side={self._display_side(active_side)} bucket=normal picker=PLAYER "
                                f"picked_unit={attacker_idx + 11} remaining_player={remaining_enemy} "
                                f"remaining_model={remaining_model}"
                            )
                        _do_melee("enemy", attacker_idx)
                        fought_enemy.add(attacker_idx)
                    else:
                        i = enemy_left[0]
                        if fight_report:
                            remaining_enemy = [idx + 11 for idx in enemy_left if idx != i]
                            remaining_model = [idx + 21 for idx in model_left]
                            self._log(
                                "[FIGHT][ORDER] "
                                f"active_side={self._display_side(active_side)} bucket=normal picker=PLAYER "
                                f"picked_unit={i + 11} remaining_player={remaining_enemy} "
                                f"remaining_model={remaining_model}"
                            )
                        _do_melee("enemy", i)
                        fought_enemy.add(i)
                next_side = "model"

        # после Fight Phase — charged сбрасываем (на всякий)
        self.unitCharged = [0] * len(self.unit_health)
        self.enemyCharged = [0] * len(self.enemy_health)

        if quiet is False:
            self._log("⚔️ Combat resolution complete.\n")



    def step(self, action):
        self._invalidate_target_cache("model_step_start")
        reward = 0
        res = 0
        secondary_interval = max(1, int(os.getenv("REWARD_SECONDARY_INTERVAL", "1")))
        run_secondary_checks = secondary_interval <= 1 or ((self.iter + 1) % secondary_interval == 0)
        model_hp_start = float(sum(self.unit_health))
        enemy_hp_start = float(sum(self.enemy_health))
        enemy_dead_start = sum(1 for hp in self.enemy_health if hp <= 0)
        pre_model_vp = self.modelVP
        pre_enemy_vp = self.enemyVP
        self.refresh_objective_control()
        _, pre_controlled = controlled_objectives(self, "model")
        pre_controlled_set = set(pre_controlled)
        min_obj_dist_start = self._min_model_obj_distance() if run_secondary_checks else None
        start_obj_dists = [
            min(distance(self.unit_coords[idx], obj) for obj in self.coordsOfOM) if len(self.coordsOfOM) > 0 else 0.0
            for idx in range(len(self.unit_health))
        ]
        terrain_snapshot_before = self._terrain_potential_snapshot(start_obj_dists)
        prev_vp_diff = self._prev_vp_diff
        self.unitCharged = [0] * len(self.unit_health)
        self.enemyCharged = [0] * len(self.enemy_health)
        self.active_side = "model"
        battle_shock, delta = self.command_phase("model", action=action)
        reward += delta
        if delta != 0:
            self._log_reward(f"Reward (шаг): командование delta={delta:+.3f}")
        advanced_flags, delta, movement_meta = self.movement_phase("model", action=action, battle_shock=battle_shock)
        self._invalidate_target_cache("model_after_movement")
        reward += delta
        if delta != 0:
            self._log_reward(f"Reward (шаг): движение delta={delta:+.3f}")
        shoot_delta = self.shooting_phase("model", advanced_flags=advanced_flags, action=action) or 0
        reward += shoot_delta
        if shoot_delta != 0:
            self._log_reward(f"Reward (шаг): стрельба delta={shoot_delta:+.3f}")
        charge_delta = self.charge_phase("model", advanced_flags=advanced_flags, action=action) or 0
        reward += charge_delta
        if charge_delta != 0:
            self._log_reward(f"Reward (шаг): чардж delta={charge_delta:+.3f}")
        fight_delta = self.fight_phase("model") or 0
        self._invalidate_target_cache("model_after_fight")
        reward += fight_delta
        if fight_delta != 0:
            self._log_reward(f"Reward (шаг): бой delta={fight_delta:+.3f}")
        game_over, end_reason, winner = apply_end_of_battle(self, log_fn=self._log)
        self.enemyStrat["overwatch"] = -1
        self.enemyStrat["smokescreen"] = -1

        for i in range(len(self.unit_health)):
            if self.unit_health[i] < 0:
                self.unit_health[i] = 0
        for i in range(len(self.enemy_health)):
            if self.enemy_health[i] < 0:
                self.enemy_health[i] = 0

        model_hp_end = float(sum(self.unit_health))
        damage_taken = max(0.0, model_hp_start - model_hp_end)
        if damage_taken > 0:
            damage_taken_norm = damage_taken / max(1.0, float(self.model_hp_max_total))
            penalty = reward_cfg.DAMAGE_TAKEN_SCALE * damage_taken_norm
            reward -= penalty
            self._log_reward(
                "Reward (урон по модели): "
                f"damage_taken={damage_taken:.2f}, norm={damage_taken_norm:.3f}, penalty=-{penalty:.3f}"
            )

        if game_over:
            res = 4
            self.last_end_reason = end_reason
            self.last_winner = winner
            if winner == "model":
                reward += reward_cfg.WIN_BONUS
                self._log_reward(f"Reward (победа): bonus=+{reward_cfg.WIN_BONUS:.3f}")
            elif winner == "enemy":
                reward -= reward_cfg.LOSS_PENALTY
                self._log_reward(f"Reward (поражение): penalty=-{reward_cfg.LOSS_PENALTY:.3f}")

        self.refresh_objective_control()
        _, post_controlled = controlled_objectives(self, "model")
        post_controlled_set = set(post_controlled)
        curr_vp_diff = self.modelVP - self.enemyVP
        vp_delta = curr_vp_diff - prev_vp_diff
        vp_reward = reward_cfg.VP_DIFF_REWARD_SCALE * max(vp_delta, 0)
        vp_penalty = reward_cfg.VP_DIFF_PENALTY_SCALE * max(-vp_delta, 0)
        if vp_reward != 0 or vp_penalty != 0:
            reward += vp_reward - vp_penalty
            self._log_reward(
                "Reward (VP diff): "
                f"prev={prev_vp_diff}, curr={curr_vp_diff}, "
                f"delta={vp_delta}, reward=+{vp_reward:.3f}, penalty=-{vp_penalty:.3f}"
            )
        self._prev_vp_diff = curr_vp_diff

        streak_bonus = 0.0
        streak_len = reward_cfg.VP_OBJECTIVE_STREAK_LEN
        if streak_len > 0:
            for idx in range(len(self._objective_hold_streaks)):
                if idx in post_controlled_set:
                    self._objective_hold_streaks[idx] += 1
                else:
                    self._objective_hold_streaks[idx] = 0
                if self._objective_hold_streaks[idx] >= streak_len:
                    streak_bonus += reward_cfg.VP_OBJECTIVE_STREAK_BONUS
        if streak_bonus != 0:
            reward += streak_bonus
            self._log_reward(
                "Reward (стрик удержания): "
                f"streaks={self._objective_hold_streaks}, "
                f"len={streak_len}, bonus=+{streak_bonus:.3f}"
            )

        enemy_hp_end = float(sum(self.enemy_health))
        enemy_dead_end = sum(1 for hp in self.enemy_health if hp <= 0)
        damage_dealt = max(0.0, enemy_hp_start - enemy_hp_end)
        kills_dealt = max(0, enemy_dead_end - enemy_dead_start)
        vp_changed = (self.modelVP != pre_model_vp) or (self.enemyVP != pre_enemy_vp)
        control_changed = pre_controlled_set != post_controlled_set
        near_objective = self._any_model_near_objective() if run_secondary_checks else False
        min_obj_dist_end = self._min_model_obj_distance() if run_secondary_checks else None
        moved_closer = False
        can_measure_move = min_obj_dist_start is not None and min_obj_dist_end is not None
        if can_measure_move:
            moved_closer = min_obj_dist_end < min_obj_dist_start
        if can_measure_move:
            progress = max(0.0, float(min_obj_dist_start - min_obj_dist_end))
            if progress > 0:
                norm_base = max(1.0, float(getattr(reward_cfg, "VP_OBJECTIVE_MISSED_PROGRESS_NORM", 6.0)))
                progress_norm = progress / norm_base
                progress_scale = float(getattr(reward_cfg, "OBJECTIVE_PROGRESS_STEP_SCALE", 0.03))
                progress_cap = float(getattr(reward_cfg, "OBJECTIVE_PROGRESS_STEP_CAP", 0.10))
                progress_bonus = min(progress_cap, progress_scale * progress_norm)
                if progress_bonus > 0:
                    reward += progress_bonus
                    self._log_reward(
                        "Reward (progress к objective): "
                        f"d_before={min_obj_dist_start:.3f}, d_after={min_obj_dist_end:.3f}, "
                        f"delta={progress:.3f}, norm={progress_norm:.3f}, bonus=+{progress_bonus:.3f}"
                    )
        if run_secondary_checks:
            idle_conditions_met = (
                not near_objective
                and not vp_changed
                and not control_changed
                and damage_dealt <= 0
                and kills_dealt <= 0
                and (not moved_closer or not can_measure_move)
            )
            hold_penalty_applied = bool(movement_meta.get("applied_hold_penalty", False))
            if idle_conditions_met and hold_penalty_applied:
                self._log_reward(
                    "Reward (idle вне цели): "
                    "skip, reason=hold_penalty_already_applied, "
                    f"near_obj={int(near_objective)}, vp_changed={int(vp_changed)}, "
                    f"control_changed={int(control_changed)}, damage={damage_dealt:.2f}, "
                    f"kills={kills_dealt}, moved_closer={int(moved_closer)}, "
                    f"min_dist={min_obj_dist_start}->{min_obj_dist_end}, "
                    f"hold_penalty_events={movement_meta.get('hold_penalty_events', 0)}"
                )
            elif idle_conditions_met:
                reward -= reward_cfg.IDLE_OUT_OF_OBJECTIVE_PENALTY
                self._log_reward(
                    "Reward (idle вне цели): "
                    f"penalty=-{reward_cfg.IDLE_OUT_OF_OBJECTIVE_PENALTY:.3f}, "
                    f"near_obj={int(near_objective)}, vp_changed={int(vp_changed)}, "
                    f"control_changed={int(control_changed)}, damage={damage_dealt:.2f}, "
                    f"kills={kills_dealt}, moved_closer={int(moved_closer)}, "
                    f"min_dist={min_obj_dist_start}->{min_obj_dist_end}"
                )

        terrain_snapshot_after = self._terrain_potential_snapshot(start_obj_dists)
        terrain_gamma = float(getattr(reward_cfg, "TERRAIN_POTENTIAL_GAMMA", 0.99))
        terrain_potential_delta = (terrain_gamma * terrain_snapshot_after["phi"]) - terrain_snapshot_before["phi"]
        terrain_reward_total = terrain_potential_delta
        self._log_reward(
            "Reward (terrain/potential): "
            f"gamma={terrain_gamma:.3f}, phi_before={terrain_snapshot_before['phi']:+.3f}, "
            f"phi_after={terrain_snapshot_after['phi']:+.3f}, delta={terrain_potential_delta:+.3f}; "
            f"cover={terrain_snapshot_before['cover_score']:.3f}->{terrain_snapshot_after['cover_score']:.3f}, "
            f"threat={terrain_snapshot_before['threat_score']:.3f}->{terrain_snapshot_after['threat_score']:.3f}, "
            f"guard={terrain_snapshot_before['guard_score']:.3f}->{terrain_snapshot_after['guard_score']:.3f}"
        )

        exposure_penalty_cfg = float(getattr(reward_cfg, "TERRAIN_EXPOSURE_PENALTY", 0.02))
        if terrain_snapshot_after["threat_count_total"] <= 0:
            self._log_reward("Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).")
        elif terrain_snapshot_after["exposed_units"] <= 0:
            self._log_reward(
                "Reward (terrain/exposure): skip, reason=нет юнитов fully_visible=True под реальной угрозой."
            )
        else:
            alive_units = max(1, sum(1 for hp in self.unit_health if hp > 0))
            exposure_penalty = exposure_penalty_cfg * (terrain_snapshot_after["exposed_units"] / alive_units)
            terrain_reward_total -= exposure_penalty
            self._log_reward(
                "Reward (terrain/exposure): "
                f"penalty=-{exposure_penalty:.3f} (exposed_units={terrain_snapshot_after['exposed_units']}, "
                f"alive_units={alive_units}, threat_count={terrain_snapshot_after['threat_count_total']})"
            )

        terrain_cap = abs(float(getattr(reward_cfg, "TERRAIN_SHAPING_STEP_RCAP", 0.12)))
        terrain_reward_clamped = max(-terrain_cap, min(terrain_cap, terrain_reward_total))
        if abs(terrain_reward_clamped - terrain_reward_total) > 1e-9:
            self._log_reward(
                "Reward (terrain/clamp): "
                f"raw={terrain_reward_total:+.3f}, cap=±{terrain_cap:.3f}, clamped={terrain_reward_clamped:+.3f}"
            )
        else:
            self._log_reward(
                "Reward (terrain/clamp): "
                f"raw={terrain_reward_total:+.3f}, cap=±{terrain_cap:.3f}, clamp не сработал"
            )
        reward += terrain_reward_clamped

        self._advance_turn_order()
        if self.game_over and res == 0:
            res = 4

        self.iter += 1
        if not self.game_over:
            self.last_end_reason = ""
            self.last_winner = None
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
            if float(self.unit_health[i] or 0.0) > 0:
                self.board[self.unit_coords[i][0]][self.unit_coords[i][1]] = 20 + i + 1

        for i in range(len(self.enemy_health)):
            self.enemy_coords[i] = bounds(self.enemy_coords[i], self.b_len, self.b_hei)
            if float(self.enemy_health[i] or 0.0) > 0:
                self.board[self.enemy_coords[i][0]][self.enemy_coords[i][1]] = 10 + i + 1

        for i in range(len(self.coordsOfOM)):
            self.board[int(self.coordsOfOM[i][0])][int(self.coordsOfOM[i][1])] = 3

        self._sync_model_positions_to_anchors()
        # Принудительный flush в узловых точках (конец шага/фазы).
        if not self._flush_state_snapshot(reason="updateBoard", force=True):
            if bool(getattr(self, "playType", False)):
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

    def get_observation_for_side(self, side: str):
        obs = []
        if side == "enemy":
            first_health = self.enemy_health
            first_coords = self.enemy_coords
            first_cp = self.enemyCP
            second_health = self.unit_health
            second_coords = self.unit_coords
            second_cp = self.modelCP
        else:
            first_health = self.unit_health
            first_coords = self.unit_coords
            first_cp = self.modelCP
            second_health = self.enemy_health
            second_coords = self.enemy_coords
            second_cp = self.enemyCP

        for i in range(len(first_health)):
            obs.append(first_health[i])
            obs.append(first_coords[i][0])
            obs.append(first_coords[i][1])

        obs.append(first_cp)

        for i in range(len(second_health)):
            obs.append(second_health[i])
            obs.append(second_coords[i][0])
            obs.append(second_coords[i][1])

        obs.append(second_cp)

        for OM in self.coordsOfOM:
            obs.append(OM[0])
            obs.append(OM[1])

        obs.append(int(self.game_over))

        return np.array(obs, dtype=np.float32)

    def _get_observation(self):
        return self.get_observation_for_side("model")
