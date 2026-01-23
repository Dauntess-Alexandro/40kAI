#include "include/RosterModel.h"

#include <algorithm>
#include <fstream>
#include <iostream>

void RosterModel::setFaction(const std::string& faction) {
  rosterFaction = faction;
}

const std::string& RosterModel::faction() const {
  return rosterFaction;
}

const std::vector<RosterEntry>& RosterModel::units() const {
  return rosterUnits;
}

bool RosterModel::empty() const {
  return rosterUnits.empty();
}

void RosterModel::addUnit(const std::string& name, int countDefault, const std::string& faction) {
  if (!faction.empty()) {
    rosterFaction = faction;
  }

  int countToAdd = countDefault > 0 ? countDefault : 1;
  auto it = std::find_if(rosterUnits.begin(), rosterUnits.end(),
                         [&](const RosterEntry& entry) { return entry.name == name; });
  if (it != rosterUnits.end()) {
    it->count += countToAdd;
    return;
  }

  rosterUnits.push_back({name, countToAdd});
}

void RosterModel::removeUnit(size_t index) {
  if (index >= rosterUnits.size()) {
    return;
  }
  rosterUnits.erase(rosterUnits.begin() + static_cast<long>(index));
}

void RosterModel::clear() {
  rosterUnits.clear();
}

std::vector<std::string> RosterModel::expandedUnits() const {
  std::vector<std::string> expanded;
  for (const auto& entry : rosterUnits) {
    constexpr int kMaxUnitsPerEntry = 10;
    if (entry.count > kMaxUnitsPerEntry) {
      std::cerr << "[RosterModel] Warning: entry '" << entry.name
                << "' count=" << entry.count
                << " looks like a model count; limiting to a single unit."
                << std::endl;
    }
    expanded.push_back(entry.name);
  }
  return expanded;
}

nlohmann::json RosterModel::toJson() const {
  nlohmann::json j;
  j["faction"] = rosterFaction;
  j["units"] = nlohmann::json::array();
  for (const auto& entry : rosterUnits) {
    j["units"].push_back({{"name", entry.name}, {"count", entry.count}});
  }
  return j;
}

bool RosterModel::fromJson(const nlohmann::json& data) {
  if (!data.is_object()) {
    return false;
  }
  std::string loadedFaction;
  if (data.contains("faction") && data.at("faction").is_string()) {
    loadedFaction = data.at("faction").get<std::string>();
  }

  std::vector<RosterEntry> loadedUnits;
  if (data.contains("units") && data.at("units").is_array()) {
    for (const auto& item : data.at("units")) {
      if (!item.is_object()) {
        continue;
      }
      if (!item.contains("name") || !item.contains("count")) {
        continue;
      }
      if (!item.at("name").is_string()) {
        continue;
      }
      int count = 0;
      if (item.at("count").is_number_integer()) {
        count = item.at("count").get<int>();
      } else if (item.at("count").is_string()) {
        try {
          count = std::stoi(item.at("count").get<std::string>());
        } catch (...) {
          count = 0;
        }
      }
      if (count <= 0) {
        continue;
      }
      loadedUnits.push_back({item.at("name").get<std::string>(), count});
    }
  }

  rosterFaction = loadedFaction;
  rosterUnits = std::move(loadedUnits);
  return true;
}

bool RosterModel::loadFromFile(const std::filesystem::path& path) {
  if (!std::filesystem::exists(path)) {
    return false;
  }
  std::ifstream infile(path);
  if (!infile) {
    return false;
  }
  nlohmann::json j;
  try {
    infile >> j;
  } catch (...) {
    return false;
  }
  return fromJson(j);
}

bool RosterModel::saveToFile(const std::filesystem::path& path) const {
  std::error_code error;
  std::filesystem::create_directories(path.parent_path(), error);
  std::ofstream outfile(path);
  if (!outfile) {
    return false;
  }
  outfile << toJson().dump(2);
  return true;
}

std::filesystem::path RosterModel::defaultRosterPath() {
  const char* xdgData = std::getenv("XDG_DATA_HOME");
  if (xdgData && *xdgData) {
    return std::filesystem::path(xdgData) / "40kAI" / "last_roster.json";
  }
  const char* home = std::getenv("HOME");
  if (home && *home) {
    return std::filesystem::path(home) / ".local" / "share" / "40kAI" / "last_roster.json";
  }
  return std::filesystem::current_path() / "last_roster.json";
}
