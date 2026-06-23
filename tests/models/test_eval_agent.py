
from core.models.action_contract import action_sizes_from_env
from core.models.eval_agent import (
    EvalAgent,
    _reaction_net_for_algo,
    build_eval_agent,
    resolve_eval_search_cfg,
)
from core.models.PPO import make_actor_critic, ppo_kwargs_from_env
from core.models.sampled_muzero_model import make_sampled_muzero_net
from tests.engine.phases._helpers import build_env


def _agent(env, algo, net, reaction_net):
    cfg = resolve_eval_search_cfg(algo)
    a = EvalAgent.__new__(EvalAgent)
    a.algo = algo
    a.net = net
    a.reaction_net = reaction_net
    a.search = None
    a.cfg = cfg
    a.len_model = len(env.model)
    return a


def _contract_from_env(env):
    """Контракт (vec:N + heads:a,b,c,...) из реального env — для build_eval_agent."""
    n_obs = len(env.get_observation_for_side("model"))
    sizes = action_sizes_from_env(env, len(env.model))
    return {
        "obs_space_signature": f"vec:{n_obs}",
        "action_space_signature": "heads:" + ",".join(str(int(s)) for s in sizes),
    }


def test_reaction_net_none_for_gmz():
    # build_eval_agent для gmz/smz должен ставить reaction_net=None (legacy реакции),
    # остальные алго получают net (value-gate). Проверяем инвариант через _reaction_net_for_algo.
    assert _reaction_net_for_algo("gumbel_muzero", object()) is None
    assert _reaction_net_for_algo("sampled_muzero", object()) is None
    sentinel = object()
    assert _reaction_net_for_algo("ppo", sentinel) is sentinel
    assert _reaction_net_for_algo("dqn", sentinel) is sentinel
    assert _reaction_net_for_algo("alphazero_tree", sentinel) is sentinel


def test_as_policy_fn_returns_action(monkeypatch):
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    a = _agent(env, "ppo", net=object(), reaction_net=object())
    monkeypatch.setattr(a, "select_action", lambda e, side: ({"move_num_0": 0}, None))
    fn = a.as_policy_fn(env, "enemy")
    out = fn(env.get_observation_for_side("enemy"))
    assert out == {"move_num_0": 0}
    assert not hasattr(env, "_pending_fight_stratagem_plan") or getattr(env, "_pending_fight_stratagem_plan", None) is None


def test_build_eval_agent_ppo_smoke():
    # End-to-end: фабрика собирает реальную PPO-сеть из контракта env и даёт рабочий select_action.
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_obs = len(env.get_observation_for_side("model"))
    n_actions = action_sizes_from_env(env, len(env.model))
    net = make_actor_critic(n_obs, n_actions, **ppo_kwargs_from_env())
    agent = build_eval_agent(
        algo="ppo",
        policy_state=net.state_dict(),
        contract=_contract_from_env(env),
        len_model=len(env.model),
        cfg=resolve_eval_search_cfg("ppo"),
    )
    assert agent.reaction_net is not None
    action, plan = agent.select_action(env, "model")
    assert isinstance(action, dict)
    assert plan is None or isinstance(plan, dict)
    for i_u in range(len(env.model)):
        assert f"move_num_{i_u}" in action
        assert isinstance(action[f"move_num_{i_u}"], int)


def test_build_eval_agent_smz_nondefault_arch_loads():
    # Регрессия I1: SMZ learner-чекпойнт с НЕдефолтной архитектурой должен грузиться 1:1.
    # До фикса build_eval_agent строил сеть из env-дефолтной арки и грузил strict → крах.
    # RAM: только TINY-сеть (latent/hidden/embed=8, num_layers=1).
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_obs = len(env.get_observation_for_side("model"))
    n_actions = action_sizes_from_env(env, len(env.model))
    tiny_arch = {"latent_dim": 8, "hidden_dim": 8, "num_layers": 1, "action_embed_dim": 8}
    net = make_sampled_muzero_net(n_obs, n_actions, **tiny_arch)
    agent = build_eval_agent(
        algo="sampled_muzero",
        policy_state=net.state_dict(),
        contract=_contract_from_env(env),
        len_model=len(env.model),
        cfg=resolve_eval_search_cfg("sampled_muzero"),
        arch=dict(tiny_arch),
    )
    assert agent.reaction_net is None  # gmz/smz → legacy реакции
    action, plan = agent.select_action(env, "model")
    assert isinstance(action, dict)
    assert plan is None
