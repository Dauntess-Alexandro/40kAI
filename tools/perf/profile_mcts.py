#!/usr/bin/env python3
"""MCTS rollout profiler — Sprint 1 baseline measurement tool.

Measures wall-clock time for each bottleneck in AlphaZeroFactorizedMCTS:
  - snapshot_state / restore_state
  - _evaluate_net (network forward pass)
  - env.step
  - enemyTurn
  - full MCTS run (simulations=64, mode='tree')

Results are printed to stdout and optionally appended to
runtime/logs/LOGS_FOR_AGENTS_TRAIN.md.

Usage (from repo root, venv activated):
    python tools/perf/profile_mcts.py
    python tools/perf/profile_mcts.py --simulations 64 --moves 20 --append-log
    python tools/perf/profile_mcts.py --cprofile
"""
from __future__ import annotations

import argparse
import cProfile
import io
import os
import pstats
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import torch

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

os.environ.setdefault("TORCHDYNAMO_DISABLE", "1")
os.environ.setdefault("TORCH_COMPILE_DISABLE", "1")
os.environ.setdefault("AGENT_LOG_FILE", "runtime/logs/LOGS_FOR_AGENTS_TRAIN.md")

from core.models.action_contract import ordered_action_keys
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.alphazero_model import AlphaZeroPolicyValueNet, make_alphazero_net


# ---------------------------------------------------------------------------
# Heavy fake env: mimics real Warhammer40kEnv snapshot state size
# ---------------------------------------------------------------------------

