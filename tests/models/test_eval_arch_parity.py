"""Тесты единого резолвера архитектуры eval и сборки агента (Task 1 + Task 2).

Источник истины: docs/superpowers/plans/2026-06-25-eval-arch-parity.md
(Task 1: resolve_arch_for_algo; Task 2: build_eval_agent — log_fn + GMZ на arch/lenient).
"""
import torch

from core.engine import agent_registry
from core.engine.agent_registry import AgentIdentity, save_agent_artifact
from core.models.action_contract import action_sizes_from_env
from core.models.eval_agent import build_eval_agent, resolve_arch_for_algo, resolve_eval_search_cfg
from core.models.gumbel_muzero_model import make_gumbel_muzero_net
from core.models.opponent_adapter import load_agent_opponent
from core.models.sampled_muzero_model import make_sampled_muzero_net
from core.models.utils import normalize_state_dict
from tests.engine.phases._helpers import build_env


def test_resolve_arch_for_algo_dispatch():
    # dqn — арка инферится из state_dict, отдельная arch не нужна
    assert resolve_arch_for_algo("dqn", {"arch": {"hidden_size": 8}}) is None
    # ppo — мёрдж с env-дефолтами, ключи из payload переопределяют
    ppo = resolve_arch_for_algo("ppo", {"arch": {"hidden_size": 17, "num_layers": 1}})
    assert ppo["hidden_size"] == 17 and ppo["num_layers"] == 1
    # alphazero_tree
    az = resolve_arch_for_algo("alphazero_tree", {"arch": {"hidden_size": 19}})
    assert az["hidden_size"] == 19
    # gumbel_muzero
    gmz = resolve_arch_for_algo("gumbel_muzero", {"arch": {"latent_dim": 8, "num_layers": 1}})
    assert gmz["latent_dim"] == 8 and gmz["num_layers"] == 1
    # sampled_muzero
    smz = resolve_arch_for_algo("sampled_muzero", {"arch": {"hidden_dim": 8}})
    assert smz["hidden_dim"] == 8
    # пустой payload → None или env-дефолты (не падает)
    assert resolve_arch_for_algo("ppo", None) is None or isinstance(resolve_arch_for_algo("ppo", None), dict)


# --- Task 2: build_eval_agent — GMZ на arch+lenient + параметр log_fn ---

def _contract(env):
    n_obs = len(env.get_observation_for_side("model"))
    sizes = action_sizes_from_env(env, len(env.model))
    return {
        "obs_space_signature": f"vec:{n_obs}",
        "action_space_signature": "heads:" + ",".join(str(int(s)) for s in sizes),
    }


def test_build_eval_agent_gmz_nondefault_arch_loads_1to1():
    # GMZ learner-чекпойнт с НЕдефолтной аркой (вкл. num_layers) грузится без потерь.
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_obs = len(env.get_observation_for_side("model"))
    n_actions = action_sizes_from_env(env, len(env.model))
    tiny = {"latent_dim": 8, "hidden_dim": 8, "num_layers": 1, "action_embed_dim": 8}
    net = make_gumbel_muzero_net(n_obs, n_actions, **tiny)

    warns: list[str] = []
    agent = build_eval_agent(
        algo="gumbel_muzero",
        policy_state=net.state_dict(),
        contract=_contract(env),
        len_model=len(env.model),
        cfg=resolve_eval_search_cfg("gumbel_muzero"),
        arch=dict(tiny),
        log_fn=warns.append,
    )
    # 1:1: ни одного WARN про missing/unexpected
    assert not any("missing" in w for w in warns), warns
    action, plan = agent.select_action(env, "model")
    assert isinstance(action, dict)


def test_build_eval_agent_gmz_missing_unexpected_warns():
    # Совпадающие по форме веса, но с лишним/недостающим ключом → lenient-загрузка:
    # WARN про missing/unexpected, БЕЗ краша. Это та «тихая деградация», которую делаем видимой.
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_obs = len(env.get_observation_for_side("model"))
    n_actions = action_sizes_from_env(env, len(env.model))
    tiny = {"latent_dim": 8, "hidden_dim": 8, "num_layers": 1, "action_embed_dim": 8}
    net = make_gumbel_muzero_net(n_obs, n_actions, **tiny)

    state = dict(net.state_dict())
    state["bogus_unexpected.weight"] = torch.zeros(2, 2)   # unexpected
    state.pop(next(iter(net.state_dict().keys())))          # missing (но без shape-конфликта)

    warns: list[str] = []
    build_eval_agent(
        algo="gumbel_muzero",
        policy_state=state,
        contract=_contract(env),
        len_model=len(env.model),
        cfg=resolve_eval_search_cfg("gumbel_muzero"),
        arch=dict(tiny),       # арка совпадает → нет size mismatch, только missing/unexpected
        log_fn=warns.append,
    )
    assert any("missing" in w or "unexpected" in w for w in warns), warns


