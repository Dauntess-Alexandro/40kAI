2026-03-10 12:47:47 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-10 12:47:47 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-10 12:47:47 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-10 12:47:47 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-10 12:47:48 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-10 12:47:48 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-48-766873.pickle
2026-03-10 12:47:48 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-48-766873.pth
2026-03-10 12:47:48 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-10 12:47:54 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-03-10 12:47:54 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-10 12:47:54 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-10 12:47:54 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-10 12:47:54 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-10 12:47:54 | [DEPLOY] Order: model first, alternating
2026-03-10 12:47:54 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-10 12:47:54 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1681, coord=(28,1), attempt=1, reward=+0.014, score_before=0.000, score_after=0.289, reward_delta=+0.014, forward=0.020, spread=1.000, edge=0.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-10 12:47:54 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (28,1)
2026-03-10 12:47:54 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-10 12:47:54 | REQ: deploy cell accepted x=55, y=26
2026-03-10 12:47:54 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,55)
2026-03-10 12:47:54 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,55)
2026-03-10 12:47:54 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-10 12:47:54 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1991, coord=(33,11), attempt=1, reward=+0.002, score_before=0.289, score_after=0.328, reward_delta=+0.002, forward=0.105, spread=0.833, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-10 12:47:54 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (33,11)
2026-03-10 12:47:55 | REQ: deploy cell accepted x=53, y=18
2026-03-10 12:47:56 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,53)
2026-03-10 12:47:56 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,53)
2026-03-10 12:47:56 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.016 total_deploy_reward=+0.016 avg_forward=0.063 avg_spread=0.917 avg_edge=0.250 avg_cover=0.000
2026-03-10 12:47:56 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.016397319668900276, 'units': 2, 'total_deploy_reward': 0.016397319668900276, 'forward_sum': 0.1254237288135593, 'spread_sum': 1.8333333333333335, 'edge_sum': 0.5, 'cover_sum': 0.0, 'avg_forward': 0.06271186440677964, 'avg_spread': 0.9166666666666667, 'avg_edge': 0.25, 'avg_cover': 0.0}
2026-03-10 12:47:56 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-10 12:47:56 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-10 12:47:56 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-10 12:47:56 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 12:47:56 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-10 12:47:56 | FX: перепроигрываю 30 строк(и) лога.
2026-03-10 12:47:57 | === БОЕВОЙ РАУНД 1 ===
2026-03-10 12:47:57 | --- ХОД PLAYER ---
2026-03-10 12:47:57 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 12:47:57 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 12:47:57 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 12:47:58 | REQ: move cell accepted (RMB) x=46, y=30, mode=advance
2026-03-10 12:47:59 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 12:47:59 | REQ: move cell accepted (RMB) x=42, y=18, mode=advance
2026-03-10 12:48:00 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 12:48:00 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 12:48:00 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 12:48:00 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 12:48:00 | --- ФАЗА ЧАРДЖА ---
2026-03-10 12:48:00 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 12:48:00 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 12:48:00 | Нет доступных целей для чарджа.
2026-03-10 12:48:00 | --- ФАЗА БОЯ ---
2026-03-10 12:48:00 | --- ХОД MODEL ---
2026-03-10 12:48:00 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 12:48:00 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 12:48:00 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 12:48:00 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (28, 1). Выбор: up, advance=нет, distance=2
2026-03-10 12:48:00 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (26, 1)
2026-03-10 12:48:00 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 12:48:00 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (33, 11). Выбор: up, advance=нет, distance=5
2026-03-10 12:48:00 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (28, 11)
2026-03-10 12:48:00 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 12:48:00 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 12:48:00 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=42.00, range=24.00, delta=+18.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:00 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=38.00, range=24.00, delta=+14.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:00 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 12:48:00 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:00 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:00 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 12:48:00 | --- ФАЗА ЧАРДЖА ---
2026-03-10 12:48:00 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 12:48:00 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 12:48:00 | [MODEL] Чардж: нет доступных целей
2026-03-10 12:48:00 | --- ФАЗА БОЯ ---
2026-03-10 12:48:00 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 12:48:00 | Reward (progress к objective): d_before=23.022, d_after=20.616, delta=2.406, norm=0.401, bonus=+0.012
2026-03-10 12:48:00 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-10 12:48:00 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-10 12:48:00 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-10 12:48:00 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-10 12:48:00 | Итерация 0 завершена с наградой tensor([0.0120], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-10 12:48:00 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 12:48:00 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-10 12:48:01 | === БОЕВОЙ РАУНД 2 ===
2026-03-10 12:48:01 | --- ХОД PLAYER ---
2026-03-10 12:48:01 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 12:48:01 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 12:48:01 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 12:48:02 | REQ: move cell accepted (RMB) x=41, y=31, mode=normal
2026-03-10 12:48:03 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 12:48:03 | REQ: move cell accepted (RMB) x=37, y=18, mode=normal
2026-03-10 12:48:03 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 12:48:03 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 12:48:03 | [TARGET][SHOOT] Unit 11 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=37.00, range=24.00, delta=+13.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:03 | [TARGET][SHOOT] Unit 11 — Necrons Necron Warriors (x10 моделей) -> Unit 22 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:03 | [TARGET][SHOOT] Unit 12 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:03 | REQ: валидные цели стрельбы для Unit 12: [22] | отфильтрованы: [21: цель вне дальности: range 33.00 > 24.00 (out_of_range by +9.00)]
2026-03-10 12:48:03 | FX: перепроигрываю 30 строк(и) лога.
2026-03-10 12:48:34 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 12:48:38 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-10 12:48:40 | 
🎲 Бросок сейвы (save): 1D6
2026-03-10 12:48:43 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 0.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-10 12:48:43 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 12:48:43 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 12:48:43 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-10 12:48:43 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-03-10 12:48:43 | Оружие: Gauss flayer
2026-03-10 12:48:43 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 12:48:43 | BS оружия: 4+
2026-03-10 12:48:43 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 12:48:43 | Save цели: 4+ (invul: нет)
2026-03-10 12:48:43 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 12:48:43 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 12:48:43 | Hit rolls:    [1, 2, 3, 4, 1, 2, 3, 4, 1, 3]  -> hits: 2
2026-03-10 12:48:43 | Wound rolls:  [2, 4]  (цель 4+) -> wounds: 1
2026-03-10 12:48:43 | Save rolls:   [4]  (цель 4+) -> failed saves: 0
2026-03-10 12:48:43 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-10 12:48:43 | FX: найден итог урона = 0.0.
2026-03-10 12:48:43 | FX: создан FxShotEvent (attacker=12, target=22, weapon=Gauss flayer, damage=0.0).
2026-03-10 12:48:43 | FX: позиция эффекта start=(900.0,444.0) end=(276.0,684.0).
2026-03-10 12:48:43 | FX: эффект добавлен в рендер (attacker=12, target=22).
2026-03-10 12:48:43 | 📌 -------------------------

2026-03-10 12:48:43 | --- ФАЗА ЧАРДЖА ---
2026-03-10 12:48:43 | Нет доступных целей для чарджа.
2026-03-10 12:48:43 | --- ФАЗА БОЯ ---
2026-03-10 12:48:43 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=37.00, range=24.00, delta=+13.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:43 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:43 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:43 | --- ХОД MODEL ---
2026-03-10 12:48:43 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 12:48:43 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 12:48:43 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 12:48:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (26, 1). Выбор: up, advance=нет, distance=2
2026-03-10 12:48:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (24, 1)
2026-03-10 12:48:43 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 12:48:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (28, 11). Выбор: up, advance=нет, distance=5
2026-03-10 12:48:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (23, 11)
2026-03-10 12:48:43 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 12:48:43 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 12:48:43 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=37.00, range=24.00, delta=+13.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:43 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 12:48:43 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-10 12:48:43 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 12:48:43 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-10 12:48:43 | 
🎲 Бросок сейвы (save): 2D6
2026-03-10 12:48:43 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-03-10 12:48:43 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-10 12:48:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-10 12:48:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-10 12:48:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=11, need<=3).
2026-03-10 12:48:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-10 12:48:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-10 12:48:43 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 12:48:43 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 12:48:43 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-10 12:48:43 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-10 12:48:43 | Оружие: Gauss flayer
2026-03-10 12:48:43 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 12:48:43 | BS оружия: 4+
2026-03-10 12:48:43 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 12:48:43 | Save цели: 4+ (invul: нет)
2026-03-10 12:48:43 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 12:48:43 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 12:48:43 | Hit rolls:    [3, 2, 3, 3, 2, 2, 3, 6, 1, 4]  -> hits: 2 (crits: 1)
2026-03-10 12:48:43 | Wound rolls:  [6]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 1 = 2
2026-03-10 12:48:43 | Save rolls:   [5, 1]  (цель 4+) -> failed saves: 1
2026-03-10 12:48:43 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-10 12:48:43 | FX: найден итог урона = 1.0.
2026-03-10 12:48:43 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-10 12:48:43 | FX: позиция эффекта start=(276.0,684.0) end=(900.0,444.0).
2026-03-10 12:48:43 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-10 12:48:43 | 📌 -------------------------

