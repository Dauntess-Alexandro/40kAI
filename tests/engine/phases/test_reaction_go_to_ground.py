"""B3-full Task 4: go_to_ground решается net-value lookahead (резолв входящего выстрела).

Сценарий: defender=enemy[0] (infantry, есть CP). resolve_trigger симулирует выстрел,
снимающий 3 HP БЕЗ cover и 0 HP С cover. net оценивает суммарное HP защитника →
apply (cover) даёт более высокий value → реакция выбирается и тратит 1 CP.
"""

from core.models.reaction_value_policy import make_reaction_value_policy
from tests.engine.phases._helpers import build_env


class _EnemyHpNet:
    """value = суммарное HP стороны enemy (выше HP → выше value)."""

    def __init__(self, env):
        self.env = env

    def infer(self, obs, masks_by_head=None):
        import torch

        return None, torch.tensor([float(sum(self.env.enemy_health))])


def _install(env, stratagem_damage_side="enemy"):
    net = _EnemyHpNet(env)
    env._reaction_net_by_side = {"enemy": net}
    env.reaction_policy = make_reaction_value_policy(env._reaction_net_by_side, device="cpu")

    def trig(apply):
        if not apply:  # без cover выстрел снимает 3 HP
            env.enemy_health[0] = max(0.0, env.enemy_health[0] - 3.0)

    env._pending_reaction_trigger = trig


def test_go_to_ground_applied_when_cover_saves_damage():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.enemyCP = 3
    env.enemy_data[0]["Keywords"] = ["Infantry"]
    env.stratagem_used = []
    _install(env)

    cp_before = env.enemyCP
    effect = env._maybe_use_go_to_ground("enemy", 0, "shooting")

    assert effect == "benefit of cover"
    assert "go_to_ground" in [r[1] for r in env.stratagem_used]
    assert env.enemyCP == cp_before - 1


def test_go_to_ground_skipped_when_no_damage_difference():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.enemyCP = 3
    env.enemy_data[0]["Keywords"] = ["Infantry"]
    env.stratagem_used = []
    net = _EnemyHpNet(env)
    env._reaction_net_by_side = {"enemy": net}
    env.reaction_policy = make_reaction_value_policy(env._reaction_net_by_side, device="cpu")
    env._pending_reaction_trigger = lambda apply: None  # урона нет ни в одной ветке → тай → PASS

    cp_before = env.enemyCP
    effect = env._maybe_use_go_to_ground("enemy", 0, "shooting")

    assert effect is None
    assert "go_to_ground" not in [r[1] for r in env.stratagem_used]
    assert env.enemyCP == cp_before
