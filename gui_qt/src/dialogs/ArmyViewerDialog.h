#pragma once

#include <QDialog>
#include <QVector>

#include "util/RosterStore.h"
#include "util/SettingsStore.h"

class QTableWidget;
class QListWidget;
class QLabel;

class ArmyViewerDialog : public QDialog {
    Q_OBJECT
public:
    explicit ArmyViewerDialog(SettingsStore* settings, RosterStore* roster, QWidget* parent = nullptr);

private slots:
    void addToPlayer();
    void addToModel();
    void removeSelected();
    void clearRosters();
    void mirrorPlayerToModel();
    void applyChanges();

private:
    struct AvailableUnit {
        QString name;
        QString faction;
        int defaultCount = 1;
    };

    void loadAvailableUnits();
    void rebuildRosterList(QListWidget* list, const QVector<RosterEntry>& roster) const;
    AvailableUnit selectedUnit() const;

    SettingsStore* settingsStore = nullptr;
    RosterStore* rosterStore = nullptr;

    QVector<AvailableUnit> availableUnits;
    QVector<RosterEntry> playerRoster;
    QVector<RosterEntry> modelRoster;

    QTableWidget* availableTable = nullptr;
    QListWidget* playerList = nullptr;
    QListWidget* modelList = nullptr;
    QLabel* statusLabel = nullptr;
};
