# Gomoku-Gym

Gomoku-Gym is a custom reinforcement learning environment for playing the classic game Gomoku, built using [Gymnasium](https://github.com/Farama-Foundation/Gymnasium).

## Installation

To install your new environment, run the following commands:

```shell
make
pip install -e .
make run
```

## Usage

1. a sample example to run a random vs. random game:

```python
import gymnasium as gym

env = gym.make("gomoku_gym/GomokuBoardEnv-v0", render_mode="human", player_count=0)
obs, info = env.reset()

done = False
while not done:
    action = env.action_space.sample()
    obs, reward, done, _, info = env.step(action)
```

2. a sample example to run a player vs. random game:

```python
import gymnasium as gym

env = gym.make("gomoku_gym/GomokuBoardEnv-v0", render_mode="human", player_count=1, player="black")
obs, info = env.reset()

done = False
while not done:
    action = env.action_space.sample()
    obs, reward, done, _, info = env.step(action)
```

3. a sample example to run a player vs. player game:

```python
import gymnasium as gym

env = gym.make("gomoku_gym/GomokuBoardEnv-v0", render_mode="human", player_count=2)
obs, info = env.reset()

done = False
while not done:
    action = env.action_space.sample()
    obs, reward, done, _, info = env.step(action)
```