from core.engine.utils import _normalize_effects, attack


class StubRoller:
    """Детерминированный roller: очереди по стадиям hit/wound/save (+damage=None)."""

    def __init__(self, hit=None, wound=None, save=None, damage=None, default=6):
        self.q = {
            "hit": list(hit or []),
            "wound": list(wound or []),
            "save": list(save or []),
            None: list(damage or []),
        }
        self.default = default

    def __call__(self, num=1, max=6, stage=None):
        q = self.q.get(stage, [])
        out = [int(q.pop(0)) if q else int(self.default) for _ in range(num)]
        return out if num != 1 else out[0]


_ATT_DATA = {"#OfModels": 1, "W": 1}


def _ranged_weapon(**over):
    w = {"BS": 4, "S": 4, "AP": 0, "Damage": 1, "Attacks": 1, "Range": 24}
    w.update(over)
    return w


def test_normalize_effects_variants():
    assert _normalize_effects(None) == {
        "cover": False,
        "reroll_hits": None,
        "reroll_wounds": None,
        "reroll_save": None,
        "strength_mod": 0,
        "ap_improve": 0,
        "hit_penalty": 0,
        "invuln_grant": 0,
    }
    assert _normalize_effects("benefit of cover")["cover"] is True
    d = _normalize_effects({"cover": True, "reroll_hits": "ones", "strength_mod": 1, "ap_improve": 2})
    assert d == {
        "cover": True,
        "reroll_hits": "ones",
        "reroll_wounds": None,
        "reroll_save": None,
        "strength_mod": 1,
        "ap_improve": 2,
        "hit_penalty": 0,
        "invuln_grant": 0,
    }
    # неизвестный reroll → None
    assert _normalize_effects({"reroll_hits": "weird"})["reroll_hits"] is None


def test_cover_back_compat_reduces_damage():
    # Sv6, AP0 → save 6+. cover → 5+. save-бросок [5]: без cover не сейвит (урон 1), с cover сейвит (урон 0).
    weapon = _ranged_weapon()
    defender = {"Sv": 6, "T": 4, "IVSave": 0}
    no_cover, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                         roller=StubRoller(hit=[5], wound=[6], save=[5]))
    with_cover, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects="benefit of cover",
                          roller=StubRoller(hit=[5], wound=[6], save=[5]))
    assert float(sum(no_cover)) == 1.0
    assert float(sum(with_cover)) == 0.0


def test_cover_dict_equivalent_to_string():
    weapon = _ranged_weapon()
    defender = {"Sv": 6, "T": 4, "IVSave": 0}
    via_dict, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"cover": True},
                        roller=StubRoller(hit=[5], wound=[6], save=[5]))
    assert float(sum(via_dict)) == 0.0


def test_strength_mod_changes_wound_threshold():
    # S4 vs T4 → 4+; S5 vs T4 → 3+. wound-бросок [3]: без +S не ранит, с +1 S ранит.
    weapon = _ranged_weapon(S=4)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}  # Sv7 → засейвить нельзя
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[5], wound=[3]))
    boosted, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"strength_mod": 1},
                        roller=StubRoller(hit=[5], wound=[3]))
    assert float(sum(base)) == 0.0
    assert float(sum(boosted)) == 1.0


def test_ap_improve_worsens_save():
    # Sv4 AP0 → 4+; ap_improve=1 → AP-1 → 5+. save-бросок [4]: без эффекта сейвит, с эффектом нет.
    weapon = _ranged_weapon(S=4, AP=0)
    defender = {"Sv": 4, "T": 4, "IVSave": 0}
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[5], wound=[6], save=[4]))
    improved, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"ap_improve": 1},
                         roller=StubRoller(hit=[5], wound=[6], save=[4]))
    assert float(sum(base)) == 0.0
    assert float(sum(improved)) == 1.0


def test_reroll_hits_ones():
    # bs4. hit [1]: без ре-ролла промах → урон 0; reroll_hits="ones" [1]→ре-ролл [5] хит → урон 1.
    weapon = _ranged_weapon(S=4)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}  # засейвить нельзя
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[1], wound=[6]))
    rer, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"reroll_hits": "ones"},
                    roller=StubRoller(hit=[1, 5], wound=[6]))
    assert float(sum(base)) == 0.0
    assert float(sum(rer)) == 1.0


def test_reroll_hits_all_rerolls_misses():
    # bs4. hit [2] промах (не 1, но < bs) → reroll_hits="all" ре-роллит [5] → хит.
    weapon = _ranged_weapon(S=4)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[2], wound=[6]))
    rer, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"reroll_hits": "all"},
                    roller=StubRoller(hit=[2, 5], wound=[6]))
    assert float(sum(base)) == 0.0
    assert float(sum(rer)) == 1.0


