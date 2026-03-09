2026-03-09 16:02:39 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-09 16:02:39 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-09 16:02:39 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-09 16:02:39 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-09 16:02:40 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 16:02:44 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-17-769447.pickle
2026-03-09 16:02:44 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-17-769447.pth
2026-03-09 16:02:44 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-09 16:02:54 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-03-09 16:02:54 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-09 16:02:54 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-09 16:02:54 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-09 16:02:54 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-09 16:02:54 | [DEPLOY] Order: model first, alternating
2026-03-09 16:02:54 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 16:02:54 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=2103, coord=(35,3), attempt=1, reward=+0.020, score_before=0.000, score_after=0.397, reward_delta=+0.020, forward=0.054, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 16:02:54 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (35,3)
2026-03-09 16:02:54 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 16:02:54 | Ошибка деплоя: reason=outside_deploy_zone, x=45, y=30. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-03-09 16:02:55 | REQ: deploy cell accepted x=48, y=21
2026-03-09 16:02:55 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (21,48)
2026-03-09 16:02:55 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (21,48)
2026-03-09 16:02:55 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 16:02:55 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1621, coord=(27,1), attempt=1, reward=-0.003, score_before=0.397, score_after=0.343, reward_delta=-0.003, forward=0.037, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 16:02:55 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (27,1)
2026-03-09 16:02:55 | REQ: deploy cell accepted x=50, y=11
2026-03-09 16:02:56 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (11,50)
2026-03-09 16:02:56 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (11,50)
2026-03-09 16:02:56 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.017 total_deploy_reward=+0.017 avg_forward=0.046 avg_spread=1.000 avg_edge=0.750 avg_cover=0.000
2026-03-09 16:02:56 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.01714623571147024, 'units': 2, 'total_deploy_reward': 0.01714623571147024, 'forward_sum': 0.09152542372881356, 'spread_sum': 2.0, 'edge_sum': 1.5, 'cover_sum': 0.0, 'avg_forward': 0.04576271186440678, 'avg_spread': 1.0, 'avg_edge': 0.75, 'avg_cover': 0.0}
2026-03-09 16:02:56 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-09 16:02:56 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-09 16:02:56 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-09 16:02:56 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 16:02:56 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-09 16:02:56 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 16:02:57 | === БОЕВОЙ РАУНД 1 ===
2026-03-09 16:02:57 | --- ХОД PLAYER ---
2026-03-09 16:02:57 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:02:57 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 16:02:57 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:02:58 | REQ: move cell accepted (RMB) x=38, y=23, mode=advance
2026-03-09 16:02:58 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:02:59 | REQ: move cell accepted (RMB) x=39, y=13, mode=advance
2026-03-09 16:02:59 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:02:59 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:02:59 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-09 16:02:59 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-09 16:02:59 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:02:59 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-09 16:02:59 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-09 16:02:59 | Нет доступных целей для чарджа.
2026-03-09 16:02:59 | --- ФАЗА БОЯ ---
2026-03-09 16:02:59 | --- ХОД MODEL ---
2026-03-09 16:02:59 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:02:59 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 16:02:59 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:02:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (35, 3). Выбор: up, advance=нет, distance=3
2026-03-09 16:02:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (32, 3)
2026-03-09 16:02:59 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:02:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (27, 1). Выбор: up, advance=да, бросок=3, макс=8, distance=8
2026-03-09 16:02:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (19, 1)
2026-03-09 16:02:59 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:02:59 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:02:59 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.84, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:02:59 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=39.12, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:02:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 16:02:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-09 16:02:59 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:02:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:02:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-09 16:02:59 | [MODEL] Чардж: нет доступных целей
2026-03-09 16:02:59 | --- ФАЗА БОЯ ---
2026-03-09 16:02:59 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 16:02:59 | Reward (progress к objective): d_before=29.833, d_after=29.017, delta=0.816, norm=0.136, bonus=+0.004
2026-03-09 16:02:59 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 16:02:59 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 16:02:59 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 16:02:59 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-09 16:02:59 | Итерация 0 завершена с наградой tensor([0.0041], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 16:02:59 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 16:02:59 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-09 16:03:01 | === БОЕВОЙ РАУНД 2 ===
2026-03-09 16:03:01 | --- ХОД PLAYER ---
2026-03-09 16:03:01 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:03:01 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 16:03:01 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:03:02 | REQ: move cell accepted (RMB) x=33, y=22, mode=normal
2026-03-09 16:03:03 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:03:03 | REQ: move cell accepted (RMB) x=34, y=17, mode=normal
2026-03-09 16:03:04 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:03:04 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:03:04 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:03:04 | Нет доступных целей для чарджа.
2026-03-09 16:03:04 | --- ФАЗА БОЯ ---
2026-03-09 16:03:04 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.46, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:04 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.30, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:04 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.07, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:04 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.02, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:04 | --- ХОД MODEL ---
2026-03-09 16:03:04 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:03:04 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 16:03:04 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:03:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (32, 3). Выбор: up, advance=нет, distance=3
2026-03-09 16:03:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (29, 3)
2026-03-09 16:03:04 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:03:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (19, 1). Выбор: up, advance=нет, distance=2
2026-03-09 16:03:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (17, 1)
2026-03-09 16:03:04 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:03:04 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:03:04 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.46, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:04 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.30, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 16:03:04 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.07, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:04 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.02, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 16:03:04 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:03:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:03:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:03:04 | [MODEL] Чардж: нет доступных целей
2026-03-09 16:03:04 | --- ФАЗА БОЯ ---
2026-03-09 16:03:04 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 16:03:04 | Reward (progress к objective): d_before=29.017, d_after=28.460, delta=0.557, norm=0.093, bonus=+0.003
2026-03-09 16:03:04 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 16:03:04 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 16:03:04 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 16:03:04 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-09 16:03:04 | Итерация 1 завершена с наградой tensor([0.0028], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 16:03:04 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 4, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 16:03:04 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 4, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0

2026-03-09 16:03:05 | === БОЕВОЙ РАУНД 3 ===
2026-03-09 16:03:05 | --- ХОД PLAYER ---
2026-03-09 16:03:05 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:03:05 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 16:03:05 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:03:07 | Unit 11: movement skipped (позиция сохранена x=33, y=22).
2026-03-09 16:03:07 | Unit 11 — Necrons Necron Warriors (x10 моделей): клетка (33,22) недостижима. Что делать дальше: выберите подсвеченную reachable-клетку.
2026-03-09 16:03:08 | REQ: move cell accepted (RMB) x=29, y=21, mode=normal
2026-03-09 16:03:09 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:03:10 | REQ: move cell accepted (RMB) x=29, y=16, mode=normal
2026-03-09 16:03:11 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:03:11 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:03:11 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:03:11 | Нет доступных целей для чарджа.
2026-03-09 16:03:11 | --- ФАЗА БОЯ ---
2026-03-09 16:03:11 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=24.04, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:11 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.94, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:11 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.18, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:11 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:11 | --- ХОД MODEL ---
2026-03-09 16:03:11 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:03:11 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 16:03:11 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:03:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=28.460, d_after=28.460, d_best=17.460, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-09 16:03:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (29, 3). Выбор: none, advance=нет, distance=0
2026-03-09 16:03:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (29, 3)
2026-03-09 16:03:11 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=29.155, d_after=29.155, d_best=18.155, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-09 16:03:11 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (17, 1). Выбор: none, advance=нет, distance=0
2026-03-09 16:03:11 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (17, 1)
2026-03-09 16:03:11 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-03-09 16:03:11 | Reward (шаг): движение delta=-0.180
2026-03-09 16:03:11 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:03:11 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=24.04, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:11 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.94, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 16:03:11 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.18, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:11 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:03:11 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 16:03:11 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:03:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:03:11 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:03:11 | [MODEL] Чардж: нет доступных целей
2026-03-09 16:03:11 | --- ФАЗА БОЯ ---
2026-03-09 16:03:11 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 16:03:11 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-03-09 16:03:11 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=28.460498941515414->28.460498941515414, hold_penalty_events=2
2026-03-09 16:03:11 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 16:03:11 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 16:03:11 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 16:03:11 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-09 16:03:11 | Итерация 2 завершена с наградой tensor([-0.2300], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 16:03:11 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 6, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 1, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 16:03:11 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 6, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 1

2026-03-09 16:03:13 | === БОЕВОЙ РАУНД 4 ===
2026-03-09 16:03:13 | --- ХОД PLAYER ---
2026-03-09 16:03:13 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:03:13 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 1 -> 2, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 16:03:13 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:03:14 | REQ: move cell accepted (RMB) x=26, y=21, mode=normal
2026-03-09 16:03:14 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-09 16:03:14 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 16:03:14 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-09 16:03:14 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 16:03:14 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 16:03:14 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:03:14 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-09 16:03:14 | Оружие: Gauss flayer
2026-03-09 16:03:14 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:03:14 | BS оружия: 4+
2026-03-09 16:03:14 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:03:14 | Save цели: 4+ (invul: нет)
2026-03-09 16:03:14 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:03:14 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:03:14 | Правило: Overwatch: попадания только на 6+
2026-03-09 16:03:14 | Hit rolls:    [5, 4, 4, 5, 3, 3, 2, 5, 5, 5]  -> hits: 7
2026-03-09 16:03:14 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 16:03:14 | FX: найден итог урона = 0.0.
2026-03-09 16:03:14 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0).
2026-03-09 16:03:14 | FX: позиция эффекта start=(84.0,708.0) end=(708.0,516.0).
2026-03-09 16:03:14 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-09 16:03:14 | 📌 -------------------------

2026-03-09 16:03:17 | REQ: move cell accepted (RMB) x=26, y=18, mode=normal
2026-03-09 16:03:17 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-09 16:03:17 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 16:03:17 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-09 16:03:17 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-09 16:03:17 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-09 16:03:17 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-09 16:03:17 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 16:03:17 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 16:03:17 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:03:17 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 16:03:17 | Оружие: Gauss flayer
2026-03-09 16:03:17 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:03:17 | BS оружия: 4+
2026-03-09 16:03:17 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:03:17 | Save цели: 4+ (invul: нет)
2026-03-09 16:03:17 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:03:17 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:03:17 | Правило: Overwatch: попадания только на 6+
2026-03-09 16:03:17 | Hit rolls:    [2, 4, 6, 6, 6, 3, 3, 4, 4, 6]  -> hits: 7 (crits: 4)
2026-03-09 16:03:17 | Wound rolls:  [6, 4, 5, 3]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 4 = 7
2026-03-09 16:03:17 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 16:03:17 | FX: найден итог урона = 1.0.
2026-03-09 16:03:17 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-09 16:03:17 | FX: позиция эффекта start=(84.0,708.0) end=(708.0,396.0).
2026-03-09 16:03:17 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-09 16:03:17 | 📌 -------------------------

2026-03-09 16:03:17 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:03:17 | REQ: валидные цели стрельбы для Unit 11: [21, 22]
2026-03-09 16:03:26 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 16:03:33 | 
🎲 Бросок на ранение (to wound): 6D6
2026-03-09 16:03:37 | 
🎲 Бросок сейвы (save): 4D6
2026-03-09 16:03:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (overwatch)
2026-03-09 16:03:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-09 16:03:40 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 2.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:03:40 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 16:03:40 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 16:03:40 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:03:40 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-09 16:03:40 | Оружие: Gauss flayer
2026-03-09 16:03:40 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:03:40 | BS оружия: 4+
2026-03-09 16:03:40 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:03:40 | Save цели: 4+ (invul: нет)
2026-03-09 16:03:40 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:03:40 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:03:40 | Hit rolls:    [1, 2, 3, 4, 5, 6, 5, 5, 5, 4]  -> hits: 7 (crits: 1)
2026-03-09 16:03:40 | Wound rolls:  [5, 6, 1, 2, 3, 4]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 1 = 4
2026-03-09 16:03:40 | Save rolls:   [2, 3, 4, 5]  (цель 4+) -> failed saves: 2
2026-03-09 16:03:40 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-09 16:03:40 | FX: найден итог урона = 2.0.
2026-03-09 16:03:40 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=2.0).
2026-03-09 16:03:40 | FX: позиция эффекта start=(636.0,516.0) end=(84.0,708.0).
2026-03-09 16:03:40 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-03-09 16:03:40 | 📌 -------------------------

2026-03-09 16:03:40 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-09 16:03:40 | REQ: валидные цели стрельбы для Unit 12: [21, 22]
2026-03-09 16:03:40 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 16:03:40 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 16:03:40 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 16:03:40 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:03:40 | FX: найден итог урона = 1.0.
2026-03-09 16:03:40 | FX: дубликат отчёта, эффект не создаём.
2026-03-09 16:03:46 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-09 16:03:50 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-09 16:03:53 | 
🎲 Бросок сейвы (save): 2D6
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (overwatch)
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-09 16:03:57 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 2.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:03:57 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 16:03:57 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 16:03:57 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:03:57 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-03-09 16:03:57 | Оружие: Gauss flayer
2026-03-09 16:03:57 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:03:57 | BS оружия: 4+
2026-03-09 16:03:57 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:03:57 | Save цели: 4+ (invul: нет)
2026-03-09 16:03:57 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:03:57 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:03:57 | Hit rolls:    [3, 4, 5, 6, 4, 5, 6, 5, 1]  -> hits: 7 (crits: 2)
2026-03-09 16:03:57 | Wound rolls:  [1, 1, 1, 1, 1]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 2 = 2
2026-03-09 16:03:57 | Save rolls:   [1, 1]  (цель 4+) -> failed saves: 2
2026-03-09 16:03:57 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-09 16:03:57 | FX: найден итог урона = 2.0.
2026-03-09 16:03:57 | FX: создан FxShotEvent (attacker=12, target=22, weapon=Gauss flayer, damage=2.0).
2026-03-09 16:03:57 | FX: позиция эффекта start=(636.0,444.0) end=(36.0,420.0).
2026-03-09 16:03:57 | FX: эффект добавлен в рендер (attacker=12, target=22).
2026-03-09 16:03:57 | 📌 -------------------------

2026-03-09 16:03:57 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:03:57 | Нет доступных целей для чарджа.
2026-03-09 16:03:57 | --- ФАЗА БОЯ ---
2026-03-09 16:03:57 | --- ХОД MODEL ---
2026-03-09 16:03:57 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-09 16:03:57 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 16:03:57 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=28.460, d_after=28.460, d_best=17.460, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (29, 3). Выбор: none, advance=нет, distance=0
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (29, 3)
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=29.155, d_after=29.155, d_best=18.155, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (17, 1). Выбор: none, advance=нет, distance=0
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (17, 1)
2026-03-09 16:03:57 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-03-09 16:03:57 | Reward (шаг): движение delta=-0.180
2026-03-09 16:03:57 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-09 16:03:57 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 16:03:57 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-09 16:03:57 | 
🎲 Бросок сейвы (save): 3D6
2026-03-09 16:03:57 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-03-09 16:03:57 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=19, need<=3).
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.200
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-09 16:03:57 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 16:03:57 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 16:03:57 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:03:57 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-09 16:03:57 | Оружие: Gauss flayer
2026-03-09 16:03:57 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:03:57 | BS оружия: 4+
2026-03-09 16:03:57 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:03:57 | Save цели: 4+ (invul: нет)
2026-03-09 16:03:57 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:03:57 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:03:57 | Hit rolls:    [4, 6, 5, 3, 2, 4, 3, 5, 3, 2]  -> hits: 5 (crits: 1)
2026-03-09 16:03:57 | Wound rolls:  [4, 5, 1, 3]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 1 = 3
2026-03-09 16:03:57 | Save rolls:   [6, 5, 1]  (цель 4+) -> failed saves: 1
2026-03-09 16:03:57 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 16:03:57 | FX: найден итог урона = 1.0.
2026-03-09 16:03:57 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-09 16:03:57 | FX: позиция эффекта start=(84.0,708.0) end=(636.0,516.0).
2026-03-09 16:03:57 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-09 16:03:57 | 📌 -------------------------

