from gameservice.tictactoe.game import TicTacToeGame

from .sequential import SequentialRoom
from ..exceptions import GameCreationException


class TicTacToeRoom(SequentialRoom):
    description = "Tic Tac Toe"
    num_seats = 2

    def create_game(self):
        users = [seat.user for seat in self.seats.all() if seat.status == "Online"]

        if len(users) < 2:
            raise GameCreationException

        self.game = TicTacToeGame(labels=[user.username for user in self.users])
        self.save()
