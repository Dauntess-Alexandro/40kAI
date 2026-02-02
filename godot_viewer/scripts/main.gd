extends Control

const TAB_NAMES := ["Все", "Ход", "Стрельба", "Ближний бой", "Кубы", "Ошибки"]
const UNITS_COLUMNS := 5
const UNITS_COLUMN_WIDTHS := [40, 90, 50, 60, 90]
const DEFAULT_COMMAND_PATH := "user://command.txt"

@onready var round_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/RoundLabel
@onready var turn_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/TurnLabel
@onready var phase_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/PhaseLabel
@onready var active_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/ActiveLabel
@onready var player_vp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PlayerVPLabel
@onready var model_vp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/ModelVPLabel
@onready var player_cp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PlayerCPLabel
@onready var model_cp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/ModelCPLabel
@onready var log_tabs: TabContainer = $MainSplit/LogGroup/LogTabs
@onready var map_view: MapView = $MainSplit/TopSplit/LeftPanel/MapView
@onready var objective_radius_toggle: CheckBox = $MainSplit/TopSplit/LeftPanel/ObjectiveRadiusToggle
@onready var units_table: GridContainer = $MainSplit/TopSplit/RightPanel/RightContent/UnitsGroup/UnitsTable
@onready var command_prompt: Label = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandPrompt
@onready var command_input: LineEdit = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandInputRow/CommandInput
@onready var command_send: Button = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandInputRow/CommandSend

var _state_reader: StateReader
var _command_path := DEFAULT_COMMAND_PATH

func _ready() -> void:
    _configure_log_tabs()
    _configure_units_headers()
    objective_radius_toggle.toggled.connect(_on_objective_radius_toggled)
    map_view.set_show_objective_radius(objective_radius_toggle.button_pressed)
    command_input.text_submitted.connect(_on_command_submitted)
    command_input.gui_input.connect(_on_command_input_gui)
    command_send.pressed.connect(_on_command_send_pressed)
    var env_command_path := OS.get_environment("COMMAND_PATH")
    if env_command_path != "":
        _command_path = env_command_path
    _state_reader = StateReader.new()
    var env_state_path := OS.get_environment("STATE_PATH")
    if env_state_path != "":
        _state_reader.state_path = env_state_path
    add_child(_state_reader)
    _state_reader.state_changed.connect(_apply_state)

func _configure_log_tabs() -> void:
    for idx in range(min(log_tabs.get_tab_count(), TAB_NAMES.size())):
        log_tabs.set_tab_title(idx, TAB_NAMES[idx])

func _configure_units_headers() -> void:
    for idx in range(min(units_table.get_child_count(), UNITS_COLUMNS)):
        var header := units_table.get_child(idx)
        if header is Label:
            if idx >= 0 and idx < UNITS_COLUMN_WIDTHS.size():
                header.custom_minimum_size = Vector2(UNITS_COLUMN_WIDTHS[idx], 0)
            header.horizontal_alignment = HORIZONTAL_ALIGNMENT_LEFT

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
    map_view.set_state(state)
    _apply_units_table(state.get("units", []))

func _on_objective_radius_toggled(pressed: bool) -> void:
    map_view.set_show_objective_radius(pressed)

func _on_command_send_pressed() -> void:
    _submit_command(command_input.text)

func _on_command_submitted(text: String) -> void:
    _submit_command(text)

func _on_command_input_gui(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and event.ctrl_pressed and event.keycode == KEY_L:
        command_input.clear()
        command_prompt.text = "Команда очищена."

func _submit_command(text: String) -> void:
    var trimmed := text.strip_edges()
    if trimmed == "":
        command_prompt.text = "Ожидаю команду..."
        return
    if _write_command(trimmed):
        command_prompt.text = "Команда отправлена: %s" % trimmed
        command_input.clear()
    else:
        command_prompt.text = "Не удалось отправить команду (проверьте путь: %s)." % _command_path

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

func _format_side(side_value) -> String:
    if side_value == "player":
        return "Игрок"
    if side_value == "model":
        return "Модель"
    return "—"

func _apply_units_table(units_value) -> void:
    while units_table.get_child_count() > UNITS_COLUMNS:
        var child := units_table.get_child(units_table.get_child_count() - 1)
        units_table.remove_child(child)
        child.queue_free()

    var units: Array = []
    if units_value is Array:
        units = units_value

    for unit in units:
        if not unit is Dictionary:
            continue
        var unit_data: Dictionary = unit
        _add_units_cell(_to_text(unit_data.get("id", "—")), 0, HORIZONTAL_ALIGNMENT_RIGHT)
        _add_units_cell(_format_side(unit_data.get("side")), 1, HORIZONTAL_ALIGNMENT_LEFT)
        _add_units_cell(_to_text(unit_data.get("hp", "—")), 2, HORIZONTAL_ALIGNMENT_RIGHT)
        _add_units_cell(_to_text(unit_data.get("models", "—")), 3, HORIZONTAL_ALIGNMENT_RIGHT)
        var x_value = unit_data.get("x")
        var y_value = unit_data.get("y")
        var coord_text := "—"
        if x_value != null and y_value != null:
            coord_text = "(%s, %s)" % [str(x_value), str(y_value)]
        _add_units_cell(coord_text, 4, HORIZONTAL_ALIGNMENT_LEFT)

    if units.is_empty():
        _add_units_cell("—", 0, HORIZONTAL_ALIGNMENT_RIGHT)
        _add_units_cell("—", 1, HORIZONTAL_ALIGNMENT_LEFT)
        _add_units_cell("—", 2, HORIZONTAL_ALIGNMENT_RIGHT)
        _add_units_cell("—", 3, HORIZONTAL_ALIGNMENT_RIGHT)
        _add_units_cell("—", 4, HORIZONTAL_ALIGNMENT_LEFT)

func _add_units_cell(text: String, column_index: int, alignment: HorizontalAlignment) -> void:
    var label := Label.new()
    label.text = text
    if column_index >= 0 and column_index < UNITS_COLUMN_WIDTHS.size():
        label.custom_minimum_size = Vector2(UNITS_COLUMN_WIDTHS[column_index], 0)
    label.horizontal_alignment = alignment
    units_table.add_child(label)

func _write_command(command: String) -> bool:
    var file := FileAccess.open(_command_path, FileAccess.READ_WRITE)
    if file == null:
        file = FileAccess.open(_command_path, FileAccess.WRITE)
    if file == null:
        return false
    file.seek_end()
    file.store_line(command)
    file.close()
    return true

func _to_text(value) -> String:
    if value == null:
        return "—"
    return str(value)
