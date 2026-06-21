"""Legacy PPO subproc worker is removed from train.py."""

from __future__ import annotations

import ast
from pathlib import Path


def _train_src() -> str:
    return Path("train.py").read_text(encoding="utf-8")


def _top_level_functions() -> set[str]:
    module = ast.parse(_train_src())
    return {node.name for node in module.body if isinstance(node, ast.FunctionDef)}


def test_legacy_ppo_subproc_helpers_removed():
    names = _top_level_functions()
    assert "_ppo_worker_install_reaction_net" not in names
    assert "_env_worker" not in names
    assert "run_ppo_training" not in names
    assert "run_ppo_training_subproc" not in names


def test_ppo_actor_learner_entrypoints_remain():
    names = _top_level_functions()
    assert "_main_actor_learner_ppo" in names
    assert "_actor_learner_actor_entry_ppo" in names


def test_main_reports_removed_legacy_flag():
    src = _train_src()
    assert "PRO_ACTOR_LEARNER=0 больше не поддерживается" in src
    assert "legacy non-pro pipeline удалён" in src
