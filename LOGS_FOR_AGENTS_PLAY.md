2026-03-24 21:30:05 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 21:30:05 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 21:30:05 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 21:30:05 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 21:30:05 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 21:30:06 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 21:30:06 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 21:30:06 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 21:30:06 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth
2026-03-24 21:30:06 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 21:30:08 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-03-24 21:30:08 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 21:30:08 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 21:30:08 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 21:30:08 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 21:30:08 | [DEPLOY] Order: model first, alternating
2026-03-24 21:30:08 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 21:30:08 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=547, coord=(9,7), attempt=1, reward=+0.021, score_before=0.000, score_after=0.429, reward_delta=+0.021, forward=0.122, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 21:30:08 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (9,7)
2026-03-24 21:30:08 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 21:30:10 | Ошибка деплоя: reason=out_of_bounds, x=58, y=21. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-03-24 21:30:11 | REQ: deploy cell accepted x=54, y=20
2026-03-24 21:30:11 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (20,54)
2026-03-24 21:30:11 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (20,54)
2026-03-24 21:30:11 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 21:30:11 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=904, coord=(15,4), attempt=1, reward=-0.001, score_before=0.429, score_after=0.417, reward_delta=-0.001, forward=0.097, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 21:30:11 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (15,4)
2026-03-24 21:30:11 | REQ: deploy cell accepted x=52, y=12
2026-03-24 21:30:12 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (12,52)
2026-03-24 21:30:12 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (12,52)
2026-03-24 21:30:12 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.109 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-24 21:30:12 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.020851399290500592, 'units': 2, 'total_deploy_reward': 0.020851399290500592, 'forward_sum': 0.21864406779661016, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.10932203389830508, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-24 21:30:12 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 21:30:12 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 21:30:12 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 21:30:12 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 21:30:12 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 21:30:12 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 21:30:12 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 21:30:14 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 21:30:14 | --- ХОД PLAYER ---
2026-03-24 21:30:14 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:30:14 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 21:30:14 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:30:18 | REQ: move cell accepted (RMB) x=43, y=26, mode=advance
2026-03-24 21:30:18 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:30:19 | REQ: move cell accepted (RMB) x=42, y=16, mode=advance
2026-03-24 21:30:19 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:30:19 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 21:30:19 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:30:19 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:30:19 | --- ФАЗА ЧАРДЖА ---
2026-03-24 21:30:19 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:30:19 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:30:19 | Нет доступных целей для чарджа.
2026-03-24 21:30:19 | --- ФАЗА БОЯ ---
2026-03-24 21:30:19 | --- ХОД MODEL ---
2026-03-24 21:30:19 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:30:19 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 21:30:19 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:30:19 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (9, 7). Выбор reachable_idx=14/397, mode=normal, advance=нет, distance=4
2026-03-24 21:30:19 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (5, 4)
2026-03-24 21:30:19 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:30:25 | [PACE] ack phase=movement unit_id=21 seq=1 step=unit ok=True
2026-03-24 21:30:25 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (15, 4). Выбор reachable_idx=6/366, mode=normal, advance=нет, distance=5
2026-03-24 21:30:25 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (10, 5)
2026-03-24 21:30:25 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:30:27 | [PACE] ack phase=movement unit_id=22 seq=2 step=unit ok=True
2026-03-24 21:30:27 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 21:30:27 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=36.00, range=24.00, delta=+12.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 21:30:27 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 21:30:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-24 21:30:27 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(42, 16), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 21:30:27 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(42, 16), full_cells=24, rapid_cells=12, вошло=1680, rapid=625, не вошло=720, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-24 21:30:38 | [PACE] ack phase=shooting unit_id=21 seq=3 step=unit ok=True
2026-03-24 21:30:38 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 21:30:38 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 21:30:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-24 21:30:41 | [PACE] ack phase=shooting unit_id=22 seq=4 step=unit ok=True
2026-03-24 21:30:41 | --- ФАЗА ЧАРДЖА ---
2026-03-24 21:30:41 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-24 21:30:44 | [PACE] ack phase=charge unit_id=21 seq=5 step=unit ok=True
2026-03-24 21:30:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-24 21:30:51 | [PACE] ack phase=charge unit_id=22 seq=6 step=unit ok=True
2026-03-24 21:30:51 | [MODEL] Чардж: нет доступных целей
2026-03-24 21:30:51 | --- ФАЗА БОЯ ---
2026-03-24 21:30:51 | [MODEL] Ближний бой: нет доступных атак
2026-03-24 21:30:51 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-24 21:30:51 | Итерация 0 завершена с наградой tensor([-0.0200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-24 21:30:51 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 21:30:51 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-24 21:30:54 | === БОЕВОЙ РАУНД 2 ===
2026-03-24 21:30:54 | --- ХОД PLAYER ---
2026-03-24 21:30:54 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:30:54 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 21:30:54 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:30:56 | REQ: move cell accepted (RMB) x=32, y=20, mode=advance
2026-03-24 21:30:57 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:30:57 | REQ: move cell accepted (RMB) x=31, y=10, mode=advance
2026-03-24 21:30:58 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-24 21:30:58 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-24 21:30:58 | 
🎲 Бросок сейвы (save): 2D6
2026-03-24 21:30:58 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-24 21:30:58 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-24 21:30:58 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-24 21:30:58 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-24 21:30:58 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-24 21:30:58 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-24 21:30:58 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-24 21:30:58 | Оружие: Gauss flayer
2026-03-24 21:30:58 | FX: найдена строка оружия: Gauss flayer.
2026-03-24 21:30:58 | BS оружия: 4+
2026-03-24 21:30:58 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-24 21:30:58 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-24 21:30:58 | Save цели: 4+ (invul: нет)
2026-03-24 21:30:58 | Benefit of Cover: не активен.
2026-03-24 21:30:58 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-24 21:30:58 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-24 21:30:58 | Правило: Overwatch: попадания только на 6+
2026-03-24 21:30:58 | Hit rolls:    [2, 6, 2, 6, 1, 2, 5, 5, 1, 3]  -> hits: 2 (crits: 2)
2026-03-24 21:30:58 | Save rolls:   [3, 6]  (цель 4+) -> failed saves: 1
2026-03-24 21:30:58 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-24 21:30:58 | FX: найден итог урона = 1.0.
2026-03-24 21:30:58 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-24 21:30:58 | FX: позиция эффекта start=(132.0,252.0) end=(1020.0,396.0).
2026-03-24 21:30:58 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-24 21:30:58 | 📌 -------------------------

2026-03-24 21:30:58 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 21:30:58 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:30:58 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:30:58 | --- ФАЗА ЧАРДЖА ---
2026-03-24 21:30:58 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:30:58 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:30:58 | Нет доступных целей для чарджа.
2026-03-24 21:30:58 | --- ФАЗА БОЯ ---
2026-03-24 21:30:58 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 21:30:58 | --- ХОД MODEL ---
2026-03-24 21:30:58 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:30:58 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-24 21:30:58 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:30:58 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (5, 4). Выбор reachable_idx=14/270, mode=normal, advance=нет, distance=4
2026-03-24 21:30:58 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 3)
2026-03-24 21:30:58 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:31:14 | [PACE] ack phase=movement unit_id=21 seq=7 step=unit ok=True
2026-03-24 21:31:14 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (10, 5). Выбор reachable_idx=6/372, mode=normal, advance=нет, distance=5
2026-03-24 21:31:14 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (5, 5)
2026-03-24 21:31:14 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-24 21:31:14 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 21:31:16 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 21:31:22 | [PACE] ack phase=movement unit_id=22 seq=8 step=unit ok=True
2026-03-24 21:31:22 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 21:31:22 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 21:31:22 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 21:31:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-24 21:31:22 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(31, 10), target_filter_size=1, max_target_dist=26, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 21:31:22 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(31, 10), full_cells=24, rapid_cells=12, вошло=1715, rapid=575, не вошло=685, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-24 21:31:25 | [PACE] ack phase=shooting unit_id=21 seq=9 step=unit ok=True
2026-03-24 21:31:25 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: выбор политики)
2026-03-24 21:31:25 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-24 21:31:25 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-24 21:31:25 | 
🎲 Бросок сейвы (save): 2D6
2026-03-24 21:31:25 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-03-24 21:31:25 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-24 21:31:25 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-24 21:31:25 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-24 21:31:25 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-24 21:31:25 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-24 21:31:25 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-24 21:31:25 | Оружие: Gauss flayer
2026-03-24 21:31:25 | FX: найдена строка оружия: Gauss flayer.
2026-03-24 21:31:25 | BS оружия: 4+
2026-03-24 21:31:25 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-24 21:31:25 | Save цели: 4+ (invul: нет)
2026-03-24 21:31:25 | Benefit of Cover: не активен.
2026-03-24 21:31:25 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-24 21:31:25 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-24 21:31:25 | Hit rolls:    [3, 4, 1, 1, 2, 5, 3, 1, 5, 3]  -> hits: 3
2026-03-24 21:31:25 | Wound rolls:  [1, 6, 5]  (цель 4+) -> wounds: 2
2026-03-24 21:31:25 | Save rolls:   [1, 4]  (цель 4+) -> failed saves: 1
2026-03-24 21:31:25 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-24 21:31:25 | FX: найден итог урона = 1.0.
2026-03-24 21:31:25 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-24 21:31:25 | FX: позиция эффекта start=(132.0,132.0) end=(780.0,492.0).
2026-03-24 21:31:25 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-24 21:31:25 | 📌 -------------------------

