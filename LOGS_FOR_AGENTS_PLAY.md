2026-03-09 10:49:26 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-09 10:49:26 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-09 10:49:26 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-09 10:49:26 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-09 10:49:26 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 10:49:26 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:49:26 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 10:49:26 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:49:26 | FX: найден итог урона = 0.0.
2026-03-09 10:49:26 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-09 10:49:26 | FX: позиция эффекта start=(60.0,324.0) end=(684.0,444.0).
2026-03-09 10:49:26 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-09 10:49:26 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 10:49:28 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-26-521961.pickle
2026-03-09 10:49:28 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-26-521961.pth
2026-03-09 10:49:28 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-09 10:49:31 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-03-09 10:49:31 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-09 10:49:31 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-09 10:49:31 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-09 10:49:31 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-09 10:49:31 | [DEPLOY] Order: model first, alternating
2026-03-09 10:49:31 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 10:49:31 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=245, coord=(4,5), attempt=1, reward=+0.021, score_before=0.000, score_after=0.413, reward_delta=+0.021, forward=0.088, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 10:49:31 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (4,5)
2026-03-09 10:49:31 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 10:49:32 | REQ: deploy cell accepted x=52, y=29
2026-03-09 10:49:32 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (29,52)
2026-03-09 10:49:32 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (29,52)
2026-03-09 10:49:32 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 10:49:32 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=841, coord=(14,1), attempt=1, reward=-0.003, score_before=0.413, score_after=0.351, reward_delta=-0.003, forward=0.054, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 10:49:32 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (14,1)
2026-03-09 10:49:32 | REQ: deploy cell accepted x=51, y=22
2026-03-09 10:49:33 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,51)
2026-03-09 10:49:33 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,51)
2026-03-09 10:49:33 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.018 total_deploy_reward=+0.018 avg_forward=0.071 avg_spread=1.000 avg_edge=0.750 avg_cover=0.000
2026-03-09 10:49:33 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.017540402049664963, 'units': 2, 'total_deploy_reward': 0.017540402049664963, 'forward_sum': 0.1423728813559322, 'spread_sum': 2.0, 'edge_sum': 1.5, 'cover_sum': 0.0, 'avg_forward': 0.0711864406779661, 'avg_spread': 1.0, 'avg_edge': 0.75, 'avg_cover': 0.0}
2026-03-09 10:49:33 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-09 10:49:33 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-09 10:49:33 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-09 10:49:33 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:49:33 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-09 10:49:33 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 10:49:34 | === БОЕВОЙ РАУНД 1 ===
2026-03-09 10:49:34 | --- ХОД PLAYER ---
2026-03-09 10:49:34 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:49:34 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:49:34 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:49:36 | REQ: move cell accepted (RMB) x=41, y=30, mode=advance
2026-03-09 10:49:37 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:49:37 | REQ: move cell accepted (RMB) x=40, y=23, mode=advance
2026-03-09 10:49:38 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:49:38 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:49:38 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-09 10:49:38 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-09 10:49:38 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:49:38 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-09 10:49:38 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-09 10:49:38 | Нет доступных целей для чарджа.
2026-03-09 10:49:38 | --- ФАЗА БОЯ ---
2026-03-09 10:49:38 | --- ХОД MODEL ---
2026-03-09 10:49:38 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:49:38 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:49:38 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:49:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (4, 5). Выбор: up, advance=нет, distance=4
2026-03-09 10:49:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 5)
2026-03-09 10:49:38 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:49:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (14, 1). Выбор: up, advance=да, бросок=4, макс=9, distance=9
2026-03-09 10:49:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (5, 1)
2026-03-09 10:49:38 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:49:38 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:49:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:49:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-09 10:49:38 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:49:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:49:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-09 10:49:38 | [MODEL] Чардж: нет доступных целей
2026-03-09 10:49:38 | --- ФАЗА БОЯ ---
2026-03-09 10:49:38 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 10:49:38 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.614185789921695->32.01562118716424
2026-03-09 10:49:38 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 10:49:38 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 10:49:38 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 10:49:38 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-09 10:49:38 | Итерация 0 завершена с наградой tensor([-0.0200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 10:49:38 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:49:38 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-09 10:49:39 | === БОЕВОЙ РАУНД 2 ===
2026-03-09 10:49:39 | --- ХОД PLAYER ---
2026-03-09 10:49:39 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:49:39 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:49:39 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:49:40 | REQ: move cell accepted (RMB) x=31, y=25, mode=advance
2026-03-09 10:49:41 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:49:41 | REQ: move cell accepted (RMB) x=31, y=19, mode=advance
2026-03-09 10:49:41 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:49:41 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:49:41 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-09 10:49:41 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-09 10:49:41 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:49:41 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-09 10:49:41 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-09 10:49:41 | Нет доступных целей для чарджа.
2026-03-09 10:49:41 | --- ФАЗА БОЯ ---
2026-03-09 10:49:41 | --- ХОД MODEL ---
2026-03-09 10:49:41 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:49:41 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 10:49:41 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:49:41 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 4). Выбор: left, advance=нет, distance=4
2026-03-09 10:49:41 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 0)
2026-03-09 10:49:41 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:49:41 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (5, 1). Выбор: left, advance=нет, distance=1
2026-03-09 10:49:41 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (5, 0)
2026-03-09 10:49:41 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:49:41 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:49:41 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:49:41 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:49:41 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:49:41 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:49:41 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:49:41 | [MODEL] Чардж: нет доступных целей
2026-03-09 10:49:41 | --- ФАЗА БОЯ ---
2026-03-09 10:49:41 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 10:49:41 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=32.202484376209235->33.54101966249684
2026-03-09 10:49:41 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 10:49:41 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 10:49:41 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 10:49:41 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-09 10:49:41 | Итерация 1 завершена с наградой tensor([-0.0200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 10:49:41 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 4, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:49:41 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 4, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0

2026-03-09 10:49:43 | === БОЕВОЙ РАУНД 3 ===
2026-03-09 10:49:43 | --- ХОД PLAYER ---
2026-03-09 10:49:43 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:49:43 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 10:49:43 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:49:44 | REQ: move cell accepted (RMB) x=26, y=23, mode=normal
2026-03-09 10:49:44 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:49:45 | REQ: move cell accepted (RMB) x=26, y=16, mode=normal
2026-03-09 10:49:45 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:49:45 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:49:45 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:49:45 | Нет доступных целей для чарджа.
2026-03-09 10:49:45 | --- ФАЗА БОЯ ---
2026-03-09 10:49:45 | --- ХОД MODEL ---
2026-03-09 10:49:45 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:49:45 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 10:49:45 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:49:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 1). Выбор: left, advance=нет, distance=1
2026-03-09 10:49:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 0)
2026-03-09 10:49:45 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:49:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (4, 1). Выбор: left, advance=нет, distance=1
2026-03-09 10:49:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (4, 0)
2026-03-09 10:49:45 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:49:45 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:49:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:49:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:49:45 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:49:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:49:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:49:45 | [MODEL] Чардж: нет доступных целей
2026-03-09 10:49:45 | --- ФАЗА БОЯ ---
2026-03-09 10:49:45 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 10:49:45 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-03-09 10:49:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=33.12099032335839->34.0
2026-03-09 10:49:45 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 10:49:45 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 10:49:45 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 10:49:45 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-09 10:49:45 | Итерация 2 завершена с наградой tensor([-0.0700], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 10:49:45 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 6, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 1, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:49:45 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 6, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 1

2026-03-09 10:49:47 | === БОЕВОЙ РАУНД 4 ===
2026-03-09 10:49:47 | --- ХОД PLAYER ---
2026-03-09 10:49:47 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:49:47 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 1 -> 2, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 10:49:47 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:49:48 | REQ: move cell accepted (RMB) x=23, y=22, mode=normal
2026-03-09 10:49:49 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:49:49 | REQ: move cell accepted (RMB) x=25, y=13, mode=normal
2026-03-09 10:49:50 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:49:50 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:49:50 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 10:49:50 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-09 10:49:50 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 10:49:50 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:49:50 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:49:50 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 10:49:50 | Оружие: Gauss flayer
2026-03-09 10:49:50 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:49:50 | BS оружия: 4+
2026-03-09 10:49:50 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:49:50 | Save цели: 4+ (invul: нет)
2026-03-09 10:49:50 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:49:50 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:49:50 | Правило: Overwatch: попадания только на 6+
2026-03-09 10:49:50 | Hit rolls:    [6, 2, 2, 1, 5, 3, 4, 6, 5, 2]  -> hits: 5 (crits: 2)
2026-03-09 10:49:50 | Wound rolls:  [5, 6]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 2 = 4
2026-03-09 10:49:50 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 10:49:50 | FX: найден итог урона = 0.0.
2026-03-09 10:49:50 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-09 10:49:50 | FX: позиция эффекта start=(36.0,36.0) end=(636.0,396.0).
2026-03-09 10:49:50 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-09 10:49:50 | 📌 -------------------------

2026-03-09 10:49:50 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:50:59 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:51:05 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 10:51:06 | 
🎲 Бросок сейвы (save): 1D6
2026-03-09 10:52:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (overwatch)
2026-03-09 10:52:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-09 10:52:53 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 1.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:52:53 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 10:52:53 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 10:52:53 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:52:53 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-03-09 10:52:53 | Оружие: Gauss flayer
2026-03-09 10:52:53 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:52:53 | BS оружия: 4+
2026-03-09 10:52:53 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:52:53 | Save цели: 4+ (invul: нет)
2026-03-09 10:52:53 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:52:53 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:52:53 | Hit rolls:    [1, 2, 3, 4, 5, 6, 1, 1, 1, 1]  -> hits: 3 (crits: 1)
2026-03-09 10:52:53 | Wound rolls:  [1, 2]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 1 = 1
2026-03-09 10:52:53 | Save rolls:   [1]  (цель 4+) -> failed saves: 1
2026-03-09 10:52:53 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 10:52:53 | FX: найден итог урона = 1.0.
2026-03-09 10:52:53 | FX: создан FxShotEvent (attacker=12, target=22, weapon=Gauss flayer, damage=1.0).
2026-03-09 10:52:53 | FX: позиция эффекта start=(612.0,324.0) end=(36.0,108.0).
2026-03-09 10:52:53 | FX: эффект добавлен в рендер (attacker=12, target=22).
2026-03-09 10:52:53 | 📌 -------------------------

2026-03-09 10:52:53 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:52:53 | Нет доступных целей для чарджа.
2026-03-09 10:52:53 | --- ФАЗА БОЯ ---
2026-03-09 10:52:53 | --- ХОД MODEL ---
2026-03-09 10:52:53 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:52:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 10:52:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-09 10:52:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-09 10:52:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 10:52:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-09 10:52:53 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:52:53 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:52:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 1). Выбор: left, advance=нет, distance=1
2026-03-09 10:52:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 0)
2026-03-09 10:52:53 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:52:55 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (4, 1). Выбор: left, advance=нет, distance=1
2026-03-09 10:52:55 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (4, 0)
2026-03-09 10:52:55 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:52:56 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:52:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-09 10:52:56 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:52:56 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-09 10:52:56 | 
🎲 Бросок сейвы (save): 6D6
2026-03-09 10:52:56 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (shooting)
2026-03-09 10:52:56 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-09 10:52:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-03-09 10:52:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-09 10:52:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-09 10:52:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.140
2026-03-09 10:52:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 3.0
2026-03-09 10:52:56 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 10:52:56 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 10:52:56 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:52:56 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 10:52:56 | Оружие: Gauss flayer
2026-03-09 10:52:56 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:52:56 | BS оружия: 4+
2026-03-09 10:52:56 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:52:56 | Save цели: 4+ (invul: нет)
2026-03-09 10:52:56 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:52:56 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:52:56 | Hit rolls:    [5, 1, 5, 6, 4, 5, 2, 5, 6, 1]  -> hits: 7 (crits: 2)
2026-03-09 10:52:56 | Wound rolls:  [5, 1, 4, 4, 6]  (цель 4+) -> rolled wounds: 4 + auto(w/LETHAL): 2 = 6
2026-03-09 10:52:56 | Save rolls:   [1, 3, 2, 4, 6, 4]  (цель 4+) -> failed saves: 3
2026-03-09 10:52:56 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-09 10:52:56 | FX: найден итог урона = 3.0.
2026-03-09 10:52:56 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=3.0).
2026-03-09 10:52:56 | FX: позиция эффекта start=(36.0,36.0) end=(612.0,324.0).
2026-03-09 10:52:56 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-09 10:52:56 | 📌 -------------------------

