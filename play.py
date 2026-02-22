# play warhammer!
import os
import pickle
import sys

import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

from gym_mod.engine import Unit, initFile, unitData, weaponData
from gym_mod.engine.deployment import deploy_only_war, post_deploy_setup
from gym_mod.engine.game_io import ConsoleIO, set_active_io
from gym_mod.engine.mission import board_dims_for_mission, normalize_mission_name
from gym_mod.envs.warhamEnv import roll_off_attacker_defender
from model.DQN import DQN
from model.alphazero import canonical_action_keys, flatten_observation, load_alphazero_checkpoint, to_action_dict
from model.utils import *
from model.utils import normalize_state_dict

PLAY_EPS = float(os.getenv("PLAY_EPS", "")) if os.getenv("PLAY_EPS") not in (None, "") else None
if os.getenv("PLAY_NO_EXPLORATION", "0") == "1":
    PLAY_EPS = 0.0


def _load_roster_config():
    default_mission = "only_war"
    config = {
        "b_len": 40,
        "b_hei": 60,
        "mission": default_mission,
        "enemy_faction": "Necrons",
        "model_faction": "Necrons",
        "enemy_units": [
            {"name": "Necron Warriors", "weapons": ("Gauss flayer", "Necron close combat weapon"), "count": None, "instance_id": None},
            {"name": "Royal Warden", "weapons": ("Relic gauss blaster", "Royal warden close combat weapon"), "count": None, "instance_id": None},
        ],
        "model_units": [
            {"name": "Necron Warriors", "weapons": ("Gauss flayer", "Necron close combat weapon"), "count": None, "instance_id": None},
            {"name": "Royal Warden", "weapons": ("Relic gauss blaster", "Royal warden close combat weapon"), "count": None, "instance_id": None},
        ],
    }
    if os.path.isfile("gui/data.json"):
        config["b_len"] = initFile.getBoardX()
        config["b_hei"] = initFile.getBoardY()
        config["enemy_faction"] = initFile.getEnemyFaction()
        config["model_faction"] = initFile.getModelFaction()
        config["mission"] = normalize_mission_name(getattr(initFile, "getMission", lambda: default_mission)())
        enemy_counts = initFile.getEnemyUnitCounts()
        model_counts = initFile.getModelUnitCounts()
        enemy_ids = initFile.getEnemyUnitInstanceIds()
        model_ids = initFile.getModelUnitInstanceIds()
        config["enemy_units"] = [
            {"name": initFile.getEnemyUnits()[i], "weapons": (initFile.getEnemyW()[i][0], initFile.getEnemyW()[i][1]), "count": enemy_counts[i] if i < len(enemy_counts) and enemy_counts[i] > 0 else None, "instance_id": enemy_ids[i] if i < len(enemy_ids) else None}
            for i in range(len(initFile.getEnemyUnits()))
        ]
        config["model_units"] = [
            {"name": initFile.getModelUnits()[i], "weapons": (initFile.getModelW()[i][0], initFile.getModelW()[i][1]), "count": model_counts[i] if i < len(model_counts) and model_counts[i] > 0 else None, "instance_id": model_ids[i] if i < len(model_ids) else None}
            for i in range(len(initFile.getModelUnits()))
        ]
    config["mission"] = normalize_mission_name(config.get("mission", os.getenv("MISSION_NAME", default_mission)))
    config["b_len"], config["b_hei"] = board_dims_for_mission(config["mission"])
    return config


def _build_units_from_config(config, b_len, b_hei):
    enemy, model = [], []
    for spec in config["enemy_units"]:
        u = unitData(config["enemy_faction"], spec["name"])
        if spec["count"]:
            u["#OfModels"] = spec["count"]
        enemy.append(Unit(u, weaponData(spec["weapons"][0]), weaponData(spec["weapons"][1]), b_len, b_hei, instance_id=spec["instance_id"]))
    for spec in config["model_units"]:
        u = unitData(config["model_faction"], spec["name"])
        if spec["count"]:
            u["#OfModels"] = spec["count"]
        model.append(Unit(u, weaponData(spec["weapons"][0]), weaponData(spec["weapons"][1]), b_len, b_hei, instance_id=spec["instance_id"]))
    return enemy, model


