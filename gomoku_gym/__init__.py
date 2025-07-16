from gymnasium.envs.registration import register

def register_envs():
    register(
        id="GomokuBoardEnv-v0",
        entry_point="gomoku_gym.envs.gomoku_board:GomokuBoardEnv",
    )