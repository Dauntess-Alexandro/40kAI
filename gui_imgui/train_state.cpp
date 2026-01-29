#include "train_state.h"

#include <algorithm>
#include <cstdlib>
#include <filesystem>
#include <optional>
#include <sstream>
#include <string>
#include <thread>

namespace {
int ClampNonNegative(int value) {
  return std::max(0, value);
}

std::optional<std::filesystem::path> FindRepoRoot() {
  const std::filesystem::path cwd = std::filesystem::current_path();
  std::filesystem::path current = cwd;
  for (int depth = 0; depth < 4; ++depth) {
#if defined(_WIN32)
    if (std::filesystem::exists(current / "train.ps1")) {
#else
    if (std::filesystem::exists(current / "train.sh")) {
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

std::string BuildEnvPrefix(const std::string& envs) {
#if defined(_WIN32)
  std::istringstream iss(envs);
  std::string token;
  std::string result;
  while (iss >> token) {
    if (token.find('=') == std::string::npos) {
      continue;
    }
    result += "set " + token + " && ";
  }
  return result;
#else
  return envs;
#endif
}

std::string BuildScriptCommand(const std::filesystem::path& root,
                               const std::string& base,
                               const std::string& args = "") {
#if defined(_WIN32)
  std::string command = "powershell -ExecutionPolicy Bypass -File \"";
  command += (root / (base + ".ps1")).string();
  command += "\"";
#else
  std::string command = "./" + base + ".sh";
#endif
  if (!args.empty()) {
    command += " ";
    command += args;
  }
  return command;
}

std::string FactionDataId(Faction faction) {
  switch (faction) {
    case Faction::SpaceMarine:
      return "Space_Marine";
    case Faction::Orks:
      return "Orks";
    case Faction::SistersOfBattle:
      return "Sisters_of_Battle";
    case Faction::AdeptusCustodes:
      return "Custodes";
    case Faction::Tyranids:
      return "Tyrannids";
    case Faction::AstraMilitarum:
      return "Militarum";
    case Faction::Tau:
      return "Tau";
    case Faction::Necrons:
      return "Necrons";
    default:
      return "Necrons";
  }
}

std::string BuildChainToken() {
#if defined(_WIN32)
  return " && ";
#else
  return " ; ";
#endif
}
}

TrainState::TrainState()
    : games_count_(100),
      dim_x_(60),
      dim_y_(40),
      model_faction_(Faction::Necrons),
      enemy_faction_(Faction::Necrons),
      training_(false),
      status_message_("Нажмите \"Train\", чтобы начать обучение"),
      progress_current_(0),
      progress_total_(0) {}

void TrainState::StartTraining(TrainMode mode) {
  const auto repo_root = FindRepoRoot();
  if (!repo_root) {
    status_message_ =
        "Не найден train.ps1/train.sh (TrainState::StartTraining). Запустите GUI из корня репозитория.";
    training_ = false;
    return;
  }

  training_ = true;
  progress_current_ = 0;
  progress_total_ = games_count_;

  std::string env_prefix;
  switch (mode) {
    case TrainMode::Standard:
      status_message_ = "Обучение...";
      break;
    case TrainMode::EightX:
      status_message_ = "Обучение 8x...";
      env_prefix = "VEC_ENV_COUNT=8 ";
      break;
    case TrainMode::SelfPlay:
      status_message_ = "Самообучение: обучение...";
      env_prefix = "SELF_PLAY_ENABLED=1 ";
      break;
    default:
      status_message_ = "Обучение...";
      break;
  }

  std::ostringstream data_args;
  data_args << games_count_ << " " << FactionDataId(model_faction_) << " "
            << FactionDataId(enemy_faction_) << " " << dim_x_ << " " << dim_y_;

  const std::string chain = BuildChainToken();
  std::string command;
#if defined(_WIN32)
  command = "cd /d \"";
  command += repo_root->string();
  command += "\"";
#else
  command = "cd \"";
  command += repo_root->string();
  command += "\"";
#endif
  command += chain;
  command += BuildScriptCommand(*repo_root, "data", data_args.str());
  command += chain;
  command += BuildEnvPrefix(env_prefix);
  command += BuildScriptCommand(*repo_root, "train");

  std::thread([this, command]() {
    const int exit_code = std::system(command.c_str());
    training_ = false;
    if (exit_code == 0) {
      status_message_ = "Обучение завершено.";
    } else {
      status_message_ = "Обучение завершено с ошибкой. Код выхода: " + std::to_string(exit_code);
    }
  }).detach();
}

void TrainState::StopTraining() {
  training_ = false;
}

void TrainState::ClearModelCache() {
  status_message_ = "Кэш моделей очищен (заглушка).";
}

void TrainState::set_games_count(int value) {
  games_count_ = std::max(1, value);
}

int TrainState::games_count() const {
  return games_count_;
}

void TrainState::set_dimensions(int x, int y) {
  dim_x_ = ClampNonNegative(x);
  dim_y_ = ClampNonNegative(y);
}

int TrainState::dim_x() const {
  return dim_x_;
}

int TrainState::dim_y() const {
  return dim_y_;
}

void TrainState::set_model_faction(Faction faction) {
  model_faction_ = faction;
}

void TrainState::set_enemy_faction(Faction faction) {
  enemy_faction_ = faction;
}

Faction TrainState::model_faction() const {
  return model_faction_;
}

Faction TrainState::enemy_faction() const {
  return enemy_faction_;
}

const char* TrainState::FactionLabel(Faction faction) const {
  switch (faction) {
    case Faction::SpaceMarine:
      return "Space Marine";
    case Faction::Orks:
      return "Orks";
    case Faction::SistersOfBattle:
      return "Sisters of Battle";
    case Faction::AdeptusCustodes:
      return "Adeptus Custodes";
    case Faction::Tyranids:
      return "Tyranids";
    case Faction::AstraMilitarum:
      return "Astra Militarum";
    case Faction::Tau:
      return "Tau";
    case Faction::Necrons:
      return "Necrons";
    default:
      return "Неизвестно";
  }
}

bool TrainState::training() const {
  return training_;
}

const std::string& TrainState::status_message() const {
  return status_message_;
}

void TrainState::set_progress(int current, int total) {
  progress_current_ = ClampNonNegative(current);
  progress_total_ = std::max(0, total);
}

int TrainState::progress_current() const {
  return progress_current_;
}

int TrainState::progress_total() const {
  return progress_total_;
}

float TrainState::progress_ratio() const {
  if (progress_total_ <= 0) {
    return 0.0f;
  }
  return static_cast<float>(progress_current_) / static_cast<float>(progress_total_);
}

std::string TrainState::progress_label() const {
  std::ostringstream oss;
  if (progress_total_ <= 0) {
    return "ep=0/0 (0%)";
  }
  const int percent = static_cast<int>(progress_ratio() * 100.0f);
  oss << "ep=" << progress_current_ << "/" << progress_total_ << " (" << percent << "%)";
  return oss.str();
}

std::string TrainState::progress_stats() const {
  return "— it/s • elapsed 00:00";
}
