#include "util/RosterStore.h"

#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QTextStream>

RosterStore::RosterStore(QObject* parent) : QObject(parent) {}

const QVector<RosterEntry>& RosterStore::playerRoster() const {
    return player;
}

const QVector<RosterEntry>& RosterStore::modelRoster() const {
    return model;
}

void RosterStore::setPlayerRoster(const QVector<RosterEntry>& roster) {
    player = roster;
    emit rosterChanged();
}

void RosterStore::setModelRoster(const QVector<RosterEntry>& roster) {
    model = roster;
    emit rosterChanged();
}

void RosterStore::clear() {
    player.clear();
    model.clear();
    emit rosterChanged();
}

QString RosterStore::summary() const {
    return QString("Юнитов игрока: %1 | Юнитов модели: %2").arg(player.size()).arg(model.size());
}

bool RosterStore::loadFromFile(const QString& path) {
    QFile file(path);
    if (!file.exists()) {
        return false;
    }
    if (!file.open(QIODevice::ReadOnly)) {
        return false;
    }
    const auto doc = QJsonDocument::fromJson(file.readAll());
    if (!doc.isObject()) {
        return false;
    }
    const auto obj = doc.object();
    QVector<RosterEntry> loadedPlayer;
    QVector<RosterEntry> loadedModel;

    auto parseArray = [](const QJsonArray& array) {
        QVector<RosterEntry> result;
        for (const auto& value : array) {
            if (!value.isObject()) {
                continue;
            }
            const auto entryObj = value.toObject();
            RosterEntry entry;
            entry.name = entryObj.value("name").toString();
            entry.faction = entryObj.value("faction").toString();
            entry.modelsCount = entryObj.value("models_count").toInt(1);
            entry.instanceId = entryObj.value("instance_id").toString();
            if (!entry.name.isEmpty()) {
                result.push_back(entry);
            }
        }
        return result;
    };

    loadedPlayer = parseArray(obj.value("player").toArray());
    loadedModel = parseArray(obj.value("model").toArray());

    player = loadedPlayer;
    model = loadedModel;
    emit rosterChanged();
    return true;
}

bool RosterStore::saveToFile(const QString& path) const {
    QJsonObject obj;
    auto toArray = [](const QVector<RosterEntry>& roster) {
        QJsonArray arr;
        for (const auto& entry : roster) {
            QJsonObject item;
            item.insert("name", entry.name);
            item.insert("faction", entry.faction);
            item.insert("models_count", entry.modelsCount);
            item.insert("instance_id", entry.instanceId);
            arr.push_back(item);
        }
        return arr;
    };
    obj.insert("player", toArray(player));
    obj.insert("model", toArray(model));

    QDir().mkpath(QFileInfo(path).absolutePath());
    QFile file(path);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate)) {
        return false;
    }
    file.write(QJsonDocument(obj).toJson(QJsonDocument::Indented));
    return true;
}

bool RosterStore::writeUnitsTxt(const QString& repoRoot, QString* errorMessage) const {
    const QString path = QDir(repoRoot).filePath("gui/units.txt");
    QFile file(path);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Truncate)) {
        if (errorMessage) {
            *errorMessage = QString("Не удалось записать %1. Проверьте права доступа.").arg(path);
        }
        return false;
    }
    QTextStream out(&file);
    out << "Player Units\n";
    for (const auto& entry : player) {
        out << entry.name << "|" << entry.modelsCount;
        if (!entry.instanceId.isEmpty()) {
            out << "|" << entry.instanceId;
        }
        out << "\n";
    }
    out << "Model Units\n";
    for (const auto& entry : model) {
        out << entry.name << "|" << entry.modelsCount;
        if (!entry.instanceId.isEmpty()) {
            out << "|" << entry.instanceId;
        }
        out << "\n";
    }
    return true;
}
