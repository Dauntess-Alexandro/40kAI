#pragma once

#include "app_state.h"
#include "play_state.h"
#include "train_state.h"

void RenderCommandPanel(AppState& state);
void RenderSettingsPanel(AppState& state);
void RenderPlayPanel(PlayState& state);
void RenderTrainPanel(TrainState& state);
