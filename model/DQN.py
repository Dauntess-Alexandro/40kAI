import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self, n_observations, n_actions, dueling=False):
        super(DQN, self).__init__()
        self.dueling = dueling
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        # layer3 for all actions
        self.move_head = nn.Linear(128, n_actions[0])
        self.attack_head = nn.Linear(128, n_actions[1])
        self.shoot_head = nn.Linear(128, n_actions[2])
        self.charge_head = nn.Linear(128, n_actions[3])
        self.use_cp = nn.Linear(128, n_actions[4])
        self.cp_on = nn.Linear(128, n_actions[5])
        self.move_len = nn.ModuleList()
        for i in range(len(n_actions) - 6):
            self.move_len.append(nn.Linear(128, n_actions[i + 6]))

        if self.dueling:
            self.move_value = nn.Linear(128, 1)
            self.attack_value = nn.Linear(128, 1)
            self.shoot_value = nn.Linear(128, 1)
            self.charge_value = nn.Linear(128, 1)
            self.use_cp_value = nn.Linear(128, 1)
            self.cp_on_value = nn.Linear(128, 1)
            self.move_len_value = nn.ModuleList()
            for _ in range(len(n_actions) - 6):
                self.move_len_value.append(nn.Linear(128, 1))

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        move_action = self.move_head(x)
        attack_action = self.attack_head(x)
        shoot_action = self.shoot_head(x)
        charge_action = self.charge_head(x)
        use_cp_action = self.use_cp(x)
        cp_on_action = self.cp_on(x)
        decs = [move_action, attack_action, shoot_action, charge_action, use_cp_action, cp_on_action]
        for i in range(len(self.move_len)):
            decs.append(self.move_len[i](x))

        if not self.dueling:
            return decs

        value_heads = [
            self.move_value(x),
            self.attack_value(x),
            self.shoot_value(x),
            self.charge_value(x),
            self.use_cp_value(x),
            self.cp_on_value(x),
        ]
        for i in range(len(self.move_len_value)):
            value_heads.append(self.move_len_value[i](x))

        out = []
        for adv, val in zip(decs, value_heads):
            adv_mean = adv.mean(dim=1, keepdim=True)
            out.append(val + (adv - adv_mean))
        return out
