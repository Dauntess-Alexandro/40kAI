from collections import Counter
import argparse
import collections
import csv
import datetime
import json
import os
import pickle
import random
import time

import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np
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


import warnings
warnings.filterwarnings("ignore")

with open(os.path.abspath("hyperparams.json")) as j:
    data = json.loads(j.read())

parser = argparse.ArgumentParser(description="40kAI DQN training")
parser.add_argument("--batch-size", type=int, default=int(data.get("batch_size", 2048)))
parser.add_argument("--max-batch-size", type=int, default=int(data.get("max_batch_size", data.get("batch_size", 2048))))
parser.add_argument("--updates-per-step", type=int, default=int(data.get("updates_per_step", 1)))
parser.add_argument("--warmup-steps", type=int, default=int(data.get("warmup_steps", 0)))
parser.add_argument("--replay-size", type=int, default=int(data.get("replay_size", 10000)))
parser.add_argument("--lr", type=float, default=float(data.get("lr", 1e-4)))
parser.add_argument("--gamma", type=float, default=float(data.get("gamma", 0.99)))
parser.add_argument("--tau", type=float, default=float(data.get("tau", 0.005)))
parser.add_argument("--eps-start", type=float, default=float(data.get("eps_start", 0.9)))
parser.add_argument("--eps-end", type=float, default=float(data.get("eps_end", 0.05)))
parser.add_argument("--eps-decay", type=float, default=float(data.get("eps_decay", 1000)))
parser.add_argument("--eps-schedule", type=str, choices=["exp", "linear"], default=str(data.get("eps_schedule", "exp")))
parser.add_argument("--seed", type=int, default=int(data.get("seed", 42)))
parser.add_argument("--target-update-interval", type=int, default=int(data.get("target_update_interval", 1)))
parser.add_argument("--grad-clip", type=float, default=float(data.get("grad_clip", 10.0)))
parser.add_argument("--amp", action=argparse.BooleanOptionalAction, default=None)
parser.add_argument("--compile", dest="compile", action=argparse.BooleanOptionalAction, default=False)
parser.add_argument("--double-dqn", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("--dueling", action=argparse.BooleanOptionalAction, default=False)
parser.add_argument("--per", action=argparse.BooleanOptionalAction, default=False)
parser.add_argument("--per-alpha", type=float, default=float(data.get("per_alpha", 0.6)))
parser.add_argument("--per-beta-start", type=float, default=float(data.get("per_beta_start", 0.4)))
parser.add_argument("--per-beta-frames", type=int, default=int(data.get("per_beta_frames", 200000)))
parser.add_argument("--profile", action=argparse.BooleanOptionalAction, default=os.getenv("TRAIN_PROFILE", "0") == "1")
parser.add_argument("--profile-interval", type=float, default=float(os.getenv("TRAIN_PROFILE_INTERVAL", "10")))
parser.add_argument("--eval-interval", type=int, default=int(data.get("eval_interval", 10)))
parser.add_argument("--eval-episodes", type=int, default=int(data.get("eval_episodes", 3)))
parser.add_argument("--eval-epsilon", type=float, default=float(data.get("eval_epsilon", 0.05)))
parser.add_argument("--auto-batch", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("--render-every", type=int, default=int(os.getenv("RENDER_EVERY", "20")))
args = parser.parse_args()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
use_amp = args.amp if args.amp is not None else device.type == "cuda"

if device.type == "cuda":
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.set_float32_matmul_precision("high")

print("[DEVICE CHECK] cuda:", torch.cuda.is_available())
print("[DEVICE CHECK] torch:", torch.__version__)
if torch.cuda.is_available():
    print("[DEVICE CHECK] name:", torch.cuda.get_device_name(0))
    props = torch.cuda.get_device_properties(0)
    print("[DEVICE CHECK] vram:", round(props.total_memory / (1024 ** 3), 2), "GB")
print("[DEVICE CHECK] device:", device)
print("[DEVICE CHECK] amp:", use_amp)

# ===== perf knobs =====
RENDER_EVERY = args.render_every  # 0 = выключить рендер полностью
UPDATES_PER_STEP = args.updates_per_step
# ======================


DEFAULT_MISSION_NAME = "only_war"

def to_np_state(s):
    if isinstance(s, (dict, collections.OrderedDict)):
        return np.array(list(s.values()), dtype=np.float32)
    return np.array(s, dtype=np.float32)

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

def set_seed(seed):
    np.random.seed(seed)
    torch.manual_seed(seed)
    random_seed = seed % (2**32 - 1)
    random.seed(random_seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

class TrainingProfiler:
    def __init__(self, interval_s=10.0, enabled=False):
        self.interval_s = interval_s
        self.enabled = enabled
        self.last_report = time.perf_counter()
        self.env_time = 0.0
        self.update_time = 0.0
        self.env_steps = 0
        self.updates = 0
        self.samples = 0
        self.batch_time = 0.0

    def record_env_step(self, dt):
        if not self.enabled:
            return
        self.env_time += dt
        self.env_steps += 1

    def record_update(self, dt, batch_size):
        if not self.enabled:
            return
        self.update_time += dt
        self.updates += 1
        self.samples += batch_size
        self.batch_time += dt

    def maybe_report(self):
        if not self.enabled:
            return
        now = time.perf_counter()
        elapsed = now - self.last_report
        if elapsed < self.interval_s:
            return
        total = max(self.env_time + self.update_time, 1e-6)
        env_share = self.env_time / total
        upd_share = self.update_time / total
        fps = self.env_steps / max(elapsed, 1e-6)
        updates_sec = self.updates / max(elapsed, 1e-6)
        samples_sec = self.samples / max(elapsed, 1e-6)
        avg_batch_time = self.batch_time / max(self.updates, 1)
        print(
            f"[profile] fps={fps:.1f} updates/s={updates_sec:.1f} samples/s={samples_sec:.1f} "
            f"avg_batch_time={avg_batch_time:.4f}s env%={env_share*100:.1f} upd%={upd_share*100:.1f}"
        )
        if torch.cuda.is_available():
            alloc = torch.cuda.memory_allocated() / (1024 ** 2)
            reserved = torch.cuda.memory_reserved() / (1024 ** 2)
            print(f"[profile] cuda mem alloc={alloc:.0f}MB reserved={reserved:.0f}MB")

        self.last_report = now
        self.env_time = 0.0
        self.update_time = 0.0
        self.env_steps = 0
        self.updates = 0
        self.samples = 0
        self.batch_time = 0.0

def auto_tune_batch_size(batch_size, max_batch_size):
    if device.type != "cuda" or not args.auto_batch:
        return batch_size
    try:
        free_mem, total_mem = torch.cuda.mem_get_info()
    except Exception:
        return batch_size
    free_gb = free_mem / (1024 ** 3)
    if free_gb > 8 and batch_size < max_batch_size:
        tuned = min(max_batch_size, batch_size * 2)
        print(f"[auto-batch] free VRAM {free_gb:.1f}GB -> batch_size {batch_size} -> {tuned}")
        return tuned
    return batch_size

def build_units_from_config():
    if os.path.isfile("gui/data.json"):
        model_units = []
        enemy_units = []
        for i in range(len(initFile.getEnemyUnits())):
            enemy_units.append(
                Unit(
                    unitData(initFile.getEnemyFaction(), initFile.getEnemyUnits()[i]),
                    weaponData(initFile.getEnemyW()[i][0]),
                    weaponData(initFile.getEnemyW()[i][1]),
                    b_len,
                    b_hei,
                )
            )
        for i in range(len(initFile.getModelUnits())):
            model_units.append(
                Unit(
                    unitData(initFile.getModelFaction(), initFile.getModelUnits()[i]),
                    weaponData(initFile.getModelW()[i][0]),
                    weaponData(initFile.getModelW()[i][1]),
                    b_len,
                    b_hei,
                )
            )
        return model_units, enemy_units
    enemy1 = Unit(unitData("Space_Marine", "Eliminator Squad"), weaponData("Bolt Pistol"), weaponData("Close combat weapon"), b_len, b_hei)
    model1 = Unit(unitData("Space_Marine", "Eliminator Squad"), weaponData("Bolt Pistol"), weaponData("Close combat weapon"), b_len, b_hei)

    enemy2 = Unit(unitData("Space_Marine", "Apothecary"), weaponData("Absolver Bolt Pistol"), weaponData("Close combat weapon"), b_len, b_hei)
    model2 = Unit(unitData("Space_Marine", "Apothecary"), weaponData("Absolver Bolt Pistol"), weaponData("Close combat weapon"), b_len, b_hei)
    return [model1, model2], [enemy1, enemy2]

def run_eval(policy_net, eval_episodes, eval_epsilon):
    eval_rewards = []
    eval_vp_diff = []
    eval_wins = 0
    for _ in range(eval_episodes):
        eval_model, eval_enemy = build_units_from_config()
        eval_env = gym.make(
            "40kAI-v0",
            disable_env_checker=True,
            enemy=eval_enemy,
            model=eval_model,
            b_len=b_len,
            b_hei=b_hei,
        )
        attacker_side, defender_side = roll_off_attacker_defender(
            manual_roll_allowed=False,
            log_fn=None,
        )
        deploy_only_war(
            model_units=eval_model,
            enemy_units=eval_enemy,
            b_len=b_len,
            b_hei=b_hei,
            attacker_side=attacker_side,
            log_fn=None,
        )
        post_deploy_setup(log_fn=None)
        eval_env.attacker_side = attacker_side
        eval_env.defender_side = defender_side
        state, info = eval_env.reset(m=eval_model, e=eval_enemy, Type="small", trunc=True)
        done = False
        ep_reward = 0.0
        while not done:
            action = select_action(eval_env, state, eval_epsilon, policy_net, len(eval_model))
            action_dict = convertToDict(action)
            eval_env.enemyTurn(trunc=True)
            next_observation, reward, done, res, info = eval_env.step(action_dict)
            ep_reward += float(reward)
            state = next_observation
        model_vp = int(info.get("model VP", 0))
        player_vp = int(info.get("player VP", 0))
        vp_diff = model_vp - player_vp
        eval_rewards.append(ep_reward)
        eval_vp_diff.append(vp_diff)
        if vp_diff > 0:
            eval_wins += 1
        eval_env.close()
    winrate = eval_wins / max(eval_episodes, 1)
    avg_reward = sum(eval_rewards) / max(len(eval_rewards), 1)
    avg_vp = sum(eval_vp_diff) / max(len(eval_vp_diff), 1)
    return winrate, avg_reward, avg_vp

TAU = args.tau
LR = args.lr

# ============================================================
# (C) Несколько обучающих апдейтов на один шаг среды
# ============================================================
UPDATES_PER_STEP = int(args.updates_per_step)  # 1 = как было раньше
WARMUP_STEPS     = int(args.warmup_steps)      # 0 = без прогрева

b_len = 60
b_hei = 40

print("\nTraining...\n")

set_seed(args.seed)

enemy = []
model = []

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
else:
    model, enemy = build_units_from_config()

if not model or not enemy:
    model, enemy = build_units_from_config()

numLifeT = 0

verbose = os.getenv("VERBOSE_LOGS", "0") == "1"
log_fn = print if verbose else None
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

# state может быть np.array или OrderedDict
if isinstance(state, dict) or "OrderedDict" in str(type(state)):
    n_observations = len(list(state.values()))
else:
    n_observations = int(np.array(state).shape[0])


policy_net = DQN(n_observations, n_actions, dueling=args.dueling).to(device)
target_net = DQN(n_observations, n_actions, dueling=args.dueling).to(device)
target_net.load_state_dict(policy_net.state_dict())
target_net.eval()

if args.compile:
    try:
        policy_net = torch.compile(policy_net)
    except Exception as exc:
        print(f"[compile] torch.compile unavailable: {exc}")

adamw_kwargs = {"lr": LR, "amsgrad": True}
if device.type == "cuda":
    try:
        optimizer = optim.AdamW(policy_net.parameters(), **adamw_kwargs, fused=True)
    except TypeError:
        optimizer = optim.AdamW(policy_net.parameters(), **adamw_kwargs)
else:
    optimizer = optim.AdamW(policy_net.parameters(), **adamw_kwargs)
if args.per:
    memory = PrioritizedReplayMemory(args.replay_size, alpha=args.per_alpha)
else:
    memory = ReplayMemory(args.replay_size)

batch_size = auto_tune_batch_size(args.batch_size, args.max_batch_size)
scaler = torch.cuda.amp.GradScaler(enabled=use_amp and device.type == "cuda")

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
os.makedirs(fold, exist_ok=True)
randNum = np.random.randint(0, 10000000)
metrics = metrics(fold, randNum, date)
verbose_log = []

rewArr = []
ep_rows = [] 

epLen = 0

profiler = TrainingProfiler(interval_s=args.profile_interval, enabled=args.profile)
best_eval_winrate = -1.0
last_loss_mean = 0.0
last_q_mean = 0.0

total_updates = 0
while end == False:
    epLen += 1
    epsilon = epsilon_by_step(steps_done, args.eps_start, args.eps_end, args.eps_decay, args.eps_schedule)
    action = select_action(env, state, epsilon, policy_net, len(model))
    action_dict = convertToDict(action)
    if trunc == False:
        print(env.get_info())

    env_start = time.perf_counter()
    env.enemyTurn(trunc=trunc)
    next_observation, reward, done, res, info = env.step(action_dict)
    profiler.record_env_step(time.perf_counter() - env_start)
    rewArr.append(float(reward))


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

    state_np = to_np_state(state)
    next_state_np = None if done else to_np_state(next_observation)
    action_np = action.numpy()[0]
    memory.push(state_np, action_np, next_state_np, float(reward))
    state = next_observation

    # =========================
    # ✅ Несколько обучающих апдейтов на 1 шаг среды
    losses = []
    qs = []

    if i >= WARMUP_STEPS:
        for _ in range(UPDATES_PER_STEP):
            per_beta = min(1.0, args.per_beta_start + (1.0 - args.per_beta_start) * (steps_done / max(args.per_beta_frames, 1)))
            update_start = time.perf_counter()
            try:
                loss_q = optimize_model(
                    policy_net,
                    target_net,
                    optimizer,
                    memory,
                    n_observations,
                    batch_size=batch_size,
                    gamma=args.gamma,
                    per=args.per,
                    per_beta=per_beta,
                    amp=use_amp,
                    scaler=scaler,
                    grad_clip=args.grad_clip,
                    double_dqn=args.double_dqn,
                )
            except RuntimeError as exc:
                if "out of memory" in str(exc).lower():
                    torch.cuda.empty_cache()
                    if batch_size > 64:
                        new_batch = max(64, batch_size // 2)
                        if new_batch != batch_size:
                            print(f"[oom] reducing batch_size {batch_size} -> {new_batch}")
                            batch_size = new_batch
                            continue
                raise
            profiler.record_update(time.perf_counter() - update_start, batch_size)

            if loss_q is not None:
                loss, q_mean = loss_q
                losses.append(loss)
                qs.append(q_mean)

            total_updates += 1
            if total_updates % max(args.target_update_interval, 1) == 0:
                with torch.no_grad():
                    for p_tgt, p in zip(target_net.parameters(), policy_net.parameters()):
                        p_tgt.data.mul_(1.0 - TAU)
                        p_tgt.data.add_(p.data, alpha=TAU)

    # чтобы график loss не раздувался в 100 раз — пишем среднее за env-step
    if len(losses) > 0:
        loss_mean = torch.stack(losses).mean().item()
        metrics.updateLoss(loss_mean)
        last_loss_mean = loss_mean
        if len(qs) > 0:
            last_q_mean = torch.stack(qs).mean().item()
    else:
        metrics.updateLoss(0)
    # =========================



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
        verbose_log.append(
            f"[episode] {numLifeT}/{totLifeT} reward={ep_reward:.3f} vp_diff={vp_diff} "
            f"eps={epsilon:.4f} loss={last_loss_mean:.6f} q={last_q_mean:.3f}"
        )

        if args.eval_interval > 0 and numLifeT % args.eval_interval == 0:
            winrate, avg_eval_rew, avg_vp = run_eval(policy_net, args.eval_episodes, args.eval_epsilon)
            print(f"[eval] winrate={winrate:.2f} avg_reward={avg_eval_rew:.2f} avg_vp_diff={avg_vp:.2f}")
            if winrate > best_eval_winrate:
                best_eval_winrate = winrate
                best_path = f"models/{name}/best-model-{date}.pth"
                torch.save(
                    {
                        "policy_net": policy_net.state_dict(),
                        "target_net": target_net.state_dict(),
                        "optimizer": optimizer.state_dict(),
                        "metadata": {
                            "schema_version": 1,
                            "action_keys": ordered_keys,
                            "hyperparams": vars(args),
                        },
                    },
                    best_path,
                )
                print(f"[eval] new best -> {best_path}")

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
    steps_done += 1
    profiler.maybe_report()

env.close()

with open('trainRes.txt', 'w') as f:
    for i in range(len(inText)):
        f.write(inText[i])
        f.write('\n')
if verbose_log:
    os.makedirs("metrics", exist_ok=True)
    verbose_path = os.path.join("metrics", f"train_verbose_{randNum}.log")
    with open(verbose_path, "w") as f:
        for line in verbose_log:
            f.write(line)
            f.write("\n")
    print(f"[log] verbose saved: {verbose_path}")

# Делать gif только если мы реально сохраняли кадры
if RENDER_EVERY > 0:
    has_frames = os.path.isdir("display") and any(os.listdir("display"))
    if has_frames:
        if totLifeT > 30:
            genDisplay.makeGif(numOfLife=totLifeT, trunc=True)
        else:
            genDisplay.makeGif(numOfLife=totLifeT)
    else:
        print("[render] display/ empty -> gif skipped")
else:
    print("[render] RENDER_EVERY=0 -> gif skipped")


metrics.lossCurve()
metrics.showRew()
metrics.showEpLen()

save_extra_metrics(run_id=str(randNum), ep_rows=ep_rows, metrics_dir="metrics")
metrics.createJson()
print("Generated metrics")

torch.save({
    "policy_net": policy_net.state_dict(),
    "target_net": target_net.state_dict(),
    "optimizer": optimizer.state_dict(),
    "metadata": {
        "schema_version": 1,
        "action_keys": ordered_keys,
        "hyperparams": vars(args),
    },
}, ("models/{}/model-{}.pth".format(name, date)))

toSave = [env, model, enemy]

with open(fileName, "wb") as file:
    pickle.dump(toSave, file)

if os.path.isfile("gui/data.json"):
    initFile.delFile()