2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-09 16:03:57 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-09 16:03:57 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-09 16:03:57 | 
🎲 Бросок сейвы (save): 5D6
2026-03-09 16:03:57 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 8. HP: 9.0 -> 8.0 (shooting)
2026-03-09 16:03:57 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.200
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-09 16:03:57 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 16:03:57 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 16:03:57 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:03:57 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-09 16:03:57 | Оружие: Gauss flayer
2026-03-09 16:03:57 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:03:57 | BS оружия: 4+
2026-03-09 16:03:57 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:03:57 | Save цели: 4+ (invul: нет)
2026-03-09 16:03:57 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:03:57 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:03:57 | Hit rolls:    [5, 5, 5, 3, 6, 2, 6, 6, 6]  -> hits: 7 (crits: 4)
2026-03-09 16:03:57 | Wound rolls:  [5, 1, 1]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 4 = 5
2026-03-09 16:03:57 | Save rolls:   [4, 6, 5, 1, 4]  (цель 4+) -> failed saves: 1
2026-03-09 16:03:57 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 16:03:57 | FX: найден итог урона = 1.0.
2026-03-09 16:03:57 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-09 16:03:57 | FX: позиция эффекта start=(36.0,420.0) end=(636.0,516.0).
2026-03-09 16:03:57 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-09 16:03:57 | 📌 -------------------------

