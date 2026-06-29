from core.models.alphazero_ids import VALID_TRAIN_ALGOS


def test_phoenix_in_valid_train_algos():
    assert "phoenix" in VALID_TRAIN_ALGOS


def test_phoenix_in_valid_agent_algos():
    from core.engine.agent_registry import _VALID_AGENT_ALGOS

    assert "phoenix" in _VALID_AGENT_ALGOS


def test_phoenix_in_train_opponent_and_eval_lists():
    for path in ("train.py", "eval.py", "play.py"):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        assert "phoenix" in text, f"phoenix отсутствует в {path} (тихий fallback на dqn!)"


def test_full_phoenix_weights_inferred_as_phoenix():
    """Полный phoenix-state_dict опознаётся как phoenix (приоритет до dqn/gmz-эвристик)."""
    from core.engine.agent_registry import infer_algo_from_policy_state
    from core.models.phoenix_config import PhoenixConfig
    from core.models.phoenix_model import PhoenixNet

    net = PhoenixNet(6, [3, 4], PhoenixConfig(hidden_size=16, num_layers=1, emb_dim=8))
    assert infer_algo_from_policy_state(net.state_dict()) == "phoenix"


def test_rl_only_weights_resolve_phoenix_via_meta():
    """RL-only веса инферятся как dqn, но meta.algo=phoenix даёт приоритет phoenix."""
    from core.engine.agent_registry import resolve_agent_algo
    from core.models.phoenix_config import PhoenixConfig
    from core.models.phoenix_model import PhoenixNet

    net = PhoenixNet(6, [3, 4], PhoenixConfig(hidden_size=16, num_layers=1, emb_dim=8))
    rl_only = {k: v for k, v in net.state_dict().items()
               if k.startswith("online.") or k.startswith("target.")}
    resolved = resolve_agent_algo(meta={"algo": "phoenix"}, policy_state=rl_only, agent_id="x")
    assert resolved == "phoenix"
