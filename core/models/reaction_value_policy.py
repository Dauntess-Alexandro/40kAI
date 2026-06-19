"""B3-full: net-value 1-ply lookahead для реакций (apply vs pass).

Ставится в env.reaction_policy. На каждое reaction-решение: snapshot → для веток
apply/pass досимулировать триггер через env._simulate_reaction_branch → value-голова
сети реагирующей стороны → restore → выбрать лучшее (тай → PASS, экономия CP).

Источник сети — net_by_side (по реагирующей стороне). Политика кладёт выбранную сеть
в ctx["net"], откуда её берёт harness env._simulate_reaction_branch.
"""

from __future__ import annotations

from collections.abc import Callable


def make_stratagem_value_policy(net_by_side: dict, *, device, eps: float = 0.0) -> Callable[[dict], bool]:
    def policy(ctx: dict) -> bool:
        env = ctx["env"]
        side = str(ctx["side"])
        net = net_by_side.get(side)
        if net is None:
            return True  # сторона без сети (напр. heuristic-оппонент): legacy «реагировать»
        if bool(getattr(env, "_reaction_sim_active", False)):
            return True  # recursion guard: не уходим в lookahead внутри branch-симуляции
        ctx["net"] = net
        snap = env.snapshot_state()
        values: dict[str, float] = {}
        try:
            for branch in ("pass", "apply"):
                env.restore_state(snap)
                values[branch] = float(env._simulate_reaction_branch(ctx, apply=(branch == "apply")))
        finally:
            env.restore_state(snap)
        return values["apply"] > values["pass"] + float(eps)

    return policy


make_reaction_value_policy = make_stratagem_value_policy
