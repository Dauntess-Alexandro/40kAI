2026-03-10 14:14:56 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-10 14:14:56 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-10 14:14:56 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-10 14:14:56 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-10 14:14:57 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-10 14:14:57 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-42-937471.pickle
2026-03-10 14:14:57 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-42-937471.pth
2026-03-10 14:14:57 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-10 14:15:02 | Roll-off Attacker/Defender: enemy=1 model=4 -> attacker=model
2026-03-10 14:15:02 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-10 14:15:02 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-10 14:15:02 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-10 14:15:02 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-10 14:15:02 | [DEPLOY] Order: model first, alternating
2026-03-10 14:15:02 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-10 14:15:02 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=63, coord=(1,3), attempt=1, reward=+0.015, score_before=0.000, score_after=0.304, reward_delta=+0.015, forward=0.054, spread=1.000, edge=0.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-10 14:15:02 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (1,3)
2026-03-10 14:15:02 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-10 14:15:02 | REQ: deploy cell accepted x=57, y=31
2026-03-10 14:15:02 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (31,57)
2026-03-10 14:15:02 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (31,57)
2026-03-10 14:15:02 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-10 14:15:02 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=608, coord=(10,8), attempt=1, reward=+0.003, score_before=0.304, score_after=0.371, reward_delta=+0.003, forward=0.097, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-10 14:15:02 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (10,8)
2026-03-10 14:15:02 | REQ: deploy cell accepted x=52, y=23
2026-03-10 14:15:03 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (23,52)
2026-03-10 14:15:03 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (23,52)
2026-03-10 14:15:03 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.075 avg_spread=1.000 avg_edge=0.250 avg_cover=0.000
2026-03-10 14:15:03 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.018525817895151758, 'units': 2, 'total_deploy_reward': 0.018525817895151758, 'forward_sum': 0.15084745762711865, 'spread_sum': 2.0, 'edge_sum': 0.5, 'cover_sum': 0.0, 'avg_forward': 0.07542372881355933, 'avg_spread': 1.0, 'avg_edge': 0.25, 'avg_cover': 0.0}
2026-03-10 14:15:03 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-10 14:15:03 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-10 14:15:03 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-10 14:15:03 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 14:15:03 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-10 14:15:03 | FX: перепроигрываю 30 строк(и) лога.
2026-03-10 14:15:04 | === БОЕВОЙ РАУНД 1 ===
2026-03-10 14:15:04 | --- ХОД PLAYER ---
2026-03-10 14:15:04 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 14:15:04 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 14:15:04 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 14:15:05 | REQ: move cell accepted (RMB) x=46, y=30, mode=advance
2026-03-10 14:15:05 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 14:15:06 | REQ: move cell accepted (RMB) x=45, y=20, mode=advance
2026-03-10 14:15:06 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 14:15:06 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 14:15:06 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 14:15:06 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 14:15:06 | --- ФАЗА ЧАРДЖА ---
2026-03-10 14:15:06 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 14:15:06 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 14:15:06 | Нет доступных целей для чарджа.
2026-03-10 14:15:06 | --- ФАЗА БОЯ ---
2026-03-10 14:15:06 | --- ХОД MODEL ---
2026-03-10 14:15:06 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 14:15:06 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 14:15:07 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 14:15:07 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=33.015, d_after=33.015, d_best=22.015, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-10 14:15:07 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 3). Выбор: stay, advance=нет, distance=0
2026-03-10 14:15:07 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (1, 3)
2026-03-10 14:15:07 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=24.166, d_after=24.166, d_best=13.166, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-10 14:15:07 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (10, 8). Выбор: stay, advance=нет, distance=0
2026-03-10 14:15:07 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (10, 8)
2026-03-10 14:15:07 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-03-10 14:15:07 | Reward (шаг): движение delta=-0.120
2026-03-10 14:15:07 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 14:15:07 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=40.00, range=24.00, delta=+16.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:07 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=39.00, range=24.00, delta=+15.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:07 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 14:15:07 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:07 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:07 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 14:15:07 | --- ФАЗА ЧАРДЖА ---
2026-03-10 14:15:07 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 14:15:07 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 14:15:07 | [MODEL] Чардж: нет доступных целей
2026-03-10 14:15:07 | --- ФАЗА БОЯ ---
2026-03-10 14:15:07 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 14:15:07 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.166091947189145->24.166091947189145, hold_penalty_events=2
2026-03-10 14:15:07 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-10 14:15:07 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-10 14:15:07 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-10 14:15:07 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-10 14:15:07 | Итерация 0 завершена с наградой tensor([-0.1200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-10 14:15:07 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 14:15:07 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-10 14:15:08 | === БОЕВОЙ РАУНД 2 ===
2026-03-10 14:15:08 | --- ХОД PLAYER ---
2026-03-10 14:15:08 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 14:15:08 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 14:15:08 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 14:15:09 | Unit 11: movement stay (позиция сохранена x=46, y=30).
2026-03-10 14:15:10 | Unit 11 — Necrons Necron Warriors (x10 моделей): движение stay (mode=stay). Позиция сохранена: (46,30).
2026-03-10 14:15:13 | Unit 12: movement stay (позиция сохранена x=45, y=20).
2026-03-10 14:15:13 | Unit 12 — Necrons Necron Warriors (x10 моделей): движение stay (mode=stay). Позиция сохранена: (45,20).
2026-03-10 14:15:13 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 14:15:13 | [TARGET][SHOOT] Unit 11 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=40.00, range=24.00, delta=+16.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:13 | [TARGET][SHOOT] Unit 11 — Necrons Necron Warriors (x10 моделей) -> Unit 22 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:13 | [TARGET][SHOOT] Unit 12 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=39.00, range=24.00, delta=+15.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:13 | [TARGET][SHOOT] Unit 12 — Necrons Necron Warriors (x10 моделей) -> Unit 22 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:13 | --- ФАЗА ЧАРДЖА ---
2026-03-10 14:15:13 | Нет доступных целей для чарджа.
2026-03-10 14:15:13 | --- ФАЗА БОЯ ---
2026-03-10 14:15:13 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=40.00, range=24.00, delta=+16.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:13 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=39.00, range=24.00, delta=+15.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:13 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:13 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:13 | --- ХОД MODEL ---
2026-03-10 14:15:13 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 14:15:13 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 14:15:13 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 14:15:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=33.015, d_after=33.015, d_best=22.015, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-10 14:15:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 3). Выбор: stay, advance=нет, distance=0
2026-03-10 14:15:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (1, 3)
2026-03-10 14:15:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=24.166, d_after=24.166, d_best=13.166, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-10 14:15:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (10, 8). Выбор: stay, advance=нет, distance=0
2026-03-10 14:15:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (10, 8)
2026-03-10 14:15:13 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-03-10 14:15:13 | Reward (шаг): движение delta=-0.120
2026-03-10 14:15:13 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 14:15:13 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=40.00, range=24.00, delta=+16.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:13 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=39.00, range=24.00, delta=+15.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 14:15:13 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:13 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 14:15:13 | --- ФАЗА ЧАРДЖА ---
2026-03-10 14:15:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 14:15:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 14:15:13 | [MODEL] Чардж: нет доступных целей
2026-03-10 14:15:13 | --- ФАЗА БОЯ ---
2026-03-10 14:15:13 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 14:15:13 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.166091947189145->24.166091947189145, hold_penalty_events=2
2026-03-10 14:15:13 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-10 14:15:13 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-10 14:15:13 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-10 14:15:13 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-10 14:15:13 | Итерация 1 завершена с наградой tensor([-0.1200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-10 14:15:13 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 4, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 14:15:13 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 4, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0

2026-03-10 14:15:15 | === БОЕВОЙ РАУНД 3 ===
2026-03-10 14:15:15 | --- ХОД PLAYER ---
2026-03-10 14:15:15 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 14:15:15 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 14:15:15 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 14:15:15 | REQ: move cell accepted (RMB) x=35, y=22, mode=advance
2026-03-10 14:15:16 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 14:15:16 | REQ: move cell accepted (RMB) x=35, y=15, mode=advance
2026-03-10 14:15:17 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 14:15:17 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 14:15:17 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 14:15:17 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 14:15:17 | --- ФАЗА ЧАРДЖА ---
2026-03-10 14:15:17 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 14:15:17 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 14:15:17 | Нет доступных целей для чарджа.
2026-03-10 14:15:17 | --- ФАЗА БОЯ ---
2026-03-10 14:15:17 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:17 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:17 | --- ХОД MODEL ---
2026-03-10 14:15:17 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 14:15:17 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 14:15:17 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 14:15:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=33.015, d_after=33.015, d_best=22.015, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-10 14:15:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 3). Выбор: stay, advance=нет, distance=0
2026-03-10 14:15:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (1, 3)
2026-03-10 14:15:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=24.166, d_after=24.166, d_best=13.166, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-10 14:15:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (10, 8). Выбор: stay, advance=нет, distance=0
2026-03-10 14:15:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (10, 8)
2026-03-10 14:15:17 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-03-10 14:15:17 | Reward (шаг): движение delta=-0.180
2026-03-10 14:15:17 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 14:15:17 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:17 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 14:15:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-10 14:15:17 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 14:15:17 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-10 14:15:17 | 
🎲 Бросок сейвы (save): 2D6
2026-03-10 14:15:17 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-03-10 14:15:17 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-10 14:15:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-10 14:15:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-10 14:15:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=14, need<=3).
2026-03-10 14:15:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-10 14:15:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-10 14:15:17 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 14:15:17 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 14:15:17 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:15:17 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-10 14:15:17 | Оружие: Gauss flayer
2026-03-10 14:15:17 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 14:15:17 | BS оружия: 4+
2026-03-10 14:15:17 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 14:15:17 | Save цели: 4+ (invul: нет)
2026-03-10 14:15:17 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 14:15:17 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 14:15:17 | Hit rolls:    [2, 3, 6, 4, 3, 5, 5, 4, 5, 3]  -> hits: 6 (crits: 1)
2026-03-10 14:15:17 | Wound rolls:  [2, 6, 1, 1, 3]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 1 = 2
2026-03-10 14:15:17 | Save rolls:   [6, 1]  (цель 4+) -> failed saves: 1
2026-03-10 14:15:17 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-10 14:15:17 | FX: найден итог урона = 1.0.
2026-03-10 14:15:17 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-10 14:15:17 | FX: позиция эффекта start=(204.0,252.0) end=(852.0,540.0).
2026-03-10 14:15:17 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-10 14:15:17 | 📌 -------------------------

2026-03-10 14:15:17 | Reward (шаг): стрельба delta=+0.080
2026-03-10 14:15:17 | --- ФАЗА ЧАРДЖА ---
2026-03-10 14:15:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 14:15:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 14:15:17 | [MODEL] Чардж: нет доступных целей
2026-03-10 14:15:17 | --- ФАЗА БОЯ ---
2026-03-10 14:15:17 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 14:15:17 | Reward (terrain/potential): gamma=0.990, phi_before=-0.033, phi_after=-0.033, delta=+0.000; cover=0.000->0.000, threat=-0.333->-0.333, guard=0.000->0.000
2026-03-10 14:15:17 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=2)
2026-03-10 14:15:17 | Reward (terrain/clamp): raw=-0.010, cap=±0.120, clamp не сработал
2026-03-10 14:15:17 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-10 14:15:17 | Итерация 2 завершена с наградой tensor([-0.1097], device='cuda:0'), здоровье игрока [9.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-10 14:15:17 | {'model health': [10.0, 10.0], 'player health': [9.0, 10.0], 'model alive models': [10, 10], 'player alive models': [9, 10], 'modelCP': 6, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 14:15:17 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [9.0, 10.0]
CP MODEL: 6, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 0
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-03-10 14:15:17 | === БОЕВОЙ РАУНД 4 ===
2026-03-10 14:15:17 | --- ХОД PLAYER ---
2026-03-10 14:15:17 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 14:15:17 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 14:15:21 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-10 14:15:21 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-10 14:15:21 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 14:15:21 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-10 14:15:21 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 14:15:21 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 14:15:22 | REQ: move cell accepted (RMB) x=31, y=21, mode=normal
2026-03-10 14:15:22 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-10 14:15:22 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 14:15:22 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-10 14:15:22 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-10 14:15:22 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-10 14:15:22 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-10 14:15:22 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-10 14:15:22 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-10 14:15:22 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:15:22 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-10 14:15:22 | Оружие: Gauss flayer
2026-03-10 14:15:22 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 14:15:22 | BS оружия: 4+
2026-03-10 14:15:22 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 14:15:22 | Save цели: 4+ (invul: нет)
2026-03-10 14:15:22 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 14:15:22 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 14:15:22 | Правило: Overwatch: попадания только на 6+
2026-03-10 14:15:22 | Hit rolls:    [4, 6, 3, 6, 1, 5, 4, 5, 2, 2]  -> hits: 6 (crits: 2)
2026-03-10 14:15:22 | Wound rolls:  [1, 5]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-10 14:15:22 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-10 14:15:22 | FX: найден итог урона = 1.0.
2026-03-10 14:15:22 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-10 14:15:22 | FX: позиция эффекта start=(204.0,252.0) end=(852.0,540.0).
2026-03-10 14:15:22 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-10 14:15:22 | 📌 -------------------------

2026-03-10 14:15:24 | Unit 12: movement stay (позиция сохранена x=35, y=15).
2026-03-10 14:15:24 | Unit 12 — Necrons Necron Warriors (x10 моделей): движение stay (mode=stay). Позиция сохранена: (35,15).
2026-03-10 14:15:24 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 14:15:24 | [TARGET][SHOOT] Unit 11 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:24 | REQ: валидные цели стрельбы для Unit 11: [22] | отфильтрованы: [21: цель вне дальности: range 25.00 > 24.00 (out_of_range by +1.00)]
2026-03-10 14:15:27 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-10 14:15:32 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-10 14:15:34 | 
🎲 Бросок сейвы (save): 3D6
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (overwatch)
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-10 14:15:37 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 3.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:15:37 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 14:15:37 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 14:15:37 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:15:37 | FX: найдена строка стрельбы (attacker=11, target=22).
2026-03-10 14:15:37 | Оружие: Gauss flayer
2026-03-10 14:15:37 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 14:15:37 | BS оружия: 4+
2026-03-10 14:15:37 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 14:15:37 | Save цели: 4+ (invul: нет)
2026-03-10 14:15:37 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 14:15:37 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 14:15:37 | Hit rolls:    [1, 2, 3, 4, 5, 6, 5, 5, 5]  -> hits: 6 (crits: 1)
2026-03-10 14:15:37 | Wound rolls:  [3, 4, 5, 1, 2]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 1 = 3
2026-03-10 14:15:37 | Save rolls:   [2, 1, 2]  (цель 4+) -> failed saves: 3
2026-03-10 14:15:37 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-10 14:15:37 | FX: найден итог урона = 3.0.
2026-03-10 14:15:37 | FX: создан FxShotEvent (attacker=11, target=22, weapon=Gauss flayer, damage=3.0).
2026-03-10 14:15:37 | FX: позиция эффекта start=(756.0,516.0) end=(204.0,252.0).
2026-03-10 14:15:37 | FX: эффект добавлен в рендер (attacker=11, target=22).
2026-03-10 14:15:37 | 📌 -------------------------

2026-03-10 14:15:37 | [TARGET][SHOOT] Unit 12 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:37 | [TARGET][SHOOT] Unit 12 — Necrons Necron Warriors (x10 моделей) -> Unit 22 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:37 | --- ФАЗА ЧАРДЖА ---
2026-03-10 14:15:37 | Нет доступных целей для чарджа.
2026-03-10 14:15:37 | --- ФАЗА БОЯ ---
2026-03-10 14:15:37 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:37 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:37 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:37 | --- ХОД MODEL ---
2026-03-10 14:15:37 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 2
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-10 14:15:37 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-10 14:15:37 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 14:15:37 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=33.015, d_after=33.015, d_best=22.015, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-10 14:15:37 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 3). Выбор: stay, advance=нет, distance=0
2026-03-10 14:15:37 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (1, 3)
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=24.166, d_after=24.166, d_best=13.166, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (10, 8). Выбор: stay, advance=нет, distance=0
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (10, 8)
2026-03-10 14:15:37 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-03-10 14:15:37 | Reward (шаг): движение delta=-0.180
2026-03-10 14:15:37 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 14:15:37 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:37 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:37 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 14:15:37 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-10 14:15:37 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-10 14:15:37 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-10 14:15:37 | 
🎲 Бросок сейвы (save): 6D6
2026-03-10 14:15:37 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 5. Осталось: 4. HP: 9.0 -> 4.0 (shooting)
2026-03-10 14:15:37 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 4. Причина: потери моделей.
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.250 (dealt=5.00)
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=14, need<=3).
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.250, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.520
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 5.0
2026-03-10 14:15:37 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 14:15:37 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 14:15:37 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:15:37 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-10 14:15:37 | Оружие: Gauss flayer
2026-03-10 14:15:37 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 14:15:37 | BS оружия: 4+
2026-03-10 14:15:37 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 14:15:37 | Save цели: 4+ (invul: нет)
2026-03-10 14:15:37 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 14:15:37 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 14:15:37 | Hit rolls:    [6, 1, 6, 2, 6, 6, 6, 6, 4]  -> hits: 7 (crits: 6)
2026-03-10 14:15:37 | Wound rolls:  [3]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 6 = 6
2026-03-10 14:15:37 | Save rolls:   [2, 1, 3, 3, 6, 2]  (цель 4+) -> failed saves: 5
2026-03-10 14:15:37 | 
✅ Итог по движку: прошло урона = 5.0
2026-03-10 14:15:37 | FX: найден итог урона = 5.0.
2026-03-10 14:15:37 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=5.0).
2026-03-10 14:15:37 | FX: позиция эффекта start=(204.0,252.0) end=(756.0,516.0).
2026-03-10 14:15:37 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-10 14:15:37 | 📌 -------------------------

