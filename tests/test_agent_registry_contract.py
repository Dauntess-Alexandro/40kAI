import unittest
from pathlib import Path


class TestAgentRegistryContract(unittest.TestCase):
    def test_registry_has_contract_helpers(self):
        source = Path("gym_mod/gym_mod/engine/agent_registry.py").read_text(encoding="utf-8")
        self.assertIn("def make_env_contract(", source)
        self.assertIn("obs_space_signature", source)
        self.assertIn("action_space_signature", source)
        self.assertIn("def compatible_contracts(", source)


if __name__ == "__main__":
    unittest.main()

