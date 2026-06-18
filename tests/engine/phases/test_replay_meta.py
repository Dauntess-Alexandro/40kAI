import numpy as np
import pytest

from core.engine.phases.replay_meta import (
    ReplayPhaseMeta,
    az_transition_from_rollout_dict,
    az_transition_to_rollout_dict,
    capture_replay_phase_meta,
    gmz_transition_from_rollout_dict,
    gmz_transition_to_rollout_dict,
    replay_phase_meta_enabled,
)
from core.models.alphazero_replay import AZTransition, AlphaZeroReplayBuffer
from core.models.gumbel_muzero_replay import GMZTransition, GumbelMuZeroReplayBuffer
from tests.engine.phases._helpers import build_env


def test_replay_phase_meta_roundtrip_dict():
    meta = ReplayPhaseMeta(
        phase="movement",
        sub_step="move_unit",
        window_id="movement:model:0",
        chosen_option='{"shoot": 1}',
        stratagem_id="insane_bravery",
        cp_before=2,
        cp_after=1,
    )
    restored = ReplayPhaseMeta.from_dict(meta.to_dict())
    assert restored == meta


def test_az_replay_load_legacy_without_phase_meta():
    rb = AlphaZeroReplayBuffer(capacity=10)
    loaded = rb.load_state_dict(
        {
            "items": [
                {
                    "state": np.zeros(8, dtype=np.float32),
                    "policy_targets": [np.ones(3, dtype=np.float32)],
                    "value_target": 0.5,
                    "policy_version": 2,
                    "faction": "Necrons",
                }
            ]
        }
    )
    assert loaded == 1
    t = rb.buffer[0]
    assert t.phase_meta is None
    assert t.faction == "Necrons"


def test_az_replay_state_dict_roundtrip_with_phase_meta():
    meta = ReplayPhaseMeta(phase="fight", stratagem_id="hungry_void", cp_before=3, cp_after=2)
    rb = AlphaZeroReplayBuffer(capacity=10)
    rb.push(
        AZTransition(
            state=np.zeros(8, dtype=np.float32),
            policy_targets=[np.ones(3, dtype=np.float32)],
            value_target=1.0,
            policy_version=4,
            phase_meta=meta,
        )
    )
    rb2 = AlphaZeroReplayBuffer(capacity=10)
    rb2.load_state_dict(rb.state_dict())
    t = rb2.buffer[0]
    assert t.phase_meta == meta


def test_az_rollout_wire_roundtrip():
    meta = ReplayPhaseMeta(phase="command", stratagem_id="insane_bravery", cp_before=1, cp_after=0)
    t = AZTransition(
        state=np.arange(5, dtype=np.float32),
        policy_targets=[np.full(3, 0.5, dtype=np.float32)],
        value_target=-0.25,
        policy_version=7,
        phase_meta=meta,
    )
    wire = az_transition_to_rollout_dict(t)
    restored = az_transition_from_rollout_dict(wire, default_policy_version=0)
    assert restored is not None
    assert restored.phase_meta == meta
    assert restored.policy_version == 7


def test_gmz_rollout_wire_roundtrip():
    meta = ReplayPhaseMeta(phase="shooting", cp_before=2, cp_after=2)
    t = GMZTransition(
        state=np.zeros(4, dtype=np.float32),
        action=np.array([1, 0, 2], dtype=np.int64),
        reward=0.1,
        done=False,
        policy_targets=[np.ones(2, dtype=np.float32)],
        value_target=0.5,
        policy_version=3,
        phase_meta=meta,
    )
    wire = gmz_transition_to_rollout_dict(t)
    restored = gmz_transition_from_rollout_dict(wire)
    assert restored is not None
    assert restored.phase_meta == meta


def test_capture_replay_phase_meta_from_env(monkeypatch):
    monkeypatch.setenv("REPLAY_PHASE_META", "1")
    assert replay_phase_meta_enabled()
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.phase = "command"
    env.modelCP = 2
    meta = capture_replay_phase_meta(
        env,
        action_dict={"use_cp": 1, "cp_on": 0, "attack": 0},
        cp_before=2,
        phase="command",
    )
    assert meta is not None
    assert meta.phase == "command"
    assert meta.stratagem_id == "insane_bravery"
    assert meta.cp_before == 2


def test_gmz_replay_buffer_legacy_load():
    rb = GumbelMuZeroReplayBuffer(capacity=5)
    rb.load_state_dict(
        {
            "capacity": 5,
            "buffer": [
                {
                    "state": np.zeros(4, dtype=np.float32),
                    "action": np.array([0], dtype=np.int64),
                    "reward": 0.0,
                    "done": False,
                    "policy_targets": [np.ones(2, dtype=np.float32)],
                    "value_target": 0.0,
                    "policy_version": 1,
                }
            ],
        }
    )
    assert len(rb) == 1
    assert rb.buffer[0].phase_meta is None
