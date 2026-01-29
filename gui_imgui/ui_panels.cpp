#include "ui_panels.h"

#include <imgui.h>

namespace {
bool SelectTabPosition(const char* label, TabPosition position, AppState& state) {
  const bool selected = state.tab_position() == position;
  if (ImGui::RadioButton(label, selected)) {
    state.set_tab_position(position);
    return true;
  }
  return false;
}

bool SelectFaction(const char* label, Faction faction, Faction current, TrainState& state, bool is_model) {
  const bool selected = current == faction;
  if (ImGui::RadioButton(label, selected)) {
    if (is_model) {
      state.set_model_faction(faction);
    } else {
      state.set_enemy_faction(faction);
    }
    return true;
  }
  return false;
}
}  // namespace

void RenderCommandPanel(AppState& state) {
  ImGui::Begin("Командный пункт");
  ImGui::Text("Минимальный ImGui GUI. Дальше переносим панели из GTKmm.");
  if (ImGui::Button("Боевой клич")) {
    state.IncrementClicks();
  }
  ImGui::SameLine();
  ImGui::Text("Нажатий: %d", state.clicks());

  bool show_demo = state.show_demo();
  if (ImGui::Checkbox("Показать демо-окно", &show_demo)) {
    state.set_show_demo(show_demo);
  }
  ImGui::End();
}

void RenderSettingsPanel(AppState& state) {
  ImGui::Begin("Настройки");
  ImGui::Text("Позиция вкладок (как в старом GTKmm GUI):");
  SelectTabPosition("Сверху", TabPosition::Top, state);
  SelectTabPosition("Слева", TabPosition::Left, state);
  SelectTabPosition("Справа", TabPosition::Right, state);
  SelectTabPosition("Снизу", TabPosition::Bottom, state);

  ImGui::Separator();
  ImGui::Text("Текущая позиция: %s", state.TabPositionLabel(state.tab_position()));
  ImGui::End();
}

void RenderPlayPanel(PlayState& state) {
  ImGui::Begin("Игра");

  ImGui::Text("Путь к модели:");
  if (ImGui::InputText("##play_model_path", state.model_path_buffer(),
                       static_cast<int>(state.model_path_buffer_size()))) {
    state.UpdateModelPathFromBuffer();
  }
  if (ImGui::Button("Choose")) {
    state.SelectModelStub();
  }

  if (ImGui::Button("Play in Terminal")) {
    state.PlayInTerminal();
  }
  ImGui::SameLine();
  if (ImGui::Button("Играть в GUI")) {
    state.PlayInGui();
  }

  ImGui::Separator();
  ImGui::Text("Ответ игрока:");
  if (ImGui::InputText("##play_response", state.response_buffer(),
                       static_cast<int>(state.response_buffer_size()))) {
    state.UpdateResponseFromBuffer();
  }
  if (ImGui::Button("Отправить")) {
    state.SendResponse();
  }
  ImGui::SameLine();
  if (ImGui::Button("Очистить лог")) {
    state.ClearLogs();
  }
  ImGui::SameLine();
  if (ImGui::Button("Остановить")) {
    state.StopGame();
  }

  bool auto_scroll = state.auto_scroll();
  if (ImGui::Checkbox("Автопрокрутка логов", &auto_scroll)) {
    state.set_auto_scroll(auto_scroll);
  }

  ImGui::Separator();
  ImGui::Text("Статус: %s", state.status_message().c_str());

  ImGui::Separator();
  ImGui::Text("Лог:");
  ImGui::BeginChild("play_log", ImVec2(0.0f, 160.0f), true);
  ImGui::TextUnformatted(state.log_text().c_str());
  if (state.auto_scroll()) {
    ImGui::SetScrollHereY(1.0f);
  }
  ImGui::EndChild();

  ImGui::Separator();
  ImGui::Text("Поле боя:");
  ImGui::BeginChild("play_board", ImVec2(0.0f, 160.0f), true);
  ImGui::TextUnformatted(state.board_text().c_str());
  ImGui::EndChild();

  ImGui::End();
}

void RenderTrainPanel(TrainState& state) {
  ImGui::Begin("Train");

  ImGui::Text("Train Model:");
  if (ImGui::Button("Train")) {
    state.StartTraining(TrainMode::Standard);
  }
  ImGui::SameLine();
  if (ImGui::Button("Тренировать 8x")) {
    state.StartTraining(TrainMode::EightX);
  }
  ImGui::SameLine();
  if (ImGui::Button("Самообучение")) {
    state.StartTraining(TrainMode::SelfPlay);
  }

  if (ImGui::Button("Clear Model Cache")) {
    state.ClearModelCache();
  }

  ImGui::Separator();
  ImGui::Text("# of Games in Training:");
  int games = state.games_count();
  if (ImGui::InputInt("##games_count", &games)) {
    state.set_games_count(games);
  }

  ImGui::Text("Dimensions of Board:");
  int dim_x = state.dim_x();
  int dim_y = state.dim_y();
  if (ImGui::InputInt("X", &dim_x)) {
    state.set_dimensions(dim_x, state.dim_y());
  }
  ImGui::SameLine();
  if (ImGui::InputInt("Y", &dim_y)) {
    state.set_dimensions(state.dim_x(), dim_y);
  }

  ImGui::Separator();
  ImGui::Text("Model Faction:");
  SelectFaction("Space Marine", Faction::SpaceMarine, state.model_faction(), state, true);
  SelectFaction("Orks", Faction::Orks, state.model_faction(), state, true);
  SelectFaction("Sisters of Battle", Faction::SistersOfBattle, state.model_faction(), state, true);
  SelectFaction("Adeptus Custodes", Faction::AdeptusCustodes, state.model_faction(), state, true);
  SelectFaction("Tyranids", Faction::Tyranids, state.model_faction(), state, true);
  SelectFaction("Astra Militarum", Faction::AstraMilitarum, state.model_faction(), state, true);
  SelectFaction("Tau", Faction::Tau, state.model_faction(), state, true);
  SelectFaction("Necrons", Faction::Necrons, state.model_faction(), state, true);

  ImGui::Separator();
  ImGui::Text("Player Faction:");
  SelectFaction("Space Marine##enemy", Faction::SpaceMarine, state.enemy_faction(), state, false);
  SelectFaction("Orks##enemy", Faction::Orks, state.enemy_faction(), state, false);
  SelectFaction("Sisters of Battle##enemy", Faction::SistersOfBattle, state.enemy_faction(), state, false);
  SelectFaction("Adeptus Custodes##enemy", Faction::AdeptusCustodes, state.enemy_faction(), state, false);
  SelectFaction("Tyranids##enemy", Faction::Tyranids, state.enemy_faction(), state, false);
  SelectFaction("Astra Militarum##enemy", Faction::AstraMilitarum, state.enemy_faction(), state, false);
  SelectFaction("Tau##enemy", Faction::Tau, state.enemy_faction(), state, false);
  SelectFaction("Necrons##enemy", Faction::Necrons, state.enemy_faction(), state, false);

  ImGui::Separator();
  ImGui::Text("Статус: %s", state.status_message().c_str());
  ImGui::Text("%s", state.progress_label().c_str());
  ImGui::ProgressBar(state.progress_ratio(), ImVec2(0.0f, 0.0f));
  ImGui::Text("%s", state.progress_stats().c_str());

  ImGui::End();
}
