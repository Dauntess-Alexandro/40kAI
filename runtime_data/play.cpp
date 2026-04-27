#include <iostream>
#include <gtkmm.h>
#include <cstdlib>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <thread>
#include "include/play.h"

using namespace Glib;
using namespace Gtk;
using namespace std;

namespace {
bool is_board_num(char num) {
	string nums= "0123456789";
	for (char n : nums) {
		if (n == num) {
			return true;
		}
	}
	return false;
}
}

bool Play :: file_exists(char * fileName) {
	ifstream infile(fileName);
	return infile.good();
}

void Play :: update() {
	bool updated = false;
	if (file_exists("response.txt")) {
		ifstream file("response.txt");
		string line;
		while(getline(file, line)) {
			for (int i = 0; line.length() > i; i++) {
				response += line[i];
			}
			response += "\n";
		}
		file.close();
		updated = true;
	}

	string nextBoard = openBoardFile("../board.txt");
	if (!nextBoard.empty() && nextBoard != boardText) {
		boardText = nextBoard;
		updated = true;
	}

	if (updated) {
		dispatcher.emit();
	}
}

void Play :: update_text_view() {
	auto logBuffer = logView.get_buffer();
	if (logBuffer) {
		logBuffer->set_text(response);
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
	char responseFile[] = "response.txt";
	if (file_exists(responseFile)) {
		system("rm response.txt");
	}
}

void Play :: keepUpdating() {
	while (true) {
    	update();
    	std::this_thread::sleep_for(std::chrono::seconds(1));
	}
}

void Play :: backgroundUpdate() {
	std::thread t(&Play::keepUpdating, this);
	t.detach();
}

Play :: Play() {
	bar.set_show_close_button(true);
	set_titlebar(bar);

	set_default_size(1000, 700);
	set_size_request(800, 600);

	bar.set_title("Playing Against the Model");

	rootBox.set_orientation(Gtk::ORIENTATION_VERTICAL);
	mainSplit.set_orientation(Gtk::ORIENTATION_HORIZONTAL);
	rightSplit.set_orientation(Gtk::ORIENTATION_VERTICAL);
	leftControls.set_orientation(Gtk::ORIENTATION_VERTICAL);

	add(rootBox);
	rootBox.pack_start(mainSplit, Gtk::PACK_EXPAND_WIDGET);

	mainSplit.add1(leftControls);
	mainSplit.add2(rightSplit);
	mainSplit.set_position(260);

	rightSplit.add1(boardScroll);
	rightSplit.add2(logScroll);
	rightSplit.set_position(350);

	responseLabel.set_text("Enter Response Here");
	numBox.set_text("");

	enter.set_label("Enter");
	enter.signal_button_release_event().connect([&](GdkEventButton*) {	
		ofstream file("response.txt", ios::out | ios::trunc);
		file << numBox.get_text();
		file.close();
		numBox.set_text("");
		return true;
	});

	clearLogButton.set_label("Clear Logs");
	clearLogButton.signal_clicked().connect([this]() {
		response.clear();
		auto logBuffer = logView.get_buffer();
		if (logBuffer) {
			logBuffer->set_text("");
		}
	});
	autoScrollToggle.set_label("Auto-scroll logs");
	autoScrollToggle.set_active(true);

	auto logBuffer = Gtk::TextBuffer::create();
	logView.set_buffer(logBuffer);
	logView.set_editable(false);
	logView.set_wrap_mode(Gtk::WRAP_WORD_CHAR);

	auto boardBuffer = Gtk::TextBuffer::create();
	boardView.set_buffer(boardBuffer);
	boardView.set_editable(false);
	boardView.set_monospace(true);
	boardView.set_wrap_mode(Gtk::WRAP_NONE);

	dispatcher.connect(sigc::mem_fun(*this, &Play::update_text_view));
	backgroundUpdate();

	boardScroll.add(boardView);
	boardScroll.set_policy(PolicyType::POLICY_AUTOMATIC, PolicyType::POLICY_AUTOMATIC);
	logScroll.add(logView);
	logScroll.set_policy(PolicyType::POLICY_AUTOMATIC, PolicyType::POLICY_AUTOMATIC);

	leftControls.pack_start(responseLabel, Gtk::PACK_SHRINK);
	leftControls.pack_start(numBox, Gtk::PACK_SHRINK);
	leftControls.pack_start(enter, Gtk::PACK_SHRINK);
	leftControls.pack_start(clearLogButton, Gtk::PACK_SHRINK);
	leftControls.pack_start(autoScrollToggle, Gtk::PACK_SHRINK);

    show_all();
}

std::string Play :: openBoardFile(const std::string& board) {
	std::fstream file;
	file.open(board, std::ios::in);
	std::string fullFile;
	char last = '\0';
	if (!file) {
		return "";
	}
	char ch;
	while (1) {
		file >> ch;
		if (file.eof()) {
			break;
		}
		if (last == '0' && ch != ',') {
			fullFile += '\n';
		} else if (ch == '0' && is_board_num(last)) {
			fullFile += '\n';
		} else if (is_board_num(ch) && ch != '0' && ch != '3') {
			fullFile += ch;
		} else if (is_board_num(ch) && ch == '3') {
			fullFile += '0';
			fullFile += '\x20';
		} else {
			fullFile += '_';
			fullFile += '\x20';
		}
		last = ch;
	}
	file.close();
	return fullFile;
}
