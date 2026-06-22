from core.engine.phases.types import Phase
from tests.engine.phases._helpers import build_env


def _setup(env, cp=2):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = cp
    env.enemyCP = cp
    env.stratagem_used = []
    env.active_stratagem_effects = []


def test_choice_none_always_legal():
    env = build_env()
    _setup(env, cp=0)
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "none") is True


def test_command_reroll_needs_cp():
    env = build_env()
    _setup(env, cp=0)
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "command_reroll:hit") is False
    env.modelCP = 1
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "command_reroll:hit") is True
    # подтип не влияет на легальность
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "command_reroll:wound") is True


def test_hungry_void_requires_necrons_keyword():
    env = build_env()
    _setup(env, cp=2)
    # по умолчанию у юнитов нет necrons-keyword (build_env) → hungry_void нелегален
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "hungry_void") is False
    env.unit_data[0]["Keywords"] = ["Necrons"]
    env._invalidate_target_cache("kw")
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "hungry_void") is True


def test_usage_limit_blocks_choice():
    env = build_env()
    _setup(env, cp=3)
    env.battle_round = 1
    env.unit_data[0]["Keywords"] = ["Necrons"]
    # hungry_void PER_PHASE: запись в journal → нелегален в той же (round, phase)
    env.stratagem_used = [("model", "hungry_void", 1, "fight", 0)]
    env.phase = "fight"
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "hungry_void") is False
