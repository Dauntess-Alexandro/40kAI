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
    bool onTimeout();
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
    Box statusContentBox;
    Box logBox;
    Box logControls;
    ScrolledWindow boardScroll;
    TextView boardView;
    Stack boardStack;
    Label statusLabel;
    Label statusTurnLabel;
    Label statusPhaseLabel;
    Label statusActiveLabel;
    Label statusVpLabel;
    Label statusCpLabel;
    Label statusBarLabel;
    Label legendLabel;
    Separator statusSeparatorTop;
    Separator statusSeparatorBottom;
    ScrolledWindow logScroll;
    TextView logView;
    Button clearLogButton;
    Button copyLogButton;
    ToggleButton autoScrollToggle;
    bool textModeEnabled;
    std::string lastLogLine;
    std::string logText;
    sigc::connection updateConnection;
    HeaderBar bar;
    Button changeMode;
    Image pictureBox;
};

#endif
