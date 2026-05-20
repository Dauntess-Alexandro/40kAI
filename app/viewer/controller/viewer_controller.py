"""Viewer QObject bridge for Widgets/QML (migration Sprint 3+).

Computes header/status strings shared between legacy widgets and future QML panels.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from PySide6.QtCore import QObject, QPointF, Property, Signal, Slot


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
    fxQualityChanged = Signal()
    commandPromptTextChanged = Signal()
    commandHintTextChanged = Signal()
    unitsSummaryChanged = Signal()
    logRevisionChanged = Signal()

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
        self._fx_quality = "medium"
        self._command_prompt_text = ""
        self._command_hint_text = ""
        self._units_summary_text = ""

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

    def _get_fx_quality(self) -> str:
        return self._fx_quality

    fxQuality = Property(str, _get_fx_quality, notify=fxQualityChanged)

    def _get_command_prompt_text(self) -> str:
        return self._command_prompt_text

    commandPromptText = Property(str, _get_command_prompt_text, notify=commandPromptTextChanged)

    def _get_command_hint_text(self) -> str:
        return self._command_hint_text

    commandHintText = Property(str, _get_command_hint_text, notify=commandHintTextChanged)

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

    @Slot(str)
    def setFxQuality(self, level: str) -> None:
        lvl = str(level or "").strip().lower() or "medium"
        if lvl not in {"low", "medium", "high"}:
            lvl = "medium"
        win = self._window
        scene = getattr(win, "map_scene", None) if win is not None else None
        fn = getattr(scene, "set_fx_quality", None)
        if callable(fn):
            fn(lvl)
        if lvl != self._fx_quality:
            self._fx_quality = lvl
            self.fxQualityChanged.emit()

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
