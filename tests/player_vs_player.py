from gomoku_gym import register_envs
register_envs()

import gymnasium as gym

env = gym.make("gomoku_gym/GomokuBoardEnv-v0", render_mode="human", player_count=2)
obs, info = env.reset()

done = False
while not done:
    action = env.action_space.sample()
    obs, reward, done, _, info = env.step(action)