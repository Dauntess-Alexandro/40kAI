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


class _WeaponRowWidget(QtWidgets.QFrame):
    hovered = QtCore.Signal(object)

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self._payload: Dict = {}
        self.setObjectName("unitTooltipWeaponRow")
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(6, 3, 6, 3)
        layout.setSpacing(8)
        self._name = QtWidgets.QLabel(self)
        self._name.setObjectName("unitTooltipWeaponRowName")
        self._name.setFont(Theme.font(size=8, bold=True))
        self._stats = QtWidgets.QLabel(self)
        self._stats.setObjectName("unitTooltipWeaponRowStats")
        self._stats.setFont(Theme.font(size=8, bold=False))
        layout.addWidget(self._name, 1)
        layout.addWidget(self._stats, 0, QtCore.Qt.AlignRight)

    def set_payload(self, payload: Dict) -> None:
        self._payload = dict(payload)
        self._name.setText(str(payload.get("name") or "—"))
        stats = [
            f'R {payload.get("range", "—")}',
            f'Atk {payload.get("attacks", "—")}',
            f'S {payload.get("strength", "—")}',
            f'AP {payload.get("ap", "—")}',
            f'D {payload.get("damage", "—")}',
        ]
        self._stats.setText(" • ".join(stats))

    def enterEvent(self, event: QtCore.QEvent) -> None:
        self.hovered.emit(self._payload)
        super().enterEvent(event)