2026-03-09 10:52:56 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-09 10:52:56 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:52:56 | 
🎲 Бросок на ранение (to wound): 7D6
2026-03-09 10:52:56 | 
🎲 Бросок сейвы (save): 4D6
2026-03-09 10:52:56 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 5. HP: 7.0 -> 5.0 (shooting)
2026-03-09 10:52:56 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-03-09 10:52:56 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-09 10:52:56 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-09 10:52:56 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-09 10:52:56 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.110
2026-03-09 10:52:56 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-09 10:52:56 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 10:52:56 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 10:52:56 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:52:56 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-09 10:52:56 | Оружие: Gauss flayer
2026-03-09 10:52:56 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:52:56 | BS оружия: 4+
2026-03-09 10:52:56 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:52:56 | Save цели: 4+ (invul: нет)
2026-03-09 10:52:56 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:52:56 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:52:56 | Hit rolls:    [5, 4, 3, 5, 1, 1, 5, 5, 4, 4]  -> hits: 7
2026-03-09 10:52:56 | Wound rolls:  [6, 5, 6, 2, 1, 4, 2]  (цель 4+) -> wounds: 4
2026-03-09 10:52:56 | Save rolls:   [3, 4, 2, 6]  (цель 4+) -> failed saves: 2
2026-03-09 10:52:56 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-09 10:52:56 | FX: найден итог урона = 2.0.
2026-03-09 10:52:56 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=2.0).
2026-03-09 10:52:56 | FX: позиция эффекта start=(36.0,108.0) end=(612.0,324.0).
2026-03-09 10:52:56 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-09 10:52:56 | 📌 -------------------------

