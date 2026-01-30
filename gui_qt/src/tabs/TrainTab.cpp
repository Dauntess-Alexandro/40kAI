#include "tabs/TrainTab.h"

#include <QDir>
#include <QFileDialog>
#include <QGroupBox>
#include <QHBoxLayout>
#include <QMessageBox>
#include <QPlainTextEdit>
#include <QProgressBar>
#include <QPushButton>
#include <QSpinBox>
#include <QVBoxLayout>
#include <QTextCursor>

#include "dialogs/ArmyViewerDialog.h"

namespace {
constexpr int kDefaultBoardX = 60;
constexpr int kDefaultBoardY = 40;
}

TrainTab::TrainTab(SettingsStore* settings, RosterStore* roster, QWidget* parent)
    : QWidget(parent), settingsStore(settings), rosterStore(roster), runner(settings, this) {
    auto* mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(12, 12, 12, 12);
    mainLayout->setSpacing(12);

    auto* topGrid = new QGridLayout();
    topGrid->setHorizontalSpacing(12);
    topGrid->setVerticalSpacing(8);

    auto* gamesLabel = new QLabel(tr("Количество игр (обучение)"), this);
    gamesSpin = new QSpinBox(this);
    gamesSpin->setRange(1, 10000);
    gamesSpin->setValue(100);

    auto* modelFactionLabel = new QLabel(tr("Фракция модели"), this);
    auto* modelFactionValue = new QLabel(tr("Necrons"), this);
    modelFactionValue->setEnabled(false);

    auto* playerFactionLabel = new QLabel(tr("Фракция игрока"), this);
    auto* playerFactionValue = new QLabel(tr("Necrons"), this);
    playerFactionValue->setEnabled(false);

    auto* boardLabel = new QLabel(tr("Размеры поля"), this);
    boardXSpin = new QSpinBox(this);
    boardXSpin->setRange(10, 200);
    boardXSpin->setValue(kDefaultBoardX);
    boardYSpin = new QSpinBox(this);
    boardYSpin->setRange(10, 200);
    boardYSpin->setValue(kDefaultBoardY);

    topGrid->addWidget(gamesLabel, 0, 0);
    topGrid->addWidget(gamesSpin, 0, 1);
    topGrid->addWidget(modelFactionLabel, 1, 0);
    topGrid->addWidget(modelFactionValue, 1, 1);
    topGrid->addWidget(playerFactionLabel, 2, 0);
    topGrid->addWidget(playerFactionValue, 2, 1);
    topGrid->addWidget(boardLabel, 3, 0);

    auto* boardLayout = new QHBoxLayout();
    boardLayout->setSpacing(8);
    boardLayout->addWidget(new QLabel(tr("X:"), this));
    boardLayout->addWidget(boardXSpin);
    boardLayout->addSpacing(8);
    boardLayout->addWidget(new QLabel(tr("Y:"), this));
    boardLayout->addWidget(boardYSpin);
    auto* boardWrapper = new QWidget(this);
    boardWrapper->setLayout(boardLayout);
    topGrid->addWidget(boardWrapper, 3, 1);

    auto* rosterGroup = new QGroupBox(tr("Ростер"), this);
    auto* rosterLayout = new QVBoxLayout(rosterGroup);
    rosterLayout->setContentsMargins(10, 10, 10, 10);
    rosterLayout->setSpacing(6);
    auto* rosterButton = new QPushButton(tr("Army Viewer"), rosterGroup);
    rosterSummary = new QLabel(tr("Юнитов игрока: 0 | Юнитов модели: 0"), rosterGroup);
    rosterLayout->addWidget(rosterButton);
    rosterLayout->addWidget(rosterSummary);

    auto* actionsGroup = new QGroupBox(tr("Действия"), this);
    auto* actionsLayout = new QGridLayout(actionsGroup);
    actionsLayout->setContentsMargins(10, 10, 10, 10);
    actionsLayout->setHorizontalSpacing(8);
    actionsLayout->setVerticalSpacing(6);

    clearCacheButton = new QPushButton(tr("Очистить кэш моделей"), actionsGroup);
    selfPlayButton = new QPushButton(tr("Самообучение"), actionsGroup);
    trainButton = new QPushButton(tr("Обучить"), actionsGroup);
    train8Button = new QPushButton(tr("Тренировать 8x"), actionsGroup);

    actionsLayout->addWidget(clearCacheButton, 0, 0);
    actionsLayout->addWidget(selfPlayButton, 0, 1);
    actionsLayout->addWidget(trainButton, 1, 0);
    actionsLayout->addWidget(train8Button, 1, 1);

    auto* topRow = new QHBoxLayout();
    topRow->addLayout(topGrid, 2);
    topRow->addWidget(rosterGroup, 1);
    topRow->addWidget(actionsGroup, 1);

    progressLabel = new QLabel(tr("ep=0/0 (0%)"), this);
    progressStatsLabel = new QLabel(tr("— it/s • elapsed 00:00"), this);
    progressBar = new QProgressBar(this);
    progressBar->setRange(0, 100);
    progressBar->setValue(0);

    logView = new QPlainTextEdit(this);
    logView->setReadOnly(true);

    auto* logButtons = new QHBoxLayout();
    auto* clearLogButton = new QPushButton(tr("Очистить"), this);
    auto* copyLogButton = new QPushButton(tr("Копировать"), this);
    auto* saveLogButton = new QPushButton(tr("Сохранить"), this);
    logButtons->addWidget(clearLogButton);
    logButtons->addWidget(copyLogButton);
    logButtons->addWidget(saveLogButton);
    logButtons->addStretch();

    mainLayout->addLayout(topRow);
    mainLayout->addWidget(progressLabel);
    mainLayout->addWidget(progressBar);
    mainLayout->addWidget(progressStatsLabel);
    mainLayout->addWidget(logView, 1);
    mainLayout->addLayout(logButtons);

    connect(trainButton, &QPushButton::clicked, this, &TrainTab::startTrain);
    connect(train8Button, &QPushButton::clicked, this, &TrainTab::startTrain8x);
    connect(selfPlayButton, &QPushButton::clicked, this, &TrainTab::startSelfPlay);
    connect(rosterButton, &QPushButton::clicked, this, &TrainTab::openArmyViewer);
    connect(clearCacheButton, &QPushButton::clicked, this, &TrainTab::clearModelCache);

    connect(clearLogButton, &QPushButton::clicked, logView, &QPlainTextEdit::clear);
    connect(copyLogButton, &QPushButton::clicked, [this]() {
        logView->selectAll();
        logView->copy();
        logView->moveCursor(QTextCursor::End);
    });
    connect(saveLogButton, &QPushButton::clicked, [this]() {
        const QString path = QFileDialog::getSaveFileName(this, tr("Сохранить лог"),
                                                          settingsStore->resolvedRepoRoot(),
                                                          tr("Text Files (*.txt)"));
        if (path.isEmpty()) {
            return;
        }
        QFile file(path);
        if (file.open(QIODevice::WriteOnly | QIODevice::Truncate)) {
            file.write(logView->toPlainText().toUtf8());
        }
    });

    connect(&runner, &ProcessRunner::outputLine, this, &TrainTab::handleOutputLine);
    connect(&runner, &ProcessRunner::progressUpdated, this, &TrainTab::handleProgress);
    connect(&runner, &ProcessRunner::finished, this, &TrainTab::handleFinished);
    connect(&runner, &ProcessRunner::statusMessage, this, &TrainTab::statusMessage);
}