2026-03-24 21:31:27 | [PACE] ack phase=shooting unit_id=22 seq=10 step=unit ok=True
2026-03-24 21:31:27 | --- ФАЗА ЧАРДЖА ---
2026-03-24 21:31:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-24 21:31:42 | [PACE] ack phase=charge unit_id=21 seq=11 step=unit ok=True
2026-03-24 21:31:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-24 21:31:46 | [PACE] ack phase=charge unit_id=22 seq=12 step=unit ok=True
2026-03-24 21:31:46 | [MODEL] Чардж: нет доступных целей
2026-03-24 21:31:46 | --- ФАЗА БОЯ ---
2026-03-24 21:31:46 | [MODEL] Ближний бой: нет доступных атак
2026-03-24 21:31:46 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-24 21:31:46 | Итерация 1 завершена с наградой tensor([0.2070], device='cuda:0'), здоровье игрока [9.0, 9.0], здоровье модели [10.0, 10.0]
2026-03-24 21:31:46 | {'model health': [10.0, 10.0], 'player health': [9.0, 9.0], 'model alive models': [10, 10], 'player alive models': [9, 9], 'modelCP': 3, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 21:31:46 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [9.0, 9.0]
CP MODEL: 3, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-03-24 21:31:54 | === БОЕВОЙ РАУНД 3 ===
2026-03-24 21:31:54 | --- ХОД PLAYER ---
2026-03-24 21:31:54 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:31:54 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-24 21:31:58 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-24 21:31:58 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-24 21:31:58 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-24 21:31:58 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-24 21:31:58 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-24 21:32:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-24 21:32:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-24 21:32:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-24 21:32:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-24 21:32:00 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-24 21:32:00 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:32:00 | REQ: move cell accepted (RMB) x=32, y=16, mode=normal
2026-03-24 21:32:01 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:32:01 | REQ: move cell accepted (RMB) x=25, y=14, mode=advance
2026-03-24 21:32:01 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-24 21:32:01 | [COVER][MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-24 21:32:01 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-24 21:32:01 | 
🎲 Бросок сейвы (save): 2D6
2026-03-24 21:32:01 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-24 21:32:01 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-24 21:32:01 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-24 21:32:01 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-24 21:32:01 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-24 21:32:01 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-24 21:32:01 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-24 21:32:01 | Оружие: Gauss flayer
2026-03-24 21:32:01 | FX: найдена строка оружия: Gauss flayer.
2026-03-24 21:32:01 | BS оружия: 4+
2026-03-24 21:32:01 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-24 21:32:01 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-24 21:32:01 | Save цели: 4+ (invul: нет)
2026-03-24 21:32:01 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-24 21:32:01 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-24 21:32:01 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-24 21:32:01 | Правило: Overwatch: попадания только на 6+
2026-03-24 21:32:01 | Эффект: benefit of cover
2026-03-24 21:32:01 | Hit rolls:    [6, 3, 6, 3, 3, 5, 4, 1, 4, 3]  -> hits: 2 (crits: 2)
2026-03-24 21:32:01 | Save rolls:   [1, 4]  (цель 3+) -> failed saves: 1
2026-03-24 21:32:01 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-24 21:32:01 | FX: найден итог урона = 1.0.
2026-03-24 21:32:01 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-24 21:32:01 | FX: позиция эффекта start=(84.0,36.0) end=(756.0,252.0).
2026-03-24 21:32:01 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-24 21:32:01 | 📌 -------------------------

2026-03-24 21:32:01 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 21:32:01 | [TARGET][SHOOT] Unit 11 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 21:32:01 | REQ: валидные цели стрельбы для Unit 11: [22] | отфильтрованы: [21: цель вне дальности: range 26.00 > 24.00 (out_of_range by +2.00)]
2026-03-24 21:32:01 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(32, 16), target_filter_size=1, max_target_dist=27, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 21:32:01 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(32, 16), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-24 21:32:07 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-24 21:32:07 | REQ: движок запросил кубы стрельбы (target=22, count=10, stage=hit).
2026-03-24 21:32:13 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 22 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-24 21:32:13 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 10D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-24 21:32:13 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-24 21:32:13 | REQ: валидные цели стрельбы для Unit 11: [22] | отфильтрованы: [21: цель вне дальности: range 26.00 > 24.00 (out_of_range by +2.00)]
2026-03-24 21:41:23 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 21:41:23 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 21:41:23 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 21:41:23 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 21:41:24 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 21:41:25 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 21:41:25 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 21:41:25 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth
2026-03-24 21:41:25 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 21:41:26 | Roll-off Attacker/Defender: enemy=2 model=3 -> attacker=model
2026-03-24 21:41:26 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 21:41:26 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 21:41:26 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 21:41:26 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 21:41:26 | [DEPLOY] Order: model first, alternating
2026-03-24 21:41:26 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 21:41:26 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1264, coord=(21,4), attempt=1, reward=+0.020, score_before=0.000, score_after=0.405, reward_delta=+0.020, forward=0.071, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 21:41:26 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (21,4)
2026-03-24 21:41:26 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 21:41:27 | REQ: deploy cell accepted x=48, y=24
2026-03-24 21:41:27 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,48)
2026-03-24 21:41:27 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,48)
2026-03-24 21:41:27 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 21:41:27 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1449, coord=(24,9), attempt=1, reward=-0.006, score_before=0.405, score_after=0.285, reward_delta=-0.006, forward=0.114, spread=0.500, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 21:41:27 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (24,9)
2026-03-24 21:41:27 | REQ: deploy cell accepted x=50, y=17
2026-03-24 21:41:28 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,50)
2026-03-24 21:41:28 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,50)
2026-03-24 21:41:28 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.014 total_deploy_reward=+0.014 avg_forward=0.092 avg_spread=0.750 avg_edge=1.000 avg_cover=0.000
2026-03-24 21:41:28 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.0142688214426488, 'units': 2, 'total_deploy_reward': 0.0142688214426488, 'forward_sum': 0.18474576271186438, 'spread_sum': 1.5, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.09237288135593219, 'avg_spread': 0.75, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-24 21:41:28 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 21:41:28 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 21:41:28 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 21:41:28 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 21:41:28 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 21:41:28 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 21:41:28 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 21:41:30 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 21:41:30 | --- ХОД PLAYER ---
2026-03-24 21:41:30 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:41:30 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 21:41:30 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:41:31 | REQ: move cell accepted (RMB) x=37, y=29, mode=advance
2026-03-24 21:41:31 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:41:32 | REQ: move cell accepted (RMB) x=39, y=22, mode=advance
2026-03-24 21:41:33 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:41:33 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 21:41:33 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:41:33 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:41:33 | --- ФАЗА ЧАРДЖА ---
2026-03-24 21:41:33 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:41:33 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:41:33 | Нет доступных целей для чарджа.
2026-03-24 21:41:33 | --- ФАЗА БОЯ ---
2026-03-24 21:41:33 | --- ХОД MODEL ---
2026-03-24 21:41:33 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:41:33 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 21:41:33 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:41:33 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (21, 4). Выбор reachable_idx=3/366, mode=normal, advance=нет, distance=5
2026-03-24 21:41:33 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (16, 2)
2026-03-24 21:41:33 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:41:41 | [PACE] ack phase=movement unit_id=21 seq=1 step=unit ok=True
2026-03-24 21:41:41 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (24, 9). Выбор reachable_idx=6/481, mode=normal, advance=нет, distance=5
2026-03-24 21:41:41 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (19, 9)
2026-03-24 21:41:41 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:41:47 | [PACE] ack phase=movement unit_id=22 seq=2 step=unit ok=True
2026-03-24 21:41:47 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 21:41:47 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 21:41:47 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 21:41:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-24 21:41:47 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(39, 22), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 21:41:47 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(39, 22), full_cells=24, rapid_cells=12, вошло=1800, rapid=625, не вошло=600, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-24 21:41:50 | [PACE] ack phase=shooting unit_id=21 seq=3 step=unit ok=True
2026-03-24 21:41:50 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 21:41:50 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 21:41:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-24 21:47:54 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 21:47:54 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 21:47:54 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 21:47:54 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 21:47:54 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 21:47:55 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 21:47:55 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 21:47:55 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth
2026-03-24 21:47:55 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 21:48:08 | Roll-off Attacker/Defender: enemy=1 model=5 -> attacker=model
2026-03-24 21:48:08 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 21:48:08 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 21:48:08 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 21:48:08 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 21:48:08 | [DEPLOY] Order: model first, alternating
2026-03-24 21:48:08 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 21:48:08 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1321, coord=(22,1), attempt=1, reward=+0.014, score_before=0.000, score_after=0.289, reward_delta=+0.014, forward=0.020, spread=1.000, edge=0.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 21:48:08 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (22,1)
2026-03-24 21:48:08 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 21:48:09 | REQ: deploy cell accepted x=50, y=25
2026-03-24 21:48:09 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,50)
2026-03-24 21:48:09 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,50)
2026-03-24 21:48:09 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 21:48:09 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=484, coord=(8,4), attempt=1, reward=+0.003, score_before=0.289, score_after=0.347, reward_delta=+0.003, forward=0.046, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 21:48:09 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (8,4)
2026-03-24 21:48:09 | REQ: deploy cell accepted x=50, y=18
2026-03-24 21:48:10 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,50)
2026-03-24 21:48:10 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,50)
2026-03-24 21:48:10 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.017 total_deploy_reward=+0.017 avg_forward=0.033 avg_spread=1.000 avg_edge=0.250 avg_cover=0.000
2026-03-24 21:48:10 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.017343318880567598, 'units': 2, 'total_deploy_reward': 0.017343318880567598, 'forward_sum': 0.06610169491525424, 'spread_sum': 2.0, 'edge_sum': 0.5, 'cover_sum': 0.0, 'avg_forward': 0.03305084745762712, 'avg_spread': 1.0, 'avg_edge': 0.25, 'avg_cover': 0.0}
2026-03-24 21:48:10 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 21:48:10 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 21:48:10 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 21:48:10 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 21:48:10 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 21:48:10 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 21:48:10 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=None, cells_rapid=None, rapid_fire=1, source_cell=(39, 22), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 21:48:10 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=None, cells_rapid=None, rapid_fire=1, source_cell=(50, 18), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 21:48:10 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 21:48:11 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 21:48:11 | --- ХОД PLAYER ---
2026-03-24 21:48:11 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:48:11 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 21:48:11 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:48:11 | REQ: move cell accepted (RMB) x=39, y=25, mode=advance
2026-03-24 21:48:12 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:48:12 | REQ: move cell accepted (RMB) x=39, y=16, mode=advance
2026-03-24 21:48:13 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:48:13 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 21:48:13 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:48:13 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:48:13 | --- ФАЗА ЧАРДЖА ---
2026-03-24 21:48:13 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:48:13 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:48:13 | Нет доступных целей для чарджа.
2026-03-24 21:48:13 | --- ФАЗА БОЯ ---
2026-03-24 21:48:13 | --- ХОД MODEL ---
2026-03-24 21:48:13 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:48:13 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 21:48:13 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:48:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (22, 1). Выбор reachable_idx=3/298, mode=normal, advance=нет, distance=5
2026-03-24 21:48:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (17, 2)
2026-03-24 21:48:13 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:51:37 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 21:51:37 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 21:51:38 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 21:51:38 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 21:51:38 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 21:51:39 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 21:51:39 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 21:51:39 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth
2026-03-24 21:51:39 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 21:51:40 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-03-24 21:51:40 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 21:51:40 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 21:51:40 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 21:51:40 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 21:51:40 | [DEPLOY] Order: model first, alternating
2026-03-24 21:51:40 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 21:51:40 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=370, coord=(6,10), attempt=1, reward=+0.023, score_before=0.000, score_after=0.453, reward_delta=+0.023, forward=0.173, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 21:51:40 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (6,10)
2026-03-24 21:51:40 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 21:51:41 | REQ: deploy cell accepted x=47, y=27
2026-03-24 21:51:41 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (27,47)
2026-03-24 21:51:41 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (27,47)
2026-03-24 21:51:41 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 21:51:41 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1568, coord=(26,8), attempt=1, reward=-0.000, score_before=0.453, score_after=0.445, reward_delta=-0.000, forward=0.156, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 21:51:41 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (26,8)
2026-03-24 21:51:41 | REQ: deploy cell accepted x=48, y=20
2026-03-24 21:51:42 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,48)
2026-03-24 21:51:42 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,48)
2026-03-24 21:51:42 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.164 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-24 21:51:42 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.022230981474182107, 'units': 2, 'total_deploy_reward': 0.022230981474182107, 'forward_sum': 0.3288135593220339, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.16440677966101694, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-24 21:51:42 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 21:51:42 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 21:51:42 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 21:51:42 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 21:51:42 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 21:51:42 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 21:51:42 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 21:51:43 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 21:51:43 | --- ХОД PLAYER ---
2026-03-24 21:51:43 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:51:43 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 21:51:43 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:51:44 | REQ: move cell accepted (RMB) x=36, y=31, mode=advance
2026-03-24 21:51:44 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:51:46 | REQ: move cell accepted (RMB) x=37, y=23, mode=advance
2026-03-24 21:51:47 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:51:47 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 21:51:47 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:51:47 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:51:47 | --- ФАЗА ЧАРДЖА ---
2026-03-24 21:51:47 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:51:47 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:51:47 | Нет доступных целей для чарджа.
2026-03-24 21:51:47 | --- ФАЗА БОЯ ---
2026-03-24 21:51:47 | --- ХОД MODEL ---
2026-03-24 21:51:47 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:51:47 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 21:51:47 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:51:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (6, 10). Выбор reachable_idx=14/395, mode=normal, advance=нет, distance=4
2026-03-24 21:51:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (2, 7)
2026-03-24 21:51:47 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:51:55 | [PACE] ack phase=movement unit_id=21 seq=1 step=unit ok=True
2026-03-24 21:51:55 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (26, 8). Выбор reachable_idx=6/459, mode=normal, advance=нет, distance=5
2026-03-24 21:51:55 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (21, 8)
2026-03-24 21:51:55 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:55:51 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 21:55:51 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 21:55:51 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 21:55:51 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 21:55:52 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 21:55:52 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 21:55:52 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 21:55:52 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth
2026-03-24 21:55:52 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 21:55:54 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-03-24 21:55:54 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 21:55:54 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 21:55:54 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 21:55:54 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 21:55:54 | [DEPLOY] Order: model first, alternating
2026-03-24 21:55:54 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 21:55:54 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=487, coord=(8,7), attempt=1, reward=+0.021, score_before=0.000, score_after=0.429, reward_delta=+0.021, forward=0.122, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 21:55:54 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (8,7)
2026-03-24 21:55:54 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 21:55:55 | REQ: deploy cell accepted x=48, y=23
2026-03-24 21:55:55 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (23,48)
2026-03-24 21:55:55 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (23,48)
2026-03-24 21:55:55 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 21:55:55 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1866, coord=(31,6), attempt=1, reward=-0.000, score_before=0.429, score_after=0.425, reward_delta=-0.000, forward=0.114, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 21:55:55 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (31,6)
2026-03-24 21:55:55 | REQ: deploy cell accepted x=51, y=17
2026-03-24 21:55:56 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,51)
2026-03-24 21:55:56 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,51)
2026-03-24 21:55:56 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.118 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-24 21:55:56 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.021245565628695312, 'units': 2, 'total_deploy_reward': 0.021245565628695312, 'forward_sum': 0.23559322033898306, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.11779661016949153, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-24 21:55:56 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 21:55:56 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 21:55:56 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 21:55:56 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 21:55:56 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 21:55:56 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 21:55:56 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 21:55:57 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 21:55:57 | --- ХОД PLAYER ---
2026-03-24 21:55:57 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:55:57 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 21:55:57 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:55:58 | REQ: move cell accepted (RMB) x=37, y=25, mode=advance
2026-03-24 21:55:58 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:55:59 | REQ: move cell accepted (RMB) x=40, y=19, mode=advance
2026-03-24 21:55:59 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:55:59 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 21:55:59 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:55:59 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:55:59 | --- ФАЗА ЧАРДЖА ---
2026-03-24 21:55:59 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:55:59 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:55:59 | Нет доступных целей для чарджа.
2026-03-24 21:55:59 | --- ФАЗА БОЯ ---
2026-03-24 21:55:59 | --- ХОД MODEL ---
2026-03-24 21:55:59 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:55:59 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 21:55:59 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:55:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (8, 7). Выбор reachable_idx=3/379, mode=normal, advance=нет, distance=5
2026-03-24 21:55:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (3, 4)
2026-03-24 21:55:59 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:58:25 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 21:58:25 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 21:58:25 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 21:58:25 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 21:58:26 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 21:58:26 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 21:58:26 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 21:58:26 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth
2026-03-24 21:58:26 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 21:58:28 | Roll-off Attacker/Defender: enemy=2 model=4 -> attacker=model
2026-03-24 21:58:28 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 21:58:28 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 21:58:28 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 21:58:28 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 21:58:28 | [DEPLOY] Order: model first, alternating
2026-03-24 21:58:28 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 21:58:28 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1686, coord=(28,6), attempt=1, reward=+0.021, score_before=0.000, score_after=0.421, reward_delta=+0.021, forward=0.105, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 21:58:28 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (28,6)
2026-03-24 21:58:28 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 21:58:28 | REQ: deploy cell accepted x=56, y=26
2026-03-24 21:58:28 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,56)
2026-03-24 21:58:28 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,56)
2026-03-24 21:58:28 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 21:58:28 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1262, coord=(21,2), attempt=1, reward=-0.002, score_before=0.421, score_after=0.382, reward_delta=-0.002, forward=0.071, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 21:58:28 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (21,2)
2026-03-24 21:58:29 | REQ: deploy cell accepted x=53, y=20
2026-03-24 21:58:29 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,53)
2026-03-24 21:58:29 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,53)
2026-03-24 21:58:29 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.088 avg_spread=1.000 avg_edge=0.875 avg_cover=0.000
2026-03-24 21:58:29 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.019097359085534095, 'units': 2, 'total_deploy_reward': 0.019097359085534095, 'forward_sum': 0.17627118644067796, 'spread_sum': 2.0, 'edge_sum': 1.75, 'cover_sum': 0.0, 'avg_forward': 0.08813559322033898, 'avg_spread': 1.0, 'avg_edge': 0.875, 'avg_cover': 0.0}
2026-03-24 21:58:29 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 21:58:29 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 21:58:29 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 21:58:29 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 21:58:29 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 21:58:29 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 21:58:29 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 21:58:31 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 21:58:31 | --- ХОД PLAYER ---
2026-03-24 21:58:31 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:58:31 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 21:58:31 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:58:31 | REQ: move cell accepted (RMB) x=45, y=20, mode=advance
2026-03-24 21:58:32 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:58:32 | REQ: move cell accepted (RMB) x=42, y=26, mode=advance
2026-03-24 21:58:33 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:58:33 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 21:58:33 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:58:33 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 21:58:33 | --- ФАЗА ЧАРДЖА ---
2026-03-24 21:58:33 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:58:33 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 21:58:33 | Нет доступных целей для чарджа.
2026-03-24 21:58:33 | --- ФАЗА БОЯ ---
2026-03-24 21:58:33 | --- ХОД MODEL ---
2026-03-24 21:58:33 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 21:58:33 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 21:58:33 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 21:58:33 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (28, 6). Выбор reachable_idx=3/412, mode=normal, advance=нет, distance=5
2026-03-24 21:58:33 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (23, 3)
2026-03-24 21:58:33 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 21:58:38 | [PACE] ack phase=movement unit_id=21 seq=1 step=unit ok=True
2026-03-24 21:58:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (20, 1). Выбор reachable_idx=6/297, mode=normal, advance=нет, distance=5
2026-03-24 21:58:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (15, 5)
2026-03-24 21:58:38 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:00:14 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 22:00:14 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 22:00:14 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 22:00:14 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 22:00:15 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:00:16 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 22:00:16 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 22:00:16 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth
2026-03-24 22:00:16 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 22:00:17 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-03-24 22:00:17 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 22:00:17 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 22:00:17 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 22:00:17 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 22:00:17 | [DEPLOY] Order: model first, alternating
2026-03-24 22:00:17 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:00:17 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=969, coord=(16,9), attempt=1, reward=+0.022, score_before=0.000, score_after=0.445, reward_delta=+0.022, forward=0.156, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:00:17 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (16,9)
2026-03-24 22:00:17 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:00:17 | Ошибка деплоя: reason=outside_deploy_zone, x=40, y=22. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-03-24 22:00:18 | Ошибка деплоя: reason=outside_deploy_zone, x=42, y=31. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-03-24 22:00:18 | REQ: deploy cell accepted x=50, y=23
2026-03-24 22:00:18 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (23,50)
2026-03-24 22:00:18 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (23,50)
2026-03-24 22:00:18 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:00:18 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=492, coord=(8,12), attempt=1, reward=+0.001, score_before=0.445, score_after=0.456, reward_delta=+0.001, forward=0.181, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:00:18 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (8,12)
2026-03-24 22:00:20 | REQ: deploy cell accepted x=49, y=16
2026-03-24 22:00:20 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (16,49)
2026-03-24 22:00:20 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (16,49)
2026-03-24 22:00:20 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.023 total_deploy_reward=+0.023 avg_forward=0.169 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-24 22:00:20 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.022822230981474182, 'units': 2, 'total_deploy_reward': 0.022822230981474182, 'forward_sum': 0.3372881355932203, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.16864406779661015, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-24 22:00:20 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 22:00:20 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 22:00:20 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 22:00:20 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 22:00:20 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 22:00:20 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 22:00:20 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 22:00:21 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 22:00:21 | --- ХОД PLAYER ---
2026-03-24 22:00:21 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:00:21 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:00:21 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:00:22 | REQ: move cell accepted (RMB) x=39, y=17, mode=advance
2026-03-24 22:00:22 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:00:23 | REQ: move cell accepted (RMB) x=38, y=20, mode=advance
2026-03-24 22:00:23 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:00:23 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 22:00:23 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:00:23 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:00:23 | --- ФАЗА ЧАРДЖА ---
2026-03-24 22:00:23 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:00:23 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:00:23 | Нет доступных целей для чарджа.
2026-03-24 22:00:23 | --- ФАЗА БОЯ ---
2026-03-24 22:00:23 | --- ХОД MODEL ---
2026-03-24 22:00:23 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:00:23 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:00:23 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:00:23 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (16, 9). Выбор reachable_idx=14/481, mode=normal, advance=нет, distance=4
2026-03-24 22:00:23 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (12, 6)
2026-03-24 22:00:23 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:00:28 | [PACE] ack phase=movement unit_id=21 seq=1 step=unit ok=True
2026-03-24 22:00:28 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (8, 12). Выбор reachable_idx=6/455, mode=normal, advance=нет, distance=5
2026-03-24 22:00:28 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (3, 12)
2026-03-24 22:00:28 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:03:42 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 22:03:42 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 22:03:42 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 22:03:42 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 22:03:43 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:03:43 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 22:03:43 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 22:03:43 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth
2026-03-24 22:03:43 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 22:03:48 | Roll-off Attacker/Defender: enemy=2 model=4 -> attacker=model
2026-03-24 22:03:48 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 22:03:48 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 22:03:48 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 22:03:48 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 22:03:48 | [DEPLOY] Order: model first, alternating
2026-03-24 22:03:48 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:03:48 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=791, coord=(13,11), attempt=1, reward=+0.023, score_before=0.000, score_after=0.460, reward_delta=+0.023, forward=0.190, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:03:48 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (13,11)
2026-03-24 22:03:48 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:03:49 | REQ: deploy cell accepted x=50, y=27
2026-03-24 22:03:49 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (27,50)
2026-03-24 22:03:49 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (27,50)
2026-03-24 22:03:49 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:03:49 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=361, coord=(6,1), attempt=1, reward=-0.004, score_before=0.460, score_after=0.374, reward_delta=-0.004, forward=0.105, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:03:49 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (6,1)
2026-03-24 22:03:49 | REQ: deploy cell accepted x=49, y=21
2026-03-24 22:03:50 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,49)
2026-03-24 22:03:50 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,49)
2026-03-24 22:03:50 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.147 avg_spread=1.000 avg_edge=0.750 avg_cover=0.000
2026-03-24 22:03:50 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.018722901064249113, 'units': 2, 'total_deploy_reward': 0.018722901064249113, 'forward_sum': 0.2949152542372881, 'spread_sum': 2.0, 'edge_sum': 1.5, 'cover_sum': 0.0, 'avg_forward': 0.14745762711864405, 'avg_spread': 1.0, 'avg_edge': 0.75, 'avg_cover': 0.0}
2026-03-24 22:03:50 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 22:03:50 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 22:03:50 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 22:03:50 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 22:03:50 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 22:03:50 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 22:03:50 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 22:03:51 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 22:03:51 | --- ХОД PLAYER ---
2026-03-24 22:03:51 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:03:51 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:03:51 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:03:52 | REQ: move cell accepted (RMB) x=39, y=20, mode=advance
2026-03-24 22:03:52 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:03:53 | REQ: move cell accepted (RMB) x=39, y=17, mode=advance
2026-03-24 22:03:53 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:03:53 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 22:03:53 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:03:53 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:03:53 | --- ФАЗА ЧАРДЖА ---
2026-03-24 22:03:53 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:03:53 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:03:53 | Нет доступных целей для чарджа.
2026-03-24 22:03:53 | --- ФАЗА БОЯ ---
2026-03-24 22:03:53 | --- ХОД MODEL ---
2026-03-24 22:03:53 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:03:53 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:03:53 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:03:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (13, 11). Выбор reachable_idx=14/524, mode=normal, advance=нет, distance=4
2026-03-24 22:03:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (9, 8)
2026-03-24 22:03:53 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:04:43 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 22:04:43 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 22:04:43 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 22:04:43 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 22:04:44 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:04:44 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 22:04:44 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 22:04:44 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth
2026-03-24 22:04:44 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 22:04:46 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-03-24 22:04:46 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 22:04:46 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 22:04:46 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 22:04:46 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 22:04:46 | [DEPLOY] Order: model first, alternating
2026-03-24 22:04:46 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:04:46 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1032, coord=(17,12), attempt=1, reward=+0.023, score_before=0.000, score_after=0.468, reward_delta=+0.023, forward=0.207, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:04:46 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (17,12)
2026-03-24 22:04:46 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:04:46 | REQ: deploy cell accepted x=51, y=25
2026-03-24 22:04:46 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,51)
2026-03-24 22:04:46 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,51)
2026-03-24 22:04:46 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:04:46 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=121, coord=(2,1), attempt=1, reward=-0.004, score_before=0.468, score_after=0.378, reward_delta=-0.004, forward=0.114, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:04:46 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (2,1)
2026-03-24 22:04:47 | REQ: deploy cell accepted x=49, y=18
2026-03-24 22:04:48 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,49)
2026-03-24 22:04:48 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,49)
2026-03-24 22:04:48 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.160 avg_spread=1.000 avg_edge=0.750 avg_cover=0.000
2026-03-24 22:04:48 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.01891998423334647, 'units': 2, 'total_deploy_reward': 0.01891998423334647, 'forward_sum': 0.3203389830508474, 'spread_sum': 2.0, 'edge_sum': 1.5, 'cover_sum': 0.0, 'avg_forward': 0.1601694915254237, 'avg_spread': 1.0, 'avg_edge': 0.75, 'avg_cover': 0.0}
2026-03-24 22:04:48 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 22:04:48 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 22:04:48 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 22:04:48 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 22:04:48 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 22:04:48 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 22:04:48 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 22:06:28 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 22:06:28 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 22:06:28 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 22:06:28 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 22:06:28 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 22:06:28 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:06:29 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 22:06:29 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 22:06:29 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth
2026-03-24 22:06:29 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 22:06:31 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-03-24 22:06:31 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 22:06:31 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 22:06:31 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 22:06:31 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 22:06:31 | [DEPLOY] Order: model first, alternating
2026-03-24 22:06:31 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:06:31 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1503, coord=(25,3), attempt=1, reward=+0.020, score_before=0.000, score_after=0.397, reward_delta=+0.020, forward=0.054, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:06:31 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (25,3)
2026-03-24 22:06:31 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:06:31 | REQ: deploy cell accepted x=48, y=27
2026-03-24 22:06:31 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (27,48)
2026-03-24 22:06:31 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (27,48)
2026-03-24 22:06:31 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:06:31 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=908, coord=(15,8), attempt=1, reward=+0.001, score_before=0.397, score_after=0.417, reward_delta=+0.001, forward=0.097, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:06:31 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (15,8)
2026-03-24 22:06:31 | REQ: deploy cell accepted x=47, y=18
2026-03-24 22:06:32 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,47)
2026-03-24 22:06:32 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,47)
2026-03-24 22:06:32 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.075 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-24 22:06:32 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.020851399290500592, 'units': 2, 'total_deploy_reward': 0.020851399290500592, 'forward_sum': 0.15084745762711865, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.07542372881355933, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-24 22:06:32 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 22:06:32 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 22:06:32 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 22:06:32 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 22:06:32 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 22:06:32 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 22:06:32 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 22:06:33 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 22:06:33 | --- ХОД PLAYER ---
2026-03-24 22:06:33 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:06:33 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:06:33 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:06:33 | REQ: move cell accepted (RMB) x=37, y=20, mode=advance
2026-03-24 22:06:34 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:06:34 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 22:06:34 | REQ: move cell accepted (RMB) x=36, y=13, mode=advance
2026-03-24 22:06:35 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:06:35 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 22:06:35 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:06:35 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:06:35 | --- ФАЗА ЧАРДЖА ---
2026-03-24 22:06:35 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:06:35 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:06:35 | Нет доступных целей для чарджа.
2026-03-24 22:06:35 | --- ФАЗА БОЯ ---
2026-03-24 22:06:35 | --- ХОД MODEL ---
2026-03-24 22:06:35 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:06:35 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:06:35 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:06:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (25, 3). Выбор reachable_idx=3/343, mode=normal, advance=нет, distance=5
2026-03-24 22:06:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (20, 2)
2026-03-24 22:06:35 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:07:42 | [PACE] ack phase=movement unit_id=21 seq=1 step=unit ok=True
2026-03-24 22:07:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (15, 8). Выбор reachable_idx=6/458, mode=normal, advance=нет, distance=5
2026-03-24 22:07:42 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (10, 8)
2026-03-24 22:07:42 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:12:09 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 22:12:09 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 22:12:09 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 22:12:09 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 22:12:10 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:12:10 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 22:12:10 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 22:12:10 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth
2026-03-24 22:12:10 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 22:12:12 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-03-24 22:12:12 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 22:12:12 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 22:12:12 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 22:12:12 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 22:12:12 | [DEPLOY] Order: model first, alternating
2026-03-24 22:12:12 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:12:12 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1986, coord=(33,6), attempt=1, reward=+0.021, score_before=0.000, score_after=0.421, reward_delta=+0.021, forward=0.105, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:12:12 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (33,6)
2026-03-24 22:12:12 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:12:12 | REQ: deploy cell accepted x=50, y=26
2026-03-24 22:12:12 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,50)
2026-03-24 22:12:12 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,50)
2026-03-24 22:12:12 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:12:12 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=123, coord=(2,3), attempt=1, reward=-0.002, score_before=0.421, score_after=0.386, reward_delta=-0.002, forward=0.080, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:12:12 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (2,3)
2026-03-24 22:12:12 | REQ: deploy cell accepted x=49, y=16
2026-03-24 22:12:13 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (16,49)
2026-03-24 22:12:13 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (16,49)
2026-03-24 22:12:13 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.092 avg_spread=1.000 avg_edge=0.875 avg_cover=0.000
2026-03-24 22:12:13 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.019294442254631457, 'units': 2, 'total_deploy_reward': 0.019294442254631457, 'forward_sum': 0.18474576271186444, 'spread_sum': 2.0, 'edge_sum': 1.75, 'cover_sum': 0.0, 'avg_forward': 0.09237288135593222, 'avg_spread': 1.0, 'avg_edge': 0.875, 'avg_cover': 0.0}
2026-03-24 22:12:13 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 22:12:13 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 22:12:13 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 22:12:13 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 22:12:13 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 22:12:13 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 22:12:13 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 22:12:16 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 22:12:16 | --- ХОД PLAYER ---
2026-03-24 22:12:16 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:12:16 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:12:16 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:12:16 | REQ: move cell accepted (RMB) x=39, y=23, mode=advance
2026-03-24 22:12:17 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:12:17 | REQ: move cell accepted (RMB) x=39, y=12, mode=advance
2026-03-24 22:12:18 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:12:18 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 22:12:18 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:12:18 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:12:18 | --- ФАЗА ЧАРДЖА ---
2026-03-24 22:12:18 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:12:18 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:12:18 | Нет доступных целей для чарджа.
2026-03-24 22:12:18 | --- ФАЗА БОЯ ---
2026-03-24 22:12:18 | --- ХОД MODEL ---
2026-03-24 22:12:18 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:12:18 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:12:18 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:12:18 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (33, 6). Выбор reachable_idx=3/323, mode=normal, advance=нет, distance=5
2026-03-24 22:12:18 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (28, 3)
2026-03-24 22:12:18 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:12:31 | [PACE] ack phase=movement unit_id=21 seq=1 step=unit ok=True
2026-03-24 22:12:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (2, 3). Выбор reachable_idx=20/209, mode=normal, advance=нет, distance=2
2026-03-24 22:12:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (2, 1)
2026-03-24 22:12:31 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:12:35 | [PACE] ack phase=movement unit_id=22 seq=2 step=unit ok=True
2026-03-24 22:12:35 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 22:12:35 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 22:12:35 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 22:12:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-24 22:12:35 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(39, 12), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 22:12:35 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(39, 12), full_cells=24, rapid_cells=12, вошло=1665, rapid=625, не вошло=735, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-24 22:12:40 | [PACE] ack phase=shooting unit_id=21 seq=3 step=unit ok=True
2026-03-24 22:12:40 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 22:12:40 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 22:12:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-24 22:12:43 | [PACE] ack phase=shooting unit_id=22 seq=4 step=unit ok=True
2026-03-24 22:12:43 | --- ФАЗА ЧАРДЖА ---
2026-03-24 22:12:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-24 22:17:52 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 22:17:52 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 22:17:52 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 22:17:52 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 22:17:53 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:17:53 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 22:17:53 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 22:17:53 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-48-802528.pth
2026-03-24 22:17:53 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 22:17:57 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-03-24 22:17:57 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 22:17:57 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 22:17:57 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 22:17:57 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 22:17:57 | [DEPLOY] Order: model first, alternating
2026-03-24 22:17:57 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:17:57 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1925, coord=(32,5), attempt=1, reward=+0.021, score_before=0.000, score_after=0.413, reward_delta=+0.021, forward=0.088, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:17:57 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (32,5)
2026-03-24 22:17:57 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:17:57 | REQ: deploy cell accepted x=49, y=26
2026-03-24 22:17:57 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,49)
2026-03-24 22:17:57 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,49)
2026-03-24 22:17:57 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:17:57 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=789, coord=(13,9), attempt=1, reward=+0.001, score_before=0.413, score_after=0.429, reward_delta=+0.001, forward=0.122, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:17:57 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (13,9)
2026-03-24 22:17:57 | Ошибка деплоя: reason=outside_deploy_zone, x=44, y=18. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-03-24 22:17:58 | REQ: deploy cell accepted x=51, y=20
2026-03-24 22:17:59 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,51)
2026-03-24 22:17:59 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,51)
2026-03-24 22:17:59 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.105 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-24 22:17:59 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02144264879779267, 'units': 2, 'total_deploy_reward': 0.02144264879779267, 'forward_sum': 0.21016949152542372, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.10508474576271186, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-24 22:17:59 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 22:17:59 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 22:17:59 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 22:17:59 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 22:17:59 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 22:17:59 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 22:17:59 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 22:18:00 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 22:18:00 | --- ХОД PLAYER ---
2026-03-24 22:18:00 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:18:00 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:18:00 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:18:00 | REQ: move cell accepted (RMB) x=38, y=23, mode=advance
2026-03-24 22:18:01 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:18:01 | REQ: move cell accepted (RMB) x=40, y=15, mode=advance
2026-03-24 22:18:02 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:18:02 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 22:18:02 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:18:02 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:18:02 | --- ФАЗА ЧАРДЖА ---
2026-03-24 22:18:02 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:18:02 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:18:02 | Нет доступных целей для чарджа.
2026-03-24 22:18:02 | --- ФАЗА БОЯ ---
2026-03-24 22:18:02 | --- ХОД MODEL ---
2026-03-24 22:18:02 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:18:02 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:18:02 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:18:02 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (32, 5). Выбор reachable_idx=3/322, mode=normal, advance=нет, distance=5
2026-03-24 22:18:02 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (27, 2)
2026-03-24 22:18:02 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:18:05 | [PACE] ack phase=movement unit_id=21 seq=1 step=unit ok=True
2026-03-24 22:18:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (13, 9). Выбор reachable_idx=6/482, mode=normal, advance=нет, distance=5
2026-03-24 22:18:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (8, 9)
2026-03-24 22:18:05 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:32:22 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 22:32:22 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 22:32:22 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 22:32:22 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 22:32:23 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:32:23 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 22:32:23 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 22:32:23 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126.pth
2026-03-24 22:32:23 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 22:32:25 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-03-24 22:32:25 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 22:32:25 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 22:32:25 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 22:32:25 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 22:32:25 | [DEPLOY] Order: model first, alternating
2026-03-24 22:32:25 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:32:25 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1261, coord=(21,1), attempt=1, reward=+0.014, score_before=0.000, score_after=0.289, reward_delta=+0.014, forward=0.020, spread=1.000, edge=0.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:32:25 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (21,1)
2026-03-24 22:32:25 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:32:25 | REQ: deploy cell accepted x=46, y=27
2026-03-24 22:32:25 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (27,46)
2026-03-24 22:32:25 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (27,46)
2026-03-24 22:32:25 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:32:25 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1205, coord=(20,5), attempt=1, reward=-0.009, score_before=0.289, score_after=0.118, reward_delta=-0.009, forward=0.054, spread=0.167, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.667, final_cover=0.000
2026-03-24 22:32:25 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (20,5)
2026-03-24 22:32:26 | REQ: deploy cell accepted x=48, y=14
2026-03-24 22:32:26 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (14,48)
2026-03-24 22:32:26 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (14,48)
2026-03-24 22:32:26 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.006 total_deploy_reward=+0.006 avg_forward=0.037 avg_spread=0.583 avg_edge=0.250 avg_cover=0.000
2026-03-24 22:32:26 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.005912495072920772, 'units': 2, 'total_deploy_reward': 0.005912495072920772, 'forward_sum': 0.07457627118644067, 'spread_sum': 1.1666666666666665, 'edge_sum': 0.5, 'cover_sum': 0.0, 'avg_forward': 0.037288135593220334, 'avg_spread': 0.5833333333333333, 'avg_edge': 0.25, 'avg_cover': 0.0}
2026-03-24 22:32:26 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 22:32:26 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 22:32:26 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 22:32:26 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 22:32:26 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 22:32:26 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 22:32:26 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 22:32:27 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 22:32:27 | --- ХОД PLAYER ---
2026-03-24 22:32:27 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:32:27 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:32:27 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:32:28 | REQ: move cell accepted (RMB) x=35, y=29, mode=advance
2026-03-24 22:32:28 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:32:29 | REQ: move cell accepted (RMB) x=37, y=15, mode=advance
2026-03-24 22:32:30 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:32:30 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 22:32:30 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:32:30 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:32:30 | --- ФАЗА ЧАРДЖА ---
2026-03-24 22:32:30 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:32:30 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:32:30 | Нет доступных целей для чарджа.
2026-03-24 22:32:30 | --- ФАЗА БОЯ ---
2026-03-24 22:32:30 | --- ХОД MODEL ---
2026-03-24 22:32:30 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:32:30 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:32:30 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:32:34 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-03-24 22:32:34 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (21, 1). Выбор reachable_idx=5/297, mode=normal, advance=нет, distance=5
2026-03-24 22:32:34 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (16, 4)
2026-03-24 22:32:34 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:32:36 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-03-24 22:32:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (20, 5). Выбор reachable_idx=18/389, mode=normal, advance=нет, distance=4
2026-03-24 22:32:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (16, 7)
2026-03-24 22:32:36 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:32:36 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 22:32:36 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(37, 15), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 22:32:36 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(37, 15), full_cells=24, rapid_cells=12, вошло=1880, rapid=625, не вошло=520, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-24 22:32:43 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-03-24 22:32:43 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 22:32:43 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 22:32:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-24 22:35:26 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 22:35:26 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 22:35:26 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 22:35:26 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 22:35:27 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:35:27 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 22:35:27 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 22:35:27 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126.pth
2026-03-24 22:35:27 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 22:35:28 | Roll-off Attacker/Defender: enemy=2 model=3 -> attacker=model
2026-03-24 22:35:28 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 22:35:28 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 22:35:28 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 22:35:28 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 22:35:28 | [DEPLOY] Order: model first, alternating
2026-03-24 22:35:28 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:35:28 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=665, coord=(11,5), attempt=1, reward=+0.021, score_before=0.000, score_after=0.413, reward_delta=+0.021, forward=0.088, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:35:28 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (11,5)
2026-03-24 22:35:28 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:35:29 | REQ: deploy cell accepted x=52, y=26
2026-03-24 22:35:29 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,52)
2026-03-24 22:35:29 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,52)
2026-03-24 22:35:29 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:35:29 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1746, coord=(29,6), attempt=1, reward=+0.000, score_before=0.413, score_after=0.417, reward_delta=+0.000, forward=0.097, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:35:29 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (29,6)
2026-03-24 22:35:29 | REQ: deploy cell accepted x=51, y=20
2026-03-24 22:35:30 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,51)
2026-03-24 22:35:30 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,51)
2026-03-24 22:35:30 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.092 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-24 22:35:30 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.020851399290500592, 'units': 2, 'total_deploy_reward': 0.020851399290500592, 'forward_sum': 0.1847457627118644, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.0923728813559322, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-24 22:35:30 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 22:35:30 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 22:35:30 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 22:35:30 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 22:35:30 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 22:35:30 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 22:35:30 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=None, cells_rapid=None, rapid_fire=1, source_cell=(37, 15), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 22:35:30 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=None, cells_rapid=None, rapid_fire=1, source_cell=(51, 20), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 22:35:30 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 22:35:32 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 22:35:32 | --- ХОД PLAYER ---
2026-03-24 22:35:32 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:35:32 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:35:32 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:35:33 | REQ: move cell accepted (RMB) x=41, y=21, mode=advance
2026-03-24 22:35:33 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:35:33 | REQ: move cell accepted (RMB) x=40, y=14, mode=advance
2026-03-24 22:35:34 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:35:34 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 22:35:34 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:35:34 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:35:34 | --- ФАЗА ЧАРДЖА ---
2026-03-24 22:35:34 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:35:34 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:35:34 | Нет доступных целей для чарджа.
2026-03-24 22:35:34 | --- ФАЗА БОЯ ---
2026-03-24 22:35:34 | --- ХОД MODEL ---
2026-03-24 22:35:34 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:35:34 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:35:34 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:35:41 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-03-24 22:35:41 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (11, 5). Выбор reachable_idx=5/390, mode=normal, advance=нет, distance=5
2026-03-24 22:35:41 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (6, 4)
2026-03-24 22:35:41 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:35:45 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-03-24 22:35:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (29, 6). Выбор reachable_idx=18/395, mode=normal, advance=нет, distance=4
2026-03-24 22:35:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (25, 7)
2026-03-24 22:35:45 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:35:45 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 22:35:45 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(40, 14), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 22:35:45 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(40, 14), full_cells=24, rapid_cells=12, вошло=1716, rapid=625, не вошло=684, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-24 22:36:06 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-03-24 22:36:06 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 22:36:06 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 22:36:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-24 22:43:04 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 22:43:04 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 22:43:04 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 22:43:04 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 22:43:05 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:43:05 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 22:43:05 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 22:43:05 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126.pth
2026-03-24 22:43:05 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 22:43:08 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-03-24 22:43:08 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 22:43:08 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 22:43:08 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 22:43:08 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 22:43:08 | [DEPLOY] Order: model first, alternating
2026-03-24 22:43:08 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:43:08 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=904, coord=(15,4), attempt=1, reward=+0.020, score_before=0.000, score_after=0.405, reward_delta=+0.020, forward=0.071, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:43:08 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (15,4)
2026-03-24 22:43:08 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:43:09 | REQ: deploy cell accepted x=51, y=24
2026-03-24 22:43:09 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,51)
2026-03-24 22:43:09 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,51)
2026-03-24 22:43:09 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:43:09 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=129, coord=(2,9), attempt=1, reward=-0.000, score_before=0.405, score_after=0.402, reward_delta=-0.000, forward=0.114, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:43:09 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (2,9)
2026-03-24 22:43:09 | REQ: deploy cell accepted x=51, y=18
2026-03-24 22:43:10 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,51)
2026-03-24 22:43:10 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,51)
2026-03-24 22:43:10 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.020 total_deploy_reward=+0.020 avg_forward=0.092 avg_spread=1.000 avg_edge=0.875 avg_cover=0.000
2026-03-24 22:43:10 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.020082774931020893, 'units': 2, 'total_deploy_reward': 0.020082774931020893, 'forward_sum': 0.18474576271186438, 'spread_sum': 2.0, 'edge_sum': 1.75, 'cover_sum': 0.0, 'avg_forward': 0.09237288135593219, 'avg_spread': 1.0, 'avg_edge': 0.875, 'avg_cover': 0.0}
2026-03-24 22:43:10 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 22:43:10 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 22:43:10 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 22:43:10 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 22:43:10 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 22:43:10 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 22:43:10 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=None, cells_rapid=None, rapid_fire=1, source_cell=(40, 14), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 22:43:10 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=None, cells_rapid=None, rapid_fire=1, source_cell=(51, 18), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 22:43:10 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 22:43:11 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 22:43:11 | --- ХОД PLAYER ---
2026-03-24 22:43:11 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:43:11 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:43:11 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:43:12 | REQ: move cell accepted (RMB) x=40, y=25, mode=advance
2026-03-24 22:43:12 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:43:13 | REQ: move cell accepted (RMB) x=40, y=17, mode=advance
2026-03-24 22:43:13 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:43:13 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 22:43:13 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:43:13 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:43:13 | --- ФАЗА ЧАРДЖА ---
2026-03-24 22:43:13 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:43:13 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:43:13 | Нет доступных целей для чарджа.
2026-03-24 22:43:13 | --- ФАЗА БОЯ ---
2026-03-24 22:43:13 | --- ХОД MODEL ---
2026-03-24 22:43:13 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:43:13 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:43:13 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:43:15 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-03-24 22:43:15 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (15, 4). Выбор reachable_idx=5/367, mode=normal, advance=нет, distance=5
2026-03-24 22:43:15 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (10, 4)
2026-03-24 22:43:15 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:43:17 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-03-24 22:43:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (2, 9). Выбор reachable_idx=18/292, mode=normal, advance=нет, distance=1
2026-03-24 22:43:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 10)
2026-03-24 22:43:17 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:43:17 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 22:43:17 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(40, 17), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 22:43:17 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(40, 17), full_cells=24, rapid_cells=12, вошло=1760, rapid=625, не вошло=640, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-24 22:43:30 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-03-24 22:43:30 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 22:43:30 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 22:43:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-24 22:43:31 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-03-24 22:43:31 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 22:43:31 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 22:43:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-24 22:43:31 | --- ФАЗА ЧАРДЖА ---
2026-03-24 22:43:32 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-03-24 22:43:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-24 22:43:33 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-03-24 22:43:33 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-24 22:43:33 | [MODEL] Чардж: нет доступных целей
2026-03-24 22:43:33 | --- ФАЗА БОЯ ---
2026-03-24 22:43:33 | [MODEL] Ближний бой: нет доступных атак
2026-03-24 22:43:33 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-24 22:43:33 | Итерация 0 завершена с наградой tensor([-0.0200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-24 22:43:33 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 22:43:33 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-24 22:43:35 | === БОЕВОЙ РАУНД 2 ===
2026-03-24 22:43:35 | --- ХОД PLAYER ---
2026-03-24 22:43:35 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:43:35 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:43:35 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:55:49 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 22:55:49 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 22:55:49 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 22:55:49 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 22:55:50 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:55:51 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 22:55:51 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 22:55:51 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126.pth
2026-03-24 22:55:51 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 22:55:54 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-03-24 22:55:54 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 22:55:54 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 22:55:54 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 22:55:54 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 22:55:54 | [DEPLOY] Order: model first, alternating
2026-03-24 22:55:54 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:55:54 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=186, coord=(3,6), attempt=1, reward=+0.021, score_before=0.000, score_after=0.421, reward_delta=+0.021, forward=0.105, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:55:54 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (3,6)
2026-03-24 22:55:54 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 22:55:54 | REQ: deploy cell accepted x=50, y=26
2026-03-24 22:55:54 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,50)
2026-03-24 22:55:54 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,50)
2026-03-24 22:55:54 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 22:55:54 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=482, coord=(8,2), attempt=1, reward=-0.004, score_before=0.421, score_after=0.335, reward_delta=-0.004, forward=0.071, spread=0.833, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 22:55:54 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (8,2)
2026-03-24 22:55:55 | REQ: deploy cell accepted x=49, y=18
2026-03-24 22:55:56 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,49)
2026-03-24 22:55:56 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,49)
2026-03-24 22:55:56 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.017 total_deploy_reward=+0.017 avg_forward=0.088 avg_spread=0.917 avg_edge=0.875 avg_cover=0.000
2026-03-24 22:55:56 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.016771777690185258, 'units': 2, 'total_deploy_reward': 0.016771777690185258, 'forward_sum': 0.17627118644067796, 'spread_sum': 1.8333333333333335, 'edge_sum': 1.75, 'cover_sum': 0.0, 'avg_forward': 0.08813559322033898, 'avg_spread': 0.9166666666666667, 'avg_edge': 0.875, 'avg_cover': 0.0}
2026-03-24 22:55:56 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 22:55:56 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 22:55:56 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 22:55:56 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 22:55:56 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 22:55:56 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 22:55:56 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 22:55:57 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 22:55:57 | --- ХОД PLAYER ---
2026-03-24 22:55:57 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:55:57 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:55:57 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 22:55:57 | REQ: move cell accepted (RMB) x=39, y=23, mode=advance
2026-03-24 22:55:58 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:55:58 | REQ: move cell accepted (RMB) x=38, y=16, mode=advance
2026-03-24 22:55:59 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 22:55:59 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 22:55:59 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:55:59 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 22:55:59 | --- ФАЗА ЧАРДЖА ---
2026-03-24 22:55:59 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:55:59 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 22:55:59 | Нет доступных целей для чарджа.
2026-03-24 22:55:59 | --- ФАЗА БОЯ ---
2026-03-24 22:55:59 | --- ХОД MODEL ---
2026-03-24 22:55:59 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 22:55:59 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 22:55:59 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 23:11:31 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-24 23:11:31 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-24 23:11:31 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-24 23:11:31 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-24 23:11:31 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 23:11:32 | [MODEL] checkpoint: используется C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126.pth (рядом нет C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126_P1_Necrons_only_war_final_ep100.pth)
2026-03-24 23:11:32 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126_P1_Necrons_only_war_final_ep100.pickle
2026-03-24 23:11:32 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons__learner_P1_Necrons\model-29-220126.pth
2026-03-24 23:11:32 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-24 23:11:34 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-03-24 23:11:34 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-24 23:11:34 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-24 23:11:34 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-24 23:11:34 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-24 23:11:34 | [DEPLOY] Order: model first, alternating
2026-03-24 23:11:34 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 23:11:34 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=122, coord=(2,2), attempt=1, reward=+0.017, score_before=0.000, score_after=0.343, reward_delta=+0.017, forward=0.037, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 23:11:34 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (2,2)
2026-03-24 23:11:34 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-24 23:11:35 | REQ: deploy cell accepted x=54, y=24
2026-03-24 23:11:35 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,54)
2026-03-24 23:11:35 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,54)
2026-03-24 23:11:35 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-24 23:11:35 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1203, coord=(20,3), attempt=1, reward=+0.001, score_before=0.343, score_after=0.370, reward_delta=+0.001, forward=0.046, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-24 23:11:35 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (20,3)
2026-03-24 23:11:35 | REQ: deploy cell accepted x=49, y=19
2026-03-24 23:11:36 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,49)
2026-03-24 23:11:36 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,49)
2026-03-24 23:11:36 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.042 avg_spread=1.000 avg_edge=0.625 avg_cover=0.000
2026-03-24 23:11:36 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.018506109578242017, 'units': 2, 'total_deploy_reward': 0.018506109578242017, 'forward_sum': 0.08305084745762711, 'spread_sum': 2.0, 'edge_sum': 1.25, 'cover_sum': 0.0, 'avg_forward': 0.04152542372881356, 'avg_spread': 1.0, 'avg_edge': 0.625, 'avg_cover': 0.0}
2026-03-24 23:11:36 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-24 23:11:36 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-03-24 23:11:36 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-24 23:11:36 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-24 23:11:36 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 23:11:36 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-24 23:11:36 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 23:11:38 | === БОЕВОЙ РАУНД 1 ===
2026-03-24 23:11:38 | --- ХОД PLAYER ---
2026-03-24 23:11:38 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 23:11:38 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 23:11:38 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 23:11:38 | REQ: move cell accepted (RMB) x=44, y=18, mode=advance
2026-03-24 23:11:38 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 23:11:38 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 23:11:39 | REQ: move cell accepted (RMB) x=40, y=26, mode=advance
2026-03-24 23:11:40 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 23:11:40 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 23:11:40 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 23:11:40 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 23:11:40 | --- ФАЗА ЧАРДЖА ---
2026-03-24 23:11:40 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 23:11:40 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 23:11:40 | Нет доступных целей для чарджа.
2026-03-24 23:11:40 | --- ФАЗА БОЯ ---
2026-03-24 23:11:40 | --- ХОД MODEL ---
2026-03-24 23:11:40 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 23:11:40 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 23:11:40 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 23:11:52 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-03-24 23:11:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (2, 2). Выбор reachable_idx=5/195, mode=normal, advance=нет, distance=2
2026-03-24 23:11:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 4)
2026-03-24 23:11:52 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 23:11:54 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-03-24 23:11:54 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (20, 3). Выбор reachable_idx=18/344, mode=normal, advance=нет, distance=5
2026-03-24 23:11:54 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (16, 8)
2026-03-24 23:11:54 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 23:11:54 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 23:11:54 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(40, 26), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 23:11:54 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(40, 26), full_cells=24, rapid_cells=12, вошло=1672, rapid=625, не вошло=728, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-24 23:11:59 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-03-24 23:11:59 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=38.00, range=24.00, delta=+14.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 23:11:59 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 23:11:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-24 23:12:04 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-03-24 23:12:04 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 23:12:04 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 23:12:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-24 23:12:04 | --- ФАЗА ЧАРДЖА ---
2026-03-24 23:12:05 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-03-24 23:12:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-24 23:12:06 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-03-24 23:12:06 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-24 23:12:06 | [MODEL] Чардж: нет доступных целей
2026-03-24 23:12:06 | --- ФАЗА БОЯ ---
2026-03-24 23:12:06 | [MODEL] Ближний бой: нет доступных атак
2026-03-24 23:12:06 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-24 23:12:06 | Итерация 0 завершена с наградой tensor([0.0387], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-24 23:12:06 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 23:12:06 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-24 23:12:07 | === БОЕВОЙ РАУНД 2 ===
2026-03-24 23:12:07 | --- ХОД PLAYER ---
2026-03-24 23:12:07 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 23:12:07 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-24 23:12:07 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 23:12:09 | REQ: move cell accepted (RMB) x=33, y=16, mode=advance
2026-03-24 23:12:09 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-24 23:12:09 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-24 23:12:09 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-24 23:12:09 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-24 23:12:09 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-24 23:12:09 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-24 23:12:09 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-24 23:12:09 | Оружие: Gauss flayer
2026-03-24 23:12:09 | FX: найдена строка оружия: Gauss flayer.
2026-03-24 23:12:09 | BS оружия: 4+
2026-03-24 23:12:09 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-24 23:12:09 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-24 23:12:09 | Save цели: 4+ (invul: нет)
2026-03-24 23:12:09 | Benefit of Cover: не активен.
2026-03-24 23:12:09 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-24 23:12:09 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-24 23:12:09 | Правило: Overwatch: попадания только на 6+
2026-03-24 23:12:09 | Hit rolls:    [5, 5, 4, 4, 4, 5, 4, 2, 1, 1]  -> hits: 0
2026-03-24 23:12:09 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-24 23:12:09 | FX: найден итог урона = 0.0.
2026-03-24 23:12:09 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=0.0).
2026-03-24 23:12:09 | FX: позиция эффекта start=(204.0,396.0) end=(1068.0,444.0).
2026-03-24 23:12:09 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-24 23:12:09 | 📌 -------------------------

