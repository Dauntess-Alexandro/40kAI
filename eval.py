import argparse
import datetime
import os
import pickle
import sys
from collections import Counter
from statistics import median
from typing import Optional

import torch

from gym_mod.engine.mission import (
    check_end_of_battle,
    normalize_mission_name,
    deploy_for_mission,
    post_deploy_setup,
)
from gym_mod.envs.warhamEnv import roll_off_attacker_defender
from model.DQN import DQN
from model.utils import normalize_state_dict

AGENT_TRAIN_LOG_FILE = "LOGS_FOR_AGENTS_TRAIN.md"
os.environ.setdefault("AGENT_LOG_FILE", AGENT_TRAIN_LOG_FILE)
from model.utils import build_shoot_action_mask, convertToDict, unwrap_env


def _append_eval_log(message: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    script_path = globals().get("__file__") or sys.argv[0] or "eval.py"
    log_path = os.path.join(os.path.dirname(os.path.abspath(script_path)), AGENT_TRAIN_LOG_FILE)
    try:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"{timestamp} | [EVAL] {message}\n")
    except Exception:
        return


def log(message: str) -> None:
    if message.startswith("["):
        rendered = f"[EVAL]{message}"
    else:
        rendered = f"[EVAL] {message}"
    print(rendered, flush=True)
    _append_eval_log(message)


