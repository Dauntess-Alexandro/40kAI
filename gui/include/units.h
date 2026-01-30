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
#include <functional>
#include "RosterModel.h"

using namespace Glib;
using namespace Gtk;

class Units : public Gtk::Window {
  public : 
    Units(RosterModel* playerRosterModel,
          std::vector<RosterEntry>* modelUnits,
          std::function<void()> onRosterUpdated);
    void loadAvailableUnits();
    void refreshRosterViews();
    void addSelectedToPlayer();
    void addSelectedToModel();
    void removeSelectedFromActiveRoster();
    void clearAllRosters();
    void clearPlayerRoster();
    void clearModelRoster();
    void mirrorPlayerToModel();
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
        RosterColumns() { add(display); add(name); add(modelsCount); add(instanceId); }
        Gtk::TreeModelColumn<Glib::ustring> display;
        Gtk::TreeModelColumn<Glib::ustring> name;
        Gtk::TreeModelColumn<int> modelsCount;
        Gtk::TreeModelColumn<Glib::ustring> instanceId;
    };

    struct AvailableUnit {
        std::string name;
        std::string faction;
        int defaultCount;
    };

    std::string formatRosterDisplay(const std::string& name, int modelsCount) const;
    void persistPlayerRoster();
    bool getSelectedAvailableUnit(AvailableUnit& unit) const;
    void refreshRosterView(const std::vector<RosterEntry>& entries,
                           const Glib::RefPtr<Gtk::ListStore>& store);
    void setStatusMessage(const std::string& message);
    void notifyRosterUpdated();
    void removeModelUnitByInstanceId(const std::string& instanceId, size_t fallbackIndex);

    RosterModel* playerRosterModel;
    std::vector<RosterEntry>* modelUnits;
    std::function<void()> onRosterUpdated;
    AvailableColumns availableColumns;
    RosterColumns rosterColumns;
    Glib::RefPtr<Gtk::ListStore> availableStore;
    Glib::RefPtr<Gtk::ListStore> playerRosterStore;
    Glib::RefPtr<Gtk::ListStore> modelRosterStore;
    Gtk::TreeView availableView;
    Gtk::TreeView playerRosterView;
    Gtk::TreeView modelRosterView;
    Gtk::ScrolledWindow availableScroll;
    Gtk::ScrolledWindow playerRosterScroll;
    Gtk::ScrolledWindow modelRosterScroll;
    Gtk::Box rootBox{Gtk::ORIENTATION_VERTICAL, 8};
    Gtk::Box mainBox{Gtk::ORIENTATION_HORIZONTAL, 12};
    Gtk::Box rosterBox{Gtk::ORIENTATION_VERTICAL, 8};
    Gtk::Box buttonBox{Gtk::ORIENTATION_VERTICAL, 6};
    Gtk::Box clearButtonBox{Gtk::ORIENTATION_HORIZONTAL, 6};
    Gtk::Frame availableFrame;
    Gtk::Frame playerRosterFrame;
    Gtk::Frame modelRosterFrame;
    Gtk::Label statusLabel;
    Gtk::Button addPlayerButton;
    Gtk::Button addModelButton;
    Gtk::Button removeButton;
    Gtk::Button clearAllButton;
    Gtk::Button clearPlayerButton;
    Gtk::Button clearModelButton;
    Gtk::Button mirrorButton;
    HeaderBar bar;
};

#endif
