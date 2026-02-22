import argparse
import os
import pickle
import sys
from collections import Counter
from statistics import median
from typing import Optional

import torch

from gym_mod.engine import Unit, initFile, unitData, weaponData
from gym_mod.engine.mission import (
    board_dims_for_mission,
    check_end_of_battle,
    deploy_for_mission,
    normalize_mission_name,
    post_deploy_setup,
)
from gym_mod.envs.warhamEnv import roll_off_attacker_defender
from model.DQN import DQN
from model.alphazero import flatten_observation, load_alphazero_checkpoint, to_action_dict
from model.utils import normalize_state_dict
from model.utils import build_shoot_action_mask, convertToDict, unwrap_env


def log(message: str) -> None:
    if message.startswith("["):
        print(f"[EVAL]{message}", flush=True)
    else:
        print(f"[EVAL] {message}", flush=True)


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
        enemy_instance_ids = initFile.getEnemyUnitInstanceIds()
        model_instance_ids = initFile.getModelUnitInstanceIds()

        enemy_units = []
        for i in range(len(initFile.getEnemyUnits())):
            count = enemy_counts[i] if i < len(enemy_counts) and enemy_counts[i] > 0 else None
            instance_id = enemy_instance_ids[i] if i < len(enemy_instance_ids) else None
            enemy_units.append({"name": initFile.getEnemyUnits()[i], "weapons": (initFile.getEnemyW()[i][0], initFile.getEnemyW()[i][1]), "count": count, "instance_id": instance_id})

        model_units = []
        for i in range(len(initFile.getModelUnits())):
            count = model_counts[i] if i < len(model_counts) and model_counts[i] > 0 else None
            instance_id = model_instance_ids[i] if i < len(model_instance_ids) else None
            model_units.append({"name": initFile.getModelUnits()[i], "weapons": (initFile.getModelW()[i][0], initFile.getModelW()[i][1]), "count": count, "instance_id": instance_id})

        config["enemy_units"] = enemy_units
        config["model_units"] = model_units

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


def _build_env_from_roster():
    import gymnasium as gym
    import gym_mod  # noqa: F401

    roster = _load_roster_config()
    enemy, model = _build_units_from_config(roster, roster["b_len"], roster["b_hei"])
    env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=roster["b_len"], b_hei=roster["b_hei"])
    env.reset(options={"m": model, "e": enemy, "Type": "small", "trunc": True})
    return env, model, enemy


def _find_checkpoint_for_pickle(pickle_path: str) -> Optional[str]:
    stem, _ = os.path.splitext(pickle_path)
    direct_candidate = f"{stem}.pth"
    if os.path.exists(direct_candidate):
        return direct_candidate
    parent = os.path.dirname(pickle_path)
    if not os.path.isdir(parent):
        return None
    best_path, best_mtime = None, -1.0
    for name in os.listdir(parent):
        if not name.endswith(".pth"):
            continue
        path = os.path.join(parent, name)
        try:
            mtime = os.path.getmtime(path)
        except OSError:
            continue
        if mtime > best_mtime:
            best_mtime = mtime
            best_path = path
    return best_path


def _load_checkpoint_payload(checkpoint_path: str):
    try:
        return torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    except TypeError:
        return torch.load(checkpoint_path, map_location="cpu")


def _extract_policy_state_dict(checkpoint):
    if not isinstance(checkpoint, dict):
        return checkpoint
    for key in ("policy_net", "model_state_dict", "state_dict"):
        value = checkpoint.get(key)
        if isinstance(value, dict):
            return value
    if checkpoint and all(hasattr(value, "shape") for value in checkpoint.values()):
        return checkpoint
    return None


