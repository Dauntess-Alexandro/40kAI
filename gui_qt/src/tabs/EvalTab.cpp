#include "tabs/EvalTab.h"

#include <QCheckBox>
#include <QDoubleSpinBox>
#include <QFileDialog>
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPlainTextEdit>
#include <QPushButton>
#include <QSpinBox>
#include <QVBoxLayout>

EvalTab::EvalTab(SettingsStore* settings, RosterStore* roster, QWidget* parent)
    : QWidget(parent), settingsStore(settings), rosterStore(roster), runner(settings, this) {
    auto* mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(12, 12, 12, 12);
    mainLayout->setSpacing(12);

    auto* fileLayout = new QHBoxLayout();
    fileLayout->addWidget(new QLabel(tr("Checkpoint"), this));
    checkpointEdit = new QLineEdit(this);
    auto* browseButton = new QPushButton(tr("Выбрать"), this);
    fileLayout->addWidget(checkpointEdit, 1);
    fileLayout->addWidget(browseButton);

    auto* optionsLayout = new QHBoxLayout();
    forceGreedyCheck = new QCheckBox(tr("FORCE_GREEDY"), this);
    forceGreedyCheck->setChecked(true);
    epsilonSpin = new QDoubleSpinBox(this);
    epsilonSpin->setRange(0.0, 1.0);
    epsilonSpin->setSingleStep(0.05);
    epsilonSpin->setValue(0.0);
    episodesSpin = new QSpinBox(this);
    episodesSpin->setRange(1, 10000);
    episodesSpin->setValue(50);

    optionsLayout->addWidget(forceGreedyCheck);
    optionsLayout->addWidget(new QLabel(tr("EVAL_EPSILON"), this));
    optionsLayout->addWidget(epsilonSpin);
    optionsLayout->addWidget(new QLabel(tr("игр"), this));
    optionsLayout->addWidget(episodesSpin);
    optionsLayout->addStretch();

    auto* runButton = new QPushButton(tr("Запустить симуляцию"), this);

    summaryLabel = new QLabel(tr("Результат: —"), this);
    logView = new QPlainTextEdit(this);
    logView->setReadOnly(true);

    mainLayout->addLayout(fileLayout);
    mainLayout->addLayout(optionsLayout);
    mainLayout->addWidget(runButton);
    mainLayout->addWidget(summaryLabel);
    mainLayout->addWidget(logView, 1);

    connect(browseButton, &QPushButton::clicked, this, &EvalTab::browseCheckpoint);
    connect(runButton, &QPushButton::clicked, this, &EvalTab::runEval);

    connect(&runner, &ProcessRunner::outputLine, this, &EvalTab::handleOutputLine);
    connect(&runner, &ProcessRunner::finished, this, &EvalTab::handleFinished);
    connect(&runner, &ProcessRunner::statusMessage, this, &EvalTab::statusMessage);
}

void EvalTab::browseCheckpoint() {
    const QString startDir = settingsStore->resolvedCheckpointsDir();
    const QString path = QFileDialog::getOpenFileName(this, tr("Выберите модель"), startDir,
                                                      tr("Pickle Files (*.pickle)"));
    if (!path.isEmpty()) {
        checkpointEdit->setText(path);
    }
}

void EvalTab::runEval() {
    QMap<QString, QString> env;
    env.insert("FORCE_GREEDY", forceGreedyCheck->isChecked() ? "1" : "0");
    env.insert("EVAL_EPSILON", QString::number(epsilonSpin->value()));

    QStringList args;
    args << "--games" << QString::number(episodesSpin->value());
    if (!checkpointEdit->text().trimmed().isEmpty()) {
        args << "--model" << checkpointEdit->text().trimmed();
    }

    summaryLabel->setText(tr("Результат: —"));
    appendLogLine(tr("Старт симуляции: игр=%1").arg(episodesSpin->value()));
    runner.startPythonScript("EVAL", "eval.py", args, env, 0);
}

void EvalTab::handleOutputLine(const QString& line) {
    appendLogLine(line);
    if (line.contains("[SUMMARY]")) {
        updateSummary(line);
    }
}

void EvalTab::handleFinished(int exitCode) {
    if (exitCode == 0) {
        appendLogLine(tr("Симуляция завершена."));
    } else {
        appendLogLine(tr("Симуляция завершена с ошибкой. Код: %1").arg(exitCode));
    }
}

void EvalTab::appendLogLine(const QString& line) {
    logView->appendPlainText(line);
}

void EvalTab::updateSummary(const QString& line) {
    summaryLabel->setText(tr("Результат: %1").arg(line));
}
