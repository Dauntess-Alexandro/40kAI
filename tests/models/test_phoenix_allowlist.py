from core.models.alphazero_ids import VALID_TRAIN_ALGOS


def test_phoenix_in_valid_train_algos():
    assert "phoenix" in VALID_TRAIN_ALGOS


def test_phoenix_in_train_opponent_and_eval_lists():
    import re
    for path in ("train.py", "eval.py", "play.py"):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        assert "phoenix" in text, f"phoenix отсутствует в {path} (тихий fallback на dqn!)"