def test_build_eval_agent_gmz_shape_mismatch_raises():
    # arch=None (env-дефолт 256) на TINY-весах (8): совпадающие ключи, РАЗНЫЕ shape →
    # PyTorch strict=False всё равно падает на size mismatch. build_eval_agent обязан отдать
    # ПОНЯТНУЮ RU-ошибку (что/где/что делать), а не сырой RuntimeError и не мусорную сеть.
    import pytest

    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_obs = len(env.get_observation_for_side("model"))
    n_actions = action_sizes_from_env(env, len(env.model))
    tiny = {"latent_dim": 8, "hidden_dim": 8, "num_layers": 1, "action_embed_dim": 8}
    net = make_gumbel_muzero_net(n_obs, n_actions, **tiny)

    with pytest.raises(RuntimeError, match="не совпадает|size mismatch"):
        build_eval_agent(
            algo="gumbel_muzero",
            policy_state=net.state_dict(),
            contract=_contract(env),
            len_model=len(env.model),
            cfg=resolve_eval_search_cfg("gumbel_muzero"),
            arch=None,  # ← рассинхрон shape → фатально
        )


# --- Task 3: OpponentSpec.arch + извлечение в load_agent_opponent ---

def test_load_agent_opponent_carries_arch(tmp_path, monkeypatch):
    # Регистрируем sampled_muzero TINY-агента с arch в meta → OpponentSpec.arch заполнен
    # через единый resolve_arch_for_algo(meta). Паттерн изоляции registry — как в
    # tests/engine/test_sampled_muzero_registry.py (три monkeypatch, чтобы не писать в реальные артефакты).
    agents_root = tmp_path / "agents"
    registry_path = tmp_path / "agents_registry.json"
    monkeypatch.setattr(agent_registry, "AGENTS_ROOT", str(agents_root))
    monkeypatch.setattr(agent_registry, "AGENTS_REGISTRY_PATH", str(registry_path))
    monkeypatch.setattr(agent_registry, "models_dir", lambda: str(tmp_path))

    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_obs = len(env.get_observation_for_side("model"))
    n_actions = action_sizes_from_env(env, len(env.model))
    tiny = {"latent_dim": 8, "hidden_dim": 8, "num_layers": 1, "action_embed_dim": 8}
    net = make_sampled_muzero_net(n_obs, n_actions, **tiny)

    contract = agent_registry.make_env_contract(
        n_observations=n_obs,
        n_actions=n_actions,
        mission_name="only_war",
    )
    identity = AgentIdentity(side="P1", faction="TestFaction")
    save_agent_artifact(
        identity=identity,
        agent_id="P1_TestFaction_sampled_only_war_v1_test_001",
        env_contract=contract,
        policy_state_dict=normalize_state_dict(net.state_dict()),
        extra_meta={"algo": "sampled_muzero", "arch": dict(tiny)},
    )

    spec = load_agent_opponent(
        agent_id="P1_TestFaction_sampled_only_war_v1_test_001",
        expected_contract=contract,
    )
    assert spec.algo == "sampled_muzero"
    assert isinstance(spec.arch, dict)
    assert spec.arch["latent_dim"] == 8
    assert spec.arch["num_layers"] == 1


# --- Task 4: eval.py (последовательный путь) — честный 1:1 на уровне сборки ---

def test_learner_and_opponent_build_1to1_for_nondefault_arch(tmp_path, monkeypatch):
    # Эмулируем eval-сборку обеих сторон из ОДНОГО registry-агента с недефолтной аркой.
    # Изоляция registry — как в Task 3 (три monkeypatch, чтобы не писать в реальные артефакты).
    monkeypatch.setattr(agent_registry, "AGENTS_ROOT", str(tmp_path / "agents"))
    monkeypatch.setattr(agent_registry, "AGENTS_REGISTRY_PATH", str(tmp_path / "agents_registry.json"))
    monkeypatch.setattr(agent_registry, "models_dir", lambda: str(tmp_path))

    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n_obs = len(env.get_observation_for_side("model"))
    n_actions = action_sizes_from_env(env, len(env.model))
    tiny = {"latent_dim": 8, "hidden_dim": 8, "num_layers": 1, "action_embed_dim": 8}
    net = make_sampled_muzero_net(n_obs, n_actions, **tiny)
    contract = agent_registry.make_env_contract(
        n_observations=n_obs,
        n_actions=n_actions,
        mission_name="only_war",
        ruleset_version="only_war_v2",
    )
    identity = AgentIdentity(side="P2", faction="space_marines", ruleset_version="only_war_v2")
    save_agent_artifact(
        identity=identity,
        agent_id="t-smz",
        env_contract=contract,
        policy_state_dict=normalize_state_dict(net.state_dict()),
        extra_meta={"algo": "sampled_muzero", "arch": dict(tiny)},
    )

    # learner: арка из meta (registry-путь)
    payload = agent_registry.load_agent_by_id("t-smz")
    learner_arch = resolve_arch_for_algo("sampled_muzero", payload["meta"])
    lw: list[str] = []
    build_eval_agent(
        algo="sampled_muzero",
        policy_state=payload["policy_state"],
        contract=contract,
        len_model=len(env.model),
        cfg=resolve_eval_search_cfg("sampled_muzero"),
        arch=learner_arch,
        log_fn=lw.append,
    )
    # opponent: арка из OpponentSpec
    spec = load_agent_opponent(agent_id="t-smz", expected_contract=contract)
    ow: list[str] = []
    build_eval_agent(
        algo=spec.algo,
        policy_state=spec.policy_state,
        contract=spec.contract,
        len_model=len(env.enemy),
        cfg=resolve_eval_search_cfg(spec.algo),
        arch=spec.arch,
        log_fn=ow.append,
    )
    assert not any("missing" in w for w in lw), lw
    assert not any("missing" in w for w in ow), ow
