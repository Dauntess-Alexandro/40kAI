# Plan: Honest AZ DET-eval (tree + proxy)

**Status: implemented**

Inline DET-eval для `alphazero_tree` / `alphazero_proxy`: 20 локальных игр на learner с MCTS (`AZ_MCTS_MODE`), temp **0.06**, `dirichlet_eps=0`, `policy_argmax=True` — как `eval.py` (`AZ_EVAL_MODE=mcts`).

Старый путь `ep_rows[-50:]` удалён. Gate (`AZ_DET_EVAL_GATE_*`) использует честный winrate.

## Config

- `AZ_HONEST_EVAL_EPISODES=20`
- `AZ_HONEST_EVAL_SIMS` (default = train `AZ_MCTS_SIMS`)
- `AZ_HONEST_EVAL_TEMPERATURE=0.06`
- `AZ_HONEST_EVAL_DIR_EPS=0.0`

Trigger: `ACTOR_DET_EVAL_EVERY_EPISODES=300`
