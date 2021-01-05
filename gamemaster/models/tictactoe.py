from gameframe.tictactoe import TicTacToeGame

from gamemaster.models.sequential import SequentialRoom

__all__ = ['TicTacToeRoom']


class TicTacToeRoom(SequentialRoom):
    def create_game(self):
        return TicTacToeGame()
