import pytest
from core.engine.phases.stratagems import (
    REGISTRY,
    StratagemDef,
    Trigger,
    by_id,
    for_phase,
    for_trigger,
)

from core.engine.phases.types import Phase


def test_registry_integrity():
    assert len(REGISTRY) == 4
    ids = [d.id for d in REGISTRY]
    assert ids == ["insane_bravery", "overwatch", "smokescreen", "heroic_intervention"]
    assert len(ids) == len(set(ids))
    for d in REGISTRY:
        assert isinstance(d, StratagemDef)
        assert d.cp_cost >= 1
        assert by_id(d.id) is d


def test_lookups_by_phase_and_trigger():
    assert any(d.id == "insane_bravery" for d in for_phase(Phase.COMMAND))
    assert any(d.id == "smokescreen" for d in for_phase(Phase.SHOOTING))
    assert [d.id for d in for_trigger(Trigger.TARGETED_BY_SHOOTING)] == ["smokescreen"]
    assert [d.id for d in for_trigger(Trigger.BATTLE_SHOCK_FAILED)] == ["insane_bravery"]


def test_smokescreen_requires_smoke_keyword():
    smoke = by_id("smokescreen")
    assert smoke.keyword_req == ("smoke",)
    assert by_id("insane_bravery").keyword_req == ()


def test_by_id_unknown_raises():
    with pytest.raises(KeyError):
        by_id("does_not_exist")
