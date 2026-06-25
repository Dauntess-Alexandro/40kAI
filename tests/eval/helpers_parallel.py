from __future__ import annotations

from collections import Counter

from core.engine.phases.legacy_compiler import default_action_dict
from core.models.eval_result import EpisodeResult


class ScriptedEvalAgent:
    algo = "scripted"
    reaction_net = None

    def __init__(self, *, force_stratagem: bool = False):
        self.force_stratagem = bool(force_stratagem)
        self.cfg = type("Cfg", (), {"epsilon": 0.0})()

    def select_action(self, env, side: str):
        units = getattr(env, "model", []) if side == "model" else getattr(env, "enemy", [])
        action = default_action_dict(len(units))
        if self.force_stratagem:
            action["strat_fight"] = 1
            action["strat_fight_unit"] = 0
        return action, None

    def as_policy_fn(self, env, side: str):
        return lambda _obs: self.select_action(env, side)[0]


def make_episode_result(
    *,
    winner: str | None = "model",
    metrics: Counter[str] | None = None,
    action_tuple_counter: Counter[tuple[int, int, int, int]] | None = None,
    model_applied_sids: set[str] | None = None,
    opp_applied_sids: set[str] | None = None,
    trace_block: list[str] | None = None,
) -> EpisodeResult:
    return EpisodeResult(
        winner=winner,
        end_reason="turn_limit",
        vp_diff=3,
        model_vp=8,
        enemy_vp=5,
        episode_len=2,
        total_reward=1.5,
        hp_diff_model_minus_enemy=0.0,
        kill_diff_model_minus_enemy=0.0,
        metrics=metrics or Counter(),
        action_tuple_counter=action_tuple_counter or Counter(),
        model_applied_sids=model_applied_sids or set(),
        opp_applied_sids=opp_applied_sids or set(),
        trace_block=trace_block or [],
        event_log_block=[],
    )
