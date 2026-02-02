extends Node2D

const DEFAULT_ROWS := 20
const DEFAULT_COLS := 20
const CELL_SIZE := 40
const STATE_PATH := "../state.json"
const ZOOM_MIN := 0.2
const ZOOM_MAX := 4.0
const ZOOM_STEP := 0.1

var _state_loader := StateLoader.new()
var _state_data: Dictionary = {}
var _rows := DEFAULT_ROWS
var _cols := DEFAULT_COLS
var _reload_timer: Timer

@onready var _camera: Camera2D = $Camera2D

func _ready() -> void:
	_setup_timer()
	_reload_state()

func _setup_timer() -> void:
	_reload_timer = Timer.new()
	_reload_timer.wait_time = 0.3
	_reload_timer.autostart = true
	_reload_timer.one_shot = false
	_reload_timer.timeout.connect(_reload_state)
	add_child(_reload_timer)

func _reload_state() -> void:
	var path := _get_state_path()
	var data := _state_loader.load_state(path)
	if data.is_empty():
		return

	_state_data = data
	var board_data := _state_data.get("board", {})
	if typeof(board_data) == TYPE_DICTIONARY:
		_rows = int(board_data.get("rows", DEFAULT_ROWS))
		_cols = int(board_data.get("cols", DEFAULT_COLS))
	else:
		_rows = DEFAULT_ROWS
		_cols = DEFAULT_COLS
	update()

func _get_state_path() -> String:
	# Используем относительный путь, как указано в требованиях.
	return ProjectSettings.globalize_path("res://" + STATE_PATH)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_R:
			_reload_state()
			return

	if event is InputEventMouseButton and event.pressed:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			_adjust_zoom(1.0 - ZOOM_STEP)
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			_adjust_zoom(1.0 + ZOOM_STEP)

func _adjust_zoom(multiplier: float) -> void:
	var new_zoom := _camera.zoom * multiplier
	new_zoom.x = clamp(new_zoom.x, ZOOM_MIN, ZOOM_MAX)
	new_zoom.y = clamp(new_zoom.y, ZOOM_MIN, ZOOM_MAX)
	_camera.zoom = new_zoom

func _draw() -> void:
	_draw_grid()
	_draw_objectives()
	_draw_units()

func _draw_grid() -> void:
	var grid_color := Color(0.35, 0.35, 0.35)
	var width := _cols * CELL_SIZE
	var height := _rows * CELL_SIZE

	for row in range(_rows + 1):
		var y := row * CELL_SIZE
		draw_line(Vector2(0, y), Vector2(width, y), grid_color)

	for col in range(_cols + 1):
		var x := col * CELL_SIZE
		draw_line(Vector2(x, 0), Vector2(x, height), grid_color)

func _draw_units() -> void:
	var units := _state_data.get("units", [])
	if typeof(units) != TYPE_ARRAY:
		return

	var font := ThemeDB.fallback_font
	var font_size := 14

	for unit in units:
		if typeof(unit) != TYPE_DICTIONARY:
			continue

		var grid_pos := _extract_unit_position(unit)
		if grid_pos == null:
			continue

		var rect := Rect2(grid_pos.x * CELL_SIZE, grid_pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
		var faction := str(unit.get("faction", "unknown")).to_lower()
		var color := _get_faction_color(faction)
		draw_rect(rect, color)

		var label := str(unit.get("name", unit.get("id", "")))
		if label != "" and font:
			var text_pos := rect.position + Vector2(4, CELL_SIZE * 0.7)
			draw_string(font, text_pos, label, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, Color.WHITE)

func _draw_objectives() -> void:
	var objectives := _state_data.get("objectives", [])
	if typeof(objectives) != TYPE_ARRAY:
		return

	var color := Color(1.0, 0.9, 0.1)
	for objective in objectives:
		if typeof(objective) != TYPE_DICTIONARY:
			continue

		var grid_pos := _extract_position(objective.get("position", {}))
		if grid_pos == null:
			continue

		var center := Vector2((grid_pos.x + 0.5) * CELL_SIZE, (grid_pos.y + 0.5) * CELL_SIZE)
		draw_circle(center, CELL_SIZE * 0.3, color)

func _extract_unit_position(unit: Dictionary) -> Variant:
	var position := unit.get("position", null)
	return _extract_position(position)

func _extract_position(position: Variant) -> Variant:
	if typeof(position) == TYPE_DICTIONARY:
		var row := _get_first_number(position, ["r", "row", "y"])
		var col := _get_first_number(position, ["c", "col", "x"])
		if row == null or col == null:
			return null
		return Vector2(int(col), int(row))
	elif typeof(position) == TYPE_ARRAY and position.size() >= 2:
		return Vector2(int(position[0]), int(position[1]))

	return null

func _get_first_number(source: Dictionary, keys: Array) -> Variant:
	for key in keys:
		if source.has(key):
			return source[key]
	return null

func _get_faction_color(faction: String) -> Color:
	match faction:
		"player":
			return Color(0.2, 0.4, 0.9)
		"model":
			return Color(0.9, 0.2, 0.2)
		_:
			return Color(0.5, 0.5, 0.5)
