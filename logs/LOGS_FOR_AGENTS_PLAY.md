2026-04-27 20:52:40 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-27 20:52:40 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-27 20:52:40 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-27 20:52:40 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-27 20:52:41 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 20:52:41 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-27 20:52:41 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-27 20:52:41 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-27 20:52:41 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-27 20:52:41 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-27 20:52:41 | [LEAGUE] Viewer использует agent-id=P1_Necrons_only_war_v1_final_ep1000_20260427_204241
2026-04-27 20:52:41 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-27 20:52:41 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 20:52:52 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-04-27 20:52:52 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-27 20:52:52 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-27 20:52:52 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-27 20:52:52 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-27 20:52:52 | [DEPLOY] Order: model first, alternating
2026-04-27 20:52:52 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 20:52:52 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=423, coord=(7,3), attempt=1, reward=+0.020, score_before=0.000, score_after=0.397, reward_delta=+0.020, forward=0.054, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 20:52:52 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (7,3)
2026-04-27 20:52:52 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 20:52:53 | REQ: deploy cell accepted x=49, y=24
2026-04-27 20:52:53 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,49)
2026-04-27 20:52:53 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,49)
2026-04-27 20:52:53 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 20:52:53 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1151, coord=(19,11), attempt=1, reward=+0.002, score_before=0.397, score_after=0.429, reward_delta=+0.002, forward=0.122, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 20:52:53 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (19,11)
2026-04-27 20:52:53 | REQ: deploy cell accepted x=50, y=17
2026-04-27 20:52:55 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,50)
2026-04-27 20:52:55 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,50)
2026-04-27 20:52:55 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.088 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-27 20:52:55 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02144264879779267, 'units': 2, 'total_deploy_reward': 0.02144264879779267, 'forward_sum': 0.17627118644067796, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.08813559322033898, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-27 20:52:55 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-27 20:52:55 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-27 20:52:55 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-04-27 20:52:55 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-27 20:52:55 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-27 20:52:55 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-27 20:52:55 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 20:52:56 | === БОЕВОЙ РАУНД 1 ===
2026-04-27 20:52:56 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-27 20:52:56 | --- ХОД PLAYER ---
2026-04-27 20:52:56 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-27 20:52:56 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-27 20:52:56 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-27 20:52:57 | REQ: move cell accepted (RMB) x=38, y=23, mode=advance
2026-04-27 20:52:57 | [MOVE] unit=11 advance to=(38,23) dist=11 M=5 adv=6
2026-04-27 20:52:58 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 20:52:58 | REQ: move cell accepted (RMB) x=39, y=15, mode=advance
2026-04-27 20:52:58 | [MOVE] unit=12 advance to=(39,15) dist=11 M=5 adv=6
2026-04-27 20:52:59 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 20:52:59 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-27 20:52:59 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-27 20:52:59 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-27 20:52:59 | --- ФАЗА ЧАРДЖА ---
2026-04-27 20:52:59 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-27 20:52:59 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-27 20:52:59 | Нет доступных целей для чарджа.
2026-04-27 20:52:59 | --- ФАЗА БОЯ ---
2026-04-27 20:52:59 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 20:52:59 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 20:52:59 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 20:52:59 | --- ХОД MODEL ---
2026-04-27 20:52:59 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-27 20:53:02 | [PACE] ack phase=command unit_id=None seq=1 step=command_resolve ok=True
2026-04-27 20:53:02 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-27 20:53:02 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-27 20:53:03 | [PACE] ack phase=movement unit_id=21 seq=2 step=before_unit ok=True
2026-04-27 20:53:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (7, 3). Выбор reachable_idx=2/284, mode=normal, advance=нет, distance=5
2026-04-27 20:53:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (2, 1)
2026-04-27 20:53:03 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 20:53:04 | [PACE] ack phase=movement unit_id=22 seq=3 step=before_unit ok=True
2026-04-27 20:53:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (19, 11). Выбор reachable_idx=12/525, mode=normal, advance=нет, distance=5
2026-04-27 20:53:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (15, 6)
2026-04-27 20:53:04 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 20:53:04 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-27 20:54:51 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-27 20:54:51 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-27 20:54:52 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-27 20:54:52 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-27 20:54:52 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 20:54:52 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-27 20:54:52 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-27 20:54:52 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-27 20:54:52 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-27 20:54:52 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-27 20:54:52 | [LEAGUE] Viewer использует agent-id=P1_Necrons_only_war_v1_final_ep1000_20260427_204241
2026-04-27 20:54:52 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-27 20:54:52 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 21 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=5, cells_rapid=2, rapid_fire=1, source_cell=(1, 1), target_filter_size=2, max_target_dist=5, inferred_from_targets=1. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-27 20:54:52 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 21; source=(1, 1), full_cells=5, rapid_cells=2, вошло=49, rapid=16, не вошло=2351, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-27 20:54:52 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 20:54:54 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-04-27 20:54:54 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-27 20:54:54 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-27 20:54:54 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-27 20:54:54 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-27 20:54:54 | [DEPLOY] Order: model first, alternating
2026-04-27 20:54:54 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 20:54:54 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1022, coord=(17,2), attempt=1, reward=+0.017, score_before=0.000, score_after=0.343, reward_delta=+0.017, forward=0.037, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 20:54:54 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (17,2)
2026-04-27 20:54:54 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 20:54:55 | REQ: deploy cell accepted x=49, y=26
2026-04-27 20:54:55 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,49)
2026-04-27 20:54:55 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,49)
2026-04-27 20:54:55 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 20:54:55 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=2168, coord=(36,8), attempt=1, reward=+0.002, score_before=0.343, score_after=0.390, reward_delta=+0.002, forward=0.088, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 20:54:55 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (36,8)
2026-04-27 20:54:55 | REQ: deploy cell accepted x=49, y=19
2026-04-27 20:54:56 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,49)
2026-04-27 20:54:56 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,49)
2026-04-27 20:54:56 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.063 avg_spread=1.000 avg_edge=0.625 avg_cover=0.000
2026-04-27 20:54:56 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.019491525423728815, 'units': 2, 'total_deploy_reward': 0.019491525423728815, 'forward_sum': 0.12542372881355932, 'spread_sum': 2.0, 'edge_sum': 1.25, 'cover_sum': 0.0, 'avg_forward': 0.06271186440677966, 'avg_spread': 1.0, 'avg_edge': 0.625, 'avg_cover': 0.0}
2026-04-27 20:54:56 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-27 20:54:56 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-27 20:54:56 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-04-27 20:54:56 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-27 20:54:56 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-27 20:54:56 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-27 20:54:56 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:03:36 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-27 21:03:36 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-27 21:03:36 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-27 21:03:36 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-27 21:03:36 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:03:37 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 21:03:37 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pth)
2026-04-27 21:03:37 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pickle
2026-04-27 21:03:37 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth
2026-04-27 21:03:37 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-27 21:03:37 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-27 21:03:37 | [LEAGUE] Viewer использует agent-id=P2_Necrons_only_war_v1_final_ep2000_20260427_205826
2026-04-27 21:03:37 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-27 21:03:37 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:03:38 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-27 21:03:38 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-27 21:03:38 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-27 21:03:38 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-27 21:03:38 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:03:38 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 21:03:39 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pth)
2026-04-27 21:03:39 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pickle
2026-04-27 21:03:39 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth
2026-04-27 21:03:39 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-27 21:03:39 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-27 21:03:39 | [LEAGUE] Viewer использует agent-id=P2_Necrons_only_war_v1_final_ep2000_20260427_205826
2026-04-27 21:03:39 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-27 21:03:39 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:03:39 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:03:45 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-04-27 21:03:45 | Юниты: [('Necron Warriors', '2', 10), ('Necron Warriors', 'unit-281', 10)]
2026-04-27 21:03:45 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-27 21:03:45 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-27 21:03:45 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-27 21:03:45 | [DEPLOY] Order: model first, alternating
2026-04-27 21:03:45 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 21:03:45 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=667, coord=(11,7), attempt=1, reward=+0.021, score_before=0.000, score_after=0.429, reward_delta=+0.021, forward=0.122, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 21:03:45 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (11,7)
2026-04-27 21:03:45 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 21:03:46 | REQ: deploy cell accepted x=51, y=26
2026-04-27 21:03:46 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,51)
2026-04-27 21:03:46 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,51)
2026-04-27 21:03:46 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 21:03:46 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=311, coord=(5,11), attempt=1, reward=+0.001, score_before=0.429, score_after=0.445, reward_delta=+0.001, forward=0.156, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 21:03:46 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (5,11)
2026-04-27 21:03:46 | REQ: deploy cell accepted x=51, y=20
2026-04-27 21:03:46 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:03:47 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,51)
2026-04-27 21:03:47 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,51)
2026-04-27 21:03:47 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.139 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-27 21:03:47 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02223098147418211, 'units': 2, 'total_deploy_reward': 0.02223098147418211, 'forward_sum': 0.27796610169491526, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.13898305084745763, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-27 21:03:47 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-27 21:03:47 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-27 21:03:47 | [MODEL] Архитектура сети: basic (источник: net_type)
2026-04-27 21:03:47 | Ошибка игры: Error(s) in loading state_dict for DQN:
	Missing key(s) in state_dict: "q_heads.0.weight", "q_heads.0.bias", "q_heads.1.weight", "q_heads.1.bias", "q_heads.2.weight", "q_heads.2.bias", "q_heads.3.weight", "q_heads.3.bias", "q_heads.4.weight", "q_heads.4.bias", "q_heads.5.weight", "q_heads.5.bias", "q_heads.6.weight", "q_heads.6.bias", "q_heads.7.weight", "q_heads.7.bias". 
	Unexpected key(s) in state_dict: "policy_heads.0.weight", "policy_heads.0.bias", "policy_heads.1.weight", "policy_heads.1.bias", "policy_heads.2.weight", "policy_heads.2.bias", "policy_heads.3.weight", "policy_heads.3.bias", "policy_heads.4.weight", "policy_heads.4.bias", "policy_heads.5.weight", "policy_heads.5.bias", "policy_heads.6.weight", "policy_heads.6.bias", "policy_heads.7.weight", "policy_heads.7.bias", "value_head.weight", "value_head.bias". . Место: game_controller._run_game_loop (File "C:\40kAI\.venv\Lib\site-packages\torch\nn\modules\module.py", line 2635, in load_state_dict). Что делать дальше: проверьте traceback ниже и исправьте источник ошибки в указанном файле/строке.
