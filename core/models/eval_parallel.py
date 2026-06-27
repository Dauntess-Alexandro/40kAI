from __future__ import annotations

import os
import traceback
from dataclasses import dataclass, field
from typing import Any

from core.models.eval_result import WorkerError


@dataclass
class EvalWorkerConfig:
    learner_agent_id: str
    opponent_agent_id: str = ""
    learner_side: str = "P1"
    mission_name: str = "only_war"
    ruleset_version: str = ""
    model_path: str = ""
    base_seed: int = 0
    trace_enabled: bool = True
    trace_style: str = "warhammer"
    env_overrides: dict[str, str] = field(default_factory=dict)


def eval_worker_entry(worker_id: int, cfg: EvalWorkerConfig, jobs: list[tuple[int, int]], result_q: Any, stop_ev: Any) -> None:
    """Spawn-safe eval worker entry.

    Импорт `eval.py` делаем лениво внутри процесса, чтобы не создавать import-cycle
    при обычном запуске и не пытаться pickle'ить сети родителя.
    """
    game_idx: int | None = None
    try:
        for key, value in dict(cfg.env_overrides or {}).items():
            os.environ[str(key)] = str(value)
        os.environ["EVAL_ACTION_TRACE"] = "1" if bool(cfg.trace_enabled) else "0"
        os.environ["EVAL_TRACE_STYLE"] = str(cfg.trace_style or "warhammer")
        os.environ["LEARNER_SIDE"] = str(cfg.learner_side or "P1")
        if cfg.mission_name:
            os.environ["MISSION_NAME"] = str(cfg.mission_name)
        if cfg.ruleset_version:
            os.environ["RULESET_VERSION"] = str(cfg.ruleset_version)

        import eval as eval_mod  # noqa: PLC0415

        runtime = eval_mod._build_eval_runtime_for_worker(cfg)
        for game_idx, seed in list(jobs or []):
            if stop_ev is not None and stop_ev.is_set():
                break
            result = eval_mod.run_episode(
                runtime["env"],
                runtime["model_units"],
                runtime["enemy_units"],
                runtime["learner_agent"],
                runtime["opponent_agent"],
                runtime["device"],
                learner_side=str(cfg.learner_side or "P1"),
                seed=int(seed),
            )
            result_q.put((int(game_idx), result))
    except BaseException as exc:  # noqa: BLE001 - worker must report everything to parent.
        tb_tail = "".join(traceback.format_exc(limit=12))
        result_q.put(
            WorkerError(
                worker_id=int(worker_id),
                game_idx=game_idx,
                message=(
                    f"Воркер eval упал: {type(exc).__name__}: {exc}. "
                    "Где: core/models/eval_parallel.py (eval_worker_entry). "
                    "Что сделать дальше: уменьшите EVAL_WORKERS или проверьте agent_id/логи eval."
                ),
                traceback_tail=tb_tail,
            )
        )