2026-03-09 10:52:56 | Reward (шаг): стрельба delta=+0.250
2026-03-09 10:52:56 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:52:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:52:56 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:52:56 | [MODEL] Чардж: нет доступных целей
2026-03-09 10:52:56 | --- ФАЗА БОЯ ---
2026-03-09 10:52:56 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 10:52:56 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-03-09 10:52:56 | Reward (terrain/potential): gamma=0.990, phi_before=-0.033, phi_after=-0.017, delta=+0.017; cover=0.000->0.000, threat=-0.333->-0.167, guard=0.000->0.000
2026-03-09 10:52:56 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=1)
2026-03-09 10:52:56 | Reward (terrain/clamp): raw=+0.007, cap=±0.120, clamp не сработал
2026-03-09 10:52:56 | === КОНЕЦ БОЕВОГО РАУНДА 4 ===
2026-03-09 10:52:56 | Итерация 3 завершена с наградой tensor([0.2068], device='cuda:0'), здоровье игрока [10.0, 5.0], здоровье модели [10.0, 10.0]
2026-03-09 10:52:56 | {'model health': [10.0, 10.0], 'player health': [10.0, 5.0], 'model alive models': [10, 10], 'player alive models': [10, 5], 'modelCP': 7, 'playerCP': 8, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 2, 'mission': 'Only War', 'turn': 5, 'battle round': 5, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:52:56 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 5.0]
CP MODEL: 7, CP PLAYER: 8
VP MODEL: 0, VP PLAYER: 2
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 3.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)

