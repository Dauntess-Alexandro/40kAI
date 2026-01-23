#include <iostream>
#include <gtkmm.h>
#include <cstdlib>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <thread>
#include <chrono>
#include <sstream>
#include <algorithm>
#include <cctype>

#include "include/popup.h"

using namespace Glib;
using namespace Gtk;

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
  char last; 
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

std::string PopUp :: openStatusFile(const std::string& statusFile) {
  std::ifstream file(statusFile);
  if (!file) {
    return "Status data is not available yet.";
  }
  std::string statusText((std::istreambuf_iterator<char>(file)),
                         std::istreambuf_iterator<char>());
  if (statusText.empty()) {
    return "Status data is not available yet.";
  }
  return statusText;
}

std::string PopUp :: openLogFile(const std::string& logFile) {
  std::ifstream file(logFile);
  if (!file) {
    return "";
  }
  std::string logText((std::istreambuf_iterator<char>(file)),
                      std::istreambuf_iterator<char>());
  return logText;
}

void PopUp :: applyStyles() {
  auto cssProvider = Gtk::CssProvider::create();
  cssProvider->load_from_data(
      "window, .board-popup {"
      "  background-color: #2c2c2c;"
      "  color: #e6e1d5;"
      "}"
      ".board-frame, .panel-frame, .status-bar, .log-frame {"
      "  background-color: #3a3a3a;"
      "  border: 1px solid #1f1f1f;"
      "  border-radius: 6px;"
      "  padding: 6px;"
      "}"
      ".panel-frame {"
      "  background-color: #353535;"
      "}"
      ".status-text, .legend-text, .status-bar-text {"
      "  color: #e6e1d5;"
      "  font-size: 13px;"
      "}"
      ".status-title, .legend-title, .log-title {"
      "  color: #d8c9a7;"
      "  font-weight: bold;"
      "}"
      ".log-view text {"
      "  color: #d0d0d0;"
      "}"
      "separator {"
      "  background-color: #1f1f1f;"
      "  min-height: 1px;"
      "}"
  );
  auto screen = Gdk::Screen::get_default();
  if (screen) {
    Gtk::StyleContext::add_provider_for_screen(
        screen, cssProvider, GTK_STYLE_PROVIDER_PRIORITY_USER);
  }
}

void PopUp :: update() {
  std::string boardpth = "../board.txt";
  std::string board;
  board = openFile(boardpth);
  auto buffer = boardView.get_buffer();
  if (buffer) {
    buffer->set_text(board);
  }
  std::string statusText = openStatusFile("../board_status.txt");
  statusLabel.set_text(statusText);
  statusFrame.set_tooltip_text(statusText);

  auto trim_left = [](std::string value) {
    value.erase(value.begin(), std::find_if(value.begin(), value.end(),
                                           [](unsigned char ch) { return !std::isspace(ch); }));
    return value;
  };
  std::istringstream statusStream(statusText);
  std::string line;
  std::string turn;
  std::string round;
  std::string phase;
  std::string active;
  std::string vp;
  std::string cp;
  while (std::getline(statusStream, line)) {
    if (line.rfind("Turn:", 0) == 0) {
      turn = trim_left(line.substr(5));
    } else if (line.rfind("Round:", 0) == 0) {
      round = trim_left(line.substr(6));
    } else if (line.rfind("Phase:", 0) == 0) {
      phase = trim_left(line.substr(6));
    } else if (line.rfind("Active Player:", 0) == 0) {
      active = trim_left(line.substr(14));
    } else if (line.rfind("VP:", 0) == 0) {
      vp = trim_left(line.substr(3));
    } else if (line.rfind("CP:", 0) == 0) {
      cp = trim_left(line.substr(3));
    }
  }
  auto split_dash = [&trim_left](const std::string& value) {
    std::string left;
    std::string right;
    auto dash = value.find('-');
    if (dash != std::string::npos) {
      left = trim_left(value.substr(0, dash));
      right = trim_left(value.substr(dash + 1));
    } else {
      left = trim_left(value);
    }
    return std::make_pair(left, right);
  };

  if (!turn.empty() || !round.empty() || !phase.empty() || !active.empty()) {
    statusTurnLabel.set_text("Turn " + turn + " • Round " + round);
    statusPhaseLabel.set_text("Phase " + phase);
    statusActiveLabel.set_text("Active " + active);
    auto vpParts = split_dash(vp);
    auto cpParts = split_dash(cp);
    statusVpLabel.set_text("VP " + vpParts.first + " - " + vpParts.second);
    statusCpLabel.set_text("CP Player " + cpParts.second + " - " + cpParts.first + " Model");
    statusBarLabel.set_text("Turn " + turn + " • Round " + round + " • Phase " + phase +
                            " • Active " + active + "\nVP " + vpParts.first + " - " + vpParts.second +
                            " | CP Player " + cpParts.second + " - " + cpParts.first + " Model");
  } else {
    statusTurnLabel.set_text("Waiting for status data...");
    statusPhaseLabel.set_text("");
    statusActiveLabel.set_text("");
    statusVpLabel.set_text("");
    statusCpLabel.set_text("");
    statusBarLabel.set_text("Waiting for status data...");
  }

  std::string latestLog = openLogFile("response.txt");
  if (!latestLog.empty() && latestLog != lastLogLine) {
    lastLogLine = latestLog;
    std::istringstream logStream(latestLog);
    std::string logLine;
    while (std::getline(logStream, logLine)) {
      if (logLine.empty()) {
        continue;
      }
      logText += "• " + logLine + "\n";
    }
  }
  auto logBuffer = logView.get_buffer();
  if (logBuffer) {
    logBuffer->set_text(logText);
    if (autoScrollToggle.get_active()) {
      auto endIter = logBuffer->end();
      logBuffer->place_cursor(endIter);
      logView.scroll_to(endIter);
    }
  }
}

