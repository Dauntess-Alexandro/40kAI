2026-02-06 12:11:28 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-02-06 12:11:28 | [VIEWER] Фоллбэк-рендер не активирован.
2026-02-06 12:11:28 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 12:11:29 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-3-407495.pickle
2026-02-06 12:11:29 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-3-407495.pth
2026-02-06 12:11:44 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-02-06 12:11:44 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-02-06 12:11:44 | [DEPLOY] Order: model first, alternating
2026-02-06 12:11:44 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (12,2)
2026-02-06 12:11:44 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (4,30)
2026-02-06 12:11:44 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (11,9)
2026-02-06 12:11:44 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (50,33)
2026-02-06 12:11:44 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-02-06 12:11:44 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-02-06 12:11:44 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-02-06 12:11:44 | {'model health': [10, 10], 'player health': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-02-06 12:11:44 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-02-06 12:11:44 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 12:11:45 | === БОЕВОЙ РАУНД 1 ===
2026-02-06 12:11:45 | --- ХОД PLAYER ---
2026-02-06 12:11:45 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 12:11:45 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0
2026-02-06 12:11:45 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 12:11:45 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 12:11:45 | REQ: target selected Unit 11, confirm enabled
2026-02-06 12:11:45 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 12:11:45 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 12:11:45 | REQ: target selected Unit 11, confirm enabled
2026-02-06 12:11:51 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-02-06 12:11:51 | 
🎲 Бросок на попадание (to hit): 10D6
2026-02-06 12:11:51 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-02-06 12:11:51 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-02-06 12:11:51 | FX: старт отчёта (overwatch), ts=no-ts.
2026-02-06 12:11:51 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-02-06 12:11:51 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-02-06 12:11:51 | Оружие: Gauss flayer
2026-02-06 12:11:51 | FX: найдена строка оружия: Gauss flayer.
2026-02-06 12:11:51 | BS оружия: 4+
2026-02-06 12:11:51 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-02-06 12:11:51 | Save цели: 4+ (invul: нет)
2026-02-06 12:11:51 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-02-06 12:11:51 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-02-06 12:11:51 | Правило: Overwatch: попадания только на 6+
2026-02-06 12:11:51 | Hit rolls:    [3, 2, 1, 3, 4, 1, 1, 5, 4, 4]  -> hits: 4
2026-02-06 12:11:51 | 
✅ Итог по движку: прошло урона = 0.0
2026-02-06 12:11:51 | FX: найден итог урона = 0.0.
2026-02-06 12:11:51 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=0.0).
2026-02-06 12:11:51 | FX: shot grid attacker=(11,9) target=(4,30) cell_size=18
2026-02-06 12:11:51 | FX: позиция эффекта start=(207.0,171.0) end=(81.0,549.0).
2026-02-06 12:11:51 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-02-06 12:11:51 | 📌 -------------------------

2026-02-06 12:11:51 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-02-06 12:11:51 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 12:11:51 | REQ: target selected Unit 12, confirm enabled
2026-02-06 12:11:51 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 12:11:51 | FX: старт отчёта (overwatch), ts=no-ts.
2026-02-06 12:11:51 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-02-06 12:11:51 | FX: найдена строка оружия: Gauss flayer.
2026-02-06 12:11:51 | FX: найден итог урона = 0.0.
2026-02-06 12:11:51 | FX: дубликат отчёта, эффект не создаём.
2026-02-06 12:11:51 | FX: старт GUI — пропускаю накопленные события модели, подхват с event_id=3.
2026-02-06 12:11:51 | Выбрано в таблице: row=3 -> unit_id=12
2026-02-06 12:11:51 | REQ: target selected Unit 12, confirm enabled
2026-02-06 12:11:55 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 12:11:55 | REQ: shooter changed Unit 12->Unit 11, target reset
2026-02-06 12:11:55 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 12:11:55 | REQ: target selected Unit 11, confirm enabled
2026-02-06 12:11:55 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 12:11:55 | REQ: target selected Unit 11, confirm enabled
2026-02-06 12:11:57 | 
🎲 Бросок на попадание (to hit): 10D6
2026-02-06 12:12:02 | 
🎲 Бросок на ранение (to wound): 7D6
2026-02-06 12:12:04 | 
🎲 Бросок сейвы (save): 2D6
2026-02-06 12:12:06 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 1.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-02-06 12:12:06 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-02-06 12:12:06 | FX: старт отчёта (shooting), ts=no-ts.
2026-02-06 12:12:06 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-02-06 12:12:06 | FX: найдена строка стрельбы (attacker=11, target=22).
2026-02-06 12:12:06 | Оружие: Gauss flayer
2026-02-06 12:12:06 | FX: найдена строка оружия: Gauss flayer.
2026-02-06 12:12:06 | BS оружия: 4+
2026-02-06 12:12:06 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-02-06 12:12:06 | Save цели: 4+ (invul: нет)
2026-02-06 12:12:06 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-02-06 12:12:06 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-02-06 12:12:06 | Hit rolls:    [2, 3, 4, 5, 5, 5, 5, 5, 5, 3]  -> hits: 7
2026-02-06 12:12:06 | Wound rolls:  [3, 4, 1, 2, 3, 4, 1]  (цель 4+) -> wounds: 2
2026-02-06 12:12:06 | Save rolls:   [3, 4]  (цель 4+) -> failed saves: 1
2026-02-06 12:12:06 | 
✅ Итог по движку: прошло урона = 1.0
2026-02-06 12:12:06 | FX: найден итог урона = 1.0.
2026-02-06 12:12:06 | FX: создан FxShotEvent (attacker=11, target=22, weapon=Gauss flayer, damage=1.0).
2026-02-06 12:12:06 | FX: shot grid attacker=(4,25) target=(11,9) cell_size=18
2026-02-06 12:12:06 | FX: позиция эффекта start=(81.0,459.0) end=(207.0,171.0).
2026-02-06 12:12:06 | FX: эффект добавлен в рендер (attacker=11, target=22).
2026-02-06 12:12:06 | 📌 -------------------------