2026-03-10 14:15:37 | Reward (шаг): стрельба delta=+0.520
2026-03-10 14:15:37 | --- ФАЗА ЧАРДЖА ---
2026-03-10 14:15:37 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 14:15:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 14:15:37 | [MODEL] Чардж: нет доступных целей
2026-03-10 14:15:37 | --- ФАЗА БОЯ ---
2026-03-10 14:15:37 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 14:15:37 | Reward (terrain/potential): gamma=0.990, phi_before=-0.017, phi_after=-0.017, delta=+0.000; cover=0.000->0.000, threat=-0.167->-0.167, guard=0.000->0.000
2026-03-10 14:15:37 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=1)
2026-03-10 14:15:37 | Reward (terrain/clamp): raw=-0.010, cap=±0.120, clamp не сработал
2026-03-10 14:15:37 | === КОНЕЦ БОЕВОГО РАУНДА 4 ===
2026-03-10 14:15:37 | Итерация 3 завершена с наградой tensor([0.3302], device='cuda:0'), здоровье игрока [4.0, 10.0], здоровье модели [10.0, 9.0]
2026-03-10 14:15:37 | {'model health': [10.0, 9.0], 'player health': [4.0, 10.0], 'model alive models': [10, 9], 'player alive models': [4, 10], 'modelCP': 7, 'playerCP': 8, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 5, 'battle round': 5, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 14:15:37 | Здоровье MODEL: [10.0, 9.0], здоровье PLAYER: [4.0, 10.0]
CP MODEL: 7, CP PLAYER: 8
VP MODEL: 0, VP PLAYER: 0
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 5.0 раз(а)

2026-03-10 14:15:39 | === БОЕВОЙ РАУНД 5 ===
2026-03-10 14:15:39 | --- ХОД PLAYER ---
2026-03-10 14:15:39 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 14:15:39 | Unit 11 — Necrons Necron Warriors (x10 моделей): ниже половины состава, тест Battle-shock.
2026-03-10 14:15:39 | Бросок 2D6...
2026-03-10 14:15:42 | Бросок: 1 2
2026-03-10 14:15:42 | Unit 11 — Necrons Necron Warriors (x10 моделей): тест Battle-shock провален.
2026-03-10 14:15:45 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 14:15:50 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-10 14:15:50 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=4, раны=[1, 1, 1, 1] всего=4
2026-03-10 14:15:50 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 14:15:50 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=5, раны=[1, 1, 1, 1, 1] всего=5
2026-03-10 14:15:50 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 14:15:50 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 14:15:53 | REQ: move cell accepted (RMB) x=29, y=21, mode=normal
2026-03-10 14:15:54 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-10 14:15:54 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-10 14:15:54 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-10 14:15:54 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 4. HP: 5.0 -> 4.0 (Overwatch)
2026-03-10 14:15:54 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 4. Причина: потери моделей.
2026-03-10 14:15:54 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-10 14:15:54 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-10 14:15:54 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-10 14:15:54 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:15:54 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-10 14:15:54 | Оружие: Gauss flayer
2026-03-10 14:15:54 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 14:15:54 | BS оружия: 4+
2026-03-10 14:15:54 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 14:15:54 | Save цели: 4+ (invul: нет)
2026-03-10 14:15:54 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 14:15:54 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 14:15:54 | Правило: Overwatch: попадания только на 6+
2026-03-10 14:15:54 | Hit rolls:    [4, 6, 4, 6, 5, 5, 1, 1, 2]  -> hits: 6 (crits: 2)
2026-03-10 14:15:54 | Wound rolls:  [2, 5]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-10 14:15:54 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-10 14:15:54 | FX: найден итог урона = 1.0.
2026-03-10 14:15:54 | FX: дубликат отчёта, эффект не создаём.
2026-03-10 14:15:54 | 📌 -------------------------

2026-03-10 14:16:01 | REQ: move cell accepted (RMB) x=30, y=12, mode=normal
2026-03-10 14:16:01 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-10 14:16:01 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-10 14:16:01 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-10 14:16:01 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-10 14:16:01 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-10 14:16:01 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-10 14:16:01 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-10 14:16:01 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-10 14:16:01 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:16:01 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-10 14:16:01 | Оружие: Gauss flayer
2026-03-10 14:16:01 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 14:16:01 | BS оружия: 4+
2026-03-10 14:16:01 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 14:16:01 | Save цели: 4+ (invul: нет)
2026-03-10 14:16:01 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 14:16:01 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 14:16:01 | Правило: Overwatch: попадания только на 6+
2026-03-10 14:16:01 | Hit rolls:    [6, 3, 1, 6, 4, 2, 4, 4, 1]  -> hits: 5 (crits: 2)
2026-03-10 14:16:01 | Wound rolls:  [2, 5]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-10 14:16:01 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-10 14:16:01 | FX: найден итог урона = 1.0.
2026-03-10 14:16:01 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-10 14:16:01 | FX: позиция эффекта start=(204.0,252.0) end=(852.0,372.0).
2026-03-10 14:16:01 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-10 14:16:01 | 📌 -------------------------

2026-03-10 14:16:01 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 14:16:01 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-10 14:16:08 | 
🎲 Бросок на попадание (to hit): 4D6
2026-03-10 14:16:11 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:16:11 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 14:16:11 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 14:16:11 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:16:11 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-10 14:16:11 | Оружие: Gauss flayer
2026-03-10 14:16:11 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 14:16:11 | BS оружия: 4+
2026-03-10 14:16:11 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 14:16:11 | Save цели: 4+ (invul: нет)
2026-03-10 14:16:11 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 14:16:11 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 14:16:11 | Hit rolls:    [1, 1, 1, 1]  -> hits: 0
2026-03-10 14:16:11 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-10 14:16:11 | FX: найден итог урона = 0.0.
2026-03-10 14:16:11 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=0.0).
2026-03-10 14:16:11 | FX: позиция эффекта start=(708.0,516.0) end=(84.0,36.0).
2026-03-10 14:16:11 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-03-10 14:16:11 | 📌 -------------------------

