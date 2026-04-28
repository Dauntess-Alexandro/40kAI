"""Compatibility wrappers for mission deployment helpers.

Only War mission deployment logic lives in core.engine.mission.
"""
from __future__ import annotations

from core.engine.mission import (
    deploy_depth,
    is_in_deploy_zone,
    validate_deploy_coord,
    get_random_free_deploy_coord,
    deploy_only_war,
    post_deploy_setup,
)

__all__ = [
    "deploy_depth",
    "is_in_deploy_zone",
    "validate_deploy_coord",
    "get_random_free_deploy_coord",
    "deploy_only_war",
    "post_deploy_setup",
]
