import collections
import json
import math
import os
import random
from collections import namedtuple

import numpy as np
import torch
import torch.nn as nn

with open(os.path.abspath("hyperparams.json")) as j:
    data = json.loads(j.read())

EPS_START = data.get("eps_start", 0.9)
EPS_END = data.get("eps_end", 0.05)
EPS_DECAY = data.get("eps_decay", 1000)
BATCH_SIZE = data.get("batch_size", 2048)
GAMMA = data.get("gamma", 0.99)

Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))


def epsilon_by_step(step, eps_start=EPS_START, eps_end=EPS_END, eps_decay=EPS_DECAY, schedule="exp"):
    if schedule == "linear":
        if eps_decay <= 0:
            return eps_end
        slope = (eps_end - eps_start) / float(eps_decay)
        return max(eps_end, eps_start + slope * step)
    return eps_end + (eps_start - eps_end) * math.exp(-1.0 * step / float(eps_decay))


def select_action(env, state, epsilon, policy_net, len_model):
    sample = random.random()
    dev = next(policy_net.parameters()).device

    if isinstance(state, collections.OrderedDict):
        state = np.array(list(state.values()), dtype=np.float32)
    elif isinstance(state, np.ndarray):
        state = state.astype(np.float32, copy=False)

    if not torch.is_tensor(state):
        state = torch.tensor(state, dtype=torch.float32, device=dev)
    else:
        state = state.to(dev)

    if state.dim() == 1:
        state = state.unsqueeze(0)

    if sample > epsilon:
        with torch.no_grad():
            decision = policy_net(state)
            action_tensor = torch.stack([head.argmax(dim=1) for head in decision], dim=1)
            return action_tensor.to("cpu")

    sampled_action = env.action_space.sample()
    action_list = [
        sampled_action['move'],
        sampled_action['attack'],
        sampled_action['shoot'],
        sampled_action['charge'],
        sampled_action['use_cp'],
        sampled_action['cp_on'],
    ]
    for i in range(len_model):
        label = "move_num_" + str(i)
        action_list.append(sampled_action[label])
    return torch.tensor([action_list], dtype=torch.long, device="cpu")


def convertToDict(action):
    naction = action.numpy()[0]
    action_dict = {
        'move': int(naction[0]),
        'attack': int(naction[1]),
        'shoot': int(naction[2]),
        'charge': int(naction[3]),
        'use_cp': int(naction[4]),
        'cp_on': int(naction[5]),
    }
    for i in range(len(naction) - 6):
        label = "move_num_" + str(i)
        action_dict[label] = int(naction[i + 6])
    return action_dict


