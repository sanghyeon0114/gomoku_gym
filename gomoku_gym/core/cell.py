from enum import IntEnum

class Cell(IntEnum):
    EMPTY = 0   # Empty
    BLACK = 1   # Black Stone
    WHITE = 2   # White Stone
    THREE = 3   # 33 (Renju, Black only)
    FOUR = 4    # 44 (Renju, Black only)
    FIVE = 5    # 5
    SIX_OVER = 6     # Overline (Renju, Black only)
