from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple
import os
import sys

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from tui.board_parser import BoardState, CellItem, slice_grid
from tui.state_parser import GameState, UnitStatus


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
                state,
                viewport,
                show_units,
                show_objectives,
                show_debug,
                highlight_coord,
            )
        )
        layout["sidebar"].update(self._render_sidebar(state, board=board, show_legend=show_legend))
        layout["journal"].update(self._render_journal(journal_lines))
        return layout

    def _render_map(
        self,
        board: Optional[BoardState],
        state: Optional[GameState],
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

        drawn_units = _collect_drawn_units(grid)
        if _debug_enabled():
            _emit_parsed_units(board, state)
            _emit_drawn_units(
                board,
                drawn_units,
                viewport=viewport,
            )

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
        grid: List[List[List[CellItem]]],
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
                value = row[col_idx] if col_idx < len(row) else []
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
        value: List[CellItem],
        show_units: bool,
        show_objectives: bool,
        highlight_coord: Optional[Tuple[int, int]],
        coord: Tuple[int, int],
    ) -> Text:
        cell_width = 2
        highlight = highlight_coord is not None and coord == highlight_coord
        units = [item for item in value if item.kind == "unit"]
        objectives = [item for item in value if item.kind == "objective"]
        unit_count = len(units)

        if show_units and unit_count:
            if unit_count == 1:
                unit_side = units[0].side
                style = "bold green" if unit_side == "enemy" else "bold blue"
                if highlight:
                    style = f"reverse {style}"
                return Text("● ", style=style)
            marker = "*" if unit_count > 9 else str(unit_count)
            style = "bold white"
            if highlight:
                style = f"reverse {style}"
            return Text(f"{marker} ", style=style)
        if objectives and show_objectives:
            style = "yellow"
            if highlight:
                style = "reverse yellow"
            return Text("◆ ", style=style)
        style = "grey70"
        if highlight:
            style = "reverse grey70"
        return Text("· ", style=style)

    def _horizontal_border(self, left: str, mid: str, right: str, cols: int, cell_width: int) -> str:
        if cols <= 0:
            return ""
        segment = "─" * cell_width
        return left + mid.join([segment] * cols) + right

    def _render_sidebar(
        self,
        state: GameState,
        *,
        board: Optional[BoardState] = None,
        show_legend: bool = True,
    ) -> Panel:
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
        legend.add_row(Text("2-9", style="bold white"), "Стек")
        legend.add_row(Text("*", style="bold white"), "Стек > 9")

        panels = [
            Panel(status_table, title="СТАТУС", border_style="grey50"),
            Panel(units_table, title="ОТРЯДЫ", border_style="grey50"),
        ]
        stacks_panel = _render_stacks_panel(board)
        if stacks_panel is not None:
            panels.append(stacks_panel)
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


def _debug_enabled() -> bool:
    value = os.getenv("TUI_DEBUG", "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def _emit_parsed_units(board: BoardState, state: Optional[GameState]) -> None:
    roster = _unit_roster_map(state)
    lines = [f"parsed_units: count={len(board.units)}"]
    for unit in board.units:
        roster_entry = roster.get(unit.unit_id)
        name = roster_entry.name if roster_entry else None
        instance_id = roster_entry.instance_id if roster_entry else None
        in_bounds = 0 <= unit.coord[0] < board.height and 0 <= unit.coord[1] < board.width
        lines.append(
            " ".join(
                [
                    f"side={unit.side}",
                    f"unit_id={unit.unit_id}",
                    f"instance_id={instance_id or '—'}",
                    f"name={name or '—'}",
                    f"x={unit.coord[0]}",
                    f"y={unit.coord[1]}",
                    f"in_bounds={in_bounds}",
                ]
            )
        )
        if not in_bounds:
            lines.append(
                f"Юнит {unit.unit_id} вне поля: x={unit.coord[0]} y={unit.coord[1]}"
            )
    _emit_debug_lines(lines)


def _emit_drawn_units(
    board: BoardState,
    drawn_units: List[int],
    *,
    viewport: Optional[Viewport],
) -> None:
    drawn_set = set(drawn_units)
    lines = [f"drawn_units: count={len(drawn_units)}", f"ids={sorted(drawn_set)}"]
    missing = _find_missing_units(board, drawn_set, viewport=viewport)
    if missing:
        missing_str = ", ".join(f"{unit_id}:{reason}" for unit_id, reason in missing)
        lines.append(f"MISSING: [{missing_str}]")
    _emit_debug_lines(lines)


def _emit_debug_lines(lines: Iterable[str]) -> None:
    for line in lines:
        print(line, file=sys.stderr)


def _unit_roster_map(state: Optional[GameState]) -> dict[int, UnitStatus]:
    roster: dict[int, UnitStatus] = {}
    if state is None:
        return roster
    for unit in state.player_units + state.model_units:
        roster[unit.unit_id] = unit
    return roster


def _collect_drawn_units(grid: List[List[List[CellItem]]]) -> List[int]:
    drawn: List[int] = []
    for row in grid:
        for cell_items in row:
            for item in cell_items:
                if item.kind == "unit" and item.unit_id is not None:
                    drawn.append(item.unit_id)
    return drawn


def _find_missing_units(
    board: BoardState,
    drawn_set: set[int],
    *,
    viewport: Optional[Viewport],
) -> List[Tuple[int, str]]:
    start_x, start_y = 0, 0
    view_w, view_h = board.width, board.height
    if viewport is not None:
        start_x = viewport.start_x
        start_y = viewport.start_y
        view_w = viewport.width
        view_h = viewport.height

    coord_index: dict[Tuple[int, int], List[int]] = {}
    for unit in board.units:
        coord_index.setdefault(unit.coord, []).append(unit.unit_id)

    missing: List[Tuple[int, str]] = []
    for unit in board.units:
        x, y = unit.coord
        in_bounds = 0 <= x < board.height and 0 <= y < board.width
        in_view = start_x <= x < start_x + view_h and start_y <= y < start_y + view_w
        if not in_view:
            continue
        if unit.unit_id in drawn_set:
            continue
        if not in_bounds:
            reason = "out_of_bounds"
        elif len(coord_index.get(unit.coord, [])) > 1:
            reason = "collision"
        else:
            reason = "overwritten_by_key"
        missing.append((unit.unit_id, reason))
    return missing


def _render_stacks_panel(board: Optional[BoardState]) -> Optional[Panel]:
    if board is None:
        return None
    stacks = []
    for row_idx, row in enumerate(board.grid):
        for col_idx, cell_items in enumerate(row):
            units = [item.unit_id for item in cell_items if item.kind == "unit" and item.unit_id]
            if len(units) > 1:
                stacks.append(((row_idx, col_idx), sorted(units)))
    if not stacks:
        return None
    stacks_table = Table(box=box.SIMPLE_HEAVY)
    stacks_table.add_column("Клетка")
    stacks_table.add_column("Юниты")
    for coord, units in stacks:
        stacks_table.add_row(f"({coord[0]},{coord[1]})", ", ".join(str(unit) for unit in units))
    return Panel(stacks_table, title="СТЕКИ", border_style="grey50")
