#include "include/LastRoster.h"

#include <filesystem>
#include <fstream>
#include <cstdlib>
#include <nlohmann/json.hpp>

namespace fs = std::filesystem;
using json = nlohmann::json;

namespace {
constexpr int kRosterVersion = 1;

json rosterEntryToJson(const RosterEntry& entry) {
  json item;
  item["name"] = entry.name;
  if (!entry.faction.empty()) {
    item["faction"] = entry.faction;
  }
  item["models_count"] = entry.modelsCount;
  if (!entry.instanceId.empty()) {
    item["instance_id"] = entry.instanceId;
  }
  return item;
}

std::vector<RosterEntry> parseRosterArray(const json& value, const std::string& fallbackFaction) {
  std::vector<RosterEntry> entries;
  if (!value.is_array()) {
    return entries;
  }
  for (const auto& item : value) {
    RosterEntry entry;
    if (item.is_string()) {
      entry.name = item.get<std::string>();
      entry.faction = fallbackFaction;
      entry.modelsCount = 1;
      entry.instanceId = RosterModel::generateInstanceId();
      entries.push_back(entry);
      continue;
    }
    if (!item.is_object()) {
      continue;
    }
    if (!item.contains("name") || !item.at("name").is_string()) {
      continue;
    }
    entry.name = item.at("name").get<std::string>();
    entry.faction = fallbackFaction;
    if (item.contains("faction") && item.at("faction").is_string()) {
      entry.faction = item.at("faction").get<std::string>();
    }
    entry.modelsCount = 1;
    if (item.contains("models_count") && item.at("models_count").is_number_integer()) {
      entry.modelsCount = item.at("models_count").get<int>();
    }
    if (item.contains("instance_id") && item.at("instance_id").is_string()) {
      entry.instanceId = item.at("instance_id").get<std::string>();
    }
    if (entry.instanceId.empty()) {
      entry.instanceId = RosterModel::generateInstanceId();
    }
    entries.push_back(entry);
  }
  return entries;
}

json entriesToJson(const std::vector<RosterEntry>& entries) {
  json array = json::array();
  for (const auto& entry : entries) {
    array.push_back(rosterEntryToJson(entry));
  }
  return array;
}
}  // namespace

std::string get_config_dir() {
  const char* xdgConfig = std::getenv("XDG_CONFIG_HOME");
  fs::path basePath;
  if (xdgConfig && *xdgConfig) {
    basePath = fs::path(xdgConfig);
  } else {
    const char* home = std::getenv("HOME");
    if (home && *home) {
      basePath = fs::path(home) / ".config";
    } else {
      basePath = fs::current_path();
    }
  }
  fs::path configPath = basePath / "40kai";
  std::error_code error;
  fs::create_directories(configPath, error);
  return configPath.string();
}

std::string get_last_roster_path() {
  fs::path path = fs::path(get_config_dir()) / "last_roster.json";
  return path.string();
}

bool save_last_roster(const RosterModel& playerRoster, const std::vector<RosterEntry>& modelRoster) {
  json data;
  data["version"] = kRosterVersion;
  data["player_faction"] = playerRoster.faction();
  data["player"] = entriesToJson(playerRoster.units());
  data["model"] = entriesToJson(modelRoster);
  fs::path path(get_last_roster_path());
  std::error_code error;
  fs::create_directories(path.parent_path(), error);
  std::ofstream out(path);
  if (!out) {
    return false;
  }
  out << data.dump(2);
  return true;
}

LastRosterLoadResult load_last_roster(RosterModel& playerRoster,
                                      std::vector<RosterEntry>& modelRoster,
                                      std::string* errorMessage) {
  fs::path path(get_last_roster_path());
  if (!fs::exists(path)) {
    if (errorMessage) {
      *errorMessage = "not_found";
    }
    return LastRosterLoadResult::kNotFound;
  }
  std::ifstream infile(path);
  if (!infile) {
    if (errorMessage) {
      *errorMessage = "open_failed";
    }
    return LastRosterLoadResult::kParseError;
  }
  json data;
  try {
    infile >> data;
  } catch (...) {
    if (errorMessage) {
      *errorMessage = "parse_failed";
    }
    return LastRosterLoadResult::kParseError;
  }

  if (data.is_object() && data.contains("units")) {
    if (!playerRoster.fromJson(data)) {
      if (errorMessage) {
        *errorMessage = "legacy_parse_failed";
      }
      return LastRosterLoadResult::kParseError;
    }
    modelRoster.clear();
    return LastRosterLoadResult::kLoaded;
  }

  if (!data.is_object()) {
    if (errorMessage) {
      *errorMessage = "invalid_format";
    }
    return LastRosterLoadResult::kParseError;
  }

  if (data.contains("version") && data.at("version").is_number_integer()) {
    int version = data.at("version").get<int>();
    if (version != kRosterVersion) {
      if (errorMessage) {
        *errorMessage = "unsupported_version";
      }
      return LastRosterLoadResult::kParseError;
    }
  }

  std::string playerFaction;
  if (data.contains("player_faction") && data.at("player_faction").is_string()) {
    playerFaction = data.at("player_faction").get<std::string>();
  }

  std::vector<RosterEntry> playerEntries;
  if (data.contains("player")) {
    playerEntries = parseRosterArray(data.at("player"), playerFaction);
  }
  std::vector<RosterEntry> modelEntries;
  if (data.contains("model")) {
    modelEntries = parseRosterArray(data.at("model"), playerFaction);
  }

  json playerJson;
  playerJson["faction"] = playerFaction;
  playerJson["units"] = json::array();
  for (const auto& entry : playerEntries) {
    playerJson["units"].push_back(rosterEntryToJson(entry));
  }
  playerRoster.fromJson(playerJson);
  modelRoster = std::move(modelEntries);
  return LastRosterLoadResult::kLoaded;
}
