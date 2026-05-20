"""Typed read-only view of ``state.json`` for viewer migration.

Contract docs: ``docs/viewer_state_contract.md``.
Engine writes JSON via ``core/engine/state_export.py``; this module must stay tolerant
to unknown keys and tolerate partial payloads (merged with viewer defaults).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Mapping, Optional, Tuple, Union

from app.viewer.state import load_state, merge_with_defaults


class StateAdapterError(ValueError):
    """Raised when a snapshot cannot be built from malformed root types."""


def _safe_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def _protocol_version_from_viewer(viewer_block: Any) -> str:
    if not isinstance(viewer_block, dict):
        return "0.0"
    raw = viewer_block.get("state_protocol_version") or viewer_block.get("protocol_version")
    text = _safe_str(raw)
    return text if text is not None else "0.0"


def _board_dims(board: Any) -> Tuple[int, int]:
    """Return (width, height) in cells — matches ``OpenGLBoardWidget._resolve_board_dims`` expectations."""
    default_w, default_h = 60, 40
    if not isinstance(board, dict):
        return default_w, default_h
    w = (
        _safe_int(board.get("width"))
        or _safe_int(board.get("cols"))
        or _safe_int(board.get("board_w"))
    )
    h = (
        _safe_int(board.get("height"))
        or _safe_int(board.get("rows"))
        or _safe_int(board.get("board_h"))
    )
    return (
        int(w if w is not None else default_w),
        int(h if h is not None else default_h),
    )


@dataclass(frozen=True)
class UnitSnapshot:
    side: Optional[str]
    id: Optional[int]
    name: Optional[str]
    x: Optional[int]
    y: Optional[int]
    hp: Optional[float]
    alive_models: Optional[int]


@dataclass(frozen=True)
class ObjectiveSnapshot:
    id: Optional[int]
    x: Optional[int]
    y: Optional[int]


@dataclass(frozen=True)
class StateSnapshot:
    """Normalized snapshot for UI/controller layers."""

    protocol_version: str
    round: Optional[int]
    turn: Optional[int]
    phase: Optional[str]
    active_side: Optional[str]
    board_width: int
    board_height: int
    vp_player: Optional[int]
    vp_model: Optional[int]
    cp_player: Optional[int]
    cp_model: Optional[int]
    units: Tuple[UnitSnapshot, ...]
    objectives: Tuple[ObjectiveSnapshot, ...]
    deployment: Mapping[str, Any]
    viewer_block: Mapping[str, Any]
    movement_overlay: Optional[Any]
    model_events: Tuple[Any, ...]
    log_tail: Tuple[str, ...]
    degraded: bool
    degraded_reason: Optional[str]


def _parse_units(raw_units: Any) -> Tuple[UnitSnapshot, ...]:
    if not isinstance(raw_units, list):
        return ()
    out: List[UnitSnapshot] = []
    for entry in raw_units:
        if not isinstance(entry, dict):
            continue
        hp_raw = entry.get("hp")
        try:
            hp_val = float(hp_raw) if hp_raw is not None else None
        except (TypeError, ValueError):
            hp_val = None
        out.append(
            UnitSnapshot(
                side=_safe_str(entry.get("side")),
                id=_safe_int(entry.get("id")),
                name=_safe_str(entry.get("name")),
                x=_safe_int(entry.get("x")),
                y=_safe_int(entry.get("y")),
                hp=hp_val,
                alive_models=_safe_int(entry.get("alive_models")),
            )
        )
    return tuple(out)


def _parse_objectives(raw_obj: Any) -> Tuple[ObjectiveSnapshot, ...]:
    if not isinstance(raw_obj, list):
        return ()
    out: List[ObjectiveSnapshot] = []
    for entry in raw_obj:
        if not isinstance(entry, dict):
            continue
        out.append(
            ObjectiveSnapshot(
                id=_safe_int(entry.get("id")),
                x=_safe_int(entry.get("x")),
                y=_safe_int(entry.get("y")),
            )
        )
    return tuple(out)


def _tuple_model_events(raw: Any) -> Tuple[Any, ...]:
    if not isinstance(raw, list):
        return ()
    return tuple(raw)


def _tuple_log_tail(raw: Any) -> Tuple[str, ...]:
    if not isinstance(raw, list):
        return ()
    lines: List[str] = []
    for item in raw:
        lines.append(str(item) if item is not None else "")
    return tuple(lines)


def adapt_snapshot(
    raw: Mapping[str, Any],
    *,
    merge_defaults: bool = True,
) -> StateSnapshot:
    """Build a ``StateSnapshot`` from a decoded JSON-like mapping."""
    degraded = False
    degraded_reason: Optional[str] = None

    if not isinstance(raw, Mapping):
        raise StateAdapterError("state root must be a JSON object")

    merged: dict[str, Any] = dict(raw)
    if merge_defaults:
        merged = merge_with_defaults(merged)

    board_w, board_h = _board_dims(merged.get("board"))

    vp_block = merged.get("vp")
    cp_block = merged.get("cp")
    vp_player = vp_model = cp_player = cp_model = None
    if isinstance(vp_block, dict):
        vp_player = _safe_int(vp_block.get("player"))
        vp_model = _safe_int(vp_block.get("model"))
    if isinstance(cp_block, dict):
        cp_player = _safe_int(cp_block.get("player"))
        cp_model = _safe_int(cp_block.get("model"))

    active = merged.get("active")
    if active is None:
        active = merged.get("active_side")
    active_side = _safe_str(active)

    viewer_block = merged.get("viewer")
    if viewer_block is not None and not isinstance(viewer_block, dict):
        viewer_block = {}
        degraded = True
        degraded_reason = "viewer block coerced from non-object"
    viewer_mapping: Mapping[str, Any] = viewer_block if isinstance(viewer_block, dict) else {}

    deployment = merged.get("deployment")
    deployment_mapping: Mapping[str, Any] = deployment if isinstance(deployment, dict) else {}

    return StateSnapshot(
        protocol_version=_protocol_version_from_viewer(viewer_mapping),
        round=_safe_int(merged.get("round")),
        turn=_safe_int(merged.get("turn")),
        phase=_safe_str(merged.get("phase")),
        active_side=active_side.lower() if active_side else None,
        board_width=board_w,
        board_height=board_h,
        vp_player=vp_player,
        vp_model=vp_model,
        cp_player=cp_player,
        cp_model=cp_model,
        units=_parse_units(merged.get("units")),
        objectives=_parse_objectives(merged.get("objectives")),
        deployment=deployment_mapping,
        viewer_block=viewer_mapping,
        movement_overlay=merged.get("movement_overlay"),
        model_events=_tuple_model_events(merged.get("model_events")),
        log_tail=_tuple_log_tail(merged.get("log_tail")),
        degraded=degraded,
        degraded_reason=degraded_reason,
    )


def adapt_snapshot_from_file(path: Union[str, Path]) -> StateSnapshot:
    """Load via ``load_state`` (retry/partial-read tolerant) then adapt."""
    merged = load_state(str(path))
    return adapt_snapshot(merged, merge_defaults=False)

