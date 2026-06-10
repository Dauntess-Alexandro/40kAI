import argparse
import datetime
import importlib
import json
import os
import pickle
import random
import re
import sys
import types
from collections import Counter
from statistics import median
from typing import Optional

import torch

from core.engine.agent_registry import (
    compatible_contracts,
    load_agent_by_id,
    make_env_contract,
    resolve_agent_algo,
)
from core.engine.game_controller import n_actions_from_env
from core.engine.mission import (
    check_end_of_battle,
    normalize_mission_name,
    deploy_for_mission,
    post_deploy_setup,
)
from core.envs.warhamEnv import roll_off_attacker_defender
from core.models.DQN import DQN
from core.models.PPO import make_actor_critic, load_actor_critic_state_dict, ppo_arch_from_payload
from core.models.alphazero_ids import is_az_algo
from core.models.alphazero_model import alphazero_arch_from_payload, load_alphazero_state_dict, make_alphazero_net
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.gumbel_muzero_search import GumbelMuZeroSearch, GumbelMuZeroSearchConfig
from core.models.utils import normalize_state_dict
from core.models.opponent_adapter import build_policy_fn, load_agent_opponent

import gymnasium as gym
import core.envs  # noqa: F401 (регистрация '40kAI-v0')
from project_paths import AGENT_EVAL_LOG_PATH, ARTIFACTS_MODELS_DIR, ensure_runtime_dirs

AGENT_EVAL_LOG_FILE = str(AGENT_EVAL_LOG_PATH.relative_to(AGENT_EVAL_LOG_PATH.parent.parent))
os.environ.setdefault("AGENT_LOG_FILE", AGENT_EVAL_LOG_FILE)
from core.models.utils import build_shoot_action_mask, build_action_masks_by_head, convertToDict, unwrap_env