class UnitTooltipWidget(QtWidgets.QFrame):
    weapon_hovered = QtCore.Signal(object)
    weapon_hover_left = QtCore.Signal()
    copy_stats_requested = QtCore.Signal(str)

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
        self._expanded = False
        self._icon_map = icon_map or dict(TOOLTIP_ICON_MAP)

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
        self.setMinimumWidth(360)
        self.hide()

    def _build_layout(self) -> None:
        self._marker = QtWidgets.QFrame(self)
        self._marker.setFixedSize(6, 24)
        self._marker.setObjectName("unitTooltipMarker")

        self._portrait = QtWidgets.QLabel(self)
        self._portrait.setFixedSize(20, 20)
        self._portrait.setAlignment(QtCore.Qt.AlignCenter)
        self._portrait.setObjectName("unitTooltipPortrait")

        self._title_label = QtWidgets.QLabel(self)
        self._title_label.setFont(Theme.font(size=11, bold=True))
        self._title_label.setObjectName("unitTooltipTitle")

        self._status_label = QtWidgets.QLabel(self)
        self._status_label.setFont(Theme.font(size=8, bold=True))
        self._status_label.setObjectName("unitTooltipStatus")

        self._meta_label = QtWidgets.QLabel(self)
        self._meta_label.setFont(Theme.font(size=8, bold=False))
        self._meta_label.setObjectName("unitTooltipMeta")

        self._details_btn = QtWidgets.QToolButton(self)
        self._details_btn.setObjectName("unitTooltipAction")
        self._details_btn.setCheckable(True)
        self._details_btn.setChecked(False)
        self._details_btn.setText("▸ Details")
        self._details_btn.clicked.connect(self._on_toggle_details)

        self._copy_btn = QtWidgets.QToolButton(self)
        self._copy_btn.setObjectName("unitTooltipAction")
        self._copy_btn.setText("Copy stats")
        self._copy_btn.clicked.connect(self._emit_copy_stats)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(6)
        header_layout.addWidget(self._marker)
        header_layout.addWidget(self._portrait, 0, QtCore.Qt.AlignVCenter)
        header_layout.addWidget(self._title_label, 1)
        header_layout.addWidget(self._status_label)

        action_row = QtWidgets.QHBoxLayout()
        action_row.setContentsMargins(0, 0, 0, 0)
        action_row.setSpacing(6)
        action_row.addWidget(self._meta_label, 1)
        action_row.addWidget(self._details_btn)
        action_row.addWidget(self._copy_btn)

        self._chips_row = QtWidgets.QWidget(self)
        chips_layout = QtWidgets.QHBoxLayout(self._chips_row)
        chips_layout.setContentsMargins(0, 0, 0, 0)
        chips_layout.setSpacing(6)
        self._chip_labels: List[QtWidgets.QLabel] = []
        for i in range(10):
            chip = QtWidgets.QLabel(self._chips_row)
            chip.setObjectName(f"unitTooltipBadge{i}")
            chip.setFont(Theme.font(size=8, bold=True))
            chip.hide()
            chips_layout.addWidget(chip)
            self._chip_labels.append(chip)
        chips_layout.addStretch(1)

        self._threat_label = QtWidgets.QLabel(self)
        self._threat_label.setObjectName("unitTooltipMeta")
        self._threat_label.setFont(Theme.font(size=8, bold=False))

        self._weapon_rows_container = QtWidgets.QWidget(self)
        self._weapon_rows_layout = QtWidgets.QVBoxLayout(self._weapon_rows_container)
        self._weapon_rows_layout.setContentsMargins(0, 0, 0, 0)
        self._weapon_rows_layout.setSpacing(4)
        self._weapon_rows: List[_WeaponRowWidget] = []
        for _ in range(8):
            row = _WeaponRowWidget(self._weapon_rows_container)
            row.hovered.connect(self.weapon_hovered.emit)
            row.hide()
            self._weapon_rows_layout.addWidget(row)
            self._weapon_rows.append(row)

        self._divider = QtWidgets.QFrame(self)
        self._divider.setFrameShape(QtWidgets.QFrame.HLine)
        self._divider.setFixedHeight(1)
        self._divider.setObjectName("unitTooltipDivider")

        self._hp_bar = QtWidgets.QProgressBar(self)
        self._hp_bar.setTextVisible(False)
        self._hp_bar.setFixedHeight(8)
        self._hp_bar.setObjectName("unitTooltipHpBar")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        layout.addLayout(header_layout)
        layout.addLayout(action_row)
        layout.addWidget(self._chips_row)
        layout.addWidget(self._threat_label)
        layout.addWidget(self._divider)
        layout.addWidget(self._weapon_rows_container)
        layout.addWidget(self._hp_bar)

    def _on_toggle_details(self, checked: bool) -> None:
        self._expanded = bool(checked)
        self._details_btn.setText("▾ Details" if checked else "▸ Details")

    def _emit_copy_stats(self) -> None:
        text = str(self.property("copyStatsText") or "")
        self.copy_stats_requested.emit(text)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self.weapon_hover_left.emit()
        super().leaveEvent(event)

    def set_debug_mode(self, enabled: bool) -> None:
        self._debug_mode = enabled

    def set_pinned(self, pinned: bool) -> None:
        self._pinned = pinned

    def update_content(self, payload: Dict, accent: QtGui.QColor) -> None:
        self._accent_color = accent
        self._title_label.setText(str(payload.get("title") or "Юнит"))
        unit_id = payload.get("unit_id", "—")
        self._meta_label.setText(f"ID: {unit_id} • Side: {payload.get('side', '—')}")

        self._portrait.setText(str(payload.get("portrait") or "⚔"))

        status_bits: List[str] = []
        if self._pinned:
            status_bits.append(f"{self._icon_map['pin']} PIN")
        if self._debug_mode:
            status_bits.append(f"{self._icon_map['debug']} DBG")
        self._status_label.setText("  ".join(status_bits))

        chips = list(payload.get("chips") or [])
        for i, chip in enumerate(self._chip_labels):
            if i >= len(chips):
                chip.hide()
                continue
            entry = chips[i]
            label = str(entry.get("label") or "").strip()
            if not label:
                chip.hide()
                continue
            chip.setText(label)
            chip.setProperty("tone", str(entry.get("tone") or "neutral"))
            chip.style().unpolish(chip)
            chip.style().polish(chip)
            chip.show()

        threat = payload.get("threat") or {}
        self._threat_label.setText(
            f"LoS: {threat.get('los', '—')}   •   Obscured: {threat.get('obscured', '—')}   •   "
            f"Enemies seeing me: {threat.get('enemies_seeing', '—')}   •   "
            f"Targets in range: {threat.get('targets_in_range', '—')}"
        )

        profiles = list(payload.get("weapon_profiles") or [])
        shown = profiles if self._expanded else [p for p in profiles if p.get("group") in {"ranged", "melee"}][:2]
        for i, row in enumerate(self._weapon_rows):
            if i >= len(shown):
                row.hide()
                continue
            row.set_payload(shown[i])
            row.show()

        wounds_value = payload.get("wounds_value")
        wounds_max = payload.get("wounds_max")
        if isinstance(wounds_value, (int, float)) and isinstance(wounds_max, (int, float)):
            self._hp_bar.setRange(0, max(1, int(wounds_max)))
            self._hp_bar.setValue(max(0, int(wounds_value)))
            self._hp_bar.show()
        else:
            self._hp_bar.hide()

        self.setProperty("copyStatsText", str(payload.get("copy_stats") or ""))
        self._apply_styles()

    def _on_anim_finished(self) -> None:
        if self._hiding and self._opacity_effect.opacity() <= 0.01:
            self.hide()
        self._hiding = False

    def _apply_styles(self) -> None:
        accent = self._accent_color
        accent_rgba = f"rgba({accent.red()}, {accent.green()}, {accent.blue()}, 0.7)"
        bg_rgba = "rgba(20, 22, 20, 0.90)"
        self.setStyleSheet(
            """
            QFrame#unitTooltip { background-color: %(bg)s; border: 1px solid %(accent)s; border-radius: 12px; }
            QFrame#unitTooltipMarker { background-color: %(accent)s; border-radius: 3px; }
            QLabel#unitTooltipPortrait { color: #201708; background: rgba(214, 172, 92, 0.92); border-radius: 10px; }
            QLabel#unitTooltipTitle { color: %(text)s; }
            QLabel#unitTooltipMeta { color: %(muted)s; }
            QLabel#unitTooltipStatus { color: %(accent)s; }
            QFrame#unitTooltipDivider { background-color: %(accent)s; }
            QToolButton#unitTooltipAction { color: %(text)s; background: rgba(14,16,14,0.55); border: 1px solid rgba(0,0,0,0.4); border-radius: 8px; padding: 2px 7px; }
            QFrame#unitTooltipWeaponRow { background: rgba(14,16,14,0.58); border: 1px solid rgba(0,0,0,0.35); border-radius: 8px; }
            QLabel#unitTooltipWeaponRowName { color: %(text)s; }
            QLabel#unitTooltipWeaponRowStats { color: %(muted)s; }
            QLabel[tone="neutral"] { color: #eceff2; background: rgba(64,68,72,0.95); border: 1px solid rgba(24,24,24,0.8); border-radius: 8px; padding: 2px 8px; }
            QLabel[tone="good"] { color: #e7f5de; background: rgba(74,112,62,0.95); border: 1px solid rgba(36,61,28,0.85); border-radius: 8px; padding: 2px 8px; }
            QLabel[tone="warn"] { color: #211808; background: rgba(242,179,76,0.95); border: 1px solid rgba(92,66,12,0.8); border-radius: 8px; padding: 2px 8px; }
            QLabel[tone="objective"] { color: #f2f4ff; background: rgba(77,94,180,0.95); border: 1px solid rgba(37,47,95,0.86); border-radius: 8px; padding: 2px 8px; }
            QProgressBar#unitTooltipHpBar { background: rgba(10,12,10,0.6); border: 1px solid rgba(0,0,0,0.3); border-radius: 5px; }
            QProgressBar#unitTooltipHpBar::chunk { background-color: %(accent)s; border-radius: 5px; }
            """ % {"bg": bg_rgba, "accent": accent_rgba, "text": Theme.text.name(), "muted": Theme.muted.name()}
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

class TerrainTooltipWidget(QtWidgets.QFrame):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        self._accent_color = Theme.accent
        self._pinned = False
        self._target_pos = QtCore.QPoint()
        self._hiding = False

        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating, True)
        self.setObjectName("unitTooltip")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
        self.setWindowFlag(QtCore.Qt.ToolTip, True)

        self._opacity_effect = QtWidgets.QGraphicsOpacityEffect(self)
        self._opacity_effect.setOpacity(0.0)
        self.setGraphicsEffect(self._opacity_effect)

        self._fade_anim = QtCore.QPropertyAnimation(self._opacity_effect, b"opacity", self)
        self._fade_anim.setDuration(120)
        self._fade_anim.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self._move_anim = QtCore.QPropertyAnimation(self, b"pos", self)
        self._move_anim.setDuration(120)
        self._move_anim.setEasingCurve(QtCore.QEasingCurve.OutCubic)

        self._anim_group = QtCore.QParallelAnimationGroup(self)
        self._anim_group.addAnimation(self._fade_anim)
        self._anim_group.addAnimation(self._move_anim)
        self._anim_group.finished.connect(self._on_anim_finished)

        self._build_layout()
        self.setMinimumWidth(280)
        self.hide()

    def _build_layout(self) -> None:
        self._marker = QtWidgets.QFrame(self)
        self._marker.setFixedSize(6, 24)
        self._marker.setObjectName("unitTooltipMarker")

        self._kind_badge = QtWidgets.QLabel(self)
        self._kind_badge.setFont(Theme.font(size=8, bold=True))
        self._kind_badge.setAlignment(QtCore.Qt.AlignCenter)
        self._kind_badge.setFixedSize(20, 20)
        self._kind_badge.setObjectName("terrainTooltipKindBadge")

        self._title_label = QtWidgets.QLabel(self)
        self._title_label.setFont(Theme.font(size=11, bold=True))
        self._title_label.setObjectName("unitTooltipTitle")

        self._meta_label = QtWidgets.QLabel(self)
        self._meta_label.setFont(Theme.font(size=8, bold=False))
        self._meta_label.setObjectName("unitTooltipMeta")

        self._coords_label = QtWidgets.QLabel(self)
        self._coords_label.setFont(Theme.font(size=8, bold=False))
        self._coords_label.setObjectName("terrainTooltipCoords")
        self._coords_label.setWordWrap(True)

        self._keywords_row = QtWidgets.QWidget(self)
        keywords_layout = QtWidgets.QHBoxLayout(self._keywords_row)
        keywords_layout.setContentsMargins(0, 0, 0, 0)
        keywords_layout.setSpacing(6)
        self._keyword_labels: List[QtWidgets.QLabel] = []
        for index in range(4):
            chip = QtWidgets.QLabel(self._keywords_row)
            chip.setFont(Theme.font(size=8, bold=True))
            chip.setObjectName(f"terrainKeywordChip{index}")
            chip.hide()
            keywords_layout.addWidget(chip, 0)
            self._keyword_labels.append(chip)
        keywords_layout.addStretch(1)

        self._rules_label = QtWidgets.QLabel(self)
        self._rules_label.setFont(Theme.font(size=8, bold=False))
        self._rules_label.setObjectName("terrainTooltipRules")
        self._rules_label.setWordWrap(True)

        self._status_label = QtWidgets.QLabel(self)
        self._status_label.setFont(Theme.font(size=8, bold=True))
        self._status_label.setObjectName("unitTooltipStatus")

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(6)
        header_layout.addWidget(self._marker)
        header_layout.addWidget(self._kind_badge, 0, QtCore.Qt.AlignVCenter)
        header_layout.addWidget(self._title_label, 1, QtCore.Qt.AlignVCenter)
        header_layout.addWidget(self._status_label, 0, QtCore.Qt.AlignRight)

        self._divider = QtWidgets.QFrame(self)
        self._divider.setFrameShape(QtWidgets.QFrame.HLine)
        self._divider.setFixedHeight(1)
        self._divider.setObjectName("unitTooltipDivider")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        layout.addLayout(header_layout)
        layout.addWidget(self._meta_label)
        layout.addWidget(self._keywords_row)
        layout.addWidget(self._coords_label)
        layout.addWidget(self._rules_label)
        layout.addWidget(self._divider)

    def set_pinned(self, pinned: bool) -> None:
        self._pinned = bool(pinned)

    def update_content(self, payload: Dict, accent: QtGui.QColor) -> None:
        self._accent_color = accent
        self._title_label.setText(str(payload.get("title") or "Terrain"))
        terrain_id = str(payload.get("id") or "—")
        terrain_type = str(payload.get("terrain_type") or "terrain")
        self._meta_label.setText(f"ID: {terrain_id} • Type: {terrain_type}")
        self._status_label.setText("📌 PIN" if self._pinned else "")

        coords_text = str(payload.get("coords") or "—")
        self._coords_label.setText(f"Coords: {coords_text}")
        rules_lines = [str(line) for line in list(payload.get("rules") or []) if str(line).strip()]
        self._rules_label.setText("\n".join(rules_lines))

        kind_badge = str(payload.get("kind_badge") or "T")
        self._kind_badge.setText(kind_badge[:1].upper())

        keywords = [str(v).upper() for v in list(payload.get("keywords") or []) if str(v).strip()]
        for idx, chip in enumerate(self._keyword_labels):
            if idx >= len(keywords):
                chip.hide()
                continue
            keyword = keywords[idx]
            chip.setText(keyword)
            chip.setProperty("keyword", keyword)
            chip.style().unpolish(chip)
            chip.style().polish(chip)
            chip.show()
        self._apply_styles()

    def _apply_styles(self) -> None:
        accent = self._accent_color
        accent_rgba = f"rgba({accent.red()}, {accent.green()}, {accent.blue()}, 0.7)"
        bg_rgba = "rgba(20, 22, 20, 0.86)"
        self.setStyleSheet(
            """
            QFrame#unitTooltip {{
                background-color: {bg};
                border: 1px solid {accent};
                border-radius: 12px;
            }}
            QFrame#unitTooltipMarker {{ background-color: {accent}; border-radius: 3px; }}
            QLabel#terrainTooltipKindBadge {{
                color: #1b1304;
                background-color: rgba(245, 170, 48, 0.92);
                border: 1px solid rgba(20, 20, 20, 0.35);
                border-radius: 10px;
                padding: 0px;
            }}
            QLabel#unitTooltipTitle {{ color: {text}; }}
            QLabel#unitTooltipMeta {{ color: {muted}; }}
            QLabel#unitTooltipStatus {{ color: {accent}; }}
            QFrame#unitTooltipDivider {{ background-color: {accent}; }}
            QLabel#terrainTooltipCoords {{ color: {text}; }}
            QLabel#terrainTooltipRules {{ color: {muted}; line-height: 120%; }}
            QLabel[keyword="OBSTACLE"] {{
                color: #e9ecef;
                background-color: rgba(62, 66, 71, 0.95);
                border: 1px solid rgba(26, 28, 31, 0.9);
                border-radius: 8px;
                padding: 2px 8px;
            }}
            QLabel[keyword="BARRICADE"] {{
                color: #1f1a0e;
                background-color: rgba(242, 173, 62, 0.95);
                border: 1px solid rgba(88, 63, 10, 0.85);
                border-radius: 8px;
                padding: 2px 8px;
            }}
            QLabel#terrainKeywordChip0, QLabel#terrainKeywordChip1, QLabel#terrainKeywordChip2, QLabel#terrainKeywordChip3 {{
                border-radius: 8px;
                padding: 2px 8px;
            }}
            """.format(bg=bg_rgba, accent=accent_rgba, text=Theme.text.name(), muted=Theme.muted.name())
        )

    def _on_anim_finished(self) -> None:
        if self._hiding and self._opacity_effect.opacity() <= 0.01:
            self.hide()
        self._hiding = False

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
