extends Node
class_name StateLoader

# Загружает состояние из JSON файла. Возвращает словарь или пустой, если ошибка.
func load_state(path: String) -> Dictionary:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		printerr("[StateLoader] Не удалось открыть файл: ", path, ". Проверьте путь и права доступа.")
		return {}

	var text := file.get_as_text()
	var json := JSON.new()
	var error_code := json.parse(text)
	if error_code != OK:
		printerr("[StateLoader] Ошибка JSON в файле ", path, ": ", json.get_error_message())
		return {}

	var data := json.get_data()
	if typeof(data) != TYPE_DICTIONARY:
		printerr("[StateLoader] Некорректный формат JSON в файле ", path, ": ожидается объект.")
		return {}

	return data
