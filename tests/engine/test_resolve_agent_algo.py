import unittest

import torch

from core.engine.agent_registry import infer_algo_from_policy_state, resolve_agent_algo
from core.models.DQN import infer_dqn_arch_from_state_dict, make_dqn


class TestResolveAgentAlgo(unittest.TestCase):
    def test_infer_dqn_dueling_from_head_bundles(self):
        net = make_dqn(12, [3, 2, 4], dueling=True, noisy=True, distributional="iqn", n_ensemble=2)
        sd = net.state_dict()
        self.assertEqual(infer_algo_from_policy_state(sd), "dqn")
        arch = infer_dqn_arch_from_state_dict(sd)
        self.assertTrue(arch["dueling"])
        rebuilt = make_dqn(12, [3, 2, 4], **arch)
        rebuilt.load_state_dict(sd)

    def test_resolve_prefers_weights_over_wrong_meta(self):
        net = make_dqn(8, [2, 2], dueling=False, noisy=False, distributional=None, n_ensemble=1)
        sd = net.state_dict()
        algo = resolve_agent_algo(
            meta={"algo": "ppo", "agent_id": "test_agent"},
            policy_state=sd,
            target_state=None,
            agent_id="test_agent",
        )
        self.assertEqual(algo, "dqn")

    def test_resolve_ppo_policy_heads_trusts_meta(self):
        # PPO и AlphaZero-tree делят архитектуру (policy_heads/value_heads),
        # поэтому инференс по весам выдаёт az. Но meta.algo="ppo" её пишет тренер —
        # для этой неоднозначности meta авторитетна, иначе PPO грузится как AZ-tree.
        sd = {
            "input_fc.weight": torch.zeros(4, 3),
            "policy_heads.0.weight": torch.zeros(2, 4),
            "value_heads.0.weight": torch.zeros(1, 4),
            "value_head.weight": torch.zeros(1, 4),
        }
        # инференс сам по себе не различает ppo/az по этим ключам:
        self.assertEqual(infer_algo_from_policy_state(sd), "alphazero_tree")
        algo = resolve_agent_algo(
            meta={"algo": "ppo", "agent_id": "ppo_test"},
            policy_state=sd,
            target_state=None,
            agent_id="ppo_test",
        )
        self.assertEqual(algo, "ppo")

    def test_resolve_az_from_policy_heads(self):
        sd = {
            "input_fc.weight": torch.zeros(4, 3),
            "policy_heads.0.weight": torch.zeros(2, 4),
            "value_heads.0.weight": torch.zeros(1, 4),
        }
        algo = resolve_agent_algo(
            meta={"algo": "dqn", "mcts_mode": "tree", "agent_id": "az_test"},
            policy_state=sd,
            target_state={},
            agent_id="az_test",
        )
        self.assertEqual(algo, "alphazero_tree")

    def test_eval_source_uses_infer_dqn_arch(self):
        source = open("eval.py", encoding="utf-8").read()
        self.assertIn("infer_dqn_arch_from_state_dict", source)
        self.assertIn("resolve_agent_algo", source)


if __name__ == "__main__":
    unittest.main()
