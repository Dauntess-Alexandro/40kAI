"""Viewer MVC/controller layer (migration Sprint 3+).

Sprint 1: typed state adapter.
Sprint 3: ``ViewerController`` QObject bridge.
"""

from app.viewer.controller.state_adapter import (
    ObjectiveSnapshot,
    StateAdapterError,
    StateSnapshot,
    UnitSnapshot,
    adapt_snapshot,
    adapt_snapshot_from_file,
)
from app.viewer.controller.viewer_controller import (
    StatusLabels,
    ViewerController,
    ViewerPresentationContext,
    compute_status_labels,
)

__all__ = [
    "ObjectiveSnapshot",
    "StateAdapterError",
    "StateSnapshot",
    "StatusLabels",
    "UnitSnapshot",
    "ViewerController",
    "ViewerPresentationContext",
    "adapt_snapshot",
    "adapt_snapshot_from_file",
    "compute_status_labels",
]
