#include <iostream>
#include <gtkmm.h>
#include <cstdlib>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <unordered_map>
#include <filesystem>
#include <optional>
#include <nlohmann/json.hpp>
#include "include/units.h"

using namespace Glib;
using namespace Gtk;
using json = nlohmann::json;
namespace fs = std::filesystem;

namespace {
std::optional<fs::path> findUnitDataPath() {
  fs::path current = fs::current_path();
  for (int depth = 0; depth < 6; ++depth) {
    fs::path candidate = current / "gym_mod" / "gym_mod" / "engine" / "unitData.json";
    if (fs::exists(candidate)) {
      return candidate;
    }
    if (!current.has_parent_path()) {
      break;
    }
    current = current.parent_path();
  }
  return std::nullopt;
}
}  // namespace

void Units::loadAvailableUnits() {
  availableStore->clear();
  auto unitDataPath = findUnitDataPath();
  if (!unitDataPath) {
    return;
  }
  std::ifstream infile(*unitDataPath);
  if (!infile) {
    return;
  }
  json j;
  infile >> j;

  if (!j.contains("UnitData") || !j.at("UnitData").is_array()) {
    return;
  }

  for (const auto& unit : j.at("UnitData")) {
    if (!unit.contains("Army") || !unit.contains("Name")) {
      continue;
    }
    std::string army = unit.at("Army").get<std::string>();
    std::string name = unit.at("Name").get<std::string>();
    int defaultCount = 1;
    if (unit.contains("#OfModels") && unit.at("#OfModels").is_number_integer()) {
      defaultCount = unit.at("#OfModels").get<int>();
    }
    auto row = *(availableStore->append());
    row[availableColumns.name] = name;
    row[availableColumns.faction] = army;
    row[availableColumns.defaultCount] = defaultCount;
  }
}

std::string Units::formatRosterDisplay(const std::string& name, int modelsCount) const {
  return "(Unit) " + name + " (x" + std::to_string(modelsCount) + " Models)";
}

void Units::persistRoster() {
  if (!rosterModel) {
    return;
  }
  rosterModel->saveToFile(RosterModel::defaultRosterPath());
}

void Units::refreshRosterView() {
  if (!rosterStore || !rosterModel) {
    return;
  }
  rosterStore->clear();
  std::unordered_map<std::string, int> totalByName;
  for (const auto& entry : rosterModel->units()) {
    totalByName[entry.name] += 1;
  }
  std::unordered_map<std::string, int> seenByName;
  for (const auto& entry : rosterModel->units()) {
    auto row = *(rosterStore->append());
    row[rosterColumns.name] = entry.name;
    row[rosterColumns.modelsCount] = entry.modelsCount;
    row[rosterColumns.instanceId] = entry.instanceId;
    int ordinal = ++seenByName[entry.name];
    std::string displayName = entry.name;
    if (totalByName[entry.name] > 1) {
      displayName += " #" + std::to_string(ordinal);
    }
    row[rosterColumns.display] = formatRosterDisplay(displayName, entry.modelsCount);
  }
}

void Units::addSelectedUnit() {
  if (!rosterModel) {
    return;
  }
  auto selection = availableView.get_selection();
  if (!selection) {
    return;
  }
  auto iter = selection->get_selected();
  if (!iter) {
    return;
  }
  auto row = *iter;
  Glib::ustring nameValue = row[availableColumns.name];
  Glib::ustring factionValue = row[availableColumns.faction];
  std::string name = nameValue.raw();
  std::string faction = factionValue.raw();
  int defaultCount = row[availableColumns.defaultCount];
  rosterModel->addUnit(name, defaultCount, faction);
  refreshRosterView();
  persistRoster();
}

void Units::removeSelectedUnit() {
  if (!rosterModel) {
    return;
  }
  auto selection = rosterView.get_selection();
  if (!selection) {
    return;
  }
  auto iter = selection->get_selected();
  if (!iter) {
    return;
  }
  auto path = rosterStore->get_path(iter);
  if (path.empty()) {
    return;
  }
  Glib::ustring instanceValue = (*iter)[rosterColumns.instanceId];
  std::string instanceId = instanceValue.raw();
  if (!instanceId.empty()) {
    rosterModel->removeUnitByInstanceId(instanceId);
  } else {
    rosterModel->removeUnit(static_cast<size_t>(path.front()));
  }
  refreshRosterView();
  persistRoster();
}

void Units::clearRoster() {
  if (!rosterModel) {
    return;
  }
  rosterModel->clear();
  refreshRosterView();
  persistRoster();
}

Units::Units(RosterModel* rosterModel) : rosterModel(rosterModel) {
  bar.set_show_close_button(true);
  set_titlebar(bar);
  bar.set_title("Army Viewer");

  add(mainBox);

  availableLabel.set_text("Available Units");
  rosterLabel.set_text("Roster");

  availableStore = Gtk::ListStore::create(availableColumns);
  rosterStore = Gtk::ListStore::create(rosterColumns);
  availableView.set_model(availableStore);
  rosterView.set_model(rosterStore);
  availableView.append_column("Faction", availableColumns.faction);
  availableView.append_column("Unit", availableColumns.name);
  rosterView.append_column("Selected", rosterColumns.display);
  availableView.set_headers_visible(true);
  rosterView.set_headers_visible(false);

  availableScroll.add(availableView);
  availableScroll.set_policy(Gtk::POLICY_AUTOMATIC, Gtk::POLICY_AUTOMATIC);
  availableScroll.set_min_content_width(260);
  rosterScroll.add(rosterView);
  rosterScroll.set_policy(Gtk::POLICY_AUTOMATIC, Gtk::POLICY_AUTOMATIC);
  rosterScroll.set_min_content_width(220);

  addButton.set_label("Add →");
  removeButton.set_label("Remove");
  clearButton.set_label("Clear");

  addButton.signal_button_release_event().connect([&](GdkEventButton*) {
    addSelectedUnit();
    return true;
  });
  removeButton.signal_button_release_event().connect([&](GdkEventButton*) {
    removeSelectedUnit();
    return true;
  });
  clearButton.signal_button_release_event().connect([&](GdkEventButton*) {
    clearRoster();
    return true;
  });

  availableView.signal_row_activated().connect([&](const Gtk::TreeModel::Path&, Gtk::TreeViewColumn*) {
    addSelectedUnit();
  });

  availableBox.pack_start(availableLabel, Gtk::PACK_SHRINK);
  availableBox.pack_start(availableScroll, Gtk::PACK_EXPAND_WIDGET);
  rosterBox.pack_start(rosterLabel, Gtk::PACK_SHRINK);
  rosterBox.pack_start(rosterScroll, Gtk::PACK_EXPAND_WIDGET);

  buttonBox.pack_start(addButton, Gtk::PACK_SHRINK);
  buttonBox.pack_start(removeButton, Gtk::PACK_SHRINK);
  buttonBox.pack_start(clearButton, Gtk::PACK_SHRINK);

  mainBox.pack_start(availableBox, Gtk::PACK_EXPAND_WIDGET);
  mainBox.pack_start(buttonBox, Gtk::PACK_SHRINK);
  mainBox.pack_start(rosterBox, Gtk::PACK_EXPAND_WIDGET);

  loadAvailableUnits();
  refreshRosterView();

  resize(700, 500);
  show_all();
}
