"""Board picking helpers (screen-space hitboxes + world-space radius pick).

Extracted from ``OpenGLBoardWidget`` so ``ViewerController`` and tests can share logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

from PySide6 import QtCore


def safe_int(value: object) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def target_hitbox_for_shoot_info(
    info: Dict[str, object],
    hitboxes: Mapping[Tuple[str, int], QtCore.QRectF],
) -> Optional[QtCore.QRectF]:
    """Screen-space rect for a shooting target row (matches legacy widget behaviour)."""
    key = info.get("unit_key")
    if isinstance(key, tuple) and len(key) >= 2:
        rect = hitboxes.get((str(key[0]), int(key[1])))
        if rect is not None and not rect.isEmpty():
            return rect
    unit_id = safe_int(info.get("unit_id"))
    if unit_id is None:
        return None
    for (side, uid), rect in hitboxes.items():
        if int(uid) != int(unit_id):
            continue
        if rect is not None and not rect.isEmpty():
            return rect
    return None


@dataclass(frozen=True)
class HitResult:
    """Serializable picking outcome for QML / tooling."""

    kind: str
    side: str = ""
    unit_id: int = -1

    def as_dict(self) -> Dict[str, Any]:
        return {"kind": self.kind, "side": self.side, "unitId": self.unit_id}

    @staticmethod
    def none() -> HitResult:
        return HitResult(kind="none")


def pick_unit_world(world: QtCore.QPointF, renders: Sequence[Any]) -> Optional[Tuple[str, int]]:
    """Closest unit whose activation radius contains ``world`` (legacy left-click behaviour)."""
    closest_key: Optional[Tuple[str, int]] = None
    closest_dist: Optional[float] = None
    for render in renders:
        dx = world.x() - render.center.x()
        dy = world.y() - render.center.y()
        distance = (dx * dx + dy * dy) ** 0.5
        if distance <= render.radius:
            if closest_dist is None or distance < closest_dist:
                closest_dist = distance
                closest_key = render.key
    return closest_key


def pick_unit_screen(
    screen_pos: QtCore.QPointF,
    hitboxes: Mapping[Tuple[str, int], QtCore.QRectF],
    units_paint_order: Sequence[Any],
) -> Optional[Tuple[str, int]]:
    """Top-most painted unit whose screen-space icon rect contains ``screen_pos``."""
    if not hitboxes:
        return None
    for render in reversed(tuple(units_paint_order)):
        key = render.key
        rect = hitboxes.get(key)
        if rect is not None and rect.contains(screen_pos):
            return key
    return None
