import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self, n_observations, n_actions, dueling=False):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.dueling = dueling
        self.action_sizes = list(n_actions)
        if self.dueling:
            self.value_heads = nn.ModuleList(
                [nn.Linear(128, 1) for _ in self.action_sizes]
            )
            self.advantage_heads = nn.ModuleList(
                [nn.Linear(128, size) for size in self.action_sizes]
            )
        else:
            self.q_heads = nn.ModuleList(
                [nn.Linear(128, size) for size in self.action_sizes]
            )

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        outputs = []
        if self.dueling:
            for value_head, advantage_head in zip(self.value_heads, self.advantage_heads):
                value = value_head(x)
                advantage = advantage_head(x)
                q_values = value + (advantage - advantage.mean(dim=1, keepdim=True))
                outputs.append(q_values)
        else:
            for head in self.q_heads:
                outputs.append(head(x))
        return outputs
