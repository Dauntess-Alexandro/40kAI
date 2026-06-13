# play warhammer!
import argparse
import collections

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

import os
import pickle
import sys
import warnings

from core.envs.warhamEnv import *

warnings.filterwarnings("ignore")

from core.engine.agent_registry import compatible_contracts, load_agent_by_id, make_env_contract
from core.engine.deployment import deploy_only_war, post_deploy_setup
from core.engine.game_controller import n_actions_from_env
from core.engine.game_io import ConsoleIO, set_active_io
from core.engine.mission import normalize_mission_name
from core.envs.warhamEnv import roll_off_attacker_defender
from core.models.alphazero_ids import az_mcts_mode_from_payload, is_alphazero_net_algo, is_gumbel_az_algo
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.alphazero_model import alphazero_arch_from_payload, load_alphazero_state_dict, make_alphazero_net
from core.models.DQN import *
from core.models.gumbel_alphazero_search import build_gumbel_inference_search
from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.gumbel_muzero_search import GumbelMuZeroSearch, GumbelMuZeroSearchConfig
from core.models.opponent_adapter import build_policy_fn, load_agent_opponent
from core.models.PPO import load_actor_critic_state_dict, make_actor_critic, ppo_arch_from_payload
from core.models.utils import (
    build_action_masks_by_head,
    build_shoot_action_mask,
    convertToDict,
    normalize_state_dict,
    select_action,
)
from eval import select_action_with_epsilon
from project_paths import ARTIFACTS_MODELS_DIR


def to_np_state(s):
    if isinstance(s, (dict, collections.OrderedDict)):
        return np.array(list(s.values()), dtype=np.float32)
    return np.array(s, dtype=np.float32)


def load_trusted_checkpoint(path: str):
    """Загрузка доверенного checkpoint для PyTorch>=2.6 (weights_only=False)."""
    return torch.load(path, weights_only=False)


PLAY_EPS = float(os.getenv("PLAY_EPS", "")) if os.getenv("PLAY_EPS") is not None and os.getenv("PLAY_EPS") != "" else None
PLAY_NO_EXPLORATION = os.getenv("PLAY_NO_EXPLORATION", "0") == "1"
if PLAY_NO_EXPLORATION:
    PLAY_EPS = 0.0
AZ_PLAY_MODE = str(os.getenv("AZ_PLAY_MODE", "greedy")).strip().lower() or "greedy"
if AZ_PLAY_MODE not in {"greedy", "mcts"}:
    AZ_PLAY_MODE = "greedy"
GMZ_PLAY_MODE = str(os.getenv("GMZ_PLAY_MODE", "greedy")).strip().lower() or "greedy"
if GMZ_PLAY_MODE not in {"greedy", "search"}:
    GMZ_PLAY_MODE = "greedy"
GAZ_PLAY_MODE = str(os.getenv("GAZ_PLAY_MODE", "greedy")).strip().lower() or "greedy"
if GAZ_PLAY_MODE not in {"greedy", "gumbel"}:
    GAZ_PLAY_MODE = "greedy"
GAZ_PLAY_SIMS = max(1, int(os.getenv("GAZ_PLAY_SIMS", "32")))
GAZ_PLAY_NUM_CONSIDERED = max(2, int(os.getenv("GAZ_PLAY_NUM_CONSIDERED", "8")))
GAZ_PLAY_TEMPERATURE = float(os.getenv("GAZ_PLAY_TEMPERATURE", "0.0"))
GAZ_JOINT_ACTION_INFER = str(os.getenv("GAZ_JOINT_ACTION", "0")).strip() == "1"

parser = argparse.ArgumentParser()
parser.add_argument("model", nargs="?", default="None")
parser.add_argument("play_in_gui", nargs="?", default="False")
parser.add_argument("--agent-id", default=os.getenv("PLAY_AGENT_ID", "").strip())
parser.add_argument("--opponent-agent-id", default=os.getenv("PLAY_OPPONENT_AGENT_ID", "").strip())
args = parser.parse_args()

if args.model == "None":
    savePath = str(ARTIFACTS_MODELS_DIR) + os.sep
    folders = os.listdir(savePath) if os.path.isdir(savePath) else []
    envs = []
    modelpth = []
    for i in folders:
        full_dir = os.path.join(savePath, i)
        if os.path.isdir(full_dir):
            fs = os.listdir(full_dir)
            for j in fs:
                full_path = os.path.join(full_dir, j)
                if j.endswith(".pickle"):
                    envs.append(full_path)
                elif j.endswith(".pth"):
                    modelpth.append(full_path)
    if not envs or not modelpth:
        raise FileNotFoundError("Не найдены legacy модели в artifacts/models/. Что делать: укажите --agent-id или путь к .pickle.")
    envs.sort(key=lambda x: os.path.getmtime(x))
    modelpth.sort()
    checkpoint = load_trusted_checkpoint(modelpth[-1])
    with open(envs[-1], "rb") as f:
        env, model, enemy = pickle.load(f)
