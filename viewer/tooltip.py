from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from PySide6 import QtCore, QtGui, QtWidgets

from viewer.styles import Theme

TOOLTIP_ICON_MAP: Dict[str, str] = {
    "models": "👥",
    "wounds": "❤️",
    "weapon": "🔫",
    "melee": "⚔️",
    "range": "📏",
    "bs": "🎯",
    "ws": "🎯",
    "attacks": "⚡",
    "strength": "💪",
    "ap": "🧷",
    "damage": "💥",
    "cover": "🛡",
    "los": "👁",
    "mods": "✨",
    "pin": "📌",
    "debug": "🔧",
}


class UnitTooltipWidget(QtWidgets.QFrame):
    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
        icon_map: Optional[Dict[str, str]] = None,
    ):
        super().__init__(parent)
        self._accent_color = Theme.accent
        self._pinned = False
        self._debug_mode = False
        self._target_pos = QtCore.QPoint()
        self._hiding = False
        self._icon_map = icon_map or dict(TOOLTIP_ICON_MAP)

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating, True)
        self.setObjectName("unitTooltip")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
        self.setWindowFlag(QtCore.Qt.ToolTip, True)

        self._opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(0.0)
        self.setGraphicsEffect(self._opacity_effect)

        self._fade_anim = QtCore.QPropertyAnimation(self._opacity_effect, b"opacity", self)
        self._fade_anim.setDuration(160)
        self._fade_anim.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

        self._move_anim = QtCore.QPropertyAnimation(self, b"pos", self)
        self._move_anim.setDuration(160)
        self._move_anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)

        self._anim_group = QtCore.QParallelAnimationGroup(self)
        self._anim_group.addAnimation(self._fade_anim)
        self._anim_group.addAnimation(self._move_anim)
        self._anim_group.finished.connect(self._on_anim_finished)

        self._build_layout()
        self.setMinimumWidth(320)
        self.hide()

    def _build_layout(self) -> None:
        self._marker = QtWidgets.QFrame(self)
        self._marker.setFixedSize(6, 22)
        self._marker.setObjectName("unitTooltipMarker")

        self._title_label = QtWidgets.QLabel(self)
        self._title_label.setFont(Theme.font(size=10, bold=True))
        self._title_label.setObjectName("unitTooltipTitle")

        self._meta_label = QtWidgets.QLabel(self)
        self._meta_label.setFont(Theme.font(size=8, bold=False))
        self._meta_label.setObjectName("unitTooltipMeta")

        self._status_label = QtWidgets.QLabel(self)
        self._status_label.setFont(Theme.font(size=8, bold=True))
        self._status_label.setObjectName("unitTooltipStatus")

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(6)
        header_layout.addWidget(self._marker)
        header_layout.addWidget(self._title_label, 1)
        header_layout.addWidget(self._status_label, 0, QtCore.Qt.AlignRight)
        header_layout.addWidget(self._meta_label, 0, QtCore.Qt.AlignRight)

        self._divider = QtWidgets.QFrame(self)
        self._divider.setFrameShape(QtWidgets.QFrame.HLine)
        self._divider.setFrameShadow(QtWidgets.QFrame.Plain)
        self._divider.setFixedHeight(1)
        self._divider.setObjectName("unitTooltipDivider")

        self._stat_widgets: Dict[str, QtWidgets.QWidget] = {}
        for key in ("models", "wounds", "cover", "los", "mods"):
            self._stat_widgets[key] = self._build_stat_widget(key)

        stats_row = QtWidgets.QHBoxLayout()
        stats_row.setContentsMargins(0, 0, 0, 0)
        stats_row.setSpacing(16)
        stats_row.addWidget(self._stat_widgets["models"], 1)
        stats_row.addWidget(self._stat_widgets["wounds"], 1)

        self._ranged_title = QtWidgets.QLabel(self)
        self._ranged_title.setFont(Theme.font(size=9, bold=True))
        self._ranged_title.setWordWrap(True)
        self._ranged_title.setObjectName("unitTooltipWeaponTitle")

        self._ranged_chip_labels = self._build_chip_labels(
            ("range", "bs", "attacks", "strength", "ap", "damage")
        )
        self._ranged_chip_layout = QtWidgets.QGridLayout()
        self._ranged_chip_layout.setContentsMargins(0, 0, 0, 0)
        self._ranged_chip_layout.setHorizontalSpacing(6)
        self._ranged_chip_layout.setVerticalSpacing(4)

        self._melee_title = QtWidgets.QLabel(self)
        self._melee_title.setFont(Theme.font(size=9, bold=True))
        self._melee_title.setWordWrap(True)
        self._melee_title.setObjectName("unitTooltipWeaponTitle")

        self._melee_chip_labels = self._build_chip_labels(
            ("ws", "attacks", "strength", "ap", "damage")
        )
        self._melee_chip_layout = QtWidgets.QGridLayout()
        self._melee_chip_layout.setContentsMargins(0, 0, 0, 0)
        self._melee_chip_layout.setHorizontalSpacing(6)
        self._melee_chip_layout.setVerticalSpacing(4)

        misc_row = QtWidgets.QHBoxLayout()
        misc_row.setContentsMargins(0, 0, 0, 0)
        misc_row.setSpacing(12)
        misc_row.addWidget(self._stat_widgets["cover"], 1)
        misc_row.addWidget(self._stat_widgets["los"], 1)
        misc_row.addWidget(self._stat_widgets["mods"], 1)

        self._hp_bar = QtWidgets.QProgressBar(self)
        self._hp_bar.setRange(0, 1)
        self._hp_bar.setValue(0)
        self._hp_bar.setTextVisible(False)
        self._hp_bar.setFixedHeight(7)
        self._hp_bar.setObjectName("unitTooltipHpBar")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)
        layout.addLayout(header_layout)
        layout.addWidget(self._divider)
        layout.addLayout(stats_row)
        layout.addWidget(self._hp_bar)
        layout.addWidget(self._ranged_title)
        layout.addLayout(self._ranged_chip_layout)
        layout.addWidget(self._melee_title)
        layout.addLayout(self._melee_chip_layout)
        layout.addLayout(misc_row)
        self.setLayout(layout)

    def _build_stat_widget(self, key: str) -> QtWidgets.QWidget:
        widget = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        icon = QtWidgets.QLabel(self._icon_map.get(key, ""), widget)
        icon.setFont(Theme.font(size=9, bold=False))
        icon.setObjectName("unitTooltipIcon")
        value = QtWidgets.QLabel("—", widget)
        value.setFont(Theme.font(size=9, bold=False))
        value.setObjectName("unitTooltipValue")
        layout.addWidget(icon)
        layout.addWidget(value, 1)
        widget.setLayout(layout)
        widget._icon_label = icon
        widget._value_label = value
        return widget

    def _build_chip_label(self) -> QtWidgets.QLabel:
        label = QtWidgets.QLabel(self)
        label.setFont(Theme.font(size=8, bold=False))
        label.setObjectName("unitTooltipChip")
        return label

    def _build_chip_labels(self, keys: Tuple[str, ...]) -> Dict[str, QtWidgets.QLabel]:
        labels: Dict[str, QtWidgets.QLabel] = {}
        for key in keys:
            labels[key] = self._build_chip_label()
        return labels

    def _update_chip_layout(
        self,
        layout: QtWidgets.QGridLayout,
        labels: Dict[str, QtWidgets.QLabel],
        values: Dict[str, Optional[str]],
    ) -> None:
        visible_labels: List[QtWidgets.QLabel] = []
        for key, label in labels.items():
            value = values.get(key)
            if value is None:
                label.hide()
                continue
            label.setText(value)
            label.show()
            visible_labels.append(label)
        for index, label in enumerate(visible_labels):
            row = index // 3
            col = index % 3
            layout.addWidget(label, row, col)

    def set_debug_mode(self, enabled: bool) -> None:
        self._debug_mode = enabled

    def set_pinned(self, pinned: bool) -> None:
        self._pinned = pinned

    def update_content(self, payload: Dict, accent: QtGui.QColor) -> None:
        self._accent_color = accent
        self._title_label.setText(payload.get("title", "Юнит"))
        unit_id = payload.get("unit_id", "—")
        self._meta_label.setText(f"Unit {unit_id}")

        status_bits: List[str] = []
        if self._pinned:
            status_bits.append(f"{self._icon_map['pin']} PIN")
        if self._debug_mode:
            status_bits.append(f"{self._icon_map['debug']} DBG")
        self._status_label.setText("  ".join(status_bits))

        self._set_stat_value("models", payload.get("models", "—"))
        self._set_stat_value("wounds", payload.get("wounds", "—"))
        self._set_stat_value("cover", payload.get("cover", "—"))
        self._set_stat_value("los", payload.get("los", "—"))
        self._set_stat_value("mods", payload.get("mods", "—"))

        ranged_name = payload.get("ranged_name", "—")
        melee_name = payload.get("melee_name", "—")
        self._ranged_title.setText(f"{self._icon_map['weapon']} {ranged_name}")
        self._melee_title.setText(f"{self._icon_map['melee']} {melee_name}")

        ranged_values = {
            "range": payload.get("ranged_range"),
            "bs": payload.get("ranged_bs"),
            "attacks": payload.get("ranged_attacks"),
            "strength": payload.get("ranged_strength"),
            "ap": payload.get("ranged_ap"),
            "damage": payload.get("ranged_damage"),
        }
        melee_values = {
            "ws": payload.get("melee_ws"),
            "attacks": payload.get("melee_attacks"),
            "strength": payload.get("melee_strength"),
            "ap": payload.get("melee_ap"),
            "damage": payload.get("melee_damage"),
        }
        self._update_chip_layout(
            self._ranged_chip_layout,
            self._ranged_chip_labels,
            self._format_chip_values(ranged_values),
        )
        self._update_chip_layout(
            self._melee_chip_layout,
            self._melee_chip_labels,
            self._format_chip_values(melee_values),
        )

        wounds_value = payload.get("wounds_value")
        wounds_max = payload.get("wounds_max")
        if isinstance(wounds_value, (int, float)) and isinstance(wounds_max, (int, float)):
            self._hp_bar.setRange(0, max(1, int(wounds_max)))
            self._hp_bar.setValue(max(0, int(wounds_value)))
            self._hp_bar.show()
        else:
            self._hp_bar.hide()

        self._apply_styles()

    def _format_chip_values(self, values: Dict[str, Optional[object]]) -> Dict[str, Optional[str]]:
        formatted: Dict[str, Optional[str]] = {}
        for key, value in values.items():
            if value is None or value == "—":
                formatted[key] = None
                continue
            label = self._icon_map.get(key, "")
            formatted[key] = f"{label} {value}"
        return formatted

    def _on_anim_finished(self) -> None:
        if self._hiding and self._opacity_effect.opacity() <= 0.01:
            self.hide()
        self._hiding = False

    def _set_stat_value(self, key: str, value: object) -> None:
        widget = self._stat_widgets.get(key)
        if not widget:
            return
        text = "—" if value is None else str(value)
        widget._value_label.setText(text)

    def _apply_styles(self) -> None:
        accent = self._accent_color
        accent_rgba = f"rgba({accent.red()}, {accent.green()}, {accent.blue()}, 0.7)"
        bg_rgba = "rgba(20, 22, 20, 0.86)"
        self.setStyleSheet(
            """
            QFrame#unitTooltip {{
                background-color: {bg};
                border: 1px solid {accent};
                border-radius: 8px;
            }}
            QFrame#unitTooltipMarker {{
                background-color: {accent};
                border-radius: 3px;
            }}
            QLabel#unitTooltipTitle {{
                color: {text};
            }}
            QLabel#unitTooltipMeta {{
                color: {muted};
            }}
            QLabel#unitTooltipStatus {{
                color: {accent};
            }}
            QFrame#unitTooltipDivider {{
                background-color: {accent};
            }}
            QLabel#unitTooltipIcon {{
                color: {accent};
            }}
            QLabel#unitTooltipValue {{
                color: {text};
            }}
            QLabel#unitTooltipWeaponTitle {{
                color: {text};
            }}
            QLabel#unitTooltipChip {{
                color: {text};
                background-color: rgba(14, 16, 14, 0.6);
                border: 1px solid rgba(0, 0, 0, 0.3);
                border-radius: 4px;
                padding: 1px 6px;
            }}
            QProgressBar#unitTooltipHpBar {{
                background: rgba(10, 12, 10, 0.6);
                border: 1px solid rgba(0, 0, 0, 0.3);
                border-radius: 4px;
            }}
            QProgressBar#unitTooltipHpBar::chunk {{
                background-color: {accent};
                border-radius: 4px;
            }}
            """.format(
                bg=bg_rgba,
                accent=accent_rgba,
                text=Theme.text.name(),
                muted=Theme.muted.name(),
            )
        )

    def show_at(self, target_pos: QtCore.QPoint, animate: bool = True) -> None:
        self._target_pos = target_pos
        self._hiding = False
        if not animate:
            self.move(target_pos)
            self._opacity_effect.setOpacity(1.0)
            self.show()
            return
        start_pos = target_pos + QtCore.QPoint(0, 6)
        self._move_anim.stop()
        self._fade_anim.stop()
        self._anim_group.stop()
        self.move(start_pos)
        self.show()
        self._fade_anim.setStartValue(self._opacity_effect.opacity())
        self._fade_anim.setEndValue(1.0)
        self._move_anim.setStartValue(start_pos)
        self._move_anim.setEndValue(target_pos)
        self._anim_group.start()

    def hide_animated(self) -> None:
        if not self.isVisible():
            return
        self._fade_anim.stop()
        self._move_anim.stop()
        self._anim_group.stop()
        self._hiding = True
        self._fade_anim.setStartValue(self._opacity_effect.opacity())
        self._fade_anim.setEndValue(0.0)
        self._move_anim.setStartValue(self.pos())
        self._move_anim.setEndValue(self.pos())
        self._anim_group.start()
