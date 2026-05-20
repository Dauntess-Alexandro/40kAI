"""Sprint 5 — picking helpers (`hit_test` module)."""

from __future__ import annotations

import unittest

from PySide6.QtCore import QPointF, QRectF

from app.viewer.rendering.hit_test import (
    HitResult,
    pick_unit_screen,
    pick_unit_world,
    safe_int,
    target_hitbox_for_shoot_info,
)


class _Render:
    __slots__ = ("key", "center", "radius")

    def __init__(self, key, cx: float, cy: float, radius: float) -> None:
        self.key = key
        self.center = QPointF(cx, cy)
        self.radius = radius


class TestHitTest(unittest.TestCase):
    def test_pick_world_prefers_closest(self) -> None:
        renders = [
            _Render(("player", 1), 0.0, 0.0, 5.0),
            _Render(("player", 2), 3.0, 0.0, 5.0),
        ]
        self.assertEqual(pick_unit_world(QPointF(1.0, 0.0), renders), ("player", 1))

    def test_pick_world_miss(self) -> None:
        renders = [_Render(("player", 1), 0.0, 0.0, 1.0)]
        self.assertIsNone(pick_unit_world(QPointF(50.0, 50.0), renders))

    def test_pick_screen_top_paint_order(self) -> None:
        r1 = _Render(("player", 1), 0.0, 0.0, 1.0)
        r2 = _Render(("model", 9), 0.0, 0.0, 1.0)
        rect = QRectF(0.0, 0.0, 100.0, 100.0)
        hitboxes = {r1.key: rect, r2.key: rect}
        pos = QPointF(50.0, 50.0)
        self.assertEqual(pick_unit_screen(pos, hitboxes, [r1, r2]), ("model", 9))

    def test_hit_result_dict(self) -> None:
        self.assertEqual(HitResult.none().as_dict(), {"kind": "none", "side": "", "unitId": -1})
        hr = HitResult(kind="unit", side="player", unit_id=7)
        self.assertEqual(hr.as_dict(), {"kind": "unit", "side": "player", "unitId": 7})

    def test_target_hitbox_prefers_explicit_key(self) -> None:
        rect_a = QRectF(0, 0, 10, 10)
        rect_b = QRectF(50, 50, 10, 10)
        boxes = {("player", 1): rect_a, ("model", 2): rect_b}
        info = {"unit_key": ("player", 1), "unit_id": 999}
        self.assertEqual(target_hitbox_for_shoot_info(info, boxes), rect_a)

    def test_target_hitbox_fallback_by_unit_id(self) -> None:
        rect = QRectF(1, 2, 8, 8)
        boxes = {("player", 5): rect}
        info = {"unit_id": 5}
        self.assertEqual(target_hitbox_for_shoot_info(info, boxes), rect)

    def test_safe_int(self) -> None:
        self.assertEqual(safe_int("42"), 42)
        self.assertIsNone(safe_int(None))
        self.assertIsNone(safe_int("x"))


if __name__ == "__main__":
    unittest.main()
