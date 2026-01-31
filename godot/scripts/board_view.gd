extends Control

var _board_size := Vector2i(60, 40)
var _units: Array = []
var _objectives: Array = []
var _active_side := ""

const COLOR_GRID := Color(0.23, 0.23, 0.28)
const COLOR_BG := Color(0.12, 0.12, 0.15)
const COLOR_MODEL := Color(0.33, 0.76, 0.35)
const COLOR_PLAYER := Color(0.8, 0.25, 0.25)
const COLOR_OBJECTIVE := Color(0.95, 0.85, 0.2)
const COLOR_ACTIVE := Color(0.4, 0.6, 1.0)


func apply_state(payload: Dictionary) -> void:
    var board = payload.get("board", {})
    _board_size.x = int(board.get("width", _board_size.x))
    _board_size.y = int(board.get("height", _board_size.y))
    _units = payload.get("units", [])
    _objectives = payload.get("objectives", [])
    _active_side = str(payload.get("active", ""))
    queue_redraw()


func _draw() -> void:
    draw_rect(Rect2(Vector2.ZERO, size), COLOR_BG, true)

    if _board_size.x <= 0 or _board_size.y <= 0:
        return

    var cell_size = min(size.x / float(_board_size.x), size.y / float(_board_size.y))
    var grid_size = Vector2(_board_size.x * cell_size, _board_size.y * cell_size)
    var origin = (size - grid_size) * 0.5

    _draw_grid(origin, grid_size, cell_size)
    _draw_objectives(origin, cell_size)
    _draw_units(origin, cell_size)


func _draw_grid(origin: Vector2, grid_size: Vector2, cell_size: float) -> void:
    for x in range(_board_size.x + 1):
        var from = origin + Vector2(x * cell_size, 0)
        var to = origin + Vector2(x * cell_size, grid_size.y)
        draw_line(from, to, COLOR_GRID, 1.0)

    for y in range(_board_size.y + 1):
        var from = origin + Vector2(0, y * cell_size)
        var to = origin + Vector2(grid_size.x, y * cell_size)
        draw_line(from, to, COLOR_GRID, 1.0)


func _draw_objectives(origin: Vector2, cell_size: float) -> void:
    for objective in _objectives:
        if typeof(objective) != TYPE_DICTIONARY:
            continue
        var x = objective.get("x", null)
        var y = objective.get("y", null)
        if x == null or y == null:
            continue
        var pos = origin + Vector2((float(x) + 0.5) * cell_size, (float(y) + 0.5) * cell_size)
        draw_circle(pos, cell_size * 0.35, COLOR_OBJECTIVE)


func _draw_units(origin: Vector2, cell_size: float) -> void:
    var font = get_theme_default_font()
    for unit in _units:
        if typeof(unit) != TYPE_DICTIONARY:
            continue
        var x = unit.get("x", null)
        var y = unit.get("y", null)
        if x == null or y == null:
            continue

        var side = str(unit.get("side", ""))
        var color = COLOR_MODEL if side == "model" else COLOR_PLAYER
        if side == _active_side:
            color = color.lerp(COLOR_ACTIVE, 0.35)

        var pos = origin + Vector2((float(x) + 0.5) * cell_size, (float(y) + 0.5) * cell_size)
        draw_circle(pos, cell_size * 0.32, color)

        var name = str(unit.get("name", ""))
        if not name.is_empty() and font != null:
            var text_pos = pos + Vector2(cell_size * 0.4, -cell_size * 0.2)
            draw_string(font, text_pos, name, HORIZONTAL_ALIGNMENT_LEFT, cell_size * 3.0, Color.WHITE)
