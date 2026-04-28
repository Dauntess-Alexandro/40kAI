import json
import os
from project_paths import CORE_DIR


_UNIT_DATA_PATH = str(CORE_DIR / "engine" / "unitData.json")

def unitData(army, unitName):
    with open(_UNIT_DATA_PATH, encoding="utf-8") as j:
        data = json.loads(j.read())
    for i in data["UnitData"]:
        if i["Army"].lower() == army.lower() and i["Name"].lower() == unitName.lower():
            return i
    print("Юнит не найден")
    return {}

def weaponData(name):
    if name == "None":
        return "None"
    with open(_UNIT_DATA_PATH, encoding="utf-8") as j:
        data = json.loads(j.read())
    for i in data["WeaponData"]:
        if i["Name"][0:len(name)].lower() == name.lower():
            return i
    print(name, "Оружие не найдено")
    return {}
