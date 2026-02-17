import os
import csv
import numpy as np
from gym_mod.engine.game_io import get_active_io

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
        self.anchor_coords = self.unit_coords
        self.unit_models = []
        self._init_unit_models()
        self.playInGUI = GUI
        if instance_id:
            self.instance_id = str(instance_id)
        else:
            self.instance_id = f"unit-{Unit._instance_counter}"
            Unit._instance_counter += 1

    def _safe_int(self, value, fallback=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return fallback

    def _model_wounds(self):
        return max(1, self._safe_int(self.unit_data.get("W"), fallback=1))

    def _init_unit_models(self):
        """
        Создаём внутреннее состояние моделей юнита.
        Пока это инфраструктура для миграции: внешний геймплей остаётся прежним.
        """
        count = max(1, self._safe_int(self.unit_data.get("#OfModels"), fallback=1))
        wounds = self._model_wounds()
        self.unit_models = [
            {
                "id": i,
                "coords": [int(self.unit_coords[0]), int(self.unit_coords[1]), 0],
                "wounds_current": wounds,
                "wounds_max": wounds,
                "alive": True,
            }
            for i in range(count)
        ]

    def _sync_models_to_anchor(self):
        """Для PR1 все модели сидят на якоре (юнит пока двигается как одна точка)."""
        x = int(self.unit_coords[0])
        y = int(self.unit_coords[1])
        for model in self.unit_models:
            if model.get("alive", True):
                model["coords"][0] = x
                model["coords"][1] = y

    def set_anchor(self, x, y):
        self.unit_coords[0] = int(x)
        self.unit_coords[1] = int(y)
        self._sync_models_to_anchor()

    def models(self):
        return self.unit_models

    def alive_models_count(self):
        return sum(1 for model in self.unit_models if model.get("alive", True))

    def total_hp(self):
        return int(sum(max(0, self._safe_int(model.get("wounds_current"), fallback=0)) for model in self.unit_models if model.get("alive", True)))

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
        io = get_active_io()

        run = True
        while run:
            xi = io.request_int("Введите координату X: ", min_value=xmin, max_value=xmax)
            yi = io.request_int("Введите координату Y: ", min_value=ymin, max_value=ymax)
            if xi is None or yi is None:
                io.log("Нужны корректные координаты в пределах поля.")
                continue
            if xmin <= xi <= xmax and ymin <= yi <= ymax:
                run = False
                self.set_anchor(xi, yi)
            else:
                io.log(
                    "Координаты вне поля (xmin: {}, xmax: {}, ymin: {}, ymax: {}). Повторите ввод.".format(
                        xmin, xmax, ymin, ymax
                    )
                )

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
        self.anchor_coords = self.unit_coords
        self._sync_models_to_anchor()
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
