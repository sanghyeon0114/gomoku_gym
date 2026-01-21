from gomoku_gym.config import Config
from gomoku_gym.rules.base_rules import BaseRules

class RenjuRules(BaseRules):
    def __init__(self,):
        pass

    def is_valid(self, board, position):
        x, y = position
        if not (0 <= x < Config.BOARD_SIZE and 0 <= y < Config.BOARD_SIZE):
            return False
        if not self.is_blank(board, position):
            return False
        return True

    def is_open_three(self, board, position):
        x, y = position

    def is_double_three(self, board, position):
        x, y = position

    def is_four(self, board, position):
        x, y = position

    def is_double_four(self, board, position):
        x, y = position

    def is_six(self, board, position):
        x, y = position