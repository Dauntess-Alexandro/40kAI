import importlib.util
import sys
import types
import unittest
from pathlib import Path


class TestUnitAnchorSync(unittest.TestCase):
    def _load_unit_class(self):
        # РџРѕРґРєР»Р°РґС‹РІР°РµРј С„РµР№РєРѕРІС‹Рµ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё РґР»СЏ unit.py,
        # С‡С‚РѕР±С‹ РЅРµ С‚СЏРЅСѓС‚СЊ РІРµСЃСЊ РїР°РєРµС‚ Рё С‚СЏР¶С‘Р»С‹Рµ РёРјРїРѕСЂС‚С‹.
        game_io = types.ModuleType("core.engine.game_io")
        game_io.get_active_io = lambda: None

        deployment = types.ModuleType("core.engine.deployment")
        deployment.get_random_free_deploy_coord = lambda unitType, b_len, b_hei, occupied: (1, 2)

        sys.modules["core"] = types.ModuleType("core")
        sys.modules["core.engine"] = types.ModuleType("core.engine")
        sys.modules["core.engine.game_io"] = game_io
        sys.modules["core.engine.deployment"] = deployment

        unit_path = Path("core/engine/unit.py")
        spec = importlib.util.spec_from_file_location("unit_under_test", unit_path)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)
        return mod.Unit

    def test_set_anchor_syncs_models(self):
        Unit = self._load_unit_class()
        unit = Unit(data={"Name": "Test", "W": 2, "#OfModels": 3}, weapon={"Range": 24})

        self.assertEqual(3, len(unit.models()))
        unit.set_anchor(7, 9)

        coords = unit.showCoords()
        self.assertEqual(7, int(coords[0]))
        self.assertEqual(9, int(coords[1]))

        for model in unit.models():
            self.assertEqual([7, 9], model["coords"][:2])


if __name__ == "__main__":
    unittest.main()

