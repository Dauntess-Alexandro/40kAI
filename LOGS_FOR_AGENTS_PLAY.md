2026-03-17 15:50:26 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-17 15:50:26 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-17 15:50:26 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-17 15:50:26 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-17 15:50:27 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-17 15:50:31 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-15-834701.pickle
2026-03-17 15:50:31 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-15-834701.pth
2026-03-17 15:50:31 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-17 15:50:41 | Roll-off Attacker/Defender: enemy=2 model=4 -> attacker=model
2026-03-17 15:50:41 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-17 15:50:41 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-17 15:50:41 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-17 15:50:41 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-17 15:50:41 | [DEPLOY] Order: model first, alternating
2026-03-17 15:50:41 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-17 15:50:41 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=2045, coord=(34,5), attempt=1, reward=+0.021, score_before=0.000, score_after=0.413, reward_delta=+0.021, forward=0.088, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-17 15:50:41 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (34,5)
2026-03-17 15:50:41 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-17 15:50:42 | REQ: deploy cell accepted x=48, y=25
2026-03-17 15:50:42 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,48)
2026-03-17 15:50:42 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,48)
2026-03-17 15:50:42 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-17 15:50:42 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=64, coord=(1,4), attempt=1, reward=-0.003, score_before=0.413, score_after=0.363, reward_delta=-0.003, forward=0.080, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-17 15:50:42 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (1,4)
2026-03-17 15:50:43 | REQ: deploy cell accepted x=49, y=16
2026-03-17 15:50:43 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (16,49)
2026-03-17 15:50:43 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (16,49)
2026-03-17 15:50:43 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.018 total_deploy_reward=+0.018 avg_forward=0.084 avg_spread=1.000 avg_edge=0.750 avg_cover=0.000
2026-03-17 15:50:43 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.018131651556957035, 'units': 2, 'total_deploy_reward': 0.018131651556957035, 'forward_sum': 0.16779661016949152, 'spread_sum': 2.0, 'edge_sum': 1.5, 'cover_sum': 0.0, 'avg_forward': 0.08389830508474576, 'avg_spread': 1.0, 'avg_edge': 0.75, 'avg_cover': 0.0}
2026-03-17 15:50:43 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-17 15:50:43 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-17 15:50:43 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-17 15:50:43 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-17 15:50:43 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-17 15:50:44 | FX: перепроигрываю 30 строк(и) лога.
2026-03-17 15:50:44 | === БОЕВОЙ РАУНД 1 ===
2026-03-17 15:50:44 | --- ХОД PLAYER ---
2026-03-17 15:50:44 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-17 15:50:44 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-17 15:50:44 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-17 15:50:45 | REQ: move cell accepted (RMB) x=37, y=27, mode=advance
2026-03-17 15:50:46 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-17 15:50:46 | REQ: move cell accepted (RMB) x=38, y=17, mode=advance
2026-03-17 15:50:47 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-17 15:50:47 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-17 15:50:47 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-17 15:50:47 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-17 15:50:47 | --- ФАЗА ЧАРДЖА ---
2026-03-17 15:50:47 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-17 15:50:47 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-17 15:50:47 | Нет доступных целей для чарджа.
2026-03-17 15:50:47 | --- ФАЗА БОЯ ---
2026-03-17 15:50:47 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-17 15:50:47 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-17 15:50:47 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-17 15:50:47 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-17 15:50:47 | --- ХОД MODEL ---
2026-03-17 15:50:47 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-17 15:50:47 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-17 15:50:47 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-17 15:50:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (34, 5). Выбор: right, advance=да, бросок=1, макс=6, distance=6
2026-03-17 15:50:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (34, 11)
2026-03-17 15:50:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): [MOVE][DEBUG] chosen_cell=(11, 34), move_mode=advance, intent_override=None, allow_advance_override=None
2026-03-17 15:50:47 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-17 15:50:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 4). Выбор: right, advance=да, бросок=1, макс=6, distance=6
2026-03-17 15:50:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 10)
2026-03-17 15:50:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): [MOVE][DEBUG] chosen_cell=(10, 1), move_mode=advance, intent_override=None, allow_advance_override=None
2026-03-17 15:50:47 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-17 15:50:47 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-17 15:50:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-17 15:50:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-17 15:50:47 | --- ФАЗА ЧАРДЖА ---
2026-03-17 15:50:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-17 15:50:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-17 15:50:47 | [MODEL] Чардж: нет доступных целей
2026-03-17 15:50:47 | --- ФАЗА БОЯ ---
2026-03-17 15:50:47 | [MODEL] Ближний бой: нет доступных атак
2026-03-17 15:50:47 | Reward (progress к objective): d_before=28.653, d_after=23.601, delta=5.052, norm=0.842, bonus=+0.025
2026-03-17 15:50:47 | [MOVE][QUALITY][SUMMARY] stay_count=0, stay_without_shoot_count=0, stay_without_shoot_rate=0.000, entered_effective_range_count=0, range_bonus_total=+0.000, stay_no_shoot_penalty_total=-0.000
2026-03-17 15:50:47 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-17 15:50:47 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-17 15:50:47 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-17 15:50:47 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-17 15:50:47 | Итерация 0 завершена с наградой tensor([0.0253], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-17 15:50:47 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-17 15:50:47 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

