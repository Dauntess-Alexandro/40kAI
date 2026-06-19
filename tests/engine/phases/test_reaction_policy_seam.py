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
    assert isinstance(effect, dict) and effect.get("cover") is True and effect.get("hit_penalty") == 1
    assert env.modelCP == 1
    assert ("model", "smokescreen", 1, "shooting", 0) in env.stratagem_used


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


def _setup_overwatch(env):
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env._invalidate_target_cache("test")
    env.modelCP = 2
    env.stratagem_used = []
    env.battle_round = 1
    assert env._collect_overwatch_candidates("model", "enemy", 0), "overwatch сетап: нет кандидатов"


def test_overwatch_fires_with_default_policy():
    env = build_env()
    _setup_overwatch(env)
    with env.simulation_mode():
        env._resolve_overwatch("model", "enemy", 0, "movement")
    assert env.modelCP == 1
    assert ("model", "overwatch", 1, "movement", 0) in env.stratagem_used


def test_overwatch_skipped_by_policy_false():
    env = build_env()
    _setup_overwatch(env)
    env.reaction_policy = lambda ctx: False
    with env.simulation_mode():
        env._resolve_overwatch("model", "enemy", 0, "movement")
    assert env.modelCP == 2
    assert env.stratagem_used == []


def test_overwatch_policy_receives_ctx():
    env = build_env()
    _setup_overwatch(env)
    seen = {}

    def policy(ctx):
        seen.update(ctx)
        return True

    env.reaction_policy = policy
    with env.simulation_mode():
        env._resolve_overwatch("model", "enemy", 0, "movement")
    assert seen["stratagem_id"] == "overwatch"
    assert seen["side"] == "model"
    assert seen["cp"] >= 1


def _setup_heroic(env):
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [12, 10]
    env.modelCP = 2
    env.stratagem_used = []
    env.battle_round = 1


def test_heroic_fires_with_default_policy_spends_two():
    env = build_env()
    _setup_heroic(env)
    with env.simulation_mode():
        env._resolve_heroic_intervention("model", "enemy", 0, "charge")
    assert env.modelCP == 0
    assert ("model", "heroic_intervention", 1, "charge", 0) in env.stratagem_used


def test_heroic_skipped_by_policy_false():
    env = build_env()
    _setup_heroic(env)
    env.reaction_policy = lambda ctx: False
    with env.simulation_mode():
        env._resolve_heroic_intervention("model", "enemy", 0, "charge")
    assert env.modelCP == 2
    assert env.stratagem_used == []