2026-03-09 10:52:59 | === БОЕВОЙ РАУНД 5 ===
2026-03-09 10:52:59 | --- ХОД PLAYER ---
2026-03-09 10:52:59 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:52:59 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 10:53:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 10:53:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=5, раны=[1, 1, 1, 1, 1] всего=5
2026-03-09 10:53:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 10:53:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-03-09 10:53:00 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 2 -> 2; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:53:00 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:53:02 | REQ: move cell accepted (RMB) x=21, y=20, mode=normal
2026-03-09 10:53:03 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:53:03 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:53:03 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 10:53:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-09 10:53:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-09 10:53:03 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-09 10:53:03 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 10:53:03 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:53:03 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:53:03 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-09 10:53:03 | Оружие: Gauss flayer
2026-03-09 10:53:03 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:53:03 | BS оружия: 4+
2026-03-09 10:53:03 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:53:03 | Save цели: 4+ (invul: нет)
2026-03-09 10:53:03 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:53:03 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:53:03 | Правило: Overwatch: попадания только на 6+
2026-03-09 10:53:03 | Hit rolls:    [3, 6, 1, 6, 3, 3, 2, 3, 5, 3]  -> hits: 3 (crits: 2)
2026-03-09 10:53:03 | Wound rolls:  [3, 5]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-09 10:53:03 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 10:53:03 | FX: найден итог урона = 1.0.
2026-03-09 10:53:03 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-09 10:53:03 | FX: позиция эффекта start=(36.0,108.0) end=(564.0,540.0).
2026-03-09 10:53:03 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-09 10:53:03 | 📌 -------------------------

