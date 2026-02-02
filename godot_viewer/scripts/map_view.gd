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
const HOVER_COLOR := Color(1.0, 0.95, 0.7, 1)
const SELECT_COLOR := Color(1.0, 0.85, 0.4, 1)
const MOVE_HIGHLIGHT_COLOR := Color(0.35, 0.6, 1.0, 0.25)
const TARGET_HIGHLIGHT_COLOR := Color(1.0, 0.65, 0.35, 1)

var _state: Dictionary = {}
var _show_objective_radius := true
var _unit_draw_data: Array = []
var _unit_centers: Dictionary = {}
var _hovered_unit_key: String = ""
var _selected_unit_key: String = ""
var _active_unit_key: String = ""
var _move_range = null
var _shoot_range = null
var _targets = null
var _phase := ""
var _board_width := 0
var _board_height := 0
var _layout_origin := Vector2.ZERO
var _layout_cell_size := 0.0

signal unit_selected(side: String, unit_id: int)

func set_state(state: Dictionary) -> void:
    _state = state if state != null else {}
    queue_redraw()

func set_show_objective_radius(visible: bool) -> void:
    _show_objective_radius = visible
    queue_redraw()

func set_active_context(
    active_unit_id = null,
    active_unit_side = null,
    phase = null,
    move_range = null,
    shoot_range = null,
    targets = null
) -> void:
    if active_unit_side != null and active_unit_id != null:
        _active_unit_key = _make_key(str(active_unit_side), int(active_unit_id))
    else:
        _active_unit_key = ""
    _phase = str(phase if phase != null else "")
    _move_range = move_range
    _shoot_range = shoot_range
    _targets = targets
    queue_redraw()

func _notification(what: int) -> void:
    if what == NOTIFICATION_RESIZED:
        queue_redraw()

func _gui_input(event: InputEvent) -> void:
    if event is InputEventMouseMotion:
        _update_hover(event.position)
    elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
        var unit_data := _pick_unit(event.position)
        if unit_data:
            _selected_unit_key = str(unit_data.get("key", ""))
            var unit := unit_data.get("unit")
            if unit is Dictionary:
                var side = str(unit.get("side", ""))
                var unit_id = int(unit.get("id", -1))
                if side != "" and unit_id >= 0:
                    unit_selected.emit(side, unit_id)
        else:
            _selected_unit_key = ""
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
    _layout_origin = origin
    _layout_cell_size = cell_size
    _board_width = width
    _board_height = height

    _draw_grid(origin, width, height, cell_size)
    _draw_movement_overlay(origin, cell_size)
    _draw_objectives(origin, cell_size)
    _draw_units(origin, cell_size)
    _draw_target_overlay(cell_size)

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
    _unit_draw_data.clear()
    _unit_centers.clear()
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
        var key := _make_key(str(side_value), int(unit_data.get("id", -1)))
        _unit_centers[key] = center
        _unit_draw_data.append({
            "key": key,
            "unit": unit_data,
            "center": center,
            "radius": radius
        })

        if _selected_unit_key != "" and _selected_unit_key == key:
            draw_arc(center, radius + 2.0, 0, TAU, 32, SELECT_COLOR, 2.0)
        elif _hovered_unit_key != "" and _hovered_unit_key == key:
            draw_arc(center, radius + 2.0, 0, TAU, 32, HOVER_COLOR, 2.0)

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

func _update_hover(position: Vector2) -> void:
    var unit_data := _pick_unit(position)
    if unit_data:
        var key = unit_data.get("key")
        if _hovered_unit_key != str(key):
            _hovered_unit_key = str(key)
            _set_tooltip_for_unit(unit_data.get("unit"))
            queue_redraw()
    else:
        if _hovered_unit_key != "":
            _hovered_unit_key = ""
            tooltip_text = ""
            queue_redraw()

func _pick_unit(position: Vector2):
    for item in _unit_draw_data:
        var center: Vector2 = item.get("center", Vector2.ZERO)
        var radius: float = float(item.get("radius", 0))
        if position.distance_to(center) <= radius + 4.0:
            return item
    return null

