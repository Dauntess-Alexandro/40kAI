#pragma once

#include <string>
#include <vector>

enum class Faction {
  SpaceMarine,
  Orks,
  SistersOfBattle,
  AdeptusCustodes,
  Tyranids,
  AstraMilitarum,
  Tau,
  Necrons
};

enum class TrainMode {
  Standard,
  EightX,
  SelfPlay
};

class TrainState {
 public:
  TrainState();

  void StartTraining(TrainMode mode);
  void StopTraining();
  void ClearModelCache();

  void set_games_count(int value);
  int games_count() const;

  void set_dimensions(int x, int y);
  int dim_x() const;
  int dim_y() const;

  void set_model_faction(Faction faction);
  void set_enemy_faction(Faction faction);
  Faction model_faction() const;
  Faction enemy_faction() const;

  const char* FactionLabel(Faction faction) const;

  bool training() const;
  const std::string& status_message() const;

  void set_progress(int current, int total);
  int progress_current() const;
  int progress_total() const;
  float progress_ratio() const;
  std::string progress_label() const;
  std::string progress_stats() const;

 private:
  int games_count_;
  int dim_x_;
  int dim_y_;
  Faction model_faction_;
  Faction enemy_faction_;
  bool training_;
  std::string status_message_;
  int progress_current_;
  int progress_total_;
};