2026-03-10 14:16:11 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-10 14:16:11 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-03-10 14:16:11 | FX: перепроигрываю 30 строк(и) лога.
2026-03-10 14:16:11 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-10 14:16:11 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-10 14:16:11 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 14:16:11 | FX: найден итог урона = 1.0.
2026-03-10 14:16:11 | FX: дубликат отчёта, эффект не создаём.
2026-03-10 14:16:29 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-10 14:16:36 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-10 14:16:38 | 
🎲 Бросок сейвы (save): 5D6
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 6. HP: 9.0 -> 6.0 (overwatch)
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-03-10 14:16:42 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 3.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:16:42 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 14:16:42 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 14:16:42 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:16:42 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-03-10 14:16:42 | Оружие: Gauss flayer
2026-03-10 14:16:42 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 14:16:42 | BS оружия: 4+
2026-03-10 14:16:42 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 14:16:42 | Save цели: 4+ (invul: нет)
2026-03-10 14:16:42 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 14:16:42 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 14:16:42 | Hit rolls:    [1, 2, 3, 4, 5, 6, 5, 4, 5]  -> hits: 6 (crits: 1)
2026-03-10 14:16:42 | Wound rolls:  [3, 4, 5, 6, 4]  (цель 4+) -> rolled wounds: 4 + auto(w/LETHAL): 1 = 5
2026-03-10 14:16:42 | Save rolls:   [2, 1, 3, 4, 5]  (цель 4+) -> failed saves: 3
2026-03-10 14:16:42 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-10 14:16:42 | FX: найден итог урона = 3.0.
2026-03-10 14:16:42 | FX: создан FxShotEvent (attacker=12, target=22, weapon=Gauss flayer, damage=3.0).
2026-03-10 14:16:42 | FX: позиция эффекта start=(732.0,300.0) end=(204.0,252.0).
2026-03-10 14:16:42 | FX: эффект добавлен в рендер (attacker=12, target=22).
2026-03-10 14:16:42 | 📌 -------------------------

