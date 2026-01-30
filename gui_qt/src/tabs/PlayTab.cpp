#include "tabs/PlayTab.h"

#include <QDesktopServices>
#include <QDir>
#include <QFileDialog>
#include <QFileInfo>
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPlainTextEdit>
#include <QProcess>
#include <QPushButton>
#include <QVBoxLayout>
#include <QUrl>
#include <QStandardPaths>

PlayTab::PlayTab(SettingsStore* settings, RosterStore* roster, QWidget* parent)
    : QWidget(parent), settingsStore(settings), rosterStore(roster), runner(settings, this) {
    auto* mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(12, 12, 12, 12);
    mainLayout->setSpacing(12);

    auto* fileLayout = new QHBoxLayout();
    fileLayout->addWidget(new QLabel(tr("Играть против модели:"), this));
    checkpointEdit = new QLineEdit(this);
    auto* browseButton = new QPushButton(tr("Выбрать"), this);
    fileLayout->addWidget(checkpointEdit, 1);
    fileLayout->addWidget(browseButton);

    auto* quickLayout = new QHBoxLayout();
    auto* latestButton = new QPushButton(tr("Использовать последний checkpoint"), this);
    auto* openButton = new QPushButton(tr("Открыть папку checkpoints"), this);
    quickLayout->addWidget(latestButton);
    quickLayout->addWidget(openButton);
    quickLayout->addStretch();

    auto* actionLayout = new QHBoxLayout();
    auto* terminalButton = new QPushButton(tr("Играть в терминале"), this);
    auto* guiButton = new QPushButton(tr("Играть в GUI"), this);
    actionLayout->addWidget(terminalButton);
    actionLayout->addWidget(guiButton);
    actionLayout->addStretch();

    logView = new QPlainTextEdit(this);
    logView->setReadOnly(true);

    mainLayout->addLayout(fileLayout);
    mainLayout->addLayout(quickLayout);
    mainLayout->addLayout(actionLayout);
    mainLayout->addWidget(logView, 1);

    connect(browseButton, &QPushButton::clicked, this, &PlayTab::browseCheckpoint);
    connect(latestButton, &QPushButton::clicked, this, &PlayTab::useLatestCheckpoint);
    connect(openButton, &QPushButton::clicked, this, &PlayTab::openCheckpointsFolder);
    connect(terminalButton, &QPushButton::clicked, this, &PlayTab::playInTerminal);
    connect(guiButton, &QPushButton::clicked, this, &PlayTab::playInGui);

    connect(&runner, &ProcessRunner::outputLine, this, &PlayTab::handleOutputLine);
    connect(&runner, &ProcessRunner::finished, this, &PlayTab::handleFinished);
    connect(&runner, &ProcessRunner::statusMessage, this, &PlayTab::statusMessage);
}

void PlayTab::browseCheckpoint() {
    const QString startDir = settingsStore->resolvedCheckpointsDir();
    const QString path = QFileDialog::getOpenFileName(this, tr("Выберите модель"), startDir,
                                                      tr("Pickle Files (*.pickle)"));
    if (path.isEmpty()) {
        return;
    }
    checkpointEdit->setText(path);
    emit activeCheckpointChanged("Checkpoint: " + path);
}

void PlayTab::useLatestCheckpoint() {
    QDir modelsDir(settingsStore->resolvedCheckpointsDir());
    modelsDir.setNameFilters(QStringList() << "*.pickle");
    modelsDir.setSorting(QDir::Time);
    const auto entries = modelsDir.entryInfoList(QDir::Files);
    if (entries.isEmpty()) {
        emit statusMessage(tr("Не найдено .pickle в models/."));
        return;
    }
    checkpointEdit->setText(entries.first().absoluteFilePath());
    emit activeCheckpointChanged("Checkpoint: " + entries.first().absoluteFilePath());
}