class _HeavyFakeEnv:
    """Fake env whose snapshot_state/restore_state mimics real env cost.

    State includes:
    - board (60×40 numpy array)
    - coords/health lists for 4 model + 4 enemy units
    - distance/target caches (dicts with ~200 entries each)
    - misc flags/counters matching warhamEnv.py keys
    """

    def __init__(self, n_obs: int, n_actions: list[int], len_model: int, board_x: int = 60, board_y: int = 40):
        self.n_obs = int(n_obs)
        self.n_actions = list(n_actions)
        self.len_model = int(len_model)
        self.n_enemy = len_model  # symmetric for profiling
        self.unwrapped = self
        self.game_over = False
        self._last_info: dict[str, Any] = {"winner": "", "end reason": ""}
        self._step_counter = 0
        self._simulation_mode_depth = 0

        # Mimic real env state
        self.board = np.zeros((board_x, board_y), dtype=np.float32)
        self.unit_coords = [[float(i * 5), float(i * 3)] for i in range(len_model)]
        self.enemy_coords = [[float(i * 5 + 1), float(i * 3 + 1)] for i in range(self.n_enemy)]
        self.unit_health = [10.0] * len_model
        self.enemy_health = [10.0] * self.n_enemy
        self.unit_model_wounds = [[1] * 3 for _ in range(len_model)]
        self.enemy_model_wounds = [[1] * 3 for _ in range(self.n_enemy)]
        self.unit_anchor_coords = [[float(i), float(i)] for i in range(len_model)]
        self.enemy_anchor_coords = [[float(i), float(i)] for i in range(self.n_enemy)]
        self.unit_model_positions = [[[float(j), float(j)] for j in range(3)] for _ in range(len_model)]
        self.enemy_model_positions = [[[float(j), float(j)] for j in range(3)] for _ in range(self.n_enemy)]
        self.model_used_advance = [False] * len_model
        self.enemy_used_advance = [False] * self.n_enemy
        self.model_advance_roll = [None] * len_model
        self.enemy_advance_roll = [None] * self.n_enemy
        self.unitInAttack = [[0, 0]] * len_model
        self.enemyInAttack = [[0, 0]] * self.n_enemy
        self.unitFellBack = [False] * len_model
        self.enemyFellBack = [False] * self.n_enemy
        self.unitCharged = [0] * len_model
        self.enemyCharged = [0] * self.n_enemy
        self.game_over = False
        self.trunc = False
        self.iter = 0
        self.restarts = 0
        self.playType = False
        self._state_flush_last_ts = 0.0
        self._state_flush_pending = False
        self.enemyCP = 0
        self.modelCP = 0
        self.enemyOverwatch = -1
        self.modelStrat = {"overwatch": -1, "smokescreen": -1}
        self.enemyStrat = {"overwatch": -1, "smokescreen": -1}
        self.modelVP = 0
        self.enemyVP = 0
        self.battle_round = 1
        self.active_side = "model"
        self.phase = "command"
        self.numTurns = 1
        self.turn_order = ["enemy", "model"]
        self._round_banner_shown = False
        self._fight_env_logged = False
        self._phase_event_emitted = False
        self._phase_unit_logged: set = set()
        self._prev_vp_diff = 0
        self._objective_hold_streaks = [0, 0, 0]
        self._target_cache_epoch = 0
        self._last_action_signature = None
        self._action_repeat_streak = 0
        self._terrain_shaping_shot_bonus_units: set = set()
        self.last_end_reason = ""
        self.last_winner = ""
        self.current_action_index = 0
        self.viewer_step_seq = 0
        self.viewer_activation = False
        self.viewer_awaiting_ack = False
        self.modelUpdates = ""

        # Caches: large dicts to mimic real env cost
        self._distance_cache = {(i, j): float(i + j) for i in range(20) for j in range(10)}
        self._shoot_target_cache = {i: list(range(3)) for i in range(50)}
        self._shoot_target_reject_cache = {i: list(range(2)) for i in range(30)}

    def get_legal_action_masks_by_head(self, side: str = "model"):
        keys = ordered_action_keys(self.len_model)
        masks = {}
        for i, k in enumerate(keys):
            m = np.ones(self.n_actions[i], dtype=bool)
            masks[k] = m
        return masks

    @contextmanager
    def simulation_mode(self):
        self._simulation_mode_depth += 1
        try:
            yield self
        finally:
            self._simulation_mode_depth = max(0, self._simulation_mode_depth - 1)

    def snapshot_state(self) -> dict:
        """Slim snapshot matching the optimised warhamEnv implementation."""
        snap: dict[str, Any] = {
            "_random_state": None,
            "_np_random_state": None,
            "_simulation_mode_depth": int(self._simulation_mode_depth),
            "_model_unit_coords": [list(c) for c in self.unit_coords],
            "_enemy_unit_coords": [list(c) for c in self.enemy_coords],
            # scalars
            "iter": self.iter, "restarts": self.restarts, "playType": self.playType,
            "_state_flush_last_ts": self._state_flush_last_ts,
            "_state_flush_pending": self._state_flush_pending,
            "game_over": self.game_over, "trunc": self.trunc,
            "enemyCP": self.enemyCP, "modelCP": self.modelCP,
            "enemyOverwatch": self.enemyOverwatch,
            "modelVP": self.modelVP, "enemyVP": self.enemyVP,
            "battle_round": self.battle_round, "active_side": self.active_side,
            "phase": self.phase, "numTurns": self.numTurns,
            "_round_banner_shown": self._round_banner_shown,
            "_fight_env_logged": self._fight_env_logged,
            "_phase_event_emitted": self._phase_event_emitted,
            "_prev_vp_diff": self._prev_vp_diff,
            "_target_cache_epoch": self._target_cache_epoch,
            "_last_action_signature": self._last_action_signature,
            "_action_repeat_streak": self._action_repeat_streak,
            "last_end_reason": self.last_end_reason, "last_winner": self.last_winner,
            "current_action_index": self.current_action_index,
            "viewer_step_seq": self.viewer_step_seq,
            "viewer_activation": self.viewer_activation,
            "viewer_awaiting_ack": self.viewer_awaiting_ack,
            "modelUpdates": self.modelUpdates,
        }
        # numpy board
        snap["board"] = self.board.copy()
        # 1-D scalar lists
        for k in ("unit_health", "enemy_health", "model_used_advance", "enemy_used_advance",
                  "model_advance_roll", "enemy_advance_roll", "unitFellBack", "enemyFellBack",
                  "unitCharged", "enemyCharged", "_objective_hold_streaks", "turn_order"):
            snap[k] = list(getattr(self, k))
        # 2-D coord lists
        for k in ("unit_coords", "enemy_coords", "unit_anchor_coords", "enemy_anchor_coords",
                  "unitInAttack", "enemyInAttack"):
            snap[k] = [list(p) for p in getattr(self, k)]
        # 2-D wounds
        for k in ("unit_model_wounds", "enemy_model_wounds"):
            snap[k] = [list(w) for w in getattr(self, k)]
        # 3-D positions
        for k in ("unit_model_positions", "enemy_model_positions"):
            snap[k] = [[list(pos) for pos in up] for up in getattr(self, k)]
        # dicts of scalars
        snap["modelStrat"] = dict(self.modelStrat)
        snap["enemyStrat"] = dict(self.enemyStrat)
        # sets
        snap["_phase_unit_logged"] = set(self._phase_unit_logged)
        snap["_terrain_shaping_shot_bonus_units"] = set(self._terrain_shaping_shot_bonus_units)
        # Cache dicts intentionally NOT stored.
        return snap

    def restore_state(self, snapshot: dict) -> None:
        """Slim restore matching the optimised warhamEnv implementation."""
        _SCALAR_KEYS = (
            "iter", "restarts", "playType", "_state_flush_last_ts", "_state_flush_pending",
            "game_over", "trunc", "enemyCP", "modelCP", "enemyOverwatch",
            "modelVP", "enemyVP", "battle_round", "active_side", "phase", "numTurns",
            "_round_banner_shown", "_fight_env_logged", "_phase_event_emitted",
            "_prev_vp_diff", "_target_cache_epoch",
            "_last_action_signature", "_action_repeat_streak",
            "last_end_reason", "last_winner", "current_action_index",
            "viewer_step_seq", "viewer_activation", "viewer_awaiting_ack",
            "modelUpdates",
        )
        for k in _SCALAR_KEYS:
            if k in snapshot:
                setattr(self, k, snapshot[k])
        if "board" in snapshot:
            b = snapshot["board"]
            self.board = b.copy() if isinstance(b, np.ndarray) else b
        for k in ("unit_health", "enemy_health", "model_used_advance", "enemy_used_advance",
                  "model_advance_roll", "enemy_advance_roll", "unitFellBack", "enemyFellBack",
                  "unitCharged", "enemyCharged", "_objective_hold_streaks", "turn_order"):
            if k in snapshot:
                setattr(self, k, list(snapshot[k]))
        for k in ("unit_coords", "enemy_coords", "unit_anchor_coords", "enemy_anchor_coords",
                  "unitInAttack", "enemyInAttack"):
            if k in snapshot:
                setattr(self, k, [list(p) for p in snapshot[k]])
        for k in ("unit_model_wounds", "enemy_model_wounds"):
            if k in snapshot:
                setattr(self, k, [list(w) for w in snapshot[k]])
        for k in ("unit_model_positions", "enemy_model_positions"):
            if k in snapshot:
                setattr(self, k, [[list(pos) for pos in up] for up in snapshot[k]])
        for k in ("modelStrat", "enemyStrat"):
            if k in snapshot:
                setattr(self, k, dict(snapshot[k]))
        for k in ("_phase_unit_logged", "_terrain_shaping_shot_bonus_units"):
            if k in snapshot:
                setattr(self, k, set(snapshot[k]))
        # Caches cleared (not restored — derived data rebuilt on demand)
        self._distance_cache.clear()
        self._shoot_target_cache.clear()
        self._shoot_target_reject_cache.clear()
        self._simulation_mode_depth = int(snapshot.get("_simulation_mode_depth", 0) or 0)

    def step(self, action_dict):
        self._step_counter += 1
        self.iter += 1
        done = self._step_counter >= 3
        if done:
            self.game_over = True
            self._last_info = {"winner": "model", "end reason": "wipeout_enemy"}
        else:
            self._last_info = {"winner": "", "end reason": ""}
        obs = np.zeros(self.n_obs, dtype=np.float32)
        return obs, 0.1, done, False, dict(self._last_info)

    def enemyTurn(self, trunc=False, policy_fn=None):
        # simulate minimal enemy work
        self.active_side = "enemy"
        self._step_counter += 1

    def get_info(self) -> dict:
        return dict(self._last_info)