2026-03-10 12:48:43 | Reward (шаг): стрельба delta=+0.080
2026-03-10 12:48:43 | --- ФАЗА ЧАРДЖА ---
2026-03-10 12:48:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 12:48:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 12:48:43 | [MODEL] Чардж: нет доступных целей
2026-03-10 12:48:43 | --- ФАЗА БОЯ ---
2026-03-10 12:48:43 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 12:48:43 | Reward (progress к objective): d_before=20.616, d_after=19.235, delta=1.380, norm=0.230, bonus=+0.007
2026-03-10 12:48:43 | Reward (terrain/potential): gamma=0.990, phi_before=-0.017, phi_after=-0.017, delta=+0.000; cover=0.000->0.000, threat=-0.167->-0.167, guard=0.000->0.000
2026-03-10 12:48:43 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=1)
2026-03-10 12:48:43 | Reward (terrain/clamp): raw=-0.010, cap=±0.120, clamp не сработал
2026-03-10 12:48:43 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-10 12:48:43 | Итерация 1 завершена с наградой tensor([0.0771], device='cuda:0'), здоровье игрока [10.0, 9.0], здоровье модели [10.0, 10.0]
2026-03-10 12:48:43 | {'model health': [10.0, 10.0], 'player health': [10.0, 9.0], 'model alive models': [10, 10], 'player alive models': [10, 9], 'modelCP': 4, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 12:48:43 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 9.0]
CP MODEL: 4, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-03-10 12:48:45 | === БОЕВОЙ РАУНД 3 ===
2026-03-10 12:48:45 | --- ХОД PLAYER ---
2026-03-10 12:48:45 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 12:48:45 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 12:48:47 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-10 12:48:47 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-10 12:48:47 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 12:48:47 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-10 12:48:47 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 12:48:47 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 12:48:48 | REQ: move cell accepted (RMB) x=36, y=30, mode=normal
2026-03-10 12:48:49 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-10 12:48:49 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 12:48:49 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-10 12:48:49 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-10 12:48:49 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-10 12:48:49 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-10 12:48:49 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-10 12:48:49 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-10 12:48:49 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 12:48:49 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-10 12:48:49 | Оружие: Gauss flayer
2026-03-10 12:48:49 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 12:48:49 | BS оружия: 4+
2026-03-10 12:48:49 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 12:48:49 | Save цели: 4+ (invul: нет)
2026-03-10 12:48:49 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 12:48:49 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 12:48:49 | Правило: Overwatch: попадания только на 6+
2026-03-10 12:48:49 | Hit rolls:    [5, 4, 3, 1, 3, 5, 1, 6, 2, 2]  -> hits: 4 (crits: 1)
2026-03-10 12:48:49 | Wound rolls:  [3]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 1 = 1
2026-03-10 12:48:49 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-10 12:48:49 | FX: найден итог урона = 1.0.
2026-03-10 12:48:49 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-10 12:48:49 | FX: позиция эффекта start=(276.0,564.0) end=(996.0,756.0).
2026-03-10 12:48:49 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-10 12:48:49 | 📌 -------------------------

