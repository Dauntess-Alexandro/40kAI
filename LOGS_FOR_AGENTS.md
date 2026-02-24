2026-02-24 15:31:21 | [TRAIN][START] DoubleDQN=1 Dueling=1 PER=1 N_STEP=3 LR=0.0001 clip_reward=on[-1.000,1.000] grad_clip=100.0 NUM_ENVS=12 UPDATES_PER_STEP=6 update_ratio=0.500 WARMUP_STEPS=5000 BATCH_ACT=1 USE_AMP=1 USE_COMPILE=1 USE_SUBPROC_ENVS=1 PREFETCH=1 PIN_MEMORY=1 LOG_EVERY=500 SAVE_EVERY=500
2026-02-24 15:31:44 | Старт обучения: USE_SUBPROC_ENVS=1, начальные HP недоступны из subprocess env.
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=24.759, d_after=24.759, d_best=13.759, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=28.284271247461902->30.265491900843113
=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.20360331117452->23.08679276123039
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | Reward (progress к objective): d_before=24.839, d_after=18.358, delta=6.482, norm=1.080, bonus=+0.032
2026-02-24 15:31:45 | Reward (progress к objective): d_before=25.554, d_after=17.692, delta=7.862, norm=1.310, bonus=+0.039
 kills=0, moved_closer=0, min_dist=19.4164878389476->24.839484696748443
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=19.697715603592208->20.591260281974
4
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.313000567495326->30.463092423455635
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.35755975068582->21.93171219946131
2026-02-24 15:31:45 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.186773244895647->24.186773244895647, hold_penalty_events=2
2026-02-24 15:31:45 | Reward (progress к objective): d_before=24.839, d_after=21.954, delta=2.885, norm=0.481, bonus=+0.014
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=17.720, d_after=17.720, d_best=6.720, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=18.358, d_after=18.358, d_best=7.358, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.154759474226502->29.154759474226502
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.95449840010015->26.1725046566048
r_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=30.463092423455635->32.31098884280702
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=18.439, d_after=18.439, d_best=7.439, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=21.932, d_after=18.028, delta=3.904, norm=0.651, bonus=+0.020
2026-02-24 15:31:45 | Reward (progress к objective): d_before=24.187, d_after=19.209, delta=4.977, norm=0.830, bonus=+0.025
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
ьба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.250
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.340
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=29.614, d_after=29.614, d_best=18.614, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=34.670, d_after=34.670, d_best=23.670, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=29.155, d_after=29.155, d_best=18.155, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=31.016, d_after=31.016, d_best=20.016, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=21.190, d_after=21.190, d_best=10.190, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=26.907, d_after=26.907, d_best=15.907, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
=25.45584412271571->26.1725046566048
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=31.016124838541646->31.016124838541646, hold_penalty_events=2
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.180
 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.1725046566048->31.78049716414141
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (progress к objective): d_before=31.016, d_after=26.870, delta=4.146, norm=0.691, bonus=+0.021
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
0
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.400
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.154759474226502->29.154759474226502, hold_penalty_events=2
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.590
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
ьба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (progress к objective): d_before=19.209, d_after=13.892, delta=5.317, norm=0.886, bonus=+0.027
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.250
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (progress к objective): d_before=18.358, d_after=17.493, delta=0.865, norm=0.144, bonus=+0.004
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=28.018, d_after=28.018, d_best=17.018, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=19.416, d_after=19.416, d_best=8.416, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)

2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=26.870, d_after=26.870, d_best=15.870, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=13.892, d_after=13.892, d_best=2.892, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=26.173, d_after=26.173, d_best=15.173, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=31.016, d_after=31.016, d_best=20.016, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=21.633, d_after=21.633, d_best=10.633, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=29.155, d_after=29.155, d_best=18.155, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
�): hold_penalty=-0.090 (obj=0, d_before=33.015, d_after=33.015, d_best=22.015, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.180
): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
пуск = -0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.160
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=02026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.400
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.200
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:45 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
 моделей): Reward (стрельба): quality_bonus=+0.050
00, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
ard=+0.000, penalty=-0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.870057685088806->26.870057685088806, hold_penalty_events=2
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (progress к objective): d_before=21.190, d_after=20.881, delta=0.309, norm=0.052, bonus=+0.002
2026-02-24 15:31:45 | Reward (progress к objective): d_before=29.155, d_after=22.204, delta=6.951, norm=1.159, bonus=+0.035
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (progress к objective): d_before=23.601, d_after=20.518, delta=3.083, norm=0.514, bonus=+0.015
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
.100
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.730
2026-02-24 15:31:45 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.045
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=-0.005
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.005
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:45 | Reward (progress к objective): d_before=17.493, d_after=17.000, delta=0.493, norm=0.082, bonus=+0.002
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | Reward (progress к objective): d_before=13.892, d_after=12.042, delta=1.851, norm=0.308, bonus=+0.009
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=29.155, d_after=29.155, d_best=18.155, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=02026-02-24 15:31:45 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
ity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.090 (norm=0.150)
�оделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:45 | Reward (progress к objective): d_before2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warrior2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.240
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-24 15:31:45 | Reward (бой): damage=0.090 (norm=0.150, dealt=3.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.135
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.560
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.105
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.200
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.105
2026-02-24 15:31:45 | Reward (progress к objective): d_before=17.000, d_after=10.630, delta=6.370, norm=1.062, bonus=+0.032
2026-02-24 15:31:45 | Reward (progress к objective): d_before=20.518, d_after=16.643, delta=3.875, norm=0.646, bonus=+0.019
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.105
re=19.416, d_after=15.620, delta=3.796, norm=0.633, bonus=+0.019
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.20360331117452->22.20360331117452
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.030
2026-02-24 15:31:45 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.090
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.090
2026-02-24 15:31:45 | Reward (progress к objective): d_before=23.601, d_after=19.799, delta=3.802, norm=0.634, bonus=+0.019
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=34.670, d_after=34.670, d_best=23.670, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=27.659, d_after=24.187, delta=3.472, norm=0.579, bonus=+0.017
ty=-0.120 (obj=0, d_before=19.026, d_after=19.026, d_best=8.026, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)

2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=15.620, d_after=15.620, d_best=4.620, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=27.166, d_after=23.854, delta=3.312, norm=0.552, bonus=+0.017
ty=-0.120 (obj=0, d_before=19.799, d_after=19.799, d_best=8.799, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.570
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.170
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
 d_after=8.944, delta=1.686, norm=0.281, bonus=+0.008
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.160
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.360
 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.030
+0.280
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.015
ors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.670
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.005
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.010
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.0102026-02-24 15:31:45 | Reward (шаг): бой delta=+0.005
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=-0.025
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.025
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.105
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.105
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.105
2026-02-24 15:31:45 | Reward (progress к objective): d_before=29.428, d_after=28.302, delta=1.126, norm=0.188, bonus=+0.006
2026-02-24 15:31:45 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=14.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=1 turn=7 battle_round=None
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=24.207, d_after=24.207, d_best=13.207, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.92582403567252->26.92582403567252
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=02026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
ld=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
(norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | Reward (шаг): движение delta=-1.000
ear_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=23.853720883753127->31.38470965295043
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.620
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (progress к objective): d_before=12.369, d_after=8.544, delta=3.825, norm=0.638, bonus=+0.019
nus=+0.100
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.732137494637012->31.76476034853718
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=19.79898987322333->22.20360331117452
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (progress к objective): d_before=30.414, d_after=29.547, delta=0.867, norm=0.145, bonus=+0.004
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.700
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.105
2026-02-24 15:31:45 | Reward (progress к objective): d_before=8.944, d_after=8.062, delta=0.882, norm=0.147, bonus=+0.004
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.105
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=22.361, d_after=22.361, d_best=11.361, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=29.017, d_after=29.017, d_best=18.017, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=24.207, d_after=24.207, d_best=13.207, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): цель мертва, выход из боя bonus=+0.300
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
9.732, d_after=29.732, d_best=18.732, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба2026-02-24 15:31:45 | Reward (шаг): движ�2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=33.015, d_after=33.015, d_best=22.015, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
): damage_term=+0.180 (norm=0.300, dealt=6.00)
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.300
 d_after=29.833, delta=1.552, norm=0.259, bonus=+0.008
 kills=0, moved_closer=0, min_dist=8.54400374531753->13.601470508735444
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.620
ear_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.20360331117452->23.40939982143925
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, n2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (n2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
mage=0.000, obj_kill=0.000, action=0.000, total=0.230
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.015
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.230
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.400
 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.010
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
0.050
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.010
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.45584412271571->25.45584412271571
2026-02-24 15:31:45 | Reward (progress к objective): d_before=26.000, d_after=24.331, delta=1.669, norm=0.278, bonus=+0.008
2026-02-24 15:31:45 | Reward (бой): advantage_term=-0.015
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=-0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.010
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.120
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.010
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.120, strength=0.000, objectives=0.000 (delta=0), total=0.120
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.120
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=22.361, d_after=22.361, d_best=11.361, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Wa2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | Reward (progress к objective): d_before=9.220, d_after=7.810, delta=1.409, norm=0.235, bonus=+0.007
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.017236257093817->29.068883707497267
2026-02-24 15:31:45 | Reward (progress к objective): d_before=13.601, d_after=8.062, delta=5.539, norm=0.923, bonus=+0.028
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
=24.20743687382041->30.364452901377952
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.100, dealt=2.00)
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.100 (norm=0.200)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
00, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.100 (norm=0.200, taken=4.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.055
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.055
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | Reward (progress к objective): d_before=23.409, d_after=17.000, delta=6.409, norm=1.068, bonus=+0.032
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | Reward (progress к objective): d_before=29.833, d_after=29.069, delta=0.764, norm=0.127, bonus=+0.004
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): advantage_term=-0.030
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=-0.030, strength=0.000, objectives=0.000 (delta=0), total=-0.000
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.000
2026-02-24 15:31:45 | Reward (поражение): penalty=-2.000
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=29.547, d_after=29.547, d_best=18.547, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=None->None
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=24.207, d_after=24.207, d_best=13.207, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=26.249, d_after=22.361, delta=3.888, norm=0.648, bonus=+0.019
�ление из боя penalty=-0.500
er=17.000, d_best=6.000, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x102026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Re2026-02-24 15:31:45 | Reward (шаг): движ2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.620
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.154759474226502->30.083217912982647
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=31.76476034853718->32.449961479175904
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
0, moved_closer=0, min_dist=24.20743687382041->24.20743687382041, hold_penalty_events=2
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | Reward (progress к objective): d_before=30.083, d_after=29.000, delta=1.083, norm=0.181, bonus=+0.005
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.170
2026-02-24 15:31:45 | Reward (progress к objective): d_before=34.132, d_after=32.450, delta=1.682, norm=0.280, bonus=+0.008
| [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=30.017, d_after=30.017, d_best=19.017, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=30.806, d_after=30.806, d_best=19.806, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.591260281974->20.591260281974
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00,2026-02-24 15:31:45 | Reward (progress к objective): d_before=26.683, d_a2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.360679774997898->22.360679774997898
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.09975124224178->20.615528128088304
60727->30.01666203960727, hold_penalty_events=2
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.839484696748443->28.319604517012593
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=29.155, d_after=29.155, d_best=18.155, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=26.249, d_after=26.249, d_best=15.249, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | Reward (progress к objective): d_before=29.275, d_after=29.155, delta=0.120, norm=0.020, bonus=+0.001
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:45 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.248809496813376->26.248809496813376, hold_penalty_events=2
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=30.01666203960727->30.01666203960727
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.615528128088304->20.615528128088304
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.30589287593181->27.202941017470888
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.360679774997898->26.30589287593181
2026-02-24 15:31:45 | Reward (progress к objective): d_before=16.125, d_after=14.142, delta=1.982, norm=0.330, bonus=+0.010
 kills=0, moved_closer=0, min_dist=28.319604517012593->29.0
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.110770276274835->18.110770276274835
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.591260281974->25.45584412271571
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (progress к objective): d_before=26.870, d_after=20.616, delta=6.255, norm=1.042, bonus=+0.031
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.248809496813376->26.92582403567252
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=30.017, d_after=30.017, d_best=19.017, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=30.610, d_after=30.610, d_best=19.610, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.068883707497267->29.732137494637012
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
=0, damage=0.00, ki2026-02-24 15:31:45 | Reward (progress к objective): d_before=25.456, d_after=19.313, delta=6.143, norm=1.024, bonus=+0.031
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
ll=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=23.769728648009426->30.083217912982647
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.30589287593181->27.202941017470888
2026-02-24 15:31:45 | Reward (progress к objective): d_before=26.000, d_after=24.515, delta=1.485, norm=0.247, bonus=+0.007
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
nged=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.110770276274835->18.973665961010276
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.732137494637012->31.38470965295043
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.202941017470888->28.861739379323623
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=20.616, d_after=18.682, delta=1.934, norm=0.322, bonus=+0.010
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.250
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.280
2026-02-24 15:31:45 | Reward (progress к objective): d_before=14.142, d_after=11.180, delta=2.962, norm=0.494, bonus=+0.015
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=28.071, d_after=28.071, d_best=17.071, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=18.974, d_after=18.974, d_best=7.974, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=28.862, d_after=28.862, d_best=17.862, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=33.015, d_after=33.015, d_best=22.015, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:45 | Reward (progress к objective): d_before=11.180, d_after=5.385, delta=5.795, norm=0.966, bonus=+0.029
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.681541692269406->29.206163733020468
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
трельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.150
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=30.083217912982647->32.202484376209235
_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (progress к objective): d_before=29.833, d_after=27.586, delta=2.247, norm=0.374, bonus=+0.011
 taken=0.00), advantage=0.150, strength=0.000, objectives=0.000 (delta=0), total=0.610
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
ьба): quality_bonus=+0.050
50, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x102026-02-24 15:31:45 | Reward (progress к objective): d_before=19.313, d_after=18.028, delta=1.285, norm=0.214, bonus=+0.006
, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | Reward (progress к objective): d_before=30.017, d_after=25.000, delta=5.017, norm=0.836, bonus=+0.025
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
n=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (progress к objective): d_before=24.515, d_after=24.187, delta=0.329, norm=0.055, bonus=+0.002
2026-02-24 15:31:45 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | Reward (progress к objective): d_before=21.541, d_after=17.000, delta=4.541, norm=0.757, bonus=+0.023
2026-02-24 15:31:45 | Reward (бой): advantage_term=-0.030
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=-0.030, strength=0.000, objectives=0.000 (delta=0), total=-0.030
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.030
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-24 15:31:45 | Reward (progress к objective): d_before=27.203, d_after=18.358, delta=8.845, norm=1.474, bonus=+0.044
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=32.202, d_after=32.202, d_best=21.202, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=29.206, d_after=29.206, d_best=18.206, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=34.132, d_after=34.132, d_best=23.132, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=27.586, d_after=27.586, d_best=16.586, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=30.610, d_after=30.610, d_best=19.610, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=29.428, d_after=29.428, d_best=18.428, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.240
 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 м�2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей)2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.240
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
oved_closer=0, min_dist=30.870698080866262->33.12099032335839
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
50, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delt2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
orm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=17.0->21.213203435596427
ity=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (progress к objective): d_before=24.187, d_after=23.195, delta=0.992, norm=0.165, bonus=+0.005
2026-02-24 15:31:45 | Reward (progress к objective): d_before=28.862, d_after=27.166, delta=1.696, norm=0.283, bonus=+0.008
500
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.220
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=0.035
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.035
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=32.202, d_after=32.202, d_best=21.202, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
9.698, d_after=19.698, d_best=8.698, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=19.849, d_after=19.849, d_best=8.849, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)

2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=19.698, d_after=19.698, d_best=8.698, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)

