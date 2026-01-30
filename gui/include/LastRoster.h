#ifndef LAST_ROSTER_H
#define LAST_ROSTER_H

#include <string>
#include <vector>
#include "RosterModel.h"

enum class LastRosterLoadResult {
  kLoaded,
  kNotFound,
  kParseError,
};

std::string get_config_dir();
std::string get_last_roster_path();
bool save_last_roster(const RosterModel& playerRoster, const std::vector<RosterEntry>& modelRoster);
LastRosterLoadResult load_last_roster(RosterModel& playerRoster,
                                      std::vector<RosterEntry>& modelRoster,
                                      std::string* errorMessage);

#endif
