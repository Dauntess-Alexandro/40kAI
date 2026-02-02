extends Control

const TAB_NAMES := ["Все", "Ход", "Стрельба", "Ближний бой", "Кубы", "Ошибки"]
const UNITS_COLUMNS := 5
const BASE_UNITS_COLUMN_WIDTHS := [90, 60, 180, 60, 70]
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
const LOG_FILE_NAME := "LOGS_FOR_AGENTS.md"
const LOG_FILE_ROTATED := "LOGS_FOR_AGENTS.old.md"
const LOG_FILE_MAX_BYTES := 5 * 1024 * 1024

@onready var round_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/StatusContent/RoundLabel
@onready var turn_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/StatusContent/TurnLabel
@onready var phase_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/StatusContent/PhaseLabel
@onready var active_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/StatusGroup/StatusContent/ActiveLabel
@onready var player_vp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PointsContent/PlayerVPLabel
@onready var model_vp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PointsContent/ModelVPLabel
@onready var player_cp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PointsContent/PlayerCPLabel
@onready var model_cp_label: Label = $MainSplit/TopSplit/RightPanel/RightContent/PointsGroup/PointsContent/ModelCPLabel
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
@onready var legend_move_swatch: ColorRect = $MainSplit/TopSplit/RightPanel/RightContent/LegendGroup/LegendContent/LegendList/LegendMove/LegendMoveSwatch
@onready var legend_shoot_swatch: ColorRect = $MainSplit/TopSplit/RightPanel/RightContent/LegendGroup/LegendContent/LegendList/LegendShoot/LegendShootSwatch
@onready var commands_title: Label = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandsTitle
@onready var commands_content: VBoxContainer = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent
@onready var command_hint: Label = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandHint
@onready var command_stack: TabContainer = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack
@onready var command_text_input: LineEdit = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack/TextPage/CommandInput
@onready var command_text_send: Button = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack/TextPage/CommandSend
@onready var direction_up: Button = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack/DirectionPage/DirectionUp
@onready var direction_left: Button = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack/DirectionPage/DirectionLeft
@onready var direction_none: Button = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack/DirectionPage/DirectionNone
@onready var direction_right: Button = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack/DirectionPage/DirectionRight
@onready var direction_down: Button = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack/DirectionPage/DirectionDown
@onready var bool_yes: Button = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack/BoolPage/BoolYes
@onready var bool_no: Button = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack/BoolPage/BoolNo
@onready var int_spin: SpinBox = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack/IntPage/IntSpin
@onready var int_ok: Button = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack/IntPage/IntOk
@onready var choice_option: OptionButton = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack/ChoicePage/ChoiceOption
@onready var choice_ok: Button = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandStack/ChoicePage/ChoiceOk
@onready var units_table: Tree = $MainSplit/TopSplit/RightPanel/RightContent/UnitsGroup/UnitsContent/UnitsTable
@onready var command_prompt: Label = $MainSplit/TopSplit/RightPanel/RightContent/CommandsGroup/CommandsContent/CommandPrompt
@onready var log_group: VBoxContainer = $MainSplit/LogGroup
@onready var log_only_current_turn: CheckBox = $MainSplit/LogGroup/LogControls/LogOnlyTurn
@onready var log_copy_turn: Button = $MainSplit/LogGroup/LogControls/LogCopyTurn
@onready var log_clear: Button = $MainSplit/LogGroup/LogControls/LogClear
@onready var log_title: Label = $MainSplit/LogGroup/LogTitle
@onready var log_tabs_container: TabContainer = $MainSplit/LogGroup/LogTabs

var _state_reader: StateReader
var _command_path := DEFAULT_COMMAND_PATH
var _selected_unit_key = null
var _last_units: Array = []
var _last_state: Dictionary = {}
var _ui_scale := 1.0
var _units_column_widths: Array = []
var _units_sort_column := 0
var _units_sort_ascending := true
var _unit_item_by_key := {}
var _pending_request = null
var _command_pages := {}
var _log_entries := []
var _current_turn_number = null
var _log_tail_snapshot = null
var _log_tabs := {}
var _log_tab_defs := [
    ["all", "Все"],
    ["turn", "Ход"],
    ["shooting", "Стрельба"],
    ["fight", "Ближний бой"],
    ["dice", "Кубы"],
    ["errors", "Ошибки"],
]
var _log_file_path := ""

