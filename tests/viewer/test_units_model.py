"""ViewerUnitsListModel smoke tests."""

from __future__ import annotations

import unittest

from PySide6.QtWidgets import QApplication

from app.viewer.ui.units_model import ViewerUnitsListModel


class TestViewerUnitsListModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if QApplication.instance() is None:
            cls._app = QApplication([])
        else:
            cls._app = QApplication.instance()

    def test_populate_and_roles(self) -> None:
        model = ViewerUnitsListModel()
        units = [
            {"side": "player", "id": 1, "name": "Warriors", "hp": "8/10", "models": "5"},
            {"side": "model", "id": 2, "name": "Scarabs", "hp": "3/3", "models": "2"},
        ]
        model.populate(
            units,
            player_label="Игрок",
            model_label="ИИ",
            active_side="player",
            active_unit_id=1,
            selected_side=None,
            selected_unit_id=None,
        )
        self.assertEqual(model.rowCount(), 2)
        idx = model.index(0, 0)
        self.assertEqual(model.data(idx, ViewerUnitsListModel.IdRole), 1)
        self.assertTrue(model.data(idx, ViewerUnitsListModel.IsActiveRole))
        row = model.rowAt(0)
        self.assertEqual(row["unitId"], 1)
        self.assertEqual(row["unitName"], "Warriors")
        model.update_selection("player", 1)
        self.assertTrue(model.data(idx, ViewerUnitsListModel.IsSelectedRole))


if __name__ == "__main__":
    unittest.main()
