# play warhammer!
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

import pickle
import os
import sys
from gym_mod.envs.warhamEnv import *
import warnings
warnings.filterwarnings("ignore")

from model.DQN import *
from model.utils import normalize_state_dict
from model.utils import *
from gym_mod.engine.game_io import ConsoleIO, set_active_io
from gym_mod.engine.deployment import deploy_only_war, post_deploy_setup
from gym_mod.envs.warhamEnv import roll_off_attacker_defender
from gym_mod.engine.agent_registry import compatible_contracts, load_agent_by_id, make_env_contract


def load_trusted_checkpoint(path: str):
    """Загрузка доверенного checkpoint для PyTorch>=2.6 (weights_only=False)."""
    return torch.load(path, weights_only=False)


PLAY_EPS = float(os.getenv("PLAY_EPS", "")) if os.getenv("PLAY_EPS") is not None and os.getenv("PLAY_EPS") != "" else None
PLAY_NO_EXPLORATION = os.getenv("PLAY_NO_EXPLORATION", "0") == "1"
if PLAY_NO_EXPLORATION:
    PLAY_EPS = 0.0

parser = argparse.ArgumentParser()
parser.add_argument("model", nargs="?", default="None")
parser.add_argument("play_in_gui", nargs="?", default="False")
parser.add_argument("--agent-id", default=os.getenv("PLAY_AGENT_ID", "").strip())
args = parser.parse_args()

if args.model == "None":
    savePath = "models/"
    folders = os.listdir(savePath) if os.path.isdir(savePath) else []
    envs = []
    modelpth = []
    for i in folders:
        full_dir = os.path.join(savePath, i)
        if os.path.isdir(full_dir):
            fs = os.listdir(full_dir)
            for j in fs:
                full_path = os.path.join(full_dir, j)
                if j.endswith(".pickle"):
                    envs.append(full_path)
                elif j.endswith(".pth"):
                    modelpth.append(full_path)
    if not envs or not modelpth:
        raise FileNotFoundError("Не найдены legacy модели в models/. Что делать: укажите --agent-id или путь к .pickle.")
    envs.sort(key=lambda x: os.path.getmtime(x))
    modelpth.sort()
    checkpoint = load_trusted_checkpoint(modelpth[-1])
    with open(envs[-1], "rb") as f:
        env, model, enemy = pickle.load(f)
else:
    with open(args.model, "rb") as f:
        env, model, enemy = pickle.load(f)
    modelpth = str(args.model)[:-len("pickle")] + "pth"
    checkpoint = load_trusted_checkpoint(modelpth)

playInGUI = str(args.play_in_gui).strip().lower() == "true"

io = ConsoleIO()
set_active_io(io)


def _log(msg: str):
    io.log(msg)


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

state, info = env.reset(options={"m": model, "e": enemy})
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
if args.agent_id:
    agent_payload = load_agent_by_id(args.agent_id)
    runtime_contract = make_env_contract(
        n_observations=n_observations,
        n_actions=n_actions,
        mission_name=str(getattr(env.unwrapped, "mission_name", "only_war")),
        ruleset_version=str(os.getenv("RULESET_VERSION", "only_war_v1")),
    )
    ok, reason = compatible_contracts(runtime_contract, agent_payload.get("contract", {}))
    if not ok:
        raise ValueError(
            f"Несовместимый --agent-id={args.agent_id}: {reason}. "
            "Что делать: выберите агента с тем же ruleset/action/obs контрактом."
        )
    checkpoint = {
        "policy_net": agent_payload.get("policy_state"),
        "target_net": agent_payload.get("target_state") or agent_payload.get("policy_state"),
        "optimizer": agent_payload.get("optimizer_state") or {},
        "net_type": "dueling" if any(str(k).startswith("value_heads.") for k in (agent_payload.get("policy_state") or {}).keys()) else "basic",
    }
    _log(f"[LEAGUE] Используется agent-id={args.agent_id} из registry.")

net_type = checkpoint.get("net_type") if isinstance(checkpoint, dict) else None
dueling = net_type == "dueling"
if not dueling and isinstance(checkpoint, dict):
    policy_state = checkpoint.get("policy_net", {})
    if any(key.startswith("value_heads.") for key in policy_state):
        dueling = True

policy_net = DQN(n_observations, n_actions, dueling=dueling).to(device)
target_net = DQN(n_observations, n_actions, dueling=dueling).to(device)
optimizer = torch.optim.Adam(policy_net.parameters())

policy_net.load_state_dict(normalize_state_dict(checkpoint['policy_net']))
target_net.load_state_dict(normalize_state_dict(checkpoint['target_net']))
if isinstance(checkpoint.get("optimizer"), dict) and checkpoint["optimizer"]:
    optimizer.load_state_dict(checkpoint["optimizer"])

policy_net.eval()
target_net.eval()

isdone = False
i = 0

if playInGUI == True:
    env.reset(options={"m": model, "e": enemy, "playType": playInGUI, "Type": "big", "trunc": True})
else:
    env.reset(options={"m": model, "e": enemy, "playType": playInGUI, "Type": "big", "trunc": False})

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
