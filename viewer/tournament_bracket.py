from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple

from PySide6 import QtCore, QtGui, QtWidgets

from viewer.styles import Theme

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_TOURNAMENT_JSON = os.path.join(ROOT_DIR, "tournament_results.json")


@dataclass
class BracketNode:
    title: str
    score: str = ""
    highlighted: bool = False


class TournamentBracketWidget(QtWidgets.QWidget):
    """Визуализация single-elimination сетки."""

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(480)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._rounds: List[List[BracketNode]] = []

    def set_bracket_data(self, rounds: List[List[Dict]]) -> None:
        prepared: List[List[BracketNode]] = []
        for bracket_round in rounds:
            nodes: List[BracketNode] = []
            for row in bracket_round:
                nodes.append(
                    BracketNode(
                        title=str(row.get("title", "TBD")),
                        score=str(row.get("score", "")),
                        highlighted=bool(row.get("highlighted", False)),
                    )
                )
            prepared.append(nodes)
        self._rounds = prepared
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        super().paintEvent(event)
        if not self._rounds:
            return

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        margin_x = 20
        margin_y = 20
        box_w = 220
        box_h = 52
        col_gap = 80

        canvas = self.rect().adjusted(margin_x, margin_y, -margin_x, -margin_y)
        n_cols = len(self._rounds)
        total_w = n_cols * box_w + max(0, n_cols - 1) * col_gap
        start_x = canvas.left() + max(0, (canvas.width() - total_w) // 2)

        round_positions: List[List[QtCore.QRectF]] = []
        for col, nodes in enumerate(self._rounds):
            x = start_x + col * (box_w + col_gap)
            positions: List[QtCore.QRectF] = []
            if not nodes:
                round_positions.append(positions)
                continue
            step = canvas.height() / max(1, len(nodes))
            for idx, node in enumerate(nodes):
                cy = canvas.top() + step * (idx + 0.5)
                rect = QtCore.QRectF(x, cy - box_h / 2, box_w, box_h)
                positions.append(rect)
                self._draw_node(painter, rect, node)
            round_positions.append(positions)

        line_pen = QtGui.QPen(Theme.accent)
        line_pen.setWidthF(2.0)
        painter.setPen(line_pen)

        for col in range(len(round_positions) - 1):
            current = round_positions[col]
            nxt = round_positions[col + 1]
            if not current or not nxt:
                continue
            for idx, target in enumerate(nxt):
                left_idx = idx * 2
                right_idx = left_idx + 1
                if right_idx >= len(current):
                    continue

                src_a = current[left_idx]
                src_b = current[right_idx]
                p1 = QtCore.QPointF(src_a.right(), src_a.center().y())
                p2 = QtCore.QPointF(src_b.right(), src_b.center().y())
                mid_x = p1.x() + 24
                join_y = target.center().y()
                target_point = QtCore.QPointF(target.left(), join_y)

                painter.drawLine(p1, QtCore.QPointF(mid_x, p1.y()))
                painter.drawLine(p2, QtCore.QPointF(mid_x, p2.y()))
                painter.drawLine(QtCore.QPointF(mid_x, p1.y()), QtCore.QPointF(mid_x, p2.y()))
                painter.drawLine(QtCore.QPointF(mid_x, join_y), target_point)

        painter.end()

    def _draw_node(self, painter: QtGui.QPainter, rect: QtCore.QRectF, node: BracketNode) -> None:
        gradient = QtGui.QLinearGradient(rect.topLeft(), rect.bottomRight())
        if node.highlighted:
            gradient.setColorAt(0.0, Theme.accent)
            gradient.setColorAt(1.0, Theme.accent_dark)
        else:
            gradient.setColorAt(0.0, Theme.panel_alt)
            gradient.setColorAt(1.0, Theme.panel)

        painter.setBrush(QtGui.QBrush(gradient))
        painter.setPen(QtGui.QPen(Theme.accent_dark, 1.5))
        painter.drawRoundedRect(rect, 8, 8)

        text_rect = rect.adjusted(10, 7, -10, -7)
        painter.setPen(QtGui.QPen(Theme.text))
        painter.setFont(Theme.font(size=10, bold=True))
        painter.drawText(text_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop, node.title)
        if node.score:
            painter.setPen(QtGui.QPen(Theme.muted))
            painter.setFont(Theme.font(size=9, bold=False))
            painter.drawText(text_rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, node.score)


class TournamentMetricsTable(QtWidgets.QTableWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(0, 5, parent)
        self.setHorizontalHeaderLabels(["Модель", "ELO", "Winrate", "VP diff", "Матчи"])
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        for col in (1, 2, 3, 4):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeToContents)

    def set_leaderboard(self, leaderboard: List[Dict]) -> None:
        self.setRowCount(len(leaderboard))
        for row_idx, row in enumerate(leaderboard):
            values = [
                str(row.get("name", "—")),
                str(row.get("elo", "—")),
                str(row.get("winrate", "—")),
                str(row.get("vp_diff", "—")),
                str(row.get("games", "—")),
            ]
            for col_idx, value in enumerate(values):
                item = QtWidgets.QTableWidgetItem(value)
                self.setItem(row_idx, col_idx, item)


class TournamentTab(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self._json_path = DEFAULT_TOURNAMENT_JSON

        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(10)

        title = QtWidgets.QLabel("Турнирная лига self-play")
        title.setFont(Theme.font(size=14, bold=True))
        subtitle = QtWidgets.QLabel(
            "Показывает сетку и рейтинг из JSON. Используй для контроля эволюции моделей."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(f"color: {Theme.muted.name()};")

        controls = QtWidgets.QHBoxLayout()
        self.path_edit = QtWidgets.QLineEdit(self._json_path)
        self.path_edit.setPlaceholderText("Путь к tournament_results.json")
        self.reload_btn = QtWidgets.QPushButton("Обновить")
        self.reload_btn.clicked.connect(self._reload_from_path)
        controls.addWidget(self.path_edit, 1)
        controls.addWidget(self.reload_btn)

        self.status_label = QtWidgets.QLabel("Загрузка турнира...")
        self.status_label.setStyleSheet(f"color: {Theme.muted.name()};")

        content_split = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.bracket = TournamentBracketWidget()

        metrics_group = QtWidgets.QGroupBox("Рейтинг моделей")
        metrics_layout = QtWidgets.QVBoxLayout(metrics_group)
        self.metrics_table = TournamentMetricsTable()
        metrics_layout.addWidget(self.metrics_table)

        content_split.addWidget(self.bracket)
        content_split.addWidget(metrics_group)
        content_split.setStretchFactor(0, 3)
        content_split.setStretchFactor(1, 2)
        content_split.setChildrenCollapsible(False)

        root_layout.addWidget(title)
        root_layout.addWidget(subtitle)
        root_layout.addLayout(controls)
        root_layout.addWidget(self.status_label)
        root_layout.addWidget(content_split, 1)

        self._reload_from_path()

    def _reload_from_path(self) -> None:
        self._json_path = self.path_edit.text().strip() or DEFAULT_TOURNAMENT_JSON
        payload, error = self._load_payload(self._json_path)
        if payload is None:
            self._apply_payload(self._demo_payload())
            self.status_label.setText(error)
            self.status_label.setStyleSheet("color: #ffb86c;")
            return

        self._apply_payload(payload)
        loaded_at = payload.get("updated_at", "—")
        self.status_label.setText(f"Турнир загружен: {self._json_path} | updated_at={loaded_at}")
        self.status_label.setStyleSheet(f"color: {Theme.muted.name()};")

    def _apply_payload(self, payload: Dict) -> None:
        rounds = payload.get("rounds", [])
        leaderboard = payload.get("leaderboard", [])
        self.bracket.set_bracket_data(rounds)
        self.metrics_table.set_leaderboard(leaderboard)

    def _load_payload(self, path: str) -> Tuple[Dict | None, str]:
        if not os.path.exists(path):
            return None, (
                "[ТУРНИР][WARN] Файл турнира не найден. "
                "Где: viewer/tournament_bracket.py::_load_payload. "
                f"Что делать: создайте JSON по пути {path}."
            )
        try:
            with open(path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            return None, (
                "[ТУРНИР][ERROR] Не удалось прочитать JSON турнира. "
                "Где: viewer/tournament_bracket.py::_load_payload. "
                f"Что делать: проверьте формат файла. Ошибка: {exc}."
            )

        if not isinstance(payload, dict):
            return None, (
                "[ТУРНИР][ERROR] Некорректная структура JSON (ожидался объект). "
                "Где: viewer/tournament_bracket.py::_load_payload. "
                "Что делать: проверьте schema с полями rounds и leaderboard."
            )
        return payload, ""

    def _demo_payload(self) -> Dict:
        return {
            "updated_at": "demo",
            "rounds": [
                [
                    {"title": "Model_A", "score": "2:1"},
                    {"title": "Model_B", "score": "1:2"},
                    {"title": "Model_C", "score": "2:0"},
                    {"title": "Model_D", "score": "0:2"},
                    {"title": "Model_E", "score": "2:1"},
                    {"title": "Model_F", "score": "1:2"},
                    {"title": "Model_G", "score": "2:0"},
                    {"title": "Model_H", "score": "0:2"},
                ],
                [
                    {"title": "Model_A", "score": "2:1", "highlighted": True},
                    {"title": "Model_C", "score": "2:0", "highlighted": True},
                    {"title": "Model_F", "score": "2:1", "highlighted": True},
                    {"title": "Model_G", "score": "2:0", "highlighted": True},
                ],
                [
                    {"title": "Model_A", "score": "3:2", "highlighted": True},
                    {"title": "Model_G", "score": "3:1", "highlighted": True},
                ],
                [
                    {"title": "Model_A", "score": "3:2", "highlighted": True},
                ],
            ],
            "leaderboard": [
                {"name": "Model_A", "elo": 1642, "winrate": "62%", "vp_diff": "+38", "games": 91},
                {"name": "Model_G", "elo": 1598, "winrate": "58%", "vp_diff": "+24", "games": 88},
                {"name": "Model_C", "elo": 1540, "winrate": "53%", "vp_diff": "+9", "games": 86},
            ],
        }