2026-03-10 12:48:54 | REQ: move cell accepted (RMB) x=37, y=16, mode=normal
2026-03-10 12:48:54 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-10 12:48:54 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 12:48:54 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-10 12:48:54 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-10 12:48:54 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-10 12:48:54 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-10 12:48:54 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-10 12:48:54 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-10 12:48:54 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-10 12:48:54 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-10 12:48:54 | Оружие: Gauss flayer
2026-03-10 12:48:54 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 12:48:54 | BS оружия: 4+
2026-03-10 12:48:54 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 12:48:54 | Save цели: 4+ (invul: нет)
2026-03-10 12:48:54 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 12:48:54 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 12:48:54 | Правило: Overwatch: попадания только на 6+
2026-03-10 12:48:54 | Hit rolls:    [3, 6, 6, 3, 2, 3, 2, 4, 5, 5]  -> hits: 5 (crits: 2)
2026-03-10 12:48:54 | Wound rolls:  [5, 2]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-10 12:48:54 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-10 12:48:54 | FX: найден итог урона = 1.0.
2026-03-10 12:48:54 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-10 12:48:54 | FX: позиция эффекта start=(276.0,564.0) end=(900.0,444.0).
2026-03-10 12:48:54 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-10 12:48:54 | 📌 -------------------------

