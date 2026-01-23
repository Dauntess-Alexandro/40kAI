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
    void update_text_view();
  private:
    std::string response;
    std::string boardText;
    bool textModeActive;

    HeaderBar bar;

    Gtk::Box rootBox;
    Gtk::Box topRow;
    Gtk::Box rightSidebar;
    Gtk::Box statusBox;
    Gtk::Box legendBox;
    Gtk::Box statusBarBox;
    Gtk::Box logBox;
    Gtk::Box logButtonsRow;
    Gtk::Box logButtonsLeft;
    Gtk::Box logButtonsRight;

    Gtk::Frame statusFrame;
    Gtk::Frame legendFrame;
    Gtk::Frame statusBarFrame;
    Gtk::Frame logFrame;

    Gtk::ScrolledWindow boardScroll;
    Gtk::Stack boardStack;
    Gtk::TextView boardView;
    Gtk::Image pictureBox;

    Gtk::Label statusSummaryLabel;
    Gtk::Label statusVpCpLabel;

    Gtk::Label legendModelLabel;
    Gtk::Label legendPlayerLabel;
    Gtk::Label legendObjectiveLabel;

    Gtk::Label statusLinePrimary;
    Gtk::Label statusLineSecondary;

    Gtk::ScrolledWindow logScroll;
    Gtk::TextView logView;
    Gtk::Button clearLogButton;
    Gtk::Button copyLogButton;
    Gtk::CheckButton autoScrollToggle;

    Glib::Dispatcher dispatcher;
};

#endif
