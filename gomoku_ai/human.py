class Human:
    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board, is_selfplay=None, print_probs_value=None):
        try:
            location = input("Your move: ")
            location = [int(n) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move, _ = self.get_action(board)
        return move, None

    def __str__(self):
        return "Human {}".format(self.player)
