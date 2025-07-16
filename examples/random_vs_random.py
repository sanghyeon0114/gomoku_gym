import gymnasium as gym
import gomoku_gym
gomoku_gym.register_envs()

env = gym.make("GomokuBoardEnv-v0", render_mode="human", player_count=0)
obs, info = env.reset()

done = False
while not done:
    action = env.action_space.sample()
    obs, reward, done, _, info = env.step(action)