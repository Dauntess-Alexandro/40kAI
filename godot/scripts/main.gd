extends Control

@export var poll_interval_sec := 0.3
@export var state_path_override := ""

@onready var board_view: Control = $HBoxContainer/BoardPanel/BoardView
@onready var status_label: Label = $HBoxContainer/SidePanel/StatusLabel
@onready var model_path_line_edit: LineEdit = $HBoxContainer/SidePanel/ModelPathLineEdit
@onready var gui_check: CheckButton = $HBoxContainer/SidePanel/GuiCheck
@onready var start_button: Button = $HBoxContainer/SidePanel/ButtonsRow/StartButton
@onready var stop_button: Button = $HBoxContainer/SidePanel/ButtonsRow/StopButton
@onready var process_label: Label = $HBoxContainer/SidePanel/ProcessLabel
@onready var units_label: RichTextLabel = $HBoxContainer/SidePanel/UnitsLabel
@onready var log_label: RichTextLabel = $HBoxContainer/SidePanel/LogLabel

var _timer: Timer
var _last_generated_at := ""
var _last_error := ""
var _process_id := -1

func _ready() -> void:
    _timer = Timer.new()
    _timer.wait_time = poll_interval_sec
    _timer.autostart = true
    _timer.timeout.connect(_reload_state)
    add_child(_timer)
    start_button.pressed.connect(_start_game)
    stop_button.pressed.connect(_stop_game)
    _update_process_status()
    _reload_state()


func _reload_state() -> void:
    _update_process_status()
    var state_path = _resolve_state_path()
    var payload = _load_json(state_path)
    if payload.is_empty():
        if _last_error.is_empty():
            _last_error = "Не удалось прочитать состояние: %s" % state_path
        status_label.text = _last_error
        return

    var generated_at = str(payload.get("generated_at", ""))
    if generated_at == _last_generated_at:
        return

    _last_generated_at = generated_at
    _last_error = ""

    _update_status(payload)
    _update_units(payload)
    _update_logs(payload)

    if board_view.has_method("apply_state"):
        board_view.call("apply_state", payload)

func _start_game() -> void:
    if _is_process_running():
        process_label.text = "Процесс уже запущен."
        return

    var repo_root = _resolve_repo_root()
    var python_bin = _resolve_python_bin()
    var model_path = model_path_line_edit.text.strip_edges()
    if model_path.is_empty():
        model_path = "None"
        model_path_line_edit.text = model_path

    var play_gui = "True" if gui_check.button_pressed else "False"
    var play_script = repo_root.path_join("play.py")

    var safe_repo_root = _py_escape(repo_root)
    var safe_model_path = _py_escape(model_path)
    var safe_play_script = _py_escape(play_script)

    var args = PackedStringArray([
        "-c",
        "import os,runpy,sys; os.chdir(r'%s'); sys.argv=['play.py','%s','%s']; runpy.run_path(r'%s', run_name='__main__')"
            % [safe_repo_root, safe_model_path, play_gui, safe_play_script],
    ])

    _process_id = OS.create_process(python_bin, args, true)
    if _process_id <= 0:
        process_label.text = "Ошибка запуска: проверьте путь к Python и проекту."
        _process_id = -1
        return

    process_label.text = "Процесс запущен (pid: %s)." % str(_process_id)


func _stop_game() -> void:
    if not _is_process_running():
        process_label.text = "Процесс уже остановлен."
        _process_id = -1
        return

    OS.kill(_process_id)
    process_label.text = "Процесс остановлен."
    _process_id = -1


func _update_process_status() -> void:
    if _is_process_running():
        process_label.text = "Процесс запущен (pid: %s)." % str(_process_id)
    else:
        if _process_id != -1:
            _process_id = -1
        if process_label.text.is_empty():
            process_label.text = "Процесс: не запущен"


func _is_process_running() -> bool:
    return _process_id > 0 and OS.is_process_running(_process_id)

func _resolve_repo_root() -> String:
    var project_root = ProjectSettings.globalize_path("res://")
    return project_root.path_join("..").simplify_path()

func _resolve_python_bin() -> String:
    var env_python = OS.get_environment("PYTHON")
    if not env_python.is_empty():
        return env_python
    return "python"

func _py_escape(value: String) -> String:
    return value.replace("'", "\\'")

func _resolve_state_path() -> String:
    if not state_path_override.is_empty():
        return state_path_override

    var env_path = OS.get_environment("STATE_JSON_PATH")
    if not env_path.is_empty():
        return env_path

    var repo_root = _resolve_repo_root()
    return repo_root.path_join("gui").path_join("state.json")


func _load_json(path: String) -> Dictionary:
    if not FileAccess.file_exists(path):
        _last_error = "Файл состояния не найден: %s" % path
        return {}

    var file = FileAccess.open(path, FileAccess.READ)
    if file == null:
        _last_error = "Не удалось открыть файл состояния: %s" % path
        return {}

    var content = file.get_as_text()
    var json = JSON.new()
    var parse_result = json.parse(content)
    if parse_result != OK:
        _last_error = "Ошибка JSON в состоянии: %s" % json.get_error_message()
        return {}

    if typeof(json.data) != TYPE_DICTIONARY:
        _last_error = "Некорректный формат состояния: ожидается объект JSON"
        return {}

    return json.data


func _update_status(payload: Dictionary) -> void:
    var board = payload.get("board", {})
    var width = board.get("width", "?")
    var height = board.get("height", "?")
    var turn = payload.get("turn", "?")
    var round = payload.get("round", "?")
    var phase = payload.get("phase", "?")
    var active = payload.get("active", "—")
    var vp = payload.get("vp", {})
    var cp = payload.get("cp", {})

    status_label.text = "Ход: %s | Раунд: %s\nФаза: %s | Активен: %s\nПоле: %sx%s\nVP: Игрок %s / Модель %s\nCP: Игрок %s / Модель %s" % [
        str(turn),
        str(round),
        str(phase),
        str(active),
        str(width),
        str(height),
        str(vp.get("player", "?")),
        str(vp.get("model", "?")),
        str(cp.get("player", "?")),
        str(cp.get("model", "?")),
    ]


func _update_units(payload: Dictionary) -> void:
    var units = payload.get("units", [])
    var lines: Array[String] = []

    for unit in units:
        if typeof(unit) != TYPE_DICTIONARY:
            continue
        var side = str(unit.get("side", "?"))
        var name = str(unit.get("name", "?"))
        var hp = unit.get("hp", null)
        var models = unit.get("models", null)
        var pos = "(%s, %s)" % [str(unit.get("x", "?")), str(unit.get("y", "?"))]
        var hp_text = hp if hp != null else "—"
        var models_text = models if models != null else "—"
        lines.append("• [%s] %s | HP: %s | Модели: %s | %s" % [side, name, str(hp_text), str(models_text), pos])

    units_label.text = "\n".join(lines) if not lines.is_empty() else "—"


func _update_logs(payload: Dictionary) -> void:
    var log_tail = payload.get("log_tail", [])
    if typeof(log_tail) != TYPE_ARRAY or log_tail.is_empty():
        log_label.text = "—"
        return

    var lines: Array[String] = []
    for entry in log_tail:
        lines.append(str(entry))
    log_label.text = "\n".join(lines)
