"""Честный 1:1 eval: обе стороны строятся одной фабрикой EvalAgent.

Симметрия — главный инвариант Task 5: для одного и того же algo learner (model)
и opponent (enemy) получают одинаковую конфигурацию (в т.ч. reaction_net).
Дополнительно проверяем, что run_episode принимает новую агент-сигнатуру.
"""
from __future__ import annotations

import inspect

import torch

from core.models.eval_agent import build_eval_agent, resolve_eval_search_cfg
from tests.engine.phases._helpers import build_env


def _contract_from_env(env):
    obs = env.get_observation_for_side("model")
    from core.models.utils import build_action_masks_by_head

    masks = build_action_masks_by_head(env, len(env.model), log_fn=None, debug=False)
    heads = ",".join(str(int(m.numel())) for m in masks)
    return {
        "obs_space_signature": f"vec:{len(obs)}",
        "action_space_signature": f"heads:{heads}",
    }


def test_both_sides_get_reaction_net_for_same_algo():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    contract = _contract_from_env(env)
    from core.models.opponent_adapter import _parse_contract_sizes
    from core.models.PPO import make_actor_critic, ppo_kwargs_from_env

    n_obs, n_actions = _parse_contract_sizes(contract)
    net = make_actor_critic(n_obs, n_actions, **ppo_kwargs_from_env())
    cfg = resolve_eval_search_cfg("ppo")
    p1 = build_eval_agent(
        algo="ppo", policy_state=net.state_dict(), contract=contract,
        len_model=len(env.model), cfg=cfg,
    )
    p2 = build_eval_agent(
        algo="ppo", policy_state=net.state_dict(), contract=contract,
        len_model=len(env.enemy), cfg=cfg,
    )
    assert p1.reaction_net is not None and p2.reaction_net is not None


def test_run_episode_accepts_agent_signature():
    """run_episode перешёл на агент-сигнатуру (Task 5): без policy_net/epsilon/algo."""
    import eval as eval_mod

    sig = inspect.signature(eval_mod.run_episode)
    params = list(sig.parameters.keys())
    assert "learner_agent" in params and "opponent_agent" in params
    # Старые позиционные параметры выехали внутрь агентов.
    assert "policy_net" not in params
    assert "epsilon" not in params
    assert "opponent_policy_fn" not in params
