2026-02-02 | [AGENT] Найдено: кнопка «Играть в GUI» запускает scripts/viewer.* -> `python -m viewer`. Viewer написан на PySide6 (Qt Widgets) и ранее использовал QGraphicsView/QGraphicsScene. Обновляем рендер в сторону QOpenGLWidget.
2026-02-02 16:50:35 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-02-02 16:50:35 | [VIEWER] Фоллбэк-рендер не активирован.
2026-02-02 16:50:36 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-8-957504.pickle
2026-02-02 16:50:36 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-8-957504.pth
2026-02-02 16:50:51 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-02-02 16:50:51 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-02-02 16:50:51 | [DEPLOY] Order: model first, alternating
2026-02-02 16:50:51 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (35,8)
2026-02-02 16:50:51 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (58,34)
2026-02-02 16:50:51 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (57,9)
2026-02-02 16:50:51 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (54,33)
2026-02-02 16:50:51 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-02-02 16:50:51 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-02-02 16:50:51 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-02-02 16:50:51 | {'model health': [10, 10], 'player health': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-02-02 16:50:51 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-02-02 16:50:55 | === БОЕВОЙ РАУНД 1 ===
2026-02-02 16:50:55 | --- ХОД PLAYER ---
2026-02-02 16:50:55 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-02 16:50:55 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0
2026-02-02 16:50:55 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-02 16:51:01 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-02 16:51:01 | Выбрано на карте: unit_id=11, name=Necron Warriors
2026-02-02 16:51:02 | Выбрано в таблице: row=1 -> unit_id=22
2026-02-02 16:51:03 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-02 16:51:04 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-02 16:51:04 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-02 16:51:05 | Выбрано в таблице: row=0 -> unit_id=21
2026-02-02 16:51:05 | Выбрано в таблице: row=1 -> unit_id=22
2026-02-02 16:51:07 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-02 16:51:35 | Бросок 1D6 на Advance...