2026-03-10 12:48:54 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 12:48:54 | [TARGET][SHOOT] Unit 11 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:48:54 | REQ: shooter changed Unit 12->Unit 11, target reset
2026-03-10 12:48:54 | REQ: валидные цели стрельбы для Unit 11: [22] | отфильтрованы: [21: цель вне дальности: range 32.00 > 24.00 (out_of_range by +8.00)]
2026-03-10 12:49:02 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-10 12:49:05 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-10 12:49:05 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 12:49:05 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 12:49:05 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-10 12:49:05 | FX: найдена строка стрельбы (attacker=11, target=22).
2026-03-10 12:49:05 | Оружие: Gauss flayer
2026-03-10 12:49:05 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 12:49:05 | BS оружия: 4+
2026-03-10 12:49:05 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 12:49:05 | Save цели: 4+ (invul: нет)
2026-03-10 12:49:05 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 12:49:05 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 12:49:05 | Hit rolls:    [1, 1, 1, 1, 1, 1, 1, 1, 1]  -> hits: 0
2026-03-10 12:49:05 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-10 12:49:05 | FX: найден итог урона = 0.0.
2026-03-10 12:49:05 | FX: создан FxShotEvent (attacker=11, target=22, weapon=Gauss flayer, damage=0.0).
2026-03-10 12:49:05 | FX: позиция эффекта start=(876.0,732.0) end=(276.0,564.0).
2026-03-10 12:49:05 | FX: эффект добавлен в рендер (attacker=11, target=22).
2026-03-10 12:49:05 | 📌 -------------------------

2026-03-10 12:49:05 | [TARGET][SHOOT] Unit 12 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:49:05 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-10 12:49:05 | REQ: валидные цели стрельбы для Unit 12: [22] | отфильтрованы: [21: цель вне дальности: range 33.00 > 24.00 (out_of_range by +9.00)]
2026-03-10 12:49:06 | FX: перепроигрываю 30 строк(и) лога.
2026-03-10 12:49:06 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-10 12:49:06 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-10 12:49:06 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 12:49:06 | FX: найден итог урона = 1.0.
2026-03-10 12:49:06 | FX: дубликат отчёта, эффект не создаём.
2026-03-10 12:49:12 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-10 12:49:18 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-10 12:49:19 | 
🎲 Бросок сейвы (save): 4D6
2026-03-10 12:49:22 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (overwatch)
2026-03-10 12:49:22 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-10 12:49:22 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 2.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-10 12:49:22 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 12:49:22 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 12:49:22 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-10 12:49:22 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-03-10 12:49:22 | Оружие: Gauss flayer
2026-03-10 12:49:22 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 12:49:22 | BS оружия: 4+
2026-03-10 12:49:22 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 12:49:22 | Save цели: 4+ (invul: нет)
2026-03-10 12:49:22 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 12:49:22 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 12:49:22 | Hit rolls:    [2, 3, 4, 5, 6, 6, 6, 6, 1]  -> hits: 6 (crits: 4)
2026-03-10 12:49:22 | Wound rolls:  [2, 2]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 4 = 4
2026-03-10 12:49:22 | Save rolls:   [4, 5, 1, 2]  (цель 4+) -> failed saves: 2
2026-03-10 12:49:22 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-10 12:49:22 | FX: найден итог урона = 2.0.
2026-03-10 12:49:22 | FX: создан FxShotEvent (attacker=12, target=22, weapon=Gauss flayer, damage=2.0).
2026-03-10 12:49:22 | FX: позиция эффекта start=(900.0,396.0) end=(276.0,564.0).
2026-03-10 12:49:22 | FX: эффект добавлен в рендер (attacker=12, target=22).
2026-03-10 12:49:22 | 📌 -------------------------

