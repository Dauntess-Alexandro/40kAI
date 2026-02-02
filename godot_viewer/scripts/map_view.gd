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

    var board: Dictionary = _state.get("board", {})
    var width := int(board.get("width", DEFAULT_BOARD.width))
    var height := int(board.get("height", DEFAULT_BOARD.height))
    if width <= 0 or height <= 0:
        return

    var cell_size := min(size.x / width, size.y / height)
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
    var units: Array = _state.get("units", []) or []
    var occupied := {}
    for unit in units:
        var key := Vector2i(int(unit.get("x", -1)), int(unit.get("y", -1)))
        if not occupied.has(key):
            occupied[key] = []
        occupied[key].append(unit)

    var font := get_theme_default_font()
    var font_size := get_theme_default_font_size()

    for unit in units:
        var x := unit.get("x")
        var y := unit.get("y")
        if x == null or y == null:
            continue

        var key := Vector2i(int(x), int(y))
        var stack: Array = occupied.get(key, [])
        var offset := 0.0
        if stack.size() > 1:
            offset = (stack.find(unit) - (stack.size() - 1) * 0.5) * (cell_size * 0.15)
        var center := origin + Vector2((x + 0.5) * cell_size + offset, (y + 0.5) * cell_size - offset)

        var color := PLAYER_COLOR if unit.get("side") == "player" else MODEL_COLOR
        var radius := cell_size * 0.35
        draw_circle(center, radius, color)
        draw_arc(center, radius, 0, TAU, 32, Color(0, 0, 0, 0.4), 1.0)

        var id_text := str(unit.get("id", ""))
        if id_text != "":
            var text_pos := center + Vector2(-radius, -radius - 4)
            draw_string(font, text_pos, id_text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, TEXT_COLOR)

func _draw_objectives(origin: Vector2, cell_size: float) -> void:
    var objectives: Array = _state.get("objectives", []) or []
    var font := get_theme_default_font()
    var font_size := get_theme_default_font_size()

    for objective in objectives:
        var x := objective.get("x")
        var y := objective.get("y")
        if x == null or y == null:
            continue
        var center := origin + Vector2((x + 0.5) * cell_size, (y + 0.5) * cell_size)
        var radius := cell_size * 0.2
        draw_circle(center, radius, OBJECTIVE_COLOR)
        draw_arc(center, radius, 0, TAU, 20, Color(0, 0, 0, 0.5), 1.0)

        var id_text := str(objective.get("id", ""))
        if id_text != "":
            var text_pos := center + Vector2(radius + 2, radius + 2)
            draw_string(font, text_pos, id_text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, TEXT_COLOR)

        if _show_objective_radius:
            var owner := objective.get("owner")
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