else:
    with open(args.model, "rb") as f:
        env, model, enemy = pickle.load(f)
    modelpth = str(args.model)[:-len("pickle")] + "pth"
    checkpoint = load_trusted_checkpoint(modelpth)

playInGUI = str(args.play_in_gui).strip().lower() == "true"
opponent_agent_id = str(getattr(args, "opponent_agent_id", "") or "").strip()

io = ConsoleIO()
set_active_io(io)


def _log(msg: str):
    io.log(msg)


verbose = os.getenv("VERBOSE_LOGS", "0") == "1"
log_fn = _log if verbose else None

attacker_side, defender_side = roll_off_attacker_defender(
    manual_roll_allowed=(playInGUI is False),
    log_fn=_log,
)
if verbose:
    _log(f"[MISSION Only War] Attacker={attacker_side}, Defender={defender_side}")
    _log(f"[roster] model_units={len(model)} enemy_units={len(enemy)}")
    for idx, unit in enumerate(model):
        unit_data = unit.showUnitData()
        unit_name = unit_data.get("Name", "Unknown")
        unit_models = unit_data.get("#OfModels", 1)
        instance_id = getattr(unit, "instance_id", "unknown")
        _log(f"[roster] model[{idx}] name={unit_name} instance_id={instance_id} models={unit_models}")
    for idx, unit in enumerate(enemy):
        unit_data = unit.showUnitData()
        unit_name = unit_data.get("Name", "Unknown")
        unit_models = unit_data.get("#OfModels", 1)
        instance_id = getattr(unit, "instance_id", "unknown")
        _log(f"[roster] enemy[{idx}] name={unit_name} instance_id={instance_id} models={unit_models}")
_log(
    "Units: "
    + str(
        [
            (u.name, getattr(u, "instance_id", "unknown"), u.models_count)
            for u in model
        ]
    )
)

deploy_only_war(
    model_units=model,
    enemy_units=enemy,
    b_len=env.unwrapped.b_len,
    b_hei=env.unwrapped.b_hei,
    attacker_side=attacker_side,
    log_fn=log_fn,
)
post_deploy_setup(log_fn=log_fn)

env.attacker_side = attacker_side
env.defender_side = defender_side

state, info = env.reset(options={"m": model, "e": enemy})
if verbose:
    squads_for_actions_count = len(model)
    _log(f"[action_space] squads_for_actions_count={squads_for_actions_count}")
    for idx, unit in enumerate(model):
        unit_data = unit.showUnitData()
        unit_name = unit_data.get("Name", "Unknown")
        _log(f"[action_space] squad[{idx}] name={unit_name}")
    total_models_count = 0
    for unit in model:
        unit_data = unit.showUnitData()
        total_models_count += int(unit_data.get("#OfModels", 1))
    _log(f"[action_space] total_models_count={total_models_count}")
    move_num_keys = [
        key for key in env.action_space.spaces.keys() if key.startswith("move_num_")
    ]
    _log(f"[action_space] move_num_keys_count={len(move_num_keys)}")
    _log(f"[action_space] move_num_keys={sorted(move_num_keys)}")
n_actions = n_actions_from_env(env, len(model))
n_observations = len(state)
if args.agent_id:
    agent_payload = load_agent_by_id(args.agent_id)
    runtime_contract = make_env_contract(
        n_observations=n_observations,
        n_actions=n_actions,
        mission_name=str(getattr(env.unwrapped, "mission_name", "only_war")),
        ruleset_version=str(os.getenv("RULESET_VERSION", "only_war_v1")),
    )
    ok, reason = compatible_contracts(runtime_contract, agent_payload.get("contract", {}))
    if not ok:
        raise ValueError(
            f"Несовместимый --agent-id={args.agent_id}: {reason}. "
            "Что делать: выберите агента с тем же ruleset/action/obs контрактом."
        )
    checkpoint = {
        "policy_net": agent_payload.get("policy_state"),
        "target_net": agent_payload.get("target_state") or agent_payload.get("policy_state"),
        "optimizer": agent_payload.get("optimizer_state") or {},
        "net_type": "dueling" if any(str(k).startswith("value_heads.") for k in (agent_payload.get("policy_state") or {}).keys()) else "basic",
        "algo": str((agent_payload.get("meta") or {}).get("algo", "dqn")).strip().lower() or "dqn",
    }
    _log(f"[LEAGUE] Используется agent-id={args.agent_id} из registry.")