2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=20.125, d_after=20.125, d_best=9.125, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=34.132, d_after=34.132, d_best=23.132, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
ld=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.206163733020468->30.0
2026-02-24 15:31:45 | Reward (бой): advantage_term=-0.030
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:45 | Reward (бой): advantage_term=-0.090
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
ьба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.045
-0.240
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=-0.030, strength=0.000, objectives=0.000 (delta=0), total=-0.030
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.110770276274835->18.681541692269406
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.030
(norm=0.050)
0), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.105
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.060
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.150, dealt=3.00)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.385164807134504->6.4031242374328485
2026-02-24 15:31:45 | Reward (progress к objective): d_before=27.166, d_after=19.235, delta=7.931, norm=1.322, bonus=+0.040
0 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=-0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.010
obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.010
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.130
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.300
 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.310
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.250
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.015
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=0.020
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.020
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | Reward (progress к objective): d_before=23.195, d_after=19.235, delta=3.959, norm=0.660, bonus=+0.020
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.120
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.120, strength=0.000, objectives=0.000 (delta=0), total=0.150
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.150
2026-02-24 15:31:45 | Reward (progress к objective): d_before=19.698, d_after=12.083, delta=7.615, norm=1.269, bonus=+0.038
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=32.202, d_after=32.202, d_best=21.202, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=27.586, d_after=27.586, d_best=16.586, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=34.132, d_after=34.132, d_best=23.132, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=30.610, d_after=30.610, d_best=19.610, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (progress к objective): d_before=18.788,2026-02-24 15:31:45 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | Reward (progress к objective): d_before=25.000, d_after=22.361, delta=2.639, norm=0.440, bonus=+0.013
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | Reward (progress к objective): d_before=19.849, d_after=18.248, delta=1.601, norm=0.267, bonus=+0.008
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=6.403, d_after=5.385, delta=1.018, norm=0.170, bonus=+0.005
2026-02-24 15:31:45 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.090 (norm=0.150)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
�делей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
oved_closer=0, min_dist=12.083045973594572->14.866068747318506
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:45 | Reward (бой): damage=0.090 (norm=0.150, dealt=3.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.135, strength=0.000, objectives=0.000 (delta=0), total=0.175
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.130
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.175
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.200
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.200
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.130
2026-02-24 15:31:45 | Reward (progress к objective): d_before=19.235, d_after=19.105, delta=0.130, norm=0.022, bonus=+0.001
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.330
 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.570
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.130
2026-02-24 15:31:45 | Reward (бой): advantage_term=-0.015
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.710
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.260
=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.035
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.035
riors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.090 (norm=0.150)
2026-02-24 15:31:45 | Reward (бой): kill_term=+0.400 (delta=1)
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.105
2026-02-24 15:31:45 | Reward (бой): damage=0.090 (norm=0.150, dealt=3.00), kills=0.400 (delta=1), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.595
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.595
2026-02-24 15:31:45 | Reward (победа): bonus=+3.000
2026-02-24 15:31:45 | Reward (progress к objective): d_before=32.202, d_after=28.792, delta=3.410, norm=0.568, bonus=+0.017
2026-02-24 15:31:45 | Reward (поражение): penalty=-2.000
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
lty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=14.866, d_after=14.866, d_best=3.866, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=27.459, d_after=27.459, d_best=16.459, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
248, d_after=18.248, d_best=7.248, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=28.42534080710379->34.132096331752024
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.400
2026-02-24 15:31:45 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warrior2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
s (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.170
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.170
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.170
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x102026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.280
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.200
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.060 (norm=0.100)
2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
fter=31.385, delta=0.396, norm=0.066, bonus=+0.002
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.210
2026-02-24 15:31:45 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.210, strength=0.000, objectives=0.000 (delta=0), total=0.245
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.245
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=19.105, d_after=18.358, delta=0.747, norm=0.125, bonus=+0.004
2026-02-24 15:31:45 | Reward (бой): kill_term=+0.400 (delta=1)
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.120
2026-02-24 15:31:45 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.400 (delta=1), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.120, strength=0.000, objectives=0.000 (delta=0), total=0.580
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.580
2026-02-24 15:31:45 | Reward (progress к objective): d_before=14.866, d_after=13.454, delta=1.412, norm=0.235, bonus=+0.007
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (progress к objective): d_before=13.454, d_after=9.849, delta=3.605, norm=0.601, bonus=+0.018
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
n_dist=23.769728648009426->27.459060435491963
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.200
 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.385164807134504->5.385164807134504
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.02026-02-24 15:31:45 | [MODEL]2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
�рельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | Reward (VP diff): prev=-2, curr=-3, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:45 | Reward (progress к objective): d_before=18.248, d_after=18.028, delta=0.221, norm=0.037, bonus=+0.001
2026-02-24 15:31:45 | Reward (progress к objective): d_before=33.121, d_after=33.015, delta=0.106, norm=0.018, bonus=+0.001
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=24.166, d_after=22.204, delta=1.962, norm=0.327, bonus=+0.010
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.045
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.590
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.150 (norm=0.250)
�оделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.075
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | Reward (progress к objective): d_before=18.358, d_after=17.889, delta=0.469, norm=0.078, bonus=+0.002
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.075
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.225
2026-02-24 15:31:45 | Reward (бой): damage=0.150 (norm=0.250, dealt=5.00), kills=0.800 (delta=2), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.225, strength=0.000, objectives=0.000 (delta=0), total=1.175
2026-02-24 15:31:45 | Reward (шаг): бой delta=+1.175
2026-02-24 15:31:45 | Reward (победа): bonus=+3.000
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.075 (norm=0.150)
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.075 (norm=0.150, taken=3.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=-0.075
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.075
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=5.00, norm=0.250, penalty=-0.125
2026-02-24 15:31:45 | Reward (progress к objective): d_before=17.889, d_after=6.000, delta=11.889, norm=1.981, bonus=+0.059
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=25.298, d_after=25.298, d_best=14.298, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (поражение): penalty=-2.000
x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=27.459, d_after=27.459, d_best=16.459, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=30.676, d_after=30.676, d_best=19.676, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=33.015, d_after=26.907, delta=6.108, norm=1.018, bonus=+0.031
ty=-0.060 (obj=0, d_before=30.000, d_after=30.000, d_best=19.000, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=24.759, d_after=24.759, d_best=13.759, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=02026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.090, proximity=0.000, total=-0.090
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.110
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.090
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
, moved_closer=0, min_dist=27.459060435491963->27.459060435491963, hold_penalty_events=2
2026-02-24 15:31:45 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:45 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:45 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.298221281347036->25.298221281347036, hold_penalty_events=2
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
0)
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.090
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.400
 d_after=27.731, delta=2.502, norm=0.417, bonus=+0.013
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.024984394500787->20.8806130178211
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
=17.88854381999832->17.88854381999832
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=30.675723300355934->30.675723300355934, hold_penalty_events=2
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | Reward (progress к objective): d_before=18.028, d_after=18.000, delta=0.028, norm=0.005, bonus=+0.000
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.000
2026-02-24 15:31:45 | Reward (бой/у цели): damage_term=+0.050 (raw=1.00)
2026-02-24 15:31:45 | Reward (объекты, бой): damage=0.050 (raw=1.00), kills=0.000 (count=0)
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=0.030
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.030
2026-02-24 15:31:45 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=1 steps=6 skip={move:3,attack:4,shoot:1,charge:4,use_cp:0,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.500,attack:0.667,shoot:0.167,charge:0.667,use_cp:0.000,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:5,without_targets:1}
2026-02-24 15:31:45 | [TRAIN][EP] ep=1 ep_reward=0.751184 win=1 vp_diff=-1 end_reason=wipeout_enemy
2026-02-24 15:31:45 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=9.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=0 turn=10 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=2 steps=9 skip={move:1,attack:4,shoot:3,charge:4,use_cp:0,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.111,attack:0.444,shoot:0.333,charge:0.444,use_cp:0.000,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:6,without_targets:3}
2026-02-24 15:31:45 | [TRAIN][EP] ep=2 ep_reward=0.626215 win=1 vp_diff=0 end_reason=wipeout_enemy
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=14.0 enemy_hp_total=14.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=3 steps=10 skip={move:2,attack:6,shoot:3,charge:6,use_cp:2,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.200,attack:0.600,shoot:0.300,charge:0.600,use_cp:0.200,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:7,without_targets:3}
2026-02-24 15:31:45 | [TRAIN][EP] ep=3 ep_reward=-0.056320 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=14.0 enemy_hp_total=7.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=4 steps=10 skip={move:2,attack:8,shoot:3,charge:8,use_cp:3,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.200,attack:0.800,shoot:0.300,charge:0.800,use_cp:0.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:7,without_targets:3}
2026-02-24 15:31:45 | [TRAIN][EP] ep=4 ep_reward=-0.022500 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=3.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=5 steps=10 skip={move:2,attack:3,shoot:4,charge:3,use_cp:1,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.200,attack:0.300,shoot:0.400,charge:0.300,use_cp:0.100,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:6,without_targets:4}
2026-02-24 15:31:45 | [TRAIN][EP] ep=5 ep_reward=-0.107812 win=0 vp_diff=0 end_reason=wipeout_model
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=16.0 enemy_hp_total=18.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=6 steps=10 skip={move:2,attack:8,shoot:1,charge:8,use_cp:1,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.200,attack:0.800,shoot:0.100,charge:0.800,use_cp:0.100,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:9,without_targets:1}
2026-02-24 15:31:45 | [TRAIN][EP] ep=6 ep_reward=-0.013656 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=9.0 enemy_hp_total=7.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=7 steps=10 skip={move:1,attack:7,shoot:3,charge:7,use_cp:1,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.100,attack:0.700,shoot:0.300,charge:0.700,use_cp:0.100,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:7,without_targets:3}
2026-02-24 15:31:45 | [TRAIN][EP] ep=7 ep_reward=0.158878 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=4.0 enemy_hp_total=12.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=8 steps=10 skip={move:3,attack:5,shoot:4,charge:5,use_cp:1,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.300,attack:0.500,shoot:0.400,charge:0.500,use_cp:0.100,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:6,without_targets:4}
2026-02-24 15:31:45 | [TRAIN][EP] ep=8 ep_reward=-0.060738 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=13.0 enemy_hp_total=5.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=9 steps=10 skip={move:2,attack:5,shoot:4,charge:5,use_cp:3,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.200,attack:0.500,shoot:0.400,charge:0.500,use_cp:0.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:6,without_targets:4}
2026-02-24 15:31:45 | [TRAIN][EP] ep=9 ep_reward=0.092755 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=16.0 enemy_hp_total=9.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=10 steps=10 skip={move:1,attack:9,shoot:4,charge:9,use_cp:2,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.100,attack:0.900,shoot:0.400,charge:0.900,use_cp:0.200,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:6,without_targets:4}
2026-02-24 15:31:45 | [TRAIN][EP] ep=10 ep_reward=-0.142453 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=4.0 enemy_hp_total=8.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=11 steps=10 skip={move:1,attack:3,shoot:3,charge:3,use_cp:4,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.100,attack:0.300,shoot:0.300,charge:0.300,use_cp:0.400,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:7,without_targets:3}
2026-02-24 15:31:45 | [TRAIN][EP] ep=11 ep_reward=0.027345 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=15.0 enemy_hp_total=18.0 model_vp=0 enemy_vp=2 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=12 steps=10 skip={move:3,attack:6,shoot:5,charge:6,use_cp:3,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.300,attack:0.600,shoot:0.500,charge:0.600,use_cp:0.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:5,without_targets:5}
2026-02-24 15:31:45 | [TRAIN][EP] ep=12 ep_reward=-0.124058 win=0 vp_diff=-2 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=4.0 enemy_hp_total=9.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=13 steps=10 skip={move:3,attack:9,shoot:6,charge:9,use_cp:1,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.300,attack:0.900,shoot:0.600,charge:0.900,use_cp:0.100,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:10,without_targets:6}
2026-02-24 15:31:45 | [TRAIN][EP] ep=13 ep_reward=-0.005414 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=20.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=1 turn=8 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=14 steps=7 skip={move:4,attack:10,shoot:7,charge:10,use_cp:1,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.571,attack:1.429,shoot:1.000,charge:1.429,use_cp:0.143,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:10,without_targets:7}
2026-02-24 15:31:45 | [TRAIN][EP] ep=14 ep_reward=0.619265 win=1 vp_diff=-1 end_reason=wipeout_enemy
2026-02-24 15:31:45 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=17.0 model_vp=0 enemy_vp=0 turn=9 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=15 steps=8 skip={move:5,attack:11,shoot:8,charge:11,use_cp:5,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.625,attack:1.375,shoot:1.000,charge:1.375,use_cp:0.625,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:10,without_targets:8}
2026-02-24 15:31:45 | [TRAIN][EP] ep=15 ep_reward=-0.294590 win=0 vp_diff=0 end_reason=wipeout_model
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=19.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=16 steps=10 skip={move:3,attack:8,shoot:8,charge:8,use_cp:1,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.300,attack:0.800,shoot:0.800,charge:0.800,use_cp:0.100,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:11,without_targets:8}
2026-02-24 15:31:45 | [TRAIN][EP] ep=16 ep_reward=0.046609 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=20.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=0 turn=10 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=17 steps=9 skip={move:3,attack:10,shoot:7,charge:10,use_cp:1,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.333,attack:1.111,shoot:0.778,charge:1.111,use_cp:0.111,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:12,without_targets:7}
2026-02-24 15:31:45 | [TRAIN][EP] ep=17 ep_reward=0.406587 win=1 vp_diff=0 end_reason=wipeout_enemy
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=13.0 enemy_hp_total=8.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=18 steps=10 skip={move:2,attack:12,shoot:4,charge:12,use_cp:8,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.200,attack:1.200,shoot:0.400,charge:1.200,use_cp:0.800,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:16,without_targets:4}
2026-02-24 15:31:45 | [TRAIN][EP] ep=18 ep_reward=0.090718 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=19.0 enemy_hp_total=3.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=19 steps=10 skip={move:3,attack:12,shoot:6,charge:12,use_cp:4,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.300,attack:1.200,shoot:0.600,charge:1.200,use_cp:0.400,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:14,without_targets:6}
2026-02-24 15:31:45 | [TRAIN][EP] ep=19 ep_reward=0.068175 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=20 steps=10 skip={move:5,attack:11,shoot:9,charge:11,use_cp:3,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.500,attack:1.100,shoot:0.900,charge:1.100,use_cp:0.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:11,without_targets:9}
2026-02-24 15:31:45 | [TRAIN][EP] ep=20 ep_reward=-0.110761 win=0 vp_diff=0 end_reason=wipeout_model
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=4.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=21 steps=10 skip={move:3,attack:11,shoot:8,charge:11,use_cp:4,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.300,attack:1.100,shoot:0.800,charge:1.100,use_cp:0.400,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:12,without_targets:8}
2026-02-24 15:31:45 | [TRAIN][EP] ep=21 ep_reward=-0.052728 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=16.0 enemy_hp_total=7.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=22 steps=10 skip={move:4,attack:13,shoot:9,charge:13,use_cp:4,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.400,attack:1.300,shoot:0.900,charge:1.300,use_cp:0.400,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:11,without_targets:9}
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
 d_after=16.155, delta=5.685, norm=0.947, bonus=+0.028
 kills=0, moved_closer=0, min_dist=27.459060435491963->27.459060435491963
2026-02-24 15:31:45 | Reward (progress к objective): d_before=23.087, d_after=22.023, delta=1.064, norm=0.177, bonus=+0.005
 kills=0, moved_closer=0, min_dist=22.02271554554524->23.021728866442675
2026-02-24 15:31:45 | Reward (progress к objective): d_before=19.723, d_after=19.235, delta=0.488, norm=0.081, bonus=+0.002
 kills=0, moved_closer=0, min_dist=19.4164878389476->20.615528128088304
2026-02-24 15:31:45 | Reward (progress к objective): d_before=18.358, d_after=16.125, delta=2.233, norm=0.372, bonus=+0.011
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.298221281347036->30.364452901377952
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=19.723, d_after=17.720, delta=2.003, norm=0.334, bonus=+0.010
=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=23.769728648009426->29.614185789921695
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.170
2026-02-24 15:31:45 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=34.670, d_after=34.670, d_best=23.670, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=31.780, d_after=31.780, d_best=20.780, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
�): hold_penalty=-0.060 (obj=0, d_before=16.125, d_after=16.125, d_best=5.125, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=19.235, d_after=14.213, delta=5.023, norm=0.837, bonus=+0.025
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.615528128088304->26.248809496813376
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=26.683, d_after=26.683, d_best=15.683, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=22.023, d_after=16.031, delta=5.991, norm=0.999, bonus=+0.030
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=29.614, d_after=23.770, delta=5.844, norm=0.974, bonus=+0.029
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (no2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=16.155, d_after=10.817, delta=5.339, norm=0.890, bonus=+0.027
0 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | Reward (progress к objective): d_before=17.720, d_after=17.117, delta=0.603, norm=0.100, bonus=+0.003
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-24 15:31:45 | Reward (progress к objective): d_before=27.459, d_after=24.698, delta=2.761, norm=0.460, bonus=+0.014
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.280
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.250
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | Reward (progress к objective): d_before=30.364, d_after=29.614, delta=0.750, norm=0.125, bonus=+0.004
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.310
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.105
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.110
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.110
2026-02-24 15:31:45 | Reward (progress к objective): d_before=31.780, d_after=23.431, delta=8.350, norm=1.392, bonus=+0.042
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=29.614, d_after=29.614, d_best=18.614, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=34.670, d_after=34.670, d_best=23.670, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=31.305, d_after=31.305, d_best=20.305, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=16.125, d_after=16.125, d_best=5.125, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=26.683, d_after=26.683, d_best=15.683, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
ьба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.698178070456937->29.427877939124322
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.080
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
nged=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.758836806279895->29.0
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | Reward (progress к objective): d_before=10.817, d_after=6.083, delta=4.734, norm=0.789, bonus=+0.024
nus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=14.212670403551895->21.02379604162864
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.385164807134504->7.0710678118654755
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (с2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=17.11724276862369->18.788294228055936
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.105
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.280
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.220
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.105
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.105
2026-02-24 15:31:45 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | Reward (progress к objective): d_before=23.770, d_after=18.974, delta=4.796, norm=0.799, bonus=+0.024
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
er=25.020, d_best=14.020, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
er=17.804, d_best=6.804, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.180
 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.100 (norm=0.200)
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.590
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.030
ors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (с�2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
ьба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
00, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.170
 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.150 (dealt=3.00)
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
 d_after=26.926, delta=2.074, norm=0.346, bonus=+0.010
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
 d_after=20.591, delta=2.839, norm=0.473, bonus=+0.014
2026-02-24 15:31:45 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
trol_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.082762530298219->6.324555320336759
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | Reward (progress к objective): d_before=7.071, d_after=5.099, delta=1.972, norm=0.329, bonus=+0.010
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.150, obj_kill=0.000, action=0.000, total=0.360
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
nged=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.788294228055936->18.788294228055936
2026-02-24 15:31:45 | Reward (progress к objective): d_before=21.024, d_after=14.213, delta=6.811, norm=1.135, bonus=+0.034
2026-02-24 15:31:45 | Reward (progress к objective): d_before=29.428, d_after=29.275, delta=0.153, norm=0.026, bonus=+0.001
2026-02-24 15:31:45 | Reward (progress к objective): d_before=18.974, d_after=18.000, delta=0.974, norm=0.162, bonus=+0.005
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.640
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.030
2026-02-24 15:31:45 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.065
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.065
2026-02-24 15:31:45 | Reward (progress к objective): d_before=17.804, d_after=17.692, delta=0.113, norm=0.019, bonus=+0.001
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (progress к objective): d_before=14.213, d_after=9.055, delta=5.157, norm=0.860, bonus=+0.026
пление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.832867780352597->31.78049716414141
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.060
=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | Reward (бой): advantage_term=-0.045
-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
-02-24 15:31:45 | Reward (шаг): движение delta=-1.000
0.150, dealt=3.00)
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.090
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.0990195135927845->10.04987562112089
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
=-0.000 (norm=0.000, taken=0.00), advantage=-0.045, strength=0.000, objectives=0.000 (delta=0), total=-0.015
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (бой): advantage_term=-0.075
age_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.090
riors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.0->18.681541692269406
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.015
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (progress к objective): d_before=18.788, d_after=17.263, delta=1.526, norm=0.254, bonus=+0.008
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.278820596099706->17.88854381999832
, total=-0.100
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.100
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.030
2026-02-24 15:31:45 | Reward (бой): advantage_term=-0.075
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.030
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=-0.075, strength=0.000, objectives=0.000 (delta=0), total=-0.045
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.030
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.045
2026-02-24 15:31:45 | Reward (progress к objective): d_before=26.926, d_after=25.298, delta=1.628, norm=0.271, bonus=+0.008
2026-02-24 15:31:45 | Reward (progress к objective): d_before=29.017, d_after=27.459, delta=1.558, norm=0.260, bonus=+0.008
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
lty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=19.105, d_after=19.105, d_best=8.105, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
r=9.055, d_best=0.000, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:45 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
ontrol_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.681541692269406->28.460498941515414
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
0)
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:45 | Reward (шаг): движение delta=-1.000
ear_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=17.26267650163207->18.027756377319946
2026-02-24 15:31:45 | Reward (шаг): движение delta=-1.000
 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | Reward (бой): advantage_term=-0.090
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
.215, bonus=+0.006
2026-02-24 15:31:45 | Reward (progress к objective): d_before=5.000, d_after=3.162, delta=1.838, norm=0.306, bonus=+0.009
2026-02-24 15:31:45 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.002026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=-0.090, strength=0.000, objectives=0.000 (delta=0), total=-0.115
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.591260281974->23.430749027719962
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist2026-02-24 15:31:45 | [MODEL] Unit 22 —2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.120
�ельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.115
=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.459060435491963->28.460498941515414
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=31.016124838541646->31.016124838541646
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.300, dealt=6.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.230
2026-02-24 15:31:45 | Reward (progress к objective): d_before=14.765, d_after=13.038, delta=1.726, norm=0.288, bonus=+0.009
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:45 | Reward (VP diff): prev=-3, curr=-4, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.790
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | Reward (поражение): penalty=-2.000
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
ear_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=None->None
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=None->None
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.360679774997898->26.248809496813376
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
d=+0.050, penalty=-0.000
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.090
2026-02-24 15:31:45 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.065
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | Reward (бой): advantage_term=-0.015
2026-02-24 15:31:45 | Reward (progress к objective): d_before=27.203, d_after=26.173, delta=1.030, norm=0.172, bonus=+0.005
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.570
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.065
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=-0.120, strength=0.000, objectives=0.000 (delta=0), total=-0.120
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.027756377319946->20.248456731316587
 total=0.015
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.570
2026-02-24 15:31:45 | Reward (шаг): бой delta=-0.120
riors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.015
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | Reward (победа): bonus=+3.000
2026-02-24 15:31:45 | Reward (progress к objective): d_before=31.016, d_after=29.155, delta=1.861, norm=0.310, bonus=+0.009
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | Reward (progress к objective): d_before=9.055, d_after=7.071, delta=1.984, norm=0.331, bonus=+0.010
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.160
2026-02-24 15:31:45 | Reward (поражение): penalty=-2.000
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=29.206, d_after=29.206, d_best=18.206, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=None->None
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
ние): отступление из боя penalty=-0.500
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=32.202, d_after=32.202, d_best=21.202, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
n_dist=21.93171219946131->21.93171219946131
2026-02-24 15:31:45 | Reward (VP diff): prev=2, curr=1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | Reward (progress к objective): d_before=24.413, d_after=21.541, delta=2.872, norm=0.479, bonus=+0.014
2026-02-24 15:31:45 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
): остался в бою bonus=+0.200
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.045361017187261->12.529964086141668
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.80350850198276->26.1725046566048
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:45 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:45 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.206163733020468->29.206163733020468, hold_penalty_events=2
=0.140
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=31.76476034853718->34.132096331752024
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.248809496813376->26.570660511172846
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.120 (norm=0.200)
2026-02-24 15:31:45 | Reward (progress к objective): d_before=20.248, d_after=17.804, delta=2.444, norm=0.407, bonus=+0.012
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.060
2026-02-24 15:31:45 | Reward (бой): damage=0.120 (norm=0.200, dealt=4.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.155
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.155
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.030
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.010
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.010
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | Reward (поражение): penalty=-2.000
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=None->None
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=None->None
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.93171219946131->21.93171219946131
2026-02-24 15:31:45 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:45 | Reward (progress к objective): d_before=24.083, d_after=19.313, delta=4.770, norm=0.795, bonus=+0.024
2026-02-24 15:31:45 | Reward (progress к objective): d_before=26.173, d_after=21.024, delta=5.149, norm=0.858, bonus=+0.026
2026-02-24 15:31:45 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:45 | Reward (бой): advantage_term=+0.015
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:45 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.010
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.540659228538015->22.360679774997898
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:45 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.135943621178654->22.135943621178654
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:45 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=0.045
2026-02-24 15:31:45 | Reward (шаг): бой delta=+0.045
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.160
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.330
2026-02-24 15:31:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | Reward (шаг): стрельба delta=+0.250
 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:45 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:45 | Reward (progress к objective): d_before=17.804, d_after=17.205, delta=0.600, norm=0.100, bonus=+0.003
2026-02-24 15:31:45 | Reward (progress к objective): d_before=29.206, d_after=25.456, delta=3.750, norm=0.625, bonus=+0.019
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=22.361, d_after=22.361, d_best=11.361, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=25.456, d_after=25.456, d_best=14.456, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=26.249, d_after=26.249, d_best=15.249, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=27.785, d_after=27.785, d_best=16.785, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | Reward (урон по модели): damage_take2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.166091947189145->24.596747752497688
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=23.40939982143925->30.083217912982647
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.02379604162864->21.95449840010015
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.240 (norm=0.400, dealt=8.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-24 15:31:46 | Reward (progress к objective): d_before=22.136, d_after=21.095, delta=1.041, norm=0.173, bonus=+0.005
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (progress к objective): d_before=28.460, d_after=27.295, delta=1.166, norm=0.194, bonus=+0.006
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.240 (norm=0.400, dealt=8.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.290
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=17.205, d_after=11.662, delta=5.543, norm=0.924, bonus=+0.028
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (progress к objective): d_before=18.868, d_after=12.806, delta=6.062, norm=1.010, bonus=+0.030
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=28.425, d_after=27.659, delta=0.767, norm=0.128, bonus=+0.004
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=29.206, d_after=29.206, d_best=18.206, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=27.659, d_after=27.659, d_best=16.659, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=20.224, d_after=20.000, delta=0.224, norm=0.037, bonus=+0.001
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.80697580112788->25.80697580112788
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.495097567963924->26.870057685088806
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
трельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=29.275, d_after=29.155, delta=0.120, norm=0.020, bonus=+0.001
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:46 | Reward (progress к objective): d_before=21.954, d_after=19.105, delta=2.850, norm=0.475, bonus=+0.014
2026-02-24 15:31:46 | Reward (progress к objective): d_before=25.456, d_after=25.000, delta=0.456, norm=0.076, bonus=+0.002
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, n2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.360679774997898->22.360679774997898
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
 d_after=24.515, delta=0.081, norm=0.014, bonus=+0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=34.670, d_after=34.670, d_best=23.670, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=26.870, d_after=26.870, d_best=15.870, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | Reward (progress к objective): d_before=27.659, d_after=27.019, delta=0.640, norm=0.107, bonus=+0.003
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.80697580112788->28.319604517012593
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.515301344262525->29.614185789921695
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
ward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.154759474226502->30.083217912982647
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=27.785, d_after=24.331, delta=3.454, norm=0.576, bonus=+0.017
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=19.1049731745428->20.248456731316587
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.870057685088806->26.870057685088806, hold_penalty_events=2
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.075
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=25.000, d_after=23.601, delta=1.399, norm=0.233, bonus=+0.007
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.075, strength=0.000, objectives=0.000 (delta=0), total=-0.065
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.280
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (progress к objective): d_before=22.361, d_after=16.401, delta=5.959, norm=0.993, bonus=+0.030
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=34.670, d_after=34.670, d_best=23.670, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
er=34.132, d_best=23.132, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=26.870, d_after=26.870, d_best=15.870, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=30.083, d_after=30.083, d_best=19.083, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=23.600847442411894->27.586228448267445
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (progress к objective): d_before=25.179, d_after=19.235, delta=5.944, norm=0.991, bonus=+0.030
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.870057685088806->26.870057685088806, hold_penalty_events=2
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=33.615, d_after=33.121, delta=0.494, norm=0.082, bonus=+0.002
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=30.083217912982647->30.083217912982647, hold_penalty_events=2
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
�оделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=28.319604517012593->33.54101966249684
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
�делей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=02026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (progress к objective): d_before=20.248, d_after=19.105, delta=1.143, norm=0.191, bonus=+0.006
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.000
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.170
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.000, strength=0.000, objectives=0.000 (delta=0), total=0.010
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.010
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
 d_after=13.416, delta=1.348, norm=0.225, bonus=+0.007
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.170
ard=+0.000, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (progress к objective): d_before=16.401, d_after=14.318, delta=2.083, norm=0.347, bonus=+0.010
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (progress к objective): d_before=29.614, d_after=24.739, delta=4.876, norm=0.813, bonus=+0.024
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.045
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.045
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.045
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=20.616, d_after=12.042, delta=8.574, norm=1.429, bonus=+0.043
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=24.021, d_after=24.021, d_best=13.021, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
lty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=33.121, d_after=33.121, d_best=22.121, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=21.213, d_after=21.213, d_best=10.213, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=34.670, d_after=34.670, d_best=23.670, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=31.401, d_after=31.401, d_best=20.401, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=14.318, d_after=14.318, d_best=3.318, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=32.202, d_after=32.202, d_best=21.202, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
�): hold_penalty=-0.090 (obj=0, d_before=31.906, d_after=31.906, d_best=20.906, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
ear_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.591260281974->23.430749027719962
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.090, proximity=0.000, total=-0.090
2026-02-24 15:31:46 | Reward (progress к objective): d_before=26.870, d_after=21.024, delta=5.846, norm=0.974, bonus=+0.029
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=30.083217912982647->30.528675044947494
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.590

2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=0.030
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.060
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.416407864998739->16.278820596099706
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.030
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.090
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.300, dealt=6.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.230
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.090
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.230
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
�рельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=12.041594578792296->13.416407864998739, hold_penalty_events=1
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=32.202484376209235->32.202484376209235, hold_penalty_events=2
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.280
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.220
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.030
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.040
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.040
2026-02-24 15:31:46 | Reward (поражение): penalty=-2.000
x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
lty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
er=34.670, d_best=23.670, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, mi2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (progress к objective): d_before=30.529, d_after=27.514, delta=3.015, norm=0.503, bonus=+0.015
за пропуск = -0.200
0)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=33.12099032335839->34.132096331752024
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
�оделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 �2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, qual2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.030
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
�делей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.065
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.065
riors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.030
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.170
=2.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.150, strength=0.000, objectives=0.000 (delta=0), total=0.160
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.160
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-24 15:31:46 | Reward (progress к objective): d_before=21.024, d_after=20.125, delta=0.899, norm=0.150, bonus=+0.004
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.670
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): kill_term=+0.400 (delta=1)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.120
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.400 (delta=1), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.120, strength=0.000, objectives=0.000 (delta=0), total=0.550
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.550
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (победа): bonus=+3.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (поражение): penalty=-2.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=34.670, d_after=34.670, d_best=23.670, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
lty=-0.500
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=None->None
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=24.021, d_after=18.028, delta=5.993, norm=0.999, bonus=+0.030
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=32.202, d_after=32.202, d_best=21.202, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.758836806279895->26.1725046566048
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.060
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
ear_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.278820596099706->31.622776601683793
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.090
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.030
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.492422502470642->18.35755975068582
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.005
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.5002026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=34.66987164671943->34.66987164671943
2026-02-24 15:31:46 | Reward (progress к objective): d_before=20.125, d_after=14.213, delta=5.912, norm=0.985, bonus=+0.030
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.075
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=-0.075, strength=0.000, objectives=0.000 (delta=0), total=-0.100
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.100
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (progress к objective): d_before=14.866, d_after=12.207, delta=2.660, norm=0.443, bonus=+0.013
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.060
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.060
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.060
2026-02-24 15:31:46 | Reward (progress к objective): d_before=32.202, d_after=25.318, delta=6.885, norm=1.147, bonus=+0.034
2026-02-24 15:31:46 | Reward (поражение): penalty=-2.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=None->None
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
271554554524->24.20743687382041
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.825424421026653->26.1725046566048
2026-02-24 15:31:46 | Reward (progress к objective): d_before=26.173, d_after=19.698, delta=6.475, norm=1.079, bonus=+0.032
�ление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.090 (norm=0.150)
2026-02-24 15:31:46 | Reward (бой): kill_term=+0.400 (delta=1)
x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.030
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.35755975068582->21.2602916254693
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.580
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.030
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.170
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.035
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.035
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:45 | [TRAIN][EP] ep=22 ep_reward=-0.082626 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=20.0 enemy_hp_total=18.0 model_vp=0 enemy_vp=3 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=23 steps=10 skip={move:3,attack:7,shoot:7,charge:7,use_cp:6,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.300,attack:0.700,shoot:0.700,charge:0.700,use_cp:0.600,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:13,without_targets:7}
2026-02-24 15:31:45 | [TRAIN][EP] ep=23 ep_reward=-0.035861 win=0 vp_diff=-3 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=15.0 enemy_hp_total=9.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=24 steps=10 skip={move:4,attack:9,shoot:10,charge:9,use_cp:5,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.400,attack:0.900,shoot:1.000,charge:0.900,use_cp:0.500,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:10,without_targets:10}
2026-02-24 15:31:45 | [TRAIN][EP] ep=24 ep_reward=-0.004018 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=18.0 enemy_hp_total=8.0 model_vp=0 enemy_vp=4 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=25 steps=10 skip={move:4,attack:16,shoot:9,charge:16,use_cp:3,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.400,attack:1.600,shoot:0.900,charge:1.600,use_cp:0.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:17,without_targets:9}
2026-02-24 15:31:45 | [TRAIN][EP] ep=25 ep_reward=-0.053407 win=0 vp_diff=-4 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=20.0 model_vp=0 enemy_vp=1 turn=9 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=26 steps=8 skip={move:3,attack:13,shoot:14,charge:13,use_cp:3,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.375,attack:1.625,shoot:1.750,charge:1.625,use_cp:0.375,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:13,without_targets:14}
2026-02-24 15:31:45 | [TRAIN][EP] ep=26 ep_reward=-0.310901 win=0 vp_diff=-1 end_reason=wipeout_model
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=9.0 enemy_hp_total=4.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=27 steps=10 skip={move:7,attack:13,shoot:12,charge:13,use_cp:2,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.700,attack:1.300,shoot:1.200,charge:1.300,use_cp:0.200,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:15,without_targets:12}
2026-02-24 15:31:45 | [TRAIN][EP] ep=27 ep_reward=0.105817 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=16.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=1 turn=8 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=28 steps=7 skip={move:6,attack:14,shoot:11,charge:14,use_cp:5,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.857,attack:2.000,shoot:1.571,charge:2.000,use_cp:0.714,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:16,without_targets:11}
2026-02-24 15:31:45 | [TRAIN][EP] ep=28 ep_reward=0.609617 win=1 vp_diff=-1 end_reason=wipeout_enemy
2026-02-24 15:31:45 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=19.0 model_vp=0 enemy_vp=1 turn=8 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=29 steps=7 skip={move:7,attack:18,shoot:13,charge:18,use_cp:5,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.000,attack:2.571,shoot:1.857,charge:2.571,use_cp:0.714,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:14,without_targets:13}
2026-02-24 15:31:45 | [TRAIN][EP] ep=29 ep_reward=-0.638405 win=0 vp_diff=-1 end_reason=wipeout_model
2026-02-24 15:31:45 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=10.0 enemy_hp_total=18.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=30 steps=10 skip={move:6,attack:16,shoot:13,charge:16,use_cp:5,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.600,attack:1.600,shoot:1.300,charge:1.600,use_cp:0.500,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:15,without_targets:13}
2026-02-24 15:31:45 | [TRAIN][EP] ep=30 ep_reward=0.032431 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:45 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=10 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=31 steps=9 skip={move:5,attack:14,shoot:12,charge:14,use_cp:2,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.556,attack:1.556,shoot:1.333,charge:1.556,use_cp:0.222,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:16,without_targets:12}
2026-02-24 15:31:45 | [TRAIN][EP] ep=31 ep_reward=-0.280516 win=0 vp_diff=0 end_reason=wipeout_model
2026-02-24 15:31:45 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=18.0 model_vp=3 enemy_vp=2 turn=10 battle_round=None
2026-02-24 15:31:45 | [TRAIN][ACTIONS] ep=32 steps=9 skip={move:3,attack:18,shoot:11,charge:18,use_cp:6,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.333,attack:2.000,shoot:1.222,charge:2.000,use_cp:0.667,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:18,without_targets:11}
2026-02-24 15:31:45 | [TRAIN][EP] ep=32 ep_reward=-0.302447 win=0 vp_diff=1 end_reason=wipeout_model
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=20.0 model_vp=0 enemy_vp=0 turn=10 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=33 steps=9 skip={move:3,attack:17,shoot:14,charge:17,use_cp:5,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.333,attack:1.889,shoot:1.556,charge:1.889,use_cp:0.556,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:15,without_targets:14}
2026-02-24 15:31:46 | [TRAIN][EP] ep=33 ep_reward=-0.264610 win=0 vp_diff=0 end_reason=wipeout_model
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=9.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=34 steps=10 skip={move:3,attack:16,shoot:7,charge:16,use_cp:12,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.300,attack:1.600,shoot:0.700,charge:1.600,use_cp:1.200,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:23,without_targets:7}
2026-02-24 15:31:46 | [TRAIN][EP] ep=34 ep_reward=0.066931 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=14.0 enemy_hp_total=14.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=35 steps=10 skip={move:3,attack:13,shoot:12,charge:13,use_cp:8,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.300,attack:1.300,shoot:1.200,charge:1.300,use_cp:0.800,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:18,without_targets:12}
2026-02-24 15:31:46 | [TRAIN][EP] ep=35 ep_reward=-0.108610 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=17.0 enemy_hp_total=8.0 model_vp=0 enemy_vp=2 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=36 steps=10 skip={move:4,attack:14,shoot:13,charge:14,use_cp:8,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.400,attack:1.400,shoot:1.300,charge:1.400,use_cp:0.800,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:17,without_targets:13}
2026-02-24 15:31:46 | [TRAIN][EP] ep=36 ep_reward=-0.042641 win=0 vp_diff=-2 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=16.0 model_vp=0 enemy_vp=0 turn=9 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=37 steps=8 skip={move:5,attack:20,shoot:17,charge:20,use_cp:3,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.625,attack:2.500,shoot:2.125,charge:2.500,use_cp:0.375,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:18,without_targets:17}
2026-02-24 15:31:46 | [TRAIN][EP] ep=37 ep_reward=-0.427615 win=0 vp_diff=0 end_reason=wipeout_model
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=18.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=2 turn=8 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=38 steps=7 skip={move:6,attack:16,shoot:15,charge:16,use_cp:3,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.857,attack:2.286,shoot:2.143,charge:2.286,use_cp:0.429,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:20,without_targets:15}
2026-02-24 15:31:46 | [TRAIN][EP] ep=38 ep_reward=0.679667 win=1 vp_diff=-2 end_reason=wipeout_enemy
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=14.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=39 steps=10 skip={move:7,attack:23,shoot:13,charge:23,use_cp:4,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.700,attack:2.300,shoot:1.300,charge:2.300,use_cp:0.400,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:23,without_targets:13}
2026-02-24 15:31:46 | [TRAIN][EP] ep=39 ep_reward=-0.249049 win=0 vp_diff=-1 end_reason=wipeout_model
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=10 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=40 steps=9 skip={move:6,attack:20,shoot:19,charge:20,use_cp:7,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.667,attack:2.222,shoot:2.111,charge:2.222,use_cp:0.778,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:18,without_targets:19}
2026-02-24 15:31:46 | [TRAIN][EP] ep=40 ep_reward=-0.183029 win=0 vp_diff=0 end_reason=wipeout_model
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=13.0 enemy_hp_total=11.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=41 steps=10 skip={move:9,attack:18,shoot:19,charge:18,use_cp:5,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.900,attack:1.800,shoot:1.900,charge:1.800,use_cp:0.500,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:18,without_targets:19}
2026-02-24 15:31:46 | [TRAIN][EP] ep=41 ep_reward=-0.003171 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=9.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=42 steps=10 skip={move:6,attack:17,shoot:17,charge:17,use_cp:6,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.600,attack:1.700,shoot:1.700,charge:1.700,use_cp:0.600,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:20,without_targets:17}
2026-02-24 15:31:46 | [TRAIN][EP] ep=42 ep_reward=0.090547 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=5.0 enemy_hp_total=15.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=43 steps=10 skip={move:10,attack:22,shoot:17,charge:22,use_cp:6,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.000,attack:2.200,shoot:1.700,charge:2.200,use_cp:0.600,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:20,without_targets:17}
2026-02-24 15:31:46 | [TRAIN][EP] ep=43 ep_reward=-0.044197 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.615528128088304->20.615528128088304
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.1245154965971->17.88854381999832
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=19.1049731745428->20.09975124224178
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.135
ors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.135, strength=0.000, objectives=0.000 (delta=0), total=0.135
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.2602916254693->None
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.135
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.027756377319946->18.439088914585774
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | Reward (progress к objective): d_before=26.173, d_after=21.954, delta=4.218, norm=0.703, bonus=+0.021
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=31.622776601683793->31.622776601683793
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (progress к objective): d_before=33.121, d_after=32.202, delta=0.919, norm=0.153, bonus=+0.005
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=26.571, d_after=21.932, delta=4.639, norm=0.773, bonus=+0.023
2026-02-24 15:31:46 | Reward (progress к objective): d_before=19.698, d_after=16.125, delta=3.573, norm=0.596, bonus=+0.018
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=18.439, d_after=18.439, d_best=7.439, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=6.00, norm=0.300, penalty=-0.150
ние): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.09975124224178->22.360679774997898
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=21.213, d_after=15.811, delta=5.402, norm=0.900, bonus=+0.027
=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=17.889, d_after=12.042, delta=5.847, norm=0.974, bonus=+0.029
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
00, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.120
ors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.200
ear_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.341664064126334->17.26267650163207
 total=0.580
2026-02-24 15:31:46 | Reward (progress к objective): d_before=21.024, d_after=17.000, delta=4.024, norm=0.671, bonus=+0.020
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.580
riors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (progress к objective): d_before=32.450, d_after=32.202, delta=0.247, norm=0.041, bonus=+0.001
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
30 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
.530
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:46 | Reward (progress к objective): d_before=21.954, d_after=18.601, delta=3.353, norm=0.559, bonus=+0.017
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.100 (norm=0.200)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.075
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.100 (norm=0.200, taken=4.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.035
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.035
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=27.295, d_after=27.295, d_best=16.295, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
lty=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=31.623, d_after=30.806, delta=0.817, norm=0.136, bonus=+0.004
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
=16.0312195418814->17.08800749063506
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.090, proximity=0.000, total=-0.090
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=15.811388300841896->19.6468827043885
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.590
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
�делей): Reward (стрельба): quality_bonus=+0.050
00, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.030
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x102026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.035
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрел2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.035
overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+02026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.220
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.015
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=-0.015, strength=0.000, objectives=0.000 (delta=0), total=0.015
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.015
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=6.325, d_after=6.325, d_best=0.000, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=28.071, d_after=28.071, d_best=17.071, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=17.26267650163207->17.26267650163207
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (progress к objective): d_before=19.209, d_after=13.892, delta=5.317, norm=0.886, bonus=+0.027
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.15549442140351->19.924858845171276
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.620
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.090, proximity=0.000, total=-0.090
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.439088914585774->19.313207915827967
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=17.088, d_after=16.125, delta=0.963, norm=0.161, bonus=+0.005
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.590
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (no2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.015
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
=17.11724276862369->19.72308292331602
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=-0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.040
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.040
riors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.160
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.027756377319946->18.027756377319946
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.160
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (progress к objective): d_before=17.029, d_after=15.264, delta=1.765, norm=0.294, bonus=+0.009
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=27.295, d_after=27.295, d_best=16.295, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=15.264, d_after=15.264, d_best=4.264, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (progress к objective): d_before=13.892, d_after=12.166, delta=1.727, norm=0.288, bonus=+0.009
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.1245154965971->16.492422502470642
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
.263, d_after=8.544, delta=8.719, norm=1.453, bonus=+0.044
9
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (no2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.110
a=+0.080
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
s (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (progress к objective): d_before=18.028, d_after=17.029, delta=0.998, norm=0.166, bonus=+0.005
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.060
2026-02-24 15:31:46 | Reward (progress к objective): d_before=19.313, d_after=18.974, delta=0.340, norm=0.057, bonus=+0.002
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=-0.060, strength=0.000, objectives=0.000 (delta=0), total=-0.060
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.060
riors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.340
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.730
2026-02-24 15:31:46 | Reward (progress к objective): d_before=19.723, d_after=19.235, delta=0.488, norm=0.081, bonus=+0.002
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=26.173, d_after=26.173, d_best=15.173, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=23.324, d_after=23.324, d_best=12.324, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=20.881, d_after=20.881, d_best=9.881, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=12.166, d_after=12.166, d_best=1.166, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=26.683, d_after=26.683, d_best=15.683, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=19.925, d_after=19.925, d_best=8.925, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.400
 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=18.974, d_after=18.974, d_best=7.974, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:46 | Reward (progress к objective): d_before=27.659, d_after=22.804, delta=4.855, norm=0.809, bonus=+0.024
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.210 (norm=0.350, dealt=7.00)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=15.264337522473747->17.88854381999832
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
EL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.210 (norm=0.350, dealt=7.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.260
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
 (x10 моделей): 2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
rm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.075 (norm=0.150)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.075
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.590
 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.075 (norm=0.150, taken=3.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=-0.015
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.075 (norm=0.150, taken=3.00), advantage=-0.075, strength=0.000, objectives=0.000 (delta=0), total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.015
2026-02-24 15:31:46 | Reward (progress к objective): d_before=16.492, d_after=10.770, delta=5.722, norm=0.954, bonus=+0.029
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.280
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
5.133, d_after=15.133, d_best=4.133, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=26.683, d_after=26.683, d_best=15.683, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=23.323807579381203->26.90724809414742
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=18.974, d_after=18.974, d_best=7.974, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=17.889, d_after=12.806, delta=5.082, norm=0.847, bonus=+0.025
us=+0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x102026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.170
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.570
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
000, overkill=-0.000, quality=0.050, ob2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
�оделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=15.132745950421556->15.132745950421556, hold_penalty_events=1
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): kill_bonus=+0.200
 dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x102026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.112026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.170, obj_damage=0.100, obj_kill=0.200, action=0.000, total=0.930
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.090
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.090, strength=0.000, objectives=0.000 (delta=0), total=-0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.740
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.110
2026-02-24 15:31:46 | Reward (progress к objective): d_before=10.770, d_after=10.050, delta=0.720, norm=0.120, bonus=+0.004
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=0.030
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.030
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+1.070
2026-02-24 15:31:46 | Reward (progress к objective): d_before=19.235, d_after=14.213, delta=5.023, norm=0.837, bonus=+0.025
2026-02-24 15:31:46 | Reward (progress к objective): d_before=12.166, d_after=8.246, delta=3.919, norm=0.653, bonus=+0.020
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=26.683, d_after=26.683, d_best=15.683, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=18.974, d_after=18.974, d_best=7.974, max_reach2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=0)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
 d_after=21.095, delta=5.812, norm=0.969, bonus=+0.029
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=14.213, d_after=10.817, delta=3.396, norm=0.566, bonus=+0.017
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
�ие delta=-0.240
2026-02-24 15:31:46 | Reward (progress к objective): d_before=12.806, d_after=10.050, delta=2.756, norm=0.459, bonus=+0.014
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=17.72004514666935->18.973665961010276
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=15.132745950421556->15.132745950421556
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.12026-02-24 15:31:46 | Reward (progress к objective): d_before=8.544, d_after=3.000, delta=5.544, norm=0.924, bonus=+0.028
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=19.925, d_after=19.026, delta=0.899, norm=0.150, bonus=+0.004
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.015
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=10.050, d_after=6.083, delta=3.967, norm=0.661, bonus=+0.020
, taken=1.00), advantage=-0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.010
2026-02-24 15:31:46 | Reward (progress к objective): d_before=23.431, d_after=21.095, delta=2.336, norm=0.389, bonus=+0.012
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.010
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.973665961010276->18.973665961010276, hold_penalty_events=2
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (командование): Insane Bravery bonus=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=17.464, d_after=17.464, d_best=6.464, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (шаг): командование delta=+0.500
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=19.6468827043885->23.53720459187964
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold=+0.500 (obj=0, dist=3.000)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.313708498984761->17.72004514666935
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.400
 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=0)
�к = -0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=21.095, d_after=14.866, delta=6.229, norm=1.038, bonus=+0.031
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=0.500, proximity=0.500, total=1.000
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.075
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=0)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.160
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.500
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=-0.075, strength=0.000, objectives=0.000 (delta=0), total=-0.100
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=18.028, d_after=13.416, delta=4.611, norm=0.769, bonus=+0.023
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
fter=3.162, delta=6.888, norm=1.148, bonus=+0.034
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (progress к objective): d_before=21.095, d_after=17.117, delta=3.978, norm=0.663, bonus=+0.020
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.973665961010276->18.973665961010276
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.090 (norm=0.150)
�оделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.090
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=6.082762530298219->7.211102550927978, hold_penalty_events=1
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.030
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.070
2026-02-24 15:31:46 | Reward (бой): damage=0.090 (norm=0.150, dealt=3.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.070
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.120
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.170
n=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (progress к objective): d_before=18.974, d_after=18.682, delta=0.292, norm=0.049, bonus=+0.001
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-24 15:31:46 | Reward (стрик удержания): streaks=[2], len=2, bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=17.117, d_after=17.117, d_best=6.117, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=12.530, d_after=12.530, d_best=1.530, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=22.672, d_after=22.672, d_best=11.672, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=17.464, d_after=17.464, d_best=6.464, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=21.541, d_after=21.541, d_best=10.541, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=27.019, d_after=27.019, d_best=16.019, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.973665961010276->19.924858845171276
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=23.537, d_after=23.022, delta=0.515, norm=0.086, bonus=+0.003
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
ld=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.620
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
, moved_closer=0, min_dist=22.67156809750927->22.67156809750927, hold_penalty_events=2
2026-02-24 15:31:46 | Reward (VP diff): prev=1, curr=2, delta=1, reward=+0.050, penalty=-0.000
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, total=0.280
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.570
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.570
_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.211102550927978->10.816653826391969, hold_penalty_events=1
2026-02-24 15:31:46 | Reward (progress к objective): d_before=18.682, d_after=13.000, delta=5.682, norm=0.947, bonus=+0.028
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=19.925, d_after=19.925, d_best=8.925, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)

2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=23.022, d_after=23.022, d_best=12.022, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=19.4164878389476->22.47220505424423
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.45584412271571->30.01666203960727
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=16.401, d_after=16.401, d_best=5.401, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.02379604162864->22.135943621178654
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=17.46424919657298->27.294688127912362
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.80350850198276->24.758836806279895
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
, damage=0.00, kills=0, moved_closer=0, min_dist=26.90724809414742->26.90724809414742
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.67156809750927->24.041630560342615
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.120
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.220
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.340
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.075
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.080
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.0->29.0
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=33.015, d_after=33.015, d_best=22.015, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.294688127912362->28.792360097775937
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=27.659, d_after=27.659, d_best=16.659, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=20.591, d_after=17.205, delta=3.387, norm=0.564, bonus=+0.017
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=22.472, d_after=18.439, delta=4.033, norm=0.672, bonus=+0.020
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба2026-02-24 15:31:46 | Reward (progress к objective): d_before=26.907, d_after=21.095, delta=5.812, norm=0.969, bonus=+0.029
2026-02-24 15:31:46 | Reward (progress к objective): d_before=17.720, d_after=11.180, delta=6.540, norm=1.090, bonus=+0.033
ty=-0.120 (obj=0, d_before=8.544, d_after=8.544, d_best=0.000, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.200, dealt=4.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.620
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.32026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.170
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.230
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.590
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (победа): bonus=+3.000
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=33.615, d_after=33.615, d_best=22.615, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=28.231, d_after=28.231, d_best=17.231, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=34.132, d_after=34.132, d_best=23.132, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=23.345, d_after=23.345, d_best=12.345, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=23.259, d_after=23.259, d_best=12.259, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=26.173, d_after=26.173, d_best=15.173, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
, damage=0.00, kills=0, moved_closer=0, min_dist=16.401219466856727->16.401219466856727
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
 d_after=21.000, delta=8.000, norm=1.333, bonus=+0.040
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=17.205, d_after=14.000, delta=3.205, norm=0.534, bonus=+0.016
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.09975124224178->20.09975124224178, hold_penalty_events=2
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
0, moved_closer=0, min_dist=23.259406699226016->23.259406699226016, hold_penalty_events=2
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.180339887498949->19.6468827043885
66048->26.1725046566048, hold_penalty_events=2
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.180 (norm=0.300, dealt=6.00)
.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.300, dealt=6.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.630
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.710
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=34.132, d_after=34.132, d_best=23.132, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=28.231, d_after=28.231, d_best=17.231, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=17.464, d_after=17.464, d_best=6.464, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=26.173, d_after=26.173, d_best=15.173, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=29.614, d_after=29.614, d_best=18.614, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=20.125, d_after=20.125, d_best=9.125, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=23.259, d_after=23.259, d_best=12.259, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
, damage=0.00, kills=0, moved_closer=0, min_dist=20.09975124224178->20.396078054371138
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
�): hold_penalty=-0.090 (obj=0, d_before=26.476, d_after=26.476, d_best=15.476, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=23.345235059857504->24.698178070456937
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
ld=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.130
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.120, strength=0.000, objectives=0.000 (delta=0), total=0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.210 (norm=0.350, dealt=7.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.120
a=+0.130
 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (progress к objective): d_before=21.000, d_after=15.000, delta=6.000, norm=1.000, bonus=+0.030
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=02026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
50, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=16.401,2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.633307652783937->21.633307652783937
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.210 (norm=0.350, dealt=7.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.660
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.310
 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=14.000, d_after=11.000, delta=3.000, norm=0.500, bonus=+0.015
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.220
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.220
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.830
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=15.811, d_after=13.153, delta=2.658, norm=0.443, bonus=+0.013
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.180 (norm=0.300, dealt=6.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=17.464, d_after=16.000, delta=1.464, norm=0.244, bonus=+0.007
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=0.060
2026-02-24 15:31:46 | Reward (progress к objective): d_before=13.454, d_after=12.207, delta=1.247, norm=0.208, bonus=+0.006
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
ьба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
�оделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.060
riors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.300, dealt=6.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.230
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.015
ors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
oved_closer=0, min_dist=23.259406699226016->29.732137494637012
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (progress к objective): d_before=20.396, d_after=20.100, delta=0.296, norm=0.049, bonus=+0.001
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.230
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.160
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=-0.015, strength=0.000, objectives=0.000 (delta=0), total=0.015
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.015
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.105
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.135
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.135
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.690
2026-02-24 15:31:46 | Reward (progress к objective): d_before=11.000, d_after=8.000, delta=3.000, norm=0.500, bonus=+0.015
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=12.207, d_after=12.207, d_best=1.207, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=12.728, d_after=12.728, d_best=1.728, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=8.0->10.0
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x102026-02-24 15:31:46 | [MODEL] Unit 22026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
ьба): damage_term=+0.030 (norm=0.050, dealt=1.00)
=21.633307652783937->22.20360331117452
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.0->16.76305461424021
2026-02-24 15:31:46 | Reward (победа): bonus=+3.000
y=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=15.0->15.811388300841896
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (no2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
s (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=29.732, d_after=27.659, delta=2.074, norm=0.346, bonus=+0.010
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.045
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.075
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.310
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.075
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.045
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.025
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.025
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=12.207, d_after=12.207, d_best=1.207, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=33.615, d_after=33.615, d_best=22.615, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=27.659, d_after=27.659, d_best=16.659, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=30.232, d_after=30.232, d_best=19.232, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=15.811388300841896->15.811388300841896
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.090, proximity=0.000, total=-0.090
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=30.414, d_after=30.414, d_best=19.414, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | Reward (progress к objective): d_before=17.464, d_after=16.000, delta=1.464, norm=0.244, bonus=+0.007
us=+0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.045
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.045
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.045
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.0->25.0
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=02026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
0
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=0.045
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.220
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.045
riors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.220
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.530
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.180 (norm=0.300, dealt=6.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
50, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.300, dealt=6.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.230
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.310
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.340
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.015
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.075
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=-0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.010
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.105
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.010
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.105
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
lty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.0->16.0
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=26.173, d_after=26.173, d_best=15.173, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=10.000, d_after=6.083, delta=3.917, norm=0.653, bonus=+0.020
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=15.811388300841896->23.53720459187964
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.620
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=9.434, d_after=5.099, delta=4.335, norm=0.722, bonus=+0.022
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.0->26.832815729997478
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.075
orm=0.100)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.135
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warri2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.135
050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.010
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.010
riors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
ьба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.065
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.530
2026-02-24 15:31:46 | Reward (progress к objective): d_before=12.207, d_after=7.616, delta=4.591, norm=0.765, bonus=+0.023
90 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.590
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=27.893, d_after=27.074, delta=0.819, norm=0.136, bonus=+0.004
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.060
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.060
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.060
2026-02-24 15:31:46 | Reward (progress к objective): d_before=22.804, d_after=18.788, delta=4.015, norm=0.669, bonus=+0.020
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
er=31.906, d_best=20.906, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
er=20.248, d_best=9.248, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.102 (obj=0, d_before=5.099, d_after=5.099, d_best=0.000, max_reach=11.000, could_reach_objective=1, severity=0.850, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=23.537, d_after=23.537, d_best=12.537, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=31.623, d_after=31.623, d_best=20.623, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=16.000, d_after=16.000, d_best=5.000, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
, damage=0.00, kills=0, moved_closer=0, min_dist=6.082762530298219->8.48528137423857
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
, damage=0.00, kills=0, moved_closer=0, min_dist=20.0->20.8806130178211
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.518284528683193->22.80350850198276
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
=18.788294228055936->21.400934559032695
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.060
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=31.064449134018133->31.622776601683793
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.060
, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.060
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
00, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_chan2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.200 (dealt=4.00)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.200, obj_kill=0.000, action=0.000, total=0.440
2026-02-24 15:31:46 | Reward (progress к objective): d_before=27.074, d_after=22.091, delta=4.983, norm=0.831, bonus=+0.025
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.440
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.670
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (progress к objective): d_before=25.612, d_after=23.854, delta=1.759, norm=0.293, bonus=+0.009
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=22.804, d_after=22.804, d_best=11.804, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=7.615773105863909->7.615773105863909
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=0.030
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.0990195135927845->10.04987562112089
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.090
=27.731, d_after=24.759, delta=2.972, norm=0.495, bonus=+0.015
us=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
oved_closer=0, min_dist=8.48528137423857->8.48528137423857
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron War2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.8806130178211->23.021728866442675
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.120
, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=31.064449134018133->31.622776601683793
_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.120
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.075
2026-02-24 15:31:46 | Reward (progress к objective): d_before=16.000, d_after=15.033, delta=0.967, norm=0.161, bonus=+0.005
2026-02-24 15:31:46 | Reward (progress к objective): d_before=23.537, d_after=21.587, delta=1.950, norm=0.325, bonus=+0.010
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.080
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.080
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (progress к objective): d_before=22.804, d_after=19.698, delta=3.106, norm=0.518, bonus=+0.016
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=15.0 model_vp=0 enemy_vp=1 turn=9 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=44 steps=8 skip={move:5,attack:20,shoot:17,charge:20,use_cp:8,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.625,attack:2.500,shoot:2.125,charge:2.500,use_cp:1.000,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:21,without_targets:17}
2026-02-24 15:31:46 | [TRAIN][EP] ep=44 ep_reward=-0.377473 win=0 vp_diff=-1 end_reason=wipeout_model
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=18.0 enemy_hp_total=3.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=45 steps=10 skip={move:4,attack:23,shoot:15,charge:23,use_cp:9,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.400,attack:2.300,shoot:1.500,charge:2.300,use_cp:0.900,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:24,without_targets:15}
2026-02-24 15:31:46 | [TRAIN][EP] ep=45 ep_reward=-0.174666 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=9.0 enemy_hp_total=12.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=46 steps=10 skip={move:4,attack:23,shoot:21,charge:23,use_cp:6,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.400,attack:2.300,shoot:2.100,charge:2.300,use_cp:0.600,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:18,without_targets:21}
2026-02-24 15:31:46 | [TRAIN][EP] ep=46 ep_reward=-0.254850 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=4.0 enemy_hp_total=7.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=47 steps=10 skip={move:5,attack:22,shoot:11,charge:22,use_cp:13,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.500,attack:2.200,shoot:1.100,charge:2.200,use_cp:1.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:29,without_targets:11}
2026-02-24 15:31:46 | [TRAIN][EP] ep=47 ep_reward=0.015807 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=14.0 enemy_hp_total=13.0 model_vp=0 enemy_vp=2 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=48 steps=10 skip={move:5,attack:15,shoot:17,charge:15,use_cp:10,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.500,attack:1.500,shoot:1.700,charge:1.500,use_cp:1.000,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:23,without_targets:17}
2026-02-24 15:31:46 | [TRAIN][EP] ep=48 ep_reward=0.056762 win=0 vp_diff=-2 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=17.0 enemy_hp_total=7.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=49 steps=10 skip={move:7,attack:29,shoot:22,charge:29,use_cp:6,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.700,attack:2.900,shoot:2.200,charge:2.900,use_cp:0.600,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:23,without_targets:22}
2026-02-24 15:31:46 | [TRAIN][EP] ep=49 ep_reward=-0.161076 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=13.0 enemy_hp_total=16.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=50 steps=10 skip={move:6,attack:19,shoot:20,charge:19,use_cp:3,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.600,attack:1.900,shoot:2.000,charge:1.900,use_cp:0.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:25,without_targets:20}
2026-02-24 15:31:46 | [TRAIN][EP] ep=50 ep_reward=-0.007026 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=6.0 enemy_hp_total=15.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=51 steps=10 skip={move:8,attack:28,shoot:18,charge:28,use_cp:7,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.800,attack:2.800,shoot:1.800,charge:2.800,use_cp:0.700,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:28,without_targets:18}
2026-02-24 15:31:46 | [TRAIN][EP] ep=51 ep_reward=0.028123 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=20.0 enemy_hp_total=8.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=52 steps=10 skip={move:8,attack:28,shoot:21,charge:28,use_cp:10,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.800,attack:2.800,shoot:2.100,charge:2.800,use_cp:1.000,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:26,without_targets:21}
2026-02-24 15:31:46 | [TRAIN][EP] ep=52 ep_reward=-0.005416 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=3.0 enemy_hp_total=17.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=53 steps=10 skip={move:10,attack:23,shoot:24,charge:23,use_cp:9,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.000,attack:2.300,shoot:2.400,charge:2.300,use_cp:0.900,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:23,without_targets:24}
2026-02-24 15:31:46 | [TRAIN][EP] ep=53 ep_reward=0.012821 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=17.0 enemy_hp_total=6.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=54 steps=10 skip={move:7,attack:21,shoot:22,charge:21,use_cp:7,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.700,attack:2.100,shoot:2.200,charge:2.100,use_cp:0.700,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:25,without_targets:22}
2026-02-24 15:31:46 | [TRAIN][EP] ep=54 ep_reward=0.058962 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=model winner_env=None model_hp_total=9.0 enemy_hp_total=8.0 model_vp=1 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=55 steps=10 skip={move:12,attack:28,shoot:21,charge:28,use_cp:7,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.200,attack:2.800,shoot:2.100,charge:2.800,use_cp:0.700,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:26,without_targets:21}
2026-02-24 15:31:46 | [TRAIN][EP] ep=55 ep_reward=0.022753 win=1 vp_diff=1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=19.0 enemy_hp_total=13.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=56 steps=10 skip={move:8,attack:27,shoot:21,charge:27,use_cp:8,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.800,attack:2.700,shoot:2.100,charge:2.700,use_cp:0.800,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:27,without_targets:21}
2026-02-24 15:31:46 | [TRAIN][EP] ep=56 ep_reward=-0.017642 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=model winner_env=None model_hp_total=17.0 enemy_hp_total=12.0 model_vp=2 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=57 steps=10 skip={move:6,attack:31,shoot:18,charge:31,use_cp:9,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.600,attack:3.100,shoot:1.800,charge:3.100,use_cp:0.900,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:31,without_targets:18}
2026-02-24 15:31:46 | [TRAIN][EP] ep=57 ep_reward=0.156118 win=1 vp_diff=2 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=10.0 enemy_hp_total=17.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=58 steps=10 skip={move:6,attack:29,shoot:23,charge:29,use_cp:6,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.600,attack:2.900,shoot:2.300,charge:2.900,use_cp:0.600,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:26,without_targets:23}
2026-02-24 15:31:46 | [TRAIN][EP] ep=58 ep_reward=-0.105313 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=17.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=0 turn=10 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=59 steps=9 skip={move:7,attack:22,shoot:20,charge:22,use_cp:11,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.778,attack:2.444,shoot:2.222,charge:2.444,use_cp:1.222,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:29,without_targets:20}
2026-02-24 15:31:46 | [TRAIN][EP] ep=59 ep_reward=0.490499 win=1 vp_diff=0 end_reason=wipeout_enemy
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=6.0 enemy_hp_total=6.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=60 steps=10 skip={move:6,attack:29,shoot:14,charge:29,use_cp:15,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.600,attack:2.900,shoot:1.400,charge:2.900,use_cp:1.500,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:36,without_targets:14}
2026-02-24 15:31:46 | [TRAIN][EP] ep=60 ep_reward=0.016218 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=15.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=1 turn=9 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=61 steps=8 skip={move:7,attack:24,shoot:21,charge:24,use_cp:4,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.875,attack:3.000,shoot:2.625,charge:3.000,use_cp:0.500,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:32,without_targets:21}
2026-02-24 15:31:46 | [TRAIN][EP] ep=61 ep_reward=0.415537 win=1 vp_diff=-1 end_reason=wipeout_enemy
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=19.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=0 turn=8 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=62 steps=7 skip={move:10,attack:32,shoot:21,charge:32,use_cp:9,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.429,attack:4.571,shoot:3.000,charge:4.571,use_cp:1.286,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:32,without_targets:21}
2026-02-24 15:31:46 | [TRAIN][EP] ep=62 ep_reward=0.630847 win=1 vp_diff=0 end_reason=wipeout_enemy
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=12.0 enemy_hp_total=5.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=63 steps=10 skip={move:9,attack:33,shoot:29,charge:33,use_cp:8,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.900,attack:3.300,shoot:2.900,charge:3.300,use_cp:0.800,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:26,without_targets:29}
2026-02-24 15:31:46 | [TRAIN][EP] ep=63 ep_reward=0.046758 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=16.0 enemy_hp_total=8.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=64 steps=10 skip={move:9,attack:36,shoot:25,charge:36,use_cp:13,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.900,attack:3.600,shoot:2.500,charge:3.600,use_cp:1.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:32,without_targets:25}
2026-02-24 15:31:46 | [TRAIN][EP] ep=64 ep_reward=-0.133842 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=13.0 enemy_hp_total=4.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=19.698, d_after=19.698, d_best=8.698, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=0)
closer=0, min_dist=15.033296378372908->15.033296378372908
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.238858928247925->25.238858928247925
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.758836806279895->24.758836806279895
2026-02-24 15:31:46 | Reward (progress к objective): d_before=27.295, d_after=27.019, delta=0.276, norm=0.046, bonus=+0.001
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.76305461424021->25.495097567963924
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.015
age_taken=2.00, norm=0.100, penalty=-0.050
ьба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.180 (norm=0.300, dealt=6.00)
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=-0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.015
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=15.033296378372908->17.0
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=7.616, d_after=4.243, delta=3.373, norm=0.562, bonus=+0.017
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.300, dealt=6.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.230
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=23.853720883753127->23.853720883753127
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.230
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.170
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.250
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.075 (norm=0.150)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.075
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.075 (norm=0.150, taken=3.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.060
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.105
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.060
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.135
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.135
2026-02-24 15:31:46 | Reward (progress к objective): d_before=19.698, d_after=16.031, delta=3.666, norm=0.611, bonus=+0.018
2026-02-24 15:31:46 | Reward (progress к objective): d_before=21.587, d_after=18.682, delta=2.905, norm=0.484, bonus=+0.015
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=23.022, d_after=23.022, d_best=12.022, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=16.031, d_after=16.031, d_best=5.031, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=24.207, d_after=24.207, d_best=13.207, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.495097567963924->27.459060435491963
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_cha2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.495097567963924->29.154759474226502
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=4.242640687119285->5.830951894845301
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.0312195418814->16.0312195418814, hold_penalty_events=1
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (progress к objective): d_before=24.759, d_after=20.591, delta=4.168, norm=0.695, bonus=+0.021
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.090
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.160
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.065
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.065
a=+0.270
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=6.083, d_after=6.083, d_best=0.000, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=30.529, d_after=30.529, d_best=19.529, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=28.460, d_after=28.460, d_best=17.460, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=19.416, d_after=19.416, d_best=8.416, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.075
-0.120
ear_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.076809620810597->29.068883707497267
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=21.024, d_after=16.553, delta=4.471, norm=0.745, bonus=+0.022
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.154759474226502->30.083217912982647
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
, strength=0.000, objectives=0.000 (delta=0), total=-0.075
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): движение delt2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=17.029386365926403->19.72308292331602

2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
trol_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=5.830951894845301->5.830951894845301
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.459060435491963->28.635642126552707
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.250 (dealt=5.00)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.090 (norm=0.150)
�оделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.250, obj_kill=0.000, action=0.000, total=0.520
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.075
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage=0.090 (norm=0.150, dealt=3.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.165
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.165
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.250
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-24 15:31:46 | Reward (progress к objective): d_before=17.205, d_after=13.454, delta=3.751, norm=0.625, bonus=+0.019
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.720
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.015
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.035
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.035
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=6.083, d_after=1.414, delta=4.669, norm=0.778, bonus=+0.023
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (командование): Insane Bravery bonus=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=27.000, d_after=27.000, d_best=16.000, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=30.887, d_after=30.887, d_best=19.887, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): командование delta=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=29.833, d_after=29.833, d_best=18.833, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
ld=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=28.636, d_after=28.071, delta=0.564, norm=0.094, bonus=+0.003
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.0->24.0
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.0->27.0, hold_penalty_events=2
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
ld=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
ьба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (progress к objective): d_before=28.460, d_after=27.166, delta=1.294, norm=0.216, bonus=+0.006
2026-02-24 15:31:46 | Reward (VP diff): prev=-1, curr=-2, delta=-1,2026-02-24 15:31:46 | Reward (progress к objective): d_before=29.428, d_after=23.537, delta=5.891, norm=0.982, bonus=+0.029
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
 d_after=17.263, delta=2.460, norm=0.410, bonus=+0.012
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=1.4142135623730951->6.082762530298219
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.400 (delta=1), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.550
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.550
2026-02-24 15:31:46 | Reward (progress к objective): d_before=18.682, d_after=18.000, delta=0.682, norm=0.114, bonus=+0.003
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-24 15:31:46 | Reward (progress к objective): d_before=16.553, d_after=15.652, delta=0.900, norm=0.150, bonus=+0.005
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.0->29.5296461204668
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=-0.025
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.015
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.015
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.0->22.0
 objectives=0.000 (delta=0), total=0.015
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=-0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.040
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.015
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | Reward (VP diff): prev=-2, curr=-3, delta=-1, reward=+0.000, penalty=-0.050
�рельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
00, norm=0.050, penalty=-0.025
ьба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=28.071, d_after=21.024, delta=7.048, norm=1.175, bonus=+0.035
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.075
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.075, strength=0.000, objectives=0.000 (delta=0), total=-0.095
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.280
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.095
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=29.530, d_after=29.530, d_best=18.530, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=19.209, d_after=19.209, d_best=8.209, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=29.017, d_after=29.017, d_best=18.017, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=19.105, d_after=19.105, d_best=8.105, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.93171219946131->26.248809496813376
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=23.770, d_after=14.318, delta=9.452, norm=1.575, bonus=+0.047
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.0->22.561028345356956
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.02379604162864->21.840329667841555
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.017236257093817->29.017236257093817, hold_penalty_events=2
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.170
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=-0.060, strength=0.000, objectives=0.000 (delta=0), total=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-2026-022026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
елей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=28.071, d_after=27.659, delta=0.413, norm=0.069, bonus=+0.002
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.220
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): kill_term=+0.400 (delta=1)
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.105
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.400 (delta=1), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.510
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.510
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
2026-02-24 15:31:46 | Reward (progress к objective): d_before=23.707, d_after=18.248, delta=5.458, norm=0.910, bonus=+0.027
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
er=28.844, d_best=17.844, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=23.770, d_after=23.770, d_best=12.770, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=26.306, d_after=26.306, d_best=15.306, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
otal=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=20.125, d_after=20.125, d_best=9.125, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.0->28.460498941515414
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.620
 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.30589287593181->26.30589287593181, hold_penalty_events=2
al=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x102026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (progress к objective): d_before=19.105, d_after=16.553, delta=2.552, norm=0.425, bonus=+0.013
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.200
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=28.844, d_after=28.844, d_best=17.844, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя pena2026-02-24 12026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
�й): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=28.160, d_after=28.160, d_best=17.160, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=28.160, d_after=28.160, d_best=17.160, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=26.306, d_after=26.306, d_best=15.306, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=23.769728648009426->26.419689627245813
2026-02-24 15:31:46 | Reward (progress к objective): d_before=31.623, d_after=28.231, delta=3.392, norm=0.565, bonus=+0.017
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=29.547, d_after=25.060, delta=4.487, norm=0.748, bonus=+0.022
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.105
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.30589287593181->26.30589287593181, hold_penalty_events=2
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.105, str2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.12461179749811->24.515301344262525
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.130
2026-02-24 15:31:46 | Reward (progress к objective): d_before=26.249, d_after=20.809, delta=5.440, norm=0.907, bonus=+0.027
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.130
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=16.553, d_after=15.133, delta=1.420, norm=0.237, bonus=+0.007
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.280
 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.015
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.280
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=0.020
2026-02-24 15:31:46 | Reward (progress к objective): d_before=28.460, d_after=27.459, delta=1.001, norm=0.167, bonus=+0.005
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.020
riors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.075
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.075, strength=0.000, objectives=0.000 (delta=0), total=-0.095
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.370
2026-02-24 15:31:46 | Reward (progress к objective): d_before=29.275, d_after=22.023, delta=7.252, norm=1.209, bonus=+0.036
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.095
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (VP diff): prev=-4, curr=-5, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=16.031, d_after=13.038, delta=2.993, norm=0.499, bonus=+0.015
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=None->None
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=29.411, d_after=28.018, delta=1.393, norm=0.232, bonus=+0.007
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
ьба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.180 (norm=0.300, dealt=6.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=25.060, d_after=21.633, delta=3.427, norm=0.571, bonus=+0.017
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
26-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
=-0.000 (norm=0.000, taken=0.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.135
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warri2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.038404810405298->13.601470508735444
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.105, strength=0.000, objectives=0.000 (delta=0), total=-0.155
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.30589287593181->28.442925306655784
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.300, dealt=6.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.630
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.155
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.560
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.630
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.560
 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.419689627245813->26.419689627245813
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.700
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=-0.025
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=21.633, d_after=21.633, d_best=10.633, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (победа): bonus=+3.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=23.022, d_after=23.022, d_best=12.022, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (поражение): penalty=-2.000
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.1245154965971->16.1245154965971
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
, damage=0.00, kills=0, moved_closer=0, min_dist=None->None
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.02271554554524->25.45584412271571
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=19.697715603592208->27.202941017470888
_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
ear_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.400934559032695->22.02271554554524
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.601470508735444->15.811388300841896
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=28.653097563788805->30.0
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.250
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=28.443, d_after=28.160, delta=0.283, norm=0.047, bonus=+0.001
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.015
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=-0.035
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.035
2026-02-24 15:31:46 | Reward (progress к objective): d_before=21.633, d_after=14.318, delta=7.315, norm=1.219, bonus=+0.037
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=29.155, d_after=29.155, d_best=18.155, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=28.601, d_after=22.672, delta=5.929, norm=0.988, bonus=+0.030
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=28.460, d_after=28.460, d_best=17.460, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.45584412271571->26.1725046566048
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
трельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=30.000, d_after=29.206, delta=0.794, norm=0.132, bonus=+0.004
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.027756377319946->19.313207915827967
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.92582403567252->28.160255680657446
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=28.284271247461902->29.154759474226502
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (progress к objective): d_before=14.318, d_after=9.487, delta=4.831, norm=0.805, bonus=+0.024
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=28.460498941515414->28.460498941515414, hold_penalty_events=2
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (поражение): penalty=-2.000
2026-02-24 15:31:46 | Reward (поражение): penalty=-2.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=None->None
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=31.623, d_after=31.623, d_best=20.623, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=None->None
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.67156809750927->22.67156809750927
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.486832980505138->9.486832980505138
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=24.207, d_after=24.207, d_best=13.207, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=28.460498941515414->30.4138126514911
2026-02-24 15:31:46 | Reward (progress к objective): d_before=29.155, d_after=29.069, delta=0.086, norm=0.014, bonus=+0.000
за пропуск = -0.200
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=19.0->20.0
2026-02-24 15:31:46 | Reward (progress к objective): d_before=29.155, d_after=21.954, delta=7.200, norm=1.200, bonus=+0.036
2026-02-24 15:31:46 | Reward (progress к objective): d_before=27.295, d_after=23.345, delta=3.949, norm=0.658, bonus=+0.020
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=28.460, d_after=27.295, delta=1.166, norm=0.194, bonus=+0.006
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.400
_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.20743687382041->24.20743687382041, hold_penalty_events=2
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=19.313207915827967->21.633307652783937
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=25.000, d_after=25.000, d_best=14.000, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=30.4138126514911->30.4138126514911
2026-02-24 15:31:46 | Reward (progress к objective): d_before=26.401, d_after=21.840, delta=4.560, norm=0.760, bonus=+0.023
2026-02-24 15:31:46 | Reward (progress к objective): d_before=14.142, d_after=11.180, delta=2.962, norm=0.494, bonus=+0.015
ty=-0.090 (obj=0, d_before=21.633, d_after=21.633, d_best=10.633, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
ear_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.1725046566048->26.870057685088806
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=9.486832980505138->9.486832980505138
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=24.207, d_after=20.616, delta=3.592, norm=0.599, bonus=+0.018
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
ll=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (progress к objective): d_before=22.672, d_after=18.601, delta=4.070, norm=0.678, bonus=+0.020
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.090
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | Reward (progress к objective): d_before=23.345, d_after=23.022, delta=0.324, norm=0.054, bonus=+0.002
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.090
riors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
oved_closer=0, min_dist=29.068883707497267->29.068883707497267
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:46 | Reward (progress к objective): d_before=21.954, d_after=19.925, delta=2.030, norm=0.338, bonus=+0.010
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.180 (norm=0.300, dealt=6.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.300, dealt=6.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.230
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.340
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=26.833, d_after=26.833, d_best=15.833, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=30.414, d_after=30.414, d_best=19.414, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=23.601, d_after=23.601, d_best=12.601, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
ьба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.840329667841555->27.294688127912362
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.633307652783937->28.0178514522438
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=29.068883707497267->29.832867780352597
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=30.4138126514911->30.4138126514911, hold_penalty_events=2
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.620
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (progress к objective): d_before=9.487, d_after=5.000, delta=4.487, norm=0.748, bonus=+0.022
onus=+0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
.229, bonus=+0.007
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (progress к objective): d_before=23.022, d_after=17.029, delta=5.992, norm=0.999, bonus=+0.030
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (progress к objective): d_before=11.180, d_after=8.246, delta=2.934, norm=0.489, bonus=+0.015
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.160
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=30.806, d_after=30.806, d_best=19.806, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=30.414, d_after=30.414, d_best=19.414, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=15.000, d_after=15.000, d_best=4.000, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=17.889, d_after=17.889, d_best=6.889, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
46, d_after=8.246, d_best=0.000, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): proximity=+0.500 (obj=0)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
�ы, движение): hold=0.000, proximity=0.500, total=0.500
2026-02-24 15:31:46 | Reward (progress к objective): d_before=19.925, d_after=19.235, delta=0.689, norm=0.115, bonus=+0.003
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.500
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=30.4138126514911->30.4138126514911, hold_penalty_events=2
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.170
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
00, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warri2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.060
 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.250, dealt=5.00)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.400 (delta=1), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.135, strength=0.000, objectives=0.000 (delta=0), total=0.565
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
00, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.565
2026-02-24 15:31:46 | Reward (progress к objective): d_before=27.295, d_after=26.000, delta=1.295, norm=0.216, bonus=+0.006
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.250
 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=28.018, d_after=27.074, delta=0.944, norm=0.157, bonus=+0.005
2026-02-24 15:31:46 | Reward (progress к objective): d_before=24.083, d_after=23.601, delta=0.482, norm=0.080, bonus=+0.002
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.280
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=-0.075, strength=0.000, objectives=0.000 (delta=0), total=-0.100
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
ьба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.600
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=1, delta=1, reward=+0.050, penalty=-0.000
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.740
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.090
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.090
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.090
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=30.871, d_after=30.871, d_best=19.871, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=20.000, d_after=20.000, d_best=9.000, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=21.000, d_after=21.000, d_best=10.000, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.090 (norm=0.150)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=30.414, d_after=30.000, delta=0.414, norm=0.069, bonus=+0.002
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
00, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.12026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
 из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warri2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.105, strength=0.000, objectives=0.000 (delta=0), total=0.165
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.170
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | Reward (progress к objective): d_before=17.889, d_after=13.601, delta=4.287, norm=0.715, bonus=+0.021
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.165
ta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=31.305, d_after=30.414, delta=0.891, norm=0.149, bonus=+0.004
2026-02-24 15:31:46 | Reward (progress к objective): d_before=26.000, d_after=24.515, delta=1.485, norm=0.247, bonus=+0.007
2026-02-24 15:31:46 | Reward (progress к objective): d_before=20.591, d_after=18.682, delta=1.910, norm=0.318, bonus=+0.010
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.220
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=65 steps=10 skip={move:10,attack:31,shoot:27,charge:31,use_cp:10,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.000,attack:3.100,shoot:2.700,charge:3.100,use_cp:1.000,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:30,without_targets:27}
2026-02-24 15:31:46 | [TRAIN][EP] ep=65 ep_reward=0.114754 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=15.0 enemy_hp_total=14.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=66 steps=10 skip={move:11,attack:26,shoot:27,charge:26,use_cp:10,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.100,attack:2.600,shoot:2.700,charge:2.600,use_cp:1.000,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:30,without_targets:27}
2026-02-24 15:31:46 | [TRAIN][EP] ep=66 ep_reward=-0.227000 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=16.0 enemy_hp_total=2.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=67 steps=10 skip={move:12,attack:34,shoot:25,charge:34,use_cp:9,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.200,attack:3.400,shoot:2.500,charge:3.400,use_cp:0.900,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:32,without_targets:25}
2026-02-24 15:31:46 | [TRAIN][EP] ep=67 ep_reward=0.022914 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=18.0 enemy_hp_total=1.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=68 steps=10 skip={move:9,attack:34,shoot:22,charge:34,use_cp:10,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.900,attack:3.400,shoot:2.200,charge:3.400,use_cp:1.000,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:36,without_targets:22}
2026-02-24 15:31:46 | [TRAIN][EP] ep=68 ep_reward=0.057671 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=8.0 enemy_hp_total=8.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=69 steps=10 skip={move:7,attack:36,shoot:23,charge:36,use_cp:13,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.700,attack:3.600,shoot:2.300,charge:3.600,use_cp:1.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:36,without_targets:23}
2026-02-24 15:31:46 | [TRAIN][EP] ep=69 ep_reward=0.095528 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=16.0 enemy_hp_total=6.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=70 steps=10 skip={move:10,attack:35,shoot:27,charge:35,use_cp:9,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.000,attack:3.500,shoot:2.700,charge:3.500,use_cp:0.900,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:32,without_targets:27}
2026-02-24 15:31:46 | [TRAIN][EP] ep=70 ep_reward=0.058107 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=7.0 enemy_hp_total=6.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=71 steps=10 skip={move:12,attack:28,shoot:25,charge:28,use_cp:12,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.200,attack:2.800,shoot:2.500,charge:2.800,use_cp:1.200,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:34,without_targets:25}
2026-02-24 15:31:46 | [TRAIN][EP] ep=71 ep_reward=0.000618 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=4.0 enemy_hp_total=17.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=72 steps=10 skip={move:9,attack:32,shoot:17,charge:32,use_cp:16,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.900,attack:3.200,shoot:1.700,charge:3.200,use_cp:1.600,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:43,without_targets:17}
2026-02-24 15:31:46 | [TRAIN][EP] ep=72 ep_reward=0.082740 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=9.0 enemy_hp_total=12.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=73 steps=10 skip={move:9,attack:26,shoot:25,charge:26,use_cp:4,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.900,attack:2.600,shoot:2.500,charge:2.600,use_cp:0.400,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:38,without_targets:25}
2026-02-24 15:31:46 | [TRAIN][EP] ep=73 ep_reward=0.246769 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=8.0 enemy_hp_total=9.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=74 steps=10 skip={move:11,attack:39,shoot:26,charge:39,use_cp:10,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.100,attack:3.900,shoot:2.600,charge:3.900,use_cp:1.000,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:37,without_targets:26}
2026-02-24 15:31:46 | [TRAIN][EP] ep=74 ep_reward=-0.121770 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=14.0 enemy_hp_total=3.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=75 steps=10 skip={move:10,attack:38,shoot:31,charge:38,use_cp:10,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.000,attack:3.800,shoot:3.100,charge:3.800,use_cp:1.000,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:34,without_targets:31}
2026-02-24 15:31:46 | [TRAIN][EP] ep=75 ep_reward=0.102226 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=19.0 model_vp=0 enemy_vp=2 turn=10 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=76 steps=9 skip={move:10,attack:35,shoot:30,charge:35,use_cp:11,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.111,attack:3.889,shoot:3.333,charge:3.889,use_cp:1.222,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:36,without_targets:30}
2026-02-24 15:31:46 | [TRAIN][EP] ep=76 ep_reward=-0.304998 win=0 vp_diff=-2 end_reason=wipeout_model
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=12.0 enemy_hp_total=4.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=77 steps=10 skip={move:9,attack:42,shoot:29,charge:42,use_cp:16,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.900,attack:4.200,shoot:2.900,charge:4.200,use_cp:1.600,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:38,without_targets:29}
2026-02-24 15:31:46 | [TRAIN][EP] ep=77 ep_reward=0.081613 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=7.0 enemy_hp_total=19.0 model_vp=0 enemy_vp=5 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=78 steps=10 skip={move:12,attack:32,shoot:33,charge:32,use_cp:11,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.200,attack:3.200,shoot:3.300,charge:3.200,use_cp:1.100,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:34,without_targets:33}
2026-02-24 15:31:46 | [TRAIN][EP] ep=78 ep_reward=-0.092694 win=0 vp_diff=-5 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=15.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=0 turn=9 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=79 steps=8 skip={move:11,attack:43,shoot:29,charge:43,use_cp:10,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.375,attack:5.375,shoot:3.625,charge:5.375,use_cp:1.250,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:38,without_targets:29}
2026-02-24 15:31:46 | [TRAIN][EP] ep=79 ep_reward=0.373340 win=1 vp_diff=0 end_reason=wipeout_enemy
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=12.0 enemy_hp_total=14.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=80 steps=10 skip={move:13,attack:41,shoot:28,charge:41,use_cp:11,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.300,attack:4.100,shoot:2.800,charge:4.100,use_cp:1.100,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:39,without_targets:28}
2026-02-24 15:31:46 | [TRAIN][EP] ep=80 ep_reward=-0.220137 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=10 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=81 steps=9 skip={move:11,attack:38,shoot:27,charge:38,use_cp:11,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.222,attack:4.222,shoot:3.000,charge:4.222,use_cp:1.222,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:40,without_targets:27}
2026-02-24 15:31:46 | [TRAIN][EP] ep=81 ep_reward=-0.095917 win=0 vp_diff=0 end_reason=wipeout_model
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=10 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=82 steps=9 skip={move:10,attack:36,shoot:24,charge:36,use_cp:18,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.111,attack:4.000,shoot:2.667,charge:4.000,use_cp:2.000,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:45,without_targets:24}
2026-02-24 15:31:46 | [TRAIN][EP] ep=82 ep_reward=-0.218193 win=0 vp_diff=0 end_reason=wipeout_model
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=2 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=83 steps=10 skip={move:8,attack:43,shoot:28,charge:43,use_cp:14,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:0.800,attack:4.300,shoot:2.800,charge:4.300,use_cp:1.400,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:41,without_targets:28}
2026-02-24 15:31:46 | [TRAIN][EP] ep=83 ep_reward=-0.314102 win=0 vp_diff=-2 end_reason=wipeout_model
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=17.0 enemy_hp_total=8.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=84 steps=10 skip={move:14,attack:35,shoot:28,charge:35,use_cp:14,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.400,attack:3.500,shoot:2.800,charge:3.500,use_cp:1.400,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:41,without_targets:28}
2026-02-24 15:31:46 | [TRAIN][EP] ep=84 ep_reward=-0.069832 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=17.0 enemy_hp_total=10.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=85 steps=10 skip={move:12,attack:33,shoot:28,charge:33,use_cp:7,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.200,attack:3.300,shoot:2.800,charge:3.300,use_cp:0.700,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:45,without_targets:28}
2026-02-24 15:31:46 | [TRAIN][EP] ep=85 ep_reward=-0.149944 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=model winner_env=None model_hp_total=8.0 enemy_hp_total=18.0 model_vp=1 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=86 steps=10 skip={move:14,attack:43,shoot:33,charge:43,use_cp:11,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.400,attack:4.300,shoot:3.300,charge:4.300,use_cp:1.100,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:40,without_targets:33}
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
y=-0.500
er=27.295, d_best=16.295, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=30.806, d_after=30.806, d_best=19.806, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
180, d_after=11.180, d_best=0.180, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.213203435596427->28.30194339616981
2026-02-24 15:31:46 | Reward (progress к objective): d_before=20.616, d_after=17.088, delta=3.528, norm=0.588, bonus=+0.018
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
eward (шаг): стрельба delta=-0.200
e=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
ld=-0.240, proximity=0.000, total=-0.240
): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+02026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.620
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
nged=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.808652046684813->25.45584412271571
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
ear_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=30.4138126514911->31.622776601683793
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.0->21.587033144922902
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.847319317591726->25.238858928247925
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.060
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
50, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
rength=0.000, objectives=0.000 (delta=0), total=-0.060
obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x102026-02-24 15:31:46 | Reward (шаг): бой delta=-0.060
0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.220
2026-02-24 15:31:46 | Reward (progress к objective): d_before=23.431, d_after=18.868, delta=4.563, norm=0.760, bonus=+0.023
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.250
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.075
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.075
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.075
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): цель мертва, выход из боя bonus=+0.300
, d_best=13.515, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=27.019, d_after=27.019, d_best=16.019, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.300
2026-02-24 15:31:46 | Reward (progress к objective): d_before=28.302, d_after=27.313, delta=0.989, norm=0.165, bonus=+0.005
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
n=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
.500
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=17.08800749063506->20.0
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=31.064449134018133->32.64965543462902
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.045
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.02026-02-24 15:31:46 | Reward (progress к objective): d_before=28.178, d_after=26.627, delta=1.551, norm=0.258, bonus=+0.02026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.045, strength=0.000, objectives=0.000 (delta=0), total=-0.095
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
00, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
oved_closer=0, min_dist=25.298221281347036->27.294688127912362
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.095
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
ьба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=11.180339887498949->18.110770276274835
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.220
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.250
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.250
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-24 15:31:46 | Reward (progress к objective): d_before=30.000, d_after=28.844, delta=1.156, norm=0.193, bonus=+0.006
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=30.806, d_after=30.806, d_best=19.806, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
3.615, d_after=33.615, d_best=22.615, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=27.459, d_after=27.074, delta=0.385, norm=0.064, bonus=+0.002
за пропуск = -0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=28.018, d_after=28.018, d_best=17.018, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=25.456, d_after=25.456, d_best=14.456, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.400
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.400
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.110770276274835->18.110770276274835
2026-02-24 15:31:46 | Reward (progress к objective): d_before=24.515, d_after=23.022, delta=1.494, norm=0.249, bonus=+0.007
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.587033144922902->23.259406699226016
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
�оделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.075
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.060
ors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.075, strength=0.000, objectives=0.000 (delta=0), total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.060, strength=0.000, objectives=0.02026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.110
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.090
 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.160
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=29.530, d_after=28.178, delta=1.352, norm=0.225, bonus=+0.007
2026-02-24 15:31:46 | Reward (progress к objective): d_before=20.000, d_after=16.971, delta=3.029, norm=0.505, bonus=+0.015
0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.690
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.790
2026-02-24 15:31:46 | Reward (победа): bonus=+3.000
2026-02-24 15:31:46 | Reward (progress к objective): d_before=30.806, d_after=28.018, delta=2.788, norm=0.465, bonus=+0.014
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.073972741361768->27.073972741361768
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=18.868, d_after=18.868, d_best=7.868, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
lty=-02026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.110770276274835->18.439088914585774
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=26.870, d_after=26.870, d_best=15.870, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
s=0, moved_closer=0, min_dist=23.259406699226016->29.410882339705484
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.150 (norm=0.250)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.530
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.075
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.867962264113206->18.867962264113206, hold_penalty_events=2
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.030
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.030
2026-02-24 15:31:46 | Reward (победа): bonus=+3.000
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=-0.075, strength=0.000, objectives=0.000 (delta=0), total=-0.075
2026-02-24 15:31:46 | Reward (бой): damage=0.150 (norm=0.250, dealt=5.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.180
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.030, strength=0.000, objectives=0.000 (delta=0), total=0.065
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.180
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.065
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=24.515, d_after=24.413, delta=0.102, norm=0.017, bonus=+0.001
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.250
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (progress к objective): d_before=27.313, d_after=26.926, delta=0.387, norm=0.065, bonus=+0.002
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=29.206, d_after=29.206, d_best=18.206, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=18.868, d_after=18.868, d_best=7.868, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=25.710, d_after=25.710, d_best=14.710, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.476404589747453->26.476404589747453
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=26.870, d_after=26.870, d_best=15.870, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.075
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.439088914585774->21.633307652783937
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
ld=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | Reward (progress к objective): d_before=27.295, d_after=26.926, delta=0.369, norm=0.061, bonus=+0.002
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.278820596099706->18.867962264113206
 total=-0.075
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=26.926, d_after=26.926, d_best=15.926, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.075
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.413111231467404->24.413111231467404
61768->27.073972741361768, hold_penalty_events=2
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
=0, damage=0.00, kills=0, moved_closer=0, min_dist=25.709920264364882->25.709920264364882, hold_penalty_events=2
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.240
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | Reward (progress к objective): d_before=22.472, d_after=16.279, delta=6.193, norm=1.032, bonus=+0.031
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.867962264113206->18.867962264113206, hold_penalty_events=2
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.120 (norm=0.200)
2026-02-24 15:31:46 | Reward (бой): kill_term=+0.400 (delta=1)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.090
2026-02-24 15:31:46 | Reward (бой): damage=0.120 (norm=0.200, dealt=4.00), kills=0.400 (delta=1), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.090, strength=0.000, objectives=0.000 (delta=0), total=0.610
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.610
2026-02-24 15:31:46 | Reward (progress к objective): d_before=26.926, d_after=25.298, delta=1.628, norm=0.271, bonus=+0.008
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (поражение): penalty=-2.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=20.000, d_after=20.000, d_best=9.000, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.459060435491963->28.635642126552707
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=None->None
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.073972741361768->27.294688127912362
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=17.464, d_after=17.464, d_best=6.464, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=26.476404589747453->27.51363298439521
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
.902, bonus=+0.027
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.413111231467404->26.1725046566048
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=25.298, d_after=24.083, delta=1.215, norm=0.203, bonus=+0.006
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.120
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (progress к objective): d_before=18.868, d_after=15.620, delta=3.247, norm=0.541, bonus=+0.016
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=16.279, d_after=13.416, delta=2.862, norm=0.477, bonus=+0.014
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.060
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=23.345, d_after=23.345, d_best=12.345, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.586228448267445->27.586228448267445
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=20.000, d_after=20.000, d_best=9.000, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=15.620, d_after=15.620, d_best=4.620, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.591260281974->24.758836806279895
lty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
464, d_after=17.464, d_best=6.464, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=23.769728648009426->23.769728648009426
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.51363298439521->30.01666203960727
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (progress к objective): d_before=20.248, d_after=14.765, delta=5.484, norm=0.914, bonus=+0.027
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.015
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=3.00, norm=0.150, penalty=-0.075
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=0.020
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.294688127912362->27.65863337187866
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=13.45362404707371->18.35755975068582
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.020

2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.060, strength=0.000, objectives=0.000 (delta=0), total=-0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.180 (norm=0.300, dealt=6.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.180 (norm=0.300, dealt=6.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.230
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.310
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.280
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.060
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.060, strength=0.000, objectives=0.000 (delta=0), total=0.060
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.060
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=17.464, d_after=16.125, delta=1.340, norm=0.223, bonus=+0.007
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=23.345, d_after=23.345, d_best=12.345, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): штраф за пропуск = -0.200
620, d_after=15.620, d_best=4.620, max_reach=11.000, could_reach_objective=1, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=24.759, d_after=16.000, delta=8.759, norm=1.460, bonus=+0.044
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.459060435491963->33.12099032335839
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.180
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
 моделей): Reward (стрельба): штраф за пропуск = -0.200
ll=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=30.01666203960727->30.01666203960727
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=-0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (progress к objective): d_before=27.586, d_after=26.907, delta=0.679, norm=0.113, bonus=+0.003
us=+0.050
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.73863375370596->25.709920264364882
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=23.769728648009426->23.769728648009426
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=19.313207915827967->25.0
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): success_bonus=+0.500
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.560
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): чардж delta=+0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.030
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.190
2026-02-24 15:31:46 | Reward (бой): damage=0.000 (norm=0.000, dealt=0.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=-0.030, strength=0.000, objectives=0.000 (delta=0), total=-0.030
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.090 (norm=0.150)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.030
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.060 (norm=0.100)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.045
0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=18.35755975068582->18.35755975068582
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.015
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.160
2026-02-24 15:31:46 | Reward (бой): damage=0.090 (norm=0.150, dealt=3.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.045, strength=0.000, objectives=0.000 (delta=0), total=0.110
2026-02-24 15:31:46 | Reward (бой): damage=0.060 (norm=0.100, dealt=2.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=0.075
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.110
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.075
2026-02-24 15:31:46 | Reward (progress к objective): d_before=27.659, d_after=22.361, delta=5.298, norm=0.883, bonus=+0.026
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=4.00, norm=0.200, penalty=-0.100
ьба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.200
2026-02-24 15:31:46 | Reward (progress к objective): d_before=23.770, d_after=22.023, delta=1.747, norm=0.291, bonus=+0.009
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.150 (norm=0.250)
r_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=16.0->16.1245154965971
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
_after=12.042, delta=4.083, norm=0.680, bonus=+0.020
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist2026-02-24 15:31:46 | Reward (бой): damage=0.150 (norm=0.250, dealt=5.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.000, strength=0.000, objectives=0.000 (delta=0), total=0.150
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x102026-02-24 15:31:46 | Reward (шаг): бой delta=+0.150
0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x102026-02-24 15:31:46 | Reward (бой): advantage_term=-0.060
0 (norm=0.200, dealt=4.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (progress к objective): d_before=25.000, d_after=19.209, delta=5.791, norm=0.965, bonus=+0.029
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.060, strength=0.000, objectives=0.000 (delta=0), total=-0.080
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.370
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.170
2026-02-24 15:31:46 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (progress к objective): d_before=30.017, d_after=23.431, delta=6.586, norm=1.098, bonus=+0.033
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
1.780, d_after=31.780, d_best=20.780, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя pena2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=31.623, d_after=31.623, d_best=20.623, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.200
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
ьба): damage_term=+0.210 (norm=0.350, dealt=7.00)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
00, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.000
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | Reward (progress к objective): d_before=33.121, d_after=31.016, delta=2.105, norm=0.351, bonus=+0.011
0 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=23.430749027719962->23.430749027719962
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.090 (norm=0.150)
r_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=20.591260281974->21.095023109728988
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x102026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
300, dealt=6.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.210 (norm=0.350, dealt=7.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.660
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.590
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
�делей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.150
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
ьба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.140
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.000 (norm=0.000, taken=0.00), advantage=0.150, strength=0.000, objectives=0.000 (delta=0), total=0.180
, obj_kill=0.000, action=0.000, total=0.230
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.140
2026-02-24 15:31:46 | Reward (бой): damage=0.090 (norm=0.150, dealt=3.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.135, st2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.180
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.095
riors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (победа): bonus=+3.000
ta=+0.110
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.170
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=12.042, d_after=10.630, delta=1.411, norm=0.235, bonus=+0.007
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.830
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.025 (norm=0.050)
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (бой): advantage_term=+0.015
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.340
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.025 (norm=0.050, taken=1.00), advantage=0.015, strength=0.000, objectives=0.000 (delta=0), total=0.020
2026-02-24 15:31:46 | Reward (шаг): бой delta=+0.020
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): остался в бою bonus=+0.200
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.120 (obj=0, d_before=27.074, d_after=27.074, d_best=16.074, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
er=19.723, d_best=8.723, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=1.00, reason=no_move_missed_progress)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | Reward (progress к objective): d_before=26.019, d_after=18.028, delta=7.991, norm=1.332, bonus=+0.040
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (движение): отступление из боя penalty=-0.500
2026-02-24 15:31:46 | Reward (VP/объекты, движение): hold=-0.240, proximity=0.000, total=-0.240
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=23.194827009486403->24.698178070456937
2026-02-24 15:31:46 | Reward (progress к objective): d_before=17.263, d_after=17.117, delta=0.145, norm=0.024, bonus=+0.001
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
rm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x102026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
50, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (шаг): движение delta=-1.000
2026-02-24 15:31:46 | Reward (бой): damage_term=+0.030 (norm=0.050)
2026-02-24 15:31:46 | Reward (шаг): движение delta=-0.500
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.110
2026-02-24 15:31:46 | Reward (бой): taken_penalty=-0.050 (norm=0.100)
2026-02-24 15:31:46 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.0->21.587033144922902
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.080
2026-02-24 15:31:46 | Reward (бой): advantage_term=-0.180
ors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.160
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.080
2026-02-24 15:31:46 | Reward (бой): damage=0.030 (norm=0.050, dealt=1.00), kills=0.000 (delta=0), taken=-0.050 (norm=0.100, taken=2.00), advantage=-0.180, strength=0.000, objectives=0.000 (delta=0), total=-0.200
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (урон по модели): damage_taken=2.00, norm=0.100, penalty=-0.050
2026-02-24 15:31:46 | Reward (шаг): бой delta=-0.200
amage_taken=1.00, norm=0.050, penalty=-0.025
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.600
2026-02-24 15:31:46 | Reward (progress к objective): d_before=31.623, d_after=29.069, delta=2.554, norm=0.426, bonus=+0.013
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.680
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.100
2026-02-24 15:31:46 | Reward (победа): bonus=+3.000
2026-02-24 15:31:46 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.400, overkill=-0.000, quality=0.100, obj_damage=0.000, obj_kill=0.000, action=0.000, total=0.530
2026-02-24 15:31:46 | Reward (шаг): стрельба delta=+0.690
2026-02-24 15:31:46 | Reward (победа): bonus=+3.000
2026-02-24 15:31:46 | [TRAIN][EP] ep=86 ep_reward=0.014805 win=1 vp_diff=1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=14.0 enemy_hp_total=8.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=87 steps=10 skip={move:10,attack:45,shoot:36,charge:45,use_cp:11,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.000,attack:4.500,shoot:3.600,charge:4.500,use_cp:1.100,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:39,without_targets:36}
2026-02-24 15:31:46 | [TRAIN][EP] ep=87 ep_reward=-0.105315 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=15.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=88 steps=10 skip={move:13,attack:42,shoot:34,charge:42,use_cp:13,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.300,attack:4.200,shoot:3.400,charge:4.200,use_cp:1.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:42,without_targets:34}
2026-02-24 15:31:46 | [TRAIN][EP] ep=88 ep_reward=0.359638 win=1 vp_diff=-1 end_reason=wipeout_enemy
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=12.0 enemy_hp_total=13.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=89 steps=10 skip={move:11,attack:49,shoot:32,charge:49,use_cp:18,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.100,attack:4.900,shoot:3.200,charge:4.900,use_cp:1.800,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:45,without_targets:32}
2026-02-24 15:31:46 | [TRAIN][EP] ep=89 ep_reward=-0.076100 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=17.0 enemy_hp_total=16.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=90 steps=10 skip={move:15,attack:38,shoot:41,charge:38,use_cp:13,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.500,attack:3.800,shoot:4.100,charge:3.800,use_cp:1.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:36,without_targets:41}
2026-02-24 15:31:46 | [TRAIN][EP] ep=90 ep_reward=0.006961 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=20.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=91 steps=10 skip={move:12,attack:52,shoot:32,charge:52,use_cp:10,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.200,attack:5.200,shoot:3.200,charge:5.200,use_cp:1.000,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:45,without_targets:32}
2026-02-24 15:31:46 | [TRAIN][EP] ep=91 ep_reward=0.437500 win=1 vp_diff=-1 end_reason=wipeout_enemy
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=15.0 enemy_hp_total=17.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=92 steps=10 skip={move:14,attack:48,shoot:31,charge:48,use_cp:13,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.400,attack:4.800,shoot:3.100,charge:4.800,use_cp:1.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:46,without_targets:31}
2026-02-24 15:31:46 | [TRAIN][EP] ep=92 ep_reward=-0.072265 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=enemy winner_env=None model_hp_total=18.0 enemy_hp_total=4.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=93 steps=10 skip={move:12,attack:42,shoot:34,charge:42,use_cp:13,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.200,attack:4.200,shoot:3.400,charge:4.200,use_cp:1.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:43,without_targets:34}
2026-02-24 15:31:46 | [TRAIN][EP] ep=93 ep_reward=-0.139698 win=0 vp_diff=-1 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=7.0 enemy_hp_total=19.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=94 steps=10 skip={move:11,attack:41,shoot:29,charge:41,use_cp:22,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.100,attack:4.100,shoot:2.900,charge:4.100,use_cp:2.200,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:50,without_targets:29}
2026-02-24 15:31:46 | [TRAIN][EP] ep=94 ep_reward=0.059345 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=3.0 enemy_hp_total=3.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=95 steps=10 skip={move:10,attack:49,shoot:31,charge:49,use_cp:15,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.000,attack:4.900,shoot:3.100,charge:4.900,use_cp:1.500,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:48,without_targets:31}
2026-02-24 15:31:46 | [TRAIN][EP] ep=95 ep_reward=-0.011583 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_model winner=enemy winner_env=enemy model_hp_total=0.0 enemy_hp_total=9.0 model_vp=0 enemy_vp=1 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=96 steps=10 skip={move:16,attack:41,shoot:31,charge:41,use_cp:15,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.600,attack:4.100,shoot:3.100,charge:4.100,use_cp:1.500,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:48,without_targets:31}
2026-02-24 15:31:46 | [TRAIN][EP] ep=96 ep_reward=-0.227552 win=0 vp_diff=-1 end_reason=wipeout_model
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=7.0 enemy_hp_total=3.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=97 steps=10 skip={move:13,attack:37,shoot:33,charge:37,use_cp:7,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.300,attack:3.700,shoot:3.300,charge:3.700,use_cp:0.700,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:50,without_targets:33}
2026-02-24 15:31:46 | [TRAIN][EP] ep=97 ep_reward=0.030260 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=turn_limit_Only War winner=draw winner_env=None model_hp_total=4.0 enemy_hp_total=20.0 model_vp=0 enemy_vp=0 turn=11 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=98 steps=10 skip={move:15,attack:48,shoot:38,charge:48,use_cp:13,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:1.500,attack:4.800,shoot:3.800,charge:4.800,use_cp:1.300,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:45,without_targets:38}
2026-02-24 15:31:46 | [TRAIN][EP] ep=98 ep_reward=-0.057141 win=0 vp_diff=0 end_reason=turn_limit_Only War
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=16.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=1 turn=7 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=99 steps=6 skip={move:14,attack:43,shoot:38,charge:43,use_cp:13,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:2.333,attack:7.167,shoot:6.333,charge:7.167,use_cp:2.167,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:45,without_targets:38}
2026-02-24 15:31:46 | [TRAIN][EP] ep=99 ep_reward=0.729862 win=1 vp_diff=-1 end_reason=wipeout_enemy
2026-02-24 15:31:46 | Конец эпизода: reason=wipeout_enemy winner=model winner_env=model model_hp_total=18.0 enemy_hp_total=0.0 model_vp=0 enemy_vp=0 turn=8 battle_round=None
2026-02-24 15:31:46 | [TRAIN][ACTIONS] ep=100 steps=7 skip={move:18,attack:43,shoot:43,charge:43,use_cp:14,cp_on:0} invalid={move:0,attack:0,shoot:0,charge:0,use_cp:0,cp_on:0} skip_rate={move:2.571,attack:6.143,shoot:6.143,charge:6.143,use_cp:2.000,cp_on:0.000} invalid_rate={move:0.000,attack:0.000,shoot:0.000,charge:0.000,use_cp:0.000,cp_on:0.000} shoot_windows={with_targets:41,without_targets:43}
2026-02-24 15:31:46 | [TRAIN][EP] ep=100 ep_reward=0.538034 win=1 vp_diff=0 end_reason=wipeout_enemy
2026-02-24 15:31:47 | [SAVE] pickle сохранён в subprocess env: models/M_Necrons_vs_P_Necrons/model-44-1810.pickle
