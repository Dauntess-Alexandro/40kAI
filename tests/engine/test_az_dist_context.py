from __future__ import annotations

import json
import os

from core.engine.agent_registry import (
    _remap_models_path,
    agents_meta_root,
    collect_registered_agents_meta,
    models_dir,
    resolve_latest_opponent_agent_id,
)
from core.models.az_rollout_sink import (
    apply_az_dist_worker_env,
    az_dist_context_path,
    build_az_dist_worker_payloads,
    build_gaz_dist_worker_payloads,
    normalize_az_dist_hyperparams,
    pack_az_dist_hyperparams,
    read_az_dist_train_context,
    reconcile_dist_opponent,
    write_az_dist_train_context,
)


def test_pack_keeps_phase_obs_and_reaction_flags():
    # ПК2-актёры обязаны совпадать с ПК1 по obs-size и value-гейту → флаги едут в SMB-контекст.
    smb = pack_az_dist_hyperparams({"phase_obs_features": 1, "reaction_value_policy": 1, "noise": 9})
    assert smb["phase_obs_features"] == 1
    assert smb["reaction_value_policy"] == 1
    assert "noise" not in smb


def test_apply_worker_env_propagates_phase_obs_and_reaction(monkeypatch):
    # С ПК1 пришло phase_obs=1, reaction=1 → перекрываем локальные значения ПК2 (obs-size критичен).
    monkeypatch.setenv("PHASE_OBS_FEATURES", "0")
    monkeypatch.setenv("AZ_REACTION_VALUE_POLICY", "0")
    apply_az_dist_worker_env({"phase_obs_features": 1, "reaction_value_policy": 1})
    assert os.environ["PHASE_OBS_FEATURES"] == "1"
    assert os.environ["AZ_REACTION_VALUE_POLICY"] == "1"


def test_apply_worker_env_no_flags_leaves_env_untouched(monkeypatch):
    # Нет флагов в hp (нет SMB-контекста) → не трогаем то, что выставил импорт train на ПК2.
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    monkeypatch.setenv("AZ_REACTION_VALUE_POLICY", "1")
    apply_az_dist_worker_env({})
    assert os.environ["PHASE_OBS_FEATURES"] == "1"
    assert os.environ["AZ_REACTION_VALUE_POLICY"] == "1"


def test_write_and_read_dist_context(tmp_path, monkeypatch):
    sync = tmp_path / "actor_sync"
    sync.mkdir()
    monkeypatch.setenv("AZ_DIST_STOP_FLAG_PATH", str(sync / "az_dist_stop.flag"))
    write_az_dist_train_context({
        "opponent_agent_id": "agent_test",
        "learner_side": "P1",
        "mission": "annihilation",
        "ruleset_version": "annihilation_v2",
        "roster": {"mission": "annihilation"},
        "env_contract_hash": "hash_pc1",
    })
    ctx = read_az_dist_train_context()
    assert ctx["opponent_agent_id"] == "agent_test"
    assert ctx["mission"] == "annihilation"
    assert ctx["ruleset_version"] == "annihilation_v2"
    assert ctx["env_contract_hash"] == "hash_pc1"
    assert az_dist_context_path().endswith("az_dist_train_context.json")


def test_pc2_az_applies_mission_context_before_train_import(monkeypatch):
    from tools.pc2_az_actors import _apply_context_env

    monkeypatch.setenv("MISSION_NAME", "only_war")
    monkeypatch.setenv("RULESET_VERSION", "only_war_v2")
    monkeypatch.setenv("ENV_RULESET_VERSION", "only_war_v2")

    _apply_context_env(
        {"mission": "annihilation", "ruleset_version": "annihilation_v2"},
        log=lambda _msg: None,
    )

    assert os.environ["MISSION_NAME"] == "annihilation"
    assert os.environ["RULESET_VERSION"] == "annihilation_v2"
    assert os.environ["ENV_RULESET_VERSION"] == "annihilation_v2"


