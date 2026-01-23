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

void PopUp :: update() {
  std::string boardpth = "../board.txt";
  std::string board;
  board = openFile(boardpth);
  contents.set_text(board);
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
