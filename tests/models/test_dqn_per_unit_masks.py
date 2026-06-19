"""B2: DQN select_action применяет per-unit shoot/charge маски ПО КЛЮЧУ.

Раньше маска стрельбы хардкодилась на голову №2 (одиночный head "shoot").
Теперь голов shoot_num_i/charge_num_i много — проверяем, что для каждой такой
головы выбранный индекс легален под её собственной маской (и greedy, и random).
"""

import os

import numpy as np
import torch

from core.models.action_contract import action_sizes_from_env, ordered_action_keys
from core.models.DQN import make_dqn
from core.models.utils import select_action
from tests.engine.phases._helpers import build_env


def _reset_env(env):
    state, _ = env.reset(
        options={"m": env.model, "e": env.enemy, "trunc": True}
    )
    # Делаем юнит 0 'в ближнем бою' -> он не может ни стрелять, ни чарджить,
    # поэтому shoot_num_0/charge_num_0 получают НЕтривиальную маску [True, False].
    # Без этого все маски были бы all-true и тест не ловил бы старый хардкод.
    env.unitInAttack[0] = [1, 0]
    if hasattr(env, "_invalidate_target_cache"):
        env._invalidate_target_cache("test_dqn_per_unit_masks")
    return state


def _assert_nontrivial_masks(env):
    legal = env.get_legal_action_masks_by_head(side="model")
    has_false = any(
        not np.asarray(legal[k], dtype=bool).all()
        for k in legal
        if k.startswith("shoot_num_") or k.startswith("charge_num_")
    )
    assert has_false, "сценарий тривиален: все shoot/charge маски all-true"


def _state_vec(state):
    if isinstance(state, dict):
        return np.array(list(state.values()), dtype=np.float32)
    return np.asarray(state, dtype=np.float32)


def _assert_legal_per_head(env, action_tensor, len_model):
    keys = ordered_action_keys(len_model)
    legal = env.get_legal_action_masks_by_head(side="model")
    acts = action_tensor.numpy()[0]
    assert len(acts) == len(keys), (
        f"число голов {len(acts)} != ordered_action_keys {len(keys)}"
    )
    for idx, key in enumerate(keys):
        if not (key.startswith("shoot_num_") or key.startswith("charge_num_")):
            continue
        mask = np.asarray(legal[key], dtype=bool)
        chosen = int(acts[idx])
        assert 0 <= chosen < len(mask), (
            f"голова {key}: индекс {chosen} вне диапазона маски {len(mask)}"
        )
        assert bool(mask[chosen]), (
            f"голова {key}: выбран нелегальный индекс {chosen}, "
            f"легальные={np.where(mask)[0].tolist()}"
        )


def test_select_action_greedy_respects_per_unit_masks():
    os.environ["FORCE_GREEDY"] = "1"  # детерминированный greedy-путь
    try:
        env = build_env()
        state = _reset_env(env)
        len_model = len(env.unit_health)
        sizes = action_sizes_from_env(env, len_model)
        n_obs = len(_state_vec(state))
        net = make_dqn(n_obs, sizes, dueling=False, noisy=True, distributional="none")
        net.eval()

        _assert_nontrivial_masks(env)
        action = select_action(env, _state_vec(state), 0, net, len_model)
        _assert_legal_per_head(env, action, len_model)
    finally:
        os.environ.pop("FORCE_GREEDY", None)


def test_select_action_random_respects_per_unit_masks():
    # Принудительно ε-ветку: eps=1.0 (sample<=eps), noisy_disable_eps выкл.
    os.environ.pop("FORCE_GREEDY", None)
    os.environ["NOISY_DISABLE_EPS"] = "0"
    os.environ["EPS_SCHEDULE"] = "linear"
    try:
        env = build_env()
        state = _reset_env(env)
        len_model = len(env.unit_health)
        sizes = action_sizes_from_env(env, len_model)
        n_obs = len(_state_vec(state))
        net = make_dqn(n_obs, sizes, dueling=False, noisy=True, distributional="none")
        net.eval()

        _assert_nontrivial_masks(env)
        torch.manual_seed(0)
        # Гоняем много раз: случайный sampler должен всегда оставаться в маске.
        for seed in range(25):
            import random as _r
            _r.seed(seed)
            action = select_action(env, _state_vec(state), 0, net, len_model)
            _assert_legal_per_head(env, action, len_model)
    finally:
        os.environ.pop("NOISY_DISABLE_EPS", None)
        os.environ.pop("EPS_SCHEDULE", None)
