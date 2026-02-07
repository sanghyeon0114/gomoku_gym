import numpy as np

class AlphaZeroAgent:
    def __init__(self, player_color, board_size=15):
        self.player_color = player_color
        self.board_size = board_size
        # self.model = load_model()

    def act(self, state):
        board = state['board']
        
        valid_positions = np.argwhere(board == 0)

        if len(valid_positions) == 0:
            return None
        
        random_idx = np.random.randint(len(valid_positions))
        row, col = valid_positions[random_idx]

        return (int(row), int(col))

    def simulate(self, state):
        pass

    def _state_to_tensor(self, state):
        pass