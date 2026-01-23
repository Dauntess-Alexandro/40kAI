#include <iostream>
#include <gtkmm.h>
#include <cstdlib>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <thread>
#include <chrono>

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
  statusLabel.set_tooltip_text(statusText);
}

void PopUp :: keepUpdating() {
  while (true) {
    update();
    std::this_thread::sleep_for(std::chrono::seconds(1));
  }
}

void PopUp :: updateImage() {
	pictureBox.set("img/board.png");
  std::string statusText = openStatusFile("../board_status.txt");
  statusLabel.set_text(statusText);
  statusLabel.set_tooltip_text(statusText);
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
      textModeEnabled(textMode) {

  system("cp img/boardINIT.png img/board.png");
  bar.set_show_close_button(true);
  set_titlebar(bar);

  add(rootBox);
  rootBox.pack_start(mainSplit, Gtk::PACK_EXPAND_WIDGET);
  
  bar.set_title("Game Board");
  if (textMode == false) {
	backgroundUpdate(false);
  } else {
	backgroundUpdate(true);
  } 
  
  boardFrame.set_label("Board");
  boardFrame.set_hexpand(true);
  boardFrame.set_vexpand(true);
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
  statusLabel.set_xalign(0.0f);
  statusLabel.set_line_wrap(true);
  statusLabel.set_max_width_chars(40);
  statusFrame.add(statusLabel);

  legendFrame.set_label("Legend");
  legendLabel.set_xalign(0.0f);
  legendLabel.set_line_wrap(true);
  legendLabel.set_text("• Model Unit (blue)\n• Player Unit (green)\n• Objective Marker (black)");
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

  update();

  resize(800,500);
  show_all();
}

PopUp :: ~PopUp() {
	std::cout << "closed" << std::endl;
	system("cp img/boardINIT.png img/board.png");
}
