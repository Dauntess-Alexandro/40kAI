import math
from contextlib import contextmanager

import numpy as np

import reward_config as reward_cfg
from core.engine.heuristic_targeting import classify_objective_control
from core.envs.warhamEnv import Warhammer40kEnv


@contextmanager
def _patched_reward(**values):
    old = {k: getattr(reward_cfg, k, None) for k in values}
    missing = {k for k in values if not hasattr(reward_cfg, k)}
    try:
        for k, v in values.items():
            setattr(reward_cfg, k, v)
        yield
    finally:
        for k, v in old.items():
            if k in missing:
                delattr(reward_cfg, k)
            else:
                setattr(reward_cfg, k, v)


class _ObjectiveStub:
    _objective_positions_available = Warhammer40kEnv._objective_positions_available
    _enemy_effective_oc = Warhammer40kEnv._enemy_effective_oc
    _enemy_objective_control_score = Warhammer40kEnv._enemy_objective_control_score

    def refresh_objective_control(self):
        return None


class _MovementStub(_ObjectiveStub):
    _enemy_heur_objective_distance = Warhammer40kEnv._enemy_heur_objective_distance
    _enemy_heur_movement_score = Warhammer40kEnv._enemy_heur_movement_score

    b_len = 20
    b_hei = 20
    unit_coords = [[10, 10]]
    unit_health = [10]
    unit_data = [{"W": 5, "T": 4}]
    enemy_health = [5]
    enemy_data = [{"W": 5, "OC": 2}]
    enemyOC = [2]
    enemy_coords = [[0, 0]]
    coordsOfOM = np.array([[5, 5]])
    model_obj_oc = np.array([1])
    enemy_obj_oc = np.array([0])

    def _grid_distance_euclid(self, a, b):
        return math.dist((float(a[0]), float(a[1])), (float(b[0]), float(b[1])))

    def _grid_distance_chebyshev(self, a, b):
        return max(abs(int(a[0]) - int(b[0])), abs(int(a[1]) - int(b[1])))

    def _enemy_heur_exposure_risk(self, enemy_idx, cell_x, cell_y):
        return 0.0

    def _enemy_cell_threat_score(self, cell_x, cell_y):
        return 0.0

    def _enemy_heur_cover_soft_at_cell(self, enemy_idx, cell_x, cell_y):
        return 0.0, "test"

    def _is_position_near_objective(self, pos, radius=5.0):
        return False

    def _enemy_effective_role(self, enemy_idx, target_idx, base_role, risk_norm):
        return base_role, "test"

    def _enemy_phase_profile(self):
        return "mid"


def test_classify_objective_control_kinds():
    cases = [
        ({"model_oc": 5, "enemy_oc_without_unit": 2, "unit_oc": 4, "candidate_in_radius": True}, "flip", 1.0),
        ({"model_oc": 0, "enemy_oc_without_unit": 0, "unit_oc": 2, "candidate_in_radius": True}, "capture", 0.8),
        ({"model_oc": 5, "enemy_oc_without_unit": 2, "unit_oc": 3, "candidate_in_radius": True}, "contest", 0.45),
        ({"model_oc": 2, "enemy_oc_without_unit": 5, "unit_oc": 2, "candidate_in_radius": True}, "hold", 0.25),
        ({"model_oc": 5, "enemy_oc_without_unit": 2, "unit_oc": 4, "candidate_in_radius": False}, "none", 0.0),
        ({"model_oc": 0, "enemy_oc_without_unit": 0, "unit_oc": 0, "candidate_in_radius": True}, "none", 0.0),
    ]
    for kwargs, kind, score in cases:
        res = classify_objective_control(**kwargs)
        assert res["kind"] == kind
        assert res["score"] == score


def test_objective_control_moves_between_objectives_without_sticky_hold():
    stub = _ObjectiveStub()
    stub.coordsOfOM = np.array([[5, 5], [15, 15]])
    stub.enemy_health = [5]
    stub.enemy_data = [{"W": 5}]
    stub.enemyOC = [2]
    stub.enemy_coords = [[5, 5]]
    stub.model_obj_oc = np.array([0, 0])
    stub.enemy_obj_oc = np.array([2, 0])

    res = stub._enemy_objective_control_score(0, 15, 15)

    assert res["objective_idx"] == 1
    assert res["kind"] == "capture"
    assert res["enemy_oc_after"] == 2


def test_objective_control_stay_on_owned_objective_is_hold():
    stub = _ObjectiveStub()
    stub.coordsOfOM = np.array([[5, 5]])
    stub.enemy_health = [5]
    stub.enemy_data = [{"W": 5}]
    stub.enemyOC = [2]
    stub.enemy_coords = [[5, 5]]
    stub.model_obj_oc = np.array([0])
    stub.enemy_obj_oc = np.array([2])

    res = stub._enemy_objective_control_score(0, 5, 5)

    assert res["objective_idx"] == 0
    assert res["kind"] == "hold"
    assert res["score"] == 0.25


def test_movement_score_prefers_flip_when_objective_control_enabled():
    stub = _MovementStub()
    matchup = {"desired_dist": 6.0, "mode": "hold", "enemy_role": "hybrid"}

    with _patched_reward(
        ENEMY_HEUR_OBJECTIVE_CONTROL_ENABLED=1,
        ENEMY_HEUR_OBJECTIVE_CONTROL_W=2.0,
        ENEMY_HEUR_TARGET_DIST_W=0.1,
        ENEMY_HEUR_MATCHUP_DIST_W=0.0,
        ENEMY_HEUR_PROGRESS_W=0.0,
    ):
        flip_score, flip_details = stub._enemy_heur_movement_score(
            enemy_idx=0,
            target_idx=0,
            cell_x=5,
            cell_y=5,
            mode="normal",
            pos_before=(0, 0),
            matchup=matchup,
            focus_count=1,
        )
        near_target_score, near_details = stub._enemy_heur_movement_score(
            enemy_idx=0,
            target_idx=0,
            cell_x=10,
            cell_y=9,
            mode="normal",
            pos_before=(0, 0),
            matchup=matchup,
            focus_count=1,
        )

    assert flip_details["obj_control_kind"] == "flip"
    assert near_details["obj_control_kind"] == "none"
    assert flip_score < near_target_score


def test_movement_score_control_disabled_keeps_distance_only_score():
    stub = _MovementStub()
    matchup = {"desired_dist": 6.0, "mode": "hold", "enemy_role": "hybrid"}

    with _patched_reward(ENEMY_HEUR_OBJECTIVE_CONTROL_ENABLED=0):
        disabled_score, disabled_details = stub._enemy_heur_movement_score(
            enemy_idx=0,
            target_idx=0,
            cell_x=5,
            cell_y=5,
            mode="normal",
            pos_before=(0, 0),
            matchup=matchup,
            focus_count=1,
        )
    with _patched_reward(ENEMY_HEUR_OBJECTIVE_CONTROL_ENABLED=1):
        enabled_score, enabled_details = stub._enemy_heur_movement_score(
            enemy_idx=0,
            target_idx=0,
            cell_x=5,
            cell_y=5,
            mode="normal",
            pos_before=(0, 0),
            matchup=matchup,
            focus_count=1,
        )

    assert disabled_details["obj_control_score"] == 0.0
    assert enabled_details["obj_control_kind"] == "flip"
    assert enabled_score < disabled_score
