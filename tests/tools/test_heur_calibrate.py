import argparse
import json

import pytest

import tools.heur_calibrate as hc


def _args(**overrides):
    base = dict(
        candidates=3,
        games=5,
        seed=1390520,
        model="",
        learner_agent_id="",
        learner_side="",
        opponent_agent_id="",
        opponent_policy="heuristic_auto",
        run_id="test_phase8",
        top_k=2,
        dry_run=True,
    )
    base.update(overrides)
    return argparse.Namespace(**base)


def test_candidates_are_deterministic_and_baseline_first():
    baseline = hc.current_weight_vector()
    a = hc.generate_candidates(3, seed=123, baseline=baseline)
    b = hc.generate_candidates(3, seed=123, baseline=baseline)
    assert a == b
    assert a[0] == baseline
    assert "ENEMY_HEUR_THREAT_W" not in a[0]


def test_overrides_json_is_validated():
    cand = {"ENEMY_HEUR_OBJECTIVE_CONTROL_W": 0.5}
    hc.validate_overrides(cand)
    payload = json.loads(hc.overrides_json(cand))
    assert payload == cand


def test_reject_guardrails():
    metrics = {
        "actual_games": 5,
        "heur_winrate": 0.57,
        "draw_rate": 0.04,
        "style_entropy_norm": 0.80,
        "invalid_rate": 0.01,
        "fallback_rate": 0.03,
    }
    reasons = hc.reject_reasons(metrics, requested_games=5)
    assert "heur_winrate > 0.56" in reasons
    assert "style_entropy_norm < 0.84" in reasons
    assert "invalid_rate > 0.001" in reasons


def test_latest_resolves_to_latest_p1(monkeypatch):
    monkeypatch.setattr(
        hc,
        "collect_registered_agents_meta",
        lambda: [
            {"agent_id": "P2_old", "side": "P2"},
            {"agent_id": "P1_new", "side": "P1"},
        ],
    )
    assert hc.resolve_learner_agent_id("latest") == "P1_new"


def test_latest_missing_is_clear(monkeypatch):
    monkeypatch.setattr(hc, "collect_registered_agents_meta", lambda: [])
    with pytest.raises(RuntimeError, match="learner-agent-id=latest"):
        hc.resolve_learner_agent_id("latest")


def test_dry_run_writes_without_subprocess(monkeypatch, tmp_path):
    monkeypatch.setattr(hc, "ARTIFACTS_METRICS_DIR", tmp_path)
    monkeypatch.setattr(hc, "run_benchmark", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("no subprocess")))

    summary = hc.run_calibration(_args())

    assert summary["dry_run"] is True
    run_dir = tmp_path / "heur_calibration" / "test_phase8"
    assert (run_dir / "candidates.jsonl").exists()
    assert (run_dir / "summary.json").exists()
    assert (run_dir / "best_reward_config_patch.md").exists()
    lines = [line for line in (run_dir / "candidates.jsonl").read_text(encoding="utf-8").splitlines() if line]
    assert len(lines) == 3
    assert json.loads(lines[0])["status"] == "dry_run"
