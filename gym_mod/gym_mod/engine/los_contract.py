from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Sequence, Tuple


class LosReason(str, Enum):
    """Коды причин LOS-решения для логов, UI и отладки."""

    VISIBLE = "visible"
    FULLY_VISIBLE = "fully_visible"
    BLOCKED_BY_TERRAIN = "blocked_by_terrain"
    BLOCKED_BY_MODEL = "blocked_by_model"
    NO_VISIBLE_SAMPLES = "no_visible_samples"
    INVALID_OBSERVER = "invalid_observer"
    INVALID_TARGET = "invalid_target"


@dataclass(frozen=True)
class LosRuleFlags:
    """Правила исключений для расчёта видимости (Wahapedia-aware)."""

    # Observer can see through other models in its own unit.
    see_through_observer_unit_models: bool = True
    # For unit fully visible checks observer can see through models in observed unit.
    see_through_target_unit_models_for_full: bool = True
    # Terrain blocks line of sight.
    block_by_terrain: bool = True
    # Non-exempt models block line of sight.
    block_by_models: bool = True


@dataclass(frozen=True)
class LosSamplingConfig:
    """Конфиг сэмплов модели для Hybrid LOS (Phase 0: контракт)."""

    sample_count: int = 5
    include_diagonals: bool = False
    # ModelFullyVisible: обязательные фронтальные точки цели.
    required_front_arc_samples: int = 3


@dataclass(frozen=True)
class LosCheckRequest:
    """Единый вход для LOS-проверки (модель->модель)."""

    observer_side: str
    observer_idx: int
    target_side: str
    target_idx: int
    observer_unit_id: Optional[int] = None
    target_unit_id: Optional[int] = None
    flags: LosRuleFlags = field(default_factory=LosRuleFlags)
    sampling: LosSamplingConfig = field(default_factory=LosSamplingConfig)


@dataclass(frozen=True)
class LosCheckResult:
    """Результат LOS-проверки с подробной диагностикой."""

    visible: bool
    fully_visible: bool
    reason_codes: Tuple[LosReason, ...] = field(default_factory=tuple)
    passed_rays: int = 0
    total_rays: int = 0


@dataclass(frozen=True)
class UnitLosSummary:
    """Сводка модельных результатов для unit-level правил."""

    unit_visible: bool
    unit_fully_visible: bool
    model_results: Tuple[LosCheckResult, ...] = field(default_factory=tuple)


def evaluate_unit_visibility(model_results: Sequence[LosCheckResult]) -> UnitLosSummary:
    """
    Агрегация Wahapedia-правил для юнита:
    - Unit Visible: хотя бы одна модель видима.
    - Unit Fully Visible: каждая модель fully visible.

    Функция без привязки к env, нужна как стабильный Phase 0 контракт.
    """

    normalized = tuple(model_results)
    if not normalized:
        return UnitLosSummary(unit_visible=False, unit_fully_visible=False, model_results=tuple())

    unit_visible = any(item.visible for item in normalized)
    unit_fully_visible = all(item.fully_visible for item in normalized)
    return UnitLosSummary(
        unit_visible=bool(unit_visible),
        unit_fully_visible=bool(unit_fully_visible),
        model_results=normalized,
    )
