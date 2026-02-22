from __future__ import annotations

import csv
import datetime
import json
import os
import pickle
from dataclasses import dataclass

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

from gym_mod.engine import Unit, initFile, unitData, weaponData
from gym_mod.engine.mission import board_dims_for_mission, normalize_mission_name

from model.alphazero import (
    AlphaZeroMCTS,
    AlphaZeroNet,
    MCTSNode,
    MCTSConfig,
    action_space_layout,
    flatten_observation,
    load_alphazero_checkpoint,
    sample_joint_actions,
    save_alphazero_checkpoint,
    safe_env_copy,
    to_action_dict,
)


DEFAULT_MISSION_NAME = "only_war"


def _load_roster_config():
    config = {
        "totLifeT": 10,
        "b_len": 40,
        "b_hei": 60,
        "mission": DEFAULT_MISSION_NAME,
        "enemy_faction": "Necrons",
        "model_faction": "Necrons",
        "enemy_units": [
            {
                "name": "Necron Warriors",
                "weapons": ("Gauss flayer", "Necron close combat weapon"),
                "count": None,
                "instance_id": None,
            },
            {
                "name": "Royal Warden",
                "weapons": ("Relic gauss blaster", "Royal warden close combat weapon"),
                "count": None,
                "instance_id": None,
            },
        ],
        "model_units": [
            {
                "name": "Necron Warriors",
                "weapons": ("Gauss flayer", "Necron close combat weapon"),
                "count": None,
                "instance_id": None,
            },
            {
                "name": "Royal Warden",
                "weapons": ("Relic gauss blaster", "Royal warden close combat weapon"),
                "count": None,
                "instance_id": None,
            },
        ],
    }

    if os.path.isfile("gui/data.json"):
        config["totLifeT"] = initFile.getNumLife()
        config["b_len"] = initFile.getBoardX()
        config["b_hei"] = initFile.getBoardY()
        config["enemy_faction"] = initFile.getEnemyFaction()
        config["model_faction"] = initFile.getModelFaction()
        config["mission"] = normalize_mission_name(getattr(initFile, "getMission", lambda: DEFAULT_MISSION_NAME)())

        enemy_counts = initFile.getEnemyUnitCounts()
        model_counts = initFile.getModelUnitCounts()
        enemy_instance_ids = initFile.getEnemyUnitInstanceIds()
        model_instance_ids = initFile.getModelUnitInstanceIds()

        enemy_units = []
        for i in range(len(initFile.getEnemyUnits())):
            count = enemy_counts[i] if i < len(enemy_counts) and enemy_counts[i] > 0 else None
            instance_id = enemy_instance_ids[i] if i < len(enemy_instance_ids) else None
            enemy_units.append(
                {
                    "name": initFile.getEnemyUnits()[i],
                    "weapons": (initFile.getEnemyW()[i][0], initFile.getEnemyW()[i][1]),
                    "count": count,
                    "instance_id": instance_id,
                }
            )

        model_units = []
        for i in range(len(initFile.getModelUnits())):
            count = model_counts[i] if i < len(model_counts) and model_counts[i] > 0 else None
            instance_id = model_instance_ids[i] if i < len(model_instance_ids) else None
            model_units.append(
                {
                    "name": initFile.getModelUnits()[i],
                    "weapons": (initFile.getModelW()[i][0], initFile.getModelW()[i][1]),
                    "count": count,
                    "instance_id": instance_id,
                }
            )

        config["enemy_units"] = enemy_units
        config["model_units"] = model_units

    config["mission"] = normalize_mission_name(config.get("mission", os.getenv("MISSION_NAME", DEFAULT_MISSION_NAME)))
    config["b_len"], config["b_hei"] = board_dims_for_mission(config["mission"])
    return config


def _build_units_from_config(config, b_len, b_hei):
    enemy = []
    model = []
    for spec in config["enemy_units"]:
        unit_data = unitData(config["enemy_faction"], spec["name"])
        if spec["count"]:
            unit_data["#OfModels"] = spec["count"]
        enemy.append(
            Unit(
                unit_data,
                weaponData(spec["weapons"][0]),
                weaponData(spec["weapons"][1]),
                b_len,
                b_hei,
                instance_id=spec["instance_id"],
            )
        )

    for spec in config["model_units"]:
        unit_data = unitData(config["model_faction"], spec["name"])
        if spec["count"]:
            unit_data["#OfModels"] = spec["count"]
        model.append(
            Unit(
                unit_data,
                weaponData(spec["weapons"][0]),
                weaponData(spec["weapons"][1]),
                b_len,
                b_hei,
                instance_id=spec["instance_id"],
            )
        )
    return enemy, model


