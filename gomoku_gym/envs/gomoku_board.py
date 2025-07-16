import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
import sys

from gomoku_gym.config import Config

class GomokuBoardEnv(gym.Env):
    metadata = {
        "render_modes": ["human", "gomoku_array"], 
        "player_count": [0, 1, 2],
        "player": ["black", "white"],
        "render_fps": 10,
    }
    

    def __init__(self, render_mode=None, player_count=0, player="black", is_random=False):
        self.board_size = Config.BOARD_SIZE
        self.window_size = Config.WINDOW_SIZE
        
        self.observation_space = spaces.Box(
            low=0, high=2, shape=(self.board_size, self.board_size), dtype=np.int8
        )

        self.action_space = spaces.MultiDiscrete([self.board_size, self.board_size])

        self.board = np.zeros((self.board_size, self.board_size), dtype=np.int8)
        self.current_player = 1  # 1: black, 2: white
        self.done = False
        self.winner = None
    
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        assert player_count is None or player_count in self.metadata["player_count"]
        self.player_count = player_count

        
        assert player is None or player in self.metadata["player"]
        self.human_player = None
        if self.player_count == 1:
            self.human_player = player

        self.window = None
        self.clock = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.board = np.zeros((self.board_size, self.board_size), dtype=np.int8)
        self.current_player = 1
        self.done = False
        self.winner = None

        if self.render_mode == "human":
            self._render_frame()

        return self._get_obs(), self._get_info()

    def _get_obs(self):
        return {
            "board": self.board.copy(),
            "current_player": self.current_player
        }

    def _get_info(self, placed=False, valid=True):
        return {
            "valid": valid,
            "winner": self.winner,
            "done": self.done,
            "placed": placed,
            "num_moves": np.count_nonzero(self.board)
        }

    def _get_position(self, pos):
        mx, my = pos
        return round((mx - Config.MARGIN) / Config.GRID_SIZE), round((my - Config.MARGIN) / Config.GRID_SIZE)

    # private
    def _check_place(self, pos):
        row, col = pos
        return (0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == 0)

    # public
    def check_place(self, pos):
        row, col = pos
        return (0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == 0)

    def _get_mouse_input(self,):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN :
                col, row = self._get_position(pygame.mouse.get_pos())
                if self._check_place((row, col)):
                    return (row, col)
        return None

    def _handle_single_player(self, action):
        if (self.current_player == 1 and self.human_player == "black") or (self.current_player == 2 and self.human_player == "white"):
            return self._get_mouse_input()
        else:
            return action
    
    def _handle_player_vs_player(self,):
        return self._get_mouse_input()
    
    def _handle_action(self, action):
        if self.player_count == 0:
            return action
        if self.player_count == 1:
            return self._handle_single_player(action)
        if self.player_count == 2:
            return self._handle_player_vs_player()

    def step(self, input_action=None):
        if self.done:
            return self._get_obs(), 0, True, False, self._get_info()

        action = self._handle_action(input_action)

        if action is None:
            return self._get_obs(), 0, self.done, False, self._get_info()

        row, col = action

        if self.board[row, col] != 0:
            return self._get_obs(), -1, False, False, self._get_info(valid=False)

        current = self.current_player
        self.board[row, col] = current

        if self._check_win(row, col):
            self.done = True
            self.winner = self.current_player
            reward = 1
        else:
            reward = 0
            self.current_player = 2 if self.current_player == 1 else 1

        if self.render_mode == "human":
            self._render_frame()

        obs = {
            "board": self.board.copy(),
            "current_player": current,
        }

        return obs, reward, self.done, False, self._get_info(placed=True)

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size), pygame.NOFRAME)
            pygame.display.set_caption(Config.TITLE)

            self.board_image = pygame.image.load(Config.BOARD_IMAGE).convert()
            self.board_image = pygame.transform.scale(self.board_image, (Config.WINDOW_SIZE, Config.WINDOW_SIZE))

            self.black_stone_img = pygame.image.load(Config.BLACK_IMAGE).convert_alpha()
            self.white_stone_img = pygame.image.load(Config.WHITE_IMAGE).convert_alpha()

            self.black_stone_img = pygame.transform.scale(self.black_stone_img, (Config.STONE_SIZE, Config.STONE_SIZE))
            self.white_stone_img = pygame.transform.scale(self.white_stone_img, (Config.STONE_SIZE, Config.STONE_SIZE))

        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        self.window.blit(self.board_image, (0, 0))

        for y in range(self.board_size):
            for x in range(self.board_size):
                stone = self.board[y][x]
                if stone != 0:
                    center = (
                        Config.MARGIN + x * Config.GRID_SIZE,
                        Config.MARGIN + y * Config.GRID_SIZE,
                    )
                    img = self.black_stone_img if stone == 1 else self.white_stone_img
                    rect = img.get_rect(center=center)
                    self.window.blit(img, rect)

        pygame.display.update()
        self.clock.tick(self.metadata["render_fps"])

    def _check_win(self, row, col):
        def count(direction):
            dr, dc = direction
            r, c = row + dr, col + dc
            count = 0
            while 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r, c] == self.current_player:
                count += 1
                r += dr
                c += dc
            return count

        directions = [(-1, 0), (0, -1), (-1, -1), (-1, 1)]
        for dr, dc in directions:
            total = 1 + count((dr, dc)) + count((-dr, -dc))
            if total >= 5:
                return True
        return False

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