2026-03-24 23:12:10 | REQ: move cell accepted (RMB) x=29, y=15, mode=advance
2026-03-24 23:12:10 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-24 23:12:10 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-24 23:12:10 | 
🎲 Бросок сейвы (save): 3D6
2026-03-24 23:12:10 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-03-24 23:12:10 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-24 23:12:10 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-24 23:12:10 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-24 23:12:10 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-24 23:12:10 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-24 23:12:10 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-24 23:12:10 | Оружие: Gauss flayer
2026-03-24 23:12:10 | FX: найдена строка оружия: Gauss flayer.
2026-03-24 23:12:10 | BS оружия: 4+
2026-03-24 23:12:10 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-24 23:12:10 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-24 23:12:10 | Save цели: 4+ (invul: нет)
2026-03-24 23:12:10 | Benefit of Cover: не активен.
2026-03-24 23:12:10 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-24 23:12:10 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-24 23:12:10 | Правило: Overwatch: попадания только на 6+
2026-03-24 23:12:10 | Hit rolls:    [6, 3, 4, 4, 2, 6, 5, 6, 5, 1]  -> hits: 3 (crits: 3)
2026-03-24 23:12:10 | Save rolls:   [3, 2, 6]  (цель 4+) -> failed saves: 2
2026-03-24 23:12:10 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-24 23:12:10 | FX: найден итог урона = 2.0.
2026-03-24 23:12:10 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=2.0).
2026-03-24 23:12:10 | FX: позиция эффекта start=(204.0,396.0) end=(972.0,636.0).
2026-03-24 23:12:10 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-24 23:12:10 | 📌 -------------------------