2026-03-09 10:53:11 | Unit 12: movement skipped
2026-03-09 10:53:11 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:53:11 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:53:11 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-09 10:53:11 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-09 10:53:11 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 10:53:11 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:53:11 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:53:11 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 10:53:11 | Оружие: Gauss flayer
2026-03-09 10:53:11 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:53:11 | BS оружия: 4+
2026-03-09 10:53:11 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:53:11 | Save цели: 4+ (invul: нет)
2026-03-09 10:53:11 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:53:11 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:53:11 | Правило: Overwatch: попадания только на 6+
2026-03-09 10:53:11 | Hit rolls:    [1, 1, 6, 2, 3, 3, 2, 1, 5, 2]  -> hits: 2 (crits: 1)
2026-03-09 10:53:11 | Wound rolls:  [6]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 1 = 2
2026-03-09 10:53:11 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 10:53:11 | FX: найден итог урона = 0.0.
2026-03-09 10:53:11 | FX: дубликат отчёта, эффект не создаём.
2026-03-09 10:53:11 | 📌 -------------------------

2026-03-09 10:53:11 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:53:11 | REQ: shooter changed Unit 12->Unit 11, target reset
2026-03-09 10:53:28 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-09 10:53:32 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-09 10:53:34 | 
🎲 Бросок сейвы (save): 2D6
2026-03-09 10:53:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (overwatch)
2026-03-09 10:53:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-09 10:53:38 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 2.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:53:38 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 10:53:38 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 10:53:38 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:53:38 | FX: найдена строка стрельбы (attacker=11, target=22).
2026-03-09 10:53:38 | Оружие: Gauss flayer
2026-03-09 10:53:38 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:53:38 | BS оружия: 4+
2026-03-09 10:53:38 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:53:38 | Save цели: 4+ (invul: нет)
2026-03-09 10:53:38 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:53:38 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:53:38 | Hit rolls:    [2, 3, 4, 5, 6, 1, 2, 3, 4]  -> hits: 4 (crits: 1)
2026-03-09 10:53:38 | Wound rolls:  [3, 4, 1]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 1 = 2
2026-03-09 10:53:38 | Save rolls:   [2, 3]  (цель 4+) -> failed saves: 2
2026-03-09 10:53:38 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-09 10:53:38 | FX: найден итог урона = 2.0.
2026-03-09 10:53:38 | FX: создан FxShotEvent (attacker=11, target=22, weapon=Gauss flayer, damage=2.0).
2026-03-09 10:53:38 | FX: позиция эффекта start=(516.0,492.0) end=(36.0,108.0).
2026-03-09 10:53:38 | FX: эффект добавлен в рендер (attacker=11, target=22).
2026-03-09 10:53:38 | 📌 -------------------------

2026-03-09 10:53:38 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-09 10:53:38 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 10:53:38 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:53:38 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 10:53:38 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:53:38 | FX: найден итог урона = 0.0.
2026-03-09 10:53:38 | FX: дубликат отчёта, эффект не создаём.
2026-03-09 10:57:04 | 
🎲 Бросок на попадание (to hit): 6D6
2026-03-09 10:57:10 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:57:10 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 10:57:10 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 10:57:10 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:57:10 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-03-09 10:57:10 | Оружие: Gauss flayer
2026-03-09 10:57:10 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:57:10 | BS оружия: 4+
2026-03-09 10:57:10 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:57:10 | Save цели: 4+ (invul: нет)
2026-03-09 10:57:10 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:57:10 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:57:10 | Hit rolls:    [1, 1, 1, 1, 1, 1]  -> hits: 0
2026-03-09 10:57:10 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 10:57:10 | FX: найден итог урона = 0.0.
2026-03-09 10:57:10 | FX: создан FxShotEvent (attacker=12, target=22, weapon=Gauss flayer, damage=0.0).
2026-03-09 10:57:10 | FX: позиция эффекта start=(588.0,300.0) end=(36.0,108.0).
2026-03-09 10:57:10 | FX: эффект добавлен в рендер (attacker=12, target=22).
2026-03-09 10:57:10 | 📌 -------------------------

