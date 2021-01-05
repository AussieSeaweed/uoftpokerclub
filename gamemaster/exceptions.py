from collections.abc import Sequence

__all__: Sequence[str] = ['GameMasterException', 'GameCreationException', 'SeatNotFoundException', 'NoEmptySeatException']


class GameMasterException(Exception):
    pass


class GameCreationException(GameMasterException):
    pass


class SeatNotFoundException(GameMasterException):
    pass


class NoEmptySeatException(GameMasterException):
    pass
