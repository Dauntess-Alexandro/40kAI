2026-03-04 13:01:49 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-04 13:01:49 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-04 13:01:49 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-04 13:01:49 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-04 13:01:50 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-04 13:02:00 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-21-622590.pickle
2026-03-04 13:02:00 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-21-622590.pth
2026-03-04 13:02:00 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-04 13:02:24 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-03-04 13:02:24 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-04 13:02:24 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-04 13:02:24 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-04 13:02:24 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-04 13:02:24 | [DEPLOY] Order: model first, alternating
2026-03-04 13:02:24 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-04 13:02:24 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1328, coord=(22,8), attempt=1, reward=+0.022, score_before=0.000, score_after=0.437, reward_delta=+0.022, forward=0.139, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-04 13:02:24 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (22,8)
2026-03-04 13:02:24 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-04 13:02:24 | REQ: deploy cell accepted x=49, y=28
2026-03-04 13:02:24 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (28,49)
2026-03-04 13:02:24 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (28,49)
2026-03-04 13:02:24 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-04 13:02:24 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=847, coord=(14,7), attempt=1, reward=-0.000, score_before=0.437, score_after=0.433, reward_delta=-0.000, forward=0.131, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-04 13:02:24 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (14,7)
2026-03-04 13:02:25 | REQ: deploy cell accepted x=48, y=17
2026-03-04 13:02:25 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,48)
2026-03-04 13:02:25 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,48)
2026-03-04 13:02:25 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.135 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-04 13:02:25 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.021639731966890025, 'units': 2, 'total_deploy_reward': 0.021639731966890025, 'forward_sum': 0.2694915254237288, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.1347457627118644, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-04 13:02:25 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-04 13:02:25 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-04 13:02:25 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-04 13:02:25 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-04 13:02:25 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-04 13:02:25 | FX: перепроигрываю 30 строк(и) лога.