void TrainTab::refreshRosterSummary() {
    if (rosterStore) {
        rosterSummary->setText(rosterStore->summary());
    }
}

void TrainTab::startTrain() {
    pendingRuns = 1;
    startTrainingRun({}, tr("Обучение"));
}

void TrainTab::startTrain8x() {
    pendingRuns = 8;
    startTrainingRun({{"VEC_ENV_COUNT", "8"}}, tr("Обучение 8x"));
}

void TrainTab::startSelfPlay() {
    pendingRuns = 1;
    startTrainingRun({{"SELF_PLAY_ENABLED", "1"}}, tr("Самообучение"));
}

void TrainTab::openArmyViewer() {
    ArmyViewerDialog dialog(settingsStore, rosterStore, this);
    if (dialog.exec() == QDialog::Accepted) {
        refreshRosterSummary();
    }
}

void TrainTab::clearModelCache() {
    const auto response = QMessageBox::warning(this, tr("Подтверждение"),
                                               tr("Вы уверены, что хотите удалить все модели и метрики?"),
                                               QMessageBox::Cancel | QMessageBox::Ok);
    if (response != QMessageBox::Ok) {
        return;
    }

    const QString repoRoot = settingsStore->resolvedRepoRoot();
    QDir modelsDir(QDir(repoRoot).filePath("models"));
    QDir metricsDir(QDir(repoRoot).filePath("metrics"));
    QDir imgDir(QDir(repoRoot).filePath("gui/img"));

    modelsDir.setFilter(QDir::Files);
    for (const auto& file : modelsDir.entryList()) {
        modelsDir.remove(file);
    }
    metricsDir.setFilter(QDir::Files | QDir::Dirs | QDir::NoDotAndDotDot);
    for (const auto& entry : metricsDir.entryList()) {
        metricsDir.remove(entry);
    }

    const QStringList keepFiles = {"epLen.png", "reward.png", "loss.png", "icon.png"};
    imgDir.setFilter(QDir::Files);
    for (const auto& file : imgDir.entryList()) {
        if (!keepFiles.contains(file)) {
            imgDir.remove(file);
        }
    }

    QFile logFile(QDir(repoRoot).filePath("LOGS_FOR_AGENTS.md"));
    if (logFile.open(QIODevice::WriteOnly | QIODevice::Truncate)) {
        logFile.close();
    }

    appendLogLine(tr("Кэш моделей и логи очищены."));
    emit statusMessage(tr("Кэш моделей очищен."));
}

