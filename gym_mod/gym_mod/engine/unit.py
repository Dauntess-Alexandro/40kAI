import os
import csv
import numpy as np
from gym_mod.engine.GUIinteract import *
import time

from gym_mod.engine.deployment import get_random_free_deploy_coord


class Unit:
    _instance_counter = 1

    def __init__(self, data, weapon, melee=None, b_len=0, b_hei=0, GUI=False, instance_id=None):
        self.unit_data = data
        self.unit_weapon = weapon
        self.unit_melee = melee
        self.b_len = int(b_len) if b_len else 0
        self.b_hei = int(b_hei) if b_hei else 0
        self.unit_coords = np.array([0, 0])
        self.playInGUI = GUI
        if instance_id:
            self.instance_id = str(instance_id)
        else:
            self.instance_id = f"unit-{Unit._instance_counter}"
            Unit._instance_counter += 1

    # --- FIX: подхватываем размеры поля из board.txt, если они нулевые ---
    def _ensure_board_dims(self):
        if self.b_len > 0 and self.b_hei > 0:
            return

        candidates = []

        # 1) board.txt в текущей папке запуска (часто это /home/dolbaeb/40kAI)
        candidates.append(os.path.join(os.getcwd(), "board.txt"))

        # 2) board.txt относительно расположения этого файла (на случай запуска из site-packages)
        # unit.py лежит в .../gym_mod/gym_mod/engine/unit.py
        # репо-root обычно на 4 уровня выше и там лежит board.txt
        candidates.append(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "board.txt"))
        )

        board_path = None
        for p in candidates:
            if os.path.exists(p):
                board_path = p
                break

        if not board_path:
            return

        with open(board_path, newline="") as f:
            rows = list(csv.reader(f))

        h = len(rows)
        w = len(rows[0]) if rows and rows[0] else 0

        if h > 0 and w > 0:
            self.b_hei = h
            self.b_len = w

    def updateUnitData(self, dicto):
        self.unit_weapon.update(dicto)

    def updateWeapon(self, dicto):
        self.unit_weapon.update(dicto)

    def updateMelee(self, dicto):
        self.unit_melee.update(dicto)

    def selectUnitPos(self, xmin, xmax, ymin, ymax):
        xmin, xmax, ymin, ymax = int(xmin), int(xmax), int(ymin), int(ymax)

        if self.playInGUI is False:
            coords = input("Enter the coordinates (example: 10,10): ")
        else:
            sendToGUI("Enter the coordinates (example: 10,10): ")
            coords = recieveGUI()

        run = True
        while run:
            if len(coords) == 0 or coords[0].isnumeric() is not True:
                if self.playInGUI is False:
                    coords = input("Use the format: x,y: ")
                else:
                    sendToGUI("Use the format: x,y: ")
                    coords = recieveGUI()
            else:
                x = ""
                y = ""
                switch = 0
                for i in range(len(coords)):
                    if coords[i].isnumeric() is not True:
                        switch = 1
                    elif switch == 0:
                        x += coords[i]
                    elif switch == 1:
                        y += coords[i]

                if x == "" or y == "":
                    if self.playInGUI is False:
                        coords = input("Use the format: x,y: ")
                    else:
                        sendToGUI("Use the format: x,y: ")
                        coords = recieveGUI()
                    continue

                xi = int(x)
                yi = int(y)

                if xi >= xmin and xi <= xmax and yi >= ymin and yi <= ymax:
                    run = False
                    self.unit_coords[0] = xi
                    self.unit_coords[1] = yi
                else:
                    if self.playInGUI is False:
                        coords = input("Not in bounds, try again: ")
                    else:
                        sendToGUI(
                            "Not in bounds (xmin: {}, xmax: {}, ymin: {}, ymax: {}), try again:".format(
                                xmin, xmax, ymin, ymax
                            )
                        )
                        coords = recieveGUI()

    def deployUnit(self, unitType, occupied=None):
        # --- FIX: убедимся, что размеры поля не нулевые ---
        self._ensure_board_dims()
        if self.b_hei <= 0 or self.b_len <= 0:
            raise RuntimeError(
                f"Board size is zero (b_hei={self.b_hei}, b_len={self.b_len}). "
                f"Не удалось прочитать board.txt или размеры не выставляются."
            )

        if occupied is None:
            occupied = set()
        coord = get_random_free_deploy_coord(unitType, self.b_len, self.b_hei, occupied)
        self.unit_coords = np.array([coord[0], coord[1]])
        occupied.add((coord[0], coord[1]))
        return coord

    def showUnitData(self):
        return self.unit_data

    def showWeapon(self):
        return self.unit_weapon

    def showMelee(self):
        return self.unit_melee

    def showCoords(self):
        return self.unit_coords

    @property
    def name(self):
        return self.unit_data.get("Name", "Unknown")

    @property
    def models_count(self):
        return int(self.unit_data.get("#OfModels", 1))