def load_latest_model(model_path: Optional[str] = None):
    if model_path and model_path != "None":
        pickle_path = model_path
    else:
        envs = []
        save_path = "models/"
        folders = os.listdir(save_path) if os.path.isdir(save_path) else []
        for folder in folders:
            full = os.path.join(save_path, folder)
            if os.path.isdir(full):
                for filename in os.listdir(full):
                    if filename.endswith(".pickle"):
                        envs.append(os.path.join(full, filename))
        for name in os.listdir(save_path) if os.path.isdir(save_path) else []:
            if name.endswith(".pickle") and name.startswith("alphazero_model-"):
                envs.append(os.path.join(save_path, name))
        if not envs:
            return None, None, None, None, None, None, "dqn"
        envs.sort(key=lambda x: os.path.getmtime(x))
        pickle_path = envs[-1]

    with open(pickle_path, "rb") as handle:
        payload = pickle.load(handle)

    if isinstance(payload, dict) and payload.get("agent_type") == "alphazero":
        checkpoint_path = payload.get("checkpoint") or _find_checkpoint_for_pickle(pickle_path)
        if checkpoint_path is None:
            return None, None, None, None, pickle_path, None, "alphazero"
        env, model, enemy = _build_env_from_roster()
        checkpoint = _load_checkpoint_payload(checkpoint_path)
        return env, model, enemy, checkpoint, pickle_path, checkpoint_path, "alphazero"

    checkpoint_path = _find_checkpoint_for_pickle(pickle_path)
    if checkpoint_path is None:
        return None, None, None, None, pickle_path, None, "dqn"
    env, model, enemy = payload
    checkpoint = _load_checkpoint_payload(checkpoint_path)
    return env, model, enemy, checkpoint, pickle_path, checkpoint_path, "dqn"


def select_action_with_epsilon(env, state, policy_net, epsilon, len_model, shoot_mask=None):
    if epsilon <= 0:
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
            shoot_choice = valid_indices[torch.randint(0, len(valid_indices), (1,)).item()]
    action_list = [sampled_action["move"], sampled_action["attack"], shoot_choice, sampled_action["charge"], sampled_action["use_cp"], sampled_action["cp_on"]]
    for i in range(len_model):
        action_list.append(sampled_action["move_num_" + str(i)])
    return torch.tensor([action_list], device="cpu")


def select_action_alphazero(env, state, policy_net, shoot_mask=None):
    obs = flatten_observation(state)
    with torch.no_grad():
        logits, _ = policy_net(obs)
    action_keys = list(env.action_space.spaces.keys())
    out = []
    for head_idx, head_logits in enumerate(logits):
        head = head_logits.squeeze(0)
        if head_idx == 2 and shoot_mask is not None:
            mask = torch.as_tensor(shoot_mask, dtype=torch.bool, device=head.device)
            if mask.numel() == head.numel() and mask.any():
                masked = head.clone()
                masked[~mask] = -1e9
                out.append(int(masked.argmax().item()))
                continue
        out.append(int(head.argmax().item()))
    return to_action_dict(action_keys, tuple(out))


