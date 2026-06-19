from tests.engine.phases._helpers import build_env, run_windowed_default_turn


def test_no_policy_runs_turn_without_error_and_no_strat_applied():
    """Parity-test: с reaction_policy=None полный оборот выполняется без ошибок и без молчаливого применения fight-стратагем."""
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.reaction_policy = None
    env.stratagem_used = []
    run_windowed_default_turn(env, side="model")
    # без политики/плана авто-fight-стратагемы не применяются молча
    assert env.stratagem_used == []
