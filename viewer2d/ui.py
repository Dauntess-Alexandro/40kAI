from __future__ import annotations

from typing import Optional
import pygame

from .state import GameState, Unit


def draw_info_panel(
    surface: pygame.Surface,
    rect: pygame.Rect,
    state: GameState,
    selected: Optional[Unit],
) -> None:
    pygame.draw.rect(surface, (25, 25, 32), rect)
    pygame.draw.rect(surface, (45, 45, 55), rect, 2)

    font_title = pygame.font.Font(None, 24)
    font = pygame.font.Font(None, 18)

    x = rect.x + 12
    y = rect.y + 10

    title = font_title.render("Информация", True, (240, 240, 240))
    surface.blit(title, (x, y))
    y += 28

    lines = [
        f"Раунд: {state.round}",
        f"Ход: {state.turn}",
        f"Фаза: {state.phase}",
        f"Активная сторона: {state.active}",
        f"VP (модель/игрок): {state.vp_model}/{state.vp_player}",
        f"CP (модель/игрок): {state.cp_model}/{state.cp_player}",
        f"Источник: {state.source}",
    ]
    for line in lines:
        label = font.render(line, True, (210, 210, 210))
        surface.blit(label, (x, y))
        y += 18

    y += 8
    header = font_title.render("Выбранный юнит", True, (240, 240, 240))
    surface.blit(header, (x, y))
    y += 26

    if selected:
        info = [
            f"ID: {selected.unit_id}",
            f"Сторона: {selected.side}",
            f"Имя: {selected.name}",
            f"HP: {selected.hp if selected.hp is not None else '—'}",
            f"Моделей: {selected.models if selected.models is not None else '—'}",
            f"Коорд: ({selected.x}, {selected.y})",
        ]
    else:
        info = ["Нет выделения"]

    for line in info:
        label = font.render(line, True, (210, 210, 210))
        surface.blit(label, (x, y))
        y += 18

    y += 8
    unit_header = font_title.render("Юниты", True, (240, 240, 240))
    surface.blit(unit_header, (x, y))
    y += 24

    max_lines = (rect.bottom - y - 10) // 18
    for unit in state.units[:max_lines]:
        hp_text = "—" if unit.hp is None else str(unit.hp)
        label = font.render(f"{unit.unit_id} {unit.name} ({hp_text})", True, (200, 200, 200))
        surface.blit(label, (x, y))
        y += 18
