"""DET-прогоны удалены из тренировки: точки метрик — окно реальных эпизодов.

Контракт: train.py не играет отдельных детерминированных игр во время обучения;
вкладка «Метрики модели» получает агрегаты ep_rows (eval_tag=train_window),
честное сравнение моделей — отдельный eval.py.
"""
from pathlib import Path


def _src() -> str:
    return Path("train.py").read_text(encoding="utf-8")


def test_det_game_runners_deleted():
    src = _src()
    for name in (
        "def _run_actor_det_eval(",
        "def _run_actor_det_eval_ppo(",
        "def _az_build_actor_det_payload(",
        "def _gmz_build_actor_det_payload(",
    ):
        assert name not in src, f"DET-прогон не удалён: {name}"


def test_train_window_payload_used_everywhere():
    src = _src()
    assert "def _train_window_payload_from_rows(" in src
    # Helper def + DQN/PPO actor-learner DET-like windows + финальная сводка.
    assert src.count("_train_window_payload_from_rows(") >= 4
    # AZ и GMZ — через свои агрегаторы с явным тегом train_window
    # (DQN/PPO получают тег внутри _train_window_payload_from_rows).
    assert src.count('eval_tag="train_window"') >= 3


def test_data_json_marks_train_window_mode():
    src = _src()
    assert 'metrics_mode="det_eval"' not in src
    assert src.count('metrics_mode="train_window"') >= 10
