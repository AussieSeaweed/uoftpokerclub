from gameframe.tictactoe import TTTGame

from gamemaster.exceptions import GameCreationException
from gamemaster.models.sequential import SequentialRoom


class TTTRoom(SequentialRoom):
    @property
    def seat_count(self):
        return 2

    @property
    def game_name(self):
        return 'Tic Tac Toe'

    def create_game(self):
        if self.user_count == 2:
            return TTTGame()
        else:
            raise GameCreationException

    class Meta:
        verbose_name = 'Tic Tac Toe Room'
