from gameservice.tictactoe.game import TicTacToeGame

from .room import Room
from ..exceptions import GameCreationException


class TicTacToeRoom(Room):
    description = "Tic Tac Toe"
    num_seats = 2

    def create_game(self):
        if len(self.users) < 2:
            raise GameCreationException

        self.game = TicTacToeGame(labels=list(user.username for user in self.users))
        self.save()
