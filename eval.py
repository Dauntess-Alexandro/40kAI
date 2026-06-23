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

import gymnasium as gym
import torch

import core.envs  # noqa: F401 (регистрация '40kAI-v0')
from core.engine.agent_registry import (
    compatible_contracts,
    load_agent_by_id,
    make_env_contract,
    resolve_agent_algo,
)
from core.engine.game_controller import n_actions_from_env
from core.engine.mission import (
    check_end_of_battle,
    deploy_for_mission,
    normalize_mission_name,
    post_deploy_setup,
)
from core.engine.phases.obs_features import phase_obs_features_enabled
from core.envs.warhamEnv import roll_off_attacker_defender
from core.models.alphazero_ids import is_alphazero_net_algo, is_az_algo, is_gumbel_az_algo
from core.models.eval_agent import build_eval_agent, resolve_eval_search_cfg
from core.models.opponent_adapter import load_agent_opponent
from core.models.sampled_muzero_search import SampledMuZeroSearch, SampledMuZeroSearchConfig
from core.models.utils import normalize_state_dict
from project_paths import AGENT_EVAL_LOG_PATH, ARTIFACTS_MODELS_DIR, EVAL_STOP_FLAG_PATH, ensure_runtime_dirs

AGENT_EVAL_LOG_FILE = str(AGENT_EVAL_LOG_PATH.relative_to(AGENT_EVAL_LOG_PATH.parent.parent))
os.environ.setdefault("AGENT_LOG_FILE", AGENT_EVAL_LOG_FILE)
from core.models.action_contract import ordered_action_keys
from core.models.utils import (
    build_action_masks_by_head,
    build_shoot_action_mask,
    sample_action_list_from_space,
    unwrap_env,
)
from core.telemetry.stratagem_trace import (
    cp_for_env_side,
    eval_side_label,
    log_stratagem_attempts,
    log_stratagem_journal_diff,
    stratagem_used_snapshot,
)


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


def _eval_stop_flag_path() -> str:
    return os.environ.get("EVAL_STOP_FLAG_PATH", "").strip() or str(EVAL_STOP_FLAG_PATH)


def eval_stop_requested() -> bool:
    return os.path.exists(_eval_stop_flag_path())


def clear_eval_stop_flag() -> None:
    try:
        path = _eval_stop_flag_path()
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass


def log(message: str) -> None:
    if message.startswith("["):
        rendered = f"[EVAL]{message}"
    else:
        rendered = f"[EVAL] {message}"
    try:
        print(rendered, flush=True)
    except UnicodeEncodeError:
        # Консоль (напр. cp1251 при запуске из GUI) не кодирует часть символов
        # (стрелки/эмодзи). Не валим весь eval — печатаем с заменой непечатных.
        enc = getattr(sys.stdout, "encoding", None) or "utf-8"
        print(rendered.encode(enc, errors="replace").decode(enc, errors="replace"), flush=True)
    _append_eval_log(message)


def _env_bool(name: str, default: str = "0") -> bool:
    return str(os.getenv(str(name), str(default))).strip().lower() in {"1", "true", "yes", "on"}


def _find_checkpoint_for_pickle(pickle_path: str) -> str | None:
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


def load_latest_model(model_path: str | None = None):
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
    # shoot_mask: legacy, игнорируется (B2 per-unit через action_masks / env masks)
    if epsilon <= 0:
        with torch.no_grad():
            decision = policy_net(state)
            ordered_keys = ordered_action_keys(int(len_model))
            legal_by_head = None
            env_u = unwrap_env(env)
            if hasattr(env_u, "get_legal_action_masks_by_head"):
                try:
                    legal_by_head = env_u.get_legal_action_masks_by_head(side="model")
                except Exception:
                    legal_by_head = None
            action = []
            for head_idx, head in enumerate(decision):
                head = head.squeeze(0)
                raw_mask = None
                if masks_seq is not None and head_idx < len(masks_seq):
                    raw_mask = masks_seq[head_idx]
                key = ordered_keys[head_idx] if head_idx < len(ordered_keys) else None
                if raw_mask is None and legal_by_head is not None and key is not None:
                    raw_mask = legal_by_head.get(key)
                if raw_mask is not None:
                    mask = torch.as_tensor(raw_mask, dtype=torch.bool, device=head.device)
                    if mask.numel() == head.numel() and mask.any():
                        masked_head = head.clone()
                        masked_head[~mask] = -1e9
                        action.append(int(masked_head.argmax().item()))
                        continue
                action.append(int(head.argmax().item()))
            return torch.tensor([action], device="cpu")

    action_list = sample_action_list_from_space(env, int(len_model), masks_seq=masks_seq)
    return torch.tensor([action_list], device="cpu")


