from gomoku_gym.envs.gomoku_board import GomokuBoardEnv
import time

env = GomokuBoardEnv(
    render_mode="human", # possible ["human", "gomoku_array"]
    player_count=1, # possible [0, 1, 2]
    player="black", # "black" or "white" ( only possible. when player_count is 1. )
)

obs, info = env.reset()

done = False
step_count = 0

while not done:
    while True:
        action = env.action_space.sample()
        if env.check_place(action):
            break

    obs, reward, done, truncated, info = env.step(action)

    if info['valid'] and info['placed']:
        step_count += 1
        print(f"Step {step_count}: Player {obs['current_player']}")
        print(f"- observation")
        print(obs)
        print(f"- information")
        print(info)
        print("-------------------------------------------")
    elif not info["valid"]:
        print(f"Step {step_count}: Player {obs['current_player']}")
        print(f"- observation")
        print(obs)
        print(f"- information")
        print(info)
        print("-------------------------------------------")

    if reward == 1:
        print(f"Winner: Player {info['winner']}")
        break

env.close()