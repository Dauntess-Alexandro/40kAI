from gymnasium.envs.registration import register, registry


if "40kAI-v0" not in registry:
    register(
        id="40kAI-v0",
        entry_point="core.envs.warhamEnv:Warhammer40kEnv",
    )
