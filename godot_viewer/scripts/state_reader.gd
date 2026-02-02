extends Node
class_name StateReader

signal state_changed(state: Dictionary)

@export var state_path := "res://state.json"
@export var poll_interval_sec := 0.5

var _last_mtime := 0
var _timer: Timer

func _ready() -> void:
    _timer = Timer.new()
    _timer.wait_time = poll_interval_sec
    _timer.autostart = true
    _timer.one_shot = false
    _timer.timeout.connect(_poll_state)
    add_child(_timer)
    _poll_state()

func _poll_state() -> void:
    if not FileAccess.file_exists(state_path):
        return
    var mtime := FileAccess.get_modified_time(state_path)
    if mtime <= _last_mtime:
        return
    _last_mtime = mtime
    var state := _load_state()
    emit_signal("state_changed", state)

func _load_state() -> Dictionary:
    var file := FileAccess.open(state_path, FileAccess.READ)
    if file == null:
        return _default_state()
    var content := file.get_as_text()
    file.close()
    var json := JSON.new()
    var result := json.parse(content)
    if result != OK:
        return _default_state()
    var data: Dictionary = {}
    if json.data is Dictionary:
        data = json.data
        var state := _default_state()
        for key in data.keys():
            state[key] = data[key]
        return state
    return _default_state()

func _default_state() -> Dictionary:
    return {
        "board": {"width": 60, "height": 40},
        "turn": null,
        "round": null,
        "phase": null,
        "active": null,
        "vp": {"player": null, "model": null},
        "cp": {"player": null, "model": null},
        "units": [],
        "objectives": [],
        "log_tail": [],
    }
