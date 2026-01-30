#include "util/ProcessRunner.h"

#include <QDateTime>
#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QJsonDocument>
#include <QJsonObject>
#include <QRegularExpression>
#include <QTextStream>

ProcessRunner::ProcessRunner(SettingsStore* settings, QObject* parent)
    : QObject(parent), settingsStore(settings) {
    setupProcess();
}

void ProcessRunner::setupProcess() {
    process = new QProcess(this);
    process->setProcessChannelMode(QProcess::SeparateChannels);

    connect(process, &QProcess::readyReadStandardOutput, this, [this]() {
        handleReadyRead(QProcess::StandardOutput);
    });
    connect(process, &QProcess::readyReadStandardError, this, [this]() {
        handleReadyRead(QProcess::StandardError);
    });
    connect(process, QOverload<int, QProcess::ExitStatus>::of(&QProcess::finished),
            this, &ProcessRunner::handleProcessFinished);
}

bool ProcessRunner::isRunning() const {
    return process && process->state() != QProcess::NotRunning;
}

void ProcessRunner::startPythonScript(const QString& tag,
                                      const QString& scriptPath,
                                      const QStringList& args,
                                      const QMap<QString, QString>& extraEnv,
                                      int expectedTotal) {
    if (!process || !settingsStore) {
        return;
    }
    if (isRunning()) {
        emit statusMessage("Процесс уже запущен. Дождитесь завершения.");
        return;
    }

    currentTag = tag;
    lastTotal = expectedTotal;
    lastEpisode = 0;
    progressSamples.clear();
    timer.restart();
    stdOutBuffer.clear();
    stdErrBuffer.clear();

    const QString repoRoot = settingsStore->resolvedRepoRoot();
    const QString pythonExe = settingsStore->resolvedPythonPath();
    if (pythonExe.isEmpty()) {
        emit statusMessage("Не найден интерпретатор Python. Укажите путь в Settings.");
        return;
    }

    QProcessEnvironment env = QProcessEnvironment::systemEnvironment();
    const QString gymPath = QDir(repoRoot).filePath("gym_mod");
    const QString existingPyPath = env.value("PYTHONPATH");
    env.insert("PYTHONPATH", gymPath + (existingPyPath.isEmpty() ? "" : ":" + existingPyPath));

    for (auto it = extraEnv.begin(); it != extraEnv.end(); ++it) {
        env.insert(it.key(), it.value());
    }

    process->setProcessEnvironment(env);
    process->setWorkingDirectory(repoRoot);

    QStringList finalArgs;
    finalArgs << "-u" << scriptPath;
    finalArgs << args;

    const QString envLog = buildEnvLogLine(pythonExe, repoRoot, scriptPath, finalArgs, extraEnv);
    logToAgentFile("ENV", envLog);
    emit statusMessage(envLog);

    process->start(pythonExe, finalArgs);
}

void ProcessRunner::stop() {
    if (!process || !isRunning()) {
        return;
    }
    process->terminate();
    if (!process->waitForFinished(3000)) {
        process->kill();
    }
}

void ProcessRunner::handleReadyRead(QProcess::ProcessChannel channel) {
    if (!process) {
        return;
    }

    QByteArray data = (channel == QProcess::StandardOutput)
                          ? process->readAllStandardOutput()
                          : process->readAllStandardError();
    QString* buffer = (channel == QProcess::StandardOutput) ? &stdOutBuffer : &stdErrBuffer;
    buffer->append(QString::fromUtf8(data));

    while (true) {
        int newlineIndex = buffer->indexOf('\n');
        if (newlineIndex < 0) {
            break;
        }
        QString line = buffer->left(newlineIndex);
        buffer->remove(0, newlineIndex + 1);
        line = line.trimmed();
        if (line.isEmpty()) {
            continue;
        }
        emit outputLine(line);
        if (!currentTag.isEmpty()) {
            logToAgentFile(currentTag, line);
        }
        int current = 0;
        int total = lastTotal;
        if (parseProgress(line, lastTotal, &current, &total)) {
            if (total > 0) {
                lastTotal = total;
            }
            if (current > 0) {
                lastEpisode = current;
            }
            int elapsedSec = static_cast<int>(timer.elapsed() / 1000);
            progressSamples.enqueue({current, elapsedSec});
            while (progressSamples.size() > 6) {
                progressSamples.dequeue();
            }
            double rate = 0.0;
            int etaSec = 0;
            if (progressSamples.size() >= 2) {
                const auto first = progressSamples.front();
                const auto last = progressSamples.back();
                int deltaEps = last.first - first.first;
                int deltaTime = last.second - first.second;
                if (deltaEps > 0 && deltaTime > 0) {
                    rate = static_cast<double>(deltaEps) / static_cast<double>(deltaTime);
                }
            }
            if (rate > 0.0 && lastTotal > 0) {
                int remaining = std::max(0, lastTotal - current);
                etaSec = static_cast<int>(remaining / rate);
            }
            emit progressUpdated(current, lastTotal, rate, elapsedSec, etaSec);
        }
    }
}

void ProcessRunner::handleProcessFinished(int exitCode, QProcess::ExitStatus status) {
    if (!currentTag.isEmpty()) {
        QString message = (status == QProcess::NormalExit)
                              ? QString("Процесс завершён. Код: %1").arg(exitCode)
                              : QString("Процесс завершён аварийно.");
        logToAgentFile(currentTag, message);
        emit outputLine(message);
    }
    emit finished(exitCode);
}

void ProcessRunner::logToAgentFile(const QString& tag, const QString& message) const {
    QString repoRoot = settingsStore ? settingsStore->resolvedRepoRoot() : QDir::currentPath();
    QString logPath = QDir(repoRoot).filePath("LOGS_FOR_AGENTS.md");
    QFile file(logPath);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Append)) {
        return;
    }
    QTextStream out(&file);
    out << QDateTime::currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        << " | [GUI][" << tag << "] " << message << "\n";
}

bool ProcessRunner::parseProgress(const QString& line, int fallbackTotal, int* currentOut, int* totalOut) const {
    if (!currentOut || !totalOut) {
        return false;
    }
    QRegularExpression epRegex("ep=(\\d+)");
    auto epMatch = epRegex.match(line);
    if (epMatch.hasMatch()) {
        *currentOut = epMatch.captured(1).toInt();
        *totalOut = fallbackTotal;
        return true;
    }

    QRegularExpression tqdmRegex("(\\d+)/(\\d+)");
    auto tqdmMatch = tqdmRegex.match(line);
    if (tqdmMatch.hasMatch()) {
        *currentOut = tqdmMatch.captured(1).toInt();
        *totalOut = tqdmMatch.captured(2).toInt();
        return true;
    }
    return false;
}

QString ProcessRunner::buildEnvLogLine(const QString& exe, const QString& cwd, const QString& script,
                                      const QStringList& args, const QMap<QString, QString>& env) const {
    QStringList envParts;
    for (auto it = env.begin(); it != env.end(); ++it) {
        envParts << QString("%1=%2").arg(it.key(), it.value());
    }
    return QString("[GUI][ENV] exe=%1 cwd=%2 script=%3 args=%4 %5")
        .arg(exe, cwd, script, args.join(" "), envParts.join(" "));
}
