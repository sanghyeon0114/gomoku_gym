import gymnasium as gym
from gymnasium import spaces
import pygame
import numpy as np
import sys

from gomoku_gym.config import Config
from gomoku_gym.rules.renju_rules import BaseRules, RenjuRules
from gomoku_gym.core.cell import Cell

class GomokuBoardEnv(gym.Env):
    metadata = {
        "render_modes": ["human", "gomoku_array"], 
        "player_count": [0, 1, 2],
        "player": ["black", "white"],
        "rules": ["basic", "renju"],
        "render_fps": 10,
    }
    

    def __init__(self, render_mode=None, player_count=0, player="black", is_random=False, rule='renju'):
        self.board_size = Config.BOARD_SIZE
        self.window_size = Config.WINDOW_SIZE
        
        self.observation_space = spaces.Dict({
            "board": spaces.Box(low=0, high=2, shape=(self.board_size, self.board_size), dtype=np.int8),
            "forbidden": spaces.Box(low=0, high=2, shape=(self.board_size, self.board_size), dtype=np.int8),
            "current_player": spaces.Discrete(3),
            "last_position": spaces.Box(low=-1, high=self.board_size - 1, shape=(2,), dtype=np.int8),
        })

        self.action_space = spaces.MultiDiscrete([self.board_size, self.board_size])

        self.board = np.full((self.board_size, self.board_size), Cell.EMPTY, dtype=np.int8)
        self.forbidden_board = np.full((self.board_size, self.board_size), Cell.EMPTY, dtype=np.int8)
        self.current_player = Cell.BLACK
        self.last_position = np.array([-1, -1], dtype=np.int8)
        self.done = False
        self.winner = None
    
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        assert player_count in self.metadata["player_count"]
        self.player_count = player_count

        assert player in self.metadata["player"]
        self.human_player = None
        if self.player_count == 1:
            self.human_player = player
        
        assert rule in self.metadata["rules"]
        if rule == "basic":
            self.rule = BaseRules()
        elif rule == "renju":
            self.rule = RenjuRules()

        self.window = None
        self.clock = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.board = np.full((self.board_size, self.board_size), Cell.EMPTY, dtype=np.int8)
        self.forbidden_board = np.full((self.board_size, self.board_size), Cell.EMPTY, dtype=np.int8)
        self.current_player = Cell.BLACK
        self.last_position = np.array([-1, -1], dtype=np.int8)
        self.done = False
        self.winner = None

        if self.render_mode == "human":
            self._render_frame()

        return self._get_obs(), self._get_info()

    def _get_obs(self):
        return {
            "board": self.board.copy(),
            "forbidden": self.forbidden_board.copy(),
            "current_player": self.current_player,
            "last_position": self.last_position
        }

    def _get_info(self, placed=False, valid=True):
        return {
            "valid": valid,
            "winner": self.winner,
            "done": self.done,
            "placed": placed,
            "num_moves": np.sum((self.board == Cell.BLACK) | (self.board == Cell.WHITE))
        }

    def _get_position(self, pos):
        mx, my = pos
        return round((mx - Config.MARGIN) / Config.GRID_SIZE), round((my - Config.MARGIN) / Config.GRID_SIZE)

    def _is_valid_position(self, pos):
        return self.rule.is_valid(self.board, pos, self.current_player)

    def _update_forbidden_board(self, pos):
        dirs = [
            (-1, -1), (1, 1),
            (-1, 0),  (1, 0),
            (0, -1),  (0, 1),
        ]

        for dx, dy in dirs:
            x, y = pos
            while self.rule.is_valid_position((x, y)):
                if self.forbidden_board[x][y] == Cell.EMPTY:
                    self.forbidden_board[x][y] = self.rule.checkForbiddenMove(
                        self.board, (x, y), self.current_player
                    )
                x += dx
                y += dy


    def _get_mouse_input(self,):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN :
                col, row = self._get_position(pygame.mouse.get_pos())
                if self._is_valid_position((row, col)):
                    return (row, col)
        return None

    def _handle_single_player(self, action):
        if (self.current_player == Cell.BLACK and self.human_player == "black") or (self.current_player == Cell.WHITE and self.human_player == "white"):
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

        if not self._is_valid_position(action):
            return self._get_obs(), -1, False, False, self._get_info(valid=False)

        row, col = action

        current = self.current_player
        self.last_position = np.array([row, col], dtype=np.int8)
        if current == 1:
            self.board[row, col] = self.forbidden_board[row, col] =  Cell.BLACK
            self._update_forbidden_board((row, col))
        elif current == 2:
            self.board[row, col] = self.forbidden_board[row, col] =  Cell.WHITE

        if self._check_win(action):
            self.done = True
            self.winner = self.current_player
            reward = 1
        else:
            reward = 0
            self.current_player = Cell.WHITE if self.current_player == Cell.BLACK else Cell.BLACK

        if self.render_mode == "human":
            self._render_frame()

        obs = {
            "board": self.board.copy(),
            "forbidden": self.forbidden_board.copy(),
            "current_player": current,
            "last_position": self.last_position
        }

        return obs, reward, self.done, False, self._get_info(placed=True)

    def render(self):
        if self.render_mode == "human":
            return self._render_frame()

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
            self.forbidden_three_img = pygame.image.load(Config.FORBIDDEN_THREE_IMAGE).convert_alpha()
            self.forbidden_four_img = pygame.image.load(Config.FORBIDDEN_FOUR_IMAGE).convert_alpha()
            self.forbidden_six_over_img = pygame.image.load(Config.FORBIDDEN_SIX_OVER_IMAGE).convert_alpha()

            self.black_stone_img = pygame.transform.scale(self.black_stone_img, (Config.STONE_SIZE, Config.STONE_SIZE))
            self.white_stone_img = pygame.transform.scale(self.white_stone_img, (Config.STONE_SIZE, Config.STONE_SIZE))

            self.forbidden_three_img = pygame.transform.scale(self.forbidden_three_img, (Config.STONE_SIZE, Config.STONE_SIZE))
            self.forbidden_four_img = pygame.transform.scale(self.forbidden_four_img, (Config.STONE_SIZE, Config.STONE_SIZE))
            self.forbidden_six_over_img = pygame.transform.scale(self.forbidden_six_over_img, (Config.STONE_SIZE, Config.STONE_SIZE))

        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        self.window.blit(self.board_image, (0, 0))

        for y in range(self.board_size):
            for x in range(self.board_size):
                stone = self.board[y][x]
                if stone != Cell.EMPTY:
                    center = (
                        Config.MARGIN + x * Config.GRID_SIZE,
                        Config.MARGIN + y * Config.GRID_SIZE,
                    )
                    img = self.black_stone_img if stone == Cell.BLACK else self.white_stone_img
                    rect = img.get_rect(center=center)
                    self.window.blit(img, rect)

        if isinstance(self.rule, RenjuRules) and self.current_player == Cell.BLACK:
            for y in range(self.board_size):
                for x in range(self.board_size):
                    if self.board[y][x] != Cell.EMPTY:
                        continue

                    forbidden = self.forbidden_board[y][x]

                    if forbidden is Cell.EMPTY:
                        continue

                    center = (
                        Config.MARGIN + x * Config.GRID_SIZE,
                        Config.MARGIN + y * Config.GRID_SIZE,
                    )

                    if forbidden == Cell.THREE:
                        img = self.forbidden_three_img
                    elif forbidden == Cell.FOUR:
                        img = self.forbidden_four_img
                    elif forbidden == Cell.SIX_OVER:
                        img = self.forbidden_six_over_img
                    else:
                        continue
                    rect = img.get_rect(center=center)
                    self.window.blit(img, rect)

        pygame.display.update()
        self.clock.tick(self.metadata["render_fps"])

    def _check_win(self, position):
        return self.rule.is_five(self.board, position, self.current_player)

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

