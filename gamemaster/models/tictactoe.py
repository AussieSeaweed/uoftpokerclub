from gameframe.tictactoe import TicTacToeGame

from gamemaster.exceptions import GameCreationException
from gamemaster.models.sequential import SequentialRoom


class TicTacToeRoom(SequentialRoom):
    @property
    def seat_count(self):
        return 2

    @property
    def game_name(self):
        return 'Tic Tac Toe'

    def create_game(self):
        if self.user_count == 2:
            return TicTacToeGame()
        else:
            raise GameCreationException

    class Meta:
        verbose_name = 'Tic Tac Toe Room'
