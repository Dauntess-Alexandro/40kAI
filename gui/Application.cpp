#include <iostream>
#include <gtkmm.h>
#include <cstdlib>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <thread>
#include <chrono>
#include <fstream>
#include <cstdio>
#include <ctime>
#include <iomanip>
#include <sstream>
#include <filesystem>
#include <vector>
#include <algorithm>
#include <array>
#include <cctype>
#include <nlohmann/json.hpp>
#include "include/Application.h"
#include "include/popup.h"
#include "include/units.h"
#include "include/warn.h"
#include "include/help.h"
#include "include/play.h"

using namespace Glib;
using namespace Gtk;
namespace fs = std::filesystem;
using json = nlohmann::json;

namespace {
constexpr int kDefaultWidth = 1500;
constexpr int kDefaultHeight = 900;
constexpr int kMinimumWidth = 1200;
constexpr int kMinimumHeight = 800;

std::string geometryPath() {
  const char* home = std::getenv("HOME");
  std::string base = home ? home : ".";
  return base + "/.config/40kAI/gui_layout.conf";
}

std::string toLowerCopy(std::string data) {
  std::transform(data.begin(), data.end(), data.begin(),
                 [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
  return data;
}

std::string nowTimestamp() {
  auto now = std::chrono::system_clock::now();
  std::time_t now_time = std::chrono::system_clock::to_time_t(now);
  std::tm local_tm{};
#if defined(_WIN32)
  localtime_s(&local_tm, &now_time);
#else
  localtime_r(&now_time, &local_tm);
#endif
  std::ostringstream oss;
  oss << std::put_time(&local_tm, "%Y-%m-%d %H:%M:%S");
  return oss.str();
}

int findDefaultModelsCount(const std::string& faction, const std::string& name) {
  std::ifstream infile("../gym_mod/gym_mod/engine/unitData.json");
  if (!infile) {
    return 1;
  }
  json j;
  infile >> j;
  if (!j.contains("UnitData") || !j.at("UnitData").is_array()) {
    return 1;
  }
  std::string factionLower = toLowerCopy(faction);
  std::string nameLower = toLowerCopy(name);
  for (const auto& unit : j.at("UnitData")) {
    if (!unit.contains("Name") || !unit.contains("Army")) {
      continue;
    }
    if (toLowerCopy(unit.at("Name").get<std::string>()) != nameLower) {
      continue;
    }
    if (toLowerCopy(unit.at("Army").get<std::string>()) != factionLower) {
      continue;
    }
    if (unit.contains("#OfModels") && unit.at("#OfModels").is_number_integer()) {
      return unit.at("#OfModels").get<int>();
    }
    return 1;
  }
  return 1;
}

int parsePositiveInt(const std::string& text) {
  const char* raw = text.c_str();
  char* end = nullptr;
  long value = std::strtol(raw, &end, 10);
  if (end == raw || value < 0) {
    return 0;
  }
  return static_cast<int>(value);
}

bool parseTrainEpisode(const std::string& line, int& current) {
  const std::string key = "ep=";
  size_t pos = line.find(key);
  if (pos == std::string::npos) {
    return false;
  }
  pos += key.size();
  if (pos >= line.size() || !std::isdigit(static_cast<unsigned char>(line[pos]))) {
    return false;
  }
  int value = 0;
  while (pos < line.size() && std::isdigit(static_cast<unsigned char>(line[pos]))) {
    value = value * 10 + (line[pos] - '0');
    ++pos;
  }
  current = value;
  return true;
}

bool parseTqdmProgress(const std::string& line, int& current, int& total) {
  size_t i = 0;
  while (i < line.size()) {
    if (!std::isdigit(static_cast<unsigned char>(line[i]))) {
      ++i;
      continue;
    }
    size_t start = i;
    while (i < line.size() && std::isdigit(static_cast<unsigned char>(line[i]))) {
      ++i;
    }
    if (i < line.size() && line[i] == '/' && i + 1 < line.size()
        && std::isdigit(static_cast<unsigned char>(line[i + 1]))) {
      int left = std::stoi(line.substr(start, i - start));
      size_t rightStart = i + 1;
      size_t rightEnd = rightStart;
      while (rightEnd < line.size()
             && std::isdigit(static_cast<unsigned char>(line[rightEnd]))) {
        ++rightEnd;
      }
      int right = std::stoi(line.substr(rightStart, rightEnd - rightStart));
      if (right > 0) {
        current = left;
        total = right;
        return true;
      }
    }
    ++i;
  }
  return false;
}

bool parseTrainingProgress(const std::string& line, int fallbackTotal, int& current, int& total) {
  int tqdmCurrent = 0;
  int tqdmTotal = 0;
  if (parseTqdmProgress(line, tqdmCurrent, tqdmTotal)) {
    current = tqdmCurrent;
    total = tqdmTotal;
    return true;
  }
  int trainCurrent = 0;
  if (parseTrainEpisode(line, trainCurrent)) {
    current = trainCurrent;
    total = fallbackTotal;
    return true;
  }
  return false;
}

std::string formatDuration(std::chrono::seconds duration) {
  auto totalSeconds = duration.count();
  int hours = static_cast<int>(totalSeconds / 3600);
  int minutes = static_cast<int>((totalSeconds % 3600) / 60);
  int seconds = static_cast<int>(totalSeconds % 60);
  std::ostringstream oss;
  if (hours > 0) {
    oss << std::setfill('0') << std::setw(2) << hours << ":"
        << std::setw(2) << minutes << ":"
        << std::setw(2) << seconds;
  } else {
    oss << std::setfill('0') << std::setw(2) << minutes << ":"
        << std::setw(2) << seconds;
  }
  return oss.str();
}

std::string buildTrainingStatsLine(double itPerSec,
                                   std::chrono::seconds elapsed,
                                   bool showEta,
                                   std::chrono::seconds eta) {
  std::ostringstream oss;
  if (itPerSec > 0.0) {
    oss << std::fixed << std::setprecision(1) << itPerSec << " it/s";
  } else {
    oss << "— it/s";
  }
  oss << " • elapsed " << formatDuration(elapsed);
  if (showEta) {
    oss << " • ETA " << formatDuration(eta);
  }
  return oss.str();
}
}  // namespace

std::string rewpth = "img/reward.png";
std::string losspth = "img/loss.png";
std::string eplenpth = "img/epLen.png";
std::string winratepth = "img/winrate.png";
std::string vpdiffpth = "img/vpdiff.png";
std::string endreasonpth = "img/endreasons.png";
std::string imgpth = "img/icon.png";

Form :: Form() {

  modelClass = " Necrons";
  enemyClass = " Necrons";
  path = " ";
  open = false;
  x = 60;
  y = 40;
  training = false;
  playing = false;
  loadingRoster = false;
  hideTrainingLogs = true;
  trainingTotalEpisodes = 0;
  trainEnvPrefix = "";
  trainingStartLabel = "обучения";
  trainingStatusLabel = "Обучение";
  trainingLogTag = "TRAIN";
  evaluating = false;

  bar.set_show_close_button(true);
  bar.set_title("40kAI GUI");
  set_titlebar(bar);

  set_default_size(kDefaultWidth, kDefaultHeight);
  set_size_request(kMinimumWidth, kMinimumHeight);

  rootBox.set_orientation(Gtk::ORIENTATION_VERTICAL);
  topBarBox.set_orientation(Gtk::ORIENTATION_HORIZONTAL);
  topBarBox.set_spacing(8);
  leftBox.set_orientation(Gtk::ORIENTATION_VERTICAL);

  rootBox.set_hexpand(true);
  rootBox.set_vexpand(true);
  topBarBox.set_hexpand(true);
  leftBox.set_hexpand(true);
  leftBox.set_vexpand(true);

  help.set_image_from_icon_name("help-about");
  help.signal_button_release_event().connect([&](GdkEventButton*){
    openHelpMenu();
    return true;
  });
  resetLayoutButton.set_label("Reset Layout");
  resetLayoutButton.signal_button_release_event().connect([&](GdkEventButton*) {
    resetLayout();
    return true;
  });
  topBarBox.pack_start(resetLayoutButton, Gtk::PACK_SHRINK);
  topBarBox.pack_start(help, Gtk::PACK_SHRINK);

  add(rootBox);
  rootBox.pack_start(topBarBox, Gtk::PACK_SHRINK);
  rootBox.pack_start(leftBox, Gtk::PACK_EXPAND_WIDGET);

  tabControl1.set_hexpand(true);
  tabControl1.set_vexpand(true);
  leftBox.pack_start(tabControl1, Gtk::PACK_EXPAND_WIDGET);

  logView.set_hexpand(true);
  logView.set_vexpand(true);
  logView.set_editable(false);
  logView.set_wrap_mode(Gtk::WRAP_WORD_CHAR);
  auto logBuffer = Gtk::TextBuffer::create();
  logView.set_buffer(logBuffer);

  logScroll.set_hexpand(true);
  logScroll.set_vexpand(true);
  logScroll.set_policy(PolicyType::POLICY_AUTOMATIC, PolicyType::POLICY_AUTOMATIC);
  logScroll.add(logView);

  leftBox.pack_start(logScroll, Gtk::PACK_EXPAND_WIDGET);

  tabControl1.insert_page(tabPage2, "Train", 0);
  tabControl1.insert_page(tabPage5, "Metrics", 1);
  tabControl1.insert_page(tabPage4, "Play", 2);
  tabControl1.insert_page(tabPage1, "Settings", 3);
  tabControl1.insert_page(tabPage6, "Оценка", 4);

    // settings tab

  labelPage1.set_label("Settings");
  tabControl1.set_tab_label(tabPage1, labelPage1);
  tabPage1.add(fixedTabPage1);

  textbox.set_text("Change Tab Location:");
  fixedTabPage1.add(textbox);
  fixedTabPage1.move(textbox, 10, 10);

  fixedTabPage1.add(radioTop);
  fixedTabPage1.move(radioTop, 10, 40);
  radioTop.set_label("Top");
  radioTop.set_group(radioButtonGroup);
  radioTop.signal_toggled().connect([this]() {
    tabControl1.set_tab_pos(PositionType::POS_TOP);
  });

  fixedTabPage1.add(radioLeft);
  fixedTabPage1.move(radioLeft, 10, 70);
  radioLeft.set_label("Left");
  radioLeft.set_group(radioButtonGroup);
  radioLeft.signal_toggled().connect([this]() {
    tabControl1.set_tab_pos(PositionType::POS_LEFT);
  });

  fixedTabPage1.add(radioRight);
  fixedTabPage1.move(radioRight, 10, 100);
  radioRight.set_label("Right");
  radioRight.set_group(radioButtonGroup);
  radioRight.signal_toggled().connect([this]() {
    tabControl1.set_tab_pos(PositionType::POS_RIGHT);
  });

  fixedTabPage1.add(radioBottom);
  fixedTabPage1.move(radioBottom, 10, 130);
  radioBottom.set_label("Bottom");
  radioBottom.set_group(radioButtonGroup);
  radioBottom.signal_toggled().connect([this]() {
    tabControl1.set_tab_pos(PositionType::POS_BOTTOM);
  });

    // eval tab

  labelPage6.set_label("Оценка");
  tabControl1.set_tab_label(tabPage6, labelPage6);
  tabPage6.add(fixedTabPage6);

  evalTitle.set_text("Симуляция: модель против эвристики");
  fixedTabPage6.add(evalTitle);
  fixedTabPage6.move(evalTitle, 10, 10);

  evalGamesLabel.set_text("Количество игр:");
  fixedTabPage6.add(evalGamesLabel);
  fixedTabPage6.move(evalGamesLabel, 10, 45);

  evalGamesAdjustment = Gtk::Adjustment::create(50, 1, 10000, 1, 10, 0);
  evalGamesSpin.set_adjustment(evalGamesAdjustment);
  evalGamesSpin.set_numeric(true);
  evalGamesSpin.set_digits(0);
  evalGamesSpin.set_value(50);
  evalGamesSpin.set_size_request(120, -1);
  fixedTabPage6.add(evalGamesSpin);
  fixedTabPage6.move(evalGamesSpin, 150, 40);

  evalRunButton.set_label("Запустить симуляцию");
  evalRunButton.signal_button_release_event().connect([this](GdkEventButton*) {
    startEvalInBackground();
    return true;
  });
  fixedTabPage6.add(evalRunButton);
  fixedTabPage6.move(evalRunButton, 300, 40);

  evalLogView.set_editable(false);
  evalLogView.set_wrap_mode(Gtk::WRAP_WORD_CHAR);
  auto evalBuffer = Gtk::TextBuffer::create();
  evalLogView.set_buffer(evalBuffer);

  evalLogScroll.set_hexpand(true);
  evalLogScroll.set_vexpand(true);
  evalLogScroll.set_policy(PolicyType::POLICY_AUTOMATIC, PolicyType::POLICY_AUTOMATIC);
  evalLogScroll.set_size_request(900, 600);
  evalLogScroll.add(evalLogView);
  fixedTabPage6.add(evalLogScroll);
  fixedTabPage6.move(evalLogScroll, 10, 90);

    // train tab

  savetoTxt(enemyUnits, modelUnits);

  labelPage2.set_label("Train");
  tabControl1.set_tab_label(tabPage2, labelPage2);
  tabPage2.add(fixedTabPage2);

  textbox1.set_text("Train Model:");
  setStatusMessage("Press the Train button to train a model");
  trainingProgressLabel.set_text("ep=0/0 (0%)");
  trainingProgressStatsLabel.set_text("— it/s • elapsed 00:00");
  trainingProgress.set_fraction(0.0);
  trainingProgress.set_show_text(true);
  trainingProgress.set_text("0%");
  trainingProgress.set_size_request(360, 24);
  trainingProgressStatsLabel.set_xalign(0.0);
  trainingProgressStatsLabel.set_size_request(520, -1);
    
  button1.set_label("Train");
  button1.signal_button_release_event().connect([&](GdkEventButton*) {
    saveLastRoster();
    syncEnemyUnitsFromRoster();
    updateInits(modelClass, enemyClass);
    if (exists_test("data.json") && training == false) {
      training = true;
      setStatusMessage("Training...");
      trainEnvPrefix = "";
      trainingStartLabel = "обучения";
      trainingStatusLabel = "Обучение";
      trainingLogTag = "TRAIN";
      startTrainInBackground();
    }
    return true;
  });

  buttonTrain6.set_label("Тренировать 8x");
  buttonTrain6.signal_button_release_event().connect([&](GdkEventButton*) {
    saveLastRoster();
    syncEnemyUnitsFromRoster();
    updateInits(modelClass, enemyClass);
    if (exists_test("data.json") && training == false) {
      training = true;
      setStatusMessage("Обучение 8x...");
      trainEnvPrefix = "VEC_ENV_COUNT=8 ";
      trainingStartLabel = "обучения 8x";
      trainingStatusLabel = "Обучение 8x";
      trainingLogTag = "TRAIN8";
      startTrainInBackground();
    }
    return true;
  });

  numOfGames.set_text("# of Games in Training:");
  setIters.set_text("100");

  modelUnitLabel.set_text("Enter Model Units:");
  enemyUnitLabel.set_text("Enter Player Units:");
  openArmyPopup.set_label("Army Viewer");
  openArmyPopup.signal_button_release_event().connect([&](GdkEventButton*) {
    openArmyView();
    return true;
  });

  dimens.set_text("Dimensions of Board: ");

  dimX.set_text("X : ");
  enterDimensX.set_text(std::to_string(x));
  upX.set_label("+");
  upX.signal_button_release_event().connect([&](GdkEventButton*) {
    x+=10;
    enterDimensX.set_text(std::to_string(x));
    return true;
  });
  downX.set_label("-");
  downX.signal_button_release_event().connect([&](GdkEventButton*) {
    x-=10;
    enterDimensX.set_text(std::to_string(x));
    return true;
  });

  dimY.set_text("Y :");
  enterDimensY.set_text(std::to_string(y));
  upY.set_label("+");
  upY.signal_button_release_event().connect([&](GdkEventButton*) {
    y+=10;
    enterDimensY.set_text(std::to_string(y));
    return true;
  });
  downY.set_label("-");
  downY.signal_button_release_event().connect([&](GdkEventButton*) {
    y-=10;
    enterDimensY.set_text(std::to_string(y));
    return true;
  });

  button3.set_label("Clear Model Cache");
  button3.signal_button_release_event().connect([&](GdkEventButton*) {
    std::string mess = "Warning: You are about to delete all of the saved models";
    openWarnMenu(mess, 0);
    return true;
  });

  buttonSelfPlay.set_label("Самообучение");
  buttonSelfPlay.signal_button_release_event().connect([&](GdkEventButton*) {
    saveLastRoster();
    syncEnemyUnitsFromRoster();
    updateInits(modelClass, enemyClass);
    if (exists_test("data.json") && training == false) {
      training = true;
      setStatusMessage("Самообучение: обучение...");
      trainEnvPrefix = "SELF_PLAY_ENABLED=1 ";
      trainingStartLabel = "самообучения";
      trainingStatusLabel = "Самообучение";
      trainingLogTag = "SELFPLAY";
      startTrainInBackground();
    }
    return true;
  });

  necModel.set_label("Necrons");
  necModel.set_group(factionModel);
  necModel.signal_toggled().connect([this]() {
    modelUnits.clear();
    modelClass = " Necrons";
  });
  necModel.set_active(true);

  necEnemy.set_label("Necrons");
  necEnemy.set_group(factionEnemy);
  necEnemy.signal_toggled().connect([this]() {
    enemyClass = " Necrons";
    if (!loadingRoster) {
      enemyUnits.clear();
      rosterModel.clear();
    }
    rosterModel.setFaction("Necrons");
    if (!loadingRoster) {
      syncEnemyUnitsFromRoster();
    }
  });
  necEnemy.set_active(true);

  enemyFact.set_text("Player Faction: ");
  modelFact.set_text("Model Faction: ");
  clearAllModel.set_label("Clear");
  clearAllModel.signal_button_release_event().connect([&](GdkEventButton*) {
    modelUnits.clear();
    savetoTxt(enemyUnits, modelUnits);
    return true;
  });
  clearAllEnemy.set_label("Clear");
  clearAllEnemy.signal_button_release_event().connect([&](GdkEventButton*) {
    rosterModel.clear();
    syncEnemyUnitsFromRoster();
    saveLastRoster();
    return true;
  });
  enemyEnter.set_label("Add");
  enemyEnter.signal_button_release_event().connect([&](GdkEventButton*) {
    if (addEnemyUnitFromEntry(enterEnemyUnit.get_text())) {
      syncEnemyUnitsFromRoster();
      saveLastRoster();
    }
    return true;
  });
  modelEnter.set_label("Add");
  modelEnter.signal_button_release_event().connect([&](GdkEventButton*) {
    if (isValidUnit(0, enterModelUnit.get_text()) == true) {
      savetoTxt(enemyUnits, modelUnits);
    }
    return true;
  });
  mirrorRosterButton.set_label("Mirror roster");
  mirrorRosterButton.signal_button_release_event().connect([&](GdkEventButton*) {
    mirrorRoster();
    return true;
  });

  fixedTabPage2.add(dimX);
  fixedTabPage2.move(dimX, 10, 265);
  fixedTabPage2.add(dimens);
  fixedTabPage2.move(dimens, 10, 240);
  fixedTabPage2.add(enterDimensX);
  fixedTabPage2.move(enterDimensX, 30, 260);
  fixedTabPage2.add(upX);
  fixedTabPage2.move(upX, 200, 260);
  fixedTabPage2.add(downX);
  fixedTabPage2.move(downX, 220, 260);

  fixedTabPage2.add(dimY);
  fixedTabPage2.move(dimY, 260, 265);
  fixedTabPage2.add(enterDimensY);
  fixedTabPage2.move(enterDimensY, 260+30, 260);
  fixedTabPage2.add(upY);
  fixedTabPage2.move(upY, 250+200, 260);
  fixedTabPage2.add(downY);
  fixedTabPage2.move(downY, 250+220, 260);

  fixedTabPage2.add(numOfGames);
  fixedTabPage2.move(numOfGames, 10, 45);
  fixedTabPage2.add(enemyFact);
  fixedTabPage2.move(enemyFact, 10, 120);
  fixedTabPage2.add(modelFact);
  fixedTabPage2.move(modelFact, 10, 80);
  fixedTabPage2.add(necModel);
  fixedTabPage2.move(necModel, 100, 80);
  fixedTabPage2.add(necEnemy);
  fixedTabPage2.move(necEnemy, 100, 120);
  fixedTabPage2.add(modelUnitLabel);
  fixedTabPage2.move(modelUnitLabel, 10, 163);
  fixedTabPage2.add(enterModelUnit);
  fixedTabPage2.move(enterModelUnit, 130, 160);
  fixedTabPage2.add(modelEnter);
  fixedTabPage2.move(modelEnter, 300, 160);
  fixedTabPage2.add(enemyUnitLabel);
  fixedTabPage2.move(enemyUnitLabel, 10, 203);
  fixedTabPage2.add(enterEnemyUnit);
  fixedTabPage2.move(enterEnemyUnit, 130, 200);
  fixedTabPage2.add(enemyEnter);
  fixedTabPage2.move(enemyEnter, 300, 200);
  fixedTabPage2.add(clearAllModel);
  fixedTabPage2.move(clearAllModel, 340, 160);
  fixedTabPage2.add(clearAllEnemy);
  fixedTabPage2.move(clearAllEnemy, 340, 200);
  fixedTabPage2.add(mirrorRosterButton);
  fixedTabPage2.move(mirrorRosterButton, 400, 140);
  fixedTabPage2.add(openArmyPopup);
  fixedTabPage2.move(openArmyPopup, 400, (160+200)/2);
  fixedTabPage2.add(textbox1);
  fixedTabPage2.move(textbox1, 10, 10);
  fixedTabPage2.add(button1);
  fixedTabPage2.move(button1, 380, 300);
  fixedTabPage2.add(buttonTrain6);
  fixedTabPage2.move(buttonTrain6, 470, 300);
  fixedTabPage2.add(setIters);
  fixedTabPage2.move(setIters, 160, 40);
  fixedTabPage2.add(button3);
  fixedTabPage2.move(button3, 10, 300);
  fixedTabPage2.add(buttonSelfPlay);
  fixedTabPage2.move(buttonSelfPlay, 200, 300);
  fixedTabPage2.add(status);
  fixedTabPage2.move(status, 10, 350);
  fixedTabPage2.add(trainingProgressLabel);
  fixedTabPage2.move(trainingProgressLabel, 10, 380);
  fixedTabPage2.add(trainingProgress);
  fixedTabPage2.move(trainingProgress, 10, 400);
  fixedTabPage2.add(trainingProgressStatsLabel);
  fixedTabPage2.move(trainingProgressStatsLabel, 10, 430);

  // show metrics tab
  labelPage5.set_label("Model Metrics");
  tabControl1.set_tab_label(tabPage5, labelPage5);
  tabPage5.add(fixedTabPage5);
  
  chooseMetrics.set_label("Choose");
  chooseMetrics.signal_button_release_event().connect([&](GdkEventButton * event){
	FileChooserDialog folderBrowserDialog("", FILE_CHOOSER_ACTION_OPEN);
    folderBrowserDialog.add_button("Cancel", RESPONSE_CANCEL);
    folderBrowserDialog.add_button("Open", RESPONSE_OK);
	system("clear");
    char resolved_path[PATH_MAX];
    realpath("../../40kAI", resolved_path);
    strcat(resolved_path, "/models");
    folderBrowserDialog.set_current_folder(resolved_path);
    folderBrowserDialog.set_transient_for(*this);

    auto filter_text = Gtk::FileFilter::create();
    filter_text->set_name("Pickle Files");
    filter_text->add_pattern("*.pickle");
    folderBrowserDialog.add_filter(filter_text);

    if (folderBrowserDialog.run() == RESPONSE_OK) {
      path = folderBrowserDialog.get_file()->get_path();
      changeMetrics(path);
    }
    return true;
  });

  fixedTabPage5.add(metricBox);
  fixedTabPage5.add(metricBox2);
  fixedTabPage5.add(metricBox4);
  fixedTabPage5.add(metricBox5);
  fixedTabPage5.add(metricBox3);
  fixedTabPage5.add(metricBox6);
  fixedTabPage5.add(chooseMetrics);

  // layout: 2 columns x 3 rows
  fixedTabPage5.move(metricBox,   0,   0);
  fixedTabPage5.move(metricBox2,  350, 0);
  fixedTabPage5.move(metricBox4,  0,   175);
  fixedTabPage5.move(metricBox5,  350, 175);
  fixedTabPage5.move(metricBox3,  0,   350);
  fixedTabPage5.move(metricBox6,  350, 350);
  fixedTabPage5.move(chooseMetrics, 300, 525);
  update_metrics();

     // Play tab
  labelPage4.set_label("Play");
  tabControl1.set_tab_label(tabPage4, labelPage4);
  tabPage4.add(fixedTabPage4);
  button2.set_label("Play in Terminal");
  textbox2.set_text("Play Against Model:");
  button2.signal_button_release_event().connect([&](GdkEventButton*) {
    if (playing == false) {
      saveLastRoster();
      syncEnemyUnitsFromRoster();
      playInGUI = "False";
      runPlayAgainstModelInBackground();
    }
    return true;
  });
  setModelFile.set_text(" ");
  button5.set_label("Choose");
  button5.signal_button_release_event().connect([&](GdkEventButton* event) {
    FileChooserDialog folderBrowserDialog("", FILE_CHOOSER_ACTION_OPEN);
    folderBrowserDialog.add_button("Cancel", RESPONSE_CANCEL);
    folderBrowserDialog.add_button("Open", RESPONSE_OK);
    system("clear");
    char resolved_path[PATH_MAX];
    realpath("../../40kAI", resolved_path);
    strcat(resolved_path, "/models");
    folderBrowserDialog.set_current_folder(resolved_path);
    folderBrowserDialog.set_transient_for(*this);

    auto filter_text = Gtk::FileFilter::create();
    filter_text->set_name("Pickle Files");
    filter_text->add_pattern("*.pickle");
    folderBrowserDialog.add_filter(filter_text);

    if (folderBrowserDialog.run() == RESPONSE_OK) {
      path = folderBrowserDialog.get_file()->get_path();
      setModelFile.set_text(path);
    }
    return true;
  });
  
  showBoard.set_label("Show Board (Ascii Mode)");
  showBoard.signal_button_release_event().connect([&](GdkEventButton* event) {
    openPopUp(true);
    return true;
  });

  playGraphicsView.set_label("Играть в GUI");
  playGraphicsView.signal_button_release_event().connect([&](GdkEventButton* event) {
    system("cd .. && scripts/viewer.sh &");
    return true;
  });

  fixedTabPage4.add(textbox2);
  fixedTabPage4.add(button2);
  fixedTabPage4.add(showBoard);
  fixedTabPage4.add(playGraphicsView);
  fixedTabPage4.add(button5);
  fixedTabPage4.add(setModelFile);
  fixedTabPage4.move(textbox2, 10, 10);
  fixedTabPage4.move(playGraphicsView, 130, 80);
  fixedTabPage4.move(showBoard, 395, 80);
  fixedTabPage4.move(button2, 10, 80);
  fixedTabPage4.move(button5, 10, 40);
  fixedTabPage4.move(setModelFile, 80, 40);

  loadWindowGeometry();
  loadLastRoster();
  if (modelUnits.empty()) {
    modelUnits.push_back({"Necron Warriors", "Necrons", findDefaultModelsCount("Necrons", "Necron Warriors"),
                          RosterModel::generateInstanceId()});
    modelUnits.push_back({"Royal Warden", "Necrons",
                          findDefaultModelsCount("Necrons", "Royal Warden"),
                          RosterModel::generateInstanceId()});
  }
  if (enemyUnits.empty()) {
    rosterModel.addUnit("Necron Warriors", 10, enemyClass.substr(1));
    rosterModel.addUnit("Canoptek Scarab Swarms", 3, enemyClass.substr(1));
    syncEnemyUnitsFromRoster();
    saveLastRoster();
  }
  signal_hide().connect([this]() {
    saveLastRoster();
    saveWindowGeometry();
  });
  show_all();
}

void Form :: setStatusMessage(const std::string& message) {
  status.set_text(message);
  if (!training || !hideTrainingLogs) {
    appendLogLine(message);
  }
}

void Form :: resetTrainingProgressStats() {
  trainingSamples.clear();
  trainingStartTime = std::chrono::steady_clock::now();
  trainingLastUiUpdate = trainingStartTime - std::chrono::milliseconds(500);
}

void Form :: recordTrainingSample(int episode, std::chrono::steady_clock::time_point now) {
  if (episode <= 0) {
    return;
  }
  if (!trainingSamples.empty() && trainingSamples.back().second == episode) {
    return;
  }
  trainingSamples.emplace_back(now, episode);
  constexpr size_t kMaxSamples = 80;
  while (trainingSamples.size() > kMaxSamples) {
    trainingSamples.pop_front();
  }
  auto cutoff = now - std::chrono::seconds(10);
  while (trainingSamples.size() > 2 && trainingSamples.front().first < cutoff) {
    trainingSamples.pop_front();
  }
}

double Form :: calculateTrainingRate() const {
  if (trainingSamples.size() < 2) {
    return 0.0;
  }
  const auto& first = trainingSamples.front();
  const auto& last = trainingSamples.back();
  auto seconds = std::chrono::duration_cast<std::chrono::duration<double>>(last.first - first.first).count();
  if (seconds <= 0.0) {
    return 0.0;
  }
  int delta = last.second - first.second;
  if (delta <= 0) {
    return 0.0;
  }
  return static_cast<double>(delta) / seconds;
}

void Form :: updateTrainingProgress(int current, int total) {
  if (total <= 0) {
    trainingProgress.set_fraction(0.0);
    trainingProgress.set_text("0%");
    trainingProgressLabel.set_text("ep=" + std::to_string(current) + "/?");
    return;
  }
  double fraction = static_cast<double>(current) / static_cast<double>(total);
  fraction = std::max(0.0, std::min(1.0, fraction));
  int percent = static_cast<int>(fraction * 100.0 + 0.5);
  trainingProgress.set_fraction(fraction);
  trainingProgress.set_text(std::to_string(percent) + "%");
  trainingProgressLabel.set_text(
      "ep=" + std::to_string(current) + "/" + std::to_string(total)
      + " (" + std::to_string(percent) + "%)");
}

void Form :: appendLogLine(const std::string& message) {
  auto logBuffer = logView.get_buffer();
  if (!logBuffer) {
    return;
  }
  logBuffer->insert(logBuffer->end(), message + "\n");
  auto endIter = logBuffer->end();
  logView.scroll_to(endIter);
}

void Form :: appendEvalLogLine(const std::string& message) {
  auto logBuffer = evalLogView.get_buffer();
  if (!logBuffer) {
    return;
  }
  logBuffer->insert(logBuffer->end(), message + "\n");
  auto endIter = logBuffer->end();
  evalLogView.scroll_to(endIter);
}

void Form :: appendTrainingLogToFile(const std::string& message, const std::string& tag) {
  fs::path logPath = fs::current_path() / "LOGS_FOR_AGENTS.md";
  if (!fs::exists(logPath)) {
    fs::path parentPath = fs::current_path().parent_path() / "LOGS_FOR_AGENTS.md";
    if (fs::exists(parentPath)) {
      logPath = parentPath;
    }
  }
  std::ofstream outfile(logPath, std::ios::app);
  if (!outfile) {
    Glib::signal_idle().connect_once([this]() {
      appendLogLine(
          "Ошибка записи в LOGS_FOR_AGENTS.md (gui/Application.cpp): проверьте путь и права доступа.");
    });
    return;
  }
  outfile << nowTimestamp() << " | [GUI][" << tag << "] " << message << "\n";
}

void Form :: startEvalInBackground() {
  if (evaluating) {
    appendEvalLogLine("Симуляция уже запущена. Дождитесь завершения.");
    return;
  }
  int games = static_cast<int>(evalGamesSpin.get_value());
  if (games < 1 || games > 10000) {
    appendEvalLogLine("Некорректное значение N. Укажите число от 1 до 10000.");
    return;
  }
  std::thread t(&Form::startEval, this, games);
  t.detach();
}

void Form :: startEval(int games) {
  evaluating = true;
  Glib::signal_idle().connect_once([this, games]() {
    appendEvalLogLine("Старт симуляции: игр=" + std::to_string(games));
  });

  std::string command =
      "cd .. ; PYTHONPATH=\"$(pwd)/gym_mod:${PYTHONPATH:-}\" FORCE_GREEDY=1 "
      "EVAL_EPSILON=0 .venv/bin/python -u eval.py --games ";
  command.append(std::to_string(games));
  command.append(" 2>&1");

  FILE* pipe = popen(command.c_str(), "r");
  if (!pipe) {
    std::string errorMessage = "Ошибка запуска симуляции (gui/Application.cpp): "
        "проверьте, что eval.py доступен.";
    Glib::signal_idle().connect_once([this, errorMessage]() {
      appendEvalLogLine(errorMessage);
    });
    evaluating = false;
    return;
  }

  std::array<char, 512> buffer{};
  while (fgets(buffer.data(), static_cast<int>(buffer.size()), pipe)) {
    std::string line(buffer.data());
    while (!line.empty() && (line.back() == '\n' || line.back() == '\r')) {
      line.pop_back();
    }
    if (line.empty()) {
      continue;
    }
    Glib::signal_idle().connect_once([this, line]() {
      appendEvalLogLine(line);
    });
  }

  int exitCode = pclose(pipe);
  if (exitCode == 0) {
    Glib::signal_idle().connect_once([this]() {
      appendEvalLogLine("Симуляция завершена.");
    });
  } else {
    std::string errLine = "Симуляция завершена с ошибкой. Код выхода: "
        + std::to_string(exitCode);
    Glib::signal_idle().connect_once([this, errLine]() {
      appendEvalLogLine(errLine);
    });
  }
  evaluating = false;
}

bool Form :: loadWindowGeometry() {
  std::ifstream infile(geometryPath());
  if (!infile) {
    return false;
  }
  int width = 0;
  int height = 0;
  if (!(infile >> width >> height)) {
    return false;
  }
  set_default_size(width, height);
  return true;
}

void Form :: saveWindowGeometry() {
  std::string path = geometryPath();
  fs::create_directories(fs::path(path).parent_path());
  int width = 0;
  int height = 0;
  get_size(width, height);
  std::ofstream outfile(path);
  if (!outfile) {
    return;
  }
  outfile << width << " " << height;
}

void Form :: ensureMinimumSize() {
  int width = 0;
  int height = 0;
  get_size(width, height);
  if (width < kMinimumWidth || height < kMinimumHeight) {
    resize(std::max(width, kMinimumWidth), std::max(height, kMinimumHeight));
  }
}

void Form :: resetLayout() {
  std::error_code ec;
  fs::remove(geometryPath(), ec);
  resize(kDefaultWidth, kDefaultHeight);
  ensureMinimumSize();
}

void Form :: changeMetrics(std::string path) {
    std::string jsonID = path.substr(path.length()-16,9);

	if (jsonID[0] == '-') {
		jsonID = path.substr(path.length()-15,8);
	} 

	std::ifstream infile("../models/data_"+jsonID+".json");
	json j;
	infile >> j;

	losspth = j.value("loss", losspth);
	rewpth = j.value("reward", rewpth);
	eplenpth = j.value("epLen", eplenpth);

	// optional extra metrics (backwards compatible with older models)
	winratepth = j.value("winrate", winratepth);
	vpdiffpth = j.value("vpdiff", vpdiffpth);
	endreasonpth = j.value("endreasons", endreasonpth);

	update_metrics();
}

int Form :: openPopUp(bool textMode) {
  boardShow = new PopUp(textMode);
  boardShow->show();
  return 0;
}

int Form :: openPlayGUI() {
  play = new Play;
  play->show();
  return 0;
}

int Form :: openArmyView() {
  armyView = new Units(&rosterModel);
  armyView->show();
  return 0;
}

int Form :: openWarnMenu(std::string mess, int comm) {
  warn = new Warn(mess, comm);
  warn->show();
  return 0;
}

int Form :: openHelpMenu() {
  helpMenu = new Help;
  helpMenu->show();
  return 0;
}

std::string Form :: toLower(std::string data) {
  std::transform(data.begin(), data.end(), data.begin(),[](unsigned char c){ return std::tolower(c); });
  return data;
}

void Form :: mirrorRoster() {
  auto playerEntry = enterEnemyUnit.get_text();
  syncEnemyUnitsFromRoster();
  if (rosterModel.empty() && playerEntry.empty()) {
    setStatusMessage("Player roster is empty, nothing to mirror.");
    return;
  }

  if (!playerEntry.empty()) {
    enterModelUnit.set_text(playerEntry);
  }

  if (!enemyClass.empty()) {
    applyFactionToModel(enemyClass.substr(1));
  }

  modelUnits = rosterModel.expandedUnits();
  savetoTxt(enemyUnits, modelUnits);
  setStatusMessage("Mirrored Player roster to Model.");
}

void Form :: applyFactionToModel(const std::string& faction) {
  if (faction.empty()) {
    return;
  }

  std::string normalized = toLower(faction);
  std::replace(normalized.begin(), normalized.end(), ' ', '_');
  if (normalized == "necrons") {
    necModel.set_active(true);
  }
}

void Form :: applyFactionToEnemy(const std::string& faction) {
  if (faction.empty()) {
    return;
  }

  std::string normalized = toLower(faction);
  std::replace(normalized.begin(), normalized.end(), ' ', '_');
  if (normalized == "necrons") {
    necEnemy.set_active(true);
  }
}

void Form :: saveLastRoster() {
  rosterModel.saveToFile(RosterModel::defaultRosterPath());
}

void Form :: loadLastRoster() {
  if (!rosterModel.loadFromFile(RosterModel::defaultRosterPath())) {
    return;
  }

  std::string loadedFaction = rosterModel.faction();
  if (!loadedFaction.empty()) {
    std::string normalized = toLower(loadedFaction);
    std::replace(normalized.begin(), normalized.end(), ' ', '_');
    if (normalized != "necrons") {
      rosterModel.clear();
      rosterModel.setFaction("Necrons");
      enemyClass = " Necrons";
      setStatusMessage("Фракция ростера не поддерживается, переключено на Necrons.");
    } else {
      loadingRoster = true;
      applyFactionToEnemy(loadedFaction);
      loadingRoster = false;
    }
  }

  syncEnemyUnitsFromRoster();
  setStatusMessage("Loaded last roster.");
}

void Form :: syncEnemyUnitsFromRoster() {
  enemyUnits = rosterModel.expandedUnits();
  savetoTxt(enemyUnits, modelUnits);
}

bool Form :: addEnemyUnitFromEntry(const std::string& entryText) {
  if (entryText.empty()) {
    return false;
  }
  std::ifstream infile("../gym_mod/gym_mod/engine/unitData.json");
  json j;
  infile >> j;

  if (!j.contains("UnitData") || !j.at("UnitData").is_array()) {
    return false;
  }

  for (const auto& unit : j.at("UnitData")) {
    if (!unit.contains("Name") || !unit.contains("Army")) {
      continue;
    }
    std::string name = unit.at("Name").get<std::string>();
    if (strcmp(toLower(name).data(), toLower(entryText).data()) != 0) {
      continue;
    }
    std::string army = unit.at("Army").get<std::string>();
    if (strcmp(toLower(army).data(), toLower(enemyClass.substr(1)).data()) != 0) {
      continue;
    }
    int defaultCount = 1;
    if (unit.contains("#OfModels") && unit.at("#OfModels").is_number_integer()) {
      defaultCount = unit.at("#OfModels").get<int>();
    }
    rosterModel.addUnit(name, defaultCount, army);
    return true;
  }
  return false;
}

// model: id = 0
// enemy: id = 1

bool Form :: isValidUnit(int id, std::string name) {
  std::ifstream infile("../gym_mod/gym_mod/engine/unitData.json");
  json j;
  infile >> j;

  const auto& unitData = j.at("UnitData");
  for (const auto& unit : unitData) {
    if (strcmp(toLower(unit.at("Name").get<std::string>()).data(), toLower(name).data()) == 0) {
      int modelsCount = 1;
      if (unit.contains("#OfModels") && unit.at("#OfModels").is_number_integer()) {
        modelsCount = unit.at("#OfModels").get<int>();
      }
      if (id == 0 && strcmp(toLower(unit.at("Army").get<std::string>()).data(), toLower(modelClass.substr(1, modelClass.length())).data()) == 0) {
        modelUnits.push_back({unit.at("Name").get<std::string>(), modelClass.substr(1, modelClass.length()),
                              modelsCount, RosterModel::generateInstanceId()});
        return true;
      } else if (id == 1 && strcmp(toLower(unit.at("Army").get<std::string>()).data(), toLower(enemyClass.substr(1, enemyClass.length())).data()) == 0) {
        enemyUnits.push_back({unit.at("Name").get<std::string>(), enemyClass.substr(1, enemyClass.length()),
                              modelsCount, RosterModel::generateInstanceId()});
        return true;
      }
    }
  }
  return false;
}

void Form :: savetoTxt(const std::vector<RosterEntry>& enemyUnits, const std::vector<RosterEntry>& modelUnits) {

  std::ofstream outfile("units.txt");
  outfile << "Player Units\n";
  for (const auto& entry : enemyUnits) {
    outfile << entry.name << "|" << entry.modelsCount;
    if (!entry.instanceId.empty()) {
      outfile << "|" << entry.instanceId;
    }
    outfile << std::endl;
  }
  outfile << "Model Units\n";
  for (const auto& entry : modelUnits) {
    outfile << entry.name << "|" << entry.modelsCount;
    if (!entry.instanceId.empty()) {
      outfile << "|" << entry.instanceId;
    }
    outfile << std::endl;
  }
  outfile.close();
}

void Form :: update_metrics() {

  const int IMG_W = 330;
  const int IMG_H = 160;

  auto load_scaled = [&](const std::string& rel) -> Glib::RefPtr<Gdk::Pixbuf> {
    std::string path = "../gui/" + rel;
    if (!fs::exists(path)) {
      return Glib::RefPtr<Gdk::Pixbuf>();
    }
    auto pix = Gdk::Pixbuf::create_from_file(path);
    return pix->scale_simple(IMG_W, IMG_H, Gdk::INTERP_BILINEAR);
  };

  if (auto p = load_scaled(rewpth)) metricBox.set(p);
  if (auto p = load_scaled(losspth)) metricBox2.set(p);
  if (auto p = load_scaled(winratepth)) metricBox4.set(p);
  if (auto p = load_scaled(vpdiffpth)) metricBox5.set(p);
  if (auto p = load_scaled(eplenpth)) metricBox3.set(p);
  if (auto p = load_scaled(endreasonpth)) metricBox6.set(p);

}

void Form :: updateInits(std::string model, std::string enemy) {
  std::string command = "cd .. ; ./data.sh ";
  command.append(setIters.get_text().data());
  command.append(model);
  command.append(enemy);
  command.append(" ");
  command.append(enterDimensX.get_text().data());
  command.append(" ");
  command.append(enterDimensY.get_text().data());
  system(command.data());
}

void Form :: startTrainInBackground() {
  std::thread t(&Form::startTrain, this);
  t.detach();
}

void Form :: startTrain() {
  training = true;
  system("clear");
  const std::string perDefaults = "PER_ENABLED=1 N_STEP=3 TRAIN_LOG_TO_CONSOLE=1 ";
  std::string command = "cd .. ; ";
  command.append(perDefaults);
  command.append(trainEnvPrefix);
  command.append("./train.sh 2>&1");

  trainingTotalEpisodes = parsePositiveInt(setIters.get_text());
  int totalEpisodes = trainingTotalEpisodes;
  resetTrainingProgressStats();
  std::string initialStats = buildTrainingStatsLine(0.0, std::chrono::seconds(0), false,
                                                    std::chrono::seconds(0));
  Glib::signal_idle().connect_once([this, totalEpisodes]() {
    updateTrainingProgress(0, totalEpisodes);
  });
  Glib::signal_idle().connect_once([this, initialStats]() {
    trainingProgressStatsLabel.set_text(initialStats);
  });

  std::string startMessage = "Старт " + trainingStartLabel + ": PER=1, N_STEP=3.";
  Glib::signal_idle().connect_once([this, startMessage]() {
    setStatusMessage(startMessage);
  });
  appendTrainingLogToFile(startMessage, trainingLogTag);

  FILE* pipe = popen(command.c_str(), "r");
  if (!pipe) {
    std::string errorMessage = "Ошибка запуска " + trainingStartLabel
        + " (gui/Application.cpp): проверьте, что train.sh доступен.";
    Glib::signal_idle().connect_once([this, errorMessage]() {
      setStatusMessage(errorMessage);
    });
    appendTrainingLogToFile(errorMessage, trainingLogTag);
    training = false;
    return;
  }

  std::array<char, 512> buffer{};
  int lastEpisode = 0;
  int lastTotal = totalEpisodes;
  while (fgets(buffer.data(), static_cast<int>(buffer.size()), pipe)) {
    std::string line(buffer.data());
    while (!line.empty() && (line.back() == '\n' || line.back() == '\r')) {
      line.pop_back();
    }
    if (line.empty()) {
      continue;
    }
    appendTrainingLogToFile(line, trainingLogTag);
    int currentEpisode = 0;
    int totalFromLine = lastTotal;
    if (parseTrainingProgress(line, lastTotal, currentEpisode, totalFromLine)) {
      if (totalFromLine > 0) {
        lastTotal = totalFromLine;
      }
      if (currentEpisode > 0) {
        lastEpisode = currentEpisode;
      }
      auto now = std::chrono::steady_clock::now();
      recordTrainingSample(currentEpisode, now);
      double rate = calculateTrainingRate();
      auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(now - trainingStartTime);
      bool showEta = (totalFromLine > 0 && rate > 0.0);
      std::chrono::seconds eta(0);
      if (showEta) {
        int remaining = std::max(0, totalFromLine - currentEpisode);
        eta = std::chrono::seconds(static_cast<long long>(remaining / rate));
      }
      std::string statsLine = buildTrainingStatsLine(rate, elapsed, showEta, eta);
      bool shouldUpdate = (now - trainingLastUiUpdate) >= std::chrono::milliseconds(250);
      if (shouldUpdate || (totalFromLine > 0 && currentEpisode >= totalFromLine)) {
        trainingLastUiUpdate = now;
        Glib::signal_idle().connect_once([this, currentEpisode, totalFromLine, statsLine]() {
          updateTrainingProgress(currentEpisode, totalFromLine);
          trainingProgressStatsLabel.set_text(statsLine);
        });
      }
    } else if (!hideTrainingLogs) {
      Glib::signal_idle().connect_once([this, line]() {
        appendLogLine(line);
      });
    }
  }

  int exitCode = pclose(pipe);
  training = false;
  if (lastTotal > 0 && lastEpisode > 0) {
    int finalEpisode = std::min(lastEpisode, lastTotal);
    auto doneElapsed = std::chrono::duration_cast<std::chrono::seconds>(
        std::chrono::steady_clock::now() - trainingStartTime);
    std::string finalStats = buildTrainingStatsLine(calculateTrainingRate(), doneElapsed, false,
                                                    std::chrono::seconds(0));
    Glib::signal_idle().connect_once([this, finalEpisode, lastTotal, finalStats]() {
      updateTrainingProgress(finalEpisode, lastTotal);
      trainingProgressStatsLabel.set_text(finalStats);
    });
  }
  if (exitCode == 0) {
    std::string doneMessage = trainingStatusLabel + " завершено.";
    Glib::signal_idle().connect_once([this, doneMessage]() {
      setStatusMessage(doneMessage);
    });
    appendTrainingLogToFile(doneMessage, trainingLogTag);
    auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(
        std::chrono::steady_clock::now() - trainingStartTime);
    std::string finalStats = trainingStatusLabel + " завершено • elapsed "
        + formatDuration(elapsed);
    Glib::signal_idle().connect_once([this, finalStats]() {
      trainingProgressStatsLabel.set_text(finalStats);
    });
  } else {
    std::string errLine = trainingStatusLabel + " завершено с ошибкой. Код выхода: "
        + std::to_string(exitCode);
    Glib::signal_idle().connect_once([this, errLine]() {
      setStatusMessage(errLine);
    });
    appendTrainingLogToFile(errLine, trainingLogTag);
    auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(
        std::chrono::steady_clock::now() - trainingStartTime);
    std::string finalStats = trainingStatusLabel + " завершено с ошибкой • elapsed "
        + formatDuration(elapsed);
    Glib::signal_idle().connect_once([this, finalStats]() {
      trainingProgressStatsLabel.set_text(finalStats);
    });
  }
  Glib::signal_idle().connect_once([this]() {
    update_metrics();
  });
}

void Form :: runPlayAgainstModelInBackground() {
  std::thread t(&Form::playAgainstModel, this);
  t.detach();
}
  
void Form :: playAgainstModel() {
  path = setModelFile.get_text();

  std::string envPrefix;

  std::string command;

  if (playInGUI == "True") {
    envPrefix = "PLAY_NO_EXPLORATION=1 FIGHT_REPORT=1 ";
    command = "cd .. ; " + envPrefix + "./play.sh ";
    if (strlen(path.data()) < 2) {
      command.append("None");
    } else {
      command.append("\"");
      command.append(path);
      command.append("\"");
    }
    command.append(" True");
  } else {
    // ВАЖНО: "Play in Terminal" теперь откроет новое окно терминала
    command = "cd .. ; " + envPrefix + "./launch_terminal_manual.sh ";
    if (strlen(path.data()) < 2) {
      command.append("None");
    } else {
      command.append("\"");
      command.append(path);
      command.append("\"");
    }
  }

  playing = true;
  system("clear");
  system(command.data());
  playing = false;
}


inline bool Form :: exists_test (const std::string& name) {
  struct stat buffer;   
  return (stat (name.c_str(), &buffer) == 0); 
}
