"""Паритет train↔eval при АСИММЕТРИЧНЫХ армиях (len(model) != len(enemy)).

Action space env размерен по len(model) per-unit голов (warhamEnv: цикл range(len(model))),
и сети (policy + reaction) имеют столько же голов. Обе стороны ходят/оцениваются через
этот же model-space контракт. Значит len_model для масок/декода ОБЯЗАН быть len(model)
(= len(self.unit_data)), независимо от стороны. Если взять len(enemy):
  - len(enemy) > len(model) → KeyError move_num_{i} (ключа нет в action_space);
  - len(enemy) < len(model) → масок/голов меньше, чем у сети → shape mismatch.

Зеркальные ростеры (len(model)==len(enemy)) этот класс багов СКРЫВАЮТ — поэтому тут
ростер намеренно асимметричный (model=2, enemy=3).
"""

import pytest
import torch

from core.envs.warhamEnv import Warhammer40kEnv
from core.models.action_contract import action_sizes_from_env
from core.models.DQN import make_dqn
from tests.engine.phases._helpers import make_unit


def _asym_env():
    """env с len(model)=2, len(enemy)=3 (асимметрия)."""
    model = [make_unit("M0"), make_unit("M1")]
    enemy = [make_unit("E0"), make_unit("E1"), make_unit("E2")]
    env = Warhammer40kEnv(enemy=enemy, model=model, b_len=30, b_hei=30)
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    assert len(env.model) == 2 and len(env.enemy) == 3
    assert "move_num_2" not in env.action_space.spaces  # action space размерен по model
    return env


def _dqn_net(env):
    n_obs = len(env.get_observation_for_side("model"))
    n_actions = action_sizes_from_env(env, len(env.model))
    return make_dqn(n_obs, n_actions)


# --- БАГ #2: value-gate (reaction_value_policy) ---

def test_reaction_net_value_enemy_side_on_asymmetric_roster_does_not_crash():
    """warhamEnv._reaction_net_value(side='enemy') строит маски по len(model)
    (=len(unit_data)=размер action_space), не по len(enemy_data). Иначе KeyError move_num_2."""
    env = _asym_env()
    net = _dqn_net(env)
    v_model = env._reaction_net_value("model", net)
    v_enemy = env._reaction_net_value("enemy", net)  # до фикса: KeyError 'move_num_2'
    assert isinstance(v_model, float)
    assert isinstance(v_enemy, float)


def test_dqn_value_bridge_enemy_side_on_asymmetric_roster_does_not_crash():
    """dqn_stratagem_bridge._masks_for_side/dqn_value(side='enemy') — тот же инвариант."""
    from core.models.dqn_stratagem_bridge import dqn_value

    env = _asym_env()
    net = _dqn_net(env)
    v_enemy = dqn_value(env, net, torch.device("cpu"), "enemy")  # до фикса: KeyError 'move_num_2'
    assert isinstance(v_enemy, float)


# --- БАГ #3: opponent через build_policy_fn (play.py + общий адаптер) ---

def test_build_policy_fn_opponent_requires_model_len_on_asymmetric_roster():
    """build_policy_fn(len_model=len(model)) даёт рабочий enemy-policy_fn на асимметрии,
    а len_model=len(enemy) падает KeyError move_num_2 (инвариант call-site play.py/train)."""
    from core.models.opponent_adapter import OpponentSpec, build_policy_fn

    env = _asym_env()
    net = _dqn_net(env)
    n_obs = len(env.get_observation_for_side("model"))
    n_actions = action_sizes_from_env(env, len(env.model))
    contract = {
        "obs_space_signature": f"vec:{n_obs}",
        "action_space_signature": "heads:" + ",".join(str(int(s)) for s in n_actions),
    }
    spec = OpponentSpec(
        agent_id="test-asym",
        algo="dqn",
        contract=contract,
        policy_state=net.state_dict(),
        arch=None,
    )

    fn_good = build_policy_fn(env=env, len_model=len(env.model), opponent=spec, deterministic=True)
    action = fn_good(env.get_observation_for_side("enemy"))
    assert isinstance(action, dict)
    for i in range(len(env.model)):
        assert f"move_num_{i}" in action

    fn_bad = build_policy_fn(env=env, len_model=len(env.enemy), opponent=spec, deterministic=True)
    with pytest.raises(KeyError):
        fn_bad(env.get_observation_for_side("enemy"))


def test_play_py_opponent_build_uses_model_len_not_enemy_len():
    """Guard на call-site play.py: opponent строится с len_model=len(model), не len(enemy)."""
    text = open("play.py", encoding="utf-8").read()
    assert "len_model=len(enemy)" not in text, (
        "play.py строит оппонента с len_model=len(enemy); должно быть len(model): "
        "action space и сеть оппонента размерены по model, иначе KeyError move_num_{i} "
        "на асимметричном ростере (AI-vs-AI Viewer)."
    )
