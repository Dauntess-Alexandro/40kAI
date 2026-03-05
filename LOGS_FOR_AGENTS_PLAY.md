2026-03-04 16:00:50 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-04 16:00:50 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-04 16:00:50 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-04 16:00:50 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-04 16:00:50 | FX: перепроигрываю 30 строк(и) лога.
2026-03-04 16:00:51 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-04 16:01:01 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-25-334461.pickle
2026-03-04 16:01:01 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-25-334461.pth
2026-03-04 16:01:01 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-04 16:01:09 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-03-04 16:01:09 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-04 16:01:09 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-04 16:01:09 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-04 16:01:09 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-04 16:01:09 | [DEPLOY] Order: model first, alternating
2026-03-04 16:01:09 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-04 16:01:09 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=2171, coord=(36,11), attempt=1, reward=+0.023, score_before=0.000, score_after=0.460, reward_delta=+0.023, forward=0.190, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-04 16:01:09 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (36,11)
2026-03-04 16:01:09 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-04 16:01:09 | REQ: deploy cell accepted x=52, y=26
2026-03-04 16:01:09 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,52)
2026-03-04 16:01:09 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,52)
2026-03-04 16:01:09 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-04 16:01:09 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1862, coord=(31,2), attempt=1, reward=-0.005, score_before=0.460, score_after=0.355, reward_delta=-0.005, forward=0.114, spread=0.833, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-04 16:01:09 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (31,2)
2026-03-04 16:01:10 | REQ: deploy cell accepted x=51, y=19
2026-03-04 16:01:10 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,51)
2026-03-04 16:01:10 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,51)
2026-03-04 16:01:10 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.018 total_deploy_reward=+0.018 avg_forward=0.152 avg_spread=0.917 avg_edge=0.875 avg_cover=0.000
2026-03-04 16:01:10 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.017757193535672056, 'units': 2, 'total_deploy_reward': 0.017757193535672056, 'forward_sum': 0.30338983050847457, 'spread_sum': 1.8333333333333335, 'edge_sum': 1.75, 'cover_sum': 0.0, 'avg_forward': 0.15169491525423728, 'avg_spread': 0.9166666666666667, 'avg_edge': 0.875, 'avg_cover': 0.0}
2026-03-04 16:01:10 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-04 16:01:10 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-04 16:01:10 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-04 16:01:10 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-04 16:01:10 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-04 16:01:10 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-04 16:01:10 | FX: перепроигрываю 30 строк(и) лога.
2026-03-04 16:01:13 | === БОЕВОЙ РАУНД 1 ===
2026-03-04 16:01:13 | --- ХОД PLAYER ---
2026-03-04 16:01:13 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-04 16:01:13 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-04 16:01:13 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-05 09:34:45 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-05 09:34:45 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-05 09:34:45 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-05 09:34:45 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-05 09:34:46 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-05 09:34:56 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-25-334461.pickle
2026-03-05 09:34:56 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-25-334461.pth
2026-03-05 09:34:56 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-05 09:34:59 | Roll-off Attacker/Defender: enemy=1 model=5 -> attacker=model
2026-03-05 09:34:59 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-05 09:34:59 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-05 09:34:59 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-05 09:34:59 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-05 09:34:59 | [DEPLOY] Order: model first, alternating
2026-03-05 09:34:59 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-05 09:34:59 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=728, coord=(12,8), attempt=1, reward=+0.022, score_before=0.000, score_after=0.437, reward_delta=+0.022, forward=0.139, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-05 09:34:59 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (12,8)
2026-03-05 09:34:59 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-05 09:34:59 | REQ: deploy cell accepted x=49, y=29
2026-03-05 09:34:59 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (29,49)
2026-03-05 09:34:59 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (29,49)
2026-03-05 09:34:59 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-05 09:34:59 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1508, coord=(25,8), attempt=1, reward=+0.000, score_before=0.437, score_after=0.437, reward_delta=+0.000, forward=0.139, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-05 09:34:59 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (25,8)
2026-03-05 09:35:00 | REQ: deploy cell accepted x=49, y=20
2026-03-05 09:35:02 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,49)
2026-03-05 09:35:02 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,49)
2026-03-05 09:35:02 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.139 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-05 09:35:02 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02183681513598739, 'units': 2, 'total_deploy_reward': 0.02183681513598739, 'forward_sum': 0.27796610169491526, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.13898305084745763, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-05 09:35:02 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-05 09:35:02 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-05 09:35:02 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-05 09:35:02 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-05 09:35:02 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-05 09:35:02 | FX: перепроигрываю 30 строк(и) лога.
2026-03-05 09:35:18 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-05 09:35:18 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-05 09:35:18 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-05 09:35:18 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-05 09:35:18 | FX: перепроигрываю 30 строк(и) лога.
2026-03-05 09:35:19 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-05 09:35:28 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-25-334461.pickle
2026-03-05 09:35:28 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-25-334461.pth
2026-03-05 09:35:28 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-05 09:35:34 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-03-05 09:35:34 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-05 09:35:34 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-05 09:35:34 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-05 09:35:34 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-05 09:35:34 | [DEPLOY] Order: model first, alternating
2026-03-05 09:35:34 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-05 09:35:34 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1085, coord=(18,5), attempt=1, reward=+0.021, score_before=0.000, score_after=0.413, reward_delta=+0.021, forward=0.088, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-05 09:35:34 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (18,5)
2026-03-05 09:35:34 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-05 09:35:35 | REQ: deploy cell accepted x=52, y=30
2026-03-05 09:35:35 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (30,52)
2026-03-05 09:35:35 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (30,52)
2026-03-05 09:35:35 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-05 09:35:35 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=2050, coord=(34,10), attempt=1, reward=+0.001, score_before=0.413, score_after=0.433, reward_delta=+0.001, forward=0.131, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-05 09:35:35 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (34,10)
2026-03-05 09:35:35 | REQ: deploy cell accepted x=51, y=17
2026-03-05 09:35:36 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,51)
2026-03-05 09:35:36 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,51)
2026-03-05 09:35:36 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.109 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-05 09:35:36 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.021639731966890025, 'units': 2, 'total_deploy_reward': 0.021639731966890025, 'forward_sum': 0.21864406779661016, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.10932203389830508, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-05 09:35:36 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-05 09:35:36 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-05 09:35:36 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-05 09:35:36 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-05 09:35:36 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-05 09:35:36 | FX: перепроигрываю 30 строк(и) лога.
2026-03-05 09:35:38 | Выбрано на карте: unit_id=11, name=Necron Warriors
