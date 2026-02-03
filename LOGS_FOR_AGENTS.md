2026-02-03 13:17:48 | [TRAIN][START] DoubleDQN=1 Dueling=1 PER=1 N_STEP=3 LR=0.0001 clip_reward=off grad_clip=100.0 NUM_ENVS=8 BATCH_ACT=1 USE_AMP=1 USE_COMPILE=0 USE_SUBPROC_ENVS=0 PREFETCH=0 PIN_MEMORY=0 LOG_EVERY=200 SAVE_EVERY=0
2026-02-03 13:17:49 | Старт обучения: model_hp_total=20.0, enemy_hp_total=20.0, battle_round=1, trunc=True
2026-02-03 13:17:49 | Логи фаз/ходов отключены (trunc=True). Чтобы включить подробные логи: VERBOSE_LOGS=1 или MANUAL_DICE=1.
2026-02-03 13:17:49 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.082762530298219->6.324555320336759
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:49 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:49 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.656854249492381->8.94427190999916
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0->8.0
2026-02-03 13:17:49 | [MASK][SHOOT] Доступные индексы: 0..1, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:49 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:49 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:49 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.082762530298219->9.219544457292887
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.06225774829855
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:49 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:49 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:49 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:49 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=15.033296378372908->16.55294535724685
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.0->10.63014581273465
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:49 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:49 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:49 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:49 | Reward (бой): advantage_term=+0.045
2026-02-03 13:17:49 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.075
2026-02-03 13:17:49 | Reward (шаг): бой delta=+0.075
2026-02-03 13:17:49 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:49 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:49 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:49 | Reward (стрик удержания): streaks=[0, 0, 0, 3], len=2, bonus=+0.200
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:49 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:49 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:49 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:49 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:49 | Reward (бой): advantage_term=+0.045
2026-02-03 13:17:49 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.075
2026-02-03 13:17:49 | Reward (шаг): бой delta=+0.075
2026-02-03 13:17:49 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:49 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:49 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.63014581273465->10.63014581273465
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.082762530298219->8.06225774829855
2026-02-03 13:17:49 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=2, размер пространства=2.
2026-02-03 13:17:49 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:49 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:49 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:49 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:49 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.63014581273465->10.63014581273465
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:49 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:49 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.700
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:49 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:49 | Reward (VP diff): prev=-2, curr=-3, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.63014581273465->13.601470508735444
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.06225774829855
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:49 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:49 | Reward (VP diff): prev=3, curr=4, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:49 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:49 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.730
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:49 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:49 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:49 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:49 | Reward (бой): kill_term=+0.400 (delta=1)
2026-02-03 13:17:49 | Reward (бой): advantage_term=+0.120
2026-02-03 13:17:49 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.400 (delta=1), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.120, strength=0.000, objectives=0.000 (delta=0), total=0.580
2026-02-03 13:17:49 | Reward (шаг): бой delta=+0.580
2026-02-03 13:17:49 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:49 | Reward (VP diff): prev=4, curr=5, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:49 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:49 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:49 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:49 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.54400374531753
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:49 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:49 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:49 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.310
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:49 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:49 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:49 | Reward (бой): damage_term=+0.090 (norm=0.150)
2026-02-03 13:17:49 | Reward (бой): advantage_term=+0.075
2026-02-03 13:17:49 | Reward (бой): damage=0.090 (norm=0.150, dealt=3.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.165
2026-02-03 13:17:49 | Reward (шаг): бой delta=+0.165
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.324555320336759->7.810249675906654
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.160
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.690
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.06225774829855
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.54400374531753->16.278820596099706
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.63014581273465->10.63014581273465
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.486832980505138->9.486832980505138
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.810249675906654->13.92838827718412
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.94427190999916->8.94427190999916
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:50 | Reward (бой): advantage_term=+0.060
2026-02-03 13:17:50 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.060
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.060
2026-02-03 13:17:50 | Конец эпизода 1. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=5.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=1 ep_reward=-0.928000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.211102550927978->12.529964086141668
2026-02-03 13:17:50 | Конец эпизода 2. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=15.0 enemy_hp_total=19.0 model_vp=5 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=2 ep_reward=-0.329500 win=1 vp_diff=5 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:50 | Конец эпизода 3. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=6.0 model_vp=2 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=3 ep_reward=-0.495000 win=1 vp_diff=2 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Конец эпизода 4. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=9.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=4 ep_reward=-0.689500 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:50 | Конец эпизода 5. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=14.0 model_vp=2 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=5 ep_reward=-0.204000 win=1 vp_diff=2 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Конец эпизода 6. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=18.0 model_vp=0 enemy_vp=3 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=6 ep_reward=-1.576000 win=0 vp_diff=-3 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.160
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 1, 3], len=2, bonus=+0.200
2026-02-03 13:17:50 | Конец эпизода 7. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=18.0 model_vp=2 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=7 ep_reward=-0.796000 win=1 vp_diff=2 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Конец эпизода 8. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=8.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=8 ep_reward=-0.647000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.045361017187261->12.041594578792296
2026-02-03 13:17:50 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.324555320336759->6.324555320336759
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MASK][SHOOT] Доступные индексы: 0..1, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.160
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.200 (dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.200, obj_kill=0.000, action=0.000, total=0.440
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.170
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): kill_bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.170, obj_damage=0.050, obj_kill=0.200, action=0.000, total=0.850
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+1.290
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.324555320336759->8.246211251235321
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.602325267042627->9.433981132056603
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 3, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 4, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.310
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:50 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:50 | Reward (бой): advantage_term=+0.105
2026-02-03 13:17:50 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.165
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.165
2026-02-03 13:17:50 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.385164807134504->5.385164807134504
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.708203932499369->9.219544457292887
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.055385138137417->10.295630140987
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:50 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:50 | Reward (бой): taken_penalty=-0.100 (norm=0.200)
2026-02-03 13:17:50 | Reward (бой): advantage_term=+0.075
2026-02-03 13:17:50 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.100 (norm=0.200, taken=4.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.035
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.035
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=5.00, norm=0.250, penalty=-0.125
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:50 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:50 | Reward (бой): advantage_term=+0.015
2026-02-03 13:17:50 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=0.045
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.045
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.385164807134504->10.63014581273465
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.219544457292887->9.219544457292887
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-2.000, proximity=0.000, total=-2.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-1.800
2026-02-03 13:17:50 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:50 | Reward (бой): kill_term=+0.400 (delta=1)
2026-02-03 13:17:50 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:50 | Reward (бой): advantage_term=+0.090
2026-02-03 13:17:50 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.400 (delta=1), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.525
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.525
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.560
2026-02-03 13:17:50 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.219544457292887->9.219544457292887
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.816653826391969->12.649110640673518
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.602325267042627->9.433981132056603
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->14.7648230602334
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.433981132056603->9.433981132056603
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.385164807134504->5.385164807134504
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:50 | Reward (бой): advantage_term=+0.075
2026-02-03 13:17:50 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.075
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.075
2026-02-03 13:17:50 | Конец эпизода 9. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=5.0 model_vp=2 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=9 ep_reward=-0.739500 win=1 vp_diff=2 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | Конец эпизода 10. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=20.0 model_vp=4 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=10 ep_reward=-0.670500 win=1 vp_diff=3 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Конец эпизода 11. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=16.0 model_vp=2 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=11 ep_reward=-0.552500 win=1 vp_diff=2 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.06225774829855
2026-02-03 13:17:50 | Конец эпизода 12. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=1 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=12 ep_reward=-0.224000 win=1 vp_diff=1 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | Конец эпизода 13. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=19.0 model_vp=2 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=13 ep_reward=0.114000 win=1 vp_diff=2 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | Конец эпизода 14. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=17.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=2 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=14 ep_reward=-0.493000 win=0 vp_diff=-2 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.385164807134504->7.0710678118654755
2026-02-03 13:17:50 | Конец эпизода 15. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=2 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=15 ep_reward=-0.717500 win=1 vp_diff=2 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | Конец эпизода 16. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=18.0 enemy_hp_total=12.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=16 ep_reward=-0.857500 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.94427190999916->10.63014581273465
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.416407864998739->14.422205101855956
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.035668847618199->15.231546211727817
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.310
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=2, размер пространства=2.
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=2, delta=2, reward=+0.100, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 2, 2], len=2, bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 2, 1], len=2, bonus=+0.200
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.422205101855956->14.422205101855956
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=15.231546211727817->15.231546211727817
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 3, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.219544457292887->10.63014581273465
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=2, curr=4, delta=2, reward=+0.100, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 3], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-2.000, proximity=1.000, total=-1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-1.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=3, delta=2, reward=+0.100, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 3, 2], len=2, bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.422205101855956->14.422205101855956
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.150 (dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.150, obj_kill=0.000, action=0.000, total=0.360
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.360
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 4, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:50 | Reward (VP diff): prev=4, curr=5, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 4], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (VP diff): prev=3, curr=5, delta=2, reward=+0.100, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 4, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.422205101855956->14.422205101855956
2026-02-03 13:17:50 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (VP diff): prev=5, curr=6, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 5], len=2, bonus=+0.200
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | Reward (VP diff): prev=5, curr=6, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=-1, curr=0, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.082762530298219->6.082762530298219
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.385164807134504->8.246211251235321
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (VP diff): prev=6, curr=7, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 3, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.422205101855956->14.422205101855956
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=-2, curr=-3, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | [PERF] steps=208 updates=0 action_ms=0.792 enemy_turn_ms=1.545 env_step_ms=1.182 replay_sample_ms=0.000 train_fwd_ms=0.000 train_bwd_ms=0.000 log_ms=0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:50 | Reward (VP diff): prev=-1, curr=0, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=7, curr=8, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.422205101855956->17.0
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0->8.0
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=-1.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.324555320336759->10.0
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:50 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:50 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=0.060
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.060
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.600
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.740
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:50 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | Конец эпизода 17. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=5 enemy_vp=2 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=17 ep_reward=-0.263000 win=1 vp_diff=3 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | Конец эпизода 18. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=17.0 model_vp=2 enemy_vp=2 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=18 ep_reward=-0.247500 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:50 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:50 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:50 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=0.035
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.035
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=5.00, norm=0.250, penalty=-0.125
2026-02-03 13:17:50 | Конец эпизода 19. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=15.0 enemy_hp_total=13.0 model_vp=0 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=19 ep_reward=0.173500 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=8, curr=9, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Конец эпизода 20. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=18.0 enemy_hp_total=19.0 model_vp=9 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=20 ep_reward=0.610000 win=1 vp_diff=9 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0710678118654755->7.0710678118654755
2026-02-03 13:17:50 | Конец эпизода 21. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=6 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=21 ep_reward=-0.961500 win=1 vp_diff=6 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (VP diff): prev=3, curr=4, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 3], len=2, bonus=+0.200
2026-02-03 13:17:50 | Конец эпизода 22. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=19.0 model_vp=5 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=22 ep_reward=0.012000 win=1 vp_diff=4 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | Конец эпизода 23. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=18.0 enemy_hp_total=17.0 model_vp=0 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=23 ep_reward=-0.802000 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (VP diff): prev=-3, curr=-2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:50 | Конец эпизода 24. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=20.0 model_vp=1 enemy_vp=3 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=24 ep_reward=-0.966500 win=0 vp_diff=-2 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.656854249492381->5.656854249492381
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0710678118654755->10.63014581273465
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.041594578792296->12.041594578792296
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.0->8.0
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=7.00, norm=0.350, penalty=-0.175
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=6.00, norm=0.300, penalty=-0.150
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=2, размер пространства=2.
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:50 | Reward (бой): damage_term=+0.090 (norm=0.150)
2026-02-03 13:17:50 | Reward (бой): advantage_term=+0.090
2026-02-03 13:17:50 | Reward (бой): damage=0.090 (norm=0.150, dealt=3.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.180
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.180
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.210 (norm=0.350, dealt=7.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.350 (dealt=7.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): kill_bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.210 (norm=0.350, dealt=7.00), kill=0.400, overkill=-0.000, quality=0.120, obj_damage=0.350, obj_kill=0.200, action=0.000, total=1.280
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+1.280
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.150 (dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.150, obj_kill=0.000, action=0.000, total=0.360
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.360
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:50 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.700
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:50 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:50 | Reward (бой): advantage_term=+0.030
2026-02-03 13:17:50 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.060
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.060
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-2.000, proximity=1.000, total=-1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-1.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:50 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:50 | Reward (бой): advantage_term=+0.015
2026-02-03 13:17:50 | Reward (бой/у цели): damage_term=+0.050 (raw=1.00)
2026-02-03 13:17:50 | Reward (объекты, бой): damage=0.050 (raw=1.00), kills=0.000 (count=0)
2026-02-03 13:17:50 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=0.095
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.095
2026-02-03 13:17:50 | Reward (VP diff): prev=-1, curr=0, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=-2, delta=-2, reward=+0.000, penalty=-0.100
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:50 | Reward (VP diff): prev=-2, curr=-3, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.54400374531753->8.54400374531753
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 3, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.570
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.570
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-2.000, proximity=1.000, total=-1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-1.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.240 (norm=0.400, dealt=8.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.240 (norm=0.400, dealt=8.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.690
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.690
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:50 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:50 | Reward (бой): advantage_term=+0.060
2026-02-03 13:17:50 | Reward (бой/у цели): damage_term=+0.050 (raw=1.00)
2026-02-03 13:17:50 | Reward (объекты, бой): damage=0.050 (raw=1.00), kills=0.000 (count=0)
2026-02-03 13:17:50 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.140
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.140
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 1, 3], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (VP diff): prev=-2, curr=-3, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.570
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.570
2026-02-03 13:17:50 | Reward (VP diff): prev=-3, curr=-4, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:50 | Reward (бой): advantage_term=+0.120
2026-02-03 13:17:50 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.120, strength=0.000, objectives=0.000 (delta=0), total=0.120
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.120
2026-02-03 13:17:50 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0710678118654755->9.899494936611665
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=3, delta=2, reward=+0.100, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=-4, curr=-5, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.899494936611665->10.0
2026-02-03 13:17:50 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.560
2026-02-03 13:17:50 | Reward (победа): bonus=+3.000
2026-02-03 13:17:50 | Конец эпизода 25. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=wipeout_enemy winner=model model_hp_total=20.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=0 turn=8 battle_round=8
2026-02-03 13:17:50 | [TRAIN][EP] ep=25 ep_reward=-0.399286 win=1 vp_diff=0 end_reason=wipeout_enemy
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (VP diff): prev=3, curr=4, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 3, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:50 | Reward (VP diff): prev=-5, curr=-6, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.602325267042627->9.433981132056603
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:50 | Reward (VP diff): prev=4, curr=5, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 4, 1], len=2, bonus=+0.200
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0710678118654755->13.038404810405298
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | Reward (VP diff): prev=-3, curr=-2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (VP diff): prev=3, curr=4, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:50 | Reward (VP diff): prev=5, curr=7, delta=2, reward=+0.100, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.038404810405298->13.038404810405298
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:50 | Reward (бой): advantage_term=+0.030
2026-02-03 13:17:50 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.060
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.060
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (VP diff): prev=-2, curr=-1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.600
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.600
2026-02-03 13:17:50 | Reward (победа): bonus=+3.000
2026-02-03 13:17:50 | Конец эпизода 26. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=wipeout_enemy winner=model model_hp_total=20.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=6 turn=10 battle_round=10
2026-02-03 13:17:50 | [TRAIN][EP] ep=26 ep_reward=-0.571667 win=1 vp_diff=-6 end_reason=wipeout_enemy
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.708203932499369->7.810249675906654
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (VP diff): prev=4, curr=5, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Конец эпизода 27. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=8.0 model_vp=5 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=27 ep_reward=-0.567000 win=1 vp_diff=5 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:50 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:50 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:50 | Reward (бой): advantage_term=+0.045
2026-02-03 13:17:50 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.080
2026-02-03 13:17:50 | Reward (шаг): бой delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | Конец эпизода 28. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=17.0 enemy_hp_total=13.0 model_vp=1 enemy_vp=3 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=28 ep_reward=-0.173000 win=0 vp_diff=-2 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:50 | Reward (VP diff): prev=7, curr=8, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 1, 3], len=2, bonus=+0.200
2026-02-03 13:17:50 | Конец эпизода 29. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=16.0 enemy_hp_total=5.0 model_vp=10 enemy_vp=2 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=29 ep_reward=0.359500 win=1 vp_diff=8 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.038404810405298->13.038404810405298
2026-02-03 13:17:50 | Конец эпизода 30. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=3 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=30 ep_reward=0.299500 win=1 vp_diff=3 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | Конец эпизода 31. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=17.0 enemy_hp_total=13.0 model_vp=2 enemy_vp=3 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=31 ep_reward=-0.198500 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | Конец эпизода 32. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:50 | Конец эпизода: reason=unknown winner=None model_hp_total=18.0 enemy_hp_total=20.0 model_vp=1 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:50 | [TRAIN][EP] ep=32 ep_reward=0.132000 win=1 vp_diff=1 end_reason=turn_limit_Only War
2026-02-03 13:17:50 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.06225774829855
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.700
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0710678118654755->9.899494936611665
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.045361017187261->11.045361017187261
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.615773105863909->10.63014581273465
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.06225774829855
2026-02-03 13:17:50 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=2, размер пространства=2.
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.206555615733702->12.806248474865697
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.899494936611665->10.63014581273465
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-2.000, proximity=1.000, total=-1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-1.000
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=-1.300
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.210 (norm=0.350, dealt=7.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.210 (norm=0.350, dealt=7.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.260
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.820
2026-02-03 13:17:50 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.530
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->10.63014581273465
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.63014581273465->10.63014581273465
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 3, 1], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:50 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 3], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.213203435596427->21.213203435596427
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.54400374531753->8.54400374531753
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:50 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.180339887498949->12.806248474865697
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:50 | Reward (VP diff): prev=2, curr=4, delta=2, reward=+0.100, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:50 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 4], len=2, bonus=+0.200
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:50 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.213203435596427->21.213203435596427
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.63014581273465->10.63014581273465
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.806248474865697->12.806248474865697
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:50 | Reward (VP diff): prev=-2, curr=-3, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:50 | Reward (VP diff): prev=4, curr=5, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:50 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:50 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:50 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:50 | Reward (VP diff): prev=3, curr=4, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:50 | Reward (стрик удержания): streaks=[0, 0, 0, 5], len=2, bonus=+0.200
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.213203435596427->22.135943621178654
2026-02-03 13:17:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:50 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.0->10.0
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.120
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.120, strength=0.000, objectives=0.000 (delta=0), total=0.150
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.150
2026-02-03 13:17:51 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=-0.015
2026-02-03 13:17:51 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=-0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.040
2026-02-03 13:17:51 | Reward (шаг): бой delta=-0.040
2026-02-03 13:17:51 | Reward (VP diff): prev=-3, curr=-4, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (VP diff): prev=4, curr=5, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.135943621178654->22.135943621178654
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.219544457292887->10.0
2026-02-03 13:17:51 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=2, размер пространства=2.
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.806248474865697->12.806248474865697
2026-02-03 13:17:51 | Конец эпизода 33. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=33 ep_reward=-0.723000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.015
2026-02-03 13:17:51 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=0.075
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.075
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | Reward (VP diff): prev=5, curr=6, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=-0.030
2026-02-03 13:17:51 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=-0.030, strength=0.000, objectives=0.000 (delta=0), total=0.005
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.005
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0->9.219544457292887
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.135943621178654->22.135943621178654
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): kill_term=+0.400 (delta=1)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.135
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.400 (delta=1), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.135, strength=0.000, objectives=0.000 (delta=0), total=0.565
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.565
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.615773105863909->10.63014581273465
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.130
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.130
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.060
2026-02-03 13:17:51 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.070
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.070
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.030
2026-02-03 13:17:51 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.090
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.090
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.082762530298219->8.06225774829855
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.02379604162864->21.02379604162864
2026-02-03 13:17:51 | Конец эпизода 34. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=34 ep_reward=-0.771000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:51 | Конец эпизода 35. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=3.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=35 ep_reward=-0.653000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.54400374531753->8.94427190999916
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Конец эпизода 36. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=9.0 model_vp=0 enemy_vp=4 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=36 ep_reward=0.135500 win=0 vp_diff=-4 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): kill_term=+0.400 (delta=1)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.135
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.400 (delta=1), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.135, strength=0.000, objectives=0.000 (delta=0), total=0.565
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.565
2026-02-03 13:17:51 | Конец эпизода 37. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=6 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=37 ep_reward=0.032500 win=1 vp_diff=6 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | Конец эпизода 38. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=12.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=38 ep_reward=-0.787500 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.06225774829855
2026-02-03 13:17:51 | Конец эпизода 39. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=5 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=39 ep_reward=-0.486500 win=1 vp_diff=5 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.280109889280518->10.63014581273465
2026-02-03 13:17:51 | Конец эпизода 40. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=20.0 model_vp=1 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=40 ep_reward=0.054000 win=1 vp_diff=1 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.433981132056603->11.313708498984761
2026-02-03 13:17:51 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.94427190999916->8.94427190999916
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.280109889280518->8.246211251235321
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=15.0->15.0
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:51 | [PERF] steps=200 updates=0 action_ms=0.239 enemy_turn_ms=1.696 env_step_ms=1.162 replay_sample_ms=0.000 train_fwd_ms=0.000 train_bwd_ms=0.000 log_ms=0.074
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:51 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=2, размер пространства=2.
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.94427190999916
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.035668847618199->14.317821063276353
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=15.0->16.15549442140351
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.94427190999916->8.94427190999916
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.317821063276353->16.1245154965971
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.94427190999916->8.94427190999916
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.030
2026-02-03 13:17:51 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.030
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.030
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=5.00, norm=0.250, penalty=-0.125
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.125 (norm=0.250)
2026-02-03 13:17:51 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.125 (norm=0.250, taken=5.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=-0.065
2026-02-03 13:17:51 | Reward (шаг): бой delta=-0.065
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.94427190999916->8.94427190999916
2026-02-03 13:17:51 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.1245154965971->16.1245154965971
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->11.313708498984761
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.4031242374328485->9.433981132056603
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=-0.500
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0710678118654755->9.899494936611665
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (VP diff): prev=-2, curr=-3, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.045
2026-02-03 13:17:51 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.105
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.105
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | [MASK][SHOOT] Доступные индексы: 0..1, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Конец эпизода 41. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=15.0 enemy_hp_total=15.0 model_vp=0 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=41 ep_reward=-0.732000 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.160
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.433981132056603->11.313708498984761
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.160
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.200
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.060
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.065
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.065
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->10.63014581273465
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.0990195135927845->6.324555320336759
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.045361017187261->13.601470508735444
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.200
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.060
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.065
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.065
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:51 | Reward (VP diff): prev=-3, curr=-2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Конец эпизода 42. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=19.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=42 ep_reward=-1.584000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.200
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.075
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.105
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.105
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Конец эпизода 43. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=17.0 enemy_hp_total=17.0 model_vp=0 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=43 ep_reward=-0.338000 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | Reward (стрик удержания): streaks=[0, 0, 1, 3], len=2, bonus=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:51 | Конец эпизода 44. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=18.0 enemy_hp_total=15.0 model_vp=1 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=44 ep_reward=-0.251000 win=1 vp_diff=1 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.656854249492381->8.94427190999916
2026-02-03 13:17:51 | Конец эпизода 45. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=17.0 enemy_hp_total=20.0 model_vp=1 enemy_vp=3 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=45 ep_reward=0.055000 win=0 vp_diff=-2 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | Конец эпизода 46. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=14.0 enemy_hp_total=19.0 model_vp=3 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=46 ep_reward=-0.096000 win=1 vp_diff=3 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:51 | Конец эпизода 47. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=18.0 enemy_hp_total=15.0 model_vp=1 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=47 ep_reward=-0.366500 win=1 vp_diff=1 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-2.000, proximity=0.000, total=-2.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-1.800
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.075
2026-02-03 13:17:51 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.110
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.110
2026-02-03 13:17:51 | Конец эпизода 48. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=13.0 model_vp=1 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=48 ep_reward=-0.353500 win=1 vp_diff=1 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=17.0->18.788294228055936
2026-02-03 13:17:51 | Reward (VP diff): prev=2, curr=4, delta=2, reward=+0.100, penalty=-0.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.0->10.0
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=-2, delta=-2, reward=+0.000, penalty=-0.100
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.788294228055936->21.540659228538015
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.082762530298219->8.06225774829855
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.385164807134504->8.246211251235321
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=-1.300
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.540659228538015->21.540659228538015
2026-02-03 13:17:51 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=2, размер пространства=2.
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.06225774829855
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.150 (dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.150, obj_kill=0.000, action=0.000, total=0.360
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.360
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.060
2026-02-03 13:17:51 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.120
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.120
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.310
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.560
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.045
2026-02-03 13:17:51 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.080
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=-0.500
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.94427190999916->10.0
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.310
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:51 | Reward (VP diff): prev=3, curr=4, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0710678118654755->9.219544457292887
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.670
2026-02-03 13:17:51 | Reward (VP diff): prev=-2, curr=-3, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->10.0
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-2.000, proximity=1.000, total=-1.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-1.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.130
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.270
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.120
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.120, strength=0.000, objectives=0.000 (delta=0), total=0.150
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.150
2026-02-03 13:17:51 | Reward (VP diff): prev=-1, curr=1, delta=2, reward=+0.100, penalty=-0.000
2026-02-03 13:17:51 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.045361017187261->12.529964086141668
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.670
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.219544457292887->9.219544457292887
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.0->10.0
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Конец эпизода 49. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=17.0 model_vp=4 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=49 ep_reward=-0.367500 win=1 vp_diff=4 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | Reward (стрик удержания): streaks=[0, 0, 3, 0], len=2, bonus=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=-0.020
2026-02-03 13:17:51 | Reward (шаг): бой delta=-0.020
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.075
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.105
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.105
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.8806130178211->20.8806130178211
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.370
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.135
2026-02-03 13:17:51 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.135, strength=0.000, objectives=0.000 (delta=0), total=0.135
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.135
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=-0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.219544457292887->10.0
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): kill_term=+0.400 (delta=1)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.120
2026-02-03 13:17:51 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.400 (delta=1), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.120, strength=0.000, objectives=0.000 (delta=0), total=0.580
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.580
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.530
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=-0.025
2026-02-03 13:17:51 | Reward (шаг): бой delta=-0.025
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Конец эпизода 50. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=14.0 enemy_hp_total=16.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=50 ep_reward=-0.353500 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [SELFPLAY] opponent snapshot updated at episode 50
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.317821063276353->14.317821063276353
2026-02-03 13:17:51 | Конец эпизода 51. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=3 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=51 ep_reward=-1.664000 win=0 vp_diff=-3 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Конец эпизода 52. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=4 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=52 ep_reward=-0.179000 win=1 vp_diff=3 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Конец эпизода 53. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=18.0 enemy_hp_total=18.0 model_vp=4 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=53 ep_reward=-0.324000 win=1 vp_diff=4 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Конец эпизода 54. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=18.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=2 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=54 ep_reward=-0.675500 win=0 vp_diff=-2 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.280109889280518->8.246211251235321
2026-02-03 13:17:51 | Конец эпизода 55. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=17.0 enemy_hp_total=7.0 model_vp=1 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=55 ep_reward=-0.431000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.830951894845301->8.54400374531753
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.670
2026-02-03 13:17:51 | Конец эпизода 56. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=56 ep_reward=-1.031500 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.830951894845301->9.433981132056603
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.615773105863909->11.40175425099138
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.324555320336759->6.324555320336759
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.165525060596439->13.416407864998739
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.0->10.0
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.433981132056603->10.0
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): kill_term=+0.400 (delta=1)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.120
2026-02-03 13:17:51 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.400 (delta=1), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.120, strength=0.000, objectives=0.000 (delta=0), total=0.580
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.580
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.40175425099138->13.038404810405298
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.324555320336759->8.246211251235321
2026-02-03 13:17:51 | [MASK][SHOOT] Доступные индексы: 0..1, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.0->10.0
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.602325267042627->8.602325267042627
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.433981132056603->9.433981132056603
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.0->13.892443989449804
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.602325267042627->10.63014581273465
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.041594578792296->12.041594578792296
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.150 (dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.150, obj_kill=0.000, action=0.000, total=0.360
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.640
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.090
2026-02-03 13:17:51 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.040
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.040
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:51 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=-0.020
2026-02-03 13:17:51 | Reward (шаг): бой delta=-0.020
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.160
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=-0.045
2026-02-03 13:17:51 | Reward (бой/у цели): damage_term=+0.050 (raw=1.00)
2026-02-03 13:17:51 | Reward (объекты, бой): damage=0.050 (raw=1.00), kills=0.000 (count=0)
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=-0.045, strength=0.000, objectives=0.000 (delta=0), total=0.035
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.035
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.210 (norm=0.350, dealt=7.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.210 (norm=0.350, dealt=7.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.260
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.260
2026-02-03 13:17:51 | Reward (VP diff): prev=1, curr=0, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (VP diff): prev=-1, curr=0, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.560
2026-02-03 13:17:51 | [PERF] steps=200 updates=0 action_ms=0.228 enemy_turn_ms=1.613 env_step_ms=1.218 replay_sample_ms=0.000 train_fwd_ms=0.000 train_bwd_ms=0.000 log_ms=0.053
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.615773105863909->8.54400374531753
2026-02-03 13:17:51 | Конец эпизода 57. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=17.0 enemy_hp_total=18.0 model_vp=1 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=57 ep_reward=0.037000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.54400374531753->12.36931687685298
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.075
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.080
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.080
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): advantage_term=-0.030
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.030, strength=0.000, objectives=0.000 (delta=0), total=-0.050
2026-02-03 13:17:51 | Reward (шаг): бой delta=-0.050
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.160
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | [MASK][SHOOT] Доступные индексы: 0..1, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.045
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.050
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.050
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.041594578792296->14.422205101855956
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=-0.020
2026-02-03 13:17:51 | Reward (шаг): бой delta=-0.020
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Конец эпизода 58. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=17.0 model_vp=1 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=58 ep_reward=-0.746500 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.045
2026-02-03 13:17:51 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.020
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.020
2026-02-03 13:17:51 | Конец эпизода 59. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=17.0 enemy_hp_total=13.0 model_vp=0 enemy_vp=2 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=59 ep_reward=-1.123000 win=0 vp_diff=-2 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-2.000, proximity=0.000, total=-2.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-1.800
2026-02-03 13:17:51 | Reward (бой): damage_term=+0.090 (norm=0.150)
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.030
2026-02-03 13:17:51 | Reward (бой): damage=0.090 (norm=0.150, dealt=3.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.095
2026-02-03 13:17:51 | Reward (шаг): бой delta=+0.095
2026-02-03 13:17:51 | Конец эпизода 60. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=17.0 enemy_hp_total=13.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=60 ep_reward=-0.432000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.422205101855956->20.615528128088304
2026-02-03 13:17:51 | Конец эпизода 61. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=61 ep_reward=-0.362000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | Конец эпизода 62. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=9.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=62 ep_reward=0.122000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Конец эпизода 63. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=16.0 enemy_hp_total=14.0 model_vp=2 enemy_vp=3 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=63 ep_reward=0.014000 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.082762530298219->6.082762530298219
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.160
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Конец эпизода 64. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:51 | Конец эпизода: reason=unknown winner=None model_hp_total=18.0 enemy_hp_total=4.0 model_vp=1 enemy_vp=2 turn=11 battle_round=11
2026-02-03 13:17:51 | [TRAIN][EP] ep=64 ep_reward=-1.338000 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-03 13:17:51 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.340
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:51 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:51 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-03 13:17:51 | Reward (бой): advantage_term=+0.015
2026-02-03 13:17:51 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.035
2026-02-03 13:17:51 | Reward (шаг): бой delta=-0.035
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.341664064126334->13.341664064126334
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.082762530298219->10.816653826391969
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.4031242374328485->8.94427190999916
2026-02-03 13:17:51 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=2, размер пространства=2.
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->9.433981132056603
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.94427190999916->8.94427190999916
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:51 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:51 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:51 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:51 | Reward (стрик удержания): streaks=[0, 0, 0, 3], len=2, bonus=+0.200
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.150 (dealt=3.00)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.150, obj_kill=0.000, action=0.000, total=0.360
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.360
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.341664064126334->13.92838827718412
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:51 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:51 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:51 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:51 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:51 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.94427190999916->8.94427190999916
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.150 (dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.150, obj_kill=0.000, action=0.000, total=0.360
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.360
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:52 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.600
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.600
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:52 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 0, 4], len=2, bonus=+0.200
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.280109889280518->9.899494936611665
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.92838827718412->17.029386365926403
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.830951894845301->5.830951894845301
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:52 | Reward (VP diff): prev=3, curr=4, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 0, 5], len=2, bonus=+0.200
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:52 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.0->13.416407864998739
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->8.246211251235321
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (VP diff): prev=4, curr=5, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.899494936611665->10.63014581273465
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.341664064126334->14.7648230602334
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.416407864998739->13.416407864998739
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.090
2026-02-03 13:17:52 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.150
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.150
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (VP diff): prev=3, curr=4, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:52 | Конец эпизода 65. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=13.0 enemy_hp_total=16.0 model_vp=4 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=65 ep_reward=-0.289000 win=1 vp_diff=4 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.830951894845301->11.40175425099138
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.280109889280518->10.63014581273465
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | Reward (VP diff): prev=-2, curr=0, delta=2, reward=+0.100, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->10.0
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.060
2026-02-03 13:17:52 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.120
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.120
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.63014581273465->10.63014581273465
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.0->10.0
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.899494936611665->9.899494936611665
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.63014581273465->10.63014581273465
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.165525060596439->18.027756377319946
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:52 | Конец эпизода 66. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=14.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=66 ep_reward=-1.179500 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:52 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Конец эпизода 67. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=20.0 model_vp=3 enemy_vp=2 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=67 ep_reward=-0.153000 win=1 vp_diff=1 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | Конец эпизода 68. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=15.0 enemy_hp_total=8.0 model_vp=2 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=68 ep_reward=-0.530000 win=1 vp_diff=2 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | Конец эпизода 69. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=15.0 model_vp=5 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=69 ep_reward=-0.398000 win=1 vp_diff=5 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.370
2026-02-03 13:17:52 | Конец эпизода 70. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=11.0 model_vp=0 enemy_vp=2 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=70 ep_reward=-1.110000 win=0 vp_diff=-2 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:52 | Конец эпизода 71. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=17.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=71 ep_reward=-0.407500 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.590
2026-02-03 13:17:52 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 3, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | Конец эпизода 72. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=3 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=72 ep_reward=-0.674500 win=1 vp_diff=3 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.246211251235321->10.0
2026-02-03 13:17:52 | [MASK][SHOOT] Доступные индексы: 0..1, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.045
2026-02-03 13:17:52 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.075
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.075
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=-1.300
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.486832980505138->11.661903789690601
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.649110640673518->14.560219778561036
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.770329614269007->10.770329614269007
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=2, размер пространства=2.
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=-0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.324555320336759->7.810249675906654
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.560219778561036->16.1245154965971
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.806248474865697->12.806248474865697
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.770329614269007->12.806248474865697
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:52 | [MASK][SHOOT] Доступные индексы: 0..1, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.180 (norm=0.300, dealt=6.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.300, dealt=6.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.230
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.130
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.360
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:52 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=0.030
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.030
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=5.00, norm=0.250, penalty=-0.125
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.324555320336759->6.324555320336759
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:52 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:52 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=-0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.590
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.160
2026-02-03 13:17:52 | Reward (VP diff): prev=1, curr=0, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.180 (norm=0.300, dealt=6.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.300, dealt=6.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.230
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.230
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:52 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.060
2026-02-03 13:17:52 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.065
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.065
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.324555320336759->7.280109889280518
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.370
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.54400374531753->9.486832980505138
2026-02-03 13:17:52 | [MASK][SHOOT] Доступные индексы: 0..1, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.200 (dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.200, obj_kill=0.000, action=0.000, total=0.440
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.440
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.848857801796104->12.041594578792296
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.280109889280518->9.219544457292887
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:52 | Reward (VP diff): prev=-2, curr=-3, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): damage_term=+0.090 (norm=0.150)
2026-02-03 13:17:52 | Reward (бой): kill_term=+0.400 (delta=1)
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.090
2026-02-03 13:17:52 | Reward (бой): damage=0.090 (norm=0.150, dealt=3.00), kills=0.400 (delta=1), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.580
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.580
2026-02-03 13:17:52 | Reward (победа): bonus=+3.000
2026-02-03 13:17:52 | Конец эпизода 73. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=wipeout_enemy winner=model model_hp_total=19.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=0 turn=10 battle_round=10
2026-02-03 13:17:52 | [TRAIN][EP] ep=73 ep_reward=0.433333 win=1 vp_diff=0 end_reason=wipeout_enemy
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=5.00, norm=0.250, penalty=-0.125
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.219544457292887->10.0
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.54400374531753->8.54400374531753
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.310
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-1.000
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0710678118654755->9.219544457292887
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.54400374531753->8.54400374531753
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.670
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.06225774829855
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.54400374531753->8.54400374531753
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.0990195135927845->7.810249675906654
2026-02-03 13:17:52 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.041594578792296->12.041594578792296
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (VP diff): prev=-2, curr=-1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.041594578792296->13.601470508735444
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->17.029386365926403
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Конец эпизода 74. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=16.0 model_vp=0 enemy_vp=3 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=74 ep_reward=-0.773500 win=0 vp_diff=-3 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:52 | Конец эпизода 75. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=20.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=75 ep_reward=-0.067500 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Конец эпизода 76. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=18.0 enemy_hp_total=20.0 model_vp=3 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=76 ep_reward=0.105500 win=1 vp_diff=2 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:52 | Reward (VP diff): prev=-1, curr=0, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 3, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | Конец эпизода 77. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=15.0 model_vp=2 enemy_vp=2 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=77 ep_reward=-0.822000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.601470508735444->13.601470508735444
2026-02-03 13:17:52 | Конец эпизода 78. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=78 ep_reward=-1.196000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=17.029386365926403->17.029386365926403
2026-02-03 13:17:52 | Конец эпизода 79. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=20.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=79 ep_reward=-0.835000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.54400374531753->8.54400374531753
2026-02-03 13:17:52 | Конец эпизода 80. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=17.0 model_vp=1 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=80 ep_reward=-0.807500 win=1 vp_diff=1 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.180339887498949->11.40175425099138
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.090
2026-02-03 13:17:52 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.120
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.120
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0->14.0
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.180339887498949->14.142135623730951
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.433981132056603->11.661903789690601
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.041594578792296->14.422205101855956
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [PERF] steps=200 updates=0 action_ms=0.232 enemy_turn_ms=1.600 env_step_ms=1.162 replay_sample_ms=0.000 train_fwd_ms=0.000 train_bwd_ms=0.000 log_ms=0.076
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.40175425099138->13.601470508735444
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.0->14.0
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0710678118654755->15.033296378372908
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.150 (dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.150, obj_kill=0.000, action=0.000, total=0.360
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.360
2026-02-03 13:17:52 | [MASK][SHOOT] Доступные индексы: 0..1, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.310
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.105
2026-02-03 13:17:52 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.055
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.055
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.0->14.317821063276353
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.280109889280518->9.219544457292887
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.433981132056603->11.313708498984761
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=15.033296378372908->21.02379604162864
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.590
2026-02-03 13:17:52 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.0->10.0
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.150 (dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.150, obj_kill=0.000, action=0.000, total=0.360
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.440
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.317821063276353->16.1245154965971
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:52 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.313708498984761->13.601470508735444
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.324555320336759->10.0
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.150 (dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.150, obj_kill=0.000, action=0.000, total=0.360
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.360
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.180 (norm=0.300, dealt=6.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.300, dealt=6.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.230
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.230
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.1245154965971->16.1245154965971
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (VP diff): prev=-2, curr=-3, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.213203435596427->22.47220505424423
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.530
2026-02-03 13:17:52 | Reward (победа): bonus=+3.000
2026-02-03 13:17:52 | Конец эпизода 81. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=wipeout_enemy winner=model model_hp_total=19.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=2 turn=7 battle_round=7
2026-02-03 13:17:52 | [TRAIN][EP] ep=81 ep_reward=0.743333 win=1 vp_diff=-2 end_reason=wipeout_enemy
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Конец эпизода 82. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=18.0 enemy_hp_total=13.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=82 ep_reward=-0.169000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.810249675906654->9.433981132056603
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:52 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.060
2026-02-03 13:17:52 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.070
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.070
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:52 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-03 13:17:52 | Reward (бой): advantage_term=-0.045
2026-02-03 13:17:52 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.045, strength=0.000, objectives=0.000 (delta=0), total=-0.065
2026-02-03 13:17:52 | Reward (шаг): бой delta=-0.065
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.0->11.313708498984761
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | [MASK][SHOOT] Доступные индексы: 0..1, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.700
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:52 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.090
2026-02-03 13:17:52 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.120
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.120
2026-02-03 13:17:52 | Reward (VP diff): prev=-3, curr=-2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.219544457292887->10.0
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.313708498984761->11.313708498984761
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:52 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.090
2026-02-03 13:17:52 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.125
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.125
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.160
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (VP diff): prev=-2, curr=-1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 3, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.310
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.420
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.280109889280518->8.06225774829855
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.730
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:52 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.075
2026-02-03 13:17:52 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.085
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.085
2026-02-03 13:17:52 | Reward (VP diff): prev=-1, curr=0, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 4, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Конец эпизода 83. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=18.0 enemy_hp_total=19.0 model_vp=0 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=83 ep_reward=-0.849000 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:52 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Конец эпизода 84. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=15.0 model_vp=0 enemy_vp=2 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=84 ep_reward=-1.050500 win=0 vp_diff=-2 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | Конец эпизода 85. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=19.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=85 ep_reward=-1.172500 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=-0.500
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Конец эпизода 86. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=4.0 model_vp=4 enemy_vp=3 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=86 ep_reward=0.092500 win=1 vp_diff=1 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:52 | Конец эпизода 87. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=17.0 enemy_hp_total=19.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=87 ep_reward=-0.413500 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.615773105863909->8.06225774829855
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:52 | Конец эпизода 88. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=13.0 model_vp=0 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=88 ep_reward=-0.735500 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.0990195135927845->7.0710678118654755
2026-02-03 13:17:52 | Reward (VP diff): prev=-1, curr=0, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.54400374531753->8.54400374531753
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.0->8.0
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.04987562112089->10.04987562112089
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=5.00, norm=0.250, penalty=-0.125
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0710678118654755->9.219544457292887
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.0->8.0
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.04987562112089->10.04987562112089
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:52 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:52 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=0.035
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.035
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.220
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (VP diff): prev=-1, curr=0, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.04987562112089->11.661903789690601
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=1)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.310
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.830951894845301->6.4031242374328485
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:52 | Reward (VP diff): prev=1, curr=0, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=1)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 2, 0, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (VP diff): prev=1, curr=0, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.530
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.615773105863909->10.63014581273465
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=1)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 3, 0, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | Конец эпизода 89. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=20.0 model_vp=3 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=89 ep_reward=-0.139000 win=1 vp_diff=3 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.700
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | Конец эпизода 90. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=2 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=90 ep_reward=-0.456500 win=1 vp_diff=1 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.0->12.206555615733702
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.090
2026-02-03 13:17:52 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.040
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.040
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->10.63014581273465
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.63014581273465->10.63014581273465
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 3, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.280
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=2, размер пространства=2.
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.0->10.0
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.105
2026-02-03 13:17:52 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.105
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.105
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:52 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 4, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.211102550927978->10.0
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.280109889280518->8.246211251235321
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.0->10.0
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.130
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.690
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=1.000, total=1.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=+1.000
2026-02-03 13:17:52 | Reward (VP diff): prev=3, curr=4, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 5, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | Конец эпизода 91. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=91 ep_reward=-0.368000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.340
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:52 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:52 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:52 | Reward (бой): advantage_term=+0.075
2026-02-03 13:17:52 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.050
2026-02-03 13:17:52 | Reward (шаг): бой delta=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-03 13:17:52 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 3, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=2, размер пространства=2.
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.180 (norm=0.300, dealt=6.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.300 (dealt=6.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.300, dealt=6.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.300, obj_kill=0.000, action=0.000, total=0.600
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.600
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:52 | Конец эпизода 92. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=17.0 model_vp=2 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=92 ep_reward=0.106500 win=1 vp_diff=2 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.0->12.206555615733702
2026-02-03 13:17:52 | Конец эпизода 93. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=20.0 model_vp=2 enemy_vp=3 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=93 ep_reward=-1.402000 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | Конец эпизода 94. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=10.0 model_vp=2 enemy_vp=3 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=94 ep_reward=-0.526500 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-2.000, proximity=1.000, total=-1.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-1.000
2026-02-03 13:17:52 | Reward (VP diff): prev=4, curr=5, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | Reward (стрик удержания): streaks=[0, 0, 6, 0], len=2, bonus=+0.200
2026-02-03 13:17:52 | Конец эпизода 95. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=20.0 model_vp=5 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=95 ep_reward=-0.040000 win=1 vp_diff=5 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:52 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.816653826391969->10.816653826391969
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:52 | Конец эпизода 96. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:52 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=11.0 model_vp=1 enemy_vp=1 turn=11 battle_round=11
2026-02-03 13:17:52 | [TRAIN][EP] ep=96 ep_reward=-0.234000 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:52 | Reward (VP diff): prev=2, curr=3, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (VP diff): prev=-1, curr=-3, delta=-2, reward=+0.000, penalty=-0.100
2026-02-03 13:17:52 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.433981132056603->10.63014581273465
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:52 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:52 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:52 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:52 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:53 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:53 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:53 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-03 13:17:53 | Reward (бой): advantage_term=+0.105
2026-02-03 13:17:53 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.135
2026-02-03 13:17:53 | Reward (шаг): бой delta=+0.135
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.63014581273465->10.63014581273465
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:53 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:53 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:53 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:53 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.082762530298219->8.06225774829855
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.219544457292887->10.816653826391969
2026-02-03 13:17:53 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.94427190999916
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:53 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:53 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:53 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.385164807134504->8.246211251235321
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:53 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=1, размер пространства=2.
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:53 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:53 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.190
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:53 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.615773105863909->9.433981132056603
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.041594578792296->12.041594578792296
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=3)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:53 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.390
2026-02-03 13:17:53 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:53 | Reward (стрик удержания): streaks=[0, 0, 0, 2], len=2, bonus=+0.200
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:53 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.200
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:53 | [MASK][SHOOT] Доступные индексы: 0..0, юнитов с целями=2, размер пространства=2.
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.433981132056603->9.433981132056603
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:53 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.160
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:53 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:53 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:53 | Reward (VP diff): prev=1, curr=0, delta=-1, reward=+0.000, penalty=-0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.486832980505138->12.727922061357855
2026-02-03 13:17:53 | Конец эпизода 97. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:53 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=20.0 model_vp=3 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:53 | [TRAIN][EP] ep=97 ep_reward=0.262000 win=1 vp_diff=3 end_reason=turn_limit_Only War
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.433981132056603->10.0
2026-02-03 13:17:53 | Конец эпизода 98. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:53 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=14.0 model_vp=0 enemy_vp=3 turn=11 battle_round=11
2026-02-03 13:17:53 | [TRAIN][EP] ep=98 ep_reward=-0.645500 win=0 vp_diff=-3 end_reason=turn_limit_Only War
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:53 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:53 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:53 | Reward (бой): advantage_term=+0.090
2026-02-03 13:17:53 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.065
2026-02-03 13:17:53 | Reward (шаг): бой delta=+0.065
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:53 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:53 | [PERF] steps=200 updates=0 action_ms=0.223 enemy_turn_ms=1.668 env_step_ms=1.197 replay_sample_ms=0.000 train_fwd_ms=0.000 train_bwd_ms=0.000 log_ms=0.059
2026-02-03 13:17:53 | [MASK][SHOOT] Нет доступных целей для стрельбы (маска не применяется).
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:53 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.110
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:53 | [MASK][SHOOT] Доступные индексы: 0..1, юнитов с целями=2, размер пространства=2.
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:53 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.830951894845301->5.830951894845301
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.0->10.63014581273465
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.06225774829855
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:53 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.570
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.570
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:53 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:53 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=0.000
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.500
2026-02-03 13:17:53 | Reward (шаг): чардж delta=-0.500
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0710678118654755->7.280109889280518
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.615773105863909->9.219544457292887
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:53 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.250
2026-02-03 13:17:53 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-03 13:17:53 | Reward (стрик удержания): streaks=[0, 0, 2, 0], len=2, bonus=+0.200
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.830951894845301->8.602325267042627
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.63014581273465->17.0
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.06225774829855
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:53 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:53 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:53 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-03 13:17:53 | Reward (бой): advantage_term=+0.030
2026-02-03 13:17:53 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.065
2026-02-03 13:17:53 | Reward (шаг): бой delta=+0.065
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=-4.000, proximity=0.000, total=-4.000
2026-02-03 13:17:53 | Reward (шаг): движение delta=-4.000
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.219544457292887->10.63014581273465
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.0710678118654755->9.433981132056603
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-03 13:17:53 | Reward (шаг): движение delta=+0.500
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.06225774829855->8.06225774829855
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.650
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=-0.650
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:53 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:53 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-03 13:17:53 | Reward (бой): advantage_term=+0.030
2026-02-03 13:17:53 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.090
2026-02-03 13:17:53 | Reward (шаг): бой delta=+0.090
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.170
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-03 13:17:53 | Reward (шаг): чардж delta=+0.500
2026-02-03 13:17:53 | Reward (бой): advantage_term=+0.120
2026-02-03 13:17:53 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.120, strength=0.000, objectives=0.000 (delta=0), total=0.120
2026-02-03 13:17:53 | Reward (шаг): бой delta=+0.120
2026-02-03 13:17:53 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=10.63014581273465->10.63014581273465
2026-02-03 13:17:53 | Конец эпизода 99. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:53 | Конец эпизода: reason=unknown winner=None model_hp_total=20.0 enemy_hp_total=20.0 model_vp=1 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:53 | [TRAIN][EP] ep=99 ep_reward=-0.353500 win=1 vp_diff=1 end_reason=turn_limit_Only War
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.140
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=0)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=1)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=2)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.500 (obj=3)
2026-02-03 13:17:53 | Reward (VP/объекты, движение): hold=-3.000, proximity=0.500, total=-2.500
2026-02-03 13:17:53 | Reward (шаг): движение delta=-2.500
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.150 (dealt=3.00)
2026-02-03 13:17:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.150, obj_kill=0.000, action=0.000, total=0.360
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, total=0.200
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.560
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-03 13:17:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-03 13:17:53 | Reward (шаг): стрельба delta=+0.080
2026-02-03 13:17:53 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-03 13:17:53 | Конец эпизода 100. [SELFPLAY] enabled=1 mode=snapshot update_every=50 opp_eps=0.0
2026-02-03 13:17:53 | Конец эпизода: reason=unknown winner=None model_hp_total=19.0 enemy_hp_total=19.0 model_vp=0 enemy_vp=0 turn=11 battle_round=11
2026-02-03 13:17:53 | [TRAIN][EP] ep=100 ep_reward=-0.830500 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-03 13:17:53 | [SELFPLAY] opponent snapshot updated at episode 100
2026-02-03 13:18:07 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-02-03 13:18:07 | [VIEWER] Фоллбэк-рендер не активирован.
2026-02-03 13:18:08 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-49-680678.pickle
2026-02-03 13:18:08 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-49-680678.pth
2026-02-03 13:18:16 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-02-03 13:18:16 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-02-03 13:18:16 | [DEPLOY] Order: model first, alternating
2026-02-03 13:18:16 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (6,0)
2026-02-03 13:18:16 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (29,36)
2026-02-03 13:18:16 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (47,5)
2026-02-03 13:18:16 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (46,33)
2026-02-03 13:18:16 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-02-03 13:18:16 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-02-03 13:18:16 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-02-03 13:18:16 | {'model health': [10, 10], 'player health': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-02-03 13:18:16 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-02-03 13:18:18 | === БОЕВОЙ РАУНД 1 ===
2026-02-03 13:18:18 | --- ХОД PLAYER ---
2026-02-03 13:18:18 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-03 13:18:18 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0
2026-02-03 13:18:18 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-03 13:18:26 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-03 13:18:26 | --- ФАЗА ЧАРДЖА ---
2026-02-03 13:18:26 | Нет доступных целей для чарджа.
2026-02-03 13:18:26 | --- ФАЗА БОЯ ---
2026-02-03 13:18:26 | --- ХОД MODEL ---
2026-02-03 13:18:26 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-03 13:18:26 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-02-03 13:18:26 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0
2026-02-03 13:18:26 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-03 13:18:26 | --- ФАЗА ДВИЖЕНИЯ ---
2026-02-03 13:18:26 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (6, 0). Выбор: right, advance=да, бросок=4, макс=9, distance=6
2026-02-03 13:18:26 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (6, 6)
2026-02-03 13:18:26 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-02-03 13:18:26 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (47, 5). Выбор: right, advance=да, бросок=6, макс=11, distance=11
2026-02-03 13:18:26 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (47, 16)
2026-02-03 13:18:26 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-02-03 13:18:44 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.486832980505138->12.041594578792296
2026-02-03 13:18:44 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-03 13:18:44 | --- ФАЗА СТРЕЛЬБЫ ---
2026-02-03 13:18:44 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-02-03 13:18:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-02-03 13:18:44 | --- ФАЗА ЧАРДЖА ---
2026-02-03 13:18:44 | --- ФАЗА ЧАРДЖА ---
2026-02-03 13:18:44 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-02-03 13:18:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-02-03 13:18:44 | [MODEL] Чардж: нет доступных целей
2026-02-03 13:18:44 | --- ФАЗА БОЯ ---
2026-02-03 13:18:44 | --- ФАЗА БОЯ ---
2026-02-03 13:18:44 | [MODEL] Ближний бой: нет доступных атак
2026-02-03 13:18:44 | Reward (idle вне цели): penalty=-0.050, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.486832980505138->12.041594578792296
2026-02-03 13:18:44 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-02-03 13:18:44 | Итерация 0 завершена с наградой tensor([-0.0500], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-02-03 13:18:44 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-02-03 13:18:44 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

