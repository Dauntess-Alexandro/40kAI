#include <iostream>
#include <gtkmm.h>
#include <cstdlib>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <thread>
#include <chrono>
#include <sstream>

#include "include/popup.h"

using namespace Glib;
using namespace Gtk;

namespace {
std::string replace_all(std::string value, const std::string& from, const std::string& to) {
  size_t pos = 0;
  while ((pos = value.find(from, pos)) != std::string::npos) {
    value.replace(pos, from.length(), to);
    pos += to.length();
  }
  return value;
}

std::string normalize_side_label(const std::string& side) {
  if (side == "enemy" || side == "ENEMY" || side == "PLAYER") {
    return "Игрок";
  }
  if (side == "model" || side == "MODEL") {
    return "Модель";
  }
  return side;
}

std::string normalize_log_text(std::string text) {
  text = replace_all(text, "ENEMY", "Игрок");
  text = replace_all(text, "enemy", "Игрок");
  text = replace_all(text, "PLAYER", "Игрок");
  text = replace_all(text, "MODEL", "Модель");
  text = replace_all(text, "model", "Модель");
  return text;
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

void PopUp :: update() {
  std::string boardpth = "../board.txt";
  std::string board;
  board = openFile(boardpth);
  contents.set_text(board);

  std::ifstream statusFile("../status.txt");
  if (!statusFile) {
    statusFile.open("status.txt");
  }
  if (statusFile) {
    std::string line;
    std::string turn;
    std::string round;
    std::string phase;
    std::string activeSide;
    std::string modelVP;
    std::string playerVP;
    std::string modelCP;
    std::string playerCP;
    std::string modelHealth;
    std::string playerHealth;

    while (std::getline(statusFile, line)) {
      auto sep = line.find('=');
      if (sep == std::string::npos) {
        continue;
      }
      std::string key = line.substr(0, sep);
      std::string value = line.substr(sep + 1);
      if (key == "turn") {
        turn = value;
      } else if (key == "battle_round") {
        round = value;
      } else if (key == "phase") {
        phase = value;
      } else if (key == "active_side") {
        activeSide = value;
      } else if (key == "model_vp") {
        modelVP = value;
      } else if (key == "player_vp") {
        playerVP = value;
      } else if (key == "model_cp") {
        modelCP = value;
      } else if (key == "player_cp") {
        playerCP = value;
      } else if (key == "model_health") {
        modelHealth = value;
      } else if (key == "player_health") {
        playerHealth = value;
      }
    }

    std::string activeSideLabelText = "Активная сторона: " + normalize_side_label(activeSide);
    std::string vpText = "VP: " + modelVP + " – " + playerVP;
    std::string cpText = "CP: Игрок " + playerCP + " – " + modelCP + " Модель";
    std::string turnRoundText = "Ход: " + turn + "   Раунд: " + round;
    std::string phaseText = "Фаза: " + phase;
    std::string healthText = "HP Модель: " + modelHealth + " | HP Игрок: " + playerHealth;

    turnRoundLabel.set_text(turnRoundText);
    phaseLabel.set_text(phaseText);
    activeSideLabel.set_text(activeSideLabelText);
    vpLabel.set_text(vpText);
    cpLabel.set_text(cpText);

    turnRoundLabel.set_tooltip_text(turnRoundText + "\n" + healthText);
    phaseLabel.set_tooltip_text(phaseText + "\n" + healthText);
    activeSideLabel.set_tooltip_text(activeSideLabelText + "\n" + healthText);
    vpLabel.set_tooltip_text(vpText + "\n" + healthText);
    cpLabel.set_tooltip_text(cpText + "\n" + healthText);
  }

  std::ifstream logFile("../response.txt");
  if (!logFile) {
    logFile.open("response.txt");
  }
  if (logFile && logBuffer) {
    std::stringstream buffer;
    buffer << logFile.rdbuf();
    std::string message = buffer.str();
    if (!message.empty()) {
      message = normalize_log_text(message);
      if (message != lastLogMessage) {
        logBuffer->insert(logBuffer->end(), message + "\n");
        auto endIter = logBuffer->end();
        logView.scroll_to(endIter);
        lastLogMessage = message;
      }
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

PopUp :: PopUp(bool textMode) {

  system("cp img/boardINIT.png img/board.png");
  bar.set_show_close_button(true);
  set_titlebar(bar);

  bar.set_title("Game Board");
  set_default_size(1400, 900);
  set_size_request(1100, 750);

  rootBox.set_orientation(Gtk::ORIENTATION_VERTICAL);
  mainSplit.set_orientation(Gtk::ORIENTATION_VERTICAL);
  boardArea.set_orientation(Gtk::ORIENTATION_HORIZONTAL);
  statusPanel.set_orientation(Gtk::ORIENTATION_VERTICAL);

  rootBox.set_hexpand(true);
  rootBox.set_vexpand(true);
  mainSplit.set_hexpand(true);
  mainSplit.set_vexpand(true);
  boardArea.set_hexpand(true);
  boardArea.set_vexpand(true);

  add(rootBox);
  rootBox.pack_start(mainSplit, Gtk::PACK_EXPAND_WIDGET);

  if (textMode == false) {
	backgroundUpdate(false);
  } else {
	backgroundUpdate(true);
  } 
  
  boardFrame.set_label("Board");
  boardFrame.set_hexpand(true);
  boardFrame.set_vexpand(true);
  boardScroll.set_hexpand(true);
  boardScroll.set_vexpand(true);
  boardScroll.set_policy(PolicyType::POLICY_AUTOMATIC, PolicyType::POLICY_AUTOMATIC);
  boardFrame.add(boardScroll);

  boardFixed.add(contents);
  boardFixed.move(contents, 0, 0);
  boardFixed.add(pictureBox);
  boardFixed.move(pictureBox, 0, 0);
  boardScroll.add(boardFixed);

  contents.set_xalign(0.0);
  contents.set_yalign(0.0);

  statusFrame.set_label("Статус");
  statusFrame.set_size_request(260, -1);
  statusFrame.set_hexpand(false);
  statusFrame.set_vexpand(true);
  statusPanel.set_spacing(6);
  statusPanel.set_margin_start(8);
  statusPanel.set_margin_end(8);
  statusPanel.set_margin_top(8);
  statusPanel.set_margin_bottom(8);

  turnRoundLabel.set_text("Ход: —   Раунд: —");
  phaseLabel.set_text("Фаза: —");
  activeSideLabel.set_text("Активная сторона: Игрок");
  vpLabel.set_text("VP: — – —");
  cpLabel.set_text("CP: Игрок — – — Модель");
  legendLabel.set_text("Легенда: Игрок / Модель");

  turnRoundLabel.set_ellipsize(Pango::ELLIPSIZE_END);
  phaseLabel.set_ellipsize(Pango::ELLIPSIZE_END);
  activeSideLabel.set_ellipsize(Pango::ELLIPSIZE_END);
  vpLabel.set_ellipsize(Pango::ELLIPSIZE_END);
  cpLabel.set_ellipsize(Pango::ELLIPSIZE_END);
  legendLabel.set_ellipsize(Pango::ELLIPSIZE_END);

  turnRoundLabel.set_tooltip_text("Ход: —   Раунд: —");
  phaseLabel.set_tooltip_text("Фаза: —");
  activeSideLabel.set_tooltip_text("Активная сторона: Игрок");
  vpLabel.set_tooltip_text("VP: — – —");
  cpLabel.set_tooltip_text("CP: Игрок — – — Модель");
  legendLabel.set_tooltip_text("Легенда: Игрок / Модель");

  turnRoundLabel.set_xalign(0.0);
  phaseLabel.set_xalign(0.0);
  activeSideLabel.set_xalign(0.0);
  vpLabel.set_xalign(0.0);
  cpLabel.set_xalign(0.0);
  legendLabel.set_xalign(0.0);

  statusPanel.pack_start(turnRoundLabel, Gtk::PACK_SHRINK);
  statusPanel.pack_start(phaseLabel, Gtk::PACK_SHRINK);
  statusPanel.pack_start(activeSideLabel, Gtk::PACK_SHRINK);
  statusPanel.pack_start(vpLabel, Gtk::PACK_SHRINK);
  statusPanel.pack_start(cpLabel, Gtk::PACK_SHRINK);
  statusPanel.pack_start(legendLabel, Gtk::PACK_SHRINK);
  statusFrame.add(statusPanel);

  logFrame.set_label("Журнал");
  logFrame.set_hexpand(true);
  logFrame.set_vexpand(true);
  logView.set_hexpand(true);
  logView.set_vexpand(true);
  logView.set_editable(false);
  logView.set_wrap_mode(Gtk::WRAP_WORD_CHAR);
  logBuffer = Gtk::TextBuffer::create();
  logView.set_buffer(logBuffer);

  logScroll.set_hexpand(true);
  logScroll.set_vexpand(true);
  logScroll.set_policy(PolicyType::POLICY_AUTOMATIC, PolicyType::POLICY_AUTOMATIC);
  logScroll.add(logView);
  logFrame.add(logScroll);

  boardArea.pack_start(boardFrame, Gtk::PACK_EXPAND_WIDGET);
  boardArea.pack_start(statusFrame, Gtk::PACK_SHRINK);

  mainSplit.add1(boardArea);
  mainSplit.add2(logFrame);
  mainSplit.set_position(700);

  show_all();
  if (textMode) {
    pictureBox.hide();
    contents.show();
  } else {
    contents.hide();
    pictureBox.show();
  }
}

PopUp :: ~PopUp() {
	std::cout << "closed" << std::endl;
	system("cp img/boardINIT.png img/board.png");
}
