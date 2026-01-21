from gomoku_gym.config import Config
from gomoku_gym.core.cell import Cell

class BaseRules(object):
    def __init__(self,):
        pass
    
    def is_valid(self, board, position):
        x, y = position
        if not (0 <= x < Config.BOARD_SIZE and 0 <= y < Config.BOARD_SIZE):
            return False
        if not self.is_blank(board, position):
            return False
        return True

    def is_blank(self, board, position):
        x, y = position
        return board[x][y] == Cell.EMPTY
    
    def is_black(self, board, position):
        x, y = position
        return board[x][y] == Cell.BLACK
    
    def is_whilte(self, board, position):
        x, y = position
        return board[x][y] == Cell.WHITE

    def is_five_stone(self, board, current_position, current_player) -> bool:
        row, col = current_position
        def count(direction):
            dr, dc = direction
            r, c = row + dr, col + dc
            count = 0
            while 0 <= r < Config.BOARD_SIZE and 0 <= c < Config.BOARD_SIZE and board[r, c] == current_player:
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