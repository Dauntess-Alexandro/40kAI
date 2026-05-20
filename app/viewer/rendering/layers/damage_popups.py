"""Floating damage / heal / save badges above units."""

from __future__ import annotations

from time import monotonic

from PySide6 import QtCore, QtGui

from app.viewer.styles import Theme
from app.viewer.rendering.layer_context import LayerContext


def paint_damage_popups_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    if not w._damage_popups_active:
        return
    now_ts = monotonic()
    painter.save()
    painter.setClipping(False)
    lod_big_font = w._scale >= w._damage_popup_lod_font_shrink_scale
    font_px = w._damage_popup_font_size if lod_big_font else max(7, w._damage_popup_font_size - 2)
    for popup in w._damage_popups_active:
        render = w._unit_by_key.get(popup.target_key)
        if render is None:
            continue
        life_t = max(0.0, min(1.0, (now_ts - popup.created_t) / max(0.001, popup.ttl_s)))
        if life_t >= 1.0:
            continue
        rise_text, rise_badge, _anticip = w._popup_motion_rise(life_t, popup.rise_px)
        fade = 1.0
        if life_t > 0.62:
            fade = max(0.0, 1.0 - (life_t - 0.62) / 0.38)
        sx, sy = w._popup_spiral_offset(popup.stack_index)
        anchor = w._popup_world_anchor_for_key(popup.target_key) or render.center
        lift = float(w.cell_size) * float(getattr(w, "_damage_popup_anchor_lift_cells", 0.34))
        base = QtCore.QPointF(
            anchor.x() + sx,
            anchor.y() - lift + sy,
        )
        badge_center = QtCore.QPointF(base.x(), base.y() - rise_badge)
        parallax_y = (rise_text - rise_badge) * 0.28

        main_font = Theme.font(size=font_px, bold=True)
        fm = QtGui.QFontMetricsF(main_font)
        tw = fm.horizontalAdvance(popup.text_main)
        th = fm.height()
        pad_x = 12.0
        pad_y = 7.0
        inner_w = max(tw + pad_x * 2, 52.0)
        inner_h = th + pad_y * 2
        rect = QtCore.QRectF(-inner_w * 0.5, -inner_h * 0.5, inner_w, inner_h)

        grad_a, grad_b = w._popup_gradient_for_kind(popup.kind)
        glow_base, rim_c = w._popup_text_outline_for_kind(popup.kind)
        badge_path = w._build_damage_popup_badge_path(popup.kind, rect)

        painter.save()
        painter.translate(badge_center)
        pop_boost = 1.0 + 0.14 * (1.0 - min(1.0, life_t / 0.18))
        painter.scale(pop_boost, pop_boost)
        bg = QtGui.QColor(10, 12, 15, int(168 * fade))
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(bg)
        painter.drawPath(badge_path)
        border = QtGui.QColor(w._damage_popup_badge_border)
        border.setAlpha(int(border.alpha() * fade))
        painter.setPen(QtGui.QPen(border, 1.0))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPath(badge_path)

        text_local = QtCore.QPointF(0.0, -parallax_y)
        w._draw_popup_gradient_label(
            painter,
            text_local,
            popup.text_main,
            main_font,
            grad_a,
            grad_b,
            fade,
            glow_base,
            rim_c,
        )
        painter.restore()
    painter.restore()
