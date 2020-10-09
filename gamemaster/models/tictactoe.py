from gameservice.tictactoe.game import TicTacToeGame

from .sequential import SequentialRoom


class TicTacToeRoom(SequentialRoom):
    description = "Tic Tac Toe"
    num_seats = 2

    req_num_players = 2
    game_type = TicTacToeGame

    class Meta:
        verbose_name = "Tic Tac Toe Room"
