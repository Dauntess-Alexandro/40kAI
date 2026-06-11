# tests/engine/test_expected_damage.py
import unittest

from core.engine.utils import expected_damage


class TestExpectedDamage(unittest.TestCase):
    def test_basic_no_specials(self):
        # 1 модель, 2 атаки, BS3 (p_hit=4/6), S4 vs T4 (wt=4, p_wound=3/6),
        # Sv4 без AP (save_target=4, p_unsaved=3/6), Damage=1, без lethal/rapid.
        weapon = {"Attacks": 2, "BS": 3, "S": 4, "AP": 0, "Damage": 1, "Range": 24}
        adata = {"#OfModels": 1, "W": 2}
        ddata = {"Sv": 4, "T": 4, "IVSave": 0}
        ev = expected_damage(2, weapon, adata, ddata, rangeOfComb="Ranged", distance_to_target=20)
        # 2 * (4/6) * (3/6) * (3/6) * 1 = 0.33333...
        self.assertAlmostEqual(ev, 2 * (4 / 6) * 0.5 * 0.5 * 1.0, places=6)

    def test_lethal_hits_increase_ev(self):
        base = {"Attacks": 6, "BS": 3, "S": 4, "AP": 0, "Damage": 1, "Range": 24}
        adata = {"#OfModels": 1, "W": 6}
        ddata = {"Sv": 4, "T": 4, "IVSave": 0}
        ev_plain = expected_damage(6, base, adata, ddata, distance_to_target=20)
        lethal = dict(base, Abilities={"LethalHits": True})
        ev_lethal = expected_damage(6, lethal, adata, ddata, distance_to_target=20)
        self.assertGreater(ev_lethal, ev_plain)

    def test_rapid_fire_within_half_range_adds_attacks(self):
        rf = {"Attacks": 1, "BS": 3, "S": 4, "AP": 0, "Damage": 1, "Range": 24,
              "Abilities": {"RapidFire": 1}}
        adata = {"#OfModels": 1, "W": 2}
        ddata = {"Sv": 4, "T": 4, "IVSave": 0}
        ev_far = expected_damage(2, rf, adata, ddata, distance_to_target=20)   # >12 => нет RF
        ev_close = expected_damage(2, rf, adata, ddata, distance_to_target=10)  # <=12 => +1 атака
        self.assertGreater(ev_close, ev_far)

    def test_ap_reduces_save_increases_ev(self):
        w0 = {"Attacks": 4, "BS": 3, "S": 4, "AP": 0, "Damage": 1, "Range": 24}
        w2 = dict(w0, AP=-2)
        adata = {"#OfModels": 1, "W": 4}
        ddata = {"Sv": 3, "T": 4, "IVSave": 0}
        self.assertGreater(
            expected_damage(4, w2, adata, ddata, distance_to_target=20),
            expected_damage(4, w0, adata, ddata, distance_to_target=20),
        )

    def test_models_scale_attacks(self):
        w = {"Attacks": 2, "BS": 3, "S": 4, "AP": 0, "Damage": 1, "Range": 24}
        ddata = {"Sv": 4, "T": 4, "IVSave": 0}
        ev1 = expected_damage(2, w, {"#OfModels": 1, "W": 2}, ddata, distance_to_target=20)
        ev5 = expected_damage(10, w, {"#OfModels": 5, "W": 2}, ddata, distance_to_target=20)
        self.assertAlmostEqual(ev5, ev1 * 5, places=6)


if __name__ == "__main__":
    unittest.main()