algo = str(checkpoint.get("algo", "dqn")).strip().lower() if isinstance(checkpoint, dict) else "dqn"
if algo not in {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero", "gumbel_az"}:
    algo = "dqn"
if is_gumbel_az_algo(algo):
    gaz_tail = f", temperature={GAZ_PLAY_TEMPERATURE:.3f}, sims={GAZ_PLAY_SIMS}" if GAZ_PLAY_MODE == "gumbel" else ""
    _log(f"[PLAY][INFERENCE_MODE] algo=gumbel_az mode={GAZ_PLAY_MODE} joint_action={int(GAZ_JOINT_ACTION_INFER)}{gaz_tail}")
elif is_alphazero_net_algo(algo):
    az_temp = float(os.getenv("AZ_PLAY_MCTS_TEMPERATURE", "0.06"))
    az_tail = f", temperature={az_temp:.3f}" if AZ_PLAY_MODE == "mcts" else ""
    _log(f"[PLAY][INFERENCE_MODE] algo={algo} mcts={az_mcts_mode_from_payload(algo, checkpoint if isinstance(checkpoint, dict) else None)} play_mode={AZ_PLAY_MODE}{az_tail}")
elif algo == "gumbel_muzero":
    gmz_temp = float(os.getenv("GMZ_PLAY_TEMPERATURE", "0.10"))
    gmz_tail = f", temperature={gmz_temp:.3f}" if GMZ_PLAY_MODE == "search" else ""
    _log(f"[PLAY][INFERENCE_MODE] algo=gumbel_muzero mode={GMZ_PLAY_MODE}{gmz_tail}")
else:
    _log(f"[PLAY][INFERENCE_MODE] algo={algo} mode=greedy(fixed)")
if algo == "ppo":
    ppo_state = checkpoint.get("actor_critic", checkpoint.get("policy_net", {}))
    arch = ppo_arch_from_payload(checkpoint if isinstance(checkpoint, dict) else None)
    policy_net = make_actor_critic(n_observations, n_actions, **arch).to(device)
    load_actor_critic_state_dict(policy_net, normalize_state_dict(ppo_state))
    policy_net.eval()
    target_net = None
elif is_alphazero_net_algo(algo):
    az_state = checkpoint.get("policy_value_net", checkpoint.get("policy_net", {}))
    arch = alphazero_arch_from_payload(checkpoint if isinstance(checkpoint, dict) else None)
    policy_net = make_alphazero_net(n_observations, n_actions, **arch).to(device)
    load_alphazero_state_dict(policy_net, normalize_state_dict(az_state))
    policy_net.eval()
    target_net = None
elif algo == "gumbel_muzero":
    gmz_state = checkpoint.get("gumbel_muzero_net", checkpoint.get("policy_net", {}))
    policy_net = GumbelMuZeroNet(
        obs_dim=int(n_observations),
        action_sizes=[int(x) for x in n_actions],
        latent_dim=int(os.getenv("GMZ_LATENT_DIM", "256")),
        hidden_dim=int(os.getenv("GMZ_HIDDEN_DIM", "256")),
        action_embed_dim=int(os.getenv("GMZ_ACTION_EMBED_DIM", "64")),
    ).to(device)
    policy_net.load_state_dict(normalize_state_dict(gmz_state))
    policy_net.eval()
    target_net = None
else:
    net_type = checkpoint.get("net_type") if isinstance(checkpoint, dict) else None
    dueling = net_type == "dueling"
    if not dueling and isinstance(checkpoint, dict):
        policy_state = checkpoint.get("policy_net", {})
        if any(key.startswith("value_heads.") for key in policy_state):
            dueling = True
    from core.models.DQN import make_dqn

    policy_net = make_dqn(n_observations, n_actions, dueling=dueling).to(device)
    target_net = make_dqn(n_observations, n_actions, dueling=dueling).to(device)
    optimizer = torch.optim.Adam(policy_net.parameters())
    policy_net.load_state_dict(normalize_state_dict(checkpoint['policy_net']))
    target_state = checkpoint.get("target_net") or checkpoint.get("target_model_state_dict")
    if isinstance(target_state, dict):
        target_net.load_state_dict(normalize_state_dict(target_state))
    else:
        target_net.load_state_dict(normalize_state_dict(policy_net.state_dict()))
    if isinstance(checkpoint.get("optimizer"), dict) and checkpoint["optimizer"]:
        optimizer.load_state_dict(checkpoint["optimizer"])
    policy_net.eval()
    target_net.eval()

def _model_source_path() -> str:
    if isinstance(modelpth, list):
        return str(modelpth[-1]) if modelpth else ""
    return str(modelpth or "")

_log(
    f"[VIEWER][MODEL] agent_id={str(args.agent_id or '-')} algo={algo} "
    f"source_checkpoint={_model_source_path() or '-'}"
)

isdone = False
i = 0

if playInGUI == True:
    env.reset(options={"m": model, "e": enemy, "playType": playInGUI, "Type": "big", "trunc": True})
else:
    env.reset(options={"m": model, "e": enemy, "playType": playInGUI, "Type": "big", "trunc": False})

env.io = io

reward = 0
io.log("\nИнструкции:\n")
io.log("Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.)")
io.log("Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.)\n")

while isdone == False:
    if opponent_agent_id:
        # AI vs AI (opponent agent controls enemyTurn; model controls step)
        done = False
        info = {}
        if i == 0:
            try:
                # Verify contract once and build policy_fn once (cached inside adapter closure).
                mission_name = normalize_mission_name(getattr(env.unwrapped, "mission_name", None))
                n_actions = n_actions_from_env(env, len(model))
                n_observations = len(to_np_state(state))
                play_contract = make_env_contract(
                    n_observations=n_observations,
                    n_actions=n_actions,
                    mission_name=mission_name,
                    ruleset_version=str(os.getenv("RULESET_VERSION", "only_war_v1")),
                )
                opp = load_agent_opponent(agent_id=opponent_agent_id, expected_contract=play_contract)
                opponent_policy_fn = build_policy_fn(env=env, len_model=len(enemy), opponent=opp, deterministic=True)
                _log(f"[PLAY] opponent-agent-id={opponent_agent_id} algo={opp.algo} (deterministic)")
                _log(
                    f"[VIEWER][OPPONENT] mode=ai agent_id={opponent_agent_id} "
                    f"algo={str(opp.algo).lower()} source=registry deterministic=1"
                )
            except Exception as exc:
                _log(f"[PLAY][WARN] opponent-agent-id invalid, fallback to human player. exc={exc}")
                opponent_agent_id = ""
                opponent_policy_fn = None
                _log("[VIEWER][OPPONENT] mode=human reason=invalid_opponent_agent_id")
        if opponent_agent_id and opponent_policy_fn is not None:
            env.unwrapped.enemyTurn(trunc=True, policy_fn=opponent_policy_fn)
            if bool(getattr(env.unwrapped, "game_over", False)):
                done = True
                info = env.unwrapped.get_info() if hasattr(env.unwrapped, "get_info") else {}
        else:
            done, info = env.unwrapped.player()
    else:
        if i == 0:
            _log("[VIEWER][OPPONENT] mode=human agent_id=- algo=manual_player")
        done, info = env.unwrapped.player()
    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    shoot_mask = build_shoot_action_mask(env)
    if algo == "ppo":
        masks = build_action_masks_by_head(env, len(model), log_fn=None, debug=False)
        masks_b = [m.to(state.device).unsqueeze(0) for m in masks]
        with torch.no_grad():
            deterministic = (PLAY_EPS is None) or float(PLAY_EPS) <= 0.0
            action, _, _ = policy_net.act(state, masks_by_head=masks_b, deterministic=deterministic)
        action = action.to("cpu")
    elif is_alphazero_net_algo(algo):
        masks = build_action_masks_by_head(env, len(model), log_fn=None, debug=False)
        if is_gumbel_az_algo(algo) and GAZ_PLAY_MODE == "gumbel":
            legal_masks = [m.detach().cpu().numpy().astype(bool) for m in masks]
            search = build_gumbel_inference_search(
                policy_net,
                num_simulations=GAZ_PLAY_SIMS,
                num_considered_actions=GAZ_PLAY_NUM_CONSIDERED,
                joint_action=GAZ_JOINT_ACTION_INFER,
                device=state.device,
            )
            _pi, selected, _value = search.run(
                obs=state.squeeze(0).detach().cpu().numpy(),
                legal_masks_by_head=legal_masks,
                temperature=GAZ_PLAY_TEMPERATURE,
                env=env,
                len_model=len(model),
                enemy_policy_fn=None,
            )
            action_list = [int(a) for a in selected]
        elif AZ_PLAY_MODE == "mcts" and not is_gumbel_az_algo(algo):
            legal_masks = [m.detach().cpu().numpy().astype(bool) for m in masks]
            az_mcts_mode = az_mcts_mode_from_payload(algo, checkpoint if isinstance(checkpoint, dict) else None)
            mcts = AlphaZeroFactorizedMCTS(
                policy_net,
                config=MCTSConfig(
                    simulations=max(1, int(os.getenv("AZ_PLAY_MCTS_SIMS", "32"))),
                    c_puct=float(os.getenv("AZ_PLAY_MCTS_C_PUCT", "1.5")),
                    dirichlet_alpha=float(os.getenv("AZ_PLAY_MCTS_DIR_ALPHA", "0.3")),
                    dirichlet_eps=float(os.getenv("AZ_PLAY_MCTS_DIR_EPS", "0.0")),
                    top_k_per_head=max(1, int(os.getenv("AZ_PLAY_MCTS_TOP_K_PER_HEAD", "8"))),
                    max_depth=max(1, int(os.getenv("AZ_PLAY_MCTS_MAX_DEPTH", "1"))),
                    mode=az_mcts_mode,
                ),
                device=state.device,
            )
            pi_targets, _selected, _value = mcts.run(
                obs=state.squeeze(0).detach().cpu().numpy(),
                legal_masks_by_head=legal_masks,
                temperature=float(os.getenv("AZ_PLAY_MCTS_TEMPERATURE", "0.06")),
                env=env,
                len_model=len(model),
                enemy_policy_fn=opponent_policy_fn if opponent_agent_id else None,
            )
            action_list = [int(torch.argmax(torch.tensor(pi)).item()) for pi in pi_targets]
        else:
            masks_b = [m.to(state.device).unsqueeze(0) for m in masks]
            with torch.no_grad():
                probs, _value = policy_net.infer(state, masks_by_head=masks_b)
            action_list = [int(torch.argmax(p.squeeze(0), dim=0).item()) for p in probs]
        action = torch.tensor([action_list], device="cpu")
    elif algo == "gumbel_muzero":
        masks = build_action_masks_by_head(env, len(model), log_fn=None, debug=False)
        if GMZ_PLAY_MODE == "search":
            legal_masks = [m.detach().cpu().numpy().astype(bool) for m in masks]
            search = GumbelMuZeroSearch(
                net=policy_net,
                config=GumbelMuZeroSearchConfig(
                    num_simulations=max(1, int(os.getenv("GMZ_PLAY_SIMS", "96"))),
                    root_top_k=max(1, int(os.getenv("GMZ_PLAY_ROOT_TOP_K", "16"))),
                    temperature=float(os.getenv("GMZ_PLAY_TEMPERATURE", "0.10")),
                ),
                device=state.device,
            )
            pi_targets, _behavior_logits, _selected, _value = search.run(
                obs=state.squeeze(0).detach().cpu().numpy(),
                legal_masks_by_head=legal_masks,
                deterministic=True,
            )
            action_list = [int(torch.argmax(torch.tensor(pi)).item()) for pi in pi_targets]
        else:
            masks_b = [m.to(state.device).unsqueeze(0) for m in masks]
            with torch.no_grad():
                probs, _value = policy_net.infer(state, masks_by_head=masks_b)
            action_list = [int(torch.argmax(p.squeeze(0), dim=0).item()) for p in probs]
        action = torch.tensor([action_list], device="cpu")
    elif PLAY_EPS is not None:
        action = select_action_with_epsilon(
            env,
            state,
            policy_net,
            PLAY_EPS,
            len(model),
            shoot_mask=shoot_mask,
        )
    else:
        action = select_action(env, state, i, policy_net, len(model), shoot_mask=shoot_mask)
    action_dict = convertToDict(action)
    if done != True:
        next_observation, reward, done, _, info = env.step(action_dict)
        reward = torch.tensor([reward], device=device)
        unit_health = info["model health"]
        enemy_health = info["player health"]
        inAttack = info["in attack"]

        board = env.render()
        message = f"Iteration {i} ended with reward {reward}, Player health {enemy_health}, Model health {unit_health}"
        io.log(message)
        next_state = torch.tensor(next_observation, dtype=torch.float32, device=device).unsqueeze(0)
        state = next_state
    if done == True:
        if reward > 0:
            io.log("Модель победила!")
        else:
            io.log("Вы победили!")
        isdone = True
    i+=1
