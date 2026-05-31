# Plan: Honest GMZ DET-eval (Search + deterministic, temp 0.10)

**Status: implemented** — старый summary из `ep_rows` удалён, только inline search-eval.

## Goal

DET-eval для GMZ = **20 локальных игр** на ПК1: search (sims=48), `deterministic=True`, temp **0.10** — как Viewer Search / `eval.py`.

Раньше «DET-eval» брал последние 50 **train**-игр (stochastic IS) → winrate занижен. Этот путь **удалён**.

## Architecture

- **Trigger:** `ACTOR_DET_EVAL_ENABLED` + `ACTOR_DET_EVAL_EVERY_EPISODES` (300)
- **Eval:** `_gmz_build_actor_det_payload` → `_run_gmz_honest_eval` → `_gmz_det_payload_from_rows`
- **Weights:** `gmz_net` (learner), не EMA
- **Opponent:** `opponent_spec`, `build_policy_fn(deterministic=True)`
- **eval_tag:** `actor_learner_search_eval`

## Config (env)

```python
GMZ_HONEST_EVAL_EPISODES = 20      # GMZ_HONEST_EVAL_EPISODES
GMZ_HONEST_EVAL_SIMS = GMZ_MCTS_SIMS
GMZ_HONEST_EVAL_TOP_K = GMZ_ROOT_TOP_K
GMZ_HONEST_EVAL_TEMPERATURE = 0.10
```

## Files

- `core/models/gumbel_muzero_selfplay.py` — `deterministic` param
- `train.py` — helpers + integration (periodic + final)
- `tests/models/test_gmz_honest_eval.py`

## Performance

~15–40 s pause every 300 ep (~9–25% overhead).