bool TrainTab::prepareDataFile(QString* errorMessage) {
    if (!rosterStore) {
        return false;
    }
    if (!rosterStore->writeUnitsTxt(settingsStore->resolvedRepoRoot(), errorMessage)) {
        return false;
    }
    return runInitScript(errorMessage);
}

bool TrainTab::runInitScript(QString* errorMessage) {
    const QString pythonExe = settingsStore->resolvedPythonPath();
    if (pythonExe.isEmpty()) {
        if (errorMessage) {
            *errorMessage = tr("Не найден Python. Укажите путь в Settings.");
        }
        return false;
    }
    QStringList args;
    args << "-u" << "gym_mod/gym_mod/engine/initFile.py";
    args << QString::number(gamesSpin->value());
    args << "Necrons" << "Necrons";
    args << QString::number(boardXSpin->value());
    args << QString::number(boardYSpin->value());

    QProcess initProcess;
    initProcess.setWorkingDirectory(settingsStore->resolvedRepoRoot());
    QProcessEnvironment env = QProcessEnvironment::systemEnvironment();
    const QString gymPath = QDir(settingsStore->resolvedRepoRoot()).filePath("gym_mod");
    const QString existingPyPath = env.value("PYTHONPATH");
    env.insert("PYTHONPATH", gymPath + (existingPyPath.isEmpty() ? "" : ":" + existingPyPath));
    initProcess.setProcessEnvironment(env);
    initProcess.start(pythonExe, args);
    if (!initProcess.waitForFinished(30000)) {
        if (errorMessage) {
            *errorMessage = tr("initFile.py не завершился вовремя. Проверьте зависимости.");
        }
        return false;
    }
    if (initProcess.exitStatus() != QProcess::NormalExit || initProcess.exitCode() != 0) {
        if (errorMessage) {
            *errorMessage = tr("Ошибка initFile.py. Проверьте лог и файлы gui/units.txt.");
        }
        return false;
    }
    return true;
}

