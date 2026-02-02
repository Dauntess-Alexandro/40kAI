extends Control

const TAB_NAMES := ["Все", "Ход", "Стрельба", "Ближний бой", "Кубы", "Ошибки"]
const UNITS_COLUMNS := 5
const BASE_UNITS_COLUMN_WIDTHS := [40, 90, 50, 60, 90]
const BASE_UNITS_FONT_SIZE := 12
const BASE_SCREEN_SIZE := Vector2(1920, 1080)
const BASE_SPLIT_OFFSET := 760
const BASE_TOP_SPLIT_OFFSET := 1320
const BASE_LEFT_PANEL_WIDTH := 820
const BASE_RIGHT_PANEL_WIDTH := 360
const BASE_MAP_MIN_SIZE := Vector2(820, 520)
const BASE_LOG_GROUP_HEIGHT := 220
const BASE_LOG_TABS_HEIGHT := 200
const BASE_RIGHT_CONTENT_SEPARATION := 10
const BASE_UNITS_SEPARATION := 6
const BASE_LEGEND_SEPARATION := 6
const BASE_LEGEND_LIST_SEPARATION := 4
const BASE_COMMANDS_SEPARATION := 6
const BASE_STATUS_SEPARATION := 2
const BASE_POINTS_SEPARATION := 2
const BASE_SWATCH_SIZE := 12
const SELECT_TEXT_COLOR := Color(1.0, 0.85, 0.4)
const DEFAULT_COMMAND_PATH := "user://command.txt"

@onready var round_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/StatusContent/RoundLabel
@onready var turn_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/StatusContent/TurnLabel
@onready var phase_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/StatusContent/PhaseLabel
@onready var active_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/StatusContent/ActiveLabel
@onready var player_vp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PointsContent/PlayerVPLabel
@onready var model_vp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PointsContent/ModelVPLabel
@onready var player_cp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PointsContent/PlayerCPLabel
@onready var model_cp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PointsContent/ModelCPLabel
@onready var log_tabs: TabContainer = $MainSplit/LogGroup/LogTabs
@onready var map_view: MapView = $MainSplit/TopSplit/LeftPanel/MapView
@onready var objective_radius_toggle: CheckBox = $MainSplit/TopSplit/LeftPanel/ObjectiveRadiusToggle
@onready var fit_button: Button = $MainSplit/TopSplit/LeftPanel/FitButton
@onready var main_split: VSplitContainer = $MainSplit
@onready var top_split: HSplitContainer = $MainSplit/TopSplit
@onready var left_panel: VBoxContainer = $MainSplit/TopSplit/LeftPanel
@onready var right_panel: ScrollContainer = $MainSplit/TopSplit/RightPanel
@onready var right_content: VBoxContainer = $MainSplit/TopSplit/RightPanel/RightContent
@onready var status_title: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/StatusContent/StatusTitle
@onready var status_content: VBoxContainer = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/StatusContent
@onready var points_title: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PointsContent/PointsTitle
@onready var points_content: VBoxContainer = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PointsContent
@onready var units_title: Label = $MainSplit/TopSplit/RightPanel/RightContent/UnitsGroup/UnitsContent/UnitsTitle
@onready var units_content: VBoxContainer = $MainSplit/TopSplit/RightPanel/RightContent/UnitsGroup/UnitsContent
@onready var legend_title: Label = $MainSplit/TopSplit/RightPanel/RightContent/LegendGroup/LegendContent/LegendTitle
@onready var legend_content: VBoxContainer = $MainSplit/TopSplit/RightPanel/RightContent/LegendGroup/LegendContent
@onready var legend_list: VBoxContainer = $MainSplit/TopSplit/RightPanel/RightContent/LegendGroup/LegendContent/LegendList
@onready var legend_player_swatch: ColorRect = $MainSplit/TopSplit/RightPanel/RightContent/LegendGroup/LegendContent/LegendList/LegendPlayer/LegendPlayerSwatch
@onready var legend_model_swatch: ColorRect = $MainSplit/TopSplit/RightPanel/RightContent/LegendGroup/LegendContent/LegendList/LegendModel/LegendModelSwatch
@onready var legend_objective_swatch: ColorRect = $MainSplit/TopSplit/RightPanel/RightContent/LegendGroup/LegendContent/LegendList/LegendObjective/LegendObjectiveSwatch
@onready var commands_title: Label = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandsTitle
@onready var commands_content: VBoxContainer = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent
@onready var command_hint: Label = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandHint
@onready var units_table: GridContainer = $MainSplit/TopSplit/RightPanel/RightContent/UnitsGroup/UnitsContent/UnitsTable
@onready var command_prompt: Label = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandPrompt
@onready var command_input: LineEdit = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandInputRow/CommandInput
@onready var command_send: Button = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandInputRow/CommandSend
@onready var log_group: VBoxContainer = $MainSplit/LogGroup
@onready var log_title: Label = $MainSplit/LogGroup/LogTitle
@onready var log_tabs_container: TabContainer = $MainSplit/LogGroup/LogTabs