def test_pc2_dqn_applies_mission_context_before_train_import(monkeypatch):
    from tools.pc2_dqn_actors import _apply_context_env

    monkeypatch.delenv("MISSION_NAME", raising=False)
    monkeypatch.delenv("RULESET_VERSION", raising=False)
    monkeypatch.delenv("ENV_RULESET_VERSION", raising=False)

    _apply_context_env(
        {"roster": {"mission": "annihilation"}},
        log=lambda _msg: None,
    )

    assert os.environ["MISSION_NAME"] == "annihilation"
    assert os.environ["RULESET_VERSION"] == "annihilation_v2"
    assert os.environ["ENV_RULESET_VERSION"] == "annihilation_v2"


def test_pack_and_pc2_mcts_payload_prefers_smb_hyperparams():
    defaults = {
        "simulations": 32,
        "parallel_simulations": 1,
        "max_depth": 1,
        "batch_eval_size": 16,
        "c_puct": 1.5,
        "c_puct_min": 1.0,
        "c_puct_max": 2.0,
        "c_puct_schedule": "none",
        "dirichlet_alpha": 0.3,
        "dirichlet_eps": 0.25,
        "top_k_per_head": 10,
        "mode": "tree",
        "root_dirichlet_only": True,
        "eval_cache_size": 10000,
        "pw_alpha": 1.0,
        "pw_beta": 0.5,
        "prior_weight_early": 0.25,
        "simulate_enemy_in_tree": True,
        "temperature_opening_moves": 12,
        "temperature_opening_value": 0.9,
        "temperature_late_value": 0.15,
        "outcome_only": True,
        "outcome_value_win": 1.0,
        "outcome_value_loss": -1.0,
        "outcome_value_draw": -0.25,
        "mission_bootstrap_coef": 0.0,
        "batch_send": 32,
        "inference_timeout": 5.0,
        "self_play_enabled": 0,
    }
    smb = pack_az_dist_hyperparams(
        {
            "mcts_parallel_sims": 8,
            "mcts_simulations": 64,
            "mcts_max_depth": 2,
            "mission_bootstrap_coef": 0.05,
            "noise": 999,
        }
    )
    assert "noise" not in smb
    assert smb["mcts_parallel_sims"] == 8
    assert smb["mission_bootstrap_coef"] == 0.05
    payloads = build_az_dist_worker_payloads(smb, defaults=defaults)
    assert payloads["mcts"]["parallel_simulations"] == 8
    assert payloads["mcts"]["simulations"] == 64
    assert payloads["mcts"]["max_depth"] == 2
    assert payloads["outcome"]["mission_bootstrap_coef"] == 0.05
    assert payloads["mcts"]["parallel_simulations"] != defaults["parallel_simulations"]
    empty = normalize_az_dist_hyperparams(None)
    assert empty == {}


def test_pc2_gaz_payload_prefers_smb_mission_bootstrap_coef():
    defaults = {
        "num_simulations": 32,
        "num_considered_actions": 8,
        "max_depth": 1,
        "value_scale": 0.1,
        "c_visit": 50.0,
        "eval_cache_size": 10000,
        "batch_eval_size": 16,
        "simulate_enemy": False,
        "joint_action": False,
        "temperature_opening_moves": 12,
        "temperature_opening_value": 0.9,
        "temperature_late_value": 0.15,
        "outcome_only": True,
        "outcome_value_win": 1.0,
        "outcome_value_loss": -1.0,
        "outcome_value_draw": -0.7,
        "mission_bootstrap_coef": 0.0,
        "batch_send": 32,
        "inference_timeout": 5.0,
        "self_play_enabled": 0,
    }
    smb = pack_az_dist_hyperparams(
        {"num_simulations": 48, "joint_action": 1, "mission_bootstrap_coef": 0.075}
    )
    payloads = build_gaz_dist_worker_payloads(smb, defaults=defaults)
    assert payloads["mcts"]["num_simulations"] == 48
    assert payloads["mcts"]["joint_action"] is True
    assert payloads["outcome"]["mission_bootstrap_coef"] == 0.075


