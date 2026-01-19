from collections import Counter
import sys
import os
import csv
import numpy as np
import gymnasium as gym
import pickle
import datetime
import json
import matplotlib.pyplot as plt
from tqdm import tqdm
from gym_mod.envs.warhamEnv import *
from gym_mod.engine import genDisplay, Unit, unitData, weaponData, initFile, metrics

from model.DQN import *
from model.memory import *
from model.utils import *

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

import warnings
warnings.filterwarnings("ignore") 

with open(os.path.abspath("hyperparams.json")) as j:
    data = json.loads(j.read())

MISSION_NAME = {
    1: "slay_and_secure",
    2: "ancient_relic",
    3: "domination",
}

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

TAU = data["tau"]
LR = data["lr"]

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
    print("Model Units:\n")
    if len(initFile.getEnemyUnits()) > 0:
        enemy = []
        for i in range(len(initFile.getEnemyUnits())):
            enemy.append(Unit(unitData(initFile.getEnemyFaction(), initFile.getEnemyUnits()[i]), weaponData(initFile.getEnemyW()[i][0]), weaponData(initFile.getEnemyW()[i][1]), b_len, b_hei))
            print("Name:", initFile.getEnemyUnits()[i], "Weapons: ", initFile.getEnemyW()[i][0], initFile.getEnemyW()[i][1])
    print("Enemy Units:\n")
    if len(initFile.getModelUnits()) > 0:
        model = []
        for i in range(len(initFile.getModelUnits())):
            model.append(Unit(unitData(initFile.getModelFaction(), initFile.getModelUnits()[i]), weaponData(initFile.getModelW()[i][0]), weaponData(initFile.getModelW()[i][1]), b_len, b_hei))
            print("Name:", initFile.getModelUnits()[i], "Weapons: ", initFile.getModelW()[i][0], initFile.getModelW()[i][1])

numLifeT = 0

deployType = ["Search and Destroy", "Hammer and Anvil", "Dawn of War"]
deployChang = np.random.choice(deployType)
for m in model:
    m.deployUnit(deployChang, "model")
for e in enemy:
    e.deployUnit(deployChang, "player")

env = gym.make("40kAI-v0", disable_env_checker=True, enemy = enemy, model = model, b_len = b_len, b_hei = b_hei)

n_actions = [5,2,len(enemy), len(enemy), 5, len(model)]
for i in range(len(model)):
    n_actions.append(12)
state, info = env.reset(m=model, e=enemy, trunc=True)
n_observations = len(state)

policy_net = DQN(n_observations, n_actions).to(device)
target_net = DQN(n_observations, n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(10000)

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
    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    
    action = select_action(env, state, i, policy_net, len(model))
    action_dict = convertToDict(action)
    if trunc == False:
        print(env.get_info())

    env.enemyTurn(trunc=trunc)
    next_observation, reward, done, res, info = env.step(action_dict)
    rewArr.append(reward)
    reward = torch.tensor([reward], device=device)

    unit_health = info["model health"]
    enemy_health = info["player health"]
    inAttack = info["in attack"]

    if inAttack == 1:
        if trunc == False:
            print("The units are fighting")

    board = env.render()
    message = "Iteration {} ended with reward {}, enemy health {}, model health {}, model VP {}, enemy VP {}, victory condition {}".format(i, reward, enemy_health, unit_health, info["model VP"], info["player VP"], info["victory condition"])
    if trunc == False:
        print(message)
    inText.append(message)

    next_state = torch.tensor(next_observation, dtype=torch.float32, device=device).unsqueeze(0)
    memory.push(state, action, next_state, reward)
    state = next_state
    loss = optimize_model(policy_net, target_net, optimizer, memory, n_observations)
    metrics.updateLoss(loss)
    
    for key in policy_net.state_dict():
        target_net.state_dict()[key] = policy_net.state_dict()[key]*TAU + target_net.state_dict()[key]*(1-TAU)
    target_net.load_state_dict(target_net.state_dict())

    if done == True:
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
            vc = info.get("victory condition", end_code)
            end_reason = f"turn_limit_{MISSION_NAME.get(vc, str(vc))}"
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

        if res == 1:
            inText.append("Slay and Secure Victory Condition")
        elif res == 2:
            inText.append("Ancient Relic Victory Condition")
        elif res == 3:
            inText.append("Domination Victory Condition")
        elif res == 4:
            inText.append("Major Victory")

        if reward > 0:
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

        deployChang = np.random.choice(deployType)
        for m in model:
            m.deployUnit(deployChang, "model")
        for e in enemy:
            e.deployUnit(deployChang, "player")

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

if totLifeT > 30:
    genDisplay.makeGif(numOfLife=totLifeT, trunc = True)
else:
    genDisplay.makeGif(numOfLife=totLifeT)

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
