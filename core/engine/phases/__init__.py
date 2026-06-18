"""Слой иерархических фаз W40k: окна решений и опции действий.

Аддитивный слой над Warhammer40kEnv. Не меняет поведение движка — только
описывает ход как последовательность DecisionWindow со списком ActionOption
и компилирует их обратно в плоский action_dict.
"""

from core.engine.phases import phase_engine, stratagem_engine
from core.engine.phases.legacy_compiler import (
    compile_options_to_action_dict,
    default_action_dict,
)
from core.engine.phases.option_generator import (
    charge_options_for_unit,
    command_window,
    fight_stratagem_options_for_unit,
    generate_windows,
    movement_options_for_unit,
    shooting_options_for_unit,
)
from core.engine.phases.stratagem_engine import apply as apply_stratagem
from core.engine.phases.stratagems import (
    REGISTRY,
    StratagemDef,
    Trigger,
    UsageLimit,
    by_id,
    for_phase,
    for_trigger,
    legal_stratagem_options,
)
from core.engine.phases.types import (
    ActionKind,
    ActionOption,
    DecisionWindow,
    Phase,
    PhaseResult,
    PhaseState,
    PhaseTurnState,
    SubStep,
    Timing,
)

__all__ = [
    "ActionKind",
    "ActionOption",
    "DecisionWindow",
    "Phase",
    "PhaseResult",
    "PhaseState",
    "PhaseTurnState",
    "SubStep",
    "Timing",
    "generate_windows",
    "command_window",
    "movement_options_for_unit",
    "shooting_options_for_unit",
    "charge_options_for_unit",
    "fight_stratagem_options_for_unit",
    "compile_options_to_action_dict",
    "default_action_dict",
    "StratagemDef",
    "Trigger",
    "UsageLimit",
    "REGISTRY",
    "by_id",
    "for_phase",
    "for_trigger",
    "legal_stratagem_options",
    "stratagem_engine",
    "apply_stratagem",
    "phase_engine",
]
