from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Iterable, Optional

from rich.console import Console
from rich.live import Live

from tui.board_parser import BoardState, clamp_viewport, parse_board
from tui.rich_view import RichRenderer, Viewport
from tui.state_parser import parse_state

DEFAULT_REFRESH = 0.3
DEFAULT_JOURNAL_LINES = 200


def _read_journal(path: Path, max_lines: int) -> Iterable[str]:
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    return lines[-max_lines:]


def _compute_viewport(board: Optional[BoardState], console: Console) -> Optional[Viewport]:
    if board is None:
        return None
    width = console.size.width
    height = console.size.height

    sidebar_width = 38
    journal_height = 12
    map_width = max(20, width - sidebar_width - 2)
    map_height = max(10, height - journal_height - 4)

    cell_width = 2
    cols = max(1, (map_width - 2) // (cell_width + 1))
    rows = max(1, (map_height - 2) // 2)

    view_w = min(cols, board.width)
    view_h = min(rows, board.height)

    start_x, start_y = _suggest_viewport_start(board, view_w, view_h)
    return Viewport(start_x=start_x, start_y=start_y, width=view_w, height=view_h)


def _suggest_viewport_start(board: BoardState, view_w: int, view_h: int) -> tuple[int, int]:
    points = [unit.coord for unit in board.units] + [obj.coord for obj in board.objectives]
    if not points:
        return clamp_viewport(
            center=(0, 0),
            size=(view_w, view_h),
            bounds=(board.height, board.width),
        )

    min_row = min(p[0] for p in points)
    max_row = max(p[0] for p in points)
    min_col = min(p[1] for p in points)
    max_col = max(p[1] for p in points)

    bbox_h = max_row - min_row + 1
    bbox_w = max_col - min_col + 1

    if bbox_h <= view_h and bbox_w <= view_w:
        pad_row = max(0, (view_h - bbox_h) // 2)
        pad_col = max(0, (view_w - bbox_w) // 2)
        start_row = min_row - pad_row
        start_col = min_col - pad_col
        max_start_row = max(0, board.height - view_h)
        max_start_col = max(0, board.width - view_w)
        start_row = min(max(start_row, 0), max_start_row)
        start_col = min(max(start_col, 0), max_start_col)
        return start_row, start_col

    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2
    return clamp_viewport(
        center=(center_row, center_col),
        size=(view_w, view_h),
        bounds=(board.height, board.width),
    )


def watch(
    board_path: Path,
    status_path: Path,
    units_path: Path,
    journal_path: Path,
    refresh: float,
    journal_lines: int,
) -> None:
    console = Console()
    renderer = RichRenderer(console)
    refresh_rate = max(1, int(1 / refresh))

    with Live(console=console, refresh_per_second=refresh_rate, screen=True, auto_refresh=False) as live:
        while True:
            board = parse_board(board_path)
            journal = _read_journal(journal_path, journal_lines)
            state = parse_state(status_path=status_path, units_path=units_path, journal_lines=journal)
            viewport = _compute_viewport(board, console)
            layout = renderer.build_layout(board, state, journal, viewport)
            live.update(layout, refresh=True)
            time.sleep(refresh)


def main() -> None:
    parser = argparse.ArgumentParser(description="TUI наблюдатель за полем боя")
    parser.add_argument("--board", default="board.txt", help="Путь к board.txt")
    parser.add_argument("--status", default="status.txt", help="Путь к status.txt")
    parser.add_argument("--units", default="units.txt", help="Путь к units.txt")
    parser.add_argument("--journal", default="journal.txt", help="Путь к журналу событий")
    parser.add_argument("--refresh", type=float, default=DEFAULT_REFRESH, help="Частота обновления")
    parser.add_argument("--lines", type=int, default=DEFAULT_JOURNAL_LINES, help="Строк журнала")
    args = parser.parse_args()

    watch(
        board_path=Path(args.board),
        status_path=Path(args.status),
        units_path=Path(args.units),
        journal_path=Path(args.journal),
        refresh=args.refresh,
        journal_lines=args.lines,
    )


if __name__ == "__main__":
    main()
