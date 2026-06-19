"""B1c: enforce usage_limit стратагем (PER_PHASE / PER_TURN / PER_BATTLE / UNLIMITED).

Проверяем два слоя: hard-guard в stratagem_engine.apply (нельзя списать CP сверх лимита)
и фильтр в legal_stratagem_options (исчерпанная стратагема не предлагается как опция).
"""

from core.engine.phases import stratagem_engine
from core.engine.phases.option_generator import fight_stratagem_options_for_unit
from core.engine.phases.stratagems import Trigger, legal_stratagem_options
from core.engine.phases.types import ActionKind, Phase
from tests.engine.phases._helpers import build_env


def _fresh(env):
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env.battle_round = 1


# --- apply hard-guard ---

def test_per_battle_blocks_second_use_same_battle():
    env = build_env()
    _fresh(env)
    env.modelCP = 5
    r1 = stratagem_engine.apply(env, "model", "insane_bravery", 0, phase="command")
    assert r1["ok"] is True and env.modelCP == 4
    r2 = stratagem_engine.apply(env, "model", "insane_bravery", 0, phase="command")
    assert r2 == {"ok": False, "cp_spent": 0, "reason": "usage_limit"}
    assert env.modelCP == 4  # CP не списан повторно
    assert [rec[1] for rec in env.stratagem_used].count("insane_bravery") == 1


def test_per_phase_blocks_second_use_same_phase_but_allows_next_round():
    env = build_env()
    _fresh(env)
    env.modelCP = 9
    assert stratagem_engine.apply(env, "model", "hungry_void", 0, phase="fight")["ok"] is True
    blocked = stratagem_engine.apply(env, "model", "hungry_void", 0, phase="fight")
    assert blocked == {"ok": False, "cp_spent": 0, "reason": "usage_limit"}
    # Новый раунд — снова доступно.
    env.battle_round = 2
    assert stratagem_engine.apply(env, "model", "hungry_void", 0, phase="fight")["ok"] is True


def test_per_phase_independent_per_side():
    env = build_env()
    _fresh(env)
    env.modelCP = 3
    env.enemyCP = 3
    assert stratagem_engine.apply(env, "model", "hungry_void", 0, phase="fight")["ok"] is True
    # У врага свой лимит — не затронут использованием model.
    assert stratagem_engine.apply(env, "enemy", "hungry_void", 0, phase="fight")["ok"] is True


def test_unlimited_allows_repeated_use():
    env = build_env()
    _fresh(env)
    env.modelCP = 5
    # go_to_ground — UsageLimit.UNLIMITED.
    assert stratagem_engine.apply(env, "model", "go_to_ground", 0, phase="shooting")["ok"] is True
    assert stratagem_engine.apply(env, "model", "go_to_ground", 0, phase="shooting")["ok"] is True


# --- legal_stratagem_options фильтр (policy path) ---

def test_legal_options_drops_exhausted_per_phase():
    env = build_env()
    _fresh(env)
    env.modelCP = 5
    env.unit_health[0] = 6.0
    opts_before = fight_stratagem_options_for_unit(env, "model", 0)
    assert any(o.meta.get("stratagem_id") == "hungry_void" for o in opts_before)
    stratagem_engine.apply(env, "model", "hungry_void", 0, phase="fight")
    opts_after = fight_stratagem_options_for_unit(env, "model", 0)
    assert not any(o.meta.get("stratagem_id") == "hungry_void" for o in opts_after)


def test_legal_options_drops_exhausted_per_battle_insane_bravery():
    env = build_env()
    _fresh(env)
    env.modelCP = 5
    env.phase = "command"
    before = [
        o
        for o in legal_stratagem_options(
            env, "model", phase=Phase.COMMAND, trigger=Trigger.BATTLE_SHOCK_FAILED, candidate_unit_idxs=[0]
        )
        if o.kind is ActionKind.USE_STRATAGEM
    ]
    assert any(o.meta.get("stratagem_id") == "insane_bravery" for o in before)
    stratagem_engine.apply(env, "model", "insane_bravery", 0, phase="command")
    env.battle_round = 3  # даже в другом раунде PER_BATTLE остаётся исчерпанной
    after = [
        o
        for o in legal_stratagem_options(
            env, "model", phase=Phase.COMMAND, trigger=Trigger.BATTLE_SHOCK_FAILED, candidate_unit_idxs=[0]
        )
        if o.kind is ActionKind.USE_STRATAGEM
    ]
    assert not any(o.meta.get("stratagem_id") == "insane_bravery" for o in after)
