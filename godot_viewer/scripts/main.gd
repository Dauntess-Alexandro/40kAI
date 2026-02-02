extends Control

const TAB_NAMES := ["Все", "Ход", "Стрельба", "Ближний бой", "Кубы", "Ошибки"]

@onready var round_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/RoundLabel
@onready var turn_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/TurnLabel
@onready var phase_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/PhaseLabel
@onready var active_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/ActiveLabel
@onready var player_vp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PlayerVPLabel
@onready var model_vp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/ModelVPLabel
@onready var player_cp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PlayerCPLabel
@onready var model_cp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/ModelCPLabel
@onready var log_tabs: TabContainer = $MainSplit/LogGroup/LogTabs

var _state_reader: StateReader

func _ready() -> void:
    _configure_log_tabs()
    _state_reader = StateReader.new()
    var env_state_path := OS.get_environment("STATE_PATH")
    if env_state_path != "":
        _state_reader.state_path = env_state_path
    add_child(_state_reader)
    _state_reader.state_changed.connect(_apply_state)

func _configure_log_tabs() -> void:
    for idx in range(min(log_tabs.get_tab_count(), TAB_NAMES.size())):
        log_tabs.set_tab_title(idx, TAB_NAMES[idx])

func _apply_state(state: Dictionary) -> void:
    round_label.text = "Раунд: %s" % _to_text(state.get("round", "—"))
    turn_label.text = "Ход: %s" % _to_text(state.get("turn", "—"))
    phase_label.text = "Фаза: %s" % _to_text(state.get("phase", "—"))
    active_label.text = "Активен: %s" % _format_active(state.get("active"))

    var vp: Dictionary = state.get("vp", {})
    var cp: Dictionary = state.get("cp", {})
    player_vp_label.text = "Player VP: %s" % _to_text(vp.get("player", "—"))
    model_vp_label.text = "Model VP: %s" % _to_text(vp.get("model", "—"))
    player_cp_label.text = "Player CP: %s" % _to_text(cp.get("player", "—"))
    model_cp_label.text = "Model CP: %s" % _to_text(cp.get("model", "—"))

    _apply_log_tail(state.get("log_tail", []))

func _apply_log_tail(lines: Array) -> void:
    var text_lines := []
    for line in lines:
        text_lines.append(str(line))
    var joined := "\n".join(text_lines)
    for idx in range(log_tabs.get_tab_count()):
        var tab := log_tabs.get_tab_control(idx)
        if tab is TextEdit:
            tab.text = joined

func _format_active(active_value) -> String:
    if active_value == "player":
        return "Игрок"
    if active_value == "model":
        return "Модель"
    return "—"

func _to_text(value) -> String:
    if value == null:
        return "—"
    return str(value)
