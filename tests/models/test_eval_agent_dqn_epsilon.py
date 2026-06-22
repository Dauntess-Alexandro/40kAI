"""EvalAgent DQN→epsilon: epsilon-greedy выбирает легальные действия, greedy детерминирован.

Проверяем сквозной путь EvalAgent.select_action для dqn:
- epsilon=0 (greedy): выбор стабилен между вызовами (argmax);
- epsilon=1.0: каждый ход случайный, но всегда в пределах легальных per-unit масок.
"""
import numpy as np

from core.models.action_contract import action_sizes_from_env, ordered_action_keys
from core.models.DQN import make_dqn
from core.models.eval_agent import EvalAgent, EvalSearchCfg
from tests.engine.phases._helpers import build_env


def _reset_env(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    # Юнит 0 в ближнем бою ⇒ нетривиальные shoot_num_0/charge_num_0 маски.
    env.unitInAttack[0] = [1, 0]
    if hasattr(env, "_invalidate_target_cache"):
        env._invalidate_target_cache("test_eval_agent_dqn_epsilon")


def _make_agent(env, *, epsilon: float):
    state = np.asarray(env.get_observation_for_side("model"), dtype=np.float32)
    len_model = len(env.unit_health)
    sizes = action_sizes_from_env(env, len_model)
    net = make_dqn(len(state), sizes, dueling=False, noisy=True, distributional="none")
    net.eval()
    mode = "epsilon" if epsilon > 0 else "greedy"
    cfg = EvalSearchCfg(
        algo="dqn",
        deterministic=(mode == "greedy"),
        epsilon=float(epsilon),
        search={"mode": mode, "epsilon": float(epsilon)},
    )
    # reaction_net=None ⇒ _fight_plan не дёргает тяжёлый бридж в тесте.
    return EvalAgent(algo="dqn", net=net, reaction_net=None, search=None, cfg=cfg, len_model=len_model)


def _assert_legal_per_head(env, action_dict, len_model):
    keys = ordered_action_keys(len_model)
    legal = env.get_legal_action_masks_by_head(side="model")
    for key in keys:
        if not (key.startswith("shoot_num_") or key.startswith("charge_num_")):
            continue
        mask = np.asarray(legal[key], dtype=bool)
        chosen = int(action_dict[key])
        assert 0 <= chosen < len(mask), f"{key}: индекс {chosen} вне маски {len(mask)}"
        assert bool(mask[chosen]), f"{key}: нелегальный индекс {chosen}"


def test_dqn_greedy_is_deterministic():
    env = build_env()
    _reset_env(env)
    agent = _make_agent(env, epsilon=0.0)
    first, _ = agent.select_action(env, "model")
    for _ in range(5):
        again, _ = agent.select_action(env, "model")
        assert again == first, "greedy DQN должен быть детерминированным между вызовами"


def test_dqn_epsilon_stays_legal():
    import random

    env = build_env()
    _reset_env(env)
    len_model = len(env.unit_health)
    agent = _make_agent(env, epsilon=1.0)
    for seed in range(25):
        random.seed(seed)
        action_dict, _ = agent.select_action(env, "model")
        _assert_legal_per_head(env, action_dict, len_model)
