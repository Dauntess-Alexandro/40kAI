from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional, Tuple
import math
import pygame

from .state import GameState, Unit


Color = Tuple[int, int, int]


def render_world(
    surface: pygame.Surface,
    state: GameState,
    origin: Tuple[int, int],
    camera: Tuple[float, float],
    cell_size: float,
    selected_id: Optional[int],
    blink_phase: float,
    colors: Dict[str, Color],
) -> None:
    _draw_grid(surface, state, origin, camera, cell_size, colors["grid"])
    _draw_objectives(surface, state, origin, camera, cell_size, colors["objective"])
    _draw_units(surface, state, origin, camera, cell_size, selected_id, blink_phase, colors)


def _draw_grid(
    surface: pygame.Surface,
    state: GameState,
    origin: Tuple[int, int],
    camera: Tuple[float, float],
    cell_size: float,
    color: Color,
) -> None:
    width_px = state.width * cell_size
    height_px = state.height * cell_size
    start_x = origin[0] + camera[0]
    start_y = origin[1] + camera[1]

    for col in range(state.width + 1):
        x = start_x + col * cell_size
        pygame.draw.line(surface, color, (x, start_y), (x, start_y + height_px), 1)
    for row in range(state.height + 1):
        y = start_y + row * cell_size
        pygame.draw.line(surface, color, (start_x, y), (start_x + width_px, y), 1)


def _draw_objectives(
    surface: pygame.Surface,
    state: GameState,
    origin: Tuple[int, int],
    camera: Tuple[float, float],
    cell_size: float,
    color: Color,
) -> None:
    for obj in state.objectives:
        center = grid_to_screen(obj.x, obj.y, origin, camera, cell_size)
        size = max(4, int(cell_size * 0.35))
        points = [
            (center[0], center[1] - size),
            (center[0] + size, center[1]),
            (center[0], center[1] + size),
            (center[0] - size, center[1]),
        ]
        pygame.draw.polygon(surface, color, points)


def _draw_units(
    surface: pygame.Surface,
    state: GameState,
    origin: Tuple[int, int],
    camera: Tuple[float, float],
    cell_size: float,
    selected_id: Optional[int],
    blink_phase: float,
    colors: Dict[str, Color],
) -> None:
    groups: Dict[Tuple[int, int], List[Unit]] = defaultdict(list)
    for unit in state.units:
        groups[(unit.x, unit.y)].append(unit)

    font = pygame.font.Font(None, max(14, int(cell_size * 0.7)))

    for (x, y), units in groups.items():
        offsets = _jitter_offsets(len(units), cell_size)
        if len(units) > 1:
            center = grid_to_screen(x, y, origin, camera, cell_size)
            count_label = font.render(str(len(units)), True, colors["text"])
            surface.blit(count_label, (center[0] + cell_size * 0.2, center[1] - cell_size * 0.2))
        for unit, offset in zip(units, offsets):
            center = grid_to_screen(x, y, origin, camera, cell_size)
            center = (center[0] + offset[0], center[1] + offset[1])
            color = colors["player"] if unit.side == "player" else colors["model"]
            radius = max(4, int(cell_size * 0.35))
            if selected_id == unit.unit_id:
                pulse = 0.25 + 0.15 * math.sin(blink_phase)
                ring_radius = radius + int(cell_size * (0.4 + pulse))
                pygame.draw.circle(surface, colors["highlight"], center, ring_radius, 2)
            pygame.draw.circle(surface, color, center, radius)
            label = font.render(str(unit.unit_id), True, colors["text"])
            surface.blit(label, (center[0] + radius, center[1] - radius))


def _jitter_offsets(count: int, cell_size: float) -> List[Tuple[float, float]]:
    if count <= 1:
        return [(0.0, 0.0)]
    radius = cell_size * 0.2
    offsets = []
    for i in range(count):
        angle = (2 * math.pi / count) * i
        offsets.append((math.cos(angle) * radius, math.sin(angle) * radius))
    return offsets


def grid_to_screen(
    x: int,
    y: int,
    origin: Tuple[int, int],
    camera: Tuple[float, float],
    cell_size: float,
) -> Tuple[float, float]:
    screen_x = origin[0] + camera[0] + (x + 0.5) * cell_size
    screen_y = origin[1] + camera[1] + (y + 0.5) * cell_size
    return screen_x, screen_y


def screen_to_grid(
    pos: Tuple[int, int],
    origin: Tuple[int, int],
    camera: Tuple[float, float],
    cell_size: float,
) -> Tuple[int, int]:
    rel_x = (pos[0] - origin[0] - camera[0]) / cell_size
    rel_y = (pos[1] - origin[1] - camera[1]) / cell_size
    return int(rel_x), int(rel_y)
