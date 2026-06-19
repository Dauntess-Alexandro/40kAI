from core.engine.phases.stratagems import Trigger, by_id, for_trigger
from tests.engine.phases._helpers import build_env


def test_registry_has_go_to_ground():
    d = by_id("go_to_ground")
    assert d.cp_cost == 1
    assert d.keyword_req == ("infantry",)
    assert d.effect_id == "benefit_of_cover"
    assert "go_to_ground" in [s.id for s in for_trigger(Trigger.TARGETED_BY_SHOOTING)]


def _infantry(env, idx):
    env.unit_data[idx]["Keywords"] = ["INFANTRY"]


def test_go_to_ground_gives_cover_for_infantry_without_smoke():
    env = build_env()
    env.modelCP = 1
    env.stratagem_used = []
    _infantry(env, 0)
    assert not env._unit_has_smoke(env.unit_data[0])  # нет SMOKE → не smokescreen
    with env.simulation_mode():
        effect = env._maybe_use_smokescreen("model", 0, "shooting")
    # Go to Ground теперь возвращает dict: Benefit of Cover + 6+ invuln (Task A5)
    assert isinstance(effect, dict)
    assert effect.get("cover") is True
    assert int(effect.get("invuln_grant", 0)) == 6
    assert env.modelCP == 0
    assert any(rec[1] == "go_to_ground" for rec in env.stratagem_used)


def test_go_to_ground_skipped_when_no_cp():
    env = build_env()
    env.modelCP = 0
    env.stratagem_used = []
    _infantry(env, 0)
    with env.simulation_mode():
        effect = env._maybe_use_smokescreen("model", 0, "shooting")
    assert effect is None
    assert env.stratagem_used == []


def test_go_to_ground_skipped_by_reaction_policy():
    env = build_env()
    env.modelCP = 1
    env.stratagem_used = []
    _infantry(env, 0)
    env.reaction_policy = lambda ctx: False
    with env.simulation_mode():
        effect = env._maybe_use_smokescreen("model", 0, "shooting")
    assert effect is None
    assert env.stratagem_used == []


def test_smoke_still_preferred_over_go_to_ground():
    env = build_env()
    env.modelCP = 1
    env.stratagem_used = []
    env.unit_data[0]["Keywords"] = ["INFANTRY", "SMOKE"]
    with env.simulation_mode():
        effect = env._maybe_use_smokescreen("model", 0, "shooting")
    assert isinstance(effect, dict) and effect.get("hit_penalty") == 1
    assert any(rec[1] == "smokescreen" for rec in env.stratagem_used)
    assert not any(rec[1] == "go_to_ground" for rec in env.stratagem_used)


def test_no_cover_when_not_infantry_and_no_smoke():
    env = build_env()
    env.modelCP = 1
    env.stratagem_used = []
    env.unit_data[0]["Keywords"] = ["VEHICLE"]
    with env.simulation_mode():
        effect = env._maybe_use_smokescreen("model", 0, "shooting")
    assert effect is None
    assert env.stratagem_used == []


def test_go_to_ground_returns_cover_and_invuln():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.stratagem_used = []
    env.unit_data[0]["Keywords"] = ["Infantry"]
    eff = env._maybe_use_go_to_ground("model", 0, "shooting")
    assert isinstance(eff, dict)
    assert eff.get("cover") is True
    assert int(eff.get("invuln_grant", 0)) == 6
