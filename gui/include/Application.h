#ifndef APP_H
#define APP_H

#include <iostream>
#include <gtkmm.h>
#include <cstdlib>
#include <stdlib.h>
#include <string>
#include <fstream>
#include <thread>
#include <chrono>
#include <filesystem>
#include "popup.h"
#include "units.h"
#include "warn.h"
#include "help.h"

class Form : public Window {

public : 
  Form();
  int openPopUp(bool textMode);
  void update_picture();
  void update_metrics();
  void updateInits(std::string model, std::string enemy);
  void startTrainInBackground();
  void startTrain();
  void runPlayAgainstModelInBackground();
  void playAgainstModel();
  inline bool exists_test (const std::string& name);
  void on_dropdown_changed();
  void savetoTxt(std::vector<std::string> enemyUnits, std::vector<std::string> modelUnits);
  bool isValidUnit(int id, std::string name);
  int openArmyView();
  int openWarnMenu(std::string mess, int comm);
  int openHelpMenu();
  int openPlayGUI();
  void changeMetrics(std::string path);
  void recentMetrics();
  std::string toLower(std::string data);
  void mirrorRoster();
  void saveLastRoster();
  void loadLastRoster();

private:
  std::filesystem::path lastRosterPath() const;
  std::string currentTimestamp() const;
  std::string joinUnits(const std::vector<std::string>& units) const;
  std::vector<std::string> splitUnits(const std::string& text) const;
  void applyFactionToModel(const std::string& faction);
  void applyFactionToEnemy(const std::string& faction);
  Window* boardShow;
  Window* armyView;
  Window* warn;
  Window* play;
  Window* helpMenu;
  Image pictureBox1;
  Image metricBox;
  Image metricBox2;
  Image metricBox3;
Image metricBox4;
Image metricBox5;
Image metricBox6;
  Fixed fixed;
  ScrolledWindow scrolledWindow;
  Notebook tabControl1;
  Label labelPage1;
  Label labelPage2;
  Label labelPage3;
  Label labelPage4;
  Label labelPage5;
  Label label1;
  Frame tabPage1;
  Frame tabPage2;
  Frame tabPage3;
  Frame tabPage4;
  Frame tabPage5;
  RadioButtonGroup radioButtonGroup;
  RadioButton radioTop;
  RadioButton radioLeft;
  RadioButton radioRight;
  RadioButton radioBottom;
  Fixed fixedTabPage1;
  Fixed fixedTabPage2;
  Fixed fixedTabPage3;
  Fixed fixedTabPage4;
  Fixed fixedTabPage5;
  Button button1;
  Button button2;
  Button button3;
  Button button4;
  Button button5;
  Button button6;
  Button showBoard;
  Button showBoardImg;
  Label textbox;
  Label textbox2;
  Label textbox1;
  Label enemyFact;
  Label modelFact;
  Label status;
  Entry setIters;
  Entry setModelFile;
  RadioButtonGroup factionModel;
  RadioButton orksModel;
  RadioButton spmModel;
  RadioButton sobModel;
  RadioButton adcModel;
  RadioButton tyrModel;
  RadioButton milModel;
  RadioButton tauModel;
  RadioButton necModel;
  RadioButtonGroup factionEnemy;
  RadioButton orksEnemy;
  RadioButton spmEnemy;
  RadioButton sobEnemy;
  RadioButton adcEnemy;
  RadioButton tyrEnemy;
  RadioButton milEnemy;
  RadioButton tauEnemy;
  RadioButton necEnemy;
  std::string enemyClass;
  std::string modelClass;
  std::string path;
  std::string foldPath;
  Label numOfGames;
  Label dimens;
  Label dimX;
  Label dimY;
  Entry enterDimensX;
  Entry enterDimensY;
  Button upX;
  Button downX;
  Button upY;
  Button downY;
  Button modelEnter;
  Button enemyEnter;
  Button mirrorRosterButton;
  Button openArmyPopup;
  Entry enterModelUnit;
  Entry enterEnemyUnit;
  Button clearAllModel;
  Button clearAllEnemy;
  int x;
  int y;
  bool open;
  bool training;
  bool playing;
  Label error;
  Label modelUnitLabel;
  Label enemyUnitLabel;
  std::vector<std::string> modelUnits;
  std::vector<std::string> enemyUnits;
  HeaderBar bar;
  Button help;
  Button chooseMetrics;
  Button playGUI;
  Label victoryConditionLabel;
  ComboBoxText victoryConditionSelect;
  std::string forcedVictoryCondition;
  std::string playInGUI;
};

#endif
