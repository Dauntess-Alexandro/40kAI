#pragma once

#include <QWidget>

#include "util/SettingsStore.h"

class QLabel;
class QPushButton;

class MetricsTab : public QWidget {
    Q_OBJECT
public:
    explicit MetricsTab(SettingsStore* settings, QWidget* parent = nullptr);

private slots:
    void chooseModel();

private:
    void loadDefaultMetrics();
    void updateMetricsFromModel(const QString& modelPath);
    void setMetricImage(QLabel* label, const QString& path);
    QString resolveMetricPath(const QString& rawPath) const;

    SettingsStore* settingsStore = nullptr;
    QLabel* rewardLabel = nullptr;
    QLabel* lossLabel = nullptr;
    QLabel* winrateLabel = nullptr;
    QLabel* vpdiffLabel = nullptr;
    QLabel* epLenLabel = nullptr;
    QLabel* endreasonLabel = nullptr;
    QLabel* selectedLabel = nullptr;
};
