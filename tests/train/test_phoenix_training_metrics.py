from __future__ import annotations

import json
from pathlib import Path


def test_phoenix_training_metrics_write_gui_data_json(tmp_path, monkeypatch):
    import train

    models_dir = tmp_path / "models"
    metrics_dir = tmp_path / "metrics"
    runtime_img_dir = tmp_path / "runtime" / "state" / "img"
    model_path = models_dir / "P1_Necrons_annihilation_v2_final_ep3_test"

    monkeypatch.setattr(train, "MODELS_DIR", str(models_dir))
    monkeypatch.setattr(train, "METRICS_DIR", str(metrics_dir))
    monkeypatch.setattr(train, "RUNTIME_IMG_DIR", str(runtime_img_dir))
    monkeypatch.setattr(train, "append_agent_log", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(train, "save_training_summary", lambda *_args, **_kwargs: None)

    ep_rows = [
        {
            "episode": 1,
            "actor_idx": 0,
            "ep_reward": 1.0,
            "ep_len": 7,
            "turn": 7,
            "model_vp": 3,
            "player_vp": 1,
            "vp_diff": 2,
            "result": "win",
            "end_reason": "wipeout_enemy",
            "opponent_label": "PPO:ep4000",
            "opponent_agent_id": "P2_Necrons_annihilation_v2_ep4000_test",
        },
        {
            "episode": 2,
            "actor_idx": 1,
            "opponent_label": "heuristic",
            "ep_reward": 0.5,
            "ep_len": 8,
            "turn": 8,
            "model_vp": 2,
            "player_vp": 2,
            "vp_diff": 0,
            "result": "draw",
            "end_reason": "turn_limit",
        },
        {
            "episode": 3,
            "actor_idx": 0,
            "ep_reward": -0.25,
            "ep_len": 9,
            "turn": 9,
            "model_vp": 1,
            "player_vp": 3,
            "vp_diff": -2,
            "result": "loss",
            "end_reason": "wipeout_model",
        },
    ]

    data_path = train.save_phoenix_training_metrics(
        run_id="1234567",
        ep_rows=ep_rows,
        loss_values=[1.25, 0.75, 0.5],
        model_path=str(model_path),
        mode="actor_learner",
        learner_identity=train.AgentIdentity(side="P1", faction="Necrons", ruleset_version="annihilation_v2"),
        roster_config={"enemy_faction": "Necrons"},
        num_actors=2,
        elapsed_s=1.5,
    )

    assert data_path == str(models_dir / "data_1234567.json")
    payload = json.loads(Path(data_path).read_text(encoding="utf-8"))
    latest = json.loads((models_dir / "data_latest.json").read_text(encoding="utf-8"))

    assert payload == latest
    assert payload["algo"] == "phoenix"
    assert payload["mode"] == "actor_learner"
    assert payload["num_actors"] == 2
    assert payload["reward"] == "img/reward_1234567.png"
    assert payload["loss"] == "img/loss_1234567.png"
    assert payload["epLen"] == "img/epLen_1234567.png"
    assert payload["winrate"] == "img/winrate_1234567.png"
    assert payload["opponent_source"] == "pool"
    assert payload["opponent_algo"] == "pool"

    assert (metrics_dir / "stats_1234567.csv").exists()
    assert (runtime_img_dir / "reward_1234567.png").exists()
    assert (runtime_img_dir / "loss_1234567.png").exists()
    assert (runtime_img_dir / "epLen_1234567.png").exists()
    assert (runtime_img_dir / "winrate_1234567.png").exists()
