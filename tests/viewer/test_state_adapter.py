"""Tests for viewer migration Sprint 1 — ``state_adapter``."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from app.viewer.controller.state_adapter import (
    StateAdapterError,
    adapt_snapshot,
    adapt_snapshot_from_file,
)

_FIXTURES = Path(__file__).resolve().parent / "fixtures"


class TestStateAdapter(unittest.TestCase):
    def _load(self, name: str) -> dict:
        path = _FIXTURES / name
        return json.loads(path.read_text(encoding="utf-8"))

    def test_empty_merged_matches_default_board(self) -> None:
        snap = adapt_snapshot(self._load("state_fixture_empty.json"), merge_defaults=True)
        self.assertEqual(snap.board_width, 60)
        self.assertEqual(snap.board_height, 40)
        self.assertEqual(snap.protocol_version, "0.0")
        self.assertFalse(snap.degraded)

    def test_movement_fixture_board_and_units(self) -> None:
        snap = adapt_snapshot(self._load("state_fixture_movement.json"), merge_defaults=True)
        self.assertEqual(snap.board_width, 30)
        self.assertEqual(snap.board_height, 20)
        self.assertEqual(snap.phase, "movement")
        self.assertEqual(snap.active_side, "player")
        self.assertEqual(snap.protocol_version, "0.9-preview")
        self.assertEqual(len(snap.units), 1)
        u = snap.units[0]
        self.assertEqual(u.id, 101)
        self.assertEqual(u.side, "player")
        self.assertEqual(u.x, 10)
        self.assertEqual(u.y, 12)
        self.assertAlmostEqual(float(u.hp or 0), 8.5)
        self.assertEqual(len(snap.objectives), 1)
        self.assertEqual(snap.objectives[0].id, 1)

    def test_deploy_phase_preserves_deployment_block(self) -> None:
        snap = adapt_snapshot(self._load("state_fixture_deploy.json"), merge_defaults=True)
        self.assertEqual(snap.phase, "deployment")
        self.assertEqual(snap.deployment.get("attacker"), "model")
        self.assertEqual(snap.deployment.get("defender"), "player")

    def test_movement_overlay_preserved(self) -> None:
        snap = adapt_snapshot(self._load("state_fixture_overlay.json"), merge_defaults=True)
        self.assertIsInstance(snap.movement_overlay, dict)
        assert isinstance(snap.movement_overlay, dict)
        self.assertEqual(snap.movement_overlay.get("unit_id"), 11)

    def test_model_events_and_log_tail_order(self) -> None:
        snap = adapt_snapshot(self._load("state_fixture_events_order.json"), merge_defaults=True)
        self.assertEqual(len(snap.model_events), 3)
        seqs = [e.get("seq") for e in snap.model_events if isinstance(e, dict)]
        self.assertEqual(seqs, [1, 2, 3])
        self.assertEqual(list(snap.log_tail), ["alpha", "beta", "gamma"])

    def test_bad_viewer_block_marks_degraded(self) -> None:
        snap = adapt_snapshot(self._load("state_fixture_bad_viewer.json"), merge_defaults=True)
        self.assertTrue(snap.degraded)
        self.assertEqual(snap.viewer_block, {})

    def test_invalid_root_raises(self) -> None:
        with self.assertRaises(StateAdapterError):
            adapt_snapshot([], merge_defaults=False)  # type: ignore[arg-type]

    def test_adapt_snapshot_from_file_load_merge(self) -> None:
        payload = self._load("state_fixture_movement.json")
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".json",
            delete=False,
        ) as tmp:
            json.dump(payload, tmp)
            path = Path(tmp.name)
        try:
            snap = adapt_snapshot_from_file(path)
            self.assertEqual(snap.board_width, 30)
            self.assertEqual(snap.units[0].id, 101)
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
