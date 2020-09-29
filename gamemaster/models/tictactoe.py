from gameservice.tictactoe.game import TicTacToeGame

from .sequential import SequentialRoom
from ..exceptions import GameCreationException


class TicTacToeRoom(SequentialRoom):
    description = "Tic Tac Toe"
    num_seats = 2

    def create_game(self):
        if len(self.users) < 2:
            raise GameCreationException

        self.game = TicTacToeGame(labels=[user.username for user in self.users])
        self.save()
