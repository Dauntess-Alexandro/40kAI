extends Control
class_name MapView

const DEFAULT_BOARD := {"width": 60, "height": 40}
const CONTROL_RADIUS_CELLS := 3
const GRID_COLOR := Color(0.2, 0.2, 0.22, 1)
const BACKGROUND_COLOR := Color(0.11, 0.1, 0.09, 1)
const PLAYER_COLOR := Color(0.26, 0.72, 1.0, 1)
const MODEL_COLOR := Color(0.96, 0.4, 0.4, 1)
const OBJECTIVE_COLOR := Color(0.95, 0.85, 0.45, 1)
const TEXT_COLOR := Color(0.92, 0.92, 0.92, 1)

var _state: Dictionary = {}
var _show_objective_radius := true

func set_state(state: Dictionary) -> void:
    _state = state if state != null else {}
    queue_redraw()

func set_show_objective_radius(visible: bool) -> void:
    _show_objective_radius = visible
    queue_redraw()

func _notification(what: int) -> void:
    if what == NOTIFICATION_RESIZED:
        queue_redraw()

func _draw() -> void:
    draw_rect(Rect2(Vector2.ZERO, size), BACKGROUND_COLOR, true)

    var board: Dictionary = {}
    var board_value = _state.get("board")
    if board_value is Dictionary:
        board = board_value
    var width: int = int(board.get("width", DEFAULT_BOARD.width))
    var height: int = int(board.get("height", DEFAULT_BOARD.height))
    if width <= 0 or height <= 0:
        return

    var cell_size: float = min(size.x / float(width), size.y / float(height))
    if cell_size <= 0:
        return

    var grid_size := Vector2(width * cell_size, height * cell_size)
    var origin := (size - grid_size) * 0.5

    _draw_grid(origin, width, height, cell_size)
    _draw_objectives(origin, cell_size)
    _draw_units(origin, cell_size)

func _draw_grid(origin: Vector2, width: int, height: int, cell_size: float) -> void:
    for x in range(width + 1):
        var from := origin + Vector2(x * cell_size, 0)
        var to := origin + Vector2(x * cell_size, height * cell_size)
        draw_line(from, to, GRID_COLOR, 1.0)
    for y in range(height + 1):
        var from := origin + Vector2(0, y * cell_size)
        var to := origin + Vector2(width * cell_size, y * cell_size)
        draw_line(from, to, GRID_COLOR, 1.0)

func _draw_units(origin: Vector2, cell_size: float) -> void:
    var units: Array = []
    var units_value = _state.get("units")
    if units_value is Array:
        units = units_value
    var occupied := {}
    for unit in units:
        var unit_data := unit as Dictionary
        var key := Vector2i(int(unit_data.get("x", -1)), int(unit_data.get("y", -1)))
        if not occupied.has(key):
            occupied[key] = []
        occupied[key].append(unit)

    var font := get_theme_default_font()
    var font_size := get_theme_default_font_size()

    for unit in units:
        var unit_data := unit as Dictionary
        var x_value = unit_data.get("x")
        var y_value = unit_data.get("y")
        if x_value == null or y_value == null:
            continue

        var x: int = int(x_value)
        var y: int = int(y_value)
        var key := Vector2i(x, y)
        var stack: Array = occupied.get(key, [])
        var offset := 0.0
        if stack.size() > 1:
            offset = (stack.find(unit) - (stack.size() - 1) * 0.5) * (cell_size * 0.15)
        var center := origin + Vector2((x + 0.5) * cell_size + offset, (y + 0.5) * cell_size - offset)

        var side_value = unit_data.get("side")
        var color := PLAYER_COLOR if side_value == "player" else MODEL_COLOR
        var radius := cell_size * 0.35
        draw_circle(center, radius, color)
        draw_arc(center, radius, 0, TAU, 32, Color(0, 0, 0, 0.4), 1.0)

        var id_text := str(unit_data.get("id", ""))
        if id_text != "":
            var text_pos := center + Vector2(-radius, -radius - 4)
            draw_string(font, text_pos, id_text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, TEXT_COLOR)

func _draw_objectives(origin: Vector2, cell_size: float) -> void:
    var objectives: Array = []
    var objectives_value = _state.get("objectives")
    if objectives_value is Array:
        objectives = objectives_value
    var font := get_theme_default_font()
    var font_size := get_theme_default_font_size()

    for objective in objectives:
        var objective_data := objective as Dictionary
        var x_value = objective_data.get("x")
        var y_value = objective_data.get("y")
        if x_value == null or y_value == null:
            continue
        var x: int = int(x_value)
        var y: int = int(y_value)
        var center := origin + Vector2((x + 0.5) * cell_size, (y + 0.5) * cell_size)
        var radius := cell_size * 0.2
        draw_circle(center, radius, OBJECTIVE_COLOR)
        draw_arc(center, radius, 0, TAU, 20, Color(0, 0, 0, 0.5), 1.0)

        var id_text := str(objective_data.get("id", ""))
        if id_text != "":
            var text_pos := center + Vector2(radius + 2, radius + 2)
            draw_string(font, text_pos, id_text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, TEXT_COLOR)

        if _show_objective_radius:
            var owner: String = ""
            var owner_value = objective_data.get("owner")
            if owner_value != null:
                owner = str(owner_value)
            var ring_color := OBJECTIVE_COLOR
            if owner == "player":
                ring_color = PLAYER_COLOR
            elif owner == "model":
                ring_color = MODEL_COLOR
            var ring_radius := CONTROL_RADIUS_CELLS * cell_size
            _draw_dashed_circle(center, ring_radius, ring_color, 1.4)

func _draw_dashed_circle(center: Vector2, radius: float, color: Color, width: float) -> void:
    var segments := 36
    var dash_size := PI * 2 / segments
    for i in range(segments):
        if i % 2 == 0:
            var start_angle := i * dash_size
            var end_angle := (i + 1) * dash_size
            draw_arc(center, radius, start_angle, end_angle, 4, color, width)