var _state_reader: StateReader
var _command_path := DEFAULT_COMMAND_PATH
var _selected_unit_key = null
var _last_units: Array = []
var _last_state: Dictionary = {}
var _ui_scale := 1.0
var _units_column_widths: Array = []

func _ready() -> void:
    _ui_scale = _calculate_ui_scale()
    _apply_ui_scale()
    _configure_log_tabs()
    _configure_units_headers()
    objective_radius_toggle.toggled.connect(_on_objective_radius_toggled)
    map_view.set_show_objective_radius(objective_radius_toggle.button_pressed)
    map_view.unit_selected.connect(_on_map_unit_selected)
    command_input.text_submitted.connect(_on_command_submitted)
    command_input.gui_input.connect(_on_command_input_gui)
    command_send.pressed.connect(_on_command_send_pressed)
    var env_command_path := OS.get_environment("COMMAND_PATH")
    if env_command_path != "":
        _command_path = env_command_path
    _state_reader = StateReader.new()
    var env_state_path := OS.get_environment("STATE_PATH")
    if env_state_path == "":
        env_state_path = OS.get_environment("STATE_JSON_PATH")
    if env_state_path != "":
        _state_reader.state_path = env_state_path
    elif not FileAccess.file_exists(_state_reader.state_path):
        var repo_state_path := ProjectSettings.globalize_path("res://../gui/state.json")
        if FileAccess.file_exists(repo_state_path):
            _state_reader.state_path = repo_state_path
    add_child(_state_reader)
    _state_reader.state_changed.connect(_apply_state)

func _notification(what: int) -> void:
    if what == NOTIFICATION_RESIZED:
        var new_scale := _calculate_ui_scale()
        if absf(new_scale - _ui_scale) >= 0.01:
            _ui_scale = new_scale
            _apply_ui_scale()
            _configure_units_headers()
            _apply_units_table(_last_units)

func _configure_log_tabs() -> void:
    for idx in range(min(log_tabs.get_tab_count(), TAB_NAMES.size())):
        log_tabs.set_tab_title(idx, TAB_NAMES[idx])

func _configure_units_headers() -> void:
    for idx in range(min(units_table.get_child_count(), UNITS_COLUMNS)):
        var header := units_table.get_child(idx)
        if header is Label:
            if idx >= 0 and idx < _units_column_widths.size():
                header.custom_minimum_size = Vector2(_units_column_widths[idx], 0)
            header.horizontal_alignment = HORIZONTAL_ALIGNMENT_LEFT
            header.add_theme_font_size_override("font_size", _scaled_font_size(BASE_UNITS_FONT_SIZE))

func _apply_state(state: Dictionary) -> void:
    _last_state = state
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
    _last_units = state.get("units", []) if state.get("units") is Array else []
    _update_active_context(state)
    _apply_units_table(_last_units)

func _on_objective_radius_toggled(pressed: bool) -> void:
    map_view.set_show_objective_radius(pressed)

