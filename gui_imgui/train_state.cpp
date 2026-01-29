#include "train_state.h"

#include <algorithm>
#include <sstream>

namespace {
int ClampNonNegative(int value) {
  return std::max(0, value);
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
  training_ = true;
  progress_current_ = 0;
  progress_total_ = games_count_;
  switch (mode) {
    case TrainMode::Standard:
      status_message_ = "Обучение...";
      break;
    case TrainMode::EightX:
      status_message_ = "Обучение 8x...";
      break;
    case TrainMode::SelfPlay:
      status_message_ = "Самообучение: обучение...";
      break;
    default:
      status_message_ = "Обучение...";
      break;
  }
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
