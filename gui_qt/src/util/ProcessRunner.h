#pragma once

#include <QObject>
#include <QProcess>
#include <QQueue>
#include <QElapsedTimer>

#include "util/SettingsStore.h"

class ProcessRunner : public QObject {
    Q_OBJECT
public:
    explicit ProcessRunner(SettingsStore* settings, QObject* parent = nullptr);

    bool isRunning() const;

    void startPythonScript(const QString& tag,
                           const QString& scriptPath,
                           const QStringList& args = {},
                           const QMap<QString, QString>& extraEnv = {},
                           int expectedTotal = 0);

    void stop();

signals:
    void outputLine(const QString& line);
    void progressUpdated(int current, int total, double rate, int elapsedSec, int etaSec);
    void statusMessage(const QString& message);
    void finished(int exitCode);

private:
    void setupProcess();
    void handleReadyRead(QProcess::ProcessChannel channel);
    void handleProcessFinished(int exitCode, QProcess::ExitStatus status);
    void logToAgentFile(const QString& tag, const QString& message) const;
    bool parseProgress(const QString& line, int fallbackTotal, int* currentOut, int* totalOut) const;
    QString buildEnvLogLine(const QString& exe, const QString& cwd, const QString& script,
                            const QStringList& args, const QMap<QString, QString>& env) const;

    SettingsStore* settingsStore = nullptr;
    QProcess* process = nullptr;
    QElapsedTimer timer;
    QQueue<QPair<int, int>> progressSamples;
    int lastTotal = 0;
    int lastEpisode = 0;
    QString currentTag;
    QString stdOutBuffer;
    QString stdErrBuffer;
};
