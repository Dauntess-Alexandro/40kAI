from core.models.reaction_value_policy import make_reaction_value_policy, make_stratagem_value_policy


class FakeEnv:
    def __init__(self):
        self._reaction_sim_active = False
        self.branch_values = {"apply": 0.5, "pass": 0.1}
        self.restored = 0

    def snapshot_state(self):
        return {"snap": 1}

    def restore_state(self, snap):
        self.restored += 1

    def _simulate_reaction_branch(self, ctx, *, apply):
        return self.branch_values["apply" if apply else "pass"]


def _ctx(env, side="model"):
    return {
        "side": side,
        "stratagem_id": "go_to_ground",
        "phase": "shooting",
        "chosen": 0,
        "candidates": [0],
        "cp": 2,
        "env": env,
        "resolve_trigger": lambda apply: None,
    }


def test_picks_apply_when_value_higher():
    env = FakeEnv()
    pol = make_reaction_value_policy({"model": object()}, device="cpu")
    assert pol(_ctx(env)) is True
    assert env.restored >= 2  # restore после каждой ветки + финал


def test_picks_pass_on_tie_for_cp_economy():
    env = FakeEnv()
    env.branch_values = {"apply": 0.3, "pass": 0.3}
    pol = make_reaction_value_policy({"model": object()}, device="cpu")
    assert pol(_ctx(env)) is False


def test_side_without_net_falls_back_to_legacy_true():
    env = FakeEnv()
    pol = make_reaction_value_policy({"model": None}, device="cpu")
    assert pol(_ctx(env)) is True


def test_recursion_guard_returns_true():
    env = FakeEnv()
    env._reaction_sim_active = True
    pol = make_reaction_value_policy({"model": object()}, device="cpu")
    assert pol(_ctx(env)) is True


def test_net_injected_into_ctx_for_harness():
    env = FakeEnv()
    sentinel = object()
    seen = {}

    def sim(ctx, *, apply):
        seen["net"] = ctx.get("net")
        return 0.5 if apply else 0.1

    env._simulate_reaction_branch = sim
    pol = make_reaction_value_policy({"model": sentinel}, device="cpu")
    pol(_ctx(env))
    assert seen["net"] is sentinel


def test_stratagem_value_policy_alias_exists():
    assert make_reaction_value_policy is make_stratagem_value_policy
