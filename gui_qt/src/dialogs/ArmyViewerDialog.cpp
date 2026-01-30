#include "dialogs/ArmyViewerDialog.h"

#include <algorithm>
#include <QDir>
#include <QFile>
#include <QHeaderView>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QLabel>
#include <QListWidget>
#include <QPushButton>
#include <QTableWidget>
#include <QVBoxLayout>
#include <QUuid>

ArmyViewerDialog::ArmyViewerDialog(SettingsStore* settings, RosterStore* roster, QWidget* parent)
    : QDialog(parent), settingsStore(settings), rosterStore(roster) {
    setWindowTitle(tr("Army Viewer"));
    resize(900, 600);

    playerRoster = rosterStore ? rosterStore->playerRoster() : QVector<RosterEntry>();
    modelRoster = rosterStore ? rosterStore->modelRoster() : QVector<RosterEntry>();

    auto* mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(12, 12, 12, 12);
    mainLayout->setSpacing(12);

    auto* contentLayout = new QHBoxLayout();
    contentLayout->setSpacing(12);

    availableTable = new QTableWidget(this);
    availableTable->setColumnCount(2);
    availableTable->setHorizontalHeaderLabels({tr("Юнит"), tr("Фракция")});
    availableTable->horizontalHeader()->setStretchLastSection(true);
    availableTable->setSelectionBehavior(QAbstractItemView::SelectRows);
    availableTable->setSelectionMode(QAbstractItemView::SingleSelection);

    auto* rosterLayout = new QVBoxLayout();
    auto* playerLabel = new QLabel(tr("Ростер игрока"), this);
    playerList = new QListWidget(this);
    auto* modelLabel = new QLabel(tr("Ростер модели"), this);
    modelList = new QListWidget(this);

    rosterLayout->addWidget(playerLabel);
    rosterLayout->addWidget(playerList);
    rosterLayout->addWidget(modelLabel);
    rosterLayout->addWidget(modelList);

    auto* buttonsLayout = new QVBoxLayout();
    auto* addPlayerButton = new QPushButton(tr("Добавить → игрок"), this);
    auto* addModelButton = new QPushButton(tr("Добавить → модель"), this);
    auto* removeButton = new QPushButton(tr("Удалить"), this);
    auto* clearButton = new QPushButton(tr("Очистить"), this);
    auto* mirrorButton = new QPushButton(tr("Зеркалировать"), this);

    buttonsLayout->addWidget(addPlayerButton);
    buttonsLayout->addWidget(addModelButton);
    buttonsLayout->addWidget(removeButton);
    buttonsLayout->addWidget(clearButton);
    buttonsLayout->addWidget(mirrorButton);
    buttonsLayout->addStretch();

    contentLayout->addWidget(availableTable, 2);
    contentLayout->addLayout(buttonsLayout);
    contentLayout->addLayout(rosterLayout, 2);

    statusLabel = new QLabel(tr("Выберите юнит и добавьте его в ростер."), this);

    auto* footerLayout = new QHBoxLayout();
    auto* applyButton = new QPushButton(tr("Применить"), this);
    auto* cancelButton = new QPushButton(tr("Отмена"), this);
    footerLayout->addStretch();
    footerLayout->addWidget(applyButton);
    footerLayout->addWidget(cancelButton);

    mainLayout->addLayout(contentLayout, 1);
    mainLayout->addWidget(statusLabel);
    mainLayout->addLayout(footerLayout);

    connect(addPlayerButton, &QPushButton::clicked, this, &ArmyViewerDialog::addToPlayer);
    connect(addModelButton, &QPushButton::clicked, this, &ArmyViewerDialog::addToModel);
    connect(removeButton, &QPushButton::clicked, this, &ArmyViewerDialog::removeSelected);
    connect(clearButton, &QPushButton::clicked, this, &ArmyViewerDialog::clearRosters);
    connect(mirrorButton, &QPushButton::clicked, this, &ArmyViewerDialog::mirrorPlayerToModel);
    connect(applyButton, &QPushButton::clicked, this, &ArmyViewerDialog::applyChanges);
    connect(cancelButton, &QPushButton::clicked, this, &ArmyViewerDialog::reject);

    loadAvailableUnits();
    rebuildRosterList(playerList, playerRoster);
    rebuildRosterList(modelList, modelRoster);
}