def test_reroll_wounds_ones():
    # S4 vs T4 → wound 4+. hit [5] (хит), wound [1] (провал-единица) → урон 0;
    # reroll_wounds="ones" [1]→ре-ролл [6] (ранит) → урон 1.
    weapon = _ranged_weapon(S=4)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[5], wound=[1]))
    rer, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"reroll_wounds": "ones"},
                    roller=StubRoller(hit=[5], wound=[1, 6]))
    assert float(sum(base)) == 0.0
    assert float(sum(rer)) == 1.0


def test_reroll_wounds_all_rerolls_failures():
    # S4 vs T4 → wound 4+. hit [5], wound [3] (провал) → урон 0;
    # reroll_wounds="all" [3]→ре-ролл [5] (ранит) → урон 1.
    weapon = _ranged_weapon(S=4)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[5], wound=[3]))
    rer, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"reroll_wounds": "all"},
                    roller=StubRoller(hit=[5], wound=[3, 5]))
    assert float(sum(base)) == 0.0
    assert float(sum(rer)) == 1.0


def test_worst_failed_index_picks_lowest_failure():
    import numpy as np

    from core.engine.utils import _worst_failed_index

    assert _worst_failed_index(np.array([3, 5, 2, 6]), 4) == 2
    assert _worst_failed_index(np.array([4, 5, 6]), 4) is None


def test_reroll_wounds_one_rerolls_worst_failure():
    weapon = _ranged_weapon(S=4, Attacks=2)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    one, _ = attack(
        1,
        weapon,
        _ATT_DATA,
        10,
        defender,
        effects={"reroll_wounds": "one"},
        roller=StubRoller(hit=[5, 5], wound=[2, 3, 6]),
    )
    assert float(sum(one)) == 1.0


def test_reroll_save_all_saves_failed_save():
    # Sv4. hit [5], wound [6] (ранит), save [3] (провал, нужно 4+) → урон 1;
    # reroll_save="all" [3]→ре-ролл [5] (сейв) → урон 0.
    weapon = _ranged_weapon(S=4)
    defender = {"Sv": 4, "T": 4, "IVSave": 0}
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[5], wound=[6], save=[3]))
    sav, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"reroll_save": "all"},
                    roller=StubRoller(hit=[5], wound=[6], save=[3, 5]))
    assert float(sum(base)) == 1.0
    assert float(sum(sav)) == 0.0


def test_normalize_effects_reroll_wounds_save():
    assert _normalize_effects({"reroll_wounds": "all"})["reroll_wounds"] == "all"
    assert _normalize_effects({"reroll_save": "ones"})["reroll_save"] == "ones"
    assert _normalize_effects({})["reroll_wounds"] is None
    assert _normalize_effects({})["reroll_save"] is None
    assert _normalize_effects({"reroll_wounds": "weird"})["reroll_wounds"] is None


def test_reroll_wounds_one_rerolls_single_failure():
    # S4 vs T4 → wound 4+. Два хита, оба провал [3,3]; "one" рероллит только первый → [5,_].
    weapon = _ranged_weapon(S=4, Attacks=2)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    one, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"reroll_wounds": "one"},
                    roller=StubRoller(hit=[5, 5], wound=[3, 3, 5]))
    assert float(sum(one)) == 1.0  # только один реролл стал успешным


def test_normalize_effects_reroll_one_allowed():
    assert _normalize_effects({"reroll_wounds": "one"})["reroll_wounds"] == "one"


def test_hit_penalty_stealth_reduces_hits():
    # bs4. hit [4]: без штрафа хит (4>=4) → урон; hit_penalty=1 → нужно 5+ → [4] промах.
    weapon = _ranged_weapon(S=4)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[4], wound=[6]))
    stealth, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"hit_penalty": 1},
                        roller=StubRoller(hit=[4], wound=[6]))
    assert float(sum(base)) == 1.0
    assert float(sum(stealth)) == 0.0


def test_hit_penalty_natural_six_still_hits():
    # hit [6] всегда попадает даже со штрафом.
    weapon = _ranged_weapon(S=4)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    stealth, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"hit_penalty": 3},
                        roller=StubRoller(hit=[6], wound=[6]))
    assert float(sum(stealth)) == 1.0


def test_invuln_grant_saves_against_ap():
    # Sv4 против AP-3 → 7+ (нельзя). invuln_grant=6 → 6+. save [6]: без грант урон 1, с грантом 0.
    weapon = _ranged_weapon(S=4, AP=-3)
    defender = {"Sv": 4, "T": 4, "IVSave": 0}
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[5], wound=[6], save=[6]))
    grant, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"invuln_grant": 6},
                      roller=StubRoller(hit=[5], wound=[6], save=[6]))
    assert float(sum(base)) == 1.0
    assert float(sum(grant)) == 0.0
