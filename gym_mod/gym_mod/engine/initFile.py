import json
import os
import sys

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

    with open('gui/data.json', 'w') as f:
        json.dump(data, f)
    
def addingUnits():
    model = []
    enemy = []
    model_counts = []
    enemy_counts = []
    model_instance_ids = []
    enemy_instance_ids = []
    file = open("gui/units.txt", "r")
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

    with open(os.path.abspath("gym_mod/gym_mod/engine/unitData.json")) as j:
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

    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data["numLife"]

def getModelFaction():
    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data["Army1"]

def getEnemyFaction():
    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data["Army2"]

def getBoardX():
    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data["x"]

def getBoardY():
    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data["y"]

def getModelUnits():
    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data["modelUnits"]

def getEnemyUnits():
    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data["enemyUnits"]

def getModelUnitCounts():
    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data.get("modelUnitCounts", [])

def getEnemyUnitCounts():
    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data.get("enemyUnitCounts", [])

def getModelUnitInstanceIds():
    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data.get("modelUnitInstanceIds", [])

def getEnemyUnitInstanceIds():
    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data.get("enemyUnitInstanceIds", [])

def getModelW():
    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data["modelWeapons"]

def getEnemyW():
    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data["enemyWeapons"]

def getMission():
    with open(os.path.abspath("gui/data.json")) as j:
        data = json.loads(j.read())

    return data.get("mission", "only_war")

def delFile():
    data_path = os.path.abspath("gui/data.json")
    try:
        if os.path.isfile(data_path):
            os.remove(data_path)
    except OSError as exc:
        print(
            f"[ERROR] Не удалось удалить gui/data.json: {exc}. "
            "Что делать: закройте приложения, которые держат файл, и попробуйте снова."
        )

if __name__ == "__main__":
    model, enemy, model_counts, enemy_counts, model_instance_ids, enemy_instance_ids = addingUnits()
    modelw, enemyw = addingWeapons(model, enemy)
    mission = sys.argv[6] if len(sys.argv) > 6 else "only_war"
    makeFile(sys.argv[1], sys.argv[2], sys.argv[3],model, enemy, modelw, enemyw,
             model_counts, enemy_counts, model_instance_ids, enemy_instance_ids, sys.argv[4], sys.argv[5], mission)
