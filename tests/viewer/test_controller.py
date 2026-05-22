"""Sprint 3 — ViewerController + status label parity tests."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.viewer.controller.viewer_controller import (
    ViewerController,
    ViewerPresentationContext,
    compute_status_labels,
)

_FIXTURES = Path(__file__).resolve().parent / "fixtures"


class TestViewerController(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Use QApplication so sibling tests (e.g. QPainter on QImage) share a GUI app.
        if QApplication.instance() is None:
            cls._app = QApplication([])
        else:
            cls._app = QApplication.instance()

    def _ctx(self) -> ViewerPresentationContext:
        return ViewerPresentationContext(
            player_role_label="Игрок",
            model_role_label="ИИ",
            rolloff_attacker_side="model",
            rolloff_defender_side="enemy",
            deploy_status_suffix="",
        )

    def test_compute_matches_fixture_state(self) -> None:
        raw = json.loads((_FIXTURES / "state_fixture_movement.json").read_text(encoding="utf-8"))
        ctx = self._ctx()
        labels = compute_status_labels(raw, ctx)
        self.assertEqual(labels.round_text, "Раунд: 2")
        self.assertEqual(labels.turn_text, "Ход: 3")
        self.assertIn("movement", labels.phase_text.lower())
        self.assertEqual(labels.vp_player_text, "Player VP: 5")

    def test_controller_apply_emits_state_updated(self) -> None:
        ctrl = ViewerController()
        hits = []

        def _rec():
            hits.append(1)

        ctrl.stateUpdated.connect(_rec)
        raw = json.loads((_FIXTURES / "state_fixture_movement.json").read_text(encoding="utf-8"))
        labels = compute_status_labels(raw, self._ctx())
        ctrl.apply_labels(labels, phase_raw="movement", active_side_raw="player")
        self.assertEqual(sum(hits), 1)
        self.assertEqual(ctrl.phaseRaw, "movement")
        self.assertEqual(ctrl.activePlayer, 0)

    def test_push_selection_emits_unit_selected(self) -> None:
        ctrl = ViewerController()
        got = []
        ctrl.unitSelected.connect(lambda i: got.append(i))
        ctrl.push_selection("player", 7)
        self.assertEqual(got, [7])
        self.assertEqual(ctrl.selectedUnitId, 7)
        self.assertEqual(ctrl.selectedUnitSide, "player")

    def test_command_kind_defaults(self) -> None:
        ctrl = ViewerController()
        self.assertEqual(ctrl.commandKind, "idle")
        ctrl.set_command_kind("move")
        self.assertEqual(ctrl.commandKind, "move")

    def test_map_overlay_legend_movement(self) -> None:
        ctrl = ViewerController()
        ctrl.set_map_overlay_legend(
            [
                {"key": "move", "color": "#4882ff", "label": 'Move 6"'},
                {"key": "advance", "color": "#ecc240", "label": "Advance +D6"},
            ]
        )
        self.assertEqual(len(ctrl.mapOverlayLegend), 2)
        self.assertEqual(ctrl.mapOverlayLegend[0]["key"], "move")

    def test_right_panel_tab_clamped(self) -> None:
        ctrl = ViewerController()
        ctrl.setRightPanelTab(5)
        self.assertEqual(ctrl.rightPanelTab, 1)
        ctrl.setRightPanelTab(-1)
        self.assertEqual(ctrl.rightPanelTab, 0)

    def test_selection_source_label(self) -> None:
        ctrl = ViewerController()
        ctrl.set_selection_source("map")
        self.assertEqual(ctrl.selectionSource, "карта")
        ctrl.set_selection_source("list")
        self.assertEqual(ctrl.selectionSource, "список")

    def test_push_selection_no_recursion_smoke(self) -> None:
        ctrl = ViewerController()
        for i in range(20):
            ctrl.push_selection("player", i % 5)
        self.assertEqual(ctrl.selectedUnitId, 4)

    def test_select_unit_calls_window_resolver(self) -> None:
        ctrl = ViewerController()
        calls = []

        class DummyWin:
            def _controller_resolve_select_unit(self, uid):
                calls.append(uid)

        ctrl.attach_window(DummyWin())
        ctrl.selectUnit(101)
        self.assertEqual(calls, [101])

    def test_hit_test_board_delegates_to_map_scene(self) -> None:
        from PySide6.QtCore import QPointF

        from app.viewer.rendering.hit_test import HitResult

        class DummyBoard:
            def hit_test_screen(self, pos: QPointF) -> HitResult:
                self.last_pos = pos
                return HitResult(kind="unit", side="player", unit_id=99)

        class DummyWin:
            def __init__(self) -> None:
                self.map_scene = DummyBoard()

        ctrl = ViewerController()
        win = DummyWin()
        ctrl.attach_window(win)
        d = ctrl.hitTestBoard(12.5, 88.0)
        self.assertEqual(d["kind"], "unit")
        self.assertEqual(d["side"], "player")
        self.assertEqual(d["unitId"], 99)
        self.assertAlmostEqual(win.map_scene.last_pos.x(), 12.5)
        self.assertAlmostEqual(win.map_scene.last_pos.y(), 88.0)


if __name__ == "__main__":
    unittest.main()
