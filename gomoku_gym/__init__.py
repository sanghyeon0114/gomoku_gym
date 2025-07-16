from gymnasium.envs.registration import register, registry

def register_envs():
    env_id = "gomoku_gym/GomokuBoardEnv-v0"
    if env_id in registry:
        del registry[env_id]
    register(
        id=env_id,
        entry_point="gomoku_gym.envs.gomoku_board:GomokuBoardEnv",
    )

register_envs()