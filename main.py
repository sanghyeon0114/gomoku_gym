import gymnasium as gym
import gomoku_gym
from gomoku_gym.core.cell import Cell
from agents.random import RandomAgent

gomoku_gym.register_envs()

env = gym.make("GomokuBoardEnv-v0", render_mode="human", rule="renju")

black_agent = RandomAgent(Cell.BLACK)
white_agent = RandomAgent(Cell.WHITE)
agents = {
    Cell.BLACK: black_agent, 
    Cell.WHITE: white_agent,
    }

obs, info = env.reset()

done = False
truncated = False
step_count = 0

while not (done or truncated):
    current_player = obs['current_player']
    action = agents[current_player].act(obs)

    if action is None:
        print("Draw!")
        break

    obs, reward, done, truncated, info = env.step(action)
    # if info['valid'] and info['placed']:
    #     step_count += 1
    #     print(f"Step {step_count}: Player {obs['current_player']}")
    #     print(f"- observation")
    #     print(obs)
    #     print(f"- information")
    #     print(info)
    #     print("-------------------------------------------")
    # elif not info["valid"]:
    #     print(f"Step {step_count}: Player {obs['current_player']}")
    #     print(f"- observation")
    #     print(obs)
    #     print(f"- information")
    #     print(info)
    #     print("-------------------------------------------")

    if done:
        if reward == 1:
            print(f"Winner: Player {info['winner']}")
            break

env.close()