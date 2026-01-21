from gomoku_gym.config import Config
from gomoku_gym.core.cell import Cell
from gomoku_gym.rules.base_rules import BaseRules

class RenjuRules(BaseRules):
    def __init__(self,):
        self.directions = [
            (1, 0),
            (0, 1),
            (1, 1),
            (1, -1),
        ]

    def is_valid(self, board, position):
        x, y = position
        if not (0 <= x < Config.BOARD_SIZE and 0 <= y < Config.BOARD_SIZE):
            return False
        if not self.is_blank(board, position):
            return False
        return True

    def is_player_stone(self, board, position, player):
        x, y = position
        return board[x][y] == player

    def _is_five(self, board, position, player, direction_index):
        x, y = position
        dx, dy = self.directions[direction_index]
        
        tmp = board[x][y]
        board[x][y] = player
        stone_count = 1

        current_x, current_y = x, y
        current_x += dx
        current_y += dy
        while self.is_in_position((current_x, current_y)):
            if self.is_player_stone(board, (current_x, current_y), player):
                stone_count+=1
            else:
                break
            current_x += dx
            current_y += dy
        
        current_x, current_y = x, y
        current_x -= dx
        current_y -= dy
        while self.is_in_position((current_x, current_y)):
            if self.is_player_stone(board, (current_x, current_y), player):
                stone_count+=1
            else:
                break
            current_x -= dx
            current_y -= dy

        board[x][y] = tmp
        return (player == Cell.BLACK and stone_count == 5) or (player == Cell.WHITE and stone_count >= 5)
    
    def is_five(self, board, position, player):
        return self._is_five(board, position, player, 0) or self._is_five(board, position, player, 1) or self._is_five(board, position, player, 2) or self._is_five(board, position, player, 3)


        