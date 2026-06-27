"""Task 7 — Qt GUI: миссия annihilation в опциях и динамический мета-текст QML.

Source-level asserts (без полного GUI init): проверяем, что controller знает
`annihilation`, а QML показывает корректный мета-текст в зависимости от
`controller.selectedMission`.
"""

from __future__ import annotations

import unittest
from pathlib import Path


class TestMissionOptionsSource(unittest.TestCase):
    def test_controller_exposes_annihilation_option(self) -> None:
        source = Path("app/gui_qt/main.py").read_text(encoding="utf-8")
        # Опции миссий должны включать annihilation рядом с only_war.
        self.assertIn('_mission_options = ["only_war", "annihilation"]', source)

    def test_qml_has_annihilation_dynamic_meta(self) -> None:
        source = Path("app/gui_qt/qml/Main.qml").read_text(encoding="utf-8")
        # QML должен ветвить мета-текст по выбранной миссии.
        self.assertIn('controller.selectedMission === "annihilation"', source)
        # Режим: Annihilation / Kill Points.
        self.assertIn("ANNIHILATION / KILL POINTS", source)
        # Точка: точек нет (Kill Points).
        self.assertIn("точек нет", source)
        # Примечание: победа по уничтоженным юнитам врага.
        self.assertIn("победа по уничтоженным юнитам врага", source)


if __name__ == "__main__":
    unittest.main()