void ArmyViewerDialog::loadAvailableUnits() {
    const QString repoRoot = settingsStore ? settingsStore->resolvedRepoRoot() : QDir::currentPath();
    QFile file(QDir(repoRoot).filePath("gym_mod/gym_mod/engine/unitData.json"));
    if (!file.open(QIODevice::ReadOnly)) {
        statusLabel->setText(tr("Не удалось открыть unitData.json."));
        return;
    }
    const auto doc = QJsonDocument::fromJson(file.readAll());
    if (!doc.isObject()) {
        statusLabel->setText(tr("unitData.json имеет неверный формат."));
        return;
    }
    const auto obj = doc.object();
    const auto unitsArray = obj.value("UnitData").toArray();

    availableUnits.clear();
    availableTable->setRowCount(unitsArray.size());

    int row = 0;
    for (const auto& value : unitsArray) {
        if (!value.isObject()) {
            continue;
        }
        const auto unitObj = value.toObject();
        AvailableUnit unit;
        unit.name = unitObj.value("Name").toString();
        unit.faction = unitObj.value("Army").toString();
        unit.defaultCount = unitObj.value("#OfModels").toInt(1);
        if (unit.name.isEmpty()) {
            continue;
        }
        availableUnits.push_back(unit);
        availableTable->setItem(row, 0, new QTableWidgetItem(unit.name));
        availableTable->setItem(row, 1, new QTableWidgetItem(unit.faction));
        ++row;
    }
    availableTable->setRowCount(row);
}

void ArmyViewerDialog::rebuildRosterList(QListWidget* list, const QVector<RosterEntry>& roster) const {
    list->clear();
    QMap<QString, int> totalByName;
    for (const auto& entry : roster) {
        totalByName[entry.name] += 1;
    }
    QMap<QString, int> seenByName;
    for (const auto& entry : roster) {
        int ordinal = ++seenByName[entry.name];
        QString displayName = entry.name;
        if (totalByName.value(entry.name) > 1) {
            displayName += QString(" #%1").arg(ordinal);
        }
        QString display = QString("(Unit) %1 (x%2 Models)").arg(displayName).arg(entry.modelsCount);
        auto* item = new QListWidgetItem(display, list);
        item->setData(Qt::UserRole, entry.instanceId);
    }
}

ArmyViewerDialog::AvailableUnit ArmyViewerDialog::selectedUnit() const {
    auto selection = availableTable->selectionModel();
    if (!selection || selection->selectedRows().isEmpty()) {
        return {};
    }
    const int row = selection->selectedRows().first().row();
    if (row < 0 || row >= availableUnits.size()) {
        return {};
    }
    return availableUnits.at(row);
}

void ArmyViewerDialog::addToPlayer() {
    auto unit = selectedUnit();
    if (unit.name.isEmpty()) {
        statusLabel->setText(tr("Выберите юнит в списке доступных."));
        return;
    }
    RosterEntry entry{unit.name, unit.faction, unit.defaultCount, QUuid::createUuid().toString(QUuid::WithoutBraces)};
    playerRoster.push_back(entry);
    rebuildRosterList(playerList, playerRoster);
    statusLabel->setText(tr("Юнит добавлен в ростер игрока."));
}

void ArmyViewerDialog::addToModel() {
    auto unit = selectedUnit();
    if (unit.name.isEmpty()) {
        statusLabel->setText(tr("Выберите юнит в списке доступных."));
        return;
    }
    RosterEntry entry{unit.name, unit.faction, unit.defaultCount, QUuid::createUuid().toString(QUuid::WithoutBraces)};
    modelRoster.push_back(entry);
    rebuildRosterList(modelList, modelRoster);
    statusLabel->setText(tr("Юнит добавлен в ростер модели."));
}

void ArmyViewerDialog::removeSelected() {
    auto* playerItem = playerList->currentItem();
    if (playerItem) {
        QString id = playerItem->data(Qt::UserRole).toString();
        playerRoster.erase(std::remove_if(playerRoster.begin(), playerRoster.end(),
                                          [&](const RosterEntry& entry) { return entry.instanceId == id; }),
                           playerRoster.end());
        rebuildRosterList(playerList, playerRoster);
        statusLabel->setText(tr("Юнит удалён из ростера игрока."));
        return;
    }

    auto* modelItem = modelList->currentItem();
    if (modelItem) {
        QString id = modelItem->data(Qt::UserRole).toString();
        modelRoster.erase(std::remove_if(modelRoster.begin(), modelRoster.end(),
                                         [&](const RosterEntry& entry) { return entry.instanceId == id; }),
                          modelRoster.end());
        rebuildRosterList(modelList, modelRoster);
        statusLabel->setText(tr("Юнит удалён из ростера модели."));
        return;
    }

    statusLabel->setText(tr("Сначала выберите юнит для удаления."));
}

void ArmyViewerDialog::clearRosters() {
    playerRoster.clear();
    modelRoster.clear();
    rebuildRosterList(playerList, playerRoster);
    rebuildRosterList(modelList, modelRoster);
    statusLabel->setText(tr("Ростеры очищены."));
}

void ArmyViewerDialog::mirrorPlayerToModel() {
    modelRoster = playerRoster;
    rebuildRosterList(modelList, modelRoster);
    statusLabel->setText(tr("Ростер модели обновлён из ростера игрока."));
}

void ArmyViewerDialog::applyChanges() {
    if (rosterStore) {
        rosterStore->setPlayerRoster(playerRoster);
        rosterStore->setModelRoster(modelRoster);
    }
    accept();
}
