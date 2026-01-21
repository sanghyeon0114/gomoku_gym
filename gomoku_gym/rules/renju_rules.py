from gomoku_gym.config import Config
from gomoku_gym.core.cell import Cell
from gomoku_gym.rules.base_rules import BaseRules

# todo : 백준을 통해 Renju 검증

class RenjuRules(BaseRules):
    DIRECTIONS = [
        (1, 0),
        (0, 1),
        (1, 1),
        (1, -1),
    ]

    def __init__(self):
        super().__init__()

    def is_valid(self, board, position, player):
        x, y = position
        if not (0 <= x < Config.BOARD_SIZE and 0 <= y < Config.BOARD_SIZE):
            return False
        if not self.is_blank(board, position):
            return False

        cell_number = self.checkForbiddenMove(board, position, player)
        return cell_number == Cell.EMPTY or cell_number == Cell.FIVE

    def is_player_stone(self, board, position, player):
        x, y = position
        return board[x][y] == player

    def is_blank(self, board, position):
        x, y = position
        return board[x][y] == Cell.EMPTY

    def is_black(self, board, position):
        x, y = position
        return board[x][y] == Cell.BLACK

    def is_white(self, board, position):
        x, y = position
        return board[x][y] == Cell.WHITE

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < Config.BOARD_SIZE and 0 <= y < Config.BOARD_SIZE

    def checkForbiddenMove(self, board, position, player):
        if player != Cell.BLACK:
            return Cell.EMPTY

        if self.is_five(board, position, player):
            return Cell.FIVE
        elif self.is_six_over(board, position, player):
            return Cell.SIX_OVER
        elif self.is_double_four(board, position, player):
            return Cell.FOUR
        elif self.is_double_open_three(board, position, player):
            return Cell.THREE
        return Cell.EMPTY

    def _is_five(self, board, position, player, direction_index):
        dx, dy = self.DIRECTIONS[direction_index]
        x, y = position

        tmp = board[x][y]
        board[x][y] = Cell.BLACK

        stone_count = 1

        cx, cy = x, y
        while True:
            cx += dx
            cy += dy
            if not (0 <= cx < Config.BOARD_SIZE and 0 <= cy < Config.BOARD_SIZE):
                break
            if board[cx][cy] == Cell.BLACK:
                stone_count += 1
            else:
                break

        cx, cy = x, y
        while True:
            cx -= dx
            cy -= dy
            if not (0 <= cx < Config.BOARD_SIZE and 0 <= cy < Config.BOARD_SIZE):
                break
            if board[cx][cy] == Cell.BLACK:
                stone_count += 1
            else:
                break

        board[x][y] = tmp
        return stone_count == 5

    def is_five(self, board, position, player):
        return any(self._is_five(board, position, player, d) for d in range(len(self.DIRECTIONS)))

    def _is_six_over(self, board, position, direction_index):
        dx, dy = self.DIRECTIONS[direction_index]
        x, y = position

        tmp = board[x][y]
        board[x][y] = Cell.BLACK

        stone_count = 1

        cx, cy = x, y
        while True:
            cx += dx
            cy += dy
            if not (0 <= cx < Config.BOARD_SIZE and 0 <= cy < Config.BOARD_SIZE):
                break
            if board[cx][cy] == Cell.BLACK:
                stone_count += 1
            else:
                break

        cx, cy = x, y
        while True:
            cx -= dx
            cy -= dy
            if not (0 <= cx < Config.BOARD_SIZE and 0 <= cy < Config.BOARD_SIZE):
                break
            if board[cx][cy] == Cell.BLACK:
                stone_count += 1
            else:
                break

        board[x][y] = tmp
        return stone_count > 5

    def is_six_over(self, board, position, player):
        if player != Cell.BLACK:
            return False
        return any(self._is_six_over(board, position, d) for d in range(len(self.DIRECTIONS)))

    def is_four(self, board, position, direction_index):
        if self.is_five(board, position, Cell.BLACK) or self.is_six_over(board, position, Cell.BLACK):
            return 0

        dx, dy = self.DIRECTIONS[direction_index]
        x, y = position

        tmp = board[x][y]
        board[x][y] = Cell.BLACK

        five_count = 0

        cx, cy = x, y
        while True:
            cx += dx
            cy += dy
            if not (0 <= cx < Config.BOARD_SIZE and 0 <= cy < Config.BOARD_SIZE):
                break

            if board[cx][cy] == Cell.WHITE:
                break
            elif board[cx][cy] == Cell.EMPTY:
                if self._is_five(board, (cx, cy), Cell.BLACK, direction_index):
                    five_count += 1
                break

        cx, cy = x, y
        while True:
            cx -= dx
            cy -= dy
            if not (0 <= cx < Config.BOARD_SIZE and 0 <= cy < Config.BOARD_SIZE):
                break

            if board[cx][cy] == Cell.WHITE:
                break
            elif board[cx][cy] == Cell.EMPTY:
                if self._is_five(board, (cx, cy), Cell.BLACK, direction_index):
                    five_count += 1
                break

        board[x][y] = tmp

        if five_count == 2 and self.is_open_four(board, position, direction_index):
            return 1
        return five_count

    def is_open_four(self, board, position, direction_index):
        if self.is_five(board, position, Cell.BLACK) or self.is_six_over(board, position, Cell.BLACK):
            return False

        dx, dy = self.DIRECTIONS[direction_index]
        x, y = position

        tmp = board[x][y]
        board[x][y] = Cell.BLACK

        five_count = 0
        stone_count = 1

        cx, cy = x, y
        while True:
            cx += dx
            cy += dy
            if not (0 <= cx < Config.BOARD_SIZE and 0 <= cy < Config.BOARD_SIZE):
                break

            if board[cx][cy] == Cell.WHITE:
                board[x][y] = tmp
                return False
            elif board[cx][cy] == Cell.EMPTY:
                if self._is_five(board, (cx, cy), Cell.BLACK, direction_index):
                    five_count += 1
                    break
                else:
                    board[x][y] = tmp
                    return False
            elif board[cx][cy] == Cell.BLACK:
                stone_count += 1

        cx, cy = x, y
        while True:
            cx -= dx
            cy -= dy
            if not (0 <= cx < Config.BOARD_SIZE and 0 <= cy < Config.BOARD_SIZE):
                break

            if board[cx][cy] == Cell.WHITE:
                board[x][y] = tmp
                return False
            elif board[cx][cy] == Cell.EMPTY:
                if self._is_five(board, (cx, cy), Cell.BLACK, direction_index):
                    five_count += 1
                    break
                else:
                    board[x][y] = tmp
                    return False
            elif board[cx][cy] == Cell.BLACK:
                stone_count += 1

        board[x][y] = tmp
        return five_count == 2 and stone_count == 4

    def is_double_four(self, board, position, player):
        if player != Cell.BLACK:
            return False
        five_count = 0
        for d in range(len(self.DIRECTIONS)):
            five_count += self.is_four(board, position, d)
        return five_count >= 2

    def is_open_three(self, board, position, direction_index):
        if (self.is_five(board, position, Cell.BLACK)
                or self.is_six_over(board, position, Cell.BLACK)
                or self.is_double_four(board, position, Cell.BLACK)):
            return False

        dx, dy = self.DIRECTIONS[direction_index]
        x, y = position

        tmp = board[x][y]
        board[x][y] = Cell.BLACK

        cx, cy = x, y
        while True:
            cx += dx
            cy += dy
            if not (0 <= cx < Config.BOARD_SIZE and 0 <= cy < Config.BOARD_SIZE):
                break

            if board[cx][cy] == Cell.WHITE:
                board[x][y] = tmp
                return False
            elif board[cx][cy] == Cell.EMPTY:
                if self.is_open_four(board, (cx, cy), direction_index):
                    if (not self.is_five(board, (cx, cy), Cell.BLACK)
                            and not self.is_six_over(board, (cx, cy), Cell.BLACK)
                            and not self.is_double_four(board, (cx, cy), Cell.BLACK)
                            and not self.is_double_open_three(board, (cx, cy), Cell.BLACK)):
                        board[x][y] = tmp
                        return True
                break

        cx, cy = x, y
        while True:
            cx -= dx
            cy -= dy
            if not (0 <= cx < Config.BOARD_SIZE and 0 <= cy < Config.BOARD_SIZE):
                break

            if board[cx][cy] == Cell.WHITE:
                board[x][y] = tmp
                return False
            elif board[cx][cy] == Cell.EMPTY:
                if self.is_open_four(board, (cx, cy), direction_index):
                    if (not self.is_five(board, (cx, cy), Cell.BLACK)
                            and not self.is_six_over(board, (cx, cy), Cell.BLACK)
                            and not self.is_double_four(board, (cx, cy), Cell.BLACK)
                            and not self.is_double_open_three(board, (cx, cy), Cell.BLACK)):
                        board[x][y] = tmp
                        return True
                break

        board[x][y] = tmp
        return False

    def is_double_open_three(self, board, position, player):
        if player != Cell.BLACK:
            return False
        open_three_count = 0
        for d in range(len(self.DIRECTIONS)):
            if self.is_open_three(board, position, d):
                open_three_count += 1
        return open_three_count >= 2
