#ifndef PLAY_H
#define PLAY_H

#include <iostream>
#include <gtkmm.h>
#include <cstdlib>
#include <stdlib.h>
#include <string>

using namespace Glib;
using namespace Gtk;
using namespace std;

class Play : public Gtk::Window {
    public:
        Play();
        void update();
        void keepUpdating();
        void backgroundUpdate();
        void update_text_view();
        bool file_exists(const char * fileName);
        std::string openBoardFile(const std::string& board);
    private:
        Box rootBox;
        Paned mainSplit;
        Paned rightSplit;
        Box leftControls;
        ScrolledWindow boardScroll;
        ScrolledWindow logScroll;
        TextView boardView;
        TextView logView;
        CheckButton autoScrollToggle;
        Button clearLogButton;
        HeaderBar bar;
		Button enter;
        Button plus;
        Button minus;
		RadioButtonGroup yesOrNoRadio;
  		RadioButton radioYes;
  		RadioButton radioNo;
  		Entry numBox;
        Label responseLabel;
  		bool takeInput;
  		std::string response;
        std::string boardText;
  		Dispatcher dispatcher;
};

#endif