2026-03-24 23:12:10 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 23:12:10 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 23:12:10 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-24 23:12:10 | --- ФАЗА ЧАРДЖА ---
2026-03-24 23:12:10 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 23:12:10 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-24 23:12:10 | Нет доступных целей для чарджа.
2026-03-24 23:12:10 | --- ФАЗА БОЯ ---
2026-03-24 23:12:10 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 23:12:10 | --- ХОД MODEL ---
2026-03-24 23:12:10 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 23:12:10 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-24 23:12:10 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-24 23:12:14 | [PACE] ack phase=movement unit_id=21 seq=7 step=before_unit ok=True
2026-03-24 23:12:14 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 3). Выбор reachable_idx=5/194, mode=normal, advance=нет, distance=1
2026-03-24 23:12:14 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 4)
2026-03-24 23:12:14 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-24 23:12:15 | [PACE] ack phase=movement unit_id=22 seq=8 step=before_unit ok=True
2026-03-24 23:12:15 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (16, 8). Выбор reachable_idx=18/459, mode=normal, advance=нет, distance=4
2026-03-24 23:12:15 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (12, 9)
2026-03-24 23:12:15 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-24 23:12:16 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-24 23:12:16 | FX: перепроигрываю 30 строк(и) лога.
2026-03-24 23:12:16 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(29, 15), target_filter_size=2, max_target_dist=26, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-24 23:12:16 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(29, 15), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-24 23:12:29 | [PACE] ack phase=shooting unit_id=21 seq=9 step=before_unit ok=True
2026-03-24 23:12:29 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-24 23:12:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-24 23:12:29 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-24 23:12:29 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-24 23:12:29 | 
🎲 Бросок сейвы (save): 5D6
2026-03-24 23:12:29 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 5. Осталось: 3. HP: 8.0 -> 3.0 (shooting)
2026-03-24 23:12:29 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 3. Причина: потери моделей.
2026-03-24 23:12:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 5.0
2026-03-24 23:12:29 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-24 23:12:29 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-24 23:12:29 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-24 23:12:29 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-24 23:12:29 | Оружие: Gauss flayer
2026-03-24 23:12:29 | FX: найдена строка оружия: Gauss flayer.
2026-03-24 23:12:29 | BS оружия: 4+
2026-03-24 23:12:29 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-24 23:12:29 | Save цели: 4+ (invul: нет)
2026-03-24 23:12:29 | Benefit of Cover: не активен.
2026-03-24 23:12:29 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-24 23:12:29 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-24 23:12:29 | Hit rolls:    [2, 5, 2, 4, 1, 6, 6, 4, 4, 1]  -> hits: 6 (crits: 2)
2026-03-24 23:12:29 | Wound rolls:  [4, 3, 5, 5]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 2 = 5
2026-03-24 23:12:29 | Save rolls:   [1, 2, 3, 2, 2]  (цель 4+) -> failed saves: 5
2026-03-24 23:12:29 | 
✅ Итог по движку: прошло урона = 5.0
2026-03-24 23:12:29 | FX: найден итог урона = 5.0.
2026-03-24 23:12:29 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=5.0).
2026-03-24 23:12:29 | FX: позиция эффекта start=(84.0,36.0) end=(708.0,372.0).
2026-03-24 23:12:29 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-24 23:12:29 | 📌 -------------------------

