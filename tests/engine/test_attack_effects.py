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
    assert _normalize_effects(None) == {"cover": False, "reroll_hits": None, "strength_mod": 0, "ap_improve": 0}
    assert _normalize_effects("benefit of cover")["cover"] is True
    d = _normalize_effects({"cover": True, "reroll_hits": "ones", "strength_mod": 1, "ap_improve": 2})
    assert d == {"cover": True, "reroll_hits": "ones", "strength_mod": 1, "ap_improve": 2}
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
