import argparse
import os
import pickle
import sys
from collections import Counter
from typing import Optional

import torch

from gym_mod.engine.deployment import deploy_only_war, post_deploy_setup
from gym_mod.engine.mission import check_end_of_battle
from gym_mod.envs.warhamEnv import roll_off_attacker_defender
from model.DQN import DQN
from model.utils import build_shoot_action_mask, convertToDict, unwrap_env


def log(message: str) -> None:
    if message.startswith("["):
        print(f"[EVAL]{message}", flush=True)
    else:
        print(f"[EVAL] {message}", flush=True)


def load_latest_model(model_path: Optional[str] = None):
    if model_path and model_path != "None":
        pickle_path = model_path
        checkpoint_path = model_path[:-len("pickle")] + "pth"
    else:
        save_path = "models/"
        folders = os.listdir(save_path) if os.path.isdir(save_path) else []
        envs = []
        modelpth = []

        for folder in folders:
            full = os.path.join(save_path, folder)
            if os.path.isdir(full):
                files = os.listdir(full)
                for filename in files:
                    if filename.endswith(".pickle"):
                        envs.append(os.path.join(full, filename))
                    elif filename.endswith(".pth"):
                        modelpth.append(os.path.join(full, filename))

        if not envs or not modelpth:
            return None, None, None, None

        envs.sort(key=lambda x: os.path.getmtime(x))
        modelpth.sort()
        pickle_path = envs[-1]
        checkpoint_path = modelpth[-1]

    with open(pickle_path, "rb") as handle:
        env, model, enemy = pickle.load(handle)

    checkpoint = torch.load(checkpoint_path, map_location="cpu")
    return env, model, enemy, checkpoint


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
    return torch.tensor([action_list], device="cpu")


def run_episode(env, model_units, enemy_units, policy_net, epsilon, device):
    env_unwrapped = unwrap_env(env)
    attacker_side, defender_side = roll_off_attacker_defender(
        manual_roll_allowed=False,
        log_fn=None,
    )

    deploy_only_war(
        model_units=model_units,
        enemy_units=enemy_units,
        b_len=env_unwrapped.b_len,
        b_hei=env_unwrapped.b_hei,
        attacker_side=attacker_side,
        log_fn=None,
    )
    post_deploy_setup(log_fn=None)

    env_unwrapped.attacker_side = attacker_side
    env_unwrapped.defender_side = defender_side

    state, info = env.reset(m=model_units, e=enemy_units, Type="big", trunc=True)

    done = False
    while not done:
        env_unwrapped.enemyTurn(trunc=True)
        if env_unwrapped.game_over:
            info = env_unwrapped.get_info()
            break

        state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        shoot_mask = build_shoot_action_mask(env)
        action = select_action_with_epsilon(
            env,
            state_tensor,
            policy_net,
            epsilon,
            len(model_units),
            shoot_mask=shoot_mask,
        )
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
    vp_diff = info.get("model VP", 0) - info.get("player VP", 0)
    return winner, end_reason or "unknown", vp_diff


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=50)
    parser.add_argument("--model", type=str, default=None)
    args = parser.parse_args()

    games = args.games
    if games < 1:
        log("Некорректное значение N. Укажите число >= 1.")
        return 0

    if os.getenv("FORCE_GREEDY", "0") == "1":
        epsilon = 0.0
    else:
        epsilon_raw = os.getenv("EVAL_EPSILON", "0")
        epsilon = float(epsilon_raw) if epsilon_raw else 0.0

    os.environ.setdefault("MANUAL_DICE", "0")

    env, model_units, enemy_units, checkpoint = load_latest_model(args.model)
    if env is None:
        log("Модель не найдена. Проверьте папку models/ и наличие файлов .pickle/.pth.")
        return 0

    attacker_side, defender_side = roll_off_attacker_defender(
        manual_roll_allowed=False,
        log_fn=None,
    )
    env_unwrapped = unwrap_env(env)
    deploy_only_war(
        model_units=model_units,
        enemy_units=enemy_units,
        b_len=env_unwrapped.b_len,
        b_hei=env_unwrapped.b_hei,
        attacker_side=attacker_side,
        log_fn=None,
    )
    post_deploy_setup(log_fn=None)
    env_unwrapped.attacker_side = attacker_side
    env_unwrapped.defender_side = defender_side

    state, info = env.reset(m=model_units, e=enemy_units, Type="big", trunc=True)
    n_actions = [5, 2, len(info["player health"]), len(info["player health"]), 5, len(info["model health"])]
    for _ in range(len(model_units)):
        n_actions.append(12)
    n_observations = len(state)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    net_type = checkpoint.get("net_type") if isinstance(checkpoint, dict) else None
    dueling = net_type == "dueling"
    if not dueling and isinstance(checkpoint, dict):
        policy_state = checkpoint.get("policy_net", {})
        if any(key.startswith("value_heads.") for key in policy_state):
            dueling = True

    policy_net = DQN(n_observations, n_actions, dueling=dueling).to(device)
    target_net = DQN(n_observations, n_actions, dueling=dueling).to(device)
    optimizer = torch.optim.Adam(policy_net.parameters())

    policy_net.load_state_dict(checkpoint["policy_net"])
    target_net.load_state_dict(checkpoint["target_net"])
    optimizer.load_state_dict(checkpoint["optimizer"])

    policy_net.eval()
    target_net.eval()

    log(f"Старт оценки: игр={games}, epsilon={epsilon:.3f}.")

    wins = 0
    vp_diffs = []
    end_reasons = Counter()

    for idx in range(1, games + 1):
        winner, end_reason, vp_diff = run_episode(
            env, model_units, enemy_units, policy_net, epsilon, device
        )
        vp_diffs.append(vp_diff)
        end_reasons[end_reason] += 1
        if winner == "model":
            wins += 1
        log(f"Игра {idx}/{games}: winner={winner} vp_diff={vp_diff} end_reason={end_reason}")

    winrate = wins / games if games else 0.0
    avg_vp_diff = sum(vp_diffs) / len(vp_diffs) if vp_diffs else 0.0
    log(
        "[SUMMARY] "
        f"winrate={winrate:.3f} avg_vp_diff={avg_vp_diff:.3f} "
        f"end_reasons={dict(end_reasons)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
