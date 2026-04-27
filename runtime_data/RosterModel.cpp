#include "include/RosterModel.h"

#include <algorithm>
#include <fstream>
#include <unordered_set>

namespace {
int g_nextInstanceId = 1;

bool isNumericString(const std::string& value) {
  if (value.empty()) {
    return false;
  }
  for (char c : value) {
    if (c < '0' || c > '9') {
      return false;
    }
  }
  return true;
}

int parseCountValue(const nlohmann::json& value) {
  if (value.is_number_integer()) {
    return value.get<int>();
  }
  if (value.is_string()) {
    try {
      return std::stoi(value.get<std::string>());
    } catch (...) {
      return 0;
    }
  }
  return 0;
}
}  // namespace

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
  // NOTE: Do not merge same-name entries; each roster row is a separate unit instance.
  rosterUnits.push_back({name, faction.empty() ? rosterFaction : faction, countToAdd, generateInstanceId()});
}

void RosterModel::removeUnit(size_t index) {
  if (index >= rosterUnits.size()) {
    return;
  }
  rosterUnits.erase(rosterUnits.begin() + static_cast<long>(index));
}

void RosterModel::removeUnitByInstanceId(const std::string& instanceId) {
  auto it = std::find_if(rosterUnits.begin(), rosterUnits.end(),
                         [&](const RosterEntry& entry) { return entry.instanceId == instanceId; });
  if (it == rosterUnits.end()) {
    return;
  }
  rosterUnits.erase(it);
}

void RosterModel::clear() {
  rosterUnits.clear();
}

std::vector<RosterEntry> RosterModel::expandedUnits() const {
  return rosterUnits;
}

nlohmann::json RosterModel::toJson() const {
  nlohmann::json j;
  j["faction"] = rosterFaction;
  j["units"] = nlohmann::json::array();
  for (const auto& entry : rosterUnits) {
    j["units"].push_back({
        {"name", entry.name},
        {"faction", entry.faction},
        {"models_count", entry.modelsCount},
        {"instance_id", entry.instanceId},
    });
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
  std::unordered_set<std::string> seenIds;
  int maxNumericId = 0;
  auto registerInstanceId = [&](const std::string& candidate) -> std::string {
    if (candidate.empty() || seenIds.count(candidate) > 0) {
      std::string generated = generateInstanceId();
      seenIds.insert(generated);
      return generated;
    }
    seenIds.insert(candidate);
    if (isNumericString(candidate)) {
      maxNumericId = std::max(maxNumericId, std::stoi(candidate));
    }
    return candidate;
  };

  if (data.contains("units") && data.at("units").is_array()) {
    for (const auto& item : data.at("units")) {
      if (!item.is_object()) {
        continue;
      }
      if (!item.contains("name") || !item.at("name").is_string()) {
        continue;
      }
      int count = 0;
      if (item.contains("models_count")) {
        count = parseCountValue(item.at("models_count"));
      } else if (item.contains("count")) {
        count = parseCountValue(item.at("count"));
      }
      if (count <= 0) {
        continue;
      }
      std::string faction;
      if (item.contains("faction") && item.at("faction").is_string()) {
        faction = item.at("faction").get<std::string>();
      }
      if (faction.empty()) {
        faction = loadedFaction;
      }
      std::string instanceId;
      if (item.contains("instance_id") && item.at("instance_id").is_string()) {
        instanceId = item.at("instance_id").get<std::string>();
      }
      instanceId = registerInstanceId(instanceId);
      loadedUnits.push_back({item.at("name").get<std::string>(), faction, count, instanceId});
    }
  } else if (data.contains("units") && data.at("units").is_object()) {
    for (auto it = data.at("units").begin(); it != data.at("units").end(); ++it) {
      if (!it.key().empty()) {
        int count = parseCountValue(it.value());
        if (count <= 0) {
          continue;
        }
        std::string instanceId = registerInstanceId("");
        loadedUnits.push_back({it.key(), loadedFaction, count, instanceId});
      }
    }
  }

  rosterFaction = loadedFaction;
  rosterUnits = std::move(loadedUnits);
  if (maxNumericId >= g_nextInstanceId) {
    g_nextInstanceId = maxNumericId + 1;
  }
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

std::string RosterModel::generateInstanceId() {
  return std::to_string(g_nextInstanceId++);
}
