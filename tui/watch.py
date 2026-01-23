from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Iterable, Optional

from rich.console import Console
from rich.live import Live

from tui.board_parser import BoardState, clamp_viewport, parse_board
from tui.rich_view import RichRenderer, Viewport
from tui.state_parser import GameState, parse_state

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

    start_x, start_y = clamp_viewport(
        center=(0, 0),
        size=(view_w, view_h),
        bounds=(board.height, board.width),
    )
    return Viewport(start_x=start_x, start_y=start_y, width=view_w, height=view_h)


def _load_state(status_path: Path, units_path: Path) -> GameState:
    return parse_state(status_path=status_path, units_path=units_path)


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

    with Live(console=console, refresh_per_second=4, screen=False) as live:
        while True:
            board = parse_board(board_path)
            state = _load_state(status_path, units_path)
            journal = _read_journal(journal_path, journal_lines)
            viewport = _compute_viewport(board, console)
            layout = renderer.build_layout(board, state, journal, viewport)
            live.update(layout)
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
