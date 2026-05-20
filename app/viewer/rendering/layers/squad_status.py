"""HP bars, model pips, and squad labels above units."""

from __future__ import annotations

from app.viewer.styles import Theme
from app.viewer.rendering.layer_context import LayerContext


def paint_squad_status_layer(ctx: LayerContext) -> None:
    w = ctx.widget
    painter = ctx.painter
    if not w._units:
        return
    compact_mode = w._scale < 0.55
    hp_text_font = Theme.font(size=7 if compact_mode else 8, bold=True)
    for render in w._units:
        unit = w._unit_state_by_key.get(render.key)
        if not isinstance(unit, dict):
            continue
        status = w._interpolate_status(render.key)
        if status is None:
            continue
        layout = w._build_status_layout(render, status, compact_mode)
        w._draw_squad_hp_bar(painter, render.key, layout, status, compact_mode)
        if not compact_mode:
            w._draw_squad_model_pips(painter, render.key, layout, status)
            w._draw_squad_hp_text(painter, layout.center_x, layout.top_y - 2.0, status, hp_text_font)