void PlayTab::openCheckpointsFolder() {
    QDesktopServices::openUrl(QUrl::fromLocalFile(settingsStore->resolvedCheckpointsDir()));
}

QString PlayTab::currentCheckpoint() const {
    const QString value = checkpointEdit->text().trimmed();
    return value.isEmpty() ? QString("None") : value;
}

void PlayTab::playInTerminal() {
    const QString repoRoot = settingsStore->resolvedRepoRoot();
    const QString pythonExe = settingsStore->resolvedPythonPath();
    if (pythonExe.isEmpty()) {
        emit statusMessage(tr("Не найден Python. Укажите путь в Settings."));
        return;
    }

    QMap<QString, QString> env;
    const QString gymPath = QDir(repoRoot).filePath("gym_mod");
    env.insert("PYTHONPATH", gymPath);
    env.insert("MANUAL_DICE", "1");
    env.insert("VERBOSE_LOGS", "1");

#ifdef Q_OS_WIN
    const QString command = "cmd.exe";
    const QStringList args = {"/c", "start", "", pythonExe, "-u", "play.py", currentCheckpoint(), "False"};
#else
    QString terminal = QStandardPaths::findExecutable("x-terminal-emulator");
    if (terminal.isEmpty()) {
        terminal = QStandardPaths::findExecutable("gnome-terminal");
    }
    if (terminal.isEmpty()) {
        terminal = QStandardPaths::findExecutable("konsole");
    }
    if (terminal.isEmpty()) {
        terminal = QStandardPaths::findExecutable("xfce4-terminal");
    }
    if (terminal.isEmpty()) {
        terminal = QStandardPaths::findExecutable("mate-terminal");
    }
    const QString command = terminal;
    const QStringList args = terminal.isEmpty()
        ? QStringList()
        : QStringList{"--", "bash", "-lc",
                      QString("cd '%1' && '%2' -u play.py '%3' False")
                          .arg(repoRoot, pythonExe, currentCheckpoint())};
#endif

    if (command.isEmpty() || !launchTerminalCommand(command, args, env)) {
        emit statusMessage(tr("Не удалось запустить терминал. Проверьте окружение."));
        return;
    }
    appendLogLine(tr("Запуск игры в терминале: %1").arg(currentCheckpoint()));
}

void PlayTab::playInGui() {
    QMap<QString, QString> env;
    env.insert("PLAY_NO_EXPLORATION", "1");
    if (settingsStore->fightReportEnabled()) {
        env.insert("FIGHT_REPORT", "1");
    }
    runner.startPythonScript("PLAY", "-m", {"viewer"}, env, 0);
    appendLogLine(tr("Запуск viewer..."));
}

bool PlayTab::launchTerminalCommand(const QString& command, const QStringList& args,
                                    const QMap<QString, QString>& env) {
    QProcess process;
    process.setWorkingDirectory(settingsStore->resolvedRepoRoot());
    QProcessEnvironment envVars = QProcessEnvironment::systemEnvironment();
    for (auto it = env.begin(); it != env.end(); ++it) {
        if (it.key() == "PYTHONPATH") {
            const QString existing = envVars.value("PYTHONPATH");
            envVars.insert("PYTHONPATH", it.value() + (existing.isEmpty() ? "" : ":" + existing));
        } else {
            envVars.insert(it.key(), it.value());
        }
    }
    process.setProcessEnvironment(envVars);
    process.setProgram(command);
    process.setArguments(args);
    return process.startDetached();
}

void PlayTab::appendLogLine(const QString& line) {
    logView->appendPlainText(line);
}

void PlayTab::handleOutputLine(const QString& line) {
    appendLogLine(line);
}

void PlayTab::handleFinished(int exitCode) {
    if (exitCode == 0) {
        appendLogLine(tr("Процесс viewer завершён."));
    } else {
        appendLogLine(tr("viewer завершён с ошибкой. Код: %1").arg(exitCode));
    }
}
