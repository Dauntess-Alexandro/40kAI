#include "play_state.h"

#include <algorithm>
#include <cstdlib>
#include <filesystem>
#include <optional>
#include <string>

namespace {
std::optional<std::filesystem::path> FindRepoRoot() {
  const std::filesystem::path cwd = std::filesystem::current_path();
  std::filesystem::path current = cwd;
  for (int depth = 0; depth < 3; ++depth) {
#if defined(_WIN32)
    if (std::filesystem::exists(current / "scripts" / "viewer.ps1")) {
#else
    if (std::filesystem::exists(current / "scripts" / "viewer.sh")) {
#endif
      return current;
    }
    if (!current.has_parent_path()) {
      break;
    }
    current = current.parent_path();
  }
  return std::nullopt;
}

bool LaunchViewerFromRoot(const std::filesystem::path& root) {
#if defined(_WIN32)
  std::string command = "cd /d \"";
  command += root.string();
  command += "\" && powershell -ExecutionPolicy Bypass -File \"";
  command += (root / "scripts" / "viewer.ps1").string();
  command += "\"";
#else
  std::string command = "cd \"";
  command += root.string();
  command += "\" && scripts/viewer.sh &";
#endif
  return std::system(command.c_str()) == 0;
}
}  // namespace

PlayState::PlayState()
    : model_path_buffer_{},
      response_buffer_{},
      model_path_(""),
      response_input_(""),
      auto_scroll_(true),
      playing_(false),
      status_message_("Выберите модель и нажмите \"Играть\""),
      log_text_("Лог игры появится здесь."),
      board_text_("Поле боя будет отображаться здесь.") {
  model_path_buffer_.front() = '\0';
  response_buffer_.front() = '\0';
}

char* PlayState::model_path_buffer() {
  return model_path_buffer_.data();
}

size_t PlayState::model_path_buffer_size() const {
  return model_path_buffer_.size();
}

const std::string& PlayState::model_path() const {
  return model_path_;
}

void PlayState::UpdateModelPathFromBuffer() {
  model_path_ = model_path_buffer_.data();
}

char* PlayState::response_buffer() {
  return response_buffer_.data();
}

size_t PlayState::response_buffer_size() const {
  return response_buffer_.size();
}

void PlayState::UpdateResponseFromBuffer() {
  response_input_ = response_buffer_.data();
}

void PlayState::StartGame() {
  UpdateModelPathFromBuffer();
  playing_ = true;
  if (model_path_.empty()) {
    status_message_ = "Игра запущена без пути к модели (заглушка).";
  } else {
    status_message_ = "Игра запущена.";
    AppendLogLine("Загружена модель: " + model_path_);
  }
}

void PlayState::StopGame() {
  playing_ = false;
  status_message_ = "Игра остановлена.";
}

bool PlayState::playing() const {
  return playing_;
}

void PlayState::PlayInTerminal() {
  UpdateModelPathFromBuffer();
  status_message_ = "Запуск игры в терминале пока не подключён.";
  if (model_path_.empty()) {
    AppendLogLine("Терминал: модель не указана.");
  } else {
    AppendLogLine("Терминал: выбранная модель: " + model_path_);
  }
}

void PlayState::PlayInGui() {
  UpdateModelPathFromBuffer();
  const auto repo_root = FindRepoRoot();
  if (!repo_root) {
    status_message_ =
        "Не найден scripts/viewer.sh (PlayState::PlayInGui). Запустите GUI из корня репозитория.";
    AppendLogLine("GUI: не найден scripts/viewer.sh. Проверьте текущую папку.");
    return;
  }
  if (!LaunchViewerFromRoot(*repo_root)) {
    status_message_ =
        "Не удалось запустить viewer (PlayState::PlayInGui). Проверьте права и зависимости.";
    AppendLogLine("GUI: запуск viewer завершился с ошибкой.");
    return;
  }
  status_message_ = "Viewer запущен.";
  if (model_path_.empty()) {
    AppendLogLine("GUI: модель не указана.");
  } else {
    AppendLogLine("GUI: выбранная модель: " + model_path_);
  }
}

void PlayState::SendResponse() {
  UpdateResponseFromBuffer();
  if (response_input_.empty()) {
    status_message_ = "Ответ пустой — введите число команды.";
    return;
  }
  AppendLogLine("Ответ игрока: " + response_input_);
  status_message_ = "Ответ отправлен (заглушка).";
  ClearResponseBuffer();
}

void PlayState::ClearLogs() {
  log_text_.clear();
  AppendLogLine("Логи очищены.");
}

void PlayState::set_auto_scroll(bool value) {
  auto_scroll_ = value;
}

bool PlayState::auto_scroll() const {
  return auto_scroll_;
}

void PlayState::SetBoardText(const std::string& text) {
  board_text_ = text;
}

const std::string& PlayState::board_text() const {
  return board_text_;
}

const std::string& PlayState::status_message() const {
  return status_message_;
}

const std::string& PlayState::log_text() const {
  return log_text_;
}

void PlayState::SelectModelStub() {
  status_message_ = "Выбор файла пока не подключён. Введите путь вручную.";
}

void PlayState::AppendLogLine(const std::string& line) {
  if (!log_text_.empty()) {
    log_text_ += '\n';
  }
  log_text_ += line;
}

void PlayState::ClearResponseBuffer() {
  response_buffer_.fill('\0');
  response_input_.clear();
}
