"""Compatibility wrappers for mission deployment helpers.

Only War mission deployment logic lives in gym_mod.engine.mission.
"""
from __future__ import annotations

from gym_mod.engine.mission import (
    deploy_depth,
    is_in_deploy_zone,
    deploy_only_war,
    post_deploy_setup,
)

__all__ = [
    "deploy_depth",
    "is_in_deploy_zone",
    "deploy_only_war",
    "post_deploy_setup",
]