# ---------------------------------------------------------------------------
# Timing utilities
# ---------------------------------------------------------------------------

class _Timer:
    def __init__(self) -> None:
        self._times: dict[str, list[float]] = {}

    @contextmanager
    def section(self, name: str):
        t0 = time.perf_counter()
        yield
        dt = time.perf_counter() - t0
        self._times.setdefault(name, []).append(dt)

    def stats(self, name: str) -> dict[str, float]:
        vals = self._times.get(name, [])
        if not vals:
            return {"n": 0, "mean_ms": 0.0, "total_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0}
        arr = sorted(vals)
        n = len(arr)
        total = sum(arr)
        return {
            "n": n,
            "mean_ms": total / n * 1000.0,
            "total_ms": total * 1000.0,
            "min_ms": arr[0] * 1000.0,
            "max_ms": arr[-1] * 1000.0,
            "p50_ms": arr[n // 2] * 1000.0,
            "p95_ms": arr[min(n - 1, int(n * 0.95))] * 1000.0,
        }

    def all_names(self) -> list[str]:
        return list(self._times.keys())


# ---------------------------------------------------------------------------
# Instrumented snapshot/restore
# ---------------------------------------------------------------------------

def _bench_snapshot_restore(env: _HeavyFakeEnv, n: int, timer: _Timer) -> None:
    """Take n snapshots and restores, recording time per section."""
    for _ in range(n):
        with timer.section("snapshot_state"):
            snap = env.snapshot_state()
        with timer.section("restore_state"):
            env.restore_state(snap)


def _legacy_snapshot(env: _HeavyFakeEnv) -> dict:
    """Legacy deepcopy snapshot (pre-Sprint-2 approach) for comparison."""
    import copy as _copy
    keys = [
        "iter", "restarts", "playType", "_state_flush_last_ts", "_state_flush_pending",
        "board", "unit_coords", "enemy_coords", "unit_health", "enemy_health",
        "unit_model_wounds", "enemy_model_wounds",
        "unit_anchor_coords", "enemy_anchor_coords",
        "unit_model_positions", "enemy_model_positions",
        "model_used_advance", "enemy_used_advance", "model_advance_roll", "enemy_advance_roll",
        "game_over", "unitInAttack", "enemyInAttack", "trunc",
        "enemyCP", "modelCP", "enemyOverwatch", "modelStrat", "enemyStrat",
        "unitFellBack", "enemyFellBack",
        "modelVP", "enemyVP", "battle_round", "active_side", "phase", "numTurns", "turn_order",
        "_round_banner_shown", "_fight_env_logged", "_phase_event_emitted", "_phase_unit_logged",
        "_prev_vp_diff", "_objective_hold_streaks", "_target_cache_epoch",
        "_distance_cache", "_shoot_target_cache", "_shoot_target_reject_cache",
        "_terrain_shaping_shot_bonus_units",
        "_last_action_signature", "_action_repeat_streak",
        "last_end_reason", "last_winner", "current_action_index",
        "viewer_step_seq", "viewer_activation", "viewer_awaiting_ack",
        "unitCharged", "enemyCharged", "modelUpdates",
    ]
    snap: dict = {
        "_random_state": None,
        "_np_random_state": None,
        "_simulation_mode_depth": int(getattr(env, "_simulation_mode_depth", 0) or 0),
        "_model_unit_coords": [list(c) for c in env.unit_coords],
        "_enemy_unit_coords": [list(c) for c in env.enemy_coords],
    }
    for key in keys:
        if hasattr(env, key):
            snap[key] = _copy.deepcopy(getattr(env, key))
    return snap


def _bench_compare_snapshot(env: _HeavyFakeEnv, n: int) -> tuple[float, float]:
    """Return (slim_ms, legacy_ms) per-call averages."""
    import copy as _copy

    # warm up
    for _ in range(5):
        s = env.snapshot_state()
        env.restore_state(s)
        _ = _legacy_snapshot(env)

    t0 = time.perf_counter()
    for _ in range(n):
        s = env.snapshot_state()
        env.restore_state(s)
    slim_ms = (time.perf_counter() - t0) / n * 1000.0

    t1 = time.perf_counter()
    for _ in range(n):
        _ = _legacy_snapshot(env)
    legacy_ms = (time.perf_counter() - t1) / n * 1000.0

    return slim_ms, legacy_ms


# ---------------------------------------------------------------------------
# Instrumented MCTS run
# ---------------------------------------------------------------------------

class _InstrumentedMCTS(AlphaZeroFactorizedMCTS):
    """Wraps AlphaZeroFactorizedMCTS to time _evaluate_net calls."""

    def __init__(self, *args, timer: _Timer, **kwargs):
        super().__init__(*args, **kwargs)
        self._timer = timer
        self._eval_count = 0

    def _evaluate_net(self, obs, legal_masks_by_head):
        with self._timer.section("_evaluate_net"):
            result = super()._evaluate_net(obs=obs, legal_masks_by_head=legal_masks_by_head)
        self._eval_count += 1
        return result


def _bench_mcts_run(
    env: _HeavyFakeEnv,
    net: AlphaZeroPolicyValueNet,
    n_moves: int,
    simulations: int,
    timer: _Timer,
    device: torch.device,
) -> float:
    """Run MCTS for n_moves moves, timing each section. Returns total seconds."""
    mcts = _InstrumentedMCTS(
        net,
        config=MCTSConfig(simulations=simulations, c_puct=1.5, top_k_per_head=6, mode="tree", max_depth=1),
        device=device,
        timer=timer,
    )
    len_model = env.len_model
    ordered = ordered_action_keys(len_model)
    obs = np.zeros(env.n_obs, dtype=np.float32)
    env._step_counter = 0
    env.game_over = False

    t_total = time.perf_counter()
    for _ in range(n_moves):
        if env.game_over:
            env._step_counter = 0
            env.game_over = False
        legal_dict = env.get_legal_action_masks_by_head("model")
        legal = [legal_dict[k] for k in ordered]
        with timer.section("mcts_run_total"):
            pi, act, val = mcts.run(
                obs=obs,
                legal_masks_by_head=legal,
                temperature=1.0,
                env=env,
                len_model=len_model,
            )
        # simulate step
        from core.models.action_contract import action_tensor_to_dict
        action_dict = action_tensor_to_dict(
            torch.tensor([act], dtype=torch.long), len_model=len_model
        )
        obs, _, done, _, _ = env.step(action_dict)
        if not done:
            with timer.section("enemyTurn"):
                env.enemyTurn()
        if env.game_over:
            obs = np.zeros(env.n_obs, dtype=np.float32)
            env._step_counter = 0
            env.game_over = False

    return time.perf_counter() - t_total


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def _format_report(
    args: argparse.Namespace,
    timer: _Timer,
    total_elapsed: float,
    n_snapshot_iters: int,
) -> str:
    lines = [
        "",
        "## [MCTS-PERF] Baseline профилирование",
        f"**Дата:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Параметры:** simulations={args.simulations}, moves={args.moves}, "
        f"snapshot_iters={n_snapshot_iters}, device={args.device}",
        "",
        "### Snapshot / Restore (изолированный бенчмарк)",
    ]
    for name in ("snapshot_state", "restore_state"):
        s = timer.stats(name)
        if s["n"] > 0:
            lines.append(
                f"- **{name}**: n={s['n']}  mean={s['mean_ms']:.2f}ms  "
                f"p50={s['p50_ms']:.2f}ms  p95={s['p95_ms']:.2f}ms  "
                f"min={s['min_ms']:.2f}ms  max={s['max_ms']:.2f}ms  total={s['total_ms']:.1f}ms"
            )
    lines.append("")
    lines.append("### MCTS run (tree mode, nested profiling)")
    for name in ("mcts_run_total", "_evaluate_net", "enemyTurn"):
        s = timer.stats(name)
        if s["n"] > 0:
            lines.append(
                f"- **{name}**: n={s['n']}  mean={s['mean_ms']:.2f}ms  "
                f"p50={s['p50_ms']:.2f}ms  p95={s['p95_ms']:.2f}ms  total={s['total_ms']:.1f}ms"
            )
    # Derived: snapshot/restore inside MCTS (snapshot called inside _run_tree)
    snap_s = timer.stats("snapshot_state")
    eval_s = timer.stats("_evaluate_net")
    mcts_s = timer.stats("mcts_run_total")
    if mcts_s["n"] > 0 and eval_s["n"] > 0:
        eval_share = eval_s["total_ms"] / max(1.0, mcts_s["total_ms"]) * 100.0
        lines.append(f"\n- **_evaluate_net share of mcts_run_total:** {eval_share:.1f}%")
    if mcts_s["n"] > 0 and snap_s["n"] > 0:
        snap_share = snap_s["total_ms"] / max(1.0, mcts_s["total_ms"]) * 100.0
        lines.append(f"- **snapshot_state share of mcts_run_total:** {snap_share:.1f}%")

    lines.append("")
    lines.append(f"**Итого elapsed:** {total_elapsed:.2f}s  "
                 f"ms/move={total_elapsed / max(1, args.moves) * 1000:.1f}ms")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="MCTS rollout profiler (Sprint 1 baseline).")
    parser.add_argument("--simulations", type=int, default=64, help="MCTS simulations per move.")
    parser.add_argument("--moves", type=int, default=10, help="Moves to simulate.")
    parser.add_argument("--snapshot-iters", type=int, default=200, help="Isolated snapshot/restore iterations.")
    parser.add_argument("--device", type=str, default="cpu", help="torch device.")
    parser.add_argument("--append-log", action="store_true", help="Append results to LOGS_FOR_AGENTS_TRAIN.md.")
    parser.add_argument("--cprofile", action="store_true", help="Also run cProfile on MCTS runs.")
    parser.add_argument("--n-obs", type=int, default=64, help="Observation dimension.")
    parser.add_argument("--len-model", type=int, default=3, help="Number of model units.")
    args = parser.parse_args()

    device = torch.device(args.device)
    len_model = args.len_model
    n_obs = args.n_obs
    n_actions = [5, 2, len_model + 1, len_model + 1, 5, len_model] + [24] * len_model

    print(f"[MCTS-PERF] Инициализация: n_obs={n_obs}, len_model={len_model}, n_actions={n_actions}")
    env = _HeavyFakeEnv(n_obs=n_obs, n_actions=n_actions, len_model=len_model)
    net = make_alphazero_net(n_obs, n_actions, hidden_size=128, num_layers=2)
    net = net.to(device)
    net.eval()

    timer = _Timer()

    # --- Sprint 2 comparison: slim vs legacy deepcopy ---
    print(f"[MCTS-PERF] Сравнение slim vs legacy deepcopy ({args.snapshot_iters} итераций)...")
    slim_ms, legacy_ms = _bench_compare_snapshot(env, args.snapshot_iters)
    ratio = legacy_ms / max(slim_ms, 1e-9)
    print(f"  slim   snapshot+restore: {slim_ms:.3f} ms/call")
    print(f"  legacy deepcopy:         {legacy_ms:.3f} ms/call  (ratio={ratio:.2f}x)")

    # --- Sprint 1a: isolated snapshot/restore bench ---
    print(f"[MCTS-PERF] Бенчмарк snapshot/restore ({args.snapshot_iters} итераций)...")
    _bench_snapshot_restore(env, args.snapshot_iters, timer)
    snap_s = timer.stats("snapshot_state")
    rest_s = timer.stats("restore_state")
    print(f"  snapshot_state:  mean={snap_s['mean_ms']:.2f}ms  p95={snap_s['p95_ms']:.2f}ms")
    print(f"  restore_state:   mean={rest_s['mean_ms']:.2f}ms  p95={rest_s['p95_ms']:.2f}ms")

    # --- Sprint 1b: cProfile on snapshot if requested ---
    if args.cprofile:
        print("[MCTS-PERF] cProfile: snapshot_state ×100...")
        pr = cProfile.Profile()
        pr.enable()
        for _ in range(100):
            snap = env.snapshot_state()
            env.restore_state(snap)
        pr.disable()
        stream = io.StringIO()
        pstats.Stats(pr, stream=stream).sort_stats("cumulative").print_stats(20)
        print(stream.getvalue())

    # --- Sprint 1c: MCTS profiling ---
    print(f"[MCTS-PERF] MCTS run: simulations={args.simulations}, moves={args.moves}...")
    if args.cprofile:
        pr2 = cProfile.Profile()
        pr2.enable()

    total_elapsed = _bench_mcts_run(env, net, args.moves, args.simulations, timer, device)

    if args.cprofile:
        pr2.disable()
        stream2 = io.StringIO()
        pstats.Stats(pr2, stream=stream2).sort_stats("cumulative").print_stats(30)
        print("[MCTS-PERF] cProfile MCTS:")
        print(stream2.getvalue())

    report = _format_report(args, timer, total_elapsed, args.snapshot_iters)
    report += (
        f"\n### Sprint 2 — slim vs legacy deepcopy comparison\n"
        f"- slim snapshot+restore: **{slim_ms:.3f} ms/call**\n"
        f"- legacy deepcopy: **{legacy_ms:.3f} ms/call**\n"
        f"- Speedup: **{ratio:.2f}x**\n"
    )
    print(report)

    if args.append_log:
        log_path = _REPO_ROOT / "runtime" / "logs" / "LOGS_FOR_AGENTS_TRAIN.md"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(report)
        print(f"[MCTS-PERF] Результаты записаны в {log_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
