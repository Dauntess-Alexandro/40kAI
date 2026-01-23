#include <iostream>
#include <gtkmm.h>
#include <cstdlib>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <thread>
#include <chrono>
#include <cctype>

#include "include/popup.h"

using namespace Glib;
using namespace Gtk;

namespace {
std::string replace_tokens(std::string output, const std::string& token, const std::string& replacement) {
  std::string::size_type pos = 0;
  while ((pos = output.find(token, pos)) != std::string::npos) {
    output.replace(pos, token.size(), replacement);
    pos += replacement.size();
  }
  return output;
}

std::string replace_enemy_with_player(const std::string& input) {
  std::string output = input;
  output = replace_tokens(output, "enemy", "Игрок");
  output = replace_tokens(output, "Enemy", "Игрок");
  output = replace_tokens(output, "ENEMY", "Игрок");
  return output;
}

std::string to_title_case(std::string text) {
  if (!text.empty()) {
    text[0] = std::toupper(text[0]);
  }
  return text;
}

std::string parse_field(const std::string& input, const std::string& key) {
  auto pos = input.find(key);
  if (pos == std::string::npos) {
    return "";
  }
  pos += key.size();
  auto end = input.find('\n', pos);
  std::string value = input.substr(pos, end == std::string::npos ? std::string::npos : end - pos);
  while (!value.empty() && (value.front() == ' ' || value.front() == ':')) {
    value.erase(value.begin());
  }
  return value;
}

std::string replace_side_tokens(const std::string& input) {
  std::string output = input;
  output = replace_tokens(output, "enemy", "Игрок");
  output = replace_tokens(output, "Enemy", "Игрок");
  output = replace_tokens(output, "ENEMY", "Игрок");
  output = replace_tokens(output, "player", "Игрок");
  output = replace_tokens(output, "Player", "Игрок");
  output = replace_tokens(output, "PLAYER", "Игрок");
  output = replace_tokens(output, "model", "Модель");
  output = replace_tokens(output, "Model", "Модель");
  output = replace_tokens(output, "MODEL", "Модель");
  return output;
}
}

bool PopUp :: isNum(char num) {
  std::string nums= "0123456789";
  for (char n : nums) {
    if (n == num) {
      return true;
    }
  }
  return false;
}

std::string PopUp :: openFile(std::string board) {
  std::fstream file;
  file.open(board, std::ios::in);
  std::string fullFile;
  char last = '\0';
  if (!file) {
    std::cout << "File does not exist";
    fullFile.append(":(");
  } else {
    char ch;
    while (1) {
      file >> ch;
      if (file.eof()) {
        break;
      }
      if (last == '0' && ch != ',') {
        fullFile += '\n';
      } else if (ch == '0' && isNum(last)) {
        fullFile += '\n';
      } else if (isNum(ch) && ch != '0' && ch != '3') {
        fullFile += ch;
      } else if (isNum(ch) && ch == '3') {
        fullFile += '0';
        fullFile += '\x20';
      } else {
        fullFile += '_';
        fullFile += '\x20';
      }
      last = ch;
    }
  }
  file.close();
  return fullFile;
}

void PopUp :: update() {
  std::string boardpth = "../board.txt";
  std::string board;
  board = openFile(boardpth);
  if (!board.empty()) {
    boardText = board;
  }

  std::fstream file("response.txt", std::ios::in);
  if (file) {
    std::string line;
    response.clear();
    while (std::getline(file, line)) {
      response += line;
      response += "\n";
    }
    file.close();
  }
  dispatcher.emit();
}

void PopUp :: keepUpdating() {
  while (true) {
    update();
    std::this_thread::sleep_for(std::chrono::seconds(1));
  }
}

void PopUp :: backgroundUpdate(bool textMode) {
  std::thread t(&PopUp::keepUpdating, this);
  t.detach();
}

