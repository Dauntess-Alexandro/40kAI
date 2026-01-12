#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch warhamEnv.py to safely resolve string weapons like "Bolt pistol [PISTOL]"
before calling engine.utils.attack().

Usage (from repo root):
  python3 apply_weapon_fix.py
or
  python3 apply_weapon_fix.py path/to/warhamEnv.py
"""

from __future__ import annotations
import sys
from pathlib import Path

DEFAULT_PATHS = [
    Path("gym_mod/gym_mod/envs/warhamEnv.py"),
    Path("gym_mod/envs/warhamEnv.py"),
    Path("warhamEnv.py"),
]

MARKER = "# 🔧 FIX: resolve string weapons like"

PATCH_BLOCK = '# ============================================================\n# 🔧 FIX: resolve string weapons like "Bolt pistol [PISTOL]"\n# so engine.utils.attack() always receives a dict (or we safely\n# skip the attack instead of crashing with "\'str\' object has no attribute \'get\'").\n# This is intentionally defensive: if WeaponData can\'t be found,\n# we still won\'t crash during training.\n# ============================================================\n\n_attack_original = attack  # keep reference to the original engine attack\n_WEAPON_INDEX = None\n\ndef _norm_weapon_name(x):\n    if not isinstance(x, str):\n        return x\n    # remove tags in square brackets: "Bolt pistol [PISTOL]" -> "Bolt pistol"\n    x = re.sub(r"\\s*\\[.*?\\]\\s*", "", x)\n    return x.strip().lower()\n\ndef _build_weapon_index():\n    """\n    Try to locate WeaponData list from a few common places.\n    Returns dict: normalized_name -> weapon_dict\n    """\n    weapon_list = None\n\n    # 1) engine_utils.weaponData / engine_utils.WeaponData\n    for attr in ("weaponData", "WeaponData"):\n        v = getattr(engine_utils, attr, None)\n        if isinstance(v, list):\n            weapon_list = v\n            break\n        if isinstance(v, dict) and "WeaponData" in v and isinstance(v["WeaponData"], list):\n            weapon_list = v["WeaponData"]\n            break\n\n    # 2) engine_utils.data["WeaponData"]\n    if weapon_list is None:\n        v = getattr(engine_utils, "data", None)\n        if isinstance(v, dict) and isinstance(v.get("WeaponData"), list):\n            weapon_list = v.get("WeaponData")\n\n    # 3) If something named WeaponData got imported via wildcard\n    if weapon_list is None:\n        v = globals().get("WeaponData")\n        if isinstance(v, list):\n            weapon_list = v\n\n    idx = {}\n    if weapon_list:\n        for w in weapon_list:\n            if isinstance(w, dict) and "Name" in w:\n                idx[_norm_weapon_name(w["Name"])] = w\n    return idx\n\ndef attack(attackerHealth, attackerWeapon, attacker_data, defenderHealth, defender_data, *args, **kwargs):\n    """\n    Wrapper over engine.utils.attack:\n    - if attackerWeapon is a string, try to resolve it into a dict from WeaponData\n    - if can\'t resolve, return zero damage and unchanged defender health (no crash)\n    """\n    global _WEAPON_INDEX\n    if isinstance(attackerWeapon, str):\n        if _WEAPON_INDEX is None:\n            _WEAPON_INDEX = _build_weapon_index()\n        attackerWeapon = _WEAPON_INDEX.get(_norm_weapon_name(attackerWeapon))\n\n    if attackerWeapon is None or not isinstance(attackerWeapon, dict):\n        # can\'t resolve weapon => skip attack safely\n        return [], defenderHealth\n\n    return _attack_original(attackerHealth, attackerWeapon, attacker_data, defenderHealth, defender_data, *args, **kwargs)\n'


def find_target(path_arg: str | None) -> Path:
    if path_arg:
        p = Path(path_arg)
        if not p.exists():
            raise FileNotFoundError(f"File not found: {p}")
        return p

    for p in DEFAULT_PATHS:
        if p.exists():
            return p

    raise FileNotFoundError(
        "Couldn't find warhamEnv.py автоматически. Передай путь явным аргументом:\n"
        "  python3 apply_weapon_fix.py path/to/warhamEnv.py"
    )


def main() -> int:
    try:
        target = find_target(sys.argv[1] if len(sys.argv) > 1 else None)
    except Exception as e:
        print(f"❌ {e}")
        return 1

    txt = target.read_text(encoding="utf-8", errors="replace")

    if MARKER in txt:
        print(f"✅ Уже пропатчено: {target}")
        return 0

    # Insert right after the GUIinteract import if present, otherwise after engine_utils import, otherwise after last import.
    insert_after_candidates = [
        "from gym_mod.engine.GUIinteract import *",
        "from ..engine import utils as engine_utils",
        "from ..engine.utils import *",
    ]

    lines = txt.splitlines(True)
    insert_idx = None

    for needle in insert_after_candidates:
        for i, line in enumerate(lines):
            if needle in line:
                insert_idx = i + 1
                break
        if insert_idx is not None:
            break

    if insert_idx is None:
        # fallback: after the last "import ..." line
        for i, line in enumerate(lines):
            if line.lstrip().startswith("import ") or line.lstrip().startswith("from "):
                insert_idx = i + 1
        if insert_idx is None:
            insert_idx = 0

    lines.insert(insert_idx, "\n" + PATCH_BLOCK + "\n")
    target.write_text("".join(lines), encoding="utf-8")

    print(f"✅ Готово! Вставил фикс в: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
