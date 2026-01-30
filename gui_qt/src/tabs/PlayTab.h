#pragma once

#include <QWidget>

#include "util/ProcessRunner.h"
#include "util/RosterStore.h"
#include "util/SettingsStore.h"

class QLineEdit;
class QPlainTextEdit;

class PlayTab : public QWidget {
    Q_OBJECT
public:
    explicit PlayTab(SettingsStore* settings, RosterStore* roster, QWidget* parent = nullptr);

signals:
    void statusMessage(const QString& message);
    void activeCheckpointChanged(const QString& message);

private slots:
    void browseCheckpoint();
    void useLatestCheckpoint();
    void openCheckpointsFolder();
    void playInTerminal();
    void playInGui();
    void handleOutputLine(const QString& line);
    void handleFinished(int exitCode);

private:
    QString currentCheckpoint() const;
    bool launchTerminalCommand(const QString& command, const QStringList& args, const QMap<QString, QString>& env);
    void appendLogLine(const QString& line);

    SettingsStore* settingsStore = nullptr;
    RosterStore* rosterStore = nullptr;
    ProcessRunner runner;

    QLineEdit* checkpointEdit = nullptr;
    QPlainTextEdit* logView = nullptr;
};