void TrainTab::startTrainingRun(const QMap<QString, QString>& extraEnv, const QString& label) {
    lastExtraEnv = extraEnv;
    QString errorMessage;
    if (!prepareDataFile(&errorMessage)) {
        appendLogLine(errorMessage);
        emit statusMessage(errorMessage);
        return;
    }

    QMap<QString, QString> env;
    env.insert("PER_ENABLED", "1");
    env.insert("N_STEP", "3");
    env.insert("TRAIN_LOG_TO_CONSOLE", "1");

    if (settingsStore->trainDebugEnabled()) {
        env.insert("TRAIN_DEBUG", "1");
    }
    if (settingsStore->fightReportEnabled()) {
        env.insert("FIGHT_REPORT", "1");
    }
    for (auto it = extraEnv.begin(); it != extraEnv.end(); ++it) {
        env.insert(it.key(), it.value());
    }

    currentTrainingLabel = label;
    appendLogLine(tr("Старт %1: PER=1, N_STEP=3.").arg(label));
    emit statusMessage(label + tr(" запущено."));

    progressBar->setValue(0);
    progressLabel->setText("ep=0/" + QString::number(gamesSpin->value()) + " (0%)");
    progressStatsLabel->setText("— it/s • elapsed 00:00");

    QString tag = "TRAIN";
    if (label.contains("8x")) {
        tag = "TRAIN8";
    } else if (label.contains("Самообуч")) {
        tag = "SELFPLAY";
    }
    runner.startPythonScript(tag, "train.py", {}, env, gamesSpin->value());
}

void TrainTab::handleOutputLine(const QString& line) {
    appendLogLine(line);
}

void TrainTab::handleProgress(int current, int total, double rate, int elapsedSec, int etaSec) {
    updateProgressUi(current, total, rate, elapsedSec, etaSec);
}

void TrainTab::handleFinished(int exitCode) {
    if (exitCode == 0) {
        appendLogLine(currentTrainingLabel + tr(" завершено."));
        emit statusMessage(currentTrainingLabel + tr(" завершено."));
        QDir modelsDir(QDir(settingsStore->resolvedRepoRoot()).filePath("models"));
        modelsDir.setNameFilters(QStringList() << "*.pickle");
        modelsDir.setSorting(QDir::Time);
        const auto entries = modelsDir.entryInfoList(QDir::Files);
        if (!entries.isEmpty()) {
            emit activeCheckpointChanged(QString("Checkpoint: %1").arg(entries.first().absoluteFilePath()));
        }
    } else {
        appendLogLine(currentTrainingLabel + tr(" завершено с ошибкой. Код: %1").arg(exitCode));
        emit statusMessage(currentTrainingLabel + tr(" завершено с ошибкой."));
    }

    if (pendingRuns > 1) {
        pendingRuns -= 1;
        startTrainingRun(lastExtraEnv, currentTrainingLabel);
        return;
    }
    pendingRuns = 0;
}

void TrainTab::appendLogLine(const QString& line) {
    logView->appendPlainText(line);
}

void TrainTab::updateProgressUi(int current, int total, double rate, int elapsedSec, int etaSec) {
    int percent = 0;
    if (total > 0) {
        percent = static_cast<int>(static_cast<double>(current) / total * 100.0);
    }
    progressBar->setValue(percent);
    progressBar->setFormat(QString::number(percent) + "%");
    progressLabel->setText(QString("ep=%1/%2 (%3%)").arg(current).arg(total).arg(percent));

    QString stats = rate > 0.0 ? QString("%1 it/s").arg(QString::number(rate, 'f', 1)) : "— it/s";
    stats += " • elapsed " + formatDuration(elapsedSec);
    if (etaSec > 0) {
        stats += " • ETA " + formatDuration(etaSec);
    }
    progressStatsLabel->setText(stats);
    emit progressMessage(stats);
}

QString TrainTab::formatDuration(int seconds) const {
    int minutes = seconds / 60;
    int hrs = minutes / 60;
    minutes = minutes % 60;
    int secs = seconds % 60;
    if (hrs > 0) {
        return QString("%1:%2:%3")
            .arg(hrs, 2, 10, QChar('0'))
            .arg(minutes, 2, 10, QChar('0'))
            .arg(secs, 2, 10, QChar('0'));
    }
    return QString("%1:%2")
        .arg(minutes, 2, 10, QChar('0'))
        .arg(secs, 2, 10, QChar('0'));
}
