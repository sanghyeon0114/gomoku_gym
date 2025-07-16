import gymnasium as gym
import gomoku_gym
gomoku_gym.register_envs()

env = gym.make("GomokuBoardEnv-v0", render_mode="human", player_count=1, player="black")

obs, info = env.reset()

done = False
step_count = 0

while not done:
    action = env.action_space.sample()

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