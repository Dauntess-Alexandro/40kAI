from core.engine.phases.stratagems import by_id
from tests.engine.phases._helpers import build_env


def test_heroic_registry_cost_is_two():
    assert by_id("heroic_intervention").cp_cost == 2


def test_should_use_reaction_default_true_when_no_policy():
    env = build_env()
    env.reaction_policy = None
    assert env._should_use_reaction("overwatch", "model", 0, [0], "movement", 2) is True


def test_should_use_reaction_delegates_to_policy_and_passes_ctx():
    env = build_env()
    captured = {}

    def policy(ctx):
        captured.update(ctx)
        return False

    env.reaction_policy = policy
    assert env._should_use_reaction("overwatch", "model", 0, [0, 1], "movement", 2) is False
    assert captured["stratagem_id"] == "overwatch"
    assert captured["side"] == "model"
    assert captured["chosen"] == 0
    assert captured["candidates"] == [0, 1]
    assert captured["cp"] == 2


def test_should_use_reaction_policy_exception_falls_back_to_true():
    env = build_env()

    def boom(ctx):
        raise ValueError("policy boom")

    env.reaction_policy = boom
    assert env._should_use_reaction("smokescreen", "model", 0, [0], "shooting", 1) is True


def test_smokescreen_fires_with_default_policy():
    env = build_env()
    env.unit_data[0]["Keywords"] = ["INFANTRY", "SMOKE"]
    env.modelCP = 2
    env.stratagem_used = []
    env.battle_round = 1
    with env.simulation_mode():
        effect = env._maybe_use_smokescreen("model", 0, "shooting")
    assert effect == "benefit of cover"
    assert env.modelCP == 1
    assert ("model", "smokescreen", 1) in env.stratagem_used


def test_smokescreen_skipped_by_policy():
    env = build_env()
    env.unit_data[0]["Keywords"] = ["INFANTRY", "SMOKE"]
    env.modelCP = 2
    env.stratagem_used = []
    env.reaction_policy = lambda ctx: False
    with env.simulation_mode():
        effect = env._maybe_use_smokescreen("model", 0, "shooting")
    assert effect is None
    assert env.modelCP == 2
    assert env.stratagem_used == []
