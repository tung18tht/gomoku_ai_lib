from game_board import Board, Game
from human import Human
from mcts_pure import MCTSPlayer as MCTS_pure
from mcts_alphaZero import MCTSPlayer
from policy_value_net_tensorlayer import PolicyValueNet


if __name__ == '__main__':
    # mcts_player = MCTS_pure(5,400)

    best_policy = PolicyValueNet(
        board_width=15, board_height=15, block=19, init_model="model/model")
    alpha_zero_player = MCTSPlayer(
        policy_value_function=best_policy.policy_value_fn_random,
        action_fc=best_policy.action_fc_test,
        evaluation_fc=best_policy.evaluation_fc2_test,
        c_puct=5,
        n_playout=400,
        is_selfplay=False
    )

    human = Human()

    game = Game(Board())
    game.start(human, alpha_zero_player)
    game.graphic()

    while True:
        current_player = game.board.get_current_player()
        player_in_turn = game.players[current_player]
        move, _ = player_in_turn.get_action(game.board)

        game.board.do_move(move)

        game.graphic()

        end, _ = game.board.game_end()

        if end:
            break
