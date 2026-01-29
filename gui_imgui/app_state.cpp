#include "app_state.h"

AppState::AppState()
    : clicks_(0),
      show_demo_(false),
      tab_position_(TabPosition::Top) {}

void AppState::IncrementClicks() {
  ++clicks_;
}

int AppState::clicks() const {
  return clicks_;
}

void AppState::set_show_demo(bool value) {
  show_demo_ = value;
}

bool AppState::show_demo() const {
  return show_demo_;
}

void AppState::set_tab_position(TabPosition position) {
  tab_position_ = position;
}

TabPosition AppState::tab_position() const {
  return tab_position_;
}

const char* AppState::TabPositionLabel(TabPosition position) const {
  switch (position) {
    case TabPosition::Top:
      return "Сверху";
    case TabPosition::Left:
      return "Слева";
    case TabPosition::Right:
      return "Справа";
    case TabPosition::Bottom:
      return "Снизу";
    default:
      return "Неизвестно";
  }
}
