import pytest

from core.engine.phases.stratagems import (
    REGISTRY,
    StratagemDef,
    Trigger,
    by_id,
    for_phase,
    for_trigger,
    legal_stratagem_options,
)
from core.engine.phases.types import ActionKind, Phase
from tests.engine.phases._helpers import build_env


def test_registry_integrity():
    assert len(REGISTRY) == 6
    ids = [d.id for d in REGISTRY]
    assert ids == ["insane_bravery", "overwatch", "smokescreen", "heroic_intervention", "hungry_void", "command_reroll"]
    assert len(ids) == len(set(ids))
    for d in REGISTRY:
        assert isinstance(d, StratagemDef)
        assert d.cp_cost >= 1
        assert by_id(d.id) is d


def test_lookups_by_phase_and_trigger():
    assert any(d.id == "insane_bravery" for d in for_phase(Phase.COMMAND))
    assert any(d.id == "smokescreen" for d in for_phase(Phase.SHOOTING))
    assert any(d.id == "hungry_void" for d in for_phase(Phase.FIGHT))
    assert [d.id for d in for_trigger(Trigger.TARGETED_BY_SHOOTING)] == ["smokescreen"]
    assert [d.id for d in for_trigger(Trigger.BATTLE_SHOCK_FAILED)] == ["insane_bravery"]
    assert [d.id for d in for_trigger(Trigger.FIGHT_PHASE)] == ["hungry_void", "command_reroll"]


def test_smokescreen_requires_smoke_keyword():
    smoke = by_id("smokescreen")
    assert smoke.keyword_req == ("smoke",)
    assert by_id("insane_bravery").keyword_req == ()


def test_by_id_unknown_raises():
    with pytest.raises(KeyError):
        by_id("does_not_exist")


def _alive(env):
    return [i for i, hp in enumerate(env.unit_health) if hp > 0]


def test_command_bravery_cp_gate_and_patch():
    env = build_env()
    alive = _alive(env)

    env.modelCP = 0
    assert (
        legal_stratagem_options(
            env, "model", phase=Phase.COMMAND, trigger=Trigger.BATTLE_SHOCK_FAILED, candidate_unit_idxs=alive
        )
        == []
    )

    env.modelCP = 2
    opts = legal_stratagem_options(
        env, "model", phase=Phase.COMMAND, trigger=Trigger.BATTLE_SHOCK_FAILED, candidate_unit_idxs=alive
    )
    assert [o.unit_idx for o in opts] == alive
    for o in opts:
        assert o.kind is ActionKind.USE_STRATAGEM
        assert o.meta["stratagem_id"] == "insane_bravery"
        assert o.legacy_patch == {"use_cp": 1, "cp_on": int(o.unit_idx)}


def test_smokescreen_legality_follows_env_keyword():
    env = build_env()
    env.modelCP = 1
    env.unit_data[0]["Keywords"] = ["INFANTRY", "SMOKE"]
    env.unit_data[1]["Keywords"] = ["INFANTRY"]
    for i in (0, 1):
        opts = legal_stratagem_options(
            env, "model", phase=Phase.SHOOTING, trigger=Trigger.TARGETED_BY_SHOOTING, candidate_unit_idxs=[i]
        )
        has_smoke_opt = any(o.meta["stratagem_id"] == "smokescreen" for o in opts)
        assert has_smoke_opt == bool(env._unit_has_smoke(env.unit_data[i]))
    assert env._unit_has_smoke(env.unit_data[0]) is True
    assert env._unit_has_smoke(env.unit_data[1]) is False


def test_reaction_options_have_empty_legacy_patch():
    env = build_env()
    env.modelCP = 2
    env.unit_data[0]["Keywords"] = ["INFANTRY", "SMOKE"]
    cases = [
        (Phase.MOVEMENT, Trigger.ENEMY_ENDED_MOVE),
        (Phase.SHOOTING, Trigger.TARGETED_BY_SHOOTING),
        (Phase.CHARGE, Trigger.ENEMY_CHARGED_IN),
    ]
    for phase, trig in cases:
        opts = legal_stratagem_options(env, "model", phase=phase, trigger=trig, candidate_unit_idxs=[0])
        assert opts, f"ожидались опции для {trig}"
        for o in opts:
            assert o.legacy_patch == {}


def test_reaction_cp_gate_blocks_all():
    env = build_env()
    env.modelCP = 0
    env.unit_data[0]["Keywords"] = ["INFANTRY", "SMOKE"]
    for phase, trig in [
        (Phase.MOVEMENT, Trigger.ENEMY_ENDED_MOVE),
        (Phase.SHOOTING, Trigger.TARGETED_BY_SHOOTING),
        (Phase.CHARGE, Trigger.ENEMY_CHARGED_IN),
    ]:
        assert legal_stratagem_options(env, "model", phase=phase, trigger=trig, candidate_unit_idxs=[0]) == []


def test_no_candidates_returns_empty():
    env = build_env()
    env.modelCP = 3
    assert (
        legal_stratagem_options(
            env, "model", phase=Phase.COMMAND, trigger=Trigger.BATTLE_SHOCK_FAILED, candidate_unit_idxs=None
        )
        == []
    )
