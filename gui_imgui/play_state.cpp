#include "play_state.h"

#include <algorithm>

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
