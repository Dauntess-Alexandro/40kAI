#pragma once

#include <QString>

struct RosterEntry {
    QString name;
    QString faction;
    int modelsCount = 0;
    QString instanceId;
};