2026-03-10 14:16:42 | --- ФАЗА ЧАРДЖА ---
2026-03-10 14:16:42 | Нет доступных целей для чарджа.
2026-03-10 14:16:42 | --- ФАЗА БОЯ ---
2026-03-10 14:16:42 | --- ХОД MODEL ---
2026-03-10 14:16:42 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-03-10 14:16:42 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 14:16:42 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 14:16:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=33.015, d_after=33.015, d_best=22.015, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-03-10 14:16:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 3). Выбор: stay, advance=нет, distance=0
2026-03-10 14:16:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (1, 3)
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=24.166, d_after=24.166, d_best=13.166, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (10, 8). Выбор: stay, advance=нет, distance=0
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (10, 8)
2026-03-10 14:16:42 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-03-10 14:16:42 | Reward (шаг): движение delta=-0.240
2026-03-10 14:16:42 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 14:16:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-10 14:16:42 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 14:16:42 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-10 14:16:42 | 
🎲 Бросок сейвы (save): 4D6
2026-03-10 14:16:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 2. HP: 4.0 -> 2.0 (shooting)
2026-03-10 14:16:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 2. Причина: потери моделей.
2026-03-10 14:16:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-10 14:16:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-03-10 14:16:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-03-10 14:16:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=19, need<=3).
2026-03-10 14:16:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.280
2026-03-10 14:16:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-10 14:16:42 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 14:16:42 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 14:16:42 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:16:42 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-10 14:16:42 | Оружие: Gauss flayer
2026-03-10 14:16:42 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 14:16:42 | BS оружия: 4+
2026-03-10 14:16:42 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 14:16:42 | Save цели: 4+ (invul: нет)
2026-03-10 14:16:42 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 14:16:42 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 14:16:42 | Hit rolls:    [1, 3, 4, 6, 1, 4, 6, 4, 5, 3]  -> hits: 6 (crits: 2)
2026-03-10 14:16:42 | Wound rolls:  [4, 3, 1, 4]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 2 = 4
2026-03-10 14:16:42 | Save rolls:   [5, 1, 6, 1]  (цель 4+) -> failed saves: 2
2026-03-10 14:16:42 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-10 14:16:42 | FX: найден итог урона = 2.0.
2026-03-10 14:16:42 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-10 14:16:42 | FX: позиция эффекта start=(84.0,36.0) end=(708.0,516.0).
2026-03-10 14:16:42 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-10 14:16:42 | 📌 -------------------------