void PopUp :: update_text_view() {
  auto logBuffer = logView.get_buffer();
  if (logBuffer) {
    std::string cleaned = replace_enemy_with_player(response);
    logBuffer->set_text(cleaned);
    if (autoScrollToggle.get_active()) {
      auto endIter = logBuffer->end();
      logBuffer->place_cursor(endIter);
      logView.scroll_to(endIter);
    }
  }
  auto boardBuffer = boardView.get_buffer();
  if (boardBuffer) {
    boardBuffer->set_text(boardText);
  }
  if (!textModeActive) {
    pictureBox.set("img/board.png");
  }

  std::string cleaned = replace_enemy_with_player(response);
  auto turn = parse_field(cleaned, "Turn");
  auto round = parse_field(cleaned, "Round");
  auto phase = parse_field(cleaned, "Phase");
  auto active = parse_field(cleaned, "Active");
  auto vp = parse_field(cleaned, "VP");
  auto cp = parse_field(cleaned, "CP");

  std::string turnText = turn.empty() ? "?" : turn;
  std::string roundText = round.empty() ? "?" : round;
  std::string phaseText = phase.empty() ? "?" : to_title_case(phase);
  std::string activeText = active.empty() ? "?" : replace_side_tokens(active);

  std::string vpText = vp.empty() ? "0-0" : vp;
  std::string cpText = cp.empty() ? "Игрок 0 - 0 Модель" : cp;

  statusSummaryLabel.set_text("Ход " + turnText + " · Раунд " + roundText + " · Фаза " + phaseText + " · Активная сторона: " + activeText);
  statusSummaryLabel.set_tooltip_text(statusSummaryLabel.get_text());

  statusVpCpLabel.set_text("VP " + vpText + " | CP " + replace_side_tokens(cpText));
  statusVpCpLabel.set_tooltip_text(statusVpCpLabel.get_text());

  statusLinePrimary.set_text("Ход " + turnText + " · Раунд " + roundText + " · Фаза " + phaseText + " · Активная сторона: " + activeText);
  statusLinePrimary.set_tooltip_text(statusLinePrimary.get_text());

  statusLineSecondary.set_text("VP " + vpText + " | CP " + replace_side_tokens(cpText));
  statusLineSecondary.set_tooltip_text(statusLineSecondary.get_text());
}

