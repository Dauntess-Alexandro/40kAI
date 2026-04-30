from __future__ import annotations

import os
import pickle
import queue
import re
import threading
import traceback
import importlib
import types
import sys
from typing import Optional

import gymnasium as gym
import torch

from core.engine.agent_registry import compatible_contracts, load_agent_by_id, make_env_contract
from core.engine import Unit, initFile, unitData, weaponData
from core.engine.game_io import GuiIO, set_active_io
from core.engine.state_export import DEFAULT_STATE_PATH
from core.engine.mission import board_dims_for_mission
from core.models.DQN import DQN
from core.models.PPO import ActorCriticMultiHead
from core.models.alphazero_model import AlphaZeroPolicyValueNet
from core.models.utils import select_action, convertToDict, build_shoot_action_mask, normalize_state_dict
from core.models.utils import build_action_masks_by_head
from core.models.action_contract import action_sizes_from_env
from core.envs.warhamEnv import roll_off_attacker_defender
from project_paths import ARTIFACTS_MODELS_DIR


def _install_pickle_compat_aliases() -> None:
    """
    Backward compatibility for old pickle module paths.
    Older artifacts may store symbols from gym_mod.* and model.*.
    """
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
            # Keep unpickling resilient even if a specific alias fails.
            pass
    # Ensure package placeholders exist for nested imports.
    sys.modules.setdefault("gym_mod", types.ModuleType("gym_mod"))
    sys.modules.setdefault("model", types.ModuleType("model"))


def load_trusted_checkpoint(checkpoint_path: str):
    """Загрузка доверенного checkpoint с поддержкой разных версий PyTorch."""
    try:
        return torch.load(checkpoint_path, weights_only=False)
    except TypeError:
        return torch.load(checkpoint_path)


def n_actions_from_env(env, model_len: int) -> list[int]:
    """Совпадает с train.py: размеры голов действия из env.action_space."""
    return action_sizes_from_env(env, int(model_len))


def _build_units_from_runtime_config(b_len: int, b_hei: int):
    """Fallback roster loader for Viewer when no pickle exists."""
    enemy = []
    model = []
    enemy_faction = initFile.getEnemyFaction()
    model_faction = initFile.getModelFaction()
    enemy_units = initFile.getEnemyUnits()
    model_units = initFile.getModelUnits()
    enemy_weapons = initFile.getEnemyW()
    model_weapons = initFile.getModelW()
    enemy_counts = initFile.getEnemyUnitCounts()
    model_counts = initFile.getModelUnitCounts()
    enemy_ids = initFile.getEnemyUnitInstanceIds()
    model_ids = initFile.getModelUnitInstanceIds()

    for i, name in enumerate(enemy_units):
        udata = unitData(enemy_faction, name)
        cnt = enemy_counts[i] if i < len(enemy_counts) else 0
        if cnt:
            udata["#OfModels"] = int(cnt)
        wpair = enemy_weapons[i] if i < len(enemy_weapons) else ("None", "None")
        instance_id = enemy_ids[i] if i < len(enemy_ids) else None
        enemy.append(
            Unit(
                udata,
                weaponData(wpair[0]),
                weaponData(wpair[1]),
                int(b_len),
                int(b_hei),
                instance_id=instance_id,
            )
        )
    for i, name in enumerate(model_units):
        udata = unitData(model_faction, name)
        cnt = model_counts[i] if i < len(model_counts) else 0
        if cnt:
            udata["#OfModels"] = int(cnt)
        wpair = model_weapons[i] if i < len(model_weapons) else ("None", "None")
        instance_id = model_ids[i] if i < len(model_ids) else None
        model.append(
            Unit(
                udata,
                weaponData(wpair[0]),
                weaponData(wpair[1]),
                int(b_len),
                int(b_hei),
                instance_id=instance_id,
            )
        )
    return enemy, model