func _on_map_unit_selected(side: String, unit_id: int) -> void:
    _selected_unit_key = {"side": side, "id": unit_id}
    _apply_units_table(_last_units)
    _update_active_context(_last_state)

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
        var unit_key = {"side": str(unit_data.get("side", "")), "id": int(unit_data.get("id", -1))}
        var is_selected := _selected_unit_key != null and _keys_equal(_selected_unit_key, unit_key)
        _add_units_cell(_to_text(unit_data.get("id", "—")), 0, HORIZONTAL_ALIGNMENT_RIGHT, is_selected)
        _add_units_cell(_format_side(unit_data.get("side")), 1, HORIZONTAL_ALIGNMENT_LEFT, is_selected)
        _add_units_cell(_to_text(unit_data.get("hp", "—")), 2, HORIZONTAL_ALIGNMENT_RIGHT, is_selected)
        _add_units_cell(_to_text(unit_data.get("models", "—")), 3, HORIZONTAL_ALIGNMENT_RIGHT, is_selected)
        var x_value = unit_data.get("x")
        var y_value = unit_data.get("y")
        var coord_text := "—"
        if x_value != null and y_value != null:
            coord_text = "(%s, %s)" % [str(x_value), str(y_value)]
        _add_units_cell(coord_text, 4, HORIZONTAL_ALIGNMENT_LEFT, is_selected)

    if units.is_empty():
        _add_units_cell("—", 0, HORIZONTAL_ALIGNMENT_RIGHT, false)
        _add_units_cell("—", 1, HORIZONTAL_ALIGNMENT_LEFT, false)
        _add_units_cell("—", 2, HORIZONTAL_ALIGNMENT_RIGHT, false)
        _add_units_cell("—", 3, HORIZONTAL_ALIGNMENT_RIGHT, false)
        _add_units_cell("—", 4, HORIZONTAL_ALIGNMENT_LEFT, false)

func _add_units_cell(text: String, column_index: int, alignment: HorizontalAlignment, selected: bool) -> void:
    var label := Label.new()
    label.text = text
    if column_index >= 0 and column_index < _units_column_widths.size():
        label.custom_minimum_size = Vector2(_units_column_widths[column_index], 0)
    label.horizontal_alignment = alignment
    label.add_theme_font_size_override("font_size", _scaled_font_size(BASE_UNITS_FONT_SIZE))
    if selected:
        label.add_theme_color_override("font_color", SELECT_TEXT_COLOR)
    units_table.add_child(label)

func _calculate_ui_scale() -> float:
    var size := get_viewport().get_visible_rect().size
    if size.x <= 0 or size.y <= 0:
        return 1.0
    var width_scale := size.x / BASE_SCREEN_SIZE.x
    var height_scale := size.y / BASE_SCREEN_SIZE.y
    return max(1.0, min(width_scale, height_scale))

func _scaled_font_size(base_size: int) -> int:
    return int(round(float(base_size) * _ui_scale))

func _apply_font_size(control: Control, base_size: int) -> void:
    if control == null:
        return
    control.add_theme_font_size_override("font_size", _scaled_font_size(base_size))

func _apply_ui_scale() -> void:
    main_split.split_offset = int(round(BASE_SPLIT_OFFSET * _ui_scale))
    top_split.split_offset = int(round(BASE_TOP_SPLIT_OFFSET * _ui_scale))
    left_panel.custom_minimum_size = Vector2(BASE_LEFT_PANEL_WIDTH * _ui_scale, 0)
    right_panel.custom_minimum_size = Vector2(BASE_RIGHT_PANEL_WIDTH * _ui_scale, 0)
    map_view.custom_minimum_size = BASE_MAP_MIN_SIZE * _ui_scale
    map_view.set_ui_scale(_ui_scale)
    right_content.add_theme_constant_override("separation", int(round(BASE_RIGHT_CONTENT_SEPARATION * _ui_scale)))
    status_content.add_theme_constant_override("separation", int(round(BASE_STATUS_SEPARATION * _ui_scale)))
    points_content.add_theme_constant_override("separation", int(round(BASE_POINTS_SEPARATION * _ui_scale)))
    units_content.add_theme_constant_override("separation", int(round(BASE_UNITS_SEPARATION * _ui_scale)))
    legend_content.add_theme_constant_override("separation", int(round(BASE_LEGEND_SEPARATION * _ui_scale)))
    legend_list.add_theme_constant_override("separation", int(round(BASE_LEGEND_LIST_SEPARATION * _ui_scale)))
    commands_content.add_theme_constant_override("separation", int(round(BASE_COMMANDS_SEPARATION * _ui_scale)))
    log_group.custom_minimum_size = Vector2(0, BASE_LOG_GROUP_HEIGHT * _ui_scale)
    log_tabs_container.custom_minimum_size = Vector2(0, BASE_LOG_TABS_HEIGHT * _ui_scale)
    legend_player_swatch.custom_minimum_size = Vector2(BASE_SWATCH_SIZE * _ui_scale, BASE_SWATCH_SIZE * _ui_scale)
    legend_model_swatch.custom_minimum_size = Vector2(BASE_SWATCH_SIZE * _ui_scale, BASE_SWATCH_SIZE * _ui_scale)
    legend_objective_swatch.custom_minimum_size = Vector2(BASE_SWATCH_SIZE * _ui_scale, BASE_SWATCH_SIZE * _ui_scale)

    _apply_font_size(fit_button, 12)
    _apply_font_size(objective_radius_toggle, 12)
    _apply_font_size(status_title, 16)
    _apply_font_size(round_label, 12)
    _apply_font_size(turn_label, 12)
    _apply_font_size(phase_label, 12)
    _apply_font_size(active_label, 12)
    _apply_font_size(points_title, 16)
    _apply_font_size(player_vp_label, 12)
    _apply_font_size(model_vp_label, 12)
    _apply_font_size(player_cp_label, 12)
    _apply_font_size(model_cp_label, 12)
    _apply_font_size(units_title, 16)
    _apply_font_size(legend_title, 16)
    _apply_font_size(commands_title, 16)
    _apply_font_size(command_prompt, 12)
    _apply_font_size(command_hint, 11)
    _apply_font_size(command_input, 12)
    _apply_font_size(command_send, 12)
    _apply_font_size(log_title, 14)
    log_tabs_container.add_theme_font_size_override("font_size", _scaled_font_size(12))
    for idx in range(log_tabs_container.get_tab_count()):
        var tab := log_tabs_container.get_tab_control(idx)
        if tab is TextEdit:
            tab.add_theme_font_size_override("font_size", _scaled_font_size(12))

    _units_column_widths.clear()
    for width in BASE_UNITS_COLUMN_WIDTHS:
        _units_column_widths.append(int(round(float(width) * _ui_scale)))

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

