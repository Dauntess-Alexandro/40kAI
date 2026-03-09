2026-03-09 10:36:58 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-09 10:36:58 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-09 10:36:58 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-09 10:36:58 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-09 10:36:58 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 10:36:59 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 10:36:59 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-48-168877.pickle
2026-03-09 10:36:59 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-48-168877.pth
2026-03-09 10:36:59 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-09 10:37:05 | Roll-off Attacker/Defender: enemy=1 model=4 -> attacker=model
2026-03-09 10:37:05 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-09 10:37:05 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-09 10:37:05 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-09 10:37:05 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-09 10:37:05 | [DEPLOY] Order: model first, alternating
2026-03-09 10:37:05 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 10:37:05 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=2108, coord=(35,8), attempt=1, reward=+0.022, score_before=0.000, score_after=0.437, reward_delta=+0.022, forward=0.139, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 10:37:05 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (35,8)
2026-03-09 10:37:05 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 10:37:05 | REQ: deploy cell accepted x=49, y=30
2026-03-09 10:37:05 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (30,49)
2026-03-09 10:37:05 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (30,49)
2026-03-09 10:37:05 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 10:37:05 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=662, coord=(11,2), attempt=1, reward=-0.002, score_before=0.437, score_after=0.390, reward_delta=-0.002, forward=0.088, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 10:37:05 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (11,2)
2026-03-09 10:37:06 | REQ: deploy cell accepted x=50, y=22
2026-03-09 10:37:06 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,50)
2026-03-09 10:37:06 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,50)
2026-03-09 10:37:06 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.114 avg_spread=1.000 avg_edge=0.875 avg_cover=0.000
2026-03-09 10:37:06 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.019491525423728815, 'units': 2, 'total_deploy_reward': 0.019491525423728815, 'forward_sum': 0.2271186440677966, 'spread_sum': 2.0, 'edge_sum': 1.75, 'cover_sum': 0.0, 'avg_forward': 0.1135593220338983, 'avg_spread': 1.0, 'avg_edge': 0.875, 'avg_cover': 0.0}
2026-03-09 10:37:06 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-09 10:37:06 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-09 10:37:06 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-09 10:37:06 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:37:06 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-09 10:37:07 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 10:37:08 | === БОЕВОЙ РАУНД 1 ===
2026-03-09 10:37:08 | --- ХОД PLAYER ---
2026-03-09 10:37:08 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:37:08 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:37:08 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:37:09 | REQ: move cell accepted (RMB) x=44, y=29, mode=normal
2026-03-09 10:37:09 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:37:10 | REQ: move cell accepted (RMB) x=39, y=21, mode=advance
2026-03-09 10:37:11 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:37:11 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:37:11 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-09 10:37:11 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:37:11 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-09 10:37:11 | Нет доступных целей для чарджа.
2026-03-09 10:37:11 | --- ФАЗА БОЯ ---
2026-03-09 10:37:11 | --- ХОД MODEL ---
2026-03-09 10:37:11 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:37:11 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:37:11 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:37:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (35, 8). Выбор: up, advance=нет, distance=3
2026-03-09 10:37:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (32, 8)
2026-03-09 10:37:11 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:37:11 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (11, 2). Выбор: up, advance=нет, distance=1
2026-03-09 10:37:11 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (10, 2)
2026-03-09 10:37:11 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:37:11 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:37:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:37:11 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:37:11 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:37:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:37:11 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:37:11 | [MODEL] Чардж: нет доступных целей
2026-03-09 10:37:11 | --- ФАЗА БОЯ ---
2026-03-09 10:37:11 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 10:37:11 | Reward (progress к objective): d_before=26.627, d_after=25.060, delta=1.567, norm=0.261, bonus=+0.008
2026-03-09 10:37:11 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 10:37:11 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 10:37:11 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 10:37:11 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-09 10:37:11 | Итерация 0 завершена с наградой tensor([0.0078], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 10:37:11 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:37:11 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-09 10:37:12 | Модель победила!
2026-03-09 10:37:12 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 10:37:27 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-09 10:37:27 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-09 10:37:27 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-09 10:37:27 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-09 10:37:27 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 10:37:27 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 10:37:28 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-48-168877.pickle
2026-03-09 10:37:28 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-48-168877.pth
2026-03-09 10:37:28 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-09 10:37:29 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-03-09 10:37:29 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-09 10:37:29 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-09 10:37:29 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-09 10:37:29 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-09 10:37:29 | [DEPLOY] Order: model first, alternating
2026-03-09 10:37:29 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 10:37:29 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1142, coord=(19,2), attempt=1, reward=+0.017, score_before=0.000, score_after=0.343, reward_delta=+0.017, forward=0.037, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 10:37:29 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (19,2)
2026-03-09 10:37:29 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 10:37:30 | REQ: deploy cell accepted x=47, y=29
2026-03-09 10:37:30 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (29,47)
2026-03-09 10:37:30 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (29,47)
2026-03-09 10:37:30 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 10:37:30 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=2286, coord=(38,6), attempt=1, reward=-0.000, score_before=0.343, score_after=0.335, reward_delta=-0.000, forward=0.071, spread=1.000, edge=0.250, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 10:37:30 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (38,6)
2026-03-09 10:37:31 | REQ: deploy cell accepted x=47, y=20
2026-03-09 10:37:31 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,47)
2026-03-09 10:37:31 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,47)
2026-03-09 10:37:31 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.017 total_deploy_reward=+0.017 avg_forward=0.054 avg_spread=1.000 avg_edge=0.375 avg_cover=0.000
2026-03-09 10:37:31 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.016771777690185258, 'units': 2, 'total_deploy_reward': 0.016771777690185258, 'forward_sum': 0.10847457627118645, 'spread_sum': 2.0, 'edge_sum': 0.75, 'cover_sum': 0.0, 'avg_forward': 0.054237288135593226, 'avg_spread': 1.0, 'avg_edge': 0.375, 'avg_cover': 0.0}
2026-03-09 10:37:31 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-09 10:37:31 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-09 10:37:31 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-09 10:37:31 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:37:31 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-09 10:37:31 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 10:37:33 | === БОЕВОЙ РАУНД 1 ===
2026-03-09 10:37:33 | --- ХОД PLAYER ---
2026-03-09 10:37:33 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:37:33 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:37:33 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:37:34 | REQ: move cell accepted (RMB) x=36, y=30, mode=advance
2026-03-09 10:37:34 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:37:35 | REQ: move cell accepted (RMB) x=40, y=11, mode=advance
2026-03-09 10:37:36 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:37:36 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:37:36 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-09 10:37:36 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-09 10:37:36 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:37:36 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-09 10:37:36 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-09 10:37:36 | Нет доступных целей для чарджа.
2026-03-09 10:37:36 | --- ФАЗА БОЯ ---
2026-03-09 10:37:36 | --- ХОД MODEL ---
2026-03-09 10:37:36 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:37:36 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:37:36 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:37:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (19, 2). Выбор: up, advance=нет, distance=3
2026-03-09 10:37:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (16, 2)
2026-03-09 10:37:36 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:37:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (38, 6). Выбор: up, advance=нет, distance=1
2026-03-09 10:37:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (37, 6)
2026-03-09 10:37:36 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:37:36 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:37:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:37:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:37:36 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:37:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:37:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:37:36 | [MODEL] Чардж: нет доступных целей
2026-03-09 10:37:36 | --- ФАЗА БОЯ ---
2026-03-09 10:37:36 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 10:37:36 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=28.0178514522438->28.284271247461902
2026-03-09 10:37:36 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 10:37:36 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 10:37:36 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 10:37:36 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-09 10:37:36 | Итерация 0 завершена с наградой tensor([-0.0200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 10:37:36 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:37:36 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-09 10:37:38 | === БОЕВОЙ РАУНД 2 ===
2026-03-09 10:37:38 | --- ХОД PLAYER ---
2026-03-09 10:37:38 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:37:38 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:37:38 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:37:42 | REQ: move cell accepted (RMB) x=32, y=28, mode=normal
2026-03-09 10:37:42 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:37:44 | REQ: move cell accepted (RMB) x=29, y=19, mode=advance
2026-03-09 10:37:44 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:37:44 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:37:44 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-09 10:37:44 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:37:44 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-09 10:37:44 | Нет доступных целей для чарджа.
2026-03-09 10:37:44 | --- ФАЗА БОЯ ---
2026-03-09 10:37:44 | --- ХОД MODEL ---
2026-03-09 10:37:44 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:37:44 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 10:37:44 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:37:44 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (16, 2). Выбор: up, advance=нет, distance=3
2026-03-09 10:37:44 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (13, 2)
2026-03-09 10:37:44 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:37:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (37, 6). Выбор: up, advance=нет, distance=1
2026-03-09 10:37:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (36, 6)
2026-03-09 10:37:44 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:37:44 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:37:44 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:37:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:37:44 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:37:44 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:37:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:37:44 | [MODEL] Чардж: нет доступных целей
2026-03-09 10:37:44 | --- ФАЗА БОЯ ---
2026-03-09 10:37:44 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 10:37:44 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=28.284271247461902->28.844410203711913
2026-03-09 10:37:44 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 10:37:44 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 10:37:44 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 10:37:44 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-09 10:37:44 | Итерация 1 завершена с наградой tensor([-0.0200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 10:37:44 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 4, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:37:44 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 4, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0

2026-03-09 10:37:48 | === БОЕВОЙ РАУНД 3 ===
2026-03-09 10:37:48 | --- ХОД PLAYER ---
2026-03-09 10:37:48 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:37:48 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 10:37:48 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:38:13 | REQ: move cell accepted (RMB) x=32, y=30, mode=normal
2026-03-09 10:38:14 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:38:14 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:38:14 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-09 10:38:14 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-09 10:38:14 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 10:38:14 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:38:14 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:38:14 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-09 10:38:14 | Оружие: Gauss flayer
2026-03-09 10:38:14 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:38:14 | BS оружия: 4+
2026-03-09 10:38:14 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:38:14 | Save цели: 4+ (invul: нет)
2026-03-09 10:38:14 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:38:14 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:38:14 | Правило: Overwatch: попадания только на 6+
2026-03-09 10:38:14 | Hit rolls:    [1, 2, 4, 5, 5, 4, 4, 6, 2, 1]  -> hits: 6 (crits: 1)
2026-03-09 10:38:14 | Wound rolls:  [5]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 1 = 2
2026-03-09 10:38:14 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 10:38:14 | FX: найден итог урона = 0.0.
2026-03-09 10:38:14 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=0.0).
2026-03-09 10:38:14 | FX: позиция эффекта start=(156.0,876.0) end=(780.0,684.0).
2026-03-09 10:38:14 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-09 10:38:14 | 📌 -------------------------

2026-03-09 10:38:32 | Unit 12: movement skipped
2026-03-09 10:38:32 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:38:32 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:38:32 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-09 10:38:32 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-09 10:38:32 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 10:38:32 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:38:32 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:38:32 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 10:38:32 | Оружие: Gauss flayer
2026-03-09 10:38:32 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:38:32 | BS оружия: 4+
2026-03-09 10:38:32 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:38:32 | Save цели: 4+ (invul: нет)
2026-03-09 10:38:32 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:38:32 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:38:32 | Правило: Overwatch: попадания только на 6+
2026-03-09 10:38:32 | Hit rolls:    [3, 1, 5, 3, 6, 5, 2, 1, 1, 1]  -> hits: 3 (crits: 1)
2026-03-09 10:38:32 | Wound rolls:  [4]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 1 = 2
2026-03-09 10:38:32 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 10:38:32 | FX: найден итог урона = 0.0.
2026-03-09 10:38:32 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-09 10:38:32 | FX: позиция эффекта start=(60.0,324.0) end=(708.0,468.0).
2026-03-09 10:38:32 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-09 10:38:32 | 📌 -------------------------

2026-03-09 10:38:32 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:38:45 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:38:50 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 10:38:53 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:38:53 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 10:38:53 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 10:38:53 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:38:53 | FX: найдена строка стрельбы (attacker=11, target=22).
2026-03-09 10:38:53 | Оружие: Gauss flayer
2026-03-09 10:38:53 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:38:53 | BS оружия: 4+
2026-03-09 10:38:53 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:38:53 | Save цели: 4+ (invul: нет)
2026-03-09 10:38:53 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:38:53 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:38:53 | Hit rolls:    [1, 1, 1, 1, 2, 3, 4, 5, 1, 1]  -> hits: 2
2026-03-09 10:38:53 | Wound rolls:  [1, 1]  (цель 4+) -> wounds: 0
2026-03-09 10:38:53 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 10:38:53 | FX: найден итог урона = 0.0.
2026-03-09 10:38:53 | FX: создан FxShotEvent (attacker=11, target=22, weapon=Gauss flayer, damage=0.0).
2026-03-09 10:38:53 | FX: позиция эффекта start=(756.0,708.0) end=(156.0,876.0).
2026-03-09 10:38:53 | FX: эффект добавлен в рендер (attacker=11, target=22).
2026-03-09 10:38:53 | 📌 -------------------------

2026-03-09 10:38:53 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-09 10:38:53 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 10:38:53 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:38:53 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 10:38:53 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:38:53 | FX: найден итог урона = 0.0.
2026-03-09 10:38:53 | FX: дубликат отчёта, эффект не создаём.