def resolve_checkpoint_for_pickle(pickle_path: str) -> Optional[str]:
    """
    Находит .pth для .pickle: обычно тот же stem; если нет — базовый run
    (model-<run>-<iter>.pth) или best_eval_checkpoint.pth в той же папке.
    Для PPO также поддерживаем checkpoint_ep*.pth (train.py сохраняет checkpoint_ep{episode}.pth).
    """
    if not pickle_path or not os.path.isfile(pickle_path):
        return None
    directory = os.path.dirname(os.path.abspath(pickle_path))
    base = os.path.splitext(os.path.basename(pickle_path))[0]

    primary = os.path.join(directory, base + ".pth")
    if os.path.isfile(primary):
        return primary

    m = re.match(r"^(model-\d+-\d+)", base)
    if m:
        fallback = os.path.join(directory, m.group(1) + ".pth")
        if os.path.isfile(fallback):
            return fallback

    best = os.path.join(directory, "best_eval_checkpoint.pth")
    if os.path.isfile(best):
        return best

    # PPO: checkpoint_ep{episode}.pth
    try:
        candidates: list[tuple[int, str]] = []
        for fn in os.listdir(directory):
            m_ep = re.match(r"^checkpoint_ep(\d+)\.pth$", str(fn))
            if not m_ep:
                continue
            ep = int(m_ep.group(1))
            full = os.path.join(directory, fn)
            if os.path.isfile(full):
                candidates.append((ep, full))
        if candidates:
            candidates.sort(key=lambda x: x[0])
            return candidates[-1][1]
    except Exception:
        pass

    return None


