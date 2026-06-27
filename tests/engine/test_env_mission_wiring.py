"""Регресс: env-конструкция применяет ВЫБРАННУЮ миссию (MISSION_NAME), не дефолт only_war.

Баг (коммит 21961674): Warhammer40kEnv.__init__ звал apply_mission_layout(self) без имени
миссии -> всегда only_war (board/scoring/лимит 20/reward-профиль). MISSION_NAME=annihilation
игнорировался; annihilation активировалась лишь в юнит-тестах (где layout зовётся явно), а
train/eval/play шли на only_war. Этот тест ловит именно интеграцию env-конструкция ->
mission_key / scoring_mode / лимит раундов / reward-профиль.
"""
import pytest

import reward_config as rc
from core.engine import mission as M
from core.envs.warhamEnv import Warhammer40kEnv
from tests.engine.phases._helpers import make_unit


@pytest.fixture(autouse=True)
def _reset_profile():
    yield
    rc.configure_for_mission("only_war")


def _make_env(monkeypatch, mission_name):
    if mission_name is None:
        monkeypatch.delenv("MISSION_NAME", raising=False)
    else:
        monkeypatch.setenv("MISSION_NAME", mission_name)
    model = [make_unit("M0")]
    enemy = [make_unit("E0")]
    return Warhammer40kEnv(enemy=enemy, model=model, b_len=30, b_hei=30)


def test_env_applies_annihilation_from_mission_name(monkeypatch):
    env = _make_env(monkeypatch, "annihilation")
    assert env.mission_key == "annihilation"
    assert env.mission_scoring_mode == "kill_points"
    assert M.mission_max_battle_rounds(env) == 8          # лимит миссии, не глобальные 20
    assert rc.active_profile_name() == "annihilation"     # reward-профиль миссии активен


def test_env_defaults_to_only_war_without_mission_name(monkeypatch):
    env = _make_env(monkeypatch, None)
    assert env.mission_key == "only_war"
    assert env.mission_scoring_mode == "objective_control"
    assert M.mission_max_battle_rounds(env) == 20
    assert rc.active_profile_name() == "only_war"
