#pragma once

#include <array>
#include <cstddef>
#include <string>

class PlayState {
 public:
  PlayState();

  char* model_path_buffer();
  size_t model_path_buffer_size() const;
  const std::string& model_path() const;
  void UpdateModelPathFromBuffer();

  char* response_buffer();
  size_t response_buffer_size() const;
  void UpdateResponseFromBuffer();

  void StartGame();
  void StopGame();
  bool playing() const;
  void PlayInTerminal();
  void PlayInGui();

  void SendResponse();
  void ClearLogs();

  void set_auto_scroll(bool value);
  bool auto_scroll() const;

  void SetBoardText(const std::string& text);
  const std::string& board_text() const;

  const std::string& status_message() const;
  const std::string& log_text() const;

  void SelectModelStub();

 private:
  void AppendLogLine(const std::string& line);
  void ClearResponseBuffer();

  std::array<char, 256> model_path_buffer_;
  std::array<char, 128> response_buffer_;
  std::string model_path_;
  std::string response_input_;
  bool auto_scroll_;
  bool playing_;
  std::string status_message_;
  std::string log_text_;
  std::string board_text_;
};