def _find_checkpoint_for_pickle(pickle_path: str) -> Optional[str]:
    stem, _ = os.path.splitext(pickle_path)
    direct_candidate = f"{stem}.pth"
    if os.path.exists(direct_candidate):
        return direct_candidate

    parent = os.path.dirname(pickle_path)
    if not os.path.isdir(parent):
        return None

    best_path = None
    best_mtime = -1.0
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
        save_path = "models/"
        folders = os.listdir(save_path) if os.path.isdir(save_path) else []
        envs = []

        for folder in folders:
            full = os.path.join(save_path, folder)
            if os.path.isdir(full):
                files = os.listdir(full)
                for filename in files:
                    if filename.endswith(".pickle"):
                        envs.append(os.path.join(full, filename))

        if not envs:
            return None, None, None, None, None, None

        envs.sort(key=lambda x: os.path.getmtime(x))
        pickle_path = envs[-1]

    checkpoint_path = _find_checkpoint_for_pickle(pickle_path)
    if checkpoint_path is None:
        return None, None, None, None, pickle_path, None

    with open(pickle_path, "rb") as handle:
        env, model, enemy = pickle.load(handle)

    checkpoint = _load_checkpoint_payload(checkpoint_path)
    return env, model, enemy, checkpoint, pickle_path, checkpoint_path


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

    mission_name = normalize_mission_name(getattr(env_unwrapped, "mission_name", None))
    deploy_for_mission(
        mission_name,
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

    state, info = env.reset(
        options={"m": model_units, "e": enemy_units, "Type": "big", "trunc": True}
    )

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
    model_vp = info.get("model VP", 0)
    enemy_vp = info.get("player VP", 0)
    vp_diff = model_vp - enemy_vp
    return winner, end_reason or "unknown", vp_diff, model_vp, enemy_vp


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

    env, model_units, enemy_units, checkpoint, pickle_path, checkpoint_path = load_latest_model(args.model)
    if env is None:
        if pickle_path and checkpoint_path is None:
            log(
                "[ERROR] Не найден checkpoint для выбранной модели. "
                "Где: eval.py (load_latest_model/_find_checkpoint_for_pickle). "
                f"Что делать: проверьте .pth рядом с .pickle. model={pickle_path}"
            )
        else:
            log("[ERROR] Модель не найдена. Проверьте папку models/ и наличие файлов .pickle/.pth.")
        return 0

    attacker_side, defender_side = roll_off_attacker_defender(
        manual_roll_allowed=False,
        log_fn=None,
    )
    env_unwrapped = unwrap_env(env)
    mission_name = normalize_mission_name(getattr(env_unwrapped, "mission_name", None))
    deploy_for_mission(
        mission_name,
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

    state, info = env.reset(
        options={"m": model_units, "e": enemy_units, "Type": "big", "trunc": True}
    )
    n_actions = [5, 2, len(info["player health"]), len(info["player health"]), 5, len(info["model health"])]
    for _ in range(len(model_units)):
        n_actions.append(12)
    n_observations = len(state)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    policy_state = _extract_policy_state_dict(checkpoint)
    if not isinstance(policy_state, dict):
        log(
            "[ERROR] В checkpoint отсутствует policy state_dict. "
            "Где: eval.py (_extract_policy_state_dict). "
            "Что делать: укажите корректный .pth, сохранённый train.py."
        )
        return 0

    net_type = checkpoint.get("net_type") if isinstance(checkpoint, dict) else None
    dueling = net_type == "dueling"
    if not dueling:
        if any(key.startswith("value_heads.") for key in policy_state):
            dueling = True

    policy_net = DQN(n_observations, n_actions, dueling=dueling).to(device)
    target_net = DQN(n_observations, n_actions, dueling=dueling).to(device)
    policy_net.load_state_dict(normalize_state_dict(policy_state))
    target_state = checkpoint.get("target_net") if isinstance(checkpoint, dict) else None
    if isinstance(target_state, dict):
        target_net.load_state_dict(normalize_state_dict(target_state))
    else:
        target_net.load_state_dict(normalize_state_dict(policy_net.state_dict()))

    policy_net.eval()
    target_net.eval()

    log(
        f"Старт оценки: игр={games}, epsilon={epsilon:.3f}, "
        f"модель={os.path.basename(pickle_path)}, checkpoint={os.path.basename(checkpoint_path)}."
    )

    wins = 0
    losses = 0
    draws = 0
    vp_diffs = []
    end_reasons = Counter()

    for idx in range(1, games + 1):
        winner, end_reason, vp_diff, model_vp, enemy_vp = run_episode(
            env, model_units, enemy_units, policy_net, epsilon, device
        )
        vp_diffs.append(vp_diff)
        end_reasons[end_reason] += 1
        if winner == "model":
            wins += 1
        elif winner == "enemy":
            losses += 1
        else:
            draws += 1
        log(
            "Игра "
            f"{idx}/{games}: "
            f"winner={winner} "
            f"model_vp={model_vp} "
            f"enemy_vp={enemy_vp} "
            f"vp_diff_model_minus_enemy={vp_diff} "
            f"end_reason={end_reason}"
        )

    winrate_all = wins / games if games else 0.0
    winrate_no_draw = wins / (wins + losses) if (wins + losses) else 0.0
    avg_vp_diff = sum(vp_diffs) / len(vp_diffs) if vp_diffs else 0.0
    median_vp_diff = median(vp_diffs) if vp_diffs else 0.0
    min_vp_diff = min(vp_diffs) if vp_diffs else 0.0
    max_vp_diff = max(vp_diffs) if vp_diffs else 0.0
    positive_vp_games = sum(1 for value in vp_diffs if value > 0)
    negative_vp_games = sum(1 for value in vp_diffs if value < 0)
    neutral_vp_games = sum(1 for value in vp_diffs if value == 0)
    sorted_reasons = sorted(end_reasons.items(), key=lambda item: (-item[1], item[0]))
    reason_labels = {
        "turn_limit": "Лимит ходов",
        "wipeout_enemy": "Уничтожение армии противника",
        "wipeout_model": "Уничтожение армии модели",
        "auto": "Авто-завершение",
        "unknown": "Неизвестно",
    }

    log(
        "[SUMMARY] "
        f"wins={wins} losses={losses} draws={draws} "
        f"winrate_all={winrate_all:.3f} "
        f"winrate_no_draw={winrate_no_draw:.3f} "
        f"avg_vp_diff={avg_vp_diff:.3f} "
        f"median_vp_diff={median_vp_diff:.3f} "
        f"end_reasons={dict(end_reasons)}"
    )

    log("[DETAIL] ---------- Подробный итог оценки ----------")
    log(f"[DETAIL] Всего игр: {games}")
    log(f"[DETAIL] Победы/Поражения/Ничьи: {wins}/{losses}/{draws}")
    log(f"[DETAIL] Winrate (все игры): {winrate_all:.3f}")
    log(f"[DETAIL] Winrate (без ничьих): {winrate_no_draw:.3f}")
    log(f"[DETAIL] VP diff (avg/median/min/max): {avg_vp_diff:.3f}/{median_vp_diff:.3f}/{min_vp_diff:.3f}/{max_vp_diff:.3f}")
    log(
        "[DETAIL] VP diff по знаку: "
        f"положительных={positive_vp_games}, отрицательных={negative_vp_games}, нулевых={neutral_vp_games}"
    )
    if sorted_reasons:
        log("[DETAIL] Причины завершения (по частоте):")
        for reason, count in sorted_reasons:
            reason_ru = reason_labels.get(reason, reason)
            log(f"[DETAIL]   - {reason_ru} ({reason}): {count}")
    else:
        log("[DETAIL] Причины завершения: данных нет")
    log("[DETAIL] ------------------------------------------------")
    return 0


if __name__ == "__main__":
    sys.exit(main())
