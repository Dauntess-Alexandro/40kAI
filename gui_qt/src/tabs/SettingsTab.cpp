#include "tabs/SettingsTab.h"

#include <QCheckBox>
#include <QFileDialog>
#include <QFormLayout>
#include <QHBoxLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>

SettingsTab::SettingsTab(SettingsStore* settings, QWidget* parent)
    : QWidget(parent), settingsStore(settings) {
    auto* mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(12, 12, 12, 12);
    mainLayout->setSpacing(12);

    auto* formLayout = new QFormLayout();
    formLayout->setHorizontalSpacing(12);
    formLayout->setVerticalSpacing(8);

    const QString pythonValue = settingsStore->pythonPath().isEmpty()
                                    ? settingsStore->resolvedPythonPath()
                                    : settingsStore->pythonPath();
    pythonEdit = new QLineEdit(pythonValue, this);
    auto* pythonBrowse = new QPushButton(tr("Выбрать"), this);
    auto* pythonLayout = new QHBoxLayout();
    pythonLayout->addWidget(pythonEdit);
    pythonLayout->addWidget(pythonBrowse);

    const QString repoValue = settingsStore->repoRoot().isEmpty()
                                  ? settingsStore->resolvedRepoRoot()
                                  : settingsStore->repoRoot();
    repoEdit = new QLineEdit(repoValue, this);
    auto* repoBrowse = new QPushButton(tr("Выбрать"), this);
    auto* repoLayout = new QHBoxLayout();
    repoLayout->addWidget(repoEdit);
    repoLayout->addWidget(repoBrowse);

    const QString checkpointsValue = settingsStore->checkpointsDir().isEmpty()
                                         ? settingsStore->resolvedCheckpointsDir()
                                         : settingsStore->checkpointsDir();
    checkpointsEdit = new QLineEdit(checkpointsValue, this);
    auto* checkpointsBrowse = new QPushButton(tr("Выбрать"), this);
    auto* checkpointsLayout = new QHBoxLayout();
    checkpointsLayout->addWidget(checkpointsEdit);
    checkpointsLayout->addWidget(checkpointsBrowse);

    formLayout->addRow(tr("Python интерпретатор"), pythonLayout);
    formLayout->addRow(tr("Корень репозитория"), repoLayout);
    formLayout->addRow(tr("Папка checkpoints"), checkpointsLayout);

    darkModeCheck = new QCheckBox(tr("Тёмная тема"), this);
    darkModeCheck->setChecked(settingsStore->darkModeEnabled());
    trainDebugCheck = new QCheckBox(tr("TRAIN_DEBUG"), this);
    trainDebugCheck->setChecked(settingsStore->trainDebugEnabled());
    fightReportCheck = new QCheckBox(tr("FIGHT_REPORT"), this);
    fightReportCheck->setChecked(settingsStore->fightReportEnabled());

    auto* togglesLayout = new QHBoxLayout();
    togglesLayout->addWidget(darkModeCheck);
    togglesLayout->addWidget(trainDebugCheck);
    togglesLayout->addWidget(fightReportCheck);
    togglesLayout->addStretch();

    auto* saveButton = new QPushButton(tr("Сохранить настройки"), this);

    mainLayout->addLayout(formLayout);
    mainLayout->addLayout(togglesLayout);
    mainLayout->addStretch();
    mainLayout->addWidget(saveButton);

    connect(pythonBrowse, &QPushButton::clicked, this, &SettingsTab::browsePython);
    connect(repoBrowse, &QPushButton::clicked, this, &SettingsTab::browseRepoRoot);
    connect(checkpointsBrowse, &QPushButton::clicked, this, &SettingsTab::browseCheckpoints);
    connect(saveButton, &QPushButton::clicked, this, &SettingsTab::saveSettings);
    connect(darkModeCheck, &QCheckBox::toggled, this, &SettingsTab::toggleTheme);
}

void SettingsTab::browsePython() {
    const QString path = QFileDialog::getOpenFileName(this, tr("Python интерпретатор"),
                                                      settingsStore->resolvedRepoRoot());
    if (!path.isEmpty()) {
        pythonEdit->setText(path);
    }
}

void SettingsTab::browseRepoRoot() {
    const QString path = QFileDialog::getExistingDirectory(this, tr("Корень репозитория"),
                                                           settingsStore->resolvedRepoRoot());
    if (!path.isEmpty()) {
        repoEdit->setText(path);
    }
}

void SettingsTab::browseCheckpoints() {
    const QString path = QFileDialog::getExistingDirectory(this, tr("Папка checkpoints"),
                                                           settingsStore->resolvedCheckpointsDir());
    if (!path.isEmpty()) {
        checkpointsEdit->setText(path);
    }
}

void SettingsTab::saveSettings() {
    settingsStore->setPythonPath(pythonEdit->text().trimmed());
    settingsStore->setRepoRoot(repoEdit->text().trimmed());
    settingsStore->setCheckpointsDir(checkpointsEdit->text().trimmed());
    settingsStore->setDarkModeEnabled(darkModeCheck->isChecked());
    settingsStore->setTrainDebugEnabled(trainDebugCheck->isChecked());
    settingsStore->setFightReportEnabled(fightReportCheck->isChecked());

    if (settingsStore->save()) {
        emit statusMessage(tr("Настройки сохранены."));
    } else {
        emit statusMessage(tr("Не удалось сохранить настройки."));
    }
}

void SettingsTab::toggleTheme(bool enabled) {
    emit themeToggled(enabled);
}
