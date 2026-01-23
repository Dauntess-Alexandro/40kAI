from __future__ import annotations

import math
import os
import time
from typing import List, Optional, Tuple

import pygame

from .render import render_world, screen_to_grid
from .state import GameState, load_state
from .ui import draw_info_panel


BACKGROUND = (18, 18, 24)
GRID_COLOR = (45, 45, 55)
PLAYER_COLOR = (70, 200, 90)
MODEL_COLOR = (70, 120, 220)
OBJECTIVE_COLOR = (230, 190, 70)
HIGHLIGHT_COLOR = (255, 255, 255)
TEXT_COLOR = (220, 220, 220)

PANEL_WIDTH = 320
BASE_CELL = 18
MIN_ZOOM = 0.25
MAX_ZOOM = 3.0
POLL_INTERVAL = 0.3


def run() -> None:
    pygame.init()
    pygame.display.set_caption("40kAI — 2D Viewer")
    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    state_path = os.path.abspath(os.path.join("gui", "state.json"))
    board_path = os.path.abspath("board.txt")
    response_path = os.path.abspath(os.path.join("gui", "response.txt"))

    state = load_state(state_path, board_path, response_path)
    selected_id: Optional[int] = None

    zoom = 1.0
    camera = [0.0, 0.0]

    def world_rect() -> pygame.Rect:
        return pygame.Rect(0, 0, max(200, screen.get_width() - PANEL_WIDTH), screen.get_height())

    def fit_to_screen() -> None:
        nonlocal zoom, camera
        rect = world_rect()
        if state.width == 0 or state.height == 0:
            return
        zoom = min(
            rect.width / (state.width * BASE_CELL),
            rect.height / (state.height * BASE_CELL),
        )
        zoom = max(MIN_ZOOM, min(MAX_ZOOM, zoom))
        cell_size = BASE_CELL * zoom
        camera[0] = (rect.width - state.width * cell_size) / 2
        camera[1] = (rect.height - state.height * cell_size) / 2

    fit_to_screen()

    dragging = False
    drag_start = (0, 0)
    camera_start = (0.0, 0.0)

    last_poll = 0.0
    last_mtime = _state_mtime(state_path, board_path)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_f:
                    fit_to_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    drag_start = event.pos
                    camera_start = (camera[0], camera[1])
                elif event.button == 4:
                    _zoom_at(event.pos, 1.1, world_rect(), camera, zoom)
                    zoom = min(MAX_ZOOM, zoom * 1.1)
                elif event.button == 5:
                    _zoom_at(event.pos, 1 / 1.1, world_rect(), camera, zoom)
                    zoom = max(MIN_ZOOM, zoom / 1.1)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if _distance(event.pos, drag_start) < 5:
                        selected_id = _select_unit(state, event.pos, world_rect(), camera, zoom)
                    dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                dx = event.pos[0] - drag_start[0]
                dy = event.pos[1] - drag_start[1]
                camera[0] = camera_start[0] + dx
                camera[1] = camera_start[1] + dy
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    _zoom_at(pygame.mouse.get_pos(), 1.1, world_rect(), camera, zoom)
                    zoom = min(MAX_ZOOM, zoom * 1.1)
                elif event.y < 0:
                    _zoom_at(pygame.mouse.get_pos(), 1 / 1.1, world_rect(), camera, zoom)
                    zoom = max(MIN_ZOOM, zoom / 1.1)

        now = time.monotonic()
        if now - last_poll > POLL_INTERVAL:
            last_poll = now
            current_mtime = _state_mtime(state_path, board_path)
            if current_mtime > last_mtime:
                last_mtime = current_mtime
                new_state = load_state(state_path, board_path, response_path)
                state = new_state
                if selected_id is not None and not any(u.unit_id == selected_id for u in state.units):
                    selected_id = None

        screen.fill(BACKGROUND)
        rect = world_rect()
        panel_rect = pygame.Rect(rect.width, 0, screen.get_width() - rect.width, screen.get_height())

        surface_clip = screen.get_clip()
        screen.set_clip(rect)
        render_world(
            screen,
            state,
            rect.topleft,
            camera,
            BASE_CELL * zoom,
            selected_id,
            now * 4,
            {
                "grid": GRID_COLOR,
                "player": PLAYER_COLOR,
                "model": MODEL_COLOR,
                "objective": OBJECTIVE_COLOR,
                "highlight": HIGHLIGHT_COLOR,
                "text": TEXT_COLOR,
            },
        )
        screen.set_clip(surface_clip)

        selected_unit = next((u for u in state.units if u.unit_id == selected_id), None)
        draw_info_panel(screen, panel_rect, state, selected_unit)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def _select_unit(
    state: GameState,
    pos: Tuple[int, int],
    rect: pygame.Rect,
    camera: List[float],
    zoom: float,
) -> Optional[int]:
    cell_size = BASE_CELL * zoom
    grid_x, grid_y = screen_to_grid(pos, rect.topleft, camera, cell_size)
    for unit in state.units:
        if unit.x == grid_x and unit.y == grid_y:
            return unit.unit_id
    return None


def _zoom_at(
    pos: Tuple[int, int],
    factor: float,
    rect: pygame.Rect,
    camera: List[float],
    zoom: float,
) -> None:
    if factor == 1:
        return
    cell_size = BASE_CELL * zoom
    if cell_size <= 0:
        return
    world_x = (pos[0] - rect.x - camera[0]) / cell_size
    world_y = (pos[1] - rect.y - camera[1]) / cell_size
    new_zoom = max(MIN_ZOOM, min(MAX_ZOOM, zoom * factor))
    new_cell = BASE_CELL * new_zoom
    camera[0] = pos[0] - rect.x - world_x * new_cell
    camera[1] = pos[1] - rect.y - world_y * new_cell


def _state_mtime(state_path: str, board_path: str) -> float:
    if os.path.exists(state_path):
        return os.path.getmtime(state_path)
    if os.path.exists(board_path):
        return os.path.getmtime(board_path)
    return 0.0


def _distance(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])