func _set_tooltip_for_unit(unit_data) -> void:
    if not unit_data is Dictionary:
        tooltip_text = ""
        return
    var name_text := str(unit_data.get("name", "—"))
    var id_text := str(unit_data.get("id", "—"))
    var hp_text := str(unit_data.get("hp", "—"))
    var models_text := str(unit_data.get("models", "—"))
    var x_text := str(unit_data.get("x", "—"))
    var y_text := str(unit_data.get("y", "—"))
    tooltip_text = "ID: %s\n%s\nHP: %s\nМодели: %s\nКоорд: (%s, %s)" % [
        id_text,
        name_text,
        hp_text,
        models_text,
        x_text,
        y_text,
    ]

func _draw_movement_overlay(origin: Vector2, cell_size: float) -> void:
    if not _should_show_movement():
        return
    var unit := _state_unit(_active_unit_key)
    if unit == null:
        return
    var move_range = _move_range
    if move_range == null:
        return
    var x_value = unit.get("x")
    var y_value = unit.get("y")
    if x_value == null or y_value == null:
        return
    var x: int = int(x_value)
    var y: int = int(y_value)
    for dx in range(-move_range, move_range + 1):
        for dy in range(-move_range, move_range + 1):
            if abs(dx) + abs(dy) > move_range:
                continue
            var cell_x := x + dx
            var cell_y := y + dy
            if cell_x < 0 or cell_y < 0 or cell_x >= _board_width or cell_y >= _board_height:
                continue
            var rect := Rect2(
                origin + Vector2(cell_x * cell_size, cell_y * cell_size),
                Vector2(cell_size, cell_size)
            )
            draw_rect(rect, MOVE_HIGHLIGHT_COLOR, true)

func _draw_target_overlay(cell_size: float) -> void:
    if not _should_show_shooting():
        return
    var unit := _state_unit(_active_unit_key)
    if unit == null:
        return
    var shoot_range = _shoot_range
    if shoot_range == null:
        return
    var targets = _resolve_targets(unit, shoot_range)
    for key in targets:
        if not _unit_centers.has(key):
            continue
        var center: Vector2 = _unit_centers[key]
        var radius := cell_size * 0.45
        draw_arc(center, radius, 0, TAU, 32, TARGET_HIGHLIGHT_COLOR, 2.0)

func _should_show_movement() -> bool:
    var phase_text := _phase.to_lower()
    return "move" in phase_text or "движ" in phase_text or "movement" in phase_text or _move_range != null

func _should_show_shooting() -> bool:
    var phase_text := _phase.to_lower()
    return "shoot" in phase_text or "стрел" in phase_text or "shooting" in phase_text

func _state_unit(unit_key: String):
    if unit_key == "":
        return null
    var units: Array = _state.get("units", []) or []
    for unit in units:
        if not unit is Dictionary:
            continue
        var unit_data: Dictionary = unit
        if unit_key == _make_key(str(unit_data.get("side", "")), int(unit_data.get("id", -1))):
            return unit_data
    return null

func _resolve_targets(unit: Dictionary, shoot_range: int) -> Array:
    var targets := {}
    if _targets is Array:
        for entry in _targets:
            if entry is Dictionary:
                var side = entry.get("side")
                var target_id = entry.get("id")
                if side != null and target_id != null:
                    targets[_make_key(str(side), int(target_id))] = true
            elif entry is Array and entry.size() >= 2:
                targets[_make_key(str(entry[0]), int(entry[1]))] = true
            elif entry is int:
                for candidate in _state.get("units", []) or []:
                    if candidate.get("id") == entry:
                        targets[_make_key(str(candidate.get("side", "")), int(candidate.get("id", -1)))] = true
    if targets.size() > 0:
        return targets.keys()
    var source_x = unit.get("x")
    var source_y = unit.get("y")
    if source_x == null or source_y == null:
        return []
    for target in _state.get("units", []) or []:
        if not target is Dictionary:
            continue
        if target.get("side") == unit.get("side"):
            continue
        var target_x = target.get("x")
        var target_y = target.get("y")
        if target_x == null or target_y == null:
            continue
        var distance := abs(int(target_x) - int(source_x)) + abs(int(target_y) - int(source_y))
        if distance <= shoot_range:
            targets[_make_key(str(target.get("side", "")), int(target.get("id", -1)))] = true
    return targets.keys()

func _make_key(side: String, unit_id: int) -> String:
    return "%s:%s" % [side, str(unit_id)]
