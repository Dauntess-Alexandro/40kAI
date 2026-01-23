#include <iostream>
#include <gtkmm.h>
#include <cstdlib>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <thread>
#include <chrono>
#include <sstream>
#include <regex>
#include <map>
#include <vector>
#include <algorithm>

#include "include/popup.h"

using namespace Glib;
using namespace Gtk;

namespace {
std::string trim(const std::string &text) {
  auto start = text.find_first_not_of(" \t\n\r");
  if (start == std::string::npos) {
    return "";
  }
  auto end = text.find_last_not_of(" \t\n\r");
  return text.substr(start, end - start + 1);
}

std::vector<int> parse_int_list(const std::string &text) {
  std::vector<int> values;
  auto start = text.find('[');
  auto end = text.find(']');
  if (start == std::string::npos || end == std::string::npos || end <= start) {
    return values;
  }
  std::string inner = text.substr(start + 1, end - start - 1);
  std::stringstream ss(inner);
  std::string item;
  while (std::getline(ss, item, ',')) {
    item = trim(item);
    if (item.empty()) {
      continue;
    }
    try {
      values.push_back(std::stoi(item));
    } catch (const std::exception &) {
      continue;
    }
  }
  return values;
}

std::string display_side_label(const std::string &side) {
  if (side == "PLAYER" || side == "enemy") {
    return "Игрок";
  }
  if (side == "MODEL" || side == "model") {
    return "Модель";
  }
  return side;
}

std::map<int, std::string> extract_unit_labels(const std::string &text) {
  std::map<int, std::string> labels;
  std::istringstream stream(text);
  std::string line;
  std::regex id_pattern(R"(\((\d+)\))");
  while (std::getline(stream, line)) {
    std::smatch match;
    if (!std::regex_search(line, match, id_pattern)) {
      continue;
    }
    int id = std::stoi(match[1].str());
    auto open = line.rfind('(');
    if (open == std::string::npos) {
      continue;
    }
    std::string name = trim(line.substr(0, open));
    auto bracket = name.rfind("] ");
    if (bracket != std::string::npos) {
      name = trim(name.substr(bracket + 2));
    }
    if (!name.empty()) {
      labels[id] = name;
    }
  }
  return labels;
}

std::string format_hp_line(const std::string &side_label,
                           const std::vector<int> &health,
                           int base_id,
                           const std::map<int, std::string> &labels) {
  if (health.empty()) {
    return side_label + ": —";
  }
  std::string result = side_label + ": ";
  for (size_t i = 0; i < health.size(); ++i) {
    int unit_id = base_id + static_cast<int>(i);
    auto label_it = labels.find(unit_id);
    std::string name = label_it != labels.end() ? label_it->second : "Юнит";
    result += name + " (" + std::to_string(unit_id) + ")=" + std::to_string(health[i]);
    if (i + 1 < health.size()) {
      result += ", ";
    }
  }
  return result;
}
}  // namespace

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

  std::string responsePath = "../response.txt";
  std::ifstream responseFile(responsePath);
  if (!responseFile) {
    return;
  }
  std::string response((std::istreambuf_iterator<char>(responseFile)),
                       std::istreambuf_iterator<char>());
  if (response.empty() || response == lastResponse) {
    return;
  }
  lastResponse = response;

  if (logBuffer) {
    std::istringstream logStream(response);
    std::string line;
    while (std::getline(logStream, line)) {
      logBuffer->insert(logBuffer->end(), line + "\n");
    }
    auto endIter = logBuffer->end();
    logView.scroll_to(endIter);
  }

  auto labels = extract_unit_labels(response);

  auto roundPos = response.rfind("=== БОЕВОЙ РАУНД ");
  if (roundPos != std::string::npos) {
    auto start = roundPos + std::string("=== БОЕВОЙ РАУНД ").size();
    auto end = response.find(" ===", start);
    if (end != std::string::npos) {
      lastRound = response.substr(start, end - start);
    }
  }

  auto turnPos = response.rfind("--- ХОД ");
  if (turnPos != std::string::npos) {
    auto start = turnPos + std::string("--- ХОД ").size();
    auto end = response.find(" ---", start);
    if (end != std::string::npos) {
      lastTurnSide = display_side_label(trim(response.substr(start, end - start)));
      lastActiveSide = lastTurnSide;
    }
  }

  auto phasePos = response.rfind("--- ФАЗА ");
  if (phasePos != std::string::npos) {
    auto start = phasePos + std::string("--- ").size();
    auto end = response.find(" ---", start);
    if (end != std::string::npos) {
      lastPhase = trim(response.substr(start, end - start));
    }
  }

  auto healthPos = response.find("Здоровье MODEL:");
  if (healthPos != std::string::npos) {
    auto cpPos = response.find("\nCP", healthPos);
    std::string healthLine = response.substr(
        healthPos,
        cpPos == std::string::npos ? std::string::npos : cpPos - healthPos);
    auto playerPos = healthLine.find(", здоровье ");
    if (playerPos != std::string::npos) {
      std::string modelPart = healthLine.substr(0, playerPos);
      std::string playerPart = healthLine.substr(playerPos + std::string(", здоровье ").size());
      auto modelHealth = parse_int_list(modelPart);
      auto playerHealth = parse_int_list(playerPart);
      lastModelHp = format_hp_line("HP Модель", modelHealth, 21, labels);
      lastPlayerHp = format_hp_line("HP Игрок", playerHealth, 11, labels);
    }
  }

  auto cpPos = response.find("CP MODEL:");
  if (cpPos != std::string::npos) {
    auto vpPos = response.find("\nVP", cpPos);
    std::string cpLine = response.substr(
        cpPos,
        vpPos == std::string::npos ? std::string::npos : vpPos - cpPos);
    std::regex cpPattern(R"(CP MODEL:\s*(\d+),\s*CP (\w+):\s*(\d+))");
    std::smatch match;
    if (std::regex_search(cpLine, match, cpPattern)) {
      std::string playerLabel = display_side_label(match[2].str());
      lastCp = "CP: " + playerLabel + " " + match[3].str() + " – " + match[1].str() + " Модель";
    }
  }

  auto vpPos = response.find("VP MODEL:");
  if (vpPos != std::string::npos) {
    std::string vpLine = response.substr(vpPos);
    std::regex vpPattern(R"(VP MODEL:\s*(\d+),\s*VP (\w+):\s*(\d+))");
    std::smatch match;
    if (std::regex_search(vpLine, match, vpPattern)) {
      std::string playerLabel = display_side_label(match[2].str());
      lastVp = "VP: " + playerLabel + " " + match[3].str() + " – " + match[1].str() + " Модель";
    }
  }

  std::string roundText = lastRound.empty() ? "—" : lastRound;
  std::string turnText = lastTurnSide.empty() ? "—" : lastTurnSide;
  std::string phaseText = lastPhase.empty() ? "—" : lastPhase;
  std::string activeText = lastActiveSide.empty() ? "—" : lastActiveSide;
  std::string vpText = lastVp.empty() ? "VP: — – —" : lastVp;
  std::string cpText = lastCp.empty() ? "CP: Игрок — – — Модель" : lastCp;

  turnRoundLabel.set_text("Ход: " + turnText + "   Раунд: " + roundText);
  phaseLabel.set_text("Фаза: " + phaseText);
  activeSideLabel.set_text("Активная сторона: " + activeText);
  vpLabel.set_text(vpText);
  cpLabel.set_text(cpText);
  std::string playerHpText = lastPlayerHp.empty() ? "HP Игрок: —" : lastPlayerHp;
  std::string modelHpText = lastModelHp.empty() ? "HP Модель: —" : lastModelHp;
  legendLabel.set_text(playerHpText);
  legendLabel.set_tooltip_text(playerHpText);
  modelHpLabel.set_text(modelHpText);
  modelHpLabel.set_tooltip_text(modelHpText);
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
		update();
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
  legendLabel.set_text("HP Игрок: —");
  modelHpLabel.set_text("HP Модель: —");

  turnRoundLabel.set_ellipsize(Pango::ELLIPSIZE_END);
  phaseLabel.set_ellipsize(Pango::ELLIPSIZE_END);
  activeSideLabel.set_ellipsize(Pango::ELLIPSIZE_END);
  vpLabel.set_ellipsize(Pango::ELLIPSIZE_END);
  cpLabel.set_ellipsize(Pango::ELLIPSIZE_END);
  legendLabel.set_ellipsize(Pango::ELLIPSIZE_END);
  modelHpLabel.set_ellipsize(Pango::ELLIPSIZE_END);

  turnRoundLabel.set_tooltip_text("Ход: —   Раунд: —");
  phaseLabel.set_tooltip_text("Фаза: —");
  activeSideLabel.set_tooltip_text("Активная сторона: Игрок");
  vpLabel.set_tooltip_text("VP: — – —");
  cpLabel.set_tooltip_text("CP: Игрок — – — Модель");
  legendLabel.set_tooltip_text("HP Игрок: —");
  modelHpLabel.set_tooltip_text("HP Модель: —");

  turnRoundLabel.set_xalign(0.0);
  phaseLabel.set_xalign(0.0);
  activeSideLabel.set_xalign(0.0);
  vpLabel.set_xalign(0.0);
  cpLabel.set_xalign(0.0);
  legendLabel.set_xalign(0.0);
  modelHpLabel.set_xalign(0.0);

  statusPanel.pack_start(turnRoundLabel, Gtk::PACK_SHRINK);
  statusPanel.pack_start(phaseLabel, Gtk::PACK_SHRINK);
  statusPanel.pack_start(activeSideLabel, Gtk::PACK_SHRINK);
  statusPanel.pack_start(vpLabel, Gtk::PACK_SHRINK);
  statusPanel.pack_start(cpLabel, Gtk::PACK_SHRINK);
  statusPanel.pack_start(legendLabel, Gtk::PACK_SHRINK);
  statusPanel.pack_start(modelHpLabel, Gtk::PACK_SHRINK);
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
  show_all();
  mainSplit.set_position(650);
  Glib::signal_idle().connect_once([this]() {
    auto height = get_allocated_height();
    if (height > 0) {
      mainSplit.set_position(static_cast<int>(height * 0.7));
    }
  });
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
