from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, List, Sequence


class TerrainType(str, Enum):
    OPAQUE = "opaque"
    OBSCURING = "obscuring"
    SOFT = "soft"


@dataclass(frozen=True)
class TerrainFeature:
    kind: TerrainType
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    name: str = ""


@dataclass(frozen=True)
class VisibilityResult:
    can_see: bool
    fully_visible: bool
    has_cover: bool
    soft_penalty: int
    blockers: List[str] = field(default_factory=list)
    obscurers: List[str] = field(default_factory=list)
    soft_zones: List[str] = field(default_factory=list)


def _point_inside_rect(px: float, py: float, feature: TerrainFeature) -> bool:
    return feature.x_min <= px <= feature.x_max and feature.y_min <= py <= feature.y_max


def _segment_intersects_rect(p1: Sequence[float], p2: Sequence[float], feature: TerrainFeature) -> bool:
    x1, y1 = float(p1[0]), float(p1[1])
    x2, y2 = float(p2[0]), float(p2[1])

    if _point_inside_rect(x1, y1, feature) or _point_inside_rect(x2, y2, feature):
        return True

    dx = x2 - x1
    dy = y2 - y1

    p = (-dx, dx, -dy, dy)
    q = (
        x1 - feature.x_min,
        feature.x_max - x1,
        y1 - feature.y_min,
        feature.y_max - y1,
    )

    u1, u2 = 0.0, 1.0
    for pi, qi in zip(p, q):
        if pi == 0:
            if qi < 0:
                return False
            continue
        t = qi / pi
        if pi < 0:
            if t > u2:
                return False
            if t > u1:
                u1 = t
        else:
            if t < u1:
                return False
            if t < u2:
                u2 = t
    return True


def normalize_terrain_features(raw_features: Iterable[dict] | None) -> List[TerrainFeature]:
    features: List[TerrainFeature] = []
    if not raw_features:
        return features
    for idx, raw in enumerate(raw_features):
        if not isinstance(raw, dict):
            continue
        kind_raw = str(raw.get("type", "")).strip().lower()
        if kind_raw not in {t.value for t in TerrainType}:
            continue
        try:
            x_min = float(raw.get("x_min", raw.get("x1")))
            y_min = float(raw.get("y_min", raw.get("y1")))
            x_max = float(raw.get("x_max", raw.get("x2")))
            y_max = float(raw.get("y_max", raw.get("y2")))
        except (TypeError, ValueError):
            continue
        if x_max < x_min:
            x_min, x_max = x_max, x_min
        if y_max < y_min:
            y_min, y_max = y_max, y_min
        features.append(
            TerrainFeature(
                kind=TerrainType(kind_raw),
                x_min=x_min,
                y_min=y_min,
                x_max=x_max,
                y_max=y_max,
                name=str(raw.get("name", "") or f"terrain_{idx}"),
            )
        )
    return features


def evaluate_visibility(attacker: Sequence[float], target: Sequence[float], terrain: Iterable[TerrainFeature]) -> VisibilityResult:
    blockers: List[str] = []
    obscurers: List[str] = []
    soft_zones: List[str] = []

    for feature in terrain:
        if not _segment_intersects_rect(attacker, target, feature):
            continue
        if feature.kind == TerrainType.OPAQUE:
            blockers.append(feature.name)
        elif feature.kind == TerrainType.OBSCURING:
            obscurers.append(feature.name)
        elif feature.kind == TerrainType.SOFT:
            soft_zones.append(feature.name)

    can_see = len(blockers) == 0
    fully_visible = can_see and len(obscurers) == 0 and len(soft_zones) == 0
    has_cover = len(obscurers) > 0
    soft_penalty = len(soft_zones)

    return VisibilityResult(
        can_see=can_see,
        fully_visible=fully_visible,
        has_cover=has_cover,
        soft_penalty=soft_penalty,
        blockers=blockers,
        obscurers=obscurers,
        soft_zones=soft_zones,
    )
