"""Тесты подсветки CUDA-полей в GUI."""

from app.gui_qt.hyperparams_cuda_hints import (
    CUDA_FIELD_MISSING,
    CUDA_FIELD_NEUTRAL,
    CUDA_FIELD_OK,
    hyperparam_cuda_field_state,
    would_gmz_hyperparam_violate_cuda,
)


def test_gmz_cuda_ok_when_gpu_available():
    assert hyperparam_cuda_field_state("gmz", "actor_device", "cuda", True) == CUDA_FIELD_OK
    assert hyperparam_cuda_field_state("gmz", "learner_compile", 1, True) == CUDA_FIELD_OK


def test_gmz_missing_when_cuda_value_without_gpu():
    assert hyperparam_cuda_field_state("gmz", "actor_device", "cuda", False) == CUDA_FIELD_MISSING
    assert hyperparam_cuda_field_state("gmz", "actor_device", "cpu", False) == CUDA_FIELD_NEUTRAL
    assert hyperparam_cuda_field_state("gmz", "inference_server_enabled", 1, False) == CUDA_FIELD_MISSING
    assert hyperparam_cuda_field_state("gmz", "inference_server_enabled", 0, False) == CUDA_FIELD_NEUTRAL


def test_gmz_set_blocked_without_cuda():
    assert would_gmz_hyperparam_violate_cuda("actor_device", "cuda", False)
    assert not would_gmz_hyperparam_violate_cuda("actor_device", "cpu", False)
    assert not would_gmz_hyperparam_violate_cuda("actor_device", "cuda", True)