def optimize_model(
    policy_net,
    target_net,
    optimizer,
    memory,
    n_obs,
    batch_size=BATCH_SIZE,
    min_batch_size=64,
    gamma=GAMMA,
    per=False,
    per_beta=0.4,
    amp=False,
    scaler=None,
    grad_clip=10.0,
    double_dqn=True,
    debug=False,
):
    if len(memory) < min_batch_size:
        return None
    if len(memory) < batch_size:
        batch_size = len(memory)

    dev = next(policy_net.parameters()).device

    if per:
        transitions, indices, weights = memory.sample(batch_size, beta=per_beta)
        weights_t = torch.as_tensor(weights, device=dev, dtype=torch.float32).unsqueeze(1)
    else:
        transitions = memory.sample(batch_size)
        indices, weights_t = None, None

    batch = Transition(*zip(*transitions))

    desired_shape = (1, n_obs)

    state_tensors = []
    for s in batch.state:
        if s is None:
            state_tensors.append(torch.zeros(desired_shape, device=dev, dtype=torch.float32))
        else:
            state_tensors.append(torch.as_tensor(s, device=dev, dtype=torch.float32).view(desired_shape))
    state_batch = torch.cat(state_tensors, dim=0)

    action_batch = torch.as_tensor(np.stack(batch.action), device=dev, dtype=torch.long)
    reward_batch = torch.as_tensor(np.array(batch.reward, dtype=np.float32), device=dev).view(-1)

    non_final_mask = torch.tensor([s is not None for s in batch.next_state], device=dev, dtype=torch.bool)

    non_final_next_states = None
    if non_final_mask.any():
        non_final_next_states = torch.cat(
            [torch.as_tensor(s, device=dev, dtype=torch.float32).view(desired_shape) for s in batch.next_state if s is not None],
            dim=0,
        )

    def _gather_q(outputs, actions):
        move_action, attack_action, shoot_action, charge_action, use_cp_action, cp_on_action, *move_actions = outputs
        arr = [
            move_action.gather(1, actions[:, 0].unsqueeze(1)),
            attack_action.gather(1, actions[:, 1].unsqueeze(1)),
            shoot_action.gather(1, actions[:, 2].unsqueeze(1)),
            charge_action.gather(1, actions[:, 3].unsqueeze(1)),
            use_cp_action.gather(1, actions[:, 4].unsqueeze(1)),
            cp_on_action.gather(1, actions[:, 5].unsqueeze(1)),
        ]
        for i in range(len(move_actions)):
            arr.append(move_actions[i].gather(1, actions[:, i + 6].unsqueeze(1)))
        return torch.cat(arr, dim=1)

    use_amp = amp and dev.type == "cuda"
    autocast_ctx = torch.cuda.amp.autocast(enabled=use_amp)

    with autocast_ctx:
        state_action_values = policy_net(state_batch)
        selected_action_values = _gather_q(state_action_values, action_batch)

        next_state_values = torch.zeros((batch_size, selected_action_values.shape[1]), device=dev, dtype=torch.float32)
        with torch.no_grad():
            if non_final_next_states is not None:
                if double_dqn:
                    policy_next = policy_net(non_final_next_states)
                    next_actions = torch.stack([head.argmax(dim=1) for head in policy_next], dim=1)
                    target_next = target_net(non_final_next_states)
                    next_q = _gather_q(target_next, next_actions)
                else:
                    target_next = target_net(non_final_next_states)
                    max_per_head = [h.max(1).values for h in target_next]
                    next_q = torch.stack(max_per_head, dim=1)

                next_state_values[non_final_mask] = next_q

        expected_state_action_values = reward_batch.unsqueeze(1) + (gamma * next_state_values)

        if per:
            criterion = nn.SmoothL1Loss(reduction="none")
            loss_elem = criterion(selected_action_values, expected_state_action_values)
            loss = (loss_elem * weights_t).mean()
        else:
            criterion = nn.SmoothL1Loss()
            loss = criterion(selected_action_values, expected_state_action_values)

    if debug:
        assert torch.isfinite(loss).all(), "Loss is not finite"

    optimizer.zero_grad(set_to_none=True)
    grad_norm = None
    if use_amp and scaler is not None:
        scaler.scale(loss).backward()
        if grad_clip is not None:
            scaler.unscale_(optimizer)
            grad_norm = torch.nn.utils.clip_grad_norm_(policy_net.parameters(), grad_clip)
        scaler.step(optimizer)
        scaler.update()
    else:
        loss.backward()
        if grad_clip is not None:
            grad_norm = torch.nn.utils.clip_grad_norm_(policy_net.parameters(), grad_clip)
        optimizer.step()

    if per and indices is not None:
        with torch.no_grad():
            td_errors = (selected_action_values - expected_state_action_values).abs().mean(dim=1)
        memory.update_priorities(indices, td_errors.detach().cpu().numpy() + 1e-6)

    q_mean = selected_action_values.detach().mean()
    q_target_mean = expected_state_action_values.detach().mean()
    td_error_mean = (selected_action_values.detach() - expected_state_action_values.detach()).abs().mean()
    with torch.no_grad():
        param_norm = torch.norm(torch.stack([p.data.norm() for p in policy_net.parameters() if p is not None]))

    return {
        "loss": loss.detach(),
        "q_mean": q_mean,
        "q_target_mean": q_target_mean,
        "td_error_mean": td_error_mean,
        "grad_norm": grad_norm.detach() if grad_norm is not None else None,
        "param_norm": param_norm.detach(),
        "batch_size": batch_size,
    }