2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-10 14:16:42 | 
🎲 Бросок на попадание (to hit): 7D6
2026-03-10 14:16:42 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-10 14:16:42 | 
🎲 Бросок сейвы (save): 4D6
2026-03-10 14:16:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 0. HP: 2.0 -> 0.0 (shooting)
2026-03-10 14:16:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 0. Причина: потери моделей.
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.170
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): kill_bonus=+0.200
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=14, need<=3).
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.170, obj_damage=0.100, obj_kill=0.200, action=0.000, terrain_event=0.000, total=0.930
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-10 14:16:42 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 14:16:42 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 14:16:42 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:16:42 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-10 14:16:42 | Оружие: Gauss flayer
2026-03-10 14:16:42 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 14:16:42 | BS оружия: 4+
2026-03-10 14:16:42 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 14:16:42 | Save цели: 4+ (invul: нет)
2026-03-10 14:16:42 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 14:16:42 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 14:16:42 | Hit rolls:    [1, 6, 2, 6, 6, 2, 4]  -> hits: 4 (crits: 3)
2026-03-10 14:16:42 | Wound rolls:  [5]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 3 = 4
2026-03-10 14:16:42 | Save rolls:   [4, 4, 3, 3]  (цель 4+) -> failed saves: 2
2026-03-10 14:16:42 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-10 14:16:42 | FX: найден итог урона = 2.0.
2026-03-10 14:16:42 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-10 14:16:42 | FX: позиция эффекта start=(204.0,252.0) end=(708.0,516.0).
2026-03-10 14:16:42 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-10 14:16:42 | 📌 -------------------------

