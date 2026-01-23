from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from tui.board_parser import BoardState, slice_grid
from tui.state_parser import GameState


@dataclass
class Viewport:
    start_x: int
    start_y: int
    width: int
    height: int


class RichRenderer:
    def __init__(self, console: Optional[Console] = None) -> None:
        self.console = console or Console()

    def build_layout(
        self,
        board: Optional[BoardState],
        state: GameState,
        journal_lines: Iterable[str],
        viewport: Optional[Viewport] = None,
        show_units: bool = True,
        show_objectives: bool = True,
        show_debug: bool = False,
        highlight_coord: Optional[Tuple[int, int]] = None,
        show_legend: bool = True,
    ) -> Layout:
        layout = Layout(name="root")
        layout.split(
            Layout(name="main", ratio=3),
            Layout(name="journal", size=12),
        )
        layout["main"].split_row(
            Layout(name="map", ratio=3),
            Layout(name="sidebar", size=38),
        )

        layout["map"].update(
            self._render_map(
                board,
                viewport,
                show_units,
                show_objectives,
                show_debug,
                highlight_coord,
            )
        )
        layout["sidebar"].update(self._render_sidebar(state, show_legend=show_legend))
        layout["journal"].update(self._render_journal(journal_lines))
        return layout

    def _render_map(
        self,
        board: Optional[BoardState],
        viewport: Optional[Viewport],
        show_units: bool,
        show_objectives: bool,
        show_debug: bool,
        highlight_coord: Optional[Tuple[int, int]],
    ) -> Panel:
        if board is None:
            content = Align.center("Нет данных о поле боя", vertical="middle")
            return Panel(content, title="=== ПОЛЕ БИТВЫ ===", border_style="grey50")

        grid = board.grid
        start_x, start_y = 0, 0
        view_w, view_h = board.width, board.height
        if viewport is not None:
            start_x = viewport.start_x
            start_y = viewport.start_y
            view_w = viewport.width
            view_h = viewport.height
            grid = slice_grid(board.grid, (start_x, start_y), (view_w, view_h))

        grid_text = self._render_grid(
            grid,
            offset=(start_x, start_y),
            show_units=show_units,
            show_objectives=show_objectives,
            show_debug=show_debug,
            highlight_coord=highlight_coord,
        )
        title = "=== ПОЛЕ БИТВЫ ==="
        return Panel(grid_text, title=title, border_style="grey50", padding=(0, 1))

    def _render_grid(
        self,
        grid: List[List[int]],
        *,
        offset: Tuple[int, int],
        show_units: bool,
        show_objectives: bool,
        show_debug: bool,
        highlight_coord: Optional[Tuple[int, int]],
    ) -> Text:
        cell_width = 2
        rows = len(grid)
        cols = max((len(row) for row in grid), default=0)

        top = self._horizontal_border("┌", "┬", "┐", cols, cell_width)
        mid = self._horizontal_border("├", "┼", "┤", cols, cell_width)
        bottom = self._horizontal_border("└", "┴", "┘", cols, cell_width)

        text = Text()
        text.append(top, style="grey50")
        text.append("\n")

        for row_idx, row in enumerate(grid):
            line = Text("│", style="grey50")
            for col_idx in range(cols):
                value = row[col_idx] if col_idx < len(row) else 0
                coord = (offset[0] + row_idx, offset[1] + col_idx)
                line.append(
                    self._cell_text(value, show_units, show_objectives, highlight_coord, coord)
                )
                line.append("│", style="grey50")
            text.append(line)
            if row_idx < rows - 1:
                text.append("\n")
                text.append(mid, style="grey50")
                text.append("\n")
        text.append("\n")
        text.append(bottom, style="grey50")

        if show_debug:
            text.append("\n")
            text.append(f"Срез: x={offset[0]} y={offset[1]}", style="dim")
        return text

    def _cell_text(
        self,
        value: int,
        show_units: bool,
        show_objectives: bool,
        highlight_coord: Optional[Tuple[int, int]],
        coord: Tuple[int, int],
    ) -> Text:
        cell_width = 2
        highlight = highlight_coord is not None and coord == highlight_coord
        if value == 3 and show_objectives:
            style = "yellow"
            if highlight:
                style = "reverse yellow"
            return Text("◆ ", style=style)
        if value >= 20 and show_units:
            style = "bold blue"
            if highlight:
                style = "reverse bold blue"
            return Text("● ", style=style)
        if 10 < value < 20 and show_units:
            style = "bold green"
            if highlight:
                style = "reverse bold green"
            return Text("● ", style=style)
        style = "grey70"
        if highlight:
            style = "reverse grey70"
        return Text("· ", style=style)

    def _horizontal_border(self, left: str, mid: str, right: str, cols: int, cell_width: int) -> str:
        if cols <= 0:
            return ""
        segment = "─" * cell_width
        return left + mid.join([segment] * cols) + right

    def _render_sidebar(self, state: GameState, show_legend: bool = True) -> Panel:
        status_table = Table.grid(padding=(0, 1))
        status_table.add_column(justify="right")
        status_table.add_column()

        status_table.add_row("Раунд", state.battle_round or "—")
        status_table.add_row("Ход", state.turn or "—")
        status_table.add_row("ФАЗА", state.phase or "—")
        status_table.add_row("АКТИВЕН", state.active_side or "—")
        status_table.add_row("VP", f"Игрок: {state.player_vp or '—'} | Модель: {state.model_vp or '—'}")
        status_table.add_row("CP", f"Игрок: {state.player_cp or '—'} | Модель: {state.model_cp or '—'}")

        units_table = Table(box=box.SIMPLE_HEAVY)
        units_table.add_column("Сторона")
        units_table.add_column("ID")
        units_table.add_column("HP", justify="right")
        units_table.add_column("Отряд")

        for unit in state.player_units:
            units_table.add_row("Игрок", str(unit.unit_id), _format_hp(unit.hp), unit.name or "—")
        for unit in state.model_units:
            units_table.add_row("Модель", str(unit.unit_id), _format_hp(unit.hp), unit.name or "—")

        legend = Table.grid(padding=(0, 1))
        legend.add_row(Text("●", style="bold green"), "Игрок")
        legend.add_row(Text("●", style="bold blue"), "Модель")
        legend.add_row(Text("◆", style="yellow"), "Цели")
        legend.add_row(Text("·", style="grey70"), "Пусто")

        panels = [
            Panel(status_table, title="СТАТУС", border_style="grey50"),
            Panel(units_table, title="ОТРЯДЫ", border_style="grey50"),
        ]
        if show_legend:
            panels.append(Panel(legend, title="ЛЕГЕНДА", border_style="grey50"))
        group = Group(*panels)
        return Panel(group, title="КОМАНДНЫЙ ПУНКТ", border_style="grey50")

    def _render_journal(self, journal_lines: Iterable[str]) -> Panel:
        text = Text()
        for line in journal_lines:
            text.append(line.rstrip() + "\n")
        if not text.plain.strip():
            text.append("Журнал пуст.")
        return Panel(text, title="ЖУРНАЛ СОБЫТИЙ", border_style="grey50")


def _format_hp(value: Optional[int]) -> str:
    return str(value) if value is not None else "—"
