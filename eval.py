import argparse
import datetime
import importlib
import os
import pickle
import sys
import types
from collections import Counter
from statistics import median
from typing import Optional

import torch

from core.engine.agent_registry import compatible_contracts, load_agent_by_id, make_env_contract
from core.engine.game_controller import n_actions_from_env
from core.engine.mission import (
    check_end_of_battle,
    normalize_mission_name,
    deploy_for_mission,
    post_deploy_setup,
)
from core.envs.warhamEnv import roll_off_attacker_defender
from core.models.DQN import DQN
from core.models.PPO import ActorCriticMultiHead
from core.models.utils import normalize_state_dict
from core.models.opponent_adapter import build_policy_fn, load_agent_opponent

import gymnasium as gym
import core.envs  # noqa: F401 (регистрация '40kAI-v0')
from project_paths import AGENT_TRAIN_LOG_PATH, ARTIFACTS_MODELS_DIR, ensure_runtime_dirs

AGENT_TRAIN_LOG_FILE = str(AGENT_TRAIN_LOG_PATH.relative_to(AGENT_TRAIN_LOG_PATH.parent.parent))
os.environ.setdefault("AGENT_LOG_FILE", AGENT_TRAIN_LOG_FILE)
from core.models.utils import build_shoot_action_mask, build_action_masks_by_head, convertToDict, unwrap_env


def _append_eval_log(message: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ensure_runtime_dirs()
    log_path = str(AGENT_TRAIN_LOG_PATH)
    try:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"{timestamp} | [EVAL] {message}\n")
    except Exception:
        return


def _install_pickle_compat_aliases() -> None:
    aliases = {
        "gym_mod": "core",
        "gym_mod.engine": "core.engine",
        "gym_mod.envs": "core.envs",
        "model": "core.models",
        "model.DQN": "core.models.DQN",
        "model.PPO": "core.models.PPO",
        "model.memory": "core.models.memory",
        "model.utils": "core.models.utils",
        "model.ppo_buffer": "core.models.ppo_buffer",
        "model.opponent_adapter": "core.models.opponent_adapter",
    }
    for old_name, new_name in aliases.items():
        if old_name in sys.modules:
            continue
        try:
            sys.modules[old_name] = importlib.import_module(new_name)
        except Exception:
            pass
    sys.modules.setdefault("gym_mod", types.ModuleType("gym_mod"))
    sys.modules.setdefault("model", types.ModuleType("model"))


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
        save_path = str(ARTIFACTS_MODELS_DIR) + os.sep
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

    _install_pickle_compat_aliases()
    with open(pickle_path, "rb") as handle:
        env, model, enemy = pickle.load(handle)

    checkpoint = _load_checkpoint_payload(checkpoint_path)
    return env, model, enemy, checkpoint, pickle_path, checkpoint_path


def _build_env_from_train_roster():
    """
    Fallback для eval без legacy .pickle:
    создаём env и юнитов из текущего roster_config (как в train.py).
    """
    try:
        from train import _build_units_from_config, _load_roster_config
    except Exception as exc:
        return None, None, None, str(exc)
    try:
        roster_config = _load_roster_config()
        b_len = int(roster_config.get("b_len", 40))
        b_hei = int(roster_config.get("b_hei", 60))
        enemy_units, model_units = _build_units_from_config(roster_config, b_len, b_hei)
        env = gym.make(
            "40kAI-v0",
            disable_env_checker=True,
            enemy=enemy_units,
            model=model_units,
            b_len=b_len,
            b_hei=b_hei,
        )
        return env, model_units, enemy_units, None
    except Exception as exc:
        return None, None, None, str(exc)


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


def select_action_with_epsilon_ppo(env, state, policy_net, epsilon, len_model):
    masks_cpu = build_action_masks_by_head(env, len_model, log_fn=None, debug=False)
    masks = [m.to(state.device).unsqueeze(0) for m in masks_cpu]
    deterministic = epsilon <= 0
    with torch.no_grad():
        actions, _, _ = policy_net.act(state, masks_by_head=masks, deterministic=deterministic)
    return actions.to("cpu")


