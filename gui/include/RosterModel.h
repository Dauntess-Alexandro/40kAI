#ifndef ROSTER_MODEL_H
#define ROSTER_MODEL_H

#include <filesystem>
#include <string>
#include <vector>
#include <nlohmann/json.hpp>

struct RosterEntry {
  std::string name;
  int modelsCount;
};

class RosterModel {
  public:
    void setFaction(const std::string& faction);
    const std::string& faction() const;
    const std::vector<RosterEntry>& units() const;
    bool empty() const;
    void addUnit(const std::string& name, int countDefault, const std::string& faction = "");
    void removeUnit(size_t index);
    void clear();
    std::vector<RosterEntry> expandedUnits() const;
    nlohmann::json toJson() const;
    bool fromJson(const nlohmann::json& data);
    bool loadFromFile(const std::filesystem::path& path);
    bool saveToFile(const std::filesystem::path& path) const;
    static std::filesystem::path defaultRosterPath();

  private:
    std::string rosterFaction;
    std::vector<RosterEntry> rosterUnits;
};

#endif
