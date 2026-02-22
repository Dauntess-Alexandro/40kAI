from __future__ import annotations

import os
import pickle
import queue
import threading
from typing import Optional

import torch

from gym_mod.engine.game_io import GuiIO, set_active_io
from gym_mod.engine.state_export import DEFAULT_STATE_PATH
from model.DQN import DQN
from model.alphazero import canonical_action_keys, flatten_observation, load_alphazero_checkpoint, to_action_dict
from model.utils import select_action, convertToDict, build_shoot_action_mask, normalize_state_dict
from gym_mod.envs.warhamEnv import roll_off_attacker_defender


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
        if self.model_path == "None":
            save_path = "models/"
            candidates = []
            if os.path.isdir(save_path):
                for root, _, files in os.walk(save_path):
                    for filename in files:
                        if filename.endswith(".pickle"):
                            candidates.append(os.path.join(root, filename))
            if not candidates:
                raise FileNotFoundError("Не найдены модели .pickle в папке models/.")
            candidates.sort(key=lambda p: os.path.getmtime(p))
            model_path = candidates[-1]
        else:
            model_path = self.model_path
            if not os.path.isfile(model_path):
                raise FileNotFoundError(f"Не найден файл модели: {model_path}")

        self._io.log(f"[MODEL] pickle={model_path}")

        with open(model_path, "rb") as handle:
            payload = pickle.load(handle)

        if isinstance(payload, dict) and payload.get("agent_type") == "alphazero":
            checkpoint_path = payload.get("checkpoint") or (os.path.splitext(model_path)[0] + ".pth")
            if not os.path.isfile(checkpoint_path):
                raise FileNotFoundError(
                    f"Не найден checkpoint для AlphaZero: {checkpoint_path}. "
                    "Проверьте, что рядом есть .pth файл."
                )
            self._io.log(f"[MODEL] checkpoint={checkpoint_path}")
            from gym_mod.engine import Unit, initFile, unitData, weaponData
            from gym_mod.engine.mission import board_dims_for_mission, normalize_mission_name
            import gymnasium as gym
            import gym_mod  # noqa: F401

            mission = normalize_mission_name(getattr(initFile, "getMission", lambda: "only_war")()) if os.path.isfile("gui/data.json") else "only_war"
            b_len, b_hei = board_dims_for_mission(mission)
            if os.path.isfile("gui/data.json"):
                enemy_faction = initFile.getEnemyFaction()
                model_faction = initFile.getModelFaction()
                enemy_units = [
                    (initFile.getEnemyUnits()[i], (initFile.getEnemyW()[i][0], initFile.getEnemyW()[i][1]), initFile.getEnemyUnitCounts()[i] if i < len(initFile.getEnemyUnitCounts()) else None, initFile.getEnemyUnitInstanceIds()[i] if i < len(initFile.getEnemyUnitInstanceIds()) else None)
                    for i in range(len(initFile.getEnemyUnits()))
                ]
                model_units = [
                    (initFile.getModelUnits()[i], (initFile.getModelW()[i][0], initFile.getModelW()[i][1]), initFile.getModelUnitCounts()[i] if i < len(initFile.getModelUnitCounts()) else None, initFile.getModelUnitInstanceIds()[i] if i < len(initFile.getModelUnitInstanceIds()) else None)
                    for i in range(len(initFile.getModelUnits()))
                ]
            else:
                enemy_faction = model_faction = "Necrons"
                enemy_units = [
                    ("Necron Warriors", ("Gauss flayer", "Necron close combat weapon"), None, None),
                    ("Royal Warden", ("Relic gauss blaster", "Royal warden close combat weapon"), None, None),
                ]
                model_units = list(enemy_units)

            enemy, model = [], []
            for name, weapons, count, instance_id in enemy_units:
                u = unitData(enemy_faction, name)
                if count:
                    u["#OfModels"] = count
                enemy.append(Unit(u, weaponData(weapons[0]), weaponData(weapons[1]), b_len, b_hei, instance_id=instance_id))
            for name, weapons, count, instance_id in model_units:
                u = unitData(model_faction, name)
                if count:
                    u["#OfModels"] = count
                model.append(Unit(u, weaponData(weapons[0]), weaponData(weapons[1]), b_len, b_hei, instance_id=instance_id))

            env = gym.make("40kAI-v0", disable_env_checker=True, enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
            env.reset(options={"m": model, "e": enemy, "Type": "small", "trunc": True})
            checkpoint = torch.load(checkpoint_path)
            return env, model, enemy, checkpoint, "alphazero", checkpoint_path

        checkpoint_path = os.path.splitext(model_path)[0] + ".pth"
        if not os.path.isfile(checkpoint_path):
            raise FileNotFoundError(
                f"Не найден checkpoint для модели: {checkpoint_path}. "
                "Проверьте, что рядом есть .pth файл."
            )
        self._io.log(f"[MODEL] checkpoint={checkpoint_path}")
        env, model, enemy = payload
        checkpoint = torch.load(checkpoint_path)
        return env, model, enemy, checkpoint, "dqn", checkpoint_path

    def _run_game_loop(self):
        os.environ["STATE_JSON_PATH"] = self.state_path
        if "MANUAL_DICE" not in os.environ:
            os.environ["MANUAL_DICE"] = "1"
        if "VERBOSE_LOGS" not in os.environ and os.environ.get("MANUAL_DICE") == "1":
            os.environ["VERBOSE_LOGS"] = "1"
        set_active_io(self._io)

        try:
            env, model, enemy, checkpoint, agent_type, checkpoint_path = self._load_game()

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

            from gym_mod.engine.mission import normalize_mission_name, deploy_for_mission, post_deploy_setup

            mission_name = normalize_mission_name(getattr(env.unwrapped, "mission_name", None))
            deploy_for_mission(
                mission_name,
                model_units=model,
                enemy_units=enemy,
                b_len=env.unwrapped.b_len,
                b_hei=env.unwrapped.b_hei,
                attacker_side=attacker_side,
                log_fn=self._io.log,
            )
            post_deploy_setup(log_fn=self._io.log)

            env.attacker_side = attacker_side
            env.defender_side = defender_side

            state, info = env.reset(
                options={"m": model, "e": enemy, "playType": True, "Type": "big", "trunc": True}
            )

            if agent_type == "alphazero":
                policy_net, _ = load_alphazero_checkpoint(checkpoint_path, device=device)
                policy_net = policy_net.to(device)
                policy_net.eval()
                self._io.log("[MODEL] Архитектура сети: AlphaZero policy/value")
            else:
                n_actions = [5, 2, len(info["player health"]), len(info["player health"]), 5, len(info["model health"])]
                for _ in range(len(model)):
                    n_actions.append(12)
                n_observations = len(state)

                net_type = checkpoint.get("net_type") if isinstance(checkpoint, dict) else None
                dueling = net_type == "dueling"
                if not dueling and isinstance(checkpoint, dict):
                    policy_state = normalize_state_dict(checkpoint.get("policy_net", {}))
                    if any(key.startswith("advantage_heads.") for key in policy_state.keys()):
                        dueling = True

                net_label = "dueling" if dueling else "basic"
                net_source = "net_type" if net_type else "state_dict"
                self._io.log(f"[MODEL] Архитектура сети: {net_label} (источник: {net_source})")

                policy_net = DQN(n_observations, n_actions, dueling=dueling).to(device)
                target_net = DQN(n_observations, n_actions, dueling=dueling).to(device)
                optimizer = torch.optim.Adam(policy_net.parameters())

                policy_net.load_state_dict(normalize_state_dict(checkpoint["policy_net"]))
                target_net.load_state_dict(normalize_state_dict(checkpoint["target_net"]))
                optimizer.load_state_dict(checkpoint["optimizer"])

                policy_net.eval()
                target_net.eval()

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
                shoot_mask = build_shoot_action_mask(env)
                if agent_type == "alphazero":
                    logits, _ = policy_net(flatten_observation(state).to(device))
                    action_keys = canonical_action_keys(env.action_space)
                    action_vals = []
                    for head_idx, head_logits in enumerate(logits):
                        head = head_logits.squeeze(0)
                        if head_idx == 2 and shoot_mask is not None:
                            mask = torch.as_tensor(shoot_mask, dtype=torch.bool, device=head.device)
                            if mask.numel() == head.numel() and mask.any():
                                masked = head.clone()
                                masked[~mask] = -1e9
                                action_vals.append(int(masked.argmax().item()))
                                continue
                        action_vals.append(int(head.argmax().item()))
                    action_dict = to_action_dict(action_keys, tuple(action_vals))
                else:
                    state_tensor = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
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
            self._io.log(
                f"Ошибка игры: {exc}. Место: запуск GameController. "
                "Проверьте путь к модели и наличие файлов .pickle/.pth."
            )
            self._finished = True
