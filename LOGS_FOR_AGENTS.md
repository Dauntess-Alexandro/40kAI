2026-02-06 11:53:54 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-02-06 11:53:54 | [VIEWER] Фоллбэк-рендер не активирован.
2026-02-06 11:53:54 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:53:54 | FX: старт GUI — пропускаю накопленные события модели, подхват с event_id=151.
2026-02-06 11:53:55 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-25-533289.pickle
2026-02-06 11:53:55 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-25-533289.pth
2026-02-06 11:53:59 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-02-06 11:53:59 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-02-06 11:53:59 | [DEPLOY] Order: model first, alternating
2026-02-06 11:53:59 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (51,6)
2026-02-06 11:53:59 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (20,34)
2026-02-06 11:53:59 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (58,2)
2026-02-06 11:53:59 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (13,34)
2026-02-06 11:53:59 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-02-06 11:53:59 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-02-06 11:53:59 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-02-06 11:53:59 | {'model health': [10, 10], 'player health': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-02-06 11:53:59 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-02-06 11:53:59 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:54:00 | === БОЕВОЙ РАУНД 1 ===
2026-02-06 11:54:00 | --- ХОД PLAYER ---
2026-02-06 11:54:00 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:54:00 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=0, VP: 0 -> 0, objectives=[1]
2026-02-06 11:54:00 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:54:00 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:54:00 | REQ: target selected Unit 11, confirm enabled
2026-02-06 11:54:00 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:54:00 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:54:00 | REQ: target selected Unit 11, confirm enabled
2026-02-06 11:54:02 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-02-06 11:54:02 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 11:54:02 | REQ: target selected Unit 12, confirm enabled
2026-02-06 11:54:02 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 11:54:02 | REQ: target selected Unit 12, confirm enabled
2026-02-06 11:54:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-06 11:54:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-06 11:54:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-06 11:54:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-06 11:54:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-06 11:54:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-06 11:54:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-06 11:54:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-06 11:54:04 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-06 11:54:04 | Reward (шаг): движение delta=-4.000
2026-02-06 11:54:04 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.152946437965905->13.152946437965905
2026-02-06 11:54:04 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:54:04 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:54:04 | Нет доступных целей для чарджа.
2026-02-06 11:54:04 | --- ФАЗА БОЯ ---
2026-02-06 11:54:04 | --- ХОД MODEL ---
2026-02-06 11:54:04 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:54:04 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:54:04 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0
2026-02-06 11:54:04 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:54:04 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:54:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-06 11:54:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-06 11:54:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-06 11:54:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-06 11:54:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (51, 6). Выбор: none, advance=нет, distance=0
2026-02-06 11:54:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (51, 6)
2026-02-06 11:54:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-06 11:54:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-06 11:54:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-06 11:54:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-06 11:54:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (58, 2). Выбор: none, advance=нет, distance=0
2026-02-06 11:54:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (58, 2)
2026-02-06 11:54:04 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-06 11:54:04 | Reward (шаг): движение delta=-4.000
2026-02-06 11:54:04 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:54:04 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:54:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-02-06 11:54:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-02-06 11:54:04 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:54:04 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:54:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-02-06 11:54:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-02-06 11:54:04 | [MODEL] Чардж: нет доступных целей
2026-02-06 11:54:04 | --- ФАЗА БОЯ ---
2026-02-06 11:54:04 | --- ФАЗА БОЯ ---
2026-02-06 11:54:04 | [MODEL] Ближний бой: нет доступных атак
2026-02-06 11:54:04 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.152946437965905->13.152946437965905
2026-02-06 11:54:04 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-02-06 11:54:04 | Итерация 0 завершена с наградой tensor([-4.0500], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-02-06 11:54:04 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-02-06 11:54:04 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-02-06 11:54:04 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:54:06 | === БОЕВОЙ РАУНД 2 ===
2026-02-06 11:54:06 | --- ХОД PLAYER ---
2026-02-06 11:54:06 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:54:06 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[1]
2026-02-06 11:54:06 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:54:06 | REQ: shooter changed Unit 12->Unit 11, target reset
2026-02-06 11:54:06 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:54:06 | REQ: target selected Unit 11, confirm enabled
2026-02-06 11:54:06 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:54:06 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:54:06 | REQ: target selected Unit 11, confirm enabled
2026-02-06 11:54:13 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-02-06 11:54:13 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 11:54:13 | REQ: target selected Unit 12, confirm enabled
2026-02-06 11:54:13 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 11:54:13 | REQ: target selected Unit 12, confirm enabled
2026-02-06 11:54:15 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-06 11:54:15 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.152946437965905->15.264337522473747
2026-02-06 11:54:15 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:54:15 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:54:15 | Нет доступных целей для чарджа.
2026-02-06 11:54:15 | --- ФАЗА БОЯ ---
2026-02-06 11:54:15 | --- ХОД MODEL ---
2026-02-06 11:54:15 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:54:15 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:54:15 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0
2026-02-06 11:54:15 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:54:15 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:54:15 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (51, 6). Выбор: right, advance=да, бросок=5, макс=10, distance=10
2026-02-06 11:54:15 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (51, 16)
2026-02-06 11:54:15 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-02-06 11:54:15 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (58, 2). Выбор: right, advance=да, бросок=2, макс=7, distance=7
2026-02-06 11:54:15 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (58, 9)
2026-02-06 11:54:15 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-02-06 11:54:15 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:54:15 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:54:15 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-02-06 11:54:15 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-02-06 11:54:15 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:54:15 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:54:15 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-02-06 11:54:15 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-02-06 11:54:15 | [MODEL] Чардж: нет доступных целей
2026-02-06 11:54:15 | --- ФАЗА БОЯ ---
2026-02-06 11:54:15 | --- ФАЗА БОЯ ---
2026-02-06 11:54:15 | [MODEL] Ближний бой: нет доступных атак
2026-02-06 11:54:15 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-06 11:54:15 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.152946437965905->15.264337522473747
2026-02-06 11:54:15 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-02-06 11:54:15 | Итерация 1 завершена с наградой tensor([-0.1000], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-02-06 11:54:15 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'modelCP': 4, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 1, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-02-06 11:54:15 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 4, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 1

2026-02-06 11:54:15 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:54:17 | === БОЕВОЙ РАУНД 3 ===
2026-02-06 11:54:17 | --- ХОД PLAYER ---
2026-02-06 11:54:17 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:54:17 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 1 -> 2, objectives=[1]
2026-02-06 11:54:17 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:54:17 | REQ: shooter changed Unit 12->Unit 11, target reset
2026-02-06 11:54:17 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:54:17 | REQ: target selected Unit 11, confirm enabled
2026-02-06 11:54:17 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:54:17 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:54:17 | REQ: target selected Unit 11, confirm enabled