2026-03-10 14:16:42 | Reward (шаг): стрельба delta=+1.210
2026-03-10 14:16:42 | --- ФАЗА ЧАРДЖА ---
2026-03-10 14:16:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 14:16:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 14:16:42 | [MODEL] Чардж: нет доступных целей
2026-03-10 14:16:42 | --- ФАЗА БОЯ ---
2026-03-10 14:16:42 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 14:16:42 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.033, delta=+0.034; cover=0.000->0.000, threat=-0.667->-0.333, guard=0.000->0.000
2026-03-10 14:16:42 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=2)
2026-03-10 14:16:42 | Reward (terrain/clamp): raw=+0.014, cap=±0.120, clamp не сработал
2026-03-10 14:16:42 | === КОНЕЦ БОЕВОГО РАУНДА 5 ===
2026-03-10 14:16:42 | Итерация 4 завершена с наградой tensor([0.9837], device='cuda:0'), здоровье игрока [0.0, 9.0], здоровье модели [10.0, 7.0]
2026-03-10 14:16:42 | {'model health': [10.0, 7.0], 'player health': [0.0, 9.0], 'model alive models': [10, 7], 'player alive models': [0, 9], 'modelCP': 7, 'playerCP': 10, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 6, 'battle round': 6, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 14:16:42 | Здоровье MODEL: [10.0, 7.0], здоровье PLAYER: [0.0, 9.0]
CP MODEL: 7, CP PLAYER: 10
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)

