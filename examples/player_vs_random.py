import gymnasium as gym
from gomoku_gym.core.cell import Cell
from agents.random import RandomAgent

env = gym.make("GomokuBoardEnv-v0", render_mode="human", player_count=1, player="black")

agent = RandomAgent(Cell.WHITE)

obs, info = env.reset()
done = False
truncated = False

while not (done or truncated):
    action = agent.act(obs)
    obs, reward, done, truncated, info = env.step(action)