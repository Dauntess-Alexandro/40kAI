2026-03-03 10:16:11 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-03 10:16:11 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-03 10:16:11 | [VIEWER][TERRAIN] features=2
2026-03-03 10:16:11 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-03 10:16:12 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-03 10:16:23 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-38-633399.pickle
2026-03-03 10:16:23 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-38-633399.pth
2026-03-03 10:16:23 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-03 10:16:26 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-03-03 10:16:26 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-03 10:16:26 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-03 10:16:26 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-03 10:16:26 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-03 10:16:26 | [DEPLOY] Order: model first, alternating
2026-03-03 10:16:26 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.150
2026-03-03 10:16:26 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=432, coord=(7,12), attempt=1, reward=+0.026, score_before=0.000, score_after=0.516, reward_delta=+0.026, forward=0.207, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-03 10:16:26 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (7,12)
2026-03-03 10:16:26 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-03 10:16:27 | REQ: deploy cell accepted x=57, y=31
2026-03-03 10:16:27 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (31,57)
2026-03-03 10:16:27 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (31,57)
2026-03-03 10:16:27 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.150
2026-03-03 10:16:27 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=549, coord=(9,9), attempt=1, reward=-0.011, score_before=0.516, score_after=0.298, reward_delta=-0.011, forward=0.181, spread=0.333, edge=1.000, cover=0.000, cover_near=0.000, congestion=1.000, final_cover=0.000
2026-03-03 10:16:27 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (9,9)
2026-03-03 10:16:27 | REQ: deploy cell accepted x=54, y=21
2026-03-03 10:16:28 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,54)
2026-03-03 10:16:28 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,54)
2026-03-03 10:16:28 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.015 total_deploy_reward=+0.015 avg_forward=0.194 avg_spread=0.667 avg_edge=1.000 avg_cover=0.000
2026-03-03 10:16:28 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.014906562364189482, 'units': 2, 'total_deploy_reward': 0.014906562364189482, 'forward_sum': 0.38813559322033897, 'spread_sum': 1.3333333333333333, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.19406779661016949, 'avg_spread': 0.6666666666666666, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-03 10:16:28 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-03 10:16:28 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-03 10:16:28 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-03 10:16:28 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-03 10:16:28 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-03 10:16:28 | FX: перепроигрываю 30 строк(и) лога.
2026-03-03 10:16:32 | === БОЕВОЙ РАУНД 1 ===
2026-03-03 10:16:32 | --- ХОД PLAYER ---
2026-03-03 10:16:32 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-03 10:16:32 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-03 10:16:32 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-03 10:16:38 | Бросок 1D6 на Advance...
2026-03-03 10:16:39 | Бросок: 5
2026-03-03 10:16:41 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-03 10:16:44 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-03 10:16:44 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-03 10:16:44 | --- ФАЗА ЧАРДЖА ---
2026-03-03 10:16:44 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-03 10:16:44 | Нет доступных целей для чарджа.
2026-03-03 10:16:44 | --- ФАЗА БОЯ ---
2026-03-03 10:16:44 | --- ХОД MODEL ---
2026-03-03 10:16:44 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-03 10:16:44 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-03 10:16:44 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-03 10:16:44 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (7, 12). Выбор: right, advance=да, бросок=4, макс=9, distance=9
2026-03-03 10:16:44 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (7, 21)
2026-03-03 10:16:44 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-03 10:16:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (9, 9). Выбор: right, advance=нет, distance=3
2026-03-03 10:16:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (9, 12)
2026-03-03 10:16:44 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-03 10:16:44 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-03 10:16:44 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-03 10:16:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-03 10:16:44 | --- ФАЗА ЧАРДЖА ---
2026-03-03 10:16:44 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-03 10:16:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-03 10:16:44 | [MODEL] Чардж: нет доступных целей
2026-03-03 10:16:44 | --- ФАЗА БОЯ ---
2026-03-03 10:16:44 | [MODEL] Ближний бой: нет доступных атак
2026-03-03 10:16:44 | Reward (progress к objective): d_before=22.204, d_after=15.811, delta=6.392, norm=1.065, bonus=+0.032
2026-03-03 10:16:44 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-03 10:16:44 | Итерация 0 завершена с наградой tensor([0.0320], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-03 10:16:44 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-03 10:16:44 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-03 10:16:44 | === БОЕВОЙ РАУНД 2 ===
2026-03-03 10:16:44 | --- ХОД PLAYER ---
2026-03-03 10:16:44 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-03 10:16:44 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-03 10:16:44 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-03 10:16:49 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-03 10:16:51 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-03 10:16:51 | --- ФАЗА ЧАРДЖА ---
2026-03-03 10:16:51 | Нет доступных целей для чарджа.
2026-03-03 10:16:51 | --- ФАЗА БОЯ ---
2026-03-03 10:16:51 | --- ХОД MODEL ---
2026-03-03 10:16:51 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-03 10:16:51 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-03 10:16:51 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-03 10:16:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (7, 21). Выбор: right, advance=нет, distance=4
2026-03-03 10:16:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (7, 25)
2026-03-03 10:16:51 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-03 10:16:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (9, 12). Выбор: right, advance=нет, distance=1
2026-03-03 10:16:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (9, 13)
2026-03-03 10:16:51 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-03 10:16:51 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-03 10:16:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-03 10:16:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-03 10:16:51 | --- ФАЗА ЧАРДЖА ---
2026-03-03 10:16:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-03 10:16:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-03 10:16:51 | [MODEL] Чардж: нет доступных целей
2026-03-03 10:16:51 | --- ФАЗА БОЯ ---
2026-03-03 10:16:51 | [MODEL] Ближний бой: нет доступных атак
2026-03-03 10:16:51 | Reward (progress к objective): d_before=15.811, d_after=13.928, delta=1.883, norm=0.314, bonus=+0.009
2026-03-03 10:16:51 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-03 10:16:51 | Итерация 1 завершена с наградой tensor([0.0094], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-03 10:16:51 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 4, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-03 10:16:51 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 4, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0

2026-03-03 10:16:52 | === БОЕВОЙ РАУНД 3 ===
2026-03-03 10:16:52 | --- ХОД PLAYER ---
2026-03-03 10:16:52 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-03 10:16:52 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-03 10:16:52 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-03 10:16:56 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-03 10:16:59 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-03 10:16:59 | --- ФАЗА ЧАРДЖА ---
2026-03-03 10:16:59 | Нет доступных целей для чарджа.
2026-03-03 10:16:59 | --- ФАЗА БОЯ ---
2026-03-03 10:16:59 | --- ХОД MODEL ---
2026-03-03 10:16:59 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-03 10:16:59 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-03 10:16:59 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-03 10:16:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=13.928, d_after=13.928, d_best=2.928, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-03 10:16:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (7, 25). Выбор: none, advance=нет, distance=0
2026-03-03 10:16:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (7, 25)
2026-03-03 10:16:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=20.248, d_after=20.248, d_best=9.248, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-03 10:16:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (9, 13). Выбор: none, advance=нет, distance=0
2026-03-03 10:16:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (9, 13)
2026-03-03 10:16:59 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-03-03 10:16:59 | Reward (шаг): движение delta=-0.180
2026-03-03 10:16:59 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-03 10:16:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-03 10:16:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-03 10:16:59 | --- ФАЗА ЧАРДЖА ---
2026-03-03 10:16:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-03 10:16:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-03 10:16:59 | [MODEL] Чардж: нет доступных целей
2026-03-03 10:16:59 | --- ФАЗА БОЯ ---
2026-03-03 10:16:59 | [MODEL] Ближний бой: нет доступных атак
2026-03-03 10:16:59 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.92838827718412->13.92838827718412, hold_penalty_events=2
2026-03-03 10:16:59 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-03 10:16:59 | Итерация 2 завершена с наградой tensor([-0.1800], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-03 10:16:59 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 6, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-03 10:16:59 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 6, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 0

2026-03-03 10:17:01 | === БОЕВОЙ РАУНД 4 ===
2026-03-03 10:17:01 | --- ХОД PLAYER ---
2026-03-03 10:17:01 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-03 10:17:01 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-03 10:17:01 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-03 10:17:04 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-03 10:17:04 | --- ФАЗА ЧАРДЖА ---
2026-03-03 10:17:04 | Нет доступных целей для чарджа.
2026-03-03 10:17:04 | --- ФАЗА БОЯ ---
2026-03-03 10:17:04 | --- ХОД MODEL ---
2026-03-03 10:17:04 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-03 10:17:04 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-03 10:17:04 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-03 10:17:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=13.928, d_after=13.928, d_best=2.928, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-03 10:17:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (7, 25). Выбор: none, advance=нет, distance=0
2026-03-03 10:17:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (7, 25)
2026-03-03 10:17:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=20.248, d_after=20.248, d_best=9.248, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-03 10:17:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (9, 13). Выбор: none, advance=нет, distance=0
2026-03-03 10:17:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (9, 13)
2026-03-03 10:17:04 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-03-03 10:17:04 | Reward (шаг): движение delta=-0.180
2026-03-03 10:17:04 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-03 10:17:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-03 10:17:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-03 10:17:04 | --- ФАЗА ЧАРДЖА ---
2026-03-03 10:17:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-03 10:17:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-03 10:17:04 | [MODEL] Чардж: нет доступных целей
2026-03-03 10:17:04 | --- ФАЗА БОЯ ---
2026-03-03 10:17:04 | [MODEL] Ближний бой: нет доступных атак
2026-03-03 10:17:04 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.92838827718412->13.92838827718412, hold_penalty_events=2
2026-03-03 10:17:04 | === КОНЕЦ БОЕВОГО РАУНДА 4 ===
2026-03-03 10:17:04 | Итерация 3 завершена с наградой tensor([-0.1800], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-03 10:17:04 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 8, 'playerCP': 8, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 5, 'battle round': 5, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-03 10:17:04 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 8, CP PLAYER: 8
VP MODEL: 0, VP PLAYER: 0

2026-03-03 10:17:05 | === БОЕВОЙ РАУНД 5 ===
2026-03-03 10:17:05 | --- ХОД PLAYER ---
2026-03-03 10:17:05 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-03 10:17:05 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-03 10:17:05 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-03 10:17:08 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-03 10:17:08 | --- ФАЗА ЧАРДЖА ---
2026-03-03 10:17:08 | Нет доступных целей для чарджа.
2026-03-03 10:17:08 | --- ФАЗА БОЯ ---
2026-03-03 10:17:08 | --- ХОД MODEL ---
2026-03-03 10:17:08 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-03 10:17:08 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-03 10:17:08 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-03 10:17:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=13.928, d_after=13.928, d_best=2.928, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-03-03 10:17:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (7, 25). Выбор: none, advance=нет, distance=0
2026-03-03 10:17:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (7, 25)
2026-03-03 10:17:08 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=20.248, d_after=20.248, d_best=9.248, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-03-03 10:17:08 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (9, 13). Выбор: none, advance=нет, distance=0
2026-03-03 10:17:08 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (9, 13)
2026-03-03 10:17:08 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-03-03 10:17:08 | Reward (шаг): движение delta=-0.240
2026-03-03 10:17:08 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-03 10:17:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-03 10:17:08 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-03 10:17:08 | --- ФАЗА ЧАРДЖА ---
2026-03-03 10:17:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-03 10:17:08 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-03 10:17:08 | [MODEL] Чардж: нет доступных целей
2026-03-03 10:17:08 | --- ФАЗА БОЯ ---
2026-03-03 10:17:08 | [MODEL] Ближний бой: нет доступных атак
2026-03-03 10:17:08 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.92838827718412->13.92838827718412, hold_penalty_events=2
2026-03-03 10:17:08 | === КОНЕЦ БОЕВОГО РАУНДА 5 ===
2026-03-03 10:17:08 | Итерация 4 завершена с наградой tensor([-0.2400], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-03 10:17:08 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 10, 'playerCP': 10, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 6, 'battle round': 6, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-03 10:17:08 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 10, CP PLAYER: 10
VP MODEL: 0, VP PLAYER: 0

2026-03-03 10:17:16 | === БОЕВОЙ РАУНД 6 ===
2026-03-03 10:17:16 | --- ХОД PLAYER ---
2026-03-03 10:17:16 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-03 10:17:16 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-03 10:17:16 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-03 10:17:19 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-03 10:17:19 | --- ФАЗА ЧАРДЖА ---
2026-03-03 10:17:19 | Нет доступных целей для чарджа.
2026-03-03 10:17:19 | --- ФАЗА БОЯ ---
2026-03-03 10:17:19 | --- ХОД MODEL ---
2026-03-03 10:17:19 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-03 10:17:19 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-03 10:17:19 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-03 10:17:19 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=13.928, d_after=13.928, d_best=2.928, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-03-03 10:17:19 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (7, 25). Выбор: none, advance=нет, distance=0
2026-03-03 10:17:19 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (7, 25)
2026-03-03 10:17:19 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=20.248, d_after=20.248, d_best=9.248, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-03-03 10:17:19 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (9, 13). Выбор: none, advance=нет, distance=0
2026-03-03 10:17:19 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (9, 13)
2026-03-03 10:17:19 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-03-03 10:17:19 | Reward (шаг): движение delta=-0.240
2026-03-03 10:17:19 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-03 10:17:19 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-03 10:17:19 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-03 10:17:19 | --- ФАЗА ЧАРДЖА ---
2026-03-03 10:17:19 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-03 10:17:19 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-03 10:17:19 | [MODEL] Чардж: нет доступных целей
2026-03-03 10:17:19 | --- ФАЗА БОЯ ---
2026-03-03 10:17:19 | [MODEL] Ближний бой: нет доступных атак
2026-03-03 10:17:19 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.92838827718412->13.92838827718412, hold_penalty_events=2
2026-03-03 10:17:19 | === КОНЕЦ БОЕВОГО РАУНДА 6 ===
2026-03-03 10:17:19 | Итерация 5 завершена с наградой tensor([-0.2400], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-03 10:17:19 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 12, 'playerCP': 12, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 7, 'battle round': 7, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-03 10:17:19 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 12, CP PLAYER: 12
VP MODEL: 0, VP PLAYER: 0