2026-03-09 10:57:10 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:57:10 | Нет доступных целей для чарджа.
2026-03-09 10:57:10 | --- ФАЗА БОЯ ---
2026-03-09 10:57:10 | --- ХОД MODEL ---
2026-03-09 10:57:10 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:57:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 10:57:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-09 10:57:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-09 10:57:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 10:57:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 10:57:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-09 10:57:10 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:57:10 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:57:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 1). Выбор: up, advance=нет, distance=1
2026-03-09 10:57:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 1)
2026-03-09 10:57:10 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:57:12 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (4, 1). Выбор: up, advance=нет, distance=3
2026-03-09 10:57:12 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 1)
2026-03-09 10:57:12 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:57:13 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:57:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-09 10:57:13 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:57:13 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-09 10:57:13 | 
🎲 Бросок сейвы (save): 3D6
2026-03-09 10:57:13 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 5. HP: 6.0 -> 5.0 (shooting)
2026-03-09 10:57:13 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-03-09 10:57:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-09 10:57:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-09 10:57:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-09 10:57:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-09 10:57:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-09 10:57:13 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 10:57:13 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 10:57:13 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:57:13 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 10:57:13 | Оружие: Gauss flayer
2026-03-09 10:57:13 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:57:13 | BS оружия: 4+
2026-03-09 10:57:13 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:57:13 | Save цели: 4+ (invul: нет)
2026-03-09 10:57:13 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:57:13 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:57:13 | Hit rolls:    [4, 4, 1, 5, 5, 4, 2, 1, 6, 6]  -> hits: 7 (crits: 2)
2026-03-09 10:57:13 | Wound rolls:  [2, 2, 1, 5, 2]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-09 10:57:13 | Save rolls:   [5, 1, 6]  (цель 4+) -> failed saves: 1
2026-03-09 10:57:13 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 10:57:13 | FX: найден итог урона = 1.0.
2026-03-09 10:57:13 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-09 10:57:13 | FX: позиция эффекта start=(36.0,36.0) end=(588.0,300.0).
2026-03-09 10:57:13 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-09 10:57:13 | 📌 -------------------------

2026-03-09 10:57:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: выбор политики)
2026-03-09 10:57:13 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:57:13 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-09 10:57:13 | 
🎲 Бросок сейвы (save): 3D6
2026-03-09 10:57:13 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 8. HP: 9.0 -> 8.0 (shooting)
2026-03-09 10:57:13 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-09 10:57:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-09 10:57:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-09 10:57:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=18, need<=3).
2026-03-09 10:57:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-09 10:57:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-09 10:57:13 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 10:57:13 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 10:57:13 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:57:13 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-09 10:57:13 | Оружие: Gauss flayer
2026-03-09 10:57:13 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:57:13 | BS оружия: 4+
2026-03-09 10:57:13 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:57:13 | Save цели: 4+ (invul: нет)
2026-03-09 10:57:13 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:57:13 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:57:13 | Hit rolls:    [2, 4, 4, 4, 3, 4, 3, 3, 6, 5]  -> hits: 6 (crits: 1)
2026-03-09 10:57:13 | Wound rolls:  [5, 2, 3, 2, 4]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 1 = 3
2026-03-09 10:57:13 | Save rolls:   [6, 6, 1]  (цель 4+) -> failed saves: 1
2026-03-09 10:57:13 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 10:57:13 | FX: найден итог урона = 1.0.
2026-03-09 10:57:13 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-09 10:57:13 | FX: позиция эффекта start=(36.0,108.0) end=(516.0,492.0).
2026-03-09 10:57:13 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-09 10:57:13 | 📌 -------------------------