@dataclass
class EpisodeRecord:
    reward: float
    length: int
    result: str


def _ensure_dirs() -> None:
    os.makedirs("models", exist_ok=True)
    os.makedirs("metrics", exist_ok=True)
    os.makedirs("gui/img", exist_ok=True)


def _plot_series(values: list[float], title: str, ylabel: str, path: str) -> None:
    plt.figure()
    plt.title(title)
    plt.xlabel("Episodes")
    plt.ylabel(ylabel)
    plt.plot(values)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def _write_metrics(run_id: str, losses: list[float], episodes: list[EpisodeRecord]) -> None:
    rewards = [e.reward for e in episodes]
    lengths = [e.length for e in episodes]
    win01 = [1 if e.result == "win" else 0 for e in episodes]
    vp = rewards

    _plot_series(rewards, "Avg. Reward per Episode", "Reward", f"metrics/reward_{run_id}.png")
    _plot_series(losses or [0.0], "Loss Curve", "Loss", f"metrics/loss_{run_id}.png")
    _plot_series(lengths, "Episode Length", "Len", f"metrics/epLen_{run_id}.png")
    _plot_series(win01, "Winrate", "Win", f"metrics/winrate_{run_id}.png")
    _plot_series(vp, "VP diff", "VP", f"metrics/vpdiff_{run_id}.png")
    _plot_series([0 for _ in episodes], "End Reasons", "Count", f"metrics/endreasons_{run_id}.png")

    for name in ["reward", "loss", "epLen", "winrate", "vpdiff", "endreasons"]:
        src = f"metrics/{name}_{run_id}.png"
        dst = f"gui/img/{name}_{run_id}.png"
        if os.path.exists(src):
            with open(src, "rb") as i, open(dst, "wb") as o:
                o.write(i.read())

    with open(f"models/alphazero_data_{run_id}.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "loss": f"img/loss_{run_id}.png",
                "reward": f"img/reward_{run_id}.png",
                "epLen": f"img/epLen_{run_id}.png",
                "winrate": f"img/winrate_{run_id}.png",
                "vpdiff": f"img/vpdiff_{run_id}.png",
                "endreasons": f"img/endreasons_{run_id}.png",
                "agent_type": "alphazero",
            },
            f,
        )

    with open(f"metrics/alphazero_stats_{run_id}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["episode", "reward", "length", "result"])
        for idx, ep in enumerate(episodes, 1):
            w.writerow([idx, ep.reward, ep.length, ep.result])



def _env_factory():
    import gymnasium as gym
    import gym_mod  # noqa: F401

    roster = _load_roster_config()
    enemy, model = _build_units_from_config(roster, roster["b_len"], roster["b_hei"])
    env = gym.make(
        "40kAI-v0",
        disable_env_checker=True,
        enemy=enemy,
        model=model,
        b_len=roster["b_len"],
        b_hei=roster["b_hei"],
    )
    env.reset(options={"m": model, "e": enemy, "Type": "small", "trunc": True})
    return env


def main() -> int:
    _ensure_dirs()
    num_episodes = int(os.getenv("AZ_NUM_EPISODES", "30"))
    simulations = int(os.getenv("AZ_MCTS_SIMS", "16"))
    max_steps = int(os.getenv("AZ_MAX_STEPS", "120"))
    lr = float(os.getenv("AZ_LR", "1e-3"))
    checkpoint = os.getenv("AZ_RESUME_CHECKPOINT", "").strip()

    env = _env_factory()
    obs, _ = env.reset()
    action_keys, action_sizes = action_space_layout(env.action_space)
    obs_dim = int(flatten_observation(obs).numel())

    if checkpoint:
        net, meta = load_alphazero_checkpoint(checkpoint)
        print(f"[ALPHAZERO] Резюмирую из {checkpoint}, epoch={meta['epoch']} step={meta['step']}")
    else:
        net = AlphaZeroNet(obs_dim, action_sizes)

    optimizer = torch.optim.Adam(net.parameters(), lr=lr)
    mcts = AlphaZeroMCTS(MCTSConfig(simulations=simulations, max_children=12))

    memories = []
    losses = []
    episodes: list[EpisodeRecord] = []
    total_steps = 0

    for ep in range(1, num_episodes + 1):
        obs, _ = env.reset()
        ep_reward = 0.0
        ep_len = 0
        history = []

        for _ in range(max_steps):
            root_obs = flatten_observation(obs)
            logits, root_value = net(root_obs)
            priors = sample_joint_actions(logits, max_children=12)

            def rollout(action_tuple):
                try:
                    sim_env = safe_env_copy(env)
                    nxt, rew, term, trunc, _ = sim_env.step(to_action_dict(action_keys, action_tuple))
                except Exception as exc:  # noqa: BLE001
                    print(
                        "[ALPHAZERO][WARN] Невалидное действие в MCTS: "
                        f"{action_tuple}. Где: train_alphazero.py/rollout. Что делать: проверьте маски целей. Детали: {exc}"
                    )
                    return -1.0, -1.0, [], True

                done = bool(term or trunc)
                nxt_logits, nxt_value = net(flatten_observation(nxt))
                nxt_priors = sample_joint_actions(nxt_logits, max_children=8) if not done else []
                return float(rew), float(nxt_value.item()), nxt_priors, done

            visits = mcts.search(root=MCTSNode(), action_priors=priors, rollout_fn=rollout)
            if not visits:
                print("[ALPHAZERO][WARN] MCTS не нашёл действий. Где: train_alphazero.py/main. Что делать: проверьте action space.")
                action_tuple = tuple(0 for _ in action_sizes)
                visit_sum = 1
                target_policy = torch.zeros(sum(action_sizes), dtype=torch.float32)
            else:
                action_tuple = max(visits.items(), key=lambda x: x[1])[0]
                visit_sum = sum(visits.values())
                target_policy = None

            action = to_action_dict(action_keys, action_tuple)
            nxt_obs, rew, term, trunc, info = env.step(action)
            done = bool(term or trunc)
            ep_reward += float(rew)
            ep_len += 1
            total_steps += 1

            if target_policy is None:
                target_heads = []
                for h, size in enumerate(action_sizes):
                    head_counts = torch.zeros(size, dtype=torch.float32)
                    for act, c in visits.items():
                        head_counts[act[h]] += c
                    target_heads.append(head_counts / max(1, visit_sum))
                history.append((root_obs, target_heads, float(root_value.item())))

            obs = nxt_obs
            if done:
                result = "win" if float(rew) > 0 else "loss"
                episodes.append(EpisodeRecord(ep_reward, ep_len, result))
                break

        if not history:
            continue

        total_loss = 0.0
        for state_tensor, policy_targets, pred_value in history:
            pred_logits, pred_val = net(state_tensor)
            p_loss = 0.0
            for h, head_logits in enumerate(pred_logits):
                log_prob = F.log_softmax(head_logits.squeeze(0), dim=-1)
                p_loss = p_loss - torch.sum(policy_targets[h] * log_prob)
            value_target = torch.tensor([max(-1.0, min(1.0, ep_reward / max(1, ep_len)))], dtype=torch.float32)
            v_loss = F.mse_loss(pred_val, value_target)
            loss = p_loss + v_loss
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += float(loss.item())

        avg_loss = total_loss / max(1, len(history))
        losses.append(avg_loss)
        print(f"[ALPHAZERO][TRAIN] ep={ep} loss={avg_loss:.4f} reward={ep_reward:.3f} len={ep_len}")

    run_id = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    ckpt = f"models/alphazero_model-{run_id}.pth"
    save_alphazero_checkpoint(ckpt, net, optimizer, epoch=num_episodes, step=total_steps)
    pickle_path = f"models/alphazero_model-{run_id}.pickle"
    with open(pickle_path, "wb") as f:
        pickle.dump({"agent_type": "alphazero", "checkpoint": ckpt}, f)

    _write_metrics(run_id, losses, episodes)
    print(f"[ALPHAZERO] Чекпойнт сохранён: {ckpt}")
    print("Generated metrics")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
