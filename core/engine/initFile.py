import json
import os
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from project_paths import CORE_DIR, TRAIN_DATA_PATH, UNITS_PATH, ensure_runtime_dirs


_UNIT_DATA_PATH = str(CORE_DIR / "engine" / "unitData.json")


def _load_runtime_data() -> dict:
    with open(str(TRAIN_DATA_PATH), encoding="utf-8") as j:
        return json.loads(j.read())

def makeFile(numIters, modelFaction, enemyFaction, modelUnits, enemyUnits, modelW, enemyW,
             modelCounts=None, enemyCounts=None, modelInstanceIds=None, enemyInstanceIds=None,
             boardx = 60, boardy = 40, mission="only_war"):
    if modelCounts is None:
        modelCounts = []
    if enemyCounts is None:
        enemyCounts = []
    if modelInstanceIds is None:
        modelInstanceIds = []
    if enemyInstanceIds is None:
        enemyInstanceIds = []

    data = {
        "Army1":modelFaction,
        "Army2":enemyFaction,
        "modelUnits":modelUnits,
        "enemyUnits":enemyUnits,
        "modelUnitCounts":modelCounts,
        "enemyUnitCounts":enemyCounts,
        "modelUnitInstanceIds": modelInstanceIds,
        "enemyUnitInstanceIds": enemyInstanceIds,
        "modelWeapons":modelW,
        "enemyWeapons":enemyW,
        "numLife": int(numIters),
        "x": int(boardx),
        "y": int(boardy),
        "mission": mission
    }

    ensure_runtime_dirs()
    with open(str(TRAIN_DATA_PATH), 'w', encoding="utf-8") as f:
        json.dump(data, f)
    
def addingUnits():
    model = []
    enemy = []
    model_counts = []
    enemy_counts = []
    model_instance_ids = []
    enemy_instance_ids = []
    file = open(str(UNITS_PATH), "r", encoding="utf-8")
    content = file.readlines()
    flip = 0
    for i in content[1:len(content)]:
        name = i[0:len(i)-1]
        if name == "Model Units":
            flip = 1
        elif flip == 0:
            unit_name, count, instance_id = _parse_unit_entry(name)
            if unit_name:
                enemy.append(unit_name)
                enemy_counts.append(count)
                enemy_instance_ids.append(instance_id)
        elif flip == 1:
            unit_name, count, instance_id = _parse_unit_entry(name)
            if unit_name:
                model.append(unit_name)
                model_counts.append(count)
                model_instance_ids.append(instance_id)

    return model, enemy, model_counts, enemy_counts, model_instance_ids, enemy_instance_ids

def _parse_unit_entry(value):
    if not value:
        return "", 0, ""
    if "|" not in value:
        return value, 0, ""
    parts = value.split("|")
    if len(parts) < 2:
        return value, 0, ""
    name_part = parts[0]
    count_part = parts[1]
    name = name_part.strip()
    count = 0
    try:
        count = int(count_part.strip())
    except ValueError:
        count = 0
    instance_id = ""
    if len(parts) >= 3:
        instance_id = parts[2].strip()
    return name, count, instance_id

def addingWeapons(m, e):

    with open(_UNIT_DATA_PATH, encoding="utf-8") as j:
        data = json.loads(j.read())

    model = []
    enemy = []

    for i in data["UnitData"]:
        for j in m:
            weaps = ["None", "None"]
            if i["Name"] == j:
                for k in i["Weapons"]:
                    for l in data["WeaponData"]:
                        if l["Name"][0:len(k)].lower() == k.lower():
                            if l["Type"] == "Ranged":
                                weaps[0] = l["Name"]
                            elif l["Type"] == "Melee":
                                weaps[1] = l["Name"]
                model.append(weaps)

        for j in e:
            weaps = ["None", "None"]
            if i["Name"] == j:
                for k in i["Weapons"]:
                    for l in data["WeaponData"]:
                        if l["Name"].lower() == k.lower():
                            if l["Type"] == "Ranged":
                                weaps[0] = l["Name"]
                            elif l["Type"] == "Melee":
                                weaps[1] = l["Name"]
                        elif l["Name"][0:len(k)].lower() == k.lower():
                            if l["Type"] == "Ranged":
                                weaps[0] = l["Name"]
                            elif l["Type"] == "Melee":
                                weaps[1] = l["Name"]
                enemy.append(weaps)
    
    return model, enemy

def getNumLife():

    data = _load_runtime_data()

    return data["numLife"]

def getModelFaction():
    data = _load_runtime_data()

    return data["Army1"]

def getEnemyFaction():
    data = _load_runtime_data()

    return data["Army2"]

def getBoardX():
    data = _load_runtime_data()

    return data["x"]

def getBoardY():
    data = _load_runtime_data()

    return data["y"]

def getModelUnits():
    data = _load_runtime_data()

    return data["modelUnits"]

def getEnemyUnits():
    data = _load_runtime_data()

    return data["enemyUnits"]

def getModelUnitCounts():
    data = _load_runtime_data()

    return data.get("modelUnitCounts", [])

def getEnemyUnitCounts():
    data = _load_runtime_data()

    return data.get("enemyUnitCounts", [])

def getModelUnitInstanceIds():
    data = _load_runtime_data()

    return data.get("modelUnitInstanceIds", [])

def getEnemyUnitInstanceIds():
    data = _load_runtime_data()

    return data.get("enemyUnitInstanceIds", [])

def getModelW():
    data = _load_runtime_data()

    return data["modelWeapons"]

def getEnemyW():
    data = _load_runtime_data()

    return data["enemyWeapons"]

def getMission():
    data = _load_runtime_data()

    return data.get("mission", "only_war")

def delFile():
    data_path = str(TRAIN_DATA_PATH)
    try:
        if os.path.isfile(data_path):
            os.remove(data_path)
    except OSError as exc:
        print(
            f"[ERROR] Не удалось удалить runtime/state/data.json: {exc}. "
            "Что делать: закройте приложения, которые держат файл, и попробуйте снова."
        )

if __name__ == "__main__":
    model, enemy, model_counts, enemy_counts, model_instance_ids, enemy_instance_ids = addingUnits()
    modelw, enemyw = addingWeapons(model, enemy)
    mission = sys.argv[6] if len(sys.argv) > 6 else "only_war"
    makeFile(sys.argv[1], sys.argv[2], sys.argv[3],model, enemy, modelw, enemyw,
             model_counts, enemy_counts, model_instance_ids, enemy_instance_ids, sys.argv[4], sys.argv[5], mission)
