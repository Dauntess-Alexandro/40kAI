2026-03-09 09:53:38 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-09 09:53:38 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-09 09:53:38 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-09 09:53:38 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-09 09:53:38 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 09:53:39 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 09:53:39 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-13-764024.pickle
2026-03-09 09:53:39 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-13-764024.pth
2026-03-09 09:53:39 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-09 09:53:41 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-03-09 09:53:41 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-09 09:53:41 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-09 09:53:41 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-09 09:53:41 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-09 09:53:41 | [DEPLOY] Order: model first, alternating
2026-03-09 09:53:41 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 09:53:41 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=901, coord=(15,1), attempt=1, reward=+0.014, score_before=0.000, score_after=0.289, reward_delta=+0.014, forward=0.020, spread=1.000, edge=0.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 09:53:41 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (15,1)
2026-03-09 09:53:41 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 09:53:42 | REQ: deploy cell accepted x=48, y=30
2026-03-09 09:53:42 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (30,48)
2026-03-09 09:53:42 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (30,48)
2026-03-09 09:53:42 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 09:53:42 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=2102, coord=(35,2), attempt=1, reward=+0.001, score_before=0.289, score_after=0.316, reward_delta=+0.001, forward=0.029, spread=1.000, edge=0.250, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 09:53:42 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (35,2)
2026-03-09 09:53:42 | REQ: deploy cell accepted x=48, y=23
2026-03-09 09:53:43 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (23,48)
2026-03-09 09:53:43 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (23,48)
2026-03-09 09:53:43 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.016 total_deploy_reward=+0.016 avg_forward=0.025 avg_spread=1.000 avg_edge=0.125 avg_cover=0.000
2026-03-09 09:53:43 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.015786361844698463, 'units': 2, 'total_deploy_reward': 0.015786361844698463, 'forward_sum': 0.04915254237288136, 'spread_sum': 2.0, 'edge_sum': 0.25, 'cover_sum': 0.0, 'avg_forward': 0.02457627118644068, 'avg_spread': 1.0, 'avg_edge': 0.125, 'avg_cover': 0.0}
2026-03-09 09:53:43 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-09 09:53:43 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-09 09:53:43 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-09 09:53:43 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 09:53:43 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-09 09:53:43 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 09:53:44 | === БОЕВОЙ РАУНД 1 ===
2026-03-09 09:53:44 | --- ХОД PLAYER ---
2026-03-09 09:53:44 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 09:53:44 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 09:53:44 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 09:53:45 | REQ: move cell accepted (RMB) x=43, y=30, mode=normal
2026-03-09 09:53:45 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 09:53:46 | REQ: move cell accepted (RMB) x=43, y=22, mode=normal
2026-03-09 09:53:46 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 09:53:46 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 09:53:46 | --- ФАЗА ЧАРДЖА ---
2026-03-09 09:53:46 | Нет доступных целей для чарджа.
2026-03-09 09:53:46 | --- ФАЗА БОЯ ---
2026-03-09 09:53:46 | --- ХОД MODEL ---
2026-03-09 09:53:46 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 09:53:46 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 09:53:46 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 09:53:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (15, 1). Выбор: right, advance=нет, distance=1
2026-03-09 09:53:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (15, 2)
2026-03-09 09:53:46 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 09:53:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (35, 2). Выбор: right, advance=нет, distance=4
2026-03-09 09:53:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (35, 6)
2026-03-09 09:53:46 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 09:53:46 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 09:53:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 09:53:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 09:53:46 | --- ФАЗА ЧАРДЖА ---
2026-03-09 09:53:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 09:53:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 09:53:46 | [MODEL] Чардж: нет доступных целей
2026-03-09 09:53:46 | --- ФАЗА БОЯ ---
2026-03-09 09:53:46 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 09:53:46 | Reward (progress к objective): d_before=29.428, d_after=28.302, delta=1.126, norm=0.188, bonus=+0.006
2026-03-09 09:53:46 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 09:53:46 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 09:53:46 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 09:53:46 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-09 09:53:46 | Итерация 0 завершена с наградой tensor([0.0056], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 09:53:46 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 09:53:46 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-09 09:53:47 | === БОЕВОЙ РАУНД 2 ===
2026-03-09 09:53:47 | --- ХОД PLAYER ---
2026-03-09 09:53:47 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 09:53:47 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 09:53:47 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 09:53:57 | REQ: move cell accepted (RMB) x=38, y=30, mode=normal
2026-03-09 09:53:57 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 09:53:58 | REQ: move cell accepted (RMB) x=38, y=22, mode=normal
2026-03-09 09:53:58 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 09:53:58 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 09:53:58 | --- ФАЗА ЧАРДЖА ---
2026-03-09 09:53:58 | Нет доступных целей для чарджа.
2026-03-09 09:53:58 | --- ФАЗА БОЯ ---
2026-03-09 09:53:58 | --- ХОД MODEL ---
2026-03-09 09:53:58 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 09:53:58 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 09:53:58 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 09:53:58 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (15, 2). Выбор: right, advance=нет, distance=1
2026-03-09 09:53:58 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (15, 3)
2026-03-09 09:53:58 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 09:53:58 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (35, 6). Выбор: right, advance=нет, distance=4
2026-03-09 09:53:58 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (35, 10)
2026-03-09 09:53:58 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 09:53:58 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 09:53:58 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 09:53:58 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 09:53:58 | --- ФАЗА ЧАРДЖА ---
2026-03-09 09:53:58 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 09:53:58 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 09:53:58 | [MODEL] Чардж: нет доступных целей
2026-03-09 09:53:58 | --- ФАЗА БОЯ ---
2026-03-09 09:53:58 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 09:53:58 | Reward (progress к objective): d_before=28.302, d_after=25.000, delta=3.302, norm=0.550, bonus=+0.017
2026-03-09 09:53:58 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 09:53:58 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 09:53:58 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 09:53:58 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-09 09:53:58 | Итерация 1 завершена с наградой tensor([0.0165], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 09:53:58 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 4, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 09:53:58 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 4, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0

2026-03-09 09:54:00 | === БОЕВОЙ РАУНД 3 ===
2026-03-09 09:54:00 | --- ХОД PLAYER ---
2026-03-09 09:54:00 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 09:54:00 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 09:54:00 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 09:54:03 | REQ: move cell accepted (RMB) x=36, y=30, mode=normal
2026-03-09 09:54:03 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-09 09:54:03 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 09:54:03 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-09 09:54:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-09 09:54:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-09 09:54:03 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-09 09:54:03 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 09:54:03 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 09:54:03 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 09:54:03 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-09 09:54:03 | Оружие: Gauss flayer
2026-03-09 09:54:03 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 09:54:03 | BS оружия: 4+
2026-03-09 09:54:03 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 09:54:03 | Save цели: 4+ (invul: нет)
2026-03-09 09:54:03 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 09:54:03 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 09:54:03 | Правило: Overwatch: попадания только на 6+
2026-03-09 09:54:03 | Hit rolls:    [6, 1, 2, 4, 5, 3, 2, 6, 6, 6]  -> hits: 6 (crits: 4)
2026-03-09 09:54:03 | Wound rolls:  [6, 3, 4, 5]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 4 = 7
2026-03-09 09:54:03 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 09:54:03 | FX: найден итог урона = 1.0.
2026-03-09 09:54:03 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-09 09:54:03 | FX: позиция эффекта start=(252.0,852.0) end=(924.0,732.0).
2026-03-09 09:54:03 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-09 09:54:03 | 📌 -------------------------

2026-03-09 09:54:04 | REQ: move cell accepted (RMB) x=36, y=22, mode=normal
2026-03-09 09:54:05 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 09:54:05 | --- ФАЗА СТРЕЛЬБЫ ---
