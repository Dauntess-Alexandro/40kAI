from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field


@dataclass
class EpisodeResult:
    """Структурный результат одной eval-игры.

    Trace/log-строки остаются только диагностикой; итоговые таблицы и summary
    должны мержить поля этой структуры напрямую, без парсинга текста.
    """

    winner: str | None
    end_reason: str
    vp_diff: int
    model_vp: int
    enemy_vp: int
    episode_len: int
    total_reward: float
    hp_diff_model_minus_enemy: float
    kill_diff_model_minus_enemy: float
    metrics: Counter[str] = field(default_factory=Counter)
    action_tuple_counter: Counter[tuple[int, int, int, int]] = field(default_factory=Counter)
    model_applied_sids: set[str] = field(default_factory=set)
    opp_applied_sids: set[str] = field(default_factory=set)
    trace_block: list[str] = field(default_factory=list)
    event_log_block: list[str] = field(default_factory=list)


@dataclass
class WorkerError:
    """Picklable error payload from eval worker to parent process."""

    worker_id: int
    game_idx: int | None
    message: str
    traceback_tail: str = ""
