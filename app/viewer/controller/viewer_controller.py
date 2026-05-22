"""Viewer QObject bridge for Widgets/QML (migration Sprint 3+).

Computes header/status strings shared between legacy widgets and future QML panels.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import json

from PySide6.QtCore import QObject, QPointF, Property, QSettings, Signal, Slot


@dataclass(frozen=True)
class ViewerPresentationContext:
    """Inputs needed to render header/status rows (role labels + deploy hints)."""

    player_role_label: str
    model_role_label: str
    rolloff_attacker_side: Optional[str]
    rolloff_defender_side: Optional[str]
    deploy_status_suffix: str


@dataclass(frozen=True)
class StatusLabels:
    round_text: str
    turn_text: str
    phase_text: str
    active_label_text: str
    deployment_text: str
    vp_player_text: str
    vp_model_text: str
    cp_player_text: str
    cp_model_text: str


def compute_status_labels(state: Optional[Dict[str, Any]], ctx: ViewerPresentationContext) -> StatusLabels:
    """Mirror legacy ``ViewerWindow._apply_state`` header rows (must stay behaviour-identical)."""
    state = state or {}

    phase_text = f"Фаза: {state.get('phase', '—')}"
    vinfo = state.get("viewer") if isinstance(state.get("viewer"), dict) else {}
    if vinfo.get("step_seq") is not None and vinfo.get("step_seq", 0) > 0:
        phase_text += f" | ИИ seq={vinfo.get('step_seq')}"
    if vinfo.get("awaiting_ack"):
        phase_text += " | ожидание «Далее»"

    active = state.get("active") or state.get("active_side")
    active_label = (
        ctx.player_role_label
        if active == "player"
        else ctx.model_role_label
        if active == "model"
        else "—"
    )
    active_label_text = f"Активен: {active_label}"

    deployment = state.get("deployment", {}) if isinstance(state.get("deployment", {}), dict) else {}
    attacker = deployment.get("attacker") or state.get("attacker_side")
    defender = deployment.get("defender") or state.get("defender_side")

    def _side_label(raw: Any) -> Optional[str]:
        side = str(raw or "").strip().lower()
        if side == "model":
            return ctx.model_role_label
        if side in {"enemy", "player"}:
            return ctx.player_role_label
        return None

    attacker_label = _side_label(attacker)
    defender_label = _side_label(defender)
    deploy_phase_text = str(state.get("phase") or "").strip().lower()
    deploy_active = ("deploy" in deploy_phase_text) or ("расст" in deploy_phase_text)
    rolloff_done = bool(attacker_label and defender_label)
    if not rolloff_done and not deploy_active:
        attacker_fallback = _side_label(ctx.rolloff_attacker_side)
        defender_fallback = _side_label(ctx.rolloff_defender_side)
        if attacker_fallback and defender_fallback:
            attacker_label = attacker_fallback
            defender_label = defender_fallback
            rolloff_done = True
    if deploy_active:
        if not rolloff_done:
            deploy_text = "Деплой: ожидание roll-off"
        else:
            deploy_text = f"Деплой: расстановка (Attacker={attacker_label} • Defender={defender_label})"
    else:
        if not rolloff_done:
            deploy_text = "Деплой: ожидание roll-off"
        else:
            deploy_text = f"Деплой завершён: Attacker = {attacker_label} • Defender = {defender_label}"

    if ctx.deploy_status_suffix:
        deploy_text = f"{deploy_text} • {ctx.deploy_status_suffix}"

    vp = state.get("vp", {})
    cp = state.get("cp", {})

    return StatusLabels(
        round_text=f"Раунд: {state.get('round', '—')}",
        turn_text=f"Ход: {state.get('turn', '—')}",
        phase_text=phase_text,
        active_label_text=active_label_text,
        deployment_text=deploy_text,
        vp_player_text=f"Player VP: {vp.get('player', '—')}",
        vp_model_text=f"Model VP: {vp.get('model', '—')}",
        cp_player_text=f"Player CP: {cp.get('player', '—')}",
        cp_model_text=f"Model CP: {cp.get('model', '—')}",
    )


class ViewerController(QObject):
    """Single bridge object for future QML and controller-mediated UI refresh."""

    stateUpdated = Signal()
    unitSelected = Signal(int)
    logAppended = Signal(str)
    fxTriggered = Signal(str)

    roundTextChanged = Signal()
    turnTextChanged = Signal()
    phaseTextChanged = Signal()
    activeLabelTextChanged = Signal()
    deploymentTextChanged = Signal()
    vpPlayerTextChanged = Signal()
    vpModelTextChanged = Signal()
    cpPlayerTextChanged = Signal()
    cpModelTextChanged = Signal()
    phaseRawChanged = Signal()
    activeSideRawChanged = Signal()
    activePlayerChanged = Signal()
    selectedUnitIdChanged = Signal()
    selectedUnitSideChanged = Signal()
    pendingRequestSummaryChanged = Signal()
    boardCursorTextChanged = Signal()
    commandPromptTextChanged = Signal()
    commandHintTextChanged = Signal()
    unitsSummaryChanged = Signal()
    logRevisionChanged = Signal()
    commandKindChanged = Signal()
    commandHotkeysChanged = Signal()
    commandChoicesChanged = Signal()
    commandConfirmEnabledChanged = Signal()
    intSpinMinChanged = Signal()
    intSpinMaxChanged = Signal()
    intSpinValueChanged = Signal()
    engineBusyChanged = Signal()
    playerRoleLabelChanged = Signal()
    modelRoleLabelChanged = Signal()
    sideHighlightPlayerChanged = Signal()
    sideHighlightModelChanged = Signal()
    objectiveHighlightChanged = Signal()
    shootPopoverOpenChanged = Signal()
    shootStageChanged = Signal()
    shootStepTitleChanged = Signal()
    shootStepperTextChanged = Signal()
    shootTargetTextChanged = Signal()
    shootMetaTextChanged = Signal()
    shootActionLabelChanged = Signal()
    shootDiceInputChanged = Signal()
    shootDiceCounterChanged = Signal()
    shootInfoTextChanged = Signal()
    shootNeedsDiceInputChanged = Signal()
    unitDetailsPayloadChanged = Signal()
    logSearchTextChanged = Signal()
    logFiltersChanged = Signal()
    rightPanelTabChanged = Signal()
    mapOnlyModeChanged = Signal()
    mapOverlayLegendChanged = Signal()
    selectionSourceChanged = Signal()
    logFilterHiddenCountsChanged = Signal()

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._window: Optional[Any] = None
        self._round_text = "Раунд: —"
        self._turn_text = "Ход: —"
        self._phase_text = "Фаза: —"
        self._active_label_text = "Активен: —"
        self._deployment_text = ""
        self._vp_player_text = "Player VP: —"
        self._vp_model_text = "Model VP: —"
        self._cp_player_text = "Player CP: —"
        self._cp_model_text = "Model CP: —"
        self._phase_raw = ""
        self._active_side_raw = ""
        self._active_player = -1
        self._selected_unit_id = -1
        self._selected_unit_side = ""
        self._pending_request_summary = ""
        self._board_cursor_text = ""
        self._command_prompt_text = ""
        self._command_hint_text = ""
        self._units_summary_text = ""
        self._command_kind = "idle"
        self._command_hotkeys: list = []
        self._command_choices: list = []
        self._command_confirm_enabled = True
        self._int_spin_min = 0
        self._int_spin_max = 999
        self._int_spin_value = 0
        self._engine_busy = False
        self._player_role_label = "Игрок"
        self._model_role_label = "Модель"
        self._side_highlight_player = False
        self._side_highlight_model = False
        self._objective_highlight = True
        self._shoot_popover_open = False
        self._shoot_stage = ""
        self._shoot_step_title = ""
        self._shoot_stepper_text = ""
        self._shoot_target_text = ""
        self._shoot_meta_text = ""
        self._shoot_action_label = ""
        self._shoot_dice_input = ""
        self._shoot_dice_counter = "0/0"
        self._shoot_info_text = ""
        self._shoot_needs_dice_input = False
        self._unit_details_payload: Dict[str, Any] = {}
        self._log_search_text = ""
        self._log_filters = {
            "movement": True,
            "shooting": True,
            "charge": True,
            "fight": True,
            "result": True,
            "errors": True,
            "debug": False,
        }
        self._right_panel_tab = 0
        self._map_only_mode = False
        self._units_scroll_target_id = -1
        self._map_overlay_legend: list = []
        self._selection_source = ""
        self._log_filter_hidden_counts: Dict[str, int] = {}

    def attach_window(self, window: Any) -> None:
        """Keep weak coupling to ``ViewerWindow`` for slot delegation."""
        self._window = window

    def _get_round_text(self) -> str:
        return self._round_text

    roundText = Property(str, _get_round_text, notify=roundTextChanged)

    def _get_turn_text(self) -> str:
        return self._turn_text

    turnText = Property(str, _get_turn_text, notify=turnTextChanged)

    def _get_phase_text(self) -> str:
        return self._phase_text

    phaseText = Property(str, _get_phase_text, notify=phaseTextChanged)

    def _get_active_label_text(self) -> str:
        return self._active_label_text

    activeLabelText = Property(str, _get_active_label_text, notify=activeLabelTextChanged)

    def _get_deployment_text(self) -> str:
        return self._deployment_text

    deploymentText = Property(str, _get_deployment_text, notify=deploymentTextChanged)

    def _get_vp_player_text(self) -> str:
        return self._vp_player_text

    vpPlayerText = Property(str, _get_vp_player_text, notify=vpPlayerTextChanged)

    def _get_vp_model_text(self) -> str:
        return self._vp_model_text

    vpModelText = Property(str, _get_vp_model_text, notify=vpModelTextChanged)

    def _get_cp_player_text(self) -> str:
        return self._cp_player_text

    cpPlayerText = Property(str, _get_cp_player_text, notify=cpPlayerTextChanged)

    def _get_cp_model_text(self) -> str:
        return self._cp_model_text

    cpModelText = Property(str, _get_cp_model_text, notify=cpModelTextChanged)

    def _get_phase_raw(self) -> str:
        return self._phase_raw

    phaseRaw = Property(str, _get_phase_raw, notify=phaseRawChanged)

    def _get_active_side_raw(self) -> str:
        return self._active_side_raw

    activeSideRaw = Property(str, _get_active_side_raw, notify=activeSideRawChanged)

    def _get_active_player(self) -> int:
        return self._active_player

    activePlayer = Property(int, _get_active_player, notify=activePlayerChanged)

    def _get_selected_unit_id(self) -> int:
        return self._selected_unit_id

    selectedUnitId = Property(int, _get_selected_unit_id, notify=selectedUnitIdChanged)

    def _get_selected_unit_side(self) -> str:
        return self._selected_unit_side

    selectedUnitSide = Property(str, _get_selected_unit_side, notify=selectedUnitSideChanged)

    def _get_pending_request_summary(self) -> str:
        return self._pending_request_summary

    pendingRequest = Property(str, _get_pending_request_summary, notify=pendingRequestSummaryChanged)

    def _get_board_cursor_text(self) -> str:
        return self._board_cursor_text

    boardCursor = Property(str, _get_board_cursor_text, notify=boardCursorTextChanged)

    def _get_command_prompt_text(self) -> str:
        return self._command_prompt_text

    commandPromptText = Property(str, _get_command_prompt_text, notify=commandPromptTextChanged)

    def _get_command_hint_text(self) -> str:
        return self._command_hint_text

    commandHintText = Property(str, _get_command_hint_text, notify=commandHintTextChanged)

    def _get_command_confirm_enabled(self) -> bool:
        return self._command_confirm_enabled

    commandConfirmEnabled = Property(
        bool, _get_command_confirm_enabled, notify=commandConfirmEnabledChanged
    )

    def set_command_confirm_enabled(self, enabled: bool) -> None:
        e = bool(enabled)
        if e != self._command_confirm_enabled:
            self._command_confirm_enabled = e
            self.commandConfirmEnabledChanged.emit()

    def _get_units_summary_text(self) -> str:
        return self._units_summary_text

    unitsSummaryText = Property(str, _get_units_summary_text, notify=unitsSummaryChanged)

    def set_command_prompt_text(self, text: str) -> None:
        t = str(text or "")
        if t != self._command_prompt_text:
            self._command_prompt_text = t
            self.commandPromptTextChanged.emit()

    def set_command_hint_text(self, text: str) -> None:
        t = str(text or "")
        if t != self._command_hint_text:
            self._command_hint_text = t
            self.commandHintTextChanged.emit()

    def set_units_summary_text(self, text: str) -> None:
        t = str(text or "")
        if t != self._units_summary_text:
            self._units_summary_text = t
            self.unitsSummaryChanged.emit()

    def bump_log_refresh(self) -> None:
        """Notify QML ``LogPanel`` ListView to scroll after model reset."""
        self.logRevisionChanged.emit()

    def _get_command_kind(self) -> str:
        return self._command_kind

    commandKind = Property(str, _get_command_kind, notify=commandKindChanged)

    def _get_command_hotkeys(self) -> list:
        return self._command_hotkeys

    commandHotkeys = Property(list, _get_command_hotkeys, notify=commandHotkeysChanged)

    def _get_command_choices(self) -> list:
        return self._command_choices

    commandChoices = Property(list, _get_command_choices, notify=commandChoicesChanged)

    def _get_int_spin_min(self) -> int:
        return self._int_spin_min

    intSpinMin = Property(int, _get_int_spin_min, notify=intSpinMinChanged)

    def _get_int_spin_max(self) -> int:
        return self._int_spin_max

    intSpinMax = Property(int, _get_int_spin_max, notify=intSpinMaxChanged)

    def _get_int_spin_value(self) -> int:
        return self._int_spin_value

    intSpinValue = Property(int, _get_int_spin_value, notify=intSpinValueChanged)

    def _get_engine_busy(self) -> bool:
        return self._engine_busy

    engineBusy = Property(bool, _get_engine_busy, notify=engineBusyChanged)

    def _get_player_role_label(self) -> str:
        return self._player_role_label

    playerRoleLabel = Property(str, _get_player_role_label, notify=playerRoleLabelChanged)

    def _get_model_role_label(self) -> str:
        return self._model_role_label

    modelRoleLabel = Property(str, _get_model_role_label, notify=modelRoleLabelChanged)

    def _get_side_highlight_player(self) -> bool:
        return self._side_highlight_player

    sideHighlightPlayer = Property(bool, _get_side_highlight_player, notify=sideHighlightPlayerChanged)

    def _get_side_highlight_model(self) -> bool:
        return self._side_highlight_model

    sideHighlightModel = Property(bool, _get_side_highlight_model, notify=sideHighlightModelChanged)

    def _get_objective_highlight(self) -> bool:
        return self._objective_highlight

    objectiveHighlight = Property(bool, _get_objective_highlight, notify=objectiveHighlightChanged)

    def _get_shoot_popover_open(self) -> bool:
        return self._shoot_popover_open

    shootPopoverOpen = Property(bool, _get_shoot_popover_open, notify=shootPopoverOpenChanged)

    def _get_shoot_stage(self) -> str:
        return self._shoot_stage

    shootStage = Property(str, _get_shoot_stage, notify=shootStageChanged)

    def _get_shoot_step_title(self) -> str:
        return self._shoot_step_title

    shootStepTitle = Property(str, _get_shoot_step_title, notify=shootStepTitleChanged)

    def _get_shoot_stepper_text(self) -> str:
        return self._shoot_stepper_text

    shootStepperText = Property(str, _get_shoot_stepper_text, notify=shootStepperTextChanged)

    def _get_shoot_target_text(self) -> str:
        return self._shoot_target_text

    shootTargetText = Property(str, _get_shoot_target_text, notify=shootTargetTextChanged)

    def _get_shoot_meta_text(self) -> str:
        return self._shoot_meta_text

    shootMetaText = Property(str, _get_shoot_meta_text, notify=shootMetaTextChanged)

    def _get_shoot_action_label(self) -> str:
        return self._shoot_action_label

    shootActionLabel = Property(str, _get_shoot_action_label, notify=shootActionLabelChanged)

    def _get_shoot_dice_input(self) -> str:
        return self._shoot_dice_input

    shootDiceInput = Property(str, _get_shoot_dice_input, notify=shootDiceInputChanged)

    def _get_shoot_dice_counter(self) -> str:
        return self._shoot_dice_counter

    shootDiceCounter = Property(str, _get_shoot_dice_counter, notify=shootDiceCounterChanged)

    def _get_shoot_info_text(self) -> str:
        return self._shoot_info_text

    shootInfoText = Property(str, _get_shoot_info_text, notify=shootInfoTextChanged)

    def _get_shoot_needs_dice_input(self) -> bool:
        return self._shoot_needs_dice_input

    shootNeedsDiceInput = Property(bool, _get_shoot_needs_dice_input, notify=shootNeedsDiceInputChanged)

    def _get_unit_details_payload(self) -> Dict[str, Any]:
        return self._unit_details_payload

    unitDetailsPayload = Property("QVariantMap", _get_unit_details_payload, notify=unitDetailsPayloadChanged)

    def _get_log_search_text(self) -> str:
        return self._log_search_text

    logSearchText = Property(str, _get_log_search_text, notify=logSearchTextChanged)

    def _get_log_filters(self) -> dict:
        return self._log_filters

    logFilters = Property("QVariantMap", _get_log_filters, notify=logFiltersChanged)

    def _get_right_panel_tab(self) -> int:
        return self._right_panel_tab

    rightPanelTab = Property(int, _get_right_panel_tab, notify=rightPanelTabChanged)

    def _get_map_overlay_legend(self) -> list:
        return self._map_overlay_legend

    mapOverlayLegend = Property(list, _get_map_overlay_legend, notify=mapOverlayLegendChanged)

    def _get_selection_source(self) -> str:
        return self._selection_source

    selectionSource = Property(str, _get_selection_source, notify=selectionSourceChanged)

    def _get_log_filter_hidden_counts(self) -> Dict[str, int]:
        return self._log_filter_hidden_counts

    logFilterHiddenCounts = Property(
        "QVariantMap", _get_log_filter_hidden_counts, notify=logFilterHiddenCountsChanged
    )

    def set_map_overlay_legend(self, items: list) -> None:
        new_items = list(items or [])
        if new_items != self._map_overlay_legend:
            self._map_overlay_legend = new_items
            self.mapOverlayLegendChanged.emit()

    def set_selection_source(self, source: str) -> None:
        labels = {
            "map": "карта",
            "table": "список",
            "list": "список",
            "auto": "",
            "deploy": "",
        }
        s = str(source or "")
        label = labels.get(s, "")
        if label != self._selection_source:
            self._selection_source = label
            self.selectionSourceChanged.emit()

    def set_log_filter_hidden_counts(self, counts: Dict[str, int]) -> None:
        normalized = {str(k): int(v) for k, v in (counts or {}).items()}
        if normalized != self._log_filter_hidden_counts:
            self._log_filter_hidden_counts = normalized
            self.logFilterHiddenCountsChanged.emit()

    def _get_map_only_mode(self) -> bool:
        return self._map_only_mode

    mapOnlyMode = Property(bool, _get_map_only_mode, notify=mapOnlyModeChanged)

    def _get_units_scroll_target_id(self) -> int:
        return self._units_scroll_target_id

    unitsScrollTargetId = Property(int, _get_units_scroll_target_id, notify=selectedUnitIdChanged)

    def set_role_labels(self, player: str, model: str) -> None:
        p, m = str(player or "Игрок"), str(model or "Модель")
        if p != self._player_role_label:
            self._player_role_label = p
            self.playerRoleLabelChanged.emit()
        if m != self._model_role_label:
            self._model_role_label = m
            self.modelRoleLabelChanged.emit()

    def set_engine_busy(self, busy: bool) -> None:
        b = bool(busy)
        if b != self._engine_busy:
            self._engine_busy = b
            self.engineBusyChanged.emit()

    def set_command_kind(self, kind: str) -> None:
        k = str(kind or "idle")
        if k != self._command_kind:
            self._command_kind = k
            self.commandKindChanged.emit()

    def set_command_hotkeys(self, items: list) -> None:
        self._command_hotkeys = list(items or [])
        self.commandHotkeysChanged.emit()

    def set_command_choices(self, items: list) -> None:
        self._command_choices = list(items or [])
        self.commandChoicesChanged.emit()

    def set_int_spin_range(self, min_v: int, max_v: int, value: int) -> None:
        self._int_spin_min = int(min_v)
        self._int_spin_max = int(max_v)
        self._int_spin_value = int(value)
        self.intSpinMinChanged.emit()
        self.intSpinMaxChanged.emit()
        self.intSpinValueChanged.emit()

    def set_shoot_popover_open(self, open_: bool) -> None:
        o = bool(open_)
        if o != self._shoot_popover_open:
            self._shoot_popover_open = o
            self.shootPopoverOpenChanged.emit()

    def update_shoot_ui(
        self,
        *,
        stage: str = "",
        step_title: str = "",
        stepper: str = "",
        target_text: str = "",
        meta_text: str = "",
        action_label: str = "",
        dice_input: Optional[str] = None,
        dice_counter: str = "",
        info_text: str = "",
        needs_dice: bool = False,
    ) -> None:
        if stage != self._shoot_stage:
            self._shoot_stage = stage
            self.shootStageChanged.emit()
        if step_title != self._shoot_step_title:
            self._shoot_step_title = step_title
            self.shootStepTitleChanged.emit()
        if stepper != self._shoot_stepper_text:
            self._shoot_stepper_text = stepper
            self.shootStepperTextChanged.emit()
        if target_text != self._shoot_target_text:
            self._shoot_target_text = target_text
            self.shootTargetTextChanged.emit()
        if meta_text != self._shoot_meta_text:
            self._shoot_meta_text = meta_text
            self.shootMetaTextChanged.emit()
        if action_label != self._shoot_action_label:
            self._shoot_action_label = action_label
            self.shootActionLabelChanged.emit()
        if dice_input is not None and dice_input != self._shoot_dice_input:
            self._shoot_dice_input = dice_input
            self.shootDiceInputChanged.emit()
        if dice_counter != self._shoot_dice_counter:
            self._shoot_dice_counter = dice_counter
            self.shootDiceCounterChanged.emit()
        if info_text != self._shoot_info_text:
            self._shoot_info_text = info_text
            self.shootInfoTextChanged.emit()
        if needs_dice != self._shoot_needs_dice_input:
            self._shoot_needs_dice_input = needs_dice
            self.shootNeedsDiceInputChanged.emit()

    def set_unit_details_payload(self, payload: Dict[str, Any]) -> None:
        self._unit_details_payload = dict(payload or {})
        self.unitDetailsPayloadChanged.emit()

    @Slot(str)
    def setLogSearchText(self, text: str) -> None:
        t = str(text or "")
        if t != self._log_search_text:
            self._log_search_text = t
            self.logSearchTextChanged.emit()
            win = self._window
            fn = getattr(win, "_refresh_log_views", None)
            if callable(fn):
                fn()

    @Slot(str, bool)
    def setLogFilter(self, key: str, enabled: bool) -> None:
        k = str(key or "")
        if k in self._log_filters:
            self._log_filters[k] = bool(enabled)
            self.logFiltersChanged.emit()
            win = self._window
            fn = getattr(win, "_refresh_log_views", None)
            if callable(fn):
                fn()

    @Slot(int)
    def setRightPanelTab(self, tab: int) -> None:
        t = max(0, min(1, int(tab)))
        if t != self._right_panel_tab:
            self._right_panel_tab = t
            self.rightPanelTabChanged.emit()
            self._save_ui_settings()

    @Slot(bool)
    def setMapOnlyMode(self, enabled: bool) -> None:
        _ = enabled  # режим убран из UI — панель всегда видна
        e = False
        if e != self._map_only_mode:
            self._map_only_mode = e
            self.mapOnlyModeChanged.emit()
            win = self._window
            fn = getattr(win, "_apply_map_only_mode", None)
            if callable(fn):
                fn(e)
            self._save_ui_settings()

    @Slot(str, bool)
    def setSideHighlight(self, side: str, enabled: bool) -> None:
        s = str(side or "").strip().lower()
        e = bool(enabled)
        if s in {"player", "enemy"}:
            if e != self._side_highlight_player:
                self._side_highlight_player = e
                self.sideHighlightPlayerChanged.emit()
        elif s == "model":
            if e != self._side_highlight_model:
                self._side_highlight_model = e
                self.sideHighlightModelChanged.emit()
        win = self._window
        fn = getattr(win, "_apply_side_highlights", None)
        if callable(fn):
            fn()

    @Slot(bool)
    def setObjectiveHighlight(self, enabled: bool) -> None:
        e = bool(enabled)
        if e != self._objective_highlight:
            self._objective_highlight = e
            self.objectiveHighlightChanged.emit()
            win = self._window
            fn = getattr(win, "_set_objective_radius_visible", None) if win is not None else None
            if callable(fn):
                fn(e)

    @Slot(int)
    def centerCameraOnUnit(self, unit_id: int) -> None:
        win = self._window
        if win is None:
            return
        fn = getattr(win, "_center_camera_on_unit", None)
        if callable(fn):
            fn(int(unit_id))

    @Slot(int)
    def previewUnit(self, unit_id: int) -> None:
        win = self._window
        if win is None:
            return
        fn = getattr(win, "_preview_unit_on_map", None)
        if callable(fn):
            fn(int(unit_id))

    @Slot(int)
    def scrollUnitsListToUnit(self, unit_id: int) -> None:
        sid = int(unit_id)
        if sid != self._units_scroll_target_id:
            self._units_scroll_target_id = sid
            self.selectedUnitIdChanged.emit()

    @Slot(str)
    def submitDirection(self, direction: str) -> None:
        self.submitChoice(str(direction))

    @Slot(bool)
    def submitBool(self, value: bool) -> None:
        win = self._window
        if win is None:
            return
        handler = getattr(win, "_controller_submit_answer_object", None)
        if callable(handler):
            handler(bool(value))

    @Slot(int)
    def submitInt(self, value: int) -> None:
        win = self._window
        if win is None:
            return
        handler = getattr(win, "_controller_submit_answer_object", None)
        if callable(handler):
            handler(int(value))

    @Slot(str)
    def submitText(self, text: str) -> None:
        win = self._window
        if win is None:
            return
        handler = getattr(win, "_controller_submit_answer_object", None)
        if callable(handler):
            handler(str(text))

    @Slot()
    def submitPaceNext(self) -> None:
        self.submitBool(True)

    @Slot(str)
    def submitShootStep(self, action: str) -> None:
        win = self._window
        if win is None:
            return
        act = str(action or "").strip().lower()
        if act == "cancel":
            fn = getattr(win, "_cancel_shoot_sequence", None)
            if callable(fn):
                fn()
            return
        fn = getattr(win, "_shoot_step_action", None)
        if callable(fn):
            fn()

    @Slot(str)
    def setShootDiceInput(self, text: str) -> None:
        win = self._window
        if win is None:
            return
        win._shoot_dice_input_text = str(text or "")
        if text != self._shoot_dice_input:
            self._shoot_dice_input = str(text or "")
            self.shootDiceInputChanged.emit()
        fn = getattr(win, "_update_shoot_input_feedback", None)
        if callable(fn):
            fn()

    def _save_ui_settings(self) -> None:
        settings = QSettings("40kAI", "Viewer")
        settings.setValue("rightPanelTab", self._right_panel_tab)
        settings.setValue("logFilters", json.dumps(self._log_filters))

    def load_ui_settings(self) -> None:
        settings = QSettings("40kAI", "Viewer")
        tab = int(settings.value("rightPanelTab", 0))
        self._right_panel_tab = max(0, min(1, tab))
        self.rightPanelTabChanged.emit()
        self._map_only_mode = False
        raw = settings.value("logFilters", "")
        if raw:
            try:
                loaded = json.loads(str(raw))
                if isinstance(loaded, dict):
                    self._log_filters.update(loaded)
                    self.logFiltersChanged.emit()
            except json.JSONDecodeError:
                pass

    @Slot()
    def onLogClearRequested(self) -> None:
        win = self._window
        if win is None:
            return
        bridge = getattr(win, "viewer_dialogs", None)
        if bridge is not None:
            win._pending_confirm_action = "log_clear"
            bridge.openConfirm(
                "Очистить журнал?",
                "Все строки журнала будут удалены из окна Viewer.",
            )
            return
        fn = getattr(win, "_clear_log_viewer", None)
        if callable(fn):
            fn()

    @Slot()
    def startQuickMatch(self) -> None:
        """Заглушка: быстрый старт матча из пустого журнала."""
        win = self._window
        if win is None:
            return
        bridge = getattr(win, "viewer_dialogs", None)
        if bridge is not None:
            bridge.showToast("Быстрый матч: запустите игру из меню «Игра».", 4000)

    @Slot(int)
    def onLogRowClicked(self, row: int) -> None:
        win = self._window
        if win is None:
            return
        fn = getattr(win, "_on_qml_log_row_clicked", None)
        if callable(fn):
            fn(int(row))

    @Slot(int)
    def onLogRowHovered(self, row: int) -> None:
        win = self._window
        if win is None:
            return
        fn = getattr(win, "_on_qml_log_row_hovered", None)
        if callable(fn):
            fn(int(row))

    @Slot()
    def onLogHoverExited(self) -> None:
        win = self._window
        if win is None:
            return
        fn = getattr(win, "_on_qml_log_hover_exited", None)
        if callable(fn):
            fn()

    @Slot(str, int)
    def showToast(self, text: str, duration_ms: int = 2800) -> None:
        win = self._window
        if win is None:
            return
        bridge = getattr(win, "viewer_dialogs", None)
        if bridge is not None:
            bridge.showToast(str(text or ""), int(duration_ms))

    @Slot(str, str)
    def openConfirmDialog(self, title: str, body: str) -> None:
        win = self._window
        if win is None:
            return
        bridge = getattr(win, "viewer_dialogs", None)
        if bridge is not None:
            bridge.openConfirm(str(title or ""), str(body or ""))

    def apply_labels(self, labels: StatusLabels, *, phase_raw: str, active_side_raw: str) -> None:
        self._round_text = labels.round_text
        self._turn_text = labels.turn_text
        self._phase_text = labels.phase_text
        self._active_label_text = labels.active_label_text
        self._deployment_text = labels.deployment_text
        self._vp_player_text = labels.vp_player_text
        self._vp_model_text = labels.vp_model_text
        self._cp_player_text = labels.cp_player_text
        self._cp_model_text = labels.cp_model_text

        self.roundTextChanged.emit()
        self.turnTextChanged.emit()
        self.phaseTextChanged.emit()
        self.activeLabelTextChanged.emit()
        self.deploymentTextChanged.emit()
        self.vpPlayerTextChanged.emit()
        self.vpModelTextChanged.emit()
        self.cpPlayerTextChanged.emit()
        self.cpModelTextChanged.emit()

        pr = str(phase_raw or "")
        if pr != self._phase_raw:
            self._phase_raw = pr
            self.phaseRawChanged.emit()

        ar = str(active_side_raw or "")
        if ar != self._active_side_raw:
            self._active_side_raw = ar
            self.activeSideRawChanged.emit()

        code = -1
        if ar == "player":
            code = 0
        elif ar == "model":
            code = 1
        if code != self._active_player:
            self._active_player = code
            self.activePlayerChanged.emit()

        self.stateUpdated.emit()

    def push_selection(self, side: Optional[str], unit_id: Optional[int]) -> None:
        sid = int(unit_id) if unit_id is not None else -1
        sds = str(side or "")
        prev_id = self._selected_unit_id
        if sid != self._selected_unit_id:
            self._selected_unit_id = sid
            self.selectedUnitIdChanged.emit()
            if sid >= 0:
                self.unitSelected.emit(sid)
        if sds != self._selected_unit_side:
            self._selected_unit_side = sds
            self.selectedUnitSideChanged.emit()
        elif sid != prev_id and sid >= 0:
            self.selectedUnitSideChanged.emit()

    def set_pending_request_summary(self, text: str) -> None:
        t = str(text or "")
        if t != self._pending_request_summary:
            self._pending_request_summary = t
            self.pendingRequestSummaryChanged.emit()

    def set_board_cursor_text(self, text: str) -> None:
        t = str(text or "")
        if t != self._board_cursor_text:
            self._board_cursor_text = t
            self.boardCursorTextChanged.emit()

    @Slot(int)
    def selectUnit(self, unit_id: int) -> None:
        win = self._window
        if win is None:
            return
        resolver = getattr(win, "_controller_resolve_select_unit", None)
        if callable(resolver):
            resolver(int(unit_id))

    @Slot(float, float, result="QVariantMap")
    def hitTestBoard(self, screen_x: float, screen_y: float) -> Dict[str, Any]:
        """Return ``{kind, side, unitId}`` for the top-most unit under screen coordinates."""
        from app.viewer.rendering.hit_test import HitResult

        empty = HitResult.none().as_dict()
        win = self._window
        if win is None:
            return empty
        scene = getattr(win, "map_scene", None)
        fn = getattr(scene, "hit_test_screen", None)
        if not callable(fn):
            return empty
        return fn(QPointF(float(screen_x), float(screen_y))).as_dict()

    @Slot(str)
    def submitChoice(self, token: str) -> None:
        win = self._window
        if win is None:
            return
        handler = getattr(win, "_controller_submit_choice", None)
        if callable(handler):
            handler(str(token))

    @Slot()
    def cancelPending(self) -> None:
        win = self._window
        if win is None:
            return
        handler = getattr(win, "_controller_cancel_pending", None)
        if callable(handler):
            handler()

    def set_fx_quality_high(self) -> None:
        """Визуальные эффекты всегда high (настройка убрана из UI)."""
        win = self._window
        scene = getattr(win, "map_scene", None) if win is not None else None
        fn = getattr(scene, "set_fx_quality", None)
        if callable(fn):
            fn("high")

    @Slot(int)
    def submitChoiceAtIndex(self, idx: int) -> None:
        win = self._window
        if win is None:
            return
        payloads = getattr(win, "_qml_command_payloads", None)
        if not isinstance(payloads, list):
            return
        if idx < 0 or idx >= len(payloads):
            return
        handler = getattr(win, "_controller_submit_answer_object", None)
        if callable(handler):
            handler(payloads[idx])

    @Slot("QVariant")
    def submitAnswerPy(self, value: object) -> None:
        win = self._window
        if win is None:
            return
        handler = getattr(win, "_controller_submit_answer_object", None)
        if callable(handler):
            handler(value)

    @Slot()
    def requestRedraw(self) -> None:
        win = self._window
        if win is None:
            return
        scene = getattr(win, "map_scene", None)
        if scene is not None:
            scene.update()
