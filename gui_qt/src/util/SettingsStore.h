#pragma once

#include <QObject>
#include <QString>
#include <QByteArray>

class SettingsStore : public QObject {
    Q_OBJECT
public:
    explicit SettingsStore(QObject* parent = nullptr);

    void load();
    bool save() const;

    QString pythonPath() const;
    QString repoRoot() const;
    QString checkpointsDir() const;
    bool darkModeEnabled() const;
    bool trainDebugEnabled() const;
    bool fightReportEnabled() const;

    void setPythonPath(const QString& value);
    void setRepoRoot(const QString& value);
    void setCheckpointsDir(const QString& value);
    void setDarkModeEnabled(bool value);
    void setTrainDebugEnabled(bool value);
    void setFightReportEnabled(bool value);

    QString configPath() const;
    QString resolvedRepoRoot() const;
    QString resolvedPythonPath() const;
    QString resolvedCheckpointsDir() const;

    void setWindowGeometry(const QByteArray& geometry);
    QByteArray windowGeometry() const;

signals:
    void settingsChanged();

private:
    QString guessRepoRoot() const;
    QString guessPythonPath(const QString& repoRoot) const;

    QString pythonPathValue;
    QString repoRootValue;
    QString checkpointsDirValue;
    bool darkMode = false;
    bool trainDebug = false;
    bool fightReport = false;
    QByteArray geometryValue;
};