2026-03-09 16:03:57 | Reward (шаг): стрельба delta=+0.400
2026-03-09 16:03:57 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:03:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:03:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:03:57 | [MODEL] Чардж: нет доступных целей
2026-03-09 16:03:57 | --- ФАЗА БОЯ ---
2026-03-09 16:03:57 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 16:03:57 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-03-09 16:03:57 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.067, delta=+0.001; cover=0.000->0.000, threat=-0.667->-0.667, guard=0.000->0.000
2026-03-09 16:03:57 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=4)
2026-03-09 16:03:57 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-09 16:03:57 | === КОНЕЦ БОЕВОГО РАУНДА 4 ===
2026-03-09 16:03:57 | Итерация 3 завершена с наградой tensor([0.1507], device='cuda:0'), здоровье игрока [8.0, 9.0], здоровье модели [10.0, 9.0]
2026-03-09 16:03:57 | {'model health': [10.0, 9.0], 'player health': [8.0, 9.0], 'model alive models': [10, 9], 'player alive models': [8, 9], 'modelCP': 6, 'playerCP': 8, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 2, 'mission': 'Only War', 'turn': 5, 'battle round': 5, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 16:03:57 | Здоровье MODEL: [10.0, 9.0], здоровье PLAYER: [8.0, 9.0]
CP MODEL: 6, CP PLAYER: 8
VP MODEL: 0, VP PLAYER: 2
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-03-09 16:03:59 | === БОЕВОЙ РАУНД 5 ===
2026-03-09 16:03:59 | --- ХОД PLAYER ---
2026-03-09 16:03:59 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:03:59 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 16:04:01 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 16:04:01 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-09 16:04:01 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 16:04:01 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-09 16:04:01 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 16:04:02 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 16:04:02 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-09 16:04:02 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 16:04:02 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-09 16:04:02 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 2 -> 3, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 16:04:02 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:04:05 | REQ: move cell accepted (RMB) x=28, y=24, mode=normal
2026-03-09 16:04:05 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-09 16:04:05 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 16:04:05 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-09 16:04:05 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 8. HP: 9.0 -> 8.0 (Overwatch)
2026-03-09 16:04:05 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-09 16:04:05 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-09 16:04:05 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 16:04:05 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 16:04:05 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:04:05 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-09 16:04:05 | Оружие: Gauss flayer
2026-03-09 16:04:05 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:04:05 | BS оружия: 4+
2026-03-09 16:04:05 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:04:05 | Save цели: 4+ (invul: нет)
2026-03-09 16:04:05 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:04:05 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:04:05 | Правило: Overwatch: попадания только на 6+
2026-03-09 16:04:05 | Hit rolls:    [6, 1, 5, 4, 5, 4, 1, 1, 5, 3]  -> hits: 6 (crits: 1)
2026-03-09 16:04:05 | Wound rolls:  [2]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 1 = 1
2026-03-09 16:04:05 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 16:04:05 | FX: найден итог урона = 1.0.
2026-03-09 16:04:05 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-09 16:04:05 | FX: позиция эффекта start=(84.0,708.0) end=(636.0,516.0).
2026-03-09 16:04:05 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-09 16:04:05 | 📌 -------------------------

2026-03-09 16:04:08 | REQ: move cell accepted (RMB) x=29, y=17, mode=normal
2026-03-09 16:04:08 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:04:08 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:04:08 | REQ: shooter changed Unit 12->Unit 11, target reset
2026-03-09 16:04:08 | REQ: валидные цели стрельбы для Unit 11: [21]
2026-03-09 16:04:13 | 
🎲 Бросок на попадание (to hit): 8D6
2026-03-09 16:04:17 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:04:17 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 16:04:17 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 16:04:17 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:04:17 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-09 16:04:17 | Оружие: Gauss flayer
2026-03-09 16:04:17 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:04:17 | BS оружия: 4+
2026-03-09 16:04:17 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:04:17 | Save цели: 4+ (invul: нет)
2026-03-09 16:04:17 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:04:17 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:04:17 | Hit rolls:    [1, 1, 1, 1, 1, 1, 1, 1]  -> hits: 0
2026-03-09 16:04:17 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 16:04:17 | FX: найден итог урона = 0.0.
2026-03-09 16:04:17 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=0.0).
2026-03-09 16:04:17 | FX: позиция эффекта start=(684.0,588.0) end=(84.0,708.0).
2026-03-09 16:04:17 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-03-09 16:04:17 | 📌 -------------------------

