"""Shooting target HUD (screen-space sprites / fallback rects)."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from PySide6 import QtCore, QtGui

from app.viewer.styles import Theme
from app.viewer.rendering.hit_test import target_hitbox_for_shoot_info
from app.viewer.rendering.layer_context import LayerContext


def paint_shooting_targets_overlay(
    ctx: LayerContext,
    target_infos: List[Dict[str, object]],
    hovered_target_key: Optional[Tuple[str, int]],
    *,
    render_under_units: bool,
) -> None:
    if not target_infos:
        return

    w = ctx.widget
    painter = ctx.painter

    w._rebuild_unit_hitboxes_screen()

    style_map = {
        "VALID": {
            "outline": QtGui.QColor(96, 214, 118, 235),
            "glow": QtGui.QColor(96, 214, 118, 78),
            "width": 1.8,
            "expand": 7.0,
            "base": "target_valid_base",
            "marker": "target_marker_valid",
        },
        "OBSCURED": {
            "outline": QtGui.QColor(232, 190, 85, 220),
            "glow": QtGui.QColor(232, 190, 85, 62),
            "width": 1.7,
            "expand": 6.0,
            "base": "target_obscured_base",
            "marker": "target_marker_obscured",
        },
        "NO_LOS": {
            "outline": QtGui.QColor(145, 150, 160, 185),
            "glow": QtGui.QColor(145, 150, 160, 0),
            "width": 1.3,
            "expand": 4.0,
            "base": "target_nolos_base",
            "marker": "target_marker_nolos",
        },
    }
    fx_assets = w._target_overlay_assets()
    hover_ring = fx_assets.get("target_hover_ring")

    def _sprite(key: str) -> Optional[QtGui.QPixmap]:
        pix = fx_assets.get(key)
        if pix is None or pix.isNull():
            return None
        return pix

    painter.save()
    painter.setTransform(QtGui.QTransform())
    painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

    hitboxes = w._unit_hitboxes_screen

    for info in target_infos:
        key = info.get("unit_key")
        rect = target_hitbox_for_shoot_info(info, hitboxes)
        if rect is None:
            continue

        classification = str(info.get("classification") or "NO_LOS")
        style = style_map.get(classification, style_map["NO_LOS"])
        hovered = hovered_target_key is not None and isinstance(key, tuple) and len(key) >= 2 and (str(key[0]), int(key[1])) == hovered_target_key
        base_pixmap = _sprite(str(style.get("base") or ""))
        marker_pixmap = _sprite(str(style.get("marker") or ""))
        use_sprite_overlay = base_pixmap is not None and marker_pixmap is not None

        if use_sprite_overlay:
            if render_under_units:
                base_rect = rect.adjusted(-rect.width() * 0.12, -rect.height() * 0.12, rect.width() * 0.12, rect.height() * 0.12)
                base_draw_rect = w._fit_pixmap_in_rect(base_pixmap, base_rect, inset_ratio=1.0)
                painter.save()
                painter.setOpacity(0.48)
                painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
                painter.drawPixmap(base_draw_rect, base_pixmap, QtCore.QRectF(base_pixmap.rect()))
                painter.restore()

                if hovered and hover_ring is not None:
                    ring_rect = rect.adjusted(-rect.width() * 0.20, -rect.height() * 0.20, rect.width() * 0.20, rect.height() * 0.20)
                    ring_draw_rect = w._fit_pixmap_in_rect(hover_ring, ring_rect, inset_ratio=1.0)
                    painter.save()
                    painter.setOpacity(0.42)
                    painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
                    painter.drawPixmap(ring_draw_rect, hover_ring, QtCore.QRectF(hover_ring.rect()))
                    painter.restore()
            else:
                marker_side = max(16.0, min(rect.width(), rect.height()) * 0.62)
                marker_target_rect = QtCore.QRectF(
                    rect.right() + 5.0,
                    rect.top() - marker_side * 0.40,
                    marker_side,
                    marker_side,
                )
                marker_draw_rect = w._fit_pixmap_in_rect(marker_pixmap, marker_target_rect, inset_ratio=1.0)
                painter.save()
                painter.setOpacity(0.86)
                painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
                painter.drawPixmap(marker_draw_rect, marker_pixmap, QtCore.QRectF(marker_pixmap.rect()))
                painter.restore()
            continue

        if render_under_units:
            continue

        expand = float(style["expand"]) + (2.0 if hovered else 0.0)
        glow_rect = rect.adjusted(-expand, -expand, expand, expand)
        outline_rect = rect.adjusted(-0.5, -0.5, 0.5, 0.5)

        glow = QtGui.QColor(style["glow"])
        if hovered:
            glow.setAlpha(min(255, int(glow.alpha() * 1.35) + 18))
        if glow.alpha() > 0:
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(glow)
            painter.drawRoundedRect(glow_rect, 6.0, 6.0)

        pen = QtGui.QPen(QtGui.QColor(style["outline"]), float(style["width"]) + (0.7 if hovered else 0.0))
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRoundedRect(outline_rect, 4.0, 4.0)

        if w._viewer_debug_enabled:
            dbg_pen = QtGui.QPen(QtGui.QColor(120, 220, 120, 135), 0.9)
            dbg_pen.setCosmetic(True)
            painter.setPen(dbg_pen)
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.drawRect(rect)

        if hovered:
            marker_pos = QtCore.QPointF(rect.right() + 6.0, rect.top() - 4.0)
            marker_bg = QtCore.QRectF(marker_pos.x() - 2.0, marker_pos.y() - 1.0, 18.0, 18.0)
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(QtGui.QColor(24, 24, 24, 155))
            painter.drawRoundedRect(marker_bg, 6.0, 6.0)
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 245, 190, 245), 1.0))
            font = QtGui.QFont(Theme.font(size=9, bold=True))
            painter.setFont(font)
            painter.drawText(marker_bg, QtCore.Qt.AlignCenter, "🎯")

    painter.restore()
