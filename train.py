from collections import Counter
import sys
import os
import csv
import numpy as np
import gymnasium as gym
import pickle
import datetime
import collections
import math
import json
import random
import matplotlib.pyplot as plt
from tqdm import tqdm
from gym_mod.envs.warhamEnv import *
from gym_mod.engine import genDisplay, Unit, unitData, weaponData, initFile, metrics
from gym_mod.engine.deployment import deploy_only_war, post_deploy_setup
from gymnasium import spaces

from model.DQN import *
from model.memory import *
from model.utils import *

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
import torch
print("[DEVICE CHECK] cuda:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("[DEVICE CHECK] name:", torch.cuda.get_device_name(0))


import warnings
warnings.filterwarnings("ignore") 

with open(os.path.abspath("hyperparams.json")) as j:
    data = json.loads(j.read())

# ===== algo flags =====
DOUBLE_DQN_ENABLED = os.getenv("DOUBLE_DQN_ENABLED", "1") == "1"
DUELING_ENABLED = os.getenv("DUELING_ENABLED", "1") == "1"
REWARD_DEBUG = os.getenv("REWARD_DEBUG", "0") == "1"
REWARD_DEBUG_EVERY = int(os.getenv("REWARD_DEBUG_EVERY", "200"))
# ===== train logging =====
TRAIN_LOG_ENABLED = os.getenv("TRAIN_LOG_ENABLED", "1") == "1"
TRAIN_LOG_EVERY_UPDATES = int(os.getenv("TRAIN_LOG_EVERY_UPDATES", "200"))
TRAIN_LOG_TO_FILE = os.getenv("TRAIN_LOG_TO_FILE", "1") == "1"
TRAIN_LOG_TO_CONSOLE = os.getenv("TRAIN_LOG_TO_CONSOLE", "0") == "1"
TRAIN_DEBUG = os.getenv("TRAIN_DEBUG", "0") == "1"
if TRAIN_LOG_EVERY_UPDATES < 1:
    TRAIN_LOG_EVERY_UPDATES = 1
if TRAIN_DEBUG:
    TRAIN_LOG_EVERY_UPDATES = min(TRAIN_LOG_EVERY_UPDATES, 50)
# =========================
# ===== per + n-step =====
PER_ENABLED = os.getenv("PER_ENABLED", "1") == "1"
PER_ALPHA = float(os.getenv("PER_ALPHA", "0.6"))
PER_BETA_START = float(os.getenv("PER_BETA_START", "0.4"))
PER_BETA_FRAMES = int(os.getenv("PER_BETA_FRAMES", "200000"))
PER_EPS = float(os.getenv("PER_EPS", "1e-6"))
N_STEP = int(os.getenv("N_STEP", "3"))
if N_STEP < 1:
    N_STEP = 1
# ======================

# ===== perf knobs =====
RENDER_EVERY = int(os.getenv("RENDER_EVERY", "20"))  # 0 = выключить рендер полностью
UPDATES_PER_STEP = int(os.getenv("UPDATES_PER_STEP", "4"))  
# ======================

# ===== self-play config =====
SELF_PLAY_ENABLED = os.getenv("SELF_PLAY_ENABLED", "0") == "1"
SELF_PLAY_UPDATE_EVERY_EPISODES = int(os.getenv("SELF_PLAY_UPDATE_EVERY_EPISODES", "50"))
SELF_PLAY_OPPONENT_MODE = os.getenv("SELF_PLAY_OPPONENT_MODE", "snapshot")
SELF_PLAY_FIXED_PATH = os.getenv("SELF_PLAY_FIXED_PATH", "")
SELF_PLAY_OPPONENT_EPSILON = float(os.getenv("SELF_PLAY_OPPONENT_EPSILON", "0.0"))

if SELF_PLAY_UPDATE_EVERY_EPISODES < 1:
    SELF_PLAY_UPDATE_EVERY_EPISODES = 1
if SELF_PLAY_OPPONENT_MODE not in ("snapshot", "fixed_checkpoint"):
    raise ValueError(
        "SELF_PLAY_OPPONENT_MODE должен быть 'snapshot' или 'fixed_checkpoint'. "
        f"Получено: {SELF_PLAY_OPPONENT_MODE}"
    )
# ============================


DEFAULT_MISSION_NAME = "only_war"

def to_np_state(s):
    if isinstance(s, (dict, collections.OrderedDict)):
        return np.array(list(s.values()), dtype=np.float32)
    return np.array(s, dtype=np.float32)

def build_n_step_transition(buffer, gamma):
    reward_sum = 0.0
    next_state = None
    next_shoot_mask = None
    n_step = 0
    for idx, (_, _, reward, next_state_candidate, done_flag, next_shoot_mask_candidate) in enumerate(buffer):
        reward_sum += (gamma ** idx) * reward
        n_step += 1
        next_state = next_state_candidate
        next_shoot_mask = next_shoot_mask_candidate
        if done_flag:
            next_state = None
            next_shoot_mask = None
            break
    return reward_sum, next_state, next_shoot_mask, n_step

def select_action_with_epsilon(env, state, policy_net, epsilon, len_model, shoot_mask=None):
    sample = random.random()
    dev = next(policy_net.parameters()).device

    if isinstance(state, collections.OrderedDict):
        state = np.array(list(state.values()), dtype=np.float32)
    elif isinstance(state, np.ndarray):
        state = state.astype(np.float32, copy=False)

    if not torch.is_tensor(state):
        state = torch.tensor(state, dtype=torch.float32, device=dev)
    else:
        state = state.to(dev)

    if state.dim() == 1:
        state = state.unsqueeze(0)

    if sample > epsilon:
        with torch.no_grad():
            decision = policy_net(state)
            action = []
            for head_idx, head in enumerate(decision):
                head = head.squeeze(0)
                if head_idx == 2 and shoot_mask is not None:
                    mask = torch.as_tensor(shoot_mask, dtype=torch.bool, device=head.device)
                    if mask.numel() == head.numel() and mask.any():
                        masked_head = head.clone()
                        masked_head[~mask] = -1e9
                        action.append(int(masked_head.argmax().item()))
                        continue
                action.append(int(head.argmax().item()))
            return torch.tensor([action], device="cpu")
    sampled_action = env.action_space.sample()
    shoot_choice = sampled_action["shoot"]
    if shoot_mask is not None:
        mask = torch.as_tensor(shoot_mask, dtype=torch.bool)
        valid_indices = torch.where(mask)[0].tolist()
        if valid_indices:
            shoot_choice = random.choice(valid_indices)
    action_list = [
        sampled_action["move"],
        sampled_action["attack"],
        shoot_choice,
        sampled_action["charge"],
        sampled_action["use_cp"],
        sampled_action["cp_on"],
    ]
    for i in range(len_model):
        label = "move_num_"+str(i)
        action_list.append(sampled_action[label])
    action = torch.tensor([action_list], device="cpu")
    return action


def moving_avg(values, window=50):
    if len(values) == 0:
        return []
    w = max(1, int(window))
    out = []
    for i in range(len(values)):
        j0 = max(0, i - w + 1)
        chunk = values[j0:i+1]
        out.append(sum(chunk) / len(chunk))
    return out

def save_extra_metrics(run_id: str, ep_rows: list[dict], metrics_dir="metrics"):
    os.makedirs(metrics_dir, exist_ok=True)
    os.makedirs("gui/img", exist_ok=True)

    # --- CSV ---
    csv_path = os.path.join(metrics_dir, f"stats_{run_id}.csv")
    cols = ["episode", "ep_reward", "ep_len", "turn", "model_vp", "player_vp", "vp_diff", "result", "end_reason", "end_code"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in ep_rows:
            w.writerow({k: r.get(k, "") for k in cols})

    wins01 = [1 if r["result"] == "win" else 0 for r in ep_rows]
    vp_diff = [r["vp_diff"] for r in ep_rows]
    ep_idx = list(range(1, len(ep_rows) + 1))

    # --- Winrate plot ---
    winrate_ma = moving_avg(wins01, window=50)
    plt.figure()
    plt.plot(ep_idx, winrate_ma)
    plt.xlabel("Episodes")
    plt.ylabel("Winrate (MA 50)")
    plt.title("Winrate (moving average)")
    plt.ylim(-0.05, 1.05)

    plt.savefig(os.path.join(metrics_dir, f"winrate_{run_id}.png"))
    plt.savefig(os.path.join("gui/img", f"winrate_{run_id}.png"))
    plt.savefig(os.path.join("gui/img", "winrate.png"))
    plt.close()

    # --- VP diff plot ---
    vp_ma = moving_avg(vp_diff, window=50)
    plt.figure()
    plt.plot(ep_idx, vp_diff)
    plt.plot(ep_idx, vp_ma)
    plt.xlabel("Episodes")
    plt.ylabel("VP diff (model - player)")
    plt.title("VP diff (per episode + MA 50)")

    plt.savefig(os.path.join(metrics_dir, f"vpdiff_{run_id}.png"))
    plt.savefig(os.path.join("gui/img", f"vpdiff_{run_id}.png"))
    plt.savefig(os.path.join("gui/img", "vpdiff.png"))
    plt.close()

    # --- End reasons bar ---
    reasons = [r["end_reason"] for r in ep_rows]
    c = Counter(reasons)
    keys = sorted(c.keys())
    vals = [c[k] for k in keys]

    plt.figure()
    plt.bar(keys, vals)
    plt.xticks(rotation=30, ha="right")
    plt.ylabel("Count")
    plt.title("End reasons")
    plt.tight_layout()

    plt.savefig(os.path.join(metrics_dir, f"endreasons_{run_id}.png"))
    plt.savefig(os.path.join("gui/img", f"endreasons_{run_id}.png"))
    plt.savefig(os.path.join("gui/img", "endreasons.png"))
    plt.close()

    print(f"[metrics] saved: {csv_path}")

def append_agent_log(line: str) -> None:
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LOGS_FOR_AGENTS.md")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_line = f"{timestamp} | {line}"
    try:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(full_line + "\n")
    except Exception as exc:
        print(f"[LOG][WARN] Не удалось записать LOGS_FOR_AGENTS.md: {exc}")

def _load_roster_config():
    config = {
        "totLifeT": 10,
        "b_len": 60,
        "b_hei": 40,
        "enemy_faction": "Space_Marine",
        "model_faction": "Space_Marine",
        "enemy_units": [
            {
                "name": "Eliminator Squad",
                "weapons": ("Bolt Pistol", "Close combat weapon"),
                "count": None,
                "instance_id": None,
            },
            {
                "name": "Apothecary",
                "weapons": ("Absolver Bolt Pistol", "Close combat weapon"),
                "count": None,
                "instance_id": None,
            },
        ],
        "model_units": [
            {
                "name": "Eliminator Squad",
                "weapons": ("Bolt Pistol", "Close combat weapon"),
                "count": None,
                "instance_id": None,
            },
            {
                "name": "Apothecary",
                "weapons": ("Absolver Bolt Pistol", "Close combat weapon"),
                "count": None,
                "instance_id": None,
            },
        ],
    }

    if os.path.isfile("gui/data.json"):
        config["totLifeT"] = initFile.getNumLife()
        config["b_len"] = initFile.getBoardX()
        config["b_hei"] = initFile.getBoardY()
        config["enemy_faction"] = initFile.getEnemyFaction()
        config["model_faction"] = initFile.getModelFaction()
        enemy_counts = initFile.getEnemyUnitCounts()
        model_counts = initFile.getModelUnitCounts()
        enemy_instance_ids = initFile.getEnemyUnitInstanceIds()
        model_instance_ids = initFile.getModelUnitInstanceIds()

        enemy_units = []
        for i in range(len(initFile.getEnemyUnits())):
            count = enemy_counts[i] if i < len(enemy_counts) and enemy_counts[i] > 0 else None
            instance_id = enemy_instance_ids[i] if i < len(enemy_instance_ids) else None
            enemy_units.append(
                {
                    "name": initFile.getEnemyUnits()[i],
                    "weapons": (initFile.getEnemyW()[i][0], initFile.getEnemyW()[i][1]),
                    "count": count,
                    "instance_id": instance_id,
                }
            )

        model_units = []
        for i in range(len(initFile.getModelUnits())):
            count = model_counts[i] if i < len(model_counts) and model_counts[i] > 0 else None
            instance_id = model_instance_ids[i] if i < len(model_instance_ids) else None
            model_units.append(
                {
                    "name": initFile.getModelUnits()[i],
                    "weapons": (initFile.getModelW()[i][0], initFile.getModelW()[i][1]),
                    "count": count,
                    "instance_id": instance_id,
                }
            )

        config["enemy_units"] = enemy_units
        config["model_units"] = model_units

    return config

def _build_units_from_config(config, b_len, b_hei):
    enemy = []
    model = []
    for spec in config["enemy_units"]:
        unit_data = unitData(config["enemy_faction"], spec["name"])
        if spec["count"]:
            unit_data["#OfModels"] = spec["count"]
        enemy.append(
            Unit(
                unit_data,
                weaponData(spec["weapons"][0]),
                weaponData(spec["weapons"][1]),
                b_len,
                b_hei,
                instance_id=spec["instance_id"],
            )
        )
    for spec in config["model_units"]:
        unit_data = unitData(config["model_faction"], spec["name"])
        if spec["count"]:
            unit_data["#OfModels"] = spec["count"]
        model.append(
            Unit(
                unit_data,
                weaponData(spec["weapons"][0]),
                weaponData(spec["weapons"][1]),
                b_len,
                b_hei,
                instance_id=spec["instance_id"],
            )
        )
    return enemy, model

def _select_actions_batch(env_contexts, states, steps_done, policy_net, shoot_masks=None):
    decay_steps = max(1.0, float(EPS_DECAY))
    progress = min(float(steps_done) / decay_steps, 1.0)
    eps_threshold = EPS_START + (EPS_END - EPS_START) * progress

    dev = next(policy_net.parameters()).device
    state_tensors = []
    for state in states:
        if isinstance(state, (dict, collections.OrderedDict)):
            arr = np.array(list(state.values()), dtype=np.float32)
        else:
            arr = np.array(state, dtype=np.float32)
        state_tensors.append(torch.tensor(arr, dtype=torch.float32, device=dev))
    state_batch = torch.stack(state_tensors, dim=0)

    actions = []
    with torch.no_grad():
        decision = policy_net(state_batch)

    for env_idx, ctx in enumerate(env_contexts):
        env = ctx["env"]
        len_model = ctx["len_model"]
        use_random = random.random() <= eps_threshold
        if use_random:
            sampled_action = env.action_space.sample()
            shoot_choice = sampled_action["shoot"]
            if shoot_masks and shoot_masks[env_idx] is not None:
                mask = torch.as_tensor(shoot_masks[env_idx], dtype=torch.bool)
                valid_indices = torch.where(mask)[0].tolist()
                if valid_indices:
                    shoot_choice = random.choice(valid_indices)
            action_list = [
                sampled_action["move"],
                sampled_action["attack"],
                shoot_choice,
                sampled_action["charge"],
                sampled_action["use_cp"],
                sampled_action["cp_on"],
            ]
            for i in range(len_model):
                label = "move_num_" + str(i)
                action_list.append(sampled_action[label])
            actions.append(torch.tensor([action_list], device="cpu"))
        else:
            action = []
            for head_idx, head in enumerate(decision):
                head_row = head[env_idx]
                if head_idx == 2 and shoot_masks and shoot_masks[env_idx] is not None:
                    mask = torch.as_tensor(shoot_masks[env_idx], dtype=torch.bool, device=head_row.device)
                    if mask.numel() == head_row.numel() and mask.any():
                        masked_head = head_row.clone()
                        masked_head[~mask] = -1e9
                        action.append(int(masked_head.argmax().item()))
                        continue
                action.append(int(head_row.argmax().item()))
            actions.append(torch.tensor([action], device="cpu"))
    return actions, eps_threshold

TAU = data["tau"]
LR = data["lr"]
GAMMA = data["gamma"]
NET_TYPE = "dueling" if DUELING_ENABLED else "basic"
CLIP_REWARD = os.getenv("CLIP_REWARD", "off")
GRAD_CLIP_VALUE = 100.0

# ============================================================
# (C) Несколько обучающих апдейтов на один шаг среды
# ============================================================
UPDATES_PER_STEP = int(data.get("updates_per_step", 1))  # 1 = как было раньше
WARMUP_STEPS     = int(data.get("warmup_steps", 0))      # 0 = без прогрева

if TRAIN_LOG_ENABLED:
    train_start_line = (
        "[TRAIN][START] "
        f"DoubleDQN={int(DOUBLE_DQN_ENABLED)} "
        f"Dueling={int(DUELING_ENABLED)} "
        f"PER={int(PER_ENABLED)} "
        f"N_STEP={N_STEP} "
        f"LR={LR} "
        f"clip_reward={CLIP_REWARD} "
        f"grad_clip={GRAD_CLIP_VALUE}"
    )
    if TRAIN_LOG_TO_FILE:
        append_agent_log(train_start_line)
    if TRAIN_LOG_TO_CONSOLE:
        print(train_start_line)

print("\nTraining...\n")

end = False
trunc = True

roster_config = _load_roster_config()
totLifeT = roster_config["totLifeT"]
b_len = roster_config["b_len"]
b_hei = roster_config["b_hei"]

vec_env_count = int(os.getenv("VEC_ENV_COUNT", "1"))
if vec_env_count < 1:
    vec_env_count = 1

env_contexts = []

numLifeT = 0

verbose = os.getenv("VERBOSE_LOGS", "0") == "1"
log_fn = print if verbose else None

if os.path.isfile("gui/data.json"):
    print("Model Units:\n")
    for spec in roster_config["model_units"]:
        print("Name:", spec["name"], "Weapons: ", spec["weapons"][0], spec["weapons"][1])
    print("Enemy Units:\n")
    for spec in roster_config["enemy_units"]:
        print("Name:", spec["name"], "Weapons: ", spec["weapons"][0], spec["weapons"][1])

for env_idx in range(vec_env_count):
    enemy, model = _build_units_from_config(roster_config, b_len, b_hei)
    env_log_fn = log_fn if env_idx == 0 else None
    attacker_side, defender_side = roll_off_attacker_defender(
        manual_roll_allowed=False,
        log_fn=print if env_idx == 0 else None,
    )
    if verbose and env_idx == 0:
        print(f"[roster] model_units={len(model)} enemy_units={len(enemy)}")
        for idx, unit in enumerate(model):
            unit_data = unit.showUnitData()
            unit_name = unit_data.get("Name", "Unknown")
            unit_models = unit_data.get("#OfModels", 1)
            print(f"[roster] model[{idx}] name={unit_name} instance_id={unit.instance_id} models={unit_models}")
        for idx, unit in enumerate(enemy):
            unit_data = unit.showUnitData()
            unit_name = unit_data.get("Name", "Unknown")
            unit_models = unit_data.get("#OfModels", 1)
            print(f"[roster] enemy[{idx}] name={unit_name} instance_id={unit.instance_id} models={unit_models}")
        print(f"[MISSION Only War] Attacker={attacker_side}, Defender={defender_side}")
        print("Units:", [(u.name, u.instance_id, u.models_count) for u in model])

    deploy_only_war(
        model_units=model,
        enemy_units=enemy,
        b_len=b_len,
        b_hei=b_hei,
        attacker_side=attacker_side,
        log_fn=env_log_fn,
    )
    post_deploy_setup(log_fn=env_log_fn)

    env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
    env.attacker_side = attacker_side
    env.defender_side = defender_side

    try:
        state, info = env.reset(m=model, e=enemy, trunc=True)
    except TypeError:
        if hasattr(env, "unwrapped") and hasattr(env.unwrapped, "reset"):
            state, info = env.unwrapped.reset(m=model, e=enemy, trunc=True)
        else:
            state, info = env.reset()
    env_contexts.append(
        {
            "env": env,
            "model": model,
            "enemy": enemy,
            "state": state,
            "info": info,
            "attacker_side": attacker_side,
            "defender_side": defender_side,
            "len_model": len(model),
        }
    )

primary_ctx = env_contexts[0]
model = primary_ctx["model"]
enemy = primary_ctx["enemy"]
env = primary_ctx["env"]

ordered_keys = ["move", "attack", "shoot", "charge", "use_cp", "cp_on"]
for i_u in range(len(model)):
    ordered_keys.append(f"move_num_{i_u}")

n_actions = []
for k in ordered_keys:
    sp = env.action_space.spaces[k]

    # Discrete (и gym, и gymnasium)
    if hasattr(sp, "n"):
        n_actions.append(int(sp.n))

    # MultiDiscrete (на всякий)
    elif hasattr(sp, "nvec"):
        n_actions.extend([int(x) for x in sp.nvec])

    else:
        raise TypeError(f"Unsupported action space for {k}: {type(sp)}")


state = primary_ctx["state"]
info = primary_ctx["info"]
if verbose:
    squads_for_actions_count = len(model)
    print(f"[action_space] squads_for_actions_count={squads_for_actions_count}")
    for idx, unit in enumerate(model):
        unit_data = unit.showUnitData()
        unit_name = unit_data.get("Name", "Unknown")
        print(f"[action_space] squad[{idx}] name={unit_name}")
    total_models_count = 0
    for unit in model:
        unit_data = unit.showUnitData()
        total_models_count += int(unit_data.get("#OfModels", 1))
    print(f"[action_space] total_models_count={total_models_count}")
    move_num_keys = [
        key for key in env.action_space.spaces.keys() if key.startswith("move_num_")
    ]
    print(f"[action_space] move_num_keys_count={len(move_num_keys)}")

# state может быть np.array или OrderedDict
if isinstance(state, dict) or "OrderedDict" in str(type(state)):
    n_observations = len(list(state.values()))
else:
    n_observations = int(np.array(state).shape[0])


policy_net = DQN(n_observations, n_actions, dueling=DUELING_ENABLED).to(device)
target_net = DQN(n_observations, n_actions, dueling=DUELING_ENABLED).to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

opponent_policy_net = None
if SELF_PLAY_ENABLED:
    opponent_policy_net = DQN(n_observations, n_actions, dueling=DUELING_ENABLED).to(device)
    opponent_policy_net.eval()
    if SELF_PLAY_OPPONENT_MODE == "fixed_checkpoint":
        if not SELF_PLAY_FIXED_PATH:
            raise ValueError("SELF_PLAY_FIXED_PATH обязателен для режима fixed_checkpoint.")
        if not os.path.isfile(SELF_PLAY_FIXED_PATH):
            raise FileNotFoundError(
                f"SELF_PLAY_FIXED_PATH не найден: {SELF_PLAY_FIXED_PATH}. Проверь путь."
            )
        checkpoint = torch.load(SELF_PLAY_FIXED_PATH, map_location=device)
        if isinstance(checkpoint, dict) and "policy_net" in checkpoint:
            checkpoint_net_type = checkpoint.get("net_type", "basic")
            if checkpoint_net_type != NET_TYPE:
                warn_msg = (
                    "[SELFPLAY] ВНИМАНИЕ: несовпадение типа сети "
                    f"(checkpoint={checkpoint_net_type}, текущая={NET_TYPE}). "
                    "Стартуем с новой инициализацией."
                )
                print(warn_msg)
                append_agent_log(warn_msg)
            else:
                opponent_policy_net.load_state_dict(checkpoint["policy_net"])
        else:
            if NET_TYPE != "basic":
                warn_msg = (
                    "[SELFPLAY] ВНИМАНИЕ: старый формат чекпойнта без net_type, "
                    f"а текущая сеть={NET_TYPE}. Стартуем с новой инициализацией."
                )
                print(warn_msg)
                append_agent_log(warn_msg)
            else:
                opponent_policy_net.load_state_dict(checkpoint)
        append_agent_log(
            f"[SELFPLAY] fixed_checkpoint path={SELF_PLAY_FIXED_PATH}"
        )
    else:
        opponent_policy_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
replay_capacity = int(os.getenv("REPLAY_CAPACITY", "100000"))
if PER_ENABLED:
    memory = PrioritizedReplayMemory(replay_capacity, alpha=PER_ALPHA, eps=PER_EPS)
else:
    memory = ReplayMemory(replay_capacity)

def opponent_policy(obs, env, len_model):
    if opponent_policy_net is None:
        return None
    action = select_action_with_epsilon(
        env,
        obs,
        opponent_policy_net,
        SELF_PLAY_OPPONENT_EPSILON,
        len_model,
    )
    return convertToDict(action)

inText = []

inText.append("Model units:")
for i in model:
    inText.append("Name: {}, Army Type: {}".format(i.showUnitData()["Name"], i.showUnitData()["Army"]))
inText.append("Enemy units:")
for i in enemy:
    inText.append("Name: {}, Army Type: {}".format(i.showUnitData()["Name"], i.showUnitData()["Army"]))
inText.append("Number of Lifetimes ran: {}\n".format(totLifeT))

pbar = tqdm(total=totLifeT)

for ctx in env_contexts:
    ctx["state"], ctx["info"] = ctx["env"].reset(m=ctx["model"], e=ctx["enemy"], Type="big", trunc=True)
    ctx["ep_len"] = 0
    ctx["rew_arr"] = []
    ctx["n_step_buffer"] = collections.deque(maxlen=N_STEP)

state = primary_ctx["state"]
info = primary_ctx["info"]

current_time = datetime.datetime.now()
date = str(current_time.second)+"-"+str(current_time.microsecond)
name = "M:"+model[0].showUnitData()["Army"]+"_vs_"+"P:"+enemy[0].showUnitData()["Army"]
fold =  "models/"+name
fileName = fold+"/model-"+date+".pickle"
randNum = np.random.randint(0, 10000000)
metrics = metrics(fold, randNum, date)
ep_rows = [] 

global_step = 0
optimize_steps = 0
primary_env_unwrapped = unwrap_env(primary_ctx["env"])
initial_model_hp = float(sum(getattr(primary_env_unwrapped, "unit_health", [])))
initial_enemy_hp = float(sum(getattr(primary_env_unwrapped, "enemy_health", [])))
append_agent_log(
    "Старт обучения: "
    f"model_hp_total={initial_model_hp}, enemy_hp_total={initial_enemy_hp}, "
    f"battle_round={getattr(primary_env_unwrapped, 'battle_round', 'n/a')}, trunc={trunc}"
)
if trunc:
    append_agent_log(
        "Логи фаз/ходов отключены (trunc=True). "
        "Чтобы включить подробные логи: VERBOSE_LOGS=1 или MANUAL_DICE=1."
    )
if initial_model_hp <= 0 or initial_enemy_hp <= 0:
    append_agent_log(
        "ВНИМАНИЕ: на старте эпизода обнаружено нулевое здоровье. "
        f"model_hp_total={initial_model_hp}, enemy_hp_total={initial_enemy_hp}. "
        "Это может приводить к мгновенному завершению эпизодов."
    )

while end is False:
    shoot_masks = []
    for idx, ctx in enumerate(env_contexts):
        mask_log_fn = append_agent_log if idx == 0 else None
        shoot_masks.append(build_shoot_action_mask(ctx["env"], log_fn=mask_log_fn, debug=TRAIN_DEBUG))

    states = [ctx["state"] for ctx in env_contexts]
    actions, eps_threshold = _select_actions_batch(env_contexts, states, global_step, policy_net, shoot_masks)

    for idx, ctx in enumerate(env_contexts):
        env_unwrapped = unwrap_env(ctx["env"])
        if SELF_PLAY_ENABLED:
            env_unwrapped.enemyTurn(
                trunc=trunc,
                policy_fn=lambda obs, env=ctx["env"], lm=ctx["len_model"]: opponent_policy(obs, env, lm),
            )
        else:
            env_unwrapped.enemyTurn(trunc=trunc)

    losses = []
    last_td_stats = None
    last_per_beta = PER_BETA_START
    last_loss_value = None

    dev = next(policy_net.parameters()).device

    for idx, ctx in enumerate(env_contexts):
        ctx["ep_len"] += 1
        action_dict = convertToDict(actions[idx])
        next_observation, reward, done, res, info = ctx["env"].step(action_dict)
        ctx["rew_arr"].append(float(reward))

        unit_health = info["model health"]
        enemy_health = info["player health"]
        inAttack = info["in attack"]

        if inAttack == 1 and trunc is False:
            print("The units are fighting")

        if RENDER_EVERY > 0 and vec_env_count == 1 and (global_step % RENDER_EVERY == 0 or done):
            ctx["env"].render()

        mission_name = info.get("mission", DEFAULT_MISSION_NAME)
        message = (
            "Iteration {} ended with reward {}, enemy health {}, model health {}, model VP {}, enemy VP {}, mission {}".format(
                global_step,
                reward,
                enemy_health,
                unit_health,
                info["model VP"],
                info["player VP"],
                mission_name,
            )
        )
        if trunc is False:
            print(message)
        inText.append(message)

        state_t = torch.tensor(to_np_state(ctx["state"]), device=dev).unsqueeze(0)
        next_state_t = None
        next_shoot_mask = None
        if not done:
            next_state_t = torch.tensor(to_np_state(next_observation), device=dev).unsqueeze(0)
            mask_log_fn = append_agent_log if idx == 0 else None
            next_shoot_mask = build_shoot_action_mask(ctx["env"], log_fn=mask_log_fn, debug=TRAIN_DEBUG)

        ctx["n_step_buffer"].append((state_t, actions[idx], float(reward), next_state_t, done, next_shoot_mask))
        if len(ctx["n_step_buffer"]) >= N_STEP:
            reward_sum, n_step_next_state, n_step_next_mask, n_step_count = build_n_step_transition(
                ctx["n_step_buffer"], GAMMA
            )
            reward_sum_t = torch.tensor([reward_sum], device=dev, dtype=torch.float32)
            head_state, head_action, _, _, _, _ = ctx["n_step_buffer"][0]
            memory.push(head_state, head_action, n_step_next_state, reward_sum_t, n_step_count, n_step_next_mask)
            ctx["n_step_buffer"].popleft()
        if done:
            while ctx["n_step_buffer"]:
                reward_sum, n_step_next_state, n_step_next_mask, n_step_count = build_n_step_transition(
                    ctx["n_step_buffer"], GAMMA
                )
                reward_sum_t = torch.tensor([reward_sum], device=dev, dtype=torch.float32)
                head_state, head_action, _, _, _, _ = ctx["n_step_buffer"][0]
                memory.push(head_state, head_action, n_step_next_state, reward_sum_t, n_step_count, n_step_next_mask)
                ctx["n_step_buffer"].popleft()
        ctx["state"] = next_observation

        if done is True:
            if SELF_PLAY_ENABLED:
                append_agent_log(
                    f"Конец эпизода {numLifeT + 1}. "
                    f"[SELFPLAY] enabled=1 mode={SELF_PLAY_OPPONENT_MODE} "
                    f"update_every={SELF_PLAY_UPDATE_EVERY_EPISODES} opp_eps={SELF_PLAY_OPPONENT_EPSILON}"
                )
            end_reason_env = info.get("end reason", "")
            winner_env = info.get("winner")
            model_hp_total = sum(info.get("model health", [])) if isinstance(info.get("model health"), (list, tuple, np.ndarray)) else info.get("model health")
            enemy_hp_total = sum(info.get("player health", [])) if isinstance(info.get("player health"), (list, tuple, np.ndarray)) else info.get("player health")
            append_agent_log(
                "Конец эпизода: "
                f"reason={end_reason_env or 'unknown'} "
                f"winner={winner_env} "
                f"model_hp_total={model_hp_total} enemy_hp_total={enemy_hp_total} "
                f"model_vp={info.get('model VP')} enemy_vp={info.get('player VP')} "
                f"turn={info.get('turn')} battle_round={info.get('battle round')}"
            )
            if ctx["ep_len"] == 1:
                append_agent_log(
                    "ВНИМАНИЕ: эпизод завершился на первом шаге. "
                    "Проверьте reset/условия завершения (нулевое здоровье, лимиты хода, "
                    "ошибки расстановки)."
                )
            pbar.update(1)
            metrics.updateRew(sum(ctx["rew_arr"]) / len(ctx["rew_arr"]))
            metrics.updateEpLen(ctx["ep_len"])
            # ===== extra metrics (winrate / VP diff / end reason) =====
            ep_reward = float(sum(ctx["rew_arr"]) / len(ctx["rew_arr"])) if len(ctx["rew_arr"]) > 0 else 0.0
            model_vp = int(info.get("model VP", 0))
            player_vp = int(info.get("player VP", 0))
            vp_diff = model_vp - player_vp

            mh_list = info.get("model health", [])
            ph_list = info.get("player health", [])

            def _sum_health(x):
                try:
                    if isinstance(x, (list, tuple, np.ndarray)):
                        return int(sum(x))
                    return int(x)
                except Exception:
                    return 0

            mh = _sum_health(mh_list)
            ph = _sum_health(ph_list)

            end_code = res  # то, что возвращает env (1..3 миссия или 4)
            end_reason_env = info.get("end reason", "")
            turn = int(info.get("turn", ctx["ep_len"]))  # если turn не добавляли в env — будет epLen

            if end_reason_env:
                end_reason = end_reason_env
                if end_reason_env == "wipeout_enemy":
                    result = "win"
                elif end_reason_env == "wipeout_model":
                    result = "loss"
                elif end_reason_env == "turn_limit":
                    if vp_diff > 0:
                        result = "win"
                    elif vp_diff < 0:
                        result = "loss"
                    else:
                        result = "draw"
                else:
                    if vp_diff > 0:
                        result = "win"
                    elif vp_diff < 0:
                        result = "loss"
                    else:
                        result = "draw"
            elif ph <= 0 and mh > 0:
                result = "win"
                end_reason = "wipe_enemy"
            elif mh <= 0 and ph > 0:
                result = "loss"
                end_reason = "wipe_model"
            else:
                mission_name = info.get("mission", DEFAULT_MISSION_NAME)
                end_reason = f"turn_limit_{mission_name}"
                if vp_diff > 0:
                    result = "win"
                elif vp_diff < 0:
                    result = "loss"
                else:
                    result = "draw"

            if result == "win":
                inText.append("model won!")
                if trunc is False:
                    print("model won!")
            elif result == "loss":
                inText.append("enemy won!")
                if trunc is False:
                    print("enemy won!")
            else:
                inText.append("draw!")
                if trunc is False:
                    print("draw!")

            if TRAIN_LOG_ENABLED:
                win_flag = 1 if result == "win" else 0
                train_ep_line = (
                    "[TRAIN][EP] "
                    f"ep={numLifeT + 1} "
                    f"ep_reward={ep_reward:.6f} "
                    f"win={win_flag} "
                    f"vp_diff={vp_diff} "
                    f"end_reason={end_reason}"
                )
                if TRAIN_LOG_TO_FILE:
                    append_agent_log(train_ep_line)
                if TRAIN_LOG_TO_CONSOLE:
                    print(train_ep_line)

            ep_rows.append(
                {
                    "episode": numLifeT + 1,  # lifetimes считаются у тебя через numLifeT
                    "ep_reward": ep_reward,
                    "ep_len": ctx["ep_len"],
                    "turn": turn,
                    "model_vp": model_vp,
                    "player_vp": player_vp,
                    "vp_diff": vp_diff,
                    "result": result,
                    "end_reason": end_reason,
                    "end_code": end_code,
                }
            )
            # ==========================================================

            if res == 4:
                inText.append("Major Victory")

            if float(reward) > 0:
                inText.append("model won!")
                if trunc is False:
                    print("model won!")
            else:
                inText.append("enemy won!")
                if trunc is False:
                    print("enemy won!")
            if trunc is False:
                print("Restarting...")
            numLifeT += 1

            if SELF_PLAY_ENABLED and SELF_PLAY_OPPONENT_MODE == "snapshot":
                if numLifeT % SELF_PLAY_UPDATE_EVERY_EPISODES == 0:
                    opponent_policy_net.load_state_dict(policy_net.state_dict())
                    append_agent_log(
                        f"[SELFPLAY] opponent snapshot updated at episode {numLifeT}"
                    )

            attacker_side, defender_side = roll_off_attacker_defender(
                manual_roll_allowed=False,
                log_fn=print if idx == 0 else None,
            )
            if verbose and idx == 0:
                print(f"[MISSION Only War] Attacker={attacker_side}, Defender={defender_side}")

            deploy_only_war(
                model_units=ctx["model"],
                enemy_units=ctx["enemy"],
                b_len=b_len,
                b_hei=b_hei,
                attacker_side=attacker_side,
                log_fn=log_fn if idx == 0 else None,
            )
            post_deploy_setup(log_fn=log_fn if idx == 0 else None)
            ctx["env"].attacker_side = attacker_side
            ctx["env"].defender_side = defender_side

            ctx["state"], ctx["info"] = ctx["env"].reset(m=ctx["model"], e=ctx["enemy"], Type="small", trunc=True)
            ctx["ep_len"] = 0
            ctx["rew_arr"] = []

        if numLifeT == totLifeT:
            end = True
            pbar.close()
            break

    if end:
        break

    if global_step >= WARMUP_STEPS:
        for _ in range(UPDATES_PER_STEP):
            per_beta = PER_BETA_START
            if PER_ENABLED and PER_BETA_FRAMES > 0:
                per_beta = min(
                    1.0,
                    PER_BETA_START
                    + (1.0 - PER_BETA_START)
                    * (optimize_steps / float(PER_BETA_FRAMES)),
                )
            result = optimize_model(
                policy_net,
                target_net,
                optimizer,
                memory,
                n_observations,
                double_dqn_enabled=DOUBLE_DQN_ENABLED,
                per_enabled=PER_ENABLED,
                per_beta=per_beta,
                per_eps=PER_EPS,
            )

            # optimize_model возвращает 0 если replay ещё маленький — такие пропускаем
            if result and result["loss"] != 0:
                losses.append(result["loss"])
                last_td_stats = result
                last_per_beta = per_beta
                last_loss_value = result["loss"]
                optimize_steps += 1
                if TRAIN_LOG_ENABLED and optimize_steps % TRAIN_LOG_EVERY_UPDATES == 0:
                    train_line = (
                        "[TRAIN] "
                        f"ep={numLifeT + 1} "
                        f"upd={optimize_steps} "
                        f"step={global_step} "
                        f"loss={last_loss_value:.6f} "
                        f"eps={eps_threshold:.4f} "
                        f"lr={LR:.6g} "
                        f"gamma={GAMMA:.6g} "
                        f"PER={int(PER_ENABLED)} "
                        f"alpha={PER_ALPHA:.4g} "
                        f"beta={last_per_beta:.4g} "
                        f"N_STEP={N_STEP}"
                    )
                    if N_STEP > 1:
                        effective_gamma = GAMMA ** N_STEP
                        train_line += f" effective_gamma={effective_gamma:.6g}"
                    if PER_ENABLED and last_td_stats.get("per_stats"):
                        per_stats = last_td_stats["per_stats"]
                        train_line += (
                            f" td_abs_mean={per_stats['td_error_mean']:.6f}"
                            f" td_abs_max={per_stats['td_error_max']:.6f}"
                            f" prio_mean={per_stats['priority_mean']:.6f}"
                            f" prio_max={per_stats['priority_max']:.6f}"
                            f" isw_mean={per_stats['is_weight_mean']:.6f}"
                            f" isw_max={per_stats['is_weight_max']:.6f}"
                        )
                    if TRAIN_LOG_TO_FILE:
                        append_agent_log(train_line)
                    if TRAIN_LOG_TO_CONSOLE:
                        print(train_line)

            # ✅ Быстрый soft-update target_net (намного быстрее, чем state_dict)
            with torch.no_grad():
                for p_tgt, p in zip(target_net.parameters(), policy_net.parameters()):
                    p_tgt.data.mul_(1.0 - TAU)
                    p_tgt.data.add_(p.data, alpha=TAU)

    # чтобы график loss не раздувался в 100 раз — пишем среднее за env-step
    if len(losses) > 0:
        metrics.updateLoss(sum(losses) / len(losses))
    else:
        metrics.updateLoss(0)
    if REWARD_DEBUG and last_td_stats and optimize_steps % REWARD_DEBUG_EVERY == 0:
        append_agent_log(
            "[TD] "
            f"step={global_step} "
            f"mean={last_td_stats['td_target_mean']:.6f} "
            f"max={last_td_stats['td_target_max']:.6f}"
        )
        if PER_ENABLED and last_td_stats.get("per_stats"):
            per_stats = last_td_stats["per_stats"]
            append_agent_log(
                "[PER] "
                f"opt_step={optimize_steps} "
                f"priority_mean={per_stats['priority_mean']:.6f} "
                f"priority_max={per_stats['priority_max']:.6f} "
                f"is_weight_mean={per_stats['is_weight_mean']:.6f} "
                f"td_error_mean={per_stats['td_error_mean']:.6f} "
                f"td_error_max={per_stats['td_error_max']:.6f}"
            )
    # =========================

    global_step += vec_env_count

for ctx in env_contexts:
    ctx["env"].close()

with open('trainRes.txt', 'w') as f:
    for i in range(len(inText)):
        f.write(inText[i])
        f.write('\n')

# Делать gif только если мы реально сохраняли кадры
if RENDER_EVERY > 0:
    if totLifeT > 30:
        genDisplay.makeGif(numOfLife=totLifeT, trunc=True)
    else:
        genDisplay.makeGif(numOfLife=totLifeT)
else:
    print("[render] RENDER_EVERY=0 -> gif skipped")


metrics.lossCurve()
metrics.showRew()
metrics.showEpLen()

save_extra_metrics(run_id=str(randNum), ep_rows=ep_rows, metrics_dir="metrics")
metrics.createJson()
print("Generated metrics")

if (os.path.exists("models/{}".format(name)) == False):
    os.system("mkdir models/{}".format(name))

torch.save({
    "policy_net": policy_net.state_dict(),
    "target_net": target_net.state_dict(),
    "net_type": NET_TYPE,
    'optimizer': optimizer.state_dict(),}
    , ("models/{}/model-{}.pth".format(name, date)))

toSave = [primary_ctx["env"], primary_ctx["model"], primary_ctx["enemy"]]

with open(fileName, "wb") as file:
    pickle.dump(toSave, file)

if os.path.isfile("gui/data.json"):
    initFile.delFile()
