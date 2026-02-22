from enum import Enum


class AgentType(str, Enum):
    DQN = "dqn"
    ALPHAZERO = "alphazero"
