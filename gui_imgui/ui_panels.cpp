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
