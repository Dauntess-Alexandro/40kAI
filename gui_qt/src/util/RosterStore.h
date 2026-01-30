#pragma once

#include "util/Types.h"

#include <QObject>
#include <QVector>

class RosterStore : public QObject {
    Q_OBJECT
public:
    explicit RosterStore(QObject* parent = nullptr);

    const QVector<RosterEntry>& playerRoster() const;
    const QVector<RosterEntry>& modelRoster() const;

    void setPlayerRoster(const QVector<RosterEntry>& roster);
    void setModelRoster(const QVector<RosterEntry>& roster);

    void clear();
    QString summary() const;

    bool loadFromFile(const QString& path);
    bool saveToFile(const QString& path) const;

    bool writeUnitsTxt(const QString& repoRoot, QString* errorMessage = nullptr) const;

signals:
    void rosterChanged();

private:
    QVector<RosterEntry> player;
    QVector<RosterEntry> model;
};
