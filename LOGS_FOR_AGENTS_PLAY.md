2026-03-09 10:00:56 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-09 10:00:56 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-09 10:00:56 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-09 10:00:56 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-09 10:00:56 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 10:00:57 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 10:00:57 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-24-306628.pickle
2026-03-09 10:00:57 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-24-306628.pth
2026-03-09 10:00:57 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-09 10:00:59 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-03-09 10:00:59 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-09 10:00:59 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-09 10:00:59 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-09 10:00:59 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-09 10:00:59 | [DEPLOY] Order: model first, alternating
2026-03-09 10:00:59 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 10:00:59 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1029, coord=(17,9), attempt=1, reward=+0.022, score_before=0.000, score_after=0.445, reward_delta=+0.022, forward=0.156, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 10:00:59 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (17,9)
2026-03-09 10:00:59 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 10:01:00 | Ошибка деплоя: reason=outside_deploy_zone, x=39, y=36. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-03-09 10:01:00 | REQ: deploy cell accepted x=46, y=22
2026-03-09 10:01:00 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (22,46)
2026-03-09 10:01:00 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (22,46)
2026-03-09 10:01:00 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 10:01:00 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1325, coord=(22,5), attempt=1, reward=-0.003, score_before=0.445, score_after=0.382, reward_delta=-0.003, forward=0.122, spread=0.833, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 10:01:00 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (22,5)
2026-03-09 10:01:00 | REQ: deploy cell accepted x=49, y=31
2026-03-09 10:01:01 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (31,49)
2026-03-09 10:01:01 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (31,49)
2026-03-09 10:01:01 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.139 avg_spread=0.917 avg_edge=1.000 avg_cover=0.000
2026-03-09 10:01:01 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.019117067402443833, 'units': 2, 'total_deploy_reward': 0.019117067402443833, 'forward_sum': 0.2779661016949152, 'spread_sum': 1.8333333333333335, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.1389830508474576, 'avg_spread': 0.9166666666666667, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-09 10:01:01 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-09 10:01:01 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-09 10:01:01 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-09 10:01:01 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:01:01 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-09 10:01:01 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 10:01:02 | === БОЕВОЙ РАУНД 1 ===
2026-03-09 10:01:02 | --- ХОД PLAYER ---
2026-03-09 10:01:02 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:01:02 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:01:02 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:01:03 | REQ: move cell accepted (RMB) x=41, y=23, mode=normal
2026-03-09 10:01:04 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:01:04 | REQ: move cell accepted (RMB) x=44, y=30, mode=normal
2026-03-09 10:01:05 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:01:05 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:01:05 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:01:05 | Нет доступных целей для чарджа.
2026-03-09 10:01:05 | --- ФАЗА БОЯ ---
2026-03-09 10:01:05 | --- ХОД MODEL ---
2026-03-09 10:01:05 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:01:05 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:01:05 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:01:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=21.213, d_after=21.213, d_best=10.213, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-09 10:01:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (17, 9). Выбор: none, advance=нет, distance=0
2026-03-09 10:01:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (17, 9)
2026-03-09 10:01:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=25.080, d_after=25.080, d_best=14.080, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-09 10:01:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (22, 5). Выбор: none, advance=нет, distance=0
2026-03-09 10:01:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (22, 5)
2026-03-09 10:01:05 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-03-09 10:01:05 | Reward (шаг): движение delta=-0.120
2026-03-09 10:01:05 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:01:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:01:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:01:05 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:01:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:01:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:01:05 | [MODEL] Чардж: нет доступных целей
2026-03-09 10:01:05 | --- ФАЗА БОЯ ---
2026-03-09 10:01:05 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 10:01:05 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.213203435596427->21.213203435596427, hold_penalty_events=2
2026-03-09 10:01:05 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 10:01:05 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 10:01:05 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 10:01:05 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-09 10:01:05 | Итерация 0 завершена с наградой tensor([-0.1200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 10:01:05 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:01:05 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-09 10:01:06 | === БОЕВОЙ РАУНД 2 ===
2026-03-09 10:01:06 | --- ХОД PLAYER ---
2026-03-09 10:01:06 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:01:06 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:01:06 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:01:07 | REQ: move cell accepted (RMB) x=36, y=23, mode=normal
2026-03-09 10:01:07 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:01:08 | REQ: move cell accepted (RMB) x=39, y=30, mode=normal
2026-03-09 10:01:08 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:01:08 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:01:08 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:01:08 | Нет доступных целей для чарджа.
2026-03-09 10:01:08 | --- ФАЗА БОЯ ---
2026-03-09 10:01:08 | --- ХОД MODEL ---
2026-03-09 10:01:08 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:01:08 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:01:08 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:01:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=21.213, d_after=21.213, d_best=10.213, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-09 10:01:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (17, 9). Выбор: none, advance=нет, distance=0
2026-03-09 10:01:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (17, 9)
2026-03-09 10:01:08 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=25.080, d_after=25.080, d_best=14.080, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-09 10:01:08 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (22, 5). Выбор: none, advance=нет, distance=0
2026-03-09 10:01:08 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (22, 5)
2026-03-09 10:01:08 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-03-09 10:01:08 | Reward (шаг): движение delta=-0.120
2026-03-09 10:01:08 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:01:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:01:08 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:01:08 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:01:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:01:08 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:01:08 | [MODEL] Чардж: нет доступных целей
2026-03-09 10:01:08 | --- ФАЗА БОЯ ---
2026-03-09 10:01:08 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 10:01:08 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.213203435596427->21.213203435596427, hold_penalty_events=2
2026-03-09 10:01:08 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 10:01:08 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 10:01:08 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 10:01:08 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-09 10:01:08 | Итерация 1 завершена с наградой tensor([-0.1200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 10:01:08 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 4, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:01:08 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 4, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0

2026-03-09 10:01:09 | === БОЕВОЙ РАУНД 3 ===
2026-03-09 10:01:09 | --- ХОД PLAYER ---
2026-03-09 10:01:09 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:01:09 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 10:01:09 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:01:11 | REQ: move cell accepted (RMB) x=33, y=23, mode=normal
2026-03-09 10:01:11 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:01:11 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 10:01:11 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 10:01:11 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-09 10:01:11 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-09 10:01:11 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-09 10:01:11 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 10:01:11 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:01:11 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:01:11 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-09 10:01:11 | Оружие: Gauss flayer
2026-03-09 10:01:11 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:01:11 | BS оружия: 4+
2026-03-09 10:01:11 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:01:11 | Save цели: 4+ (invul: нет)
2026-03-09 10:01:11 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:01:11 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:01:11 | Правило: Overwatch: попадания только на 6+
2026-03-09 10:01:11 | Hit rolls:    [3, 6, 1, 6, 3, 4, 1, 2, 3, 4]  -> hits: 4 (crits: 2)
2026-03-09 10:01:11 | Wound rolls:  [3, 4]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-09 10:01:11 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 10:01:11 | FX: найден итог урона = 1.0.
2026-03-09 10:01:11 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-09 10:01:11 | FX: позиция эффекта start=(228.0,420.0) end=(876.0,564.0).
2026-03-09 10:01:11 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-09 10:01:11 | 📌 -------------------------

2026-03-09 10:01:12 | REQ: move cell accepted (RMB) x=35, y=29, mode=normal
2026-03-09 10:01:12 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 10:01:12 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:01:22 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-09 10:01:29 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-09 10:01:32 | 
🎲 Бросок сейвы (save): 4D6
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (overwatch)
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-09 10:01:35 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 2.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:01:35 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 10:01:35 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 10:01:35 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:01:35 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-09 10:01:35 | Оружие: Gauss flayer
2026-03-09 10:01:35 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:01:35 | BS оружия: 4+
2026-03-09 10:01:35 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:01:35 | Save цели: 4+ (invul: нет)
2026-03-09 10:01:35 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:01:35 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:01:35 | Hit rolls:    [3, 4, 5, 6, 1, 1, 2, 3, 4]  -> hits: 4 (crits: 1)
2026-03-09 10:01:35 | Wound rolls:  [4, 5, 6]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 1 = 4
2026-03-09 10:01:35 | Save rolls:   [3, 4, 5, 1]  (цель 4+) -> failed saves: 2
2026-03-09 10:01:35 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-09 10:01:35 | FX: найден итог урона = 2.0.
2026-03-09 10:01:35 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=2.0).
2026-03-09 10:01:35 | FX: позиция эффекта start=(804.0,564.0) end=(228.0,420.0).
2026-03-09 10:01:35 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-03-09 10:01:35 | 📌 -------------------------

2026-03-09 10:01:35 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:01:35 | Нет доступных целей для чарджа.
2026-03-09 10:01:35 | --- ФАЗА БОЯ ---
2026-03-09 10:01:35 | --- ХОД MODEL ---
2026-03-09 10:01:35 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-09 10:01:35 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 10:01:35 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=21.213, d_after=21.213, d_best=10.213, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (17, 9). Выбор: none, advance=нет, distance=0
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (17, 9)
2026-03-09 10:01:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=25.080, d_after=25.080, d_best=14.080, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-09 10:01:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (22, 5). Выбор: none, advance=нет, distance=0
2026-03-09 10:01:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (22, 5)
2026-03-09 10:01:35 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-03-09 10:01:35 | Reward (шаг): движение delta=-0.180
2026-03-09 10:01:35 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-09 10:01:35 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-09 10:01:35 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-09 10:01:35 | 
🎲 Бросок сейвы (save): 5D6
2026-03-09 10:01:35 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 7. HP: 9.0 -> 7.0 (shooting)
2026-03-09 10:01:35 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=13, need<=3).
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.280
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-09 10:01:35 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 10:01:35 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 10:01:35 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:01:35 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-09 10:01:35 | Оружие: Gauss flayer
2026-03-09 10:01:35 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:01:35 | BS оружия: 4+
2026-03-09 10:01:35 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:01:35 | Save цели: 4+ (invul: нет)
2026-03-09 10:01:35 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:01:35 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:01:35 | Hit rolls:    [5, 5, 1, 4, 5, 2, 6, 5, 6]  -> hits: 7 (crits: 2)
2026-03-09 10:01:35 | Wound rolls:  [5, 3, 4, 1, 4]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 2 = 5
2026-03-09 10:01:35 | Save rolls:   [6, 4, 1, 4, 2]  (цель 4+) -> failed saves: 2
2026-03-09 10:01:35 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-09 10:01:35 | FX: найден итог урона = 2.0.
2026-03-09 10:01:35 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-09 10:01:35 | FX: позиция эффекта start=(228.0,420.0) end=(804.0,564.0).
2026-03-09 10:01:35 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-09 10:01:35 | 📌 -------------------------

2026-03-09 10:01:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 10:01:35 | Reward (шаг): стрельба delta=+0.280
2026-03-09 10:01:35 | --- ФАЗА ЧАРДЖА ---
2026-03-09 10:01:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:01:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 10:01:35 | [MODEL] Чардж: нет доступных целей
2026-03-09 10:01:35 | --- ФАЗА БОЯ ---
2026-03-09 10:01:35 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 10:01:35 | Reward (terrain/potential): gamma=0.990, phi_before=-0.017, phi_after=-0.017, delta=+0.000; cover=0.000->0.000, threat=-0.167->-0.167, guard=0.000->0.000
2026-03-09 10:01:35 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=1)
2026-03-09 10:01:35 | Reward (terrain/clamp): raw=-0.010, cap=±0.120, clamp не сработал
2026-03-09 10:01:35 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-09 10:01:35 | Итерация 2 завершена с наградой tensor([0.0902], device='cuda:0'), здоровье игрока [7.0, 10.0], здоровье модели [9.0, 10.0]
2026-03-09 10:01:35 | {'model health': [9.0, 10.0], 'player health': [7.0, 10.0], 'model alive models': [9, 10], 'player alive models': [7, 10], 'modelCP': 5, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 10:01:35 | Здоровье MODEL: [9.0, 10.0], здоровье PLAYER: [7.0, 10.0]
CP MODEL: 5, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)

2026-03-09 10:01:38 | === БОЕВОЙ РАУНД 4 ===
2026-03-09 10:01:38 | --- ХОД PLAYER ---
2026-03-09 10:01:38 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 10:01:38 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 10:01:39 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 10:01:39 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-03-09 10:01:39 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 10:01:39 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-09 10:01:39 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 10:01:39 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 10:01:42 | REQ: move cell accepted (RMB) x=30, y=24, mode=normal
2026-03-09 10:01:42 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:01:42 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-09 10:01:42 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 10:01:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 6. HP: 8.0 -> 6.0 (Overwatch)
2026-03-09 10:01:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-03-09 10:01:42 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-09 10:01:42 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 10:01:42 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:01:42 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:01:42 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-09 10:01:42 | Оружие: Gauss flayer
2026-03-09 10:01:42 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:01:42 | BS оружия: 4+
2026-03-09 10:01:42 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:01:42 | Save цели: 4+ (invul: нет)
2026-03-09 10:01:42 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:01:42 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:01:42 | Правило: Overwatch: попадания только на 6+
2026-03-09 10:01:42 | Hit rolls:    [6, 6, 4, 2, 1, 5, 2, 1, 2]  -> hits: 4 (crits: 2)
2026-03-09 10:01:42 | Wound rolls:  [1, 3]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 2 = 2
2026-03-09 10:01:42 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-09 10:01:42 | FX: найден итог урона = 2.0.
2026-03-09 10:01:42 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-09 10:01:42 | FX: позиция эффекта start=(228.0,420.0) end=(804.0,564.0).
2026-03-09 10:01:42 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-09 10:01:42 | 📌 -------------------------

2026-03-09 10:01:46 | REQ: move cell accepted (RMB) x=29, y=30, mode=normal
2026-03-09 10:01:47 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-09 10:01:47 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-09 10:01:47 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 10:01:47 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-03-09 10:01:47 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-09 10:01:47 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-09 10:01:47 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 10:01:47 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:01:47 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:01:47 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 10:01:47 | Оружие: Gauss flayer
2026-03-09 10:01:47 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:01:47 | BS оружия: 4+
2026-03-09 10:01:47 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:01:47 | Save цели: 4+ (invul: нет)
2026-03-09 10:01:47 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:01:47 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:01:47 | Правило: Overwatch: попадания только на 6+
2026-03-09 10:01:47 | Hit rolls:    [2, 2, 6, 4, 6, 5, 3, 1, 1]  -> hits: 4 (crits: 2)
2026-03-09 10:01:47 | Wound rolls:  [2, 3]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 2 = 2
2026-03-09 10:01:47 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-09 10:01:47 | FX: найден итог урона = 2.0.
2026-03-09 10:01:47 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=2.0).
2026-03-09 10:01:47 | FX: позиция эффекта start=(228.0,420.0) end=(828.0,684.0).
2026-03-09 10:01:47 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-09 10:01:47 | 📌 -------------------------

2026-03-09 10:01:47 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 10:03:29 | 
🎲 Бросок на попадание (to hit): 6D6
2026-03-09 10:03:33 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:03:33 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 10:03:33 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 10:03:33 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 10:03:33 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-09 10:03:33 | Оружие: Gauss flayer
2026-03-09 10:03:33 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:03:33 | BS оружия: 4+
2026-03-09 10:03:33 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 10:03:33 | Save цели: 4+ (invul: нет)
2026-03-09 10:03:33 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 10:03:33 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 10:03:33 | Hit rolls:    [1, 1, 1, 1, 1, 1]  -> hits: 0
2026-03-09 10:03:33 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 10:03:33 | FX: найден итог урона = 0.0.
2026-03-09 10:03:33 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=0.0).
2026-03-09 10:03:33 | FX: позиция эффекта start=(732.0,588.0) end=(228.0,420.0).
2026-03-09 10:03:33 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-03-09 10:03:33 | 📌 -------------------------

2026-03-09 10:03:33 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-09 10:03:33 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 10:03:33 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 10:03:33 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 10:03:33 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 10:03:33 | FX: найден итог урона = 2.0.
2026-03-09 10:03:33 | FX: дубликат отчёта, эффект не создаём.