def _append_eval_log(message: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ensure_runtime_dirs()
    log_path = str(AGENT_EVAL_LOG_PATH)
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


def select_action_with_epsilon(env, state, policy_net, epsilon, len_model, action_masks=None, shoot_mask=None):
    masks_seq = action_masks
    if masks_seq is None and shoot_mask is not None:
        masks_seq = [None] * (6 + int(len_model))
        masks_seq[2] = torch.as_tensor(shoot_mask, dtype=torch.bool)
    if epsilon <= 0:
        with torch.no_grad():
            decision = policy_net(state)
            action = []
            for head_idx, head in enumerate(decision):
                head = head.squeeze(0)
                if masks_seq is not None and head_idx < len(masks_seq):
                    raw_mask = masks_seq[head_idx]
                    if raw_mask is not None:
                        mask = torch.as_tensor(raw_mask, dtype=torch.bool, device=head.device)
                        if mask.numel() == head.numel() and mask.any():
                            masked_head = head.clone()
                            masked_head[~mask] = -1e9
                            action.append(int(masked_head.argmax().item()))
                            continue
                action.append(int(head.argmax().item()))
            return torch.tensor([action], device="cpu")

    sampled_action = env.action_space.sample()
    action_list = [
        sampled_action["move"],
        sampled_action["attack"],
        sampled_action["shoot"],
        sampled_action["charge"],
        sampled_action["use_cp"],
        sampled_action["cp_on"],
    ]
    for i in range(len_model):
        label = "move_num_" + str(i)
        action_list.append(sampled_action[label])
    if masks_seq is not None:
        for idx, raw_mask in enumerate(masks_seq):
            if raw_mask is None or idx >= len(action_list):
                continue
            mask = torch.as_tensor(raw_mask, dtype=torch.bool)
            valid_indices = torch.where(mask)[0].tolist()
            if valid_indices:
                action_list[idx] = int(valid_indices[torch.randint(0, len(valid_indices), (1,)).item()])
    return torch.tensor([action_list], device="cpu")


def select_action_with_epsilon_ppo(env, state, policy_net, epsilon, len_model):
    masks_cpu = build_action_masks_by_head(env, len_model, log_fn=None, debug=False)
    masks = [m.to(state.device).unsqueeze(0) for m in masks_cpu]
    deterministic = epsilon <= 0
    with torch.no_grad():
        actions, _, _ = policy_net.act(state, masks_by_head=masks, deterministic=deterministic)
    return actions.to("cpu")


def select_action_with_epsilon_alphazero(env, state, policy_net, epsilon, len_model):
    masks_cpu = build_action_masks_by_head(env, len_model, log_fn=None, debug=False)
    az_eval_mode = str(os.getenv("AZ_EVAL_MODE", os.getenv("AZ_EVAL_OPPONENT_MODE", "greedy"))).strip().lower() or "greedy"
    if az_eval_mode not in {"greedy", "mcts"}:
        az_eval_mode = "greedy"
    if az_eval_mode == "mcts":
        legal_masks = [m.detach().cpu().numpy().astype(bool) for m in masks_cpu]
        mcts = AlphaZeroFactorizedMCTS(
            policy_net,
            config=MCTSConfig(
                simulations=max(1, int(os.getenv("AZ_EVAL_MCTS_SIMS", "32"))),
                c_puct=float(os.getenv("AZ_EVAL_MCTS_C_PUCT", "1.5")),
                dirichlet_alpha=float(os.getenv("AZ_EVAL_MCTS_DIR_ALPHA", "0.3")),
                dirichlet_eps=float(os.getenv("AZ_EVAL_MCTS_DIR_EPS", "0.0")),
                top_k_per_head=max(1, int(os.getenv("AZ_EVAL_MCTS_TOP_K_PER_HEAD", "8"))),
                max_depth=max(1, int(os.getenv("AZ_EVAL_MCTS_MAX_DEPTH", "1"))),
                mode=str(os.getenv("AZ_EVAL_MCTS_MODE", "tree")).strip().lower() or "tree",
            ),
            device=state.device,
        )
        pi_targets, selected, _value = mcts.run(
            obs=state.squeeze(0).detach().cpu().numpy(),
            legal_masks_by_head=legal_masks,
            temperature=float(os.getenv("AZ_EVAL_MCTS_TEMPERATURE", "0.06")),
            env=env,
            len_model=len_model,
            enemy_policy_fn=None,
        )
        action_list = [int(torch.argmax(torch.tensor(pi)).item()) for pi in pi_targets]
        if not action_list:
            action_list = [int(x) for x in selected]
        return torch.tensor([action_list], device="cpu")
    masks = [m.to(state.device).unsqueeze(0) for m in masks_cpu]
    with torch.no_grad():
        probs, _value = policy_net.infer(state, masks_by_head=masks)
    if epsilon > 0 and random.random() < float(epsilon):
        sampled = env.action_space.sample()
        action_list = [
            sampled["move"], sampled["attack"], sampled["shoot"],
            sampled["charge"], sampled["use_cp"], sampled["cp_on"],
        ]
        for i in range(int(len_model)):
            action_list.append(sampled[f"move_num_{i}"])
        return torch.tensor([action_list], device="cpu")
    action_list = [int(torch.argmax(p.squeeze(0), dim=0).item()) for p in probs]
    return torch.tensor([action_list], device="cpu")


def select_action_with_epsilon_gumbel_muzero(env, state, policy_net, epsilon, len_model):
    masks_cpu = build_action_masks_by_head(env, len_model, log_fn=None, debug=False)
    legal_masks = [m.detach().cpu().numpy().astype(bool) for m in masks_cpu]
    obs_np = state.squeeze(0).detach().cpu().numpy()
    if epsilon > 0 and random.random() < float(epsilon):
        sampled = env.action_space.sample()
        action_list = [
            sampled["move"], sampled["attack"], sampled["shoot"],
            sampled["charge"], sampled["use_cp"], sampled["cp_on"],
        ]
        for i in range(int(len_model)):
            action_list.append(sampled[f"move_num_{i}"])
        return torch.tensor([action_list], device="cpu")
    gmz_eval_mode = str(os.getenv("GMZ_EVAL_MODE", os.getenv("GMZ_OPPONENT_MODE", "search"))).strip().lower() or "search"
    if gmz_eval_mode not in {"search", "greedy"}:
        gmz_eval_mode = "search"
    if gmz_eval_mode == "greedy":
        with torch.no_grad():
            probs, _value = policy_net.infer(
                state,
                masks_by_head=[m.to(state.device).unsqueeze(0) for m in masks_cpu],
            )
        action_list = [int(torch.argmax(p.squeeze(0), dim=0).item()) for p in probs]
        return torch.tensor([action_list], device="cpu")
    search = GumbelMuZeroSearch(
        net=policy_net,
        config=GumbelMuZeroSearchConfig(
            num_simulations=max(1, int(os.getenv("GMZ_EVAL_SIMS", "32"))),
            root_top_k=max(1, int(os.getenv("GMZ_EVAL_ROOT_TOP_K", "8"))),
            temperature=float(os.getenv("GMZ_EVAL_TEMPERATURE", "0.10")),
        ),
        device=state.device,
    )
    pi_targets, _behavior_logits, selected, _value = search.run(
        obs=obs_np, legal_masks_by_head=legal_masks, deterministic=True
    )
    action_list = [int(torch.argmax(torch.tensor(pi)).item()) for pi in pi_targets]
    if not action_list:
        action_list = [int(x) for x in selected]
    return torch.tensor([action_list], device="cpu")


def run_episode(
    env,
    model_units,
    enemy_units,
    policy_net,
    epsilon,
    device,
    algo: str,
    opponent_policy_fn=None,
    learner_side: str = "P1",
):
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
    trace_enabled = str(os.getenv("EVAL_ACTION_TRACE", "1")).strip() == "1"
    trace_max_lines = max(200, int(os.getenv("EVAL_TRACE_MAX_LINES_PER_GAME", "2000")))
    trace_everything = str(os.getenv("EVAL_TRACE_EVERYTHING", "0")).strip() == "1"
    trace_style = str(os.getenv("EVAL_TRACE_STYLE", "warhammer")).strip().lower() or "warhammer"
    opponent_side = "P2" if str(learner_side).upper() == "P1" else "P1"
    trace_lines: list[str] = []
    current_round = 0
    round_stats: dict[int, dict[str, int]] = {}
    move_dir_labels = {
        0: "up",
        1: "left",
        2: "down",
        3: "right",
        4: "stay",
    }

    def _safe_int(v, default=0):
        try:
            return int(v)
        except Exception:
            return int(default)

    def _safe_float(v, default=0.0):
        try:
            return float(v)
        except Exception:
            return float(default)

    def _head_masks_summary() -> str:
        try:
            masks = build_action_masks_by_head(env, len(model_units), log_fn=None, debug=False)
            head_names = ["move", "attack", "shoot", "charge", "use_cp", "cp_on"]
            parts = []
            for i, m in enumerate(masks[:6]):
                m_np = m.detach().cpu().numpy() if hasattr(m, "detach") else m
                total = int(len(m_np))
                valid = int(sum(1 for x in m_np if bool(x)))
                label = head_names[i] if i < len(head_names) else f"h{i}"
                parts.append(f"{label}:{valid}/{total}")
            return ", ".join(parts)
        except Exception:
            return "masks=unavailable"

    def _head_masks_counts() -> dict[str, tuple[int, int]]:
        out = {
            "move": (0, 0),
            "attack": (0, 0),
            "shoot": (0, 0),
            "charge": (0, 0),
            "use_cp": (0, 0),
            "cp_on": (0, 0),
        }
        try:
            masks = build_action_masks_by_head(env, len(model_units), log_fn=None, debug=False)
            for idx, key in enumerate(("move", "attack", "shoot", "charge", "use_cp", "cp_on")):
                if idx >= len(masks):
                    continue
                m = masks[idx]
                m_np = m.detach().cpu().numpy() if hasattr(m, "detach") else m
                total = int(len(m_np))
                valid = int(sum(1 for x in m_np if bool(x)))
                out[key] = (valid, total)
        except Exception:
            pass
        return out

    def _human_action(action_dict: dict) -> str:
        move_val = _safe_int(action_dict.get("move", 4), 4)
        attack_val = _safe_int(action_dict.get("attack", 0), 0)
        shoot_val = _safe_int(action_dict.get("shoot", -1), -1)
        charge_val = _safe_int(action_dict.get("charge", 0), 0)
        use_cp_val = _safe_int(action_dict.get("use_cp", 0), 0)
        cp_on_val = _safe_int(action_dict.get("cp_on", 0), 0)
        move_units = []
        for i_u in range(int(len(model_units))):
            k = f"move_num_{i_u}"
            if k in action_dict:
                move_units.append(str(_safe_int(action_dict.get(k, 0), 0)))
        move_units_text = ",".join(move_units) if move_units else "-"
        return (
            f"move={move_val}({move_dir_labels.get(move_val, 'unk')}) "
            f"attack={attack_val} shoot={shoot_val} charge={charge_val} "
            f"use_cp={use_cp_val} cp_on={cp_on_val} move_num=[{move_units_text}]"
        )

    def _human_action_with_units(action_dict: dict) -> str:
        chunks = [_human_action(action_dict)]
        unit_parts = []
        for i_u in range(int(len(model_units))):
            key = f"move_num_{i_u}"
            if key not in action_dict:
                continue
            unit_name = f"unit{i_u}"
            try:
                ud = model_units[i_u].showUnitData() if i_u < len(model_units) else {}
                candidate = str((ud or {}).get("Name", "")).strip()
                if candidate:
                    unit_name = candidate
            except Exception:
                pass
            unit_parts.append(f"{unit_name}:{_safe_int(action_dict.get(key, 0), 0)}")
        if unit_parts:
            chunks.append(f"units=[{' | '.join(unit_parts)}]")
        return " ; ".join(chunks)

    def _step_verdict(action_dict: dict, masks_counts: dict[str, tuple[int, int]], shoot_targets: int) -> str:
        verdicts: list[str] = []
        attack_v, _attack_t = masks_counts.get("attack", (0, 0))
        charge_v, _charge_t = masks_counts.get("charge", (0, 0))
        shoot_v, _shoot_t = masks_counts.get("shoot", (0, 0))
        move_v, _move_t = masks_counts.get("move", (0, 0))

        move = _safe_int(action_dict.get("move", 4), 4)
        attack = _safe_int(action_dict.get("attack", 0), 0)
        shoot = _safe_int(action_dict.get("shoot", -1), -1)
        charge = _safe_int(action_dict.get("charge", 0), 0)
        use_cp = _safe_int(action_dict.get("use_cp", 0), 0)

        if shoot_targets <= 0 and shoot >= 0:
            verdicts.append("shoot_without_targets")
        if attack_v > 1 and attack == 0:
            verdicts.append("skip_attack_while_options_exist")
        if charge_v > 1 and charge == 0:
            verdicts.append("skip_charge_while_options_exist")
        if shoot_v > 1 and shoot == 0:
            verdicts.append("default_shoot_choice_with_options")
        if move_v > 1 and move == 4:
            verdicts.append("stay_while_move_options_exist")
        if use_cp == 0:
            verdicts.append("cp_not_used")

        if not verdicts:
            return "ok"
        return ",".join(verdicts)

    def _step_verdict_ru(verdict_raw: str) -> str:
        if verdict_raw == "ok":
            return "OK: выбор действий выглядит корректно."
        mapping = {
            "shoot_without_targets": "Выбран shoot без доступных целей.",
            "skip_attack_while_options_exist": "Пропущена атака при доступных вариантах.",
            "skip_charge_while_options_exist": "Пропущен charge при доступных вариантах.",
            "default_shoot_choice_with_options": "Выбран дефолтный shoot при наличии альтернатив.",
            "stay_while_move_options_exist": "Выбран stay при доступных вариантах движения.",
            "cp_not_used": "CP не использован в этот шаг.",
        }
        parts = []
        for token in str(verdict_raw).split(","):
            token = token.strip()
            if not token:
                continue
            parts.append(mapping.get(token, token))
        return " | ".join(parts) if parts else str(verdict_raw)

    def _mask_tuple(masks_counts: dict[str, tuple[int, int]] | None, key: str) -> tuple[int, int]:
        if not isinstance(masks_counts, dict):
            return (0, 0)
        return masks_counts.get(key, (0, 0))

    def _emit_wh40k_phase_report(
        *,
        side_label: str,
        step_no: int,
        action_dict: dict,
        masks_counts: dict[str, tuple[int, int]] | None = None,
        shoot_targets: int | None = None,
    ) -> None:
        move = _safe_int(action_dict.get("move", 4), 4)
        attack = _safe_int(action_dict.get("attack", 0), 0)
        shoot = _safe_int(action_dict.get("shoot", -1), -1)
        charge = _safe_int(action_dict.get("charge", 0), 0)
        use_cp = _safe_int(action_dict.get("use_cp", 0), 0)
        cp_on = _safe_int(action_dict.get("cp_on", 0), 0)

        mv_valid, mv_total = _mask_tuple(masks_counts, "move")
        at_valid, at_total = _mask_tuple(masks_counts, "attack")
        sh_valid, sh_total = _mask_tuple(masks_counts, "shoot")
        ch_valid, ch_total = _mask_tuple(masks_counts, "charge")

        _trace(
            "[WH40K][PHASE][COMMAND] "
            f"step={step_no} side={side_label} use_cp={use_cp} cp_on={cp_on} "
            f"attack_options={at_valid}/{at_total} shoot_options={sh_valid}/{sh_total} charge_options={ch_valid}/{ch_total}"
        )
        _trace(
            "[WH40K][PHASE][MOVE] "
            f"step={step_no} side={side_label} move={move}({move_dir_labels.get(move, 'unk')}) "
            f"move_options={mv_valid}/{mv_total}"
        )
        if shoot_targets is not None:
            _trace(
                "[WH40K][PHASE][SHOOT] "
                f"step={step_no} side={side_label} shoot_target={shoot} targets_available={int(shoot_targets)}"
            )
        else:
            _trace(
                "[WH40K][PHASE][SHOOT] "
                f"step={step_no} side={side_label} shoot_target={shoot} targets_available=unknown"
            )
        _trace(
            "[WH40K][PHASE][CHARGE] "
            f"step={step_no} side={side_label} charge_target={charge} charge_options={ch_valid}/{ch_total}"
        )
        _trace(
            "[WH40K][PHASE][FIGHT] "
            f"step={step_no} side={side_label} attack_flag={attack}"
        )

    def _trace(line: str) -> None:
        if not trace_enabled:
            return
        if len(trace_lines) < trace_max_lines:
            trace_lines.append(line)

    _trace(
        "[TRACE][EP_START] "
        f"mission={mission_name} attacker={attacker_side} defender={defender_side} "
        f"algo={algo} epsilon={float(epsilon):.3f} learner_side={learner_side} opponent_side={opponent_side}"
    )
    while not done:
        step_no = int(episode_len) + 1
        enemy_mode = "policy_fn" if opponent_policy_fn is not None else "heuristic_auto"
        _trace(
            f"[TRACE][STEP] idx={step_no} phase=enemy_turn mode={enemy_mode} "
            f"game_over_before={int(bool(getattr(env_unwrapped, 'game_over', False)))}"
        )
        if opponent_policy_fn is not None:
            def _logged_opponent_policy(obs_any):
                try:
                    action = opponent_policy_fn(obs_any)
                    _trace(f"[TRACE][ENEMY_ACTION] step={step_no} action={action}")
                    if trace_style == "warhammer" and isinstance(action, dict):
                        _emit_wh40k_phase_report(
                            side_label=opponent_side,
                            step_no=step_no,
                            action_dict=action,
                            masks_counts=None,
                            shoot_targets=None,
                        )
                    return action
                except Exception as exc:
                    _trace(f"[TRACE][ENEMY_ACTION][WARN] step={step_no} exc={exc}")
                    raise

            env_unwrapped.enemyTurn(trunc=True, policy_fn=_logged_opponent_policy)
        else:
            env_unwrapped.enemyTurn(trunc=True)
        if env_unwrapped.game_over:
            info = env_unwrapped.get_info()
            _trace(
                f"[TRACE][STEP] idx={step_no} phase=enemy_turn_end game_over=1 "
                f"winner={info.get('winner', None)} end_reason={info.get('end reason', '')}"
            )
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
        elif is_az_algo(algo):
            action = select_action_with_epsilon_alphazero(
                env,
                state_tensor,
                policy_net,
                epsilon,
                len(model_units),
            )
        elif algo == "gumbel_muzero":
            action = select_action_with_epsilon_gumbel_muzero(
                env,
                state_tensor,
                policy_net,
                epsilon,
                len(model_units),
            )
        else:
            action_masks = build_action_masks_by_head(env, len(model_units), log_fn=None, debug=False)
            action = select_action_with_epsilon(
                env,
                state_tensor,
                policy_net,
                epsilon,
                len(model_units),
                action_masks=action_masks,
            )
        action_dict = convertToDict(action)
        masks_counts = _head_masks_counts()
        shoot_targets = 0
        try:
            shoot_mask_for_log = build_shoot_action_mask(env)
            if shoot_mask_for_log is not None:
                shoot_targets = int(sum(1 for x in shoot_mask_for_log if bool(x)))
        except Exception:
            shoot_targets = 0
        _trace(
            f"[TRACE][MODEL_ACTION] step={step_no} action={action_dict} "
            f"shoot_targets={shoot_targets}"
        )
        _trace(
            f"[TRACE][MODEL_ACTION_HUMAN] step={step_no} {_human_action(action_dict)} "
            f"masks=({_head_masks_summary()})"
        )
        if trace_style == "warhammer":
            _trace(
                f"[WH40K][ORDERS] step={step_no} side={learner_side} "
                f"{_human_action_with_units(action_dict)}"
            )
            _emit_wh40k_phase_report(
                side_label=learner_side,
                step_no=step_no,
                action_dict=action_dict,
                masks_counts=masks_counts,
                shoot_targets=int(shoot_targets),
            )
        verdict = _step_verdict(action_dict, masks_counts=masks_counts, shoot_targets=shoot_targets)
        _trace(f"[TRACE][STEP_VERDICT] step={step_no} verdict={verdict}")
        if trace_style == "warhammer":
            _trace(f"[WH40K][TACTIC_VERDICT] step={step_no} { _step_verdict_ru(verdict) }")
        next_observation, reward, done, _, info = env.step(action_dict)
        battle_round = _safe_int(info.get("battle round", 0), 0)
        if battle_round > 0 and battle_round != current_round:
            current_round = battle_round
            _trace(f"[TRACE][ROUND] battle_round={current_round} turn={_safe_int(info.get('turn', 0), 0)}")
            if trace_style == "warhammer":
                _trace(
                    "[WH40K][ROUND_START] "
                    f"BR={current_round} TURN={_safe_int(info.get('turn', 0), 0)} "
                    f"phase={str(info.get('phase', '') or '')} active_side={str(info.get('active side', '') or '')}"
                )
        if current_round > 0:
            st = round_stats.setdefault(
                int(current_round),
                {
                    "steps": 0,
                    "reward_sum_x1000": 0,
                    "attack_nonzero": 0,
                    "shoot_nonzero": 0,
                    "charge_nonzero": 0,
                    "cp_used": 0,
                },
            )
            st["steps"] += 1
            st["reward_sum_x1000"] += int(round(float(reward) * 1000.0))
            st["attack_nonzero"] += 1 if _safe_int(action_dict.get("attack", 0), 0) > 0 else 0
            st["shoot_nonzero"] += 1 if _safe_int(action_dict.get("shoot", -1), -1) > 0 else 0
            st["charge_nonzero"] += 1 if _safe_int(action_dict.get("charge", 0), 0) > 0 else 0
            st["cp_used"] += 1 if _safe_int(action_dict.get("use_cp", 0), 0) > 0 else 0
        model_ctrl = info.get("model controlled objectives", []) if isinstance(info, dict) else []
        enemy_ctrl = info.get("player controlled objectives", []) if isinstance(info, dict) else []
        model_health = info.get("model health", []) if isinstance(info, dict) else []
        enemy_health = info.get("player health", []) if isinstance(info, dict) else []
        model_hp_total = (
            sum(_safe_float(x, 0.0) for x in model_health)
            if isinstance(model_health, (list, tuple))
            else _safe_float(model_health, 0.0)
        )
        enemy_hp_total = (
            sum(_safe_float(x, 0.0) for x in enemy_health)
            if isinstance(enemy_health, (list, tuple))
            else _safe_float(enemy_health, 0.0)
        )
        _trace(
            "[TRACE][STEP_RESULT] "
            f"step={step_no} reward={float(reward):.4f} done={int(bool(done))} "
            f"battle_round={_safe_int(info.get('battle round', 0), 0)} "
            f"turn={int(info.get('turn', 0) or 0)} "
            f"model_vp={int(info.get('model VP', 0) or 0)} "
            f"enemy_vp={int(info.get('player VP', 0) or 0)} "
            f"model_ctrl_n={len(model_ctrl) if isinstance(model_ctrl, (list, tuple)) else 0} "
            f"enemy_ctrl_n={len(enemy_ctrl) if isinstance(enemy_ctrl, (list, tuple)) else 0} "
            f"model_hp_total={model_hp_total:.2f} enemy_hp_total={enemy_hp_total:.2f} "
            f"winner={info.get('winner', None)} "
            f"end_reason={info.get('end reason', '')}"
        )
        if trace_style == "warhammer":
            _trace(
                "[WH40K][BATTLESTATE] "
                f"BR={battle_round} TURN={_safe_int(info.get('turn', 0), 0)} "
                f"{learner_side}_vp={_safe_int(info.get('model VP', 0), 0)} "
                f"{opponent_side}_vp={_safe_int(info.get('player VP', 0), 0)} "
                f"{learner_side}_hp={model_hp_total:.2f} {opponent_side}_hp={enemy_hp_total:.2f} "
                f"{learner_side}_ctrl={len(model_ctrl) if isinstance(model_ctrl, (list, tuple)) else 0} "
                f"{opponent_side}_ctrl={len(enemy_ctrl) if isinstance(enemy_ctrl, (list, tuple)) else 0} "
                f"reward={_safe_float(reward, 0.0):.4f}"
            )
        if trace_everything:
            try:
                _trace(
                    "[TRACE][STEP_INFO_JSON] "
                    f"step={step_no} data={json.dumps(info, ensure_ascii=False, default=str, sort_keys=True)}"
                )
            except Exception:
                _trace(f"[TRACE][STEP_INFO_JSON][WARN] step={step_no} json_dump_failed")
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
    _trace(
        "[TRACE][EP_END] "
        f"winner={winner} end_reason={end_reason} "
        f"model_vp={model_vp} enemy_vp={enemy_vp} vp_diff={vp_diff} "
        f"episode_len={episode_len} reward_total={float(total_reward):.4f}"
    )
    if trace_style == "warhammer":
        winner_side = "draw"
        if winner == "model":
            winner_side = str(learner_side)
        elif winner == "enemy":
            winner_side = str(opponent_side)
        _trace(
            "[WH40K][AFTER_ACTION_REPORT] "
            f"winner={winner_side} end_reason={end_reason} "
            f"{learner_side}_vp={_safe_int(model_vp, 0)} {opponent_side}_vp={_safe_int(enemy_vp, 0)} "
            f"len={episode_len} reward_total={float(total_reward):.4f}"
        )
    for r_idx in sorted(round_stats.keys()):
        rs = round_stats.get(r_idx, {})
        steps_r = int(rs.get("steps", 0) or 0)
        reward_r = float(int(rs.get("reward_sum_x1000", 0) or 0)) / 1000.0
        _trace(
            "[TRACE][ROUND_SUMMARY] "
            f"battle_round={r_idx} steps={steps_r} reward_sum={reward_r:.4f} "
            f"attack_nonzero={int(rs.get('attack_nonzero', 0) or 0)} "
            f"shoot_nonzero={int(rs.get('shoot_nonzero', 0) or 0)} "
            f"charge_nonzero={int(rs.get('charge_nonzero', 0) or 0)} "
            f"cp_used={int(rs.get('cp_used', 0) or 0)}"
        )
        if trace_style == "warhammer":
            _trace(
                "[WH40K][ROUND_SUMMARY] "
                f"BR={r_idx} steps={steps_r} reward_sum={reward_r:.4f} "
                f"attack={int(rs.get('attack_nonzero', 0) or 0)} "
                f"shoot={int(rs.get('shoot_nonzero', 0) or 0)} "
                f"charge={int(rs.get('charge_nonzero', 0) or 0)} "
                f"cp_used={int(rs.get('cp_used', 0) or 0)}"
            )
    if trace_enabled and len(trace_lines) >= trace_max_lines:
        trace_lines.append(
            f"[TRACE][EP_TRUNCATED] Достигнут лимит строк trace: {trace_max_lines}. "
            "Увеличьте EVAL_TRACE_MAX_LINES_PER_GAME при необходимости."
        )

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
        trace_lines,
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
    learner_registry_target_state = None
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
        try:
            learner_algo_override = resolve_agent_algo(
                meta=meta if isinstance(meta, dict) else {},
                policy_state=policy_state if isinstance(policy_state, dict) else None,
                target_state=payload.get("target_state") if isinstance(payload, dict) else None,
                agent_id=selected_agent_id,
            )
        except ValueError as exc:
            log(
                f"[ERROR] Не удалось определить algo learner-agent-id={selected_agent_id}: {exc}. "
                "Где: eval.py (resolve_agent_algo). Что делать: переобучите/пересохраните агента."
            )
            return 1
        target_guess = payload.get("target_state") if isinstance(payload, dict) else None
        learner_registry_target_state = target_guess if isinstance(target_guess, dict) and target_guess else None
        log(f"Используется learner-agent-id={selected_agent_id} (policy из registry, algo={learner_algo_override}).")
    else:
        policy_state = _extract_policy_state_dict(checkpoint)

    opponent_agent_id = (args.opponent_agent_id or "").strip()
    opponent_algo_label = "heuristic"
    opponent_policy_fn = None
    if opponent_agent_id:
        try:
            opp = load_agent_opponent(agent_id=opponent_agent_id, expected_contract=eval_contract)
            opponent_algo_label = str(getattr(opp, "algo", "") or "").strip().lower() or "unknown"
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
        arch = ppo_arch_from_payload(checkpoint if isinstance(checkpoint, dict) else None)
        policy_net = make_actor_critic(n_observations, n_actions, **arch).to(device)
        load_actor_critic_state_dict(policy_net, normalize_state_dict(ppo_state))
        policy_net.eval()
    elif is_az_algo(algo):
        az_state = checkpoint.get("policy_value_net") if isinstance(checkpoint, dict) else None
        if not isinstance(az_state, dict):
            az_state = policy_state
        arch = alphazero_arch_from_payload(checkpoint if isinstance(checkpoint, dict) else None)
        policy_net = make_alphazero_net(n_observations, n_actions, **arch).to(device)
        load_alphazero_state_dict(policy_net, normalize_state_dict(az_state))
        policy_net.eval()
    elif algo == "gumbel_muzero":
        gmz_state = checkpoint.get("gumbel_muzero_net") if isinstance(checkpoint, dict) else None
        if not isinstance(gmz_state, dict):
            gmz_state = policy_state
        policy_net = GumbelMuZeroNet(
            obs_dim=int(n_observations),
            action_sizes=[int(x) for x in n_actions],
            latent_dim=int(os.getenv("GMZ_LATENT_DIM", "256")),
            hidden_dim=int(os.getenv("GMZ_HIDDEN_DIM", "256")),
            action_embed_dim=int(os.getenv("GMZ_ACTION_EMBED_DIM", "64")),
        ).to(device)
        policy_net.load_state_dict(normalize_state_dict(gmz_state))
        policy_net.eval()
    else:
        from core.models.DQN import infer_dqn_arch_from_state_dict, make_dqn

        dqn_arch = infer_dqn_arch_from_state_dict(policy_state)
        policy_net = make_dqn(n_observations, n_actions, **dqn_arch).to(device)
        target_net = make_dqn(n_observations, n_actions, **dqn_arch).to(device)
        policy_net.load_state_dict(normalize_state_dict(policy_state))
        target_state = None
        if isinstance(checkpoint, dict):
            target_state = checkpoint.get("target_net") or checkpoint.get("target_model_state_dict")
        if not isinstance(target_state, dict) and learner_registry_target_state is not None:
            target_state = learner_registry_target_state
        if isinstance(target_state, dict) and target_state:
            target_net.load_state_dict(normalize_state_dict(target_state))
        else:
            target_net.load_state_dict(normalize_state_dict(policy_net.state_dict()))
        policy_net.eval()
        target_net.eval()

    az_eval_mode = str(os.getenv("AZ_EVAL_MODE", "greedy")).strip().lower() or "greedy"
    az_opp_mode = str(os.getenv("AZ_EVAL_OPPONENT_MODE", "greedy")).strip().lower() or "greedy"
    gmz_eval_mode = str(os.getenv("GMZ_EVAL_MODE", "search")).strip().lower() or "search"
    gmz_opp_mode = str(os.getenv("GMZ_OPPONENT_MODE", "search")).strip().lower() or "search"
    mode_parts: list[str] = []
    if is_az_algo(algo) or is_az_algo(opponent_algo_label):
        az_eval_tail = f"az_eval_mode={az_eval_mode}"
        az_opp_tail = f"az_opponent_mode={az_opp_mode}"
        if is_az_algo(algo) and az_eval_mode == "mcts":
            az_eval_tail += f"(temp={float(os.getenv('AZ_EVAL_MCTS_TEMPERATURE', '0.06')):.3f})"
        if is_az_algo(opponent_algo_label) and az_opp_mode == "mcts":
            az_opp_tail += (
                f"(temp={float(os.getenv('AZ_EVAL_OPPONENT_MCTS_TEMPERATURE', os.getenv('AZ_EVAL_MCTS_TEMPERATURE', '0.06'))):.3f})"
            )
        mode_parts.append(az_eval_tail)
        mode_parts.append(az_opp_tail)
    if algo == "gumbel_muzero" or opponent_algo_label == "gumbel_muzero":
        gmz_eval_tail = f"gmz_eval_mode={gmz_eval_mode}"
        gmz_opp_tail = f"gmz_opponent_mode={gmz_opp_mode}"
        if algo == "gumbel_muzero" and gmz_eval_mode == "search":
            gmz_eval_tail += f"(temp={float(os.getenv('GMZ_EVAL_TEMPERATURE', '0.10')):.3f})"
        if opponent_algo_label == "gumbel_muzero" and gmz_opp_mode == "search":
            gmz_opp_tail += (
                f"(temp={float(os.getenv('GMZ_EVAL_OPPONENT_TEMPERATURE', os.getenv('GMZ_EVAL_TEMPERATURE', '0.10'))):.3f})"
            )
        mode_parts.append(gmz_eval_tail)
        mode_parts.append(gmz_opp_tail)
    modes_tail = (", " + ", ".join(mode_parts)) if mode_parts else ""
    log(
        f"Старт оценки: игр={games}, epsilon={epsilon:.3f}, "
        f"модель={os.path.basename(pickle_path)}, checkpoint={os.path.basename(checkpoint_path)}, "
        f"heuristic_mode={str(os.getenv('HEURISTIC_MODE', 'v2')).strip().lower() or 'v2'}, algo={algo}, "
        f"opponent_algo={opponent_algo_label}{modes_tail}."
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
    step_metrics = Counter()
    action_tuple_counter = Counter()
    model_action_re = re.compile(
        r"move=(?P<move>-?\d+).*?attack=(?P<attack>-?\d+).*?shoot=(?P<shoot>-?\d+).*?"
        r"charge=(?P<charge>-?\d+).*?use_cp=(?P<use_cp>-?\d+).*?cp_on=(?P<cp_on>-?\d+).*?"
        r"masks=\(move:(?P<move_v>\d+)/(?P<move_t>\d+), attack:(?P<attack_v>\d+)/(?P<attack_t>\d+), "
        r"shoot:(?P<shoot_v>\d+)/(?P<shoot_t>\d+), charge:(?P<charge_v>\d+)/(?P<charge_t>\d+),"
    )
    step_result_re = re.compile(r"model_ctrl_n=(?P<model_ctrl>\d+)")

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
            trace_lines,
        ) = run_episode(
            env,
            model_units,
            enemy_units,
            policy_net,
            epsilon,
            device,
            algo,
            opponent_policy_fn=opponent_policy_fn,
            learner_side=learner_side,
        )
        for line in trace_lines:
            _append_eval_log(f"[TRACE][GAME {idx}] {line}")
            if line.startswith("[TRACE][MODEL_ACTION_HUMAN]"):
                m = model_action_re.search(line)
                if m:
                    move = int(m.group("move"))
                    attack = int(m.group("attack"))
                    shoot = int(m.group("shoot"))
                    charge = int(m.group("charge"))
                    use_cp = int(m.group("use_cp"))
                    cp_on = int(m.group("cp_on"))
                    move_v = int(m.group("move_v"))
                    shoot_v = int(m.group("shoot_v"))
                    charge_v = int(m.group("charge_v"))
                    step_metrics["total_model_steps"] += 1
                    action_tuple_counter[(move, attack, shoot, charge, use_cp, cp_on)] += 1
                    if move_v > 1:
                        step_metrics["move_opt_steps"] += 1
                        if move == 4:
                            step_metrics["stay_opt_steps"] += 1
                    if shoot_v > 1:
                        step_metrics["shoot_opt_steps"] += 1
                        if shoot == 0:
                            step_metrics["shoot_zero_opt_steps"] += 1
                    if charge_v > 1:
                        step_metrics["charge_opt_steps"] += 1
                        if charge == 0:
                            step_metrics["charge_zero_opt_steps"] += 1
            elif line.startswith("[TRACE][STEP_VERDICT]"):
                verdict_raw = line.split("verdict=", 1)[-1].strip()
                for token in verdict_raw.split(","):
                    token = token.strip()
                    if not token or token == "ok":
                        continue
                    if token == "stay_while_move_options_exist":
                        step_metrics["verdict_stay"] += 1
                    elif token == "skip_charge_while_options_exist":
                        step_metrics["verdict_skip_charge"] += 1
                    elif token == "default_shoot_choice_with_options":
                        step_metrics["verdict_default_shoot"] += 1
            elif line.startswith("[TRACE][STEP_RESULT]"):
                m = step_result_re.search(line)
                if m:
                    step_metrics["step_result_total"] += 1
                    if int(m.group("model_ctrl")) == 0:
                        step_metrics["step_result_model_ctrl_zero"] += 1
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

        end_reasons_v2[str(end_reason or "unknown")] += 1
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
    total_model_steps = int(step_metrics.get("total_model_steps", 0))
    move_opt_steps = int(step_metrics.get("move_opt_steps", 0))
    shoot_opt_steps = int(step_metrics.get("shoot_opt_steps", 0))
    charge_opt_steps = int(step_metrics.get("charge_opt_steps", 0))
    step_result_total = int(step_metrics.get("step_result_total", 0))
    stay_rate_when_move_options = (
        float(step_metrics.get("stay_opt_steps", 0)) / float(move_opt_steps)
        if move_opt_steps
        else 0.0
    )
    skip_charge_rate_when_options = (
        float(step_metrics.get("verdict_skip_charge", 0)) / float(total_model_steps)
        if total_model_steps
        else 0.0
    )
    default_shoot_rate_when_options = (
        float(step_metrics.get("verdict_default_shoot", 0)) / float(total_model_steps)
        if total_model_steps
        else 0.0
    )
    shoot_zero_rate_when_shoot_options = (
        float(step_metrics.get("shoot_zero_opt_steps", 0)) / float(shoot_opt_steps)
        if shoot_opt_steps
        else 0.0
    )
    charge_zero_rate_when_charge_options = (
        float(step_metrics.get("charge_zero_opt_steps", 0)) / float(charge_opt_steps)
        if charge_opt_steps
        else 0.0
    )
    model_ctrl_zero_rate = (
        float(step_metrics.get("step_result_model_ctrl_zero", 0)) / float(step_result_total)
        if step_result_total
        else 0.0
    )
    top_action_counts = [count for _action, count in action_tuple_counter.most_common(5)]
    top1_action_share = (
        float(top_action_counts[0]) / float(total_model_steps)
        if total_model_steps and top_action_counts
        else 0.0
    )
    top5_action_share = (
        float(sum(top_action_counts)) / float(total_model_steps)
        if total_model_steps
        else 0.0
    )

    turn_limit_count = int(end_reasons_v2.get("turn_limit", 0))
    wipeout_model_count = int(end_reasons_v2.get("wipeout_model", 0))
    wipeout_enemy_count = int(end_reasons_v2.get("wipeout_enemy", 0))
    if learner_side == "P1":
        wipeout_p1_count = wipeout_enemy_count
        wipeout_p2_count = wipeout_model_count
    else:
        wipeout_p1_count = wipeout_model_count
        wipeout_p2_count = wipeout_enemy_count

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
        f"stay_rate_when_move_options={stay_rate_when_move_options:.3f} "
        f"skip_charge_rate_when_options={skip_charge_rate_when_options:.3f} "
        f"default_shoot_rate_when_options={default_shoot_rate_when_options:.3f} "
        f"shoot_zero_rate_when_shoot_options={shoot_zero_rate_when_shoot_options:.3f} "
        f"charge_zero_rate_when_charge_options={charge_zero_rate_when_charge_options:.3f} "
        f"model_ctrl_zero_rate={model_ctrl_zero_rate:.3f} "
        f"top1_action_share={top1_action_share:.3f} top5_action_share={top5_action_share:.3f} "
        f"turn_limit_count={turn_limit_count} "
        f"wipeout_model_count={wipeout_model_count} wipeout_enemy_count={wipeout_enemy_count} "
        f"wipeout_p1_count={wipeout_p1_count} wipeout_p2_count={wipeout_p2_count} "
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
        "[DETAIL] Пассивность: "
        f"stay@move_opts={stay_rate_when_move_options:.3f}, "
        f"skip_charge={skip_charge_rate_when_options:.3f}, "
        f"default_shoot={default_shoot_rate_when_options:.3f}, "
        f"shoot0@opts={shoot_zero_rate_when_shoot_options:.3f}, "
        f"charge0@opts={charge_zero_rate_when_charge_options:.3f}, "
        f"model_ctrl0={model_ctrl_zero_rate:.3f}, "
        f"top1={top1_action_share:.3f}, top5={top5_action_share:.3f}"
    )
    log(
        "[DETAIL] Причины завершения: "
        f"turn_limit={turn_limit_count}, "
        f"wipeout_model={wipeout_model_count}, wipeout_enemy={wipeout_enemy_count}, "
        f"wipeout_p1={wipeout_p1_count}, wipeout_p2={wipeout_p2_count}, "
        f"raw={dict(end_reasons_v2)}"
    )
    log("[DETAIL] ------------------------------------------------")
    return 0


if __name__ == "__main__":
    sys.exit(main())