func _ready() -> void:
    _ui_scale = _calculate_ui_scale()
    _apply_ui_scale()
    _configure_log_tabs()
    _configure_units_headers()
    _configure_units_tree()
    _init_log_viewer()
    objective_radius_toggle.toggled.connect(_on_objective_radius_toggled)
    map_view.set_show_objective_radius(objective_radius_toggle.button_pressed)
    map_view.unit_selected.connect(_on_map_unit_selected)
    command_text_input.text_submitted.connect(_on_command_submitted)
    command_text_input.gui_input.connect(_on_command_input_gui)
    command_text_send.pressed.connect(_on_command_send_pressed)
    direction_up.pressed.connect(func(): _submit_answer("up"))
    direction_down.pressed.connect(func(): _submit_answer("down"))
    direction_left.pressed.connect(func(): _submit_answer("left"))
    direction_right.pressed.connect(func(): _submit_answer("right"))
    direction_none.pressed.connect(func(): _submit_answer("none"))
    bool_yes.pressed.connect(func(): _submit_answer("y"))
    bool_no.pressed.connect(func(): _submit_answer("n"))
    int_ok.pressed.connect(func(): _submit_answer(int(int_spin.value)))
    choice_ok.pressed.connect(_submit_choice)
    units_table.item_selected.connect(_on_units_table_selected)
    units_table.column_title_clicked.connect(_on_units_column_clicked)
    log_only_current_turn.toggled.connect(_refresh_log_views)
    log_copy_turn.pressed.connect(_copy_current_turn)
    log_clear.pressed.connect(_clear_log_viewer)
    var env_command_path := OS.get_environment("COMMAND_PATH")
    if env_command_path != "":
        _command_path = env_command_path
    _log_file_path = ProjectSettings.globalize_path("res://../%s" % LOG_FILE_NAME)
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
        if not is_node_ready() or main_split == null:
            return
        var new_scale := _calculate_ui_scale()
        if absf(new_scale - _ui_scale) >= 0.01:
            _ui_scale = new_scale
            _apply_ui_scale()
            _configure_units_headers()
            _apply_units_table(_last_units)

func _configure_log_tabs() -> void:
    for idx in range(min(log_tabs_container.get_tab_count(), TAB_NAMES.size())):
        log_tabs_container.set_tab_title(idx, TAB_NAMES[idx])

func _init_log_viewer() -> void:
    _log_tabs = {
        "all": log_tabs_container.get_node("AllTab"),
        "turn": log_tabs_container.get_node("TurnTab"),
        "shooting": log_tabs_container.get_node("ShootingTab"),
        "fight": log_tabs_container.get_node("FightTab"),
        "dice": log_tabs_container.get_node("DiceTab"),
        "errors": log_tabs_container.get_node("ErrorsTab"),
    }
    for key in _log_tabs.keys():
        var view := _log_tabs[key]
        if view is TextEdit:
            view.editable = false

func _configure_units_headers() -> void:
    if units_table == null:
        return
    units_table.set_column_title(0, "Сторона")
    units_table.set_column_title(1, "ID")
    units_table.set_column_title(2, "Имя")
    units_table.set_column_title(3, "HP")
    units_table.set_column_title(4, "Модели")
    for idx in range(UNITS_COLUMNS):
        if idx >= 0 and idx < _units_column_widths.size():
            units_table.set_column_custom_minimum_width(idx, _units_column_widths[idx])
        units_table.set_column_title_alignment(idx, HORIZONTAL_ALIGNMENT_LEFT)
    units_table.add_theme_font_size_override("font_size", _scaled_font_size(BASE_UNITS_FONT_SIZE))

func _configure_units_tree() -> void:
    units_table.columns = UNITS_COLUMNS
    units_table.hide_root = true
    units_table.set_column_titles_visible(true)

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

    _update_log(state.get("log_tail", []))
    map_view.set_state(state)
    _last_units = state.get("units", []) if state.get("units") is Array else []
    _set_request(state.get("request") if state is Dictionary else null)
    _update_active_context(state)
    _apply_units_table(_last_units)

func _on_objective_radius_toggled(pressed: bool) -> void:
    map_view.set_show_objective_radius(pressed)

