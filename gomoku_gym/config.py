class Config:
    TITLE = "Gomoku Game"
    STONE_SIZE = 64
    GRID_SIZE = STONE_SIZE - 10
    BOARD_SIZE = 15
    MARGIN = 40
    WINDOW_SIZE = GRID_SIZE * (BOARD_SIZE - 1) + MARGIN * 2
    LINE_COLOR = (0, 0, 0)
    BG_COLOR = (205, 170, 125)

    # Stone Color
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    BOARD_IMAGE = "gomoku_gym/images/board/board_background.png"
    BLACK_IMAGE = "gomoku_gym/images/stones/black_stone.png"
    WHITE_IMAGE = "gomoku_gym/images/stones/white_stone.png"
    FORBIDDEN_THREE_IMAGE = "gomoku_gym/images/rules/forbidden_three.png"
    FORBIDDEN_FOUR_IMAGE = "gomoku_gym/images/rules/forbidden_four.png"
    FORBIDDEN_SIX_OVER_IMAGE = "gomoku_gym/images/rules/forbidden_six_over.png"