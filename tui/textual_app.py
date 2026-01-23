from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Static

from tui.board_parser import BoardState, clamp_viewport, parse_board
from tui.rich_view import RichRenderer, Viewport
from tui.state_parser import GameState, parse_state


@dataclass
class Camera:
    start_x: int = 0
    start_y: int = 0
    width: int = 40
    height: int = 20


class MapPanel(Static):
    board: reactive[Optional[BoardState]] = reactive(None)
    state: reactive[GameState | None] = reactive(None)
    viewport: reactive[Viewport | None] = reactive(None)
    highlight_coord: reactive[Tuple[int, int] | None] = reactive(None)
    show_units: reactive[bool] = reactive(True)
    show_objectives: reactive[bool] = reactive(True)
    show_debug: reactive[bool] = reactive(False)

    def render(self):
        renderer = RichRenderer()
        return renderer._render_map(
            self.board,
            self.viewport,
            self.show_units,
            self.show_objectives,
            self.show_debug,
            self.highlight_coord,
        )


class SidebarPanel(Static):
    state: reactive[GameState | None] = reactive(None)
    show_legend: reactive[bool] = reactive(True)

    def render(self):
        renderer = RichRenderer()
        if self.state is None:
            return renderer._render_sidebar(parse_state(), show_legend=self.show_legend)
        return renderer._render_sidebar(self.state, show_legend=self.show_legend)


class JournalPanel(Static):
    lines: reactive[list[str]] = reactive([])

    def render(self):
        renderer = RichRenderer()
        return renderer._render_journal(self.lines)


class BattlefieldApp(App):
    CSS = """
    Screen {
        layout: vertical;
    }
    #main {
        layout: horizontal;
        height: 1fr;
    }
    #map {
        width: 3fr;
    }
    #sidebar {
        width: 38;
    }
    #journal {
        height: 12;
    }
    """

    BINDINGS = [
        ("w", "camera_up", "Камера вверх"),
        ("s", "camera_down", "Камера вниз"),
        ("a", "camera_left", "Камера влево"),
        ("d", "camera_right", "Камера вправо"),
        ("up", "camera_up", ""),
        ("down", "camera_down", ""),
        ("left", "camera_left", ""),
        ("right", "camera_right", ""),
        ("+", "zoom_in", "Zoom +"),
        ("-", "zoom_out", "Zoom -"),
        ("tab", "next_unit", "Следующий отряд"),
        ("l", "toggle_legend", "Легенда"),
        ("u", "toggle_units", "Юниты"),
        ("o", "toggle_objectives", "Цели"),
        ("d", "toggle_debug", "Debug"),
    ]

    def __init__(
        self,
        board_path: Path = Path("board.txt"),
        status_path: Path = Path("status.txt"),
        units_path: Path = Path("units.txt"),
        journal_path: Path = Path("journal.txt"),
        refresh: float = 0.4,
    ) -> None:
        super().__init__()
        self.board_path = board_path
        self.status_path = status_path
        self.units_path = units_path
        self.journal_path = journal_path
        self.refresh = refresh
        self.camera = Camera()
        self.selected_index = 0
        self.legend_visible = True

    def compose(self) -> ComposeResult:
        with Horizontal(id="main"):
            yield MapPanel(id="map")
            yield SidebarPanel(id="sidebar")
        yield JournalPanel(id="journal")

    def on_mount(self) -> None:
        self.set_interval(self.refresh, self.refresh_data)

    def refresh_data(self) -> None:
        board = parse_board(self.board_path)
        state = parse_state(self.status_path, self.units_path)
        lines = self._read_journal(200)

        viewport = self._viewport_for_board(board)
        highlight = self._selected_coord(board)

        map_panel = self.query_one("#map", MapPanel)
        map_panel.board = board
        map_panel.viewport = viewport
        map_panel.highlight_coord = highlight

        sidebar_panel = self.query_one("#sidebar", SidebarPanel)
        sidebar_panel.state = state

        journal_panel = self.query_one("#journal", JournalPanel)
        journal_panel.lines = lines

    def _viewport_for_board(self, board: Optional[BoardState]) -> Optional[Viewport]:
        if board is None:
            return None
        self.camera.width = max(10, min(self.camera.width, board.width))
        self.camera.height = max(6, min(self.camera.height, board.height))
        start_x, start_y = clamp_viewport(
            (self.camera.start_x, self.camera.start_y),
            (self.camera.width, self.camera.height),
            (board.height, board.width),
        )
        self.camera.start_x = start_x
        self.camera.start_y = start_y
        return Viewport(start_x, start_y, self.camera.width, self.camera.height)

    def _selected_coord(self, board: Optional[BoardState]) -> Optional[Tuple[int, int]]:
        if board is None or not board.units:
            return None
        self.selected_index = self.selected_index % len(board.units)
        return board.units[self.selected_index].coord

    def _read_journal(self, max_lines: int) -> list[str]:
        if not self.journal_path.exists():
            return []
        try:
            lines = self.journal_path.read_text(encoding="utf-8").splitlines()
        except OSError:
            return []
        return lines[-max_lines:]

    def action_camera_up(self) -> None:
        self.camera.start_x = max(0, self.camera.start_x - 1)

    def action_camera_down(self) -> None:
        self.camera.start_x = self.camera.start_x + 1

    def action_camera_left(self) -> None:
        self.camera.start_y = max(0, self.camera.start_y - 1)

    def action_camera_right(self) -> None:
        self.camera.start_y = self.camera.start_y + 1

    def action_zoom_in(self) -> None:
        self.camera.width = max(6, self.camera.width - 2)
        self.camera.height = max(4, self.camera.height - 1)

    def action_zoom_out(self) -> None:
        self.camera.width = self.camera.width + 2
        self.camera.height = self.camera.height + 1

    def action_next_unit(self) -> None:
        self.selected_index += 1

    def action_toggle_units(self) -> None:
        map_panel = self.query_one("#map", MapPanel)
        map_panel.show_units = not map_panel.show_units

    def action_toggle_objectives(self) -> None:
        map_panel = self.query_one("#map", MapPanel)
        map_panel.show_objectives = not map_panel.show_objectives

    def action_toggle_debug(self) -> None:
        map_panel = self.query_one("#map", MapPanel)
        map_panel.show_debug = not map_panel.show_debug

    def action_toggle_legend(self) -> None:
        self.legend_visible = not self.legend_visible
        sidebar_panel = self.query_one("#sidebar", SidebarPanel)
        sidebar_panel.show_legend = self.legend_visible


def run() -> None:
    BattlefieldApp().run()


if __name__ == "__main__":
    run()