2026-03-10 14:16:43 | === БОЕВОЙ РАУНД 6 ===
2026-03-10 14:16:43 | --- ХОД PLAYER ---
2026-03-10 14:16:43 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 14:16:43 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 14:16:45 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-10 14:16:45 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-10 14:16:45 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 14:16:45 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-10 14:16:45 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 14:16:45 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 14:16:48 | REQ: move cell accepted (RMB) x=25, y=11, mode=normal
2026-03-10 14:16:49 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-10 14:16:49 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 14:16:49 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-10 14:16:49 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-10 14:16:49 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-10 14:16:49 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-10 14:16:49 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-10 14:16:49 | Оружие: Gauss flayer
2026-03-10 14:16:49 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 14:16:49 | BS оружия: 4+
2026-03-10 14:16:49 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 14:16:49 | Save цели: 4+ (invul: нет)
2026-03-10 14:16:49 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 14:16:49 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 14:16:49 | Правило: Overwatch: попадания только на 6+
2026-03-10 14:16:49 | Hit rolls:    [5, 3, 4, 3, 5, 3, 4, 5, 4, 5]  -> hits: 7
2026-03-10 14:16:49 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-10 14:16:49 | FX: найден итог урона = 0.0.
2026-03-10 14:16:49 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-10 14:16:49 | FX: позиция эффекта start=(84.0,36.0) end=(732.0,300.0).
2026-03-10 14:16:49 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-10 14:16:49 | 📌 -------------------------

2026-03-10 14:16:49 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 14:16:49 | Ошибка игры: not enough values to unpack (expected 2, got 0). Место: запуск GameController. Проверьте путь к модели и наличие файлов .pickle/.pth.
