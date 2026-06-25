
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


def test_as_policy_fn_unwraps_gym_wrapper(monkeypatch):
    # Регрессия (GMZ/PPO vs снапшот-оппонент): воркеры self-play передают в build_policy_fn/
    # as_policy_fn env, обёрнутый gym.make в OrderEnforcing. В текущей версии Gymnasium обёртки
    # не проксируют кастомные методы движка → env.get_observation_for_side падал AttributeError
    # ('OrderEnforcing' object has no attribute 'get_observation_for_side'). as_policy_fn обязан
    # развернуть обёртку до Warhammer40kEnv (как делает eval: env_unwrapped).
    from gymnasium.wrappers import OrderEnforcing

    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    a = _agent(env, "ppo", net=object(), reaction_net=object())

    seen = {}

    def _fake_select(e, side):
        # select_action обязан получить РАЗВёрнутый env с методами движка.
        seen["obs"] = e.get_observation_for_side(side)
        return ({"move_num_0": 0}, None)

    monkeypatch.setattr(a, "select_action", _fake_select)

    wrapped = OrderEnforcing(env)
    fn = a.as_policy_fn(wrapped, "enemy")
    out = fn(None)

    assert out == {"move_num_0": 0}
    assert seen["obs"] is not None


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

import torch

from core.models.action_contract import action_tensor_to_dict, ordered_action_keys
from core.models.utils import convertToDict


def test_action_contract_move_heads_are_not_legacy_six_plus_i_for_four_units():
    keys = ordered_action_keys(4)
    assert keys[2:6] == ["move_num_0", "move_num_1", "move_num_2", "move_num_3"]
    assert keys[6:10] == ["shoot_num_0", "shoot_num_1", "shoot_num_2", "shoot_num_3"]
    shoot_start = keys.index("shoot_num_0")
    assert all(keys[shoot_start + i] != f"move_num_{i}" for i in range(4))

    action = torch.zeros((1, len(keys)), dtype=torch.long)
    for i in range(4):
        action[0, 2 + i] = i + 10
        action[0, 6 + i] = i
    decoded = action_tensor_to_dict(action, len_model=4)
    decoded_legacy = convertToDict(action, len_model=4)
    for i in range(4):
        assert decoded[f"move_num_{i}"] == i + 10
        assert decoded_legacy[f"move_num_{i}"] == i + 10


class _FixedDQN(torch.nn.Module):
    def __init__(self, values_by_head):
        super().__init__()
        self.anchor = torch.nn.Parameter(torch.zeros(()))
        self.values_by_head = values_by_head

    def forward(self, obs):
        return [torch.tensor([vals], dtype=torch.float32, device=obs.device) for vals in self.values_by_head]


class _FixedPPO(torch.nn.Module):
    def __init__(self, action):
        super().__init__()
        self.anchor = torch.nn.Parameter(torch.zeros(()))
        self.action = torch.tensor([action], dtype=torch.long)

    def act(self, obs, masks_by_head=None, deterministic=True, temperature=1.0):
        return self.action.to(obs.device), None, None


def test_eval_agent_dqn_and_ppo_do_not_overwrite_move_num_from_legacy_offsets(monkeypatch):
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    lm = len(env.model)
    keys = ordered_action_keys(lm)
    assert lm >= 4

    desired = [0 for _ in keys]
    values = []
    for idx, key in enumerate(keys):
        size = env.action_space.spaces[key].n
        # Для move_num_i выбираем 7+i, для shoot_num_i (= legacy 6+i при n=4) — 0.
        if key.startswith("move_num_"):
            choice = min(7 + int(key.rsplit("_", 1)[1]), size - 1)
        elif key.startswith("shoot_num_"):
            choice = 0
        else:
            choice = 0
        desired[idx] = choice
        vals = [-100.0] * size
        vals[choice] = 100.0
        values.append(vals)

    dqn_agent = _agent(env, "dqn", _FixedDQN(values), reaction_net=object())
    dqn_agent.device = torch.device("cpu")
    monkeypatch.setattr(dqn_agent.cfg, "epsilon", 0.0)
    dqn_action, _ = dqn_agent.select_action(env, "model")

    ppo_agent = _agent(env, "ppo", _FixedPPO(desired), reaction_net=object())
    ppo_agent.device = torch.device("cpu")
    ppo_action, _ = ppo_agent.select_action(env, "model")

    for i in range(4):
        expected = desired[keys.index(f"move_num_{i}")]
        assert dqn_action[f"move_num_{i}"] == expected
        assert ppo_action[f"move_num_{i}"] == expected


