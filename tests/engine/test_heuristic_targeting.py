# tests/engine/test_heuristic_targeting.py
import unittest

from core.engine.heuristic_targeting import allocate_shots


class TestAllocateShots(unittest.TestCase):
    def test_focus_fire_finishes_one_target(self):
        # Два стрелка по 5 EV; Ta(hp6), Tb(hp12). Оба бьют Ta, чтобы снять юнит.
        shooters = [1, 2]
        ev = {1: {10: 5.0, 20: 5.0}, 2: {10: 5.0, 20: 5.0}}
        targets = {10: (6.0, 6.0), 20: (12.0, 12.0)}
        result = allocate_shots(shooters, ev, targets)
        self.assertEqual(result[1], 10)
        self.assertEqual(result[2], 10)

    def test_avoid_overkill_on_already_dead_projection(self):
        # S1 (10 EV) сносит Ta(6). S2 не добивает труп, а бьёт Tb.
        shooters = [1, 2]
        ev = {1: {10: 10.0}, 2: {10: 10.0, 20: 3.0}}
        targets = {10: (6.0, 6.0), 20: (9.0, 9.0)}
        result = allocate_shots(shooters, ev, targets)
        self.assertEqual(result[1], 10)
        self.assertEqual(result[2], 20)

    def test_objective_bonus_breaks_ties_toward_objective_target(self):
        shooters = [1]
        ev = {1: {10: 4.0, 20: 4.0}}
        targets = {10: (10.0, 10.0), 20: (10.0, 10.0)}
        result = allocate_shots(shooters, ev, targets, obj_bonus={20: 1.0})
        self.assertEqual(result[1], 20)

    def test_assigns_every_shooter(self):
        shooters = [1, 2, 3]
        ev = {1: {10: 2.0}, 2: {20: 2.0}, 3: {10: 1.0, 20: 1.0}}
        targets = {10: (5.0, 5.0), 20: (5.0, 5.0)}
        result = allocate_shots(shooters, ev, targets)
        self.assertEqual(set(result.keys()), {1, 2, 3})
        for s in (1, 2, 3):
            self.assertIn(result[s], (10, 20))


if __name__ == "__main__":
    unittest.main()
