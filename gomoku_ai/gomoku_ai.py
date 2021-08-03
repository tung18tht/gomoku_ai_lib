from pathlib import Path

from .game_board import Board, Game
from .mcts_alphaZero import MCTSPlayer
from .policy_value_net_tensorlayer import PolicyValueNet


class BlankHuman:
    def __init__(self):
        self.player = None

    def set_player_ind(self, index):
        self.player = index

    def get_action(self, board, is_selfplay=None, print_probs_value=None):
        raise NotImplementedError

    def __str__(self):
        return f"BlankHuman {self.player}"


class GomokuAI:
    def __init__(self):
        current_dir = Path(__file__).parent.absolute()
        model_path = f"{current_dir}/model/model"
        self._policy_value_net = PolicyValueNet(
            board_width=15, board_height=15, block=19, init_model=model_path)
        self._games = {}

    def start_game(self, id, human_play_first=False):
        if id in self._games:
            raise ValueError("ID already existed!")

        blank_human = BlankHuman()
        alpha_zero = MCTSPlayer(
            policy_value_function=self._policy_value_net.policy_value_fn_random,
            action_fc=self._policy_value_net.action_fc_test,
            evaluation_fc=self._policy_value_net.evaluation_fc2_test,
            c_puct=5,
            n_playout=400,
            is_selfplay=False
        )

        game = Game(Board())
        game.ai_player = alpha_zero

        if human_play_first:
            game.start(blank_human, alpha_zero)
        else:
            game.start(alpha_zero, blank_human)

        self._games[id] = game

    def end_game(self, id):
        if id not in self._games:
            raise ValueError("ID not found!")

        del self._games[id]

    def get_ai_move(self, id, human_move):
        if id not in self._games:
            raise ValueError("ID not found!")

        game = self._games[id]

        if human_move is not None:
            move = game.board.location_to_move(human_move)
            if move == -1 or move not in game.board.availables:
                raise ValueError("Invalid move!")

            game.board.do_move(move)
            end, _ = game.board.game_end()
            if end:
                del self._games[id]
                return None

        move, _ = game.ai_player.get_action(game.board)
        game.board.do_move(move)

        end, _ = game.board.game_end()
        if end:
            del self._games[id]

        return game.board.move_to_location(move)
