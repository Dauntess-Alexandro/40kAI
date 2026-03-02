2026-03-02 18:30:21 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-02 18:30:21 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-02 18:30:21 | [VIEWER][TERRAIN] features=0
2026-03-02 18:30:22 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-02 18:30:24 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-39-29972.pickle
2026-03-02 18:30:24 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-39-29972.pth
2026-03-02 18:30:24 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-02 18:30:30 | Roll-off Attacker/Defender: enemy=1 model=5 -> attacker=model
2026-03-02 18:30:30 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-02 18:30:30 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-02 18:30:30 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-02 18:30:30 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-02 18:30:30 | [DEPLOY] Order: model first, alternating
2026-03-02 18:30:30 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.000
2026-03-02 18:30:30 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=843, coord=(14,3), attempt=1, reward=+0.024, score_before=0.000, score_after=0.475, reward_delta=+0.024, forward=0.054, spread=1.000, edge=1.000, cover=0.000
2026-03-02 18:30:30 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (14,3)
2026-03-02 18:30:30 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-02 18:30:31 | REQ: deploy cell accepted x=51, y=31
2026-03-02 18:30:31 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (31,51)
2026-03-02 18:30:31 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (31,51)
2026-03-02 18:30:31 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.000
2026-03-02 18:30:31 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=2287, coord=(38,7), attempt=1, reward=-0.002, score_before=0.475, score_after=0.438, reward_delta=-0.002, forward=0.088, spread=1.000, edge=0.500, cover=0.000
2026-03-02 18:30:31 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (38,7)
2026-03-02 18:30:31 | REQ: deploy cell accepted x=50, y=17
2026-03-02 18:30:32 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,50)
2026-03-02 18:30:32 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,50)
2026-03-02 18:30:32 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.071 avg_spread=1.000 avg_edge=0.750 avg_cover=0.000
2026-03-02 18:30:32 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.021892655367231638, 'units': 2, 'total_deploy_reward': 0.021892655367231638, 'forward_sum': 0.1423728813559322, 'spread_sum': 2.0, 'edge_sum': 1.5, 'cover_sum': 0.0, 'avg_forward': 0.0711864406779661, 'avg_spread': 1.0, 'avg_edge': 0.75, 'avg_cover': 0.0}
2026-03-02 18:30:32 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-02 18:30:32 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-02 18:30:32 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-02 18:30:32 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-02 18:30:32 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-02 18:30:32 | [VIEWER][TERRAIN] features=2
2026-03-02 18:30:32 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-02 18:30:32 | FX: перепроигрываю 30 строк(и) лога.
2026-03-02 18:30:37 | === БОЕВОЙ РАУНД 1 ===
2026-03-02 18:30:37 | --- ХОД PLAYER ---
2026-03-02 18:30:37 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-02 18:30:37 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-02 18:30:37 | --- ФАЗА ДВИЖЕНИЯ ---
