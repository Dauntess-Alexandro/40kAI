import os
import csv
import numpy as np
from gym_mod.engine.GUIinteract import *
import time


class Unit:
    def __init__(self, data, weapon, melee=None, GUI=False, b_len=0, b_hei=0):
        self.unit_data = data
        self.unit_weapon = weapon
        self.unit_melee = melee
        self.b_len = int(b_len) if b_len else 0
        self.b_hei = int(b_hei) if b_hei else 0
        self.unit_coords = np.array([0, 0])
        self.playInGUI = GUI

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

    def deployUnit(self, deployment, unitType, GUI=False, choose=False):
        self.playInGUI = GUI

        # --- FIX: убедимся, что размеры поля не нулевые ---
        self._ensure_board_dims()
        if self.b_hei <= 0 or self.b_len <= 0:
            raise RuntimeError(
                f"Board size is zero (b_hei={self.b_hei}, b_len={self.b_len}). "
                f"Не удалось прочитать board.txt или размеры не выставляются."
            )

        if choose is True:
            run = True
            if self.playInGUI is False:
                contChoose = input("Would you like to choose where to deploy this unit? (y/n): ")
            else:
                sendToGUI("Would you like to choose where to deploy this unit? (y/n): ")
                contChoose = recieveGUI()
            while run:
                if contChoose.lower() in ("y", "yes"):
                    choose = True
                    run = False
                elif contChoose.lower() in ("n", "no"):
                    choose = False
                    run = False
                else:
                    if self.playInGUI is False:
                        contChoose = input("Valid answers are: y, yes, n, and no: ")
                    else:
                        sendToGUI("Valid answers are: y, yes, n, and no: ")
                        contChoose = recieveGUI()

        # Везде используем целочисленные границы и защиту от high<=low
        half_h = max(1, self.b_hei // 2)
        half_w = max(1, self.b_len // 2)
        quarter_h = max(1, self.b_hei // 4)
        quarter_w = max(1, self.b_len // 4)
        three_quarter_w = max(0, (self.b_len * 3) // 4)
        three_quarter_h = max(0, (self.b_hei * 3) // 4)

        if deployment == "Search and Destroy":
            if choose is False:
                if unitType == "model":
                    self.unit_coords[0] = np.random.randint(0, half_h)
                    self.unit_coords[1] = np.random.randint(0, half_w)
                elif unitType == "player":
                    x_low = self.b_hei // 2
                    x_high = max(x_low + 1, self.b_hei)
                    y_low = self.b_len // 2
                    y_high = max(y_low + 1, self.b_len)
                    self.unit_coords[0] = np.random.randint(x_low, x_high)
                    self.unit_coords[1] = np.random.randint(y_low, y_high)

            elif choose is True:
                if unitType == "player":
                    x_low = self.b_hei // 2
                    x_high = self.b_hei
                    y_low = self.b_len // 2
                    y_high = self.b_len
                    if self.playInGUI is False:
                        print(
                            "The bounds for x axis: {} to {}\nThe bounds for y axis: {} to {}".format(
                                x_low, x_high, y_low, y_high
                            )
                        )
                    else:
                        sendToGUI(
                            "The bounds for x axis: {} to {}\nThe bounds for y axis: {} to {}".format(
                                x_low, x_high, y_low, y_high
                            )
                        )
                    self.selectUnitPos(x_low, x_high, y_low, y_high)

        elif deployment == "Hammer and Anvil":
            if choose is False:
                if unitType == "model":
                    self.unit_coords[0] = np.random.randint(0, max(1, self.b_hei))
                    self.unit_coords[1] = np.random.randint(0, quarter_w)
                elif unitType == "player":
                    y_low = three_quarter_w
                    y_high = max(y_low + 1, self.b_len)
                    self.unit_coords[0] = np.random.randint(0, max(1, self.b_hei))
                    self.unit_coords[1] = np.random.randint(y_low, y_high)

            elif choose is True:
                if unitType == "player":
                    y_low = three_quarter_w
                    y_high = self.b_len
                    if self.playInGUI is False:
                        print(
                            "The bounds for x axis: {} to {}\nThe bounds for y axis: {} to {}".format(
                                0, self.b_hei, y_low, y_high
                            )
                        )
                    else:
                        sendToGUI(
                            "The bounds for x axis: {} to {}\nThe bounds for y axis: {} to {}".format(
                                0, self.b_hei, y_low, y_high
                            )
                        )
                    self.selectUnitPos(0, self.b_hei, y_low, y_high)

        elif deployment == "Dawn of War":
            if choose is False:
                if unitType == "model":
                    self.unit_coords[0] = np.random.randint(0, quarter_h)
                    self.unit_coords[1] = np.random.randint(0, max(1, self.b_len))
                elif unitType == "player":
                    x_low = three_quarter_h
                    x_high = max(x_low + 1, self.b_hei)
                    self.unit_coords[0] = np.random.randint(x_low, x_high)
                    self.unit_coords[1] = np.random.randint(0, max(1, self.b_len))

            elif choose is True:
                if unitType == "player":
                    x_low = three_quarter_h
                    x_high = self.b_hei
                    if self.playInGUI is False:
                        print(
                            "The bounds for x axis: {} to {}\nThe bounds for y axis: {} to {}".format(
                                x_low, x_high, 0, self.b_len
                            )
                        )
                    else:
                        sendToGUI(
                            "The bounds for x axis: {} to {}\nThe bounds for y axis: {} to {}".format(
                                x_low, x_high, 0, self.b_len
                            )
                        )
                    self.selectUnitPos(x_low, x_high, 0, self.b_len)

    def showUnitData(self):
        return self.unit_data

    def showWeapon(self):
        return self.unit_weapon

    def showMelee(self):
        return self.unit_melee

    def showCoords(self):
        return self.unit_coords

