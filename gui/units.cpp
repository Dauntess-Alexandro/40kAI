#include <iostream>
#include <gtkmm.h>
#include <cstdlib>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <unordered_map>
#include <nlohmann/json.hpp>
#include <algorithm>
#include <utility>
#include "include/units.h"

using namespace Glib;
using namespace Gtk;
using json = nlohmann::json;

void Units::loadAvailableUnits() {
  availableStore->clear();
  std::ifstream infile("../gym_mod/gym_mod/engine/unitData.json");
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

void Units::persistPlayerRoster() {
  if (!playerRosterModel) {
    return;
  }
  playerRosterModel->saveToFile(RosterModel::defaultRosterPath());
}

bool Units::getSelectedAvailableUnit(AvailableUnit& unit) const {
  auto selection = availableView.get_selection();
  if (!selection) {
    return false;
  }
  auto iter = selection->get_selected();
  if (!iter) {
    return false;
  }
  auto row = *iter;
  Glib::ustring nameValue = row[availableColumns.name];
  Glib::ustring factionValue = row[availableColumns.faction];
  unit.name = nameValue.raw();
  unit.faction = factionValue.raw();
  unit.defaultCount = row[availableColumns.defaultCount];
  return true;
}

void Units::refreshRosterView(const std::vector<RosterEntry>& entries,
                              const Glib::RefPtr<Gtk::ListStore>& store) {
  if (!store) {
    return;
  }
  store->clear();
  std::unordered_map<std::string, int> totalByName;
  for (const auto& entry : entries) {
    totalByName[entry.name] += 1;
  }
  std::unordered_map<std::string, int> seenByName;
  for (const auto& entry : entries) {
    auto row = *(store->append());
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

void Units::refreshRosterViews() {
  if (playerRosterModel) {
    refreshRosterView(playerRosterModel->units(), playerRosterStore);
  }
  if (modelUnits) {
    refreshRosterView(*modelUnits, modelRosterStore);
  }
}

void Units::setStatusMessage(const std::string& message) {
  statusLabel.set_text(message);
}

void Units::notifyRosterUpdated() {
  if (onRosterUpdated) {
    onRosterUpdated();
  }
}

void Units::addSelectedToPlayer() {
  if (!playerRosterModel) {
    return;
  }
  AvailableUnit unit;
  if (!getSelectedAvailableUnit(unit)) {
    setStatusMessage("Выберите юнит в списке доступных.");
    return;
  }
  playerRosterModel->addUnit(unit.name, unit.defaultCount, unit.faction);
  refreshRosterViews();
  persistPlayerRoster();
  notifyRosterUpdated();
  setStatusMessage("Юнит добавлен в ростер игрока.");
}

void Units::addSelectedToModel() {
  if (!modelUnits) {
    return;
  }
  AvailableUnit unit;
  if (!getSelectedAvailableUnit(unit)) {
    setStatusMessage("Выберите юнит в списке доступных.");
    return;
  }
  modelUnits->push_back({unit.name, unit.faction, unit.defaultCount, RosterModel::generateInstanceId()});
  refreshRosterViews();
  notifyRosterUpdated();
  setStatusMessage("Юнит добавлен в ростер модели.");
}

void Units::removeModelUnitByInstanceId(const std::string& instanceId, size_t fallbackIndex) {
  if (!modelUnits) {
    return;
  }
  if (!instanceId.empty()) {
    auto it = std::find_if(modelUnits->begin(), modelUnits->end(),
                           [&](const RosterEntry& entry) { return entry.instanceId == instanceId; });
    if (it != modelUnits->end()) {
      modelUnits->erase(it);
    }
    return;
  }
  if (fallbackIndex < modelUnits->size()) {
    modelUnits->erase(modelUnits->begin() + static_cast<long>(fallbackIndex));
  }
}

void Units::removeSelectedFromActiveRoster() {
  auto playerSelection = playerRosterView.get_selection();
  auto modelSelection = modelRosterView.get_selection();
  auto playerIter = playerSelection ? playerSelection->get_selected() : Gtk::TreeModel::iterator();
  if (playerIter && playerRosterModel) {
    auto path = playerRosterStore->get_path(playerIter);
    if (!path.empty()) {
      Glib::ustring instanceValue = (*playerIter)[rosterColumns.instanceId];
      std::string instanceId = instanceValue.raw();
      if (!instanceId.empty()) {
        playerRosterModel->removeUnitByInstanceId(instanceId);
      } else {
        playerRosterModel->removeUnit(static_cast<size_t>(path.front()));
      }
      refreshRosterViews();
      persistPlayerRoster();
      notifyRosterUpdated();
      setStatusMessage("Юнит удалён из ростера игрока.");
      return;
    }
  }

  auto modelIter = modelSelection ? modelSelection->get_selected() : Gtk::TreeModel::iterator();
  if (modelIter && modelUnits) {
    auto path = modelRosterStore->get_path(modelIter);
    if (!path.empty()) {
      Glib::ustring instanceValue = (*modelIter)[rosterColumns.instanceId];
      std::string instanceId = instanceValue.raw();
      removeModelUnitByInstanceId(instanceId, static_cast<size_t>(path.front()));
      refreshRosterViews();
      notifyRosterUpdated();
      setStatusMessage("Юнит удалён из ростера модели.");
      return;
    }
  }

  setStatusMessage("Сначала выберите юнит для удаления.");
}

void Units::clearPlayerRoster() {
  if (!playerRosterModel) {
    return;
  }
  playerRosterModel->clear();
  refreshRosterViews();
  persistPlayerRoster();
  notifyRosterUpdated();
  setStatusMessage("Ростер игрока очищен.");
}

void Units::clearModelRoster() {
  if (!modelUnits) {
    return;
  }
  modelUnits->clear();
  refreshRosterViews();
  notifyRosterUpdated();
  setStatusMessage("Ростер модели очищен.");
}

void Units::clearAllRosters() {
  if (playerRosterModel) {
    playerRosterModel->clear();
    persistPlayerRoster();
  }
  if (modelUnits) {
    modelUnits->clear();
  }
  refreshRosterViews();
  notifyRosterUpdated();
  setStatusMessage("Оба ростера очищены.");
}

void Units::mirrorPlayerToModel() {
  if (!playerRosterModel || !modelUnits) {
    return;
  }
  *modelUnits = playerRosterModel->expandedUnits();
  refreshRosterViews();
  notifyRosterUpdated();
  setStatusMessage("Ростер модели обновлён из ростера игрока.");
}

Units::Units(RosterModel* playerRosterModel,
             std::vector<RosterEntry>* modelUnits,
             std::function<void()> onRosterUpdated)
    : playerRosterModel(playerRosterModel),
      modelUnits(modelUnits),
      onRosterUpdated(std::move(onRosterUpdated)) {
  bar.set_show_close_button(true);
  set_titlebar(bar);
  bar.set_title("Army Viewer");

  add(rootBox);

  availableFrame.set_label("Available Units");
  playerRosterFrame.set_label("Player Roster");
  modelRosterFrame.set_label("Model Roster");

  availableStore = Gtk::ListStore::create(availableColumns);
  playerRosterStore = Gtk::ListStore::create(rosterColumns);
  modelRosterStore = Gtk::ListStore::create(rosterColumns);
  availableView.set_model(availableStore);
  playerRosterView.set_model(playerRosterStore);
  modelRosterView.set_model(modelRosterStore);
  availableView.append_column("Faction", availableColumns.faction);
  availableView.append_column("Unit", availableColumns.name);
  playerRosterView.append_column("Selected", rosterColumns.display);
  modelRosterView.append_column("Selected", rosterColumns.display);
  availableView.set_headers_visible(true);
  playerRosterView.set_headers_visible(false);
  modelRosterView.set_headers_visible(false);

  availableScroll.add(availableView);
  availableScroll.set_policy(Gtk::POLICY_AUTOMATIC, Gtk::POLICY_AUTOMATIC);
  availableScroll.set_min_content_width(260);
  playerRosterScroll.add(playerRosterView);
  playerRosterScroll.set_policy(Gtk::POLICY_AUTOMATIC, Gtk::POLICY_AUTOMATIC);
  playerRosterScroll.set_min_content_width(220);
  modelRosterScroll.add(modelRosterView);
  modelRosterScroll.set_policy(Gtk::POLICY_AUTOMATIC, Gtk::POLICY_AUTOMATIC);
  modelRosterScroll.set_min_content_width(220);

  addPlayerButton.set_label("Add → Player");
  addModelButton.set_label("Add → Model");
  removeButton.set_label("Remove");
  clearAllButton.set_label("Clear All");
  clearPlayerButton.set_label("Clear Player");
  clearModelButton.set_label("Clear Model");
  mirrorButton.set_label("Mirror");

  addPlayerButton.signal_button_release_event().connect([&](GdkEventButton*) {
    addSelectedToPlayer();
    return true;
  });
  addModelButton.signal_button_release_event().connect([&](GdkEventButton*) {
    addSelectedToModel();
    return true;
  });
  removeButton.signal_button_release_event().connect([&](GdkEventButton*) {
    removeSelectedFromActiveRoster();
    return true;
  });
  clearAllButton.signal_button_release_event().connect([&](GdkEventButton*) {
    clearAllRosters();
    return true;
  });
  clearPlayerButton.signal_button_release_event().connect([&](GdkEventButton*) {
    clearPlayerRoster();
    return true;
  });
  clearModelButton.signal_button_release_event().connect([&](GdkEventButton*) {
    clearModelRoster();
    return true;
  });
  mirrorButton.signal_button_release_event().connect([&](GdkEventButton*) {
    mirrorPlayerToModel();
    return true;
  });

  availableView.signal_row_activated().connect([&](const Gtk::TreeModel::Path&, Gtk::TreeViewColumn*) {
    addSelectedToPlayer();
  });

  auto playerSelection = playerRosterView.get_selection();
  if (playerSelection) {
    playerSelection->signal_changed().connect([&]() {
      auto modelSelection = modelRosterView.get_selection();
      if (modelSelection && playerSelection->get_selected()) {
        modelSelection->unselect_all();
      }
    });
  }
  auto modelSelection = modelRosterView.get_selection();
  if (modelSelection) {
    modelSelection->signal_changed().connect([&]() {
      auto playerSelectionLocal = playerRosterView.get_selection();
      if (playerSelectionLocal && modelSelection->get_selected()) {
        playerSelectionLocal->unselect_all();
      }
    });
  }

  availableFrame.add(availableScroll);
  playerRosterFrame.add(playerRosterScroll);
  modelRosterFrame.add(modelRosterScroll);

  clearButtonBox.pack_start(clearPlayerButton, Gtk::PACK_SHRINK);
  clearButtonBox.pack_start(clearModelButton, Gtk::PACK_SHRINK);

  buttonBox.pack_start(addPlayerButton, Gtk::PACK_SHRINK);
  buttonBox.pack_start(addModelButton, Gtk::PACK_SHRINK);
  buttonBox.pack_start(removeButton, Gtk::PACK_SHRINK);
  buttonBox.pack_start(clearAllButton, Gtk::PACK_SHRINK);
  buttonBox.pack_start(clearButtonBox, Gtk::PACK_SHRINK);
  buttonBox.pack_start(mirrorButton, Gtk::PACK_SHRINK);

  rosterBox.pack_start(playerRosterFrame, Gtk::PACK_EXPAND_WIDGET);
  rosterBox.pack_start(modelRosterFrame, Gtk::PACK_EXPAND_WIDGET);

  mainBox.pack_start(availableFrame, Gtk::PACK_EXPAND_WIDGET);
  mainBox.pack_start(buttonBox, Gtk::PACK_SHRINK);
  mainBox.pack_start(rosterBox, Gtk::PACK_EXPAND_WIDGET);

  rootBox.pack_start(mainBox, Gtk::PACK_EXPAND_WIDGET);
  rootBox.pack_start(statusLabel, Gtk::PACK_SHRINK);

  rootBox.set_margin_top(12);
  rootBox.set_margin_bottom(12);
  rootBox.set_margin_start(12);
  rootBox.set_margin_end(12);
  rootBox.set_hexpand(true);
  rootBox.set_vexpand(true);
  availableFrame.set_hexpand(true);
  playerRosterFrame.set_hexpand(true);
  modelRosterFrame.set_hexpand(true);
  buttonBox.set_valign(Gtk::ALIGN_START);
  statusLabel.set_xalign(0.0);

  loadAvailableUnits();
  refreshRosterViews();

  resize(700, 500);
  show_all();
}
