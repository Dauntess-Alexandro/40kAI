#ifndef POPOP_H
#define POPOP_H

#include <iostream>
#include <gtkmm.h>
#include <cstdlib>
#include <string>
#include <stdlib.h>

using namespace Glib;
using namespace Gtk;

class PopUp : public Gtk::Window {
  public : 
    PopUp(bool textMode);
    ~PopUp();
    std::string openFile(std::string board);
    bool isNum(char num);
    void update();
    void backgroundUpdate(bool textMode);
    void keepUpdating();
    void keepUpdatingElecBoogaloo();
    void updateImage();
  private:
    Box rootBox;
    Paned mainSplit;
    Box boardArea;
    Frame boardFrame;
    ScrolledWindow boardScroll;
    Fixed boardFixed;
    Frame statusFrame;
    Box statusPanel;
    Label turnRoundLabel;
    Label phaseLabel;
    Label activeSideLabel;
    Label vpLabel;
    Label cpLabel;
    Label legendLabel;
    Frame logFrame;
    ScrolledWindow logScroll;
    TextView logView;
    RefPtr<TextBuffer> logBuffer;
    Label contents;
    std::string lastLogMessage;
    HeaderBar bar;
    Button changeMode;
    Image pictureBox;
};

#endif
