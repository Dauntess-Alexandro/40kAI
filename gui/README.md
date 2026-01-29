# Application Guide

## Instructions

When you open the app you'll be greeted to something like the image below:
<p align="center">
  <img src="../assets/home_app.png" width=400/>
  <br>Figure 1: App on First Glance
</p>
The app has 5 tabs that are called "Training", "Model Metrics", "Play", "Settings", and "Оценка".

In Figure 1 the "Train" tab is open. Its function is to be used to generate models to play against later. In the textbox the user has to input the number of games the model is trained for. Training for at least 100 games is suggested. Below it are some checkboxes. The top ones are for choosing the faction the trained model will have and the bottom ones are for choosing the faction the model will be trained against. Below that the user can add units to the model's and their armies. The Add button adds the unit and the Clear button deletes all of the units from either army. Below that the dimensions of the game board can be entered. Has 60 by 40 by default. The bottom two buttons are for deleting all of the files saved in the /40kAI/models/ directory and to start the training process. 

<p align="center">
    <img src="../assets/play.png" width=400>
    <br>Figure 2: "Play" section in the app
</p>

Figure 2 shows the "Play" tab of the app. The user selects a model file with the "Choose" button and then plays a game against said model with the "Play" button. It will be played in the terminal and the board will be visible from the popup from the "Show Board" button board.txt.

<p align="center">
    <img src="../assets/Settings.png" width=400>
    <br>Figure 3: Settings page
</p>

The "Settings" page shown above does not show much at the moment, but currently it allows the user to change the orientation of the tabs. 

## Compile

```bash
$ cd gui/build
$ cmake ..
$ cmake --build . --config Debug
```