2026-03-09 16:04:17 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:04:17 | Нет доступных целей для чарджа.
2026-03-09 16:04:17 | --- ФАЗА БОЯ ---
2026-03-09 16:04:17 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.50, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:04:17 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.71, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:04:17 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:04:17 | --- ХОД MODEL ---
2026-03-09 16:04:17 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:04:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 16:04:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 16:04:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-09 16:04:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 16:04:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-09 16:04:17 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 16:04:17 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:04:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=28.460, d_after=28.460, d_best=17.460, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-03-09 16:04:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (29, 3). Выбор: none, advance=нет, distance=0
2026-03-09 16:04:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (29, 3)
2026-03-09 16:04:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=29.155, d_after=29.155, d_best=18.155, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-03-09 16:04:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (17, 1). Выбор: none, advance=нет, distance=0
2026-03-09 16:04:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (17, 1)
2026-03-09 16:04:17 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-03-09 16:04:17 | Reward (шаг): движение delta=-0.240
2026-03-09 16:04:17 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:04:17 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.50, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:04:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-09 16:04:17 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 16:04:17 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 16:04:17 | 
🎲 Бросок сейвы (save): 3D6
2026-03-09 16:04:17 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 7. HP: 8.0 -> 7.0 (shooting)
2026-03-09 16:04:17 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-09 16:04:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-09 16:04:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-03-09 16:04:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-03-09 16:04:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=19, need<=3).
2026-03-09 16:04:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.200
2026-03-09 16:04:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-09 16:04:17 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 16:04:17 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 16:04:17 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:04:17 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-09 16:04:17 | Оружие: Gauss flayer
2026-03-09 16:04:17 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:04:17 | BS оружия: 4+
2026-03-09 16:04:17 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:04:17 | Save цели: 4+ (invul: нет)
2026-03-09 16:04:17 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:04:17 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:04:17 | Hit rolls:    [4, 4, 2, 6, 1, 6, 2, 1, 2, 6]  -> hits: 5 (crits: 3)
2026-03-09 16:04:17 | Wound rolls:  [3, 2]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 3 = 3
2026-03-09 16:04:17 | Save rolls:   [5, 4, 1]  (цель 4+) -> failed saves: 1
2026-03-09 16:04:17 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 16:04:17 | FX: найден итог урона = 1.0.
2026-03-09 16:04:17 | FX: дубликат отчёта, эффект не создаём.
2026-03-09 16:04:17 | 📌 -------------------------

