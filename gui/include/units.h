#ifndef UNITS_H
#define UNITS_H

#include <iostream>
#include <gtkmm.h>
#include <cstdlib>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <thread>
#include <chrono>
#include <filesystem>
#include "RosterModel.h"

using namespace Glib;
using namespace Gtk;

class Units : public Gtk::Window {
  public : 
    explicit Units(RosterModel* rosterModel);
    void loadAvailableUnits();
    void refreshRosterView();
    void addSelectedUnit();
    void removeSelectedUnit();
    void clearRoster();
  private:
    class AvailableColumns : public Gtk::TreeModel::ColumnRecord {
      public:
        AvailableColumns() { add(name); add(faction); add(defaultCount); }
        Gtk::TreeModelColumn<Glib::ustring> name;
        Gtk::TreeModelColumn<Glib::ustring> faction;
        Gtk::TreeModelColumn<int> defaultCount;
    };

    class RosterColumns : public Gtk::TreeModel::ColumnRecord {
      public:
        RosterColumns() { add(display); add(name); add(modelsCount); }
        Gtk::TreeModelColumn<Glib::ustring> display;
        Gtk::TreeModelColumn<Glib::ustring> name;
        Gtk::TreeModelColumn<int> modelsCount;
    };

    std::string formatRosterDisplay(const std::string& name, int modelsCount) const;
    void persistRoster();

    RosterModel* rosterModel;
    AvailableColumns availableColumns;
    RosterColumns rosterColumns;
    Glib::RefPtr<Gtk::ListStore> availableStore;
    Glib::RefPtr<Gtk::ListStore> rosterStore;
    Gtk::TreeView availableView;
    Gtk::TreeView rosterView;
    Gtk::ScrolledWindow availableScroll;
    Gtk::ScrolledWindow rosterScroll;
    Gtk::Box mainBox{Gtk::ORIENTATION_HORIZONTAL, 12};
    Gtk::Box availableBox{Gtk::ORIENTATION_VERTICAL, 6};
    Gtk::Box rosterBox{Gtk::ORIENTATION_VERTICAL, 6};
    Gtk::Box buttonBox{Gtk::ORIENTATION_VERTICAL, 6};
    Gtk::Label availableLabel;
    Gtk::Label rosterLabel;
    Gtk::Button addButton;
    Gtk::Button removeButton;
    Gtk::Button clearButton;
    HeaderBar bar;
};

#endif
