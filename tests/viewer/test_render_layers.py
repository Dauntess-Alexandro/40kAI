"""Sprint 4 — modular render layers (smoke: stub widget + QPainter on QImage)."""

from __future__ import annotations

import unittest
from types import SimpleNamespace

from PySide6 import QtCore, QtGui, QtWidgets

from app.viewer.config import load_viewer_config
from app.viewer.rendering.layer_context import LayerContext
from app.viewer.rendering.layers.ground import paint_ground_layer
from app.viewer.rendering.layers.grid import paint_grid_layer
from app.viewer.rendering.layers.labels import paint_labels_layer
from app.viewer.rendering.layers.objectives import paint_objectives_layer
from app.viewer.styles import Theme


class _StubBoard:
    """Minimal surface matching attributes/methods used by Sprint 4 layers."""

    def __init__(self) -> None:
        self._board_rect = QtCore.QRectF(0.0, 0.0, 480.0, 360.0)
        self._scale = 1.0
        self._pan = QtCore.QPointF(0.0, 0.0)
        self.cell_size = 32
        self._board_width = 15
        self._board_height = 12
        self._w = 640
        self._h = 480

    def width(self) -> int:
        return self._w

    def height(self) -> int:
        return self._h

    def devicePixelRatioF(self) -> float:
        return 1.0

    def _snap_pan_to_pixels(self, pan: QtCore.QPointF) -> tuple[float, float]:
        return pan.x(), pan.y()

    def _view_world_rect(self) -> QtCore.QRectF:
        pan_x, pan_y = self._snap_pan_to_pixels(self._pan)
        scale = self._scale if self._scale > 0 else 1.0
        width = self.width()
        height = self.height()
        left_world = (-pan_x) / scale
        right_world = (width - pan_x) / scale
        top_world = (-pan_y) / scale
        bottom_world = (height - pan_y) / scale
        return QtCore.QRectF(
            left_world,
            top_world,
            right_world - left_world,
            bottom_world - top_world,
        )


class TestRenderLayers(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if QtWidgets.QApplication.instance() is None:
            cls._app = QtWidgets.QApplication([])
        else:
            cls._app = QtWidgets.QApplication.instance()
        Theme.apply_from_config(load_viewer_config())

    @staticmethod
    def _region_has_paint(img: QtGui.QImage, x0: int, y0: int, x1: int, y1: int) -> bool:
        for y in range(max(0, y0), min(y1, img.height())):
            for x in range(max(0, x0), min(x1, img.width())):
                if img.pixelColor(x, y).alpha() > 0:
                    return True
        return False

    def _paint_to_image(self, paint_fn, stub: _StubBoard) -> QtGui.QImage:
        img = QtGui.QImage(stub.width(), stub.height(), QtGui.QImage.Format_ARGB32_Premultiplied)
        img.fill(0)
        painter = QtGui.QPainter(img)
        paint_fn(LayerContext(stub, painter))
        painter.end()
        self.assertFalse(img.isNull())
        return img

    def test_grid_layer_draws_non_blank(self) -> None:
        stub = _StubBoard()
        img = self._paint_to_image(paint_grid_layer, stub)
        # Cosmetic grid lines rarely hit an arbitrary pixel inside a cell.
        self.assertTrue(self._region_has_paint(img, 90, 40, 98, 200))

    def test_ground_layer_with_textures(self) -> None:
        stub = _StubBoard()
        pm = QtGui.QPixmap(8, 8)
        pm.fill(QtGui.QColor(40, 120, 200))
        stub._ground_textures = [pm]
        img = self._paint_to_image(paint_ground_layer, stub)
        self.assertGreater(img.pixelColor(50, 50).alpha(), 0)

    def test_ground_layer_skips_when_empty(self) -> None:
        stub = _StubBoard()
        stub._ground_textures = []
        img = self._paint_to_image(paint_ground_layer, stub)
        self.assertEqual(img.pixelColor(10, 10).alpha(), 0)

    def test_objectives_layer(self) -> None:
        stub = _StubBoard()
        stub._objectives = [
            SimpleNamespace(
                center=QtCore.QPointF(100.0, 100.0),
                radius=20.0,
                color=QtGui.QColor(200, 50, 50),
                label="A",
                owner_color=QtGui.QColor(255, 255, 0),
                control_radius=35.0,
            )
        ]
        stub._show_objective_radius = False
        img = self._paint_to_image(paint_objectives_layer, stub)
        c = img.pixelColor(100, 100)
        corner = img.pixelColor(5, 5)
        self.assertNotEqual((c.red(), c.green(), c.blue()), (corner.red(), corner.green(), corner.blue()))

    def test_labels_layer(self) -> None:
        stub = _StubBoard()
        stub._objective_labels = [("Obj1", QtCore.QPointF(120.0, 140.0))]
        img = self._paint_to_image(paint_labels_layer, stub)
        self.assertTrue(self._region_has_paint(img, 110, 125, 180, 155))


if __name__ == "__main__":
    unittest.main()
