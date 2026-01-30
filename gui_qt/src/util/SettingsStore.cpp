#include "util/SettingsStore.h"

#include <QCoreApplication>
#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QJsonDocument>
#include <QJsonObject>
#include <QStandardPaths>

namespace {
QString ensureAbsolute(const QString& path) {
    if (path.isEmpty()) {
        return {};
    }
    return QDir(path).absolutePath();
}
}

SettingsStore::SettingsStore(QObject* parent) : QObject(parent) {}

void SettingsStore::load() {
    QFile file(configPath());
    if (!file.exists()) {
        return;
    }
    if (!file.open(QIODevice::ReadOnly)) {
        return;
    }
    const auto doc = QJsonDocument::fromJson(file.readAll());
    if (!doc.isObject()) {
        return;
    }
    const auto obj = doc.object();
    pythonPathValue = obj.value("python_path").toString();
    repoRootValue = obj.value("repo_root").toString();
    checkpointsDirValue = obj.value("checkpoints_dir").toString();
    darkMode = obj.value("dark_mode").toBool(false);
    trainDebug = obj.value("train_debug").toBool(false);
    fightReport = obj.value("fight_report").toBool(false);
    geometryValue = QByteArray::fromBase64(obj.value("window_geometry").toString().toUtf8());
}

bool SettingsStore::save() const {
    QJsonObject obj;
    obj.insert("python_path", pythonPathValue);
    obj.insert("repo_root", repoRootValue);
    obj.insert("checkpoints_dir", checkpointsDirValue);
    obj.insert("dark_mode", darkMode);
    obj.insert("train_debug", trainDebug);
    obj.insert("fight_report", fightReport);
    obj.insert("window_geometry", QString::fromUtf8(geometryValue.toBase64()));

    QDir().mkpath(QFileInfo(configPath()).absolutePath());
    QFile file(configPath());
    if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate)) {
        return false;
    }
    file.write(QJsonDocument(obj).toJson(QJsonDocument::Indented));
    return true;
}

QString SettingsStore::pythonPath() const {
    return pythonPathValue;
}

QString SettingsStore::repoRoot() const {
    return repoRootValue;
}

QString SettingsStore::checkpointsDir() const {
    return checkpointsDirValue;
}

bool SettingsStore::darkModeEnabled() const {
    return darkMode;
}

bool SettingsStore::trainDebugEnabled() const {
    return trainDebug;
}

bool SettingsStore::fightReportEnabled() const {
    return fightReport;
}

void SettingsStore::setPythonPath(const QString& value) {
    pythonPathValue = value;
    emit settingsChanged();
}

void SettingsStore::setRepoRoot(const QString& value) {
    repoRootValue = value;
    emit settingsChanged();
}

void SettingsStore::setCheckpointsDir(const QString& value) {
    checkpointsDirValue = value;
    emit settingsChanged();
}

void SettingsStore::setDarkModeEnabled(bool value) {
    darkMode = value;
    emit settingsChanged();
}

void SettingsStore::setTrainDebugEnabled(bool value) {
    trainDebug = value;
    emit settingsChanged();
}

void SettingsStore::setFightReportEnabled(bool value) {
    fightReport = value;
    emit settingsChanged();
}

QString SettingsStore::configPath() const {
    QString root = resolvedRepoRoot();
    if (root.isEmpty()) {
        root = QDir::currentPath();
    }
    return QDir(root).filePath("gui_qt/config.json");
}

QString SettingsStore::resolvedRepoRoot() const {
    if (!repoRootValue.isEmpty()) {
        return ensureAbsolute(repoRootValue);
    }
    return guessRepoRoot();
}

QString SettingsStore::resolvedPythonPath() const {
    if (!pythonPathValue.isEmpty()) {
        return ensureAbsolute(pythonPathValue);
    }
    return guessPythonPath(resolvedRepoRoot());
}

QString SettingsStore::resolvedCheckpointsDir() const {
    if (!checkpointsDirValue.isEmpty()) {
        return ensureAbsolute(checkpointsDirValue);
    }
    const QString root = resolvedRepoRoot();
    if (!root.isEmpty()) {
        return QDir(root).filePath("models");
    }
    return {};
}

void SettingsStore::setWindowGeometry(const QByteArray& geometry) {
    geometryValue = geometry;
}

QByteArray SettingsStore::windowGeometry() const {
    return geometryValue;
}

QString SettingsStore::guessRepoRoot() const {
    QDir dir(QCoreApplication::applicationDirPath());
    for (int i = 0; i < 6; ++i) {
        if (dir.exists("train.py") && dir.exists("gym_mod")) {
            return dir.absolutePath();
        }
        if (!dir.cdUp()) {
            break;
        }
    }
    return QDir::currentPath();
}

QString SettingsStore::guessPythonPath(const QString& repoRoot) const {
    QDir dir(repoRoot);
#ifdef Q_OS_WIN
    const QString candidate = dir.filePath(".venv/Scripts/python.exe");
#else
    const QString candidate = dir.filePath(".venv/bin/python");
#endif
    if (QFile::exists(candidate)) {
        return candidate;
    }
    return {};
}