2026-03-24 23:12:35 | [PACE] ack phase=shooting unit_id=22 seq=10 step=before_unit ok=True
2026-03-24 23:12:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: выбор политики)
2026-03-24 23:12:35 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-24 23:12:35 | 
🎲 Бросок на ранение (to wound): 6D6
2026-03-24 23:12:35 | 
🎲 Бросок сейвы (save): 4D6
2026-03-24 23:12:35 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 4. Осталось: 6. HP: 10.0 -> 6.0 (shooting)
2026-03-24 23:12:35 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-03-24 23:12:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 4.0
2026-03-24 23:12:35 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-24 23:12:35 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-24 23:12:35 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-24 23:12:35 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-24 23:12:35 | Оружие: Gauss flayer
2026-03-24 23:12:35 | FX: найдена строка оружия: Gauss flayer.
2026-03-24 23:12:35 | BS оружия: 4+
2026-03-24 23:12:35 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-24 23:12:35 | Save цели: 4+ (invul: нет)
2026-03-24 23:12:35 | Benefit of Cover: не активен.
2026-03-24 23:12:35 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-24 23:12:35 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-24 23:12:35 | Hit rolls:    [5, 4, 5, 5, 5, 1, 6, 1, 4, 2]  -> hits: 7 (crits: 1)
2026-03-24 23:12:35 | Wound rolls:  [5, 5, 3, 4, 3, 2]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 1 = 4
2026-03-24 23:12:35 | Save rolls:   [2, 1, 3, 2]  (цель 4+) -> failed saves: 4
2026-03-24 23:12:35 | 
✅ Итог по движку: прошло урона = 4.0
2026-03-24 23:12:35 | FX: найден итог урона = 4.0.
2026-03-24 23:12:35 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=4.0).
2026-03-24 23:12:35 | FX: позиция эффекта start=(228.0,300.0) end=(804.0,396.0).
2026-03-24 23:12:35 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-24 23:12:35 | 📌 -------------------------

