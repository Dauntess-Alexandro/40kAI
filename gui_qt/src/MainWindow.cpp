#include "MainWindow.h"

#include <QAction>
#include <QApplication>
#include <QClipboard>
#include <QCloseEvent>
#include <QDateTime>
#include <QDesktopServices>
#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QLabel>
#include <QTabWidget>
#include <QToolBar>
#include <QUrl>

#include "tabs/TrainTab.h"
#include "tabs/MetricsTab.h"
#include "tabs/PlayTab.h"
#include "tabs/SettingsTab.h"
#include "tabs/EvalTab.h"

MainWindow::MainWindow(QWidget* parent) : QMainWindow(parent), settingsStore(this), rosterStore(this) {
    setWindowTitle("40kAI GUI (Qt)");
    resize(1400, 900);

    setupToolbar();
    setupStatusBar();

    auto* tabs = new QTabWidget(this);
    setCentralWidget(tabs);

    trainTab = new TrainTab(&settingsStore, &rosterStore, this);
    metricsTab = new MetricsTab(&settingsStore, this);
    playTab = new PlayTab(&settingsStore, &rosterStore, this);
    settingsTab = new SettingsTab(&settingsStore, this);
    evalTab = new EvalTab(&settingsStore, &rosterStore, this);

    tabs->addTab(trainTab, tr("Train"));
    tabs->addTab(metricsTab, tr("Model Metrics"));
    tabs->addTab(playTab, tr("Play"));
    tabs->addTab(settingsTab, tr("Settings"));
    tabs->addTab(evalTab, tr("Оценка"));

    connect(trainTab, &TrainTab::statusMessage, this, &MainWindow::updateStatusMessage);
    connect(trainTab, &TrainTab::progressMessage, this, &MainWindow::updateProgressMessage);
    connect(trainTab, &TrainTab::activeCheckpointChanged, this, &MainWindow::updateCheckpointMessage);

    connect(playTab, &PlayTab::statusMessage, this, &MainWindow::updateStatusMessage);
    connect(playTab, &PlayTab::activeCheckpointChanged, this, &MainWindow::updateCheckpointMessage);

    connect(evalTab, &EvalTab::statusMessage, this, &MainWindow::updateStatusMessage);

    connect(settingsTab, &SettingsTab::statusMessage, this, &MainWindow::updateStatusMessage);
    connect(settingsTab, &SettingsTab::themeToggled, this, &MainWindow::applyTheme);

    connect(&settingsStore, &SettingsStore::settingsChanged, this, [this]() {
        pythonLabel->setText("Python: " + settingsStore.resolvedPythonPath());
    });
    connect(&rosterStore, &RosterStore::rosterChanged, this, &MainWindow::handleRosterChanged);

    loadSettings();
    handleRosterChanged();
}

void MainWindow::closeEvent(QCloseEvent* event) {
    saveSettings();
    QMainWindow::closeEvent(event);
}

void MainWindow::setupToolbar() {
    auto* toolbar = new QToolBar(tr("Инструменты"), this);
    toolbar->setMovable(false);
    addToolBar(toolbar);

    auto* resetAction = toolbar->addAction(tr("Сбросить макет"));
    connect(resetAction, &QAction::triggered, this, &MainWindow::resetLayout);

    auto* logsAction = toolbar->addAction(tr("Открыть папку логов"));
    connect(logsAction, &QAction::triggered, this, &MainWindow::openLogsFolder);

    auto* debugAction = toolbar->addAction(tr("Скопировать debug info"));
    connect(debugAction, &QAction::triggered, this, &MainWindow::copyDebugInfo);

    auto* darkAction = toolbar->addAction(tr("Тёмная тема"));
    darkAction->setCheckable(true);
    connect(darkAction, &QAction::toggled, this, &MainWindow::applyTheme);

    connect(&settingsStore, &SettingsStore::settingsChanged, this, [darkAction, this]() {
        darkAction->setChecked(settingsStore.darkModeEnabled());
    });
}

void MainWindow::setupStatusBar() {
    statusLabel = new QLabel(tr("Готово"), this);
    progressLabel = new QLabel(tr(""), this);
    pythonLabel = new QLabel(tr("Python: не выбран"), this);
    checkpointLabel = new QLabel(tr("Checkpoint: не выбран"), this);

    statusBar()->addWidget(statusLabel, 2);
    statusBar()->addWidget(progressLabel, 1);
    statusBar()->addPermanentWidget(pythonLabel, 2);
    statusBar()->addPermanentWidget(checkpointLabel, 2);
}

void MainWindow::loadSettings() {
    settingsStore.load();

    const auto geometry = settingsStore.windowGeometry();
    if (!geometry.isEmpty()) {
        restoreGeometry(geometry);
    }

    pythonLabel->setText("Python: " + settingsStore.resolvedPythonPath());
    applyTheme(settingsStore.darkModeEnabled());

    const QString rosterPath = QDir(settingsStore.resolvedRepoRoot()).filePath("gui_qt/roster.json");
    rosterStore.loadFromFile(rosterPath);
}

void MainWindow::saveSettings() {
    settingsStore.setWindowGeometry(saveGeometry());
    settingsStore.save();

    const QString rosterPath = QDir(settingsStore.resolvedRepoRoot()).filePath("gui_qt/roster.json");
    rosterStore.saveToFile(rosterPath);
}

void MainWindow::resetLayout() {
    resize(1400, 900);
    updateStatusMessage("Макет сброшен.");
}

void MainWindow::openLogsFolder() {
    const QString repoRoot = settingsStore.resolvedRepoRoot();
    const QString logPath = QDir(repoRoot).filePath("LOGS_FOR_AGENTS.md");
    QDesktopServices::openUrl(QUrl::fromLocalFile(QFileInfo(logPath).absolutePath()));
}

void MainWindow::copyDebugInfo() {
    QString info;
    info += QString("Дата: %1\n").arg(QDateTime::currentDateTime().toString(Qt::ISODate));
    info += QString("Repo: %1\n").arg(settingsStore.resolvedRepoRoot());
    info += QString("Python: %1\n").arg(settingsStore.resolvedPythonPath());
    info += QString("Checkpoints: %1\n").arg(settingsStore.resolvedCheckpointsDir());
    info += QString("Qt: %1\n").arg(QT_VERSION_STR);

    QApplication::clipboard()->setText(info);
    updateStatusMessage("Debug info скопирован в буфер обмена.");
}

void MainWindow::applyTheme(bool enabled) {
    settingsStore.setDarkModeEnabled(enabled);
    QFile file(QDir(settingsStore.resolvedRepoRoot()).filePath("gui_qt/resources/dark.qss"));
    if (enabled && file.open(QIODevice::ReadOnly)) {
        qApp->setStyleSheet(QString::fromUtf8(file.readAll()));
    } else {
        qApp->setStyleSheet("");
    }
}

void MainWindow::updateStatusMessage(const QString& message) {
    statusLabel->setText(message);
}

void MainWindow::updateProgressMessage(const QString& message) {
    progressLabel->setText(message);
}

void MainWindow::updateCheckpointMessage(const QString& message) {
    checkpointLabel->setText(message);
}

void MainWindow::handleRosterChanged() {
    if (trainTab) {
        trainTab->refreshRosterSummary();
    }
}