2026-03-09 10:57:13 | Reward (шаг): стрельба delta=+0.160
2026-03-09 10:57:13 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:57:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:57:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:57:13 | [MODEL] Чардж: нет доступных целей
2026-03-09 10:57:13 | --- ФАЗА БОЯ ---
2026-03-09 10:57:13 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 10:57:13 | Reward (progress к objective): d_before=33.121, d_after=31.064, delta=2.057, norm=0.343, bonus=+0.010
2026-03-09 10:57:13 | Reward (terrain/potential): gamma=0.990, phi_before=-0.050, phi_after=-0.050, delta=+0.001; cover=0.000->0.000, threat=-0.500->-0.500, guard=0.000->0.000
2026-03-09 10:57:13 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=3)
2026-03-09 10:57:13 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-09 10:57:13 | === КОНЕЦ БОЕВОГО РАУНДА 5 ===
2026-03-09 10:57:13 | Итерация 4 завершена с наградой tensor([0.1508], device='cuda:0'), здоровье игрока [8.0, 5.0], здоровье модели [10.0, 10.0]
2026-03-09 10:57:13 | {'model health': [10.0, 10.0], 'player health': [8.0, 5.0], 'model alive models': [10, 10], 'player alive models': [8, 5], 'modelCP': 7, 'playerCP': 10, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 2, 'mission': 'Only War', 'turn': 6, 'battle round': 6, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:57:13 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [8.0, 5.0]
CP MODEL: 7, CP PLAYER: 10
VP MODEL: 0, VP PLAYER: 2
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-03-09 10:57:14 | === БОЕВОЙ РАУНД 6 ===
2026-03-09 10:57:14 | --- ХОД PLAYER ---
2026-03-09 10:57:14 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:57:14 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 10:57:15 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 10:57:15 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-09 10:57:15 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 10:57:15 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-09 10:57:15 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 10:57:16 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 10:57:16 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=5, раны=[1, 1, 1, 1, 1] всего=5
2026-03-09 10:57:16 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 10:57:16 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-03-09 10:57:16 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 2 -> 2; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:57:16 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:57:18 | Unit 11: movement skipped
2026-03-09 10:57:18 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:57:18 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:57:18 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 10:57:18 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 8. HP: 9.0 -> 8.0 (Overwatch)
2026-03-09 10:57:18 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-09 10:57:18 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-09 10:57:18 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 10:57:18 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:57:18 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:57:18 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-09 10:57:18 | Оружие: Gauss flayer
2026-03-09 10:57:18 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:57:18 | BS оружия: 4+
2026-03-09 10:57:18 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:57:18 | Save цели: 4+ (invul: нет)
2026-03-09 10:57:18 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:57:18 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:57:18 | Правило: Overwatch: попадания только на 6+
2026-03-09 10:57:18 | Hit rolls:    [2, 6, 3, 2, 6, 5, 4, 1, 3, 1]  -> hits: 4 (crits: 2)
2026-03-09 10:57:18 | Wound rolls:  [3, 5]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-09 10:57:18 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 10:57:18 | FX: найден итог урона = 1.0.
2026-03-09 10:57:18 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-09 10:57:18 | FX: позиция эффекта start=(36.0,36.0) end=(516.0,492.0).
2026-03-09 10:57:18 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-09 10:57:18 | 📌 -------------------------

2026-03-09 10:57:21 | Unit 12: movement skipped
2026-03-09 10:57:22 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:57:22 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:57:22 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 10:57:22 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 5. HP: 6.0 -> 5.0 (Overwatch)
2026-03-09 10:57:22 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-03-09 10:57:22 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-09 10:57:22 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 10:57:22 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:57:22 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:57:22 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 10:57:22 | Оружие: Gauss flayer
2026-03-09 10:57:22 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:57:22 | BS оружия: 4+
2026-03-09 10:57:22 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:57:22 | Save цели: 4+ (invul: нет)
2026-03-09 10:57:22 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:57:22 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:57:22 | Правило: Overwatch: попадания только на 6+
2026-03-09 10:57:22 | Hit rolls:    [1, 6, 5, 5, 3, 3, 5, 6, 3, 3]  -> hits: 5 (crits: 2)
2026-03-09 10:57:22 | Wound rolls:  [6, 3]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-09 10:57:22 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 10:57:22 | FX: найден итог урона = 1.0.
2026-03-09 10:57:22 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-09 10:57:22 | FX: позиция эффекта start=(36.0,36.0) end=(588.0,300.0).
2026-03-09 10:57:22 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-09 10:57:22 | 📌 -------------------------

2026-03-09 10:57:22 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:57:22 | REQ: shooter changed Unit 12->Unit 11, target reset