2026-04-27 21:03:47 | Traceback (последние вызовы):
2026-04-27 21:03:47 | Traceback (most recent call last):
2026-04-27 21:03:47 |   File "C:\40kAI\gym_mod\gym_mod\engine\game_controller.py", line 357, in _run_game_loop
2026-04-27 21:03:47 |     policy_net.load_state_dict(normalize_state_dict(checkpoint["policy_net"]))
2026-04-27 21:03:47 |   File "C:\40kAI\.venv\Lib\site-packages\torch\nn\modules\module.py", line 2635, in load_state_dict
2026-04-27 21:03:47 |     raise RuntimeError(
2026-04-27 21:03:47 | RuntimeError: Error(s) in loading state_dict for DQN:
2026-04-27 21:03:47 | 	Missing key(s) in state_dict: "q_heads.0.weight", "q_heads.0.bias", "q_heads.1.weight", "q_heads.1.bias", "q_heads.2.weight", "q_heads.2.bias", "q_heads.3.weight", "q_heads.3.bias", "q_heads.4.weight", "q_heads.4.bias", "q_heads.5.weight", "q_heads.5.bias", "q_heads.6.weight", "q_heads.6.bias", "q_heads.7.weight", "q_heads.7.bias". 
2026-04-27 21:03:47 | 	Unexpected key(s) in state_dict: "policy_heads.0.weight", "policy_heads.0.bias", "policy_heads.1.weight", "policy_heads.1.bias", "policy_heads.2.weight", "policy_heads.2.bias", "policy_heads.3.weight", "policy_heads.3.bias", "policy_heads.4.weight", "policy_heads.4.bias", "policy_heads.5.weight", "policy_heads.5.bias", "policy_heads.6.weight", "policy_heads.6.bias", "policy_heads.7.weight", "policy_heads.7.bias", "value_head.weight", "value_head.bias".
2026-04-27 21:03:47 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:04:03 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-27 21:04:03 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-27 21:04:03 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-27 21:04:03 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-27 21:04:03 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:04:04 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 21:04:04 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pth)
2026-04-27 21:04:04 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pickle
2026-04-27 21:04:04 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth
2026-04-27 21:04:04 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-27 21:04:04 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-27 21:04:04 | [LEAGUE] Viewer использует agent-id=P2_Necrons_only_war_v1_final_ep2000_20260427_205826
2026-04-27 21:04:04 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-27 21:04:04 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:04:06 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-04-27 21:04:06 | Юниты: [('Necron Warriors', '2', 10), ('Necron Warriors', 'unit-281', 10)]
2026-04-27 21:04:06 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-27 21:04:06 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-27 21:04:06 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-27 21:04:06 | [DEPLOY] Order: model first, alternating
2026-04-27 21:04:06 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 21:04:06 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1265, coord=(21,5), attempt=1, reward=+0.021, score_before=0.000, score_after=0.413, reward_delta=+0.021, forward=0.088, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 21:04:06 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (21,5)
2026-04-27 21:04:06 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 21:04:06 | REQ: deploy cell accepted x=54, y=26
2026-04-27 21:04:06 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,54)
2026-04-27 21:04:06 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,54)
2026-04-27 21:04:06 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 21:04:06 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=423, coord=(7,3), attempt=1, reward=-0.000, score_before=0.413, score_after=0.405, reward_delta=-0.000, forward=0.071, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 21:04:06 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (7,3)
2026-04-27 21:04:07 | REQ: deploy cell accepted x=54, y=20
2026-04-27 21:04:08 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,54)
2026-04-27 21:04:08 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,54)
2026-04-27 21:04:08 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.020 total_deploy_reward=+0.020 avg_forward=0.080 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-27 21:04:08 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.020260149783208517, 'units': 2, 'total_deploy_reward': 0.020260149783208517, 'forward_sum': 0.15932203389830507, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.07966101694915254, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-27 21:04:08 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-27 21:04:08 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-27 21:04:08 | [MODEL] Архитектура сети: basic (источник: net_type)
2026-04-27 21:04:08 | Ошибка игры: Error(s) in loading state_dict for DQN:
	Missing key(s) in state_dict: "q_heads.0.weight", "q_heads.0.bias", "q_heads.1.weight", "q_heads.1.bias", "q_heads.2.weight", "q_heads.2.bias", "q_heads.3.weight", "q_heads.3.bias", "q_heads.4.weight", "q_heads.4.bias", "q_heads.5.weight", "q_heads.5.bias", "q_heads.6.weight", "q_heads.6.bias", "q_heads.7.weight", "q_heads.7.bias". 
	Unexpected key(s) in state_dict: "policy_heads.0.weight", "policy_heads.0.bias", "policy_heads.1.weight", "policy_heads.1.bias", "policy_heads.2.weight", "policy_heads.2.bias", "policy_heads.3.weight", "policy_heads.3.bias", "policy_heads.4.weight", "policy_heads.4.bias", "policy_heads.5.weight", "policy_heads.5.bias", "policy_heads.6.weight", "policy_heads.6.bias", "policy_heads.7.weight", "policy_heads.7.bias", "value_head.weight", "value_head.bias". . Место: game_controller._run_game_loop (File "C:\40kAI\.venv\Lib\site-packages\torch\nn\modules\module.py", line 2635, in load_state_dict). Что делать дальше: проверьте traceback ниже и исправьте источник ошибки в указанном файле/строке.