def run_episode(env, model_units, enemy_units, policy_net, epsilon, device, algo: str, opponent_policy_fn=None):
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
    episode_len = 0
    total_reward = 0.0
    while not done:
        if opponent_policy_fn is not None:
            env_unwrapped.enemyTurn(trunc=True, policy_fn=opponent_policy_fn)
        else:
            env_unwrapped.enemyTurn(trunc=True)
        if env_unwrapped.game_over:
            info = env_unwrapped.get_info()
            break

        state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        if algo == "ppo":
            action = select_action_with_epsilon_ppo(
                env,
                state_tensor,
                policy_net,
                epsilon,
                len(model_units),
            )
        else:
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
        next_observation, reward, done, _, info = env.step(action_dict)
        try:
            total_reward += float(reward)
        except (TypeError, ValueError):
            pass
        episode_len += 1
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

    model_health = info.get("model health", []) if isinstance(info, dict) else []
    enemy_health = info.get("player health", []) if isinstance(info, dict) else []
    model_alive = info.get("model alive models", []) if isinstance(info, dict) else []
    enemy_alive = info.get("player alive models", []) if isinstance(info, dict) else []

    def _safe_sum(value):
        if isinstance(value, (list, tuple)):
            out = 0.0
            for item in value:
                try:
                    out += float(item)
                except (TypeError, ValueError):
                    continue
            return out
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    hp_diff_model_minus_enemy = _safe_sum(model_health) - _safe_sum(enemy_health)
    kill_diff_model_minus_enemy = _safe_sum(model_alive) - _safe_sum(enemy_alive)
    return (
        winner,
        end_reason or "unknown",
        vp_diff,
        model_vp,
        enemy_vp,
        episode_len,
        total_reward,
        hp_diff_model_minus_enemy,
        kill_diff_model_minus_enemy,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=50)
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--learner-agent-id", type=str, default="")
    parser.add_argument("--opponent-agent-id", type=str, default="")
    parser.add_argument("--opponent-policy", type=str, default="mirror")
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
        # Fallback: если указаны agent-id, можем построить env без legacy pickle.
        if (args.learner_agent_id or "").strip():
            env, model_units, enemy_units, err = _build_env_from_train_roster()
            if env is None:
                log(
                    "[ERROR] Не удалось собрать окружение без .pickle. "
                    "Где: eval.py (_build_env_from_train_roster). "
                    f"Детали: {err}"
                )
                return 0
            checkpoint = {}
            pickle_path = "generated_from_roster"
            checkpoint_path = "registry_only"
            log("[EVAL] legacy .pickle не найден: использую roster_config из train.py.")
        else:
            if pickle_path and checkpoint_path is None:
                log(
                    "[ERROR] Не найден checkpoint для выбранной модели. "
                    "Где: eval.py (load_latest_model/_find_checkpoint_for_pickle). "
                    f"Что делать: проверьте .pth рядом с .pickle. model={pickle_path}"
                )
            else:
                log("[ERROR] Модель не найдена. Проверьте папку artifacts/models/ и наличие файлов .pickle/.pth.")
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
    n_actions = n_actions_from_env(env, len(model_units))
    n_observations = len(state)
    eval_contract = make_env_contract(
        n_observations=n_observations,
        n_actions=n_actions,
        mission_name=mission_name,
        ruleset_version=str(os.getenv("RULESET_VERSION", "only_war_v1")),
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    policy_state = None
    learner_algo_override = ""
    selected_agent_id = (args.learner_agent_id or "").strip()
    if selected_agent_id:
        try:
            payload = load_agent_by_id(selected_agent_id)
        except Exception as exc:
            log(
                f"[ERROR] Не удалось загрузить learner-agent-id={selected_agent_id}: {exc}. "
                "Что делать: обновите список агентов в GUI или выберите существующий agent_id из artifacts/models/agents."
            )
            return 0
        ok, reason = compatible_contracts(eval_contract, payload.get("contract", {}))
        if not ok:
            log(
                f"[ERROR] Несовместимый learner-agent-id={selected_agent_id}: {reason}. "
                "Где: eval.py (compatible_contracts). Что делать: выберите агента с тем же контрактом окружения."
            )
            return 1
        policy_state = payload.get("policy_state")
        meta = payload.get("meta") if isinstance(payload, dict) else {}
        learner_algo_override = str((meta or {}).get("algo", "")).strip().lower()
        if learner_algo_override not in {"dqn", "ppo"}:
            target_state_guess = payload.get("target_state") if isinstance(payload, dict) else None
            learner_algo_override = "dqn" if isinstance(target_state_guess, dict) else "ppo"
        log(f"Используется learner-agent-id={selected_agent_id} (policy из registry).")
    else:
        policy_state = _extract_policy_state_dict(checkpoint)

    opponent_agent_id = (args.opponent_agent_id or "").strip()
    opponent_policy_fn = None
    if opponent_agent_id:
        try:
            opp = load_agent_opponent(agent_id=opponent_agent_id, expected_contract=eval_contract)
            opponent_policy_fn = build_policy_fn(env=env, len_model=len(enemy_units), opponent=opp, deterministic=True)
            log(
                f"Оппонент через registry: opponent-agent-id={opponent_agent_id}, algo={opp.algo} (deterministic)."
            )
        except Exception as exc:
            log(
                f"[ERROR] Не удалось загрузить opponent-agent-id={opponent_agent_id}: {exc}. "
                "Что делать: выберите оппонента с тем же контрактом."
            )
            return 1

    if not isinstance(policy_state, dict):
        log(
            "[ERROR] В checkpoint отсутствует policy state_dict. "
            "Где: eval.py (_extract_policy_state_dict). "
            "Что делать: укажите корректный .pth, сохранённый train.py."
        )
        return 0

    algo = learner_algo_override or (
        str(checkpoint.get("algo", "dqn")).strip().lower() if isinstance(checkpoint, dict) else "dqn"
    )
    if algo == "ppo":
        ppo_state = checkpoint.get("actor_critic") if isinstance(checkpoint, dict) else None
        if not isinstance(ppo_state, dict):
            ppo_state = policy_state
        policy_net = ActorCriticMultiHead(n_observations, n_actions).to(device)
        policy_net.load_state_dict(normalize_state_dict(ppo_state))
        policy_net.eval()
    else:
        net_type = checkpoint.get("net_type") if isinstance(checkpoint, dict) else None
        dueling = net_type == "dueling"
        if not dueling:
            if any(key.startswith("value_heads.") for key in policy_state):
                dueling = True
        dist_type = str(os.getenv("DIST_TYPE", "iqn")).strip().lower() or "iqn"
        iqn_n_quant = int(os.getenv("IQN_N_QUANTILES", "32"))
        iqn_n_target = int(os.getenv("IQN_N_TARGET_QUANTILES", "32"))
        iqn_n_tau = int(os.getenv("IQN_N_TAU_SAMPLES", "32"))
        iqn_embed = int(os.getenv("IQN_EMBED_DIM", "64"))
        noisy_sigma0 = float(os.getenv("NOISY_SIGMA0", "0.5"))
        policy_net = DQN(
            n_observations, n_actions, dueling=dueling, noisy=True,
            noisy_sigma0=noisy_sigma0, distributional=dist_type,
            iqn_num_quantiles=iqn_n_quant, iqn_num_target_quantiles=iqn_n_target,
            iqn_num_tau_samples=iqn_n_tau, iqn_embed_dim=iqn_embed
        ).to(device)
        target_net = DQN(
            n_observations, n_actions, dueling=dueling, noisy=True,
            noisy_sigma0=noisy_sigma0, distributional=dist_type,
            iqn_num_quantiles=iqn_n_quant, iqn_num_target_quantiles=iqn_n_target,
            iqn_num_tau_samples=iqn_n_tau, iqn_embed_dim=iqn_embed
        ).to(device)
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
        f"модель={os.path.basename(pickle_path)}, checkpoint={os.path.basename(checkpoint_path)}, "
            f"heuristic_mode={str(os.getenv('HEURISTIC_MODE', 'v2')).strip().lower() or 'v2'}, algo={algo}."
    )

    learner_side = str(os.getenv("LEARNER_SIDE", "P1")).strip().upper() or "P1"
    if learner_side not in {"P1", "P2"}:
        learner_side = "P1"
    opponent_side = "P2" if learner_side == "P1" else "P1"

    wins = 0
    losses = 0
    draws = 0
    p1_wins = 0
    p2_wins = 0
    vp_diffs = []
    p1_vps = []
    p2_vps = []
    ep_lens = []
    hp_diffs_p1_minus_p2 = []
    kill_diffs_p1_minus_p2 = []
    rewards_learner = []
    end_reasons_v2 = Counter()

    for idx in range(1, games + 1):
        (
            winner,
            end_reason,
            vp_diff,
            model_vp,
            enemy_vp,
            episode_len,
            total_reward,
            hp_diff_model_minus_enemy,
            kill_diff_model_minus_enemy,
        ) = run_episode(
            env, model_units, enemy_units, policy_net, epsilon, device, algo, opponent_policy_fn=opponent_policy_fn
        )
        if learner_side == "P1":
            p1_vp = model_vp
            p2_vp = enemy_vp
            vp_diff_p1_minus_p2 = vp_diff
            hp_diff_p1_minus_p2 = hp_diff_model_minus_enemy
            kill_diff_p1_minus_p2 = kill_diff_model_minus_enemy
        else:
            p1_vp = enemy_vp
            p2_vp = model_vp
            vp_diff_p1_minus_p2 = -vp_diff
            hp_diff_p1_minus_p2 = -hp_diff_model_minus_enemy
            kill_diff_p1_minus_p2 = -kill_diff_model_minus_enemy

        vp_diffs.append(vp_diff)
        p1_vps.append(p1_vp)
        p2_vps.append(p2_vp)
        ep_lens.append(int(episode_len))
        hp_diffs_p1_minus_p2.append(float(hp_diff_p1_minus_p2))
        kill_diffs_p1_minus_p2.append(float(kill_diff_p1_minus_p2))
        rewards_learner.append(float(total_reward))
        if winner == "model":
            wins += 1
            winner_side = learner_side
        elif winner == "enemy":
            losses += 1
            winner_side = opponent_side
        else:
            draws += 1
            winner_side = "draw"

        if winner_side == "P1":
            p1_wins += 1
        elif winner_side == "P2":
            p2_wins += 1

        if end_reason == "wipeout_enemy":
            end_reasons_v2["wipeout_" + learner_side.lower()] += 1
        elif end_reason == "wipeout_model":
            end_reasons_v2["wipeout_" + opponent_side.lower()] += 1
        else:
            end_reasons_v2[end_reason] += 1
        log(
            "Игра "
            f"{idx}/{games}: "
            f"winner={winner} "
            f"winner_side={winner_side} "
            f"model_vp={model_vp} "
            f"enemy_vp={enemy_vp} "
            f"vp_diff_model_minus_enemy={vp_diff} "
            f"p1_vp={p1_vp} "
            f"p2_vp={p2_vp} "
            f"vp_diff_p1_minus_p2={vp_diff_p1_minus_p2} "
            f"episode_len={episode_len} "
            f"reward_learner={total_reward:.3f} "
            f"hp_diff_p1_minus_p2={hp_diff_p1_minus_p2:.3f} "
            f"kill_diff_p1_minus_p2={kill_diff_p1_minus_p2:.3f} "
            f"end_reason={end_reason}"
        )

    winrate_p1_all = p1_wins / games if games else 0.0
    winrate_p2_all = p2_wins / games if games else 0.0
    winrate_p1_decisive = p1_wins / (p1_wins + p2_wins) if (p1_wins + p2_wins) else 0.0
    winrate_p2_decisive = p2_wins / (p1_wins + p2_wins) if (p1_wins + p2_wins) else 0.0
    avg_vp_diff = sum(vp_diffs) / len(vp_diffs) if vp_diffs else 0.0
    avg_vp_p1 = sum(p1_vps) / len(p1_vps) if p1_vps else 0.0
    avg_vp_p2 = sum(p2_vps) / len(p2_vps) if p2_vps else 0.0
    avg_vp_diff_p1_minus_p2 = avg_vp_p1 - avg_vp_p2
    avg_ep_len = sum(ep_lens) / len(ep_lens) if ep_lens else 0.0
    avg_reward_learner = sum(rewards_learner) / len(rewards_learner) if rewards_learner else 0.0
    avg_hp_diff_p1_minus_p2 = sum(hp_diffs_p1_minus_p2) / len(hp_diffs_p1_minus_p2) if hp_diffs_p1_minus_p2 else 0.0
    avg_kill_diff_p1_minus_p2 = (
        sum(kill_diffs_p1_minus_p2) / len(kill_diffs_p1_minus_p2) if kill_diffs_p1_minus_p2 else 0.0
    )

    turn_limit_count = int(end_reasons_v2.get("turn_limit", 0))
    wipeout_p1_count = int(end_reasons_v2.get("wipeout_p1", 0))
    wipeout_p2_count = int(end_reasons_v2.get("wipeout_p2", 0))

    log(
        "[SUMMARY_V2] "
        f"p1_wins={p1_wins} p2_wins={p2_wins} draws={draws} "
        f"winrate_p1_all={winrate_p1_all:.3f} winrate_p2_all={winrate_p2_all:.3f} "
        f"winrate_p1_decisive={winrate_p1_decisive:.3f} winrate_p2_decisive={winrate_p2_decisive:.3f} "
        f"avg_vp_p1={avg_vp_p1:.3f} avg_vp_p2={avg_vp_p2:.3f} "
        f"avg_vp_diff_p1_minus_p2={avg_vp_diff_p1_minus_p2:.3f} "
        f"avg_reward_learner={avg_reward_learner:.3f} "
        f"avg_ep_len={avg_ep_len:.3f} "
        f"avg_hp_diff_p1_minus_p2={avg_hp_diff_p1_minus_p2:.3f} "
        f"avg_kill_diff_p1_minus_p2={avg_kill_diff_p1_minus_p2:.3f} "
        f"turn_limit_count={turn_limit_count} wipeout_p1_count={wipeout_p1_count} wipeout_p2_count={wipeout_p2_count} "
        f"end_reasons={dict(end_reasons_v2)}"
    )

    log("[DETAIL] ---------- Подробный итог оценки ----------")
    log(f"[DETAIL] Стороны матча: P1 vs P2")
    log(f"[DETAIL] Итог серии P1/P2/Draw: {p1_wins}/{p2_wins}/{draws}")
    log(f"[DETAIL] Winrate P1 (все/решающие): {winrate_p1_all:.3f}/{winrate_p1_decisive:.3f}")
    log(f"[DETAIL] Winrate P2 (все/решающие): {winrate_p2_all:.3f}/{winrate_p2_decisive:.3f}")
    log(f"[DETAIL] Avg награда learner ({learner_side}): {avg_reward_learner:.3f}")
    log(f"[DETAIL] VP P1/P2 (avg): {avg_vp_p1:.3f}/{avg_vp_p2:.3f}")
    log(f"[DETAIL] Avg VP diff (P1-P2): {avg_vp_diff_p1_minus_p2:.3f}")
    log(f"[DETAIL] Avg HP diff (P1-P2): {avg_hp_diff_p1_minus_p2:.3f}")
    log(f"[DETAIL] Avg Kill diff (P1-P2): {avg_kill_diff_p1_minus_p2:.3f}")
    log(f"[DETAIL] Avg длина эпизода: {avg_ep_len:.3f}")
    log(
        "[DETAIL] Причины завершения: "
        f"turn_limit={turn_limit_count}, wipeout_p1={wipeout_p1_count}, wipeout_p2={wipeout_p2_count}, "
        f"raw={dict(end_reasons_v2)}"
    )
    log("[DETAIL] ------------------------------------------------")
    return 0


if __name__ == "__main__":
    sys.exit(main())