2026-03-09 16:04:17 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:04:17 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:04:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 16:04:17 | Reward (шаг): стрельба delta=+0.200
2026-03-09 16:04:17 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:04:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:04:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:04:17 | [MODEL] Чардж: нет доступных целей
2026-03-09 16:04:17 | --- ФАЗА БОЯ ---
2026-03-09 16:04:17 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 16:04:17 | Reward (VP diff): prev=-2, curr=-3, delta=-1, reward=+0.000, penalty=-0.050
2026-03-09 16:04:17 | Reward (terrain/potential): gamma=0.990, phi_before=-0.017, phi_after=-0.017, delta=+0.000; cover=0.000->0.000, threat=-0.167->-0.167, guard=0.000->0.000
2026-03-09 16:04:17 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=1)
2026-03-09 16:04:17 | Reward (terrain/clamp): raw=-0.010, cap=±0.120, clamp не сработал
2026-03-09 16:04:17 | === КОНЕЦ БОЕВОГО РАУНДА 5 ===
2026-03-09 16:04:17 | Итерация 4 завершена с наградой tensor([-0.0998], device='cuda:0'), здоровье игрока [7.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 16:04:17 | {'model health': [10.0, 10.0], 'player health': [7.0, 10.0], 'model alive models': [10, 10], 'player alive models': [7, 10], 'modelCP': 7, 'playerCP': 10, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 3, 'mission': 'Only War', 'turn': 6, 'battle round': 6, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 16:04:17 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [7.0, 10.0]
CP MODEL: 7, CP PLAYER: 10
VP MODEL: 0, VP PLAYER: 3
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-03-09 16:04:19 | === БОЕВОЙ РАУНД 6 ===
2026-03-09 16:04:19 | --- ХОД PLAYER ---
2026-03-09 16:04:19 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:04:19 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 16:04:20 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 16:04:20 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-03-09 16:04:20 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 16:04:20 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-09 16:04:20 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 3 -> 4, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 16:04:20 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:04:24 | REQ: move cell accepted (RMB) x=31, y=26, mode=normal
2026-03-09 16:04:24 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:04:29 | REQ: move cell accepted (RMB) x=27, y=17, mode=normal
2026-03-09 16:04:29 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-09 16:04:29 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 16:04:29 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-09 16:04:29 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (Overwatch)
2026-03-09 16:04:29 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-09 16:04:29 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 3.0.
2026-03-09 16:04:29 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 16:04:29 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 16:04:29 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:04:29 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 16:04:29 | Оружие: Gauss flayer
2026-03-09 16:04:29 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:04:29 | BS оружия: 4+
2026-03-09 16:04:29 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:04:29 | Save цели: 4+ (invul: нет)
2026-03-09 16:04:29 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:04:29 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:04:29 | Правило: Overwatch: попадания только на 6+
2026-03-09 16:04:29 | Hit rolls:    [6, 4, 1, 1, 2, 2, 6, 6, 1, 3]  -> hits: 4 (crits: 3)
2026-03-09 16:04:29 | Wound rolls:  [2, 2, 3]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 3 = 3
2026-03-09 16:04:29 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-09 16:04:29 | FX: найден итог урона = 3.0.
2026-03-09 16:04:29 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=3.0).
2026-03-09 16:04:29 | FX: позиция эффекта start=(84.0,708.0) end=(708.0,420.0).
2026-03-09 16:04:29 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-09 16:04:29 | 📌 -------------------------

2026-03-09 16:04:29 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:04:29 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-09 16:04:29 | REQ: валидные цели стрельбы для Unit 12: [21, 22]
2026-03-09 16:04:37 | 
🎲 Бросок на попадание (to hit): 7D6
2026-03-09 16:04:40 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:04:40 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 16:04:40 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 16:04:40 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:04:40 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-03-09 16:04:40 | Оружие: Gauss flayer
2026-03-09 16:04:40 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:04:40 | BS оружия: 4+
2026-03-09 16:04:40 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:04:40 | Save цели: 4+ (invul: нет)
2026-03-09 16:04:40 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:04:40 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:04:40 | Hit rolls:    [1, 1, 1, 1, 1, 1, 1]  -> hits: 0
2026-03-09 16:04:40 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 16:04:40 | FX: найден итог урона = 0.0.
2026-03-09 16:04:40 | FX: создан FxShotEvent (attacker=12, target=22, weapon=Gauss flayer, damage=0.0).
2026-03-09 16:04:40 | FX: позиция эффекта start=(660.0,420.0) end=(36.0,420.0).
2026-03-09 16:04:40 | FX: эффект добавлен в рендер (attacker=12, target=22).
2026-03-09 16:04:40 | 📌 -------------------------

2026-03-09 16:04:40 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:04:40 | Нет доступных целей для чарджа.
2026-03-09 16:04:40 | --- ФАЗА БОЯ ---
2026-03-09 16:04:40 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.08, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:04:40 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.46, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:04:40 | --- ХОД MODEL ---
2026-03-09 16:04:40 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:04:40 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 16:04:40 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:04:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=28.460, d_after=28.460, d_best=17.460, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-03-09 16:04:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (29, 3). Выбор: none, advance=нет, distance=0
2026-03-09 16:04:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (29, 3)
2026-03-09 16:04:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=29.155, d_after=29.155, d_best=18.155, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-03-09 16:04:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (17, 1). Выбор: none, advance=нет, distance=0
2026-03-09 16:04:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (17, 1)
2026-03-09 16:04:40 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-03-09 16:04:40 | Reward (шаг): движение delta=-0.240
2026-03-09 16:04:40 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:04:40 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.08, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:04:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-09 16:04:40 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 16:04:40 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 16:04:40 | 
🎲 Бросок сейвы (save): 3D6
2026-03-09 16:04:40 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 5. HP: 7.0 -> 5.0 (shooting)
2026-03-09 16:04:40 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-03-09 16:04:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-09 16:04:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-03-09 16:04:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-03-09 16:04:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=19, need<=3).
2026-03-09 16:04:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.280
2026-03-09 16:04:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-09 16:04:40 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 16:04:40 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 16:04:40 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:04:40 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 16:04:40 | Оружие: Gauss flayer
2026-03-09 16:04:40 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:04:40 | BS оружия: 4+
2026-03-09 16:04:40 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:04:40 | Save цели: 4+ (invul: нет)
2026-03-09 16:04:40 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:04:40 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:04:40 | Hit rolls:    [2, 5, 6, 6, 2, 2, 1, 6, 3, 5]  -> hits: 5 (crits: 3)
2026-03-09 16:04:40 | Wound rolls:  [2, 2]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 3 = 3
2026-03-09 16:04:40 | Save rolls:   [1, 1, 4]  (цель 4+) -> failed saves: 2
2026-03-09 16:04:40 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-09 16:04:40 | FX: найден итог урона = 2.0.
2026-03-09 16:04:40 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=2.0).
2026-03-09 16:04:40 | FX: позиция эффекта start=(84.0,708.0) end=(660.0,420.0).
2026-03-09 16:04:40 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-09 16:04:40 | 📌 -------------------------