2026-03-10 12:49:22 | --- ФАЗА ЧАРДЖА ---
2026-03-10 12:49:22 | Нет доступных целей для чарджа.
2026-03-10 12:49:22 | --- ФАЗА БОЯ ---
2026-03-10 12:49:22 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:49:22 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:49:22 | --- ХОД MODEL ---
2026-03-10 12:49:22 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 12:49:22 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 12:49:22 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-10 12:49:22 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-10 12:49:22 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 12:49:22 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-10 12:49:22 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 12:49:22 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 12:49:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (24, 1). Выбор: up, advance=нет, distance=2
2026-03-10 12:49:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (22, 1)
2026-03-10 12:49:22 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 12:49:22 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (23, 11). Выбор: up, advance=нет, distance=5
2026-03-10 12:49:22 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (18, 11)
2026-03-10 12:49:22 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-10 12:49:24 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 12:49:24 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:49:24 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 12:49:24 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 12:49:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-10 12:49:24 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-10 12:49:24 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-10 12:49:24 | 
🎲 Бросок сейвы (save): 1D6
2026-03-10 12:49:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=11, need<=3).
2026-03-10 12:49:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.000
2026-03-10 12:49:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 0.0
2026-03-10 12:49:24 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 12:49:24 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 12:49:24 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 12:49:24 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-10 12:49:24 | Оружие: Gauss flayer
2026-03-10 12:49:24 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 12:49:24 | BS оружия: 4+
2026-03-10 12:49:24 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 12:49:24 | Save цели: 4+ (invul: нет)
2026-03-10 12:49:24 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 12:49:24 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 12:49:24 | Hit rolls:    [3, 1, 3, 4, 3, 1, 5, 3, 5]  -> hits: 3
2026-03-10 12:49:24 | Wound rolls:  [3, 1, 4]  (цель 4+) -> wounds: 1
2026-03-10 12:49:24 | Save rolls:   [4]  (цель 4+) -> failed saves: 0
2026-03-10 12:49:24 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-10 12:49:24 | FX: найден итог урона = 0.0.
2026-03-10 12:49:24 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=0.0).
2026-03-10 12:49:24 | FX: позиция эффекта start=(276.0,564.0) end=(876.0,732.0).
2026-03-10 12:49:24 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-10 12:49:24 | 📌 -------------------------

2026-03-10 12:49:24 | --- ФАЗА ЧАРДЖА ---
2026-03-10 12:49:24 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 12:49:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 12:49:24 | [MODEL] Чардж: нет доступных целей
2026-03-10 12:49:24 | --- ФАЗА БОЯ ---
2026-03-10 12:49:24 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 12:49:24 | Reward (progress к objective): d_before=19.235, d_after=19.105, delta=0.130, norm=0.022, bonus=+0.001
2026-03-10 12:49:24 | Reward (terrain/potential): gamma=0.990, phi_before=-0.033, phi_after=-0.033, delta=+0.000; cover=0.000->0.000, threat=-0.333->-0.333, guard=0.000->0.000
2026-03-10 12:49:24 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=2)
2026-03-10 12:49:24 | Reward (terrain/clamp): raw=-0.010, cap=±0.120, clamp не сработал
2026-03-10 12:49:24 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-10 12:49:24 | Итерация 2 завершена с наградой tensor([-0.0090], device='cuda:0'), здоровье игрока [9.0, 9.0], здоровье модели [10.0, 9.0]
2026-03-10 12:49:24 | {'model health': [10.0, 9.0], 'player health': [9.0, 9.0], 'model alive models': [10, 9], 'player alive models': [9, 9], 'modelCP': 4, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 12:49:24 | Здоровье MODEL: [10.0, 9.0], здоровье PLAYER: [9.0, 9.0]
CP MODEL: 4, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 0
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 0.0 раз(а)

2026-03-10 12:49:24 | === БОЕВОЙ РАУНД 4 ===
2026-03-10 12:49:24 | --- ХОД PLAYER ---
2026-03-10 12:49:24 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 12:49:24 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 12:49:29 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-10 12:49:29 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-10 12:49:29 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 12:49:29 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-10 12:49:29 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 12:49:31 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-10 12:49:31 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-10 12:49:31 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 12:49:31 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-10 12:49:31 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 12:49:31 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 12:49:34 | Unit 11: movement skipped (позиция сохранена x=36, y=30).
2026-03-10 12:49:34 | Unit 11 — Necrons Necron Warriors (x10 моделей): клетка (36,30) недостижима. Что делать дальше: выберите подсвеченную reachable-клетку.
2026-03-10 12:49:35 | Unit 11: movement skipped (позиция сохранена x=36, y=30).
2026-03-10 12:49:35 | Unit 11 — Necrons Necron Warriors (x10 моделей): клетка (36,30) недостижима. Что делать дальше: выберите подсвеченную reachable-клетку.
2026-03-10 12:49:35 | Unit 11: movement skipped (позиция сохранена x=36, y=30).
2026-03-10 12:49:35 | Unit 11 — Necrons Necron Warriors (x10 моделей): клетка (36,30) недостижима. Что делать дальше: выберите подсвеченную reachable-клетку.
2026-03-10 12:49:35 | Unit 11: movement skipped (позиция сохранена x=36, y=30).
2026-03-10 12:49:35 | Unit 11 — Necrons Necron Warriors (x10 моделей): клетка (36,30) недостижима. Что делать дальше: выберите подсвеченную reachable-клетку.
