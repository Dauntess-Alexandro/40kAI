#pragma once

enum class TabPosition {
  Top,
  Left,
  Right,
  Bottom
};

class AppState {
 public:
  AppState();

  void IncrementClicks();
  int clicks() const;

  void set_show_demo(bool value);
  bool show_demo() const;

  void set_tab_position(TabPosition position);
  TabPosition tab_position() const;

  const char* TabPositionLabel(TabPosition position) const;

 private:
  int clicks_;
  bool show_demo_;
  TabPosition tab_position_;
};
