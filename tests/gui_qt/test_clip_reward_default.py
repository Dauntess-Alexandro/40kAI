from __future__ import annotations

from PySide6 import QtCore

from app.gui_qt.main import GUIController


def test_clip_reward_default_is_off_for_dqn_ppo_and_phoenix():
    assert GUIController._default_clip_reward_for_algo("dqn") == "off"
    assert GUIController._default_clip_reward_for_algo("ppo") == "off"
    assert GUIController._default_clip_reward_for_algo("phoenix") == "off"


def test_clip_reward_default_keeps_legacy_for_other_algos():
    assert GUIController._default_clip_reward_for_algo("alphazero_tree") == "1"
    assert GUIController._default_clip_reward_for_algo("gumbel_muzero") == "1"


def test_clip_reward_env_override_is_preserved():
    ctrl = GUIController.__new__(GUIController)
    ctrl._training_algo = "dqn"
    env = QtCore.QProcessEnvironment()
    env.insert("CLIP_REWARD", "-5,5")

    ctrl._apply_default_clip_reward_to_env(env)

    assert env.value("CLIP_REWARD") == "-5,5"


def test_clip_reward_env_default_inserted_for_dqn():
    ctrl = GUIController.__new__(GUIController)
    ctrl._training_algo = "dqn"
    env = QtCore.QProcessEnvironment()

    ctrl._apply_default_clip_reward_to_env(env)

    assert env.value("CLIP_REWARD") == "off"