def _load_play_artifacts(model_arg):
    if model_arg == "None":
        save_path = "models"
        candidates = []
        for root, _, files in os.walk(save_path):
            for name in files:
                if name.endswith(".pickle"):
                    candidates.append(os.path.join(root, name))
        if not candidates:
            raise FileNotFoundError("Не найдено моделей .pickle в папке models/")
        candidates.sort(key=lambda x: os.path.getmtime(x))
        pickle_path = candidates[-1]
    else:
        pickle_path = model_arg

    with open(pickle_path, "rb") as f:
        payload = pickle.load(f)

    if isinstance(payload, dict) and payload.get("agent_type") == "alphazero":
        checkpoint_path = payload.get("checkpoint") or f"{os.path.splitext(pickle_path)[0]}.pth"
        if not os.path.exists(checkpoint_path):
            raise FileNotFoundError(f"Не найден checkpoint AlphaZero: {checkpoint_path}")
        roster = _load_roster_config()
        enemy, model = _build_units_from_config(roster, roster["b_len"], roster["b_hei"])
        import gymnasium as gym
        import gym_mod  # noqa: F401
        env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=roster["b_len"], b_hei=roster["b_hei"])
        return env, model, enemy, checkpoint_path, "alphazero"

    modelpth = f"{os.path.splitext(pickle_path)[0]}.pth"
    if not os.path.exists(modelpth):
        raise FileNotFoundError(f"Не найден checkpoint DQN: {modelpth}")
    env, model, enemy = payload
    return env, model, enemy, modelpth, "dqn"


playInGUI = sys.argv[2] == "True"
env, model, enemy, checkpoint_path, agent_type = _load_play_artifacts(sys.argv[1])

io = ConsoleIO()
set_active_io(io)


def _log(msg: str):
    io.log(msg)


verbose = os.getenv("VERBOSE_LOGS", "0") == "1"
log_fn = _log if verbose else None

attacker_side, defender_side = roll_off_attacker_defender(manual_roll_allowed=(playInGUI is False), log_fn=_log)
if verbose:
    _log(f"[MISSION Only War] Attacker={attacker_side}, Defender={defender_side}")

deploy_only_war(model_units=model, enemy_units=enemy, b_len=env.unwrapped.b_len, b_hei=env.unwrapped.b_hei, attacker_side=attacker_side, log_fn=log_fn)
post_deploy_setup(log_fn=log_fn)
env.attacker_side = attacker_side
env.defender_side = defender_side

state, info = env.reset(options={"m": model, "e": enemy})

if agent_type == "alphazero":
    policy_net, _ = load_alphazero_checkpoint(checkpoint_path, device=device)
    policy_net = policy_net.to(device)
    policy_net.eval()
else:
    checkpoint = torch.load(checkpoint_path)
    n_actions = [5, 2, len(info["player health"]), len(info["player health"]), 5, len(info["model health"])]
    for _ in range(len(model)):
        n_actions.append(12)
    n_observations = len(state)
    net_type = checkpoint.get("net_type") if isinstance(checkpoint, dict) else None
    dueling = net_type == "dueling"
    if not dueling and isinstance(checkpoint, dict):
        policy_state = checkpoint.get("policy_net", {})
        if any(key.startswith("value_heads.") for key in policy_state):
            dueling = True
    policy_net = DQN(n_observations, n_actions, dueling=dueling).to(device)
    policy_net.load_state_dict(normalize_state_dict(checkpoint["policy_net"]))
    policy_net.eval()

if playInGUI:
    env.reset(options={"m": model, "e": enemy, "playType": playInGUI, "Type": "big", "trunc": True})
else:
    env.reset(options={"m": model, "e": enemy, "playType": playInGUI, "Type": "big", "trunc": False})

env.io = io
io.log("\nИнструкции:\n")
io.log("Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.)")
io.log("Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.)\n")

isdone = False
i = 0
reward = 0

while not isdone:
    done, info = env.unwrapped.player()
    shoot_mask = build_shoot_action_mask(env)

    if agent_type == "alphazero":
        logits, _ = policy_net(flatten_observation(state).to(device))
        action_keys = canonical_action_keys(env.action_space)
        action_vals = []
        for head_idx, head_logits in enumerate(logits):
            head = head_logits.squeeze(0)
            if head_idx == 2 and shoot_mask is not None:
                mask = torch.as_tensor(shoot_mask, dtype=torch.bool, device=head.device)
                if mask.numel() == head.numel() and mask.any():
                    masked = head.clone()
                    masked[~mask] = -1e9
                    action_vals.append(int(masked.argmax().item()))
                    continue
            action_vals.append(int(head.argmax().item()))
        action_dict = to_action_dict(action_keys, tuple(action_vals))
    else:
        state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        if PLAY_EPS is not None:
            action = select_action_with_epsilon(env, state_tensor, policy_net, PLAY_EPS, len(model), shoot_mask=shoot_mask)
        else:
            action = select_action(env, state_tensor, i, policy_net, len(model), shoot_mask=shoot_mask)
        action_dict = convertToDict(action)

    if not done:
        next_observation, reward, done, _, info = env.step(action_dict)
        reward = torch.tensor([reward], device=device)
        io.log(f"Iteration {i} ended with reward {reward}, Player health {info['player health']}, Model health {info['model health']}")
        state = torch.tensor(next_observation, dtype=torch.float32).tolist() if isinstance(next_observation, torch.Tensor) else next_observation
    if done:
        io.log("Модель победила!" if reward > 0 else "Вы победили!")
        isdone = True
    i += 1
