"""GAZ distributed: паковка GAZ-полей поиска для ПК2 + сборка worker-payload.

Реальный разрыв AZ-distributed для GAZ: на ПК2 уезжали AZ MCTS-параметры, а
GumbelAlphaZeroSearch ждёт num_simulations/num_considered_actions/joint_action и т.д.
Здесь проверяем, что GAZ-поля корректно пакуются в SMB-контекст (pack/normalize
не теряют их) и что build_gaz_dist_worker_payloads даёт GAZ-форму mcts-payload.
"""

from __future__ import annotations

from core.models.az_rollout_sink import (
    az_dist_stop_flag_path,
    build_gaz_dist_worker_payloads,
    normalize_az_dist_hyperparams,
    pack_az_dist_hyperparams,
)

_GAZ_DEFAULTS = {
    "num_simulations": 32,
    "num_considered_actions": 8,
    "max_depth": 1,
    "value_scale": 0.1,
    "c_visit": 50.0,
    "simulate_enemy": False,
    "joint_action": True,
    "eval_cache_size": 10000,
    "batch_eval_size": 16,
    "batch_send": 32,
    "inference_timeout": 5.0,
    "self_play_enabled": 1,
}


def test_pack_preserves_gaz_search_fields():
    src = {
        "num_simulations": 48,
        "num_considered_actions": 4,
        "joint_action": 1,
        "value_scale": 0.2,
        "c_visit": 40.0,
        "simulate_enemy": 0,
        "batch_eval_size": 24,
        "actor_batch_send": 16,
        "inference_timeout": 7.0,
        "self_play_enabled": 1,
    }
    packed = pack_az_dist_hyperparams(src)
    assert packed["num_simulations"] == 48
    assert packed["num_considered_actions"] == 4
    assert packed["joint_action"] == 1
    assert packed["batch_eval_size"] == 24
    # round-trip через normalize (ПК2) не теряет GAZ-поля
    assert normalize_az_dist_hyperparams(packed)["num_simulations"] == 48


def test_build_gaz_payload_uses_pc1_values():
    hp = pack_az_dist_hyperparams({
        "num_simulations": 64,
        "num_considered_actions": 6,
        "joint_action": 1,
        "max_depth": 1,
        "value_scale": 0.15,
        "c_visit": 30.0,
        "simulate_enemy": 0,
        "batch_eval_size": 20,
        "actor_batch_send": 8,
    })
    payloads = build_gaz_dist_worker_payloads(hp, defaults=_GAZ_DEFAULTS)
    mcts = payloads["mcts"]
    assert mcts["num_simulations"] == 64
    assert mcts["num_considered_actions"] == 6
    assert bool(mcts["joint_action"]) is True
    assert mcts["batch_eval_size"] == 20
    assert bool(mcts["simulate_enemy"]) is False
    assert payloads["batch_send"] == 8
    # форма содержит все ключи, которые читает _build_az_search для gumbel_az
    for key in ("num_simulations", "num_considered_actions", "max_depth", "value_scale",
                "c_visit", "eval_cache_size", "batch_eval_size", "simulate_enemy", "joint_action"):
        assert key in mcts


def test_build_gaz_payload_falls_back_to_defaults():
    payloads = build_gaz_dist_worker_payloads({}, defaults=_GAZ_DEFAULTS)
    mcts = payloads["mcts"]
    assert mcts["num_simulations"] == 32
    assert mcts["num_considered_actions"] == 8
    assert bool(mcts["joint_action"]) is True


def test_gaz_stop_flag_name(monkeypatch):
    monkeypatch.delenv("AZ_DIST_STOP_FLAG_PATH", raising=False)
    assert az_dist_stop_flag_path("gumbel_az").endswith("gaz_dist_stop.flag")
    assert az_dist_stop_flag_path("alphazero_tree").endswith("az_dist_stop.flag")
    assert az_dist_stop_flag_path().endswith("az_dist_stop.flag")


def test_gaz_stop_flag_env_override_wins(monkeypatch):
    monkeypatch.setenv("AZ_DIST_STOP_FLAG_PATH", r"X:\custom_stop.flag")
    assert az_dist_stop_flag_path("gumbel_az") == r"X:\custom_stop.flag"
