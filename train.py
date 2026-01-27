from collections import Counter
import sys
import os
import csv
import numpy as np
import gymnasium as gym
import pickle
import datetime
import collections
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

def select_action_with_epsilon(env, state, policy_net, epsilon, len_model):
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
            for i in decision:
                action.append(int(i.argmax(dim=1).item()))
            return torch.tensor([action], device="cpu")
    sampled_action = env.action_space.sample()
    action_list = [
        sampled_action['move'],
        sampled_action['attack'],
        sampled_action['shoot'],
        sampled_action['charge'],
        sampled_action['use_cp'],
        sampled_action['cp_on']
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

def append_log_for_agents(message: str, log_path: str = "LOGS_FOR_AGENTS.md"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {message}"
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(line + "\n")

TAU = data["tau"]
LR = data["lr"]

# ============================================================
# (C) Несколько обучающих апдейтов на один шаг среды
# ============================================================
UPDATES_PER_STEP = int(data.get("updates_per_step", 1))  # 1 = как было раньше
WARMUP_STEPS     = int(data.get("warmup_steps", 0))      # 0 = без прогрева

b_len = 60
b_hei = 40

print("\nTraining...\n")

enemy1 = Unit(unitData("Space_Marine", "Eliminator Squad"), weaponData("Bolt Pistol"), weaponData("Close combat weapon"), b_len, b_hei)
model1 = Unit(unitData("Space_Marine", "Eliminator Squad"), weaponData("Bolt Pistol"), weaponData("Close combat weapon"), b_len, b_hei)

enemy2 = Unit(unitData("Space_Marine", "Apothecary"), weaponData("Absolver Bolt Pistol"), weaponData("Close combat weapon"), b_len, b_hei)
model2 = Unit(unitData("Space_Marine", "Apothecary"), weaponData("Absolver Bolt Pistol"), weaponData("Close combat weapon"), b_len, b_hei)

enemy = [enemy1, enemy2]
model = [model1, model2]

end = False
trunc = True
totLifeT = 10
steps_done = 0

if os.path.isfile("gui/data.json"):

    totLifeT = initFile.getNumLife()
    b_len = initFile.getBoardX()
    b_hei = initFile.getBoardY()
    enemy_counts = initFile.getEnemyUnitCounts()
    model_counts = initFile.getModelUnitCounts()
    enemy_instance_ids = initFile.getEnemyUnitInstanceIds()
    model_instance_ids = initFile.getModelUnitInstanceIds()
    print("Model Units:\n")
    if len(initFile.getEnemyUnits()) > 0:
        enemy = []
        for i in range(len(initFile.getEnemyUnits())):
            unit_data = unitData(initFile.getEnemyFaction(), initFile.getEnemyUnits()[i])
            if i < len(enemy_counts) and enemy_counts[i] > 0:
                unit_data["#OfModels"] = enemy_counts[i]
            instance_id = enemy_instance_ids[i] if i < len(enemy_instance_ids) else ""
            enemy.append(Unit(unit_data, weaponData(initFile.getEnemyW()[i][0]), weaponData(initFile.getEnemyW()[i][1]),
                              b_len, b_hei, instance_id=instance_id))
            print("Name:", initFile.getEnemyUnits()[i], "Weapons: ", initFile.getEnemyW()[i][0], initFile.getEnemyW()[i][1])
    print("Enemy Units:\n")
    if len(initFile.getModelUnits()) > 0:
        model = []
        for i in range(len(initFile.getModelUnits())):
            unit_data = unitData(initFile.getModelFaction(), initFile.getModelUnits()[i])
            if i < len(model_counts) and model_counts[i] > 0:
                unit_data["#OfModels"] = model_counts[i]
            instance_id = model_instance_ids[i] if i < len(model_instance_ids) else ""
            model.append(Unit(unit_data, weaponData(initFile.getModelW()[i][0]), weaponData(initFile.getModelW()[i][1]),
                              b_len, b_hei, instance_id=instance_id))
            print("Name:", initFile.getModelUnits()[i], "Weapons: ", initFile.getModelW()[i][0], initFile.getModelW()[i][1])

numLifeT = 0

verbose = os.getenv("VERBOSE_LOGS", "0") == "1"
log_fn = print if verbose else None
attacker_side, defender_side = roll_off_attacker_defender(
    manual_roll_allowed=False,
    log_fn=print,
)
if verbose:
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
    log_fn=log_fn,
)
post_deploy_setup(log_fn=log_fn)

env = gym.make("40kAI-v0", disable_env_checker=True, enemy = enemy, model = model, b_len = b_len, b_hei = b_hei)
env.attacker_side = attacker_side
env.defender_side = defender_side

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


state, info = env.reset(m=model, e=enemy, trunc=True)
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


policy_net = DQN(n_observations, n_actions).to(device)
target_net = DQN(n_observations, n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

opponent_policy_net = None
if SELF_PLAY_ENABLED:
    opponent_policy_net = DQN(n_observations, n_actions).to(device)
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
            opponent_policy_net.load_state_dict(checkpoint["policy_net"])
        else:
            opponent_policy_net.load_state_dict(checkpoint)
        append_log_for_agents(
            f"[SELFPLAY] fixed_checkpoint path={SELF_PLAY_FIXED_PATH}"
        )
    else:
        opponent_policy_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(10000)

def opponent_policy(obs):
    if opponent_policy_net is None:
        return None
    action = select_action_with_epsilon(
        env,
        obs,
        opponent_policy_net,
        SELF_PLAY_OPPONENT_EPSILON,
        len(model),
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

i = 0

pbar = tqdm(total=totLifeT)

state, info = env.reset(m=model, e=enemy, Type="big", trunc=True)

current_time = datetime.datetime.now()
date = str(current_time.second)+"-"+str(current_time.microsecond)
name = "M:"+model[0].showUnitData()["Army"]+"_vs_"+"P:"+enemy[0].showUnitData()["Army"]
fold =  "models/"+name
fileName = fold+"/model-"+date+".pickle"
randNum = np.random.randint(0, 10000000)
metrics = metrics(fold, randNum, date)

rewArr = []
ep_rows = [] 

epLen = 0

while end == False:
    epLen += 1
    if SELF_PLAY_ENABLED and epLen == 1:
        append_log_for_agents(
            f"Старт эпизода {numLifeT + 1}. "
            f"[SELFPLAY] enabled=1 mode={SELF_PLAY_OPPONENT_MODE} "
            f"update_every={SELF_PLAY_UPDATE_EVERY_EPISODES} opp_eps={SELF_PLAY_OPPONENT_EPSILON}"
        )
    action = select_action(env, state, i, policy_net, len(model))
    action_dict = convertToDict(action)
    if trunc == False:
        print(env.get_info())

    if SELF_PLAY_ENABLED:
        env.enemyTurn(trunc=trunc, policy_fn=opponent_policy)
    else:
        env.enemyTurn(trunc=trunc)
    next_observation, reward, done, res, info = env.step(action_dict)
    rewArr.append(float(reward))  
    reward_t = torch.tensor([reward], device=device, dtype=torch.float32)  # тензор для replay


    unit_health = info["model health"]
    enemy_health = info["player health"]
    inAttack = info["in attack"]

    if inAttack == 1:
        if trunc == False:
            print("The units are fighting")

    if RENDER_EVERY > 0 and (i % RENDER_EVERY == 0 or done):
        env.render()
    mission_name = info.get("mission", DEFAULT_MISSION_NAME)
    message = "Iteration {} ended with reward {}, enemy health {}, model health {}, model VP {}, enemy VP {}, mission {}".format(
        i,
        reward,
        enemy_health,
        unit_health,
        info["model VP"],
        info["player VP"],
        mission_name,
    )
    if trunc == False:
        print(message)
    inText.append(message)

    dev = next(policy_net.parameters()).device
    state_t = torch.tensor(to_np_state(state), device=dev).unsqueeze(0)
    next_state_t = torch.tensor(to_np_state(next_observation), device=dev).unsqueeze(0)

    
    memory.push(state_t, action, next_state_t, reward_t)
    state = next_observation

    # =========================
    # ✅ Несколько обучающих апдейтов на 1 шаг среды
    losses = []

    if i >= WARMUP_STEPS:
        for _ in range(UPDATES_PER_STEP):
            loss = optimize_model(policy_net, target_net, optimizer, memory, n_observations)

            # optimize_model возвращает 0 если replay ещё маленький — такие пропускаем
            if loss and loss != 0:
                losses.append(loss)

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
    # =========================



    if done == True:
        if SELF_PLAY_ENABLED:
            append_log_for_agents(
                f"Конец эпизода {numLifeT + 1}. "
                f"[SELFPLAY] enabled=1 mode={SELF_PLAY_OPPONENT_MODE} "
                f"update_every={SELF_PLAY_UPDATE_EVERY_EPISODES} opp_eps={SELF_PLAY_OPPONENT_EPSILON}"
            )
        pbar.update(1)
        metrics.updateRew(sum(rewArr)/len(rewArr))
        metrics.updateEpLen(epLen)
        # ===== extra metrics (winrate / VP diff / end reason) =====
        ep_reward = float(sum(rewArr) / len(rewArr)) if len(rewArr) > 0 else 0.0
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
        turn = int(info.get("turn", epLen))  # если turn не добавляли в env — будет epLen

        if ph <= 0 and mh > 0:
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
            if trunc == False:
                print("model won!")
        elif result == "loss":
            inText.append("enemy won!")
            if trunc == False:
                print("enemy won!")
        else:
            inText.append("draw!")
            if trunc == False:
                print("draw!")


        ep_rows.append({
            "episode": numLifeT + 1,   # lifetimes считаются у тебя через numLifeT
            "ep_reward": ep_reward,
            "ep_len": epLen,
            "turn": turn,
            "model_vp": model_vp,
            "player_vp": player_vp,
            "vp_diff": vp_diff,
            "result": result,
            "end_reason": end_reason,
            "end_code": end_code,
        })
        # ==========================================================

        epLen = 0
        rewArr = []

        if res == 4:
            inText.append("Major Victory")

        if float(reward) > 0:
            inText.append("model won!")
            if trunc == False:
                print("model won!")
        else:
            inText.append("enemy won!")
            if trunc == False:
                print("enemy won!")
        if trunc == False:
            print("Restarting...")
        numLifeT+=1

        if SELF_PLAY_ENABLED and SELF_PLAY_OPPONENT_MODE == "snapshot":
            if numLifeT % SELF_PLAY_UPDATE_EVERY_EPISODES == 0:
                opponent_policy_net.load_state_dict(policy_net.state_dict())
                append_log_for_agents(
                    f"[SELFPLAY] opponent snapshot updated at episode {numLifeT}"
                )

        attacker_side, defender_side = roll_off_attacker_defender(
            manual_roll_allowed=False,
            log_fn=print,
        )
        if verbose:
            print(f"[MISSION Only War] Attacker={attacker_side}, Defender={defender_side}")

        deploy_only_war(
            model_units=model,
            enemy_units=enemy,
            b_len=b_len,
            b_hei=b_hei,
            attacker_side=attacker_side,
            log_fn=log_fn,
        )
        post_deploy_setup(log_fn=log_fn)
        env.attacker_side = attacker_side
        env.defender_side = defender_side

        state, info = env.reset(m=model, e=enemy, Type="small", trunc=True)

    if numLifeT == totLifeT:
        end = True
        pbar.close()
    i+=1

env.close()

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
    'optimizer': optimizer.state_dict(),}
    , ("models/{}/model-{}.pth".format(name, date)))

toSave = [env, model, enemy]

with open(fileName, "wb") as file:
    pickle.dump(toSave, file)

if os.path.isfile("gui/data.json"):
    initFile.delFile()
