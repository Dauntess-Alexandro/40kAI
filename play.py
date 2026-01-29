# play warhammer!

import pickle
import os
import sys
from gym_mod.envs.warhamEnv import *
import warnings
warnings.filterwarnings("ignore")

from model.DQN import *
from model.utils import *
from gym_mod.engine.game_io import ConsoleIO, set_active_io
from gym_mod.engine.deployment import deploy_only_war, post_deploy_setup
from gym_mod.envs.warhamEnv import roll_off_attacker_defender

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

PLAY_EPS = float(os.getenv("PLAY_EPS", "")) if os.getenv("PLAY_EPS") is not None and os.getenv("PLAY_EPS") != "" else None
PLAY_NO_EXPLORATION = os.getenv("PLAY_NO_EXPLORATION", "0") == "1"
if PLAY_NO_EXPLORATION:
    PLAY_EPS = 0.0

if sys.argv[1] == "None":
    savePath = "models/"

    folders = os.listdir(savePath)

    envs = []
    modelpth = []

    for i in folders:
        
        if os.path.isdir(savePath+i):
            fs = os.listdir(savePath+i)
            for j in fs:
                if j[-len(".pickle"):] == ".pickle":
                    envs.append(savePath+i+"/"+j)
                elif j[-len(".pth"):] == ".pth":
                    modelpth.append(savePath+i+"/"+j)

    envs.sort(key=lambda x: os.path.getmtime(x))
    modelpth.sort()

    checkpoint = torch.load(modelpth[-1])

    #print("Playing with environment saved here: ", envs[-1])
    with open(envs[-1], 'rb') as f:
        env, model, enemy = pickle.load(f)
else: 
    #print("Playing with model saved here: ", sys.argv[1])
    with open(sys.argv[1], 'rb') as f:
        env, model, enemy = pickle.load(f)
    f = str(sys.argv[1])
    modelpth = f[:-len("pickle")]+"pth"
    checkpoint = torch.load(modelpth)

playInGUI = False
if sys.argv[2] == "True":
    playInGUI = True

io = ConsoleIO()
set_active_io(io)


def _log(msg: str):
    io.log(msg)


def _uses_dueling(checkpoint_state):
    policy_state = checkpoint_state.get("policy_net", checkpoint_state)
    return any(
        key.startswith("value_heads.") or key.startswith("advantage_heads.")
        for key in policy_state.keys()
    )


verbose = os.getenv("VERBOSE_LOGS", "0") == "1"
log_fn = _log if verbose else None

attacker_side, defender_side = roll_off_attacker_defender(
    manual_roll_allowed=(playInGUI is False),
    log_fn=_log,
)
if verbose:
    _log(f"[MISSION Only War] Attacker={attacker_side}, Defender={defender_side}")
    _log(f"[roster] model_units={len(model)} enemy_units={len(enemy)}")
    for idx, unit in enumerate(model):
        unit_data = unit.showUnitData()
        unit_name = unit_data.get("Name", "Unknown")
        unit_models = unit_data.get("#OfModels", 1)
        instance_id = getattr(unit, "instance_id", "unknown")
        _log(f"[roster] model[{idx}] name={unit_name} instance_id={instance_id} models={unit_models}")
    for idx, unit in enumerate(enemy):
        unit_data = unit.showUnitData()
        unit_name = unit_data.get("Name", "Unknown")
        unit_models = unit_data.get("#OfModels", 1)
        instance_id = getattr(unit, "instance_id", "unknown")
        _log(f"[roster] enemy[{idx}] name={unit_name} instance_id={instance_id} models={unit_models}")
_log(
    "Units: "
    + str(
        [
            (u.name, getattr(u, "instance_id", "unknown"), u.models_count)
            for u in model
        ]
    )
)

deploy_only_war(
    model_units=model,
    enemy_units=enemy,
    b_len=env.unwrapped.b_len,
    b_hei=env.unwrapped.b_hei,
    attacker_side=attacker_side,
    log_fn=log_fn,
)
post_deploy_setup(log_fn=log_fn)

env.attacker_side = attacker_side
env.defender_side = defender_side

state, info = env.reset(m=model, e=enemy)
if verbose:
    squads_for_actions_count = len(model)
    _log(f"[action_space] squads_for_actions_count={squads_for_actions_count}")
    for idx, unit in enumerate(model):
        unit_data = unit.showUnitData()
        unit_name = unit_data.get("Name", "Unknown")
        _log(f"[action_space] squad[{idx}] name={unit_name}")
    total_models_count = 0
    for unit in model:
        unit_data = unit.showUnitData()
        total_models_count += int(unit_data.get("#OfModels", 1))
    _log(f"[action_space] total_models_count={total_models_count}")
    move_num_keys = [
        key for key in env.action_space.spaces.keys() if key.startswith("move_num_")
    ]
    _log(f"[action_space] move_num_keys_count={len(move_num_keys)}")
    _log(f"[action_space] move_num_keys={sorted(move_num_keys)}")
n_actions = [5,2,len(info["player health"]), len(info["player health"]), 5, len(info["model health"])]
for i in range(len(model)):
    n_actions.append(12)
n_observations = len(state)

dueling = _uses_dueling(checkpoint)
if dueling:
    io.log("Модель обучена в dueling-режиме — запускаем dueling-сеть.")
else:
    io.log("Модель обучена в обычном режиме — запускаем обычную сеть.")

policy_net = DQN(n_observations, n_actions, dueling=dueling).to(device)
target_net = DQN(n_observations, n_actions, dueling=dueling).to(device)
optimizer = torch.optim.Adam(policy_net.parameters())

policy_net.load_state_dict(checkpoint['policy_net'])
target_net.load_state_dict(checkpoint['target_net'])
optimizer.load_state_dict(checkpoint['optimizer'])

policy_net.eval()
target_net.eval()

isdone = False
i = 0

if playInGUI == True:
    env.reset(m=model, e=enemy, playType=playInGUI, Type="big", trunc=True)
else:
    env.reset(m=model, e=enemy, playType=playInGUI, Type="big", trunc=False)

env.io = io

reward = 0
io.log("\nИнструкции:\n")
io.log("Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.)")
io.log("Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.)\n")

while isdone == False:
    done, info = env.unwrapped.player()
    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    shoot_mask = build_shoot_action_mask(env)
    if PLAY_EPS is not None:
        action = select_action_with_epsilon(
            env,
            state,
            policy_net,
            PLAY_EPS,
            len(model),
            shoot_mask=shoot_mask,
        )
    else:
        action = select_action(env, state, i, policy_net, len(model), shoot_mask=shoot_mask)
    action_dict = convertToDict(action)
    if done != True:
        next_observation, reward, done, _, info = env.step(action_dict)
        reward = torch.tensor([reward], device=device)
        unit_health = info["model health"]
        enemy_health = info["player health"]
        inAttack = info["in attack"]

        board = env.render()
        message = "Iteration {} ended with reward {}, Player health {}, Model health {}".format(i, reward, enemy_health, unit_health)
        io.log(message)
        next_state = torch.tensor(next_observation, dtype=torch.float32, device=device).unsqueeze(0)
        state = next_state
    if done == True:
        if reward > 0:
            io.log("Модель победила!")
        else:
            io.log("Вы победили!")
        isdone = True
    i+=1