def select_action_with_epsilon_sampled_muzero(env, state, policy_net, epsilon, len_model):
    masks_cpu = build_action_masks_by_head(env, len_model, log_fn=None, debug=False)
    legal_masks = [m.detach().cpu().numpy().astype(bool) for m in masks_cpu]
    obs_np = state.squeeze(0).detach().cpu().numpy()
    if epsilon > 0 and random.random() < float(epsilon):
        action_list = sample_action_list_from_space(env, int(len_model))
        return torch.tensor([action_list], device="cpu")
    smz_eval_mode = str(os.getenv("SMZ_EVAL_MODE", os.getenv("SMZ_OPPONENT_MODE", "search"))).strip().lower() or "search"
    if smz_eval_mode not in {"search", "greedy"}:
        smz_eval_mode = "search"
    if smz_eval_mode == "greedy":
        with torch.no_grad():
            probs, _value = policy_net.infer(
                state,
                masks_by_head=[m.to(state.device).unsqueeze(0) for m in masks_cpu],
            )
        action_list = [int(torch.argmax(p.squeeze(0), dim=0).item()) for p in probs]
        return torch.tensor([action_list], device="cpu")
    search = SampledMuZeroSearch(
        net=policy_net,
        config=SampledMuZeroSearchConfig(
            num_samples=int(os.getenv("SMZ_EVAL_NUM_SAMPLES", "24")),
            temperature=float(os.getenv("SMZ_EVAL_TEMPERATURE", "0.10")),
            sample_temperature=float(os.getenv("SMZ_EVAL_SAMPLE_TEMPERATURE", "1.0")),
            prior_weight=0.0,
            dedup=True,
            discount=float(os.getenv("SMZ_DISCOUNT", "0.997")),
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
    learner_agent,
    opponent_agent,
    device,
    *,
    learner_side: str = "P1",
):
    env_unwrapped = unwrap_env(env)
    # algo/epsilon уехали внутрь агентов; для логов читаем из learner_agent.
    algo = str(getattr(learner_agent, "algo", "")).strip().lower()
    epsilon = float(getattr(getattr(learner_agent, "cfg", None), "epsilon", 0.0) or 0.0)
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

    from core.envs.warhamEnv import resolve_first_turn_side
    env_unwrapped.first_turn_side = resolve_first_turn_side(manual_roll_allowed=False, log_fn=None)
    _append_eval_log(
        f"[FIRST_TURN] mode={os.getenv('FIRST_TURN', 'roll')} first={env_unwrapped.first_turn_side}"
    )

    _, info = env.reset(
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
    ep_stratagem_attempts: Counter[str] = Counter()
    ep_stratagem_applied: Counter[str] = Counter()
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

    def _aggregate_per_unit_max(action_dict: dict, prefix: str, n_units: int, default: int = 0) -> int:
        vals = [_safe_int(action_dict.get(f"{prefix}_{i}", default), default) for i in range(int(n_units))]
        return max(vals) if vals else int(default)

    def _head_masks_summary() -> str:
        try:
            n_units = int(len(model_units))
            keys = ordered_action_keys(n_units)
            masks = build_action_masks_by_head(env, n_units, log_fn=None, debug=False)
            parts = []
            for i, key in enumerate(keys):
                if i >= len(masks):
                    break
                m = masks[i]
                m_np = m.detach().cpu().numpy() if hasattr(m, "detach") else m
                total = int(len(m_np))
                valid = int(sum(1 for x in m_np if bool(x)))
                parts.append(f"{key}:{valid}/{total}")
            return ", ".join(parts)
        except Exception:
            return "masks=unavailable"

    def _head_masks_counts() -> dict[str, tuple[int, int]]:
        n_units = int(len(model_units))
        keys = ordered_action_keys(n_units)
        out: dict[str, tuple[int, int]] = {}
        try:
            masks = build_action_masks_by_head(env, n_units, log_fn=None, debug=False)
            for idx, key in enumerate(keys):
                if idx >= len(masks):
                    continue
                m = masks[idx]
                m_np = m.detach().cpu().numpy() if hasattr(m, "detach") else m
                total = int(len(m_np))
                valid = int(sum(1 for x in m_np if bool(x)))
                out[key] = (valid, total)
            shoot_v = max((out.get(f"shoot_num_{i}", (0, 0))[0] for i in range(n_units)), default=0)
            shoot_t = max((out.get(f"shoot_num_{i}", (0, 0))[1] for i in range(n_units)), default=0)
            charge_v = max((out.get(f"charge_num_{i}", (0, 0))[0] for i in range(n_units)), default=0)
            charge_t = max((out.get(f"charge_num_{i}", (0, 0))[1] for i in range(n_units)), default=0)
            out["shoot"] = (int(shoot_v), int(shoot_t))
            out["charge"] = (int(charge_v), int(charge_t))
        except Exception:
            out.setdefault("shoot", (0, 0))
            out.setdefault("charge", (0, 0))
        return out

    def _human_action(action_dict: dict) -> str:
        n_units = int(len(model_units))
        move_val = _safe_int(action_dict.get("move", 4), 4)
        attack_val = _safe_int(action_dict.get("attack", 0), 0)
        shoot_val = _aggregate_per_unit_max(action_dict, "shoot_num", n_units, default=-1)
        charge_val = _aggregate_per_unit_max(action_dict, "charge_num", n_units, default=0)
        move_units = []
        shoot_units = []
        charge_units = []
        for i_u in range(n_units):
            k_move = f"move_num_{i_u}"
            if k_move in action_dict:
                move_units.append(str(_safe_int(action_dict.get(k_move, 0), 0)))
            shoot_units.append(str(_safe_int(action_dict.get(f"shoot_num_{i_u}", 0), 0)))
            charge_units.append(str(_safe_int(action_dict.get(f"charge_num_{i_u}", 0), 0)))
        move_units_text = ",".join(move_units) if move_units else "-"
        return (
            f"move={move_val}({move_dir_labels.get(move_val, 'unk')}) "
            f"attack={attack_val} shoot={shoot_val} charge={charge_val} "
            f"move_num=[{move_units_text}] "
            f"shoot_num=[{','.join(shoot_units)}] charge_num=[{','.join(charge_units)}]"
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
        shoot = _aggregate_per_unit_max(action_dict, "shoot_num", len(model_units), default=-1)
        charge = _aggregate_per_unit_max(action_dict, "charge_num", len(model_units), default=0)

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
        shoot = _aggregate_per_unit_max(action_dict, "shoot_num", len(model_units), default=-1)
        charge = _aggregate_per_unit_max(action_dict, "charge_num", len(model_units), default=0)

        mv_valid, mv_total = _mask_tuple(masks_counts, "move")
        at_valid, at_total = _mask_tuple(masks_counts, "attack")
        sh_valid, sh_total = _mask_tuple(masks_counts, "shoot")
        ch_valid, ch_total = _mask_tuple(masks_counts, "charge")

        _trace(
            "[WH40K][PHASE][COMMAND] "
            f"step={step_no} side={side_label} "
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
    from core.engine.turn_sequencing import run_battle_round

    while not done:
        step_no = int(episode_len) + 1
        # round_io — разделяемый контейнер для передачи результатов step из _model_half наружу
        round_io: dict = {"done": done, "reward": 0.0, "info": info}

        def _enemy_half() -> None:
            enemy_mode = "policy_fn" if opponent_agent is not None else "heuristic_auto"
            _trace(
                f"[TRACE][STEP] idx={step_no} phase=enemy_turn mode={enemy_mode} "
                f"game_over_before={int(bool(getattr(env_unwrapped, 'game_over', False)))}"
            )
            enemy_su_before = stratagem_used_snapshot(env_unwrapped)
            cp_model_before_enemy = cp_for_env_side(env_unwrapped, "model")
            cp_enemy_before_enemy = cp_for_env_side(env_unwrapped, "enemy")
            enemy_attempt_specs: list[tuple[str, int | None, str]] = []
            base_enemy_fn = (
                opponent_agent.as_policy_fn(env_unwrapped, "enemy")
                if opponent_agent is not None
                else None
            )
            if base_enemy_fn is not None:
                def _logged_opponent_policy(obs_any):
                    try:
                        action = base_enemy_fn(obs_any)
                        _trace(f"[TRACE][ENEMY_ACTION] step={step_no} action={action}")
                        if isinstance(action, dict):
                            enemy_attempt_specs.extend(
                                log_stratagem_attempts(
                                    _trace,
                                    step_no=step_no,
                                    env_side="enemy",
                                    learner_side=learner_side,
                                    action_dict=action,
                                    fight_plan=None,
                                    ep_attempts=ep_stratagem_attempts,
                                    emit=(trace_style == "warhammer"),
                                    tag="WH40K",
                                )
                            )
                            if trace_style == "warhammer":
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
            log_stratagem_journal_diff(
                _trace,
                step_no=step_no,
                env_side_acting="enemy",
                learner_side=learner_side,
                su_before=enemy_su_before,
                su_after=stratagem_used_snapshot(env_unwrapped),
                cp_model_before=cp_model_before_enemy,
                cp_enemy_before=cp_enemy_before_enemy,
                env_unwrapped=env_unwrapped,
                attempt_specs=enemy_attempt_specs,
                ep_applied=ep_stratagem_applied,
                emit=(trace_style == "warhammer"),
                tag="WH40K",
            )
            # Не делаем break здесь: run_battle_round сам прервёт раунд через game_over.
            # Лог game_over переехал ниже, после run_battle_round.

        def _model_half() -> None:
            nonlocal done, info, episode_len, total_reward
            # Действие фазы — единый путь через агента; fight-стратагемы через голову strat_fight.
            action_dict, _plan = learner_agent.select_action(env_unwrapped, "model")
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
                    f"[WH40K][ORDERS] step={step_no} side={eval_side_label('model', learner_side)} "
                    f"{_human_action_with_units(action_dict)}"
                )
                _emit_wh40k_phase_report(
                    side_label=eval_side_label("model", learner_side),
                    step_no=step_no,
                    action_dict=action_dict,
                    masks_counts=masks_counts,
                    shoot_targets=int(shoot_targets),
                )
            model_attempt_specs = log_stratagem_attempts(
                _trace,
                step_no=step_no,
                env_side="model",
                learner_side=learner_side,
                action_dict=action_dict,
                fight_plan={},
                ep_attempts=ep_stratagem_attempts,
                emit=(trace_style == "warhammer"),
                tag="WH40K",
            )
            verdict = _step_verdict(action_dict, masks_counts=masks_counts, shoot_targets=shoot_targets)
            _trace(f"[TRACE][STEP_VERDICT] step={step_no} verdict={verdict}")
            if trace_style == "warhammer":
                _trace(f"[WH40K][TACTIC_VERDICT] step={step_no} { _step_verdict_ru(verdict) }")
            su_before = stratagem_used_snapshot(env_unwrapped)
            cp_model_before = cp_for_env_side(env_unwrapped, "model")
            cp_enemy_before = cp_for_env_side(env_unwrapped, "enemy")
            _next_observation, _reward, _done, _, _info = env.step(action_dict)
            new_strat_records = log_stratagem_journal_diff(
                _trace,
                step_no=step_no,
                env_side_acting="model",
                learner_side=learner_side,
                su_before=su_before,
                su_after=stratagem_used_snapshot(env_unwrapped),
                cp_model_before=cp_model_before,
                cp_enemy_before=cp_enemy_before,
                env_unwrapped=env_unwrapped,
                attempt_specs=model_attempt_specs,
                ep_applied=ep_stratagem_applied,
                emit=(trace_style == "warhammer"),
                tag="WH40K",
            )
            battle_round = _safe_int(_info.get("battle round", 0), 0)
            nonlocal current_round
            if battle_round > 0 and battle_round != current_round:
                current_round = battle_round
                _trace(f"[TRACE][ROUND] battle_round={current_round} turn={_safe_int(_info.get('turn', 0), 0)}")
                if trace_style == "warhammer":
                    _trace(
                        "[WH40K][ROUND_START] "
                        f"BR={current_round} TURN={_safe_int(_info.get('turn', 0), 0)} "
                        f"phase={str(_info.get('phase', '') or '')} active_side={str(_info.get('active side', '') or '')}"
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
                        "strat_attempt": 0,
                        "strat_applied": 0,
                    },
                )
                st["steps"] += 1
                st["reward_sum_x1000"] += int(round(float(_reward) * 1000.0))
                st["attack_nonzero"] += 1 if _safe_int(action_dict.get("attack", 0), 0) > 0 else 0
                st["shoot_nonzero"] += 1 if any(
                    _safe_int(action_dict.get(f"shoot_num_{i}", -1), -1) > 0
                    for i in range(int(len(model_units)))
                ) else 0
                st["charge_nonzero"] += 1 if any(
                    _safe_int(action_dict.get(f"charge_num_{i}", 0), 0) > 0
                    for i in range(int(len(model_units)))
                ) else 0
                st["strat_attempt"] += len(model_attempt_specs)
                st["strat_applied"] += len(new_strat_records)
            model_ctrl = _info.get("model controlled objectives", []) if isinstance(_info, dict) else []
            enemy_ctrl = _info.get("player controlled objectives", []) if isinstance(_info, dict) else []
            model_health = _info.get("model health", []) if isinstance(_info, dict) else []
            enemy_health = _info.get("player health", []) if isinstance(_info, dict) else []
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
                f"step={step_no} reward={float(_reward):.4f} done={int(bool(_done))} "
                f"battle_round={_safe_int(_info.get('battle round', 0), 0)} "
                f"turn={int(_info.get('turn', 0) or 0)} "
                f"model_vp={int(_info.get('model VP', 0) or 0)} "
                f"enemy_vp={int(_info.get('player VP', 0) or 0)} "
                f"model_ctrl_n={len(model_ctrl) if isinstance(model_ctrl, (list, tuple)) else 0} "
                f"enemy_ctrl_n={len(enemy_ctrl) if isinstance(enemy_ctrl, (list, tuple)) else 0} "
                f"model_hp_total={model_hp_total:.2f} enemy_hp_total={enemy_hp_total:.2f} "
                f"winner={_info.get('winner', None)} "
                f"end_reason={_info.get('end reason', '')}"
            )
            if trace_style == "warhammer":
                _trace(
                    "[WH40K][BATTLESTATE] "
                    f"BR={battle_round} TURN={_safe_int(_info.get('turn', 0), 0)} "
                    f"{learner_side}_vp={_safe_int(_info.get('model VP', 0), 0)} "
                    f"{opponent_side}_vp={_safe_int(_info.get('player VP', 0), 0)} "
                    f"{learner_side}_hp={model_hp_total:.2f} {opponent_side}_hp={enemy_hp_total:.2f} "
                    f"{learner_side}_ctrl={len(model_ctrl) if isinstance(model_ctrl, (list, tuple)) else 0} "
                    f"{opponent_side}_ctrl={len(enemy_ctrl) if isinstance(enemy_ctrl, (list, tuple)) else 0} "
                    f"reward={_safe_float(_reward, 0.0):.4f}"
                )
            if trace_everything:
                try:
                    _trace(
                        "[TRACE][STEP_INFO_JSON] "
                        f"step={step_no} data={json.dumps(_info, ensure_ascii=False, default=str, sort_keys=True)}"
                    )
                except Exception:
                    _trace(f"[TRACE][STEP_INFO_JSON][WARN] step={step_no} json_dump_failed")
            try:
                total_reward += float(_reward)
            except (TypeError, ValueError):
                pass
            episode_len += 1
            round_io["done"] = _done
            round_io["reward"] = _reward
            round_io["info"] = _info

        run_battle_round(env_unwrapped, run_model_half=_model_half, run_enemy_half=_enemy_half)

        if bool(getattr(env_unwrapped, "game_over", False)):
            done = True
            info = env_unwrapped.get_info()
            # Старое поведение: трейс enemy_turn_end эмитился только при game_over от хода врага.
            # При game_over от хода модели старый цикл выходил без этого трейса (round_io["done"]=True).
            if not round_io["done"]:
                _trace(
                    f"[TRACE][STEP] idx={step_no} phase=enemy_turn_end game_over=1 "
                    f"winner={info.get('winner', None)} end_reason={info.get('end reason', '')}"
                )
            break
        done = bool(round_io["done"])
        if round_io["info"] is not None:
            info = round_io["info"]

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
    _trace(
        "[TRACE][STRATAGEM_SUMMARY] "
        f"attempts={dict(ep_stratagem_attempts)} applied={dict(ep_stratagem_applied)} "
        f"attempt_total={sum(ep_stratagem_attempts.values())} "
        f"applied_total={sum(ep_stratagem_applied.values())}"
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
        _trace(
            "[WH40K][STRATAGEM_SUMMARY] "
            f"attempts={dict(ep_stratagem_attempts)} applied={dict(ep_stratagem_applied)} "
            f"attempt_total={sum(ep_stratagem_attempts.values())} "
            f"applied_total={sum(ep_stratagem_applied.values())}"
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
            f"strat_attempt={int(rs.get('strat_attempt', 0) or 0)} "
            f"strat_applied={int(rs.get('strat_applied', 0) or 0)}"
        )
        if trace_style == "warhammer":
            _trace(
                "[WH40K][ROUND_SUMMARY] "
                f"BR={r_idx} steps={steps_r} reward_sum={reward_r:.4f} "
                f"attack={int(rs.get('attack_nonzero', 0) or 0)} "
                f"shoot={int(rs.get('shoot_nonzero', 0) or 0)} "
                f"charge={int(rs.get('charge_nonzero', 0) or 0)} "
                f"strat_attempt={int(rs.get('strat_attempt', 0) or 0)} "
                f"strat_applied={int(rs.get('strat_applied', 0) or 0)}"
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


def _aggregate_swap(res_a: dict, res_b: dict) -> dict:
    """res_a: A=model/B=enemy; res_b: B=model/A=enemy. Winrate агента = его победы в обоих назначениях / 2N."""
    n = int(res_a["games"]) + int(res_b["games"])
    a_wins = int(res_a["model_wins"]) + int(res_b["enemy_wins"])
    b_wins = int(res_a["enemy_wins"]) + int(res_b["model_wins"])
    return {"agentA_winrate": a_wins / n if n else 0.0,
            "agentB_winrate": b_wins / n if n else 0.0,
            "total_games": n, "draws": int(res_a["draws"]) + int(res_b["draws"])}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=50)
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--learner-agent-id", type=str, default="")
    parser.add_argument("--opponent-agent-id", type=str, default="")
    parser.add_argument("--opponent-policy", type=str, default="mirror")
    parser.add_argument("--swap-sides", action="store_true",
                        help="Сыграть оба назначения сторон и усреднить (честный P1≡P2).")
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
    # B6: phase_obs_features меняет размер obs (+24). Фиксируем в логе для сверки с чекпойнтом.
    log(
        f"[EVAL][AZ][CONFIG] phase_obs_features={int(phase_obs_features_enabled())} "
        f"obs_size={int(n_observations)}"
    )
    # B3-full: стратагемы через net-value lookahead (env AZ_REACTION_VALUE_POLICY, дефолт 1 для AZ; 0 = legacy).
    _reaction_vp_on = str(os.getenv("AZ_REACTION_VALUE_POLICY", "1")).strip().lower() in ("1", "true", "yes", "on")
    log(f"[EVAL][AZ][CONFIG] reaction_value_policy={int(_reaction_vp_on)}")
    eval_contract = make_env_contract(
        n_observations=n_observations,
        n_actions=n_actions,
        mission_name=mission_name,
        ruleset_version=str(os.getenv("RULESET_VERSION", "only_war_v2")),
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
        log(f"Используется learner-agent-id={selected_agent_id} (policy из registry, algo={learner_algo_override}).")
    else:
        policy_state = _extract_policy_state_dict(checkpoint)

    opponent_agent_id = (args.opponent_agent_id or "").strip()
    opponent_algo_label = "heuristic"
    opponent_agent = None
    if opponent_agent_id:
        try:
            opp = load_agent_opponent(agent_id=opponent_agent_id, expected_contract=eval_contract)
            opponent_algo_label = str(getattr(opp, "algo", "") or "").strip().lower() or "unknown"
            opponent_agent = build_eval_agent(
                algo=opp.algo,
                policy_state=opp.policy_state,
                contract=opp.contract,
                len_model=len(enemy_units),
                cfg=resolve_eval_search_cfg(opp.algo),
                device=device,
            )
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
    # Извлечение learner net-state под algo-специфичным ключом checkpoint'а
    # (registry-путь уже даёт корректный policy_state). Конструкция сети/поиска —
    # внутри build_eval_agent (единый путь обеих сторон, Task 5).
    if algo == "ppo":
        learner_state = checkpoint.get("actor_critic") if isinstance(checkpoint, dict) else None
    elif is_alphazero_net_algo(algo):
        learner_state = checkpoint.get("policy_value_net") if isinstance(checkpoint, dict) else None
    elif algo == "gumbel_muzero":
        learner_state = checkpoint.get("gumbel_muzero_net") if isinstance(checkpoint, dict) else None
    elif algo == "sampled_muzero":
        learner_state = checkpoint.get("sampled_muzero_net") if isinstance(checkpoint, dict) else None
    else:  # dqn
        learner_state = None
    if not isinstance(learner_state, dict):
        learner_state = policy_state

    cfg = resolve_eval_search_cfg(algo)
    # Стартовый лог epsilon берём из cfg (DQN→epsilon): FORCE_GREEDY больше не маскирует
    # реальный epsilon, который применяет EvalAgent (run_episode читает learner_agent.cfg.epsilon).
    epsilon = float(getattr(cfg, "epsilon", epsilon))
    # Примечание: после унификации на EvalAgent обе стороны строятся через один
    # resolve_eval_search_cfg, который *_OPPONENT_* ключи в search НЕ читает (они
    # кормят только диагностическую лог-строку modes_tail ниже). Поэтому наличие
    # *_OPPONENT_* env (GUI выставляет их всегда) больше НЕ нарушает честный 1:1 —
    # старый WARN был структурно ложным и удалён. Поле cfg.opponent_override_active
    # оставлено для обратной совместимости.
    # Арку learner-сети резолвим ИЗ payload чекпойнта (как до Task5), чтобы недефолтные
    # чекпойнты грузились 1:1. Registry-путь без payload → arch=None (env/дефолт-арка).
    learner_arch = None
    if isinstance(checkpoint, dict):
        if algo == "ppo":
            from core.models.PPO import ppo_arch_from_payload

            learner_arch = ppo_arch_from_payload(checkpoint)
        elif is_alphazero_net_algo(algo):
            from core.models.alphazero_model import alphazero_arch_from_payload

            learner_arch = alphazero_arch_from_payload(checkpoint)
        elif algo == "sampled_muzero":
            from core.models.sampled_muzero_model import sampled_muzero_arch_from_payload

            learner_arch = sampled_muzero_arch_from_payload(checkpoint)
    learner_agent = build_eval_agent(
        algo=algo,
        policy_state=normalize_state_dict(learner_state),
        contract=eval_contract,
        len_model=len(model_units),
        cfg=cfg,
        device=device,
        arch=learner_arch,
    )

    # Симметричный reaction-словарь: обе стороны (model/enemy) одной фабрикой.
    _eu = unwrap_env(env)
    _reaction_net_by_side = {
        "model": learner_agent.reaction_net,
        "enemy": getattr(opponent_agent, "reaction_net", None),
    }
    if any(v is not None for v in _reaction_net_by_side.values()):
        from core.models.reaction_value_policy import make_reaction_value_policy

        _eu._reaction_net_by_side = _reaction_net_by_side
        _eu.reaction_policy = make_reaction_value_policy(_reaction_net_by_side, device=device)
        log("[EVAL][CONFIG] reaction_value_policy установлена both-sides (model/enemy).")

    az_eval_mode = str(os.getenv("AZ_EVAL_MODE", "mcts")).strip().lower() or "mcts"
    az_opp_mode = str(os.getenv("AZ_EVAL_OPPONENT_MODE", "mcts")).strip().lower() or "mcts"
    gmz_eval_mode = str(os.getenv("GMZ_EVAL_MODE", "search")).strip().lower() or "search"
    gmz_opp_mode = str(os.getenv("GMZ_OPPONENT_MODE", "search")).strip().lower() or "search"
    gaz_eval_mode = str(os.getenv("GAZ_EVAL_MODE", "gumbel")).strip().lower() or "gumbel"
    gaz_opp_mode = str(os.getenv("GAZ_EVAL_OPPONENT_MODE", "gumbel")).strip().lower() or "gumbel"
    if az_eval_mode not in {"greedy", "mcts"}:
        az_eval_mode = "mcts"
    if az_opp_mode not in {"greedy", "mcts"}:
        az_opp_mode = "mcts"
    if gmz_eval_mode not in {"greedy", "search"}:
        gmz_eval_mode = "search"
    if gmz_opp_mode not in {"greedy", "search"}:
        gmz_opp_mode = "search"
    if gaz_eval_mode not in {"greedy", "gumbel"}:
        gaz_eval_mode = "gumbel"
    if gaz_opp_mode not in {"greedy", "gumbel"}:
        gaz_opp_mode = "gumbel"
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
    smz_eval_mode = str(os.getenv("SMZ_EVAL_MODE", "search")).strip().lower() or "search"
    smz_opp_mode = str(os.getenv("SMZ_OPPONENT_MODE", "search")).strip().lower() or "search"
    if smz_eval_mode not in {"greedy", "search"}:
        smz_eval_mode = "search"
    if smz_opp_mode not in {"greedy", "search"}:
        smz_opp_mode = "search"
    if algo == "sampled_muzero" or opponent_algo_label == "sampled_muzero":
        smz_eval_tail = f"smz_eval_mode={smz_eval_mode}"
        smz_opp_tail = f"smz_opponent_mode={smz_opp_mode}"
        if algo == "sampled_muzero" and smz_eval_mode == "search":
            smz_eval_tail += f"(temp={float(os.getenv('SMZ_EVAL_TEMPERATURE', '0.10')):.3f})"
        if opponent_algo_label == "sampled_muzero" and smz_opp_mode == "search":
            smz_opp_tail += (
                f"(temp={float(os.getenv('SMZ_EVAL_OPPONENT_TEMPERATURE', os.getenv('SMZ_EVAL_TEMPERATURE', '0.10'))):.3f})"
            )
        mode_parts.append(smz_eval_tail)
        mode_parts.append(smz_opp_tail)
    if is_gumbel_az_algo(algo) or is_gumbel_az_algo(opponent_algo_label):
        gaz_eval_tail = f"gaz_eval_mode={gaz_eval_mode}"
        gaz_opp_tail = f"gaz_opponent_mode={gaz_opp_mode}"
        if is_gumbel_az_algo(algo) and gaz_eval_mode == "gumbel":
            gaz_eval_tail += f"(temp={float(os.getenv('GAZ_EVAL_TEMPERATURE', '0.05')):.3f})"
        if is_gumbel_az_algo(opponent_algo_label) and gaz_opp_mode == "gumbel":
            gaz_opp_tail += f"(temp={float(os.getenv('GAZ_EVAL_TEMPERATURE', '0.05')):.3f})"
        mode_parts.append(gaz_eval_tail)
        mode_parts.append(gaz_opp_tail)
    if algo == "dqn" or opponent_algo_label == "dqn":
        # DQN→epsilon. Значение читаем из env (DQN_EVAL_EPSILON): резолвер унифицирован,
        # и для dqn-оппонента learner-cfg.epsilon относится к другому algo — врал бы 0.
        dqn_mode = str(os.getenv("DQN_EVAL_MODE", "greedy")).strip().lower() or "greedy"
        dqn_tail = f"dqn_eval_mode={dqn_mode}"
        if dqn_mode == "epsilon":
            dqn_tail += f"(eps={float(os.getenv('DQN_EVAL_EPSILON', '0')):.3f})"
        mode_parts.append(dqn_tail)
    if algo == "ppo" or opponent_algo_label == "ppo":
        # PPO→temperature. Температуру читаем из env (PPO_EVAL_TEMPERATURE) по той же причине.
        ppo_mode = str(os.getenv("PPO_EVAL_MODE", "greedy")).strip().lower() or "greedy"
        ppo_tail = f"ppo_eval_mode={ppo_mode}"
        if ppo_mode == "stochastic":
            ppo_tail += f"(temp={float(os.getenv('PPO_EVAL_TEMPERATURE', '1.0')):.3f})"
        mode_parts.append(ppo_tail)
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

    clear_eval_stop_flag()

    def _run_assignment(
        _env,
        _model_units,
        _enemy_units,
        _learner_agent,
        _opponent_agent,
        _device,
        _games: int,
        _learner_side: str,
        *,
        assignment_label: str = "",
    ) -> dict:
        """Прогон N игр одного назначения (learner=model, opponent=enemy). Возвращает агрегированные метрики."""
        # M1: len_model каждого агента берётся из своей стороны (model/enemy units) и предполагает
        # зеркальные ростеры. При --swap-sides с асимметричными ростерами граница move-head цикла
        # (range(len_model)) у сторон может отличаться — учесть при анализе таких прогонов.
        _opponent_side = "P2" if str(_learner_side).upper() == "P1" else "P1"
        wins = 0
        losses = 0
        _draws = 0
        p1_wins = 0
        p2_wins = 0
        vp_diffs: list[int] = []
        p1_vps: list[int] = []
        p2_vps: list[int] = []
        ep_lens: list[int] = []
        hp_diffs_p1_minus_p2: list[float] = []
        kill_diffs_p1_minus_p2: list[float] = []
        rewards_learner: list[float] = []
        end_reasons_v2: Counter[str] = Counter()
        step_metrics: Counter[str] = Counter()
        action_tuple_counter: Counter[tuple] = Counter()
        model_action_re = re.compile(
            r"move=(?P<move>-?\d+).*?attack=(?P<attack>-?\d+).*?shoot=(?P<shoot>-?\d+).*?"
            r"charge=(?P<charge>-?\d+).*?"
            r"masks=\(move:(?P<move_v>\d+)/(?P<move_t>\d+), attack:(?P<attack_v>\d+)/(?P<attack_t>\d+), "
            r"shoot:(?P<shoot_v>\d+)/(?P<shoot_t>\d+), charge:(?P<charge_v>\d+)/(?P<charge_t>\d+),"
        )
        step_result_re = re.compile(r"model_ctrl_n=(?P<model_ctrl>\d+)")
        strat_attempt_re = re.compile(r"stratagem=(?P<sid>\S+)")
        strat_applied_re = re.compile(r"applied=(?P<sid>\S+)")
        _label = f" [{assignment_label}]" if assignment_label else ""

        for idx in range(1, _games + 1):
            if eval_stop_requested():
                log(f"Остановка по запросу пользователя после {idx - 1}/{_games} игр{_label}.")
                break
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
                _env,
                _model_units,
                _enemy_units,
                _learner_agent,
                _opponent_agent,
                _device,
                learner_side=_learner_side,
            )
            for line in trace_lines:
                _append_eval_log(f"[TRACE][GAME {idx}]{_label} {line}")
                if line.startswith("[TRACE][MODEL_ACTION_HUMAN]"):
                    m = model_action_re.search(line)
                    if m:
                        move = int(m.group("move"))
                        attack = int(m.group("attack"))
                        shoot = int(m.group("shoot"))
                        charge = int(m.group("charge"))
                        move_v = int(m.group("move_v"))
                        shoot_v = int(m.group("shoot_v"))
                        charge_v = int(m.group("charge_v"))
                        step_metrics["total_model_steps"] += 1
                        action_tuple_counter[(move, attack, shoot, charge)] += 1
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
                elif line.startswith("[WH40K][STRATAGEM][ATTEMPT]"):
                    step_metrics["stratagem_attempt_total"] += 1
                    m = strat_attempt_re.search(line)
                    if m:
                        step_metrics[f"strat_attempt_{m.group('sid')}"] += 1
                elif line.startswith("[WH40K][STRATAGEM] applied="):
                    step_metrics["stratagem_applied_total"] += 1
                    m = strat_applied_re.search(line)
                    if m:
                        step_metrics[f"strat_applied_{m.group('sid')}"] += 1
                elif line.startswith("[WH40K][STRATAGEM][MISS]"):
                    step_metrics["stratagem_miss_total"] += 1
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
            if _learner_side == "P1":
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
                winner_side = _learner_side
            elif winner == "enemy":
                losses += 1
                winner_side = _opponent_side
            else:
                _draws += 1
                winner_side = "draw"

            if winner_side == "P1":
                p1_wins += 1
            elif winner_side == "P2":
                p2_wins += 1

            end_reasons_v2[str(end_reason or "unknown")] += 1
            log(
                "Игра "
                f"{idx}/{_games}{_label}: "
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

        played_games = len(vp_diffs)
        return {
            "model_wins": wins,
            "enemy_wins": losses,
            "draws": _draws,
            "games": played_games,
            "p1_wins": p1_wins,
            "p2_wins": p2_wins,
            "vp_diffs": vp_diffs,
            "p1_vps": p1_vps,
            "p2_vps": p2_vps,
            "ep_lens": ep_lens,
            "hp_diffs_p1_minus_p2": hp_diffs_p1_minus_p2,
            "kill_diffs_p1_minus_p2": kill_diffs_p1_minus_p2,
            "rewards_learner": rewards_learner,
            "end_reasons_v2": end_reasons_v2,
            "step_metrics": step_metrics,
            "action_tuple_counter": action_tuple_counter,
            "learner_side": _learner_side,
        }

    # --- Запуск назначений ---
    do_swap = bool(getattr(args, "swap_sides", False)) and opponent_agent is not None
    if do_swap:
        log("[EVAL][SWAP] --swap-sides: назначение A (learner=model, opponent=enemy)")
    res_a = _run_assignment(
        env, model_units, enemy_units, learner_agent, opponent_agent,
        device, games, learner_side,
        assignment_label="A" if do_swap else "",
    )

    res_b: dict | None = None
    if do_swap:
        log("[EVAL][SWAP] --swap-sides: назначение B (learner<->opponent swap)")
        # Переставляем reaction_net_by_side для симметрии (model<->enemy).
        _eu = unwrap_env(env)
        _swapped_reaction_net = {
            "model": getattr(opponent_agent, "reaction_net", None),
            "enemy": learner_agent.reaction_net,
        }
        if any(v is not None for v in _swapped_reaction_net.values()):
            from core.models.reaction_value_policy import make_reaction_value_policy

            _eu._reaction_net_by_side = _swapped_reaction_net
            _eu.reaction_policy = make_reaction_value_policy(_swapped_reaction_net, device=device)
            log("[EVAL][SWAP] reaction_value_policy переустановлена (model<->enemy swap).")
        res_b = _run_assignment(
            env, model_units, enemy_units, opponent_agent, learner_agent,
            device, games, learner_side,
            assignment_label="B",
        )
        # Восстановить оригинальный reaction_net_by_side после swap.
        _orig_reaction_net = {
            "model": learner_agent.reaction_net,
            "enemy": getattr(opponent_agent, "reaction_net", None),
        }
        if any(v is not None for v in _orig_reaction_net.values()):
            from core.models.reaction_value_policy import make_reaction_value_policy

            _eu._reaction_net_by_side = _orig_reaction_net
            _eu.reaction_policy = make_reaction_value_policy(_orig_reaction_net, device=device)

    # --- Агрегация ---
    if do_swap and res_b is not None:
        agg = _aggregate_swap(res_a, res_b)
        log(
            "[EVAL][SWAP][RESULT] Per-color агрегация: "
            f"agentA_winrate={agg['agentA_winrate']:.3f}, "
            f"agentB_winrate={agg['agentB_winrate']:.3f}, "
            f"total_games={agg['total_games']}, draws={agg['draws']}"
        )
        log(
            "[EVAL][SWAP][DETAIL] Назначение A: "
            f"model_wins={res_a['model_wins']}, enemy_wins={res_a['enemy_wins']}, "
            f"draws={res_a['draws']}, games={res_a['games']}"
        )
        log(
            "[EVAL][SWAP][DETAIL] Назначение B: "
            f"model_wins={res_b['model_wins']}, enemy_wins={res_b['enemy_wins']}, "
            f"draws={res_b['draws']}, games={res_b['games']}"
        )

    # Для итогового репорта используем res_a (или объединённые метрики при swap).
    _report = res_a
    if do_swap and res_b is not None:
        # Объединяем списочные метрики из обоих назначений для общего summary.
        _report = dict(res_a)
        _report["p1_wins"] = int(res_a.get("p1_wins", 0)) + int(res_b.get("p1_wins", 0))
        _report["p2_wins"] = int(res_a.get("p2_wins", 0)) + int(res_b.get("p2_wins", 0))
        _report["draws"] = int(res_a.get("draws", 0)) + int(res_b.get("draws", 0))
        _report["games"] = int(res_a.get("games", 0)) + int(res_b.get("games", 0))
        _report["vp_diffs"] = list(res_a.get("vp_diffs", [])) + list(res_b.get("vp_diffs", []))
        _report["p1_vps"] = list(res_a.get("p1_vps", [])) + list(res_b.get("p1_vps", []))
        _report["p2_vps"] = list(res_a.get("p2_vps", [])) + list(res_b.get("p2_vps", []))
        _report["ep_lens"] = list(res_a.get("ep_lens", [])) + list(res_b.get("ep_lens", []))
        _report["hp_diffs_p1_minus_p2"] = list(res_a.get("hp_diffs_p1_minus_p2", [])) + list(res_b.get("hp_diffs_p1_minus_p2", []))
        _report["kill_diffs_p1_minus_p2"] = list(res_a.get("kill_diffs_p1_minus_p2", [])) + list(res_b.get("kill_diffs_p1_minus_p2", []))
        _report["rewards_learner"] = list(res_a.get("rewards_learner", [])) + list(res_b.get("rewards_learner", []))
        _merged_end_reasons: Counter[str] = Counter(res_a.get("end_reasons_v2", {}))
        _merged_end_reasons.update(res_b.get("end_reasons_v2", {}))
        _report["end_reasons_v2"] = _merged_end_reasons
        _merged_step_metrics: Counter[str] = Counter(res_a.get("step_metrics", {}))
        _merged_step_metrics.update(res_b.get("step_metrics", {}))
        _report["step_metrics"] = _merged_step_metrics
        _merged_actions: Counter[tuple] = Counter(res_a.get("action_tuple_counter", {}))
        _merged_actions.update(res_b.get("action_tuple_counter", {}))
        _report["action_tuple_counter"] = _merged_actions

    played_games = int(_report.get("games", 0))
    if played_games == 0:
        log("Оценка прервана до первой завершённой игры.")
        clear_eval_stop_flag()
        return 0

    p1_wins = int(_report["p1_wins"])
    p2_wins = int(_report["p2_wins"])
    draws = int(_report["draws"])
    vp_diffs = _report["vp_diffs"]
    p1_vps = _report["p1_vps"]
    p2_vps = _report["p2_vps"]
    ep_lens = _report["ep_lens"]
    hp_diffs_p1_minus_p2 = _report["hp_diffs_p1_minus_p2"]
    kill_diffs_p1_minus_p2 = _report["kill_diffs_p1_minus_p2"]
    rewards_learner = _report["rewards_learner"]
    end_reasons_v2 = _report["end_reasons_v2"]
    step_metrics = _report["step_metrics"]
    action_tuple_counter = _report["action_tuple_counter"]

    winrate_p1_all = p1_wins / played_games if played_games else 0.0
    winrate_p2_all = p2_wins / played_games if played_games else 0.0
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
        f"stratagem_attempt_total={int(step_metrics.get('stratagem_attempt_total', 0) or 0)} "
        f"stratagem_applied_total={int(step_metrics.get('stratagem_applied_total', 0) or 0)} "
        f"stratagem_miss_total={int(step_metrics.get('stratagem_miss_total', 0) or 0)} "
        f"turn_limit_count={turn_limit_count} "
        f"wipeout_model_count={wipeout_model_count} wipeout_enemy_count={wipeout_enemy_count} "
        f"wipeout_p1_count={wipeout_p1_count} wipeout_p2_count={wipeout_p2_count} "
        f"end_reasons={dict(end_reasons_v2)}"
    )

    log("[DETAIL] ---------- Подробный итог оценки ----------")
    log("[DETAIL] Стороны матча: P1 vs P2")
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
    clear_eval_stop_flag()
    return 0


if __name__ == "__main__":
    sys.exit(main())