2026-03-09 16:04:40 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.46, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:04:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-09 16:04:40 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 16:04:40 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-09 16:04:40 | 
🎲 Бросок сейвы (save): 4D6
2026-03-09 16:04:40 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 2. HP: 5.0 -> 2.0 (shooting)
2026-03-09 16:04:40 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 2. Причина: потери моделей.
2026-03-09 16:04:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-03-09 16:04:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-03-09 16:04:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.150 (dealt=3.00)
2026-03-09 16:04:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-09 16:04:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.150, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.360
2026-03-09 16:04:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 3.0
2026-03-09 16:04:40 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 16:04:40 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 16:04:40 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:04:40 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-09 16:04:40 | Оружие: Gauss flayer
2026-03-09 16:04:40 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:04:40 | BS оружия: 4+
2026-03-09 16:04:40 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:04:40 | Save цели: 4+ (invul: нет)
2026-03-09 16:04:40 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:04:40 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:04:40 | Hit rolls:    [1, 5, 2, 1, 3, 1, 4, 5, 6, 4]  -> hits: 5 (crits: 1)
2026-03-09 16:04:40 | Wound rolls:  [4, 4, 4, 1]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 1 = 4
2026-03-09 16:04:40 | Save rolls:   [1, 3, 5, 3]  (цель 4+) -> failed saves: 3
2026-03-09 16:04:40 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-09 16:04:40 | FX: найден итог урона = 3.0.
2026-03-09 16:04:40 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=3.0).
2026-03-09 16:04:40 | FX: позиция эффекта start=(36.0,420.0) end=(660.0,420.0).
2026-03-09 16:04:40 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-09 16:04:40 | 📌 -------------------------

