from gameservice.tictactoe.game import TicTacToeGame

from .sequential import SequentialRoom


class TicTacToeRoom(SequentialRoom):
    description = "Tic Tac Toe"
    num_seats = 2

    req_num_players = 2
    game_type = TicTacToeGame

    """Django Templates"""

    @property
    def stylesheet_paths(self):
        return [
            *super().stylesheet_paths,
            "gamemaster/stylesheets/tictactoe.css",
        ]

    @property
    def javascript_paths(self):
        return [
            *super().javascript_paths,
            "gamemaster/javascripts/tictactoe.js",
        ]

    class Meta:
        verbose_name = "Tic Tac Toe Room"
