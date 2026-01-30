#pragma once

#include <QWidget>

#include "util/SettingsStore.h"

class QLineEdit;
class QCheckBox;

class SettingsTab : public QWidget {
    Q_OBJECT
public:
    explicit SettingsTab(SettingsStore* settings, QWidget* parent = nullptr);

signals:
    void statusMessage(const QString& message);
    void themeToggled(bool enabled);

private slots:
    void browsePython();
    void browseRepoRoot();
    void browseCheckpoints();
    void saveSettings();
    void toggleTheme(bool enabled);

private:
    SettingsStore* settingsStore = nullptr;

    QLineEdit* pythonEdit = nullptr;
    QLineEdit* repoEdit = nullptr;
    QLineEdit* checkpointsEdit = nullptr;
    QCheckBox* darkModeCheck = nullptr;
    QCheckBox* trainDebugCheck = nullptr;
    QCheckBox* fightReportCheck = nullptr;
};
