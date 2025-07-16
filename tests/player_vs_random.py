import gymnasium as gym
import gomoku_gym

env = gym.make("GomokuBoardEnv-v0", render_mode="human", player_count=1, player="black")
obs, info = env.reset()

done = False
while not done:
    action = env.action_space.sample()
    obs, reward, done, _, info = env.step(action)