def test_eval_agent_masks_are_applied_by_head_name_not_legacy_head_two(monkeypatch):
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    lm = len(env.model)
    keys = ordered_action_keys(lm)
    move0_idx = keys.index("move_num_0")
    values = []
    for idx, key in enumerate(keys):
        size = env.action_space.spaces[key].n
        vals = [0.0] * size
        vals[0] = 10.0
        if idx == move0_idx and size > 1:
            vals[1] = 1.0
        values.append(vals)

    original = env.get_legal_action_masks_by_head

    def _masked(side="model"):
        masks = original(side=side)
        mask = masks["move_num_0"].copy()
        mask[:] = False
        mask[1] = True
        masks["move_num_0"] = mask
        return masks

    monkeypatch.setattr(env, "get_legal_action_masks_by_head", _masked)
    agent = _agent(env, "dqn", _FixedDQN(values), reaction_net=object())
    agent.device = torch.device("cpu")
    monkeypatch.setattr(agent.cfg, "epsilon", 0.0)
    action, _ = agent.select_action(env, "model")
    assert action["move_num_0"] == 1


def test_eval_agent_builds_masks_for_requested_side(monkeypatch):
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    seen = []
    original = env.get_legal_action_masks_by_head

    def _spy(side="model"):
        seen.append(side)
        return original(side=side)

    monkeypatch.setattr(env, "get_legal_action_masks_by_head", _spy)
    keys = ordered_action_keys(len(env.model))
    values = [[1.0] + [0.0] * (env.action_space.spaces[k].n - 1) for k in keys]
    agent = _agent(env, "dqn", _FixedDQN(values), reaction_net=object())
    agent.device = torch.device("cpu")
    monkeypatch.setattr(agent.cfg, "epsilon", 0.0)
    agent.select_action(env, "enemy")
    assert "enemy" in seen


def test_no_legacy_action_head_magic_indices_in_core_paths():
    needles = ("[6" + " +", "head_idx" + " == " + "2")
    paths = [
        "core/models/eval_agent.py",
        "core/models/utils.py",
        "train.py",
    ]
    for path in paths:
        text = open(path, encoding="utf-8").read()
        for needle in needles:
            assert needle not in text, f"legacy action-head index осталось в {path}: {needle}"


class _DummyAZSearch:
    def __init__(self):
        self.calls = []

    def run(self, **kwargs):
        self.calls.append(kwargs)
        legal = kwargs["legal_masks_by_head"]
        pi = []
        selected = []
        for mask in legal:
            arr = mask.astype("float32")
            if arr.sum() <= 0:
                arr[:] = 1.0
            arr = arr / arr.sum()
            pi.append(arr)
            selected.append(int(arr.argmax()))
        return pi, selected, 0.0


def test_az_and_gaz_eval_enemy_side_do_not_use_model_env_rollout():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    for algo in ("alphazero_tree", "gumbel_az"):
        agent = _agent(env, algo, net=object(), reaction_net=object())
        agent.search = _DummyAZSearch()
        agent.device = torch.device("cpu")
        agent.select_action(env, "enemy")
        assert agent.search.calls[-1]["env"] is None
        assert agent.search.calls[-1]["len_model"] is None


def test_az_and_gaz_eval_model_side_keep_env_search_for_train_eval_parity():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    for algo in ("alphazero_tree", "gumbel_az"):
        agent = _agent(env, algo, net=object(), reaction_net=object())
        agent.search = _DummyAZSearch()
        agent.device = torch.device("cpu")
        agent.select_action(env, "model")
        assert agent.search.calls[-1]["env"] is env
        assert agent.search.calls[-1]["len_model"] == len(env.model)


def test_no_legacy_convert_to_dict_in_az_gmz_smz_selfplay_paths():
    paths = [
        "core/models/alphazero_selfplay.py",
        "core/models/gumbel_muzero_selfplay.py",
        "core/models/sampled_muzero_selfplay.py",
    ]
    for path in paths:
        text = open(path, encoding="utf-8").read()
        assert "convertToDict(" not in text, path
        assert "action_tensor_to_dict" in text or path.endswith("sampled_muzero_selfplay.py")