2026-04-27 21:04:08 | Traceback (последние вызовы):
2026-04-27 21:04:08 | Traceback (most recent call last):
2026-04-27 21:04:08 |   File "C:\40kAI\gym_mod\gym_mod\engine\game_controller.py", line 357, in _run_game_loop
2026-04-27 21:04:08 |     policy_net.load_state_dict(normalize_state_dict(checkpoint["policy_net"]))
2026-04-27 21:04:08 |   File "C:\40kAI\.venv\Lib\site-packages\torch\nn\modules\module.py", line 2635, in load_state_dict
2026-04-27 21:04:08 |     raise RuntimeError(
2026-04-27 21:04:08 | RuntimeError: Error(s) in loading state_dict for DQN:
2026-04-27 21:04:08 | 	Missing key(s) in state_dict: "q_heads.0.weight", "q_heads.0.bias", "q_heads.1.weight", "q_heads.1.bias", "q_heads.2.weight", "q_heads.2.bias", "q_heads.3.weight", "q_heads.3.bias", "q_heads.4.weight", "q_heads.4.bias", "q_heads.5.weight", "q_heads.5.bias", "q_heads.6.weight", "q_heads.6.bias", "q_heads.7.weight", "q_heads.7.bias". 
2026-04-27 21:04:08 | 	Unexpected key(s) in state_dict: "policy_heads.0.weight", "policy_heads.0.bias", "policy_heads.1.weight", "policy_heads.1.bias", "policy_heads.2.weight", "policy_heads.2.bias", "policy_heads.3.weight", "policy_heads.3.bias", "policy_heads.4.weight", "policy_heads.4.bias", "policy_heads.5.weight", "policy_heads.5.bias", "policy_heads.6.weight", "policy_heads.6.bias", "policy_heads.7.weight", "policy_heads.7.bias", "value_head.weight", "value_head.bias".
2026-04-27 21:04:08 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:05:43 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-27 21:05:43 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-27 21:05:43 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-27 21:05:43 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-27 21:05:43 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:05:44 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 21:05:44 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pth)
2026-04-27 21:05:44 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pickle
2026-04-27 21:05:44 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth
2026-04-27 21:05:44 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-27 21:05:44 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-27 21:05:44 | [LEAGUE] Viewer использует agent-id=P2_Necrons_only_war_v1_final_ep2000_20260427_205826
2026-04-27 21:05:44 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-27 21:05:44 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:05:45 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-04-27 21:05:45 | Юниты: [('Necron Warriors', '2', 10), ('Necron Warriors', 'unit-281', 10)]
2026-04-27 21:05:45 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-27 21:05:45 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-27 21:05:45 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-27 21:05:45 | [DEPLOY] Order: model first, alternating
2026-04-27 21:05:45 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 21:05:45 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=2044, coord=(34,4), attempt=1, reward=+0.020, score_before=0.000, score_after=0.405, reward_delta=+0.020, forward=0.071, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 21:05:45 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (34,4)
2026-04-27 21:05:45 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 21:05:45 | REQ: deploy cell accepted x=56, y=24
2026-04-27 21:05:45 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,56)
2026-04-27 21:05:45 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,56)
2026-04-27 21:05:45 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 21:05:45 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1149, coord=(19,9), attempt=1, reward=+0.001, score_before=0.405, score_after=0.425, reward_delta=+0.001, forward=0.114, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 21:05:45 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (19,9)
2026-04-27 21:05:46 | REQ: deploy cell accepted x=53, y=17
2026-04-27 21:05:46 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,53)
2026-04-27 21:05:46 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,53)
2026-04-27 21:05:46 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.092 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-27 21:05:46 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.021245565628695312, 'units': 2, 'total_deploy_reward': 0.021245565628695312, 'forward_sum': 0.18474576271186438, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.09237288135593219, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-27 21:05:46 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-27 21:05:46 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-27 21:05:46 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-27 21:05:46 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-27 21:05:46 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-27 21:05:46 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-27 21:05:46 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:05:47 | === БОЕВОЙ РАУНД 1 ===
2026-04-27 21:05:47 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-27 21:05:47 | --- ХОД PLAYER ---
2026-04-27 21:05:47 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-27 21:05:47 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-27 21:05:47 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-27 21:05:48 | REQ: move cell accepted (RMB) x=45, y=26, mode=advance
2026-04-27 21:05:48 | [MOVE] unit=11 advance to=(45,26) dist=11 M=5 adv=6
2026-04-27 21:05:48 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 21:05:52 | REQ: move cell accepted (RMB) x=45, y=17, mode=advance
2026-04-27 21:05:52 | [MOVE] unit=12 advance to=(45,17) dist=8 M=5 adv=3
2026-04-27 21:05:52 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 21:05:52 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-27 21:05:52 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-27 21:05:52 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-27 21:05:52 | --- ФАЗА ЧАРДЖА ---
2026-04-27 21:05:52 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-27 21:05:52 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-27 21:05:52 | Нет доступных целей для чарджа.
2026-04-27 21:05:52 | --- ФАЗА БОЯ ---
2026-04-27 21:05:52 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=38.00, range=24.00, delta=+14.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:05:52 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=38.00, range=24.00, delta=+14.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:05:52 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:05:52 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:05:52 | --- ХОД MODEL ---
2026-04-27 21:05:52 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-27 21:05:55 | [PACE] ack phase=command unit_id=None seq=1 step=command_resolve ok=True
2026-04-27 21:05:55 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-27 21:05:55 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-27 21:05:56 | [PACE] ack phase=movement unit_id=21 seq=2 step=before_unit ok=True
2026-04-27 21:05:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (34, 4). Выбор reachable_idx=13/271, mode=normal, advance=нет, distance=4
2026-04-27 21:05:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (30, 2)
2026-04-27 21:05:56 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 21:05:57 | [PACE] ack phase=movement unit_id=22 seq=3 step=before_unit ok=True
2026-04-27 21:05:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (19, 9). Выбор reachable_idx=22/481, mode=normal, advance=нет, distance=5
2026-04-27 21:05:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (15, 14)
2026-04-27 21:05:57 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 21:05:57 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-27 21:06:03 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-27 21:06:03 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-27 21:06:03 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-27 21:06:03 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-27 21:06:03 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 21:06:03 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pth)
2026-04-27 21:06:03 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pickle
2026-04-27 21:06:03 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth
2026-04-27 21:06:03 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-27 21:06:03 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-27 21:06:03 | [LEAGUE] Viewer использует agent-id=P2_Necrons_only_war_v1_final_ep2000_20260427_205826
2026-04-27 21:06:03 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-27 21:06:03 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 21 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=5, cells_rapid=2, rapid_fire=1, source_cell=(1, 1), target_filter_size=2, max_target_dist=5, inferred_from_targets=1. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-27 21:06:03 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 21; source=(1, 1), full_cells=5, rapid_cells=2, вошло=49, rapid=16, не вошло=2351, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-27 21:06:03 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:06:13 | Roll-off Attacker/Defender: enemy=2 model=6 -> attacker=model
2026-04-27 21:06:13 | Юниты: [('Necron Warriors', '2', 10), ('Necron Warriors', 'unit-281', 10)]
2026-04-27 21:06:13 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-27 21:06:13 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-27 21:06:13 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-27 21:06:13 | [DEPLOY] Order: model first, alternating
2026-04-27 21:06:13 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 21:06:13 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=541, coord=(9,1), attempt=1, reward=+0.014, score_before=0.000, score_after=0.289, reward_delta=+0.014, forward=0.020, spread=1.000, edge=0.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 21:06:13 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (9,1)
2026-04-27 21:06:13 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 21:06:14 | REQ: deploy cell accepted x=52, y=25
2026-04-27 21:06:14 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,52)
2026-04-27 21:06:14 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,52)
2026-04-27 21:06:14 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 21:06:14 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1502, coord=(25,2), attempt=1, reward=+0.001, score_before=0.289, score_after=0.316, reward_delta=+0.001, forward=0.029, spread=1.000, edge=0.250, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 21:06:14 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (25,2)
2026-04-27 21:06:29 | REQ: deploy cell accepted x=54, y=18
2026-04-27 21:06:29 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,54)
2026-04-27 21:06:29 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,54)
2026-04-27 21:06:29 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.016 total_deploy_reward=+0.016 avg_forward=0.025 avg_spread=1.000 avg_edge=0.125 avg_cover=0.000
2026-04-27 21:06:29 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.015786361844698463, 'units': 2, 'total_deploy_reward': 0.015786361844698463, 'forward_sum': 0.04915254237288136, 'spread_sum': 2.0, 'edge_sum': 0.25, 'cover_sum': 0.0, 'avg_forward': 0.02457627118644068, 'avg_spread': 1.0, 'avg_edge': 0.125, 'avg_cover': 0.0}
2026-04-27 21:06:29 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-27 21:06:29 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-27 21:06:29 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-27 21:06:29 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-27 21:06:29 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-27 21:06:29 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-27 21:06:29 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:06:40 | === БОЕВОЙ РАУНД 1 ===
2026-04-27 21:06:40 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-27 21:06:40 | --- ХОД PLAYER ---
2026-04-27 21:06:40 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-27 21:06:40 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-27 21:06:40 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-27 21:11:01 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-27 21:11:01 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-27 21:11:01 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-27 21:11:01 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-27 21:11:01 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 21:11:01 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pth)
2026-04-27 21:11:01 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pickle
2026-04-27 21:11:01 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth
2026-04-27 21:11:02 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-27 21:11:02 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-27 21:11:02 | [LEAGUE] Viewer использует agent-id=P2_Necrons_only_war_v1_final_ep2000_20260427_205826
2026-04-27 21:11:02 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-27 21:11:02 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:11:03 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-04-27 21:11:03 | Юниты: [('Necron Warriors', '2', 10), ('Necron Warriors', 'unit-281', 10)]
2026-04-27 21:11:03 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-27 21:11:03 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-27 21:11:03 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-27 21:11:03 | [DEPLOY] Order: model first, alternating
2026-04-27 21:11:03 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 21:11:03 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1391, coord=(23,11), attempt=1, reward=+0.023, score_before=0.000, score_after=0.460, reward_delta=+0.023, forward=0.190, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 21:11:03 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (23,11)
2026-04-27 21:11:03 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 21:11:03 | REQ: deploy cell accepted x=47, y=27
2026-04-27 21:11:03 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (27,47)
2026-04-27 21:11:03 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (27,47)
2026-04-27 21:11:03 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 21:11:03 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1503, coord=(25,3), attempt=1, reward=-0.011, score_before=0.460, score_after=0.243, reward_delta=-0.011, forward=0.122, spread=0.333, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 21:11:03 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (25,3)
2026-04-27 21:11:04 | REQ: deploy cell accepted x=50, y=21
2026-04-27 21:11:04 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,50)
2026-04-27 21:11:04 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,50)
2026-04-27 21:11:04 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.012 total_deploy_reward=+0.012 avg_forward=0.156 avg_spread=0.667 avg_edge=1.000 avg_cover=0.000
2026-04-27 21:11:04 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.012140323216397318, 'units': 2, 'total_deploy_reward': 0.012140323216397318, 'forward_sum': 0.311864406779661, 'spread_sum': 1.3333333333333333, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.1559322033898305, 'avg_spread': 0.6666666666666666, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-27 21:11:04 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-27 21:11:04 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-27 21:11:04 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-27 21:11:04 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-27 21:11:04 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-27 21:11:04 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-27 21:11:04 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:11:05 | === БОЕВОЙ РАУНД 1 ===
2026-04-27 21:11:05 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-27 21:11:05 | --- ХОД PLAYER ---
2026-04-27 21:11:05 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-27 21:11:05 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-27 21:11:05 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-27 21:11:05 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:11:06 | REQ: move cell accepted (RMB) x=37, y=30, mode=advance
2026-04-27 21:11:06 | [MOVE] unit=11 advance to=(37,30) dist=10 M=5 adv=5
2026-04-27 21:11:06 | [COVER][MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-04-27 21:11:06 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=benefit of cover cover_active=1 save_base=4 ap=0 inv=0 save_target=- save_rolls=[]
2026-04-27 21:11:06 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-27 21:11:06 | [COVER][MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-04-27 21:11:06 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-27 21:11:06 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-27 21:11:06 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-27 21:11:06 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-27 21:11:06 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-27 21:11:06 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-27 21:11:06 | Оружие: Gauss flayer
2026-04-27 21:11:06 | FX: найдена строка оружия: Gauss flayer.
2026-04-27 21:11:06 | BS оружия: 4+
2026-04-27 21:11:06 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-27 21:11:06 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-27 21:11:06 | Save цели: 4+ (invul: нет)
2026-04-27 21:11:06 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-04-27 21:11:06 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-27 21:11:06 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-27 21:11:06 | Правило: Overwatch: попадания только на 6+
2026-04-27 21:11:06 | Эффект: benefit of cover
2026-04-27 21:11:06 | Hit rolls:    [1, 2, 5, 5, 3, 5, 4, 1, 2, 1]  -> hits: 0
2026-04-27 21:11:06 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-27 21:11:06 | FX: найден итог урона = 0.0.
2026-04-27 21:11:06 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0, outcome=miss).
2026-04-27 21:11:06 | FX: позиция эффекта start=(276.0,564.0) end=(1140.0,660.0).
2026-04-27 21:11:06 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-27 21:11:06 | 📌 -------------------------

2026-04-27 21:11:07 | REQ: move cell accepted (RMB) x=39, y=23, mode=advance
2026-04-27 21:11:07 | [MOVE] unit=12 advance to=(39,23) dist=11 M=5 adv=6
2026-04-27 21:11:07 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 21:11:07 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-27 21:11:07 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-27 21:11:07 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-27 21:11:07 | --- ФАЗА ЧАРДЖА ---
2026-04-27 21:11:07 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-27 21:11:07 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-27 21:11:07 | Нет доступных целей для чарджа.
2026-04-27 21:11:07 | --- ФАЗА БОЯ ---
2026-04-27 21:11:07 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:11:07 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:11:07 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:11:07 | --- ХОД MODEL ---
2026-04-27 21:11:07 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-27 21:11:07 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:11:07 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-27 21:11:07 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-27 21:11:07 | FX: найдена строка оружия: Gauss flayer.
2026-04-27 21:11:07 | FX: найден итог урона = 0.0.
2026-04-27 21:11:07 | FX: дубликат отчёта, эффект не создаём.
2026-04-27 21:11:10 | [PACE] ack phase=command unit_id=None seq=1 step=command_resolve ok=True
2026-04-27 21:11:10 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-27 21:11:10 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-27 21:11:11 | [PACE] ack phase=movement unit_id=21 seq=2 step=before_unit ok=True
2026-04-27 21:11:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (23, 11). Выбор reachable_idx=13/526, mode=normal, advance=нет, distance=4
2026-04-27 21:11:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (19, 7)
2026-04-27 21:11:11 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-27 21:11:12 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:11:12 | [PACE] ack phase=movement unit_id=22 seq=3 step=before_unit ok=True
2026-04-27 21:11:12 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (25, 3). Выбор reachable_idx=22/343, mode=normal, advance=нет, distance=3
2026-04-27 21:11:12 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (22, 3)
2026-04-27 21:11:12 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 21:11:12 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-27 21:11:13 | [PACE] ack phase=shooting unit_id=21 seq=4 step=before_unit ok=True
2026-04-27 21:11:13 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:11:13 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:11:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-27 21:11:14 | [PACE] ack phase=shooting unit_id=22 seq=5 step=before_unit ok=True
2026-04-27 21:11:14 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:11:14 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:11:14 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-27 21:11:14 | --- ФАЗА ЧАРДЖА ---
2026-04-27 21:11:15 | [PACE] ack phase=charge unit_id=21 seq=6 step=before_unit ok=True
2026-04-27 21:11:15 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-27 21:11:15 | [PACE] ack phase=charge unit_id=22 seq=7 step=before_unit ok=True
2026-04-27 21:11:15 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-27 21:11:15 | [MODEL] Чардж: нет доступных целей
2026-04-27 21:11:15 | --- ФАЗА БОЯ ---
2026-04-27 21:11:15 | [MODEL] Ближний бой: нет доступных атак
2026-04-27 21:11:15 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-27 21:11:15 | Итерация 0 завершена с наградой tensor([-0.0033], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-04-27 21:11:15 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 1, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-27 21:11:15 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 1, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-04-27 21:11:16 | === БОЕВОЙ РАУНД 2 ===
2026-04-27 21:11:16 | --- ХОД PLAYER ---
2026-04-27 21:11:16 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-27 21:11:16 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-27 21:11:16 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-27 21:11:17 | REQ: move cell accepted (RMB) x=30, y=25, mode=advance
2026-04-27 21:11:17 | [MOVE] unit=11 advance to=(30,25) dist=7 M=5 adv=2
2026-04-27 21:11:17 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[4, 6]
2026-04-27 21:11:18 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-27 21:11:18 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-27 21:11:18 | 
🎲 Бросок сейвы (save): 2D6
2026-04-27 21:11:18 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-27 21:11:18 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-27 21:11:18 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-27 21:11:18 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-27 21:11:18 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-27 21:11:18 | Оружие: Gauss flayer
2026-04-27 21:11:18 | FX: найдена строка оружия: Gauss flayer.
2026-04-27 21:11:18 | BS оружия: 4+
2026-04-27 21:11:18 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-27 21:11:18 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-27 21:11:18 | Save цели: 4+ (invul: нет)
2026-04-27 21:11:18 | Benefit of Cover: не активен.
2026-04-27 21:11:18 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-27 21:11:18 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-27 21:11:18 | Правило: Overwatch: попадания только на 6+
2026-04-27 21:11:18 | Hit rolls:    [2, 1, 3, 6, 5, 4, 1, 6, 3, 3]  -> hits: 2 (crits: 2)
2026-04-27 21:11:18 | Save rolls:   [4, 6]  (цель 4+) -> failed saves: 0
2026-04-27 21:11:18 | FX: найден failed saves = 0.
2026-04-27 21:11:18 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-27 21:11:18 | FX: найден итог урона = 0.0.
2026-04-27 21:11:18 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-27 21:11:18 | FX: позиция эффекта start=(180.0,468.0) end=(900.0,732.0).
2026-04-27 21:11:18 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-27 21:11:18 | 📌 -------------------------

2026-04-27 21:11:19 | REQ: move cell accepted (RMB) x=36, y=29, mode=advance
2026-04-27 21:11:19 | [MOVE] unit=12 advance to=(36,29) dist=6 M=5 adv=1
2026-04-27 21:11:19 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 21:11:19 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-27 21:11:19 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-27 21:11:19 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-27 21:11:19 | --- ФАЗА ЧАРДЖА ---
2026-04-27 21:11:19 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-27 21:11:19 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-27 21:11:19 | Нет доступных целей для чарджа.
2026-04-27 21:11:19 | --- ФАЗА БОЯ ---
2026-04-27 21:11:19 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:11:19 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:11:19 | --- ХОД MODEL ---
2026-04-27 21:11:19 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-27 21:29:47 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-27 21:29:47 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-27 21:29:47 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-27 21:29:47 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-27 21:29:48 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 21:29:48 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pth)
2026-04-27 21:29:48 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pickle
2026-04-27 21:29:48 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth
2026-04-27 21:29:48 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-27 21:29:48 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-27 21:29:48 | [LEAGUE] Viewer использует agent-id=P2_Necrons_only_war_v1_final_ep2000_20260427_205826
2026-04-27 21:29:48 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-27 21:29:48 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:29:48 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-27 21:29:48 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-27 21:29:48 | FX: найдена строка оружия: Gauss flayer.
2026-04-27 21:29:48 | FX: найден failed saves = 0.
2026-04-27 21:29:48 | FX: найден итог урона = 0.0.
2026-04-27 21:29:48 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-27 21:29:48 | FX: позиция эффекта start=(36.0,36.0) end=(36.0,132.0).
2026-04-27 21:29:48 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-27 21:29:56 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-04-27 21:29:56 | Юниты: [('Necron Warriors', '2', 10), ('Necron Warriors', 'unit-281', 10)]
2026-04-27 21:29:56 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-27 21:29:56 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-27 21:29:56 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-27 21:29:56 | [DEPLOY] Order: model first, alternating
2026-04-27 21:29:56 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 21:29:56 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1022, coord=(17,2), attempt=1, reward=+0.017, score_before=0.000, score_after=0.343, reward_delta=+0.017, forward=0.037, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 21:29:56 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (17,2)
2026-04-27 21:29:56 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-27 21:29:57 | REQ: deploy cell accepted x=53, y=25
2026-04-27 21:29:57 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,53)
2026-04-27 21:29:57 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,53)
2026-04-27 21:29:57 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-27 21:29:57 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=2044, coord=(34,4), attempt=1, reward=+0.002, score_before=0.343, score_after=0.374, reward_delta=+0.002, forward=0.054, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-27 21:29:57 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (34,4)
2026-04-27 21:29:57 | REQ: deploy cell accepted x=53, y=17
2026-04-27 21:29:57 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,53)
2026-04-27 21:29:57 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,53)
2026-04-27 21:29:57 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.046 avg_spread=1.000 avg_edge=0.625 avg_cover=0.000
2026-04-27 21:29:57 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.01870319274733938, 'units': 2, 'total_deploy_reward': 0.01870319274733938, 'forward_sum': 0.09152542372881356, 'spread_sum': 2.0, 'edge_sum': 1.25, 'cover_sum': 0.0, 'avg_forward': 0.04576271186440678, 'avg_spread': 1.0, 'avg_edge': 0.625, 'avg_cover': 0.0}
2026-04-27 21:29:57 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-27 21:29:57 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-27 21:29:57 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-27 21:29:57 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-27 21:29:57 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-27 21:29:57 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-27 21:29:57 | FX: перепроигрываю 30 строк(и) лога.
2026-04-27 21:29:59 | === БОЕВОЙ РАУНД 1 ===
2026-04-27 21:29:59 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-27 21:29:59 | --- ХОД PLAYER ---
2026-04-27 21:29:59 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-27 21:29:59 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-27 21:29:59 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-27 21:30:06 | REQ: move cell accepted (RMB) x=43, y=30, mode=advance
2026-04-27 21:30:06 | [MOVE] unit=11 advance to=(43,30) dist=10 M=5 adv=5
2026-04-27 21:30:06 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 21:30:06 | REQ: move cell accepted (RMB) x=42, y=18, mode=advance
2026-04-27 21:30:06 | [MOVE] unit=12 advance to=(42,18) dist=11 M=5 adv=6
2026-04-27 21:30:07 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 21:30:07 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-27 21:30:07 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-27 21:30:07 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-27 21:30:07 | --- ФАЗА ЧАРДЖА ---
2026-04-27 21:30:07 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-27 21:30:07 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-27 21:30:07 | Нет доступных целей для чарджа.
2026-04-27 21:30:07 | --- ФАЗА БОЯ ---
2026-04-27 21:30:07 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=38.00, range=24.00, delta=+14.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:30:07 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=37.00, range=24.00, delta=+13.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:30:07 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=36.00, range=24.00, delta=+12.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:30:07 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:30:07 | --- ХОД MODEL ---
2026-04-27 21:30:07 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-27 21:30:10 | [PACE] ack phase=command unit_id=None seq=1 step=command_resolve ok=True
2026-04-27 21:30:10 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-27 21:30:10 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-27 21:30:12 | [PACE] ack phase=movement unit_id=21 seq=2 step=before_unit ok=True
2026-04-27 21:30:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (17, 2). Выбор reachable_idx=7/321, mode=normal, advance=нет, distance=5
2026-04-27 21:30:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (12, 6)
2026-04-27 21:30:12 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 21:30:13 | [PACE] ack phase=movement unit_id=22 seq=3 step=before_unit ok=True
2026-04-27 21:30:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (34, 4). Выбор reachable_idx=22/271, mode=normal, advance=нет, distance=3
2026-04-27 21:30:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (31, 1)
2026-04-27 21:30:13 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-27 21:30:13 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-27 21:30:14 | [PACE] ack phase=shooting unit_id=21 seq=4 step=before_unit ok=True
2026-04-27 21:30:14 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:30:14 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:30:14 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-27 21:30:14 | [PACE] ack phase=shooting unit_id=22 seq=5 step=before_unit ok=True
2026-04-27 21:30:14 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=39.00, range=24.00, delta=+15.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:30:14 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=38.00, range=24.00, delta=+14.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-27 21:30:14 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-27 21:30:14 | --- ФАЗА ЧАРДЖА ---
2026-04-27 21:30:15 | [PACE] ack phase=charge unit_id=21 seq=6 step=before_unit ok=True
2026-04-27 21:30:15 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-28 16:44:40 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-28 16:44:40 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-28 16:44:40 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-28 16:44:40 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-28 16:44:41 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-28 16:44:41 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pth)
2026-04-28 16:44:41 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260427-205825\model-20260427-205825.pickle
2026-04-28 16:44:41 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260427-205825\checkpoint_ep2000.pth
2026-04-28 16:44:41 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-28 16:44:41 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-28 16:44:41 | [LEAGUE] Viewer использует agent-id=P2_Necrons_only_war_v1_final_ep2000_20260427_205826
2026-04-28 16:44:41 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-28 16:44:41 | FX: перепроигрываю 30 строк(и) лога.
2026-04-28 16:45:47 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-04-28 16:45:47 | Юниты: [('Necron Warriors', '2', 10), ('Necron Warriors', 'unit-281', 10)]
2026-04-28 16:45:47 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-28 16:45:47 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-28 16:45:47 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-28 16:45:47 | [DEPLOY] Order: model first, alternating
2026-04-28 16:45:47 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-28 16:45:47 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=2225, coord=(37,5), attempt=1, reward=+0.018, score_before=0.000, score_after=0.367, reward_delta=+0.018, forward=0.088, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-28 16:45:47 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (37,5)
2026-04-28 16:45:47 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-28 16:45:48 | REQ: deploy cell accepted x=47, y=23
2026-04-28 16:45:48 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (23,47)
2026-04-28 16:45:48 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (23,47)
2026-04-28 16:45:48 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-28 16:45:48 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=246, coord=(4,6), attempt=1, reward=+0.001, score_before=0.367, score_after=0.394, reward_delta=+0.001, forward=0.097, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-28 16:45:48 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (4,6)
2026-04-28 16:45:48 | REQ: deploy cell accepted x=49, y=17
2026-04-28 16:45:48 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,49)
2026-04-28 16:45:48 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,49)
2026-04-28 16:45:48 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.020 total_deploy_reward=+0.020 avg_forward=0.092 avg_spread=1.000 avg_edge=0.625 avg_cover=0.000
2026-04-28 16:45:48 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.019688608592826173, 'units': 2, 'total_deploy_reward': 0.019688608592826173, 'forward_sum': 0.1847457627118644, 'spread_sum': 2.0, 'edge_sum': 1.25, 'cover_sum': 0.0, 'avg_forward': 0.0923728813559322, 'avg_spread': 1.0, 'avg_edge': 0.625, 'avg_cover': 0.0}
2026-04-28 16:45:48 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-28 16:45:48 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-28 16:45:48 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-28 16:45:48 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-28 16:45:48 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-28 16:45:48 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-28 16:45:48 | FX: перепроигрываю 30 строк(и) лога.
2026-04-28 16:45:49 | === БОЕВОЙ РАУНД 1 ===
2026-04-28 16:45:49 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-28 16:45:49 | --- ХОД PLAYER ---
2026-04-28 16:45:49 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-28 16:45:49 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-28 16:45:49 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-28 16:45:50 | REQ: move cell accepted (RMB) x=36, y=27, mode=advance
2026-04-28 16:45:50 | [MOVE] unit=11 advance to=(36,27) dist=11 M=5 adv=6
2026-04-28 16:45:51 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-28 16:45:51 | REQ: move cell accepted (RMB) x=38, y=18, mode=advance
2026-04-28 16:45:51 | [MOVE] unit=12 advance to=(38,18) dist=11 M=5 adv=6
2026-04-28 16:45:52 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-28 16:45:52 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-28 16:45:52 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-28 16:45:52 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-28 16:45:52 | --- ФАЗА ЧАРДЖА ---
2026-04-28 16:45:52 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-28 16:45:52 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-28 16:45:52 | Нет доступных целей для чарджа.
2026-04-28 16:45:52 | --- ФАЗА БОЯ ---
2026-04-28 16:45:52 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-28 16:45:52 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-28 16:45:52 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-28 16:45:52 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-28 16:45:52 | --- ХОД MODEL ---
2026-04-28 16:45:52 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-28 16:45:53 | [PACE] ack phase=command unit_id=None seq=1 step=command_resolve ok=True
2026-04-28 16:45:53 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-28 16:45:53 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-28 16:45:54 | [PACE] ack phase=movement unit_id=21 seq=2 step=before_unit ok=True
2026-04-28 16:45:54 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (37, 5). Выбор reachable_idx=13/237, mode=normal, advance=нет, distance=4
2026-04-28 16:45:54 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (33, 1)
2026-04-28 16:45:54 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-28 16:45:54 | [PACE] ack phase=movement unit_id=22 seq=3 step=before_unit ok=True
2026-04-28 16:45:54 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (4, 6). Выбор reachable_idx=1/287, mode=normal, advance=нет, distance=5
2026-04-28 16:45:54 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 1)
2026-04-28 16:45:54 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-28 16:45:54 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-28 16:45:55 | [PACE] ack phase=shooting unit_id=21 seq=4 step=before_unit ok=True
2026-04-28 16:45:55 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-28 16:45:55 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-28 16:45:55 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-28 16:45:56 | [PACE] ack phase=shooting unit_id=22 seq=5 step=before_unit ok=True
2026-04-28 16:45:56 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-28 16:45:56 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-28 16:45:56 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-28 16:45:56 | --- ФАЗА ЧАРДЖА ---
2026-04-28 16:45:57 | [PACE] ack phase=charge unit_id=21 seq=6 step=before_unit ok=True
2026-04-28 16:45:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-28 16:45:57 | FX: перепроигрываю 30 строк(и) лога.
2026-04-28 16:45:57 | [PACE] ack phase=charge unit_id=22 seq=7 step=before_unit ok=True
2026-04-28 16:45:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-28 16:45:57 | [MODEL] Чардж: нет доступных целей
2026-04-28 16:45:57 | --- ФАЗА БОЯ ---
2026-04-28 16:45:57 | [MODEL] Ближний бой: нет доступных атак
2026-04-28 16:45:57 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-28 16:45:57 | Итерация 0 завершена с наградой tensor([-0.0200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-04-28 16:45:57 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-28 16:45:57 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

