from collections import Counter

from eval import _accumulate_episode_result, new_assignment_accumulator
from tests.eval.helpers_parallel import make_episode_result


def test_accumulator_uses_structured_metrics_and_action_counter():
    result = make_episode_result(
        winner="model",
        metrics=Counter({"total_model_steps": 2, "m_strat_applied_command_reroll": 1}),
        action_tuple_counter=Counter({(4, 0, 0, 0): 2}),
        model_applied_sids={"command_reroll"},
        trace_block=["[TRACE][MODEL_ACTION_HUMAN] should_not_be_parsed"],
    )
    acc = new_assignment_accumulator()

    _accumulate_episode_result(acc, idx=1, result=result, learner_side="P1", opponent_side="P2")

    assert acc.step_metrics["total_model_steps"] == 2
    assert acc.step_metrics["m_games_total"] == 1
    assert acc.step_metrics["m_strat_games_used_command_reroll"] == 1
    assert acc.action_tuple_counter[(4, 0, 0, 0)] == 2
