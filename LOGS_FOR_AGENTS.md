2026-02-06 11:33:38 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-02-06 11:33:38 | [VIEWER] Фоллбэк-рендер не активирован.
2026-02-06 11:33:38 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:33:38 | FX: старт GUI — пропускаю накопленные события модели, подхват с event_id=54.
2026-02-06 11:33:39 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-25-533289.pickle
2026-02-06 11:33:39 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-25-533289.pth
2026-02-06 11:33:45 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-02-06 11:33:45 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-02-06 11:33:45 | [DEPLOY] Order: model first, alternating
2026-02-06 11:33:45 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (52,3)
2026-02-06 11:33:45 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (15,34)
2026-02-06 11:33:45 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (27,8)
2026-02-06 11:33:45 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (15,30)
2026-02-06 11:33:45 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-02-06 11:33:45 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-02-06 11:33:45 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-02-06 11:33:45 | {'model health': [10, 10], 'player health': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-02-06 11:33:45 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-02-06 11:33:45 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:33:46 | === БОЕВОЙ РАУНД 1 ===
2026-02-06 11:33:46 | --- ХОД PLAYER ---
2026-02-06 11:33:46 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:33:46 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0
2026-02-06 11:33:46 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:33:46 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:33:46 | REQ: target selected Unit 11, confirm enabled
2026-02-06 11:33:46 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:33:46 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:33:46 | REQ: target selected Unit 11, confirm enabled
2026-02-06 11:33:48 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-02-06 11:33:48 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 11:33:48 | REQ: target selected Unit 12, confirm enabled
2026-02-06 11:33:48 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 11:33:48 | REQ: target selected Unit 12, confirm enabled
2026-02-06 11:33:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-06 11:33:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-06 11:33:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-06 11:33:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-06 11:33:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-06 11:33:50 | Reward (шаг): движение delta=-2.500
2026-02-06 11:33:50 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:33:50 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:33:50 | Нет доступных целей для чарджа.
2026-02-06 11:33:50 | --- ФАЗА БОЯ ---
2026-02-06 11:33:50 | --- ХОД MODEL ---
2026-02-06 11:33:50 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:33:50 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:33:50 | [MODEL] Only War: end of Command phase -> controlled=1, gained=0, VP: 0 -> 0, objectives=[3]
2026-02-06 11:33:50 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:33:50 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:33:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-06 11:33:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-06 11:33:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-06 11:33:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-06 11:33:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (52, 3). Выбор: none, advance=нет, distance=0
2026-02-06 11:33:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (52, 3)
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (27, 8). Выбор: none, advance=нет, distance=0
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (27, 8)
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-06 11:33:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-06 11:33:50 | Reward (шаг): движение delta=-2.500
2026-02-06 11:33:50 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:33:50 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:33:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-02-06 11:33:50 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:33:50 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:33:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-02-06 11:33:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-02-06 11:33:50 | [MODEL] Чардж: нет доступных целей
2026-02-06 11:33:50 | --- ФАЗА БОЯ ---
2026-02-06 11:33:50 | --- ФАЗА БОЯ ---
2026-02-06 11:33:50 | [MODEL] Ближний бой: нет доступных атак
2026-02-06 11:33:50 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-02-06 11:33:50 | Итерация 0 завершена с наградой tensor([-2.5000], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-02-06 11:33:50 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-02-06 11:33:50 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-02-06 11:33:50 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:33:52 | === БОЕВОЙ РАУНД 2 ===
2026-02-06 11:33:52 | --- ХОД PLAYER ---
2026-02-06 11:33:52 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:33:52 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0
2026-02-06 11:33:52 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:33:52 | REQ: shooter changed Unit 12->Unit 11, target reset
2026-02-06 11:33:52 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:33:52 | REQ: target selected Unit 11, confirm enabled
2026-02-06 11:33:52 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:33:52 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:33:52 | REQ: target selected Unit 11, confirm enabled
2026-02-06 11:33:54 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-02-06 11:33:54 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 11:33:54 | REQ: target selected Unit 12, confirm enabled
2026-02-06 11:33:54 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 11:33:54 | REQ: target selected Unit 12, confirm enabled
2026-02-06 11:33:55 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:33:55 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:33:55 | Нет доступных целей для чарджа.
2026-02-06 11:33:55 | --- ФАЗА БОЯ ---
2026-02-06 11:33:55 | --- ХОД MODEL ---
2026-02-06 11:33:55 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:33:55 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:33:55 | [MODEL] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[3]
2026-02-06 11:33:55 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:33:55 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:33:55 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (52, 3). Выбор: up, advance=да, бросок=6, макс=11, distance=6
2026-02-06 11:33:55 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (46, 3)
2026-02-06 11:33:55 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-02-06 11:33:55 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (27, 8). Выбор: up, advance=нет, distance=3
2026-02-06 11:33:55 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (24, 8)
2026-02-06 11:33:55 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-02-06 11:33:55 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:33:55 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 11:33:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-06 11:33:57 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-06 11:33:57 | Reward (шаг): движение delta=+0.500
2026-02-06 11:33:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-06 11:33:57 | Reward (шаг): стрельба delta=-0.650
2026-02-06 11:33:57 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-06 11:33:57 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-06 11:33:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-06 11:33:57 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-06 11:33:57 | Reward (шаг): движение delta=+0.500
2026-02-06 11:33:57 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:33:57 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:33:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-02-06 11:33:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана недоступная цель (raw=1). Стрельба пропущена.
2026-02-06 11:33:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-06 11:33:57 | [MODEL][SHOOT] Невалидный выбор цели: raw=1, доступные=[1] (ожидался индекс 0..0). Стрельба пропущена.
2026-02-06 11:33:57 | Reward (шаг): стрельба delta=-0.650
2026-02-06 11:33:57 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:33:57 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:33:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-02-06 11:33:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-02-06 11:33:57 | [MODEL] Чардж: нет доступных целей
2026-02-06 11:33:57 | --- ФАЗА БОЯ ---
2026-02-06 11:33:57 | --- ФАЗА БОЯ ---
2026-02-06 11:33:57 | [MODEL] Ближний бой: нет доступных атак
2026-02-06 11:33:57 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-06 11:33:57 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-06 11:33:57 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-02-06 11:33:57 | Итерация 1 завершена с наградой tensor([0.1000], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-02-06 11:33:57 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'modelCP': 4, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 1, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-02-06 11:33:57 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 4, CP PLAYER: 4
VP MODEL: 1, VP PLAYER: 0

2026-02-06 11:33:57 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:33:57 | FX: buffer phase command (model)
2026-02-06 11:33:57 | FX: enqueue phase script command: units=0
2026-02-06 11:33:57 | FX: show summary command VP=1, CP=4
2026-02-06 11:33:57 | FX: wait_continue reason=phase_done next=ФАЗА ДВИЖЕНИЯ
2026-02-06 11:33:57 | FX: buffer phase movement (model)
2026-02-06 11:33:57 | FX: enqueue phase script movement: units=2
2026-02-06 11:33:57 | FX: buffer phase shooting (model)
2026-02-06 11:33:57 | FX: enqueue phase script shooting: units=2
2026-02-06 11:33:57 | FX: buffer phase charge (model)
2026-02-06 11:33:57 | FX: enqueue phase script charge: units=2
2026-02-06 11:33:57 | FX: buffer phase fight (model)
2026-02-06 11:33:57 | FX: enqueue phase script fight: units=2
2026-02-06 11:34:01 | FX: continue=Y
2026-02-06 11:34:01 | FX: show summary movement двигались 2/2, advance=1, dist=9.0
2026-02-06 11:34:01 | Выбрано в таблице: row=0 -> unit_id=21
2026-02-06 11:34:01 | FX: move apply event_id=65 unit_id=21 side=model action=move from=[52, 3] types=('int', 'int') to=[46, 3] types=('int', 'int') key=('model', 21) render_found=1
2026-02-06 11:34:01 | FX: move write unit_id=21 side=model grid=(46,3) before=(52, 3) after=(46,3) cell_size=18 conversion=grid->world(cell_size)
2026-02-06 11:34:01 | FX: play unit_action unit=21 action=move
2026-02-06 11:34:01 | FX: wait_continue reason=unit_done next=Unit 22 — Necron Warriors (🚶 Движение: [27, 8] → [24, 8], dist=3.0, advance=нет)
2026-02-06 11:34:02 | FX: continue=Y
2026-02-06 11:34:02 | Выбрано в таблице: row=1 -> unit_id=22
2026-02-06 11:34:02 | FX: move apply event_id=70 unit_id=22 side=model action=move from=[27, 8] types=('int', 'int') to=[24, 8] types=('int', 'int') key=('model', 22) render_found=1
2026-02-06 11:34:02 | FX: move write unit_id=22 side=model grid=(24,8) before=(27, 8) after=(24,8) cell_size=18 conversion=grid->world(cell_size)
2026-02-06 11:34:02 | FX: play unit_action unit=22 action=move
2026-02-06 11:34:02 | FX: wait_continue reason=unit_done next=unit
2026-02-06 11:34:02 | FX: continue=Y
2026-02-06 11:34:02 | FX: wait_continue reason=phase_done next=ФАЗА СТРЕЛЬБЫ
2026-02-06 11:34:03 | FX: continue=Y
2026-02-06 11:34:03 | FX: show summary shooting shots=0, skipped=2 (reasons: advanced_no_assault=1, invalid_target=1)
2026-02-06 11:34:03 | Выбрано в таблице: row=0 -> unit_id=21
2026-02-06 11:34:03 | FX: play unit_action unit=21 action=skip_shoot
2026-02-06 11:34:03 | FX: wait_continue reason=unit_done next=Unit 22 — Necron Warriors (⏭️ Skip shoot (invalid_target))
2026-02-06 11:34:03 | FX: continue=Y
2026-02-06 11:34:03 | Выбрано в таблице: row=1 -> unit_id=22
2026-02-06 11:34:03 | FX: play unit_action unit=22 action=skip_shoot
2026-02-06 11:34:03 | FX: wait_continue reason=unit_done next=unit
2026-02-06 11:34:03 | FX: continue=Y
2026-02-06 11:34:03 | FX: wait_continue reason=phase_done next=ФАЗА ЧАРДЖА
2026-02-06 11:34:04 | FX: continue=Y
2026-02-06 11:34:04 | FX: show summary charge charges=0, skipped=2 (reasons: advanced_no_charge=1, no_targets=1)
2026-02-06 11:34:04 | Выбрано в таблице: row=0 -> unit_id=21
2026-02-06 11:34:04 | FX: play unit_action unit=21 action=skip_charge
2026-02-06 11:34:04 | FX: wait_continue reason=unit_done next=Unit 22 — Necron Warriors (⏭️ Skip charge (no_targets))
2026-02-06 11:34:04 | FX: continue=Y
2026-02-06 11:34:04 | Выбрано в таблице: row=1 -> unit_id=22
2026-02-06 11:34:04 | FX: play unit_action unit=22 action=skip_charge
2026-02-06 11:34:04 | FX: wait_continue reason=unit_done next=unit
2026-02-06 11:34:04 | FX: continue=Y
2026-02-06 11:34:04 | FX: wait_continue reason=phase_done next=ФАЗА БОЯ
2026-02-06 11:34:05 | FX: continue=Y
2026-02-06 11:34:05 | FX: show summary fight fights=0, skipped=2 (reasons: no_attacks=2)
2026-02-06 11:34:05 | Выбрано в таблице: row=0 -> unit_id=21
2026-02-06 11:34:05 | FX: play unit_action unit=21 action=skip_fight
2026-02-06 11:34:05 | FX: wait_continue reason=unit_done next=Unit 22 — Necron Warriors (⏭️ Skip fight (no_attacks))
2026-02-06 11:34:05 | FX: continue=Y
2026-02-06 11:34:05 | Выбрано в таблице: row=1 -> unit_id=22
2026-02-06 11:34:05 | FX: play unit_action unit=22 action=skip_fight
2026-02-06 11:34:05 | FX: wait_continue reason=unit_done next=unit
2026-02-06 11:34:05 | FX: continue=Y
2026-02-06 11:34:05 | FX: wait_continue reason=phase_done next=ФАЗА БОЯ
2026-02-06 11:34:05 | FX: continue=Y
2026-02-06 11:34:06 | === БОЕВОЙ РАУНД 3 ===
2026-02-06 11:34:06 | --- ХОД PLAYER ---
2026-02-06 11:34:06 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:34:06 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0
2026-02-06 11:34:06 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:34:06 | REQ: shooter changed Unit 12->Unit 11, target reset
2026-02-06 11:34:06 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:34:06 | REQ: target selected Unit 11, confirm enabled
2026-02-06 11:34:06 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:34:06 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:34:06 | REQ: target selected Unit 11, confirm enabled
2026-02-06 11:34:08 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-02-06 11:34:08 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 11:34:08 | REQ: target selected Unit 12, confirm enabled
2026-02-06 11:34:08 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 11:34:08 | REQ: target selected Unit 12, confirm enabled
2026-02-06 11:34:10 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:34:10 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 11:34:10 | REQ: target selected Unit 12, confirm enabled
2026-02-06 11:34:11 | 
🎲 Бросок на попадание (to hit): 10D6
2026-02-06 11:34:15 | 
🎲 Бросок на ранение (to wound): 10D6
2026-02-06 11:34:21 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-02-06 11:34:21 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-02-06 11:34:21 | FX: старт отчёта (shooting), ts=no-ts.
2026-02-06 11:34:21 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-02-06 11:34:21 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-02-06 11:34:21 | Оружие: Gauss flayer
2026-02-06 11:34:21 | FX: найдена строка оружия: Gauss flayer.
2026-02-06 11:34:21 | BS оружия: 4+
2026-02-06 11:34:21 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-02-06 11:34:21 | Save цели: 4+ (invul: нет)
2026-02-06 11:34:21 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-02-06 11:34:21 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-02-06 11:34:21 | Hit rolls:    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]  -> hits: 10
2026-02-06 11:34:21 | Wound rolls:  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  (цель 4+) -> wounds: 0
2026-02-06 11:34:21 | 
✅ Итог по движку: прошло урона = 0.0
2026-02-06 11:34:21 | FX: найден итог урона = 0.0.
2026-02-06 11:34:21 | FX: создан FxShotEvent (attacker=12, target=22, weapon=Gauss flayer, damage=0.0).
2026-02-06 11:34:21 | FX: shot grid attacker=(15,30) target=(24,8) cell_size=18
2026-02-06 11:34:21 | FX: позиция эффекта start=(279.0,549.0) end=(441.0,153.0).
2026-02-06 11:34:21 | FX: эффект добавлен в рендер (attacker=12, target=22).
2026-02-06 11:34:21 | 📌 -------------------------

2026-02-06 11:34:21 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:34:21 | Нет доступных целей для чарджа.
2026-02-06 11:34:21 | --- ФАЗА БОЯ ---
2026-02-06 11:34:21 | --- ХОД MODEL ---
2026-02-06 11:34:21 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:34:21 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 11:34:21 | [MODEL] Only War: end of Command phase -> controlled=1, gained=1, VP: 1 -> 2, objectives=[3]
2026-02-06 11:34:21 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:34:21 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 11:34:21 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (46, 3). Выбор: right, advance=да, бросок=6, макс=11, distance=10
2026-02-06 11:34:21 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (46, 13)
2026-02-06 11:34:21 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-02-06 11:34:21 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (24, 8). Выбор: right, advance=да, бросок=3, макс=8, distance=8
2026-02-06 11:34:21 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (24, 16)
2026-02-06 11:34:21 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-02-06 11:34:21 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:34:21 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:34:21 | FX: старт отчёта (shooting), ts=no-ts.
2026-02-06 11:34:21 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-02-06 11:34:21 | FX: найдена строка оружия: Gauss flayer.
2026-02-06 11:34:21 | FX: найден итог урона = 0.0.
2026-02-06 11:34:21 | FX: дубликат отчёта, эффект не создаём.
2026-02-06 11:34:21 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 11:34:22 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-06 11:34:22 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:34:22 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 11:34:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-02-06 11:34:22 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-02-06 11:34:22 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:34:22 | --- ФАЗА ЧАРДЖА ---
2026-02-06 11:34:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-02-06 11:34:22 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-02-06 11:34:22 | [MODEL] Чардж: нет доступных целей
2026-02-06 11:34:22 | --- ФАЗА БОЯ ---
2026-02-06 11:34:22 | --- ФАЗА БОЯ ---
2026-02-06 11:34:22 | [MODEL] Ближний бой: нет доступных атак
2026-02-06 11:34:22 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-06 11:34:22 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-02-06 11:34:22 | Итерация 2 завершена с наградой tensor([0.0500], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-02-06 11:34:22 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'modelCP': 6, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 2, 'player VP': 0, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-02-06 11:34:22 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 6, CP PLAYER: 6
VP MODEL: 2, VP PLAYER: 0

2026-02-06 11:34:22 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 11:34:22 | FX: buffer phase command (model)
2026-02-06 11:34:22 | FX: enqueue phase script command: units=0
2026-02-06 11:34:22 | FX: show summary command VP=2, CP=6
2026-02-06 11:34:22 | FX: wait_continue reason=phase_done next=ФАЗА ДВИЖЕНИЯ
2026-02-06 11:34:22 | FX: buffer phase movement (model)
2026-02-06 11:34:22 | FX: enqueue phase script movement: units=2
2026-02-06 11:34:22 | FX: buffer phase shooting (model)
2026-02-06 11:34:22 | FX: enqueue phase script shooting: units=2
2026-02-06 11:34:22 | FX: buffer phase charge (model)
2026-02-06 11:34:22 | FX: enqueue phase script charge: units=2
2026-02-06 11:34:22 | FX: buffer phase fight (model)
2026-02-06 11:34:22 | FX: enqueue phase script fight: units=2
2026-02-06 11:34:26 | FX: continue=Y
2026-02-06 11:34:26 | FX: show summary movement двигались 2/2, advance=2, dist=18.0
2026-02-06 11:34:26 | FX: move apply event_id=116 unit_id=21 side=model action=move from=[46, 3] types=('int', 'int') to=[46, 13] types=('int', 'int') key=('model', 21) render_found=1
2026-02-06 11:34:26 | FX: move write unit_id=21 side=model grid=(46,13) before=(46, 3) after=(46,13) cell_size=18 conversion=grid->world(cell_size)
2026-02-06 11:34:26 | FX: play unit_action unit=21 action=move
2026-02-06 11:34:26 | FX: wait_continue reason=unit_done next=Unit 22 — Necron Warriors (🚶 Движение: [24, 8] → [24, 16], dist=8.0, advance=да)
2026-02-06 11:34:29 | FX: continue=Y
2026-02-06 11:34:29 | Выбрано в таблице: row=1 -> unit_id=22
2026-02-06 11:34:29 | FX: move apply event_id=121 unit_id=22 side=model action=move from=[24, 8] types=('int', 'int') to=[24, 16] types=('int', 'int') key=('model', 22) render_found=1
2026-02-06 11:34:29 | FX: move write unit_id=22 side=model grid=(24,16) before=(24, 8) after=(24,16) cell_size=18 conversion=grid->world(cell_size)
2026-02-06 11:34:29 | FX: play unit_action unit=22 action=move
2026-02-06 11:34:29 | FX: wait_continue reason=unit_done next=unit
2026-02-06 11:34:38 | FX: continue=Y
2026-02-06 11:34:38 | FX: wait_continue reason=phase_done next=ФАЗА СТРЕЛЬБЫ
2026-02-06 11:34:40 | FX: continue=Y
2026-02-06 11:34:40 | FX: show summary shooting shots=0, skipped=2 (reasons: advanced_no_assault=2)
2026-02-06 11:34:40 | Выбрано в таблице: row=0 -> unit_id=21
2026-02-06 11:34:40 | FX: play unit_action unit=21 action=skip_shoot
2026-02-06 11:34:40 | FX: wait_continue reason=unit_done next=Unit 22 — Necron Warriors (⏭️ Skip shoot (advanced_no_assault))
2026-02-06 11:34:41 | FX: continue=Y
2026-02-06 11:34:41 | Выбрано в таблице: row=1 -> unit_id=22
2026-02-06 11:34:41 | FX: play unit_action unit=22 action=skip_shoot
2026-02-06 11:34:41 | FX: wait_continue reason=unit_done next=unit
2026-02-06 11:34:41 | FX: continue=Y
2026-02-06 11:34:41 | FX: wait_continue reason=phase_done next=ФАЗА ЧАРДЖА
2026-02-06 11:34:42 | FX: continue=Y
2026-02-06 11:34:42 | FX: show summary charge charges=0, skipped=2 (reasons: advanced_no_charge=2)
2026-02-06 11:34:42 | Выбрано в таблице: row=0 -> unit_id=21
2026-02-06 11:34:42 | FX: play unit_action unit=21 action=skip_charge
2026-02-06 11:34:42 | FX: wait_continue reason=unit_done next=Unit 22 — Necron Warriors (⏭️ Skip charge (advanced_no_charge))
2026-02-06 11:34:42 | FX: continue=Y
2026-02-06 11:34:42 | Выбрано в таблице: row=1 -> unit_id=22
2026-02-06 11:34:42 | FX: play unit_action unit=22 action=skip_charge
2026-02-06 11:34:42 | FX: wait_continue reason=unit_done next=unit
2026-02-06 11:34:42 | FX: continue=Y
2026-02-06 11:34:42 | FX: wait_continue reason=phase_done next=ФАЗА БОЯ
2026-02-06 11:34:47 | FX: continue=Y
2026-02-06 11:34:47 | FX: show summary fight fights=0, skipped=2 (reasons: no_attacks=2)
2026-02-06 11:34:47 | Выбрано в таблице: row=0 -> unit_id=21
2026-02-06 11:34:47 | FX: play unit_action unit=21 action=skip_fight
2026-02-06 11:34:47 | FX: wait_continue reason=unit_done next=Unit 22 — Necron Warriors (⏭️ Skip fight (no_attacks))
