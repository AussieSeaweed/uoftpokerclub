from collections.abc import Sequence

from gameframe.tictactoe import TicTacToeGame

from gamemaster.exceptions import GameCreationException
from gamemaster.models.sequential import SequentialRoom

__all__: Sequence[str] = ['TicTacToeRoom']


class TicTacToeRoom(SequentialRoom[TicTacToeGame]):
    seat_count: int = 2

    def create_game(self) -> TicTacToeGame:
        if self.user_count == 2:
            return TicTacToeGame()
        else:
            raise GameCreationException

    class Meta:
        verbose_name: str = 'Tic Tac Toe Room'
