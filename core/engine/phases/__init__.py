"""Слой иерархических фаз W40k: окна решений и опции действий.

Аддитивный слой над Warhammer40kEnv. Не меняет поведение движка — только
описывает ход как последовательность DecisionWindow со списком ActionOption
и компилирует их обратно в плоский action_dict.
"""

from core.engine.phases.legacy_compiler import (
    compile_options_to_action_dict,
    default_action_dict,
)
from core.engine.phases.option_generator import (
    charge_options_for_unit,
    command_window,
    generate_windows,
    movement_options_for_unit,
    shooting_options_for_unit,
)
from core.engine.phases.types import (
    ActionKind,
    ActionOption,
    DecisionWindow,
    Phase,
    PhaseResult,
    PhaseState,
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
    "SubStep",
    "Timing",
    "generate_windows",
    "command_window",
    "movement_options_for_unit",
    "shooting_options_for_unit",
    "charge_options_for_unit",
    "compile_options_to_action_dict",
    "default_action_dict",
]