class GameController:
    def __init__(self, model_path: Optional[str] = None, state_path: Optional[str] = None):
        self.model_path = model_path or "None"
        self.state_path = state_path or os.getenv("STATE_JSON_PATH", DEFAULT_STATE_PATH)
        self._request_queue: queue.Queue = queue.Queue()
        self._answer_queue: queue.Queue = queue.Queue()
        self._io = GuiIO(self._request_queue, self._answer_queue)
        self._thread: Optional[threading.Thread] = None
        self._finished = False
        self._started = False

    @property
    def is_finished(self) -> bool:
        return self._finished

    def start(self):
        if self._started:
            return self._consume_messages(), self._next_request(block=False)
        self._started = True
        self._thread = threading.Thread(target=self._run_game_loop, daemon=True)
        self._thread.start()
        request = self._next_request(block=True)
        return self._consume_messages(), request

    def answer(self, value):
        if self._finished:
            return [], None
        self._answer_queue.put(value)
        request = self._next_request(block=True)
        return self._consume_messages(), request

    def _consume_messages(self):
        return self._io.consume_messages()

    def _next_request(self, block: bool):
        if self._finished and self._request_queue.empty():
            return None
        if not block:
            try:
                return self._request_queue.get_nowait()
            except queue.Empty:
                return None
        while True:
            try:
                return self._request_queue.get(timeout=0.1)
            except queue.Empty:
                if self._finished:
                    return None

    def _load_game(self):
        agent_id_override = os.getenv("VIEWER_AGENT_ID", "").strip()
        if isinstance(self.model_path, str) and self.model_path.startswith("agent:"):
            agent_id_override = self.model_path.split("agent:", 1)[1].strip()
        if self.model_path == "None":
            save_path = str(ARTIFACTS_MODELS_DIR) + os.sep
            folders = os.listdir(save_path) if os.path.isdir(save_path) else []
            paired_models = []

            for folder in folders:
                full = os.path.join(save_path, folder)
                if os.path.isdir(full):
                    files = os.listdir(full)
                    for filename in files:
                        if not filename.endswith(".pickle"):
                            continue
                        pickle_path = os.path.join(full, filename)
                        checkpoint_path = resolve_checkpoint_for_pickle(pickle_path)
                        if checkpoint_path:
                            paired_models.append((os.path.getmtime(pickle_path), pickle_path, checkpoint_path))

            if not paired_models:
                if not agent_id_override:
                    raise FileNotFoundError(
                        "Не найдены пары файлов моделей (.pickle/.pth) в папке artifacts/models/."
                    )
                mission_name = str(os.getenv("MISSION_NAME", "") or "").strip() or "only_war"
                b_len, b_hei = board_dims_for_mission(mission_name)
                enemy, model = _build_units_from_runtime_config(int(b_len), int(b_hei))
                env = gym.make(
                    "40kAI-v0",
                    disable_env_checker=True,
                    enemy=enemy,
                    model=model,
                    b_len=int(b_len),
                    b_hei=int(b_hei),
                )
                self._io.log(
                    "[VIEWER][BOOTSTRAP] pickle/checkpoint не найдены; "
                    "использую runtime roster (train_data/units) + agent-id."
                )
                checkpoint = {"algo": "dqn"}
                payload = load_agent_by_id(agent_id_override)
                model_info, enemy_info = env.reset(options={"m": model, "e": enemy, "playType": True, "Type": "big", "trunc": True})
                n_actions = n_actions_from_env(env, len(model))
                runtime_contract = make_env_contract(
                    n_observations=len(model_info),
                    n_actions=n_actions,
                    mission_name=str(getattr(env.unwrapped, "mission_name", "only_war")),
                    ruleset_version=str(os.getenv("RULESET_VERSION", "only_war_v1")),
                )
                ok, reason = compatible_contracts(runtime_contract, payload.get("contract", {}))
                if not ok:
                    raise ValueError(
                        f"Несовместимый VIEWER_AGENT_ID={agent_id_override}: {reason}. "
                        "Что делать дальше: выберите агента с тем же контрактом."
                    )
                policy_state = payload.get("policy_state") or {}
                target_state = payload.get("target_state")
                optimizer_state = payload.get("optimizer_state") or {}
                meta = payload.get("meta") if isinstance(payload.get("meta"), dict) else {}
                agent_algo = str(meta.get("algo", "")).strip().lower()
                if agent_algo not in {"dqn", "ppo", "alphazero"}:
                    if any(str(k).startswith("policy_heads.") for k in policy_state.keys()):
                        agent_algo = "ppo"
                    else:
                        agent_algo = "dqn"
                if agent_algo == "ppo":
                    checkpoint = {"actor_critic": policy_state, "algo": "ppo"}
                elif agent_algo == "alphazero":
                    checkpoint = {"policy_value_net": policy_state, "algo": "alphazero"}
                else:
                    checkpoint = {
                        "policy_net": policy_state,
                        "target_net": target_state or policy_state,
                        "optimizer": optimizer_state,
                        "net_type": "dueling" if any(str(k).startswith("value_heads.") for k in policy_state.keys()) else "basic",
                        "algo": "dqn",
                    }
                checkpoint["_viewer_agent_id"] = agent_id_override
                checkpoint["_viewer_model_source"] = "registry"
                checkpoint["_viewer_bootstrap_pickle"] = "-"
                checkpoint["_viewer_bootstrap_checkpoint"] = "-"
                self._io.log(f"[LEAGUE] Viewer использует agent-id={agent_id_override}")
                return env, model, enemy, checkpoint

            paired_models.sort(key=lambda item: item[0])
            _, model_path, checkpoint_path = paired_models[-1]
        else:
            model_path = self.model_path
            if not os.path.isfile(model_path):
                raise FileNotFoundError(f"Не найден файл модели: {model_path}")
            expected = os.path.splitext(model_path)[0] + ".pth"
            checkpoint_path = resolve_checkpoint_for_pickle(model_path)
            if not checkpoint_path:
                raise FileNotFoundError(
                    f"Не найден checkpoint для модели. Ожидался файл рядом с pickle: {expected}. "
                    "Допустимы также базовый model-<run>-<iter>.pth, best_eval_checkpoint.pth, "
                    "а для PPO — checkpoint_ep<episode>.pth в той же папке. "
                    f"Папка: {os.path.dirname(os.path.abspath(model_path))}"
                )
            if os.path.normpath(checkpoint_path) != os.path.normpath(expected):
                self._io.log(f"[MODEL] checkpoint: используется {checkpoint_path} (рядом нет {expected})")

        if agent_id_override:
            self._io.log(f"[VIEWER][BOOTSTRAP] pickle={model_path}")
            self._io.log(f"[VIEWER][BOOTSTRAP] checkpoint={checkpoint_path}")
            self._io.log("[VIEWER][BOOTSTRAP] source используется только для env/roster, сеть берется из agent-id.")
        else:
            self._io.log(f"[MODEL] pickle={model_path}")
            self._io.log(f"[MODEL] checkpoint={checkpoint_path}")

        _install_pickle_compat_aliases()
        with open(model_path, "rb") as handle:
            loaded = pickle.load(handle)
        # Исторически сохранялось как (env, model, enemy).
        # Для PPO часто: (None, model, enemy).
        if isinstance(loaded, (list, tuple)) and len(loaded) >= 3:
            env, model, enemy = loaded[0], loaded[1], loaded[2]
        else:
            raise ValueError(
                "Неожиданный формат pickle модели. Ожидалось (env, model, enemy). "
                f"Фактически: {type(loaded)}."
            )

        # PPO pickles могут хранить env=None (мы сохраняем только roster'ы).
        # В этом случае создаём env заново из текущей миссии.
        if env is None:
            mission_name = str(os.getenv("MISSION_NAME", "") or "").strip() or "only_war"
            try:
                b_len, b_hei = board_dims_for_mission(mission_name)
            except Exception:
                b_len, b_hei = (30, 44)
            env = gym.make(
                "40kAI-v0",
                disable_env_checker=True,
                enemy=enemy,
                model=model,
                b_len=int(b_len),
                b_hei=int(b_hei),
            )
            self._io.log(f"[MODEL] env отсутствовал в pickle: пересоздан (mission={mission_name}, b_len={int(b_len)}, b_hei={int(b_hei)})")
            try:
                env.unwrapped.mission_name = mission_name
            except Exception:
                pass

        checkpoint = load_trusted_checkpoint(checkpoint_path)
        if agent_id_override:
            payload = load_agent_by_id(agent_id_override)
            model_info, enemy_info = env.reset(options={"m": model, "e": enemy, "playType": True, "Type": "big", "trunc": True})
            n_actions = n_actions_from_env(env, len(model))
            runtime_contract = make_env_contract(
                n_observations=len(model_info),
                n_actions=n_actions,
                mission_name=str(getattr(env.unwrapped, "mission_name", "only_war")),
                ruleset_version=str(os.getenv("RULESET_VERSION", "only_war_v1")),
            )
            ok, reason = compatible_contracts(runtime_contract, payload.get("contract", {}))
            if not ok:
                raise ValueError(
                    f"Несовместимый VIEWER_AGENT_ID={agent_id_override}: {reason}. "
                    "Что делать дальше: выберите агента с тем же контрактом."
                )
            policy_state = payload.get("policy_state") or {}
            target_state = payload.get("target_state")
            optimizer_state = payload.get("optimizer_state") or {}
            meta = payload.get("meta") if isinstance(payload.get("meta"), dict) else {}
            agent_algo = str(meta.get("algo", "")).strip().lower()
            if agent_algo not in {"dqn", "ppo", "alphazero"}:
                # Backward-compat: для старых снапшотов infer по структуре state_dict.
                if any(str(k).startswith("policy_heads.") for k in policy_state.keys()):
                    agent_algo = "ppo"
                else:
                    agent_algo = "dqn"

            if agent_algo == "ppo":
                checkpoint = {
                    "actor_critic": policy_state,
                    "algo": "ppo",
                    "_viewer_agent_id": agent_id_override,
                    "_viewer_model_source": "registry",
                    "_viewer_bootstrap_pickle": model_path,
                    "_viewer_bootstrap_checkpoint": checkpoint_path,
                }
            elif agent_algo == "alphazero":
                checkpoint = {
                    "policy_value_net": policy_state,
                    "algo": "alphazero",
                    "_viewer_agent_id": agent_id_override,
                    "_viewer_model_source": "registry",
                    "_viewer_bootstrap_pickle": model_path,
                    "_viewer_bootstrap_checkpoint": checkpoint_path,
                }
            else:
                checkpoint = {
                    "policy_net": policy_state,
                    "target_net": target_state or policy_state,
                    "optimizer": optimizer_state,
                    "net_type": "dueling"
                    if any(str(k).startswith("value_heads.") for k in policy_state.keys())
                    else "basic",
                    "algo": "dqn",
                    "_viewer_agent_id": agent_id_override,
                    "_viewer_model_source": "registry",
                    "_viewer_bootstrap_pickle": model_path,
                    "_viewer_bootstrap_checkpoint": checkpoint_path,
                }
            self._io.log(f"[LEAGUE] Viewer использует agent-id={agent_id_override}")
        elif isinstance(checkpoint, dict):
            checkpoint["_viewer_agent_id"] = ""
            checkpoint["_viewer_model_source"] = "pickle_checkpoint"
            checkpoint["_viewer_bootstrap_pickle"] = model_path
            checkpoint["_viewer_bootstrap_checkpoint"] = checkpoint_path
        return env, model, enemy, checkpoint

    def _run_game_loop(self):
        os.environ["STATE_JSON_PATH"] = self.state_path
        os.environ.setdefault("VIEWER_PACING_MODE", "per_unit")
        if "MANUAL_DICE" not in os.environ:
            os.environ["MANUAL_DICE"] = "1"
        if "VERBOSE_LOGS" not in os.environ and os.environ.get("MANUAL_DICE") == "1":
            os.environ["VERBOSE_LOGS"] = "1"
        set_active_io(self._io)

        try:
            env, model, enemy, checkpoint = self._load_game()

            if os.getenv("PLAY_NO_EXPLORATION", "0") == "1" or os.getenv("FORCE_GREEDY", "0") == "1":
                self._io.log("[MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).")

            env.io = self._io
            env.playType = True

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

            attacker_side, defender_side = roll_off_attacker_defender(
                manual_roll_allowed=True,
                log_fn=self._io.log,
            )

            self._io.log(
                "Юниты: "
                + str(
                    [
                        (u.name, getattr(u, "instance_id", "unknown"), u.models_count)
                        for u in model
                    ]
                )
            )

            from core.engine.mission import normalize_mission_name, deploy_for_mission, post_deploy_setup

            mission_name = normalize_mission_name(getattr(env.unwrapped, "mission_name", None))
            deployment_mode = str(os.getenv("DEPLOYMENT_MODE", "auto")).strip().lower() or "auto"
            deployment_strategy = str(os.getenv("DEPLOYMENT_STRATEGY", "template_jitter")).strip().lower() or "template_jitter"
            deployment_seed_raw = os.getenv("DEPLOYMENT_SEED", "").strip()
            deployment_seed = None
            if deployment_seed_raw:
                try:
                    deployment_seed = int(deployment_seed_raw)
                except ValueError:
                    self._io.log(
                        f"[DEPLOY] invalid DEPLOYMENT_SEED='{deployment_seed_raw}'. "
                        "Где: game_controller._run_game_loop. Что делать дальше: укажите целое число."
                    )
            self._io.log(
                f"[DEPLOY] mode={deployment_mode}, strategy={deployment_strategy}, seed={deployment_seed_raw or 'none'}"
            )
            deploy_stats = deploy_for_mission(
                mission_name,
                model_units=model,
                enemy_units=enemy,
                b_len=env.unwrapped.b_len,
                b_hei=env.unwrapped.b_hei,
                attacker_side=attacker_side,
                log_fn=self._io.log,
                deployment_seed=deployment_seed,
                deployment_strategy=deployment_strategy,
                deployment_mode=deployment_mode,
            )
            if deploy_stats:
                self._io.log(f"[DEPLOY] rl_phase stats: {deploy_stats}")
            post_deploy_setup(log_fn=self._io.log)

            env.attacker_side = attacker_side
            env.defender_side = defender_side
            env.deployment_mode = deployment_mode
            env.deployment_rl_stats = deploy_stats if isinstance(deploy_stats, dict) else None

            state, info = env.reset(
                options={"m": model, "e": enemy, "playType": True, "Type": "big", "trunc": True}
            )

            n_actions = n_actions_from_env(env, len(model))
            n_observations = len(state)
            self._io.log(f"[MODEL] n_actions (из env): {n_actions}")

            algo = str(checkpoint.get("algo", "dqn")).strip().lower() if isinstance(checkpoint, dict) else "dqn"
            if algo == "ppo":
                self._io.log("[MODEL] Архитектура сети: ppo_actor_critic")
                ppo_state = checkpoint.get("actor_critic", checkpoint.get("policy_net", {}))
                policy_net = ActorCriticMultiHead(n_observations, n_actions).to(device)
                policy_net.load_state_dict(normalize_state_dict(ppo_state))
                policy_net.eval()
                target_net = None
            elif algo == "alphazero":
                self._io.log("[MODEL] Архитектура сети: alphazero_policy_value")
                az_state = checkpoint.get("policy_value_net", checkpoint.get("policy_net", {}))
                policy_net = AlphaZeroPolicyValueNet(n_observations, n_actions).to(device)
                policy_net.load_state_dict(normalize_state_dict(az_state))
                policy_net.eval()
                target_net = None
            else:
                net_type = checkpoint.get("net_type") if isinstance(checkpoint, dict) else None
                dueling = net_type == "dueling"
                if not dueling and isinstance(checkpoint, dict):
                    policy_state = normalize_state_dict(checkpoint.get("policy_net", {}))
                    if any(key.startswith("advantage_heads.") for key in policy_state.keys()):
                        dueling = True
                net_label = "dueling" if dueling else "basic"
                net_source = "net_type" if net_type else "state_dict"
                self._io.log(f"[MODEL] Архитектура сети: {net_label} (источник: {net_source})")
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
                optimizer = torch.optim.Adam(policy_net.parameters())
                policy_net.load_state_dict(normalize_state_dict(checkpoint["policy_net"]))
                target_net.load_state_dict(normalize_state_dict(checkpoint["target_net"]))
                optimizer.load_state_dict(checkpoint["optimizer"])
                policy_net.eval()
                target_net.eval()

            viewer_agent_id = str(checkpoint.get("_viewer_agent_id", "")).strip() if isinstance(checkpoint, dict) else ""
            viewer_model_source = str(checkpoint.get("_viewer_model_source", "")).strip() if isinstance(checkpoint, dict) else ""
            if viewer_model_source == "registry" and viewer_agent_id:
                self._io.log(
                    f"[VIEWER][MODEL_SELECTED] algo={algo} agent_id={viewer_agent_id} source=registry deterministic=1"
                )
                self._io.log(
                    "[VIEWER][MODEL_SELECTED] "
                    f"bootstrap_pickle={checkpoint.get('_viewer_bootstrap_pickle', '-')} "
                    f"bootstrap_checkpoint={checkpoint.get('_viewer_bootstrap_checkpoint', '-')}"
                )
            else:
                self._io.log(
                    "[VIEWER][MODEL_SELECTED] "
                    f"algo={algo} agent_id=- source=pickle_checkpoint "
                    f"pickle={checkpoint.get('_viewer_bootstrap_pickle', '-')} "
                    f"checkpoint={checkpoint.get('_viewer_bootstrap_checkpoint', '-')}"
                )

            self._io.log(
                "\nИнструкции:\nИгрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).\n"
                "Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).\n"
            )

            is_done = False
            i = 0
            reward = 0

            def update_board(target_env):
                board_env = target_env
                if not hasattr(board_env, "updateBoard") and hasattr(board_env, "unwrapped"):
                    board_env = board_env.unwrapped
                if hasattr(board_env, "updateBoard"):
                    board_env.updateBoard()

            while not is_done:
                done, info = env.unwrapped.player()
                update_board(env)
                state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
                shoot_mask = build_shoot_action_mask(env)
                if algo == "ppo":
                    masks = build_action_masks_by_head(env, len(model), log_fn=None, debug=False)
                    masks_b = [m.to(state_tensor.device).unsqueeze(0) for m in masks]
                    with torch.no_grad():
                        action, _, _ = policy_net.act(state_tensor, masks_by_head=masks_b, deterministic=True)
                    action = action.to("cpu")
                elif algo == "alphazero":
                    masks = build_action_masks_by_head(env, len(model), log_fn=None, debug=False)
                    masks_b = [m.to(state_tensor.device).unsqueeze(0) for m in masks]
                    with torch.no_grad():
                        probs, _value = policy_net.infer(state_tensor, masks_by_head=masks_b)
                    action_list = [int(torch.argmax(p.squeeze(0), dim=0).item()) for p in probs]
                    action = torch.tensor([action_list], device="cpu")
                else:
                    action = select_action(env, state_tensor, i, policy_net, len(model), shoot_mask=shoot_mask)
                action_dict = convertToDict(action)
                if done is not True:
                    next_observation, reward, done, _, info = env.step(action_dict)
                    reward_tensor = torch.tensor([reward], device=device)
                    unit_health = info["model health"]
                    enemy_health = info["player health"]

                    message = (
                        f"Итерация {i} завершена с наградой {reward_tensor}, "
                        f"здоровье игрока {enemy_health}, здоровье модели {unit_health}"
                    )
                    self._io.log(message)
                    state = next_observation
                    update_board(env)

                if done is True:
                    if reward > 0:
                        self._io.log("Модель победила!")
                    else:
                        self._io.log("Вы победили!")
                    is_done = True
                i += 1

            self._finished = True
        except Exception as exc:
            trace = traceback.format_exc()
            last_trace_line = "не удалось определить"
            try:
                lines = [line.strip() for line in trace.splitlines() if line.strip()]
                for line in reversed(lines):
                    if line.startswith("File "):
                        last_trace_line = line
                        break
            except Exception:
                pass
            self._io.log(
                f"Ошибка игры: {exc}. Место: game_controller._run_game_loop ({last_trace_line}). "
                "Что делать дальше: проверьте traceback ниже и исправьте источник ошибки в указанном файле/строке."
            )
            self._io.log("Traceback (последние вызовы):")
            for line in trace.rstrip().splitlines():
                self._io.log(line)
            self._finished = True
