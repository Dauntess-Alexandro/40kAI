# core/telemetry/stratagem_report.py
"""Таблица применения стратагем обучаемой стороны (model) по eval-прогону.

Чистые функции расчёта/форматирования: на вход — агрегаты per-sid и тоталы,
на выход — строки таблицы, Markdown и CSV. Без файлового I/O и без запуска игр,
чтобы тестировать изолированно.
"""
from __future__ import annotations

from dataclasses import dataclass

# Колонки CSV/таблицы — единый источник порядка.
_COLUMNS = [
    "stratagem", "attempts", "applied", "miss", "apply_rate_pct",
    "applied_per_game", "games_used", "pct_games", "wr_used", "wr_notused", "dwr",
]


@dataclass
class StratagemRow:
    stratagem: str
    attempts: int
    applied: int
    miss: int
    apply_rate_pct: float | None
    applied_per_game: float
    games_used: int
    pct_games: float
    wr_used: float | None
    wr_notused: float | None
    dwr: float | None


def build_stratagem_rows(
    *,
    attempts: dict[str, int],
    applied: dict[str, int],
    miss: dict[str, int],
    games_used: dict[str, int],
    wins_used: dict[str, int],
    games_total: int,
    model_wins_total: int,
) -> list[StratagemRow]:
    """Собрать строки таблицы по всем встретившимся стратагемам (model-сторона).

    Деления на ноль не бывает: при нулевом знаменателе соответствующая метрика = None
    (в отчёте отрисуется как «—»). Сортировка — по applied убыв.
    """
    sids = set(attempts) | set(applied) | set(miss) | set(games_used) | set(wins_used)
    rows: list[StratagemRow] = []
    for sid in sids:
        att = int(attempts.get(sid, 0))
        app = int(applied.get(sid, 0))
        ms = int(miss.get(sid, 0))
        gu = int(games_used.get(sid, 0))
        wu = int(wins_used.get(sid, 0))
        apply_rate = (app / att * 100.0) if att > 0 else None
        per_game = (app / games_total) if games_total > 0 else 0.0
        pct_games = (gu / games_total * 100.0) if games_total > 0 else 0.0
        wr_used = (wu / gu) if gu > 0 else None
        games_not = games_total - gu
        wins_not = model_wins_total - wu
        wr_notused = (wins_not / games_not) if games_not > 0 else None
        dwr = (wr_used - wr_notused) if (wr_used is not None and wr_notused is not None) else None
        rows.append(StratagemRow(
            stratagem=sid, attempts=att, applied=app, miss=ms,
            apply_rate_pct=apply_rate, applied_per_game=per_game,
            games_used=gu, pct_games=pct_games,
            wr_used=wr_used, wr_notused=wr_notused, dwr=dwr,
        ))
    rows.sort(key=lambda r: r.applied, reverse=True)
    return rows


def _f(value: float | None, digits: int = 3) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def rows_to_markdown(rows: list[StratagemRow], *, header_meta: dict) -> str:
    lines: list[str] = []
    lines.append("# Таблица стратагем (только DQN-модель)\n")
    lines.append(
        f"- agent_id: `{header_meta.get('agent_id', '?')}`  "
        f"games: {header_meta.get('games', 0)}  "
        f"overall winrate: {float(header_meta.get('winrate', 0.0)):.3f}  "
        f"дата: {header_meta.get('date', '')}\n"
    )
    lines.append(
        "> ⚠️ Связь с winrate — **корреляция, а не причинность**: редкие стратагемы "
        "часто маркируют состояние партии (их жмут, когда уже хорошо/плохо), а не определяют исход.\n"
    )
    if not rows:
        lines.append("\n_нет данных: стратагемы моделью не применялись или трейс выключен._\n")
        return "\n".join(lines)
    lines.append(
        "| стратагема | attempts | applied | miss | apply_rate% | applied/game | "
        "games_used | %games | WR_used | WR_notused | ΔWR |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        lines.append(
            f"| {r.stratagem} | {r.attempts} | {r.applied} | {r.miss} | "
            f"{_f(r.apply_rate_pct, 1)} | {r.applied_per_game:.2f} | "
            f"{r.games_used} | {r.pct_games:.1f} | "
            f"{_f(r.wr_used)} | {_f(r.wr_notused)} | {_f(r.dwr)} |"
        )
    return "\n".join(lines) + "\n"


def rows_to_csv(rows: list[StratagemRow]) -> str:
    out = [",".join(_COLUMNS)]
    for r in rows:
        out.append(",".join([
            r.stratagem, str(r.attempts), str(r.applied), str(r.miss),
            "" if r.apply_rate_pct is None else f"{r.apply_rate_pct:.4f}",
            f"{r.applied_per_game:.6f}", str(r.games_used), f"{r.pct_games:.4f}",
            "" if r.wr_used is None else f"{r.wr_used:.6f}",
            "" if r.wr_notused is None else f"{r.wr_notused:.6f}",
            "" if r.dwr is None else f"{r.dwr:.6f}",
        ]))
    return "\n".join(out) + "\n"
