import numpy as np

from core.models.alphazero_replay import AZTransition


def _tr(**over):
    kw = dict(state=np.zeros(4, dtype=np.float32), policy_targets=[np.ones(2)], value_target=0.5)
    kw.update(over)
    return AZTransition(**kw)


def test_aztransition_backward_compatible_defaults():
    t = _tr()
    assert t.policy_version == 0
    assert t.faction == ""
    assert t.phase is None
    assert t.window_id is None
    assert t.stratagem_id is None
    assert t.cp_before is None
    assert t.cp_after is None


def test_aztransition_stores_stratagem_metadata():
    t = _tr(phase="fight", window_id="fight:model:0", stratagem_id="hungry_void", cp_before=2, cp_after=1)
    assert t.phase == "fight"
    assert t.window_id == "fight:model:0"
    assert t.stratagem_id == "hungry_void"
    assert t.cp_before == 2
    assert t.cp_after == 1
