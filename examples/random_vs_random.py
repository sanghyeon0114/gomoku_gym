import gymnasium as gym
from gomoku_gym.core.cell import Cell
from agents.random import RandomAgent

env = gym.make("GomokuBoardEnv-v0", player_count=0, render_mode="human", rule="renju")

black_agent = RandomAgent(Cell.BLACK)
white_agent = RandomAgent(Cell.WHITE)
agents = {
    Cell.BLACK: black_agent, 
    Cell.WHITE: white_agent,
    }

obs, info = env.reset()
done = False
truncated = False

while not (done or truncated):
    current_player = obs['current_player']
    action = agents[current_player].act(obs)

    obs, reward, done, truncated, info = env.step(action)
            
env.close()