#pragma once

#include <QWidget>

#include "util/ProcessRunner.h"
#include "util/RosterStore.h"
#include "util/SettingsStore.h"

class QLabel;
class QLineEdit;
class QPlainTextEdit;
class QCheckBox;
class QDoubleSpinBox;
class QSpinBox;

class EvalTab : public QWidget {
    Q_OBJECT
public:
    explicit EvalTab(SettingsStore* settings, RosterStore* roster, QWidget* parent = nullptr);

signals:
    void statusMessage(const QString& message);

private slots:
    void browseCheckpoint();
    void runEval();
    void handleOutputLine(const QString& line);
    void handleFinished(int exitCode);

private:
    void appendLogLine(const QString& line);
    void updateSummary(const QString& line);

    SettingsStore* settingsStore = nullptr;
    RosterStore* rosterStore = nullptr;
    ProcessRunner runner;

    QLineEdit* checkpointEdit = nullptr;
    QCheckBox* forceGreedyCheck = nullptr;
    QDoubleSpinBox* epsilonSpin = nullptr;
    QSpinBox* episodesSpin = nullptr;
    QLabel* summaryLabel = nullptr;
    QPlainTextEdit* logView = nullptr;
};