2026-03-09 16:04:40 | Reward (шаг): стрельба delta=+0.640
2026-03-09 16:04:40 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:04:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:04:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:04:40 | [MODEL] Чардж: нет доступных целей
2026-03-09 16:04:40 | --- ФАЗА БОЯ ---
2026-03-09 16:04:40 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 16:04:40 | Reward (VP diff): prev=-3, curr=-4, delta=-1, reward=+0.000, penalty=-0.050
2026-03-09 16:04:40 | Reward (terrain/potential): gamma=0.990, phi_before=-0.033, phi_after=-0.017, delta=+0.017; cover=0.000->0.000, threat=-0.333->-0.167, guard=0.000->0.000
2026-03-09 16:04:40 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=1)
2026-03-09 16:04:40 | Reward (terrain/clamp): raw=+0.007, cap=±0.120, clamp не сработал
2026-03-09 16:04:40 | === КОНЕЦ БОЕВОГО РАУНДА 6 ===
2026-03-09 16:04:40 | Итерация 5 завершена с наградой tensor([0.3568], device='cuda:0'), здоровье игрока [8.0, 2.0], здоровье модели [10.0, 10.0]
2026-03-09 16:04:40 | {'model health': [10.0, 10.0], 'player health': [8.0, 2.0], 'model alive models': [10, 10], 'player alive models': [8, 2], 'modelCP': 8, 'playerCP': 12, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 4, 'mission': 'Only War', 'turn': 7, 'battle round': 7, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 16:04:40 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [8.0, 2.0]
CP MODEL: 8, CP PLAYER: 12
VP MODEL: 0, VP PLAYER: 4
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 3.0 раз(а)

2026-03-09 16:04:41 | === БОЕВОЙ РАУНД 7 ===
2026-03-09 16:04:41 | --- ХОД PLAYER ---
2026-03-09 16:04:41 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:04:41 | Unit 12 — Necrons Necron Warriors (x10 моделей): ниже половины состава, тест Battle-shock.
2026-03-09 16:04:41 | Бросок 2D6...
2026-03-09 16:04:48 | Бросок: 2 2
2026-03-09 16:04:48 | Unit 12 — Necrons Necron Warriors (x10 моделей): тест Battle-shock провален.
2026-03-09 16:04:51 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 16:04:52 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 16:04:52 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-09 16:04:52 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 16:04:52 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-09 16:04:52 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 16:04:54 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 16:04:54 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=2, раны=[1, 1] всего=2
2026-03-09 16:04:54 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 16:04:54 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=3, раны=[1, 1, 1] всего=3
2026-03-09 16:04:54 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 4 -> 5, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 16:04:54 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:04:57 | REQ: move cell accepted (RMB) x=30, y=26, mode=normal
2026-03-09 16:04:57 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:05:02 | REQ: move cell accepted (RMB) x=30, y=18, mode=normal
2026-03-09 16:05:03 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:05:03 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:05:03 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:05:03 | Нет доступных целей для чарджа.
2026-03-09 16:05:03 | --- ФАЗА БОЯ ---
2026-03-09 16:05:03 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=24.08, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:03 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.40, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:03 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.20, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:03 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.02, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:03 | --- ХОД MODEL ---
2026-03-09 16:05:03 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:05:03 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 16:05:03 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:05:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (29, 3). Выбор: down, advance=нет, distance=4
2026-03-09 16:05:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (33, 3)
2026-03-09 16:05:03 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:05:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (17, 1). Выбор: down, advance=нет, distance=4
2026-03-09 16:05:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (21, 1)
2026-03-09 16:05:03 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:05:03 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:05:03 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=24.08, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:03 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.40, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 16:05:03 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.20, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:03 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.02, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 16:05:03 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:05:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:05:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:05:03 | [MODEL] Чардж: нет доступных целей
2026-03-09 16:05:03 | --- ФАЗА БОЯ ---
2026-03-09 16:05:03 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 16:05:03 | Reward (VP diff): prev=-4, curr=-5, delta=-1, reward=+0.000, penalty=-0.050
2026-03-09 16:05:03 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=28.460498941515414->29.017236257093817
2026-03-09 16:05:03 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 16:05:03 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 16:05:03 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 16:05:03 | === КОНЕЦ БОЕВОГО РАУНДА 7 ===
2026-03-09 16:05:03 | Итерация 6 завершена с наградой tensor([-0.0700], device='cuda:0'), здоровье игрока [9.0, 3.0], здоровье модели [10.0, 10.0]
2026-03-09 16:05:03 | {'model health': [10.0, 10.0], 'player health': [9.0, 3.0], 'model alive models': [10, 10], 'player alive models': [9, 3], 'modelCP': 10, 'playerCP': 13, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 5, 'mission': 'Only War', 'turn': 8, 'battle round': 8, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 16:05:03 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [9.0, 3.0]
CP MODEL: 10, CP PLAYER: 13
VP MODEL: 0, VP PLAYER: 5

2026-03-09 16:05:04 | === БОЕВОЙ РАУНД 8 ===
2026-03-09 16:05:04 | --- ХОД PLAYER ---
2026-03-09 16:05:04 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:05:04 | Unit 12 — Necrons Necron Warriors (x10 моделей): ниже половины состава, тест Battle-shock.
2026-03-09 16:05:04 | Бросок 2D6...
2026-03-09 16:05:07 | Бросок: 1 1
2026-03-09 16:05:07 | Unit 12 — Necrons Necron Warriors (x10 моделей): тест Battle-shock провален.
2026-03-09 16:05:10 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 16:05:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 16:05:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-09 16:05:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 16:05:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-09 16:05:12 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 16:05:14 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 16:05:14 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=3, раны=[1, 1, 1] всего=3
2026-03-09 16:05:14 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 16:05:14 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=4, раны=[1, 1, 1, 1] всего=4
2026-03-09 16:05:14 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 5 -> 5; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 16:05:14 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:05:17 | REQ: move cell accepted (RMB) x=29, y=28, mode=normal
2026-03-09 16:05:18 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-09 16:05:18 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 16:05:18 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-09 16:05:18 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-03-09 16:05:18 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-09 16:05:18 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-09 16:05:18 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 16:05:18 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 16:05:18 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:05:18 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-09 16:05:18 | Оружие: Gauss flayer
2026-03-09 16:05:18 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:05:18 | BS оружия: 4+
2026-03-09 16:05:18 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:05:18 | Save цели: 4+ (invul: нет)
2026-03-09 16:05:18 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:05:18 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:05:18 | Правило: Overwatch: попадания только на 6+
2026-03-09 16:05:18 | Hit rolls:    [6, 3, 4, 1, 3, 6, 5, 2, 3, 6]  -> hits: 5 (crits: 3)
2026-03-09 16:05:18 | Wound rolls:  [1, 5, 1]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 3 = 4
2026-03-09 16:05:18 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-09 16:05:18 | FX: найден итог урона = 2.0.
2026-03-09 16:05:18 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-09 16:05:18 | FX: позиция эффекта start=(84.0,804.0) end=(732.0,636.0).
2026-03-09 16:05:18 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-09 16:05:18 | 📌 -------------------------

2026-03-09 16:05:21 | REQ: move cell accepted (RMB) x=28, y=19, mode=normal
2026-03-09 16:05:21 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:05:21 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:05:21 | REQ: shooter changed Unit 12->Unit 11, target reset
2026-03-09 16:05:21 | REQ: валидные цели стрельбы для Unit 11: [21]
2026-03-09 16:05:25 | REQ: ПКМ по Unit 22 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [21]
2026-03-09 16:05:39 | 
🎲 Бросок на попадание (to hit): 8D6
2026-03-09 16:05:44 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:05:44 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 16:05:44 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 16:05:44 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:05:44 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-09 16:05:44 | Оружие: Gauss flayer
2026-03-09 16:05:44 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:05:44 | BS оружия: 4+
2026-03-09 16:05:44 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:05:44 | Save цели: 4+ (invul: нет)
2026-03-09 16:05:44 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:05:44 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:05:44 | Hit rolls:    [1, 1, 1, 1, 1, 1, 1, 1]  -> hits: 0
2026-03-09 16:05:44 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 16:05:44 | FX: найден итог урона = 0.0.
2026-03-09 16:05:44 | FX: дубликат отчёта, эффект не создаём.
2026-03-09 16:05:44 | 📌 -------------------------

2026-03-09 16:05:44 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:05:44 | Нет доступных целей для чарджа.
2026-03-09 16:05:44 | --- ФАЗА БОЯ ---
2026-03-09 16:05:44 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.08, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:44 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.96, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:44 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=24.08, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:44 | --- ХОД MODEL ---
2026-03-09 16:05:44 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:05:44 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 16:05:44 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 16:05:44 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (33, 3). Выбор: down, advance=нет, distance=4
2026-03-09 16:05:44 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (37, 3)
2026-03-09 16:05:44 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-09 16:05:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (21, 1). Выбор: down, advance=нет, distance=4
2026-03-09 16:05:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (25, 1)
2026-03-09 16:05:45 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 16:05:45 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 16:05:45 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.08, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-09 16:05:45 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 16:05:45 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 16:05:45 | 
🎲 Бросок сейвы (save): 5D6
2026-03-09 16:05:45 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 5. HP: 8.0 -> 5.0 (shooting)
2026-03-09 16:05:45 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-03-09 16:05:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-03-09 16:05:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-09 16:05:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=22, need<=3).
2026-03-09 16:05:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.140
2026-03-09 16:05:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 3.0
2026-03-09 16:05:45 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 16:05:45 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 16:05:45 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 16:05:45 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-09 16:05:45 | Оружие: Gauss flayer
2026-03-09 16:05:45 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 16:05:45 | BS оружия: 4+
2026-03-09 16:05:45 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 16:05:45 | Save цели: 4+ (invul: нет)
2026-03-09 16:05:45 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 16:05:45 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 16:05:45 | Hit rolls:    [4, 1, 5, 6, 2, 1, 6, 6, 3, 3]  -> hits: 5 (crits: 3)
2026-03-09 16:05:45 | Wound rolls:  [4, 4]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 3 = 5
2026-03-09 16:05:45 | Save rolls:   [2, 3, 5, 6, 2]  (цель 4+) -> failed saves: 3
2026-03-09 16:05:45 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-09 16:05:45 | FX: найден итог урона = 3.0.
2026-03-09 16:05:45 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=3.0).
2026-03-09 16:05:45 | FX: позиция эффекта start=(84.0,804.0) end=(708.0,684.0).
2026-03-09 16:05:45 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-09 16:05:45 | 📌 -------------------------