2026-02-06 12:12:06 | --- ФАЗА ЧАРДЖА ---
2026-02-06 12:12:06 | Нет доступных целей для чарджа.
2026-02-06 12:12:06 | --- ФАЗА БОЯ ---
2026-02-06 12:12:06 | --- ХОД MODEL ---
2026-02-06 12:12:06 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 12:12:06 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 12:12:06 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-02-06 12:12:06 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 2
2026-02-06 12:12:06 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-02-06 12:12:06 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-02-06 12:12:06 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-02-06 12:12:06 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0
2026-02-06 12:12:06 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 12:12:06 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 12:12:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (12, 2). Выбор: up, advance=да, бросок=6, макс=11, distance=11
2026-02-06 12:12:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 2)
2026-02-06 12:12:06 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-02-06 12:12:06 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 12:12:06 | FX: старт отчёта (shooting), ts=no-ts.
2026-02-06 12:12:06 | FX: найдена строка стрельбы (attacker=11, target=22).
2026-02-06 12:12:06 | FX: найдена строка оружия: Gauss flayer.
2026-02-06 12:12:06 | FX: найден итог урона = 1.0.
2026-02-06 12:12:06 | FX: дубликат отчёта, эффект не создаём.
2026-02-06 12:12:06 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 12:12:08 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (11, 9). Выбор: up, advance=да, бросок=2, макс=7, distance=7
2026-02-06 12:12:08 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (4, 9)
2026-02-06 12:12:08 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-02-06 12:12:10 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.045361017187261->18.027756377319946
2026-02-06 12:12:10 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 12:12:10 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-06 12:12:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-02-06 12:12:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-02-06 12:12:10 | --- ФАЗА ЧАРДЖА ---
2026-02-06 12:12:10 | --- ФАЗА ЧАРДЖА ---
2026-02-06 12:12:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-02-06 12:12:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-02-06 12:12:10 | [MODEL] Чардж: нет доступных целей
2026-02-06 12:12:10 | --- ФАЗА БОЯ ---
2026-02-06 12:12:10 | --- ФАЗА БОЯ ---
2026-02-06 12:12:10 | [MODEL] Ближний бой: нет доступных атак
2026-02-06 12:12:10 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.045361017187261->18.027756377319946
2026-02-06 12:12:10 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-02-06 12:12:10 | Итерация 0 завершена с наградой tensor([-0.0500], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-02-06 12:12:10 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'modelCP': 1, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-02-06 12:12:10 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 1, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-02-06 12:12:10 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 12:12:10 | FX: buffer phase command (model)
2026-02-06 12:12:10 | FX: enqueue phase script command: units=0
2026-02-06 12:12:10 | FX: show summary command VP=0, CP=1
2026-02-06 12:12:10 | FX: wait_continue reason=phase_done next=ФАЗА ДВИЖЕНИЯ
2026-02-06 12:12:10 | FX: buffer phase movement (model)
2026-02-06 12:12:10 | FX: enqueue phase script movement: units=2
2026-02-06 12:12:10 | FX: buffer phase shooting (model)
2026-02-06 12:12:10 | FX: enqueue phase script shooting: units=2
2026-02-06 12:12:10 | FX: buffer phase charge (model)
2026-02-06 12:12:10 | FX: enqueue phase script charge: units=2
2026-02-06 12:12:10 | FX: buffer phase fight (model)
2026-02-06 12:12:10 | FX: enqueue phase script fight: units=2
2026-02-06 12:12:15 | FX: continue=Y
2026-02-06 12:12:15 | FX: show summary movement двигались 2/2, advance=2, dist=18.0
2026-02-06 12:12:15 | FX: move apply event_id=15 unit_id=21 side=model action=move from=[12, 2] types=('int', 'int') to=[1, 2] types=('int', 'int') key=('model', 21) render_found=1
2026-02-06 12:12:15 | FX: move write unit_id=21 side=model grid=(1,2) before=(12, 2) after=(1,2) cell_size=18 conversion=grid->world(cell_size)
2026-02-06 12:12:15 | FX: play unit_action unit=21 action=move
2026-02-06 12:12:15 | FX: wait_continue reason=unit_done next=Unit 22 — Necron Warriors (🚶 Движение: [11, 9] → [4, 9], dist=7.0, advance=да)
2026-02-06 12:12:18 | FX: continue=Y
2026-02-06 12:12:18 | Выбрано в таблице: row=1 -> unit_id=22
2026-02-06 12:12:18 | FX: move apply event_id=20 unit_id=22 side=model action=move from=[11, 9] types=('int', 'int') to=[4, 9] types=('int', 'int') key=('model', 22) render_found=1
2026-02-06 12:12:18 | FX: move write unit_id=22 side=model grid=(4,9) before=(11, 9) after=(4,9) cell_size=18 conversion=grid->world(cell_size)
2026-02-06 12:12:18 | FX: play unit_action unit=22 action=move
2026-02-06 12:12:18 | FX: wait_continue reason=unit_done next=unit
2026-02-06 12:12:21 | FX: continue=Y
2026-02-06 12:12:21 | FX: wait_continue reason=phase_done next=ФАЗА СТРЕЛЬБЫ
2026-02-06 12:12:23 | FX: continue=Y
2026-02-06 12:12:23 | FX: show summary shooting shots=0, skipped=2 (reasons: advanced_no_assault=2)
2026-02-06 12:12:23 | Выбрано в таблице: row=0 -> unit_id=21
2026-02-06 12:12:23 | FX: play unit_action unit=21 action=skip_shoot
2026-02-06 12:12:23 | FX: wait_continue reason=unit_done next=Unit 22 — Necron Warriors (⏭️ Skip shoot (advanced_no_assault))
2026-02-06 12:12:24 | FX: continue=Y
2026-02-06 12:12:24 | Выбрано в таблице: row=1 -> unit_id=22
2026-02-06 12:12:24 | FX: play unit_action unit=22 action=skip_shoot
2026-02-06 12:12:24 | FX: wait_continue reason=unit_done next=unit
2026-02-06 12:12:25 | FX: continue=Y
2026-02-06 12:12:25 | FX: wait_continue reason=phase_done next=ФАЗА ЧАРДЖА
2026-02-06 12:12:25 | FX: continue=Y
2026-02-06 12:12:25 | FX: show summary charge charges=0, skipped=2 (reasons: advanced_no_charge=2)
2026-02-06 12:12:25 | Выбрано в таблице: row=0 -> unit_id=21
2026-02-06 12:12:25 | FX: play unit_action unit=21 action=skip_charge
2026-02-06 12:12:25 | FX: wait_continue reason=unit_done next=Unit 22 — Necron Warriors (⏭️ Skip charge (advanced_no_charge))
2026-02-06 12:12:25 | FX: continue=Y
2026-02-06 12:12:25 | Выбрано в таблице: row=1 -> unit_id=22
2026-02-06 12:12:25 | FX: play unit_action unit=22 action=skip_charge
2026-02-06 12:12:25 | FX: wait_continue reason=unit_done next=unit
2026-02-06 12:12:26 | FX: continue=Y
2026-02-06 12:12:26 | FX: wait_continue reason=phase_done next=ФАЗА БОЯ
2026-02-06 12:12:26 | FX: continue=Y
2026-02-06 12:12:26 | FX: show summary fight fights=0, skipped=2 (reasons: no_attacks=2)
2026-02-06 12:12:26 | Выбрано в таблице: row=0 -> unit_id=21
2026-02-06 12:12:26 | FX: play unit_action unit=21 action=skip_fight
2026-02-06 12:12:26 | FX: wait_continue reason=unit_done next=Unit 22 — Necron Warriors (⏭️ Skip fight (no_attacks))
2026-02-06 12:12:26 | FX: continue=Y
2026-02-06 12:12:26 | Выбрано в таблице: row=1 -> unit_id=22
2026-02-06 12:12:26 | FX: play unit_action unit=22 action=skip_fight
2026-02-06 12:12:26 | FX: wait_continue reason=unit_done next=unit
2026-02-06 12:12:26 | FX: continue=Y
2026-02-06 12:12:26 | FX: wait_continue reason=phase_done next=ФАЗА БОЯ
2026-02-06 12:12:27 | FX: continue=Y
2026-02-06 12:12:27 | === БОЕВОЙ РАУНД 2 ===
2026-02-06 12:12:27 | --- ХОД PLAYER ---
2026-02-06 12:12:27 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-06 12:12:27 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0
2026-02-06 12:12:27 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-06 12:12:27 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 12:12:27 | REQ: target selected Unit 11, confirm enabled
2026-02-06 12:12:27 | FX: перепроигрываю 30 строк(и) лога.
2026-02-06 12:12:27 | Выбрано в таблице: row=2 -> unit_id=11
2026-02-06 12:12:27 | REQ: target selected Unit 11, confirm enabled
