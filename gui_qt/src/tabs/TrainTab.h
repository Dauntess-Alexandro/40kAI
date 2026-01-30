#pragma once

#include <QWidget>
#include <QMap>

#include "util/ProcessRunner.h"
#include "util/RosterStore.h"
#include "util/SettingsStore.h"

class QLabel;
class QPlainTextEdit;
class QProgressBar;
class QSpinBox;
class QPushButton;

class TrainTab : public QWidget {
    Q_OBJECT
public:
    explicit TrainTab(SettingsStore* settings, RosterStore* roster, QWidget* parent = nullptr);

    void refreshRosterSummary();

signals:
    void statusMessage(const QString& message);
    void progressMessage(const QString& message);
    void activeCheckpointChanged(const QString& message);

private slots:
    void startTrain();
    void startTrain8x();
    void startSelfPlay();
    void openArmyViewer();
    void clearModelCache();
    void handleOutputLine(const QString& line);
    void handleProgress(int current, int total, double rate, int elapsedSec, int etaSec);
    void handleFinished(int exitCode);

private:
    bool prepareDataFile(QString* errorMessage);
    bool runInitScript(QString* errorMessage);
    void appendLogLine(const QString& line);
    void updateProgressUi(int current, int total, double rate, int elapsedSec, int etaSec);
    void startTrainingRun(const QMap<QString, QString>& extraEnv, const QString& label);
    QString formatDuration(int seconds) const;

    SettingsStore* settingsStore = nullptr;
    RosterStore* rosterStore = nullptr;
    ProcessRunner runner;

    QSpinBox* gamesSpin = nullptr;
    QSpinBox* boardXSpin = nullptr;
    QSpinBox* boardYSpin = nullptr;
    QLabel* rosterSummary = nullptr;
    QLabel* progressLabel = nullptr;
    QLabel* progressStatsLabel = nullptr;
    QProgressBar* progressBar = nullptr;
    QPlainTextEdit* logView = nullptr;
    QPushButton* trainButton = nullptr;
    QPushButton* train8Button = nullptr;
    QPushButton* selfPlayButton = nullptr;
    QPushButton* clearCacheButton = nullptr;

    int pendingRuns = 0;
    QString currentTrainingLabel;
    QMap<QString, QString> lastExtraEnv;
};