2026-03-24 23:12:35 | --- ФАЗА ЧАРДЖА ---
2026-03-24 23:12:38 | [PACE] ack phase=charge unit_id=21 seq=11 step=before_unit ok=True
2026-03-24 23:12:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-24 23:12:39 | [PACE] ack phase=charge unit_id=22 seq=12 step=before_unit ok=True
2026-03-24 23:12:39 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-24 23:12:39 | [MODEL] Чардж: нет доступных целей
2026-03-24 23:12:39 | --- ФАЗА БОЯ ---
2026-03-24 23:12:39 | [MODEL] Ближний бой: нет доступных атак
2026-03-24 23:12:39 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-24 23:12:39 | Итерация 1 завершена с наградой tensor([0.6205], device='cuda:0'), здоровье игрока [6.0, 3.0], здоровье модели [10.0, 10.0]
2026-03-24 23:12:39 | {'model health': [10.0, 10.0], 'player health': [6.0, 3.0], 'model alive models': [10, 10], 'player alive models': [6, 3], 'modelCP': 2, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-24 23:12:39 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [6.0, 3.0]
CP MODEL: 2, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 5.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 4.0 раз(а)

2026-03-24 23:12:40 | === БОЕВОЙ РАУНД 3 ===
2026-03-24 23:12:40 | --- ХОД PLAYER ---
2026-03-24 23:12:40 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-24 23:12:40 | Unit 12 — Necrons Necron Warriors (x10 моделей): ниже половины состава, тест Battle-shock.
2026-03-24 23:12:40 | Бросок 2D6...