func _on_map_unit_selected(side: String, unit_id: int) -> void:
    _selected_unit_key = {"side": side, "id": unit_id}
    _apply_units_table(_last_units)
    _update_active_context(_last_state)
    _select_row_for_unit(side, unit_id)

func _on_command_send_pressed() -> void:
    _submit_text()

func _on_command_submitted(text: String) -> void:
    _submit_text()

func _on_command_input_gui(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and event.ctrl_pressed and event.keycode == KEY_L:
        command_text_input.clear()
        command_prompt.text = "Команда очищена."

func _submit_text() -> void:
    var trimmed := command_text_input.text.strip_edges()
    if trimmed == "":
        command_prompt.text = "Ожидаю команду..."
        return
    if _pending_request != null and _pending_request.get("kind") == "dice":
        var count = int(_pending_request.get("count", 0))
        var min_value = int(_pending_request.get("min_value", 1))
        var max_value = int(_pending_request.get("max_value", 6))
        var parsed = _parse_dice_values(trimmed, count, min_value, max_value)
        if parsed.is_empty() and count > 0:
            command_prompt.text = "Ошибка ввода кубов в панели «Команды»: " \
                + "нужно %s, введено %s. Что делать дальше: исправьте ввод и отправьте снова.\n%s" \
                % [str(count), str(_count_dice_entries(trimmed)), _pending_request.get("prompt", "")]
            return
        command_text_input.clear()
        _submit_answer(parsed)
        return
    command_text_input.clear()
    _submit_answer(trimmed)

func _submit_choice() -> void:
    _submit_answer(choice_option.get_item_text(choice_option.selected))

func _submit_answer(value) -> void:
    if _pending_request == null and (value == null or str(value) == ""):
        return
    var payload := _format_command_value(value)
    if payload == "":
        command_prompt.text = "Команда не отправлена: пустой ввод."
        return
    if _write_command(payload):
        command_prompt.text = "Команда отправлена: %s" % payload
    else:
        command_prompt.text = "Не удалось отправить команду (проверьте путь: %s)." % _command_path

func _format_command_value(value) -> String:
    if value is Array:
        return " ".join(value.map(func(entry): return str(entry)))
    if value is bool:
        return "y" if value else "n"
    return str(value).strip_edges()

func _set_request(request) -> void:
    _pending_request = null
    if not (request is Dictionary):
        command_stack.disabled = false
        command_prompt.text = "Ожидаю команду..."
        command_hint.text = "Горячие клавиши: Enter — отправить"
        command_text_input.placeholder_text = "Введите команду..."
        _show_command_page("text")
        return
    _pending_request = request
    var prompt = str(request.get("prompt", "Ожидаю команду..."))
    command_prompt.text = prompt
    command_stack.disabled = false
    var kind = str(request.get("kind", "text"))
    if kind == "none":
        command_stack.disabled = true
        command_hint.text = "Горячие клавиши: —"
        return
    _show_command_page(kind)
    if kind == "int":
        var min_value = int(request.get("min_value", 0))
        var max_value = int(request.get("max_value", 999))
        int_spin.min_value = min_value
        int_spin.max_value = max_value
        int_spin.value = min_value
    elif kind == "choice":
        choice_option.clear()
        var options = request.get("options", [])
        if options is Array:
            for opt in options:
                choice_option.add_item(str(opt))
    elif kind == "dice":
        var count = int(request.get("count", 0))
        var example_values := []
        for idx in range(count):
            example_values.append(str((idx % 6) + 1))
        var spaced = " ".join(example_values)
        var comma = ",".join(example_values)
        var compact = "".join(example_values)
        var hint = "Например: %s или %s" % [spaced, comma]
        if compact != "":
            hint += " или %s" % compact
        command_text_input.placeholder_text = hint
    else:
        command_text_input.placeholder_text = "Введите команду..."
    _update_command_hint(kind)

func _show_command_page(kind: String) -> void:
    if _command_pages.is_empty():
        _command_pages = {
            "text": command_stack.get_tab_idx_from_control(command_stack.get_node("TextPage")),
            "direction": command_stack.get_tab_idx_from_control(command_stack.get_node("DirectionPage")),
            "bool": command_stack.get_tab_idx_from_control(command_stack.get_node("BoolPage")),
            "int": command_stack.get_tab_idx_from_control(command_stack.get_node("IntPage")),
            "choice": command_stack.get_tab_idx_from_control(command_stack.get_node("ChoicePage")),
            "dice": command_stack.get_tab_idx_from_control(command_stack.get_node("TextPage")),
        }
    var target = kind if _command_pages.has(kind) else "text"
    command_stack.current_tab = _command_pages[target]

func _update_command_hint(kind: String) -> void:
    if kind == "direction":
        command_hint.text = "Горячие клавиши: ↑ ↓ ← →, пробел/0 — нет"
    elif kind == "bool":
        command_hint.text = "Горячие клавиши: Y — да, N — нет"
    elif kind == "int":
        command_hint.text = "Горячие клавиши: Enter — отправить"
    elif kind == "choice":
        command_hint.text = "Горячие клавиши: Enter — выбрать"
    else:
        command_hint.text = "Горячие клавиши: Enter — отправить"

func _parse_dice_values(text: String, count: int, min_value: int, max_value: int) -> Array:
    var stripped := text.strip_edges()
    if stripped == "":
        return []
    var parts := []
    if stripped.is_valid_int():
        for ch in stripped:
            parts.append(ch)
    else:
        var raw = stripped.split(",", false)
        for entry in raw:
            var sub = entry.strip_edges()
            if sub == "":
                continue
            for piece in sub.split(" ", false):
                if piece != "":
                    parts.append(piece)
    var values := []
    for part in parts:
        if not String(part).is_valid_int():
            return []
        var value = int(part)
        if value < min_value or value > max_value:
            return []
        values.append(value)
    if count > 0 and values.size() != count:
        return []
    return values

func _count_dice_entries(text: String) -> int:
    var stripped := text.strip_edges()
    if stripped == "":
        return 0
    if stripped.is_valid_int():
        return stripped.length()
    var parts := []
    for chunk in stripped.split(",", false):
        for piece in chunk.split(" ", false):
            if piece != "":
                parts.append(piece)
    return parts.size()

func _unhandled_input(event: InputEvent) -> void:
    if not (event is InputEventKey and event.pressed):
        return
    if _pending_request == null:
        return
    var kind = str(_pending_request.get("kind", ""))
    var key = event.keycode
    if kind == "direction":
        if key == KEY_UP:
            _submit_answer("up")
        elif key == KEY_DOWN:
            _submit_answer("down")
        elif key == KEY_LEFT:
            _submit_answer("left")
        elif key == KEY_RIGHT:
            _submit_answer("right")
        elif key == KEY_SPACE or key == KEY_0:
            _submit_answer("none")
    elif kind == "bool":
        if key == KEY_Y:
            _submit_answer("y")
        elif key == KEY_N:
            _submit_answer("n")
        elif key == KEY_ESCAPE:
            command_text_input.clear()
    elif kind == "int":
        if key == KEY_ENTER or key == KEY_KP_ENTER:
            _submit_answer(int(int_spin.value))
    elif kind == "choice":
        if key == KEY_ENTER or key == KEY_KP_ENTER:
            _submit_choice()

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

func _make_unit_key(side: String, unit_id: int) -> String:
    return "%s:%s" % [side, str(unit_id)]

func _sort_units(units: Array) -> Array:
    var sorted_units := units.duplicate()
    sorted_units.sort_custom(func(a, b):
        var a_value = _unit_sort_value(a, _units_sort_column)
        var b_value = _unit_sort_value(b, _units_sort_column)
        if a_value == b_value:
            return false
        return a_value < b_value if _units_sort_ascending else a_value > b_value
    )
    return sorted_units

func _unit_sort_value(unit_data, column: int):
    if not unit_data is Dictionary:
        return ""
    var unit: Dictionary = unit_data
    match column:
        0:
            return str(unit.get("side", ""))
        1:
            return int(unit.get("id", -1))
        2:
            return str(unit.get("name", ""))
        3:
            return float(unit.get("hp", -1))
        4:
            return int(unit.get("models", -1))
        _:
            return ""

func _on_units_column_clicked(column: int) -> void:
    if _units_sort_column == column:
        _units_sort_ascending = not _units_sort_ascending
    else:
        _units_sort_column = column
        _units_sort_ascending = true
    _apply_units_table(_last_units)

func _on_units_table_selected() -> void:
    var item := units_table.get_selected()
    if item == null:
        return
    var unit_key = item.get_metadata(0)
    if unit_key == null:
        return
    _selected_unit_key = unit_key
    map_view.set_selected_unit(unit_key.get("side"), unit_key.get("id"))
    _update_active_context(_last_state)

func _select_row_for_unit(side: String, unit_id: int) -> void:
    var key = _make_unit_key(side, unit_id)
    if not _unit_item_by_key.has(key):
        return
    var item: TreeItem = _unit_item_by_key[key]
    units_table.set_selected(item, 0)

func _apply_units_table(units_value) -> void:
    units_table.clear()
    _unit_item_by_key.clear()
    var units: Array = []
    if units_value is Array:
        units = units_value
    var sorted_units = _sort_units(units)
    var root = units_table.create_item()
    for unit in sorted_units:
        if not unit is Dictionary:
            continue
        var unit_data: Dictionary = unit
        var side_value = str(unit_data.get("side", ""))
        var unit_id = int(unit_data.get("id", -1))
        var unit_key = {"side": side_value, "id": unit_id}
        var item := units_table.create_item(root)
        item.set_text(0, _format_side(side_value))
        item.set_text(1, _to_text(unit_id))
        item.set_text(2, _to_text(unit_data.get("name", "—")))
        item.set_text(3, _to_text(unit_data.get("hp", "—")))
        item.set_text(4, _to_text(unit_data.get("models", "—")))
        item.set_metadata(0, unit_key)
        _unit_item_by_key[_make_unit_key(side_value, unit_id)] = item
        if _selected_unit_key != null and _keys_equal(_selected_unit_key, unit_key):
            units_table.set_selected(item, 0)

    if units.is_empty():
        var empty_item := units_table.create_item(root)
        for idx in range(UNITS_COLUMNS):
            empty_item.set_text(idx, "—")

func _update_log(lines) -> void:
    if not (lines is Array):
        return
    var text_lines := []
    for line in lines:
        text_lines.append(str(line))
    if _log_tail_snapshot == text_lines:
        return
    if _log_entries.is_empty():
        _reset_log_lines(text_lines, true)
        _log_tail_snapshot = text_lines
        return
    var existing := []
    for entry in _log_entries:
        existing.append(entry.get("text", ""))
    if text_lines.size() >= existing.size() and text_lines.slice(0, existing.size()) == existing:
        for line in text_lines.slice(existing.size(), text_lines.size()):
            add_log_line(str(line))
        _log_tail_snapshot = text_lines
        return
    _reset_log_lines(text_lines, false)
    _log_tail_snapshot = text_lines

func _reset_log_lines(lines: Array, write_to_file: bool) -> void:
    _log_entries.clear()
    _current_turn_number = null
    for line in lines:
        if write_to_file:
            add_log_line(str(line))
        else:
            var text = str(line)
            var new_turn = _detect_turn_number(text)
            if new_turn != null:
                _current_turn_number = new_turn
            _log_entries.append({
                "text": text,
                "turn": _current_turn_number,
                "categories": _classify_line(text),
            })
    _refresh_log_views()

func add_log_line(line: String) -> void:
    var text = str(line)
    var new_turn = _detect_turn_number(text)
    if new_turn != null:
        _current_turn_number = new_turn
    var entry = {
        "text": text,
        "turn": _current_turn_number,
        "categories": _classify_line(text),
    }
    _log_entries.append(entry)
    _append_log_to_file(text)
    if _log_entries.size() > 5000:
        _log_entries = _log_entries.slice(_log_entries.size() - 5000, _log_entries.size())
        _refresh_log_views()
        return
    if new_turn != null and log_only_current_turn.button_pressed:
        _refresh_log_views()
        return
    for tab_key in _log_tabs.keys():
        if _should_show_entry(entry, tab_key):
            _append_to_view(_log_tabs[tab_key], text)

func _append_to_view(view: TextEdit, text: String) -> void:
    if view == null:
        return
    view.text += text + "\n"
    view.scroll_vertical = view.get_line_count()

func _classify_line(line: String) -> Array:
    var lowered = line.to_lower()
    var categories := []
    if _matches_any(lowered, ["боевого раунда", "фаза", "===", "iteration", "раунд", "turn"]):
        categories.append("turn")
    if _matches_any(lowered, ["[shoot]", "отчёт по стрельбе", "hit rolls", "wound", "save", "оружие", "стрельб"]):
        categories.append("shooting")
    if _matches_any(lowered, ["[fight]", "фаза боя", "melee", "атаки", "удар"]):
        categories.append("fight")
    if _matches_any(lowered, ["d6", "2d6", "d3", "бросок", "roll", "rolling", "🎲"]):
        categories.append("dice")
    if _matches_any(lowered, ["error", "traceback", "exception", "warn", "warning", "недоступен", "ошибка"]):
        categories.append("errors")
    return categories

func _matches_any(text: String, tokens: Array) -> bool:
    for token in tokens:
        if text.find(str(token)) != -1:
            return true
    return false

func _detect_turn_number(line: String):
    var regex = RegEx.new()
    regex.compile("боевого раунда\\s*(\\d+)")
    var regex_match = regex.search(line)
    if regex_match:
        return int(regex_match.get_string(1))
    regex.compile("\\bturn\\s*(\\d+)")
    regex_match = regex.search(line)
    if regex_match:
        return int(regex_match.get_string(1))
    regex.compile("\\bраунд\\s*(\\d+)")
    regex_match = regex.search(line)
    if regex_match:
        return int(regex_match.get_string(1))
    return null

func _should_show_entry(entry: Dictionary, tab_key: String) -> bool:
    if tab_key != "all" and not entry.get("categories", []).has(tab_key):
        return false
    if not log_only_current_turn.button_pressed:
        return true
    if _current_turn_number == null:
        return true
    return entry.get("turn") == _current_turn_number

func _refresh_log_views() -> void:
    for view in _log_tabs.values():
        if view is TextEdit:
            view.text = ""
    var grouped := {
        "all": [],
        "turn": [],
        "shooting": [],
        "fight": [],
        "dice": [],
        "errors": [],
    }
    for entry in _log_entries:
        for key in grouped.keys():
            if _should_show_entry(entry, key):
                grouped[key].append(entry.get("text", ""))
    for key in grouped.keys():
        if _log_tabs.has(key):
            var view: TextEdit = _log_tabs[key]
            if grouped[key].size() > 0:
                view.text = "\n".join(grouped[key]) + "\n"
            view.scroll_vertical = view.get_line_count()

func _clear_log_viewer() -> void:
    _log_entries.clear()
    _current_turn_number = null
    _log_tail_snapshot = null
    _refresh_log_views()

func _collect_current_turn_logs() -> String:
    if _current_turn_number == null:
        return "\n".join(_log_entries.map(func(entry): return entry.get("text", "")))
    var lines := []
    for entry in _log_entries:
        if entry.get("turn") == _current_turn_number:
            lines.append(entry.get("text", ""))
    return "\n".join(lines)

func _copy_current_turn() -> void:
    DisplayServer.clipboard_set(_collect_current_turn_logs())

func _append_log_to_file(line: String) -> void:
    _rotate_log_file_if_needed()
    var timestamp = Time.get_datetime_string_from_system(false, true)
    var file := FileAccess.open(_log_file_path, FileAccess.READ_WRITE)
    if file == null:
        file = FileAccess.open(_log_file_path, FileAccess.WRITE)
    if file == null:
        return
    file.seek_end()
    file.store_line("%s | %s" % [timestamp, line])
    file.close()

func _rotate_log_file_if_needed() -> void:
    if not FileAccess.file_exists(_log_file_path):
        return
    var file := FileAccess.open(_log_file_path, FileAccess.READ)
    if file == null:
        return
    var size = file.get_length()
    file.close()
    if size <= LOG_FILE_MAX_BYTES:
        return
    var rotated_path = ProjectSettings.globalize_path("res://../%s" % LOG_FILE_ROTATED)
    var dir := DirAccess.open("res://../")
    if dir == null:
        return
    if FileAccess.file_exists(rotated_path):
        dir.remove(LOG_FILE_ROTATED)
    dir.rename(LOG_FILE_NAME, LOG_FILE_ROTATED)

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
    if main_split != null:
        main_split.split_offset = int(round(BASE_SPLIT_OFFSET * _ui_scale))
    if top_split != null:
        top_split.split_offset = int(round(BASE_TOP_SPLIT_OFFSET * _ui_scale))
    if left_panel != null:
        left_panel.custom_minimum_size = Vector2(BASE_LEFT_PANEL_WIDTH * _ui_scale, 0)
    if right_panel != null:
        right_panel.custom_minimum_size = Vector2(BASE_RIGHT_PANEL_WIDTH * _ui_scale, 0)
    if map_view != null:
        map_view.custom_minimum_size = BASE_MAP_MIN_SIZE * _ui_scale
        map_view.set_ui_scale(_ui_scale)
    if right_content != null:
        right_content.add_theme_constant_override("separation", int(round(BASE_RIGHT_CONTENT_SEPARATION * _ui_scale)))
    if status_content != null:
        status_content.add_theme_constant_override("separation", int(round(BASE_STATUS_SEPARATION * _ui_scale)))
    if points_content != null:
        points_content.add_theme_constant_override("separation", int(round(BASE_POINTS_SEPARATION * _ui_scale)))
    if units_content != null:
        units_content.add_theme_constant_override("separation", int(round(BASE_UNITS_SEPARATION * _ui_scale)))
    if legend_content != null:
        legend_content.add_theme_constant_override("separation", int(round(BASE_LEGEND_SEPARATION * _ui_scale)))
    if legend_list != null:
        legend_list.add_theme_constant_override("separation", int(round(BASE_LEGEND_LIST_SEPARATION * _ui_scale)))
    if commands_content != null:
        commands_content.add_theme_constant_override("separation", int(round(BASE_COMMANDS_SEPARATION * _ui_scale)))
    if log_group != null:
        log_group.custom_minimum_size = Vector2(0, BASE_LOG_GROUP_HEIGHT * _ui_scale)
    if log_tabs_container != null:
        log_tabs_container.custom_minimum_size = Vector2(0, BASE_LOG_TABS_HEIGHT * _ui_scale)
    if legend_player_swatch != null:
        legend_player_swatch.custom_minimum_size = Vector2(BASE_SWATCH_SIZE * _ui_scale, BASE_SWATCH_SIZE * _ui_scale)
    if legend_model_swatch != null:
        legend_model_swatch.custom_minimum_size = Vector2(BASE_SWATCH_SIZE * _ui_scale, BASE_SWATCH_SIZE * _ui_scale)
    if legend_objective_swatch != null:
        legend_objective_swatch.custom_minimum_size = Vector2(BASE_SWATCH_SIZE * _ui_scale, BASE_SWATCH_SIZE * _ui_scale)
    if legend_move_swatch != null:
        legend_move_swatch.custom_minimum_size = Vector2(BASE_SWATCH_SIZE * _ui_scale, BASE_SWATCH_SIZE * _ui_scale)
    if legend_shoot_swatch != null:
        legend_shoot_swatch.custom_minimum_size = Vector2(BASE_SWATCH_SIZE * _ui_scale, BASE_SWATCH_SIZE * _ui_scale)

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
    _apply_font_size(command_text_input, 12)
    _apply_font_size(command_text_send, 12)
    _apply_font_size(direction_up, 12)
    _apply_font_size(direction_left, 12)
    _apply_font_size(direction_none, 12)
    _apply_font_size(direction_right, 12)
    _apply_font_size(direction_down, 12)
    _apply_font_size(bool_yes, 12)
    _apply_font_size(bool_no, 12)
    _apply_font_size(int_spin, 12)
    _apply_font_size(int_ok, 12)
    _apply_font_size(choice_option, 12)
    _apply_font_size(choice_ok, 12)
    _apply_font_size(log_title, 14)
    _apply_font_size(log_only_current_turn, 12)
    _apply_font_size(log_copy_turn, 12)
    _apply_font_size(log_clear, 12)
    if log_tabs_container != null:
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
    var prompt_unit_id = _extract_unit_id(_pending_request.get("prompt") if _pending_request is Dictionary else "")
    if prompt_unit_id != null:
        for unit in _last_units:
            if unit is Dictionary and int(unit.get("id", -1)) == prompt_unit_id:
                return {"side": str(unit.get("side", "")), "id": int(unit.get("id", -1))}
    return null

func _extract_unit_id(prompt: String):
    if prompt == null or prompt == "":
        return null
    var regex = RegEx.new()
    regex.compile("(?:юнит|unit)\\s*#?\\s*(\\d+)")
    var regex_match = regex.search(prompt)
    if regex_match:
        return int(regex_match.get_string(1))
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
