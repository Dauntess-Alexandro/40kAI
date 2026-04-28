import unittest
from pathlib import Path


class TestFallbackLoggingRegression(unittest.TestCase):
    def test_model_fallback_does_not_log_stay_in_melee(self):
        """Р РµРіСЂРµСЃСЃРёСЏ: РїРѕСЃР»Рµ Fall Back РЅРµ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ Р»РѕР¶РЅРѕРіРѕ Р»РѕРіР° "РћСЃС‚Р°С‘С‚СЃСЏ РІ Р±Р»РёР¶РЅРµРј Р±РѕСЋ"."""
        source = Path("core/envs/warhamEnv.py").read_text(encoding="utf-8")

        anchor = 'elif self.unitInAttack[i][0] == 1 and self.unit_health[i] > 0:'
        self.assertIn(anchor, source, "РќРµ РЅР°Р№РґРµРЅ Р±Р»РѕРє movement_phase РґР»СЏ model melee-РІРµС‚РєРё")

        start = source.index(anchor)
        tail_anchor = 'if objective_hold_delta != 0 or objective_proximity_delta != 0:'
        self.assertIn(tail_anchor, source[start:], "РќРµ РЅР°Р№РґРµРЅ РєРѕРЅРµС† model movement-Р±Р»РѕРєР°")
        end = source.index(tail_anchor, start)
        block = source[start:end]

        self.assertIn('retreated = False', block)
        self.assertIn('retreated = True', block)
        self.assertIn('if not retreated:', block)
        self.assertIn('РћСЃС‚Р°С‘С‚СЃСЏ РІ Р±Р»РёР¶РЅРµРј Р±РѕСЋ', block)

        # РЎР°РЅРёС‚Рё: Р»РѕРі "РѕСЃС‚Р°РµС‚СЃСЏ" РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ СѓСЃР»РѕРІРЅС‹Рј (РїРѕСЃР»Рµ if not retreated)
        guard_pos = block.index('if not retreated:')
        stay_pos = block.index('РћСЃС‚Р°С‘С‚СЃСЏ РІ Р±Р»РёР¶РЅРµРј Р±РѕСЋ')
        self.assertGreater(stay_pos, guard_pos, "Р›РѕРі 'РћСЃС‚Р°С‘С‚СЃСЏ РІ Р±Р»РёР¶РЅРµРј Р±РѕСЋ' РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ РїРѕРґ if not retreated")


if __name__ == '__main__':
    unittest.main()

