from core.engine.unit import Unit
from core.envs.warhamEnv import Warhammer40kEnv


def make_unit(name: str, movement: int = 6, models: int = 3, wounds: int = 2, rng: int = 24) -> Unit:
    data = {
        "Name": name,
        "Movement": movement,
        "M": movement,
        "W": wounds,
        "#OfModels": models,
        "OC": 1,
        "Ld": 7,
        "T": 4,
        "Sv": 3,
    }
    weapon = {
        "Name": "Stub gun",
        "Type": "Ranged",
        "Range": rng,
        "A": 1,
        "BS": 4,
        "S": 4,
        "AP": 0,
        "Damage": 1,
    }
    melee = {
        "Name": "Stub blade",
        "Type": "Melee",
        "Range": 2,
        "A": 1,
        "WS": 4,
        "S": 4,
        "AP": 0,
        "Damage": 1,
    }
    return Unit(data=data, weapon=weapon, melee=melee, b_len=30, b_hei=30, GUI=False)


def build_env(b_len: int = 30, b_hei: int = 30) -> Warhammer40kEnv:
    model = [make_unit("ModelA"), make_unit("ModelB")]
    enemy = [make_unit("EnemyA"), make_unit("EnemyB")]
    return Warhammer40kEnv(enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