2026-03-09 16:05:45 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.18, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:45 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=24.74, range=24.00). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-09 16:05:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 16:05:45 | Reward (шаг): стрельба delta=+0.140
2026-03-09 16:05:45 | --- ФАЗА ЧАРДЖА ---
2026-03-09 16:05:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:05:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 16:05:45 | [MODEL] Чардж: нет доступных целей
2026-03-09 16:05:45 | --- ФАЗА БОЯ ---
2026-03-09 16:05:45 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 16:05:45 | Reward (terrain/potential): gamma=0.990, phi_before=-0.017, phi_after=+0.000, delta=+0.017; cover=0.000->0.000, threat=-0.167->-0.000, guard=0.000->0.000
2026-03-09 16:05:45 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 16:05:45 | Reward (terrain/clamp): raw=+0.017, cap=±0.120, clamp не сработал
2026-03-09 16:05:45 | === КОНЕЦ БОЕВОГО РАУНДА 8 ===
2026-03-09 16:05:45 | Итерация 7 завершена с наградой tensor([0.1567], device='cuda:0'), здоровье игрока [5.0, 4.0], здоровье модели [10.0, 10.0]
2026-03-09 16:05:45 | {'model health': [10.0, 10.0], 'player health': [5.0, 4.0], 'model alive models': [10, 10], 'player alive models': [5, 4], 'modelCP': 11, 'playerCP': 15, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 5, 'mission': 'Only War', 'turn': 9, 'battle round': 9, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 16:05:45 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [5.0, 4.0]
CP MODEL: 11, CP PLAYER: 15
VP MODEL: 0, VP PLAYER: 5
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 3.0 раз(а)

2026-03-09 16:05:46 | === БОЕВОЙ РАУНД 9 ===
2026-03-09 16:05:46 | --- ХОД PLAYER ---
2026-03-09 16:05:46 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 16:05:46 | Unit 12 — Necrons Necron Warriors (x10 моделей): ниже половины состава, тест Battle-shock.
2026-03-09 16:05:46 | Бросок 2D6...
