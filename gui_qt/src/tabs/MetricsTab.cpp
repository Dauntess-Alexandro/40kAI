#include "tabs/MetricsTab.h"

#include <QDir>
#include <QFile>
#include <QFileInfo>
#include <QFileDialog>
#include <QGridLayout>
#include <QJsonDocument>
#include <QJsonObject>
#include <QLabel>
#include <QPixmap>
#include <QPushButton>
#include <QRegularExpression>
#include <QHBoxLayout>
#include <QVBoxLayout>

MetricsTab::MetricsTab(SettingsStore* settings, QWidget* parent)
    : QWidget(parent), settingsStore(settings) {
    auto* mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(12, 12, 12, 12);
    mainLayout->setSpacing(12);

    auto* grid = new QGridLayout();
    grid->setHorizontalSpacing(12);
    grid->setVerticalSpacing(12);

    rewardLabel = new QLabel(this);
    lossLabel = new QLabel(this);
    winrateLabel = new QLabel(this);
    vpdiffLabel = new QLabel(this);
    epLenLabel = new QLabel(this);
    endreasonLabel = new QLabel(this);

    rewardLabel->setMinimumSize(330, 160);
    lossLabel->setMinimumSize(330, 160);
    winrateLabel->setMinimumSize(330, 160);
    vpdiffLabel->setMinimumSize(330, 160);
    epLenLabel->setMinimumSize(330, 160);
    endreasonLabel->setMinimumSize(330, 160);

    grid->addWidget(rewardLabel, 0, 0);
    grid->addWidget(lossLabel, 0, 1);
    grid->addWidget(winrateLabel, 1, 0);
    grid->addWidget(vpdiffLabel, 1, 1);
    grid->addWidget(epLenLabel, 2, 0);
    grid->addWidget(endreasonLabel, 2, 1);

    auto* chooseButton = new QPushButton(tr("Выбрать"), this);
    selectedLabel = new QLabel(tr("Выбранный файл: (последний)"), this);

    auto* footerLayout = new QHBoxLayout();
    footerLayout->addWidget(chooseButton);
    footerLayout->addWidget(selectedLabel);
    footerLayout->addStretch();

    mainLayout->addLayout(grid);
    mainLayout->addLayout(footerLayout);

    connect(chooseButton, &QPushButton::clicked, this, &MetricsTab::chooseModel);

    loadDefaultMetrics();
}

void MetricsTab::chooseModel() {
    const QString startDir = settingsStore ? settingsStore->resolvedCheckpointsDir() : QDir::currentPath();
    const QString path = QFileDialog::getOpenFileName(this, tr("Выберите модель"), startDir,
                                                      tr("Pickle Files (*.pickle)"));
    if (path.isEmpty()) {
        return;
    }
    updateMetricsFromModel(path);
}

void MetricsTab::loadDefaultMetrics() {
    const QString repoRoot = settingsStore ? settingsStore->resolvedRepoRoot() : QDir::currentPath();
    setMetricImage(rewardLabel, QDir(repoRoot).filePath("gui/img/reward.png"));
    setMetricImage(lossLabel, QDir(repoRoot).filePath("gui/img/loss.png"));
    setMetricImage(epLenLabel, QDir(repoRoot).filePath("gui/img/epLen.png"));
    setMetricImage(winrateLabel, QDir(repoRoot).filePath("gui/img/winrate.png"));
    setMetricImage(vpdiffLabel, QDir(repoRoot).filePath("gui/img/vpdiff.png"));
    setMetricImage(endreasonLabel, QDir(repoRoot).filePath("gui/img/endreasons.png"));
}

void MetricsTab::updateMetricsFromModel(const QString& modelPath) {
    selectedLabel->setText(tr("Выбранный файл: %1").arg(modelPath));

    QRegularExpression regex("(\\d{8,9})");
    auto match = regex.globalMatch(modelPath);
    QString id;
    while (match.hasNext()) {
        id = match.next().captured(1);
    }
    if (id.isEmpty()) {
        loadDefaultMetrics();
        return;
    }

    const QString repoRoot = settingsStore ? settingsStore->resolvedRepoRoot() : QDir::currentPath();
    QFile file(QDir(repoRoot).filePath(QString("models/data_%1.json").arg(id)));
    if (!file.open(QIODevice::ReadOnly)) {
        loadDefaultMetrics();
        return;
    }
    const auto doc = QJsonDocument::fromJson(file.readAll());
    if (!doc.isObject()) {
        loadDefaultMetrics();
        return;
    }
    const auto obj = doc.object();

    setMetricImage(rewardLabel, resolveMetricPath(obj.value("reward").toString("img/reward.png")));
    setMetricImage(lossLabel, resolveMetricPath(obj.value("loss").toString("img/loss.png")));
    setMetricImage(epLenLabel, resolveMetricPath(obj.value("epLen").toString("img/epLen.png")));
    setMetricImage(winrateLabel, resolveMetricPath(obj.value("winrate").toString("img/winrate.png")));
    setMetricImage(vpdiffLabel, resolveMetricPath(obj.value("vpdiff").toString("img/vpdiff.png")));
    setMetricImage(endreasonLabel, resolveMetricPath(obj.value("endreasons").toString("img/endreasons.png")));
}

QString MetricsTab::resolveMetricPath(const QString& rawPath) const {
    if (rawPath.isEmpty()) {
        return {};
    }
    QFileInfo info(rawPath);
    if (info.isAbsolute()) {
        return rawPath;
    }
    const QString repoRoot = settingsStore ? settingsStore->resolvedRepoRoot() : QDir::currentPath();
    return QDir(repoRoot).filePath("gui/" + rawPath);
}

void MetricsTab::setMetricImage(QLabel* label, const QString& path) {
    if (!label) {
        return;
    }
    QPixmap pix(path);
    if (!pix.isNull()) {
        label->setPixmap(pix.scaled(330, 160, Qt::KeepAspectRatio, Qt::SmoothTransformation));
    } else {
        label->setText(tr("Нет данных"));
    }
}