void PopUp :: keepUpdating() {
  while (true) {
    update();
    std::this_thread::sleep_for(std::chrono::seconds(1));
  }
}

void PopUp :: updateImage() {
	pictureBox.set("img/board.png");
  update();
}

void PopUp :: keepUpdatingElecBoogaloo() {
	while (true) {
		updateImage();
		std::this_thread::sleep_for(std::chrono::seconds(1));
	}
}

void PopUp :: backgroundUpdate(bool textMode) {
  if (textMode == true) {
	std::thread t(&PopUp::keepUpdating, this);
	t.detach();
  } else {
	std::thread t(&PopUp::keepUpdatingElecBoogaloo, this);
	t.detach();
  }  
}

PopUp :: PopUp(bool textMode)
    : rootBox(Gtk::ORIENTATION_VERTICAL),
      mainSplit(Gtk::ORIENTATION_HORIZONTAL),
      sideBox(Gtk::ORIENTATION_VERTICAL),
      statusBarBox(Gtk::ORIENTATION_VERTICAL),
      statusContentBox(Gtk::ORIENTATION_VERTICAL),
      logBox(Gtk::ORIENTATION_VERTICAL),
      logControls(Gtk::ORIENTATION_HORIZONTAL),
      textModeEnabled(textMode) {

  system("cp img/boardINIT.png img/board.png");
  bar.set_show_close_button(true);
  set_titlebar(bar);

  applyStyles();

  add(rootBox);
  rootBox.set_margin_start(8);
  rootBox.set_margin_end(8);
  rootBox.set_margin_top(8);
  rootBox.set_margin_bottom(8);
  rootBox.get_style_context()->add_class("board-popup");
  rootBox.pack_start(mainSplit, Gtk::PACK_EXPAND_WIDGET);
  rootBox.pack_start(statusBarFrame, Gtk::PACK_SHRINK);
  rootBox.pack_start(logFrame, Gtk::PACK_EXPAND_WIDGET);
  
  bar.set_title("Game Board");
  if (textMode == false) {
	backgroundUpdate(false);
  } else {
	backgroundUpdate(true);
  } 
  
  boardFrame.set_label("Board");
  boardFrame.set_hexpand(true);
  boardFrame.set_vexpand(true);
  boardFrame.get_style_context()->add_class("board-frame");
  boardStack.set_hexpand(true);
  boardStack.set_vexpand(true);

  boardView.set_editable(false);
  boardView.set_monospace(true);
  boardView.set_wrap_mode(Gtk::WRAP_WORD_CHAR);
  boardScroll.add(boardView);
  boardScroll.set_policy(PolicyType::POLICY_AUTOMATIC, PolicyType::POLICY_AUTOMATIC);

  boardStack.add(pictureBox, "board-image");
  boardStack.add(boardScroll, "board-text");
  boardStack.set_visible_child(textModeEnabled ? "board-text" : "board-image");
  boardFrame.add(boardStack);

  statusFrame.set_label("Status");
  statusFrame.get_style_context()->add_class("panel-frame");
  statusFrame.set_margin_bottom(8);
  statusLabel.set_xalign(0.0f);
  statusLabel.set_line_wrap(true);
  statusLabel.set_max_width_chars(40);
  statusLabel.get_style_context()->add_class("status-text");
  statusLabel.set_no_show_all(true);

  statusTurnLabel.set_xalign(0.0f);
  statusPhaseLabel.set_xalign(0.0f);
  statusActiveLabel.set_xalign(0.0f);
  statusVpLabel.set_xalign(0.0f);
  statusCpLabel.set_xalign(0.0f);
  statusTurnLabel.get_style_context()->add_class("status-text");
  statusPhaseLabel.get_style_context()->add_class("status-text");
  statusActiveLabel.get_style_context()->add_class("status-text");
  statusVpLabel.get_style_context()->add_class("status-text");
  statusCpLabel.get_style_context()->add_class("status-text");

  statusContentBox.set_spacing(6);
  statusContentBox.pack_start(statusTurnLabel, Gtk::PACK_SHRINK);
  statusContentBox.pack_start(statusSeparatorTop, Gtk::PACK_SHRINK);
  statusContentBox.pack_start(statusPhaseLabel, Gtk::PACK_SHRINK);
  statusContentBox.pack_start(statusActiveLabel, Gtk::PACK_SHRINK);
  statusContentBox.pack_start(statusSeparatorBottom, Gtk::PACK_SHRINK);
  statusContentBox.pack_start(statusVpLabel, Gtk::PACK_SHRINK);
  statusContentBox.pack_start(statusCpLabel, Gtk::PACK_SHRINK);
  statusFrame.add(statusContentBox);

  legendFrame.set_label("Legend");
  legendFrame.get_style_context()->add_class("panel-frame");
  legendLabel.set_xalign(0.0f);
  legendLabel.set_line_wrap(true);
  legendLabel.set_use_markup(true);
  legendLabel.set_markup(
      "<span foreground=\"#5a78b5\">●</span> Model Units\n"
      "<span foreground=\"#5e8f4b\">●</span> Player Units\n"
      "<span foreground=\"#2b2b2b\">●</span> Objective Markers");
  legendLabel.get_style_context()->add_class("legend-text");
  legendFrame.add(legendLabel);

  sideBox.set_spacing(10);
  sideBox.set_margin_start(8);
  sideBox.set_margin_end(8);
  sideBox.set_margin_top(8);
  sideBox.set_margin_bottom(8);
  sideBox.pack_start(statusFrame, Gtk::PACK_SHRINK);
  sideBox.pack_start(legendFrame, Gtk::PACK_SHRINK);

  mainSplit.set_wide_handle(true);
  mainSplit.add1(boardFrame);
  mainSplit.add2(sideBox);
  mainSplit.set_position(650);

  statusBarFrame.set_label(" ");
  statusBarFrame.get_style_context()->add_class("status-bar");
  statusBarFrame.set_margin_top(8);
  statusBarFrame.set_margin_bottom(4);
  statusBarLabel.set_xalign(0.0f);
  statusBarLabel.set_line_wrap(true);
  statusBarLabel.get_style_context()->add_class("status-bar-text");
  statusBarBox.set_spacing(4);
  statusBarBox.pack_start(statusBarLabel, Gtk::PACK_SHRINK);
  statusBarFrame.add(statusBarBox);

  logFrame.set_label("Log");
  logFrame.get_style_context()->add_class("log-frame");
  logFrame.set_margin_top(4);
  auto logBuffer = Gtk::TextBuffer::create();
  logView.set_buffer(logBuffer);
  logView.set_editable(false);
  logView.set_wrap_mode(Gtk::WRAP_WORD_CHAR);
  logView.get_style_context()->add_class("log-view");
  logScroll.add(logView);
  logScroll.set_policy(PolicyType::POLICY_AUTOMATIC, PolicyType::POLICY_AUTOMATIC);

  clearLogButton.set_label("Clear");
  clearLogButton.signal_clicked().connect([this]() {
    logText.clear();
    auto buffer = logView.get_buffer();
    if (buffer) {
      buffer->set_text("");
    }
  });
  copyLogButton.set_label("Copy Log");
  copyLogButton.signal_clicked().connect([this]() {
    auto clipboard = Gtk::Clipboard::get();
    if (clipboard) {
      clipboard->set_text(logText);
    }
  });
  autoScrollToggle.set_label("Auto-scroll");
  autoScrollToggle.set_active(true);
  logControls.set_spacing(8);
  logControls.pack_start(clearLogButton, Gtk::PACK_SHRINK);
  logControls.pack_start(copyLogButton, Gtk::PACK_SHRINK);
  logControls.pack_end(autoScrollToggle, Gtk::PACK_SHRINK);

  logBox.set_spacing(6);
  logBox.pack_start(logScroll, Gtk::PACK_EXPAND_WIDGET);
  logBox.pack_start(logControls, Gtk::PACK_SHRINK);
  logFrame.add(logBox);

  update();

  resize(900,700);
  show_all();
}

PopUp :: ~PopUp() {
	std::cout << "closed" << std::endl;
	system("cp img/boardINIT.png img/board.png");
}