func _update_active_context(state: Dictionary) -> void:
    var unit_key = _resolve_active_unit(state)
    if unit_key == null and _selected_unit_key != null:
        unit_key = _selected_unit_key
    var active_unit = _find_unit_by_key(unit_key)
    var phase = null
    if state.has("phase"):
        phase = state.get("phase")
    var move_range = null
    var shoot_range = null
    if _is_movement_phase(phase):
        move_range = _resolve_move_range(active_unit)
    if _is_shooting_phase(phase):
        shoot_range = _resolve_weapon_range(active_unit)
    var targets = null
    if state.has("available_targets"):
        targets = state.get("available_targets")
    var active_unit_id = unit_key.get("id") if unit_key != null else null
    var active_unit_side = unit_key.get("side") if unit_key != null else null
    map_view.set_active_context(
        active_unit_id,
        active_unit_side,
        phase,
        move_range,
        shoot_range,
        targets
    )

func _resolve_active_unit(state: Dictionary):
    if state.has("active_unit") and state.get("active_unit") is Dictionary:
        var active_data: Dictionary = state.get("active_unit")
        var side = active_data.get("side")
        var unit_id = active_data.get("id")
        if side != null and unit_id != null:
            return {"side": str(side), "id": int(unit_id)}
    if state.has("active_unit_side") and state.has("active_unit_id"):
        return {"side": str(state.get("active_unit_side")), "id": int(state.get("active_unit_id"))}
    return null

func _resolve_move_range(unit: Dictionary):
    if unit == null:
        return null
    for key in ["move", "movement", "move_range", "speed"]:
        var value = unit.get(key)
        if value is int or value is float:
            return int(value)
    return 6

func _resolve_weapon_range(unit: Dictionary):
    if unit == null:
        return null
    for key in ["range", "weapon_range", "shoot_range", "shooting_range"]:
        var value = unit.get(key)
        if value is int or value is float:
            return int(value)
    return 12

func _is_movement_phase(phase_value) -> bool:
    var phase_text := str(phase_value if phase_value != null else "").to_lower()
    return "move" in phase_text or "движ" in phase_text or "movement" in phase_text

func _is_shooting_phase(phase_value) -> bool:
    var phase_text := str(phase_value if phase_value != null else "").to_lower()
    return "shoot" in phase_text or "стрел" in phase_text or "shooting" in phase_text

func _find_unit_by_key(unit_key):
    if unit_key == null:
        return null
    for unit in _last_units:
        if not unit is Dictionary:
            continue
        var unit_data: Dictionary = unit
        var key = {"side": str(unit_data.get("side", "")), "id": int(unit_data.get("id", -1))}
        if _keys_equal(unit_key, key):
            return unit_data
    return null

func _keys_equal(a, b) -> bool:
    if a == null or b == null:
        return false
    return str(a.get("side", "")) == str(b.get("side", "")) and int(a.get("id", -1)) == int(b.get("id", -1))
