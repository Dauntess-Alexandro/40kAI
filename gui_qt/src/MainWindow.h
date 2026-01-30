#pragma once

#include <QMainWindow>

#include "util/SettingsStore.h"
#include "util/RosterStore.h"

class TrainTab;
class MetricsTab;
class PlayTab;
class SettingsTab;
class EvalTab;

class MainWindow : public QMainWindow {
    Q_OBJECT
public:
    explicit MainWindow(QWidget* parent = nullptr);

protected:
    void closeEvent(QCloseEvent* event) override;

private slots:
    void updateStatusMessage(const QString& message);
    void updateProgressMessage(const QString& message);
    void updateCheckpointMessage(const QString& message);
    void applyTheme(bool enabled);
    void handleRosterChanged();

private:
    void setupToolbar();
    void setupStatusBar();
    void loadSettings();
    void saveSettings();
    void resetLayout();
    void openLogsFolder();
    void copyDebugInfo();

    SettingsStore settingsStore;
    RosterStore rosterStore;

    TrainTab* trainTab = nullptr;
    MetricsTab* metricsTab = nullptr;
    PlayTab* playTab = nullptr;
    SettingsTab* settingsTab = nullptr;
    EvalTab* evalTab = nullptr;

    QLabel* statusLabel = nullptr;
    QLabel* progressLabel = nullptr;
    QLabel* pythonLabel = nullptr;
    QLabel* checkpointLabel = nullptr;
};