PopUp :: PopUp(bool textMode) {
  system("cp img/boardINIT.png img/board.png");
  textModeActive = textMode;

  bar.set_show_close_button(true);
  set_titlebar(bar);
  bar.set_title("Поле битвы");

  set_default_size(1400, 900);
  set_size_request(1100, 750);
  set_resizable(true);

  rootBox.set_orientation(Gtk::ORIENTATION_VERTICAL);
  rootBox.set_spacing(6);
  topRow.set_orientation(Gtk::ORIENTATION_HORIZONTAL);
  topRow.set_spacing(8);
  rightSidebar.set_orientation(Gtk::ORIENTATION_VERTICAL);
  rightSidebar.set_spacing(8);
  statusBox.set_orientation(Gtk::ORIENTATION_VERTICAL);
  statusBox.set_spacing(6);
  legendBox.set_orientation(Gtk::ORIENTATION_VERTICAL);
  legendBox.set_spacing(6);
  statusBarBox.set_orientation(Gtk::ORIENTATION_VERTICAL);
  statusBarBox.set_spacing(4);
  logBox.set_orientation(Gtk::ORIENTATION_VERTICAL);
  logBox.set_spacing(4);
  logButtonsRow.set_orientation(Gtk::ORIENTATION_HORIZONTAL);
  logButtonsRow.set_spacing(8);
  logButtonsLeft.set_orientation(Gtk::ORIENTATION_HORIZONTAL);
  logButtonsLeft.set_spacing(6);
  logButtonsRight.set_orientation(Gtk::ORIENTATION_HORIZONTAL);
  logButtonsRight.set_spacing(6);

  add(rootBox);

  rootBox.pack_start(topRow, Gtk::PACK_EXPAND_WIDGET);
  rootBox.pack_start(statusBarFrame, Gtk::PACK_SHRINK);
  rootBox.pack_start(logFrame, Gtk::PACK_EXPAND_WIDGET);

  boardScroll.add(boardStack);
  boardScroll.set_policy(Gtk::POLICY_AUTOMATIC, Gtk::POLICY_AUTOMATIC);
  boardScroll.set_hexpand(true);
  boardScroll.set_vexpand(true);

  auto boardBuffer = Gtk::TextBuffer::create();
  boardView.set_buffer(boardBuffer);
  boardView.set_editable(false);
  boardView.set_monospace(true);
  boardView.set_wrap_mode(Gtk::WRAP_NONE);
  boardStack.add(boardView, "text");
  boardStack.add(pictureBox, "image");
  if (textMode) {
    boardStack.set_visible_child(boardView);
  } else {
    boardStack.set_visible_child(pictureBox);
  }

  topRow.pack_start(boardScroll, Gtk::PACK_EXPAND_WIDGET);

  rightSidebar.set_size_request(260, -1);
  topRow.pack_start(rightSidebar, Gtk::PACK_SHRINK);

  statusFrame.set_label("Статус");
  statusFrame.add(statusBox);
  statusSummaryLabel.set_text("Ход ? · Раунд ? · Фаза ? · Активная сторона: ?");
  statusSummaryLabel.set_xalign(0.0f);
  statusSummaryLabel.set_ellipsize(Pango::ELLIPSIZE_END);
  statusSummaryLabel.set_line_wrap(true);
  statusSummaryLabel.set_line_wrap_mode(Pango::WRAP_WORD_CHAR);
  statusVpCpLabel.set_text("VP 0-0 | CP Игрок 0 - 0 Модель");
  statusVpCpLabel.set_xalign(0.0f);
  statusVpCpLabel.set_ellipsize(Pango::ELLIPSIZE_END);
  statusVpCpLabel.set_line_wrap(true);
  statusVpCpLabel.set_line_wrap_mode(Pango::WRAP_WORD_CHAR);
  statusBox.pack_start(statusSummaryLabel, Gtk::PACK_SHRINK);
  statusBox.pack_start(statusVpCpLabel, Gtk::PACK_SHRINK);

  legendFrame.set_label("Легенда");
  legendFrame.add(legendBox);
  legendModelLabel.set_text("Модель");
  legendPlayerLabel.set_text("Игрок");
  legendObjectiveLabel.set_text("Маркеры целей");
  legendModelLabel.set_xalign(0.0f);
  legendPlayerLabel.set_xalign(0.0f);
  legendObjectiveLabel.set_xalign(0.0f);
  legendBox.pack_start(legendModelLabel, Gtk::PACK_SHRINK);
  legendBox.pack_start(legendPlayerLabel, Gtk::PACK_SHRINK);
  legendBox.pack_start(legendObjectiveLabel, Gtk::PACK_SHRINK);

  rightSidebar.pack_start(statusFrame, Gtk::PACK_SHRINK);
  rightSidebar.pack_start(legendFrame, Gtk::PACK_SHRINK);

  statusBarFrame.set_label("Статус");
  statusBarFrame.add(statusBarBox);
  statusLinePrimary.set_text("Ход ? · Раунд ? · Фаза ? · Активная сторона: ?");
  statusLineSecondary.set_text("VP 0-0 | CP Игрок 0 - 0 Модель");
  statusLinePrimary.set_xalign(0.0f);
  statusLineSecondary.set_xalign(0.0f);
  statusLinePrimary.set_ellipsize(Pango::ELLIPSIZE_END);
  statusLineSecondary.set_ellipsize(Pango::ELLIPSIZE_END);
  statusLinePrimary.set_line_wrap(true);
  statusLineSecondary.set_line_wrap(true);
  statusLinePrimary.set_line_wrap_mode(Pango::WRAP_WORD_CHAR);
  statusLineSecondary.set_line_wrap_mode(Pango::WRAP_WORD_CHAR);
  statusBarBox.pack_start(statusLinePrimary, Gtk::PACK_SHRINK);
  statusBarBox.pack_start(statusLineSecondary, Gtk::PACK_SHRINK);

  logFrame.set_label("Журнал");
  logFrame.add(logBox);

  auto logBuffer = Gtk::TextBuffer::create();
  logView.set_buffer(logBuffer);
  logView.set_editable(false);
  logView.set_wrap_mode(Gtk::WRAP_WORD_CHAR);

  logScroll.add(logView);
  logScroll.set_policy(Gtk::POLICY_AUTOMATIC, Gtk::POLICY_AUTOMATIC);
  logScroll.set_hexpand(true);
  logScroll.set_vexpand(true);

  clearLogButton.set_label("Очистить");
  clearLogButton.signal_clicked().connect([this]() {
    response.clear();
    auto buffer = logView.get_buffer();
    if (buffer) {
      buffer->set_text("");
    }
  });

  copyLogButton.set_label("Скопировать");
  copyLogButton.signal_clicked().connect([this]() {
    auto buffer = logView.get_buffer();
    if (buffer) {
      auto clipboard = Gtk::Clipboard::get_default();
      if (clipboard && buffer) {
        clipboard->set_text(buffer->get_text());
      }
    }
  });

  autoScrollToggle.set_label("Автопрокрутка");
  autoScrollToggle.set_active(true);

  logButtonsLeft.pack_start(clearLogButton, Gtk::PACK_SHRINK);
  logButtonsLeft.pack_start(copyLogButton, Gtk::PACK_SHRINK);
  logButtonsRight.pack_start(autoScrollToggle, Gtk::PACK_SHRINK);

  logButtonsRow.pack_start(logButtonsLeft, Gtk::PACK_SHRINK);
  logButtonsRow.pack_end(logButtonsRight, Gtk::PACK_SHRINK);

  logBox.pack_start(logScroll, Gtk::PACK_EXPAND_WIDGET);
  logBox.pack_start(logButtonsRow, Gtk::PACK_SHRINK);

  dispatcher.connect(sigc::mem_fun(*this, &PopUp::update_text_view));

  if (textMode == false) {
    backgroundUpdate(false);
  } else {
    backgroundUpdate(true);
  }

  show_all();
}

PopUp :: ~PopUp() {
  std::cout << "closed" << std::endl;
  system("cp img/boardINIT.png img/board.png");
}
