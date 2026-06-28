"""RCFG_ A/B-override должен достигать активного профиля миссии.

Баг: RCFG_ применялся на import (active=only_war), но annihilation-ран переключает
профиль позже → override не доезжал до annihilation (тихо baseline-vs-baseline).
Фикс: apply_override_all_profiles() кладёт override во ВСЕ профили, где ключ есть.
"""
import importlib

import reward_config as rc


def teardown_function():
    importlib.reload(rc)
    rc.configure_for_mission("only_war")


def test_override_reaches_both_profiles_for_shared_key():
    rc.apply_override_all_profiles("DAMAGE_TAKEN_SCALE", 0.99)
    rc.configure_for_mission("annihilation")
    assert rc.DAMAGE_TAKEN_SCALE == 0.99
    rc.configure_for_mission("only_war")
    assert rc.DAMAGE_TAKEN_SCALE == 0.99


def test_override_skips_profiles_without_key():
    # Ключа нет ни в одном профиле → применилось к нулю профилей (не падаем).
    applied = rc.apply_override_all_profiles("TOTALLY_NONEXISTENT_KEY_XYZ", 0.05)
    assert applied == {}


def test_override_preserves_int_type():
    # int-константа остаётся int (не превращается во float).
    rc.apply_override_all_profiles("VP_OBJECTIVE_STREAK_LEN", 4)
    rc.configure_for_mission("annihilation")
    assert rc.VP_OBJECTIVE_STREAK_LEN == 4
    assert isinstance(rc.VP_OBJECTIVE_STREAK_LEN, int)