def test_resolve_latest_opponent(tmp_path, monkeypatch):
    agents = tmp_path / "agents" / "a1"
    agents.mkdir(parents=True)
    meta = {
        "agent_id": "snap_old",
        "side": "P2",
        "created_at": "2020-01-01T00:00:00",
        "algo": "ppo",
    }
    (agents / "meta.json").write_text(json.dumps(meta), encoding="utf-8")
    agents2 = tmp_path / "agents" / "a2"
    agents2.mkdir(parents=True)
    meta2 = {
        "agent_id": "snap_new",
        "side": "P2",
        "created_at": "2026-01-01T00:00:00",
        "algo": "alphazero_tree",
    }
    (agents2 / "meta.json").write_text(json.dumps(meta2), encoding="utf-8")
    monkeypatch.setenv("MODELS_DIR", str(tmp_path))
    records = collect_registered_agents_meta()
    assert records[0]["agent_id"] == "snap_new"
    assert resolve_latest_opponent_agent_id(learner_side="P1") == "snap_new"
    assert resolve_latest_opponent_agent_id(learner_side="P2") == ""


def test_remap_models_path_pc1_to_smb(tmp_path, monkeypatch):
    smb = tmp_path / "models"
    agents = smb / "agents" / "P2" / "Necrons" / "agent1"
    agents.mkdir(parents=True)
    policy = agents / "policy.pth"
    policy.write_text("x", encoding="utf-8")
    monkeypatch.setenv("MODELS_DIR", str(smb))
    pc1_path = r"C:\40kAI\artifacts\models\agents\P2\Necrons\agent1\policy.pth"
    assert _remap_models_path(pc1_path) == str(policy)
    assert agents_meta_root() == str(smb / "agents")
    assert models_dir() == str(smb)


def test_reconcile_opponent_stale_to_fresh_warns():
    # ПК2 стартовал раньше ПК1 и прочитал оппонента прошлого прогона (PPO) → берём свежего (DQN) + WARN.
    opp, warn = reconcile_dist_opponent(
        "P2_Necrons_only_war_v2_final_ep3000_20260626_110232",
        {"opponent_agent_id": "P1_Necrons_only_war_v2_final_ep1000_20260626_105022"},
        explicit_opp="",
    )
    assert opp == "P1_Necrons_only_war_v2_final_ep1000_20260626_105022"
    assert warn is not None
    assert "ep3000" in warn and "ep1000" in warn


def test_reconcile_opponent_same_no_warn():
    opp, warn = reconcile_dist_opponent("agent_x", {"opponent_agent_id": "agent_x"}, explicit_opp="")
    assert opp == "agent_x"
    assert warn is None


def test_reconcile_opponent_explicit_wins_and_warns_on_diff():
    # Явный OPPONENT_AGENT_ID (конфиг) приоритетнее контекста, но при расхождении предупреждаем.
    opp, warn = reconcile_dist_opponent("agent_x", {"opponent_agent_id": "agent_y"}, explicit_opp="agent_x")
    assert opp == "agent_x"
    assert warn is not None


def test_reconcile_opponent_explicit_match_no_warn():
    opp, warn = reconcile_dist_opponent("agent_x", {"opponent_agent_id": "agent_x"}, explicit_opp="agent_x")
    assert opp == "agent_x"
    assert warn is None


def test_reconcile_opponent_empty_fresh_keeps_initial():
    # Контекст без оппонента (эвристика/пусто) → оставляем то, что уже резолвили, без WARN.
    opp, warn = reconcile_dist_opponent("agent_x", {}, explicit_opp="")
    assert opp == "agent_x"
    assert warn is None


def test_write_az_remote_search_cfg_payload(tmp_path, monkeypatch):
    """Авто-запись search-cfg для IS на ПК2: корректный payload в actor_sync."""
    import core.models.az_rollout_sink as sink

    share = tmp_path / "actor_sync"
    monkeypatch.setattr(sink, "_actor_sync_dir", lambda: str(share))
    written = sink.write_az_remote_search_cfg(
        obs_dim=17,
        action_sizes=[5, 2, 2, 2, 5, 2, 24, 24],
        hidden_size=256,
        num_layers=2,
        n_value_ensemble=1,
        num_simulations=32,
    )
    share_file = share / "az_remote_search_cfg.json"
    assert str(share_file) in written
    cfg = json.loads(share_file.read_text(encoding="utf-8"))
    assert cfg["obs_dim"] == 17
    assert cfg["action_sizes"] == [5, 2, 2, 2, 5, 2, 24, 24]
    assert cfg["hidden_size"] == 256
    assert cfg["num_layers"] == 2
    assert cfg["n_value_ensemble"] == 1
    assert cfg["num_simulations"] == 32
