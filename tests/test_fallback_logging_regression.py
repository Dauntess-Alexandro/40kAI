import unittest
from pathlib import Path


class TestFallbackLoggingRegression(unittest.TestCase):
    def test_model_fallback_does_not_log_stay_in_melee(self):
        """Регрессия: после Fall Back не должно быть ложного лога "Остаётся в ближнем бою"."""
        source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")

        anchor = 'elif self.unitInAttack[i][0] == 1 and self.unit_health[i] > 0:'
        self.assertIn(anchor, source, "Не найден блок movement_phase для model melee-ветки")

        start = source.index(anchor)
        tail_anchor = 'if objective_hold_delta != 0 or objective_proximity_delta != 0:'
        self.assertIn(tail_anchor, source[start:], "Не найден конец model movement-блока")
        end = source.index(tail_anchor, start)
        block = source[start:end]

        self.assertIn('retreated = False', block)
        self.assertIn('retreated = True', block)
        self.assertIn('if not retreated:', block)
        self.assertIn('Остаётся в ближнем бою', block)

        # Санити: лог "остается" должен быть условным (после if not retreated)
        guard_pos = block.index('if not retreated:')
        stay_pos = block.index('Остаётся в ближнем бою')
        self.assertGreater(stay_pos, guard_pos, "Лог 'Остаётся в ближнем бою' должен быть под if not retreated")


if __name__ == '__main__':
    unittest.main()