def run_episode(env, model_units, enemy_units, policy_net, epsilon, device, agent_type: str):
    env_unwrapped = unwrap_env(env)
    attacker_side, defender_side = roll_off_attacker_defender(manual_roll_allowed=False, log_fn=None)
    mission_name = normalize_mission_name(getattr(env_unwrapped, "mission_name", None))
    deploy_for_mission(mission_name, model_units=model_units, enemy_units=enemy_units, b_len=env_unwrapped.b_len, b_hei=env_unwrapped.b_hei, attacker_side=attacker_side, log_fn=None)
    post_deploy_setup(log_fn=None)
    env_unwrapped.attacker_side = attacker_side
    env_unwrapped.defender_side = defender_side
    state, info = env.reset(options={"m": model_units, "e": enemy_units, "Type": "big", "trunc": True})

    done = False
    while not done:
        env_unwrapped.enemyTurn(trunc=True)
        if env_unwrapped.game_over:
            info = env_unwrapped.get_info()
            break

        shoot_mask = build_shoot_action_mask(env)
        if agent_type == "alphazero":
            action_dict = select_action_alphazero(env, state, policy_net, shoot_mask=shoot_mask)
        else:
            state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
            action = select_action_with_epsilon(env, state_tensor, policy_net, epsilon, len(model_units), shoot_mask=shoot_mask)
            action_dict = convertToDict(action)
        next_observation, _, done, _, info = env.step(action_dict)
        state = next_observation

    end_reason = info.get("end reason", "")
    winner = info.get("winner")
    if not end_reason or winner is None:
        _, fallback_reason, fallback_winner = check_end_of_battle(env_unwrapped)
        if not end_reason:
            end_reason = fallback_reason
        if winner is None:
            winner = fallback_winner
    model_vp = info.get("model VP", 0)
    enemy_vp = info.get("player VP", 0)
    return winner, end_reason or "unknown", model_vp - enemy_vp, model_vp, enemy_vp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=50)
    parser.add_argument("--model", type=str, default=None)
    args = parser.parse_args()

    games = args.games
    if games < 1:
        log("Некорректное значение N. Укажите число >= 1.")
        return 0

    epsilon = 0.0 if os.getenv("FORCE_GREEDY", "0") == "1" else float(os.getenv("EVAL_EPSILON", "0") or "0")
    os.environ.setdefault("MANUAL_DICE", "0")

    env, model_units, enemy_units, checkpoint, pickle_path, checkpoint_path, agent_type = load_latest_model(args.model)
    if env is None:
        if pickle_path and checkpoint_path is None:
            log(f"[ERROR] Не найден checkpoint для выбранной модели. model={pickle_path}")
        else:
            log("[ERROR] Модель не найдена. Проверьте папку models/ и наличие файлов .pickle/.pth.")
        return 0

    state, info = env.reset(options={"m": model_units, "e": enemy_units, "Type": "big", "trunc": True})
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if agent_type == "alphazero":
        policy_net, meta = load_alphazero_checkpoint(checkpoint_path, device=device)
        policy_net = policy_net.to(device)
        policy_net.eval()
        log(f"Старт оценки AlphaZero: игр={games}, модель={os.path.basename(pickle_path)}, checkpoint={os.path.basename(checkpoint_path)}.")
    else:
        n_actions = [5, 2, len(info["player health"]), len(info["player health"]), 5, len(info["model health"])]
        for _ in range(len(model_units)):
            n_actions.append(12)
        n_observations = len(state)

        policy_state = _extract_policy_state_dict(checkpoint)
        if not isinstance(policy_state, dict):
            log("[ERROR] В checkpoint отсутствует policy state_dict. Где: eval.py. Что делать: укажите корректный .pth, сохранённый train.py.")
            return 0

        net_type = checkpoint.get("net_type") if isinstance(checkpoint, dict) else None
        dueling = net_type == "dueling" or any(key.startswith("value_heads.") for key in policy_state)
        policy_net = DQN(n_observations, n_actions, dueling=dueling).to(device)
        policy_net.load_state_dict(normalize_state_dict(policy_state))
        policy_net.eval()
        log(f"Старт оценки: игр={games}, epsilon={epsilon:.3f}, модель={os.path.basename(pickle_path)}, checkpoint={os.path.basename(checkpoint_path)}.")

    wins = losses = draws = 0
    vp_diffs = []
    end_reasons = Counter()

    for idx in range(1, games + 1):
        winner, end_reason, vp_diff, model_vp, enemy_vp = run_episode(env, model_units, enemy_units, policy_net, epsilon, device, agent_type)
        vp_diffs.append(vp_diff)
        end_reasons[end_reason] += 1
        if winner == "model":
            wins += 1
        elif winner == "enemy":
            losses += 1
        else:
            draws += 1
        log(f"Игра {idx}/{games}: winner={winner} model_vp={model_vp} enemy_vp={enemy_vp} vp_diff_model_minus_enemy={vp_diff} end_reason={end_reason}")

    winrate_all = wins / games if games else 0.0
    winrate_no_draw = wins / (wins + losses) if (wins + losses) else 0.0
    avg_vp_diff = sum(vp_diffs) / len(vp_diffs) if vp_diffs else 0.0
    median_vp_diff = median(vp_diffs) if vp_diffs else 0.0
    sorted_reasons = sorted(end_reasons.items(), key=lambda item: (-item[1], item[0]))

    log(f"[SUMMARY] wins={wins} losses={losses} draws={draws} winrate_all={winrate_all:.3f} winrate_no_draw={winrate_no_draw:.3f} avg_vp_diff={avg_vp_diff:.3f} median_vp_diff={median_vp_diff:.3f} end_reasons={dict(end_reasons)}")
    log("[DETAIL] ---------- Подробный итог оценки ----------")
    log(f"[DETAIL] Всего игр: {games}")
    log(f"[DETAIL] Победы/Поражения/Ничьи: {wins}/{losses}/{draws}")
    if sorted_reasons:
        for reason, count in sorted_reasons:
            log(f"[DETAIL]   - {reason}: {count}")
    log("[DETAIL] ------------------------------------------------")
    return 0


if __name__ == "__main__":
    sys.exit(main())
