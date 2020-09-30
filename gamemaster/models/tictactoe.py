from gameservice.tictactoe.game import TicTacToeGame

from .sequential import SequentialRoom
from ..exceptions import GameCreationException


class TicTacToeRoom(SequentialRoom):
    description = "Tic Tac Toe"
    num_seats = 2

    """Constant methods/Properties"""

    def create_game(self):
        users = list(filter(lambda seat: seat.status == "Online", self.seats.all()))

        if len(users) < 2:
            raise GameCreationException

        return TicTacToeGame(labels=[user.username for user in users])
