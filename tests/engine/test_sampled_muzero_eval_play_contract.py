"""Контрактный тест eval/play для sampled_muzero.

Проверяет, что:
1. Чекпойнт sampled_muzero корректно строится и сохраняется.
2. Сеть загружается из state_dict без ошибок.
3. infer() возвращает прогнозы правильного формата (probs x heads, value shape).
4. select_action_with_epsilon_sampled_muzero возвращает тензор с легальными
   действиями корректного формата (без исключений, action в пределах пространства).

Аналог tests/engine/test_gumbel_muzero_eval_play_contract.py для sampled_muzero.
"""

import os
import pathlib
import sys

import pytest
import torch

# Убеждаемся, что корень проекта в sys.path
_PROJECT_ROOT = str(pathlib.Path(__file__).parent.parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from core.models.sampled_muzero_model import (
    SampledMuZeroNet,
    load_sampled_muzero_state_dict,
    make_sampled_muzero_net,
    sampled_muzero_arch_from_payload,
)
from core.models.utils import normalize_state_dict

# ---------------------------------------------------------------------------
# Параметры игрушечной сети (маленькие, чтобы тест был быстрым)
# ---------------------------------------------------------------------------
N_OBS = 14
N_ACTIONS = [4, 2, 6]
_SMALL_KWARGS = dict(latent_dim=32, hidden_dim=32, num_layers=1, action_embed_dim=8)


# ---------------------------------------------------------------------------
# Test 1: структура чекпойнта
# ---------------------------------------------------------------------------

def test_sampled_muzero_checkpoint_contract_contains_algo_and_state():
    """Чекпойнт содержит algo, sampled_muzero_net; state_dict загружается."""
    net = SampledMuZeroNet(obs_dim=N_OBS, action_sizes=N_ACTIONS, **_SMALL_KWARGS)
    payload = {
        "algo": "sampled_muzero",
        "sampled_muzero_net": normalize_state_dict(net.state_dict()),
        "arch": _SMALL_KWARGS,
    }
    assert payload["algo"] == "sampled_muzero"
    assert isinstance(payload["sampled_muzero_net"], dict)

    # Загружаем в клон
    clone = SampledMuZeroNet(obs_dim=N_OBS, action_sizes=N_ACTIONS, **_SMALL_KWARGS)
    clone.load_state_dict(payload["sampled_muzero_net"])

    # infer должен возвращать probs по каждой голове + value
    x = torch.randn(1, N_OBS)
    probs, value = clone.infer(x, masks_by_head=None)
    assert len(probs) == len(N_ACTIONS), "Число голов политики должно совпадать с n_actions"
    assert value.shape == (1,), f"value.shape ожидалось (1,), получено {value.shape}"
    for i, (p, n) in enumerate(zip(probs, N_ACTIONS)):
        assert p.shape == (1, n), f"Голова {i}: ожидалось shape (1, {n}), получено {p.shape}"


# ---------------------------------------------------------------------------
# Test 2: sampled_muzero_arch_from_payload восстанавливает arch
# ---------------------------------------------------------------------------

def test_sampled_muzero_arch_from_payload():
    """arch из payload корректно восстанавливается через sampled_muzero_arch_from_payload."""
    payload = {
        "algo": "sampled_muzero",
        "arch": _SMALL_KWARGS,
    }
    arch = sampled_muzero_arch_from_payload(payload)
    assert arch["latent_dim"] == _SMALL_KWARGS["latent_dim"]
    assert arch["hidden_dim"] == _SMALL_KWARGS["hidden_dim"]
    assert arch["num_layers"] == _SMALL_KWARGS["num_layers"]
    assert arch["action_embed_dim"] == _SMALL_KWARGS["action_embed_dim"]


# ---------------------------------------------------------------------------
# Test 3: load_sampled_muzero_state_dict не вызывает исключений
# ---------------------------------------------------------------------------

def test_load_sampled_muzero_state_dict_no_crash():
    """load_sampled_muzero_state_dict успешно загружает state_dict без исключений."""
    net = SampledMuZeroNet(obs_dim=N_OBS, action_sizes=N_ACTIONS, **_SMALL_KWARGS)
    sd = normalize_state_dict(net.state_dict())

    clone = SampledMuZeroNet(obs_dim=N_OBS, action_sizes=N_ACTIONS, **_SMALL_KWARGS)
    missing, unexpected = load_sampled_muzero_state_dict(clone, sd)
    assert len(missing) == 0, f"missing keys: {missing}"
    assert len(unexpected) == 0, f"unexpected keys: {unexpected}"


# ---------------------------------------------------------------------------
# Test 4: select_action_with_epsilon_sampled_muzero — greedy-режим
# ---------------------------------------------------------------------------

def test_select_action_greedy_format_and_legality(tmp_path, monkeypatch):
    """
    В greedy-режиме select_action_with_epsilon_sampled_muzero возвращает тензор
    shape=(1, n_heads), все действия в легальном диапазоне, без исключений.

    Используется минимальный mock-env чтобы не поднимать полный warhamEnv.
    """
    # Форсируем greedy, чтобы не запускать полный поиск
    monkeypatch.setenv("SMZ_EVAL_MODE", "greedy")

    from eval import select_action_with_epsilon_sampled_muzero

    # Строим сеть
    net = make_sampled_muzero_net(obs_dim=N_OBS, action_sizes=N_ACTIONS, **_SMALL_KWARGS)
    net.eval()

    # Фиктивный obs
    state = torch.randn(1, N_OBS)

    # Маски: все легальны
    n_model_units = 1  # len_model

    # Расширенное действие: move, attack, shoot, charge, use_cp, cp_on, move_num_0
    # n_heads = len(N_ACTIONS) = 3 в нашей игрушечной сети, но реальный env
    # возвращает 6 + n_model_units голов. Используем mock-env.
    class MockSpace:
        def sample(self):
            return {
                "move": 0, "attack": 0, "shoot": 0,
                "charge": 0, "use_cp": 0, "cp_on": 0,
                "move_num_0": 0,
            }

    class MockEnv:
        action_space = MockSpace()

        def get_legal_actions(self, *a, **kw):
            return list(range(N_ACTIONS[0]))

    # Имитируем build_action_masks_by_head: вернём маски по N_ACTIONS
    import eval as eval_module

    original_build = eval_module.build_action_masks_by_head

    def mock_build_masks(env, len_model, log_fn=None, debug=False):
        return [torch.ones(s, dtype=torch.bool) for s in N_ACTIONS]

    monkeypatch.setattr(eval_module, "build_action_masks_by_head", mock_build_masks)

    env = MockEnv()
    action = select_action_with_epsilon_sampled_muzero(
        env=env,
        state=state,
        policy_net=net,
        epsilon=0.0,
        len_model=n_model_units,
    )

    # Проверки формата
    assert isinstance(action, torch.Tensor), "Действие должно быть torch.Tensor"
    assert action.dim() == 2, f"Ожидалось 2D тензор, получено {action.dim()}D"
    assert action.shape[0] == 1, f"Первое измерение должно быть 1, получено {action.shape[0]}"
    # Число голов: len(N_ACTIONS)
    assert action.shape[1] == len(N_ACTIONS), (
        f"Число голов: ожидалось {len(N_ACTIONS)}, получено {action.shape[1]}"
    )

    # Все действия в допустимом диапазоне
    for i, (a, n) in enumerate(zip(action[0].tolist(), N_ACTIONS)):
        assert 0 <= a < n, f"Голова {i}: действие {a} вне диапазона [0, {n})"


# ---------------------------------------------------------------------------
# Test 5: чекпойнт изолирован в tmp_path (нет записи в репо)
# ---------------------------------------------------------------------------

def test_checkpoint_saved_to_tmp_path_only(tmp_path):
    """Чекпойнт сохраняется только в tmp_path, репозиторий не загрязнён."""
    ckpt_path = tmp_path / "smz_contract_test.pt"

    net = SampledMuZeroNet(obs_dim=N_OBS, action_sizes=N_ACTIONS, **_SMALL_KWARGS)
    payload = {
        "algo": "sampled_muzero",
        "sampled_muzero_net": normalize_state_dict(net.state_dict()),
        "arch": _SMALL_KWARGS,
    }
    torch.save(payload, ckpt_path)
    assert ckpt_path.exists(), "Чекпойнт должен существовать в tmp_path"

    # Перезагрузка
    loaded = torch.load(ckpt_path, map_location="cpu", weights_only=True)
    assert loaded["algo"] == "sampled_muzero"
    assert isinstance(loaded["sampled_muzero_net"], dict)

    clone = SampledMuZeroNet(obs_dim=N_OBS, action_sizes=N_ACTIONS, **_SMALL_KWARGS)
    clone.load_state_dict(loaded["sampled_muzero_net"])
    x = torch.randn(1, N_OBS)
    probs, value = clone.infer(x, masks_by_head=None)
    assert len(probs) == len(N_ACTIONS)
    assert value.shape == (1,)
