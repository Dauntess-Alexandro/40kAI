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
    std::string openStatusFile(const std::string& statusFile);
    std::string openLogFile(const std::string& logFile);
    bool isNum(char num);
    void update();
    void backgroundUpdate(bool textMode);
    void keepUpdating();
    void keepUpdatingElecBoogaloo();
    void updateImage();
    void applyStyles();
  private:
    Box rootBox;
    Paned mainSplit;
    Box sideBox;
    Frame boardFrame;
    Frame statusFrame;
    Frame legendFrame;
    Frame statusBarFrame;
    Frame logFrame;
    Box statusBarBox;
    Box logBox;
    Box logControls;
    ScrolledWindow boardScroll;
    TextView boardView;
    Stack boardStack;
    Label statusLabel;
    Label statusBarLabel;
    Label legendLabel;
    ScrolledWindow logScroll;
    TextView logView;
    Button clearLogButton;
    Button copyLogButton;
    ToggleButton autoScrollToggle;
    bool textModeEnabled;
    std::string lastLogLine;
    std::string logText;
    HeaderBar bar;
    Button changeMode;
    Image pictureBox;
};

#endif
